[R745] POSITIVE - exact head b6a1c189fa83de85b470c77a2c7c1e5996138909

Internal cleared-context review, round R745-1, of kebag-logic/milan-fpga PR #816 (issue #70), `70-boot-report-link` into `dev`.
Head `b6a1c189fa83de85b470c77a2c7c1e5996138909`, tree `74c696c64d1eb5b12fc7154a38cbc6d656954c50`, source base and live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`.
Whole-PR review of `git diff 1e80128f..b6a1c189` (10 commits, 22 files, no RTL).

STATUS OF THIS FILE: verdict and ledger written after the independent pass and BEFORE any prior public review finding was read. The prior-findings section is appended afterwards.

## Verdict

POSITIVE. All five lenses were applied at the exact head and are CLEAN. There is no open BLOCKER, MAJOR or MINOR. One SUGGESTION (F1, Tests) is optional and leaves coverage unaffected. There is no RESIDUE.

## What was reconstructed, and from where

- AGENTS.md, CONTRIBUTING.md sections 3 and 6, docs/README.md.
- Issue #70 body only. Under the isolation rule no issue or PR comment was listed before this verdict, so scope was taken from the PR body's three pieces and the focus statement: D3 5.3 change 3; the PHY link on every boot path, the persistence-disabled one included; the volatile-set desk check with mutants; plus the capture re-measure and the regenerated firmware-derived records.
- Authorities: `docs/design/SAVED_STATE_MATERIALIZATION.md` 5.3 (change 3) and 9, `docs/design/SAVED_STATE_FASTCONNECT.md` 16, `docs/integration/BAREMETAL_FIRMWARE.md` (boot and PHY), the processor's `tb/pp_top/README.md` and `d3_mutants.py` at pin `f65c8ff7`. Clauses: Milan v1.2 5.3.4.1, 5.3.4.2 and 5.3.12, and IEEE 1722.1-2021 7.4.2, 7.4.25/26 and 7.4.37.
- The diff and its history, then the author's public evidence tree `review-evidence/70b-r1/author` at `999e04e9` (REVIEW-READY.md and the receipts index).

## Findings

### F1 - SUGGESTION - Tests - `sw/firmware/nvm_hosttest/test_phy_firmware.py:3-9,97` - the boot-path arm grades a publication COUNT, not the 250 ms period its docstring states

- Authority/evidence: the module docstring says the shipping and persistence-disabled paths "must publish the peer's link at least every 250 ms while the console idles". The check is `idle < IDLE_MS // PUBLICATION_MS`, so it asks for at least 4 publications in 1000 ms of idle. Probe `scripts/phy_gap_probe.py` (receipt `receipts/phy_gap_probe.txt`) plants a disabled-path poll that stops 600 ms after boot, which leaves about 400 ms of the idle unpolled. The arm returns no finding: `persistence disabled: ... idle_publishes=4 status=13`, "findings on the planted copy: NONE".
- Why SUGGESTION and not MINOR: the shipping firmware is not at fault. Both branches call the same `phy_link_tick()` behind the same `PHY_POLL_NS` (125 ms) gate, and the clean run publishes 8 times in the 1000 ms idle on both paths. The 250 ms bound is graded with observed gaps by `tb/verilator/fw_service_budget/run.py` (`service_findings`, "PHY publication interval exceeds 250 ms", with its one-cycle control at `publication_controls`). BAREMETAL_FIRMWARE scopes that bound to "the measured duties", and the disabled path's duties are a subset of them, with no writer. The arm does catch each realistic defect class: a missing hook, an unarmed poll, the poll behind the writer, a slower poll, and an unguarded poll on an identity mismatch (5 of 5 planted mutants).
- Impact: a disabled-path-only defect that publishes in bursts with gaps over 250 ms would pass this arm.
- Optional outcome: either stamp each `PHY_PUBLISH` with the harness time and grade the largest gap against 250 ms, or state the graded property as "at least four publications per 1000 ms of idle".
- Verification: re-run `scripts/phy_gap_probe.py`. It reports a finding once the gap is graded.

