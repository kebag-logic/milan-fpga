#!/bin/bash
# Copy the final gates' receipts into the output directory: small logs whole, big ones as their tail with size and
# SHA-256, host paths replaced. usage: collect.sh
set -u
T=<scratch>
O=<management>/2026-09-23/665s2b-a683ze/receipts/gates
H=3a1d14c2
san() { sed "s#<scratch>#<scratch>#g; s#<lane>#<lane>#g; s#<tools>#<tools>#g; s#<management>#<management>#g; s#<home>#<home>#g; s#<data>#<data>#g"; }
put() { # SRC DEST: whole when under 150 KB, else its last 200 lines with its size and SHA-256
    local s=$1 d=$2; mkdir -p "$(dirname "$d")"
    if [ "$(stat -c %s "$s")" -lt 150000 ]; then san < "$s" > "$d"
    else { echo "# the last 200 lines of $(basename "$s"): $(stat -c %s "$s") bytes, sha256 $(sha256sum "$s" | cut -c1-64)"; tail -200 "$s" | cut -c1-600 | san; } > "$d.tail"; fi
}
mkdir -p $O/sweep $O/lane $O/harness $O/workflows $O/scripts
for k in 0 1 2 3; do put $T/sweep/shard-$k/spec/01.log $O/sweep/shard-$k.log; put $T/sweep/shard-$k/spec/complete.json $O/sweep/shard-$k.complete.json
    for f in $T/sweep/shard-$k/logs/preflight/*.log; do put $f $O/sweep/preflight-$k/$(basename $f); done; done
san < $T/665s2b-a683ze-sweep-spec.json > $O/sweep/sweep-spec.json 2>/dev/null
for f in $T/gates-out/lane-$H/*.log $T/gates-out/lane-$H/*.rc $T/gates-out/lane-$H/summary.txt $T/gates-out/lane-$H/tree-after.txt; do [ -f "$f" ] && put $f $O/lane/$(basename $f); done
for n in GA8 GA1 GN8 GN1; do [ -f $T/logs/$n-regrade.log ] && grep -v "^COMMAND" $T/logs/$n-regrade.log | true
    [ -f $T/logs/$n-regrade.log ] && { grep -v "^COMMAND" $T/logs/$n-regrade.log > /tmp/a683ze-rg.log; put /tmp/a683ze-rg.log $O/harness/$n-reuse-refused-at-head.log; }
    [ -f $T/builds/$n/results-all/table.md ] && put $T/builds/$n/results-all/table.md $O/harness/$n-table.md
    [ -f $T/builds/$n/results/table.md ] && put $T/builds/$n/results/table.md $O/harness/$n-table.md
    [ -f $T/logs/$n-tree-after.txt ] && put $T/logs/$n-tree-after.txt $O/harness/$n-tree-after.txt
    for k in 0 1 2 3; do [ -f $T/logs/$n-part$k.log ] && { grep -v "^COMMAND" $T/logs/$n-part$k.log > /tmp/a683ze-p.log; put /tmp/a683ze-p.log $O/harness/$n-part$k.log; }; done
    [ -f $T/logs/$n.log ] && { grep -v "^COMMAND" $T/logs/$n.log > /tmp/a683ze-p.log; put /tmp/a683ze-p.log $O/harness/$n-run.log; }
done
put $T/logs/finish.txt $O/harness/finish.txt
put $T/logs/dispatch.txt $O/dispatch.txt
for f in $T/gates-out/wf/*.driver.log; do put $f $O/workflows/drivers/$(basename $f); done
for f in $T/gates-out/wf/logs/*.rc; do cp $f $O/workflows/rc/ 2>/dev/null || { mkdir -p $O/workflows/rc; cp $f $O/workflows/rc/; }; done
for f in $T/gates-out/wf/logs/*__tree-after.txt; do put $f $O/workflows/tree-after/$(basename $f); done
san < $T/gates/not_run.json > $O/workflows/not_run.json
san < $T/gates/run_wf.py > $O/workflows/run_wf.py
san < $T/gates/verify_wf.py > $O/workflows/verify_wf.py
echo collected
# The harness at the head (harness_head_one.sh): each leg's build-and-sample log, its comparison, its regrade.
for n in GA8 GA1 GN8 GN1; do
    for f in head-$n.log head-$n-regrade.log; do [ -f $T/logs/$f ] && { grep -v "^COMMAND" $T/logs/$f > /tmp/a683ze-h.log; put /tmp/a683ze-h.log $O/harness/$f; }; done
    for f in head-$n-compare.txt head-$n-explain.txt head-$n-tree-after.txt; do [ -f $T/logs/$f ] && put $T/logs/$f $O/harness/$f; done
    [ -f $T/builds-head/$n/results-regrade/table.md ] && put $T/builds-head/$n/results-regrade/table.md $O/harness/head-$n-table.md
done
put $T/logs/harness-head.txt $O/harness/harness-head.txt
put $T/logs/clone-hleg-head.log $O/harness/clone-hleg-head.log
put $T/logs/665s2b-a683ze-sweep.txt $O/sweep/launch.txt
for f in harness_head.sh harness_head_one.sh lane_gates_resume.sh dispatch2.py regrade_head.sh sweep_free.py collect2.sh explain_diffs.sh; do put $T/scripts/$f $O/scripts/$f; done
echo collected-head
