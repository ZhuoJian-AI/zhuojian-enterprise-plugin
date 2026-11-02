"""Pair a native OAuth request. Never handle browser callbacks or OAuth tokens.

Read the short-lived invitation JSON from stdin. The native CLI owns PKCE,
loopback reception and its credential store. Python uses the standard library.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def configured_origin():
    package = Path(__file__).resolve().parents[3]
    config = json.loads((package / 'mcp.json').read_text(encoding='utf-8'))
    server = config['mcpServers']['zhuojian-enterprise']
    value = urlsplit(server['url'])
    if value.scheme != 'https' or value.username or value.password or value.query or value.fragment:
        raise ValueError('The installed plugin must have a verified HTTPS endpoint')
    if value.path != '/api/v1/enterprise-mcp' or value.hostname.endswith('.invalid'):
        raise ValueError('Install the released enterprise plugin before pairing')
    return f'{value.scheme}://{value.netloc}'


def checked_invitation(value, origin):
    if not isinstance(value, dict) or set(value) != {'origin', 'ticket'} or value['origin'] != origin:
        raise ValueError('Invitation must belong to the installed enterprise service')
    if not isinstance(value['ticket'], str) or not re.fullmatch(r'[A-Za-z0-9_-]{43}', value['ticket']):
        raise ValueError('Invalid or incomplete invitation; copy it again from the signed-in platform')
    return value['ticket']


def request_id_url(raw, origin):
    """Follow only the native authorization request's one first-party redirect."""
    url = urlsplit(raw)
    query = parse_qs(url.query, keep_blank_values=True)
    if (f'{url.scheme}://{url.netloc}' == origin and not url.username and not url.password and not url.fragment
            and url.path == '/enterprise-plugin/authorize' and set(query) == {'request_id'}
            and len(query['request_id']) == 1
            and re.fullmatch(r'[a-f0-9]{8}-[a-f0-9-]{27,28}', query['request_id'][0])):
        return raw
    if (f'{url.scheme}://{url.netloc}' != origin or url.username or url.password or url.fragment
            or url.path != '/api/v1/enterprise-mcp/oauth/authorize'
            or any(len(values) != 1 for values in query.values())
            or query.get('code_challenge_method') != ['S256']
            or query.get('resource') != [origin + '/api/v1/enterprise-mcp']):
        raise ValueError('Expected the current native client authorization request; never paste a callback URL')
    try:
        with build_opener(NoRedirect).open(Request(raw, headers={'Accept': 'text/html'}), timeout=20):
            raise ValueError('Native authorization did not create a consent request')
    except HTTPError as error:
        if error.code != 302:
            raise ValueError(f'Native authorization request rejected ({error.code})') from None
        location = error.headers.get('Location', '')
    destination = urlsplit(location)
    if (f'{destination.scheme}://{destination.netloc}' != origin
            or destination.path != '/enterprise-plugin/authorize'
            or set(parse_qs(destination.query)) != {'request_id'} or destination.fragment):
        raise ValueError('Unexpected authorization redirect')
    return location


