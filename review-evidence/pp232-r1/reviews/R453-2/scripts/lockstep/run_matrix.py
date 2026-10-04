#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Build and run the reviewer lockstep bench over shapes x modes x seeds, and the
planted controls; write one TSV row per run and a summary.

Usage: run_matrix.py --ref REF.sv --cand CAND.sv --pkg PKG.sv --controls DIR
                     --work DIR --out TSV [--cycles N] [--seeds N] [--jobs N]
"""
import argparse
import concurrent.futures as cf
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHAPES = [  # N_CTRL, N_SI, N_SO, IDENT
    (16, 8, 8, 0), (16, 2, 2, 0), (16, 2, 2, 1), (16, 9, 9, 0),
    (2, 1, 1, 0), (5, 8, 8, 0), (8, 3, 5, 1), (3, 1, 2, 0), (1, 1, 1, 0),
]
MODES = (0, 1, 2, 3)


def build(work: Path, name: str, cand: Path, ref: Path, pkg: Path, shape) -> tuple[str, int]:
    out = work / name
    r = subprocess.run([str(HERE / "build.sh"), str(out), str(cand), str(ref), str(pkg),
                        *map(str, shape)], capture_output=True, text=True)
    return name, r.returncode


def run(work: Path, name: str, seed: int, mode: int, cycles: int, nctrl: int) -> dict:
    exe = work / name / "obj" / "Vlk_top"
    r = subprocess.run([str(exe), str(seed), str(cycles), str(mode), str(nctrl)],
                       cwd=work / name, capture_output=True, text=True)
    m = re.search(r"^mismatches (\d+)", r.stdout, re.M)
    cov = re.search(r"^coverage: (.*)$", r.stdout, re.M)
    log = work / name / f"run_s{seed}_m{mode}.log"
    log.write_text(r.stdout + r.stderr)
    return {"name": name, "seed": seed, "mode": mode, "rc": r.returncode,
            "mism": int(m.group(1)) if m else -1, "cov": cov.group(1) if cov else ""}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", type=Path, required=True)
    ap.add_argument("--cand", type=Path, required=True)
    ap.add_argument("--pkg", type=Path, required=True)
    ap.add_argument("--controls", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--cycles", type=int, default=2_000_000)
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--control-seeds", type=int, default=4)
    ap.add_argument("--jobs", type=int, default=8)
    a = ap.parse_args()
    a.work.mkdir(parents=True, exist_ok=True)

    builds = []
    for s in SHAPES:
        builds.append((f"cand_{s[0]}_{s[1]}_{s[2]}_{s[3]}", a.cand, s))
    ctrl_shape = (16, 2, 2, 0)
    controls = sorted(a.controls.glob("*.sv"))
    for c in controls:
        builds.append((f"ctl_{c.stem}", c, ctrl_shape))

    with cf.ThreadPoolExecutor(a.jobs) as ex:
        res = list(ex.map(lambda b: build(a.work, b[0], b[1], a.ref, a.pkg, b[2]), builds))
    bad = [n for n, rc in res if rc != 0]
    for n in bad:
        print(f"BUILD FAILED {n}")

    jobs = []
    for name, _, shape in builds:
        if name in bad:
            continue
        seeds = a.seeds if name.startswith("cand_") else a.control_seeds
        for mode in MODES:
            for seed in range(1, seeds + 1):
                jobs.append((name, 1000 * mode + seed, mode, shape[0]))
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        rows = list(ex.map(lambda j: run(a.work, j[0], j[1], j[2], a.cycles, j[3]), jobs))

    with a.out.open("w") as f:
        f.write("name\tseed\tmode\tcycles\trc\tmismatches\tcoverage\n")
        for r in rows:
            f.write(f"{r['name']}\t{r['seed']}\t{r['mode']}\t{a.cycles}\t{r['rc']}\t{r['mism']}\t{r['cov']}\n")

    ok = not bad
    print("== candidate (must match every run)")
    for name, _, _ in builds:
        if not name.startswith("cand_"):
            continue
        rr = [r for r in rows if r["name"] == name]
        mm = sum(1 for r in rr if r["rc"] != 0 or r["mism"] != 0)
        print(f"{name}: {len(rr)} runs, {mm} with a mismatch or error")
        ok &= mm == 0 and len(rr) > 0
    print("== controls (each must be caught)")
    for name, _, _ in builds:
        if not name.startswith("ctl_"):
            continue
        rr = [r for r in rows if r["name"] == name]
        caught = [r for r in rr if r["rc"] == 1 and r["mism"] > 0]
        errs = [r for r in rr if r["rc"] not in (0, 1)]
        tot = sum(r["mism"] for r in caught)
        by_mode = {m: sum(1 for r in caught if r["mode"] == m) for m in MODES}
        verdict = "CAUGHT" if caught and not errs else "SURVIVED" if not errs else "ERROR"
        print(f"{name}: {verdict} {len(caught)}/{len(rr)} runs, {tot} mismatches, by mode {by_mode}")
        ok &= verdict == "CAUGHT"
    print("OVERALL", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
