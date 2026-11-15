[A773]

## Contents

- **[Status](#status)**: the head of rounds 12 to 18, SET_CONFIGURATION's record cut and paced, the slice at the rule's choice, and `894-tiers` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: #894, #904 and #908, with the executor and reviewers.
- **[Description](#description)**: round 12's items in the ruling's order and the round-11 delta reviews' findings, then round 13's.
- **[Round 13](#round-13)**: the slice at the rule's choice, the reruns, the carries and the late-acknowledgement proof.
- **[Round 14](#round-14)**: every cost, slice and load figure the round-12 and round-13 moves touched, stated as the head's or as history; item 5's precondition; the identity proof.
- **[Round 15](#round-15)**: every superseded 1x1/1if row figure, stated as history or beside the head's; round 14's residues.
- **[Round 16](#round-16)**: THE PACE's comment, the two-interface `CTRL_LOOP_TX_MS` at 99 ms and its planted control, and every statement check at both points.
- **[Round 17](#round-17)**: the pre-tiers JoinTime product at `:2004` stated as history, and the statement-figure sweep.
- **[Round 18](#round-18)**: the queued-notice table and `EDIT_RECORD_US` at the head's figures, and the mechanical sweep over every moved constant and every row.
- **[Findings](#findings)**: every finding this round answers, each with its resolution, file:line and verification.
- **[Authoritative references](#authoritative-references)**: the rulings and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the commands to check out the branch.
- **[How to validate](#how-to-validate)**: the reviewer's commands, their expected results, and the final pass gate by gate.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what this round leaves open.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

**REVIEW READY at 1x1/1if.** Head `4ae887a1`: twenty-three commits on round 11's `9606b3a9`, rounds 12 to 18. `894-tiers` -> `dev-soft-core`.

- **Round 12** (#894 issuecomment-6883864236): it cut the answering-ports arm's SET_CONFIGURATION record and paced it, and charged the paced class at the dearer member's record. It held the SRP drain's record cost to the load gate's (issuecomment-6886633874). It restated four 1x1/1if costs its final pass measured over their statements. With those, the last queued notice was over its bound at the 900 us slice, and the slice rule chose 950 us: a STOP (issuecomment-6888749411).
- **Round 13** (the ruling on it, issuecomment-6888782796): the built one-interface slice is the slice rule's choice, 950 us. `ctrl_loop.h` states the rule and the self-tests hold it. Every one-interface leg was measured again on the rebuilt images; every stated table holds there by the rule but for the class lines, so nothing more is restated. A late-acknowledged SET_CONFIGURATION is shown not to complete late on the product port.
- **Round 14** (round 13's delta reviews: R837-7 and R838-7 NEGATIVE, each on one MINOR; R838-8 POSITIVE): documents, two comments and a docstring only. Every cost, slice and load figure the round-12 and round-13 moves touched is the head's or stated as history. Item 5's clock and reset precondition is stated. Every image file and harness ELF is byte-identical to `234bc149`'s, so round 13's measurements carry unchanged.
- **Round 15** (round 14's delta reviews: R837-8 NEGATIVE on one MINOR, R838-9 POSITIVE): two Markdown files only. Every superseded 1x1/1if row figure its tokens held (the rows-history table's cells: R4, R4L, ACMP, ADP, MAAP, the first and last queued notice, R5, R6, tx, txL, and the load) is stated as history or beside the head's. Those tokens missed the queued-notice table's figures, which round 18 found (18.1). Nothing compiled or executed changed, so round 13's measurements carry unchanged.
- **Round 16** (round 15's delta review, R837-9: NEGATIVE on two MINORs): `aecp_mbx.h`'s comment gives the direct index's txL at 7 ms as history. `CTRL_LOOP_TX_MS` states 99 ms at two interfaces, over the tx row's 98.49 there, and the self-tests plant each interface count's statement under its row. Every statement check holds at both points but 8x8/2if's reported rows. Every image file and harness ELF is byte-identical to `234bc149`'s, so round 13's measurements carry unchanged.
- **Round 17** (round 16's delta review, R837-10: NEGATIVE on one MINOR): one Markdown file. Section 13's `:2004` states the pre-tiers 176 ms JoinTime product as history and says what governs under THE TIERS. A sweep of the superseded figures of the constants it named, with their derived products and clause-citing sentences, found four more present-tense sites, now history. It named no `EDIT_RECORD_US`, which round 18 found (18.2). Nothing compiled or executed changed.
- **Round 18** (round 17's delta review, R837-11: NEGATIVE on three MINORs): one Markdown file. Section 13's queued-notice table gives the head's rows and the amendment's 130 ms, and `EDIT_RECORD_US` the paced class's 300 and 595 us. The sweep is now mechanical: superseded values come from the history of every stated constant over the PR's commits, and from every row figure that is not the head's. Every hit is classified, and none states a superseded figure as current (18.3). Nothing compiled or executed changed.

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

**For #894's 8x8 lane and #890** (8x8/2if, reported, no flip row): R4 44.24, R5 206.45, R6 196.31, the first queued notice 20.93, the last 806.60, R4L 195.76, ACMP 67.94, ADP 68.08, MAAP 69.13, tx 98.49 and txL 459.40 ms. The load is 0.794 at the pin and 0.754 in the second column, and the paced class is 595 us. The two-interface images are unchanged by round 13 and every later round. Round 16 restates the two-interface `CTRL_LOOP_TX_MS` at 99 ms, over the tx row's 98.49 (it was 98, under the row since `e4d80a8a`).

## Linked Issue / roles

Relates to #894
Relates to #904
Relates to #908

Executor: `[A773]`
Internal cleared-context reviewer: `[R837]`
External reviewer: `[R838]`

## Description

Round 12 follows #894's ruling issuecomment-6883864236. Round 11's cut, its class split (paced edits at 260 us at 1x1/1if and 325 at 8x8/2if, every other AECP record at 235) and its TICK stood at round 12's start (its TICK restated to 55 us by the final pass, below). The defect: the answering-ports arm's `aecp-fanout` SET_CONFIGURATION record, 33,724 CPU cycles at 1x1/1if (355 us by the rule) and 78,332 at 8x8/2if, which no stated cost covered. The product's ports answer as that arm's do, so the path is the product's.

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

### 14.1 The cost, slice and load figures the round-12 and round-13 moves touched (R837-7-F1, `b25530f6`)

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

Every row moved too. Round 14's tokens were the figures above, and held no row figure, so two present-tense row sites stayed; round 15 swept the rows (15.1). Each current-tense site of the figures above gives the head's figure, or says that the figure was then.

- **`SPLIT_CONTROL_MEMORY.md` section 13:**
  - `:2197`: a build of one is stated at 735 us at 1x1/1if.
  - `:2342`: the rule picked 900 us then. At the costs restated under the SET_CONFIGURATION cut it picks 950 us, and a 950 us slice holds one MRPDU's build. The 8x8/1if sentence gives 735 us now.
  - `:2373`, `:2443` to `:2445`, `:2459`, `:2467`, `:2477` and `:2509` are past tense. `:2443`, `:2444` and `:2509` give the head's figure beside the old one: 950 us since #894's ruling of 2026-11-15, 735 us since the cut, and the rows at 950 us.
  - `:2380`: at the head the pace finds 8 ms, txL 48.43 ms and R4L 188.48 ms (48.09 and 188.39 then). The load is 0.516 at the pin, and 0.695 with every command the largest legal one.
  - `:2479`, `:2480` and `:2489`: the TICK was stated at 50 us then, and is 55 since the SRP drain's record cost moved. The tx row's 33.01 ms is history beside the head's 33.38 ms.
- **`FR_NFR.md:383`:** "8 ms then held txL, 48.23 ms".
- **`sw/firmware/ctrl/srp/README.md:238`:** 33.38 ms at the 950 us slice. As history: 33.01 at 900 us under the one-row edit cut, and 29.78 before it.
- **`poll_grade.py:70`** (found by the sweep; a comment only): a retained record's retry is stated at the SRP record's cost, 280 and 365 us. It said 250 and 365.
- **The grep receipt** (`receipts/stale-figures-grep.txt`, generated again on the clean clone at `867faf1e`):
  - Tokens: 725, 33.01, 900 us, 0.515, 0.511, 13.05 and 132.71; 50 on a line naming a TICK; 65 on a line naming AECP, a timer or a slot; 150 on a line naming a LINK; 250 on a line naming SRP or the drain.
  - Scope: section 13, FR_NFR 3.4.1, every tracked README, and every tracked C, C++, header, Python, SystemVerilog and workflow file.
  - 64 hits: 36 historical, and 28 another quantity (725 Mb/s, a test's clock step, a byte offset, owed-row milliseconds). None of those hits is current with an old value. 0.515, 0.511 and a LINK at 150 have no hit.
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

## Round 15

Round 15 answers round 14's delta reviews:
- R837-8 (PR #902 issuecomment-6891424100): NEGATIVE, on one MINOR;
- R838-9 (issuecomment-6891425121): POSITIVE.

It changes two Markdown files (`6b759b30`) and this body. No file under `sw/`, `tb/`, `hw/`, `syn/` or `scripts/` changes. Its receipts are in its own packet.

### 15.1 Every superseded 1x1/1if row figure (R837-8-F1, `6b759b30`)

- **The two sites the review names:**
  - `FR_NFR.md:383` now reads "8 ms held it, txL 48.09 ms and R4L 188.39 ms". Where the line states the head, it reads "there 8 ms holds txL, 48.43 ms, and R4L, 188.48 ms". The SRP drain's clause is past tense too ("was the load gate's 280 us").
  - `SPLIT_CONTROL_MEMORY.md:2467` now reads "Then txL was 49.69 ms at 7 ms, and 8 ms was the smallest pace that held: txL 48.09 ms within 49 and R4L 188.39 within 238 (`AECP_PACE_MS`; 48.43 and 188.48 at the head)". Its measurement and 8x8/2if's rows are past tense too.
- **Further sites the sweep found,** with tokens from every earlier row, not only the last four:
  - `:2351`: the tx row at the merge's costs gives the head's beside it, 33.38 and 98.49 ms.
  - `:2380`: at the merged costs no pace "held" txL, and with ACMP's item itemised none "did".
  - `:2402`: at lever (a)'s costs txL "was" 46.58 ms, the load "was" 0.499, and 8x8/1if's load "was" 0.696.
  - `:2466`: the 64-slot case is a counterfactual and now reads as one: "that would be 1,040 us, which would move the pace to 9 ms and the load to 0.705".
  - `FR_NFR.md:387`: the last queued notice's row "was 125.84 ms (127.21 at the head)".
- **The grep receipt** (`receipts/stale-rows-grep.txt`, made by `scripts/stale_rows.py` and `scripts/stale_rows_classify.py`, which exits 1 on any hit it does not classify):
  - **Tokens, by construction** (R837-8-S1). The row tokens are every figure of every row of section 13's rows-history table before the head's row, less any equal to the head's figure in its column: R4, R4L, ACMP, ADP, MAAP, the first and last queued notice, R5, R6, tx and txL. The load tokens are every load figure on a line naming the load in section 13, FR_NFR 3.4.1 or this body, less the head's and the ceilings. The list is at the top of the receipt.
  - **Scope:** section 13, FR_NFR 3.4.1, MAILBOX_SPLIT, every tracked README and every tracked C, C++, header, Python and SystemVerilog file, outside table lines; and this body, every line, its tables included.
  - **Result:** 141 hits: 96 historical, 30 beside the head's figure, and 15 another quantity (another point, a counterfactual, a self-test's number). None of those hits states a superseded figure as current. The tokens missed the queued-notice table's figures (18.1).
- **Round 14's cost-token grep,** run again at `6b759b30`, classifies every hit as before (`receipts/stale-figures-grep.txt`).

### 15.2 Round 14's residues

- **R837-8-R1 and R838-9-R1:** the R838-6-F2 row cites `:2525`, the current summary (R4 13.10).
- **R837-8-R2:** `:2509` now reads "Every other 1x1/1if row held by every source, the load was 0.516 and 0.512, and the pace stayed 8 ms". "Only the one-interface images changed" is past tense too.
- **R837-8-R3:** 14.1 now names exactly the sites that give the head's figure beside the old one: `:2443`, `:2444` and `:2509`. Its "Every row moved too" sentence now says that round 14's tokens held no row figure, and that the rows are 15.1's.
- **R838-9's note on item 5's precondition:** the two domains share their reset's cause, not a cycle-identical release. `:2509` now says both are held in reset until the PLL locks and enter it when it loses lock, each released through its own synchronizer.

### 15.3 Proof

- `git diff --name-only 867faf1e 6b759b30` lists `docs/design/SPLIT_CONTROL_MEMORY.md` and `docs/reference/FR_NFR.md`, and nothing else. No compiled or executed input changed, so round 14's identity proof (14.5) and round 13's measurements carry to `6b759b30`.
- **The documentation gates** ran on a clean clone of `6b759b30`, with both sweeps: 29 commands, each rc 0 (`receipts/gates/SUMMARY.txt`, one log each).

## Round 16

Round 16 answers round 15's delta review, R837-9 (PR #902 issuecomment-6891685454): NEGATIVE, on two MINORs. It follows the manager's maintainer-delegated ruling: outcome 1 of R837-9-F2, by the stated-cost rule. Two commits: `eed2e40d` (a comment) and `b6f5c638` (one constant, the model's two controls, and the documents). Its receipts are in its own packet.

### 16.1 THE PACE's comment (R837-9-F1, `eed2e40d`)

`aecp_mbx.h:50` now reads "txL was 49.69 ms at 7 ms, and 8 ms did". This is the direct index's figure, as the same clause reads at `SPLIT_CONTROL_MEMORY.md:2467` and `FR_NFR.md:383`. The head's own figures are 52.09 ms at 7 ms and 48.43 at 8. The header's token stream is identical, and its line count is unchanged.

### 16.2 The two-interface TX statement (R837-9-F2, `b6f5c638`)

- **The constant:** `ctrl_loop.h:371` now reads `#define CTRL_LOOP_TX_MS (MBX_N_IF == 1u ? 34u : 99u)`. 99 ms is the 8x8/2if tx row, 98.49 ms, rounded up, as the header's comment states the figure. It had stayed 98 since the row passed it at `e4d80a8a`.
  - The constant is read by one `_Static_assert` (`ctrl_loop.c:203`), which holds 1x1/1if alone, and by the model.
  - No image changes (16.4).
- **The check:** `rows_tiers.tx_statements(root)` returns `[]` at both points (`receipts/statements/model-statements.txt`). At `6b759b30` it returned the 8x8/2if line `CTRL_LOOP_TX_MS states 98 ms, under the built design's tx row 98.49 ms`.
- **The controls:**
  - `rows_tiers.py:932-935` plants both legs under their rows (33 and 98 ms) and requires as many refusals as points. `tx_statements` reports at most one figure line a point, so that is one at each. `rows_tiers.py` stays at its 1,000 lines.
  - `flip_grade.py:174-184` plants each interface count's leg under its row alone (33 at 1x1/1if; 98 at 8x8/2if) and requires the refusal by name at its own point. 8x8/2if's flip check exits 1 by design, so only this control holds that statement.
  - With `tx_statements` made blind to 8x8/2if, both controls escape by name (`receipts/statements/controls-probe.txt`).
  - The self-tests still refuse 1,033 of 1,033 and 585 of 585.
- **The documents:**
  - `:2351` now reads: `CTRL_LOOP_TX_MS` "stated as 30 and 98 ms. At the head it states 34 and 99 ms", with the reason for each.
  - `:2004` and `:2521` gave the pre-tiers 44 ms as current. Both now mark it as before THE TIERS, with the head's statement beside it. `:2521` also put its consequence in the past tense. At `b6f5c638`, `:2004` still stated its derived 176 ms JoinTime product in present tense (R837-10-F1); round 17 makes that history (17.1).
  - The harness README's check description names both points and the planted legs.
- **The flip receipt** (R837-9-S2): at 8x8/2if, `flip_grade.py --check --point 8x8/2if` now lists only rows over their bounds, which are reported by decision. Its one difference from round 13's receipt is that the statement line is gone (`receipts/statements/flip-check-8x8.txt`). The statement checks are published on their own, at both points.

### 16.3 Every statement check at both points (item 4)

All of these ran on a clean clone of `b6f5c638` (`receipts/statements/`):
- **The model's checks** (`scripts/statement_checks.py`, `model-statements.txt`): `[]` at both points, except `rows_tiers.findings` at 8x8/2if, whose rows are reported.
  - `rows_tiers.tx_statements`, `unrowed` and `findings`;
  - `edit_rows.findings`;
  - `queued_bound.statements`;
  - `paced_rows.statements` and `count_findings`;
  - `load_grade.srp_unit` and `findings`.
  - `load_grade.held` holds 1x1/1if at 0.516 and 0.512 against 0.70, and each point's stated table is printed.
- **The CLI checks:**
  - `flip_grade.py --check --point 1x1/1if`: rc 0.
  - `--point 8x8/2if`, and the default over both points: rc 1, on the reported rows alone.
  - `load_grade.py --check`: rc 0.
- **Every stated table against the measured costs,** both points: `compare_point.py` at `b6f5c638`, over round 13's costs from every leg. The image files are byte-identical, so the measurements stand. Its output equals round 13's: the class lines only, and at 8x8/2if #910's build of one.
- **`record_classes.py` over every leg** of round 13, at `b6f5c638`'s statements: RESULT PASS. Its output equals round 13's up to the order of two result-set listing lines, the two `results: 8x8/2if none` lines (R837-10-R1). Every verdict line and the RESULT are identical.

### 16.4 Proof

- **Images:** 332 of 332 image files at `b6f5c638` are byte-identical to `234bc149`'s, on one clone path (`receipts/identity/image-compare.txt`). The objects carry no debug or macro sections, so a macro read only by a `_Static_assert` leaves them unchanged.
- **Harness ELFs:** all 14 harness legs' ELFs, linked again from each leg's own build parameters and flash map, are identical to `234bc149`'s (`receipts/identity/harness-elf-sha256.txt`).
- **Sources** (`receipts/identity/tokens.txt`):
  - `aecp_mbx.h`'s token stream is identical.
  - `ctrl_loop.h`'s differs only by `98u` -> `99u`.

### 16.5 Every comment and docstring under `sw/` and `tb/` (item 4)

`scripts/comment_sweep.py` reads every comment and docstring under `sw/` and `tb/`: C, C++, headers and SystemVerilog; Python comments and docstrings; shell comments; and every Markdown line there. That is 766 files.
- **Tokens** (`receipts/sweep-tokens.txt`, 144): round 15's generated row and load tokens, R837-9's 115 (with 8x8/2if's earlier rows), and txL and R4L at every non-built pace (R837-9-S1). It also takes the cost figures in context: 725 on a build line, 900 us, 65 with AECP's timer slot, 150 with LINK, 250 with the SRP drain, 50 with TICK, and 98, 30 and 44 with `CTRL_LOOP_TX_MS` or THE TRANSMIT.
- **Result** (`receipts/comment-sweep.txt`): 15 hits, 4 historical, 3 beside the head's figure and 8 another quantity. None of those hits is current with a superseded figure.
- **It can fail:** at `6b759b30` the same sweep finds `aecp_mbx.h:50`'s present tense (`receipts/comment-sweep-6b759b30-control.txt`).
- **In the documents,** the nine non-built-pace figures appear only at `:2380`, `:2436`, `:2457` and `:2467`, all past tense. Round 15's row sweep and round 14's cost grep run again at the head (`receipts/stale-rows-grep.txt`, `receipts/stale-figures-grep.txt`).

### 16.6 Gates on a clean clone of `b6f5c638`

35 commands, each rc 0, on a clean clone of `b6f5c638` with 0 changed paths before and after (`receipts/gates/SUMMARY.txt`, one log each):
- **The model self-tests:** `rows_tiers.py --selftest` (1,033 of 1,033), `flip_grade.py --selftest` (585 of 585) and `load_grade.py --selftest` (26 of 26).
- **The firmware unit gate's AECP and loop arms** (`scripts/fw_arms_aecp_loop.py`): the compiled service bounds, the port and event loop, and every AECP arm, as the gate's suites phase runs them. 18 arms, PASS.
- **The documentation and idiom gates,** as in round 15:
  - `docs_check.py`;
  - `check_em_dash.py` from `66adb9a9`, `cec88385` and `6b759b30`;
  - doc style, gPTP docs and `DOC_MAP`;
  - both idiom gates;
  - `git diff --check`;
  - the solution, submodule, feature-status, TODO-ownership, hygiene, doc-path and archive gates, with their self-tests.
- **The sweeps and the probe:** round 14's cost grep (64 hits), round 15's row sweep over this body (141 hits), the comment sweep (15 hits), each with every hit classified, and the controls probe.

## Round 17

Round 17 answers round 16's delta review, R837-10 (PR #902 issuecomment-6892175293): NEGATIVE, on one MINOR. One commit, `478ff78c`, changes `docs/design/SPLIT_CONTROL_MEMORY.md` alone; this body changes too. Its receipts are in its own packet.

### 17.1 The pre-tiers JoinTime product (R837-10-F1)

`:2004` now reads: "every participant's owed MRPDU, one a call, was then within 2 x `MBX_N_IF` x 44 = 176 ms at two interfaces, inside the 200 ms JoinTime (IEEE 802.1Q Table 10-7). Under THE TIERS no such product is claimed: the MRP timer budget, `CTRL_LOOP_TX_BOUND_MS` (49 ms at the head's 19 cs join timer), holds the tx row at 1x1/1if, and at 8x8/2if the rows are reported, not held (#890)." No two-interface JoinTime compliance is claimed.

### 17.2 Every superseded statement figure (R837-10-S2, taken)

- **The sweep** (`scripts/statement_sweep.py`) reads sentence by sentence.
  - **Tokens:** each constant's old value, wherever the sentence names what the constant states:
    - `CTRL_LOOP_TX_MS` 44, 30 and 98;
    - `CTRL_LOOP_TX_BOUND_MS` 40 and 50;
    - the join timer's 20 cs and 200 ms;
    - `CTRL_LOOP_BUILD_ONE_PASS_US` 725 and 430;
    - a TICK's 45 and 50 us, AECP's timer slot's 60 and 65, a LINK's 150, and `CTRL_LOOP_SRP_UNIT_US`'s 250;
    - the slice's 800, 900 and 1,200 us, `AECP_PACE_MS`'s 6 and 7 ms, and the load's 0.515 and 0.511.
  - **Derivations:** every arithmetic derivation (a x b = c, a + b = c) one of those figures enters, and each derived result wherever it appears: 44 from 30 + 7 x 2, and 176 from 2 x `MBX_N_IF` x 44.
  - **Clause flags:** each hit is flagged when its sentence cites a clause or table (IEEE, Milan, 802.1Q, 1722, Table, Clause).
  - **Scope:** section 13, FR_NFR 3.4.1, MAILBOX_SPLIT, every tracked README, every comment and docstring under `sw/` and `tb/`, and this body: every line, tables included.
- **What it found besides `:2004`**, each now history, with the head's figure beside it where one moved:
  - `:2260`: the sources table gave `SRP_JOIN_CS` as 200 ms. It is 190 ms at 19 cs since #908's contingent moves.
  - `:2357`: the built design "at the slice ruling's 800 us" is now "then at ... 800 us (950 us at the head)".
  - `:2377`: "every row held ... and the six rows' rule picked 800 us".
  - `:2442`: THE TRANSMIT's bound "was ... 50 ms (49 ms since `T_egress` is counted)", and "the pace stayed ... then 6 ms (8 ms at the head)".
- **The receipt** (`receipts/statement-sweep.txt`, from `scripts/statement_classify.py`, which exits 1 on any hit it does not classify): 178 hits: 114 historical, 41 beside the head's figure, 17 another quantity, and 6 that name the `milan_dp` defect reported below; 18 sit in a sentence citing a clause. None of those hits states a superseded figure as current. Its tokens named no `EDIT_RECORD_US` (18.2).
- **Round 15's row sweep, round 14's cost grep and round 16's comment sweep** run again at the head, with every hit classified (`receipts/stale-rows-grep.txt`, `stale-figures-grep.txt`, `comment-sweep.txt`).
- **Found and not fixed here** (a harness's code, outside a documents round): `tb/verilator/milan_dp/srptx.hpp:82-83`.
  - The SRP transmit check (#867) mirrors the adapter's JoinTime as `kJoinCs = 20`, and its README (`:1610`, `:1639`) says the adapter configures 200 ms.
  - `srp_mbx.c:29` configures `CTRL_LOOP_JOIN_CS`, 19 cs since #908's contingent moves.
  - So the check's Join-arm layout test (`srptx.hpp:591`) matches no arm, and its record's `timers_cs.join` reads 20.
  - It is listed under Known limitations for an Issue of its own.

### 17.3 Round 16's residue (R837-10-R1)

16.3 now says `record_classes.py`'s output equals round 13's up to the order of two result-set listing lines. The corrected RC line is `receipts/statements/RC.txt` in this round's packet.

### 17.4 Proof and gates

- `git diff --name-only b6f5c638 478ff78c` lists `docs/design/SPLIT_CONTROL_MEMORY.md` alone. No compiled or executed input changed, so round 16's identity proof and statement checks, and round 13's measurements, carry to `478ff78c`.
- **The documentation gates** on a clean clone of `478ff78c`: 23 commands, each rc 0, with 0 changed paths before and after (`receipts/gates/SUMMARY.txt`, one log each). They are `docs_check.py`; `check_em_dash.py` from `66adb9a9`, `cec88385` and `b6f5c638`; doc style, gPTP docs and `DOC_MAP`; both idiom gates; `git diff --check`; the solution, submodule, feature-status, TODO-ownership, hygiene, doc-path and archive gates; and the four sweeps, round 14's cost grep (64 hits), round 15's row sweep (143), round 16's comment sweep (15) and the statement sweep (178), every hit classified.

## Round 18

Round 18 answers round 17's delta review, R837-11 (PR #902 issuecomment-6892594920): NEGATIVE, on three MINORs. Two commits, `6ef3be3b` and `4ae887a1`, change `docs/design/SPLIT_CONTROL_MEMORY.md` alone; this body changes too. Its receipts are in its own packet.

### 18.1 The queued-notice table (R837-11-F1)

- **`:2204-2205`** now give the head's rows, with `12180198`'s at the 1,200 us slice beside them:
  - 1x1/1if: the first notice 14.66 ms, held to 20, and the last 127.21 ms, held to 130 (`AECP_QUEUED_MS`);
  - 8x8/2if: 20.93 ms (stated 22) and 806.60 ms (stated 62, ceiling 70), reported.
- **`:2207`:** at 1x1/1if, the first notice's bound is decision D's 20 ms, and the last's is #894's amendment's 130 ms (decision D's 125 before it).
- These equal `flip_grade.py --check` at both points (`receipts/flip-check-1x1.txt`, `flip-check-8x8.txt`).

### 18.2 `EDIT_RECORD_US` (R837-11-F2)

`:2477` now says each paced record "was then charged a one-row edit's record, `EDIT_RECORD_US`, 260 us at 1x1/1if ... and 325 us at 8x8/2if". It adds: "At the head `EDIT_RECORD_US` is the paced class's record, its dearest member's, 300 and 595 us, since SET_CONFIGURATION joined the class". That equals `edit_rows.EDIT_RECORD_US`, `{'1x1/1if': 300, '8x8/2if': 595}`.

### 18.3 The mechanical sweep (R837-11-F3)

- **Credit:** the method and its scripts are the R837-11 reviewer's. `scripts/constant_history.py` is copied unchanged, and `scripts/figure_sweep.py` is adapted.
- **Superseded values:**
  - `constant_history.py` reads every `#define` with a number under `sw/firmware/ctrl`, and every stated table of the model, at the PR's base `66f71326` and at every commit that touches one of them: 125 snapshots, 73 constants moved (`receipts/constant_history.txt`). Every value a constant held that the head does not is superseded.
- **The sweep** (`figure_sweep.py` at `4ae887a1`, `receipts/figure_sweep.part00.tsv` and `.part01.tsv`, split for the index (`figure_sweep.README.txt`)) has four parts:
  - **The reviewer's rules,** unchanged: each moved constant's prose subject beside its superseded values.
  - **One AUTO rule per moved constant,** added in round 18: the constant's own name beside any number its history held and the head does not. So no hand list bounds the sweep.
  - **ROW:** every two-decimal ms figure, in a sentence naming a row, that is not one of the head's rows from `flip_grade.py --check` at both points.
  - **LOAD:** every three-decimal figure, in a sentence naming the load, that is not one of the head's loads.
  - **Scope:** every Markdown file the PR changes, every first-party README, every first-party source line under `sw/` and `tb/`, and this body.
- **Classification** (`scripts/figure_classify.py`, `receipts/figure-classes.txt`). It exits 1 on any hit it does not class. Its 824 hits at the head: 457 historical, 75 beside the head's figure, 15 the head's own, 269 another quantity (another point, component, clause figure, requirement bound or plant), and 8 that name #916. 541 hits carry no history marker, and each of them is classed by its own line, or by a region whose every hit was read.
- **The claim, exactly:** every hit of this sweep at `4ae887a1` is classified, and none states a superseded figure as current. Any figure a sentence states beside no moved constant's name or subject, and that is not a two-decimal row or a three-decimal load figure, is outside the sweep's reach.

### 18.4 Found by reading the sweep's hits

Each is now history, with the head's figure beside it:
- **`:2284`,** the "#32 moves" table's `item.acmp` row: 55 and 55 us at 1x1/1if and 70 and 70 at 8x8/2if at the head (120, 125 and 185, 165 at round 30). The sweep could not see this row, since a table cell carries no unit.
- **`:2287`:** round 30's ACMP owed frame, 125 us, now beside the head's 55.
- **`:2379`:** the long record's successive states are past tense, with the head's record beside them: 87,895 cycles at 1x1/1if and 146,678 at 8x8/2if, within the 975 and 1,650 us stated.
- **`:2476` and `:2477`:** the one-row edit cut's measurements are past tense.
- **`:2520`:** THE RETRY's pre-tiers 20 ms bound is past tense. Under THE TIERS the first queued notice is a tier row: 14.66 ms within 20 at 1x1/1if, and 20.93 ms at 8x8/2if, stated 22 and reported.

### 18.5 The residues (R837-11-R1 to R4), as the report gives them

- **R1:** `:2427` "None (the head lever c measured)".
- **R2:** `:2432` "the last queued notice was 125.87 ms then".
- **R3:** `:2244` "before #894, ... R4 was 73.02 ms": "was" and "were" throughout the three sentences.
- **R4:** this body's round-12 narrative: "stood at round 12's start (its TICK restated to 55 us by the final pass, below)".

### 18.6 Proof and gates

- `git diff --name-only 478ff78c 4ae887a1` lists `docs/design/SPLIT_CONTROL_MEMORY.md` alone. Round 16's image, ELF and statement proofs, and round 13's measurements, carry to `4ae887a1`.
- **Gates on a clean clone of `4ae887a1`:** the documentation and idiom gates as in round 17, the flip check at both points and the load check, `constant_history.py`, and the sweep and its classifier, each rc 0 but the flip check over both points and at 8x8/2if, which exit 1 by design (`receipts/gates/SUMMARY.txt`).

## Findings

| Finding | Resolution | file:line | Verification |
|---|---|---|---|
| Ruling 6883864236: arm B's SET_CONFIGURATION record 33,724 cycles at 1x1/1if (355 by the rule) and 78,332 at 8x8/2if, which no stated cost covers | Attributed (item 1). Cut once (`f275b619`): one GSI word a stream for the running check, and stream entries only on a moved index. That gives 28,509 (300) and 55,377 (585). Still over 235, so it is paced (`fe0cef5b`) and the paced class is the dearer member (`e4d80a8a`): 300 at 1x1/1if, 595 at 8x8/2if | `aecp_commands.c:100`, `:125`, `:196`, `:198`, `:214`; `aecp_face.c:119`, `:169`; `aecp.h:106`, `:170`; `edit_rows.py:38`, `:41` | arm B in the final pass: 28,376 (300 of 300) and 56,474 (595 of 595) held as paced by `record_classes.py`; 4 new tests and 1 for the pace; 13 rows caught by name; AECP campaign 299 of 299 |
| Ruling item 3: a planted control charging an unpaced SET_CONFIGURATION as ordinary must fail by name | Model: the class at the edits' record alone is refused by name (`an accepted SET_CONFIGURATION charged below its record`) and shortens ACMP's row. Pass check: a SET_CONFIGURATION followed within the pace is held as ordinary and refused (`SET_CONFIGURATION not paced`) | `edit_rows.py:43`, `:86`; `record_classes.py:257` | `rows_tiers.py --selftest`: the control refused; `record_classes.py --selftest` 11 of 11 |
| Ruling item 4: the completion tick against `event.TICK` | Arm B never waits; the window's only TICK precedes the command: 2,159 (25) and 2,404 (30), within 50 and 40, so the completion restates nothing. (The TICK is restated at 55 us on arm A's `backlog-adp` groups at the final firmware: below.) The late-acknowledgement completion is staged by no arm (open) | `receipts/attribution/tickwin-*.txt` | the traced passes after the record (`tree-b1-poll.txt`, `tree-b1-deliver.txt`, `tree-b8-*.txt`) |
| Ruling item 5: hold arm B's SET_CONFIGURATION and SET_STREAM_INFO, and refuse a pass lacking them | Held by class; a pass whose 1x1/1if answering-ports leg ran no accepted SET_CONFIGURATION or no SET_STREAM_INFO is refused; planted controls for each | `record_classes.py:49`, `:134`, `:189`, `:255` | `record_classes.py --selftest` 11 of 11; over every leg RESULT PASS |
| R837-6-F1 (MINOR): the 1x1/1if stated-table survey read only arm A legs | The answering-every-port arm run whole at 1x1/1if (16 groups), and every stated table compared by the rule over it, arm A and arm B, each line with its leg prefix. It found AECP's timer slot over (6,206, 70 > 65), and arm A found a LINK (155 > 150), a build of one (735 > 725) and, at the final firmware, a TICK (55 > 50). All four restated; rows, the pace and the slice rule rerun: the last queued notice 132.71 > 130 at 900 us and the slice rule chose 950: round 12's STOP. Round 13 takes the rule's choice, and at 950 every row holds (the last queued notice 127.21) | `load_grade.py:138`, `:174`, `:177`; `rows_grade.py:93`; `ctrl_loop.h:326`; `poll_grade.py:90` | round 12's compare (`A1/`, `A2/`, `E1/`, `B1F/`); round 13's `receipts/compare/compare-1x1.txt` (`A1/` to `A4/`, `E1/`, `B1F/`) and `compare-8x8.txt`; `receipts/model/flip-1x1-ed0df35b.txt` (exit 0), `tier-grid-1x1-ed0df35b.txt` |
| R838-6-F1 (MINOR), R837-6-R2: "the cut adds 220 B of rom to every image" | Replaced by each image's growth against `7398ec0a`: +224 B in each 1x1 image, +208 B in each 8x8 image. Round 12's growth is stated the same way: +216 B, and +224 in the 1x1/1if size fixture | `SPLIT_CONTROL_MEMORY.md:2480`, its new subsection's images bullet | `receipts/images/rom-per-image.txt` (8 images at `7398ec0a`, `9606b3a9`, `fe0cef5b`) |
| R838-6-F2 (MINOR): section 13's current R4 12.85 and the validation example's load were the previous head's | Section 13's current rows table, its rows-history row, its current summary (R4 13.10, the last queued notice 127.21 within 130 at the rule's 950 us slice; the 900 us figures, R4 13.05 and 132.71 over 130, are its history row and round 12's stop) and its load (0.516 and 0.512), and FR_NFR 3.4.1, are the head's; so are this body's examples | `SPLIT_CONTROL_MEMORY.md:2346`, `:2370`, `:2525`; `FR_NFR.md:383`; [How to validate](#how-to-validate) | `flip_grade.py --check --point 1x1/1if` and `load_grade.py --check` at the head (`receipts/model/*-3909588f.txt`) |
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
| R837-8-F1 (MINOR, Docs): a superseded txL/R4L pace figure stated as current in FR_NFR 3.4.1, and its twin at section 13's `:2467` | Both made history, with the head's figure beside them. The rows-history table's row figures and every load figure were swept (15.1); round 18's sweep found the queued-notice table's, which those tokens missed (18.1) | `FR_NFR.md:383`, `:387`; `SPLIT_CONTROL_MEMORY.md:2351`, `:2380`, `:2402`, `:2466`, `:2467` | `receipts/stale-rows-grep.txt`: 141 hits: 96 historical, 30 beside the head's figure, 15 another quantity; 0 current with a superseded figure |
| R837-8-R1, R838-9-R1 (RESIDUE): the R838-6-F2 row cites `:2524` | It cites `:2525` | the R838-6-F2 row | the cited line gives R4 13.10 |
| R837-8-R2 (RESIDUE): a present-tense sentence in the past-tense 900 us paragraph | Past tense | `SPLIT_CONTROL_MEMORY.md:2509` | the text |
| R837-8-R3 (RESIDUE): 14.1 claims a head figure beside every moved past-tense site | Made exact (15.2) | 14.1 | the text |
| R837-8-S1 (SUGGESTION): take the stale-figure tokens from the rows-history table | Taken | `scripts/stale_rows.py` (the packet) | the token list in the receipt |
| R837-8-S2 (SUGGESTION): point to item 5's precondition from the face's contract note | Not taken: section 13 and the receipt state it, which the review finds sufficient, and round 15 keeps to the two files the finding names | none | none |
| R837-9-F1 (MINOR, Docs): `aecp_mbx.h:50` states txL 49.69 ms at 7 ms as current | History, "txL was 49.69 ms at 7 ms, and 8 ms did" (`eed2e40d`); tokens identical | `aecp_mbx.h:50` | `receipts/identity/tokens.txt`; `receipts/comment-sweep.txt` |
| R837-9-F2 (MINOR, Docs and Tests): `CTRL_LOOP_TX_MS` states 98 ms at two interfaces under the tx row's 98.49, and no control plants the two-interface statement | Outcome 1, by the manager's ruling: 99 ms at two interfaces. Both controls plant the two-interface leg, and `:2351` is history plus the head's (`b6f5c638`) | `ctrl_loop.h:371`; `rows_tiers.py:932-935`; `flip_grade.py:174-184`; `SPLIT_CONTROL_MEMORY.md:2351` | `tx_statements` `[]` at both points; `flip_grade.py --check --point 1x1/1if` rc 0; self-tests 1,033 and 585 of as many; the blind-check probe escapes both controls |
| R837-9-S1 (SUGGESTION): tokens from every superseded figure, and the constants' comments swept | Taken for `sw/` and `tb/`: the sweep's tokens include txL and R4L at every pace and 8x8/2if's earlier rows. In the documents, the nine pace figures are all past tense | `scripts/comment_sweep.py` (the packet) | `receipts/comment-sweep.txt` |
| R837-9-S2 (SUGGESTION): separate rows over their bounds from statements under their rows at 8x8/2if | Taken: the statement checks are published on their own at both points, and the 8x8/2if flip receipt now holds rows alone | `receipts/statements/` (the packet) | `model-statements.txt`; `flip-check-8x8.txt` |
| New: section 13's `:2004` and `:2521` gave the pre-tiers `CTRL_LOOP_TX_MS`, 44 ms, as current | Marked as before THE TIERS, with the head's statement beside it; `:2004`'s derived 176 ms product stayed present tense until round 17 (R837-10-F1) | `SPLIT_CONTROL_MEMORY.md:2004`, `:2521` | the text |
| R837-10-F1 (MINOR, Docs): `:2004` states the pre-tiers 176 ms JoinTime product as current | History, and what governs under THE TIERS: `CTRL_LOOP_TX_BOUND_MS` holds the tx row at 1x1/1if, and 8x8/2if is reported (#890). No two-interface JoinTime claim (`478ff78c`) | `SPLIT_CONTROL_MEMORY.md:2004` | `receipts/statement-sweep.txt` |
| R837-10-R1 (RESIDUE): the round-16 RC line called `record_classes.py`'s output equal to round 13's | "Up to the order of two result-set listing lines", in 16.3 and this packet's RC line | 16.3; `receipts/statements/RC.txt` (the packet) | the two outputs, sorted, identical |
| R837-10-S1 (SUGGESTION): `tx_statements` holds the figure at or over the row, while the header says "rounded up" | Not taken: round 17 changes documents only. `:2351` states the check as "at or over its row", which is what it holds | `rows_tiers.py:565`; `ctrl_loop.h:366-367` | none |
| R837-10-S2 (SUGGESTION): sweep every superseded statement figure and its derivations | Taken (17.2). It found four more present-tense sites, now history | `SPLIT_CONTROL_MEMORY.md:2260`, `:2357`, `:2377`, `:2442` | `receipts/statement-sweep.txt` |
| R837-10-S3 (SUGGESTION): give the head's result at 8 ms in `aecp_mbx.h:50` | Not taken: round 17 changes documents only, and the review finds the history wording acceptable | `aecp_mbx.h:50` | none |
| New: `milan_dp`'s SRP transmit check mirrors the adapter's JoinTime as 20 cs (`srptx.hpp:83`), and the adapter configures 19 | Reported, not fixed: a harness's code, now #916 (17.2, Known limitations) | `tb/verilator/milan_dp/srptx.hpp:82-83`, `:591`; `tb/verilator/milan_dp/README.md:1610`, `:1639` | none in this round |
| R837-11-F1 (MINOR, Docs and Conformance): section 13's queued-notice table gives `12180198`'s rows and decision D's 125 ms as current | The head's rows: 14.66 within 20 and 127.21 within 130 at 1x1/1if; 20.93 (stated 22) and 806.60 (stated 62, ceiling 70) at 8x8/2if, with `12180198`'s beside them. `:2207` names the amendment's 130 ms (`6ef3be3b`) | `SPLIT_CONTROL_MEMORY.md:2204-2207` | `flip_grade.py --check` at both points; `receipts/figure-classes.txt` |
| R837-11-F2 (MINOR, Docs and Tests): `:2477` gives `EDIT_RECORD_US` as 260 and 325 us | Round 11's 260 and 325 as history, and the head's 300 and 595 beside them (`6ef3be3b`) | `SPLIT_CONTROL_MEMORY.md:2477` | `edit_rows.EDIT_RECORD_US`; `receipts/figure-classes.txt` |
| R837-11-F3 (MINOR, Docs and Tests): the sweeps' completeness claims are false at the head | The reviewer's mechanical sweep is adopted and credited, with one AUTO rule per moved constant added. Every claim is now stated of its own sweep's hits (Status, 14.1, 15.1, 16.5, 17.2, and the R837-8-F1 row), and 18.3 states this sweep's | `scripts/constant_history.py`, `scripts/figure_sweep.py` (the packet); this body | `receipts/figure_sweep.part00.tsv` and `.part01.tsv`, split for the index (`figure_sweep.README.txt`), `figure-classes.txt` |
| R837-11-R1 to R4 (RESIDUE) | The report's exact fixes (18.5) | `SPLIT_CONTROL_MEMORY.md:2427`, `:2432`, `:2244`; this body's round-12 narrative | the text |
| New, found by reading the sweep's hits: `:2284`, `:2287`, `:2379`, `:2476`, `:2477` and `:2520` gave superseded figures in present tense | Each made history, with the head's figure beside it (18.4) | `SPLIT_CONTROL_MEMORY.md:2284`, `:2287`, `:2379`, `:2476`, `:2477`, `:2520` | `receipts/figure-classes.txt` |
| R837-11-S1 (SUGGESTION): derive tokens from each constant's history | Taken (18.3) | `scripts/constant_history.py` | `receipts/constant_history.txt` |
## Authoritative references

- #894's round-12 ruling, issuecomment-6883864236, and the round-13 ruling on its STOP, issuecomment-6888782796.
- Round 11's authority, which stands: issuecomment-6878230332, its amendment issuecomment-6878532871 (the class split), issuecomment-6876349104, and the measurement issuecomment-6878200592.
- The bounds: issuecomment-6858269025, issuecomment-6862465874 and issuecomment-6867990126 (49 ms, 238 ms, 181 to 239 ms). The last queued notice's bound is 130 ms.
- The direct-index ruling, issuecomment-6870437042. The every-table instruction, issuecomment-6881287231.
- The round-11 delta reviews: R837-6 (PR #902 issuecomment-6884063444) and R838-6 (issuecomment-6884009601).
- Round 13's delta reviews: R837-7 (PR #902 issuecomment-6890948441), R838-7 (issuecomment-6890766701) and R838-8 (issuecomment-6890858159).
- Round 14's delta reviews: R837-8 (PR #902 issuecomment-6891424100) and R838-9 (issuecomment-6891425121).
- Round 15's delta review: R837-9 (PR #902 issuecomment-6891685454).
- Round 16's delta review: R837-10 (PR #902 issuecomment-6892175293).
- Round 17's delta review: R837-11 (PR #902 issuecomment-6892594920).
- Milan v1.2 5.4.2.5 (SET_CONFIGURATION refused while any Stream Input is bound or any Stream Output is streaming) and 5.4.5.2.
- IEEE 1722.1-2021 7.4.7 (SET_CONFIGURATION), 7.4.15 (SET_STREAM_INFO), 7.5.2 and 9.3.2.6.
- `docs/reference/FR_NFR.md` 3.4.1 and `docs/design/SPLIT_CONTROL_MEMORY.md` section 13.

## How to get into the same state

```sh
git fetch origin
git checkout 894-tiers
git rev-parse --short=8 HEAD   # 4ae887a1
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
git diff --stat 867faf1e 6b759b30    # round 15: SPLIT_CONTROL_MEMORY.md and FR_NFR.md only
git diff --stat 6b759b30 b6f5c638    # round 16: aecp_mbx.h, ctrl_loop.h, rows_tiers.py, flip_grade.py, two Markdown files
git diff --stat b6f5c638 478ff78c    # round 17: SPLIT_CONTROL_MEMORY.md only
git diff --stat 478ff78c 4ae887a1    # round 18: SPLIT_CONTROL_MEMORY.md only
python3 -B -c "import sys; sys.path.insert(0, 'tb/verilator/ctrl_service_budget'); import rows_tiers, pathlib; print(rows_tiers.tx_statements(pathlib.Path('.')))"   # []
```

The final pass, gate by gate. Commands ran on clean clones and never through a pipe; receipts are under `receipts/`. The final head is `4ae887a1`. Round 18 changes one Markdown file (18.6). Round 17 changes one Markdown file (17.4). Round 16 restates one constant read only by a `_Static_assert` and the model, with identical images and ELFs (16.4); its gates are 16.6. Round 15's commit changes two Markdown files only (15.3). Round 14's two commits change Markdown, two comments and a docstring, and every image file and harness ELF is byte-identical to `234bc149`'s (14.5), so round 13's pass below carries to it. Round 13's own pass was at `234bc149`. After `ed0df35b` it changes only `tb/verilator/ctrl_service_hooks/hooks.py`, which no workflow job and no sweep suite reads: its one reader is lane part a's `hooks_selftest`, which ran at the final head. After `c274b9f5` only five Markdown files changed before it, so the legs' firmware and graders are the head's.

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
| Round 15: the documentation and idiom gates and both stale-figure sweeps (15.3) | `6b759b30` | rc 0 |
| Round 16: 332 image files and the 14 harness legs' ELFs against `234bc149` | `b6f5c638` | 0 of 332 differ; 14 of 14 identical |
| Round 16: every statement check at both points, the stated tables and `record_classes.py` over round 13's legs (16.3) | `b6f5c638` | as 16.3 states |
| Round 16: the model self-tests, the firmware unit gate's AECP and loop arms, the documentation gates and the sweeps (16.6) | `b6f5c638` | rc 0 |
| Round 17: the documentation gates and the four sweeps (17.4) | `478ff78c` | rc 0 |
| Round 18: the documentation gates, the flip and load checks, and the mechanical sweep (18.6) | `4ae887a1` | rc 0 but the flip check over both points and at 8x8/2if, which exit 1 by design |

None of the commits after `c274b9f5` changes the compiled firmware output, as the image and object identity receipts show, round 14's included.

## Known limitations / out of scope

- **A late-acknowledged SET_CONFIGURATION's completion is unreachable on the product port** ([13.4](#134-a-late-acknowledged-set_configurations-completion-item-5-it-cannot-happen-on-the-product-port)), so no arm stages it. An SoC with no datapath, the CPU harnesses' own build, holds the acknowledgement idle, and every change waits there as the contract defines. That is a fixture, not the product.
- **Item 5's proof rests on one clock and reset precondition** (14.3): the datapath's domain is a clock output of the sys PLL, and its reset is that PLL's lock. A datapath clock or reset of its own would reopen the late path.
- **An unanswered over-cost record in arm B's `aecp-fanout` is reported, not held** (R837-7-S2). The pace holds the record after an accepted SET_CONFIGURATION for 8 ms, so its answer commits first, and no published span shows the case. Holding or refusing it needs an executable change, which round 14 does not make.
- **`milan_dp`'s SRP transmit check still mirrors a 20 cs JoinTime** (`srptx.hpp:83`), while the adapter configures 19 cs, so its Join-arm layout test matches no arm (17.2). It is #916, not fixed in a documents round.
- **The product's running check reads one window word a stream.** The answering-ports arm cannot measure it, since its stream port answers without a read.
- **8x8/2if stays reported**, no flip row; its paced class is 595 us. Its figures for #894's 8x8 lane and #890 are in [Status](#status).
- **8x8-1if's legs exit 1 as in rounds 9 to 12** (that point states one interface's costs; the 40-notice model), and so does the 8x8 `srp` leg, on #910's build of one.
- **The tier model's load does not split the paced records.** At 300 against 235 and one paced record a pace, it adds about 0.008 at 1x1/1if.
- **`dispatch-build/` is still left untracked** by the firmware campaigns' shard-dispatch self-test (issuecomment-6881004362), not changed here.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (round 12's items 1 to 6; round 13's items 1 to 6; round 14's items 1 to 5; round 15's items 1 to 3; round 16's items 1 to 5; round 17's items 1 to 4; round 18's items 1 to 5)
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
