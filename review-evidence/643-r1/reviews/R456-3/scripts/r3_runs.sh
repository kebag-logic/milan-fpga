#!/bin/bash
# R456-3 probe RUNS for #643 / PR #648 at 36207e91. Usage: r3_runs.sh PACKET BATCH
# Same mechanism as r2_runs.sh (R456-1's unchanged run_probe.py, at most JOBS at
# once). B5 holds round 2's ad hoc runs of its NEW builds (crfhist, crfw1104),
# under the names round 2's receipts used, plus the R456-3 additions marked NEW.
set -u
P=$1; BATCH=$2; S=$P/scratch; R=$P/receipts/probes; mkdir -p $R
D="$P/scripts/r1-unchanged/run_probe.py"
case $BATCH in
B5) cat <<EOF ;;
hp2 crfhist full hp-crfhist-full
c4b crfhist full c4-crfhist-full
hp2 crfw1104 --crf-only hp-crfw1104-crf
hp clean --crf-only hp-clean-crf
pc4c clean --crf-only c4-clean-crf
hp clean --law-boundary=975..995 hp-clean-lb-975up
pc4c clean --law-boundary=975..995 c4-clean-lb-975up
EOF
esac > $R/batch-$BATCH.txt
# NEW (R456-3): hp-/c4-clean-crf, the CRF window under --crf-only on the clean
# build (its walk and clearance where the window sits elsewhere against the
# grid); hp-/c4-clean-lb-975up, phases half a tick from the boundary, where the
# nearest pop changes side, so the new walk_wraps() branch is exercised.
echo "== batch $BATCH start $(date +%T)"
xargs -P ${JOBS:-16} -L 1 sh -c 'python3 "$0" run "'$S'/$1" "$2" --mode="$3" --log "'$R'/$4.log"; echo "  done $4 $(cat "'$R'/$4.log.rc")"' $D < $R/batch-$BATCH.txt
echo "== batch $BATCH done $(date +%T)"
