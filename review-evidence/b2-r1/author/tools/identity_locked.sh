#!/usr/bin/env bash
# Identity gate under the bench lock: read-only console CRC readback, then the UART grader.
# usage: identity_locked.sh <packet_dir> <lane_worktree>; endpoints from B2_ENDPOINTS (private, not in the packet).
set -u
. "${B2_ENDPOINTS:?}"
P=$1; L=$2
timeout -k 5 200 flock -w 120 /tmp/milan-bench.lock bash -c '
echo "LOCK $(date -u +%FT%T.%3NZ)"
timeout 150 python3 -B "$0/tools/console_read.py" "$2" "$0/identity/console-identity.txt" milan_status mem_list "crc 0x00000000 53344" "crc 0x01000000 3825788" "crc 0x01400000 7352" milan_nvm "mem_read 0x90000110 4" "mem_read 0xf000181c 4" "mem_read 0x90000720 4" "mem_read 0x90000774 4" "mem_read 0x90000780 4" "mem_read 0x900008f8 4" "mem_read 0x9000071c 4" > "$0/identity/console-identity.stdout" 2>&1
echo "CONSOLE_RC=$?"
timeout 60 python3 -B "$1/scripts/baremetal_uart_smoke.py" --port "$2" > "$0/identity/grader-identity.txt" 2>&1
echo "GRADER_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$L" "$CONSOLE_PORT"
echo "LOCK_RC=$?"
