#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Observer-purity structural gate (stream-observer regression class, 2026-07-25):
# tap/telemetry modules must drive ONLY their own CSR/counter outputs and
# NEVER drive the observed streams' tvalid/tready/tdata/tkeep/tlast/tuser
# nets. An "observer" that participates in a stream handshake is a datapath
# actor wearing telemetry clothing - the wiring-mistake class that can kill a
# data path while every green TB watches the counters instead of the stream.
#
# Two disciplined text-level checks over the SOURCE (same parse style as
# scripts/check_tied_inputs.sh - the house pattern):
#   1. module level (PURE observers: hdl/**/*_taps.sv, the *_tap_bank.sv
#      observation-point adapters that wrap them, + the AVTP RX
#      monitors): no OUTPUT port may carry a stream-handshake name
#      (tvalid/tready/tdata/tkeep/tlast/tuser);
#   2. site level (pure observers + every raw-stream tap reader wired in
#      hdl/milan/milan_datapath.sv - parser/MAAP/protocol processor): every
#      instantiation port binding one of the datapath's observed stream nets
#      (rx_axis_*/tx_axis_* members, [sm]_axis_* boundary
#      lanes) must be an INPUT of that module - reads only, never drives.
#      The bindings-checked count is printed so a vacuous pass is visible.
#   3. the same two rules at the MAC site (#360): the gPTP launch observer
#      watches the MAC's own transmit stream, one register stage before the
#      GMII pads, so its wiring file is sw/litex/milan_soc.py and its
#      observed nets are that PHY endpoint's members rather than AXIS ones.
#      Its Migen bindings are read with the direction the instantiator
#      claims AND the direction its SV header declares, and a drive needs
#      only one of the two to say so. Its own bindings-checked count is
#      printed for the same anti-vacuity reason.
#
# A negative SELF-TEST runs first on a deliberately-broken fixture; if the
# checker fails to flag it, the checker itself is declared broken (exit 3).
#
#   syn/yosys/check_tap_purity.sh   # exit 0 clean / 1 violation / 3 self-test broken
#
# Wired into syn/yosys/run.sh as a trailing report next to the tied-input
# inventory; standalone use is the exit-coded gate.

# The full trio is safe here, and the three places where a non-zero status is
# EXPECTED are spelled out rather than left to errexit: `run_checks` returns a
# violation COUNT (taken with `|| rc=$?` at both call sites and at the
# self-test), the port parse may legitimately come back empty (taken with
# `|| dirs=""`, so the "header drifted?" diagnostic still prints), and the
# report's `grep -v` finds nothing when there are no violations (`|| true`).
# Everything else that fails here - find, mktemp, the fixture heredocs - is a
# broken checker, and a broken checker must not print a purity verdict.
set -euo pipefail
R="$(cd "$(dirname "$0")/../.." && pwd)"
DP="$R/hdl/milan/milan_datapath.sv"
# The second wiring file. Not every observer hangs off the datapath: the gPTP
# launch observer watches the MAC's OWN transmit stream, so its site is the
# LiteX MAC wrapper and its instantiation is a Migen `Instance(...)`, not an
# SV instantiation (#360). A gate that only ever parsed milan_datapath.sv
# would report PASS on that observer while never having read its site.
SOC="$R/sw/litex/milan_soc.py"

# PURE observers: telemetry-only modules - both checks apply. The *_tap_bank.sv
# glob is load-bearing: the LTAP adapter Rule 1 cut out of milan_datapath is
# the module whose port list binds the observed MAC/AAF stream nets, and a
# find over *_taps.sv alone never read it (24 bindings checked either way).
PURE_FILES=()
while IFS= read -r f; do PURE_FILES+=("$f"); done \
    < <(find "$R/hdl" \( -name "*_taps.sv" -o -name "*_tap_bank.sv" \) | sort)
PURE_FILES+=("$R/hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv"
             "$R/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv")

