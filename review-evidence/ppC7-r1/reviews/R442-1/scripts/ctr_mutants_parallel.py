#!/usr/bin/env python3
"""Reviewer re-run of tb/pp_top/ctr_mutants.py, arms in parallel.

Same arm list, patches and kill rule as the in-tree driver (imported from it):
the control must pass; an arm is KILLED only when its `counters` run printed a
tally, exited non-zero and printed a FAIL line starting with the arm's named
check. Each arm gets its own copy of hdl/, tb/common and tb/pp_top (no obj_*,
no ROM images). The only difference from the in-tree driver is the copy's
Makefile building with `-j 3` instead of `-j 0`, so concurrent arms fit the
reviewer's memory cap. Usage:
  ctr_mutants_parallel.py <tree> <outdir> [--jobs N] [--patches DIR] [--arms a,b]
"""
import argparse
import concurrent.futures as cf
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path


def load_driver(tree: Path):
    spec = importlib.util.spec_from_file_location("ctr_mutants", tree / "tb/pp_top/ctr_mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def prepare(tree: Path, work: Path) -> None:
    if work.exists():
        shutil.rmtree(work)
    ign = shutil.ignore_patterns("obj_*", "*.hex", "__pycache__")
    shutil.copytree(tree / "hdl", work / "hdl", ignore=ign)
    for s in ("common", "pp_top"):
        shutil.copytree(tree / "tb" / s, work / "tb" / s, ignore=ign)
    mk = work / "tb/pp_top/Makefile"
    mk.write_text(mk.read_text().replace("--build -j 0", "--build -j 3"))


def one(tree: Path, out: Path, scratch: Path, arm: str, expected: str, patches: Path):
    work = scratch / arm
    prepare(tree, work)
    if arm != "control":
        p = patches / (arm + ".patch")
        subprocess.run(["git", "apply", "--check", str(p)], cwd=work, check=True)
        subprocess.run(["git", "apply", str(p)], cwd=work, check=True)
    log = out / f"{arm}.log"
    with log.open("w") as s:
        rc = subprocess.run(["make", "-C", str(work / "tb/pp_top"), "counters"],
                            stdout=s, stderr=subprocess.STDOUT).returncode
    text = log.read_text()
    fails = [l for l in text.splitlines() if l.startswith("FAIL:")]
    tally = [l for l in text.splitlines() if l.startswith("K-AVB:")]
    named = [l for l in fails if l[5:].strip().startswith(expected)] if expected else []
    if arm == "control":
        ok = rc == 0 and bool(tally) and not fails
        verdict = "PASS" if ok else "FAIL"
    else:
        ok = rc != 0 and bool(tally) and bool(named)
        verdict = "KILLED" if ok else "UNPROVEN"
    shutil.rmtree(work, ignore_errors=True)
    return arm, rc, len(fails), len(named), verdict, tally, fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tree", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--jobs", type=int, default=5)
    ap.add_argument("--patches", type=Path, default=None)
    ap.add_argument("--arms", default="")
    ap.add_argument("--extra", action="append", default=[],
                    help="arm=named-check for an extra reviewer patch in --patches")
    a = ap.parse_args()
    tree = a.tree.resolve()
    drv = load_driver(tree)
    patches = (a.patches or (tree / "tb/pp_top/ctr_mutations")).resolve()
    arms = [("control", "")] + list(drv.MUTANTS)
    for e in a.extra:
        k, v = e.split("=", 1)
        arms.append((k, v))
    if a.arms:
        keep = set(a.arms.split(","))
        arms = [m for m in arms if m[0] in keep or m[0] == "control"]
    a.out.mkdir(parents=True, exist_ok=True)
    scratch = a.out / "work"
    scratch.mkdir(exist_ok=True)
    res = {}
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        futs = [ex.submit(one, tree, a.out, scratch, arm, exp, patches) for arm, exp in arms]
        for f in cf.as_completed(futs):
            r = f.result()
            res[r[0]] = r
    bad = 0
    with (a.out / "summary.txt").open("w") as s:
        for arm, exp in arms:
            _, rc, nf, nn, v, tally, fails = res[arm]
            line = f"{arm}: rc={rc} failures={nf} named={nn} {v} {tally[-1] if tally else 'NO-TALLY'}"
            print(line); s.write(line + "\n")
            for l in fails:
                s.write("    " + l + "\n")
            bad += v not in ("PASS", "KILLED")
        s.write(f"{len(arms)} arms incl. control: {len(arms) - bad} as required, {bad} not\n")
    print(f"{len(arms)} arms incl. control: {len(arms) - bad} as required, {bad} not")
    return int(bad != 0)


if __name__ == "__main__":
    sys.exit(main())
