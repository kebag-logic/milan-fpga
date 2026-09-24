[R303] POSITIVE - exact head 0c61d458941088f3847513b7c6fe6589c75b4270

Round R303-3 is the external review of PR #554 (issue #546), done in a cleared context. Head `0c61d458941088f3847513b7c6fe6589c75b4270`, tree `88a5ce9545a23561beae21d3e0323a9d1fb0d051`, source base `57456af96b3127b9d309a995bbbd35a6113ce52d`. All five lenses were applied at this head. Receipts are listed in `MANIFEST.sha256`, and the exact commands are in `receipts/COMMANDS.txt`.

## Summary

Round 3 closes the one open item from round 2, and it takes both round-2 suggestions.

- **Citation fixed (R303-2-F1 = R302-2-F1).** The derivation of the 2048 ns jump threshold now cites clauses that state what they are cited for:
  - IEEE 802.1AS Annex B.1.1 for the +/-100 ppm LocalClock bound. This bound is stated as an assumption for the media oscillator.
  - Milan v1.2 Section 7.4 for the better-than +/-50 ppm media-source bound. The 100 ppm figure is kept as conservative margin.
  - The false claim that "no independent media-clock clause" exists is gone.
  - The RTL comment, `TIME_SYNC.md` and the PR body agree.
- **RTL unchanged.** The round-3 RTL delta is comments only. After preprocessing, with comments stripped and whitespace normalised, both modules are byte-identical to `d04a61678`. The servo blob is identical. Both revisions elaborate `RATE_DRIFT_NS_C` = 601 and `TS_JUMP_NS_C` = 2048 ns.
- **Resume check added (R303-2 S1).** U13 now fails a servo that never resumes PI:
  - The committed `servo_never_resumes` mutant is killed in the default campaign by `[U13] valid offset resumes PI trim`.
  - Two independent reviewer variants are also killed: a resume delayed 84 ms, and a loop whose lock count runs while its trim and integrator stay frozen.
  - Under the round-2 harness the same mutant passes. So the new check is what catches it.
- **Disposition text fixed (R303-2 S2 = R302-2 S1).** The evidence-gate disposition now names the servo read and the ignored-validity and PI-resume defects. The gate passes.
- **Round-2 probes unchanged.** I re-ran every round-2 probe as it was. Every verdict line matches round 2. The only difference is that the committed campaign now reports 8 controls instead of 7.

No BLOCKER, MAJOR or MINOR finding is open. Every lens is covered clean at this head.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### R303-3-S1 - SUGGESTION - Docs - the PR body's Status section still describes the pre-publication state

- Artifact: the PR #554 body, section "Status": "Round 3 is committed locally at `0c61d458...`. ... Publication and independent re-review remain pending."
- Evidence: the head is published, and the hosted exact-head checks are complete (`receipts/hosted_check_runs.tsv`).
- Impact: none on correctness. A cold reader of the PR sees a stale lifecycle line.
- Optional outcome: refresh the Status line when the manager next edits the body.
- Verification: text inspection.

## Verification of the round-3 assignment

