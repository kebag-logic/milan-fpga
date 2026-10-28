[A680h]

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

GREEN at head `0052e62e46582b701aa91d879c766b41682bfd3e`, the merge of `dev-soft-core` `6660a1a0` (PR #792, lane S2) into round 6's `424b1489`; `665-s1-faces` -> `dev-soft-core`. Every gate the merge round names is rc 0 at that head (below), and the four-shard Verilator sweep passes 64 of 64 suites there (2,191,124 checks, 0 in-suite failures), as at `424b1489`.

R701-6 and R702-6 were each POSITIVE at `424b1489`. This round makes no change of its own: it merges `dev-soft-core` and resolves one conflict, in `sw/firmware/ctrl/test/ctrl_configs.py`, by keeping both sides. A delta review of the resolution follows. #665 itself stays open.

## Linked Issue / roles

Relates to #665 (lane S1: assignment 6409739310, rulings 6410169666, 6412739248, 6421238472 and 6425357821, round-4 assignment 6417644908, round-6 assignment 6426858104, merge-round assignment 6447669608). This PR is one lane of #665 and must not close it.

Executor: `[A680h]` (earlier: `[A680]`, `[A680b]`, `[A680c]`, `[A680d]`, `[A680e]`, `[A680f]` and `[A680g]`)
Internal cleared-context reviewer: `[R701]`
External reviewer: `[R702]`

## Description

**The merge (this round).** `0052e62e` merges `dev-soft-core` at `6660a1a0` (PR #792, lane S2: the CPU budget harness `tb/verilator/ctrl_service_budget/`, the CI workflows and scripts it needs, and their docs) into `424b1489`, as a merge commit; nothing is rebased. One file is changed on both sides, `sw/firmware/ctrl/test/ctrl_configs.py`: each side appended to `OUTSIDE` after `sw/mailbox/publication_census.py`. Both are kept verbatim, each with its own reason: this lane's `sw/mailbox/census_ports.py` entry ("classifies every port of the processor wrapper in the census's netlists, naming the firmware that writes each face (#665 S1); it compiles nothing"), then S2's comment and its five harness entries (`build.py`, `runtime_ssp.py`, `scenario.py`, `selftest.py`, `split_soc.py`). S2's `SUITES` entry (`fixture_variant.py`) merged cleanly. The merge differs from `424b1489` only in S2's 36 files and from `6660a1a0` only in this lane's files, and every file but `ctrl_configs.py` equals the version of the side that changed it. The four linked images are byte-identical to round 6's.

The split placement removes the whole processor wrapper (`KL_pp_shadow`, ruling 6088423771, decision 1). This branch decides each of its 217 ports and adds what the mailbox must still carry, as contract 2.3, an additive minor. The all-fabric build is unchanged: its export is digest-identical for every shipped config.

| Piece | What changed |
|---|---|
| Port census | `sw/mailbox/census_ports.py` names each `pp_shadow` port under one class in all six shapes: C 25, F 28, R 34, E 6, M 14, G 110. A G output's cone may end only at the CSR block's processor-status inputs, the twenty memory-master outputs, or `pp_maap_shim` while that shim feeds `pp_shadow` alone. It stops at the map writer's 25 nets, which go with the wrapper; the placement switch must pass the census without that exclusion. There are 12 rules with 18 plants, which ride on existing netlists. |
| Contract 2.3 | `sw/mailbox/mailbox.yaml`, with `mailbox_face.py` the face block's generator and new checks and arms. Each interface's face block holds the settings, published by one commit per interface with a bounded acknowledgement. There are four request windows (CTR, AMAP, EDIT, GSI) with tag and timeout, and four events (COUNTERS_CHANGED per descriptor with a 1,000 ms holdoff, AVB_INFO_CHANGED, AS_PATH_CHANGED, AMAP_LIVE_WRITE). |
| RTL | `KL_mbx` is regenerated with the face ports, and `KL_mbx_evt` gains the face events. `CtrlMailbox` names every face port and leaves it unread, its inputs idle. `milan_datapath.sv` is not touched. Rounds 5 and 6 change no RTL. |
| Firmware | `aecp_face.c` answers the AECP owner's `changed`, `applied`, `format`, `counters`, `stream` and `avb` ports on the face block. A setting is written and committed, and its acknowledgement awaited within a bound. A lock change and a lock expiry are published (`AECP_CHANGE_LOCK`). The store's restore and NVM status are written before AECP opens and on each change. `ctrl_app_open_aecp` opens AECP only once every interface has acknowledged the initial publication. |
| Acknowledged state (round 5) | LOCK_ENTITY, SET_CONFIGURATION, SET_STREAM_FORMAT, SET_STREAM_INFO, SET_CLOCK_SOURCE and SET_CONTROL (`AECP_WAITS`) carry their change in a face commit. Each change records the bytes it overwrites. When `applied` is false after one of them, the core keeps its SUCCESS response, undoes the change, and answers IN_PROGRESS at once with the values in force. Taken by every interface within `AECP_WAIT_MS` (100 ms), the change is done again, and SUCCESS then its notification follow. Otherwise it stays undone and the command answers ENTITY_MISBEHAVING with the values in force, notifying no one. While a change waits, every getter, READ_DESCRIPTOR and notification reports the values in force, the face writes nothing, and the core's own work follows the wait. While a change waits, an expiry's notification waits, or any interface is held or owed, the lock check refuses every other change, with what the command's lock refusal reports. |
| The lock in force (round 6, R702-5 F1) | A lock still expires at 60 s, and its release (LOCK_HELD 0) is still committed then. Until that commit is acknowledged, however late, the lock holds, by its owner, for every response and read. ENTITY_AVAILABLE, LOCK_ENTITY's `locked_id`, the lock the ACMP owner reads (`aecp_locked`) and every refusal report it. So another controller is refused ENTITY_LOCKED, naming the owner, and the owner is refused ENTITY_MISBEHAVING, as under a held lock while the face is held. The expiry's notification leaves once the commit is acknowledged, and from then on the lock is released for every reader. `aecp_other_lock` (`aecp_commands.c`) is the one predicate the lock check, the refusal status and the MVU path use. |
| SET_SYSTEM_UNIQUE_ID (round 6, R701-5 F1, option (a)) | Refused only because a change waits or the face is held, it answers ENTITY_MISBEHAVING with the `system_unique_id` in force, changing nothing, as the AEM refusals do. Under another controller's lock, including the lock in force above, it keeps NOT_IMPLEMENTED. |
| Memory budget | `ctrl_memory.plan` keeps refusing any image past 56 RAMB36. One named override, `8x8-two-interfaces`, lets that point's measurement plan 57.5 (ruling 6425357821), and refuses it past that. The override is refused on every other point. `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 ledgers this head's figures at all four points (below). |
| Tests | The face block's checks run through both adapters, at two interfaces and on the host model, with 24 RTL face arms and 6 model twins. GoogleTest's `Core`, `Face`, `FaceLatency`, `AppFace` and `AppFaceUnacknowledged` hold 101 tests at each interface count. The AECP campaign plants 137 defects, 59 of them the face's. Coverage is 100 % lines and branches with no new exclusion. |
| Docs | `docs/design/MAILBOX_SPLIT.md` "The firmware's writer" (the model, the lock in force, the MVU refusal, its timing and clauses, and "the undone value after a failed change", named and accepted below) and the verification rows; `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3, 5 and 6; `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 1; `docs/reference/FR_NFR.md` (the AECP response row's IN_PROGRESS policy); the aecp and ctrl READMEs; `aecp.h`; `aecp_face.h`. |

**The timing, by clause.** IN_PROGRESS leaves within the service bound of the command. The final response leaves at most `AECP_WAIT_MS` plus the service bound after the command. That is inside the 120 ms IN_PROGRESS cadence of IEEE 1722.1-2021 9.3.2.6, so no second IN_PROGRESS is owed, and inside its 240 ms. `Face.AWaitingChangeIsAnsweredWithinTheInProgressCadence` measures both on the model's millisecond clock, with the 10 ms service bound added, and never reads `AECP_WAIT_MS`. A plant at 130 ms and one at 115 ms (inside 120 ms alone, outside it with the service bound) are each caught. The final response leaves on the interface its command came in on. No getter waits, so GET_DYNAMIC_INFO, which carries only getters, never answers IN_PROGRESS (IEEE 1722.1-2021 7.4.76). `FR_NFR.md`'s no-IN_PROGRESS policy names this one exception.

**Tests for the model.**

- `Core.AChangeThePlatformHasNotAppliedPromisesNothing`: every lock-guarded change refused, its body exactly its lock refusal's; reads answered.
- `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: pending then success, with a getter, READ_DESCRIPTOR and a second command meanwhile; then each of the six commands timing out with the whole core state unchanged and no notification.
- `Core.ALockExpiryIsNotifiedOnceThePlatformAppliedTheRelease`: the expiry's notification held until applied, through a full ring.
- `Core.AnExpiredLockHoldsByItsOwnerUntilThePlatformAppliedItsRelease` (round 6): ENTITY_AVAILABLE from either controller, `aecp_locked`, LOCK_ENTITY's `locked_id`, the refusals' status, and SET_SYSTEM_UNIQUE_ID all report the lock in force until the release is applied. Once it is notified, they report it released.
- `Core.ASystemIdChangeWhileOneWaitsIsRefusedAsEveryChangeIs` (round 6): ENTITY_MISBEHAVING with the identifier in force during a pending wait and after a failed wait; NOT_IMPLEMENTED under another controller's lock.
- `Core.AWaitingChangeIsAnsweredOnTheInterfaceItCameIn` (round 6): asked on interface 1 while interface 0's command is answered meanwhile. IN_PROGRESS, SUCCESS and the failure each leave on interface 1, from its address.
- `Face.AWaitingChangeIsAnsweredWithinTheInProgressCadence` (round 6): above.
- `Face.ALateCommitIsOwedAndPublishedAgainWhole`, `Face.APendingChangeIsAnsweredOnceTheDatapathTakesIt`, `Face.APartialAcknowledgementFailsTheChangeUntilEveryInterfaceTakesIt`, `Face.AMissingAcknowledgementFailsTheChangeAndRefusesEveryOther`, `Face.ALockThatExpiresWhileAChangeWaitsIsNotifiedOnceTaken`.
- Round 6's nine new plants: an expired lock read as released, its owner dropped, unread by the ACMP owner, not held against another controller, or its owner kept once notified; SET_SYSTEM_UNIQUE_ID's refusal at status 1; the waiting response's interface restore removed; `AECP_WAIT_MS` at 130 and at 115. Three round-5 plants were re-pointed to the lines this round changed.

**Every reviewer probe of rounds 3 to 5, unchanged, at round 6's head `424b1489`** (the merge changes none of the files they read). Each probe file's sha256 equals its reviewer's published manifest.

| Probe (unchanged) | Result at `424b1489` |
|---|---|
| R702-5 `probe_release_reads.cpp`, core and app arms, one and two interfaces | passes at each: `pending-release ENTITY_AVAILABLE flags=2 lock_owner=1020304050607081`, `pending-release foreign LOCK_ENTITY status=3 locked_id=1020304050607081`, `after-applied ENTITY_AVAILABLE flags=0 lock_owner=0` |
| R702-5 `probe_held_interface.cpp`, two interfaces | passes: `final status=0 egress=1`. At one interface the probe skips itself (`AECP_TEST_INTERFACES < 2`), and the harness's tally counts that skip as a failure, so that run exits 1 by the probe's design; the reviewer ran it at two interfaces only |
| R702-5 `review_mutants.py`: `wait-bound-past-cadence`, `held-interface-not-restored`, `owed-change-not-refused`, `record-not-reset` | each CAUGHT at two interfaces; the first two escaped at round 5 and are caught by `Face.AWaitingChangeIsAnsweredWithinTheInProgressCadence` and `Core.AWaitingChangeIsAnsweredOnTheInterfaceItCameIn` |
| R701-5 `probe_wait_refusals.cpp`, app arm, one and two interfaces | passes at each: SET_NAME 10; SET_SYSTEM_UNIQUE_ID 10 during the wait and 10 after the failed wait |
| R701-5 `count_face_defects.py` | `total 137 face-family 39 core-applied-only 18 sum 57`. The README's 59 is round 5's 50 plus round 6's nine; the script counts by test name (`Applied` or `LockExpiry`), and two new plants' tests (`ASystemIdChange...`, `AWaitingChangeIsAnsweredOnTheInterface...`) name neither |
| R701-3 `response_probe.py`, mailbox arm, one and two interfaces | passes |
| R701-4 `late_ack_notify_probe.py`, R702-4 `delta_probes.py`, R702-3 `probe_ack.py` | each one's own assertion holds; each fails only its first-frame status fixture, by design (next table) |

**The three probe fixtures whose first-frame status check differs.** Item 1 of ruling 6421238472 makes a waiting command's first frame IN_PROGRESS (9), by design. Each fixture below was written before that ruling and checks the first frame's status against the outcome of its own round. The probes are not edited.

| Probe (unchanged) | Fixture's status check | Status at `424b1489`, and why | The probe's own assertion |
|---|---|---|---|
| R701-4 `late_ack_notify_probe.py`, `Face.ReviewerProbeALateAcknowledgedChangeIsAnnounced` | SET_CONTROL (command 24): ENTITY_MISBEHAVING (10), round 4's immediate failure | IN_PROGRESS (9): the change waits for the acknowledgement the probe withholds | holds: `PROBE held: core_identify=0 get_control_identify=0 datapath_identify=255`, then `PROBE after: datapath_identify=255 owed0=0 unsolicited_set_control=1` |
| R702-4 `delta_probes.py`, `Face.ReviewGetterMustNotPromiseUnacknowledgedIdentify` and `Face.ReviewStreamNotificationMustNotPromiseUnacknowledgedOffset` | SET_CONTROL (24) and SET_STREAM_INFO (14): ENTITY_MISBEHAVING (10) | IN_PROGRESS (9), for the same reason | holds: `REVIEW getter: status=0 returned=0 last_acknowledged=0`; no notification with the unacknowledged offset while it is held; `ReviewAutomaticUnlockMustBeNotifiedAfterRecovery` passes (`applied=1 notifications=1 registered=1`); 23 of 25 tests pass at each width |
| R702-3 `probe_ack.py`, `Face.ReviewHeldSettingMustNotPromiseUnwrittenValue` | SET_CONTROL (24): SUCCESS (0), round 3's answer once acknowledged | IN_PROGRESS (9) first, then ENTITY_MISBEHAVING (10): the probe holds the acknowledgement past `AECP_WAIT_MS`, so the change fails and stays undone (ruling item 2) | holds: `response_status=10 core_identify=0 mailbox_identify=255`, so no SUCCESS promises the unwritten value; the script exits 1 because it exits 0 only on the defect |

**The memory figure.** Round 6 added 64 B of `rom` and no `sram` at every point, against round 5's head `6d2b77bb`, and moved no point's RAMB36 count. The merge adds nothing: the four images linked at `0052e62e` are byte-identical to `424b1489`'s, and plan the same. Every image is linked against the same runtime (built with `-fno-stack-protector`):

| Point (linked image, planned) | `rom` B, base -> round 5 -> head | `sram` B, base -> head | RAMB36, base -> round 5 -> head | Held to |
|---|---:|---:|---:|---|
| 1x1, one interface | 97,920 -> 104,360 -> 104,424 | 45,920 -> 46,256 | 35.5 -> 37.0 -> 37.0 | 56 |
| 1x1, two interfaces | 99,416 -> 105,944 -> 106,008 | 57,312 -> 57,648 | 38.5 -> 40.5 -> 40.5 | 56 |
| 8x8, one interface | 111,648 -> 118,080 -> 118,144 | 86,496 -> 86,832 | 49.0 -> 50.5 -> 50.5 | 56 |
| 8x8, two interfaces | 113,208 -> 119,736 -> 119,800 | 112,656 -> 112,992 | 56.0 -> 57.5 -> 57.5 | 57.5, by its override (ruling 6425357821) |

The 64 B are `aecp_other_lock` (+64), `aecp_command` (+32), `aecp_locked` (+16), `aecp_rx` (+8), `aecp_poll` (-8) and `aecp_foreign_lock` (-48). The largest point has 1,032 B of `rom` left before 58.0, and 1,016 B would return it to 57.0. The shipping point has 24 B left before 37.5. No compaction was needed, so none is taken. The two measured at round 5 (-64 B each) would leave 119,672 B, still 57.5. Section 5 of `SPLIT_CONTROL_MEMORY.md` records all of this.

## Authoritative references

- #665: ruling 6088423771 (decisions 1 and 2), decisions 6409738976 (D1, D3), assignment 6409739310, rulings 6410169666, 6412739248, 6421238472 and 6425357821, owner clarification 6410301079, round-4 assignment 6417644908, round-6 assignment 6426858104, merge-round assignment 6447669608; PR #795 reviews R701-5 (6426457867) and R702-5 (6426851137), and R701-6 and R702-6 (POSITIVE at `424b1489`)
- IEEE 1722.1-2021 7.4 (7.4.2 lock, 7.4.3 entity available, 7.4.5.1, 7.4.7 configuration, 7.4.15.1, 7.4.23 clock source, 7.4.42 counters, 7.4.76), 7.5.2 and 9.3.2.6
- Milan v1.2 5.3.7.3, 5.4.2.2, 5.4.2.12, 5.4.4.2, 5.4.5.2 (Table 5.22), 5.6.1; FR-CTRL-03
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
python3 sw/firmware/ctrl/test/aecp_arms.py --output "$OUT/app1" --app --interfaces 1
python3 sw/firmware/ctrl/test/aecp_arms.py --output "$OUT/app2" --app --interfaces 2
python3 sw/firmware/ctrl/test/aecp_mutants.py --output "$OUT/plants0" --shard 0 4
python3 sw/firmware/ctrl/test/aecp_mutants.py --output "$OUT/plants1" --shard 1 4
python3 sw/firmware/ctrl/test/aecp_mutants.py --output "$OUT/plants2" --shard 2 4
python3 sw/firmware/ctrl/test/aecp_mutants.py --output "$OUT/plants3" --shard 3 4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4
python3 sw/firmware/gtest/fw_coverage.py --check
python3 scripts/ci_rv32_sdk_selftest.py
python3 scripts/ci_rv32_sdk.py --destination "$SDK"
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator
python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator
python3 sw/builder/test_builder.py --require-rv32
python3 sw/litex/test_ctrl_memory.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_baremetal_only.py --selftest
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
(cd tests && behave --no-capture -f plain)
bash scripts/run_all_suites.sh "$OUT/sweep" --wait
python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml \
  --interfaces 2 --with-aecp --layout split --ledgered-point 8x8-two-interfaces --output "$OUT/image" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
python3 sw/litex/ctrl_memory.py plan "$OUT/image/ctrl_app.elf" --stage-bytes 13264 \
  --ledgered-point 8x8-two-interfaces
```

At the merge head, `aecp_arms.py`, `aecp_mutants.py` and `test_ctrl_memory.py` were not run again: the merge changes no file they read, and their `424b1489` receipts stand (the firmware self-test's shard 2 runs the same 137 AECP plants, all caught). Rounds 5 and 6 and the merge change no file the following gates read, so their round-4 and round-5 receipts stand (the merge's sweep runs `mbx` again): `gen_mailbox.py --check --crosscheck` and `--selftest`, `publication_census.py --check --selftest --jobs 4`, and `make -C tb/verilator/mbx`.

Expected result and pass criteria:

- `$SDK` is a new directory: the installer installs the pinned archive into an absent prefix, or verifies one that carries its receipt, and replaces nothing.
- Every command exits 0. The last two link and plan the 8x8 two-interface image with its override: 57.5 RAMB36, `"ledgered_tiles": 57.5`. Without `--ledgered-point` both refuse it (exit 2), and the other three points plan within 56 and refuse the override.
- The AECP arms pass 101 tests at each interface count.
- The AECP campaign catches 137 of 137 plants (35, 34, 34 and 34 across the four shards). The firmware self-test's shard 2 runs the same 137 again, and shard 1 catches 528 of 528.
- Coverage is 100 % of lines and branches over 31 files, with no new exclusion: `aecp.c` 417/417 and 360/360, `aecp_commands.c` 450/450 and 374/374.
- `ctrl_boundary.py` passes both legs with 0 findings. `test_builder.py` reports one arm not run where no local Arty build report exists.
- `test_ctrl_memory.py` reports 0 failures under LiteX's own interpreter.
- `run.py --self-test` (S2's harness) reports 0 failures, every one of its 62 grader mutants caught.
- `behave` passes 406 scenarios.
- The sweep passes every suite, 64 of 64; `tsn_fuzz` declares its field campaigns skipped without tsn-gen.

## Known limitations / out of scope

- The 8x8 two-interface image plans 57.5 RAMB36, a tile and a half over the budget, owed to lane S14 (decision D3, hybrid XIP; rulings 6412739248 and 6425357821). The flip (S13) still requires 56 or fewer at every point, with S14 merged. The other three points plan within 56; the shipping point has 24 B of `rom` left before 37.5.
- **The undone value after a failed change** (accepted for this lane by ruling 6425357821 item 2, as R701-4's outcome (a)). A written commit stays in the face block until the datapath takes it, and `cdc_handshake` holds its value. Firmware cannot withdraw it. After a failed command, the datapath takes the undone value with the late acknowledgement, and the poll then publishes the values in force whole. So the datapath ends at the values in force, where the controllers were told, but holds the undone value from that late acknowledgement until it takes the republished block. Closing that window needs the datapath side, so it belongs to the placement switch (#665 F-INT PR 2), which wires that side. `MAILBOX_SPLIT.md` "The firmware's writer" states it by this name.
- A lock that expires while a change waits is released when the wait ends, at most 100 ms late. Until its release is acknowledged it holds, by its owner, for every reader. A datapath that never acknowledges keeps it held, and keeps every change refused.
- SET_SYSTEM_UNIQUE_ID under another controller's lock answers NOT_IMPLEMENTED, as before this lane (R701-5 S4). Whether Milan v1.2 5.4.4.2 requires ENTITY_LOCKED there is outside this lane.
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
