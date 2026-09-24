#!/usr/bin/env bash
# Final state (issue 530, A237). Run under the bench lock by the caller:
#   timeout 400 flock -w 60 /tmp/milan-bench.lock bash tools/run_final.sh
# 40 s tap capture (no stream expected), end census on the controller host,
# console read (read-only), UART grader.
set -u
PK=$REVIEWS/530-a237-packet; OUT=$PK/bench/final; mkdir -p $OUT
P=/dev/serial/by-id/<adapter>
ts() { date -u +%FT%T.%3NZ; }
echo "LOCK $(ts)"
echo "start_local $(ts)" > $OUT/timeline.txt
ssh -o BatchMode=yes <bench-host-prefix>ubuntu-server "sudo -n timeout 40 tcpdump -i <MAC-derived-interface-name> -w /tmp/a237/tap-final.pcap" > $OUT/tcpdump-tap.log 2>&1 &
CAP=$!
sleep 2
echo "census_start $(ts)" >> $OUT/timeline.txt
timeout 200 ssh -o BatchMode=yes <bench-host-prefix>pw1 'bash /tmp/a237/a237_census.sh' > $OUT/census-final.jsonl 2>&1
echo "census_end rc=$? $(ts)" >> $OUT/timeline.txt
timeout 60 python3 $PK/tools/console_read.py $P $OUT/console-final.txt milan_status 'mem_read 0x90000750 4' \
  'mem_read 0x90000764 4' 'mem_read 0x90000694 4' 'mem_read 0x90000698 4' 'mem_read 0x9000066c 4' \
  'mem_read 0x90000780 4' 'mem_read 0x90000788 4' 'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4' \
  'mem_read 0x90000774 4' 'mem_read 0x90000720 4' > $OUT/console-final.stdout 2>&1
echo "reader_rc=$? $(ts)" >> $OUT/timeline.txt
timeout 60 python3 $PK/tools/baremetal_uart_smoke.py --port $P > $OUT/uart-smoke-final.log 2>&1
echo "smoke_rc=$? $(ts)" >> $OUT/timeline.txt
wait $CAP; echo "capture_rc=$? $(ts)" >> $OUT/timeline.txt
echo "UNLOCK $(ts)"
