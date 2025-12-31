from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from contextlib import contextmanager
from typing import Generator
import pprint

class CompetitiveCompanionHandler(BaseHTTPRequestHandler):
    callback = None

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    @staticmethod
    def set_callback(callback):
        callback = callback

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        payload = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(payload)

        if CompetitiveCompanionHandler.callback:
            CompetitiveCompanionHandler.callback(data)

@contextmanager
def run_server(
        serverclass = HTTPServer,
        handler_class = CompetitiveCompanionHandler,
        port = 10046,
        callback = None,
) -> Generator[HTTPServer, None, None]:
    server_address = ("0.0.0.0", port)
    httpd = serverclass(server_address, handler_class)

    handler = handler_class
    handler.callback = callback

    print(f'Starting server on port {port}...')
    try:
        yield httpd
    finally:
        httpd.server_close()
        print(f'Stopping server on port {port}.')


def listen_once():
    payload = None

    def set_payload(data) -> None:
        nonlocal payload
        payload = data

    with run_server(callback = set_payload) as server:
        server.timeout = None
        server.handle_request()

    pprint.pprint(payload)
    if not isinstance(payload, dict):
        return

    for i, test in enumerate(payload["tests"]):
        test_id = i + 1
        with open(f"inp{test_id}", mode="w", encoding="utf-8") as f:
            f.write(test["input"])
        with open(f"out{test_id}", mode="w", encoding="utf-8") as f:
            f.write(test["output"])

