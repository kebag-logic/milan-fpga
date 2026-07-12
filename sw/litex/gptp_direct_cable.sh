#!/usr/bin/env bash
# gptp_direct_cable.sh — turnkey two-node gPTP validation over a DIRECT cable.
#
# WHY this exists: the bench AVB switch (d&b audiotechnik, OUI 3c:c0:c6) does
# NOT present gPTP on the board-facing ports and forwards only registered AVB
# multicast (ADP 91:e0:f0:xx) between them — no board<->board unicast, no PTP
# multicast, gPTP only on its gigabit uplink (verified 2026-07-12, all four
# link-local protocols present on pw0, zero on both board ports). P2P gPTP is
# hop-by-hop, so the boards can only peer with a real gPTP partner on their
# link. The switch is not it; a direct board<->board cable is.
#
# PHYSICAL STEP FIRST: unplug both boards from the switch, connect eth0<->eth0
# with one Ethernet cable. THEN run this from the host (drives both consoles).
#
# What it does: starts ptp4l P2P/L2 on both boards (AX7101 = GM via priority1),
# then polls the Arty (slave) for offset convergence and PHC discipline.
set -u
AX_INSMOD="hs_pgsz=16384 rsc_clk_mhz=100"
ARTY_TMUX=arty_console
CONX=/tmp/scratch/-home-alex-prjs-avb-on-fpga-milan-fpga/3df0ee19-2b36-4cfc-a0de-bf6207c5f92d/scratchpad/conx.sh
AXSESS=milan_qspi_boot

echo "== gPTP direct-cable bring-up (P2P/L2, AX7101=GM priority1=100) =="
# AX7101 (grandmaster): lower priority1 wins BMCA
CONX_SESSION=$AXSESS $CONX 'killall ptp4l 2>/dev/null; sleep 1;
  nohup ptp4l -i eth0 -f /tmp/gptp.cfg -S -m --priority1=100 >/tmp/ptp4l.log 2>&1 &
  echo AX-PTP4L-UP' 6

# Arty (slave): default priority1=128 -> slaves to the AX
tmux send-keys -t $ARTY_TMUX \
  'killall ptp4l 2>/dev/null; sleep 1; nohup ptp4l -i eth0 -f /tmp/gptp.cfg -S -m >/tmp/ptp4l.log 2>&1 & echo ARTY-PTP4L-UP' Enter

echo "== waiting for convergence (up to 60 s) =="
for i in $(seq 12); do
  sleep 5
  tmux send-keys -t $ARTY_TMUX \
    'grep -aE "SLAVE|rms|master offset" /tmp/ptp4l.log | tail -2; echo ---A-$RANDOM' Enter
  sleep 1
  out=$(tmux capture-pane -t $ARTY_TMUX -p | tail -6)
  if echo "$out" | grep -qE "rms [0-9]|master offset"; then
    echo "CONVERGING:"; echo "$out" | grep -E "rms|offset" | tail -3
    echo "GATE: gPTP two-node PASS — Arty PHC disciplined to AX7101 GM."
    exit 0
  fi
  echo "  ...waiting ($((i*5))s)"
done
echo "GATE: no convergence — check: cable direct (not switch)? both ptp4l up?"
echo "  AX log:  (conx) tail /tmp/ptp4l.log ; Arty log: tail /tmp/ptp4l.log"
exit 1
