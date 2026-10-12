#!/usr/bin/env bash
# Verification loop for the explain-it-with-pictures repo.
# Runs every check a contributor or release needs; exits non-zero on failure.
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
PORT=3471
FAILED=0
step() { echo; echo "== $1 =="; }

cleanup() {
  [ -n "${SERVER_PID:-}" ] && kill "$SERVER_PID" 2>/dev/null
  rm -rf "$TMP"
}
trap cleanup EXIT

step "1. Template SVG: well-formed + label geometry"
python3 "$REPO/scripts/check-svg.py" "$REPO/explain-it-with-pictures/templates/annotated-diagram.svg" || FAILED=1

step "2. Example explainer: balanced, offline, SVGs valid + geometry"
python3 "$REPO/scripts/verify-explainer.py" "$REPO/examples/recipe-saver-explainer.html" || FAILED=1

step "3. Demo app smoke test (isolated data file)"
cp "$REPO/examples/recipe-saver/recipes.json" "$TMP/recipes.json"
PORT=$PORT DATA_FILE="$TMP/recipes.json" node "$REPO/examples/recipe-saver/server.js" &
SERVER_PID=$!
sleep 1
base="http://localhost:$PORT"
check() {
  local name="$1" expect="$2" got="$3"
  if [ "$got" = "$expect" ]; then
    echo "  $name -> $got"
  else
    echo "  $name -> got '$got', expected '$expect'"
    FAILED=1
  fi
}
check "GET / page"          200 "$(curl -s -o /dev/null -w '%{http_code}' "$base/")"
check "GET /public CSS"     200 "$(curl -s -o /dev/null -w '%{http_code}' "$base/public/style.css")"
check "GET /api/recipes"    200 "$(curl -s -o /dev/null -w '%{http_code}' "$base/api/recipes")"
check "GET search filtered" 200 "$(curl -s -o /dev/null -w '%{http_code}' "$base/api/recipes?q=chapati")"
check "POST valid recipe"   201 "$(curl -s -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: application/json' -d '{"title":"Verify pancake"}' "$base/api/recipes")"
check "POST missing title"  400 "$(curl -s -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: application/json' -d '{"ingredients":"no title"}' "$base/api/recipes")"
check "POST broken json"    400 "$(curl -s -o /dev/null -w '%{http_code}' -X POST -H 'Content-Type: application/json' -d 'not-json' "$base/api/recipes")"
check "path traversal"      404 "$(curl -s -o /dev/null -w '%{http_code}' --path-as-is "$base/public/../server.js")"
kill "$SERVER_PID" 2>/dev/null
wait "$SERVER_PID" 2>/dev/null
SERVER_PID=""

step "4. Fixture untouched"
if python3 -c "
import json, sys
recipes = json.load(open('$REPO/examples/recipe-saver/recipes.json'))
assert len(recipes) == 2, f'expected 2 fixture recipes, found {len(recipes)}'
assert not any('Verify pancake' in r['title'] for r in recipes), 'smoke test leaked into the fixture'
"; then
  echo "  demo fixture clean"
else
  echo "  demo fixture was modified by the smoke test"
  FAILED=1
fi

step "5. Result"
if [ "$FAILED" -eq 0 ]; then
  echo "ALL GREEN"
else
  echo "RED — fix and re-run"
fi
exit "$FAILED"
