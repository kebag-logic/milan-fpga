#!/usr/bin/env python3
"""Reviewer probe: run the acmp and acmpwalk arms of the control firmware at
the checked-out head, unplanted and with planted defects, using the
repository's own planting (ctrl_mutants.plant) and arms (ctrl_arms).
usage: probe_walk.py <repo root> <scratch root> [jobs]"""
import sys
from pathlib import Path
repo = Path(sys.argv[1]).resolve(); root = Path(sys.argv[2]).resolve()
jobs = int(sys.argv[3]) if len(sys.argv) > 3 else 4
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import ctrl_arms, ctrl_mutants, fw_gtest  # noqa: E402
from ctrl_build import CTRL, Tree, stack_pin, STACK  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402
from ctrl_mutant import Mutant, ACMP_C  # noqa: E402

byname = {m.name: m for m in ctrl_mutants.MUTANTS}
OLD_DRIVE = ("        } else if (s.tk_kind == 2u && a.sinks[k].state == ACMP_SETTLED_RSV_OK) {\n"
             "            acmp_tk_kind_changed(&a, static_cast<unsigned>(k), s.tk_fail);   // the swap, as ctrl_app_srp.c delivers it\n"
             "        } else if (s.tk_kind == 2u) {\n")
probes = [
    ("head-unplanted", None),
    ("acmp-kind-lost", byname["acmp-kind-lost"]),
    ("acmp-kind-not-notified", byname["acmp-kind-not-notified"]),
    # reviewer's own controls
    ("rev-kind-inverted", Mutant("rev-kind-inverted", ACMP_C, "\ta->sinks[sink].tk_failed = failed;",
                                "\ta->sinks[sink].tk_failed = !failed;", "acmpwalk", "", "")),
]
# The arms compile test sources from the checkout's test/, not from a planted
# copy, so a test-side revert is applied to the checkout by the caller
# (probe_walk_revert.sh) and run here as label "checkout-as-is".
only = sys.argv[4].split(",") if len(sys.argv) > 4 else None
if only:
    probes = [p for p in probes if p[0] in only] + ([("checkout-as-is", None)] if "checkout-as-is" in only else [])
print(f"tsn-c-stack at {stack_pin()}"); sys.stdout.flush()
reuse = root / "reuse"; reuse.mkdir(parents=True, exist_ok=True)
cut_reuse(reuse)
build = fw_gtest.Build(jobs=jobs)
for label, m in probes:
    if m is None:
        tree = Tree(CTRL, root / label / "build", reuse, build)
    else:
        ctrl, stack = ctrl_mutants.plant(m, root / label)
        tree = Tree(ctrl, root / label / "work" / "build", reuse, build, stack)
    for arm in ("acmp", "acmpwalk"):
        o = getattr(ctrl_arms, "arm_" + arm)(tree)
        tallies = [ln.strip() for ln in o.log.splitlines() if ln.startswith("== ")]
        fails = sorted({ln.strip() for ln in o.log.splitlines() if "[FAIL]" in ln})
        (root / f"{label}.{arm}.log").write_text(o.log)
        print(f"{label} {arm} rc={o.rc} {' | '.join(tallies)}")
        for f in fails:
            print(f"    {f}")
        sys.stdout.flush()
