#!/usr/bin/env python3
"""Reviewer probe: plant reclaim-state defects not in srp_reclaim_mutants.py into a disposable copy of
sw/firmware/ctrl and run the whole srp_listeners.cpp suite at 1x1/1if and 8x8/1if. Usage:
probe_reclaim.py <repo> <scratch-out> <suite.cpp> [probe...]"""
import shutil, sys
from pathlib import Path
repo = Path(sys.argv[1]).resolve(); outroot = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import srp_arms, fw_gtest
from srp_arms import arm_srp
from ctrl_build import Tree
FREED = "#define SRP_FREED_APPL ((1u << MRP_APPL_STATE_VO) | (1u << MRP_APPL_STATE_AO) | (1u << MRP_APPL_STATE_QO))\n"
PROBES = {
    "control": None,
    "ao-dropped": (FREED, FREED.replace(" | (1u << MRP_APPL_STATE_AO)", "")),
    "qo-dropped": (FREED, FREED.replace(" | (1u << MRP_APPL_STATE_QO)", "")),
    "ao-qo-dropped": (FREED, "#define SRP_FREED_APPL (1u << MRP_APPL_STATE_VO)\n"),
    "room-medium-only": ("    return (unsigned)pool->bins[1].free_count + pool->bins[2].free_count;\n",
                         "    return (unsigned)pool->bins[1].free_count;\n"),
    "prefilter-byte6": ("        if (s[7] == id[7] && same(s,id,8)) {\n", "        if (s[6] == id[6] && same(s,id,7)) {\n"),
}
suite = sys.argv[3]
which = sys.argv[4:] or list(PROBES)
import os
lw = Path(os.environ.get("PROBE_LWSRP", str(repo / "third_party/lwSRP")))
for name in which:
    for cfg in (srp_arms.DEFAULT_ENTITY, srp_arms.ENTITY_8X8):
        out = outroot / f"{name}-{suite}-{cfg.stem}"
        src = out / "ctrl"
        shutil.copytree(repo / "sw/firmware/ctrl", src, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        if PROBES[name]:
            p = src / "srp/srp_mbx.c"; t = p.read_text(); old, new = PROBES[name]
            assert t.count(old) == 1, name
            p.write_text(t.replace(old, new))
        build = fw_gtest.Build(jobs=2)
        r = arm_srp(Tree(src, out / "build", out / "reuse", build), lw, 1, test=(suite, "*"), config=cfg)
        (outroot / f"{name}-{suite}-{cfg.stem}.log").write_text(r.log)
        fails = [l for l in r.log.splitlines() if l.startswith("[  FAILED  ]")]
        print(f"{name} {suite} {cfg.stem} rc={r.rc} failed={len(fails)} {fails[:6]}", flush=True)
