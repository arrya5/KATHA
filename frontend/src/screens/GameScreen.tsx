import * as Speech from "expo-speech";
import { useEffect, useRef, useState } from "react";
import {
  ActivityIndicator, Platform, Pressable, StatusBar, StyleSheet, Text, TextInput, View,
} from "react-native";
import { fetchSeason, postTurn } from "../api";

// Top inset without the safe-area-context native module (which mismatches Expo Go):
// Android exposes the status-bar height directly; iOS notch ≈ 50.
const TOP_INSET = Platform.OS === "android" ? (StatusBar.currentHeight ?? 28) : 50;
const BOTTOM_INSET = 16;
import { Choices } from "../components/Choices";
import { DialoguePanel } from "../components/DialoguePanel";
import { Portrait } from "../components/Portrait";
import { SceneBackground } from "../components/SceneBackground";
import { theme } from "../theme";
import type { SceneRender, SeasonEntry } from "../types";

const SID = "app-" + Math.random().toString(36).slice(2);

// Per-character pitch/rate for the device TTS (expo-speech).
const VOICE: Record<string, { pitch: number; rate: number }> = {
  betaal_sonorous: { pitch: 0.6, rate: 0.84 }, sutradhar: { pitch: 0.8, rate: 0.92 },
  king_regal: { pitch: 0.9, rate: 0.94 }, m_unctuous: { pitch: 1.05, rate: 0.92 },
  f_grave: { pitch: 1.4, rate: 0.9 }, f_soft: { pitch: 1.5, rate: 0.92 },
  m_grave: { pitch: 0.8, rate: 0.9 }, m_child: { pitch: 1.6, rate: 1.0 },
};

