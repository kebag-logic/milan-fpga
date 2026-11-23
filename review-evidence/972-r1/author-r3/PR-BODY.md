[A820]

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

GREEN. Every gate passes (the table below), at local head `77a74b2f4e289c5a5a89687e07a6925cfedf6860`.
`pf-972-1` -> `dev-soft-core`; the manager updates PR #974 from these local commits.
The branch starts at #960's reviewed head `dd163e41` and retains the stack pin `715589c1`.

## Linked Issue / roles

Closes #972
Relates to #970, #665, #840

Executor: `[A820]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned; `[R890]` reviewed round 2's head)
External reviewer: `[R<n>]` (to be assigned; `[R889]` reviewed round 2's head)

## Description

A boot used to restart a PHY even when it already held the required advertisement.
The datapath could also transmit before firmware verified the link.
The boot now preserves a correctly negotiating PHY and keeps the split datapath's effective link down from reset through verified publication.

- Firmware skips the restart only when BMCR enables autonegotiation, reset/isolate are clear, and registers 4 and 9 already hold the gigabit-only advertisement. Forced modes, including retained `BMCR=0x2100`, are renegotiated and never published up on the managed gigabit PHY. Existing advertisement readback and negotiated-speed checks remain.
- The two shipping split images with an MDIO pair reset `milan_mac_link_status` to `0xC` (link down, gigabit, full duplex). Its link bit qualifies the gPTP port and mailbox LINK, which firmware MAAP, ADP and SRP follow. LINK_CTRL and the guard cannot override the down status bit. Builds without firmware PHY management retain reset-up behavior. The split does not instantiate fabric MAAP.
- The arm also writes link down for a CPU-only reset. Identity refusal leaves the reset-down status intact. The `linkreset` integration leg observes effective link and actual MAC transmit output at both shipping shapes, with retained PHY clocks, successful publication and refused boot. Its premature-qualification plant fails at both shapes.
- Host tests cover retained healthy negotiation, forced 10/100/1000 modes, isolate/reset, subsequent forced operation and a dropped restart. Five BMCR plants detect those regressions. The reviewer's forced-100 scenario passes here and fails at the previous head.
- ADP tests retain Milan's literal 4,000 ms and 2,000 ms draws. Both grandmaster orders check the advertised grandmaster and available_index. FR_NFR 2.1.1 derives the declared 6.0 s discovery time: 250 ms publication, 30 ms event service, 4,000 ms draw, 30 ms expiry service and 1 ms egress; the 41.94 ms link-guard settle fits inside publication. The resulting bound is 4,311 ms.

The separate stack PR #36 strengthens its GM_CHANGE assertion to require exactly one fresh draw, with a no-draw plant. It changes no production source or constants and requires no parent pin change.

## Authoritative references

- #972 acceptance and its manager scope decision; #970's corrected discovery acceptance; #840 gigabit-only behavior.
- IEEE 802.3-2022 22.2.4.1, 22.2.4.2.13 and 28.2.4.1.3.
- IEEE 1722.1-2021 6.2.2.16, 6.2.4 and 6.2.5; Milan v1.2 5.6.3.5.2, 5.6.3.5.3, 5.6.3.5.7 and Tables 5.50/5.51.
- IEEE 802.1AS-2020 11.2.19; REQUIREMENTS REQ-MAC-03; FR_NFR 2.1.1; the register map and platform PHY contract.

## How to get into the same state

After the manager pushes the local head:

```sh
git fetch origin pull/974/head:972-link-once
git switch 972-link-once
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

## How to validate

