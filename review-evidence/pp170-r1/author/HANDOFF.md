# [A577] Lane 3 handoff

Status: REVIEW READY at `c3864686c0b254bd2d7b7f733078ec302fb9be62`, under manager ruling 6087242563. Every acceptance item of processor issue #170 is met. The matched 1x1 OOC comparison shows a zero names-stage delta on every figure, within DR4's ceilings. The 8x8 diagnostic is also unchanged. Both parent frontend checks pass. The head is unchanged from the STOP. Production RTL is byte-identical to the base.

Processor branch: `pp170-names`.
Base: `09e357fb4bf3d35c8a9deba9a787e13f74d08c83`.
Head: `c3864686c0b254bd2d7b7f733078ec302fb9be62`.
Origin `Mister-M-alt/protocol-processor-control-plane-avb-milan` and HEAD verified; tree clean.
Assignment: processor issue #170, comment 6085041490. Ruling: comment 6087242563.

## Scope and stop conditions

Scope: name capture/replay, any NVM framing it needs, tests and docs. No register map, top-level port or parameter change. DR4 names-stage ceilings: +750 LUT-equivalents / +400 FF; cumulative +3,250 / +1,800; no new BRAM or DSP. No STOP condition is met. No scope exception is requested.

## Intake

- Read the exact assignment, the issue #170 body (acceptance items 1–6), #131, PR #132, parent PR #623 and design sections 15–18.
- Inspected the source and mutation tables.
- Ruling 6087242563 resolves the earlier adoption-input question. The two adoption patches in the launch brief were a manager error, and none was supplied. Both historical candidates reverse-apply at parent `5603c353`, so their changes are already present (`patch-input-audit.json`). The approved composition is: the pin, the author gitlink and `parent-name-evidence.patch`.
- `parent-name-evidence.patch` is an input to the separate parent adoption lane. The parent stays uncommitted.
- Standards reviewed: Milan v1.2 §5.3.13 (all user names) and §5.3.12 (IDENTIFY remains volatile). IEEE 1722.1-2021 §7.4.17.1 and §7.4.18.2 (64-byte values and semantic name indices). No standards text is copied into the repository.

## Changes and clauses

All processor changes are confined to the name verification path. Production RTL, existing harnesses, registers, ports and parameters are byte-for-byte unchanged from the base. `git diff 09e357fb c3864686` touches only `tb/name_state/` and one row of `docs/architecture/09_verification.md`. `source-scope.json` records the changed-file identities.

| File:line | Change | Governing clause |
| --- | --- | --- |
| `tb/name_state/sim_main.cpp:11` | Independent complete semantic-name inventory; patterned 64-byte and empty values | Milan v1.2 §5.3.13; IEEE 1722.1-2021 §7.4.17.1 / §7.4.18.2; D3 §18.3 |
| `tb/name_state/sim_main.cpp:31` | Real SET/GET; every framed record; reset-to-default before replay; volatile IDENTIFY | Same name clauses; Milan v1.2 §5.3.12 |
| `tb/name_state/sim_main.cpp:77` | Separate first/last record completion; capture-overlap sweep | D3 §18.3; §15.1 DR2b |
| `tb/name_state/sim_main.cpp:142` | Retained rollback, taint and late-image (healing) name assertions | D3 §18.3; §15.1 DR3a/DR3b |
| `tb/name_state/sim_main.cpp:151` | All-name, late-image and failed-restore timing report | D3 §15.1 DR3a; §18.3 |
| `tb/name_state/fixture.py:25` | Fixed synthetic descriptor populations for the normal regression | D3 §15.1 DR5; §18.3 |
| `tb/name_state/run.py:21` | External build directory; test-only 128-name observation geometry | D3 §18.3 validation; no product-interface change |
| `tb/name_state/mutants.py:19` | Isolated planted defects; completed-run, named-failure grading | D3 §18.3 negative controls |
| `tb/name_state/Makefile:1` | Default suite integration; external mutation output | D3 §18.3 local gates |
| `tb/name_state/README.md:1` | Inventory, oracle, controls, commands and measurement limits | Same clauses as the corresponding checks |
| `docs/architecture/09_verification.md:204` | Complete-name coverage row in the verification table | Milan v1.2 §5.3.13; D3 §18.3 |

