#!/usr/bin/env python3
"""Production-path probe for processor #189's SETTLED_RSV_OK kind swap.

Runs the composed firmware (ctrl_app with SRP attached, real mailbox SRP
input, real ACMP wire) suite test_acmp_mbx.cpp filtered to SrpFeedback.*, at
one and two interfaces, in three variants:

  clean      the firmware and stack as committed;
  glue-lost  app/ctrl_app_srp.c's acmp_tk_kind_changed call dropped;
  stack-mute tsn-c-stack's acmp_tk_kind_changed marks its view reported
             before finish(), so only the notification is lost.

The caller has added, in the worktree and only for this probe, one check per
swap to srp_feedback.hpp: the CHANGED port fired through the composed app
(a one-shot hook armed before the swap and consumed by it). The caller
restores the file afterwards.

Usage: probe_production.py REPO OUT
"""
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import ctrl_build  # noqa: E402
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
import srp_arms  # noqa: E402
from ctrl_mutant import ACMP_C, Mutant  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

LWSRP = root / "third_party/lwSRP"
VARIANTS = {
    "clean": None,
    "glue-lost": Mutant("probe-glue-lost", "app/ctrl_app_srp.c",
                        "acmp_tk_kind_changed(&app->acmp.acmp,sink,registered == 1u);",
                        "(void)registered;", "", "", ""),
    "stack-mute": Mutant("probe-stack-mute", ACMP_C,
                         "\ta->sinks[sink].tk_failed = failed;\n\tfinish(a);",
                         "\ta->sinks[sink].tk_failed = failed;\n"
                         "\tview_of(&a->sinks[sink], &a->sinks[sink].reported);\n\tfinish(a);", "", "", ""),
}

print("toolchain", fw_gtest.toolchain())
print("stack pin", ctrl_build.stack_pin())
result = {}
for name, m in VARIANTS.items():
    base = out / name
    reuse = base / "reuse"
    cut_reuse(reuse)
    if m is None:
        tree = ctrl_build.Tree(ctrl_build.CTRL, base / "build", reuse, fw_gtest.Build(jobs=4))
    else:
        ctrl, stack = ctrl_mutants.plant(m, base)
        tree = ctrl_build.Tree(ctrl, base / "work" / "build", reuse, fw_gtest.Build(jobs=4), stack)
    for interfaces in (1, 2):
        o = srp_arms.arm_srp(tree, LWSRP, interfaces, test=("test_acmp_mbx.cpp", "SrpFeedback.*"))
        (base / f"if{interfaces}.log").write_text(o.log)
        fails = [ln.strip() for ln in o.log.splitlines() if "[FAIL]" in ln]
        tally = [ln for ln in o.log.splitlines() if ln.startswith("==")]
        result[f"{name}-if{interfaces}"] = {"rc": o.rc, "tally": tally, "fails": fails}
print(json.dumps(result, indent=2))
(out / "result.json").write_text(json.dumps(result, indent=2) + "\n")
