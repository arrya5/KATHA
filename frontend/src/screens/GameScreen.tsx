import { useEffect, useRef, useState } from "react";
import {
  ActivityIndicator, Pressable, SafeAreaView, StyleSheet, Text, TextInput, View,
} from "react-native";
import { fetchSeason, postTurn } from "../api";
import { Choices } from "../components/Choices";
import { DialoguePanel } from "../components/DialoguePanel";
import { Portrait } from "../components/Portrait";
import { SceneBackground } from "../components/SceneBackground";
import { theme } from "../theme";
import type { SceneRender, SeasonEntry } from "../types";

const SID = "app-" + Math.random().toString(36).slice(2);

export function GameScreen() {
  const [render, setRender] = useState<SceneRender | null>(null);
  const [season, setSeason] = useState<SeasonEntry[]>([]);
  const [busy, setBusy] = useState(false);
  const [text, setText] = useState("");
  const scene = useRef("prologue");
  const idx = useRef(0);

  async function turn(playerInput = "", choiceId: string | null = null) {
    setBusy(true);
    try {
      setRender(await postTurn({ session_id: SID, player_input: playerInput, choice_id: choiceId, scene_id: scene.current }));
    } catch (e) {
      setRender({
        scene_id: scene.current, speaker: "Narrator",
        line: "The connection to the cremation ground is lost. Is the backend running?  (cd backend && python -m app.webserver)",
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
      turn("begin"); // open on the prologue
    })();
  }, []);

  const m = render?.meta ?? {};
  const title = season[idx.current]?.title ?? scene.current;

  return (
    <SceneBackground sceneId={render?.scene_id ?? "prologue"}>
      <SafeAreaView style={styles.root}>
        <View style={styles.hud}>
          <Text style={styles.brand}>KATHA · Vikram aur Betaal</Text>
          <View style={styles.grow} />
          <Text style={styles.stat}>Trust {m.trust ?? 0}</Text>
          <Text style={styles.stat}>Dharma {m.dharma ?? 0}</Text>
        </View>

        {render && <Portrait speaker={render.speaker} expression={render.expression} />}

        <View style={styles.grow} />

        <View style={styles.panel}>
          {render ? (
            <>
              <DialoguePanel speaker={render.speaker} line={render.line} ambient={render.ambient} />
              <View style={styles.controls}>
                <Choices choices={render.choices} onPick={(id) => turn("", id)} />

                {!!m.advance_to && (
                  <Pressable style={[styles.choice]} onPress={() => gotoScene(m.advance_to!)}>
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
                    placeholder="Speak, or question a character by name…"
                    placeholderTextColor={theme.dim} onSubmitEditing={() => { if (text.trim()) { turn(text.trim()); setText(""); } }}
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
                    <Text style={styles.btnText}>Next scene ▸</Text>
                  </Pressable>
                  <View style={styles.grow} />
                  <Text style={styles.sceneTag}>{title}</Text>
                </View>
              </View>
            </>
          ) : (
            <ActivityIndicator color={theme.gold} />
          )}
          {busy && <ActivityIndicator color={theme.gold} style={styles.busy} />}
        </View>
      </SafeAreaView>
    </SceneBackground>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, paddingHorizontal: 16 },
  hud: { flexDirection: "row", alignItems: "center", paddingTop: 8, gap: 8 },
  brand: { color: theme.gold, fontSize: 12, letterSpacing: 2 },
  grow: { flex: 1 },
  stat: { color: theme.dim, fontSize: 12, borderColor: "rgba(201,168,76,0.35)", borderWidth: 1, borderRadius: 12, paddingHorizontal: 8, paddingVertical: 2 },
  panel: { backgroundColor: theme.panel, borderTopColor: theme.gold, borderTopWidth: 2, borderRadius: 12, padding: 16, marginBottom: 8 },
  controls: { marginTop: 12, gap: 8 },
  choice: { backgroundColor: "rgba(201,168,76,0.10)", borderColor: "rgba(201,168,76,0.5)", borderWidth: 1, borderRadius: 8, paddingVertical: 11, paddingHorizontal: 14 },
  choiceLabel: { color: theme.text, fontSize: 16 },
  row: { flexDirection: "row", alignItems: "center", gap: 8 },
  input: { flex: 1, backgroundColor: "rgba(255,255,255,0.06)", borderColor: "rgba(255,255,255,0.18)", borderWidth: 1, borderRadius: 8, color: theme.text, paddingHorizontal: 12, paddingVertical: 10, fontSize: 15 },
  btn: { borderColor: "rgba(201,168,76,0.5)", borderWidth: 1, borderRadius: 8, paddingHorizontal: 14, paddingVertical: 10 },
  btnText: { color: theme.gold, fontSize: 14 },
  sceneTag: { color: theme.dim, fontSize: 12 },
  ending: { color: theme.gold, textAlign: "center", fontSize: 16, letterSpacing: 2, paddingVertical: 6 },
  busy: { position: "absolute", top: 10, right: 10 },
});
