#!/usr/bin/env bash
# Lane B8 copy of lane B7's script: only the environment name (B8_ENV), the controller staging (/tmp/a521), the controller tool name (b8_ctl.py) and the raw root (/tmp/b8-a521/raw) differ.
# One read-only state snapshot under the bench lock (lane B5's baseline_locked.sh, retargeted):
# SoC board health (bridge status, PIDs and command lines, PCM states, UDC, fault scan, /tmp),
# DUT console reads (lane B5's list plus the CRF sink and media-clock servo words), the
# controller's AVDECC census of the DUT and the reference peer (read commands and
# GET_AUDIO_MAP only), the controller's process and staging state, and this host's view of
# the SoC board's USB function and the external capture's card.
# With tag `start` it also runs the read-only descriptor surveys of the peer and the DUT.
# The snapshot tagged `end` removes the controller staging directory afterwards.
# Lane B7 changes against B6: the environment B8_ENV, the staging directory /tmp/a521, the
# controller tool b8_ctl.py, the AAF clock meter words (0x8E0, 0x8E4) in the DUT reads, and a
# GET_COUNTERS read of both entities (counters-<tag>.jsonl).
# Lane B6 differences: the SoC console reply comes back over the board link (soccon_net.py),
# the controller staging directory is /tmp/a521, and the controller tool is b8_ctl.py.
# usage: baseline_locked.sh <packet_dir> <tag>
# Endpoints come from the private file named by B8_ENV (not in this packet).
set -u
. "${B8_ENV:?}"
P=$1; T=$2
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
timeout 90 python3 -B "$P/tools/soccon_net.py" "$SOC_CONSOLE" "$P/soc/$T-health.log" 60 "$SOC_CMD" > /dev/null 2>&1
echo "SOC_RC=$?"
timeout 60 python3 -B "$P/tools/console_read.py" "$DUT_CONSOLE" "$P/restore/dut-$T.txt" milan_status milan_nvm \
  "mem_read 0x90000654 12" "mem_read 0x90000660 20" "mem_read 0x90000694 8" "mem_read 0x900006a4 4" \
  "mem_read 0x900006cc 12" "mem_read 0x900006dc 4" "mem_read 0x90000900 4" "mem_read 0x900008d4 12" \
  "mem_read 0x90000680 36" "mem_read 0x900006e0 16" "mem_read 0x90000738 4" "mem_read 0x90000748 8" \
  "mem_read 0x900008f8 8" "mem_read 0x900008e0 8" > /dev/null 2>&1
echo "DUT_RC=$?"
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/a521" && \
timeout 30 scp -q "$P/tools/avdecc_ro.py" "$P/tools/b8_ctl.py" "$CTL_HOST:/tmp/a521/"
echo "STAGE_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a521 && \
  sudo -n timeout 40 python3 -B b8_ctl.py census $CTL_IFACE $PEER_EID $PEER_MAC" > "$P/restore/census-$T.jsonl" 2> "$P/restore/census-$T.err"
echo "CENSUS_RC=$?"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a521 && \
  sudo -n timeout 40 python3 -B b8_ctl.py counters $CTL_IFACE $PEER_EID $PEER_MAC" > "$P/restore/counters-$T.jsonl" 2> "$P/restore/counters-$T.err"
echo "COUNTERS_RC=$?"
if [ "$T" = start ]; then
  timeout 120 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a521 && \
    sudo -n timeout 100 python3 -B b8_ctl.py descs $CTL_IFACE $PEER_EID $PEER_MAC" > "$P/restore/peer-descs.jsonl" 2> "$P/restore/peer-descs.err"
  echo "DESCS_RC=$?"
  timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a521 && \
    sudo -n timeout 40 python3 -B b8_ctl.py dutdescs $CTL_IFACE $PEER_EID $PEER_MAC" > "$P/restore/dut-descs.jsonl" 2> "$P/restore/dut-descs.err"
  echo "DUTDESCS_RC=$?"
fi
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "pgrep -a ptp4l; echo PGREP_RC=\$?; \
  pgrep -af '[b]8_ctl'; echo PGREP2_RC=\$?; cd /tmp/a521 && sha256sum *.py; ls -la /tmp/a521" > "$P/restore/controller-$T.txt" 2>&1
echo "CTL_RC=$?"
{ cat /proc/asound/cards; ip -br link; ip -4 -br addr; ls -l /dev/serial/by-id/; } > "$P/restore/host-$T.txt" 2>&1
echo "HOST_RC=$?"
case "$T" in end*) true;; *) false;; esac && {  # lane B8 resume: any end tag (end, end2)
  timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "rm -rf /tmp/a521; ls -d /tmp/a521 2>&1; pgrep -af '[b]8_ctl'; echo PGREP_RC=\$?" \
    > "$P/restore/controller-cleanup.txt" 2>&1
  echo "CLEANUP_RC=$?"
}
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$T"
echo "LOCK_RC=$?"
