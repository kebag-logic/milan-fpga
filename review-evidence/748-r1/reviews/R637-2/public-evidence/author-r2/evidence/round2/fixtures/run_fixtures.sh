#!/bin/bash
# Round-2 fixtures for the tool-cache isolation control, all through its CLI.
# Usage: run_fixtures.sh <head sha> <out dir>
# Each case runs in its own empty directory and writes <case>.log, .rc, .json.
set -uo pipefail
H=$1; OUT=$2
LANE=$LANES/748-elab-race
PY=$VALIDATION_STORAGE/748-a623/gatevenv/bin/python3
PLANT=$VALIDATION_TOOLS/uvpy/cpython-3.12.3-linux-x86_64-gnu
PIPC=$VALIDATION_STORAGE/748-a623/pipwarm/home/.cache/pip
FX=$VALIDATION_STORAGE/748-a623/r2/fx
mkdir -p "$OUT"

# A disposable clone at $H whose generated workflow has the patch step's
# script replaced by $2 in both legs, committed so the control reads it.
mutant() {
  local name=$1 script=$2 repo="$FX/$1/repo"
  git clone -q "$LANE" "$repo" && git -C "$repo" checkout -q --detach "$H" || return 1
  "$PY" -I - "$repo/.github/workflows/elaborate.yml" "$script" <<'PYEOF' || return 1
import sys
from pathlib import Path
path, script = Path(sys.argv[1]), sys.argv[2]
old = "        run: sw/litex/patches/apply.sh\n"
text = path.read_text()
assert text.count(old) == 2, text.count(old)
path.write_text(text.replace(old, f"        run: {script}\n"))
PYEOF
  git -C "$repo" commit -q -am "fixture: $name" || return 1
}

# case <name> <cwd> <control script> <args...>
case_run() {
  local name=$1 dir=$2 script=$3; shift 3
  mkdir -p "$dir"
  local began=$(date +%s)
  (cd "$dir" && "$PY" -I "$script" --python "$PLANT" --pip-cache "$PIPC" \
     --report "$OUT/$name.json" "$@") > "$OUT/$name.log" 2>&1
  echo $? > "$OUT/$name.rc"
  echo "$name rc $(cat "$OUT/$name.rc") in $(( $(date +%s) - began )) s" >> "$OUT/summary.txt"
  # Keep the patch-check sections, then free the run tree (scratch space and page cache).
  for leg in 0 1; do
    sed -n '/===== gate 23h/,$p' "$dir/run/elaborate-gates-$leg/steps.log" | cut -c1-400 | head -n 40 \
      > "$OUT/$name-leg$leg-gate23h.txt"
  done
  if [ -d "$dir/repo" ]; then
    git -C "$dir/repo" diff HEAD~1 HEAD > "$OUT/$name-mutation.diff"
    git -C "$dir/repo" rev-parse HEAD~1 > "$OUT/$name-mutation.base"
  fi
  rm -rf "$dir/run" "$dir/repo"
}

: > "$OUT/summary.txt"
# F02: the same complete run with a relative and an absolute --work.
case_run head-relative "$FX/head-relative" "$LANE/scripts/ci_toolcache_isolation.py" --work run --rev "$H"
case_run head-absolute "$FX/head-absolute" "$LANE/scripts/ci_toolcache_isolation.py" --work "$FX/head-absolute/run" --rev "$H"
# F01: a missing dependency on patched trees; the same unpatched (the review's
# probe shape); an available but unpatched interpreter.
mutant missing-dep 'sw/litex/patches/apply.sh && python3 -m pip uninstall --quiet --yes litex-boards' &&
  case_run missing-dep "$FX/missing-dep" "$FX/missing-dep/repo/scripts/ci_toolcache_isolation.py" --work run
mutant missing-dep-unpatched 'python3 -m pip uninstall --quiet --yes litex-boards' &&
  case_run missing-dep-unpatched "$FX/missing-dep-unpatched" "$FX/missing-dep-unpatched/repo/scripts/ci_toolcache_isolation.py" --work run
mutant unpatched 'echo the patch series is withheld' &&
  case_run unpatched "$FX/unpatched" "$FX/unpatched/repo/scripts/ci_toolcache_isolation.py" --work run
# The shared-cache negative controls, kept.
case_run shared-4 "$FX/shared-4" "$LANE/scripts/ci_toolcache_isolation.py" --work run --rev "$H" --shared
case_run dev-race-3 "$FX/dev-race-3" "$LANE/scripts/ci_toolcache_isolation.py" --work run --rev 9ef717727e6fdac11ee7f01672fefae948452343
echo done > "$OUT/done"
