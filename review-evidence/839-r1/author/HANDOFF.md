# A731 HANDOFF: issue #839, the first MSRP PDU after boot carries source address zero

PRIVATE. Nothing pushed (the manager pushes and opens the PR from `PR-BODY.md`). Receipts are under `receipts/`, indexed in `receipts/INDEX.md` (generated from the files present).

## Status

Resumed 2026-11-05 after the 2026-11-04 22:19 host reset. The cut session had left one uncommitted edit (`sim_gptp.cpp`, the station-MAC write the gptp legs lacked). It was verified (gptp and gptp-lat legs 210 of 210 checks each, `receipts/diagnostic/fix-gptp/`) and committed as `b04c4307`. The 2026-11-04 sweep at `e893e640` was cut by the reset; its milan_dp log is kept as a diagnostic only (`receipts/diagnostic/sweep-e893e640/`).

This session then made two more commits. `8d2dfb65` corrects four clause citations in the leg's comments, checked against the texts. `992c3d7b` fixes a regression the sweep at `8d2dfb65` found: the render leg's mid-test resets returned the pair to unwritten and the harness never wrote it again, so its rebind's PROBE_TX stayed held (`T1 BIND: listener 0 launched a PROBE_TX at the named talker got=0 exp=1`, 8 of 260 checks; `receipts/diagnostic/sweep-8d2dfb65/`). Every gate below is at `992c3d7b`.

| Item | State |
|---|---|
| Base | `604899c08ff1cd1830e1dd08b733109ef852400c` (dev; the live `dev` tip on 2026-11-05) |
| Head | `992c3d7bb37f4ade0b151c17d718baed0e119753` |
| TAKEN on #839 | posted, issuecomment-6641107923 (text: `taken.md`) |
| REVIEW READY on #839 | posted 2026-11-05, issuecomment-6654836727 (text: `review-ready.md`), naming head `992c3d7b` |
| Branch `839-boot-source-address` | from `dev` `604899c0` (verified: merge base `604899c08ff1cd1830e1dd08b733109ef852400c`), not pushed |
| Remote | `origin` = `https://github.com/kebag-logic/milan-fpga.git` (verified) |
| Submodules | none edited; each initialised one sits at its pin, its `rev-parse --show-toplevel` is its own directory and its `origin` is its `.gitmodules` URL (checked 2026-11-05): `third_party/verilog-axis` `48ff7a7e`, `protocol-processor` `a9e84b66`, `gptp-processor` `135afd04`, `third_party/lwSRP` `08ee86e8`, `third_party/tsn-c-stack` `70936b77`. `external` (the private dependency) is not initialised and no gate builds it |
| Project card | #839 is in `Backlog`; not moved (not among the assignment's allowed actions) |
| `scripts/docs_inventory.py` | not in the tree at `604899c0`, at the head or at the live `dev` tip (`604899c0` on 2026-11-05): NOT RUN, it cannot be |
| CPU booking | The final sweep's four shards ran on `16-19`, `20-23`, `24-27`, `28-31`: `cpu_ranges.py pick` returned `16-31` at 08:42 and `show` listed it busy once the shard units held it. The diagnostic sweeps at `b04c4307` and `8d2dfb65` ran inside this unit's own range (80-95) while `show` listed no free CPU. MemAvailable 59 GB at the final launch, so in parallel. `capture_coherence` is in shard 2, on 4 CPUs |

## Design, and why

