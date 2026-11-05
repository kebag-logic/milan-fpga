[A731]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at `992c3d7b`: the full Verilator sweep 65 of 65 suites (four shards, 2,192,475 checks, 0 failures), every `run:` step of `docs.yml` that runs off the hosted runner (64 of 64; 31 hosted-only steps not run, each with its reason), the firmware self-test, coverage, the builder, behave, the LiteX SoC simulations, Yosys and the lint ratchet. `839-boot-source-address` -> `dev`

## Linked Issue / roles

Relates to #839

Maintainer decision (2026-11-05): both readings are accepted. There is no register-map generator in the tree, so the sequencing is documented on the hand-maintained `MAC_ADDR_LO/HI` rows. Every simulated boot gate is green. The issue stays open until a capture of the first frames of a hardware boot shows no all-zero source address; this PR relates to #839.

Executor: `[A731]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

The first MSRP PDU after every boot left with source address 00:00:00:00:00:00. The processor's SRP engine runs from reset and builds its first MRPDU at the 200 ms join tick (Milan v1.2 Table 4.3), and the firmware writes the station MAC only in `configure_fabric()`, after the BIOS. The new `bootsa` leg reproduces it on the base: one MSRP PDU with a zero source at cycle 20198, before `configure_fabric()` completes the station MAC at cycle 40088.

**The fix holds each transmitter until the station MAC is written** (acceptance 1's first option), and stamps the control lane's source address. The firmware boot order is unchanged.

| Piece | Where | What |
|---|---|---|
| The pair's own sequencing | `hdl/milan/milan_datapath.sv`, `mac_addr_seq` | Each half of `MAC_ADDR_LO/HI` records its first write since reset, read off the CSR slave's own write handshake (`milan_csr` asserts AWREADY on the cycle it commits a write, ignores WSTRB and decodes the same 16-bit address). `tx_sa_ok_w` is 1 once both halves are written, in either order, until reset. `milan_csr` is unchanged |
| The transmit gate | `milan_datapath.sv`, beside the TX arbiters | The processor's control lane (SRP, ADP, ACMP, AECP), MAAP, the AAF talkers and the CRF talker see `tready` 0 and their arbiters see `tvalid` 0 until `tx_sa_ok_w`. At each source rather than at the MAC boundary, so no arbiter sees a refused beat and `A_TXARB_DIAG` stays quiet. It only rises, so it never cuts a frame |
| The control-lane stamp | `milan_datapath.sv`, `ctl_sa_stamp` | Octets 6 to 11 of every control-lane frame are taken from the CSR as they leave. The hold alone is not enough: the processor's SRP encoder writes octets 6 to 11 into its TX slot when it builds the frame, so the boot's first PDU would otherwise be released with the reset address. AAF, CRF and MAAP form octets 6 to 11 from the CSR on the beat they emit, so the hold covers them |
| gPTP | not held | Its source address is the builder's `platform.mac_address` in its program ROM, the value firmware writes to the pair, and the builder refuses a zero or group address. Its path to the MAC stays free of runtime gates (the boot contract) |
| The `bootsa` leg | `tb/verilator/milan_dp/sim_boot_sa.cpp`, `gen_boot_fw.py`, `bootsa_probes.vlt` | The shipping 1x1 datapath booted through `milan_init()`'s own stage order, with the firmware's own `configure_fabric()` and `entity_advertise()` compiled in (copied out of `milan_baremetal.c`, CSR access routed to the harness). Every frame at `m_axis_mac_tx` is graded, up to and past the first ENTITY_AVAILABLE and its re-advertisement, with AECP and ACMP answers and an AAF stream on the wire. Two more boots write one half alone, then the other |
| Seven planted controls | `tb/verilator/milan_dp/bootsa_mutants.py` | The defect as shipped (no hold, no stamp: the old order), the hold alone, the stamp alone, either half alone completing the pair, the stamp on the destination octets, and the stamp's beat position kept across a frame's end. Each must fail the leg by every check it names |
| Harnesses | `capture_coherence/sim_dp.cpp`, `milan_dp/sim_nxn.cpp`, `milan_dp/sim_gptp.cpp`, `milan_dp_render/sim_tdm8_render.cpp` | They never wrote the station MAC; they now write it after reset, as `configure_fabric()` does, keeping the all-zero address their stream IDs root in. The render leg writes it again after its four mid-test resets, before the rebind that needs the processor's frames: a reset returns the pair to unwritten, as it returns the CSR to zero, and in the product the datapath resets only with the system, after which firmware writes the pair again |
| Docs | `docs/reference/REGISTER_MAP.md` (`MAC_ADDR_LO/HI` rows), `docs/integration/BAREMETAL_FIRMWARE.md`, `docs/testing/TESTING.md`, `tb/verilator/milan_dp/README.md`, `CHANGELOG.md` | The sequencing, the hold, the stamp, the leg and its campaign. No field, address or reset value changes; VERSION stays `0x0002_0060` |

No new top-level port: the module's 140 port declarations are identical at base and head. No submodule change.

Area, out-of-context synthesis of `milan_datapath` (`syn/ooc/milan_datapath_ooc.tcl`, its default 1x1 shape, same instrument at both commits): LUTs 45,176 to 45,275 (+99), registers 40,222 to 40,233 (+11), F7 muxes +115, F8 muxes +5, block RAM and DSP unchanged, OOC WNS unchanged (-4.914 ns at 10 ns, the base's own figure).

## Authoritative references

- IEEE 802.1AC-2016 11.1: "The source_address parameter is the individual address of the source MSAP."
- IEEE 802.1Q-2022 6.8.1: the EISS source_address is as defined for the ISS (6.6).
- IEEE 802.3-2022 2.3.1.2: "If the source_address parameter is omitted, the local MAC sublayer entity will insert a value associated with that entity" (the stamp).
- Milan v1.2 4.2.7 (MRP, MSRP, MVRP) and Table 4.3 (joinTime 200 ms); Milan v1.2 5.6.3.5.2 (TMR_DELAY before the first ENTITY_AVAILABLE).
- IEEE 802.1AS-2011 11.3.4: Sync, Follow_Up and Pdelay messages use the egress port's MAC address as the source address.
- Issue #839 acceptance 1 to 4; `docs/reference/REGISTER_MAP.md` `MAC_ADDR_LO/HI`; `docs/integration/BAREMETAL_FIRMWARE.md` (boot contract).

## How to get into the same state

```sh
git fetch origin
git switch 839-boot-source-address
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
```

## How to validate

```sh
make -C tb/verilator/milan_dp bootsa
make -C tb/verilator/milan_dp bootsa-mutants
make -C tb/verilator/milan_dp gptp gptp-lat
make -C tb/verilator/milan_dp_render
suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$suite_logs"
syn/yosys/run.sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/builder/test_builder.py --require-rv32
cd tests && behave
```

Expected result / pass criteria: every command exits 0. `bootsa` ends `== bootsa: checks: 40   failures: 0 ==` with `[ ok ] [BOOTSA] no frame carries the all-zero source address`; `bootsa-mutants` ends `8 checks: 8 PASS, 0 FAIL` (the clean leg and seven controls, each caught by its named checks).

Evidence at head `992c3d7bb37f4ade0b151c17d718baed0e119753`, base `604899c08ff1cd1830e1dd08b733109ef852400c`, each gate on a clean clone of the head:

| Gate | Result |
|---|---|
| `scripts/run_all_suites.sh`, four shards | 15 + 17 + 17 + 16 = 65 of 65 suites, 0 failed, 0 timed out, 0 in-suite failures; `bootsa` `checks: 40 failures: 0`; gptp and gptp-lat 210 of 210 each; `tdm8_render` 263 of 263 |
| `make -C tb/verilator/milan_dp bootsa-mutants` | `8 checks: 8 PASS, 0 FAIL`: the clean leg, and seven controls each caught by every check it names |
| The same leg against the base RTL | fails 9 of 40, first `#0 MSRP cycle 20198 source 000000000000 (before the MAC write)` |
| `test_ctrl_firmware.py --require-rv32 --self-test`, four shards; `test_ctrl_nvm.py`; `fw_rv32_selftest.py`; `tally_selftest.py` | all PASS (`mutants: 523 of 523 caught` in shard 1) |
| `fw_coverage.py --selftest`, `--check` | `firmware coverage: PASS (30 files)` |
| `test_builder.py --require-rv32` (`docs.yml` legs) and `--require-elaboration --require-rv32` (`elaborate.yml` legs) | all four exit 0; the arms not run are listed by the builder with their reasons (host tooling, a calibration build tree), none for a missing toolchain |
| `run_litex_sims.sh --selftest` and its three legs | 16 of 16; all eight members PASS |
| `cd tests && behave` | 508 scenarios, 2330 steps passed |
| Every `run:` step of `docs.yml` | 64 ran, all exit 0; 31 hosted-only, not run, each with its reason |
| `syn/yosys/run.sh`; `scripts/lint_rtl.py --check --self-test`; `scripts/pp_srcs.py --check --selftest`; `git diff --check` against the merge base | all exit 0 |

