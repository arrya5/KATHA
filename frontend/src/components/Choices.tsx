import { Pressable, StyleSheet, Text, View } from "react-native";
import { theme } from "../theme";
import type { Choice } from "../types";

export function Choices({ choices, onPick }: { choices: Choice[]; onPick: (id: string) => void }) {
  if (!choices.length) return null;
  return (
    <View style={styles.wrap}>
      {choices.map((c) => (
        <Pressable key={c.id} style={styles.choice} onPress={() => onPick(c.id)}>
          <Text style={styles.label}>{c.label}</Text>
        </Pressable>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: { gap: 8 },
  choice: {
    backgroundColor: "rgba(201,168,76,0.10)", borderColor: "rgba(201,168,76,0.5)",
    borderWidth: 1, borderRadius: 8, paddingVertical: 11, paddingHorizontal: 14,
  },
  label: { color: theme.text, fontSize: 16 },
});