The fix holds the transmitters (acceptance 1's first option) and adds a source-address stamp. Nothing in the firmware boot order changes.

- **Cause, confirmed in simulation.** On the base RTL the new leg sends one MSRP PDU with source `00:00:00:00:00:00` at cycle 20198 (the 200 ms join tick, Milan v1.2 Table 4.3), before `configure_fabric()` writes the MAC at cycle 40088. The processor's `KL_srp_encoder` writes octets 6 to 11 into its TX slot when it builds the frame (`protocol-processor/hdl/srp/KL_srp_encoder.sv:458`), so a hold alone would release that frame with the stale address later.
- **Clauses.** IEEE 802.1AC-2016 11.1: "The source_address parameter is the individual address of the source MSAP." IEEE 802.1Q-2022 6.8.1: the EISS source_address is "as defined for the ISS". IEEE 802.3-2022 2.3.1.2: "If the source_address parameter is omitted, the local MAC sublayer entity will insert a value associated with that entity" (the basis for stamping at the lane). Milan v1.2 4.2.7: MRP/MSRP/MVRP operation runs over that service.
- **Why not firmware order.** The engines leave reset at FPGA configuration and the SRP engine's first PDU is due 200 ms later; the firmware's first CSR write happens after the BIOS. No reordering inside `milan_init()` can come first. A reset-value change of `MAC_ADDR` would be a register-map change beyond sequencing, which acceptance 3 rules out.
- **Why at the sources and not at the MAC boundary.** A boundary hold refuses a beat each arbiter has presented, and `adp_tx_arbiter`'s watchdog then reports a stall (`hdl/ieee17221/adp/adp_tx_arbiter.sv:173-188`) into the sticky `A_TXARB_DIAG` bits on every boot. Masking `tvalid` at each source means no arbiter sees a frame until the gate opens.
- **Why gPTP is not held.** Its source address is not the CSR's: the builder generates the gPTP program with `--mac` = `platform.mac_address` (`sw/builder/endstation_builder.py:5933-5937`), the same value the firmware writes (`sw/builder/endstation_builder.py:2677`), and `_mac48` refuses a zero or group MAC (`sw/builder/endstation_builder.py:3303-3305`). Builder gate 1b also pins the gPTP TX path free of runtime gates (`sw/builder/test_builder.py:11616-11720`, "independent of AEM, ADP and protocol-processor gates").
- **Why the sequencing is in the datapath, not in `milan_csr`.** A new `milan_csr` port breaks the csr suite's lockstep legs, which refuse a port list different from the frozen `e8454e27` block (`tb/verilator/csr/gen_lockstep.py:23-24,171-172`). The datapath observes the CSR slave's own write handshake instead: `milan_csr` drives `s_axi_awready = wr_fire` and commits on that edge (`hdl/common/csr/milan_csr.sv:1117-1121,1144`), so `s_axi_awvalid & s_axi_awready` with the pair's address is exactly that register's write enable. `milan_csr` is byte-identical to the base.
- **No value check.** The gate opens once both halves are written, whatever the value. A zero or group address is refused at its only producer (the builder). Requiring a non-zero value would have stopped every harness that runs with the all-zero station address (sim_nxn addresses its commands to DA 0).

## Changes (file:line at head `992c3d7b`, clause)

Base `604899c08ff1cd1830e1dd08b733109ef852400c` (dev), head `992c3d7bb37f4ade0b151c17d718baed0e119753`, ten commits, 17 files. No submodule, no `milan_csr` file and no top-level port changes: the module's 140 port declarations hash the same at base and head, and `git diff --quiet 604899c0 HEAD -- hdl/common/csr/` is clean.

| Change | Where | Clause / reason |
|---|---|---|
| The station-MAC pair's own sequencing: each half's first write since reset, read off the CSR slave's write handshake (`s_axi_awvalid && s_axi_awready` with address `0x108` or `0x10C`); `tx_sa_ok_w` is 1 once both have been written, in either order, until reset | `hdl/milan/milan_datapath.sv:3092-3115` (`mac_addr_seq`) | IEEE 802.1AC-2016 11.1 (source_address is the individual address of the source MSAP). `milan_csr` sets `s_axi_awready = wr_fire` and commits on that edge, ignores WSTRB, and decodes the same 16-bit address (`hdl/common/csr/milan_csr.sv:1117-1121`, `:1671-1683`, `:212`) |
| The transmit gate: the processor's control lane, MAAP, the AAF talkers and the CRF talker see `tready` 0 and their arbiters see `tvalid` 0 until `tx_sa_ok_w` | `hdl/milan/milan_datapath.sv:787-800` (nets), `:8807-8822` (gate); the source ports re-pointed at `:1616-1617` (AAF), `:7625-7626` (CRF), `:8599-8600` and `:8608` (MAAP), `:9716-9718` (processor) | Acceptance 1, first option: the fix holds each transmitter. The gate sits at each source, not at the MAC boundary, so no `adp_tx_arbiter` sees a refused beat and `A_TXARB_DIAG` stays quiet. It only rises, so it never cuts a frame |
| The control-lane source-address stamp: octets 6 to 11 of every frame after the control lane's IFG gasket are taken from `cfg_mac_addr` | `hdl/milan/milan_datapath.sv:8888-8941` (`ctl_sa_position`, `ctl_sa_stamp`) | IEEE 802.3-2022 2.3.1.2 (the MAC sublayer entity inserts its own address). Needed because the processor's `KL_srp_encoder` writes octets 6 to 11 into its TX slot when it builds the frame (`protocol-processor/hdl/srp/KL_srp_encoder.sv:458`), so the hold alone would release the boot's first MSRP PDU with the reset address |
| The gPTP plane is not held | `hdl/milan/milan_datapath.sv:8807-8814` (comment) | Its source address is the builder's `platform.mac_address` in its program ROM (`sw/builder/endstation_builder.py:5933-5937`), the value firmware writes (`:2677`), refused when zero or group (`:3303-3305`) |
| The `bootsa` leg: the shipping 1x1 datapath booted through `milan_init()`'s own stage order, with the firmware's own `configure_fabric()` and `entity_advertise()` compiled in, grading every frame at `m_axis_mac_tx` up to and past the first ENTITY_AVAILABLE, then two more boots writing one half alone | `tb/verilator/milan_dp/sim_boot_sa.cpp` (new), `gen_boot_fw.py` (new), `bootsa_probes.vlt` (new); `Makefile:495-525` (recipe), `:717` (`ORDINARY_CASES`), `:740` (`CASE_OPTIONS_bootsa`), `:904-907` | Acceptance 2 |
| Seven planted controls for the leg | `tb/verilator/milan_dp/bootsa_mutants.py` (new), `make -C tb/verilator/milan_dp bootsa-mutants` | Acceptance 2 (the old order, by name) |
| Harnesses that never wrote the station MAC now write it after reset, as `configure_fabric()` does, keeping the all-zero address their stream IDs root in | `tb/verilator/capture_coherence/sim_dp.cpp:291-292`, `tb/verilator/milan_dp/sim_nxn.cpp:3023`, `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:1640` and, after its four mid-test resets, `:2868-2873`, `tb/verilator/milan_dp/sim_gptp.cpp:849-850` | A reset returns the pair to unwritten as it returns the CSR to zero; the product resets the datapath only with the system, and firmware's `configure_fabric()` then writes the pair again. Without the write the gate holds their AECP answers and media frames the gate holds their AECP answers and media frames (the 2026-11-04 sweep at `e893e640`: the gptp legs failed 87 of 210 checks, `GET_AVB_INFO response length got 0`) |
| Docs: `MAC_ADDR_LO/HI` rows carry the sequencing; firmware boot contract; the campaign row; the leg's inventory and section; CHANGELOG | `docs/reference/REGISTER_MAP.md:414-415`, `docs/integration/BAREMETAL_FIRMWARE.md:112-116`, `:217`, `docs/testing/TESTING.md:277`, `:406-421`, `tb/verilator/milan_dp/README.md:91`, `:110`, `:1114-`, `CHANGELOG.md:11`, `:55-73` | Acceptance 3 (documented sequencing; no field, address or reset value changes) |
| Ratchets: the new campaign named among the test-evidence readers; the sim-pool test's leg list | `scripts/measure_test_evidence_readers.py:171`, `tb/verilator/milan_dp/test_sim_pool.py:104` | The C++, Python and test-evidence ratchets the docs workflow runs |

## New checks, planted mutants and their failing words

The leg (`obj_bootsa`, run by the milan_dp suite's `run`) prints one line per check. Those that grade acceptance 1 and 2:

- `[BOOTSA] the processor offered a frame before the station MAC was written` (the boot reached the defect: `KL_pp_shadow.txp_valid_r` rose in the BIOS window)
- `[BOOTSA] no frame carries the all-zero source address`
- `[BOOTSA] no CSR-addressed transmitter starts a frame before the station MAC is written`
- `[BOOTSA] every <MSRP|MVRP|gPTP|ADP|AECP|ACMP|MAAP|AAF|CRF|other> frame's source address is the station MAC`
- `[BOOTSA] every <kind> frame's destination address is its protocol's (octets 0 to 5 untouched)`, and `every frame is a known protocol's (octets 12 and 13 untouched)`
- `[BOOTSA] <MSRP|gPTP|ADP|AECP|ACMP|MAAP|AAF> frames were sent and graded`
- `[BOOTSA] the first ENTITY_AVAILABLE leaves after entity_advertise()` and `the entity re-advertises past the first ENTITY_AVAILABLE`
- `[BOOTSA] A_TXARB_DIAG: no arbiter stall or abort since reset`
- `[BOOTSA] pair: MAC_ADDR_LO alone opens no CSR-addressed transmitter`, `... MAC_ADDR_HI alone ...`, `pair: the second half after <half> releases the processor's frame`, `pair: every frame of the <half> boot carries the station MAC`

`bootsa_mutants.py` plants each defect in a copy of `milan_datapath.sv`, rebuilds the same leg through `make bootsa-build`, and counts a catch only when the leg fails by its own verdict and by every named check (a crash or a build failure is not a catch). The clean leg runs first.

| Mutant | Planted | Must fail by |
|---|---|---|
| the defect as shipped: no hold and no stamp (the old order) | `tx_sa_ok_w = 1'b1`, stamp disabled | `no frame carries the all-zero source address`; `no CSR-addressed transmitter starts a frame before the station MAC is written`; `every MSRP frame's source address is the station MAC` |
| no hold: the stamp alone | `tx_sa_ok_w = 1'b1` | the same three |
| no stamp: the hold alone | stamp disabled | `no frame carries the all-zero source address`; `every MSRP frame's source address is the station MAC` |
| MAC_ADDR_LO alone completes the pair | `tx_sa_ok_w = mac_alo_wr_r` | `pair: MAC_ADDR_LO alone opens no CSR-addressed transmitter` |
| MAC_ADDR_HI alone completes the pair | `tx_sa_ok_w = mac_ahi_wr_r` | `pair: MAC_ADDR_HI alone opens no CSR-addressed transmitter` |
| the stamp lands on the destination | octets 0 to 5 instead of 6 to 11 | `every MSRP frame's destination address is its protocol's`; `every MSRP frame's source address is the station MAC` |
| the stamp's beat position survives a frame's last beat | `ctl_sa_idx_r <= 1` on `tlast` | `every ADP frame's destination address is its protocol's` |

Result at the head: see Gates (`bootsa_mutants`).

## Acceptance, item by item

| # | Item | State | Evidence |
|---|---|---|---|
| 1 | From reset no frame leaves with source 00:00:00:00:00:00 and none with another address than the station MAC, for SRP, ADP, ACMP, AECP, MAAP, gPTP and the streams; the fix states whether it holds or reorders | Met: the fix holds each CSR-addressed transmitter (and stamps the control lane); gPTP's address is the same station MAC from its ROM | the `bootsa` leg in the final sweep: 831 frames (MSRP 36, gPTP 1, ADP 5, AECP 1, ACMP 1, MAAP 5, AAF 1, CRF 781), `no frame carries the all-zero source address got=0`, `every <kind> frame's source address is the station MAC got=0` for every kind; the first frame is MSRP at cycle 40112, after `configure_fabric()` completes the MAC at 40088. Stated in `REGISTER_MAP.md`, `BAREMETAL_FIRMWARE.md`, `CHANGELOG.md` |
| 2 | A datapath simulation from reset, through the firmware's real boot order, asserts 1 for every frame up to and past the first ENTITY_AVAILABLE; a mutant restoring the old order fails it by name | Met | the leg compiles the firmware's own `configure_fabric()` and `entity_advertise()` and runs `milan_init()`'s stage order read from the firmware; first ENTITY_AVAILABLE at cycle 196252, re-advertised after; `bootsa-mutants` `8 checks: 8 PASS`, the first control being the defect as shipped (no hold, no stamp), failing `no frame carries the all-zero source address`, `no CSR-addressed transmitter starts a frame before the station MAC is written` and `every MSRP frame's source address is the station MAC`. On the base RTL the same leg fails 9 of 40 (`receipts/base-repro/`) |
| 3 | No new top-level port; a register-map change is the CSR's own sequencing only, documented through the register-map generator | No new port (140 port declarations, same hash at base and head); `milan_csr`, its addresses, fields and reset values unchanged; the sequencing is documented on the `MAC_ADDR_LO/HI` rows. **Reading for a maintainer:** there is no register-map generator in the tree. `REGISTER_MAP.md` is hand-maintained (`gen_toc.py` keeps only its contents list), and the builder generates only the `0x680` group's reset words, which test_builder cross-checks against REGISTER_MAP's Reset column. Nothing generated changes | `git diff --quiet 604899c0 HEAD -- hdl/common/csr/`; `docs/reference/REGISTER_MAP.md:414-415` |
| 4 | Every parent gate the boot order touches is green: the firmware self-test, the builder, behave and the boot runs | Green, with one reading for a maintainer: the firmware self-test (four shards, NVM, coverage), the builder (`docs.yml` and `elaborate.yml` legs), behave, and the simulated boot runs (the `bootsa` boot through the firmware's own `configure_fabric()` and `entity_advertise()`, and the LiteX SoC simulations). **Not run:** a boot on hardware with a capture of its first frames, the kind the defect was found in; this lane has no bench access | Gates below |

`Closes #839` is therefore withheld in `PR-BODY.md` (`Relates to #839`): items 3 and 4 each carry a reading only a maintainer can accept.

## Gates

Every gate at head `992c3d7bb37f4ade0b151c17d718baed0e119753`, on clean clones of the committed head (the four sweep shard clones; one `clone_at.sh` clone for the lane gates; one fresh clone per `docs.yml` job), never piped, one log and one rc each. Receipts under `receipts/gates/`; logs over 200 KB are in each directory's `LARGE-LOGS.txt` by size and sha256, with a tail beside them.

| Gate | Command (as run) | rc | What the log shows | Receipt |
|---|---|---:|---|---|
| Full Verilator sweep, 4 native shards | `native-shards.py 839-a731 sweep4-spec.json <out> 4 16-19 20-23 24-27 28-31`; each shard runs `scripts/run_all_suites.sh <logs> --wait --shard k/4` with `MAKEFLAGS=-j4 --no-print-directory` | 0, 0, 0, 0 | shard 0: 15 of 15 suites, 361,161 checks; shard 1: 17 of 17, 1,525,511; shard 2: 17 of 17, 284,228 (`capture_coherence` here, on 4 CPUs); shard 3: 16 of 16, 21,575. 65 of 65 suites, 0 failed, 0 timed out, 0 in-suite failures. The preflight (its suite-cancellation self-test among it) passed first time in every shard, and the `gptp_shadow` suite passed in shard 1, so no #833 re-run was needed. `milan_dp` carries the `bootsa` leg (`== bootsa: checks: 40 failures: 0 ==`) and the gptp legs (210 of 210 each); `milan_dp_render` `tdm8_render: checks: 263 failures: 0` | `gates/sweep/shard-*/` (`01.log`, `complete.json`, `results.json`, suite logs) |
| Firmware self-test | `tally_selftest.py`; `fw_rv32_selftest.py --require-rv32`; `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard k/4` for k = 0..3; `test_ctrl_nvm.py --require-rv32 --jobs 4` | all 0 | tally self-test ok; `RV32 build self-test: 17 checks PASS`; four shards `test_ctrl_firmware: PASS` (shard 0: 18 planted defects caught; shard 1: `mutants: 523 of 523 caught`); `saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests` | `gates/lane/fw_*` |
| Firmware coverage | `fw_coverage.py --selftest`; `fw_coverage.py --check --jobs 8` | 0, 0 | `firmware coverage: PASS (30 files)` | `gates/lane/fw_coverage_*` |
| Builder | `test_builder.py --require-rv32` in `docs.yml`'s two legs (`docs-gates-1` `gate_25_0`, `docs-gates-2` `gate_25_1`); and `elaborate.yml`'s two legs with the LiteX interpreter, `ci_builder_legs.py run k -- test_builder.py --require-elaboration --require-rv32` | 0, 0; 0, 0 | `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN` (the latter without LiteX, so its elaboration arms are the LiteX legs'); the LiteX legs `ALL GATES PASS EXCEPT 1 NOT RUN` each, for reasons they record: leg 0, the `MAKEFLAGS += -e` mutation has nothing to act on with this host's make; leg 1, gate 11's calibration needs a build tree not on this host | `gates/docsyml/docs-gates-1__gate_25_0.log`, `docs-gates-2__gate_25_1.log`; `gates/lane/builder_leg*_elab.*` |
| behave | `cd tests && behave --no-capture -f plain` | 0 | `14 features passed, 0 failed, 0 skipped`, `508 scenarios passed`, `2330 steps passed` | `gates/lane/behave.*` |
| Every `run:` step of `docs.yml` | `run_docs_yml.py <head> <job> <root>` for each of its nine jobs, then `verify_docs_yml.py` | verify 0 | `64 steps ran, 31 not run with a reason, 0 bad`; every job `failed 0`, every clone clean after its job. The 31 are hosted-only steps (records, uploads, cancels, apt and sudo installs), each with its reason in `tools/not_run.json` | `gates/docsyml/docs-yml-table.md` |
| `scripts/docs_inventory.py --check` | not run | n/a | the script is not in the tree at the base, the head or the live `dev` tip | n/a |
| `git diff --check` against the merge base | `git diff --check 604899c08ff1cd1830e1dd08b733109ef852400c HEAD` | 0 | no output | `gates/lane/diffcheck.*` |
| RTL lint | `lint_rtl.py --check --self-test --jobs 8` | 0 | `LINT GATE: PASS (89 violation(s) <= ratchet 89; 19 waived, 0 justified lint_off)` | `gates/lane/lint_rtl.*` |
| Processor source list | `pp_srcs.py --check --selftest` | 0 | `46 tracked source(s) derived; ... (self-test passed)` | `gates/lane/pp_srcs.*` |
| Yosys portability | `syn/yosys/run.sh` | 0 | `RESULT: PASS`, `TIED-INPUT GATE: PASS`, `TAP-PURITY RESULT: PASS` | `gates/lane/yosys.*` |
| The leg's planted controls | `make -C tb/verilator/milan_dp bootsa-mutants` | 0 | `8 checks: 8 PASS, 0 FAIL`: the clean leg passes and all seven controls are caught by every check they name | `gates/lane/bootsa_mutants.*` |
| LiteX SoC simulations (the simulated boot runs) | `run_litex_sims.sh --selftest`; `ci_litex_legs.py run k -- run_litex_sims.sh <logs>` for k = 0..2 | 0; 0, 0, 0 | `16 checks: 16 PASS`; all eight inventory members PASS, `test_pp_boot_bus_freeze` among them | `gates/lane/litex_*`, `litex-verdicts-leg*.tsv` |

Not a gate, the defect shown by the same leg: `base_repro.sh` builds the head's `bootsa` leg against the base `milan_datapath.sv` (sha256 `30d8ae96...`, `604899c0`'s). Build rc 0; the run fails as it must, 9 of 40 checks, first `#0 MSRP cycle 20198 source 000000000000 (before the MAC write)` (`receipts/base-repro/`).

Run notes, all public in the receipts:

- The heavy group's first attempt at the five LiteX legs was refused before running anything: `source dependency origin differs: third_party/tsn-c-stack` (`scripts/ci_case_receipts.py:83-84`). The lane clone took its submodules from the lane's own copies, so their `origin` was a local path. Each submodule's `origin` was set to its `.gitmodules` URL (objects unchanged) and the five legs re-ran green. The refused logs are in `receipts/diagnostic/refused-origin/`; `clone_at.sh` now sets the origins itself.
- The sweep at `8d2dfb65` found the render regression `992c3d7b` fixes; its logs are in `receipts/diagnostic/sweep-8d2dfb65/`. The local render run that confirmed the fix ran in the lane worktree (`receipts/diagnostic/render-fix-lane-worktree/`, rc 0). The final evidence is the sweep at `992c3d7b`.
- `docs.yml` at `8d2dfb65` (superseded) is in `receipts/diagnostic/docsyml-8d2dfb65/`.
- No hardware boot was run: this lane has no bench access.

## Area

Measured, out-of-context synthesis of `milan_datapath` (`syn/ooc/milan_datapath_ooc.tcl`, its default 1x1 `arty_current` shape, Vivado through `vivado-slot.sh`, a fresh clean clone at each commit). The head run is at `8d2dfb65`; `git diff 8d2dfb65 992c3d7b` touches only `tb/verilator/milan_dp_render/sim_tdm8_render.cpp`, so nothing the synthesis reads differs from the final head.

| Figure | base `604899c0` | head | Delta |
|---|---:|---:|---:|
| Slice LUTs | 45,176 | 45,275 | +99 |
| Slice registers | 40,222 | 40,233 | +11 |
| F7 / F8 muxes | 805 / 104 | 920 / 109 | +115 / +5 |
| Block RAM tiles | 27.5 | 27.5 | 0 |
| DSPs | 13 | 13 | 0 |
| WNS at 10 ns, OOC | -4.914 ns | -4.914 ns | 0 |

Not the routed shipping image: the daily area flow builds that, and its preflight opens the bench console, which this lane may not touch. The base's own OOC WNS is unchanged. Receipts: `receipts/area/AREA.md` and the reports beside it.

## Findings outside scope (for new Issues; not filed)

- `tb/verilator/milan_dp/test_sim_pool.py`'s `LEGACY_LEGS` lacks `obj_sidmove` and `obj_sidmove8` at `604899c0`, so its `arm_the_makefile_hands_the_runner_the_recipes_ordinary_legs` fails on the base too. No gate runs that file. This lane added `obj_bootsa` to the list and did not add the two missing legs.
- Prose counts in `tb/verilator/milan_dp/README.md` ("fifteen elaborations", "The eleven ordinary simulations") were already stale at the base; not changed.
