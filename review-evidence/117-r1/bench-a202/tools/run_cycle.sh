#!/usr/bin/env bash
# One GM loss/return cycle through the bench AVB switch's outlet (issue 117,
# A202, step 3). Runs in the foreground; every remote process is bounded by
# `timeout` and is stopped explicitly at the end.
#   tap capture on the DUT link, controller-host capture on switch port 8,
#   controller-host watcher (optionally holding one CRF binding), then under
#   the bench lock a 0.1 s console poll and the outlet off/hold/on sequence.
# usage: [PRE=20 HOLD=20 POST=260 BIND=0 PROOF=0] run_cycle.sh <n>
set -u
N=$1
PRE=${PRE:-20}; HOLD=${HOLD:-20}; POST=${POST:-260}; BIND=${BIND:-0}; PROOF=${PROOF:-0}; OUTLET=4
PK=$REVIEWS/117-a202-packet
OUT=$PK/bench/cycle$N
SSH="ssh -o BatchMode=yes -o StrictHostKeyChecking=no"
D=$((PRE + HOLD + POST))
mkdir -p "$OUT"
ts() { date -u +%FT%T.%3NZ; }
echo "start_local $(ts) N=$N PRE=$PRE HOLD=$HOLD POST=$POST BIND=$BIND PROOF=$PROOF OUTLET=$OUTLET" > $OUT/timeline.txt
for h in <bench-host-prefix>ubuntu-server <bench-host-prefix>pw1 <bench-host-prefix>pi; do timeout 40 python3 $PK/tools/clock_offset.py $h 25; done > $OUT/clock-before.jsonl 2>&1
$SSH <bench-host-prefix>ubuntu-server "sudo -n timeout $((D + 120)) tcpdump -i <MAC-derived-interface-name> -w /tmp/a202-c$N.pcap" > $OUT/tcpdump-tap.log 2>&1 &
CAP=$!
$SSH <bench-host-prefix>pw1 "sudo -n timeout $((D + 120)) tcpdump -i ens10 -w /tmp/a202/c$N-pw1.pcap" > $OUT/tcpdump-pw1.log 2>&1 &
CAP2=$!
WARGS=""
if [ "$BIND" = 1 ]; then WARGS="--bind --unbind-deadline 240"; fi
$SSH <bench-host-prefix>pw1 "sudo -n timeout -k 20 $((D + 420)) python3 /tmp/a202/a202_watch.py ens10 $((D + 110)) 1 $WARGS" > $OUT/pw1-watch.jsonl 2>&1 &
PW=$!
sleep 3
echo "locked_start_local $(ts)" >> $OUT/timeline.txt
timeout $((D + 150)) flock -w 60 /tmp/milan-bench.lock bash $PK/tools/cycle_locked.sh $OUT $D $PRE $HOLD $OUTLET $PROOF $BIND > $OUT/lock.txt 2>&1
echo "locked_rc=$? locked_end_local $(ts)" >> $OUT/timeline.txt
sleep 10
# stop the watcher (it unbinds on SIGTERM) and both captures
$SSH <bench-host-prefix>pw1 "sudo -n pkill -TERM -f '^python3 /tmp/a202/a202_watch\.py '" ; echo "watch_term_rc=$?" >> $OUT/timeline.txt
wait $PW; echo "pw1_watch_rc=$?" >> $OUT/timeline.txt
$SSH <bench-host-prefix>ubuntu-server "sudo -n pkill -INT -f '^tcpdump -i <MAC-derived-interface-name> -w /tmp/a202-c$N\.pcap$'"
$SSH <bench-host-prefix>pw1 "sudo -n pkill -INT -f '^tcpdump -i ens10 -w /tmp/a202/c$N-pw1\.pcap$'"
wait $CAP; echo "capture_tap_rc=$?" >> $OUT/timeline.txt
wait $CAP2; echo "capture_pw1_rc=$?" >> $OUT/timeline.txt
for h in <bench-host-prefix>ubuntu-server <bench-host-prefix>pw1 <bench-host-prefix>pi; do timeout 40 python3 $PK/tools/clock_offset.py $h 25; done > $OUT/clock-after.jsonl 2>&1
$SSH <bench-host-prefix>ubuntu-server "sudo -n chown alex /tmp/a202-c$N.pcap" && scp -q <bench-host-prefix>ubuntu-server:/tmp/a202-c$N.pcap $OUT/tap-c$N.pcap && \
  $SSH <bench-host-prefix>ubuntu-server "sha256sum /tmp/a202-c$N.pcap" > $OUT/tap-remote.sha256 && $SSH <bench-host-prefix>ubuntu-server "rm -f /tmp/a202-c$N.pcap"
echo "copied_tap_rc=$?" >> $OUT/timeline.txt
$SSH <bench-host-prefix>pw1 "sudo -n chown alex /tmp/a202/c$N-pw1.pcap" && scp -q <bench-host-prefix>pw1:/tmp/a202/c$N-pw1.pcap $OUT/pw1-c$N.pcap && \
  $SSH <bench-host-prefix>pw1 "sha256sum /tmp/a202/c$N-pw1.pcap" > $OUT/pw1-remote.sha256 && $SSH <bench-host-prefix>pw1 "rm -f /tmp/a202/c$N-pw1.pcap"
echo "copied_pw1_rc=$?" >> $OUT/timeline.txt
echo "end_local $(ts)" >> $OUT/timeline.txt
