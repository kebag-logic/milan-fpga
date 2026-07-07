#!/bin/sh
# Phase-0 on-silicon measurement — TX_READER_PREFETCH_PLAN.md Appendix A.5.
# Runs ON THE BOARD (busybox sh + devmem + iperf3) against the peer, on the
# build_dp100_p0 gateware. Measures, by hardware counter (never assume, always measure):
#   * L  — RingDMAReader AR->first-R round-trip latency (mean, payload-only + all)
#   * the 7-way starve breakdown: prefetchable (pre_wait+rd_wait) vs structural
#     double-read (pre_busy) vs CPU/ring-empty (idle) — the number that decides
#     whether prefetch ALONE can reach 200
#   * the write-outstanding depth proxy (RX phase) — can the interconnect pipeline reads?
#
# Peer must be running `iperf3 -s` (default 192.168.127.2). Sys clock = 100 MHz => 10 ns/cyc.
# Usage: sh phase0_measure.sh [PEER_IP] [DURATION_s]
set -e
PEER="${1:-192.168.127.2}"
DUR="${2:-12}"
NSCYC=10                                   # ns per sys cycle @100 MHz

# --- CSR addresses (from build_dp100_p0 csr.csv; MSW-first for the 2-word accumulators) ---
RESET=0xf0004000; CAPTURE=0xf0004004; HASHSEL=0xf0003080
LAT_ACC_HI=0xf0004088; LAT_ACC_LO=0xf000408c
LAT_N=0xf0004090;      LAT_MAX=0xf0004094
LAT_PACC_HI=0xf0004098; LAT_PACC_LO=0xf000409c
LAT_PN=0xf00040a0
BUSY=0xf00040a4; STALL=0xf00040a8; PRE_WAIT=0xf00040ac; PRE_BUSY=0xf00040b0
RD_WAIT=0xf00040b4; IDLE=0xf00040b8; SETUP=0xf00040bc; CYC=0xf00040c0
RXW_HI=0xf00040c4; RX1W_HI=0xf00040c8

rd()   { devmem "$1"; }                     # -> 0xXXXXXXXX
rd64() { hi=$(devmem "$1"); lo=$(devmem "$2"); echo $(( (hi << 32) | lo )); }
pct()  { [ "$2" -gt 0 ] && echo $(( $1 * 1000 / $2 )) || echo 0; }   # per-mille (x10 = %)
reset_ctrs()  { devmem "$RESET" 32 1; devmem "$RESET" 32 0; }
# `capture` latches on the RISING edge (MilanDebug self.capture.re), so pulse 0->1
# every time — otherwise a 2nd capture (Phase B, or a re-run) sees no edge and reads
# the PREVIOUS snapshot. reset does not clear capture.storage.
capture()     { devmem "$CAPTURE" 32 0; devmem "$CAPTURE" 32 1; }

echo "@@@ Phase-0 measurement — peer=$PEER dur=${DUR}s (sys=100MHz, 10ns/cyc)"
echo "@@@ hash_sel=1 (single-queue TCP safety) before any TCP"
devmem "$HASHSEL" 32 1

# ================= Phase A — TX flow: L + starve breakdown =========================
echo "@@@ --- Phase A: TX (board->peer, zerocopy/TSO) ---"
iperf3 -c "$PEER" -Z -t "$DUR" >/tmp/p0_txA.txt 2>&1 &
IPF=$!
sleep 2                                     # let TCP ramp to steady state
reset_ctrs                                  # measure a clean steady-state window
sleep $(( DUR - 4 ))
capture                                     # coherent snapshot of every counter
wait $IPF 2>/dev/null || true
RATE_A=$(grep -iE "sender|receiver" /tmp/p0_txA.txt | grep -iE "bits/sec" | tail -2 | head -1)

acc=$(rd64 $LAT_ACC_HI $LAT_ACC_LO);  n=$(( $(rd $LAT_N) ))
pacc=$(rd64 $LAT_PACC_HI $LAT_PACC_LO); pn=$(( $(rd $LAT_PN) )); mx=$(( $(rd $LAT_MAX) ))
busy=$(( $(rd $BUSY) )); stall=$(( $(rd $STALL) ))
pw=$(( $(rd $PRE_WAIT) )); pb=$(( $(rd $PRE_BUSY) )); rw=$(( $(rd $RD_WAIT) ))
idle=$(( $(rd $IDLE) )); setup=$(( $(rd $SETUP) )); cyc=$(( $(rd $CYC) ))

