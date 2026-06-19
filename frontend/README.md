# Katha — Frontend (Expo / React Native)

The visual-novel client for **Phase 1: Vikram aur Betaal**. It talks to the Katha backend's
`/turn` and `/season` endpoints and renders the scene, Betaal's dialogue (typewriter),
choices, the trust/dharma HUD, and the season finale.

## Two ways to play

### 1. Instant browser demo (no install) — recommended first
The backend ships a built-in web client. No npm, no Expo, no API keys:
```bash
cd ../backend
python -m app.webserver      # open http://127.0.0.1:8000
```

### 2. This Expo app (mobile / Play Store target)
```bash
# 1) start the backend (serves /turn and /season)
cd ../backend && python -m app.webserver

# 2) in another terminal, run the app
cd frontend
npm install
npm start                    # press w (web), a (Android), or i (iOS)
```
Set the backend address in [src/config.ts](src/config.ts):
- web / iOS simulator → `http://127.0.0.1:8000`
- Android emulator → `http://10.0.2.2:8000`
- physical device (Expo Go) → `http://<your-computer-LAN-IP>:8000`

## Structure
```
App.tsx                      entry
src/
├── config.ts                API_BASE
├── api.ts                   postTurn() / fetchSeason()
├── types.ts                 SceneRender, Choice, ...
├── theme.ts                 palette + per-scene gradients + portrait glyphs
├── components/
│   ├── SceneBackground.tsx  gradient that shifts per scene
│   ├── Portrait.tsx         character portrait + expression
│   ├── DialoguePanel.tsx    speaker + typewriter line + ambient
│   └── Choices.tsx          choice buttons
└── screens/
    └── GameScreen.tsx       orchestrates a turn loop (mirrors the verified web client)
```

## Notes / next steps
- **Art & portraits:** placeholders (glyphs + gradients) until generated assets land
  (Midjourney/Flux per the HANDOFF visual direction). Drop images into `assets/` and swap them
  into `Portrait`/`SceneBackground`.
- **Voice:** the HUD has a stub toggle; wire Sarvam STT/TTS at the API layer (docs/01 §6).
- **Typecheck:** `npm run tsc`.
