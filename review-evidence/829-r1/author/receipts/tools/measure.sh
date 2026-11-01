#!/usr/bin/env bash
# measure.sh <out> <seconds> : tap capture of the Arty's link with a read-only console poll, under the bench lock taken here; computes one table row.
set -u
R=$1; S=$2; I=${POLL_PERIOD:-4}
mkdir -p "$R"
P=/dev/serial/by-id/<adapter>
T=$VALIDATION_STORAGE/583-a724b/tools
SSH="ssh -o BatchMode=yes <bench-host-prefix>ubuntu-server"
IFACE=<MAC-derived-interface-name>
run() {
  echo "LOCK $(date -Iseconds)"
  stty -F $P -a | tr ';' '\n' | grep -a -o -- '-\?hupcl' > "$R/hupcl.txt"
  $SSH "mkdir -p ~/a725b; sudo -n timeout $S tcpdump -i $IFACE -U -s 200 -w a725b/m.pcap" > "$R/tcpdump.log" 2>&1 &
  cap=$!
  timeout $((S+15)) python3 $T/console_poll.py $P "$R/poll.txt" $((S-2)) $I milan_status 'mem_read 0x900006e4 4' 'mem_read 0x900007f0 4' 'mem_read 0x900007e8 4' 'mem_read 0x900007ec 4' 'mem_read 0x90000110 4' > "$R/poll.stdout" 2>&1
  echo "poll rc=$?"
  wait $cap; echo "tcpdump rc=$?"
  scp -q <bench-host-prefix>ubuntu-server:a725b/m.pcap "$R/cap.pcap"
  ls -la "$R/cap.pcap" | cut -c20-
  echo "UNLOCK $(date -Iseconds)"
}
export -f run 2>/dev/null
{ flock -w 300 9 || { echo "no bench lock"; exit 5; }; run; } 9>/tmp/milan-bench.lock
python3 $VALIDATION_STORAGE/829-a725b/tools/row.py "$R" | tee "$R/row.json"
