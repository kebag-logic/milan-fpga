[A781]

## Contents

- **[Status](#status)**: THE RETRY's round costs are keyed on the shape, 8x8/1if is measured again on its new image, its gate holds, and `894-8x8-1if` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: #894 and #872, with the executor and reviewers.
- **[Description](#description)**: what round 3 changed and why, the measurement, each new check and its planted defects, and what rounds 1 and 2 changed.
- **[Authoritative references](#authoritative-references)**: the rulings and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the commands to check out the branch.
- **[How to validate](#how-to-validate)**: the reviewer's commands and their expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: the open question, what stays reported, and a finding for a new Issue.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

**8x8/1if's gate holds on its new image, and no cost there is over its statement.** Head `716a8ae7979a31315a6e085959dc4dcc8b7ee022`, `894-8x8-1if` -> `dev-soft-core`, which #902 (`894-tiers`, its head `7398ec0a` merged here) still has to reach.

- **The finding round 2 left for a decision is fixed.** THE RETRY's cold start and refused attempt are stated for each shape, and 8x8/1if states its own: 165 and 25 us, its measurement plus 5 %.
- **The measurement** ran once at 8x8/1if on the new image, with round 2's groups and criteria: every group of arm A, the `answering-every-port` arm and the `answering-ports` arm's `aecp-largest-notice`. That is 112 groups and 1,680 instances.
  - Every row the CPU decides is within its bound.
  - THE RETRY's 2,455,411 rounds are all within their statement. Every leg exits 0, and no leg prints a STATED line.
  - The only budget misses are the seven held-egress rows, each the same as round 2's and under its recorded figure.
  - The joins are 186.687 to 190.705 ms, within 181.0 to 239.0.
  - The load is 0.711 of 0.75.
  - The platform image is 56.0 RAMB36.
- **No STOP trigger fired, and the second-hart trigger is not met.** No slice is stated over 1,600 us. Every 1x1 and 8x8/2if image is byte-identical to round 2's head `184d47ca`, whose six equal #902's `7398ec0a`.
- **The full pass at the head is clean.** The sweep ran 65 suites and 2,713,040 checks with 0 failures. Every hosted job step verifies: 139 run, 226 not run with a reason, 0 bad. The firmware campaigns caught 716, 275 and 345 plants, with 0 escaped. The lane gates are 51 at 0, with 4 exiting 1 by design.
  - A first pass, at `bae44edf`, found one step refused: the wire comparison's standalone build of the core. That is fixed in `716a8ae7`, and the pass ran again in full there.
- **`894-tiers` moved to `9606b3a9` after the measurement.** #902 is still open and in review. The move is not merged here; see [Known limitations](#known-limitations--out-of-scope).

## Linked Issue / roles

Relates to #894
Relates to #872

Executor: `[A781]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

### Round 3: THE RETRY's round costs by shape

**The ruling** (#894 issuecomment-6878014227) keys `AECP_ROUND_COLD_US` and `AECP_ATTEMPT_US` on the shape, through the shape header that `CTRL_LOOP_SHAPE` already reads. They are stated at 8x8/1if at the measurement plus 5 %, and every 1x1 and 8x8/2if image stays byte-identical.

**What was wrong.** Round 2's measurement held 1,654 of THE RETRY's rounds in the `answering-every-port` arm over their stated cost. Each was a round with no notice beside 1, 2 or 4 refused attempts: up to 12,547, 19,326 and 23,343 cycles, against 11,900, 15,300 and 22,100.
- The cold start was keyed on `MBX_N_IF`, so 8x8/1if took the 1x1's 85 us.
- **A correction to round 2's report:** the attempt cost was never keyed on `MBX_N_IF`. It was a single 34 us at every shape, in the AECP core.

| Piece | Change |
|---|---|
| THE SHAPES (`ctrl_loop.h`) | Each listed shape now states `CTRL_LOOP_RETRY_COLD_US` and `CTRL_LOOP_RETRY_ATTEMPT_US`. (1, 2, 2) states 85 and 34 us; (1, 9, 9) states 165 and 25 us; both two-interface shapes state 185 and 34 us. A shape not listed fails the build, as before. |
| `aecp_mbx.h`, `aecp.h` | `AECP_ROUND_COLD_US` is now `CTRL_LOOP_RETRY_COLD_US`, where it was `(MBX_N_IF == 1u ? 85u : 185u)`. `AECP_ATTEMPT_US` is now `CTRL_LOOP_RETRY_ATTEMPT_US`, where it was `34u`. The adapter's admission (`aecp_mbx.c`) and the core's charge (`aecp.c`) are unchanged text. |
| `aecp.c` | It now includes `ctrl_loop.h`. The core charges a refused attempt as a compile-time immediate, and a shape's interface count is the mailbox contract's. It calls nothing that header declares. See [the open question](#known-limitations--out-of-scope). |
| `aecp_arms.py`, `aecp_wire.py` | The builds of the core that have no shape header compile at the shipping shape: the host core arms (`-I loop -I mbx` after any mailbox group's paths) and the wire comparison (`716a8ae7`, after the first full pass found it refused). The 8x8/1if mailbox arm also runs THE RETRY's two attempt tests. |
| `round_grade.py`, `grade.py` | A round is held at the shape of its build. Each cost is evaluated from `aecp_mbx.h` and `aecp.h` through THE SHAPES, with no regex on the interface ternary. |
| `shape_costs.py` | The table carries the two costs. `retry_findings` holds each AECP name to the table's at every point, and three controls plant the fallback. |
| `selftest_round.py`, `selftest_mutants.py` | An independent reader of the shape's block, a check at 8x8/1if, and two mutants. |
| The docs | FR_NFR 3.4.1, section 13, the AECP README and the harness README. |

**The derivation (the measurement plus 5 %).** It uses round 2's rounds at 8x8/1if, whose image is byte-identical to `184d47ca`'s, taking the dearest round at each count of refused attempts, with notices charged at `AECP_NOTICE_US`:
- 2,206 cycles with no refused attempt;
- 12,547 with one;
- 19,326 with two;
- 23,343 with four, every port.

The rule is #665's definition of the attempt: what a round of `AECP_ROUND_PORTS` refusals costs past its cold start, per refusal. The cold start is what any round implies at that attempt cost. Many lines hold every round and charge a round of every port refused exactly its measured cost; of those, the rule takes the one with the least cold start. That is the last edge of the upper hull, through the rounds of two and four refused attempts:
- 15,309 cycles once and 2,008.5 per refused attempt (153.09 and 20.09 us);
- plus 5 %, rounded up to 5 us: **165 and 25 us**.

Every round is within the line. The other arms' rounds were all within the earlier 85 + 34 k us, which lies under the line for every k up to the four ports. The roughly 125 us round 2 reported was the cold start implied at a 34 us attempt; measuring the attempt as well gives this line.

**The images.** Byte-identity is checked by sha256 of each ELF and of its loadable bytes.
- With 8x8/1if's values left at 85 and 34, all eight images are identical to `184d47ca`'s. Restructuring alone moves no byte.
- At 165 and 25, the six fixed images stay identical.
- Exactly two instructions move in each 8x8/1if image: `scan`'s `addi -34` becomes `-25`, and `retry`'s `addi -85` becomes `-165`.
- The platform image stays 56.0 RAMB36, with the same ROM and SRAM.

**The measurement at 8x8/1if** was run once on the new image (`d8629751`, both 8x8/1if images of which are byte-identical at the head). Where round 2's figure differs, it is in brackets.

| Row (bound, ms) | Worst measured, ms |
|---|---:|
| AECP (20) | 4.693 |
| ACMP, ADP, MAAP (30) | 6.813, 5.897 (5.522), 6.020 |
| SRP (90) | 10.284 |
| MRPDU (49) | 3.578 |
| The first queued notice (20) | 2.259 |
| The last queued notice (130), of 40 | 26.195 (23.730) |
| The largest legal command, the paced R4L row (238) | 2.442 |

- **THE RETRY's rounds.** 2,455,411 rounds, each within 165 + 255 n + 25 k us. The closest is 89.9 % of its statement. The same dearest rounds give the same line, 165 and 25 us. With the dearer cold start, a round admits fewer notices, so the last queued notice moves from 23.730 to 26.195 ms.
- **Every other stated cost** is within its measurement: the heaviest SRP record is again 32,421 cycles against 345 us, and every poll is within. Nothing is restated.
- **Budget misses.** The only ones are `backlog-owed`'s seven held-egress rows, 61.680 to 63.969 ms, the same as round 2's. They stay recorded misses, and none is new.
- **Joins and run-outs.** 346 joins, 186.687 to 190.705 ms. Of 2,311 run-outs, none was late, absent or unresolved.
- **Slices.** SRP's longest is 146,052 cycles, the build's 137,924 and THE RETRY's round 89,462 (109,745), all within 147,500.
- **The load.** 0.711 at the pin and 0.671 with tsn-c-stack#32, within 0.75. Round 2 had 0.709 and 0.670 at the 85 us cold start.
- **The aged build's control.** `transmit-aged` is caught: 8 of 8 groups' timer-driven MRPDU are over 49 ms, at 66.505 to 67.015 ms.

**New checks and their planted defects.** Each defect is caught, in words that name the point.

| Check | Planted defect | Failing words |
|---|---|---|
| `shape_costs.retry_findings` (in `--check`, `--selftest` and the harness self-test's table checks) | the cold start keyed on the interface count again | "8x8/1if: AECP_ROUND_COLD_US is 85 us at its shape (1, 9, 9), not the 165 us THE SHAPES state for it" |
| the same | a refused attempt at a single figure for every shape again | "8x8/1if: AECP_ATTEMPT_US is 34 us at its shape (1, 9, 9), not the 25 us THE SHAPES state for it" |
| the table's rules | 8x8/1if's block stating the cold start as the interface ternary | "ctrl_loop.h states '#define CTRL_LOOP_RETRY_COLD_US (MBX_N_IF == 1u ? 85u : 185u)' for the shape (1, 9, 9) (8x8/1if)" |
| The harness self-test: a round at 8x8/1if is held to its shape's costs, apart from the interface count's | the round's costs read at the interface count | that check fails |
| the same | the round held at its point's interface count instead of the image's shape | that check fails |

### Earlier rounds

**Round 2** (#894 issuecomment-6871343905), with #902's bounds and round 9's direct-index table merged in from `894-tiers`:

| Item | Change |
|---|---|
| (i) The MRPDU row's harness budget | `mrpdu_grade.BUDGET_MS` is `CTRL_LOOP_TX_BOUND_MS` as `ctrl_loop.h` derives it: 49 ms with `T_egress`, read once and never typed. A planted defect sets it one over the bound. |
| (ii) An SRP record's cost per shape | `CTRL_LOOP_SRP_UNIT_US` is stated in each shape's block: 250 us at 1x1/1if, 365 us at two interfaces and 345 us at 8x8/1if, its heaviest record plus 5 %. |
| (iii) The polls per shape | `poll_grade.STATED_US` is keyed on the shape, with 8x8/1if's polls at its measurement plus 5 %. The load is recomputed. |
| (iv) The notices a reset leaves | `AECP_NOTICES_MOST` is derived from the descriptors the shape header states: 12 at 1x1/1if and 40 at 8x8/1if. None is dropped, and a plant proves it. A build whose descriptors hold more fails its static assertion. |
| (c) The single source | The shape header states the direct-index table's key domain. `aecp_entity_gen.h` states it only for a compile that has no shape header. |
| The sync merges | `219ea7ed` merges #902's `5b264bf2`, with five conflicts resolved. `184d47ca` merges `7398ec0a`, with no conflict. |

**Round 1** (#894 issuecomment-6867393730, item (b)) made 8x8/1if the flip's other point. It added THE SHAPES table, the 8x8/1if slice of 1,475 us (one MRPDU's build there plus 5 %, within the ruling's 1,600 us), and its builds.

## Authoritative references

- **The ruling:** #894 issuecomment-6878014227 (round 3), with issuecomment-6871343905, item (b)(ii): a stated cost below its measurement is the defect.
- **#902's bounds:** #894 issuecomment-6867990126: MRPDU 49 ms, paced R4L 238 ms, and the harness join gate 181.0 to 239.0 ms.
- **Earlier:** #894 issuecomment-6871343905 (round 2), issuecomment-6870437042 (round 9's direct-index table) and issuecomment-6867393730 (THE SHAPES and the 8x8/1if gate).
- **#665:** the attempt cost's definition (`aecp.h`), and the decision of 2026-11-13 on the 8x8/2if cold start (issuecomment-6842347916), which is unchanged.
- **The two-core trigger:** #872 issuecomment-6862464924, as the round 2 ruling restates it.
- **The requirements:** FR_NFR.md 3.4.1.
- **The clauses:** IEEE 802.1Q-2018 10.7.4 and 10.7.11; Milan v1.2 4.2.7.1.1 (Table 4.3), 5.4.2.27, 5.4.2.28 and 5.4.5.2; IEEE 1722.1-2021 7.4.45, 7.4.46, 7.5.2, 9.3.2.6 and Table 7-1.

## How to get into the same state

```sh
git fetch origin 894-8x8-1if
git switch --detach 716a8ae7979a31315a6e085959dc4dcc8b7ee022
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

- **The table of shapes** prints the four shapes with THE RETRY's two columns ((1, 9, 9): 165 and 25 us) and PASS, with 24 of 24 controls refused.
- **The flip check** passes at 8x8/1if (load 0.711 of 0.75) and at 1x1/1if. `load_grade.py --check` holds 1x1/1if at 0.513 and 0.509.
- **The harness self-test** passes with 0 failures: 879 checks, and 259 mutants caught.
- **Arm A at 8x8-1if** exits 0. Its only budget misses are `backlog-owed`'s seven held-egress rows, and its joins are within 181.0 to 239.0 ms.
- **The `answering-every-port` arm** exits 0 with no STATED line. Every queued notice is within 130 ms, and each group's first within 20 ms.
- **`aecp-largest-notice`** exits 0.
- **The `transmit-aged` control** is caught in all 8 groups.
- **The firmware-unit job** (`aecp_arms.all_arms`) runs the 8x8/1if mailbox arm's notice and attempt tests, and they pass.

## Known limitations / out of scope

- **An open question: the AECP core now reads `ctrl_loop.h`.**
  - **Why.** The core charges a refused attempt as an immediate, so keying it on the shape needs the shape at compile time. The shape includes the interface count, which only the mailbox contract states, and `ctrl_loop.h` includes `mbx.h`.
  - **What it does not do.** The core calls nothing either header declares, and the disassembly shows no other change. The AECP README now says this: no mailbox dependency at run time, and one header at compile time.
  - **The alternative.** An attempt cost set at run time by the adapter, as `notice_us` is, would move every image (a load in place of an immediate, and a field in `struct aecp`), which the ruling forbids.
- **`AECP_NOTICE_US` stays keyed on the interface count** (255 us at one interface). The ruling keys the other two. Every round with a notice at 8x8/1if is within it.
- **A finding for a new Issue: `Mailbox.ARoundFillsWhatItsPassHasLeft` fails at the 8x8 shape at one interface,** at `184d47ca` itself. Its last step expects a queue served to its end within `AECP_NOTICES_MOST` rounds of a share each (`test_aecp.cpp:3121`, `adapter.yields` 3 where it expects 0). The arm never ran it there, and this change does not alter it, so it is left out of the 8x8/1if selection.
- **1x1/1if's SRP record** measured 26,086 cycles in round 1, over its 250 us. Its slices hold, and its image is held byte-identical, so it stays left for a decision.
- **Reported, not held, owed to #872:** 8x8/1if's rows by every source. They are derived with its own polls, its round costs, 40 notices and its largest command, with the records' and events' costs taken from 8x8/2if. The figures are R4 18.64, R5 113.95, R6 108.80, the first queued notice 17.07, the last 274.91, R4L 192.91, ACMP 45.56, ADP 44.85, MAAP 46.26, tx 58.61 and txL 147.06 ms. Also reported:
  - the load with every AECP command the largest legal one, 0.993;
  - two passes of `aecp-largest-notice` over THE SHARE (213,816 cycles).
- **`rows_grade.py`** is unchanged in round 3. It already reads THE SHAPES' names at a point's shape, so `AECP_ROUND_COLD_US` resolves to the shape's own value there. Its points are 1x1/1if and 8x8/2if.
- **Left for a decision: `894-tiers` at `9606b3a9`.** #902 is still open.
  - **When it moved.** `894-tiers` was at `7398ec0a`, which is merged here, at every check through the measurement and the docs (the last at 20:1x CET). After that it moved ten commits to `9606b3a9`, #902's round 11 head, which its round 12 delta reviews have found NEGATIVE.
  - **What it changes.** `aecp_maps.c`'s code (new fields and logic in `struct edit`), so every image moves, 8x8/1if's included.
  - **Why it is not merged here.** Merging it needs #902's new head as the byte-identity base, and a second 8x8/1if measurement and full pass. This round allows one of each, and its sync item applies before the measurement.
  - **How it gets here.** It reaches this branch through the planned merge of `dev-soft-core` after #902 merges, unless a ruling asks for it earlier.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (the round 3 ruling's items 1 to 3; one open question above)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (the full pass at the head: see the REVIEW READY comment)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
