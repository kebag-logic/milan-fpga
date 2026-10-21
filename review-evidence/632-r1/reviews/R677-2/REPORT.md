[R677] NEGATIVE - exact head 2ff30f0dc5e89be46f8103272883885e8553f4b8

# R677-2: internal cleared-context review of PR #770, round 2 (Relates to #632, #764)

- Head `2ff30f0dc5e89be46f8103272883885e8553f4b8`, tree `2a2cc5362850cee5a857d7d277d8e8ec3aaeae7a`. The round-2 delta is the twelve commits `f1fda3f1..2ff30f0d`. The PR source base is `e26f1816`. Dev `78ca9bdf` / `59740e3c` is not merged.
- **Verdict: NEGATIVE.** One MAJOR and two MINOR findings are open.
  - **R677-2-F1 (MAJOR).** The whole-period offset fix changed which value GET_STREAM_INFO word 3 returns. The processor also reads that word to decide whether SET_STREAM_INFO changed anything. The result, measured on the real datapath and processor:
    - repeating an identical SET now sends an unsolicited notification;
    - a SET that changes both the stored and the applied offset sends none.
  - **R677-2-F2 (MINOR, Tests).** The tracking reference is meant to restart at a hold. Removing that restart brings back the round-1 cancellation after an event, and every case still passes.
  - **R677-2-F3 (MINOR, Docs).** Two figures in the PR body are stale.
- Every other round-2 item checks out at its cause. That covers R678-1-F2 (timestamps), F3 (RTL), F4 and R1, and R677-1-F1 to F5.
- Five RESIDUE items and four SUGGESTIONs are listed for one-pass absorption.
- Scope: as ruled in issuecomment-6306187740, R678-1-F1 (listener presentation at the pin) is out of this PR. It is not counted as a finding. Only the required scope statement was checked; see R677-2-R3 to R5.

## Reconstruction (public state only)

- **Workflow.** AGENTS.md, CONTRIBUTING.md and docs/README.md.
- **Assignments and rulings.** The round-2 assignment (issuecomment-6300015619) and the scope ruling (issuecomment-6306187740). The PR body as it stands (`receipts/pr_body_snapshot.txt`).
- **Requirements.**
  - IEEE 1722-2016 4.3.5 and 10.7/10.8, Equations (14) and (15).
  - Milan v1.2 7.6.1 (frequency and phase).
  - Milan v1.2 5.4.2.9 (the SET_STREAM_INFO response echoes the command) and 5.4.5 (unsolicited notifications). This repository's `[NOTIFY]` bench grades 5.4.5.2 as "a SET of the value already held ... pushes NOTHING".
- **Delta read in full.**
  - `KL_mmcm_drp_servo.sv`: tracking unwrap, re-fold, all-samples settle, snapshot hold.
  - `KL_mtt_round.sv` (new), plus the `KL_crf_tx` `ROUND_MTT_P` split.
  - `milan_datapath.sv`: the rounder binding, the GET_STREAM_INFO word, the blend close slot.
  - `KL_aaf_capture_i2s.sv` and `aaf_talker_i2s.sv`: the pop-edge fix.
  - `KL_chan_map_capture.sv` (`TDM_CLOSE_SLOT_P`) and `KL_media_if_latency_pkg.sv` (`close_slot`, `close_is_i2s`).
  - The `media_phase` harnesses (det, ofs, blend, pins, loop), `phase_mutants.py`, the `milan_dp` nxn offset leg, and the docs and tooling lists.
- **Consumers outside the diff.** The processor's SET_STREAM_INFO program: `protocol-processor/hdl/aecp/ucode/gen_ucode.py:2242-2294` and `KL_aecp_engine.sv:3600`.
- **Published evidence spot-checked** (`review-evidence/632-r1/author-r2/receipts/round2` at `65768509`):
  - the sweep at `2ff30f0d`, all four shards `rc=0`: 15/15, 16/16, 17/17 and 16/16, with check totals matching the PR body;
  - the `milan_dp` #632 extract: 2,010,000 ns reads back as 2,020,834 ns and is stamped by AAF output 1 and the CRF output;
  - route-1x1 at `f1643214`: `RESULT: PASS`, with the PR table's figures. `f1643214..2ff30f0d` changes only one doc paragraph and one Makefile comment;
  - lint at `2ff30f0d`: `rc=0`;
  - the unwrap equivalence at `f1643214`.
