"""Per-character voice profiles (docs/01 sec 6).

Each tale's `voice_profiles` (in content/tales.py) names a profile per speaker. Here we map
that name to BOTH:
  * Sarvam: a `speaker` voice + language (production quality, Indian voices).
  * Browser: pitch/rate hints for the free SpeechSynthesis fallback (in app/web/index.html).

NOTE: confirm/expand the Sarvam `speaker` names against the current Bulbul speaker list
(docs.sarvam.ai). 'shubh' (male) and 'anushka' (female) are the documented defaults; the
others below reuse them until the full roster is wired.
"""
from __future__ import annotations

# name -> {speaker (Sarvam), lang (BCP-47), pitch, rate}  (pitch/rate are browser hints)
PROFILES: dict[str, dict] = {
    "betaal_sonorous": {"speaker": "shubh", "lang": "en-IN", "pitch": 0.6, "rate": 0.86},
    "sutradhar":       {"speaker": "shubh", "lang": "en-IN", "pitch": 0.8, "rate": 0.95},  # narrator
    "king_regal":      {"speaker": "shubh", "lang": "en-IN", "pitch": 0.9, "rate": 0.95},  # Vikramaditya
    "m_unctuous":      {"speaker": "shubh", "lang": "en-IN", "pitch": 1.05, "rate": 0.95},  # Kshantishila
    "m_measured":      {"speaker": "shubh", "lang": "en-IN", "pitch": 0.95, "rate": 0.95},
    "m_plain":         {"speaker": "shubh", "lang": "en-IN", "pitch": 1.0, "rate": 1.0},
    "m_proud":         {"speaker": "shubh", "lang": "en-IN", "pitch": 0.95, "rate": 1.0},
    "m_quiet":         {"speaker": "shubh", "lang": "en-IN", "pitch": 0.85, "rate": 0.9},
    "m_learned":      {"speaker": "shubh", "lang": "en-IN", "pitch": 1.0, "rate": 0.95},
    "m_grave":         {"speaker": "shubh", "lang": "en-IN", "pitch": 0.8, "rate": 0.9},
    "m_young":         {"speaker": "shubh", "lang": "en-IN", "pitch": 1.15, "rate": 1.0},
    "m_child":         {"speaker": "shubh", "lang": "en-IN", "pitch": 1.3, "rate": 1.0},
    "m_broken":        {"speaker": "shubh", "lang": "en-IN", "pitch": 0.8, "rate": 0.85},
    "f_grave":         {"speaker": "anushka", "lang": "en-IN", "pitch": 0.9, "rate": 0.9},
    "f_soft":          {"speaker": "anushka", "lang": "en-IN", "pitch": 1.0, "rate": 0.92},
}

_DEFAULT = {"speaker": "shubh", "lang": "en-IN", "pitch": 1.0, "rate": 1.0}


def get(name: str) -> dict:
    return PROFILES.get(name or "", _DEFAULT)
