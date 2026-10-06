[R475] NEGATIVE - exact head 4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f

R475-1 is an independent external review of issue #645 / PR #672, including #647. All five lenses were applied. Three findings remain open: one MAJOR and two MINOR. No lens is banked CLEAN. This verdict does not authorize a merge.

Identity and reconstruction

- Reviewed tree: `1cb3772cf102a9296b4fea2db7096315c3c76360`.
- Requested source-base comparison: `fea346e76c2a57ed5cd131af8fc68dfeff57f877..4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f`.
- Read repository operating rules, contribution rules and the documentation index; then the issue bodies and public scope decisions; then requirements, interface/design authorities, diff and history; then public executable evidence. The additional `28f9666f..HEAD` comparison separates the 28 lane-owned paths from intervening dev merges. Those merges adopt processor `ead80360`; the last merge changes only `docs/findings/653_DISCONNECT_ORDER_BENCH.md` relative to `f325c3ab`.
- Public authorities: [#645](https://github.com/kebag-logic/milan-fpga/issues/645), [#647](https://github.com/kebag-logic/milan-fpga/issues/647), [option C](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5982568394), [own-area and #657 scope](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5985974804), [depth/envelope ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5987852678), [decision-PDU/startup/reset ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5990646410), [timing/comment ruling](https://github.com/kebag-logic/milan-fpga/issues/645#issuecomment-5994641859).
- Executable evidence was read only from [public commit 6efdd244](https://github.com/kebag-logic/milan-fpga/tree/6efdd2447c72b9b60f5d0d9e393c851bb742945a/review-evidence/645-r1). All 591 files named by its publication manifest matched their published hashes. The 20 follow-ring input hashes match this checkout; the authorized comment-only difference and final documentation-only merge are separately identified. See `receipts/public-evidence-integrity.json` and `receipts/follow-source-identity.json`.
- No other reviewer's report or private author material was read. After the independent diff pass, the public PR snapshot contained two review-start comments, zero reviews and zero inline review comments. There were no prior public review findings to resolve or retain; see `receipts/prior-findings.json`.

[R475] MAJOR Conformance, RTL, Robustness, Tests, Docs - F1 - `hdl/ieee1722/aaf/KL_chan_map_capture.sv:1062` - The declared five-pop hold can occupy two output PDUs

Authority/evidence: Stage 2d requires the exact declared repeat/gap at the decision PDU only, with zero ordering errors elsewhere. `docs/design/MEDIA_CLOCK_FOLLOWING.md:1169`, `tb/verilator/milan_dp/README.md:211`, and `tb/verilator/milan_dp/sim_ax1x1gptp.cpp:740` make this a single output-PDU bound; the checker increments `recentre_span_bad` if the same decision appears in another output PDU. The capture RTL starts a hold at the next walk and counts down one pop per walk, independently of the packetizer's six-event output position.

The independent `scripts/probe_output_span.py` keeps the capture and packetizer RTL unchanged. It feeds ordinary six-event PDUs, drains the previous PDU, and moves the output packet phase through all six positions before requesting the same empty-queue recentre. Phases 0 and 1 place all five repeats in one output PDU; phases 2 through 5 place them in two. At phase 2, consecutive output PDUs contain `5,6,6,6,6,6` and `6,7,8,9,10,11`: four repeats in the first, one in the second. Every case has exactly five repeats and zero duplicate/skip counter increments. The probe reports 427 checks, four failures, all four on the single-output-PDU assertion. The unchanged unit suite separately passes 408 checks. Raw receipts: `receipts/span-probe.log`, `receipts/span-probe.rc`, `receipts/capture-unit.log`.

Impact: A legal packet phase produces a discontinuity outside the one output PDU covered by the declaration. The bound on total repeated events is correct, but the bound on where those events occur is not. The current physical normal run checks only its observed startup/reset phases; the existing hold-five unit case explicitly aligns the output frame first and misses this boundary.

Required outcome: Satisfy the existing single-output-PDU declaration across packet phases and add wire-visible phase coverage. If a multi-PDU action is intended instead, obtain an explicit public scope/contract decision before changing the declaration and checker. Preserve exact event accounting, pair lockstep, unchanged slip counters, and rejection of additional repeats/gaps; do not replace the exact allowance with a grace interval.

Verification: Re-run the six-phase probe, the physical normal and both ordering controls, and the four arrival/INTERNAL campaigns at the corrected head. Each declared action must satisfy the finally authorized span and step; everything outside it must remain strictly ordered.

[R475] MINOR Docs - F2 - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1092` - Disengaged INTERNAL is documented as immediate but waits the same 2,048-tick dwell

Authority/evidence: The table says "or at once if it is not engaged." In `hdl/milan/milan_datapath.sv:6357`, disengagement makes `settle_steady_w` true, but `settle_need_w` remains `SRC_SETTLE_TICKS_C`. There is no immediate-fire arm. A probe of the verbatim root control, switching from a followed source to INTERNAL with the aligner disengaged, observes the pulse after 2,048 counted media ticks plus its registered evaluation edge, about 42.67 ms at 48 kHz. `scripts/probe_settle.py` and `receipts/settle-probe.log` also verify the 196,608-tick LOCKED dwell and 2^20-tick unlocked ceiling.

Impact: The authoritative design gives an incorrect trigger latency for a supported boundary condition. This changes a behavior/bound claim, so it is MINOR under the review rule, not wording-only RESIDUE.

Required outcome: State the implemented disengaged-INTERNAL dwell accurately: when disengaged, the same 2,048-tick run can complete without waiting for an aligner band. If immediate action is intended, obtain a public decision and implement/test it; do not silently change the behavior to match prose.

Verification: The documented trigger must agree with the exact root-control measurement for engaged/in-band and disengaged INTERNAL cases.

[R475] MINOR Conformance, Tests, Docs - F3 - `tb/verilator/follow_ring/Makefile:30`; `docs/traceability/MODULE_MATRIX.md:7` - The new harness leaves the mandatory traceability artifacts stale

Authority/evidence: REQ-VER-04 requires generated artifacts and traceability to be green. `.github/workflows/docs.yml:137` runs `python3 docs/traceability/gen_module_matrix.py --check`. This read-only command passes at dev `28f9666f` and exits 1 at the reviewed head: the top matrix and twelve `README-tests.md` files are stale. The exact-head hosted `docs-check` job fails this same named step; later steps are skipped. The public 26-command source receipt omits this command, so that bank does not establish this gate's result. See `receipts/traceability-base.log`, `receipts/traceability-head.log`, `receipts/traceability-head.diff`, and `receipts/hosted-docs-steps.json`.

The repair must also preserve truthful coverage. The generator currently treats the new `DP_SRC` text-extraction input as a compiled `milan_datapath` source. Its generated result consequently credits `follow_ring` with the entire datapath and unrelated descendants, although `follow_ring` compiles selected leaf modules and copied glue. `docs/traceability/gen_module_matrix.py:140` scans every `.sv` name in a Makefile, and the retained generated diff demonstrates this false attribution. Merely accepting that generated diff would satisfy byte consistency while adding inaccurate coverage claims.

Impact: A mandatory exact-head context fails, and the durable test inventory has not been integrated with the reduced harness's actual coverage boundary.

Required outcome: Integrate the reduced harness into traceability without attributing uninstantiated full-datapath coverage, regenerate the affected artifacts, and include the no-drift command in the recorded source gate set. Keep the untested ratchet unchanged unless actual new evidence warrants a reduction.

Verification: The same command must pass at the corrected head, the generated matrix must name the actual compiled/exercised scope, and the required hosted context must execute successfully. `scripts/probe_traceability.py` reproduces the base/head comparison without editing this checkout.

Independent lens results and retained evidence

| Lens | What was examined and established | Open result |
|---|---|---|
| Conformance | #645/#647 bodies and all five scope rulings; REQUIREMENTS.md, `TIME_SYNC.md:363`, `MEDIA_CLOCK_FOLLOWING.md:1058`; depth 16, derived target 11, maximum five holds/one drop, no slip charge, source-switch/INTERNAL trigger and unchanged AAF law. The interface discrepancy is F1; mandatory traceability is F3. | F1, F3 |
| RTL | `milan_datapath.sv:1304`, `:5778`, `:6272`, `:6340`; `KL_chan_map_capture.sv:501`, `:803`, `:877`, `:1038`. Checked root binding, unchanged original trigger, synchronous reset, counter widths, saturating slip accounting, same-cycle pop/push arithmetic, pair-wide action transfer, and flush precedence. Added state stays in the axis domain. The extracted control reaches its dwell/ceiling values; the capture/packetizer phase probe exposes F1. Area evidence independently checks below the ruled limit. | F1 |
| Robustness | Capture unit cases for empty/full queues, hold/drop/no-op, unprimed state, flush and pulse on the first PDU beat; all 32 INTERNAL hold/phase cases; three full-duration phases in each arrival envelope; source changes and the following-disabled ceiling in the extracted controller. Packet-boundary placement fails F1. | F1 |
| Tests | `follow_ring/dp_glue.py`, wrapper, stimulus, margin and render-law oracle, sweep and mutation drivers; `chmap_capture/sim_main.cpp:1656`; physical order plan/actual sample comparison at `sim_ax1x1gptp.cpp:671`, `:740`, `:758`; `verify_recentres.py`; render PULLIN/LAW/boundary code and public logs. Exact expectation is derived from the ruled target, not hold/drop outputs or observed samples. Controls fail at the required locations. Ungradable render windows earn no law credit. Missing output-phase coverage is F1; traceability is F3. | F1, F3 |
| Docs | Design, timing, register and testing documentation, PR body, issue decisions, public recipes and measured tables; the stale depth fix `e80dd7ad` and its pre-edit context search. All five follow-ring and twenty capture-coherence edit arms still plant at this head. Single-PDU and disengaged-INTERNAL claims require F1/F2 correction; generated inventory requires F3. | F1, F2, F3 |

The diagnosis is consistent with the public bench observations: frequency-only acquisition moves phase before lock, the old render trigger runs early, and the loopback queue previously lacked a recentre. The changed render stage itself is not rewritten; the additional root pulse restores the declared fill/first-event law after the measured INTERNAL pull-in. This is simulation evidence, not a new hardware finding.

Independent executions

| Execution | Result / receipt |
|---|---|
| Unchanged capture unit | 408 checks, zero failures; `receipts/capture-unit.log` |
| Six output-phase boundary probe | 427 checks, four single-PDU failures; all event-count/counter checks pass; `receipts/span-probe.log` |
| Exact root control probe | INTERNAL disengaged: 2,048 ticks; LOCKED: 196,608 ticks; unlocked ceiling: 1,048,576 ticks, each plus its pulse evaluation edge; `receipts/settle-probe.log` |
| INTERNAL sweep | 32/32 runs pass, two hold lengths at sixteen phases; zero post-decision slips, 27 fully gradable before/after pairs; `receipts/campaigns/internal/` |
| Arrival reruns | Three complete phases per envelope, k=0,1,2 of k/16, seeds 645+k; 40 s first hold and 20 s each following switch. All twelve runs pass, with zero post-decision slips. Remaining duplicate runs were explicitly cancelled; no full independent sixteen-phase campaign pass is claimed. `receipts/campaign-summary.json`, `receipts/campaigns/partial-run-disposition.json` |
| Five existing fault controls | 5/5 caught: NO-SETTLE, RENDER-ONLY, EARLY, W1 and OVERSHOOT; `receipts/follow-mutants.log`, rc 0 |
| Own-area arithmetic/shared proof | OOC +80 LUT/+73 FF; routed bound 112 LUT/73 FF; all ten functions equal over 65,536 assignments, planted truth-table defect caught; `receipts/area-verification.json`, `receipts/shared-proof.log` |
| Traceability comparison | Base passes, head fails; `receipts/traceability-base.log`, `receipts/traceability-head.log` |

The independent arrival minima (empty/full, in ticks) are 5.414400/5.514240 with no lateness, 5.406720/5.283840 at 0..5 us, 4.170240/5.091840 with the rare tail, and 2.565120/2.764800 at 0..60 us. INTERNAL minima are 4.984320/5.091840. These are the completed local subset, not replacements for the public full-sweep minima.

The public source evidence reports sixteen phases in each of four arrival campaigns, zero post-decision slips, and full-sweep empty/full minima 4.984320/5.076480, 4.899840/4.907520, 3.893760/5.091840 and 2.565120/2.234880. It reports the full datapath, render, media-clock, builder, parser and portability banks separately. The public physical normal log contains 143 checks with no failures, accounting 40/0, and ordering controls 14/0. Startup and reset each declare and observe -5 events, at output PDUs 6047 and 92220, with both slip counters unchanged. The larger-step control declares -4 and observes -5; the undeclared-repeat control fails at output PDU 6049 outside the declared PDU. Those controls are meaningful; their passing normal phases do not address F1's phase dependence.

Area and timing interpretation

The OOC deltas are (67-41)+(1130-1076)=80 LUT and (92-51)+(1368-1336)=73 FF. The routed bound is 80 cone LUTs - 1 already counted in capture - 6 identical direct functions - 10 exhaustively equal shared functions + 49 capture LUTs = 112 LUT; 41 settle FF + 32 capture FF = 73. The named cell lists, query scope, LUT/CARRY equations and planted control were inspected; the equivalence proof was rerun from the public tables. No implementation run was launched.

All timing cells below are measured WNS/WHS in ns, using the published shipping 1x1 recipe, part xc7a100t-fgg484-2, AreaOptimized_high synthesis, ExploreArea optimization, named placement directive, AggressiveExplore physical optimization/routing, 32 threads and default seed. Each tree's directives reuse its own fresh synthesis checkpoint. Slow/Fast are fixed timing models; 0/85 C power settings repeat those models rather than supplying four independent timing corners.

| Tree | Placement directive | Slow WNS/WHS | Fast WNS/WHS | Margin grade |
|---|---|---|---|---|
| fa450d30 base | ExtraPostPlacementOpt | +0.244/+0.102 | +1.638/+0.036 | PASS |
| fa450d30 base | AltSpreadLogic_high | +0.026/+0.049 | +1.478/+0.014 | FAIL |
| fa450d30 base | ExtraTimingOpt | +0.056/+0.049 | +1.478/+0.017 | PASS |
| reviewed head | ExtraPostPlacementOpt | +0.151/+0.099 | +1.552/+0.036 | PASS |
| reviewed head | AltSpreadLogic_high | +0.101/+0.097 | +1.385/+0.033 | PASS |
| reviewed head | ExtraTimingOpt | -0.209/+0.062 | +1.420/+0.030 | FAIL |

The head's ExtraTimingOpt failure has TNS -0.294 ns at two setup endpoints and one Route 35-39 diagnostic. Its worst path runs from notification `wr_ix_r_reg[0]_replica_4` to transmit-arbiter `slot_r_reg[0]/D`, 42 logic levels. The older base minimum is an SDRAM path, and that base predates the adopted processor pin. Implementation rc 0 is not timing success. The base miss permits review readiness under the public ruling; it does not prove this head's processor-path failure is pre-existing. The manager's current-dev table remains required before any merge decision.

Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #645/#647 rulings; REQUIREMENTS.md; design/render law; decision-PDU and traceability receipts (F1, F3) | R475-1, applied; no clean coverage | 4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f |
| RTL | UNCLEAN | root settle control; capture pop/push/action logic; packetizer phase probe; public OOC/routed/timing artifacts (F1) | R475-1, applied; no clean coverage | 4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f |
| Robustness | UNCLEAN | capture boundary/flush/reset cases; INTERNAL and arrival reruns; controller ceiling; output phases (F1) | R475-1, applied; no clean coverage | 4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f |
| Tests | UNCLEAN | follow-ring/render/physical oracles and controls; phase probe; traceability generator and generated diff (F1, F3) | R475-1, applied; no clean coverage | 4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f |
| Docs | UNCLEAN | design/TIME_SYNC/register/testing docs; issue/PR declarations; generated matrices; public evidence and stale-comment planting proof (F1, F2, F3) | R475-1, applied; no clean coverage | 4e1ddee9d7b9ebf58ebebcacd90c5d72dce0c96f |

Limits and manager duties

This review makes no hardware, physical calibration, licensed ACMP/SRP streaming, PHY/MAC, CPU/DDR, physical TDM render, or field-conformance claim. Ungradable windows, first-10-ms warm-up exclusions, and NOT RUN fields remain exclusions. The historical Arty area-calibration arm is NOT RUN. The four historical full render-mutation failures remain with #657; they were not repaired or represented as passing here. No full parent/processor/gPTP/builder/portability bank was rerun by this reviewer.

The exact-head hosted snapshot had `rtl-fast` successful, `docs-check` failed at traceability, physical gPTP skipped, and several long jobs/aggregate work still running. A skipped physical context is not executed evidence. Hosted/local-replica acceptance remains the manager's, including the requested physical job. This report does not clear a missing or skipped required execution.

The manager must resolve and independently re-review F1-F3; obtain the same-recipe timing table at current dev `28f9666f` and apply the STOP/follow-up ruling without changing the failing grades; satisfy both independent-review and all-lens coverage requirements; reconcile the reported #658 Makefile lane conflict if applicable; build and validate the final current-dev merge candidate; obtain explicit merge authorization; then perform containment and retain the bench obligations before closing the full task. Source-head evidence is not final-candidate validation.

All probes used disposable files under this packet's `scratch/`. No tracked source edits, commits, pushes, GitHub writes, external contact, shared installation, hardware access, or implementation runs were performed. The final raw-blob/mode/index/gitlink audit passed for 1,897 tracked blobs across this checkout and all three required submodules, with clean indexes/worktrees and exact pins; see `receipts/checkout-final.json`. Private toolchain installation prefixes are replaced by `<SIMULATOR_ROOT>` in four public build logs; execution results and all test lines are retained. Unmodified originals remain unpublished under scratch, with original and published hashes recorded in `receipts/publication-redactions.json`. Only files in `MANIFEST.sha256` and this report are publishable; scratch is excluded.

R475-1 FINISHED
