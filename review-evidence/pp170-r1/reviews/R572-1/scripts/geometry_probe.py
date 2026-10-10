#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Disposable probe: tb/name_state at the shipping name capacity.

The suite's harness sets DESC_NAME_ENTRIES_P to 128; the parent binds it to
the generated inventory (39 at 1x1 TDM8, 107 at 8x8). This builds isolated
copies with the capacity set to CAP and an optional capacity-boundary edit
(the last ordinal loses its trigger: `< N_NAME_P` becomes `< N_NAME_P - 1`),
and runs the unmodified suite (`all`) on the synthetic population, plus the
--measure report at the exact capacity.

Usage: geometry_probe.py --root <export> --output <new dir> [--verilator V]
"""
import argparse, json, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

EDIT = ("hdl/aecp/KL_aecp_nvm_writer.sv",
        "    if (nchg_i && (32'(nchg_ord_i) < N_NAME_P)) begin\n",
        "    if (nchg_i && (32'(nchg_ord_i) < N_NAME_P - 1)) begin\n")

VARIANTS = [  # name, capacity, aaf, boundary edit
    ("cap128_golden_1x1", 128, 1, False),
    ("cap128_boundary_1x1", 128, 1, True),
    ("cap39_golden_1x1", 39, 1, False),
    ("cap39_boundary_1x1", 39, 1, True),
    ("cap107_golden_8x8", 107, 8, False),
    ("cap107_boundary_8x8", 107, 8, True),
]


def one(args, v):
    name, cap, aaf, edit = v
    work = args.output / name
    work.mkdir(parents=True)
    tree = work / "source"
    skip = shutil.ignore_patterns("obj*", "*.hex", "__pycache__")
    for d in ("hdl", "tb/common", "tb/pp_top", "tb/name_state"):
        shutil.copytree(args.root / d, tree / d, ignore=skip)
    run_py = tree / "tb/name_state/run.py"
    s = run_py.read_text()
    old = '      .DESC_NAME_ENTRIES_P (128),\\n'
    assert s.count(old) == 1, "capacity anchor"
    run_py.write_text(s.replace(old, f'      .DESC_NAME_ENTRIES_P ({cap}),\\n'))
    if edit:
        f, o, n = EDIT
        p = tree / f
        t = p.read_text()
        assert t.count(o) == 1
        p.write_text(t.replace(o, n))
    sys.path.insert(0, str(tree / "tb/name_state"))
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"run_{name}", run_py)
    harness = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(harness)
    import fixture as fx
    binary = harness.build(tree, work, args.verilator)
    wrap = (work / "pp_top_wrap.sv").read_text()
    image = work / f"names-{aaf}.bin"
    image.write_bytes(fx.packer(tree).build(fx.fixture(aaf), lint=False)[0])
    rec = {"capacity_in_wrapper": re.findall(r"DESC_NAME_ENTRIES_P \((\d+)\)", wrap),
           "aaf": aaf, "boundary_edit": edit}
    r = subprocess.run([str(binary), str(image), str(aaf), "all"], cwd=work, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (work / "all.log").write_text(r.stdout)
    rec["all_rc"] = r.returncode
    rec["all_tally"] = (re.search(r"\d+ checks: \d+ PASS, \d+ FAIL", r.stdout) or [None])[0]
    rec["all_fails"] = [l for l in r.stdout.splitlines() if l.startswith("FAIL")][:10]
    if not edit:
        m = subprocess.run([str(binary), str(image), str(aaf), "--measure"], cwd=work, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        (work / "measure.log").write_text(m.stdout)
        rec["measure"] = [l for l in m.stdout.splitlines() if l.startswith("DR3a")]
    print(name, json.dumps(rec), flush=True)
    return name, rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--verilator", default="verilator")
    ap.add_argument("--jobs", type=int, default=3)
    a = ap.parse_args()
    a.root = a.root.resolve(); a.output = a.output.resolve()
    a.output.mkdir(parents=True, exist_ok=False)
    with ThreadPoolExecutor(a.jobs) as pool:
        res = dict(pool.map(lambda v: one(a, v), VARIANTS))
    (a.output / "results.json").write_text(json.dumps(res, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
