#!/usr/bin/env python3
"""R532-12 reviewer driver: focused SRP arms, AddressSanitizer arms and parallel
plant/probe campaigns against an unmodified candidate checkout.

Usage (from anywhere; SOURCE is the candidate checkout, LWSRP the pinned lwSRP):
  r12_run.py arms     SOURCE LWSRP OUT [--asan] [--workers N]
  r12_run.py mutants  SOURCE LWSRP OUT --prefix feedback- --prefix p11- [--interfaces 1 2] [--workers N]
  r12_run.py probes   SOURCE LWSRP OUT PROBES.py [--interfaces 1 2] [--workers N]

Every planted copy lives under OUT; the candidate checkout is never written.
Exit 0 only when every arm passed / every plant was caught by name /
every probe produced its declared expectation.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

SUITES = ("srp_mbx.cpp", "srp_rx_retry.cpp", "srp_app.cpp", "test_acmp_mbx.cpp",
          "srp_latency.cpp", "srp_walk.cpp")


def setup(source: Path):
    sys.path.insert(0, str(source / "sw/firmware/ctrl/test"))
    sys.path.insert(0, str(source / "sw/firmware/gtest"))


def one_arm(job):
    source, lwsrp, out, suite, ifs, debug, asan = job
    setup(Path(source))
    import fw_gtest, srp_arms
    from ctrl_build import CTRL, Tree, Refusal
    root = Path(out) / f"{'asan-' if asan else ''}{'debug' if debug else suite.removesuffix('.cpp')}-if{ifs}"
    tree = Tree(CTRL, root / "build", root / "reuse", fw_gtest.Build(jobs=2, address_sanitizer=asan))
    try:
        o = srp_arms.arm_srp(tree, Path(lwsrp), ifs, debug=debug, test=suite)
        rc, log = o.rc, o.log
    except Refusal as e:
        rc, log = 2, f"REFUSED: {e}"
    (Path(out) / f"{root.name}.log").write_text(log)
    tally = [ln for ln in log.splitlines() if "checks:" in ln or ln.startswith("RESULT") or "PASSED" in ln or "FAILED" in ln]
    shutil.rmtree(root, ignore_errors=True)
    return root.name, rc, tally[-3:]


def one_plant(job):
    source, lwsrp, out, d, ifs, expect_caught = job
    setup(Path(source))
    import fw_gtest, srp_mutants
    from ctrl_build import CTRL, Tree, Refusal
    from srp_arms import arm_srp
    work = Path(out) / f"work-{d['name']}-if{ifs}"
    src = work / "ctrl"
    shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    target = src / d["path"]
    text = target.read_text()
    sites = text.count(d["old"])
    if sites != 1:
        shutil.rmtree(work, ignore_errors=True)
        return d["name"], ifs, "REFUSED", f"{sites} planting sites"
    target.write_text(text.replace(d["old"], d["new"]))
    selected = d["test"] if ("." in d["test"] or d["test"] == "*") else "Srp." + d["test"]
    try:
        r = arm_srp(Tree(src, work / "build", work / "reuse", fw_gtest.Build(jobs=2)), Path(lwsrp), ifs,
                    debug=d.get("debug", False), test=(d["suite"], selected))
        ok = (r.rc == 1) if d["test"] == "*" else srp_mutants.caught(selected, d["needle"], r)
        log = r.log
        status = "CAUGHT" if ok else ("FAILED-OTHER" if r.rc else "SURVIVED")
    except Refusal as e:
        log, status = f"REFUSED: {e}", "BUILD-REFUSED"
    (Path(out) / f"{d['name']}-if{ifs}.log").write_text(log)
    shutil.rmtree(work, ignore_errors=True)
    return d["name"], ifs, status, d["test"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("arms", "mutants", "probes"))
    ap.add_argument("source", type=Path)
    ap.add_argument("lwsrp", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("probes", type=Path, nargs="?")
    ap.add_argument("--asan", action="store_true")
    ap.add_argument("--prefix", action="append", default=[])
    ap.add_argument("--interfaces", type=int, nargs="+", default=[1, 2])
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    src, lw, out = str(a.source.resolve()), str(a.lwsrp.resolve()), str(a.out.resolve())
    results = []
    if a.mode == "arms":
        jobs = [(src, lw, out, s, i, False, a.asan) for i in a.interfaces for s in SUITES]
        jobs += [(src, lw, out, "srp_mbx.cpp", i, True, a.asan) for i in a.interfaces]
        with ProcessPoolExecutor(a.workers) as ex:
            for name, rc, tally in ex.map(one_arm, jobs):
                print(f"[{'PASS' if rc == 0 else 'FAIL'}] {name} rc={rc} {' | '.join(tally)}", flush=True)
                results.append({"arm": name, "rc": rc, "tally": tally})
        bad = any(r["rc"] for r in results)
    else:
        setup(a.source.resolve())
        if a.mode == "mutants":
            import srp_mutants
            defs = [d.__dict__ for d in srp_mutants.DEFECTS if d.name.startswith(tuple(a.prefix))]
            expect = {d["name"]: True for d in defs}
        else:
            spec = importlib.util.spec_from_file_location("probes", a.probes)
            mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
            defs = mod.PROBES
            expect = {d["name"]: d.get("expect", "CAUGHT") for d in defs}
        jobs = [(src, lw, out, d, i, True) for d in defs for i in a.interfaces]
        with ProcessPoolExecutor(a.workers) as ex:
            for name, ifs, status, test in ex.map(one_plant, jobs):
                want = "CAUGHT" if a.mode == "mutants" else expect[name]
                print(f"[{status}] {name} IF={ifs} ({test}) expected={want}", flush=True)
                results.append({"name": name, "if": ifs, "status": status, "expected": want, "test": test})
        bad = any(r["status"] != r["expected"] for r in results)
    (a.out / "results.json").write_text(json.dumps(results, indent=1))
    print(f"{a.mode}: {'FAIL' if bad else 'PASS'} ({len(results)} entries)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
