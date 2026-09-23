#!/usr/bin/env bash
# Run A (issue 117, A200): steady-state capture for steps 2 and 4.
# 300 s tap capture + console poll every 5 s (under the bench lock) + controller-host
# GET_AVB_INFO/GET_AS_PATH poll every 5 s on the DUT and the reference peer.
set -u
PK=$REVIEWS/117-a200-packet
OUT=$PK/bench/runA
mkdir -p "$OUT"
P=/dev/<adapter>
DUR=${DUR:-300}
echo "start_local $(date -u +%FT%T.%3NZ)" > "$OUT/timeline.txt"
ssh -o BatchMode=yes <bench-host-prefix>ubuntu-server "sudo -n timeout $((DUR+15)) tcpdump -i <MAC-derived-interface-name> -w /tmp/a200-runA.pcap" > "$OUT/tcpdump.log" 2>&1 &
CAP=$!
sleep 3
echo "console_start_local $(date -u +%FT%T.%3NZ)" >> "$OUT/timeline.txt"
timeout $((DUR+40)) flock -w 30 /tmp/milan-bench.lock bash -c "echo LOCK \$(date -u +%FT%T.%3NZ); timeout $((DUR+20)) python3 $PK/tools/console_poll.py $P $OUT/console.txt $DUR 5 milan_status 'mem_read 0x9000062c 4' 'mem_read 0x90000644 4' 'mem_read 0x90000780 4' 'mem_read 0x900007e4 4' 'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4' 'mem_read 0x90000774 4' 'mem_read 0x90000720 4' 'mem_read 0x900006f4 4'; echo POLL_RC=\$?; echo UNLOCK \$(date -u +%FT%T.%3NZ)" > "$OUT/lock.txt" 2>&1 &
CON=$!
ssh -o BatchMode=yes <bench-host-prefix>pw1 "sudo -n timeout $((DUR+20)) python3 /tmp/a200/avdecc_ro.py watch ens10 $DUR 5 020000fffe000001=02:00:00:00:00:01 3cc0c60102030000=3c:c0:c6:01:02:03" > "$OUT/pw1-watch.jsonl" 2>&1 &
PW=$!
wait $CON; echo "console_rc=$?" >> "$OUT/timeline.txt"
wait $PW; echo "pw1_rc=$?" >> "$OUT/timeline.txt"
wait $CAP; echo "capture_rc=$?" >> "$OUT/timeline.txt"
echo "end_local $(date -u +%FT%T.%3NZ)" >> "$OUT/timeline.txt"
ssh -o BatchMode=yes <bench-host-prefix>ubuntu-server 'sudo -n chown alex /tmp/a200-runA.pcap' && scp -q <bench-host-prefix>ubuntu-server:/tmp/a200-runA.pcap "$OUT/tap-runA.pcap"
echo "copied_rc=$?" >> "$OUT/timeline.txt"
