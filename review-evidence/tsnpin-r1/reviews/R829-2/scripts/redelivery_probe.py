"""Reviewer probe: plant the round-2 redelivery mutants and reviewer-own
defects into a scratch copy of the ctrl tree and run the ACMP arms.
Usage: python3 -I redelivery_probe.py <checkout> <workdir> <jobs>"""
import sys
from pathlib import Path
checkout, work, jobs = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
import ctrl_mutants  # noqa: E402
import acmp_owed_mutants  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402

C = "acmp/acmp_mbx.c"
K = "AcmpMailbox."
OWN = (
    # R1 the redelivery keeps going past a record the core declined (overwrites the kept record)
    Mutant("rv-continue-after-decline", C,
           "k < ACMP_MBX_REDELIVER_RECORDS && m->kept.len == 0u; ++k)",
           "k < ACMP_MBX_REDELIVER_RECORDS; ++k)", "acmp", "", ""),
    # R2 a refused record does not end the redelivery
    Mutant("rv-bad-continues", C,
           "\t\t\tl->stats.rx_bad += st == MBX_STATUS_BAD;\n\t\t\treturn;",
           "\t\t\tl->stats.rx_bad += st == MBX_STATUS_BAD;\n\t\t\tif (st == MBX_STATUS_BAD) continue;\n\t\t\treturn;",
           "acmp", "", ""),
    # R3 the kept record is not offered first: ring records go ahead of it
    Mutant("rv-ring-before-kept", C,
           "\tif (m->kept.len != 0u) {\n\t\tif (!acmp_rx(",
           "\tif (false) {\n\t\tif (!acmp_rx(", "acmp", "", ""),
    # R4 the redelivery takes a single ring record only
    Mutant("rv-one-record", C,
           "for (unsigned k = 0; k < ACMP_MBX_REDELIVER_RECORDS &&",
           "for (unsigned k = 0; k < 1u &&", "acmp", "", ""),
    # R5 the redelivery runs only when nothing remains owed
    Mutant("rv-only-when-drained", C,
           "\tif (m->acmp.owed_count < owed) {\n\t\tredeliver(m);",
           "\tif (m->acmp.owed_count < owed && m->acmp.owed_count == 0u) {\n\t\tredeliver(m);",
           "acmp", "", ""),
    # R6 the redelivered record is handed to the core directly, a decline not kept
    Mutant("rv-decline-dropped", C,
           "\t\tl->stats.rx_records++;\n\t\ton_frame(m, &l->frame);",
           "\t\tl->stats.rx_records++;\n\t\t(void)acmp_rx(&m->acmp, l->frame.interface, l->frame.bytes, l->frame.len);",
           "acmp", "", ""),
    # R7 the redelivery bound one short in the header constant
    Mutant("rv-bound-short-in-header", "acmp/acmp_mbx.h",
           "#define ACMP_MBX_REDELIVER_RECORDS ACMP_MBX_RX_BACKLOG",
           "#define ACMP_MBX_REDELIVER_RECORDS (ACMP_MBX_RX_BACKLOG - 1u)", "acmp", "", ""),
)
names = {"acmp-poll-owes-nothing-at-one", "acmp-redelivery-takes-no-waiting-record",
         "acmp-redelivery-only-behind-a-kept-command", "acmp-redelivery-refusal-uncounted",
         "acmp-redelivery-records-uncounted", "acmp-redelivery-short-of-a-full-ring"}
NEW = tuple(m for m in acmp_owed_mutants.MUTANTS if m.name in names)
assert len(NEW) == 6, [m.name for m in NEW]
# a reviewer-own defect has no named test: "caught" here means the acmp arm failed (rc 1) with any [FAIL]
orig_caught = ctrl_mutants.caught
ctrl_mutants.caught = lambda test, needle, o: (o.rc == 1 and "[FAIL]" in o.log) if not test else orig_caught(test, needle, o)
ctrl_mutants.unnamed_tests = lambda: []
ctrl_mutants.MUTANTS = NEW + OWN
work.mkdir(parents=True, exist_ok=True)
failed = ctrl_mutants.campaign(work, work / "reuse", jobs)
print("probe:", "some escaped" if failed else "every plant caught")
