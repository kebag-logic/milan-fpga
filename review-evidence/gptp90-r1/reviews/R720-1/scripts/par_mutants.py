#!/usr/bin/env python3
"""Run the engine mutation arm of a FPGA-gPTP tree in parallel.

Usage: par_mutants.py TREE OUTDIR JOBS [--probes PROBES.py] [--only-probes]

TREE is an extracted source tree (never the review clone). The positive
control is built and run once; each mutant then runs through the tree's own
mutants.run_mutant(), so planting, image generation, harness runs and the
named-check verdict are exactly the tree's own logic. Only the scheduling is
parallel. PROBES.py, when given, defines REVIEWER_MUTATIONS in the same
5-tuple shape; those run as well and are reported separately.

Writes OUTDIR/<index>-<slug>.log per mutant and OUTDIR/summary.tsv.
Exit 0 only when the control passes and every mutant is caught.
"""
import contextlib
import importlib.util
import io
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
JOBS = int(sys.argv[3])
PROBES = None
ONLY_PROBES = "--only-probes" in sys.argv
if "--probes" in sys.argv:
    PROBES = Path(sys.argv[sys.argv.index("--probes") + 1]).resolve()

MUT_PATH = TREE / "tb/verilator/engine/mutants.py"


def load_mutants():
    spec = importlib.util.spec_from_file_location("mutants", MUT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def slug(s):
    return "".join(c if c.isalnum() else "_" for c in s)[:60]


def worker(args):
    idx, kind, mutation, work, clean_exe = args
    m = load_mutants()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            ok = m.run_mutant(Path(work), Path(clean_exe), mutation)
        except Exception as e:  # report, never hide
            print(f"[FAIL] exception {e!r}")
            ok = False
    log = OUT / f"{kind}-{idx:03d}-{slug(mutation[0])}.log"
    log.write_text(buf.getvalue(), encoding="utf-8")
    return idx, kind, mutation[0], ok, log.name


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    m = load_mutants()
    todo = []
    if not ONLY_PROBES:
        todo += [("author", i, mu) for i, mu in enumerate(m.MUTATIONS)]
    if PROBES:
        spec = importlib.util.spec_from_file_location("probes", PROBES)
        pm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pm)
        todo += [("probe", i, mu)
                 for i, mu in enumerate(pm.REVIEWER_MUTATIONS)]
    with tempfile.TemporaryDirectory(prefix="r720-mut-",
                                     dir=str(TREE.parent)) as td:
        work = Path(td)
        clean_src = m.stage(work, "clean")
        clean_run = work / "run_clean"
        clean_exe = m.build(clean_src, work, "clean")
        if clean_exe is None or not m.generate_image(clean_src, clean_run):
            print("CONTROL did not build")
            return 1
        rc, out = m.run_harness(clean_exe, clean_run)
        ans = m.verdict(rc, out)
        (OUT / "control.log").write_text(out, encoding="utf-8")
        print(f"CONTROL {ans}", flush=True)
        rows = []
        with ProcessPoolExecutor(max_workers=JOBS) as ex:
            futs = [ex.submit(worker, (i, kind, mu, str(work), str(clean_exe)))
                    for kind, i, mu in todo]
            for f in as_completed(futs):
                idx, kind, name, ok, log = f.result()
                rows.append((kind, idx, name, "caught" if ok else "NOT-CAUGHT",
                             log))
                print(f"{kind} {idx:3d} {'caught' if ok else 'NOT-CAUGHT'} "
                      f"{name}", flush=True)
    rows.sort()
    with open(OUT / "summary.tsv", "w", encoding="utf-8") as fh:
        fh.write(f"control\t-\tunmutated\t{ans}\tcontrol.log\n")
        for r in rows:
            fh.write("\t".join(str(x) for x in r) + "\n")
    a = [r for r in rows if r[0] == "author"]
    p = [r for r in rows if r[0] == "probe"]
    print(f"control={ans} author={sum(r[3]=='caught' for r in a)}/{len(a)} "
          f"probes caught={sum(r[3]=='caught' for r in p)}/{len(p)}")
    bad = ans != "pass" or any(r[3] != "caught" for r in a)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
