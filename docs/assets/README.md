# docs/assets

This directory holds media assets referenced in documentation and the root README.

## Expected files

| File | Purpose |
|---|---|
| `demo.gif` | Animated terminal/browser playthrough — the hero demo in the root README. Record with `python -m app.demo` or `python -m app.webserver`. |
| `demo.png` | Static fallback for environments that do not render GIFs. |
| `architecture.png` | Optional: rendered version of the Mermaid architecture diagram. |

Add files here and the root README `![Katha playthrough](docs/assets/demo.gif)` reference will resolve automatically.
