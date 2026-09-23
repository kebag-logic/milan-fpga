#!/usr/bin/env bash
# run_mutants.sh <leg> <tag-prefix> [--harness <abs path>] <mutant.sv>...
# Builds and runs each mutant datapath on one milan_dp leg, one at a time
# (the recipe's -j 8), with its own object directory. Writes one receipt per
# mutant to $OUT/logs/mutants/<tag-prefix>_<leg>__<mutant>.txt and prints its
# verdict: KILLED (build ok, at least one [FAIL]) or SURVIVED.
set -euo pipefail
: "${LANE:?}" "${OUT:?}" "${SCRATCH:?}"
leg=$1; prefix=$2; shift 2
harg=()
if [ "${1:-}" = "--harness" ]; then harg=(--harness "$2"); shift 2; fi
mkdir -p "$OUT/logs/mutants" "$SCRATCH/obj"
for m in "$@"; do
  name=$(basename "$m" .sv)
  tag="${prefix}_${leg}__${name}"
  log="$OUT/logs/mutants/$tag.txt"
  rm -rf "$SCRATCH/obj/$tag"
  python3 "$OUT/scripts/leg.py" "$LANE/tb/verilator/milan_dp" "$OUT/make-n-run.txt" \
      "$leg" "$log" --dp "$m" --mdir "$SCRATCH/obj/$tag" "${harg[@]}" >/dev/null || true
  nfail=$(grep -c '\[FAIL\]' "$log" || true)
  tally=$(grep -E 'checks: [0-9]+|[0-9]+ checks, [0-9]+ failures' "$log" | tail -1 || true)
  if ! grep -q '^build exit: 0$' "$log"; then v="BUILD-FAILED"
  elif [ "$nfail" -gt 0 ]; then v="KILLED"; else v="SURVIVED"; fi
  printf '%s\t%s\t%s\t%s\n' "$tag" "$v" "$nfail" "$tally" | tee -a "$OUT/logs/mutants/SUMMARY.tsv"
  rm -rf "$SCRATCH/obj/$tag"
done
