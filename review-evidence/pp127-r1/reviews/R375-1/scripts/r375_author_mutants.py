#!/usr/bin/env python3
"""Independent re-execution of the author's mutant table (tb/srp_top/mutants.py
at the exact head) with the pinned simulator, in parallel disposable trees
under <packet>/scratch/amut/. Kill rule as the author's: nonzero exit, a
summary line, and the named assertion among the FAIL lines.

usage: r375_author_mutants.py controls|all|NAME[,NAME...] [--jobs N]
"""
import argparse
import concurrent.futures as cf
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess

PKT = Path(__file__).resolve().parents[1]
HEAD = PKT / "scratch" / "head"
WORK = PKT / "scratch" / "amut"
RCPT = PKT / "receipts" / "author-mutants"
VERILATOR = os.environ.get(
    "R375_VERILATOR",
    "$VALIDATION_STORAGE/pp127-manager-cf4e5c63/pinned-tool-bin/verilator")

spec = importlib.util.spec_from_file_location("am", HEAD / "tb/srp_top/mutants.py")
am = importlib.util.module_from_spec(spec)
spec.loader.exec_module(am)
MUT = {m[0]: m for m in am.MUTANTS}


def tree(label, suite):
    dest = WORK / label
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(HEAD / "hdl", dest / "hdl")
    for s in ("common", suite):
        shutil.copytree(HEAD / "tb" / s, dest / "tb" / s, ignore=shutil.ignore_patterns("obj_*"))
    mk = dest / "tb" / suite / "Makefile"
    t = mk.read_text()
    if "--build -j 0" in t:
        mk.write_text(t.replace("--build -j 0", "--build -j 2"))
    return dest


def run(label, suite, group, edits, expected):
    dest = tree(label, suite)
    for path, anchor, repl in edits:
        f = dest / path
        s = f.read_text()
        assert s.count(anchor) == 1, (label, anchor[:50])
        f.write_text(s.replace(anchor, repl))
    RCPT.mkdir(parents=True, exist_ok=True)
    log = RCPT / f"{label}.log"
    with log.open("w") as out:
        rc = subprocess.run(["make", "-C", str(dest / "tb" / suite), f"VERILATOR={VERILATOR}",
                             f"RUN_ARGS={group}"], stdout=out, stderr=subprocess.STDOUT,
                            timeout=3000).returncode
    txt = log.read_text()
    fails = [l for l in txt.splitlines() if l.startswith("FAIL:")]
    summ = [l for l in txt.splitlines() if " checks: " in l]
    if expected is None:
        ok = rc == 0 and bool(summ) and " 0 FAIL" in summ[-1]
        verdict = "PASS" if ok else "CONTROL-FAILED"
    else:
        ok = rc != 0 and bool(summ) and any(expected in l for l in fails)
        verdict = "KILLED" if ok else "SURVIVED"
    tags = sorted({l.split(":", 2)[1].strip() for l in fails})
    shutil.rmtree(dest / "tb" / suite / "obj_dir", ignore_errors=True)
    return (f"{label} suite={suite} group={group or 'all'} rc={rc} "
            f"{summ[-1] if summ else 'NO SUMMARY'} {verdict} failures={len(fails)} tags={','.join(tags)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    jobs = []
    if a.what == "controls":
        for suite, group in sorted({(m[1], m[2]) for m in am.MUTANTS}):
            jobs.append((f"control-{suite}-{group or 'all'}", suite, group, [], None))
    else:
        names = list(MUT) if a.what == "all" else a.what.split(",")
        for n in names:
            _, suite, group, edits, exp = MUT[n]
            jobs.append((n, suite, group, edits, exp))
    with cf.ThreadPoolExecutor(max_workers=min(a.jobs, 4)) as ex:
        for r in ex.map(lambda j: run(*j), jobs):
            print(r, flush=True)


if __name__ == "__main__":
    main()
