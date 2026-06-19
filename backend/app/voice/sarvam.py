"""Sarvam Bulbul TTS — production voice (key-gated, stdlib urllib, cached).

POST {sarvam_tts_url} with header `api-subscription-key`:
  body: {text, target_language_code, speaker, model, speech_sample_rate}
  resp: {"audios": ["<base64 wav>", ...]}

Returns base64 WAV (the /tts endpoint passes it to the client). No key -> returns None and
the client uses the browser's built-in speech instead.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request

from ..config import settings
from . import profiles

# Cache SUCCESSFUL syntheses only (text+profile+lang -> base64). A transient failure must
# never be cached, or that line would stay silent for the whole process.
_CACHE: dict[tuple[str, str, str], str] = {}


def enabled() -> bool:
    return settings.tts_enabled


def _request(text: str, profile_name: str, language: str) -> str | None:
    prof = profiles.get(profile_name)
    body = json.dumps({
        "text": text[:2500],                       # REST limit
        "target_language_code": language or prof["lang"],
        "speaker": prof["speaker"],
        "model": settings.sarvam_model,
        "speech_sample_rate": settings.sarvam_sample_rate,
    }).encode("utf-8")
    req = urllib.request.Request(
        settings.sarvam_tts_url, data=body,
        headers={"Content-Type": "application/json",
                 "api-subscription-key": settings.sarvam_api_key},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            audios = json.loads(resp.read()).get("audios") or []
        return audios[0] if audios else None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError, IndexError):
        return None


def synthesize(text: str, profile_name: str = "", language: str = "") -> str | None:
    """base64 WAV, or None (no key / failure -> client falls back to browser speech)."""
    if not enabled() or not text.strip():
        return None
    key = (text.strip(), profile_name or "", language or "")
    if key in _CACHE:
        return _CACHE[key]
    audio = _request(*key)
    if audio:                       # cache successes only
        _CACHE[key] = audio
    return audio
