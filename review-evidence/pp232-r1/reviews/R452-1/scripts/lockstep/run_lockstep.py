#!/usr/bin/env python3
"""Reviewer lockstep campaign: main's KL_aecp_notify beside the candidate.

Usage: run_lockstep.py --repo CLONE --ref MAIN_COMMIT --cand-commit HEAD_COMMIT
                       --work DIR --jobs N [--seeds S] [--cycles C] [--controls]

Builds every shape (and, with --controls, every planted control at 16/2/2),
runs seeds 1..S in protocol mode (odd seeds) and fully random mode (even seeds),
and prints one line per run plus a summary. Exit 0 only when every head run has
zero mismatches and every control is caught by at least one run.
"""
import argparse
import concurrent.futures as cf
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHAPES = [  # N_CTRL, N_IN, N_OUT, IDENT
    (16, 2, 2, 0), (16, 9, 9, 0), (2, 1, 1, 0), (16, 2, 2, 1), (5, 8, 8, 0),
    (1, 1, 1, 0), (3, 1, 2, 1),
]


def build(repo, ref, cand, shape, obj):
    n, i, o, d = shape
    subprocess.run([str(HERE / "build.sh"), repo, ref, str(cand), str(n), str(i), str(o),
                    str(d), str(obj)], check=True, stdout=subprocess.DEVNULL)
    return obj / "Vlockstep"


def run(binary, seed, cycles):
    mode = seed % 2 == 0
    p = subprocess.run([str(binary), str(seed), str(cycles), str(int(mode))],
                       capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--cand-commit", required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--seeds", type=int, default=16)
    ap.add_argument("--cycles", type=int, default=2_000_000)
    ap.add_argument("--control-seeds", type=int, default=8)
    ap.add_argument("--controls", action="store_true")
    a = ap.parse_args()
    a.work.mkdir(parents=True, exist_ok=True)
    cand = a.work / "cand.sv"
    cand.write_bytes(subprocess.run(["git", "-C", a.repo, "show",
                                     f"{a.cand_commit}:hdl/aecp/KL_aecp_notify.sv"],
                                    check=True, capture_output=True).stdout)
    targets = {}
    for s in SHAPES:
        targets["head_%d_%d_%d_%d" % s] = (cand, s)
    if a.controls:
        subprocess.run([sys.executable, str(HERE / "plant.py"), str(cand), str(a.work / "controls")],
                       check=True, stdout=subprocess.DEVNULL)
        for f in sorted((a.work / "controls").glob("*.sv")):
            targets["ctl_" + f.stem] = (f, SHAPES[0])
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        futs = {k: ex.submit(build, a.repo, a.ref, c, s, a.work / k) for k, (c, s) in targets.items()}
        bins = {k: f.result() for k, f in futs.items()}
    print(f"built {len(bins)} targets", flush=True)
    jobs = []
    for k, b in bins.items():
        seeds = a.seeds if k.startswith("head_") else a.control_seeds
        for seed in range(1, seeds + 1):
            jobs.append((k, b, seed))
    results = {}
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        futs = {ex.submit(run, b, seed, a.cycles): (k, seed) for k, b, seed in jobs}
        for f in cf.as_completed(futs):
            k, seed = futs[f]
            results[(k, seed)] = f.result()
    ok = True
    for k in bins:
        runs = sorted((s, r) for (kk, s), r in results.items() if kk == k)
        caught = sum(1 for _, r in runs if r[0] == 1)
        bad = sum(1 for _, r in runs if r[0] not in (0, 1))
        for s, (rc, out, err) in runs:
            print(f"{k} rc={rc} {out}")
            if err and k.startswith("head_"):
                print("   " + err.replace("\n", "\n   "))
        if k.startswith("head_"):
            verdict = "PASS" if caught == 0 and bad == 0 else "FAIL"
        else:
            verdict = "CAUGHT" if caught > 0 and bad == 0 else "MISSED"
        ok &= verdict in ("PASS", "CAUGHT")
        print(f"SUMMARY {k}: {len(runs)} runs x {a.cycles} cycles, {caught} with mismatches, "
              f"{bad} errored -> {verdict}", flush=True)
    print("LOCKSTEP " + ("OK" if ok else "NOT OK"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
