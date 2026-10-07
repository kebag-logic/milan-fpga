[A558]

# F2 MAAP handoff

Status: REVIEW READY; round 2 implementation and authorized local validation complete.
Head: `938497af1dffd8a87edebf3ab93663914bf85e5e`.
Starting head: `1a5d70faba6a9b01aab6bb868c12e4c7023e0c70`.
Branch: `665-f2-maap`; stacked on FC at `db9aa8c9b135b34ff3d070a979dee70440b37cc6`.
Relates to #665. Assignment: #665 comment 6029239721.
Executor: [A558]. Internal reviewer: [R528]. External reviewer: [R529].

## Round 2

The round answers R529-1-F1/F2 and R528-1-F1 through F6, plus S1.
The reviewer probes are credited in the standing tests and mutation catalog.
Both earlier reviews are NEGATIVE; this packet requests corrected-head review.
The executor does not publish a clean-lens ledger or a review verdict.

Two one-line commits follow the starting head, without amend or rebase:
`11e195bea` fixes behavior and adds regression controls;
`938497af1` separates the new C++ declarations to meet the idiom gate.
No RTL, register map, submodule pin, default build or shipping-image input changed.

### Authority and acceptance

IEEE 1722-2016 Annex B: B.2 PDUs; B.3.2/Table B.7 (including note a);
B.3.3/Table B.8; B.3.4.1/.2 timing; B.3.5 events; B.3.6 actions;
B.3.6.4 reversed-octet priority; B.4 address pool.
`docs/reference/FR_NFR.md`: NFR-SCOUT-02/03/08 and section 3.4 H-MAAP.
`docs/design/MAILBOX_SPLIT.md`, the FC mailbox contract, and #678's no-callback rule.
The parent is a comparison subject; Annex B remains the protocol authority.
#686 comment 6029233665 now records the parent count and delayed first probe.

| Assignment item | Result and evidence |
|---|---|
| 1, receive wake | MAAP RX IRQ enabled with ADP and event bits; actual loop wait/wake tested at one and two interfaces; missing-bit control caught in both |
| 2, differential | Timer-port deadlines and parent frame completion cycles measured; strict core interval boundaries, parent 500..627 ms and 3 delayed versus 4 immediate-start probes checked; all previous cases retained |
| 3, saved Begin range | Accepted down-link preference retained until first reservation; invalid Begin cannot overwrite it; conflict and later unpreferred Begin draw again |
| 4, restart/priority | Fixed-seed restart changes base; all six deciding octets tested in both comparison directions, including tied suffixes |
| 5, CSR direction/order | Listener DMAC writes are read-only in the model; every destination word precedes either admission enable |
| 6, interface 1 drain | Deferred interface-1 DEFEND drains after a 5 ms ring stall within the original 10 ms budget |
| 7, integration dependency | README and PR body state the ALLOC_DA/talker_active dependency and #664 decision 3 obligation |
| 8, optional controls | Four generic predicate defects added; RV32 release-only object-build limit stated |
| 9, dev merge | #683 and #685 are OPEN at final handoff; manager merge round applies under item 9 |

### Changes at this head

| File:line | Change |
|---|---|
| `sw/firmware/ctrl/app/ctrl_app.c:55` | Configure MAAP RX, ADP RX and event interrupts before opening the composed filter |
| `sw/firmware/ctrl/maap/maap.c:102` | Consume the saved preference exactly once during reservation |
| `sw/firmware/ctrl/maap/maap.c:185` | Retain an accepted Begin preference while down |
| `sw/firmware/ctrl/maap/maap.c:230` | Use that preference on the next operational port; preserve fresh conflict Restart draws |
| `sw/firmware/ctrl/maap/maap.h:49` | Static preference field and API lifetime contract at line 77 |
| `sw/firmware/ctrl/maap/README.md:29` | Saved-range contract, receive IRQ at line 81, allocation dependency at line 101, target build limit at line 144, complete #686 list at line 166 |
| `sw/firmware/ctrl/test/test_maap.cpp:179` | Six-octet priority and fixed-seed restart tests (line 195) |
| `sw/firmware/ctrl/test/test_maap.cpp:311` | Begin-before-link regression and one-use preference checks |
| `sw/firmware/ctrl/test/test_maap.cpp:368` | Direction-aware CSR model and complete destination-before-enable ordering test (line 423) |
| `sw/firmware/ctrl/test/test_maap_mbx.cpp:273` | Composition through actual loop wait/wake, repeated at one/two interfaces |
| `sw/firmware/ctrl/test/test_maap_mbx.cpp:324` | Interface-1 deferred output and original-budget measurement |
| `sw/firmware/ctrl/test/test_maap_differential.cpp:39` | Software timer deadlines and frame timestamps; parent cycle timestamps at line 67; cadence/count/boundary case at line 133 |
| `sw/firmware/ctrl/test/maap_differential.py:31` | Build each copied differential source, so expectation defects are executable controls; timing/count controls at line 55 |
| `sw/firmware/ctrl/test/maap_mutants.py:31` | Eight accepted review defects; four generic predicate defects at line 63 |
| `sw/firmware/gtest/coverage.ratchet:7` | Generator-raised application/core coverage totals; exclusions unchanged |

### Tests and planted defects

Current F2 cases: 36 core/CSR, 12 mailbox at one interface, 13 at two,
one debug assertion case and 12 differential cases: 74 executions.
The prior 66-case evidence is retained under Round 1 below.
Every new defect must fail its named check after successful compilation.
A build refusal is never credited as a caught defect.

| Test / source | Planted defect and the property it catches |
|---|---|
| `MaapHost.AppWaitWakesForMaapWithinBudget`, `test_maap_mbx.cpp:273` | `maap-app-missing-rx-interrupt`: accepted frame cannot wake an idle loop; one-interface campaign plus explicit two-interface control |
| `MaapCore.BeginBeforePortOperationalRetainsRange`, `test_maap.cpp:311` | `maap-begin-down-forgets-range`: accepted saved range discarded before PortOperational! |
| `MaapCore.RestartDrawsNewRange`, `test_maap.cpp:195` | `maap-restart-reuses-range`: conflict re-probes the lost range with the fixed seed |
| `MaapCore.PriorityAfterTiedOctets`, `test_maap.cpp:179` | `maap-reverse-five-octets`, `maap-compare-mac-lsb-only`: earlier deciding octets ignored |
| `MaapCsr.EveryStreamAddressAndLossGate`, `test_maap.cpp:390` | `maap-csr-select-listener`: talker window writes accidentally target read-only listener destinations |
| `MaapCsr.AdmissionAfterEveryDestinationWrite`, `test_maap.cpp:423` | `maap-csr-enable-before-programming`: admission opens before all 18 destination words are written |
| `MaapHost.InterfaceOneStallDrainsWithinBudget`, `test_maap_mbx.cpp:324` | `maap-poll-first-interface-only`: interface 1's queued DEFEND never drains |
| `AllStates/MaapCell.TableB7/0`, `test_maap.cpp:140` | `maap-generic-initial-handles-conflict`: INITIAL incorrectly handles a conflict |
| `AllStates/MaapCell.TableB7/12`, `test_maap.cpp:140` | `maap-generic-probe-state-defends`: DEFEND action uses the wrong state predicate |
| `AllStates/MaapCell.TableB7/10`, `test_maap.cpp:140` | `maap-generic-probe-defend-uses-priority`: a DEFEND during probing incorrectly depends on priority |
| `MaapCore.ReverseOctetPriority`, `test_maap.cpp:170` | `maap-generic-equal-mac-wins`: equality incorrectly grants priority |
| `MaapDifferential.ProbeTimingAndParentDelta`, `test_maap_differential.cpp:133` | `probe-1ms`, `probe-500ms`, `probe-600ms`: actual timer-driven sends violate strict B.3.4.2 bounds |
| Same differential case | `parent-probe-bound`, `parent-probe-count`: falsified parent cadence/count expectations fail |

Observed software draws reach 511 and 589 ms. The parent reaches 500 and 627 ms
under 1,024 start phases; equal-length consecutive frame completions cancel
serialization error. The initial parent observation allows at most 1 ms of
tick/serialization uncertainty. Four core PROBEs start immediately; the parent
sends three delayed PROBEs. All six named #686 differences remain explicit.

H-MAAP wake response: 4,700 ns from RX_HEAD publication in each interface case.
Interface-1 stalled response: 5,004,400 ns, including the 5 ms stall.
These are host measurements assuming 100 ns per ordered mailbox transaction.
The standing callback bound is 48 accesses; standalone pass bounds are 616/664
at one/two interfaces. They do not prove target CPU time, bus arbitration,
wire departure, NVM interference, media quiescence or physical timing.

### Coverage table

Regenerated only through `fw_coverage.py --write`; checked with `--check --jobs 4`.
All 17 files remain at 100% measured line/branch coverage after the existing
documented exclusions. No exclusions were added. The three new MAAP C files
have no exclusions. RV32 validation covers `-DNDEBUG` freestanding objects;
the host debug assertion does not establish target debug linkage or an image.

| File | Lines | Branches |
|---|---|---|
| `sw/firmware/ctrl/adp/adp.c` | 168/168 | 73/73 |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/38 |
| `sw/firmware/ctrl/app/ctrl_app.c` | 31/31 | 20/20 |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 95/95 | 56/56 |
| `sw/firmware/ctrl/maap/maap.c` | 209/209 | 140/140 |
| `sw/firmware/ctrl/maap/maap_csr.c` | 39/39 | 18/18 |
| `sw/firmware/ctrl/maap/maap_mbx.c` | 98/98 | 60/60 |
| `sw/firmware/ctrl/mbx/mbx.c` | 173/173 | 62/62 |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 |
| `sw/firmware/ctrl/wire/wire.h` | 10/10 | 2/2 |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 195/195 | 104/104 |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/259 |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/63 |

### Gate table

All final gate command exits are zero. The 93-entry builder/documentation bank
retains the explicit vendor-analysis and historical-calibration limits below.
The controller campaign covers the exact 192-entry catalog in four disjoint
partitions; the driver requires each declared named failure. The separate
two-interface wake control passes too. Differential controls are 16/16.

The final controller campaigns, coverage check and differential ran after commit
`938497af1`. Earlier mailbox and unaffected bank evidence ran at `11e195bea`;
the only later source changes split declarations in two MAAP test files, neither
of which the mailbox suite or those bank functions consume. The changed idiom
gate was rerun at the final head. Builder source hash:
`3fdadcc6c1b2560652cbae3054eb34fd810989162ec76d0f3641ce8c67e74a81`.

#### Firmware and mailbox gates

| Receipt | Command | Exit | Seconds | Result |
|---|---|---|---|---|
| `campaign-final0.log` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard 0 4 --build-dir $CHECK_ROOT/campaign-final0` | 0 | 477.24 | 48/48 controller defects; all positive arms and required RV32 build |
| `campaign-final1.log` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard 1 4 --build-dir $CHECK_ROOT/campaign-final1` | 0 | 483.09 | 48/48 controller defects; all positive arms and required RV32 build |
| `campaign-final2.log` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard 2 4 --build-dir $CHECK_ROOT/campaign-final2` | 0 | 420.29 | 48/48 controller defects; all positive arms and required RV32 build |
| `campaign-final3.log` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard 3 4 --build-dir $CHECK_ROOT/campaign-final3` | 0 | 397.74 | 48/48 controller defects; all positive arms and required RV32 build |
| `differential-head.log` | `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep $CHECK_ROOT/differential-head` | 0 | 162.93 | 12 positive cases; 16/16 named differential controls |
| `irq-if2-control.log` | `python3 $CHECK_ROOT/irq_if2.py` | 0 | 5.82 | Missing-interrupt defect caught by the named two-interface wake test |
| `coverage-write-fixed.log` | `python3 sw/firmware/gtest/fw_coverage.py --write --jobs 4 --keep $CHECK_ROOT/coverage` | 0 | 140.18 | Ratchet regenerated by its generator |
| `coverage-head.log` | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --keep $CHECK_ROOT/coverage-head` | 0 | 142.14 | 17 files at 100% after existing exclusions; no new exclusions |
| `tally.log` | `python3 sw/firmware/gtest/tally_selftest.py --mutants` | 0 | 62.19 | 18 tally cases and 18 listener mutations |
| `coverage-selftest.log` | `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | 0.52 | 28 coverage controls |
| `firmware-nvm.log` | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 99.81 | 434 tests across five shapes; required RV32 objects |
| `mbx.log` | `make -C $CHECK_ROOT/export/tb/verilator/mbx -j1 VBUILD_JOBS=8` | 0 | 47.49 | WB 316; AXI-Lite 361; cosim 13; IF2 316/361/316; quick controls 5/5 |

