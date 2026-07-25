#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# Observer-purity structural gate (the host-plane regression class, 2026-07-25):
# tap/telemetry modules must drive ONLY their own CSR/counter outputs and
# NEVER drive the observed streams' tvalid/tready/tdata/tkeep/tlast/tuser
# nets. An "observer" that participates in a stream handshake is a datapath
# actor wearing telemetry clothing - the wiring-mistake class that can kill a
# host lane while every green TB watches the counters instead of the stream.
#
# Two disciplined text-level checks over the SOURCE (same parse style as
# scripts/check_tied_inputs.sh - the house pattern):
#   1. module level (PURE observers: hdl/**/*_taps.sv + the AVTP RX
#      monitors): no OUTPUT port may carry a stream-handshake name
#      (tvalid/tready/tdata/tkeep/tlast/tuser);
#   2. site level (pure observers + every raw-stream tap reader wired in
#      hdl/milan/milan_datapath.sv - AECP/ACMP/parser/MAAP/lwSRP): every
#      instantiation port binding one of the datapath's observed stream nets
#      (rx_axis_*/tx_axis_*/ts_metadata_axis members, [sm]_axis_* boundary
#      lanes) must be an INPUT of that module - reads only, never drives.
#      The bindings-checked count is printed so a vacuous pass is visible.
#
# A negative SELF-TEST runs first on a deliberately-broken fixture; if the
# checker fails to flag it, the checker itself is declared broken (exit 3).
#
#   syn/yosys/check_tap_purity.sh   # exit 0 clean / 1 violation / 3 self-test broken
#
# Wired into syn/yosys/run.sh as a trailing report next to the tied-input
# inventory; standalone use is the exit-coded gate.

set -u
R="$(cd "$(dirname "$0")/../.." && pwd)"
DP="$R/hdl/milan/milan_datapath.sv"

# PURE observers: telemetry-only modules - both checks apply.
PURE_FILES=()
while IFS= read -r f; do PURE_FILES+=("$f"); done \
    < <(find "$R/hdl" -name "*_taps.sv" | sort)
PURE_FILES+=("$R/hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv"
             "$R/hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv")

# Raw-stream tap READERS (monitor-tap + low-rate-TX engines): they own their
# own TX lanes, so only the site-level input-only rule applies to the
# OBSERVED stream nets they tap.
READER_FILES=(
    "$R/hdl/ieee17221/aecp/KL_aecp_top.sv"
    "$R/hdl/ieee17221/acmp/KL_acmp_responder.sv"
    "$R/hdl/ieee17221/acmp/KL_acmp_listener.sv"
    "$R/hdl/ieee1722/avtp/avtp_stream_parser.sv"
    "$R/hdl/ieee1722/maap/KL_maap.sv"
    "$R/hdl/ieee8021q/srp/KL_lwsrp_top.sv"
)

STREAM_TERM='t(valid|ready|data|keep|last|user)'
# nets a tap may READ but never DRIVE (datapath interface members + flat
# boundary lanes of milan_datapath)
STREAM_NET_RE='((rx_axis_to_ts|rx_axis_ptp_to_filt|rx_axis_to_dma|ts_metadata_axis|tx_axis_to_shaper|tx_axis_shaper_to_ts|tx_axis_dp_to_arb|tx_axis_to_mac)\.t(valid|ready|data|keep|last|user)|[sm]_axis_[a-z_]*t(valid|ready|data|keep|last|user))'

n_bind=0    # stream-net bindings actually resolved (anti-vacuity witness)

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

# run_checks MODE(pure|reader) WIRING_FILE FILE... -> prints violations, returns count
run_checks() {
    local mode="$1" wiring="$2"; shift 2
    local viol=0 f m dirs dir name port expr
    for f in "$@"; do
        [ -r "$f" ] || { echo "  [ERROR] missing tap source $f"; viol=$((viol+1)); continue; }
        dirs="$(port_dirs "$f")"
        [ -n "$dirs" ] || { echo "  [ERROR] no ports parsed from $f (header drifted?)"; viol=$((viol+1)); continue; }
        for m in $(module_names "$f"); do
            if [ "$mode" = "pure" ]; then
                # 1) module level: no stream-handshake-named OUTPUT
                while read -r dir name; do
                    [ "$dir" = "output" ] || continue
                    if echo "$name" | grep -qE "$STREAM_TERM"; then
                        echo "  [VIOLATION] $m.$name: pure-observer OUTPUT carries a stream-handshake name"
                        viol=$((viol+1))
                    fi
                done <<< "$dirs"
            fi
            # 2) site level: observed stream nets land on INPUT ports only
            while IFS='|' read -r port expr; do
                [ -n "$port" ] || continue
                echo "$expr" | grep -qE "$STREAM_NET_RE" || continue
                n_bind=$((n_bind+1))
                dir="$(echo "$dirs" | awk -v p="$port" '$2 == p { print $1; exit }')"
                if [ -z "$dir" ]; then
                    echo "  [VIOLATION] $m.$port: bound to a stream net but not on the module header (parse drift)"
                    viol=$((viol+1))
                elif [ "$dir" != "input" ]; then
                    echo "  [VIOLATION] $m.$port ($dir) drives stream net '$(echo "$expr" | tr -s ' ')'"
                    viol=$((viol+1))
                fi
            done < <(inst_bindings "$wiring" "$m")
        done
    done
    return $viol
}

echo "== observer-purity structural check (taps/telemetry never drive streams) =="

# ---- negative self-test: the checker must FAIL a deliberately-broken fixture
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
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
    .rx_tvalid_i (rx_axis_to_dma.tvalid),
    .rx_tready_o (rx_axis_to_dma.tready)
  );
endmodule
EOF
self_out="$(run_checks pure "$TMP/fixture_dp.sv" "$TMP/bad_probe_taps.sv")"
self_n=$?
if [ "$self_n" -ge 2 ]; then
    echo "  negative self-test: checker flags the broken fixture ($self_n violations) - OK"
else
    echo "  negative self-test FAILED: broken fixture produced only $self_n finding(s):"
    echo "$self_out"
    echo "TAP-PURITY RESULT: CHECKER-BROKEN"
    exit 3
fi

# ---- the real tree ----------------------------------------------------------
[ -r "$DP" ] || { echo "  missing $DP"; exit 2; }
# in-shell runs (redirects, no subshell) so the n_bind witness accumulates
n_bind=0
viol=0
run_checks pure   "$DP" "${PURE_FILES[@]}"   > "$TMP/pure.log";   viol=$((viol+$?))
run_checks reader "$DP" "${READER_FILES[@]}" > "$TMP/reader.log"; viol=$((viol+$?))
cat "$TMP/pure.log" "$TMP/reader.log" | grep -v '^$' || true
echo "--------------------------------------------------------------"
echo "pure observers: ${#PURE_FILES[@]} file(s)   tap readers: ${#READER_FILES[@]} file(s)   stream-net bindings checked: $n_bind   violations: $viol"
if [ "$n_bind" -eq 0 ]; then
    echo "  [ERROR] zero stream-net bindings resolved - the wiring parse went vacuous"
    viol=$((viol+1))
fi
echo "TAP-PURITY RESULT: $([ "$viol" -eq 0 ] && echo PASS || echo FAIL)"
[ "$viol" -eq 0 ]
