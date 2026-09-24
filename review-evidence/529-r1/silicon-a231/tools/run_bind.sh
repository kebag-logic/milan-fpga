#!/usr/bin/env bash
# Step 3 (issue 529, A231): counters before, during and after a bounded CRF bind.
# Run under the bench lock (the caller takes flock /tmp/milan-bench.lock).
#   - controller-host capture of AVTP/AVDECC on its own port (no tap, no instrument);
#   - console poll every 5 s: milan_status plus CRF talker/sink, controller-diag and drop CSRs;
#   - la_avdecc enumerator (the #117 binary) kept alive 300 s as the registered controller,
#     so the DUT pushes its Table 5.22 unsolicited notifications to it;
#   - read-only GET_COUNTERS poll every 5 s: DUT STREAM_INPUT 0/1, STREAM_OUTPUT 0/1,
#     AVB_INTERFACE 0, CLOCK_DOMAIN 0, and the reference peer's STREAM_INPUT 8;
#   - crf_bind_window.py (the #117 tool, unchanged): peer STREAM_INPUT 8 <- DUT STREAM_OUTPUT 1,
#     20 s pre, 180 s bound, 40 s post; refuses unless the input reads unbound; always unbinds.
set -u
PK=$MANAGEMENT/2026-09-23/529-a231
OUT=$PK/bench/step3
mkdir -p "$OUT"
P=/dev/serial/by-id/<adapter>
R=<bench-host-prefix>pw1
DUT=020000fffe000001; DMAC=02:00:00:00:00:01; PEER=3cc0c60102030000; PMAC=3c:c0:c6:01:02:03
ts() { date -u +%FT%T.%3NZ; }
echo "start_local $(ts)" > "$OUT/timeline.txt"
ssh -o BatchMode=yes $R "mkdir -p /tmp/a231/enum-bind && rm -f /tmp/a231/enum-bind/*.json; sudo -n timeout 345 tcpdump -i ens10 -w /tmp/a231/bind.pcap ether proto 0x22f0" > "$OUT/tcpdump.log" 2>&1 &
CAP=$!
timeout 340 python3 $PK/tools/console_poll.py $P $OUT/console.txt 320 5 milan_status \
  'mem_read 0x90000750 4' 'mem_read 0x90000764 4' 'mem_read 0x9000066c 4' 'mem_read 0x90000738 4' \
  'mem_read 0x9000074c 4' 'mem_read 0x90000780 4' 'mem_read 0x900006f4 4' 'mem_read 0x900007e8 4' \
  'mem_read 0x900007ec 4' 'mem_read 0x90000720 4' > "$OUT/console-poll.stdout" 2>&1 &
CON=$!
sleep 3
echo "enum_start_local $(ts)" >> "$OUT/timeline.txt"
ssh -o BatchMode=yes $R "sudo -n timeout --signal=TERM 330 /tmp/a231/a200_enum ens10 300 /tmp/a231/enum-bind; echo ENUM_RC=\$?; sudo -n chown -R alex /tmp/a231/enum-bind" > "$OUT/a200-enum.log" 2>&1 &
ENUM=$!
sleep 12
echo "poll_start_local $(ts)" >> "$OUT/timeline.txt"
ssh -o BatchMode=yes $R "sudo -n timeout 300 python3 /tmp/a231/a231_counters_poll.py ens10 285 5 \
  $DUT=$DMAC:5:0 $DUT=$DMAC:5:1 $DUT=$DMAC:6:0 $DUT=$DMAC:6:1 $DUT=$DMAC:9:0 $DUT=$DMAC:0x24:0 $PEER=$PMAC:5:8" > "$OUT/counters-poll.jsonl" 2>&1 &
POLL=$!
sleep 15
echo "bind_window_start_local $(ts)" >> "$OUT/timeline.txt"
ssh -o BatchMode=yes $R "sudo -n timeout -k 30 300 python3 /tmp/a231/crf_bind_window.py ens10 20 180 40" > "$OUT/pw1-bind.jsonl" 2>&1
echo "bind_rc=$? bind_window_end_local $(ts)" >> "$OUT/timeline.txt"
wait $POLL; echo "poll_rc=$?" >> "$OUT/timeline.txt"
wait $ENUM; echo "enum_rc=$?" >> "$OUT/timeline.txt"
wait $CON; echo "console_rc=$?" >> "$OUT/timeline.txt"
wait $CAP; echo "capture_rc=$?" >> "$OUT/timeline.txt"
echo "end_local $(ts)" >> "$OUT/timeline.txt"
