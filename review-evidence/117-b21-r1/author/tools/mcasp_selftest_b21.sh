#!/usr/bin/env bash
# Lane B21 round 3, step 1: self-test of the SoC board's McASP0 capture path, deficit-only.
# Runs inside one locked action (tracked_b21.sh holds the bench lock for its whole length).
# On the board: arecord -D hw:0,0 (8 x S32_LE, 48 kHz, lane B5's period 480 and buffer 24,000)
# into b21stamp, which stamps every read with the board's clocks and keeps no samples; a 1 Hz
# shell sampler reads the McASP DMA interrupt rows and /proc/stat. No DUT, peer, tap or controller
# action. The records come back over the board's USB network link (TFTP, lane B3's receiver).
# usage: mcasp_selftest_b21.sh <packet_dir> <name> <seconds>
set -u
. "${B21_ENV:?}"
P=$1; N=$2; S=$3
OUT=$P/r3/selftest/$N; RAW=/tmp/a625/raw/$N
mkdir -p "$OUT" "$RAW"
soc() { timeout $(($2 + 30)) python3 -B "$P/tools/soccon_b21.py" "$SOC_CONSOLE" "$OUT/soc-$1.log" "$2" "$3" > /dev/null 2>&1; echo "SOC_$1_RC=$? $(date -u +%FT%T.%3NZ)"; }
echo "START $(date -u +%FT%T.%3NZ) name=$N seconds=$S"
soc pre 30 "cat /proc/uptime; for s in /proc/asound/card0/pcm0*/sub0/status; do echo \$s: \$(head -1 \$s); done; ps -o pid,comm | grep -E 'alsaloop|arecord|aplay|pipewire|soloist' ; sha256sum /tmp/a625/b21stamp; df -k /tmp | tail -1"
soc launch 30 "cd /tmp/a625 && rm -f $N.*; nohup bash -c 'set -o pipefail; arecord -v -D hw:0,0 -c 8 -f S32_LE -r 48000 -t raw --period-size=480 --buffer-size=24000 -d $S - 2> $N.arecord.log | ./b21stamp 8 4 none /dev/null $N.ts 4 2> $N.stamp.log; echo \"\${PIPESTATUS[*]}\" > $N.done' > /dev/null 2>&1 < /dev/null & (while [ ! -f $N.done ]; do cat /proc/uptime; grep -E '485c0100.dma-controller chan[01]\$' /proc/interrupts; head -1 /proc/stat; sleep 1; done) > $N.samp 2>&1 < /dev/null & sleep 3; head -40 $N.arecord.log; ps -o pid,comm | grep -E 'arecord|b21stamp'; cat /proc/uptime"
sleep $((S + 5))
for i in 1 2 3 4 5 6; do
  soc "wait$i" 20 "ls /tmp/a625/$N.done && cat /tmp/a625/$N.done" | tee -a "$OUT/wait.txt"
  grep -q "SOC_wait${i}_RC=0" "$OUT/wait.txt" && break
  sleep 10
done
timeout 120 python3 -B "$P/tools/b21_xfer.py" /tmp/a625/serve 18625 "$RAW" 18626 40 > "$OUT/xfer.jsonl" 2>&1 &
XP=$!
sleep 1
soc collect 90 "cd /tmp/a625 && cat /proc/uptime; cat $N.done; cat $N.stamp.log; cat $N.arecord.log | tail -30; grep -c -i overrun $N.arecord.log; ls -l $N.*; sha256sum $N.ts $N.samp $N.arecord.log $N.stamp.log; for f in $N.ts $N.samp $N.arecord.log $N.stamp.log; do tftp -p -b 1428 -l \$f -r \$f <bench-address>.1 18626 && echo tftp_ok \$f; done; for s in /proc/asound/card0/pcm0*/sub0/status; do echo \$s: \$(head -1 \$s); done"
wait $XP
(cd "$RAW" && sha256sum -- * > "$OUT/raw.sha256"; ls -l > "$OUT/raw.ls")
soc cleanup 20 "cd /tmp/a625 && rm -f $N.ts $N.samp $N.arecord.log $N.stamp.log $N.done && ls -l /tmp/a625"
echo "END $(date -u +%FT%T.%3NZ)"