echo "@@@ TX rate: $RATE_A"
echo "@@@ --- latency L (AR -> first R) ---"
[ "$n"  -gt 0 ] && echo "@@@ L_all  = $(( acc / n ))  cyc = $(( acc / n * NSCYC )) ns   (n=$n reads)"
[ "$pn" -gt 0 ] && echo "@@@ L_pay  = $(( pacc / pn )) cyc = $(( pacc / pn * NSCYC )) ns  (payload bursts, pn=$pn)  <-- model input"
echo "@@@ L_max  = $mx cyc = $(( mx * NSCYC )) ns (worst-case; TLB-walk spikes)"

sum=$(( busy + stall + pw + pb + rw + idle + setup ))
echo "@@@ --- starve breakdown (per-mille of cyc; x10 = %) ---   cyc=$cyc"
echo "@@@   busy      = $(pct $busy $cyc)   (producing)"
echo "@@@   stall     = $(pct $stall $cyc)   (datapath back-pressure)"
echo "@@@   pre_wait  = $(pct $pw $cyc)   PREFETCHABLE (pre-pass read-blocked)"
echo "@@@   rd_wait   = $(pct $rw $cyc)   PREFETCHABLE (real-pass read-blocked)"
echo "@@@   pre_busy  = $(pct $pb $cyc)   STRUCTURAL   (pre-pass summing beats / double-read)"
echo "@@@   idle      = $(pct $idle $cyc)   CPU/ring-empty (not the reader)"
echo "@@@   setup     = $(pct $setup $cyc)   (AR/PREP/header)"
echo "@@@   PREFETCHABLE total (pre_wait+rd_wait) = $(pct $(( pw + rw )) $cyc)"
echo "@@@   BALANCE: sum=$sum cyc=$cyc  $( [ "$sum" = "$cyc" ] && echo OK || echo "MISMATCH(diff $(( cyc - sum )))" )"

# cross-check against the datapath-input probe over the SAME idea (separate capture)
echo "@@@   (cross-check) txdp_in busy/stall/starve @0xf0004060.. below"
di_b=$(( $(rd 0xf0004060) )); di_s=$(( $(rd 0xf0004064) )); di_v=$(( $(rd 0xf0004068) )); di_c=$(( $(rd 0xf000406c) ))
echo "@@@   txdp_in: busy=$(pct $di_b $di_c) stall=$(pct $di_s $di_c) starve=$(pct $di_v $di_c) (per-mille; free-running)"

# ================= Phase B — RX flow: outstanding-depth proxy ======================
echo "@@@ --- Phase B: RX reverse (peer->board) for write-outstanding depth proxy ---"
iperf3 -c "$PEER" -Z -R -t "$DUR" >/tmp/p0_rxB.txt 2>&1 &
IPF=$!
sleep 2; reset_ctrs; sleep $(( DUR - 4 )); capture
wait $IPF 2>/dev/null || true
RATE_B=$(grep -iE "receiver" /tmp/p0_rxB.txt | grep -iE "bits/sec" | tail -1)
rxo=$(( $(rd $RXW_HI) )); rx1o=$(( $(rd $RX1W_HI) ))
echo "@@@ RX rate: $RATE_B"
echo "@@@ writer outstanding high-water: rxw=$rxo  rx1w=$rx1o   (>=4 => read prefetch depth likely available; <=2 => interconnect serializing => DEFER prefetch)"

echo "@@@ --- DECISION (plan A.6) ---"
echo "@@@   D_full = ceil((L_pay+64)/64) bursts to fully hide L; pick D=min(D_full, rxw_hi)."
echo "@@@   pre_wait+rd_wait dominate -> prefetch IS the lever (build it)."
echo "@@@   pre_busy large            -> single-pass csum FIRST (prefetch alone won't reach 200)."
echo "@@@   idle dominates            -> re-attribute to CPU/driver, not the reader."
echo "@@@ done."
