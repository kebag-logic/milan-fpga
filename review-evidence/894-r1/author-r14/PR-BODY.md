[A773]

## Contents

- **[Status](#status)**: the head of rounds 12 to 14, SET_CONFIGURATION's record cut and paced, the slice at the rule's choice, and `894-tiers` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: #894, #904 and #908, with the executor and reviewers.
- **[Description](#description)**: round 12's items in the ruling's order and the round-11 delta reviews' findings, then round 13's.
- **[Round 13](#round-13)**: the slice at the rule's choice, the reruns, the carries and the late-acknowledgement proof.
- **[Round 14](#round-14)**: every figure the round-12 and round-13 moves touched, stated as the head's or as history; item 5's precondition; the identity proof.
- **[Findings](#findings)**: every finding this round answers, each with its resolution, file:line and verification.
- **[Authoritative references](#authoritative-references)**: the rulings and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the commands to check out the branch.
- **[How to validate](#how-to-validate)**: the reviewer's commands, their expected results, and the final pass gate by gate.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what this round leaves open.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

**REVIEW READY at 1x1/1if.** Head `867faf1e`: seventeen commits on round 11's `9606b3a9`, rounds 12 to 14. `894-tiers` -> `dev-soft-core`.

- **Round 12** (#894 issuecomment-6883864236): it cut the answering-ports arm's SET_CONFIGURATION record and paced it, and charged the paced class at the dearer member's record. It held the SRP drain's record cost to the load gate's (issuecomment-6886633874). It restated four 1x1/1if costs its final pass measured over their statements. With those, the last queued notice was over its bound at the 900 us slice, and the slice rule chose 950 us: a STOP (issuecomment-6888749411).
- **Round 13** (the ruling on it, issuecomment-6888782796): the built one-interface slice is the slice rule's choice, 950 us. `ctrl_loop.h` states the rule and the self-tests hold it. Every one-interface leg was measured again on the rebuilt images; every stated table holds there by the rule but for the class lines, so nothing more is restated. A late-acknowledged SET_CONFIGURATION is shown not to complete late on the product port.
- **Round 14** (round 13's delta reviews: R837-7 and R838-7 NEGATIVE, each on one MINOR; R838-8 POSITIVE): documents, two comments and a docstring only. Every figure the round-12 and round-13 moves touched is the head's or stated as history. Item 5's clock and reset precondition is stated. Every image file and harness ELF is byte-identical to `234bc149`'s, so round 13's measurements carry unchanged.

Every CPU-decided row at 1x1/1if holds by every source at the head:

| Row | At the head, ms | Bound, ms |
|---|---:|---:|
| R4 | 13.10 | 20 |
| R4L (paced) | 188.48 | 238 |
| ACMP | 28.95 | 30 |
| ADP | 27.30 | 30 |
| MAAP | 27.42 | 30 |
| First queued notice | 14.66 | 20 |
| R5 | 74.07 | 90 |
| R6 | 69.86 | 90 |
| Last queued notice | 127.21 | 130 |
| tx | 33.38 | 49 |
| txL | 48.43 | 49 |

- **The load:** 0.516 at the pin and 0.512 in the second column, against 0.70.
- **The slice rule** (`tier_grid.py --point 1x1/1if`): it chooses the built design, slice 950 us, tier 1 aecp-first, tier 2 srp-first, AECP queue, cap 2. 10 of 420 candidates hold; the least margin is +0.0116. It did not move again on the rebuilt images.
- **The pace:** 8 ms, the smallest that holds txL and R4L.
- **The join intervals:** 187.994 to 190.021 ms in arm A, and 185.486 to 190.147 ms over every leg, within 181.0 to 239.0 ms.
- **Every image is within its cap:** the 8x8/2if platform holds 130,920 B of 131,072, and the 1x1/1if size fixture 111,024 B (41.0 RAMB36).

**For #894's 8x8 lane and #890** (8x8/2if, reported, no flip row): R4 44.24, R5 206.45, R6 196.31, the first queued notice 20.93, the last 806.60, R4L 195.76, ACMP 67.94, ADP 68.08, MAAP 69.13, tx 98.49 and txL 459.40 ms. The load is 0.794 at the pin and 0.754 in the second column, and the paced class is 595 us. The two-interface images and statements are unchanged by round 13.

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
- **Image identity:** `CTRL_LOOP_BUILD_ONE_PASS_US` feeds only a static assertion. 332 of 332 image files (8 ELFs, binaries and objects, one clone path) are identical across `30a01422`, `94e828ed` and `21aeb997` (`receipts/images/image-sha256-*.txt`). In round 12, nothing under `sw/` changed after `a47cd3f2`.
- **At the head's statements** only the class lines remain at 1x1/1if: the paced edit and SET_CONFIGURATION, and the largest legal notice within `LONG_NOTICE_US`. The polls' base is 19,074 cycles, 205 of 205. At 8x8/2if, #910's build of one remains, as before (145,595 cycles).
- **The slice rule's rerun** left the built design: the last queued notice 132.71 ms over 130 at 900 us, and the rule choosing 950. Round 12 stopped there (issuecomment-6888749411); round 13 takes the rule's choice ([13.1](#131-the-slice-is-the-rules-choice-c274b9f5-its-own-commit)).

### 7a. The SRP drain's record cost (`1c0ca94b`, `a47cd3f2`; #894 issuecomment-6886633874, from #895 issuecomment-6886630886 item 8)

- **The defect.** `ctrl_loop.h` stated `CTRL_LOOP_SRP_UNIT_US` at 250 us at one interface as the load gate's SRP record cost, where `load_grade.py` states that cost at 280. The slice starts an SRP record only while it has that much left (`ctrl_loop.c:322`, `start + CTRL_LOOP_SLICE_US - CTRL_LOOP_SRP_UNIT_US`), so a 280 us record could start with 250 us left.
- **The fix.** The constant is the load gate's `record.srp` at each point, the dearer of the two columns': 280 us at one interface and 365 at two (`ctrl_loop.h:282`). `load_grade.py --check` refuses any other figure by name (`load_grade.py:266`, `srp_unit`, in `findings`): at 250 it fails with `1x1/1if: ctrl_loop.h states CTRL_LOOP_SRP_UNIT_US 250 us, not the load gate's record.srp 280 us`.
- **The planted control** `the SRP drain's record cost not the load gate's` plants 250 at one interface and 300 at two; each is refused by name (`load_grade.py:563`; `load_grade.py --selftest` 26 of 26).
- **The tests.** `Loop.L23TheDrainIsTierTwoInASlice` reads the constant, so it holds the limit at 280 (the loop arm: 51 tests pass). The campaign row `drain-past-its-time` (`loop_step_mutants.py:222`) plants the limit's own text, which is unchanged.
- **The images.** Only the one-interface images change, in `ctrl_loop.o`, the ELF and its binary, at equal sizes. Every two-interface image is byte-identical (`receipts/images/image-sha256-a47cd3f2.txt`), so the 8x8/2if legs stand. Every one-interface leg was measured again at `a47cd3f2`: the full arm A, the answering-every-port arm, the answering-ports leg, C-R1 and the 8x8-1if legs.

### 8. The round-11 delta reviews' other findings

- **Per-image rom** (R838-6-F1, R837-6-R2): section 13's "220 B of rom to every image" is replaced by each image's growth, reconciled against `7398ec0a`. Round 11's cut added 224 B to each 1x1 image (the size fixture 110,576 to 110,800 B) and 208 B to each 8x8 image (the 8x8/2if platform 130,496 to 130,704 B). Round 12's growth is stated the same way (`receipts/images/rom-per-image.txt`).
- **No stale current figure** (R838-6-F2): section 13's current summary gives this head's R4, and this body's validation examples give this head's load (`load_grade.py --check`: 0.516 and 0.512).
- **No review round or lane name in source comments** (R838-6-R1, R837-6-R1; `30a01422`): `edit_rows.py`, `record_classes.py`, `load_grade.py` and `poll_grade.py` name the issue, the cut (`bc971054`) and measured commits (`5b264bf2` for the old "round 9's head"). Numbers and behaviour are unchanged, and the new comments name none either. The same wording in `sw/firmware/gtest/README.md` is fixed too.
- **Historical margins** (R838-6-R2, R837-5-R1): "The margins at this head" is now "The margins in round 30's measurements", and "arm A's least margin at this head" drops "at this head" (`SPLIT_CONTROL_MEMORY.md`).
- **Identity wording** (R838-6-R3): where a carry rests on identity, this body says that none of the later commits changes the compiled firmware output, as the image and object identity receipts show.
- **The packet's index** (R837-6-S1): receipts are sanitized first, then indexed, and the indexer reads every row back against its file and fails on a mismatch (`scripts/index.py`).

### 9. The documents (`94e828ed`, `99626ee4`, `783b1596`)

- **`docs/design/SPLIT_CONTROL_MEMORY.md`:** THE TIERS rows at the head at both points; the rows-history table gains two rows (the record cut and paced, and the final pass's restatements); new subsections *The SRP drain's record cost* and *The final pass's restatements*; *The one-row edit*'s images bullet per image and its arm-B bullet pointing on; a new subsection, *SET_CONFIGURATION's record* (the attribution, the completion, the cut, the pace, the tests, the pass check and the images); the reviewed headings and the current R4.
- **`docs/reference/FR_NFR.md` 3.4.1:** the paced records, the class at 300 us, the pass check, and the final pass's restatements with the last queued notice over its bound.
- **`sw/firmware/ctrl/aecp/README.md`** (the cut and the pace) and **`tb/verilator/ctrl_service_budget/README.md`** (the paced class and the pass check).

## Round 13

Round 13 follows #894's ruling issuecomment-6888782796 on round 12's STOP (issuecomment-6888749411). Round 12's four restatements, its cut, the pace stamp and the drain fix stand.

### 13.1 The slice is the rule's choice (`c274b9f5`, its own commit)

- **The change.** `CTRL_LOOP_SLICE_US` is 950 us at one interface (900 before) and 1,300 us at two (`ctrl_loop.h:279`). The header now states the rule: the built slice is the slice rule's choice within 650 to 1,100 us at one interface (`rows_tiers.py`, `ruled`), which the model's self-test holds.
- **No hand-picked number in the checks.** Two self-test checks anchored on the literal `900u`. The `rows_tiers` control "the built design's slice not the rule's" now reads the header's line and plants 600 us against it (`rows_tiers.py:879`). The round checks' "each point's slice is ctrl_loop.h's stated length at it" now holds it to `rows_tiers.ruled` (`selftest_round.py:109`). A slice other than the rule's choice fails both.
- **`CTRL_LOOP_BUILD_MOST` does not move.** It is 2 only where the slice holds a build of both of an interface's MRPDUs, `CTRL_LOOP_BUILD_PASS_US`, 1,010 us at one interface. At 950 it stays 1, as at 900, so a slice still makes one MRPDU's build and the next slice the other. No row term changes through it.
- **The images.** At one interface `ctrl_loop.o`, the ELF and its binary change, at equal sizes, in the 1x1/1if and 8x8/1if images. Every two-interface image is byte-identical (`receipts/images/`).
- **The tests.** The loop arm (51 tests) and the AECP mailbox arm (124 tests) pass at 950.

### 13.2 The reruns on the rebuilt images (item 3)

All on `c274b9f5`'s firmware, on a clean clone.

| Leg | Result |
|---|---|
| The full arm A at 1x1/1if: every group, four parts of 24 on one build | 96 groups, 0 refusals. 7 misses, `backlog-owed`'s held-egress rows as before. 0 of 140,032 passes over THE SHARE. |
| The whole answering-every-port arm at 1x1/1if: 16 groups | rc 0 |
| The answering-ports leg at 1x1/1if (`aecp-fanout`, `aecp`, `aecp-largest-notice`), and C-R1 | rc 0. SET_CONFIGURATION is 28,376 cycles and SET_STREAM_INFO 19,925, unchanged to the cycle. |
| The 8x8/1if legs (H-81L, H-81A, H-81N, H-J81) | rc 1 on round 11's reasons. That point states one interface's costs: a build of one of 92,066 to 94,601 cycles against 73,500; a polls base of 20,580 against 20,500; and the 40-notice model's RuntimeError. |
| The 8x8/2if legs (B8F, L8A, L8N, L8L, L8O, J8), run again | rc 0, but J8, which exits 1 on #910's build of one as before |

- **The stated-table compare.** At 1x1/1if it reads every one of those legs by leg prefix (`A1/` to `A4/`, `E1/`, `B1F/`); at 8x8/2if, its legs (`receipts/compare/`).
  - At 1x1/1if every statement holds by the rule but for the class lines: the paced edit (245 of 300), the paced SET_CONFIGURATION (300 of 300), and the largest legal notice within `LONG_NOTICE_US` (365 of 365).
  - Among the others: the build of one is 69,635 cycles (735 of 735), the polls' base 19,074 (205 of 205), AECP's timer slot 6,206 (70 of 70), a LINK 14,715 (155 of 155) and a TICK 4,692 (50 of 55).
  - At 8x8/2if, #910's build of one and the class lines remain, as before.
  - Nothing is restated, so the rows, the pace and the slice rule are those at the head ([Status](#status)).
- **The pass check** (`record_classes.py`) over every leg: RESULT PASS. At 1x1/1if: paced 300 of 300, ordinary 235 of 235 and long 925 of 975. At 8x8/2if: 595 of 595, 250 of 265 and 1,545 of 1,650.

### 13.3 Carries (item 4)

- **The 8x8/2if legs were run again** at `c274b9f5` rather than carried, since there was room. Their harness images are byte-identical to the round-12 legs' by sha256: `aecp-fanout`'s and `aecp-largest-notice`'s answering-ports image, and the arm A image (`receipts/images/harness-elf-sha256.txt`). The 166 two-interface image files of the size fixture and the platform are identical across `30a01422` and `c274b9f5` (`receipts/images/image-sha256-*.txt`).
- **The gates carry only by their inputs' identity.** Lane part a, rtl-fast's other jobs, firmware-boundary and the docs jobs ran on a clean clone of the final head `234bc149`. The firmware, RTL and elaborate jobs, lane parts b and c and the sweep ran on one of `ed0df35b`. The two differ only in `tb/verilator/ctrl_service_hooks/hooks.py`, which none of those reads; its one reader, lane part a's hooks self-test, ran at the final head ([How to validate](#how-to-validate)).

### 13.4 A late-acknowledged SET_CONFIGURATION's completion (item 5): it cannot happen on the product port

Shown from the product port, not staged (`receipts/item5-no-late-completion.md`, each link at a file and line):

1. **The contract bounds the acknowledgement.** Contract 2.3: every setting holds until the datapath's acknowledgement, within 64 cycles (`MAILBOX_CONTRACT.md:346`).
2. **The product's datapath meets that bound unconditionally.** The product connects the face through `KL_mbx_cdc` (`milan_soc.py:3154`). The commit's edge crosses as one pulse, and the datapath takes every setting on that pulse, with no ready or backpressure (`KL_mbx_cdc.sv:272`, `:278`). The same pulse is the acknowledgement's source (`:274`).
3. **It is measured on the product composition.** `sim_split.cpp:371` ("[FACE] the commit is acknowledged within MBX_FACE_ACK_CYCLES") clears BUSY in 2 polls against 64, in the sweep's `milan_dp` suite at `ed0df35b`.
4. **The firmware outwaits the bound.** `mbx_face_commit` reads F_STATUS up to `MBX_FACE_ACK_CYCLES` + 1 times, each read a bus cycle or more (`mbx.c:346`). Every commit waits for its own acknowledgement inside the port, so the block is never found busy.
5. **So nothing ever waits.** The face never owes an interface after its open (`aecp_face.c:79-101`), `applied` is always true, and the core never enters the wait (`aecp.c:489`). The completion (`aecp.c:906`) and the whole republication never run.
6. **The measured record already holds the slowest compliant datapath.** The CPU budget harness acknowledges every commit at exactly the bound (`split_soc.py:226`).
7. **The fault path stays tested.** Its behaviour, for a datapath that broke the contract, is held by `Face.ALateCommitIsOwedAndPublishedAgainWhole`.

### 13.5 The documents

- **`ctrl_loop.h`** (`c274b9f5`) states the slice rule beside `CTRL_LOOP_SLICE_US`.
- **`ed0df35b`:**
  - **`docs/design/SPLIT_CONTROL_MEMORY.md`:** THE TIERS rows at 950 us, the rows-history row, the round-13 ruling's text in *The final pass's restatements*, and the current summary.
  - **`docs/reference/FR_NFR.md` 3.4.1:** the slice and the rows.
  - **`docs/design/MAILBOX_SPLIT.md`:** the slice, now 0.95 ms at one interface.
  - **The harness and SRP READMEs:** the slice, and the self-test check's words.

## Round 14

Round 14 answers round 13's delta reviews:
- R837-7 (issuecomment-6890948441): NEGATIVE, on one MINOR;
- R838-7 (issuecomment-6890766701): NEGATIVE, on one MINOR;
- R838-8 (issuecomment-6890858159): POSITIVE.

R838-7-F1 was two sites in this body: the *No stale current figure* bullet and the R838-6-F2 row. Both were corrected before round 14, and both are kept as corrected. Round 14 changes documents, two comments and a docstring, and nothing compiled or executed (`b25530f6`, `867faf1e`). Its receipts are in its own packet. The receipts named in the round-12 and round-13 sections are in round 13's packet.

### 14.1 Every figure the round-12 and round-13 moves touched (R837-7-F1, `b25530f6`)

The moves, each from its old figure to the head's:

| Figure | Old | Head |
|---|---:|---:|
| A build of one, us | 725 | 735 |
| A TICK, us | 50 | 55 |
| AECP's timer slot, us | 65 | 70 |
| A LINK, us | 150 | 155 |
| The SRP drain, us | 250 | 280 |
| The slice, us | 900 | 950 |
| The load (pin, second column) | 0.515, 0.511 | 0.516, 0.512 |

Every row moved too. Each current-tense site now gives the head's figure, or says that the figure was then.

- **`SPLIT_CONTROL_MEMORY.md` section 13:**
  - `:2197`: a build of one is stated at 735 us at 1x1/1if.
  - `:2342`: the rule picked 900 us then. At the costs restated under the SET_CONFIGURATION cut it picks 950 us, and a 950 us slice holds one MRPDU's build. The 8x8/1if sentence gives 735 us now.
  - `:2373`, `:2443` to `:2445`, `:2459`, `:2467`, `:2477` and `:2509` are past tense. Where a figure moved, each gives the head's beside it: 950 us since #894's ruling of 2026-11-15, and 735 us since the cut.
  - `:2380`: at the head the pace finds 8 ms, txL 48.43 ms and R4L 188.48 ms (48.09 and 188.39 then). The load is 0.516 at the pin, and 0.695 with every command the largest legal one.
  - `:2479`, `:2480` and `:2489`: the TICK was stated at 50 us then, and is 55 since the SRP drain's record cost moved. The tx row's 33.01 ms is history beside the head's 33.38 ms.
- **`FR_NFR.md:383`:** "8 ms then held txL, 48.23 ms".
- **`sw/firmware/ctrl/srp/README.md:238`:** 33.38 ms at the 950 us slice. As history: 33.01 at 900 us under the one-row edit cut, and 29.78 before it.
- **`poll_grade.py:70`** (found by the sweep; a comment only): a retained record's retry is stated at the SRP record's cost, 280 and 365 us. It said 250 and 365.
- **The grep receipt** (`receipts/stale-figures-grep.txt`, generated again on the clean clone at `867faf1e`):
  - Tokens: 725, 33.01, 900 us, 0.515, 0.511, 13.05 and 132.71; 50 on a line naming a TICK; 65 on a line naming AECP, a timer or a slot; 150 on a line naming a LINK; 250 on a line naming SRP or the drain.
  - Scope: section 13, FR_NFR 3.4.1, every tracked README, and every tracked C, C++, header, Python, SystemVerilog and workflow file.
  - 64 hits: 36 historical, and 28 another quantity (725 Mb/s, a test's clock step, a byte offset, owed-row milliseconds). None is current with an old value. 0.515, 0.511 and a LINK at 150 have no hit.
- **This body:** section 7 said "Nothing under `sw/` changed after `a47cd3f2`". That now reads "In round 12", since round 13's `c274b9f5` changed `ctrl_loop.h`.

### 14.2 The build-of-one comment (R837-7-R1, `b25530f6`)

`ctrl_loop.h:321-323` now says "and 69,635 under #894's SET_CONFIGURATION cut, measured at fe0cef5b, the same build moved by the cut's code". No token changes (14.5).

### 14.3 Item 5's clock and reset precondition (R837-7-S1, taken; `b25530f6`)

The proof that an accepted SET_CONFIGURATION cannot complete late holds while the datapath's clock runs and its domain is out of reset. In the product, that is whenever the mailbox's is:
- `cd_milan` is a clock output of the PLL that makes `cd_sys` (`milan_soc.py:282`, `:288`; `cd_sys` at `:265`).
- LiteX, at the revision `litex_pins.txt` pins, gives each clock output's domain the PLL's lock as its reset (`xilinx_common.py:58-60`, `AsyncResetSynchronizer(cd, ~self.locked)`).

So both domains leave and enter reset together. A datapath clock or reset of its own would reopen the late path. Section 13 says so where it states item 5 (*The final pass's restatements*). `receipts/item5-no-late-completion.md` adds it as the chain's precondition.

### 14.4 The docstring residue (R838-7-R1, `867faf1e`)

`edit_rows.py:3` now names "its SET_CONFIGURATION ruling, item 3", not the comment ID. The docstring is rewrapped within its nine lines, so no cited line moves.

### 14.5 Proof instead of reruns (item 4)

No leg and no sweep ran. Each comparison is against `234bc149`:
- **Images:** 332 of 332 image files are byte-identical at `b25530f6` and at `867faf1e`, built on one clone path.
  - They are the size fixture and the target platform at 1x1/1if, 1x1/2if, 8x8/1if and 8x8/2if: 8 ELFs, 8 binaries and 316 objects.
  - They also match round 13's `c274b9f5` table.
  - Receipts: `receipts/identity/image-compare.txt` and `image-sha256-*.txt`.
- **Harness ELFs:** each harness leg's firmware was linked again at each head, on one clone path.
  - Each link used the leg's own build parameters and flash map, through `build.firmware` alone: no SoC, no simulation.
  - The legs are arm A, E1, C-R1 and the eleven H- legs: 14 legs, 10 distinct ELFs.
  - All 14 are identical at both heads, and equal to round 13's own leg builds (`receipts/identity/harness-elf-sha256.txt`).
- **Sources** (`receipts/identity/tokens-and-ast.txt`):
  - `ctrl_loop.h`'s token stream (`gcc -fpreprocessed -dD -E -P`) is identical, at 516 lines.
  - `poll_grade.py`'s AST is identical, positions included.
  - `edit_rows.py`'s AST is identical but for the module docstring, which differs only by the phrase R838-7-R1 names. Nothing reads it.
  - The other three files are Markdown.

So round 13's measurements, rows, load, pace, slice rule, campaigns and sweep carry to `867faf1e` unchanged.

### 14.6 The documentation gates on a clean clone of `867faf1e`

28 commands, each rc 0, with one log each (`receipts/gates/SUMMARY.txt`):
- `docs_check.py`;
- `check_em_dash.py` from `66adb9a9`, from `cec88385` (the merge base with `dev-soft-core`) and from `234bc149`;
- `check_doc_style.py` and `check_gptp_docs.py`, each with its self-test;
- `DOC_MAP.gen.py --check`;
- `check_cpp_idiom.py` and `check_py_idiom.py`, each with its self-test;
- `git diff --check 234bc149 HEAD`;
- the solution, submodule, feature-status, TODO-ownership, hygiene, doc-path and archive gates, each with its self-test;
- the stale-figure grep.

## Findings

| Finding | Resolution | file:line | Verification |
|---|---|---|---|
| Ruling 6883864236: arm B's SET_CONFIGURATION record 33,724 cycles at 1x1/1if (355 by the rule) and 78,332 at 8x8/2if, which no stated cost covers | Attributed (item 1). Cut once (`f275b619`): one GSI word a stream for the running check, and stream entries only on a moved index. That gives 28,509 (300) and 55,377 (585). Still over 235, so it is paced (`fe0cef5b`) and the paced class is the dearer member (`e4d80a8a`): 300 at 1x1/1if, 595 at 8x8/2if | `aecp_commands.c:100`, `:125`, `:196`, `:198`, `:214`; `aecp_face.c:119`, `:169`; `aecp.h:106`, `:170`; `edit_rows.py:38`, `:41` | arm B in the final pass: 28,376 (300 of 300) and 56,474 (595 of 595) held as paced by `record_classes.py`; 4 new tests and 1 for the pace; 13 rows caught by name; AECP campaign 299 of 299 |
| Ruling item 3: a planted control charging an unpaced SET_CONFIGURATION as ordinary must fail by name | Model: the class at the edits' record alone is refused by name (`an accepted SET_CONFIGURATION charged below its record`) and shortens ACMP's row. Pass check: a SET_CONFIGURATION followed within the pace is held as ordinary and refused (`SET_CONFIGURATION not paced`) | `edit_rows.py:43`, `:86`; `record_classes.py:257` | `rows_tiers.py --selftest`: the control refused; `record_classes.py --selftest` 11 of 11 |
| Ruling item 4: the completion tick against `event.TICK` | Arm B never waits; the window's only TICK precedes the command: 2,159 (25) and 2,404 (30), within 50 and 40, so the completion restates nothing. (The TICK is restated at 55 us on arm A's `backlog-adp` groups at the final firmware: below.) The late-acknowledgement completion is staged by no arm (open) | `receipts/attribution/tickwin-*.txt` | the traced passes after the record (`tree-b1-poll.txt`, `tree-b1-deliver.txt`, `tree-b8-*.txt`) |
| Ruling item 5: hold arm B's SET_CONFIGURATION and SET_STREAM_INFO, and refuse a pass lacking them | Held by class; a pass whose 1x1/1if answering-ports leg ran no accepted SET_CONFIGURATION or no SET_STREAM_INFO is refused; planted controls for each | `record_classes.py:49`, `:134`, `:189`, `:255` | `record_classes.py --selftest` 11 of 11; over every leg RESULT PASS |
| R837-6-F1 (MINOR): the 1x1/1if stated-table survey read only arm A legs | The answering-every-port arm run whole at 1x1/1if (16 groups), and every stated table compared by the rule over it, arm A and arm B, each line with its leg prefix. It found AECP's timer slot over (6,206, 70 > 65), and arm A found a LINK (155 > 150), a build of one (735 > 725) and, at the final firmware, a TICK (55 > 50). All four restated; rows, the pace and the slice rule rerun: the last queued notice 132.71 > 130 at 900 us and the slice rule chose 950: round 12's STOP. Round 13 takes the rule's choice, and at 950 every row holds (the last queued notice 127.21) | `load_grade.py:138`, `:174`, `:177`; `rows_grade.py:93`; `ctrl_loop.h:326`; `poll_grade.py:90` | round 12's compare (`A1/`, `A2/`, `E1/`, `B1F/`); round 13's `receipts/compare/compare-1x1.txt` (`A1/` to `A4/`, `E1/`, `B1F/`) and `compare-8x8.txt`; `receipts/model/flip-1x1-ed0df35b.txt` (exit 0), `tier-grid-1x1-ed0df35b.txt` |
| R838-6-F1 (MINOR), R837-6-R2: "the cut adds 220 B of rom to every image" | Replaced by each image's growth against `7398ec0a`: +224 B in each 1x1 image, +208 B in each 8x8 image. Round 12's growth is stated the same way: +216 B, and +224 in the 1x1/1if size fixture | `SPLIT_CONTROL_MEMORY.md:2480`, its new subsection's images bullet | `receipts/images/rom-per-image.txt` (8 images at `7398ec0a`, `9606b3a9`, `fe0cef5b`) |
| R838-6-F2 (MINOR): section 13's current R4 12.85 and the validation example's load were the previous head's | Section 13's current rows table, its rows-history row, its current summary (R4 13.10, the last queued notice 127.21 within 130 at the rule's 950 us slice; the 900 us figures, R4 13.05 and 132.71 over 130, are its history row and round 12's stop) and its load (0.516 and 0.512), and FR_NFR 3.4.1, are the head's; so are this body's examples | `SPLIT_CONTROL_MEMORY.md:2346`, `:2370`, `:2524`; `FR_NFR.md:383`; [How to validate](#how-to-validate) | `flip_grade.py --check --point 1x1/1if` and `load_grade.py --check` at the head (`receipts/model/*-3909588f.txt`) |
| R838-6-R1, R837-6-R1 (RESIDUE): round and lane names in new source comments | Reworded with the issue, the cut and the measured commits; numbers and behaviour unchanged; none in the new comments | `edit_rows.py:3`, `:29`; `record_classes.py:4`, `:84`; `load_grade.py:126`, `:130`; `poll_grade.py:86`, `:89`; `gtest/README.md:319` | `git diff 9606b3a9 30a01422`: comment lines only |
| R838-6-R2, R837-5-R1 (RESIDUE): "The margins at this head" and "at this head" on round 30's figures | "The margins in round 30's measurements", and "at this head" dropped | `SPLIT_CONTROL_MEMORY.md:2506`, `:2484` | the text |
| R838-6-R3 (RESIDUE): "none changes a compiled firmware file" | This body states that none of the later commits changes the compiled firmware output, as the image and object identity receipts show | this body | `receipts/images/image-sha256-*.txt` |
| R837-6-S1 (SUGGESTION): the packet index was generated before sanitizing | Taken: receipts are sanitized, then indexed, and every row is read back; a mismatch fails the indexer | `scripts/index.py` (the packet) | `INDEX.md`, generated last |
| R837-6-S2 (SUGGESTION): a record named by a later record's response | Taken: a record takes the first response before the next record starts, else it is unanswered. A synthetic control escapes under the old naming and is refused under the new | `record_classes.py:102` | `receipts/model/record-classes-naming-control.txt` |
| #894 issuecomment-6886633874 (from #895 issuecomment-6886630886 item 8): `CTRL_LOOP_SRP_UNIT_US` stated 250 us at 1x1/1if where the load gate states an SRP record at 280, so the SRP drain (`ctrl_loop.c:322`) could start a 280 us record with 250 us left | The constant is the load gate's `record.srp` at each point, the dearer column's, 280 and 365 us (`1c0ca94b`); `load_grade.py --check` refuses any other figure by name, with a planted control at each point (`a47cd3f2`, the controls in a function of their own within the long-function ratchet) | `ctrl_loop.h:282`; `load_grade.py:262`, `:266`, `:563` | `load_grade.py --check` at 250: `1x1/1if: ctrl_loop.h states CTRL_LOOP_SRP_UNIT_US 250 us, not the load gate's record.srp 280 us`; `--selftest` 26 of 26; the loop arm 51 tests (L23 holds the limit at 280); the one-interface legs measured again at `a47cd3f2`; two-interface images byte-identical |
| New: the TICK at the final firmware, 4,784 cycles in arm A's `backlog-adp@program-0`, 55 us by the rule, over 50 (4,692 on the drain's earlier figure) | Restated at 55 us, both columns (`3909588f`) | `load_grade.py:138`, `:174` | `receipts/final2/compare/compare-1x1-at-a47cd3f2-statements.txt` |
| New: `aecp_mutants.py` over the long-module limit once the rows were added (`check_py_idiom.py`: long module 11 > 10 at `fe0cef5b`) | The rows moved to their own table, `aecp_configuration_mutants.py` (`1c8c071b`) | `aecp_mutants.py:936` | `check_py_idiom.py` rc 0 |
| New: round 11's `face-write-after-response` plant, anchored on the line the cut changed, escaped on a build refusal (`every` unused) | Its replacement keeps `every` referenced, so the build compiles and the named test fails | `aecp_mutants.py:578` | the row caught by name; campaign 299 of 299 |
| Ruling 6888782796 item 1: the built one-interface slice is the slice rule's choice within 650 to 1,100 us, 950 us now, its own commit, with `ctrl_loop.h` stating the rule | `CTRL_LOOP_SLICE_US` 950 us at one interface (`c274b9f5`). The header states the rule. The self-tests hold the slice to `rows_tiers.ruled`, and their two anchors on the literal `900u` now read the header. `CTRL_LOOP_BUILD_MOST` stays 1 (950 < 1,010) | `ctrl_loop.h:279`; `rows_tiers.py:879`; `selftest_round.py:109` | `rows_tiers.py --selftest` 1,033 of 1,033 (the control "the built design's slice not the rule's" refused); the round checks 10 of 10; `tier_grid.py` chooses the built design; `flip_grade.py --check --point 1x1/1if` exit 0 |
| Ruling item 3: rerun every one-interface leg on the rebuilt images, the compare, the pace and slice rules, the firmware jobs and the sweep, and every gate on a clean clone of the final head | Done ([13.2](#132-the-reruns-on-the-rebuilt-images-item-3), [How to validate](#how-to-validate)). Nothing is over by the rule but the class lines, so nothing is restated, and the rule's choice does not move | `receipts/compare/compare-1x1.txt` | arm A 96 groups, 0 refusals; every stated table within; the pace 8 ms; the slice rule 950 = built |
| Ruling item 4: carry the 8x8/2if legs only by the two-interface images' byte identity, shown by hash | Shown, and the legs were also run again: 6 of 6 harness ELFs identical to round 12's, and 166 of 166 two-interface image files identical across `30a01422` and `c274b9f5` | `receipts/images/harness-elf-sha256.txt`, `image-sha256-*.txt` | the hashes |
| Ruling item 5: stage a late-acknowledged SET_CONFIGURATION's completion at each point, or show from the product port that it cannot complete late | Shown: the product datapath takes a commit on its crossing's pulse with no backpressure and acknowledges it within the contract's 64 cycles. The split composition measures 2 polls. The firmware outwaits the bound, so no interface is ever owed and no change waits ([13.4](#134-a-late-acknowledged-set_configurations-completion-item-5-it-cannot-happen-on-the-product-port)) | `KL_mbx_cdc.sv:272`, `:274`, `:278`; `mbx.c:346`; `aecp_face.c:97`; `aecp.c:489`; `sim_split.cpp:371` | `receipts/item5-no-late-completion.md`; the sweep's `milan_dp` suite at `ed0df35b`: `[FACE] commit to BUSY clear: 2 polls` |
| Ruling item 6: 8x8/2if stays reported, its figures to the 8x8 lane and #890 | Reported in [Status](#status); unchanged by round 13 | `flip_grade.py` | `receipts/model/flip-8x8-ed0df35b.txt` (exit 1, the reported point) |
| New: lane part a's `hooks_selftest` refused `ed0df35b` (27 of 28): the hooks harness's face plant anchored on the publication line round 12's cut rewrote | The plant anchors on the new line, and its replacement keeps the stream flag referenced, as the AECP campaign's row does (`234bc149`) | `tb/verilator/ctrl_service_hooks/hooks.py:204` | `hooks_selftest` at `234bc149`: 28 of 28, 96 of 96 mutants caught; no workflow job or sweep suite reads the file |
| R837-7-F1 (MINOR, Docs): current-tense figures left stale by the round-12 and round-13 moves | Every site the grep finds is the head's figure or stated as history (14.1). This body's two sites were corrected before round 14 and are kept | `SPLIT_CONTROL_MEMORY.md:2197`, `:2342`, `:2373`, `:2380`, `:2443` to `:2445`, `:2459`, `:2467`, `:2477`, `:2479`, `:2480`, `:2489`, `:2509`; `FR_NFR.md:383`; `srp/README.md:238`; `poll_grade.py:70` | `receipts/stale-figures-grep.txt`: 64 hits, 36 historical, 28 another quantity, 0 current with an old value. The checks that give the head's figures read inputs identical to `234bc149`'s (14.5) |
| R837-7-R1 (RESIDUE): `ctrl_loop.h:322` attributes the cut to the pace commit | Reworded as the review gives it | `ctrl_loop.h:321` | token stream identical (`receipts/identity/tokens-and-ast.txt`) |
| R837-7-S1 (SUGGESTION): item 5's clock and reset precondition is implicit | Taken (14.3) | section 13, *The final pass's restatements*; `receipts/item5-no-late-completion.md` | `milan_soc.py:265`, `:282`, `:288`; LiteX `xilinx_common.py:58-60` at the pinned revision |
| R837-7-S2 (SUGGESTION): an unanswered over-cost record in arm B's `aecp-fanout` is reported, not held | Not taken: round 14 changes no executable file. The pace holds the record after an accepted SET_CONFIGURATION for 8 ms, so its answer commits first, and no published span shows the case. Listed under Known limitations | `record_classes.py:134` | none |
| R837-7-S3 (SUGGESTION): the archive's path redaction leaves script rows off their INDEX hashes | Taken: no file in round 14's packet carries a host path, scripts included, so nothing needs redacting. INDEX.md states that the outer manifest is authoritative for an earlier packet's redacted scripts | `scripts/index.py`, `scripts/sanitize.py` (the packet) | `index.py` refuses any file carrying a host path |
| R838-7-F1 (MINOR, Tests and Docs): this body's load and the R838-6-F2 row's summary | Corrected before round 14 (R838-8, POSITIVE) and kept | this body, section 8 and the R838-6-F2 row | R838-8 |
| R838-7-R1 (RESIDUE): `edit_rows.py:3` names an issue-comment ID | Reworded as the review gives it (`867faf1e`) | `edit_rows.py:3` | AST identical but for the docstring (`receipts/identity/tokens-and-ast.txt`) |
| R838-8-S1 (SUGGESTION): the R838-6-F2 row's receipt label | Not taken: that row is kept as corrected, and its commands are exact-head | the R838-6-F2 row | none |
## Authoritative references

- #894's round-12 ruling, issuecomment-6883864236, and the round-13 ruling on its STOP, issuecomment-6888782796.
- Round 11's authority, which stands: issuecomment-6878230332, its amendment issuecomment-6878532871 (the class split), issuecomment-6876349104, and the measurement issuecomment-6878200592.
- The bounds: issuecomment-6858269025, issuecomment-6862465874 and issuecomment-6867990126 (49 ms, 238 ms, 181 to 239 ms). The last queued notice's bound is 130 ms.
- The direct-index ruling, issuecomment-6870437042. The every-table instruction, issuecomment-6881287231.
- The round-11 delta reviews: R837-6 (PR #902 issuecomment-6884063444) and R838-6 (issuecomment-6884009601).
- Round 13's delta reviews: R837-7 (PR #902 issuecomment-6890948441), R838-7 (issuecomment-6890766701) and R838-8 (issuecomment-6890858159).
- Milan v1.2 5.4.2.5 (SET_CONFIGURATION refused while any Stream Input is bound or any Stream Output is streaming) and 5.4.5.2.
- IEEE 1722.1-2021 7.4.7 (SET_CONFIGURATION), 7.4.15 (SET_STREAM_INFO), 7.5.2 and 9.3.2.6.
- `docs/reference/FR_NFR.md` 3.4.1 and `docs/design/SPLIT_CONTROL_MEMORY.md` section 13.

## How to get into the same state

```sh
git fetch origin
git checkout 894-tiers
git rev-parse --short=8 HEAD   # 867faf1e
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if    # exit 0, every row held
python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if             # 10 of 420 hold; the built 950 us chosen
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check                    # 0.516 and 0.512, PASS
python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --selftest                 # 1033 of 1033 refused
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest                 # 585 of 585 refused
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest                 # 26 of 26 refused
python3 -B tb/verilator/ctrl_service_budget/record_classes.py --selftest             # 11 of 11 refused
python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test                        # 28 of 28; 96 of 96 mutants caught
python3 -B sw/firmware/ctrl/test/aecp_mutants.py --output "$(mktemp -d)" --shard 286 299   # one of the 13 new rows (286 to 298)
python3 -I tb/verilator/ctrl_service_budget/record_classes.py B/results ...          # over a pass's legs: RESULT PASS
git diff --stat 234bc149 867faf1e    # round 14: three Markdown files, ctrl_loop.h, poll_grade.py, edit_rows.py
```

The final pass, gate by gate. Commands ran on clean clones and never through a pipe; receipts are under `receipts/`. The final head is `867faf1e`. Round 14's two commits change Markdown, two comments and a docstring, and every image file and harness ELF is byte-identical to `234bc149`'s (14.5), so round 13's pass below carries to it. Round 13's own pass was at `234bc149`. After `ed0df35b` it changes only `tb/verilator/ctrl_service_hooks/hooks.py`, which no workflow job and no sweep suite reads: its one reader is lane part a's `hooks_selftest`, which ran at the final head. After `c274b9f5` only five Markdown files changed before it, so the legs' firmware and graders are the head's.

| Gate | Head | Result |
|---|---|---|
| Full arm A at 1x1/1if (every group, four parts of 24 on one build) | `c274b9f5` | 96 groups, 0 refusals. 7 misses (`backlog-owed`'s held-egress rows, ruling 6871343905 (a)). 0 of 140,032 passes over THE SHARE. Joins 187.994 to 190.021 ms. |
| The answering-every-port arm at 1x1/1if, all 16 groups | `c274b9f5` | rc 0 |
| The answering-ports leg and C-R1 at 1x1/1if; the 8x8/1if legs | `c274b9f5` | 2 exit 0. H-81L, H-81A, H-81N and H-J81 exit 1 on round 11's reasons (that point states one interface's costs). |
| The 8x8/2if legs (B8F, L8A, L8N, L8L, L8O, J8) | `c274b9f5` (images identical to round 12's) | 5 exit 0; J8 exits 1 on #910's build of one |
| Joins over every leg | `c274b9f5` | 185.486 to 190.147 ms |
| `record_classes.py` over every leg | `ed0df35b` | RESULT PASS |
| Every stated table by the rule, both points | `ed0df35b` | 1x1/1if: the class lines only. 8x8/2if: #910's build of one and the class lines. |
| Images: 332 files, and the harness legs' ELFs | `30a01422`, `c274b9f5` | the 166 two-interface files and the 6 8x8/2if harness ELFs identical; the one-interface ones differ in `ctrl_loop.o` alone, at equal sizes |
| Lane gates, part a (48) | `234bc149` | rc 0 but the four that exit 1 by design (`rows_tiers --terms`, `flip --check`, `--point 1x1/1if --design as-built`, `--point 8x8/2if`). The harness self-test has 0 failures, the hooks self-test 28 of 28, and the model's self-tests 1,033, 585, 26 and 11 of as many. |
| Lane gates, parts b and c (`test_builder`; `nvm_selftest`, `boot_1x1`, `boot_8x8`, `boot_native`, `boot_plants`) | `ed0df35b` | rc 0 |
| Every workflow step (`verify_wf.py`, `rtl-fast.yml`, `rtl.yml`, `elaborate.yml`, `docs.yml`; the yosys shards 0-4 to 3-4) | `ed0df35b` and `234bc149` | 139 ran rc 0, 226 not run with a reason, 0 bad. rtl-fast's other jobs, firmware-boundary and the docs jobs ran at `234bc149`; the firmware, RTL and elaborate jobs at `ed0df35b`. |
| The AECP, control and SRP campaigns; firmware-unit with `fw_coverage.py --check` | `ed0df35b` | AECP 299 of 299, control 716 of 716, SRP rc 0; coverage PASS (39 files) |
| The four-shard Verilator sweep, each shard on its own picked range (0-7, 8-15, 16-23, 24-31) | `ed0df35b` | each shard's command rc 0 (4,019, 3,856, 4,321 and 3,396 s); `milan_dp`'s `[FACE] commit to BUSY clear: 2 polls` |
| `docs_check.py`, `check_em_dash.py`, both idiom gates | `234bc149` | 0 findings; rc 0 |
| Round 14: 332 image files and the 14 harness legs' ELFs against `234bc149` | `b25530f6`, `867faf1e` | 0 of 332 differ; 14 of 14 ELFs identical |
| Round 14: the documentation and idiom gates (28 commands, 14.6) | `867faf1e` | rc 0 |

None of the commits after `c274b9f5` changes the compiled firmware output, as the image and object identity receipts show, round 14's included.

## Known limitations / out of scope

- **A late-acknowledged SET_CONFIGURATION's completion is unreachable on the product port** ([13.4](#134-a-late-acknowledged-set_configurations-completion-item-5-it-cannot-happen-on-the-product-port)), so no arm stages it. An SoC with no datapath, the CPU harnesses' own build, holds the acknowledgement idle, and every change waits there as the contract defines. That is a fixture, not the product.
- **Item 5's proof rests on one clock and reset precondition** (14.3): the datapath's domain is a clock output of the sys PLL, and its reset is that PLL's lock. A datapath clock or reset of its own would reopen the late path.
- **An unanswered over-cost record in arm B's `aecp-fanout` is reported, not held** (R837-7-S2). The pace holds the record after an accepted SET_CONFIGURATION for 8 ms, so its answer commits first, and no published span shows the case. Holding or refusing it needs an executable change, which round 14 does not make.
- **The product's running check reads one window word a stream.** The answering-ports arm cannot measure it, since its stream port answers without a read.
- **8x8/2if stays reported**, no flip row; its paced class is 595 us. Its figures for #894's 8x8 lane and #890 are in [Status](#status).
- **8x8-1if's legs exit 1 as in rounds 9 to 12** (that point states one interface's costs; the 40-notice model), and so does the 8x8 `srp` leg, on #910's build of one.
- **The tier model's load does not split the paced records.** At 300 against 235 and one paced record a pace, it adds about 0.008 at 1x1/1if.
- **`dispatch-build/` is still left untracked** by the firmware campaigns' shard-dispatch self-test (issuecomment-6881004362), not changed here.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (round 12's items 1 to 6; round 13's items 1 to 6; round 14's items 1 to 5)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (How to validate)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
