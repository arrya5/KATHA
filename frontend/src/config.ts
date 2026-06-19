import Constants from "expo-constants";
import { Platform } from "react-native";

// Where the Katha backend lives. By default we AUTO-DETECT your PC's address from Expo's
// dev connection, so the app reaches the backend on a phone/emulator with NO manual editing.
//
// Run the backend first:  cd backend && python -m app.webserver   (it listens on port 8000)
//
// Override only if needed (e.g. a deployed backend), by setting API_BASE_OVERRIDE below.
const API_BASE_OVERRIDE = ""; // e.g. "https://api.yourdomain.com"
const PORT = 8000;

function detect(): string {
  if (API_BASE_OVERRIDE) return API_BASE_OVERRIDE;

  // Expo exposes the Metro bundler host (your PC's LAN IP) — reuse it for the backend.
  const hostUri =
    Constants.expoConfig?.hostUri ||
    (Constants as any).expoGoConfig?.debuggerHost ||
    (Constants as any).manifest?.debuggerHost ||
    "";
  const host = hostUri.split(":")[0];

  if (host && host !== "127.0.0.1" && host !== "localhost") {
    return `http://${host}:${PORT}`;
  }
  // Fallbacks: Android emulator can't see the PC's loopback — use its host alias.
  if (Platform.OS === "android") return `http://10.0.2.2:${PORT}`;
  return `http://127.0.0.1:${PORT}`; // web / iOS simulator
}

export const API_BASE = detect();