def pair(ticket, native_url, origin):
    body = json.dumps({'ticket': ticket, 'authorization_url': request_id_url(native_url, origin)}).encode()
    request = Request(origin + '/api/v1/enterprise-mcp/pairing/requests', data=body,
                      headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
    try:
        with build_opener(NoRedirect).open(request, timeout=20) as response:
            result = json.loads(response.read(8192))
    except HTTPError as error:
        raise ValueError(f'Pairing request rejected ({error.code}); copy a new invitation if expired') from None
    code = result.get('user_code', '')
    if not re.fullmatch(r'[23456789A-HJ-NP-Z]{5}-[23456789A-HJ-NP-Z]{5}', code):
        raise ValueError('Server did not return a valid pairing code')
    return {'status': 'awaiting_user_confirmation', 'user_code': code, 'expires_at': result.get('expires_at'),
            'client_name': result.get('client_name'), 'businessVerified': False}


def native_command(host, origin, server='zhuojian-enterprise'):
    executable = shutil.which(host)
    if not executable:
        raise ValueError(f'{host} native CLI is unavailable; use its supported connector interface')
    help_result = subprocess.run([executable, 'mcp', 'login', '--help'], capture_output=True, text=True,
                                 encoding='utf-8', errors='replace', timeout=15)
    if help_result.returncode or '--no-browser' not in help_result.stdout:
        raise ValueError('This native client lacks supported non-opening OAuth; use its connection interface')
    get_args = [executable, 'mcp', 'get', server] + (['--json'] if host == 'codex' else [])
    existing = subprocess.run(get_args, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=20)
    endpoint = origin + '/api/v1/enterprise-mcp'
    if existing.returncode:
        # A failed read/health check is not evidence of an absent connector.
        # These are the verified native "not found" responses, not arbitrary
        # errors that would justify overwriting an existing configuration.
        message = (existing.stdout + existing.stderr).lower()
        if not re.search(r'no mcp server (?:named|found with name)', message):
            raise ValueError('Could not verify the existing native connector; no configuration was changed')
        add = ([executable, 'mcp', 'add', server, '--url', endpoint] if host == 'codex' else
               [executable, 'mcp', 'add', '--transport', 'http', '--scope', 'user', server, endpoint])
        added = subprocess.run(add, capture_output=True, timeout=20)
        if added.returncode:
            raise ValueError('Native connector installation failed; no existing configuration was replaced')
        existing = subprocess.run(get_args, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=20)
    if host == 'codex':
        try:
            transport = json.loads(existing.stdout)['transport']
            actual_url = transport['url'] if transport['type'] == 'streamable_http' else None
        except (ValueError, KeyError, TypeError):
            actual_url = None
    else:
        matches = re.findall(r'^\s*URL:\s*(\S+)\s*$', existing.stdout, re.MULTILINE | re.IGNORECASE)
        actual_url = matches[0] if len(matches) == 1 else None
    if existing.returncode or actual_url != endpoint:
        raise ValueError('Existing native connector points elsewhere; do not overwrite it')
    command = [executable, 'mcp', 'login', server, '--no-browser']
    if host == 'codex':
        command += ['--scopes', 'business:read,files:read,admin:read']
    return command


def run_native(command, ticket, origin, *, timeout=300):
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, encoding='utf-8', errors='replace', bufsize=1)
    lines = queue.Queue()

    def read():
        for line in process.stdout:
            lines.put(line)
        lines.put(None)

    threading.Thread(target=read, daemon=True).start()
    deadline = time.monotonic() + timeout
    announced = False
    try:
        while time.monotonic() < deadline:
            try:
                line = lines.get(timeout=min(1, max(.01, deadline - time.monotonic())))
            except queue.Empty:
                continue
            if line is None:
                code = process.wait(timeout=10)
                if code != 0 or not announced:
                    raise ValueError('Native OAuth did not finish; no business connection has been verified')
                print(json.dumps({'status': 'native_authenticated', 'businessVerified': False,
                                  'next': 'Load native MCP tools, get_identity, discover_capabilities and read actual authorized data'}), flush=True)
                return
            # Suppress native logs, especially any fallback callback instructions.
            # We never supply stdin or parse a callback's code/state/token.
            if not announced:
                urls = re.findall(r'https://[^\s\x1b<>"\']+', line)
                for url in urls:
                    if url.startswith(origin + '/api/v1/enterprise-mcp/oauth/authorize?'):
                        result = pair(ticket, url, origin)
                        print(json.dumps(result, ensure_ascii=False), flush=True)
                        announced = True
                        break
        raise ValueError('Native login timed out; copy a new invitation and start again')
    finally:
        if process.poll() is None:
            process.terminate()  # only the login process created by this helper
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
        if process.stdin:
            process.stdin.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', choices=['codex', 'claude'])
    parser.add_argument('--authorization-url', help='Current native authorization request, never a callback')
    args = parser.parse_args()
    if bool(args.host) == bool(args.authorization_url):
        parser.error('Choose --host or a native --authorization-url')
    try:
        origin = configured_origin()
        ticket = checked_invitation(json.loads(sys.stdin.readline(4096)), origin)
        if args.host == 'claude':
            command = native_command(args.host, origin)
            # Claude 2.1.227 refuses redirected stdin. The host must launch its
            # own PTY and retain that session, then bind its authorization URL
            # using --authorization-url. Never emulate a callback paste.
            print(json.dumps({'status': 'native_terminal_required', 'command': command,
                              'next': 'Run in the host interactive terminal, keep it alive, then use --authorization-url with the native request; invitation JSON stays on stdin',
                              'businessVerified': False}), flush=True)
        elif args.host:
            run_native(native_command(args.host, origin), ticket, origin)
        else:
            print(json.dumps(pair(ticket, args.authorization_url, origin), ensure_ascii=False), flush=True)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        # All messages above are static; never print HTTP/native response bodies.
        print(json.dumps({'status': 'not_connected', 'error': str(error), 'businessVerified': False}), flush=True)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
