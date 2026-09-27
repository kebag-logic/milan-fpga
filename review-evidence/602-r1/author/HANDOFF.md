# [A383] Deliverable 2 handoff

Status: REVIEW READY at `49012143b335ea48d6a71c441a05d0c1796887ff`. All 34 final-head command receipts have rc 0. The [scope correction](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859621253) is applied as test-only commit `49012143b`; `81893de43` corrects the remaining restart input-port comment within the original documentation scope. Both descend from `f7660247e`. The full builder bank passes in both compiler modes, with its explicit not-run bounds documented below. All foreground verification has finished.
Issue: https://github.com/kebag-logic/milan-fpga/issues/602
Assignment: https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859299480
Ruling: https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859297355
Branch: `602-phc-step-mr`
Base: `6d5ebd7357c1e468e446f18a61527c5be6118a04`
Origin and base verified; initial worktree clean.
Executor: [A383]. Internal reviewer: [R366]. External reviewer: [R367].

## Change list

| File:line | Change |
|---|---|
| `hdl/milan/milan_datapath.sv:3124` | Remove the PHC-only restart term; retain the render re-base pulse and independent tu wiring. |
| `hdl/ieee1722/avtp/KL_media_clock_restart.sv:105` and `:168` | Comment-only correction of the banner and input-port restart contract; executable engine unchanged. |
| `tb/verilator/milan_dp/sim_gmstep.cpp:811` | Grade a real source switch through its on-wire mr transition. |
| `tb/verilator/milan_dp/sim_gmstep.cpp:1035` | Count wire edges across the stimulus boundary; exclude PHC-only mr/MEDIA_RESET and preserve selected-CRF propagation. |
| `tb/verilator/milan_dp/sim_main.cpp:991` | Grade INTERNAL adjtime and settime as non-restart causes. |
| `tb/verilator/milan_dp/gmstep_mutants.py:125` | Plant required defects and require the named harness failure. |
| `tb/verilator/milan_dp/Makefile:116` | Allow disposable restart-engine mutation through the normal source list. |
| `sw/builder/test_builder.py:10717`, `:10777`, `:12481`, `:12503`, `:15100` and `:16653` | Authorized test-only census, initializer, mutation-anchor, diagnostic and comment correction. |
| `tb/verilator/milan_dp/README.md:640` | Document the ruled expectations, controls and proof boundaries. |
| `docs/design/GM_LOSS_RECOVERY.md:142` | Update outgoing mr, MEDIA_RESET, pending-step rows and adopted annex interpretation. |
| `docs/design/TIME_SYNC.md:113` | Separate the render event from the media-clock restart and cite #602. |
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md:206` | Update mr conformance and clock-source rows for the ruling. |

`rtl-scope.json` records an executable-HDL comparison: only the requested restart term changes. The restart engine differs only in comments.

## Simulation assertions and controls

| Assertion/control | Measured result | Evidence |
|---|---|---|
| Isolated selected-CRF PHC step | One 1.5 s step; outgoing AAF mr transitions 0 | gmstep `grade_the_event` and `grade_the_restart`; 64 checks pass |
| Step-caused MEDIA_RESET | Delta 0 before/after the step; valid GET_COUNTERS masks 0x1f | gmstep counter reads before, between commit/step, and after |
| tu rise/hold/clear | Rises at the GM publication; held 224891 cycles after the step, quarter tick 131072; clears within the existing bound | gmstep `grade_uncertainty` |
| Render re-base | One counted recentre at a PDU end 132 cycles after the step; no reset rail; post-push fill 14 events | gmstep `grade_the_render` |
| Continuing stream | 1286 outgoing PDUs; no sequence gap; baseline rate within 1%; longest pause 708 cycles; listener MEDIA_UNLOCKED unchanged | gmstep `grade_the_licence` |
| Real source switch | INTERNAL to selected CRF through SET_CLOCK_SOURCE; exactly one outgoing mr transition; PDUs bracket the command | gmstep `provision_media` |
| Selected CRF mr | Received toggle propagates exactly once while the sink stays locked; no PHC step supplies the event | gmstep `check_crf_restart` |
| INTERNAL software PHC controls | Adjtime and settime must leave mr unchanged; settime adds no MEDIA_RESET | option-off `sim_main.cpp`, included in the full datapath target |
| Existing restart hold/merge | 96 checks pass; four engine mutants caught | `tkdiag.log` |

The gmstep licence checks grade uninterrupted escape-enabled transport and held listener lock, not an lwSRP reservation. TDM clocks remain held and DRP answers zero; no physical clock or hardware continuity claim is made. The restart-engine unit checks drive generic requests; their historical “step” labels do not prove PHC integration.

The disabled-render negative control is retained as the event-count failure. [#387 decision 5802264260](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5802264260) explicitly replaced the impossible fill-drift assertion for this accept-timed stage. #602 preserves that render behavior.

## Mutant table

All sixteen mutants are caught; both clean legs pass (18/18 campaign verdicts, rc 0). The clean gmstep run is 64/64. A catch requires a nonzero harness verdict containing the named assertion; compile errors and crashes do not count.

| Planted defect | Named failing assertion | Verdict |
|---|---|---|
| the policy level is tied low at the servo | `slew path: the actual servo receives the level` | Caught |
| the policy level omits the applied-rate tail | `slew path: every staged sample covers the PHC tail` | Caught |
| the policy level misses an extra addend stage | `slew path: every staged sample covers the PHC tail` | Caught |
| the PHC re-base restart term is restored | `restart: a PHC-only step leaves outgoing mr unchanged` | Caught |
| the source-change term is removed | `source control: a real source change toggles mr once` | Caught |
| selected CRF mr propagation is removed | `CRF control: selected CRF mr propagates exactly once` | Caught |
| the grandmaster identity re-bases the render stage as well as the step | `render: the GM change is one counted re-base event` | Caught |
| the step does not re-centre the render stage | `render: the GM change is one counted re-base event` | Caught |
| the render re-base is keyed to the identity, not the step | `render: every counted re-base lands at a PDU end right after the step` | Caught |
| tu reaches the talkers four cycles late | `tu: set in the first cycle the bank names GM B` | Caught |
| the plane's step does not re-arm the holdover | `tu: held at least the 0.25 s holdover after the step` | Caught |
| tu stops the talker | `licence: the talker never pauses beyond four of its intervals` | Caught |
| the grandmaster change stops the talker for good | `licence: the talker never pauses beyond four of its intervals` | Caught |
| the step's re-centre snaps one event off the setpoint | `render: every PDU push leaves the target fill across the event` | Caught |
| software settime is restored as an mr cause | `CLKV: the settime leaves mr unchanged (#602)` | Caught |
| PHC adjtime is restored as an mr cause | `CLKV: PHC-only steps leave INTERNAL mr unchanged (#602)` | Caught |

## Yosys before/after table

All six OOC runs returned 0 at `49012143b`: base, functional edit and neutral base edit, each at both AX shapes. The repeated before/after counts exactly match the earlier measurements. The neutral edit has zero cell-count delta on both shapes.

Recipe: the repository `syn/yosys/ooc.sh` flow, `synth_xilinx -family xc7 -flatten`, default DSP mapping and the printed jemalloc allocator. `ooc_measure.py` copies only the datapath source and adjusts parameter defaults because this flow documents that `chparam` cannot shape its flattened interfaces. Its runner changes only root/source path resolution; every other source, synthesis command and refusal remains the repository version. Parameters and artifact hashes are in the per-shape JSON receipts. No checkout or repository source was reshaped.

| AX shape | Version | LUT | LUTRAM | LUT total | FF | RAMB36 | RAMB18 | DSP | CARRY4 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1 TDM8 | Before | 97630 | 6764 | 104394 | 46021 | 16 | 20 | 17 | 3725 |
| 1x1 TDM8 | After | 97812 | 6764 | 104576 | 46021 | 16 | 20 | 17 | 3725 |
| 1x1 TDM8 | Functional delta | +182 | 0 | +182 | 0 | 0 | 0 | 0 | 0 |
| 1x1 TDM8 | Neutral control | 97630 | 6764 | 104394 | 46021 | 16 | 20 | 17 | 3725 |
| 1x1 TDM8 | Neutral delta | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 8x8 | Before | 141366 | 6748 | 148114 | 60064 | 17 | 21 | 19 | 4523 |
| 8x8 | After | 142972 | 6748 | 149720 | 60064 | 17 | 21 | 19 | 4523 |
| 8x8 | Functional delta | +1606 | 0 | +1606 | 0 | 0 | 0 | 0 | 0 |
| 8x8 | Neutral control | 141366 | 6748 | 148114 | 60064 | 17 | 21 | 19 | 4523 |
| 8x8 | Neutral delta | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

The 1x1 mapped cell changes are: LUT1 +31, LUT2 +200, LUT3 +150, LUT4 -74, LUT5 -153, LUT6 +28; MUXF7 -106, MUXF8 -47 and INV -58. Total cell count falls by 29 while LUT count rises by 182. The executable-source comparison proves only the requested combinational restart term changed; no RTL state was added. This is an OOC mapping comparison, not a placement, timing or physical-continuity result.

The 8x8 cell deltas are INV -61, LUT1 +13, LUT2 +815, LUT3 -193, LUT4 +238, LUT5 +50, LUT6 +683, MUXF7 +113, MUXF8 +23, cells +1681. Flip-flops, LUTRAM, block RAM, DSP and carry counts remain identical in both shapes. LUT totals increase by 0.17% (1x1) and 1.08% (8x8); these are measured flattened mapping outcomes, not an area-saving claim. The changed Boolean cone is the restart request. These totals describe the mapped result; they do not establish why this functional edit increases LUTs.

The [scope correction](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859621253) requested a null-change control. `ooc_measure.py neutral` starts from the exact base datapath and renames `tkd_crflk_q_r` to `tkd_crf_lock_prev_r` at all four references. It asserts that the inverse rename restores the base bytes exactly. The same shaped defaults, source set, allocator and synthesis recipe apply. `ooc-comparison.json` compares every reported cell count: the neutral and base inventories are identical for both shapes. Thus this control does **not** reproduce the functional LUT delta and does not demonstrate the proposed explanation of mapping variation from a neutral source edit. No alternative control was selected after seeing the zero result. Release area is judged on the placed build, which this lane does not measure.

## Five-configuration identity

Before manifests captured for all five generated configurations. Final regeneration is byte-identical for all 50 artifacts (10 per configuration); `generated-before.json` and `generated-after.json` record every size and SHA-256. No builder generator source changed; only the authorized test assertions changed.

| Configuration | Generated files | Identity |
|---|---:|---|
| `endstation_arty_4x4` | 10 | Byte-identical |
| `endstation_arty_8ch` | 10 | Byte-identical |
| `endstation_arty_current` | 10 | Byte-identical |
| `endstation_ax7101_1x1_tdm8` | 10 | Byte-identical |
| `endstation_ax7101_8x8` | 10 | Byte-identical |

## Gates

The required bank now passes in both compiler modes at `49012143b335ea48d6a71c441a05d0c1796887ff`. The prepared assertion patch was applied verbatim in the test-only commit `49012143b`, under the [public scope correction](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859621253). The earlier `builder.json`/`builder.log` record the resolved failure at `f7660247e`; they are historical evidence, not the final verdict.

| Full builder mode | rc | Gate 1b mutation result | Explicitly not run |
|---|---:|---|---|
| RV32 required, GCC 14.3.0 | 0 | 358/358 rejected; 53/53 RTL variants elaborated | Gate 11: historical placed calibration report absent |
| Cross compilers absent | 0 | 256/256 rejected; 53/53 RTL variants elaborated | Gate 1b: compiler-dependent instruments and their controls; gate 11: same report absent |

`builder_absent.py` runs the complete unchanged `test_builder.py` entry point through `runpy`. It intercepts only the three cross-compiler candidates and makes each absent; host probes and other subprocess calls remain unchanged. `builder-absent-audit.json` records all three hidden calls and the two registered not-run entries. These missing instruments are not counted as coverage. They execute in the separate RV32-required run. Neither mode proves the unavailable historical placed-area calibration.

All 34 final-head gate commands returned 0. The full datapath target finished in 1642.38 s, including its render campaign (6/6) and default gmstep campaign (6/6). The explicit gmstep campaign returned 18/18 verdicts: both clean legs and all 16 caught mutants. Its clean gmstep leg passes 64/64 assertions. The 25 short gates, tkdiag, both builder modes, all six OOC shape runs and artifact identity pass within their stated bounds.

| Gate | Command | rc | Head | Seconds | Receipt |
|---|---|---:|---|---:|---|
| archive | `python3 scripts/check_archive.py` | 0 | 49012143b | 0.29 | [archive.json](archive.json) |
| artifact-identity | `python3 $OUTPUT/check_artifact_identity.py` | 0 | 49012143b | 0.55 | [artifact-identity.json](artifact-identity.json) |
| baremetal-check | `python3 scripts/check_baremetal_only.py --check` | 0 | 49012143b | 15.08 | [baremetal-check.json](baremetal-check.json) |
| baremetal-selftest | `python3 scripts/check_baremetal_only.py --selftest` | 0 | 49012143b | 5.89 | [baremetal-selftest.json](baremetal-selftest.json) |
| builder-absent | `python3 $OUTPUT/builder_absent.py` | 0 | 49012143b | 586.05 | [builder-absent.json](builder-absent.json) |
| builder-rv32 | `python3 sw/builder/test_builder.py --require-rv32` | 0 | 49012143b | 793.56 | [builder-rv32.json](builder-rv32.json) |
| ci-scope | `python3 scripts/ci_scope.py --selftest` | 0 | 49012143b | 2.06 | [ci-scope.json](ci-scope.json) |
| cpp-idiom | `python3 scripts/check_cpp_idiom.py` | 0 | 49012143b | 1.29 | [cpp-idiom.json](cpp-idiom.json) |
| diagram-pngs | `python3 scripts/check_diagram_pngs.py` | 0 | 49012143b | 0.35 | [diagram-pngs.json](diagram-pngs.json) |
| diff-check | `git diff --check 6d5ebd7357c1e468e446f18a61527c5be6118a04 HEAD` | 0 | 49012143b | 0.07 | [diff-check.json](diff-check.json) |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0 | 49012143b | 0.09 | [doc-paths.json](doc-paths.json) |
| doc-style-selftest | `python3 scripts/check_doc_style.py --selftest` | 0 | 49012143b | 0.06 | [doc-style-selftest.json](doc-style-selftest.json) |
| doc-style | `python3 scripts/check_doc_style.py` | 0 | 49012143b | 0.06 | [doc-style.json](doc-style.json) |
| docs | `python3 scripts/docs_check.py` | 0 | 49012143b | 4.29 | [docs.json](docs.json) |
| em-dash | `python3 scripts/check_em_dash.py --base 6d5ebd7357c1e468e446f18a61527c5be6118a04` | 0 | 49012143b | 3.52 | [em-dash.json](em-dash.json) |
| feature-status | `python3 scripts/check_feature_status.py --self-test` | 0 | 49012143b | 0.67 | [feature-status.json](feature-status.json) |
| gmstep-mutants | `make -C $LANES/602-phc-step-mr/tb/verilator/milan_dp gmstep-mutants` | 0 | 49012143b | 793.55 | [gmstep-mutants.json](gmstep-mutants.json) |
| gptp-docs | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | 49012143b | 0.18 | [gptp-docs.json](gptp-docs.json) |
| hygiene | `python3 scripts/check_hygiene.py --check` | 0 | 49012143b | 1.20 | [hygiene.json](hygiene.json) |
| milan-dp | `make -C $LANES/602-phc-step-mr/tb/verilator/milan_dp run` | 0 | 49012143b | 1642.38 | [milan-dp.json](milan-dp.json) |
| module-matrix | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | 49012143b | 0.97 | [module-matrix.json](module-matrix.json) |
| ooc-after | `python3 $OUTPUT/ooc_measure.py after` | 0 | 49012143b | 1200.46 | [ooc-after.json](ooc-after.json) |
| ooc-before | `python3 $OUTPUT/ooc_measure.py before` | 0 | 49012143b | 1195.99 | [ooc-before.json](ooc-before.json) |
| ooc-neutral | `python3 $OUTPUT/ooc_measure.py neutral` | 0 | 49012143b | 1181.66 | [ooc-neutral.json](ooc-neutral.json) |
| py-idiom | `python3 scripts/check_py_idiom.py` | 0 | 49012143b | 3.53 | [py-idiom.json](py-idiom.json) |
| rtl-lint | `python3 scripts/lint_rtl.py --check --jobs 8` | 0 | 49012143b | 11.30 | [rtl-lint.json](rtl-lint.json) |
| solution-docs | `python3 scripts/check_solution_docs.py` | 0 | 49012143b | 0.14 | [solution-docs.json](solution-docs.json) |
| source-lists | `python3 scripts/check_rtl_source_lists.py` | 0 | 49012143b | 1.41 | [source-lists.json](source-lists.json) |
| submodule-docs | `python3 scripts/check_submodule_docs.py` | 0 | 49012143b | 0.52 | [submodule-docs.json](submodule-docs.json) |
| sv-idiom | `python3 scripts/check_sv_idiom.py` | 0 | 49012143b | 0.45 | [sv-idiom.json](sv-idiom.json) |
| test-evidence | `python3 scripts/measure_test_evidence.py --check` | 0 | 49012143b | 5.87 | [test-evidence.json](test-evidence.json) |
| tkdiag | `make -C $LANES/602-phc-step-mr/tb/verilator/tkdiag` | 0 | 49012143b | 28.45 | [tkdiag.json](tkdiag.json) |
| toc-selftest | `python3 scripts/gen_toc.py --selftest` | 0 | 49012143b | 0.86 | [toc-selftest.json](toc-selftest.json) |
| toc | `python3 scripts/gen_toc.py --check` | 0 | 49012143b | 2.59 | [toc.json](toc.json) |

All commands run in the foreground with explicit timeouts, from `$LANES/602-phc-step-mr`, without pipes. Receipts carry elapsed time, timeout, full log size and SHA-256. `$OUTPUT` denotes this handoff directory. OOC `before` and `neutral` are executed at the final head while taking their datapath input from the pinned base; `after` takes the committed candidate.

## Delivery

Local commits and `PR-BODY.md` are prepared. The prior STOP is resolved by the scope correction. No push, PR operation or merge occurred. [TAKEN](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859307452) and [STOP](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859611271) remain unchanged. The final [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/602#issuecomment-5859870644) comment is posted; `REVIEW-READY.md` contains its exact body and `review-ready-publication.json` records the publication.

`final-audit.json` confirms the exact head, three one-line commits without bodies or trailers, clean worktree, and clean pinned submodules. All 566 pinned submodule blobs were checked against their commit objects, with the submodule root verified before each Git command. All 34 final-head gate logs match their recorded sizes and SHA-256 values. Every output file is below 200 KB; generated trees, build products and larger logs remain outside this directory, with size and SHA-256 recorded in receipts. All foreground verification has finished.
