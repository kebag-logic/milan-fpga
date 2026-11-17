[A781] STOP

Head: `acfa5601` (`894-8x8-1if`, PR #914), round 8: the `--no-ff` merge of dev-soft-core `70f4056f` (`d1c9023b`) and two commits on it, on round 7's `d539f162`. Nothing is pushed.

**Exit: STOP to the maintainer: held-egress rows over their ledger figures on the composed image.** The 8x8/1if measurement, graded with `egress_ledger.py` (a new or larger miss fails the leg; a ledger figure moves only by ruling), fails on six of the seven rows:

| Row (`backlog-owed`, 8x8/1if) | Round 5, ms | Composed, ms | Ledger, ms | Over by, ms |
|---|---:|---:|---:|---:|
| `backlog.owed.if0` | 63.23710 | 63.67337 | 63.40 | 0.27337 |
| `backlog.owed_behind0.if0` | 63.45889 | 63.90106 | 63.64 | 0.26106 |
| `backlog.owed_behind1.if0` | 63.73898 | 64.14858 | 63.93 | 0.21858 |
| `backlog.owed_behind2.if0` | 63.95746 | 64.38819 | 64.16 | 0.22819 |
| `backlog.owed_behind3.if0` | 64.19076 | 64.62511 | 64.41 | 0.21511 |
| `backlog-owed.service.acmp.last.if0` | 62.18386 | 62.49045 | 62.30 | 0.19045 |

The seventh, `backlog-owed.service.aecp.last.if0`, is within: 61.75319 ms against 61.94.

**Where the growth comes from: the composed code, not this round's keying.**
- The measured image (`d1c9023b`'s) differs from the bare composition's in one instruction of each 8x8/1if image. The bare composition is the same tree with 8x8/1if's `CTRL_LOOP_TX_MS` at 1x1/1if's 34 ms. The instruction is the hold-off's, `li a3,2023` to `li a3,2026`; every other instruction and section byte is equal. The head's images are byte-identical to the measured ones.
- Against round 5's measurement (`a15345f7`'s image), six rows are 0.31 to 0.44 ms longer, and `service.aecp.last` is 0.09 ms shorter. Between those images is dev-soft-core's code since `4ae887a1`: #901, SRP's Talker declarations with its pace of 9 ms; #902's later heads are comments and documents.
- What grew is the service behind the 60 ms hold. ACMP's owed frame measures 7,450 cycles in `backlog-owed`, 80 us by the rule against 75; that is restated.
- By the rule at this measurement the six figures would be 63.86, 64.10, 64.36, 64.61, 64.86 and 62.62 ms, and `service.aecp.last` would be 61.85.
- Moving them is the maintainer's: [#894's ledger ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6892938049), item 3, allows a restatement only by ruling, and only for growth reproduced at a ruled upstream head.

