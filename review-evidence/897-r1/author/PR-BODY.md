[A776]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

BLOCKED on one decision (#897, the STOP comment): the status a GET_AS_PATH answers when its datapath window does not answer. Everything else is implemented and gated at head `5e6fef3e`. The clean-clone pass ran every workflow job and the lane gates once: the firmware self-test, the AECP campaign (236 of 236) and the control campaign (697 of 697), coverage, the builder, behave and the split boot simulation all PASS. Three gates are red as they are at the base, each fixed by #810's round 29 after `7f50ee6a`: the C/C++ idiom ratchet, the hooks self-test and the firmware boundary. `897-split-as-path` -> `dev-soft-core`, on #810's round 29 head `7f50ee6a`.

## Linked Issue / roles

Relates to #897
Relates to #665

Executor: `[A776]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

The Mark II split answered GET_AS_PATH with ENTITY_MISBEHAVING: the platform's `path()` was a stub that always failed, and the AECP face forwarded to it. The face now reads the path through the datapath's GSI window, kind 2, as it already reads GET_AVB_INFO's words.

| Piece | Change |
|---|---|
| `sw/firmware/ctrl/aecp/aecp_face.c` `path()` | the count at kind 2 selector 0, then each `path_sequence` ClockIdentity at selector 8 by its ordinal, through the AVB interface's own window; a count past the core's capacity (`AECP_PATH_ITEMS`) fails the port at the count, reading no entry; a word with no answer fails the port there, as for GET_AVB_INFO |
| `sw/firmware/ctrl/plat/ctrl_plat.c` | the unavailable stub removed; the platform supplies `random` only |
| `sw/firmware/ctrl/test/ctrl_aecp_image.c` | the size fixture's stub removed, so the fixture links the same read |
| AS_PATH_CHANGED | already led to the unsolicited GET_AS_PATH response (`ctrl_app_aecp.c`, Table 5.22 bit 2); it now carries the datapath's sequence, tested |
| `tb/verilator/ctrl_service_budget/build.py` | the `answering-ports` and `answering-every-port` arms put their answering port in the face's `path` port, as they did through the removed stub |
| docs | `sw/firmware/ctrl/plat/README.md` (the "GET_AS_PATH answers unavailable" item replaced by the behaviour), `sw/firmware/ctrl/aecp/README.md`, `aecp_face.h`, `docs/design/MAILBOX_SPLIT.md` (the writer section and the host tests' row), `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 (the images' sizes), the harness README |

The split datapath serves kind 2 (`hdl/milan/milan_datapath.sv`, `g_sp_ctrl` and the GSI answer block): the count from a snapshot taken at the count's request, the entries from that snapshot, at most eight, so one response carries one sequence. No RTL and no mailbox contract change.

New tests (each named by a planted defect that it kills by its own words):

| Test | Rule | Plants |
|---|---|---|
| `Face.AsPathIsTheDatapathsSequenceThroughItsOwnWindow` | SUCCESS at 0, 1, 3 and 8 entries on every interface, the count and entries in order, cdl 16 + 8 an entry, the count at selector 0 then each entry at selector 8 by its ordinal, through the interface's own window | count read as kind 1; every entry at ordinal 0; the count through interface 0 |
| `Face.AsPathCarriesItsWholeBoundAndFailsACountPastIt` | `AECP_PATH_ITEMS` carried whole; a count past it, or past the caller's capacity, fails the port at the count | the count clamped and carried; `>=` for `>` |
| `Face.AnUnansweredAsPathWordFailsItsPortThere` | a window with no answer at the count or any entry fails the port at that word, counted unanswered | the count's failure ignored; an entry's failure ignored |
| `AppFace.AnAsPathChangeNotifiesTheDatapathsSequence` | AS_PATH_CHANGED sends the registered controller a SUCCESS GET_AS_PATH carrying the sequence the datapath serves, through the changed interface's window | the event marks bit 1; the notice for AVB_INTERFACE 0 |
| `Boot.B11GetAsPathAnswersTheDatapathsSequence` | the composed split answers GET_AS_PATH SUCCESS with the datapath's sequence, at one and two interfaces | the old stub's answer restored |

## Authoritative references

- IEEE 1722.1-2021 7.4.41 (GET_AS_PATH command and response), 9.3.2.5 and Table 7-141 (status codes), 9.3.2.6 (timeouts, IN_PROGRESS)
- Milan v1.2 5.4.1 (response length), 5.4.2.24 (GET_AS_PATH), 5.4.5.2 Table 5.22 (the unsolicited GET_AS_PATH)
- `sw/firmware/ctrl/mbx/mbx_contract.h`: `MBX_FACE_REG_GSI_SEL` (kind 2 GET_AS_PATH, selector, ordinal), `MBX_EV_TYPE_AS_PATH_CHANGED`
- `docs/design/MAILBOX_SPLIT.md`, class R (the GSI window) and class E (the face events)
- protocol-processor `docs/architecture/06_aecp_engine.md` 6.10 (the gather face's kind 2 word table)
- #665 owner decision 2026-11-12 (issuecomment-6824896581) and the #895 ruling (issuecomment-6824623445): the ROM caps

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
python3 tb/verilator/ctrl_service_budget/run.py --self-test
python3 tb/verilator/ctrl_service_budget/load_grade.py --check
python3 sw/builder/test_builder.py --require-rv32
python3 scripts/docs_check.py
(cd tests && behave)
```

Expected result / pass criteria: every command exits 0; the AECP campaign catches its nine new plants and the control campaign `plat-as-path-unavailable`; `aecp_face.c` stays at 100 % of lines and branches; the load gate holds 1x1/1if at 0.486 against 0.70.

ROM (planned by `ctrl_memory.plan`, both images at the four points, on #810 round 29's runtime archives and split SoC exports): each image gains 312 to 328 B of `rom`, no `sram` and no tile. The fixture's 8x8/2if image stays at 58.0 RAMB36 (cap 58.5), the platform's at 59.5 (cap 60.5; the tree's own 59.0 entry refuses it at the base as at this head), every other point within 56.

## Known limitations / out of scope

- The status a GET_AS_PATH answers when the datapath does not answer within the window's bound is unchanged (ENTITY_MISBEHAVING, as for GET_AVB_INFO, GET_STREAM_INFO and GET_COUNTERS); #897 holds the question.
- The bench check (#897 acceptance 5) is the bench lane's, on the bring-up board.
- The harness's full legs were not run again: this change's read runs only on a GET_AS_PATH, which no arm A group stages, and both answering arms replace the port as before. A fresh build of each point and arm ran sampled groups; their costs are within the stated tables.
- `scripts/check_cpp_idiom.py` and the hooks self-test fail at the base `7f50ee6a` as at this head, on code this branch does not touch; #810's later round 29 commit fixes both.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (blocked on the decision for acceptance 3's failure case; acceptance 5 is the bench lane's)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
