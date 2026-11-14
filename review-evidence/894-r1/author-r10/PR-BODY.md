[A773]

## Contents

- **[Status](#status)**: round 10's head, the three MINOR findings at `5b264bf2` and both reports' residue answered, every image byte-identical, and `894-tiers` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: #894, #904 and #908, with the executor and reviewers.
- **[Description](#description)**: the round 10 assignment's items in its order, and the state the head carries from round 9.
- **[Findings](#findings)**: every finding of round 9's two reviews, with its resolution, file:line and verification.
- **[Authoritative references](#authoritative-references)**: the rulings and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the commands to check out the branch.
- **[How to validate](#how-to-validate)**: the reviewer's commands and their expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what this round leaves open.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

**REVIEW READY at 1x1/1if.** Head `7398ec0aeea468d92ff642a03a06e291a0cd58d1`: the delta from `5b264bf2` to `7398ec0a`, three commits. `894-tiers` -> `dev-soft-core` (still `cec88385`, #810 merged).

Round 10 answers the three MINOR findings at `5b264bf2` and the RESIDUE items of both reports (#894's assignment, issuecomment-6873298790). It changes no behaviour, and every image is byte-identical to `5b264bf2`'s.

- **R837-4-1: the map table's static assertion.**
  - The assertion now bounds the declared slot array by the range of index `place()` forms: `MAP_FIRSTS` x `MAP_CHANNELS` (`MAP_DOMAIN`). The 256-slot floor is a separate macro (`MAP_FLOOR`).
  - Round 9's assertion was true by definition, so it could never fire. It is removed.
  - A new AECP campaign row, `map-table-each-direction-alone`, plants an undersized table at 1x1/1if: 16 slots, where an input key's index reaches 56. The compiler must refuse it, with the assertion's words.
  - Against round 9's assertion the same plant compiles and the row escapes.
  - Two sentences in both documents now say what the assertion holds. Separately, they say the floor is a layout choice (#909).
- **R838-4-F1: the current rows.** `SPLIT_CONTROL_MEMORY.md`'s current table and summary now give the head's figures from `flip_grade.py --check`:
  - 1x1/1if: R4 12.85, R5 72.91, R6 68.80, first 14.51 and last 126.46 ms.
  - 8x8/2if: 42.09, 189.14, 177.28, 20.24 and 626.87 ms. This row of the same table had been that tool's output at `a07de012`.
  - Historical figures stay marked with their named state.
- **R838-4-F2: the validation command.** The core filter below is `'Core.*Map*:Core.Every*'`, which runs 13 tests. Round 9's `'Core.Map*:Core.Every*'` ran 8.
- **RESIDUE: R837-4-R1, R837-4-R2 and R838-4-R1,** each with its report's exact fix (Findings, below).
- **Every image is byte-identical to `5b264bf2`'s.** I hashed 332 files: 8 ELFs, their 8 binaries and 316 objects. A second build of `5b264bf2` reproduces them. A control with `MAP_FLOOR` planted at 264 changes 24 of them.
  - So round 9's measurements stand at this head: the record, the datapath events, the harness legs and the join intervals.
  - By the assignment's rule, the sweep is not run again.
- **No STOP trigger.** No image changes, and no behaviour change is needed.
- **The local pass at the head, on clean clones and never piped:**
  - every hosted job step of rtl-fast, rtl, elaborate and docs except the Verilator sweep: 139 run and 226 not run with a reason, 0 bad. The sweep's steps are among those not run, with their reason restated for this round;
  - the firmware suite and `fw_coverage.py --check`: PASS, coverage PASS over 39 files;
  - the AECP campaign: 274 of 274 caught, the build row among them;
  - the lane gates: 46 at 0. The 4 that exit 1 are the reported 8x8/2if and as-built checks, by design. They include the diff checks against twelve bases, `5b264bf2` among them; em-dash, 0 findings over 26 pages; the rows_tiers, flip and load self-tests, 971/971, 555/555 and 25/25; the harness self-test, 246 mutants caught and 0 escaped; `tier_grid.py`, 18 of 420; and the builder, NVM, boot, BDD and twin gates.

## Linked Issue / roles

Relates to #894
Relates to #904
Relates to #908

Executor: `[A773]`
Internal cleared-context reviewer: `[R837]`
External reviewer: `[R838]`

## Description

| Piece | What changed |
|---|---|
| `aecp_maps.c`, `aecp_map_mutants.py`, `aecp_mutants.py`, the AECP README, SPLIT_CONTROL_MEMORY section 13 (`55b8e621`) | **Item 1 (R837-4-1).**<br>- `MAP_DOMAIN` is `MAP_FIRSTS * MAP_CHANNELS`, the positions `place()` forms. `MAP_FLOOR` is `256u`. `MAP_SLOTS` is the larger of the two: the same expansion and type as before.<br>- After `struct edit`, `_Static_assert(sizeof ((struct edit *)0)->slot / sizeof ((struct edit *)0)->slot[0] >= (size_t)MAP_DOMAIN, "the table holds every position place() forms")`. Round 9's per-direction assertion is removed.<br>- `aecp_map_mutants.BUILD` marks a row that only its own file's compile refusal can catch, on its words (`aecp_mutants.refused`). Its first row is `map-table-each-direction-alone`.<br>- `controls()` leaves BUILD out of the claimed test set, and holds `refused()` to three reader controls: other words, another file's refusal, and a row that is not a build row.<br>- Any other compile failure is still an escape.<br>- Both documents say what the assertion holds, and, separately, that the floor is a layout choice (#909). |
| SPLIT_CONTROL_MEMORY section 13 (`947bd389`) | **Item 2 (R838-4-F1) and R837-4-R2.**<br>- The current table under "The rows by every source" names its tool and its head, and gives `flip_grade.py --check`'s figures at both points. The summary's R4 is 12.85 ms.<br>- Round 30's load table is named as the merge of `dev-soft-core` `0fb66211`'s, and its paragraph speaks of it in the past tense. Every figure is unchanged. |
| `aecp_arms.py` (`7398ec0a`) | **R837-4-R1:** the 16x4 geometry is described by what it is, with no review label. |

### The state at this head (round 9's measurements, the firmware unchanged)

- **The `aecp-largest-notice` group** (CPU cycles):

  | Table | 1x1/1if REMOVE of 63 | ADD | Refused edits | 8x8 | 8x8-1if |
  |---|---:|---:|---:|---:|---:|
  | round 8 (hash, 256 slots) | 92,766 | 86,504 | 23,014 to 79,384 | 142,634 | 151,629 |
  | direct index, the domain's 64 slots (`58e6b60f`) | 98,720 | 92,801 | 23,956 to 83,664 | 146,010 | 155,625 |
  | direct index, at least 256 slots (`5b264bf2`'s firmware, this head's) | 91,625 | 83,716 | 23,883 to 75,892 | 156,716 | 154,850 |

  The 64-slot table does less work and costs more. Its smaller frame moves the edit's arrays 192 B across the 8 KiB direct-mapped data cache. Restated, its 98,720 cycles would be 1,040 us, and the 1x1/1if load with every command the largest legal one would be 0.705, over 0.70. That load crosses 0.70 near 1,015 us.
- **The pace table at 1x1/1if** (txL against 49, R4L against 238):
  - P 6: 53.99 / 158.39;
  - P 7: 49.69 / 173.39;
  - **P 8: 48.09 / 188.39**;
  - P 9: 47.35 / 203.39;
  - P 10 and 11: 45.76 / 218.39 and 233.39;
  - P 12: R4L 248.39, over.
- **The datapath events** (`eventcost.py`, us):
  - 1x1/1if: AVB_INFO_CHANGED 30.55, AS_PATH_CHANGED 31.57, AMAP_LIVE_WRITE 25.51 (stated 35, 35, 30);
  - 8x8/2if: 35.76, 32.79, 22.65 (stated 40, 40, 25).
- **Every 1x1/1if row by every source** (`flip_grade.py --check --point 1x1/1if`, ms):
  - R4 12.85 (20), R4L 188.39 (238);
  - ACMP 28.44, ADP 26.83, MAAP 26.95 (30);
  - first queued notice 14.51 (20), R5 72.91 and R6 68.80 (90), last 126.46 (130);
  - tx 29.86, txL 48.09 (49).

  The loads are 0.513 at the pin and 0.509 with tsn-c-stack#32, and `tier_grid.py` holds 18 of 420 designs, choosing the built design.
- **The map work** (`Core.MapEditWorkIsLinearInItsMappings`, 63 mappings):
  - a REMOVE of one key's values: 127 visits, where 2 (n + R) = 128;
  - an accepted ADD: 63 (126);
  - a REMOVE of every row: 315 (378).
- **`Core.EveryAcceptedMapKeyIsItsOwn`:**
  - Each 63-mapping ADD is 63 visits plus each row read, and each REMOVE is within its bound.
  - At 16x32 there are 488 keys in 8 ADDs, and the first REMOVE is 1,165 visits against 2,078.
- **On THE SHARE at 1x1/1if:** in the `aecp-largest-notice` leg, the heaviest work pass of any edit, accepted or refused, is 149,490 of 200,000 cycles.
- **The join intervals and MRP run-outs** (round 9's full pass):
  - 57 intervals in 14 group runs (54 in the 13 unplanted runs), 185.485 to 190.040 ms, within 181.0 to 239.0;
  - 195 run-outs: 126 released and 69 empty, none late, absent or unresolved.

New checks and their planted defects, each caught by its own words:

| Check | Planted defect | Failing words |
|---|---|---|
| The table's declared slots hold every position `place()` forms (compile time, this round) | `map-table-each-direction-alone`: `MAP_SLOTS` the larger direction's own product, 16 at 1x1/1if | `static assertion failed: "the table holds every position place() forms"` |
| Every accepted key its own slot | `map-index-channel-dropped`; `map-index-stream-or-cluster-dropped` | "an ADD of every key the port accepts holds each as its own" |
| Every position of the domain one key's | `map-index-stride-short` | "an ADD of every key of the domain holds each as its own" |
| No key outside the domain forms an index | `map-domain-a-channel-wide` | "a key outside the domain is refused at its turn, before its port is read" |
| A row outside the domain holds no key | `map-outside-row-looked-up` | "a row outside the domain bars no mapping" |
| Work linear | `map-table-scanned`; `map-remove-values-rewalked` | "past twice their sum"; "not under n(n+1)/2" |

The AECP table has 274 plants: round 9's 273 plus the build row. Every test is claimed by one.

The compile-time row can fail:
- Round 9's assertion, planted back in place of the new one, lets the undersized table compile at every configuration. The row then runs no test and escapes, with exit 1.
- The assertion refuses an undersized table exactly where it would overflow. The probe compiles `aecp_maps.c` with the arms' flags at the five checked-in configurations, 16x4 and 16x32:
  - each direction's own product is refused at the three configurations where it is smaller than the domain;
  - the floor alone, or the array declared at the floor, is refused at 16x32 (544 positions);
  - the source as committed compiles at all seven.

## Findings

| Finding | Resolution | File:line | Verification |
|---|---|---|---|
| R837-4-1 MINOR (Conformance, RTL, Tests, Docs): the table's `_Static_assert` cannot fire and does not bound the range of index `place()` forms | The assertion holds the declared `slot` array's element count to `MAP_DOMAIN` = `MAP_FIRSTS` x `MAP_CHANNELS`. The floor is a separate macro. A campaign row plants an undersized table at 1x1/1if, and it is refused at compile time. The two document sentences say what the assertion holds, and, separately, that the floor is a layout choice (#909). | `aecp_maps.c:149-163`, `:190-191`; `aecp_map_mutants.py:17-19`, `:58-64`; `aecp_mutants.py:885-890`, `:898`, `:909-914`, `:948`; `SPLIT_CONTROL_MEMORY.md:2461`, `:2462`; AECP `README.md:213-221`, `:240-242` | The row is caught at the head, and escapes against round 9's assertion. The probe results are as above. `aecp_mutants.py --shard 257 274` runs the row alone: `[ok]`. Every image is byte-identical. |
| R838-4-F1 MINOR (Docs): the current rows retained superseded values | The current table and summary give `flip_grade.py --check`'s figures at the head, and name the tool. The table's 8x8/2if row, the same tool's output at `a07de012`, is updated too. The progression table and the historical sentences keep their named states. | `SPLIT_CONTROL_MEMORY.md:2342`, `:2346`, `:2347`, `:2481` | Each of the ten cells and the summary's R4 equals the flip check's output at `7398ec0a`. `docs_check.py` and `check_em_dash.py` report 0 findings. |
| R838-4-F2 MINOR (Tests, Docs): the thirteen-test claim had an eight-test command | The command is `'Core.*Map*:Core.Every*'`. | this body, How to validate | At the head, `--core --filter 'Core.*Map*:Core.Every*'` passes 13 tests and round 9's filter passes 8. |
| R837-4-R1 RESIDUE: a review named in a source comment | The report's exact wording. | `aecp_arms.py:17-19` | Read. No code, test or figure changes. |
| R837-4-R2 RESIDUE: "At this head" named a round-30 table | The report's exact fix, with the same paragraph's two other "at this head" read the same way. Every figure is unchanged. | `SPLIT_CONTROL_MEMORY.md:2314`, `:2322`, `:2330` | Read against `load_grade.py --check` at the head (0.792 / 0.752, 0.513 / 0.509, stated at `:2481`). |
| R838-4-R1 RESIDUE: "last REMOVE" for the first | "the first REMOVE is 1,165 visits against 2,078" | this body, The state at this head | Round 9's keys receipt: the first 16x32 REMOVE reads 976 rows. |
| R838-4-S10 (suggestion): the refused edits' 93,813 lacked attribution | The share bullet states only what the leg's receipt carries: the heaviest work pass, 149,490 of 200,000 cycles. | this body | Round 9's final-pass receipt: the heaviest work passes are 93,346, 95,503, 138,064 and 149,490. |
| R837-4 S5 / R838-4-S7 (suggestion): the packet index | Taken: this round's index is generated from the files present. | the packet's `INDEX.md` | Each row's sha256 against its file. |
| R837-4 S1 to S4, S6; R838-4-S1 to S6, S8, S9 (suggestions) | Not taken this round. They are optional, and none is in this round's assignment. | - | - |

## Authoritative references

- **#894's round 10 assignment** (issuecomment-6873298790).
- **#894's ruling of 2026-11-14** (issuecomment-6870437042), and the egress ruling of 2026-11-13 (issuecomment-6867990126), whose STOP triggers it keeps.
- **Earlier rulings:**
  - the ruling 6867393730;
  - the contingent ruling (issuecomment-6858269025) and its amendment (issuecomment-6862465874);
  - the pace ruling (issuecomment-6848507008);
  - the slice ruling (issuecomment-6845846512);
  - the ruling on the owner's questions (issuecomment-6844175391) and the owner's confirmation (issuecomment-6844947317);
  - the tiers' rows (issuecomment-6840564634).
- **The reviews:** R837-4 (PR #902 issuecomment-6873294087) and R838-4 (issuecomment-6873195590).
- **The requirements:** FR_NFR.md 3.4.1; NFR-SCOUT-01; #904's one decode and linear work.
- **The clauses:** IEEE 1722.1-2021 7.4.45, 7.4.46, 9.2.2.6 and 9.3.2.6; IEEE 802.1Q-2018 10.7.11; Milan v1.2 4.2.7.1.1 (Table 4.3), 5.4.2.27, 5.4.2.28 and 6.3.
- **#909:** the placement sensitivity behind the floor.

## How to get into the same state

```sh
git fetch origin 894-tiers
git switch --detach 7398ec0aeea468d92ff642a03a06e291a0cd58d1
git submodule update --init --recursive
```

## How to validate

```sh
python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 -B sw/firmware/gtest/fw_coverage.py --check
python3 -B sw/firmware/ctrl/test/aecp_mutants.py --output <dir> --shard 257 274
python3 -B sw/firmware/ctrl/test/aecp_arms.py --output <dir> --keys
python3 -B sw/firmware/ctrl/test/aecp_arms.py --output <dir> --work --filter 'Core.MapEditWork*:Core.Every*'
python3 -B sw/firmware/ctrl/test/aecp_arms.py --output <dir> --core --filter 'Core.*Map*:Core.Every*'
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B scripts/docs_check.py
python3 -B scripts/check_py_idiom.py
python3 -B scripts/check_cpp_idiom.py
git diff --check 5b264bf26416108add32d7fe5abca5252ffde2cb HEAD
```

Expected result / pass criteria:

- **The firmware self-test** passes, with every AECP plant caught: 274, the build row among them.
- **`fw_coverage.py --check`** exits 0.
- **`--shard 257 274`** runs `map-table-each-direction-alone` alone and prints `[ok]`. Its log is the compiler's refusal: `static assertion failed: "the table holds every position place() forms"`.
- **`--keys`** exits 0 at seven geometries, each `MAP KEYS` line within its 2 (n + R).
- **The work arm** prints `MAP WORK` lines, each at most 2 (n + R), with the collisions under n(n+1)/2.
- **The core filter** passes 13 tests, the definition test among them.
- **The harness self-test** passes, with every mutant caught. rows_tiers, flip and load refuse every control.
- **The 1x1/1if flip check prints RESULT: PASS**, with the rows above; SPLIT_CONTROL_MEMORY's current table gives the same figures.
- **`tier_grid.py`** chooses the built design at 900 us, with 18 of 420 holding.
- **The loads** are 0.513 and 0.509.
- **The checks that exit 1 by design** are those of the reported 8x8/2if point: `flip_grade.py --check`, `--point 8x8/2if`, `--design as-built` and `rows_tiers.py --terms`.

## Known limitations / out of scope

- **The table's floor is a layout choice made by measurement** (#909). Any later change to the edit's frame, or to the data around it, can move the record again, as the 64-slot table did. The record is measured in every full pass's `aecp-largest-notice` legs. The assertion bounds the table's size, not its timing.
- **The compile-time row runs at the campaign's configuration, 1x1/1if.** The probe receipt covers the other six geometries. The assertion itself compiles into every build.
- **The direct index's constants come from the entity generator.** When lane 894b merges #902, its THE SHAPES header is to become their single source (ruling 6871343905, (c)).
- **#908 stays open** until the last queued notice is within 125 ms and txL within 40 ms, with the join timer at 20 cs.
- **The bench capture of the join intervals on the wire** is S12b's (180.0 to 240.0 ms). This round had no bench access.
- **8x8/1if is lane 894b's** (the ruling 6867393730, item (b); the egress ruling, item 6).
- **8x8/2if's build of one** is #910's debt. 8x8/2if stays reported, not held.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (#894 at 1x1/1if: met under the rulings; 8x8/1if: lane 894b; #908: stays open by its own terms)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (the local pass at the head above: every hosted job step but the sweep, which the byte-identical images let this round skip, 139 run and 0 bad; the firmware suite and coverage; the AECP campaign, 274 of 274; every lane gate at its expected exit)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
