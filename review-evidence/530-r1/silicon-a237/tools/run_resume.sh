#!/usr/bin/env bash
# Bench resume check after the 07:30-07:46 network outage (issue 530, A237). Read-only.
# Run under the bench lock by the caller:
#   timeout 400 flock -w 60 /tmp/milan-bench.lock bash tools/run_resume.sh
# Records: processes still running on the controller host and the capture server,
# leftover files in /tmp/a237 on both, the census (ACMP bind state on both ends +
# AEM settings reads) and a read-only console readback of the DUT.
set -u
PK=$REVIEWS/530-a237-packet; OUT=$PK/bench/resume; mkdir -p $OUT
P=/dev/serial/by-id/<adapter>
SSH="ssh -o BatchMode=yes -o ConnectTimeout=15"
ts() { date -u +%FT%T.%3NZ; }
echo "LOCK $(ts)"
echo "start_local $(ts)" > $OUT/timeline.txt
for h in <bench-host-prefix>pw1 <bench-host-prefix>ubuntu-server; do
  timeout 60 $SSH $h "hostname; date -u +%FT%T.%NZ; uptime; echo '-- processes'; ps -eo pid,lstart,etime,args | grep -E 'tcpdump|crf_bind_window|a231_counters_poll|avdecc_ro|a237' | grep -v grep; echo '-- /tmp/a237'; ls -la --time-style=full-iso /tmp/a237 2>&1" > $OUT/procs-$h.txt 2>&1
  echo "procs_$h rc=$? $(ts)" >> $OUT/timeline.txt
done
timeout 200 $SSH <bench-host-prefix>pw1 'bash /tmp/a237/a237_census.sh' > $OUT/census-resume.jsonl 2>&1
echo "census rc=$? $(ts)" >> $OUT/timeline.txt
timeout 90 python3 $PK/tools/console_read.py $P $OUT/console-resume.txt milan_status 'mem_read 0x90000000 4' \
  'mem_read 0x90000004 4' 'mem_read 0x90000750 4' 'mem_read 0x90000764 4' 'mem_read 0x90000694 4' \
  'mem_read 0x90000698 4' 'mem_read 0x9000066c 4' 'mem_read 0x90000780 4' 'mem_read 0x90000788 4' \
  'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4' 'mem_read 0x90000774 4' 'mem_read 0x90000720 4' > $OUT/console-resume.stdout 2>&1
echo "reader_rc=$? $(ts)" >> $OUT/timeline.txt
echo "end_local $(ts)" >> $OUT/timeline.txt
echo "UNLOCK $(ts)"
