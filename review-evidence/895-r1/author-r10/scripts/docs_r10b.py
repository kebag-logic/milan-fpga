#!/usr/bin/env python3
"""docs_r10b.py TREE: round 10's second documentation pass (lane 895): section 13's subsection "The record classes
graded (#895)" (R836-4-F2: the head's class grader over every held leg, the class maxima, the planted controls, the
corrected survey's coverage), the survey's coverage claims of rounds 6, 7A and 8 corrected, and the hold-off's THE
TRANSMIT term's test (R835-4-F1) in THE TRANSMIT's figure's subsection. Markdown only; each replacement unique."""
import sys
from pathlib import Path

tree = Path(sys.argv[1])
C = '#the-record-classes-graded-895'
X = '#the-transmits-figure-at-two-interfaces-895'
R836 = 'https://github.com/kebag-logic/milan-fpga/pull/901#issuecomment-6899966960'
R835 = 'https://github.com/kebag-logic/milan-fpga/pull/901#issuecomment-6900107977'


def edit(path, pairs):
    p = tree / path
    t = p.read_text()
    for old, new in pairs:
        assert t.count(old) == 1, (path, t.count(old), old[:100])
        t = t.replace(old, new)
    p.write_text(t)


section = f"""
### The record classes graded (#895)

[R836-4's review of #901]({R836}) found the cost survey of rounds 6 to 9 short on two of AECP's record classes. Its `EDIT_RECORD_US` row looked for a class `record_classes.py` never names, so the paced class read no record and printed "not staged". And it called `record_classes.held` without the record's command, so arm B's `aecp-fanout` SET_STREAM_INFO, which the formal measurement holds only with its command, was left out of the ordinary class. Both are answered on round 8's legs, which carry to this head ([above]({X})):

- **The head's class grader over every held leg** (`record_classes.py` over arm A, the `answering-every-port` and `valid-destinations` arms and arm B, at both points, in one pass) gives RESULT PASS. The dearest record of each class, by the rule, against its statement:

  | Point | Class | Dearest record | CPU cycles | By the rule | Stated |
  |---|---|---|---:|---:|---:|
  | 1x1/1if | paced (`EDIT_RECORD_US`) | arm B's accepted SET_CONFIGURATION | 28,288 | 300 us | 300 us |
  | 1x1/1if | ordinary (`record.aecp`) | `answering-every-port`, `notice-burst-0` | 21,187 | 225 us | 235 us |
  | 1x1/1if | long (`LONG_RECORD_US`) | arm B, `aecp-largest-notice` | 86,698 | 915 us | 975 us |
  | 8x8/2if | paced | arm B's accepted SET_CONFIGURATION | 55,365 | 585 us | 595 us |
  | 8x8/2if | ordinary | `answering-every-port`, `notice-every-7` | 18,904 | 200 us | 265 us |
  | 8x8/2if | long | arm B, `aecp-largest-notice` | 126,152 | 1,325 us | 1,650 us |

  Arm B's SET_STREAM_INFO is 20,363 cycles at 1x1/1if (215 us) and at most 17,511 at 8x8/2if (185 us), each held in the ordinary class and within it. 8x8/1if is reported by class and never held (`record_classes.held`), and this branch has no leg there.
- **No statement moves.** Every class's dearest record is within its statement by the rule, the paced class at 1x1/1if at its 300 us exactly, so the rows, the load, the pace and the slice stand.
- **The survey corrected** reads the paced class under its key, gives `held` the record's command and counts `record.aecp` like every other statement. At each point it holds 63 statements: 57 measured, each within by the rule, and 6 derived and not staged (the probe's item; the polls' owed MRPDU, and in the donor column the owed MRPDU and a build of both MRPDUs; and the pass given whole's build). The rows also read `aecp_mbx.h`'s round costs, which each leg's round check holds, and `CTRL_LOOP_TICK_US`, a floor under the centisecond the survey holds.
- **Planted on the same path.** An accepted SET_CONFIGURATION raised over the paced record (40,000 cycles at 1x1/1if, 60,000 at 8x8/2if), and a SET_STREAM_INFO raised over the ordinary record (30,000 at each point), each in a copy of arm B's leg. The class grader over every leg refuses each, naming the record, and the corrected survey refuses each (UNDER 1). Round 8's survey passed all four: the two defects, each now caught.
"""
edit('docs/design/SPLIT_CONTROL_MEMORY.md', [
    ("Every stated cost the rows read is held to those legs by the rule, the most measured plus 5 % and rounded up to "
     "5 us",
     "Every stated cost the rows read is held to those legs by the rule (but the paced record class, of which that "
     "survey read no record, and arm B's SET_STREAM_INFO, which it left out of the ordinary class: [the record classes "
     "graded](" + C + ")), the most measured plus 5 % and rounded up to 5 us"),
    ("Every stated table the rows read was held to those legs by the rule, as [above](#the-composition-measured-again-895).",
     "Every stated table the rows read was held to those legs by the rule, as [above](#the-composition-measured-again-895), "
     "with the same two record-class exceptions."),
    ("No stated cost is under its rule figure, so the bound and the slice settle after the one rebuild.",
     "No stated cost the survey measured is under its rule figure, so the bound and the slice settle after the one "
     "rebuild; that survey read no paced record and left arm B's SET_STREAM_INFO out of the ordinary class, which [the "
     "record classes graded](" + C + ") answers, no statement moving."),
    ("- **Refused** (item 3): a statement under its row, and a second source for the hold-off's term.\n",
     "- **Refused** (item 3): a statement under its row, and a second source for the hold-off's term.\n"
     "- **The term held** ([R835-4's review of #901](" + R835 + ")). "
     "`Talker.ChangedDestinationWaitsTwoLeaveAllTimePeriodsAfterTheLatestLeave` (`srp_talker.cpp`) requests the Leave on "
     "a centisecond and holds the loop a JoinTime and `CTRL_LOOP_TX_MS` after it, the latest the Leave can leave, and "
     "requires the changed destination no sooner than two LeaveAllTime periods after the Leave on the wire: 20,005 ms "
     "at two interfaces and 20,006 at one. The Talker campaign plants the hold-off without THE TRANSMIT's term (19,895 "
     "and 19,966 ms), with it rounded down (19,995 and 19,996) and without the JoinTime's either, each caught by name at "
     "1x1/1if and at 8x8/2if.\n"),
    ("([section 3](#3-named-refusals)), and `plat_ledger.py` passes at every point.\n",
     "([section 3](#3-named-refusals)), and `plat_ledger.py` passes at every point.\n" + section),
])
print('ok')
