#!/usr/bin/env bash
# Step 2 (issue 529, A231), recorded verbatim as run at 03:16:39 build-box UTC from the
# build box (PK, OUT and PROBE set as below; the whole block ran inside
# timeout 400 flock -w 60 /tmp/milan-bench.lock bash -c "...", with the inner \$ escapes
# resolved as shown here).
PK=$MANAGEMENT/2026-09-23/529-a231; OUT=$PK/bench/step2; mkdir -p $OUT; PROBE=$WORKSPACE_HOME/milan-bench/2026-09-08/controller-probe/target-counters-probe
echo LOCK $(date -u +%FT%T.%3NZ) > $OUT/lock.txt
echo start_local $(date -u +%FT%T.%3NZ) > $OUT/timeline.txt
ssh -o BatchMode=yes <bench-host-prefix>pw1 'mkdir -p /tmp/a231/enum-step2; sudo -n timeout 170 tcpdump -i ens10 -w /tmp/a231/step2.pcap ether proto 0x22f0' > $OUT/tcpdump.log 2>&1 &
CAP=$!
sleep 3
for e in 020000fffe000001 3cc0c60102030000; do
  echo probe_$e start $(date -u +%FT%T.%3NZ) >> $OUT/timeline.txt
  ssh -o BatchMode=yes <bench-host-prefix>pw1 "sudo -n timeout --signal=TERM 35 $PROBE ens10 $e 20; echo PROBE_RC=\$?" > $OUT/counters-probe-$e.log 2>&1
done
echo enum start $(date -u +%FT%T.%3NZ) >> $OUT/timeline.txt
ssh -o BatchMode=yes <bench-host-prefix>pw1 'rm -f /tmp/a231/enum-step2/*.json; sudo -n timeout --signal=TERM 70 /tmp/a231/a200_enum ens10 40 /tmp/a231/enum-step2; echo ENUM_RC=$?; sudo -n chown -R alex /tmp/a231/enum-step2' > $OUT/a200-enum.log 2>&1
echo enum end $(date -u +%FT%T.%3NZ) >> $OUT/timeline.txt
wait $CAP; echo capture_rc=$? >> $OUT/timeline.txt
echo UNLOCK $(date -u +%FT%T.%3NZ) >> $OUT/lock.txt
# after the lock was released:
ssh -o BatchMode=yes <bench-host-prefix>pw1 'sudo -n chown alex /tmp/a231/step2.pcap; sha256sum /tmp/a231/step2.pcap /tmp/a231/enum-step2/*.json' | tee $OUT/remote-sha256.txt
scp -q <bench-host-prefix>pw1:/tmp/a231/step2.pcap $OUT/pw1-step2.pcap; scp -q '<bench-host-prefix>pw1:/tmp/a231/enum-step2/*.json' $OUT/