RV32 controller object totals: text 14,884 B, data 0 B, BSS 167 B (12 objects).
Undefined symbols: libgcc integer helpers and memcpy/memset/vsnprintf only.
These are object totals, not a linked-image size or a whole-program memory bound.

#### Full builder/static and documentation bank

Commands below are the repository entry points. B48 and D24 ran as bounded
partitions preserving all original functions, fixture values and assertions.
Each foreground invocation remained under ten minutes. No command was piped.
CHECK_ROOT is disk-backed scratch; CANDIDATE_ROOT is the implementation checkout.
SDK_DIR is the verified pinned SDK; the controller pre-#679 RV32 arm instead
selects the installed bare-metal compiler via CTRL_RV32_CC. The HDL parser is
loaded from the pinned requirements through PYTHONPATH. The simulator is 5.050,
with VERILATOR_JOBS=2 and make -j8; campaign workers are limited to four.

| ID | Command | Exit | Seconds | Result |
|---|---|---|---|---|
| B01 | `python3 avdecc/gen_aem_store.py --self-test` | 0 | 0.11 | PASS |
| B02 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.36 | PASS |
| B03 | `python3 scripts/lint_rtl.py --check --self-test` | 0 | 10.5 | PASS |
| B04 | `python3 scripts/suite_shards.py --selftest` | 0 | 0.06 | PASS |
| B05 | `python3 scripts/ci_events.py --check` | 0 | 0.26 | PASS |
| B06 | `python3 scripts/ci_scope.py --selftest` | 0 | 5.73 | PASS |
| B07 | `python3 scripts/ci_events.py --selftest` | 0 | 19.99 | PASS |
| B08 | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | 1.42 | PASS |
| B09 | `python3 scripts/check_feature_status.py` | 0 | 1.07 | PASS |
| B10 | `python3 scripts/check_submodule_docs.py` | 0 | 0.51 | PASS |
| B11 | `python3 scripts/check_cpp_idiom.py` | 0 | 1.72 | PASS |
| B12 | `python3 scripts/check_py_idiom.py` | 0 | 4.52 | PASS |
| B13 | `python3 scripts/docs_check.py` | 0 | 5.73 | PASS |
| B14 | `python3 scripts/check_doc_style.py` | 0 | 0.06 | PASS |
| B15 | `python3 scripts/check_doc_style.py --selftest` | 0 | 0.06 | PASS |
| B16 | `python3 scripts/check_solution_docs.py` | 0 | 0.11 | PASS |
| B17 | `python3 scripts/check_doc_paths.py` | 0 | 0.11 | PASS |
| B18 | `python3 scripts/check_archive.py` | 0 | 0.42 | PASS |
| B19 | `python3 scripts/gen_toc.py --verify-anchors` | 0 | 2.98 | PASS |
| B20 | `python3 scripts/gen_toc.py --check` | 0 | 4.98 | PASS |
| B21 | `python3 scripts/check_hygiene.py --check` | 0 | 0.46 | PASS |
| B22 | `python3 scripts/check_todo_ownership.py` | 0 | 1.82 | PASS |
| B23 | `python3 scripts/check_sv_idiom.py` | 0 | 0.52 | PASS |
| B24 | `python3 scripts/check_sh_idiom.py` | 0 | 0.27 | PASS |
| B25 | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.69 | PASS |
| B26 | `python3 scripts/check_soc_sources.py` | 0 | 0.16 | PASS |
| B27 | `python3 scripts/check_port_contracts.py` | 0 | 2.77 | PASS |
| B28 | `python3 scripts/check_nvm_record_space.py` | 0 | 2.47 | PASS |
| B29 | `python3 scripts/check_baremetal_only.py --check` | 0 | 19.22 | PASS |
| B30 | `python3 scripts/check_baremetal_only.py --selftest` | 0 | 7.61 | PASS |
| B31 | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 84.03 | PASS |
| B32 | `python3 scripts/check_sweep_shape.py --self-test` | 0 | 16.05 | PASS |
| B33 | `sudo -n docker run --rm --network none --cap-drop ALL --security-opt no-new-privileges --memory 2g --cpus 2 --user $JOB_UID:$JOB_GID --mount type=bind,src=$CANDIDATE_ROOT,dst=/candidate,readonly --mount type=bind,src=$CHECK_ROOT/container-B33,dst=/scratch --workdir /candidate --env TMPDIR=/scratch --env PYTHONDONTWRITEBYTECODE=1 catthehacker/ubuntu:full-latest python3 scripts/xvlog_gate.py --check` | 0 | 0.77 | SKIPPED: vendor analyzer absent; no analysis pass claimed |
| B34 | `python3 scripts/measure_control_flow.py --selftest` | 0 | 0.16 | PASS |
| B35 | `python3 scripts/measure_cohesion.py --selftest` | 0 | 0.11 | PASS |
| B36 | `python3 scripts/check_em_dash.py --base db9aa8c9b135b34ff3d070a979dee70440b37cc6` | 0 | 3.72 | PASS |
| B37 | `python3 scripts/measure_fail_fast.py --check` | 0 | 1.72 | PASS |
| B38 | `python3 scripts/measure_test_evidence.py --check` | 0 | 6.98 | PASS |
| B39 | `python3 scripts/measure_naming.py --check` | 0 | 0.57 | PASS |
| B40 | `python3 scripts/measure_test_evidence.py --selftest` | 0 | 7.49 | PASS |
| B41 | `python3 scripts/gen_toc.py --selftest` | 0 | 1.03 | PASS |
| B42 | `python3 scripts/check_em_dash.py --selftest` | 0 | 5.83 | PASS |
| B43 | `python3 scripts/docs_check.py --selftest` | 0 | 0.21 | PASS |
| B44 | `git diff --check db9aa8c9b135b34ff3d070a979dee70440b37cc6` | 0 | 0.03 | PASS |
| B45 | `python3 scripts/check_wire_accountability.py --self-test` | 0 | 0.31 | PASS |
| B46 | `python3 scripts/check_entity_shape.py --self-test` | 0 | 61.53 | PASS |
| B47 | `python3 scripts/check_deploy_shape.py --self-test` | 0 | 0.51 | PASS |
| B48 | `python3 sw/builder/test_builder.py --require-rv32` | 0 | 1448.85 | PASS via complete original-function/fixture partitions; historical gate 11 calibration NOT RUN |
| D01 | `python3 scripts/gen_hdl_reference.py --selftest` | 0 | 0.47 | PASS |
| D02 | `python3 scripts/gen_hdl_reference.py --output $CHECK_ROOT/hdl-reference` | 0 | 1.92 | PASS |
| D03 | `python3 scripts/check_gptp_docs.py` | 0 | 0.21 | PASS |
| D04 | `python3 scripts/check_gptp_docs.py --selftest` | 0 | 0.26 | PASS |
| D05 | `python3 docs/DOC_MAP.gen.py --check` | 0 | 0.42 | PASS |
| D06 | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | 0.51 | PASS |
| D07 | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | 0.43 | PASS |
| D08 | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | 0.47 | PASS |
| D09 | `python3 scripts/check_solution_docs.py --selftest` | 0 | 3.05 | PASS |
| D10 | `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | 0.47 | PASS |
| D11 | `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | 0.62 | PASS |
| D12 | `python3 scripts/check_submodule_docs.py --selftest` | 0 | 0.07 | PASS |
| D13 | `python3 scripts/gen_wavedrom.py --selftest` | 0 | 0.17 | PASS |
| D14 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | 0.36 | PASS |
| D15 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | 0.42 | PASS |
| D16 | `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | 0.42 | PASS |
| D17 | `python3 scripts/check_diagram_pngs.py` | 0 | 0.42 | PASS |
| D18 | `python3 scripts/check_diagram_pngs.py --selftest` | 0 | 7.78 | PASS |
| D19 | `python3 scripts/check_feature_status.py --self-test` | 0 | 1.02 | PASS |
| D20 | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | 0.22 | PASS |
| D21 | `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | 1.32 | PASS |
| D22 | `python3 scripts/ci_rv32_sdk.py --destination $SDK_DIR` | 0 | 0.87 | PASS |
| D23 | `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 | 2.27 | PASS |
| D24 | `python3 sw/builder/test_firmware_compiler.py --absent --audit $CHECK_ROOT/rv32-absent.jsonl` | 0 | 621.55 | PASS via complete fixture partitions; no compiler-dependent proof |
| D25 | `python3 scripts/check_nvm_record_space.py --self-test` | 0 | 51.78 | PASS |
| D26 | `python3 scripts/check_nvm_capture.py` | 0 | 1.02 | PASS |
| D27 | `python3 scripts/check_soc_sources.py --selftest` | 0 | 0.27 | PASS |
| D28 | `python3 sw/litex/iob_pack_selftest.py` | 0 | 2.52 | PASS |
| D29 | `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | 3.12 | PASS |
| D30 | `python3 scripts/measure_naming.py --selftest` | 0 | 0.52 | PASS |
| D31 | `python3 scripts/check_port_contracts.py --selftest` | 0 | 3.23 | PASS |
| D32 | `python3 scripts/measure_fail_fast.py --selftest` | 0 | 1.72 | PASS |
| D33 | `python3 scripts/check_todo_ownership.py --selftest` | 0 | 1.87 | PASS |
| D34 | `python3 scripts/check_hygiene.py --selftest` | 0 | 0.41 | PASS |
| D35 | `python3 scripts/check_sv_idiom.py --selftest` | 0 | 0.52 | PASS |
| D36 | `python3 scripts/check_cpp_idiom.py --selftest` | 0 | 1.92 | PASS |
| D37 | `python3 scripts/check_py_idiom.py --selftest` | 0 | 4.33 | PASS |
| D38 | `python3 scripts/check_sh_idiom.py --selftest` | 0 | 0.26 | PASS |
| D39 | `sudo -n docker run --rm --network none --cap-drop ALL --security-opt no-new-privileges --memory 2g --cpus 2 --user $JOB_UID:$JOB_GID --mount type=bind,src=$CANDIDATE_ROOT,dst=/candidate,readonly --mount type=bind,src=$CHECK_ROOT/container-D39,dst=/scratch --workdir /candidate --env TMPDIR=/scratch --env PYTHONDONTWRITEBYTECODE=1 catthehacker/ubuntu:full-latest python3 scripts/act_ci.py --selftest` | 0 | 4.18 | PASS: offline self-test in a disposable container only |
| D40 | `python3 scripts/check_archive.py --selftest` | 0 | 0.06 | PASS |
| E01 | `python3 sw/mailbox/gen_mailbox.py --check --crosscheck` | 0 | 0.16 | PASS |
| E02 | `python3 sw/mailbox/gen_mailbox.py --selftest` | 0 | 0.72 | PASS |
| G01 | `make -C gptp-processor docs` | 0 | 0.82 | PASS |
| N01 | `(from $CHECK_ROOT/builder-export) python3 scripts/docs_check.py` | 0 | shared 6.93 | PASS; inventory parity unavailable without Git; B13 supplies it |
| N02 | `(from $CHECK_ROOT/builder-export) python3 scripts/check_feature_status.py` | 0 | shared 6.93 | PASS |

#### Partition census

The official builder entry point contains 100 functions. The partitions executed
indices 0:12, 13:56, 56:90 and 90:100; index 12 is the long bare-metal profile.
That profile's independent loops were sliced by INDEX::4. The union audit
compares each fixture's hash, proves no omission or overlap and checks the
original source hash. Unpartitioned setup and assertions run in every partition.
The compiler-absent mode proves refusal/degraded behavior only; SDK mode supplies
the actual compiler evidence. The required compiler profile has zero NOT RUN.

| Mode | Loop line in test_builder.py | Fixtures | Executed across four partitions |
|---|---|---|---|
| sdk | 15307 | 4 | 4 |
| sdk | 15349 | 20 | 20 |
| sdk | 15604 | 38 | 38 |
| sdk | 15650 | 4 | 4 |
| sdk | 17021 | 358 | 358 |
| sdk | 17038 | 3 | 3 |
| sdk | 17060 | 43 | 43 |
| absent | 15307 | 4 | 4 |
| absent | 15349 | 20 | 20 |
| absent | 15604 | 35 | 35 |
| absent | 15650 | 4 | 4 |
| absent | 17016 | 17 | 17 |
| absent | 17021 | 256 | 256 |
| absent | 17029 | 3 | 3 |

