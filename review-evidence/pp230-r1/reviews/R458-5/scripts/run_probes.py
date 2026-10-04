#!/usr/bin/env python3
"""Run each R458-5 probe in a scratch copy of its own and record which checks fail.

usage: run_probes.py <tree> <probe-dir> <scratch-dir> <receipt-dir> [--jobs N]
VERILATOR (the pinned 5.050) is taken from the environment. A probe is
KILLED when its suite exits non-zero with a FAIL line and no build error;
the per-shape FAIL tags are printed so the shapes that catch it are visible.
"""
import argparse
import concurrent.futures as cf
import re
import shutil
import subprocess
from pathlib import Path

# which suite runs see each probe (suite dir, RUN_ARGS)
SUITES = {
    "wid": [("srp_stream_fsms", "walk")], "wtsp": [("srp_stream_fsms", "walk")],
    "wsid": [("srp_stream_fsms", "walk")], "tf": [("srp_top", "storage")],
    "granted": [("srp_admission", "")],
    "eq": [("srp_stream_fsms", ""), ("srp_top", ""), ("srp_admission", "")],
}


def suites_for(name: str):
    key = name.split("-")[1]
    return SUITES[key]


def one(args, patch: Path):
    name = patch.stem
    tree = Path(args.scratch) / name
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(Path(args.tree) / "hdl", tree / "hdl")
    for d in ("common", "srp_top", "srp_stream_fsms", "srp_admission"):
        shutil.copytree(Path(args.tree) / "tb" / d, tree / "tb" / d,
                        ignore=shutil.ignore_patterns("obj_*"))
    subprocess.run(["git", "apply", "--check", str(patch)], cwd=tree, check=True)
    subprocess.run(["git", "apply", str(patch)], cwd=tree, check=True)
    lines = []
    worst = 0
    for suite, group in suites_for(name):
        log = Path(args.receipts) / f"{name}.{suite}.log"
        with log.open("w") as f:
            r = subprocess.run(["make", "-C", str(tree / "tb" / suite), "RUN_ARGS=" + group],
                               stdout=f, stderr=subprocess.STDOUT, check=False)
        text = log.read_text()
        fails = [l for l in text.splitlines() if l.startswith("FAIL")]
        tags = sorted({re.sub(r"^FAIL:\s*", "", l).split(":")[0].split(" ")[0] + " "
                       + (re.search(r"\[(\d+/\d+)\]", l).group(1) if re.search(r"\[(\d+/\d+)\]", l) else "-")
                       for l in fails})
        tallies = re.findall(r"^(\d+) checks: (\d+) PASS, (\d+) FAIL", text, re.M)
        builderr = "%Error" in text
        lines.append(f"  {suite}/{group or 'all'}: rc={r.returncode} fails={len(fails)} "
                     f"builderr={builderr} tallies={tallies} tags={tags}")
        worst = max(worst, r.returncode)
    shutil.rmtree(tree, ignore_errors=True)
    return name, worst, lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tree"); ap.add_argument("probes"); ap.add_argument("scratch"); ap.add_argument("receipts")
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    Path(args.receipts).mkdir(parents=True, exist_ok=True)
    patches = sorted(Path(args.probes).glob("*.patch"))
    with cf.ThreadPoolExecutor(args.jobs) as ex:
        for name, rc, lines in ex.map(lambda p: one(args, p), patches):
            verdict = "SURVIVED" if rc == 0 else "FAILED-SUITE"
            print(f"{name}: {verdict} rc={rc}", flush=True)
            for l in lines:
                print(l, flush=True)


if __name__ == "__main__":
    main()
