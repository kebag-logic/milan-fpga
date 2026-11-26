#!/usr/bin/env python3
"""Run the planted defects of tb/verilator/usbnet/mutants.py in parallel, plus reviewer probes.

Reads the CONTROLS table from the tree under test (it is not modified), plants each
defect in a copy of hdl/usbnet under a scratch directory, builds the named harness
with a bounded per-build job count, and applies the same verdict rule as mutants.py:
a control is caught only when the harness fails AND a FAIL line carries its named text.

Usage: run_mutants_parallel.py TREE SCRATCH VERILATOR WORKERS BUILD_JOBS [--extra]
  TREE       a checkout or export of the head under review
  SCRATCH    disposable directory for planted copies and objects
  --extra    also run the reviewer probes in EXTRA below (expected outcome stated)
Writes one line per control to stdout; exit 0 when every author control is caught
and every reviewer probe has its stated outcome.
"""
import concurrent.futures as cf
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

# reviewer probes: (name, harness, file, old, new, FAIL text, expected 'caught'|'survives')
EXTRA = [
    ("probe_rx_length_rule_removed", "tap", "KL_usbnet_pkg.sv",
     "if (len < 12'(need_octets(h)) || is_unreadable_tag(h)) return RXV_SHAPE;",
     "if (is_unreadable_tag(h)) return RXV_SHAPE;",
     "copied=", "survives"),
    ("probe_tx_length_rule_removed", "tap", "KL_usbnet_pkg.sv",
     "    if (len < 12'(need_octets(h)))                  return TXV_LENGTH;\n", "",
     "verdict", "survives"),
]


def load_controls(tree: Path):
    spec = importlib.util.spec_from_file_location("usbnet_mutants", tree / "tb/verilator/usbnet/mutants.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.CONTROLS


def run_one(tree: Path, scratch: Path, verilator: str, jobs: int, ctl) -> tuple[str, str]:
    name, harness, fname, old, new, want = ctl[:6]
    here = tree / "tb/verilator/usbnet"
    work = scratch / name
    rtl = work / "rtl"
    shutil.rmtree(work, ignore_errors=True)
    shutil.copytree(tree / "hdl/usbnet", rtl)
    src = (rtl / fname).read_text()
    n = src.count(old)
    if n != 1:
        return name, f"NOT APPLIED ({n} matches)"
    (rtl / fname).write_text(src.replace(old, new))
    (work / "obj" / harness).mkdir(parents=True, exist_ok=True)
    vflags = (f"--cc --exe --build -j {jobs} -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL "
              "-Wno-PROCASSINIT -Werror-UNDRIVEN -Werror-MULTIDRIVEN "
              "-CFLAGS \"-std=c++17 -O2 -Wall -Wextra\"")
    p = subprocess.run(["make", "-C", str(here), harness, f"RTL={rtl}", f"OBJ={work / 'obj'}",
                        f"VERILATOR={verilator}", f"VFLAGS={vflags}"], capture_output=True, text=True)
    out = p.stdout + p.stderr
    (work / "log.txt").write_text(out)
    fails = [l for l in out.splitlines() if l.startswith("FAIL ") and ".cpp:" in l]
    if p.returncode == 0:
        return name, "survives (the harness passed)"
    if not fails:
        return name, "NO CHECK RAN (build failed)"
    if not any(want in l for l in fails):
        return name, "caught by another check: " + fails[0]
    return name, "caught"


def main() -> int:
    tree, scratch, verilator = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    workers, jobs = int(sys.argv[4]), int(sys.argv[5])
    extra = "--extra" in sys.argv[6:]
    ctls = [tuple(c) + ("caught",) for c in load_controls(tree)]
    if extra:
        ctls += EXTRA
    expect = {c[0]: c[6] for c in ctls}
    bad = 0
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(run_one, tree, scratch, verilator, jobs, c) for c in ctls]
        results = dict(f.result() for f in futs)
    for c in ctls:
        r = results[c[0]]
        got = "caught" if r == "caught" else ("survives" if r.startswith("survives") else "other")
        ok = got == expect[c[0]]
        bad += not ok
        print(f"{'OK  ' if ok else 'BAD '} expect={expect[c[0]]:8s} {c[0]}: {r}")
    author = [c for c in ctls if c[0] not in {e[0] for e in EXTRA}]
    caught = sum(results[c[0]] == "caught" for c in author)
    print(f"author controls caught by their named check: {caught} of {len(author)}")
    print(f"outcomes as expected: {len(ctls) - bad} of {len(ctls)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
