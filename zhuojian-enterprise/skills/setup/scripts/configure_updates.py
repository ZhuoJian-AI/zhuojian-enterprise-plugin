"""Check or configure native Codex updates from the package's first-party origin."""

from __future__ import annotations

import argparse
from http.client import HTTPException
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
try:
    import tomllib
except ImportError:  # A host without this runtime must use its native UI.
    tomllib = None
from urllib.error import URLError
from urllib.parse import urlsplit, urlunsplit

from check_connection import MAX_BYTES, SERVER, fetch_public, public_url


MARKETPLACE = "zhuojian-enterprise-pilot"
PLUGIN_ID = f"{SERVER}@{MARKETPLACE}"
UPDATES_PATH = "/enterprise-plugin/updates"
RELEASE = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")

MESSAGES = {
    "configuration_error": ("安装包的更新配置无效。", "contact_platform", "请维护者核对安装包；当前来源没有变更。"),
    "endpoint_unavailable": ("国内更新入口尚未就绪或当前无法连接。", "retry_later", "保留当前来源，稍后重试或交由平台维护者处理；不需要重新登录。"),
    "metadata_invalid": ("国内更新信息未通过校验。", "contact_platform", "保留当前来源，请平台维护者核对发布信息。"),
    "downgrade_rejected": ("国内发布版本低于当前版本，已停止更新。", "contact_platform", "保留当前安装和来源，请维护者核对版本。"),
    "host_unavailable": ("当前无法核实 Codex 的插件管理状态。", "check_host", "使用支持插件管理的 Codex；没有修改当前来源或登录。"),
    "host_unsupported": ("当前宿主缺少原生更新所需的 Git 能力。", "use_supported_host", "没有修改来源；由维护者提供支持原生插件更新的宿主，不要求员工手工安装 Git。"),
    "host_configuration_mismatch": ("宿主实际使用的来源与当前用户登记不一致。", "check_host", "保留来源和安装，请维护者核对宿主的有效配置；不能据此更新其他来源。"),
    "migration_required": ("当前来源尚未接入国内自动更新。", "apply_when_requested", "用户已要求启用自动更新或安装升级后，使用 --apply 接入国内发行源。"),
    "installation_required": ("国内发行源已核实，当前插件尚未安装。", "apply_when_requested", "用户已要求安装或自动更新后，使用 --apply 完成原生安装。"),
    "update_available": ("国内发行源已核实，实际安装版本仍需更新。", "apply_when_requested", "用户已要求安装升级后，使用 --apply 调用原生更新并核验版本。"),
    "ready": ("国内来源和实际安装版本已验证，原生自动更新已接入。", "use_native_updates", "Codex 启动时由原生机制检查更新；本聊天不承诺热刷新，必要时在新聊天核验工具。"),
    "update_failed": ("原生更新未完成，尚未确认自动更新接入。", "retry_later", "保留现有登录，检查国内更新入口后重试；不要手动覆盖缓存。"),
    "installation_failed": ("国内发行源已接入，但插件安装尚未完成。", "verify_installation", "保留现有缓存和 OAuth，通过原生插件管理继续核查安装；当前不能报告自动更新已启用。"),
    "update_failed_restored": ("国内发行源接入失败，原来源已恢复。", "retry_later", "保留当前安装和登录，待国内入口恢复后重试。"),
    "rollback_required": ("国内发行源接入失败，原来源未能自动恢复。", "restore_source", "保留现有插件缓存和 OAuth；请维护者处理来源恢复，不自动访问境外旧源。"),
    "verification_required": ("原生命令已完成，来源或实际安装版本尚未验证。", "verify_installation", "重新检查安装状态；当前不能报告自动更新已启用，本聊天不承诺热刷新。"),
}


def report(status: str, version: str | None = None, *, trusted: bool = False) -> dict:
    summary, action, message = MESSAGES[status]
    return {"status": status, "summary": summary,
            "nextAction": {"type": action, "message": message},
            "expectedVersion": version, "sourceTrusted": trusted,
            "automaticUpdates": {"enabled": status == "ready"}}


