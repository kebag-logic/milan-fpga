#!/usr/bin/env python3
"""Reviewer-designed mutants of hdl/milan/milan_datapath.sv for the #529 root wiring.

Each mutant is a set of exact textual substitutions; every search string must occur
exactly once in the source, or generation stops. Output, per mutant:
  OUT/<id>/milan_datapath.sv   the mutated copy
  OUT/<id>/mutant.diff         unified diff against the source
  OUT/<id>/desc.txt            one-line description
and OUT/index.tsv listing id, class and description.

usage: mutants.py SRC OUT
"""
import difflib
import itertools
import os
import sys

# the ten KL_crf_rx Table 5.16 outputs and the root wires the head binds them to
PORTS = [
    ("pdu_count_o", "crf_pducnt_w"),
    ("fmt_err_o", "crf_fmterr_w"),
    ("seq_err_o", "crf_seqerr_w"),
    ("mr_cnt_o", "crf_mrcnt_w"),
    ("tu_cnt_o", "crf_tucnt_w"),
    ("late_cnt_o", "crf_latecnt_w"),
    ("early_cnt_o", "crf_earlycnt_w"),
    ("cnt_locked_o", "crf_lockcnt_w"),
    ("cnt_unlocked_o", "crf_unlockcnt_w"),
    ("cnt_intr_o", "crf_intrcnt_w"),
]


def port_line(src, port, wire):
    """the exact instance connection text `.port   (wire)` as written in SRC"""
    hits = [ln for ln in src.splitlines()
            if ln.strip().startswith(f".{port} ") and f"({wire})" in ln]
    if len(hits) != 1:
        raise SystemExit(f"port {port}->{wire}: {len(hits)} lines")
    return hits[0]


def binding(src, mapping):
    """rebind ports: mapping port -> new wire. Returns substitution list."""
    subs = []
    for port, wire in PORTS:
        if port in mapping:
            ln = port_line(src, port, wire)
            subs.append((ln, ln.replace(f"({wire})", f"({mapping[port]})")))
    return subs


