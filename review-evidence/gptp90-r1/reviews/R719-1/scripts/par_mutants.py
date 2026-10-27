#!/usr/bin/env python3
"""Run a tree's engine mutation arm in parallel and record, per control,
its verdict and every FAIL line it produced.

Usage: par_mutants.py <tree> <outdir> [--jobs N]

<tree> is an exported source tree (tb/verilator/engine/mutants.py inside).
The tree's own mutants.py supplies MUTATIONS, stage(), generate_image(),
build(), run_harness(), verdict() and named_verdict(); this script only
schedules them concurrently and keeps each control's raw output. The
`verilator` on PATH is used, exactly as the tree's driver uses it.
"""
import argparse
import contextlib
import importlib.util
import io
import json
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def load(tree: Path):
    path = tree / "tb/verilator/engine/mutants.py"
    spec = importlib.util.spec_from_file_location("tree_mutants", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tree", type=Path)
    ap.add_argument("outdir", type=Path)
    ap.add_argument("--jobs", type=int, default=12)
    a = ap.parse_args()
    m = load(a.tree.resolve())
    out = a.outdir.resolve()
    (out / "controls").mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="parmut-", dir=str(out)))

    clean_src = m.stage(work, "clean")
    clean_run = work / "run_clean"
    clean_exe = m.build(clean_src, work, "clean")
    assert clean_exe is not None and m.generate_image(clean_src, clean_run)
    rc, output = m.run_harness(clean_exe, clean_run)
    clean_answer = m.verdict(rc, output)
    (out / "controls" / "000_clean.log").write_text(output)
    print(f"clean: {clean_answer}", flush=True)

    def one(i_mut):
        i, mut = i_mut
        name, fname, pattern, replacement, breaks = mut
        tag = f"{i + 1:03d}"
        rec = {"index": i + 1, "name": name, "file": fname,
               "breaks": breaks.split(" | ")}
        src = (m.HDL / fname).read_text(encoding="utf-8")
        if src.count(pattern) != 1:
            rec["answer"] = f"pattern count {src.count(pattern)}"
            return rec
        srcdir = m.stage(work, tag, (fname, pattern, replacement))
        rundir = work / f"run_{tag}"
        if not m.generate_image(srcdir, rundir):
            rec["answer"] = "generator refused"
            return rec
        exe = clean_exe if fname == m.GENERATOR else m.build(srcdir, work, tag)
        if exe is None:
            rec["answer"] = "did not build"
            return rec
        rc, output = m.run_harness(exe, rundir)
        # the tree's named_verdict() prints; its rule is re-applied here
        # per named check instead, so concurrent output stays separable
        answer = m.verdict(rc, output)
        failed = [l for l in output.splitlines() if l.startswith("FAIL ")]
        missed = []
        if answer == "caught":
            for want in rec["breaks"]:
                if want.startswith("slew:"):
                    hit = any(l.startswith("FAIL ") and want in l and
                              not l.startswith("FAIL " + m.P1_PREFIX)
                              for l in failed)
                    # the tree's rule checks only the whole breaks string
                    # for slew: controls; record each name anyway
                else:
                    hit = m._named_failure(failed, want) is not None
                if not hit:
                    missed.append(want)
        rec["answer"] = answer
        rec["named_missed"] = missed
        rec["fail_lines"] = failed
        (out / "controls" / f"{tag}.log").write_text(
            f"# {name}\n# {fname}\n# breaks: {breaks}\n{output}")
        print(f"{tag} {answer} missed={len(missed)} {name}", flush=True)
        return rec

    with ThreadPoolExecutor(max_workers=a.jobs) as ex:
        recs = list(ex.map(one, enumerate(m.MUTATIONS)))
    summary = {"clean": clean_answer, "controls": recs,
               "total": len(recs),
               "caught": sum(r.get("answer") == "caught" for r in recs)}
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    bad = [r for r in recs if r.get("answer") != "caught" or r.get("named_missed")]
    print(f"clean={clean_answer} controls={len(recs)} caught={summary['caught']} "
          f"not-clean={len(bad)}")
    for r in bad:
        print("NOT CLEAN", r["index"], r["name"], r.get("answer"),
              r.get("named_missed"))
    return 0 if clean_answer == "pass" and not bad else 1


if __name__ == "__main__":
    sys.exit(main())
