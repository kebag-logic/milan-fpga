#!/usr/bin/env bash
# run_bg.sh NAME CMD... : run CMD in the reviewed clone with its own log and rc file under receipts/runs
set -u
P=${PACKET:-$REVIEWS/tsnpin-r830-1-packet}
C=${CLONE:-$REVIEWS/r830-1-tsnpin}
n=$1; shift
export TMPDIR=$P/scratch/tmp PYTHONHASHSEED=0 PYTHONUNBUFFERED=1 MAKEFLAGS="-j1 --no-print-directory"
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export PATH=$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:$HOME/br-milan-rv32/host/bin:/usr/local/bin:/usr/bin:/bin
cd "$C" || exit 3
( echo "# head $(git rev-parse HEAD) cmd: $*"; date -u +%FT%TZ; "$@"; rc=$?; date -u +%FT%TZ; exit $rc ) > "$P/receipts/runs/$n.log" 2>&1
echo $? > "$P/receipts/runs/$n.rc"
