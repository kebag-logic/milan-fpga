# [A570] Issue #696 handoff

## Round 14: merge the shared-stack candidate: REVIEW READY

Assignment: issue #696 comment 6148294623. Starting head: `313616d1a18549d41907db389d378f0beb9bc543`.
The origin URL and starting head match the resume instruction. The worktree starts clean.
The requested input is PR #705 head `d40e4e9827be2516f8f34b9d65f0a483fff2194c`.
Fetched head verified exactly. Merge committed as `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd`, tree `295aadcc963e941f2fcc97b27d497aa787da0d86`. All final Round 14 validation commands passed; one boundary environment refusal was corrected and rerun without changing source. The ordered parents are the starting head and the requested shared-stack head.
REVIEW READY was posted as a new comment and read back byte-identical: https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6152831020.

Until #705 merges, PR #706's diff shows the imported 697c commits.
No additional dev merge is authorized in this round. No push is authorized.

| Change | Location | Status |
|---|---|---|
| Shared stack pin and stack-built C core plus Annex B differential | `sw/firmware/ctrl/test/maap_differential.py:23` | Resolved and committed |

| Gate | Round 13 total | Round 14 |
|---|---:|---|
| MAAP clean checks | 186 | 186, zero failures, rc 0 |
| MAAP campaign | 63 rejected defects, 2 clean controls | Identical totals; zero failures, rc 0 |
| Datapath integration | 5 | 5, zero failures, rc 0 |
| Line coverage | 225/225 | 225/225 eligible lines; rc 0 |
| Differential | 12 cases, 17 rejected defects | 12 clean cases; 17/17 rejected defects; rc 0 |
| Firmware parent campaign | 506/506 rejected defects | 506/506; full firmware command rc 0 |
| Store gate | Not separately recorded | 435 tests across 5 shapes; rc 0 |
| Coverage self-test | Not separately recorded | 29/29 planted cases; rc 0 |
| Firmware coverage | Not separately recorded | 30 files pass after declared exclusions; rc 0 |
| Shared-stack boundary | Not separately recorded | 117 boundary, 120 pin and 4 figure controls; zero findings/misbehavior; rc 0 after environment correction |
| Other merge-touched suites | See prior round | All seven selected suites: 38,218 checks, unchanged; all final command results rc 0 |
| Static checks | 28 commands | 28 commands, rc 0 |
| Parser ratchet | 0 findings | 0 findings, rc 0 |
| MAAP OOC | 446 LUT / 340 FF | 446 LUT / 340 FF; +7 / +60 against base; rc 0 |
| Shipping route | 49,277 LUT / 53,419 FF; WNS +0.242 ns; WHS +0.017 ns | Identical figures; complete route; rc 0 |
| Two standalone endpoints | Both passed | 1×1: 23,179 LUT / 19,779 FF; 8×8: 30,135 LUT / 27,380 FF; both rc 0 |

| Lens | Covering round | Head |
|---|---|---|
| Conformance | Pending independent review | Pending |
| RTL | Pending independent review | Pending |
| Robustness | Pending independent review | Pending |
| Tests | Pending independent review | Pending |
| Docs | Pending independent review | Pending |

This section is author evidence. All resource commands and three `record --write` calls passed. The 251 measured input-file checks are unchanged; all final simulation and firmware commands passed. Exact commands and final totals follow.

### Round 14 default-suite totals

The repository tally reader reports identical totals in all seven selected suites. MAAP includes its 65 campaign checks. Integration, coverage, the differential and firmware campaigns are listed separately above; they are not added twice to this total.

| Suite | Round 13 | Round 14 | Delta |
|---|---:|---:|---:|
| `maap` | 251 | 251 | 0 |
| `milan_dp` | 11,956 | 11,956 | 0 |
| `mbx` | 2,123 | 2,123 | 0 |
| `pp_shadow` | 2,184 | 2,184 | 0 |
| `capture_coherence` | 21,194 | 21,194 | 0 |
| `milan_dp_mclk` | 168 | 168 | 0 |
| `milan_dp_render` | 342 | 342 | 0 |
| **Total** | **38,218** | **38,218** | **0** |

### Round 14 boundary environment refusal

The first boundary capture exited 2 because its interpreter lacked `migen` when invoking `sw/litex/test_ctrl_memory.py --build-only`. The preceding RV32, firmware, store and coverage-builder captures exited 0. No repository source changed. The refusal is preserved under `round14-receipts/attempts/boundary-docenv.*`; the corrected run used the existing build interpreter and passed with rc 0. Its result is recorded separately from the original command-chain status.

### Round 14 resolution and imported paths

Only `sw/firmware/ctrl/test/maap_differential.py` conflicted, in four hunks.
The combined signature at :23 accepts the shared stack and optional RTL source.
At :27 the C object comes from the selected stack; :33 keeps object/library link order.
At :50 the campaign accepts the proven pin, and :75 copies that stack for C plants.
At :80 the RTL plant still selects its separate source; :89 builds it together with the stack.
At :92 detection still requires the named MAC/phase assertion. At :107 both command modes run the shared pin proof before building.
The auto-merged MAAP README keeps its stack-core attribution and pin refusal text alongside the Annex B account.
A separate merge-tree reconstruction gives the unresolved tree `63a94f32238ef4ec2319b3e545bcd418aa168d63`; exactly the differential differs from that tree.
No other imported file is changed by hand. The merge imports the requested candidate's mailbox-header include move; it makes no new mailbox behavior or register-map change.

All imported paths are listed below. Deleted paths cite the first removed line in the first parent. Other line references are at the merged head.

| Imported artifact | Source |
|---|---|
| `.github/workflows/rtl-fast.yml:314` (M) | Requested shared-stack candidate |
| `.github/workflows/rtl.yml:161` (M) | Requested shared-stack candidate |
| `.gitmodules:16` (M) | Requested shared-stack candidate |
| `CONTRIBUTING.md:384` (M) | Requested shared-stack candidate |
| `QUICKSTART.md:157` (M) | Requested shared-stack candidate |
| `README.md:191` (M) | Requested shared-stack candidate |
| `THIRD_PARTY.md:21` (M) | Requested shared-stack candidate |
| `docs/design/MAILBOX_SPLIT.md:7` (M) | Requested shared-stack candidate |
| `docs/diagrams/PNG_MANIFEST.json:11` (M) | Requested shared-stack candidate |
| `docs/diagrams/submodule_boundaries.drawio:1` (M) | Requested shared-stack candidate |
| `docs/diagrams/submodule_boundaries.gen.py:43` (M) | Requested shared-stack candidate |
| `docs/diagrams/submodule_boundaries.png:1` (M) | Requested shared-stack candidate |
| `docs/diagrams/submodule_boundaries.svg:1` (M) | Requested shared-stack candidate |
| `docs/reference/SUBMODULES.md:27` (M) | Requested shared-stack candidate |
| `docs/testing/CI_WORKFLOWS.md:59` (M) | Requested shared-stack candidate |
| `scripts/act_ci.py:234` (M) | Requested shared-stack candidate |
| `scripts/check_submodule_docs.py:31` (M) | Requested shared-stack candidate |
| `scripts/ci_events.py:569` (M) | Requested shared-stack candidate |
| `scripts/ci_scope.py:27` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/README.md:13` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/acmp/acmp.c:1` (D) | Requested shared-stack candidate |
| `sw/firmware/ctrl/acmp/acmp.h:1` (D) | Requested shared-stack candidate |
| `sw/firmware/ctrl/adp/adp.c:1` (D) | Requested shared-stack candidate |
| `sw/firmware/ctrl/adp/adp.h:1` (D) | Requested shared-stack candidate |
| `sw/firmware/ctrl/aecp/README.md:141` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/maap/README.md:19` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/maap/maap.c:1` (D) | Requested shared-stack candidate |
| `sw/firmware/ctrl/maap/maap.h:1` (D) | Requested shared-stack candidate |
| `sw/firmware/ctrl/mbx/mbx_wire.h:8` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/acmp_fake.hpp:1` (D) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/acmp_mutants.py:15` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/acmp_review_mutants.py:15` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/aecp_arms.py:6` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/aecp_mutants.py:14` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/aecp_wire.py:2` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/aecp_wire_model.hpp:4` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_arms.py:15` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_boundary.py:1` (A) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_build.py:11` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_capture.py:1` (A) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_configs.py:1` (A) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_expand.py:1` (A) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_image.py:49` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_mutant.py:10` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_mutants.py:5` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_pin.py:1` (A) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_pin_bench.py:1` (A) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_pin_env.py:1` (A) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_pin_store.py:1` (A) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_plants.py:1` (A) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_runs.py:1` (A) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_shim.py:1` (A) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/ctrl_srp_image.py:11` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/maap_differential.py:4` (M) | Conflict resolution, both parents |
| `sw/firmware/ctrl/test/maap_mutants.py:8` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/srp_arms.py:8` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/test_acmp.cpp:1` (D) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/test_adp.cpp:7` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/test_adp_reentry.cpp:1` (D) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:8` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/test_maap.cpp:3` (M) | Requested shared-stack candidate |
| `sw/firmware/ctrl/test/test_maap_debug.cpp:1` (D) | Requested shared-stack candidate |
| `sw/firmware/ctrl/wire/wire.h:1` (D) | Requested shared-stack candidate |
| `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py:36` (M) | Requested shared-stack candidate |
| `sw/firmware/gtest/README.md:176` (M) | Requested shared-stack candidate |
| `sw/firmware/gtest/coverage.ratchet:4` (M) | Requested shared-stack candidate |
| `sw/firmware/gtest/fw_coverage.py:7` (M) | Requested shared-stack candidate |
| `sw/firmware/gtest/fw_coverage_selftest.py:109` (M) | Requested shared-stack candidate |
| `sw/firmware/gtest/fw_gtest.py:18` (M) | Requested shared-stack candidate |
| `sw/firmware/gtest/fw_gtest_label.cpp:1` (A) | Requested shared-stack candidate |
| `sw/litex/ctrl_memory_probe.py:1` (A) | Requested shared-stack candidate |
| `sw/litex/test_ctrl_memory.py:53` (M) | Requested shared-stack candidate |
| `tb/verilator/mbx/Makefile:50` (M) | Requested shared-stack candidate |
| `tb/verilator/mbx/README.md:16` (M) | Requested shared-stack candidate |
| `tb/verilator/milan_dp/Makefile:34` (M) | Requested shared-stack candidate |
| `tb/verilator/milan_dp/stream_counter_f5.py:17` (M) | Requested shared-stack candidate |
| `third_party/tsn-c-stack:1` (A) | Requested shared-stack candidate |

### Round 14 test-to-defect coverage

These unchanged checks were rerun at the merged head: all 63 planted defects were rejected, and both clean controls passed. A rejection requires the designated assertion and exit 1; build failures never count. The differential also passed all 12 clean cases and 17 named rejections. All final merge-touched gate commands also exited 0.

| Item | Scope | Test assertion | Planted defect |
|---|---|---|---|
| M3 | unit | M3 B.3.6.1 generator period is 2^32-1 | `m3_short_period` |
| M3 | unit | M3 B.3.6.1 generator period is 2^32-1 | `m3_trap_outside_basis` |
| M3 | unit | M3 B.3.6.1 first enable seeds MAC plus clock | `m3_ignores_clock` |
| M3 | unit | M3 B.3.6.1 first enable seeds MAC plus clock | `m3_xors_clock` |
| M3 | unit | M3 Release/Begin retains the generator sequence | `m3_reseeds_after_release` |
| M3 | unit | M3 B.3.6.1 clocks 2^k apart claim different first offsets | `m3_first_offset_ignores_clock` |
| M4 | unit | M4 B.3.6.1 adjacent MACs claim disjoint first blocks | `m4_first_offset_ignores_seed` |
| M4 | unit | M4 B.3.6.1 adjacent MACs claim disjoint first blocks | `m4_first_offset_raw_seed_bits` |
| M4 | unit | M4 B.3.6.1 MACs 2^i apart (16 <= i <= 31) claim disjoint first blocks | `m4_first_offset_drops_seed_high_half` |
| M4 | unit | M4 B.3.4 MACs 2^i apart draw different first probe intervals | `m4_first_interval_raw_seed_bits` |
| M4 | unit | M4 B.3.6.1 seed bits 16..31 map one-to-one onto the first offset word | `m4_offset_row0_bit_drop` |
| M4 | unit | M4 B.3.6.1 every seed pair 2^i apart claims disjoint first blocks of 1..8 | `m4_offset_row6_bit_drop` |
| M4 | unit | M4 B.3.4 every seed pair 2^i apart draws different first probe intervals | `m4_probe_fold_unstepped` |
| M4 | unit | M4 first-draw maps learned from the RTL are linear in the seed | `m4_first_offset_nonlinear` |
| M4 | unit | M4 B.3.6.1 first offset word and first probe draw are independent | `m4_probe_row_repeats_offset_row` |
| M6 | unit | M6 occupied response buffer preserves active DEFEND | `m6_overwrite_active_response` |
| M6 | unit | M6 pending response preserves prober and requested range | `m6_replace_pending_response` |
| M6 | unit | M6 pending response cancelled with allocation | `m6_pending_survives_release` |
| M6 | unit | M6 busy PROBE gets DEFEND after wire is free | `m6_drop_busy_probe` |
| M6 | unit | M6 pending response preserves prober and requested range | `m6_pending_source_not_saved` |
| M5 | unit | M5 B.3.5.9 link return revokes and reprobes | `m5_ignore_link_return` |
| M5 | unit | M5 B.3.5.9 link return restarts PROBE | `m5_level_restarts` |
| M5 | unit | M5 B.3.5.9 link loss is no event; return reprobes | `m5_restart_on_link_loss` |
| M1 | unit | M1 rProbe/PROBE lower MAC keeps range | `m1_probe_no_compare` |
| M1 | unit | M1 rDefend/DEFEND lower MAC keeps range | `m1_defend_no_compare` |
| M8 | unit | M8 B.2 truncated PROBE-state input has no effect | `m8_early_last_accepted` |
| M8 | unit | M8 B.2 truncated DEFEND-state input has no effect | `m8_missing_bytes_accepted` |
| M7 | unit | M7 Table B.9 invalid supplied range refused | `m7_accept_invalid_seed` |
| M7 | unit | M7 Table B.9 valid supplied boundary retained | `m7_reject_valid_boundary` |
| M2 | unit | M2 B.3.6.6 requested start echoes PROBE | `m2_own_requested_start` |
| M2 | unit | M2 B.3.6.6 requested start echoes a PROBE starting below ours | `m2_echo_overlap_start` |
| M2 | unit | M2 B.3.6.6 requested count echoes all 16 bits | `m2_own_requested_count` |
| 1 | unit | B.2.1 cdl 16 (Begin! PROBE 1) | `cdl_28` |
| 1 | unit | B.2.1 DEFEND DA = PROBE source (above) | `defend_to_multicast` |
| 1 | unit | B.2.1 DEFEND DA latched at send | `defend_destination_not_latched` |
| 1 | unit | B.2.1 PROBE DA multicast (Begin! 1) | `every_frame_to_the_prober` |
| 2 | unit | B.3.4.2 probe T < 600 ms (campaign) | `probe_draw_7_bits` |
| 2 | unit | B.3.4.2 probe T > 500 ms (campaign) | `probe_base_500` |
| 2 | unit | B.3.4.1 announce T > 30 s | `announce_base_3s` |
| 2 | unit | B.3.4.1 announce T < 32 s | `announce_draw_11_bits` |
| 2 | unit | B.3.4.1 announce T randomized | `announce_not_randomized` |
| 2 | unit | B.3.4.2 probe T randomized (zero-seed MAC) | `zero_seed_freezes_the_probe_draw` |
| 2 | unit | B.3.4.1 announce T randomized (zero-seed MAC) | `zero_seed_freezes_the_announce_draw` |
| 3 | unit | B.2.7 ANNOUNCE conflict_* is not its range | `announce_judged_on_conflict_fields` |
| 3 | unit | note b adjacent above: no conflict | `inclusive_range_end` |
| 3 | unit | note b adjacent below: no conflict | `inclusive_range_start` |
| 3 | unit | note b empty range: no conflict | `empty_range_conflicts` |
| 3 | unit | T.B7 note d: lower MAC keeps range | `no_compare_mac` |
| 3 | unit | T.B7 rAnnounce!/PROBE: no compare_MAC | `compare_mac_while_probing` |
| 3 | unit | T.B7 rAnnounce!/DEFEND: re-address | `compare_mac_unreversed` |
| 4 | unit | T.B7 Begin!: four PROBEs before ANNOUNCE | `three_probes` |
| 4 | unit | T.B7 Begin!: first PROBE at once | `first_probe_after_a_timer` |
| 4 | unit | T.B7 Restart!: first PROBE at once | `restart_probe_after_a_timer` |
| 4 | unit | T.B7 probeCount!: ANNOUNCE at once (Begin!) | `announce_after_a_timer` |
| 0 | unit | frame on the wire keeps its offset | `restart_rewrites_the_frame_on_the_wire` |
| 0 | unit | B.2.8 conflict_count = overlap (below) | `overlap_count_to_our_end` |
| 0 | unit | PROBE mid-frame: frame on the wire byte-identical | `defend_rewrites_the_frame_on_the_wire` |
| 0 | unit | note b: this station's empty range never conflicts | `own_empty_range_conflicts` |
| M4 | datapath | M4 datapath: programmed MAC changes probe intervals | `m4_reset_time_sampling` |
| M5 | datapath | M5 datapath: link return starts four fresh PROBEs | `m5_datapath_ignores_link` |
| M3 | datapath | M3 datapath: real-time clock changes probe intervals | `m3_datapath_ignores_clock` |
| M4 | datapath | M4 datapath: fixed adjacent MAC pair claims disjoint first blocks | `m4_datapath_first_offset_ignores_seed` |
| M3 | datapath | M3 datapath: fixed PHC time pair claims different first offsets | `m3_datapath_first_offset_ignores_clock` |

The differential separately grades 12 clean cases and 17 controls: `wire` (CDL 28), `release` (stay in DEFEND), all nine `maap-table-b7-*` conflict cells, `probe-1ms`, `probe-500ms`, `probe-600ms`, `parent-probe-bound`, `parent-probe-count`, and `parent-ignores-mac`. The last still requires the named MAC/phase coverage failure, not merely a failing process. The shared boundary self-test covers refusing edited or off-pin stacks before either differential mode builds.

### Round 14 differential rejection ledger

All rows below passed at the merged head. Source: `sw/firmware/ctrl/test/maap_differential.py:50`; the conflict-cell plants are defined at `sw/firmware/ctrl/test/maap_mutants.py:233`.

| Plant | Test that must reject it | Defect |
|---|---|---|
| `wire` | `MaapDifferential.ProbeSequenceWireAndCadence` | C core emits CDL 28 |
| `release` | `MaapDifferential.ReleaseAndRetry` | Release leaves the C core in DEFEND |
| `maap-table-b7-0` | `AllStates/DifferentialCell.SharedConflict/0` | Invent restart in INITIAL on PROBE |
| `maap-table-b7-1` | `AllStates/DifferentialCell.SharedConflict/1` | Invent restart in INITIAL on DEFEND |
| `maap-table-b7-2` | `AllStates/DifferentialCell.SharedConflict/2` | Invent restart in INITIAL on ANNOUNCE |
| `maap-table-b7-6` | `AllStates/DifferentialCell.SharedConflict/3` | Suppress required action in PROBE on PROBE |
| `maap-table-b7-7` | `AllStates/DifferentialCell.SharedConflict/4` | Suppress required action in PROBE on DEFEND |
| `maap-table-b7-8` | `AllStates/DifferentialCell.SharedConflict/5` | Suppress required action in PROBE on ANNOUNCE |
| `maap-table-b7-12` | `AllStates/DifferentialCell.SharedConflict/6` | Suppress required action in DEFEND on PROBE |
| `maap-table-b7-13` | `AllStates/DifferentialCell.SharedConflict/7` | Suppress required action in DEFEND on DEFEND |
| `maap-table-b7-14` | `AllStates/DifferentialCell.SharedConflict/8` | Suppress required action in DEFEND on ANNOUNCE |
| `probe-1ms` | `MaapDifferential.ProbeTimingAndCount` | C core fixes the interval at 1 ms |
| `probe-500ms` | `MaapDifferential.ProbeTimingAndCount` | C core fixes the interval at 500 ms |
| `probe-600ms` | `MaapDifferential.ProbeTimingAndCount` | C core fixes the interval at 600 ms |
| `parent-probe-bound` | `MaapDifferential.ProbeTimingAndCount` | Parent upper-bound oracle incorrectly requires <500 ms |
| `parent-probe-count` | `MaapDifferential.ProbeTimingAndCount` | Parent oracle expects only four total frames |
| `parent-ignores-mac` | `MaapDifferential.ProbeTimingAndCount` | RTL replaces MAC plus clock with a constant; rejection must name MAC/phase draw coverage |

### Round 14 final command ledger

All final commands below exited 0. The original boundary environment refusal is retained separately; it is not erased by the corrected run. `$WORK` is disk-backed scratch, `$BUILD_ENV` is the installed build environment, `$DOC_ENV` is the documentation environment, and `$SYNTHESIS_INSTALL`/`$SYNTHESIS_LOCK` identify the synthesis installation and exclusive lock. Commands run from the candidate root unless their JSON record gives another working directory. The full argument vectors and durations are in the receipts.

| Validation command | rc | Evidence |
|---|---:|---|
| `python3 scripts/lint_rtl.py --check --self-test --jobs 2` | 0 | `round14-receipts/validation/lint.json` |
| `make -j8 -C tb/verilator/maap MDIR=$WORK/validation/unit` | 0 | `round14-receipts/validation/maap.json` |
| `make -j8 -C tb/verilator/maap integration-build DP_MDIR=$WORK/validation/integration` | 0 | `round14-receipts/validation/maap-integration-build.json` |
| `$WORK/validation/integration/maap_integration` | 0 | `round14-receipts/validation/maap-integration.json` |
| `make -j8 -C tb/verilator/maap coverage COV_MDIR=$WORK/validation/coverage` | 0 | `round14-receipts/validation/maap-coverage.json` |
| `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep $WORK/validation/differential` | 0 | `round14-receipts/validation/maap-differential.json` |
| `make -j8 -C tb/verilator/milan_dp` | 0 | `round14-receipts/validation/milan_dp.json` |
| `make -j8 -C tb/verilator/mbx` | 0 | `round14-receipts/validation/mbx.json` |
| `make -j8 -C tb/verilator/pp_shadow` | 0 | `round14-receipts/validation/pp_shadow.json` |
| `make -j8 -C tb/verilator/capture_coherence` | 0 | `round14-receipts/validation/capture_coherence.json` |
| `make -j8 -C tb/verilator/milan_dp_mclk` | 0 | `round14-receipts/validation/milan_dp_mclk.json` |
| `make -j8 -C tb/verilator/milan_dp_render` | 0 | `round14-receipts/validation/milan_dp_render.json` |
| `bash syn/yosys/run.sh --results $WORK/validation/portability-results` | 0 | `round14-receipts/validation/portability.json` |
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 2` | 0 | `round14-receipts/validation/firmware.json` |
| `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 2` | 0 | `round14-receipts/validation/store.json` |
| `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | `round14-receipts/validation/coverage-selftest.json` |
| `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 2` | 0 | `round14-receipts/validation/firmware-coverage.json` |
| `$BUILD_ENV/bin/python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest` | 0 | `round14-receipts/validation/boundary.json` |
| `$BUILD_ENV/bin/python3 sw/litex/test_ctrl_memory.py` | 0 | `round14-receipts/validation/control-memory.json` |
| `python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py` | 0 | `round14-receipts/validation/firmware-shards.json` |
| `python3 sw/builder/test_builder.py --require-rv32 --require-elaboration` | 0 | `round14-receipts/validation/builder.json` |
| `python3 -m behave --no-capture -f plain` | 0 | `round14-receipts/validation/behaviour.json` |

The builder command explicitly leaves historical estimator-calibration gate 11 **NOT RUN** because its old reference report is absent, exactly as in Round 13. No required elaboration arm was skipped. This unchanged arm is not counted as covered.

| Static command | rc |
|---|---:|
| `$DOC_ENV/bin/python3 scripts/docs_check.py` | 0 |
| `$DOC_ENV/bin/python3 scripts/check_doc_style.py` | 0 |
| `$DOC_ENV/bin/python3 scripts/check_doc_paths.py` | 0 |
| `$DOC_ENV/bin/python3 scripts/gen_toc.py --check` | 0 |
| `$DOC_ENV/bin/python3 scripts/gen_toc.py --verify-anchors` | 0 |
| `$DOC_ENV/bin/python3 scripts/check_em_dash.py --base e81ce82f` | 0 |
| `$DOC_ENV/bin/python3 scripts/check_baremetal_only.py --check` | 0 |
| `$DOC_ENV/bin/python3 scripts/check_sv_idiom.py` | 0 |
| `$DOC_ENV/bin/python3 scripts/check_cpp_idiom.py` | 0 |
| `$DOC_ENV/bin/python3 scripts/check_py_idiom.py` | 0 |
| `$DOC_ENV/bin/python3 scripts/check_sh_idiom.py` | 0 |
| `$DOC_ENV/bin/python3 scripts/check_hygiene.py --check` | 0 |
| `$DOC_ENV/bin/python3 scripts/measure_test_evidence.py --check` | 0 |
| `$DOC_ENV/bin/python3 scripts/measure_fail_fast.py --check` | 0 |
| `$DOC_ENV/bin/python3 scripts/measure_naming.py --check` | 0 |
| `$DOC_ENV/bin/python3 scripts/check_todo_ownership.py` | 0 |
| `$DOC_ENV/bin/python3 scripts/check_port_contracts.py` | 0 |
| `$DOC_ENV/bin/python3 scripts/check_soc_sources.py` | 0 |
| `$DOC_ENV/bin/python3 scripts/check_rtl_source_lists.py` | 0 |
| `$DOC_ENV/bin/python3 scripts/ci_events.py --check` | 0 |
| `$DOC_ENV/bin/python3 scripts/ci_events.py --selftest` | 0 |
| `$DOC_ENV/bin/python3 scripts/ci_scope.py --selftest` | 0 |
| `$DOC_ENV/bin/python3 scripts/suite_shards.py --selftest` | 0 |
| `$DOC_ENV/bin/python3 scripts/check_feature_status.py --self-test` | 0 |
| `$DOC_ENV/bin/python3 scripts/check_submodule_docs.py` | 0 |
| `$DOC_ENV/bin/python3 scripts/pp_srcs.py --check --selftest` | 0 |
| `$DOC_ENV/bin/python3 docs/traceability/gen_module_matrix.py --check` | 0 |
| `$DOC_ENV/bin/python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 |

