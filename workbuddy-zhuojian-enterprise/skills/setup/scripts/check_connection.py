"""Anonymous, read-only connection checks. No login, credentials or host changes."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import html
from http.client import HTTPException
import ipaddress
import json
from pathlib import Path
import re
import shutil
import socket
import ssl
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, HTTPSHandler, ProxyHandler, Request, build_opener


SERVER = "zhuojian-enterprise"
MCP_PATH = "/api/v1/enterprise-mcp"
MAX_BYTES = 131072


@dataclass(frozen=True)
class ProbeResponse:
    status: int
    headers: dict
    body: bytes


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # A network login page must never receive a forwarded OAuth request.
        return None


def public_url(value: str, *, endpoint: bool = False) -> str:
    if not isinstance(value, str) or any(c.isspace() for c in value) or "\\" in value:
        raise ValueError("invalid_url")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("invalid_url")
    if parsed.query or parsed.fragment or "?" in value or "#" in value:
        raise ValueError("invalid_url")
    host = parsed.hostname.lower()
    if host == "localhost" or host.endswith((".localhost", ".local", ".invalid")) or "." not in host:
        raise ValueError("invalid_url")
    if parsed.port is not None and not 1 <= parsed.port <= 65535:
        raise ValueError("invalid_url")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    if address is not None and not address.is_global:
        raise ValueError("invalid_url")
    if endpoint and parsed.path != MCP_PATH:
        raise ValueError("invalid_endpoint")
    return value


def origin(value: str) -> str:
    parsed = urlsplit(value)
    return f"{parsed.scheme}://{parsed.hostname}:{parsed.port or (443 if parsed.scheme == 'https' else 80)}"


def fetch_public(url: str, timeout: float) -> ProbeResponse:
    # This enterprise endpoint uses the host's direct domestic route. Never
    # change the OS proxy, trust store, DNS or existing browser connection.
    opener = build_opener(ProxyHandler({}), HTTPSHandler(context=ssl.create_default_context()), NoRedirect())
    request = Request(url, method="GET", headers={
        "Accept": "application/json", "User-Agent": "ZhuoJian-Enterprise-Setup/0.1.2",
    })
    try:
        response = opener.open(request, timeout=timeout)
    except HTTPError as error:
        response = error
    with response:
        return ProbeResponse(response.code, dict(response.headers), response.read(MAX_BYTES + 1))


def native_host_status(expected_endpoint: str | None = None) -> dict:
    executable = shutil.which("codex")
    if not executable:
        return {"available": False}
    try:
        completed = subprocess.run(
            [executable, "mcp", "list", "--json"], capture_output=True,
            encoding="utf-8", errors="replace", timeout=10, check=False,
        )
        if completed.returncode:
            return {"available": False}
        servers = json.loads(completed.stdout)
        if not isinstance(servers, list):
            return {"available": False}
        matches = [item for item in servers if isinstance(item, dict) and item.get("name") == SERVER]
        if not matches:
            return {"available": True, "configured": False}
        server = matches[0]
        status = {"available": True, "configured": True,
                  "enabled": bool(server.get("enabled", False)), "authStatus": server.get("auth_status", "unknown")}
        if expected_endpoint is not None:
            transport = server.get("transport") or {}
            status["endpointMatches"] = (isinstance(transport, dict)
                and transport.get("type") == "streamable_http" and transport.get("url") == expected_endpoint)
        return status
    except (OSError, ValueError, subprocess.TimeoutExpired):
        # Never echo subprocess stderr, config, headers or credential fields.
        return {"available": False}


def safe_host(value: dict) -> dict:
    if not isinstance(value, dict):
        return {"available": False, "configured": False, "enabled": False, "authStatus": "unknown"}
    status = value.get("authStatus", "unknown")
    if status not in {"oauth", "o_auth", "not_logged_in", "unsupported", "bearer_token", "unknown"}:
        status = "unknown"
    host = {"available": value.get("available") is True,
            "configured": value.get("configured") is True,
            "enabled": value.get("enabled") is True, "authStatus": status}
    if isinstance(value.get("endpointMatches"), bool):
        host["endpointMatches"] = value["endpointMatches"]
    return host


def headers(response: ProbeResponse) -> dict:
    return {str(key).lower(): str(value) for key, value in response.headers.items()}


def portal(response: ProbeResponse, base: str) -> tuple[bool, str | None]:
    """Recognize explicit captive/ePortal evidence without visiting that URL."""
    if response.status == 511:
        return True, None
    text = response.body[:MAX_BYTES].decode("utf-8", errors="replace")
    candidates = [headers(response).get("location", "")]
    candidates += re.findall(r"https?://[^\s\"'<>]+", text)
    for candidate in candidates:
        if not candidate:
            continue
        try:
            parsed = urlsplit(urljoin(base, html.unescape(candidate)))
            if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
                continue
            explicit = re.search(r"/(?:eportal|captive[-_]?portal)(?:/|$)", parsed.path, re.I)
            if explicit and origin(urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))) != origin(base):
                # A portal query can contain device IDs and SSO tickets.
                return True, urlunsplit((parsed.scheme, parsed.netloc, parsed.path[:512], "", ""))
        except ValueError:
            continue
    explicit_text = re.search(r"上网认证|网络认证|captive\s+portal", text, re.I)
    is_html = "html" in headers(response).get("content-type", "").lower() or "<html" in text.lower()
    return bool(explicit_text and is_html), None


def error_kind(error: Exception) -> str:
    reason = error.reason if isinstance(error, URLError) else error
    if isinstance(reason, ssl.SSLError):
        return "tls_error"
    if isinstance(reason, socket.gaierror):
        return "dns_error"
    if isinstance(reason, (TimeoutError, socket.timeout)):
        return "timeout"
    return "network_error"


MESSAGES = {
    "configuration_error": ("插件连接地址未正确配置。", "contact_admin", "请让插件维护者检查安装包的 MCP 地址，不能直接使用作者模板。"),
    "network_auth_required": ("当前网络返回了上网认证页面，灼见连接尚未建立。", "network_auth", "先完成当前网络的正常上网认证，再重新检查灼见连接；若仍受限，将诊断结果交给网管。"),
    "tls_error": ("灼见连接未通过 HTTPS 证书校验。", "contact_it", "请网管核查证书或 HTTPS 拦截；恢复正常证书连接后重试。"),
    "dns_error": ("当前网络无法解析灼见服务地址。", "retry_connection", "请检查当前网络的域名解析，恢复后重新检查连接。"),
    "timeout": ("连接灼见服务超时，尚未进入企业授权。", "retry_connection", "请稍后重试；持续超时请交由网管或平台维护者排查。"),
    "network_error": ("连接灼见服务失败，尚未进入企业授权。", "retry_connection", "请检查网络访问限制；连接恢复后重新检查，不要据此认定账号未登录。"),
    "service_error": ("灼见连接服务返回异常。", "contact_platform", "请平台维护者检查服务；恢复后重试，不要反复重新授权。"),
    "metadata_invalid": ("灼见授权发现信息未通过校验。", "contact_platform", "请平台维护者检查 MCP/OAuth 配置；当前不能生成有效授权链接。"),
    "unexpected_response": ("连接地址返回了非预期内容，尚未确认是灼见业务服务。", "contact_it", "请核查网络跳转和服务地址；不能把网页或 HTTP 200 当作连接成功。"),
    "authorization_required": ("连接和授权发现检查通过，需要完成灼见企业授权。", "login", "直接发起宿主原生登录，由本人在灼见官方页面核对企业、身份和授权范围。"),
    "connection_verified": ("连接和授权发现检查通过，尚需核验真实企业身份和业务能力。", "verify_identity", "调用当前获权 get_identity 和能力发现工具；工具未加载时刷新连接或在新聊天中核验。"),
    "host_disabled": ("网络检查通过，但宿主中的灼见企业连接被停用。", "enable_connection", "在宿主插件管理中启用当前连接，然后核验身份和可用能力。"),
    "host_configuration_mismatch": ("安装包与宿主中的灼见连接地址不一致。", "check_host_configuration", "先核对当前插件来源和宿主连接配置，地址一致后重检；当前不能对同名旧连接发起登录。"),
    "host_not_configured": ("网络检查通过，但本机 CLI 未找到灼见企业连接。", "connect_host", "核对正在使用的宿主及插件连接；不能把另一宿主的 CLI 状态当作当前身份。"),
    "host_unavailable": ("网络检查通过，本机无法读取宿主连接状态。", "connect_host", "使用当前宿主提供的连接入口或实际企业工具核验；不能据此认定尚未授权。"),
}


def result(status: str, host: dict, evidence: list[str], *, portal_url: str | None = None) -> dict:
    summary, action, message = MESSAGES[status]
    next_action = {"type": action, "message": message}
    if portal_url:
        next_action["url"] = portal_url
    if action == "login":
        next_action["command"] = ["codex", "mcp", "login", SERVER,
                                  "--scopes", "business:read,files:read"]
    return {"schemaVersion": 1, "status": status, "summary": summary,
            "nextAction": next_action, "evidence": evidence, "host": host,
            "businessVerified": False}


def json_document(response: ProbeResponse) -> dict:
    if response.status != 200 or len(response.body) > MAX_BYTES:
        raise ValueError("invalid_metadata")
    data = json.loads(response.body)
    if not isinstance(data, dict):
        raise ValueError("invalid_metadata")
    return data


def diagnose(endpoint: str, *, requester=None, host_checker=None, timeout: float = 6,
             http_probe: bool = True) -> dict:
    requester = requester or fetch_public
    evidence = []
    try:
        public_url(endpoint, endpoint=True)
    except (ValueError, TypeError):
        return result("configuration_error", safe_host({}), ["endpoint_invalid"])
    try:
        host = safe_host(host_checker() if host_checker else native_host_status(endpoint))
    except Exception:
        host = safe_host({})

    def finish(status, portal_url=None):
        return result(status, host, evidence.copy(), portal_url=portal_url)

    def probe_network_portal():
        if not http_probe:
            return None
        parsed = urlsplit(endpoint)
        # Plain HTTP is only an anonymous captive-network diagnostic. It is
        # never used for OAuth metadata, credentials or enterprise operations.
        probe_url = urlunsplit(("http", parsed.hostname, "/", "", ""))
        try:
            response = requester(probe_url, timeout)
            found, address = portal(response, probe_url)
            if found:
                evidence.append("http_network_portal_detected")
                return finish("network_auth_required", address)
        except (OSError, URLError, HTTPException, ValueError):
            pass
        return None

    try:
        response = requester(endpoint, timeout)
    except (OSError, URLError, HTTPException) as error:
        status = error_kind(error)
        evidence.append(status)
        return probe_network_portal() or finish(status)

    evidence.append(f"mcp_http_{response.status}")
    found, address = portal(response, endpoint)
    if found:
        return finish("network_auth_required", address)
    if response.status >= 500:
        return finish("service_error")
    if response.status != 401:
        # OAuth-bearing tools may be missing even while an HTML login page
        # responds with 200. That is not proof of a valid MCP connection.
        return probe_network_portal() or finish("unexpected_response")

    challenge = headers(response).get("www-authenticate", "")
    match = re.search(r'(?:^|[,\s])resource_metadata\s*=\s*"([^"\r\n]+)"', challenge, re.I)
    if not re.search(r"\bBearer\b", challenge, re.I) or not match:
        evidence.append("resource_metadata_challenge_missing")
        return finish("metadata_invalid")
    try:
        metadata_url = public_url(match.group(1))
        if origin(metadata_url) != origin(endpoint):
            raise ValueError("cross_origin_resource_metadata")
    except ValueError:
        evidence.append("resource_metadata_url_rejected")
        return finish("metadata_invalid")

    def metadata_fetch(url):
        try:
            metadata_response = requester(url, timeout)
        except (OSError, URLError, HTTPException) as error:
            evidence.append(error_kind(error))
            return None, probe_network_portal() or finish(error_kind(error))
        evidence.append(f"metadata_http_{metadata_response.status}")
        found, address = portal(metadata_response, url)
        if found:
            return None, finish("network_auth_required", address)
        if metadata_response.status >= 500:
            return None, finish("service_error")
        return metadata_response, None

    response, failure = metadata_fetch(metadata_url)
    if failure:
        return failure
    try:
        resource = json_document(response)
        if resource.get("resource") != endpoint:
            raise ValueError("resource_mismatch")
        issuers = resource.get("authorization_servers")
        if not isinstance(issuers, list) or not issuers:
            raise ValueError("issuer_missing")
        # Check the advertised authority. Never guess a login link or register
        # an OAuth client as part of a read-only preflight.
        issuer = public_url(issuers[0]).rstrip("/")
        parsed = urlsplit(issuer)
        authority = urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))
        authorization_metadata = authority + "/.well-known/oauth-authorization-server" + parsed.path.rstrip("/")
    except (ValueError, TypeError):
        evidence.append("resource_metadata_invalid")
        return finish("metadata_invalid")

    response, failure = metadata_fetch(authorization_metadata)
    if failure:
        return failure
    if response.status == 404:
        response, failure = metadata_fetch(issuer + "/.well-known/openid-configuration")
        if failure:
            return failure
    try:
        authorization = json_document(response)
        if authorization.get("issuer", "").rstrip("/") != issuer:
            raise ValueError("issuer_mismatch")
        public_url(authorization.get("authorization_endpoint"))
        public_url(authorization.get("token_endpoint"))
        methods = authorization.get("code_challenge_methods_supported")
        if not isinstance(methods, list) or not all(isinstance(method, str) for method in methods) or "S256" not in methods:
            raise ValueError("pkce_missing")
    except (ValueError, TypeError, AttributeError):
        evidence.append("authorization_metadata_invalid")
        return finish("metadata_invalid")

    evidence.append("oauth_discovery_verified")
    if not host["available"]:
        return finish("host_unavailable")
    if not host["configured"]:
        return finish("host_not_configured")
    if not host["enabled"]:
        return finish("host_disabled")
    if host.get("endpointMatches") is False:
        return finish("host_configuration_mismatch")
    if host["authStatus"] == "not_logged_in":
        return finish("authorization_required")
    return finish("connection_verified")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="只读检查灼见连接；不登录、不读取凭据、不修改宿主或网络配置。")
    parser.add_argument("--config", type=Path, default=Path(__file__).resolve().parents[3] / "mcp.json")
    parser.add_argument("--json", action="store_true", help="输出脱敏 JSON")
    parser.add_argument("--skip-host", action="store_true", help="仅检查网络，适用于非 Codex CLI 宿主")
    parser.add_argument("--timeout", type=float, default=6, help="每个匿名请求超时秒数，1–15")
    args = parser.parse_args(argv)
    if not 1 <= args.timeout <= 15:
        parser.error("timeout must be between 1 and 15 seconds")
    try:
        config = json.loads(args.config.read_text(encoding="utf-8-sig"))
        endpoint = config["mcpServers"][SERVER]["url"]
    except (OSError, ValueError, KeyError, TypeError):
        report = result("configuration_error", safe_host({}), ["package_configuration_unreadable"])
    else:
        report = diagnose(endpoint, timeout=args.timeout,
                          host_checker=(lambda: {"available": False}) if args.skip_host else None)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(report["summary"])
        print(report["nextAction"]["message"])
        if "url" in report["nextAction"]:
            print(report["nextAction"]["url"])
    return 0 if report["status"] in {"connection_verified", "authorization_required", "host_unavailable"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
