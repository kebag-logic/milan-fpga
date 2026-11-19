[A801]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN: the firmware gate (units and every planted-defect campaign), fw_coverage, the twin and its plants, the docs workflow steps and both builder legs pass; the 20 split images differ from the base's in the hold-off's encoding alone; the release image is byte-identical; the CPU budget legs measured on both images change no verdict. `951-redeclare` -> `dev-soft-core`, on the flip train's head `0839453f` (PR #945, not yet merged). This change is the three commits after `0839453f`; until #945 merges, the diff against `dev-soft-core` also shows the train's.

Author packets: [`review-evidence/951-r1/author-r1`](https://github.com/kebag-logic/milan-fpga/tree/951-review-evidence/review-evidence/951-r1) on branch `951-review-evidence` (archive `af4b3079`).

## Linked Issue / roles

Closes #951
Relates to #665

Executor: `[A801]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

After a MAAP conflict, a withdrawn Talker re-declares its changed destination only after `SRP_REDECLARE_CS`. That was 2 x LeaveAllTime plus a JoinTime and THE TRANSMIT's term, 20.23 s at 1x1/1if: #895's accepted reading of IEEE 802.1Q-2018 35.2.2.8. But each LeaveAll period is drawn up to 1.5 x LeaveAllTime (10.7.4.3; Milan v1.2 Table 4.3), so #665's ruling has the hold-off cover two of the longest periods.

| Piece | Change |
|---|---|
| `srp/srp_mbx.c` | `SRP_LEAVEALL_CS` (1000 cs) names LeaveAllTime once, and `create_participants` configures both participants with it (it was the literal `1000`). `SRP_LEAVEALL_LONGEST_CS` is 1.5 times it. `SRP_REDECLARE_CS` is twice that, plus the JoinTime and THE TRANSMIT's term as they were: **3,023 cs at 1x1/1if, 3,027 at 8x8/1if, 3,030 at two interfaces** (2,023, 2,027 and 2,030 before). A compile-time check refuses a hold-off past `held_cs`'s 16 bits. |
| `test/srp_talker.cpp` | The horizon is stated from the clauses, 2 x (10,000 + 10,000 / 2) ms, not from the firmware's names. The two hold-off tests are renamed `ChangedDestinationWaitsTwoLongestLeaveAllPeriods` and `...AfterTheLatestLeave`, with their words restated. The re-allocation's wait is derived from the hold-off (it was a typed 21 s). |
| `test/srp_gate.hpp` | `SrpGate.F895ARangeLostWithdrawsAndTheNewRangeWaitsTheHoldOff`, a range lost to a peer's ANNOUNCE through the composition: the source is still held at 29 s and is declared by 31 s (it was 19 s and 21 s). |
| `test/srp_talker_mutants.py` | Two new plants put back the old value, 2 x LeaveAllTime. `talker-hold-off-two-leavealltime-periods` is caught by `ChangedDestinationWaitsTwoLongestLeaveAllPeriods` ("no Talker of a changed destination is declared before the hold-off ends"). `...-after-a-conflict` is caught by the `SrpGate` conflict test ("a changed destination waits two of the longest LeaveAll periods after the Leave"). The one-LeaveAll and drop-a-term plants are restated on the new terms. 53 Talker plants, each caught at 1x1/1if and 8x8/2if. |
| `test/srp_mutants.py` | Three LeaveTime plants matched the configure call's literal; their needle names `SRP_LEAVEALL_CS` now, the same defect. |
| Docs | `srp/README.md` (the Talker paragraph: two longest periods, the values, the reading before #951), `MAILBOX_SPLIT.md` (`TALKER_DECL`), `SPLIT_CONTROL_MEMORY.md` section 13 (the constant, the images, the rows), `ctrl_service_budget/README.md` (`srp-talker-loss`). |

**A test fails on the old value.** With 2 x LeaveAllTime put back in a scratch copy, four Talker tests fail by name at 1x1/1if and at 8x8/2if, and so does the composed conflict test. For example, the changed destination is declared at 20,630 ms of model time, where the test requires the Leave's time plus 30 s, 30,570 ms.

**The image diff is limited to the value.** Twenty images were linked at the base and at this head: the target platform's four, the size fixture's four and the CPU budget harness's twelve. The base's budget images reproduce the train's recorded hashes, 12 of 12. In every image, `srp_mbx.o` is the only linked input that differs (archives compared by member). The hold-off no longer fits an `addi` immediate: `li a3,2023` becomes `lui a3,0x1; addi a3,a3,-1073`, 4 bytes more in `declare_sources`. What follows it in the map moves 4 bytes, or 8 for `.rodata` by its alignment. Each image was linked again from its own inputs with its relocations kept, and its loadable bytes equal the built image's. With every address field named by its relocation's symbol, head and base differ in exactly those three lines.

**The CPU rows carry.** No code path changes, but the hot code after `declare_sources` fetches 4 bytes later, so the legs were measured on both images at 1x1/1if and 8x8/1if. These were the legs the hold-off reaches (the `valid-destinations` arm) and arm A's groups behind the tightest rows. Every leg exits 0, with no STATED line and no pass over the share. None of the 156 probes changes its verdict, and each image has only arm A's seven `backlog-owed` misses. The table graders print the same output on both trees. In the `valid-destinations` arm at 8x8/1if, rows that wait on a timer's phase move further: `srp.talker_loss` goes from 184.154 to 177.088 ms, of 220. A control image, built in scratch only, has the base's value with one `nop` after its store, so it has the head's placement. It gives 176.954 ms there, and every declaration row of that group equals the head's to the microsecond. Its `srp-talker` follows the head too: 34,434 passes against the head's 34,431 and the base's 33,619, the same count each second, and every row the head's. So the rows follow the code's placement, not the value.

## Authoritative references

- [#665's ruling of 2026-11-19](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7007273447), item 2: two longest LeaveAll periods plus the existing JoinTime and transmit terms, derived and never a mirrored literal; an image diff limited to that value; the Talker tests, mutants and docs restated.
- IEEE 802.1Q-2018 35.2.2.8: no changed FirstValue on a StreamID; at least two LeaveAllTime periods between the Leave and the new declaration.
- IEEE 802.1Q-2018 10.7.4.3: each leavealltimer is drawn in LeaveAllTime < T < 1.5 x LeaveAllTime. Table 10-7: LeaveAllTime 10 s.
- Milan v1.2 Table 4.3: LeaveAll 10 to 15 s.
- #895's acceptance 2 and [its ruling of 2026-11-15 on THE TRANSMIT's figure](https://github.com/kebag-logic/milan-fpga/issues/895#issuecomment-6895331865), items 1 and 2: the JoinTime and transmit terms.
- `sw/firmware/ctrl/srp/README.md` (the Talker declarations), `docs/design/MAILBOX_SPLIT.md` (`TALKER_DECL`), `docs/design/SPLIT_CONTROL_MEMORY.md` section 13.

## How to get into the same state

```sh
git fetch origin 951-redeclare dev-soft-core
git checkout 951-redeclare
git submodule update --init gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
# the repository's pinned toolchain and RV32 SDK (sw/firmware/gtest/README.md, docs/testing/CI_WORKFLOWS.md)
```

## How to validate

```sh
# the firmware: units, every arm and the planted-defect campaigns (the two new Talker plants among them)
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --selftest
python3 sw/firmware/gtest/fw_coverage.py --check
# the two-placement simulation and its plants
make -C tb/verilator/milan_dp twin twin-plants twin-maps twin-maps-plants
# the table graders, on this head and on the base: the same output
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
```

Expected result / pass criteria:
- Every arm passes, and `Talker.ChangedDestinationWaitsTwoLongestLeaveAllPeriods*` and the `SrpGate` conflict test pass at 1x1/1if and 8x8/2if.
- Each campaign reports every defect caught, `talker-hold-off-two-leavealltime-periods` and `...-after-a-conflict` among them, at both points.
- `firmware coverage: PASS`; the twin reports `0 finding(s)`, and every plant is refused by its words.
- `flip_grade.py --check` without `--point` fails at 8x8/2if, as it does at the base: it holds that point.
- For the image diff: link the images at the base and at this head (`tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir`, and the CPU budget harness's `build.firmware` at each point and arm). Then link each again from the inputs its map loads, with `-Wl,-q`, and compare the listings with every relocated field named by its symbol. The relinked loadable bytes equal the built image's; only the hold-off's instruction differs.

## Known limitations / out of scope

- **The reference device's delay after a MAAP conflict is not measured.** Provoking a conflict on it needs bench access, which this change did not have. It is for the bench run.
- **Milan v1.2 Table 4.3 states LeaveAll as 10 to 15 s with a +/-0.5 s tolerance.** The ruling's derivation takes 1.5 x LeaveAllTime, about 30.2 s at one interface, without the tolerance, and this change follows the ruling. A peer drawing at the tolerance's edge would make two periods 31 s.
- **The CPU rows were measured on a subset**, not on every group: the `valid-destinations` arm and five arm A groups at 1x1/1if, four at 8x8/1if. Arm A alone is 99 groups and 714 s simulated at 1x1/1if. The measured figures move: in arm A by up to 0.171 ms, in the timer-phase rows of the `valid-destinations` arm at 8x8/1if by up to 7.1 ms, of a 220 ms bound. No verdict moves.
- **The processor's own path is unchanged.** On the all-fabric image a conflict moves the source to a new Stream ID, declared at once (`MAAP_FABRIC.md`), so no hold-off applies there, and the release image is byte-identical.
- **Not run here:** the full suite sweep (`scripts/run_all_suites.sh`) and the act replica. The change is firmware and tests; the hosted gates and act follow the push.
- The hold-off still starts at the Leave's request and adds the JoinTime and THE TRANSMIT's term, as #895's rulings set them.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the reference device's delay after a conflict is not measured here: no bench access for this change)
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