- Prior round-1 findings (R678-1, R677-1) were read only after my own pass over the diff.

## Findings

### R677-2-F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs - SET_STREAM_INFO's change gate now compares the commanded offset with the applied one

- **Where:**
  - `hdl/milan/milan_datapath.sv:5236`. GET_STREAM_INFO word 3 (`gsi_ans_raw_w`, `4'd3`) for an output now serves `aecp_pres_applied_w`, the rounded row. At base `e26f1816` it served `aecp_pres_offset`, the stored row.
  - `protocol-processor/hdl/aecp/ucode/gen_ucode.py:2258`, `:2264-2266`. The SET_STREAM_INFO program gathers that same word as "current presentation offset" (`GATHER_EXT rd=6 GSI(3)`). It compares the commanded value with it (`COMPARE ra=12 rb=6`) and calls `NOTIFY_ENQ` only when they differ.
  - The notification body (`E_SINFOUNS`, `gen_ucode.py:2307-2330`) and the solicited response (the echo that Milan 5.4.2.9 requires) both carry the stored value as set.
  - The docs claim "what a controller reads is what every output stamps": `docs/design/MEDIA_CLOCK_FOLLOWING.md:1674-1677` and `hdl/ieee1722/crf/KL_mtt_round.sv:33-35`.
- **Authority:**
  - Milan v1.2 5.4.5 (and 5.4.5.2 as this repository grades it, `tb/verilator/milan_dp/sim_nxn.cpp:1396-1399`): a command that modifies state notifies the other registered controllers, and one that modifies nothing pushes nothing.
  - The R678-1-F2 required outcome: "preserving coherent control-plane readback". The round-2 assignment: "GET_STREAM_INFO reports the applied offset, so readback stays coherent".
  - AGENTS.md section 5: preserve documented module and interface contracts.
- **Evidence.** This was executed on the real `milan_datapath` and processor through the focused `milan_dp` notify leg (1x1 shape). A disposable probe was inserted after the `[NOTIFY]` section registered controllers A and B. Script: `scripts/sinfo_notify_probe.py`. Receipt: `receipts/probe_milan_dp_notify_sinfo.log`.

  | Step | SET from A | Notifications to B | GET reads | Expected |
  |---|---|---|---|---|
  | 1 | 2,000,000 ns (held) | 0 | 2,000,000 | 0 |
  | 2 | 2,010,000 ns | 1 | 2,020,834 | 1 |
  | 3 | 2,010,000 ns again (nothing modified) | **1** | 2,020,834 | 0 |
  | 4 | 2,020,834 ns, the value GET returned | **0** | **2,041,667** | 1 |

  - In step 4 the stored offset moves from 2,010,000 to 2,020,834 and the applied offset moves from 97 to 98 periods. Controller B is not told; the last notification it holds says 2,010,000.
  - The leg's third failure, `[NOTIFY] ...reaches B with sequence_id 1 ... got=0x4`, is an artifact of the probe's extra pushes, not a separate defect.
- **Impact:**
  - A controller that writes back a value it read loses coherence with every other registered controller. The PR's own text names this write-back, and the change is real (one period more).
  - A repeated identical SET spams the other controllers.
  - Both cases are reachable by any controller with any offset that is not a whole number of periods (the SET range is 0 to 0x7FFFFFFF).
  - The interface contract between the datapath's GET_STREAM_INFO face and the processor changed without that consumer being updated.
  - No test covers notifications with a rounded offset.
- **Required outcome:**
  - SET_STREAM_INFO's notification decision is taken against a like-for-like current value. An identical SET pushes nothing. A SET that changes the stored offset, or the applied offset, pushes exactly once.
  - The relationship between the SET response or notification (the commanded value, per 5.4.2.9) and GET_STREAM_INFO (the applied value) is documented, and the "what a controller reads" claim is scoped to match.
  - If the fix needs the processor submodule or a design choice, publish it as a decision rather than leaving the gate as is.
- **Verification:** a `milan_dp` `[NOTIFY]`-section case with the four steps above, plus a planted defect restoring the present gate that fails it.

### R677-2-F2 - MINOR - Tests - the tracking reference's restart at a hold is claimed but no check kills its removal

