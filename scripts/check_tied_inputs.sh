#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Tied-off-input inventory for the milan_datapath SoC boundary — the
# "RMON lesson" made permanent: a port-level TB proved the eth_event_counter
# bus while the SoC instantiation had it constant-tied, so the silicon
# feature was dead and every TB still passed. This check makes that class
# VISIBLE forever: it lists every `milan_datapath` INPUT port that the LiteX
# instantiation (sw/litex/milan_soc.py, add_milan_datapath ports dict) ties
# to a constant, and flags the ones no other wiring site ever overrides.
#
# NON-FATAL by design (exit 0 unless the inputs it needs are missing): the
# default stub wiring is legitimate (CSR-only elaboration), the DMA/MAC
# attach overrides part of it via extra_ports. The value is the INVENTORY —
# a reviewer adding a TB for behavior behind one of these ports must find it
# here and check the real build's extra_ports before trusting a green TB.
#
#   scripts/check_tied_inputs.sh            # report to stdout
#
# Wired into syn/yosys/run.sh as a trailing non-fatal report.

set -u
R="$(cd "$(dirname "$0")/.." && pwd)"
RTL="$R/hdl/milan/milan_datapath.sv"
SOC="$R/sw/litex/milan_soc.py"

[ -r "$RTL" ] || { echo "check_tied_inputs: missing $RTL"; exit 2; }
[ -r "$SOC" ] || { echo "check_tied_inputs: missing $SOC"; exit 2; }

echo "== milan_datapath tied-off input inventory (non-fatal) =="

# 1) input ports of the RTL wrapper (flat ANSI header, `input wire ...`)
rtl_inputs="$(sed -n '/^module milan_datapath/,/^);/p' "$RTL" \
  | grep -E '^\s*input\s' \
  | sed -E 's/.*(wire|logic)\s*(\[[^]]*\]\s*)?//; s/[,)].*$//; s/\s+$//; s/^\s+//' \
  | grep -E '^[A-Za-z_][A-Za-z0-9_]*$')"

# 2) constant-tied i_* entries in the add_milan_datapath ports dict.
#    A tie is `i_NAME = <literal>` where the literal is an integer
#    (0, 1, 0b10, 0x..). Signal wirings (`csr_axil...`, `ClockSignal...`)
#    are not ties. migen doubles an existing i_/o_ prefix (RTL `i_link_up`
#    -> Instance kw `i_i_link_up`), so strip exactly ONE leading `i_`.
tied="$(sed -n '/^    ports = dict($/,/^    )$/p' "$SOC" \
  | grep -oE 'i_[A-Za-z0-9_]+\s*=\s*(0b[01]+|0x[0-9a-fA-F]+|[0-9]+)\b' \
  | sed -E 's/\s*=\s*/=/')"

[ -n "$tied" ] || { echo "  no constant-tied i_* entries found (dict parse failed?)"; exit 2; }

SIM="$R/sw/litex/milan_sim.py"

# ---- allowlist: ties that are INTENTIONAL by design, with the reason.
# An allowlisted never-overridden tie prints [allowed] instead of [WARNING]
# so the report stays clean of KNOWN-inert boundaries — remove the entry the
# moment a real engine is supposed to drive the port (then a green TB with
# the tie still in place becomes the RMON class again).
# P11 (NxN CSR window, NXN_ARCHITECTURE.md §1.5): the 0x800 window's
# LCTX/TCTX/ACMP-tbl engine boundary is tied inert until the lane-K shared
# context engines land; snap_ok=1 completes A_STRM_SNAP immediately and
# rd_data/tbl_*=0 makes the engine-backed window words read 0 (the CSR-side
# FSMs are TB-proven against modeled/live engines in tb/verilator/csr).
allow_reason() {
  case "$1" in
    i_i_lctx_rd_data|i_i_lctx_snap_ok|i_i_tctx_rd_data|i_i_tctx_snap_ok|\
    i_i_acmp_tbl_gnt|i_i_acmp_tbl_ctx)
      echo "P11 0x800 window: lane-K context engine pending" ;;
    *) echo "" ;;
  esac
}

n_tied=0; n_dead=0
while IFS='=' read -r kw val; do
  port="${kw#i_}"                      # Instance kw -> RTL port name
  # confirm the port really exists on the RTL boundary (catch renames)
  if ! printf '%s\n' "$rtl_inputs" | grep -qx "$port"; then
    echo "  [STALE]   $kw: no such input '$port' on milan_datapath — dict/RTL drifted"
    continue
  fi
  n_tied=$((n_tied+1))
  # every binding of this Instance kw across the wiring sites (the ports
  # dict stub + every extra_ports/dp_ports attach in soc/sim). A binding
  # whose value is a bare integer literal is a tie; anything else (a
  # Signal/endpoint/expression) means some build actually drives the port.
  driven=0
  while read -r bind; do
    v="${bind#*=}"; v="$(echo "$v" | sed -E 's/^\s+|\s+$//g')"
    case "$v" in
      0b[01]*|0x[0-9a-fA-F]*|[0-9]*) : ;;   # integer literal = tie
      *) driven=1 ;;
    esac
  done < <(grep -hoE "\b${kw}\s*=\s*[^,)]+" "$SOC" "$SIM" 2>/dev/null)
  if [ "$driven" -eq 1 ]; then
    echo "  [tied]    ${kw}=${val}  (stub default; a real attach site drives it)"
  else
    reason="$(allow_reason "$kw")"
    if [ -n "$reason" ]; then
      echo "  [allowed] ${kw}=${val}  intentional: $reason"
    else
      n_dead=$((n_dead+1))
      echo "  [WARNING] ${kw}=${val}  constant at EVERY wiring site — the cone"
      echo "            behind '$port' is dead in silicon no matter what a TB says"
      echo "            (the RMON class: tie was why RMON never counted on boards)"
    fi
  fi
done <<< "$tied"

echo "--------------------------------------------------------------"
echo "tied inputs: $n_tied   never-overridden: $n_dead"
echo "TIED-INPUT REPORT: done (informational — see WARNING lines above)"
exit 0
