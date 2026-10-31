#!/usr/bin/env bash
# #787 round 4: the default sweep's milan_dp suites at <rev> in a clean clone, each as scripts/run_all_suites.sh
# runs one suite (`timeout <its budget> make -C tb/verilator/<suite>`, the log judged by scripts/suite_tally.py
# --verdict), then the tally over the logs. The suites of one chain run one at a time; MAKEFLAGS=-j4.
# usage: dp_suites.sh <rev> <chain-name> <suite>...
set -u
rev=$1; chain=$2; shift 2
X=$VALIDATION_STORAGE/787-a700e; C=$X/clone-dp-$chain-${rev:0:8}; O=$X/r/dp-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O/logs"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone-$chain.log" 2>&1 || exit 2
cd "$C" || exit 2
source "$D/env.sh"
export TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/a662/tsn-gen MAKEFLAGS=-j4
git rev-parse HEAD > "$O/head-$chain.txt"
for s in "$@"; do
  case "$s" in
    milan_dp) tmo=4800 ;; milan_dp_mclk) tmo=3600 ;; *) tmo=1800 ;;
  esac
  st=$(date +%s)
  timeout "$tmo" make -C "tb/verilator/$s" > "$O/logs/$s.log" 2>&1; rc=$?
  python3 scripts/suite_tally.py --verdict "$O/logs/$s.log" > "$O/logs/$s.verdict" 2>&1; vrc=$?
  echo "$rc $vrc $(( $(date +%s)-st ))s $s (make rc, verdict rc, seconds; budget ${tmo}s)" >> "$O/table-$chain.txt"
done
git status --porcelain --untracked-files=no > "$O/clone-status-after-$chain.txt"
echo "DP-DONE $chain" >> "$O/table-$chain.txt"
