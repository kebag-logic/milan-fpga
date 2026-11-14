[A773]

## Contents

- **[Status](#status)**: round 8's head, 1x1/1if held under the egress ruling, and `894-tiers` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: #894, #904 and #908, with the executor and reviewers.
- **[Description](#description)**: the egress ruling's items in its order, each its own commit, and the findings they answer.
- **[Findings](#findings)**: every finding of round 7's two reviews, with its resolution, file:line and verification.
- **[Authoritative references](#authoritative-references)**: the rulings and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the commands to check out the branch.
- **[How to validate](#how-to-validate)**: the reviewer's commands and their expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what this round leaves open.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

**REVIEW READY at 1x1/1if.** Head `dd01b0afef87037ec485cd49b40a26b542854bdd`: 11 commits on round 7's `8a3791e4`. `894-tiers` -> `dev-soft-core` (still `cec88385`, #810 merged).

- **1x1/1if holds every row by every source** (`flip_grade.py --check --point 1x1/1if`) under #894's egress ruling of 2026-11-13 (issuecomment-6867990126):
  - THE TRANSMIT's MRPDU bound is 240 - 10 x JOIN_CS - T_egress = 49 ms, and paced R4L's 240 - T_ingress - T_egress = 238 ms, both derived from `ctrl_loop.h`'s stated allowances.
  - THE PACE counts edits as the whole-millisecond gate allows, ceil((w + 1) / P).
  - ADD and REMOVE_AUDIO_MAPPINGS do bounded, linear work for refused edits too; the largest legal command's record is re-measured with the maximum-length collision and conflict cases and restated at 975 us.
  - THE PACE is 7 ms, the smallest that holds: txL 47.98 of 49 ms, R4L 173.37 of 238.
  - The last queued notice 125.84 of 130; the load 0.513 at the pin and 0.509 with tsn-c-stack#32 (0.70); every image within its cap.
- **The join grader has no horizon:** every MRP timer's run-out is released, empty, late, absent or unresolved, and late or absent fails the run. The harness gate is 181.0 to 239.0 ms commit to commit.
- **No STOP trigger:** 7 ms holds (none was needed up to 11); the last queued notice is within 140 ms; no image is over its cap; the map commands' behaviour is unchanged; the collision case's pass is 96,142 of THE SHARE's 200,000 cycles at 1x1/1if.
- **The full local pass at the head, each part on its own clean clone and never piped:** the sweep's four shards exit 0 (65 suites, 2,713,040 checks, 0 failures); every hosted job's steps of rtl-fast, rtl, elaborate and docs run locally, 139 run and 226 not run with a reason, one of the 139 UNKNOWN on its first run (`test_soc_timing_cuts` past its 900 s wall clock under the pass's load, exit 92, "not a failure") and passing when run again alone at the same 900 s; every lane gate and harness leg at its expected exit.

## Linked Issue / roles

Relates to #894
Relates to #904
Relates to #908

Executor: `[A773]`
Internal cleared-context reviewer: `[R837]`
External reviewer: `[R838]`

## Description

Round 8 follows the egress ruling item by item, item 2 first as it directs.

| Piece | What changed |
|---|---|
| `paced_rows.py`, `rows_tiers.py`, `flip_grade.py`, `aecp_mbx.h` (`8ba93f26`) | **Item 2: the pace count.**<br>- `paced_rows.edits(w, P)` is ceil((w + 1) / P). The gate compares whole ms (`aecp_mbx.c:154-158`), the edit stamped with the fresh read `aecp_rx` makes as it takes the record (`aecp.c:31-37`, `aecp_maps.c`), and the gate's clock is never ahead of it, so floor(t[k+1]) >= floor(t[k]) + P.<br>- `gate_most` simulates the gate by its own arithmetic; `count_findings` holds `edits` to it at every window from 0.01 to 120 ms and every P to 13, in the flip check.<br>- The earlier rule, 1 + floor(w / P), is planted: it is named, and it shortens txL at some P. |
| `ctrl_loop.h`, `tier1_rows.py`, `rows_tiers.py`, `paced_rows.py`, `join_grade.py`, `flip_grade.py`, `selftest_polls.py`, `ctrl_configs.py`, FR_NFR 3.4.1 (`96565297`) | **Item 1: T_egress counted.**<br>- `CTRL_LOOP_T_INGRESS_MS 1u` and `CTRL_LOOP_T_EGRESS_MS 1u` (FR_NFR 3.4.1's table).<br>- `CTRL_LOOP_TX_BOUND_MS (240u - 10u * CTRL_LOOP_JOIN_CS - CTRL_LOOP_T_EGRESS_MS)`, 49 ms; only a static assert reads it, so no image moves.<br>- `paced_rows.PACED_BOUNDS` is 240 less both, 238 ms; `join_grade.LEAST_MS`, `MOST_MS` are 180 + T_egress and 240 - T_egress.<br>- FR_NFR 3.4.1: the R4L and MRPDU paragraphs and lines 424-426 state the split's figures and cite the ruling. |
| `aecp_maps.c`, `test_aecp.cpp`, `aecp_arms.py`, `aecp_mutants.py`, `aecp_map_mutants.py`, the AECP README (`6c232270`) | **Item 3: bounded map work.**<br>- A mapping its port's geometry refuses ends the table (`legal`, which reads nothing), as an ADD's earlier conflict does: its own turn refuses the edit before its port is read, so status, reads and precedence are unchanged.<br>- One slot a key; a REMOVE's other values of a key are linked from the key's first, so no lookup walks one key's values. The hash, the stream or cluster plus nine times the channel, gives every legal key its own slot at every configuration.<br>- `Core.MapEditsAreTheirDefinitionRowForRow` is unchanged and passes. New: `Core.MapKeysThatShareASlotAreTheirOwn`, and a work arm (`AECP_MAP_WORK`, test-only) whose `Core.MapEditWorkIsLinearInItsMappings` holds six cases at 8, 16, 32 and 63 mappings to 2 (n + R) and the collisions under n(n+1)/2. |
| `long_notice.py` (`44f897ab`) | **Item 3: the collision and conflict cases join `aecp-largest-notice`**, each 550 B and refused BAD_ARGUMENTS: a REMOVE of one key from distinct indices, a REMOVE of the key's legal values in turn, an ADD whose last mapping conflicts. |
| `mrpdu_grade.py`, `join_grade.py`, `run.py`, `selftest_polls.py`, `selftest_mutants.py`, `ctrl_configs.py` (`b6b94d92`) | **Item 4: the join grader.**<br>- `mrpdu_grade.resolve` seeks a run-out's builds wherever they come: the first after it and each next one with at most one ordinary or idle pass between, a build's frames including what it left owed.<br>- Outcomes: released; empty; late (first frame, or first build, past the derived 49 ms); absent (no build, the log running on past it); unresolved (the log ends first). Late and absent fail the run and are named; unresolved is counted. |
| `aecp_mbx.h`, `rows_tiers.py` (`197012aa`) | **Item 3's restatement and the pace.** `LONG_RECORD_US['1x1/1if']` 940 -> 975 us (92,766 cycles, the accepted REMOVE of 63); `AECP_PACE_MS 7u`. |
| `long_notice.py` (`f2f92fdc`) | Docstrings for three nested helpers, as the Python idiom gate requires. |
| FR_NFR 3.4.1, MAILBOX_SPLIT, SPLIT_CONTROL_MEMORY section 13, the READMEs, `ctrl_loop.h`, `ctrl_memory.py`, the model's docstrings (`2763cc06`, `dd01b0af`) | **Item 5: docs and residue** (below). |

### Measured

- **The `aecp-largest-notice` group at 1x1/1if** (CPU cycles): the REMOVE of 63 copies 92,766 and the ADD 86,504; the refused collision by indices 23,014, by values 78,262, the conflict at the last turn 79,281. Their passes: 150,004, 140,498, 41,545, 96,142 and 97,172, each within THE SHARE.
- **On the 8x8 shape** (answering-ports): the longest record 142,634 cycles, 1,500 us by the rule, so the stated 1,555 us is kept. At 8x8-1if 151,629 cycles, 1,595 us, reported.
- **The map work** (`Core.MapEditWorkIsLinearInItsMappings`, 63 mappings): a REMOVE of one key's values 127 visits (bound 128), of one key from distinct streams 3. The start head's table, its walk counted the same way, visits 2,080 in both (n(n+1)/2 = 2,016).
- **The pace table at 1x1/1if** (txL against 49, R4L against 238): P 6 53.86 / 158.37; P 7 47.98 / 173.37; P 8 47.98 / 188.37; P 9 47.24 / 203.37; P 10 45.65 / 218.37; P 11 45.65 / 233.37. Under item 2's count alone at the start head's inputs (bounds 50 and 240): P 6 49.99, P 7 47.73, P 8 47.73, P 9 47.03, P 10 44.96, P 11 44.96, R4L 158.34 to 233.34.
- **At this head** (the full pass's legs): 57 join intervals in 14 group runs, 185.468 to 190.059 ms, 54 of them in the 13 unplanted runs; 195 MRP timers' run-outs, 126 released and 69 empty, none late, absent or unresolved.
- **Re-graded with the new grader:** round 7's 14 published legs give 57 join intervals, 185.645 to 190.025 ms (52 by the earlier grader; the 5 more are frames it dropped where a run-out's first build sent nothing), none late, absent or unresolved; the latest first frame is 1.55 ms after its run-out. Its timer-to-MRPDU rows: 1.292 ms at 1x1 and 2.245 and 3.440 ms at 8x8 (3.085 before), each within 20 ms. Of those intervals, 3 are the planted control C-R1's, so the unplanted legs give 54 in 13 runs.

New checks and their planted defects, each caught by its own words:

| Check | Planted defect | Failing words |
|---|---|---|
| The pace count is the gate's (`paced_rows.count_findings`) | the earlier rule, 1 + floor(w / P) | "THE PACE's edits in a window of 0.01 ms at 1 ms counted 1, not the 2 the gate takes" (`count_controls`) |
| The MRPDU bound counts T_egress | `CTRL_LOOP_TX_BOUND_MS (240u - 10u * CTRL_LOOP_JOIN_CS)`; `90u` | "CTRL_LOOP_TX_BOUND_MS states 50 ms, not the timer budget's 49" |
| The join gate is 181.0 to 239.0 | `joins: the wire's 180.0 to 240.0 ms held at the commit, T_egress uncounted` | "a join interval is two MRPDUs of one participant ... 181 and 239 ms ... hold" |
| Map work linear | `map-remove-values-rewalked` (38, 138, 530, 2,018 visits); `map-hash-the-stream-alone` | "not under n(n+1)/2"; "past twice their sum" |
| Legal keys that share a slot are their own | `map-table-key-unchecked` (re-anchored) | "an ADD of two keys that share a slot adds both" |
| An illegal mapping ends the table at its own turn | `map-illegal-ends-early`; `map-illegal-unflagged` | "status for command" |
| A run-out's build is sought with no horizon | `joins: a run-out's builds sought within 100 ms of it (earlier rule)` | "a run-out's build past THE TRANSMIT's bound is late and named ... 241, 289, 291 and 500 ms fail" |
| Late fails, absent is not unresolved, unresolved is not empty | `joins: a late build taken for an on-time one`; `... late build's run-out not failing the run`; `... absent build taken for an unresolved one`; `... unresolved build taken for one that owes nothing` | the same check, and "no build after a run-out is absent and named ..." |
| An owed frame is its build's | `joins: a frame its build left owed not the build's` | "a frame its build left owed, which the poll sends a pass later, is that build's" |

Re-anchored, same names and words: `map-value-cluster-channel-ignored`, `map-add-stops-early`, `map-checked-before-its-read`, `map-remove-every-copy`.

## Findings

| Finding | Resolution | File:line | Verification |
|---|---|---|---|
| R837-2-1 MAJOR: the 50 ms MRPDU bound leaves no room for T_egress | Ruled (item 1): the bound is 240 - 10 x JOIN_CS - T_egress, 49 ms; paced R4L 238 ms; the harness gate 181.0 to 239.0 ms; each derived | `ctrl_loop.h:342-343`, `:360`; `tier1_rows.py:213-241`; `rows_tiers.py:114`; `paced_rows.py:43`; `join_grade.py:27-33`; `FR_NFR.md:373`, `:381`, `:424-426` | flip check at 1x1/1if PASS against 49 and 238; `grep -n "leave 19 ms" docs/reference/FR_NFR.md` finds nothing; the planted egress-free derivation is refused |
| R837-2-2 MINOR: the pace count | ceil((w + 1) / P), proven from the gate and held to its simulation | `paced_rows.py:54-84`, `:176-193`; `aecp_mbx.h:38-52`; `FR_NFR.md:383` | the table above; the probe's two columns now agree for every P; `rows_tiers.py --selftest` 971 of 971 |
| R837-2-3 MINOR: stale figures; the 30 ms citations | each line states the tree's value; the citations name the ruling | `FR_NFR.md:374`, `:415`; `MAILBOX_SPLIT.md:390`; `ctrl_loop.h:206-209`; `SPLIT_CONTROL_MEMORY.md:361`, `:2355`, "What is left" | a grep of each line; `docs_check.py` and `check_em_dash.py` 0 findings |
| R837-2-4 RESIDUE: issue-comment IDs in source | rulings by name and date | `aecp_mbx.h`, `ctrl_loop.h`, `ctrl_memory.py:260-261`, `flip_grade.py`, `join_grade.py`, `load_grade.py:235`, `notice_window.py:61`, `queued_bound.py:3-4`, `rows_tiers.py`, `run.py`, `selftest_notice.py:88`, `selftest_polls.py`, `tier1_rows.py` | `git diff cec88385..HEAD -U0 -- . ':!*.md' \| grep '^+.*issuecomment-'` is empty |
| R837-2-5 RESIDUE: the interval count; the pre-restatement receipt | counted with and without the planted control (above); round 7's `receipts/model/rows-1x1-final.txt` is the rows at `2953091e`, before the build-of-one restatement, and its final rows are `receipts/gates/lane-flip_check_1x1.txt` | this body; the REVIEW READY comment | the receipts named |
| R838-2-F1 MAJOR: late join intervals disappear past the 100 ms horizon | Item 4: no horizon; late, absent and unresolved told apart; late and absent fail | `mrpdu_grade.py:1-122`; `join_grade.py:66-84`; `run.py` (`stated_misses`, `print_joins`); `selftest_polls.py:305-345`; `selftest_mutants.py:851-871` | R838-2's probe: 291 and 500 ms now counted, over and late; the six new plants caught; round 7's logs re-graded |
| R838-2-F2 MAJOR: a quadratic collision path in the map rewrite | Item 3: bounded linear work, refused or not; behaviour unchanged; collision and conflict cases measured; the record restated | `aecp_maps.c:84-112`, `:132-230`, `:348-398`; `test_aecp.cpp:2589`, `:2621`; `aecp_arms.py:12`, `:57`; `aecp_map_mutants.py:79-87`; `long_notice.py:45-95`; `rows_tiers.py:132` | the counts above; 21 map plants caught; the definition test unchanged and passing; the flip check at the 975 us record |
| R838-2-F3 MINOR: numeric contracts disagree | as R837-2-3, and the AECP README's last queued notice | `FR_NFR.md:415`; `aecp/README.md:120`; `MAILBOX_SPLIT.md:390` | compared with `CTRL_LOOP_JOIN_CS`, `CTRL_LOOP_TX_BOUND_MS`, `AECP_QUEUED_MS`, `CTRL_LOOP_SLICE_US` and the model |
| R838-2-R1 RESIDUE: review rounds and IDs in source | as R837-2-4, and "on round 5" gone from `paced_rows.py` | as above | the grep above, and `grep -n "round [0-9]" ` of the added lines |
| R838-2-R2 RESIDUE: round 7's handoff pointer | round 7's packet is not rewritten; the correct receipt is named here | this body | `receipts/gates/lane-flip_check_1x1.txt` names `8a3791e4`, last 125.84 and txL 49.99 |
| R837-2 S1, S3; R838-2 S1 to S5 (suggestions) | not taken this round | | |
| R837-2 S2: the packet index | this round's index is generated from the files present | the packet's `INDEX.md` | each row's sha256 against the file |

## Authoritative references

- **#894's egress ruling of 2026-11-13** (issuecomment-6867990126), this round's; **its ruling on round 7's REVIEW READY** (issuecomment-6867393730).
- **Earlier:** the contingent ruling (issuecomment-6858269025) and its amendment (issuecomment-6862465874); issuecomment-6857835707; the pace ruling (issuecomment-6848507008); the slice ruling (issuecomment-6845846512); the ruling on the owner's questions (issuecomment-6844175391) and the owner's confirmation (issuecomment-6844947317); the tiers' rows (issuecomment-6840564634).
- **The reviews:** R837-2 (PR #902 issuecomment-6867959154) and R838-2 (issuecomment-6867751113).
- **The requirements:** FR_NFR.md 3.4.1 (its numeric deadlines' table: `T_ingress`, `T_egress`); NFR-SCOUT-01.
- **The clauses:** IEEE 1722.1-2021 7.4.45, 7.4.46, 9.2.2.6 and 9.3.2.6; IEEE 802.1Q-2018 10.7.4, 10.7.11 and Tables 10-5 to 10-7; Milan v1.2 4.2.7.1.1 (Table 4.3), 5.4.2.27, 5.4.2.28, 5.4.3.4 and 5.5.2.3 (Table 5.26).

## How to get into the same state

```sh
git fetch origin 894-tiers
git switch --detach dd01b0afef87037ec485cd49b40a26b542854bdd
git submodule update --init --recursive
```

## How to validate

```sh
python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 -B sw/firmware/ctrl/test/aecp_arms.py --output <dir> --work --filter 'Core.MapEditWork*'
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --groups aecp-largest-notice --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --groups srp --record-budget-findings --record-share-findings
make -C tb/verilator/milan_dp twin twin-plants
python3 -B scripts/check_py_idiom.py
git diff --check 8a3791e44533d6b1cc26d486d0b18e7d83470dc1 HEAD
```

Expected result / pass criteria:

- **The self-tests:** the firmware suite and its campaigns pass with every plant caught, the map table's 21 among them; the harness's passes with 246 mutants caught; the model's controls are all refused: rows_tiers 971 of 971, flip 555 of 555, load 25 of 25.
- **The work arm** prints `MAP WORK` lines, each at most 2 (n + R), and the collisions under n(n+1)/2.
- **The 1x1/1if flip check prints RESULT: PASS**, with txL 47.98 of 49, R4L 173.37 of 238 and the last queued notice 125.84 of 130; `load_grade.py --check` gives 0.513 and 0.509.
- **`aecp-largest-notice` at 1x1** exits 0, its refused edits answered BAD_ARGUMENTS and no pass over THE SHARE. **`srp` at 1x1** exits 0; its `JOINS` line reads 188.006 to 190.059 ms against 181.0 to 239.0, 8 run-outs released and 5 empty.
- **The twin** reports 0 findings, and every plant is refused.
- **The checks that exit 1 by design** are the reported 8x8/2if (`flip_grade.py --check`, `--point 8x8/2if`, `--design as-built`, `rows_tiers.py --terms`) and the 8x8-1if harness legs.

## Known limitations / out of scope

- **#908 stays open** until the last queued notice is within 125 ms and txL within 40 ms with the join timer at 20 cs.
- **The bench capture of the join intervals on the wire** is S12b's (180.0 to 240.0 ms); this round had no bench access.
- **8x8/1if is lane 894b's** (the ruling 6867393730, item (b)), which takes the 49 and 238 ms bounds after #902 merges (the egress ruling, item 6).
- **8x8/2if's build of one** is #910's debt; 8x8/2if stays reported, not held.
- **The map table's one-slot-a-key bound** holds where no two legal keys share a hash, which every configuration meets; a port with more than nine streams or clusters of more than 28 channels would need a wider table.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (#894 at 1x1/1if: met under the egress ruling; 8x8/1if: lane 894b; #908: stays open by its own terms)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (the full pass above: the sweep 65 suites and 0 failures; 139 hosted steps run, the one UNKNOWN passing when run again alone; the firmware campaigns, AECP 269 of 269; every lane gate and harness leg at its expected exit)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
