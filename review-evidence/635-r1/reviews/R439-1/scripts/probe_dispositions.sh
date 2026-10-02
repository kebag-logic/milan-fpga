#!/bin/bash
# Remove each new DUT-reader disposition in turn, run the test-evidence ratchet,
# restore. Usage: probe_dispositions.sh <clone> <outdir>
set -u
C=$1; O=$2; cd "$C"; F=scripts/measure_test_evidence.py
for which in acmp notify; do
python3 - "$F" "$which" <<'PY'
import sys
p, w = sys.argv[1:3]; s = open(p).read()
key = f'    "protocol-processor/tb/pp_top/{w}_mutants.py":\n'
i = s.index(key); j = s.index('    "protocol-processor/tb/pp_top/', i + len(key))
open(p, 'w').write(s[:i] + s[j:])
PY
python3 "$F" --check > "$O/P_${which}_disposition_removed.log" 2>&1
echo "P_${which}_disposition_removed test_evidence rc=$?" >> "$O/summary.txt"
git checkout -q -- "$F"
done
git diff --quiet && echo "restored clean (dispositions)" >> "$O/summary.txt"
