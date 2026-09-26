[A337] REVIEW READY

Issue #231, PR #572. Local head: `0a506fa8f0032d21e9614a617b75b0a57dc5f2e4`.
Starting head: `af6d19c553ad8c445a80528344baf2273b41ad46`. Branch: `231-pp-shadow-baseline`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
All five round-two items are addressed. No RTL or donor bytes changed.
The commit is unpushed; independent re-review and publication remain pending.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/231#issuecomment-5846064333

Public review packet: `e21bc530eb89f7bd325f8d774aad5b5d95c70c1c`.
It was fetched read-only into temporary scratch, then extracted.
The temporary fetch was deleted.
Raw reports, commands, logs, checkpoints and hashes remain under
`$VALIDATION_STORAGE/231-a337-work`.
This output directory contains only summaries, tables and prepared prose.

## Changes

| File and line | Change |
|---|---|
| `docs/findings/PP_SHADOW_BASELINE.md:58` | Separate default totals, attribution, probe evidence and mapping explanation. |
| `docs/findings/PP_SHADOW_BASELINE_MAPPING.tsv:1` | Complete disjoint raw logic-LUT reconciliation. |
| `docs/findings/PP_SHADOW_BASELINE_RANKING.tsv:1` | All direct-child LUT and FF ranks, own logic and reconciliation rows. |
| `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:170` | Reproduction commands and the clean-export citation repair. |
| `syn/ooc/pp_baseline.py:185` | Boundary-preserving variant, unfiltered hierarchy and real preparation self-tests. |
| `syn/ooc/pp_baseline_rank.py:19` | Complete hierarchy ranking with parent reconciliation. |
| `syn/ooc/pp_baseline_mapping.py:26` | Disjoint module expansion, primitive accounting and flattening residual. |
| `syn/ooc/pp_baseline_mutants.py:12` | Ten enforcement-removal mutants and a passing control. |
| `syn/ooc/pp_baseline_reports_selftest.py:13` | Ancestry, sharing, omission, multiplicity, blackboxes and residual tests. |
| `.github/workflows/rtl-fast.yml:209` | Run the baseline checks in fast CI. |
| `scripts/ci_events.py:2325` | Bind the new commands in the canonical CI contract. |

## Attribution versus default

Only the attribution variant adds the wrapper KEEP_HIERARCHY constraint.
Every reopened attribution checkpoint reports that property as TRUE.
All 20 parameters and all six image hashes match each product shape.
Sources, part, directives and clocks otherwise remain matched.
The two 118-source exports match after normalizing external work roots.
Generated Verilog also has timestamp and hierarchy-comment differences.
Removing those comments proves the generated executable Verilog identical.
See source-comparison.json for the source hashes and comparison receipt.
Default whole-design totals remain the published fit baseline.

| Attribution-only wrapper | LUT | FF | RAMB36 | RAMB18 | DSP | CARRY4 | Internal WNS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1x1 synthesis | 22,314 | 24,535 | 21 | 3 | 5 | 1,415 | -1.201 |
| 1x1 route | 20,655 | 23,558 | 21 | 3 | 5 | 1,321 | +0.041 |
| 8x8 synthesis | 29,489 | 32,991 | 26 | 5 | 8 | 1,809 | -10.846 |

| Endpoint | Whole LUT, default / attribution | Wrapper-name LUT, default / attribution | AECP LUT, default / attribution | Dynamic-state LUT, default / attribution |
|---|---:|---:|---:|---:|
| 1x1 synthesis | 51,125 / 52,210 | 23,272 / 22,314 | 6,639 / 4,678 | 1,296 / 111 |
| 1x1 route | 48,618 / 48,825 | 22,441 / 20,655 | 6,428 / 4,504 | 1,299 / 111 |
| 8x8 synthesis | 68,136 / 70,206 | 37,809 / 29,489 | 15,199 / 5,025 | 6,915 / 574 |

The 1x1 attribution route has WNS +0.041 ns and WHS +0.015 ns.
It has zero failing setup, hold and pulse-width endpoints.
Those margins describe the attribution variant, not a new shipping result.

## Boundary probes

| Synthesis scope | Raw LUT cells, default / attribution | Only external loads, default / attribution | External input and only external loads, default / attribution |
|---|---:|---:|---:|
| 1x1 `u_pp/u_aecp/u_dyn` | 1,624 / 144 | 763 / 0 | 476 / 0 |
| 1x1 `u_pp/u_aecp` | 7,649 / 5,269 | 903 / 18 | 574 / 0 |
| 1x1 `u_pp/u_srp` | 4,960 / 4,947 | 87 / 96 | 86 / 96 |
| 1x1 `u_pp/u_notify` | 3,419 / 3,361 | 0 / 0 | 0 / 0 |
| 1x1 `wrapper` | 26,213 / 24,983 | 1,175 / 173 | 792 / 131 |
| 8x8 `u_pp/u_aecp/u_dyn` | 8,817 / 607 | 5,922 / 0 | 3,108 / 0 |
| 8x8 `u_pp/u_aecp` | 17,872 / 5,607 | 6,187 / 18 | 3,357 / 0 |
| 8x8 `u_pp/u_srp` | 9,110 / 9,480 | 74 / 442 | 67 / 432 |
| 8x8 `u_pp/u_notify` | 3,565 / 3,027 | 1 / 0 | 0 / 0 |
| 8x8 `wrapper` | 42,962 / 32,833 | 6,397 / 519 | 3,499 / 467 |

