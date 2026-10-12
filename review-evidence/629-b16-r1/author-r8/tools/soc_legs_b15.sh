#!/usr/bin/env bash
# Lane B15 copy of lane B10's soc_legs_b10.sh. Changes: the board is reached over key-based SSH on
# the board link (SOC_SSH; this lane's rule forbids its serial console), so the command runs in that
# SSH session instead of being typed at the console; each leg is handled on its own, because as
# found only the to-host leg runs (from-host DEAD): `stop to-host <pid>` and `start to-host`. The
# command lines, the status check and the pid file are lane B10's. The start's presence check reads
# the bridge script's `status` (a ps pattern matched this SSH session's own command line, which carries
# the leg's line: pts1's restart printed LEG_PRESENT_NOT_STARTED with the leg dead). The caller holds the bench lock
# (this script takes no lock: it runs inside one locked action).
# Never the bridge script's up/down verbs, never the UDC, never pkill: only the alsaloop PID that
# `tdm8-uac2.sh status` names, after checking its command line, and only that leg's recorded line.
# usage: soc_legs_b15.sh <log> stop to-host <pid>
#        soc_legs_b15.sh <log> start to-host
set -u
. "${B15_ENV:?}"
LOG=$1; OP=$2; LEG=$3; PID=${4:-}
TO_LINE='alsaloop -C hw:0,0 -P hw:1,0 -c 8 -r 48000 -f S32_LE -t 8000 -S samplerate -z'
[ "$LEG" = to-host ] || { echo "only the to-host leg runs as found"; exit 2; }
POST="sleep 3; cat /proc/uptime; tdm8-uac2.sh status | sed -n '/bridge/,\$p'; cat /run/tdm8/to-host.pid; \
ps -o pid,args | grep [a]lsaloop; echo UDC=\$(cat /sys/class/udc/*/state); \
echo BAD=\$(dmesg | grep -ciE 'self-detected|rcu_preempt detected|replenish|WARNING|teardown|refused to stop|Call trace|BUG:|Oops'); \
cat /proc/sys/kernel/tainted; grep dma-controller /proc/interrupts; dmesg | tail -2"
if [ "$OP" = stop ]; then
  CMD="S=\$(tdm8-uac2.sh status); echo \"\$S\" | sed -n '/bridge/,/PCM/p'; \
A=\$(tr '\\0' ' ' < /proc/$PID/cmdline); echo \"$PID: \$A\"; \
if echo \"\$S\" | grep -q 'to-host: running (pid $PID)' && [ \"\$A\" = '$TO_LINE ' ]; then kill $PID; echo KILLED; else echo MISMATCH_NOT_KILLED; fi; \
sleep 2; ls -d /proc/$PID 2>&1; for s in /proc/asound/card*/pcm*/sub0/status; do echo \"\$s: \$(head -1 \$s)\"; done; $POST"
elif [ "$OP" = start ]; then
  CMD="ps -o pid,args | grep [a]lsaloop; for s in /proc/asound/card*/pcm*/sub0/status; do echo \"\$s: \$(head -1 \$s)\"; done; \
if tdm8-uac2.sh status | grep -q 'to-host: running'; then echo LEG_PRESENT_NOT_STARTED; else cd /; \
setsid nohup $TO_LINE >/dev/null 2>&1 </dev/null & echo \$! > /run/tdm8/to-host.pid; echo STARTED; fi; $POST"
else
  echo "unknown op $OP"; exit 2
fi
{ echo "### $(date -u +%FT%T.%3NZ) $OP $LEG $PID"; echo "### cmd: $CMD"; } >> "$LOG"
timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$SOC_SSH" "$CMD" >> "$LOG" 2>&1
RC=$?
echo "### rc=$RC $(date -u +%FT%T.%3NZ)" >> "$LOG"
tail -40 "$LOG" | grep -E "KILLED|MISMATCH|STARTED|LEG_PRESENT|to-host:|from-host:|UDC=|BAD=" | tail -6
exit $RC
