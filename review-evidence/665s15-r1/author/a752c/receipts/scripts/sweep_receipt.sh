#!/bin/bash
# Copy one finished shard's receipts: complete.json, spec.json, the tally, the unit's journal lines, the preflight logs.
# usage: sweep_receipt.sh K
set -eu
T=$SCRATCH K=$1 D=$T/sweep3/shard-$K R="bash $T/scripts/receipt.sh"
$R sweep/7aa6 $D/spec/complete.json shard-$K-complete.json
$R sweep/7aa6 $D/spec.json shard-$K-spec.json
sed -n '/^shard: /,$p' $D/spec/01.log > $T/logs/shard-$K-tally.log
$R sweep/7aa6 $T/logs/shard-$K-tally.log
journalctl --user -u milan-665s15-a752c-sw3-shard$K --no-pager -o cat | grep -E "^Started|^START|^END|Consumed" > $T/logs/shard-$K-unit.txt
$R sweep/7aa6 $T/logs/shard-$K-unit.txt
for f in $D/logs/preflight/*.log; do $R sweep/7aa6/preflight-$K $f; done
