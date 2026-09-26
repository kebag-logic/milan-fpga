#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned mutants for the processor's aecp_name_wr_o export.

Each mutant is applied to a private copy of hdl/, tb/common and tb/pp_top
taken from --src (an exported tree at the reviewed head), built with the
Verilator found first on PATH, and run with --name-writes-only.
A mutant counts as KILLED only if it builds, the simulation completes
(the "NW:" and "[build default," lines are present), the run exits
non-zero and at least one FAIL line is printed. A build failure is
reported as INVALID, never as a kill.

Usage: r335_name_wr_mutants.py --src <tree> --work <dir> --out <dir>
                               [--only NAME ...] [--jobs N]
"""

import argparse
import concurrent.futures as cf
import json
import shutil
import subprocess
from pathlib import Path

STORE = "hdl/aecp/KL_aecp_desc_store.sv"
ENGINE = "hdl/aecp/KL_aecp_engine.sv"
TOP = "hdl/top/protocol_processor_top.sv"

EXPORT = "  assign name_wr_o = take_wr_w && st_name_i;"
RAM_EN = "      name_we_w    = name_wr_o;"
# every store-side export mutant keeps the name RAM on its original enable,
# so only the exported wire differs from the reviewed head
RAM_EN_ORIG = "      name_we_w    = take_wr_w && st_name_i;"
ENG_CONN = "      .name_wr_o         (name_wr_o),"
ENG_ANCHOR = "  logic [15:0] store_fetch_nc_w, store_rowr_nc_w, store_dlen_nc_w;"
TOP_CONN = "      .name_wr_o          (aecp_name_wr_o),"
TOP_ANCHOR = "  assign dbg_now_ms_o"


def store_export(expr_or_block):
    """Replace the store export with a new body; RAM enable stays original."""
    return [(STORE, EXPORT, expr_or_block), (STORE, RAM_EN, RAM_EN_ORIG)]


MUTANTS = {
    # SET_NAME command decode at the µCPU dispatch (one pulse per command)
    "decode_dispatch": [
        (ENGINE, ENG_CONN, "      .name_wr_o         (),"),
        (ENGINE, ENG_ANCHOR, ENG_ANCHOR +
         "\n  assign name_wr_o = disp_valid_r && disp_ready_w"
         " && (upc_r == UPC_SNAME_C);"),
    ],
    # NAME_WR instruction decode: request instead of acceptance (no ready)
    "decode_request": store_export(
        "  assign name_wr_o = st_req_i && st_we_i && st_name_i;"),
    # level: sticky after the first accepted write until reset
    "level_sticky": store_export(
        "  logic mut_lvl_r;\n"
        "  always_ff @(posedge clk_i or negedge rst_n)\n"
        "    if (!rst_n) mut_lvl_r <= 1'b0;\n"
        "    else if (take_wr_w && st_name_i) mut_lvl_r <= 1'b1;\n"
        "  assign name_wr_o = (take_wr_w && st_name_i) || mut_lvl_r;"),
    # pulse stretched to two cycles
    "stretch2": store_export(
        "  logic mut_d_r;\n"
        "  always_ff @(posedge clk_i or negedge rst_n)\n"
        "    if (!rst_n) mut_d_r <= 1'b0;\n"
        "    else mut_d_r <= take_wr_w && st_name_i;\n"
        "  assign name_wr_o = (take_wr_w && st_name_i) || mut_d_r;"),
    # registered: one cycle after the accepting edge
    "delayed1": store_export(
        "  logic mut_d_r;\n"
        "  always_ff @(posedge clk_i or negedge rst_n)\n"
        "    if (!rst_n) mut_d_r <= 1'b0;\n"
        "    else mut_d_r <= take_wr_w && st_name_i;\n"
        "  assign name_wr_o = mut_d_r;"),
    # a multi-lane name misses one middle beat (lane 3)
    "drop_lane3": store_export(
        "  assign name_wr_o = take_wr_w && st_name_i"
        " && (st_addr_i[5:3] != 3'd3);"),
    # a multi-lane name misses its last beat (lane 7)
    "drop_lane7": store_export(
        "  assign name_wr_o = take_wr_w && st_name_i"
        " && (st_addr_i[5:3] != 3'd7);"),
    # only the first accepted lane of a command pulses
    "first_lane_only": store_export(
        "  logic mut_seen_r;\n"
        "  always_ff @(posedge clk_i or negedge rst_n)\n"
        "    if (!rst_n) mut_seen_r <= 1'b0;\n"
        "    else if (take_wr_w && st_name_i) mut_seen_r <= 1'b1;\n"
        "    else if (st_req_i && !st_we_i && !st_name_i) mut_seen_r <= 1'b0;\n"
        "  assign name_wr_o = take_wr_w && st_name_i && !mut_seen_r;"),
    # includes the boot walk's name-table loading
    "with_boot": [(STORE, EXPORT, "  assign name_wr_o = name_we_w;"),
                  (STORE, RAM_EN, RAM_EN_ORIG)],
    # any accepted store write, not only the name lane
    "any_store_write": store_export("  assign name_wr_o = take_wr_w;"),
    # accepted name reads counted too
    "with_name_reads": store_export(
        "  assign name_wr_o = (take_wr_w || take_rd_w) && st_name_i;"),
    # the later group-7 completion mark instead of the live write
    "from_nvm_mark7": [
        (TOP, TOP_CONN, "      .name_wr_o          (),"),
        (TOP, TOP_ANCHOR, "  assign aecp_name_wr_o = aecp_nvm_stb_o"
         " && (aecp_nvm_mark_o == 8'd7);\n" + TOP_ANCHOR),
    ],
    # export tied off at the top
    "top_tied0": [
        (TOP, TOP_CONN, "      .name_wr_o          (),"),
        (TOP, TOP_ANCHOR, "  assign aecp_name_wr_o = 1'b0;\n" + TOP_ANCHOR),
    ],
}


def run(cmd, cwd, log):
    with log.open("w") as fh:
        return subprocess.run(cmd, cwd=cwd, stdout=fh,
                              stderr=subprocess.STDOUT, check=False).returncode


def one(name, src, work, out):
    tree = work / name
    if tree.exists():
        shutil.rmtree(tree)
    for d in ("hdl", "tb/common", "tb/pp_top"):
        shutil.copytree(src / d, tree / d, ignore=shutil.ignore_patterns(
            "obj*", "*.hex", "__pycache__"))
    for path, old, new in MUTANTS.get(name, []):
        f = tree / path
        text = f.read_text()
        n = text.count(old)
        if n != 1:
            return dict(mutant=name, verdict="INVALID",
                        reason=f"anchor count {n} in {path}: {old!r}")
        f.write_text(text.replace(old, new))
    bench = tree / "tb/pp_top"
    brc = run(["make", "gsi-build"], bench, out / f"{name}-build.log")
    if brc:
        return dict(mutant=name, verdict="INVALID", build_rc=brc)
    log = out / f"{name}-run.log"
    rrc = run(["./obj_dir/Vpp_top_sim", "--name-writes-only"], bench, log)
    text = log.read_text()
    fails = [ln for ln in text.splitlines() if ln.startswith("FAIL")]
    complete = "NW:" in text and "[build default," in text
    if name == "golden":
        verdict = "PASS" if (complete and rrc == 0 and not fails) else "BROKEN"
    elif not complete:
        verdict = "INCOMPLETE"
    elif rrc != 0 and fails:
        verdict = "KILLED"
    else:
        verdict = "SURVIVED"
    shutil.rmtree(bench / "obj_dir", ignore_errors=True)
    return dict(mutant=name, verdict=verdict, build_rc=brc, run_rc=rrc,
                complete=complete, n_fail=len(fails), fails=fails)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--jobs", type=int, default=2)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    a.work.mkdir(parents=True, exist_ok=True)
    names = a.only or (["golden"] + list(MUTANTS))
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        results = list(ex.map(lambda n: one(n, a.src.resolve(), a.work.resolve(),
                                            a.out.resolve()), names))
    for r in results:
        print(json.dumps({k: v for k, v in r.items() if k != "fails"}))
    (a.out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    bad = [r for r in results if r["verdict"] not in ("PASS", "KILLED")]
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
