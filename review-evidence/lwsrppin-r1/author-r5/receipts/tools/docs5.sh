#!/bin/bash
# docs5.sh: docs.yml's gate steps at the lane head (round 3's selection, docs_gates_r2.py), the em-dash gate as a push
# from 507bce7f (this commit's parent), then the two renderer steps with the pinned Markdown renderer.
source /data-2/milan/tmp/lwsrppin-a834/penv.sh
o=/data-2/milan/tmp/lwsrppin-a834/r5/docs2; mkdir -p $o; R=/data-2/milan/lanes/lwsrp-pin; B=/data-2/milan/tmp/lwsrppin-a834/bin3
base=507bce7f9fe50fcaf7b0abe6a198bdb4d0ea4698
date -Iseconds > $o/start; git -C $R rev-parse HEAD > $o/head; git -C $R status --porcelain > $o/porcelain-before
python3 -B $B/docs_gates_r2.py $R $o $base wire-accountability#4,docs-check-no-git#3,docs-gates-0#3,docs-gates-0#11,docs-gates-0#13,docs-gates-0#14,docs-gates-0#15,docs-gates-0#16,docs-gates-0#17,docs-gates-0#18,docs-gates-0#19,docs-gates-0#20,docs-gates-0#22,docs-gates-0#23,docs-gates-0#26,docs-gates-0#29,docs-gates-0#30,docs-gates-0#31,docs-gates-0#32,docs-gates-0#33,docs-gates-0#34,docs-gates-0#35,docs-gates-0#36,docs-gates-0#37,docs-gates-0#38,docs-gates-0#39,docs-gates-0#40,docs-gates-0#41,docs-gates-0#42,docs-gates-0#43,docs-gates-0#44,docs-gates-0#45,docs-gates-0#46,docs-gates-0#48,docs-gates-0#49,docs-gates-0#50,docs-gates-0#51,docs-gates-0#52,docs-gates-0#53,docs-gates-0#55,docs-gates-1#14,docs-gates-2#14,docs-gates-2#15,docs-gates-2#16 > $o/run.log 2>&1; echo $? > $o/rc-main
python3 -B $B/docs_gates_r2.py $R $o $base docs-gates-0#12,docs-gates-0#47 --md /data-2/milan/tmp/lwsrppin-a834/mdvenv >> $o/run.log 2>&1; echo $? > $o/rc-md
git -C $R status --porcelain > $o/porcelain-after; date -Iseconds > $o/end