| Resource command | rc |
|---|---:|
| `flock $SYNTHESIS_LOCK $SYNTHESIS_INSTALL/bin/vivado -mode batch -source run.tcl -nojournal -log baseline.log` | 0 |
| `flock $SYNTHESIS_LOCK python3 scripts/xvlog_gate.py --check` | 0 |
| `flock $SYNTHESIS_LOCK $SYNTHESIS_INSTALL/bin/vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log` | 0 |
| `python3 syn/ooc/pp_resource_gate.py check $WORK/shipping-candidate/ax7101/gateware --endpoint route-1x1` | 0 |
| `flock $SYNTHESIS_LOCK $SYNTHESIS_INSTALL/bin/vivado -mode batch -source rtl.tcl -nojournal -log baseline.log` | 0 |
| `python3 syn/ooc/pp_baseline.py $WORK/shipping-candidate/ax7101/gateware --single-thread-synthesis --integrated-clock --output $WORK/shipping-candidate/ax7101-ooc --integrated-log $WORK/shipping-candidate/ax7101/gateware/baseline.log` | 0 |
| `flock $SYNTHESIS_LOCK $SYNTHESIS_INSTALL/bin/vivado -mode batch -source baseline_ooc.tcl -nojournal -log baseline.log` | 0 |
| `python3 syn/ooc/pp_resource_gate.py check $WORK/shipping-candidate/ax7101-ooc --endpoint ooc-1x1` | 0 |
| `python3 syn/ooc/pp_baseline.py $WORK/shipping-candidate/ax8x8/gateware --single-thread-synthesis --integrated-clock --output $WORK/shipping-candidate/ax8x8-ooc --integrated-log $WORK/shipping-candidate/ax8x8-rtl/baseline.log` | 0 |
| `flock $SYNTHESIS_LOCK $SYNTHESIS_INSTALL/bin/vivado -mode batch -source baseline_ooc.tcl -nojournal -log baseline.log` | 0 |
| `python3 syn/ooc/pp_resource_gate.py check $WORK/shipping-candidate/ax8x8-ooc --endpoint ooc-8x8` | 0 |

Three recipe records were written through `pp_resource_gate.py record --write --baseline $WORK/measurement-policy.json`, one each for `route-1x1`, `ooc-1x1`, and `ooc-8x8`; all rc 0. Exact argument vectors are in `round14-receipts/recorded/*.command.json`. The repository baseline remains unchanged under D7.

The canonical seven-suite tally and all seven log-verdict checks exited 0. `round14-receipts/validation/suite-tally.log`, `suite-comparison.json`, and `validation-summary.json` record the 38,218 checks, zero failures and no unparsed or skipped tally rows. This is the scoped Round 14 bank; Round 13's 62-suite sweep remains prior-head evidence.

### Round 14 additional coverage and final state

| Gate | Result and defects checked |
|---|---|
| Boundary | 3,107 compiled sources from 3,365 recorded invocations; 117 boundary, 120 pin and 4 figure controls; zero findings/misbehavior. Controls catch non-public headers, heap/OS calls, compiler-input omissions, unpinned builders, edited/off-pin stack input, and false README counts. Both differential command modes are included in the pin census. |
| Control memory | 44 planted defects caught; zero failures. Checks cover memory origins, region sizes, decode holes, ROM contents/protection, BIOS exclusions, and firmware/staging bindings. |
| Firmware sharding | 916 invocations, exactly one shard each; sizes 60/507/77/272, identical to Round 13. Missing/duplicate suite plants and nine invalid shard combinations are rejected. |
| Builder | rc 0; required elaborations executed. Contract, generated image, memory-budget, routing, clock and binding plants are rejected; historical calibration gate 11 remains explicitly not run. Named checks and plants appear in the bounded builder excerpts. |
| Behavior | 14 features, 406 scenarios, 1,977 steps; zero failed/skipped, identical to Round 13. |
| Portability | 58/58 tops pass; no unjustified ties; observer negative fixtures detected and final stream bindings clean. |

Final integrity: head `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd`, ordered parents and tree verified; ten protected blobs still match the first parent; all 251 measured input-file checks unchanged. Both worktrees and all ten initialized submodule checkouts are clean. The three temporary recipe links were removed after the input recheck; their original targets are retained in `final-integrity.json`. Twelve generated binary/checkpoint identities are recorded by size and SHA-256 without copying those files into the packet.

Resource envelope: kernel peak 8,899,997,696 bytes (below 9 GB); lowest sampled free space 40,456,912,896 bytes (37.68 GiB); zero OOM or OOM-kill events. No synthesis run overlapped the native bank; synthesis used the exclusive lock and the single-thread synthesis recipe. Inactive Round 13 generated build directories were retired to maintain disk headroom, preserving tracked source, logs and reports.

Acceptance items 1–3 are met under the recorded issue rulings. Item 4 remains assigned to the separate post-merge bench lane. No new unresolved technical decision is introduced. Independent review of this merge head, publication, hosted gates, final dev-merge validation and post-merge containment remain pending. No push, PR edit, additional dev merge or hardware operation was performed.

Small sanitized receipts and bounded result excerpts are in `round14-receipts/`. Larger raw logs and generated binaries remain in scratch with recorded original sizes and hashes. `provenance-*.json` distinguishes original and published bytes; `MANIFEST-*.sha256` hashes the published files.

## Round: merge dev e81ce82f: REVIEW READY

Assignment: issue #696 comment 6142198285. The starting lane is clean at `26e2748f47b0d8fa533f53203264d9f31fc13c48`; fetched dev is `e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c`. Remote and branch verified. No second TAKEN comment.

Completed: merged the fetched tip without conflicts or manual source edits. All assigned MAAP checks, five standard suite shards and the canonical tally pass, as do the required local gates and current resource measurements. The builder command records one unchanged historical calibration arm not run; that arm is not counted as covered. No push, PR edit, hardware operation or second TAKEN comment. REVIEW READY was posted and read back byte-identical: https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6147603995.

| Gate | State | Evidence |
|---|---|---|
| Merge and protected-path conflict check | PASS | `313616d1a18549d41907db389d378f0beb9bc543`; exact mechanical tree `8eb5d868bfac1973ba1d82b0665aabae07d9494c`; no conflict |
| Sharding self-test, duration 1,375 s and 60 percent bound | PASS | Self-test rc 0; worker 1/5 predicted 4,205 s <= 4,320 s |
| MAAP suite and campaign | PASS | 186 clean checks; 65 campaign rows: all 63 named defect rejections and two clean controls; suite rc 0 |
| MAAP datapath and line coverage | PASS | Five integration checks; 225/225 eligible lines; both rc 0 |
| MAAP differential | PASS | 12 cases and 17/17 planted defects caught; rc 0 |
| Behavior gate | PASS | 14 features, 406 scenarios, 1,977 steps; no failure or skip |
| Static gates | PASS | 28 checks, each rc 0; three setup refusals were rerun using the existing YAML-capable environment |
| Portability gate | PASS | 58 top-level checks; tied-input and observer/stream-binding gates pass; rc 0 |
| Processor regression bank | PASS | 1,028,250 checks, zero failing; rc 0 |
| gPTP regression bank | PASS | Full `make -j8 tb`, rc 0 |
| Auxiliary commands | rc 0 | Eight commands; all required elaboration arms pass. Builder gate 11 (unchanged historical estimator calibration) did not run because its report is absent; see limitation below |
| Firmware regression bank | PASS | `test_ctrl_firmware.py --require-rv32 --self-test --jobs 2`, rc 0 |
| Full parent sweep and tally | PASS | Five shards, each rc 0; exact 62-suite inventory; 2,187,183 checks, zero in-suite failures; canonical tally and final aggregate rc 0 |
| MAAP OOC ceiling | PASS | 446 LUT / 340 FF; +7 / +60 against 439 / 280 at `6aa25dec` |
| Candidate shipping route | PASS | 49,277 LUT / 53,419 FF, WNS +0.242 ns, WHS +0.017 ns; route complete; resource gate rc 0 |
| Standalone 1×1 endpoint | PASS | 23,179 LUT / 19,779 FF; unchanged from accepted record; resource gate rc 0 |
| Standalone 8×8 endpoint | PASS | 30,135 LUT / 27,380 FF; unchanged from accepted record; resource gate rc 0 |
| Shipping comparison against dev | PASS | Candidate 49,277 LUT / 53,419 FF vs dev 49,427 / 53,378: −150 LUT / +41 FF; both route gates rc 0 |
| Recipe measurement records and input recheck | PASS | Four `record --write` calls to an external policy copy, rc 0; 378 input-file checks unchanged; memory-image hashes identical |

| Lens | Prior covering rounds | Head | New-head coverage |
|---|---|---|---|
| Conformance | R558-12, R559-9 | `26e2748f` | Pending independent disposition |
| RTL | R558-12, R559-9 | `26e2748f` | Pending independent disposition |
| Robustness | R558-12, R559-9 | `26e2748f` | Pending independent disposition |
| Tests | R558-12, R559-9 | `26e2748f` | Pending independent disposition |
| Docs | R558-12, R559-9 | `26e2748f` | Pending independent disposition |

Author evidence is not a review verdict. The historical sections below retain their original head and scope.

Operational exception: the kernel peak counter showed 10,561,486,848 bytes before the hard guard was installed, above the requested 9 GB limit; the full final scan also found a sampled maximum of 10,560,684,032 bytes (correcting the earlier receipt note that samples had missed it). No out-of-memory event occurred. At 13:04 local time, the service hard limit was reduced to 8.9 GB with an 8.5 GB reclaim threshold, forced reclaim was removed, and sampling increased to every five seconds. The earlier breach remains disclosed; it is not described as a compliant peak. The 8×8 synthesis log also records a filesystem-thrashing warning during the earlier forced-reclaim phase; synthesis and its resource check both exited 0, and the warning remains in the retained log.


### Final acceptance and closeout

| Issue acceptance | Result at this head | Evidence |
|---|---|---|
| 1. Conform or clause-justify M1..M8, checks and defect plants | Met under the recorded rulings | Unchanged MAAP contract; 186 clean checks, all 63 named defect rejections; limitations retained |
| 2. M4 first-enable sampling and real datapath MAC distinction | Met | Five integration checks; real MAC and clock plants rejected; every-seed and fixed-pair checks pass |
| 3. OOC, shipping route and recipe records within budget | Met | MAAP +7 LUT / +60 FF; three candidate resource endpoints pass; candidate/dev routes and four external recipe records |
| 4. Reference-peer bench interoperability | Not run here | Assigned post-merge bench lane; no hardware access |

All five shards exit 0: workers 0/1/2/3/4 take 2,439.8 / 2,768.2 / 3,077.8 / 2,174.2 / 2,417.5 seconds. The disjoint inventory is exactly 62 suites. The canonical tally reports 2,187,183 checks and zero in-suite failures. `native/final-results.json` and `native-final.rc` are the final native verdict; `extra/results.json` and `extra-bank-independent.rc` carry the eight auxiliary command results and the builder coverage limit.

The final main worktree is clean at the stated merge head, with the configured author identity and a one-line commit. All ten protected blobs still match the reviewed head. All 378 measured source inputs and 30 memory-image references still match after testing. Two scratch field-campaign reports regenerated only their timestamp on line 7; their generated bytes and diff were preserved, then those scratch reports were restored from the reviewed commit. No main-lane file was changed by the campaigns.

All owned background jobs and monitoring have ended. The lowest sampled free space was 40,216,285,184 bytes, above the 30 GiB guard. The maximum sampled memory after the hard guard was 8,510,918,656 bytes, with no sample above 9 GB afterward and no out-of-memory event. The earlier breach remains an operational exception.

The six temporary recipe links (three each in the candidate and dev scratch checkouts) were removed after all source/image checks, as the recipe requires. Their exact relative targets are in `recorded/recipe-link-cleanup.json`. To replay a resource check, recreate those links from that receipt to the retained external builder and ROM directories, then remove them again. Measurement reports and 17 checkpoint/binary artifacts remain in scratch; their hashes and sizes are recorded, and no large build artifact is copied into the output directory.

Receipts: `merge-dev-e81ce82f-receipts/` (526 sanitized small receipts, four provenance parts, one receipt manifest; 42 large log/report artifacts retained by hash and size). Publication text: `REVIEW-READY-COMMENT-MERGE-DEV.md`; readback receipt: `COMMENT-PUBLICATION-MERGE-DEV.json`. Root digest ledger: `MANIFEST-merge-dev-e81ce82f.sha256`. Historical sections below describe their original heads and output-file states. The current PR body is this merge round's body.

### Merge provenance and changed artifacts

The accepted baseline stays at its recorded input head under `docs/design/AREA_BUDGET.md:453` (D7) and `:530` (inherited Mark II movement). Fresh measurements are compared with that policy and written through `record --write` to an external measurement copy; the improvement recommendation does not authorize replacing the repository baseline.

The new commit is `313616d1a18549d41907db389d378f0beb9bc543`, with ordered parents `26e2748f47b0d8fa533f53203264d9f31fc13c48` and `e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c`. Its tree equals the independent mechanical merge result. There was no conflict and no manual source edit. The inherited register documentation and control-memory changes below come from the explicitly requested dev merge.

The MAAP RTL, datapath integration, MAAP design document, unit/integration Makefiles and harnesses, mutation table and differential harness retain exactly the blobs reviewed at `26e2748f`. Candidate and dev memory-image hashes are identical. Of 127 route input files in each population, functional differences are confined to `hdl/ieee1722/maap/KL_maap.sv` and `hdl/milan/milan_datapath.sv`; the generated top differs only in ordering inside its hierarchy block comment. Removing comments and normalizing build roots gives the same top-level text hash. All 378 candidate and dev input-file checks still match the captured bytes. The duration authority is `scripts/suite_shards.py:166`; the bound is defined at `scripts/suite_shards.py:118` and checked by its self-test, including planted overloaded durations.

All 57 imported paths follow. Each line is the first changed line at the merge head relative to the first parent; the merge diff provides the remaining hunks.

