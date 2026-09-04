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
# THIS IS A GATE (2026-07-26), not a report. It used to exit 0 always and
# print three WARNINGs on every run — the three TDM inputs, which are
# EXPECTED (no board has a TDM header, so there are no pins to wire). A
# checker whose warnings are mostly expected is a checker nobody reads, and
# the one genuine defect in the list (`i_mac_events`, dead RMON on both
# boards) sat there unnoticed among them. So:
#
#   * a never-overridden tie WITH a justified-tie entry prints [expected]
#     together with its reason and where that reason is recorded;
#   * a never-overridden tie WITHOUT one prints [WARNING] and FAILS the run.
#
# Adding a new unjustified tie therefore breaks the build; keeping one costs
# exactly one allowlist line naming the reason and its record. Exit codes:
#   0 = clean · 1 = unjustified never-overridden tie(s) · 2 = inputs missing.
#
#   scripts/check_tied_inputs.sh            # report + gate
#   SOC=<file> scripts/check_tied_inputs.sh # gate an alternative wiring file
#                                           # (used to prove the gate bites)
#
# Wired into syn/yosys/run.sh as a trailing FATAL gate.
#
# STRICT MODE (Rule 13). Two extractions below are allowed to come back empty
# and say so with `|| true`, because "this pattern matched nothing" is a
# VERDICT this gate prints (dict parse failed → exit 2), not a crash to
# propagate — and under `pipefail` a grep that matches nothing is the status
# of the whole pipeline. Every other non-zero here is already read by an `if`
# or an `||`. The `| grep -q` / `| awk` searches over the two in-memory lists
# are herestrings rather than pipes for the same reason: with `pipefail` the
# early exit of a `-q` reader can make the WRITER's status the pipeline's, and
# a gate must not learn "STALE" from a signal.

set -euo pipefail
R="$(cd "$(dirname "$0")/.." && pwd)"
RTL="$R/hdl/milan/milan_datapath.sv"
SOC="${SOC:-$R/sw/litex/milan_soc.py}"
SIM="$R/sw/litex/milan_sim.py"

# ---- JUSTIFIED-TIE ALLOWLIST ------------------------------------------------
# One line per intentionally never-overridden tie:
#
#   <Instance kw>|<why this tie is correct>|<where that reason is recorded>
#
# The third field is the point: a reason with no record is an opinion, and the
# next reader cannot check it. An entry here turns [WARNING] into [expected]
# and keeps the run green; DELETE the entry the moment something is supposed
# to drive the port, and the gate goes red until it does.
#
# Rules for adding one:
#   * the tie must be structural (no pins / no engine exists), not "not done
#     yet" — a TODO belongs in the roadmap, where it is visible, not here
#     where it is silenced;
#   * the record must be a real file (and ideally a line) a reviewer can open.
#
# (P12 note: the P11 0x800-window engine-boundary entries are GONE - the
# LCTX/TCTX/ACMP-tbl ports moved inside milan_datapath, wired to live
# engines. That is what retiring an entry looks like.)
ALLOWLIST="\
i_tdm_bclk_i|no TDM header exists on either board, so there are no pins to wire; a platform extension drives it via extra_ports when one lands|sw/litex/milan_soc.py, the 'TDM bus (item-4 front-end family)' comment in the add_milan_datapath ports dict
i_tdm_fsync_i|no TDM header exists on either board, so there are no pins to wire; a platform extension drives it via extra_ports when one lands|sw/litex/milan_soc.py, the 'TDM bus (item-4 front-end family)' comment in the add_milan_datapath ports dict
i_tdm_data_i|no TDM header exists on either board, so there are no pins to wire; a platform extension drives it via extra_ports when one lands|sw/litex/milan_soc.py, the 'TDM bus (item-4 front-end family)' comment in the add_milan_datapath ports dict"

#! the two files this gate reads, or exit 2 naming the missing one
require_inputs() {
  [ -r "$RTL" ] || { echo "check_tied_inputs: missing $RTL"; exit 2; }
  [ -r "$SOC" ] || { echo "check_tied_inputs: missing $SOC"; exit 2; }
}

#! input ports of the RTL wrapper (flat ANSI header, `input wire ...`)
read_rtl_inputs() {
  rtl_inputs="$(sed -n '/^module milan_datapath/,/^);/p' "$RTL" \
    | grep -E '^\s*input\s' \
    | sed -E 's/.*(wire|logic)\s*(\[[^]]*\]\s*)?//; s/[,)].*$//; s/\s+$//; s/^\s+//' \
    | grep -E '^[A-Za-z_][A-Za-z0-9_]*$')" || true
}

#! constant-tied i_* entries in the add_milan_datapath ports dict.
#  A tie is `i_NAME = <literal>` where the literal is an integer
#  (0, 1, 0b10, 0x..). Signal wirings (`csr_axil...`, `ClockSignal...`)
#  are not ties. migen doubles an existing i_/o_ prefix (RTL `i_link_up`
#  -> Instance kw `i_i_link_up`), so strip exactly ONE leading `i_`.
read_tied_entries() {
  tied="$(sed -n '/^    ports = dict($/,/^    )$/p' "$SOC" \
    | grep -oE 'i_[A-Za-z0-9_]+\s*=\s*(0b[01]+|0x[0-9a-fA-F]+|[0-9]+)\b' \
    | sed -E 's/\s*=\s*/=/')" || true
  [ -n "$tied" ] || { echo "  no constant-tied i_* entries found (dict parse failed?)"; exit 2; }
}

