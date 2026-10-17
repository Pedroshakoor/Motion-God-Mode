#!/usr/bin/env bash
# Sync this local copy to the existing Motion-God-Mode repository.
# Requires gh and git, local git identity, and explicit invocation by owner.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
REPO="Pedroshakoor/Motion-God-Mode"
if ! command -v gh >/dev/null 2>&1; then echo 'Install GitHub CLI: https://cli.github.com/' >&2; exit 1; fi
if ! gh auth status >/dev/null 2>&1; then echo 'Run: gh auth login' >&2; exit 1; fi
LOGIN="$(gh api user --jq .login)"
if [[ "${LOGIN,,}" != "pedroshakoor" ]]; then echo "Refusing: signed in as $LOGIN" >&2; exit 1; fi
if ! gh repo view "$REPO" >/dev/null 2>&1; then echo "Repo $REPO does not exist" >&2; exit 1; fi
if [[ ! -d .git ]]; then git init -b main; fi
if git remote get-url origin >/dev/null 2>&1; then
  ORIGIN="$(git remote get-url origin)"
  if [[ "$ORIGIN" != "https://github.com/$REPO.git" && "$ORIGIN" != "git@github.com:$REPO.git" ]]; then
    echo "Refusing to modify unexpected origin $ORIGIN" >&2; exit 1
  fi
else
  git remote add origin "https://github.com/$REPO.git"
fi
git add .
if ! git diff --cached --quiet; then git commit -m 'Release Motion God Mode: cinematic agent skill'; fi
# Never force push: if someone else made changes, fetch and merge manually.
git push -u origin main
echo "Published https://github.com/$REPO"
