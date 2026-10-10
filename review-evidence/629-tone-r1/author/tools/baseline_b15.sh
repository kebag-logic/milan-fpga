#!/usr/bin/env bash
# Lane B15 copy of lane B10's baseline_b10.sh. Changes: the environment is B15_ENV and the controller
# staging /tmp/a588; the SoC board is read over key-based SSH on the board link (SOC_SSH) instead of
# its serial console (this lane's rule), with the same read-only commands; the host view adds the
# tone source's and the board link's substream status lines as before. Everything else is lane B10's.
# One read-only state snapshot under the bench lock: SoC board health, DUT console reads, the
# controller's census, GET_COUNTERS, and with tag `start` the descriptor surveys. Tag end* removes the
# controller staging directory afterwards.
# usage: baseline_b15.sh <packet_dir> <tag>
set -u
. "${B15_ENV:?}"
P=$1; T=$2
timeout -k 5 300 flock -w 120 /tmp/milan-bench.lock bash -c '
set -u
P=$0; T=$1
echo "LOCK $(date -u +%FT%T.%3NZ)"
SOC_CMD="cat /proc/uptime; uname -a; tdm8-uac2.sh status; echo PIDFILES; cat /run/tdm8/*.pid; \
for p in \$(cat /run/tdm8/*.pid); do echo \"PID \$p: \$(tr \"\\0\" \" \" < /proc/\$p/cmdline 2>/dev/null)\"; done; \
ps -o pid,args | grep -E \"[a]lsaloop|[a]play|[a]record\"; \
echo UDC=\$(cat /sys/class/udc/*/state); \
for s in /proc/asound/card*/pcm*/sub0/status; do echo \"== \$s\"; head -3 \$s; done; cat /proc/asound/cards; \
df -k /tmp | tail -1; free -k | head -2; ls /tmp; \
echo BAD=\$(dmesg | grep -ciE \"self-detected|rcu_preempt detected|replenish|WARNING|teardown|refused to stop|Call trace|BUG:|Oops\"); \
cat /proc/sys/kernel/tainted; dmesg | tail -3; \
grep -n alsaloop \$(which tdm8-uac2.sh); sha256sum \$(which tdm8-uac2.sh); \
cat /proc/uptime; grep dma-controller /proc/interrupts; sleep 5; cat /proc/uptime; grep dma-controller /proc/interrupts"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$SOC_SSH" "$SOC_CMD" > "$P/soc/$T-health.log" 2>&1
echo "SOC_RC=$?"
timeout 60 python3 -B "$P/tools/console_read.py" "$DUT_CONSOLE" "$P/restore/dut-$T.txt" milan_status milan_nvm \
  "mem_read 0x90000654 12" "mem_read 0x90000660 20" "mem_read 0x90000694 8" "mem_read 0x900006a4 4" \
  "mem_read 0x900006cc 12" "mem_read 0x900006dc 4" "mem_read 0x90000900 4" "mem_read 0x900008d4 12" \
  "mem_read 0x90000680 36" "mem_read 0x900006e0 16" "mem_read 0x90000738 4" "mem_read 0x90000748 8" \
  "mem_read 0x900008f8 8" "mem_read 0x900008e0 8" > /dev/null 2>&1
echo "DUT_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/a588" && \
timeout 30 scp -q "$P/tools/avdecc_ro.py" "$P/tools/b8_ctl.py" "$CTL_HOST:/tmp/a588/"
echo "STAGE_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a588 && \
  sudo -n timeout 40 python3 -B b8_ctl.py census $CTL_IFACE $PEER_EID $PEER_MAC" > "$P/restore/census-$T.jsonl" 2> "$P/restore/census-$T.err"
echo "CENSUS_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a588 && \
  sudo -n timeout 40 python3 -B b8_ctl.py counters $CTL_IFACE $PEER_EID $PEER_MAC" > "$P/restore/counters-$T.jsonl" 2> "$P/restore/counters-$T.err"
echo "COUNTERS_RC=$?"
if [ "$T" = start ]; then
  timeout 120 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a588 && \
    sudo -n timeout 100 python3 -B b8_ctl.py descs $CTL_IFACE $PEER_EID $PEER_MAC" > "$P/restore/peer-descs.jsonl" 2> "$P/restore/peer-descs.err"
  echo "DESCS_RC=$?"
  timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a588 && \
    sudo -n timeout 40 python3 -B b8_ctl.py dutdescs $CTL_IFACE $PEER_EID $PEER_MAC" > "$P/restore/dut-descs.jsonl" 2> "$P/restore/dut-descs.err"
  echo "DUTDESCS_RC=$?"
fi
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "pgrep -a ptp4l; echo PGREP_RC=\$?; \
  pgrep -af '[b]8_ctl'; echo PGREP2_RC=\$?; cd /tmp/a588 && sha256sum *.py; ls -la /tmp/a588" > "$P/restore/controller-$T.txt" 2>&1
echo "CTL_RC=$?"
{ cat /proc/asound/cards; for s in /proc/asound/card*/pcm*/sub0/status; do echo "$s: $(head -1 $s)"; done; ip -br link; ip -4 -br addr; ls -l /dev/serial/by-id/; } > "$P/restore/host-$T.txt" 2>&1
echo "HOST_RC=$?"
case "$T" in end*) true;; *) false;; esac && {
  timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "rm -rf /tmp/a588; ls -d /tmp/a588 2>&1; pgrep -af '[b]8_ctl'; echo PGREP_RC=\$?" \
    > "$P/restore/controller-cleanup.txt" 2>&1
  echo "CLEANUP_RC=$?"
}
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$T"
echo "LOCK_RC=$?"
