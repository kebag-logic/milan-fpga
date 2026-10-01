#!/usr/bin/env bash
# One read-only state snapshot under the bench lock (lane B3's baseline_locked.sh, retargeted):
# SoC board health (bridge status, PIDs and command lines, PCM states, UDC, fault scan, /tmp),
# DUT console reads, the controller's AVDECC census of the DUT and the reference peer (read
# commands and GET_AUDIO_MAP only), the controller's process and staging state, and this
# host's view of the SoC board's USB function and the external capture's card.
# With tag `start` it also runs the peer's read-only descriptor survey. The snapshot tagged
# `end` removes the controller staging directory afterwards.
# usage: baseline_locked.sh <packet_dir> <tag>
# Endpoints come from the private file named by B5_ENV (not in this packet).
set -u
. "${B5_ENV:?}"
P=$1; T=$2
export DUT_CONSOLE SOC_CONSOLE CTL_HOST CTL_IFACE PEER_EID PEER_MAC
timeout -k 5 300 flock -w 120 /tmp/milan-bench.lock bash -c '
set -u
P=$0; T=$1
echo "LOCK $(date -u +%FT%T.%3NZ)"
SOC_CMD="cat /proc/uptime; uname -a; tdm8-uac2.sh status; echo PIDFILES; cat /run/tdm8/*.pid; \
for p in \$(cat /run/tdm8/*.pid); do echo \"PID \$p: \$(tr \"\\0\" \" \" < /proc/\$p/cmdline)\"; done; \
ps -o pid,args | grep -E \"[a]lsaloop|[a]play|[a]record\"; \
echo UDC=\$(cat /sys/class/udc/*/state); \
for s in /proc/asound/card*/pcm*/sub0/status; do echo \"== \$s\"; head -3 \$s; done; cat /proc/asound/cards; \
df -k /tmp | tail -1; free -k | head -2; ls /tmp; \
echo BAD=\$(dmesg | grep -ciE \"self-detected|rcu_preempt detected|replenish|WARNING|teardown|refused to stop|Call trace|BUG:|Oops\"); \
cat /proc/sys/kernel/tainted; dmesg | tail -3; \
grep -n alsaloop \$(which tdm8-uac2.sh); sha256sum \$(which tdm8-uac2.sh); \
cat /proc/uptime; grep dma-controller /proc/interrupts; sleep 5; cat /proc/uptime; grep dma-controller /proc/interrupts"
timeout 90 python3 -B "$P/tools/soccon.py" "$SOC_CONSOLE" "$P/soc/$T-health.log" 60 "$SOC_CMD" > /dev/null 2>&1
echo "SOC_RC=$?"
timeout 60 python3 -B "$P/tools/console_read.py" "$DUT_CONSOLE" "$P/restore/dut-$T.txt" milan_status milan_nvm \
  "mem_read 0x90000654 12" "mem_read 0x90000660 20" "mem_read 0x90000694 8" "mem_read 0x900006a4 4" \
  "mem_read 0x900006cc 12" "mem_read 0x900006dc 4" "mem_read 0x90000900 4" "mem_read 0x900008d4 12" \
  "mem_read 0x90000680 36" "mem_read 0x900006e0 16" > /dev/null 2>&1
echo "DUT_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/a472" && \
timeout 30 scp -q "$P/tools/avdecc_ro.py" "$P/tools/b5_ctl.py" "$CTL_HOST:/tmp/a472/"
echo "STAGE_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a472 && \
  sudo -n timeout 40 python3 -B b5_ctl.py census $CTL_IFACE $PEER_EID $PEER_MAC" > "$P/restore/census-$T.jsonl" 2> "$P/restore/census-$T.err"
echo "CENSUS_RC=$?"
if [ "$T" = start ]; then
  timeout 120 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a472 && \
    sudo -n timeout 100 python3 -B b5_ctl.py descs $CTL_IFACE $PEER_EID $PEER_MAC" > "$P/restore/peer-descs.jsonl" 2> "$P/restore/peer-descs.err"
  echo "DESCS_RC=$?"
fi
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "pgrep -a ptp4l; echo PGREP_RC=\$?; \
  pgrep -af b5_ctl; echo PGREP2_RC=\$?; cd /tmp/a472 && sha256sum *.py; ls -la /tmp/a472" > "$P/restore/controller-$T.txt" 2>&1
echo "CTL_RC=$?"
{ cat /proc/asound/cards; ip -br link; ls -l /dev/serial/by-id/; } > "$P/restore/host-$T.txt" 2>&1
echo "HOST_RC=$?"
if [ "$T" = end ]; then
  timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "rm -rf /tmp/a472; ls -d /tmp/a472 2>&1; pgrep -af b5_ctl; echo PGREP_RC=\$?" \
    > "$P/restore/controller-cleanup.txt" 2>&1
  echo "CLEANUP_RC=$?"
fi
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$T"
echo "LOCK_RC=$?"
