#!/usr/bin/env bash
# Revert each round-4 checker change on its own in an archive copy and run the
# docs self-test. A change that its arms bind makes the self-test fail (rc 1).
# Usage: checker_mutants_r4.sh <clone> <scratch-dir> <out-file>
set -u
SRC=$(cd "$1" && pwd); WORK=$2; OUT=$3
mkdir -p "$WORK"
run() { # name python-old python-new
  local t="$WORK/m-$1"; rm -rf "$t"; mkdir -p "$t"
  git -C "$SRC" archive HEAD | tar -x -C "$t"
  python3 -I - "$t/scripts/check_docs.py" "$2" "$3" <<'PY'
import sys
path, old, new = sys.argv[1:]
text = open(path, encoding="utf-8").read()
assert text.count(old) == 1, (old, text.count(old))
open(path, "w", encoding="utf-8").write(text.replace(old, new))
PY
  local out rc; out=$(cd "$t" && python3 -I scripts/check_docs.py --selftest 2>&1); rc=$?
  printf '%-26s rc=%s | %s\n' "$1" "$rc" "$(printf '%s' "$out" | tail -1)"
  rm -rf "$t"
}
{
run unit_comma_only  'r"(?:,\s*|\s+|\()(ms|ns|ppm)\)?\s*$"' 'r",\s*(ms|ns|ppm)\s*$"' &
run unit_no_space    'r"(?:,\s*|\s+|\()(ms|ns|ppm)\)?\s*$"' 'r"(?:,\s*|\()(ms|ns|ppm)\)?\s*$"' &
run unit_no_paren    'r"(?:,\s*|\s+|\()(ms|ns|ppm)\)?\s*$"' 'r"(?:,\s*|\s+)(ms|ns|ppm)\s*$"' &
run no_tilde         'FENCE_MARKERS = ("```", "~~~")' 'FENCE_MARKERS = ("```",)' &
run any_marker_close 'fence in ("", marker)' 'True' &
run digit_no_lookbehind 'rf"(?<![\d.,])\b{minutes}' 'rf"\b{minutes}' &
run digit_space_required '{minutes}[\s-]?min' '{minutes}[\s-]min' &
run digit_no_trailing_b  'rf"(?<![\d.,])\b{minutes}[\s-]?min(?:ute)?s?\b"' 'rf"(?<![\d.,])\b{minutes}[\s-]?min"' &
run word_boundary    'rf"(?<![\w-]){word}' 'rf"\b{word}' &
run word_minutes_only '{word}[\s-]min(?:ute)?s?\b' '{word}[\s-]minutes?\b' &
run control          'FENCE_MARKERS = ' 'FENCE_MARKERS = ' &
wait
} | sort > "$OUT"
cat "$OUT"
