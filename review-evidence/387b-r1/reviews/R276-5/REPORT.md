[R276] NEGATIVE - exact head a21cd3585abdd3cdf4ac5774a048361a66fed043

Round R276-5 is the internal cleared-context review of issue #387 / PR #555 (acceptance 3, the datapath half).

- Head `a21cd3585abdd3cdf4ac5774a048361a66fed043`, tree `5376deee90b2e0732f533f287daaf7dfc666f32e`.
- Range `57456af96b3127b9d309a995bbbd35a6113ce52d..a21cd358`: 22 files, +1155/-126. It is ten commits: `29036eb4`..`00d388d8`, the merge `e68c1b1a` of dev `57456af9`, `a9636e0f`, and `d5dc47c0`..`a21cd358`.
- All five lenses were applied at this head.

The datapath behaviour conforms to the #387 decisions and rulings at this head, and the executable evidence supports it:
- a PHC step is one `mr` toggle and one Table 5.4 MEDIA_RESET, whatever the clock source;
- the render stage re-bases once;
- a request on a pending restart merges until the first PDU at the adopted level is reported;
- no request is cancelled.

Every prior public finding on this PR is resolved at this head.

The verdict is NEGATIVE because two MINOR findings are open:
- **F1.** The exact-head hosted `milan_dp` window leaves 8.9% of its 2700 s deadline. That is below the 10% revisit trigger the manager recorded in 5819379503 item 2, while the PR and `CI_WORKFLOWS.md` state 16%.
- **F2.** `docs/fpga/FPGA_DESIGN.md` still says the CRF-selection verdict gates the whole `mr` machinery and that it is idle at INTERNAL. This change made that untrue, and it corrected the identical sentence in `REGISTER_MAP.md`.

Conformance, RTL and Robustness are covered clean. Tests and Docs are unclean.

## Reconstruction