def release_version(value: str) -> tuple[int, int, int]:
    if not isinstance(value, str) or not RELEASE.fullmatch(value):
        raise ValueError("invalid_release_version")
    return tuple(int(part) for part in value.split("."))


def package_settings(config_path: Path) -> tuple[str, str, str]:
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    endpoint = public_url(config["mcpServers"][SERVER]["url"], endpoint=True)
    parsed = urlsplit(endpoint)
    if "@" in parsed.netloc:
        raise ValueError("invalid_origin")
    base = urlunsplit((parsed.scheme, parsed.netloc, UPDATES_PATH, "", ""))
    manifest = config_path.parent / "plugin.json"
    if not manifest.exists():
        manifest = config_path.parent / "connector-meta.json"
    version = json.loads(manifest.read_text(encoding="utf-8-sig"))["version"]
    release_version(version)
    return base, base + "/marketplace.git", version


def read_marketplace(home: Path) -> dict | None:
    """Read only the target table; never return the remaining configuration."""
    if tomllib is None:
        raise ValueError("host_configuration_reader_unavailable")
    config = home / "config.toml"
    if not config.exists():
        return None
    with config.open("rb") as stream:
        value = tomllib.load(stream).get("marketplaces", {}).get(MARKETPLACE)
    if value is None:
        return None
    if not isinstance(value, dict) or value.get("source_type") not in {"local", "git"}:
        raise ValueError("invalid_marketplace")
    source = value.get("source")
    ref = value.get("ref")
    if not isinstance(source, str) or not source or (ref is not None and not isinstance(ref, str)):
        raise ValueError("invalid_marketplace")
    return {"source_type": value["source_type"], "source": source, "ref": ref}


def trusted_source(source: dict | None, url: str) -> bool:
    return bool(source and source.get("source_type") == "git"
                and source.get("source") == url and source.get("ref") == "main")


def effective_source(value) -> dict | None:
    if not isinstance(value, dict) or value.get("sourceType") not in {"local", "git"}:
        return None
    if not isinstance(value.get("source"), str):
        return None
    return {"source_type": value["sourceType"], "source": value["source"], "ref": value.get("ref")}


def source_matches(registered: dict | None, effective: dict | None) -> bool:
    return bool(registered and effective
                and all(registered.get(key) == effective.get(key) for key in ("source_type", "source"))
                and (effective.get("ref") is None or effective["ref"] == registered.get("ref")))


def native_run(command: list[str], *, direct_origin: str):
    # The registered endpoint is domestic. Proxy and TLS settings stay local
    # to this child process; never change the user's global Git/OS settings.
    environment = os.environ.copy()
    hostname = urlsplit(direct_origin).hostname
    bypass = ",".join(filter(None, [environment.get("NO_PROXY", environment.get("no_proxy", "")), hostname]))
    environment["NO_PROXY"] = bypass
    environment["no_proxy"] = bypass
    environment.pop("GIT_SSL_NO_VERIFY", None)
    count = int(environment.get("GIT_CONFIG_COUNT", "0"))
    for key, value in ((f"http.{direct_origin}.proxy", ""), ("http.followRedirects", "false"), ("http.sslVerify", "true")):
        environment[f"GIT_CONFIG_KEY_{count}"] = key
        environment[f"GIT_CONFIG_VALUE_{count}"] = value
        count += 1
    environment["GIT_CONFIG_COUNT"] = str(count)
    environment["GIT_TERMINAL_PROMPT"] = "0"
    environment["GCM_INTERACTIVE"] = "Never"
    environment[f"GIT_CONFIG_KEY_{count}"] = "credential.helper"
    environment[f"GIT_CONFIG_VALUE_{count}"] = ""
    environment["GIT_CONFIG_COUNT"] = str(count + 1)
    return subprocess.run(command, capture_output=True, encoding="utf-8", errors="replace",
                          timeout=60, check=False, env=environment)


