import { Platform } from "react-native";

// Palette from HANDOFF visual direction: deep indigo/navy, amber/saffron, gold accents.
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

// Background gradient stops per scene, keyed by a substring of scene_id.
export function backgroundFor(sceneId: string): [string, string, string] {
  if (sceneId.includes("prologue")) return ["#5a3a1e", "#2c1f12", "#0b0a08"]; // warm court
  if (sceneId.includes("climax")) return ["#5b1622", "#27101c", "#0a0510"]; // blood/fire
  if (sceneId.includes("three-suitors")) return ["#16384a", "#0e2230", "#060e16"]; // river ghat
  return ["#2a2150", "#161235", "#070612"]; // cremation ground (default)
}

export const portraitGlyph: Record<string, string> = {
  Betaal: "☾",
  Narrator: "❖",
  Kshantishila: "⚯",
  Vikramaditya: "♛",
  Madanasundari: "✿",
  Maiden: "✿",
};
