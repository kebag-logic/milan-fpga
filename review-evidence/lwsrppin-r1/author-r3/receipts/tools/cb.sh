#!/bin/bash
# cb.sh: ctrl_boundary.py --require-rv32 --selftest at the lane head, its start, end and rc recorded.
source /data-2/milan/tmp/lwsrppin-a834/penv.sh
o=/data-2/milan/tmp/lwsrppin-a834/r3; cd /data-2/milan/lanes/lwsrp-pin || exit 9
date -Iseconds > $o/cb.start; git rev-parse HEAD > $o/cb.head
python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest > $o/ctrl_boundary.log 2>&1
echo $? > $o/cb.rc; date -Iseconds > $o/cb.end
