"""FastAPI surface — the production HTTP API (docs/01 sec 1).

    pip install -r requirements.txt
    uvicorn app.api:app --reload

Mirrors the zero-dependency demo server (app/webserver.py) but adds CORS (for the Expo
app / web client), graceful error handling, and the same /turn, /season, /health routes.
The core engine runs without FastAPI; this is the HTTP envelope. STT/TTS (Sarvam) attach
here at the voice milestone (docs/01 sec 6).
"""
from __future__ import annotations

import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .config import settings
from .content.tales import SEASON_ORDER, TALES
from .engine import run_turn
from .models import TurnRequest
from .voice import sarvam

app = FastAPI(title="Katha", version="0.1.0",
              description="AI interactive visual novel — Phase 1: Vikram aur Betaal")

# Dev-open CORS so the Expo app / browser client can call us. Restrict origins in prod.
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# Serve generated art from C:\Katha\assets (drop-in slots; see docs/14).
_ASSETS = Path(__file__).resolve().parents[2] / "assets"
if _ASSETS.is_dir():
    app.mount("/assets", StaticFiles(directory=str(_ASSETS)), name="assets")


class TurnIn(BaseModel):
    session_id: str
    player_input: str = ""
    language: str = "en"
    scene_id: str = ""
    choice_id: str | None = None
    player_id: str = ""


class ChoiceOut(BaseModel):
    id: str
    label: str


class TurnOut(BaseModel):
    scene_id: str
    speaker: str
    line: str
    expression: str
    choices: list[ChoiceOut]
    ambient: str
    voice_profile: str
    fallback_used: bool
    meta: dict


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": app.version}


@app.get("/season")
def season() -> dict:
    return {
        "order": [{"id": t, "title": TALES[t]["title"], "kind": TALES[t].get("kind", "tale")}
                  for t in SEASON_ORDER],
        "tts_enabled": settings.tts_enabled,
    }


class TtsIn(BaseModel):
    text: str
    voice_profile: str = ""
    language: str = ""


@app.post("/tts")
def tts(body: TtsIn) -> dict:
    return {"audio": sarvam.synthesize(body.text, body.voice_profile, body.language), "format": "wav"}


@app.post("/turn", response_model=TurnOut)
def turn(body: TurnIn) -> TurnOut:
    render = run_turn(TurnRequest(
        session_id=body.session_id, player_input=body.player_input,
        language=body.language, scene_id=body.scene_id, choice_id=body.choice_id,
        player_id=body.player_id,
    ))
    return TurnOut(
        scene_id=render.scene_id, speaker=render.speaker, line=render.line,
        expression=render.expression,
        choices=[ChoiceOut(id=c.id, label=c.label) for c in render.choices],
        ambient=render.ambient, voice_profile=render.voice_profile,
        fallback_used=render.fallback_used, meta=render.meta,
    )


@app.exception_handler(Exception)
async def graceful_error(request, exc):  # never 500 into the player's face
    return JSONResponse(status_code=200, content={
        "scene_id": "", "speaker": "Betaal", "expression": "amused",
        "line": ("Betaal flickers. \"The night itself stumbles, little king. Ask me again "
                 "in a moment.\""),
        "choices": [], "ambient": "", "voice_profile": "", "fallback_used": True,
        "meta": {"intent": "error"}})
