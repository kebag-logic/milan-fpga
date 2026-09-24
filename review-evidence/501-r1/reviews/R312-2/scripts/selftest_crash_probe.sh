#!/bin/sh
# [R312] R312-2 probe: plant faults into the record-space gate's control
# table (scripts/check_nvm_record_space.py) and require --self-test to FAIL.
# Run from the repository root at the exact head. Each plant is transient:
# the file is restored from HEAD after every arm and verified clean.
#   crash_no_finding    a control raises before any finding (traceback, rc 1)
#   finding_then_crash  a control prints its named finding, then a traceback
#   unrelated_finding   a control yields a real FINDING, but not its named one
#   vacuous             a control does nothing (gate passes, rc 0)
#   r1_crash_no_finding the round-1 file (b5ee412) with crash_no_finding,
#                       showing the plant is one the previous rule accepted
set -u
F=scripts/check_nvm_record_space.py
restore() { git show HEAD:$F > $F; git diff --quiet -- $F || { echo "RESTORE FAILED"; exit 3; }; }
trap restore EXIT
plant() { # label source-rev python-edit
  git show "$2":$F > $F
  python3 - "$F" "$3" <<'PY' || { echo "$1: PLANT FAILED"; return; }
import sys; p, arm = sys.argv[1], sys.argv[2]; s = open(p).read()
defs = ("def _probe_crash():\n    raise RuntimeError('R312 crash probe')\n\n\n"
        "def _probe_late_crash():\n    _mut_old_output_length()\n"
        "    import atexit\n    atexit.register(lambda: 1 / 0)\n\n\n"
        "def _probe_nothing():\n    return None\n\n\n")
anchor = "MUTATIONS = {"
assert s.count(anchor) == 1
s = s.replace(anchor, defs + anchor)
edits = {
  "crash_no_finding": ('"collide": (_mut_collide,', '"collide": (_probe_crash,'),
  "finding_then_crash": ('"old_output_length": (_mut_old_output_length,',
                         '"old_output_length": (_probe_late_crash,'),
  "unrelated_finding": ('"block": (_mut_block,', '"block": (_mut_payload,'),
  "vacuous": ('"payload": (_mut_payload,', '"payload": (_probe_nothing,'),
  "r1_crash_no_finding": ('"collide": _mut_collide,', '"collide": _probe_crash,'),
}
old, new = edits[arm]
assert s.count(old) == 1, (arm, s.count(old))
open(p, "w").write(s.replace(old, new))
PY
  out=$(python3 $F --self-test 2>&1); rc=$?
  echo "== $1 (file from $2): --self-test rc=$rc"
  echo "$out" | grep -E '^SELF-TEST FAILED|^self-test OK: --mutate=(collide|old_output_length|block|payload) ' | cut -c1-260
  restore
}
plant crash_no_finding HEAD crash_no_finding
plant finding_then_crash HEAD finding_then_crash
plant unrelated_finding HEAD unrelated_finding
plant vacuous HEAD vacuous
plant r1_crash_no_finding b5ee412cdc0fd771d3df1f7fda49031409cf11fa r1_crash_no_finding
# the planted crash on its own, as a direct control run
git show HEAD:$F > $F
python3 - "$F" <<'PY'
import sys; p = sys.argv[1]; s = open(p).read()
s = s.replace("MUTATIONS = {", "def _probe_crash():\n    raise RuntimeError('R312 crash probe')\n\n\nMUTATIONS = {", 1)
open(p, "w").write(s.replace('"collide": (_mut_collide,', '"collide": (_probe_crash,', 1))
PY
python3 $F --mutate=collide --quiet > /dev/null 2>/tmp/r312_crash_err.$$; rc=$?
echo "== direct --mutate=collide with crash plant: rc=$rc traceback=$(grep -c 'Traceback (most recent call last)' /tmp/r312_crash_err.$$)"
rm -f /tmp/r312_crash_err.$$
restore
echo "restored: $(git hash-object $F) vs HEAD $(git rev-parse HEAD:$F)"
