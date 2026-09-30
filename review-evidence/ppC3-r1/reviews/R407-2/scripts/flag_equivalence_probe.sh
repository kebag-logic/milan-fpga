#!/usr/bin/env bash
# Disposable probe: export the exact head, add a cycle monitor inside
# KL_aecp_engine comparing the published flag (dyn_cfg_v_r) with the store's
# own cfg_v_r in EVERY clock of the full default tb/pp_top run (main suite,
# GSI, name writes, D3, AD), and count each way the flag can move.
# Arg 1: variant name; optional arg 2: an ADP campaign patch to plant (control).
set -euo pipefail
source "$(dirname "$0")/env.sh"
name="$1"; patch="${2:-}"
T="$PKT/scratch/probe-$name"; rm -rf "$T"; mkdir -p "$T"
git -C "$CLONE" archive 20ec92b7b190d03c46e40be89d236bc9a0702a59 | tar -x -C "$T"
[ -n "$patch" ] && git -C "$T" apply "$CLONE/tb/adp_engine/mutations/$patch.patch" 2>/dev/null || { [ -n "$patch" ] && (cd "$T" && patch -p1 < "$CLONE/tb/adp_engine/mutations/$patch.patch"); }
python3 - "$T/hdl/aecp/KL_aecp_engine.sv" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
anchor = "  assign dyn_cur_config_v_o = dyn_cfg_v_r;\n"
assert s.count(anchor) == 1
probe = r'''
  // ---- REVIEW PROBE (disposable, never published as source) ----
  int unsigned prb_mis = 0, prb_wr_u = 0, prb_wr_w = 0, prb_clr_rst = 0, prb_clr_rb = 0, prb_cyc = 0;
  logic prb_hit_w;
  assign prb_hit_w = st_req_w && dyn_sel_w && st_we_w && (st_addr_w[19:16] == RGN_DYN_C)
                     && (st_addr_w[15:3] == 13'd0);
  always_ff @(posedge clk_i) begin : review_probe
    prb_cyc <= prb_cyc + 1;
    if (dyn_cfg_v_r !== u_dyn.cfg_v_r) begin
      prb_mis <= prb_mis + 1;
      if (prb_mis < 10) $display("PROBE-MISMATCH cyc=%0d published=%0b store=%0b", prb_cyc, dyn_cfg_v_r, u_dyn.cfg_v_r);
    end
    if (store_rst_n_w && prb_hit_w && !d3_bus_w) begin prb_wr_u <= prb_wr_u + 1;
      $display("PROBE-EV ucpu-cfg-write n=%0d didx=%0d store_v=%0b pub_v=%0b", prb_wr_u + 1, dyn_didx_w, u_dyn.cfg_v_r, dyn_cfg_v_r); end
    if (store_rst_n_w && prb_hit_w &&  d3_bus_w) begin prb_wr_w <= prb_wr_w + 1;
      $display("PROBE-EV writer-cfg-write n=%0d didx=%0d wdata=%0h", prb_wr_w + 1, dyn_didx_w, st_wdata_w[15:0]); end
    if (!rst_n && u_dyn.cfg_v_r) begin prb_clr_rst <= prb_clr_rst + 1;
      if (prb_clr_rst < 3) $display("PROBE-EV hard-reset-with-flag-set n=%0d pub_v=%0b", prb_clr_rst + 1, dyn_cfg_v_r); end
    if (rst_n && d3_rb_rst_w && u_dyn.cfg_v_r) begin prb_clr_rb <= prb_clr_rb + 1;
      $display("PROBE-EV rollback-with-flag-set n=%0d pub_v=%0b", prb_clr_rb + 1, dyn_cfg_v_r); end
  end
'''
s = s.replace(anchor, anchor + probe)
open(p, "w").write(s)
PY
cd "$T/tb/pp_top"
set +e
$CAP make run > "$PKT/receipts/probe-$name.log" 2>&1
rc=$?
set -e
echo "make rc=$rc" >> "$PKT/receipts/probe-$name.log"
grep -E 'checks, [0-9]+ failures|^make rc' "$PKT/receipts/probe-$name.log" | tail -4
echo "mismatch lines: $(grep -c PROBE-MISMATCH "$PKT/receipts/probe-$name.log")"
for k in ucpu-cfg-write writer-cfg-write hard-reset-with-flag-set rollback-with-flag-set; do
  echo "$k events: $(grep -c "PROBE-EV $k" "$PKT/receipts/probe-$name.log")"
done