# Raw-stream tap READERS (monitor-tap + low-rate-TX engines): they own their
# own TX lanes, so only the site-level input-only rule applies to the
# OBSERVED stream nets they tap.
READER_FILES=(
    "$R/hdl/ieee1722/avtp/avtp_stream_parser.sv"
    "$R/hdl/ieee1722/maap/KL_maap.sv"
    # THE CONTROL PLANE IS ONE READER NOW. The four 1722.1/SRP tops that used
    # to be listed here (KL_aecp_top, KL_acmp_responder, KL_acmp_listener,
    # KL_lwsrp_top) are deleted; the protocol processor replaced them, and
    # KL_pp_shadow is exactly what this gate exists to police - it hangs off
    # rx_axis as a monitor tap and owns its own TX lane, so it must never
    # appear on the drive side of an observed stream net.
    "$R/hdl/milan/KL_pp_shadow.sv"
    # The gPTP plane's fabric observer (#114): the shadow taps rx_axis_fabric
    # and owns its own TX lane. Listing it is what makes GPTP_PLANE.md's
    # "check_tap_purity holds" claim NON-vacuous.
    #
    # KL_gptp_txstamp.sv USED TO BE LISTED HERE and was deleted with the
    # module (#360). It watched tx_axis_to_mac, which is the datapath's MAC
    # boundary - upstream of the queueing this issue is about - so the
    # observation moved to the MAC's own transmit stream. Its replacement,
    # KL_gptp_gmii_launch, does not appear on this list because its site is
    # not milan_datapath.sv; it is covered by LITEX_PURE_FILES below. A
    # retired path left here is not a harmless leftover: run_checks reports a
    # missing tap source as a violation, which is how this entry was found.
    "$R/hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv"
)

# PURE observers wired in the LiteX MAC rather than in milan_datapath.sv.
# Both checks apply, against $SOC as the wiring file: the module-level rule
# reads the SV header exactly as above, and the site-level rule reads the
# Migen binding prefixes, which carry the direction the same way `.port(net)`
# plus the header does.
LITEX_PURE_FILES=(
    # #360's launch observer. It declares itself a PURE OBSERVER over
    # `phy.sink`, the source feeding the PHY's transmit register stage, and
    # this is where that claim is held: it may read those octets and must
    # never appear on their drive side.
    "$R/hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv"
)

STREAM_TERM='t(valid|ready|data|keep|last|user)'
# nets a tap may READ but never DRIVE (datapath interface members + flat
# boundary lanes of milan_datapath)
STREAM_NET_RE='((rx_axis_from_mac|rx_axis_fabric|tx_axis_to_mac)\.t(valid|ready|data|keep|last|user)|[sm]_axis_[a-z_]*t(valid|ready|data|keep|last|user))'
# The MAC-side equivalent: the PHY-facing stream endpoints of the LiteEth PHY
# the launch observer watches. Migen names them as attribute paths, so the
# member set is the LiteEth endpoint's (valid/ready/data/last/first/error),
# not the AXIS spelling.
GMII_NET_RE='phy\.(sink|source)\.(valid|ready|data|last|first|error)'

n_bind=0    # stream-net bindings actually resolved (anti-vacuity witness)
n_rx_fabric=0 # bindings on the live post-filter fabric-observer seam
n_gmii=0    # bindings resolved on the MAC's own transmit stream (#360)

# ---- helpers ---------------------------------------------------------------
# port_dirs FILE -> lines "dir name" for every ANSI header port in the file
port_dirs() {
    sed -e 's://.*$::' "$1" | awk '
        /^[[:space:]]*module[[:space:]]/ { inhdr = 1 }
        inhdr {
            line = $0
            if (match(line, /(input|output|inout)/)) {
                dir = substr(line, RSTART, RLENGTH)
                rest = substr(line, RSTART + RLENGTH)
                gsub(/\[[^]]*\]/, " ", rest)      # strip widths
                gsub(/wire|logic|reg|signed|int|unsigned/, " ", rest)
                n = split(rest, tok, /[ \t,()]+/)
                name = ""
                for (i = 1; i <= n; i++) if (tok[i] ~ /^[A-Za-z_][A-Za-z0-9_]*$/) name = tok[i]
                if (name != "") print dir, name
            }
            if (line ~ /\);/) inhdr = 0
        }'
}

