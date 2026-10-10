#!/usr/bin/env python3
"""R583-4: the firmware gate's arms, then only the plants this PR adds.

Usage: python3 -I r583_4_fw_gate_pr_plants.py <tree> <base-test-dir> <lwsrp> <build-dir> <jobs>

<tree> is an export of the head; <base-test-dir> holds the base's
sw/firmware/ctrl/test/*.py (dev 554e61d2, which the head merged). A plant is
this PR's when its name occurs in no base test script. The gate's own main()
runs unchanged (every arm, including srpcmp, then --self-test campaigns) over
the filtered tables. One reviewer change, stated: ctrl_mutants.unnamed_tests
is answered with no tests, because a filtered table leaves most tests named by
no planted defect, which the full-table check exists to catch.
"""
import re
import sys
from pathlib import Path

tree, base, lwsrp, build, jobs = (Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(),
                                  Path(sys.argv[3]).resolve(), Path(sys.argv[4]).resolve(), sys.argv[5])
test = tree / "sw/firmware/ctrl/test"
sys.path.insert(0, str(test))
import aecp_mutants  # noqa: E402
import ctrl_mutants  # noqa: E402
import srp_mutants  # noqa: E402
import test_ctrl_firmware  # noqa: E402

old = "\n".join(p.read_text() for p in base.glob("*.py"))
old_names = set(re.findall(r"""["']([A-Za-z0-9_.-]+)["']""", old))


def new(items):
    return tuple(x for x in items if x.name not in old_names)


ctrl_mutants.MUTANTS = new(ctrl_mutants.MUTANTS)
srp_mutants.DEFECTS = new(srp_mutants.DEFECTS)
aecp_mutants.DEFECTS = new(aecp_mutants.DEFECTS)
ctrl_mutants.unnamed_tests = lambda: []
for label, table in (("ctrl", ctrl_mutants.MUTANTS), ("srp", srp_mutants.DEFECTS), ("aecp", aecp_mutants.DEFECTS)):
    print(f"PR plants, {label}: {len(table)}: {', '.join(x.name for x in table)}", flush=True)
sys.exit(test_ctrl_firmware.main(["--require-rv32", "--self-test", "--jobs", jobs, "--lwsrp", str(lwsrp),
                                  "--build-dir", str(build)]))
