import { StyleSheet, Text, View } from "react-native";
import { portraitGlyph, theme } from "../theme";

export function Portrait({ speaker, expression }: { speaker: string; expression: string }) {
  const intense = expression === "intense";
  return (
    <View style={styles.wrap} pointerEvents="none">
      <View style={[styles.circle, intense && styles.intense, expression === "grave" && styles.grave]}>
        <Text style={styles.glyph}>{portraitGlyph[speaker] ?? speaker.slice(0, 1)}</Text>
      </View>
      {!!expression && <Text style={styles.expr}>{expression.toUpperCase()}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { alignItems: "center" },
  circle: {
    width: 140, height: 140, borderRadius: 70, alignItems: "center", justifyContent: "center",
    backgroundColor: theme.gold, borderWidth: 2, borderColor: "rgba(255,255,255,0.25)",
    shadowColor: theme.gold, shadowOpacity: 0.5, shadowRadius: 30, shadowOffset: { width: 0, height: 0 },
  },
  intense: { transform: [{ scale: 1.05 }], shadowColor: theme.saffron, shadowRadius: 40 },
  grave: { opacity: 0.85 },
  glyph: { fontSize: 60, color: "#1a1330" },
  expr: { marginTop: 10, color: theme.dim, fontSize: 11, letterSpacing: 3 },
});
