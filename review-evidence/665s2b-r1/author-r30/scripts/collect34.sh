#!/bin/bash
# The final pass's receipts at a head into the output directory's receipts/final-<head>: small logs whole, big ones as
# their last 200 lines with their size and sha256 (host paths replaced afterwards by scrub30.py). usage: collect34.sh HEAD
set -u
T=/data-2/milan/tmp/665s2b-a683zo HF=$1 H=${1:0:8}
O=$MANAGEMENT/2026-09-23/665s2b-a683zo/receipts/final-$H
put() { local s=$1 d=$2; mkdir -p "$(dirname "$d")"
    if [ "$(stat -c %s "$s")" -lt 150000 ]; then cp "$s" "$d"
    else { echo "# the last 200 lines of $(basename "$s"): $(stat -c %s "$s") bytes, sha256 $(sha256sum "$s" | cut -c1-64)"; tail -n 200 "$s" | cut -c1-600; } > "$d.tail"; fi; }
mkdir -p $O/sweep $O/lane $O/workflows $O/harness
S=$T/gates-run/sweep
for k in 0 1 2 3; do
    for f in $S/shard-$k/spec.json $S/shard-$k/*.json $S/shard-$k/*.log; do [ -f "$f" ] && put $f $O/sweep/shard-$k-$(basename $f); done
    for f in $S/shard-$k/logs/preflight/*.log; do [ -f "$f" ] && put $f $O/sweep/preflight-$k/$(basename $f); done
    for f in $S/shard-$k/logs/*.log $S/shard-$k/logs/*.txt $S/shard-$k/logs/*.json; do [ -f "$f" ] && put $f $O/sweep/suites-$k/$(basename $f); done
done
put $T/665s2b-a683zo-sweep-spec.json $O/sweep/sweep-spec.json
put $T/logs/launch-sweep34.txt $O/sweep/launch.txt
for f in $T/gates-out/lane-$H/*; do [ -f "$f" ] && put $f $O/lane/$(basename $f); done
for f in $T/gates-out/lane-$H/rederive/*; do [ -f "$f" ] && put $f $O/lane/rederive/$(basename $f); done
W=$T/gates-out/wf-$H
for f in $W/*.driver.log; do put $f $O/workflows/drivers/$(basename $f); done
mkdir -p $O/workflows/rc; for f in $W/logs/*.rc; do [ -f "$f" ] && cp $f $O/workflows/rc/; done
for f in $W/logs/*__tree-after.txt; do [ -f "$f" ] && put $f $O/workflows/tree-after/$(basename $f); done
for f in $W/logs/*.log; do [ -f "$f" ] && put $f $O/workflows/logs/$(basename $f); done
for f in not_run.json run_wf.py verify_wf.py; do put $T/gates/$f $O/workflows/$f; done
[ -f $T/logs/verify-$HF.md ] && put $T/logs/verify-$HF.md $O/workflows/verify-table.md
for n in X-GA8 X-GN8 X-GB8 X-GA1 X-GN1 X-GB1; do
    for f in $T/logs/$n.log $T/logs/$n.log.rc $T/logs/$n-compare.txt $T/logs/$n-regrade.log $T/logs/$n-tree-after.txt; do
        [ -f "$f" ] && put $f $O/harness/$(basename $f); done; done
for f in $T/logs/ctl-*-$H.log $T/logs/ctl-*-$H.log.rc $T/logs/ctl-*-$H-tree-after.txt; do [ -f "$f" ] && put $f $O/harness/controls/$(basename $f); done
put $T/logs/dispatch30.txt $O/dispatch.txt
mkdir -p $O/../../scripts $O/../../tools
for f in $T/scripts/*; do [ -f "$f" ] && put $f $O/../../scripts/$(basename $f); done
for f in $T/tools/*.py; do put $f $O/../../tools/$(basename $f); done
echo collected34
