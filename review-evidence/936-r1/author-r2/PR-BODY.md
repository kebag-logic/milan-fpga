[A793]

## Contents

- **[Status](#status)** -- Current result and branch.
- **[Linked Issue / roles](#linked-issue--roles)** -- Scope and review ownership.
- **[Description](#description)** -- Behavior and tests.
- **[The declared and withdrawn Talker's notice, timed (R862-1-F1)](#the-declared-and-withdrawn-talkers-notice-timed-r862-1-f1)** -- The new CPU budget rows and their controls.
- **[No idle pass with the notice owed (R861-F1)](#no-idle-pass-with-the-notice-owed-r861-f1)** -- The loop contract.
- **[Finding, tracked by #943](#finding-tracked-by-943)** -- The split's `stream_dest_mac`.
- **[Authoritative references](#authoritative-references)** -- Governing clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout.
- **[How to validate](#how-to-validate)** -- Commands, expected results and evidence.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Rulings, dependencies and reports.
- **[Definition of Done](#definition-of-done)** -- Remaining merge requirements.

## Status

Ready for review at `d1aa4c44`: 15 commits on dev-soft-core `70f4056f`, branch `936-stream-notice`. Round 2,
`343dfe43` to `d1aa4c44`, answers R862-1 and R861-1.

- **R862-1-F1.** The CPU budget harness's new `talker-notices` arm times a real Talker declaration and a withdrawal.
  Each runs through SRP's record and the AECP bridge to the last registered controller's STREAM_OUTPUT
  GET_STREAM_INFO commit, with the observation answering, under `notice-retried`'s load and with 16 registrations.
  At 1x1/1if and 8x8/1if every row is within its 20 ms: at most 6.887 ms and 7.553 ms. The dropped and delayed
  plants are each caught by name on every row.
- **R861-F1.** A pass that takes SRP's record reports output owed, so no pass reports the loop idle with the notice
  unsent. A per-pass test checks this at the composition and on the real gate path, each with a plant caught by name.
- **Residues.** The dest-MAC owed row names #943, and `ctrl_memory.py:247`'s comment uses R862-1-R1's exact words.
- **R861's questions 1 and 2 are ruled not defects of this PR, owed to #894** ([below](#known-limitations--out-of-scope)).
- Every gate passes on fresh clean clones of `d1aa4c44` ([How to validate](#how-to-validate)). The release image is
  byte-identical to the base.

## Linked Issue / roles

Closes #936
Relates to #665

Executor: `[A793]`
Internal cleared-context reviewer: `[R<n>]` (to be named by the manager)
External reviewer: `[R<n>]` (to be named by the manager)

## Description

**The specs oblige the notice.** Milan v1.2 5.4.5.2 and Table 5.22 list, for GET_STREAM_INFO, a Stream Output's
"MSRP Talker attribute declaration state", the MSRP failure code and bridge ID, the Stream ID, destination MAC and
VLAN ID. IEEE 1722.1-2021 7.5.2 ties "MSRP Talker Advertisements or Failures" to GET_STREAM_INFO notices. The release
processor sends one at each Talker declaration and withdrawal (`protocol-processor/hdl/top/protocol_processor_top.sv:3679-3684`).
The split sent none: no firmware caller passed STREAM_OUTPUT to `aecp_changed`.

| Piece | Change |
|---|---|
| `sw/firmware/ctrl/srp/srp_mbx.h`, `srp_mbx.c` (`declare_sources`) | After TALKER_DECL is published, each source whose declaration changed against what its STREAM_OUTPUT last showed is recorded in `noticed`: declared or withdrawn, still declared with its type swapped (once the swap is made), or still declared on another VID (an adopted Domain's). A reset that declares an unchanged source again records nothing; a failed creation records once it succeeds. |
| `sw/firmware/ctrl/app/ctrl_app.h`, `ctrl_app_srp.c` | The SRP delivery takes each interface's record into `ctrl_app.srp_noticed`; an SRP attach clears it, so a recomposition keeps no earlier record. A pass that takes a record reports output owed (round 2, R861-F1). |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c` | The AECP bridge raises each recorded source's STREAM_OUTPUT GET_STREAM_INFO event (`aecp_changed`, type 6). AECP's own notice path and pacing then send it to every registered controller (Milan v1.2 5.4.5.1). |
| `sw/firmware/ctrl/test/srp_talker.cpp`, `srp_gate.hpp`, `test_aecp.cpp` | One test per trigger: `DeclarationAndWithdrawalAreNoticed`, `TypeSwapIsNoticed` (Failed declared and withdrawn, a swap lwSRP refuses, a swap made), `AdoptedDomainVidIsNoticed`, `ResetNoticesNothingUnchanged`; the composition's `F936AProbeAndItsExpiryEachNoticeTheSource` (a real PROBE_TX through MAAP's DA gate and its 15 s expiry, over a stale record); `App.SrpDeclarationChangeIsItsStreamOutputsNotice` (every registered controller, the named source only, nothing without a record). Round 2: `F936BThePassThatTakesTheRecordOwesItsNotice` and `App.NoPassIsIdleWhileAStreamOutputsNoticeIsOwed` ([below](#no-idle-pass-with-the-notice-owed-r861-f1)). |
| `sw/firmware/ctrl/test/srp_talker_mutants.py`, `aecp_notice_mutants.py`, `aecp_mutants.py`, `srp_mutants.py` | 13 SRP plants `talker-notice-*` (both SRP campaigns) and 5 AECP plants `app-output-notice-*` (`aecp_notice_mutants.py`, which the AECP campaign composes as its other sub-modules; round 1's four moved there unchanged), each caught by its test's words. Round 2 adds `talker-notice-owed-unreported` and `app-output-notice-owed-unreported`; `TAKE`'s and `binding-poll-adds-access`'s anchors follow the new `deliver` text. |
| `tb/verilator/ctrl_service_budget/talker_notice.py`, `build.py`, `run.py`, `selftest_notice.py`, `README.md` | Round 2: the `talker-notices` arm, its `talker-notice-<k>` groups and rows, the plants `declared-notice-dropped` and `declared-notice-delayed` with their verdict (`run.declared_verdict`), and their self-test checks ([below](#the-declared-and-withdrawn-talkers-notice-timed-r862-1-f1)). `talker_notice.py` holds the talker arms' variants, plants and control kinds, so `build.py`, at Rule 12's 1,000 lines, changes three lines. |
| `tb/verilator/milan_dp/twin_compare.py`, `twin_plants.py`, `Makefile`, `README.md` | `stream-output-0-notices` deleted: the split now sends the fabric's four notices of STREAM_OUTPUT 0, at the same changes, to the same controllers. One byte group still differs (#943, below), held by its own exact owed row `stream-output-0-dest-mac`, whose owner is now `#943`. New capture plant `output-notice-dropped` (this issue's defect back); `vanished-owed` re-aimed at the new row. |
| `sw/litex/ctrl_memory.py`, `ctrl_memory_ledger.py`, `test_ctrl_memory.py`, `docs/design/SPLIT_CONTROL_MEMORY.md`, `MARK_II_AREA_PLAN.md` | `ctrl_plat` +64 B at both two-interface points (19,136 and 20,416 B). The size fixture's `8x8-two-interfaces` entry 59.0 -> 59.5 RAMB36, by the owner's decision of 2026-11-15 (#665 issuecomment-6892332745). At `d1aa4c44` the harness's `answering-every-port`, `valid-destinations` and `talker-notices` arm images at 8x8/2if need 127,140, 126,992 and 127,048 B of rom: 164, 16 and 72 B past 59.0's 126,976. |
| `sw/firmware/ctrl/srp/README.md`, `sw/firmware/ctrl/aecp/README.md`, `tb/verilator/ctrl_service_budget/README.md` | The rule, its tests and plants; where a STREAM_OUTPUT GET_STREAM_INFO event comes from; the owed report; the new arm and its plants; the fixture's entry. |

No RTL, mailbox-contract or CPU-budget-bound change, and no bound added or moved.

**Product images.** Round 2's one firmware change, `ctrl_app_srp.c`'s owed report, adds 8 B of `rom` in five split
images: the fixture's and the platform's at 1x1/2if and 8x8/2if, and the platform's at 8x8/1if. The other images and
every `sram` figure are unchanged. `plat_ledger.py` passes at every point; `SPLIT_CONTROL_MEMORY.md` states the
figures. The release (all-fabric) image is byte-identical to the base.

## The declared and withdrawn Talker's notice, timed (R862-1-F1)

The arm `talker-notices` ([`talker_notice.py`](tb/verilator/ctrl_service_budget/talker_notice.py)) is
`valid-destinations`' fixture: its ACMP source port is valid once MAAP holds the range. The face block's stream
observation answers zeroed values at every attempt, as `answering-ports`' does. Each of its eight groups,
`talker-notice-<k>`:

- **Population.** Registers 16 controllers on every interface, the firmware's capacity (Milan v1.2 5.3.4.2, 5.4.5.1),
  and starts a save of the saved-state store, as `notice-retried-<k>` does.
- **The declaration** (`notice.declared`). Once MAAP holds the ranges, a PROBE_TX for source 0 is answered SUCCESS.
  Its DA gate opens, SRP declares the Talker and records the source, the SRP delivery takes the record, the AECP
  bridge raises the notice and THE RETRY sends it. The row runs from the PROBE_TX's mailbox RX commit, the event, to
  the later of its response and the last registration's STREAM_OUTPUT 0 GET_STREAM_INFO commit.
- **The withdrawal** (`notice.withdrawn`). A peer ANNOUNCEs the range from a MAC for which `compare_MAC` is FALSE
  (IEEE 1722-2016 B.3.6.4), as in `srp-talker-loss`. MAAP restarts on a new range, the gate closes and SRP withdraws
  the Talker. The row runs from the ANNOUNCE's RX commit to the last registration's notice.
- **Load.** Each event comes `k` ms into 130 ms of `notice-retried`'s load: every receive channel at its contract
  refill rate with its bursts, and a grandmaster change as every pass starts. The event's own channel's load starts
  one refill period after it, so its bucket admits the burst whole. SRP's channel carries a Listener Ready for another
  entity's stream, the same size as the load's own, because one for source 0's stream would open its DA gate by
  itself.
- **Bound.** The asynchronous notifications' row, min(T_svc, 24 ms) = 20 ms (FR_NFR.md 3.4.1: events start at their
  occurrence; the last required recipient's commit ends a fan-out; backlog and TX-ring backpressure consume the
  budget). It is the `notify` family's existing bound; none is added or moved.
- **Failing.** A row over its bound, or with no notice, fails the run whatever its options record (`run.notice_misses`;
  the row's refusal).

| Run (clean clone) | Image `ctrl_app.elf` | Rows | Recipients | Elapsed, ms | Bound | Refusals | rc |
|---|---|---:|---:|---|---:|---:|---:|
| 1x1/1if, unplanted | `ec6f0066` | 16 | 16 each | 2.043 to 6.887 | 20 ms | 0 | 0 |
| 8x8/1if, unplanted | `b8d11ef5` | 16 | 16 each | 2.245 to 7.553 | 20 ms | 0 | 0 |
| 1x1/1if, `declared-notice-dropped` | `cebd7792` | 16 | 0 | none committed | 20 ms | 16, each "no notification" | 0, `CONTROL declared-notice-dropped caught: 16 of 16` |
| 1x1/1if, `declared-notice-delayed` | `25a65fe5` | 16 | 16 each | 26.641 to 30.568 | 20 ms | 0 | 0, `CONTROL declared-notice-delayed caught: 16 of 16` |

Each row's event origin and final commit, in system cycles, are in the receipts' per-row table. For example,
`talker-notice-1.declared.if0` at 1x1/1if runs from the PROBE_TX committed at sys 300,100,141 to the last of 16
recipients at sys 300,788,856, 6.887 ms. Neither the unplanted arm nor its plants print a `STATED` line at either point.

Every run is on a fresh clean clone of `d1aa4c44`, and the unplanted runs' images are the size fixture's
`talker-notices` images at that head, by sha256. The same legs on `33f24ca3`, whose split images are byte-identical,
printed the same `NOTICE`, `REFUSED`, `BUDGET`, `STATED` and `CONTROL` lines.

## No idle pass with the notice owed (R861-F1)

`ctrl_loop.h`: a poll returns true while its module still owes output, and only a pass that handled nothing and owes
nothing sleeps. The SRP delivery took SRP's record and returned only its sinks' pending, so the pass that took it could
report the loop idle with the notice unsent. Now `deliver` reports a taken record as owed (`pending = noticed`), and
the AECP bridge raises the notice in the next pass. Once raised, a notice AECP cannot send yet is AECP's own owed
retry, as before.

- `App.NoPassIsIdleWhileAStreamOutputsNoticeIsOwed`, `test_aecp.cpp`: from an idle loop, SRP's record is set and
  each pass stepped alone until one returns 0. By then both registered controllers' notices must be committed. This
  runs at one and two interfaces. Plant `app-output-notice-owed-unreported` (AECP campaign) is caught by name.
- `SrpGate.F936BThePassThatTakesTheRecordOwesItsNotice`, `test_acmp_mbx.cpp`: a real PROBE_TX through MAAP's DA gate,
  then its 15 s expiry. The pass that takes each record must return nonzero. Plant `talker-notice-owed-unreported`
  (both SRP campaigns) is caught by name.

The take stays where it was. A gate's declaration is made in a pass given whole to THE TRANSMIT, where no poll runs,
so the next pass's delivery takes it, and that pass now reports it owed.

## Finding, tracked by #943

- **What.** On the split, a declaring STREAM_OUTPUT's GET_STREAM_INFO answer sets STREAM_DEST_MAC_VALID with
  `stream_dest_mac` 0. The fabric's answer carries the declared Talker's destination.
- **Evidence.** The twin: STREAM_OUTPUT 0's declared notices, fabric
  `f2000000 0205022002006000 0200000000010000 001e8480 91e0f0000100 ...`, split
  `f2000000 0205022002006000 0200000000010000 001e8480 000000000000 ...`. Every other field and both withdrawn
  notices are equal. The row `stream-output-0-dest-mac` (`tb/verilator/milan_dp/twin_compare.py`) pins both halves'
  exact values; the plant `vanished-owed` shows it refused once the split matches.
- **Clause.** Milan v1.2 5.4.2.10.2; Table 5.11, STREAM_DEST_MAC_VALID.
- **Cause.** The datapath's GET_STREAM_INFO face answers a STREAM_OUTPUT's destination from the fabric MAAP engine's
  address (`hdl/milan/milan_datapath.sv:6424`, read at `:6625`), which the split does not build (`:8731`,
  `:8760-8761`). The same face sets no MSRP failure fields and no REGISTERING, its declaring bit is the DA gate, and
  the split raises no Listener-registration notice of a STREAM_OUTPUT. All of this is #943's.

## Authoritative references

- Milan v1.2 5.4.5.1, 5.4.5.2, Table 5.22: unsolicited recipients and triggers.
- Milan v1.2 5.4.2.10.2, Tables 5.11 and 5.12: a STREAM_OUTPUT's fields.
- IEEE 1722.1-2021 7.5.2 and 7.4.16 (GET_STREAM_INFO). The issue's 7.4.40 is GET_AVB_INFO in this edition.
- `docs/reference/FR_NFR.md` 3.4.1 and its asynchronous-notification row: the event-to-commit budget, 20 ms.
- `sw/firmware/ctrl/loop/ctrl_loop.h`, the polls: the loop contract.
- `protocol-processor/hdl/top/protocol_processor_top.sv:3679-3684`: the release processor's trigger.
- #665 issuecomment-6892332745 (block RAM kept loose); #936 issuecomment-6938589620 (the held-egress rows).
- PR #944's reviews R862-1 (issuecomment-6953846656) and R861-1 (issuecomment-6954572914).

## How to get into the same state

```sh
git fetch origin 936-stream-notice && git checkout --detach d1aa4c44
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4   # and 1/4, 2/4, 3/4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
make -C tb/verilator/milan_dp twin            # one finding, PR #935's stale split-talker-failed row
make -C tb/verilator/milan_dp twin-plants TWIN_PLANTS="byte-flip missing-notification"   # srp-plus-k is PR #935's
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --variant talker-notices --build-dir "$T1" --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --variant talker-notices --build-dir "$T8" --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --variant talker-notices --mutation declared-notice-dropped --build-dir "$D1"
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --variant talker-notices --mutation declared-notice-delayed --build-dir "$L1"
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --variant answering-later --build-dir "$A1" --record-budget-findings --record-share-findings
#   and answering-later at 8x8-1if, answering-every-port at 1x1
python3 tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir "$L"
python3 scripts/docs_check.py
```

Every workflow job was replayed step by step on its own fresh clone of `d1aa4c44`. Each `run:` step has rc 0 or a
stated reason for not running, and those reasons are only tool installs this host already has and the hosted
step-context recorders.

| Gate | Result at `d1aa4c44` |
|---|---|
| rtl-fast `firmware-unit` | PASS: firmware suites and RV32 builds, saved-state store 526 tests, `fw_coverage.py --check` PASS (39 files) |
| rtl-fast `firmware-srp-mutants` | PASS: both SRP campaigns, 447 caught, none escaped; the 13 `talker-notice-*` plants caught in each, `talker-notice-owed-unreported` and `binding-poll-adds-access` included |
| rtl-fast `firmware-aecp-mutants` | PASS: 304 caught, none escaped; the 5 `app-output-notice-*` plants caught, `app-output-notice-owed-unreported` included |
| rtl-fast `firmware-control-mutants` | PASS: 716 of 716 caught |
| docs `wire-accountability`, `docs-check-no-git`, `docs-gates-0/1/2`, `docs-check` | PASS (61 steps; the link-health, Python-idiom and no-git checks that failed at `83f1785f` included) |
| twin | 1 finding, `split-talker-failed`, PR #935's stale row; `stream-output-0-dest-mac` holds |
| twin plants | `srp-plus-k` escapes by its stale words (PR #935's); the other 20 plants refused in both runs, 40 of 40; tree clean |
| CPU budget harness self-test; `check_py_idiom.py` | `self-test: 0 failures`; Rule 12 PASS (long function 9 of 9, long module 10 of 10) |
| `talker-notices`, 1x1/1if and 8x8/1if | PASS: 16 rows each, every one within 20 ms, at most 6.887 and 7.553 ms; 0 refusals; no `STATED` line; rc 0 |
| `declared-notice-dropped`, `declared-notice-delayed` (1x1/1if) | `CONTROL ... caught: 16 of 16` each: no notification to any registration, and 26.641 to 30.568 ms against 20 |
| `answering-later`, 1x1/1if and 8x8/1if | PASS: the retried notice at most 8.392 and 8.164 ms against 20 ms; 0 refusals, 0 misses |
| `answering-every-port`, 1x1/1if | PASS: 192 notices at most 27.294 ms against 140 ms; 0 refusals, 0 misses |
| release image | byte-identical to the base: `bios.bin` 1x1 `860d4771`, 8x8 `d8851b6d`; disassembly and debug-stripped ELF identical |
| split images, `plat_ledger.py` | PASS at every point: rom 117,688 / 119,304 / 130,392 / 131,976 B at 1x1/1if, 1x1/2if, 8x8/1if, 8x8/2if (43, 44, 56, 60.5 RAMB36); `ctrl_plat` unchanged; product ROM banks unchanged |
| size fixture | 112,624 / 114,216 / 125,280 / 126,832 B (41.0, 42.5, 55.0, 59.0 RAMB36); every-port 127,140, valid-destinations 126,992, talker-notices 127,048 B at 8x8/2if (59.5) |

Each `talker-notices` row's event origin and final commit, in system cycles, and each run's image and simulator
identity are in the receipts (`budget/talker-notice-rows.md`). The release, platform and fixture image comparisons
are in `images/image-identity.txt`.

## Known limitations / out of scope

- **R861's questions 1 and 2 are ruled not defects of this PR, owed to #894.**
  - The seven held-egress rows at 1x1/1if measure 0.132 to 0.151 ms more than the base's. 1x1/1if has no egress
    ledger. At 8x8/1if they are within the ledger.
  - At 8x8/1if the `valid-destinations` arm reports THE RETRY rounds of one refused attempt at 11,922 to 12,537 CPU
    cycles against the one-interface stated 11,900. That fixture leaves the observation unanswered.
  - Both are figures for the egress ledger's and the 8x8 point's owner, #894.
- The finding above, the split's STREAM_OUTPUT GET_STREAM_INFO answer, is RTL; tracked by #943.
- The twin's `split-talker-failed` row and the `srp-plus-k` plant's words are stale at the base; PR #935 (#929)
  deletes and restates them.
- Lane conflicts, by `git merge-tree` of `d1aa4c44` with each open head:
  - PR #935 (`37255683`): text conflicts in the twin's `Makefile`, `README.md` and `twin_compare.py`. A scratch merge
    at round 1 resolved them by keeping this PR's dest-MAC row, #935's deletion of `split-talker-failed` and both new
    capture plants; its twin found 0 differences and refused all 22 plants (44 of 44).
  - PR #932 (`0fdfdba7`): text conflicts in the memory ledger; whichever lands second re-measures its figures.
  - PR #914 (`e1ecce20`): one text conflict in `tb/verilator/ctrl_service_budget/run.py`'s `all_groups`, where #914
    passes the build to `talker_window.groups` and this PR adds the `talker-notices` arm. Keeping both resolves it;
    #914's `build.py` uses `talker_window` only in the two lines this PR replaces.
- The harness's `answering-every-port` arm refuses the 8x8/1if point at this base by name ("the model holds 40
  notices, not AECP_NOTICES_MOST at 8x8-1if", `notice_window.py`), unchanged here; it runs at 1x1/1if.
- Product split ROM banking is unchanged (1x1/1if 64+32+16+4 KiB, 8x8/1if one 128 KiB bank), so no route is owed.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
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
