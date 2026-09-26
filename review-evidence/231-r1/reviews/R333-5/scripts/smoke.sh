#!/bin/sh
# Re-run the three fast-CI baseline self-tests at the checked-out head (run from the clone root).
set -u
for c in "syn/ooc/pp_baseline.py --selftest" "syn/ooc/pp_baseline_mutants.py" "syn/ooc/pp_baseline_reports_selftest.py"; do
  echo "== python3 $c"; python3 $c; echo "rc=$?"
done
