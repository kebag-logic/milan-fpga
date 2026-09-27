#!/usr/bin/env bash
# R346-4 disposable probes. Usage: probes.sh <candidate-clone> <python> <scratch-dir> <receipt-dir>
# Works only in a throwaway local clone under <scratch-dir>; the candidate clone is read-only here.
set -u
SRC=${1:?candidate clone}
PY=${2:?python}
SCR=${3:?scratch}
OUT=${4:?receipts}
HEAD_EXPECT=10a5bf59a6a73e9b6487d9ea6f42669ce142ae25
SOURCE_HEAD=07f72ad640f99c43bc1354642ad4d7ed8ba410cc
mkdir -p "$OUT"
: >"$OUT/SUMMARY.txt"
rm -rf "$SCR/probe"
git clone -q --no-checkout "$SRC" "$SCR/probe" || exit 2
cd "$SCR/probe" || exit 2
git checkout -q --detach "$HEAD_EXPECT" || exit 2
note() { printf '%s\n' "$*" | tee -a "$OUT/SUMMARY.txt"; }
reset_tree() { git checkout -q -- . && git clean -qfdx; }

# Doc anchor probes: each rename must be caught by at least one docs gate.
anchor_probe() {
  label=$1 file=$2 old=$3 new=$4
  reset_tree
  "$PY" - "$file" "$old" "$new" <<'EOF'
import sys
p, old, new = sys.argv[1:]
t = open(p, encoding="utf-8").read()
assert t.count(old) == 1, (p, old, t.count(old))
open(p, "w", encoding="utf-8").write(t.replace(old, new))
EOF
  "$PY" -B scripts/docs_check.py >"$OUT/$label.docs_check.log" 2>&1; a=$?
  "$PY" -B scripts/gen_toc.py --verify-anchors >"$OUT/$label.verify_anchors.log" 2>&1; b=$?
  "$PY" -B scripts/gen_toc.py --check >"$OUT/$label.toc_check.log" 2>&1; c=$?
  if [ $a -ne 0 ] || [ $b -ne 0 ] || [ $c -ne 0 ]; then v=CAUGHT; else v=MISSED; fi
  note "$label $v docs_check=$a verify_anchors=$b toc_check=$c"
}
anchor_probe A1_6d_heading docs/testing/TESTING.md "## 6d. Unattended campaign vehicle" "## 6d. Unattended campaign vehicles"
anchor_probe A2_6b_heading docs/testing/TESTING.md "## 6b. Bench evidence retention" "## 6b. Bench evidence retentions"
anchor_probe A3_req8_heading REQUIREMENTS.md "## 8. Verification and release acceptance" "## 8. Verification and release acceptances"

# Independent oracle mutants on check_release_tu; the planner self-test must fail.
oracle_probe() {
  label=$1 old=$2 new=$3
  reset_tree
  "$PY" - tb/tools/torture_campaign.py "$old" "$new" <<'EOF'
import sys
p, old, new = sys.argv[1:]
t = open(p, encoding="utf-8").read()
assert t.count(old) == 1, (old, t.count(old))
open(p, "w", encoding="utf-8").write(t.replace(old, new))
EOF
  "$PY" -B tb/tools/torture_campaign.py --self-test >"$OUT/$label.selftest.log" 2>&1; a=$?
  "$PY" -B -m behave tests/features/torture_campaign_plan.feature -f plain >"$OUT/$label.behave.log" 2>&1; b=$?
  if [ $a -ne 0 ]; then v=KILLED; else v=SURVIVED; fi
  note "$label $v selftest=$a behave=$b"
}
oracle_probe M1_complete_capture_ignored "if (capture_complete is not True or len(interval_s) != 2" "if (len(interval_s) != 2"
oracle_probe M2_clear_deadline_strict "\"PASS\" if clear_s <= deadline_s else \"FAIL\"" "\"PASS\" if clear_s < deadline_s else \"FAIL\""
oracle_probe M3_nonfinite_accepted "type(value) not in (int, float) or not math.isfinite(value) for value in values" "type(value) not in (int, float) for value in values"
oracle_probe M4_bool_resolution_accepted "type(value) not in (int, float) or not math.isfinite(value)" "not isinstance(value, (int, float)) or not math.isfinite(value)"

# Source head versus candidate: the planner and plan feature give the same result.
reset_tree
for rev in "$SOURCE_HEAD" "$HEAD_EXPECT"; do
  git checkout -q --detach "$rev" || exit 2
  "$PY" -B tb/tools/torture_campaign.py --self-test >"$OUT/cmp_$rev.selftest.log" 2>&1; a=$?
  "$PY" -B -m behave tests/features/torture_campaign_plan.feature -f plain >"$OUT/cmp_$rev.behave.log" 2>&1; b=$?
  "$PY" -B tb/tools/torture_campaign.py --plan --areas soak,power --json >"$OUT/cmp_$rev.plan.json" 2>&1; c=$?
  note "compare $rev selftest=$a behave=$b plan=$c tests=$(grep -o 'Ran [0-9]* tests' "$OUT/cmp_$rev.selftest.log") scenarios=$(grep 'scenarios passed' "$OUT/cmp_$rev.behave.log")"
done
if cmp -s "$OUT/cmp_$SOURCE_HEAD.plan.json" "$OUT/cmp_$HEAD_EXPECT.plan.json"; then note "default plan JSON identical"; else note "default plan JSON DIFFERS"; fi
for f in tb/tools/torture_campaign.py tb/tools/torture_release_mutants.py tests/features/torture_campaign_plan.feature \
         tests/steps/torture_plan_steps.py tests/steps/torture_release_steps.py REQUIREMENTS.md CONTRIBUTING.md; do
  if [ "$(git rev-parse "$SOURCE_HEAD:$f")" = "$(git rev-parse "$HEAD_EXPECT:$f")" ]; then note "blob identical $f"; else note "blob DIFFERS $f"; fi
done
