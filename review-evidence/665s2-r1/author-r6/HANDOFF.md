# [A681f] #665 lane S2, round 6: classify the harness's files for the TSN stack boundary gate (HANDOFF)

Status: **REVIEW READY**, 2026-10-27. The hosted `firmware-boundary` refusal is fixed by classifying the six harness files in `ctrl_configs.py`. The gate passes locally at the head exactly as the workflow runs it, and every other gate is rc 0. No firmware, image or figure changed.

- Head: `e0e1b4649ea3af908a8f32eccaad7903fa2cc134`, one commit on round 5's `f58d049beb377c3f535628067022d4d5b51e8208`:
  - `e0e1b464` `Classify the CPU budget harness's six files the TSN stack boundary gate finds by text, each with what it compiles (#665)`. It has a one-line subject, no body and no trailers.
- Branch `665-s2-cpu-budget`, base `origin/dev-soft-core` `e76a755afc0536453161e3cd33f6f4d2dcd7641f`. The lane is not rebased. PR #792 targets `dev-soft-core`.
- Remote `https://github.com/kebag-logic/milan-fpga.git` (verified).
- Git ran inside submodules only in a scratch clone (section 6), and only after `rev-parse --show-toplevel` and origin were checked:
  - `protocol-processor`: origin is the processor repository;
  - `gptp-processor`: origin is the gPTP repository.
- Assignment: issue #665 issuecomment-6435512208. Hosted failure: run 40408916714, job `firmware-boundary`, exit 2.
- TAKEN: issuecomment-6438501884 (`TAKEN-COMMENT.md`). It published the departure from the assignment's two named options before any edit.
- REVIEW READY: issuecomment-6441276168 (`REVIEW-READY-COMMENT.md`). The PR body for the manager is `PR-BODY.md`.
- Nothing pushed. No PR, issue or comment edited. No Vivado, bench or hardware.

## Contents

