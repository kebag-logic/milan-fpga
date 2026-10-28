#!/usr/bin/env python3
"""Reviewer-owned disposable fault probes for FPGA-gPTP PR #93 (#87, #88).

Usage: reviewer_probes.py <tree> <suite: parser|engine> <probe-name|all> [build_jobs]

Each probe plants edits into one source file of a staged copy of <tree>,
using that suite's own mutants.py stage/build/run code (imported unchanged),
and reports the harness tally and every FAIL line. A probe whose run prints
zero FAIL lines SURVIVED. Nothing is written into <tree>.
"""
import sys
import tempfile
import importlib.util
from pathlib import Path

P = "wire/KL_gptp_rx_parser.sv"
E = "top/KL_gptp_engine.sv"
G = "ucode/gen_gptp_ucode.py"

HDR_OLD = "        (ann_tlv_len_w[2:0] || pt_seen_r)));\n"
STEPS_CAP = ("  logic [15:0] rv_steps_r;\n"
             "  always_ff @(posedge clk_i)\n"
             "    if (rx_valid_i && (cnt_r == 11'd76)) rv_steps_r <= acc_nxt_w[15:0];\n")
HDR_HEAD = "  assign ann_tlv_header_bad_w = ann_tlv_header_end_w &&\n"


def count_rule(op: str):
    return [(HDR_HEAD, STEPS_CAP + HDR_HEAD),
            (HDR_OLD, "        (ann_tlv_len_w[2:0] || pt_seen_r ||\n"
                      f"         ({{1'b0, ann_tlv_len_w[15:3]}} {op} "
                      "({1'b0, rv_steps_r} + 17'd1)))));\n")]


PROBES = {
    # count refusal restored only for paths LONGER than stepsRemoved+1
    "count refusal, longer only": ("both", P, count_rule(">")),
    # count refusal restored only for paths SHORTER than stepsRemoved+1
    "count refusal, shorter only": ("both", P, count_rule("<")),
    # any zero-length TLV (not only PATH_TRACE) marks presence; the duplicate
    # rule is left untouched, presence is reported through a separate flag
    "zero-length unknown TLV marks presence": ("both", P, [
        ("  logic        pt_self_r;\n",
         "  logic        pt_self_r;\n  logic        rv_z_r;\n"),
        ("          pt_seen_r <= 1'b0;\n          pt_self_r <= 1'b0;\n",
         "          pt_seen_r <= 1'b0;\n          pt_self_r <= 1'b0;\n"
         "          rv_z_r <= 1'b0;\n"),
        ("                    if (ann_tlv_type_w == 16'h0008) pt_seen_r <= 1'b1;\n",
         "                    if (ann_tlv_type_w == 16'h0008) pt_seen_r <= 1'b1;\n"
         "                    rv_z_r <= 1'b1;\n"),
        ("            bank_wdata_o <= {pt_seen_r, 54'd0, pt_self_r, pt_cnt_r};\n",
         "            bank_wdata_o <= {pt_seen_r | rv_z_r, 54'd0, pt_self_r, pt_cnt_r};\n"),
    ]),
    # the singular-PathTrace rule removed (duplicate accepted)
    "duplicate PathTrace accepted": ("both", P, [
        (HDR_OLD, "        (ann_tlv_len_w[2:0])));\n")]),
    # presence latched sticky in the engine's frozen Announce context
    "engine presence sticky": ("engine", E, [
        ("            ann_pub_present_r <= bank_wdata_w[63];\n",
         "            ann_pub_present_r <= ann_pub_present_r | bank_wdata_w[63];\n")]),
    # entry 0 (w16) no longer captured into the frozen context
    "engine head not captured": ("engine", E, [
        ("          if ((bank_addr_w >= 5'd16) && (bank_addr_w <= 5'd23))\n",
         "          if ((bank_addr_w >= 5'd17) && (bank_addr_w <= 5'd23))\n")]),
    # without a TLV the entries are kept but the count is still rewritten
    "engine TLV-less rewrites count only": ("engine", E, [
        ("                if (ann_pub_present_r) begin\n"
         "                  pub_path_count_r <= path_trace_count_w;\n",
         "                pub_path_count_r <= path_trace_count_w;\n"
         "                if (ann_pub_present_r) begin\n")]),
    # thisClock appended even after eight received entries (count 9)
    "engine append past eight": ("engine", E, [
        ("  wire       path_append_w = (ann_pub_count_clamped_w != 4'd8);\n",
         "  wire       path_append_w = 1'b1;\n")]),
    # self-master (address 6) keeps the stale entries under count 1
    "engine address 6 keeps entries": ("engine", E, [
        ("                  pub_path_count_r <= 4'd1;\n"
         "                  pub_path_r       <= self_path_w;\n"
         "                end\n",
         "                  pub_path_count_r <= 4'd1;\n"
         "                end\n")]),
    # (b) boundary moved: stepsRemoved 255 qualifies
    "ucode (b) off by one": ("engine", G, [
        ("STEPS_MAX_C = 255 ", "STEPS_MAX_C = 256 ")]),
}


