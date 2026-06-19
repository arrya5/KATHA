import { LinearGradient } from "expo-linear-gradient";
import { StyleSheet, View } from "react-native";
import { backgroundFor } from "../theme";

export function SceneBackground({ sceneId, children }: { sceneId: string; children: React.ReactNode }) {
  return (
    <LinearGradient colors={backgroundFor(sceneId)} style={StyleSheet.absoluteFill}>
      <View style={styles.vignette} />
      {children}
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  vignette: { ...StyleSheet.absoluteFillObject, backgroundColor: "transparent" },
});
