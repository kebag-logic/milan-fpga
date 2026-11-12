#!/bin/bash
# The final pass's receipts at a head into the output directory's receipts/gates: small logs whole, big ones as their
# last 200 lines with their size and sha256, host paths replaced afterwards by scrub.py. usage: collect_gates28.sh H8 HEAD
set -u
T=<scratch> H=$1 HF=$2
O=<management>/2026-09-23/665s2b-a683zm/receipts/gates
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
put $T/665s2b-a683zm-sweep-spec.json $O/sweep/sweep-spec.json
put $T/logs/665s2b-a683zm-sweep.txt $O/sweep/launch.txt
for f in $T/gates-out/lane-$H/*; do [ -f "$f" ] && put $f $O/lane/$(basename $f); done
W=$T/gates-out/wf-$HF
for f in $W/*.driver.log; do put $f $O/workflows/drivers/$(basename $f); done
mkdir -p $O/workflows/rc; for f in $W/logs/*.rc; do [ -f "$f" ] && cp $f $O/workflows/rc/; done
for f in $W/logs/*__tree-after.txt; do [ -f "$f" ] && put $f $O/workflows/tree-after/$(basename $f); done
for f in $W/logs/*.log; do [ -f "$f" ] && put $f $O/workflows/logs/$(basename $f); done
for f in not_run.json run_wf.py verify_wf.py; do put $T/gates/$f $O/workflows/$f; done

for f in $W/first-elaborate-gates-1/*.driver.log $W/first-elaborate-gates-1/logs/*; do [ -f "$f" ] && put $f $O/workflows/first-elaborate-gates-1/$(basename $f); done
# the elaborate job run again (its LiteX simulation timed out under the session pool's load on the first run)
W2=$T/gates-out/wf2-$HF
for f in $W2/*.driver.log; do [ -f "$f" ] && put $f $O/workflows/rerun-elaborate-gates-1/$(basename $f); done
for f in $W2/logs/*; do [ -f "$f" ] && put $f $O/workflows/rerun-elaborate-gates-1/logs/$(basename $f); done
for f in a683zm_disp.py a683zm_sweep_wait.py lane_gates.sh gate_queue.sh head28.sh head_all.sh head_sample.sh compare_builds.py unit.sh env.sh clone.sh make_donor.sh fleg.sh pair.sh rest4.sh ctl.sh ctl2.sh ctls.sh remerge.sh merge_leg.py a683zm_helper.py a683zm_helper2.py qimage.sh early.sh collect_gates28.sh; do
    put $T/scripts/$f $O/../scripts/$f; done
[ -f $T/logs/verify-$HF.md ] && put $T/logs/verify-$HF.md $O/workflows/verify-table.md
put $T/logs/dispatch3.txt $O/dispatch.txt; put $T/gates-out/queue-as-started.txt $O/queue-as-started.txt
echo collected28
