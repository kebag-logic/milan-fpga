[A680d]

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

GREEN: every gate rc 0 at head `d33a5adc`, each run there or at an ancestor that differs only in what the gate does not read; the Verilator sweep passes 64 of 64 suites (2,191,124 checks); `665-s1-faces` -> `dev-soft-core`.

Round 4 answers R701-3 and R702-3. A response or notification now promises a face value only once the datapath has acknowledged it. The other acceptance items stand as in round 3. The one point over the 56-RAMB36 budget, 8x8 with two interfaces at 57, is ledgered and owed to lane S14. #665 itself stays open.

## Linked Issue / roles

Relates to #665 (lane S1: assignment 6409739310, rulings 6410169666 and 6412739248, round-4 assignment 6417644908). This PR is one lane of #665 and must not close it.

Executor: `[A680d]` (rounds 1 to 3: `[A680]`, `[A680b]`, `[A680c]`)
Internal cleared-context reviewer: `[R701]`
External reviewer: `[R702]`

## Description

The split placement removes the whole processor wrapper (`KL_pp_shadow`, ruling 6088423771, decision 1). This branch decides each of its 217 ports and adds what the mailbox must still carry, as contract 2.3, an additive minor. The all-fabric build is unchanged: its export is digest-identical for every shipped config.

