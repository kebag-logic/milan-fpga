#!/usr/bin/env bash
# Final state and the third enumeration, in the #529 final shape (issue 387, A249). Run under
# the bench lock:
#   timeout 480 flock -w 60 /tmp/milan-bench.lock bash tools/run_final.sh
# Controller host: its own-port capture (AVDECC ethertype), the end census, the #117 enumerator
# for 40 s. Console: read-only reads, then the UART grader.
set -u
PK=$MANAGEMENT/2026-09-23/387-a249; OUT=$PK/bench/final; mkdir -p $OUT
P=/dev/serial/by-id/<adapter>
ts() { date -u +%FT%T.%3NZ; }
echo "LOCK $(ts)" > $OUT/lock.txt
echo "start_local $(ts)" > $OUT/timeline.txt
ssh -o BatchMode=yes <bench-host-prefix>pw1 'mkdir -p /tmp/a249/enum-final; rm -f /tmp/a249/enum-final/*.json; sudo -n timeout 130 tcpdump -i ens10 -w /tmp/a249/final.pcap ether proto 0x22f0' > $OUT/tcpdump.log 2>&1 &
CAP=$!
sleep 3
echo "census start $(ts)" >> $OUT/timeline.txt
timeout 200 ssh -o BatchMode=yes <bench-host-prefix>pw1 'bash /tmp/a249/a249_census.sh' > $OUT/census-final.jsonl 2>&1
echo "census end rc=$? $(ts)" >> $OUT/timeline.txt
echo "enum start $(ts)" >> $OUT/timeline.txt
ssh -o BatchMode=yes <bench-host-prefix>pw1 'sudo -n timeout --signal=TERM 70 /tmp/a249/a200_enum ens10 40 /tmp/a249/enum-final; echo ENUM_RC=$?; sudo -n chown -R alex /tmp/a249/enum-final' > $OUT/a200-enum.log 2>&1
echo "enum end $(ts)" >> $OUT/timeline.txt
timeout 60 python3 $PK/tools/console_read.py $P $OUT/console-final.txt milan_status 'mem_read 0x9000077c 4' \
  'mem_read 0x90000780 4' 'mem_read 0x900007e4 4' 'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4' \
  'mem_read 0x90000720 4' 'mem_read 0x90000774 4' 'mem_read 0x90000750 4' 'mem_read 0x90000764 4' \
  > $OUT/console-final.stdout 2>&1; echo "READER_RC=$? $(ts)" >> $OUT/timeline.txt
timeout 60 python3 $PK/tools/baremetal_uart_smoke.py --port $P > $OUT/uart-smoke-final.log 2>&1; echo "SMOKE_RC=$? $(ts)" >> $OUT/timeline.txt
wait $CAP; echo "capture_rc=$? $(ts)" >> $OUT/timeline.txt
echo "UNLOCK $(ts)" >> $OUT/lock.txt
