[A303] REVIEW READY

Commit: `fc8a719fecfaade8f5cdd7e7aef5292ffebcc1b4` (local branch `545-crf-servo-slew`, base `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`).

Items 1-6 are implemented. The processor is pinned at `5dce647a`; the repository recipe regenerated the ROM ledger. The registered policy level passes through `KL_gptp_shadow`, includes the effective PHC rate pipeline tail, and reaches the actual CRF servo. Sticky window overlap suppresses PI/trim/lock updates and counts every affected window in `MCSRV_STAT[15:10]`, including the partial tail. A replacing step counts its same open window only once. Clean windows resume without ACQUIRE.

Clock statement: engine, shadow and servo use `axis_clk`; the existing product PHC contract requires `gtx_clk == axis_clk`. There is no new asynchronous crossing. Release covers the shadow latch, two rate synchronizer stages and PHC application edge, then is staged beside the servo PHC sample. No network-port count or redundancy selector is assumed.

Validation (all listed command exits are 0):

- `make -C tb/verilator/mmcm_servo`: 94 unit, 8 rail, 113 step and 87 slew checks; default mutation campaign 5/5. The separate `mutants` target also passes. Removing discard, tying the level low, trusting the partial tail and removing the tally increment each fail the intended assertion.
- The +100 us / 200 ppm case holds its +30.625 ppm integrator and command exactly through two affected windows. The first clean integrator update is 20/512 ppm, within the stated 1 ppm bound, before 1.536 s from start. Both signs remain LOCKED on every observed edge. Short, shared-boundary, already-closed, prolonged-level, reset, saturation and replacing-step cases pass.
- `make -C tb/verilator/crf_rx`: 13,836 unit, 1,658 discontinuity and 69 connected checks; mutation campaign 8/8.
- `make -C tb/verilator/gptp_shadow -j8`: 309 checks, nine mutation controls and lifecycle gate pass.
- `milan_dp` default `run` recipe: every one of its 33 commands executed in foreground chunks 0-6, 7-13, 14-19, 20-25 and 26-32, with recorded exit 0. The connected gmstep leg passes 56 checks; `gmstep_mutants.py --slew` passes its positive control and catches both the tied-low port and missing release-tail defects. Default render and GM-step campaigns pass 6/6 and 4/4.
- Changed auxiliary fixtures: autorepair 47/47 and egress timestamp `run` 85/85.
- `python3 sw/builder/test_builder.py`: exit 0. **NOT RUN:** gate 11 real board-report calibration, because its input report is absent. The RV32 compilation/census arms ran.
- `scripts/docs_check.py` in both CI modes; `check_em_dash.py --base 5b73d3f47dfed519eb988c13d6beb1db664ef1e0`; `check_doc_style.py`; `gen_toc.py --check` and `--verify-anchors`; `check_doc_paths.py`; `docs/traceability/gen_module_matrix.py --check`: all exit 0. The no-Git mode explicitly skips only Git inventory parity.
- `xvlog_gate.py --check`, `check_rtl_source_lists.py`, `check_sv_idiom.py`, `lint_rtl.py --check`, `check_cpp_idiom.py`, `check_py_idiom.py`, `check_port_contracts.py`, `measure_naming.py --check`, `measure_test_evidence.py --check`: all exit 0; existing ratchets unchanged. The final HDL checks used the committed files.
- `cd tests && behave --no-capture -f plain`: 344 scenarios / 1,739 steps pass. `git diff --check`: exit 0; parent and processor worktrees clean.

Documentation updates cover TIME_SYNC, both required GM_LOSS_RECOVERY rows and the existing register tally. No independent review, hosted CI or hardware result is claimed.

Area (all measurement commands exit 0): repository `cd syn/yosys && ./ooc.sh KL_mmcm_drp_servo` recipe measures 864 -> 871 LUT and 790 -> 792 FF (+7/+2), with DSP/CARRY/memory unchanged. The exact new release-alignment block measures 1 LUT / 4 FF using the same recipe. Sum of isolated parent additions: +8 LUT / +6 FF; this is not a measured whole-datapath delta. The adopted processor's separate published PR #76 measurement is +80 LUT / +6 FF and is not mixed with this flow.

The duration clarification remains as published in the takeover: the explicitly adopted engine contract has measured completion and no 0.5 s expiry. The consumer honors a prolonged level; 100 us / 200 ppm is the prescribed stimulus, not a producer completion guarantee. Frequency citations use the assignment's correction.

The assigned output packet contains HANDOFF.md (file:line changes, clock statement, test/mutation/gate tables, area and limitations), PR-BODY.md, exact sweep commands and raw receipts. No push, PR action, merge, other checkout, donor edit, delegation or hardware action. Independent review remains with the assigned reviewers. No review verdict is claimed here.
