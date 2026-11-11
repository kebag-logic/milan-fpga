#!/usr/bin/env python3
"""Run a shard (or a named subset) of tb/verilator/mbx/mutants.py's arms, or
reviewer probe arms from a JSON file, with the driver's own plant/build/run
functions. Each Verilator build uses one compile job so that --jobs bounds the
host's parallel processes.

Usage (from anywhere; paths are arguments):
  python3 -B run_arms.py --tree <clone> --shard I/N --jobs J [--controls]
  python3 -B run_arms.py --tree <clone> --names a,b,c --jobs J
  python3 -B run_arms.py --tree <clone> --probes probes.json --jobs J

Probe arms are judged inverted from the driver's arms only in reporting: a
probe prints CAUGHT when the suite fails with rc 1 and any [FAIL] line, and
ESCAPED otherwise, together with every failing check's label.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", type=Path, required=True)
    ap.add_argument("--shard")
    ap.add_argument("--names")
    ap.add_argument("--probes", type=Path)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--controls", action="store_true")
    ap.add_argument("--scratch", type=Path, required=True)
    a = ap.parse_args()
    sys.path.insert(0, str(a.tree / "tb" / "verilator" / "mbx"))
    import mutants as m  # noqa: E402

    orig_recipe = m.recipe

    def recipe_one_job() -> list[str]:
        argv = orig_recipe()
        out = []
        skip = False
        for i, w in enumerate(argv):
            if skip:
                skip = False
                continue
            if w == "-j":
                out += ["-j", "1"]
                skip = True
                continue
            out.append(w)
        return out

    m.recipe = recipe_one_job
    orig_bar = m.build_and_run

    def build_and_run(rtl_dir, work, host, ifs=1):
        # the driver appends "-j 4"; rewrite to 1 job
        import subprocess
        work.mkdir(parents=True, exist_ok=True)
        argv = m.recipe()
        if ifs != 1:
            include = f"-I{m.CONTRACT_INC}"
            argv = [w.replace(include, f"-I{rtl_dir}") for w in argv]
        argv += [f"-GHOST_P={host}", "--Mdir", str(work / "obj"), "-j", "1",
                 *[str(rtl_dir / f) for f in m.RTL_FILES], "tb_mbx_top.sv", "sim_main.cpp", "-o", "Vmbx"]
        built = subprocess.run(argv, cwd=m.HERE, capture_output=True, text=True, check=False)
        if built.returncode != 0:
            return 2, built.stdout + built.stderr
        ran = subprocess.run([str(work / "obj" / "Vmbx"), str(host)], capture_output=True, text=True, check=False)
        return ran.returncode, ran.stdout + ran.stderr

    m.build_and_run = build_and_run

    probe = False
    if a.probes:
        probe = True
        arms = tuple(m.Arm(**d) for d in json.loads(a.probes.read_text()))
    elif a.names:
        want = a.names.split(",")
        arms = tuple(x for x in m.ARMS if x.name in want)
    else:
        i, n = (int(v) for v in a.shard.split("/"))
        arms = tuple(x for k, x in enumerate(m.ARMS) if k % n == i)
    a.scratch.mkdir(parents=True, exist_ok=True)
    bad = 0
    with tempfile.TemporaryDirectory(prefix="arms-", dir=a.scratch) as tmp:
        root = Path(tmp)
        if a.controls:
            for ifs in sorted({1} | {x.ifs for x in m.ARMS}):
                rtl = m.RTL
                if ifs != 1:
                    rtl = root / f"control-if{ifs}" / "rtl"
                    import shutil
                    shutil.copytree(m.RTL, rtl)
                    m.variant(rtl, ifs)
                for host in (0, 1):
                    rc, log = build_and_run(rtl, root / f"control-if{ifs}-{host}", host, ifs)
                    tally = [ln for ln in log.splitlines() if "checks:" in ln]
                    print(f"[{'ok' if rc == 0 else 'FAIL'}] positive control, {ifs} if, host {host}: "
                          f"{tally[-1] if tally else log[-200:]}", flush=True)
                    bad += rc != 0

        def one(arm):
            copy = m.plant(arm, root)
            rc, log = build_and_run(copy, root / arm.name, arm.host, arm.ifs)
            fails = [ln.strip() for ln in log.splitlines() if "[FAIL]" in ln]
            return arm, rc, fails, log

        with ThreadPoolExecutor(max_workers=a.jobs) as pool:
            for arm, rc, fails, log in pool.map(one, arms):
                if probe:
                    caught = rc == 1 and bool(fails)
                    print(f"[{'CAUGHT' if caught else 'ESCAPED'}] probe {arm.name} rc={rc}", flush=True)
                    for f in fails:
                        print(f"    {f}", flush=True)
                    if rc not in (0, 1):
                        print("    " + "\n    ".join(log.strip().splitlines()[-8:]), flush=True)
                else:
                    caught = rc == 1 and any(arm.needle in ln for ln in fails)
                    print(f"[{'ok' if caught else 'ESCAPED'}] {arm.name}: rc={rc} {len(fails)} failed; "
                          f"first: {fails[0] if fails else 'none'}", flush=True)
                    bad += not caught
        print(f"arms: {len(arms) - (0 if probe else bad)} of {len(arms)} {'run' if probe else 'caught'}", flush=True)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
