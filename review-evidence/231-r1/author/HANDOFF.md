# Issue 231 author handoff

Status: Committed; local author work ready for independent review.
Role: [A328], author. Internal reviewer: [R332]. External reviewer: [R333].
Branch: `231-pp-shadow-baseline`.
Base and measured RTL: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.
Head: `af6d19c553ad8c445a80528344baf2273b41ad46`.
Repository: `https://github.com/kebag-logic/milan-fpga.git`.
Lane: `$LANES/231-pp-shadow-baseline`.
Work and retained checkpoints: `$VALIDATION_STORAGE/231-a328-work`.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/231#issuecomment-5844867171
Takeover: https://github.com/kebag-logic/milan-fpga/issues/231#issuecomment-5844892720
Epic baseline link: https://github.com/kebag-logic/milan-fpga/issues/229#issuecomment-5845524962
Review-ready publication target: https://github.com/kebag-logic/milan-fpga/issues/231

## Change list

Paths and line numbers are relative to the lane root.

| File:line | Change |
|---|---|
| `docs/design/AREA_BUDGET.md:9` | Links the new measured baseline and reproduction recipe. |
| `docs/findings/PP_SHADOW_BASELINE.md:56` | Standalone and integrated resource/timing results, hierarchy attribution, placement sweep, mapping differences and historical provenance. |
| `docs/findings/PP_SHADOW_BASELINE_INPUTS.json:2` | Complete wrapper parameters, SDK archive identity and all six image inputs per configuration, with hashes and path roots. |
| `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:16` | Clean-checkout commands, shipping exports, out-of-tree artifacts, three placement directives, equivalent mapping geometry and checkpoint report commands. |
| `syn/ooc/pp_baseline.py:18` | Prepares scripts from the exported shipping build; verifies images, derives exact wrapper parameters and emits resource and scoped timing reports. |
| `syn/ooc/pp_baseline.py:231` | Valid-input control plus nine refusals for missing, malformed, partial or ambiguous inputs. |

No RTL, submodule gitlink, donor source or shipping configuration was changed.

## Measurement evidence

All completed measurement commands returned rc 0. Synthesis WNS is estimated;
the routed rows are final post-route optimization reports under the existing
shipping constraints. Product 1x1 includes two processor stream contexts;
product 8x8 includes nine. CRF accounts for the extra context in each direction.
The integrated clocks are 50 MHz and 100 MHz respectively.

| Measurement | LUT | FF | RAMB36 | RAMB18 | DSP | CARRY4 | WNS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| Standalone product 1x1, 100 MHz | 22,350 | 24,533 | 21 | 3 | 5 | 1,415 | -6.180 |
| Standalone product 8x8, 100 MHz | 28,992 | 32,984 | 26 | 5 | 5 | 1,775 | -10.987 |
| Integrated 1x1 synthesis | 51,125 | 58,006 | 79 | 27 | 11 | 3,214 | -1.201 |
| Integrated 1x1 shipping route | 48,618 | 57,854 | 79 | 27 | 11 | 3,203 | +0.013 |
| Integrated 8x8 synthesis | 68,136 | 70,835 | 80 | 29 | 11 | 3,916 | -11.331 |
| Integrated 1x1 comparison: AltSpreadLogic_high | 48,972 | 57,854 | 79 | 27 | 11 | 3,203 | +0.123 |
| Integrated 1x1 comparison: ExtraTimingOpt | 48,893 | 57,854 | 79 | 27 | 11 | 3,203 | +0.106 |

The shipping routed wrapper alone uses 22,441 LUT, 23,493 FF, 21 RAMB36,
3 RAMB18, 5 DSP and 1,361 CARRY4, with internal WNS +0.013 ns.
The integrated 8x8 wrapper uses 37,809 LUT, 31,391 FF, 26 RAMB36, 5 RAMB18,
5 DSP and 1,803 CARRY4, with internal WNS -10.594 ns.
8x8 is synthesis only by the public assignment: 68,136 LUT exceeds the
device's 63,400 LUT capacity before placement.

