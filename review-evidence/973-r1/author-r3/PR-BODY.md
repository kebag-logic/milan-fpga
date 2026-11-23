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

Requested round-3 local gates PASS at this head, including the firmware boundary with its self-test, the CPU
service-budget rows at 1x1/1if and 8x8/1if, and the image ledgers. Hosted checks and independent re-review are
pending.

`973-srp-link-carried` -> `dev-soft-core`; local branch `pf-973-1`.
Head: `87b2fc0f2867ef132b9388e22ec262fc626cbb57`.
Sixteen commits after the flip PR's reviewed head `dd163e41` (#960). Round 3 adds four commits after `5759780f`.

The hosted `firmware-boundary` job has to pass at this exact head. That job is the outstanding verification for the
retained R895-1-F1 finding. The required hosted jobs also have to run to completion without being cancelled. Both
are checked once the branch is pushed. The local boundary gate with its self-test passes at this head (see
the table below).

## Linked Issue / roles

Closes #973
Relates to #665, #970, #972, #872

Executor: `[A822]`
Internal cleared-context reviewer: `[R895]`
External reviewer: `[R896]`
Both reviews must cover the corrected head before merge.

## Description

A link-up between the loop's event take and SRP's poll used to reset the interface twice. The poll took the
register's new UP before its LINK record was dispatched. That record then looked like a repeated UP, so it reset the
interface again and lost the clean startup participants.

SRP now keeps, per interface, the level of the last LINK the loop dispatched. Attach sets it from the register. The
poll takes a DOWN from the register at once and takes an UP only when it is carried. A first UP keeps the startup
participants and resets nothing; a later UP resets once.

A re-attach can read a DOWN while a full event ring holds that DOWN's record. If the link recovers before the record
posts, no LINK is owed. For that case a poll marks an uncarried UP. A later poll takes the UP only if no LINK has
come and that poll's pass's event take emptied the ring. The fabric posts a pending LINK before its other sources
once there is room, and a full ring holds more records than one pass takes, so an owed LINK is dispatched before the
mark is used.

Round 3 (R896-2-F1): a DOWN that a poll reads now clears the mark. Before, a DOWN skipped the mark update, so in this
sequence a stale mark let the poll take a fresh UP that still had its own LINK coming:
1. an UP is marked while the ring is full;
2. a DOWN arrives before the UP's record can post, so the UP's record is never posted;
3. the ring drains;
4. a fresh UP rises after a later pass's take.

The poll then took that fresh UP, and its LINK reset the interface a second time. Now the mark survives only while
every poll reads the link up, and an UP after a DOWN is taken from its own LINK. Re-attach recovery, the fail-closed
DOWN and the carried-UP rules are unchanged. The change is byte-identical in `.text` at 1x1/1if and 8x8/1if.

| File | Change |
|---|---|
| `srp/srp_mbx.c`, `srp/srp_mbx.h` | carried level, attach initialization, marked recovery after the ring drains; a DOWN the poll reads clears the mark |
| `test/srp_link_pass.cpp`, `srp_fixture.hpp`, `srp_arms.py` | tests at four pass phases, behind a full ring, across an UP a DOWN elided (first and later UP) and across re-attach; separate processes at both shipping shapes |
| `test/srp_link_mutants.py`, `srp_mutants.py` | fourteen planted link defects, and the poll-read plant at the new poll line |
| `test/ctrl_configs.py` | classify the non-compiling plant table in `OUTSIDE`, with its reason |
| SRP README, changelog | link reconciliation, when the mark is valid, and the remaining limitation |

Paths in the table are relative to `sw/firmware/ctrl`, except the changelog. Every fix was preceded by a test commit
that fails without it:
- `d9f8929d` (round 3): both elided-UP tests fail at `5759780f` at both shipping shapes. They pass with `9a71daa9`'s
  SRP sources and at this head;
- `88d81818` (round 2): the re-attach test fails with the round-1 firmware;
- the original inside-pass test fails on the flip base.

No RTL, mailbox contract, loop, CPU budget bound or budget harness file changes.

## Authoritative references

