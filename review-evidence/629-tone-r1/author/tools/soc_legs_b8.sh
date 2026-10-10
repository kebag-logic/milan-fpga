#!/usr/bin/env bash
# Lane B8 copy of lane B7's script: only the environment name (B8_ENV), the controller staging (/tmp/a521), the controller tool name (b8_ctl.py) and the raw root (/tmp/b8-a521/raw) differ.
# Stop or restart the SoC board's two audio bridge legs by the recorded method, under
# the bench lock. Never the bridge script's gadget or bridge up/down verbs, never the
# UDC, never pkill: only the alsaloop PIDs that `tdm8-uac2.sh status` names, after
# checking each command line, and the two recorded alsaloop lines to restart.
# usage: soc_legs_locked.sh <packet_dir> stop <to_host_pid> <from_host_pid> <tag>
#        soc_legs_locked.sh <packet_dir> start <tag>
# Endpoints come from the private file named by B8_ENV (not in this packet). Lane B5 copy; lane B6 changes only the environment name and the console runner (reply over the board link, soccon_net.py); lane B7 changes only the environment name.
set -u
. "${B8_ENV:?}"
P=$1; OP=$2
TO_LINE='alsaloop -C hw:0,0 -P hw:1,0 -c 8 -r 48000 -f S32_LE -t 8000 -S samplerate -z'
FROM_LINE='alsaloop -C hw:1,0 -P hw:0,0 -c 8 -r 48000 -f S32_LE -t 8000 -S samplerate -z'
POST="sleep 3; cat /proc/uptime; tdm8-uac2.sh status | sed -n '/bridge/,\$p'; cat /run/tdm8/to-host.pid /run/tdm8/from-host.pid; \
ps -o pid,args | grep [a]lsaloop; echo UDC=\$(cat /sys/class/udc/*/state); \
echo BAD=\$(dmesg | grep -ciE 'self-detected|rcu_preempt detected|replenish|WARNING|teardown|refused to stop|Call trace|BUG:|Oops'); \
cat /proc/sys/kernel/tainted; grep dma-controller /proc/interrupts; dmesg | tail -2"
if [ "$OP" = stop ]; then
  A=$3; B=$4; T=$5
  CMD="S=\$(tdm8-uac2.sh status); echo \"\$S\" | sed -n '/bridge/,/PCM/p'; \
A=\$(tr '\\0' ' ' < /proc/$A/cmdline); B=\$(tr '\\0' ' ' < /proc/$B/cmdline); echo \"$A: \$A\"; echo \"$B: \$B\"; \
if echo \"\$S\" | grep -q 'to-host: running (pid $A)' && echo \"\$S\" | grep -q 'from-host: running (pid $B)' \
&& [ \"\$A\" = '$TO_LINE ' ] && [ \"\$B\" = '$FROM_LINE ' ]; then kill $A $B; echo KILLED; else echo MISMATCH_NOT_KILLED; fi; \
sleep 2; ls -d /proc/$A /proc/$B 2>&1; for s in /proc/asound/card*/pcm*/sub0/status; do echo \"\$s: \$(head -1 \$s)\"; done; $POST"
elif [ "$OP" = start ]; then
  T=$3
  CMD="ps -o pid,args | grep [a]lsaloop; for s in /proc/asound/card*/pcm*/sub0/status; do echo \"\$s: \$(head -1 \$s)\"; done; \
if ps -o args | grep -q [a]lsaloop; then echo LEGS_PRESENT_NOT_STARTED; else cd /; \
nohup $TO_LINE >/dev/null 2>&1 </dev/null & echo \$! > /run/tdm8/to-host.pid; \
nohup $FROM_LINE >/dev/null 2>&1 </dev/null & echo \$! > /run/tdm8/from-host.pid; disown -a; echo STARTED; fi; $POST"
else
  echo "unknown op $OP"; exit 2
fi
timeout -k 5 150 flock -w 120 /tmp/milan-bench.lock bash -c '
echo "LOCK $(date -u +%FT%T.%3NZ)"
timeout 100 python3 -B "$0/tools/soccon_net.py" "$SOC_CONSOLE" "$0/soc/$1-legs.log" 60 "$2" > /dev/null 2>&1
echo "SOC_RC=$?"
echo "UNLOCK $(date -u +%FT%T.%3NZ)"
' "$P" "$T" "$CMD"
echo "LOCK_RC=$?"
