#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Write disposable single-edit copies of hdl/milan/milan_datapath.sv.

Each mutant is one or more exact-text replacements, each of which must match
exactly once in the exact-head source, so a mutant can never silently be a
copy of the original. Output: <outdir>/<name>.sv plus a manifest of the edit.

usage: make_mutants.py <exact-head milan_datapath.sv> <outdir>
"""
import hashlib
import pathlib
import sys

PUB = " /* verilator public_flat_rw */"

MUTANTS = {
    # ---- the reviewer's own wiring probes: the KL_crf_rx instance port map
    "mx1_port_swap_mr_tu": [
        (".mr_cnt_o    (crf_mrcnt_w),", ".mr_cnt_o    (crf_tucnt_w),"),
        (".tu_cnt_o    (crf_tucnt_w),", ".tu_cnt_o    (crf_mrcnt_w),"),
    ],
    "mx2_port_swap_locked_unlocked": [
        (".cnt_locked_o   (crf_lockcnt_w),", ".cnt_locked_o   (crf_unlockcnt_w),"),
        (".cnt_unlocked_o (crf_unlockcnt_w),", ".cnt_unlocked_o (crf_lockcnt_w),"),
    ],
    "mx3_port_swap_late_early": [
        (".late_cnt_o  (crf_latecnt_w),", ".late_cnt_o  (crf_earlycnt_w),"),
        (".early_cnt_o (crf_earlycnt_w),", ".early_cnt_o (crf_latecnt_w),"),
    ],
    # control: a swap involving a tally the real-PDU arm drives
    "mx4_port_swap_intr_locked": [
        (".cnt_locked_o   (crf_lockcnt_w),", ".cnt_locked_o   (crf_intrcnt_w),"),
        (".cnt_intr_o     (crf_intrcnt_w),", ".cnt_intr_o     (crf_lockcnt_w),"),
    ],
    # ---- a sample of the author's recorded mutations, re-derived here
    "ma1_mask_fff": [
        ("localparam logic [31:0] CTR_VALID_CRF_C = 32'h0000_0F3F;",
         "localparam logic [31:0] CTR_VALID_CRF_C = 32'h0000_0FFF;"),
    ],
    "ma2_mux_swap_q0_q1": [
        ("6'd0    : ctr_crf_blk_w = crf_lockcnt_w;",
         "6'd0    : ctr_crf_blk_w = crf_unlockcnt_w;"),
        ("6'd1    : ctr_crf_blk_w = crf_unlockcnt_w;",
         "6'd1    : ctr_crf_blk_w = crf_lockcnt_w;"),
    ],
    "ma3_dirty_removed": [
        ("assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w};",
         "assign pp_ctr_sin_dirty_w = {1'b0, avtprx_dirty_p_w};"),
    ],
    "ma4_crf_arm_no_index_first": [
        ("  assign ctr_ans_raw_w = ctr_sin_w ? ctr_blk_w\n"
         "                       : ctr_crf_w ? ctr_crf_blk_w\n",
         "  assign ctr_ans_raw_w = ((ACMP_SINKS_C > N_STREAMS)\n"
         "                          && (ctrq_type_r == DESC_STREAM_INPUT_C)) ? ctr_crf_blk_w\n"
         "                       : ctr_sin_w ? ctr_blk_w\n"),
    ],
    "ma5_q11_16bit_slice": [
        ("6'd11   : ctr_crf_blk_w = crf_pducnt_w;",
         "6'd11   : ctr_crf_blk_w = {16'd0, crf_pducnt_w[15:0]};"),
    ],
    "ma6_aaf_guard_le": [
        ("                && (ctrq_index_r < 16'(N_STREAMS));",
         "                && (ctrq_index_r <= 16'(N_STREAMS));"),
    ],
    # the dropped reader removes flops the harness seeds by name, so this
    # copy marks the seven root wires public (no logic effect), as the
    # author's recipe states
    "ma7_row_removed_public": [
        ("                       : ctr_crf_w ? ctr_crf_blk_w\n", ""),
        ("  wire [31:0] crf_lockcnt_w, crf_unlockcnt_w, crf_intrcnt_w;\n",
         "  wire [31:0] crf_lockcnt_w" + PUB + ";\n"
         "  wire [31:0] crf_unlockcnt_w" + PUB + ";\n"
         "  wire [31:0] crf_intrcnt_w" + PUB + ";\n"),
        ("  wire [31:0] crf_mrcnt_w, crf_tucnt_w, crf_latecnt_w, crf_earlycnt_w;\n",
         "  wire [31:0] crf_mrcnt_w" + PUB + ";\n"
         "  wire [31:0] crf_tucnt_w" + PUB + ";\n"
         "  wire [31:0] crf_latecnt_w" + PUB + ";\n"
         "  wire [31:0] crf_earlycnt_w" + PUB + ";\n"),
    ],
}


def main() -> int:
    src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    out = pathlib.Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    lines = ["# name sha256 edits"]
    for name, edits in MUTANTS.items():
        text = src
        for old, new in edits:
            n = text.count(old)
            if n != 1:
                print(f"{name}: expected exactly one match, found {n}: {old!r}")
                return 1
            text = text.replace(old, new)
        assert text != src
        path = out / f"{name}.sv"
        path.write_text(text, encoding="utf-8")
        digest = hashlib.sha256(text.encode()).hexdigest()
        lines.append(f"{name} {digest} {len(edits)}")
    (out / "MUTANTS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
