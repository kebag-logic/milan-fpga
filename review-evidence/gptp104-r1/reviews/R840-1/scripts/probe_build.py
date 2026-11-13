#!/usr/bin/env python3
"""Call one tree's engine-arm build() once, for the clean sources.

usage: probe_build.py <tree-root> <work-dir> [--env]
Imports <tree-root>/tb/verilator/engine/mutants.py, stages the clean RTL
under <work-dir>, builds it with the arm's own build(), and prints BUILT
or NOT-BUILT, then the absolute <work-dir> occurrences found in the
generated model sources. With --env, prints only compiler_env()'s
OBJCACHE and CCACHE_NOHASHDIR and exits.
"""
import importlib.util
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
spec = importlib.util.spec_from_file_location(
    "arm", root / "tb/verilator/engine/mutants.py")
arm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arm)
if "--env" in sys.argv:
    env = arm.compiler_env()
    print(f"OBJCACHE={env.get('OBJCACHE')!r} CCACHE_NOHASHDIR={env.get('CCACHE_NOHASHDIR')!r}")
    sys.exit(0)
work.mkdir(parents=True, exist_ok=True)
src = arm.stage(work, "clean")
exe = arm.build(src, work, "clean")
print("BUILT" if exe is not None else "NOT-BUILT")
hits = []
for f in sorted((work / "obj_clean").glob("*")):
    if f.suffix in (".cpp", ".h") and str(work) in f.read_text(errors="replace"):
        hits.append(f.name)
print(f"model sources naming the work dir: {len(hits)} {hits[:5]}")
sys.exit(0 if exe is not None else 1)
