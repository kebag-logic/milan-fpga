[A776]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Round 7: the sync onto dev-soft-core 70f4056f](#round-7-the-sync-onto-dev-soft-core-70f4056f)** -- The merge of #902 and #901, its resolution, the composed image measured again, and the gates.
- **[Findings, one by one](#findings-one-by-one)** -- Every public finding and suggestion on this PR, and its status at this head.
- **[Earlier rounds](#earlier-rounds)** -- Rounds 2 to 6, kept as their record.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN (round 7) at head `59c934c6`, `897-split-as-path` -> `dev-soft-core`, synced onto `dev-soft-core` `70f4056f` (#902 and #901 merged): every 1x1/1if row holds by every source on the composed image at the built 900 us, the last queued notice 136.99 ms within its 140 and the load 0.519 against 0.70; the record classes hold at both points, GET_AS_PATH's answered read 175 us at 1x1/1if; every image is within its entry, the size fixture's 8x8/2if raised to 59.5 as S14 debt. Gates at this head: the firmware jobs and campaigns, coverage, the docs workflow, the lane gates, the split-firmware suites and the harness legs. One red that `dev-soft-core` already carries, the `milan_dp` twin (below).

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
- round 6 (R833-6): POSITIVE at `b15da60a` (issuecomment-6897027049), the bar met there with R834's ancestor;
- round 7: the sync onto `dev-soft-core` `70f4056f`; one composition review of the merge resolution, as the manager assigns it.

External reviewer: `[R834]` (round 1, POSITIVE at `5e6fef3e`). Rounds 2 to 7 have no external reviewer, by the manager's assignment.

## Description

The Mark II split answered GET_AS_PATH with ENTITY_MISBEHAVING: the platform's `path()` was a stub that always failed, and the AECP face forwarded to it. The face now reads the path through the datapath's GSI window, kind 2, as it already reads GET_AVB_INFO's words.

| Piece | Change |
|---|---|
| `sw/firmware/ctrl/aecp/aecp_face.c` `path()` | reads the count at kind 2 selector 0, then each `path_sequence` ClockIdentity at selector 8 by its ordinal, through the AVB interface's own window. A count past the core's capacity (`AECP_PATH_ITEMS`) fails the port at the count, reading no entry. A word with no answer fails the port there, as for GET_AVB_INFO |
| `sw/firmware/ctrl/plat/ctrl_plat.c` | the unavailable stub is removed. The platform supplies `random` only (and, since #902, the owed-notice queue's slots at one interface) |
| `sw/firmware/ctrl/test/ctrl_aecp_image.c` | the size fixture's stub is removed, so the fixture links the same read |
| AS_PATH_CHANGED | already led to the unsolicited GET_AS_PATH response (`ctrl_app_aecp.c`, Table 5.22 bit 2). It now carries the datapath's sequence, and that is tested |
| `sw/litex/ctrl_memory.py` | the platform's 8x8/2if entry is 60.5 RAMB36, the owner's cap, by the ruling (round 5); the size fixture's 59.5, for the harness arms on it once composed with SRP's Talker declarations, by the owner's decision of 2026-11-15 (round 7) |
| `sw/firmware/ctrl/loop/ctrl_loop.h` | `CTRL_LOOP_TX_MS` at 1x1/1if 35 ms, the composed tx row's 34.20 rounded up by #895's rule (round 7); no image changes |
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

## Round 7: the sync onto dev-soft-core 70f4056f

#902 merged into `dev-soft-core` as `659d7687`, and #901 (SRP's Talker declarations, #895) as `70f4056f`. This round is the sync. Round 6's head `b15da60a` met the bar (R833-6 POSITIVE).

| Commit | What |
|---|---|
| `d0355a45` | `Merge dev-soft-core 70f4056f`: one merge commit, parents `b15da60a` and `70f4056f`; the merge base is `234bc149` |
| `4b9dc6ce` | `CTRL_LOOP_TX_MS` at 1x1/1if 35 ms, for the composed tx row's 34.20, by #895's rule; the size fixture's 8x8/2if entry at 59.5, by the owner's decision of 2026-11-15 |
| `59c934c6` | section 13's "GET_AS_PATH on SRP's Talker declarations", as the composed image measures it |

**The merge.** Eight files conflicted, and each keeps both sides' behaviour:

| File | Hunks | Resolution | Why |
|---|---|---|---|
| `tb/verilator/ctrl_service_budget/build.py` | 1, the arms' comment | this branch's answering-ports arm (its `path` port `arm_path.py`'s) and #901's `valid-destinations` sentence | both arms are in the merged `VARIANTS` |
| `build.py`, the module limit | none | the module docstring's second paragraph rewrapped to 118 columns, the same words, 11 lines to 7 | the composition was 1,001 lines, past the 1,000-line module limit |
| `tb/verilator/ctrl_service_budget/run.py` | 1, `--variant`'s help | both arms' descriptions | both arms |
| `tb/verilator/ctrl_service_budget/load_grade.py` | 2, both stated columns and their comments | #901's tables, with `record.aecp` at 1x1/1if this branch's 245; both histories | each cost is the one of the side that moved it from the merge base `234bc149`, the larger where both did (#895's composition ruling, item 2). Against `70f4056f` that cell alone differs |
| `sw/litex/ctrl_memory.py` | 3 | the comment this branch's (carrying #901's); `ctrl_plat` 20,352 B, as `plat_ledger.py` measures the composed image; the reason both rulings', 992 B past 60.0 | the ledger holds the built image |
| `sw/firmware/gtest/coverage.ratchet` | 1, `ctrl_plat.c`'s row | `fw_coverage.py --write` on the composed tree, as CI checks it, then `--check`: `ctrl_plat.c` 132/132, and four more rows at their measured totals, each 100 % | from the tool, never by hand |
| `sw/firmware/ctrl/plat/README.md` | 3 | #901's SRP bullet and this branch's AECP bullet; the 8x8/2if image's lines with all three changes | both |
| `docs/reference/FR_NFR.md` | 1, 3.4.1's paced paragraph | #901's paragraph (9 ms pace, 900 us, the 140 ms bound), with the paced class at 305, the composition's sentence and the GET_AS_PATH guard | both |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | 12 | each current line at the composed figures; both lanes' history kept, in the order they merged (#902, #901, #898), with a new section-13 subsection and section 5's composed table | both |

Every other file either side changed carries that side's own diff exactly (`merge_sides.py`). `ctrl_memory_ledger.py` and `test_ctrl_memory.py` equal `70f4056f`'s byte for byte, since this branch's change to them was #901's own `8238156d` text.

**The composed images** (`plat_ledger.py --self-test`, 7 of 7 controls, and the size fixture at the four points), against #901's head:

| Image | 1x1/1if | 1x1/2if | 8x8/1if | 8x8/2if |
|---|---|---|---|---|
| size fixture | 112,744 B (+320), 41.5 | 114,304 B (+320), 42.5 | 125,408 B (+320), 55.0 | 126,928 B (+320), 59.0, its entry 59.5 |
| platform | 117,800 B (+312), 43.0 | 119,384 B (+312), 44.0 | 130,504 B (+304), 56.0 | 132,064 B (+312), 60.5, 1,056 B left in 133,120 |
| harness arms on the fixture (arm A / B / every-port / valid-destinations) | 112,744 / 113,232 / 113,068 / 112,872 B, 41.5 | | | 126,928 / 127,416 / 127,252 / 127,096 B, 59.0 / 59.5 / 59.5 / 59.5 |

- `sram` and `ctrl_plat` are #901's at every point.
- Every writable symbol has the address and size it has at `70f4056f` (#909).
- The platform's 8x8/2if image is 992 B past 60.0 and within the 133,120 B ruling item 3 grades the composed #901 and #898 image against.
- The three harness arms on the 8x8/2if fixture need 59.5, so that entry is raised to 59.5 as named debt owed to S14, by the owner's decision of 2026-11-15 (#665 issuecomment-6892332745). `test_ctrl_memory.py` holds the new entry and refuses 60.0.

**The tables and the rows.** At the composed tables every 1x1/1if row holds by every source at the built design, the slice rule's 900 us (tier 1 aecp-first, tier 2 srp-first, AECP queue, cap 2):

| R4 (20) | R4L (238) | ACMP (30) | ADP (30) | MAAP (30) | First (20) | R5 (90) | R6 (90) | Last (140) | tx (49) | txL (49) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 13.40 | 203.57 | 29.82 | 28.05 | 28.15 | 14.73 | 76.10 | 73.61 | 136.99 | 34.20 | 48.77 |

- The load is 0.519 at the pin and 0.516 with tsn-c-stack #32, against 0.70.
- The pace by its rule stays 9 ms.
- The slice rule holds 6 of 420 designs and chooses the built one (least margin +0.0047).
- The tx row at 1x1/1if, 34.20 ms, was over the 34 `CTRL_LOOP_TX_MS` stated. By #895's rule (issuecomment-6895331865, item 1) the figure is that row rounded up, 35. A withdrawn Talker's hold-off adds `(CTRL_LOOP_TX_MS + 9) / 10` cs, 4 at both 34 and 35, so it stays 2,023 cs, and all 12 images are byte-identical at either figure. The self-tests' plants move with it (flip 585 of 585, `rows_tiers` 1,033 of 1,033).

**Measured again on the composed image** (every group of every arm at both points: arm A, 96 groups at 1x1/1if and 94 at 8x8/2if; the `answering-every-port` arm, 16; `valid-destinations`, 2; arm B's three):
- Every leg exits 0 with no refusal. The only misses are the seven held-egress `backlog-owed` paths at each point (tsn-c-stack #26), and two arm B `aecp-largest-notice` passes over THE SHARE at 8x8/2if (#894's reported condition).
- The joins are 188.156 to 190.104 ms at 1x1/1if (359) and 185.525 to 190.193 ms at 8x8/2if (750), all within 181 to 239.
- **Every stated 1x1/1if cost holds by the rule.** The nearest are AECP's timer slot at 75 us of 75, and a grandmaster event, AVB_INFO_CHANGED and AMAP_LIVE_WRITE each at its statement. Only two class lines exceed an ordinary statement, each held by its class: the largest legal notice at 360 of 365 us, and the paced SET_CONFIGURATION at 295 of 305. **No cost is restated**, so the rows above stand.
- **`record_classes.py` over every leg at both points: RESULT PASS:**

  | Class | 1x1/1if | 8x8/2if |
  |---|---|---|
  | long | 910 of 975 us | 1,335 of 1,650 |
  | ordinary | 220 of 245 | 200 of 265 |
  | paced | 295 of 305 | 580 of 595 |

  GET_AS_PATH's answered read, held as an ordinary record, is 16,500 cycles (175 us) at 1x1/1if, and 14,521 and 14,318 (155 us) at 8x8/2if. Each response is SUCCESS with its eight entries, control_data_length 80. Arm A's refused response is 11,308 cycles.
- **8x8/2if, reported:** AMAP_LIVE_WRITE is 28.82 us, 35 by the rule, over the 30 stated there. It is not restated (Known limitations).

No STOP condition holds: the last queued notice is 136.99 ms within 140, every 1x1/1if row is within its bound, and the load is 0.519 against 0.70.

**The gates at `59c934c6`** (each part on its own fresh clean clone; the 65-suite sweep runs in the manager's merge candidate):

| Gate | Result |
|---|---|
| `rtl-fast`: the firmware jobs | the firmware unit suites PASS; `fw_coverage.py --check` PASS (39 files); the AECP campaign 308 caught, none missed, the nine `face-as-path-*` plants by name; the control campaign 717 of 717, `plat-as-path-unavailable` among them; the SRP campaigns 421 caught; `ctrl_boundary` PASS at both builders |
| `rtl-fast`: every other job and the docs workflow, every `run:` step | every job and `run:` step: 108 ran, 94 not run with a stated reason, 0 bad, and the 19 job clones have no tracked change afterwards. `publication-census`'s step 12 timed out once (sv2v's 900 s, on the shared pool at the host's heaviest load) and passes on its own booked range (0 of 57 rules unproven) |
| the Verilator suites that build the split firmware, each alone as `run_all_suites.sh` runs it | `milan_dp` PASS (4,083 s of its 4,800), `mbx` PASS, `milan_dp_gm_steps` PASS, each with `suite_tally.py --verdict` clean |
| lane gates (45) | 39 at 0; the 4 that exit 1 by design, each refusing the rows it refused at round 6 (8x8/2if's ten; as built at 1x1/1if R4 and last); and the `milan_dp` twin and its plants, identical at `dev-soft-core` `70f4056f` (below). Among the 39: the harness self-test (0 failures, every mutant), `record_classes.py --selftest` (14 of 14 and the port check), `rows_tiers` 1,033 of 1,033, flip 585 of 585, load 26 of 26; `flip_grade.py --check --point 1x1/1if`, `load_grade.py --check`, `tier_grid.py` (900 us); `plat_ledger.py`, the fixtures and `test_ctrl_memory.py`; `docs_check` 0 findings, the em-dash gate against `70f4056f` and `234bc149`, both idiom ratchets; the split boot at every point with its controls and plants; `test_builder.py --require-rv32`; the NVM gate; `behave`; the hooks self-test |
| CPU budget harness legs, one a point and arm (8) | every leg rc 0; every ELF byte-identical to its measurement build |

**A red already on `dev-soft-core`:** the `milan_dp` twin (`make -C tb/verilator/milan_dp twin`, a lane gate no workflow runs) and its plants exit 2. Its owed row `split-talker-failed` still expects the split's Talker Failed for both sources from boot, never withdrawn, the behaviour before #895, and the split now declares and withdraws as #895 makes it. The finding and every plant's verdict are identical at #901's merged head `70f4056f` on a clean clone; the composition does not cause it. For #895's lane (#901).

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

- **Round 6** (`b15da60a`, REVIEW READY issuecomment-6896663632, R833-6 POSITIVE issuecomment-6897027049). R833-5's two MINORs: `record_classes.py` holds arm B's GET_AS_PATH as the answered read, its response's control_data_length 80, and the self-test pins arm B's `path` port to `arm_path.py`'s; the 1x1/1if focus figures receipted; five wording residues.
- **Round 5** (`eca1b9ca`, REVIEW READY issuecomment-6894799910, R833-5 NEGATIVE then answered). The platform's 8x8/2if entry at 60.5 (#901's `8238156d`); GET_AS_PATH's record tracked in arm B's `aecp` group; the probe on AVB_INTERFACE 0; an ordinary AECP record at 1x1/1if restated 245 us and the paced class 305 by the rule; the full pass and the 65-suite sweep.
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
- `flip_grade.py --check --point 1x1/1if` prints `RESULT: PASS` (R4 13.40 ... the last queued notice 136.99 within 140 ... txL 48.77 within 49).
- `load_grade.py --check` prints `HELD 1x1/1if at the pin: the load 0.519, its ceiling 0.70`.
- `tier_grid.py` prints `CHOSEN: slice 900 us, tier 1 aecp-first, tier 2 srp-first, AECP queue, cap 2`.
- The harness self-test reports 0 failures, 250 of 250 mutants caught, among them "build: arm B's path port answers no entries at once, reading no window (earlier rule)".
- `record_classes.py --selftest` prints `record classes: 14 of 14 planted controls refused; the answering-ports arm's path port is arm_path.py's`.
- The answering-ports legs exit 0, GET_AS_PATH answered SUCCESS in `aecp` with control_data_length 80 (16,500 cycles at 1x1/1if on the composed image).
- `record_classes.py` over every one-interface leg prints `RESULT: PASS`.
- `plat_ledger` prints `POINT 8x8-if2: rom 132,064 B ... 60.5 RAMB36 (platform-8x8-two-interfaces) ... PASS`.

## Known limitations / out of scope

- The status of a GET_AS_PATH whose datapath window does not answer is unchanged: ENTITY_MISBEHAVING, as for GET_AVB_INFO, GET_STREAM_INFO and GET_COUNTERS, by the #897 ruling.
- The bench check (#897 acceptance 5) belongs to the bench lane, on the bring-up board.
- The test SoC answers no datapath window, so the measured record reads every word to the contract's bound and fetches no answer's data words. Those 18 reads are bounded, not measured: about 1,080 cycles.
- The answering-every-port arm's `path` still stands in without a read. Its answered notice is measured in a scratch copy of that arm.
- At two interfaces each image's entity model holds one AVB_INTERFACE (the mailbox contract keeps one, `MBX_CTRCHG_AVB_INTERFACE_COUNT`). So a command naming AVB_INTERFACE 1 finds no descriptor: GET_AS_PATH there answered NO_SUCH_DESCRIPTOR in this round's first 8x8 legs. Whether a two-interface entity must hold an AVB_INTERFACE an interface is outside #897's scope, and is raised here for a decision.
- At 8x8/2if, a reported point, AMAP_LIVE_WRITE's take and sinks measure 28.82 us on the composed image, 35 by the rule, over the 30 stated there. It is not restated: a restated 8x8/2if cost moves that point's tx row, and so `CTRL_LOOP_TX_MS` at two interfaces and a withdrawn Talker's hold-off. For #894's 8x8 lane and #890.
- The face carries a path of up to `AECP_PATH_ITEMS`, 64 entries, the core's capacity since `a008ea92` (before this branch). A 64-entry response would have a control_data_length of 528, past IEEE 1722.1-2021 9.2.2.6's 524, so the largest legal count is 63. The shipped datapath serves at most 8, so no image reaches it.
- No executable check runs the firmware's kind 2 read against the split RTL itself (R834-1). `Boot.B11` runs the composed split against its datapath model.
- The composed #901 and #898 platform image at 8x8/2if is 132,064 B, within the 133,120 B ruling item 3 grades it against (1,056 B left at 60.5). The size fixture's entry there is 59.5, as S14 debt, for the harness arms on it.

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
