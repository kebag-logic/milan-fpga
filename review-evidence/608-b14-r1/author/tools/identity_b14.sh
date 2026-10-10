#!/usr/bin/env bash
# Lane B14 identity gate under the bench lock, read-only (lane B8's identity_b8.sh, reduced).
# DUT console: milan_status (CSR ID, VERSION), CRC of the QSPI AEM bytes and of the RAM copy over
# the flashed 7,512 B, milan_nvm. SoC board console: soc_check.py. Controller host: AECP
# READ_DESCRIPTOR of ENTITY 0, CONFIGURATION 0, STREAM_INPUT 0-1, STREAM_OUTPUT 0-1,
# CLOCK_DOMAIN 0, AVB_INTERFACE 0, GET_CLOCK_SOURCE, ADP discovery (4 s).
# usage: identity_b14.sh <out_dir>; endpoints from B14_ENV (private, outside the packet).
set -u
. "${B14_ENV:?}"
D=$1; T=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$D"
echo "LOCK_REQUEST $(date -u +%FT%T.%3NZ)"
timeout -k 5 300 flock -w 120 /tmp/milan-bench.lock bash -c '
set -u
D=$0; T=$1
echo "LOCK $(date -u +%FT%T.%3NZ)"
timeout 150 python3 -B "$T/console_read.py" "$DUT_CONSOLE" "$D/console-identity.txt" \
  milan_status "crc 0x01400000 7512" "crc 0x7f700000 7512" milan_nvm > "$D/console-identity.stdout" 2>&1
echo "CONSOLE_RC=$?"
timeout 20 python3 -B "$T/soc_check.py" "$SOC_CONSOLE" "$D/soc-check.txt"
echo "SOC_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/608-b14" && \
timeout 30 scp -q "$T/avdecc_ro.py" "$CTL_HOST:/tmp/608-b14/"
echo "STAGE_RC=$?"
R=""
for d in 00000000 00010000 00050000 00050001 00060000 00060001 00240000 00090000; do R="$R 0x0004 00000000$d"; done
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/608-b14 && sha256sum avdecc_ro.py && sudo -n timeout 40 python3 -B avdecc_ro.py aem $CTL_IFACE 020000fffe000001 020000000001 $R 0x0017 00240000" > "$D/identity-aecp.jsonl" 2>&1
echo "AECP_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/608-b14 && sudo -n timeout 20 python3 -B avdecc_ro.py discover $CTL_IFACE 4" > "$D/adp-discover.jsonl" 2>&1
echo "ADP_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$D" "$T"
echo "LOCK_RC=$? $(date -u +%FT%T.%3NZ)"