| Equivalent mapping | Logic LUT | LUTRAM equivalents | Total LUT | FF | RAMB36 | RAMB18 | DSP | CARRY4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Yosys 1x1 | 41,258 | 5,972 | 47,230 | 23,041 | 15 | 4 | 5 | 1,813 |
| Yosys 8x8 | 65,724 | 6,136 | 71,860 | 32,615 | 16 | 4 | 7 | 2,108 |

The baseline explains notification row replication and listener/timer memory
mapping, accounts for the complete 5.5/10.5 BRAM tile differences, and identifies
the extra 8x8 record-address DSPs. Remaining aggregate LUT mapping effects are
not claimed to be individually isolated.

## Artifact index

`reports/` contains only reports, primitive censuses, input records and compressed
logs. `report-manifest.json` binds them to their source files and hashes.
`measurements.json` contains the parsed complete hierarchy and timing records.
`source-hashes.json` records the 120 exported source inputs per configuration.
`versions.json` records the installed version identities.
`gates.json` is the latest combined gate result table; `gates-fast.json` preserves
the initial batch, including a subsequently corrected documentation wording failure.
`gates-final.json` supersedes affected initial results.
`builder-modes.py` preserves the full-suite compiler selector used for the gates.
New build trees, source exports, installed dependencies, mapped netlists, ROM
bytes and checkpoints remain under `$VALIDATION_STORAGE/231-a328-*`, outside this
output directory. The provided SDK remains read-only at its provided prefix.

| Evidence | Report path under this directory |
|---|---|
| Standalone 1x1 / 8x8 | `reports/ax7101-ooc/` / `reports/ax8x8-ooc/` |
| Integrated synthesis 1x1 / 8x8 | `reports/ax7101-synth-reports/` / `reports/ax8x8-synth-reports/` |
| Shipping route | `reports/ax7101-route-reports/` |
| Original integrated logs and IOB/route checks | `reports/ax7101-integrated/` / `reports/ax8x8-integrated/` |
| Other placement directives | `reports/ax7101-AltSpreadLogic_high/` / `reports/ax7101-ExtraTimingOpt/` |
| Equivalent geometry mapping logs | `reports/ax7101-yosys/` / `reports/ax8x8-yosys/` |

The original reports and their checkpoint-reopened equivalents agree after
excluding timestamps and command headers. The recipe's embedded shell syntax and
three embedded Python programs parse. Generated integrated commands match the
shipping export exactly through each requested endpoint; all 20 OOC parameters
and all 120 source reads match the integrated export for each shape.

## Gate table

All commands ran in the foreground without pipes. The table names the complete
gate entrypoints. Markdown checks used the repository's hash-pinned dependencies
installed at `$VALIDATION_STORAGE/231-a328-python`; temporary files used the work root.
The parser gate used the installed front end and did not take its missing-tool skip.

