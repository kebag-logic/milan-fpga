[A776]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Round 2: the sync onto dev-soft-core after #810](#round-2-the-sync-onto-dev-soft-core-after-810)** — The merge, its conflicts, the base reds, the ROM ledger and the load.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN (round 2) at head `3bebf03a1d25bcbde9c0ec48dfd711af7280131e`, `897-split-as-path` -> `dev-soft-core`, synced onto `dev-soft-core` `cec88385` (#810 merged) with one merge commit. The clean-clone pass ran once on this head: every step of every workflow job a pull request to `dev-soft-core` triggers, each job on its own fresh clean clone (139 steps ran, 226 not run with a stated reason, 0 bad), the full Verilator sweep as four shards (65 suites, 0 failed: 62 passed in the sweep, and the 3 that the sweep's wall clock killed under CPU contention, milan_dp, milan_dp_render and mmcm_servo, passed when re-run alone), the lane's own gates, the split boot simulation to ready at 1x1/1if, 8x8/1if and 8x8/2if, and the CPU budget harness at both points. The three gates red at round 1's base (the C/C++ idiom ratchet, the hooks self-test, the firmware boundary) are green on the composed tree. Every ROM point is within its cap and the 1x1/1if load is 0.501 against 0.70, unchanged from `cec88385`.

Campaigns at this head: AECP 236 of 236 caught, control 699 of 699 caught, SRP 340 ok with none escaped; this PR's nine AECP plants and its platform plant are each caught by name.

## Linked Issue / roles

Relates to #897
Relates to #665

Executor: `[A776]`
Internal cleared-context reviewer: `[R833]` (round 1, POSITIVE at `5e6fef3e`); round 2 to be assigned
External reviewer: `[R834]` (round 1, POSITIVE at `5e6fef3e`); round 2 to be assigned

## Description

The Mark II split answered GET_AS_PATH with ENTITY_MISBEHAVING: the platform's `path()` was a stub that always failed, and the AECP face forwarded to it. The face now reads the path through the datapath's GSI window, kind 2, as it already reads GET_AVB_INFO's words.

| Piece | Change |
|---|---|
| `sw/firmware/ctrl/aecp/aecp_face.c` `path()` | the count at kind 2 selector 0, then each `path_sequence` ClockIdentity at selector 8 by its ordinal, through the AVB interface's own window; a count past the core's capacity (`AECP_PATH_ITEMS`) fails the port at the count, reading no entry; a word with no answer fails the port there, as for GET_AVB_INFO |
| `sw/firmware/ctrl/plat/ctrl_plat.c` | the unavailable stub removed; the platform supplies `random` only |
| `sw/firmware/ctrl/test/ctrl_aecp_image.c` | the size fixture's stub removed, so the fixture links the same read |
| AS_PATH_CHANGED | already led to the unsolicited GET_AS_PATH response (`ctrl_app_aecp.c`, Table 5.22 bit 2); it now carries the datapath's sequence, tested |
| `tb/verilator/ctrl_service_budget/build.py` | the `answering-ports` and `answering-every-port` arms put their answering port in the face's `path` port, as they did through the removed stub |
| docs | `sw/firmware/ctrl/plat/README.md`, `sw/firmware/ctrl/aecp/README.md`, `aecp_face.h`, `docs/design/MAILBOX_SPLIT.md` (the writer section and the host tests' row), `docs/design/SPLIT_CONTROL_MEMORY.md` sections 5 and 6 (the images' sizes), the harness README, the split boot README |

The split datapath serves kind 2 (`hdl/milan/milan_datapath.sv`, `g_sp_ctrl` and the GSI answer block): the count from a snapshot taken at the count's request, the entries from that snapshot, at most eight, so one response carries one sequence. No RTL and no mailbox contract change.

A datapath window that does not answer keeps ENTITY_MISBEHAVING, as GET_AVB_INFO's, GET_STREAM_INFO's and GET_COUNTERS' do (the #897 ruling, option (a)).

New tests (each named by a planted defect that it kills by its own words):

