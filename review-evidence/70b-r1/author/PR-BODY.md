[A704]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN for review -- every local gate rc 0 at the head `b6a1c189` (100-gate docs battery 0 nonzero; builder bank, firmware unit, nvm_cosim, milan_dp legs and mutants, processor controls, capture and service re-measures as tabled below) -- `70-boot-report-link` -> `dev`

## Linked Issue / roles

Relates to #70

The bench items of #70 remain open, so this PR does not close it.

Executor: `[A704]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

Two recorded firmware defects on #70, and the desk check of the volatile set. No RTL changes, so there is no sweep and no route.

| Piece | Change | Check that fails without it |
|---|---|---|
| The enable report (D3 section 5.3, change 3) | `entity_advertise()` prints that it requested the enable and that the fabric holds it until the restore releases it, never "fabric entity enabled". At its timeout the bounded restore wait prints that the restore has not reached its terminal and that the fabric holds the entity enable. The two enable writes, the single choke point and the verdict data flow are unchanged. | `test_boot_walk.py`: every boot path reports one request and no enabled entity, including two new stalled-restore paths (`--walk-stall`). Mutants `enable_line_claims_enabled` and `timeout_line_holds_unsaid` restore dev's lines. |
| The PHY link on the persistence-disabled path | `nvm_boot()` sets `phy_live` first. The heartbeat's no-writer branch polls the PHY, and the disabled path installs the console idle hook. An admitted writer's heartbeat is textually dev's. After a CSR identity mismatch nothing touches the MDIO pins. | `test_phy_firmware.py` boot-path arms, in a PHY build of the host harness with the shared pin-level peer (`phy_peer.h`). The shipping and disabled paths must publish the peer's 1000BASE-T full duplex at least every 250 ms of console idle; the identity-mismatch path must make no MDIO transfer. Five mutants, `phy_behind_the_writer` (dev's heartbeat) among them. |
| The volatile set (FASTCONNECT section 16; D3 section 9) | `[VOLATILE]` in milan_dp's dynmap leg. It boots over a window holding a saved entity name. Controller A registers, sets IDENTIFY 255 and locks, each proved first. A planted power cycle follows, with the window kept and the restore walked. Then the saved name is back, IDENTIFY reads 0, the lock is clear and the registry is empty. | `dynmap_mutants.py` arms 64 to 66 delete the lock's, the registry's and IDENTIFY's reset terms in a processor copy (`PP_DIR`). Each fails its own `[VOLATILE]` check. |
| The IDENTIFY exclusion control (FASTCONNECT 16) | Already in the pinned processor: `protocol-processor/tb/pp_top/d3_mutants.py` arm `identify_is_a_change`, caught by D3S7. Cited, and re-run here. | |
| UART readers | The service-budget grader (`tb/verilator/fw_service_budget/run.py`) requires the new line. Its `oracle.json` is regenerated through `gen_oracle.py` from fresh runs, and the boot-walk host check and the deployment guide move with it. | |
| Firmware-derived records | `tb/verilator/nvm_capture_cpu/measurements.json` is re-measured at the new firmware digest, and SNAPSHOT_OWNERSHIP sections 18 and 20 are refreshed from it. The CI command table re-pins the four declared scripts this PR changes that were in sync at dev. | `check_nvm_capture.py` |

The UART lines, old and new:

```text
old: Milan baremetal: fabric entity enabled; UART diagnostics ready.
new: Milan baremetal: fabric entity enable requested; the fabric holds it until the restore releases it; UART diagnostics ready.
old: Milan NVM: the restore walk did not sequence in time.
new: Milan NVM: the restore walk has not reached its terminal; the fabric holds the entity enable until it does.
```

A reader outside this repository that waits for either old line must move to the new one.

The capture was re-measured at the new firmware digest: six arms of 16 captures by the harness's README. The 8x8 contract maximum is 13.86052 ms against the 24.5 ms limit (half the 49 ms hold floor), a 10.63948 ms margin and 3.5352x the floor. The previous receipt had 13.86328 ms; `nvm_capture()` is unchanged, and the code layout moved. The 1x1 maximum is 3.96490 ms, and the non-contract 8x8 at 100 MHz is 10.42630 ms.

Service timing on the product CPU, against a dev `1e80128f` run of the same 1x1 plan: boot to the enable -0.011 ms, each commit +0.09 ms, worst heartbeat gap +0.085 ms. Budget findings are none on either side. An admitted writer's heartbeat is textually dev's.

Firmware object (`riscv32-linux-gcc` 14.3.0, the 1x1 headers with the MDIO path compiled in): text 17,451 to 17,697 B (+246), bss 104 to 108 B (+4), data unchanged.

## Authoritative references

- `docs/design/SAVED_STATE_MATERIALIZATION.md` section 5.3 change 3 and section 9.
- `docs/design/SAVED_STATE_FASTCONNECT.md` section 16: the volatile-set row and the IDENTIFY exclusion row.
- Milan v1.2 5.3.4.1 (the lock is cleared by a power cycle), 5.3.4.2 (the registered-controller list is cleared by a power cycle) and 5.3.12 (IDENTIFY 0 after reset).
- IEEE 1722.1-2021 7.4.2 (LOCK_ENTITY), 7.4.25 and 7.4.26 (SET_CONTROL, GET_CONTROL) and 7.4.37 (REGISTER_UNSOLICITED_NOTIFICATION).
- `docs/integration/BAREMETAL_FIRMWARE.md` (the boot and PHY sections), `tb/verilator/milan_dp/README.md` (`[VOLATILE]`, rows 64 to 66).

## How to get into the same state

```sh
git fetch origin
git checkout 70-boot-report-link
git submodule update --init --recursive
```

The RV32 and product-CPU steps need the pinned RV32 SDK and the product LiteX environment, as `tb/verilator/nvm_capture_cpu/README.md` and `tb/verilator/fw_service_budget/README.md` describe.

## How to validate

```sh
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
python3 sw/firmware/nvm_hosttest/test_phy_firmware.py
make -C tb/verilator/milan_dp dynmap
cd tb/verilator/milan_dp && python3 dynmap_mutants.py --jobs 3 64 65 66 && cd -
cd protocol-processor && python3 tb/pp_top/d3_mutants.py --output "$(mktemp -d)" --only identify_is_a_change && cd -
python3 scripts/check_nvm_capture.py
python3 -B tb/verilator/fw_service_budget/run.py --self-test
python3 sw/builder/test_builder.py --require-rv32
```

Expected result / pass criteria: every command exits 0. The host gate ends `saved-state writer gate: OK across 5 shape(s), and every planted defect reddened`. The PHY test ends `PHY_BOOT_OK`. The dynmap leg reads `checks: 711   failures: 0`. The mutant driver reads `4 checks: 4 PASS, 0 FAIL`. The processor control reads `1 of 1 KILLED`. The capture gate prints `PASS`.

| Gate | Commit | Result |
|---|---|---|
| Docs workflow battery, 100 gates (behave, `check_nvm_capture.py`, the host firmware gate, the PHY test, the service-budget self-test and `baremetal_uart_smoke.py --self-test` among them) | `b6a1c189` | 0 nonzero; behave 495 scenarios passed |
| `sw/builder/test_builder.py --require-rv32` | `c71364bd` | rc 0; one arm NOT RUN (gate 11 needs an Arty build tree this host lacks). Nothing it reads changed after |
| Firmware-unit job (`test_ctrl_firmware.py --require-rv32 --self-test`, `test_ctrl_nvm.py`, `fw_coverage.py --selftest` and `--check`, three self-tests) | `dc7b1417` | 7 of 7 rc 0. None reads the bare-metal firmware or anything changed after |
| `make -C tb/verilator/nvm_cosim` | `c71364bd` | 465 checks pass, 39 of 39 mutants killed (dev also 465) |
| milan_dp `dynmap`, `maprec8`, `maprec4` | `1767346a` | 711/0, 219/0, 137/0 |
| `dynmap_mutants.py 64 65 66` | `c71364bd` | 4 of 4 PASS |
| processor `d3_mutants.py`: `identify_is_a_change`; the three volatile reset arms | pin `f65c8ff7` | 1 of 1 and 3 of 3 KILLED |
| Capture re-measure (6 arms) and service-budget runs (3) with `gen_oracle.py` twice | `c71364bd` | all rc 0; the oracle repeat is byte-identical |
| `scripts/ci_tool_inventory.py --check` | `b6a1c189` | NOT RUN: refuses on this host for want of the pinned Bash parser |

## Known limitations / out of scope

- The bench items of #70 stay with the release run of #76: started and stopped across a cycle, a power cut during a commit, the blank-board walk, non-default maps on silicon (#637) and the soak.
- The volatile set is proved on the desk. A board reading after a cold cycle is still owed, and FASTCONNECT 16 says so.
- The milan_dp README's mutant rows 1 to 63 keep their 2026-10-20 totals (686 checks). `[VOLATILE]` added 25 after them, and the README says so.
- `ci/image/command-table.json` already had 32 stale declarations at dev `1e80128f`, `tb/verilator/milan_dp/dynmap_mutants.py` among them. This PR re-pins only the declared scripts it changed that were in sync at dev.

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
