"""Small local report server for the judge walkthrough."""

from __future__ import annotations

from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class QuietHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path in {"", "/"}:
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Location", "/report.html")
            self.end_headers()
            return
        super().do_GET()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        print(f"[replay] {format % args}")


def serve_report(output_dir: str | Path, host: str, port: int) -> None:
    directory = Path(output_dir).resolve()
    handler = partial(QuietHandler, directory=str(directory))
    server = ThreadingHTTPServer((host, port), handler)
    print(f"OmarAGI Reliability BYOK Replay: http://{host}:{port}/report.html")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
