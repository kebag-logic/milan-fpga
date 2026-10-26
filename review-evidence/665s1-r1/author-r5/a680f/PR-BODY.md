[A680f]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `665-s1-faces` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at head `6d2b77bb3bfb8e2fbd30db56613c8c3b5ea0ef44`; `665-s1-faces` -> `dev-soft-core`. Every gate this round touches is rc 0 there. The firmware is unchanged since `4e3aab32`, where every other gate is rc 0 and the Verilator sweep passes 64 of 64 suites (2,191,124 checks).

Round 5 answers R701-4 and R702-4 under the round-5 ruling (6421238472): acknowledged state is the only truth a controller sees. The ruling on the round's STOP (6425357821) lets the 8x8 two-interface image plan 57.5 RAMB36, owed to lane S14. The other acceptance items stand as in round 4. #665 itself stays open.

## Linked Issue / roles

Relates to #665 (lane S1: assignment 6409739310, rulings 6410169666, 6412739248, 6421238472 and 6425357821, round-4 assignment 6417644908). This PR is one lane of #665 and must not close it.

Executor: `[A680f]` (earlier: `[A680]`, `[A680b]`, `[A680c]`, `[A680d]`, and `[A680e]` for round 5 up to `4e3aab32`)
Internal cleared-context reviewer: `[R701]`
External reviewer: `[R702]`

## Description

The split placement removes the whole processor wrapper (`KL_pp_shadow`, ruling 6088423771, decision 1). This branch decides each of its 217 ports and adds what the mailbox must still carry, as contract 2.3, an additive minor. The all-fabric build is unchanged: its export is digest-identical for every shipped config.

