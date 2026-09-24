#!/usr/bin/env bash
# Issue 530 silicon rerun (A237): the #117 Run B shape with a 720 s bound window.
# The caller holds the bench lock for the whole run:
#   timeout 1300 flock -w 60 /tmp/milan-bench.lock bash tools/run_bind.sh
# Recorders, all bounded by `timeout` and all started before the bind:
#   - tap capture of the DUT link on the capture server (as #117 Run B, tcpdump on the tap interface);
#   - capture of the controller host's own port, AVDECC ethertype only;
#   - console poll every 0.5 s (read-only allowlist): milan_status, CRFT_CTRL, CRFT_COUNT,
#     LWSRP_STATUS, ACMP_TALKER, CLKV_TUCNT, GPTP_DROPW, GPTP_DROPE;
#   - read-only GET_COUNTERS every 1 s: DUT STREAM_OUTPUT 1 (CRF) and 0 (AAF), peer STREAM_INPUT 8.
# Pre-flight: both captures listening and the console transcript growing, or no bind.
# The bind: crf_bind_window.py (the #117 tool, unchanged) on the controller host, 30 s pre,
# 720 s bound, 90 s post; it refuses unless the input reads unbound, and it unbinds at the
# window end, on SIGTERM/SIGINT and on any exception. It writes to a file on the controller
# host, so it completes and unbinds even if this build-box session dies.
set -u
PK=$REVIEWS/530-a237-packet
OUT=$PK/bench/run
mkdir -p "$OUT"
P=/dev/serial/by-id/<adapter>
SSH="ssh -o BatchMode=yes"
TAPIF=<MAC-derived-interface-name>
DUT=020000fffe000001; DMAC=02:00:00:00:00:01; PEER=3cc0c60102030000; PMAC=3c:c0:c6:01:02:03
PRE=30; WIN=720; POST=90
CAPMAX=1000; CONDUR=895; CTRDUR=920
ts() { date -u +%FT%T.%3NZ; }
tl() { echo "$1 $(ts)" >> "$OUT/timeline.txt"; }
echo "LOCK $(ts)"
echo "start_local $(ts) PRE=$PRE WIN=$WIN POST=$POST" > "$OUT/timeline.txt"
$SSH <bench-host-prefix>ubuntu-server "mkdir -p /tmp/a237 && sudo -n timeout $CAPMAX tcpdump -i $TAPIF -w /tmp/a237/tap-run.pcap" > "$OUT/tcpdump-tap.log" 2>&1 &
CAP=$!
$SSH <bench-host-prefix>pw1 "sudo -n timeout $CAPMAX tcpdump -i ens10 -w /tmp/a237/pw1-run.pcap ether proto 0x22f0" > "$OUT/tcpdump-pw1.log" 2>&1 &
CAP2=$!
timeout $((CONDUR + 30)) python3 $PK/tools/console_poll.py $P $OUT/console.txt $CONDUR 0.5 milan_status \
  'mem_read 0x90000750 4' 'mem_read 0x90000764 4' 'mem_read 0x90000694 4' 'mem_read 0x9000066c 4' \
  'mem_read 0x90000780 4' 'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4' > "$OUT/console-poll.stdout" 2>&1 &
CON=$!
tl recorders_started
sleep 6
S1=$(stat -c %s "$OUT/console.txt" 2>/dev/null || echo 0)
sleep 2
S2=$(stat -c %s "$OUT/console.txt" 2>/dev/null || echo 0)
if ! grep -q "listening on $TAPIF" "$OUT/tcpdump-tap.log" || ! grep -q "listening on ens10" "$OUT/tcpdump-pw1.log" || [ "$S2" -le "$S1" ]; then
  tl "PREFLIGHT_FAIL tap=$(grep -c listening "$OUT/tcpdump-tap.log") pw1=$(grep -c listening "$OUT/tcpdump-pw1.log") console=$S1->$S2"
  kill $CON 2>/dev/null
  $SSH <bench-host-prefix>ubuntu-server "sudo -n pkill -INT -f '^tcpdump -i $TAPIF -w /tmp/a237/tap-run\.pcap$'"
  $SSH <bench-host-prefix>pw1 "sudo -n pkill -INT -f '^tcpdump -i ens10 -w /tmp/a237/pw1-run\.pcap ether proto 0x22f0$'"
  wait
  echo "UNLOCK $(ts)"
  exit 2
fi
tl "preflight_ok console=$S1->$S2"
$SSH <bench-host-prefix>pw1 "sudo -n timeout $CTRDUR python3 /tmp/a237/a231_counters_poll.py ens10 $((CTRDUR - 20)) 1 \
  $DUT=$DMAC:6:1 $DUT=$DMAC:6:0 $PEER=$PMAC:5:8 > /tmp/a237/counters.jsonl 2>&1; echo CTR_RC=\$?" > "$OUT/counters-poll.rc" 2>&1 &
CTR=$!
sleep 10
tl bind_window_start
$SSH <bench-host-prefix>pw1 "sudo -n timeout -k 30 $((PRE + WIN + POST + 60)) python3 /tmp/a237/crf_bind_window.py ens10 $PRE $WIN $POST > /tmp/a237/bind.jsonl 2>&1; echo BIND_RC=\$?" > "$OUT/bind.rc" 2>&1
tl "bind_window_end rc=$(cat "$OUT/bind.rc" | tr '\n' ' ')"
sleep 20
$SSH <bench-host-prefix>ubuntu-server "sudo -n pkill -INT -f '^tcpdump -i $TAPIF -w /tmp/a237/tap-run\.pcap$'"; tl "tap_stop_rc=$?"
$SSH <bench-host-prefix>pw1 "sudo -n pkill -INT -f '^tcpdump -i ens10 -w /tmp/a237/pw1-run\.pcap ether proto 0x22f0$'"; tl "pw1_stop_rc=$?"
$SSH <bench-host-prefix>pw1 "sudo -n pkill -TERM -f '^python3 /tmp/a237/a231_counters_poll\.py '"; tl "ctr_stop_rc=$?"
wait $CAP; tl "capture_tap_rc=$?"
wait $CAP2; tl "capture_pw1_rc=$?"
wait $CTR; tl "counters_rc=$?"
wait $CON; tl "console_rc=$? (ends on its own after CONDUR)"
tl end_local
echo "UNLOCK $(ts)"
