#!/usr/bin/env python3
"""Tiny HTTPS CONNECT proxy that only tunnels to an allowlist of hosts.

Run it on localhost, then point the sandboxed grader at it (GRADER_PROXY_PORT).
The OS sandbox blocks all other outbound traffic, so a grader that tries to reach
anything else fails. Check the hosts your Codex version actually needs
(typically the ChatGPT and OpenAI auth/API hosts) and set ALLOW below.
Usage: python allowlist_proxy.py PORT
"""
import select, socket, socketserver, sys

ALLOW = {"chatgpt.com", "auth.openai.com"}  # verify for your Codex version


class H(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(65536).decode("latin1", "replace")
        first = data.split("\r\n", 1)[0].split()
        if len(first) < 2 or first[0] != "CONNECT":
            self.request.sendall(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n"); return
        host, _, port = first[1].partition(":")
        if host not in ALLOW:
            self.request.sendall(b"HTTP/1.1 403 Forbidden\r\n\r\n"); return
        up = socket.create_connection((host, int(port or 443)), timeout=20)
        self.request.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
        socks = [self.request, up]
        while True:
            r, _, _ = select.select(socks, [], [], 60)
            if not r: break
            for s in r:
                chunk = s.recv(65536)
                if not chunk: return
                (up if s is self.request else self.request).sendall(chunk)


class S(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    S(("127.0.0.1", int(sys.argv[1])), H).serve_forever()
