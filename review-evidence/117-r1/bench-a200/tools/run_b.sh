#!/usr/bin/env bash
# Run B (issue 117, A200): tu on the wire. Tap capture + console poll every 2 s
# (under the bench lock) around a 60 s CRF bind window on the reference peer.
set -u
PK=$REVIEWS/117-a200-packet
OUT=$PK/bench/runB
mkdir -p "$OUT"
P=/dev/<adapter>
echo "start_local $(date -u +%FT%T.%3NZ)" > "$OUT/timeline.txt"
ssh -o BatchMode=yes <bench-host-prefix>ubuntu-server "sudo -n timeout 115 tcpdump -i <MAC-derived-interface-name> -w /tmp/a200-runB.pcap" > "$OUT/tcpdump.log" 2>&1 &
CAP=$!
sleep 3
timeout 150 flock -w 30 /tmp/milan-bench.lock bash -c "echo LOCK \$(date -u +%FT%T.%3NZ); timeout 125 python3 $PK/tools/console_poll.py $P $OUT/console.txt 105 2 milan_status 'mem_read 0x90000750 4' 'mem_read 0x90000764 4' 'mem_read 0x9000066c 4' 'mem_read 0x90000780 4' 'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4'; echo POLL_RC=\$?; echo UNLOCK \$(date -u +%FT%T.%3NZ)" > "$OUT/lock.txt" 2>&1 &
CON=$!
ssh -o BatchMode=yes <bench-host-prefix>pw1 "sudo -n timeout -k 30 140 python3 /tmp/a200/crf_bind_window.py ens10 10 60 25" > "$OUT/pw1-bind.jsonl" 2>&1
echo "pw1_rc=$?" >> "$OUT/timeline.txt"
wait $CON; echo "console_rc=$?" >> "$OUT/timeline.txt"
wait $CAP; echo "capture_rc=$?" >> "$OUT/timeline.txt"
echo "end_local $(date -u +%FT%T.%3NZ)" >> "$OUT/timeline.txt"
ssh -o BatchMode=yes <bench-host-prefix>ubuntu-server 'sudo -n chown alex /tmp/a200-runB.pcap' && scp -q <bench-host-prefix>ubuntu-server:/tmp/a200-runB.pcap "$OUT/tap-runB.pcap"
echo "copied_rc=$?" >> "$OUT/timeline.txt"
