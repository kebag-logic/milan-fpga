#!/usr/bin/env bash
set -u
echo "LOCK $(date -Iseconds)"
SSH="ssh -o BatchMode=yes <bench-host-prefix>ubuntu-server"
$SSH "sudo -n timeout 70 tcpdump -i <MAC-derived-interface-name> -U -s 96 -w a725b/s.pcap" > $MANAGEMENT/2026-09-23/829-a725b/receipts/stream-2/tcpdump.log 2>&1 &
cap=$!
timeout 80 python3 $VALIDATION_STORAGE/583-a724b/tools/console_poll.py /dev/serial/by-id/<adapter> $MANAGEMENT/2026-09-23/829-a725b/receipts/stream-2/poll.txt 66 5 milan_status 'mem_read 0x900007ec 4' 'mem_read 0x900007e8 4' > $MANAGEMENT/2026-09-23/829-a725b/receipts/stream-2/poll.stdout 2>&1 &
pol=$!
sleep 4
timeout 70 python3 $VALIDATION_STORAGE/829-a725b/tools/connect.py 45 0205022001006000 > $MANAGEMENT/2026-09-23/829-a725b/receipts/stream-2/agent.jsonl 2> $MANAGEMENT/2026-09-23/829-a725b/receipts/stream-2/agent.err
echo "connect rc=$?"
wait $pol; echo "poll rc=$?"
wait $cap; echo "tcpdump rc=$?"
scp -q <bench-host-prefix>ubuntu-server:a725b/s.pcap $VALIDATION_STORAGE/829-a725b/large/stream-2/cap.pcap
ls -la $VALIDATION_STORAGE/829-a725b/large/stream-2/cap.pcap | cut -c20-
echo "UNLOCK $(date -Iseconds)"
