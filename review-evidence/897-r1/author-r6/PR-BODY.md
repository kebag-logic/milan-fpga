[A776]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Round 6: R833-5's two MINORs](#round-6-r833-5s-two-minors)** -- The GET_AS_PATH guard holding the answered read, the focus figures receipted, the five residues.
- **[Round 5: the ruled ledger and GET_AS_PATH's record, on #902's round-13 head](#round-5-the-ruled-ledger-and-get_as_paths-record-on-902s-round-13-head)** -- The ledger, the tracked record, the compare and its two restatements, and the full pass.
- **[Findings, one by one](#findings-one-by-one)** -- Every public finding and suggestion on this PR, and its status at this head.
- **[Earlier rounds](#earlier-rounds)** -- Rounds 2 to 4, kept as their record.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN (round 6) at head `b15da60a`, `897-split-as-path` -> `dev-soft-core`, on #902's round-13 head `234bc149`. It answers R833-5's two MINORs: the GET_AS_PATH guard now holds the answered read, at control_data_length 80, and pins arm B's path port; the 1x1/1if focus figures are receipted. No firmware or RTL change, and every image is byte-identical to round 5's `eca1b9ca`, whose full pass stands (the 1x1/1if flip check, txL 48.61 of 49, the last queued notice 127.52 of 130, the load 0.518). At this head: the docs workflow, 24 lane gates and the harness legs.

## Linked Issue / roles

Relates to #897
Relates to #665
Relates to #894
Relates to #901

Executor: `[A776]`

Internal cleared-context reviewer: `[R833]`:
- round 1: POSITIVE at `5e6fef3e`;
- round 2 (R833-2): POSITIVE at `3bebf03a`;
- round 3: R833-3 NEGATIVE at `f098f893` on one MINOR, an evidence-publication gap; then R833-4 POSITIVE at `f098f893`, F1's re-check;
- round 5 (R833-5): NEGATIVE at `eca1b9ca` on two MINORs, F1 (Tests) and F2 (Docs, Tests), the delta review from `f098f893` that #897's ruling of 2026-11-15, item 4, asks;
- round 6: answers R833-5 at `b15da60a`; its re-review as the manager assigns it (F1 un-covers Tests, F2 asks a Docs re-check).

External reviewer: `[R834]` (round 1, POSITIVE at `5e6fef3e`). Rounds 2 to 6 have no external reviewer, by the manager's assignment.

## Description

The Mark II split answered GET_AS_PATH with ENTITY_MISBEHAVING: the platform's `path()` was a stub that always failed, and the AECP face forwarded to it. The face now reads the path through the datapath's GSI window, kind 2, as it already reads GET_AVB_INFO's words.

| Piece | Change |
|---|---|
| `sw/firmware/ctrl/aecp/aecp_face.c` `path()` | reads the count at kind 2 selector 0, then each `path_sequence` ClockIdentity at selector 8 by its ordinal, through the AVB interface's own window. A count past the core's capacity (`AECP_PATH_ITEMS`) fails the port at the count, reading no entry. A word with no answer fails the port there, as for GET_AVB_INFO |
| `sw/firmware/ctrl/plat/ctrl_plat.c` | the unavailable stub is removed. The platform supplies `random` only (and, since #902, the owed-notice queue's slots at one interface) |
| `sw/firmware/ctrl/test/ctrl_aecp_image.c` | the size fixture's stub is removed, so the fixture links the same read |
| AS_PATH_CHANGED | already led to the unsolicited GET_AS_PATH response (`ctrl_app_aecp.c`, Table 5.22 bit 2). It now carries the datapath's sequence, and that is tested |
| `sw/litex/ctrl_memory.py` | the platform's 8x8/2if entry is 60.5 RAMB36, the owner's cap, by the ruling (round 5) |
| `tb/verilator/ctrl_service_budget/` | the `answering-ports` arm's `path` port reads the window as the face's does (`arm_path.py`). The `aecp` group times an answered GET_AS_PATH, and `record_classes.py` holds it as an ordinary record. `answering-every-port` keeps its stand-in. The 1x1/1if ordinary record and paced class are restated by the rule (round 5) |
| docs | `sw/firmware/ctrl/plat/README.md`, `sw/firmware/ctrl/aecp/README.md`, `aecp_face.h`, `docs/design/MAILBOX_SPLIT.md`, `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3, 5, 6 and 13, `docs/reference/FR_NFR.md` 3.4.1, the harness README, the split boot README |

The split datapath serves kind 2 (`hdl/milan/milan_datapath.sv`, `g_sp_ctrl` and the GSI answer block). The count comes from a snapshot taken at the count's request, and the entries come from that snapshot, at most eight (`KL_gptp_engine.sv` clamps the pathTrace count to 8), so one response carries one sequence. There is no RTL change and no mailbox contract change. A datapath window that does not answer keeps ENTITY_MISBEHAVING, as GET_AVB_INFO's, GET_STREAM_INFO's and GET_COUNTERS' do (the #897 ruling, option (a)).

Each new test below is named by a planted defect that it kills by its own words:

| Test | Rule | Plants |
|---|---|---|
| `Face.AsPathIsTheDatapathsSequenceThroughItsOwnWindow` | SUCCESS at 0, 1, 3 and 8 entries on every interface; the count and the entries in order; cdl 16 + 8 an entry; the count at selector 0, then each entry at selector 8 by its ordinal, through the interface's own window | count read as kind 1; every entry at ordinal 0; the count through interface 0 |
| `Face.AsPathCarriesItsWholeBoundAndFailsACountPastIt` | `AECP_PATH_ITEMS` carried whole; a count past it, or past the caller's capacity, fails the port at the count | the count clamped and carried; `>=` for `>` |
| `Face.AnUnansweredAsPathWordFailsItsPortThere` | a window with no answer at the count or at any entry fails the port at that word, counted unanswered | the count's failure ignored; an entry's failure ignored |
| `AppFace.AnAsPathChangeNotifiesTheDatapathsSequence` | AS_PATH_CHANGED sends the registered controller a SUCCESS GET_AS_PATH carrying the sequence the datapath serves, through the changed interface's window | the event marks bit 1; the notice for AVB_INTERFACE 0 |
| `Boot.B11GetAsPathAnswersTheDatapathsSequence` | the composed split answers GET_AS_PATH SUCCESS with the datapath's sequence, at one and two interfaces | the old stub's answer restored |
| harness: the `get_as_path` row (`selftest_answers.py`) | GET_AS_PATH on AVB_INTERFACE 0 at its length, SUCCESS where the ports answer | sent on AVB_INTERFACE 9; stated SUCCESS on the image as linked; sent as GET_AVB_INFO |
| harness: `record_classes.py` | a pass's answering-ports leg at 1x1/1if answers a GET_AS_PATH SUCCESS with its eight entries (control_data_length 80), held to `record.aecp`; every GET_AS_PATH that arm answers SUCCESS at another length is refused | a pass missing arm B's GET_AS_PATH; a GET_AS_PATH over `record.aecp`; a GET_AS_PATH answered SUCCESS with no entries |
| harness: `record_classes.port_findings` | the answering-ports arm's `path` port is `arm_path.py`'s, which reads the count and each entry through the window | arm B's path port answers no entries at once, reading no window (the earlier port) |

## Round 6: R833-5's two MINORs

R833-5 (PR #898) reviewed rounds 4 and 5 from `f098f893`. It was NEGATIVE at `eca1b9ca` on two MINORs: the code otherwise checked out, and every STOP condition of the ruling was clear. Round 6 changes no firmware and no RTL.

| Commit | What |
|---|---|
| `b15da60a` | `record_classes.py` holds arm B's GET_AS_PATH as the answered read; the self-test pins arm B's `path` port to `arm_path.py`'s; a harness mutant restores the earlier port; section 13's residue (RES1-RES3) and the guard's description; the harness README |

**F1: the guard holds the answered read.** The guard held a GET_AS_PATH answered SUCCESS. The earlier port, which read nothing and answered no entries, also answers SUCCESS, so restoring it left every self-test green.
- **The response is read.** `record_classes.py` reads each record's response control_data_length from the frame it already parses. A pass is refused unless its answering-ports leg at 1x1/1if answered a GET_AS_PATH SUCCESS at `ANSWERED_LENGTH`, 80. That is 16 B (controller_entity_id, sequence_id, command_type, descriptor_index, count) and 8 B for each of `arm_path.ENTRIES` entries (IEEE 1722.1-2021 7.4.41.2). Every GET_AS_PATH the answering-ports arm answers SUCCESS at another length is refused by name.
- **The planted control.** "a GET_AS_PATH answered SUCCESS with no entries" is refused: 14 of 14 controls.
- **The port is pinned.** `port_findings()` requires `build.VARIANTS['answering-ports']` to define `arm_path.B_PATH` and put it in the face's `path` port, and that port to read the count and each entry through the window. It is a harness self-test check ("the answering-ports arm's path port is arm_path.py's, which reads the window"), and `record_classes.py --selftest` fails on it. The mutant "build: arm B's path port answers no entries at once, reading no window (earlier rule)" is caught by that check: 250 of 250 mutants.
- **The real legs.** Arm B answers GET_AS_PATH SUCCESS at length 80: 16,208 cycles at 1x1/1if; 16,397 and 15,966 at 8x8/2if. Arm A's refused responses are 16. `record_classes.py` over every one-interface leg and the 8x8 legs: **RESULT PASS**.
- **The stub, on a real leg.** A scratch arm B leg built with the earlier port (never committed) answers SUCCESS at length 16, 10,019 cycles. Graded beside every leg, it is refused: "a GET_AS_PATH answered SUCCESS with control_data_length 16, not the 80 of the 8 entries the arm's path port reads and answers".
- **R833-5's own probe** (`probe_stub_path.sh`), on a clean clone of `b15da60a`: both suites refuse it by name: `run.py --self-test` fails "the answering-ports arm's path port is arm_path.py's, which reads the window" ("the answering-ports arm's build does not define arm_path.py's path port"), `record_classes.py --selftest` exits 1 on the same finding, and `build.py` is restored.

**F2: the focus figures, receipted.** The round's receipts list every AECP record of the head's legs (arm B and arm A at both points) and of the measurement legs:
- each record's cycles, its cost by the rule, its command and status, and its response's control_data_length;
- each GET_AS_PATH response frame, decoded: its count, control_data_length, frame length and ClockIdentities.

| Figure | Receipted as |
|---|---|
| 1x1/1if, arm B | `16,208 cycles 175 us command GET_AS_PATH status 0 control_data_length 80`; `count 8, control_data_length 80 (16 + 8 x 8 = 80), frame 106 B` |
| 1x1/1if, arm A, refused | `10,948 cycles 115 us command GET_AS_PATH status 10 control_data_length 16`; `count 0` |
| 8x8/2if, arm B, interfaces 0 and 1 | `16,397` and `15,966 cycles ... status 0 control_data_length 80`; the interface-1 response on port 1, `count 8` |

**Residue** (R833-5's exact fixes):
- RES1: section 13, R4 13.25 ms (13.10 at the final pass's restatements).
- RES2: the 950 us paragraph's figures are in the past tense, the load "was 0.516 and 0.512" (with GET_AS_PATH's restatements, below).
- RES3: "within the 245 us of an ordinary record (235 before the restatements below)".
- RES4: this body's roles.
- RES5: round 5's REVIEW READY, edited in place. The as-built check refuses R4 and last; the first queued notice is at its 20 ms bound.

**At this head** (each part on its own fresh clean clone):

| Gate | Result |
|---|---|
| the docs workflow, every job and `run:` step (`wire-accountability`, `docs-check-no-git`, `docs-check`, `docs-gates-0` to `-2`) | 61 steps ran, 34 not run with a stated reason, 0 bad; the job clones have no tracked change afterwards |
| lane gates (24) | 20 at 0, and the 4 that exit 1 by design, each output byte-identical to `eca1b9ca`'s. Among the 20: the harness self-test (0 failures, 250 of 250 mutants), `record_classes.py --selftest` (14 of 14 and the port check), `rows_tiers`, `load_grade.py --selftest` and `--check` (0.518 / 0.514), `flip_grade.py --selftest` and `--check --point 1x1/1if` (output identical to `eca1b9ca`'s), `tier_grid.py` (950 us), `plat_ledger`, the fixtures and `test_ctrl_memory`, `docs_check` 0 findings, the em-dash gate against `cec88385` and `234bc149`, both idiom ratchets, and R833-5's probe refused by name |
| CPU budget harness legs, one a point and arm | every leg rc 0; `record_classes.py` at this head over them and round 5's one-interface legs: RESULT PASS |
| the images | all 14 byte-identical to `eca1b9ca`'s: the six harness arms, and the size fixture and the platform at the four points |

## Round 5: the ruled ledger and GET_AS_PATH's record, on #902's round-13 head

This round follows #897's ruling of 2026-11-15 (issuecomment-6890824581) on round 4's STOP. It continues from round 4's local merge `b58a5430` (`f098f893` + `894-tiers` `234bc149`). `dev-soft-core` is still `cec88385`.

| Commit | What |
|---|---|
| `2170b22e` | the platform's 8x8/2if entry at 60.5: #901's `8238156d`, its ledger and control lines identical, the rest adapted to this tree (below) |
| `3079bb1e` | GET_AS_PATH's record timed in the answering-ports arm's `aecp` group, its `path` port reading the window as the face's does, and held in `record_classes.py` as an ordinary record |
| `6ef7a8ff` | the `aecp` group's GET_AS_PATH sent on AVB_INTERFACE 0 at every interface, the one AVB_INTERFACE each image holds, as `get_avb_info`'s |
| `eca1b9ca` | the ordinary AECP record at 1x1/1if at 245 us and the paced class at 305, by the rule; section 13's GET_AS_PATH subsection on `234bc149` |

**Item 1, the ledger.** `8238156d` does not cherry-pick onto this tree: the platform entry's reason and its `ctrl_plat` figure differ between the two trees (#895's 20,352 B, this tree's 20,288). So the identical text is applied where the trees agree:
- `ctrl_memory_ledger.py`'s 30 lines and `test_ctrl_memory.py`'s control ("the size fixture's entry at the platform's 60.5") are byte-for-byte `8238156d`'s;
- the entry moves `60.0` -> `60.5`, as in `8238156d`;
- its reason names this tree's 168 B and both rulings;
- section 5 states the plan: 1,880 B of `rom` left in 133,120, a debt of 4.5 RAMB36, GET_AS_PATH using 312 B of the half tile, graded against 133,120 B once #901 is composed (items 3 and 5).

`plat_ledger.py --self-test` passes every point, with 7 of 7 planted controls; the platform's 8x8/2if image is 131,240 B, 60.5. At the #901 merge only the entry's reason, its `ctrl_plat` figure and two docs lines conflict. The ledger module and its control merge trivially.

**Item 4, GET_AS_PATH's record, tracked.** The answering-ports arm's `path` port (`arm_path.py`) reads the count and then each entry through the interface's window. Each word runs to the contract's whole bound, since the test SoC never answers, and the port answers eight entries, the shipped datapath's most. The `aecp` group's `get_as_path` row is in the scenario's group list, so every later pass times it:

| Point | Arm | GET_AS_PATH's record, CPU cycles | By the rule | The ordinary class |
|---|---|---:|---:|---:|
| 1x1/1if | answering-ports, SUCCESS, 8 entries (control_data_length 80) | 16,208 | 175 us | 235 (245 restated, below) |
| 8x8/2if | answering-ports, SUCCESS, if0 / if1 | 16,397 / 15,966 | 175 / 170 us | 265 |
| 1x1/1if | arm A, ENTITY_MISBEHAVING | 10,948 | 115 us | 235 |
| 8x8/2if | arm A, ENTITY_MISBEHAVING | 11,328 / 11,150 | 120 us | 265 |

The nine answers' two data words each (18 reads), which an unanswered read does not fetch, would add about 1,080 cycles: about 17,290, 185 us. The record holds as an ordinary record, and the response does not change on the wire.

At `3079bb1e` the row sent descriptor_index = the interface, and both 8x8 legs were refused: "aecp.get_as_path.if1: unexpected response: status NO_SUCH_DESCRIPTOR". Each image holds one AVB_INTERFACE (`MBX_CTRCHG_AVB_INTERFACE_COUNT 1u`), so `6ef7a8ff` sends it on AVB_INTERFACE 0 at every interface, as `get_avb_info`'s row does. The 1x1 scripts are unchanged by it.

**The record classes over every one-interface leg.** The legs: the full arm A at 1x1/1if (96 groups, one build), the whole answering-every-port arm (16 groups) and the answering-ports leg (`aecp`, `aecp-fanout`, `aecp-largest-notice`), plus the 8x8 legs (answering-ports `aecp`, `aecp-largest-notice` and `aecp-fanout`; arm A `aecp` and `datapath-events`). Every leg exits 0:
- 0 refusals;
- the 7 known held-egress `backlog-owed` misses;
- 0 of 140,748 arm A passes over THE SHARE at 1x1/1if;
- at 8x8/2if, #902's two reported `aecp-largest-notice` passes over THE SHARE (the longest 244,460 cycles).

Two class lines were over at 1x1/1if:

| Class | Record | CPU cycles | By the rule | Stated | At `234bc149` | At `b58a5430` |
|---|---|---:|---:|---:|---:|---:|
| ordinary (`record.aecp`) | the answering-every-port arm's SET_NAME, each of its 16 groups | 23,051 | 245 us | 235 | 22,236 | 23,051, the same ELF |
| paced (`edit_rows.PACED`) | the answering-ports arm's accepted SET_CONFIGURATION | 28,752 | 305 us | 300 | 28,376, #902's | 28,357, with the earlier port that answered at once |

Each is the same work with its fetches moved by the code's placement:
- at the merge, 156 of the every-port image's 407 uniquely named functions sit 4 to 868 B later;
- the reading port puts every function after arm B's ports 304 B later.

**The stated-table compare by the rule** (over arm A's four parts, the every-port arm and the answering-ports leg, each figure named by its leg). Every other 1x1/1if cost holds by the rule. Measured, then by the rule, then stated:

| Cost | Measured | By the rule | Stated |
|---|---:|---:|---:|
| the build of one | 690.59 us | 730 | 735 |
| AECP's timer slot | 66.47 us | 70 | 70 |
| a LINK | | 150 | 155 |
| a TICK | | 50 | 55 |
| an SRP record | | 280 | 280 |
| the largest legal notice | | 360 | 365 |
| the largest legal command | | 925 | 975 |
| AS_PATH_CHANGED | 29.18 us | | 35 |
| AVB_INFO_CHANGED | 30.53 us | | 35 |
| AMAP_LIVE_WRITE | 24.24 us | | 30 |

So the two class lines are restated by the rule (ruling item 4):
- `load_grade.py`'s `record.aecp` at 1x1/1if: 235 -> 245 us, both columns;
- `edit_rows.PACED`'s accepted SET_CONFIGURATION at 1x1/1if: 300 -> 305 us.

Re-graded at those costs, the compare's only exceedances are class lines, each within its own class: the largest legal notice 360 of 365, SET_CONFIGURATION 305 of 305. `record_classes.py` over every leg at both points: **RESULT PASS**.

**The pace and slice rules, and the rows.** `flip_grade.py --check --point 1x1/1if`: **RESULT PASS** at the built design, every row by every source:

| | R4 (20) | R4L (238) | ACMP (30) | ADP (30) | MAAP (30) | First (20) | R5 (90) | R6 (90) | Last (130) | tx (49) | txL (49) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| this head | 13.25 | 188.48 | 29.14 | 27.49 | 27.61 | 14.67 | 74.32 | 72.41 | 127.52 | 33.57 | 48.61 |
| #902 at `234bc149` | 13.10 | 188.48 | 28.95 | 27.30 | 27.42 | 14.66 | 74.07 | 69.86 | 127.21 | 33.38 | 48.43 |

- **The load:** 0.518 at the pin and 0.514 with tsn-c-stack #32, against 0.70.
- **The pace:** 8 ms by its rule (`paced_rows.choice`), as `aecp_mbx.h` states.
- **The slice rule** (`tier_grid.py --point 1x1/1if`): 6 of 420 candidates hold. It chooses slice 950 us, tier 1 aecp-first, tier 2 srp-first, AECP queue, cap 2, the built design, with a least margin of +0.0080 (#902: 10 of 420, +0.0116).
- **The images:** no firmware header states either cost, so every image is unchanged by the restatement.

**8x8/2if, reported** (not held, and not restated: this pass compared the 1x1/1if tables only):
- Arm A's `datapath-events` measures 38.64, 34.56 and 23.88 us for AVB_INFO_CHANGED, AS_PATH_CHANGED and AMAP_LIVE_WRITE (37.40, 33.67 and 23.19 at `234bc149`).
- AVB_INFO_CHANGED and AMAP_LIVE_WRITE are 45 and 30 us by the rule, against the 40 and 25 stated there.
- Restated in a scratch tree, the reported last queued notice would be 836.57 ms (806.60) and txL 469.52 (459.40). Every other 8x8 row and the 8x8 load are #902's.
- Every other 8x8 class is within: the largest legal command 1,540 of 1,650, the ordinary record 240 of 265, the paced class 585 of 595.
- For #894's 8x8 lane and #890.

**The answered notice** (a scratch copy of the answering-every-port arm whose `path` reads the count and eight entries and answers them once the arm's ports answer, never committed; its diff and the round's inputs are published with this round's receipts):
- the round that builds it is 28,098 CPU cycles in `notice-every-0` (one notice, admitted at 34,000) and 65,576 in `notice-burst-0` (three notices, 85,000), the eight entry reads 3,103 cycles of each;
- both groups exit 0, with no round, notice or pass over its bound.

**ROM at this head** (`plat_ledger.py --self-test`, 7 of 7 controls; the fixtures linked on the same maps; the harness arms freshly built). `sram` is unchanged at every point.

| Image | 1x1/1if | 1x1/2if | 8x8/1if | 8x8/2if |
|---|---|---|---|---|
| size fixture | 111,344 B, 41.0 | 112,632 B, 41.5 (8 B before its next granule) | 124,848 B, 54.0 | 126,112 B, 59.0, its entry (864 B to spare) |
| platform | 116,392 B, 42.5 | 117,704 B, 43.5 | 129,944 B, 56.0 (1,128 B to spare) | 131,240 B, 60.5, its entry (1,880 B left in 133,120) |
| harness arm A / answering-ports / answering-every-port | 111,344 / 111,832 / 111,660 B, 41.0 each | | | 126,112 / 126,600 / 126,436 B, 59.0 each |

**The full pass, once, at the final head** (each part on its own fresh clean clone):

| Gate | Result |
|---|---|
| every workflow job a PR to `dev-soft-core` triggers, every `run:` step (`rtl-fast`, `docs`, `elaborate`, `rtl` with its four yosys shards) | 139 steps ran, 226 not run with a stated reason, 0 bad; the 28 job clones have no tracked change afterwards |
| AECP campaign | 308 caught, none missed; the nine `face-as-path-*` plants each caught by its named test |
| control campaign | 717 of 717; `plat-as-path-unavailable` caught by `platboot1` and `platboot2` |
| SRP campaign | 345 caught, none escaped |
| firmware self-test, coverage, boundary | PASS; `fw_coverage.py --check` PASS, 39 files; `ctrl_boundary: PASS` |
| lane gates | 40 at 0, and the 4 that exit 1 by design (the flip check over both points, at 8x8/2if and as built at 1x1/1if, and the tier model's report), each refusing the same rows as at `234bc149`. Among the 40: the harness self-test (0 failures, 249 of 249 mutants), `rows_tiers` 1,033 of 1,033, flip 585 of 585, load 26 of 26 planted controls; `flip_grade.py --check --point 1x1/1if`, `load_grade.py --check`, `tier_grid.py --point 1x1/1if`; `plat_ledger.py --self-test` (8x8-if2 131,240 B, 60.5), the fixtures, `test_ctrl_memory`; `docs_check` 0 findings, the em-dash gate against `cec88385` and `234bc149`, both idiom ratchets; the split boot ready at 26.921, 66.545 and 68.766 ms against 20,000, its native controls and plants; `test_builder.py --require-rv32`; the NVM gate (526 tests, 144 plants); `behave`; the twin and its plants; the hooks self-test |
| CPU budget harness legs, one a point and arm | every leg rc 0; every ELF byte-identical to its measurement build, and the group scripts to the measurement's |
| full Verilator sweep | 65 suites (15, 17, 17 and 16 a shard, each shard on its own picked range): 64 passed, 0 failed; `milan_dp` timed out at its 4,800 s in shard 0 under the host's contention (load average about 200; "result UNKNOWN, not a failure" by the runner, its partial log 13,690 checks, 0 failures), and ran again alone on its own booked range on a fresh clean clone at the head, as the runner asks: PASS in 2,548 s, `suite_tally.py --verdict` clean, 13,878 checks. 2,713,040 checks in all, 0 in-suite failures, round 3's count |

**The data placement (#909).** The 8 images at the final head's firmware are byte-identical to the merge's (`b58a5430`), and every writable symbol (`.data`, `.bss`, the stack) has the address and size it has at `234bc149`.

## Findings, one by one

| Finding | Lens | Status at this head | Where |
|---|---|---|---|
| R833-5 F1 (MINOR): the GET_AS_PATH guard held a SUCCESS, not the answered read | Tests | fixed at `b15da60a`: the response's control_data_length 80 held, a planted control with no entries, arm B's port pinned and its mutant | `record_classes.py`; `selftest_mutants.py` |
| R833-5 F2 (MINOR): the 1x1/1if focus figures had no published receipt | Docs, Tests | fixed: every record of the head's legs, with each GET_AS_PATH response decoded | round 6's receipts, `records/` |
| R833-5 RES1-RES3: section 13's current figures | Docs | fixed with the exact wording | `SPLIT_CONTROL_MEMORY.md` section 13 |
| R833-5 RES4: the PR body's round-5 line | Docs | fixed | this body, roles |
| R833-5 RES5: round 5's REVIEW READY, "Lane gates" | Docs | fixed in place | #897 issuecomment-6894799910 |
| R833-5 S1: `arm_path.B_PATH` ignores each read's status and the count | Tests | retained: the stand-in its docstring states, since the test SoC never answers a window | `arm_path.py` |
| R833-5 S2: the packet INDEX's pre-redaction hashes | Docs | applied: this round's INDEX is generated after sanitizing | round 6's INDEX |
| R833-5 S3: the answering-every-port arm's `a_path` reads nothing | Tests | retained (R833-1 S1); its answered notice is measured in the scratch arm | `build.py` |
| R833-5 S4: `build.py:122-134` comment wrapping | Docs | retained; `build.py` stays at the 1,000-line limit | `build.py` |
| round 4 STOP: the platform's 8x8/2if image 168 B past its 60.0 entry | (STOP) | ruled (issuecomment-6890824581): the entry at 60.5, `8238156d`'s ledger | `2170b22e`; `plat_ledger` PASS |
| R833-3 F1 (MINOR): the scratch measurement's receipts unpublished | Tests, Docs | resolved at `f098f893` (R833-4). This round publishes its scratch diff, the excerpts `path_round.py` reads and the whole logs' sha256 | round 5's receipts |
| R833-3 R1 (RESIDUE): "at the merge of `894-tiers` `5b264bf2`" stated as current | Docs | fixed: section 13's GET_AS_PATH subsection is measured on `234bc149`; section 5's paragraph states this head (`2170b22e`), and its arm table adds the `234bc149` row | `SPLIT_CONTROL_MEMORY.md`, section 13, "GET_AS_PATH through the face" |
| R833-3 R2 (RESIDUE): "their answers' two data words each" | Docs | fixed: "the nine answers' two data words each (18 reads)" | the same subsection, first bullet |
| R833-3 R3 (RESIDUE): the PR body's reviewer lines | Docs | fixed: each round's reviewer named, round 5's as the ruling assigns it | this body, roles |
| R833-3 S1: the build of one's 725 us against 730 by the rule | Conformance, Docs | closed by #902, which states 735 us; measured 690.59 us, 730 by the rule | `ctrl_loop.h`; the compare |
| R833-3 S2: the packet INDEX generated before redaction | Docs | applied: this round's INDEX is generated after sanitizing | round 5's INDEX |
| R833-4 S3: the scratch round's inputs unpublished | Tests, Docs | applied: the two groups' `round_of` SPANs, `aecp_command` / `aecp:finish` CALLs and `mbx_win_read` SPANs are published, and `path_round.py 0000ef2c` reprints both rounds from them | round 5's receipts, `harness/scratch/` |
| R833-4 S4: the event tool's `stated_us` was the rule figure | Tests | applied: the key is `rule_us` | round 5's receipts |
| R833-4 S5: record rows unlabelled by build | Docs | applied: every record figure names its leg (build, arm, point, head) | round 5's receipts, `harness/`, `8x8/` |
| R833-1 S1: the answering arms' `path` stand-ins answer an empty sequence | Tests, Robustness | applied for the answering-ports arm, whose port reads the window and answers 8 entries (`3079bb1e`); the answering-every-port arm keeps its stand-in, and its answered notice is measured in the scratch arm | `arm_path.py`; `build.py` |
| R833-2 F4: `build.py:124-126` comment widths | Docs | retained, unchanged; `build.py` stays at the 1,000-line limit | `build.py` |
| R834-1: no executable check of the firmware's kind 2 read on the split RTL | RTL, Tests | retained: `Boot.B11` runs the composed split's read against the datapath model; no RTL changes | known limitations |
| R834-1: a datapath reset between the count and the entry reads | Robustness | retained: the datapath answers entries from the count's snapshot | known limitations |
| R834-1: 123,756 B unreceipted | Docs | resolved in round 2 | section 5's history table |
| open question: a 64-entry path's control_data_length | Conformance | open, unchanged: 528 is past 9.2.2.6's 524, so the largest legal count is 63; the shipped datapath serves at most 8 | known limitations |

## Earlier rounds

- **Round 4** (`b58a5430`, STOP issuecomment-6890794725). The sync merge of `894-tiers` `234bc149`. Three files conflicted, and each kept both sides:
  - section 13's subsections;
  - `aecp_mutants.py`'s `DEFECTS`;
  - `test_aecp.cpp`'s GSI model, which serves kind 2 and records #902's selectors.

  The platform's 8x8/2if image came to 131,240 B, 168 B past the 60.0 tiles, and the STOP was ruled as above.
- **Round 3** (`f098f893`, REVIEW READY issuecomment-6875785531, R833-4 POSITIVE). The composition with #902's `5b264bf2` and `7398ec0a` (two merges), the `ctrl_plat.c` coverage row, and the nine face plants moved into `aecp_face_mutants.py` to keep `aecp_mutants.py` within 1,000 lines. The 1x1/1if flip check passed at #902's figures.
- **Round 2** (`3bebf03a`, R833-2 POSITIVE). The sync onto `dev-soft-core` `cec88385` after #810, and `build.py` held within the 1,000-line limit.

## Authoritative references

- IEEE 1722.1-2021 7.4.41 (GET_AS_PATH command and response), 9.2.2.6 (control_data_length), 9.3.2.5 and Table 7-141 (status codes), 9.3.2.6 (timeouts, IN_PROGRESS)
- Milan v1.2 5.4.1 (response length), 5.4.2.24 (GET_AS_PATH), 5.4.5.2 Table 5.22 (the unsolicited GET_AS_PATH)
- `sw/firmware/ctrl/mbx/mbx_contract.h`: `MBX_FACE_REG_GSI_SEL` (kind 2 GET_AS_PATH, selector, ordinal), `MBX_WIN_GSI_WAIT_CYCLES`, `MBX_EV_TYPE_AS_PATH_CHANGED`, `MBX_CTRCHG_AVB_INTERFACE_COUNT`
- `docs/design/MAILBOX_SPLIT.md`, class R (the GSI window) and class E (the face events)
- protocol-processor `docs/architecture/06_aecp_engine.md` 6.10 (the gather face's kind 2 word table)
- #897 rulings issuecomment-6828659285 (option (a): an unanswering datapath window keeps ENTITY_MISBEHAVING) and issuecomment-6890824581 (round 5: the ledger, the tracked record, the compare by the rule, the STOP conditions, the merge order #902, #901, #898)
- #895 issuecomment-6876349305, item 4 (the platform's 8x8/2if entry at 60.5), and #665's owner decision of 2026-11-12 (issuecomment-6824896581, the caps)
- #894 rulings issuecomment-6867393730 (item (d)), issuecomment-6867990126, issuecomment-6883864236 (the paced class), issuecomment-6888782796 (the slice rule's choice)

## How to get into the same state

```sh
git fetch origin
git checkout 897-split-as-path
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -I tb/verilator/ctrl_service_budget/record_classes.py --selftest
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$OUT/b1" --groups aecp,aecp-fanout,aecp-largest-notice --variant answering-ports --out "$OUT/b1/results" --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir "$OUT/b8" --groups aecp,aecp-largest-notice,aecp-fanout --variant answering-ports --out "$OUT/b8/results" --record-budget-findings --record-share-findings
python3 -I tb/verilator/ctrl_service_budget/record_classes.py "$OUT/b1/results" <every one-interface leg's results>
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir "$OUT/plat-ledger" --self-test
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --check
python3 -B scripts/check_cpp_idiom.py
python3 -B scripts/check_py_idiom.py
python3 scripts/docs_check.py
```

Expected result / pass criteria: every command exits 0.
- `flip_grade.py --check --point 1x1/1if` prints `RESULT: PASS` (R4 13.25 ... txL 48.61 within 49).
- `load_grade.py --check` prints `HELD 1x1/1if at the pin: the load 0.518, its ceiling 0.70`.
- `tier_grid.py` prints `CHOSEN: slice 950 us, tier 1 aecp-first, tier 2 srp-first, AECP queue, cap 2`.
- The harness self-test reports 0 failures, 250 of 250 mutants caught, among them "build: arm B's path port answers no entries at once, reading no window (earlier rule)".
- `record_classes.py --selftest` prints `record classes: 14 of 14 planted controls refused; the answering-ports arm's path port is arm_path.py's`.
- The answering-ports legs exit 0, GET_AS_PATH answered SUCCESS in `aecp` with control_data_length 80 (16,208 cycles at 1x1/1if).
- `record_classes.py` over every one-interface leg prints `RESULT: PASS`.
- `plat_ledger` prints `POINT 8x8-if2: rom 131,240 B ... 60.5 RAMB36 (platform-8x8-two-interfaces) ... PASS`.

## Known limitations / out of scope

- The status of a GET_AS_PATH whose datapath window does not answer is unchanged: ENTITY_MISBEHAVING, as for GET_AVB_INFO, GET_STREAM_INFO and GET_COUNTERS, by the #897 ruling.
- The bench check (#897 acceptance 5) belongs to the bench lane, on the bring-up board.
- The test SoC answers no datapath window, so the measured record reads every word to the contract's bound and fetches no answer's data words. Those 18 reads are bounded, not measured: about 1,080 cycles.
- The answering-every-port arm's `path` still stands in without a read. Its answered notice is measured in a scratch copy of that arm.
- At two interfaces each image's entity model holds one AVB_INTERFACE (the mailbox contract keeps one, `MBX_CTRCHG_AVB_INTERFACE_COUNT`). So a command naming AVB_INTERFACE 1 finds no descriptor: GET_AS_PATH there answered NO_SUCH_DESCRIPTOR in this round's first 8x8 legs. Whether a two-interface entity must hold an AVB_INTERFACE an interface is outside #897's scope, and is raised here for a decision.
- 8x8/2if's datapath event costs are over their statements by the rule at this head (above). That point is reported, not held, and they are not restated.
- The face carries a path of up to `AECP_PATH_ITEMS`, 64 entries, the core's capacity since `a008ea92` (before this branch). A 64-entry response would have a control_data_length of 528, past IEEE 1722.1-2021 9.2.2.6's 524, so the largest legal count is 63. The shipped datapath serves at most 8, so no image reaches it.
- No executable check runs the firmware's kind 2 read against the split RTL itself (R834-1). `Boot.B11` runs the composed split against its datapath model.
- At the #901 merge the platform's 8x8/2if image is graded against 133,120 B (ruling item 3). Over 60.5 goes to the owner.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (acceptance 1-4, acceptance 3 as amended by the ruling; acceptance 5 belongs to the bench lane)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (the full pass at `eca1b9ca`, above)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive (rounds 1 to 3 were; R833-5 at `eca1b9ca` was NEGATIVE on two MINORs, answered in round 6)
- [ ] External review is positive (round 1 was)
- [x] Blocking and major findings are fixed and re-reviewed (R833-3 F1, resolved by R833-4)
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
