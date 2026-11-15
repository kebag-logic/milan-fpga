[A773]

## Contents

- **[Status](#status)**: round 12's head, SET_CONFIGURATION's record cut and paced, and `894-tiers` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: #894, #904 and #908, with the executor and reviewers.
- **[Description](#description)**: round 12's items in the ruling's order, then the round-11 delta reviews' findings.
- **[Findings](#findings)**: every finding this round answers, each with its resolution, file:line and verification.
- **[Authoritative references](#authoritative-references)**: the rulings and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the commands to check out the branch.
- **[How to validate](#how-to-validate)**: the reviewer's commands, their expected results, and the final pass gate by gate.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what this round leaves open.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

**STOP at 1x1/1if, to the maintainer.** Head `783b1596d4acb431698c6e5da9d3f4506cfc091e`: twelve commits on round 11's `9606b3a9`. `894-tiers` -> `dev-soft-core`. Not for review until the decision below.

Round 12 (#894 issuecomment-6883864236) cut SET_CONFIGURATION's record, paced it, and charged the paced class at 300 us; every 1x1/1if row held after those steps. Before the final pass it also held the SRP drain's record cost to the load gate's (issuecomment-6886633874). The final pass, on the final firmware `a47cd3f2`, then measured four 1x1/1if costs over their statements:

| Cost at 1x1/1if | Measured, CPU cycles | By the rule | Stated before | Where |
|---|---:|---:|---:|---|
| A build of one, and an owed MRPDU by its rule | 69,635 | 735 | 725 | arm A `srp` (68,972 at round 11) |
| A TICK | 4,784 | 55 | 50 | arm A `backlog-adp@program-0` (4,692 before the drain item) |
| AECP's timer slot | 6,206 | 70 | 65 | the answering-every-port arm, 6 of 16 groups (5,753 at `9606b3a9`) |
| A LINK | 14,715 | 155 | 150 | arm A `fixture` (13,956 at round 11) |

Restated by the rule (`21aeb997`, `3909588f`), they put **the last queued notice at 132.71 ms against its 130**, and **the slice rule chooses 950 us** over the built 900. The build of one or the TICK alone puts it over (132.64 and 132.65 ms); without both it is 127.98.

| Row (1x1/1if, by every source) | At the head | Bound |
|---|---:|---:|
| R4 | 13.05 | 20 |
| R4L (paced) | 188.43 | 238 |
| ACMP | 28.90 | 30 |
| ADP | 27.25 | 30 |
| MAAP | 27.37 | 30 |
| First queued notice | 14.61 | 20 |
| R5 | 74.02 | 90 |
| R6 | 69.81 | 90 |
| **Last queued notice** | **132.71** | **130** |
| tx | 33.33 | 49 |
| txL | 48.38 | 49 |

- **The load:** 0.516 at the pin and 0.512 in the second column, against 0.70.
- **The join intervals:** 187.994 to 190.021 ms in arm A, and 185.486 to 190.147 ms over every leg, within 181.0 to 239.0 ms.
- **The pace:** 8 ms, still the smallest that holds txL and R4L.
- **The slice rule** (`tier_grid.py --point 1x1/1if`): 10 of 420 candidates hold. It chooses slice 950 us, tier 1 aecp-first, tier 2 srp-first, AECP queue, cap 2 (least margin +0.0116); the built design is 900 us.
- **Every image is within its cap:** the 8x8/2if platform holds 130,920 B of 131,072.

**For #894's 8x8 lane** (8x8/2if, reported; its images and statements are unchanged by the 1x1/1if items): R4 44.24, R5 206.45, R6 196.31, the first queued notice 20.93, the last 806.60, R4L 195.76, ACMP 67.94, ADP 68.08, MAAP 69.13, tx 98.49 and txL 459.40 ms. The load is 0.794 at the pin and 0.754 in the second column, and the paced class is 595 us.

## Linked Issue / roles

Relates to #894
Relates to #904
Relates to #908

Executor: `[A773]`
Internal cleared-context reviewer: `[R837]`
External reviewer: `[R838]`

## Description

Round 12 follows #894's ruling issuecomment-6883864236. Round 11's cut, its class split (paced edits at 260 us at 1x1/1if and 325 at 8x8/2if, every other AECP record at 235) and its TICK stand. The defect: the answering-ports arm's `aecp-fanout` SET_CONFIGURATION record, 33,724 CPU cycles at 1x1/1if (355 us by the rule) and 78,332 at 8x8/2if, which no stated cost covered. The product's ports answer as that arm's do, so the path is the product's.

### 1. Attribution

Each record and the passes after it were traced commit by commit (`sim_main.cpp`'s `BUDGET_TRACE_AFTER` and `BUDGET_TRACE_PCS`) on round 11's final-pass builds of the answering-ports arm, whose images equal `9606b3a9`'s (round 11's 332-file identity). The traced runs reproduce the spans exactly (`receipts/attribution/`).

| Point | Record, cycles | Commits | Short stalls | Fetch stalls | Data stalls |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | 33,724 | 6,322 | 16,131 | 8,823 | 2,448 |
| 8x8/2if | 78,332 | 17,729 | 37,812 | 7,322 | 15,469 |

By function (inclusive call tree, `receipts/attribution/tree-b1-frame.txt`, `tree-b8-frame.txt`):

| Part of the record | 1x1/1if | 8x8/2if |
|---|---:|---:|
| The change's publication (`aecp_note` -> the face's `changed` -> `publish`) | 8,376 | 27,666 |
| of it, every stream entry written and looked up (`write_stream`, `current`, `interface_of`) | 4,294 | 19,905 |
| The running check of every stream of the configuration (4 and 18 streams) | 6,618 | 22,704 |
| The command's own scans of every descriptor (`aecp_command` self) | 6,198 | ~18,700 |
| Keeping the changed values (`aecp_keep`) | 1,182 | 640 |
| The record's handling around the command (`aecp_rx`, `transmit`, `arm`, `header`, `applied`, `owe`) | ~10,000 | ~8,000 |

- **The arm's stream port answers without a window read.** The harness's answering-ports variant replaces the face's `stream` with its own (`build.py`, `VARIANTS`): a zeroed answer. So the running check's six GSI window reads a stream, which the product makes, are not in the measured record. The running check's measured cost is the port chain, ACMP's view of each input (1,993 at 1x1/1if) and three clears of the observation.
- **The completion.** In this arm the accepted command never waits: the face's commit is acknowledged inside the port, and the record answers SUCCESS. At 1x1/1if the record sends it; at 8x8/2if the pass's poll does. No IN_PROGRESS goes out at either point. The pass after the record does no work of the change:
  - its AECP poll fans the notice out to the registered controllers (20,631 cycles at 1x1/1if, 16 recipients; 28,308 at 8x8/2if, the response and 32 recipients), held by the harness as AECP's notice item;
  - the AECP bridge's delivery is 4,124 cycles (the saved-state mark and the store words; the face owes nothing);
  - at 8x8/2if the next centisecond's dispatch is SRP's timer tick (6,941), unrelated.

### 2. The cut (`f275b619`), once

- **The running check reads only what it uses** (`aecp_commands.c:125`, `aecp_face.c:169`). It still observes every stream of the configuration in force, first, before the lock and index checks. The observation is now brief (`aecp_stream_info.brief`, `aecp.h:106`): bound and running are all the check uses, so the face reads one GSI word a stream, selector 0, whose answer proves the window answers, where it read six. Bound comes from ACMP's view and running from the SRP owner's licence, as before.
  - An input bound or an output streaming still answers STREAM_IS_RUNNING, including for a SET naming the index in force (Milan v1.2 5.4.2.5, stricter than IEEE 1722.1-2021 7.4.7.2).
  - An observation the window does not answer still answers ENTITY_MISBEHAVING.
  - GET_STREAM_INFO and SET_STREAM_INFO still read their six words (`aecp_stream_read`, `aecp_commands.c:116`).
- **A configuration's stream entries are written only when its index moves** (`aecp_commands.c:198`, `:214`; `aecp_face.c:119`). The change now names whether the index moved, as `changed`'s index (1 or 0; `aecp.h:170`). A SET naming the index in force, the first of which sets its override, commits the settings alone. The wait's completion re-notes the same change, so a change that moved the index republishes the streams either way.
- **Unchanged:** every status and its order, and the notify rule (a SET notes a change when the index moves or its override is first set).
- **Measured once** (`r12/cut-wt`, arm B `aecp-fanout`): at 1x1/1if 28,509 cycles, 300 us by the rule, still over 235; at 8x8/2if 55,377 (585). So item 3's second branch applies.

### 3. Paced (`fe0cef5b`, `e4d80a8a`)

- **An accepted SET_CONFIGURATION stamps THE PACE** as a checked map edit does (`aecp_commands.c:196`; `aecp_maps.c:424` for the edits; `aecp_mbx.h`, THE PACE). AECP's next record waits in its ring, never dropped, until `AECP_PACE_MS` after it. A refused one stamps nothing.
- **It shares the edits' count:** at most `ceil((w + 1) / P)` paced records in a window of w ms.
- **The paced class's record is the dearer of its members' by the rule** (`edit_rows.py:38`, `:41`):

| Point | One-row edit | Accepted SET_CONFIGURATION (final image) | Paced class |
|---|---:|---:|---:|
| 1x1/1if | 260 (24,418 cycles) | 300 (28,376) | **300** |
| 8x8/2if | 325 (30,124) | 595 (56,474) | 595, reported |

- **The planted control** (`edit_rows.py:43`, `:86`): the class charged at the edits' record alone, the SET_CONFIGURATION left out of the pace and charged as ordinary, is refused by name (`an accepted SET_CONFIGURATION charged below its record`) and shortens the held ACMP row. The pass check has its own control for an unpaced SET_CONFIGURATION (section 5).
- **The images:** the cut and the stamp add 216 B of rom to each image but the 1x1/1if size fixture, 224 B there (`receipts/images/rom-per-image.txt`). Every image is within its cap: the 8x8/2if platform holds 130,920 B of 131,072 (152 B spare, 60.0 RAMB36), the 8x8/1if platform 129,624 B (56.0), and the 1x1/1if size fixture 111,024 B (41.0). Sram is unchanged.

The rows at `e4d80a8a`, with the paced class at 300 us and before the final pass's restatements, all held: R4 13.01, R5 73.80, R6 69.60, the first queued notice 14.59, the last 127.86, R4L 188.41, ACMP 28.80, ADP 27.17, MAAP 27.29, tx 33.21 (`CTRL_LOOP_TX_MS` 34) and txL 48.23 ms. The load was 0.515 and 0.511, the pace 8 ms, and the slice rule chose the built design (18 of 420 hold). The [status](#status) gives the head's rows.

### 4. The completion tick

The ruling holds the completion's tick against `event.TICK`. In the answering-ports arm there is no completion after the record (section 1), and the window's only TICK comes before the command:

| Point | TICK in the SET_CONFIGURATION window | By the rule | `event.TICK` |
|---|---:|---:|---:|
| 1x1/1if | 2,159 cycles | 25 us | 50 |
| 8x8/2if | 2,404 cycles | 30 us | 40 |

So the completion restates nothing (`receipts/attribution/tickwin-*.txt`). Arm A at the final firmware then measured a TICK at 4,784 cycles in `backlog-adp@program-0`, and `event.TICK` is restated at 55 us for that ([section 7](#7-every-stated-table-by-the-rule-over-the-answering-every-port-arm-too-r837-6-f1-and-the-restatements-21aeb997-3909588f)). The wait's completion after a late acknowledgement, which republishes an owed interface whole, is staged by no arm ([below](#known-limitations--out-of-scope)).

### 5. The pass check (`e4d80a8a`, `record_classes.py`)

- **Holds the answering-ports arm's `aecp-fanout` SET_CONFIGURATION and SET_STREAM_INFO by class** (`record_classes.py:49`, `:134`), whose accepted paths no other arm reaches. An accepted SET_CONFIGURATION (SUCCESS or IN_PROGRESS) is in the paced class where the next record follows it by more than the pace less 1 ms (`:142`); else it is held as ordinary.
- **Refuses a pass** whose answering-ports leg at 1x1/1if ran no accepted SET_CONFIGURATION or no SET_STREAM_INFO in `aecp-fanout` (`:189`).
- **Names a record by its own response** (R837-6-S2, `:102`): the first solicited response committed at or after its start and before the next record's, else unanswered. A record that answers nothing is never named by a later one's response. A response the owed-notice queue does not take is committed by the pass's poll after the span, so the bound is the next record, not the span's end.
- **Eleven planted controls** (six were round 11's), run in the harness self-test: arm B's SET_CONFIGURATION missing, its SET_STREAM_INFO missing, an unpaced SET_CONFIGURATION charged as ordinary (`SET_CONFIGURATION not paced`), a SET_CONFIGURATION over the paced record, and a record named by a later record's response. The last escapes when the naming is the old unbounded one (`receipts/model/record-classes-naming-control.txt`).

Over every leg of the final pass (`receipts/classes/record-classes-21aeb997.txt`), the result is RESULT PASS:

| Point | Paced (dearest) | Ordinary (dearest held) | Long |
|---|---|---|---|
| 1x1/1if | SET_CONFIGURATION 28,376, 300 of 300 | 22,236 (the every-port arm's SET_NAME), 235 of 235 | 87,895, 925 of 975 |
| 8x8/2if | SET_CONFIGURATION 56,474, 595 of 595 | 23,485, 250 of 265 | 146,678, 1,545 of 1,650 |

Arm B's SET_STREAM_INFO is 19,925 cycles at 1x1/1if (210) and 19,080 at 8x8/2if (205), each an ordinary record.

### 6. The tests and plants

New tests (`sw/firmware/ctrl/test/test_aecp.cpp`):

| Test | Holds |
|---|---|
| `Core.TheRunningCheckObservesEveryStreamBriefly` (`:1903`) | SET_CONFIGURATION observes every stream of the configuration, each briefly; SET_STREAM_FORMAT's check is brief; GET_STREAM_INFO reads whole |
| `Core.AConfigurationChangeNamesWhetherItsIndexMoved` (`:1919`) | the index in force notes (0, 0) once; a moved index (0, 1), each way; no repeat |
| `Face.TheRunningCheckReadsOneWindowWordAStream` (`:3890`) | one GSI word a stream, selector 0; GET_STREAM_INFO's six; STREAM_IS_RUNNING for the index in force while an output streams; ENTITY_MISBEHAVING when the window is silent |
| `Face.OnlyAMovedConfigurationIndexWritesTheStreamEntries` (`:3908`) | no stream entry for the index in force; every entry of the configuration named, its own formats, on a moved index; again on moving back |
| `Mailbox.AnAcceptedConfigurationHoldsTheNextRecordForThePace` (`:3457`) | the next record held to the pace's last millisecond and then answered; a refused SET holds nothing |

The tests that send another command right after an accepted SET_CONFIGURATION now let the pace pass first, as they already did after an edit: the Face fixture's `receive` and the latency test.

Thirteen campaign rows (`sw/firmware/ctrl/test/aecp_configuration_mutants.py`), each caught by name, and round 11's `face-write-after-response` re-anchored on the changed line (`aecp_mutants.py:578`):

| Row | Plant | Caught by, words |
|---|---|---|
| `running-reads-every-word` | the brief read ignored | `Face.TheRunningCheck...`: one word a stream, selector 0 |
| `running-reads-no-word` | a brief read reads nothing | the same: status for command 6; `Face.StreamAvbAndFormat...`: status for command 8 |
| `running-reads-another-word` | the brief read takes selector 2 | one word a stream, selector 0 |
| `running-check-blind-to-the-licence` | a brief read never streams | status for command 6 and 8 |
| `running-check-reads-whole` | `running` not brief | `Core.TheRunningCheck...`: SET_CONFIGURATION observes every stream, briefly; the Face test |
| `stream-read-brief` | `aecp_stream_read` brief | GET_STREAM_INFO reads the stream whole; reads its six |
| `configuration-streams-every-time` | every stream on every configuration change | the index in force writes no stream entry |
| `configuration-streams-never` | no stream entry ever | a moved index writes the stream entries |
| `configuration-move-unnamed` | the note's index always 0 | `Changed(AECP_CHANGE_CONFIGURATION,0,1)`; a moved index writes the stream entries |
| `configuration-move-always-named` | the note's index always 1 | `Changed(AECP_CHANGE_CONFIGURATION,0,0)`; the index in force writes no stream entry |
| `configuration-moved-by-its-override` | moved read from the override | the same |
| `configuration-unpaced` | the stamp removed | held 1 ms after the accepted SET_CONFIGURATION |
| `configuration-paced-when-refused` | the stamp before the running check | a refused SET_CONFIGURATION holds nothing |

### 7. Every stated table by the rule over the answering-every-port arm too (R837-6-F1), and the restatements (`21aeb997`, `3909588f`)

The final pass ran the answering-every-port arm at 1x1/1if whole, all 16 groups (E1), where round 11 ran its `notice-every-0` alone. `compare_point.py` held every stated table by the rule over arm A (both parts, `A1/` and `A2/`), E1 (`E1/`) and the answering-ports leg (`B1F/`), each line naming its leg (`receipts/final2/compare/`). The tables are both `load_grade` columns, `poll_grade.STATED_US[1]`, `whole_grade.stated_us(1)`, `rows_grade.ROW_COSTS`, `rows_tiers.DATAPATH_US`, `LONG_NOTICE_US` and `LONG_RECORD_US`. The 8x8/2if compare reads its legs the same way (`receipts/final/compare/compare-8x8.txt`).

The final pass ran twice. The first ran on `fe0cef5b`'s firmware and found three costs over; the SRP drain item then changed the one-interface firmware, so every one-interface leg ran again on `a47cd3f2`'s. That second pass found the same three and a TICK (the [Status](#status) table).

| Restated at 1x1/1if | file:line |
|---|---|
| AECP's timer slot, 70, both columns | `load_grade.py:138`, `:174` |
| A LINK, 155 | `rows_grade.py:93` |
| A build of one, 735, and an owed MRPDU with it | `ctrl_loop.h:326`, `load_grade.py:177`, `poll_grade.py:90` |
| A TICK, 55, both columns | `load_grade.py:138`, `:174` |

- **The timer slot** is the same work as at `9606b3a9`. There the same groups measure 5,329 (`notice-every-5`) and 5,753 (`notice-burst-5`), 65 by the rule. The traced events have 1,024 and 1,030 commits, and the SET_CONFIGURATION cut's code adds 479 cycles of instruction-fetch stalls (`receipts/attribution/budget-e1-timer.txt`).
- **The build of one** is round 11's 68,972 cycles, 725 by the rule exactly, moved by the cut's layout to 69,635. The `srp` group's log is byte-identical at both firmwares.
- **The TICK** is 4,692 cycles on the first pass and 4,784 on the second: the drain's record cost moves which SRP records a pass takes.
- **Image identity:** `CTRL_LOOP_BUILD_ONE_PASS_US` feeds only a static assertion. 332 of 332 image files (8 ELFs, binaries and objects, one clone path) are identical across `30a01422`, `94e828ed` and `21aeb997` (`receipts/images/image-sha256-*.txt`). Nothing under `sw/` changed after `a47cd3f2`.
- **At the head's statements** only the class lines remain at 1x1/1if: the paced edit and SET_CONFIGURATION, and the largest legal notice within `LONG_NOTICE_US`. The polls' base is 19,074 cycles, 205 of 205. At 8x8/2if, #910's build of one remains, as before (145,595 cycles).
- **The slice rule's rerun** leaves the built design ([Status](#status)).

### 7a. The SRP drain's record cost (`1c0ca94b`, `a47cd3f2`; #894 issuecomment-6886633874, from #895 issuecomment-6886630886 item 8)

- **The defect.** `ctrl_loop.h` stated `CTRL_LOOP_SRP_UNIT_US` at 250 us at one interface as the load gate's SRP record cost, where `load_grade.py` states that cost at 280. The slice starts an SRP record only while it has that much left (`ctrl_loop.c:322`, `start + CTRL_LOOP_SLICE_US - CTRL_LOOP_SRP_UNIT_US`), so a 280 us record could start with 250 us left.
- **The fix.** The constant is the load gate's `record.srp` at each point, the dearer of the two columns': 280 us at one interface and 365 at two (`ctrl_loop.h:282`). `load_grade.py --check` refuses any other figure by name (`load_grade.py:266`, `srp_unit`, in `findings`): at 250 it fails with `1x1/1if: ctrl_loop.h states CTRL_LOOP_SRP_UNIT_US 250 us, not the load gate's record.srp 280 us`.
- **The planted control** `the SRP drain's record cost not the load gate's` plants 250 at one interface and 300 at two; each is refused by name (`load_grade.py:563`; `load_grade.py --selftest` 26 of 26).
- **The tests.** `Loop.L23TheDrainIsTierTwoInASlice` reads the constant, so it holds the limit at 280 (the loop arm: 51 tests pass). The campaign row `drain-past-its-time` (`loop_step_mutants.py:222`) plants the limit's own text, which is unchanged.
- **The images.** Only the one-interface images change, in `ctrl_loop.o`, the ELF and its binary, at equal sizes. Every two-interface image is byte-identical (`receipts/images/image-sha256-a47cd3f2.txt`), so the 8x8/2if legs stand. Every one-interface leg was measured again at `a47cd3f2`: the full arm A, the answering-every-port arm, the answering-ports leg, C-R1 and the 8x8-1if legs.

### 8. The round-11 delta reviews' other findings

- **Per-image rom** (R838-6-F1, R837-6-R2): section 13's "220 B of rom to every image" is replaced by each image's growth, reconciled against `7398ec0a`. Round 11's cut added 224 B to each 1x1 image (the size fixture 110,576 to 110,800 B) and 208 B to each 8x8 image (the 8x8/2if platform 130,496 to 130,704 B). Round 12's growth is stated the same way (`receipts/images/rom-per-image.txt`).
- **No stale current figure** (R838-6-F2): section 13's current summary gives this head's R4, and this body's validation examples give this head's load (`load_grade.py --check`: 0.515 and 0.511).
- **No review round or lane name in source comments** (R838-6-R1, R837-6-R1; `30a01422`): `edit_rows.py`, `record_classes.py`, `load_grade.py` and `poll_grade.py` name the issue, the cut (`bc971054`) and measured commits (`5b264bf2` for the old "round 9's head"). Numbers and behaviour are unchanged, and the new comments name none either. The same wording in `sw/firmware/gtest/README.md` is fixed too.
- **Historical margins** (R838-6-R2, R837-5-R1): "The margins at this head" is now "The margins in round 30's measurements", and "arm A's least margin at this head" drops "at this head" (`SPLIT_CONTROL_MEMORY.md`).
- **Identity wording** (R838-6-R3): where a carry rests on identity, this body says that none of the later commits changes the compiled firmware output, as the image and object identity receipts show.
- **The packet's index** (R837-6-S1): receipts are sanitized first, then indexed, and the indexer reads every row back against its file and fails on a mismatch (`scripts/index.py`).

### 9. The documents (`94e828ed`, `99626ee4`, `783b1596`)

- **`docs/design/SPLIT_CONTROL_MEMORY.md`:** THE TIERS rows at the head at both points; the rows-history table gains two rows (the record cut and paced, and the final pass's restatements); new subsections *The SRP drain's record cost* and *The final pass's restatements*; *The one-row edit*'s images bullet per image and its arm-B bullet pointing on; a new subsection, *SET_CONFIGURATION's record* (the attribution, the completion, the cut, the pace, the tests, the pass check and the images); the reviewed headings and the current R4.
- **`docs/reference/FR_NFR.md` 3.4.1:** the paced records, the class at 300 us, the pass check, and the final pass's restatements with the last queued notice over its bound.
- **`sw/firmware/ctrl/aecp/README.md`** (the cut and the pace) and **`tb/verilator/ctrl_service_budget/README.md`** (the paced class and the pass check).

## Findings

| Finding | Resolution | file:line | Verification |
|---|---|---|---|
| Ruling 6883864236: arm B's SET_CONFIGURATION record 33,724 cycles at 1x1/1if (355 by the rule) and 78,332 at 8x8/2if, which no stated cost covers | Attributed (item 1). Cut once (`f275b619`): one GSI word a stream for the running check, and stream entries only on a moved index. That gives 28,509 (300) and 55,377 (585). Still over 235, so it is paced (`fe0cef5b`) and the paced class is the dearer member (`e4d80a8a`): 300 at 1x1/1if, 595 at 8x8/2if | `aecp_commands.c:100`, `:125`, `:196`, `:198`, `:214`; `aecp_face.c:119`, `:169`; `aecp.h:106`, `:170`; `edit_rows.py:38`, `:41` | arm B in the final pass: 28,376 (300 of 300) and 56,474 (595 of 595) held as paced by `record_classes.py`; 4 new tests and 1 for the pace; 13 rows caught by name; AECP campaign 299 of 299 |
| Ruling item 3: a planted control charging an unpaced SET_CONFIGURATION as ordinary must fail by name | Model: the class at the edits' record alone is refused by name (`an accepted SET_CONFIGURATION charged below its record`) and shortens ACMP's row. Pass check: a SET_CONFIGURATION followed within the pace is held as ordinary and refused (`SET_CONFIGURATION not paced`) | `edit_rows.py:43`, `:86`; `record_classes.py:257` | `rows_tiers.py --selftest`: the control refused; `record_classes.py --selftest` 11 of 11 |
| Ruling item 4: the completion tick against `event.TICK` | Arm B never waits; the window's only TICK precedes the command: 2,159 (25) and 2,404 (30), within 50 and 40, so the completion restates nothing. (The TICK is restated at 55 us on arm A's `backlog-adp` groups at the final firmware: below.) The late-acknowledgement completion is staged by no arm (open) | `receipts/attribution/tickwin-*.txt` | the traced passes after the record (`tree-b1-poll.txt`, `tree-b1-deliver.txt`, `tree-b8-*.txt`) |
| Ruling item 5: hold arm B's SET_CONFIGURATION and SET_STREAM_INFO, and refuse a pass lacking them | Held by class; a pass whose 1x1/1if answering-ports leg ran no accepted SET_CONFIGURATION or no SET_STREAM_INFO is refused; planted controls for each | `record_classes.py:49`, `:134`, `:189`, `:255` | `record_classes.py --selftest` 11 of 11; over every leg RESULT PASS |
| R837-6-F1 (MINOR): the 1x1/1if stated-table survey read only arm A legs | The answering-every-port arm run whole at 1x1/1if (16 groups), and every stated table compared by the rule over it, arm A and arm B, each line with its leg prefix. It found AECP's timer slot over (6,206, 70 > 65), and arm A found a LINK (155 > 150), a build of one (735 > 725) and, at the final firmware, a TICK (55 > 50). All four restated; rows, the pace and the slice rule rerun: **the last queued notice 132.71 > 130 and the slice rule chooses 950 us: STOP** | `load_grade.py:138`, `:174`, `:177`; `rows_grade.py:93`; `ctrl_loop.h:326`; `poll_grade.py:90` | `receipts/final2/compare/compare-1x1-at-99626ee4-statements.txt` (`A1/`, `A2/`, `E1/`, `B1F/`), `receipts/final/compare/compare-8x8.txt`; `receipts/model/flip-1x1-3909588f.txt` (exit 1), `tier-grid-1x1-3909588f.txt` |
| R838-6-F1 (MINOR), R837-6-R2: "the cut adds 220 B of rom to every image" | Replaced by each image's growth against `7398ec0a`: +224 B in each 1x1 image, +208 B in each 8x8 image. Round 12's growth is stated the same way: +216 B, and +224 in the 1x1/1if size fixture | `SPLIT_CONTROL_MEMORY.md:2480`, its new subsection's images bullet | `receipts/images/rom-per-image.txt` (8 images at `7398ec0a`, `9606b3a9`, `fe0cef5b`) |
| R838-6-F2 (MINOR): section 13's current R4 12.85 and the validation example's load were the previous head's | Section 13's current rows table, its rows-history row, its current summary (R4 13.05, the last queued notice 132.71 over 130) and its load (0.516 and 0.512), and FR_NFR 3.4.1, are the head's; so are this body's examples | `SPLIT_CONTROL_MEMORY.md:2346`, `:2370`, `:2524`; `FR_NFR.md:383`; [How to validate](#how-to-validate) | `flip_grade.py --check --point 1x1/1if` and `load_grade.py --check` at the head (`receipts/model/*-3909588f.txt`) |
| R838-6-R1, R837-6-R1 (RESIDUE): round and lane names in new source comments | Reworded with the issue, the cut and the measured commits; numbers and behaviour unchanged; none in the new comments | `edit_rows.py:3`, `:29`; `record_classes.py:4`, `:84`; `load_grade.py:126`, `:130`; `poll_grade.py:86`, `:89`; `gtest/README.md:319` | `git diff 9606b3a9 30a01422`: comment lines only |
| R838-6-R2, R837-5-R1 (RESIDUE): "The margins at this head" and "at this head" on round 30's figures | "The margins in round 30's measurements", and "at this head" dropped | `SPLIT_CONTROL_MEMORY.md:2506`, `:2484` | the text |
| R838-6-R3 (RESIDUE): "none changes a compiled firmware file" | This body states that none of the later commits changes the compiled firmware output, as the image and object identity receipts show | this body | `receipts/images/image-sha256-*.txt` |
| R837-6-S1 (SUGGESTION): the packet index was generated before sanitizing | Taken: receipts are sanitized, then indexed, and every row is read back; a mismatch fails the indexer | `scripts/index.py` (the packet) | `INDEX.md`, generated last |
| R837-6-S2 (SUGGESTION): a record named by a later record's response | Taken: a record takes the first response before the next record starts, else it is unanswered. A synthetic control escapes under the old naming and is refused under the new | `record_classes.py:102` | `receipts/model/record-classes-naming-control.txt` |
| #894 issuecomment-6886633874 (from #895 issuecomment-6886630886 item 8): `CTRL_LOOP_SRP_UNIT_US` stated 250 us at 1x1/1if where the load gate states an SRP record at 280, so the SRP drain (`ctrl_loop.c:322`) could start a 280 us record with 250 us left | The constant is the load gate's `record.srp` at each point, the dearer column's, 280 and 365 us (`1c0ca94b`); `load_grade.py --check` refuses any other figure by name, with a planted control at each point (`a47cd3f2`, the controls in a function of their own within the long-function ratchet) | `ctrl_loop.h:282`; `load_grade.py:262`, `:266`, `:563` | `load_grade.py --check` at 250: `1x1/1if: ctrl_loop.h states CTRL_LOOP_SRP_UNIT_US 250 us, not the load gate's record.srp 280 us`; `--selftest` 26 of 26; the loop arm 51 tests (L23 holds the limit at 280); the one-interface legs measured again at `a47cd3f2`; two-interface images byte-identical |
| New: the TICK at the final firmware, 4,784 cycles in arm A's `backlog-adp@program-0`, 55 us by the rule, over 50 (4,692 on the drain's earlier figure) | Restated at 55 us, both columns (`3909588f`) | `load_grade.py:138`, `:174` | `receipts/final2/compare/compare-1x1-at-a47cd3f2-statements.txt` |
| New: `aecp_mutants.py` over the long-module limit once the rows were added (`check_py_idiom.py`: long module 11 > 10 at `fe0cef5b`) | The rows moved to their own table, `aecp_configuration_mutants.py` (`1c8c071b`) | `aecp_mutants.py:936` | `check_py_idiom.py` rc 0 |
| New: round 11's `face-write-after-response` plant, anchored on the line the cut changed, escaped on a build refusal (`every` unused) | Its replacement keeps `every` referenced, so the build compiles and the named test fails | `aecp_mutants.py:578` | the row caught by name; campaign 299 of 299 |

## Authoritative references

- #894's round-12 ruling, issuecomment-6883864236.
- Round 11's authority, which stands: issuecomment-6878230332, its amendment issuecomment-6878532871 (the class split), issuecomment-6876349104, and the measurement issuecomment-6878200592.
- The bounds: issuecomment-6858269025, issuecomment-6862465874 and issuecomment-6867990126 (49 ms, 238 ms, 181 to 239 ms). The last queued notice's bound is 130 ms.
- The direct-index ruling, issuecomment-6870437042. The every-table instruction, issuecomment-6881287231.
- The round-11 delta reviews: R837-6 (PR #902 issuecomment-6884063444) and R838-6 (issuecomment-6884009601).
- Milan v1.2 5.4.2.5 (SET_CONFIGURATION refused while any Stream Input is bound or any Stream Output is streaming) and 5.4.5.2.
- IEEE 1722.1-2021 7.4.7 (SET_CONFIGURATION), 7.4.15 (SET_STREAM_INFO), 7.5.2 and 9.3.2.6.
- `docs/reference/FR_NFR.md` 3.4.1 and `docs/design/SPLIT_CONTROL_MEMORY.md` section 13.

## How to get into the same state

```sh
git fetch origin
git checkout 894-tiers
git rev-parse HEAD   # 21aeb997d06fa9a8897eefdaf3f30ebe1c081008
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if    # exit 1: last 132.71 over 130 (the STOP)
python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if             # 10 of 420 hold; slice 950 chosen
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check                    # 0.516 and 0.512, PASS
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest                 # 26 of 26 refused
python3 -B tb/verilator/ctrl_service_budget/record_classes.py --selftest             # 11 of 11 refused
python3 -B sw/firmware/ctrl/test/aecp_mutants.py --output "$(mktemp -d)" --shard 286 299   # one of the 13 new rows (286 to 298)
python3 -I tb/verilator/ctrl_service_budget/record_classes.py B/results ...          # over a pass's legs: RESULT PASS
```

At the head, `rows_tiers.py --selftest` refuses 1,032 of 1,033 controls and `flip_grade.py --selftest` 584 of 585. The two that escape are the model's own consistency controls: the built design's slice being the rule's, and `AECP_QUEUED_MS` being the bound the last queued notice's row rules. The over row itself defeats both. At `e4d80a8a`, before the restatements, they refused 1,033 of 1,033 and 585 of 585.

The final pass, gate by gate. Commands ran on clean clones and never through a pipe. Receipts for the final firmware are under `receipts/final2/`, and those of the first run and the carried 8x8/2if legs under `receipts/final/`.

| Gate | Head | Result |
|---|---|---|
| Full arm A at 1x1/1if (every group, two parts of 48 on one build) | `a47cd3f2` | 96 groups, 0 refusals. 7 misses (`backlog-owed`'s held-egress rows, ruling 6871343905 (a)). 0 of 139,988 passes over THE SHARE. Joins 187.994 to 190.021 ms. |
| The answering-every-port arm at 1x1/1if, all 16 groups | `a47cd3f2` | rc 0; joins 188.071 to 189.937 ms |
| The answering-ports leg at 1x1/1if (`aecp-fanout`, `aecp`, `aecp-largest-notice`), C-R1, and the 8x8-1if legs | `a47cd3f2` | B1F and C-R1 exit 0. H-81L, H-81A, H-81N and H-J81 exit 1 on the same STATED lines and error as round 11. |
| The 8x8/2if legs (B8F, L8A, L8N, L8L, L8O, J8) | `30a01422`, carried: every two-interface image byte-identical to `a47cd3f2`'s | 5 exit 0; J8 exits 1 on #910's build of one, as before |
| `record_classes.py` over every final leg | `3909588f` | RESULT PASS |
| Every stated table by the rule, both points | `3909588f` (later commits are documents) | 1x1/1if: the class lines only, after the four restatements. 8x8/2if: #910's build of one and the class lines. |
| Images, 332 files, one clone path | `30a01422`, `94e828ed`, `21aeb997`; `a47cd3f2` | identical across the first three; at `a47cd3f2` only the one-interface images' `ctrl_loop.o`, ELF and binary differ, at equal sizes |
| The firmware jobs (unit, AECP, control and SRP campaigns, boundary, Verilator) | `a47cd3f2` | 22 steps, every one rc 0. AECP campaign 299 of 299, control 716 of 716, `fw_coverage.py --check` PASS. |
| The four-shard Verilator sweep, each shard on its own picked range (0-7, 8-15, 32-39, 40-47) | `a47cd3f2` | each shard's command rc 0 (3,884, 3,745, 4,277 and 3,314 s) |
| The RTL and elaborate jobs; lane gates, parts b and c (`test_builder`; `nvm_selftest`, `boot_1x1`, `boot_8x8`, `boot_native`, `boot_plants`) | `94e828ed`, before the drain item | every step rc 0; not run again at the final firmware |
| `docs_check.py`, `check_em_dash.py`, both idiom gates | the head | 0 findings; rc 0 |
| Lane gates part a, rtl-fast's other jobs, the docs jobs | the head | not run: the head fails the row gate, so the round stops first |

After `a47cd3f2` only graders' tables and documents changed. None of the later commits changes the compiled firmware output, as the image and object identity receipts show.

## Known limitations / out of scope

- **The wait's completion after a late acknowledgement is staged by no arm.** In every arm the face's commit is acknowledged inside the port. When the datapath acknowledges late, the command waits; the poll that sees the acknowledgement does the change again and notes it, and the face's poll then publishes the owed interface whole, every stream entry included (the late-commit rule `Face.ALateCommitIsOwedAndPublishedAgainWhole` holds). That publication is the record's own publication with every stream (8,376 cycles at 1x1/1if before the cut), in a poll, not in a TICK. No harness arm delays the face's acknowledgement, so its cost is not measured.
- **The product's running check reads one window word a stream**, which the answering-ports arm cannot measure, since its stream port answers without a read.
- **8x8/2if's rows are reported, not held, as before;** its paced class is 595 us. Its figures for #894's 8x8 lane are in [Status](#status).
- **8x8-1if's legs exit 1 as in rounds 9 to 11** (THE TRANSMIT's build slice; the 40-notice model at that point), and so does the 8x8 `srp` leg, on #910's build of one.
- **The tier model's load does not split the paced records.** At 300 against 235 and one paced record a pace, it adds about 0.008 at 1x1/1if.
- **`dispatch-build/` is still left untracked** by the firmware campaigns' shard-dispatch self-test (issuecomment-6881004362), not changed this round.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (round 12's items 1 to 6; item 3 by its second branch, the pace)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes (How to validate)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
