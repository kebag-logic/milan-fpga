#!/usr/bin/env python3
"""Mutation receipts for #529: each mutant removes or bends one piece of the
new root wiring, is built through the milan_dp recipe (DP_SRC override) and
run; the receipt records which checks went red."""
import pathlib
import re
import subprocess
import sys

LANE = pathlib.Path("$LANES/529-crf-input-counters")
PKT = pathlib.Path("$REVIEWS/529-a204-packet")
DP = LANE / "hdl/milan/milan_datapath.sv"
TBDIR = LANE / "tb/verilator/milan_dp"

#: A mutant that removes the only reader of a tally lets the simulator drop
#: that flop, and the harness then no longer compiles (it seeds the tallies
#: by name). These mutants also mark the seven tally wires visible - a
#: simulator pragma with no logic effect - so the red is behavioural.
KEEP = [(
    "  wire [31:0] crf_lockcnt_w, crf_unlockcnt_w, crf_intrcnt_w;\n"
    "  wire [31:0] crf_mrcnt_w, crf_tucnt_w, crf_latecnt_w, crf_earlycnt_w;\n",
    "".join(f"  wire [31:0] {n} /* verilator public_flat_rw */;\n" for n in (
        "crf_lockcnt_w", "crf_unlockcnt_w", "crf_intrcnt_w", "crf_mrcnt_w",
        "crf_tucnt_w", "crf_latecnt_w", "crf_earlycnt_w")))]

MUTANTS = {
    # M1: the CRF row is not on the gather face at all (the pre-#529 shape)
    "M1_row_removed": KEEP + [(
        "                       : ctr_crf_w ? ctr_crf_blk_w\n", "")],
    # M2: two quadlets of the bank permuted (MEDIA_LOCKED <-> MEDIA_UNLOCKED)
    "M2_ml_mu_swapped": [
        ("6'd0    : ctr_crf_blk_w = crf_lockcnt_w;",
         "6'd0    : ctr_crf_blk_w = crf_unlockcnt_w;"),
        ("6'd1    : ctr_crf_blk_w = crf_unlockcnt_w;",
         "6'd1    : ctr_crf_blk_w = crf_lockcnt_w;")],
    # M3: FRAMES_RX served through the CSR's 16-bit slice
    "M3_frx_16bit": [(
        "6'd11   : ctr_crf_blk_w = crf_pducnt_w;",
        "6'd11   : ctr_crf_blk_w = {16'd0, crf_pducnt_w[15:0]};")],
    # M4: the mask claims the two tv tallies nothing keeps
    "M4_mask_0xFFF": [(
        "CTR_VALID_CRF_C = 32'h0000_0F3F;", "CTR_VALID_CRF_C = 32'h0000_0FFF;")],
    # M5: the CRF dirty source is not delivered to the arbiter
    "M5_dirty_removed": [(
        "assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w};",
        "assign pp_ctr_sin_dirty_w = {1'b0, avtprx_dirty_p_w};")],
    # M6: the CRF row loses its index qualifier and outranks the AAF rows
    "M6_crf_answers_every_input": [
        ("                && (32'(ctrq_index_r) == CRF_SNK_IDX_C);", ";"),
        ("  assign ctr_ans_raw_w = ctr_sin_w ? ctr_blk_w\n"
         "                       : ctr_crf_w ? ctr_crf_blk_w\n",
         "  assign ctr_ans_raw_w = ctr_crf_w ? ctr_crf_blk_w\n"
         "                       : ctr_sin_w ? ctr_blk_w\n")],
    # M7: the AAF guard admits index N, so the monitor's clamp answers for
    # the CRF input with sink 0's numbers
    "M7_aaf_guard_admits_crf": [(
        "&& (ctrq_index_r < 16'(N_STREAMS));",
        "&& (ctrq_index_r <= 16'(N_STREAMS));")],
    # M8: one tally's wire removed from the row (STREAM_INTERRUPTED)
    "M8_si_unwired": KEEP + [(
        "6'd2    : ctr_crf_blk_w = crf_intrcnt_w;",
        "6'd2    : ctr_crf_blk_w = 32'd0;")],
}

LEGS = {"M5_dirty_removed": ["nxn", "notify"], "M1_row_removed": ["nxn", "notify"]}


def make_mutant(name, edits):
    src = DP.read_text(encoding="utf-8")
    for old, new in edits:
        n = src.count(old)
        if n != 1:
            sys.exit(f"{name}: anchor found {n} times: {old!r}")
        src = src.replace(old, new)
    out = PKT / "mutants" / f"{name}.sv"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(src, encoding="utf-8")
    return out


def run_leg(name, leg, mut):
    mdir = PKT / "obj" / f"mut_{name}_{leg}"
    b = subprocess.run([str(PKT / "leg.sh"), leg, str(mdir), str(mut)],
                       capture_output=True, text=True)
    if b.returncode != 0:
        return f"BUILD FAILED rc={b.returncode}", []
    binary = next(mdir.glob("Vmilan_dp_*"))
    r = subprocess.run([str(binary)], cwd=TBDIR, capture_output=True, text=True)
    (PKT / "logs" / f"mut_{name}_{leg}.txt").write_text(r.stdout + r.stderr)
    fails = [ln.strip() for ln in r.stdout.splitlines() if "[FAIL]" in ln]
    tally = re.search(r"checks: (\d+)\s+failures: (\d+)", r.stdout)
    return (f"rc={r.returncode} {tally.group(0) if tally else 'no tally'}", fails)


def main():
    only = sys.argv[1:]
    lines = []
    for name, edits in MUTANTS.items():
        if only and name not in only:
            continue
        mut = make_mutant(name, edits)
        for leg in LEGS.get(name, ["nxn"]):
            verdict, fails = run_leg(name, leg, mut)
            lines.append(f"== {name} [{leg}] {verdict}")
            lines.extend(f"   {f}" for f in fails)
            print(lines[-1 - len(fails)], flush=True)
    (PKT / "mutation_receipt.txt").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
