#!/usr/bin/env bash
# Run every tb/*/ suite of a processor checkout, at most N at a time, with the
# same per-suite command and tally rule as scripts/run_suites.sh.
# usage: run_suites_parallel.sh <repo> <logdir> [N]   (verilator taken from PATH)
set -uo pipefail
repo=$1; logs=$2; n=${3:-8}
mkdir -p "$logs"
cd "$repo" || exit 2
python3 scripts/check_upc_map.py > "$logs/check_upc_map.log" 2>&1 || { echo "FAIL check_upc_map"; exit 1; }
one() {
  d=$1; logs=$2; name=$(basename "$d")
  start=$(date +%s)
  (cd "$d" && make) > "$logs/$name.log" 2>&1; rc=$?
  end=$(date +%s)
  tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$logs/$name.log" | tail -1)
  echo "$name rc=$rc s=$((end-start)) ${tally:-NO-TALLY}"
}
export -f one
ls -d tb/*/ | while read -r d; do [ -f "$d/Makefile" ] && echo "$d"; done \
  | xargs -P "$n" -I{} bash -c 'one "$@"' _ {} "$logs" | sort > "$logs/SUMMARY.txt"
cat "$logs/SUMMARY.txt"
bad=$(grep -vc ' rc=0 .* [0-9]* checks: [0-9]* PASS, 0 FAIL$' "$logs/SUMMARY.txt")
tot=$(grep -Eo '[0-9]+ checks:' "$logs/SUMMARY.txt" | awk '{s+=$1} END{print s+0}')
echo "suites: $(wc -l < "$logs/SUMMARY.txt"), checks: $tot, not-clean: $bad"
[ "$bad" -eq 0 ]
