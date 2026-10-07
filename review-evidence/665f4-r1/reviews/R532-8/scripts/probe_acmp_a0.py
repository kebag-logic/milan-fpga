#!/usr/bin/env python3
"""R532-8 reviewer probe: is the A0 'more sources' catch of the F3 plant
acmp-init-too-many-sources deterministic? Plants it (and a control without it)
into a scratch copy of the exact-head tree and runs the acmp arm with the
default compiler, with AddressSanitizer, and with clang.

usage: probe_acmp_a0.py REPO WORK
"""
import os, shutil, sys
sys.dont_write_bytecode = True
from pathlib import Path


def main() -> int:
    repo, work = Path(sys.argv[1]), Path(sys.argv[2])
    sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest")]
    import fw_gtest
    from ctrl_build import Tree
    from ctrl_reuse import cut_reuse
    import ctrl_arms
    shutil.rmtree(work, ignore_errors=True)
    reuse = work / "reuse"; cut_reuse(reuse)
    old = "cfg->n_sources > ACMP_MAX_SOURCES) {"
    new = "cfg->n_sources > ACMP_MAX_SOURCES + 1u) {"
    needle = "A0 more sources than ACMP_MAX_SOURCES"
    for planted in (False, True):
        src = work / ("planted" if planted else "control") / "ctrl"
        shutil.copytree(repo / "sw/firmware/ctrl", src)
        if planted:
            target = src / "acmp/acmp.c"; text = target.read_text()
            assert text.count(old) == 1
            target.write_text(text.replace(old, new))
        for label, build, env in (("gcc", fw_gtest.Build(jobs=4), {}),
                                  ("gcc+asan", fw_gtest.Build(jobs=4, address_sanitizer=True), {}),
                                  ("clang", fw_gtest.Build(jobs=4), {"CC": "clang", "CXX": "clang++"})):
            saved = {k: os.environ.get(k) for k in env}
            os.environ.update(env)
            try:
                out = ctrl_arms.arm_acmp(Tree(src, src.parent / f"build-{label}", reuse, build))
            finally:
                for k, v in saved.items():
                    os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
            lines = out.log.splitlines()
            a0 = [l.strip() for l in lines if needle in l]
            asan = [l.strip() for l in lines if "AddressSanitizer" in l or "stack-buffer-overflow" in l][:3]
            tally = next((l.strip() for l in reversed(lines) if "verdict:" in l), "")
            print(f"{'planted' if planted else 'control'} {label}: rc={out.rc} A0-sources-check-failed={bool(a0)} "
                  f"{tally[:120]}")
            for l in asan:
                print(f"    {l[:200]}")
            (work / f"{'planted' if planted else 'control'}-{label}.log").write_text(out.log)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
