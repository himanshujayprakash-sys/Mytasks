"""Minimal MCP streamable-HTTP client, so large read-only results can be processed locally."""
import json
import urllib.request

SERVERS = {s['name']: s['url'] for s in json.loads(__import__('os').environ['MCP_SERVERS_JSON'])}


class Client:
    def __init__(self, name):
        self.url = SERVERS[name]
        self.sid = None
        self.n = 0
        self._init()

    def _post(self, payload):
        data = json.dumps(payload).encode()
        hdr = {'Content-Type': 'application/json',
               'Accept': 'application/json, text/event-stream'}
        if self.sid:
            hdr['Mcp-Session-Id'] = self.sid
        req = urllib.request.Request(self.url, data=data, headers=hdr, method='POST')
        with urllib.request.urlopen(req, timeout=120) as r:
            sid = r.headers.get('Mcp-Session-Id')
            if sid:
                self.sid = sid
            body = r.read().decode()
        if 'text/event-stream' in (r.headers.get('Content-Type') or ''):
            out = None
            for line in body.splitlines():
                if line.startswith('data:'):
                    out = json.loads(line[5:].strip())
            return out
        return json.loads(body) if body.strip() else None

    def _init(self):
        self.n += 1
        self._post({'jsonrpc': '2.0', 'id': self.n, 'method': 'initialize',
                    'params': {'protocolVersion': '2025-03-26',
                               'capabilities': {},
                               'clientInfo': {'name': 'local', 'version': '1'}}})
        hdr = {'Content-Type': 'application/json',
               'Accept': 'application/json, text/event-stream',
               'Mcp-Session-Id': self.sid or ''}
        req = urllib.request.Request(
            self.url, data=json.dumps({'jsonrpc': '2.0', 'method': 'notifications/initialized'}).encode(),
            headers=hdr, method='POST')
        try:
            urllib.request.urlopen(req, timeout=60).read()
        except Exception:
            pass

    def call(self, tool, args):
        self.n += 1
        r = self._post({'jsonrpc': '2.0', 'id': self.n, 'method': 'tools/call',
                        'params': {'name': tool, 'arguments': args}})
        if r is None:
            raise RuntimeError('no response')
        if 'error' in r:
            raise RuntimeError(r['error'])
        content = r['result'].get('content') or []
        texts = [c['text'] for c in content if c.get('type') == 'text']
        for t in reversed(texts):
            try:
                return json.loads(t)
            except Exception:
                continue
        return texts


if __name__ == '__main__':
    import sys
    c = Client(sys.argv[1])
    print(json.dumps(c.call(sys.argv[2], json.loads(sys.argv[3])))[:2000])
