"""Sarvam Bulbul v3 TTS — production voice (key-gated, stdlib urllib, cached).

POST {sarvam_tts_url} with header `api-subscription-key`:
  body: {text, target_language_code, speaker, model, speech_sample_rate, properties}
  resp: {"audios": ["<base64 wav>", ...]}

`properties` carries per-character pace (0.5–2.0) and temperature (0.01–2.0), read from
the voice profile. This is what makes Betaal sound slow and dramatic vs. the narrator crisp.

Returns base64 WAV (the /tts endpoint passes it to the client). No key → returns None and
the client uses the browser's built-in speech instead.

Latency strategy (docs/01 §7.2 — target < 2.5 s to first spoken word):
  synthesize_first_sentence() splits the text on sentence boundaries, synthesises only the
  first sentence immediately (fast), and queues the rest async. The caller can stream the
  first chunk to the client while the remainder arrives.
"""
from __future__ import annotations

import json
import logging
import re
import urllib.error
import urllib.request

from ..config import settings
from . import profiles

log = logging.getLogger("katha.voice")

# Cache SUCCESSFUL syntheses only (text+profile+lang -> base64). A transient failure must
# never be cached, or that line would stay silent for the whole process.
_CACHE: dict[tuple[str, str, str], str] = {}


def enabled() -> bool:
    return settings.tts_enabled


def _build_body(text: str, prof: dict, language: str) -> bytes:
    """Assemble the JSON request body including Bulbul v3 `properties`."""
    lang = language or prof.get("lang", "hi-IN")
    payload: dict = {
        "text": text[:2500],                        # REST character limit
        "target_language_code": lang,
        "speaker": prof.get("speaker", "shubh"),
        "model": settings.sarvam_model,
        "speech_sample_rate": settings.sarvam_sample_rate,
    }
    # Pass pace / temperature if the profile defines them (Bulbul v3 feature).
    props: dict = {}
    if "pace" in prof:
        props["pace"] = prof["pace"]
    if "temperature" in prof:
        props["temperature"] = prof["temperature"]
    if props:
        payload["properties"] = props
    return json.dumps(payload).encode("utf-8")


def _request(text: str, profile_name: str, language: str) -> str | None:
    prof = profiles.get(profile_name)
    body = _build_body(text, prof, language)
    req = urllib.request.Request(
        settings.sarvam_tts_url, data=body,
        headers={"Content-Type": "application/json",
                 "api-subscription-key": settings.sarvam_api_key},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            audios = json.loads(resp.read()).get("audios") or []
        return audios[0] if audios else None
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            log.warning("sarvam: 401 Unauthorized — check SARVAM_API_KEY")
        else:
            log.warning("sarvam: HTTP %s from TTS endpoint", exc.code)
        return None
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError, IndexError) as exc:
        log.warning("sarvam: TTS request failed — %s", exc)
        return None


def synthesize(text: str, profile_name: str = "", language: str = "") -> str | None:
    """Return base64 WAV, or None (no key / failure → client falls back to browser speech)."""
    if not enabled() or not text.strip():
        return None
    key = (text.strip(), profile_name or "", language or "")
    if key in _CACHE:
        return _CACHE[key]
    audio = _request(*key)
    if audio:                        # cache successes only
        _CACHE[key] = audio
    return audio


# ── First-sentence streaming helper (docs/01 §7.2) ──────────────────────────
_SENTENCE_RE = re.compile(r'(?<=[.!?।])\s+')


def _split_sentences(text: str) -> list[str]:
    """Split on sentence boundaries (handles English ., !, ? and Hindi ।)."""
    parts = _SENTENCE_RE.split(text.strip())
    return [p for p in parts if p.strip()]


def synthesize_first_sentence(
    text: str, profile_name: str = "", language: str = ""
) -> tuple[str | None, str]:
    """Synthesise the first sentence immediately for low-latency first-word delivery.

    Returns:
        (first_audio_b64_or_None, remainder_text)

    The caller should:
      1. Stream `first_audio_b64` to the client immediately.
      2. Call synthesize(remainder_text, ...) async / in background.
    """
    if not text.strip():
        return None, ""
    sentences = _split_sentences(text)
    first = sentences[0]
    remainder = " ".join(sentences[1:]) if len(sentences) > 1 else ""
    return synthesize(first, profile_name, language), remainder
