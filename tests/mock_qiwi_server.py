from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


class MockHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length).decode("utf-8")) if length else {}

    def do_GET(self):
        path = urlparse(self.path).path
        if path.endswith("/payments"):
            self.send_json(200, {"data": [{"txnId": 1001, "date": "2026-01-01", "status": "SUCCESS", "type": "OUT", "sum": {"amount": 1, "currency": 643}, "commission": {"amount": 0, "currency": 643}, "total": {"amount": 1, "currency": 643}, "provider": {"id": 99}}]})
            return
        if path.endswith("/accounts"):
            self.send_json(200, {"accounts": [{"alias": "qw_wallet_rub", "currency": 643, "balance": {"amount": 100.5, "currency": 643}}]})
            return
        if "/transactions/" in path:
            txn_id = path.rsplit("/", 1)[-1]
            self.send_json(200, {"txnId": txn_id, "status": "SUCCESS", "type": "OUT", "sum": {"amount": 1, "currency": 643}, "errorCode": 0, "error": None})
            return
        self.send_json(404, {"error": "not found"})

    def do_POST(self):
        payload = self.read_json()
        self.send_json(200, {"id": payload.get("id"), "sum": payload["sum"], "fields": payload["fields"], "terms": "99", "transaction": {"id": "123456789", "state": {"code": "Accepted"}}})


def run_mock_server(host="127.0.0.1", port=0):
    server = ThreadingHTTPServer((host, port), MockHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, f"http://{host}:{server.server_port}"