**The merge, `d1c9023b`.** Nine files conflicted: the six named, plus the SRP README, the harness README and `poll_grade.py`. Each is resolved keeping both sides; the PR body has the resolution table. Two bounds are keyed per shape in THE SHAPES, so one shape's figure is never another's:
- **`AECP_QUEUED_MS`:** 140 ms at 1x1/1if (#901's), 130 at 8x8/1if (this PR's), 62 at two interfaces. It is `CTRL_LOOP_QUEUED_MS`, and its readers and planted controls follow; `shape_costs.py` refuses it put back on the interface count, naming 8x8/1if.
- **`CTRL_LOOP_TX_MS`:** 34, 70 and 105 ms. #901 makes it a term of a withdrawn Talker's hold-off (IEEE 802.1Q-2018 35.2.2.8: two LeaveAllTime periods after the Leave departs).
  - Keyed on the interface count, 8x8/1if would take 1x1/1if's 34 ms, against its own tx row of 69.84 ms by every source, so the hold-off would undercount the Leave's latest departure there.
  - The hold-off is now 2,026 cs at 8x8/1if, 2,023 at 1x1/1if and 2,030 at two interfaces.
  - `ctrl_loop.c`'s assertion holds 1x1/1if alone, keyed on its shape. 8x8/1if's rows by every source are reported, as 8x8/2if's are.
  - This keying is for the composition review.
- **Not keyed:** the pace, #901's 9 ms, one figure at every shape on both sides.
- **The other images:** the six 1x1 and 8x8/2if images are byte-identical to `70f4056f`'s, so #901's measurement carries there.

**Every other criterion holds on the composed image:**
- **The measurement:** 116 groups and 1,736 instances, every leg exiting 0 at the restated statements. The legs cover arm A, the answering-every-port arm, the answering-ports arm's `aecp`, `aecp-fanout` and `aecp-largest-notice`, and the `valid-destinations` arm, new in this tree. The transmit-aged control is caught in 8 of 8 groups.
- **The rows the CPU decides, measured,** each within its bound: AECP 4.719 (20), ACMP 7.611, ADP 6.973 and an ENTITY_AVAILABLE 5.099, MAAP 6.143 (30), SRP 9.929 (90), MRPDU 2.296 (49), AECP's notices 3.132 (20), the first queued notice 2.649 (20), the last 25.646 (130), and the largest legal command 3.599 (238 ms).
- **SRP's Talker declaration rows:** each carries a JoinTime's wait, and the worst is 189.688 ms against its 220 ms harness budget.
- **Joins, slices and THE RETRY:** joins are 383 in 115 groups, 186.613 to 190.363 ms. The slices are SRP's 119,542, the build 91,604 and THE RETRY's round 92,686 cycles, each within 147,500. THE RETRY's 2,303,370 rounds are none over their statement.
- **The load:** 0.718 at the pin and 0.677 with tsn-c-stack#32, within 0.75. 1x1/1if's rows all hold by every source (the flip check), and its load is 0.517 and 0.514, within 0.70.
- **The record classes** pass at 8x8/1if's restated statements.
- **ROM per image** (`plat_ledger.py`, PASS at four points, 7 of 7 controls):

  | Point | ROM, B | RAMB36 |
  |---|---:|---|
  | 1x1-if1 | 117,488 | 43 |
  | 1x1-if2 | 119,072 | 44 |
  | 8x8-if1 | 130,200 | 56 of 56 |
  | 8x8-if2 | 131,752 | 60.5, its override |

  No image is past its entry.
- **lwSRP and every donor are unchanged.**

**Restated by the rule** on the composed image (`84c1704d`, `acfa5601`), with the legs regraded at those statements and no STATED line left:

| Cost at 8x8/1if | Measured, cycles | Stated now, us | Before, us |
|---|---:|---:|---:|
| The polls' base | 23,756 | 250 | 235 |
| ACMP's owed frame | 7,450 | 80 | 75 |
| Its own MAAP record (a range lost to a peer in `valid-destinations`) | 16,323 | 175 | 155, 8x8/2if's |
| The largest legal command's record | 162,969 | 1,715 | 1,510 |
| The paced class (an accepted SET_CONFIGURATION; a one-row edit 31,449, 335) | 65,169 | 685 | 635 |

THE TRANSMIT's figure moves to 70 ms for 69.84 with the hold-off unchanged.

**#918's three stated-cost lines** (builds during link-up over one interface's 1,010 and 735 us) do not arise on the composed image: 8x8/1if's builds are its shape's 1,795 and 1,475 us, and no leg prints a STATED line on a pass given whole. The heaviest build of one is 91,604 cycles, within 147,500.

**For the maintainer, beside the ledger:**
- **The build's coverage.** Since #901 a Talker declares only while its destination is valid. So arm A's `srp` group builds its Listener Ready with no Talker declaration (42,796 cycles, against 138,906 before), and the `valid-destinations` arm declares Talkers with no Listener (91,604). No group now composes both, the build 8x8/1if's slice and builds were measured on. They are kept, since a statement over its measurement is not the defect, and a group that composes both is owed.
- **The rows by every source at 8x8/1if** are reported, owed to #872. R4 is now over its bound at 20.96 ms against 20; R5 is 129.34, the last queued notice 347.75 and txL 148.97 ms; with every AECP command the largest legal one the load is 1.017. I read the STOP list's "any row" as a measured row, by round 6's item 1. If it meant these derived rows, R4 is a second STOP reason.

**Not run, by the STOP:** item 3's gates on a clean clone of the final head: the firmware units and campaigns, `fw_coverage --check`, the docs jobs, the harness self-tests and lane gates, and verilator shards 1, 3, 4, 6, 10 and 17 of 19, the ones whose suites build the split firmware. Their scripts are in the packet. Quick checks on a clean clone of `acfa5601` all pass, 18 of 18:
- the shape table, 25 of 25;
- the flip check, 612 of 612, and both points;
- rows_tiers, 1,033 of 1,033;
- the load gate, 28 of 28 and `--check`;
- record classes, 14 of 14, and R843-3's mixed-point probe;
- the ledger, 13 mutants;
- docs_check and the idiom gates;
- both comment scans and R844-1's audit, 0 lines;
- the diff checks.
