#!/usr/bin/env bash
# Run one donor suite (default `make` target) in the head or base scratch copy with
# the pinned tool.  Usage: 07-donor-suite.sh <head|base> <suite>
set -uo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); export PATH=$PK/tools:$PATH
tree=$1; suite=$2; log=$PK/receipts/07-$tree-$suite.log
(cd $PK/scratch/$tree/tb/$suite && make) > $log 2>&1; rc=$?
tally=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' $log | tail -1)
echo "$tree $suite rc=$rc ${tally:-NO-TALLY}"
(cd $PK/scratch/$tree/tb/$suite && make clean >/dev/null 2>&1 || true)
