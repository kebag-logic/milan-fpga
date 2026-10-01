#!/usr/bin/env bash
# End snapshot after the STOP, under the bench lock, without the SoC board's console
# (it stands at a login prompt). Read-only on the DUT (console reads, the same list as
# baseline_locked.sh) and on the controller (AVDECC census, PHC and timestamping state);
# the controller staging directory /tmp/a468 is removed. SoC board: this host's view only
# (USB Audio card present, ECM link answers ping).
# usage: end_locked.sh <packet_dir>
# Endpoints come from the private file named by B4_ENV (not in this packet).
set -u
. "${B4_ENV:?}"
P=$1
timeout -k 5 300 flock -w 120 /tmp/milan-bench.lock bash -c '
set -u
P=$0
echo "LOCK $(date -u +%FT%T.%3NZ)"
{ date -u +%FT%T.%3NZ; cat /proc/asound/cards; ip -br addr show "$(ip -br addr | awk "/192\.168\.7\.1\// {print \$1}")"; \
  ping -c 3 -W 2 "${ECM_HOST%.1}.12"; echo PING_RC=$?; } > "$P/soc/end-host-view.txt" 2>&1
echo "HOSTVIEW_RC=$?"
timeout 60 python3 -B "$P/tools/console_read.py" "$DUT_CONSOLE" "$P/restore/dut-end.txt" milan_status milan_nvm \
  "mem_read 0x90000654 12" "mem_read 0x90000660 20" "mem_read 0x90000694 8" "mem_read 0x900006a4 4" \
  "mem_read 0x900006cc 12" "mem_read 0x900006dc 4" "mem_read 0x90000900 4" "mem_read 0x900008d4 12" \
  "mem_read 0x90000680 36" "mem_read 0x900006e0 16" > /dev/null 2>&1
echo "DUT_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a468 && sudo -n env PEER_EID=$PEER_EID PEER_MAC=$PEER_MAC \
  timeout 40 python3 -B avdecc_rw.py census $CTL_IFACE" > "$P/restore/census-end.jsonl" 2> "$P/restore/census-end.err"
echo "CENSUS_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "ls -l /sys/class/net/$CTL_IFACE/device/ptp/ 2>&1; \
  pgrep -a ptp4l; echo PGREP_RC=\$?; ls /tmp/a468; sudo -n $HWSTAMP_CTL -i $CTL_IFACE; echo HWSTAMP_RC=\$?; \
  sudo -n $PHC_CTL $CTL_IFACE freq cmp; echo PHC_RC=\$?" > "$P/restore/controller-end.txt" 2>&1
echo "CTL_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "rm -rf /tmp/a468; ls -d /tmp/a468 2>&1; pgrep -a ptp4l; echo PGREP_RC=\$?" \
  > "$P/restore/controller-cleanup.txt" 2>&1
echo "CLEANUP_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P"
echo "LOCK_RC=$?"
