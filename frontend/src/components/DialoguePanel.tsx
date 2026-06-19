import { useEffect, useRef, useState } from "react";
import { Pressable, ScrollView, StyleSheet, Text, View } from "react-native";
import { theme } from "../theme";

/** Speaker + typewriter line + ambient. Tap the line to skip the typewriter. */
export function DialoguePanel({
  speaker, line, ambient,
}: { speaker: string; line: string; ambient: string }) {
  const [shown, setShown] = useState("");
  const timer = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    if (timer.current) clearInterval(timer.current);
    setShown("");
    let i = 0;
    timer.current = setInterval(() => {
      i += 1;
      setShown(line.slice(0, i));
      if (i >= line.length && timer.current) clearInterval(timer.current);
    }, 16);
    return () => { if (timer.current) clearInterval(timer.current); };
  }, [line]);

  return (
    <View>
      <Text style={styles.speaker}>{speaker}</Text>
      <Pressable onPress={() => setShown(line)}>
        <ScrollView style={styles.lineBox}>
          <Text style={styles.line}>{shown}</Text>
        </ScrollView>
      </Pressable>
      {!!ambient && <Text style={styles.ambient}>❧ {ambient}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  speaker: { color: theme.gold, fontSize: 13, letterSpacing: 3, marginBottom: 6 },
  lineBox: { maxHeight: 180 },
  line: { color: theme.text, fontSize: 18, lineHeight: 27 },
  ambient: { color: theme.dim, fontStyle: "italic", fontSize: 12, marginTop: 6 },
});
