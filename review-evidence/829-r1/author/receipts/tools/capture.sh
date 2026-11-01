#!/usr/bin/env bash
# capture.sh <out> <seconds> [console commands]: tap capture of the Arty's link with a read-only console poll; caller holds the bench lock.
set -u
R=$1; S=$2; I=${POLL_PERIOD:-5}; shift 2
mkdir -p "$R"
P=/dev/serial/by-id/<adapter>
T=$VALIDATION_STORAGE/583-a724b/tools
SSH="ssh -o BatchMode=yes <bench-host-prefix>ubuntu-server"
IFACE=<MAC-derived-interface-name>
echo "LOCK $(date -Iseconds)"
stty -F $P -a | tr ';' '\n' | grep -a -o -- '-\?hupcl' > "$R/hupcl.txt"; cat "$R/hupcl.txt"
$SSH "mkdir -p ~/a725b; sudo -n timeout $S tcpdump -i $IFACE -U -s ${SNAP:-200} -w a725b/c.pcap" > "$R/tcpdump.log" 2>&1 &
cap=$!
if [ "$#" -gt 0 ]; then
  timeout $((S+15)) python3 $T/console_poll.py $P "$R/poll.txt" $((S-2)) "$I" "$@" > "$R/poll.stdout" 2>&1
  echo "poll rc=$?"
fi
wait $cap; echo "tcpdump rc=$?"
scp -q <bench-host-prefix>ubuntu-server:a725b/c.pcap "$R/cap.pcap"
ls -la "$R/cap.pcap" | cut -c20-
echo "UNLOCK $(date -Iseconds)"
