#!/usr/bin/env bash
# Round 3: records go to r3/restore/ instead of restore/; nothing else changed.
# Lane B21: lane B19's baseline_b19.sh with the environment B21_ENV and the controller staging /tmp/a625; nothing else. Its notes follow.
# Lane B19: lane B18's baseline_b18.sh with B19_ENV, the controller staging /tmp/a624, the power-strip status read
# and the controller host's gPTP process check added. Its notes follow.
# Lane B18: lane B17's baseline_b17r.sh with B19_ENV and the controller staging /tmp/a624. Its notes follow.
# Lane B17 resume: baseline_b17.sh with the SoC board's console check removed (the resume ruling: the SoC
# board is not used, no console access at all). Otherwise unchanged; its notes follow.
# Lane B17 copy of lane B15's baseline_b15.sh. Changes: the environment is B21_ENV and the controller
# staging /tmp/a625; the SoC board is checked on its serial console with one empty line and, at a root
# prompt only, the board script's read-only `status` verb (soc_check_b17.py), instead of B15's SSH
# health reads; the descriptor surveys are dropped (the census carries the restore set); the host view
# and the SoC transcript go to the private directory (PRIV), because they name adapters and the board.
# One read-only state snapshot under the bench lock: DUT console reads, the controller's census,
# GET_COUNTERS, the controller and host views. Tag end* removes the controller staging afterwards.
# usage: baseline_b17r.sh <packet_dir> <tag>
set -u
. "${B21_ENV:?}"
: "${PRIV:?}"
P=$1; T=$2
timeout -k 5 240 flock -w 120 /tmp/milan-bench.lock bash -c '
set -u
P=$0; T=$1
echo "LOCK $(date -u +%FT%T.%3NZ)"
timeout 60 python3 -B "$P/tools/console_read.py" "$DUT_CONSOLE" "$P/r3/restore/dut-$T.txt" milan_status milan_nvm \
  "mem_read 0x90000654 12" "mem_read 0x90000660 20" "mem_read 0x90000694 8" "mem_read 0x900006a4 4" \
  "mem_read 0x900006cc 12" "mem_read 0x900006dc 4" "mem_read 0x90000900 4" "mem_read 0x900008d4 12" \
  "mem_read 0x90000680 36" "mem_read 0x900006e0 16" "mem_read 0x90000738 4" "mem_read 0x90000748 8" \
  "mem_read 0x900008f8 8" "mem_read 0x900008e0 8" > /dev/null 2>&1
echo "DUT_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/a625" && \
timeout 30 scp -q "$P/tools/avdecc_ro.py" "$P/tools/b8_ctl.py" "$CTL_HOST:/tmp/a625/"
echo "STAGE_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a625 && \
  sudo -n timeout 40 python3 -B b8_ctl.py census $CTL_IFACE $PEER_EID $PEER_MAC" > "$P/r3/restore/census-$T.jsonl" 2> "$P/r3/restore/census-$T.err"
echo "CENSUS_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a625 && \
  sudo -n timeout 40 python3 -B b8_ctl.py counters $CTL_IFACE $PEER_EID $PEER_MAC" > "$P/r3/restore/counters-$T.jsonl" 2> "$P/r3/restore/counters-$T.err"
echo "COUNTERS_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "pgrep -a ptp4l; echo PGREP_RC=\$?; \
  pgrep -af '"'"'[b]8_ctl'"'"'; echo PGREP2_RC=\$?; cd /tmp/a625 && sha256sum *.py; ls -la /tmp/a625" > "$P/r3/restore/controller-$T.txt" 2>&1
echo "CTL_RC=$?"
{ cat /proc/asound/cards; for s in /proc/asound/card*/pcm*/sub0/status; do echo "$s: $(head -1 $s)"; done; ip -br link; ip -4 -br addr; ls -l /dev/serial/by-id/; } > "$PRIV/host-$T.txt" 2>&1
echo "HOST_RC=$?"
timeout 20 ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=no "$STRIP_HOST" "powerstrip status" > "$P/r3/restore/outlets-$T.txt" 2>&1
echo "OUTLETS_RC=$?"
case "$T" in end*) true;; *) false;; esac && {
  timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "rm -rf /tmp/a625; ls -d /tmp/a625 2>&1; pgrep -af '"'"'[b]8_ctl'"'"'; echo PGREP_RC=\$?" \
    > "$P/r3/restore/controller-cleanup.txt" 2>&1
  echo "CLEANUP_RC=$?"
}
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$T"
echo "LOCK_RC=$?"
