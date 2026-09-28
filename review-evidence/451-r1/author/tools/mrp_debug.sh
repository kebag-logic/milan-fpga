#!/bin/sh
# Controller host, under sudo, inside with_gptp.py; bench lock held by the caller.
# Records every MSRP/MVRP frame on the port (both directions) while the
# software listener declares for 25 s.
cd /tmp/a403 || exit 1
# IFACE, IFACE_MAC, TALKER_EID: the controller AVB interface, its MAC and the endpoint id
timeout 40 tcpdump -n -U -i "$IFACE" -w /tmp/a403/mrp.pcap 'ether proto 0x22ea or ether proto 0x88f5' 2>/dev/null &
TD=$!
sleep 1
timeout 35 python3 -B din_listener.py "$IFACE" 25 /tmp/a403/mrp-din.pcap /tmp/a403/mrp-listener.jsonl
wait $TD
cat /tmp/a403/mrp-listener.jsonl
