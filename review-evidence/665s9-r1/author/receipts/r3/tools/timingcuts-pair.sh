#!/usr/bin/env bash
# timingcuts-pair.sh: sw/litex/test_soc_timing_cuts.py at the base (1d6bf555) and at the head (ad2ed0e3), started
# together on clean clones under the same host load, with the LiteX venv's python; each log ends rc=N wall=Ns
set -uo pipefail
S=<scratch>; G=$S/gates
export HOME=$S/home TMPDIR=$S/tmp PYTHONHASHSEED=0 PATH=<home>/litex-milan/venv/bin:/usr/local/bin:/usr/bin:/bin
one() { local name=$1 dir=$2; local t0=$(date +%s)
  (cd "$dir/sw/litex" && python3 -B test_soc_timing_cuts.py) > "$G/$name.log" 2>&1; local rc=$?
  echo "rc=$rc wall=$(( $(date +%s) - t0 ))s" >> "$G/$name.log"; echo "$(date +%T) $name $(tail -n 1 "$G/$name.log")" >> $S/gates-run.log; }
one timingcuts-pair-base $G/timingcuts-base & one timingcuts-pair-head $G/timingcuts & wait