module_names() {
    grep -oE '^[[:space:]]*module[[:space:]]+[A-Za-z_][A-Za-z0-9_]*' "$1" \
        | awk '{print $2}'
}

# inst_bindings WIRING_FILE MODULE -> lines "port|expr" for each .port(expr)
# of every instantiation of MODULE (comments stripped, one nesting level ok)
inst_bindings() {
    sed -e 's://.*$::' "$1" | awk -v mod="$2" '
        BEGIN { on = 0 }
        {
            if (!on && match($0, "(^|[^A-Za-z0-9_])" mod "([^A-Za-z0-9_]|$)")) on = 1
            if (on) {
                buf = buf " " $0
                if ($0 ~ /\);/) { print buf; buf = ""; on = 0 }
            }
        }' | grep -oE '\.[A-Za-z_][A-Za-z0-9_]*[[:space:]]*\(([^()]|\([^()]*\))*\)' \
           | sed -E 's/^\.([A-Za-z_][A-Za-z0-9_]*)[[:space:]]*\((.*)\)$/\1|\2/'
}

# migen_bindings WIRING_FILE MODULE -> lines "port|expr" for each i_/o_ keyword
# argument of every `Instance("MODULE", ...)` in a Migen wiring file.
#
# THE PREFIX IS NOT THE ANSWER, only a second opinion. Migen's `i_`/`o_` says
# which way the instantiator believes the port goes; the module header says
# which way it actually goes, and a drive needs BOTH to agree. So the prefix
# is stripped here and the port name handed on exactly as the SV parser hands
# its own on - the direction verdict below comes from port_dirs either way -
# and a prefix that DISAGREES with the header is reported separately, because
# `o_gmii_tvalid_i = phy.sink.valid` is a drive whatever the header says.
migen_bindings() {
    sed -e 's:#.*$::' "$1" | awk -v mod="$2" '
        BEGIN { on = 0; depth = 0 }
        {
            if (!on && match($0, "Instance\\([ \t]*\"" mod "\"")) { on = 1 }
            if (on) {
                # the Instance call ends at the line whose running paren
                # balance returns to zero, so a nested ClockSignal() or a
                # ~ResetSignal() argument cannot close it early
                line = $0
                n = gsub(/\(/, "(", line); depth += n
                n = gsub(/\)/, ")", line); depth -= n
                print $0
                if (depth <= 0) { on = 0; depth = 0 }
            }
        }' | grep -oE '(^|[^A-Za-z0-9_])[io]_[A-Za-z_][A-Za-z0-9_]*[[:space:]]*=[^,]*' \
           | sed -E 's/^[^A-Za-z0-9_]*([io])_([A-Za-z_][A-Za-z0-9_]*)[[:space:]]*=[[:space:]]*(.*)$/\1|\2|\3/'
}