The sources were read in this order:
1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. The issue #387 body and its frozen acceptance.
3. The decisions and rulings:
   - 5606198212 (part b);
   - 5794731090 (owner step policy);
   - 5802264260 (items 1 and 2);
   - 5810378282 (the aligner gets no re-centre);
   - 5816509317 (#545 slew coupling);
   - 5818091077 (pending ends on the wire);
   - 5819379503 (option (a): the feed report is "launched"; the sweep controls stay; the 10% trigger).
4. The assignments 5814963103, 5816975318, 5817362105 and 5818091077.
5. The public author notes [A256], [A268], [A269] and [A270].
6. The PR #555 body.
7. The diff and its history, including the merge parents and the dev-side rows.
8. The exact-head hosted check runs and the shard 4/5 log.

The prior public review findings (R276-4, R277-3) were read only after this round's verdict, findings and ledger had been drafted to REPORT.md. See "Prior public findings" below.

## Findings

### F1 - MINOR - Tests, Docs - `docs/testing/CI_WORKFLOWS.md:169-175`, PR #555 "Known limitations / Sweep time", hosted shard 4/5 job 107763352706

**The exact-head `milan_dp` margin is under the ruled 10% trigger.**

- **Authority/evidence.**
  - Decision 5819379503 item 2: "The measured hosted margin is 435 s of 2,700 s (16%). If a later change brings it under 10%, the budget or the split is revisited."
  - `CI_WORKFLOWS.md:174` and the PR's "Known limitations" state that margin from the `a9636e0f` sample.
  - At this exact head, hosted rtl-full run 36038109516, job 107763352706 ("Verilator shard 4/5", head_sha `a21cd358`) timed the suite from its `shard: 4/5` line (18:01:19.387Z) to `PASS milan_dp` (18:42:19.258Z): 2459.9 s, 9781 checks. That leaves 240.1 s, 8.9% of 2700 s (`receipts/milan_dp_hosted_windows.txt`, `scripts/milan_dp_window.py`, read-only).
- **Runner noise is large relative to that margin.** Measured the same way:
  - The same 9635-check content ran 1296.1 to 2049.9 s across six dev pushes on 2026-09-24.
  - Dev `57456af9` ran 2133.3 s, and live dev `573f0052` ran 2150.6 s.
  - `a9636e0f` ran 2264.9 s.
  - The head differs from `a9636e0f` only by six checks, two 4096-cycle settles in three short legs, and docs. So the 195 s rise is noise, and that noise is larger than the margin.
- **Impact.**
  - A hosted `milan_dp` timeout is a red required context (the driver exits 92). With this PR's added sweep cost, the observed spread already reaches within 240 s of the deadline.
  - The documented and PR-stated margin (435 s, 16%) is a single non-head sample. The measurement at the head under review meets the ruling's own revisit condition.
- **Required outcome.** A published decision under 5819379503 item 2 on this exact-head figure: revisit the budget or the split, move the three default controls to the explicit campaign, or rule the sample out with further samples. The margin statement in `CI_WORKFLOWS.md` and the PR must reflect whatever figure that decision rests on.
- **Verification.** The shard 4/5 window at the candidate (or at the samples the decision cites) is recorded next to the budget, and the stated margin equals 2700 s minus that window.

### F2 - MINOR - Docs - `docs/fpga/FPGA_DESIGN.md:170-175` (secondary: `docs/reference/MILAN_COMPLIANCE_MATRIX.md:120`, `docs/MILAN_V12_ROADMAP.md:356-359`)

**A current architecture page still gives the pre-#387 `mr` gating.**

- **Authority/evidence.**
  - `FPGA_DESIGN.md` is the current "Locate RTL modules" authority in docs/README.md. It reads: "the one registered verdict gates `KL_mmcm_drp_servo`, the `KL_media_grid_align` packet-grid chain and the 1722-2016 4.4.4.3 `mr` machinery; at the INTERNAL power-on state everything still reads idle".
  - Since this change, `milan_datapath.sv:3110-3113` ORs `media_rebase_p_w` into `mcr_restart_p_w` outside the `crf_clk_selected_r` gate. A settime or plane-off adjtime at INTERNAL toggles `mr` and counts MEDIA_RESET, and the option-off legs grade exactly that.
  - This PR rewrote the identical sentence in `REGISTER_MAP.md:124-133` to "the CRF triggers of the 4.4.4.3 `mr` machinery ... A PHC step toggles `mr` on every running Stream Output whatever the selection". `FPGA_DESIGN.md` was not touched.
  - Less strictly, the compliance matrix (`:120`, "arms the servo, the grid-align chain and `mr` from the stored index") and the roadmap note (`:356-359`) carry the same unscoped wording.
- **Impact.** A current architecture page states a gating contract the RTL no longer has. An integrator reading it would expect no `mr` activity at INTERNAL selection.
- **Required outcome.** `FPGA_DESIGN.md` scopes the verdict to the CRF triggers and states that a PHC step toggles `mr` whatever the selection, as `REGISTER_MAP.md` now does. Scoping the matrix and roadmap wording the same way is optional.
- **Verification.** Inspection at the corrected head, and the docs gates pass.

### Suggestions (do not affect coverage)

- **S1 (Docs), PR #555 body.** "Status" ("Open: R277-3's property probe P1 ..."), "Decisions" item 1 ("Decision requested") and the DoD line ("the probe conflict awaits a decision") predate decision 5819379503, which chose option (a). Citing that decision would let a cold reader see the residue is ruled.
- **S2 (Docs), `hdl/ieee1722/aaf/KL_render_setpoint.sv:120`.** The module summary still reads "re-centred once on a GM/PHC step". The banner (`:81-89`) and port spec (`:169-173`) now say "a PHC step or a settled clock-source change"; the summary could say the same.
- **S3 (Tests).** A software settime re-centring the render stage is pinned only structurally (builder gate 1b, `render_recentre_p_w` exactly `media_rebase_p_w | src_recentre_p_r`). No simulation leg issues a settime and counts a re-base: gmstep drives the plane's step, and `sim_aclk` counts pulses without a settime. This is pre-existing (#386 had the same set). A behavioural arm would close it.

## Judgements the round asked for

- **IEEE 1722-2016 4.4.4.3 and Milan Table 5.4.** Conforms.
  - `media_rebase_p_w = eff_ptp_adjust_w | cfg_ptp_cmd_load` (`milan_datapath.sv:3110`) is ORed into `mcr_restart_p_w` outside the CRF gate (`:3111-3113`). The CRF disruption and echo stay gated, per 10.4.3.
  - `eff_ptp_adjust_w` is the plane's `gptp_step_we_w` when the plane is on and CLKV adjtime when it is off (`:2750-2751`). Settime always stays with software (`:2743-2745`).
  - The step is an `axis_clk` pulse that already fed `ptp_csr_sync` (aclk = `axis_clk`), so no crossing is added.
  - The eight-PDU hold is unchanged and per stream (`KL_media_clock_restart.sv:240-257`). MEDIA_RESET counts the bit each reported PDU carried.
  - gmstep at this head passes 48/48 (`receipts/gmstep_head.log`).
  - The option-off legs grade the adjtime parity and the settime's one toggle and one MEDIA_RESET at INTERNAL: `obj_dir` 233/0, `obj_nolpf` 233/0, `obj_ax1x1` 230/0 (`receipts/optionoff_head.log`, `nolpf_head.log`, `ax1x1_head.log`).
- **Reading 1, "pending = requested but not on the wire".** Implemented as ruled in 5818091077 and 5819379503 item 1. The window closes at the first reported PDU at the adopted level (`KL_media_clock_restart.sv:230`, `:236-238`), and the banner (`:55-91`) states the launch-to-report residue. My independent property probe grades the engine on the feed only (`scripts/mcr_property/`):
  - The head engine is clean on 120 randomized runs: 60 seeds, continuous streams and random stop/start, 300k cycles each, 3 talkers at AAF-like and CRF-like rates, 0-3 cycle report latency with a shared feed. That is 229,975 requests and 182,841 toggles, with 0 spurious toggles, 0 hold violations (< 8 PDUs), 0 requests starved past one hold plus one PDU, and 0 left pending.
  - 3,365 requests landed in a launch-to-report gap: the ruled residue, bounded by the report latency.
  - Six planted engines each fail 116-120 of 120 runs: flip-per-request (the pre-#387 rule), a window ending at adoption (the `a9636e0f` rule), a window open for the whole hold, a window one PDU late, a 7-PDU hold, and a hold counting any level (`receipts/mcr_property_summary.txt`, `mcr_property_mutant_first_fails.txt`).
  - Three reference-model errors of my own were found and fixed before the final run: the stream-start baseline and the two-cycle grant latency. They are recorded in `scripts/mcr_property/mcr_prop.cpp`, and the engine was not at fault in any of them.
- **Reading 2, "streams may end on opposite `mr` levels".** Accepted.
  - 4.4.4.3's toggle and hold are per stream, and 10.4.3 validates only the recovered stream's bit.
  - Each stream still gets at least one toggle per restart need: the probe's per-talker service and liveness properties hold.
  - `tgt_r` has no reader outside the engine, its benches and `sim_nxn.cpp:3108`, which now flips every context.
  - `KL_crf_tx.sv` changed only in comments.
- **The changed legacy tv/mr check (`sim_main.cpp:973-979`).** Not a weakening.
  - It masks only bit 3 (`& 0xF7`, still `0x81`: sv, version, gv, tv graded) and adds a parity check against the steps the harness issued (`:560`, `:1048`).
  - The settime arm (`:1063-1072`) follows a 4096-cycle settle.
  - Controls h9 (`settime_no_mr`) and h10 (the step gated by CRF selection) each fail their named check (`receipts/gmstep_controls_part2.log`).
- **Sweep time.** Locally: the gmstep leg with its build took 38 s. The two positive legs, the three acceptance controls and one reviewer control took 178 s. The eight other controls took 258.5 s (Verilator 5.050, 8 jobs). The hosted margin is F1.
- **The #387 part b aligner decision is untouched.**
  - `KL_media_grid_align.sv`, `KL_mmcm_drp_servo.sv` and `hdl/ieee8021as` do not differ across the range.
  - The `GM_LOSS_RECOVERY.md` grid-aligner and CRF-servo rows are byte-identical to dev `57456af9` (`receipts/scope_checks.txt`).
  - The gitlinks are unchanged.

## Lens results (clean lines carry their evidence)

- `[R276] PASS Conformance - hdl/milan/milan_datapath.sv:2743-2751,3097-3113,6017-6028; hdl/ieee1722/avtp/KL_media_clock_restart.sv:55-135,214-259; receipts/gmstep_head.log, optionoff_head.log, nolpf_head.log, ax1x1_head.log, mcr_property_summary.txt - checked against 1722-2016 4.4.4.3 and 10.4.3, Milan Table 5.4, decision 5606198212 part b, owner decision 5794731090, rulings 5802264260 items 1-2, 5818091077 and 5819379503 item 1; the step is one toggle and one count ungated by selection, merged while pending, never cancelled.`
- `[R276] PASS RTL - KL_media_clock_restart.sv:197-259 (per-talker tgt_r width and reset, request on the adoption cycle reads the pre-edge mr_o and merges, request in the report cycle sees hold_r == 0, a stopped stream re-satisfies its hold); milan_datapath.sv:2750,3110-3143 (axis_clk only, no new crossing; the step pulse is idempotent under the merge); KL_render_setpoint.sv and KL_crf_tx.sv comment-only; receipts/lint_rtl_check.log (90 <= 90); hosted yosys-elaboration, Yosys shards 0-3, verilator-lint and elaborate success at a21cd358 (receipts/hosted_checkruns_head.tsv).`
- `[R276] PASS Robustness - scripts/mcr_property/ against KL_media_clock_restart.sv at head: repeated and back-to-back requests, a source change and a restart in one cycle, streams stopping and starting mid-pending, three rates, 0-3 cycle report latency with feed contention, minimum hold (planted 7-PDU hold killed), 120/120 clean; tkdiag T12, T15, T17, T18 96/96 with 4/4 engine mutants (receipts/tkdiag_head.log); INTERNAL and plane-off paths graded by the three option-off legs.`
- `[R276] MINOR Tests - hosted job 107763352706 - F1.` Also applied and found sound:
  - every one of the eleven lane controls fails its named check (`receipts/gmstep_controls_part1.log`, `part2.log`);
  - a reviewer control that requests a second restart 3000 cycles after the step fails "restart: the outgoing mr toggles exactly once", so the upper bound is graded;
  - the positive gmstep and option-off legs pass through the runner;
  - tkdiag's T12 and T15 edits keep the per-stream hold graded;
  - the `run` wiring (`Makefile:436`, `:532-533`) and `measure_test_evidence --check` exit 0 (`receipts/docs_gates.log`).
- `[R276] MINOR Docs - docs/testing/CI_WORKFLOWS.md:169-175 - F1` and `[R276] MINOR Docs - docs/fpga/FPGA_DESIGN.md:170-175 - F2`. Also applied and found sound:
  - `GM_LOSS_RECOVERY.md:148-208,234-235`, `TIME_SYNC.md:197`, `REGISTER_MAP.md:124-133`, `TESTING.md:267,501`, the milan_dp README, `CHANGELOG.md:30-52`, the `BAREMETAL_FIRMWARE.md` 1b rows and the RTL banners match the code;
  - `docs_check`, `check_em_dash --base 57456af9`, `gen_toc --check`, `check_doc_style`, `check_doc_paths` and `check_gptp_docs` exit 0 with the pinned renderer (`receipts/docs_gates.log`).

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `milan_datapath.sv:2743-2751,3097-3113,6017-6028`; `KL_media_clock_restart.sv`; #387 decisions and rulings; gmstep, three option-off legs, the engine property probe | R276-5 | a21cd3585abdd3cdf4ac5774a048361a66fed043 |
| RTL | CLEAN | `KL_media_clock_restart.sv`, `milan_datapath.sv` hunks, `KL_render_setpoint.sv`, `KL_crf_tx.sv`; lint ratchet; hosted Yosys, lint and elaborate | R276-5 | a21cd3585abdd3cdf4ac5774a048361a66fed043 |
| Robustness | CLEAN | Engine property probe (120 runs, 6 planted engines); tkdiag T12, T15, T17, T18 plus 4 mutants; option-off INTERNAL paths | R276-5 | a21cd3585abdd3cdf4ac5774a048361a66fed043 |
| Tests | UNCLEAN (F1) | `sim_gmstep.cpp`, `gmstep_mutants.py` (all 11 plus 1 reviewer control), tkdiag `sim_main.cpp` and `mcr_mutants.py`, milan_dp `sim_main.cpp`, `sim_nxn.cpp`, both Makefiles, the `test_builder.py` gate 1b diff, hosted shard timing | R276-5 | a21cd3585abdd3cdf4ac5774a048361a66fed043 |
| Docs | UNCLEAN (F1, F2) | CHANGELOG, `GM_LOSS_RECOVERY.md`, `TIME_SYNC.md`, `REGISTER_MAP.md`, `TESTING.md`, `CI_WORKFLOWS.md`, `BAREMETAL_FIRMWARE.md`, `FPGA_DESIGN.md`, compliance matrix, milan_dp README, RTL banners, PR body | R276-5 | a21cd3585abdd3cdf4ac5774a048361a66fed043 |

## Prior public findings (read after this round's verdict and ledger were drafted)

Status of each prior finding at `a21cd358`:

| Finding | Status | Evidence |
|---|---|---|
| R276-4 F1 = R277-3 F1 (BLOCKER, builder gate 1b pin) | Resolved | `test_builder.py:8860-8887` pins `media_rebase_p_w`, `mcr_restart_p_w`, the direct engine port and `render_recentre_p_w`. Seven refusal mutants are added (`:12624-12653`). Hosted `elaborate` (which runs `test_builder.py --require-elaboration --require-rv32`), `docs-check` and `docs-check-no-git` succeed at this head. I did not run the builder bank (outside this round's allowance) |
| R276-4 F2 = R277-3 F3 (MINOR, the pending boundary) | Resolved | Ruling 5818091077; `KL_media_clock_restart.sv:236-238`; the banner no longer claims listeners saw the toggle in the gap; the `GM_LOSS_RECOVERY.md:157` row; T17 and T18 with 4 mutants; my feed-graded property probe is clean. R277-3's P1 residue is ruled acceptable by 5819379503 item 1 and documented at `:79-91` |
| R276-4 F3 = R277-3 F4 (MINOR, render stage banner and port) | Resolved | `KL_render_setpoint.sv:81-89`, `:169-173`. The one-line summary at `:120` is this round's S2 |
| R276-4 F4 (MINOR, margin on a stale figure) | Resolved as filed | The PR and `CI_WORKFLOWS.md` now state a hosted measurement (`a9636e0f`), and the manager ruled on it (5819379503 item 2). Its concern returns as this round's F1: the exact-head measurement crosses that ruling's trigger |
| R277-3 F2 (MINOR, no settime check) | Resolved | `sim_main.cpp:1036-1072`; `settime_no_mr` (h9) caught; three legs pass |
| R276-4 S1 = R277-3 S2 (PR status head) | Resolved | The PR status names `a21cd358`. The decision-state text is stale: this round's S1 |
| R276-4 S2 = R277-3 S4 (stale positive binary) | Resolved | `is_fresh()` in both runners |
| R277-3 S1 (margin record) | Resolved | `CI_WORKFLOWS.md:169-175` (see F1) |
| R277-3 S3 (INTERNAL-source citation) | Resolved | `GM_LOSS_RECOVERY.md:155` cites the option-off legs and their CRF-gating control |

Reading them changed no finding and no ledger row of this round.

## Receipts and scripts (all under MANIFEST.sha256)

- **Scripts.**
  - `scripts/mcr_property/{mcr_prop.cpp,mcr_prop_top.sv,plant.py,run.sh}`: the engine property probe and its six planted engines. Usage: `run.sh <tree> <workdir> 60 300000`.
  - `scripts/run_gmstep_controls.py`: runs the head's own `gmstep_mutants.py` controls by index plus the reviewer control, through the head's runner functions.
  - `scripts/milan_dp_window.py`: read-only hosted timing.
  - `scripts/nolpf_leg.mk`: a side makefile for the `obj_nolpf` recipe.
- **Receipts.**
  - `receipts/`: the leg logs, the control logs, the property summary and head runs, hosted windows and check runs, scope checks, docs gates, lint, tool identity and review-clone integrity.
  - The issue and PR JSON exactly as read.
  - Host paths are redacted (`$HOME`, `$DATA`, `$PACKET`, `$CLONE`, `$PINNED_BIN`, `$VERILATOR_IMAGE`).

## Real limits

- **Not run here:**
  - the full `milan_dp` default sweep, which exceeds one foreground command (the exact-head hosted shard 4/5 ran it: 9781 checks, 0 failures);
  - the full builder, parent, PP and gPTP banks;
  - Yosys, xvlog, behave and `run_all_suites.sh`;
  - act.

  Instead I ran gmstep, the three `sim_main` legs, tkdiag with its arm, all eleven gmstep controls plus one reviewer control, lint and the docs gates. The builder gate 1b resolution rests on the diff and the exact-head hosted `elaborate` and `docs-check` successes.
- **Probe model limits.** The property probe runs the engine alone with a modelled packetizer (latch at launch, 0-3 cycle report latency, one report per cycle). It does not run the datapath's feed mux or the talkers.
- **Standards text.** Standards clauses were read as quoted in the tree and the decisions, not from the standards documents.
- **F1 sample size.** F1 rests on one hosted sample at the head, set against the spread of ten dev and PR samples. It is not a distribution.
- **Not claimed.** Physical calibration and the #117 two-board handover (acceptance 4) were NOT RUN and are not claimed. Field skips are not hardware proof.
- **Clone integrity.** The review clone is byte-exact at the head (`receipts/review_clone_integrity.txt`):
  - HEAD `a21cd358`, and `write-tree` equals the head tree `5376deee`;
  - empty `status --ignored`;
  - no assume-unchanged or skip-worktree flags;
  - 883 tracked entries with 0 byte or mode mismatches;
  - gitlinks `gptp-processor` e5dcea6e, `protocol-processor` 09f9bf38 and `third_party/verilog-axis` 48ff7a7e checked out clean at their pins, with `external` uninitialised as at the start.

  Every build and probe ran in a copy under the unpublished scratch directory. Verilator 5.050 rev v5.050 was used, with at most 8 jobs (`receipts/tool_identity.txt`).

## Pending manager duties

- Decide F1 under 5819379503 item 2 on the exact-head figure (2459.9 s, 8.9%).
- Obtain the F2 docs correction, then re-review the corrected head.
- Build and validate the final current-dev candidate: source base `57456af9`, live dev `573f0052`.
- Own the hosted and act acceptance.
- Run the #117 bench step (acceptance 4) after merge.

R276-5 FINISHED
