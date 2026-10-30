# HANDOFF - [A704], issue #70 fix lane (boot report + PHY link + volatile-set desk check)

Status: REVIEW READY at `b6a1c189fa83de85b470c77a2c7c1e5996138909` (local; nothing pushed). REVIEW READY posted: 6520937367.
Branch `70-boot-report-link` from dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
Assignment: the latest [A10] comment on issue #70 (6515314113, 2026-10-30T04:55:29Z). TAKEN: 6515697413.
STOP conditions: neither met. No second write site for either enable bit and no change to the verdict data flow; the 8x8 capture maximum is 13.86052 ms against 24.5 ms.

## Lane checks
- origin `https://github.com/kebag-logic/milan-fpga.git`; HEAD at start == origin/dev == `1e80128f0a`.
- protocol-processor: `git -C protocol-processor rev-parse --show-toplevel` is the submodule directory; its origin is the processor repository; pin `f65c8ff7`; read only, never edited (every processor mutant plants into a copy under a temporary directory; `git -C protocol-processor status --porcelain` empty after each run).
- No RTL file changed (`git diff 1e80128f HEAD -- hdl` is empty): no sweep, no Vivado.

## Commits (local, nothing pushed; one-line subjects, no body, no trailers)
| Commit | Subject |
|---|---|
| `dc7b1417` | Report the entity enable as a request the restore releases, publish the PHY link on the persistence-disabled path, and grade both on every boot path (#70) |
| `c1972509` | Prove in milan_dp that the lock, the controller registry and IDENTIFY do not survive a planted power cycle, with a processor-copy mutant per item (#70) |
| `ac0da94e` | Re-pin test_nvm_firmware.py and test_boot_walk.py in the CI command table at their new contents (#70) |
| `6260c53c` | Split the deployment guide's enable-request sentences to the page's one-short-sentence style (#70) |
| `38fd88f3` | Boot the volatile-set check over a saved entity name, so the restore it grades applies a record and the cut is proved inside the debounce (#70) |
| `1767346a` | Keep test_nvm_firmware.py within the module-length ratchet by passing harness defines through, and cite processor test paths with their submodule prefix (#70) |
| `c71364bd` | Keep the admitted writer's heartbeat as dev has it and poll the PHY in the no-writer branch alone, so the shipping path reads the time once per tick (#70) |
| `af61a041` | Grade the service budget's boot on the enable-request line, and regenerate its oracle through gen_oracle.py from fresh runs of the new firmware (#70) |
| `14e956f0` | Re-measure the product-CPU capture at the #70 firmware digest: 8x8 contract maximum 13.86052 ms against the 24.5 ms limit (#70) |
| `b6a1c189` | Refresh SAVED_STATE_SNAPSHOT_OWNERSHIP section 18 and section 20 item 6 from the re-measured capture receipt (#70) |

## Changes, with clause

### 1. The enable report (D3 `SAVED_STATE_MATERIALIZATION.md` section 5.3, change 3)
- `sw/firmware/milan_baremetal/milan_baremetal.c:1552` (`nvm_restore_walk`): at the bounded wait's timeout the line says the restore has not reached its terminal and that the fabric holds the entity enable. The wait still decides nothing. Comment `:1539-1542`.
- `sw/firmware/milan_baremetal/milan_baremetal.c:1857` (`entity_advertise`): the line reports that the enable was REQUESTED and that the fabric holds it until the restore releases it. Comment `:1845-1849`.
- Unchanged, verified: the only writes that set PP_CTRL[0] / ADP_CTRL[0] are `:1855-1856` inside `entity_advertise()`. The diff touches no PP_CTRL/ADP_CTRL write and nothing on the `load_aem_image()` -> `aem_loaded` -> `entity_advertise(aem_loaded)` verdict path. The builder's gate 1b (one entrance; the verdict traced to the verifier; the enable census) passes at `c71364bd`.
- Docs: `docs/integration/BAREMETAL_FIRMWARE.md` (the boot paragraph after the order block), `docs/guides/BOARD_DEPLOYMENT.md:218-229`.

### 2. The PHY link on the persistence-disabled path
- `:954` `static int phy_live;`, set at `:1671`, the top of `nvm_boot()` (reached only after the CSR identity check and `configure_fabric()`).
- `:1095-1107` `nvm_heartbeat_tick()`: the writer's gate `if (!nvm_started)` now opens a block that polls the PHY when `phy_live` and returns. An admitted writer's path is textually dev's (`now = gettime_ns(); phy_link_tick(now); ...`), so the shipping heartbeat is unchanged. `test_disabled_writer.py`'s admission plant moves with the gate's text (`if (!nvm_started) {` -> `if (0) {`) and is still caught in both rejected states.
- `:1676` the persistence-disabled path installs the console idle hook (`set_idle_hook(nvm_service)`) before its blind walk; the writer behind it is never admitted (`nvm_started` 0). The shipping path's hook (`:1812`) is unchanged.
- After a CSR identity mismatch `phy_live` stays 0 and nothing touches the MDIO pins, as before; now checked.
- History, corrected: the first form (`dc7b1417`) polled the PHY ahead of the gate with a second `gettime_ns()` per tick. I read the service-budget rows against `oracle.json` as a +36 ms boot cost of that and restructured (`c71364bd`). That reading was wrong: `oracle.json` was recorded from an older firmware, and both forms measure the same 330.04 ms. Against a real dev baseline the change is within noise (Resources / timing). The restructure is kept on its own merit (the shipping heartbeat stays textually dev's). The capture and service runs were restarted on `c71364bd` because the digest changed (`receipts/superseded/`).
- Docs: `docs/integration/BAREMETAL_FIRMWARE.md` PHY section (five lines after "Discovery probes one PHY address per service opportunity").

### 3. The volatile set desk check (FASTCONNECT section 16, D3 section 9)
Milan v1.2 5.3.4.1 (the locked state is cleared by a power cycle), 5.3.4.2 (the registered-controller list is cleared by a power cycle), 5.3.12 (IDENTIFY 0 after reset); IEEE 1722.1-2021 7.4.2 (LOCK_ENTITY), 7.4.25/7.4.26 (SET/GET_CONTROL), 7.4.37 (REGISTER_UNSOLICITED_NOTIFICATION).
- `tb/verilator/milan_dp/sim_nxn.cpp:5879` `volatile_set_across_a_power_cycle_section()`, called at `:3347` at the end of the dynmap leg. Boots over a window holding a saved entity name (`0x80`, framed by the repository's codec) and proves each premise first: the restore applied the saved name; A's registration (B's change notifies A); IDENTIFY 255 read back; A's lock (B refused ENTITY_LOCKED, `AECP_STAT0[16]` 1); the cut inside the processor's debounce (the window still holds the saved set). After the planted power cycle (datapath reset, window kept, the firmware's load, the restore walk), it checks: PP_STAT done 1, busy 0, fail 0, blank 0; the saved name is back and B's unsaved one is lost; GET_CONTROL reads IDENTIFY 0; `AECP_STAT0[16]` reads 0; B's SET_NAME is SUCCESS; and that accepted change notifies no controller.
- `tb/verilator/milan_dp/dynmap_mutants.py:440-451` three arms, `:532` `plant_pp()` (a copy of the processor's `hdl/` tree, built with `PP_DIR`). Each deletes one item's reset term, the plant the processor's own `d3_mutants.py` VOLATILE arms make: nothing the parent owns can carry the three (D3 section 9).
- `:1647` (adding IDENTIFY to persistence fails D3's exclusion control) already exists: `protocol-processor/tb/pp_top/d3_mutants.py` arm `identify_is_a_change`, caught by D3S7. Cited, and re-run here.
- Docs: FASTCONNECT 16 rows `:1637` and `:1647` ticked with their evidence (the board reading after a cold cycle is still owed); D3 section 9 table and paragraph; `tb/verilator/milan_dp/README.md` (`obj_dynmap` row, `[VOLATILE]` paragraph, rows 64-66 and a note on rows 1-63); `docs/testing/TESTING.md` campaign row; the Makefile comment.

## UART enable-line consumers (old -> new exact strings)
Old enable line (dev `1e80128f`):
`Milan baremetal: fabric entity enabled; UART diagnostics ready.`
New enable line:
`Milan baremetal: fabric entity enable requested; the fabric holds it until the restore releases it; UART diagnostics ready.`
Old timeout line:
`Milan NVM: the restore walk did not sequence in time.`
New timeout line:
`Milan NVM: the restore walk has not reached its terminal; the fabric holds the entity enable until it does.`

In-tree readers (submodules searched too), all handled in this change:
| Reader | Reads | Action |
|---|---|---|
| `tb/verilator/fw_service_budget/run.py:281` (grader) | enable line | requires the new line (`ENABLE_REQUEST`, `:37`) |
| `tb/verilator/fw_service_budget/oracle.json` raw logs | enable line, old firmware | regenerated through `gen_oracle.py` from fresh runs at `c71364bd` (1x1 `all`, 1x1 `uart-paced`, 8x8 `all`); a second generation is byte-identical; every log carries the new line and none the old claim; budget findings unchanged (8x8's two pre-existing `milan_nvm`) |
| `sw/firmware/nvm_hosttest/test_boot_walk.py:27` `TIMEOUT_LINE` | timeout line | new line; `REQUEST_LINE` `:30` added |
| `docs/guides/BOARD_DEPLOYMENT.md:218` | enable line | new line and its explanation |
| `scripts/baremetal_uart_smoke.py` | `milan_status` CSR fields only | no boot-line match: unchanged (`--self-test` rc 0) |
| BDD steps (`tests/`) | none | none |
| `docs/findings/117_GPTP_SILICON_EVIDENCE.md:840`, `:887` | the old line as dated silicon evidence | historical record: unchanged |
| `sw/builder/test_builder.py:15466`, `:15523` | a synthetic `#define` banner in mutant fixtures | not a reader: unchanged |
| submodules (external, protocol-processor, gptp-processor, lwSRP, tsn-c-stack, verilog-axis) | none | none |

Outside this repository: any bench script or grader that waits for `fabric entity enabled` or `did not sequence in time` must move to the new strings.

## New checks, planted mutants, failing words

### Host: `sw/firmware/nvm_hosttest/test_boot_walk.py` (in `test_nvm_firmware.py`; mutants in `--self-test`)
Every boot path must report exactly one request line and no "entity enabled". The two new stalled paths (`--walk-stall`, `nvm_host.c:148`, `:471`: a walk that never reaches a terminal) must print the new timeout line; no other path may.
| Mutant | Plant | Failing words |
|---|---|---|
| `enable_line_claims_enabled` | the enable printf as at dev | `boot walk, cold boot, CLOSED restore: the console claims the entity enabled ('entity enabled') with done=0 closed=1` |
| `timeout_line_holds_unsaid` | the timeout printf as at dev | `boot walk, cold boot, stalled restore: the timeout did not report that the restore has not reached its terminal and the fabric holds the enable` |
| `shape_path_skips_walk` (existing, now named) | | `boot walk, persistence disabled: walks=0, expected 1` |
| `wait_on_done_only` (existing, now named) | | `boot walk, cold boot, CLOSED restore: the restore wait ran out its timeout` |

### Host: `sw/firmware/nvm_hosttest/test_phy_firmware.py` boot-path arms
These run in a PHY build of `nvm_host.c` (`-DNVM_HOST_PHY`) against the pin-level Clause-22 peer, now shared as `phy_peer.h`. The shipping and persistence-disabled paths must publish the peer's 1000BASE-T full duplex (13), at least one publication per 250 ms over 1000 ms of console idle. The identity-mismatch path must make no MDIO transfer.
| Mutant | Plant | Failing words |
|---|---|---|
| `phy_behind_the_writer` | the heartbeat exactly as at dev | `PHY boot path persistence disabled: the link-status CSR holds 0, not the peer's 1000BASE-T full duplex (13)` |
| `disabled_path_no_idle_hook` | no idle hook on the disabled path | `PHY boot path persistence disabled: 0 publication(s) in 1000 ms of console idle, fewer than one per 250 ms` |
| `phy_never_armed` | `phy_live = 1;` removed | `PHY boot path persistence disabled: the link-status CSR holds 0, not the peer's 1000BASE-T full duplex (13)` |
| `phy_off_the_writer_path` | `phy_link_tick(now);` removed from the admitted writer's path | `PHY boot path shipping: the link-status CSR holds 0, not the peer's 1000BASE-T full duplex (13)` |
| `phy_unguarded` | the `phy_live` guard removed | `PHY boot path identity mismatch: 1 MDIO transfer(s) and 1 publication(s) on a fabric that failed its identity check` |
Dev control (`receipts/dev-firmware-controls.log`): dev `1e80128f`'s own firmware fails all three named host checks (the disabled path: 0 MDIO transfers, 0 publications).

### milan_dp: `[VOLATILE]` (dynmap leg 711 checks, 0 failures, 25 new; maprec8 219/0 and maprec4 137/0 unchanged)
| Mutant (`dynmap_mutants.py` place) | Plant (processor copy) | Failing words | Failures |
|---|---|---|---|
| 64 the lock survives the power cycle | `lk_held_r <= 1'b0;` deleted from `KL_aecp_notify`'s reset branch | `[VOLATILE] the lock is clear after the restore: SET_NAME from B is SUCCESS` | 3 of 711 |
| 65 the registered-controller list survives the power cycle | `valid_r <= '0;` deleted from the same branch | `[VOLATILE] the registry is empty after the restore: B's accepted change notifies no controller` | 1 of 711 |
| 66 the IDENTIFY value survives the power cycle | the `ident_r` reset deleted from `KL_aecp_dyn_state` | `[VOLATILE] IDENTIFY reads 0 after the restore` | 1 of 711 |

### Processor controls (pin `f65c8ff7`, read only)
- `identify_is_a_change` (IDENTIFY made a persisted change: the writer's trigger and the store's field mask take selector 7): KILLED by D3S7, golden PASS.
- `registry_survives_reset`, `lock_survives_reset`, `identify_survives_reset`: 3 of 3 KILLED, goldens PASS.

## Resources / timing
- RTL unchanged: no route, no area change, no route timing to report.
- Firmware object (`riscv32-linux-gcc` 14.3.0, Buildroot 2026.05, LiteX's own compile rule, the service-budget 1x1 headers with the MDIO path compiled in), dev `497845e6...` against `c71364bd`'s `60799c75...`: text 17,451 -> 17,697 B (+246), data 104 -> 104, bss 104 -> 108 B (+4, `phy_live`). `receipts/fw-size.txt`.
- Firmware service timing on the product CPU (`tb/verilator/fw_service_budget`, 1x1 `all` plan, populated), dev `1e80128f` against `c71364bd`, same harness (`receipts/service-dev-baseline/compare-1x1-all.txt`):
  - boot to the entity enable: 359.42385 -> 359.41313 ms (-0.011);
  - each `milan_nvm commit`: 290.776 and 290.788 -> 290.864 and 290.865 ms (+0.09);
  - worst heartbeat gap: 265.933 -> 266.018 ms (+0.085);
  - heartbeat period margin: 234.07 -> 233.98 ms;
  - budget findings: none on either side.

## Capture margin (check_nvm_capture.py vs 24.5 ms)
Six arms, 16 captures each, `tb/verilator/nvm_capture_cpu/run.py` by its README (network namespace, offline, `PYTHONHASHSEED=0`, Verilator 5.052 as the receipt records), at `c71364bd`, two drivers of three arms. Receipt `tb/verilator/nvm_capture_cpu/measurements.json` (`14e956f0`), assembled by `scripts/assemble_receipt.py`. That script takes each arm's `measurement.json` verbatim and recomputes the census, harness hashes and maxima through `check_nvm_capture.py`'s own functions, then runs `check_receipt`.
| Shape | CPU MHz | Traffic | min to max, ms | 49 ms floor / max |
|---|---:|---|---:|---:|
| 1x1 | 50 | on | 3.95892 to 3.96490 | 12.3584x |
| 1x1 | 50 | off | 3.90676 to 3.91178 | 12.5263x |
| 8x8 | 50 | on | 13.84558 to 13.86052 | 3.5352x |
| 8x8 | 50 | off | 13.67538 to 13.68956 | 3.5794x |
| 8x8 | 100 (non-contract) | on | 10.41876 to 10.42630 | 4.6997x |
| 8x8 | 100 (non-contract) | off | 10.41406 to 10.41516 | 4.7047x |
- **8x8 contract maximum 13.86052 ms; margin to 24.5 ms is 10.63948 ms (3.5352x the floor).** The previous receipt (#671 round 8) had 13.86328 ms. 39 of 96 captures repeat its cycle counts: the firmware's code layout moved, and `nvm_capture()` is unchanged.
- `python3 scripts/check_nvm_capture.py`: rc 0, `PASS: capture census, clocks, both timing arms and receipt agree` (final battery).
- SNAPSHOT_OWNERSHIP section 18 and section 20 item 6 were refreshed by `scripts/refresh_section18.py`, every edit exact-once, from the receipts alone.

## Gate table
Every command ran in a clean clone at the commit named, never piped; rc is the command's own; receipts under `receipts/` (index `receipts/INDEX.md`). "Carries" says why a result at an earlier commit stands at the head: nothing the gate reads changed after it.

| Gate | Commit | Result | Receipt |
|---|---|---|---|
| docs workflow battery: 100 gates (docs, TOC, anchors, paths, em dash, style, doc map, diagrams, idiom, naming, scope, CI self-tests, `check_nvm_capture.py`, `test_nvm_firmware.py --self-test`, `test_phy_firmware.py`, `fw_service_budget/run.py --self-test`, `baremetal_uart_smoke.py --self-test`, behave, `git diff --check`, hdl reference, soc options) | `b6a1c189` (head) | `0 of 100 gates nonzero or left the tree dirty`; behave `495 scenarios passed, 0 failed` | `gates-final/summary.md` |
| `python3 sw/builder/test_builder.py --require-rv32` (the docs workflow's bank; verdict and image pin gates included) | `c71364bd` | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11 (resource calibration) needs an Arty build tree this host lacks. Tree clean. Carries: the bank reads none of the later commits' files | `builder/builder-require-rv32-c71364bd.log` |
| firmware-unit job: `tally_selftest.py`, `ci_rv32_sdk_selftest.py`, `fw_rv32_selftest.py --require-rv32`, `test_ctrl_firmware.py --require-rv32 --self-test`, `test_ctrl_nvm.py --require-rv32`, `fw_coverage.py --selftest`, `fw_coverage.py --check` | `dc7b1417` | 7 of 7 rc 0; carries: none reads `milan_baremetal.c` or anything changed after | `firmware_unit/` |
| `make -C tb/verilator/nvm_cosim` (every case, controls, the 39 named mutants) | `c71364bd` | rc 0, `465 checks: 465 PASS`, `39 of 39 mutant(s) killed`; dev `1e80128f` also reads 465 | `nvm_cosim/` |
| milan_dp `make dynmap`, `make maprec8`, `make maprec4` | `1767346a` | rc 0: 711/0, 219/0, 137/0; carries: `sim_nxn.cpp` and the RTL unchanged since; the legs read no firmware | `milan_dp/legs-1767346a.log` |
| `make dynmap`, then `python3 dynmap_mutants.py --jobs 3 64 65 66` | `c71364bd` | rc 0, `4 checks: 4 PASS, 0 FAIL`, tree clean | `milan_dp/volatile-mutants-64-66-c71364bd.log` |
| `protocol-processor/tb/pp_top/d3_mutants.py --only identify_is_a_change` | pin `f65c8ff7` | rc 0, `1 of 1 KILLED`, golden PASS | `processor/` |
| `protocol-processor/tb/pp_top/d3_mutants.py --only registry_survives_reset lock_survives_reset identify_survives_reset` | pin `f65c8ff7` | rc 0, `3 of 3 KILLED`, goldens PASS | `processor/` |
| dev firmware against the new host checks (`scripts/dev_firmware_controls.py`) | dev `1e80128f` firmware, head test code | rc 0, all three named checks fail on dev | `dev-firmware-controls.log` |
| capture re-measure: 6 arms | `c71364bd` | 6 of 6 rc 0; receipt passes `check_receipt` | `capture/` |
| service budget: 1x1 `all`, 1x1 `uart-paced`, 8x8 `all`; `gen_oracle.py` twice; `run.py --self-test` | `c71364bd` + the committed `run.py` | 3 of 3 rc 0; generation byte-identical; self-test `55` oracle and `14` flash checks, 0 failures | `service/` |
| `python3 scripts/ci_tool_inventory.py --check` (the CI command table) | `b6a1c189` | NOT RUN: rc 2, `REFUSED: CI_IMAGE_SHFMT must name the checksum-pinned Bash parser` (host environment) | `ci_tool_inventory-check.log` |
| not run, by instruction | | `act_ci.py --selftest` (AGENTS.md: never the candidate's copy on the host), the RTL sweep, Vivado | |

## Open items / risks
- TAKEN cited the lock clause as IEEE 1722.1-2021 7.4.1; LOCK_ENTITY is 7.4.2 (corrected in REVIEW READY).
- `ci/image/command-table.json`: 32 declarations were already stale at dev `1e80128f`, `tb/verilator/milan_dp/dynmap_mutants.py` among them. This lane re-pins only the declared files it changed that were in sync at dev: `test_nvm_firmware.py`, `test_boot_walk.py`, `test_disabled_writer.py` and `fw_service_budget/run.py`. The table's own check refuses on this host; the hosted image workflow will judge it.
- milan_dp README mutant table: rows 1-63 keep their 2026-10-20 totals (686 checks); the README says `[VOLATILE]` added 25 checks after them. A full re-measure of the campaign (about four hours here) was not run.
- `docs/findings/397_SERVICE_BUDGET.md` keeps its dated measurement tables; the regenerated oracle changes no budget finding.
- Bench, out of desk scope (release run of #76): started/stopped across a cycle, a power cut during a commit, the blank-board walk, non-default maps on silicon (#637), the soak, and the volatile set read on the board after a cold cycle.