| Test | Rule | Plants |
|---|---|---|
| `Face.AsPathIsTheDatapathsSequenceThroughItsOwnWindow` | SUCCESS at 0, 1, 3 and 8 entries on every interface, the count and entries in order, cdl 16 + 8 an entry, the count at selector 0 then each entry at selector 8 by its ordinal, through the interface's own window | count read as kind 1; every entry at ordinal 0; the count through interface 0 |
| `Face.AsPathCarriesItsWholeBoundAndFailsACountPastIt` | `AECP_PATH_ITEMS` carried whole; a count past it, or past the caller's capacity, fails the port at the count | the count clamped and carried; `>=` for `>` |
| `Face.AnUnansweredAsPathWordFailsItsPortThere` | a window with no answer at the count or any entry fails the port at that word, counted unanswered | the count's failure ignored; an entry's failure ignored |
| `AppFace.AnAsPathChangeNotifiesTheDatapathsSequence` | AS_PATH_CHANGED sends the registered controller a SUCCESS GET_AS_PATH carrying the sequence the datapath serves, through the changed interface's window | the event marks bit 1; the notice for AVB_INTERFACE 0 |
| `Boot.B11GetAsPathAnswersTheDatapathsSequence` | the composed split answers GET_AS_PATH SUCCESS with the datapath's sequence, at one and two interfaces | the old stub's answer restored |

## Round 2: the sync onto dev-soft-core after #810