| Imported artifact | Change source |
|---|---|
| `.github/workflows/rtl-fast.yml:315` | Fetched dev `e81ce82f` |
| `docs/ARCHITECTURE_HW_SW_SPLIT.md:192` | Fetched dev `e81ce82f` |
| `docs/README.md:79` | Fetched dev `e81ce82f` |
| `docs/design/AREA_BUDGET.md:238` | Fetched dev `e81ce82f` |
| `docs/design/MAILBOX_SPLIT.md:1136` | Fetched dev `e81ce82f` |
| `docs/design/MARK_II_AREA_PLAN.md:42` | Fetched dev `e81ce82f` |
| `docs/design/SPLIT_CONTROL_MEMORY.md:1` | Fetched dev `e81ce82f` |
| `docs/findings/117_GPTP_SILICON_EVIDENCE.md:4` | Fetched dev `e81ce82f` |
| `docs/findings/394_387_E1_SWITCH_CYCLES.md:4` | Fetched dev `e81ce82f` |
| `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4` | Fetched dev `e81ce82f` |
| `docs/findings/667_TALKER_START_BENCH.md:4` | Fetched dev `e81ce82f` |
| `docs/findings/B14_BENCH_5603C353.md:4` | Fetched dev `e81ce82f` |
| `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:320` | Fetched dev `e81ce82f` |
| `docs/litex/LITEX_SOC.md:8` | Fetched dev `e81ce82f` |
| `docs/reference/REGISTER_MAP.md:148` | Fetched dev `e81ce82f` |
| `docs/testing/726_STREAM_COUNTERS.md:1` | Fetched dev `e81ce82f` |
| `docs/testing/CI_WORKFLOWS.md:45` | Fetched dev `e81ce82f` |
| `docs/testing/MILAN_V12_AUDIT_2026-08-16.md:218` | Fetched dev `e81ce82f` |
| `docs/testing/TESTING.md:513` | Fetched dev `e81ce82f` |
| `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:182` | Fetched dev `e81ce82f` |
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:18` | Fetched dev `e81ce82f` |
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:27` | Fetched dev `e81ce82f` |
| `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv:32` | Fetched dev `e81ce82f` |
| `hdl/ieee1722/crf/KL_crf_rx.sv:58` | Fetched dev `e81ce82f` |
| `scripts/check_py_idiom.py:175` | Fetched dev `e81ce82f` |
| `scripts/ci_events.py:129` | Fetched dev `e81ce82f` |
| `scripts/ci_scope.py:63` | Fetched dev `e81ce82f` |
| `scripts/measure_test_evidence_readers.py:127` | Fetched dev `e81ce82f` |
| `scripts/run_litex_sims.sh:101` | Fetched dev `e81ce82f` |
| `scripts/suite_shards.py:2` | Fetched dev `e81ce82f` |
| `sw/firmware/ctrl/README.md:367` | Fetched dev `e81ce82f` |
| `sw/firmware/ctrl/aecp/README.md:55` | Fetched dev `e81ce82f` |
| `sw/firmware/ctrl/plat/ctrl_split.ld:1` | Fetched dev `e81ce82f` |
| `sw/firmware/ctrl/plat/ctrl_split_start.S:1` | Fetched dev `e81ce82f` |
| `sw/firmware/ctrl/test/ctrl_srp_image.py:8` | Fetched dev `e81ce82f` |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:91` | Fetched dev `e81ce82f` |
| `sw/firmware/ctrl/test/test_ctrl_firmware_shards.py:1` | Fetched dev `e81ce82f` |
| `sw/litex/ctrl_memory.py:1` | Fetched dev `e81ce82f` |
| `sw/litex/milan_soc.py:44` | Fetched dev `e81ce82f` |
| `sw/litex/test_ctrl_memory.py:1` | Fetched dev `e81ce82f` |
| `syn/ooc/ctrl_memory_ooc.py:1` | Fetched dev `e81ce82f` |
| `tb/tools/torture_campaign.py:68` | Fetched dev `e81ce82f` |
| `tb/verilator/avtp_rxmon/sim_lockstep.cpp:9` | Fetched dev `e81ce82f` |
| `tb/verilator/avtp_rxmon/sim_main_nx.cpp:16` | Fetched dev `e81ce82f` |
| `tb/verilator/crf_rx/sim_main.cpp:98` | Fetched dev `e81ce82f` |
| `tb/verilator/milan_dp/Makefile:27` | Fetched dev `e81ce82f` |
| `tb/verilator/milan_dp/README.md:24` | Fetched dev `e81ce82f` |
| `tb/verilator/milan_dp/sim_crf_licence.cpp:55` | Fetched dev `e81ce82f` |
| `tb/verilator/milan_dp/sim_nxn.cpp:93` | Fetched dev `e81ce82f` |
| `tb/verilator/milan_dp/stream_counter_f5.cpp:1` | Fetched dev `e81ce82f` |
| `tb/verilator/milan_dp/stream_counter_f5.py:1` | Fetched dev `e81ce82f` |
| `tb/verilator/milan_dp/stream_counters.hpp:1` | Fetched dev `e81ce82f` |
| `tb/verilator/milan_dp/stream_counters.py:1` | Fetched dev `e81ce82f` |
| `tb/verilator/tkdiag/sim_main.cpp:17` | Fetched dev `e81ce82f` |
| `tests/features/counters_contract_milan.feature:42` | Fetched dev `e81ce82f` |
| `tests/steps/counters_contract_steps.py:344` | Fetched dev `e81ce82f` |
| `tests/steps/torture_plan_steps.py:298` | Fetched dev `e81ce82f` |

### Verification setup correction

The first full-suite attempt exited 2 in the production cancellation preflight, before any RTL suite ran. Its hard-HUP control timed out because the detached launcher passed an ignored SIGHUP disposition to the driver. Process status confirmed that inheritance. The replacement cancellation preflight passes, including both hard-HUP controls. Its full sweep resets HUP, INT and QUIT to their normal dispositions before launching the unchanged driver; no source, assertion, timeout or gate was altered. The original log and rc remain evidence. The serial replacement passed cancellation preflight and 19 suites, then was deliberately cancelled with TERM (rc 143) to use the repository’s standard five-worker distribution. Those partial results do not count as completion. Five isolated scratch checkouts are pinned at the merge head and all four required submodule roots and pins are verified. At most four shard drivers run together; every build shares the two-slot compilation cap. Their selections are disjoint and exactly equal the 62-suite default inventory; MAAP is on worker 1/5. The final aggregate requires every focused gate, all five shard verdicts, exact suite membership, and the repository tally over all 62 complete logs. The independent auxiliary bank runs alongside the remaining simulations; final readiness requires its separate rc 0 as well. The former idle auxiliary waiter was cancelled before it started any test. The original native aggregate exits 1 because it still includes the first preflight failure; the authoritative `native/final-results.json` substitutes the completed five-shard sweep and preserves every focused result. The original dependent auxiliary wrapper consequently exits without starting tests; `extra-bank-independent.rc` is the auxiliary result. No original return code is rewritten. The builder gate also requires elaboration, with the existing build environment selected explicitly.

### Auxiliary coverage limit

The builder command with `--require-rv32 --require-elaboration` exits 0. Every required elaboration arm runs, but its verdict explicitly excludes gate 11 (`sw/builder/test_builder.py:19268`): the historical mf48 placement utilization report is absent. That unchanged arm calibrates the legacy `arty_current` estimator and is not claimed as covered. Its source blob is identical to the reviewed head. The current candidate/dev recipe measurements and resource gates are independent completed evidence; they do not stand in for this skipped historical check.

### Current-head resource comparison

Every figure below comes from the recipe and resource gate. Synthesis uses the documented single-thread setting. Candidate and dev shipping routes used the same software build, device, constraints and flow. Every route is complete with no unrouted nets or routing errors. The accepted repository record remains unchanged under D7; fresh records were written by `record --write` to the external measurement copy.

| Figure | Candidate `313616d1` | Dev `e81ce82f` | Candidate minus dev |
|---|---:|---:|---:|
| LUT | 49,277 | 49,427 | −150 |
| FF | 53,419 | 53,378 | +41 |
| Slice | 15,779 | 15,753 | +26 |
| BRAM tiles | 87.5 | 87.5 | 0 |
| RAMB36 / RAMB18 | 74 / 27 | 74 / 27 | 0 / 0 |
| DSP | 14 | 14 | 0 |
| WNS, ns | +0.242 | +0.451 | −0.209 |
| WHS, ns | +0.017 | +0.036 | −0.019 |

Both standalone endpoints match the accepted LUT/FF and primitive figures: 1×1 = 23,179 / 19,779; 8×8 = 30,135 / 27,380. The routed candidate clears the +0.03 ns WNS floor. The separate MAAP OOC measurement is 446 LUT / 340 FF, within the original +60 / +60 ceiling against 439 / 280. This round introduces no per-item RTL change; the historical per-item table retains its original measurement head.

<!-- MERGE_COMMAND_LEDGER -->
### Current-head command ledger

Paths below use the same role variables as PR-BODY.md. Each row names its command receipt; the adjacent log and rc preserve the result. Commands ran directly, without pipelines. The final suite verdict additionally requires the strict 62-log aggregate. Setup failures and deliberately cancelled attempts remain separately disclosed above.

| Receipt | Command | Working directory | rc |
|---|---|---|---:|
| `static/00-docs_check` | `$DOC_PYTHON scripts/docs_check.py` | `$WORK/candidate` | 0 |
| `static/01-check_doc_style` | `$DOC_PYTHON scripts/check_doc_style.py` | `$WORK/candidate` | 0 |
| `static/02-check_doc_paths` | `$DOC_PYTHON scripts/check_doc_paths.py` | `$WORK/candidate` | 0 |
| `static/03-gen_toc` | `$DOC_PYTHON scripts/gen_toc.py --check` | `$WORK/candidate` | 0 |
| `static/04-gen_toc` | `$DOC_PYTHON scripts/gen_toc.py --verify-anchors` | `$WORK/candidate` | 0 |
| `static/05-check_em_dash` | `$DOC_PYTHON scripts/check_em_dash.py --base e81ce82f` | `$WORK/candidate` | 0 |
| `static/06-check_baremetal_only-retry` | `python3 scripts/check_baremetal_only.py --check` | `$WORK/candidate` | 0 |
| `static/07-check_sv_idiom` | `$DOC_PYTHON scripts/check_sv_idiom.py` | `$WORK/candidate` | 0 |
| `static/08-check_cpp_idiom` | `$DOC_PYTHON scripts/check_cpp_idiom.py` | `$WORK/candidate` | 0 |
| `static/09-check_py_idiom` | `$DOC_PYTHON scripts/check_py_idiom.py` | `$WORK/candidate` | 0 |
| `static/10-check_sh_idiom` | `$DOC_PYTHON scripts/check_sh_idiom.py` | `$WORK/candidate` | 0 |
| `static/11-check_hygiene` | `$DOC_PYTHON scripts/check_hygiene.py --check` | `$WORK/candidate` | 0 |
| `static/12-measure_test_evidence` | `$DOC_PYTHON scripts/measure_test_evidence.py --check` | `$WORK/candidate` | 0 |
| `static/13-measure_fail_fast` | `$DOC_PYTHON scripts/measure_fail_fast.py --check` | `$WORK/candidate` | 0 |
| `static/14-measure_naming` | `$DOC_PYTHON scripts/measure_naming.py --check` | `$WORK/candidate` | 0 |
| `static/15-check_todo_ownership` | `$DOC_PYTHON scripts/check_todo_ownership.py` | `$WORK/candidate` | 0 |
| `static/16-check_port_contracts` | `$DOC_PYTHON scripts/check_port_contracts.py` | `$WORK/candidate` | 0 |
| `static/17-check_soc_sources` | `$DOC_PYTHON scripts/check_soc_sources.py` | `$WORK/candidate` | 0 |
| `static/18-check_rtl_source_lists` | `$DOC_PYTHON scripts/check_rtl_source_lists.py` | `$WORK/candidate` | 0 |
| `static/19-ci_events-retry` | `python3 scripts/ci_events.py --check` | `$WORK/candidate` | 0 |
| `static/20-ci_events-retry` | `python3 scripts/ci_events.py --selftest` | `$WORK/candidate` | 0 |
| `static/21-ci_scope` | `$DOC_PYTHON scripts/ci_scope.py --selftest` | `$WORK/candidate` | 0 |
| `static/22-suite_shards` | `$DOC_PYTHON scripts/suite_shards.py --selftest` | `$WORK/candidate` | 0 |
| `static/23-check_feature_status` | `$DOC_PYTHON scripts/check_feature_status.py --self-test` | `$WORK/candidate` | 0 |
| `static/24-check_submodule_docs` | `$DOC_PYTHON scripts/check_submodule_docs.py` | `$WORK/candidate` | 0 |
| `static/25-pp_srcs` | `$DOC_PYTHON scripts/pp_srcs.py --check --selftest` | `$WORK/candidate` | 0 |
| `static/26-gen_module_matrix` | `$DOC_PYTHON docs/traceability/gen_module_matrix.py --check` | `$WORK/candidate` | 0 |
| `static/27-pp_resource_gate` | `$DOC_PYTHON syn/ooc/pp_resource_gate.py check-baseline` | `$WORK/candidate` | 0 |
| `native/behaviour` | `python3 -m behave --no-capture -f plain` | `$WORK/candidate/tests` | 0 |
| `native/field-build` | `cmake --build $WORK/tsn-gen/build --target packet_gen --parallel 4` | `$WORK/candidate` | 0 |
| `native/field-configure` | `cmake -S $WORK/tsn-gen -B $WORK/tsn-gen/build -DCMAKE_BUILD_TYPE=Release -DENABLE_PARSER_TESTS=OFF` | `$WORK/candidate` | 0 |
| `native/firmware` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 2` | `$WORK/candidate` | 0 |
| `native/gptp-suites` | `make -j8 tb` | `$WORK/candidate/gptp-processor` | 0 |
| `native/lint` | `python3 scripts/lint_rtl.py --check --self-test --jobs 2` | `$WORK/candidate` | 0 |
| `native/maap-coverage` | `make -j8 -C tb/verilator/maap coverage COV_MDIR=$WORK/native/coverage-build` | `$WORK/candidate` | 0 |
| `native/maap-differential` | `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep $WORK/native/differential` | `$WORK/candidate` | 0 |
| `native/maap-integration-build` | `make -j8 -C tb/verilator/maap integration-build DP_MDIR=$WORK/native/integration-build` | `$WORK/candidate` | 0 |
| `native/maap-integration` | `$WORK/native/integration-build/maap_integration` | `$WORK/native/integration-build` | 0 |
| `native/portability` | `bash syn/yosys/run.sh --results $WORK/native/portability-results` | `$WORK/candidate` | 0 |
| `native/processor-suites` | `bash scripts/run_suites.sh` | `$WORK/candidate/protocol-processor` | 0 |
| `shards/0` | `bash scripts/run_all_suites.sh $WORK/native/shards/0/logs --shard 0/5` | `$WORK/shard-0` | 0 |
| `shards/1` | `bash scripts/run_all_suites.sh $WORK/native/shards/1/logs --shard 1/5` | `$WORK/shard-1` | 0 |
| `shards/2` | `bash scripts/run_all_suites.sh $WORK/native/shards/2/logs --shard 2/5` | `$WORK/shard-2` | 0 |
| `shards/3` | `bash scripts/run_all_suites.sh $WORK/native/shards/3/logs --shard 3/5` | `$WORK/shard-3` | 0 |
| `shards/4` | `bash scripts/run_all_suites.sh $WORK/native/shards/4/logs --shard 4/5` | `$WORK/shard-4` | 0 |
| `resource/maap-ooc-candidate` | `flock $SYNTHESIS_LOCK $SYNTHESIS -mode batch -source run.tcl -nojournal -log baseline.log` | `$WORK/maap-ooc-candidate` | 0 |
| `resource/parser` | `flock $SYNTHESIS_LOCK python3 scripts/xvlog_gate.py --check` | `$WORK/candidate` | 0 |
| `resource/candidate-route` | `flock $SYNTHESIS_LOCK $SYNTHESIS -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log` | `$WORK/shipping-candidate/ax7101/gateware` | 0 |
| `resource/candidate-route-check` | `python3 syn/ooc/pp_resource_gate.py check $WORK/shipping-candidate/ax7101/gateware --endpoint route-1x1` | `$WORK/candidate` | 0 |
| `resource/rtl-8x8` | `flock $SYNTHESIS_LOCK $SYNTHESIS -mode batch -source rtl.tcl -nojournal -log baseline.log` | `$WORK/shipping-candidate/ax8x8-rtl` | 0 |
| `resource/ax7101-prepare-ooc` | `python3 syn/ooc/pp_baseline.py $WORK/shipping-candidate/ax7101/gateware --single-thread-synthesis --integrated-clock --output $WORK/shipping-candidate/ax7101-ooc --integrated-log $WORK/shipping-candidate/ax7101/gateware/baseline.log` | `$WORK/candidate` | 0 |
| `resource/ax7101-ooc` | `flock $SYNTHESIS_LOCK $SYNTHESIS -mode batch -source baseline_ooc.tcl -nojournal -log baseline.log` | `$WORK/shipping-candidate/ax7101-ooc` | 0 |
| `resource/candidate-ooc-1x1-check` | `python3 syn/ooc/pp_resource_gate.py check $WORK/shipping-candidate/ax7101-ooc --endpoint ooc-1x1` | `$WORK/candidate` | 0 |
| `resource/ax8x8-prepare-ooc` | `python3 syn/ooc/pp_baseline.py $WORK/shipping-candidate/ax8x8/gateware --single-thread-synthesis --integrated-clock --output $WORK/shipping-candidate/ax8x8-ooc --integrated-log $WORK/shipping-candidate/ax8x8-rtl/baseline.log` | `$WORK/candidate` | 0 |
| `resource/ax8x8-ooc` | `flock $SYNTHESIS_LOCK $SYNTHESIS -mode batch -source baseline_ooc.tcl -nojournal -log baseline.log` | `$WORK/shipping-candidate/ax8x8-ooc` | 0 |
| `resource/candidate-ooc-8x8-check` | `python3 syn/ooc/pp_resource_gate.py check $WORK/shipping-candidate/ax8x8-ooc --endpoint ooc-8x8` | `$WORK/candidate` | 0 |
| `resource/prepare-dev` | `python3 $WORK/prepare_shipping.py $WORK/dev $WORK/shipping-dev ax7101` | `$WORK/candidate` | 0 |
| `resource/dev-route` | `flock $SYNTHESIS_LOCK $SYNTHESIS -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log` | `$WORK/shipping-dev/ax7101/gateware` | 0 |
| `resource/dev-route-check` | `python3 syn/ooc/pp_resource_gate.py check $WORK/shipping-dev/ax7101/gateware --endpoint route-1x1` | `$WORK/candidate` | 0 |
| `recorded/candidate-ooc-1x1` | `python3 syn/ooc/pp_resource_gate.py record $WORK/shipping-candidate/ax7101-ooc --endpoint ooc-1x1 --write --baseline $WORK/measurement-policy.json` | `$WORK/candidate` | 0 |
| `recorded/candidate-ooc-8x8` | `python3 syn/ooc/pp_resource_gate.py record $WORK/shipping-candidate/ax8x8-ooc --endpoint ooc-8x8 --write --baseline $WORK/measurement-policy.json` | `$WORK/candidate` | 0 |
| `recorded/candidate-route` | `python3 syn/ooc/pp_resource_gate.py record $WORK/shipping-candidate/ax7101/gateware --endpoint route-1x1 --write --baseline $WORK/measurement-policy.json` | `$WORK/candidate` | 0 |
| `recorded/dev-route` | `python3 syn/ooc/pp_resource_gate.py record $WORK/shipping-dev/ax7101/gateware --endpoint route-1x1 --write --baseline $WORK/measurement-policy.json` | `$WORK/candidate` | 0 |
| `extra/control-memory` | `$BUILD_PYTHON sw/litex/test_ctrl_memory.py` | `$WORK/candidate` | 0 |
| `extra/firmware-shards` | `python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py` | `$WORK/candidate` | 0 |
| `extra/builder` | `python3 sw/builder/test_builder.py --require-rv32 --require-elaboration` | `$WORK/candidate` | 0 |
| `extra/recipe-selftest` | `python3 syn/ooc/pp_baseline.py --selftest` | `$WORK/candidate` | 0 |
| `extra/recipe-mutants` | `python3 syn/ooc/pp_baseline_mutants.py` | `$WORK/candidate` | 0 |
| `extra/resource-selftest` | `python3 syn/ooc/pp_resource_gate.py --selftest` | `$WORK/candidate` | 0 |
| `extra/resource-mutants` | `python3 syn/ooc/pp_resource_gate_mutants.py` | `$WORK/candidate` | 0 |
| `extra/baseline` | `python3 syn/ooc/pp_resource_gate.py check-baseline` | `$WORK/candidate` | 0 |

The duration self-test receipt is `sharding-selftest.log` (rc 0). Repository-owned self-tests also run as the full sweep preflight. The source, image and merge checks are in the provenance receipts. Only completed gates appear in this command ledger.
<!-- /MERGE_COMMAND_LEDGER -->

### Current-head MAAP check and planted-defect coverage

This table names the existing 63 planted defects and the checks that must reject them. All rows pass at the merged head; the complete suite reports 186 clean checks and 65 campaign checks, with zero failures. Each plant must compile, then exit 1 with its named check; build failures and abnormal termination do not count. The unit and datapath clean controls must exit 0. No new test or defect plant is introduced by the merge.

