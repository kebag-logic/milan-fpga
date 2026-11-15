#!/bin/bash
# Lane 897 round 6's clean-clone pass for a head (round 5's gate_queue5.sh, reduced to what round 6 changes: the
# record classes, the harness self-test's mutants, docs): the docs workflow's jobs (run_wf.py, each on its own fresh
# clean clone), the lane gates that reach record_classes and the docs and idiom gates (part r6, with R833-5's stub
# probe), the ROM gates (part r6rom: the 8 images), and one group of every harness arm at each point (fresh builds, whose
# ELFs show the images unchanged and whose legs the record classes grade). No sweep: no firmware or RTL change.
# usage: gate_queue6.sh HEAD OUTDIR > QUEUE
set -u
H=$1 O=$2
T=/data-2/milan/tmp/897-a776
W="/usr/bin/python3 $T/gates/run_wf.py"
C=$T/r4/cl-final-${H:0:8}
for p in r6 r6rom; do echo "lane-$p 10G /bin/bash $T/scripts/r4/lane_gates6.sh $H ${H:0:8} $p"; done
for spec in "B1 1x1 aecp,aecp-fanout,aecp-largest-notice --variant answering-ports" \
            "B8 8x8 aecp,aecp-largest-notice,aecp-fanout --variant answering-ports" \
            "A1 1x1 aecp" "A8 8x8 aecp" \
            "E1 1x1 notice-every-0 --variant answering-every-port" \
            "N8 8x8 notice-every-0 --variant answering-every-port"; do
  set -- $spec; n=$1; shift
  echo "hs-g$n 10G /bin/bash $T/scripts/r4/hs3.sh $C g$n $* > $T/r4/logs/hs-g$n.log 2>&1"
done
echo "W-docs-a 10G mkdir -p $O; for j in wire-accountability docs-check-no-git docs-check; do $W docs.yml $H \$j $O > $O/docs-\$j.driver.log 2>&1; done"
for j in docs-gates-0 docs-gates-1 docs-gates-2; do echo "W-$j 10G mkdir -p $O; $W docs.yml $H $j $O > $O/docs-$j.driver.log 2>&1"; done