#! reason text for an allowlisted tie, or empty when it is not allowlisted
allow_reason() {
  awk -F'|' -v k="$1" '$1 == k { print $2; exit }' <<< "$ALLOWLIST"
}
#! where that reason is recorded (the auditable half of the entry)
allow_record() {
  awk -F'|' -v k="$1" '$1 == k { print $3; exit }' <<< "$ALLOWLIST"
}

#! is every wiring site of this Instance kw a constant? sets `driven` and
#  `constexpr`: driven=1 when some build really drives the port, constexpr
#  non-empty when every site is a build-time constant EXPRESSION.
classify_bindings() {
  local kw="$1" bind v t
  driven=0; constexpr=""
  # every binding of this Instance kw across the wiring sites (the ports
  # dict stub + every extra_ports/dp_ports attach in soc/sim). A binding
  # whose value is a bare integer literal is a tie; anything else (a
  # Signal/endpoint/expression) means some build actually drives the port.
  while read -r bind; do
    v="${bind#*=}"; v="$(echo "$v" | sed -E 's/^\s+|\s+$//g')"
    # A BUILD-TIME CONSTANT EXPRESSION is still a tie. `i_i_mac_speed =
    # (0b01 if phy_model == "mii" else 0b10)` looked "driven" to the old test
    # (it is not a bare literal) while being just as constant in silicon as
    # `= 1` - a per-board guess that MAC_STATUS reported as the negotiated
    # speed. Strip an outer paren and match "<literal> [if ... else <literal>]".
    t="$(echo "$v" | sed -E 's/^\(//; s/\)$//')"
    case "$v" in
      0b[01]*|0x[0-9a-fA-F]*|[0-9]*) : ;;   # integer literal = tie
      *)
        if grep -qE '^(0b[01]+|0x[0-9a-fA-F]+|[0-9]+)( +if +.+ +else +(0b[01]+|0x[0-9a-fA-F]+|[0-9]+))?$' <<< "$t"; then
          constexpr="$t"                     # constant ternary = tie
        else
          driven=1
        fi ;;
    esac
  done < <(grep -hoE "\b${kw}\s*=\s*[^,)]+\)?" "$SOC" "$SIM" 2>/dev/null)
}

#! one line per tied entry: [tied] / [expected] / [WARNING] / [STALE]
report_ties() {
  local kw val port reason
  while IFS='=' read -r kw val; do
    port="${kw#i_}"                      # Instance kw -> RTL port name
    # confirm the port really exists on the RTL boundary (catch renames)
    if ! grep -qx "$port" <<< "$rtl_inputs"; then
      echo "  [STALE]   $kw: no such input '$port' on milan_datapath — dict/RTL drifted"
      n_stale=$((n_stale+1))
      continue
    fi
    n_tied=$((n_tied+1))
    classify_bindings "$kw"
    if [ "$driven" -eq 1 ]; then
      echo "  [tied]    ${kw}=${val}  (stub default; a real attach site drives it)"
    elif [ -n "$constexpr" ]; then
      n_dead=$((n_dead+1))
      echo "  [WARNING] ${kw}: every wiring site is a BUILD-TIME CONSTANT"
      echo "            (\`${constexpr}\`) - a python-level select, constant in"
      echo "            silicon. Same class as a bare tie: the CSR reports a"
      echo "            build-time guess, not what the hardware negotiated."
    else
      reason="$(allow_reason "$kw")"
      if [ -n "$reason" ]; then
        n_ok=$((n_ok+1))
        echo "  [expected] ${kw}=${val}"
        echo "            why:       $reason"
        echo "            recorded:  $(allow_record "$kw")"
      else
        n_dead=$((n_dead+1))
        echo "  [WARNING] ${kw}=${val}  constant at EVERY wiring site — the cone"
        echo "            behind '$port' is dead in silicon no matter what a TB says"
        echo "            (the RMON class: tie was why RMON never counted on boards)"
      fi
    fi
  done <<< "$tied"
}

#! an allowlist line whose port no longer exists (renamed / removed) is itself
#  rot: it would silently stop covering anything. Fail on it like a stale tie.
report_stale_allowlist() {
  local kw _reason _rec port
  while IFS='|' read -r kw _reason _rec; do
    [ -n "$kw" ] || continue
    port="${kw#i_}"
    grep -qx "$port" <<< "$rtl_inputs" || {
      echo "  [STALE]   allowlist entry '$kw' names no milan_datapath input"
      n_stale=$((n_stale+1))
    }
  done <<< "$ALLOWLIST"
}

#! the verdict line, and the gate's exit status
summarise() {
  echo "--------------------------------------------------------------"
  echo "tied inputs: $n_tied   justified: $n_ok   UNJUSTIFIED: $n_dead   stale: $n_stale"
  if [ "$n_dead" -gt 0 ] || [ "$n_stale" -gt 0 ]; then
    echo "TIED-INPUT GATE: FAIL — $n_dead unjustified never-overridden tie(s), $n_stale stale entr(y/ies)."
    echo "  Either drive the port from a real wiring site, or add a justified-tie"
    echo "  line (kw|reason|where the reason is recorded) to ALLOWLIST in $0."
    exit 1
  fi
  echo "TIED-INPUT GATE: PASS ($n_ok justified tie(s), no unjustified ones)"
  exit 0
}

main() {
  require_inputs
  echo "== milan_datapath tied-off input inventory (gate) =="
  read_rtl_inputs
  read_tied_entries
  n_tied=0; n_dead=0; n_ok=0; n_stale=0
  report_ties
  report_stale_allowlist
  summarise
}

main "$@"
