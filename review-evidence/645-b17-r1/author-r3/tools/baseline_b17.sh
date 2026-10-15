#!/usr/bin/env bash
# Lane B17 copy of lane B15's baseline_b15.sh. Changes: the environment is B17_ENV and the controller
# staging /tmp/a619; the SoC board is checked on its serial console with one empty line and, at a root
# prompt only, the board script's read-only `status` verb (soc_check_b17.py), instead of B15's SSH
# health reads; the descriptor surveys are dropped (the census carries the restore set); the host view
# and the SoC transcript go to the private directory (PRIV), because they name adapters and the board.
# One read-only state snapshot under the bench lock: DUT console reads, the controller's census,
# GET_COUNTERS, the controller and host views. Tag end* removes the controller staging afterwards.
# usage: baseline_b17.sh <packet_dir> <tag>
set -u
. "${B17_ENV:?}"
: "${PRIV:?}"
P=$1; T=$2
timeout -k 5 240 flock -w 120 /tmp/milan-bench.lock bash -c '
set -u
P=$0; T=$1
echo "LOCK $(date -u +%FT%T.%3NZ)"
timeout 20 python3 -B "$P/tools/soc_check_b17.py" "$SOC_CONSOLE" "$PRIV/soc-$T.txt"
echo "SOC_RC=$?"
timeout 60 python3 -B "$P/tools/console_read.py" "$DUT_CONSOLE" "$P/restore/dut-$T.txt" milan_status milan_nvm \
  "mem_read 0x90000654 12" "mem_read 0x90000660 20" "mem_read 0x90000694 8" "mem_read 0x900006a4 4" \
  "mem_read 0x900006cc 12" "mem_read 0x900006dc 4" "mem_read 0x90000900 4" "mem_read 0x900008d4 12" \
  "mem_read 0x90000680 36" "mem_read 0x900006e0 16" "mem_read 0x90000738 4" "mem_read 0x90000748 8" \
  "mem_read 0x900008f8 8" "mem_read 0x900008e0 8" > /dev/null 2>&1
echo "DUT_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/a619" && \
timeout 30 scp -q "$P/tools/avdecc_ro.py" "$P/tools/b8_ctl.py" "$CTL_HOST:/tmp/a619/"
echo "STAGE_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a619 && \
  sudo -n timeout 40 python3 -B b8_ctl.py census $CTL_IFACE $PEER_EID $PEER_MAC" > "$P/restore/census-$T.jsonl" 2> "$P/restore/census-$T.err"
echo "CENSUS_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a619 && \
  sudo -n timeout 40 python3 -B b8_ctl.py counters $CTL_IFACE $PEER_EID $PEER_MAC" > "$P/restore/counters-$T.jsonl" 2> "$P/restore/counters-$T.err"
echo "COUNTERS_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "pgrep -a ptp4l; echo PGREP_RC=\$?; \
  pgrep -af '"'"'[b]8_ctl'"'"'; echo PGREP2_RC=\$?; cd /tmp/a619 && sha256sum *.py; ls -la /tmp/a619" > "$P/restore/controller-$T.txt" 2>&1
echo "CTL_RC=$?"
{ cat /proc/asound/cards; for s in /proc/asound/card*/pcm*/sub0/status; do echo "$s: $(head -1 $s)"; done; ip -br link; ip -4 -br addr; ls -l /dev/serial/by-id/; } > "$PRIV/host-$T.txt" 2>&1
echo "HOST_RC=$?"
case "$T" in end*) true;; *) false;; esac && {
  timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "rm -rf /tmp/a619; ls -d /tmp/a619 2>&1; pgrep -af '"'"'[b]8_ctl'"'"'; echo PGREP_RC=\$?" \
    > "$P/restore/controller-cleanup.txt" 2>&1
  echo "CLEANUP_RC=$?"
}
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$T"
echo "LOCK_RC=$?"
