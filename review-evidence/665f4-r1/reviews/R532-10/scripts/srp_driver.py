#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer driver for the SRP arms of a milan-fpga checkout (round R532-10).

Usage (run with python3 -B so nothing is cached inside the checkout):
  srp_driver.py REPO LWSRP OUT positive IF [--asan]
  srp_driver.py REPO LWSRP OUT plants IF PREFIX[,PREFIX...]
  srp_driver.py REPO LWSRP OUT probes IF PROBES.py

positive: every SRP suite plus the debug arm, at one interface count.
plants:   the checkout's own srp_mutants.DEFECTS whose names start with PREFIX.
probes:   reviewer Defect entries (a module defining PROBES = (Defect, ...)).
Every build lands under OUT; the checkout is only read.
"""
import importlib.util
import sys
from pathlib import Path


def main() -> int:
    repo, lwsrp, out, mode, interfaces = (Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(),
                                          Path(sys.argv[3]).resolve(), sys.argv[4], int(sys.argv[5]))
    sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest")]
    import fw_gtest
    import srp_mutants
    from ctrl_build import CTRL, Tree
    from srp_arms import arm_srp
    out.mkdir(parents=True, exist_ok=True)
    if mode == "positive":
        asan = "--asan" in sys.argv[6:]
        tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4, address_sanitizer=asan))
        failed = 0
        runs = [("srp_mbx.cpp", False), ("srp_mbx.cpp", True)] + [
            (s, False) for s in ("srp_rx_retry.cpp", "srp_app.cpp", "test_acmp_mbx.cpp",
                                 "srp_latency.cpp", "srp_walk.cpp")]
        for suite, debug in runs:
            r = arm_srp(tree, lwsrp, interfaces, debug=debug, test=suite)
            (out / f"{r.arm}.log").write_text(r.log)
            tail = [l for l in r.log.splitlines() if "PASSED" in l or "FAILED" in l or "SRP " in l]
            print(f"[{'PASS' if r.rc == 0 else 'FAIL'}] {r.arm} rc={r.rc} {' | '.join(tail[-4:])}", flush=True)
            failed |= r.rc != 0
        return 1 if failed else 0
    if mode == "suite":
        # One suite with a gtest filter: srp_driver.py REPO LWSRP OUT suite IF SUITE FILTER [--asan]
        asan = "--asan" in sys.argv[8:]
        tree = Tree(CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4, address_sanitizer=asan))
        r = arm_srp(tree, lwsrp, interfaces, test=(sys.argv[6], sys.argv[7]))
        print(r.log, flush=True)
        print(f"[{'PASS' if r.rc == 0 else 'FAIL'}] {r.arm} filter={sys.argv[7]} asan={asan} rc={r.rc}", flush=True)
        return r.rc
    if mode == "escape":
        # Reviewer plants: CAUGHT when any test of the named suite/filter fails
        # (the most generous reading for the suite), ESCAPED when it stays green.
        import shutil
        spec = importlib.util.spec_from_file_location("probes", sys.argv[6])
        module = importlib.util.module_from_spec(spec)
        sys.modules["probes"] = module
        spec.loader.exec_module(module)
        build = fw_gtest.Build(jobs=4)
        for d in module.PROBES:
            work = out / "work"
            src = work / "ctrl"
            shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            target = src / d.path
            text = target.read_text()
            if text.count(d.old) != 1:
                print(f"[REFUSED] {d.name}: {text.count(d.old)} sites", flush=True)
                continue
            target.write_text(text.replace(d.old, d.new))
            try:
                r = arm_srp(Tree(src, work / "build", work / "reuse", build), lwsrp, interfaces,
                            test=(d.suite, d.test))
                fails = [l for l in r.log.splitlines() if l.strip().startswith("[FAIL]")]
                (out / f"{d.name}.log").write_text(r.log)
                print(f"[{'CAUGHT' if r.rc else 'ESCAPED'}] {d.name} IF={interfaces} rc={r.rc} "
                      f"failing={fails[:6]}", flush=True)
            except Exception as error:  # a compile refusal is not a catch
                print(f"[REFUSED] {d.name}: {error}", flush=True)
            # restore the pristine copy for the next probe
            target.write_text(text)
        shutil.rmtree(out / "work", ignore_errors=True)
        return 0
    if mode == "plants":
        prefixes = tuple(sys.argv[6].split(","))
        table = tuple(d for d in srp_mutants.DEFECTS if d.name.startswith(prefixes))
    elif mode == "probes":
        spec = importlib.util.spec_from_file_location("probes", sys.argv[6])
        module = importlib.util.module_from_spec(spec)
        sys.modules["probes"] = module
        spec.loader.exec_module(module)
        table = module.PROBES
    else:
        raise SystemExit(f"unknown mode {mode}")
    print(f"{len(table)} defects at IF={interfaces}: {[d.name for d in table]}", flush=True)
    srp_mutants.DEFECTS = table
    failed = srp_mutants.campaign(out, lwsrp, 4, interfaces)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
