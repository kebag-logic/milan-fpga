#!/usr/bin/env bash
# One la_avdecc enumeration in the #529 step-2 shape (issue 387, A249). Run under the bench lock:
#   timeout 400 flock -w 60 /tmp/milan-bench.lock bash tools/run_enum.sh <tag>
# Controller host only: a capture of its own port (AVDECC ethertype), the 2026-09-08
# counters probe on the DUT and on the reference peer, then the #117 enumerator binary
# for 40 s. Same binaries, arguments and order as #529 step 2; only the /tmp path differs.
set -u
TAG=$1
PK=$MANAGEMENT/2026-09-23/387-a249; OUT=$PK/bench/$TAG; mkdir -p $OUT
PROBE=$WORKSPACE_HOME/milan-bench/2026-09-08/controller-probe/target-counters-probe
ts() { date -u +%FT%T.%3NZ; }
echo "LOCK $(ts)" > $OUT/lock.txt
echo "start_local $(ts)" > $OUT/timeline.txt
ssh -o BatchMode=yes <bench-host-prefix>pw1 "mkdir -p /tmp/a249/enum-$TAG; rm -f /tmp/a249/enum-$TAG/*.json; sudo -n timeout 170 tcpdump -i ens10 -w /tmp/a249/$TAG.pcap ether proto 0x22f0" > $OUT/tcpdump.log 2>&1 &
CAP=$!
sleep 3
for e in 020000fffe000001 3cc0c60102030000; do
  echo "probe_$e start $(ts)" >> $OUT/timeline.txt
  ssh -o BatchMode=yes <bench-host-prefix>pw1 "sudo -n timeout --signal=TERM 35 $PROBE ens10 $e 20; echo PROBE_RC=\$?" > $OUT/counters-probe-$e.log 2>&1
done
echo "enum start $(ts)" >> $OUT/timeline.txt
ssh -o BatchMode=yes <bench-host-prefix>pw1 "sudo -n timeout --signal=TERM 70 /tmp/a249/a200_enum ens10 40 /tmp/a249/enum-$TAG; echo ENUM_RC=\$?; sudo -n chown -R alex /tmp/a249/enum-$TAG" > $OUT/a200-enum.log 2>&1
echo "enum end $(ts)" >> $OUT/timeline.txt
wait $CAP; echo "capture_rc=$?" >> $OUT/timeline.txt
echo "UNLOCK $(ts)" >> $OUT/lock.txt