| Commit | What |
|---|---|
| `d3202fa2` | `Merge dev-soft-core cec88385`: one merge commit, parents `5e6fef3e` (round 1's head) and `cec88385` |
| `d395f682` | `SPLIT_CONTROL_MEMORY.md` sections 5 and 6, the plat README and the split boot README: the images' sizes at the composed head |
| `3bebf03a` | `tb/verilator/ctrl_service_budget/build.py` held within the 1,000-line module limit: the arms' comment rewrapped, five lines to four, the same words |

**The merge.** Eight files changed on both sides since the merge base `7f50ee6a`. Two conflicted, both in docs, and each kept both sides:

- `docs/design/MAILBOX_SPLIT.md`, the host tests' table: this branch's AECP-face row (the GET_AS_PATH tests) and `dev-soft-core`'s planted-defects row (twelve `mutants.py` arms in the default `make`).
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 5: `dev-soft-core`'s platform paragraph (the 60.0 entry, `plat_ledger.py`) and harness-arm paragraph (the 58.5 cap), with this branch's GET_AS_PATH paragraph; `d395f682` then restates that paragraph at the composed head.

The other six (`plat/README.md`, `test_aecp.cpp`, `coverage.ratchet`, and the harness's `build.py`, `run.py` and `README.md`) merged cleanly. For every one of this branch's 16 files, the merge's diff from `cec88385` is exactly this branch's diff from `7f50ee6a`, and the merged tree differs from `cec88385` in those 16 files only. The submodule pins are unchanged.

**The base reds**, red at round 1's base and fixed by #810's later commits, are green at the composed head:

| Gate | Command | rc |
|---|---|---:|
| C/C++ idiom ratchet | `python3 -B scripts/check_cpp_idiom.py` (and docs-gates-0's gate_38) | 0 ("multi-declarator declaration: 0 <= 0") |
| hooks self-test | `python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test` | 0 (28 of 28 checks, 96 of 96 mutants caught) |
| firmware boundary | the `firmware-boundary` job's steps; step 9 `ctrl_boundary` | 0 ("ctrl_boundary: PASS", 0 findings) |

The composition had a red of its own: `scripts/check_py_idiom.py` failed with "long module 11 > ratchet 10", because `build.py` is exactly 1,000 lines at `cec88385` and this branch's change made it 1,001. `3bebf03a` rewraps the comment and changes no generated code; the harness images at `3bebf03a` are byte-identical (their ELF digests) to those at the merge.

**ROM ledger** (`plat_ledger.py --self-test` for the platform, the size fixture linked on its runtime and flash maps; `rom` B, RAMB36):

| Point | Fixture, `cec88385` -> this head | Platform, `cec88385` -> this head | Cap |
|---|---|---|---:|
| 1x1/1if | 108,600 -> 108,920 (+320), 38.5 | 113,672 -> 113,984 (+312), 39.5 | 56 |
| 1x1/2if | 110,304 -> 110,624 (+320), 41.0 -> 41.5 | 115,400 -> 115,712 (+312), 43.0 | 56 |
| 8x8/1if | 122,136 -> 122,464 (+328), 51.5 | 127,256 -> 127,568 (+312), 53.0 | 56 |
| 8x8/2if | 123,808 -> 124,136 (+328), 58.5, 792 B before its next granule | 128,960 -> 129,272 (+312), 59.5 -> 60.0, its entry's tiles | fixture 58.5, platform 60.5 |

`sram` and `ctrl_plat` are unchanged at every point, and `plat_ledger: PASS` holds at every point with its seven planted ledgers refused as required. The CPU budget harness's arms at 8x8/2if, freshly built at this head, all plan 58.5 against their 58.5 cap: arm A 124,136 B (+328), `answering-ports` 124,320 B (+344), `answering-every-port` 124,452 B (+336, 476 B under 124,928). At 1x1/1if they plan 38.5. Nothing is over its cap. The platform's 8x8/2if entry is now fully used, as the fixture's already was: a granule more of either region at that point plans 60.5, which the entry refuses.

**Load.** `load_grade.py --check`: 1x1/1if 0.501 at the pin and 0.499 with tsn-c-stack#32, against a ceiling of 0.70, at `cec88385` and at this head alike (delta 0.000; the stated tables are unchanged). The harness at both points ran on fresh builds at this head and at `cec88385`: arm A's `aecp`, `aecp-fanout` and `acmp-cmd`, `answering-ports`' `aecp` and `answering-every-port`'s `notice-burst-0`. At both heads that gave 0 refusals, 0 budget misses, 0 share misses and 0 notice misses. Each path's worst instance moves by layout effects of at most a few percent of its bound either way.

## Authoritative references

- IEEE 1722.1-2021 7.4.41 (GET_AS_PATH command and response), 9.3.2.5 and Table 7-141 (status codes), 9.3.2.6 (timeouts, IN_PROGRESS)
- Milan v1.2 5.4.1 (response length), 5.4.2.24 (GET_AS_PATH), 5.4.5.2 Table 5.22 (the unsolicited GET_AS_PATH)
- `sw/firmware/ctrl/mbx/mbx_contract.h`: `MBX_FACE_REG_GSI_SEL` (kind 2 GET_AS_PATH, selector, ordinal), `MBX_EV_TYPE_AS_PATH_CHANGED`
- `docs/design/MAILBOX_SPLIT.md`, class R (the GSI window) and class E (the face events)
- protocol-processor `docs/architecture/06_aecp_engine.md` 6.10 (the gather face's kind 2 word table)
- #897 ruling (issuecomment-6828659285, option (a)): an unanswering datapath window keeps ENTITY_MISBEHAVING
- #665 owner decision 2026-11-12 (issuecomment-6824896581), the #895 ruling (issuecomment-6824623445) and the round 30 ruling (#665 issuecomment-6831583372): the ROM caps and entries

## How to get into the same state

```sh
git fetch origin
git checkout 897-split-as-path
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --check
python3 -B scripts/check_cpp_idiom.py
python3 -B scripts/check_py_idiom.py
python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test
python3 tb/verilator/ctrl_service_budget/run.py --self-test
python3 tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir "$OUT/plat-ledger" --self-test
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$OUT/8x8-if2" --shape endstation_ax7101_8x8 --interfaces 2
python3 sw/builder/test_builder.py --require-rv32
python3 scripts/docs_check.py
(cd tests && behave)
```

Expected result / pass criteria: every command exits 0. The AECP campaign catches its nine new plants and the control campaign catches `plat-as-path-unavailable`. `aecp_face.c` stays at 100 % of lines and branches. The load gate holds 1x1/1if at 0.501 against 0.70. `plat_ledger` prints `POINT 8x8-if2: rom 129,272 B ... 60 RAMB36 (platform-8x8-two-interfaces) ... PASS`. The split boot reaches ready at each point.

## Known limitations / out of scope

- The status of a GET_AS_PATH whose datapath window does not answer is unchanged: ENTITY_MISBEHAVING, as for GET_AVB_INFO, GET_STREAM_INFO and GET_COUNTERS, by the #897 ruling.
- The bench check (#897 acceptance 5) belongs to the bench lane, on the bring-up board.
- The harness's full legs (every group at both points) were not run again. This change's read runs only on a GET_AS_PATH, which no arm A group stages, and both answering arms replace the port. Fresh builds at both points ran sampled groups at this head and at `cec88385`, and their costs are within the stated tables.
- `flip_grade.py --check` exits 1 at `cec88385` and at this head alike, with identical output. It is no merge gate.
- The platform's and the fixture's 8x8/2if entries are both fully used at this head. Any later growth at that point is the ROM debt owed to S14.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (acceptance 1-4, acceptance 3 as amended by the ruling; acceptance 5 belongs to the bench lane)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive (round 1 POSITIVE at `5e6fef3e`; round 2 to be assigned)
- [ ] External review is positive (round 1 POSITIVE at `5e6fef3e`; round 2 to be assigned)
- [x] Blocking and major findings are fixed and re-reviewed (round 1 had none)
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