Run each firmware shard in its own checkout and build directory:

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 1/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 2/4
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 3/4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
make -C tb/verilator/milan_dp linkreset linkreset-plants
make -C tb/verilator/milan_dp twin twin-plants twin-maps twin-maps-plants
python3 tb/verilator/ctrl_split_boot/run.py --build-dir <work>/1x1
python3 tb/verilator/ctrl_split_boot/run.py --build-dir <work>/8x8 --shape endstation_ax7101_8x8
python3 tb/verilator/ctrl_split_boot/run.py --build-dir <work>/plants --self-test
python3 tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <work>/images
```

Every shard must pass and every registered plant must be caught. The link-reset leg must show four passing arms and two caught plants. Both boot shapes, the twin, image ledgers and documentation gates must pass.

| Gate | Head | Result |
|---|---|---|
| Firmware gate, four shards (`test_ctrl_firmware.py --require-rv32 --self-test --shard k/4`) | `77a74b2f` | PASS: 75 of 75 suite verdicts; control campaign 837 of 837 caught (round 2's 832 and the five BMCR plants); no `[FAIL]` or escaped line |
| Native suite sweep, four shards (`scripts/run_all_suites.sh --shard k/4`) | `77a74b2f` | shards 0, 1 and 3 PASS; shard 2 rerun whole after the host crash, PASS (17 of 17). In all: 65 of 65 suites (15, 17, 17, 16), 2,713,969 checks, 0 in-suite failures, 0 timed out |
| `linkreset` and `linkreset-plants` | `77a74b2f` | 4 of 4 arms PASS; 2 of 2 plants caught |
| Split boot simulation, both shapes and `--self-test` | `77a74b2f` | 1x1 and 8x8 PASS: ready 27.940 / 67.214 ms; the arm's link down at 2.637 / 4.437 ms, before the first frame at 27.096 / 66.163 ms; 6 of 6 native controls, 7 of 7 plants, 8 of 8 placement controls |
| The reviewers' forced scenario (`focused.py`) | `77a74b2f` | PASS here; their receipt fails it at `0f508a01` |
| fw_coverage `--selftest`, `--check` | `d9e1d728` | PASS, 40 files |
| Twin, `twin-plants`, `twin-maps`, `twin-maps-plants` | `d9e1d728` | PASS, 0 findings |
| `plat_ledger` and the image diff against round 2 | `fc7504f1` | PASS; RAMB36 45 / 46 / 58 / 63 unchanged; rom +40 B at each point; only `ctrl_plat_phy.o` differs; size fixtures identical |
| CPU budget legs, 9 groups, 1x1/1if and 8x8/1if | `fc7504f1` | harness images byte-identical to round 2; 63 of 63 probes equal at each shape; 0 verdicts changed; 0 misses |
| Routes, three directives at each shape (the gating recipe) | `93d9eaaf` | all six meet #818 at every corner. 1x1: ExtraPostPlacementOpt +0.331 / +0.031 ns (best), AltSpreadLogic_high +0.130 / +0.036, ExtraTimingOpt +0.133 / +0.036. 8x8: ExtraPostPlacementOpt +0.176 / +0.036 (best), AltSpreadLogic_high +0.150 / +0.036, ExtraTimingOpt +0.059 / +0.036 (worst-corner WNS / WHS). Routed `link_status_storage` `4'd12` in all six |
| Synthesis portability (Yosys) | `77a74b2f` | PASS |
| RTL lint, behaviour scenarios, xvlog | `77a74b2f` | lint PASS (89 of ratchet 89); 511 of 511 scenarios; xvlog 0 findings |
| Docs workflow steps | `77a74b2f` | 104 of 104 |
| Builder legs 0 and 1 | `d9e1d728` | PASS, each with the one NOT RUN arm the tree declares on this host (as round 2) |
| tsn-c-stack `validate.py --graphs`, `baremetal.py` | `5585226` | rc 0, 28 of 28 gates; 479 of 479 plants caught; rc 0 |

Heads: the commits after the code head `93d9eaaf` change test code, the leg, documentation and comments, no firmware or gateware code. The commits after `fc7504f1` and `d9e1d728` change no file those gates read but comments, READMEs and test-only idiom fixes; the gates that read them ran at `77a74b2f`. The host crashed at 00:39 during the native sweep; shard 2, cut before its verdict, was rerun whole from a cleaned clone, and only that rerun is counted.

## Known limitations / out of scope

- The 8x8/1if ROM uses all 139,264 bytes of its 34 tiles; it remains within the existing 58-RAMB36 firmware ledger, with no ROM headroom. Approved CPU and resource bounds are unchanged.
- The focused link-reset leg uses the product datapath and firmware CSR policy, with modeled status crossings and retained clocks. It does not model the physical PHY or full CPU. It runs by name, outside the hosted ordinary-case inventory.
- Fixed-seed ADP spread checks detect the planted narrowing; they are not a statistical proof over all random sequences.
- Physical discovery acceptance remains the manager's bench rerun after merge. All-fabric PHY initialization is unchanged. Review, hosted checks, merge-candidate validation and containment remain pending.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (physical rerun pending)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