No other finding. Nothing in the reviewed delta breaks the owner comment rule: the scan of added non-markdown, non-JSON lines for lane, round, reviewer and comment-id shapes found none.

## Lens results (clean lenses carry their evidence)

[R745] PASS Conformance - `sw/firmware/milan_baremetal/milan_baremetal.c:1543-1557,1851-1858`, `docs/design/SAVED_STATE_MATERIALIZATION.md:683-687` - D3 5.3 change 3 is met. The bounded wait (`NVM_RESTORE_TIMEOUT_NS`) decides nothing. At its timeout it prints "the restore walk has not reached its terminal; the fabric holds the entity enable until it does." `entity_advertise()` prints "fabric entity enable requested; the fabric holds it until the restore releases it", and it still writes PP_CTRL[0] then ADP_CTRL[0] after the wait. On the PHY item, `phy_live = 1` is set at `:1671` before the shape check, the no-writer heartbeat branch (`:1099-1103`) polls it, and the disabled path installs `set_idle_hook(nvm_service)` (`:1676`), so the link is published on every path past the CSR identity check. The other writer-held and retired paths have `nvm_started = 1` and keep dev's poll-first heartbeat. On the volatile set, `tb/verilator/milan_dp/sim_nxn.cpp:5892-5976` checks Milan v1.2 5.3.4.1 (no lock: `AECP_STAT0[16]` 0 and B's SET_NAME SUCCESS), 5.3.4.2 (B's accepted change notifies nobody) and 5.3.12 (GET_CONTROL reads IDENTIFY 0) across a planted power cycle that reapplies a saved record. Each premise is proved first: notify reaches A, IDENTIFY reads 255, the lock refuses B with ENTITY_LOCKED (Table 7-126 value 3), and the window still holds the saved set. Processor citations D3S7, D3V3, D3V4, D3V5, D3V7, D3V8 and D3V9 exist at pin `f65c8ff7` (`tb/pp_top/README.md:76,365-374,1202,1280-1282`). Capture: the 8x8 contract maximum is 13.86052 ms against 24.5 ms (`receipts/capture_receipt_probe.txt`).

[R745] PASS RTL - `receipts/fw_delta_probe.txt`, `receipts/choke_point_gate.log`, `receipts/dynmap_chain.log` - No RTL file is in the diff, so this lens covered the firmware architecture and the processor-copy plant mechanics. By construction, the diff's changed code lines are just `static int phy_live;`, the braced no-writer branch with its guarded `phy_link_tick()`, `phy_live = 1;`, `set_idle_hook(nvm_service);` and two printf strings. None of them names MILAN_PP_CTRL, MILAN_ADP_CTRL, `aem_loaded` or the `entity_advertise()` call. `entity_advertise`, `configure_fabric`, `nvm_restore_walk`, `milan_init` and `load_aem_image` are byte-identical to dev once printf lines are removed. The six enable-register store sites are the same statements at both revisions: one PP_CTRL[0] and one ADP_CTRL[0] set site, both in `entity_advertise`; the clears are in `configure_fabric`; PP_CTRL[1] is only in `nvm_restore_walk`. So the verdict path `load_aem_image() -> aem_loaded -> entity_advertise(aem_loaded)` is unchanged. The builder's data-flow census `test_baremetal_profile_contract` (gate 1b) ran alone at this head with `~/br-milan-rv32` riscv32-linux-gcc 14.3.0 and passed, rc 0. On the disabled path the writer is never admitted: `nvm_service` returns at `!nvm_ready` and no heartbeat strobe is sent with `nvm_started` 0. The poll there is the same tick the shipping path already runs during its walk, so it adds no boot cost beyond the graded service budget. `dynmap_mutants.py` copies the processor `hdl/` tree whole and hands it to the recipe as `PP_DIR`, so the submodule is never edited (tree clean after the runs).

[R745] PASS Robustness - `sw/firmware/nvm_hosttest/test_boot_walk.py:43-55`, `receipts/host_gate.log`, `receipts/phy_test.log` - The stalled restore (`--walk-stall`, busy for ever) is graded on the cold and the persistence-disabled paths: the timeout line is required, the request line exactly once, and no "entity (is) enabled" claim on any of the 7 paths, CLOSED restores included. An identity mismatch makes 0 MDIO transfers and 0 publications, and the `phy_unguarded` mutant is caught by that check. The writer-restart and disabled-writer suites still pass with the new branch, and the admission mutant was re-anchored to `if (0) {`, which still removes admission (caught in both states).

[R745] PASS Tests - `receipts/host_gate.log`, `receipts/phy_test.log`, `receipts/dynmap_chain.log`, `receipts/pp_d3_controls.log`, `receipts/nvm_cosim.log`, `receipts/fw_coverage_check.log`, `receipts/fw_coverage_selftest.log`, `receipts/budget_selftest.log`, `receipts/capture_gate.log`, `receipts/behave.log` - Every new check fails for the defect it names:
  - Boot walk: 4 of 4 plants are caught by their named finding (`enable_line_claims_enabled`, `timeout_line_holds_unsaid`, and the two existing ones), and the gate ends "OK across 5 shape(s), and every planted defect reddened".
  - PHY: 5 of 5 boot-path mutants are caught by name, then `PHY_BOOT_OK`.
  - milan_dp: `dynmap` reads 711 checks, 0 failures. `dynmap_mutants.py --jobs 3 64 65 66` gives 4 of 4 PASS: lock 3 of 711, registry 1 of 711 and IDENTIFY 1 of 711 failures, each on its own `[VOLATILE]` check.
  - Processor `d3_mutants.py` at the pin: `identify_is_a_change`, `registry_survives_reset`, `lock_survives_reset` and `identify_survives_reset` are 4 of 4 KILLED, goldens PASS.
  - `nvm_cosim` gives 465 of 465 PASS and 39 of 39 mutants killed. `fw_coverage.py --check` reads PASS over 30 files at 100 % lines and branches, and `--selftest` reads 29 of 29.
  - `fw_service_budget/run.py --self-test` gives oracle 55/0 and flash 14/0. `check_nvm_capture.py` passes. behave: 495 scenarios passed. `baremetal_uart_smoke.py --self-test` reads PASS with 13 negative arms (`receipts/uart_smoke_selftest.log`; it grades `PTP_CTRL` bit 0, not the enable line).
  - The registry check only counts over an accepted change, and a missing GET answer reads -1, so neither can pass vacuously.
  - F1 is the only gap, a SUGGESTION.

[R745] PASS Docs - `docs/design/SAVED_STATE_MATERIALIZATION.md:1858-1881`, `docs/design/SAVED_STATE_FASTCONNECT.md:1637-1656`, `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 and section 20 item 6, `docs/integration/BAREMETAL_FIRMWARE.md:2096-2104,2174-2178`, `docs/guides/BOARD_DEPLOYMENT.md:218-229`, `docs/testing/TESTING.md:277`, `tb/verilator/milan_dp/README.md`, `receipts/docs_gates.log`, `receipts/md_gates.log`, `receipts/command_table_probe.txt` - Each changed contract matches the code and the executed numbers:
  - SNAPSHOT_OWNERSHIP's measured commit `c71364bd`, tree `69b8ed0f`, firmware SHA-256 `60799c75...` (which equals `sha256sum` of the head firmware) and pins `f65c8ff7`/`f97c1803` all match git.
  - Its per-arm ranges and ratios match `measurements.json`, recomputed from the rows. The "39 of 96 captures repeat" claim is recomputed against dev's receipt.
  - TESTING.md's 66 controls and the Makefile's 66/57 are 63+3 and 54+3. The README rows 64 to 66 carry the measured 3/1/1-of-711 tallies.
  - Every in-tree reader of the old UART lines moved: the grader, its oracle (3 rows carry the new line once and the old one zero times, each `log_sha256` self-consistent), the boot-walk check and the deployment guide. What remains of the old text is the two dev-line mutant plants and the dated silicon finding `docs/findings/117_GPTP_SILICON_EVIDENCE.md`, which records that earlier firmware and is rightly unchanged.
  - The four re-pinned command-table entries are in sync at both revisions. The PR body's "32 stale declarations at dev" is 27 stale plus 5 absent, unchanged at head.
  - Docs gates at head:
    - With the system interpreter: `docs_check.py`, `check_feature_status.py` (and `--self-test`), `check_doc_style.py`, `check_doc_paths.py`, `check_nvm_record_space.py`, `check_baremetal_only.py --check`, `measure_test_evidence.py --check`, `measure_fail_fast.py --check`, `check_hygiene.py --check`, `check_cpp_idiom.py`, `check_py_idiom.py`, `check_todo_ownership.py`, `measure_naming.py --check`, `ci_gate_workflows.py --check` and `gen_module_matrix.py --check`.
    - With the pinned renderer venv: `check_em_dash.py --base 1e80128f` (0 findings over 105 added lines), `gen_toc.py --verify-anchors` and `gen_toc.py --check`. All rc 0.
    - `receipts/docs_gates.rc` reads 1, for two reasons and no gate finding. Its three renderer-dependent gates refused (rc 2, "the pinned Markdown renderer is not installed") under the system interpreter, and `receipts/md_gates.log` re-runs them green. Its `ci_command_table.py --check` line is the library's circular import (see the limits).

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | D3 5.3 change 3 and 9; FASTCONNECT 16; `milan_baremetal.c` `nvm_restore_walk`, `entity_advertise`, `nvm_boot`, `nvm_heartbeat_tick`; `sim_nxn.cpp` `[VOLATILE]`; processor pin README and `d3_mutants.py`; `measurements.json` | R745-1 | b6a1c189fa83de85b470c77a2c7c1e5996138909 |
| RTL | CLEAN | firmware enable data flow (`fw_delta_probe.txt`), builder gate 1b census run alone at head, `dynmap_mutants.py` `PP_DIR` plant mechanics; no RTL file in the diff | R745-1 | b6a1c189fa83de85b470c77a2c7c1e5996138909 |
| Robustness | CLEAN | `test_boot_walk.py` stalled and CLOSED paths, `nvm_host.c --walk-stall`, PHY identity-mismatch arm, `test_disabled_writer.py` re-anchor | R745-1 | b6a1c189fa83de85b470c77a2c7c1e5996138909 |
| Tests | CLEAN (F1 SUGGESTION) | host gate, PHY test, dynmap leg and mutants 64 to 66, processor D3 controls, nvm_cosim, fw_coverage, service-budget self-test, capture gate, behave, `phy_gap_probe.py` | R745-1 | b6a1c189fa83de85b470c77a2c7c1e5996138909 |
| Docs | CLEAN | the seven changed pages, milan_dp README, `measurements.json` vs SNAPSHOT_OWNERSHIP, command table, oracle, 18 docs gates | R745-1 | b6a1c189fa83de85b470c77a2c7c1e5996138909 |

## Real limits

- No product-CPU run. The capture re-measure and the service-budget timings (boot to the enable -0.011 ms, commit +0.09 ms, heartbeat gap +0.085 ms against dev) were not reproduced: the LiteX product environment was not used in this round. What is checked is that the receipt binds the head firmware's SHA-256, that its rows recompute to its maxima and to the page's figures, and that `check_nvm_capture.py` and the oracle self-test pass.
- The full builder bank `test_builder.py --require-rv32` was not run (not allowed). Only its gate 1b function `test_baremetal_profile_contract` ran, alone, at this head. The author's receipt for the full bank is at `c71364bd`, and nothing it reads changed after that commit except the four test scripts it does not build.
- Not run: `maprec8` and `maprec4` (the diff does not touch their sections), the firmware-unit `test_ctrl_*` scripts, `ci_tool_inventory.py --check`, the full 100-gate docs battery (18 gates reached by these files were run), Yosys, Vivado, act, and anything on hardware. `scripts/ci_command_table.py` is a library, not a CLI: `--check` fails on a circular import when run directly, and `receipts/command_table_probe.txt` stands in for it.
- Physical calibration NOT RUN. The board's cold boot printing the new enable line on the pre-run image is the focus statement's report and was not observed here. The volatile set after a real cold cycle stays owed (FASTCONNECT 16 says so), and so do the #70 bench items.
- Hosted, exact head, at the time of this round: 49 check runs success, 1 skipped, 8 still in progress (7 Verilator shards and "Fail fast across this head"). Not graded here.

## Pending manager duties

- Hosted and act acceptance at the exact head, including the in-flight Verilator shards and the exhaustive Verilator and Yosys contexts.
- The current-dev merge candidate (builder and native banks) at the merge turn. Live dev is still `1e80128f`, the source base.
- The external review and post-merge containment.
- Carry F1 as an optional improvement. It is not a residue item.

## Prior public review findings (read after the verdict and ledger above were on disk)

- PR #816 has one other review, the concurrent external round R746-1: POSITIVE, with no findings. Only its headline was read. There is no prior finding on this PR to resolve.
- The #70 assignment of 2026-10-30 (issue comment 6515314113) fixes this lane's scope. It was read after the verdict and changes nothing above. Each item is met at this head:
  - Change 3 (Conformance).
  - R412-1 S2 (below).
  - The volatile desk check with three failing mutants, and the `:1647` exclusion control cited and re-run (Tests).
  - The consumers it names: graders, `baremetal_uart_smoke.py`, BDD steps and docs, of which only the grader, oracle, boot-walk check and deployment guide read the line (Docs).
  - Its gates: those run here plus the author's receipts listed under the limits.
  - Both STOP conditions are clear: no second write site and no change to the verdict data flow (RTL), and the capture stays inside 24.5 ms.
- R412-1 S2 (PR #623, issue comment 5904318669, carried to #70 by R413-1 F2): "on the persistence-disabled path `nvm_started` is never set, so `phy_link_tick()` never runs and the link-status CSR keeps its reset constant". RESOLVED at this head. `phy_live` is armed at `milan_baremetal.c:1671`, the no-writer branch polls at `:1099-1103`, and the disabled path installs the idle hook at `:1676`. Executed: that path ends with link status 13 and 8 publications in 1000 ms of idle (`receipts/phy_test.log`). Dev's heartbeat, planted as `phy_behind_the_writer`, fails by name.
- R413-1 F2, which recorded D3 5.3 change 3 as open: RESOLVED at this head (Conformance).

## Exact-head restoration

No tracked file was edited. Every probe planted into copies under `scratch/` or into the drivers' own temporary trees. After the runs, `git write-tree` of the index equals the head tree `74c696c64d1eb5b12fc7154a38cbc6d656954c50`, the worktree has no tracked change, and there are 0 untracked non-ignored files. The gitlinks are mode 160000, stage 0, at the pinned commits: protocol-processor `f65c8ff7`, gptp-processor `f97c1803`, verilog-axis `48ff7a7e`, lwSRP `08ee86e8`, tsn-c-stack `70936b77`, external `efeb541a` (uninitialised, as found). The processor and gPTP worktrees are clean at their pins (`receipts/tree_verification.txt`).

R745-1 FINISHED
