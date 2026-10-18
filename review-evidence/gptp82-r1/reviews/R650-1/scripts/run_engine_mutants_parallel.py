#!/usr/bin/env python3
"""Reviewer-owned parallel runner for tb/verilator/engine/mutants.py.

Imports the tree's own mutation table and helpers (stage, build,
generate_image, run_harness, verdict) and runs the clean control plus each
selected mutant concurrently. Extra reviewer probe mutants can be appended
with --extra FILE (a Python file defining EXTRA = [(name, file, pattern,
replacement, breaks), ...]).

The #82 rule of the tree's driver is reproduced: a mutant whose `breaks`
starts with "#82 " must fail every " | "-separated check it names.

usage: run_engine_mutants_parallel.py TREE [--jobs N] [--only REGEX]
                                         [--extra FILE] [--keep DIR]
"""
import argparse
import concurrent.futures as cf
import importlib.util
import re
import sys
import tempfile
from pathlib import Path


def load(tree: Path):
    eng = tree / "tb" / "verilator" / "engine"
    spec = importlib.util.spec_from_file_location("eng_mutants",
                                                  eng / "mutants.py")
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(tree / "tb"))
    spec.loader.exec_module(mod)
    return mod


def judge(mod, name, breaks, rc, out):
    answer = mod.verdict(rc, out)
    failed = [l for l in out.splitlines() if l.startswith("FAIL ")]
    if answer == "caught" and breaks.startswith("#82 "):
        missed = [w for w in breaks.split(" | ")
                  if not any(w in l for l in failed)]
        if missed:
            answer = "missed named: " + "; ".join(missed)
    elif answer == "caught" and breaks.startswith("slew:"):
        if not any(breaks in l for l in failed):
            answer = "missed its named check"
    return answer, failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tree", type=Path)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--only", default=None)
    ap.add_argument("--extra", type=Path, default=None)
    ap.add_argument("--keep", type=Path, default=None)
    ap.add_argument("--no-control", action="store_true")
    ap.add_argument("--build-jobs", default="2")
    a = ap.parse_args()
    mod = load(a.tree.resolve())
    vf = list(mod.VFLAGS)
    vf[vf.index("-j") + 1] = a.build_jobs
    mod.VFLAGS = vf
    muts = list(mod.MUTATIONS)
    if a.only:
        muts = [m for m in muts if re.search(a.only, m[0] + " " + m[4])]
    if a.extra:
        ns = {}
        exec(a.extra.read_text(), ns)
        muts += ns["EXTRA"]
    base = a.keep or Path(tempfile.mkdtemp(prefix="r650-mut-"))
    base.mkdir(parents=True, exist_ok=True)

    def one(idx, m):
        tag = f"m{idx:02d}" if m else "clean"
        work = base / tag
        work.mkdir(parents=True, exist_ok=True)
        if m:
            name, fname, pat, rep, breaks = m
            text = (mod.HDL / fname).read_text(encoding="utf-8")
            if pat not in text:
                return (tag, name, "PATTERN NOT FOUND", [])
            src = mod.stage(work, tag, (fname, pat, rep))
        else:
            name, breaks = "unmutated control", ""
            src = mod.stage(work, tag)
        run = work / "run"
        exe = mod.build(src, work, tag)
        if exe is None or not mod.generate_image(src, run):
            return (tag, name, "build/generate refused", [])
        rc, out = mod.run_harness(exe, run)
        (work / "harness.log").write_text(out)
        if not m:
            return (tag, name, mod.verdict(rc, out), [])
        ans, failed = judge(mod, name, breaks, rc, out)
        return (tag, name, ans, failed)

    jobs = ([] if a.no_control else [(0, None)]) + \
        [(i + 1, m) for i, m in enumerate(muts)]
    bad = 0
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(one, i, m) for i, m in jobs]
        for f in futs:
            tag, name, ans, failed = f.result()
            ok = (ans == "pass") if tag == "clean" else (ans == "caught")
            bad += 0 if ok else 1
            print(f"[{'OK' if ok else 'XX'}] {tag} {name}: {ans}")
            for l in failed[:12]:
                print(f"      {l}")
    print(f"RESULT {len(jobs) - bad}/{len(jobs)} as expected")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
