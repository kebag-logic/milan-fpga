#!/bin/sh
# Controller host, under sudo, bench lock held by the caller. Bounded: every
# child has a timeout and is waited for. Captures ADP/ACMP around one bind of
# DUT STREAM_INPUT 0 to the software talker, then unbinds.
cd /tmp/a403 || exit 1
# IFACE, IFACE_MAC, TALKER_EID: the controller AVB interface, its MAC and the endpoint id
timeout 40 tcpdump -n -U -i "$IFACE" -w /tmp/a403/probe.pcap 'ether proto 0x22f0 and not (ether src "$IFACE_MAC" and ether[14] == 0x02)' 2>/tmp/a403/probe-tcpdump.txt &
TD=$!
timeout 38 python3 -B aaf_talker.py "$IFACE" 30 /tmp/a403/probe-talker.jsonl 0 &
TK=$!
sleep 6
timeout 10 python3 -B avdecc_rw.py bind "$IFACE" "$TALKER_EID" 0 020000fffe000001 0
sleep 12
timeout 10 python3 -B avdecc_rw.py unbind "$IFACE" "$TALKER_EID" 0 020000fffe000001 0
wait $TK
echo talker_rc=$?
wait $TD
cat /tmp/a403/probe-talker.jsonl | grep -v progress
tcpdump -n -e -r /tmp/a403/probe.pcap 2>/dev/null | wc -l
tcpdump -n -e -x -r /tmp/a403/probe.pcap 'ether[14] == 0xfc' 2>/dev/null | head -80
