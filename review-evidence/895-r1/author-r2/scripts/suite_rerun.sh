#!/bin/bash
# Re-run named suites of the full sweep in a sweep clone as run_all_suites.sh runs each (make -C tb/verilator/<suite>,
# then scripts/suite_tally.py --verdict on its log), with CI's MAKEFLAGS form (rtl.yml: -jN --no-print-directory)
# (lane 895 round 2). usage: suite_rerun.sh CLONE OUT SUITE...
set -u
C=$1 O=$2; shift 2
export PATH=$WORKSPACE_HOME/litex-milan/venv/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export VERILATOR_ROOT=$WORKSPACE_HOME/.local/share/containers/storage/overlay/9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff/usr/share/verilator
export PYTHONHASHSEED=0 MAKEFLAGS="-j4 --no-print-directory"
mkdir -p $O
cd $C || exit 3
echo "head $(git rev-parse HEAD) tracked changes $(git status --porcelain --untracked-files=no | wc -l) MAKEFLAGS=$MAKEFLAGS" > $O/summary.txt
for s in "$@"; do
  timeout 7200 make -C tb/verilator/$s > $O/$s.log 2>&1; rc=$?
  v=$(python3 scripts/suite_tally.py --verdict $O/$s.log 2>&1); vr=$?
  echo "$s make rc $rc, tally verdict rc $vr: $v" >> $O/summary.txt
done
echo "tracked changes after $(git status --porcelain --untracked-files=no | wc -l)" >> $O/summary.txt
