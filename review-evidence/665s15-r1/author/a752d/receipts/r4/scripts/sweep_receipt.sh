#!/bin/bash
# Copy one finished shard's receipts: complete.json, spec.json, the tally, the unit's journal lines, the preflight logs.
# usage: sweep_receipt.sh K
set -eu
S=$SCRATCH K=$1 D=$S/sweep5/shard-$K R=$MGMT/2026-09-23/665s15-a752c/receipts/r4/sweep
C="python3 -I $S/scripts/copy_receipts.py"
mkdir -p $S/logs/sw5
cp $D/spec/complete.json $S/logs/sw5/shard-$K-complete.json; cp $D/spec.json $S/logs/sw5/shard-$K-spec.json
sed -n '/^shard: /,$p' $D/spec/01.log > $S/logs/sw5/shard-$K-tally.log
journalctl --user -u milan-665s15-a752d-sw5-shard$K --no-pager -o cat | grep -E "^Started|^START|^END|Consumed" > $S/logs/sw5/shard-$K-unit.txt
$C $R $S/logs/sw5/shard-$K-complete.json $S/logs/sw5/shard-$K-spec.json $S/logs/sw5/shard-$K-tally.log $S/logs/sw5/shard-$K-unit.txt
mkdir -p $R/preflight-$K; for f in $D/logs/preflight/*.log; do $C $R/preflight-$K $f > /dev/null; done
