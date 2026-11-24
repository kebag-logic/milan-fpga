#!/bin/bash
source /data-2/milan/tmp/lwsrppin-a834/penv.sh
o=/data-2/milan/tmp/lwsrppin-a834/docs; mkdir -p $o
date -Iseconds > $o/start; git -C /data-2/milan/lanes/lwsrp-pin rev-parse HEAD > $o/head
python3 /data-2/milan/tmp/lwsrppin-a834/bin/docs_gates.py /data-2/milan/lanes/lwsrp-pin $o aa30d77f75 > $o/run.log 2>&1
echo $? > $o/rc; date -Iseconds > $o/end
