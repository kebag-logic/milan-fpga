[A776]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Round 3: composed with #902 (the control loop's tiers)](#round-3-composed-with-902-the-control-loops-tiers)** -- The sync merges, the 1x1/1if flip check, GET_AS_PATH's cost in the rows, the ROM ledger and the deltas against #902.
- **[Round 2: the sync onto dev-soft-core after #810](#round-2-the-sync-onto-dev-soft-core-after-810)** -- The earlier merge, kept as its record.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN (round 3) at head `f098f893d57e0fa3ec95a7e459313c5cfe4f4224`, `897-split-as-path` -> `dev-soft-core`, composed with #902 (`894-tiers`, not merged) by two sync merges: `5b264bf2`, then `7398ec0a` when #902's round 10 reached `894-tiers` during the round. **The 1x1/1if flip check, composed with #902, passes**: every row by every source, with #902's figures unchanged, and the 1x1/1if load is 0.513 against 0.70. GET_AS_PATH's cost in the rows is measured or bounded within every stated cost it enters, so no stated cost moves. Every ROM point is within its cap. The full pass ran once on this head, each part on its own fresh clean clone: every step of every workflow job a pull request to `dev-soft-core` triggers (139 ran, 226 not run with a stated reason, 0 bad); the full Verilator sweep (65 suites, 0 failed, 0 timed out); the lane's own gates; and the CPU budget harness's legs at both points.

Campaigns at this head: AECP 283 of 283 caught, control 717 of 717 caught, SRP 345 caught with none escaped. This PR's nine AECP plants (now in `aecp_face_mutants.py`) and its platform plant are each caught by name.

## Linked Issue / roles

Relates to #897
Relates to #665
Relates to #894

Executor: `[A776]`
Internal cleared-context reviewer: `[R833]` (round 1, POSITIVE at `5e6fef3e`; round 2, R833-2, POSITIVE at `3bebf03a`, PR #898 issuecomment-6864287713); round 3 as the manager assigns it
External reviewer: `[R834]` (round 1, POSITIVE at `5e6fef3e`); round 2 was a merge-only delta with one reviewer, by the manager's assignment; round 3 as the manager assigns it

## Description

The Mark II split answered GET_AS_PATH with ENTITY_MISBEHAVING: the platform's `path()` was a stub that always failed, and the AECP face forwarded to it. The face now reads the path through the datapath's GSI window, kind 2, as it already reads GET_AVB_INFO's words.

| Piece | Change |
|---|---|
| `sw/firmware/ctrl/aecp/aecp_face.c` `path()` | the count at kind 2 selector 0, then each `path_sequence` ClockIdentity at selector 8 by its ordinal, through the AVB interface's own window; a count past the core's capacity (`AECP_PATH_ITEMS`) fails the port at the count, reading no entry; a word with no answer fails the port there, as for GET_AVB_INFO |
| `sw/firmware/ctrl/plat/ctrl_plat.c` | the unavailable stub removed; the platform supplies `random` only (and, since #902, the owed-notice queue's slots at one interface) |
| `sw/firmware/ctrl/test/ctrl_aecp_image.c` | the size fixture's stub removed, so the fixture links the same read |
| AS_PATH_CHANGED | already led to the unsolicited GET_AS_PATH response (`ctrl_app_aecp.c`, Table 5.22 bit 2); it now carries the datapath's sequence, tested |
| `tb/verilator/ctrl_service_budget/build.py` | the `answering-ports` and `answering-every-port` arms put their answering port in the face's `path` port, as they did through the removed stub |
| docs | `sw/firmware/ctrl/plat/README.md`, `sw/firmware/ctrl/aecp/README.md`, `aecp_face.h`, `docs/design/MAILBOX_SPLIT.md` (the writer section and the host tests' row), `docs/design/SPLIT_CONTROL_MEMORY.md` sections 5, 6 and 13 (the images' sizes; GET_AS_PATH's cost in the rows), the harness README, the split boot README |

The split datapath serves kind 2 (`hdl/milan/milan_datapath.sv`, `g_sp_ctrl` and the GSI answer block): the count from a snapshot taken at the count's request, the entries from that snapshot, at most eight (`KL_gptp_engine.sv` clamps the pathTrace count to 8), so one response carries one sequence. No RTL and no mailbox contract change.

A datapath window that does not answer keeps ENTITY_MISBEHAVING, as GET_AVB_INFO's, GET_STREAM_INFO's and GET_COUNTERS' do (the #897 ruling, option (a)).

New tests (each named by a planted defect that it kills by its own words):

| Test | Rule | Plants |
|---|---|---|
| `Face.AsPathIsTheDatapathsSequenceThroughItsOwnWindow` | SUCCESS at 0, 1, 3 and 8 entries on every interface, the count and entries in order, cdl 16 + 8 an entry, the count at selector 0 then each entry at selector 8 by its ordinal, through the interface's own window | count read as kind 1; every entry at ordinal 0; the count through interface 0 |
| `Face.AsPathCarriesItsWholeBoundAndFailsACountPastIt` | `AECP_PATH_ITEMS` carried whole; a count past it, or past the caller's capacity, fails the port at the count | the count clamped and carried; `>=` for `>` |
| `Face.AnUnansweredAsPathWordFailsItsPortThere` | a window with no answer at the count or any entry fails the port at that word, counted unanswered | the count's failure ignored; an entry's failure ignored |
| `AppFace.AnAsPathChangeNotifiesTheDatapathsSequence` | AS_PATH_CHANGED sends the registered controller a SUCCESS GET_AS_PATH carrying the sequence the datapath serves, through the changed interface's window | the event marks bit 1; the notice for AVB_INTERFACE 0 |
| `Boot.B11GetAsPathAnswersTheDatapathsSequence` | the composed split answers GET_AS_PATH SUCCESS with the datapath's sequence, at one and two interfaces | the old stub's answer restored |

## Round 3: composed with #902 (the control loop's tiers)

#894's ruling issuecomment-6867393730, item (d): this PR must pass the 1x1/1if flip check as composed with #902, or wait behind the flip. #902 (`894-tiers`) has not merged, so this round composes with its branch head.

| Commit | What |
|---|---|
| `e45981f8` | `Merge 894-tiers 5b264bf2`: one merge commit, parents `3bebf03a` (round 2's head) and `5b264bf2` (#902's head) |
| `417f44af` | `sw/firmware/gtest/coverage.ratchet`: `ctrl_plat.c` recorded at 132 of 132 lines, as `fw_coverage.py --write` measures the composed tree |
| `25ea917f` | `SPLIT_CONTROL_MEMORY.md` section 5 (the images' sizes at the composed head; the paragraph no longer opens "At this branch's head", R833-2 F1), the harness arm's table (the composed `answering-every-port` arm), and section 13's new "GET_AS_PATH through the face" (its cost in the rows) |
| `a3a509d7` | `Merge 894-tiers 7398ec0a`: the second sync merge, parents `25ea917f` and `7398ec0a` (#902's round 10), which reached `894-tiers` during this round; no conflict |
| `f098f893` | `sw/firmware/ctrl/test/aecp_face_mutants.py`: the nine GET_AS_PATH face plants in their own module, so `aecp_mutants.py` stays within the 1,000-line module limit at the composition |

**The merge.** `dev-soft-core` is still `cec88385`, the merge base of both branches. Thirteen files changed on both sides. Four conflicted, and each kept both sides:

- `sw/firmware/ctrl/plat/ctrl_plat.c`, `compose`: #902's `#if AECP_MBX_OWED_SLOTS != 0u` block (the owed-notice slots and queue at one interface), then this branch's `aecp_platform` with no `.path`, since the stub stays removed.
- `sw/firmware/gtest/coverage.ratchet`, the `ctrl_plat.c` row: 100 % on both sides; `417f44af` records the composed tree's measured 132/132.
- `sw/firmware/ctrl/plat/README.md` and `SPLIT_CONTROL_MEMORY.md` section 6: both sides moved the platform's 8x8/2if plan from 59.5 to 60.0; this branch's line, which adds that half a tile more is refused, was kept. It still holds: that image needs 130,816 B of `rom` in 131,072.

The other nine merged without a conflict (`MAILBOX_SPLIT.md`, the AECP README, `aecp_mutants.py`, `ctrl_aecp_image.c`, `test_aecp.cpp`, the harness's `README.md`, `build.py` and `run.py`, and the split boot README, which both sides edited identically). For each of this branch's 17 files, the merge's diff from `5b264bf2` is exactly this branch's diff from `cec88385`, and for each of #902's 85 files the merge's diff from `3bebf03a` is exactly #902's from `cec88385`; the only lines not carried verbatim are the four rows above. No gitlink changes on either side, and #902 changes no RTL and no workflow.

**The second merge.** `894-tiers` moved from `5b264bf2` to `7398ec0a` at 09:30 (#902's round 10: the map table's assertion and its campaign control, section 13's current rows, a comment; no image change), with `dev-soft-core` still `cec88385`. It was merged again before the full pass, with no conflict: every file of both sides is carried exactly. The merged tree is byte-identical, image for image, to the composition with `5b264bf2`: the size fixture's and the platform's ELF at the four points have the same sha256, so every measurement above stands for this head.

**The composition's own red** (as in round 2): `scripts/check_py_idiom.py` refused the merge with "long module 11 > ratchet 10". `aecp_mutants.py` is 963 lines at `5b264bf2`, 999 with this branch's nine plants, 976 with #902's round 10, and 1,012 composed, past the 1,000-line limit. `f098f893` moves the nine plants, unchanged, into `aecp_face_mutants.py` as rows, the pattern of #902's own `aecp_map_mutants.py` and `aecp_owed_mutants.py`. The campaign's 283 defects are the same in every field (name, file, anchor, replacement, named checks), and `aecp_mutants.py` is 977 lines.

**The 1x1/1if flip check, composed.** `flip_grade.py --check --point 1x1/1if`: **RESULT: PASS**, every row by every source, with #902's figures at `5b264bf2` unchanged:

| R4 (20) | R4L (238) | ACMP (30) | ADP (30) | MAAP (30) | First (20) | R5 (90) | R6 (90) | Last (130) | tx (49) | txL (49) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 12.85 | 188.39 | 28.44 | 26.83 | 26.95 | 14.51 | 72.91 | 68.80 | 126.46 | 29.86 | 48.09 |

The load gate holds 1x1/1if at **0.513** at the pin and 0.509 with tsn-c-stack#32, against 0.70 (`load_grade.py --check`). The flip check over both points, at 8x8/2if, and as built at 1x1/1if, `rows_tiers.py --terms` and `tier_grid.py --point 1x1/1if` print the same output at `5b264bf2` and at the composed head; the first four exit 1 by design (8x8/2if's rows are reported, not held), `tier_grid.py` exits 0.

**GET_AS_PATH's cost in the rows.** Before this branch the `path` port answered false at once. Now each GET_AS_PATH reads its interface's GSI window, the count and then each entry, every word a bounded window read (`mbx_win_read`, `MBX_WIN_GSI_WAIT_CYCLES`). The shipped datapath serves at most eight entries, so a read is at most nine words. That cost enters three of the rows' terms, each measured or bounded at 1x1/1if on the composed tree:

| Term | Stated | Measured or bounded | How |
|---|---:|---|---|
| AS_PATH_CHANGED's take and sinks (`rows_tiers.DATAPATH_US`) | 35 us | 30.02 us (31.57 at `5b264bf2`); AVB_INFO_CHANGED 30.64 (30.55), AMAP_LIVE_WRITE 23.34 (25.51). At 8x8/2if 32.87, 35.23 and 22.16 (32.79, 35.76, 22.65), within 40, 40, 25 | `datapath-events` at both heads; the sink marks the notice and reads nothing |
| its notice in THE RETRY's rounds (`AECP_ROUND_COLD_US` + n x `AECP_NOTICE_US` + k x `AECP_ATTEMPT_US`) | 85 + n x 255 + k x 34 us | unanswered (arm A): one GSI word an attempt, 378 to 796 CPU cycles, and no round over its stated cost; answered with eight entries (a scratch arm, below): the round that builds it 46,397 and 47,490 cycles against the 59,500 it is admitted at (a cold start, two notices) | `round_grade.py` in every leg; a scratch build tracing `mbx_win_read` |
| a GET_AS_PATH command's record (`record.aecp`) | 235 us | no group sends one; bounded at about 19,950 cycles, 200 us: GET_AVB_INFO's record in arm A (the same handler, one unanswered word) 11,655 cycles, eight words more at the most a word took (877), their two data words each at the most a mailbox read took (60), and the 64 B of entries | arm A's `aecp` group record spans |

No group answers the datapath's windows (the test SoC holds them idle) and the answering arms' stand-ins read none, so the answered read was measured in a scratch copy of the `answering-every-port` arm, never committed: its `path` reads the count and eight entries, each word to the contract's whole bound, and answers the eight. In `notice-every-0` and `notice-burst-0` no round, notice or pass is over its bound, and every notice commits within 19.5 ms of its port's answer, against 130.

So no stated cost moves, and the rows and the load are #902's. Every measured input of the composed legs is within its stated cost: the largest legal command's record is 91,231 CPU cycles at 1x1/1if (91,625 at `5b264bf2`; 975 us stated) and 156,972 on the 8x8 shape (156,716; 1,650 us). THE TRANSMIT's build of one is 69,269 cycles at 1x1/1if (68,937), within the 725 us `CTRL_LOOP_BUILD_ONE_PASS_US` states; by the stating rule (+5 %, up to 5 us) it would be 730 us, and the rows solved at 730 us in a scratch tree still pass, each moving by at most 0.01 ms (txL 48.10 within 49).

**The data placement (#909).** Every writable symbol (`.data`, `.bss`, the stack) of every image, the size fixture's and the platform's at the four points and the harness's arm A and `answering-ports` arm at 1x1/1if, has the same address and size at the composed head as at `5b264bf2`: GET_AS_PATH adds `rom` only, so it moves no object in the data cache. (The `answering-every-port` test arm swaps two of its own statics.)

**ROM ledger, every point, against `5b264bf2`** (`plat_ledger.py --self-test`: 7 of 7 controls, `plat_ledger: PASS`; the size fixture linked on the same runtime and flash maps; the harness arms freshly built):

| Image, point | `5b264bf2` -> composed, `rom` B | RAMB36 | Cap | Margin |
|---|---|---|---:|---|
| fixture 1x1/1if | 110,576 -> 110,904 (+328) | 40.5 -> 41.0 | 56 | |
| fixture 1x1/2if | 111,872 -> 112,192 (+320) | 41.5 | 56 | |
| fixture 8x8/1if | 124,104 -> 124,424 (+320) | 54.0 | 56 | |
| fixture 8x8/2if | 125,368 -> 125,688 (+320) | 59.0 | 59.0, #902's entry | 1,288 B before 126,976 |
| platform 1x1/1if | 115,640 -> 115,952 (+312) | 42.5 | 56 | |
| platform 1x1/2if | 116,952 -> 117,264 (+312) | 43.5 | 56 | |
| platform 8x8/1if | 129,208 -> 129,520 (+312) | 56.0 | 56 | 1,552 B before 131,072 |
| platform 8x8/2if | 130,504 -> 130,816 (+312) | 60.0 | 60.5 (its entry 60.0) | 256 B before 131,072 |
| harness arm A, 8x8/2if | 125,368 -> 125,688 (+320) | 59.0 | 59.0 | 1,288 B |
| harness `answering-ports`, 8x8/2if | 125,528 -> 125,872 (+344) | 59.0 | 59.0 | 1,104 B |
| harness `answering-every-port`, 8x8/2if | 125,676 -> 126,012 (+336) | 59.0 | 59.0 | 964 B |
| harness arm A / `answering-ports` / `answering-every-port`, 1x1/1if | 110,576 / 110,744 / 110,884 -> 110,904 / 111,088 / 111,220 | 40.5 / 41.0 / 41.0 -> 41.0 each | 56 | |

`sram` and `ctrl_plat` are unchanged at every point. One plan moves by half a tile: the fixture's shipping image, which had 16 B left in its banks at `5b264bf2`, takes another 2 KiB granule (41.0, within 56). The platform's 8x8/1if image, which has no tile to spare, stays at 56.0 with 1,552 B before its next granule. Nothing is over its cap.

**The harness legs at both heads** (fresh builds of `5b264bf2` and of the composed head, the legs #902's round 9 ran, recorded with `--record-budget-findings --record-share-findings`):

- 1x1, arm A (`datapath-events`, `aecp-largest-notice`, `backlog-owed`, `srp`, `aecp`, `aecp-fanout`, `acmp-cmd`): exit 0 at both. No `STATED` line. The join intervals are 187.958 to 190.027 ms against 181.0 to 239.0, none late or absent. The same seven `backlog-owed` probe budgets are recorded over their 20 ms at both heads (61.5 to 63.6 ms, #902's: the egress-held paths of tsn-c-stack #26).
- 1x1, `answering-every-port` (`notice-every-0`, `notice-burst-0`) and `answering-ports` (`aecp`): exit 0 at both, with 0 misses of any kind.
- 8x8, arm A (the same groups but `aecp-largest-notice`, which runs in `answering-ports` there): exit 1 at both, on `srp`'s build of one alone (138,998 and 149,156 cycles here, 138,054 and 147,814 at `5b264bf2`, against 121,500: #910's debt, reported). The difference is the code's place in the instruction cache: SRP's code and every data object are unchanged.
- 8x8, `answering-every-port` and `answering-ports` (`aecp`, `aecp-largest-notice`): exit 0 at both. The same two `aecp-largest-notice` passes are over THE SHARE at both heads (255,281 cycles here, 254,919 there; #902's reported 8x8 condition).

**The full pass, once, at `f098f893`** (each part on its own fresh clean clone):

| Gate | Result |
|---|---|
| every workflow job a PR to `dev-soft-core` triggers, every `run:` step (`rtl-fast`, `docs`, `elaborate`, `rtl` with its four yosys shards) | 139 steps ran, 226 not run with a stated reason, 0 bad; 28 job clones at the head with no tracked change |
| AECP campaign | 283 caught of 283; the nine `face-as-path-*` plants each caught by its named test |
| control campaign | 717 of 717 caught; `plat-as-path-unavailable` caught by `platboot1` and `platboot2` |
| SRP campaign | 345 caught, none escaped |
| firmware self-test, coverage | PASS in its four shards; `fw_coverage.py --check` PASS, 39 files (`aecp_face.c` 179/179 lines, 160/160 branches; `ctrl_plat.c` at 100 %, its ratchet row 132/132) |
| firmware boundary | `ctrl_boundary: PASS` |
| lane gates | 40 at 0, and the 4 that exit 1 by design (the flip check over both points, at 8x8/2if and as built at 1x1/1if, and the tier model's report over both points), with output identical to `5b264bf2`'s; among them `flip_grade.py --check --point 1x1/1if` 0, `load_grade.py --check` 0, `tier_grid.py --point 1x1/1if` 0, `check_py_idiom.py` 0, `check_cpp_idiom.py` 0, `docs_check.py` 0 findings, the em-dash gate against `cec88385` and `5b264bf2`, `plat_ledger.py --self-test` (7 of 7 controls), the split boot ready at 1x1/1if, 8x8/1if and 8x8/2if (26.911, 66.436 and 68.576 ms against 20,000), 6 of 6 native controls, 8 of 8 placement controls and 3 of 3 plants, `test_builder.py --require-rv32`, the NVM gate (526 tests, 144 plants reddened), `behave` (511 scenarios, 2,346 steps, 0 failed), the twin (0 findings) and its plants |
| CPU budget harness legs | every image byte-identical to its measurement build; every leg rc 0 but 8x8 `srp`'s, on #910's build of one as at `5b264bf2` |
| full Verilator sweep | 65 suites (15, 17, 17 and 16 a shard, each shard on its own booked CPU range): 65 passed, 0 failed, 0 timed out; 2,713,040 checks, 0 in-suite failures |

## Round 2: the sync onto dev-soft-core after #810

| Commit | What |
|---|---|
| `d3202fa2` | `Merge dev-soft-core cec88385`: one merge commit, parents `5e6fef3e` (round 1's head) and `cec88385` |
| `d395f682` | `SPLIT_CONTROL_MEMORY.md` sections 5 and 6, the plat README and the split boot README: the images' sizes at the composed head |
| `3bebf03a` | `tb/verilator/ctrl_service_budget/build.py` held within the 1,000-line module limit: the arms' comment rewrapped, five lines to four, the same words |

Two docs files conflicted and each kept both sides; for every one of this branch's 16 files the merge's diff from `cec88385` was exactly this branch's diff from `7f50ee6a`. The three gates red at round 1's base (the C/C++ idiom ratchet, the hooks self-test, the firmware boundary) were green on that composed tree, and `3bebf03a` fixed the composition's own py-idiom red. R833-2 reviewed that head POSITIVE.

## Authoritative references

- IEEE 1722.1-2021 7.4.41 (GET_AS_PATH command and response), 9.2.2.6 (control_data_length), 9.3.2.5 and Table 7-141 (status codes), 9.3.2.6 (timeouts, IN_PROGRESS)
- Milan v1.2 5.4.1 (response length), 5.4.2.24 (GET_AS_PATH), 5.4.5.2 Table 5.22 (the unsolicited GET_AS_PATH)
- `sw/firmware/ctrl/mbx/mbx_contract.h`: `MBX_FACE_REG_GSI_SEL` (kind 2 GET_AS_PATH, selector, ordinal), `MBX_WIN_GSI_WAIT_CYCLES`, `MBX_EV_TYPE_AS_PATH_CHANGED`
- `docs/design/MAILBOX_SPLIT.md`, class R (the GSI window) and class E (the face events)
- protocol-processor `docs/architecture/06_aecp_engine.md` 6.10 (the gather face's kind 2 word table)
- #897 ruling (issuecomment-6828659285, option (a)): an unanswering datapath window keeps ENTITY_MISBEHAVING
- #894 rulings issuecomment-6867393730 (item (d): the 1x1/1if flip check composed with #902), issuecomment-6867990126 (MRPDU 49 ms, paced R4L 238 ms, the harness join gate 181.0 to 239.0 ms), issuecomment-6870437042 (the map table as a direct index)
- #665 owner decision 2026-11-12 (issuecomment-6824896581) and #894 issuecomment-6844175391, item 2 (the ROM caps and entries: the platform's 60.0 refused at 60.5, the size fixture's 59.0)

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
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --check
python3 -B scripts/check_cpp_idiom.py
python3 -B scripts/check_py_idiom.py
python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir "$OUT/plat-ledger" --self-test
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$OUT/8x8-if2" --shape endstation_ax7101_8x8 --interfaces 2
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$OUT/budget-1x1" --groups datapath-events,aecp-largest-notice,backlog-owed,srp,aecp,aecp-fanout,acmp-cmd --record-budget-findings --record-share-findings
python3 sw/builder/test_builder.py --require-rv32
python3 scripts/docs_check.py
(cd tests && behave)
```

Expected result / pass criteria: every command exits 0.
- `flip_grade.py --check --point 1x1/1if` prints `RESULT: PASS` (R4 12.85 ... txL 48.09 within 49).
- `load_grade.py --check` prints `HELD 1x1/1if at the pin: the load 0.513, its ceiling 0.70`.
- The AECP campaign catches 283 of 283, the nine `face-as-path-*` plants by name. The control campaign catches 717 of 717, `plat-as-path-unavailable` among them. `aecp_face.c` stays at 100 % of lines and branches.
- `plat_ledger` prints `POINT 8x8-if2: rom 130,816 B ... 60 RAMB36 (platform-8x8-two-interfaces) ... PASS`.
- The split boot reaches ready at each point.
- The harness leg exits 0 with no `STATED` line. It records the seven `backlog-owed` probe budgets #902's own legs record: the egress-held paths of tsn-c-stack #26.

## Known limitations / out of scope

- The status of a GET_AS_PATH whose datapath window does not answer is unchanged: ENTITY_MISBEHAVING, as for GET_AVB_INFO, GET_STREAM_INFO and GET_COUNTERS, by the #897 ruling.
- The bench check (#897 acceptance 5) belongs to the bench lane, on the bring-up board.
- No CPU budget harness group answers the datapath's windows: the test SoC holds them idle, and the answering arms' stand-ins read none. GET_AS_PATH's answered read (at most nine words) was measured in a scratch arm (never committed), and its command's record is bounded, not measured. The same holds for every observation: GET_STREAM_INFO's answered read is six window words, GET_AVB_INFO's three and GET_COUNTERS' 33, each at up to about 880 CPU cycles a word, and no stated notice or record cost includes them. That is #894's model as it stands at `7398ec0a`, not a change here; GET_COUNTERS' is the largest.
- The face carries a path of up to `AECP_PATH_ITEMS`, 64 entries, the core's capacity since `a008ea92` (before this branch). A 64-entry response would have a control_data_length of 528, past IEEE 1722.1-2021 9.2.2.6's 524, so the largest legal count is 63. The shipped datapath serves at most 8 (`KL_gptp_engine.sv` clamps the pathTrace count), so no image reaches it.
- #902's section 13 still says, in the present tense, that the 1x1/1if size fixture is 110,400 B and 40.5 RAMB36 (its round-9 text, not changed by its round 10). It is 110,576 B at `5b264bf2` and 110,904 B, 41.0, here; section 5 states the composed figures. Left to #902.
- #902's `coverage.ratchet` rows for `aecp.c`, `aecp_maps.c` and `aecp_mbx.c` are behind their measurement on the composed tree (611 to 615, 223 to 267 and 132 to 136 lines), all at 100 %, so the ratchet passes. Only `ctrl_plat.c`'s row, which both sides edited, is recorded here.
- At 8x8/2if THE TRANSMIT's build of one is 138,998 and 149,156 CPU cycles here, against 138,054 and 147,814 at `5b264bf2`; both are over its 121,500 (#910, reported, not held). SRP's code and every data object are unchanged, so the difference is the code's place in the instruction cache. At 1x1/1if the same build is 69,269 cycles (68,937 at `5b264bf2`), within the 725 us `CTRL_LOOP_BUILD_ONE_PASS_US` states.
- `flip_grade.py --check` over both points, at 8x8/2if and as built at 1x1/1if exits 1 by design (8x8/2if's rows are reported, not held), with output identical to `5b264bf2`'s.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (acceptance 1-4, acceptance 3 as amended by the ruling; acceptance 5 belongs to the bench lane)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive (round 1 at `5e6fef3e` and round 2 at `3bebf03a` were; round 3 is to be reviewed)
- [ ] External review is positive (round 1 at `5e6fef3e` was; round 3 is to be reviewed)
- [x] Blocking and major findings are fixed and re-reviewed (rounds 1 and 2 had none)
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