#### Superseded attempts and final state

Initial attempts exposed a protected-member test-lambda compile error, then a
256-phase parent scan that did not reach the 500 ms endpoint. Both were fixed
before the implementation commit, keeping the strict assertions. The C++ idiom
gate then required splitting new declarations; that is the second commit.
The first parser run lacked its pinned module path. A builder partition needed
the default output layout and Git inventory, so it was rerun in a complete
isolated checkout. Corrected receipts above all return zero; the earlier
nonzero attempts are not counted as passes. Two completed profile runs were
repeated to preserve their separate fixture receipts after a receipt-name collision.

Only the recorded generated coverage ratchet enters the source tree. Incidental
generated files from repository gates are moved into scratch before final
integrity verification. Tracked bytes/modes and index entries are checked against
HEAD for 1,154 root files and 558/104/214 pinned submodule files. The final tree
and ignored-file check are clean. Free space remains above 136 billion bytes,
well above the 30 GB floor. The 5-second samples peaked at 9,093,722,112 B
(8.47 GiB). The cgroup lifetime high-water is 10,414,649,344 B (9.70 GiB),
above the requested 9 GiB working target and below the 12 GiB cap. Sampling
therefore does not prove that memory stayed below the working target throughout.
Final MemoryCurrent is about 2.4 billion bytes. No resource-limit compliance
claim is inferred from the green gates.

#### Evidence size and digest receipts

Logs, toolchains, dependencies, archives and generated trees stay in scratch.
No artifact over 200 KB is copied to the output packet. These hashes identify
the retained evidence; they are not a substitute for independent execution.