1. [Result](#1-result)
2. [The failure and the decision](#2-the-failure-and-the-decision)
3. [Changes, file:line and reason](#3-changes-fileline-and-reason)
4. [Checks, planted mutants and failing words](#4-checks-planted-mutants-and-failing-words)
5. [Gate table](#5-gate-table)
6. [No image or figure change](#6-no-image-or-figure-change)
7. [Run history](#7-run-history)
8. [Acceptance](#8-acceptance)
9. [Open items, risks and questions](#9-open-items-risks-and-questions)

## 1. Result

- The hosted step that failed, run locally exactly as `rtl-fast.yml` writes it at the head: `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator`.
  - It printed `ctrl_boundary: PASS`, rc 0, in 939 s, with the tree clean after it.
  - Its summary line: `ctrl_boundary: 2854 compiled sources of 3084 recorded invocations (1639 the firmware's, 347 the stack's, 868 test equipment's and builders' own), ... 0 finding(s), 112 boundary, 167 pin and 4 figure controls, 0 misbehaved`.
  - Log: `receipts/gates/fw_boundary_without_verilator.log`.
- The rest of rtl-fast's firmware jobs' steps, the harness self-test and mutants, the bare-metal scope gate, the full docs-check set and behave: 107 gates, every one rc 0, the tree clean after each (section 5).
- The full Verilator sweep, because a shared file changed: 64 of 64 suites passed in four shards, 2,190,531 checks, 0 in-suite failures, rc 0 each.
- No firmware, harness code, measurement or published figure changed.
  - The nine harness images (six arms, three controls) were rebuilt at the head. Each ELF is byte-identical to round 2's (section 6).
  - The STOP condition ("registering the builder would change any firmware image or published figure") is not met.

## 2. The failure and the decision

The hosted refusal (`receipts/hosted_40408916714_refusal.txt`) names six files, not only `build.py`:

- four programs: `build.py`, `fixture_variant.py`, `runtime_ssp.py` and `selftest.py`;
- two modules that compiled nothing in the capture: `scenario.py` and `split_soc.py`.

The assignment quotes the message up to PART_OF. The message itself continues "compiles none of the firmware's (OUTSIDE) or compiles only in a suite (SUITES)", and `ctrl_configs.py`'s docstring defines all four categories.

Each file was classified by what it compiles:

| File | Category | Evidence |
|---|---|---|
| `build.py` | OUTSIDE | `build.py:124-145` (`firmware`): the runtime through `runtime_ssp.py`, then the image through `ctrl_srp_image.py` (or `fixture_variant.py` for a variant), each a subprocess. `:110-121`: a control's planted copy of `sw/firmware/ctrl` outside the checkout, passed as `--ctrl-source`. `:333-346`: its own compiles are Verilator and `make` of the native model. `run.py:29` POINTS are exactly `ctrl_image.SHAPES` at 1 and 2 interfaces. `ctrl_runs.py:62-81` runs `ctrl_srp_image.py --with-aecp` at both shapes and both interface counts on every gate run. `ctrl_srp_image.py:80-95`: `--layout split` and the runtime archives act only in `link()`. The split layout's extra compile, `plat/ctrl_split_start.S`, is the one `sw/litex/ctrl_memory_probe.py:27` compiles under `test_ctrl_memory.py --build-only`. Precedent: the `tb/verilator/milan_dp/Makefile` OUTSIDE entry. |
| `runtime_ssp.py` | OUTSIDE | `runtime_ssp.py:21-32`: runs `ctrl_image_runtime.py` (OUTSIDE, "no firmware or stack source") with one added flag. |
| `scenario.py` | OUTSIDE | `scenario.py:483-487`: reads `aecp.h`. The file has no `subprocess`. |
| `selftest.py` | OUTSIDE | `selftest.py:65`, `:605`: reads `aecp.h`. It calls `build.digest`, `run_inputs`, `tree_digest` and `reused` only (`:687-694`). No `subprocess`. |
| `split_soc.py` | OUTSIDE | `split_soc.py:313`: `Builder(..., compile_software=False, compile_gateware=False)`; `:60-80`: reads `ctrl_build.RV32_FLAGS` and the store's generated headers. |
| `fixture_variant.py` | SUITES | `fixture_variant.py:15-20`: runs `ctrl_srp_image.main()` in-process with `HERE` set to `build.py`'s edited copy (`build.py:92-107`). Used only with `run.py --variant`. |

**Why not BUILDERS.**

- A BUILDERS entry must hold an invocation from a run of its own, unless the run leaves it out (`ctrl_configs.py:312-314`). The gate's standalone mode refuses a builder that exits non-zero (`ctrl_runs.py:140-143`).
- `build.firmware` imports `pythondata_software_picolibc` and `pythondata_software_compiler_rt`. No workflow or CI script installs them (`grep -rn picolibc .github/workflows scripts/ci_*.py sw/litex/*.txt`: no match).
- The SoC export needs the patched LiteX tree (`sw/litex/litex_pins.txt:20-33`) together with Verilator. `firmware-boundary` installs the pins but has no Verilator. `firmware-verilator` installs only PyYAML.
- So a BUILDERS entry needs a workflow and generator change. That is outside this lane's scope, so it was not made.

**Why not PART_OF.** No known builder runs these files. `run.py` is their parent, and it names no firmware tree.

## 3. Changes, file:line and reason

| File:line (head `e0e1b464`) | What | Reason |
|---|---|---|
| `sw/firmware/ctrl/test/ctrl_configs.py:179-180` | comment: no hosted job can run the harness's build, so none of it is a known builder | why OUTSIDE/SUITES and not BUILDERS |
| `sw/firmware/ctrl/test/ctrl_configs.py:181-188` | OUTSIDE `build.py` | section 2 |
| `sw/firmware/ctrl/test/ctrl_configs.py:189-192` | OUTSIDE `runtime_ssp.py` | section 2 |
| `sw/firmware/ctrl/test/ctrl_configs.py:193-194` | OUTSIDE `scenario.py` | section 2 |
| `sw/firmware/ctrl/test/ctrl_configs.py:195-196` | OUTSIDE `selftest.py` | section 2 |
| `sw/firmware/ctrl/test/ctrl_configs.py:197-200` | OUTSIDE `split_soc.py` | section 2 |
| `sw/firmware/ctrl/test/ctrl_configs.py:217-220` | SUITES `fixture_variant.py` | section 2 |
| `tb/verilator/ctrl_service_budget/README.md:107-117` | "The test SoC": the six files, their categories and why; a new file naming the firmware's tree must be listed | Docs: the harness's contract with the gate |

No other file changed: `git diff --numstat f58d049b e0e1b464` reports `26 0 ctrl_configs.py` and `12 0 README.md`. No gate code, control or other entry changed.

## 4. Checks, planted mutants and failing words

No check was added: the gate's own found-by-text rule is the check, and the hosted run is its failing case. The new entries were mutated one at a time to show that each is load-bearing.

`scripts/classification_probe.py` runs `ctrl_configs.held` on the checkout with a stub capture. In the stub, every known builder ran and every PART_OF program and non-program compiled, except the harness's files. So only the found-by-text classification can refuse.

| Case | Result (`receipts/classification_probe*.txt`) |
|---|---|
| head `e0e1b464` | `PASS` |
| head `f58d049b` (no entries) | `REFUSED:` with the six refusals, **byte-identical** to the hosted log line (compared: `identical`) |
| each of the six entries removed in turn | `CAUGHT`. The refusal names exactly that file and nothing else, e.g. `REFUSED: tb/verilator/ctrl_service_budget/build.py names the firmware's tree and is a program, and is neither a known builder (ctrl_configs.BUILDERS) nor listed as one that runs under another (PART_OF), compiles none of the firmware's (OUTSIDE) or compiles only in a suite (SUITES)`. For `scenario.py` and `split_soc.py` the words are `... names the firmware's tree, compiled nothing in the capture, and is neither a known builder ...` |

The harness self-test is unchanged: 87 `PASS`, 62 `MUTANT caught`, `self-test: 0 failures`. `scripts/mutant_table_check.py` matches all 62 README rows (`receipts/mutant_table_check.txt`).

## 5. Gate table

Every gate ran at the head `e0e1b4649ea3af908a8f32eccaad7903fa2cc134`, one at a time, in a single runner (`scripts/gates_r6.py`).

- The runner is round 5's with eleven rtl-fast firmware steps added. The boundary gate runs first; it is the step the hosted run failed.
- It refuses to start on a dirty tree. After every gate it checks `git status --porcelain --untracked-files=all --ignore-submodules=none`, and it stops at the first gate that leaves the tree dirty. None did.
- It was started detached (`setsid nohup`) and polled with foreground waits, because four gates exceed ten minutes.
- Each log is in `receipts/gates/`, with its rc and the tree's state on its last lines. `HEAD.txt` names the head, `summary.md` is the runner's table with each gate's seconds, and `serial.out` is its console.
- Two logs exceed 200 KB: `bdd_conformance.log` and `ci_events_selftest.log`. Each is kept out of the packet, with its size, sha256 and last lines in `<log>.digest.txt`.

Environments:

- The firmware jobs' steps ran with the host's `python3`, which has PyYAML, as `firmware-unit` and the mutant jobs install it, and with the system GoogleTest and GoogleMock.
- `firmware-boundary`'s step ran with the product LiteX environment's `python3` first on `PATH`, which has PyYAML and the LiteX pins the job installs.
- `firmware-verilator`'s step ran with the pinned Verilator 5.050 first on `PATH` (`rtl-fast.yml` `VERILATOR_VERSION: v5.050`).
- Every firmware step used the pinned RV32 SDK at its installed path.
- `CI_CAMPAIGN_JOBS` was 8. Hosted, it is `min(nproc, 4)`. The value sets parallelism only.
- The Markdown gates ran with round 4's pinned-renderer environment, and the HDL reference with its own, as in round 5.

Key verdicts:

- `fw_boundary_without_verilator`, the hosted failure: `ctrl_boundary: PASS`, `0 finding(s), 112 boundary, 167 pin and 4 figure controls, 0 misbehaved` over 3084 recorded invocations.
- `fw_boundary_only_verilator`: `ctrl_boundary: PASS` over 934 invocations (the MBX bench, the MAAP differential and the AECP wire comparison), 0 findings.
- `test_ctrl_firmware: PASS` on each of the four shards.
- `saved-state store gate (#665 F1): OK across 5 shape(s), 435 tests`.
- `firmware coverage: PASS (30 files)`; coverage self-test 29 of 29; tally self-test 18 of 18; `RV32 build self-test: 17 checks PASS`.
- `baremetal-only: OK (0 findings across 1431 tracked first-party file(s))`.
- Harness `self-test: 0 failures`: 87 `PASS` and 62 `MUTANT caught`. All 62 README mutant rows match.
- `check_em_dash: 0 finding(s) over 655 added line(s) in 1 changed Markdown page(s) ... [e76a755a..HEAD]`.
- `docs_check: 0 finding(s) across 211 md files + 1433 scrubbed text files`.
- `TOC gate: OK`, and the anchor check reproduces all 545 cross-page fragment links. `doc path gate: OK (1062 cited paths all resolve ...)`. `documentation style: OK`.
- `GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations`: the compiler-absent control, whose NOT RUN is the compiled census this mode hides.
- `ALL GATES PASS EXCEPT 1 NOT RUN`: the end-station builder, whose gate 11 needs an mf48 calibration build tree this host lacks, as in rounds 4 and 5.
- behave: 14 features passed, 406 scenarios passed, 1977 steps passed.

| Gate (log `receipts/gates/<gate>.log`) | Command | rc | Tree after |
|---|---|---:|---|
| `fw_boundary_without_verilator` | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator` | 0 | clean |
| `harness_selftest` | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | 0 | clean |
| `baremetal_check` | `python3 scripts/check_baremetal_only.py --check` | 0 | clean |
| `baremetal_selftest` | `python3 scripts/check_baremetal_only.py --selftest` | 0 | clean |
| `wire_accountability_selftest` | `python3 scripts/check_wire_accountability.py --self-test` | 0 | clean |
| `docs_check` | `python3 scripts/docs_check.py` | 0 | clean |
| `feature_status` | `python3 scripts/check_feature_status.py` | 0 | clean |
| `feature_status_selftest` | `python3 scripts/check_feature_status.py --self-test` | 0 | clean |
| `traceability_matrix` | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | clean |
| `em_dash` | `python3 scripts/check_em_dash.py --base e76a755afc0536453161e3cd33f6f4d2dcd7641f` | 0 | clean |
| `em_dash_selftest` | `python3 scripts/check_em_dash.py --selftest` | 0 | clean |
| `doc_style` | `python3 scripts/check_doc_style.py` | 0 | clean |
| `doc_style_selftest` | `python3 scripts/check_doc_style.py --selftest` | 0 | clean |
| `gptp_docs` | `python3 scripts/check_gptp_docs.py` | 0 | clean |
| `gptp_docs_selftest` | `python3 scripts/check_gptp_docs.py --selftest` | 0 | clean |
| `gptp_docs_with_submodule` | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | clean |
| `gptp_processor_docs` | `make -C gptp-processor docs PYTHON=python3` | 0 | clean |
| `doc_map` | `python3 docs/DOC_MAP.gen.py --check` | 0 | clean |
| `doc_map_selftest` | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | clean |
| `timesync_chain` | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | clean |
| `timesync_chain_selftest` | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | clean |
| `solution_docs` | `python3 scripts/check_solution_docs.py` | 0 | clean |
| `solution_docs_selftest` | `python3 scripts/check_solution_docs.py --selftest` | 0 | clean |
| `submodule_boundaries` | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | clean |
| `submodule_boundaries_selftest` | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | clean |
| `submodule_docs` | `python3 scripts/check_submodule_docs.py` | 0 | clean |
| `submodule_docs_selftest` | `python3 scripts/check_submodule_docs.py --selftest` | 0 | clean |
| `wavedrom_selftest` | `python3 scripts/gen_wavedrom.py --selftest` | 0 | clean |
| `wavedrom_axis_backpressure` | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | clean |
| `wavedrom_cdc_handshake` | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | clean |
| `wavedrom_gptp_pdelay` | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | clean |
| `diagram_pngs` | `python3 scripts/check_diagram_pngs.py` | 0 | clean |
| `diagram_pngs_selftest` | `python3 scripts/check_diagram_pngs.py --selftest` | 0 | clean |
| `control_flow_selftest` | `python3 scripts/measure_control_flow.py --selftest` | 0 | clean |
| `cohesion_selftest` | `python3 scripts/measure_cohesion.py --selftest` | 0 | clean |
| `rv32_sdk_selftest` | `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | clean |
| `firmware_compiler_selftest` | `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 | clean |
| `firmware_compiler_absent` | `python3 sw/builder/test_firmware_compiler.py --absent --audit <scratch>/tmp/rv32-absent.jsonl` | 0 | clean |
| `nvm_record_space` | `python3 scripts/check_nvm_record_space.py` | 0 | clean |
| `nvm_record_space_selftest` | `python3 scripts/check_nvm_record_space.py --self-test` | 0 | clean |
| `nvm_capture` | `python3 scripts/check_nvm_capture.py` | 0 | clean |
| `nvm_firmware_selftest` | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | clean |
| `soc_sources` | `python3 scripts/check_soc_sources.py` | 0 | clean |
| `soc_sources_selftest` | `python3 scripts/check_soc_sources.py --selftest` | 0 | clean |
| `iob_pack_selftest` | `python3 sw/litex/iob_pack_selftest.py` | 0 | clean |
| `rtl_source_lists` | `python3 scripts/check_rtl_source_lists.py` | 0 | clean |
| `rtl_source_lists_selftest` | `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | clean |
| `naming` | `python3 scripts/measure_naming.py --check` | 0 | clean |
| `naming_selftest` | `python3 scripts/measure_naming.py --selftest` | 0 | clean |
| `port_contracts` | `python3 scripts/check_port_contracts.py` | 0 | clean |
| `port_contracts_selftest` | `python3 scripts/check_port_contracts.py --selftest` | 0 | clean |
| `fail_fast` | `python3 scripts/measure_fail_fast.py --check` | 0 | clean |
| `fail_fast_selftest` | `python3 scripts/ci_fail_fast_selftest.py` | 0 | clean |
| `todo_ownership` | `python3 scripts/check_todo_ownership.py` | 0 | clean |
| `todo_ownership_selftest` | `python3 scripts/check_todo_ownership.py --selftest` | 0 | clean |
| `test_evidence` | `python3 scripts/measure_test_evidence.py --check` | 0 | clean |
| `test_evidence_selftest` | `python3 scripts/measure_test_evidence.py --selftest` | 0 | clean |
| `hygiene` | `python3 scripts/check_hygiene.py --check` | 0 | clean |
| `hygiene_selftest` | `python3 scripts/check_hygiene.py --selftest` | 0 | clean |
| `sv_idiom` | `python3 scripts/check_sv_idiom.py` | 0 | clean |
| `sv_idiom_selftest` | `python3 scripts/check_sv_idiom.py --selftest` | 0 | clean |
| `cpp_idiom` | `python3 scripts/check_cpp_idiom.py` | 0 | clean |
| `cpp_idiom_selftest` | `python3 scripts/check_cpp_idiom.py --selftest` | 0 | clean |
| `py_idiom` | `python3 scripts/check_py_idiom.py` | 0 | clean |
| `py_idiom_selftest` | `python3 scripts/check_py_idiom.py --selftest` | 0 | clean |
| `sh_idiom` | `python3 scripts/check_sh_idiom.py` | 0 | clean |
| `sh_idiom_selftest` | `python3 scripts/check_sh_idiom.py --selftest` | 0 | clean |
| `doc_paths` | `python3 scripts/check_doc_paths.py` | 0 | clean |
| `archive` | `python3 scripts/check_archive.py` | 0 | clean |
| `archive_selftest` | `python3 scripts/check_archive.py --selftest` | 0 | clean |
| `toc_selftest` | `python3 scripts/gen_toc.py --selftest` | 0 | clean |
| `toc_verify_anchors` | `python3 scripts/gen_toc.py --verify-anchors` | 0 | clean |
| `toc_check` | `python3 scripts/gen_toc.py --check` | 0 | clean |
| `aem_store_selftest` | `python3 avdecc/gen_aem_store.py --self-test` | 0 | clean |
| `sweep_shape_selftest` | `python3 scripts/check_sweep_shape.py --self-test` | 0 | clean |
| `deploy_shape_selftest` | `python3 scripts/check_deploy_shape.py --self-test` | 0 | clean |
| `entity_shape_selftest` | `python3 scripts/check_entity_shape.py --self-test` | 0 | clean |
| `gate_workflows` | `python3 scripts/ci_gate_workflows.py --check` | 0 | clean |
| `gate_workflows_selftest` | `python3 scripts/ci_gate_workflows_selftest.py` | 0 | clean |
| `case_receipts_selftest` | `python3 scripts/ci_case_receipts_selftest.py` | 0 | clean |
| `make_cases_selftest` | `python3 scripts/ci_make_cases_selftest.py` | 0 | clean |
| `maap_cases_selftest` | `python3 scripts/ci_maap_cases_selftest.py` | 0 | clean |
| `capture_cases_selftest` | `python3 scripts/ci_capture_cases_selftest.py` | 0 | clean |
| `suite_pieces_selftest` | `python3 scripts/ci_suite_pieces_selftest.py` | 0 | clean |
| `suite_collect_selftest` | `python3 scripts/ci_suite_collect_selftest.py` | 0 | clean |
| `fail_fast_selftest` | `python3 scripts/ci_fail_fast_selftest.py` | 0 | clean |
| `install_cache_selftest` | `python3 scripts/ci_install_cache_selftest.py` | 0 | clean |
| `workflow_plan_selftest` | `python3 scripts/ci_workflow_plan_selftest.py` | 0 | clean |
| `manifest_selftest` | `python3 scripts/ci_manifest_selftest.py` | 0 | clean |
| `evidence_pins` | `python3 scripts/generate_ci_evidence_pins.py --check` | 0 | clean |
| `ci_events` | `python3 scripts/ci_events.py --check` | 0 | clean |
| `ci_events_selftest` | `python3 scripts/ci_events.py --selftest` | 0 | clean |
| `git_diff_check` | `git diff --check e76a755afc0536453161e3cd33f6f4d2dcd7641f HEAD` | 0 | clean |
| `bdd_conformance` | `cd tests && behave` | 0 | clean |
| `hdl_reference_selftest` | `python3 scripts/gen_hdl_reference.py --selftest` | 0 | clean |
| `hdl_reference` | `python3 scripts/gen_hdl_reference.py --output <scratch>/tmp/milan-hdl-reference` | 0 | clean |
| `builder_require_rv32` | `python3 sw/builder/test_builder.py --require-rv32` | 0 | clean |
| `fw_tally_selftest` | `python3 sw/firmware/gtest/tally_selftest.py` | 0 | clean |
| `fw_rv32_selftest` | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | clean |
| `fw_ctrl_selftest_shard0` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 8 --shard 0/4` | 0 | clean |
| `fw_ctrl_selftest_shard1` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 8 --shard 1/4` | 0 | clean |
| `fw_ctrl_selftest_shard2` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 8 --shard 2/4` | 0 | clean |
| `fw_ctrl_selftest_shard3` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 8 --shard 3/4` | 0 | clean |
| `fw_ctrl_nvm` | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 8` | 0 | clean |
| `fw_coverage_selftest` | `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | clean |
| `fw_coverage_check` | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8` | 0 | clean |
| `fw_boundary_only_verilator` | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator` | 0 | clean |

107 gates, every one rc 0, the tree clean after each.

**The full Verilator sweep.** It ran because a shared file (`ctrl_configs.py`) changed, at `e0e1b464`, as `scripts/run_all_suites.sh --shard k/4` in four shard units with the pinned Verilator 5.050 (`receipts/sweep/`, spec `receipts/sweep-spec.json`):

| Shard | Suites passed | Checks | In-suite failures | rc | Seconds |
|---|---:|---:|---:|---:|---:|
| 0/4 | 15 of 15 | 250,913 | 0 | 0 | 4424 |
| 1/4 | 17 of 17 | 1,536,446 | 0 | 0 | 3855 |
| 2/4 | 16 of 16 | 380,086 | 0 | 0 | 5057 |
| 3/4 | 16 of 16 | 23,086 | 0 | 0 | 3531 |

64 of 64 suites passed, with 2,190,531 checks and no failure or timeout. `tsn_fuzz` skips its two field campaigns and their freshness checks, because `tsn-gen` is absent on this host ("set TSN_GEN_ROOT to enable").

Not run, with the reason:

- `act_ci.py --selftest`: AGENTS.md lets a candidate's copy run it only inside the disposable CI job, and this lane does not change it.
- `ci_rv32_sdk.py --destination ...` installs the SDK, which is already at its pinned path. `ci_rv32_sdk_selftest.py` passed.
- rtl-fast's RTL jobs (`verilator-lint`, `yosys-elaboration`, `publication-census`) and the ready-only `yosys-portability`: this round changes no RTL. They stay hosted evidence. `bdd-conformance` is `behave`, above.

## 6. No image or figure change

- `ctrl_configs.py` is imported only by `ctrl_boundary.py`, `ctrl_runs.py` and `ctrl_plants.py`. Other files name it in prose only. No image builder reads it.
- `scripts/image_identity.py` rebuilt every harness image at the head through `build.firmware` alone: the runtime, then the linked split image, unchanged.
  - It ran in a scratch `--shared` clone at `e0e1b464`, with `third_party/tsn-c-stack`, `third_party/lwSRP`, `protocol-processor` and `gptp-processor` initialised from the lane's own submodules.
  - Each ELF's sha256 was compared with the `build:image/ctrl_app.elf` digest in round 2's `build.json`, as R703-2's packet keeps it. All nine match (`receipts/image_identity.txt`):
    - A1 and C-asbuilt: `d4c28047…`;
    - A8: `c89a1871…`;
    - B1: `f561a45f…`; B8: `741d33e3…`;
    - S1: `ef7809fe…`; S8: `5d54d5e4…`;
    - C-slow: `367e7f7f…`; C-shutdown: `3818d15f…`.
- **Disclosed side effect.** `build.py`'s `tree:firmware` digest covers every file of `sw/firmware/ctrl`, and `ctrl_configs.py` is one (`build.py:352-353`).
  - The digest moves from `0dd3f074…`, the value round 2's `build.json` recorded, to `0c55de38…`. `ctrl_configs.py` is the only changed file under those trees (`receipts/tree_firmware_digest.txt`).
  - So `build.reused` refuses a pre-round-6 build as stale, and a regrade needs a rebuild.
  - Round 2's build directories are no longer on the host anyway; only their `build.json` receipts remain.
  - The reviewers' and the PR body's validation commands build afresh, so they are unaffected. The rebuilt images are those above.

## 7. Run history

- The first commit, `1620f8c1`, carried a wrong reason: "no hosted job installs ... the test SoC's packages". `firmware-boundary` does install the LiteX pins.
  - The boundary gate had passed at `1620f8c1` (rc 0, 16:45).
  - The gate runner was stopped between gates, after `solution_docs`: the parent was killed, no child was running, and the tree was verified clean.
  - The wording was corrected and the commit amended. Nothing was pushed, so no public object names `1620f8c1`.
  - Every gate was then rerun from the start at `e0e1b464`. The stopped run's logs stay in scratch and are not cited.
- The sweep could not get four free 16-CPU blocks (`cpu_ranges.py pick` found only `112-127`). It ran as four shard units of 4 CPUs each inside that one free block, so no two jobs shared a core, each unit with MemoryMax 10G and `-j4`, beside the gate runner with MemAvailable above 50 GB.
- Scratch, environments and build trees stay outside the packet. Host paths in receipts are replaced by `<path>` or `~`.

## 8. Acceptance

| Item (round 6) | Status | Evidence |
|---|---|---|
| 1. Register `build.py` the way the gate's rules intend, pick by what it does, say why, do not weaken the gate | met, with a published departure. All six refused files are classified, `build.py` in OUTSIDE, because BUILDERS needs a CI change outside scope and PART_OF is false. No gate code changed, and each entry is load-bearing. | sections 2 to 4; TAKEN |
| 2. The gate exactly as the workflow runs it, at the new head, rc 0; then rtl-fast's other firmware jobs, the harness self-test and mutants, the bare-metal gate, the docs gates and behave | met: both boundary runs `ctrl_boundary: PASS`, rc 0; every firmware job step rc 0; the harness self-test (87 checks, 62 mutants caught); the bare-metal gate (0 findings); the docs-check set; behave 406/406; and the full sweep, 64/64 | section 5 |
| 3. The gate in the standing gate table | met: `fw_boundary_without_verilator` and `fw_boundary_only_verilator` are in `scripts/gates_r6.py` | section 5 |
| No measurement change; STOP if an image or published figure changes | met: nine images byte-identical; no figure regraded or re-measured | section 6 |
| Rows within T_svc | **not met**: the measurement STOP, unchanged | README Findings |

So the PR body says "Relates to #665".

## 9. Open items, risks and questions

- **For the manager: BUILDERS against OUTSIDE for `build.py`.** If the harness's build should run under the hosted capture, a workflow would have to install the picolibc and compiler-rt data packages and the patched LiteX tree beside Verilator. `build.py` would also need a build-only mode. That is a CI change and a new Issue, not this lane.
- **For S2b and S2c:** a re-measure at or after this head rebuilds, because the firmware tree digest moved (section 6). The images are unchanged, so the figures should repeat to the cycle.
- Carried from round 5: the ACMP owed-capacity drop, the SRP starvation and the per-recipient fan-out cost (Issues or S2b scope); R-4 / R704-3-R1 not applied (`docs/testing/TESTING.md`); R703-4 S1 to S3 optional, not applied.
- The act runner's `--selftest` was not run on the host, because AGENTS.md lets a candidate's copy run it only inside the disposable CI job.
- Physical calibration NOT RUN; nothing here is hardware evidence.
