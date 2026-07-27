#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# csr_window.sh <csr_base_hex> <index> <dir 0=listener 1=talker>
#
# One coherent read of the 0x800 indexed per-stream window, in ONE process.
#
# THE DISCIPLINE, in order, and why each step is here:
#   1. write A_STRM_SEL (0x800) = {dir<<8 | idx}.  A SEL write INVALIDATES the
#      ACMP/SRP read snapshots.
#   2. write A_STRM_SNAP (0x804) = 1.  This latches STATE + CNT0..9 + PDUS as
#      ONE coherent block.
#   3. poll A_STRM_SNAP[0] (busy) to 0 before reading anything.  Reading during
#      the burst returns 0 for engine-backed words.
#   4. read the block.
#
# Skipping step 3 is the "snapshot not fresh" trap: the snapshot-served words
# read a literal 0, which looks exactly like "no bind" and is not. The host
# side flags it (`fresh` in csr.window()) but the poll is what avoids it.
#
# Note a running persistence daemon may be moving SEL in its own loop, so the
# host reads the value twice and compares. This script reports SEL readback so
# the host can see whether its selection survived.

BASE="${1:-0x90000000}"
IDX="${2:-0}"
DIR="${3:-0}"

SEL=$((BASE + 0x800))
SNAP=$((BASE + 0x804))

devmem $SEL 32 $(( (DIR << 8) | (IDX & 0xF) )) 2>/dev/null

# Snap, then poll busy. Bounded: 40 polls is far past the engine-arbitrated
# burst, and a stuck busy must fail this step rather than hang the campaign.
devmem $SNAP 32 0x1 2>/dev/null
n=0
while [ $n -lt 40 ]; do
    b=$(devmem $SNAP 32 2>/dev/null)
    case "$b" in
        ""|0x00000000|0) break ;;
    esac
    # Busy is bit 0 only; anything with bit 0 clear is done.
    if [ $(( b & 1 )) -eq 0 ]; then break; fi
    n=$((n + 1))
done
echo "#SNAP_POLLS=$n"
printf '#SEL_READBACK=%s\n' "$(devmem $SEL 32 2>/dev/null)"

for off in 0x810 0x814 0x818 0x81C 0x820 0x824 0x828 0x82C \
           0x830 0x834 0x838 0x83C 0x840 0x844 0x848 0x84C 0x850 0x854 \
           0x858 0x85C 0x860 0x864 0x868; do
    v=$(devmem $((BASE + off)) 32 2>/dev/null)
    [ -n "$v" ] || v=0x00000000
    printf '0x%03X=%s\n' "$off" "$v"
done
