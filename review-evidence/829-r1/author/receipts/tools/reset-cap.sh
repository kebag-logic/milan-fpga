#!/usr/bin/env bash
# reset-cap.sh <out> <seconds>: tap capture and read-only polls across one console reset of the Arty's SoC; caller holds the bench lock.
set -u
R=$1; S=$2
mkdir -p "$R"
P=/dev/serial/by-id/<adapter>
T=$VALIDATION_STORAGE/583-a724b/tools
SSH="ssh -o BatchMode=yes <bench-host-prefix>ubuntu-server"
IFACE=<MAC-derived-interface-name>
echo "LOCK $(date -Iseconds)"
$SSH "mkdir -p ~/a725b; sudo -n timeout $S tcpdump -i $IFACE -U -s 200 -w a725b/boot.pcap" > "$R/tcpdump.log" 2>&1 &
cap=$!
timeout 3 tail -f /dev/null
stty -F $P hupcl; stty -F $P -hupcl
echo "reset(dtr) done $(date +%s.%N)" | tee "$R/reset-time.txt"
python3 $T/console_log.py $P "$R/console-boot.txt" 9
timeout $((S+5)) python3 $T/console_poll.py $P "$R/poll.txt" $((S-16)) ${POLL_PERIOD:-3} milan_status 'mem_read 0x900007e8 4' 'mem_read 0x900007f0 4' 'mem_read 0x90000784 4' 'mem_read 0x900007ec 4' 'mem_read 0x90000110 4' > "$R/poll.stdout" 2>&1
echo "poll rc=$?"
wait $cap; echo "tcpdump rc=$?"
scp -q <bench-host-prefix>ubuntu-server:a725b/boot.pcap "$R/cap.pcap"
ls -la "$R/cap.pcap" | cut -c20-
echo "UNLOCK $(date -Iseconds)"