| Artifact under CHECK_ROOT | Bytes | SHA-256 |
|---|---|---|
| `B01.log` | 3596 | `9f126bf9dfc7cb552a2414b98d2792449dc4ae126395997750d5039cb896f022` |
| `B02.log` | 955 | `fad5e1b9dd5f465b7fcb2334e2abe6c6db44be93b5bb12afb3a35f3ebf432e1a` |
| `B03.log` | 14888 | `fdfaa1c6d9058fd1f1d30ef75e8590d1e633c21b21ff6fb7455e0542dc99123a` |
| `B04.log` | 1269 | `52039414c215a5a8cf1f3ebe1b830567c059f0a4df09d097926beaa26719316d` |
| `B05.log` | 167 | `617e44ed66b13896b9bf7fa2c76c7242990622e9ced9ba79a693484ad4bd4a77` |
| `B06.log` | 6877 | `cda2e3e13229332d91d0863932d724a7fdeef280c924f262aa43f5d5448c62da` |
| `B07.log` | 150787 | `323df9bf49ae1b88fd84f24ed0dee9120127a78d412f74c2ceec781f980cd55c` |
| `B08.log` | 118 | `d0be3b6428ae2079134f2a21b2972c524a26103b0e9c8b64039bb24ae22797dc` |
| `B09.log` | 29 | `802f5eeb2f0aa147169f3ddb9c64d4369ca92ab380455195403f2e8ae02490d0` |
| `B10.log` | 47 | `dffc750855c2574e23bad0174564fcde9dc0d351b65e2f5e954f2dc64e894835` |
| `B11.log` | 316 | `4442bd5d4073138fd9e71b3c6bafecbd7d17ec2a85c5deaaa72d8ce6eda0c46d` |
| `B12.log` | 461 | `7e309294408092eca3b35094bbe20459b2d06755c6a8a826da21779bcc86b630` |
| `B13.log` | 128 | `962f461c1639dcb0cf9c4a2a46e24ed200529f6b5da33e02d71850bc2ebb1d91` |
| `B14.log` | 47 | `1491d3f6bec03b920cf58f5fb28e6abff4a9d433a758bc0fe5d2db77bf4f53cd` |
| `B15.log` | 33 | `0acc8195c60dd145a8f17d24b7b07c29074ac131d71893f9cef5f880239dd909` |
| `B16.log` | 87 | `48ac84ddbd532247deb21834ee60bd4b7322f69bb9ab9fc5f9901969ccb38c42` |
| `B17.log` | 100 | `f6b4bf0ee623dc3c0e2d45e1b24678a931ceece007f4eeaf3e06fa47af34c3b4` |
| `B18.log` | 93 | `69d45782911c2958be2fef681f849e9b3915293c938de331bb6885dab21fd46c` |
| `B19.log` | 64 | `47c81d0215393f2dcd32e68857b340b140a5dc1808509010aa87038af24f36a6` |
| `B20.log` | 94 | `35e7e86e67b2d3d3968be2ae5107b946549d31bc8426a393fdae86c12f341b47` |
| `B21.log` | 2000 | `83dffcb345691dae55056b6babf94f8cb6d02e5619acc2c54a26e00b043cdb9a` |
| `B22.log` | 161 | `fa01582c02b69a59b174bd6dea0892f022138072e0ab8735e0fe57d8d0039d08` |
| `B23.log` | 218 | `aed2873a1909e4a41b3e6dee6dc5aaab993bbf1ef41f556062a5b377a6a8b167` |
| `B24.log` | 235 | `7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9` |
| `B25.log` | 153 | `ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95` |
| `B26.log` | 85 | `7ea77f321df0437a49feae4436006813f0653a8151945dbf7601fe0e5e289033` |
| `B27.log` | 421 | `3c1a34d3169cf6f071f2cbb62a8ddca7591338e9f45ee665e1c66758f22c5524` |
| `B28.log` | 2578 | `cf53746e34d5ec76dc263f5ce98c17e9f1b227048b67c9e6bdbb8e798007f4f0` |
| `B29.log` | 72 | `56a770ed2f431447ed314974411097eca7fc31d4b7503eaac5f8f58b59e2efd1` |
| `B30.log` | 43 | `09b491b87735efaef68eafe7f45f4fe4ba1f8ad036c0d252d2a93a00906d51f8` |
| `B31.log` | 5189 | `cba18482dbf27c70ee56b28a8fbbe7bfdc2cc49b4644a42daa5ad4db8f6d4972` |
| `B32.log` | 19682 | `869fb51228577e47ba7a40dc4a0ff9734b4efcae8dcb68bf0c875f6d08c8ac8a` |
| `B33.log` | 109 | `2530eb83cff115f67e104fd0440c33b78441363278d88c86ae155a8e7bf9cdb0` |
| `B34.log` | 2565 | `34d85283c432e38af30c33dcc6de6b85208e1ec98a538b78e68061d27421972b` |
| `B35.log` | 728 | `10f526cea8560a3a39135260553e767b316076d7598559fb5f07e8cfab2c5363` |
| `B36.log` | 140 | `c07b307be985628f0f16d26e514616e9b8f6739263cb94fabf7bd1af6432114c` |
| `B37.log` | 6085 | `bbf0264b3cc1beedf3b725b71c379498d33eceeff22f734695af87a77240563e` |
| `B38.log` | 14635 | `4322b73a4b194c5aedc7a75ca57b7e20bbecce56a56032963eb515d2e1892a2a` |
| `B39.log` | 36608 | `1cf945250501b5b0267ea1d21f976938536502d765b18d75110bfb3bffbc4508` |
| `B40.log` | 5659 | `3c818777e9f41c6d64a15fa699cd238a94b030f0ce19981df099f855b97416ba` |
| `B41.log` | 38 | `d7fd5f6ebcdd25e6cf93b623b0fba00cfa32d19c812ce34eb6b8d8b352ac9b32` |
| `B42.log` | 42 | `46aaf33b1a5f1d99dba778a65e86a452bbd5642cde32cf136a7a8e1721f7a19a` |
| `B43.log` | 56 | `83cb6b9c5f7a556a8ea31ad3a751a39e6d573b00fe44ac39f5e1591022048339` |
| `B44.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `B45.log` | 4965 | `bd97b8b53304baf2b912ac2e4ec507e3b8f9ae4c5c2511b5dc69a41d2cbdd3d4` |
| `B46.log` | 25694 | `65d5dc4df5f47df5472223c1e4a59a8b35ce8d135e1a42e9db41f563ec8337b4` |
| `B47.log` | 9270 | `e39530f8b8939af926a16b241021b155c0df83c6cfce904280e2c5d16e60ec73` |
| `D01.log` | 417 | `7ed924696f40b12c7e72b7f3452d9503564e6a0d5ecd81a70f25745ba40443ea` |
| `D02.log` | 410 | `94a9316ea953df1a3f2df4dc992d8fdedcc03594dbb0ddc1d2e8ecb6648c1cd9` |
| `D03.log` | 41 | `d8a77a32600566f0613626fd361bad845759693a08b1095dd54865c1aa25455d` |
| `D04.log` | 46 | `200332e4eddfd8a6338d8a4dbe27d2f513de92f951a1aa1f6b25882182bc290e` |
| `D05.log` | 61 | `74408f0fbcdfc1c7e22f6eccd3eb299da61cabe9bb4526eed416b31a8bf61e16` |
| `D06.log` | 60 | `85ddf25d9a99974b71a9c165cbfbbf390be3d7bf74f081b4cc669622a0a562b9` |
| `D07.log` | 60 | `51058c96a481bf763246394b619601227bdec11b6b11ddcaa1d6f57593d2f1f4` |
| `D08.log` | 61 | `7c7ad79fa685d29607abf71e3a99d98855fd7ffa1ba5fbf7de23bfb41a33c8fa` |
| `D09.log` | 59 | `c57d3ed2e5c9be43085106227b69fe55f866b1198ad209fbb27f940e5757ec30` |
| `D10.log` | 54 | `905777610f39981543faabafcc11309ac6ab670121c8866a45e171e5c9b7d00c` |
| `D11.log` | 60 | `51bca8fb66fd6f0acc480e3364f74fd7a4874946b191468bfbe20ad159cca889` |
| `D12.log` | 66 | `54dbecff3ad17dc651e86c7b313ef57fa96baf89fb40f0fb90af4bbb8ddc802b` |
| `D13.log` | 77 | `8439889f74aa49f8d61f50d6b525f358d0774a4133b54cd9895edad971302d42` |
| `D14.log` | 58 | `b3f8f3a790f92f14932f7c8a8c6b7ad9f33d327b6a6cfe653364d5f34617f8e3` |
| `D15.log` | 54 | `4d9e7670f2a4615d27d64a23c95a4882fd923026e00120f90d44a031c39b61d5` |
| `D16.log` | 52 | `411f08b7121f1a0c6b28105fe433aa4561caad5a8e4caf9e7a6c6aa2fd33cac9` |
| `D17.log` | 66 | `05e0fcfa26a97494e8983dcfca3ad89cdaf91e390acbfb9dbdfb6f614cba4e51` |
| `D18.log` | 59 | `918e8cc85a2a2b0d45eeb3f0c7b006824c81e2ed404a535eded095b09d875dc5` |
| `D19.log` | 1500 | `77f7649b1865c0daf4f3de04dd18c78be4885c9c94a8f03fd1e4f262758c3184` |
| `D20.log` | 66 | `7ca87a8501c54854805f1cf90d49b2a8ff6353a1049fd21cf0631569f5024e41` |
| `D21.log` | 6431 | `ecf6210b750a7f243d63cce2ee20883a5e5a3c364edac32cd43f7e8ee6f1fdf4` |
| `D22.log` | 1557 | `1b6b32eb5c237ff5fb98ba5e8f7a46b5ca9a03694acf1a3466b9200298379eb3` |
| `D23.log` | 138 | `f6da142138888df7ecd9ef31e7b86895260648309005e1400148d78004e385d7` |
| `D25.log` | 7010 | `8e636c8b39e0ce66934ec2a3a7088ef7e6be29b5820a3a87f147d40c612320c6` |
| `D26.log` | 324 | `9a4196c774ce4ddfa9980cf9345d111028f3afa812677fe5bab392f81c955439` |
| `D27.log` | 1501 | `d877c9fa9a5d1db2854c5ed3486ca7d2d135944cf3953143bdf63b554f8c3dc0` |
| `D28.log` | 3147 | `55e08920618778573a58f152092c4605e53735fdaf550c99ed72016963b2ffad` |
| `D29.log` | 3300 | `418b0ce0f1f8a55805a4c0e75385ae0f3c18b83b3af16598f5cfc45b40591f1d` |
| `D30.log` | 4026 | `20635e2ee5994ddc3555ad8acef6af506885fef1ccec25b9c4efb88ab4984c02` |
| `D31.log` | 4619 | `8cbdbe06b994bf0db6efd8d9289a0a237bb965d3a771a9d536aa23e8ae0ae75e` |
| `D32.log` | 6597 | `ef92c9eb4e29bf495c938a2ebe16cb2ec7896671a4e7a63ae465c76f5ca8373a` |
| `D33.log` | 2584 | `696cea82f33dcda09f3d8b1047ee2682f9ca7c6da9348a07813eaf3d3d6f978b` |
| `D34.log` | 1847 | `2c7b5cb25dc4cc0407fc27441f4bba2291c74fa2aa2b22f1276e129651f615a8` |
| `D35.log` | 2955 | `0e4826a9db5e2e72c2d3a62bfef0d017bacb9a51238353b44b469b7dbd1c5f9b` |
| `D36.log` | 3593 | `7fd74c4ebf8b2f0a9812a20518981f63c8350a34c535bcde2c7fa6c58fbec2b9` |
| `D37.log` | 2531 | `d7413b83955948950d15e364a901be97cf05148dad38e97be07b2d63eb46406d` |
| `D38.log` | 2461 | `b9af4f07f8aabdddc7af15799e1e06640c7a0a356ef30681b059784e385d3a57` |
| `D39.log` | 36483 | `876a6eca5975005e4e1d1ddddad9f74d2443039a10df8b7f590e4c781632fdab` |
| `D40.log` | 35 | `83aa5efe967935657a1678bf63262a7c435d29d571cc08dd2ae8cf6f8569d34a` |
| `E01.log` | 26 | `9bb7d3a8faff1627f39a3bb7c9462a0b15ec8dd6c94a44c48d2fc7ac515a982f` |
| `E02.log` | 4567 | `8ef156d44be8e67a3887770fb6a2ad888d5712b9b2a14ca0eb7e51159acbf939` |
| `G01.log` | 2670 | `b8d251402281ad38d34f2afd1019bce15961b876a705e06ce2c67b579c038641` |
| `archive-docs.log` | 225 | `237952aa5a518dff0d39b0413f23b6e734c04bfddad4420247193826d4c6b5f1` |
| `audit_campaign.py` | 1953 | `c493a3c5a4ae012842a0446ff32e519fe5be696d0f56e29dd9764ec28acd9ca0` |
| `builder-functions-a.log` | 10872 | `e2f48a96b000b400093f825b9603d929d524dea3f5f2c8a15f87ccd8cc35591b` |
| `builder-functions-b.log` | 18348 | `6b6e5ca6cf2d5f95ca8f3a37e404e857b43b2468f751e57398a9e318d2cdf556` |
| `builder-functions-c-corrected.log` | 19795 | `75c132c8ce0325ae8dda200ef5c5f3ad84074502f276aaf30e957a368ac054a4` |
| `builder-functions-d.log` | 10795 | `d80cc7ef102a2ffaf1f76c228a030c1fe88b4f39c99ae00803aefced64871483` |
| `builder_shard.py` | 1270 | `c295c7c7f2309cf7cdca9c2c814af22ac49c9a815ab9b92b2bd005293a05a5b9` |
| `campaign-complete.json` | 7772 | `afce095de1d9aadb519878c1eb93a264bfbf558f21205ebedd984986e849304b` |
| `campaign-final0.log` | 13214 | `855a115931fa50c027d2e95671c618b65a389528736b541ad230823a0aa7328c` |
| `campaign-final1.log` | 13306 | `8626d95cf461b6105e02964d9a643b65c47ea470d5b118906e197dd4c488b66d` |
| `campaign-final2.log` | 13606 | `71e72a0375871d72ebb06a511f6148f119cd4303be6a0096791e0cc5046e9682` |
| `campaign-final3.log` | 13067 | `c74228d84cafa0d791375fe59b75a1b7a6a3bb3ea280e2555dfecbeeef39b5ac` |
| `coverage-head.log` | 2966 | `a46efe594155f50d4cd58331c897f2767f190da1ddf5b06ab32ce44d827c740b` |
| `coverage-selftest.log` | 3710 | `3788b02a1c5d91d7ff2c8581f2ed09040261511d92565dd669103fee911dca0b` |
| `coverage-write-fixed.log` | 2987 | `67bd9c59ee5fe418e76f82288e6cdeebc73c45c715fde9a151b60fe37c610766` |
| `dev-status.json` | 272 | `3df36f6ba2f748ade4d859a2b7c90f5166c4f660e1ff900e132eedbdffc8bd70` |
| `differential-head.log` | 13619114 | `0bd0644a15963a0ab1e2f1e6a90282b0096f1b2b6d714b3a20d8af8aa56ec80f` |
| `firmware-nvm.log` | 3549 | `d60a249e5af72d96171e30fab017700d9b58610eb1e70fda3cd606c3114f9513` |
| `integrity-head.json` | 995 | `430ba6e0e50cc5da85e49943c9377823a18ba46080a40f2115ec020d079f3b79` |
| `irq-if2-control.log` | 200 | `710263bb95e4c10b1119c2c7e127fbd3e32d44632224f7c0de31903cecc49f3c` |
| `mbx.log` | 36773 | `e0025b0c57f945d95901962cf66a55abf8709f7df526c08a946647f39fb18add` |
| `profile-complete.json` | 1529 | `330246864a987ce7a6c5f159f1fa9155c05d8662ba36947c707fbc91bcfbb963` |
| `profile-exec-absent-0.log` | 49369 | `10c3284a0afdbe3780ea5da13933874208d48021913775479d2de2c935fca5fa` |
| `profile-exec-absent-1.log` | 49265 | `da8c780e1c037b4d96685efcbdd86813aa9cbe2716ac3db334cdfc3304d18bab` |
| `profile-exec-absent-2.log` | 49255 | `789f67d640592c11a6a7632dc09b21df0a3b45cfbf468711456ff200ff0daa6d` |
| `profile-exec-absent-3.log` | 49241 | `67d36c71bb4cc63b672052a325f50cbebd1f1d751157675f50e86ae9d12168eb` |
| `profile-exec-sdk-0.log` | 51172 | `8dae830e5746abcb46c82cafbe5f5e3f12eba984cd7efaac8414a9bf288b3675` |
| `profile-exec-sdk-1.log` | 51171 | `fabdf05f11eaa1644a2d8644d9b3e42578bd6dd3f6fae21d246756efbb7a36d6` |
| `profile-exec-sdk-2.log` | 51174 | `77325fcdcd8387dcf9980cf257aecf4ccbd8f9671a466ca75a8ecc5096b64b5d` |
| `profile-exec-sdk-3.log` | 51055 | `6d6124c7b6d5bf1d8511fe3a5427c0ff0cae4e49162b95a55eb12e5c30ea7168` |
| `profile_shard.py` | 2308 | `bb7289a277dd4fcd4d274d80fc74aca2021534785070163dd0f147f36d2efe88` |
| `resources.json` | 237 | `5b4417a4333f10a5469cd95eef07a292498470d45322ece20bb36615b22702b7` |
| `tally.log` | 3982 | `02268c336448885863d0308d88968cde7fe44eedb9743f0589fc01020f7eca11` |
| `verify_profiles.py` | 1830 | `d41f49ed891b1e717d94f602d27c02a619386fee44ed98d817ca0b3bce3bddcc` |

### Integration and manager duties

Clearing `MAAP_CTRL[0]` disables `KL_maap`. `KL_pp_maap_shim` therefore never
answers ALLOC_DA ok, and `talker_active` never asserts. Correct destination
registers alone cannot admit the fabric talker. Before this output is used,
feed the processor's MAAP face from the firmware allocation, or move ACMP onto
the core through F3. This is a #664 decision 3 default-flip condition; F2 does
not alter the wiring or authorize a default flip.

The manager publishes the local commits, obtains independent corrected-head
reviews and a reviewer-owned completion ledger, and handles hosted/local-replica
evidence, dev integration, candidate-merge validation and post-merge containment.
If #683 is still open, its later merge must preserve both ilp32d SDK builds and
this lane's MAAP arms/partitions, then rerun the whole firmware gate set.
No push, PR edit, merge, hardware or bench action occurred in this round.

## Round 1

The following is the retained original implementation evidence. Its review-ready
status was superseded by the two negative reviews and this round's assignment.

[A558]

### F2 MAAP handoff

Status: REVIEW READY; implementation and authorized local validation complete.
Head: `1a5d70faba6a9b01aab6bb868c12e4c7023e0c70`.
Branch: `665-f2-maap`; resumed base: `db9aa8c9b135b34ff3d070a979dee70440b37cc6`.
Executor: [A558]. Internal reviewer: [R528]. External reviewer: [R529].

Assignment: https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6026720272
Resume: https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6026839422
Relates to #665. No push, PR creation/edit, merge, rebase, bench or hardware access.

#### Scope and authority

IEEE 1722-2016 B.2; B.3.2/Table B.7; B.3.3/Table B.8;
B.3.4.1/.2; B.3.5.1 through B.3.5.9; B.3.6.1 through B.3.6.7; B.4.
`docs/reference/FR_NFR.md` NFR-SCOUT-02/03/08 and section 3.4 H-MAAP;
`docs/design/MAILBOX_SPLIT.md`; #678 no synchronous port callbacks.

The resumed FC ingress diagnostic delivers own-unicast DEFEND. Both planted
filter defects still fail their named tests. The original STOP baseline and controls
remain beside the round-2 evidence. Parent fabric deviations are #686; Annex B
is the core oracle. The owner's approval of FC's amended row remains an FC merge
condition. No RTL, shipping-image, default-build or register-definition changes.

#### Changes

| File:line | Change |
|---|---|
| `docs/design/MAILBOX_SPLIT.md:420` | MAAP integration and service proof boundary |
| `sw/firmware/ctrl/README.md:9` | Module/test map and explicit compiler selection |
| `sw/firmware/ctrl/app/ctrl_app.c:36` | Explicit opt-in composition with ADP and separate timers |
| `sw/firmware/ctrl/app/ctrl_app.h:39` | Static MAAP state and composition declaration |
| `sw/firmware/ctrl/maap/README.md:17` | Full clause map, API, work bounds and proof limits |
| `sw/firmware/ctrl/maap/maap.c:11` | Guarded state machine, seeded draws, PDUs, timers and bounded output |
| `sw/firmware/ctrl/maap/maap.h:14` | Pure ports, constants, static state and lifecycle API |
| `sw/firmware/ctrl/maap/maap_csr.c:15` | Existing AAF/CRF DMAC output, loss and mismatch admission closure |
| `sw/firmware/ctrl/maap/maap_csr.h:14` | Ordered per-interface CSR allocation interface |
| `sw/firmware/ctrl/maap/maap_mbx.c:34` | FC channel, range envelope, interface timers/tags and bounded polling |
| `sw/firmware/ctrl/maap/maap_mbx.h:15` | Mailbox-access bounds and static per-interface adapter state |
| `sw/firmware/ctrl/test/ctrl_arms.py:37` | Core, one/two-interface and debug arms; explicit RV32 compiler option |
| `sw/firmware/ctrl/test/ctrl_build.py:36` | Portable source set, release guards and bounded compiler jobs |
| `sw/firmware/ctrl/test/ctrl_mutants.py:439` | Register new defects and named arms |
| `sw/firmware/ctrl/test/maap_differential.py:19` | Unchanged parent RTL/C comparison and case-specific sensitivity |
| `sw/firmware/ctrl/test/maap_mutants.py:12` | 83 new named protocol, adapter, CSR and hook defects |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:84` | MAAP coverage/default gates and exhaustive mutation partition selection |
| `sw/firmware/ctrl/test/test_maap.cpp:97` | 32 core/CSR cases including 18 receive/state/priority cells |
| `sw/firmware/ctrl/test/test_maap_debug.cpp:11` | Debug reentry expected-abort check |
| `sw/firmware/ctrl/test/test_maap_differential.cpp:102` | Eleven shared-stimulus wire/state cases against Annex B and explicit #686 deltas |
| `sw/firmware/ctrl/test/test_maap_mbx.cpp:91` | Eleven mailbox/CSR integration cases at one and two interfaces |
| `sw/firmware/gtest/coverage.ratchet:7` | Generator-owned 100% ratchet for all new portable C, no exclusions added |
| `tb/verilator/mbx/Makefile:20` | New composition dependencies and optional bounded build jobs |

#### Tests and planted defects

