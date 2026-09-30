#!/usr/bin/env bash
# One read-only state snapshot under the bench lock: SoC board health (bridge status,
# PCM states, interrupt rates, fault scan), DUT console reads, the controller's AVDECC
# census (DUT and reference peer, read commands and GET_AUDIO_MAP only) and the
# controller NIC's PHC and timestamping state. The AVDECC tools are staged in /tmp/a453 on
# the controller for the census; the snapshot tagged `end` removes that directory afterwards.
# usage: baseline_locked.sh <packet_dir> <tag>
# Endpoints come from the private file named by B3_ENV (not in this packet).
set -u
. "${B3_ENV:?}"
P=$1; T=$2
timeout -k 5 300 flock -w 120 /tmp/milan-bench.lock bash -c '
set -u
P=$0; T=$1
echo "LOCK $(date -u +%FT%T.%3NZ)"
SOC_CMD="cat /proc/uptime; uname -a; tdm8-uac2.sh status; echo PIDFILES; cat /run/tdm8/*.pid; \
for p in \$(cat /run/tdm8/*.pid); do echo \"PID \$p: \$(tr \"\\0\" \" \" < /proc/\$p/cmdline)\"; done; \
echo UDC=\$(cat /sys/class/udc/*/state); \
for s in /proc/asound/card*/pcm*/sub0/status; do echo \"== \$s\"; head -3 \$s; done; cat /proc/asound/cards; \
df -k /tmp | tail -1; free -k | head -2; ls /tmp; \
echo BAD=\$(dmesg | grep -ciE \"self-detected|rcu_preempt detected|replenish|WARNING|teardown|refused to stop|Call trace|BUG:|Oops\"); \
cat /proc/sys/kernel/tainted; cat /sys/kernel/rcu_stall_count 2>/dev/null; \
grep -n alsaloop \$(which tdm8-uac2.sh); sha256sum \$(which tdm8-uac2.sh); \
cat /proc/uptime; grep dma-controller /proc/interrupts; sleep 5; cat /proc/uptime; grep dma-controller /proc/interrupts"
timeout 90 python3 -B "$P/tools/soccon.py" "$SOC_CONSOLE" "$P/soc/$T-health.log" 60 "$SOC_CMD" > /dev/null 2>&1
echo "SOC_RC=$?"
timeout 60 python3 -B "$P/tools/console_read.py" "$DUT_CONSOLE" "$P/restore/dut-$T.txt" milan_status milan_nvm \
  "mem_read 0x90000654 12" "mem_read 0x90000660 20" "mem_read 0x90000694 8" "mem_read 0x900006a4 4" \
  "mem_read 0x900006cc 12" "mem_read 0x900006dc 4" "mem_read 0x90000900 4" "mem_read 0x900008d4 12" \
  "mem_read 0x90000680 36" "mem_read 0x900006e0 16" > /dev/null 2>&1
echo "DUT_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/a453" && \
timeout 30 scp -q "$P/tools/avdecc_ro.py" "$P/tools/avdecc_rw.py" "$CTL_HOST:/tmp/a453/"
echo "STAGE_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a453 && sudo -n env PEER_EID=$PEER_EID PEER_MAC=$PEER_MAC \
  timeout 40 python3 -B avdecc_rw.py census $CTL_IFACE" > "$P/restore/census-$T.jsonl" 2> "$P/restore/census-$T.err"
echo "CENSUS_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "ls -l /sys/class/net/$CTL_IFACE/device/ptp/ 2>&1; \
  pgrep -a ptp4l; echo PGREP_RC=\$?; ls /tmp/a453; sudo -n $HWSTAMP_CTL -i $CTL_IFACE; echo HWSTAMP_RC=\$?; \
  sudo -n $PHC_CTL $CTL_IFACE freq cmp; echo PHC_RC=\$?" > "$P/restore/controller-$T.txt" 2>&1
echo "CTL_RC=$?"
if [ "$T" = end ]; then
  timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "rm -rf /tmp/a453; ls -d /tmp/a453 2>&1; pgrep -a ptp4l; echo PGREP_RC=\$?" \
    > "$P/restore/controller-cleanup.txt" 2>&1
  echo "CLEANUP_RC=$?"
fi
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$T"
echo "LOCK_RC=$?"