| Gate entrypoint | rc | Log |
|---|---:|---|
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | `gates/nvm-firmware.log` |
| `python3 scripts/check_nvm_capture.py` | 0 | `gates/nvm-capture.log` |
| `python3 scripts/check_baremetal_only.py --check` | 0 | `gates/baremetal-only.log` |
| `python3 scripts/ci_events.py --check` | 0 | `gates/ci-events-check.log` |
| `python3 scripts/ci_events.py --selftest` | 0 | `gates/ci-events-selftest.log` |
| `python3 scripts/xvlog_gate.py --check` | 0 | `gates/xvlog.log` |
| `python3 scripts/check_rtl_source_lists.py` | 0 | `gates/rtl-sources.log` |
| `python3 scripts/check_sv_idiom.py` | 0 | `gates/sv-idiom.log` |
| `python3 scripts/lint_rtl.py --check` | 0 | `gates/rtl-lint.log` |
| `python3 scripts/check_cpp_idiom.py` | 0 | `gates/cpp-idiom.log` |
| `python3 scripts/check_py_idiom.py` | 0 | `gates/py-idiom.log` |
| `python3 scripts/check_port_contracts.py` | 0 | `gates/port-contracts.log` |
| `python3 scripts/measure_naming.py --check` | 0 | `gates/naming.log` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `gates/test-evidence.log` |
| `cd tests && behave --no-capture -f plain` | 0 | `gates/behave.log` |
| `python3 syn/ooc/pp_baseline.py --selftest` | 0 | `gates/baseline-selftest.log` |
| `python3 -B scripts/docs_check.py` | 0 | `gates/docs-git.log` |
| `python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 | `gates/em-dash.log` |
| `python3 scripts/check_doc_style.py` | 0 | `gates/doc-style.log` |
| `python3 scripts/gen_toc.py --check` | 0 | `gates/toc.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | `gates/anchors.log` |
| `python3 scripts/check_doc_paths.py` | 0 | `gates/doc-paths.log` |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `gates/module-matrix.log` |
| `git diff --check` | 0 | `gates/diff.log` |
| `python3 -B scripts/docs_check.py (export without git metadata)` | 0 | `gates/docs-no-git.log` |
| `python3 $VALIDATION_STORAGE/231-a328-work/full_builder.py sdk` | 0 | `gates/builder-sdk.log` |
| `python3 $VALIDATION_STORAGE/231-a328-work/full_builder.py absent` | 0 | `gates/builder-absent.log` |
| `git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | 0 | `gates/diff-candidate.log` |

The SDK gate executes the full `sw/builder/test_builder.py` entrypoint with
`--require-rv32`, mapping only the compiler executable to the provided verified
SDK. All arguments remain unchanged. Its audit records 855 target invocations:
807 successful and 48 intentionally rejected negative mutation compilations.
The no-compiler mode hides all three target-compiler candidates and executes the
same full entrypoint. Detailed argv records are in `gates/builder-*-compiler.jsonl`.

Both full builder modes explicitly report the historical mf48 calibration arm
NOT RUN because its old place report is unavailable. The no-compiler mode also
reports the target compile/census arm NOT RUN, as intended. These omissions are
not presented as executed coverage. The SDK run covers the target compile arm.
The no-git documentation mode uses a tracked-file export with empty submodule
directories, matching the CI checkout after metadata removal. Inventory parity
is explicitly inapplicable in that mode.

## Acceptance and limits

| Acceptance criterion | Evidence |
|---|---|
| Reproduce both OOC product configurations | Committed recipe derives the shipping commands, verifies complete images and binds all parameters from integrated elaboration. Both actual OOC runs return rc 0. |
| Identify dominant resource consumers | Four detailed hierarchy tables, complete hierarchy reports, exact carry censuses and scoped internal WNS. |
| Distinguish standalone, integrated and mapping flows | Separate tables with measured clocks, stages, directives and limitations. |
| Replace retired substitution comparison as decided | Shipping 1x1 route and integrated 8x8 synthesis; historical delta quoted only with its historical provenance. |
| Bind ROM inputs and avoid missing-image results | Complete geometry and hashes for every input; zero Synth 8-4445 diagnostics in all four synthesis logs; source/image hashes rechecked. |
| Link baseline from #229 | Public epic reference above; committed page publication remains the maintainer's step under the no-push instruction. |

The shipping route has zero routing errors, zero failing setup/hold/pulse-width
endpoints and a passing active-port IOB check. Its final setup/hold margins are
only +0.013/+0.014 ns. Existing unmatched-clock/conditional-XDC warnings remain;
the report lists 46 inputs and 87 outputs without I/O delays. This is a measured
baseline, not complete board-interface signoff. No hardware was touched.

The installed Yosys package reports revision `86f2ddebc-dirty`; its figures are
labelled version-specific measurements, not a pinned portability verdict.
The corrected historical datapath head is 38,879 LUT at `b3507ddd`, not the
superseded 38,611 figure. The old area record was read from its relocated history
path, and the removed campaign from `654cdd70^`.

## Handoff state

The implementation remains local as requested. No push, PR creation or edit,
merge, hardware action, other checkout, or donor edit was performed.
Independent reviews, publication, hosted checks and merge remain outside this
author handoff. No author approval is claimed.
The three temporary builder/ROM symlinks were removed; the lane is clean.
The actual generated bytes remain under `builder/` and `roms/` in the work root.
