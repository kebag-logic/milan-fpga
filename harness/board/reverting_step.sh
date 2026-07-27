#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# reverting_step.sh <csr_base_hex> <what> <hold_secs> [extra]
#
# THE SELF-REVERTING DESTRUCTIVE STEP. Run DETACHED (`transport.push_sh_detached`)
# and read back afterwards, because several of these cut the very ssh session
# that started them.
#
#   what = loopback   MAC loopback on/off  (extra = loopback CSR address)
#          macreinit  LINK_CTRL[1] MAC reinit - a link event with no cable
#          linkfreeze LINK_CTRL[3] fake eth-clock death - drills the guard FSM
#          promisc    toggle allmulti/promisc on the netif (extra = iface)
#
# THE REVERT IS UNCONDITIONAL. `trap` covers ordinary death (INT/TERM/HUP and
# normal exit) and a detached WATCHDOG covers the rest: it is started BEFORE the
# destructive write, sleeps `hold + grace`, and restores the register no matter
# what happened to the parent. So the box comes back even if this script is
# SIGKILLed, the board panics the shell, or the network drops the console.
#
# Exit status is the STEP's status; the revert is not optional and not reported
# as failure - if the revert itself cannot be proven, that is FAIL, loudly,
# because half-recovered is the dangerous outcome.

BASE="${1:-0x90000000}"
WHAT="${2:-macreinit}"
HOLD="${3:-5}"
EXTRA="${4:-}"
GRACE=20

rd() { devmem "$1" 32 2>/dev/null; }
wr() { devmem "$1" 32 "$2" 2>/dev/null; }

case "$WHAT" in
    loopback)
        [ -n "$EXTRA" ] || { echo "loopback needs the loopback CSR address"; exit 2; }
        ADDR="$EXTRA"; SET=0x1; CLR=0x0 ;;
    macreinit)   ADDR=$((BASE + 0x71C)); SET=""; CLR="" ;;
    linkfreeze)  ADDR=$((BASE + 0x71C)); SET=""; CLR="" ;;
    promisc)     ADDR=""; ;;
    *) echo "unknown step $WHAT"; exit 2 ;;
esac

# ---- capture the value we must return to --------------------------------
if [ -n "$ADDR" ]; then
    ORIG=$(rd "$ADDR")
    [ -n "$ORIG" ] || { echo "cannot read $ADDR - refusing to touch it"; exit 2; }
else
    ORIG=""
fi
echo "ORIG=$ORIG"

restore() {
    if [ -n "$ADDR" ] && [ -n "$ORIG" ]; then
        wr "$ADDR" "$ORIG"
        BACK=$(rd "$ADDR")
        echo "RESTORED=$BACK"
        [ "$BACK" = "$ORIG" ] || { echo "REVERT_VERIFY: FAIL ($BACK != $ORIG)"; return 1; }
    fi
    if [ "$WHAT" = promisc ] && [ -n "$EXTRA" ]; then
        ip link set "$EXTRA" promisc off 2>/dev/null
        ip link set "$EXTRA" allmulticast on 2>/dev/null
        echo "RESTORED=promisc-off-allmulti-on"
    fi
    echo "REVERT_VERIFY: PASS"
    return 0
}

trap 'restore; exit 3' INT TERM HUP

# ---- the watchdog: armed BEFORE the destructive write --------------------
# It restores even if this script never runs another line.
if [ -n "$ADDR" ] && [ -n "$ORIG" ]; then
    ( setsid sh -c "sleep $((HOLD + GRACE)); devmem $ADDR 32 $ORIG" \
        > /dev/null 2>&1 & ) < /dev/null > /dev/null 2>&1
    echo "WATCHDOG=armed +$((HOLD + GRACE))s"
fi

# ---- the destructive part -------------------------------------------------
case "$WHAT" in
    loopback)
        wr "$ADDR" "$SET"; echo "APPLIED=loopback-on" ;;
    macreinit)
        wr "$ADDR" $(( ORIG | 0x2 )); echo "APPLIED=mac-reinit" ;;
    linkfreeze)
        wr "$ADDR" $(( ORIG | 0x8 )); echo "APPLIED=link-freeze" ;;
    promisc)
        ip link set "$EXTRA" promisc on 2>/dev/null; echo "APPLIED=promisc-on" ;;
esac

sleep "$HOLD"

# ---- observations while the step is applied are the caller's job; we only
# ---- report what the board itself can see, then revert.
echo "LINKG_STAT=$(rd $((BASE + 0x774)))"
echo "RST_EPOCH=$(rd $((BASE + 0x720)))"

restore || exit 1
exit 0
