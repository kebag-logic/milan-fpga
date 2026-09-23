#!/usr/bin/env python3
"""Reviewer mutation probes for PR #534 (issue #529).

Each mutant is ONE exact-text edit applied to a COPY of
hdl/milan/milan_datapath.sv (every anchor must match exactly once, or the
mutant is refused). The copy is elaborated through the milan_dp suite's own
recipe (legs.mk, included after the suite Makefile, DP_SRC=<copy>) and the
named legs are run. Nothing in the checkout under test is written except
disposable obj_m_* build directories inside the checkout's milan_dp suite.

Usage:
  mutants.py --repo <checkout> --out <dir> [--legs nxn,notify] [ids...]

The positive control "ctl_marked" applies only the public_flat_rw marking
used by every mutant, so each mutant differs from a passing control by its
one edit.
"""
import argparse
import os
import re
import subprocess
import sys

MARK_FROM = ("  wire [31:0] crf_lockcnt_w, crf_unlockcnt_w, crf_intrcnt_w;\n"
             "  wire [31:0] crf_mrcnt_w, crf_tucnt_w, crf_latecnt_w, crf_earlycnt_w;\n")
MARK_TO = "".join(
    f"  wire [31:0] {n} /* verilator public_flat_rw */;\n"
    for n in ("crf_lockcnt_w", "crf_unlockcnt_w", "crf_intrcnt_w",
              "crf_mrcnt_w", "crf_tucnt_w", "crf_latecnt_w", "crf_earlycnt_w"))

