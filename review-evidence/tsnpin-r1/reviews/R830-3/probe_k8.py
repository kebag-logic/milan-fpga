#!/usr/bin/env python3
"""Reviewer probe for the K8 redelivery test (#665).

Usage: python3 -I probe_k8.py <repo-root> <work-dir>

Uses the repository's own ctrl_build / ctrl_arms / ctrl_mutants machinery,
reading the tree read-only and writing every build and planted copy under
<work-dir>. Phases:
  1. the clean `acmp` and `acmpif2` arms, and whether K8 ran and passed in each;
  2. a mutant campaign over the author's plant, the two plants on the same
     loop line, and reviewer-own plants (below), each required caught by K8
     or by its named check.
"""
from __future__ import annotations

import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.dont_write_bytecode = True

import ctrl_arms  # noqa: E402
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import Tree  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

K8 = "AcmpMailbox.K8ACommandTheRedeliveryDeclinesKeepsItsPlaceAheadOfTheNext"
K8_WORDS = "K8 the owed frames, then each command answered once, in arrival order"

print(f"mutant table size: {len(ctrl_mutants.MUTANTS)}")
print(f"toolchain: {fw_gtest.toolchain()}")

work.mkdir(parents=True, exist_ok=True)
fw_gtest.EXECUTION.run = True
tree = Tree(ctrl_mutants.CTRL, work / "clean" / "checkout", work / "reuse", fw_gtest.Build(jobs=4))
cut_reuse(tree.reuse)
for name, arm in (("acmp", ctrl_arms.arm_acmp), ("acmpif2", ctrl_arms.arm_acmpif2)):
    out = arm(tree)
    k8 = [ln for ln in out.log.splitlines() if "K8ACommandTheRedelivery" in ln]
    summary = [ln for ln in out.log.splitlines() if "tests" in ln and ("PASSED" in ln or "FAILED" in ln or "ran" in ln)]
    print(f"[clean {name}] rc={out.rc}")
    for ln in k8 + summary[-3:]:
        print(f"    {ln.strip()}")

LOOP = "\tfor (unsigned k = 0; k < ACMP_MBX_REDELIVER_RECORDS && m->kept.len == 0u; ++k) {"
own = (
    # the stop moved from the loop guard to after the take: the record behind a decline is taken and
    # its decline overwrites the kept one (a second spelling of the same defect)
    Mutant("rv-stop-checked-after-take", "acmp/acmp_mbx.c",
           LOOP + "\n\t\tconst enum mbx_status st = mbx_rx_take(MBX_CH_ACMP, &l->frame);",
           "\tfor (unsigned k = 0; k < ACMP_MBX_REDELIVER_RECORDS; ++k) {\n"
           "\t\tconst enum mbx_status st = mbx_rx_take(MBX_CH_ACMP, &l->frame);",
           "acmp", K8, K8_WORDS),
    # past a decline, but the later decline is dropped instead of overwriting the kept one: the third
    # command is lost instead of the second
    Mutant("rv-past-decline-drops-later", "acmp/acmp_mbx.c",
           "\tmemcpy(m->kept.frame, f->bytes, f->len);",
           "\tif (m->kept.len != 0u) {\n\t\treturn;\n\t}\n\tmemcpy(m->kept.frame, f->bytes, f->len);",
           "acmp", K8, K8_WORDS),
    # stop removed AND later declines dropped: only K8's shape (a decline with a record behind it) sees it
    Mutant("rv-past-decline-and-drop", "acmp/acmp_mbx.c",
           LOOP + "\n\t\tconst enum mbx_status st = mbx_rx_take(MBX_CH_ACMP, &l->frame);"
           "\n\t\tif (st != MBX_STATUS_OK) {",
           "\tfor (unsigned k = 0; k < ACMP_MBX_REDELIVER_RECORDS; ++k) {\n"
           "\t\tif (m->kept.len != 0u) { struct mbx_frame d; (void)mbx_rx_take(MBX_CH_ACMP, &d); continue; }\n"
           "\t\tconst enum mbx_status st = mbx_rx_take(MBX_CH_ACMP, &l->frame);"
           "\n\t\tif (st != MBX_STATUS_OK) {",
           "acmp", K8, K8_WORDS),
)
by_name = {m.name: m for m in ctrl_mutants.MUTANTS}
chosen = [by_name[n] for n in ("acmp-redelivery-past-a-decline", "acmp-redelivery-takes-no-waiting-record",
                               "acmp-redelivery-short-of-a-full-ring")]
ctrl_mutants.MUTANTS = tuple(chosen) + own
# a subset names only some tests: the whole-table "every test named" check is the full campaign's, not this probe's
ctrl_mutants.unnamed_tests = lambda: []
escaped = ctrl_mutants.campaign(work / "mutants", tree.reuse, 4)
print(f"probe campaign escaped={escaped}")
sys.exit(1 if escaped else 0)
