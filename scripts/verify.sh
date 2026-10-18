#!/usr/bin/env bash
# Verification loop for the explain-it-with-pictures repo.
# Runs every check a contributor or release needs; exits non-zero on failure.
# Browser-render and PDF checks are skipped (declared) when google-chrome
# is unavailable — everything else is dependency-free.
set -u
REPO="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
PORT=3471
FAILED=0
SKIPPED=0
step() { echo; echo "== $1 =="; }
fail() { echo "  $1"; FAILED=1; }

cleanup() {
  [ -n "${SERVER_PID:-}" ] && kill "$SERVER_PID" 2>/dev/null
  rm -rf "$TMP"
}
trap cleanup EXIT

step "1. Template SVG: well-formed + label geometry"
python3 "$REPO/scripts/check-svg.py" "$REPO/explain-it-with-pictures/templates/annotated-diagram.svg" || FAILED=1

step "2. Example explainer: balance, offline, SVGs, design system, fonts"
python3 "$REPO/scripts/verify-explainer.py" "$REPO/examples/recipe-saver-explainer.html" || FAILED=1

step "3. WCAG contrast: design-system color pairs"
python3 "$REPO/scripts/check-contrast.py" | tail -1 || FAILED=1

step "4. Demo app smoke test (isolated data file)"
cp "$REPO/examples/recipe-saver/recipes.json" "$TMP/recipes.json"
PORT=$PORT DATA_FILE="$TMP/recipes.json" node "$REPO/examples/recipe-saver/server.js" &
SERVER_PID=$!
base="http://localhost:$PORT"
READY=""
for _ in $(seq 1 50); do
  if [ "$(curl -s -o /dev/null -w '%{http_code}' "$base/api/recipes" 2>/dev/null)" = "200" ]; then READY=1; break; fi
  sleep 0.1
done
if [ -z "$READY" ]; then
  fail "server never became ready on port $PORT"
fi
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

if command -v google-chrome >/dev/null 2>&1; then
  step "5. Live render: explainer JS + reveal, app page"
  google-chrome --headless=new --no-sandbox --disable-gpu --virtual-time-budget=5000 \
    --dump-dom "file://$REPO/examples/recipe-saver-explainer.html" > "$TMP/explainer-dom.html" 2>/dev/null
  grep -q '<html lang="en" class="js"' "$TMP/explainer-dom.html" \
    && echo "  explainer: JS gate class applied" || fail "explainer: JS gate class missing — script did not run"
  INVIEW=$(grep -c 'class="[^"]*in-view' "$TMP/explainer-dom.html")
  [ "$INVIEW" -ge 1 ] && echo "  explainer: scroll-reveal fired ($INVIEW elements in-view)" \
    || fail "explainer: IntersectionObserver never fired"
  google-chrome --headless=new --no-sandbox --disable-gpu --virtual-time-budget=5000 \
    --dump-dom "$base/" > "$TMP/app-dom.html" 2>/dev/null
  grep -q 'id="recipe-form"' "$TMP/app-dom.html" \
    && echo "  app page: form rendered" || fail "app page: form missing from rendered DOM"

  step "6. Print test: explainer renders to a real PDF"
  google-chrome --headless=new --no-sandbox --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$REPO/assets/recipe-saver-explainer.pdf" \
    "file://$REPO/examples/recipe-saver-explainer.html" 2>/dev/null
  if [ -s "$REPO/assets/recipe-saver-explainer.pdf" ]; then
    PAGES=$(pdfinfo "$REPO/assets/recipe-saver-explainer.pdf" 2>/dev/null | sed -n 's/^Pages:\s*//p')
    echo "  PDF generated: ${PAGES:-?} pages"
    [ "${PAGES:-0}" -ge 4 ] || fail "PDF unexpectedly short ($PAGES pages) — print CSS may hide content"
  else
    fail "PDF was not generated"
  fi
else
  SKIPPED=1
  echo "  SKIPPED (declared): live render + PDF checks need google-chrome"
fi

kill "$SERVER_PID" 2>/dev/null
wait "$SERVER_PID" 2>/dev/null
SERVER_PID=""

step "7. Fixture untouched"
if python3 -c "
import json, sys
recipes = json.load(open('$REPO/examples/recipe-saver/recipes.json'))
assert len(recipes) == 2, f'expected 2 fixture recipes, found {len(recipes)}'
assert not any('Verify pancake' in r['title'] for r in recipes), 'smoke test leaked into the fixture'
"; then
  echo "  demo fixture clean"
else
  fail "demo fixture was modified by the smoke test"
fi

step "8. Result"
if [ "$FAILED" -eq 0 ]; then
  [ "$SKIPPED" -eq 1 ] && echo "ALL GREEN (with declared skips)" || echo "ALL GREEN"
else
  echo "RED — fix and re-run"
fi
exit "$FAILED"
