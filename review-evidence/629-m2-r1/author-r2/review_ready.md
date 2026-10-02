[A494] REVIEW READY
Commit: `d81198c2001756fd84c353d93c312c133c5af66b` on `629-media-clock-impl` (PR #634): eight commits on round 1's `57f4b742`, none amended; local, not pushed. Pushing, applying the prepared PR body (it keeps the `[A491]` first line and adds a Round 2 section) and the re-reviews are the manager's.
Changed, in the [assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5946975634)'s order:
1. **Capture re-measure** (R432-1 F1 = R433-1 F2; `d048e48b7`, `a2f173428`, `d81198c20`). Re-measured per `tb/verilator/nvm_capture_cpu/README.md`: both shapes at 50 MHz with aligned edges, traffic ON and OFF, 16 captures each, plus the labelled 100 MHz 8x8 point. **8x8 maximum 13.86484 ms against the 24.5 ms limit** (margin 10.63516 ms; was 13.23352 ms), so no STOP. 1x1 3.96728 ms; 100 MHz 8x8 10.42973 ms. The census grows from 156 to 164 records (12,634 to 13,210 bytes) at 8x8 and from 53 to 54 (3,218 to 3,290) at 1x1. The harness now takes each row's expected census from the generated shape (`nvm_shape.closed_record_census`, shared with the gate) instead of a literal. A first run exposed a harness defect: the simulator's TX-frame trace shares stdout with the firmware console, and it split a CAPTURE row in the 8x8 OFF arm. The trace now waits for a console line start, and all six arms were re-run. Every capture the first run graded reproduces its cycle count exactly. Refreshed: `measurements.json` (identities, rows, maxima), section 18 (and 17, 20) of the saved-state ownership page, and the harness README. The FASTCONNECT 4.2 sizes the census drives (3,336 / 13,256-byte images) are refreshed too, each equal to `check_nvm_record_space.py`'s output.
2. **Root suite under hosted make** (R432-1 F2; `62822ca69`): `--no-print-directory` on both nested derivations. Reproduced first under a real GNU make 4.3: `Cannot find file containing module: 'Entering'`, schemata not compiled, rc 2. Then 27/27 rc 0 under the same make.
3. **Ratchets** (`13721318e`): `//!` contracts on the meter's `clk_i`, `rst_n` and `subtype_i`. `CLK_FREQ_HZ_P` is documented in Hz and `fsh_i` by its octets. The largest deviation is split out of `status_o` as `max_dev_ns_o`; `AAFM_STAT` is unchanged and OOC area is unchanged (574 LUT, 636 FF). The design page's trailing blank line is removed. No budget raised.
4. **Tests that can fail** (`21dbf51c0`). The root plants "`tu` taken from the `tv` net" (mutant 15). Leg A's followed talker sets and clears `tu`; each edge restarts the meter's history with no request. Meter checks now kill each R432-1 F5 probe: the restart at the step's PDU, a gap breaking the settle run, lock behaviour per era event (listener change, entry, `tu` edge, bind edge), zero channels refused, and the largest deviation. All six probes are named mutants. A listener change keeping the lock also fails at the root (mutant 16, a switch onto a talker silent past the meter's timeout).
5. **Docs** (`f40822b31`): the FR_NFR status row, the REGISTER_MAP 0x8C8 sentence, and the `obj_aclk` row now naming `milan_dp_mclk` mutant 3.
6. **RESIDUE and suggestions** (`2253eca31`). R433-1 R1 to R3 and R432-1 R1, R2 and R4 are taken (R3 is in the PR body). R432-1 S2 is taken. R433-1 S2 is taken for `sim_aclk` (two-sided, +0.80 ppm measured) and retained for render T30 (its window is the pull-in; T31 bounds the settled walk). R432-1 S1 = R433-1 S1 is retained: it changes the merged design's settle table and needs its own decision and re-validation; no defect is observed.
Validation, at `d81198c20` unless noted. All rc 0, unpiped, physical path, pinned 5.050, suites under GNU make 4.3:
- every suite as the five CI shards: 59/59 suites, 2,148,404 checks, 0 failures (shard 0 11/11, 1 23/23, 2 12/12, 3 12/12, 4 1/1); `milan_dp_mclk` passes inside shard 2 under make 4.3, the path that failed on the hosted runner, and under R432-1's `MAKEFLAGS=w MAKELEVEL=1` line;
- `check_nvm_capture.py` (its four named mutations each rc 1);
- the builder test (ALL GATES PASS EXCEPT gate 11, which needs an Arty build tree on disk, as in round 1);
- `check_port_contracts.py` (hdl 217 <= 217) and `measure_naming.py --check` (95 recorded);
- `check_entity_shape.py` (166/0);
- the docs gates (`docs_check`, `check_doc_style`, `gen_toc --check`, `--verify-anchors`, `check_em_dash --base cdf49d1a`, `check_doc_paths`), plus a 77-step local replica of the `docs-check` workflow's gate steps;
- `git diff --check`, on the worktree and `cdf49d1a HEAD`;
- the lint ratchet (90 <= 90), `xvlog_gate.py --check` (0 findings in `hdl/`) and `syn/yosys/run.sh` (55/55).
Mutants:
- root campaign 31/31: 16 mutants, 15 and 16 new;
- meter campaign 33/33: 32 mutants, 6 new;
- `reviewer_meter_probes.py` from the R432-1 packet, unmodified: 15/15 CAUGHT.
Shipping image, rebuilt since RTL changed (`TAG=a494m2d81198c2 sw/litex/build.sh ax7101`, Vivado 2026.1, the repository recipe):
- WNS +0.065 ns, WHS +0.036 ns, WPWS +0.264 ns, 0 failing endpoints, no negative slack at the four sign-off corners;
- 0 critical warnings, the #607 refusal clean;
- LUT 80.52 %, slices 99.90 %; meter placed 483 LUT / 630 FF.
Acceptance criteria: items 1 to 6 met as above. The STOP condition (8x8 above 24.5 ms) is not reached.
Open risks/questions:
- Outside #629, for the manager to file if wanted: `milan_dp_render` and `pp_shadow` derive lists with the same unguarded nested `make`, reached only by explicit targets today. `fw_service_budget/oracle.json` keeps the pre-#629 image sizes in a fixture no gate binds.
- The capture timing stays a simulation measurement.
