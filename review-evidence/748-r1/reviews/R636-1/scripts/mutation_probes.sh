#!/usr/bin/env bash
# Reviewer mutation probes on disposable copies of the head.
# Usage: mutation_probes.sh <repo clone at head> <packet dir> <venv python> <CPython prefix>
# Each probe: copy the head into scratch, apply one edit to the TEMPLATE, regenerate
# (scripts/ci_gate_workflows.py), commit in the copy, and record what the contract
# (scripts/ci_events.py --check) and, for M1, the native control say.
set -u
REPO="$1"; P="$2"; VPY="$3"; PLANT="$4"
R="$P/receipts/mutations"; S="$P/scratch/mut"
mkdir -p "$R" "$S"
TPL=.github/ci-templates/elaborate.yml
probe_copy() {  # name -> path of a fresh clone of the head
  local d="$S/$1"
  rm -rf "$d"; git clone -q --no-hardlinks "$REPO" "$d"
  git -C "$d" checkout -q --detach c48bfe38b25f002d24898cec265520b9fc1a7111
  echo "$d"
}
finish() {  # dir name: regenerate, commit, contract check
  local d="$1" name="$2"
  ( cd "$d" && "$VPY" scripts/ci_gate_workflows.py > "$R/$name.regen.log" 2>&1; echo "regen rc $?" >> "$R/$name.summary"
    git -c user.name=probe -c user.email=probe@invalid commit -qam "probe $name"
    git diff --stat HEAD~1 HEAD >> "$R/$name.summary"
    "$VPY" scripts/ci_events.py --check > "$R/$name.events.log" 2>&1; echo "events --check rc $?" >> "$R/$name.summary" )
}
# M1: the private step moved after the LiteX install (a partial fix).
m1() {
  local d; d="$(probe_copy M1)"
  "$VPY" - "$d/$TPL" <<'PY'
import sys
p = sys.argv[1]; t = open(p).read()
start = t.index("      # EVERY LATER STEP INSTALLS")
end = t.index("      # LiteX ships from git")
block = t[start:end]; t = t[:start] + t[end:]
anchor = t.index("      # The VexiiRiscv wrapper turns")
t = t[:anchor] + block + t[anchor:]
open(p, "w").write(t)
PY
  finish "$d" M1
  ( cd "$d" && "$VPY" scripts/ci_toolcache_isolation.py --python "$PLANT" --work "$S/M1-control" \
      --report "$R/M1.control.json" > "$R/M1.control.log" 2>&1; echo "control rc $?" >> "$R/M1.summary" )
}
# M2: venv placed in a path inside the tool cache's interpreter (not job-private).
m2() {
  local d; d="$(probe_copy M2)"
  sed -i 's#"\$RUNNER_TEMP/litex-venv#"$(dirname "$(dirname "$(command -v python3)")")/litex-venv#g' "$d/$TPL"
  finish "$d" M2
}
# M3: the step's if: dropped (runs on documentation-only heads too).
m3() {
  local d; d="$(probe_copy M3)"
  "$VPY" - "$d/$TPL" <<'PY'
import sys
p = sys.argv[1]; t = open(p).read()
old = "      - name: Put a job-private Python environment on PATH\n        if: ${{ steps.scope.outputs.rtl == 'true' }}\n"
assert old in t
t = t.replace(old, "      - name: Put a job-private Python environment on PATH\n")
open(p, "w").write(t)
PY
  finish "$d" M3
}
# M4: template edited but the workflow NOT regenerated (generator drift check).
m4() {
  local d; d="$(probe_copy M4)"
  sed -i 's#litex-venv#litex-venv2#g' "$d/$TPL"
  ( cd "$d" && "$VPY" scripts/ci_gate_workflows.py --check > "$R/M4.genchk.log" 2>&1; echo "gate_workflows --check rc $?" >> "$R/M4.summary" )
}
m1 & m2 & m3 & m4 &
wait
for f in "$R"/*.summary; do echo "== $(basename "$f")"; cat "$f"; done