| Item (assignment, issue 546 comment 5820794596) | Result at this head | Evidence |
|---|---|---|
| `KL_crf_rx.sv` comment cites IEEE 802.1AS Annex B.1.1 (100 ppm LocalClock, assumed for the media oscillator) and Milan v1.2 Section 7.4 (50 ppm, 100 ppm as margin) | Met | `hdl/ieee1722/crf/KL_crf_rx.sv:274-277`; `receipts/authority_excerpts.txt` (802.1AS-2011/2020 B.1.1 "within +/-100 ppm"; Milan v1.2 7.4 "better than +/-50PPM"; Milan B.1.1 is the tu 0.25 s rule) |
| `TIME_SYNC.md` says the same | Met | `docs/design/TIME_SYNC.md:191-201` |
| PR body says the same | Met | PR #554 body, Description, paragraph 2 |
| The "rather than an independent media-clock clause" claim is removed | Met | `git grep` finds no "independent media-clock" in the tree; the PR body mentions it only to record its removal |
| Comment-free RTL identical to `d04a6167` | Met | `receipts/rtl_round3_comment_only.txt`: only `hdl/ieee1722/crf/KL_crf_rx.sv` changed under `hdl/`, and only in comments. Both preprocessed streams match (`1d8c8930...` receiver, `2ed1d115...` servo). Servo blob `12eaa99c` at both. No gitlink moved |
| `TS_JUMP_NS_C` still 2048 ns | Met | `receipts/elab_params.txt`: both revisions give 601 / 2048 |
| R303-2 S1: U13 fails a servo that never resumes PI; `servo_never_resumes` killed in the default campaign | Met | `receipts/crf_rx_default.log:1981-1982`; `receipts/r3_probe_batch1.txt` (S1-S4); `receipts/r3_probe_batch2.txt` (S5) |
| R303-2 S2: `measure_test_evidence.py` disposition text | Met | `scripts/measure_test_evidence.py:597-600`; `receipts/measure_test_evidence_check.log:117,138` |

## Lens results

- `[R303] PASS Conformance - hdl/ieee1722/crf/KL_crf_rx.sv:274-289,385-398; docs/design/TIME_SYNC.md:147,167-215; receipts/authority_excerpts.txt; receipts/crf_rx_default.log:1891-1967; receipts/threshold_sensitivity.txt`. Checked against issue #546 acceptance 1-3, IEEE 1722-2016 4.4.4.7 and 10.4.5 (tu), Milan v1.2 Annex B.1.1 (the tu hold), Milan v1.2 Section 7.4 and IEEE 802.1AS Annex B.1.1:
  - **Acceptance 1.** A rate sample that spans a talker discontinuity is discarded on either tu edge, an unmarked step or a sequence gap. The failing arms are in the default gate: `tu_ignored`, `jump_removed`, `refill_short` and `accept_edge_late` are all rejected by name.
  - **Acceptance 2.** Steps of +/-150 us at both ends keep every observed clock LOCKED, with zero receiver unlocks (`both_short_*`, `both_long_*`: state 4). The integrator stays within 30.703..30.723 ppm.
  - **Acceptance 3.** At this head my focused gates are green: receiver, servo, evidence and documentation. Hosted exact-head `rtl-fast`, `verilator-suites` and `yosys-portability` all succeeded. The full banks and the candidate merge belong to the manager.
  - **Citations.** Every clause now states what it is cited for. The threshold is 2048 ns under either media bound.
- `[R303] PASS RTL - hdl/ieee1722/crf/KL_crf_rx.sv:329-332,385-398,446-447,517-522,543-549,590-601,614-618; hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:254,567-574; hdl/milan/milan_datapath.sv:1725,5448,5488,5532,5547; receipts/rtl_round3_comment_only.txt; receipts/elab_params.txt`. Checked against the servo sampling contract and the receiver's reset, bind, STOP and silence rules:
  - **No clock crossing.** Receiver and servo both run on `axis_clk` (`milan_datapath.sv:5448,5532`), so validity needs no CDC.
  - **Widths.** Spacing uses 64 bits, which catches both signs without a 2^32 alias.
  - **Refill.** Refill is exactly 256 intervals: the event PDU seeds `hfill_r = 1`, and the 257th timestamp publishes.
  - **Reset and invalidation.** All four new registers reset. Silence, bind rise and STOP invalidate. A pending publication is cancelled by a same-cycle break.
  - **Servo gate.** The servo gates only `pp_run_r`, so lock state and the local guards are untouched.
  - **Round-3 delta.** Comments only, verified by preprocessing. The constants elaborate unchanged.
  - **Round-1 RTL mutants.** D1-D10 were re-run at this head and all are killed again (`receipts/r1_campaign_batch4.txt`, `receipts/r1_campaign_batch5.txt`).
