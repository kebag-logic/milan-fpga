#!/bin/sh
# R601-1 portable suite runner.
# Usage: run_suite.sh <tree> <suite> <logdir> [make target...]
# Runs `make -C <tree>/tb/verilator/<suite> [targets]` with the scoped
# Verilator 5.050 first on PATH, writing <logdir>/<label>.log and
# <logdir>/<label>.rc (label = suite plus targets). The tree is a disposable
# export (git archive of the reviewed head or the dev base plus its pinned
# submodule contents); nothing in the reviewed clone is touched.
set -u
TREE=$1; SUITE=$2; LOGDIR=$3; shift 3
VBIN=${VBIN:-$VALIDATION_TOOLS/pinned-verilator-5.050}
LABEL=$(printf '%s' "$SUITE${*:+_$*}" | tr ' /' '__')
mkdir -p "$LOGDIR"
PATH="$VBIN:$PATH"; export PATH
{
  echo "# tree=$TREE suite=$SUITE targets=${*:-<default>}"
  echo "# verilator: $(verilator --version)"
  echo "# start: $(date -u +%FT%TZ)"
} > "$LOGDIR/$LABEL.log"
make -C "$TREE/tb/verilator/$SUITE" VERILATOR=verilator "$@" >> "$LOGDIR/$LABEL.log" 2>&1
rc=$?
echo "# end: $(date -u +%FT%TZ) rc=$rc" >> "$LOGDIR/$LABEL.log"
echo $rc > "$LOGDIR/$LABEL.rc"
exit $rc