| Plant and source | Target | Required named rejection | Result |
|---|---|---|---|
| `m3_short_period` (`tb/verilator/maap/mutants.py:48`) | unit | M3 B.3.6.1 generator period is 2^32-1 | PASS |
| `m3_trap_outside_basis` (`tb/verilator/maap/mutants.py:52`) | unit | M3 B.3.6.1 generator period is 2^32-1 | PASS |
| `m3_ignores_clock` (`tb/verilator/maap/mutants.py:56`) | unit | M3 B.3.6.1 first enable seeds MAC plus clock | PASS |
| `m3_xors_clock` (`tb/verilator/maap/mutants.py:58`) | unit | M3 B.3.6.1 first enable seeds MAC plus clock | PASS |
| `m3_reseeds_after_release` (`tb/verilator/maap/mutants.py:60`) | unit | M3 Release/Begin retains the generator sequence | PASS |
| `m3_first_offset_ignores_clock` (`tb/verilator/maap/mutants.py:62`) | unit | M3 B.3.6.1 clocks 2^k apart claim different first offsets | PASS |
| `m4_first_offset_ignores_seed` (`tb/verilator/maap/mutants.py:65`) | unit | M4 B.3.6.1 adjacent MACs claim disjoint first blocks | PASS |
| `m4_first_offset_raw_seed_bits` (`tb/verilator/maap/mutants.py:67`) | unit | M4 B.3.6.1 adjacent MACs claim disjoint first blocks | PASS |
| `m4_first_offset_drops_seed_high_half` (`tb/verilator/maap/mutants.py:69`) | unit | M4 B.3.6.1 MACs 2^i apart (16 <= i <= 31) claim disjoint first blocks | PASS |
| `m4_first_interval_raw_seed_bits` (`tb/verilator/maap/mutants.py:72`) | unit | M4 B.3.4 MACs 2^i apart draw different first probe intervals | PASS |
| `m4_offset_row0_bit_drop` (`tb/verilator/maap/mutants.py:76`) | unit | M4 B.3.6.1 seed bits 16..31 map one-to-one onto the first offset word | PASS |
| `m4_offset_row6_bit_drop` (`tb/verilator/maap/mutants.py:79`) | unit | M4 B.3.6.1 every seed pair 2^i apart claims disjoint first blocks of 1..8 | PASS |
| `m4_probe_fold_unstepped` (`tb/verilator/maap/mutants.py:81`) | unit | M4 B.3.4 every seed pair 2^i apart draws different first probe intervals | PASS |
| `m4_first_offset_nonlinear` (`tb/verilator/maap/mutants.py:83`) | unit | M4 first-draw maps learned from the RTL are linear in the seed | PASS |
| `m4_probe_row_repeats_offset_row` (`tb/verilator/maap/mutants.py:87`) | unit | M4 B.3.6.1 first offset word and first probe draw are independent | PASS |
| `m6_overwrite_active_response` (`tb/verilator/maap/mutants.py:90`) | unit | M6 occupied response buffer preserves active DEFEND | PASS |
| `m6_replace_pending_response` (`tb/verilator/maap/mutants.py:93`) | unit | M6 pending response preserves prober and requested range | PASS |
| `m6_pending_survives_release` (`tb/verilator/maap/mutants.py:96`) | unit | M6 pending response cancelled with allocation | PASS |
| `m6_drop_busy_probe` (`tb/verilator/maap/mutants.py:99`) | unit | M6 busy PROBE gets DEFEND after wire is free | PASS |
| `m6_pending_source_not_saved` (`tb/verilator/maap/mutants.py:101`) | unit | M6 pending response preserves prober and requested range | PASS |
| `m5_ignore_link_return` (`tb/verilator/maap/mutants.py:103`) | unit | M5 B.3.5.9 link return revokes and reprobes | PASS |
| `m5_level_restarts` (`tb/verilator/maap/mutants.py:105`) | unit | M5 B.3.5.9 link return restarts PROBE | PASS |
| `m5_restart_on_link_loss` (`tb/verilator/maap/mutants.py:107`) | unit | M5 B.3.5.9 link loss is no event; return reprobes | PASS |
| `m1_probe_no_compare` (`tb/verilator/maap/mutants.py:110`) | unit | M1 rProbe/PROBE lower MAC keeps range | PASS |
| `m1_defend_no_compare` (`tb/verilator/maap/mutants.py:112`) | unit | M1 rDefend/DEFEND lower MAC keeps range | PASS |
| `m8_early_last_accepted` (`tb/verilator/maap/mutants.py:114`) | unit | M8 B.2 truncated PROBE-state input has no effect | PASS |
| `m8_missing_bytes_accepted` (`tb/verilator/maap/mutants.py:116`) | unit | M8 B.2 truncated DEFEND-state input has no effect | PASS |
| `m7_accept_invalid_seed` (`tb/verilator/maap/mutants.py:118`) | unit | M7 Table B.9 invalid supplied range refused | PASS |
| `m7_reject_valid_boundary` (`tb/verilator/maap/mutants.py:120`) | unit | M7 Table B.9 valid supplied boundary retained | PASS |
| `m2_own_requested_start` (`tb/verilator/maap/mutants.py:123`) | unit | M2 B.3.6.6 requested start echoes PROBE | PASS |
| `m2_echo_overlap_start` (`tb/verilator/maap/mutants.py:125`) | unit | M2 B.3.6.6 requested start echoes a PROBE starting below ours | PASS |
| `m2_own_requested_count` (`tb/verilator/maap/mutants.py:128`) | unit | M2 B.3.6.6 requested count echoes all 16 bits | PASS |
| `cdl_28` (`tb/verilator/maap/mutants.py:131`) | unit | B.2.1 cdl 16 (Begin! PROBE 1) | PASS |
| `defend_to_multicast` (`tb/verilator/maap/mutants.py:133`) | unit | B.2.1 DEFEND DA = PROBE source (above) | PASS |
| `defend_destination_not_latched` (`tb/verilator/maap/mutants.py:135`) | unit | B.2.1 DEFEND DA latched at send | PASS |
| `every_frame_to_the_prober` (`tb/verilator/maap/mutants.py:137`) | unit | B.2.1 PROBE DA multicast (Begin! 1) | PASS |
| `probe_draw_7_bits` (`tb/verilator/maap/mutants.py:139`) | unit | B.3.4.2 probe T < 600 ms (campaign) | PASS |
| `probe_base_500` (`tb/verilator/maap/mutants.py:141`) | unit | B.3.4.2 probe T > 500 ms (campaign) | PASS |
| `announce_base_3s` (`tb/verilator/maap/mutants.py:143`) | unit | B.3.4.1 announce T > 30 s | PASS |
| `announce_draw_11_bits` (`tb/verilator/maap/mutants.py:145`) | unit | B.3.4.1 announce T < 32 s | PASS |
| `announce_not_randomized` (`tb/verilator/maap/mutants.py:147`) | unit | B.3.4.1 announce T randomized | PASS |
| `zero_seed_freezes_the_probe_draw` (`tb/verilator/maap/mutants.py:149`) | unit | B.3.4.2 probe T randomized (zero-seed MAC) | PASS |
| `zero_seed_freezes_the_announce_draw` (`tb/verilator/maap/mutants.py:151`) | unit | B.3.4.1 announce T randomized (zero-seed MAC) | PASS |
| `announce_judged_on_conflict_fields` (`tb/verilator/maap/mutants.py:153`) | unit | B.2.7 ANNOUNCE conflict_* is not its range | PASS |
| `inclusive_range_end` (`tb/verilator/maap/mutants.py:157`) | unit | note b adjacent above: no conflict | PASS |
| `inclusive_range_start` (`tb/verilator/maap/mutants.py:159`) | unit | note b adjacent below: no conflict | PASS |
| `empty_range_conflicts` (`tb/verilator/maap/mutants.py:161`) | unit | note b empty range: no conflict | PASS |
| `no_compare_mac` (`tb/verilator/maap/mutants.py:163`) | unit | T.B7 note d: lower MAC keeps range | PASS |
| `compare_mac_while_probing` (`tb/verilator/maap/mutants.py:164`) | unit | T.B7 rAnnounce!/PROBE: no compare_MAC | PASS |
| `compare_mac_unreversed` (`tb/verilator/maap/mutants.py:166`) | unit | T.B7 rAnnounce!/DEFEND: re-address | PASS |
| `three_probes` (`tb/verilator/maap/mutants.py:169`) | unit | T.B7 Begin!: four PROBEs before ANNOUNCE | PASS |
| `first_probe_after_a_timer` (`tb/verilator/maap/mutants.py:171`) | unit | T.B7 Begin!: first PROBE at once | PASS |
| `restart_probe_after_a_timer` (`tb/verilator/maap/mutants.py:173`) | unit | T.B7 Restart!: first PROBE at once | PASS |
| `announce_after_a_timer` (`tb/verilator/maap/mutants.py:175`) | unit | T.B7 probeCount!: ANNOUNCE at once (Begin!) | PASS |
| `restart_rewrites_the_frame_on_the_wire` (`tb/verilator/maap/mutants.py:178`) | unit | frame on the wire keeps its offset | PASS |
| `overlap_count_to_our_end` (`tb/verilator/maap/mutants.py:181`) | unit | B.2.8 conflict_count = overlap (below) | PASS |
| `defend_rewrites_the_frame_on_the_wire` (`tb/verilator/maap/mutants.py:183`) | unit | PROBE mid-frame: frame on the wire byte-identical | PASS |
| `own_empty_range_conflicts` (`tb/verilator/maap/mutants.py:186`) | unit | note b: this station's empty range never conflicts | PASS |
| `m4_reset_time_sampling` (`tb/verilator/maap/mutants.py:192`) | datapath | M4 datapath: programmed MAC changes probe intervals | PASS |
| `m5_datapath_ignores_link` (`tb/verilator/maap/mutants.py:195`) | datapath | M5 datapath: link return starts four fresh PROBEs | PASS |
| `m3_datapath_ignores_clock` (`tb/verilator/maap/mutants.py:197`) | datapath | M3 datapath: real-time clock changes probe intervals | PASS |
| `m4_datapath_first_offset_ignores_seed` (`tb/verilator/maap/mutants.py:199`) | datapath | M4 datapath: fixed adjacent MAC pair claims disjoint first blocks | PASS |
| `m3_datapath_first_offset_ignores_clock` (`tb/verilator/maap/mutants.py:201`) | datapath | M3 datapath: fixed PHC time pair claims different first offsets | PASS |

The sharding self-test also plants missing, stale, zero and over-budget durations and checks the exact-bound/one-second-over boundary (`scripts/suite_shards.py:692`, `:741`). Other unchanged regression banks verify imported dev behavior; their individual results will be retained in the gate receipts. The prior round-7 table below explains the first-draw and requested-start defects in detail; those same harness bytes are tested again at this head.


## Round 7 status: REVIEW READY (round 7)

Head `32582421bbf095a7b5a7d4b953c4d737b86fe54b`, branch `696-maap-annexb`, local only (not pushed; no PR edit). Clean tree.
Every gate in the round-7 gate table exits 0 at the head; the p7 copy fails by design (the one gate rc 1, the bare-metal policy finding at `4a54d852`, was fixed by `49c0a83c` and the banks were rerun at the head).
REVIEW READY text: `REVIEW-READY-COMMENT-R7.md`, published and read back identical at https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6103504186. `PR-BODY.md` is the round-7 body (`Closes #696`).
Receipts: `r7-receipts/` (`MANIFEST-r7.sha256`; three logs over 200 KB stay in scratch, listed with sha256 and size in `SCRATCH-ARTIFACTS-r7.json`).
No job of this lane remains running; the exclusive Vivado lock was not taken this round. The service's memory stayed far below the cap (1.9 GB when sampled during the banks).
Four new commits on `d1b18b3f`; no rebase, amend or history rewrite. No RTL, record, route, register-map, filter, mailbox, pin or policy change.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6102832618 (records the narrowed round-6 criterion; items 1 to 4).
Reviews answered: R558-7 (https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6102796423) and R559-6 (https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6102829355).
Reviewer packets read from `696-review-evidence` at `bcd06a3201770919bac4842f12b9c74d954e5dc6`, extracted to scratch; their scripts ran unchanged, with paths as arguments.

Plan (all four items done; evidence below):