The scratch-only `parent-name-evidence.patch` adds the new mutation driver to `scripts/measure_test_evidence_readers.py:22`. It classifies the source reads used to plant defects. Expected names and ordinals are still specified independently. This is the minimal parent gate adoption that the parent-consumer requirement needs. It changes no product logic, RTL or constraint, and it is an input to the parent adoption lane.

The behavior under test is supplied by the existing implementation:

- `KL_aecp_nvm_writer.sv:1131` waits for command completion before its eight-lane latch.
- `:1067` clears only the selected record, and `:1078` retains tainted changes.
- `:747` proves the image before replay at `:842`.
- `:870` retains rollback until descriptor debt is gone.
- `KL_aecp_engine.sv:1993` qualifies command-side name writes and excludes replay writes.
- The engine's local reset at `:1617` reaches both stores, while the guard keeps its hard-reset-only debt.
- `KL_aecp_desc_store.sv:559` initializes names from the image.
- `KL_aecp_dyn_state.sv:280` excludes the IDENTIFY value from the persisted projection.

These paths and the NVM framing are unchanged. The expanded tests found no production correction to make.

## Test expectation changes

No existing test expectation changes.

- The new normal suite adds 169 checks for 1x1 and 441 for 8x8 (610 in total). The increase is needed to grade every generated ordinal instead of five selected names. N0 and the boot/terminal assertions establish premises; the remaining assertions grade values.
- Static file/link inventories grow only by the six new test files and their documentation link:
  - processor IDs: 556→562 files, 1,179→1,180 links;
  - parent C++ units: 313→314;
  - parent Python modules: 368→371.
- The parent evidence inventory becomes 101 suites and 40 classified source readers. Its default-arm count stays at 30. The new mutation campaign is an explicit target, so the unarmed-in-default count becomes 71 (within 77).
- No ratchet is loosened. `static-gate-comparison.json` retains every static-output difference.

## New checks and failing mutants

Every row is observed in both complete base and head campaigns.

- Golden: PASS, 169 checks.
- Fourteen controls: each KILLED in a completed simulation with run rc 1; campaign rc 0.
- A build failure, crash or missing completion tally never counts as a kill.
- The named failures are in the two mutation result files, whose records match exactly.

| Check | Name-value assertion | Failing planted mutant | #170 item 5 control |
| --- | --- | --- | --- |
| N1 | GET_NAME returns each image default | `image_names_zeroed` | — |
| N2 | Real SET and GET preserve every byte | `live_name_lane_dropped` | — |
| N3 | Every 72-byte saved frame matches its independent ordinal/name oracle | `TRG_name`, `name_record_id_shifted` | delete trigger; swap ordinal and record ID |
| N4 | Every name is at its image default before replay | `image_names_zeroed` (explicit N4 failure) | — |
| N5 | Every retained name is read back after reset | `RPL_name`, `name_entry_shifted`, `name_empty_refused`, `name_lanes_partial` | delete replay; empty treated as absent |
| N6 | First-record completion leaves the last changed name saved | `pending_clears_other_name` | clear pending while another name is unsaved |
| N7 | Every observed WRITE carries eight coherent lanes and the latest value | `latch_ignores_program`: 99 mixed frames across 21 overlap offsets | mixed old/new lanes |
| N8 | CONTROL name survives the reset that clears its IDENTIFY value | `identify_survives_reset` | — |
| D3N5 | Failed restoration returns the name to its image default | `store_not_rolled_back` | omit descriptor rollback |
| D3N6 | A change after capture reaches the next complete record | `name_taint_ignored` | — |
| D3N7 | Late image initialization precedes name replay | `names_before_the_image` | replay before image initialization |

The old descriptor-debt and rollback checks remain in the unchanged `pp_top` suite, including D3R10's late-burst arms. No debt-protection source changed. A focused rerun of `rollback_ignores_debt` at both revisions gives:

- a passing golden;
- a completed KILLED control at D3R10 16000;
- identical detailed records, with both campaign rc values 0.

This is the retained debt-protection assertion, distinct from the new name-value checks.

The capture sweep measures the actual fourth-lane phase before sweeping. An initial uncalibrated experiment was rejected: it failed other assertions without failing the intended capture assertion.

