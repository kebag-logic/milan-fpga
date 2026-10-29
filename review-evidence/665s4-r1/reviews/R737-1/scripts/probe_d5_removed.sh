#!/bin/sh
# Reviewer probe: D5 on the current flash writer is still gated.
# Usage: probe_d5_removed.sh COPY OUTDIR
# COPY is a disposable export of the head (git archive plus submodule trees).
# Runs scripts/check_nvm_capture.py unplanted (must exit 0), then with the
# 24.5 ms check deleted from tb/verilator/nvm_capture_cpu/run.py grade_rows
# (must exit nonzero), then restores the file and checks its digest.
set -u
copy=$1; out=$2
f=$copy/tb/verilator/nvm_capture_cpu/run.py
orig=$(sha256sum "$f" | cut -c1-64)
(cd "$copy" && python3 -B scripts/check_nvm_capture.py) > "$out/d5_unplanted.log" 2>&1; echo $? > "$out/d5_unplanted.rc"
cp "$f" "$f.orig"
python3 - "$f" <<'EOF'
import sys
p = sys.argv[1]
t = open(p).read()
check = ("        if (spec.get('mutation', 'none') == 'none'\n"
         "                and row['sys_cycles'] * 2000 > HOLD_FLOOR_MS * spec['sys_hz']):\n"
         "            raise RuntimeError('worst measured copy exceeds half the 49 ms hold floor')\n")
assert t.count(check) == 1, t.count(check)
open(p, 'w').write(t.replace(check, ''))
EOF
(cd "$copy" && python3 -B scripts/check_nvm_capture.py) > "$out/d5_planted.log" 2>&1; echo $? > "$out/d5_planted.rc"
mv "$f.orig" "$f"
now=$(sha256sum "$f" | cut -c1-64)
echo "restored: $([ "$orig" = "$now" ] && echo yes || echo NO) $now" > "$out/d5_restore.txt"
echo "unplanted rc=$(cat "$out/d5_unplanted.rc") planted rc=$(cat "$out/d5_planted.rc")"
