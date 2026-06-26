# Contributing to Katha

Welcome. This document covers how to get the backend running, how to run the test gates, and the conventions that keep the codebase solid.

---

## Running the backend

The core engine runs on the Python standard library alone — no installation required.

```bash
cd backend

# Start the zero-dependency terminal demo
python -m app.demo

# Or launch the interactive visual novel in your browser
python -m app.webserver
# Open http://127.0.0.1:8000
```

For the production HTTP layer (FastAPI, LangGraph, ChromaDB, voice), install the full requirements:

```bash
cd backend
pip install -r requirements.txt
```

---

## Running the test gates

Three commands must pass before any push. Run them all from the `backend/` directory:

```bash
cd backend

# 1. Core engine + knowledge-isolation self-tests (33 checks)
python -m app.selftest

# 2. pytest suite
python -m pytest -q

# 3. Knowledge-leak eval (must print "0 leaks" and exit 0)
python -m app.eval_leak
```

All three are the CI hard gates. A PR with any of these failing will not be merged.

---

## Code style: ruff and mypy

Linting and type checking are configured in `pyproject.toml` at the repo root.

```bash
# From the repo root
ruff check backend

# From the backend/ directory
mypy app --config-file ../pyproject.toml
```

Both must exit 0. The ruff config selects `E`, `F`, and `I` rules at Python 3.12 target; a small set of rules that would require reformatting existing content strings are suppressed. mypy runs with `ignore_missing_imports = true` and `disallow_untyped_defs = false` to accommodate the duck-typed provider and knowledge-engine interfaces.

---

## Key conventions

### Keep the self-test green

Always run `python -m app.selftest` before pushing. It guarantees the core game engine, state validation, and RAG leakage protection are all functional.

### Offline-first principle

Any external service failure — LLM provider down, voice provider unavailable, vector store error — must be caught and must fall back to the offline mock/lexical versions so the game remains fully playable with no API keys. This is non-negotiable: the mock path must always work.

### No hardcoded secrets

Never check in keys or `.env` files. All secrets are read from environment variables exclusively through `backend/app/config.py`. Copy `backend/.env.example` to `backend/.env` to configure local overrides; the `.env` file is in `.gitignore` and must never be committed.

### Branching strategy

- Work on feature branches (`feature/your-feature-name`).
- Open a Pull Request to `main` for code review.
- Squash-merge once CI is green and at least one reviewer has approved.

### Cultural sensitivity

Katha handles sacred Indian narratives. Any content touching Mahabharata characters, religious rites, or mythology must be reviewed against the source-text citations in `docs/04-cultural-fidelity.md` and `docs/11-phase1-content-tales-and-betaal.md`. When in doubt, stay closer to the source text and flag for advisory review.