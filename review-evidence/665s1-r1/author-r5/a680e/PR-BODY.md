[A680e]

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

BLOCKED (STOP, round 5) at head `4e3aab32`: the 8x8 two-interface image now plans 57.5 RAMB36, half a tile over the 57 the ruling of 2026-10-26 (6412739248) allows that point. Every other gate is rc 0 at that head, and the Verilator sweep passes 64 of 64 suites (2,191,124 checks); `665-s1-faces` -> `dev-soft-core`.

Round 5 answers R701-4 and R702-4 under the round-5 ruling (6421238472): acknowledged state is the only truth a controller sees. The other acceptance items stand as in round 4. #665 itself stays open.

## Linked Issue / roles

Relates to #665 (lane S1: assignment 6409739310, rulings 6410169666, 6412739248 and 6421238472, round-4 assignment 6417644908). This PR is one lane of #665 and must not close it.

Executor: `[A680e]` (rounds 1 to 4: `[A680]`, `[A680b]`, `[A680c]`, `[A680d]`)
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
| Memory budget | `ctrl_memory.plan` keeps refusing any image past 56 RAMB36. One named override, `8x8-two-interfaces`, lets that point's measurement plan 57.0, and it now refuses that image at 57.5 (below). |
| Tests | The face block's checks run through both adapters, at two interfaces and on the host model, with 24 RTL face arms and 6 model twins. GoogleTest's `Core`, `Face`, `FaceLatency`, `AppFace` and `AppFaceUnacknowledged` hold 97 tests at each interface count; the AECP campaign plants 128 defects, 50 of them the face's. Coverage is 100 % lines and branches with no new exclusion. |
| Docs | `docs/design/MAILBOX_SPLIT.md` "The firmware's writer" (the model, its timing and clauses, and what the datapath holds after a failure) and the verification rows; `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 1; `docs/reference/FR_NFR.md` (the AECP response row's IN_PROGRESS policy); the aecp and ctrl READMEs; `aecp_face.h`. |

**The timing, by clause.** IN_PROGRESS leaves within the service bound of the command. The final response leaves at most `AECP_WAIT_MS` plus the service bound after the command: inside the 120 ms IN_PROGRESS cadence of IEEE 1722.1-2021 9.3.2.6, so no second IN_PROGRESS is owed, and inside its 240 ms. No getter waits, so GET_DYNAMIC_INFO, which carries only getters, never answers IN_PROGRESS (IEEE 1722.1-2021 7.4.76). `FR_NFR.md`'s no-IN_PROGRESS policy now names this one exception.

**Tests for the model.**

- `Core.AChangeThePlatformHasNotAppliedPromisesNothing`: every lock-guarded change refused, its body exactly its lock refusal's; reads answered.
- `Core.AChangeThePlatformHasNotAppliedWaitsUndoneAndIsAnsweredOnce`: pending then success, with a getter, READ_DESCRIPTOR and a second command meanwhile; then each of the six commands timing out at exactly `AECP_WAIT_MS` with the whole core state unchanged and no notification.
- `Core.ALockExpiryIsNotifiedOnceThePlatformAppliedTheRelease`: the expiry's notification held until applied, through a full ring.
- `Face.ALateCommitIsOwedAndPublishedAgainWhole`: timeout with rollback on the model, the datapath ending at the value in force, then recovery.
- `Face.APendingChangeIsAnsweredOnceTheDatapathTakesIt`: pending then success; a notification falling due meanwhile waits and reports the value then in force.
- `Face.APartialAcknowledgementFailsTheChangeUntilEveryInterfaceTakesIt`, `Face.AMissingAcknowledgementFailsTheChangeAndRefusesEveryOther` (the automatic unlock notified once LOCK_HELD is taken), `Face.ALockThatExpiresWhileAChangeWaitsIsNotifiedOnceTaken`.
- Every reviewer probe of rounds 3 and 4 runs unmodified, and each one's own assertion holds. Three fail only their fixture's check of the first frame's status, which the ruling makes IN_PROGRESS.

**The memory figure.** The model adds 1,056 B of `rom` and 224 B of `sram` at every point, against round 4's firmware:

| Point (linked image, planned) | `rom` B, base -> head | `sram` B, base -> head | RAMB36, base -> head |
|---|---:|---:|---:|
| 1x1, one interface | 97,920 -> 104,360 | 45,920 -> 46,256 | 35.5 -> 37.0 |
| 1x1, two interfaces | 99,416 -> 105,944 | 57,312 -> 57,648 | 38.5 -> 40.5 |
| 8x8, one interface | 111,648 -> 118,080 | 86,496 -> 86,832 | 49.0 -> 50.5 |
| 8x8, two interfaces | 113,208 -> 119,736 | 112,656 -> 112,992 | 56.0 -> 57.5, refused: the override allows 57 |

Round 4 left 104 B of `rom` before that point's next bank. The other three points stay within 56. The base is `e76a755a`, linked against the same runtime as the head (built with `-fno-stack-protector`).

## Authoritative references

- #665: ruling 6088423771 (decisions 1 and 2), decisions 6409738976 (D1, D3), assignment 6409739310, rulings 6410169666, 6412739248 and 6421238472, owner clarification 6410301079, round-4 assignment 6417644908; PR #795 reviews R701-4 (6421229873) and R702-4 (6421210118)
- IEEE 1722.1-2021 7.4 (7.4.2 lock, 7.4.5.1, 7.4.7 configuration, 7.4.15.1, 7.4.23 clock source, 7.4.42 counters, 7.4.76), 7.5.2 and 9.3.2.6
- Milan v1.2 5.3.7.3, 5.4.2.2, 5.4.2.12, 5.4.5.2 (Table 5.22), 5.6.1; FR-CTRL-03
- `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 1; `docs/reference/FR_NFR.md` (the AECP rows); `docs/design/MAILBOX_SPLIT.md`; `docs/reference/MAILBOX_CONTRACT.md`; `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3 and 5
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
```

Expected result and pass criteria:

- Every command exits 0 except the last, which refuses the 8x8 two-interface image even with its override (exit 2, "57.5 RAMB36 ... exceeds the 57-RAMB36 budget ledgered for 8x8, two interfaces"). That refusal is this round's STOP.
- The mailbox bench reports 523 Wishbone, 568 AXI4-Lite and 32 cosim checks, and 530, 575 and 488 at two interfaces, with 7 of 7 quick plants.
- The census proves 138 arms and all 43 rules over 217 ports per shape.
- The AECP arms pass 97 tests at each interface count.
- In the firmware self-test, shard 1 catches 528 of 528 and shard 2's AECP campaign 128 of 128.
- Coverage is 100 % of lines and branches over 31 files, with no new exclusion.
- `test_ctrl_memory.py` reports 0 failures under LiteX's own interpreter.
- `test_builder.py` reports one arm not run where no local Arty build report exists.
- `behave` passes 406 scenarios.
- The sweep passes every suite; `tsn_fuzz` declares its field campaigns skipped without tsn-gen.

## Known limitations / out of scope

- The 8x8 two-interface image plans 57.5 RAMB36: the ledgered tile owed to lane S14, and half a tile more that no ruling covers yet. The flip (S13) still requires 56 or fewer at every point. The other three points plan within 56.
- A written commit stays in the face block until the datapath takes it, and `cdc_handshake` holds its value. Firmware cannot withdraw it. After a failed command, the datapath takes the undone value with the late acknowledgement, and the poll then publishes the values in force whole. The datapath ends where the controllers were told, but holds the undone value in between. Withdrawing a held commit would need the datapath side, which the placement switch wires.
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
