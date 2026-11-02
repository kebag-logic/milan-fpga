| Job | Step | Command | rc | Last line |
|---|---|---|---:|---|
| wire-accountability | Advertised-vs-emitted gate | `check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| docs-check-no-git | Strip git metadata, then run the docs gate | `docs_check.py`, `check_feature_status.py` on `git archive HEAD`, no .git | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | gate_1 HDL reference | `gen_hdl_reference.py --selftest`; `--output` | 0 | Wrote: $VALIDATION_STORAGE/640-a720o/gates/runner_temp/milan-hdl-reference/index.html |
| docs-gates-0 | gate_7 link health | `docs_check.py` | 0 | docs_check: 0 finding(s) across 213 md files + 1436 scrubbed text files, scrub self-test 23/23, routing arms 4/4 [git ls-files] |
| docs-gates-0 | gate_8 em dash | `check_em_dash.py --base 503bc97c` | 0 | check_em_dash: 0 finding(s) over 231 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [503bc97c..HEAD] |
| docs-gates-0 | gate_9 concise docs | `check_doc_style.py` (+ `--selftest`), `check_gptp_docs.py` (+ `--selftest`) | 0 | gPTP documentation selftest: OK (30 controls) |
| docs-gates-0 | gate_10 diagram no-drift | `DOC_MAP.gen.py`, `timesync_chain.gen.py` `--check`/`--selftest` | 0 | time-sync diagram selftest: OK (source, status, XML, raster) |
| docs-gates-0 | gate_11 solution docs | `check_solution_docs.py` (+ `--selftest`) | 0 | solution documentation selftest: OK (45 mutation controls) |
| docs-gates-0 | gate_12 submodule docs | `submodule_boundaries.gen.py`, `check_submodule_docs.py` | 0 | submodule documentation selftest: OK (table and diagram controls) |
| docs-gates-0 | gate_13 WaveDrom | `gen_wavedrom.py --selftest` and three `--check` | 0 | WaveDrom current: docs/diagrams/wd_gptp_pdelay.json |
| docs-gates-0 | gate_14 PNGs | `check_diagram_pngs.py` (+ `--selftest`) | 0 | diagram PNG selftest: OK (6 rasters, 28 mutation controls) |
| docs-gates-0 | gate_15 feature status | `check_feature_status.py --self-test` | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | gate_16 traceability | `gen_module_matrix.py --check` | 0 | traceability matrix up to date (80 modules, 0 untested <= ratchet 0, 0 archived) |
| docs-gates-0 | gate_18 imported gPTP docs | `check_gptp_docs.py --with-submodule`; `make -C gptp-processor docs` | 0 | source evidence selftest: PASS (7 arms) |
| docs-gates-0 | gate_19 measurement self-tests | `measure_control_flow.py`, `measure_cohesion.py` `--selftest` | 0 | 18 checks: 18 PASS, 0 FAIL |
| docs-gates-0 | gate_21 bare-metal scope | `check_baremetal_only.py --check`/`--selftest` | 0 | baremetal-only selftest: PASS (867 arm(s)) |
| docs-gates-0 | ci_step_28 RV32 SDK | `ci_rv32_sdk_selftest.py`; `ci_rv32_sdk.py --destination $HOME/br-milan-rv32/host` | 0 | SDK fresh installation: verified |
| docs-gates-0 | gate_24 compiler-absent controls | `test_firmware_compiler.py --selftest`; `--absent --audit` | 0 | GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations |
| docs-gates-0 | gate_26 NVM record space | `check_nvm_record_space.py` (+ `--self-test`) | 0 | 0 finding(s) across 5 config(s): the inventory's (group, index) key set is exactly the set the shape requires with no key claimed twice, every persisted record has a unique id inside record_id[7:0], every group is inside its block, every payload fits MAX_PAYLOAD_P, every image fits one erase block, the allocation is the donor's own F07.8 rule and its floor fits the namespace at every shipped shape, the worst-case commit fits T-NVM-COMMIT-TIMEOUT with 2x margin, every record round trips through a KLJ2 image, an empty user name survives it, and a CRC-clean image missing any mandatory record is refused with zero records applied |
| docs-gates-0 | gate_27 capture census | `check_nvm_capture.py` | 0 | PASS: capture census, clocks, both timing arms and receipt agree |
| docs-gates-0 | gate_28 saved-state writer | `test_nvm_firmware.py --self-test` | 0 | saved-state writer gate: OK across 5 shape(s), and every planted defect reddened |
| docs-gates-0 | gate_29 SoC sources | `check_soc_sources.py` (+ `--selftest`), `iob_pack_selftest.py` | 0 | iob_pack_selftest: 22 arms, 21 mutants, 0 failure(s) |
| docs-gates-0 | gate_30 RTL source lists | `check_rtl_source_lists.py` (+ `--selftest`) | 0 | 50 checks: 50 PASS, 0 FAIL |
| docs-gates-0 | gate_31 naming | `measure_naming.py --check`/`--selftest` | 0 | 66 checks: 66 PASS, 0 FAIL |
| docs-gates-0 | gate_32 port contracts | `check_port_contracts.py` (+ `--selftest`) | 0 | 82 checks: 82 PASS, 0 FAIL |
| docs-gates-0 | gate_33 fail-fast | `measure_fail_fast.py --check`/`--selftest` | 0 | 106 checks: 106 PASS, 0 FAIL |
| docs-gates-0 | gate_34 TODO ownership | `check_todo_ownership.py` (+ `--selftest`) | 0 | 45 checks: 45 PASS, 0 FAIL |
| docs-gates-0 | gate_35 test evidence | `measure_test_evidence.py --check`/`--selftest` | 0 | 105 checks: 105 PASS, 0 FAIL |
| docs-gates-0 | gate_36 hygiene | `check_hygiene.py --check`/`--selftest` | 0 | 35 checks: 35 PASS, 0 FAIL |
| docs-gates-0 | gate_37 SV idiom | `check_sv_idiom.py` (+ `--selftest`) | 0 | 55 checks: 55 PASS, 0 FAIL |
| docs-gates-0 | gate_38 C++ idiom | `check_cpp_idiom.py` (+ `--selftest`) | 0 | 75 checks: 75 PASS, 0 FAIL |
| docs-gates-0 | gate_39 Python idiom | `check_py_idiom.py` (+ `--selftest`) | 0 | 54 checks: 54 PASS, 0 FAIL |
| docs-gates-0 | gate_40 shell idiom | `check_sh_idiom.py` (+ `--selftest`) | 0 | 48 checks: 48 PASS, 0 FAIL |
| docs-gates-0 | gate_43 cited paths | `check_doc_paths.py` | 0 | doc path gate: OK (1084 cited paths all resolve, 2 allowlisted; 10 line anchor(s) within their file) |
| docs-gates-0 | gate_44 archive | `check_archive.py` (+ `--selftest`) | 0 | archive selftest: OK (24 controls) |
| docs-gates-0 | gate_45 contents | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | TOC gate: OK (152 page(s) carry an annotated contents list, 18 below the 3-section threshold) |
| docs-gates-0 | gate_46 AEM store | `gen_aem_store.py --self-test` | 0 | gen_aem_store self-test: PASS |
| docs-gates-0 | gate_47 sweep shape | `check_sweep_shape.py --self-test` | 0 |   [self-test] OK: 1 drift(s) reported |
| docs-gates-0 | gate_48 deploy shape | `check_deploy_shape.py --self-test` | 0 |   [selftest] OK: 1 drift(s) reported |
| docs-gates-0 | gate_49 entity shape | `check_entity_shape.py --self-test` | 0 | RESULT: PASS |
| docs-gates-0 | gate_50 CI controls | `ci_gate_workflows.py --check` and the thirteen self-tests | 0 | manifest comparison controls: PASS |
| docs-gates-1 | gate_25_0 builder leg 0 | `ci_builder_legs.py run 0 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS |
| docs-gates-2 | gate_25_1 builder leg 1 | `ci_builder_legs.py run 1 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 16 NOT RUN |
| docs-gates-2 | gate_41 CI events | `ci_events.py --check`/`--selftest` | 0 | selftest: PASS (2199 contract items, 5258 arms) |
| docs-gates-2 | gate_42 act runner contract | `act_ci.py --selftest`; installed copy `--selftest --worktree` | 0 | selftest: PASS |
| (lane) | Markdown gates, pinned venv | `docs_check.py` | 0 | docs_check: 0 finding(s) across 213 md files + 1436 scrubbed text files, scrub self-test 23/23, routing arms 4/4 [git ls-files] |
| (lane) | Markdown gates, pinned venv | `check_em_dash.py --base 503bc97c` | 0 | check_em_dash: 0 finding(s) over 231 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [503bc97c..HEAD] |
| (lane) | Markdown gates, pinned venv | `check_doc_style.py` | 0 | documentation style: OK (23 current documents) |
| (lane) | Markdown gates, pinned venv | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | TOC gate: OK (152 page(s) carry an annotated contents list, 18 below the 3-section threshold) |
| (lane) | whitespace | `git diff --check 503bc97c HEAD` | 0 |  |
| (lane) | style on changed blocks | check_doc_style's `analyze()` on every changed block of the 4 pages against 503bc97c, and of this round's page against 545ac9cb | 0 | docs/design/MARK_II_AREA_PLAN.md: 0 finding(s) in changed blocks |
| (reader) | AREA_BUDGET.md's gate reader (rtl-fast) | `syn/ooc/pp_resource_gate.py check-baseline` | 0 | baseline PASS: 3 endpoints |
| (reader) | MAILBOX_SPLIT.md's gate reader (rtl-fast firmware-unit) | `ctrl_service_bounds.arm_service_bounds` via `service_bounds_arm.py` | 0 | rc 0 |
| (lane) | census coverage | `census_coverage.py` over the basis hierarchy, CSR map and placed rows, and the split-only parts | 0 | RESULT: PASS |
| (lane) | census coverage control | `! census_coverage.py` against the round 1 page (3f8ed303): rc 0 means the check failed there, as it must | 0 | RESULT: FAIL |