1. R559-6-F1: every first-draw check named for what it grades; fixed pairs in their own named checks; campaign anchors follow.
2. R559-6-F2: a named unit section that learns the first-offset and first-probe maps from the RTL's own first Begin! and establishes, for every seed, every carry run x every word x counts 1..8 through the RTL's pool fold and clip, the probe difference and the bits-16..31 bijection (plus the documented rank-22 independence); q3 and q9 in the default campaign, each failing its check by name.
3. R558-7-F1: a named M2 check at `[4b]` (PROBE below this station's offset) and the overlap-start echo plant.
4. Residues R558-7-R1 and R559-6-R1 with their exact texts.

## Round 7 commits

| Commit | Subject |
|---|---|
| `8e8f03434d2975c0bda4f0469caec10514ccadb1` | Establish the MAAP first-draw criterion for every seed from the RTL, name each first-draw check for what it grades and grade the below-offset requested-start echo |
| `4a54d8529c58693e1f689b9398afd92ad1c808f5` | Cite the recorded MAAP separation criterion and describe the every-seed first-draw checks, the fixed pairs and the below-offset echo check |
| `49c0a83c2dda51469f5ace2522b250d712cfd08f` | Call the steering seed of the MAAP every-seed check a null-space seed and group the plants that survive every sampled pair |
| `32582421bbf095a7b5a7d4b953c4d737b86fe54b` | Name R558-6's MAC pairs and the nonlinear plant among the MAAP plants that survive every sampled pair |

The third commit exists because the documentation bank's bare-metal policy check (`check_baremetal_only.py --check`, #259) refuses the word `kernel` anywhere in first-party sources; at `4a54d852` it reported 12 findings in `sim_main.cpp` (the linear-algebra sense). The variable and comments now say null space. The same commit corrects the campaign comment, which had claimed that all five new first-draw plants survive every sampled pair (the probe-row plant does not). Both banks were stopped and restarted at `32582421`; no result from the stopped runs is used.

## Round 7 design (R559-6-F2)

The first offset word and the first probe draw are GF(2)-linear in the seed (one generator step, then parity folds). So the harness learns both maps from the RTL instead of restating the fold rows:

- `seeded_first_offset(seed, count)` (`tb/verilator/maap/sim_main.cpp:1142`-`:1148`): one reset cycle, then MAC low word = seed at clock 0 and enable; the offset the RTL claims at that edge (`offset_o`). `tready` is held low, so nothing reaches the wire.
- `seeded_first_probe_draw(seed)` (`:1152`-`:1157`): one cycle later the first PROBE loads its probe timer; the draw is that load less the RTL's own `PROBE_MIN_MS_C` (read from the compiled model).
- `learn_seed_map()` (`:124`-`:144`): column k is the XOR of two observations whose seeds differ in bit k only. For the offset, count 0 keeps the clip out, and an offset at or above `2^16 - POOL_SIZE_C` (the RTL's constant) can only be the word itself, so only such pairs are used.
- Steering (`:1201`-`:1221`): a row-echelon basis of the learned columns (`insert_image`, `:1161`-`:1170`) gives every word of the image with a seed that the RTL maps onto it; a null-space seed is added so no steered seed is zero (the fallback). Each word is claimed through the RTL for counts 1 to 8 (524,288 claims at the head).
- Linearity (`:1222`-`:1233`): 256 further seeds must claim exactly the tabled offset of their learned word (counts cycling 1..8) and draw exactly the learned probe draw.
- Claims (`:1235`-`:1276`): for each of the 528 carry runs i..j (seeds s and s + 2^i differ by exactly that run), every word w of the image and every count must claim blocks at least `count` apart from w XOR the run's image; the run's probe image must be nonzero; columns 16..31 must have rank 16; the 32 combined 22-bit columns must have rank 22.

Cost: about 1 s on top of 2.4 s for the whole harness. No fold row, generator tap or pool bound is restated in the suite. A changed constant is therefore graded as it stands, and a nonlinear change fails the linearity check instead of passing stale.

## Round 7 changes

Line numbers are at `32582421`.

| Item | Artifact | Change |
|---|---|---|
| R558-7-F1 | `tb/verilator/maap/sim_main.cpp:437`-`:440` | `[4b]`: `M2 B.3.6.6 requested start echoes a PROBE starting below ours` reads bytes 26..31 of the DEFEND against pool base + `off0-4` |
| R558-7-F1 | `tb/verilator/maap/mutants.py:125`-`:127` | `m2_echo_overlap_start`: `tx_defend_off_r <= conf_start_w;` |
| R559-6-F1 | `sim_main.cpp:1083`-`:1137` | Section [12] split and renamed: adjacent MACs (32 sampled pairs), MACs 2^i apart (16 <= i <= 31) (136), MACs 2^i apart (1 <= i <= 15) (360), R558-6's fixed MAC pairs (4), clocks 2^k apart (32), fixed clock pairs (2), MACs 2^i apart first probe intervals (48), R558-6's fixed MAC pairs first probe intervals (4); the comment cites 6102832618 |
| R559-6-F1 | `tb/verilator/maap/sim_integration.cpp:153`-`:159`, `:182`-`:187` | Datapath first-claim checks renamed `M4 datapath: fixed adjacent MAC pair claims disjoint first blocks` and `M3 datapath: fixed PHC time pair claims different first offsets` |
| R559-6-F1 | `mutants.py:62`-`:73`, `:199`-`:203` | Anchors of `m3_first_offset_ignores_clock`, `m4_first_offset_drops_seed_high_half`, `m4_first_interval_raw_seed_bits` and both datapath first-claim plants follow the renames |
| R559-6-F2 | `sim_main.cpp:12`-`:15`, `:62`-`:68`, `:113`-`:144`, `:266`-`:270`, `:1139`-`:1276`, `:1301` | Header; `kMacBase`, `kLinearitySamples`, `kColumnTries`; `SeedImage`, `ImageBasis`, `SeedMap`, `learn_seed_map`; declarations; section [13] (`first_draws_for_every_seed`) and its call |
| R559-6-F2 | `mutants.py:74`-`:89` | `m4_offset_row0_bit_drop` (R559-6's q3), `m4_offset_row6_bit_drop` (q9), `m4_probe_fold_unstepped` (R559-6's q1 = R558-7's q3), `m4_first_offset_nonlinear`, `m4_probe_row_repeats_offset_row` |
| Criterion | `docs/design/MAAP_FABRIC.md:112`, `:115` | Cites comment 6102832618; "MACs 2^i apart with i up to 31" (bits 32..47 do not enter the seed) |
| R559-6-R1 | `MAAP_FABRIC.md:117` | Exact text appended |
| R559-6-F2 | `MAAP_FABRIC.md:120`, `:261`-`:266`, `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:5` | The every-seed evidence |
| R559-6-F1 | `MAAP_FABRIC.md:220`-`:221`, `:258`-`:259` | Fixed-pair naming for the datapath and unit checks |
| R558-7-R1 | `MAAP_FABRIC.md:260` | Exact replacement text |
| R558-7-F1 | `MAAP_FABRIC.md:255`, `:272` | The below-offset echo check and its plant |
| Plants | `MAAP_FABRIC.md:270`-`:271` | Which new plants survive every sampled pair, and what each fails |

`KL_maap.sv` is not touched (not even its comment at `:156`-`:162`): the three recorded endpoints hash it as a measured input.

## Round 7 tests and planted defects

A detection needs a successful build, exit status 1 and the named `[FAIL]` line; compiler failures and abnormal exits never count. All rows are in the default campaign (`make -C tb/verilator/maap`).
Failure lists below come from running each planted build on its own (`rows1/`, at `4a54d852`, whose RTL and checks equal the head's).

| Named check (where) | What it grades | Planted defect that must fail it | Other failures of that plant |
|---|---|---|---|
| `M2 B.3.6.6 requested start echoes a PROBE starting below ours` (`sim_main.cpp:439`) | DEFEND requested_start for the `[4b]` PROBE at `off0-4` | `m2_echo_overlap_start` (R558-7's q1): got pool + `off0`, expected pool + `off0-4` | none (186 checks, 1 failure) |
| `M4 first-draw maps learned from the RTL are linear in the seed` (`:1233`) | 32 + 32 learned columns, 256 fresh seeds against the tabled claims and draws | `m4_first_offset_nonlinear` (first fold XOR the AND of stepped bits 0 and 1) | the four claim checks below, which cannot be established (5 failures) |
| `M4 B.3.6.1 every seed pair 2^i apart claims disjoint first blocks of 1..8` (`:1270`) | 528 runs x 65,536 words x counts 1..8 through the RTL's claims | `m4_offset_row6_bit_drop` (R559-6's q9): run 18..18, count 5, words 0xfdf7 / 0xfdff claim 0xfdf7 / 0xfdfb | none (1 failure); every sampled pair passes |
| `M4 B.3.4 every seed pair 2^i apart draws different first probe intervals` (`:1271`) | 528 runs, learned probe image nonzero | `m4_probe_fold_unstepped` (R559-6's q1, R558-7's q3; also answers R558-7-S1 and R559-6-S1): run 1..1 draws equal | none (1 failure) |
| `M4 B.3.6.1 seed bits 16..31 map one-to-one onto the first offset word` (`:1272`) | rank of learned columns 16..31 = 16 | `m4_offset_row0_bit_drop` (R559-6's q3) | none (1 failure); every sampled pair passes |
| `M4 B.3.6.1 first offset word and first probe draw are independent` (`:1274`) | rank of the 32 combined 22-bit columns = 22 | `m4_probe_row_repeats_offset_row` (probe row 0 := offset row 0) | `MACs 2^i apart draw different first probe intervals`, every-run probe check (3 failures) |
| `M4 B.3.6.1 adjacent MACs claim disjoint first blocks` (`:1126`) | 32 sampled adjacent pairs, one per carry run | `m4_first_offset_ignores_seed` (R558-6's p7), `m4_first_offset_raw_seed_bits` | unchanged rows |
| `M4 B.3.6.1 MACs 2^i apart (16 <= i <= 31) claim disjoint first blocks` (`:1127`) | 136 sampled pairs | `m4_first_offset_drops_seed_high_half` | 7 failures in total, among them the three every-seed claim checks |
| `M4 B.3.6.1 MACs 2^i apart (1 <= i <= 15) claim disjoint first blocks` (`:1129`) | 360 sampled pairs | p7 and the high-half plant also fail it | - |
| `M4 B.3.6.1 R558-6's fixed MAC pairs claim disjoint first blocks` (`:1131`) | R558-6's four pairs | p7 also fails it | - |
| `M3 B.3.6.1 clocks 2^k apart claim different first offsets` (`:1132`) | 32 sampled clock pairs | `m3_first_offset_ignores_clock` | also `fixed clock pairs` (2 failures) |
| `M3 B.3.6.1 fixed clock pairs claim different first offsets` (`:1133`) | (0, 17) and (0x01020304, 0xffff1234) | p7 and the clock plant also fail it | - |
| `M4 B.3.4 MACs 2^i apart draw different first probe intervals` (`:1134`) | 48 sampled pairs (32 adjacent, 16 single bits 16..31) | `m4_first_interval_raw_seed_bits` | also the fixed-pair interval check and the every-run probe check (3 failures) |
| `M4 B.3.4 R558-6's fixed MAC pairs draw different first probe intervals` (`:1135`) | R558-6's four pairs | the raw-seed probe plant also fails it | - |
| `M4 datapath: fixed adjacent MAC pair claims disjoint first blocks` (`sim_integration.cpp:158`) | 0x7029 / 0x9821 | `m4_datapath_first_offset_ignores_seed` | unchanged row |
| `M3 datapath: fixed PHC time pair claims different first offsets` (`sim_integration.cpp:186`) | 0xf229 / 0xf1cd | `m3_datapath_first_offset_ignores_clock` | unchanged row |

R558-6's p7 copy at the head (PR body command): 186 checks, 9 failures (six first-claim checks, and the every-seed disjointness, one-to-one and independence checks); make rc 2 by design.

Reviewer probes, unchanged scripts from the evidence branch, run against the clean gate worktree at `32582421` through the two-slot build semaphore (`r7-receipts/probes/`):

| Script | Result |
|---|---|
| R558-7 `reviewer_probes.py` (10 probes) | q1 (overlap-start echo, F1) CAUGHT at `M2 B.3.6.6 requested start echoes a PROBE starting below ours`, 1 failure; q3 (unstepped probe fold, S1) CAUGHT at the every-run probe check; q2, q6, q7, q11, q12, q13, q14 CAUGHT; q4 (every Begin! re-folds, S2) ESCAPED, 186/0 |
| R559-6 `probes.py` (8 probes) | q1 (S1) CAUGHT at the every-run probe check; q3 (F2) CAUGHT at the one-to-one check alone; q2, q4, q6, q7 CAUGHT; q5 (S3) and q8 (S2) ESCAPED, 186/0 |
| R559-6 `q9_probe.sh` | full unit harness rc 1: 186 checks, 1 failure, `M4 B.3.6.1 every seed pair 2^i apart claims disjoint first blocks of 1..8` (run 18..18, count 5: claims 0xfdf7 / 0xfdfb); its `first_offsets` pair gives 0xfdf8 / 0xfdf3 under q9 and 0xfdf8 / 0xfdb3 at the head |

The escaping probes are the optional suggestions R558-7-S2, R559-6-S2 and R559-6-S3, outside this assignment; the PR body lists them under known limitations.
An earlier probe pass straddled the move of the gate worktree from `4a54d852` to `32582421` (harness change: the variable rename only); it is kept aside as `probes-mixed/` and not used.

## Round 7 gate table

Commands are unpiped; each rc is the command's own. Verilator: the pinned 5.050 through the round's two-slot build semaphore.
Gate tree: the clean detached worktree `merge/final` (submodules at their pins), moved from `d1b18b3f` to `32582421`; `git status --short` empty after every bank.
Heads: `H` = `32582421` (final). `L` = the lane tree before committing.

| Gate | Exact command | Head | Result |
|---|---|---|---|
| Lane quick checks | `check_cpp_idiom.py`, `check_py_idiom.py`, `check_hygiene.py --check`, `measure_test_evidence.py --check`, `measure_fail_fast.py --check`, `measure_naming.py --check`, `check_todo_ownership.py`, `docs_check.py`, `check_em_dash.py --base e8454e275`, `check_doc_style.py`, `check_doc_paths.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `gen_module_matrix.py --check` | L (before `8e8f0343`) | each rc 0 |
| Bare-metal policy | `check_baremetal_only.py --check` | `4a54d852` (documentation bank, stopped) | rc 1: 12 findings, the word `kernel` in `sim_main.cpp`; fixed by `49c0a83c` |
| Lane quick checks | `check_baremetal_only.py --check`, `check_cpp_idiom.py`, `check_py_idiom.py`, `check_hygiene.py --check`, `docs_check.py`, `check_em_dash.py --base e8454e275`, `check_doc_style.py` | L (before `49c0a83c`) | each rc 0 |
| Unit harness, clean RTL | `make -C tb/verilator/maap build MDIR=…`, then `VKL_maap_sim` | L at each commit | rc 0; 186 checks, 0 failures; 3.3 s (2.4 s at `d1b18b3f`) |
| Planted rows, singly | `try_rows.py` (each named row through the campaign's own `run_case`) | `4a54d852` RTL and checks | rc 0; nine rows caught at their named checks (failure lists in the tests table) |
| Lint | `python3 scripts/lint_rtl.py --check --self-test --jobs 2` | H | rc 0; 90 <= 90 |
| Behaviour | `behave --no-capture -f plain` (in `tests`) | H | rc 0; 14 features, 404 scenarios, 1,968 steps |
| Full MAAP target | `make -j8 -C tb/verilator/maap MDIR=…` (default: unit run, then `mutants.py`), CPython 3.12.3 first on `PATH` | H | rc 0; 186 checks, 0 failures; campaign 65 rows, 0 failures (63 defects at their named checks: 58 unit, 5 datapath; 2 clean controls) |
| MAAP datapath | `make -j8 -C tb/verilator/maap integration-build DP_MDIR=…`, then `./maap_integration` | H | rc 0 / rc 0; 5 checks, 0 failures; first offsets 0x7029 / 0x9821 and 0xf229 / 0xf1cd |
| MAAP coverage | `make -j8 -C tb/verilator/maap coverage COV_MDIR=…` | H | rc 0; `KL_maap.sv` 225/225 lines, 95 % gate PASS |
| MAAP differential | `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep …` | H | rc 0; clean 12/12 (sweep 5,172..5,810 cycles); 17/17 defects caught |
| p7 copy | the PR body's p7 command | H (lane) | make rc 2 by design: 186 checks, 9 failures (listed in the PR body) |
| Reviewer probes | as in the probes table | H | scripts rc 0; verdicts as listed |
| Documentation set | `docs_bank.py`: the `docs.yml` docs-check, wire-accountability and no-git jobs plus the fast-workflow self-tests (94 rows: HDL reference, em-dash `--base e8454e27`, doc style, TOC and anchors, doc paths, bare-metal policy, module matrix, idiom and hygiene checks, builder `--require-rv32`, recipe and resource-gate self-tests and mutants, `check-baseline`, Yosys self-tests) | H | 94/94 rc 0; tree and `gptp-processor` clean |
| Sweep shard owning the MAAP suite | `bash scripts/run_all_suites.sh <logs> --shard 1/5` (`shard_bank.py`) | H | rc 0; 23/23 suites, 196,929 checks, 0 in-suite failures, 0 timeouts; 4 declared `tsn_fuzz` field-campaign skips; MAAP 186/0 and campaign 65/0 inside it; 42.5 min; tree clean |

Not rerun in round 7, with the reason:

| Gate | Last run | Why it still holds |
|---|---|---|
| Full parent sweep (61 suites) | `30242308` (61/61, 2,185,927 checks) | Round 7 changes only `tb/verilator/maap/{sim_main.cpp,sim_integration.cpp,mutants.py}` and two documentation pages; the MAAP suite ran at H through its default target and in the sweep shard that owns it |
| Portability (Yosys) | `30242308` (58/58 tops) | No RTL change |
| Firmware bank, field campaigns | `d1b18b3f` | No firmware, generator or suite input change |
| Vivado: MAAP instrument, route, standalone endpoints, records | `bee1b0d7` | No RTL change; `KL_maap.sv` byte-identical; `check-baseline` passes at H |
| Processor banks | `963ad3b8e` | Pins and processor sources unchanged |
| Hosted checks / local workflow replica | none at this head | Need the pushed head; no push in this assignment |
| Bench | none | Acceptance 4; post-merge bench lane |

## Round 7 coverage (author's view; the ledger is reviewer-owned)

| Lens | State at `d1b18b3f` | Artifacts round 7 changes in that lens's scope | Author's reading |
|---|---|---|---|
| Conformance | R558-7 CLEAN; R559-6 UNCLEAN (R559-6-F1: criterion unmet as written, no recorded narrowing) | The criterion is now recorded (6102832618); check names, `MAAP_FABRIC.md:112`-`:120`; no RTL change | Un-covered for R559-6; needs re-review at the head |
| RTL | R558-7 CLEAN; R559-6 CLEAN | None: `hdl/ieee1722/maap/KL_maap.sv` and every other RTL file are byte-identical to `d1b18b3f` (`git diff --stat d1b18b3f..HEAD -- hdl/ '*.sv'` lists only `KL_maap.md`) | Covered at `d1b18b3f`, an ancestor nothing in the lens's scope has touched since |
| Robustness | R558-7 CLEAN; R559-6 CLEAN | Tests only; the new M2 fixture check reads an existing fixture | Robustness covers behaviour under malformed and edge input; the RTL is unchanged, so the reviewers decide whether the test changes touch it |
| Tests | R558-7 UNCLEAN (F1); R559-6 UNCLEAN (F1, F2) | `sim_main.cpp`, `sim_integration.cpp`, `mutants.py` | Un-covered; needs re-review |
| Docs | R558-7 CLEAN (R558-7-R1); R559-6 UNCLEAN (F2; R559-6-R1) | `MAAP_FABRIC.md`, `KL_maap.md`, PR body | Un-covered; needs re-review |

This is author evidence, not a review verdict.

## Round 7 acceptance

| Acceptance | Status at `32582421` |
|---|---|
| 1 | MET: M4's first draw now has executable every-seed evidence for the recorded criterion; M2's echo is graded where it differs from the overlap start; other items as before |
| 2 | MET (unchanged): datapath checks show different MACs drawing different intervals; the first-claim datapath checks are now named as fixed pairs |
| 3 | MET (unchanged): no RTL change, so the round-6 records and `check-baseline` stand (`check-baseline` rerun at the head in the documentation bank) |
| 4 | NOT RUN; post-merge bench lane |

So the PR body says `Closes #696`.

## Round 6 status: REVIEW READY (round 6)

Head `d1b18b3fa0b476a9b534c88466b163e15f469004`, branch `696-maap-annexb`, local only (not pushed; no PR edit). Clean tree.
Five new commits on `6de3904e`; no rebase, amend or history rewrite. No register-map, filter, mailbox, pin or policy change.
Every gate below exits 0 at its stated head; the final banks ran at `d1b18b3f`. All three resource endpoints passed and are re-recorded (`b7f342ae`).
Published and read back identical: https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6102601784 (text in `REVIEW-READY-COMMENT-R6.md`); `PR-BODY.md` is the round-6 body (`Closes #696`, R558-6-R1's head and round table fixed).
No job of this lane remains running; the exclusive Vivado lock is not held by this lane.

Resume after an external usage-limit stop (21:06, 2026-10-10; not a gate failure).
At the stop the lane tree was clean at `bee1b0d7`; the exclusive-lock Vivado job had finished the MAAP instrument, parser, route, route queries, 8x8 RTL elaboration and the 1x1 standalone endpoint (all rc 0, gate checks rc 0), and was inside the 8x8 standalone synthesis, which the stop killed.
The resume moves the killed attempt aside (`shipping/ax8x8-ooc-killed`, `ax8x8-ooc-killed.log`) and reruns only that endpoint and its check under the exclusive lock (`vivado_bank_resume.py`, lock taken 21:39).
No campaign planted a file; nothing in the tree needed restoring.
After the resume, the records were written, documented and committed, and the final banks ran at the new head.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6097504752 (option 1, conform).
It answers R558-6 (https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6097490649): R558-6-F1 (MINOR; Conformance, RTL, Robustness, Tests) and R558-6-R1 (PR body head).
Start head `6de3904ec2d6b2f04325c94c7686519ecd92a202` (PR #706). New commits only; no rebase, amend or push.
The reviewer packet was read from `696-review-evidence` at `0dcfa9b4f6131138b83c7ede413ff9ae7ad68d06`, extracted to scratch.

Plan:

1. RTL: the first Begin! offset and the first probe interval draw from the generator one step past the seed, through parity folds of all 32 bits (no new flip-flop).
2. Checks: a named unit check over equally timed stations (adjacent MACs at every carry length, MACs differing only in bits 16..31, MACs one bit apart, clocks); datapath first-block checks; p7 and related plants in the default campaign.
3. Reviewer probes rerun; MAAP OOC against the ceiling; three endpoints through the recipe under the exclusive lock; record only if every gate passes.
4. Docs: `MAAP_FABRIC.md`, `KL_maap.md`; PR body head and round table.

All four items are done; the sections below give the evidence.

## Round 6 commits

| Commit | Subject |
|---|---|
| `3024230808cb6e29f2cd0f717e347ecedaaa60fd` | Draw the first MAAP offset and probe interval from the generator one step past the seed through full-seed folds |
| `05eca371ea1f31aed793e0f6240435455ebc4837` | Describe the first MAAP draw from the stepped seed, its folds and the equally timed station checks |
| `bee1b0d712773de799e50f8d9cfc7a02263651f4` | Accept either end of the draw-coverage check for the MAC-ignoring differential plant |
| `b7f342ae72ef10add0e6b087c40794f4396fcb30` | Re-record the three resource endpoints at the MAAP first-draw head |
| `d1b18b3fa0b476a9b534c88466b163e15f469004` | Document the first-draw resource re-baseline and the MAAP area at the measured head |

All five are new commits on `6de3904e`; no rebase, amend or push. The last is the round's head.

## Round 6 design

R558-6-F1: at first enable the offset was `rand_offset(enable_seed_w[15:0])`, the raw low 16 bits of MAC + clock, and the first probe timer read `lfsr_r[5:0]` of the same raw seed.
The 32-bit Fibonacci generator cannot be used as the mixer directly: one step only shifts the seed, and a jump of k steps needs about 20 seed bits per output bit (too many LUTs for the 54 left).
So the round keeps the generator, its period and its M3 seed load exactly, and changes only what the two first draws read:

- `seed_next_w = lfsr_step(enable_seed_w)`: the generator one step past the seed (the firmware core also steps before its first draw).
- First offset word: `offset_fold(seed_next_w)`. Bit i is the parity of the stepped seed under row i of `OFFSET_FOLD_C` (16 rows, at most 3 stepped bits each; two rows use the feedback bit).
- Probe draw: `probe_fold(lfsr_next_w)` for every probe interval. At the first PROBE `lfsr_r` holds the seed, so this is the same stepped seed (6 rows, at most 6 stepped bits each, counting the feedback bit as its 4 taps).

The rows come from a search over sparse GF(2) matrices (`r6-receipts/model/design.py`, seed 24), accepted only when all of these hold:

1. For every carry run i..j of the seed (528 runs: two seeds 2^i apart), the offset-word difference D has gap(D) >= 15 and does not contain bits 10..15.
   Then two count-8 blocks share no address for every seed pair of that run, through rand_offset's fold (subtract 0xFE00) and clip (at most 7 addresses).
   Here gap(D) = 2^h minus the sum of D's lower set bits, with h the top bit: the smallest arithmetic distance two words differing by D can have.
2. Seed bits 16..31 map one-to-one onto the offset word (16x16 rank 16): MACs differing only in bits 16..31 never draw equal words.
3. Rank 16 for the offset rows; the 33 prefix images of the probe rows are distinct (every run changes the first probe draw); rank 22 for all rows together (the first offset word and first probe draw are jointly uniform and independent).
4. R558-6's four probe pairs are disjoint, and the unit fixture MAC's first offset at clock 0 (0x0129) leaves room for the range cases.

`r6-receipts/model/rtl_tables.py` reads the two tables back out of `KL_maap.sv` and re-checks 1 to 3 (all true).
`verify.py` samples 300 bases per run (158,103 pairs): 0 overlaps and 0 equal first probe draws.
Random pairs differing only in bits 16..31 overlap 55 times in 200,000 (about 46 expected for independent draws) and are never identical.

No flip-flop is added; the change is LUT-only, as R558-6 required.

## Round 6 changes

Line numbers are at `30242308` (code) and `05eca371` (docs).

| Finding | Artifact | Change |
|---|---|---|
| F1 | `hdl/ieee1722/maap/KL_maap.sv:146`-`:149` | `lfsr_step()` holds the generator's one step; `lfsr_next_w = lfsr_step(lfsr_r)` (same taps, same period) |
| F1 | `KL_maap.sv:152`-`:154` | `seed_next_w = lfsr_step(enable_seed_w)`; the M3 seed load (`lfsr_r <= enable_seed_w`) is unchanged |
| F1 | `KL_maap.sv:156`-`:178` | `OFFSET_FOLD_C` (16 rows), `PROBE_FOLD_C` (6 rows), `offset_fold()`, `probe_fold()`; the comment states the guaranteed properties |
| F1 | `KL_maap.sv:200`-`:202` | Probe interval `518 + probe_fold(lfsr_next_w)` ms; announce unchanged (`30488 + lfsr_r[9:0]`) |
| F1 | `KL_maap.sv:333`-`:339` | First Begin! offset `rand_offset(offset_fold(seed_next_w))`; later Begin! and Restart! unchanged |
| F1 | `tb/verilator/maap/sim_main.cpp:93`-`:105`, `:979`-`:1077`, `:1101` | `first_claim()` (one station from reset, same reset/enable cycles for every station, the first PROBE's requested_start and its first interval) and five named checks in section [12] |
| F1 | `sim_main.cpp:12`-`:13`, `:50` | Header names the new grading; the fixture comment no longer says the seed is used directly |
| F1 | `tb/verilator/maap/sim_integration.cpp:60`-`:93`, `:134`-`:186` | First PROBE requested_start per station; two new datapath checks; 5 checks |
| F1 | `tb/verilator/maap/mutants.py:36`-`:43`, `:48`-`:55`, `:62`-`:73`, `:120`-`:121`, `:171`-`:184`, `:246`-`:251` | New anchors; `m3_short_period`, `m3_trap_outside_basis` and `probe_draw_7_bits` re-pointed to the moved expressions (same plants); five unit plants and two datapath plants added; the three existing datapath plants moved into `DATAPATH_MUTANTS` unchanged |
| F1 | `docs/design/MAAP_FABRIC.md:96`-`:118` | The probe and announce draws, the M3 seed load, the first Begin! draw exactly, and what the folds guarantee (and what no 16-bit draw can) |
| F1 | `MAAP_FABRIC.md:157` | Deviation: "the 16-bit draw" (not "the generator's low 16 bits") folds into the pool with bias |
| F1 | `MAAP_FABRIC.md:215`-`:217`, `:250`-`:257` | Randomness and TB paragraphs name the new datapath and unit checks and the #696 plants |
| F1 | `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:5` | The first draw and its property |

Third commit, `bee1b0d712773de799e50f8d9cfc7a02263651f4` ("Accept either end of the draw-coverage check for the MAC-ignoring differential plant"):

| Finding | Artifact | Change |
|---|---|---|
| F1 (gate the RTL change touches) | `sw/firmware/ctrl/test/maap_differential.py:79`-`:80` | The `parent-ignores-mac` plant (seed forced to `32'hAC61`) must fail the draw-coverage check at either end. At `30242308` the needle named only "highest draws". With the new probe fold the planted parent's draws over 1,024 MAC/phase pairs reach 5,801 cycles but not the low end (5,230 > 5,200), so it fails `MAC/phase sampling reaches the parent's lowest draws` instead (same test, `ProbeTimingAndCount`). The needle is now the common prefix, which only those two assertions carry (`test_maap_differential.cpp:191`-`:194`). The README already describes the property as "fails the draw-coverage check" |

Fourth and fifth commits (assignment item 3, area and records; line numbers at `d1b18b3f`):

| Item | Artifact | Change |
|---|---|---|
| Records | `syn/ooc/pp_resource_baseline.json:27`-`:114` (`b7f342ae`) | `record --write` replaced the three endpoints' `record` objects; only the `measured` note was then set (same serialisation). Every policy key, the schema and the description are byte-identical (checked by `record_r6.py` and `check-baseline`) |
| Records | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:7`-`:8`, `:17`, `:34`-`:107` | New section "Re-baseline of 2026-10-10, issue #696 first draw": inputs, method, three endpoint rows, differences, corners, worst path, MAAP routed figures and slack, input digests, receipts; the intro names it as the current record; contents entry through `gen_toc.py --write` plus its description |
| Records | `docs/design/AREA_BUDGET.md:13`, `:109`-`:112`, `:124`-`:129`, `:132`-`:137`, `:146`-`:147`, `:151`-`:152`, `:371`, `:410`, `:466`-`:469` | Record narrative, headroom table (50,013 LUT, 78.88 %, 11,973 over; 97 slices free; +0.233 / +0.017 ns), critical path, preceding images, datapath and wrapper LUTs, NFR-RES-01 arithmetic (wrapper at most 11,020 LUT, remove 11,973, 52 %), M0s comparison anchor, WNS floor text, the eighth re-baseline |
| Records | `docs/design/MARK_II_AREA_PLAN.md:56`, `:110`-`:111`, `:121`-`:141`, `:654` | Gate-comparison row, current-record reference, route column of the inventory (19 of 22 rows changed; every cell equals the written record, both standalone columns unchanged), the M0s comparison anchor |
| MAAP area | `docs/design/MAAP_FABRIC.md:161`, `:164`-`:165`, `:167` | 490 LUT / 340 FF at `bee1b0d7`: +45 / +0 against `0df48637`, +51 / +60 against `6aa25dec`, within the +60 / +60 ceiling; routed 468 / 339 |
| Index | `docs/findings/README.md:25` | Names the first-draw re-baseline as the gate's current record |

## Round 6 tests and planted defects

A detection needs a successful build, exit status 1 and the named `[FAIL]` line. Compiler failures and abnormal exits never count.
All rows below are in the default campaign (`make -C tb/verilator/maap` = unit run, then `mutants.py`) unless marked otherwise.

| Named check (where) | What it grades | Planted defect that must fail it |
|---|---|---|
| `M4 B.3.6.1 adjacent MACs claim disjoint first blocks` (unit, `sim_main.cpp:1072`) | 33 pairs: one per carry length of `seed + 1` (MAC low words `s - c`, `s - c + 1`, common clock `c`), plus R558-6's `…:01`/`…:02` at clock 0 | `m4_first_offset_ignores_seed` (R558-6's p7, the pre-#696 expression `rand_offset(lfsr_next_w[15:0], count_i)`); `m4_first_offset_raw_seed_bits` (the `6de3904e` expression `enable_seed_w[15:0]`) |
| `M4 B.3.6.1 MACs differing in bits 16..31 claim disjoint first blocks` (unit, `:1073`) | 139 pairs: 136 seed pairs 2^i apart with i >= 16 (every carry run), R558-6's three pairs (bit 16; octet 4 `0a`/`5b` at clock 7; octet 3 `11`/`22`) | `m4_first_offset_drops_seed_high_half` (fold of `{16'd0, seed_next_w[15:0]}`) |
| `M4 B.3.6.1 MACs 2^i apart claim disjoint first blocks` (unit, `:1074`) | 360 pairs, i = 1..15, every carry run | p7 and the raw-seed plant also fail it (demonstration rows below) |
| `M3 B.3.6.1 different clocks claim different first offsets` (unit, `:1075`) | One MAC, 34 clock pairs: c and c + 2^k for k = 0..31, then (0, 17) and (0x01020304, 0xffff1234) | `m3_first_offset_ignores_clock` (fold of `lfsr_step(station_mac_i[31:0])`) |
| `M4 B.3.4 first probe interval differs across MACs` (unit, `:1076`) | 52 pairs: the 32 adjacent-run pairs, 16 single-bit pairs in bits 16..31, R558-6's four pairs; first PROBE to second PROBE, cycles | `m4_first_interval_raw_seed_bits` (`{10'd0, lfsr_r[5:0]}`, the `6de3904e` draw) |
| `M4 datapath: adjacent MACs claim disjoint first blocks` (real CSR path, `sim_integration.cpp:155`-`:158`) | MACs `02:00:00:00:00:01` and `…:02`, equal reset/write/enable timing: first PROBE requested_start 0x7029 / 0x9821 | `m4_datapath_first_offset_ignores_seed` (p7 again; both stations claim 0x7c4f, as R558-6 measured) |
| `M3 datapath: real-time clock changes the first offset` (real CSR path, `:181`-`:184`) | One MAC enabled 1,000 and 2,000 cycles after programming: 0xf229 / 0xf1cd | `m3_datapath_first_offset_ignores_clock` |
| Re-pointed existing rows | `m3_short_period`, `m3_trap_outside_basis` (the generator step now lives in `lfsr_step`), `probe_draw_7_bits` (a 7-bit probe draw) | same named checks as before |

Demonstrations outside the campaign (plant diffs in `r6-receipts/plants/`, driver `r6-receipts/scripts/try_plants.py`), run at `bee1b0d7` (its RTL and harness equal `30242308`), with the checks each failed:

| Plant | Result |
|---|---|
| p7 (unit) | 4 failures: adjacent, bits 16..31, 2^i apart, different clocks |
| raw low seed bits as the first offset (`6de3904e` behaviour) | the same 4 failures |
| offset fold without the high half | 3 failures: bits 16..31, 2^i apart, different clocks |
| raw seed as the first probe draw | 1 failure: first probe interval |
| first offset folded from the seed without the generator step | 1 failure: bits 16..31 (caught because these rows were chosen for the stepped seed) |
| probe fold of the current state instead of the next (no step on the probe side) | ESCAPES (177/0): the step is a linear re-indexing, and the 6-bit fold of the unstepped seed still separates every tested pair. No property-based check can see it without restating the RTL table; it is reported, not graded |

Reviewer probes (R558-6's `reviewer_probes.py`, gate tree at `30242308`):

| Run | Result |
|---|---|
| Unchanged script | p1 to p5, p8, p9 CAUGHT; p6 ESCAPED (R558-6-S1, unchanged); both p7 rows `ANCHOR-NOT-UNIQUE`, because its anchor is the replaced `enable_seed_w[15:0]` text |
| Copy with only the p7 anchor re-pointed to the new first-draw text (`r6-receipts/probes/reviewer_probes_r6.diff`, one line; the replacement stays the pre-#696 expression) | p7 unit CAUGHT, p7 datapath CAUGHT; the other eight rows as above |
| `first_draw_probe.cpp`, unchanged, built against the new `KL_maap.sv` | all four pairs `disjoint`: 0x0109/0x4901, 0x0109/0x4109, 0x7a78/0x3ef8, 0x8174/0xa044; first intervals 5200/5520, 5200/5360, 5560/5690, 5630/5510 cycles |

Suggestions R558-6-S1 (p6 snapshot check) and R558-6-S2 (outage wording) are not applied: they are optional and outside this round's assignment.

## Round 6 area and records (assignment item 3)

Measured tree: the clean detached validation worktree at `bee1b0d7` (lane tree and validation tree both clean, byte-compared on every repository input before and after).
One exclusive-lock job per run set (`flock $VIVADO_LOCK`, exclusive only), nothing else of this lane running beside it.
The first job (19:08-21:06) ran every step below except the 8x8 standalone synthesis, which an external usage-limit stop killed mid-run; the resume job (lock 21:39, done 22:32) reran only that endpoint and its check from a fresh directory.

**MAAP against the ceiling** (`syn/ooc/milan_datapath_ooc.tcl`, one thread, ruling 6079087547: base `6aa25dec` 439 LUT / 280 FF, ceiling +60 / +60):

| Head | `g_maap.maap_engine` LUT | FF | vs base | Within ceiling |
|---|---:|---:|---:|---|
| `0df48637` (merge result, round 1) | 445 | 340 | +6 / +60 | yes |
| `bee1b0d7` (round 6) | 490 | 340 | +51 / +60 | yes (499 / 340 limit) |

The first-draw folds cost +45 LUT and no flip-flop. No `Synth 8-4445` line in the instrument log.

**Three endpoints through the recipe** (`--single-thread-synthesis`, `--integrated-clock` for both standalone runs; parser `xvlog_gate.py --check` rc 0 before the route):

| Endpoint | LUT | FF | Slice | RAMB36 / 18 | DSP | WNS / WHS ns | Against the preceding record (`0df48637`) | Gate |
|---|---:|---:|---:|---:|---:|---:|---|---|
| `route-1x1` | 50,013 | 54,306 | 15,753 | 74 / 27 | 14 | +0.233 / +0.017 | -217 LUT, -2 FF, -70 slices, WNS +0.119, WHS -0.019; fully routed | `check` rc 0, PASS |
| `ooc-1x1` | 23,179 | 19,779 | - | 16 / 3 | 8 | -3.562 / +0.159 | every figure equal | `check` rc 0, PASS |
| `ooc-8x8` | 30,135 | 27,380 | - | 21 / 5 | 8 | -2.278 / +0.159 | every figure equal | `check` rc 0, PASS |

- Route floor and drop limit: WNS +0.233 ns is 0.203 ns above the +0.030 ns floor and rose (no fall against the 0.25 ns limit); WHS +0.017 ns is above the zero floor (WHS fell 0.019 ns, which the gate accepts). Every primitive count is unchanged. No exception was needed or taken.
- Worst route path: 27 levels on the 20 ns clock, `pp_shadow/u_pp/u_aecp/u_d3/rec_r_reg[3]` to the reset pin of `deb_cnt_r_reg[29]`, slack +0.233 ns, inside the processor wrapper (outside the lane's logic; its sources are unchanged).
- MAAP in the route: 468 LUT / 339 FF (425 / 339 before). Worst incoming setup +3.906 ns (16 levels, `ts_counter/acc_reg[36]` to `maap_engine/offset_r_reg[10]`, the first-draw path), worst outgoing +5.963 ns, worst incoming hold +0.175 ns.
- Inputs: each endpoint's measured inputs differ from the preceding record's only in `hdl/ieee1722/maap/KL_maap.sv` (`r6-receipts/scripts/input_delta.py`; same file order, generics, generated top and memory images). The standalone wrapper does not instantiate `KL_maap`, so both standalone endpoints keep every figure.
- Input digests: route `29b603ff…`, ooc-1x1 `b2a2e9df…`, ooc-8x8 `3b3ed3f9…` (full values in the findings section and the record).
- Records: written only after all three `check` runs passed, by `record --write` (`record_r6.py`), which then set the `measured` note, re-ran the three `check`s against the new records (all PASS, zero deltas) and `check-baseline` (PASS, 3 endpoints). Policies, schema and description unchanged.
- Memory: Vivado peaks 7,964 MB (route), 4,999 MB (1x1), 5,986 MB (8x8), 4,198 MB (8x8 RTL elaboration). The service's anonymous memory peaked at 10.17 GB in one 30 s sample during the route (19:53), above the 9 GB guidance; nothing else of this lane was running, and no out-of-memory event was recorded. The route is one recipe process and was not split.
- Run receipts (Vivado `baseline.log` of each run): route 52.7 min, `d9f952db…`, 818,672 B; rtl-8x8 1.4 min, `6cc79615…`, 213,944 B; ooc-1x1 25.5 min, `0d620fe3…`, 319,289 B; ooc-8x8 53.2 min, `8345a4cd…`, 324,996 B (full digests in the findings section).

## Round 6 gate table

Commands are unpiped; each rc is the command's own. Verilator: the pinned 5.050 through the round's two-slot build semaphore (never more than two compilations at once).
Heads: `C` = `30242308` (code), `D` = `bee1b0d7` (code + docs + differential driver; RTL, harness and campaign blobs equal `C`; the measured head), `F` = `d1b18b3f` (the final head: `D` plus the record and its documentation).
Gate tree: a clean detached scratch worktree at `C`, moved to `F` for the final banks, submodules at their pins; `git status --short` empty after every bank (`r6-receipts/focus-r6/tree-status.txt`, `r6-receipts/final-F/tree-status.txt`).
Vivado rows ran in the separate clean validation worktree at `D` under the exclusive lock.

| Gate | Exact command | Head | Result |
|---|---|---|---|
| Lint | `python3 scripts/lint_rtl.py --check --self-test --jobs 2` | C | rc 0; 90 <= 90 (the one `KL_maap` entry is the existing `rx_msg_r` WIDTHTRUNC, now at line 412) |
| Behaviour | `behave --no-capture -f plain` (in `tests`) | C | rc 0; 14 features, 404 scenarios, 1,968 steps |
| MAAP unit | `make -j8 -C tb/verilator/maap run MDIR="$WORK/unit-build"` | C | rc 0; 177 checks, 0 failures |
| MAAP datapath | `make -j8 -C tb/verilator/maap integration-build DP_MDIR="$WORK/integration-build"`, then `./maap_integration` from that directory | C | rc 0 / rc 0; 5 checks, 0 failures |
| MAAP campaign | `python3 tb/verilator/maap/mutants.py` | C | rc 0; 59 rows: 57 defects exit 1 at their named checks (52 unit, 5 datapath), 2 clean controls exit 0 |
| MAAP coverage | `make -j8 -C tb/verilator/maap coverage COV_MDIR="$WORK/coverage-build"` | C | rc 0; `KL_maap.sv` 225/225 lines, 95 % gate |
| MAAP differential | `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$WORK/differential"` | C | rc 1: clean 12/12, but `parent-ignores-mac` failed the low-end draw-coverage assertion while the driver required the high-end one (16/17). Fixed by `bee1b0d7` |
| MAAP differential | the same command, in the measured validation tree | D | rc 0; clean 12/12 (sweep 5,172..5,810 cycles); 17/17 defects caught, `parent-ignores-mac` at the low end (5,230 > 5,200); tree unchanged |
| Portability | `bash syn/yosys/run.sh --results "$WORK/portability-results"` | C | rc 0; 58/58 tops (`KL_maap` 2,493 cells), tied-input and tap-purity gates pass |
| Parent sweep | `bash scripts/run_all_suites.sh "$WORK/parent-suites-logs"` (gate tree, no lock) | C | rc 0; 61/61 suites, 2,185,927 checks, 0 failures, 0 timeouts; four declared field-campaign skips; 9,458 s |
| Reviewer probes | R558-6's `reviewer_probes.py`, unchanged and with the p7 anchor re-pointed | C | both rc 0; see the probes table |
| First-draw probe | R558-6's `first_draw_probe.cpp`, unchanged | C | rc 0; four pairs `disjoint` |
| Demonstration plants | `r6-receipts/scripts/try_plants.py` (six unit plants through `mutants.run_case`) | D | rc 0; failures as listed in the plants table |
| Lane quick checks | `check_cpp_idiom.py`, `check_py_idiom.py`, `check_hygiene.py --check`, `check_sv_idiom.py`, `measure_naming.py --check`, `check_port_contracts.py`, `check_rtl_source_lists.py`, `measure_test_evidence.py --check`, `measure_fail_fast.py --check`, `check_todo_ownership.py`, `gen_module_matrix.py --check`, `docs_check.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_em_dash.py --base e8454e27`, `check_doc_style.py`, `check_doc_paths.py` | lane before committing | each rc 0 |
| MAAP ceiling instrument | Vivado batch on `syn/ooc/milan_datapath_ooc.tcl` (one thread), exclusive lock | D | rc 0; `g_maap.maap_engine` 490 LUT / 340 FF, +51 / +60, within +60 / +60; 0 `Synth 8-4445` |
| Parser | `python3 scripts/xvlog_gate.py --check` (measured tree) | D | rc 0 |
| Shipping route | recipe `baseline_integrated.tcl` (ax7101 1x1), exclusive lock; then `pp_resource_gate.py check <route> --endpoint route-1x1` | D | rc 0 / rc 0, PASS: 50,013 LUT, 54,306 FF, 15,753 slices, 74/27/14, +0.233 / +0.017 ns, fully routed, IOB packing PASS |
| Route queries | Vivado on the routed checkpoint (MAAP and design worst paths, hierarchy) | D | rc 0; MAAP 468 / 339; MAAP slack in +3.906, out +5.963, hold +0.175 ns |
| 8x8 elaboration | recipe RTL elaboration for the 8x8 bound parameters | D | rc 0 |
| Standalone 1x1 | `pp_baseline.py <ax7101> --single-thread-synthesis --integrated-clock --output … --integrated-log …`, Vivado, `check --endpoint ooc-1x1` | D | rc 0 / rc 0 / rc 0, PASS, every figure equal |
| Standalone 8x8 | the same for ax8x8 (resume job; the stopped attempt is not used) | D | rc 0 / rc 0 / rc 0, PASS, every figure equal |
| Input re-verification | `vivado_bank*.py` `verify()`: every repository input byte-compared against the lane tree, images rehashed, digests before = after | D | 122 / 119 comparisons, 0 problems; digests unchanged |
| Records | `pp_resource_gate.py record <dir> --endpoint <e> --write` ×3, then `check` ×3 and `check-baseline` (`record_r6.py`) | D (lane tree at D, committed as `b7f342ae`) | all rc 0; zero deltas against the new records; `baseline PASS: 3 endpoints` |
| Doc quick checks | `docs_check.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_em_dash.py --base e8454e27`, `check_doc_style.py`, `check_doc_paths.py`, `check_hygiene.py --check`, `pp_resource_gate.py check-baseline` | lane before committing `d1b18b3f` | each rc 0 |
| Lint | `python3 scripts/lint_rtl.py --check --self-test --jobs 2` | F | rc 0; 90 <= 90 |
| Full MAAP target | `make -j8 -C tb/verilator/maap MDIR="$WORK/unit-build"` (default target: unit run, then `mutants.py`) | F | rc 0; 177 checks, 0 failures; campaign 59 rows, 0 failures (57 defects at their named checks, 2 clean controls) |
| MAAP datapath | `make -j8 -C tb/verilator/maap integration-build DP_MDIR=…`, then `./maap_integration` | F | rc 0 / rc 0; 5 checks, 0 failures |
| MAAP coverage | `make -j8 -C tb/verilator/maap coverage COV_MDIR=…` | F | rc 0; 225/225 lines |
| MAAP differential | `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep …` | F | rc 0; clean 12/12; 17/17 defects caught |
| Documentation set | `docs_bank.py`: the `docs.yml` docs-check, wire-accountability and no-git jobs plus the fast-workflow self-tests (HDL reference, em-dash `--base e8454e27`, doc style, TOC check and anchors, doc paths, module matrix, idiom and hygiene checks, builder `--require-rv32`, recipe and resource-gate self-tests and mutants, `check-baseline`, Yosys self-tests; full list in `r6-receipts/docs_bank.py`) | F | 94/94 rc 0; tree and `gptp-processor` clean afterwards |
| Firmware bank | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 2` | F | rc 0; `test_ctrl_firmware: PASS` (host, RV32 and campaigns; mutants 471 of 471 caught) |
| Field campaigns | `TSN_GEN_ROOT=<generator at the rtl.yml pin> make -j8 -C tb/verilator/tsn_fuzz` | F | rc 0; AAF 164 pass, gPTP 677 pass, 0 fail, freshness PASS; generator at pin `deca300c`, clean; only the two timestamp lines changed (diff kept) and were restored; tree clean |

Not rerun in round 6, with the reason:

| Gate | Last run | Why it still holds |
|---|---|---|
| Parent sweep, portability, behaviour | `C` | The record and documentation commits after `D` change no RTL, harness or suite input; `C` and `D` share every RTL, harness and campaign blob |
| Processor banks | `963ad3b8e` | Pins and processor sources unchanged |
| Hosted checks / local workflow replica | none at this head | Need the pushed head; no push in this assignment |
| Bench | none | Acceptance 4; post-merge bench lane |

## Round 6 coverage (author's view; the ledger is reviewer-owned)

| Lens | State at `6de3904e` | Artifacts round 6 changes in that lens's scope | Author's reading |
|---|---|---|---|
| Conformance | R558-6 UNCLEAN (F1); R559-5 clean | `KL_maap.sv:146`-`:178`, `:200`-`:202`, `:333`-`:339` (first draw); `MAAP_FABRIC.md:96`-`:118`; `KL_maap.md:5` | Un-covered; needs re-review at `d1b18b3f` |
| RTL | R558-6 UNCLEAN (F1); R559-5 clean | `KL_maap.sv` as above (LUT-only; no flip-flop, no state, no width change of a port); MAAP 490 / 340 within ceiling; route MAAP slack +3.906 ns | Un-covered; needs re-review |
| Robustness | R558-6 UNCLEAN (F1); R559-5 clean | First draw for every carry run, bits 16..31, clocks; `sim_main.cpp` section [12]; `sim_integration.cpp` first-claim checks | Un-covered; needs re-review |
| Tests | R558-6 UNCLEAN (F1); R559-5 clean | `sim_main.cpp`, `sim_integration.cpp`, `mutants.py` (7 new plants, 3 re-pointed), `maap_differential.py:79`-`:80` | Un-covered; needs re-review |
| Docs | R558-6 clean; R559-5 clean | `MAAP_FABRIC.md`, `KL_maap.md`, `AREA_BUDGET.md`, `MARK_II_AREA_PLAN.md`, `234_PP_SHADOW_AREA_BASELINE.md`, `docs/findings/README.md`, the record file and the PR body | Un-covered by these commits; needs re-review |

This is author evidence, not a review verdict.

## Round 6 acceptance

| Acceptance | Status at `d1b18b3f` |
|---|---|
| 1 | MET: R558-6-F1 conformed (first offset and first probe interval from the stepped full seed; five unit and two datapath checks; p7 and five related plants caught); other items as before |
| 2 | MET: seed at first enable from MAC plus clock; datapath checks show different MACs drawing different intervals and disjoint first blocks |
| 3 | MET: MAAP 490 / 340, +51 / +60 within +60 / +60; all three endpoints pass and are re-recorded through the recipe at `bee1b0d7` (`b7f342ae`); `check-baseline` passes at the head |
| 4 | NOT RUN; post-merge bench lane |

So the PR body says `Closes #696`.

## Round 2 status: REVIEW READY (round 2)

Published and read back identical: https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6093452983 (text in `REVIEW-READY-COMMENT-R2.md`).

Head `f909d6c460344527f102f24b8e7a77f09959e755`, branch `696-maap-annexb`, local only (not pushed; no PR edit).
Clean tree. Three new commits on `030eb98a` (the head pushed as PR #706); no rebase, no amend, no history rewrite.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6093171536.
It answers R558-1 (https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6093137183, one MINOR)
and R559-1 (https://github.com/kebag-logic/milan-fpga/pull/706#issuecomment-6093167069, three MINOR).
Both reviews found the RTL correct and covered Conformance, RTL and Robustness clean at `030eb98a`.

No RTL, register-map, filter, mailbox, record, policy or submodule-pin change. `KL_maap.sv` and `milan_datapath.sv` keep their blobs
(`3f4ea795`, `ee15148f`), so there is no re-measure; the design-input digests confirm it (gate table).

## Round 2 commits

| Commit | Subject |
|---|---|
| `eb2cac845e86ffaf3a9e83220bac2aa48d4f0508` | Grade M5 link loss with an outage longer than a walk and name the zero-seed fixture's MAC |
| `f03e254e11716ad2c1bef7b7e9a3f1e0629381b9` | State the merge-result MAAP area, the current record in the Mark II plan and the M5 loss contract |
| `f909d6c460344527f102f24b8e7a77f09959e755` | Say which record figures changed in the Mark II current inventory |

Every subject is one line with no body and no trailer, under the configured identity (`r2-receipts/head-identity.log`).

## Round 2 changes, by assignment item

Line numbers are at `f909d6c4`.

| Item | Finding | Commit | Artifact | Change |
|---|---|---|---|---|
| 1 | R559-1-F1 (Tests) | `eb2cac84` | `tb/verilator/maap/sim_main.cpp:68`-`:71` | `kOutageCyc` = 4 x 600 ms scaled = 24,000 cycles. A whole walk (the at-once PROBE, three intervals under 600 ms, the at-once ANNOUNCE) ends within about 18,020 cycles at the B.3.4.2 bound, and within 17,460 at the RTL's largest draw of 581 ms |
| 1 | R559-1-F1 | `eb2cac84` | `tb/verilator/maap/sim_main.cpp:763`-`:803` | New `port_loss_is_no_event()`, in PROBE (after the first PROBE) and in ANNOUNCE (after the first ANNOUNCE). The link drops for `kOutageCyc`. During the outage only the walk in progress may continue, on the original range: three timer PROBEs and the ANNOUNCE from PROBE, no frame from ANNOUNCE, and no frame within the at-once bound (4 cycles) of the loss. At the end the engine is in ANNOUNCE with the same offset and conflict count. At the rise it must enter PROBE with validity revoked and walk four PROBEs, the first at once, then the ANNOUNCE, without counting a conflict. One named check: `M5 B.3.5.9 link loss is no event; return reprobes` (`:802`) |
| 1 | R559-1-F1 | `eb2cac84` | `tb/verilator/maap/sim_main.cpp:202`, `:974` | Declaration; called after the existing M5 checks |
| 1 | R559-1-F1 | `eb2cac84` | `tb/verilator/maap/mutants.py:70`-`:72` | `m5_restart_on_link_loss`: R559-1's `r_restart_on_link_loss` replacement (same line, same text), required to fail the new named check |
| 1 | R559-1-F1 | `f03e254e` | `docs/design/MAAP_FABRIC.md:109`-`:110` | Contract: Table B.3 defines no event for leaving the operational state; a falling level leaves the walk in progress running until the return |
| 1 | R559-1-F1 | `f03e254e` | `docs/design/MAAP_FABRIC.md:229`-`:230` | TB paragraph names the long-outage requirement |
| 2 | R558-1-F1 (Docs); residue R1 | `f03e254e` | `docs/design/MAAP_FABRIC.md:143`-`:148` | R1's wording verbatim: 441 / 340 is the M3 step at lane head `39571196`, before the dev merge. Added: merge result `0df48637` 445 LUT / 340 FF, +6 / +60 against `6aa25dec`; dev `8b61b709` alone 443 / 280, so the lane's share is +2 / +60 |
| 3 | R559-1-F2 (Docs) | `f03e254e`, `f909d6c4` | `docs/design/MARK_II_AREA_PLAN.md:110`-`:113` | The current inventory names #696's re-baseline of 2026-10-10 (merge result `0df48637`, dev `8b61b709`, processor `2ad2f845`). Against the plan's baseline only the route figures changed; both standalone endpoints keep every figure. The levers and the ledger keep the baseline's route figures |
| 3 | R559-1-F2 | `f03e254e` | `docs/design/MARK_II_AREA_PLAN.md:121`-`:142` | Route column written from the recorded `route-1x1` scopes by `r2-receipts/scripts/plan_vs_record.py --write` (18 of 22 rows changed). The standalone columns were compared only, and all 44 equal the record |
| 3 | R559-1-F2 | `f03e254e` | `docs/design/MARK_II_AREA_PLAN.md:147` | #696 changed MAAP again before the current record |
| 3 | R558-1-S1 | `f03e254e` | `docs/design/MARK_II_AREA_PLAN.md:56` | Gate row: at the +0.114 ns WNS record the +0.030 ns floor binds first, after a fall of 0.084 ns; the 0.25 ns limit is unchanged (as `AREA_BUDGET.md:383`) |
| 4 | R559-1-F3 (Docs, Tests) | `eb2cac84` | `tb/verilator/maap/sim_main.cpp:9`, `:645`-`:646` | Header and banner name the fixture by its seed and MAC: `02:00:00:00:00:00`, clock 0 |
| 4 | R559-1-F3 | `f03e254e` | `docs/design/MAAP_FABRIC.md:227`-`:229` | Same fixture text in the design page |
| 5 | Residue R2 | `f03e254e` | `docs/design/MAAP_FABRIC.md:137`-`:138`, `:36` | R2's wording verbatim ("Remaining deviations"); the contents entry says "the remaining deviations" |
| 5 | Residue R3 | `f03e254e` | `docs/findings/README.md:25` | R3's wording verbatim: #696's re-baseline of 2026-10-10 |

Suggestions (optional per the assignment):

- R558-1-S1: applied (item 3).
- R559-1-S2: applied in `PR-BODY.md` ("How to validate" runs the datapath binary from its build directory).
- R559-1-S1: not applied. The period check learns the transition map from the 32 basis states and checks linearity on 5 listed and 128 sampled states.
  A trap at a state outside both lists is invisible to any non-exhaustive sample, so moving the mutant's trap off the list would make it escape rather than strengthen the check.
- R559-1-S3: not applied; it asks for an RTL change or a clock-assumption note, and this round is "no RTL change". The shipping clock is 50 MHz and the routed path keeps +4.037 ns.
- R559-1-S4: not applied (optional).

## Round 2 tests and planted defects

A detection needs a successful build, exit status 1 and the named failure. Compiler failures and abnormal exits never count.

| Named check | Planted defect | Where it runs | Result at `f909d6c4` |
|---|---|---|---|
| M5 B.3.5.9 link loss is no event; return reprobes | `m5_restart_on_link_loss`: `port_operational_p` on the falling edge (R559-1's `r_restart_on_link_loss`) | default campaign (`mutants.py`) | caught: exit 1 at the named check (`r2-receipts/bank/focus-r2/maap-mutants.log`) |
| M5 B.3.5.9 link loss is no event; return reprobes | R559-1's `r_restart_on_link_loss.patch`, applied verbatim with `patch` to a scratch copy | unit harness at `f909d6c4`, by hand | harness exit 1 (make rc 2); 172 checks, 1 failure: only this check (`r2-receipts/head-plants/link-loss.log`) |
| M5 B.3.5.9 link loss is no event; return reprobes, and both short-outage M5 checks | Restart on either edge (`port_operational_i != port_operational_r`); demonstration only, not in the campaign | unit harness at `f909d6c4`, by hand | harness exit 1 (make rc 2); 172 checks, 3 failures (`r2-receipts/head-plants/either-edge.log`) |
| M5 B.3.5.9 link return revokes and reprobes / restarts PROBE; M5 datapath | `m5_ignore_link_return`, `m5_level_restarts`, `m5_datapath_ignores_link` (unchanged) | default campaign | caught |
| B.3.4.2 / B.3.4.1 randomized (zero-seed MAC) | `zero_seed_freezes_the_probe_draw`, `zero_seed_freezes_the_announce_draw` (F3 verification) | default campaign | caught |

Before round 2, the reviewer's link-loss plant passed the unit harness (171 checks, 0 failures) and the datapath harness (R559-1's receipts); the new check is the only one it now fails.

## Round 2 gate table

Gate tree: a clean detached scratch worktree at `f909d6c4` (submodules at their pins, verified clean after each bank).
Verilator: the pinned 5.050 through the lane's two-slot build semaphore. Commands are unpiped; each rc is the command's own.

| Gate | Exact command | Result |
|---|---|---|
| MAAP unit | `make -j8 -C tb/verilator/maap run MDIR="$WORK/unit-build"` | rc 0; 172 checks, 0 failures |
| MAAP datapath | `make -j8 -C tb/verilator/maap integration-build DP_MDIR="$WORK/integration-build"`, then the built binary from its directory | rc 0 / rc 0; 3 checks, 0 failures |
| MAAP campaign | `python3 tb/verilator/maap/mutants.py` | rc 0; 52 rows: 50 defects exit 1 at their named checks, 2 clean controls, 0 escapes |
| MAAP coverage | `make -j8 -C tb/verilator/maap coverage COV_MDIR="$WORK/coverage-build"` | rc 0; `KL_maap.sv` 215/215 lines, 95 % gate |
| Documentation set | the 94 commands of `r2-receipts/bank/docs_bank.py`: every `docs.yml` docs-check, wire-accountability and no-git command, plus the fast-workflow self-tests, `pp_srcs --check --selftest`, the `syn/ooc` and `syn/yosys` self-tests and mutants, and `check-baseline` | rc 0; 94/94 commands rc 0; em-dash base `8b61b709`; gate tree and `gptp-processor` clean afterwards |
| Design inputs | `python3 -I design_inputs.py <lane> <measured exports> <measured tree>` | rc 0; `route-1x1` a6574248..., `ooc-1x1` 80fe5d90..., `ooc-8x8` cf62186b... each equal the record; 122 / 119 / 119 measured-tree inputs, 0 differ at the lane head |
| Plan against record | `python3 -I plan_vs_record.py <lane>` | rc 0; 22 rows, 66 figures, 0 differences (`r2-receipts/plan-vs-record-head.log`) |
| Old plan against old record | the same script on dev `8b61b709`'s plan and record | rc 0; 0 differences: the old table described the #645/#647 record (`r2-receipts/plan-vs-record-dev.log`) |
| Lane quick checks | `docs_check.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_em_dash.py --base 8b61b709`, `check_doc_style.py`, `check_doc_paths.py`, `check_cpp_idiom.py`, `check_py_idiom.py`, `measure_test_evidence.py --check` | each rc 0 in the lane before committing; all are repeated in the documentation set at the head |
| Head identity | `git diff --name-only 030eb98a f909d6c4`; blob ids; gitlinks; commit format | 5 files (2 harness, 3 docs); RTL blobs and gitlinks equal `0df48637`; three one-line subjects, no body |
| Whitespace and tree | `git diff --check 030eb98a HEAD`; `git status --short` | rc 0; clean (`r2-receipts/whitespace.log`) |

Not rerun in round 2, with the reason:

| Gate | Last run | Why it still holds |
|---|---|---|
| Parent sweep (61/61), parser, portability (58/58), lint (90 <= 90), behaviour (404) | merge result `0df48637` | Their inputs are unchanged except the MAAP harness and campaign, whose suite entry (`make -C tb/verilator/maap` = unit run, then campaign) is the unit and campaign rows above |
| MAAP differential, firmware bank, pinned field campaigns | `0df48637` | No firmware, RTL or field-campaign input changed |
| `route-1x1`, `ooc-1x1`, `ooc-8x8`; MAAP ceiling | `0df48637` | The design inputs are byte-identical (row above); the assignment requires no re-measure |
| Hosted checks / local workflow replica | none at this head | Need the pushed head; no push in this assignment |
| Bench | none | Acceptance 4; post-merge bench lane |

## Coverage (author's view; the ledger is reviewer-owned)

| Lens | Covered clean at `030eb98a` by | Artifacts round 2 touches in that lens's scope | Author's reading |
|---|---|---|---|
| Conformance | R558-1, R559-1 | `MAAP_FABRIC.md` contract text (`:109`-`:110` new M5 sentence, `:137`-`:148`); RTL unchanged | Needs a reviewer's decision: the contract text changed, the implementation did not |
| RTL | R558-1, R559-1 | none: `KL_maap.sv`, `milan_datapath.sv`, `KL_pp_maap_shim.sv` unchanged | Unaffected |
| Robustness | R558-1, R559-1 | `sim_main.cpp` gains the M5 outage section | Needs a reviewer's decision (harness section added, RTL unchanged) |
| Tests | R558-1 clean; R559-1 unclean (F1, F3) | `sim_main.cpp`, `mutants.py` | Needs re-review |
| Docs | unclean in both (R558-1-F1; R559-1-F2, F3) | `MAAP_FABRIC.md`, `MARK_II_AREA_PLAN.md`, `docs/findings/README.md`, `PR-BODY.md` | Needs re-review |

This is author evidence, not a review verdict.

## Acceptance (unchanged by round 2)

| Acceptance | Status at `f909d6c4` |
|---|---|
| 1 | MET: M1, M2, M4, M5, M7 conformed; M5 now also graded for link loss; M8 discard conformed (counting withdrawn by ruling); M6 and M3 within documented, clause-cited limits |
| 2 | MET |
| 3 | MET: MAAP +6 / +60 at the merge result within +60 / +60; all three endpoints recorded at `0df48637` (`e6f00121`); inputs unchanged since |
| 4 | NOT RUN; post-merge bench lane |

## Round 2 receipts and boundary

- `r2-receipts/`: bounded, path-redacted receipts with `PROVENANCE.json` (raw and published digests) and `SCRATCH-ARTIFACTS.json` (files over 200 KB, by size and digest).
  It holds the bank logs (`bank/focus-r2/`, `bank/docs-r2/`), the plant patches and logs, `design-inputs.log`, `head-identity.log` and the scripts that produced them.
- `PR-BODY.md` is the updated, unpublished PR body (`Closes #696`); `REVIEW-READY-COMMENT-R2.md` is the posted comment text.
- The earlier files (`REVIEW-READY-COMMENT.md`, `STOP-COMMENT*.md`, `merge-receipts/` and the older receipt folders) are unchanged history.
- No push, PR creation or edit, merge, rebase, amend or history rewrite; no hardware or bench access. No job remains running.
- Reviewers named by the ruling: [R558] internal, [R559] external.

## Round 1 record (head `030eb98a`)

The rest of this file is the round-1 handoff as published, unchanged except for heading levels.

### Round 1 status: REVIEW READY

Published and read back identical: https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6092935897 (text in `REVIEW-READY-COMMENT.md`).

Head `030eb98a12685a2ca41cf8d785bb0eb69dc32a98`, branch `696-maap-annexb`, local only (no push, no PR).
Clean tree; fourteen first-parent commits over dev `6aa25dec`, the merge of dev `8b61b709` among them.
Ruling applied: https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6089712293 (option b, no floor exception),
on top of rulings 6080332335, 6079463350, 6079087547, 6076940309 and the assignment 6076750392.
The previous STOP (route floor) is https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6089695284 (text in `STOP-COMMENT.md`).

What this resume did, in order:

1. Merged dev `8b61b70902f3ebf118e56967277e2686731081bd` (`origin/dev` at fetch, the merge of #699) as merge commit `0df48637`. No rebase.
   No conflict; submodule pins unchanged. The lane's diff over dev is identical to its diff over `6aa25dec`, hunk headers aside.
2. Reran the full local bar at the merged head `0df48637`: parent sweep without any lock, parser, portability, lint, behaviour,
   the documentation set, the focused MAAP checks, the firmware bank and the pinned field campaigns. Every gate rc 0 (table below).
3. Re-measured `route-1x1`, `ooc-1x1` and `ooc-8x8` at `0df48637` through the recipe in one exclusive-lock job. All three gate checks exit 0.
4. Recorded all three through `pp_resource_gate.py record --write` and committed the record alone (`e6f00121`); `check-baseline` exits 0.
5. Updated the two documents that restate the gate's record (`030eb98a`) and reran the documentation set at that head: 94/94 rc 0.
6. Measured the MAAP block with its ceiling instrument at dev and at the merged head: within the ceiling.

No register-map, filter, mailbox, submodule-pin or policy change. No tolerance, floor or ceiling changed.

### Merged-head measurement

| Endpoint | Figures at `0df48637` | Against the #645/#647 record (dev) | Gate |
|---|---|---|---|
| `route-1x1` | LUT 50,230; FF 54,308; slice 15,823 (27 free); RAMB36 74; RAMB18 27; DSP 14; CARRY4 3,397; WNS +0.114 ns; WHS +0.036 ns; 101,344/101,344 nets routed, 0 errors; IOB packing 22 ports OK | LUT -37, FF -105, slice +44, WNS -0.185 ns, WHS +0.005 ns | `check` exit 0 |
| `ooc-1x1` | LUT 23,179; FF 19,779; RAMB36 16; RAMB18 3; DSP 8 | every figure equal | `check` exit 0 |
| `ooc-8x8` | LUT 30,135; FF 27,380; RAMB36 21; RAMB18 5; DSP 8 | every figure equal | `check` exit 0 |

The record's WNS +0.299 ns made the 0.25 ns fall limit bind first (at least +0.049 ns needed); +0.114 ns meets it and the +0.030 ns floor.
Route corners: Slow 0C/85C WNS +0.114 / WHS +0.102 ns; Fast 0C/85C WNS +1.518 / WHS +0.036 ns.

Worst setup path: `milansoc_crg_clkout0` (10 ns), slack +0.114 ns, 16 logic levels, data path 9.574 ns (logic 2.279, routing 7.295).
It runs from `milansoc_sdram_zqcs_timer_count1_reg[1]` to `milansoc_sdram_bankmachine1_level_reg[0]`, inside the soft CPU's SDRAM controller.
Receipt: `merge-receipts/route-queries/worst_path.rpt` and `worst10.rpt`.

MAAP in the routed checkpoint (same lock hold, `merge-receipts/route-queries/queries.log`):
`g_maap.maap_engine` 425 LUT / 339 FF (339 sequential cells).
The worst setup path into it keeps +4.037 ns (18 levels, from the PHC `ts_counter/acc_reg[31]` to `offset_r_reg[12]`).
The worst path out of it keeps +6.719 ns, and the worst hold into it +0.135 ns.

Slack history of `route-1x1` (all the same recipe identity F):

| Image | WNS ns | WHS ns | Critical path |
|---|---:|---:|---|
| F (#682) | +0.124 | +0.031 | AXI-Lite-to-Wishbone bridge to SPI-flash PHY counter, 18 levels |
| #686 record | +0.241 | +0.029 | - |
| #645/#647 record (dev `6aa25dec`) | +0.299 | +0.031 | `milansoc_write_w_buffer_level0_reg[1]` to `storage_13_dat1_reg[14]`, 14 levels |
| Lane head `39571196` (not recorded, previous STOP) | +0.029 | +0.015 | soft CPU DMA write bridge `downW_header_reg[3]` to `pendings_valids_reg[0]`, 19 levels |
| Merge `0df48637` (recorded) | +0.114 | +0.036 | SDRAM controller `zqcs_timer_count1_reg[1]` to `bankmachine1_level_reg[0]`, 16 levels |

Both worst paths in this lane lie outside `KL_maap` and `milan_datapath`; placement variation in unchanged soft-CPU logic explains the spread.

#### MAAP resources against the ceiling

Instrument: unchanged `syn/ooc/milan_datapath_ooc.tcl`, one synthesis and general thread, under the exclusive lock (`merge-receipts/maap-ooc-*`).
Ceiling (ruling 6079087547): +60 LUT / +60 FF at `g_maap.maap_engine` over the `6aa25dec` base of 439 / 280.

| Tree | `g_maap.maap_engine` LUT | FF | vs base `6aa25dec` | vs dev `8b61b709` | Within ceiling |
|---|---:|---:|---:|---:|---|
| Base `6aa25dec` (historical) | 439 | 280 | 0 / 0 | - | - |
| Dev `8b61b709` (no lane change) | 443 | 280 | +4 / 0 | 0 / 0 | - |
| Lane head `39571196` (historical, M3 committed) | 441 | 340 | +2 / +60 | - | yes |
| Merge `0df48637` | 445 | 340 | +6 / +60 | +2 / +60 | yes: 445 <= 499, 340 <= 340 |

The FF allowance is fully used, as before the merge. Dev's datapath edits alone move the block by +4 LUT.
Zero `Synth 8-4445` diagnostics in both runs; input hashes equal before and after.

### Changes in this resume

| Commit | Artifact | Change |
|---|---|---|
| `0df48637` | merge of dev `8b61b709` | Merge commit; one-line subject; no conflict. The lane's MAAP hunks at `hdl/milan/milan_datapath.sv:267`, `:7171` and `:7172` are intact |
| `e6f00121` | `syn/ooc/pp_resource_baseline.json:5`, `:470`, `:928` | `record --write` replaced the three records (figures and input digests) |
| `e6f00121` | `syn/ooc/pp_resource_baseline.json:451`, `:919`, `:1377` | `measured` notes name merge input `0df48637`, dev `8b61b709` and the passed comparison; identities, tolerances, floors and ceilings unchanged |
| `030eb98a` | `docs/design/AREA_BUDGET.md:13`, `:108` | Current record named as #696's merge of dev `8b61b709` |
| `030eb98a` | `docs/design/AREA_BUDGET.md:122`-`:127`, `:130`-`:134` | Headroom table ("the gate's record"), binding slice margin, critical path and preceding image |
| `030eb98a` | `docs/design/AREA_BUDGET.md:143`, `:148` | Datapath and wrapper LUTs and the NFR-RES-01 arithmetic at the new record |
| `030eb98a` | `docs/design/AREA_BUDGET.md:383` | Which WNS limit binds at the new record (the floor, after a 0.084 ns fall) |
| `030eb98a` | `docs/design/AREA_BUDGET.md:436`-`:438` | Seventh re-baseline: deltas against #645 and the routed `KL_maap` |
| `030eb98a` | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:6`, `:16`, `:32`-`:104` | Current-record pointer, generated contents entry (description hand-written) and the new re-baseline section |

### Merged-head gate table

WORK denotes disk-backed scratch. Commands are unpiped; each rc is the command's own.
Heads: `M` = merge `0df48637`; `F` = final `030eb98a` (adds only the record JSON and two documents to `M`).
Verilator builds used the pinned 5.050 through a two-slot build semaphore; never more than two compilations at once.

| Gate | Exact command | Head | Result |
|---|---|---|---|
| Parent sweep | `bash scripts/run_all_suites.sh "$WORK/parent-suites-logs"` (clean worktree, no flock) | M | rc 0; 61/61 suites, 2,185,905 checks, 0 failures, 0 timeouts; four declared field-campaign skips; 8,862 s |
| Pinned field campaigns | `TSN_GEN_ROOT="$FIELD_GENERATOR" make -j8 -C tb/verilator/tsn_fuzz` (generator at the `rtl.yml` pin, clean) | M | rc 0; AAF 164 and gPTP 677 pass, both freshness checks pass; the two generated pages differ only in their timestamp line (diff kept, scratch tree restored) |
| Parser | `python3 scripts/xvlog_gate.py --check` (exclusive lock) | M | rc 0; 81 + 52 sources, 0 findings |
| Portability | `bash syn/yosys/run.sh --results "$WORK/portability-results"` | M | rc 0; 58/58 tops, tied-input and tap-purity gates pass |
| Lint | `python3 scripts/lint_rtl.py --check --self-test --jobs 2` | M | rc 0; 90 <= 90 |
| Behaviour | `behave --no-capture -f plain` (in `tests`) | M | rc 0; 14 features, 404 scenarios, 1,968 steps |
| MAAP unit | `make -j8 -C tb/verilator/maap run MDIR="$WORK/unit-build"` | M | rc 0; 171 checks, 0 failures |
| MAAP datapath | `make -j8 -C tb/verilator/maap integration-build DP_MDIR="$WORK/integration-build"`, then the built binary | M | rc 0; 3 checks, 0 failures |
| MAAP campaign | `python3 tb/verilator/maap/mutants.py` | M | rc 0; 51 rows: 49 defects caught (rc 1, named check), 2 clean controls |
| MAAP coverage | `make -j8 -C tb/verilator/maap coverage COV_MDIR="$WORK/coverage-build"` | M | rc 0; `KL_maap.sv` 215/215 lines, 95 % gate |
| Differential | `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep "$WORK/differential"` | M | rc 0; 12/12 cases; 17/17 defects; clean sweep 5,173..5,810 cycles; MAC-ignoring 5,220..5,710, rejected at the highest-draw check |
| Firmware bank | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 2` | M | rc 0; host, RV32 and campaigns; general campaign 471/471 |
| Documentation set | 94 commands: every `docs.yml` docs-check, wire-accountability and no-git command, plus `pp_srcs --check --selftest`, the `syn/ooc` and `syn/yosys` self-tests and mutants, and `check-baseline` | M and F | rc 0 at both heads, tree clean; em-dash base `8b61b709` |
| Shipping exports | Recipe previews, emitted arguments without `--build`, helper with `--single-thread-synthesis` | M | every step rc 0; 122 / 119 inputs byte-identical to the lane; 6 / 6 images match |
| `route-1x1` | `baseline_integrated.tcl`, then `pp_resource_gate.py check ... --endpoint route-1x1` | M | Vivado rc 0 (50.2 min); check rc 0 |
| `ooc-1x1` | `baseline_ooc.tcl` with `--integrated-clock`, then `check ... --endpoint ooc-1x1` | M | Vivado rc 0 (22.3 min); check rc 0 |
| `ooc-8x8` | RTL elaboration for parameters, `baseline_ooc.tcl` with `--integrated-clock`, then `check ... --endpoint ooc-8x8` | M | Vivado rc 0 (1.2 + 43.0 min); check rc 0 |
| Input stability | Measurement-input digests before and after the job | M | equal: 1x1 `a6574248...`, 8x8 `e05f6bd1...` |
| Record | `record ... --write` for the three endpoints, `check` after each, `check-baseline` | M -> F | all rc 0; committed alone as `e6f00121` |
| MAAP ceiling | `syn/ooc/milan_datapath_ooc.tcl`, one thread, exclusive lock | dev and M | rc 0; 443/280 at dev; 445/340 at M |
| Whitespace and tree | `git diff --check 8b61b709 HEAD`; `git status --short` | F | clean |
| Hosted checks / local workflow replica | exact pushed PR head | - | NOT RUN: no push or PR in this assignment |
| Processor banks | protocol-processor `scripts/run_suites.sh`; gptp-processor `make -j8 tb` | - | Not rerun: pins and processor sources unchanged; last run at `963ad3b8e` passed (1,028,250 checks; gPTP bank) |
| Bench | Acceptance 4 | - | NOT RUN; separate post-merge lane |

The focused bank wrapper exited 1 only because the field campaign rewrote the timestamp lines of its two generated pages;
every one of its eleven commands returned 0 (`merge-receipts/focus-merged/`, `field-generated-diff.log`).
Vivado ran alone: the go file released the measurement job only after the sweep and the focused bank had ended.
Measurement lock hold 02:12-04:12; MAAP-ceiling hold 04:17-04:34. Largest Vivado peak 8,026 MB; no out-of-memory event.

### Acceptance coverage

| Acceptance | Status at `030eb98a` |
|---|---|
| 1. Each item conformed with a suite check and planted defect, or justified by clause | MET: M1, M2, M4, M5, M7 conformed; M8 discard conformed (counting withdrawn by ruling, documented); M6 and M3 conformed with explicit, clause-cited limits in `MAAP_FABRIC.md` (one-response capacity; pool-fold bias) |
| 2. M4 fixed in RTL first, datapath check with two MACs | MET (`39bf3d5f`); real-datapath check and reset-time defect pass at M |
| 3. OOC area and one shipping route within budget; records re-recorded through the recipe | MET: MAAP +6 / +60 against base (ceiling +60 / +60); route and both standalone endpoints pass the gate at the merge result and are recorded (`e6f00121`) |
| 4. Bench interop unchanged | NOT RUN; separate post-merge bench lane (assignment item 6) |

| Item | Clause | Status |
|---|---|---|
| M4 | B.3.4 NOTE; B.3.6.1 | Implemented first; datapath check and planted defect pass; consumer differential corrected and passing |
| M2 | B.3.6.6 | Implemented; check and planted defects pass |
| M7 | B.4; Table B.9 | Implemented; boundary checks and planted defects pass |
| M8 | B.2 | Discard implemented and tested; counting withdrawn by ruling and documented |
| M1 | Table B.7 note d; B.3.6.4 | Implemented; both-cell checks and planted defects pass |
| M5 | B.3.5.9; Table B.7 | Implemented; unit and real-datapath checks and defects pass |
| M6 | Table B.7; B.3.6.6 | Shared buffer retained; finite capacity explicitly documented |
| M3 | B.3.6.1 | 32-bit period, MAC-plus-clock seed; six planted defects pass; pool bias documented |

### Implementation summary

The fabric allocator samples the programmed MAC at first enable, echoes the PROBE requested range in DEFEND,
rejects supplied ranges outside the dynamic pool and discards truncated PDUs without protocol effects.
It applies the remaining MAC comparisons and re-probes on link return.
One shared buffer retains a response while PROBE or ANNOUNCE drains.
A 32-bit generator of period 2^32 - 1 is seeded at first enable from the low 32 bits of MAC plus the existing PHC,
and continues across Release/Begin retries.
The buffer holds one pending or transmitting DEFEND; further PROBEs while occupied remain unsupported, including during DEFEND.
Full Table B.7 conformance is not claimed. B.3.6.6 defines the response action; B.3.6.3 defines probe-count decrement.

### Commits and changes before this resume

Line numbers are at the current head. Only `milan_datapath.sv` moved, by dev's merged lines.

| Commit | Artifact | Change |
|---|---|---|
| `39bf3d5f` | `hdl/ieee1722/maap/KL_maap.sv:352` | M4: sample the programmed MAC on first enable |
| `39bf3d5f` | `tb/verilator/maap/sim_integration.cpp:18` | Different programmed MACs draw different intervals through real CSRs |
| `39bf3d5f` | `tb/verilator/maap/integration.mk:8` | Derive real datapath sources and generate images |
| `74692746` | `hdl/ieee1722/maap/KL_maap.sv:408` | M2: echo requested start and all sixteen count bits |
| `74692746` | `hdl/ieee1722/maap/KL_maap.sv:300` | M7: reject supplied ranges outside the dynamic pool |
| `74692746` | `hdl/ieee1722/maap/KL_maap.sv:193` | M8: require every PDU byte and complete final beat |
| `74692746` | `tb/verilator/maap/Makefile:17` | External build directories and unpiped coverage execution |
| `19cc4eec` | `hdl/ieee1722/maap/KL_maap.sv:285` | M1: both remaining MAC-ordering cells |
| `19cc4eec` | `hdl/ieee1722/maap/KL_maap.sv:433` | M5: operational rising event revokes and re-probes |
| `19cc4eec` | `hdl/milan/milan_datapath.sv:7171` | Drive operational input from existing effective link |
| `19cc4eec` | `tb/verilator/maap/sim_integration.cpp:39` | Link-return datapath check |
| `832ee972` | `tb/verilator/maap/sim_main.cpp:462` | M6: deferred response, intact current frame and exact-once checks |
| `832ee972` | `tb/verilator/maap/sim_main.cpp:707` | Pending-response cancellation on reset/release/restart/link return |
| `bc89c6c1` | `tb/verilator/maap/sim_main.cpp:78` | Missing frames fail checks instead of crashing the harness |
| `bb1940966` | `hdl/ieee1722/maap/KL_maap.sv:218` | Share pending and transmitting DEFEND storage |
| `bb1940966` | `hdl/ieee1722/maap/KL_maap.sv:242` | Separate own-range snapshots preserve PROBE/ANNOUNCE while storing a response |
| `bb1940966` | `hdl/ieee1722/maap/KL_maap.sv:296` | Prevent overwriting pending or active response data |
| `bb1940966` | `tb/verilator/maap/sim_main.cpp:394` | Active DEFEND integrity at stalls after 0, 2, 4 and 7 beats |
| `bb1940966` | `tb/verilator/maap/sim_main.cpp:483` | A later conflicting PROBE cannot replace the first pending response |
| `bb1940966` | `tb/verilator/maap/mutants.py:39` | Two occupied-buffer defects; refresh existing mutation anchors |
| `bb1940966` | `docs/design/MAAP_FABRIC.md:145` | Explicit shared-buffer capacity and precise clause citation |
| `313b20b34` | `sw/firmware/ctrl/test/test_maap_differential.cpp:176` | Program 1,024 MAC identities before first enable; preserve every bound and draw assertion |
| `313b20b34` | `sw/firmware/ctrl/test/maap_differential.py:18` | Permit the self-test to substitute one copied RTL source |
| `313b20b34` | `sw/firmware/ctrl/test/maap_differential.py:65` | Plant a MAC-ignoring generator and require its named highest-draw failure |
| `963ad3b8e` | `hdl/ieee1722/maap/doc/KL_maap/KL_maap.md:5` | MAC ordering, first-enable seeding, bounded supplied ranges and operational input |
| `963ad3b8e` | `sw/firmware/ctrl/maap/README.md:189` | Programmed-MAC sweep and named negative control |
| `c1bc77f4` | `docs/design/MAAP_FABRIC.md:153` | Measured shared-buffer area; M6 retained under the ceiling |
| `a872917ca` | `hdl/ieee1722/maap/KL_maap.sv:141` | M3: 32-bit maximal recurrence, MAC-plus-clock seed, nonzero fallback, explicit low-bit pool draw |
| `a872917ca` | `hdl/milan/milan_datapath.sv:7172` | Existing synchronous PHC supplies the seed input |
| `a872917ca` | `tb/verilator/maap/Makefile:18` | Unit harness can clock selected generator states |
| `a872917ca` | `tb/verilator/maap/sim_main.cpp:50` | Fixture MAC preserves overlap-test margins under direct-sum seeding |
| `a872917ca` | `tb/verilator/maap/sim_main.cpp:856` | Transition-map order, zero/carry/wrap seed cases, Release/Begin continuity |
| `a872917ca` | `tb/verilator/maap/sim_integration.cpp:147` | Same MAC at two PHC times changes probe intervals |
| `a872917ca` | `tb/verilator/maap/mutants.py:39`, `:224` | Five generator/seed defects; missing clock contribution fails the datapath check |
| `a872917ca` | `sw/firmware/ctrl/test/test_maap_differential.cpp:72`; `maap_differential.py:65` | Explicit zero clock in the isolated sweep; MAC-ignoring defect uses the new seed expression |
| `a872917ca` | `docs/design/MAAP_FABRIC.md:97`; `KL_maap.md:28`; `sw/firmware/ctrl/maap/README.md:190` | Period/seed contract, cost, live-clock integration, retained pool bias |
| `395711960` | `hdl/milan/milan_datapath.sv:267` | Area comment points to the measured contract |

### Tests and planted defects

All existing clause checks remain; no threshold was loosened. A detected defect requires a successful build, process status 1 and its named failure.
Compiler failures and abnormal exits never count as detections. Every row below ran again at the merged head (campaign rc 0, 51 rows).

| Item | Named check | Planted defect | Result at M |
|---|---|---|---|
| M3 | M3 B.3.6.1 generator period is 2^32-1 | `m3_short_period` | Caught, rc 1 |
| M3 | M3 B.3.6.1 generator period is 2^32-1 | `m3_trap_outside_basis` | Caught, rc 1 |
| M3 | M3 B.3.6.1 first enable seeds MAC plus clock | `m3_ignores_clock` | Caught, rc 1 |
| M3 | M3 B.3.6.1 first enable seeds MAC plus clock | `m3_xors_clock` | Caught, rc 1 |
| M3 | M3 Release/Begin retains the generator sequence | `m3_reseeds_after_release` | Caught, rc 1 |
| M3 | M3 datapath: real-time clock changes probe intervals | `m3_datapath_ignores_clock` | Caught, rc 1 |
| M6 | M6 occupied response buffer preserves active DEFEND | `m6_overwrite_active_response` | Caught, rc 1 |
| M6 | M6 pending response preserves prober and requested range | `m6_replace_pending_response` | Caught, rc 1 |
| M6 | M6 pending response cancelled with allocation | `m6_pending_survives_release` | Caught, rc 1 |
| M6 | M6 busy PROBE gets DEFEND after wire is free | `m6_drop_busy_probe` | Caught, rc 1 |
| M6 | M6 pending response preserves prober and requested range | `m6_pending_source_not_saved` | Caught, rc 1 |
| M5 | M5 B.3.5.9 link return revokes and reprobes | `m5_ignore_link_return` | Caught, rc 1 |
| M5 | M5 B.3.5.9 link return restarts PROBE | `m5_level_restarts` | Caught, rc 1 |
| M5 | Link return starts four fresh PROBEs through the datapath | `m5_datapath_ignores_link` | Caught, rc 1 |
| M1 | M1 rProbe/PROBE lower MAC keeps range | `m1_probe_no_compare` | Caught, rc 1 |
| M1 | M1 rDefend/DEFEND lower MAC keeps range | `m1_defend_no_compare` | Caught, rc 1 |
| M8 | M8 B.2 truncated PROBE-state input has no effect | `m8_early_last_accepted` | Caught, rc 1 |
| M8 | M8 B.2 truncated DEFEND-state input has no effect | `m8_missing_bytes_accepted` | Caught, rc 1 |
| M7 | M7 Table B.9 invalid supplied range refused | `m7_accept_invalid_seed` | Caught, rc 1 |
| M7 | M7 Table B.9 valid supplied boundary retained | `m7_reject_valid_boundary` | Caught, rc 1 |
| M2 | M2 B.3.6.6 requested start echoes PROBE | `m2_own_requested_start` | Caught, rc 1 |
| M2 | M2 B.3.6.6 requested count echoes all 16 bits | `m2_own_requested_count` | Caught, rc 1 |
| M4 | Programmed MAC changes probe intervals through real CSRs | `m4_reset_time_sampling` | Caught, rc 1 |
| 1 | B.2.1 cdl 16 (Begin! PROBE 1) | `cdl_28` | Caught, rc 1 |
| 1 | B.2.1 DEFEND DA = PROBE source (above) | `defend_to_multicast` | Caught, rc 1 |
| 1 | B.2.1 DEFEND DA latched at send | `defend_destination_not_latched` | Caught, rc 1 |
| 1 | B.2.1 PROBE DA multicast (Begin! 1) | `every_frame_to_the_prober` | Caught, rc 1 |
| 2 | B.3.4.2 probe T < 600 ms (campaign) | `probe_draw_7_bits` | Caught, rc 1 |
| 2 | B.3.4.2 probe T > 500 ms (campaign) | `probe_base_500` | Caught, rc 1 |
| 2 | B.3.4.1 announce T > 30 s | `announce_base_3s` | Caught, rc 1 |
| 2 | B.3.4.1 announce T < 32 s | `announce_draw_11_bits` | Caught, rc 1 |
| 2 | B.3.4.1 announce T randomized | `announce_not_randomized` | Caught, rc 1 |
| 2 | B.3.4.2 probe T randomized (zero-seed MAC) | `zero_seed_freezes_the_probe_draw` | Caught, rc 1 |
| 2 | B.3.4.1 announce T randomized (zero-seed MAC) | `zero_seed_freezes_the_announce_draw` | Caught, rc 1 |
| 3 | B.2.7 ANNOUNCE conflict_* is not its range | `announce_judged_on_conflict_fields` | Caught, rc 1 |
| 3 | note b adjacent above: no conflict | `inclusive_range_end` | Caught, rc 1 |
| 3 | note b adjacent below: no conflict | `inclusive_range_start` | Caught, rc 1 |
| 3 | note b empty range: no conflict | `empty_range_conflicts` | Caught, rc 1 |
| 3 | T.B7 note d: lower MAC keeps range | `no_compare_mac` | Caught, rc 1 |
| 3 | T.B7 rAnnounce!/PROBE: no compare_MAC | `compare_mac_while_probing` | Caught, rc 1 |
| 3 | T.B7 rAnnounce!/DEFEND: re-address | `compare_mac_unreversed` | Caught, rc 1 |
| 4 | T.B7 Begin!: four PROBEs before ANNOUNCE | `three_probes` | Caught, rc 1 |
| 4 | T.B7 Begin!: first PROBE at once | `first_probe_after_a_timer` | Caught, rc 1 |
| 4 | T.B7 Restart!: first PROBE at once | `restart_probe_after_a_timer` | Caught, rc 1 |
| 4 | T.B7 probeCount!: ANNOUNCE at once (Begin!) | `announce_after_a_timer` | Caught, rc 1 |
| 0 | frame on the wire keeps its offset | `restart_rewrites_the_frame_on_the_wire` | Caught, rc 1 |
| 0 | B.2.8 conflict_count = overlap (below) | `overlap_count_to_our_end` | Caught, rc 1 |
| 0 | PROBE mid-frame: frame on the wire byte-identical | `defend_rewrites_the_frame_on_the_wire` | Caught, rc 1 |
| 0 | note b: this station's empty range never conflicts | `own_empty_range_conflicts` | Caught, rc 1 |
| control | unit harness unmodified | `clean` | rc 0 |
| control | datapath harness unmodified | `m4_datapath_clean` | rc 0 |

M8 compares malformed input with cycle-matched idle RX: lengths 1..41 and missing bytes 0..41, all three types, in PROBE and DEFEND states.

| Differential check | Planted defect | Result at M |
|---|---|---|
| Golden probe/announce wire | `wire`: control-data length 28 | Caught |
| Release and retry | `release`: remain in DEFEND | Caught |
| Nine Table B.7 cells | `maap-table-b7-0/1/2/6/7/8/12/13/14` | All nine caught |
| Strict probe timing | `probe-1ms`, `probe-500ms`, `probe-600ms` | All three caught |
| Fabric draw bound | `parent-probe-bound`: expected maximum 499 ms | Caught |
| Fabric probe count | `parent-probe-count`: expect four total frames | Caught |
| Highest draw across 1,024 programmed identities | `parent-ignores-mac`: constant seed | Caught at the named coverage assertion |

### Area attribution (assignment item 5)

Instrument: `syn/ooc/milan_datapath_ooc.tcl`, Arty 1x1 geometry, one synthesis and general thread.

| Cumulative item | Clause | MAAP LUT | MAAP FF | LUT vs base | FF vs base |
|---|---|---:|---:|---:|---:|
| base `6aa25dec` | Baseline | 439 | 280 | +0 | +0 |
| M4 | B.3.4 NOTE; B.3.6.1 | 460 | 281 | +21 | +1 |
| M2 | B.3.6.6 | 473 | 297 | +34 | +17 |
| M7 | B.4; Table B.9 | 483 | 297 | +44 | +17 |
| M8 | B.2, amended ruling | 498 | 298 | +59 | +18 |
| M1 | Table B.7 note d; B.3.6.4 | 491 | 298 | +52 | +18 |
| M5 | B.3.5.9; Table B.7 | 456 | 299 | +17 | +19 |
| M6 original, replaced | Table B.7; B.3.6.6 | 518 | 380 | +79 | +100 |
| M6 shared, from M5 | Table B.7; B.3.6.6 | 457 | 324 | +18 | +44 |
| M3, after shared M6 | B.3.6.1 | 441 | 340 | +2 | +60 |
| Merge `0df48637` | all, on dev `8b61b709` | 445 | 340 | +6 | +60 |

The first rows are historical recipe results (`fresh-receipts/area/`, `final-receipts/area/`); the last row is this resume's.

### Independent review coverage

| Lens | Covering round | Head |
|---|---|---|
| Conformance | Pending independent review | None |
| RTL | Pending independent review | None |
| Robustness | Pending independent review | None |
| Tests | Pending independent review | None |
| Docs | Pending independent review | None |

This is author evidence, not a review verdict. No merge readiness or physical acceptance is claimed.

### Receipts and resume boundary

- `merge-receipts/`: this resume's bounded, path-redacted receipts (681 files) with `PROVENANCE*.json` (raw and published digests).
  `SCRATCH-ARTIFACTS.json` lists the 34 artifacts over 200 KB (logs, timing reports, checkpoints) by size and digest; they stay in scratch.
  The executed bank scripts are included (`parent_bank.py`, `docs_bank.py`, `focus_bank.py`, `vivado_bank.py`, `maap_ooc_bank.py`, `record_merge.py`).
- `route-stop-receipts/`, `final-receipts/`, `consumer-resume-receipts/`, `resume-receipts/`, `fresh-receipts/`: earlier sessions, unchanged.
- `STOP-COMMENT.md` (route-floor STOP) and `STOP-COMMENT-6080309288.md` (documentation-scope STOP) are historical.
- `PR-BODY.md` is the unpublished PR body (`Closes #696`).
- Scratch worktrees (validation, parent sweep, gate trees at M and F, dev) are detached and outside the lane; the lane tree is clean.
- No push, PR creation or edit, merge, rebase, amend or history rewrite; no hardware access. No job remains running.
- Reviewers named by the ruling: [R558] internal, [R559] external.
