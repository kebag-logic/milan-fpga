#!/usr/bin/env bash
# Lane B8 copy of lane B7's script: only the environment name (B8_ENV), the controller staging (/tmp/a521), the controller tool name (b8_ctl.py) and the raw root (/tmp/b8-a521/raw) differ.
# Identity gate under the bench lock (lane B6's identity_locked.sh, retargeted to the dev bbf704ec
# image). Read-only on the DUT (console CRCs of the AEM image, the BIOS ROM and the QSPI bitstream
# payload over the build's own sizes; NVM status; the QSPI AEM bytes of ENTITY, CONFIGURATION,
# CLOCK_SOURCE 0-2 and CLOCK_DOMAIN 0; the UART grader) and on the controller host (AECP
# READ_DESCRIPTOR of ENTITY 0, CONFIGURATION 0, STREAM_INPUT 0-1, STREAM_OUTPUT 0-1,
# CLOCK_SOURCE 0-3, CLOCK_DOMAIN 0, AVB_INTERFACE 0; GET_CLOCK_SOURCE; ADP discovery).
# CLOCK_SOURCE 3 is read to show the list ends at 3 sources (NO_SUCH_DESCRIPTOR expected).
# Lane B7 changes against B6: the CRC sizes come from the build (AEM 7,512 B, BIOS 53,588 B);
# the QSPI dumps add CLOCK_SOURCE and CLOCK_DOMAIN; the AECP walk adds the stream, clock and
# interface descriptors; the environment is B8_ENV and the controller staging /tmp/a521.
# usage: identity_b8.sh <packet_dir> <lane_worktree> [<out_subdir>]
# Lane B8 resume: the optional third argument names the packet subdirectory (default identity), so the
# gate after the power cycle writes beside the first one instead of over it.
set -u
. "${B8_ENV:?}"
P=$1; L=$2; D=${3:-identity}
mkdir -p "$P/$D"
timeout -k 5 420 flock -w 120 /tmp/milan-bench.lock bash -c '
set -u
P=$0; L=$1; D=$2
echo "LOCK $(date -u +%FT%T.%3NZ)"
timeout 200 python3 -B "$P/tools/console_read.py" "$DUT_CONSOLE" "$P/$D/console-identity.txt" \
  milan_status "crc 0x01400000 7512" milan_nvm "crc 0x00000000 53588" "crc 0x01000000 3825788" \
  "mem_read 0x01400110 312" "mem_read 0x01400248 106" "mem_read 0x01400620 264" "mem_read 0x01401340 82" \
  > "$P/$D/console-identity.stdout" 2>&1
echo "CONSOLE_RC=$?"
timeout 60 python3 -B "$L/scripts/baremetal_uart_smoke.py" --port "$DUT_CONSOLE" > "$P/$D/grader-identity.txt" 2>&1
echo "GRADER_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/a521" && \
timeout 30 scp -q "$P/tools/avdecc_ro.py" "$CTL_HOST:/tmp/a521/"
echo "STAGE_RC=$?"
R=""
for d in 00000000 00010000 00050000 00050001 00060000 00060001 000a0000 000a0001 000a0002 000a0003 00240000 00090000; do
  R="$R 0x0004 00000000$d"
done
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a521 && sha256sum *.py; sudo -n timeout 40 python3 -B avdecc_ro.py aem $CTL_IFACE \
  020000fffe000001 020000000001 $R 0x0017 00240000" > "$P/$D/identity-aecp.jsonl" 2>&1
echo "AECP_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a521 && sudo -n timeout 20 python3 -B avdecc_ro.py discover $CTL_IFACE 4" \
  > "$P/$D/adp-discover.jsonl" 2>&1
echo "ADP_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$L" "$D"
echo "LOCK_RC=$?"