# id -> (description, [(old, new), ...])
MUTANTS = {
    "ctl_marked": ("positive control: public_flat_rw marking only", []),
    # --- the author's published table, reproduced independently ---
    "a1_row_removed": ("drop the CRF arm from ctr_ans_raw_w", [
        ("                       : ctr_crf_w ? ctr_crf_blk_w\n", "")]),
    "a2_q0_q1_swap": ("swap quadlet 0 / 1 sources", [
        ("6'd0    : ctr_crf_blk_w = crf_lockcnt_w;",
         "6'd0    : ctr_crf_blk_w = crf_unlockcnt_w;"),
        ("6'd1    : ctr_crf_blk_w = crf_unlockcnt_w;",
         "6'd1    : ctr_crf_blk_w = crf_lockcnt_w;")]),
    "a3_q11_16bit": ("quadlet 11 served through a 16-bit slice", [
        ("6'd11   : ctr_crf_blk_w = crf_pducnt_w;",
         "6'd11   : ctr_crf_blk_w = {16'd0, crf_pducnt_w[15:0]};")]),
    "a4_mask_fff": ("CTR_VALID_CRF_C claims the tv pair (0xFFF)", [
        ("CTR_VALID_CRF_C = 32'h0000_0F3F;", "CTR_VALID_CRF_C = 32'h0000_0FFF;")]),
    "a5_dirty_removed": ("CRF dirty source tied off at the arbiter", [
        ("assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w};",
         "assign pp_ctr_sin_dirty_w = {1'b0, avtprx_dirty_p_w};")]),
    "a6_crf_answers_aaf": ("CRF arm without its index term, ahead of the AAF arm", [
        ("                && (32'(ctrq_index_r) == CRF_SNK_IDX_C);\n", ";\n"),
        ("  assign ctr_ans_raw_w = ctr_sin_w ? ctr_blk_w\n"
         "                       : ctr_crf_w ? ctr_crf_blk_w\n",
         "  assign ctr_ans_raw_w = ctr_crf_w ? ctr_crf_blk_w\n"
         "                       : ctr_sin_w ? ctr_blk_w\n")]),
    "a7_aaf_guard_le": ("AAF guard admits index N_STREAMS", [
        ("&& (ctrq_index_r < 16'(N_STREAMS));", "&& (ctrq_index_r <= 16'(N_STREAMS));")]),
    "a8_q2_zero": ("quadlet 2 tied to zero", [
        ("6'd2    : ctr_crf_blk_w = crf_intrcnt_w;",
         "6'd2    : ctr_crf_blk_w = 32'd0;")]),
    # --- reviewer-chosen mutants ---
    "r1_index_ge": ("CRF row answers for every index >= N_STREAMS", [
        ("&& (32'(ctrq_index_r) == CRF_SNK_IDX_C);",
         "&& (32'(ctrq_index_r) >= CRF_SNK_IDX_C);")]),
    "r2_sout_offset": ("arbiter types STREAM_OUTPUT indices from the old base", [
        ("pp_ctr_evt_index_w = 16'(pick - PP_CTR_SIN_N_C);",
         "pp_ctr_evt_index_w = 16'(pick - N_STREAMS);")]),
    "r3_crf_pend_stuck": ("pending-clear loop stops below the CRF row", [
        ("for (int unsigned s = 0; s < PP_CTR_SIN_N_C; s++) begin",
         "for (int unsigned s = 0; s < N_STREAMS; s++) begin")]),
    "r4_type_dropped": ("CRF row guard ignores descriptor_type", [
        ("                && (ctrq_type_r == DESC_STREAM_INPUT_C)\n"
         "                && (32'(ctrq_index_r) == CRF_SNK_IDX_C);",
         "                && (32'(ctrq_index_r) == CRF_SNK_IDX_C);")]),
    "r5_dirty_order": ("CRF dirty bit concatenated on the wrong end", [
        ("assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w};",
         "assign pp_ctr_sin_dirty_w = {avtprx_dirty_p_w, crf_dirty_p_w};")]),
    "r6_rr_sout_old": ("round-robin resume point after a STREAM_OUTPUT uses the old base", [
        ("pp_ctr_rr_r <= PP_CTR_RR_W_C'(PP_CTR_SIN_N_C\n"
         "                                        + 32'(pp_ctr_evt_index_w) + 1);",
         "pp_ctr_rr_r <= PP_CTR_RR_W_C'(N_STREAMS\n"
         "                                        + 32'(pp_ctr_evt_index_w) + 1);")]),
    "r7_pick_sin_old": ("arbiter types the CRF pick as a STREAM_OUTPUT", [
        ("        if (pick < PP_CTR_SIN_N_C) begin",
         "        if (pick < N_STREAMS) begin")]),
    # port-binding permutations at the KL_crf_rx instance: the quadlet mux
    # is untouched, only which engine output drives which named root wire
    "p1_bind_lock_unlock": ("KL_crf_rx port map: lock/unlock tallies swapped", [
        (".cnt_locked_o   (crf_lockcnt_w),", ".cnt_locked_o   (crf_unlockcnt_w),"),
        (".cnt_unlocked_o (crf_unlockcnt_w),", ".cnt_unlocked_o (crf_lockcnt_w),")]),
    "p2_bind_late_early": ("KL_crf_rx port map: late/early tallies swapped", [
        (".late_cnt_o  (crf_latecnt_w),", ".late_cnt_o  (crf_earlycnt_w),"),
        (".early_cnt_o (crf_earlycnt_w),", ".early_cnt_o (crf_latecnt_w),")]),
    "p3_bind_mr_tu": ("KL_crf_rx port map: mr/tu tallies swapped", [
        (".mr_cnt_o    (crf_mrcnt_w),", ".mr_cnt_o    (crf_tucnt_w),"),
        (".tu_cnt_o    (crf_tucnt_w),", ".tu_cnt_o    (crf_mrcnt_w),")]),
    "p5_bind_fmt_late": ("KL_crf_rx port map: format-error/late tallies swapped", [
        (".fmt_err_o   (crf_fmterr_w),", ".fmt_err_o   (crf_latecnt_w),"),
        (".late_cnt_o  (crf_latecnt_w),", ".late_cnt_o  (crf_fmterr_w),")]),
    "p4_bind_intr_lock": ("KL_crf_rx port map: intr/lock tallies swapped", [
        (".cnt_locked_o   (crf_lockcnt_w),", ".cnt_locked_o   (crf_intrcnt_w),"),
        (".cnt_intr_o     (crf_intrcnt_w),", ".cnt_intr_o     (crf_lockcnt_w),")]),
}