New cases: 32 core/CSR, 11 mailbox cases at each interface count, one debug guard
and 11 parent differential cases: 66 executed cases. The complete controller
campaign catches 180 defects, including 83 added here. Eight partitions cover the
179-entry catalog; the final appended allocation-seam defect is additionally caught
in `final-seams.log`. Its append preserves every preceding index. The differential
also catches eleven case-specific defects. A build failure does not count as caught.

Core table indices 0..17 are INITIAL/PROBE/DEFEND × losing/winning local MAC
priority × PROBE/DEFEND/ANNOUNCE. Mailbox rows run at one and two interfaces;
the indexed-routing defect uses two. Each row names a test and its planted defect.

| Test / source | Planted defect IDs |
|---|---|
| `MaapCore.ReleaseLossAndRetry`; `sw/firmware/ctrl/test/test_maap.cpp:259` | `maap-down-start-keeps-owner`, `maap-port-up-keeps-claim`, `maap-release-keeps-enable` |
| `MaapCore.InitialAndThreeRetransmissions`; `sw/firmware/ctrl/test/test_maap.cpp:97` | `maap-initial-send-absent`, `maap-retransmit-count`, `maap-probe-count-not-decremented`, `maap-wire-version`, `maap-wire-length`, `maap-wire-source`, `maap-wire-padding` |
| `MaapCore.ConstantsStrictTimersAndSeed`; `sw/firmware/ctrl/test/test_maap.cpp:119` | `maap-constant-probe_base`, `maap-constant-probe_variation`, `maap-constant-announce_base`, `maap-constant-announce_variation`, `maap-seed-clock-ignored`, `maap-zero-seed-sticks` |
| `MaapCore.UniformDrawRejectsIncompleteBucket`; `sw/firmware/ctrl/test/test_maap.cpp:178` | `maap-biased-random-bucket` |
| `MaapCore.ReverseOctetPriority`; `sw/firmware/ctrl/test/test_maap.cpp:170` | `maap-numeric-mac-priority` |
| `MaapCore.DefendEchoAndIntersection`; `sw/firmware/ctrl/test/test_maap.cpp:188` | `maap-defend-multicast`, `maap-defend-echo-own-range`, `maap-intersection-too-long` |
| `MaapCore.DisjointAdjacentZeroAndDefendRange`; `sw/firmware/ctrl/test/test_maap.cpp:200` | `maap-adjacent-overlaps`, `maap-zero-count-conflicts`, `maap-defend-checks-request` |
| `MaapCore.MalformedAndVersionCompatibility`; `sw/firmware/ctrl/test/test_maap.cpp:211` | `maap-malformed-ethertype`, `maap-malformed-subtype`, `maap-malformed-version`, `maap-malformed-reserved-zero`, `maap-malformed-reserved-high`, `maap-malformed-cdl-short`, `maap-malformed-cdl-truncated`, `maap-malformed-cdl-current`, `maap-malformed-source-zero`, `maap-malformed-source-group`, `maap-malformed-destination`, `maap-malformed-own-probe`, `maap-valid-minimum-refused`, `maap-future-version-refused` |
| `MaapCore.InitAndPreferredRangeBounds`; `sw/firmware/ctrl/test/test_maap.cpp:237` | `maap-range-end-off-by-one` |
| `MaapCore.StalledOutputRetainsOrderAndOriginalExpiry`; `sw/firmware/ctrl/test/test_maap.cpp:281` | `maap-expiry-forgotten-on-stall`, `maap-allocation-before-commit`, `maap-probe-announce-reordered` |
| `MaapCore.QueueBoundAndWithdrawal`; `sw/firmware/ctrl/test/test_maap.cpp:299` | `maap-overflow-uncounted`, `maap-poll-unbounded`, `maap-release-leaves-output` |
| `MaapCore.ReentrantPortsAreCountedAndIgnored`; `sw/firmware/ctrl/test/test_maap.cpp:312` | `maap-reentry-not-counted` |
| `MaapDebug.SynchronousExpiryAsserts`; `sw/firmware/ctrl/test/test_maap_debug.cpp:11` | `maap-debug-no-assert` |
| `MaapCsr.EveryStreamAddressAndLossGate`; `sw/firmware/ctrl/test/test_maap.cpp:338` | `maap-stream-index-missing`, `maap-selection-not-restored`, `maap-fabric-owner-kept`, `maap-loss-keeps-crf` |
| `MaapCsr.ShapesAndCountRefusal`; `sw/firmware/ctrl/test/test_maap.cpp:356` | `maap-count-mismatch-accepted`, `maap-crf-index-wrong` |
| `MaapHost.StaleTagsForeignInputsAndLinkEdges`; `sw/firmware/ctrl/test/test_maap_mbx.cpp:190` | `maap-timer-tag-ignored`, `maap-foreign-not-counted` |
| `MaapHost.AttachRefusalsAndTimerWrap`; `sw/firmware/ctrl/test/test_maap_mbx.cpp:214` | `maap-half-attach` |
| `MaapHost.InterfaceIsolationAndRangeEnvelope`; `sw/firmware/ctrl/test/test_maap_mbx.cpp:233` | `maap-interface-zero` |
| `MaapHost.HMaapConflictLossAndRetry`; `sw/firmware/ctrl/test/test_maap_mbx.cpp:113` | `maap-no-range-filter` |
| `MaapHost.HMaapFilterTupleAndRate`; `sw/firmware/ctrl/test/test_maap_mbx.cpp:139` | `maap-filter-destination-ignored` |
| `MaapHost.HMaapTimerCommitsAndIntervals`; `sw/firmware/ctrl/test/test_maap_mbx.cpp:91` | `maap-late-service` |
| `MaapHost.HMaapBacklogAndStallNeverRestartClock`; `sw/firmware/ctrl/test/test_maap_mbx.cpp:162` | `maap-stall-unqueued` |
| `MaapHost.ExplicitAppComposition`; `sw/firmware/ctrl/test/test_maap_mbx.cpp:249` | `maap-app-channel-closed` |
| `MaapHost.CallbackWorkAndEveryOutputCount`; `sw/firmware/ctrl/test/test_maap_mbx.cpp:272` | `maap-callback-work-overrun` |
| `MaapHost.IgnoredInputCommitsStateWithinOriginalBudget`; `sw/firmware/ctrl/test/test_maap_mbx.cpp:297` | `maap-ignored-input-late` |
| `AllStates/MaapCell.TableB7/0`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-0` |
| `AllStates/MaapCell.TableB7/1`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-1` |
| `AllStates/MaapCell.TableB7/2`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-2` |
| `AllStates/MaapCell.TableB7/3`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-3` |
| `AllStates/MaapCell.TableB7/4`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-4` |
| `AllStates/MaapCell.TableB7/5`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-5` |
| `AllStates/MaapCell.TableB7/6`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-6` |
| `AllStates/MaapCell.TableB7/7`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-7` |
| `AllStates/MaapCell.TableB7/8`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-8` |
| `AllStates/MaapCell.TableB7/9`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-9` |
| `AllStates/MaapCell.TableB7/10`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-10` |
| `AllStates/MaapCell.TableB7/11`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-11` |
| `AllStates/MaapCell.TableB7/12`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-12` |
| `AllStates/MaapCell.TableB7/13`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-13` |
| `AllStates/MaapCell.TableB7/14`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-14` |
| `AllStates/MaapCell.TableB7/15`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-15` |
| `AllStates/MaapCell.TableB7/16`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-16` |
| `AllStates/MaapCell.TableB7/17`; `sw/firmware/ctrl/test/test_maap.cpp:140` | `maap-table-b7-17` |
| `MaapHost.AcquiredRangeFeedsExistingCsrPath`; `sw/firmware/ctrl/test/test_maap_mbx.cpp:308` | `maap-allocation-seam-disconnected` |
| `MaapDifferential.ProbeSequenceWireAndCadence`; `sw/firmware/ctrl/test/test_maap_differential.cpp:102` | `wire`: control_data_length changed from 16 to 28 |
| `AllStates/DifferentialCell.SharedConflict/0..8`; `sw/firmware/ctrl/test/test_maap_differential.cpp:122` | `maap-table-b7-0/1/2/6/7/8/12/13/14`, one defect per state/message stimulus |
| `MaapDifferential.ReleaseAndRetry`; `sw/firmware/ctrl/test/test_maap_differential.cpp:158` | `release`: released state incorrectly remains DEFEND |

The replayed ingress diagnostic has five positive cases. `ignore_destination`
misdelivers foreign-unicast DEFEND and `reject_all_destinations` blocks four valid
receive cases. Round-2 baseline and both controls are retained.

#### Coverage

The ratchet was regenerated with its generator, then checked. Existing exclusions
are unchanged. New files have no exclusions; debug assertion behavior is separately
tested by the expected-abort case. Values below are after existing exclusions.

| Portable source | Lines hit/total | Branches hit/total |
|---|---|---|
| `sw/firmware/ctrl/adp/adp.c` | 168/168 | 73/73 |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/38 |
| `sw/firmware/ctrl/app/ctrl_app.c` | 28/28 | 20/20 |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 95/95 | 56/56 |
| `sw/firmware/ctrl/maap/maap.c` | 205/205 | 138/138 |
| `sw/firmware/ctrl/maap/maap_csr.c` | 39/39 | 18/18 |
| `sw/firmware/ctrl/maap/maap_mbx.c` | 98/98 | 60/60 |
| `sw/firmware/ctrl/mbx/mbx.c` | 173/173 | 62/62 |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 |
| `sw/firmware/ctrl/wire/wire.h` | 10/10 | 2/2 |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 195/195 | 104/104 |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/259 |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/63 |

#### H-MAAP evidence and limits

The start is original RX_HEAD publication or armed timer deadline; output completion
is the complete accepted TX_HEAD write. Ignored input completes at state commitment.
The monotonic host model clock assumes 100 ns per ordered mailbox transaction and a
millisecond timer tick. Checks preserve the deadline's original fractional position
and never restart after a queue stall.

| Observed path | Pass accesses | One-interface ns | Two-interface ns |
|---|---|---|---|
| First probe expiry | 30 | 8300 | 12200 |
| Second probe expiry | 30 | 11300 | 15200 |
| Final probe expiry plus ANNOUNCE | 56 | 16600 | 20500 |
| Announcement expiry | 30 | 19900 | 23800 |
| Received conflict DEFEND | 40 | 3900 | 3900 |

Callback ceiling: 48 mailbox accesses. Standalone pass ceiling: 616 at one interface,
664 at two; add other protocol callbacks for a composed loop. The service budget is
10 ms against the shared 50 ms ceiling. A forced 11 ms stall must fail on recovery.
Separate datapath CSR operations are bounded but are not mailbox transactions.

The allocation interface is `maap_csr_allocation` over ordered per-interface
`maap_csr_port` reads/writes to existing AAF/CRF and indexed stream registers.
The end-to-end test drives acquisition and conflict loss through that callback.
The platform supplies those operations, exclusive indexed-window ownership,
boot-policy controls and initial media quiescence. Ordinary startup and shipping
policy remain unchanged. Target CPU, arbitration, wire departure, NVM overlap,
all-placement, audio-deadline and bench timing proof remain integration obligations.

#### Gate table

Evidence labels are relative to the lane's `round2` scratch directory. Every command
ran in the foreground with a bounded invocation. Environment: disk-backed TMPDIR;
pinned simulator 5.050; VERILATOR_JOBS=2; build jobs at most 8; campaign workers at
most 4; explicit CTRL_RV32_CC=riscv64-elf-gcc. Dependencies, exports and large logs
remain in scratch, identified by size and SHA-256 receipts below.

| Gate / command | Exit | Evidence / result |
|---|---|---|
| Original STOP diagnostic replay | 0 | `baseline.log`, `ignore_destination.log`, `reject_all_destinations.log`; five positive cases and both defects detected |
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --mutation-shard INDEX 8` for INDEX 0..7 | 0 each | `campaign0.log` through `campaign7.log`; 179 catalog entries caught; final appended defect caught in `final-seams.log` |
| Final MAAP integration arms and five targeted controls | 0 | `final-seams.log`; both interface variants, complete CSR callback and timing controls |
| `python3 sw/firmware/ctrl/test/maap_differential.py --self-test` | 0 | `differential-final.log`; 11 positives and 11 named defects caught |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | `firmware-nvm.log` |
| `python3 sw/firmware/gtest/tally_selftest.py` and `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 each | `ft-selftests.log` |
| `python3 sw/firmware/gtest/fw_coverage.py --write --jobs 4` | 0 | `coverage-all.log`; ratchet generator |
| `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4` | 0 | `coverage-final.log`; all 17 files meet the ratchet |
| `make -C tb/verilator/mbx -j1 VBUILD_JOBS=8` target partitions | 0 each | `mbx-wb-axil.log`, `mbx-cosim-if2.log`, `mbx-mutants.log`; both buses, firmware co-simulation, two-interface RTL/model and five controls |
| Mailbox build job selector argument comparison | 0 | `mbx-job-option.log`; exact token equality to successful suite flags |
| B01: `python3 avdecc/gen_aem_store.py --self-test` | 0 | `B01.log`; PASS |
| B02: `python3 scripts/pp_srcs.py --check --selftest` | 0 | `B02.log`; PASS |
| B03: `python3 scripts/lint_rtl.py --check --self-test` | 0 | `B03.log`; PASS |
| B04: `python3 scripts/suite_shards.py --selftest` | 0 | `B04.log`; PASS |
| B05: `python3 scripts/ci_events.py --check` | 0 | `B05.log`; PASS |
| B06: `python3 scripts/ci_scope.py --selftest` | 0 | `B06.log`; PASS |
| B07: `python3 scripts/ci_events.py --selftest` | 0 | `B07.log`; PASS |
| B08: `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `B08.log`; PASS |
| B09: `python3 scripts/check_feature_status.py` | 0 | `B09.log`; PASS |
| B10: `python3 scripts/check_submodule_docs.py` | 0 | `B10.log`; PASS |
| B11: `python3 scripts/check_cpp_idiom.py` | 0 | `B11.log`; PASS |
| B12: `python3 scripts/check_py_idiom.py` | 0 | `B12.log`; PASS |
| B13: `python3 scripts/docs_check.py` | 0 | `B13.log`; PASS |
| B14: `python3 scripts/check_doc_style.py` | 0 | `B14.log`; PASS |
| B15: `python3 scripts/check_doc_style.py --selftest` | 0 | `B15.log`; PASS |
| B16: `python3 scripts/check_solution_docs.py` | 0 | `B16.log`; PASS |
| B17: `python3 scripts/check_doc_paths.py` | 0 | `B17.log`; PASS |
| B18: `python3 scripts/check_archive.py` | 0 | `B18.log`; PASS |
| B19: `python3 scripts/gen_toc.py --verify-anchors` | 0 | `B19.log`; PASS |
| B20: `python3 scripts/gen_toc.py --check` | 0 | `B20.log`; PASS |
| B21: `python3 scripts/check_hygiene.py --check` | 0 | `B21.log`; PASS |
| B22: `python3 scripts/check_todo_ownership.py` | 0 | `B22.log`; PASS |
| B23: `python3 scripts/check_sv_idiom.py` | 0 | `B23.log`; PASS |
| B24: `python3 scripts/check_sh_idiom.py` | 0 | `B24.log`; PASS |
| B25: `python3 scripts/check_rtl_source_lists.py` | 0 | `B25.log`; PASS |
| B26: `python3 scripts/check_soc_sources.py` | 0 | `B26.log`; PASS |
| B27: `python3 scripts/check_port_contracts.py` | 0 | `B27.log`; PASS |
| B28: `python3 scripts/check_nvm_record_space.py` | 0 | `B28.log`; PASS |
| B29: `python3 scripts/check_baremetal_only.py --check` | 0 | `B29.log`; PASS |
| B30: `python3 scripts/check_baremetal_only.py --selftest` | 0 | `B30.log`; PASS |
| B31: `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | `B31.log`; PASS |
| B32: `python3 scripts/check_sweep_shape.py --self-test` | 0 | `B32.log`; PASS |
| B33: `sudo -n docker run --rm --network none --cap-drop ALL --security-opt no-new-privileges --memory 2g --cpus 2 --user 1000:1000 --mount type=bind,src=$CANDIDATE_ROOT,dst=/candidate,readonly --mount type=bind,src=$CHECK_ROOT/container-B33,dst=/scratch --workdir /candidate --env TMPDIR=/scratch --env PYTHONDONTWRITEBYTECODE=1 catthehacker/ubuntu:full-latest python3 scripts/xvlog_gate.py --check` | 0 | `B33.log`; SKIPPED: vendor analyzer absent in disposable container |
| B34: `python3 scripts/measure_control_flow.py --selftest` | 0 | `B34.log`; PASS |
| B35: `python3 scripts/measure_cohesion.py --selftest` | 0 | `B35.log`; PASS |
| B36: `python3 scripts/check_em_dash.py --base db9aa8c9b135b34ff3d070a979dee70440b37cc6` | 0 | `B36.log`; PASS |
| B37: `python3 scripts/measure_fail_fast.py --check` | 0 | `B37.log`; PASS |
| B38: `python3 scripts/measure_test_evidence.py --check` | 0 | `B38.log`; PASS |
| B39: `python3 scripts/measure_naming.py --check` | 0 | `B39.log`; PASS |
| B40: `python3 scripts/measure_test_evidence.py --selftest` | 0 | `B40.log`; PASS |
| B41: `python3 scripts/gen_toc.py --selftest` | 0 | `B41.log`; PASS |
| B42: `python3 scripts/check_em_dash.py --selftest` | 0 | `B42.log`; PASS |
| B43: `python3 scripts/docs_check.py --selftest` | 0 | `B43.log`; PASS |
| B44: `git diff --check db9aa8c9b135b34ff3d070a979dee70440b37cc6` | 0 | `B44.log`; PASS |
| B45: `python3 scripts/check_wire_accountability.py --self-test` | 0 | `B45.log`; PASS |
| B46: `python3 scripts/check_entity_shape.py --self-test` | 0 | `B46.log`; PASS |
| B47: `python3 scripts/check_deploy_shape.py --self-test` | 0 | `B47.log`; PASS |
| D01: `python3 scripts/gen_hdl_reference.py --selftest` | 0 | `D01.log`; PASS |
| D02: `python3 scripts/gen_hdl_reference.py --output $CHECK_ROOT/hdl-reference` | 0 | `D02.log`; PASS |
| D03: `python3 scripts/check_gptp_docs.py` | 0 | `D03.log`; PASS |
| D04: `python3 scripts/check_gptp_docs.py --selftest` | 0 | `D04.log`; PASS |
| D05: `python3 docs/DOC_MAP.gen.py --check` | 0 | `D05.log`; PASS |
| D06: `python3 docs/DOC_MAP.gen.py --selftest` | 0 | `D06.log`; PASS |
| D07: `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | `D07.log`; PASS |
| D08: `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | `D08.log`; PASS |
| D09: `python3 scripts/check_solution_docs.py --selftest` | 0 | `D09.log`; PASS |
| D10: `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 | `D10.log`; PASS |
| D11: `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | `D11.log`; PASS |
| D12: `python3 scripts/check_submodule_docs.py --selftest` | 0 | `D12.log`; PASS |
| D13: `python3 scripts/gen_wavedrom.py --selftest` | 0 | `D13.log`; PASS |
| D14: `python3 scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | `D14.log`; PASS |
| D15: `python3 scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | `D15.log`; PASS |
| D16: `python3 scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | `D16.log`; PASS |
| D17: `python3 scripts/check_diagram_pngs.py` | 0 | `D17.log`; PASS |
| D18: `python3 scripts/check_diagram_pngs.py --selftest` | 0 | `D18.log`; PASS |
| D19: `python3 scripts/check_feature_status.py --self-test` | 0 | `D19.log`; PASS |
| D20: `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | `D20.log`; PASS |
| D21: `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | `D21.log`; PASS |
| D22: `python3 scripts/ci_rv32_sdk.py --destination $CHECK_ROOT/rv32-sdk` | 0 | `D22.log`; PASS |
| D23: `python3 sw/builder/test_firmware_compiler.py --selftest` | 0 | `D23.log`; PASS |
| D25: `python3 scripts/check_nvm_record_space.py --self-test` | 0 | `D25.log`; PASS |
| D26: `python3 scripts/check_nvm_capture.py` | 0 | `D26.log`; PASS |
| D27: `python3 scripts/check_soc_sources.py --selftest` | 0 | `D27.log`; PASS |
| D28: `python3 sw/litex/iob_pack_selftest.py` | 0 | `D28.log`; PASS |
| D29: `python3 scripts/check_rtl_source_lists.py --selftest` | 0 | `D29.log`; PASS |
| D30: `python3 scripts/measure_naming.py --selftest` | 0 | `D30.log`; PASS |
| D31: `python3 scripts/check_port_contracts.py --selftest` | 0 | `D31.log`; PASS |
| D32: `python3 scripts/measure_fail_fast.py --selftest` | 0 | `D32.log`; PASS |
| D33: `python3 scripts/check_todo_ownership.py --selftest` | 0 | `D33.log`; PASS |
| D34: `python3 scripts/check_hygiene.py --selftest` | 0 | `D34.log`; PASS |
| D35: `python3 scripts/check_sv_idiom.py --selftest` | 0 | `D35.log`; PASS |
| D36: `python3 scripts/check_cpp_idiom.py --selftest` | 0 | `D36.log`; PASS |
| D37: `python3 scripts/check_py_idiom.py --selftest` | 0 | `D37.log`; PASS |
| D38: `python3 scripts/check_sh_idiom.py --selftest` | 0 | `D38.log`; PASS |
| D39: `sudo -n docker run --rm --network none --cap-drop ALL --security-opt no-new-privileges --memory 2g --cpus 2 --user 1000:1000 --mount type=bind,src=$CANDIDATE_ROOT,dst=/candidate,readonly --mount type=bind,src=$CHECK_ROOT/container-D39,dst=/scratch --workdir /candidate --env TMPDIR=/scratch --env PYTHONDONTWRITEBYTECODE=1 catthehacker/ubuntu:full-latest python3 scripts/act_ci.py --selftest` | 0 | `D39.log`; offline self-test inside disposable container only |
| D40: `python3 scripts/check_archive.py --selftest` | 0 | `D40.log`; PASS |
| G01: `make -C gptp-processor docs` | 0 | `G01.log`; PASS |
| E01: `python3 sw/mailbox/gen_mailbox.py --check --crosscheck` | 0 | `E01.log`; PASS |
| E02: `python3 sw/mailbox/gen_mailbox.py --selftest` | 0 | `E02.log`; PASS |
| B48: `python3 sw/builder/test_builder.py --require-rv32` | 0 in every partition | 100 original test functions; gate 11 historical calibration NOT RUN because prior report is absent |
| D24: `python3 sw/builder/test_firmware_compiler.py --absent --audit AUDIT` | 0 in every partition | Explicit compiler-absence control; no compiler-dependent proof |
| N01/N02: no-Git export documentation and feature-status checks | 0 each | `N01.log`, `N02.log`; export of the exact committed head, initialized submodule contents included |

