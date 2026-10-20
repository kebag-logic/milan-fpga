#!/usr/bin/env python3
"""[762-DP] wiring mutants: plant one .stopped_i variant at milan_datapath.sv:6308
in a byte copy of a clean clone, run one milan_dp leg, and grade the failing set.

Usage: dp762_mutants.py <clean-clone> <work-dir> <out-dir> <leg> [<leg> ...]
Each leg is a RUN_CASES name (dynmap, nxn4c, ...). A clean control runs in the
clean clone itself. A mutant is CAUGHT only if its run exits nonzero and its
[FAIL] lines are exactly the named checks; anything else is not evidence.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

LINE = 6308
CLEAN = "    .stopped_i      (acmpl_stopped_v_w[N_STREAMS-1:0]),"
GAP = "[762-DP] 2 stopped gap: STREAM_INTERRUPTED +0"
SIL = "[762-DP] 3 stopped silence: STREAM_INTERRUPTED +0"
RESTART = "[762-DP] 4 started gap: STREAM_INTERRUPTED +1"
MUTANTS = [
    ("tie0", "    .stopped_i      ('0),", {GAP, SIL}),
    ("sink1", "    .stopped_i      (acmpl_stopped_v_w[N_STREAMS:1]),", {GAP, SIL}),
    ("bound", "    .stopped_i      (acmpl_bound_v_w[N_STREAMS-1:0]),", {RESTART}),
]


def fails(log: str) -> set[str]:
    out = set()
    for line in log.splitlines():
        s = line.strip()
        if s.startswith("[FAIL]"):
            name = s[len("[FAIL]"):].strip()
            out.add(name.split(" got=")[0].strip())
    return out


def tally(log: str) -> str:
    for line in log.splitlines():
        if line.startswith("checks:"):
            return " ".join(line.split())
    return "no tally"


def run(clone: Path, leg: str, log: Path) -> int:
    with log.open("w") as f:
        r = subprocess.run(["make", "--no-print-directory", f"run-{leg}"],
                           cwd=clone / "tb/verilator/milan_dp", stdout=f,
                           stderr=subprocess.STDOUT, check=False)
    return r.returncode


def main() -> int:
    clean, work, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    legs = sys.argv[4:]
    out.mkdir(parents=True, exist_ok=True)
    dp = clean / "hdl/milan/milan_datapath.sv"
    lines = dp.read_text().split("\n")
    if lines[LINE - 1] != CLEAN:
        print(f"line {LINE} is not the clean wiring: {lines[LINE - 1]!r}")
        return 2
    rows = []
    bad = 0
    for leg in legs:
        log = out / f"clean.{leg}.log"
        rc = run(clean, leg, log)
        text = log.read_text(errors="replace")
        f = fails(text)
        ok = rc == 0 and not f
        bad += not ok
        rows.append(f"clean\t{leg}\trc={rc}\t{tally(text)}\t{'PASS' if ok else 'NOT CLEAN'}\t"
                    + "; ".join(sorted(f)))
    for name, repl, expect in MUTANTS:
        m = work / f"mut-{name}"
        if m.exists():
            shutil.rmtree(m)
        # no built objects: each mutant elaborates from its own source
        shutil.copytree(clean, m, symlinks=True,
                        ignore=shutil.ignore_patterns("obj_*"))
        mdp = m / "hdl/milan/milan_datapath.sv"
        ml = mdp.read_text().split("\n")
        ml[LINE - 1] = repl
        mdp.write_text("\n".join(ml))
        diff = subprocess.run(["git", "diff", "--", "hdl/milan/milan_datapath.sv"], cwd=m,
                              capture_output=True, text=True, check=False).stdout
        (out / f"mut-{name}.diff").write_text(diff)
        for leg in legs:
            log = out / f"mut-{name}.{leg}.log"
            rc = run(m, leg, log)
            text = log.read_text(errors="replace")
            f = fails(text)
            caught = rc != 0 and f == expect
            bad += not caught
            rows.append(f"{name}\t{leg}\trc={rc}\t{tally(text)}\t"
                        f"{'CAUGHT' if caught else 'NOT EVIDENCE'}\t" + "; ".join(sorted(f)))
        shutil.rmtree(m / "tb/verilator/milan_dp", ignore_errors=True)
    (out / "SUMMARY.tsv").write_text("\n".join(rows) + "\n")
    print("\n".join(rows))
    print(f"result: {'PASS' if bad == 0 else 'FAIL'} ({len(rows) - bad}/{len(rows)})")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    os.environ.setdefault("VERILATOR_JOBS", "2")
    sys.exit(main())
