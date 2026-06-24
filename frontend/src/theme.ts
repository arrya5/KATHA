import { Platform } from "react-native";

// Palette from docs/14 art direction: deep indigo/navy night base, amber/saffron key
// light, gold accents (#C9A84C). Per-scene tint mirrors the doc's tint table.
export const theme = {
  gold: "#C9A84C",
  saffron: "#e8a33d",
  text: "#f3ead4",
  dim: "#b9b09a",
  ink: "#05060f",
  panel: "rgba(8,10,28,0.92)",
  // Mythic serif (Android: Noto Serif; iOS: Georgia) for a painted-storybook feel.
  serif: Platform.OS === "ios" ? "Georgia" : "serif",
};

// Background gradient stops per scene, keyed by a substring of scene_id. Tints follow the
// docs/14 per-scene table so the mobile gradient matches whatever painted art lands later.
export function backgroundFor(sceneId: string): [string, string, string] {
  const id = sceneId || "";
  if (id.includes("prologue")) return ["#5a3a1e", "#2c1f12", "#0b0a08"]; // Ujjain court, warm gold
  if (id.includes("climax")) return ["#5b1622", "#27101c", "#0a0510"]; // the circle, blood/fire
  if (id.includes("three-suitors")) return ["#16384a", "#0e2230", "#060e16"]; // river ghat, teal
  if (id.includes("lion")) return ["#1e3a2a", "#13241b", "#070f0b"]; // forest clearing, green-indigo
  if (id.includes("viravara")) return ["#1c2d52", "#101a33", "#060912"]; // palace gate, cold blue + torch
  if (id.includes("child-who-laughed")) return ["#3a2630", "#221019", "#0a0608"]; // sacrificial court, ashen dawn
  return ["#2a2150", "#161235", "#070612"]; // cremation ground (default), indigo + ember
}

// Per-speaker glyph (shown until real portrait art exists) and accent colour (drives the
// portrait halo / speaker name tint). Keyed by the DISPLAY name the backend synthesizer
// emits (title-cased mini-agent ids, e.g. "Tree Climber", "First Brahmin").
interface SpeakerStyle {
  glyph: string;
  accent: string;
}

const SPEAKERS: Record<string, SpeakerStyle> = {
  // Frame / recurring
  Betaal: { glyph: "☾", accent: "#9fd8e8" }, // spectral blue-gold (special-cased in Portrait)
  Narrator: { glyph: "❖", accent: theme.gold },
  Kshantishila: { glyph: "⚯", accent: "#b56b3a" }, // saffron robe, cold beneath
  Vikramaditya: { glyph: "♛", accent: theme.gold },
  // Tale 1 — Transposed Heads
  Madanasundari: { glyph: "✿", accent: "#d98aa6" },
  Dhavala: { glyph: "⚔", accent: "#c8a06a" },
  // Tale 2 — The Lion
  "Tree Climber": { glyph: "ᛗ", accent: "#8fae6a" },
  "First Brahmin": { glyph: "☷", accent: "#cbb06a" },
  // Tale 3 — Three Suitors
  "Ash Keeper": { glyph: "⚱", accent: "#9aa0a8" },
  Reviver: { glyph: "ॐ", accent: "#7fa6c4" },
  Maiden: { glyph: "✿", accent: "#e0a6b6" },
  // Tale 4 — Viravara
  Viravara: { glyph: "⚔", accent: "#b08a4c" },
  Son: { glyph: "✦", accent: "#d6c07a" },
  // Tale 5 — The Child Who Laughed
  Boy: { glyph: "✦", accent: "#e6dca8" },
  Father: { glyph: "☷", accent: "#7a6f5e" },
};

const DEFAULT_STYLE: SpeakerStyle = { glyph: "❖", accent: theme.gold };

export function speakerStyle(speaker: string): SpeakerStyle {
  if (SPEAKERS[speaker]) return SPEAKERS[speaker];
  // Unknown speaker: first letter as glyph, gold accent.
  return { glyph: (speaker || "?").slice(0, 1).toUpperCase(), accent: theme.gold };
}

// Back-compat: some call sites used portraitGlyph directly.
export const portraitGlyph: Record<string, string> = Object.fromEntries(
  Object.entries(SPEAKERS).map(([k, v]) => [k, v.glyph]),
);

// Expression -> visual tokens for the portrait (scale, glow radius, opacity, tint mix).
// Mirrors the backend's expression set: neutral | amused | intense | grave.
export interface ExpressionStyle {
  scale: number;
  glowRadius: number;
  glowColor: string;
  opacity: number;
  label: string;
}

const EXPRESSIONS: Record<string, ExpressionStyle> = {
  neutral: { scale: 1.0, glowRadius: 26, glowColor: theme.gold, opacity: 1, label: "NEUTRAL" },
  amused: { scale: 1.02, glowRadius: 30, glowColor: theme.gold, opacity: 1, label: "AMUSED" },
  intense: { scale: 1.06, glowRadius: 42, glowColor: theme.saffron, opacity: 1, label: "INTENSE" },
  grave: { scale: 0.98, glowRadius: 22, glowColor: "#6f6450", opacity: 0.88, label: "GRAVE" },
};

export function expressionStyle(expression: string): ExpressionStyle {
  return EXPRESSIONS[expression] ?? EXPRESSIONS.neutral;
}