export function GameScreen() {
  const [render, setRender] = useState<SceneRender | null>(null);
  const [season, setSeason] = useState<SeasonEntry[]>([]);
  const [busy, setBusy] = useState(false);
  const [text, setText] = useState("");
  const [voiceOn, setVoiceOn] = useState(false);
  const voiceRef = useRef(false);
  const scene = useRef("prologue");
  const idx = useRef(0);

  function speak(r: SceneRender | null) {
    Speech.stop();
    if (!voiceRef.current || !r || !r.line) return;
    const p = VOICE[r.voice_profile] || { pitch: 1, rate: 1 };
    Speech.speak(r.line.replace(/[*"]/g, ""), { language: "en-IN", pitch: p.pitch, rate: p.rate });
  }

  function toggleVoice() {
    const v = !voiceRef.current;
    voiceRef.current = v;
    setVoiceOn(v);
    if (v) speak(render); else Speech.stop();
  }

  async function turn(playerInput = "", choiceId: string | null = null) {
    setBusy(true);
    try {
      const r = await postTurn({ session_id: SID, player_input: playerInput, choice_id: choiceId, scene_id: scene.current });
      setRender(r);
      speak(r);
    } catch {
      setRender({
        scene_id: scene.current, speaker: "Narrator",
        line: "The connection to the cremation ground is lost. Is the backend running?",
        expression: "grave", choices: [], ambient: "", voice_profile: "", fallback_used: true, meta: {},
      });
    } finally {
      setBusy(false);
    }
  }

  function gotoScene(id: string) {
    scene.current = id;
    idx.current = season.findIndex((s) => s.id === id);
    turn("begin");
  }

  useEffect(() => {
    (async () => {
      try { setSeason(await fetchSeason()); } catch {}
      turn("begin");
    })();
    return () => { Speech.stop(); };
  }, []);

  const m = render?.meta ?? {};
  const title = season[idx.current]?.title ?? scene.current;

  return (
    <SceneBackground sceneId={render?.scene_id ?? "prologue"}>
      <View style={[styles.root, { paddingTop: TOP_INSET + 6 }]}>
        <View style={styles.hud}>
          <Text style={styles.brand}>KATHA</Text>
          <View style={styles.grow} />
          <Text style={styles.stat}>Trust {m.trust ?? 0}</Text>
          <Text style={styles.stat}>Dharma {m.dharma ?? 0}</Text>
          <Pressable onPress={toggleVoice} hitSlop={10}>
            <Text style={[styles.stat, voiceOn && styles.statOn]}>{voiceOn ? "🔊" : "🔇"}</Text>
          </Pressable>
        </View>

        <View style={styles.stage}>
          {render && <Portrait speaker={render.speaker} expression={render.expression} />}
        </View>

        <View style={[styles.panel, { paddingBottom: BOTTOM_INSET }]}>
          {render ? (
            <>
              <DialoguePanel speaker={render.speaker} line={render.line} ambient={render.ambient} />
              <View style={styles.controls}>
                <Choices choices={render.choices} onPick={(id) => turn("", id)} />

                {!!m.advance_to && (
                  <Pressable style={styles.choice} onPress={() => gotoScene(m.advance_to!)}>
                    <Text style={styles.choiceLabel}>▸ Take up the corpse and walk on…</Text>
                  </Pressable>
                )}
                {!!m.season_complete && (
                  <Text style={styles.ending}>
                    ❖ {(m.outcome ?? "the road ends").replace(/_/g, " ").toUpperCase()} ❖
                  </Text>
                )}

                <View style={styles.row}>
                  <TextInput
                    style={styles.input} value={text} onChangeText={setText}
                    placeholder="Speak, or name a character…" placeholderTextColor={theme.dim}
                    onSubmitEditing={() => { if (text.trim()) { turn(text.trim()); setText(""); } }}
                  />
                  <Pressable style={styles.btn} onPress={() => { if (text.trim()) { turn(text.trim()); setText(""); } }}>
                    <Text style={styles.btnText}>Speak</Text>
                  </Pressable>
                </View>

                <View style={styles.row}>
                  <Pressable style={styles.btn} onPress={() => turn("continue")}>
                    <Text style={styles.btnText}>Continue ▸</Text>
                  </Pressable>
                  <Pressable style={styles.btn} onPress={() => {
                    if (idx.current < season.length - 1) gotoScene(season[idx.current + 1].id);
                  }}>
                    <Text style={styles.btnText}>Next ▸</Text>
                  </Pressable>
                  <View style={styles.grow} />
                  <Text style={styles.sceneTag} numberOfLines={1}>{title}</Text>
                </View>
              </View>
            </>
          ) : (
            <ActivityIndicator color={theme.gold} />
          )}
          {busy && <ActivityIndicator color={theme.gold} style={styles.busy} />}
        </View>
      </View>
    </SceneBackground>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, paddingHorizontal: 16 },
  hud: { flexDirection: "row", alignItems: "center", gap: 8, paddingBottom: 4 },
  brand: { color: theme.gold, fontSize: 14, letterSpacing: 4, fontFamily: theme.serif },
  grow: { flex: 1 },
  stat: { color: theme.dim, fontSize: 12, borderColor: "rgba(201,168,76,0.35)", borderWidth: 1, borderRadius: 12, paddingHorizontal: 9, paddingVertical: 3, overflow: "hidden" },
  statOn: { color: theme.gold, borderColor: theme.gold },
  stage: { flex: 1, alignItems: "center", justifyContent: "center" },
  panel: { backgroundColor: theme.panel, borderTopColor: theme.gold, borderTopWidth: 2, borderRadius: 14, padding: 16 },
  controls: { marginTop: 14, gap: 9 },
  choice: { backgroundColor: "rgba(201,168,76,0.10)", borderColor: "rgba(201,168,76,0.5)", borderWidth: 1, borderRadius: 10, paddingVertical: 12, paddingHorizontal: 14 },
  choiceLabel: { color: theme.text, fontSize: 16, fontFamily: theme.serif },
  row: { flexDirection: "row", alignItems: "center", gap: 8 },
  input: { flex: 1, backgroundColor: "rgba(255,255,255,0.06)", borderColor: "rgba(255,255,255,0.18)", borderWidth: 1, borderRadius: 10, color: theme.text, paddingHorizontal: 12, paddingVertical: 11, fontSize: 15, fontFamily: theme.serif },
  btn: { borderColor: "rgba(201,168,76,0.5)", borderWidth: 1, borderRadius: 10, paddingHorizontal: 14, paddingVertical: 11 },
  btnText: { color: theme.gold, fontSize: 14, fontFamily: theme.serif },
  sceneTag: { color: theme.dim, fontSize: 12, fontFamily: theme.serif, flexShrink: 1 },
  ending: { color: theme.gold, textAlign: "center", fontSize: 17, letterSpacing: 2, paddingVertical: 8, fontFamily: theme.serif },
  busy: { position: "absolute", top: 12, right: 12 },
});
