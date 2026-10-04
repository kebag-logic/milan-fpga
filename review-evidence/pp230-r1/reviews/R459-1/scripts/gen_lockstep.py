#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate a base-vs-head lockstep checker for KL_srp_top.

usage: gen_lockstep.py BASE_HDL_DIR HEAD_HDL_DIR OUT_DIR

Writes into OUT_DIR:
  ref/*.sv          the base SRP modules, every module renamed <name>_ref
  lockstep_chk.sv   a checker holding KL_srp_top_ref; it compares every
                    output of KL_srp_top and a set of internal signals
                    with the reference every clock after the first reset
  lockstep_bind.sv  binds the checker into every KL_srp_top instance

Adding ref/*.sv, lockstep_chk.sv and lockstep_bind.sv to any bench's
source list makes that bench a lockstep bench (the bench itself is not
edited). A mismatch is $fatal unless +ls_count is given, in which case
mismatching cycles are counted and printed by the final block.
"""
import pathlib
import re
import sys

SRP_MODS = ["KL_srp_decoder", "KL_srp_domain", "KL_srp_vlan",
            "KL_srp_talker_fsm", "KL_srp_listener_fsm", "KL_srp_admission",
            "KL_srp_encoder", "KL_srp_top"]

# Internal signals: (name, head expression in KL_srp_top scope,
# reference expression under u_ref, gate expression or None). With a gate,
# the gates must agree and the values are compared only while it is set.
INTERNALS = [
    ("tk_app_state", "u_talker.dbg_app_state_o", None),
    ("tk_reg_state", "u_talker.dbg_reg_state_o", None),
    ("ls_app_state", "u_listener.dbg_app_state_o", None),
    ("ls_reg_state", "u_listener.dbg_reg_state_o", None),
    ("tk_ev_valid", "u_talker.ev_valid_o", None),
    ("tk_ev_type", "u_talker.ev_attr_type_o", None),
    ("tk_ev_event", "u_talker.ev_event_o", None),
    ("tk_ev_value", "u_talker.ev_value_o", None),
    ("ls_ev_valid", "u_listener.ev_valid_o", None),
    ("ls_ev_event", "u_listener.ev_event_o", None),
    ("ls_ev_fourpack", "u_listener.ev_fourpack_o", None),
    ("ls_ev_value", "u_listener.ev_value_o", None),
    ("tk_txop_done", "u_talker.txop_done_o", None),
    ("ls_txop_done", "u_listener.txop_done_o", None),
    ("tk_user", "{u_talker.user_valid_o, u_talker.user_join_o, u_talker.user_vid_o}", None),
    ("tk_arm", "{u_talker.arm_valid_o, u_talker.arm_cancel_o, u_talker.arm_slot_o, u_talker.arm_owner_o, u_talker.arm_deadline_ms_o}", None),
    ("ls_arm", "{u_listener.arm_valid_o, u_listener.arm_cancel_o, u_listener.arm_slot_o, u_listener.arm_owner_o, u_listener.arm_deadline_ms_o}", None),
    ("tk_rec_valid", "u_talker.rec_valid_r", None),
    ("tk_walk", "{u_talker.walk_r, u_talker.wsrc_r, u_talker.wtxla_r}", None),
    ("ls_rec_valid", "u_listener.rec_valid_r", None),
    ("ls_walk", "{u_listener.walk_r, u_listener.wsrc_r, u_listener.wtxla_r}", None),
    # the walk's FirstValue, read through the RAM copies at head
    ("tk_wval", "u_talker.wval_w", "u_talker.rec_valid_r[u_talker.wsrc_r]"),
    ("ls_wval", "u_listener.wval_w", "u_listener.rec_valid_r[u_listener.wsrc_r]"),
    # admission: the slope read point and the walk state
    ("adm_slope_valid", "u_admission.slope_valid_r", None),
    ("adm_aidx", "u_admission.aidx_r", None),
    ("adm_slope_rd", "u_admission.slope_q_r[u_admission.aidx_r]",
     "u_admission.slope_valid_r[u_admission.aidx_r]"),
    ("adm_acc", "{u_admission.acc_r, u_admission.over_acc_r, u_admission.pend_acc_r}", None),
    ("adm_wgrant", "u_admission.wgrant_r", None),
    ("adm_wgslope", "u_admission.wgslope_r", None),
    ("adm_grant", "u_admission.grant_r", None),
    ("adm_gslope", "u_admission.gslope_r", None),
    ("adm_round", "u_admission.round_done_o", None),
    # timer-arm FIFO bookkeeping and the head consumed in TM_POP
    ("tf_push", "tf_push_w", None),
    ("tf_pop", "tf_pop_w", None),
    ("tf_cnt", "{tf_cnt_r[0], tf_cnt_r[1]}", None),
    ("tf_wptr", "{tf_wptr_r[0], tf_wptr_r[1]}", None),
    ("tf_rptr", "{tf_rptr_r[0], tf_rptr_r[1]}", None),
    ("tm_state", "{tm_st_r, tm_sel_r, tm_rr_r}", None),
    ("tf_head", "tf_q_r[tm_sel_r]", "(tm_st_r == 1'b1)"),
    ("cad", "{cad_pend_r, cad_dl_r}", None),
]


def ports_of(top_src: str):
    body = top_src[top_src.index(") (", top_src.index("module KL_srp_top")):]
    body = body[:body.index(");")]
    ports = []
    for line in body.splitlines():
        line = line.split("//")[0].strip().rstrip(",")
        m = re.match(r"(input|output)\s+(wire|logic)\s*(.*?)\s*(\w+)$", line)
        if m:
            ports.append((m.group(1), m.group(3), m.group(4)))
    return ports


def params_of(top_src: str):
    head = top_src[top_src.index("module KL_srp_top"):]
    head = head[:head.index(") (")]
    return re.findall(r"^\s*parameter\s+(.*?)\s+(\w+)\s*=\s*([^,]+?),?\s*$",
                      head, re.M)


def ref_expr(ex):
    ex = re.sub(r"\b(u_talker|u_listener|u_admission)\b", r"u_ref.\1", ex)
    return re.sub(r"(?<![.\w])(tf_\w+|tm_\w+|cad_\w+)\b", r"u_ref.\1", ex)


W = 1024   # internal compare width (zero-extended both sides)


def main():
    base, headd, out = map(pathlib.Path, sys.argv[1:4])
    (out / "ref").mkdir(parents=True, exist_ok=True)
    pat = re.compile(r"\b(" + "|".join(SRP_MODS) + r")\b")
    for m in SRP_MODS:
        src = (base / "srp" / f"{m}.sv").read_text()
        (out / "ref" / f"{m}_ref.sv").write_text(pat.sub(r"\1_ref", src))
    top = (headd / "srp" / "KL_srp_top.sv").read_text()
    btop = (base / "srp" / "KL_srp_top.sv").read_text()
    ports, params = ports_of(top), params_of(top)
    assert ports == ports_of(btop) and params == params_of(btop), "port/param drift"
    outs = [p for p in ports if p[0] == "output"]
    L = ["// generated by gen_lockstep.py: base KL_srp_top_ref beside head KL_srp_top",
         "`default_nettype none", "module lockstep_chk", "  import srp_pkg::*;", "#("]
    L.append(",\n".join(f"  parameter {t} {n} = {v}" for t, n, v in params) + ",")
    L.append("  localparam int unsigned SRC_W_C  = (N_SOURCES_P > 1) ? $clog2(N_SOURCES_P) : 1,")
    L.append("  localparam int unsigned SNK_W_C  = (N_SINKS_P > 1) ? $clog2(N_SINKS_P) : 1,")
    L.append("  localparam int unsigned SLOT_W_C = $bits(pp_pkg::PP_SLOT_NULL_C),")
    L.append("  localparam int unsigned TXA_W_C  = $clog2(TX_OVERSIZE_BYTES_P + 1)")
    L.append(") (")
    decl = [f"  input wire {w} {n}" for d, w, n in ports]
    for nm, ex, g in INTERNALS:
        decl.append(f"  input wire [{W-1}:0] h_{nm}")
        if g is not None:
            decl.append(f"  input wire g_{nm}")
    L.append(",\n".join(decl))
    L.append(");")
    for d, w, n in outs:
        L.append(f"  logic {w} r_{n};")
    L.append("  KL_srp_top_ref #(")
    L.append(",\n".join(f"    .{n}({n})" for _, n, _ in params))
    L.append("  ) u_ref (")
    L.append(",\n".join(f"    .{n}({n if d == 'input' else 'r_' + n})" for d, w, n in ports))
    L.append("  );")
    L.append("  bit seen_rst = 0, count_mode = 0;")
    L.append("  longint unsigned cyc = 0, bad_cyc = 0, cmp_cyc = 0, rst_cyc = 0, rst_edges = 0;")
    L.append("  bit rst_q = 1;")
    L.append(f"  longint unsigned gated[0:{len(INTERNALS)-1}];")
    L.append("  longint unsigned tf_full_cyc[0:1], tf_push_empty[0:1], tf_push_pop[0:1], tf_pops[0:1], tf_push_full_blocked[0:1];")
    L.append("  int unsigned tf_max[0:1];")
    L.append("  initial begin")
    L.append("    count_mode = $test$plusargs(\"ls_count\");")
    L.append("    foreach (gated[i]) gated[i] = 0;")
    L.append("    for (int u = 0; u < 2; u++) begin tf_full_cyc[u] = 0; tf_push_empty[u] = 0; tf_push_pop[u] = 0; tf_pops[u] = 0; tf_max[u] = 0; tf_push_full_blocked[u] = 0; end")
    L.append("  end")
    L.append("  always @(posedge clk_i) begin : compare")
    L.append("    automatic bit bad = 0;")
    L.append("    if (seen_rst) begin")
    L.append("      cmp_cyc++;")
    for d, w, n in outs:
        L.append(f"      if ({n} !== r_{n}) begin bad = 1; if (bad_cyc < 10) $display(\"LOCKSTEP MISMATCH cyc=%0d out {n} head=%h ref=%h\", cyc, {n}, r_{n}); end")
    for i, (nm, ex, g) in enumerate(INTERNALS):
        rex = ref_expr(ex)
        if g is None:
            L.append(f"      if (h_{nm} !== {W}'({rex})) begin bad = 1; if (bad_cyc < 10) $display(\"LOCKSTEP MISMATCH cyc=%0d int {nm}\", cyc); end")
        else:
            rg = ref_expr(g)
            L.append(f"      if (g_{nm} !== 1'({rg})) begin bad = 1; if (bad_cyc < 10) $display(\"LOCKSTEP MISMATCH cyc=%0d gate {nm}\", cyc); end")
            L.append(f"      else if (g_{nm}) begin gated[{i}]++; if (h_{nm} !== {W}'({rex})) begin bad = 1; if (bad_cyc < 10) $display(\"LOCKSTEP MISMATCH cyc=%0d gated {nm}\", cyc); end end")
    L.append("      if (rst_n) for (int u = 0; u < 2; u++) begin")
    L.append("        if (u_ref.tf_cnt_r[u] == 6'd32) tf_full_cyc[u]++;")
    L.append("        if (u_ref.tf_push_w[u] && u_ref.tf_cnt_r[u] == 6'd0) tf_push_empty[u]++;")
    L.append("        if (u_ref.tf_push_w[u] && u_ref.tf_pop_w[u]) tf_push_pop[u]++;")
    L.append("        if (u_ref.tf_pop_w[u]) tf_pops[u]++;")
    L.append("        if (32'(u_ref.tf_cnt_r[u]) > tf_max[u]) tf_max[u] = 32'(u_ref.tf_cnt_r[u]);")
    L.append("      end")
    L.append("      if (rst_n && (u_ref.tk_arm_v_w && !u_ref.tf_push_w[0])) tf_push_full_blocked[0]++;")
    L.append("      if (rst_n && (u_ref.ls_arm_v_w && !u_ref.tf_push_w[1])) tf_push_full_blocked[1]++;")
    L.append("      if (bad) begin")
    L.append("        bad_cyc++;")
    L.append("        if (!count_mode) $fatal(1, \"LOCKSTEP: head and base KL_srp_top diverge at cycle %0d (%m)\", cyc);")
    L.append("      end")
    L.append("    end")
    L.append("    // compare from the edge after the first reset edge (unreset start)")
    L.append("    if (!rst_n) begin seen_rst = 1; rst_cyc++; if (rst_q) rst_edges++; end")
    L.append("    rst_q = rst_n;")
    L.append("    cyc++;")
    L.append("  end")
    L.append("  final begin")
    L.append(f"    $display(\"LOCKSTEP SUMMARY %m M=%0d N=%0d cycles=%0d compared=%0d mismatching=%0d reset_cycles=%0d reset_assertions=%0d outputs={len(outs)} internals={len(INTERNALS)}\", N_SOURCES_P, N_SINKS_P, cyc, cmp_cyc, bad_cyc, rst_cyc, rst_edges);")
    cov = [(nm, i) for i, (nm, _, g) in enumerate(INTERNALS) if g is not None]
    L.append("    $display(\"LOCKSTEP COVER %m " + " ".join(f"{nm}=%0d" for nm, _ in cov) + "\", "
             + ", ".join(f"gated[{i}]" for _, i in cov) + ");")
    L.append("    $display(\"LOCKSTEP FIFO %m tk: max=%0d full_cycles=%0d full_blocked_pushes=%0d push_into_empty=%0d push_with_pop=%0d pops=%0d | ls: max=%0d full_cycles=%0d full_blocked_pushes=%0d push_into_empty=%0d push_with_pop=%0d pops=%0d\", tf_max[0], tf_full_cyc[0], tf_push_full_blocked[0], tf_push_empty[0], tf_push_pop[0], tf_pops[0], tf_max[1], tf_full_cyc[1], tf_push_full_blocked[1], tf_push_empty[1], tf_push_pop[1], tf_pops[1]);")
    L.append("  end")
    L.append("endmodule")
    L.append("`default_nettype wire")
    (out / "lockstep_chk.sv").write_text("\n".join(L) + "\n")
    b = ["// generated by gen_lockstep.py", "bind KL_srp_top lockstep_chk #("]
    b.append(",\n".join(f"  .{n}({n})" for _, n, _ in params))
    conns = [".*"]
    for nm, ex, g in INTERNALS:
        conns.append(f".h_{nm}({W}'({ex}))")
        if g is not None:
            conns.append(f".g_{nm}({g})")
    b.append(") u_lockstep (\n  " + ",\n  ".join(conns) + "\n);")
    (out / "lockstep_bind.sv").write_text("\n".join(b) + "\n")
    print(f"ports {len(ports)} outputs {len(outs)} internals {len(INTERNALS)}")


if __name__ == "__main__":
    main()
