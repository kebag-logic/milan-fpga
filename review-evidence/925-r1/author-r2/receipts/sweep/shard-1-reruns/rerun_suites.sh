#!/usr/bin/env bash
# rerun_suites.sh <clone> <outdir> <suite:timeout_s[:jobs]>...: re-run sweep suites one at a time, uncontended by any other
# sweep in that tree, as run_all_suites.sh runs one (timeout make -C tb/verilator/<suite>, the log judged by
# scripts/suite_tally.py --verdict); prints one verdict line a suite and exits with the count that did not pass.
set -u
C=$1 O=$2; shift 2
mkdir -p "$O"; cd "$C" || exit 3
echo "head $(git rev-parse HEAD) porcelain $(git status --porcelain --untracked-files=no | wc -l) MAKEFLAGS=$MAKEFLAGS"
bad=0
for spec in "$@"; do
  IFS=: read -r s t j <<< "$spec"
  export MAKEFLAGS="-j${j:-4} --no-print-directory"
  start=$(date +%s)
  timeout "$t" make -C "$C/tb/verilator/$s" > "$O/$s.log" 2>&1; rc=$?
  v=$(python3 scripts/suite_tally.py --verdict "$O/$s.log" 2>&1); vrc=$?
  echo "$s make rc=$rc (timeout $t s, $MAKEFLAGS; 124 = the wall clock) verdict rc=$vrc: $v; $(( $(date +%s) - start )) s"
  [ $rc -ne 0 ] || [ $vrc -ne 0 ] && bad=$((bad + 1))
done
echo "RERUN DONE: $bad of $# did not pass"
exit $bad
