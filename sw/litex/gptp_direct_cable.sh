#!/usr/bin/env bash
# gptp_direct_cable.sh — turnkey two-node gPTP validation over a DIRECT cable,
# HARDWARE timestamps on both ends (Phase B gateware, hwts5/eto_hwts_ax2+).
#
# WHY a direct cable: the bench AVB switch (d&b audiotechnik) runs pdelay on
# its edge ports and relays a BOARD grandmaster's Sync/Follow_Up to the
# gigabit uplink (Arty-GM -> pw0 rms 2-4 ns, proven 2026-07-13), but the
# uplink->board direction is flap-suppression-flaky and board<->board carries
# only registered AVB multicast. P2P gPTP is hop-by-hop, so the one topology
# that exercises the UNTESTED role — Arty as HW-timestamped SLAVE — is a
# direct board<->board cable.
#
# PHYSICAL STEP FIRST: unplug both boards from the switch, connect eth0<->eth0
# with one cable. THEN run this from the host (it drives both tmux consoles).
#
# What it does:
#   AX7101 (console tmux '$AXSESS')  = GM: clockClass 6 / priority1 100
#   Arty   (console tmux '$ARTYSESS') = slave: stock /etc/gptp.cfg
# Both run ptp4l in HW-timestamp mode (no -S; linuxptp defaults to hardware
# and the kl-eth PHC + dma-ts ring are flash-default since hwts5). Gates:
#   1. Arty reaches SLAVE with servo rms converging
#   2. peerMeanPathDelay in the HW-grade range (~1-3 us; SW stamps read ~600 us)
#   3. zero "timed out while polling for tx timestamp" on either end
# Both boards are turnkey: DT-derived PHC clock, per-board identity — no
# insmod overrides, no config pushes.
set -u
ARTYSESS=${ARTYSESS:-arty_console}
AXSESS=${AXSESS:-milan_qspi_boot}

# sentinel console exec: run CMD on a tmux console, wait for the marker, print output
conx() { # conx <session> <cmd> [timeout_s]
  local sess=$1 cmd=$2 tmo=${3:-15} m="M$RANDOM$RANDOM" n=0
  tmux send-keys -t "$sess" "echo S-$m; $cmd; echo E-$m" Enter
  while ! tmux capture-pane -t "$sess" -p | grep -q "E-$m"; do
    n=$((n+1)); [ "$n" -gt "$tmo" ] && { echo "(timeout on $sess)"; return 1; }
    sleep 1
  done
  tmux capture-pane -t "$sess" -p -S -60 | sed -n "/S-$m/,/E-$m/p" | grep -v "^echo\|S-$m\|E-$m"
}

echo "== gPTP direct-cable, HW timestamps (AX7101=GM cc6/prio100, Arty=slave) =="
conx "$AXSESS" 'killall ptp4l 2>/dev/null; sleep 1;
  sed "s/priority1 254/priority1 100/; s/clockClass 248/clockClass 6/" /etc/gptp.cfg > /tmp/gm.cfg;
  nohup ptp4l -i eth0 -f /tmp/gm.cfg -m > /tmp/ptp4l.log 2>&1 & echo AX-GM-UP' 8
conx "$ARTYSESS" 'killall ptp4l 2>/dev/null; sleep 1;
  nohup ptp4l -i eth0 -f /etc/gptp.cfg -m > /tmp/ptp4l.log 2>&1 & echo ARTY-SLAVE-UP' 8

echo "== waiting for SLAVE + servo convergence (up to 90 s) =="
for i in $(seq 18); do
  sleep 5
  out=$(conx "$ARTYSESS" 'grep -aE "assuming.*SLAVE|rms" /tmp/ptp4l.log | tail -2; printf "txto="; grep -ac "timed out" /tmp/ptp4l.log' 10)
  if echo "$out" | grep -qE "rms +[0-9]+ +max"; then
    echo "$out" | grep -E "rms|txto"
    pdel=$(conx "$ARTYSESS" 'pmc -u -b 0 -t 1 "GET PORT_DATA_SET" 2>/dev/null | grep peerMeanPathDelay' 10)
    echo "$pdel"
    echo "GATE 1 PASS: Arty slaved, servo running (HW timestamps both ends)."
    echo "GATE 2: peerMeanPathDelay above should read ~1000-3000 ns (HW-grade);"
    echo "        ~600000 ns means a software-timestamp end — check ts caps."
    echo "GATE 3: txto= must stay 0 on both ends (Arty above; AX below):"
    conx "$AXSESS" 'printf "txto="; grep -ac "timed out" /tmp/ptp4l.log' 8
    exit 0
  fi
  echo "  ...waiting ($((i*5))s)"
done
echo "GATE FAIL: no SLAVE/rms on the Arty — checklist:"
echo "  - cable really direct (not through the switch)?"
echo "  - both consoles alive? (tmux ls: $ARTYSESS, $AXSESS)"
echo "  - AX log: run: tail /tmp/ptp4l.log on $AXSESS (expect 'assuming the grand master role')"
exit 1
