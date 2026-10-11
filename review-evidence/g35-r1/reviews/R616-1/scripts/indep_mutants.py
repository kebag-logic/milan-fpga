#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-written rx_err_i mutants, run against the parser suite at head.

Independent of tb/verilator/parser/mutants.py: different edit forms and
three defects that file does not plant. Each mutant is built from a
private copy of the RTL and the head sim_main.cpp; a mutant is CAUGHT only
when every check name it lists appears on a FAIL line, and an expected
survivor (an equivalent rewrite) must PASS the suite.

usage: indep_mutants.py <head-tree> <workdir> [--jobs N]
Needs Verilator 5.050 first on PATH.
"""
import argparse, concurrent.futures as cf, pathlib, re, shutil, subprocess, sys

LATCH = "        if (rx_err_i) bad_r <= 1'b1;\n"
FIN = "fin_ok_r <= !bad_r && !rx_err_i && (cnt_r >= min_end_w) &&"
T = ("sync", "fu", "pdreq", "pdresp")
def each(c): return [f"{t} {c}" for t in T]

MUTANTS = [
    # name, [(old, new)], checks that must FAIL ([] = must PASS: equivalent)
    ("R1 latch deleted (re-applied control)", [(LATCH, "")],
     each("rx_err at every byte: one drop") + each("rx_err at every byte: no event")
     + each("rx_err at every byte: no later write")),
    ("R2 latch skips the sof byte (other form of the first-byte defect)",
     [(LATCH, "        if (rx_err_i && !rx_sof_i) bad_r <= 1'b1;\n")],
     each("rx_err at every byte: one drop") + each("rx_err at every byte: no event")),
    ("R3 eof term removed from fin_ok_r (re-applied)",
     [(FIN, "fin_ok_r <= !bad_r && (cnt_r >= min_end_w) &&")],
     each("rx_err at every byte: one drop") + each("rx_err at every byte: no event")),
    ("R4 latch only in the first 30 bytes (novel)",
     [(LATCH, "        if (rx_err_i && (rx_sof_i || cnt_r < 11'd30)) bad_r <= 1'b1;\n")],
     each("rx_err at every byte: one drop") + each("rx_err at every byte: no event")),
    ("R5 an eof flag also counts as a runt drop (novel)",
     [("assign runt_drop_w = rx_valid_i && rx_sof_i && rx_eof_i;",
       "assign runt_drop_w = rx_valid_i && rx_eof_i && (rx_sof_i || rx_err_i);")],
     each("rx_err at every byte: one drop") + each("rx_err held from byte 20 to eof: one drop")),
    ("R6 flag refuses at eof but bank writes continue (novel)",
     [("  logic        bad_r;", "  logic        err_r;\n  logic        bad_r;"),
      ("      bad_r       <= 1'b0;\n", "      bad_r       <= 1'b0;\n      err_r       <= 1'b0;\n"),
      ("          bad_r    <= 1'b0;\n", "          bad_r    <= 1'b0;\n          err_r    <= 1'b0;\n"),
      (LATCH, "        if (rx_err_i) err_r <= 1'b1;\n"),
      (FIN, "fin_ok_r <= !bad_r && !err_r && !rx_err_i && (cnt_r >= min_end_w) &&")],
     each("rx_err at every byte: no later write")),
    ("R7 latch gated off the eof byte (equivalent: the eof term still refuses)",
     [(LATCH, "        if (rx_err_i && !rx_eof_i) bad_r <= 1'b1;\n")], []),
]

def run(head, work, idx, name, edits, must):
    d = work / f"m{idx}"; diff = ""
    shutil.rmtree(d, ignore_errors=True)
    (d / "hdl/wire").mkdir(parents=True); (d / "hdl/ucpu").mkdir(parents=True)
    shutil.copy(head / "hdl/ucpu/gptp_ucpu_pkg.sv", d / "hdl/ucpu/")
    src = (head / "hdl/wire/KL_gptp_rx_parser.sv").read_text()
    for old, new in edits:
        if src.count(old) != 1:
            return idx, name, "PATTERN-NOT-UNIQUE", ""
        src = src.replace(old, new)
    (d / "hdl/wire/KL_gptp_rx_parser.sv").write_text(src)
    if idx >= 0:
        diff = subprocess.run(["diff", "-u", str(head / "hdl/wire/KL_gptp_rx_parser.sv"),
                               str(d / "hdl/wire/KL_gptp_rx_parser.sv")], capture_output=True, text=True).stdout
    b = subprocess.run(["verilator", "--cc", "--exe", "--build", "-j", "2", "--top-module",
                        "KL_gptp_rx_parser", "-Wall", "-Wno-fatal", "-Wno-DECLFILENAME",
                        "-Wno-UNUSEDSIGNAL", "-Wno-WIDTHEXPAND", "-Wno-WIDTHTRUNC",
                        "-Wno-UNUSEDPARAM", "--Mdir", str(d / "obj"), "-CFLAGS",
                        f"-std=c++17 -O1 -I{head}/tb/verilator/parser",
                        str(d / "hdl/ucpu/gptp_ucpu_pkg.sv"), str(d / "hdl/wire/KL_gptp_rx_parser.sv"),
                        str(head / "tb/verilator/parser/sim_main.cpp"), "-o", "Vsim"],
                       capture_output=True, text=True)
    if b.returncode != 0:
        return idx, name, "BUILD-FAILED", diff
    r = subprocess.run([str(d / "obj/Vsim")], capture_output=True, text=True)
    out = r.stdout
    tally = re.search(r"^(\d+) checks: (\d+) PASS, (\d+) FAIL$", out, re.M)
    fails = [l for l in out.splitlines() if l.startswith("FAIL ")]
    (work / f"m{idx}.out").write_text(out)
    tl = tally.group(0) if tally else "no tally"
    if not must:
        verdict = "EQUIVALENT-PASSES" if (r.returncode == 0 and tally and tally.group(3) == "0") else "UNEXPECTED-FAIL"
    else:
        missed = [c for c in must if not any(c in l for l in fails)]
        verdict = "CAUGHT-BY-NAME" if (r.returncode != 0 and not missed) else f"NOT-CAUGHT missed={missed}"
    return idx, name, f"{verdict} rc={r.returncode} [{tl}] named={len(must)} faillines={len(fails)}", diff

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("head"); ap.add_argument("work")
    ap.add_argument("--jobs", type=int, default=8); a = ap.parse_args()
    head, work = pathlib.Path(a.head).resolve(), pathlib.Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    jobs = [(-1, "C0 unmutated head", [], [])] + [(i, *m) for i, m in enumerate(MUTANTS)]
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        res = sorted(ex.map(lambda j: run(head, work, *j), jobs))
    bad = 0
    for idx, name, v, diff in res:
        print(f"{name}: {v}")
        if diff: print("".join("    " + l + "\n" for l in diff.splitlines()[2:]), end="")
        ok = v.startswith("CAUGHT-BY-NAME") or v.startswith("EQUIVALENT-PASSES")
        bad += not ok
    print(f"{len(res)} arms: {len(res)-bad} as expected, {bad} unexpected")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
