[A781]

## Contents

- **[Status](#status)**: rounds 5 to 7. The lane is synced onto #902's `4ae887a1`; 8x8/1if is measured on the merged image, its held-egress ledger and its ADP record are restated by rule, and round 7 answers R843-3 and R844-3. `894-8x8-1if` -> `894-tiers`.
- **[Linked Issue / roles](#linked-issue--roles)**: #894 and #872, with the executor and reviewers.
- **[Description](#description)**: the finding-by-finding table, the sync, 8x8/1if's own figures, the measurement, the restatements, and the earlier rounds.
- **[Authoritative references](#authoritative-references)**: the rulings and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the commands to check out the branch.
- **[How to validate](#how-to-validate)**: the reviewer's commands and their expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what stays reported or open.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

**8x8/1if holds on #902's merged code, with its held-egress ledger and its ADP record restated by rule.** Head `d539f162`, on round 6's `af2c4d7a` (R844-3 POSITIVE there, R843-3 NEGATIVE on two MINORs), itself on round 4's `98c0b62b` (R843-2 and R844-2 POSITIVE there). `894-8x8-1if` -> `894-tiers`, with #902 open at `4ae887a1`, which is merged here.

- **The sync.** #902's `234bc149` (round 5) and `4ae887a1` (round 6) are merged. Its one-interface figures go to THE SHAPES' 1x1/1if block, and 8x8/1if keeps its own.
- **The measurement** is on the merged image: 114 groups and 1,717 instances, every leg rc 0 with no STATED line.
  - Every measured row the CPU decides is within its bound.
  - Joins are 187.397 to 190.147 ms.
  - THE RETRY's 2,453,084 rounds are within their statement.
  - The load is 0.711 of 0.75.
  - All eight images at the `4ae887a1` merge are byte-identical to the measured ones, so the measurement carries.
- **Round 5's STOP** (four held-egress rows over round 1's ledger figures, the growth #902's merged code's) is ruled.
  - The ledger is restated by rule, derived in the tool from the scenario's 60 ms hold.
  - 8x8/1if states its own ADP record.
  - Round 5's measurement regrades PASS.
- **Round 7** (`d2fd8975`, `d0fea5f0`, `d539f162`) fixes R843-3's two MINORs and both reviews' residue: section 13 states 8x8/1if's gate as measured on the head's image, and `record_classes.py` holds a pass complete at every point it runs any leg at again. No firmware or image changes: all eight images are byte-identical to `af2c4d7a`'s. See [Round 7's gates](#round-7s-gates-at-d539f162).
- **Round 6's final pass at `af2c4d7a`** was clean; see [The final pass](#the-final-pass-at-af2c4d7a).

## Linked Issue / roles

Relates to #894
Relates to #872

Executor: `[A781]`
Internal cleared-context reviewer: `[R843]` (R843-3 at `af2c4d7a`, NEGATIVE on two MINORs; the re-review of `d539f162` to be assigned)
External reviewer: `[R844]` (R844-3 at `af2c4d7a`, POSITIVE)

## Description

### Finding by finding

| Finding or ruling item | Disposition | Commit, evidence |
|---|---|---|
| R843-2-RES1: `egress_ledger.py:42` and the first mutant's name carry history | Fixed, wording only | `a15345f7` |
| R844-2-R1: `aecp.h`'s guard sentence contradicts `aecp.c`'s include order | Fixed: "Most units include this header before the table and charge nothing" | `a15345f7` |
| R843-2-RES2: the PR body over-states which host arms the assertion holds | This body: the assertion holds each host arm that compiles `test_aecp.cpp`. The debug arm and the wire comparison keep the tracked contract by design. | — |
| R843-2-RES3, R844-2-R2: round 4's carry receipt names a stale file and range | Round 4's packet is published. Its final-head receipt is `firmware/counters-f5-98c0b62b.txt`, and the range is `716a8ae7..98c0b62b`. | — |
| R843-2-S1: results-directory mode cannot see a refused group | Taken: a results directory must carry its run's `results.json`, and any refusal there fails; two controls and a mutant | `25c782a4` |
| R843-2-S2: the debug arm and the wire comparison at two interfaces | Not taken: neither measures THE RETRY's costs, and the debug test configures one interface | — |
| R843-2-S3: the packet index | Each round's INDEX is generated after its last edit | — |
| Round 5's STOP: four held-egress rows over round 1's ledger on #902's merged code | Ruled in round 6 (below). The bare merge `647d5c4a` gives the same figures to the microsecond. | `receipts/harness/attribution-backlog-owed-647d5c4a.txt` (round 5) |
| Round 6, item 1: the trigger reading | Confirmed: a measured CPU-decided row over its bound, or the load over 0.75. The every-source rows stay reported. | — |
| Round 6, item 2: the held-egress ledger restated by rule | See [The held-egress ledger](#the-held-egress-ledger-derived-by-rule-item-2). The tool derives each figure; section 13 shows both measurements and the attribution. | `6bf90e0d` |
| Round 6, item 3: they stay recorded misses | `egress_ledger.py` still fails a new or larger miss. A later restatement needs a ruling (section 13). | `6bf90e0d` |
| Round 6, item 4: 8x8/1if's own ADP record | 130 us by the rule where its nearest point's #32 column states 125, held with controls. 8x8/2if's table is untouched. The load is 0.711 and 0.673. | `f8ea6d72` |
| Round 6, item 5: the sync, the carry, the controls, the final pass | `4ae887a1` merged; all eight images identical to round 5's measured ones; the final pass at the head | `5aadbc8c`; `receipts/images/` |
| The final pass's comment scans: four new source-comment lines in `egress_ledger.py` and `load_grade.py` named a review round | Fixed: they name #894's ledger ruling by its subject and items, and section 13 links it. The pass ran again at the new head. | `af2c4d7a` |
| Round 6, item 6: an image over its entry is reported | No image is past its entry (see the final pass) | — |
| R843-3-F1 (MINOR; Docs, Conformance): section 13 states 8x8/1if's gate, its load and its every-source rows from round 3's superseded image | Fixed. Section 13 states the gate as measured on the head's image: round 5's measurement of `a15345f7`'s image, carried by byte identity, with its 114 groups, rows, queued notices, largest command, joins, slices and THE RETRY's rounds. The load is 0.711 and 0.673 everywhere it is stated. The every-source rows and the load with every command the largest (0.969) are as the head derives them, with the largest command's record at 1,510 us. Round 3's figures stay as labelled history, and FR_NFR 3.4.1 cites the gate. The receipt link names its archive commit by short ID. | `d0fea5f0`, `d539f162` |
| R843-3-F2 (MINOR; Tests, Robustness): a mixed-point pass skips 1x1/1if's completeness | Fixed. Completeness is held at every point of `COMPLETE` the pass runs any leg at, as #902's `647d5c4a` held 1x1/1if, and an 8x8/1if-only pass still runs. R843-3's probe input is refused by name with the two findings `647d5c4a` gives. A planted control holds it (14 of 14), and it escapes on `af2c4d7a`'s rule. | `d2fd8975` |
| R843-3-R1, R844-3-R2: `MAILBOX_SPLIT.md:390` keys the slice on the interface count | Fixed with both exact fixes together: "stated for each shape (THE SHAPES): the slice rule's choice at 1x1/1if, 0.95 ms, 1.475 ms at 8x8/1if, and 1.3 ms at two interfaces", with THE SHAPES linked | `d0fea5f0` |
| R843-3-R2: `FR_NFR.md:394`'s ledger citation has no link | Fixed: "([#894's ledger ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6892938049), item 2)". Section 13's two citations of that ruling take the same name. | `d0fea5f0` |
| R844-3-R1: `record_classes.py:96` calls 8x8/1if "reported" | Fixed: "(#894's 8x8/1if shape)" | `d2fd8975` |
| R844-3-R3: section 13 :2547 and :2593 carry round-3 figures beside current ones | Fixed with F1. "The round-3 load record" and "Round-3 reported rows, owed to #872" label them, with their numbers unchanged, and the current rows link the round-6 receipt. | `d0fea5f0` |
| R844-3-R4: this body's survey bullet reverses the relation | Fixed: "The survey over every leg finds every measurement within its statement by the rule." | this body |
| R843-3-S1: 8x8/1if's retained retry at its measured record, not its unit | Not taken. Section 13 states it ("the measured record stays the retained retry's cost"). It is the stricter apply check, and the survey holds it: 316.40 us measured, 335 by the rule, against 345. | — |
| R843-3-S2 (R843-2-S2, retained) | Not taken, as before | — |

### The sync onto #902

**What #902 brought** to `234bc149` (round 5):
- the one-row map edit's cut;
- SET_CONFIGURATION's cut and its pace stamp, with the paced class at the dearer of a one-row edit and an accepted SET_CONFIGURATION;
- the SRP drain's limit held to the load gate's `record.srp`;
- four 1x1/1if restatements;
- the slice rule's 950 us at one interface.

To `4ae887a1` (round 6) it brought `CTRL_LOOP_TX_MS` at two interfaces, 98 to 99 ms (read by a static assertion), and documents.

**How THE SHAPES keys it.** #902's one-interface figures are stated as `(MBX_N_IF == 1u ? ...)`. Keyed so, they would give 8x8/1if 1x1/1if's, under its own measurements.

| Piece | Change |
|---|---|
| `ctrl_loop.h` | The (1, 2, 2) block takes #902's figures: slice 950, build of one 735 and SRP limit 280 us. 8x8/1if keeps its own slice and builds: 1,475 / 1,795 / 1,475 us. |
| `load_grade.py` | #902's drain check now reads each point's figure at its shape. 8x8/1if's limit is 365 us, the load gate's `record.srp` there (NEAREST), held with a plant at its measured 345. |
| `record_classes.py`, `edit_rows.py`, `rows_tiers.py` | 8x8/1if's AECP records are held at its own statements: the paced class at 635 us (an accepted SET_CONFIGURATION's 60,027 cycles beside a one-row edit's 30,277) and the long record at 1,510 us (143,648 cycles). The class's point is read by the shape. |
| `poll_grade.py` | 8x8/1if's walk is restated at 55 us and its notice item at 145, by the rule. |

### The measurement on the merged image

114 groups and 1,717 instances, all measured, every leg rc 0, no STATED line, no refusal:
- arm A whole, 95 groups;
- the answering-every-port arm, 16;
- arm B's `aecp`, `aecp-fanout` (its accepted SET_CONFIGURATION and SET_STREAM_INFO) and `aecp-largest-notice`.

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

- **Joins:** 352 in 113 groups, 187.397 to 190.147 ms.
- **Slices:** SRP's 142,809, the build's 138,906 and THE RETRY's round 92,744 CPU cycles, each within 147,500.
- **THE RETRY:** 2,453,084 rounds, none over its statement.
- **The load:** 0.711 at the pin and 0.673 with tsn-c-stack#32, within 0.75. One pass of `aecp-largest-notice` is over THE SHARE, reported as before.
- **The images:** the eight at the `4ae887a1` merge `5aadbc8c` are byte-identical, by ELF and loadable sha256, to round 5's measured `a15345f7` images. The six fixed images are identical to #902's `4ae887a1`'s too, so the 1x1/1if and 8x8/2if legs carry.

### The held-egress ledger, derived by rule (item 2)

`egress_ledger.py` reads the scenario's egress hold from `scenario.py`'s `backlog-owed` group (60 ms). Each figure is the hold plus the service behind it at the merged image's measurement plus 5 %, rounded up to 0.01 ms, in integer 10 ns units. These figures are the tool's output:

| Row | At `716a8ae7`, ms | On #902's `234bc149` merged, ms | Ledger, ms |
|---|---:|---:|---:|
| `backlog.owed.if0` | 63.083 | 63.23710 | 63.40 |
| `backlog.owed_behind0.if0` | 63.305 | 63.45889 | 63.64 |
| `backlog.owed_behind1.if0` | 63.526 | 63.73898 | 63.93 |
| `backlog.owed_behind2.if0` | 63.747 | 63.95746 | 64.16 |
| `backlog.owed_behind3.if0` | 63.969 | 64.19076 | 64.41 |
| `backlog-owed.service.acmp.last.if0` | 62.025 | 62.18386 | 62.30 |
| `backlog-owed.service.aecp.last.if0` | 61.680 | 61.84625 | 61.94 |

- **The growth is #902's merged code's:** the bare merge `647d5c4a` gives the same seven figures to the microsecond. Section 13 shows both measurements and the attribution.
- **Its self-test** holds section 13's table to the tool, the derivation to an independent decimal computation, and the hold to the scenario.
  - 35 controls run in process and as a process. One bus cycle over each restated figure exits 1 naming the row, and a new miss exits 1.
  - 13 mutants are refused, among them a figure without its 5 %, the 5 % taken on the hold too, a measurement the ledger does not derive from, and a hold not the scenario's.
- **The regrade:** round 5's measurement, graded at the head, passes. Each row is under its figure by 0.094 to 0.219 ms.

### 8x8/1if's own ADP record (item 4)

The nearest point supplies a cost only while 8x8/1if's measurement is within it.
- **The measurement:** an ADP record of 12,210 cycles in arm A's `backlog-adp-refill`, 130 us by the rule. 8x8/2if's tsn-c-stack#32 column states 125.
- **The statement:** 8x8/1if states its own 130 us (`load_grade.OWN`). The pin column's 240 still supplies it there, and 8x8/2if's table is untouched.
- **Its check:** `--check` holds the own figure to its measurement and every column at or over it. Its plants are the own record left out and the own record at 125, each refused by name (28 of 28 controls).
- **The load** is 0.711 at the pin and 0.673 with tsn-c-stack#32.
- **The survey** over every leg finds every measurement within its statement by the rule.

### Round 7's gates at `d539f162`

Round 7 changes no firmware and no image, so no sweep was run. Each check ran on a clean clone of the head.

| Gate | Result |
|---|---|
| The images | All eight are byte-identical, by ELF and loadable sha256, to `af2c4d7a`'s. |
| The lane gates of what changed (part r) | 45 as required, the four by design `_exits_1`, and the clone clean after. The comment scans (over the whole delta and over `af2c4d7a..d539f162`) and R844-1's audit find 0 lines. py idiom and docs_check pass. The harness self-test has 0 failures, and its PASS lines are round 6's plus the new control. load 28 of 28 and `--check` pass, the record classes 14 of 14, and the shape-cost, ledger, flip and rows gates. |
| The docs workflow's jobs | docs-gates-0, 1 and 2, wire-accountability, docs-check-no-git and docs-check: 61 steps run rc 0, 34 not run with a stated reason, 0 bad. |
| R843-3's mixed-point probe, through a gate | PASS at the head: the two 1x1/1if findings. It exits 1 on `af2c4d7a`'s module, and the new control escapes on `af2c4d7a`'s rule (13 of 14). |
| 8x8/1if's measurement legs, graded by the changed `record_classes.py` | PASS, identical to round 5's receipt |
| F1's figures | Each of the 36 figures section 13 states for 8x8/1if's gate, load and every-source rows equals its receipt, and 0.671 and 154,850 stand only as round 3's. The same check finds 37 of its 38 lines bad on `af2c4d7a`'s section 13. |

### The final pass at `af2c4d7a`

Round 6's final pass, at its head. Round 7 changes no firmware or image, so it carries.

Each job ran on its own clean clone of the head.

| Gate | Result |
|---|---|
| The lane gates (three parts) | 65 of 65 as required. Both source-comment scans and R844-1's audit find 0 lines, and each part's clone is clean after. |
| Every hosted job step of rtl-fast, rtl, elaborate and docs | 139 run, each rc 0. 226 are not run, each with its stated reason, and 0 are bad. |
| The firmware campaigns | 716 control, 302 AECP and 345 SRP mutants caught, 0 escaped. Boundary and firmware-verilator pass, and `aecp_wire.py --every` exits 0. |
| The four-shard sweep, each shard on its own picked CPU range | Each shard exits 0. 65 suites (15, 17, 17 and 16), 2,713,040 checks, 0 failures and 0 SKIPPED. |
| `counters-f5` | rc 0 at both shapes, the clone clean after |
| `plat_ledger.py --self-test` (item 6) | PASS at its four points, 7 of 7 controls. 8x8/1if is at 56 of 56 RAMB36 and its `ctrl_plat` at its entry. No image is past its entry. |
| The images | All eight are byte-identical to the measured ones, and the six fixed images to #902's `4ae887a1`'s. |

Two restarts, both recorded in the packet:
- **The first pass, at `f8ea6d72`, stopped.** Lane part a's comment scans found four new source-comment lines naming a review round. `af2c4d7a` fixes them, and the pass ran again from fresh clones.
- **Its first sweep exited 1 in every shard.** Verilator refused its root because the sweep's first PATH entry, another lane's shared tool directory, was absent while it ran. No other job reads that directory. The sweep ran again from a private copy whose three files are byte-identical.

### Earlier rounds

- **Round 4:** `egress_ledger.py` in the tree; the source-comment rule; THE SHAPES guard in `aecp.h`; each host arm's contract.
- **Round 3:** THE RETRY's round costs keyed on the shape, 165 and 25 us at 8x8/1if.
- **Round 2:** the MRPDU budget, the SRP record, the polls and the notices made the shape's own.
- **Round 1:** THE SHAPES, and 8x8/1if as the flip's other point.

## Authoritative references

- **#894's rulings:**
  - [round 6](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6892938049), on round 5's STOP;
  - [the held-egress ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6871343905), item (a);
  - [the shape ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867393730), item (b);
  - [the drain ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6886633874);
  - [round 12](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6883864236) and [round 13](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6888782796);
  - [the retry-cost ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6878014227);
  - [the egress ruling](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6867990126).
- **#665:** the owner's direction on block-RAM entries ([issuecomment-6892332745](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6892332745)).
- **#872:** [the second-hart trigger](https://github.com/kebag-logic/milan-fpga/issues/872#issuecomment-6862464924).
- **Documents:** FR_NFR.md 3.4.1, and SPLIT_CONTROL_MEMORY.md section 13.

## How to get into the same state

```sh
git fetch origin 894-8x8-1if
git switch --detach d539f162
git submodule update --init --recursive
```

## How to validate

```sh
python3 -I tb/verilator/ctrl_service_budget/egress_ledger.py --selftest
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest
python3 -I tb/verilator/ctrl_service_budget/record_classes.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <dir> --groups backlog-owed --record-budget-findings --record-share-findings
python3 -I tb/verilator/ctrl_service_budget/egress_ledger.py --point 8x8-1if <dir>/results
```

Expected result / pass criteria:

- **The ledger's self-test** passes, refusing 13 of 13 mutants.
- **The load gate** passes, with 28 of 28 controls refused; the load is 0.711 at 8x8/1if.
- **The record classes** refuse 14 of 14 planted controls, the mixed-point pass among them.
- **The `backlog-owed` leg** gives the seven rows above, each within its derived figure, and the ledger exits 0.

## Known limitations / out of scope

- **The rows by every source at 8x8/1if** are derived and reported, owed to #872 (round 6, item 1). R5, R6, the last queued notice, ACMP, ADP, MAAP, tx and txL are over their bounds there. R4, the first queued notice and R4L are within.
- **The `valid-destinations` arm** is #895's and is not in this tree.
- **`Mailbox.ARoundFillsWhatItsPassHasLeft` at 8x8/1if, and 1x1/1if's SRP record figure**, stay for new Issues.
- **#902's newer heads are not merged.** #902 has posted REVIEW READY at 26898c05, 41ca9f87 and 07ed787e since 4ae887a1; 894-tiers is at 07ed787e. Its five new commits change comments, docstrings and documents only (aecp_mbx.h's comments, rows_grade.py's docstring, section 13 and section 5, FR_NFR and the harness README), so no image can move. They are not merged here, as the sync was to 4ae887a1. A merge conflicts in FR_NFR.md and in aecp_mbx.h's comments, so the next sync resolves them.
- **Physical calibration is not run.** Local CPU simulation is not hardware proof.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (rounds 5 and 6, under the round-6 ruling)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (the final pass at the head)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