| Piece | What changed |
|---|---|
| Port census | `sw/mailbox/census_ports.py` names each `pp_shadow` port under one class in all six shapes: C 25, F 28, R 34, E 6, M 14, G 110. A G output's cone may end only at the CSR block's processor-status inputs, the twenty memory-master outputs, or `pp_maap_shim` while that shim feeds `pp_shadow` alone. It stops at the map writer's 25 nets, which go with the wrapper; the placement switch must pass the census without that exclusion. There are 12 rules with 18 plants, which ride on existing netlists. |
| Contract 2.3 | `sw/mailbox/mailbox.yaml`, with `mailbox_face.py` the face block's generator and new checks and arms. Each interface's face block holds the settings, published by one commit per interface with a bounded acknowledgement. There are four request windows (CTR, AMAP, EDIT, GSI) with tag and timeout, and four events (COUNTERS_CHANGED per descriptor with a 1,000 ms holdoff, AVB_INFO_CHANGED, AS_PATH_CHANGED, AMAP_LIVE_WRITE). |
| RTL | `KL_mbx` is regenerated with the face ports, and `KL_mbx_evt` gains the face events. `CtrlMailbox` names every face port and leaves it unread, its inputs idle. `milan_datapath.sv` is not touched. |
| Firmware | `aecp_face.c` answers the AECP owner's `changed`, `applied`, `format`, `counters`, `stream` and `avb` ports on the face block. A setting is written and committed, and its acknowledgement awaited within a bound. A lock change and a lock expiry are published (`AECP_CHANGE_LOCK`). The store's restore and NVM status are written before AECP opens and on each change. The driver decodes no field of an event type the contract does not define. |
| Apply acknowledgement (round 4) | The core asks the new `applied` port, false while an interface owes a publication or holds a commit not yet acknowledged. After a state-changing command, false means ENTITY_MISBEHAVING and no notification. Before one, false means ENTITY_MISBEHAVING with its data echoed and nothing changed, so no second value joins the owed one. A lock expiry with `applied` false sends no unlock notification. `ctrl_app_open_aecp` opens AECP only once every interface has acknowledged the initial publication. |
| Memory budget | `ctrl_memory.plan` keeps refusing any image past 56 RAMB36. One named override, `8x8-two-interfaces`, lets that point's measurement plan 57.0. The override recognises its image by the image's own symbols and is refused on every other one. The SoC build names none. `docs/design/SPLIT_CONTROL_MEMORY.md` ledgers the tile as owed to lane S14 (ruling 6412739248). |
| Tests | The face block's checks run through both adapters, at two interfaces and on the host model, with 24 RTL face arms and 6 model twins. GoogleTest adds `Face`, `FaceLatency`, `AppFace` and `AppFaceUnacknowledged`, with 30 AECP face defects among the campaign's 108. D9 requires every field of an undefined event to stay 0. The face's timing check stays bounded when a defect keeps a request from opening, so the whole `make mutants` campaign finishes (199 of 199). `test_ctrl_memory.py` plants the override on each other point. Coverage is 100 % lines and branches. |
| Docs | `docs/design/MAILBOX_SPLIT.md` "The processor's other faces" (the writer's ordering and failure path, the verification rows at this head) and the `KL_mbx` area with the face block; `docs/design/SPLIT_CONTROL_MEMORY.md` the override and the ledger; the placement contract; the ctrl, aecp and mbx READMEs. |

**The failure path, chosen by clause.** The project keeps its no-IN_PROGRESS policy and IEEE 1722.1-2021 9.3.2.6's 240 ms response deadline (`docs/reference/FR_NFR.md`, the AECP rows). So a commit not acknowledged in its bound is answered within the same service bound with ENTITY_MISBEHAVING. That is the status the core already gives a datapath that does not answer in its bound: an unanswered observation, or an expired START_STREAMING. The value stays in the held block and reaches the datapath if and when it acknowledges. A read answered meanwhile reports that value. Reads, registrations and other notifications continue, and changes are taken again once the poll has published the interface whole.

**Tests for the path.**

- `Face.ALateCommitIsOwedAndPublishedAgainWhole` now checks ordering:
  - the command whose commit is late answers ENTITY_MISBEHAVING and notifies no one;
  - a second change is refused, writing nothing and leaving the held value;
  - after recovery, the next change is committed and acknowledged before its response and its notification.
- `Face.APartialAcknowledgementFailsTheChangeUntilEveryInterfaceTakesIt`: one interface acknowledges, the other does not.
- `Face.AMissingAcknowledgementRefusesEveryChangeAndNotifiesNothing`:
  - all ten state-changing commands refused within the service bound;
  - reads answered;
  - a lock expiry with no notification.
- `AppFaceUnacknowledged.AecpOpensOnlyOnceTheInitialPublicationIsAcknowledged`: AECP stays closed until the initial publication is acknowledged.
- `Core.AChangeThePlatformHasNotAppliedPromisesNothing`: the core's side on a mock port.

Measured:

| Point (linked image, planned) | `rom` B, base -> head | `sram` B, base -> head | RAMB36, base -> head |
|---|---:|---:|---:|
| 1x1, one interface | 97,920 -> 103,304 | 45,920 -> 46,032 | 35.5 -> 37.0 |
| 1x1, two interfaces | 99,416 -> 104,888 | 57,312 -> 57,424 | 38.5 -> 40.5 |
| 8x8, one interface | 111,648 -> 117,024 | 86,496 -> 86,608 | 49.0 -> 50.5 |
| 8x8, two interfaces | 113,208 -> 118,680 | 112,656 -> 112,768 | 56.0 -> 57.0, ledgered, owed to S14 |

The acknowledgement path adds 392 to 400 B of `rom` and 16 B of `sram` at each point. At 8x8 with one interface it doubles `rom`'s last bank, from 50.0 to 50.5 RAMB36. At 8x8 with two interfaces 104 B of `rom` remain before that point would plan 57.5, which the override refuses. The five largest `.bss` objects are unchanged from the base at every point. At 8x8 with two interfaces they are:

- the lwSRP arena, 48,064;
- `nvm_stage`, 13,264;
- the AECP values, 11,753;
- the application, 10,056;
- SRP, 5,896.

Both images of each point link against one runtime: `ctrl_image_runtime.py`'s archives, built with `-fno-stack-protector` added to each compile (the flag every firmware object already gets). The stack-protected runtime the host's RV32 SDK builds does not link at the base or the head. The target runtime is lane S3's (ruling 6412739248 item 2).

`KL_mbx` out of context (the recipe of `MAILBOX_SPLIT.md` "Measured area"): 3,585 -> 5,515 LUT, 4,114 -> 7,632 FF, 1 RAMB36 and 10 RAMB18 unchanged, WNS +0.123 ns at 10 ns. Round 4 changes only comments in the mailbox RTL. Yosys's cell counts for `KL_mbx`, `KL_mbx_wb` and `KL_mbx_axil` are the measured head's (420,989, 5 and 136).

Material choices, each visible to the placement switch's comparison:
- `RS_CAUSE` and `CAUSE` are written 0.
- `BACKED` means the store's boot walk has ended, and `IMG_VALID` that it holds an authoritative image.
- An output streams while it holds its SRP licence (Milan v1.2 5.3.7.3).
- `AMAP_LIVE_WRITE` is counted only.
- The owner does not drive the `EDIT` window, so applying the maps is the placement switch's.
- While any face commit is held, every state-changing AEM command is refused, not only those whose values the face carries.

## Authoritative references

- #665: ruling 6088423771 (decisions 1 and 2), decisions 6409738976 (D1, D3), assignment 6409739310, rulings 6410169666 and 6412739248, owner clarification 6410301079, round-4 assignment 6417644908; PR #795 reviews R701-3 (6417591484) and R702-3 (6417635453)
- IEEE 1722.1-2021 7.4 (7.4.2 lock, 7.4.7 configuration, 7.4.23 clock source, 7.4.42 counters), 7.5.2 and 9.3.2.6
- Milan v1.2 5.3.7.3, 5.4.2.2, 5.4.2.12, 5.4.5.2 (Table 5.22), 5.6.1
- `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 1; `docs/reference/FR_NFR.md` (the AECP response and no-IN_PROGRESS rows); `docs/design/MAILBOX_SPLIT.md`; `docs/reference/MAILBOX_CONTRACT.md`; `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3 and 5
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
make -C tb/verilator/mbx mutants
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
python3 scripts/lint_rtl.py --check
python3 scripts/xvlog_gate.py --check
syn/yosys/run.sh --top KL_mbx --top KL_mbx_wb --top KL_mbx_axil
(cd tests && behave --no-capture -f plain)
bash scripts/run_all_suites.sh "$OUT/sweep" --wait
python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml \
  --interfaces 2 --with-aecp --layout split --ledgered-point 8x8-two-interfaces --output "$OUT/image" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
python3 sw/litex/ctrl_memory.py plan "$OUT/image/ctrl_app.elf" --stage-bytes 13264
```

Expected result and pass criteria:

- Every command exits 0 except the last. It refuses the 8x8 two-interface image without its override (exit 2, "allocation over budget: 57 RAMB36 ... exceeds the 56-RAMB36 budget"). The command before it plans that image at 57.0 RAMB36 under `8x8-two-interfaces`.
- The mailbox bench reports 523 Wishbone, 568 AXI4-Lite and 32 cosim checks, and 530, 575 and 488 at two interfaces; the AXI4-Lite build's own 45 handshake checks are the difference. `make mutants` catches 199 of 199.
- The census proves 138 arms and all 43 rules.
- The AECP arms pass 93 tests at each interface count.
- In the firmware self-test, shard 1 catches 528 of 528 and shard 2's AECP campaign 108 of 108.
- `test_ctrl_memory.py` reports 0 failures.
- `test_builder.py` reports one arm not run where no local Arty build report exists.
- `behave` passes 406 scenarios.
- The sweep passes 64 suites; `tsn_fuzz` declares its field campaigns skipped without tsn-gen.

## Known limitations / out of scope

- The 8x8 two-interface image plans 57 RAMB36, one tile over the 56-RAMB36 budget. It is ledgered and owed to lane S14 (hybrid XIP), with 104 B of `rom` left before 57.5. The flip (S13) still requires 56 or fewer at every point. The other three points plan within 56.
- The image figures are planned by `ctrl_memory.plan`. This branch maps none of them out of context.
- The image measurements use a runtime built with `-fno-stack-protector`. The stack-protected runtime the host SDK builds is lane S3's to resolve.
- The face block's datapath side is unread until the placement switch connects it, with its clock crossing. The acknowledgement path is tested on the host model, not on a datapath.
- A datapath that never acknowledges keeps every state-changing command refused, and AECP closed if it held the initial publication; no timeout releases a held commit, because the RTL holds it until the acknowledgement.
- The audio maps are not applied through the `EDIT` window.
- `GET_AS_PATH` stays the platform's port.
- `docs/testing/TESTING.md:753` counts the memory test's in-tree mutants (forty-four). The override's eleven plants run as a probe, not as in-tree mutants, because that file is in a release lane's file map.
- `test_builder.py`'s gate 11 needs a local Arty build report and did not run here; every other gate passed.
- No changelog entry: the build is default-off, as for the earlier mailbox lanes.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
