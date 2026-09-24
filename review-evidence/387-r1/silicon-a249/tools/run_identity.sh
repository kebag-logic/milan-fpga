#!/usr/bin/env bash
# Identity and start census (issue 387, A249). Run under the bench lock by the caller:
#   timeout 400 flock -w 60 /tmp/milan-bench.lock bash tools/run_identity.sh
# Console: read-only commands only (console_read.py allowlist), then the UART grader.
# Controller host: the binding census (read-only ACMP state queries and AEM reads).
set -u
PK=$MANAGEMENT/2026-09-23/387-a249
P=/dev/serial/by-id/<adapter>
ts() { date -u +%FT%T.%3NZ; }
echo "LOCK_ACQUIRED $(ts)"
timeout 150 python3 $PK/tools/console_read.py $P $PK/identity/console-identity.txt milan_status mem_list \
  'crc 0x00000000 52200' 'crc 0x01000000 3825788' 'crc 0x01400000 7352' milan_status \
  'mem_read 0x90000000 4' 'mem_read 0x90000004 4' 'mem_read 0x9000077c 4' 'mem_read 0x90000780 4' \
  'mem_read 0x900007e4 4' 'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4' 'mem_read 0x900007f0 4' \
  'mem_read 0x900006e4 4' 'mem_read 0x90000774 4' 'mem_read 0x90000720 4' 'mem_read 0x90000750 4' \
  'mem_read 0x90000764 4' 'mem_read 0x90000788 4' > $PK/identity/console-identity.stdout 2>&1
echo "READER_RC=$? $(ts)"
timeout 60 python3 $PK/tools/baremetal_uart_smoke.py --port $P > $PK/identity/uart-smoke-identity.log 2>&1
echo "SMOKE_RC=$? $(ts)"
echo "CENSUS_START $(ts)"
timeout 200 ssh -o BatchMode=yes <bench-host-prefix>pw1 'bash /tmp/a249/a249_census.sh' > $PK/bench/census-start.jsonl 2>&1
echo "CENSUS_RC=$? $(ts)"
echo "LOCK_RELEASE $(ts)"
