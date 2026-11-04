#!/usr/bin/env python3
"""Reviewer probe: extra Follow_Up TLV-walk mutants beyond the repository's arm.

usage: extra_mutants.py <repo-tree> <work-dir> [jobs]

Each mutant edits a copy of hdl/wire/KL_gptp_rx_parser.sv (exact-once
patterns, else reported STALE), then builds and runs
  (a) the repository parser harness tb/verilator/parser/sim_main.cpp, and
  (b) the reviewer's independent random-chain probe fu_walk_diff.cpp.
A mutant is 'caught by the harness' when (a) exits nonzero and prints at
least one FAIL line, and 'caught by the probe' when (b) reports mismatches.
Nothing is written outside <work-dir>.
"""
from __future__ import annotations

import concurrent.futures as cf
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VFLAGS = ["--cc", "--exe", "--build", "-j", "2", "--top-module",
          "KL_gptp_rx_parser", "-Wno-fatal", "-Wno-WIDTHEXPAND",
          "-Wno-WIDTHTRUNC"]

MUTANTS = [
    ("X1 a bad Follow_Up TLV header does not latch the refusal",
     [("                  if (fu_tlv_header_bad_w) begin\n"
       "                    bad_r <= 1'b1;\n",
       "                  if (fu_tlv_header_bad_w) begin\n")]),
    ("X2 fu_found_r not cleared at start of frame",
     [("          fu_found_r <= 1'b0;\n", "")]),
    ("X3 a zero-length header ending at messageLength counts as cut",
     [("      (fu_tlv_header_byte_w ? !fu_tlv_header_end_w\n",
       "      (fu_tlv_header_byte_w ? 1'b1\n")]),
    ("X4 the last declared octet is not walked as a header byte",
     [("  assign fu_tlv_header_byte_w = (mtype_r == MT_FU_C) && tlv_hdr_run_r &&\n"
       "                                (cnt_r <= msg_end_r);\n",
       "  assign fu_tlv_header_byte_w = (mtype_r == MT_FU_C) && tlv_hdr_run_r &&\n"
       "                                (cnt_r < msg_end_r);\n")]),
    ("X5 a value ending exactly at messageLength is refused",
     [("       ({6'd0, cnt_r} + {1'b0, acc_nxt_w[15:0]} > {6'd0, msg_end_r}));\n",
       "       ({6'd0, cnt_r} + {1'b0, acc_nxt_w[15:0]} >= {6'd0, msg_end_r}));\n")]),
    ("X6 word 11 written for a type/length match without the OUI/subtype",
     [("                if (fu_info_r && fu_found_r &&\n"
       "                    (tlv_left_r == FU_LEFT_AT_TBI_C)) begin\n",
       "                if (fu_info_r &&\n"
       "                    (tlv_left_r == FU_LEFT_AT_TBI_C)) begin\n")]),
    ("X7 organizationSubType not compared",
     [("                    (acc_nxt_w[47:0] == FU_TLV_ORG_C)) fu_found_r <= 1'b1;\n",
       "                    (acc_nxt_w[47:24] == FU_TLV_ORG_C[47:24])) fu_found_r <= 1'b1;\n")]),
    ("X8 organizationId not compared",
     [("                    (acc_nxt_w[47:0] == FU_TLV_ORG_C)) fu_found_r <= 1'b1;\n",
       "                    (acc_nxt_w[23:0] == FU_TLV_ORG_C[23:0])) fu_found_r <= 1'b1;\n")]),
    ("X9 the OUI match without the type/length qualification",
     [("                if (fu_info_r && (tlv_left_r == FU_LEFT_AT_SUB_C) &&\n",
       "                if ((tlv_left_r == FU_LEFT_AT_SUB_C) &&\n")]),
    ("X10 the walk starts one octet late",
     [("              if (cnt_r == 11'(OFF_TS_NS_END_C)) begin\n"
       "                tlv_hdr_run_r <= 1'b1;\n",
       "              if (cnt_r == 11'(OFF_TS_NS_END_C + 1)) begin\n"
       "                tlv_hdr_run_r <= 1'b1;\n")]),
    ("X11 the walk stops after the first TLV value",
     [("                if (tlv_left_r == 16'd1) tlv_hdr_run_r <= 1'b1;\n", "")]),
    ("X12 the gmTimeBaseIndicator offset one octet early",
     [("  localparam logic [15:0] FU_LEFT_AT_TBI_C = 16'd17;\n",
       "  localparam logic [15:0] FU_LEFT_AT_TBI_C = 16'd18;\n")]),
    ("X13 a cut header after padding is not refused (padded branch lost)",
     [("                            : (tlv_hdr_pos_r != 2'd0));\n",
       "                            : 1'b0);\n")]),
    ("X14 the odd test reads lengthField bit 1",
     [("      (acc_nxt_w[0] ||\n       ({6'd0, cnt_r} + {1'b0, acc_nxt_w[15:0]} > {6'd0, msg_end_r}));\n",
       "      (acc_nxt_w[1] ||\n       ({6'd0, cnt_r} + {1'b0, acc_nxt_w[15:0]} > {6'd0, msg_end_r}));\n")]),
    ("X15 messageLength minimum for Follow_Up lowered to the header+body",
     [("      MT_FU_C:     min_end_w = 11'(OFF_FU_END_C);\n",
       "      MT_FU_C:     min_end_w = 11'(OFF_TS_NS_END_C);\n")]),
]