def load(tree: Path, suite: str):
    path = tree / f"tb/verilator/{suite}/mutants.py"
    spec = importlib.util.spec_from_file_location(f"{suite}_mut", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run_one(tree: Path, suite: str, name: str, fname: str, edits, work: Path, jobs: str) -> int:
    m = load(tree, suite)
    if "-j" in m.VFLAGS:
        m.VFLAGS[m.VFLAGS.index("-j") + 1] = jobs
    src = (m.HDL / fname).read_text(encoding="utf-8")
    for pat, _ in edits:
        n = src.count(pat)
        if n != 1:
            print(f"[PROBE-ERROR] {suite} / {name}: pattern appears {n} times")
            return 2
    tag = "".join(c if c.isalnum() else "_" for c in f"{suite}_{name}")
    if suite == "parser":
        if fname != P:
            print(f"[PROBE-SKIP] {name}: parser suite builds only the parser")
            return 0
        srcdir = m.stage(work, tag, edits)
        exe = m.build(srcdir, work, tag)
        if exe is None:
            print(f"[PROBE-ERROR] {suite} / {name}: build failed")
            return 2
        rc, out = m.run_harness(exe)
    else:
        srcdir = m.stage(work, tag, (fname, edits))
        rundir = work / f"run_{tag}"
        if not m.generate_image(srcdir, rundir):
            print(f"[PROBE-ERROR] {suite} / {name}: generator refused")
            return 2
        exe = m.build(srcdir, work, tag)
        if exe is None:
            print(f"[PROBE-ERROR] {suite} / {name}: build failed")
            return 2
        rc, out = m.run_harness(exe, rundir)
    fails = [l for l in out.splitlines() if l.startswith("FAIL")]
    tally = [l for l in out.splitlines() if " checks: " in l]
    verdict = "CAUGHT" if fails else "SURVIVED"
    print(f"[PROBE] {suite} / {name}: {verdict}; rc {rc}; "
          f"{tally[-1] if tally else 'no tally'}; {len(fails)} FAIL lines")
    for l in fails[:40]:
        print("    " + l)
    if len(fails) > 40:
        print(f"    ... {len(fails) - 40} more")
    other = [l for l in out.splitlines() if "%Error" in l or "Assertion" in l][:5]
    for l in other:
        print("    [sim] " + l)
    sys.stdout.flush()
    return 0


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    suite, which = sys.argv[2], sys.argv[3]
    jobs = sys.argv[4] if len(sys.argv) > 4 else "2"
    rc = 0
    with tempfile.TemporaryDirectory(prefix=f"probe-{suite}-") as td:
        for name, (suites, fname, edits) in PROBES.items():
            if which != "all" and which != name:
                continue
            if suites not in ("both", suite):
                continue
            if suite == "parser" and fname != P:
                continue
            rc |= run_one(tree, suite, name, fname, edits, Path(td), jobs)
    return rc


if __name__ == "__main__":
    sys.exit(main())
