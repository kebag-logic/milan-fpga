#!/usr/bin/env bash
# Bench start census (issue 530, A258). Read-only. Run under the bench lock by the caller:
#   timeout 400 flock -w 60 /tmp/milan-bench.lock bash tools/run_start_census.sh
# Records: processes still running on the controller host and the capture server, the census
# (ACMP bind state on both ends + AEM settings reads, a237_census.sh with the A258 remote path)
# and a read-only console readback of the DUT.
set -u
PK=$MANAGEMENT/2026-09-23/530-a258; OUT=$PK/bench/start; mkdir -p $OUT
P=/dev/serial/by-id/<adapter>
SSH="ssh -o BatchMode=yes -o ConnectTimeout=15"
CTRL=<bench-host-prefix>pw1; CAPSRV=<bench-host-prefix>ubuntu-server
ts() { date -u +%FT%T.%3NZ; }
echo "LOCK $(ts)"
echo "start_local $(ts)" > $OUT/timeline.txt
for role in controller-host capture-server; do
  h=$CTRL; [ $role = capture-server ] && h=$CAPSRV
  timeout 60 $SSH $h "date -u +%FT%T.%NZ; uptime; echo '-- processes'; ps -eo pid,lstart,etime,args | grep -E 'tcpdump|crf_bind_window|counters_poll|avdecc_ro' | grep -v grep; echo '-- /tmp/a258'; ls -la --time-style=full-iso /tmp/a258 2>&1" > $OUT/procs-$role.txt 2>&1
  echo "procs_$role rc=$? $(ts)" >> $OUT/timeline.txt
done
echo "census_start $(ts)" >> $OUT/timeline.txt
timeout 200 $SSH $CTRL 'bash /tmp/a258/a258_census.sh' > $PK/bench/census-start.jsonl 2>&1
echo "census_end rc=$? $(ts)" >> $OUT/timeline.txt
timeout 90 python3 $PK/tools/console_read.py $P $OUT/console-start.txt milan_status 'mem_read 0x90000000 4' \
  'mem_read 0x90000004 4' 'mem_read 0x90000750 4' 'mem_read 0x90000764 4' 'mem_read 0x90000694 4' \
  'mem_read 0x90000698 4' 'mem_read 0x9000066c 4' 'mem_read 0x90000780 4' 'mem_read 0x90000788 4' \
  'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4' 'mem_read 0x90000774 4' 'mem_read 0x90000720 4' > $OUT/console-start.stdout 2>&1
echo "reader_rc=$? $(ts)" >> $OUT/timeline.txt
echo "end_local $(ts)" >> $OUT/timeline.txt
echo "UNLOCK $(ts)"