## Name inventory and oracle comparison

The parent generators at the pinned parent and processor base produce:

| Class | 1x1 TDM8 | 8x8 diagnostic |
| --- | ---: | ---: |
| ENTITY names | 2 | 2 |
| CONFIGURATION | 1 | 1 |
| AUDIO_UNIT | 1 | 1 |
| STREAM_INPUT, including CRF | 2 | 9 |
| STREAM_OUTPUT, including CRF | 2 | 9 |
| AVB_INTERFACE | 1 | 1 |
| CLOCK_SOURCE | 3 | 10 |
| AUDIO_CLUSTER | 25 | 72 |
| CONTROL | 1 | 1 |
| CLOCK_DOMAIN | 1 | 1 |
| Total | 39 | 107 |

Both inventories fit the existing 128-record name allocation. No inventory growth is proposed, so no #584 authorization is needed.

The C++ oracle enumerates descriptor type, descriptor index and semantic name index from fixed class populations, independently of the image directory and RTL.

- It encodes header, record ID, payload and CRC. All 72 saved bytes are compared at every ordinal.
- Values are patterned full 64-byte non-NUL names, plus empty names at every seventh ordinal starting at two.
- The byte pattern has period 90 in the ordinal, so it does not prove against every permutation of equal payloads. Record headers, IDs and CRCs are checked independently at every ordinal, and the planted ordinal shift fails its value assertion.
- Both ENTITY selectors, CONTROL and the last ordinal are covered.

A separate image-directory parser confirmed all 146 semantic tuples against the oracle inventory. Split directory entries are resolved by each descriptor body's actual index.

- `name-inventory.csv` records each tuple, ordinal, record ID, factory-name digest and expected saved-frame digest.
- `inventory-comparison.json` records the comparison.
- Both generated images pass the final 169/441 checks at base and head, with byte-identical reported results.

The synthetic default-suite images isolate this path; they are not shipping models.

## DR3a restore-path timing

Conditions:

- Generated images; 128-entry test capacity (conservative, with extra blank records).
- Nominal clock 1,000,001 Hz; derived per-wait deadline 20,001 clocks, aggregate 1,000,001 clocks.
- The NVM model returns one byte per cycle. Descriptor latency is 31 or 143 clocks.

These are model measurements, not physical cold-cycle or flash-slot evidence.

| Population | Path | 31-clock memory | 143-clock memory | Verdict |
| --- | --- | ---: | ---: | --- |
| 39 | all names | 15,336 | 15,784 | COMPLETE |
| 39 | late image | 15,471 | 15,919 | COMPLETE |
| 39 | last name pass-1 DEVICE error | 14,768 | 15,664 | DEFAULTS |
| 107 | all names | 26,928 | 27,488 | COMPLETE |
| 107 | late image | 27,063 | 27,623 | COMPLETE |
| 107 | last name pass-1 DEVICE error | 27,888 | 29,008 | DEFAULTS |

Results:

- Longest D3 wait: 1,908 clocks. Binding wait: 12 clocks. D3 record operation: 87 clocks. All are within the ratified budgets.
- The largest terminal measurement, 29,008 clocks, is 2.9% of the 1,000,001-clock aggregate.
- No production restore path changes. All twelve timing records are byte-identical at base and head.
- The test geometry walks extra erased records, so these numbers do not claim exact shipping-parameter geometry or physical service latency.

## OOC 1x1 before/after

The parent's recipe at pin `5603c353` was run in one session for base and head, with the same exports and firmware. The pin contains #607's corrected constraints: PR #615 (`eaa88a32`) merged the #607 branch.

- Synthesis tool: Vivado v2026.1, Build 6511674.
- Device: `xc7a100t-fgg484-2`. Top: `KL_pp_shadow`, the processor plus the parent's wrapper glue.
- Synthesis: `synth_design -mode out_of_context -directive AreaOptimized_high`, `synth.maxThreads 1`, `general.maxThreads 32`.
- Clock: `clk_i` at the bound `CLK_HZ_P`, 50 MHz (20.000 ns).
- Wrapper parameters come from an RTL-only elaboration (`synth_design -rtl`) of each shape's generated export. `elaborate.tcl` is the exported build script, cut before its constraint and implementation steps. `pp_baseline.py` reads only the wrapper's elaborated parameter block from its log. Each shape was elaborated once, with the base checkout, and the head preparation read the same log. The equal input digest, which includes every generic, confirms the parameters are identical.
- No placement is requested at this endpoint, so a placement seed does not apply.

