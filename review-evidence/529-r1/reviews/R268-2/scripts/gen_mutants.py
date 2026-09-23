#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Generate the round's independent milan_datapath.sv mutants.

usage: gen_mutants.py <milan_datapath.sv at the reviewed head> <outdir>

Writes <outdir>/<id>.sv and <outdir>/<id>.diff for every mutant, plus
<outdir>/INDEX.tsv (id, class, description, sha256 of the mutant). Every
substitution is anchored on the exact source text it replaces and must match
exactly once, so a drifted source refuses rather than yielding a no-op mutant.

Classes
  swap   the 45 pairwise exchanges of the ten KL_crf_rx tally outputs at the
         crf_rx instance (both port bindings rewritten, nothing else)
  mux    gather-face (ctr_crf_block / ctr_crf_w / priority) faults
  dirty  Table 5.22 source and arbiter faults
  tally  a tally output unbound at the instance and its root wire tied off
  tout   the root's CLK_FREQ_HZ_P binding of KL_crf_rx, which sets the 100 ms
         silence timeout the event arm's shortcut advances
"""
import difflib
import hashlib
import itertools
import pathlib
import sys

PORTS = [  # (port, root wire) in instance order
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
INST_OPEN = "  ) crf_rx (\n"
INST_CLOSE = "    .dirty_p_o      (crf_dirty_p_w)\n  );\n"


def once(src: str, old: str, new: str) -> str:
    n = src.count(old)
    if n != 1:
        raise SystemExit(f"anchor matched {n} times, need 1: {old!r}")
    return src.replace(old, new)


def instance_span(src: str) -> tuple[int, int]:
    a = src.index(INST_OPEN)
    b = src.index(INST_CLOSE, a) + len(INST_CLOSE)
    return a, b


def port_line(block: str, port: str, wire: str) -> str:
    for ln in block.splitlines(keepends=True):
        s = ln.strip()
        if s.startswith(f".{port} ") or s.startswith(f".{port}("):
            if f"({wire})" not in ln:
                raise SystemExit(f"{port} not bound to {wire}: {ln!r}")
            return ln
    raise SystemExit(f"port {port} not found in the crf_rx instance")


def swap(src: str, i: int, j: int) -> str:
    a, b = instance_span(src)
    blk = src[a:b]
    (pi, wi), (pj, wj) = PORTS[i], PORTS[j]
    li, lj = port_line(blk, pi, wi), port_line(blk, pj, wj)
    blk = once(blk, li, li.replace(f"({wi})", f"({wj})"))
    blk = once(blk, lj, lj.replace(f"({wj})", f"({wi})"))
    return src[:a] + blk + src[b:]


def unbind(src: str, k: int) -> str:
    a, b = instance_span(src)
    blk = src[a:b]
    p, w = PORTS[k]
    ln = port_line(blk, p, w)
    blk = once(blk, ln, ln.replace(f"({w})", "()"))
    blk = blk + f"  assign {w} = 32'd0;\n"
    return src[:a] + blk + src[b:]


MUX = {
    "mux_q01_swap": ("quadlets 0 and 1 of ctr_crf_block exchanged",
        [("      6'd0    : ctr_crf_blk_w = crf_lockcnt_w;   // @0   MEDIA_LOCKED\n"
          "      6'd1    : ctr_crf_blk_w = crf_unlockcnt_w; // @4   MEDIA_UNLOCKED\n",
          "      6'd0    : ctr_crf_blk_w = crf_unlockcnt_w;   // @0   MEDIA_LOCKED\n"
          "      6'd1    : ctr_crf_blk_w = crf_lockcnt_w; // @4   MEDIA_UNLOCKED\n")]),
    "mux_q9_q10_swap": ("quadlets 9 (LATE) and 10 (EARLY) exchanged",
        [("      6'd9    : ctr_crf_blk_w = crf_latecnt_w;   // @36  LATE_TIMESTAMP\n"
          "      6'd10   : ctr_crf_blk_w = crf_earlycnt_w;  // @40  EARLY_TIMESTAMP\n",
          "      6'd9    : ctr_crf_blk_w = crf_earlycnt_w;   // @36  LATE_TIMESTAMP\n"
          "      6'd10   : ctr_crf_blk_w = crf_latecnt_w;  // @40  EARLY_TIMESTAMP\n")]),
    "mux_frx_16bit": ("FRAMES_RX served through a 16-bit slice",
        [("      6'd11   : ctr_crf_blk_w = crf_pducnt_w;    // @44  FRAMES_RX\n",
          "      6'd11   : ctr_crf_blk_w = {16'd0, crf_pducnt_w[15:0]};    // @44  FRAMES_RX\n")]),
    "mux_mr_dup_tu": ("MEDIA_RESET quadlet serves the TIMESTAMP_UNCERTAIN tally",
        [("      6'd4    : ctr_crf_blk_w = crf_mrcnt_w;     // @16  MEDIA_RESET\n",
          "      6'd4    : ctr_crf_blk_w = crf_tucnt_w;     // @16  MEDIA_RESET\n")]),
    "mux_mask_fff": ("mask claims the tv pair (0xFFF)",
        [("localparam logic [31:0] CTR_VALID_CRF_C = 32'h0000_0F3F;",
          "localparam logic [31:0] CTR_VALID_CRF_C = 32'h0000_0FFF;")]),
    "mux_mask_f3e": ("mask drops MEDIA_LOCKED (0xF3E)",
        [("localparam logic [31:0] CTR_VALID_CRF_C = 32'h0000_0F3F;",
          "localparam logic [31:0] CTR_VALID_CRF_C = 32'h0000_0F3E;")]),
    "mux_row_removed": ("CRF row dropped from the answer priority chain",
        [("                       : ctr_crf_w ? ctr_crf_blk_w\n", "")]),
    "mux_row_at_n_plus_1": ("CRF row answers index N + 1 instead of N",
        [("                && (32'(ctrq_index_r) == CRF_SNK_IDX_C);",
          "                && (32'(ctrq_index_r) == CRF_SNK_IDX_C + 1);")]),
    "mux_crf_first_for_aaf0": ("CRF row also answers AAF input 0, ahead of the AAF row",
        [("                && (32'(ctrq_index_r) == CRF_SNK_IDX_C);",
          "                && ((32'(ctrq_index_r) == CRF_SNK_IDX_C) || (ctrq_index_r == 16'd0));"),
         ("  assign ctr_ans_raw_w = ctr_sin_w ? ctr_blk_w\n"
          "                       : ctr_crf_w ? ctr_crf_blk_w\n",
          "  assign ctr_ans_raw_w = ctr_crf_w ? ctr_crf_blk_w\n"
          "                       : ctr_sin_w ? ctr_blk_w\n")]),
    "mux_aaf_guard_le_n": ("AAF guard extended to index N (the monitor answers the CRF input)",
        [("                && (ctrq_index_r < 16'(N_STREAMS));",
          "                && (ctrq_index_r <= 16'(N_STREAMS));")]),
}

DIRTY = {
    "dirty_removed": ("CRF dirty source dropped at the arbiter",
        [("    assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w};",
          "    assign pp_ctr_sin_dirty_w = {1'b0, avtprx_dirty_p_w};")]),
    "dirty_also_aaf": ("CRF dirty also raises every AAF input row",
        [("    assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w};",
          "    assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w | {N_STREAMS{crf_dirty_p_w}}};")]),
    "dirty_to_aaf0": ("CRF dirty delivered as AAF input 0 instead of N",
        [("    assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w};",
          "    assign pp_ctr_sin_dirty_w = {1'b0, avtprx_dirty_p_w | {{(N_STREAMS-1){1'b0}}, crf_dirty_p_w}};")]),
    "pend_crf_stuck": ("the CRF row's pending bit is never cleared by its delivery",
        [("      if (pp_ctr_evt_valid_w\n"
          "          && (pp_ctr_evt_type_w == DESC_STREAM_INPUT_C)\n"
          "          && (pp_ctr_evt_index_w == 16'(s))) pp_ctr_sin_pend_n[s] = 1'b0;",
          "      if ((s < N_STREAMS) && pp_ctr_evt_valid_w\n"
          "          && (pp_ctr_evt_type_w == DESC_STREAM_INPUT_C)\n"
          "          && (pp_ctr_evt_index_w == 16'(s))) pp_ctr_sin_pend_n[s] = 1'b0;")]),
    "dirty_free_running": ("CRF dirty ORed with the engine's free-running interval tick",
        [("    assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w};",
          "    assign pp_ctr_sin_dirty_w = {crf_dirty_p_w | crf_rx.iv_tick_r, avtprx_dirty_p_w};")]),
}

TOUT = {
    "tout_half": ("KL_crf_rx given half the fabric clock: a 50 ms silence timeout",
        [("    .CLK_FREQ_HZ_P (MILAN_CLK_FREQ_HZ),\n    .IVAL_CYC_P    (LDIAG_IVAL_CYC_P)\n  ) crf_rx (",
          "    .CLK_FREQ_HZ_P (MILAN_CLK_FREQ_HZ / 2),\n    .IVAL_CYC_P    (LDIAG_IVAL_CYC_P)\n  ) crf_rx (")]),
    "tout_double": ("KL_crf_rx given twice the fabric clock: a 200 ms silence timeout",
        [("    .CLK_FREQ_HZ_P (MILAN_CLK_FREQ_HZ),\n    .IVAL_CYC_P    (LDIAG_IVAL_CYC_P)\n  ) crf_rx (",
          "    .CLK_FREQ_HZ_P (MILAN_CLK_FREQ_HZ * 2),\n    .IVAL_CYC_P    (LDIAG_IVAL_CYC_P)\n  ) crf_rx (")]),
}


def main() -> int:
    src_path, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    src = src_path.read_text()
    out.mkdir(parents=True, exist_ok=True)
    muts: list[tuple[str, str, str, str]] = []
    for i, j in itertools.combinations(range(len(PORTS)), 2):
        mid = f"swap_{PORTS[i][0]}__{PORTS[j][0]}"
        muts.append((mid, "swap",
                     f"crf_rx .{PORTS[i][0]} <-> .{PORTS[j][0]} bindings exchanged",
                     swap(src, i, j)))
    for cls, table in (("mux", MUX), ("dirty", DIRTY), ("tout", TOUT)):
        for mid, (desc, subs) in table.items():
            m = src
            for old, new in subs:
                m = once(m, old, new)
            muts.append((mid, cls, desc, m))
    for k in (7, 9, 3):  # cnt_locked_o, cnt_intr_o, mr_cnt_o
        mid = f"unbind_{PORTS[k][0]}"
        muts.append((mid, "tally", f"crf_rx .{PORTS[k][0]} unbound, {PORTS[k][1]} tied to 0",
                     unbind(src, k)))
    rows = []
    for mid, cls, desc, m in muts:
        if m == src:
            raise SystemExit(f"{mid} is a no-op")
        (out / f"{mid}.sv").write_text(m)
        d = "".join(difflib.unified_diff(src.splitlines(keepends=True), m.splitlines(keepends=True),
                                         "a/hdl/milan/milan_datapath.sv", "b/hdl/milan/milan_datapath.sv"))
        (out / f"{mid}.diff").write_text(d)
        rows.append(f"{mid}\t{cls}\t{desc}\t{hashlib.sha256(m.encode()).hexdigest()}")
    (out / "INDEX.tsv").write_text("id\tclass\tdescription\tsha256\n" + "\n".join(rows) + "\n")
    print(f"{len(rows)} mutants written to {out} from {src_path} "
          f"(sha256 {hashlib.sha256(src.encode()).hexdigest()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
