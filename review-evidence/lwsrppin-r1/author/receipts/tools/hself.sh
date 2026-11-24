#!/bin/bash
source /data-2/milan/tmp/lwsrppin-a834/penv.sh
o=/data-2/milan/tmp/lwsrppin-a834/harness; cd /data-2/milan/lanes/lwsrp-pin || exit 9
date -Iseconds > $o/start-selftest; git rev-parse HEAD > $o/head-selftest
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test > $o/selftest.log 2>&1; echo $? > $o/rc-selftest; date -Iseconds > $o/end-selftest