Every vendor invocation ran under the exclusive lock as a detached background job with no timeout (`resumed-invocations.csv`). The first base synthesis queued about 1 h 55 min behind another lane's exclusive hold. Nothing was withdrawn.

| 1x1 TDM8 (`KL_pp_shadow`) | Base `09e357fb` | Head `c3864686` | Delta |
| --- | ---: | ---: | ---: |
| LUT (all) | 23,171 | 23,171 | 0 |
| of which LUTRAM | 2,728 | 2,728 | 0 |
| FF | 19,807 | 19,807 | 0 |
| RAMB36 / RAMB18 (BRAM tiles) | 16 / 3 (17.5) | 16 / 3 (17.5) | 0 |
| DSP | 8 | 8 | 0 |
| CARRY4 | 1,494 | 1,494 | 0 |
| WNS / WHS at 20 ns | +3.203 / +0.159 ns | +3.203 / +0.159 ns | 0 |

Comparison of the two records:

- Tool identity, device, design, flow and clock are equal.
- The design-input digest is equal. It covers every read source, include, generic and memory image.
- All 57 hierarchy rows, all scope records and the per-scope timing file are equal.

`resumed-measurement-comparison.json` and the four `ooc-*.json` records hold the complete figures.

**DR4 names stage: within the ceiling.** The 1x1 delta is 0 LUT-equivalents / 0 FF / 0 BRAM / 0 DSP, against +750 / +400 / 0 / 0. The DSP delta is zero, so the LUT-equivalent delta equals the LUT delta. The parent glue is inside `KL_pp_shadow`, and the scratch parent changes no RTL, so processor and parent glue are included together.

This stage adds nothing to the cumulative D3 total. The cumulative total after lane 3 equals the scalar-core total from lanes 1–2:

- Lane 1 measured +1,031 LUT / +559 FF / 0 / 0 with the same instrument in PR #132.
- PR #623 left lane 2's matched post-place comparison open.

A scalar-core total within its 2,500 / 1,400 ceiling therefore stays within the 3,250 / 1,800 cumulative ceiling. The absolute figures belong to this session's instrument at this pin. The DR4 quantity is the matched delta.

| 8x8 diagnostic (`KL_pp_shadow`) | Base | Head | Delta |
| --- | ---: | ---: | ---: |
| LUT (LUTRAM) | 30,141 (2,658) | 30,141 (2,658) | 0 |
| FF | 27,401 | 27,401 | 0 |
| RAMB36 / RAMB18 | 21 / 5 | 21 / 5 | 0 |
| DSP | 8 | 8 | 0 |
| WNS / WHS at 20 ns | −3.243 / +0.159 ns | −3.243 / +0.159 ns | 0 |