# run_checks MODE(pure|reader|litex) WIRING_FILE FILE... -> prints violations, returns count
run_checks() {
    local mode="$1" wiring="$2"; shift 2
    local viol=0 f m dirs dir name port expr m_bind site_bindings site_net_re claim
    for f in "$@"; do
        [ -r "$f" ] || { echo "  [ERROR] missing tap source $f"; viol=$((viol+1)); continue; }
        # An empty parse is a FINDING below, not a reason to stop: the awk
        # exits non-zero on a header it cannot read, and that diagnostic is
        # worth more than errexit's silence.
        dirs="$(port_dirs "$f")" || dirs=""
        [ -n "$dirs" ] || { echo "  [ERROR] no ports parsed from $f (header drifted?)"; viol=$((viol+1)); continue; }
        for m in $(module_names "$f"); do  # shellcheck disable=SC2086 - deliberate split: one word per module name declared in the file
            m_bind=0
            if [ "$mode" = "pure" ] || [ "$mode" = "litex" ]; then
                # 1) module level: no stream-handshake-named OUTPUT
                while read -r dir name; do
                    [ "$dir" = "output" ] || continue
                    if echo "$name" | grep -qE "$STREAM_TERM"; then
                        echo "  [VIOLATION] $m.$name: pure-observer OUTPUT carries a stream-handshake name"
                        viol=$((viol+1))
                    fi
                done <<< "$dirs"
            fi
            # 2) site level: observed stream nets land on INPUT ports only.
            # The two site parsers hand back the same "port|expr" shape, so
            # the verdict below is one rule with two front ends; `litex`
            # prefixes a third field, the instantiator's own claimed
            # direction.
            if [ "$mode" = "litex" ]; then
                site_bindings="$(migen_bindings "$wiring" "$m")" || site_bindings=""
                site_net_re="$GMII_NET_RE"
            else
                site_bindings="$(inst_bindings "$wiring" "$m")" || site_bindings=""
                site_net_re="$STREAM_NET_RE"
            fi
            while IFS='|' read -r port expr; do
                claim=""
                if [ "$mode" = "litex" ]; then
                    claim="$port"; port="${expr%%|*}"; expr="${expr#*|}"
                fi
                [ -n "$port" ] || continue
                echo "$expr" | grep -qE "$site_net_re" || continue
                n_bind=$((n_bind+1))
                m_bind=$((m_bind+1))
                if echo "$expr" | grep -qE 'rx_axis_fabric\.'; then
                    n_rx_fabric=$((n_rx_fabric+1))
                fi
                [ "$mode" != "litex" ] || n_gmii=$((n_gmii+1))
                if [ "$claim" = "o" ]; then
                    echo "  [VIOLATION] $m.$port: instantiated as an OUTPUT onto observed stream '$(echo "$expr" | tr -s ' ')'"
                    viol=$((viol+1))
                fi
                dir="$(echo "$dirs" | awk -v p="$port" '$2 == p { print $1; exit }')"
                if [ -z "$dir" ]; then
                    echo "  [VIOLATION] $m.$port: bound to a stream net but not on the module header (parse drift)"
                    viol=$((viol+1))
                elif [ "$dir" != "input" ]; then
                    echo "  [VIOLATION] $m.$port ($dir) drives stream net '$(echo "$expr" | tr -s ' ')'"
                    viol=$((viol+1))
                fi
            done <<< "$site_bindings"
            if [ "$mode" != "pure" ] && [ "$m_bind" -eq 0 ]; then
                echo "  [VIOLATION] $m: no observed-stream binding resolved at its $([ "$mode" = litex ] && echo MAC || echo datapath) site"
                viol=$((viol+1))
            fi
        done
    done
    return "$viol"
}


# ---- negative self-test: the checker must FAIL a deliberately-broken fixture
# NO LOCALS ANYWHERE IN THIS FILE, deliberately. $TMP and the
# n_bind/n_rx_fabric witnesses run_checks accumulates are read by the
# real-tree pass below, and a `local` in either of these two functions would
# hand it a fresh copy of a counter whose whole job is to prove the wiring
# parse was not vacuous.
selftest_checker() {
    cat > "$TMP/bad_probe_taps.sv" <<'EOF'
module bad_probe_taps (
  input  wire        clk_i,
  input  wire        rx_tvalid_i,
  output wire        rx_tready_o,
  output wire [15:0] count_o
);
endmodule
EOF
    cat > "$TMP/fixture_dp.sv" <<'EOF'
module fixture_dp;
  bad_probe_taps probe (
    .clk_i       (clk),
    .rx_tvalid_i (rx_axis_fabric.tvalid),
    .rx_tready_o (rx_axis_fabric.tready)
  );
endmodule
EOF
    # The COUNT is the answer here, so the status is taken: a non-zero
    # run_checks is what this fixture exists to produce, not a failure.
    self_n=0
    self_out="$(run_checks pure "$TMP/fixture_dp.sv" "$TMP/bad_probe_taps.sv")" \
        || self_n=$?
    if [ "$self_n" -ge 2 ]; then
        echo "  negative self-test: checker flags the broken fixture ($self_n violations) - OK"
    else
        echo "  negative self-test FAILED: broken fixture produced only $self_n finding(s):"
        echo "$self_out"
        echo "TAP-PURITY RESULT: CHECKER-BROKEN"
        exit 3
    fi

    # The SECOND front end gets its own broken fixture. The Migen site parser
    # is new code on the same rule (#360), and a site parser that silently
    # matches nothing reports PASS forever; this fixture plants both halves of
    # the mistake it exists to catch - a port turned OUTPUT in the header, and
    # an `o_` binding onto the observed stream - so a parse that goes blind
    # fails here rather than in the tree.
    cat > "$TMP/bad_launch_obs.sv" <<'EOF'
module bad_launch_obs (
  input  wire       eth_clk_i,
  output wire       gmii_tvalid_x,
  input  wire [7:0] gmii_tdata_i,
  output wire       rec_valid_o
);
endmodule
EOF
    cat > "$TMP/fixture_soc.py" <<'EOF'
self.specials += Instance("bad_launch_obs",
    i_eth_clk_i     = ClockSignal("maceth_tx"),
    o_gmii_tvalid_x = self.phy.sink.valid,
    i_gmii_tdata_i  = self.phy.sink.data,
    o_rec_valid_o   = self.gptp_txrec_valid,
)
EOF
    self_n=0
    self_out="$(run_checks litex "$TMP/fixture_soc.py" "$TMP/bad_launch_obs.sv")" \
        || self_n=$?
    # three: the stream-named OUTPUT, the `o_` claim on an observed net, and
    # the header direction behind it
    if [ "$self_n" -ge 3 ]; then
        echo "  negative self-test: checker flags the broken MAC-site fixture ($self_n violations) - OK"
    else
        echo "  negative self-test FAILED: broken MAC-site fixture produced only $self_n finding(s):"
        echo "$self_out"
        echo "TAP-PURITY RESULT: CHECKER-BROKEN"
        exit 3
    fi
}