LEG_BIN = {"nxn": "Vmilan_dp_nxn", "notify": "Vmilan_dp_notify",
           "nxn8": "Vmilan_dp_nxn8", "nxndv": "Vmilan_dp_nxndv",
           "nxn4c": "Vmilan_dp_nxn4c"}


def make_copy(src_text, edits):
    t = src_text
    if t.count(MARK_FROM) != 1:
        raise SystemExit("marking anchor not unique")
    t = t.replace(MARK_FROM, MARK_TO)
    for old, new in edits:
        n = t.count(old)
        if n != 1:
            raise SystemExit(f"anchor matched {n} times: {old!r}")
        t = t.replace(old, new)
    return t


def run(cmd, cwd, log):
    with open(log, "w") as fh:
        p = subprocess.run(cmd, cwd=cwd, stdout=fh, stderr=subprocess.STDOUT)
    return p.returncode


def summarize(log):
    txt = open(log, errors="replace").read()
    fails = re.findall(r"^\s*\[FAIL\] (.*)$", txt, re.M)
    m = re.search(r"checks:\s*(\d+)\s+failures:\s*(\d+)", txt)
    tags = {}
    for f in fails:
        t = re.match(r"(\[[A-Z0-9-]+\])", f)
        k = t.group(1) if t else "(untagged)"
        tags[k] = tags.get(k, 0) + 1
    return (m.group(1) if m else "?", m.group(2) if m else "?", tags, fails)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--legs", default="nxn,notify")
    ap.add_argument("--jobs", default="8")
    ap.add_argument("ids", nargs="*")
    a = ap.parse_args()
    suite = os.path.join(a.repo, "tb/verilator/milan_dp")
    legsmk = os.path.join(os.path.dirname(os.path.abspath(__file__)), "legs.mk")
    src = open(os.path.join(a.repo, "hdl/milan/milan_datapath.sv")).read()
    ids = a.ids or list(MUTANTS)
    os.makedirs(a.out, exist_ok=True)
    for mid in ids:
        desc, edits = MUTANTS[mid]
        d = os.path.join(a.out, mid)
        os.makedirs(d, exist_ok=True)
        cp = os.path.join(d, "milan_datapath.sv")
        with open(cp, "w") as fh:
            fh.write(make_copy(src, edits))
        with open(os.path.join(d, "mutant.diff"), "w") as fh:
            subprocess.run(["diff", "-u",
                            os.path.join(a.repo, "hdl/milan/milan_datapath.sv"),
                            cp], stdout=fh)
        for leg in a.legs.split(","):
            mdir = f"obj_m_{mid}_{leg}"
            blog = os.path.join(d, f"build_{leg}.log")
            rlog = os.path.join(d, f"run_{leg}.log")
            rc = run(["make", "-f", "Makefile", "-f", legsmk, f"r_{leg}",
                      f"DP_SRC={cp}", f"R_MDIR={mdir}",
                      f"VERILATOR_JOBS={a.jobs}"], suite, blog)
            if rc != 0:
                print(f"{mid:22s} {leg:6s} BUILD-FAILED rc={rc} ({desc})",
                      flush=True)
                continue
            rrc = run([f"./{mdir}/{LEG_BIN[leg]}"], suite, rlog)
            checks, nf, tags, fails = summarize(rlog)
            tagtxt = " ".join(f"{k}x{v}" for k, v in sorted(tags.items()))
            print(f"{mid:22s} {leg:6s} rc={rrc} checks={checks} "
                  f"failures={nf} {tagtxt} ({desc})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
