[A793]

## Contents

- **[Status](#status)** -- Current result and branch.
- **[Linked Issue / roles](#linked-issue--roles)** -- Scope and review ownership.
- **[Description](#description)** -- Behavior and tests.
- **[Finding: a declaring STREAM_OUTPUT's stream_dest_mac is 0 on the split](#finding-a-declaring-stream_outputs-stream_dest_mac-is-0-on-the-split)** -- For a new issue.
- **[Authoritative references](#authoritative-references)** -- Governing clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout.
- **[How to validate](#how-to-validate)** -- Commands, expected results and evidence.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- Dependencies and reports.
- **[Definition of Done](#definition-of-done)** -- Remaining merge requirements.

## Status

Ready for review at `7cfb8a04`: 9 commits on dev-soft-core `70f4056f`, branch `936-stream-notice`.

- Every local gate passes on fresh clean clones (below).
- The release image is byte-identical to the base.
- The base's seven held-egress rows are graded by the egress ledger at 8x8/1if (#936 issuecomment-6938589620): PASS.
  At 1x1/1if, which has no ledger, they measure 0.13 to 0.15 ms more than the base's (reported below).
- One finding is for a new issue: the split's `stream_dest_mac` (below).

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
| `sw/firmware/ctrl/app/ctrl_app.h`, `ctrl_app_srp.c` | The SRP delivery takes each interface's record into `ctrl_app.srp_noticed`; an SRP attach clears it, so a recomposition keeps no earlier record. |
| `sw/firmware/ctrl/app/ctrl_app_aecp.c` | The AECP bridge raises each recorded source's STREAM_OUTPUT GET_STREAM_INFO event (`aecp_changed`, type 6). AECP's own notice path and pacing then send it to every registered controller (Milan v1.2 5.4.5.1). |
| `sw/firmware/ctrl/test/srp_talker.cpp`, `srp_gate.hpp`, `test_aecp.cpp` | One test per trigger: `DeclarationAndWithdrawalAreNoticed`, `TypeSwapIsNoticed` (Failed declared and withdrawn, a swap lwSRP refuses, a swap made), `AdoptedDomainVidIsNoticed`, `ResetNoticesNothingUnchanged`; the composition's `F936AProbeAndItsExpiryEachNoticeTheSource` (a real PROBE_TX through MAAP's DA gate and its 15 s expiry, over a stale record); `App.SrpDeclarationChangeIsItsStreamOutputsNotice` (every registered controller, the named source only, nothing without a record). |
| `sw/firmware/ctrl/test/srp_talker_mutants.py`, `aecp_mutants.py` | 12 SRP plants `talker-notice-*` (both SRP campaigns) and 4 AECP plants `app-output-notice-*`, each caught by its test's words. |
| `tb/verilator/milan_dp/twin_compare.py`, `twin_plants.py`, `Makefile`, `README.md` | `stream-output-0-notices` deleted: the split now sends the fabric's four notices of STREAM_OUTPUT 0, at the same changes, to the same controllers. One byte group still differs (the finding below), held by its own exact owed row `stream-output-0-dest-mac`. New capture plant `output-notice-dropped` (this issue's defect back); `vanished-owed` re-aimed at the new row. |
| `sw/litex/ctrl_memory.py`, `ctrl_memory_ledger.py`, `test_ctrl_memory.py`, `docs/design/SPLIT_CONTROL_MEMORY.md`, `MARK_II_AREA_PLAN.md` | `ctrl_plat` +64 B at both two-interface points (19,136 and 20,416 B). The size fixture's `8x8-two-interfaces` entry 59.0 -> 59.5 RAMB36: at `b496c99e` the CPU budget harness's `answering-every-port` and `valid-destinations` arm images need 127,132 and 126,992 B of rom, 156 B and 16 B past 59.0's 126,976. Raised as named debt owed to S14 by the owner's decision of 2026-11-15 (#665 issuecomment-6892332745). |
| `sw/firmware/ctrl/srp/README.md`, `sw/firmware/ctrl/aecp/README.md`, `tb/verilator/ctrl_service_budget/README.md` | The rule, its tests and plants; where a STREAM_OUTPUT GET_STREAM_INFO event comes from; the fixture's entry. |

No RTL, mailbox-contract or CPU-budget-bound change.

## Finding: a declaring STREAM_OUTPUT's stream_dest_mac is 0 on the split

For the manager to open as an issue (#665 has no step that owns it).

- **What.** On the split, a declaring STREAM_OUTPUT's GET_STREAM_INFO answer sets STREAM_DEST_MAC_VALID with
  `stream_dest_mac` 0. The fabric's answer carries the declared Talker's destination.
- **Evidence.** The twin at the final head: STREAM_OUTPUT 0's declared notices, fabric
  `f2000000 0205022002006000 0200000000010000 001e8480 91e0f0000100 ...`, split
  `f2000000 0205022002006000 0200000000010000 001e8480 000000000000 ...`. Every other field and both withdrawn
  notices are equal. The row `stream-output-0-dest-mac` (`tb/verilator/milan_dp/twin_compare.py`) pins both halves'
  exact values; the plant `vanished-owed` shows it refused once the split matches.
- **Clause.** Milan v1.2 5.4.2.10.2: while a Stream Output declares a Talker attribute, "the stream_id,
  stream_dest_mac and stream_vlan_id fields shall be set to the corresponding values of the declared Talker
  attribute"; Table 5.11, STREAM_DEST_MAC_VALID.
- **Cause.** The datapath's GET_STREAM_INFO face answers a STREAM_OUTPUT's destination from the fabric MAAP
  engine's address (`hdl/milan/milan_datapath.sv:6424` `gsi_odmac_w`, read at `:6625` under `maap_addr_valid`).
  The split does not build that engine (`:8731` builds it only where `CTRL_SPLIT_P == 0`), so `maap_addr` and
  `maap_addr_valid` are 0 (`:8760-8761`). The firmware's MAAP owner holds the range. Solicited GET_STREAM_INFO
  responses read the same face, so they are affected too.
- **Seen beside it, the same face (reported, not changed):** the split's STREAM_OUTPUT answer never sets
  MSRP_FAILURE_VALID or a failure code or bridge ID (`:6374` needs a declaration state of 2; the split ties it to
  `{0, TALKER_DECL}` at `:9991`, and the failure code to 0 at `:10003`). It never sets REGISTERING or
  REGISTERING_FAILED (Listener registration tied 0 at `:10001`). Its "declaring" bit is the DA gate (`:9980`,
  `:6370`), not TALKER_DECL. And the split raises no notice on a Listener registration change of a STREAM_OUTPUT
  (Table 5.22, "MSRP Listener attribute registration state (Stream Output only)"), where the release processor does
  (`protocol_processor_top.sv:3683`). So the notice this PR adds at a Talker Advertise/Failed swap is sent, but its
  answer cannot show the failure fields yet.

## Authoritative references

- Milan v1.2 5.4.5.1, 5.4.5.2, Table 5.22: unsolicited recipients and triggers.
- Milan v1.2 5.4.2.10.2, Tables 5.11 and 5.12: a STREAM_OUTPUT's fields.
- IEEE 1722.1-2021 7.5.2 and 7.4.16 (GET_STREAM_INFO). The issue's 7.4.40 is GET_AVB_INFO in this edition.
- `protocol-processor/hdl/top/protocol_processor_top.sv:3679-3684`: the release processor's trigger.
- #665 issuecomment-6892332745 (block RAM kept loose); #936 issuecomment-6938589620 (the held-egress rows).
- `sw/firmware/ctrl/srp/README.md`, `sw/firmware/ctrl/aecp/README.md`, `tb/verilator/milan_dp/README.md`,
  `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3 and 5.

## How to get into the same state

```sh
git fetch origin 936-stream-notice && git checkout --detach 7cfb8a04
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4   # and 1/4, 2/4, 3/4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
make -C tb/verilator/milan_dp twin            # one finding, PR #935's stale split-talker-failed row
make -C tb/verilator/milan_dp twin-plants TWIN_PLANTS="byte-flip missing-notification"   # srp-plus-k is PR #935's
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$B1" --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir "$B8" --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --variant answering-later --build-dir "$B1L" --record-budget-findings --record-share-findings
#   and --variant answering-every-port (1x1), --variant valid-destinations (both points), answering-later at 8x8-1if
python3 -I tb/verilator/ctrl_service_budget/egress_ledger.py --point 8x8-1if "$B8/results"   # PR #914's tool
python3 tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir "$L"
python3 scripts/ci_builder_legs.py run all --receipt legs.json -- python3 sw/builder/test_builder.py --require-elaboration --require-rv32
scripts/run_litex_sims.sh --selftest && scripts/run_litex_sims.sh "$LOGS"
scripts/run_all_suites.sh "$LOGS" --ci-pieces --shard 1/19   # and 4, 6, 10, 17: the shards that build the split firmware
python3 scripts/docs_check.py
```

Results. Every workflow job was replayed step by step on its own fresh clone; each `run:` step has rc 0 or a stated
reason for not running, and those reasons are only tool installs this host already has and the hosted
step-context recorders.

| Gate | Head | Result |
|---|---|---|
| rtl-fast `firmware-unit` | `7cfb8a04` (and `b496c99e`) | PASS: firmware suites and RV32 builds, saved-state store 526 tests, `fw_coverage.py --check` PASS (39 files) |
| rtl-fast `firmware-srp-mutants` | `b496c99e` | PASS: both SRP campaigns, 445 caught, none escaped; the 12 `talker-notice-*` plants caught in each |
| rtl-fast `firmware-aecp-mutants` | `b496c99e` | PASS: 303 caught, none escaped; the 4 `app-output-notice-*` plants caught |
| rtl-fast `firmware-control-mutants` | `b496c99e` | PASS: 716 of 716 caught |
| rtl-fast `firmware-boundary`, `firmware-verilator`, `split-cdc` | `b496c99e` | PASS |
| docs `wire-accountability`, `docs-check-no-git`, `docs-gates-0/1/2`, `docs-check` | `7cfb8a04` (and `b496c99e`) | PASS (61 steps) |
| elaborate builder legs (both) and LiteX aggregate | `7cfb8a04` | PASS; LiteX 8 of 8, `test_ctrl_memory` included; the builder's 2 arms its test records as not run here |
| rtl `verilator-shards` 1, 4, 6, 10, 17 of 19 (`milan_dp__0..3`, `mbx`) | `b496c99e` | PASS: 28 suites, 763,945 checks, 0 failed |
| twin | `7cfb8a04` (and `b496c99e`) | 1 finding, `split-talker-failed`, PR #935's stale row; `stream-output-0-dest-mac` holds |
| twin plants | `7cfb8a04` (and `b496c99e`) | `srp-plus-k` escapes by its stale words (PR #935's); the other 20 plants refused in both runs, 40 of 40 |
| twin on a scratch merge with PR #935 | `b496c99e` + `37255683` | 0 findings; all 22 plants refused, 44 of 44 |
| release image | `7cfb8a04` | byte-identical to the base: `bios.bin` 1x1 `860d4771`, 8x8 `d8851b6d`; disassembly and debug-stripped ELF identical |
| split images | `7cfb8a04` | `plat_ledger.py` PASS; platform (24) and fixture (6) image hashes identical to `b496c99e`'s; product ROM banks unchanged, no route owed |
| CPU budget harness, arm A, 1x1/1if (96 groups) | final image | 0 refusals; 0 of 130,941 passes over the 2 ms share; no `STATED` line; 7 misses, the base's held-egress rows |
| CPU budget harness, arm A, 8x8/1if (95 groups) | final image | 0 refusals; 0 of 263,828 passes over the share; 7 misses, the held-egress rows. `STATED` lines report the costs this point takes past the 1x1/1if stated ones (`ctrl_service_budget/README.md`): polls base at most 24,541 against 22,500, ACMP item 7,030 against 5,500, declined ACMP offer 2,380 against 2,000. The base's `backlog-owed` group reports the same two ACMP kinds |
| egress ledger, 8x8/1if | final image | PASS: the seven rows 0.136 to 0.314 ms inside their figures |
| `answering-later`, 1x1/1if and 8x8/1if | final image | PASS: the retried notice at most 8.301 and 8.246 ms, bound 20 ms |
| `answering-every-port`, 1x1/1if | final image | PASS: 192 notices at most 27.073 ms, bound 140 ms (the arm refuses 8x8/1if at this base) |
| `valid-destinations`, 1x1/1if and 8x8/1if | final image | PASS: every Talker declare and withdraw row within 220 ms, at most 189.315 ms at 1x1/1if and 189.423 ms at 8x8/1if; no `STATED` line at 1x1/1if. At 8x8/1if `STATED` reports: a tier-2 slice of THE TRANSMIT's build (92,226; the base's 91,604) and build-one passes, as at the base; new with this PR, 21 THE RETRY rounds of one refused attempt, 11,922 to 12,537 cycles against the one-interface 11,900 (below) |

"Final image": arm A ran on images built at `77c1aad7`, whose `ctrl_app.elf` files equal those `7cfb8a04` builds,
by sha256. The variant arms ran on clean clones of `b496c99e`. `7cfb8a04` changes no image input: every image the
size fixture and the ledger build is identical between the two, by sha256.

The seven held-egress rows against the base (each the harness's own grade of `backlog-owed`; the base by
`--groups backlog-owed` on a clean clone of `70f4056f`):

| Row | 1x1/1if base -> final, ms | 8x8/1if base -> final, ms | 8x8/1if ledger, ms |
|---|---|---|---:|
| `backlog.owed.if0` | 62.905 -> 63.041 (+0.136) | 63.513 -> 63.546 (+0.033) | 63.86 |
| `backlog.owed_behind0.if0` | 63.092 -> 63.228 (+0.135) | 63.799 -> 63.837 (+0.038) | 64.1 |
| `backlog.owed_behind1.if0` | 63.280 -> 63.413 (+0.133) | 64.027 -> 64.071 (+0.044) | 64.36 |
| `backlog.owed_behind2.if0` | 63.466 -> 63.599 (+0.132) | 64.273 -> 64.330 (+0.056) | 64.61 |
| `backlog.owed_behind3.if0` | 63.652 -> 63.784 (+0.132) | 64.512 -> 64.578 (+0.066) | 64.86 |
| `backlog-owed.service.acmp.last.if0` | 62.002 -> 62.145 (+0.143) | 62.380 -> 62.389 (+0.008) | 62.62 |
| `backlog-owed.service.aecp.last.if0` | 61.736 -> 61.887 (+0.151) | 62.030 -> 62.024 (-0.006) | 62.16 |

At 1x1/1if the service behind the scenario's 60 ms egress hold grows 3.6 to 8.7 %. `egress_ledger.py` holds no
figure there and refuses the point, so these rows stay the base's recorded misses by the ruling. They are reported
here, not graded.

New at 8x8/1if in `valid-destinations`: 21 rounds of THE RETRY with one refused attempt each, 11,922 to 12,537 CPU
cycles against the one-interface stated 11,900 (`round_grade.py`). The base runs the same arm with none; its longest
round is 2,174. Each attempt is a new STREAM_OUTPUT notice's GET_STREAM_INFO (`aecp.c` `scan`). This arm's fixture
does not answer the gather window (`aecp_face.c` `gsi`), so the attempt is refused and AECP's backoff retries it. The
`answering-*` arms answer the window, and there the retried notice is built within its row. At 1x1/1if the same
rounds are at most 9,015 cycles, within 11,900. 8x8/1if reports the costs it takes past the one-interface ones
(`ctrl_service_budget/README.md`), as it does for the tier-2 slice and the build-one passes at the base.

No harness group registers a controller while its Talker declares, so no row times the new GET_STREAM_INFO notice of
a STREAM_OUTPUT itself. The record's cost is inside the SRP rows' passes (`valid-destinations`, arm A's `srp`). The
notice is sent by AECP's notice path, which the `answering-*` rows time.

## Known limitations / out of scope

- The finding above (the split's STREAM_OUTPUT GET_STREAM_INFO answer) is RTL; no issue owns it yet.
- The twin's `split-talker-failed` row and the `srp-plus-k` plant's words are stale at the base; PR #935 (#929)
  deletes and restates them. PR #935 (`37255683`) also restates `stream-output-0-notices`, which this PR deletes,
  so the two conflict as text in the twin's `Makefile`, `README.md` and `twin_compare.py`. A scratch merge resolves
  them by keeping this PR's `stream-output-0-dest-mac` row, #935's deletion of `split-talker-failed`, and both new
  capture plants (`output-notice-dropped`, `talker-failed-back`). On that scratch merge (`32919b5f`, of `b496c99e`
  and `37255683`, not pushed; `7cfb8a04` changes no twin file) the twin finds 0 differences, and each of its 22 plants
  is refused in both runs (44 of 44), `srp-plus-k`, `talker-failed-back` and `output-notice-dropped` included.
- PR #932 (`0fdfdba7`) conflicts as text in the memory ledger (`sw/litex/ctrl_memory.py`, `ctrl_memory_ledger.py`,
  `test_ctrl_memory.py`, `docs/design/SPLIT_CONTROL_MEMORY.md`); whichever lands second re-measures its figures.
  PR #914 (`8883d499`) merges cleanly as text and shares `srp_mbx.c`/`.h` and `test_aecp.cpp`.
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
