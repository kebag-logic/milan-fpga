#!/usr/bin/env bash
# Final (issue 529, A231), recorded verbatim as run at 03:28:11 build-box UTC; the block ran
# inside timeout 480 flock -w 60 /tmp/milan-bench.lock bash -c "...".
PK=$MANAGEMENT/2026-09-23/529-a231; OUT=$PK/bench/final; mkdir -p $OUT
P=/dev/serial/by-id/<adapter>
echo LOCK $(date -u +%FT%T.%3NZ) > $OUT/lock.txt
echo start_local $(date -u +%FT%T.%3NZ) > $OUT/timeline.txt
ssh -o BatchMode=yes <bench-host-prefix>pw1 'mkdir -p /tmp/a231/enum-final; rm -f /tmp/a231/enum-final/*.json; sudo -n timeout 130 tcpdump -i ens10 -w /tmp/a231/final.pcap ether proto 0x22f0' > $OUT/tcpdump.log 2>&1 &
CAP=$!
sleep 3
echo census start $(date -u +%FT%T.%3NZ) >> $OUT/timeline.txt
ssh -o BatchMode=yes <bench-host-prefix>pw1 'bash /tmp/a231/a231_census.sh' > $OUT/census-final.jsonl 2>&1
echo enum start $(date -u +%FT%T.%3NZ) >> $OUT/timeline.txt
ssh -o BatchMode=yes <bench-host-prefix>pw1 'sudo -n timeout --signal=TERM 70 /tmp/a231/a200_enum ens10 40 /tmp/a231/enum-final; echo ENUM_RC=$?; sudo -n chown -R alex /tmp/a231/enum-final' > $OUT/a200-enum.log 2>&1
echo enum end $(date -u +%FT%T.%3NZ) >> $OUT/timeline.txt
timeout 60 python3 $PK/tools/console_read.py $P $OUT/console-final.txt milan_status 'mem_read 0x90000750 4' 'mem_read 0x90000764 4' 'mem_read 0x90000738 4' 'mem_read 0x9000074c 4' 'mem_read 0x90000780 4' 'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4' 'mem_read 0x90000774 4' 'mem_read 0x90000720 4' > $OUT/console-final.stdout 2>&1; echo READER_RC=$? >> $OUT/timeline.txt
timeout 60 python3 $LANES/trusted-dev-20260924-50e78097/scripts/baremetal_uart_smoke.py --port $P > $OUT/uart-smoke-final.log 2>&1; echo SMOKE_RC=$? >> $OUT/timeline.txt
wait $CAP; echo capture_rc=$? >> $OUT/timeline.txt
echo UNLOCK $(date -u +%FT%T.%3NZ) >> $OUT/lock.txt
# after the lock was released:
ssh -o BatchMode=yes <bench-host-prefix>pw1 'sudo -n chown alex /tmp/a231/final.pcap; sha256sum /tmp/a231/final.pcap /tmp/a231/enum-final/*.json' | tee $OUT/remote-sha256.txt
scp -q <bench-host-prefix>pw1:/tmp/a231/final.pcap $OUT/pw1-final.pcap; scp -q '<bench-host-prefix>pw1:/tmp/a231/enum-final/*.json' $OUT/
