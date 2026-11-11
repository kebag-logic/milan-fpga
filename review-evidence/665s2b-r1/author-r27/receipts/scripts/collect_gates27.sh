#!/bin/bash
# The final pass's receipts at a head into the output directory's receipts/gates: small logs whole, big ones as their
# last 200 lines with their size and sha256, host paths replaced afterwards by scrub.py. usage: collect_gates27.sh H8
set -u
T=<scratch> H=$1
O=<management>/2026-09-23/665s2b-a683zj/receipts/gates
put() { local s=$1 d=$2; mkdir -p "$(dirname "$d")"
    if [ "$(stat -c %s "$s")" -lt 150000 ]; then cp "$s" "$d"
    else { echo "# the last 200 lines of $(basename "$s"): $(stat -c %s "$s") bytes, sha256 $(sha256sum "$s" | cut -c1-64)"; tail -n 200 "$s" | cut -c1-600; } > "$d.tail"; fi; }
mkdir -p $O/sweep $O/lane $O/workflows
for k in 0 1 2 3; do
    for f in $T/sweep/shard-$k/spec/*.log; do [ -f "$f" ] && put $f $O/sweep/shard-$k-$(basename $f); done
    [ -f $T/sweep/shard-$k/spec/complete.json ] && put $T/sweep/shard-$k/spec/complete.json $O/sweep/shard-$k.complete.json
    for f in $T/sweep/shard-$k/logs/preflight/*.log; do [ -f "$f" ] && put $f $O/sweep/preflight-$k/$(basename $f); done
done
for f in $T/sweep/rerun-*/*.log; do [ -f "$f" ] && put $f $O/sweep/$(basename $(dirname $f))/$(basename $f); done
put $T/665s2b-a683zj-sweep-spec.json $O/sweep/sweep-spec.json
put $T/logs/665s2b-a683zj-sweep.txt $O/sweep/launch.txt
for f in $T/gates-out/lane-$H/*; do [ -f "$f" ] && put $f $O/lane/$(basename $f); done
W=$T/gates-out/wf-$H
for f in $W/*.driver.log; do put $f $O/workflows/drivers/$(basename $f); done
mkdir -p $O/workflows/rc; for f in $W/logs/*.rc; do [ -f "$f" ] && cp $f $O/workflows/rc/; done
for f in $W/logs/*__tree-after.txt; do [ -f "$f" ] && put $f $O/workflows/tree-after/$(basename $f); done
for f in $W/logs/*.log; do [ -f "$f" ] && put $f $O/workflows/logs/$(basename $f); done
for f in not_run.json run_wf.py verify_wf.py; do put $T/gates/$f $O/workflows/$f; done
[ -f $T/logs/verify-$H.md ] && put $T/logs/verify-$H.md $O/workflows/verify-table.md
put $T/logs/dispatch.txt $O/dispatch-to-1107.txt; put $T/logs/dispatch3.txt $O/dispatch3.txt
put $T/gates-out/queue-as-started.txt $O/queue-to-1107.txt; put $T/gates-out/queue3-as-started.txt $O/queue3.txt

# the outputs set aside unused: the jobs cut at 11:05 and 11:07, their driver logs and step logs
for d in killed-1105 killed-1107; do
    for f in $W/$d/*.driver.log $W/$d/logs/*; do [ -f "$f" ] && put $f $O/workflows/$d/$(basename $f); done
done
for f in dispatch3.py a683zj_sweep_wait.py sweep_free.py lane_gates.sh unit.sh env.sh clone.sh collect_gates27.sh index27.py assemble_pr.py scrub.py; do
    put $T/scripts/$f $O/../scripts/$f; done
put $T/logs/verify-e7e2b744.md $O/workflows/verify-table.md
echo collected27
