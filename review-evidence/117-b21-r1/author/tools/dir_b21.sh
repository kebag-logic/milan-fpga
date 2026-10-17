#!/usr/bin/env bash
# Lane B21 round 3: one direction run, inside one locked action (tracked_b21.sh holds the bench lock).
# Both bindings are in place as found, with equal formats on each side (census), so the run sends no
# bind, format, map or clock-source command: every ATDECC exchange is a read.
#
# A: the SoC board plays the first-light pattern into McASP0 (lane B5's period build and aplay line);
#    the DUT's talker carries it to the reference peer; taps on both links keep the DUT's AAF and CRF
#    streams; the external capture on this host records the peer's output as a cross-check only.
# B: the SoC board records McASP0 (the DUT's TDM output) with arecord into b21stamp, which keeps TDM
#    slots 0-3 (the DUT's STREAM_PORT_INPUT 0 map: stream channels 0-3 on clusters 0-3) and stamps
#    every read; taps on both links keep the peer's AAF stream; nothing is played.
# Both: DUT CSRs polled read-only on the console every 5 s; GET_COUNTERS on both entities at the
# start, the middle and the end.
#
# usage: dir_b21.sh <packet_dir> <name> <A|B> <tap_seconds>
set -u
. "${B21_ENV:?}"
P=$1; N=$2; DIR=$3; TS=$4
OUT=$P/r3/runs/$N; RAW=/tmp/a625/raw/$N
mkdir -p "$OUT" "$RAW"
ev() { echo "{\"t\": $(date +%s.%N | cut -c1-17), \"utc\": \"$(date -u +%FT%T.%3NZ)\", \"kind\": \"$1\"${2:+, $2}}" | tee -a "$OUT/events.jsonl"; }
soc() { timeout $(($2 + 30)) python3 -B "$P/tools/soccon_b21.py" "$SOC_CONSOLE" "$OUT/soc-$1.log" "$2" "$3" > /dev/null 2>&1; ev soc "\"tag\": \"$1\", \"rc\": $?"; }
ctl_counters() {
  timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "cd /tmp/a625 && sudo -n timeout 40 python3 -B b8_ctl.py counters $CTL_IFACE $PEER_EID $PEER_MAC" > "$OUT/counters-$1.jsonl" 2> "$OUT/counters-$1.err"
  ev counters "\"tag\": \"$1\", \"rc\": $?"
}
DUTREADS=("milan_status" "mem_read 0x90000660 8" "mem_read 0x900006b8 12" "mem_read 0x900008d4 12" "mem_read 0x900008e0 8" "mem_read 0x90000738 4" "mem_read 0x90000748 4")
POLL=("mem_read 0x90000660 8" "mem_read 0x900006b8 12" "mem_read 0x900008d4 12" "mem_read 0x900008e0 8")
if [ "$DIR" = A ]; then
  F="(ether[40:2]=0x8100 and ether[44:2]=0x22f0 and ether[50:4]=0x02000000 and (ether[54:4]=0x00010000 or ether[54:4]=0x00010001)) or (ether[40:2]=0x22f0 and ether[46:4]=0x02000000 and (ether[50:4]=0x00010000 or ether[50:4]=0x00010001))"
else
  F="(ether[40:2]=0x8100 and ether[44:2]=0x22f0 and ether[50:4]=0x3cc0c601 and ether[54:4]=0x02030000) or (ether[40:2]=0x22f0 and ether[46:4]=0x3cc0c601 and ether[50:4]=0x02030000)"
fi
ev start "\"name\": \"$N\", \"direction\": \"$DIR\", \"tap_seconds\": $TS, \"tap_filter\": \"$F\""
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/a625" && timeout 30 scp -q "$P/tools/avdecc_ro.py" "$P/tools/b8_ctl.py" "$CTL_HOST:/tmp/a625/"
ev stage "\"rc\": $?"
timeout 60 python3 -B "$P/tools/console_read.py" "$DUT_CONSOLE" "$OUT/dut-pre.txt" "${DUTREADS[@]}" > /dev/null 2>&1; ev dut "\"tag\": \"pre\", \"rc\": $?"
ctl_counters pre
timeout 20 ssh -o BatchMode=yes -o ConnectTimeout=10 "$TAP_HOST" "df -k /tmp | tail -1; rm -f /tmp/a625-$N-*.pcap 2>/dev/null; true" > "$OUT/tap-pre.txt" 2>&1
if [ "$DIR" = A ]; then
  soc build 180 "cd /tmp/a625 && cat /proc/uptime; awk 'BEGIN{for(n=0;n<65536;n++){h=sprintf(\"00%02x%02x\",n%256,int(n/256));s=\"\";for(c=1;c<=8;c++)s=s h sprintf(\"%02x\",c);print s}}' | xxd -r -p > /tmp/a625/din.raw; echo build_rc=\$?; cat /proc/uptime; wc -c < /tmp/a625/din.raw; echo 'b6a92e9724e945354c3f8fc5178cec7bb8fd0e62d52bd9ee7f13ed5347bfa97c  /tmp/a625/din.raw' | sha256sum -c"
  grep -q 'din.raw: OK' "$OUT/soc-build.log" || { ev abort "\"why\": \"pattern period check failed\""; exit 3; }
fi
# taps: both links, for TS seconds, on the tap host's /tmp
for IF in <MAC-derived-interface-name> <MAC-derived-interface-name>; do
  timeout $((TS + 40)) ssh -o BatchMode=yes -o ConnectTimeout=10 "$TAP_HOST" "sudo -n timeout -s INT $TS tcpdump -U -n -B 65536 -i $IF -w /tmp/a625-$N-$IF.pcap '$F'" > "$OUT/tap-$IF.txt" 2>&1 &
