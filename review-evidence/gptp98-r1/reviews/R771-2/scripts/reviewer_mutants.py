#!/usr/bin/env python3
"""Reviewer-planted parser defects, built against the UNMODIFIED head harness.

usage: reviewer_mutants.py TREE WORKDIR OUTDIR

TREE is an exported FPGA-gPTP tree at the reviewed head. Each mutant edits a
copy of hdl/wire/KL_gptp_rx_parser.sv under WORKDIR (pattern must occur
exactly once), builds tb/verilator/parser/sim_main.cpp against it, and writes
the harness output and its FAIL lines to OUTDIR/<tag>.log. Nothing in TREE is
written. The question each answers: which named checks catch this defect.
"""
from __future__ import annotations

import concurrent.futures as cf
import subprocess
import sys
from pathlib import Path

TREE, WORK, OUT = (Path(a).resolve() for a in sys.argv[1:4])
PARSER = "hdl/wire/KL_gptp_rx_parser.sv"

CUT = ("  assign fu_tlv_cut_after_w = tlv_hdr_run_r &&\n"
       "      (fu_tlv_header_byte_w ? !fu_tlv_header_end_w\n")
LATCH = ("                  if (fu_tlv_header_bad_w) begin\n"
         "                    bad_r <= 1'b1;\n")
MUTANTS = {
    # round 2: the refusal latch of a malformed header deleted
    "latch_deleted": [(LATCH, "                  if (fu_tlv_header_bad_w) begin\n")],
    # a complete header that ends on the last declared octet counts as cut
    "eof_header_counts_as_cut": [(CUT,
        "  assign fu_tlv_cut_after_w = tlv_hdr_run_r &&\n"
        "      (fu_tlv_header_byte_w ? 1'b1\n")],
    # a zero-length TLV after the information TLV refuses the Follow_Up
    "zero_len_after_info_refuses": [(
        "                  end else if (acc_nxt_w[15:0] != 16'd0) begin\n",
        "                  end else if ((acc_nxt_w[15:0] == 16'd0) && fu_found_r) begin\n"
        "                    bad_r <= 1'b1;\n"
        "                  end else if (acc_nxt_w[15:0] != 16'd0) begin\n")],
    # gmTimeBaseIndicator taken two octets late (lastGmPhaseChange's head)
    "w11_two_octets_late": [(
        "  localparam logic [15:0] FU_LEFT_AT_TBI_C = 16'd17;\n",
        "  localparam logic [15:0] FU_LEFT_AT_TBI_C = 16'd15;\n")],
}


def run(tag: str, edits: list[tuple[str, str]]) -> str:
    src = (TREE / PARSER).read_text(encoding="utf-8")
    for pattern, repl in edits:
        if src.count(pattern) != 1:
            return f"{tag}: pattern not unique"
        src = src.replace(pattern, repl)
    d = WORK / tag
    d.mkdir(parents=True, exist_ok=True)
    (d / "KL_gptp_rx_parser.sv").write_text(src, encoding="utf-8")
    par = TREE / "tb/verilator/parser"
    b = subprocess.run(
        ["verilator", "--cc", "--exe", "--build", "-j", "2", "--top-module",
         "KL_gptp_rx_parser", "-Wall", "-Wno-fatal", "-Wno-DECLFILENAME",
         "-Wno-UNUSEDSIGNAL", "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC",
         "-Wno-UNUSEDPARAM", "--Mdir", str(d / "obj"),
         "-CFLAGS", f"-std=c++17 -O2 -I{par} -Wall -Wextra",
         str(TREE / "hdl/ucpu/gptp_ucpu_pkg.sv"), str(d / "KL_gptp_rx_parser.sv"),
         str(par / "sim_main.cpp"), "-o", "Vmut"], capture_output=True, text=True)
    if b.returncode != 0:
        return f"{tag}: build failed\n{b.stderr[-2000:]}"
    r = subprocess.run([str(d / "obj/Vmut")], capture_output=True, text=True)
    text = r.stdout + r.stderr
    (OUT / f"{tag}.log").write_text(text, encoding="utf-8")
    fails = [ln for ln in text.splitlines() if ln.startswith("FAIL ")]
    tally = [ln for ln in text.splitlines() if "checks:" in ln]
    return f"{tag}: rc={r.returncode} {tally[-1] if tally else 'no tally'}\n  " + \
        "\n  ".join(f[:110] for f in fails)


OUT.mkdir(parents=True, exist_ok=True)
with cf.ThreadPoolExecutor(max_workers=len(MUTANTS)) as ex:
    for res in ex.map(lambda kv: run(*kv), MUTANTS.items()):
        print(res)
