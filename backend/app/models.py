"""Core domain models for a turn.

Plain stdlib dataclasses so the engine runs without pydantic/FastAPI installed.
The FastAPI layer (app/api.py) defines request/response schemas that convert to/from
these.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# --- Moderation -------------------------------------------------------------
class Verdict(str, Enum):
    ALLOW = "allow"
    DEFLECT = "deflect"
    BLOCK = "block"


@dataclass
class ModerationResult:
    verdict: Verdict = Verdict.ALLOW
    reason: str = ""
    strike_delta: int = 0
    category: str = "benign"


# --- Intent (what the player is doing this turn) ----------------------------
class Intent(str, Enum):
    NARRATE = "narrate"        # advance/hear the tale
    INVESTIGATE = "investigate"  # question a tale character (lean-in)
    JUDGE = "judge"            # answer the riddle
    SMALLTALK = "smalltalk"    # talk to Betaal directly


# --- RAG units --------------------------------------------------------------
@dataclass
class CanonChunk:
    chunk_id: str
    tale_id: str
    speaker: str
    characters_present: list[str]
    text: str
    themes: list[str] = field(default_factory=list)
    source: str = "Baital Pachisi (public domain)"


@dataclass
class WorldEvent:
    """A thing that happened. `known_to` is the crux of the asymmetry engine
    (docs/01 sec 3.2): an agent can only ever retrieve an event whose `known_to`
    contains its id."""
    id: str
    session_id: str
    scene_id: str
    description: str
    known_to: list[str]
    turn_no: int
    dharma_relevant: bool = False


@dataclass
class Memory:
    npc_id: str
    session_id: str
    text: str
    turn_no: int
    salience: float = 1.0


# --- Generation output ------------------------------------------------------
@dataclass
class NpcDraft:
    npc_id: str
    line: str
    expression: str = "neutral"      # narrator/portrait cue
    trust_delta: int = 0
    memory_note: Optional[str] = None
    reveal: Optional[str] = None      # a fragment of the meta-arc conspiracy


@dataclass
class Choice:
    id: str
    label: str


@dataclass
class SceneRender:
    scene_id: str
    speaker: str
    line: str
    expression: str = "neutral"
    choices: list[Choice] = field(default_factory=list)
    ambient: str = ""
    voice_profile: str = ""
    fallback_used: bool = False
    meta: dict = field(default_factory=dict)


# --- The turn request + threaded state --------------------------------------
@dataclass
class TurnRequest:
    session_id: str
    player_input: str
    language: str = "en"
    scene_id: str = ""
    choice_id: Optional[str] = None   # set when the player taps a choice button


@dataclass
class TurnState:
    """Threaded through every node of the turn graph (docs/01 sec 2)."""
    request: TurnRequest
    scene_id: str = ""
    moderation: ModerationResult = field(default_factory=ModerationResult)
    intent: Intent = Intent.SMALLTALK
    active_npc_id: str = "betaal"
    investigate_target: Optional[str] = None
    retrieval: dict = field(default_factory=dict)   # context handed to the NPC node
    draft: Optional[NpcDraft] = None
    world_updates: list[WorldEvent] = field(default_factory=list)
    dharma_delta: int = 0
    render: Optional[SceneRender] = None
