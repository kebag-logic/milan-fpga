#!/usr/bin/env bash
# Lane B21 round 3: Direction A restarts, inside one locked action (tracked_b21.sh holds the bench lock).
# The SoC board plays the first-light pattern (as dir_b21.sh A, from the period it already built and
# checked); both taps keep the DUT's AAF and CRF streams and every ACMP frame; the external capture
# records the peer's output; restart_b21.py runs the unbind and rebind cycles of DUT STREAM_OUTPUT 0 to
# the peer's STREAM_INPUT 0, each under the binding rule, and leaves the binding in place.
# usage: restart_run_b21.sh <packet_dir> <name> <cycles> <tap_seconds>
set -u
. "${B21_ENV:?}"
P=$1; N=$2; NC=$3; TS=$4
OUT=$P/r3/runs/$N; RAW=/tmp/a625/raw/$N
mkdir -p "$OUT" "$RAW"
ev() { echo "{\"t\": $(date +%s.%N | cut -c1-17), \"utc\": \"$(date -u +%FT%T.%3NZ)\", \"kind\": \"$1\"${2:+, $2}}" | tee -a "$OUT/events.jsonl"; }
soc() { timeout $(($2 + 30)) python3 -B "$P/tools/soccon_b21.py" "$SOC_CONSOLE" "$OUT/soc-$1.log" "$2" "$3" > /dev/null 2>&1; ev soc "\"tag\": \"$1\", \"rc\": $?"; }
F="(ether[40:2]=0x8100 and ether[44:2]=0x22f0 and ether[50:4]=0x02000000 and (ether[54:4]=0x00010000 or ether[54:4]=0x00010001)) or (ether[40:2]=0x22f0 and ether[42]=0xfc) or (ether[40:2]=0x8100 and ether[44:2]=0x22f0 and ether[46]=0xfc)"
ev start "\"name\": \"$N\", \"cycles\": $NC, \"tap_seconds\": $TS, \"tap_filter\": \"$F\""
timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$CTL_HOST" "mkdir -p /tmp/a625" && timeout 30 scp -q "$P/tools/avdecc_ro.py" "$P/tools/b8_ctl.py" "$CTL_HOST:/tmp/a625/"
ev stage "\"rc\": $?"
timeout 60 python3 -B "$P/tools/console_read.py" "$DUT_CONSOLE" "$OUT/dut-pre.txt" milan_status "mem_read 0x90000660 8" "mem_read 0x900006b8 12" "mem_read 0x900008d4 12" > /dev/null 2>&1; ev dut "\"tag\": \"pre\", \"rc\": $?"
soc check 30 "sha256sum /tmp/a625/din.raw; ps -o pid,comm | grep -E 'aplay|arecord'; for s in /proc/asound/card0/pcm0*/sub0/status; do echo \$s: \$(head -1 \$s); done"
grep -q 'b6a92e9724e945354c3f8fc5178cec7bb8fd0e62d52bd9ee7f13ed5347bfa97c  /tmp/a625/din.raw' "$OUT/soc-check.log" || { ev abort "\"why\": \"pattern period missing\""; exit 3; }
for IF in <MAC-derived-interface-name> <MAC-derived-interface-name>; do
  timeout $((TS + 40)) ssh -o BatchMode=yes -o ConnectTimeout=10 "$TAP_HOST" "sudo -n timeout -s INT $TS tcpdump -U -n -B 65536 -i $IF -w /tmp/a625-$N-$IF.pcap '$F'" > "$OUT/tap-$IF.txt" 2>&1 &
done
ev taps-started
sleep 2
timeout $((TS + 120)) python3 -B "$P/tools/selftest_b21.py" "$N-ext" $((TS - 10)) /tmp/a625/raw > "$RAW/ext-stdout.jsonl" 2>&1 &
ev ext-started
sleep 2
soc play 30 "cd /tmp/a625 && nohup sh -c 'while cat /tmp/a625/din.raw; do :; done | aplay -v -D hw:0,0 -t raw -c 8 -f S32_LE -r 48000 -d $((TS + 10)); echo aplay_rc=\$?' > /tmp/a625/$N.play.log 2>&1 < /dev/null & sleep 2; ps -o pid,comm | grep -E 'aplay|cat'"
sleep 8
timeout $((TS + 60)) python3 -B "$P/tools/restart_b21.py" "$OUT" "$NC" 2.0 4.0 > "$OUT/restart-stdout.jsonl" 2>&1
ev cycles-done "\"rc\": $?"
wait
ev taps-and-ext-done
timeout 60 python3 -B "$P/tools/console_read.py" "$DUT_CONSOLE" "$OUT/dut-post.txt" milan_status "mem_read 0x90000660 8" "mem_read 0x900006b8 12" "mem_read 0x900008d4 12" > /dev/null 2>&1; ev dut "\"tag\": \"post\", \"rc\": $?"
for IF in <MAC-derived-interface-name> <MAC-derived-interface-name>; do
  timeout 200 scp -q "$TAP_HOST:/tmp/a625-$N-$IF.pcap" "$RAW/"; ev tap-copy "\"if\": \"$IF\", \"rc\": $?"
  timeout 30 ssh -o BatchMode=yes -o ConnectTimeout=10 "$TAP_HOST" "ls -l /tmp/a625-$N-$IF.pcap; sha256sum /tmp/a625-$N-$IF.pcap; sudo -n rm -f /tmp/a625-$N-$IF.pcap; ls /tmp/a625-$N-$IF.pcap 2>&1" >> "$OUT/tap-post.txt" 2>&1
done
sleep 15
soc end 30 "cd /tmp/a625 && tail -4 $N.play.log; ps -o pid,comm | grep -E 'aplay|cat'; for s in /proc/asound/card0/pcm0*/sub0/status; do echo \$s: \$(head -1 \$s); done; rm -f $N.play.log"
(cd "$RAW" && sha256sum -- *.pcap > "$OUT/raw.sha256"; ls -l > "$OUT/raw.ls")
ev end
