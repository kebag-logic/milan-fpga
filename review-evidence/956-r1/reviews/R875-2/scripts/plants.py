"""Reviewer plant driver (#956/#957), with a checkout's own campaign code; every disposable tree stays under <out>.
  python3 -B plants.py <checkout> <out> srp <interfaces> <entity|-> <name>[,<name>...]   named rows of the SRP table
  python3 -B plants.py <checkout> <out> own <interfaces> <entity|-> <name>[,<name>...]   the reviewer's own plants
  python3 -B plants.py <checkout> <out> aecp <name>[,<name>...]                          named rows of the AECP table
Prints one [ok]/[ESCAPED] line per plant and CAMPAIGN ALL CAUGHT or FAIL; exit status 1 on any escape."""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
mode, out = sys.argv[3], Path(sys.argv[2]).resolve()
names = set(sys.argv[-1].split(","))
if mode in ("srp", "own"):
    import srp_mutants  # noqa: E402
    if mode == "own":
        D = srp_mutants.Defect
        own = (
            # a whole build keeps the due it was made for, so THE TRANSMIT never settles
            D("r875-whole-build-keeps-its-due", "Srp.ABuildPausedBetweenSlicesStaysOwedAndKeepsWhatCameDue",
              "    const unsigned again = resume != 0u ? m->tx_due : 0u;\n",
              "    const unsigned again = m->tx_due;\n", "(the start settles owing THE TRANSMIT nothing)"),
            # the reset leaves the record at Ready, not none: the first Ready after it is not noticed
            D("r875-reset-records-ready", "Talker.ListenerRegistrationAfterAResetIsNoticed",
              "        i->declaration[k] = 0u;\n", "        i->declaration[k] = 2u;\n",
              "the first Listener registration after a reset is noticed, whatever the one before it declared",
              suite="srp_talker.cpp", entity="endstation_ax7101_8x8"),
            # the reset clears only the first source's record
            D("r875-reset-clears-source-0-only", "Talker.ListenerRegistrationAfterAResetIsNoticed",
              "        i->declaration[k] = 0u;\n", "        i->declaration[k] = k == 0u ? 0u : i->declaration[k];\n",
              "the first Listener registration after a reset is noticed, whatever the one before it declared",
              suite="srp_talker.cpp", entity="endstation_ax7101_8x8"),
        )
        srp_mutants.DEFECTS = tuple(d for d in own if d.name in names)
    else:
        srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name in names)
    assert {d.name for d in srp_mutants.DEFECTS} == names, ("missing", names - {d.name for d in srp_mutants.DEFECTS})
    entity = "" if sys.argv[5] == "-" else sys.argv[5]
    failed = srp_mutants.campaign(out, (root / "third_party/lwSRP").resolve(), 2, int(sys.argv[4]), entity)
else:
    import aecp_mutants  # noqa: E402
    aecp_mutants.DEFECTS = tuple(d for d in aecp_mutants.DEFECTS if d.name in names)
    assert {d.name for d in aecp_mutants.DEFECTS} == names, ("missing", names - {d.name for d in aecp_mutants.DEFECTS})
    aecp_mutants.controls = lambda: None  # the full-table drift control; this run plants a named subset
    failed = aecp_mutants.campaign(out, 2)
print("CAMPAIGN", "FAIL" if failed else "ALL CAUGHT", sorted(names), flush=True)
sys.exit(1 if failed else 0)
