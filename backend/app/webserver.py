"""Zero-dependency web server for the playable demo.

    python -m app.webserver        # then open http://127.0.0.1:8000

Uses only the standard library (http.server) so the whole game is playable in a browser
with NO installs and NO API keys — it wraps the same run_turn() the FastAPI app uses.
FastAPI (app/api.py) remains the production surface; this is the instant-play demo.
"""
from __future__ import annotations

import json
import mimetypes
import posixpath
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .config import settings
from .engine import run_turn
from .models import TurnRequest
from .content.tales import SEASON_ORDER, TALES
from .voice import sarvam

_WEB = Path(__file__).parent / "web"
_ASSETS = Path(__file__).resolve().parents[2] / "assets"   # C:\Katha\assets (drop art here)


def _render_to_dict(r) -> dict:
    d = asdict(r)  # SceneRender is a dataclass; choices are dataclasses too
    return d


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code: int = 200) -> None:
        self._send(code, json.dumps(obj).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/", "/index.html"):
            html = (_WEB / "index.html").read_bytes()
            self._send(200, html, "text/html; charset=utf-8")
        elif self.path == "/season":
            self._json({
                "order": [{"id": t, "title": TALES[t]["title"], "kind": TALES[t].get("kind", "tale")}
                          for t in SEASON_ORDER],
                "tts_enabled": settings.tts_enabled,   # Sarvam available? else browser speech
            })
        elif self.path.startswith("/assets/"):
            self._serve_asset(self.path[len("/assets/"):])
        else:
            self._json({"error": "not found"}, 404)

    def _serve_asset(self, rel: str) -> None:
        # Serve a generated art file from C:\Katha\assets, with a path-traversal guard.
        rel = posixpath.normpath(rel.split("?")[0]).lstrip("/")
        target = (_ASSETS / rel).resolve()
        if not str(target).startswith(str(_ASSETS.resolve())) or not target.is_file():
            self._send(404, b"not found", "text/plain")
            return
        ctype = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
        self._send(200, target.read_bytes(), ctype)

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            self._json({"error": "bad json"}, 400)
            return

        if self.path == "/turn":
            render = run_turn(TurnRequest(
                session_id=body.get("session_id", "web"),
                player_input=body.get("player_input", ""),
                language=body.get("language", "en"),
                scene_id=body.get("scene_id", ""),
                choice_id=body.get("choice_id"),
                player_id=body.get("player_id", ""),
            ))
            self._json(_render_to_dict(render))
        elif self.path == "/tts":
            audio = sarvam.synthesize(body.get("text", ""), body.get("voice_profile", ""),
                                      body.get("language", ""))
            self._json({"audio": audio, "format": "wav"})
        else:
            self._json({"error": "not found"}, 404)

    def log_message(self, *args) -> None:  # quieter console
        pass


def main(host: str | None = None, port: int | None = None) -> None:
    import logging
    import os
    host = host or os.environ.get("HOST", "127.0.0.1")
    port = port or int(os.environ.get("PORT", "8000"))
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Katha is playable at  http://{host}:{port}   (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()


if __name__ == "__main__":
    main()