| Piece | What changed |
|---|---|
| Port census | `sw/mailbox/census_ports.py` names each `pp_shadow` port under one class in all six shapes: C 25, F 28, R 34, E 6, M 14, G 110. A G output's cone may end only at the CSR block's processor-status inputs, the twenty memory-master outputs, or `pp_maap_shim` while that shim feeds `pp_shadow` alone. It stops at the map writer's 25 nets, which go with the wrapper; the placement switch must pass the census without that exclusion. There are 12 rules with 18 plants, which ride on existing netlists. |
| Contract 2.3 | `sw/mailbox/mailbox.yaml`, with `mailbox_face.py` the face block's generator and new checks and arms. Each interface's face block holds the settings, published by one commit per interface with a bounded acknowledgement. There are four request windows (CTR, AMAP, EDIT, GSI) with tag and timeout, and four events (COUNTERS_CHANGED per descriptor with a 1,000 ms holdoff, AVB_INFO_CHANGED, AS_PATH_CHANGED, AMAP_LIVE_WRITE). |
| RTL | `KL_mbx` is regenerated with the face ports, and `KL_mbx_evt` gains the face events. `CtrlMailbox` names every face port and leaves it unread, its inputs idle. `milan_datapath.sv` is not touched. Round 5 changes no RTL. |
| Firmware | `aecp_face.c` answers the AECP owner's `changed`, `applied`, `format`, `counters`, `stream` and `avb` ports on the face block. A setting is written and committed, and its acknowledgement awaited within a bound. A lock change and a lock expiry are published (`AECP_CHANGE_LOCK`). The store's restore and NVM status are written before AECP opens and on each change. `ctrl_app_open_aecp` opens AECP only once every interface has acknowledged the initial publication. |
| Acknowledged state (round 5) | LOCK_ENTITY, SET_CONFIGURATION, SET_STREAM_FORMAT, SET_STREAM_INFO, SET_CLOCK_SOURCE and SET_CONTROL (`AECP_WAITS`) carry their change in a face commit. Each change records the bytes it overwrites. When `applied` is false after one of them, the core keeps its SUCCESS response, undoes the change, and answers IN_PROGRESS at once with the values in force. Taken by every interface within `AECP_WAIT_MS` (100 ms), the change is done again, and SUCCESS then its notification follow. Otherwise it stays undone and the command answers ENTITY_MISBEHAVING with the values in force, notifying no one. While a change waits, every getter, READ_DESCRIPTOR and notification reports the values in force, the face writes nothing, and the core's own work follows the wait. While a change waits, an expiry's notification waits, or any interface is held or owed, the lock check refuses every other change. That refusal carries what the command's lock refusal reports (R701-4 F2). A lock expiry still releases at 60 s; its notification is kept until LOCK_HELD's publication is acknowledged, however late (R702-4 F2). |
| Memory budget | `ctrl_memory.plan` keeps refusing any image past 56 RAMB36. One named override, `8x8-two-interfaces`, lets that point's measurement plan 57.5 (ruling 6425357821), and refuses it past that. The override is refused on every other point. `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 ledgers this head's figures at all four points (below). |
| Tests | The face block's checks run through both adapters, at two interfaces and on the host model, with 24 RTL face arms and 6 model twins. GoogleTest's `Core`, `Face`, `FaceLatency`, `AppFace` and `AppFaceUnacknowledged` hold 97 tests at each interface count; the AECP campaign plants 128 defects, 50 of them the face's. Coverage is 100 % lines and branches with no new exclusion. |
| Docs | `docs/design/MAILBOX_SPLIT.md` "The firmware's writer" (the model, its timing and clauses, and "the undone value after a failed change", named and accepted below) and the verification rows; `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3, 5 and 6 (the ledger at 57.5); `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 1; `docs/reference/FR_NFR.md` (the AECP response row's IN_PROGRESS policy); the aecp and ctrl READMEs; `aecp_face.h`. |

**The timing, by clause.** IN_PROGRESS leaves within the service bound of the command. The final response leaves at most `AECP_WAIT_MS` plus the service bound after the command: inside the 120 ms IN_PROGRESS cadence of IEEE 1722.1-2021 9.3.2.6, so no second IN_PROGRESS is owed, and inside its 240 ms. No getter waits, so GET_DYNAMIC_INFO, which carries only getters, never answers IN_PROGRESS (IEEE 1722.1-2021 7.4.76). `FR_NFR.md`'s no-IN_PROGRESS policy now names this one exception.

**Tests for the model.**

- `Core.AChangeThePlatformHasNotAppliedPromisesNothing`: every lock-guarded change refused, its body exactly its lock refusal's; reads answered.
- `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: pending then success, with a getter, READ_DESCRIPTOR and a second command meanwhile; then each of the six commands timing out at exactly `AECP_WAIT_MS` with the whole core state unchanged and no notification.
- `Core.ALockExpiryIsNotifiedOnceThePlatformAppliedTheRelease`: the expiry's notification held until applied, through a full ring.
- `Face.ALateCommitIsOwedAndPublishedAgainWhole`: timeout with rollback on the model, the datapath ending at the value in force, then recovery.
- `Face.APendingChangeIsAnsweredOnceTheDatapathTakesIt`: pending then success; a notification falling due meanwhile waits and reports the value then in force.
- `Face.APartialAcknowledgementFailsTheChangeUntilEveryInterfaceTakesIt`, `Face.AMissingAcknowledgementFailsTheChangeAndRefusesEveryOther` (the automatic unlock notified once LOCK_HELD is taken), `Face.ALockThatExpiresWhileAChangeWaitsIsNotifiedOnceTaken`.
- Every reviewer probe of rounds 3 and 4 runs unmodified at `4e3aab32`, and each one's own assertion holds. Three fixtures' status checks now differ (next paragraph).

**The three probe fixtures whose first-frame status check differs.** Item 1 of ruling 6421238472 makes a waiting command's first frame IN_PROGRESS (9), by design. Each fixture below was written before that ruling and checks the first frame's status against the outcome of its own round. The probes are not edited.

| Probe (unmodified) | Fixture's status check | Status at this head, and why | The probe's own assertion |
|---|---|---|---|
| R701-4 `late_ack_notify_probe.py`, `Face.ReviewerProbeALateAcknowledgedChangeIsAnnounced` | SET_CONTROL (command 24): ENTITY_MISBEHAVING (10), round 4's immediate failure | IN_PROGRESS (9): the change waits for the acknowledgement the probe withholds | holds: `PROBE held: core_identify=0 get_control_identify=0 datapath_identify=255`, then `PROBE after: datapath_identify=255 owed0=0 unsolicited_set_control=1` (the late-taken change is done and announced) |
| R702-4 `delta_probes.py`, `Face.ReviewGetterMustNotPromiseUnacknowledgedIdentify` and `Face.ReviewStreamNotificationMustNotPromiseUnacknowledgedOffset` | SET_CONTROL (24) and SET_STREAM_INFO (14): ENTITY_MISBEHAVING (10) | IN_PROGRESS (9), for the same reason | holds: `REVIEW getter: status=0 returned=0 last_acknowledged=0`; no notification with the unacknowledged offset while it is held; `ReviewAutomaticUnlockMustBeNotifiedAfterRecovery` passes (`applied=1 notifications=1 registered=1`); 22 of 24 tests pass at each width |
| R702-3 `probe_ack.py`, `Face.ReviewHeldSettingMustNotPromiseUnwrittenValue` | SET_CONTROL (24): SUCCESS (0), round 3's answer once acknowledged | IN_PROGRESS (9) first, then ENTITY_MISBEHAVING (10): the probe holds the acknowledgement past `AECP_WAIT_MS`, so the change fails and stays undone (ruling item 2) | holds: `response_status=10 core_identify=0 mailbox_identify=255`, so no SUCCESS promises the unwritten value; the script exits 1 because it exits 0 only on the defect |

**The memory figure.** The model adds 1,056 B of `rom` and 224 B of `sram` at every point, against round 4's firmware (`989c9f53`). The base is `e76a755a`, linked against the same runtime as the head (built with `-fno-stack-protector`):

| Point (linked image, planned) | `rom` B, base -> round 4 -> head | `sram` B, base -> round 4 -> head | RAMB36, base -> round 4 -> head | Held to |
|---|---:|---:|---:|---|
| 1x1, one interface | 97,920 -> 103,304 -> 104,360 | 45,920 -> 46,032 -> 46,256 | 35.5 -> 37.0 -> 37.0 | 56 |
| 1x1, two interfaces | 99,416 -> 104,888 -> 105,944 | 57,312 -> 57,424 -> 57,648 | 38.5 -> 40.5 -> 40.5 | 56 |
| 8x8, one interface | 111,648 -> 117,024 -> 118,080 | 86,496 -> 86,608 -> 86,832 | 49.0 -> 50.5 -> 50.5 | 56 |
| 8x8, two interfaces | 113,208 -> 118,680 -> 119,736 | 112,656 -> 112,768 -> 112,992 | 56.0 -> 57.0 -> 57.5 | 57.5, by its override (ruling 6425357821) |

Only the largest point crosses a granule: round 4 left it 104 B of `rom`, and it now has 1,096 B before 58.0. The 1,056 B are the change record and its ten call sites, the undo and redo swap, the held SUCCESS response and its re-answer as a refusal, the wait's resolution, the expiry's kept notification and the lock check's refusal. All 224 B of `sram` are the core's state. Two compactions were measured on throwaway edits and not taken: constant port tables in three files (-64 B) and IN_PROGRESS carrying the held SUCCESS body instead of a re-answer (-64 B more), which leave 119,608 B, still 57.5. Returning to 57.0 would need 952 B. Section 5 of `SPLIT_CONTROL_MEMORY.md` records all of this.

## Authoritative references

- #665: ruling 6088423771 (decisions 1 and 2), decisions 6409738976 (D1, D3), assignment 6409739310, rulings 6410169666, 6412739248, 6421238472 and 6425357821, owner clarification 6410301079, round-4 assignment 6417644908; PR #795 reviews R701-4 (6421229873) and R702-4 (6421210118)
- IEEE 1722.1-2021 7.4 (7.4.2 lock, 7.4.5.1, 7.4.7 configuration, 7.4.15.1, 7.4.23 clock source, 7.4.42 counters, 7.4.76), 7.5.2 and 9.3.2.6
- Milan v1.2 5.3.7.3, 5.4.2.2, 5.4.2.12, 5.4.5.2 (Table 5.22), 5.6.1; FR-CTRL-03
- `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 1; `docs/reference/FR_NFR.md` (the AECP rows); `docs/design/MAILBOX_SPLIT.md`; `docs/reference/MAILBOX_CONTRACT.md`; `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3, 5 and 6
- `CONTRIBUTING.md` (CDC: every handshake crosses through `cdc_handshake` or toggle-plus-sync)

## How to get into the same state

```sh
git fetch origin
git checkout 665-s1-faces
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

## How to validate

```sh
python3 sw/mailbox/gen_mailbox.py --check --crosscheck
python3 sw/mailbox/gen_mailbox.py --selftest
python3 sw/mailbox/publication_census.py --check --selftest --jobs 4
make -C tb/verilator/mbx
python3 sw/firmware/ctrl/test/aecp_arms.py --output "$OUT/app1" --app --interfaces 1
python3 sw/firmware/ctrl/test/aecp_arms.py --output "$OUT/app2" --app --interfaces 2
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4
python3 sw/firmware/gtest/fw_coverage.py --check
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
python3 sw/builder/test_builder.py --require-rv32
python3 sw/litex/test_ctrl_memory.py
(cd tests && behave --no-capture -f plain)
bash scripts/run_all_suites.sh "$OUT/sweep" --wait
python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml \
  --interfaces 2 --with-aecp --layout split --ledgered-point 8x8-two-interfaces --output "$OUT/image" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
python3 sw/litex/ctrl_memory.py plan "$OUT/image/ctrl_app.elf" --stage-bytes 13264 \
  --ledgered-point 8x8-two-interfaces
```

Expected result and pass criteria:

- Every command exits 0. The last two link and plan the 8x8 two-interface image with its override: 57.5 RAMB36, `"ledgered_tiles": 57.5`. Without `--ledgered-point` both refuse it (exit 2), and the other three points plan within 56 and refuse the override.
- The mailbox bench reports 523 Wishbone, 568 AXI4-Lite and 32 cosim checks, and 530, 575 and 488 at two interfaces, with 7 of 7 quick plants.
- The census proves 138 arms and all 43 rules over 217 ports per shape.
- The AECP arms pass 97 tests at each interface count.
- In the firmware self-test, shard 1 catches 528 of 528 and shard 2's AECP campaign 128 of 128.
- Coverage is 100 % of lines and branches over 31 files, with no new exclusion.
- `test_ctrl_memory.py` reports 0 failures under LiteX's own interpreter: the ledgered point plans at 57.5 by name and is refused at 58.0, without the override and through the SoC build; the override is refused on every other point.
- `test_builder.py` reports one arm not run where no local Arty build report exists.
- `behave` passes 406 scenarios.
- The sweep passes every suite; `tsn_fuzz` declares its field campaigns skipped without tsn-gen.

## Known limitations / out of scope

- The 8x8 two-interface image plans 57.5 RAMB36, a tile and a half over the budget, owed to lane S14 (decision D3, hybrid XIP; rulings 6412739248 and 6425357821). The flip (S13) still requires 56 or fewer at every point, with S14 merged. The other three points plan within 56.
- **The undone value after a failed change** (accepted for this lane by ruling 6425357821 item 2, as R701-4's outcome (a)). A written commit stays in the face block until the datapath takes it, and `cdc_handshake` holds its value. Firmware cannot withdraw it. After a failed command, the datapath takes the undone value with the late acknowledgement, and the poll then publishes the values in force whole. So the datapath ends at the values in force, where the controllers were told, but holds the undone value from that late acknowledgement until it takes the republished block. Closing that window needs the datapath side, so it belongs to the placement switch (#665 F-INT PR 2), which wires that side. `MAILBOX_SPLIT.md` "The firmware's writer" states it by this name.
- A lock that expires while a change waits is released when the wait ends, at most 100 ms late.
- The image figures are planned by `ctrl_memory.plan`. This branch maps none of them out of context.
- The image measurements use a runtime built with `-fno-stack-protector`. The stack-protected runtime the host SDK builds is lane S3's to resolve.
- The face block's datapath side is unread until the placement switch connects it, with its clock crossing. The acknowledgement path is tested on the host model, not on a datapath.
- The audio maps are not applied through the `EDIT` window. `GET_AS_PATH` stays the platform's port.
- `test_builder.py`'s gate 11 needs a local Arty build report and did not run here.
- No changelog entry: the build is default-off, as for the earlier mailbox lanes.

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
