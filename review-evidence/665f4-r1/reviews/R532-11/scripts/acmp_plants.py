#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Plant named entries of the checkout's own ACMP/control mutant table.

Usage (python3 -B): acmp_plants.py REPO OUT JOBS NAME[,NAME...]
Each named mutant (plus one reviewer plant, p11-acmp-kind-unguarded) runs through ctrl_mutants.campaign unchanged (catch means the
named test failed on its own words). The unnamed-test audit is the complete
table's concern and is disabled for this subset only.
"""
import sys
from pathlib import Path


def main() -> int:
    repo, out, jobs, names = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3]), sys.argv[4]
    sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest")]
    import ctrl_mutants
    from ctrl_reuse import cut_reuse
    wanted = names.split(",")
    table = tuple(m for m in ctrl_mutants.MUTANTS if m.name in wanted)
    missing = sorted(set(wanted) - {m.name for m in table})
    if missing:
        print(f"missing mutants: {missing}")
        return 2
    from ctrl_mutant import Mutant
    # Reviewer plant: the new settled-view entry loses its #678 reentry guard.
    table += (Mutant("p11-acmp-kind-unguarded", "acmp/acmp.c",
                     "void acmp_tk_kind_changed(struct acmp *a, unsigned sink, bool failed)\n{\n"
                     "\tif (!enter(a)) {\n\t\treturn;\n\t}\n",
                     "void acmp_tk_kind_changed(struct acmp *a, unsigned sink, bool failed)\n{\n",
                     "acmp", "AcmpCore.A23EveryEntryRefusesACallFromInsideAPort",
                     "A23 a call made from inside the send port is refused, counted and trapped, entry 4"),)
    ctrl_mutants.MUTANTS = table
    ctrl_mutants.unnamed_tests = lambda *a, **k: []
    out.mkdir(parents=True, exist_ok=True)
    cut_reuse(out / "reuse")
    return 1 if ctrl_mutants.campaign(out, out / "reuse", jobs) else 0


if __name__ == "__main__":
    sys.exit(main())
