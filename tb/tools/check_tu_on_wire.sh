#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Read the AVTP "tu" (timestamp uncertain) bit straight off the wire for one
# talker. Run FROM a host that can actually SEE the stream.
#
#   check_tu_on_wire.sh <iface> <talker-mac> [seconds] [--tap]
#
# WHY THIS EXISTS. tu is the ONLY conformant lever a Milan talker has when its
# clock is not trustworthy: Milan v1.2 5.3.7.3 forbids stopping a Stream Output
# ("STREAMING_WAIT shall not be implemented") and IEEE 1722-2016 7.5 makes tv=1
# mandatory on every AAF AVTPDU at sp=0, so the talker can neither go silent nor
# mark the timestamp invalid - it must say UNCERTAIN and keep streaming. Milan
# 4.3.5.2 upgrades IEEE 1722 4.4.4.7 from *should* to *shall*.
#
# WHERE TO RUN IT. The AVB switch forwards a stream ONLY to registered
# listeners, so the peer test host does NOT see stream frames it has not
# subscribed to - a capture there returns a handful of ADP/ACMP control frames
# and nothing else. Use an inline ProfiShark tap for stream traffic and pass
# --tap: those records carry a 28-byte header, so every offset shifts by +28.
#
# WHERE THE BIT IS. The fabric writes fb[21] = {7'h00, tu}: frame byte 21,
# which is AVTPDU byte 3 once the 14-byte Ethernet header and the 4-byte VLAN
# tag are counted. The frames are matched EXACTLY - TPID 0x8100, ethertype
# 0x22F0, subtype 0x02 (AAF) - because ADP/ACMP/MAAP share ethertype 0x22F0 and
# their byte 21 means something else entirely. Filtering only on the source MAC
# once produced a "MIXED" verdict built from three control frames.
#
# READING THE RESULT. tu = 1 on every frame is the CORRECT state for a board
# whose gPTP daemon has not leased CLKV_CTRL (0x778): reset is no-lease, and an
# unknown clock state means NOT valid. tu = 0 has to be earned by a live lease.
set -u
IF=${1:?usage: check_tu_on_wire.sh <iface> <talker-mac> [seconds] [--tap]}
MAC=${2:?talker source MAC, e.g. 02:00:00:00:00:01}
SECS=${3:-10}
O=0
[ "${4:-}" = "--tap" ] && O=28

AAF="ether src $MAC and ether[$((O+12)):2] == 0x8100 and ether[$((O+16)):2] == 0x22f0 and ether[$((O+18))] == 0x02"
PCAP=$(mktemp /tmp/tu_XXXXXX.pcap)
trap 'rm -f "$PCAP"' EXIT

echo "=== tu on the wire: $MAC on $IF, ${SECS}s (offset +$O) ==="
sudo timeout "$SECS" tcpdump -i "$IF" -s 64 -w "$PCAP" -nn "$AAF" >/dev/null 2>&1

# One capture, two reads: the counts are of the SAME frames, so they cannot
# drift the way two live captures would.
n=$(tcpdump -r "$PCAP" -nn 2>/dev/null | wc -l)
t1=$(tcpdump -r "$PCAP" -nn "ether[$((O+21))] & 1 == 1" 2>/dev/null | wc -l)
t0=$((n - t1))

if [ "$n" -eq 0 ]; then
  echo "NO AAF FRAMES from this talker - it is not streaming, or this host is"
  echo "not on a path that carries the stream (switch prunes to registered"
  echo "listeners; use an inline tap and --tap)."
  exit 1
fi
echo "frames=$n  tu=1: $t1  tu=0: $t0"
if   [ "$t1" -eq "$n" ]; then echo "VERDICT: tu SET on every frame - talker declares its clock UNCERTAIN"
elif [ "$t0" -eq "$n" ]; then echo "VERDICT: tu CLEAR on every frame - talker claims a VALID clock"
else echo "VERDICT: MIXED ($t1/$n set) - tu changed during the window (a lease was taken or lapsed)"
fi
