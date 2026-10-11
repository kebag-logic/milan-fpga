#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer-owned, independent mutant re-application for the rx_err_i change.

Each mutant is an edit written by the reviewer (three re-apply arm mutants in
a different textual form, four are new). Every mutant is built twice: against
the project's parser bench (tb/verilator/parser/sim_main.cpp at the clone
head) and against the reviewer probe (scripts/probe_rxerr.cpp). Nothing is
written into the clone. Usage:
  python3 -I reviewer_mutants.py <clone> <workdir> <outdir> [--jobs N]
"""
import concurrent.futures as cf
import os
import re
import subprocess
import sys
from pathlib import Path

PIN = os.environ.get("PIN", "$VALIDATION_TOOLS/pinned-verilator-5.050")
HERE = Path(__file__).resolve().parent
LATCH = "        if (rx_err_i) bad_r <= 1'b1;\n"

MUTANTS = {
    # re-applied arm defects, independent edit text
    "R1_latch_deleted": [(LATCH, "")],
    "R2_latch_before_sof_clear": [
        (LATCH, ""),
        ("        if (rx_sof_i) begin\n          cnt_r    <= 11'd1;\n",
         "        if (rx_err_i) bad_r <= 1'b1;\n"
         "        if (rx_sof_i) begin\n          cnt_r    <= 11'd1;\n")],
    "R3_eof_direct_term_dropped": [
        ("fin_ok_r <= !bad_r && !rx_err_i &&", "fin_ok_r <= !bad_r &&")],
    "R7_latch_outside_valid": [
        (LATCH + "      end\n    end\n  end\n",
         "      end\n      if (rx_err_i) bad_r <= 1'b1;\n    end\n  end\n")],
    # reviewer-new defects
    "N1_latch_skips_sof_byte": [
        (LATCH, "        if (rx_err_i && !rx_sof_i) bad_r <= 1'b1;\n")],
    "N2_latch_needs_run": [
        (LATCH, "        if (rx_err_i && run_r) bad_r <= 1'b1;\n")],
    "N3_header_writes_ignore_poison": [
        ("bank_we_o    <= !bad_r;", "bank_we_o    <= 1'b1;")],
    "N4_latch_skips_eof_byte_equivalent": [
        (LATCH, "        if (rx_err_i && !rx_eof_i) bad_r <= 1'b1;\n")],
}


def stage(clone: Path, work: Path, name: str, edits) -> Path:
    src = (clone / "hdl/wire/KL_gptp_rx_parser.sv").read_text()
    for pat, rep in edits:
        if pat.endswith("<= !bad_r;") or pat.startswith("bank_we_o"):
            n = src.count(pat)
            if n < 1:
                raise SystemExit(f"{name}: pattern absent")
            src = src.replace(pat, rep)
            continue
        if src.count(pat) != 1:
            raise SystemExit(f"{name}: pattern count {src.count(pat)} != 1")
        src = src.replace(pat, rep)
    d = work / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "KL_gptp_rx_parser.sv").write_text(src)
    return d


def build_run(clone: Path, d: Path, which: str) -> str:
    pkg = clone / "hdl/ucpu/gptp_ucpu_pkg.sv"
    cpp = (clone / "tb/verilator/parser/sim_main.cpp") if which == "bench" \
        else (HERE / "probe_rxerr.cpp")
    inc = clone / "tb/verilator/parser"
    mdir = d / f"obj_{which}"
    b = subprocess.run(
        [f"{PIN}/verilator", "--cc", "--exe", "--build", "-j", "2",
         "--top-module", "KL_gptp_rx_parser", "-Wno-fatal", "-Wno-WIDTHEXPAND",
         "-Wno-WIDTHTRUNC", "--Mdir", str(mdir),
         "-CFLAGS", f"-std=c++17 -O2 -I{inc}", str(pkg),
         str(d / "KL_gptp_rx_parser.sv"), str(cpp), "-o", "V"],
        capture_output=True, text=True)
    if b.returncode != 0:
        return f"BUILD FAILED rc={b.returncode}\n{b.stdout[-2000:]}{b.stderr[-2000:]}"
    r = subprocess.run([str(mdir / "V")], capture_output=True, text=True)
    return f"rc={r.returncode}\n{r.stdout}"


def main() -> int:
    clone, work, out = (Path(a).resolve() for a in sys.argv[1:4])
    jobs = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
    out.mkdir(parents=True, exist_ok=True)
    tasks = {}
    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
        for name, edits in MUTANTS.items():
            d = stage(clone, work, name, edits)
            for which in ("bench", "probe"):
                tasks[ex.submit(build_run, clone, d, which)] = (name, which)
        for f in cf.as_completed(tasks):
            name, which = tasks[f]
            (out / f"{name}.{which}.log").write_text(f.result())
    rows = []
    for name in MUTANTS:
        b = (out / f"{name}.bench.log").read_text()
        p = (out / f"{name}.probe.log").read_text()
        tb = re.search(r"(\d+) checks: (\d+) PASS, (\d+) FAIL", b)
        tp = re.search(r"(\d+) checks: (\d+) PASS, (\d+) FAIL", p)
        bf = [l[5:].split(" got ")[0].strip() for l in b.splitlines() if l.startswith("FAIL ")]
        pf = [l[11:] for l in p.splitlines() if l.startswith("CHECK FAIL ")]
        rows.append(f"{name}\tbench {tb.group(0) if tb else 'NO TALLY'}\t"
                    f"probe {tp.group(0) if tp else 'NO TALLY'}\n"
                    f"  bench FAIL names: {sorted(set(bf))}\n"
                    f"  probe FAIL names: {pf}\n")
    (out / "SUMMARY.txt").write_text("".join(rows))
    print("".join(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