The public boundary.tcl and loads.tcl ran unchanged at all three attribution endpoints.
They retain the original two-thread setting and all return rc 0.
Counts describe raw LUT cells, not combined Slice LUT utilization.
The classification does not measure reverse relocation.

| Attribution endpoint | Dynamic-state raw LUT cells | Only external loads | External input and only external loads | Load-histogram rows |
|---|---:|---:|---:|---:|
| attribution-synth-1x1 | 144 | 0 | 0 | 0 |
| attribution-route-1x1 | 143 | 0 | 0 | 0 |
| attribution-synth-8x8 | 607 | 0 | 0 | 0 |

## Mapping reconciliation

| Raw logic contribution | Hierarchical Yosys 1x1 | Raw Vivado 1x1 | Difference 1x1 | Hierarchical Yosys 8x8 | Raw Vivado 8x8 | Difference 8x8 |
|---|---:|---:|---:|---:|---:|---:|
| `u_pp/u_srp` | 13,924 | 4,971 | 8,953 | 28,045 | 9,423 | 18,622 |
| `u_pp` own logic | 7,075 | 628 | 6,447 | 11,381 | 505 | 10,876 |
| `u_pp/u_notify` | 7,090 | 3,305 | 3,785 | 6,387 | 3,083 | 3,304 |
| Remaining disjoint scopes | 20,826 | 16,037 | 4,789 | 24,409 | 19,339 | 5,070 |
| Hierarchical total | 48,915 | 24,941 | 23,974 | 70,222 | 32,350 | 37,872 |
| Flattening residual | -7,657 | 0 | -7,657 | -4,498 | 0 | -4,498 |
| Original flattened total | 41,258 | 24,941 | 16,317 | 65,724 | 32,350 | 33,374 |

Complete rows are in PP_SHADOW_BASELINE_MAPPING.tsv.
Both flattened runs reproduce the published counts exactly.
Independent aggregate statistics match both hierarchical totals.
The flattening residual is global, without guessed per-module savings.

## Mutants

| Enforcement removed | Self-test rc | Result |
|---|---:|---|
| control | 0 | Control passes |
| ROM error promotion | 1 | Killed |
| readmemh inventory equality | 1 | Killed |
| empty SRAM requirement | 1 | Killed |
| parameter ROM depth | 1 | Killed |
| outside repository guard | 1 | Killed |
| image depth | 1 | Killed |
| image width | 1 | Killed |
| hexadecimal image words | 1 | Killed |
| attribution constraint loading | 1 | Killed |
| attribution boundary preservation | 1 | Killed |

The original external-review mutant driver was rerun unchanged.
Its control passed; all five original mutants were killed.
The internal-review SRAM mutant is also killed.

## Gates

Commands ran in the foreground, with separate logs and no output pipelines.
These are final results after correcting the initial CI command-record mismatch.

