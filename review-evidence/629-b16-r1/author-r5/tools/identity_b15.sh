#!/usr/bin/env bash
# Lane B15 identity gate under the bench lock: lane B10's identity_b10.sh with these changes.
# The environment is B15_ENV and the controller staging /tmp/a588. The console reads keep
# milan_status (CSR ID and VERSION), the AEM image CRC over its 7,512 bytes, milan_nvm and the
# QSPI AEM bytes of ENTITY, CONFIGURATION, CLOCK_SOURCE 0-2 and CLOCK_DOMAIN 0; they drop the
# BIOS ROM and bitstream payload CRCs, because this lane holds no build values for dev 5603c353
# to compare them with (the assignment's identity facts are the four ATDECC facts, the CSR ID,
# VERSION and the AEM CRC). The UART grader, the AECP descriptor walk and ADP are unchanged.
# Read-only on the DUT and the controller host.
# usage: identity_b15.sh <packet_dir> <lane_worktree> [<out_subdir>]
set -u
. "${B15_ENV:?}"
P=$1; L=$2; D=${3:-identity}
mkdir -p "$P/$D"
timeout -k 5 300 flock -w 120 /tmp/milan-bench.lock bash -c '
set -u
P=$0; L=$1; D=$2
echo "LOCK $(date -u +%FT%T.%3NZ)"
timeout 120 python3 -B "$P/tools/console_read.py" "$DUT_CONSOLE" "$P/$D/console-identity.txt" \
  milan_status "crc 0x01400000 7512" milan_nvm \
  "mem_read 0x01400110 312" "mem_read 0x01400248 106" "mem_read 0x01400620 264" "mem_read 0x01401340 82" \
  > "$P/$D/console-identity.stdout" 2>&1
echo "CONSOLE_RC=$?"
timeout 60 python3 -B "$L/scripts/baremetal_uart_smoke.py" --port "$DUT_CONSOLE" > "$P/$D/grader-identity.txt" 2>&1
echo "GRADER_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/a588" && \
timeout 30 scp -q "$P/tools/avdecc_ro.py" "$CTL_HOST:/tmp/a588/"
echo "STAGE_RC=$?"
R=""
for d in 00000000 00010000 00050000 00050001 00060000 00060001 000a0000 000a0001 000a0002 000a0003 00240000 00090000; do
  R="$R 0x0004 00000000$d"
done
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a588 && sha256sum *.py; sudo -n timeout 40 python3 -B avdecc_ro.py aem $CTL_IFACE \
  020000fffe000001 020000000001 $R 0x0017 00240000" > "$P/$D/identity-aecp.jsonl" 2>&1
echo "AECP_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a588 && sudo -n timeout 20 python3 -B avdecc_ro.py discover $CTL_IFACE 4" \
  > "$P/$D/adp-discover.jsonl" 2>&1
echo "ADP_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$L" "$D"
echo "LOCK_RC=$?"
