#!/usr/bin/env bash
# gPTP lock and steady-state soak (issue 387, A249). The caller holds the bench lock for the
# whole run:
#   timeout 1400 flock -w 60 /tmp/milan-bench.lock bash tools/run_soak.sh
# Recorders, all bounded by `timeout`:
#   - tap capture of the DUT link on the capture server (tcpdump on the tap interface, as #117/#530);
#   - capture of the controller host's own port, AVDECC ethertype only;
#   - console poll every 1 s (read-only allowlist): milan_status (GM, parent, peer delay, path,
#     CLKV_STAT = tu/sync/holdover/asCapable, PHC time), CLKV_TUCNT, ASP_CMD, GPTP_DROPW,
#     GPTP_DROPE, RST_EPOCH, LINKG_STAT;
#   - controller-host GET_AVB_INFO / GET_AS_PATH every 1 s on the DUT and the reference peer;
#   - controller-host GET_COUNTERS every 1 s: DUT STREAM_OUTPUT 0 and 1 (TIMESTAMP_UNCERTAIN),
#     DUT AVB_INTERFACE 0 (GPTP_GM_CHANGED), DUT CLOCK_DOMAIN 0, peer AVB_INTERFACE 0.
# The UART grader runs before and after the poll. Nothing is bound and nothing is written.
set -u
PK=$MANAGEMENT/2026-09-23/387-a249
OUT=$PK/bench/soak
mkdir -p "$OUT"
P=/dev/serial/by-id/<adapter>
SSH="ssh -o BatchMode=yes"
TAPIF=<MAC-derived-interface-name>
DUT=020000fffe000001; DMAC=02:00:00:00:00:01; PEER=3cc0c60102030000; PMAC=3c:c0:c6:01:02:03
SOAK=${SOAK:-900}
CAPMAX=$((SOAK + 200))
ts() { date -u +%FT%T.%3NZ; }
tl() { echo "$1 $(ts)" >> "$OUT/timeline.txt"; }
echo "LOCK $(ts)"
echo "start_local $(ts) SOAK=$SOAK" > "$OUT/timeline.txt"
$SSH <bench-host-prefix>ubuntu-server "mkdir -p /tmp/a249 && sudo -n timeout $CAPMAX tcpdump -i $TAPIF -w /tmp/a249/tap-soak.pcap" > "$OUT/tcpdump-tap.log" 2>&1 &
CAP=$!
$SSH <bench-host-prefix>pw1 "sudo -n timeout $CAPMAX tcpdump -i ens10 -w /tmp/a249/pw1-soak.pcap ether proto 0x22f0" > "$OUT/tcpdump-pw1.log" 2>&1 &
CAP2=$!
sleep 3
tl grader_pre_start
timeout 60 python3 $PK/tools/baremetal_uart_smoke.py --port $P > "$OUT/uart-smoke-pre.log" 2>&1
tl "grader_pre_rc=$?"
timeout $((SOAK + 60)) python3 $PK/tools/console_poll.py $P "$OUT/console.txt" $SOAK 1 milan_status \
  'mem_read 0x90000780 4' 'mem_read 0x900007e4 4' 'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4' \
  'mem_read 0x90000720 4' 'mem_read 0x90000774 4' > "$OUT/console-poll.stdout" 2>&1 &
CON=$!
tl console_started
$SSH <bench-host-prefix>pw1 "sudo -n timeout $((SOAK + 30)) python3 /tmp/a249/avdecc_ro.py watch ens10 $SOAK 1 $DUT=$DMAC $PEER=$PMAC > /tmp/a249/watch.jsonl 2>&1; echo WATCH_RC=\$?" > "$OUT/watch.rc" 2>&1 &
WAT=$!
$SSH <bench-host-prefix>pw1 "sudo -n timeout $((SOAK + 30)) python3 /tmp/a249/a231_counters_poll.py ens10 $SOAK 1 \
  $DUT=$DMAC:6:0 $DUT=$DMAC:6:1 $DUT=$DMAC:9:0 $DUT=$DMAC:0x24:0 $PEER=$PMAC:9:0 > /tmp/a249/counters.jsonl 2>&1; echo CTR_RC=\$?" > "$OUT/counters.rc" 2>&1 &
CTR=$!
tl pollers_started
sleep 8
S1=$(stat -c %s "$OUT/console.txt" 2>/dev/null || echo 0)
sleep 2
S2=$(stat -c %s "$OUT/console.txt" 2>/dev/null || echo 0)
PRE_TAP=$(grep -c "listening on $TAPIF" "$OUT/tcpdump-tap.log")
PRE_PW1=$(grep -c "listening on ens10" "$OUT/tcpdump-pw1.log")
if [ "$PRE_TAP" -lt 1 ] || [ "$PRE_PW1" -lt 1 ] || [ "$S2" -le "$S1" ]; then
  tl "PREFLIGHT_WARN tap=$PRE_TAP pw1=$PRE_PW1 console=$S1->$S2 (recorded; the soak is passive, so it continues)"
else
  tl "preflight_ok tap=$PRE_TAP pw1=$PRE_PW1 console=$S1->$S2"
fi
wait $CON; tl "console_rc=$?"
wait $WAT; tl "watch_rc=$? $(tr '\n' ' ' < "$OUT/watch.rc")"
wait $CTR; tl "counters_rc=$? $(tr '\n' ' ' < "$OUT/counters.rc")"
tl grader_post_start
timeout 60 python3 $PK/tools/baremetal_uart_smoke.py --port $P > "$OUT/uart-smoke-post.log" 2>&1
tl "grader_post_rc=$?"
timeout 60 python3 $PK/tools/console_read.py $P "$OUT/console-end.txt" milan_status 'mem_read 0x9000077c 4' \
  'mem_read 0x90000780 4' 'mem_read 0x900007e4 4' 'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4' \
  'mem_read 0x90000720 4' 'mem_read 0x90000774 4' 'mem_read 0x90000750 4' > "$OUT/console-end.stdout" 2>&1
tl "console_end_rc=$?"
sleep 5
$SSH <bench-host-prefix>ubuntu-server "sudo -n pkill -INT -f '^tcpdump -i $TAPIF -w /tmp/a249/tap-soak\.pcap$'"; tl "tap_stop_rc=$?"
$SSH <bench-host-prefix>pw1 "sudo -n pkill -INT -f '^tcpdump -i ens10 -w /tmp/a249/pw1-soak\.pcap ether proto 0x22f0$'"; tl "pw1_stop_rc=$?"
wait $CAP; tl "capture_tap_rc=$?"
wait $CAP2; tl "capture_pw1_rc=$?"
tl end_local
echo "UNLOCK $(ts)"