- **Where:**
  - `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:901` (`ph_ref_v_r <= 1'b0;` in the hold).
  - The banner at `:93-96`.
  - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1610-1611` ("restarts the tracking reference").
- **Authority:**
  - R678-1-F3 and the round-2 ruling ask for a circular aggregate that does not cancel across +/-Ps/2, plus closed-loop engagements near +/-Ps/2 with quantization and jitter.
  - AGENTS.md section 6, Tests: each claimed behaviour has a test that can fail.
- **Evidence:**
  - Planted probe `hold_keeps_ref` (`ph_ref_v_r` kept across the hold) passes:
    - all ten `det` cases (`receipts/probe_p2det.log`);
    - all thirteen loop cases (`receipts/probe_p2loop.log` and `receipts/probe_p2loop2.log`).
  - A disposable detector case `afterhold` (`scripts/det_afterhold_probe.py`) runs these steps:
    1. settle on +/-100 ns;
    2. raise an mr hold;
    3. feed the reviewer's balanced +/-10,416 ns population from the hold onwards.
  - Results of `afterhold`:
    - Clean RTL: theta -31,250, the half-period phase (`receipts/probe_afterhold_clean.log`).
    - With the probe: theta **0** (`receipts/probe_afterhold_p2.log`). The round-1 cancellation returns for any event that lands the phase on the fold.
  - The closed-loop `edge` and `edge2` cases re-engage at -0.4912 and -0.4913 Ps. That is about 180 ns from the fold, against +/-48 ns of jitter and 8 ns of truncation, so no closed-loop sample ever straddles the fold.
  - The other new reference behaviour is graded: freezing the reference at the era's first sample (`ref_not_tracked`) fails `edge` and `edge2` at "the servo reports settled at the end" (`receipts/probe_p1loop.log`).
- **Impact:** a regression that drops the restart passes the suite and its campaign. With it, the half-period pull after a hold becomes the cancelling mean that round 1 found. The all-samples settle predicate still keeps settled low, so the impact is a stall at the fold, not a false settled.
- **Required outcome:**
  - A check in which a hold is followed by samples straddling +/-Ps/2 while the pre-hold reference sat elsewhere, requiring the half-period reading and the slew-limited pull.
  - A planted defect removing the restart that fails it.
  - Optionally, a closed-loop engagement whose samples do straddle the fold.
- **Verification:** `make -C tb/verilator/media_phase mutants` kills the new defect at its named check.

### R677-2-F3 - MINOR - Docs - PR body figures are stale

- **Where and evidence:**
  - PR body, "The decision R678-1-F1 needs": "against 469 LUTs and 20 slices of route-1x1 headroom". The round-1 route at `a6ae20f9` left that headroom. The route this PR records at `f1643214` leaves 404 LUTs and 8 slices: 49,709 of 50,113 and 15,797 of 15,805. `MEDIA_CLOCK_FOLLOWING.md:1760` and the ruling both say 404.
  - PR body, "How to validate", expected result 2: "all twenty-seven planted defects". The campaign has 28 defects, and the measured table in the same body says 28 of 28 (`receipts/media_phase_mutants_head.log`: 28 killed, 46 checks, 0 failures).
- **Impact:** the figures a reader uses for the area decision and for the campaign bar disagree with the evidence. These are measurement figures, so they are not RESIDUE.
- **Required outcome and verification:** the PR body reads 404 LUTs and 8 slices, and twenty-eight.

### RESIDUE (wording only, carried to the residue checklist)

**R677-2-R1 - Docs - comment rule.** Twenty-one new source comments in the delta show review-finding IDs (reviewer ID and round). Remove the `R67x-1-Fn` token and keep the issue ID and behaviour.

- `hdl/ieee1722/aaf/KL_aaf_capture_i2s.sv:141`
- `hdl/ieee1722/crf/KL_mtt_round.sv:14`
- `hdl/milan/milan_datapath.sv:1245`, `:3430`
- `tb/verilator/media_phase/Makefile:92`, `:106`
- `tb/verilator/media_phase/blend_wrap.sv:4`
- `tb/verilator/media_phase/ofs_wrap.sv:5`
- `tb/verilator/media_phase/phase_mutants.py:94`, `:107`, `:113`, `:118`, `:124`, `:157`, `:162`, `:179`, `:187`
- `tb/verilator/media_phase/sim_blend.cpp:4`, `:15`
- `tb/verilator/media_phase/sim_ofs.cpp:5`
- `tb/verilator/milan_dp/sim_nxn.cpp:7217`

Exact fix: `(#632, R677-1-F1)` becomes `(#632)`; `R678-1-F3:` is deleted from the `#:` lines; at `sim_blend.cpp:15`, "as before #632's R677-1-F1" becomes "as before this fix (#632)".

**R677-2-R2 - Docs - `hdl/milan/milan_datapath.sv:3419-3421`.** The comment says GET_STREAM_INFO "serves these same entries", but it now serves the applied rows. Exact fix: "This fold is the ONE derivation point of the rows as set; GET_STREAM_INFO's latency word and every output serve them as applied (pres_round below), so the wire and the answer cannot disagree."

**R677-2-R3 - Docs - `docs/design/MEDIA_CLOCK_FOLLOWING.md:1721`, `:1751-1754`.** This is the ruling's required scope statement, which the head predates. Exact fix: retitle the section "The listener: not compensated, out of this PR (#632)". Replace "Round 2 ruled the compensation in ... published with the hand-off," with: "Presenting each sample at the pin was taken out of PR #770 ([ruling](https://github.com/kebag-logic/milan-fpga/pull/770#issuecomment-6306187740)) and stays open under #632; it needs an owner area or RAMB budget. The listener keeps the #386 law at the crossbar grid, and its post-grid delays stay the documented constants of [TIME_SYNC.md](TIME_SYNC.md#listener-render-latency). The costs that decision weighs:"

**R677-2-R4 - Docs - `docs/design/TIME_SYNC.md:519-523`.** Exact fix: replace "Timestamp presentation is ruled in (R678-1-F1). A decision is pending: its queue exceeds route-1x1's gates." with "Timestamp presentation is out of PR #770 and open under #632, pending an owner area decision; the listener keeps the fill law above at the crossbar grid."

**R677-2-R5 - Docs - PR body.**
- Exact fix for Status: "R678-1-F1 (the listener at the pin) is out of this PR by the [A10] ruling (issuecomment-6306187740) and stays open under #632; the listener keeps the #386 law at the crossbar grid, its post-grid delays the documented constants of TIME_SYNC.md."
- Make the same change to "Linked Issue / roles", the first Known-limitations bullet and the DoD first item ("the listener item is out of scope by ruling").

### SUGGESTIONS (optional)

- **S1.** `hdl/milan/milan_datapath.sv:6460`: the listener monitor's EARLY threshold still reads row 0 as set (`aecp_pres_offset`), so it is up to one period off the applied offset. It is diagnostic only. Consider the applied row.
- **S2.** `KL_mtt_round` maps a row at or above 4,294,958,334 ns modulo 2^32 (0xFFFFFFFF applies as 11,871 ns). A controller cannot reach this, because `KL_aecp_engine.sv:3600` refuses bit 31. Only a factory row could, so consider an elaboration guard on `RESET_NS_P` rows at or above 2^31.
- **S3.** `KL_mmcm_drp_servo.sv:853-856`: a sample whose fold completes on a window's closing cycle is unwrapped against the outgoing reference. This is documented and negligible, at most Ps/256 in one window and only at the fold.
- **S4 (R677-1-F6 retained, unchanged).** `milan_datapath.sv:6110-6111` still passes the data-delay `1` as a literal beside the instantiations.

## Prior findings at this head

| Prior | Status at `2ff30f0d` | Evidence |
|---|---|---|
| R677-1-F1 blend constants and pin grade | Resolved | Close slot and I2S latency in `close_slot()`/`close_is_i2s()`; the I2S pop-edge alias in both front ends; `media_phase` blend 24 checks pass; `blend_closed_on_tdm_pair` and `i2s_pair_one_pop_late` killed; `pin_wrap.sv:4-8` premise corrected |
| R677-1-F2 PHC step hold | Resolved | `phcstep` 16 checks pass; `step_hold_removed` killed at "[phcstep] the phase term let go at the PHC step" |
| R677-1-F3 settled timing and fold range | Resolved | `settled_is_engaged` killed (det:inband), `fold_range_guard_removed` killed (det:range); every loop case grades "settled never read 1 with the true phase outside the band" and the `MCSRV_STAT[9]` mirror |
| R677-1-F4 budget basis | Resolved | `CI_WORKFLOWS.md:432`, `run_all_suites.sh:250` and the Makefile agree at 578 s, three case jobs (author receipt `media_phase_suite/wall.txt`). My run: 417 s at eight jobs |
| R677-1-F5 divider texts | Resolved | `milan_datapath.sv`, `endstation_builder.py:4748`, `test_builder.py:21628` |
| R678-1-F1 | Out of scope by ruling; not counted | Scope wording: R677-2-R3 to R5 |
| R678-1-F2 non-period offsets | Resolved for timestamps and GET readback. Its "coherent control-plane readback" outcome is not met for notifications: **R677-2-F1** | `ofs` 15 checks over four AAF outputs, the CRF output and boundary rows, reset and run time; `offset_rounding_bypassed` and `crf_row_raw` killed; my probe `mtt_pass2_floor` (floor in pass 2) caught at "every row reads back as applied" (`receipts/probe_p4.log`); `milan_dp` reads 2,020,834 at the head |
| R678-1-F3 circular aggregation | Resolved in RTL and in the detector cases. One test gap: **R677-2-F2** | Exhaustive arithmetic check of the unwrap and re-fold over every reference and sample, 0 violations (`receipts/unwrap_spec_check.txt`); det balanced, unbal129, unbal160, jitter, meanin and cross pass; `tracking_fold_removed`, `window_refold_removed` and `settled_on_mean_only` killed; `edge`/`edge2` closed loop pass (26.4 s and 26.6 s, 619 ns and 599 ns, as documented) |
| R678-1-F4 hold on the snapshot edge | Resolved | `KL_mmcm_drp_servo.sv:1023`; det snap 18 checks (each hold on, before and after the edge, with the committed contribution graded); `snapshot_hold_ignored` killed; comment corrected |
| R678-1-R1 | Resolved | PR body lists `[R677]` and `[R678]` |

The other named items:

- **28 planted defects:** each fails its named check (`receipts/media_phase_mutants_head.log`: 18 clean controls, then 28 of 28 killed, 46 checks, 0 failures, 674 s at eight jobs).
- **route-1x1 within the gate:** at `f1643214` (RTL identical to the head): LUT +96 of +500, FF +407 of +600, slice +72 of +80, RAMB +0, DSP -1, WNS +0.305 ns, WHS +0.036 ns, route complete, `RESULT: PASS`.

## Per-lens results

| Lens | Result | Artifact examined at `2ff30f0d` |
|---|---|---|
| Conformance | UNCLEAN (F1) | Eq. (14)/(15) and 4.3.5 against `KL_mtt_round.sv`, `KL_crf_tx.sv` `g_applied`, `milan_datapath.sv:3430-3458` and `:5236`, and the `ofs`, pins and blend grades. Milan 5.4.5 against `gen_ucode.py:2254-2268` and `receipts/probe_milan_dp_notify_sinfo.log` (fails). Milan 7.6.1 against the servo phase path and the closed-loop cases |
| RTL | UNCLEAN (F1) | Widths, signedness and guards of the unwrap and re-fold (`KL_mmcm_drp_servo.sv:780-812`, exhaustive check clean). The snapshot hold `:1023`. `KL_mtt_round.sv` divider sizing, two-pass numerators, row walk and reset rows. `KL_crf_tx` `ROUND_MTT_P` split. `KL_chan_map_capture` `TDM_CLOSE_SLOT_P` and its guard. The I2S alias timing (data stable from the valid cycle until the next ren). Interface contract of GET_STREAM_INFO word 3 against its processor consumer (fails, F1) |
| Robustness | UNCLEAN (F1) | Repeated identical SET and write-back of a read value (F1). Holds on, before and after the closing edge (det snap). Fold range +/-2^25 (det range). Window cap (burst). Rows at 0, 1, boundary and 0xFFFFFFFF at reset and at run time (ofs). Six reset phases (blend) |
| Tests | UNCLEAN (F1, F2) | `media_phase` default target at head (26 tallies, 291 checks, 0 failures). The mutants campaign (28 of 28). Probes: `ref_not_tracked` caught, `hold_keeps_ref` survives everything (F2), `mtt_pass2_floor` caught. No notification test with a rounded offset (F1) |
| Docs | UNCLEAN (F1, F3) | `MEDIA_CLOCK_FOLLOWING.md` Phase alignment (`:1572-1820`), `TIME_SYNC.md:202-203` and `:519-523`, `REGISTER_MAP.md` 0x8F8, `MILAN_COMPLIANCE_MATRIX.md` 4.3.5/10.8, `TESTING.md`, `CI_WORKFLOWS.md`, CHANGELOG and the PR body. Docs gates at the head: `docs_check` 0 findings over 210 md files, style OK (`receipts/docs_check_head.log`, `receipts/check_doc_style_head.log`). RESIDUE R1 to R5 do not unclean the lens; F1 and F3 do |

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | as in the table above; F1 open | R677-2 | `2ff30f0dc5e89be46f8103272883885e8553f4b8` |
| RTL | UNCLEAN | as above; F1 open | R677-2 | `2ff30f0dc5e89be46f8103272883885e8553f4b8` |
| Robustness | UNCLEAN | as above; F1 open | R677-2 | `2ff30f0dc5e89be46f8103272883885e8553f4b8` |
| Tests | UNCLEAN | as above; F1 and F2 open | R677-2 | `2ff30f0dc5e89be46f8103272883885e8553f4b8` |
| Docs | UNCLEAN | as above; F1 and F3 open | R677-2 | `2ff30f0dc5e89be46f8103272883885e8553f4b8` |

No lens is covered clean at this head. The fix of F1 touches the GET_STREAM_INFO and processor interface, so every lens must be re-applied at the corrected head.

## Real limits of this round

- **No manager source bank** runs at this head. Source-head execution evidence is the author's published receipts plus my focused runs below. This is not a full sweep, builder, Yosys or route run.
- **My runs used the pinned simulator 5.050** (identity checked) on a shared, heavily loaded host. Wall times are indicative only.
  - The `media_phase` default target: 417 s at eight case jobs, rc 0.
  - The mutants campaign: 674 s at eight jobs, rc 0.
  - Detector and loop probes.
  - One focused `milan_dp` notify build with a disposable probe. That leg's verdict (3 failures) is the probe's, not a statement on the unmodified suite.
- **R677-2-F1's evidence is the 1x1 shape on output 0.** The gate is shape-independent microcode, and other shapes were not run.
- **The rounder's wrap** above 2^32 is only reachable through a factory row; it was not exercised beyond the author's `ofs` case D.
- **Physical calibration and the bench proof** (the #764 method) were NOT RUN. Simulation is not hardware proof.
- **Hosted contexts at the head** were mostly queued or in progress when snapshotted (`receipts/hosted_checks_snapshot.tsv`): `changes`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability` and `full-ci-gate` succeeded, and "Physical gPTP" was skipped. No hosted acceptance is claimed.
- **Composition with live dev** `59740e3c` was not built here.

## Pending manager and owner duties

- Rule how R677-2-F1 is to be fixed (datapath, processor submodule or both), and re-review the corrected head on all five lenses.
- Carry R677-2-R1 to R5 to the residue checklist.
- The route-1x1 gate reported "re-baseline recommended" for DSP -1. Headroom left at `f1643214`: LUT 404, FF 193, slice 8. Any F1 fix that adds logic must be re-routed against it.
- Build the current-dev merge candidate at the merge turn (builder and native banks), and own hosted/act acceptance at the exact head.
- The owner's area or RAMB decision for R678-1-F1, under #632.
- The bench proof after merge.

## Receipts and scripts (each listed in MANIFEST.sha256)

- `receipts/media_phase_default_head.{log,rc,wall}`: the default target at the head.
- `receipts/media_phase_mutants_head.{log,rc,wall}`: the campaign at the head.
- `receipts/unwrap_spec_check.txt`, from `scripts/unwrap_spec_check.py`: an exhaustive model of the unwrap and re-fold at RTL widths.
- `receipts/probe_p4.{log,rc}`: `mtt_pass2_floor`.
- `receipts/probe_p1det.{log,rc}` and `receipts/probe_p1loop.{log,rc}`: `ref_not_tracked`.
- `receipts/probe_p2det.{log,rc}`, `receipts/probe_p2loop.{log,rc}` and `receipts/probe_p2loop2.{log,rc}`: `hold_keeps_ref`.
- `receipts/probe_afterhold_{clean,p2}.{log,rc}`, from `scripts/det_afterhold_probe.py`.
- `receipts/probe_milan_dp_notify_sinfo.{log,rc}`, from `scripts/sinfo_notify_probe.py`.
- `scripts/probe.py`: the disposable single-substitution driver. Its own exit status is always 0; the make rc is in each log.
- `receipts/docs_check_head.{log,rc}` and `receipts/check_doc_style_head.{log,rc}`.
- `receipts/hosted_checks_snapshot.tsv` and `receipts/pr_body_snapshot.txt`.
- `receipts/clone_restore_check.txt`: the review clone at exact head bytes. The index blob IDs and modes equal the HEAD tree, the worktree has no untracked or ignored entries, and every initialised submodule sits on its gitlink and is clean.

R677-2 FINISHED
