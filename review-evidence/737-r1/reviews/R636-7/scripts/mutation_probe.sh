#!/usr/bin/env bash
# R636-7 disposable mutation probes for the round-7 S1/S2 self-test additions.
# Usage: mutation_probe.sh <source-clone> <scratch-dir> <receipt-dir>
# Each mutation is applied to a fresh export of HEAD, the workflows are
# regenerated (so the generator's --check passes under the mutation), and the
# gate self-test is run. A surviving mutation (self-test rc 0) is a gap.
set -u
SRC=$1; SCRATCH=$2; OUT=$3
mkdir -p "$SCRATCH" "$OUT"
fresh() {
  rm -rf "$SCRATCH/$1"; mkdir -p "$SCRATCH/$1"
  # Copy the clean working tree with initialized submodules, with Git metadata (the source-list helpers read it).
  rsync -a "$SRC"/ "$SCRATCH/$1"/
}
run_case() {
  local id=$1 file=$2 old=$3 new=$4
  fresh "$id"
  local d="$SCRATCH/$id"
  if [ -n "$file" ]; then
    python3 -I - "$d/$file" "$old" "$new" <<'EOF'
import sys
p, old, new = sys.argv[1:]
s = open(p, encoding="utf-8").read()
assert s.count(old) == 1, ("anchor count", s.count(old))
open(p, "w", encoding="utf-8").write(s.replace(old, new))
EOF
  fi
  ( cd "$d" && python3 scripts/ci_gate_workflows.py ) > "$OUT/$id-generate.log" 2>&1
  echo "generate rc=$?" >> "$OUT/$id-generate.log"
  ( cd "$d" && python3 scripts/ci_gate_workflows.py --check ) > "$OUT/$id-check.log" 2>&1
  echo "check rc=$?" >> "$OUT/$id-check.log"
  ( cd "$d" && python3 scripts/ci_gate_workflows_selftest.py ) > "$OUT/$id-selftest.log" 2>&1
  local rc=$?
  echo "selftest rc=$rc" >> "$OUT/$id-selftest.log"
  echo "$id selftest_rc=$rc $(tail -1 "$OUT/$id-check.log")"
}
run_case m0-pristine "" "" ""
run_case m1-receipts-elaborate-only scripts/ci_gate_workflows.py \
  '    if leg in BUILDER_WORKERS[name]:' '    if name == "elaborate":'
run_case m2-receipts-every-worker scripts/ci_gate_workflows.py \
  '    if leg in BUILDER_WORKERS[name]:' '    if True:'
run_case m3-prep-line-refusal-removed scripts/ci_gate_workflows.py \
  '            or any("sw/builder/test_builder.py" in line for line in preparation)):' '            or False):'
run_case m4-last-line-refusal-removed scripts/ci_gate_workflows.py \
  '    if (not command.startswith(DRIVER_COMMAND + " ")' '    if (False'
run_case m5-receipts-drop-last-builder-worker scripts/ci_gate_workflows.py \
  '    if leg in BUILDER_WORKERS[name]:' '    if leg in BUILDER_WORKERS[name][:-1]:'