def installed_plugin(executable: str, runner) -> dict | None:
    completed = runner([executable, "plugin", "list", "--marketplace", MARKETPLACE, "--json"])
    if completed.returncode:
        raise ValueError("native_list_failed")
    value = json.loads(completed.stdout)
    if not isinstance(value, dict) or not isinstance(value.get("installed"), list):
        raise ValueError("native_list_invalid")
    matches = [item for item in value["installed"]
               if isinstance(item, dict) and item.get("pluginId") == PLUGIN_ID]
    if not matches:
        return None
    if len(matches) != 1 or matches[0].get("installed") is not True:
        raise ValueError("native_installation_invalid")
    item = matches[0]
    release_version(item.get("version"))
    return {"version": item["version"], "enabled": item.get("enabled") is True,
            "marketplaceSource": effective_source(item.get("marketplaceSource"))}


def available_source(executable: str, runner) -> dict | None:
    completed = runner([executable, "plugin", "list", "--marketplace", MARKETPLACE, "--available", "--json"])
    if completed.returncode:
        raise ValueError("native_available_failed")
    value = json.loads(completed.stdout)
    if not isinstance(value, dict) or not isinstance(value.get("available"), list):
        raise ValueError("native_available_invalid")
    matches = [item for item in value["available"] if isinstance(item, dict) and item.get("pluginId") == PLUGIN_ID]
    return effective_source(matches[0].get("marketplaceSource")) if len(matches) == 1 else None


