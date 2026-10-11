#!/usr/bin/env python3
"""Usage: python3 engine_mutants_parallel.py <tree-root> [jobs]

Runs the exact-head tb/verilator/engine/mutants.py arm with its own stage,
generate_image, build, run_harness and verdict functions, but executes the
control and each mutant concurrently. The per-mutant decision logic mirrors
mutants.main() line for line; only scheduling differs. Exit 0 only when the
control passes and every mutant is caught.
"""
import importlib.util
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

root = Path(sys.argv[1]).resolve()
jobs = int(sys.argv[2]) if len(sys.argv) > 2 else 10
spec = importlib.util.spec_from_file_location(
    "engine_mutants", root / "tb/verilator/engine/mutants.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def one(work, clean_exe, item):
    name, fname, pattern, replacement, breaks = item
    src = (m.HDL / fname).read_text(encoding="utf-8")
    if src.count(pattern) != 1:
        return False, f"[FAIL] mutation {name!r}: pattern count {src.count(pattern)}"
    tag = "".join(c if c.isalnum() else "_" for c in name)
    srcdir = m.stage(work, tag, (fname, pattern, replacement))
    rundir = work / f"run_{tag}"
    if not m.generate_image(srcdir, rundir):
        return False, f"[FAIL] mutation {name!r}: the generator refused its image"
    exe = clean_exe if fname == m.GENERATOR else m.build(srcdir, work, tag)
    if exe is None:
        return False, f"[FAIL] mutation {name!r} did not build"
    rc, output = m.run_harness(exe, rundir)
    answer = m.verdict(rc, output)
    extra = ""
    if breaks.startswith("slew:") and answer == "caught":
        named = [ln for ln in output.splitlines()
                 if ln.startswith("FAIL ") and breaks in ln]
        if not named:
            answer = "missed its named check"
        else:
            extra = named[0] + "\n"
    if answer == "caught":
        return True, f"{extra}[PASS] mutant caught: {name} - breaks \"{breaks}\""
    if answer == "pass":
        return False, f"[FAIL] mutant SURVIVED: {name}. \"{breaks}\""
    return False, f"[FAIL] mutant {name!r} {answer}"


def main() -> int:
    passes = fails = 0
    with tempfile.TemporaryDirectory(prefix="engine-mutants-par-") as td:
        work = Path(td)
        clean_src = m.stage(work, "clean")
        clean_run = work / "run_clean"
        clean_exe = m.build(clean_src, work, "clean")
        if clean_exe is None or not m.generate_image(clean_src, clean_run):
            print("[FAIL] the unmutated sources did not build")
            return 1
        with ThreadPoolExecutor(max_workers=jobs) as ex:
            ctl = ex.submit(m.run_harness, clean_exe, clean_run)
            futs = [ex.submit(one, work, clean_exe, it) for it in m.MUTATIONS]
            answer = m.verdict(*ctl.result())
            if answer == "pass":
                passes += 1
                print("[PASS] the unmutated engine still passes the harness")
            else:
                fails += 1
                print(f"[FAIL] the unmutated engine does NOT pass ({answer})")
            for f in futs:
                ok, line = f.result()
                print(line, flush=True)
                passes += ok
                fails += not ok
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