done
ev taps-started
# DUT CSR poller
timeout $((TS + 60)) python3 -B "$P/tools/console_poll.py" "$DUT_CONSOLE" "$OUT/dut-poll.txt" $((TS - 10)) 5 "${POLL[@]}" > /dev/null 2>&1 &
PP=$!
ev poll-started
sleep 3
if [ "$DIR" = A ]; then
  # the external capture cross-check (lane B5's reader and capture command, as round 1 ran them)
  timeout $((TS + 120)) python3 -B "$P/tools/selftest_b21.py" "$N-ext" $((TS - 10)) /tmp/a625/raw > "$RAW/ext-stdout.jsonl" 2>&1 &
  XP=$!
  ev ext-started
  sleep 2
  soc play 30 "cd /tmp/a625 && cat /proc/uptime; nohup sh -c 'while cat /tmp/a625/din.raw; do :; done | aplay -v -D hw:0,0 -t raw -c 8 -f S32_LE -r 48000 -d $((TS + 20)); echo aplay_rc=\$?' > /tmp/a625/$N.play.log 2>&1 < /dev/null & sleep 2; ps -o pid,comm | grep -E 'aplay|cat'; head -30 /tmp/a625/$N.play.log; cat /proc/uptime"
else
  soc rec 30 "mkdir -p /root/a625-b21 && cd /root/a625-b21 && rm -f $N.*; cat /proc/uptime; nohup bash -c 'set -o pipefail; arecord -v -D hw:0,0 -c 8 -f S32_LE -r 48000 -t raw --period-size=480 --buffer-size=24000 -d $((TS - 15)) - 2> $N.arecord.log | /tmp/a625/b21stamp 8 4 0,1,2,3 $N.pcm $N.ts 64 2> $N.stamp.log; echo \"\${PIPESTATUS[*]}\" > $N.done' > /dev/null 2>&1 < /dev/null & sleep 3; head -40 $N.arecord.log; ps -o pid,comm | grep -E 'arecord|b21stamp'; cat /proc/uptime; df -k /root | tail -1"
fi
sleep $((TS / 2 - 10))
ctl_counters mid
soc mid 20 "cat /proc/uptime; ps -o pid,comm | grep -E 'aplay|arecord|b21stamp'; for s in /proc/asound/card0/pcm0*/sub0/status; do head -3 \$s; done; cat /proc/loadavg"
wait $PP; ev poll-done "\"rc\": $?"
wait
ev taps-and-ext-done
ctl_counters post
timeout 60 python3 -B "$P/tools/console_read.py" "$DUT_CONSOLE" "$OUT/dut-post.txt" "${DUTREADS[@]}" > /dev/null 2>&1; ev dut "\"tag\": \"post\", \"rc\": $?"
for IF in <MAC-derived-interface-name> <MAC-derived-interface-name>; do
  timeout 200 scp -q "$TAP_HOST:/tmp/a625-$N-$IF.pcap" "$RAW/"; ev tap-copy "\"if\": \"$IF\", \"rc\": $?"
  timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$TAP_HOST" "ls -l /tmp/a625-$N-$IF.pcap; sha256sum /tmp/a625-$N-$IF.pcap; sudo -n rm -f /tmp/a625-$N-$IF.pcap; ls /tmp/a625-$N-$IF.pcap 2>&1" >> "$OUT/tap-post.txt" 2>&1
done
if [ "$DIR" = A ]; then
  sleep 25
  soc end 30 "cd /tmp/a625 && cat /proc/uptime; cat $N.play.log | tail -8; ps -o pid,comm | grep -E 'aplay|cat' ; for s in /proc/asound/card0/pcm0*/sub0/status; do echo \$s: \$(head -1 \$s); done; rm -f $N.play.log; ls /tmp/a625"
else
  for i in 1 2 3 4 5 6; do
    soc "wait$i" 20 "ls /root/a625-b21/$N.done && cat /root/a625-b21/$N.done"
    grep -q '"tag": "wait'$i'", "rc": 0' "$OUT/events.jsonl" && break
    sleep 10
  done
  timeout 400 python3 -B "$P/tools/b21_xfer.py" /tmp/a625/serve 18625 "$RAW" 18626 360 > "$OUT/xfer.jsonl" 2>&1 &
  XP=$!
  sleep 1
  soc collect 380 "cd /root/a625-b21 && cat /proc/uptime; cat $N.done; cat $N.stamp.log; tail -30 $N.arecord.log; grep -c -i overrun $N.arecord.log; ls -l $N.*; sha256sum $N.pcm $N.ts $N.arecord.log $N.stamp.log; for f in $N.ts $N.arecord.log $N.stamp.log $N.pcm; do tftp -p -b 1428 -l \$f -r \$f <bench-address>.1 18626 && echo tftp_ok \$f; done; cat /proc/uptime"
  kill $XP 2>/dev/null; wait $XP 2>/dev/null
  soc cleanup 30 "cd /root/a625-b21 && rm -f $N.pcm $N.ts $N.arecord.log $N.stamp.log $N.done && cd / && rmdir /root/a625-b21; ls -d /root/a625-b21 2>&1; for s in /proc/asound/card0/pcm0*/sub0/status; do echo \$s: \$(head -1 \$s); done"
fi
(cd "$RAW" && sha256sum -- *.pcap *.ts *.pcm *.log 2>/dev/null > "$OUT/raw.sha256"; ls -l > "$OUT/raw.ls")
ev end