`scripts/docs_inventory.py --check` was not run: the script is not in the tree at the base or the head.

## Known limitations / out of scope

- **Acceptance 3, "documented through the register-map generator".** The tree has no register-map generator: `docs/reference/REGISTER_MAP.md` is maintained by hand (`scripts/gen_toc.py` keeps only its contents list), and the builder generates reset words for the `0x680` group only. This change alters no address, field or reset value, so nothing generated changes; the sequencing is documented on the `MAC_ADDR_LO/HI` rows. A maintainer decides whether that meets the item.
- **Acceptance 4, "the boot runs".** Run here in simulation: the `bootsa` boot through the firmware's own `configure_fabric()` and `entity_advertise()`, the builder's elaboration legs and the LiteX SoC simulation legs. Not run: a boot on hardware with a capture of its first frames. This lane has no bench access.
- The leg does not drive an order no shipping firmware uses, such as enabling MAAP, AAF or CRF before the station MAC is written (the hold covers it), and does not model `nvm_boot()`'s own saved-state CSR traffic.
- Rewriting the station MAC after boot is not atomic across the two words: a frame stamped between the two writes carries half of each. Firmware writes the pair once per boot.
- The area figure is the out-of-context synthesis, not the routed shipping image.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (1 and 2 with evidence; 3 and 4 as read above, pending a maintainer)
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
