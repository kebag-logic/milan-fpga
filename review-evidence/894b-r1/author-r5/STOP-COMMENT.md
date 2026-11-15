[A781] STOP

Head: `0700f09e` (`894-8x8-1if`, PR #914), round 5: the merge of #902's `234bc149` (`647d5c4a`) and six commits on it. The round started from round 4's `98c0b62b`. Nothing is pushed.

**Exit: STOP to the maintainer, on round 5's list: held-egress rows over their ledger figures.** The 8x8/1if measurement on the merged image, graded with `egress_ledger.py` (a new or larger miss fails the leg; the ledger figures are not moved by hand), fails on four of the seven rows:

| Row (`backlog-owed`, 8x8/1if) | Measured, ms | Ledger, ms | Over by, ms |
|---|---:|---:|---:|
| `backlog.owed_behind1.if0` | 63.73898 | 63.69 | 0.04898 |
| `backlog.owed_behind2.if0` | 63.95746 | 63.91 | 0.04746 |
| `backlog-owed.service.acmp.last.if0` | 62.18386 | 62.18 | 0.00386 |
| `backlog-owed.service.aecp.last.if0` | 61.84625 | 61.83 | 0.01625 |

The other three are within their figures: `backlog.owed.if0` 63.23710 (63.24), `owed_behind0` 63.45889 (63.47), `owed_behind3` 64.19076 (64.20).

**Where the growth comes from: #902's merge, not this lane's commits after it.**
- `backlog-owed` run alone on a clean clone of the merge commit `647d5c4a` gives all seven rows identical to the head's to the microsecond. That commit predates this round's own changes, its SRP drain limit still 345 us.
- Against round 3's measurement at `716a8ae7` (63.083 / 63.305 / 63.526 / 63.747 / 63.969 / 62.025 / 61.680), each row is 0.154 to 0.222 ms longer.
- The rows are set by the scenario's 60 ms egress hold. What grew is the service behind it: the owed ACMP frames and the records behind them.
- #902's round 11 restated ACMP's owed frame from 50 to 55 us at 1x1/1if and from 65 to 70 at 8x8/2if, because the code after the map edit moved.
- No source change is proposed here. Moving a ledger figure, or ruling the growth, is the maintainer's decision.

**Every other round-5 criterion holds** on the merged image (`a15345f7`'s, which the head carries unchanged: no firmware change since):
- **Images.** The six fixed images (fixture and platform at 1x1/1if, 1x1/2if, 8x8/2if) are byte-identical to `234bc149`'s by ELF and loadable sha256, so the 1x1/1if and 8x8/2if legs carry. The 8x8/1if platform image is 56.0 RAMB36 (1,448 B of ROM spare).
- **The measurement.** 114 groups, 1,717 instances, all measured, every leg rc 0, no STATED line, no refusal:
  - arm A whole (95 groups);
  - the answering-every-port arm (16);
  - arm B's `aecp`, `aecp-fanout` (its accepted SET_CONFIGURATION and SET_STREAM_INFO) and `aecp-largest-notice`.
  - The transmit-aged control is caught in 8 of 8 groups.
  - The `valid-destinations` arm is #895's, not in this tree, so it is not run.
- **The rows the CPU decides, measured**, each within its bound: AECP 4.860 (20), ACMP 7.231, ADP 6.014 and an ENTITY_AVAILABLE 4.629, MAAP 6.255 (30), SRP 10.474 (90), MRPDU 4.114 (49), AECP's notices 2.168 (20), the first queued notice 2.812 (20), the last 26.636 (130), and the largest legal command's rows 2.547 (238 ms).
- **Joins:** 352 in 113 groups, 187.397 to 190.147 ms, within 181 to 239.
- **Slices:** SRP's 142,809 cycles, the build 138,906 and THE RETRY's round 92,744, each within the stated 147,500. The build of one is 1,460 us by the rule, under its 1,475.
- **THE RETRY:** 2,453,084 rounds, none over 165 + 255 n + 25 k us.
- **The load:** 0.711 at the pin and 0.672 with tsn-c-stack#32, within 0.75. One pass of `aecp-largest-notice` is over THE SHARE (202,546 cycles), reported as before.
- **lwSRP and every donor are unchanged.**

**The sync and 8x8/1if's own figures** (THE SHAPES; never keyed on the interface count alone):
- **#902's one-interface figures** (the slice rule's 950 us, a build of one of 735 us, the SRP drain limit of 280) go to THE SHAPES' 1x1/1if block. 8x8/1if keeps its own slice and builds (1,475 / 1,795 / 1,475 us), which the measurement holds.
- **8x8/1if's SRP drain limit is 365 us** (`b2737ba5`). That is the load gate's `record.srp` there, whose records are 8x8/2if's (NEAREST), as #894's drain ruling holds the limit at the other points. Its own measured 345 us sat under that statement, and a planted control at 345 is refused naming 8x8/1if.
- **8x8/1if's AECP records are held at its own statements by the rule** (`1a0fedad`; `record_classes.py` held them at 1x1/1if's and reported them):
  - the paced class at 635 us, an accepted SET_CONFIGURATION's 60,027 cycles beside a one-row edit's 30,277 (320 us), read by the shape;
  - the largest legal command's record at 1,510 us (143,648 cycles).
  - The record classes pass at those statements. The self-test refuses 13 of 13.
- **The stated-table survey by the rule** over every leg finds three statements under their measurement:
  - a notice poll item, 13,572 cycles, 145 against 140 us, restated at 145 (`d09494c4`);
  - the walk, 4,905, 55 against 50, restated at 55 (`d09494c4`);
  - an ADP record of 12,210 cycles in `backlog-adp-refill`, 130 us by the rule against the 125 us that 8x8/2if's tsn-c-stack#32 column states. 8x8/1if takes that column by NEAREST, so this one is **left for the decision**. Charged at 130 it moves the #32 column's load from 0.6720 to 0.6725.
- **Round 4's residues** are fixed in wording (`a15345f7`), and R843-2's S1 is taken (`25c782a4`): a results directory's run refusals now fail the ledger, with its controls and a mutant.

**The rows by every source at 8x8/1if** are derived and reported, owed to #872, as since round 1. At the head, with 8x8/1if's own paced class and polls:
- within their bounds: R4 19.82 (20), the first queued notice 17.83 (20), R4L 192.81 (238);
- over their bounds: R5 126.36 and R6 118.28 (90), the last queued notice 325.90 (130), ACMP 48.37, ADP 48.33 and MAAP 49.03 (30), tx 67.24 and txL 134.96 (49).

I read the STOP list's "an 8x8/1if CPU-decided row over its bound by any source" as a measured row of any arm. That is how the shape ruling (b) and the held-egress ruling (a) state 8x8/1if's trigger, and how FR_NFR 3.4.1 reports those rows. If the list meant these derived rows, it is a second STOP reason.

**Not run, by the STOP:** item 3's final pass (every hosted job step, the four-shard sweep, the campaigns, the docs and lane gates on clean clones). Its scripts are in the packet. Quick checks on the clean head pass: the ledger 9 of 9 mutants, record classes 13/13, the shape table, load 26/26, flip 611/611, rows_tiers 1033/1033, the idiom and docs gates, and diff checks against `234bc149` and `98c0b62b`.

**`894-tiers` has since moved to `4ae887a1`** (eight commits on `234bc149`). Its code change is `CTRL_LOOP_TX_MS` at two interfaces, 98 to 99 ms; the rest is comments and documents. It is not merged here, by the round's instruction; the manager relays.

**Decision needed:** what the four held-egress rows' growth on #902's merged code means for 8x8/1if's ledger, and how the 8x8/1if ADP record against the NEAREST #32 column is stated. With those, round 5's final pass runs at the head.
