#!/bin/bash
# Collect lane 897 round 7's pass receipts (round 5's collect5.sh: no sweep; the split-firmware suites, the twin) at a head into the output directory (round 2's practice): the
# verification table of every workflow step (verify_wf.py), every job's step logs and rc files (a file over 200 KB is
# listed with its size and sha256 and an excerpt kept), the lane gates, the harness legs' summaries, tables and images,
# and the sweep's summaries. usage: collect3.sh HEAD
set -u
H=$1 T=/data-2/milan/tmp/897-a776 R=$MANAGEMENT/2026-09-23/897-a776/round7/receipts
O=$T/r4/gates-out/final-${H:0:8}
mkdir -p $R/gates/wf $R/gates/lane $R/gates/large $R/harness/final-${H:0:8} $R/sweep
$T/gates/venv/bin/python3 -I $T/gates/verify_wf.py $H $O rtl-fast.yml docs.yml > $R/gates/verify-table.md 2>&1; echo "verify_wf rc=$?" >> $R/gates/verify-table.md
: > $R/gates/large/wf-large-files.txt
for f in $O/logs/*; do
  s=$(stat -c %s $f)
  if [ $s -gt 200000 ]; then
    echo "$(basename $f) $s $(sha256sum $f | cut -d' ' -f1)" >> $R/gates/large/wf-large-files.txt
    { head -40 $f; echo '[...]'; tail -60 $f; } > $R/gates/wf/$(basename $f).excerpt.txt
  else cp $f $R/gates/wf/; fi
done
for f in $O/*.driver.log; do cp $f $R/gates/wf/ 2>/dev/null; done
G=$T/r4/gates-out/lane-${H:0:8}
: > $R/gates/large/lane-large-files.txt
for f in $G/*; do
  s=$(stat -c %s $f)
  if [ $s -gt 200000 ]; then
    echo "$(basename $f) $s $(sha256sum $f | cut -d' ' -f1)" >> $R/gates/large/lane-large-files.txt
    { head -40 $f; echo '[...]'; tail -60 $f; } > $R/gates/lane/$(basename $f).excerpt.txt
  else cp $f $R/gates/lane/; fi
done
for n in hA1 hE1 hB1 hV1 hA8 hE8 hB8 hV8; do
  [ -f $T/r4/logs/hs-$n.log ] && grep -v '^COMMAND\|^INFO\|^│\|^├\|^└\|^ ' $T/r4/logs/hs-$n.log > $R/harness/final-${H:0:8}/summary-$n.txt
  [ -f $T/r4/gates-out/rc/hs-$n.rc ] && cp $T/r4/gates-out/rc/hs-$n.rc $R/harness/final-${H:0:8}/
  [ -f $T/r4/builds/$n/results/table.md ] && cp $T/r4/builds/$n/results/table.md $R/harness/final-${H:0:8}/table-$n.md
done
{ for n in hA1 hE1 hB1 hV1 hA8 hE8 hB8 hV8; do b=$T/r4/builds/$n
    case $n in hA1) m=m7A1;; hE1) m=m7E1;; hB1) m=m7B1;; hV1) m=m7V1;; hA8) m=m7A8;; hE8) m=m7bE8;; hB8) m=m7bB8;; hV8) m=m7bV8;; esac; m=$T/r4/builds/$m
    [ -f $b/image/ctrl_app.elf ] || continue
    a=$(sha256sum $b/image/ctrl_app.elf | cut -c1-16); c=$(sha256sum $m/image/ctrl_app.elf 2>/dev/null | cut -c1-16)
    echo "$n $(grep -h '^PLAN' $T/r4/logs/hs-$n.log) | elf $a | the measurement build ($(basename $m)) $c | $([ "$a" = "$c" ] && echo identical || echo DIFFER)"; done; } > $R/harness/final-${H:0:8}/images.txt
mkdir -p $R/suites
for s in milan_dp mbx milan_dp_gm_steps; do d=$T/r4/rerun-out-$s-${H:0:8}; [ -d $d ] || continue; cp $d/summary.txt $R/suites/$s-summary.txt
  echo "$s.log $(stat -c %s $d/$s.log) $(sha256sum $d/$s.log | cut -d' ' -f1)" >> $R/suites/large-files.txt; { head -30 $d/$s.log; echo '[...]'; tail -60 $d/$s.log; } > $R/suites/$s.log.excerpt.txt; done
mkdir -p $R/twin; for d in twin7-901 twin7-head; do mkdir -p $R/twin/$d; cp $T/r4/$d/summary.txt $R/twin/$d/; grep -E '^\[DIFF\]|^\[OWED\]|^twin: ' $T/r4/$d/twin.log > $R/twin/$d/twin-findings.txt; grep -E 'ESCAPED|REFUSED' $T/r4/$d/twin_plants.log > $R/twin/$d/twin-plants-verdicts.txt; done
cp $T/r4/logs/dispatch-final-${H:0:8}.log $T/r4/logs/final-pass.txt $R/gates/ 2>/dev/null
echo collected
