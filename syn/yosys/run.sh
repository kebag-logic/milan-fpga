#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Open-toolchain synthesis check: prove the (XPM-free) RTL maps to a *generic*,
# device-independent cell library with Yosys — i.e. it will build on non-Xilinx
# FPGAs. SystemVerilog (interfaces, packages, assignment patterns) is converted to
# Verilog-2005 by sv2v first. `hierarchy -check` fails if any vendor/undefined
# primitive remains, so a PASS means the module is fully mapped to generic logic.
#
#   ./run.sh                 # generic synth of every top below
#   YOSYS_SYNTH=synth_ecp5 ./run.sh   # target a real device (Lattice ECP5)
#
# Requires: yosys, and sv2v on PATH (see README.md).

set -u
export PATH="$HOME/.local/bin:$PATH"
R="$(cd "$(dirname "$0")/../.." && pwd)"
A="$R/third_party/verilog-axis/rtl"
C="$R/hdl/common"; Q="$R/hdl/802_1q_traffic_shaper"; P="$R/hdl/ptp_timestamp"
E="$R/hdl/eth_event_counter"; D="$R/hdl/adp"
INC="-I $R/hdl/common -I $Q -I $E -I $D -I $P"
SYNTH="${YOSYS_SYNTH:-synth}"           # generic 'synth' = device-independent
TMP="$(mktemp -d)"

for t in sv2v yosys; do command -v $t >/dev/null || { echo "missing tool: $t (see syn/yosys/README.md)"; exit 2; }; done

# top | source files (interface modules go through their flat wrapper)
tops=(
  "tcam|$C/tcam.sv"
  "cdc_pulse|$C/cdc_pulse.sv"
  "cdc_handshake|$C/cdc_handshake.sv"
  "adp_tx_arbiter|$D/adp_tx_arbiter.sv"
  "adp_advertiser|$D/adp_pkg.sv $D/adp_advertiser.sv"
  "rx_mac_filter|$C/tcam.sv $C/rx_mac_filter.sv"
  "milan_csr|$R/hdl/csr/milan_csr.sv"
  "credit_based_shaper|$C/ethernet_packet_pkg.sv $Q/credit_based_shaper.sv"
  "timestamp_counter|$P/timestamp_counter.sv"
  "ptp_csr_sync|$P/ptp_csr_sync.sv"
  "event_counter|$E/event_counter.sv"
  "ethernet_events|$E/ethernet_events.sv $E/event_counter.sv"
  "classifier_wrap|$C/ethernet_packet_pkg.sv $C/axi_stream_if.sv $Q/traffic_class_map.sv $Q/traffic_classifier.sv $A/axis_fifo.v $R/tb/verilator/classifier/classifier_wrap.sv"
  "queues_wrap|$C/axi_stream_if.sv $Q/traffic_queues.sv $A/axis_fifo.v $A/axis_demux.v $A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v $R/tb/verilator/queues/queues_wrap.sv"
  "axis_fifo|$A/axis_fifo.v"
  "axis_demux|$A/axis_demux.v"
  "axis_arb_mux|$A/axis_arb_mux.v $A/arbiter.v $A/priority_encoder.v"
)

echo "== Yosys open-synthesis check ($SYNTH, via sv2v) =="
pass=0; fail=0
for spec in "${tops[@]}"; do
  top="${spec%%|*}"; srcs="${spec#*|}"
  if ! sv2v --top="$top" $INC $srcs > "$TMP/$top.v" 2> "$TMP/$top.sv2v.err"; then
    printf "  [FAIL] %-22s sv2v: %s\n" "$top" "$(head -1 "$TMP/$top.sv2v.err")"; fail=$((fail+1)); continue
  fi
  yosys -p "read_verilog $TMP/$top.v; $SYNTH -top $top; hierarchy -check; stat" > "$TMP/$top.yos.log" 2>&1
  rc=$?
  cells="$(grep -E '^[[:space:]]+[0-9]+ cells$' "$TMP/$top.yos.log" | head -1 | grep -oE '[0-9]+')"
  if [ $rc -eq 0 ]; then printf "  [PASS] %-22s cells=%s\n" "$top" "${cells:-?}"; pass=$((pass+1))
  else printf "  [FAIL] %-22s yosys: %s\n" "$top" "$(grep -iE '^ERROR' "$TMP/$top.yos.log" | head -1)"; fail=$((fail+1)); fi
done
echo "--------------------------------------------------------------"
echo "tops: $((pass+fail))   pass: $pass   fail: $fail"
echo "RESULT: $([ $fail -eq 0 ] && echo PASS || echo FAIL)"
rm -rf "$TMP"
[ $fail -eq 0 ]
