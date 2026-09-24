#!/usr/bin/env bash
# Identity and gPTP window (issue 530, A237). Run under the bench lock by the caller:
#   timeout 300 flock -w 60 /tmp/milan-bench.lock bash tools/run_identity_gptp.sh
# Console: read-only commands only (console_read.py / console_poll.py allowlist).
# Controller host: avdecc_ro.py watch (GET_AVB_INFO / GET_AS_PATH), read-only.
set -u
PK=$REVIEWS/530-a237-packet
P=/dev/serial/by-id/<adapter>
ts() { date -u +%FT%T.%3NZ; }
echo "LOCK_ACQUIRED $(ts)"
timeout 150 python3 $PK/tools/console_read.py $P $PK/identity/console-identity.txt milan_status mem_list \
  'crc 0x00000000 52200' 'crc 0x01000000 3825788' 'crc 0x01400000 7352' milan_status \
  'mem_read 0x90000000 4' 'mem_read 0x90000004 4' 'mem_read 0x90000750 4' 'mem_read 0x90000764 4' \
  'mem_read 0x90000694 4' 'mem_read 0x90000698 4' 'mem_read 0x9000066c 4' 'mem_read 0x90000780 4' \
  'mem_read 0x90000788 4' 'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4' 'mem_read 0x90000774 4' \
  'mem_read 0x90000720 4' > $PK/identity/console-identity.stdout 2>&1
echo "READER_RC=$? $(ts)"
timeout 60 python3 $PK/tools/baremetal_uart_smoke.py --port $P > $PK/identity/uart-smoke-identity.log 2>&1
echo "SMOKE_RC=$? $(ts)"
OUT=$PK/bench/gptp; mkdir -p $OUT
echo "start_local $(ts)" > $OUT/timeline.txt
timeout 90 python3 $PK/tools/console_poll.py $P $OUT/console.txt 60 5 milan_status 'mem_read 0x90000780 4' \
  'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4' 'mem_read 0x90000774 4' 'mem_read 0x90000720 4' \
  'mem_read 0x90000750 4' 'mem_read 0x90000764 4' 'mem_read 0x90000694 4' > $OUT/console-poll.stdout 2>&1 &
CON=$!
timeout 120 ssh -o BatchMode=yes <bench-host-prefix>pw1 "sudo -n timeout 80 python3 /tmp/a237/avdecc_ro.py watch ens10 60 5 020000fffe000001=02:00:00:00:00:01 3cc0c60102030000=3c:c0:c6:01:02:03" > $OUT/pw1-watch.jsonl 2>&1
echo "pw1_rc=$?" >> $OUT/timeline.txt
wait $CON; echo "console_rc=$?" >> $OUT/timeline.txt
echo "end_local $(ts)" >> $OUT/timeline.txt
echo "LOCK_RELEASE $(ts)"