- `[R303] PASS Robustness - probes/probe_talker.cpp (receipts/r1_campaign_batch1.txt clean_probe); probes/probe_gm_order.cpp (receipts/r1_campaign_batch6.txt, receipts/r1_campaign_batch7.txt); tb/verilator/crf_rx/sim_discontinuity.cpp via receipts/r1_campaign_batch4.txt, receipts/r1_campaign_batch5.txt, receipts/r2_probe_batch3.txt N5`. Checked against false-positive, recovery, ordering and malformed-input behaviour:
  - **Jitter.** +/-500 ns timestamp jitter gives 0 invalid clocks. +/-1200 ns, outside the derived envelope, holds validity low while the servo stays LOCKED with a frozen integrator. That is the documented choice. Discard telemetry was moved to #495 by manager decision.
  - **Recovery.** A tu pulse with no step recovers with the integrator within 0.020 ppm.
  - **Ordering.** A listener-first GM change stays LOCKED, and the jump, detector and servo-validity mutants fail it.
  - **Malformed and edge input.** Sequence gaps, duplicates, STOP, silence, rebind and back-to-back markers are covered by named checks.
  - **PI resume.** The servo resumes PI after invalidity within 24 ms (`receipts/r3_probe_batch1.txt` S0: trim +240 units against the 80 required).
- `[R303] PASS Tests - tb/verilator/mmcm_servo/sim_main.cpp:29,585-609; tb/verilator/crf_rx/mutants.py:19-116; tb/verilator/crf_rx/Makefile:53; tb/verilator/crf_rx/sim_talker_step.cpp (receipts/crf_rx_default.log); receipts/r3_probe_batch1.txt; receipts/r3_probe_batch2.txt; receipts/r2_probe_rerun_compare.txt`. Checked against the rule that each test can fail for the defect it claims:
  - **The new resume check fails the right servos.** It fails the committed latched-off servo (S1). It also fails a resume delayed 84 ms (S2), and a servo whose trim and integrator writeback stay frozen while its lock count runs (S3).
  - **The check is load-bearing.** Under the round-2 U13 the latched-off mutant passes (S4: 82 checks, 0 failures).
  - **The campaign fails closed.** A no-op resume mutant makes the campaign fail, and the sweep verdict reader then returns 1 (S5).
  - **Default gates.** crf_rx gives 13,836 unit, 1,658 discontinuity and 69 connected checks, and all 8 campaign controls pass. mmcm_servo gives 85 unit, 8 rails and 113 PHC-step checks. Both logs pass the sweep verdict reader with rc 0.
  - **Round-2 probes.** All 23 round-1 cases and all 10 round-2 addendum cases give the same verdicts as at `d04a61678`.
- `[R303] PASS Docs - hdl/ieee1722/crf/KL_crf_rx.sv:274-284; docs/design/TIME_SYNC.md:147,167-231; docs/design/GM_LOSS_RECOVERY.md:152,154,213-214; docs/reference/REGISTER_MAP.md:838; docs/testing/TESTING.md:462; scripts/measure_test_evidence.py:597-600; hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:76-80; PR #554 body; receipts/doc_gates.log`. Checked against the clause texts and the behaviour executed above:
  - **Agreement.** The citations agree in the RTL, the design page and the PR body. `CRF_RATE`'s hold-last-clean behaviour is documented. The test-suite and evidence-gate descriptions match the committed campaign.
  - **Gates.** doc style, doc paths, module matrix and docs_check pass.
  - **Em dashes.** No added diff line contains an em dash (the em-dash and TOC gates could not run here; see Limits).
  - **Remaining gap.** Only the non-blocking S1 remains.

## Prior public findings on this PR

