"""Reviewer probe: the prior round's optional plant at the redelivery's kept-record guard,
`if (m->kept.len != 0u)` -> `if (true)`, in the acmp and acmpif2 arms.
Usage: python3 -I empty_kept_probe.py <checkout> <workdir> <jobs>"""
import sys
from pathlib import Path
co, work, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
sys.path.insert(0, str(co / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(co / "sw/firmware/gtest"))
import ctrl_mutants  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402
OLD = "\tif (m->kept.len != 0u) {\n\t\tif (!acmp_rx("
NEW = "\tif (true) {\n\t\tif (!acmp_rx("
ctrl_mutants.caught = lambda test, needle, o: o.rc == 1 and "[FAIL]" in o.log
ctrl_mutants.unnamed_tests = lambda: []
ctrl_mutants.MUTANTS = tuple(Mutant(f"empty-kept-offered@{a}", "acmp/acmp_mbx.c", OLD, NEW, a, "", "")
                             for a in ("acmp", "acmpif2"))
work.mkdir(parents=True, exist_ok=True)
ctrl_mutants.campaign(work, work / "reuse", jobs)
