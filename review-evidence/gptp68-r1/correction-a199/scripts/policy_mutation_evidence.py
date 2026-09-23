#!/usr/bin/env python3
"""Show, per required #68 test, which planted defect makes it fail.

Reuses the suite's own mutation machinery (tb/verilator/engine/mutants.py:
stage, generate_image, build, run_harness; tb/mutation_verdict.py), so the
harness, the build flags and the image arguments are exactly the suite's.
Nothing is written into the lane tree; everything is staged in a temp dir.

Runs, four at a time, each against the NEW harness and the unmutated RTL:
  * the clean sources (must pass);
  * every #68 generator mutant listed in mutants.py;
  * the BASE generator (c1b6174, the pre-#68 20 us rule on every pair);
  * the REVIEWED generator (77c34e9, the retired one-second rule).
For each run: the verdict, every FAIL line, then a matrix of the required
tests against the runs, each cell the number of that test's checks that
failed (0: the test does not see that defect).

Usage: python3 policy_mutation_evidence.py   (source env.sh first)
"""
from __future__ import annotations

import concurrent.futures as cf
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path(os.environ.get("A199_LANE", "$LANES/gptp68-step-policy"))
ENGINE = LANE / "tb/verilator/engine"
sys.path.insert(0, str(ENGINE))
sys.path.insert(0, str(LANE / "tb"))
import mutants as M  # noqa: E402
from mutation_verdict import verdict  # noqa: E402

FIRST_68 = "every pair uses the locked threshold"
OLD = {"base c1b6174 (20 us on every pair)":
       "c1b617435824929a790739ea8585c3fe1a328cc0",
       "reviewed 77c34e9 (first sync over 1 s)":
       "77c34e904eba2446755d13e1bf4763d1652c3ca7"}

#: required test -> the check-name prefixes that belong to it
TESTS = {
    "T1 link-up: 15 us slews, 25 us steps": (
        "link-up +15 us", "link-up -15 us", "link-up +25 us",
        "link-up -25 us", "link-up: one step pulse"),
    "T1 link-up: exactly 20 us slews, 20 us + 1 ns steps": (
        "link-up +20 us", "link-up -20 us"),
    "T1 link-up after asCapable returns: -25 us steps": (
        "link-up after asCapable",),
    "T1 link-up after become: +25 us steps": ("link-up after become",),
    "T1 link-up after a warm reset: +25 us steps": ("warm-reset link-up",),
    "T2 locked: 90 us slews, 110 us steps": (
        "locked +90 us", "locked -90 us", "locked +110 us",
        "locked -110 us", "locked: one step pulse"),
    "T2 locked: exactly 100 us slews, 100 us + 1 ns steps": (
        "locked +100 us", "locked -100 us"),
    "T3 GM change: 50 us slews, 5 ms steps": ("GM change",),
    "T4 long locked slew never exceeds +-200 ppm": ("long slew",),
    "T5 consumer envelope over the whole run": ("consumer envelope",),
    "becoming grandmaster clears sync-ok": (
        "becoming grandmaster clears",),
}

FAIL_RE = re.compile(r"^FAIL (.*?)\s+got [0-9a-f]{16} exp", re.M)


def classify(fails: list[str]) -> dict[str, int]:
    return {t: sum(1 for f in fails if f.startswith(p))
            for t, p in TESTS.items()}


def one(exe: Path, work: Path, tag: str, srcdir: Path) -> tuple[str, list[str], str]:
    rundir = work / f"run_{tag}"
    if not M.generate_image(srcdir, rundir):
        return "generator refused", [], ""
    rc, out = M.run_harness(exe, rundir)
    tally = [ln for ln in out.splitlines() if " checks: " in ln]
    return verdict(rc, out), FAIL_RE.findall(out), tally[-1] if tally else ""


def main() -> int:
    names = [m[0] for m in M.MUTATIONS]
    muts = M.MUTATIONS[names.index(FIRST_68):]
    jobs = []
    with tempfile.TemporaryDirectory(prefix="a199-policy-") as td:
        work = Path(td)
        clean = M.stage(work, "clean")
        exe = M.build(clean, work, "clean")
        if exe is None:
            print("clean build failed")
            return 1
        jobs.append(("clean sources", clean))
        for name, fname, pat, rep, _ in muts:
            assert fname == M.GENERATOR, name
            tag = "".join(c if c.isalnum() else "_" for c in name)
            jobs.append((f"mutant: {name}", M.stage(work, tag, (fname, pat, rep))))
        for label, sha in OLD.items():
            src = M.stage(work, sha[:7])
            (src / M.GENERATOR).write_text(subprocess.run(
                ["git", "-C", str(LANE), "show", f"{sha}:hdl/{M.GENERATOR}"],
                capture_output=True, text=True, check=True).stdout)
            jobs.append((label, src))
        with cf.ThreadPoolExecutor(max_workers=4) as pool:
            futs = [pool.submit(one, exe, work, f"j{i}", src)
                    for i, (_, src) in enumerate(jobs)]
            results = [f.result() for f in futs]
    bad = 0
    rows = []
    for (label, _), (ans, fails, tally) in zip(jobs, results):
        print(f"== {label}: {ans} ({tally})")
        for f in fails:
            print(f"   FAIL {f}")
        rows.append((label, classify(fails)))
        want = "pass" if label == "clean sources" else "caught"
        if ans != want:
            bad += 1
            print(f"   ^^ expected {want}")
    tests = list(TESTS)
    print("\n| run | " + " | ".join(tests) + " |")
    print("|---" * (len(tests) + 1) + "|")
    for label, c in rows:
        print(f"| {label} | " + " | ".join(str(c[t]) for t in tests) + " |")
    print("\nRESULT:", "PASS" if bad == 0 else f"FAIL ({bad})")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
