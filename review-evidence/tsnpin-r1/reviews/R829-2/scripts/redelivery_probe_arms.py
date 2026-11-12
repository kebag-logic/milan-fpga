"""Reviewer probe 2: the two plants that escaped the acmp arm, each run in
every ACMP-reading arm separately. Usage: python3 -I redelivery_probe_arms.py <checkout> <workdir> <jobs>"""
import sys
from pathlib import Path
checkout, work, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
import ctrl_mutants  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402
C = "acmp/acmp_mbx.c"
PLANTS = (
    ("rv-continue-after-decline", "k < ACMP_MBX_REDELIVER_RECORDS && m->kept.len == 0u; ++k)",
     "k < ACMP_MBX_REDELIVER_RECORDS; ++k)"),
    ("rv-bad-continues", "\t\t\tl->stats.rx_bad += st == MBX_STATUS_BAD;\n\t\t\treturn;",
     "\t\t\tl->stats.rx_bad += st == MBX_STATUS_BAD;\n\t\t\tif (st == MBX_STATUS_BAD) continue;\n\t\t\treturn;"),
)
ARMS = sys.argv[4].split(",") if len(sys.argv) > 4 else ["acmpif2", "acmpwalk", "acmpnvm", "plat", "model"]
ctrl_mutants.caught = lambda test, needle, o: o.rc == 1 and "[FAIL]" in o.log
ctrl_mutants.unnamed_tests = lambda: []
ctrl_mutants.MUTANTS = tuple(Mutant(f"{n}@{a}", C, old, new, a, "", "") for n, old, new in PLANTS for a in ARMS)
work.mkdir(parents=True, exist_ok=True)
ctrl_mutants.campaign(work, work / "reuse", jobs)
