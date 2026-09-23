#!/usr/bin/env python3
"""Show, per required #68 test, which planted defect makes it fail.

Reuses the lane's own mutation machinery (tb/verilator/engine/mutants.py:
stage, generate_image, build, run_harness, verdict), so the harness, the
build flags and the image arguments are exactly the suite's. Nothing is
written into the lane tree; everything is staged under a temp directory.

Runs:
  * the clean sources (must pass),
  * every #68 generator mutant listed in mutants.py,
  * the BASE generator (git show BASE:hdl/ucode/gen_gptp_ucode.py), i.e.
    the whole policy removed, against the NEW harness.

For each run it prints the verdict and every FAIL line, then a matrix of
the four required tests (plus the boundary and envelope checks) against the
runs, each cell the number of that test's checks that failed.

Usage: python3 policy_mutation_evidence.py [--base SHA]
Requires the scoped verilator first on PATH (source env.sh).
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path(os.environ.get("A188_LANE", "$LANES/gptp68-step-policy"))
ENGINE = LANE / "tb/verilator/engine"
sys.path.insert(0, str(ENGINE))
sys.path.insert(0, str(LANE / "tb"))
import mutants as M  # noqa: E402

FIRST_68 = "a synchronized servo may step"

#: required test -> the check-name prefixes that belong to it
TESTS = {
    "900 ms slews, no step pulse": ("+900 ms first", "-900 ms synchronized",
                                    "+900 ms:", "-900 ms:", "900 ms:"),
    "1.1 s steps exactly once": ("+1.1 s first", "+1.1 s synchronized",
                                 "+1.1 s:", "-1.1 s first", "1.1 s:",
                                 "over one second"),
    "GM change, small offset: no step": ("before the GM change",
                                         "GM change: ", "GM change, +300 us",
                                         "GM change alone"),
    "GM change contrast, 1.5 s: one step": ("second GM change",
                                            "GM change over one second"),
    "first sync after asCapable": ("first sync under 1 s",
                                   "first pair after asCapable returns"),
    "exact 1 s boundary": ("+1 s first", "-1 s first", "+1 s + 1 ns",
                           "-1 s - 1 ns"),
}

FAIL_RE = re.compile(r"^FAIL (.*?)\s+got ", re.M)


def classify(fails: list[str]) -> dict[str, int]:
    out = {}
    for test, prefixes in TESTS.items():
        out[test] = sum(1 for f in fails if f.startswith(prefixes))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="c1b617435824929a790739ea8585c3fe1a328cc0")
    args = ap.parse_args()
    names = [m[0] for m in M.MUTATIONS]
    muts = M.MUTATIONS[names.index(FIRST_68):]
    runs: list[tuple[str, str, list[str]]] = []
    with tempfile.TemporaryDirectory(prefix="a188-policy-") as td:
        work = Path(td)
        clean_src = M.stage(work, "clean")
        exe = M.build(clean_src, work, "clean")
        if exe is None:
            print("clean build failed")
            return 1

        def one(tag: str, srcdir: Path) -> None:
            rundir = work / f"run_{len(runs)}"
            if not M.generate_image(srcdir, rundir):
                runs.append((tag, "generator refused", []))
                return
            rc, out = M.run_harness(exe, rundir)
            fails = FAIL_RE.findall(out)
            tally = re.findall(r"^\d+ checks: .*$", out, re.M)
            runs.append((tag, f"{M.verdict(rc, out)} ({tally[-1] if tally else 'no tally'})", fails))

        one("clean sources", clean_src)
        for name, fname, pat, rep, _ in muts:
            tag = "m_" + "".join(c if c.isalnum() else "_" for c in name)
            one(f"mutant: {name}", M.stage(work, tag, (fname, pat, rep)))
        base_src = M.stage(work, "basegen")
        base_gen = subprocess.run(
            ["git", "-C", str(LANE), "show", f"{args.base}:hdl/ucode/gen_gptp_ucode.py"],
            capture_output=True, text=True, check=True).stdout
        (base_src / M.GENERATOR).write_text(base_gen, encoding="utf-8")
        one(f"base generator {args.base[:12]} (policy removed)", base_src)

    for tag, verdict, fails in runs:
        print(f"== {tag}: {verdict}")
        for f in fails:
            print(f"   FAIL {f}")
    print("\nMatrix: failed checks per required test (0 = the test does not see it)")
    cols = list(TESTS)
    print("| run | " + " | ".join(cols) + " |")
    print("|---|" + "---|" * len(cols))
    for tag, _, fails in runs:
        c = classify(fails)
        print(f"| {tag} | " + " | ".join(str(c[k]) for k in cols) + " |")
    ok = runs[0][1].startswith("pass") and all(
        v.startswith("caught") for _, v, _ in runs[1:])
    print("\nRESULT:", "PASS (clean passes, every defect caught)" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
