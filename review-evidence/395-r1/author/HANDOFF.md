# [A387] Issue 395 handoff

Status: implementation and assigned validation complete; ready for independent review. Items 1, 2 and 5 only; items 3 and 4 remain open.

Base: `8bc97021f28fb7f729418d3a00851c84ea0b50fd`.
Branch: `395-timing-grade`.
Head: `66001a307ce5de57577e66d6e3a18b9f4020764b`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Physical worktree: `$LANES/395-timing-grade`.
Owner decision: commercial grade, 0 to 85 C junction.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5859935504
Independent reviewers: [R372] and [R373].

## Declaration and candidate derivation

`sw/litex/platforms/ax7101_timing.py::TIMING_GRADE` owns the part,
grade, junction endpoints and fixed timing models. The AX7101 platform reads
its part from this declaration and installs its generated pre-placement
commands. The bitstream hook checks that part, power conditions and both
setup/hold analyses remain selected, then emits the corner and diagnostic
reports. `sw/litex/report_timing_grade.py` uses the same declaration and Tcl
hook to analyse an existing checkpoint read-only. Builder tests pin the owner
decision, exercise ten wrong-condition refusals and the report-failure restore
path, and inspect the actual platform hooks.

Both AX7101 shapes and every placement-directive candidate enter
`milan_soc.py`'s AX7101 platform branch through the existing build/sweep/deploy
launchers. That branch constructs `alinx_ax7101.Platform`, so the selected
recipe cannot supply another part or omit the grade hook. There is no grade
command-line override. The platform feeds `TIMING_GRADE["part"]` to the
platform constructor and `configure_commands()` to the pre-placement command
list. Its first bitstream command runs `kl_timing_grade_reports`, after route
and physical optimization and before bitstream generation. The existing
launcher files require no duplicate grade literals or edits. The saved-checkpoint
script calls the identical `configure_commands()` and report procedure.

## Shipping candidate provenance

Read-only candidate: `build_ax7101_eto_tdm8dev9e9954e9`, source `9e9954e9`.
Checkpoint: 115715651 bytes, SHA-256
`5f7a442b6a9327ad5d41aa0b10e18c84d9ca4c0aacd573d2ad25d444f5b2f5d1`.
Bitstream: 3825992 bytes, SHA-256
`1696d1ea7568b2cf3cd536b1d34488e1ce7702e4a79e7cf3aca2c6ed6a54d2c7`.
See `shipping-inputs.json` for the full input inventory.
The nominated source commit is `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5`.
Vivado 2026.1 build 6511674 reads part `xc7a100tfgg484-2`, production speed
file 1.23 dated 2018-06-13, with the checkpoint in `Physopt postRoute` state.
The retained implementation Tcl records AreaOptimized_high synthesis,
ExploreArea optimization, ExtraTimingOpt placement, and AggressiveExplore
routing and both physical-optimization passes. No explicit placement seed
appears in that Tcl; this analysis reuses the exact routed bytes rather than
claiming a regenerated placement. The clock report gives 100 MHz system and
50 MHz fabric. The original implementation used 32 threads; the reports here
used 16, and the live controls used one. No implementation run was repeated.
Reports are retained outside this output directory in
`$VALIDATION_STORAGE/395-a387-work/final-66001a307`. No candidate file was written. All six input size/hash pairs were rechecked
after the committed-head timing run and remain identical.

## Timing corners

| Process | Junction temperature | WNS ns | TNS ns | WHS ns | THS ns | Result |
|---|---|---|---|---|---|---|
| Slow | 0 C | 0.123 | 0.000 | 0.101 | 0.000 | constrained paths pass |
| Slow | 85 C | 0.123 | 0.000 | 0.101 | 0.000 | constrained paths pass |
| Fast | 0 C | 1.429 | 0.000 | 0.036 | 0.000 | constrained paths pass |
| Fast | 85 C | 1.429 | 0.000 | 0.036 | 0.000 | constrained paths pass |

Artix-7 has fixed Slow/Fast timing models. Junction temperature in
`set_operating_conditions` is power metadata and does not prorate timing.
Thus each model repeats at the two endpoints; these are not four independent
PVT models. Both setup and hold were selected at each model. Combined WNS
0.123 ns, WHS 0.036 ns, TNS/THS zero. WPWS 0.264 ns. Each timing report counts
175907 setup and hold endpoints, with no failures.

Negative-slack paths: none. All four explicit negative-slack reports say no
paths found. No timing fix was made.

Clock interaction: 16 active pairs, eight Clean, six Ignored, two No Common
Clock. The two unsafe classifications connect `eth_clocks0_rx` and
`milansoc_crg_clkout1` in opposite directions.

CDC: CDC-2 Warning 11; CDC-3 Info 21; CDC-5 Warning 4; CDC-6 Warning 56;
CDC-9 Info 1; CDC-10 Critical 6; CDC-12 Critical 4; CDC-15 Warning 249;
CDC-26 Warning 183. Total: ten Critical, 503 Warning, 22 Info diagnostics.
These are reported, not waived or repaired.

Unconstrained paths: zero unclocked registers and zero unconstrained internal
endpoints, but 46 inputs lack input delays and 87 outputs lack output delays.
CDC skips unconstrained inputs. Positive slack does not discharge these
external constraints or the CDC diagnostics. The public findings document
`docs/findings/COMMERCIAL_TIMING_395.md` records the table and limitations.

