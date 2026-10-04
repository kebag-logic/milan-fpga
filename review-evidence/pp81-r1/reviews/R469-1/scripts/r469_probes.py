#!/usr/bin/env python3
"""[R469] disposable fault probes against tb/pp_top at an exact processor head.

Each probe copies hdl/ and tb/{common,ucpu,pp_top} of SRC (an extracted tree of
the head under review) into a scratch directory of its own, applies one patch
from PROBES with `git apply`, builds and runs one tb/pp_top make target, and
records the return code, every FAIL: line and the section summary lines. The
source tree is never written. Usage:

  VERILATOR=/path/to/verilator-5.050 \
  python3 r469_probes.py --src TREE --scratch DIR --out RECEIPTS --jobs N \
      [name:target ...]

`name` is a patch stem under ../probes, or `control` for no patch. The
expectation column is the reviewer's hypothesis; the verdict is what ran.
"""
import argparse
import concurrent.futures as cf
import os
import shutil
import subprocess
import time
from pathlib import Path

PROBES = Path(__file__).resolve().parent.parent / "probes"
SUITES = ("common", "ucpu", "pp_top")


def trial(src: Path, scratch: Path, out: Path, name: str, target: str) -> str:
    tree = scratch / f"{name}--{target}"
    if tree.exists():
        shutil.rmtree(tree)
    tree.mkdir(parents=True)
    shutil.copytree(src / "hdl", tree / "hdl")
    for s in SUITES:
        shutil.copytree(src / "tb" / s, tree / "tb" / s,
                        ignore=shutil.ignore_patterns("obj_*", "*.hex", "__pycache__"))
    log = out / f"{name}--{target}.log"
    with log.open("w") as fh:
        if name != "control":
            patch = PROBES / f"{name}.patch"
            r = subprocess.run(["git", "apply", "--check", str(patch)], cwd=tree,
                               stdout=fh, stderr=subprocess.STDOUT)
            if r.returncode:
                return f"{name} {target}: PATCH-REFUSED"
            subprocess.run(["git", "apply", str(patch)], cwd=tree, check=True)
        t0 = time.time()
        r = subprocess.run(["make", "-C", str(tree / "tb" / "pp_top"), target],
                           stdout=fh, stderr=subprocess.STDOUT)
        dt = time.time() - t0
    text = log.read_text(errors="replace").splitlines()
    fails = [l for l in text if l.startswith("FAIL:")]
    summ = [l for l in text if l.startswith(("TD:", "HZ:", "  [TD]", "[build"))]
    tally = any("checks" in l for l in text)
    lines = [f"{name} {target}: rc={r.returncode} tally={'yes' if tally else 'no'} "
             f"fails={len(fails)} wall={dt:.0f}s"]
    lines += [f"    {l}" for l in summ]
    lines += [f"    {l[:300]}" for l in fails]
    shutil.rmtree(tree, ignore_errors=True)
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", type=Path, required=True)
    ap.add_argument("--scratch", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("units", nargs="+")
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    a.scratch.mkdir(parents=True, exist_ok=True)
    print("VERILATOR=" + os.environ.get("VERILATOR", "verilator"), flush=True)
    units = [u.split(":", 1) for u in a.units]
    with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        futs = [ex.submit(trial, a.src, a.scratch, a.out, n, t) for n, t in units]
        for f in futs:
            print(f.result(), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
