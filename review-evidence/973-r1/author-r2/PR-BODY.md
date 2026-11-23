[A822]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

Requested Round 2 local gates PASS at this head, including the firmware boundary and its self-test.
The additional split-boot campaign also passed. Hosted checks and independent re-review remain pending.

`973-srp-link-carried` -> `dev-soft-core`; local branch `pf-973-1`.
Head: `5759780f2251ef25221c6a395250312dce656ca4`.
Twelve commits after the flip PR's reviewed head `dd163e41` (#960).

## Linked Issue / roles

Closes #973
Relates to #665, #970, #972, #872

Executor: `[A822]`
Internal cleared-context reviewer: `[R895]`
External reviewer: `[R896]`
Both reviews must cover the corrected head before merge.

## Description

A link-up between the loop's event take and SRP's poll previously reset the interface twice. The poll took the
register's new UP before its LINK record was dispatched. That record then looked like a repeated UP and reset the
interface again, losing the clean startup participants.

SRP now carries the last dispatched LINK level in each interface. Attach initializes it from the register. The
poll takes a DOWN immediately from the register and waits for the carried level before taking an UP. A first UP
keeps the startup participants without resetting them; a later UP resets once.

A re-attach can read DOWN while a full event ring holds its record. If the link recovers before that record posts,
no LINK is owed. To recover in this case, a poll marks an uncarried UP. A later poll takes it only after a pass whose
event take emptied the ring. The fabric posts a pending LINK before other sources when space opens, and a full ring
holds more records than one pass takes. Thus an owed LINK is dispatched before the poll falls back to its mark.

| File | Change |
|---|---|
| `srp/srp_mbx.c`, `srp/srp_mbx.h` | carried level, attach initialization, and marked recovery after the event ring drains |
| `test/srp_link_pass.cpp`, `srp_fixture.hpp`, `srp_arms.py` | tests at four pass phases, behind a full ring, and across re-attach; separate processes at both shipping shapes |
| `test/srp_link_mutants.py`, `srp_mutants.py` | eleven planted link defects and updated poll-read plant |
| `test/ctrl_configs.py` | classify the non-compiling plant table in `OUTSIDE`, with its reason |
| SRP README, changelog | describe link reconciliation and its remaining limitation |

Paths in the table are relative to `sw/firmware/ctrl`, except the changelog.
The test commit `88d81818` precedes the recovery fix: the re-attach test fails with the Round 1 firmware at both
shapes, while its ordinary later-UP control passes. The original inside-pass test also fails on the flip base.
No RTL, mailbox contract, loop, CPU budget bound, or budget harness file changes.

## Authoritative references

- #973 acceptance and #665.
- IEEE 802.1Q-2018 10.7 and 35.2: MRP participants, operational port state, and MSRP.
- [SRP adapter lifecycle](sw/firmware/ctrl/srp/README.md).
- [Loop service order](sw/firmware/ctrl/loop/ctrl_loop.h).
- [Mailbox event posting](hdl/milan/mailbox/KL_mbx_evt.sv).

## How to get into the same state

```sh
git fetch origin 973-srp-link-carried
git checkout --detach 5759780f2251ef25221c6a395250312dce656ca4
git submodule update --init third_party/lwSRP third_party/tsn-c-stack protocol-processor gptp-processor third_party/verilog-axis
```

Use the pinned environment described in [QUICKSTART.md](QUICKSTART.md).

## How to validate

Run each firmware shard in its own checkout, with its own build directory. Set `WORK` to a scratch directory.

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard K/4 --jobs 8
# K = 0, 1, 2, 3
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
make -C tb/verilator/milan_dp twin twin-plants twin-maps twin-maps-plants
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir "$WORK/plat"
G=srp,adp-link,maap,control,backlog,aecp,aecp-fanout,acmp-cmd,datapath-events,fixture
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir "$WORK/b1" --groups "$G" --jobs 8 --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir "$WORK/b8" --groups "$G" --jobs 8 --record-budget-findings --record-share-findings
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
python3 -I tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -I tb/verilator/ctrl_service_budget/shape_costs.py --check
```

The CPU campaigns must report zero refusals and zero budget misses, in addition to exit 0.
Run the documentation workflow's gate commands and both builder legs as specified in
[CI workflow policy](docs/testing/CI_WORKFLOWS.md).

| Gate | Result at this head |
|---|---|
| Firmware, four shards | PASS: 77 suites; 826 control, 385 AECP, 576 SRP successful campaign checks; no escaped plants |
| Firmware boundary and self-test | PASS: 4,455 compiled sources, zero findings; 117 boundary, 185 pin, 4 figure controls |
| Coverage self-test and check | PASS: 40 files |
| Twin, map twin, and plants | PASS: zero findings, all plants caught |
| CPU measured campaigns | PASS: 88 / 86 probes, zero refusals or misses; no verdict changed from base |
| CPU table graders | PASS, byte-identical to base: loads 0.511 / 0.744 against 0.70 / 0.75 |
| 1x1 timing rows | Last notice 127.31 ms; ACMP 29.06 ms; txL 47.88 ms, all below unchanged limits |
| Platform image ledger | PASS: ROM 126488 / 128104 / 139256 / 140856 B; SRAM and 45 / 46 / 58 / 63 RAMB36 allocations unchanged |
| Docs workflow steps | PASS: 104 / 104 |
| Builder legs 0 / 1 | PASS with one declared NOT RUN arm each: ineffective environment-option plant; physical calibration report unavailable |
| Split boot | Both shipping shapes PASS; all 6 native controls and 6 planted defects caught |

The largest absolute base/head CPU-probe difference is 0.217 ms against a 20 ms budget. The stored last-notice
gate is still 130 ms, tighter than the owner's 140 ms ceiling. No limit was relaxed.

## Known limitations / out of scope

- A DOWN inside a pass still resets twice: once from the register, then from its LINK record. Nothing transmits
  between them. A prototype that skips the second reset adds 16 B to the 8x8/1if ROM and is refused at 58.5 RAMB36
  against its unchanged 58-tile ledger. The documented limitation remains.
- The corrected 8x8/1if image occupies 139,256 B of ROM, just 8 B below the next allocation boundary. SRAM and the
  existing BRAM allocations are unchanged; existing fit and timing requirements remain.
- An uncarried UP needs a marking poll and a later pass that empties the event ring. This also recovers an UP
  dropped by the sink's re-entry guard; that invariant violation remains counted and asserted in debug builds.
- The reviewer's clear-carried-on-DOWN control survives because marked recovery now restores the UP with the same
  single reset, potentially one poll later. Its raw escaped result is retained. The register-UP double-reset and
  attach-carries-UP plants remain killed; the OR-instead-of-AND defect is replanted at the new poll line.
- The second-hart lane (#872) owns integration with its changes to the same poll.
- Hosted reruns, independent re-review, merge-candidate validation, and post-merge bench scenarios remain required.
  Local evidence is not LAB qualification.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
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