| Prior finding | Status at `0c61d458` | Evidence |
|---|---|---|
| R303-2-F1 MINOR (Conformance, Docs) = R302-2-F1 MINOR (Conformance, Docs): media-bound derivation cites a clause that does not state it | **Resolved** | Assignment table above; `receipts/authority_excerpts.txt`; `receipts/rtl_round3_comment_only.txt`; `receipts/elab_params.txt` |
| R303-2 S1 (Tests): U13 resume check cannot fail for a servo that never resumes PI | **Resolved** | `sim_main.cpp:598-608`; `receipts/crf_rx_default.log:1981-1982`; `receipts/r3_probe_batch1.txt` S1-S4 |
| R303-2 S2 (Docs) = R302-2 S1 (Docs): stale evidence-gate disposition | **Resolved** | `scripts/measure_test_evidence.py:597-600`; `receipts/measure_test_evidence_check.log` |
| R302-2 S2 (Tests): the six connected events share one lock, so per-event attribution under a mutant is not independent | **Retained, optional** (SUGGESTION; does not affect coverage) | Unchanged at this head. The gate verdict is still correct: `receipts/r2_cases/N2_jump_removed.log` shows later events failing after the first |
| R302-2 S3 (Tests): receiver mutants run only against the discontinuity harness in the default campaign | **Retained, optional** (SUGGESTION) | Unchanged at this head. Connected-harness rejection is shown by reviewer probes (`receipts/r2_probe_batch1.txt`, `receipts/r2_probe_batch2.txt`), not by a gate |
| R303-1 F1 MAJOR (Tests) = R302-1-F1 MAJOR (Tests, Docs): connected harness cannot fail for the defect | **Resolved** (since round 2; re-verified) | `receipts/r2_probe_batch1.txt` N1 (-115.762 ppm, ACQUIRE), N2/N3 killed, N0 clean, H1 killed |
| R303-1 F2 MINOR = R302-1 S1: 100 ppm term's authority | **Resolved** | As R303-2-F1 above |
| R303-1 F3 MINOR = R302-1 S2: mutation arm in no gate | **Resolved** (since round 2; re-verified) | `Makefile:53`; `receipts/crf_rx_default.log:1969-1983`; `receipts/r2_probe_batch4.txt` M1 |
| R303-1 S1 = R302-1 S4 (Robustness): unbounded invisible hold under LOCKED | **Out of scope by manager decision** | Moved to the #495 telemetry checklist (issue 546 comment 5818237636) |
| R303-1 S2 = R302-1 S5 (Docs): wording | **Resolved** (since round 2) | `GM_LOSS_RECOVERY.md:152`; `REGISTER_MAP.md:838` |
| R302-1 S3 (Docs): servo banner omits the validity skip | **Resolved** (since round 2) | `KL_mmcm_drp_servo.sv:76-80` |

