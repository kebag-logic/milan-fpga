#!/usr/bin/env bash
# Identity (03:14:10) and gPTP window (03:15:07), issue 529, A231, recorded verbatim as run.
PK=$MANAGEMENT/2026-09-23/529-a231
P=/dev/serial/by-id/<adapter>
git -C $LANES/trusted-dev-20260924-50e78097 ls-remote origin refs/heads/dev > $PK/identity/origin-dev.txt
timeout 200 flock -w 60 /tmp/milan-bench.lock bash -c "echo LOCK_ACQUIRED \$(date -u +%FT%T.%3NZ); timeout 120 python3 $PK/tools/console_read.py $P $PK/identity/console-identity.txt milan_status mem_list 'crc 0x00000000 52200' 'crc 0x01000000 3825788' 'crc 0x01400000 7352' milan_status 'mem_read 0x90000000 4' 'mem_read 0x90000004 4' > $PK/identity/console-identity.stdout 2>&1; echo READER_RC=\$?; timeout 60 python3 $LANES/trusted-dev-20260924-50e78097/scripts/baremetal_uart_smoke.py --port $P > $PK/identity/uart-smoke-identity.log 2>&1; echo SMOKE_RC=\$?; echo LOCK_RELEASE \$(date -u +%FT%T.%3NZ)" > $PK/identity/lock-window.txt 2>&1
python3 $PK/tools/expected_crc.py $WORKSPACE_HOME/litex-milan/work/build_ax7101_{asl,eppo,eto}_tdm8dev50e78097 $WORKSPACE_HOME/litex-milan/work/build_ax7101_asl_tdm8devede8d48e > $PK/identity/expected-crc.txt
python3 $PK/tools/a231_clock_offset.py <bench-host-prefix>pw1 15 > $PK/bench/clock-offset-start.txt 2>&1
ssh -o BatchMode=yes <bench-host-prefix>pw1 'sudo -n timeout 15 python3 /tmp/a231/avdecc_ro.py discover ens10 6' > $PK/bench/discover-start.jsonl 2>&1
OUT=$PK/bench/gptp; mkdir -p $OUT; echo "start_local $(date -u +%FT%T.%3NZ)" > $OUT/timeline.txt
timeout 150 flock -w 60 /tmp/milan-bench.lock bash -c "echo LOCK \$(date -u +%FT%T.%3NZ); timeout 90 python3 $PK/tools/console_poll.py $P $OUT/console.txt 60 5 milan_status 'mem_read 0x90000780 4' 'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4' 'mem_read 0x90000774 4' 'mem_read 0x90000720 4' 'mem_read 0x900006f4 4' 'mem_read 0x90000750 4' 'mem_read 0x90000764 4'; echo POLL_RC=\$?; echo UNLOCK \$(date -u +%FT%T.%3NZ)" > $OUT/lock.txt 2>&1 &
CON=$!
timeout 120 ssh -o BatchMode=yes <bench-host-prefix>pw1 "sudo -n timeout 80 python3 /tmp/a231/avdecc_ro.py watch ens10 60 5 020000fffe000001=02:00:00:00:00:01 3cc0c60102030000=3c:c0:c6:01:02:03" > $OUT/pw1-watch.jsonl 2>&1; echo "pw1_rc=$?" >> $OUT/timeline.txt
wait $CON; echo "console_rc=$?" >> $OUT/timeline.txt; echo "end_local $(date -u +%FT%T.%3NZ)" >> $OUT/timeline.txt
# census before (03:16:15): ssh -o BatchMode=yes <bench-host-prefix>pw1 'bash /tmp/a231/a231_census.sh' > $PK/bench/census-start.jsonl
