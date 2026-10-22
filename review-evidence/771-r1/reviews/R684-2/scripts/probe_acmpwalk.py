#!/usr/bin/env python3
"""Build and run only the firmware gate's acmpwalk arm (and, with --controls,
the planted SOK kind controls through the gate's own plant/caught judgement).

Usage: probe_acmpwalk.py REPO OUT LABEL [--controls NAME[,NAME...]]

Reads REPO; writes only under OUT. Exit 0 when the run matches what LABEL
expects is printed by the caller; this script prints the outcomes as JSON.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
label = sys.argv[3]
controls = []
if len(sys.argv) > 5 and sys.argv[4] == "--controls":
    controls = sys.argv[5].split(",")
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_arms  # noqa: E402
import ctrl_build  # noqa: E402
import ctrl_mutants  # noqa: E402
import ctrl_reuse  # noqa: E402
import fw_gtest  # noqa: E402

print("toolchain", fw_gtest.toolchain())
print("stack pin", ctrl_build.stack_pin())
print("processor pin", ctrl_reuse.prove_pin("tb/acmp_listener/sim_main.cpp"))
base = out / label
reuse = base / "reuse"
ctrl_reuse.cut_reuse(reuse)
result = {}
if not controls:
    tree = ctrl_build.Tree(ctrl_build.CTRL, base / "build", reuse, fw_gtest.Build(jobs=4))
    o = ctrl_arms.arm_acmpwalk(tree)
    (base / "acmpwalk.log").write_text(o.log)
    tally = [ln for ln in o.log.splitlines() if ln.startswith("== ctrl ACMP walk")]
    result["acmpwalk"] = {"rc": o.rc, "tally": tally,
                          "fails": [ln.strip() for ln in o.log.splitlines() if "[FAIL]" in ln],
                          "log_sha256": hashlib.sha256(o.log.encode()).hexdigest()}
else:
    arms = {"acmp": ctrl_arms.arm_acmp, "acmpwalk": ctrl_arms.arm_acmpwalk}
    by_name = {m.name: m for m in ctrl_mutants.MUTANTS}
    build = fw_gtest.Build(jobs=4)
    for name in controls:
        m = by_name[name]
        ctrl, stack = ctrl_mutants.plant(m, base)
        tree = ctrl_build.Tree(ctrl, base / "work" / "build", reuse, build, stack)
        kills = []
        for arm, test, needle in m.kills():
            o = arms[arm](tree)
            (base / f"{name}.{arm}.log").write_text(o.log)
            kills.append({"arm": arm, "test": test, "needle": needle, "rc": o.rc,
                          "caught": ctrl_mutants.caught(test, needle, o),
                          "fails": [ln.strip() for ln in o.log.splitlines() if "[FAIL]" in ln]})
        result[name] = {"path": m.path, "old": m.old, "new": m.new, "kills": kills,
                        "killed": all(k["caught"] for k in kills)}
print(json.dumps(result, indent=2))
(base / "result.json").write_text(json.dumps(result, indent=2) + "\n")
if controls:
    assert all(v['killed'] for v in result.values()), 'a selected control escaped'
else:
    assert result['acmpwalk']['rc'] == 0 and not result['acmpwalk']['fails']
    assert any('checks: 127   failures: 0' in x for x in result['acmpwalk']['tally'])
