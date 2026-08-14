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
#   6. pp memory-bridge bank present    (0x5B tag, DFI handover seen)
#   7. descriptor bridge completed      (issued == acked, no err, no timeout)
#   8. response bridge completed        (same rails, AECP response path)
#
# busybox-safe: plain sh, no pgrep -c, values surfaced as NAME=value echoes.
# Overrides: IFACE, MILAN_CSR_BASE, DMA_TS_OFF_REG, PPMEM_BASE, RX_WAIT,
# TS_WAIT. PPMEM_BASE=none declares a build with no protocol processor and
# prints a SKIPPED line instead of checks 6-8.
# DT-rot caution (TROUBLESHOOTING section 20): DMA_TS_OFF_REG must match the
# FLASHED build's csr.csv - a wrong-but-writable address reads back happily.
# This script pokes physical addresses directly (devmem), NOT the DT windows,
# which is exactly why it catches the stale-DTB class the driver cannot see.
# The same caution applied to this script itself: until 2026-08-14 the default
# was 0xf00030a4, which csr.csv names milan_dma_rx1_wr_ptr, so check 2 graded
# the RX ring and passed on boards whose ts records never left the fabric.

IFACE="${IFACE:-eth0}"
BASE="${MILAN_CSR_BASE:-0x90000000}"
# csr.csv csr_register,milan_dma_ts_offset,0xf0003118 (build_ax7101_asl_dfigate).
TS_OFF_REG="${DMA_TS_OFF_REG:-0xf0003118}"
# csr.csv csr_base,ppmem,0xf000f800; the five words are +0x00 desc_req,
# +0x04 desc_fault, +0x08 resp_req, +0x0c resp_fault, +0x10 stat.
PPMEM="${PPMEM_BASE:-0xf000f800}"
RX_WAIT="${RX_WAIT:-15}"
TS_WAIT="${TS_WAIT:-30}"

fails=0
checks=0
verdict() {  # $1 name, $2 0=pass else fail, $3 detail
    checks=$((checks + 1))
    if [ "$2" -eq 0 ]; then
        echo "CHECK $1: PASS $3"
    else
        echo "CHECK $1: FAIL $3"
        fails=$((fails + 1))
    fi
}

echo "== hostplane post-flash smoke (iface=$IFACE csr=$BASE ts=$TS_OFF_REG ppmem=$PPMEM) =="

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

# ---- 6-8. protocol-processor memory bridges (LiteX CSR bank) --------------
# The entity model is fetched, and every AECP response written back, through
# two wishbone masters with no port into the 0x9000_0000 window; PP_STAT
# reports the same fault whether a bridge never asked the bus or asked and was
# never answered. On 2026-08-13 that ambiguity cost a board week: 16 issued,
# 0 acked, 16 timed out, while every other check on this page passed.

# $1 label, $2 req reg, $3 fault reg, $4 1 = a bridge that never asked is
# itself the fault. Both rails saturate at 0xFFFF, so equality there proves
# only that no fault was counted.
pp_bridge() {
    pb_req=$(devmem "$2" 32 2>/dev/null)
    pb_flt=$(devmem "$3" 32 2>/dev/null)
    pb_name="pp-$(echo "$1" | tr 'A-Z' 'a-z')-bridge"
    echo "PPMEM_${1}_REQ=$pb_req PPMEM_${1}_FAULT=$pb_flt"
    if [ -z "$pb_req" ] || [ -z "$pb_flt" ]; then
        verdict "$pb_name" 1 "(counters unreadable at $2 / $3)"
        return
    fi
    pb_iss=$(( pb_req >> 16 ));  pb_ack=$(( pb_req & 0xFFFF ))
    pb_err=$(( pb_flt >> 16 ));  pb_tmo=$(( pb_flt & 0xFFFF ))
    echo "PPMEM_${1}: issued=$pb_iss acked=$pb_ack errored=$pb_err timed_out=$pb_tmo"
    # An access issued and never acked is the wedge itself, and the processor
    # reports it as an invalid image - the same word it uses for an image that
    # is merely wrong.
    if [ "$pb_iss" -ne "$pb_ack" ]; then
        verdict "$pb_name" 1 "($pb_iss issued, $pb_ack acked - $((pb_iss - pb_ack)) access(es) the bus never completed)"
    # A refused or abandoned access reaches the entity as that same one word.
    elif [ "$pb_err" -ne 0 ] || [ "$pb_tmo" -ne 0 ]; then
        verdict "$pb_name" 1 "($pb_err errored, $pb_tmo timed out - the memory refused or never answered)"
    # 0 issued is a request path that never ran, and on these counters it reads
    # exactly like a healthy bus with nothing to do.
    elif [ "$4" -eq 1 ] && [ "$pb_iss" -eq 0 ]; then
        verdict "$pb_name" 1 "(0 issued - the bridge never asked the bus; the image walk never ran, read PP_DIAG 0x930)"
    else
        verdict "$pb_name" 0 "($pb_iss issued, $pb_ack acked, no faults)"
    fi
}

if [ "$PPMEM" = none ]; then
    # A build with no protocol processor has no such bank (the Arty configs
    # carry none). Declaring that costs one line; letting an absent bank read
    # as four zero counters is the reading these checks exist to refuse.
    echo "PPMEM_STAT=skipped"
    echo "CHECK pp-bridges: SKIPPED (PPMEM_BASE=none - build declared to carry no protocol processor)"
else
    PP_STAT=$(devmem $((PPMEM + 0x10)) 32 2>/dev/null)
    echo "PPMEM_STAT=$PP_STAT"
    if [ -z "$PP_STAT" ]; then
        verdict "pp-bridge-bank" 1 "(ppmem stat unreadable at $PPMEM +0x10)"
    # A bitstream built before this bank reads 0 at all five words, which is
    # the reading of a bus that never faulted: the tag is what separates them.
    elif [ $(( (PP_STAT >> 24) & 0xFF )) -ne $((0x5B)) ]; then
        verdict "pp-bridge-bank" 1 "(PPMEM_STAT=$PP_STAT - no 0x5B tag, this gateware predates the bank; the counters below read 0 whatever the bus did)"
    # Bridges held off the bus (the BIOS never finished sdram_init) also read
    # 0 issued and 0 faults, and that is a dead entity model, not a quiet one.
    elif [ $(( (PP_STAT >> 4) & 1 )) -ne 1 ]; then
        verdict "pp-bridge-bank" 1 "(PPMEM_STAT=$PP_STAT - stat[4]=0, the DFI handover was never seen: both bridges answer err without touching the bus)"
    else
        verdict "pp-bridge-bank" 0 "(PPMEM_STAT=$PP_STAT)"
    fi

    # The descriptor face walks the image at startup, so 0 there is a fault.
    # The response face only moves once a controller has sent an AECP command,
    # so on a quiet bench 0 is legitimate and only the fault rails condemn it.
    pp_bridge DESC $((PPMEM + 0x00)) $((PPMEM + 0x04)) 1
    pp_bridge RESP $((PPMEM + 0x08)) $((PPMEM + 0x0c)) 0
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
if [ -z "$TS0" ]; then
    # An unreadable baseline followed by any later read compares unequal, so
    # the advance test would report a PASS built on a read that failed.
    verdict "ts-ring" 1 "(TS offset unreadable at $TS_OFF_REG - check it against the FLASHED build's csr.csv)"
else
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
    echo "HOSTPLANE SMOKE: PASS ($checks/$checks)"
    exit 0
else
    echo "HOSTPLANE SMOKE: FAIL ($fails check(s) failed)"
    exit 1
fi
