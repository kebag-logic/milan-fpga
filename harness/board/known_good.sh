#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# known_good.sh <csr_base_hex> <version_expect_hex> <netif> [pcm_ring_csr_hex]
#
# Assert the board is in a KNOWN-GOOD state - not merely that it responds.
#
# HALF-RECOVERED IS THE DANGEROUS OUTCOME. A board that answers ssh, answers
# devmem and has a listener reporting "bound" can still be accepting nothing:
# that combination is exactly the accept blocker, where every control-plane
# indication was healthy and the media plane was dead. "Responds" is therefore
# not a recovery criterion; each check below is a POSITIVE assertion about a
# specific plane, and the media check is a MOVEMENT check, not a state read.
#
# Checks (one verdict line each, nonzero exit on any FAIL):
#   1. CSR plane   ID = "MILN" and VERSION = the campaign's expected word
#   2. VID trap    AAF_CTRL[27:16] = 2 (a VID-0 stream floods UNSHAPED)
#   3. safety rail no talker context t>0 armed while LWSRP_CTRL[0] = 0
#   4. link        LINKG_STAT rx_alive and the guard not holding a reinit
#   5. host plane  kernel rx_packets advances
#   6. media       APRB_PARSED advances (frames really reach the RX parser)
#
# Check 6 is the one that separates known-good from responsive: it is the view
# UPSTREAM of the stream-table match, so it moves whenever AVTP frames arrive
# at all - before any question of binding.

BASE="${1:-0x90000000}"
WANT_VER="${2:-}"
IFACE="${3:-eth0}"

fails=0
verdict() {
    if [ "$2" -eq 0 ]; then echo "CHECK $1: PASS $3"
    else echo "CHECK $1: FAIL $3"; fails=$((fails + 1)); fi
}
rd() { devmem $((BASE + $1)) 32 2>/dev/null; }

# ---- 1. CSR plane ---------------------------------------------------------
ID=$(rd 0x000); VER=$(rd 0x004)
echo "ID=$ID"; echo "VERSION=$VER"
case "$ID" in
    0x4D494C4E|0x4d494c4e) verdict csr-id 0 "(VERSION=$VER)" ;;
    *) verdict csr-id 1 "(ID=$ID expected 0x4D494C4E)" ;;
esac
if [ -n "$WANT_VER" ]; then
    if [ $((VER)) -eq $((WANT_VER)) ]; then
        verdict csr-version 0 "($VER)"
    else
        verdict csr-version 1 "(VERSION=$VER expected $WANT_VER - wrong gateware)"
    fi
fi

# ---- 2. AAF_CTRL VID field ------------------------------------------------
AAF=$(rd 0x654); echo "AAF_CTRL=$AAF"
if [ -z "$AAF" ]; then
    verdict aaf-vid 1 "(unreadable)"
elif [ $(( (AAF >> 16) & 0xFFF )) -eq 2 ]; then
    verdict aaf-vid 0 "($AAF)"
else
    verdict aaf-vid 1 "($AAF - VID field is not 2; an unregistered VID-0 stream floods unshaped)"
fi

# ---- 3. the t>0 / engine-off safety rail ----------------------------------
LW=$(rd 0x680); echo "LWSRP_CTRL=$LW"
armed=0
i=1
while [ $i -lt 8 ]; do
    devmem $((BASE + 0x800)) 32 $(( (1 << 8) | i )) 2>/dev/null
    devmem $((BASE + 0x804)) 32 0x1 2>/dev/null
    st=$(devmem $((BASE + 0x82C)) 32 2>/dev/null)
    [ -n "$st" ] || st=0
    # STATE[3] = composed admission. 0xDEADDEAD = not backed here, not armed.
    case "$st" in
        0xDEADDEAD|0xdeaddead) : ;;
        *) if [ $(( (st >> 3) & 1 )) -eq 1 ]; then armed=$((armed + 1)); fi ;;
    esac
    i=$((i + 1))
done
devmem $((BASE + 0x800)) 32 0 2>/dev/null
echo "TALKER_T_GT_0_ARMED=$armed"
if [ "$armed" -gt 0 ] && [ $(( LW & 1 )) -eq 0 ]; then
    verdict safety-rail 1 "($armed t>0 context(s) armed with the lwSRP engine OFF - unpaced blast risk)"
else
    verdict safety-rail 0 "(armed=$armed lwsrp_en=$(( LW & 1 )))"
fi

# ---- 4. link guard --------------------------------------------------------
LG=$(rd 0x774); echo "LINKG_STAT=$LG"
if [ -z "$LG" ]; then
    verdict link-guard 1 "(unreadable)"
elif [ $(( LG & 1 )) -eq 1 ] && [ $(( (LG >> 6) & 1 )) -eq 0 ]; then
    verdict link-guard 0 "($LG rx_alive, no reinit held)"
else
    verdict link-guard 1 "($LG rx_alive=$(( LG & 1 )) guard_rst=$(( (LG >> 6) & 1 )))"
fi

# ---- 5. host plane --------------------------------------------------------
RX0=$(cat /sys/class/net/"$IFACE"/statistics/rx_packets 2>/dev/null)
# ---- 6. media plane: read APRB_PARSED around the same wait ----------------
AP0=$(rd 0x8B4)
sleep 5
RX1=$(cat /sys/class/net/"$IFACE"/statistics/rx_packets 2>/dev/null)
AP1=$(rd 0x8B4)
echo "RX_PACKETS=$RX0->$RX1"
echo "APRB_PARSED=$AP0->$AP1"

if [ -n "$RX0" ] && [ -n "$RX1" ] && [ "$RX1" -gt "$RX0" ]; then
    verdict host-plane 0 "(+$((RX1 - RX0)) frames in 5s)"
else
    verdict host-plane 1 "(rx_packets stuck at $RX0 - host RX dead)"
fi

if [ -n "$AP0" ] && [ -n "$AP1" ] && [ $((AP1)) -gt $((AP0)) ]; then
    verdict media-plane 0 "(parser saw $(( $((AP1)) - $((AP0)) )) AVTP frames in 5s)"
else
    verdict media-plane 1 "(APRB_PARSED static at $AP0 - no AVTP frames reach the parser at all)"
fi

echo "----------------------------------------------------------"
if [ "$fails" -eq 0 ]; then
    echo "KNOWN_GOOD: PASS"
    exit 0
fi
echo "KNOWN_GOOD: FAIL ($fails check(s))"
exit 1
