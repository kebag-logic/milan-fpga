#!/usr/bin/env bash
# Run C (issue 117, A200): controller conformance from the controller host (step 5).
# Tap capture while the pinned la_avdecc counters probe runs against the DUT and,
# for parity, the reference peer; then a full la_avdecc discovery and enumeration.
set -u
PK=$REVIEWS/117-a200-packet
OUT=$PK/bench/runC
mkdir -p "$OUT"
echo "start_local $(date -u +%FT%T.%3NZ)" > "$OUT/timeline.txt"
ssh -o BatchMode=yes <bench-host-prefix>ubuntu-server "sudo -n timeout 100 tcpdump -i <MAC-derived-interface-name> -w /tmp/a200-runC.pcap" > "$OUT/tcpdump.log" 2>&1 &
CAP=$!
sleep 3
PROBE=$WORKSPACE_HOME/milan-bench/2026-09-08/controller-probe/target-counters-probe
for e in 020000fffe000001 3cc0c60102030000; do
  echo "probe_$e start $(date -u +%FT%T.%3NZ)" >> "$OUT/timeline.txt"
  ssh -o BatchMode=yes <bench-host-prefix>pw1 "sudo -n timeout --signal=TERM 35 $PROBE ens10 $e 20; echo PROBE_RC=\$?" > "$OUT/counters-probe-$e.log" 2>&1
done
echo "enum start $(date -u +%FT%T.%3NZ)" >> "$OUT/timeline.txt"
ssh -o BatchMode=yes <bench-host-prefix>pw1 "rm -f /tmp/a200/enum/*.json; sudo -n timeout --signal=TERM 70 /tmp/a200/a200_enum ens10 40 /tmp/a200/enum; echo ENUM_RC=\$?; sudo -n chown -R alex /tmp/a200/enum" > "$OUT/a200-enum.log" 2>&1
echo "enum end $(date -u +%FT%T.%3NZ)" >> "$OUT/timeline.txt"
wait $CAP; echo "capture_rc=$?" >> "$OUT/timeline.txt"
ssh -o BatchMode=yes <bench-host-prefix>ubuntu-server 'sudo -n chown alex /tmp/a200-runC.pcap' && scp -q <bench-host-prefix>ubuntu-server:/tmp/a200-runC.pcap "$OUT/tap-runC.pcap"
scp -q '<bench-host-prefix>pw1:/tmp/a200/enum/*.json' "$OUT/"
echo "copied_rc=$? end_local $(date -u +%FT%T.%3NZ)" >> "$OUT/timeline.txt"