All timing-engine invocations returned rc 0: baseline checkpoint probe,
command-help query, initial report run, committed-head report run, and live
negative controls. `timing-runs.json` records each script/log SHA-256 and
size; small copies are in `timing-runs/`. Initial probes are not claimed as
committed-head evidence.

The live controls at `66001a307` rejected nine wrong conditions on the real
checkpoint: wrong part; changed grade; changed junction temperature; and
none/min-only/max-only analysis at each of Slow/Fast. The harness caught each
expected production error and returned rc 0 after restoring the declaration.
It used one thread and wrote no checkpoint.
The committed-head rerun completed with rc 0 in 56.89 seconds and reproduced
all five timing rows. Final raw reports are in
`$VALIDATION_STORAGE/395-a387-work/final-66001a307`; full sizes and SHA-256 hashes are in
`report-artifacts.json`. Files larger than 200000 bytes stay there. Small
reports and timing-summary extracts are copied under `reports/`.
The foreground command used `timeout --foreground 1800`, `-mode batch`,
`-nojournal`, `-notrace`, an explicit log and the generated `report.tcl`.

The tightest reported paths are:

| Model/check | Slack ns | Source | Destination |
|---|---:|---|---|
| Slow setup | 0.123 | `milansoc_sdram_zqcs_timer_count1_reg[7]/C` | `subfragments_bankmachine2_state_reg[0]/CE` |
| Slow hold | 0.101 | `milan_datapath/pp_shadow/u_pp/u_aecp/u_resp/lane_d_r_reg[15]/C` | `storage_36_reg_0/DIBDI[15]` |
| Fast setup | 1.429 | `KL_gptp_gmii_launch/u_seal_cdc/req_tog_reg/C` | `KL_gptp_gmii_launch/u_seal_cdc/req_sync_reg[0]/D` |
| Fast hold | 0.036 | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/rxts_commit_r_reg[42]/C` | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/evq_pd_ctx_r_reg_0_3_42_47/RAMA/I` |

These path details and the CDC paths are diagnostic evidence, not waivers.
The existing WNS >= 0 gate is met; no new release-margin policy was invented.

## Gate table

Every row ran at `66001a307ce5de57577e66d6e3a18b9f4020764b`. `gate-results.json` records exact argv, working directories, timestamps, log sizes and SHA-256 hashes. All commands ran in the foreground, without pipelines.

| Gate | Exit code | Seconds | Log |
|---|---:|---:|---|
| timing-script | 0 | 0.05 | `gates/timing-script.log` |
| timing | 0 | 56.89 | `gates/timing.log` |
| builder-present | 0 | 775.77 | `gates/builder-present.log` |
| builder-absent | 0 | 559.57 | `gates/builder-absent.log` |
| ci-scope-selftest | 0 | 2.06 | `gates/ci-scope-selftest.log` |
| docs | 0 | 4.31 | `gates/docs.log` |
| doc-paths | 0 | 0.07 | `gates/doc-paths.log` |
| toc | 0 | 2.6 | `gates/toc.log` |
| em-dash | 0 | 3.18 | `gates/em-dash.log` |
| feature-status | 0 | 0.67 | `gates/feature-status.log` |
| doc-style | 0 | 0.05 | `gates/doc-style.log` |
| doc-style-selftest | 0 | 0.04 | `gates/doc-style-selftest.log` |
| solution-docs | 0 | 0.11 | `gates/solution-docs.log` |
| python-idiom | 0 | 3.37 | `gates/python-idiom.log` |
| python-idiom-selftest | 0 | 3.33 | `gates/python-idiom-selftest.log` |
| diff-committed | 0 | 0.02 | `gates/diff-committed.log` |
| diff-worktree | 0 | 0.02 | `gates/diff-worktree.log` |
| Live checkpoint refusal controls | 0 | see log | `timing-runs/live-controls/vivado.log` |

The present bank used `python3 -B sw/builder/test_builder.py --require-rv32 --require-elaboration`. The absent bank used the retained `run_builder_absent.py`, which runs the full entry point with required elaboration and hides only the three RV32 candidates from subprocess probing. Host compilers remain available. `run_gates.py` retains the complete command sequence.

## Builder coverage limits

- Compiler present: rc 0 in 775.77 seconds; 1 recorded arm(s) not run. See `builder-present-summary.txt`.
- Compiler absent: rc 0 in 559.57 seconds; 2 recorded arm(s) not run. See `builder-absent-summary.txt`.

Both modes report the missing legacy Arty utilization report for gate 11 calibration. The absent mode additionally records its intentional stand-down of compiler-dependent firmware instruments. Required elaboration ran, and no timing-grade arm was skipped. These limits are not claimed as covered.

## Acceptance and remaining work

- Item 1: declaration shared by every AX7101 candidate and the checkpoint reporter; builder pin and offline/live refusal controls pass.
- Item 2: nominated shipping checkpoint analysed read-only at both supported timing models and both recorded junction endpoints; slack and diagnostic reports retained. No negative-slack path was found. CDC and missing-I/O-constraint diagnostics remain unwaived.
- Item 5: BUILDING section 5, RUNNING_TESTS section 5 and the canonical `docs/litex/LITEX_SOC.md` section 7 declare the grade and rule; documentation gates return 0.
- Items 3 and 4 remain open: die-temperature logging and externally referenced oscillator measurements. Independent reviews remain assigned to [R372] and [R373]. This handoff is author evidence, not a review verdict.

The worktree is clean. No push, pull-request action, merge, firmware/RTL change, timing fix or hardware access occurred. The one-line commit has no body or trailers. The final public message will be REVIEW READY on issue #395.
