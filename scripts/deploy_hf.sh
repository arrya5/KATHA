#!/usr/bin/env bash
# Deploy the current committed code to the Hugging Face Space (arrya5/katha),
# IN PLACE — the live URL stays https://arrya5-katha.hf.space/ .
#
# What it does:
#   * Clones the Space repo (separate from GitHub) to a temp dir.
#   * Overlays ONLY the app code from this repo's HEAD: backend/, Dockerfile,
#     requirements-demo.txt  (via `git archive`, so untracked files like .env are
#     NEVER included — the Space repo is public).
#   * Leaves the Space's own README.md untouched (it holds the HF `sdk: docker`
#     / app_port config), then commits & pushes so the Space rebuilds.
#
# Auth: reads HF_TOKEN from backend/.env (gitignored). This script holds no secret,
# so it is safe to commit.
#
# Usage:  bash scripts/deploy_hf.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SPACE="arrya5/katha"
HF_USER="arrya5"

HF_TOKEN="$(grep -E '^HF_TOKEN=' "$REPO_ROOT/backend/.env" 2>/dev/null | head -1 | cut -d= -f2- || true)"
if [ -z "${HF_TOKEN:-}" ]; then
  echo "ERROR: HF_TOKEN not found in backend/.env" >&2
  exit 1
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo ">> Cloning Space $SPACE ..."
git clone --quiet "https://${HF_USER}:${HF_TOKEN}@huggingface.co/spaces/${SPACE}" "$TMP"

echo ">> Syncing app code from local HEAD ..."
rm -rf "$TMP/backend"
git -C "$REPO_ROOT" archive HEAD backend Dockerfile requirements-demo.txt | tar -x -C "$TMP"

cd "$TMP"
git add -A
if git diff --cached --quiet; then
  echo ">> No changes — Space already matches local HEAD."
  exit 0
fi
REV="$(git -C "$REPO_ROOT" rev-parse --short HEAD)"
git -c user.email="deploy@katha.local" -c user.name="Katha Deploy" \
    commit --quiet -m "Deploy from GitHub main @ ${REV}"
git push --quiet origin HEAD:main
echo ">> Deployed @ ${REV}. Space is rebuilding -> https://arrya5-katha.hf.space/"