def mutants(src):
    out = []
    wires = dict(PORTS)
    # X: every pairwise exchange of two output bindings at the instance
    for (pa, wa), (pb, wb) in itertools.combinations(PORTS, 2):
        out.append((f"vx-{pa[:-2]}-{pb[:-2]}", "exchange",
                    f"instance: {pa} and {pb} exchange their root wires",
                    binding(src, {pa: wb, pb: wa})))
    # R3 / R10: rotations the pairwise set does not contain
    out.append(("vr3-mr-tu-late", "rotation",
                "instance: mr->tu wire, tu->late wire, late->mr wire (3-cycle)",
                binding(src, {"mr_cnt_o": wires["tu_cnt_o"],
                              "tu_cnt_o": wires["late_cnt_o"],
                              "late_cnt_o": wires["mr_cnt_o"]})))
    rot = {PORTS[i][0]: PORTS[(i + 1) % 10][1] for i in range(10)}
    out.append(("vr10", "rotation", "instance: every output moved to the next wire (10-cycle)",
                binding(src, rot)))
    # G: the gather row
    g = []
    g.append(("vg-lvl-q0", "row",
              "row: quadlet 0 serves the lock LEVEL, not the MEDIA_LOCKED tally",
              [("6'd0    : ctr_crf_blk_w = crf_lockcnt_w;",
                "6'd0    : ctr_crf_blk_w = {31'd0, crf_locked_w};")]))
    g.append(("vg-dup-q1", "row", "row: quadlet 1 serves MEDIA_LOCKED again",
              [("6'd1    : ctr_crf_blk_w = crf_unlockcnt_w;",
                "6'd1    : ctr_crf_blk_w = crf_lockcnt_w;")]))
    g.append(("vg-q9-q10", "row", "row: LATE and EARLY quadlets exchanged",
              [("6'd9    : ctr_crf_blk_w = crf_latecnt_w;",
                "6'd9    : ctr_crf_blk_w = crf_earlycnt_w;"),
               ("6'd10   : ctr_crf_blk_w = crf_earlycnt_w;",
                "6'd10   : ctr_crf_blk_w = crf_latecnt_w;")]))
    g.append(("vg-slice-q2", "row", "row: STREAM_INTERRUPTED served through a 16-bit slice",
              [("6'd2    : ctr_crf_blk_w = crf_intrcnt_w;",
                "6'd2    : ctr_crf_blk_w = {16'd0, crf_intrcnt_w[15:0]};")]))
    g.append(("vg-mask-3f", "row", "row: mask 0x03F (drops UF/LT/ET/FRX claims)",
              [("CTR_VALID_CRF_C = 32'h0000_0F3F;", "CTR_VALID_CRF_C = 32'h0000_003F;")]))
    g.append(("vg-mask-fff", "row", "row: mask 0xFFF (claims the untallied tv pair)",
              [("CTR_VALID_CRF_C = 32'h0000_0F3F;", "CTR_VALID_CRF_C = 32'h0000_0FFF;")]))
    g.append(("vg-idx-plus1", "guard", "guard: the CRF row answers at N_STREAMS + 1",
              [("&& (32'(ctrq_index_r) == CRF_SNK_IDX_C);",
                "&& (32'(ctrq_index_r) == CRF_SNK_IDX_C + 1);")]))
    g.append(("vg-no-type", "guard",
              "guard: the CRF row ignores descriptor_type (answers any type at index N)",
              [("                && (ctrq_type_r == DESC_STREAM_INPUT_C)\n"
                "                && (32'(ctrq_index_r) == CRF_SNK_IDX_C);",
                "                && (32'(ctrq_index_r) == CRF_SNK_IDX_C);")]))
    g.append(("vg-sin-le", "guard", "guard: the AAF row answers index N_STREAMS too",
              [("&& (ctrq_index_r < 16'(N_STREAMS));", "&& (ctrq_index_r <= 16'(N_STREAMS));")]))
    # the remaining classes the head's docs list (REGISTER_MAP criterion 4). A
    # mutant that removes the only reader of a tally lets the simulator drop the
    # wire the harness seeds by name, so those copies (and a marked-only control)
    # carry a visibility marking with no logic effect.
    mark = [("  wire [31:0] crf_lockcnt_w, crf_unlockcnt_w, crf_intrcnt_w;\n"
             "  wire [31:0] crf_mrcnt_w, crf_tucnt_w, crf_latecnt_w, crf_earlycnt_w;\n",
             "".join(f"  wire [31:0] {w} /* verilator public_flat_rw */;\n"
                     for w in ("crf_lockcnt_w", "crf_unlockcnt_w", "crf_intrcnt_w",
                               "crf_mrcnt_w", "crf_tucnt_w", "crf_latecnt_w",
                               "crf_earlycnt_w")))]
    g.append(("vg-ctl-marked", "control", "control: the visibility marking alone (must stay green)",
              list(mark)))
    g.append(("vg-row-removed", "row", "row: the CRF arm removed from the answer mux (marked)",
              mark + [("                       : ctr_crf_w ? ctr_crf_blk_w\n", "")]))
    g.append(("vg-q2-zero", "row",
              "row: STREAM_INTERRUPTED quadlet tied to zero, one tally unwired (marked)",
              mark + [("6'd2    : ctr_crf_blk_w = crf_intrcnt_w;",
                       "6'd2    : ctr_crf_blk_w = 32'd0;")]))
    g.append(("vg-crf-first-noidx", "guard",
              "guard: the CRF arm, without its index term, ahead of the AAF arm",
              [("                && (ctrq_type_r == DESC_STREAM_INPUT_C)\n"
                "                && (32'(ctrq_index_r) == CRF_SNK_IDX_C);",
                "                && (ctrq_type_r == DESC_STREAM_INPUT_C);"),
               ("  assign ctr_ans_raw_w = ctr_sin_w ? ctr_blk_w\n"
                "                       : ctr_crf_w ? ctr_crf_blk_w\n",
                "  assign ctr_ans_raw_w = ctr_crf_w ? ctr_crf_blk_w\n"
                "                       : ctr_sin_w ? ctr_blk_w\n")]))
    out.extend(g)
    # D: the Table 5.22 arbiter
    d = []
    d.append(("vd-nodirty", "arbiter", "arbiter: the CRF dirty pulse dropped",
              [("assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w};",
                "assign pp_ctr_sin_dirty_w = {1'b0, avtprx_dirty_p_w};")]))
    d.append(("vd-to-idx0", "arbiter", "arbiter: the CRF dirty pulse delivered as STREAM_INPUT 0",
              [("assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w};",
                "assign pp_ctr_sin_dirty_w = {1'b0, avtprx_dirty_p_w "
                "| N_STREAMS'(crf_dirty_p_w)};")]))
    d.append(("vd-clear-stuck", "arbiter", "arbiter: the CRF row's pending bit never clears",
              [("for (int unsigned s = 0; s < PP_CTR_SIN_N_C; s++) begin",
                "for (int unsigned s = 0; s < N_STREAMS; s++) begin")]))
    d.append(("vd-sout-off", "arbiter",
              "arbiter: STREAM_OUTPUT index still offset by N_STREAMS (pre-#529 formula)",
              [("pp_ctr_evt_index_w = 16'(pick - PP_CTR_SIN_N_C);",
                "pp_ctr_evt_index_w = 16'(pick - N_STREAMS);")]))
    d.append(("vd-avb-pick", "arbiter",
              "arbiter: AVB_INTERFACE selected at the pre-#529 position",
              [("end else if (pick == (PP_CTR_SIN_N_C + ACMP_SRC_C)) begin",
                "end else if (pick == (N_STREAMS + ACMP_SRC_C)) begin")]))
    d.append(("vd-rr-sout", "arbiter",
              "arbiter: round-robin resume after a STREAM_OUTPUT uses N_STREAMS",
              [("pp_ctr_rr_r <= PP_CTR_RR_W_C'(PP_CTR_SIN_N_C\n",
                "pp_ctr_rr_r <= PP_CTR_RR_W_C'(N_STREAMS\n")]))
    # E: the CRF pulse ALSO delivered as another descriptor (probes the docs'
    # "as {STREAM_INPUT, N_STREAMS} and as nothing else")
    d.append(("ve-also-ckd", "extra-tuple",
              "arbiter: the CRF dirty pulse also raises CLOCK_DOMAIN 0",
              [("pp_ctr_ckd_pend_n  = pp_ctr_ckd_pend_r  | ctr_ckd_dirty_w;",
                "pp_ctr_ckd_pend_n  = pp_ctr_ckd_pend_r  | ctr_ckd_dirty_w | crf_dirty_p_w;")]))
    d.append(("ve-also-sout", "extra-tuple",
              "arbiter: the CRF dirty pulse also raises STREAM_OUTPUT N_STREAMS",
              [("pp_ctr_sout_pend_n = pp_ctr_sout_pend_r | tkd_dirty_p_w;",
                "pp_ctr_sout_pend_n = pp_ctr_sout_pend_r | tkd_dirty_p_w"
                " | (ACMP_SRC_C'(crf_dirty_p_w) << N_STREAMS);")]))
    out.extend(d)
    return out


def main():
    src_path, outdir = sys.argv[1], sys.argv[2]
    src = open(src_path).read()
    os.makedirs(outdir, exist_ok=True)
    rows = []
    for mid, cls, desc, subs in mutants(src):
        m = src
        for a, b in subs:
            n = m.count(a)
            if n != 1:
                raise SystemExit(f"{mid}: search text occurs {n} times: {a!r}")
            m = m.replace(a, b)
        if m == src:
            raise SystemExit(f"{mid}: no change")
        d = os.path.join(outdir, mid)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "milan_datapath.sv"), "w").write(m)
        diff = difflib.unified_diff(src.splitlines(True), m.splitlines(True),
                                    "a/hdl/milan/milan_datapath.sv",
                                    "b/hdl/milan/milan_datapath.sv")
        open(os.path.join(d, "mutant.diff"), "w").writelines(diff)
        open(os.path.join(d, "desc.txt"), "w").write(desc + "\n")
        rows.append(f"{mid}\t{cls}\t{desc}")
    open(os.path.join(outdir, "index.tsv"), "w").write("\n".join(rows) + "\n")
    print(f"{len(rows)} mutants")


if __name__ == "__main__":
    main()
