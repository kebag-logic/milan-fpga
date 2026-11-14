[A781]

## Contents

- **[Status](#status)**: 8x8/1if measured on the tree that merges #902, its gate holds, and `894-8x8-1if` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: #894 and #872, with the executor and reviewers.
- **[Description](#description)**: what each round 2 item changed, the sync merges, the measurement, and what each new check plants.
- **[Authoritative references](#authoritative-references)**: the rulings and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the commands to check out the branch.
- **[How to validate](#how-to-validate)**: the reviewer's commands and their expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what is left for a decision, and what stays reported.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

**8x8/1if's gate holds on the tree that merges #902.** Head `184d47cacc0b4eccb923cfbd4f2df9c3a05f5638`, `894-8x8-1if` -> `dev-soft-core`, which #902 (`894-tiers`, its head `7398ec0a` merged here) still has to reach.

- **The measurement** ran once at 8x8/1if, on the built image at its 1,475 us slice: every group of arm A, the `answering-every-port` arm and the `answering-ports` arm's `aecp-largest-notice`. That is 112 groups and 1,680 instances.
  - Every row the CPU decides is within its bound.
  - The only budget misses are the seven held-egress rows, each smaller than its recorded figure.
  - The joins are 186.687 to 190.705 ms, within 181.0 to 239.0.
  - The load is 0.709 of 0.75.
  - The platform image is 56.0 RAMB36.
- **No STOP trigger fired, and the second-hart trigger is not met.** No slice is stated over 1,600 us, and every 1x1 and 8x8/2if image is byte-identical to #902's.
- **One finding is left for a decision.** THE RETRY's cold cost at 8x8/1if is stated below its measurement. No row and no slice is affected; see [Known limitations](#known-limitations--out-of-scope).
- **The full pass at the head is clean.** The sweep ran 65 suites and 2,713,040 checks with 0 failures. Every hosted job step verifies: 139 run, 226 not run with a reason, 0 bad. The firmware campaigns caught 716, 275 and 345 plants, with 0 escaped. The lane gates are 49 at 0, with 4 exiting 1 by design.

## Linked Issue / roles

Relates to #894
Relates to #872

Executor: `[A781]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

**The round 2 ruling** (#894 issuecomment-6871343905) asks for the items below, with #902's bounds and round 9's direct-index map table taken in by merge.

| Item | Change |
|---|---|
| (i) The MRPDU row's harness budget | `mrpdu_grade.BUDGET_MS` is `CTRL_LOOP_TX_BOUND_MS` as `ctrl_loop.h` derives it, 49 ms with `T_egress`. It is read once, by the same reader as #902's run-out resolution (`LATE_MS`), and never typed. The row carries the wait W that brings its family's 20 ms to it. Before, T_svc's 20 ms held it. |
| (ii) An SRP record's cost per shape | `CTRL_LOOP_SRP_UNIT_US` is stated in each block of THE SHAPES (`ctrl_loop.h`): 250 us at 1x1/1if, 365 us at two interfaces, and 345 us at 8x8/1if. That is its heaviest record, 32,421 cycles, plus 5 %. At 345 us SRP's longest slice is 146,052 cycles, within 147,500; at 250 us slices overran it, up to 156,198. |
| (iii) The polls per shape | `poll_grade.STATED_US` is keyed on the shape. 8x8/1if's base and items are its own measurement plus 5 %: the base 235 us, the rebuild 590, the withdrawal 110, the walk 50, ACMP's item 75 and a declined offer 30, a notice 140 and a long one 320. The load at 8x8/1if takes them: 0.709 at the pin and 0.670 with tsn-c-stack#32. |
| (iv) The notices a reset leaves pending | Each pending notice is kept in its descriptor's event, so none is dropped. `AECP_NOTICES_MOST` is derived from the descriptors the shape header states: 12 at 1x1/1if and 40 at 8x8/1if. At two interfaces it stays 40. A build whose descriptors hold more fails its static assertion. The queued-notice arm builds and is measured at 8x8/1if. |

**The sync merges.**
- **`219ea7ed`** merges #902's `5b264bf2`, with five conflicts resolved:
  - `mrpdu_grade.py`: one reader of THE TRANSMIT's bound;
  - `ctrl_configs.py`: both sides' boundary entries;
  - FR_NFR 3.4.1's SRP/MRP row: #902's figures with this branch's sentence on the harness budget;
  - the AECP and SRP READMEs.
- **`184d47ca`** merges `7398ec0a`, which `894-tiers` moved to during the round, with no conflict. Its `aecp_maps.c` change holds the map table's slots to every position `place()` forms, adds a build-row plant, and changes no image.

**The shape header is the single source of round 9's direct-index table** (`6122db33`, ruling item (c)).
- `srp_entity.py` writes the map edits' key domain into the shape header that every image unit is compiled with: `AECP_ENTITY_KEY_STREAMS`, `_STREAM_CHANNELS`, `_CLUSTERS` and `_CLUSTER_CHANNELS`. They come from `aecp_shape.key_domain` over the builder's own AEM image.
- `aecp_entity_gen.h` states the domain only under `#ifndef CTRL_SRP_ENTITY_H`, for the host arms that compose no SRP, with the same derivation.
- No image byte moved.

**The measurement at 8x8/1if** (the head `6122db33`; both 8x8/1if images at the final head are byte-identical to it):

| Row (bound, ms) | Worst measured, ms |
|---|---:|
| AECP (20) | 4.693 |
| ACMP, ADP, MAAP (30) | 6.813, 5.522, 6.020 |
| SRP (90) | 10.284 |
| MRPDU (49) | 3.578 |
| The first queued notice (20) | 2.259 |
| The last queued notice (130), of 40 queued | 23.730 |
| The largest legal command, the paced R4L row (238) | 2.442 |

- **The held-egress rows.** `backlog-owed`'s seven rows (61.680 to 63.969 ms) are the only budget misses. They are set by the scenario's 60 ms egress hold and recorded in section 13's ledger in 1x1/1if's form, each under its earlier figure.
- **The aged build's control.** `transmit-aged` holds an owed MRPDU 300 passes. At 8x8/1if it puts all eight groups' timer-driven MRPDU over the derived 49 ms.

**New checks and their planted defects.** Each is caught in its own words.

| Check | Planted defect |
|---|---|
| THE TRANSMIT's row at its derived bound: a row at the bound is within, one 1 ms over it is a miss (harness self-test) | the budget one over `CTRL_LOOP_TX_BOUND_MS`; the row held to T_svc's 20 ms (the earlier rule) |
| A pass's polls at 8x8/1if at its shape's costs, and the load reading them in both columns | the polls held at the interface count's; the load's polls at 8x8/2if's (each the earlier rule) |
| The table of shapes (`shape_costs.py --selftest`, 21 controls) | an SRP record over its slice; a listed shape whose polls are not stated; `AECP_NOTICES_MOST` at the 1x1's 12 at one interface; an AVB interface's notices counted as two; two interfaces' count under the 8x8's; the default not the shipping configuration's; a load point counting other descriptors than the shape header states |
| The key domain's single source (`shape_costs.key_findings`) | the shape header not stating it; `aecp_entity_gen.h` stating it beside the shape header; the two differing |
| An image's map table sized from the shape header | the shape header's key streams widened to 64, which changes all eight images |
| Every notice the descriptors hold kept and sent once (host suite, at the shipping configuration and at the 8x8 configuration at one interface) | the AECP campaign's `notice-dropped-with-its-descriptors-next` |
| A shape whose descriptors hold more notices than the count fails the build (`aecp_mbx.c`) | the earlier `(MBX_N_IF == 1u ? 12u : 40u)` at the 8x8 shape |

## Authoritative references

- **The ruling:** #894 issuecomment-6871343905 (round 2: items (a), (b)(i) to (v), (c)), on the STOP issuecomment-6871307898.
- **#902's bounds:** #894 issuecomment-6867990126 (MRPDU 49 ms, paced R4L 238 ms, the harness join gate 181.0 to 239.0 ms).
- **Round 9's direct-index map table:** #894 issuecomment-6870437042.
- **Earlier:** #894 issuecomment-6867393730 (THE SHAPES, the 8x8/1if gate).
- **The two-core trigger:** #872 issuecomment-6862464924, as the round 2 ruling restates it.
- **The requirements:** FR_NFR.md 3.4.1.
- **The clauses:** IEEE 802.1Q-2018 10.7.4 and 10.7.11; Milan v1.2 4.2.7.1.1 (Table 4.3), 5.4.2.27, 5.4.2.28 and 5.4.5.2; IEEE 1722.1-2021 7.4.45, 7.4.46, 7.5.2, 9.3.2.6 and Table 7-1.

## How to get into the same state

```sh
git fetch origin 894-8x8-1if
git switch --detach 184d47cacc0b4eccb923cfbd4f2df9c3a05f5638
git submodule update --init --recursive
```

## How to validate

```sh
python3 -I tb/verilator/ctrl_service_budget/shape_costs.py --check --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <dir> --record-budget-findings --record-share-findings --jobs 8
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <dir2> --variant answering-every-port --record-budget-findings --record-share-findings --jobs 8
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <dir3> --variant answering-ports --groups aecp-largest-notice --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <dir4> --variant answering-later --mutation transmit-aged --record-budget-findings --record-share-findings --jobs 8
```

Expected result / pass criteria:

- **The table of shapes** prints the four shapes with their SRP record column, and PASS, 21 of 21 controls refused.
- **The flip check** passes at 8x8/1if (load 0.709 of 0.75) and at 1x1/1if. `load_grade.py --check` holds 1x1/1if at 0.513 and 0.509.
- **The harness self-test** passes with every mutant caught.
- **Arm A at 8x8-1if** exits 0. Its only budget misses are `backlog-owed`'s seven held-egress rows, and its joins are within 181.0 to 239.0 ms.
- **The `answering-every-port` arm** shows every queued notice within 130 ms and each group's first within 20 ms. It exits 1 only on THE RETRY's round lines, below.
- **`aecp-largest-notice`** exits 0.
- **The `transmit-aged` control** is caught in all 8 groups.

## Known limitations / out of scope

- **Left for a decision: THE RETRY's cold cost at 8x8/1if.**
  - **Where it shows.** The `answering-every-port` arm, now measured at 8x8/1if, holds 1,654 of THE RETRY's rounds over their stated cost. Every one is a round with no notice beside 1, 2 or 4 refused attempts: up to 12,547, 19,326 and 23,343 cycles, against 11,900, 15,300 and 22,100.
  - **Why.** `AECP_ROUND_COLD_US` (`aecp_mbx.h`) and `AECP_ATTEMPT_US` (`aecp.h`) are keyed on `MBX_N_IF`, so 8x8/1if takes the 1x1's 85 us cold cost. Its rounds measure about 125 us. At the 8x8 shape's two-interface 185 us, every round is within.
  - **What it does not affect.** No round with a notice is over, no row misses, and no slice runs past its length: THE RETRY's longest round is 109,745 cycles of 147,500.
  - **Why it is not fixed here.** Keying the cold cost on the shape, as the ruling keys an SRP record's, changes the 8x8/1if image and its rounds, so it needs a ruling and a new measurement.
- **1x1/1if's SRP record** measured 26,086 cycles in round 1, over its 250 us unit. Its slices hold (76,072 cycles against 90,000) and its image is held byte-identical, so its unit is left for a decision.
- **Reported, not held, owed to #872:** 8x8/1if's rows by every source. They are derived with its own polls, the 40 notices and its largest command, with the records' and events' costs taken from 8x8/2if: R4 18.56, R5 113.87, R6 108.72, the first queued notice 16.99, the last 266.70, R4L 192.83, ACMP 45.48, ADP 44.77, MAAP 46.18, tx 58.53 and txL 146.97 ms. Also reported:
  - the load with every AECP command the largest legal one, 0.991;
  - two passes of `aecp-largest-notice` over THE SHARE (213,816 cycles).
- **`rows_grade.py`** is unchanged beyond round 1's keying. Its points are 1x1/1if and 8x8/2if.
- **#902 is still open:** #894 issuecomment-6876349104 asks #902's lane to check 1x1/1if's AECP record before it merges. Anything that changes reaches this branch when `dev-soft-core` is merged in.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the round 2 ruling's items (i) to (v); one finding left for a decision)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (the full pass at the head, once: see the REVIEW READY comment)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
