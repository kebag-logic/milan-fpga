#!/usr/bin/env python3
"""Run the engine mutation arm's control and a chosen subset of its mutants.

usage: arm_subset.py <repo root> <work dir> <jobs> <index>...
Index 0 is the unmutated control (mutants.main()'s own steps); index k>0 is
MUTATIONS[k-1], run through the arm's own run_mutant(). Each job prints its
verdict lines; the summary tallies PASS/FAIL. Exit 1 on any FAIL.
"""
import concurrent.futures as cf, contextlib, importlib.util, io, sys, time
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
WORK = Path(sys.argv[2]).resolve()
_M = {}

def mod():
    if "m" not in _M:
        eng = ROOT / "tb/verilator/engine"
        sys.path.insert(0, str(eng)); sys.path.insert(0, str(ROOT / "tb/verilator"))
        spec = importlib.util.spec_from_file_location("mutants", eng / "mutants.py")
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        _M["m"] = m
    return _M["m"]

def job(k):
    m = mod()
    w = WORK / f"job{k:03d}"; w.mkdir(parents=True, exist_ok=True)
    t0 = time.monotonic(); out = io.StringIO()
    with contextlib.redirect_stdout(out):
        src = m.stage(w, "clean"); exe = m.build(src, w, "clean")
        if k == 0:
            run = w / "run_clean"
            if exe is None or not m.generate_image(src, run):
                ok = False; print("[FAIL] control did not build")
            else:
                ans = m.verdict(*m.run_harness(exe, run)); ok = ans == "pass"
                print(f"[{'PASS' if ok else 'FAIL'}] the unmutated engine: {ans}")
        else:
            ok = m.run_mutant(w, exe, m.MUTATIONS[k - 1])
    name = "control" if k == 0 else m.MUTATIONS[k - 1][0]
    return k, name, ok, time.monotonic() - t0, out.getvalue()

if __name__ == "__main__":
    jobs = int(sys.argv[3]); idx = [int(x) for x in sys.argv[4:]]
    res = []
    with cf.ProcessPoolExecutor(max_workers=jobs) as ex:
        for k, name, ok, s, text in ex.map(job, idx):
            res.append(ok)
            print(f"## {k:03d} {'ok' if ok else 'FAIL'}: {name} ({s:.1f} s)")
            for line in text.splitlines():
                if line.startswith("[") or line.startswith("FAIL "):
                    print("    " + line)
            sys.stdout.flush()
    print(f"\n{len(res)} checks: {sum(res)} PASS, {len(res) - sum(res)} FAIL")
    sys.exit(0 if all(res) else 1)