| Gate | Command | rc |
|---|---|---:|
| nvm-firmware | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 |
| nvm-capture | `python3 scripts/check_nvm_capture.py` | 0 |
| baremetal | `python3 scripts/check_baremetal_only.py --check` | 0 |
| ci-events-check | `python3 scripts/ci_events.py --check` | 0 |
| ci-events-selftest | `python3 scripts/ci_events.py --selftest` | 0 |
| xvlog | `python3 scripts/xvlog_gate.py --check` | 0 |
| rtl-source-lists | `python3 scripts/check_rtl_source_lists.py` | 0 |
| sv-idiom | `python3 scripts/check_sv_idiom.py` | 0 |
| rtl-lint | `python3 scripts/lint_rtl.py --check` | 0 |
| cpp-idiom | `python3 scripts/check_cpp_idiom.py` | 0 |
| py-idiom | `python3 scripts/check_py_idiom.py` | 0 |
| port-contracts | `python3 scripts/check_port_contracts.py` | 0 |
| naming | `python3 scripts/measure_naming.py --check` | 0 |
| test-evidence | `python3 scripts/measure_test_evidence.py --check` | 0 |
| behave | `cd tests && behave --no-capture -f plain` | 0 |
| baseline-selftest | `python3 -B syn/ooc/pp_baseline.py --selftest` | 0 |
| baseline-mutants | `python3 -B syn/ooc/pp_baseline_mutants.py` | 0 |
| builder-sdk | `python3 sw/builder/test_builder.py` | 0 |
| builder-absent | `python3 sw/builder/test_builder.py` | 0 |
| docs-git | `python3 -B scripts/docs_check.py` | 0 |
| em-dash | `python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 |
| doc-style | `python3 scripts/check_doc_style.py` | 0 |
| toc | `python3 scripts/gen_toc.py --check` | 0 |
| anchors | `python3 scripts/gen_toc.py --verify-anchors` | 0 |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0 |
| module-matrix | `python3 docs/traceability/gen_module_matrix.py --check` | 0 |
| baseline-report-selftest | `python3 -B syn/ooc/pp_baseline_reports_selftest.py` | 0 |
| diff | `git diff --check` | 0 |
| docs-no-git | `python3 -B scripts/docs_check.py` | 0 |
| doc-paths-clean | `python3 scripts/check_doc_paths.py` | 0 |

Compiler selection used an explicit target-compiler selector.
SDK mode redirected the existing selector to the freshly verified pinned SDK.
Its audit records 855 compiler invocations, including expected negative test arms.
Absent mode refused all three target candidates and executed none.
Host C remained available for ordinary host tests.
SDK mode has one NOT RUN arm: missing historical calibration data.
Absent mode additionally skips the target compiled CSR census.
These are named limits, not target or calibration evidence.
The front-end gate retains four existing processor findings within its ratchet.
The clean-export path gate passed with builder output absent.
Both documentation CI modes returned rc 0.

Reproduction controllers under the raw-work root:
`run-builder.py`, `run-code-gates.py`, `run-doc-gates.py`,
and `run-final-clean-export.py` record the environments, working directories
and foreground invocations. Gate logs are under `gates/`.
The compiler selector is `compiler-selector/sitecustomize.py`.
The three temporary artifact symlinks were removed; see `cleanup.json`.

## Measurement receipts

| Measurement | rc |
|---|---:|
| ax7101 attribution | 0 |
| ax8x8 attribution | 0 |
| ax7101 flattened mapping | 0 |
| ax7101 hierarchical mapping | 0 |
| ax8x8 flattened mapping | 0 |
| ax8x8 hierarchical mapping | 0 |

Default checkpoint reports were reopened with the small-instance filter disabled.
Every previously published hierarchy row still matches exactly.
Both attribution logs contain zero Synth 8-4445 diagnostics.
Input images were rehashed after the runs.
Executed-script hashes: input-validation-final.json.
Report sizes and SHA-256 hashes: report-manifest.json.
Existing clock warnings and I/O-delay omissions remain documented.
No bitstream or hardware operation was performed.

## Complete ranking

Threshold zero. Every reported direct wrapper and processor child appears.
LUT and FF ranks are separate; ties use lexical instance order.
@own is the report own-logic row; @total is the parent.
@reconciliation records cross-child LUT sharing.
The TSV also records logic LUT, LUTRAM, SRL, RAMB36, RAMB18 and DSP.

### ooc-1x1

| Scope | Instance | LUT rank | FF rank | LUT | FF |
|---|---|---:|---:|---:|---:|
| wrapper | u_pp | 1 | 1 | 21762 | 23704 |
| wrapper | u_nvm | 2 | 2 | 507 | 469 |
| wrapper | ctl_fifo | 3 | 4 | 79 | 33 |
| wrapper | @own | 4 | 3 | 11 | 327 |
| wrapper | @reconciliation |  |  | -9 | 0 |
| wrapper | @total |  |  | 22350 | 24533 |
| u_pp | u_aecp | 1 | 4 | 4663 | 3010 |
| u_pp | u_srp | 2 | 1 | 4296 | 6377 |
| u_pp | u_notify | 3 | 2 | 3150 | 3299 |
| u_pp | u_listener | 4 | 5 | 1553 | 1099 |
| u_pp | u_dispatch | 5 | 9 | 879 | 759 |
| u_pp | u_talker | 6 | 10 | 860 | 514 |
| u_pp | u_originator | 7 | 7 | 771 | 885 |
| u_pp | u_nvm_shadow | 8 | 6 | 746 | 1083 |
| u_pp | u_maap | 9 | 11 | 727 | 499 |
| u_pp | u_timer | 10 | 15 | 694 | 179 |
| u_pp | u_adp | 11 | 12 | 622 | 463 |
| u_pp | @own | 12 | 3 | 566 | 3242 |
| u_pp | u_rx_validator | 13 | 8 | 510 | 773 |
| u_pp | u_nvm_port | 14 | 19 | 271 | 121 |
| u_pp | u_event_router | 15 | 24 | 233 | 51 |
| u_pp | u_tx_slots | 16 | 18 | 219 | 138 |
| u_pp | u_tx_arbiter | 17 | 14 | 186 | 187 |
| u_pp | u_prng | 18 | 17 | 156 | 150 |
| u_pp | u_ca_builder | 19 | 16 | 155 | 152 |
| u_pp | g_rx_pool[5].u_rx_slots | 20 | 23 | 90 | 62 |
| u_pp | u_mrp_strip | 21 | 20 | 72 | 107 |
| u_pp | u_scoreboard | 22 | 21 | 63 | 73 |
| u_pp | u_side_port | 23 | 29 | 53 | 6 |
| u_pp | g_rx_pool[2].u_rx_slots | 24 | 22 | 52 | 62 |
| u_pp | g_rx_pool[0].u_rx_slots | 25 | 25 | 44 | 38 |
| u_pp | g_rx_pool[4].u_rx_slots | 26 | 27 | 40 | 22 |
| u_pp | u_trace | 27 | 28 | 40 | 18 |
| u_pp | g_rx_pool[1].u_rx_slots | 28 | 26 | 29 | 22 |
| u_pp | u_normalizer | 29 | 13 | 16 | 304 |
| u_pp | u_nvm_arb | 30 | 31 | 6 | 3 |
| u_pp | u_lsn_admit | 31 | 33 | 2 | 1 |
| u_pp | u_desc_mem_guard | 32 | 32 | 1 | 1 |
| u_pp | u_release_merge | 33 | 30 | 0 | 4 |
| u_pp | @reconciliation |  |  | -3 | 0 |
| u_pp | @total |  |  | 21762 | 23704 |

### ooc-8x8

| Scope | Instance | LUT rank | FF rank | LUT | FF |
|---|---|---:|---:|---:|---:|
| wrapper | u_pp | 1 | 1 | 28166 | 31600 |
| wrapper | u_nvm | 2 | 2 | 745 | 1024 |
| wrapper | ctl_fifo | 3 | 4 | 79 | 33 |
| wrapper | @own | 4 | 3 | 11 | 327 |
| wrapper | @reconciliation |  |  | -9 | 0 |
| wrapper | @total |  |  | 28992 | 32984 |
| u_pp | u_srp | 1 | 1 | 8302 | 11130 |
| u_pp | u_aecp | 2 | 3 | 5053 | 4152 |
| u_pp | u_notify | 3 | 4 | 2948 | 3799 |
| u_pp | u_listener | 4 | 5 | 1669 | 1131 |
| u_pp | u_timer | 5 | 14 | 1452 | 217 |
| u_pp | u_talker | 6 | 10 | 1354 | 522 |
| u_pp | u_rx_validator | 7 | 8 | 861 | 773 |
| u_pp | u_dispatch | 8 | 9 | 857 | 759 |
| u_pp | u_maap | 9 | 11 | 846 | 506 |
| u_pp | u_adp | 10 | 12 | 798 | 449 |
| u_pp | u_originator | 11 | 7 | 767 | 881 |
| u_pp | u_nvm_shadow | 12 | 6 | 724 | 978 |
| u_pp | @own | 13 | 2 | 448 | 4700 |
| u_pp | u_event_router | 14 | 19 | 389 | 129 |
| u_pp | u_tx_slots | 15 | 18 | 343 | 138 |
| u_pp | u_nvm_port | 16 | 20 | 333 | 124 |
| u_pp | u_tx_arbiter | 17 | 15 | 180 | 187 |
| u_pp | u_ca_builder | 18 | 16 | 168 | 152 |
| u_pp | u_prng | 19 | 17 | 158 | 150 |
| u_pp | g_rx_pool[5].u_rx_slots | 20 | 24 | 95 | 62 |
| u_pp | u_mrp_strip | 21 | 21 | 77 | 107 |
| u_pp | u_scoreboard | 22 | 22 | 73 | 73 |
| u_pp | u_side_port | 23 | 29 | 54 | 6 |
| u_pp | g_rx_pool[2].u_rx_slots | 24 | 23 | 52 | 62 |
| u_pp | g_rx_pool[4].u_rx_slots | 25 | 27 | 42 | 22 |
| u_pp | g_rx_pool[0].u_rx_slots | 26 | 25 | 40 | 38 |
| u_pp | g_rx_pool[1].u_rx_slots | 27 | 26 | 33 | 22 |
| u_pp | u_trace | 28 | 28 | 28 | 18 |
| u_pp | u_normalizer | 29 | 13 | 18 | 304 |
| u_pp | u_nvm_arb | 30 | 31 | 4 | 3 |
| u_pp | u_desc_mem_guard | 31 | 32 | 1 | 1 |
| u_pp | u_lsn_admit | 32 | 33 | 0 | 1 |
| u_pp | u_release_merge | 33 | 30 | 0 | 4 |
| u_pp | @reconciliation |  |  | -1 | 0 |
| u_pp | @total |  |  | 28166 | 31600 |

### default-synth-1x1

| Scope | Instance | LUT rank | FF rank | LUT | FF |
|---|---|---:|---:|---:|---:|
| wrapper | u_pp | 1 | 1 | 22775 | 22678 |
| wrapper | u_nvm | 2 | 2 | 423 | 469 |
| wrapper | ctl_fifo | 3 | 4 | 74 | 33 |
| wrapper | @own | 4 | 3 | 9 | 319 |
| wrapper | @reconciliation |  |  | -9 | 0 |
| wrapper | @total |  |  | 23272 | 23499 |
| u_pp | u_aecp | 1 | 4 | 6639 | 3013 |
| u_pp | u_srp | 2 | 1 | 4329 | 6210 |
| u_pp | u_notify | 3 | 2 | 3231 | 3299 |
| u_pp | u_listener | 4 | 5 | 1506 | 1106 |
| u_pp | u_originator | 5 | 7 | 756 | 885 |
| u_pp | u_nvm_shadow | 6 | 6 | 755 | 1083 |
| u_pp | u_talker | 7 | 10 | 750 | 480 |
| u_pp | u_timer | 8 | 14 | 717 | 179 |
| u_pp | u_dispatch | 9 | 9 | 711 | 579 |
| u_pp | u_rx_validator | 10 | 8 | 533 | 695 |
| u_pp | u_adp | 11 | 11 | 450 | 455 |
| u_pp | @own | 12 | 3 | 390 | 3164 |
| u_pp | u_tx_slots | 13 | 17 | 355 | 138 |
| u_pp | u_nvm_port | 14 | 18 | 266 | 121 |
| u_pp | u_event_router | 15 | 24 | 230 | 51 |
| u_pp | u_maap | 16 | 23 | 199 | 54 |
| u_pp | u_tx_arbiter | 17 | 13 | 184 | 187 |
| u_pp | u_prng | 18 | 16 | 143 | 150 |
| u_pp | u_ca_builder | 19 | 15 | 125 | 152 |
| u_pp | g_rx_pool[5].u_rx_slots | 20 | 22 | 81 | 62 |
| u_pp | u_mrp_strip | 21 | 19 | 73 | 107 |
| u_pp | u_scoreboard | 22 | 20 | 66 | 73 |
| u_pp | g_rx_pool[2].u_rx_slots | 23 | 21 | 53 | 62 |
| u_pp | u_side_port | 24 | 29 | 53 | 6 |
| u_pp | g_rx_pool[0].u_rx_slots | 25 | 25 | 48 | 38 |
| u_pp | u_trace | 26 | 28 | 40 | 18 |
| u_pp | g_rx_pool[4].u_rx_slots | 27 | 27 | 33 | 22 |
| u_pp | g_rx_pool[1].u_rx_slots | 28 | 26 | 32 | 22 |
| u_pp | u_normalizer | 29 | 12 | 17 | 258 |
| u_pp | u_nvm_arb | 30 | 31 | 12 | 3 |
| u_pp | u_desc_mem_guard | 31 | 32 | 1 | 1 |
| u_pp | u_lsn_admit | 32 | 33 | 1 | 1 |
| u_pp | u_release_merge | 33 | 30 | 0 | 4 |
| u_pp | @reconciliation |  |  | -4 | 0 |
| u_pp | @total |  |  | 22775 | 22678 |

### default-route-1x1

| Scope | Instance | LUT rank | FF rank | LUT | FF |
|---|---|---:|---:|---:|---:|
| wrapper | u_pp | 1 | 1 | 21980 | 22672 |
| wrapper | u_nvm | 2 | 2 | 391 | 469 |
| wrapper | ctl_fifo | 3 | 4 | 73 | 33 |
| wrapper | @own | 4 | 3 | 9 | 319 |
| wrapper | @reconciliation |  |  | -12 | 0 |
| wrapper | @total |  |  | 22441 | 23493 |
| u_pp | u_aecp | 1 | 4 | 6428 | 3013 |
| u_pp | u_srp | 2 | 1 | 4166 | 6203 |
| u_pp | u_notify | 3 | 2 | 3158 | 3299 |
| u_pp | u_listener | 4 | 5 | 1381 | 1107 |
| u_pp | u_originator | 5 | 7 | 743 | 885 |
| u_pp | u_nvm_shadow | 6 | 6 | 732 | 1083 |
| u_pp | u_talker | 7 | 10 | 716 | 480 |
| u_pp | u_timer | 8 | 14 | 716 | 179 |
| u_pp | u_dispatch | 9 | 9 | 707 | 579 |
| u_pp | u_rx_validator | 10 | 8 | 508 | 695 |
| u_pp | u_adp | 11 | 11 | 446 | 455 |
| u_pp | @own | 12 | 3 | 382 | 3164 |
| u_pp | u_tx_slots | 13 | 17 | 354 | 138 |
| u_pp | u_nvm_port | 14 | 18 | 259 | 121 |
| u_pp | u_event_router | 15 | 24 | 219 | 51 |
| u_pp | u_maap | 16 | 23 | 192 | 54 |
| u_pp | u_tx_arbiter | 17 | 13 | 181 | 187 |
| u_pp | u_prng | 18 | 16 | 135 | 150 |
| u_pp | u_ca_builder | 19 | 15 | 120 | 152 |
| u_pp | g_rx_pool[5].u_rx_slots | 20 | 22 | 79 | 62 |
| u_pp | u_mrp_strip | 21 | 19 | 70 | 107 |
| u_pp | u_scoreboard | 22 | 20 | 63 | 73 |
| u_pp | u_side_port | 23 | 29 | 52 | 6 |
| u_pp | g_rx_pool[2].u_rx_slots | 24 | 21 | 48 | 62 |
| u_pp | g_rx_pool[0].u_rx_slots | 25 | 25 | 45 | 38 |
| u_pp | u_trace | 26 | 28 | 40 | 18 |
| u_pp | g_rx_pool[4].u_rx_slots | 27 | 27 | 32 | 22 |
| u_pp | g_rx_pool[1].u_rx_slots | 28 | 26 | 31 | 22 |
| u_pp | u_normalizer | 29 | 12 | 17 | 258 |
| u_pp | u_nvm_arb | 30 | 31 | 12 | 3 |
| u_pp | u_desc_mem_guard | 31 | 32 | 1 | 1 |
| u_pp | u_lsn_admit | 32 | 33 | 1 | 1 |
| u_pp | u_release_merge | 33 | 30 | 0 | 4 |
| u_pp | @reconciliation |  |  | -54 | 0 |
| u_pp | @total |  |  | 21980 | 22672 |

### default-synth-8x8

| Scope | Instance | LUT rank | FF rank | LUT | FF |
|---|---|---:|---:|---:|---:|
| wrapper | u_pp | 1 | 1 | 37100 | 30015 |
| wrapper | u_nvm | 2 | 2 | 635 | 1024 |
| wrapper | ctl_fifo | 3 | 4 | 74 | 33 |
| wrapper | @own | 4 | 3 | 9 | 319 |
| wrapper | @reconciliation |  |  | -9 | 0 |
| wrapper | @total |  |  | 37809 | 31391 |
| u_pp | u_aecp | 1 | 3 | 15199 | 4169 |
| u_pp | u_srp | 2 | 1 | 8155 | 10393 |
| u_pp | u_notify | 3 | 4 | 3316 | 3799 |
| u_pp | u_listener | 4 | 5 | 1652 | 1136 |
| u_pp | u_timer | 5 | 13 | 1460 | 217 |
| u_pp | u_rx_validator | 6 | 8 | 858 | 695 |
| u_pp | u_talker | 7 | 10 | 848 | 473 |
| u_pp | u_originator | 8 | 7 | 771 | 881 |
| u_pp | u_nvm_shadow | 9 | 6 | 715 | 978 |
| u_pp | u_dispatch | 10 | 9 | 680 | 579 |
| u_pp | u_adp | 11 | 11 | 655 | 441 |
| u_pp | @own | 12 | 2 | 504 | 4643 |
| u_pp | u_nvm_port | 13 | 19 | 357 | 124 |
| u_pp | u_event_router | 14 | 18 | 356 | 129 |
| u_pp | u_tx_slots | 15 | 17 | 355 | 138 |
| u_pp | u_maap | 16 | 24 | 249 | 54 |
| u_pp | u_tx_arbiter | 17 | 14 | 191 | 187 |
| u_pp | u_prng | 18 | 16 | 143 | 150 |
| u_pp | u_ca_builder | 19 | 15 | 123 | 152 |
| u_pp | u_scoreboard | 20 | 21 | 90 | 73 |
| u_pp | g_rx_pool[5].u_rx_slots | 21 | 23 | 85 | 62 |
| u_pp | u_mrp_strip | 22 | 20 | 73 | 107 |
| u_pp | g_rx_pool[2].u_rx_slots | 23 | 22 | 57 | 62 |
| u_pp | u_side_port | 24 | 29 | 54 | 6 |
| u_pp | g_rx_pool[0].u_rx_slots | 25 | 25 | 40 | 38 |
| u_pp | g_rx_pool[4].u_rx_slots | 26 | 27 | 32 | 22 |
| u_pp | g_rx_pool[1].u_rx_slots | 27 | 26 | 31 | 22 |
| u_pp | u_trace | 28 | 28 | 28 | 18 |
| u_pp | u_normalizer | 29 | 12 | 17 | 258 |
| u_pp | u_nvm_arb | 30 | 31 | 4 | 3 |
| u_pp | u_desc_mem_guard | 31 | 32 | 2 | 1 |
| u_pp | u_lsn_admit | 32 | 33 | 2 | 1 |
| u_pp | u_release_merge | 33 | 30 | 0 | 4 |
| u_pp | @reconciliation |  |  | -2 | 0 |
| u_pp | @total |  |  | 37100 | 30015 |

### attribution-synth-1x1

| Scope | Instance | LUT rank | FF rank | LUT | FF |
|---|---|---:|---:|---:|---:|
| wrapper | u_pp | 1 | 1 | 21716 | 23706 |
| wrapper | u_nvm | 2 | 2 | 517 | 469 |
| wrapper | ctl_fifo | 3 | 4 | 79 | 33 |
| wrapper | @own | 4 | 3 | 11 | 327 |
| wrapper | @reconciliation |  |  | -9 | 0 |
| wrapper | @total |  |  | 22314 | 24535 |
| u_pp | u_aecp | 1 | 4 | 4678 | 3010 |
| u_pp | u_srp | 2 | 1 | 4271 | 6376 |
| u_pp | u_notify | 3 | 2 | 3193 | 3299 |
| u_pp | u_listener | 4 | 5 | 1535 | 1103 |
| u_pp | u_dispatch | 5 | 9 | 857 | 759 |
| u_pp | u_talker | 6 | 10 | 833 | 514 |
| u_pp | u_maap | 7 | 11 | 764 | 499 |
| u_pp | u_originator | 8 | 7 | 756 | 885 |
| u_pp | u_nvm_shadow | 9 | 6 | 754 | 1083 |
| u_pp | u_timer | 10 | 15 | 723 | 179 |
| u_pp | u_adp | 11 | 12 | 593 | 463 |
| u_pp | u_rx_validator | 12 | 8 | 540 | 773 |
| u_pp | @own | 13 | 3 | 365 | 3241 |
| u_pp | u_tx_slots | 14 | 18 | 349 | 138 |
| u_pp | u_nvm_port | 15 | 19 | 266 | 121 |
| u_pp | u_event_router | 16 | 24 | 230 | 51 |
| u_pp | u_tx_arbiter | 17 | 14 | 184 | 187 |
| u_pp | u_ca_builder | 18 | 16 | 157 | 152 |
| u_pp | u_prng | 19 | 17 | 157 | 150 |
| u_pp | g_rx_pool[5].u_rx_slots | 20 | 23 | 85 | 62 |
| u_pp | u_mrp_strip | 21 | 20 | 73 | 107 |
| u_pp | u_scoreboard | 22 | 21 | 66 | 73 |
| u_pp | g_rx_pool[2].u_rx_slots | 23 | 22 | 53 | 62 |
| u_pp | u_side_port | 24 | 29 | 53 | 6 |
| u_pp | g_rx_pool[0].u_rx_slots | 25 | 25 | 48 | 38 |
| u_pp | u_trace | 26 | 28 | 40 | 18 |
| u_pp | g_rx_pool[4].u_rx_slots | 27 | 27 | 33 | 22 |
| u_pp | g_rx_pool[1].u_rx_slots | 28 | 26 | 32 | 22 |
| u_pp | u_normalizer | 29 | 13 | 17 | 304 |
| u_pp | u_nvm_arb | 30 | 31 | 12 | 3 |
| u_pp | u_desc_mem_guard | 31 | 32 | 1 | 1 |
| u_pp | u_lsn_admit | 32 | 33 | 1 | 1 |
| u_pp | u_release_merge | 33 | 30 | 0 | 4 |
| u_pp | @reconciliation |  |  | -3 | 0 |
| u_pp | @total |  |  | 21716 | 23706 |

### attribution-route-1x1

| Scope | Instance | LUT rank | FF rank | LUT | FF |
|---|---|---:|---:|---:|---:|
| wrapper | u_pp | 1 | 1 | 20110 | 22737 |
| wrapper | u_nvm | 2 | 2 | 474 | 469 |
| wrapper | ctl_fifo | 3 | 4 | 75 | 33 |
| wrapper | @own | 4 | 3 | 9 | 319 |
| wrapper | @reconciliation |  |  | -13 | 0 |
| wrapper | @total |  |  | 20655 | 23558 |
| u_pp | u_aecp | 1 | 4 | 4504 | 3010 |
| u_pp | u_srp | 2 | 1 | 3998 | 6246 |
| u_pp | u_notify | 3 | 2 | 3111 | 3299 |
| u_pp | u_listener | 4 | 5 | 1404 | 1103 |
| u_pp | u_talker | 5 | 10 | 789 | 492 |
| u_pp | u_originator | 6 | 7 | 739 | 885 |
| u_pp | u_nvm_shadow | 7 | 6 | 734 | 1083 |
| u_pp | u_dispatch | 8 | 9 | 729 | 579 |
| u_pp | u_timer | 9 | 14 | 723 | 179 |
| u_pp | u_adp | 10 | 11 | 542 | 455 |
| u_pp | u_rx_validator | 11 | 8 | 513 | 695 |
| u_pp | @own | 12 | 3 | 356 | 3173 |
| u_pp | u_tx_slots | 13 | 17 | 348 | 138 |
| u_pp | u_nvm_port | 14 | 18 | 259 | 121 |
| u_pp | u_maap | 15 | 23 | 227 | 62 |
| u_pp | u_event_router | 16 | 24 | 218 | 51 |
| u_pp | u_tx_arbiter | 17 | 13 | 182 | 187 |
| u_pp | u_ca_builder | 18 | 15 | 152 | 152 |
| u_pp | u_prng | 19 | 16 | 136 | 150 |
| u_pp | g_rx_pool[5].u_rx_slots | 20 | 22 | 81 | 62 |
| u_pp | u_mrp_strip | 21 | 19 | 70 | 107 |
| u_pp | u_scoreboard | 22 | 20 | 64 | 73 |
| u_pp | u_side_port | 23 | 29 | 52 | 6 |
| u_pp | g_rx_pool[2].u_rx_slots | 24 | 21 | 48 | 62 |
| u_pp | g_rx_pool[0].u_rx_slots | 25 | 25 | 45 | 38 |
| u_pp | u_trace | 26 | 28 | 40 | 18 |
| u_pp | g_rx_pool[4].u_rx_slots | 27 | 27 | 33 | 22 |
| u_pp | g_rx_pool[1].u_rx_slots | 28 | 26 | 31 | 22 |
| u_pp | u_normalizer | 29 | 12 | 17 | 258 |
| u_pp | u_nvm_arb | 30 | 31 | 12 | 3 |
| u_pp | u_desc_mem_guard | 31 | 32 | 1 | 1 |
| u_pp | u_lsn_admit | 32 | 33 | 1 | 1 |
| u_pp | u_release_merge | 33 | 30 | 0 | 4 |
| u_pp | @reconciliation |  |  | -49 | 0 |
| u_pp | @total |  |  | 20110 | 22737 |

### attribution-synth-8x8

| Scope | Instance | LUT rank | FF rank | LUT | FF |
|---|---|---:|---:|---:|---:|
| wrapper | u_pp | 1 | 1 | 28277 | 31607 |
| wrapper | u_nvm | 2 | 2 | 1131 | 1024 |
| wrapper | ctl_fifo | 3 | 4 | 79 | 33 |
| wrapper | @own | 4 | 3 | 11 | 327 |
| wrapper | @reconciliation |  |  | -9 | 0 |
| wrapper | @total |  |  | 29489 | 32991 |
| u_pp | u_srp | 1 | 1 | 8382 | 11130 |
| u_pp | u_aecp | 2 | 3 | 5025 | 4154 |
| u_pp | u_notify | 3 | 4 | 2895 | 3799 |
| u_pp | u_listener | 4 | 5 | 1655 | 1124 |
| u_pp | u_timer | 5 | 14 | 1451 | 217 |
| u_pp | u_talker | 6 | 10 | 1350 | 522 |
| u_pp | u_rx_validator | 7 | 8 | 883 | 773 |
| u_pp | u_dispatch | 8 | 9 | 849 | 759 |
| u_pp | u_maap | 9 | 11 | 839 | 506 |
| u_pp | u_adp | 10 | 12 | 812 | 449 |
| u_pp | u_originator | 11 | 7 | 792 | 881 |
| u_pp | u_nvm_shadow | 12 | 6 | 714 | 978 |
| u_pp | @own | 13 | 2 | 457 | 4712 |
| u_pp | u_nvm_port | 14 | 20 | 434 | 124 |
| u_pp | u_tx_slots | 15 | 18 | 362 | 138 |
| u_pp | u_event_router | 16 | 19 | 358 | 129 |
| u_pp | u_tx_arbiter | 17 | 15 | 191 | 187 |
| u_pp | u_prng | 18 | 17 | 158 | 150 |
| u_pp | u_ca_builder | 19 | 16 | 154 | 152 |
| u_pp | u_scoreboard | 20 | 22 | 90 | 73 |
| u_pp | g_rx_pool[5].u_rx_slots | 21 | 24 | 81 | 62 |
| u_pp | u_mrp_strip | 22 | 21 | 77 | 107 |
| u_pp | g_rx_pool[2].u_rx_slots | 23 | 23 | 57 | 62 |
| u_pp | u_side_port | 24 | 29 | 55 | 6 |
| u_pp | g_rx_pool[0].u_rx_slots | 25 | 25 | 39 | 38 |
| u_pp | g_rx_pool[4].u_rx_slots | 26 | 27 | 32 | 22 |
| u_pp | g_rx_pool[1].u_rx_slots | 27 | 26 | 29 | 22 |
| u_pp | u_trace | 28 | 28 | 28 | 18 |
| u_pp | u_normalizer | 29 | 13 | 18 | 304 |
| u_pp | u_nvm_arb | 30 | 31 | 11 | 3 |
| u_pp | u_desc_mem_guard | 31 | 32 | 1 | 1 |
| u_pp | u_lsn_admit | 32 | 33 | 1 | 1 |
| u_pp | u_release_merge | 33 | 30 | 0 | 4 |
| u_pp | @reconciliation |  |  | -3 | 0 |
| u_pp | @total |  |  | 28277 | 31607 |

