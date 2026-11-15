[A781]

## Contents

- **[Status](#status)**: round 5 syncs onto #902's `234bc149` and measures 8x8/1if on the merged images. It is STOPPED to the maintainer on four held-egress rows over their ledger figures. `894-8x8-1if` -> `894-tiers`.
- **[Linked Issue / roles](#linked-issue--roles)**: #894 and #872, with the executor and reviewers.
- **[Description](#description)**: the sync, 8x8/1if's own figures, the measurement and the STOP, round 4's review items, and rounds 1 to 4.
- **[Authoritative references](#authoritative-references)**: the rulings and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the commands to check out the branch.
- **[How to validate](#how-to-validate)**: the reviewer's commands and their expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what waits for the decision, and what stays reported.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

**STOPPED to the maintainer: four of 8x8/1if's seven held-egress rows are over their ledger figures on #902's merged code.** Head `0700f09e`: the merge of #902's `234bc149` (`647d5c4a`) and six commits on it, on round 4's `98c0b62b` (R843-2 and R844-2 POSITIVE there). `894-8x8-1if` -> `894-tiers`, with #902 open at `234bc149`.

- **The STOP.** `egress_ledger.py` fails `backlog.owed_behind1.if0` (63.739 against 63.69 ms), `owed_behind2` (63.957 against 63.91), `service.acmp.last` (62.184 against 62.18) and `service.aecp.last` (61.846 against 61.83).
  - The merge commit `647d5c4a` gives the same seven figures to the microsecond. The growth is #902's merged code's, not this lane's commits after it.
  - The decision is the maintainer's; the ledger figures are not moved by hand.
- **Everything else holds** on the merged image:
  - every measured row the CPU decides is within its bound;
  - joins are 187.397 to 190.147 ms;
  - THE RETRY's 2,453,084 rounds are within their statement;
  - the load is 0.711 of 0.75;
  - no image is over its cap.
  - The six fixed images are byte-identical to `234bc149`'s, so the 1x1/1if and 8x8/2if legs carry.
- **Not run, by the STOP:** item 3's final pass. Quick checks on the clean head pass.

## Linked Issue / roles

Relates to #894
Relates to #872

Executor: `[A781]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned; round 4's was `[R843]`, R843-2)
External reviewer: `[R<n>]` (to be assigned; round 4's was `[R844]`, R844-2)

## Description

### Round 5: the sync onto #902's `234bc149`

**What #902 brings** (`7398ec0a..234bc149`, rounds 11 to 13):
- the one-row map edit's cut;
- SET_CONFIGURATION's cut, and its pace stamp: an accepted SET_CONFIGURATION is paced as a checked edit is, and the paced class is the dearer of a one-row edit's record and its own;
- the SRP drain's limit held to the load gate's `record.srp`;
- four 1x1/1if restatements;
- the slice rule's choice at one interface, 950 us.

**How THE SHAPES keys it.** #902 states its one-interface figures as `(MBX_N_IF == 1u ? ...)`. Keyed so, they would give 8x8/1if 1x1/1if's figures: a 950 us slice under its measured build of one, and a 280 us SRP limit under its measured record. So:

| Piece | Change |
|---|---|
| `ctrl_loop.h` THE SHAPES | The (1, 2, 2) block takes #902's figures: slice 950, build of one 735 and SRP limit 280 us. (1, 9, 9) keeps its own slice and builds, 1,475 / 1,795 / 1,475 us, which the measurement holds: the build of one is 138,906 cycles, 1,460 us by the rule. |
| `load_grade.py` | #902's drain check read the first `CTRL_LOOP_SRP_UNIT_US`, which in THE SHAPES is the 1x1/1if block's. It now reads each point's figure at its shape, and its plants go in that point's block. |
| `poll_grade.py`, `rows_tiers.py`, `selftest_round.py` | The shape-keyed table and point-keyed constants are kept, with #902's ACMP restatements, its `edit_rows` import and its slice-rule checks. |
| `edit_rows.py` | The paced class's point is read by the shape (interfaces and sinks), not by the interface count. 8x8/1if states its own (below). |

**8x8/1if's own figures, by the rule:**
- **The SRP drain limit, 365 us** (`b2737ba5`). It is the load gate's `record.srp` at 8x8/1if, whose records are 8x8/2if's (NEAREST). This is how #894's drain ruling holds the limit at the other points. Its own measured record, 345 us, sat under that statement, so a planted control at 345 is refused naming 8x8/1if, and so is #902's interface-keyed 280.
- **The AECP records by class** (`1a0fedad`). `record_classes.py` now holds 8x8/1if's legs at 8x8/1if's own statements, where it reported them at 1x1/1if's:
  - the paced class, 635 us: an accepted SET_CONFIGURATION, 60,027 cycles, beside a one-row REMOVE's 30,277 (320 us), each in arm B's `aecp-fanout`;
  - the largest legal command's record, 1,510 us (143,648 cycles);
  - an ordinary record, at 8x8/2if's 265 us.
  - A pass is held complete at each point it runs arm A at. Two new controls (an 8x8/1if record over its class's statement, and an 8x8/1if pass missing arm B's SET_CONFIGURATION) bring the self-test to 13 of 13.
- **Two polls** (`d09494c4`): a notice item at 145 us (13,572 cycles) and the walk at 55 (4,905), each over its statement by the rule.

### The measurement and the STOP

114 groups and 1,717 instances, all measured on `a15345f7`'s image. The head carries it with no firmware change since. Every leg ended rc 0 with no STATED line and no refusal:
- arm A whole, 95 groups;
- the answering-every-port arm, 16 groups;
- arm B's `aecp`, `aecp-fanout` and `aecp-largest-notice`.

The transmit-aged control is caught in 8 of 8 groups.

| Row (bound, ms) | Worst measured, ms |
|---|---:|
| AECP (20) | 4.860 |
| ACMP, ADP, MAAP (30) | 7.231, 6.014, 6.255; an ENTITY_AVAILABLE 4.629 |
| SRP (90) | 10.474 |
| MRPDU (49) | 4.114 |
| AECP's notices (20) | 2.168 |
| The first and last queued notice (20, 130) | 2.812, 26.636 |
| The largest legal command, the paced R4L row (238) | 2.547 |

Joins are 352 in 113 groups, 187.397 to 190.147 ms. THE RETRY's 2,453,084 rounds are none over 165 + 255 n + 25 k us. The slices fit 147,500 cycles (SRP 142,809, the build 138,906, THE RETRY's round 92,744). The load is 0.711 at the pin and 0.672 with tsn-c-stack#32, within 0.75.

**The held-egress rows**, graded by `egress_ledger.py`. A new or larger miss fails the leg, by #894's held-egress ruling, item (a).

| Row (`backlog-owed`) | Measured, ms | Ledger, ms | Round 3's, ms |
|---|---:|---:|---:|
| `backlog.owed.if0` | 63.23710 | 63.24 | 63.083 |
| `backlog.owed_behind0.if0` | 63.45889 | 63.47 | 63.305 |
| `backlog.owed_behind1.if0` | **63.73898** | 63.69 | 63.526 |
| `backlog.owed_behind2.if0` | **63.95746** | 63.91 | 63.747 |
| `backlog.owed_behind3.if0` | 64.19076 | 64.20 | 63.969 |
| `backlog-owed.service.acmp.last.if0` | **62.18386** | 62.18 | 62.025 |
| `backlog-owed.service.aecp.last.if0` | **61.84625** | 61.83 | 61.680 |

- On the merge commit `647d5c4a`, before this round's own commits, the seven are the same to the microsecond.
- The service behind the 60 ms hold grew with #902's code. #902 restated ACMP's owed frame on the same move of the code after the map edit.

**The stated-table survey by the rule** (`survey_r5.py`, over every leg, with #665 round 28's tools read only):
- the notice item and the walk, restated above;
- an ADP record, 12,210 cycles in `backlog-adp-refill`, 130 us by the rule. That is against 125 us in 8x8/2if's tsn-c-stack#32 column, which 8x8/1if takes by NEAREST, and is left for the decision. At 130 the #32 column's load moves from 0.6720 to 0.6725.
- Everything else is within its statement, the largest legal notice at 315 of 320 us included.

**Rows by every source at 8x8/1if**: derived and reported, owed to #872, as since round 1.
- R4 is 19.82 ms, the first queued notice 17.83 and R4L 192.81.
- R5 126.36, R6 118.28, the last queued notice 325.90, ACMP 48.37, ADP 48.33, MAAP 49.03, tx 67.24 and txL 134.96 ms stay over their bounds.
- The STOP list's "by any source" is read as a measured row of any arm, as the shape and held-egress rulings state the trigger.

### Round 4's review items

| Item | Disposition |
|---|---|
| R843-2-RES1 (`egress_ledger.py:42`, the first mutant's name) | Fixed (`a15345f7`), wording only. |
| R844-2-R1 (`aecp.h`'s guard sentence) | Fixed (`a15345f7`): "Most units include this header before the table and charge nothing". |
| R843-2-RES2 (PR body: which host arms the assertion holds) | This body: the assertion holds each host arm that compiles `test_aecp.cpp`. The debug arm and the wire comparison keep the tracked contract by design. |
| R843-2-RES3, R844-2-R2 (round 4's carry receipt: stale name and range) | Round 4's packet is published. Its final-head receipt is `firmware/counters-f5-98c0b62b.txt`, and the range is `716a8ae7..98c0b62b`. |
| R843-2-S1 (results-directory mode cannot see a refused group) | Taken (`25c782a4`). A results directory must carry its run's `results.json`, and any refusal there fails. The self-test adds two controls and a mutant, and refuses 9 of 9 mutants. |
| R843-2-S2 (the debug arm and the wire comparison at two interfaces) | Not taken: neither measures THE RETRY's costs, and the debug test configures one interface whatever the arm's count. |
| R843-2-S3 (the packet index) | This round's INDEX is generated after the last edit. |

### Earlier rounds

- **Round 4:** `egress_ledger.py` in the tree; the source-comment rule; THE SHAPES guard in `aecp.h` and each host arm's contract.
- **Round 3:** THE RETRY's round costs keyed on the shape, 165 and 25 us at 8x8/1if.
- **Round 2:** the MRPDU budget, the SRP record, the polls and the notices made the shape's own.
- **Round 1:** THE SHAPES, and 8x8/1if as the flip's other point.

## Authoritative references

- **#894's rulings:**
  - [the held-egress ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6871343905), item (a);
  - [the shape ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730), item (b);
  - [the drain ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6886633874);
  - [round 12](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6883864236) and [round 13](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6888782796);
  - [the retry-cost ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6878014227);
  - [the egress ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867990126).
- **#902's REVIEW READY** at `234bc149` ([issuecomment-6890460677](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6890460677)).
- **#872:** [the second-hart trigger](https://github.com/kebag-logic/milan-fpga/issues/872#issuecomment-6862464924).
- **Documents:** FR_NFR.md 3.4.1, and SPLIT_CONTROL_MEMORY.md section 13 (the ledger table).

## How to get into the same state

```sh
git fetch origin 894-8x8-1if
git switch --detach 0700f09e
git submodule update --init --recursive
```

## How to validate

```sh
python3 -I tb/verilator/ctrl_service_budget/egress_ledger.py --selftest
python3 -I tb/verilator/ctrl_service_budget/record_classes.py --selftest
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <dir> --groups backlog-owed --record-budget-findings --record-share-findings
python3 -I tb/verilator/ctrl_service_budget/egress_ledger.py --point 8x8-1if <dir>/results
```

Expected result / pass criteria:

- **The ledger's self-test** passes, refusing 9 of 9 mutants.
- **The record classes** refuse 13 of 13 planted controls.
- **The load** is 0.711 at 8x8/1if, and the flip check passes there.
- **The `backlog-owed` leg** gives the seven rows above, and **the ledger exits 1** naming the four over their figures. That is the STOP.

## Known limitations / out of scope

- **Waiting for the decision:**
  - the four held-egress rows;
  - the 8x8/1if ADP record against the NEAREST #32 column;
  - then round 5's final pass.
- **The rows by every source at 8x8/1if** stay reported, owed to #872 (figures above).
- **The `valid-destinations` arm** is #895's and is not in this tree.
- **`894-tiers` is now at `4ae887a1`**, eight commits on `234bc149`: `CTRL_LOOP_TX_MS` at two interfaces, 98 to 99 ms, and documents. It is not merged here; the manager relays.
- **`Mailbox.ARoundFillsWhatItsPassHasLeft` at 8x8/1if, and 1x1/1if's SRP record figure**, stay for new Issues, unchanged from round 3.
- **Physical calibration is not run.** Local CPU simulation is not hardware proof.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (STOPPED: the held-egress ledger)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes (the final pass waits for the decision)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