## Reviewer ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_crf_rx.sv:274-289,385-398`; `TIME_SYNC.md:147,167-215`; PR body; Milan v1.2 7.4 and B.1.1, IEEE 802.1AS-2011/2020 B.1.1, IEEE 1722-2016 4.4.4.7/10.4.5; `crf_rx_default.log` connected results | R303-3 | 0c61d458941088f3847513b7c6fe6589c75b4270 |
| RTL | CLEAN | `KL_crf_rx.sv` (new registers, detection, validity, refill, invalidation); `KL_mmcm_drp_servo.sv:254,567-574`; `milan_datapath.sv:1725,5448,5488,5532,5547`; comment-only and elaboration proofs; D1-D10 re-run | R303-3 | 0c61d458941088f3847513b7c6fe6589c75b4270 |
| Robustness | CLEAN (discard telemetry moved to #495 by manager decision) | `probe_talker.cpp` phases B-E; `probe_gm_order.cpp` O0-O4; `sim_discontinuity.cpp` via D1-D10, N5; U13 resume margin (S0) | R303-3 | 0c61d458941088f3847513b7c6fe6589c75b4270 |
| Tests | CLEAN | `sim_main.cpp:585-609`; `mutants.py`; `Makefile:53`; `sim_talker_step.cpp`; default gates; r1/r2/r3 probe campaigns; sweep verdict reader | R303-3 | 0c61d458941088f3847513b7c6fe6589c75b4270 |
| Docs | CLEAN (S1 optional) | `KL_crf_rx.sv:274-284`; `TIME_SYNC.md`; `GM_LOSS_RECOVERY.md`; `REGISTER_MAP.md:838`; `TESTING.md:462`; `measure_test_evidence.py:597-600`; servo banner; PR body; doc gates | R303-3 | 0c61d458941088f3847513b7c6fe6589c75b4270 |

## Executed evidence at this head (reviewer-run)

- `receipts/crf_rx_default.log`, `receipts/crf_rx_default.rc`: `make -C tb/verilator/crf_rx` gives make rc 0 and verdict rc 0.
- `receipts/mmcm_servo_default.log`, `receipts/mmcm_servo_default.rc`: `make -C tb/verilator/mmcm_servo` gives make rc 0 and verdict rc 0.
- `receipts/r1_campaign_batch1..7.txt`: 23 round-1 cases, all as expected. The verdict lines are identical to round 2.
- `receipts/r2_probe_batch1..4.txt`, `receipts/r2_campaign_sweep_reader.txt`: 10 round-2 cases, all as expected. The sweep reader gives rc 0 on M0 and rc 1 on M1.
- `receipts/r2_probe_rerun_compare.txt`: the only difference from round 2 is the campaign's control count, 7 to 8.
- `receipts/probe_artifact.log`: 300 port-low and 0 register-low reads after the edge, unchanged.
- `receipts/r3_probe_batch1.txt`, `receipts/r3_probe_batch2.txt`, `receipts/r3_cases/`: the U13 resume probes S0-S5.
- `receipts/rtl_round3_comment_only.txt`, `receipts/elab_params.txt`, `receipts/authority_excerpts.txt`, `receipts/threshold_sensitivity.txt`.
- `receipts/measure_test_evidence_check.log`: ratchet PASS, rc 0.
- `receipts/doc_gates.log`: see Limits for the two gates that could not judge.
- `receipts/hosted_check_runs.tsv`: 21 executed contexts succeeded. `Physical gPTP (nightly and manual)` was skipped, which is not hardware evidence.
- `receipts/clone_integrity.txt`: the clone is at the exact head and tree. Worktree and index are clean, with no untracked or ignored files. The four gitlinks are unchanged and the submodule worktrees are clean.

## Real limits

- `check_em_dash.py` and `gen_toc.py --check` could not judge here, because the pinned Markdown renderer is not installed and shared installs are not allowed. I substituted an em-dash count over the added diff lines (0). The TOC gate was not run by this reviewer. The manager's round-3 gate results cover both.
- I ran only focused suites: crf_rx, mmcm_servo, evidence and documentation gates. I did not run the full parent, protocol-processor, gPTP, Yosys or builder banks, or the 344 behaviour scenarios, and I ran no act or container job. The linked public evidence tree (`148f1a2e.../review-evidence/546-r1`) holds author and prior-review receipts. I found no manager source-bank receipt for this head in it. The manager's statement that those banks passed at this head is taken as the manager's duty, not as verified here.
- The servo mutants are graded by the servo unit harness only. Connected-harness rejection of receiver defects comes from reviewer probes, not a gate (retained R302-2 S3).
- The 2048 ns threshold assumes the remote talker shares this design's PHC envelope. A talker whose adjacent-timestamp jitter is too large holds validity low, which is the documented choice. The probes bracket that limit: +/-500 ns passes and +/-1200 ns holds. Arithmetic puts the edge between about +/-700 ns and +/-1000 ns, depending on drift.
- Physical calibration was not run, and the field and physical contexts skipped are not hardware proof. Timing closure was not examined: validity is combinational from the accept path into `pp_run_r`, in one clock domain.

## Pending manager duties

- Build and validate the final candidate on live `dev` `573f0052a0e4412e81f0845438fcec2086ce5d55`. Source validation at base `57456af9` is distinct from that candidate.
- Own hosted and act acceptance, including exact-head hosted evidence for any later commit. A later commit un-covers the affected lenses.
- Keep the physical calibration and hardware items tracked as not run.
- Keep the discard-telemetry item on the #495 checklist.
- Merge only with explicit maintainer authorization, a second independent positive at this head, and the full completion bar.
- Optional: refresh the PR body Status line (S1).

R303-3 FINISHED