The 8x8 synthesis diagnostic is retained and unchanged. Its negative OOC WNS is pre-existing at the base. Its post-place obligation stays open and blocked, not waived, and it remains non-shipping (#584/#229).

Firmware was held fixed between the base and head exports, and no firmware source changes. `firmware-footprint.json` records the binary and ELF identities.

| Shape | Text | Data | BSS | ROM image / capacity | Data+BSS / SRAM capacity |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1x1 TDM8 | 52,524 B | 584 B | 2,164 B | 53,116 / 131,072 B | 2,748 / 8,192 B |
| 8x8 diagnostic | 52,684 B | 584 B | 2,164 B | 53,276 / 131,072 B | 2,748 / 8,192 B |

Firmware growth is 0 B. The SRAM column covers static data and BSS, not a measured runtime stack maximum. No hardware execution is claimed.

## Processor suites

| Gate | Base | Head | Evidence |
| --- | --- | --- | --- |
| All suites (`scripts/run_suites.sh`) | rc 0; 1,028,293 checks / 33 suites | rc 0; 1,028,903 checks / 34 suites | `suite-record-comparison.json` |
| HDL lint (`scripts/lint_hdl.sh`) | rc 0 | rc 0 | base/lint.log, head/lint.log |
| `make check` | rc 0 | rc 0 | base/check.log, head/check.log |
| `scripts/gen_matrix.py --check` | rc 0 | rc 0 | base/matrix.log, head/matrix.log |
| `syn/yosys/run.sh` | rc 0 | rc 0 | base/synthesis.log, head/synthesis.log |

All 33 pre-existing suites have identical retained simulation records, including printed values, cycles and seeds. Only compiler/build output, generated-ROM announcements and host unit-test durations are excluded. The full head suite runs from a byte-verified export of all 587 tracked files, so generated outputs stay outside the primary worktree.

## Campaigns

Only the new `tb/name_state` files are compiled by a changed-file campaign. Existing campaigns do not build these files, and production and shared harness bytes are unchanged.

| Campaign | Base | Head | Result |
| --- | --- | --- | --- |
| `tb/name_state` mutation campaign | rc 0 | rc 0 | Golden PASS; 14/14 KILLED by their named assertions; complete records identical |
| `tb/pp_top` `rollback_ignores_debt` (retained debt control) | rc 0 | rc 0 | Golden PASS; KILLED at D3R10; records identical |
| Generated 1x1 / 8x8 inventories, functional and `--measure` | rc 0 ×4 | rc 0 ×4 | 169 / 441 checks; identical results and timing |

The final head campaign was rerun through its Makefile `mutants` target after the output-path fix: 14/14 KILLED, rc 0, records matching the baseline.

## Parent consumer

Scratch parent: milan-fpga dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee`, detached. Required gPTP and stream-support submodules are initialized at their pins.

- The processor checkout and gitlink were switched together for each matched run. Both finish at the author head.
- The only other change is `parent-name-evidence.patch`, applied with `git apply`.
- The parent is uncommitted and unpushed.
- `final-source-state.json` records all three submodule pins and their clean worktrees.

All seventeen consumer gates pass at base and head. The evidence gate's initial unexplained-reader refusal is retained, and the classified gate passes.

Output comparisons:

- `parent-record-comparison.json`: eleven equal output blocks.
- `nvm-file-comparison.json`: all 724 equal case files. Binary journals are compared without normalization.
- Only host phase durations and two printed host allocation pointers are normalized. Value, cycle, event and completion records are preserved.

| Parent consumer command | Base | Head | Result / boundary |
| --- | --- | --- | --- |
| `python3 scripts/check_cpp_idiom.py` | 0 | 0 | No findings; new translation unit counted |
| `python3 scripts/check_py_idiom.py` | 0 | 0 | No findings; three new modules counted |
| `python3 scripts/check_rtl_source_lists.py` | 0 | 0 | Identical |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0 | Identical |
| `python3 scripts/check_port_contracts.py` | 0 | 0 | Identical |
| `python3 scripts/measure_naming.py --check` | 0 | 0 | Identical |
| `python3 scripts/measure_test_evidence.py --check` | 0 | 0 | New suite and classified mutation reader only |
| `python3 scripts/docs_check.py` | 0 | 0 | Identical |
| `python3 scripts/check_sh_idiom.py` | 0 | 0 | Identical |
| `python3 sw/builder/test_builder.py` | 0 | 0 | 389 named records identical after host-metadata normalization; historical gate-11 calibration report absent at both revisions |
| `python3 scripts/lint_rtl.py --check` | 0 | 0 | Identical: 90 findings within the existing 90 ratchet |
| `make -j16 -C tb/verilator/pp_shadow` | 0 | 0 | 2,184 checks across four binaries; every retained record identical |
| `make -j16 -C tb/verilator/nvm_cosim lint` | 0 | 0 | Existing diagnostics only |
| `make -j16 -C tb/verilator/nvm_cosim quick JOBS=4 POOL=2` | 0 | 0 | 315 checks / 62 cases; all 724 retained case files identical |
| `make -j16 -C tb/verilator/milan_dp SIM_JOBS=2` | 0 | 0 | 12,065 checks; pool and default controls match across 12,585 report lines, excluding host phase durations |
| `make -j16 -C tb/verilator/milan_dp_render` | 0 | 0 | 71 + 258 + 5 checks; synchronized records identical |
| `python3 scripts/xvlog_gate.py --check` | 0 | 0 | PASS: 0 findings = ratchet over 81 parent and 52 pinned-processor files; logs identical except the line naming the processor pin |

Initial setup refusals are retained separately:

- Submodule registration was initialized before the successful baseline static runs.
- The new mutation-reader classification was added before the successful head evidence run.

No threshold was increased. The builder's absent calibration arm remains outside these results.

## Reproduction

Use the pinned 5.050 simulation compiler through `VERILATOR` and the executable search path. The full suite uses `MAKEFLAGS=-j16`. Run each gate with a separate log and rc receipt, without a pipe.

Processor:

```sh
scripts/run_suites.sh
scripts/lint_hdl.sh
make -j16 check
python3 scripts/gen_matrix.py --check
syn/yosys/run.sh
python3 tb/name_state/mutants.py --jobs 2 --output /tmp/name-controls
python3 tb/pp_top/d3_mutants.py --jobs 2 --only rollback_ignores_debt --output /tmp/debt-controls
python3 tb/name_state/run.py --image /tmp/1x1.img.bin --aaf 1
python3 tb/name_state/run.py --image /tmp/8x8.img.bin --aaf 8
python3 tb/name_state/run.py --image /tmp/1x1.img.bin --aaf 1 --measure
python3 tb/name_state/run.py --image /tmp/8x8.img.bin --aaf 8 --measure
```

Parent OOC, for each shape. `elaborate.tcl` is the exported `alinx_ax7101.tcl`, cut before its constraint section and ending with `synth_design -rtl` for the same top, part and include directories, then `quit`. Run it beside the exported constraint and memory-initialization files, then prepare and synthesize the standalone endpoint in a new directory:

```sh
vivado -mode batch -source elaborate.tcl -nojournal -log elaborate.log
python3 syn/ooc/pp_baseline.py <export>/gateware --single-thread-synthesis --integrated-clock --output <ooc-dir> --integrated-log <elaboration-dir>/elaborate.log
vivado -mode batch -source baseline_ooc.tcl -nojournal -log baseline.log
python3 scripts/xvlog_gate.py --check
```

Run the vendor commands one at a time, never beside another heavy build.

The new suite did not exist at the base commit. Its baseline campaign uses the same new harness over an external source export of the base production and shared-test files. `baseline-source-proof.json` verifies all 181 such inputs against the base blobs, and `head-export-proof.json` verifies all 587 tracked head files used by the full suite. No Git checkout beyond the authorized scratch parent was created.

## Artifact inventory

- `gate-results.csv` maps every accepted invocation (33 rows, all rc 0 at base and head) to its base/head rc and external log.
- `resumed-invocations.csv` lists the twelve resumed lock-held or preparation invocations with lock-acquisition time, rc and log hash.
- `EXTERNAL-ARTIFACTS.csv` records the size and SHA-256 of 448 files under the external evidence root `$VALIDATION_STORAGE/pp170-a577`.
- `OUTPUT-ARTIFACTS.csv` records this directory.

The external root holds build trees, complete logs, generated images, firmware, checkpoints and reports. No build tree, installed package or file above 200,000 bytes is in this output directory.

## History: STOP and resolution

- The STOP (comment 6087210228) had two causes: the two adoption patches named in the launch brief were absent, and the exclusive lock was unavailable for 648 s, so a queued invocation was withdrawn before vendor startup. `measurement-blocker.json` keeps that historical boundary.
- Ruling 6087242563 confirmed that no adoption patch was needed and asked for detached lock-held runs with no timeout. Those runs completed above.
- One resumed queue was interrupted by an external session limit before acquiring the lock (no vendor child). Its record is kept under `resume-interrupted/`, and the full sequence was rerun from the start.

## Final state

- Both processor commits use one-line subjects with no body or trailers. No commit was added this round.
- The primary tree is clean at the head.
- The scratch parent is at its pin, uncommitted and unpushed. Only its staged processor gitlink (author head) and the evidence-classification patch are changed, and temporary export links were removed.
- No owned job remains running (`final-process-state.json`).
- No push, PR creation, hardware operation or existing-comment edit was performed.

Final issue status: [REVIEW READY with the head](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/170#issuecomment-6091061489).
