#!/usr/bin/env bash
# Mutation probes of record_classes.py's GET_AS_PATH guard: each mutant is applied to a disposable
# archive of the head, record_classes.py --selftest is run, and the exit is recorded (1 = caught).
# usage: probe_record_classes.sh CLONE OUTDIR SCRATCHDIR (the archive goes to SCRATCHDIR/probe)
set -u
clone=$1; out=$2; scratch=$3; mkdir -p "$out"
probe=$scratch/probe; rm -rf "$probe"; mkdir -p "$probe"
git -C "$clone" archive HEAD | tar -x -C "$probe"
rc=tb/verilator/ctrl_service_budget/record_classes.py
cp "$probe/$rc" "$probe/$rc.orig"
run() { # name python-replacement-expression
  cp "$probe/$rc.orig" "$probe/$rc"
  python3 -I - "$probe/$rc" "$2" "$3" <<'PY'
import sys
p, old, new = sys.argv[1:]
s = open(p).read()
assert s.count(old) == 1, ('anchor', old)
open(p, 'w').write(s.replace(old, new))
PY
  ( cd "$probe" && python3 -I "$rc" --selftest ) > "$out/mut-$1.log" 2>&1; echo "$1 rc=$?" | tee -a "$out/mutants.txt"
}
: > "$out/mutants.txt"
( cd "$probe" && python3 -I "$rc" --selftest ) > "$out/mut-none.log" 2>&1; echo "none rc=$?" | tee -a "$out/mutants.txt"
run M1-no-length-in-answered "r.status == 0 and r.length == ANSWERED_LENGTH" "r.status == 0"
run M2-no-per-leg-loop "        if leg.variant == 'answering-ports':" "        if False:"
run M3-missing-check-status-only "leg.groups.get('aecp', []) if answered_path(r)]" "leg.groups.get('aecp', []) if r.command == GET_AS_PATH and r.status == 0]"
run M4-answered-length-16 "ANSWERED_LENGTH = 16 + 8 * arm_path.ENTRIES" "ANSWERED_LENGTH = 16"
run M5-decode-wrong-byte "(fr[16] << 8 | fr[17]) & 0x7FF)" "(fr[16] << 8 | fr[18]) & 0x7FF)"
run M6-no-wiring-check "    if not any('image_face.ports.path=b_path;' in new for new in patches):" "    if False:"
run M7-loop-only-at-1x1 "        if leg.variant == 'answering-ports':" "        if leg.variant == 'answering-ports' and leg.point == '1x1/1if':"
cp "$probe/$rc.orig" "$probe/$rc"
