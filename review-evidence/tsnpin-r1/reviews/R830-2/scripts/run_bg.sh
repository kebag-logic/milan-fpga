#!/usr/bin/env bash
# run_bg.sh NAME TREE CMD... : run CMD in TREE (a scratch copy of the reviewed head) with the pinned SDK at
# $HOME/br-milan-rv32/host, its own log and rc file under receipts/runs. PACKET defaults to this packet.
set -u
P=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
n=$1; t=$2; shift 2
export HOME=$P/scratch/home TMPDIR=$P/scratch/tmp PYTHONHASHSEED=0 PYTHONUNBUFFERED=1 MAKEFLAGS="-j1 --no-print-directory"
TOOLS=${TOOLS:?set TOOLS to the directory holding pinned-verilator-5.050 and the Python env}
export VERILATOR=$TOOLS/pinned-verilator-5.050/verilator
export PATH=$TOOLS/md-venv-40cdefe08ebd/bin:$TOOLS/pinned-verilator-5.050:/usr/local/bin:/usr/bin:/bin
cd "$t" || exit 3
( echo "# head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree}) cmd: $*"; date -u +%FT%TZ; "$@"; rc=$?; date -u +%FT%TZ; exit $rc ) > "$P/receipts/runs/$n.log" 2>&1
echo $? > "$P/receipts/runs/$n.rc"
