#!/usr/bin/env bash
# Identity gate and controller preflight under the bench lock. Read-only on the DUT
# (console CRC and descriptor readback, the UART grader) and on the controller host
# (AECP READ_DESCRIPTOR, ADP discovery, interface, PHC and timestamping state).
# usage: identity_locked.sh <packet_dir> <lane_worktree>
# Endpoints come from the private file named by B4_ENV (not in this packet).
set -u
. "${B4_ENV:?}"
P=$1; L=$2
timeout -k 5 420 flock -w 120 /tmp/milan-bench.lock bash -c '
set -u
P=$0; L=$1
echo "LOCK $(date -u +%FT%T.%3NZ)"
timeout 200 python3 -B "$P/tools/console_read.py" "$DUT_CONSOLE" "$P/identity/console-identity.txt" \
  milan_status "crc 0x01400000 7352" milan_nvm "crc 0x00000000 53344" "crc 0x01000000 3825788" \
  "mem_read 0x01400110 312" "mem_read 0x01400248 106" > "$P/identity/console-identity.stdout" 2>&1
echo "CONSOLE_RC=$?"
timeout 60 python3 -B "$L/scripts/baremetal_uart_smoke.py" --port "$DUT_CONSOLE" > "$P/identity/grader-identity.txt" 2>&1
echo "GRADER_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/a468" && \
timeout 30 scp -q "$P/tools/avdecc_ro.py" "$P/tools/avdecc_rw.py" "$P/tools/with_gptp.py" \
  "$P/tools/aaf_talker.py" "$CTL_HOST:/tmp/a468/"
echo "STAGE_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a468 && sha256sum *.py; \
  ip -br link; sudo -n ethtool -T $CTL_IFACE; pgrep -a ptp4l; echo PGREP_RC=\$?; \
  sudo -n $HWSTAMP_CTL -i $CTL_IFACE; echo HWSTAMP_RC=\$?; \
  sudo -n $PHC_CTL $CTL_IFACE freq cmp; echo PHC_RC=\$?" > "$P/identity/controller-preflight.txt" 2>&1
echo "CTL_PREFLIGHT_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a468 && sudo -n timeout 20 python3 -B avdecc_ro.py aem $CTL_IFACE \
  020000fffe000001 020000000001 0x0004 0000000000000000 0x0004 0000000000010000" > "$P/identity/identity-aecp.jsonl" 2>&1
echo "AECP_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a468 && sudo -n timeout 20 python3 -B avdecc_ro.py discover $CTL_IFACE 4" \
  > "$P/identity/adp-discover.jsonl" 2>&1
echo "ADP_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$L"
echo "LOCK_RC=$?"
