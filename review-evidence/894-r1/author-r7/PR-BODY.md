[A773]

## Contents

- **[Status](#status)**: round 7's head, 1x1/1if held under the contingent ruling, 8x8/1if a STOP, and `894-tiers` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: #894, #904 and #908, with the executor and reviewers.
- **[Description](#description)**: #908's levers, the contingent ruling's moves, the restated build cost, the join gate, and the earlier rounds' pieces.
- **[Authoritative references](#authoritative-references)**: the decisions, rulings and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the commands to check out the branch.
- **[How to validate](#how-to-validate)**: the reviewer's commands and their expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what this round leaves open.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

**REVIEW READY at 1x1/1if; 8x8/1if is a STOP.** Head `8a3791e44533d6b1cc26d486d0b18e7d83470dc1`: 20 commits on `ccb47e39`, the merge of dev-soft-core `cec88385` (#810 merged). `894-tiers` -> `dev-soft-core`.

- **1x1/1if holds every row by every source** (`flip_grade.py --check --point 1x1/1if`), under #908's cuts and #894's contingent ruling (issuecomment-6858269025) with its amendment (issuecomment-6862465874).
  - The join timer is armed at 19 cs, and the MRPDU bound is 240 ms less it: 50 ms.
  - THE PACE is 6 ms; the slice 900 us.
  - The last queued notice's bound is 130 ms, its row rounded up to the next 5 ms.
  - txL is 49.99 of 50 ms; the last queued notice 125.84 of 130.
  - The load is 0.513 (0.70), and every image is within its cap.
- **8x8/1if: STOP** on its per-point slice, which is not built. Its derived load (0.698, against 0.75) and its platform image hold.
- **#908 stays open:** the last queued notice is over 125 ms, and txL is over 40 ms at 20 cs.
- **The full local pass at the head:** every hosted job's steps run locally, 139 run and 0 bad, the sweep's four shards exit 0, every lane gate and harness leg at its expected exit.

## Linked Issue / roles

Relates to #894
Relates to #904
Relates to #908

Executor: `[A773]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

Round 7: #908's levers in the ruling's order, then the contingent ruling's moves, each its own commit.

| Piece | What changed |
|---|---|
| `poll_items.py`, `poll_grade.py`, `run.py`, `selftest_polls.py`, `selftest_mutants.py`, `load_grade.py`, `rows_grade.py` (item 4's allowance), `rows_tiers.py`, `flip_grade.py`, the harness README, SPLIT_CONTROL_MEMORY section 13 (`5dc3fb35`) | **ACMP's item, itemised (#908, lever a).**<br>- The poll that sends an owed frame also runs THE KEPT COMMAND's redelivery, so the item had been the whole poll: 12,259 CPU cycles at 1x1/1if, over its stated 12,000.<br>- The item is now the send less the offers nested in it. A declined offer is held to its own cost (20 us), and the kept record's accepted re-offer to the ACMP record's.<br>- **Occurrence bound:** at most 2 declines a send + 1. The proof is `acmp_mbx.c:111-128`, `:157-175` and `:186-187`. The harness holds the bound over each log, and the rows and the load charge it.<br>- **Measured:** the send at 50 and 65 us. |
| SPLIT_CONTROL_MEMORY section 13 (`fda4ef56`) | **The polls' base, attributed (lever b).**<br>- The two-cycle register read: 2 cycles.<br>- The hot list without `nvm_any`: 203.<br>- The rest, about 4,400, is data-cache stalls: KLJ3's 552 B store state falls on SRP's state's sets. |
| `ctrl_split.ld` and others (`77a2da0b`, reverted in `5013dbc1`); section 13 (`bbeb9299`) | **The cut, tried (lever c).** Three placements were tried, and none was taken: each one that recovers the base moves the conflict onto THE RETRY's rounds and AECP's item, whose costs the loop schedules by. |
| `ctrl_loop.h`, `srp_mbx.c`, `srp_mbx.cpp`, the model, FR_NFR 3.4.1 (`158265c2`) | **The join timer at 19 cs (contingent item 3).**<br>- `CTRL_LOOP_JOIN_CS 19u`.<br>- `CTRL_LOOP_TX_BOUND_MS (240u - 10u * CTRL_LOOP_JOIN_CS)`, 50 ms, derived and never typed.<br>- lwSRP is configured from it through `SRP_JOIN_CS`, so the donor is unchanged. |
| `join_grade.py`, `grade.py`, `run.py`, the self-test (`3d3afc17`, corrected in `0ab4e574`) | **The join interval gate (item 4).**<br>- Each group's shortest and longest print on a `JOINS` line. One outside 180.0 to 240.0 ms fails the run.<br>- An interval ends only at an MRPDU that a join timer's run-out released (`mrpdu_grade.released`), since lwSRP arms the timer at a commit alone.<br>- Six planted defects, the first definition among them. |
| `aecp_mbx.h`, FR_NFR 3.4.1 (`1560e4f4`) | **THE PACE at 6 ms:** the smallest P that holds txL within 50 ms with R4L within 240. |
| `ctrl_loop.h`, `rows_tiers.py`, `selftest_round.py`, the READMEs (`dec9f1d7`) | **The slice at 900 us at 1x1/1if:** the slice ruling's own rule, applicable once every row holds by every source. |
| `ctrl_loop.h`, `poll_grade.py`, `load_grade.py` (`7290f0f3`) | **A build of one MRPDU restated at 725 us at 1x1/1if.**<br>- The `srp` group's build after its Listener Ready makes its declarations in the first MRPDU's pass: 68,951 cycles. It was refused at the branch's start too.<br>- An owed MRPDU follows the build-of-one cost by its documented rule. |
| `aecp_mbx.h`, `queued_bound.py`, `rows_tiers.bounds_at`, `flip_grade.py`, `notice_window.py`, `selftest_notice.py`, FR_NFR 3.4.1 (`8cf7e2b7`) | **The last queued notice at 130 ms at 1x1/1if (the amendment).** Its row after the cuts is 125.84 ms. `queued_bound.py` derives the bound (decision D's 125 while the row holds it, else the row rounded up to the next 5 ms, never over 140), and the flip check refuses any other statement. |
| `srp_mbx.cpp`, `srp_walk.cpp`, `srp_latency.cpp` (`18e14164`) | The SRP tests derive the JoinTime from `CTRL_LOOP_JOIN_CS`, where they held the 200 ms default. |
| `twin_compare.py`, the milan_dp README (`f02457a6`) | Three twin plants' words restated at the split's join times under 19 cs. Each is refused by the same finding. |
| `srp_mbx.cpp`, `srp_rx_retry.cpp` (`5cbebb80`) | Two SRP tests timed from the armed JoinTime, so their planted defects fail them by their own words at 19 cs as at 20:<br>- the shared-bindings test filters on its unbind's own time;<br>- the oversized-record test offers its record two JoinTimes in, so its expiry falls on a build resumed across slices. |
| `ctrl_configs.py` (`8a3791e4`) | `queued_bound.py` named among the TSN stack boundary gate's scripts that read the firmware's headers and compile nothing. |
| SPLIT_CONTROL_MEMORY section 13, the READMEs, the model's docstrings (`64a19f03`, `cc758286`, `2953091e`, `11c586a8`) | The moves recorded, each row against both bounds; a function split for the long-function ratchet. |

New checks and their planted defects, each caught by its own words:

| Check | Planted defect |
|---|---|
| ACMP's item is its send; the redelivery's offers leave it and the base | `polls: an ACMP item carries the redelivery's offers (earlier rule)` |
| A decline is told by the kept record's re-offer after it | `polls: no offer is the kept record's re-offer, so none is told declined` |
| A declined offer is held to its own cost; the kept accepted re-offer to the record's | `polls: no declined ACMP offer is held to its cost`; `polls: no kept command's accepted offer is held to its cost`; `polls: a kept command's accepted offer held to the send's cost, not the record's` |
| At most 2 declines a send + 1 | `polls: the declined offers held to no bound`; `polls: the declined offers held to three a send`; the firmware plant `acmp-redelivered-every-poll` |
| The rows count 2 declines a send + 1 | the flip check's rule control, "ACMP's declined offers counted once a send" |
| A join interval is held to 180.0 to 240.0 ms | `joins: no join interval held to its range`; `joins: the range from the armed 190 ms` |
| Only a join timer's released MRPDU ends an interval | `joins: an MRPDU a join timer did not release taken for a join's`; `joins: any two MRPDUs, with no join timer between`; `joins: a periodic or LeaveAll timer's MRPDU taken for a join's` |
| Participants are told apart | `joins: the participants' applications not told apart` |
| The MRPDU bound is derived, not typed | `#define CTRL_LOOP_TX_BOUND_MS 90u`; flip `TX_BUDGET_MS != 50` |
| The last queued notice's bound is the amendment's | `queued_bound.controls`: the rule off its grid or ceiling, a statement 5 ms either side, a row past 140 ms |

Earlier rounds (#894, #904), unchanged this round:
- the map commands in one pass (#904);
- THE PACE, with R4L held to the 240 ms response time;
- the measured largest legal command's record and notice;
- the `8x8-1if` harness point;
- THE TRANSMIT's figure;
- THE TIERS, the channel rows and the owed-notice queue;
- the merges of #810's head and of dev-soft-core.

## Authoritative references

- **The round 7 ruling** (#894 issuecomment-6857835707); **the contingent ruling** (issuecomment-6858269025) and **its amendment** (issuecomment-6862465874); this round's STEP 0 (issuecomment-6857903645); #908's acceptance.
- **#894's earlier rulings:** issuecomment-6848507008 (round 6), issuecomment-6845846512 (the slice), issuecomment-6844175391 (option A and the fixture cap's fallback), issuecomment-6840564634 (the tiers' rows).
- **The requirements:** FR_NFR.md 3.4.1; NFR-SCOUT-01.
- **The clauses:**
  - IEEE 1722.1-2021 8.2.4, 8.2.5, 9.2.2.6 and 9.3.2.6;
  - IEEE 802.1Q-2018 10.7.4, 10.7.11 and Table 10-3;
  - Milan v1.2 4.2.7.1.1 (Table 4.3), 5.4.3.4, 5.4.5.2 and 5.5.2.3 (Table 5.26).

## How to get into the same state

```sh
git fetch origin 894-tiers
git switch --detach 8a3791e44533d6b1cc26d486d0b18e7d83470dc1
git submodule update --init --recursive
```

## How to validate

```sh
python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --groups srp --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --groups backlog-owed --record-budget-findings --record-share-findings
make -C tb/verilator/milan_dp twin twin-plants
python3 -B scripts/check_py_idiom.py
git diff --check ccb47e39a534f4c8d02af826fa50fcd6578a38de HEAD
```

Expected result / pass criteria:

- **The self-tests:** the harness's passes with every mutant caught, this round's thirteen included (seven polls, six joins). The model's controls are all refused: rows_tiers 969 of 969, flip 555 of 555, load 25 of 25.
- **The 1x1/1if flip check prints RESULT: PASS**, with txL 49.99 of 50 and the last queued notice 125.84 of 130.
  - `load_grade.py --check` gives 0.513 and 0.509.
  - `tier_grid.py` chooses the built design at 900 us.
- **The `srp` group at 1x1** exits 0. Its `JOINS` line reads 188.094 to 190.025 ms.
- **`backlog-owed` at 1x1** grades with no ACMP item, decline or kept re-offer over its cost.
- **The twin** reports 0 findings, and every plant is refused.
- **The checks that exit 1 by design** are the reported 8x8/2if: `flip_grade.py --check`, `--point 8x8/2if`, `--design as-built`, and `rows_tiers.py --terms`. The `srp` group at 8x8 and at 8x8-1if is also reported (below).

## Known limitations / out of scope

- **#908 stays open** until the last queued notice is within 125 ms and txL within 40 ms with the join timer at 20 cs, when the original bounds return.
- **The bench capture of the join intervals is owed** (the contingent ruling, item 4). This round had no bench access.
- **8x8/1if: STOP.** The per-point slice (1,070 to 1,300 us, build costs per shape) is not built.
  - `ctrl_loop.h` states the slice and the build costs by `MBX_N_IF` alone. Where the shape is stated is a decision.
  - Its derived rows by every source are #872's. Its harness legs are reported.
- **8x8/2if's build of one is refuted:** 147,613 cycles in the `srp` group, 1,550 us by the rule. It cannot be restated within the 1,300 us slice it must fit (`ctrl_loop.c`), so it is reported with 8x8/2if's rows. That is an owner decision.
- **8x8/2if** stays reported, not held.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (#894 at 1x1/1if: met under the contingent ruling; at 8x8/1if: not met, the slice; #908: levers a and b met, c tried, the Issue stays open by the ruling)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (every hosted job's steps run locally, 139 run and 0 bad, the sweep's four shards exit 0, every lane gate and harness leg at its expected exit)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