# ---- the real tree ----------------------------------------------------------
check_tree() {
    [ -r "$DP" ] || { echo "  missing $DP"; exit 2; }
    [ -r "$SOC" ] || { echo "  missing $SOC"; exit 2; }
    # in-shell runs (redirects, no subshell) so the n_bind witness accumulates
    n_bind=0
    n_rx_fabric=0
    n_gmii=0
    viol=0
    rc=0; run_checks pure   "$DP"  "${PURE_FILES[@]}"       > "$TMP/pure.log"   || rc=$?; viol=$((viol+rc))
    rc=0; run_checks reader "$DP"  "${READER_FILES[@]}"     > "$TMP/reader.log" || rc=$?; viol=$((viol+rc))
    rc=0; run_checks litex  "$SOC" "${LITEX_PURE_FILES[@]}" > "$TMP/litex.log"  || rc=$?; viol=$((viol+rc))
    cat "$TMP/pure.log" "$TMP/reader.log" "$TMP/litex.log" | grep -v '^$' || true
    echo "--------------------------------------------------------------"
    echo "pure observers: ${#PURE_FILES[@]} file(s)   tap readers: ${#READER_FILES[@]} file(s)   MAC-site observers: ${#LITEX_PURE_FILES[@]} file(s)"
    echo "stream-net bindings checked: $n_bind (rx_axis_fabric: $n_rx_fabric, MAC transmit stream: $n_gmii)   violations: $viol"
    if [ "$n_bind" -eq 0 ]; then
        echo "  [ERROR] zero stream-net bindings resolved - the wiring parse went vacuous"
        viol=$((viol+1))
    fi
    if [ "$n_rx_fabric" -eq 0 ]; then
        echo "  [ERROR] zero bindings resolved on the live rx_axis_fabric observer seam"
        viol=$((viol+1))
    fi
    if [ "$n_gmii" -eq 0 ]; then
        echo "  [ERROR] zero bindings resolved on the MAC's own transmit stream - the Migen site parse went vacuous"
        viol=$((viol+1))
    fi
    echo "TAP-PURITY RESULT: $([ "$viol" -eq 0 ] && echo PASS || echo FAIL)"
    [ "$viol" -eq 0 ]
}

main() {
    echo "== observer-purity structural check (taps/telemetry never drive streams) =="
    TMP="$(mktemp -d)"
    trap 'rm -rf "$TMP"' EXIT
    selftest_checker
    check_tree
}

main "$@"
