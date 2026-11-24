#!/bin/bash
# docs3.sh: wait for the twin plants to end, then docs.yml's gate steps at the lane head (docs_gates_r2.py):
# every run step but the hosted runner's (install, fetch, resolve, budget, record), then the two renderer steps with
# the pinned Markdown renderer, the em-dash gate as a push from 2509db68 and from 30796098.
source /data-2/milan/tmp/lwsrppin-a834/penv.sh
o=/data-2/milan/tmp/lwsrppin-a834/r3/docs; mkdir -p $o; R=/data-2/milan/lanes/lwsrp-pin
while [ ! -e /data-2/milan/tmp/lwsrppin-a834/r3/twin/rc-plants-2 ]; do sleep 20; done
date -Iseconds > $o/start; git -C $R rev-parse HEAD > $o/head; git -C $R status --porcelain > $o/porcelain-before
python3 -B /data-2/milan/tmp/lwsrppin-a834/bin3/docs_gates_r2.py $R $o 2509db684b58b920e215b0d5d327b4a845bac3f4 wire-accountability#4,docs-check-no-git#3,docs-gates-0#3,docs-gates-0#11,docs-gates-0#13,docs-gates-0#14,docs-gates-0#15,docs-gates-0#16,docs-gates-0#17,docs-gates-0#18,docs-gates-0#19,docs-gates-0#20,docs-gates-0#22,docs-gates-0#23,docs-gates-0#26,docs-gates-0#29,docs-gates-0#30,docs-gates-0#31,docs-gates-0#32,docs-gates-0#33,docs-gates-0#34,docs-gates-0#35,docs-gates-0#36,docs-gates-0#37,docs-gates-0#38,docs-gates-0#39,docs-gates-0#40,docs-gates-0#41,docs-gates-0#42,docs-gates-0#43,docs-gates-0#44,docs-gates-0#45,docs-gates-0#46,docs-gates-0#48,docs-gates-0#49,docs-gates-0#50,docs-gates-0#51,docs-gates-0#52,docs-gates-0#53,docs-gates-0#55,docs-gates-1#14,docs-gates-2#14,docs-gates-2#15,docs-gates-2#16 > $o/run.log 2>&1; echo $? > $o/rc-main
python3 -B /data-2/milan/tmp/lwsrppin-a834/bin3/docs_gates_r2.py $R $o 2509db684b58b920e215b0d5d327b4a845bac3f4 docs-gates-0#12,docs-gates-0#47 --md /data-2/milan/tmp/lwsrppin-a834/mdvenv >> $o/run.log 2>&1; echo $? > $o/rc-md
mkdir -p $o/push-30796098; python3 -B /data-2/milan/tmp/lwsrppin-a834/bin3/docs_gates_r2.py $R $o/push-30796098 30796098256670c76115610498a3cdad4d8281ba docs-gates-0#12 --md /data-2/milan/tmp/lwsrppin-a834/mdvenv >> $o/run.log 2>&1; echo $? > $o/rc-md2
git -C $R status --porcelain > $o/porcelain-after; date -Iseconds > $o/end
