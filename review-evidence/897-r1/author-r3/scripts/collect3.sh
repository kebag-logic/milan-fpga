#!/bin/bash
# Collect lane 897 round 3's full-pass receipts at a head into the output directory (round 2's practice): the
# verification table of every workflow step (verify_wf.py), every job's step logs and rc files (a file over 200 KB is
# listed with its size and sha256 and an excerpt kept), the lane gates, the harness legs' summaries, tables and images,
# and the sweep's summaries. usage: collect3.sh HEAD
set -u
H=$1 T=/data-2/milan/tmp/897-a776 R=$MANAGEMENT/2026-09-23/897-a776/round3/receipts
O=$T/r3/gates-out/final-${H:0:8}
mkdir -p $R/gates/wf $R/gates/lane $R/gates/large $R/harness/final-${H:0:8} $R/sweep
$T/gates/venv/bin/python3 -I $T/gates/verify_wf.py $H $O rtl-fast.yml docs.yml elaborate.yml rtl.yml \
    --matrix=yosys-shards=shard:0-4,1-4,2-4,3-4 > $R/gates/verify-table.md 2>&1; echo "verify_wf rc=$?" >> $R/gates/verify-table.md
: > $R/gates/large/wf-large-files.txt
for f in $O/logs/*; do
  s=$(stat -c %s $f)
  if [ $s -gt 200000 ]; then
    echo "$(basename $f) $s $(sha256sum $f | cut -d' ' -f1)" >> $R/gates/large/wf-large-files.txt
    { head -40 $f; echo '[...]'; tail -60 $f; } > $R/gates/wf/$(basename $f).excerpt.txt
  else cp $f $R/gates/wf/; fi
done
for f in $O/*.driver.log; do cp $f $R/gates/wf/ 2>/dev/null; done
G=$T/r3/gates-out/lane-${H:0:8}
: > $R/gates/large/lane-large-files.txt
for f in $G/*; do
  s=$(stat -c %s $f)
  if [ $s -gt 200000 ]; then
    echo "$(basename $f) $s $(sha256sum $f | cut -d' ' -f1)" >> $R/gates/large/lane-large-files.txt
    { head -40 $f; echo '[...]'; tail -60 $f; } > $R/gates/lane/$(basename $f).excerpt.txt
  else cp $f $R/gates/lane/; fi
done
for n in fA1 fN1 fB1 fA8 fS8 fN8 fB8; do
  [ -f $T/r3/logs/hs-$n.log ] && grep -v '^COMMAND\|^INFO\|^│\|^├\|^└\|^ ' $T/r3/logs/hs-$n.log > $R/harness/final-${H:0:8}/summary-$n.txt
  [ -f $T/r3/gates-out/rc/hs-$n.rc ] && cp $T/r3/gates-out/rc/hs-$n.rc $R/harness/final-${H:0:8}/
  [ -f $T/r3/builds/$n/results/table.md ] && cp $T/r3/builds/$n/results/table.md $R/harness/final-${H:0:8}/table-$n.md
done
{ for n in fA1 fN1 fB1 fA8 fS8 fN8 fB8; do b=$T/r3/builds/$n; m=$T/r3/builds/h${n:1}; [ $n = fS8 ] && m=$T/r3/builds/hA8
    [ -f $b/image/ctrl_app.elf ] || continue
    a=$(sha256sum $b/image/ctrl_app.elf | cut -c1-16); c=$(sha256sum $m/image/ctrl_app.elf 2>/dev/null | cut -c1-16)
    echo "$n $(grep -h '^PLAN' $T/r3/logs/hs-$n.log) | elf $a | the measurement build at e45981f8 ($(basename $m)) $c | $([ "$a" = "$c" ] && echo identical || echo DIFFER)"; done; } > $R/harness/final-${H:0:8}/images.txt
for k in 0 1 2 3; do
  d=$T/r3/sweep-${H:0:8}/shard-$k; [ -d $d ] || continue; mkdir -p $R/sweep/shard-$k
  cp $d/spec/01.log $R/sweep/shard-$k/summary.log; cp $d/spec/complete.json $d/spec.json $R/sweep/shard-$k/
  (cd $d/logs && sha256sum *.log 2>/dev/null) > $R/sweep/shard-$k/suite-logs-sha256.txt
done
cp $T/r3/logs/launch-sweep-${H:0:8}.txt $T/r3/logs/dispatch-final-${H:0:8}.log $T/r3/logs/final-pass.txt $R/gates/ 2>/dev/null
echo collected