- #973 acceptance and #665.
- IEEE 802.1Q-2018 10.7 and 35.2: MRP participants, operational port state, and MSRP.
- IEEE 802.3-2022 28.3.2 (`break_link_timer`): a dropped autonegotiated link stays down for 1,200 ms or more before
  it renegotiates. This is the stated assumption under [Known limitations](#known-limitations--out-of-scope).
- [SRP adapter lifecycle](sw/firmware/ctrl/srp/README.md).
- [Loop service order](sw/firmware/ctrl/loop/ctrl_loop.h).
- [Mailbox event posting](hdl/milan/mailbox/KL_mbx_evt.sv).

## How to get into the same state

```sh
git fetch origin 973-srp-link-carried
git checkout --detach 87b2fc0f2867ef132b9388e22ec262fc626cbb57
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
| Test-first regression | round-3 tests FAIL at `5759780f`, PASS at this head, both shipping shapes |
| Firmware, four shards | PASS: 77 suites; 826 control, 385 AECP, 585 SRP successful campaign checks; no escaped plants |
| Link plants | 14 link plants killed at 1x1/1if, 8x8/1if and 1x1/2if |
| Firmware boundary and self-test | PASS: 4,455 compiled sources, zero findings; 117 boundary, 185 pin, 4 figure controls |
| Coverage self-test and check | PASS: 40 files |
| Twin, map twin, and plants | PASS |
| CPU measured campaigns | PASS: 88 / 86 probes; zero refusals, budget misses or share misses; no verdict changed from base |
| CPU table graders | PASS, byte-identical to base: loads 0.511 / 0.744 against 0.70 / 0.75 |
| 1x1 timing rows | Last notice 127.31 ms; ACMP 29.06 ms; txL 47.88 ms, all below unchanged limits |
| Platform image ledger | PASS: ROM 126,488 / 128,112 / 139,256 / 140,856 B; 45 / 46 / 58 / 63 RAMB36. 1x1/1if and 8x8/1if unchanged from the previous head |
| Docs workflow steps | PASS: 104 / 104 |
| Builder legs 0 / 1 | PASS with one declared NOT RUN arm each: ineffective environment-option plant; physical calibration report unavailable |
| Split boot | Both shipping shapes PASS; native controls and planted defects caught |

The largest absolute base/head CPU-probe difference is 0.204 ms against a 20 ms budget. The stored last-notice
gate is still 130 ms, tighter than the owner's 140 ms ceiling. No limit was relaxed.

## Known limitations / out of scope

- **Stated assumption.** A DOWN that no poll reads lasts less than the gap between two SRP polls. A level register
  cannot show such a DOWN, so a rule that reads only the register cannot tell it from a steady UP. A real link does
  not go down and come back that fast: a dropped autonegotiated link waits at least `break_link_timer`, 1,200 ms
  (IEEE 802.3-2022 28.3.2), before it renegotiates, and SRP polls every few milliseconds. The code comment and the
  SRP README state this.
- A DOWN inside a pass still resets twice: once from the register, then from its LINK record. Nothing transmits
  between the two. A prototype that skips the second reset adds 16 B to the 8x8/1if ROM, which needs 58.5 RAMB36
  against the unchanged 58-tile ledger, so it was refused. The documented limitation remains.
- The 8x8/1if image uses 139,256 B of ROM, 8 B below the next allocation boundary. This round does not change that
  image. SRAM and BRAM allocations are unchanged. Existing fit and timing requirements remain.
- An uncarried UP needs a marking poll and a later pass that empties the event ring. This also recovers an UP that
  the sink's re-entry guard dropped. That invariant violation is still counted, and asserted in debug builds.
- The reviewer's clear-carried-on-DOWN control still survives: marked recovery restores the UP with the same single
  reset, possibly one poll later. Its raw escaped result is kept. The register-UP double-reset and
  attach-carries-UP plants are still killed, and the OR-instead-of-AND defect is planted again at the new site.
- The second-hart lane (#872) owns integration with its changes to the same poll.
- Still required: hosted runs at this head (including `firmware-boundary`, see Status), independent re-review,
  merge-candidate validation and the post-merge bench scenarios. Local evidence is not LAB qualification.

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
