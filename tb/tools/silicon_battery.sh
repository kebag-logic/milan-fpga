#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Post-flash live battery for a Milan end-station board, run FROM the peer
# test host (it needs the AVB subnet; the dev box never gets an address on it).
#
#   silicon_battery.sh <board-ip> [stream-index]
#
# Every number this prints is read from the board. Three rules are baked in
# because each one has already produced a wrong conclusion on this bench:
#
#  1. ALL TEN Milan 5.3.8.10 / 1722.1 Table 7-157 counters, BY NAME. A frozen
#     AVTPRX_ERR (0x6C0) once "proved" a healthy datapath while 9.9 M frames
#     were landing late or early - that register only covers three of the ten.
#  2. The 0x800 window reads ZERO until SNAP is armed. A direct read of
#     0x830+4k looks exactly like a dead counter block. SEL -> SNAP -> poll
#     busy -> read, and every value that will be COMPARED comes from one
#     armed snapshot.
#  3. devmem costs ~0.75 s per call, which is enough to fake a defect: reading
#     `parsed` and `matched` in separate calls once made matched look LARGER
#     than parsed. Anything compared is read in ONE invocation.
#
# A large static count is history; a moving one is a live fault. That is why
# this samples twice and prints the delta - run it with no stream traffic and
# every counter should stand still.
set -u
B=0x90000000
IP=${1:?usage: silicon_battery.sh <board-ip> [stream-index]}
IDX=${2:-0}
SSHO="-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=8"

CNAMES="MEDIA_LOCKED MEDIA_UNLOCKED STREAM_INTERRUPTED SEQ_NUM_MISMATCH \
MEDIA_RESET TIMESTAMP_UNCERTAIN UNSUPPORTED_FORMAT LATE_TIMESTAMP \
EARLY_TIMESTAMP FRAMES_RX"

# One remote shell per sample: see rule 3.
snap() {
  ssh $SSHO "root@$IP" "
    devmem $((B+0x800)) 32 $IDX >/dev/null
    devmem $((B+0x804)) 32 1    >/dev/null
    i=0; while [ \$i -lt 20 ]; do
      case \$(devmem $((B+0x804)) 32) in *0) break;; esac; i=\$((i+1)); done
    k=0; while [ \$k -lt 10 ]; do
      printf '%d ' \$(devmem \$(($((B+0x830))+4*k)) 32); k=\$((k+1)); done
    echo
  " 2>/dev/null
}

echo "=== board $IP  stream index $IDX  $(date -u +%H:%M:%SZ) ==="
ssh $SSHO "root@$IP" "
  printf 'ID       %s\n' \$(devmem $((B+0x000)) 32)
  printf 'VERSION  %s\n' \$(devmem $((B+0x004)) 32)
  printf 'CAP      %s\n' \$(devmem $((B+0x008)) 32)
  printf 'ADP_TALK %s   (0x618 {caps,sources} - RO from 0x0015)\n' \$(devmem $((B+0x618)) 32)
  printf 'ADP_LIST %s   (0x61C {caps,sinks})\n'   \$(devmem $((B+0x61C)) 32)
  printf 'GM_HI    %s\n' \$(devmem $((B+0x624)) 32)
  printf 'GM_LO    %s\n' \$(devmem $((B+0x628)) 32)
  printf 'LWSRP    %s   (0x694 - sample repeatedly for flapping)\n' \$(devmem $((B+0x694)) 32)
  printf 'CLKV_CTL %s   (0x778 - 0 on pre-0x0016 gateware = UNMAPPED, not clear)\n' \$(devmem $((B+0x778)) 32)
  printf 'CLKV_STAT %s  (0x77C)\n' \$(devmem $((B+0x77C)) 32)
  printf 'CLKV_TUCNT %s (0x780 - Milan Table 5.4, per 1 s interval)\n' \$(devmem $((B+0x780)) 32)
" 2>/dev/null

A=$(snap); sleep 30; C=$(snap)
[ -n "$A" ] && [ -n "$C" ] || { echo "FAIL: no snapshot from $IP"; exit 1; }

echo
printf '%-22s %14s %14s  %s\n' counter t0 delta rate
i=1
for n in $CNAMES; do
  v0=$(echo "$A" | cut -d' ' -f$i); v1=$(echo "$C" | cut -d' ' -f$i)
  d=$((v1 - v0))
  if [ "$d" -ne 0 ]; then r="$((d / 30))/s  MOVING"; else r=""; fi
  printf '%-22s %14s %14s  %s\n' "$n" "$v0" "$d" "$r"
  i=$((i + 1))
done

# The one arithmetic check worth automating: on a healthy listener the frames
# that arrived should NOT all be late or early.
f0=$(echo "$A" | cut -d' ' -f10); f1=$(echo "$C" | cut -d' ' -f10)
l0=$(echo "$A" | cut -d' ' -f8);  l1=$(echo "$C" | cut -d' ' -f8)
e0=$(echo "$A" | cut -d' ' -f9);  e1=$(echo "$C" | cut -d' ' -f9)
df=$((f1 - f0)); dl=$((l1 - l0)); de=$((e1 - e0))
echo
if [ "$df" -eq 0 ]; then
  echo "VERDICT: no frames received in the window - counters above are HISTORY,"
  echo "         not a live measurement. Bind a stream before judging health."
else
  echo "VERDICT: $df frames, $((dl + de)) late-or-early = $(( (dl + de) * 100 / df ))%"
fi