def configure(config_path: Path, *, apply: bool = False, requester=None, runner=None,
              executable: str | None = None, codex_home: Path | None = None,
              config_reader=None, git_executable: str | None = None, timeout: float = 6) -> dict:
    requester = requester or fetch_public
    config_reader = config_reader or read_marketplace
    home = codex_home or Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    try:
        base, marketplace_url, current = package_settings(config_path)
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return report("configuration_error")
    parsed = urlsplit(base)
    direct_origin = urlunsplit((parsed.scheme, parsed.netloc, "", "", ""))
    runner = runner or (lambda command: native_run(command, direct_origin=direct_origin))
    try:
        response = requester(base + "/latest.json", timeout)
    except (OSError, URLError, HTTPException, ValueError):
        return report("endpoint_unavailable")
    if response.status != 200:
        return report("endpoint_unavailable")
    try:
        if len(response.body) > MAX_BYTES:
            raise ValueError("metadata_too_large")
        content_type = {str(key).lower(): str(value) for key, value in response.headers.items()}.get("content-type", "")
        if content_type.split(";", 1)[0].strip().lower() != "application/json":
            raise ValueError("invalid_content_type")
        latest = json.loads(response.body)
        if not isinstance(latest, dict) or type(latest.get("schemaVersion")) is not int or latest["schemaVersion"] != 1:
            raise ValueError("invalid_schema")
        version = latest["version"]
        release_version(version)
        commit = latest["gitCommit"]
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
            raise ValueError("invalid_git_commit")
        public_url(latest["marketplaceUrl"])
        if latest["marketplaceUrl"] != marketplace_url:
            raise ValueError("untrusted_marketplace")
    except (ValueError, KeyError, TypeError):
        return report("metadata_invalid")
    if release_version(version) < release_version(current):
        return report("downgrade_rejected", version)
    executable = executable or shutil.which("codex")
    if not executable:
        return report("host_unavailable", version)
    try:
        if runner([executable, "plugin", "--help"]).returncode:
            return report("host_unavailable", version)
        old_source = config_reader(home)
        installed = installed_plugin(executable, runner)
        effective = (installed["marketplaceSource"] if installed else
                     available_source(executable, runner) if old_source else None)
    except (OSError, ValueError, TypeError, AttributeError, subprocess.TimeoutExpired):
        return report("host_unavailable", version)
    if (old_source or effective) and not source_matches(old_source, effective):
        return report("host_configuration_mismatch", version)
    trusted = trusted_source(old_source, marketplace_url) and source_matches(old_source, effective)
    if installed and release_version(installed["version"]) > release_version(version):
        return report("downgrade_rejected", version, trusted=trusted)
    if not apply:
        if not trusted:
            return report("migration_required", version)
        if not installed:
            return report("installation_required", version, trusted=True)
        if installed["version"] != version or not installed["enabled"]:
            return report("update_available", version, trusted=True)
        return report("ready", version, trusted=True)

    def succeeds(arguments):
        try:
            return runner([executable, "plugin", *arguments]).returncode == 0
        except (OSError, ValueError, subprocess.TimeoutExpired):
            return False

    git_executable = git_executable or shutil.which("git")
    if not git_executable:
        return report("host_unsupported", version, trusted=trusted)
    try:
        remote = runner([git_executable, "ls-remote", "--exit-code", marketplace_url, "refs/heads/main"])
        if remote.returncode:
            return report("endpoint_unavailable", version, trusted=trusted)
        references = [line.split() for line in remote.stdout.splitlines() if line.strip()]
        if references != [[commit, "refs/heads/main"]]:
            return report("metadata_invalid", version, trusted=trusted)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return report("endpoint_unavailable", version, trusted=trusted)

    if trusted:
        if not succeeds(["marketplace", "upgrade", MARKETPLACE, "--json"]):
            return report("update_failed", version, trusted=True)
        if not installed and not succeeds(["add", PLUGIN_ID, "--json"]):
            return report("update_failed", version, trusted=True)
    else:
        if old_source and not succeeds(["marketplace", "remove", MARKETPLACE, "--json"]):
            return report("update_failed", version)
        if not succeeds(["marketplace", "add", marketplace_url, "--ref", "main", "--json"]):
            if not old_source:
                return report("update_failed", version)
            if old_source["source_type"] == "local" and not Path(old_source["source"]).is_absolute():
                return report("rollback_required", version)
            if old_source["source_type"] == "git":
                try:
                    old_url = urlsplit(public_url(old_source["source"]))
                    if "@" in old_url.netloc or urlunsplit((old_url.scheme, old_url.netloc, "", "", "")) != direct_origin:
                        raise ValueError("foreign_restore_forbidden")
                except (ValueError, TypeError):
                    return report("rollback_required", version)
            restore = ["marketplace", "add", old_source["source"]]
            if old_source["source_type"] == "git" and old_source.get("ref") is not None:
                restore += ["--ref", old_source["ref"]]
            restore.append("--json")
            restored = succeeds(restore)
            if restored:
                try:
                    restored = config_reader(home) == old_source
                except (OSError, ValueError, TypeError, AttributeError):
                    restored = False
            return report("update_failed_restored" if restored else "rollback_required", version)
        try:
            registered = config_reader(home)
            if not trusted_source(registered, marketplace_url) or not source_matches(registered, available_source(executable, runner)):
                return report("verification_required", version)
        except (OSError, ValueError, TypeError, AttributeError, subprocess.TimeoutExpired):
            return report("verification_required", version)
        if not succeeds(["add", PLUGIN_ID, "--json"]):
            return report("installation_failed", version)
    try:
        registered = config_reader(home)
        installed = installed_plugin(executable, runner)
        trusted = trusted_source(registered, marketplace_url) and bool(installed) and source_matches(registered, installed["marketplaceSource"])
    except (OSError, ValueError, TypeError, AttributeError, subprocess.TimeoutExpired):
        return report("verification_required", version)
    verified = trusted and installed and installed["version"] == version and installed["enabled"]
    return report("ready" if verified else "verification_required", version, trusted=trusted)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="检查国内更新；--apply 仅用于用户已要求安装升级或自动更新的任务。")
    parser.add_argument("--config", type=Path, default=Path(__file__).resolve().parents[3] / "mcp.json")
    parser.add_argument("--apply", action="store_true", help="调用原生 Codex 配置；不退出 OAuth，不覆盖缓存")
    parser.add_argument("--timeout", type=float, default=6)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if not 1 <= args.timeout <= 15:
        parser.error("timeout must be between 1 and 15 seconds")
    result = configure(args.config, apply=args.apply, timeout=args.timeout)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["summary"])
        print(result["nextAction"]["message"])
    return 0 if result["status"] == "ready" else 2


if __name__ == "__main__":
    raise SystemExit(main())
