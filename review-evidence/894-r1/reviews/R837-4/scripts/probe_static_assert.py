#!/usr/bin/env python3
"""Probe the map table's _Static_assert (aecp_maps.c) at exact head.

usage: probe_static_assert.py REPO SCRATCH
Copies REPO/sw/firmware/ctrl to SCRATCH/ctrl-<variant>, plants one variant of MAP_SLOTS / the assert, and for each
variant (a) compiles aecp_maps.c against every checked-in configuration's generated header (syntax and constraints
only) and (b) runs Core.EveryAcceptedMapKeyIsItsOwn:Core.MapEdit* in the core arm at 1x1/1if. Prints one line per
result. The repository itself is never written."""
import shutil, subprocess, sys
from pathlib import Path

repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import aecp_arms, fw_gtest
from ctrl_build import Tree, STACK, STACK_INCLUDE, HARNESS

OLD_SLOTS = "#define MAP_SLOTS MAP_MOST(MAP_FIRSTS * MAP_CHANNELS, 256u)\n"
PER_TYPE = ("#define MAP_SLOTS MAP_MOST(AECP_ENTITY_KEY_STREAMS * AECP_ENTITY_KEY_STREAM_CHANNELS, "
            "AECP_ENTITY_KEY_CLUSTERS * AECP_ENTITY_KEY_CLUSTER_CHANNELS)\n")
OLD_ASSERT = "_Static_assert(AECP_ENTITY_KEY_STREAMS * AECP_ENTITY_KEY_STREAM_CHANNELS <= MAP_SLOTS &&"
NEW_ASSERT = "_Static_assert(MAP_FIRSTS * MAP_CHANNELS <= MAP_SLOTS &&"
VARIANTS = {
    "head": [],
    "per-type-slots": [(OLD_SLOTS, PER_TYPE)],
    "per-type-slots+index-assert": [(OLD_SLOTS, PER_TYPE), (OLD_ASSERT, NEW_ASSERT)],
}
stack = STACK.resolve()
for name, edits in VARIANTS.items():
    src = scratch / f"ctrl-{name}"
    if src.exists():
        shutil.rmtree(src)
    shutil.copytree(repo / "sw/firmware/ctrl", src)
    path = src / "aecp/aecp_maps.c"
    text = path.read_text()
    for old, new in edits:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    path.write_text(text)
    for config in sorted((repo / "configs").glob("endstation_*.yaml")):
        gen = scratch / f"gen-{name}-{config.stem}"
        gen.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, "-B", str(repo / "sw/firmware/ctrl/aecp/aecp_entity.py"), str(config),
                        "-o", str(gen / "aecp_entity_gen.h")], check=True)
        r = subprocess.run(["cc", "-std=c11", "-fsyntax-only", f"-I{src / 'aecp'}", f"-I{stack / STACK_INCLUDE}",
                            f"-I{HARNESS}", f"-I{gen}", f"-I{src / 'test'}", str(path)],
                           capture_output=True, text=True)
        err = [l for l in r.stderr.splitlines() if "static assert" in l or "static_assert" in l]
        print(f"{name} {config.stem}: compile rc {r.returncode}{' ' + err[0].split('error: ')[-1] if err else ''}",
              flush=True)
    build = fw_gtest.Build(coverage=False, address_sanitizer=True, jobs=4)
    tree = Tree(src, scratch / f"out-{name}", scratch / f"out-{name}" / "reuse", build, stack)
    try:
        out = aecp_arms.core_arm(tree, repo / "configs/endstation_ax7101_1x1_tdm8.yaml", 1, "work",
                                 "Core.EveryAcceptedMapKeyIsItsOwn:Core.MapEdit*")
        tail = [l for l in out.log.splitlines() if "FAILED" in l or "PASSED" in l or "ERROR" in l or "Failure" in l]
        print(f"{name} 1x1/1if work arm: rc {out.rc}; " + " | ".join(tail[:6]), flush=True)
    except Exception as exc:  # a build that refuses is a result too
        print(f"{name} 1x1/1if work arm: refused: {str(exc).strip().splitlines()[-1][:300]}", flush=True)
