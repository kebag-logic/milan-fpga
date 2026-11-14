[A773]

## Contents

- **[Status](#status)**: round 11's head, the one-row map edit's record cut and the edits charged as a class of their own, and `894-tiers` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: #894, #904 and #908, with the executor and reviewers.
- **[Description](#description)**: round 11's items in the assignment's order.
- **[Findings](#findings)**: every finding of the measurement that opened round 11, and the one this round found, each with its resolution, file:line and verification.
- **[Authoritative references](#authoritative-references)**: the rulings and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the commands to check out the branch.
- **[How to validate](#how-to-validate)**: the reviewer's commands and their expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what this round leaves open, the answering-ports arm's SET_CONFIGURATION first.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

**REVIEW READY at 1x1/1if.** Head `9606b3a915de284c71d3063c2e8d94b097f18241`: ten commits on `7398ec0a`. `894-tiers` -> `dev-soft-core`.

The measurement that opened round 11 (#894 issuecomment-6878200592) found the AECP record over `record.aecp`'s 235 us at 1x1/1if: `aecp-fanout`'s one-row REMOVE_AUDIO_MAPPINGS at 27,851 CPU cycles (295 us by the rule) and its ADD at 22,932 (245). No final pass had run that group since round 4. Round 11 (issuecomment-6878230332, amended by issuecomment-6878532871):

- **Cuts the record.** The REMOVE is 22,728 cycles (240 us by the rule) and the ADD 20,595 (within 235). The direct index, the 2 (n + R) work bound and every refusal with its precedence stand.
- **Charges the edits as a class of their own,** because the cut leaves the REMOVE 348 cycles over 22,380. A row's window holds at most ceil((w + 1) / P) paced edits; they are charged 260 us at 1x1/1if (the one-row output edit, 24,360 cycles) and 325 us at 8x8/2if. Every other AECP record is charged 235 and 265 us. No firmware change is needed for this and no bound moves.
- **Restates three costs** from the final pass's full arm A:
  - a TICK at 1x1/1if at 50 us. One TICK measured 4,617 cycles at `7398ec0a`, and 4,612 under the cut, each time AECP's sink sending an owed frame inside it;
  - ACMP's owed frame at 55 us (4,890 cycles). The cut's layout moved it from 4,723;
  - THE TRANSMIT's stated figure, `CTRL_LOOP_TX_MS`, at 34 ms, over the tx row's 33.01;
  - at 8x8/2if, from that point's legs, a pass's events' fixed part at 35 us and ACMP's owed frame at 70.
- **Ends the gap** with a check: a final pass's AECP records are held by class, and a pass that did not run every group of arm A at 1x1/1if is refused.

Every CPU-decided row at 1x1/1if holds by every source:

| Row | Value | Bound |
|---|---:|---:|
| R4 | 12.93 | 20 |
| R4L (paced) | 188.41 | 238 |
| ACMP | 28.64 | 30 |
| ADP | 27.01 | 30 |
| MAAP | 27.13 | 30 |
| First queued notice | 14.56 | 20 |
| R5 | 73.39 | 90 |
| R6 | 69.24 | 90 |
| Last queued notice | 127.22 | 130 |
| tx | 33.01 | 49 |
| txL | 48.23 | 49 |

- **The load:** 0.515 at the pin and 0.511 in the second column, against 0.70.
- **The join intervals:** 188.002 to 190.022 ms in every group of arm A, and 186.492 to 190.044 ms over every leg, within 181.0 to 239.0 ms.
- **The pace:** 8 ms, still the smallest that holds txL and R4L.

**One finding is left to the owner** ([below](#known-limitations--out-of-scope)). In the answering-ports arm, `aecp-fanout`'s SET_CONFIGURATION is 33,724 cycles at 1x1/1if (355 us by the rule) and 78,332 on the 8x8 shape. That arm is labelled and is never the formal measurement. Arm A's fixture refuses SET_CONFIGURATION, so arm A never measured it. The cost predates this lane: it is 33,533 cycles at round 4's head.

## Linked Issue / roles

Relates to #894
Relates to #904
Relates to #908

Executor: `[A773]`
Internal cleared-context reviewer: `[R837]`
External reviewer: `[R838]`

## Description

### 1. Attribution

Each record was traced commit by commit (sim_main.cpp's `BUDGET_TRACE_AFTER` and `BUDGET_TRACE_PCS`) on the bisect's builds of `9d7167bd`, `1b70cedd` and `7398ec0a`. The traced runs reproduce every span exactly. Each line is read from a `-g` build whose `aecp_map_command` is byte-identical to the measured one.

| Commit | REMOVE, cycles | Commits | Short stalls | Fetch stalls | Data stalls | Refills |
|---|---:|---:|---:|---:|---:|---:|
| `9d7167bd`, before #904's check | 17,932 | 2,699 | 7,311 | 6,338 | 1,584 | 114 |
| `1b70cedd`, #904's one-pass check | 25,356 | 4,342 | 10,488 | 7,852 | 2,674 | 126 |
| `7398ec0a`, the head | 27,851 | 4,321 | 10,397 | 10,349 | 2,784 | 143 |
| `bc971054`, the cut | 22,728 | 2,863 | 8,200 | 10,245 | 1,420 | 148 |

- **What `1b70cedd` added: 1,643 commits.**
  - `look`'s copy of each row (`union held x = {*r}`) and the REMOVE pass's copy of each kept row were each a call of `memcpy` of 8 B, about 120 cycles: `forward` went from 208 to 1,030 commits.
  - The edit cleared 960 B of `struct edit` whatever its size: `memset` went from 48 to 371 commits.
  - `mark`'s own commits went from 20 to 443.
- **What came after: 2,495 cycles at the same commit count.** These are lines that were cached before and are cold at the later layouts, for example the change notice's `changed`, 1 refill at `9d7167bd` against 8 to 9 since.
- **The caches:** a 16 KiB two-way fetch L1 and an 8 KiB direct-mapped data L1, both with 64 B lines. About 580k cycles of other work run between two of the group's commands, so most of a command's path is cold.
- **By pass at the head,** inside `aecp_map_command` (17,068 of the 27,851): the clear 2,616, the table 2,388, the FOUND marks 2,899, the REMOVE pass 2,813, the change notice 2,560 and the checks before the edit 3,355.
- **The assignment's "8cc3e5d3's 17,932"** is `9d7167bd`'s figure. `8cc3e5d3`'s image (`12180198`) is 19,008.

### 2. The cut (`bc971054`)

`sw/firmware/ctrl/aecp/aecp_maps.c`:

- `:244` `assign`: a mapping is copied a coordinate at a time. `:259` a row's words are composed in registers, guarded by the little-endian `#error` at `:179`, which states the order `place` already assumed. No edit calls `memcpy` except for its response's rows.
- `:434` and `:447`: the edit clears only the slots `place` forms (`MAP_DOMAIN`, 64 B at 1x1/1if), and each mapping's link, marks and occurrences at its turn in the table. No read reaches past either.
- `:278`-`:309` `mark`: the FOUND pass holds the reach of its port's map (`:192`, `:301`), from the first row equal to a held mapping to one past the last. The REMOVE pass looks up only the rows inside the reach. Rows before it stay in place and rows after it move down unread (`:304`). A row kept in its place is not copied.
- `:364`: the descriptor and GET_AUDIO_MAP's page are echoed a byte at a time.
- `:204` `stale`, under `AECP_MAP_WORK` only (no image contains it): the work arm starts each edit from the table an earlier edit left.

What the cut measures, in the harness group `aecp-fanout` (input map) and `aecp-largest-notice`. Each variant was built and run on a fresh clone. µs is cycles / 100; "rule" adds 5 % and rounds up to 5 µs.

| Variant | REMOVE | ADD | Largest legal | `.text` |
|---|---:|---:|---:|---:|
| `7398ec0a` | 27,851 | 22,932 | 91,625 | 97,956 |
| `memcpy` calls removed | 25,611 | 22,338 | 88,953 | 97,940 |
| and the clear narrowed | 23,941 | 21,483 | 87,497 | |
| and the row's words in registers, the per-mapping clears at the turn | 23,793 | 21,214 | 87,685 | 97,928 |
| and the echo inline, kept rows not self-copied | 23,210 | 20,931 | 87,500 | 97,952 |
| and the REMOVE's reach (`bc971054`) | **22,728** | **20,595** | **86,978** | 98,176 |
| and the response's rows written by the table (not taken) | 23,105 | 20,603 | 86,895 | 98,288 |

- **The REMOVE:** 240 us by the rule, 348 cycles over the 22,380 that 235 allows.
- **The ADD:** within.
- **The largest legal command at 1x1/1if:** 915 us by the rule, within the 975 kept.
- **On the 8x8 shape:** 145,770 cycles (1,535 us), within the 1,650 kept. Its work passes over THE SHARE are 2 of 138, the longest 244,041 cycles; round 9 had 2 of 139, the longest 254,919.
- **The layout effect:** the last variant shows it. That variant writes the response rows from the table and is 112 B longer, and it raised every other record of the group by 300 to 400 cycles.
- **The committed image:** `bc971054`'s ELF is byte-identical to the measured variant's.

**The plants** (`sw/firmware/ctrl/test/aecp_map_mutants.py:109`-`:160`): twelve new rows. Each was run alone with `aecp_mutants.py --shard`, and each is caught by name. The 30 existing rows planted in `aecp_maps.c` were re-run and all are still caught.

| Row | Plant | Test | Failing words |
|---|---|---|---|
| `map-remove-reach-a-row-late` | `from = k + 1` | `Core.MapEditsAreTheirDefinitionRowForRow` | the edit's map is its definition's, row for row |
| `map-remove-reach-a-row-short` | `to = k` | the same | the same |
| `map-remove-rows-past-the-reach-dropped` | the move after the reach removed | the same | the same |
| `map-remove-kept-row-unmoved` | `kept++ == k` | the same | the same |
| `map-row-words-cluster-channel-dropped` | a row's second word its cluster alone | the same | status for command |
| `map-copy-cluster-channel-dropped` | `assign` drops the cluster channel | the same | the edit's map is its definition's, row for row |
| `map-slots-cleared-a-slot-short` | `MAP_DOMAIN - 1` | `Core.MapEditWorkReadsOnlyWhatItCleared` | an ADD beside a row at the domain's last position is accepted |
| `map-marks-uncleared` | the marks not cleared | the same | the same |
| `map-occurrences-uncleared` | the occurrences not cleared | the same | a REMOVE of one of two equal rows removes one |
| `map-links-uncleared` | the links not cleared | the same | visits past twice their sum |
| `map-echo-page-dropped` | `k < 4` | `Core.MapCommandsEchoTheirDescriptorAndPage` | a map command's response echoes its descriptor and page |
| `map-echo-index-short` | `k < 3` for an edit | the same | the same |

**The new tests** (`sw/firmware/ctrl/test/test_aecp.cpp`):

- **`:2809` `Core.MapEditWorkReadsOnlyWhatItCleared`** (work arm):
  - The channels are widened to the domain's.
  - An ADD beside a row at the domain's last position is accepted.
  - A REMOVE of one of two equal rows removes one.
  - Each edit stays within 2 (n + R).
- **`:2333` `Core.MapCommandsEchoTheirDescriptorAndPage`:** GET_AUDIO_MAP, ADD and REMOVE to STREAM_PORT_OUTPUT 0x0203 echo its type, its index and the page. No test checked that echo before: the page-echo plant escapes every other Core test.

The definition test passes unchanged. The KEYS arm passes at all 7 geometries with the work arm's stale table: every key a port accepts, at every geometry the builder accepts, reads only what the edit cleared.

### 3. The edits as a class of their own (`895f8906`, `dd788ed5`)

Amendment step 2 applies, since the cut does not hold 235.

- **`tb/verilator/ctrl_service_budget/edit_rows.py:32` `EDIT_RECORD_US`:** 260 us at 1x1/1if and 325 at 8x8/2if.
  - Each is the most a one-row edit measures over `aecp-fanout`, in arm A (the input map) and in the answering-ports arm (the output map too). At 8x8 only the answering-ports arm edits a map: its input maps have capacity 0.
  - The 1x1/1if figures are an output REMOVE of 24,360 cycles and arm A's input REMOVE of 22,728 (240). The 8x8 figure is 30,563.
  - `:48` `terms`: of the k AECP records a row counts in a window of w ms, `min(k, ceil((w + 1) / P))` are edits. Unpaced, all k are.
- **`tier1_rows.py:134`, `:140`, `:191`:** every row now keeps AECP's records apart from `others` and adds the term `edits`.
- **`rows_tiers.py:137`:** the term belongs to the records source.
- **`rows_tiers.py:465`:** LONG_ROWS take none; they charge each edit the largest legal command's record, as before.
- **The planted control** (`edit_rows.py:71`, in `rows_tiers.py --selftest`, `:885`): *an unpaced edit charged at the non-edit record*. The term takes the pace's count where no pace holds; the control must be refused by name and must shorten the unpaced ACMP row.
- **Why 260 and not 240 at 1x1/1if:** at 240, with the TICK at 50, `rows_tiers.py --selftest` escaped `built 1x1/1if first: the source edits not counted`. The first queued notice charges two AECP records, so its term was 10 us, the rows' resolution. The dearer output edit is also the edit the product makes.

What-ifs at the head, computed in process (`round11/scripts/whatif.py`). Starred figures are over their bounds.

| AECP's costs | ACMP | ADP | MAAP | Last notice | txL |
|---|---:|---:|---:|---:|---:|
| The split at 260 (the tree) | 28.64 | 27.01 | 27.13 | 127.22 | 48.23 |
| The split at 295, the uncut head | 28.78 | 27.15 | 27.27 | 127.78 | 48.23 |
| Flat 295 | 33.21* | 28.87 | 28.99 | 135.37* | 53.07* |
| Flat 240 | 28.64 | 27.01 | 27.13 | 127.01 | 48.32 |
| Non-edits at 355 (answering-ports SET_CONFIGURATION) | 35.60* | 33.78* | 34.01* | 141.49* | 57.06* |

These are at the final costs. At round 10's other costs, before the TICK and ACMP's owed frame were restated, the "295" lines reproduced the amendment's own scratch figures within 0.06 ms: 28.68, 127.42 and 48.09 against 28.69, 127.48 and 48.12 for the split, and 33.10, 134.99 and 52.91 against 33.12, 135.06 and 52.94 flat (`receipts/model/whatif-tick45.txt`).

### 4. The TICK (`0a474c6f`), ACMP's owed frame and THE TRANSMIT's figure (`6ec12ad7`)

- **At `7398ec0a`:** 4,617 cycles = 508 commits and 29 refills.
  - AECP's sink, about 1,400 cycles: its poll transmits an owed frame (`transmit` 434, `now` 266, `arm` 205).
  - SRP's on_event: 809 cycles in 19 commits.
  - The loop and the take: about 2,000.
- **Every other TICK** was at most 3,241.
- **Under the cut,** the same TICK of `backlog-adp@program-0` is 3,242 cycles. AECP's sink there takes 103 cycles and sends nothing; the frame goes out in another pass.
- **Why it is restated anyway:** the coincidence can recur, and in the final pass's full arm A it did: one TICK in another group is 4,612 cycles, 50 us by the rule. Moving the transmit out of the tick would be a behaviour change. `load_grade.py:137` and `:169` state a TICK at 1x1/1if at 50 us in both columns, the larger kept.

**ACMP's owed frame.**

- Under the cut, its send in `backlog-owed` is 4,890 cycles: 55 us by the rule, over the 50 stated. At `7398ec0a` it was 4,723, exactly 50. The code after the map edit's moved with the cut.
- It is now stated at 55 us at 1x1/1if (`poll_grade.py:89`, `load_grade.py:172`).
- With it, the tx row takes a seventeenth pass: 33.01 ms, within its 49.
- `CTRL_LOOP_TX_MS`, THE TRANSMIT's stated figure, must not be under that row, so `ctrl_loop.h:366` states it at 34 ms. Only a static assertion reads the figure (`ctrl_loop.c:203`, held to 49 ms), so every image is byte-identical.
- The two controls that plant it one ms under the row are re-anchored at 34 and 33 (`rows_tiers.py:932`, `flip_grade.py:174`).

**The other inputs.** Every other cost the round 4 tools measure over the full arm A is within its statement at the head (`receipts/final/armA/compare-A-at-6ec12ad7-statements.txt`). The two lines that tool still flags are class lines it cannot split: `aecp-fanout`'s edit, held to the edit class, and the largest legal notice, held to `LONG_NOTICE_US` 365 (360 by the rule).
- The datapath events by the rule: AVB 35, AS_PATH 30 and AMAP 25 us at 1x1/1if (35, 35 and 30 stated), and 40, 35 and 25 at 8x8/2if (40, 40 and 25).
- The long record at 8x8: 1,535 us by the rule (1,650 stated).

**Every stated table at 8x8/2if** (#894 issuecomment-6881287231). The same comparison over the 8x8 shape's legs (`receipts/final/armA/compare-8x8-at-final-statements.txt`) found two costs over their statements:
- a pass's events' fixed part: 2,859 cycles in `notice-every-0`, 35 us by the rule against 30 (2,093 at round 9's head);
- ACMP's owed frame: 6,193 cycles, 70 against 65 (already 6,239 at round 9's head).

`9606b3a9` states both at 8x8/2if (`load_grade.py`, both columns; `poll_grade.py:92`). What remains over there is #910's build of one, which `ctrl_loop.c` asserts and which is owed to the owner as before, and the largest legal notice, within its 655 us.

### 5. The gap closed

**`record_classes.py`** holds a final pass's AECP records by class.

- **Naming each record:** each record is a span of `aecp_mbx.c`'s `frame` handler. It is named by the first solicited AECP response committed at or after its start.
- **How each record is held** (by the rule, at its leg's point):
  - `aecp-largest-notice`'s records: `LONG_RECORD_US`.
  - A paced edit: `EDIT_RECORD_US`. Paced means the next AECP record starts more than `AECP_PACE_MS` less 1 ms after it.
  - Every other record, and an unpaced edit: `record.aecp`.
- **Which legs are held:** those of the formal measurement.
  - Arm A.
  - The answering-every-port arm.
  - The answering-ports arm's `aecp` and `aecp-largest-notice`, and its `aecp-fanout`'s edits.
  - Everything else is reported by class.
- **Coverage:** the pass is refused unless its arm A legs at 1x1/1if together ran every group of `run.all_groups`.
- **Planted controls** (`:43`, `:179`; in the harness self-test through `load_grade.py:620`): a pass missing `aecp-fanout`; an unpaced edit; an edit, an ordinary and a long record over their records; and a labelled arm's record held. All six are refused.
- **On real logs** it names SET_CONFIGURATION (0x0006), SET_NAME and the edits. It finds the edits paced, and it refuses a pass of two groups for the 94 it misses.

**At round 11's final pass** (`receipts/final/classes/record-classes-6ec12ad7.txt`): RESULT PASS over the full arm A (96 groups, 3,223 AECP records) and round 9's legs and the answering-ports `aecp-fanout` at both points.

| Point | Class | Dearest, cycles | By the rule | Stated | Where |
|---|---|---:|---:|---:|---|
| 1x1/1if | edit, held | 24,360 | 260 | 260 | answering-ports `aecp-fanout`, REMOVE |
| 1x1/1if | long, held | 86,978 | 915 | 975 | `aecp-largest-notice` |
| 1x1/1if | other, held | 21,908 | 235 | 235 | answering-every-port `notice-every-0`, SET_NAME |
| 1x1/1if | other, reported | 33,724 | 355 | 235 | answering-ports `aecp-fanout`, SET_CONFIGURATION |
| 8x8/2if | edit, held | 30,563 | 325 | 325 | answering-ports `aecp-fanout`, REMOVE |
| 8x8/2if | long, held | 145,770 | 1,535 | 1,650 | answering-ports `aecp-largest-notice` |
| 8x8/2if | other, held | 23,715 | 250 | 265 | answering-every-port `notice-every-0`, SET_NAME |
| 8x8/2if | other, reported | 78,332 | 825 | 265 | answering-ports `aecp-fanout`, SET_CONFIGURATION |

The 8x8-1if legs, lane 894b's point, are reported: their long records are over 1x1/1if's 975 us, as that point states one interface's costs.

### 6. The documents (`9fda93a1`)

- **`docs/design/SPLIT_CONTROL_MEMORY.md`:**
  - `:2368`: the rows table gains the round's row.
  - THE TIERS table: the head's rows at both points.
  - The 1x1/1if fixture: 110,800 B and 41.0 RAMB36.
  - `:2468`: a new subsection, *The one-row edit*: the attribution, the cut, the class split, the check, the TICK, the answering-ports finding and the images.
- **`docs/reference/FR_NFR.md:383`:** the edits' class, the TICK and the rows, in 3.4.1.
- **`sw/firmware/ctrl/aecp/README.md`** and **`tb/verilator/ctrl_service_budget/README.md`:** the cut, the class split and the pass check.

### 7. What the final pass refused, and its fixes (`3e0ca737`, `9106a980`, `2d579e89`)

The final pass ran at `9fda93a1`, with arm A and the harness legs on `bc971054`'s firmware, and three of its checks refused that head. Each fix moves the head; none changes a compiled firmware file.

- **`check_cpp_idiom.py`** (lane gate and docs gate 38) found three multi-declarator declarations against a ratchet of 0. `3e0ca737` declares each on a line of its own.
- **The final pass's full arm A** found ACMP's owed frame over its 50 us (4,890 cycles), so `6ec12ad7` restates it. That put the tx row over `CTRL_LOOP_TX_MS`, which `6ec12ad7` restates at 34 ms.
- **Then the flip check's control** still looked for the old words, `states 29 ms`, and `9106a980` holds it to its own.
- **`fw_coverage.py --check`** (firmware-unit step 12) found one arc of the cut unreached, the self-copy test inside the reach. No input reaches it, and `2d579e89` names it in the coverage exclusions with the reason.
- **The 8x8 legs** found two 8x8/2if statements under their measurements, and `9606b3a9` raises them ([above](#4-the-tick-0a474c6f-acmps-owed-frame-and-the-transmits-figure-6ec12ad7)).

**The images.** Every image is byte-identical across `9fda93a1`, `3e0ca737` and `6ec12ad7`: 332 of 332 files (8 ELFs, their binaries and 316 objects), built on one clone path. A planted one-constant change (`MAP_FLOOR` 264) differs in 24 of them. `9106a980` changes a grader, `2d579e89` a README and `9606b3a9` two graders' tables and a document, so none of them compiles anything.

**Regrading.** Arm A and every leg were regraded with the head's graders on their own builds (`run.py --regrade`). A build is tied to the clone it was made in, so the regrade ran there, at `9fda93a1`, with `6ec12ad7`'s `tb/` applied (`git diff 9fda93a1 6ec12ad7 -- tb`, 4 files). The later `tb/` change, `9106a980`'s, is one flip-check control's words, which grading never reads.

## Findings

| Finding | Resolution | file:line | Verification |
|---|---|---|---|
| The one-row REMOVE's record 27,851 cycles, 295 us by the rule, over `record.aecp`'s 235 (issuecomment-6878200592) | Cut to 22,728, 240 by the rule, 348 cycles still over. The edits are charged as their own class, at most ceil((w + 1) / P) a window at 260 us (amendment step 2). | `aecp_maps.c:244`, `:259`, `:278`, `:434`, `:447`, `:364`; `edit_rows.py:32`, `:48`; `tier1_rows.py:134` | `aecp-fanout` in the final pass's full arm A: REMOVE 22,728, ADD 20,595; the answering-ports arm's output REMOVE 24,360, 260 by the rule, held to 260 by the pass check; `flip_grade.py --check --point 1x1/1if` exit 0 with every row held |
| The one-row ADD's record 22,932 cycles, 245 us by the rule, over 235 | Cut to 20,595, 220 by the rule, within | the same | the same |
| `event.TICK` 4,617 cycles, 50 us by the rule, over 45 | Attributed: AECP's sink sent an owed frame inside the TICK. Restated at 50 us at 1x1/1if in both columns; under the cut the same TICK is 3,242. | `load_grade.py:137`, `:169` | `load_grade.py --check` exit 0 (0.515, 0.511); the final pass's TICKs: at most 4,612 cycles, 50 by the rule |
| No final pass after round 4 ran `aecp-fanout`, so a stated cost moved unseen | `record_classes.py` refuses a pass whose arm A at 1x1/1if missed a group, and holds every record by class, with six planted controls | `record_classes.py:142`, `:179`; `load_grade.py:620` | `record_classes.py --selftest`: 6 of 6; the harness self-test; the final pass: RESULT PASS, every group of arm A run |
| New: ACMP's owed frame 4,890 cycles under the cut (4,723 at `7398ec0a`), 55 us by the rule, over 50, found by the final pass's full arm A | Restated at 55 us at 1x1/1if. The tx row then takes a seventeenth pass, 33.01 ms within 49, and `CTRL_LOOP_TX_MS` is restated at 34 ms over it. Only a static assertion reads it, and every image is byte-identical. | `poll_grade.py:89`, `load_grade.py:172`, `ctrl_loop.h:366`, `rows_tiers.py:932`, `flip_grade.py:174` | `flip_grade.py --check --point 1x1/1if` exit 0; `compare.py` at the head's statements |
| New: the lane gate `check_cpp_idiom.py` refused `9fda93a1`: three multi-declarator declarations, against a ratchet of 0 | Each declared on a line of its own (`3e0ca737`); the images are byte-identical, 332 of 332 | `aecp_maps.c:192`-`:193`, `:281`-`:286` | `check_cpp_idiom.py` rc 0 at the head |
| New: the flip check's planted TRANSMIT figure, re-anchored at 34 and 33 in `6ec12ad7`, still looked for the words `states 29 ms`, so `flip_grade.py --selftest` and the harness self-test escaped it at that head | The control holds its own words, `states 33 ms` (`9106a980`) | `flip_grade.py:178` | `flip_grade.py --selftest` 585 of 585, the harness self-test 0 failures, at `9106a980` |
| New: the firmware coverage ratchet (`fw_coverage.py --check`, firmware-unit step 12) refused `9fda93a1` and `6ec12ad7`: `aecp_maps.c`'s branches 351 of 352. The second arc of `kept++ != k` is unreachable inside the reach: its first row is always one the REMOVE removes. | The arc is named in the coverage exclusions with that reason (`2d579e89`). No firmware changes, so the measurement stands. | `sw/firmware/gtest/README.md:319`; `aecp_maps.c:296` | `fw_coverage.py --check` PASS (39 files) and `--selftest` 29 of 29 at the head; firmware-unit at the head, every step rc 0 |
| #894 issuecomment-6881287231: every stated table the rows read must be checked against this head's measurements by the rule, not only `load_grade.py`'s | Done at both points. At 1x1/1if, over the full arm A, against `load_grade` (both columns), `poll_grade.STATED_US[1]`, `whole_grade.stated_us(1)` (`ctrl_loop.h`'s pass costs), `rows_grade.ROW_COSTS`, and `rows_tiers.DATAPATH_US`, `LONG_NOTICE_US` and `LONG_RECORD_US`. The polls' base is 18,843 cycles, 200 by the rule against 205. At 8x8/2if, over its legs, the same tables; two raised. | `load_grade.py`, `poll_grade.py:89`, `:92` | `receipts/final/armA/compare-A-at-*-statements.txt`, `compare-8x8-at-final-statements.txt` |
| #894 issuecomment-6881004362: the shard-dispatch self-test leaves `dispatch-build/` untracked in a firmware job's checkout | Reproduced: every run of the AECP, control and SRP campaigns and of firmware-unit leaves `?? dispatch-build/`, at every head this round ran (`aecp_arms.key_arms`, from `58e6b60f`). It fails no step. It is not changed this round, to keep the delta to round 11's items. | `aecp_arms.py:37` | `receipts/final/wf/*/rtl-fast__firmware-*__tree-after.txt` |
| New: the answering-ports arm's SET_CONFIGURATION 33,724 cycles at 1x1/1if (355 us by the rule) and 78,332 at 8x8 (825), over the ordinary record | Reported, not held: the arm is labelled and never the formal measurement, and arm A's fixture refuses the command. It predates the lane (33,533 at `12180198`). Left to the owner. | `SPLIT_CONTROL_MEMORY.md:2468` (the subsection's sixth bullet) | `record_classes.py` reports it on H-B1F and H-B8F |

## Authoritative references

- #894's round 11 assignment, issuecomment-6878230332, and its amendment, issuecomment-6878532871 (the class split).
- The authority, issuecomment-6876349104. The measurement, issuecomment-6878200592.
- The bounds: issuecomment-6858269025, issuecomment-6862465874 and issuecomment-6867990126 (49 ms, 238 ms, 181 to 239 ms). The last queued notice's bound is 130 ms.
- The direct-index ruling, issuecomment-6870437042: the index, the 2 (n + R) bound and the controls are kept.
- IEEE 1722.1-2021 7.4.44 to 7.4.46 (GET_AUDIO_MAP, ADD and REMOVE_AUDIO_MAPPINGS), 9.2.2.6 and 9.3.2.6.
- Milan v1.2 5.4.2.26 to 5.4.2.28 and 5.4.3.4.
- `docs/reference/FR_NFR.md` 3.4.1 and `docs/design/SPLIT_CONTROL_MEMORY.md` section 13.

## How to get into the same state

```sh
git fetch origin
git checkout 894-tiers
git rev-parse HEAD   # 9606b3a915de284c71d3063c2e8d94b097f18241
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if    # exit 0, every row held
python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --selftest                 # 1032 of 1032 refused
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest                 # 585 of 585 refused
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest                 # 25 of 25 refused
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check                    # 0.513 and 0.509, PASS
python3 -B tb/verilator/ctrl_service_budget/record_classes.py --selftest             # 6 of 6 refused
python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if             # 18 of 420 hold, the built design chosen
python3 -B sw/firmware/ctrl/test/aecp_arms.py --output /tmp/aecp-keys --keys         # 7 geometries, rc 0
python3 -B sw/firmware/ctrl/test/aecp_mutants.py --output /tmp/aecp-rows --shard 267 286   # one new row; 267 to 278 are round 11's
# the full arm A at 1x1/1if, then the pass check over it and the other legs:
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir B --record-budget-findings --record-share-findings
python3 -I tb/verilator/ctrl_service_budget/record_classes.py B/results ...
```

Expected:

- Every 1x1/1if row within its bound.
- Every planted control refused.
- The pass check reports the answering-ports arm's SET_CONFIGURATION and refuses nothing held.

The final pass, gate by gate. Commands ran on clean clones and never through a pipe; receipts are under `receipts/final/`.

| Gate | Head | Result |
|---|---|---|
| Full arm A at 1x1/1if (`run.py --point 1x1`, every group, two parts of 48 on one build), regraded with the head's graders | `bc971054`'s firmware | 96 groups, 0 refusals. 7 misses, all `backlog-owed`'s held-egress rows (ruling 6871343905 (a)). 0 of 139,557 passes over THE SHARE. Joins 188.002 to 190.022 ms. Every save within its stated worst case. |
| Round 9's legs at 8x8/2if and 8x8-1if, H-L1N, C-R1, and the answering-ports `aecp-fanout` at 1x1 and 8x8 (13), regraded | the same | 8 exit 0. H-81L, H-81A, H-81N, H-J8 and H-J81 exit 1 on round 9's own STATED lines and error (the 8x8-1if point, and #910's build of one). |
| `record_classes.py` over every leg | `9606b3a9`'s graders | RESULT PASS: every group of arm A run. Held classes within: at 1x1/1if the edit 260 of 260, the long record 915 of 975 and the other records 235 of 235; at 8x8/2if 325 of 325, 1,535 of 1,650 and 250 of 265. Reported, not held: SET_CONFIGURATION at both points, and the 8x8-1if long records. |
| Every stated table by the rule (`compare.py`, both points) | `9606b3a9` | 1x1/1if: only the two class lines. 8x8/2if: #910's build of one and the class line. |
| Images, 332 files (8 ELFs, binaries, objects), one clone path | `9fda93a1`, `3e0ca737`, `6ec12ad7` | identical. Control `MAP_FLOOR` 264: 24 differ. |
| Lane gates, part a (46) | `9fda93a1`, `6ec12ad7` | rc 0 but the four that exit 1 by design (the reported 8x8/2if and as-built rows), `cpp_idiom` at `9fda93a1` (fixed `3e0ca737`), and the flip and harness self-tests at `6ec12ad7` (fixed `9106a980`) |
| Lane gates, parts b and c (`test_builder`; `nvm_selftest`, `boot_1x1`, `boot_8x8`, `boot_native`, `boot_plants`) | `9fda93a1`, `6ec12ad7` | rc 0 |
| Lane gates that read the model or the text (33: every `diff --check`, `em_dash`, both idiom gates, `docs_check`, the model's self-tests and checks, `tier_grid`, the probes) | `9106a980`, `9606b3a9` | rc 0 but the four by design, at both heads. The harness self-test has 0 failures; the self-tests refuse `rows_tiers` 1,032 of 1,032, flip 585 of 585, load 25 of 25 and record classes 6 of 6. |
| Every workflow step (`verify_wf.py`, `rtl-fast.yml`, `rtl.yml`, `elaborate.yml`, `docs.yml`; the yosys shards 0-4 to 3-4) | `9fda93a1`; `6ec12ad7` | 139 ran, 226 not run with a reason. 2 bad at `9fda93a1` (docs gate 38, the C/C++ idiom; firmware-unit step 12, the coverage ratchet); 1 bad at `6ec12ad7` (step 12). |
| The six firmware jobs | `3e0ca737`, `6ec12ad7` | every step rc 0 but step 12 |
| firmware-unit, every step (`fw_coverage.py --check` PASS, 39 files) | `2d579e89` | rc 0 (67 steps with the docs jobs) |
| The AECP campaign (`aecp_mutants.py`, all rows) | `6ec12ad7` | 286 of 286 caught |
| The docs jobs (docs-gates 0 to 2, docs-a) | `2d579e89`, `9606b3a9` | every step rc 0 (61 at the head), each checkout left clean |
| The four-shard Verilator sweep (`native-shards.py`, one picked range each: 8-15, 16-23, 48-55, 80-87) | `9fda93a1` | each shard's command rc 0 (3,993, 3,879, 4,495 and 3,412 s) |

The sweep and the RTL jobs ran at `9fda93a1`. Every change after it is either a firmware text whose images are byte-identical, or a grader, a README or a document.

## Known limitations / out of scope

- **The answering-ports arm's SET_CONFIGURATION is left to the owner.** It is 33,724 cycles at 1x1/1if (355 us by the rule) and 78,332 on the 8x8 shape (825 us).
  - Arm A's fixture refuses the command, because its stream observation does not answer. The labelled arm, whose ports answer as the product's do, takes it.
  - No stated cost but the arm's `aecp` group's and the edits' is measured over that arm (the harness README).
  - Charged as an ordinary record, it would put ACMP at 35.47 ms, ADP at 33.68 and MAAP at 33.91, the last queued notice at 137.73 and txL at 54.84, each over its bound.
  - It is 33,533 cycles at round 4's head, so it predates this lane.
  - The arm's output-port edits are within their class (260 at 1x1/1if; 325 at 8x8/2if).
- **The REMOVE is not under 235 us.** The cut stops at a principled change: what remains is instruction-fetch stalls, mostly code shared with every command (`aecp_rx` 26 refills, the change notice about 20). Each further change moved every other record by its layout.
- **8x8/2if's rows are reported, not held, as before.** R4 is 42.62 ms, the last queued notice 665.47 and txL 459.40. The load there is 0.794, and 0.754 in the second column.
- **`dispatch-build/` left untracked** by the firmware campaigns' shard-dispatch self-test (issuecomment-6881004362). It is reproduced and not changed this round.
- **8x8-1if's legs are lane 894b's point and exit 1 as in round 9.** So does the 8x8 `srp` leg, on THE TRANSMIT's build slice.
- The tier-model's load does not split the edits. At 260 against 235 and one edit a pace, it adds about 0.003 at 1x1/1if.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (round 11's items 1 to 6; item 3 by the amendment's class split)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes (every gate at the head, or carried from `9fda93a1` by byte-identical images: How to validate)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
