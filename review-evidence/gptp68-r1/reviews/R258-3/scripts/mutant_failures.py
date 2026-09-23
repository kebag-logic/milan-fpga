#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Per-check attribution for generator mutants and older generators.

For every generator mutant of the tree's own #68 list, every reviewer mutant
(mutant_slices.REVIEWER_MUTATIONS) and every extra generator given, build
the suite's shipping image (--clk-hz 2000000 --cease-ms 3000) and run ONE
prebuilt harness executable (the head's sim_main.cpp against the head RTL)
on it. Record the tally line and every FAIL line. A generator mutant moves
only the ROM image, so one executable serves every row, as mutants.py does.

usage: mutant_failures.py <tree> <harness-exe> <out-dir> [label=gen.py ...]
Runs at most 8 harnesses at once.
"""
from __future__ import annotations

import concurrent.futures as cf
import importlib.util
import subprocess
import sys
from pathlib import Path

GENARGS = ["--clk-hz", "2000000", "--cease-ms", "3000"]
HERE = Path(__file__).resolve().parent


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def one(label: str, gen_text: str, exe: Path, out: Path) -> str:
    tag = "".join(c if c.isalnum() else "_" for c in label)[:60]
    d = out / tag
    d.mkdir(parents=True, exist_ok=True)
    (d / "gen.py").write_text(gen_text, encoding="utf-8")
    g = subprocess.run([sys.executable, str(d / "gen.py"), *GENARGS,
                        "-o", str(d / "gptp_ucode.hex")],
                       capture_output=True, text=True)
    if g.returncode != 0:
        return f"### {label}\nGENERATOR REFUSED\n{g.stderr[-400:]}\n"
    r = subprocess.run([str(exe)], cwd=str(d), capture_output=True, text=True)
    text = r.stdout + r.stderr
    (d / "run.log").write_text(text, encoding="utf-8")
    lines = text.splitlines()
    fails = [ln for ln in lines if ln.startswith("FAIL")]
    tally = [ln for ln in lines if " checks: " in ln]
    body = "\n".join(fails)
    return (f"### {label}\nexit {r.returncode}; "
            f"{tally[-1] if tally else 'NO TALLY'}\n{body}\n")


def main() -> int:
    tree = Path(sys.argv[1]).resolve()
    exe = Path(sys.argv[2]).resolve()
    out = Path(sys.argv[3]).resolve()
    extra = sys.argv[4:]
    gen_path = tree / "hdl/ucode/gen_gptp_ucode.py"
    src = gen_path.read_text(encoding="utf-8")
    own = load(tree / "tb/verilator/engine/mutants.py", "own_mutants")
    rev = load(HERE / "mutant_slices.py", "rev_mutants")
    jobs = [("control (head generator)", src)]
    start = next(i for i, m in enumerate(own.MUTATIONS)
                 if m[0] == "every pair uses the locked threshold")
    for name, fname, pat, rep, _ in own.MUTATIONS[start:]:
        assert fname == own.GENERATOR and src.count(pat) == 1, name
        jobs.append((f"own: {name}", src.replace(pat, rep)))
    for name, fname, pat, rep, _ in rev.REVIEWER_MUTATIONS:
        assert src.count(pat) == 1, name
        jobs.append((f"reviewer: {name}", src.replace(pat, rep)))
    for spec in extra:
        label, path = spec.split("=", 1)
        jobs.append((f"generator: {label}",
                     Path(path).read_text(encoding="utf-8")))
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(lambda j: one(j[0], j[1], exe, out), jobs))
    for r in results:
        print(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