#### Bounded builder reproduction

The original main sequence runs at indices [0,12), [13,56), [56,90), [90,100).
Function 12 is the complete bare-metal profile gate. For that function only,
scratch AST dispatch partitions independent case iterators at source lines
15307, 15349, 15604, 15650, 17016, 17021, 17029, 17038 and 17060 across indices
0..3. Every original assertion remains unchanged. Other setup and checks run in
every partition. The mutation tuple itself is partitioned before its loop so the
original tally remains truthful for each invocation. The manifest verifies identical
source/case hashes and exactly one occurrence of every selected-loop case across
all four runs. Both required SDK and absent-compiler modes run all four.
The original audit maps only the compiler selector's argv[0] to a verified scratch
SDK. Flags, inputs, results and all audit assertions remain unchanged. This is local
gate evidence, not hosted-selector deployment evidence.

The unpartitioned profile and absent-compiler attempts exceeded foreground time
limits; those attempts are not passes. Earlier fixture corrections and initial
sensitivity escapes are also not final evidence. Old logs remain retained; final
receipts name completed runs only.

#### Outstanding integration and review

Independent [R528]/[R529] reviews, the reviewer-owned five-lens ledger, hosted
checks, candidate-merge validation and post-merge containment remain pending.
No PR is created or updated, no branch is pushed and no merge is performed.
The manager must integrate dev with --no-ff after FC lands, then validate that head.

#### Evidence receipts

All final evidence below is retained in scratch. These receipts identify the exact bytes.
The controller union audit catches 180/180 current defect IDs. The profile manifest
checks all 100 original builder functions and the complete case populations below.


