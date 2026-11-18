#!/bin/bash
# One measurement leg: run.py at a point on CLONE, into BUILD, JOBS groups at once. usage: leg.sh CLONE BUILD POINT JOBS [run.py args]
# A leg given --reuse-build waits (up to 50 min) for the building leg's log WAIT_LOG to show the native model run.
set -u
C=$1 B=$2 P=$3 J=$4; shift 4
T=<scratch>
. $T/bin/env.sh
export MAKEFLAGS="-j8 --no-print-directory" PYTHONUNBUFFERED=1 TMPDIR=$T/tmp/$(basename $B)-$$
mkdir -p $B $TMPDIR
case " $* " in *" --reuse-build "*)
  timeout 3000 bash -c "until [ -s '$B/build.json' ] && [ -e '$B/native/Vsim' ] && grep -q '^COMMAND .*native/Vsim' '$WAIT_LOG'; do sleep 20; done" || { echo "no build"; exit 3; } ;;
esac
echo "HEAD $(git -C $C rev-parse HEAD) DIRTY $(git -C $C status --porcelain --untracked-files=no | wc -l) point $P jobs $J args $* start $(date +%FT%T)"
python3 -B $C/tb/verilator/ctrl_service_budget/run.py --point $P --build-dir $B --record-budget-findings --record-share-findings --jobs $J "$@"
rc=$?; echo "END rc=$rc $(date +%FT%T)"; rm -rf $TMPDIR; exit $rc
