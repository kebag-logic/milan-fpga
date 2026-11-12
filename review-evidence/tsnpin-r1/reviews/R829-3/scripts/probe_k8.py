#!/usr/bin/env python3
"""Reviewer probe for K8 (#665): run the acmp and acmpif2 arms on the
unmodified tree, then plant each probe defect into a COPY (the campaign's own
plant()) and report which named checks fail.
Usage: python3 -B probe_k8.py <repo-root> <out-dir>"""
import sys
from pathlib import Path
repo, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import ctrl_arms, ctrl_mutants, fw_gtest  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402
from ctrl_build import Tree  # noqa: E402

LOOP = "\tfor (unsigned k = 0; k < ACMP_MBX_REDELIVER_RECORDS && m->kept.len == 0u; ++k) {"
K8 = "AcmpMailbox.K8ACommandTheRedeliveryDeclinesKeepsItsPlaceAheadOfTheNext"
PROBES = [
    # the author's plant, verbatim from the table
    next(m for m in ctrl_mutants.MUTANTS if m.name == "acmp-redelivery-past-a-decline"),
    # reviewer variant: the stop tested after the take, so the record taken behind a decline is dropped
    Mutant("rv-stop-after-take", "acmp/acmp_mbx.c",
           LOOP + "\n\t\tconst enum mbx_status st = mbx_rx_take(MBX_CH_ACMP, &l->frame);\n"
           "\t\tif (st != MBX_STATUS_OK) {\n\t\t\tl->stats.rx_bad += st == MBX_STATUS_BAD;\n\t\t\treturn;\n\t\t}\n"
           "\t\tl->stats.rx_records++;\n",
           "\tfor (unsigned k = 0; k < ACMP_MBX_REDELIVER_RECORDS; ++k) {"
           "\n\t\tconst enum mbx_status st = mbx_rx_take(MBX_CH_ACMP, &l->frame);\n"
           "\t\tif (st != MBX_STATUS_OK) {\n\t\t\tl->stats.rx_bad += st == MBX_STATUS_BAD;\n\t\t\treturn;\n\t\t}\n"
           "\t\tl->stats.rx_records++;\n\t\tif (m->kept.len != 0u) {\n\t\t\treturn;\n\t\t}\n",
           "acmp", K8, "K8 the owed frames, then each command answered once, in arrival order"),
]
arms = {"acmp": ctrl_arms.arm_acmp, "acmpif2": ctrl_arms.arm_acmpif2}
build = fw_gtest.Build(jobs=4)
rc = 0

def show(label, outcome):
    fails = [ln.strip() for ln in outcome.log.splitlines() if "[FAIL]" in ln]
    k8 = [ln for ln in outcome.log.splitlines() if "K8ACommandTheRedelivery" in ln]
    print(f"{label}: rc={outcome.rc} fails={len(fails)}")
    for ln in fails[:6]:
        print("    FAIL", ln[:220])
    for ln in k8[:4]:
        print("    K8  ", ln.strip()[:220])
    verdict = [ln.strip() for ln in outcome.log.splitlines() if "verdict" in ln or "tests," in ln]
    for ln in verdict[-2:]:
        print("    ", ln[:200])
    return fails

base = Tree(ctrl_mutants.CTRL, out / "base" / "build", out / "reuse", build)
for name, fn in arms.items():
    o = fn(base)
    f = show(f"[clean] arm {name}", o)
    (out / f"clean-{name}.log").write_text(o.log)
    rc |= 1 if (o.rc != 0 or f) else 0
for m in PROBES:
    ctrl, stack = ctrl_mutants.plant(m, out / m.name)
    tree = Tree(ctrl, out / m.name / "work" / "build", out / "reuse", build, stack)
    for name, fn in arms.items():
        o = fn(tree)
        f = show(f"[{m.name}] arm {name}", o)
        (out / f"{m.name}-{name}.log").write_text(o.log)
        hit = ctrl_mutants.caught(m.test, m.needle, o)
        print(f"    named catch ({m.test.split('.')[1][:2]} on its words): {hit}")
        if name == "acmp" and not hit:
            rc |= 2
print("probe rc", rc)
sys.exit(rc)
