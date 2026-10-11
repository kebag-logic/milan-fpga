#!/usr/bin/env python3
"""Reviewer-planted defects for the CSR read-path lockstep (PR #722 review R599-1).

Independent of tb/verilator/csr/lock_mutants.py: each defect below is chosen by the
reviewer, planted as ONE exact text replacement into a copy of
hdl/common/csr/milan_csr.sv, built through the suite Makefile's own lock1/lock8 recipe
(LOCK_SRC and the leg's build directory overridden) and run. The harness's printed
[FAIL] lines are recorded. A defect counts as caught when the harness exits nonzero
with at least one named [FAIL] line; `expect` names the check(s) the reviewer
predicted, and `equivalent` marks a planted change the reviewer predicts to be
unobservable in today's map (it is run to test that prediction, not counted as a catch).

usage: python3 -I r599_mutants.py <source-root> <work-dir>
       (VERILATOR in the environment selects the simulator)
"""
import subprocess
import sys
from pathlib import Path

MUTANTS = [
    ("R1 shadow served under a live claim (shadow_rd_w drops !live_hit)",
     "  wire shadow_rd_w = rd_in_window && !live_hit;",
     "  wire shadow_rd_w = rd_in_window;",
     "lock1", ("decode",), False),
    ("R2 stage-1 window/read-window gate removed",
     "        live_mux_q <= (strm_hit || rd_in_window) ? live_mux : 32'h0;",
     "        live_mux_q <= live_mux;",
     "lock1", (), True),
    ("R3 out-of-range SNAP leaves the CNT kinds unchanged",
     "            for (int w = 1; w < 11; w++) snap_kind_r[w] <= SK_ZERO_C;\n",
     "",
     "lock1", ("snapshot-freshness",), False),
    ("R4 extra talker context SNAP does not pre-POISON the CNT kinds",
     "            if (strm_dir_r)\n"
     "              for (int w = 1; w < 11; w++) snap_kind_r[w] <= SK_POISON_C;\n",
     "",
     "lock8", ("snapshot-coherence",), False),
    ("R5 CNT kind read off by one word",
     "            unique case (snap_kind_r[1 + 32'(coff[5:2])])",
     "            unique case (snap_kind_r[32'(coff[5:2])])",
     "lock1", ("decode", "snapshot-coherence"), False),
    ("R6 listener burst arm elaborated only above eight listeners",
     "              default: if (N_LISTENERS_P > 1) begin",
     "              default: if (N_LISTENERS_P > 8) begin",
     "lock8", ("snapshot-coherence",), False),
    ("R7 shadow output register loads on every cycle, not only on rd_pend",
     "    else if (rd_pend)\n      shadow_qq <= shadow_q;",
     "    else\n      shadow_qq <= shadow_q;",
     "lock1", ("lockstep",), False),
]


def failed_checks(out: str) -> list[str]:
    """Names of the checks the harness printed as [FAIL]."""
    return [ln.strip()[len("[FAIL]"):].split(":")[0].strip()
            for ln in out.splitlines() if ln.strip().startswith("[FAIL]")]


def main(argv: list[str]) -> int:
    """Plant, build and run every reviewer mutant; print one verdict line each."""
    root = Path(argv[1]).resolve()
    work = Path(argv[2]).resolve()
    csr_dir = root / "tb/verilator/csr"
    src = (root / "hdl/common/csr/milan_csr.sv").read_text()
    bad = 0
    for n, (name, pat, rep, leg, expect, equivalent) in enumerate(MUTANTS):
        if src.count(pat) != 1:
            print(f"[ERROR] {name}: pattern occurs {src.count(pat)} times")
            bad += 1
            continue
        mdir = work / f"r{n}"
        mdir.mkdir(parents=True, exist_ok=True)
        mpath = mdir / "milan_csr.sv"
        mpath.write_text(src.replace(pat, rep))
        b = subprocess.run(["make", "-s", "-C", str(csr_dir), leg, f"LOCK_SRC={mpath}",
                            f"{leg.upper()}_MDIR={mdir / 'obj'}"],
                           capture_output=True, text=True, check=False)
        (mdir / "build.log").write_text(b.stdout + b.stderr)
        exe = mdir / "obj" / "Vcsr_lock"
        if b.returncode != 0 or not exe.is_file():
            print(f"[ERROR] {name}: build rc {b.returncode}")
            bad += 1
            continue
        r = subprocess.run([str(exe)], cwd=str(csr_dir), capture_output=True, text=True,
                           check=False)
        out = r.stdout + r.stderr
        (mdir / "run.log").write_text(out)
        fails = failed_checks(out)
        caught = r.returncode != 0 and bool(fails)
        if equivalent:
            tag = "PREDICTED-EQUIVALENT, survived" if not caught else "PREDICTED-EQUIVALENT but CAUGHT"
        elif caught:
            hit = [e for e in expect if e in fails]
            tag = "CAUGHT" + ("" if not expect or hit else " (not by the predicted check)")
        else:
            tag = "SURVIVED"
            bad += 1
        print(f"[{tag}] {leg} rc={r.returncode} {name}; failed: {', '.join(fails) or '-'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
