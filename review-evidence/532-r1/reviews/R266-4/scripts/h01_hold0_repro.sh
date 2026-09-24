#!/usr/bin/env bash
# h01_hold0_repro.sh PROOF OUTDIR RUNS JOBS [ONLY_LATE]: the diagnostic behind
# receipts/hold-sensitivity-022290e4.txt sections D and E. Builds mutant H01 of PROOF
# with proof_mutants.py, keeps each self-test's scratch (its `rm -rf "$scratch"` is
# replaced by an echo of the path), optionally keeps only the late-refusal case,
# and runs it RUNS times, JOBS at a time, as namespace uid 0 with FAKE_HOLD=0.
# Prints each run's rc and, for a surviving run, the late-refusal case's SUMMARY.
# Diagnostic only: the shipped self-test always uses the stand-in's 3 s default.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
proof=$1 outdir=$2 runs=$3 jobs=$4 only_late=${5:-}
mkdir -p "$outdir/tmp"
python3 "$here/proof_mutants.py" "$proof" "$outdir" H01 >/dev/null
python3 - "$outdir/H01/act_slot_proof.sh" "$outdir/h01.sh" "$only_late" <<'EOF'
import sys
source, target, only_late = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(source).read()
assert s.count('  rm -rf "$scratch"\n') == 1
s = s.replace('  rm -rf "$scratch"\n', '  echo "scratch $scratch"\n')
if only_late:
    start = s.index("done <<'EOF'\n") + len("done <<'EOF'\n")
    end = s.index("EOF\n", start)
    rows = [r for r in s[start:end].splitlines()
            if r.startswith("the rival is refused only after the holder left|")]
    assert len(rows) == 1
    s = s[:start] + rows[0] + "\n" + s[end:]
open(target, "w").write(s)
EOF
seq 1 "$runs" | FAKE_HOLD=0 xargs -P "$jobs" -I{} sh -c \
  "TMPDIR='$outdir/tmp' '$here/sandbox.sh' uid0 bash '$outdir/h01.sh' --selftest >'$outdir/run{}.txt' 2>&1; echo \"run {} rc=\$?\"" \
  | sort -V
for result in "$outdir"/run*.txt; do
  if grep -q 'act_slot_proof selftest: PASS' "$result"; then
    scratch=$(sed -n 's/^scratch //p' "$result")
    echo "SURVIVED $result; late-refusal SUMMARY:"
    sed 's/^/  | /' "$scratch/the rival is refused only after the holder left/logs/SUMMARY"
  fi
done