| Profile mode | Partitioned source loop line | Cases executed / total |
|---|---|---|
| sdk | 15307 | 4/4 |
| sdk | 15349 | 20/20 |
| sdk | 15604 | 38/38 |
| sdk | 15650 | 4/4 |
| sdk | 17021 | 358/358 |
| sdk | 17038 | 3/3 |
| sdk | 17060 | 43/43 |

sdk partition durations in seconds: 273.32, 289.32, 298.58, 275.64.

| Profile mode | Partitioned source loop line | Cases executed / total |
|---|---|---|
| absent | 15307 | 4/4 |
| absent | 15349 | 20/20 |
| absent | 15604 | 35/35 |
| absent | 15650 | 4/4 |
| absent | 17016 | 17/17 |
| absent | 17021 | 256/256 |
| absent | 17029 | 3/3 |

absent partition durations in seconds: 151.21, 158.37, 174.79, 155.82.


| Evidence path | Bytes | SHA-256 |
|---|---|---|
| `../1722-2016.txt` | 796018 | `f8725b4553a4afdecfc1adf888c7fc7ca44a14d67056b4836a151eb177caf40d` |
| `../baseline.log` | 1403 | `ca2c00c891b62dc98e805f1e63e735ec81660aea87ce9c2e61f5a2b421452048` |
| `../ignore_destination.log` | 3483 | `e38bb42f991a1025505ce484cbc667f59a070be2d1f7361db178e712319beab2` |
| `../ingress_probe.cpp` | 3210 | `048e2e31407b1aeb7bc8924ee936d38b9fee28e9372c92179ccc196402542e04` |
| `../reject_all_destinations.log` | 5756 | `f269925202c93553df9b1acba1da5693def974d03f180d9f502d122f4cd2135a` |
| `../run_ingress_probe.py` | 2619 | `0fc09bff0add807b358888cf592414f578c9766b037b5ddb9d6e17d881355b5c` |
| `B01.log` | 3596 | `9f126bf9dfc7cb552a2414b98d2792449dc4ae126395997750d5039cb896f022` |
| `B02.log` | 955 | `fad5e1b9dd5f465b7fcb2334e2abe6c6db44be93b5bb12afb3a35f3ebf432e1a` |
| `B03.log` | 14888 | `fdfaa1c6d9058fd1f1d30ef75e8590d1e633c21b21ff6fb7455e0542dc99123a` |
| `B04.log` | 1269 | `52039414c215a5a8cf1f3ebe1b830567c059f0a4df09d097926beaa26719316d` |
| `B05.log` | 167 | `617e44ed66b13896b9bf7fa2c76c7242990622e9ced9ba79a693484ad4bd4a77` |
| `B06.log` | 6877 | `cda2e3e13229332d91d0863932d724a7fdeef280c924f262aa43f5d5448c62da` |
| `B07.log` | 150787 | `323df9bf49ae1b88fd84f24ed0dee9120127a78d412f74c2ceec781f980cd55c` |
| `B08.log` | 118 | `d0be3b6428ae2079134f2a21b2972c524a26103b0e9c8b64039bb24ae22797dc` |
| `B09.log` | 29 | `802f5eeb2f0aa147169f3ddb9c64d4369ca92ab380455195403f2e8ae02490d0` |
| `B10.log` | 47 | `dffc750855c2574e23bad0174564fcde9dc0d351b65e2f5e954f2dc64e894835` |
| `B11.log` | 316 | `4442bd5d4073138fd9e71b3c6bafecbd7d17ec2a85c5deaaa72d8ce6eda0c46d` |
| `B12.log` | 461 | `635aa4a9c39b9d4066735e6ee4cd19217bd1133942d03ad5bcfbba4f916e06e5` |
| `B13.log` | 128 | `962f461c1639dcb0cf9c4a2a46e24ed200529f6b5da33e02d71850bc2ebb1d91` |
| `B14.log` | 47 | `1491d3f6bec03b920cf58f5fb28e6abff4a9d433a758bc0fe5d2db77bf4f53cd` |
| `B15.log` | 33 | `0acc8195c60dd145a8f17d24b7b07c29074ac131d71893f9cef5f880239dd909` |
| `B16.log` | 87 | `48ac84ddbd532247deb21834ee60bd4b7322f69bb9ab9fc5f9901969ccb38c42` |
| `B17.log` | 100 | `f6b4bf0ee623dc3c0e2d45e1b24678a931ceece007f4eeaf3e06fa47af34c3b4` |
| `B18.log` | 93 | `69d45782911c2958be2fef681f849e9b3915293c938de331bb6885dab21fd46c` |
| `B19.log` | 64 | `47c81d0215393f2dcd32e68857b340b140a5dc1808509010aa87038af24f36a6` |
| `B20.log` | 94 | `35e7e86e67b2d3d3968be2ae5107b946549d31bc8426a393fdae86c12f341b47` |
| `B21.log` | 2000 | `83dffcb345691dae55056b6babf94f8cb6d02e5619acc2c54a26e00b043cdb9a` |
| `B22.log` | 161 | `fa01582c02b69a59b174bd6dea0892f022138072e0ab8735e0fe57d8d0039d08` |
| `B23.log` | 218 | `aed2873a1909e4a41b3e6dee6dc5aaab993bbf1ef41f556062a5b377a6a8b167` |
| `B24.log` | 235 | `7ace602f03fa0e411862de119cff9d337583f1f2170d920dff65a0e0f39ee6d9` |
| `B25.log` | 153 | `ed979d7e26c3cd7a6f14364c11994089b77632424d04252613eeed458ebc8a95` |
| `B26.log` | 85 | `7ea77f321df0437a49feae4436006813f0653a8151945dbf7601fe0e5e289033` |
| `B27.log` | 421 | `3c1a34d3169cf6f071f2cbb62a8ddca7591338e9f45ee665e1c66758f22c5524` |
| `B28.log` | 2578 | `cf53746e34d5ec76dc263f5ce98c17e9f1b227048b67c9e6bdbb8e798007f4f0` |
| `B29.log` | 72 | `56a770ed2f431447ed314974411097eca7fc31d4b7503eaac5f8f58b59e2efd1` |
| `B30.log` | 43 | `09b491b87735efaef68eafe7f45f4fe4ba1f8ad036c0d252d2a93a00906d51f8` |
| `B31.log` | 5189 | `cba18482dbf27c70ee56b28a8fbbe7bfdc2cc49b4644a42daa5ad4db8f6d4972` |
| `B32.log` | 19682 | `7d9161b60de4b9034b89d705732d30722289339ca8a65fe4d15f5c6db1f352e6` |
| `B33.log` | 109 | `2530eb83cff115f67e104fd0440c33b78441363278d88c86ae155a8e7bf9cdb0` |
| `B34.log` | 2565 | `34d85283c432e38af30c33dcc6de6b85208e1ec98a538b78e68061d27421972b` |
| `B35.log` | 728 | `10f526cea8560a3a39135260553e767b316076d7598559fb5f07e8cfab2c5363` |
| `B36.log` | 140 | `681e5efdcd63e5dbfa729855f6cbd824eb6a849c6086b2b65191f03dcaf29e67` |
| `B37.log` | 6085 | `bbf0264b3cc1beedf3b725b71c379498d33eceeff22f734695af87a77240563e` |
| `B38.log` | 14635 | `4322b73a4b194c5aedc7a75ca57b7e20bbecce56a56032963eb515d2e1892a2a` |
| `B39.log` | 36608 | `1cf945250501b5b0267ea1d21f976938536502d765b18d75110bfb3bffbc4508` |
| `B40.log` | 5659 | `3c818777e9f41c6d64a15fa699cd238a94b030f0ce19981df099f855b97416ba` |
| `B41.log` | 38 | `d7fd5f6ebcdd25e6cf93b623b0fba00cfa32d19c812ce34eb6b8d8b352ac9b32` |
| `B42.log` | 42 | `46aaf33b1a5f1d99dba778a65e86a452bbd5642cde32cf136a7a8e1721f7a19a` |
| `B43.log` | 56 | `83cb6b9c5f7a556a8ea31ad3a751a39e6d573b00fe44ac39f5e1591022048339` |
| `B44.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `B45.log` | 4965 | `bd97b8b53304baf2b912ac2e4ec507e3b8f9ae4c5c2511b5dc69a41d2cbdd3d4` |
| `B46.log` | 25694 | `65d5dc4df5f47df5472223c1e4a59a8b35ce8d135e1a42e9db41f563ec8337b4` |
| `B47.log` | 9270 | `e39530f8b8939af926a16b241021b155c0df83c6cfce904280e2c5d16e60ec73` |
| `B48-0-12.log` | 10311 | `7ca864e4af3d1297813dc8724dfa30125da081408e9a9032db92cd6581014cbf` |
| `B48-13-56.log` | 18341 | `863f4389c408ab674d033e11ab4f5c7bfb40d0166206c992e395fbf31c1d6ede` |
| `B48-56-90-rerun.log` | 19796 | `80689342960fddb0e49d8c12f0cfaa00d25267fd201948847ac8a3faea3c8af1` |
| `B48-90-100.log` | 10795 | `7581f4c60fcce6a45bb6b8a4b1aa7a0c436f725657c09d3d26bcff5ee28f17f0` |
| `D01.log` | 407 | `ff000e18e7b2e89d601d8d53f42344c1a6ac735de6a5ecd377199bf161fab974` |
| `D02.log` | 407 | `15a0a30ff1cc69a56c5a75aeb69f6bba787ea03a6dce12eebc0460542ea829be` |
| `D03.log` | 41 | `d8a77a32600566f0613626fd361bad845759693a08b1095dd54865c1aa25455d` |
| `D04.log` | 46 | `200332e4eddfd8a6338d8a4dbe27d2f513de92f951a1aa1f6b25882182bc290e` |
| `D05.log` | 61 | `74408f0fbcdfc1c7e22f6eccd3eb299da61cabe9bb4526eed416b31a8bf61e16` |
| `D06.log` | 60 | `85ddf25d9a99974b71a9c165cbfbbf390be3d7bf74f081b4cc669622a0a562b9` |
| `D07.log` | 60 | `51058c96a481bf763246394b619601227bdec11b6b11ddcaa1d6f57593d2f1f4` |
| `D08.log` | 61 | `7c7ad79fa685d29607abf71e3a99d98855fd7ffa1ba5fbf7de23bfb41a33c8fa` |
| `D09.log` | 59 | `c57d3ed2e5c9be43085106227b69fe55f866b1198ad209fbb27f940e5757ec30` |
| `D10.log` | 54 | `905777610f39981543faabafcc11309ac6ab670121c8866a45e171e5c9b7d00c` |
| `D11.log` | 60 | `51bca8fb66fd6f0acc480e3364f74fd7a4874946b191468bfbe20ad159cca889` |
| `D12.log` | 66 | `54dbecff3ad17dc651e86c7b313ef57fa96baf89fb40f0fb90af4bbb8ddc802b` |
| `D13.log` | 77 | `8439889f74aa49f8d61f50d6b525f358d0774a4133b54cd9895edad971302d42` |
| `D14.log` | 58 | `b3f8f3a790f92f14932f7c8a8c6b7ad9f33d327b6a6cfe653364d5f34617f8e3` |
| `D15.log` | 54 | `4d9e7670f2a4615d27d64a23c95a4882fd923026e00120f90d44a031c39b61d5` |
| `D16.log` | 52 | `411f08b7121f1a0c6b28105fe433aa4561caad5a8e4caf9e7a6c6aa2fd33cac9` |
| `D17.log` | 66 | `05e0fcfa26a97494e8983dcfca3ad89cdaf91e390acbfb9dbdfb6f614cba4e51` |
| `D18.log` | 59 | `918e8cc85a2a2b0d45eeb3f0c7b006824c81e2ed404a535eded095b09d875dc5` |
| `D19.log` | 1500 | `77f7649b1865c0daf4f3de04dd18c78be4885c9c94a8f03fd1e4f262758c3184` |
| `D20.log` | 66 | `7ca87a8501c54854805f1cf90d49b2a8ff6353a1049fd21cf0631569f5024e41` |
| `D21.log` | 6221 | `fbf80e28d7fd44bbdda399a49861e76ab27490bff32acc19ad33061fb1fb13b6` |
| `D22.log` | 2536 | `70a300c4aa78724a0482c0b45ad29e29edda6861545d4ebac6ea34a3ce29f166` |
| `D23.log` | 138 | `f6da142138888df7ecd9ef31e7b86895260648309005e1400148d78004e385d7` |
| `D25.log` | 7010 | `8e636c8b39e0ce66934ec2a3a7088ef7e6be29b5820a3a87f147d40c612320c6` |
| `D26.log` | 324 | `9a4196c774ce4ddfa9980cf9345d111028f3afa812677fe5bab392f81c955439` |
| `D27.log` | 1501 | `d877c9fa9a5d1db2854c5ed3486ca7d2d135944cf3953143bdf63b554f8c3dc0` |
| `D28.log` | 3147 | `55e08920618778573a58f152092c4605e53735fdaf550c99ed72016963b2ffad` |
| `D29.log` | 3300 | `418b0ce0f1f8a55805a4c0e75385ae0f3c18b83b3af16598f5cfc45b40591f1d` |
| `D30.log` | 4026 | `20635e2ee5994ddc3555ad8acef6af506885fef1ccec25b9c4efb88ab4984c02` |
| `D31.log` | 4619 | `8cbdbe06b994bf0db6efd8d9289a0a237bb965d3a771a9d536aa23e8ae0ae75e` |
| `D32.log` | 6597 | `ef92c9eb4e29bf495c938a2ebe16cb2ec7896671a4e7a63ae465c76f5ca8373a` |
| `D33.log` | 2584 | `696cea82f33dcda09f3d8b1047ee2682f9ca7c6da9348a07813eaf3d3d6f978b` |
| `D34.log` | 1847 | `2c7b5cb25dc4cc0407fc27441f4bba2291c74fa2aa2b22f1276e129651f615a8` |
| `D35.log` | 2955 | `0e4826a9db5e2e72c2d3a62bfef0d017bacb9a51238353b44b469b7dbd1c5f9b` |
| `D36.log` | 3593 | `7fd74c4ebf8b2f0a9812a20518981f63c8350a34c535bcde2c7fa6c58fbec2b9` |
| `D37.log` | 2531 | `d7413b83955948950d15e364a901be97cf05148dad38e97be07b2d63eb46406d` |
| `D38.log` | 2461 | `b9af4f07f8aabdddc7af15799e1e06640c7a0a356ef30681b059784e385d3a57` |
| `D39.log` | 36483 | `876a6eca5975005e4e1d1ddddad9f74d2443039a10df8b7f590e4c781632fdab` |
| `D40.log` | 35 | `83aa5efe967935657a1678bf63262a7c435d29d571cc08dd2ae8cf6f8569d34a` |
| `E01.log` | 26 | `9bb7d3a8faff1627f39a3bb7c9462a0b15ec8dd6c94a44c48d2fc7ac515a982f` |
| `E02.log` | 4537 | `651ca60d7658c7566fac08cb00c7837697902969cb42cb5804d6e1a08e4bd527` |
| `G01.log` | 2670 | `b8d251402281ad38d34f2afd1019bce15961b876a705e06ce2c67b579c038641` |
| `N01.log` | 196 | `e609d1792d57affec06f8d7821e7fd66659036b94a30a4785311b09d308bd662` |
| `N02.log` | 29 | `802f5eeb2f0aa147169f3ddb9c64d4369ca92ab380455195403f2e8ae02490d0` |
| `baseline.log` | 1387 | `12e3aa14e68f24b3034f88f3d01d73fa026334b9931e25f8effbc23be5df5770` |
| `builder_shard.py` | 1304 | `6846c87c93281608ca37050119b8ab229ab1a3e53e6df52d5101bdaa44a5f863` |
| `campaign-complete.json` | 209 | `5747ffe4faff36c5356422de483972c951348096797758fad9f3e64d2c557d7b` |
| `campaign0.log` | 8088 | `ee89099ec41d9e05dd52d910125f6749c4739e94aaff49361fd8eb9c4c6b35fe` |
| `campaign1.log` | 8083 | `769c40bda600c9bce0b349b4555466482931a1c22a91a4c390e52b4d19e7c35c` |
| `campaign2.log` | 8431 | `c6e07c2fcba9dfccd7a7547416408cb83af08568a207edce2ce69181755b9409` |
| `campaign3.log` | 7935 | `e5b7790be95832fbbabab9bc723033760c39e6cab2208eed06d5a74f1562cf9e` |
| `campaign4.log` | 8630 | `b9a4611cbdfdae800d48baad15039342f30b4d0f2c66b2adea0fe80ea28d1185` |
| `campaign5.log` | 8729 | `c2b043ce9ba2d6cce02c9cf3decbea5605ec0a99a4cfccd6a46993c208ae1a0f` |
| `campaign6.log` | 8696 | `70ab6ec445360e1d6a6ed439fb45db9ce6a7138b05aed3b94c32e770677f22c5` |
| `campaign7.log` | 8506 | `38f16fac279b91d339db8cf724cb2dfbad9bbf0eed86a198f5b9d5e4552f5268` |
| `coverage-all.log` | 2884 | `a0afd2e148e655ea4527c7533e28ceff0d1e30844708123603e6babd130be530` |
| `coverage-final.log` | 3007 | `93083b08fc27c73a9fd6ec88522fa4cbbf60d75a0c22d1f76e2a22a5bb655ca9` |
| `differential-final.log` | 40001 | `9a3fcf86955ce6a55d63cc9d4b2d33be1ee0c537263e8c26309d66b32f5a5408` |
| `export.json` | 165 | `d904bcba5d8210387d37cd2700871d56ffa4d26c2551313e8d6f038b59ceaf5e` |
| `export.tar` | 33546240 | `33889fab960addb52652f2240b675c488e26a7c0b824ca0549e66450ea286709` |
| `final-seams.log` | 9738 | `cdc1bd663185a1356dc52ce62a6baca19bdb32bc7c646f8f5e4c62ea852ec8f3` |
| `firmware-nvm.log` | 3549 | `d60a249e5af72d96171e30fab017700d9b58610eb1e70fda3cd606c3114f9513` |
| `ft-selftests.log` | 5755 | `446408aa2f4add65d557aa675d47cd20f623bfb4607614543e19b353546897cf` |
| `gate_bank.py` | 1333 | `e7c3cb0d9bc3dc7a8a3afb0d379c2f1a3f82924f638be8fd9b580a6f10243ddd` |
| `gptp-processor.tar` | 4024320 | `faecd44e56a1ae439ba4b12fa7c8c973c7e3c981e75fd26c6f5c6d93bdab4bf0` |
| `ignore_destination.log` | 2477 | `7217a7b65ea7faa22f4eab8348cd0ecc42590e9322ed1779c83bd80a034524a6` |
| `mbx-cosim-if2.log` | 23700 | `86e1d77a4b4239657ad9f134aa29e56635816a85262d1b90da0af4ae6a35e16f` |
| `mbx-job-option.log` | 99 | `235b6acb4481a92d87f1af27101c107d2a1b4cca59aef9b234abd095b3eb9fe2` |
| `mbx-make.json` | 391 | `cc774e882366835b5e9feee10dd1fa5f9084b58cde30babaaad314d58667532e` |
| `mbx-mutants.log` | 668 | `ac426917a9f4ea12b93cb77e929914f65be99dc8033df544bd8f677593e099c1` |
| `mbx-wb-axil.log` | 11643 | `4379f29aa0aa6f85f0e7bc198e49f8f172ba29de28547ed14d9850083f912594` |
| `profile-absent-0.audit.jsonl` | 1909 | `25545d12c9428da63089cd33c9aa3698b39da22da02d7f76f0ea7f5bd2631cd0` |
| `profile-absent-0.json` | 23977 | `1de8e5342cc63588359dc449d25a8656b02a492b2409e86ff8b839d9dccb11fb` |
| `profile-absent-0.log` | 49367 | `a16a541dbbf76c5f875a67509ee05a062e53e34e22440d4f8be90bb15af4c3d5` |
| `profile-absent-1.audit.jsonl` | 1909 | `edbd23bdaa7cf46b0097bcd6cd49dbb4d58c5b1c3ce5df57544f3bbbd5d27b17` |
| `profile-absent-1.json` | 23973 | `e5a9c63d13e2ef57b5b1b91964ddee4ef498ba6139e153fc2b273d4c1992e40b` |
| `profile-absent-1.log` | 49261 | `e9fa692442b6079ee435f15583fb8dc1edd83ee3fdb335b0e1a6d14a2262b402` |
| `profile-absent-2.audit.jsonl` | 1909 | `77679dd813f369f8112d30476fd884247f6f12a0c13c9e4ad182c1f16b68fbd7` |
| `profile-absent-2.json` | 23977 | `2cd6c1fbde8ee4e395b9d724962e1c24df813b25cfc1c5c39fc007a2f886da50` |
| `profile-absent-2.log` | 49253 | `d65697a6bbe10e0471a95fe3fa594d7d4c569f3facf0b80bc44708fe82f2e2a1` |
| `profile-absent-3.audit.jsonl` | 1909 | `1090d00b2a1961ae6f10402b100560848a0f7b08dfdb5d2c7374eb2bc93a75ed` |
| `profile-absent-3.json` | 23972 | `cf386fc0552e9d6a5cd4100b09722538d6dd567547f4d7f3cbdad285611c26f8` |
| `profile-absent-3.log` | 49238 | `fa169a83cb963e662c76620ce06cbe0cdc215184736538573bc321f64446503d` |
| `profile-complete.json` | 1529 | `1657ced9dffe6434e2871f3b31da9e8b5bcd2eb5af2f3e72fb295982876a71de` |
| `profile-sdk-0.audit.jsonl` | 1459529 | `c3e0505fbbc9373e68b28b76eab7a63eb87923fe5280aa416638efa8a825fc08` |
| `profile-sdk-0.json` | 33040 | `5c2810d00cf69fd4bc90b026e21dc4c04fcf9ff211b59e92c001bfb512a0ebb6` |
| `profile-sdk-0.log` | 51167 | `5af3238b49168a28c6adbeb7df59526921204222515577cb90a2e85cff77c09d` |
| `profile-sdk-1.audit.jsonl` | 1480547 | `82c9465341254f7eaf3564079fda0b11a54ddb3e37984a2512447e3b083e0cde` |
| `profile-sdk-1.json` | 33040 | `cb3d4afdcf911b6dfcf3eb54caae8e9f516734c04e8e993cc940096b8a4f4736` |
| `profile-sdk-1.log` | 51166 | `59a65d3ce8ed6c4ceeeb6022b054c35ebe33ea6b8223e9dd4a7ea6ad38ddc5b2` |
| `profile-sdk-2.audit.jsonl` | 1466741 | `5834a762a3170ab08ef32bbf2b9be34ddb614f053446d68cae7f89ecaac976d3` |
| `profile-sdk-2.json` | 33035 | `c2d50f50dc2d538bc849ae19bac24500270858c47d66a677fb058adb745fff77` |
| `profile-sdk-2.log` | 51171 | `24769a81b828bbfe25615ba84ec69bd5f78ef90a2ffe935f71ed618134e45874` |
| `profile-sdk-3.audit.jsonl` | 1433827 | `cc5e1d1b509d46797c80c05efbdb7f011994c4a0dfb93e26d7a647005500edc3` |
| `profile-sdk-3.json` | 33030 | `5c71c8d29191387e3e2412148c362b1a4fbad46f2ff882bc522663d9a26a7f5a` |
| `profile-sdk-3.log` | 51051 | `7d1ec590eee1bf67f45ee4af3423f0be6df717783f911e06d4ab621dfb4d2393` |
| `profile_shard.py` | 2269 | `50ce6f6730fbb6c913911f6eb8ead51365b7a1b28f5223b2c0a2297eb16fb23a` |
| `protocol-processor.tar` | 12349440 | `1807151ad43ae81c8ff75f4f0b95242bb6e3c5271c2dbf357ceef8d4ad9e5e61` |
| `reject_all_destinations.log` | 7406 | `eb2ce09eec00f0a205d56ac5aad3dd1c21715398c4717baab586f824ffd86297` |
| `third_party-verilog-axis.tar` | 1843200 | `0d0eb5b826cdbd3e21900ef68fb2dc6eb8af44f1e84c1e462df2999467c7c344` |
| `verify_profiles.py` | 1827 | `97c0ed2bafdf96125cc71e24478cbb76b49182e42ff73766f97ccd2f15f0c169` |
| `final-state.json` | 245 | `88983695b2b836cccabe140abf7f24e304c44681987b1c8500ded8be18d1b5c9` |

Final hygiene: tracked and ignored source-tree state clean, including all three
initialized submodules. No build products remain in the source tree. Observed
service memory peak: 8967770112 bytes (below 9 GB); final current:
2856083456 bytes. Final free space on the data volume:
142413291520 bytes (above the 30 GB floor).
