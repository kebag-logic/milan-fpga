#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# hostplane_smoke.sh - MANDATORY first step after every flash, run ON THE
# BOARD shell (~60 s). Catches the host-plane regression class in one pass:
# a build whose fabric paths (AAF/CRF/SRP/ADP) run perfectly while the host
# plane is dead (no RX frames to the kernel, no TX timestamp records) looks
# healthy on every audio drill - THIS is the drill that looks at the host.
#
# Checks (one PASS/FAIL verdict line each, final verdict, nonzero exit on
# any FAIL):
#   1. rx_packets increments            (kernel really receives frames)
#   2. dma-ts ring offset advances      (ts records really reach DRAM;
#      gPTP's pdelay cadence feeds it even while sync is still hunting)
#   3. ID=MILN + VERSION readable       (CSR plane alive, right gateware)
#   4. AAF_CTRL VID field intact        (0x0002xxxx - the VID-2 clobber trap)
#   5. ALSA card module loaded          (snd_kl_* present)
#
# busybox-safe: plain sh, no pgrep -c, values surfaced as NAME=value echoes.
# Overrides: IFACE, MILAN_CSR_BASE, DMA_TS_OFF_REG, RX_WAIT, TS_WAIT.
# DT-rot caution (TROUBLESHOOTING section 20): DMA_TS_OFF_REG must match the
# FLASHED build's csr.csv - a wrong-but-writable address reads back happily.
# This script pokes physical addresses directly (devmem), NOT the DT windows,
# which is exactly why it catches the stale-DTB class the driver cannot see.

IFACE="${IFACE:-eth0}"
BASE="${MILAN_CSR_BASE:-0x90000000}"
TS_OFF_REG="${DMA_TS_OFF_REG:-0xf00030a4}"
RX_WAIT="${RX_WAIT:-15}"
TS_WAIT="${TS_WAIT:-30}"

fails=0
verdict() {  # $1 name, $2 0=pass else fail, $3 detail
    if [ "$2" -eq 0 ]; then
        echo "CHECK $1: PASS $3"
    else
        echo "CHECK $1: FAIL $3"
        fails=$((fails + 1))
    fi
}

echo "== hostplane post-flash smoke (iface=$IFACE csr=$BASE ts=$TS_OFF_REG) =="

# ---- 3. CSR identity first (everything else is noise if this fails) --------
ID=$(devmem $((BASE + 0x000)) 32 2>/dev/null)
echo "ID=$ID"
VER=$(devmem $((BASE + 0x004)) 32 2>/dev/null)
echo "VERSION=$VER"
case "$ID" in
    0x4D494C4E|0x4d494c4e) verdict "id-miln" 0 "(ID=$ID VERSION=$VER)";;
    *)                     verdict "id-miln" 1 "(ID=$ID expected 0x4D494C4E)";;
esac

# ---- 4. AAF_CTRL VID field (the VID-0 flood trap: must stay 0x0002xxxx) ----
AAF=$(devmem $((BASE + 0x654)) 32 2>/dev/null)
echo "AAF_CTRL=$AAF"
if [ -z "$AAF" ]; then
    verdict "aaf-vid" 1 "(AAF_CTRL unreadable)"
else
    AAF_HI=$(( AAF >> 16 ))
    if [ "$AAF_HI" -eq 2 ]; then
        verdict "aaf-vid" 0 "(AAF_CTRL=$AAF)"
    else
        verdict "aaf-vid" 1 "(AAF_CTRL=$AAF - VID field is not 0x0002)"
    fi
fi

# ---- 1. kernel RX liveness ---------------------------------------------------
RX0=$(cat /sys/class/net/"$IFACE"/statistics/rx_packets 2>/dev/null)
echo "RX_PACKETS_T0=$RX0"
if [ -z "$RX0" ]; then
    verdict "rx-packets" 1 "(no $IFACE statistics)"
else
    sleep "$RX_WAIT"
    RX1=$(cat /sys/class/net/"$IFACE"/statistics/rx_packets 2>/dev/null)
    echo "RX_PACKETS_T1=$RX1"
    if [ -n "$RX1" ] && [ "$RX1" -gt "$RX0" ]; then
        verdict "rx-packets" 0 "(+$((RX1 - RX0)) in ${RX_WAIT}s)"
    else
        verdict "rx-packets" 1 "(stuck at $RX0 for ${RX_WAIT}s - host RX dead)"
    fi
fi

# ---- 2. dma-ts ring offset advances (poll up to TS_WAIT in 5 s steps) -----
TS0=$(devmem "$TS_OFF_REG" 32 2>/dev/null)
echo "TS_OFFSET_T0=$TS0"
TS_OK=1
TS1=""
t=0
while [ "$t" -lt "$TS_WAIT" ]; do
    sleep 5
    t=$((t + 5))
    TS1=$(devmem "$TS_OFF_REG" 32 2>/dev/null)
    if [ -n "$TS1" ] && [ "$TS1" != "$TS0" ]; then TS_OK=0; break; fi
done
echo "TS_OFFSET_T1=$TS1"
if [ "$TS_OK" -eq 0 ]; then
    verdict "ts-ring" 0 "($TS0 -> $TS1 in ${t}s)"
else
    verdict "ts-ring" 1 "(stuck at $TS0 for ${TS_WAIT}s - no ts records; is gPTP running?)"
fi

# ---- 5. ALSA card module -----------------------------------------------------
SND=$(grep -c '^snd_kl' /proc/modules 2>/dev/null)
echo "SND_KL_MODULES=$SND"
if [ -n "$SND" ] && [ "$SND" -gt 0 ]; then
    verdict "alsa-module" 0 "($SND snd_kl_* module(s))"
else
    CARDS=$(cat /proc/asound/cards 2>/dev/null | grep -c '\[')
    echo "ASOUND_CARDS=$CARDS"
    if [ -n "$CARDS" ] && [ "$CARDS" -gt 0 ]; then
        verdict "alsa-module" 0 "(built-in: $CARDS card(s) in /proc/asound/cards)"
    else
        verdict "alsa-module" 1 "(no snd_kl_* module, no ALSA card)"
    fi
fi

echo "--------------------------------------------------------------"
if [ "$fails" -eq 0 ]; then
    echo "HOSTPLANE SMOKE: PASS (5/5)"
    exit 0
else
    echo "HOSTPLANE SMOKE: FAIL ($fails check(s) failed)"
    exit 1
fi
