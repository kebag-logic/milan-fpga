[A704] REVIEW READY
Commit: `b6a1c189fa83de85b470c77a2c7c1e5996138909` (branch `70-boot-report-link`, 10 local commits on dev `1e80128f`; not pushed)

Changed:
- Enable report (D3 `SAVED_STATE_MATERIALIZATION.md` 5.3, change 3). `entity_advertise()` now prints that it requested the enable and that the fabric holds it until the restore releases it, not "fabric entity enabled". At its timeout the bounded restore wait prints that the restore has not reached its terminal and that the fabric holds the entity enable. The PP_CTRL[0]/ADP_CTRL[0] writes, the single choke point and the verdict data flow are unchanged; the builder's gate 1b passes.
- PHY link on the persistence-disabled path. `nvm_boot()` arms the PHY poll first; the heartbeat's no-writer branch polls it, and that path installs the console idle hook. An admitted writer's heartbeat is textually dev's. After a CSR identity mismatch nothing touches the MDIO pins.
- Volatile set (FASTCONNECT 16, D3 section 9; Milan v1.2 5.3.4.1, 5.3.4.2, 5.3.12). New milan_dp dynmap section `[VOLATILE]`: over a saved entity name, controller A registers, sets IDENTIFY 255 and locks, each proved first. After a planted power cycle (window kept, restore walked) the saved name is back, IDENTIFY reads 0, the lock is clear and the registry is empty. The `:1647` IDENTIFY exclusion control already exists in the pinned processor (`tb/pp_top/d3_mutants.py` `identify_is_a_change`, caught by D3S7): cited and re-run.
- Readers of the two lines: the service-budget grader and its oracle (regenerated through `gen_oracle.py`), the boot-walk host check and the deployment guide. Also the capture receipt (re-measured), SNAPSHOT_OWNERSHIP 18/20 (refreshed from it) and four command-table re-pins. No RTL changes.

Exact strings, for readers outside the repository:
- enable, old: `Milan baremetal: fabric entity enabled; UART diagnostics ready.`
- enable, new: `Milan baremetal: fabric entity enable requested; the fabric holds it until the restore releases it; UART diagnostics ready.`
- timeout, old: `Milan NVM: the restore walk did not sequence in time.`
- timeout, new: `Milan NVM: the restore walk has not reached its terminal; the fabric holds the entity enable until it does.`

Validation (clean clones at the commit named; every rc 0 unless stated):
- Head `b6a1c189`: the docs workflow's 100-gate battery, 0 nonzero. It includes `check_nvm_capture.py` (PASS), `test_nvm_firmware.py --self-test`, `test_phy_firmware.py`, `fw_service_budget/run.py --self-test` (55 oracle and 14 flash checks), `baremetal_uart_smoke.py --self-test` and behave (495 scenarios passed).
- `test_builder.py --require-rv32` at `c71364bd`: ALL GATES PASS EXCEPT 1 NOT RUN. Gate 11 (calibration) needs an Arty build tree this host lacks.
- Firmware-unit job at `dc7b1417`, 7 of 7: `test_ctrl_firmware.py --require-rv32 --self-test`, `test_ctrl_nvm.py`, `fw_coverage.py --selftest` and `--check`, and three self-tests. None reads the bare-metal firmware.
- `nvm_cosim` at `c71364bd`: 465 checks pass and 39 of 39 mutants are killed (dev: 465).
- milan_dp `dynmap` 711/0, `maprec8` 219/0, `maprec4` 137/0. `dynmap_mutants.py 64 65 66` gives 4 of 4 PASS: each processor-copy arm (lock, registry, IDENTIFY kept across the cycle) fails its own `[VOLATILE]` check.
- Processor `d3_mutants.py`: `identify_is_a_change` 1 of 1 KILLED; the three volatile reset arms 3 of 3 KILLED.
- Planted mutants on the host checks, each failing by name. Boot walk: `enable_line_claims_enabled` ("the console claims the entity enabled") and `timeout_line_holds_unsaid` ("the timeout did not report..."). PHY: `phy_behind_the_writer` (dev's heartbeat; "persistence disabled: the link-status CSR holds 0"), `disabled_path_no_idle_hook`, `phy_never_armed`, `phy_off_the_writer_path` and `phy_unguarded`. Dev's own firmware fails all three named checks.
- Capture at `c71364bd`, 6 arms of 16: 8x8 contract maximum 13.86052 ms against 24.5 ms, a margin of 10.63948 ms (3.5352x the 49 ms floor; previous receipt 13.86328 ms). 1x1 3.96490 ms.
- Service budget on the product CPU against a dev run of the same 1x1 plan: boot to the enable -0.011 ms, each commit +0.09 ms, worst heartbeat gap +0.085 ms. No budget finding on either side, and the oracle's findings are unchanged.
- Firmware object: text +246 B, bss +4 B.
- Not run: `ci_tool_inventory.py --check` refuses on this host (pinned Bash parser absent). `act_ci.py --selftest` is not run from the candidate on the host. No sweep and no Vivado (no RTL change).

Acceptance criteria (the [A10] assignment): change 3 is met; the PHY link on every path past the identity check is met; the volatile-set desk check with three failing mutants is met; the `:1647` control is cited and re-run; the readers are listed and updated; the capture holds 24.5 ms. Both STOP conditions are clear.

Open risks/questions:
- `ci/image/command-table.json` already had 32 stale declarations at dev, `dynmap_mutants.py` among them. Only the files this lane changed that were in sync at dev are re-pinned.
- The milan_dp README's mutant rows 1-63 keep their 2026-10-20 totals (686); the README says `[VOLATILE]` added 25 checks after them.
- The volatile set on the board after a cold cycle, and the bench items, stay with the #76 release run.
- Correction to TAKEN: the lock clause is IEEE 1722.1-2021 7.4.2 (LOCK_ENTITY), not 7.4.1.
