#!/usr/bin/env bash
# account.sh <out> <gap>: tap capture around one accounting window; caller holds the bench lock.
set -u
R=$1; S=$2
mkdir -p $R
P=/dev/serial/by-id/<adapter>
SSH="ssh -o BatchMode=yes <bench-host-prefix>ubuntu-server"
echo "LOCK $(date -Iseconds)"
$SSH "mkdir -p ~/a725b; sudo -n timeout $((S+8)) tcpdump -i <MAC-derived-interface-name> -U -s 200 -w a725b/a.pcap" > $R/tcpdump.log 2>&1 &
cap=$!
timeout 2 tail -f /dev/null
python3 $VALIDATION_STORAGE/829-a725/tools/account.py $P $R/console.txt $S; echo "account rc=$?"
wait $cap; echo "tcpdump rc=$?"
scp -q <bench-host-prefix>ubuntu-server:a725b/a.pcap $R/cap.pcap
echo "UNLOCK $(date -Iseconds)"