def stage(tree: Path, work: Path, tag: str, edits) -> tuple[Path | None, str]:
    src = (tree / "hdl/wire/KL_gptp_rx_parser.sv").read_text(encoding="utf-8")
    for pat, _ in edits:
        if src.count(pat) != 1:
            return None, f"STALE pattern (count {src.count(pat)}): {pat[:60]!r}"
    for pat, rep in edits:
        src = src.replace(pat, rep)
    d = work / tag / "hdl"
    (d / "wire").mkdir(parents=True, exist_ok=True)
    (d / "ucpu").mkdir(parents=True, exist_ok=True)
    shutil.copy(tree / "hdl/ucpu/gptp_ucpu_pkg.sv", d / "ucpu")
    (d / "wire/KL_gptp_rx_parser.sv").write_text(src, encoding="utf-8")
    return d, ""


def build(hdl: Path, cpp: Path, inc: Path, mdir: Path, exe: str) -> Path | None:
    out = subprocess.run(
        ["verilator", *VFLAGS, "--Mdir", str(mdir),
         "-CFLAGS", f"-std=c++17 -O2 -I{inc}",
         str(hdl / "ucpu/gptp_ucpu_pkg.sv"), str(hdl / "wire/KL_gptp_rx_parser.sv"),
         str(cpp), "-o", exe], capture_output=True, text=True)
    p = mdir / exe
    return p if out.returncode == 0 and p.is_file() else None


def one(tree: Path, work: Path, name: str, edits) -> str:
    tag = name.split()[0]
    hdl, err = stage(tree, work, tag, edits)
    if hdl is None:
        return f"{name}: {err}"
    harness = tree / "tb/verilator/parser"
    a = build(hdl, harness / "sim_main.cpp", harness, work / tag / "obj_h", "Vh")
    b = build(hdl, HERE / "fu_walk_diff.cpp", HERE, work / tag / "obj_p", "Vp")
    if a is None or b is None:
        return f"{name}: BUILD FAILED"
    ra = subprocess.run([str(a)], capture_output=True, text=True)
    fails = [l for l in ra.stdout.splitlines() if l.startswith("FAIL ")]
    tally = [l for l in ra.stdout.splitlines() if " checks: " in l]
    rb = subprocess.run([str(b), "100000"], capture_output=True, text=True)
    res = [l for l in rb.stdout.splitlines() if l.startswith("RESULT")]
    h = "CAUGHT" if (ra.returncode != 0 and fails) else "SURVIVED"
    p = "CAUGHT" if rb.returncode != 0 else "SURVIVED"
    first = fails[0] if fails else "-"
    return (f"{name}\n  harness: {h} rc={ra.returncode} {tally[-1] if tally else ''}"
            f" first: {first}\n  probe:   {p} {res[-1] if res else ''}")


def main() -> int:
    tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    work.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = [ex.submit(one, tree, work, n, e) for n, e in MUTANTS]
        for f in futs:
            print(f.result(), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
