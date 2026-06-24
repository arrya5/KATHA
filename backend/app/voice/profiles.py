"""Per-character voice profiles (docs/01 sec 6).

Each tale's `voice_profiles` (in content/tales.py) names a profile per speaker. Here we map
that name to BOTH:
  * Sarvam Bulbul v3: a `speaker` voice + language + pace/temperature (production Indian voices).
  * Browser: pitch/rate hints for the free SpeechSynthesis fallback (in app/web/index.html).

Confirmed Bulbul v3 speaker roster (30+ voices, shared between bulbul:v3 and bulbul:v3-beta):
  Male:   kabir, rahul, aditya, manan, advait, aayan, ashutosh, varun, rohan, amit, dev,
          sumit, ratan, shubh (default)
  Female: roopa, priya, ritu, neha, pooja, simran, kavya, ishita, shreya, sophia, amelia, anushka

Voice assignments rationale:
  betaal_sonorous → kabir   : Deep, resonant, ancient-feeling male voice; theatrical
  king_regal      → rahul   : Measured, strong, commanding — fitting for a just king
  sutradhar       → aditya  : Clear, articulate narrator voice
  m_unctuous      → manan   : Smooth, persuasive — perfect for the oily mendicant Kshantishila
  m_measured      → ratan   : Steady, thoughtful male
  m_plain         → shubh   : Default clean male voice
  m_proud         → rohan   : Confident, slightly elevated tone
  m_quiet         → sumit   : Quieter, understated delivery
  m_learned       → advait  : Scholarly, considered pacing
  m_grave         → varun   : Heavy, weighted — for morally serious moments
  m_young         → aayan   : Younger-sounding male voice
  m_child         → ashutosh: Lightest male voice for child characters
  m_broken        → dev     : Rough, strained — for characters in grief or defeat
  f_grave         → roopa   : Deep female voice; sorrow and gravity
  f_soft          → priya   : Warm, gentle — for calm female characters

pace: 0.5–2.0 (1.0 = normal); temperature: 0.01–2.0 (higher = more expressive/varied)
"""
from __future__ import annotations

# name -> {speaker (Sarvam), lang (BCP-47), pace, temperature, pitch, rate}
# pitch/rate are browser SpeechSynthesis fallback hints only (ignored by Sarvam).
# pace/temperature are Sarvam Bulbul v3 `properties` fields.
PROFILES: dict[str, dict] = {
    # ── Principal characters ────────────────────────────────────────────────
    "betaal_sonorous": {
        "speaker": "kabir", "lang": "hi-IN",
        "pace": 0.82, "temperature": 1.3,     # slow, dramatic, expressive
        "pitch": 0.6, "rate": 0.86,            # browser fallback
    },
    "sutradhar": {
        "speaker": "aditya", "lang": "hi-IN",
        "pace": 0.95, "temperature": 1.0,     # clear narrator, slightly measured
        "pitch": 0.8, "rate": 0.95,
    },
    "king_regal": {
        "speaker": "rahul", "lang": "hi-IN",
        "pace": 0.92, "temperature": 0.9,     # measured, controlled, regal
        "pitch": 0.9, "rate": 0.95,
    },
    # ── The mendicant — Kshantishila ────────────────────────────────────────
    "m_unctuous": {
        "speaker": "manan", "lang": "hi-IN",
        "pace": 0.9, "temperature": 0.85,     # smooth, slightly unctuous cadence
        "pitch": 1.05, "rate": 0.95,
    },
    # ── Generic male character profiles ────────────────────────────────────
    "m_measured": {
        "speaker": "ratan", "lang": "hi-IN",
        "pace": 0.95, "temperature": 0.9,
        "pitch": 0.95, "rate": 0.95,
    },
    "m_plain": {
        "speaker": "shubh", "lang": "hi-IN",
        "pace": 1.0, "temperature": 1.0,
        "pitch": 1.0, "rate": 1.0,
    },
    "m_proud": {
        "speaker": "rohan", "lang": "hi-IN",
        "pace": 1.0, "temperature": 0.95,     # confident, slightly elevated
        "pitch": 0.95, "rate": 1.0,
    },
    "m_quiet": {
        "speaker": "sumit", "lang": "hi-IN",
        "pace": 0.88, "temperature": 0.8,     # soft, understated
        "pitch": 0.85, "rate": 0.9,
    },
    "m_learned": {
        "speaker": "advait", "lang": "hi-IN",
        "pace": 0.92, "temperature": 0.85,    # scholarly, deliberate
        "pitch": 1.0, "rate": 0.95,
    },
    "m_grave": {
        "speaker": "varun", "lang": "hi-IN",
        "pace": 0.85, "temperature": 1.1,     # heavy, weighted, morally serious
        "pitch": 0.8, "rate": 0.9,
    },
    "m_young": {
        "speaker": "aayan", "lang": "hi-IN",
        "pace": 1.05, "temperature": 1.1,     # younger energy
        "pitch": 1.15, "rate": 1.0,
    },
    "m_child": {
        "speaker": "ashutosh", "lang": "hi-IN",
        "pace": 1.1, "temperature": 1.2,      # lightest male voice for children
        "pitch": 1.3, "rate": 1.0,
    },
    "m_broken": {
        "speaker": "dev", "lang": "hi-IN",
        "pace": 0.82, "temperature": 1.2,     # strained, grief-heavy
        "pitch": 0.8, "rate": 0.85,
    },
    # ── Female character profiles ────────────────────────────────────────────
    "f_grave": {
        "speaker": "roopa", "lang": "hi-IN",
        "pace": 0.88, "temperature": 1.1,     # deep female, sorrowful gravitas
        "pitch": 0.9, "rate": 0.9,
    },
    "f_soft": {
        "speaker": "priya", "lang": "hi-IN",
        "pace": 0.93, "temperature": 0.95,    # warm, gentle
        "pitch": 1.0, "rate": 0.92,
    },
}

_DEFAULT: dict = {"speaker": "shubh", "lang": "hi-IN", "pace": 1.0, "temperature": 1.0,
                  "pitch": 1.0, "rate": 1.0}


def get(name: str) -> dict:
    return PROFILES.get(name or "", _DEFAULT)

