[R300] NEGATIVE - exact head fc8a719fecfaade8f5cdd7e7aef5292ffebcc1b4

# R300-1: internal independent review of #545 / PR #563

- Head `fc8a719fecfaade8f5cdd7e7aef5292ffebcc1b4`, tree `d9f1e5139a3ad0a1208be34344ccb8e9d6cdee69`, base and live dev `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`.
- Scope was reconstructed from the public record only: AGENTS.md, CONTRIBUTING.md (sections 1 and 3), docs/README.md, the #545 body, assignment 5827358783 with its citation correction, the #387 decisions 5816509317 and 5794731090, the [A303] TAKEN and REVIEW READY comments, the FPGA-gPTP `INTEGRATION.md` slew-active contract at `5dce647a`, the diff `5b73d3f4..fc8a719f`, the published evidence tree `8602e704:review-evidence/545-r1`, and the exact-head hosted runs.
- Prior public review findings on PR #563: none. When this review was written, the PR had only the two review-start comments and no review bodies, so nothing had to be resolved or retained.
- Verdict: **NEGATIVE**. The product RTL is correct, and both my own probes and the author's probes support that. The verdict is NEGATIVE because a mandatory hosted gate is red at this exact tree (F1), a documented tally clause has no test that can fail (F2), and the authoritative suite index is stale (F3).

## Findings

### F1 MAJOR: Conformance, Tests. The default `mmcm_servo` target overruns its suite deadline, so hosted `rtl-full` is red at the exact tree

- Artifact: `tb/verilator/mmcm_servo/Makefile:44` (`all: run mutants`), `:60-72` (`run` now also runs `Vphc_step +slew_suite`), `:79-80` (`mutants: python3 slew_mutants.py`, five extra Verilator builds and runs).
- Evidence:
  - Hosted `rtl-full` run 36102671321 tested merge commit `dbb41727` (tree `d9f1e513`, identical to the head tree; parents `5b73d3f4`, `fc8a719f`). `Verilator shard 2/5` ended `TIMEOUT mmcm_servo (1800s wall clock)` with exit 92, and the run concluded `failure` (`receipts/hosted_verilator_shard2_job_107968459795.log`, lines 267-289).
  - The suite's own log shows the unit, rails, step and slew suites passing. The runner then killed it partway through the new mutant campaign, after `level_tied_low` (`receipts/hosted_head_suite-logs-2_mmcm_servo.log`, tail: `make: *** [Makefile:80: mutants] Error 143`).
  - At the base, the same shard ran `mmcm_servo` in about 5.6 min (`receipts/hosted_base_5b73d3f47_verilator_shard2_job_107957156222.log`, lines 250-251). Locally the head's default target took 21 min 53 s on a shared host (`receipts/mmcm_servo_make.log`).
  - Authority: #545 acceptance 3 ("Gates green"). AGENTS.md section 7 requires exact-head `verilator-suites` evidence. `docs/testing/TESTING.md:257` says "A long mutation campaign is an explicit target, never a raised deadline."
- Impact: this tree cannot produce a green exact-head hosted Verilator gate, so the completion bar and acceptance 3 are unmet. Every later run of the shared sweep inherits a suite that sits over its deadline. `run_all_suites.sh` reports that as result-unknown, which hides real results.
- Required outcome: the default `mmcm_servo` target finishes well inside its deadline on the hosted runner, and no check is trimmed to make it fit. For example, the slew mutant campaign could become an explicit target recorded in TESTING.md's explicit-campaign table, keeping a no-elaboration arm in the default if the pattern of other suites is followed. The deadline is not raised.
- Verification: a green exact-head `rtl-full` shard 2/5 with `PASS mmcm_servo`, and the explicit campaign's own run recorded with 5/5 named rejections.

### F2 MINOR: Tests. The coincident step-and-slew de-duplication clause has no test that can fail for it

- Artifact: `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:496` (`slew_window_w && !step_hit_w`). Its only claimed check is `tb/verilator/mmcm_servo/sim_main.cpp:638` (`[U14] replacing step counts its open window once`). The contract is documented at `docs/reference/REGISTER_MAP.md:1968` ("a coincident step counts that same window once") and `docs/design/TIME_SYNC.md:212`.
- Evidence: my mutant `step_dedupe_removed` deletes `&& !step_hit_w`. It **survives** the unit harness (94/94) and the silicon-scale `+slew_suite` (87/87): `receipts/mutants/step_dedupe_removed_unit.log`, `receipts/mutants/step_dedupe_removed_suite.log`.
  - U14 places its step at an arbitrary instant. A step that is not on the boundary cycle abandons the window (`win_valid_r` low), so `slew_hit_w` cannot fire anyway, and the check passes with or without the clause.
  - The double count that the clause prevents needs the stepped sample to be staged on the boundary tick while the window is slew-marked. No case builds that.
  - Authority: AGENTS.md section 6 Tests lens, "Each new test can fail for the defect it claims to detect."
- Impact: a documented `MCSRV_STAT[15:10]` behaviour, and the PR evidence line "A replacing step counts its open window once", rest on a clause that could regress silently. The tally would then read one high in that coincidence. This is diagnostic only. Lock and integrator are unaffected.
- Required outcome: a case that stages a PHC step on the boundary sample of a slew-marked window and requires a tally delta of exactly 1. The existing `[P2a]` step-on-boundary arm with the level held is one way. The case must fail with the clause removed.
- Verification: a clean pass, and a named failure for the `&& !step_hit_w` removal mutant.

### F3 MINOR: Docs. The authoritative suite index and explicit-campaign table are stale for the changed test contracts

- Artifact: `docs/testing/TESTING.md:267` and `docs/testing/TESTING.md:483`.
- Evidence:
  - Line 267 still describes the `gmstep-mutants` campaign as "the gmstep leg's nine controls and the option-off leg's two". At the head, `tb/verilator/milan_dp/gmstep_mutants.py` has 13 controls, 11 of them on the gmstep leg. Two are the #545 connection controls, and the "who runs it" file list does not name the slew wiring they guard (`.phc_slew_active_i`, `slew_rate_alignment`). The count went from 11 to 13, measured by parsing the `Control(...)` entries at `5b73d3f4` and `fc8a719f`.
  - Line 483, the `mmcm_servo` row, mentions only the #539 step harness. It says nothing of the `+slew_suite` cases or of the default target now running the `slew_mutants.py` campaign.
  - `scripts/measure_test_evidence.py` was updated for both campaigns and TESTING.md was not.
  - CONTRIBUTING section 3 names TESTING.md as the suite index. AGENTS.md section 6 Docs lens: "Changed contracts are reflected in authoritative docs."
- Impact: a later reviewer who reads the index does not know that the #545 controls exist, which change should trigger them, or what the default `mmcm_servo` target costs, and the default-target cost is the direct cause of F1.
- Required outcome: TESTING.md states the actual campaign inventory and triggers for the #545 controls and the `mmcm_servo` slew coverage, consistent with how F1 is resolved.
- Verification: the text matches the control inventories at the fixing head, and the doc gates pass.

### S1 SUGGESTION: Tests. The connected release-tail check re-encodes the implementation's formula

- Artifact: `tb/verilator/milan_dp/sim_gmstep.cpp:419-443`, `:1082`.
- The check `slew path: every staged sample covers the PHC tail` compares the servo's staged level with `raw || any(last four raw samples)`, which is the RTL expression at `hdl/milan/milan_datapath.sv:2763`. It proves the wiring. It does not prove that four cycles covers the real PHC application latency, so an added stage in `ptp_csr_sync` would still pass.
- I checked the latency independently. My probe drives the real `ptp_csr_sync` and `timestamp_counter` and the transcribed shadow latch, alignment block and servo staging, and reads each slewed per-cycle advance directly. Over 24 schedules, 492 slewed samples, 0 were uncovered (`receipts/latency_probe.log`). The tail is exactly the minimum: tails of 3 and 2 leave 24 and 42 uncovered samples (`receipts/latency_probe_controls.log`).
- The impact of a one-cycle slip is about 1.6 ps per 512 ms window, which is immaterial. That is why this is a suggestion. The optional improvement is to grade against the measured PHC advance rather than the formula.

## Lens results (clean-lens format, with evidence)

- [R300] UNCLEAN Conformance: F1. Acceptance 3 ("Gates green") is unmet at the exact tree. Everything else under this lens checked out:
  - Assignment item 1: the gitlink is `160000 5dce647a`, which is FPGA-gPTP PR #76's merge commit and identical to its `main`. Regenerating `gptp_ucode.hex` with the pinned generator gives `c496ed8a…0371`, equal to the `syn/yosys/rom_digests.tsv` row for that pin (`receipts/rom_digest_check.txt`). No `e5dcea6e` text remains outside the digest ledger. SUBMODULES, GPTP_PLANE, the gptp guides, traceability, both diagrams and CHANGELOG are updated.
  - Item 2: the level passes shadow → datapath → servo, all on `axis_clk` (`KL_gptp_shadow.sv:147-150,685`, `milan_datapath.sv:2756-2767,5562-5568,6944`), and the crossing statement is correct.
  - Item 3: discard, count, hold and LOCKED behave as #387 decision 5816509317 requires. The indication comes from the plane and is not inferred.
  - Item 4: the tests exist and pass.
  - Item 5: the named docs are updated.
  - Item 6: the area evidence is +7 LUT / +2 FF for the servo and 1 LUT / 4 FF for the alignment block. That matches the two added servo flops and the four tail flops by inspection.
  - No single-port assumption: one plane-wide level, no port index.
  - The citation correction (IEEE 802.1AS B.1.1 ±100 ppm; Milan v1.2 7.4 ±50 ppm) is applied in `docs/design/TIME_SYNC.md:124-132`.
  - The 0.5 s conflict between the historical decision and the adopted engine contract is published on #545 and in `TIME_SYNC.md:116-122`, not resolved privately.
- [R300] PASS RTL: `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:466-496,585-611,705-719,955-956`; `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:147-150,685,746-749`; `hdl/milan/milan_datapath.sv:1462,2748-2767,5567-5568,6944,7036`; `hdl/ieee8021as/ptp_timestamp/ptp_csr_sync.sv:112-126` and `timestamp_counter.sv:150-171`. What I checked:
  - The window marking covers every sample of a window, including its closing sample. It relies on the sticky set, `slew_window_w = win_slew_r || phc_slew_q_r` at the boundary, and seeding at the boundary and at open.
  - The PI, trim and lock writeback is gated through `pp_run_r`. Guard double counting is impossible because `guard_hit_w` needs `pp_run_r`.
  - A step wins its window via later non-blocking assignments.
  - All new flops are reset. Widths are correct, including the 7-bit tally sum saturating at 63.
  - Same-domain alignment holds: engine edge E0 → latch E1 → two sync flops E2/E3 → counter E4. The 4-cycle tail is exact, and my latency probe confirms it with negative controls.
  - `g_gptp_off` ties the level to 0.
  - The lint ratchet passes at the head: 90 ≤ 90 (`receipts/lint_rtl_check.log`).
  - No finding.
- [R300] PASS Robustness: `tb/verilator/mmcm_servo/sim_main.cpp:615-642` (U14) and `sim_phc_step.cpp:447-513` (S1-S4), run at the head (`receipts/mmcm_servo_make.log`: 94 unit, 8 rails, 113 step, 87 slew, author mutants 5/5). What I checked:
  - Both 100 us signs at 200 ppm. The integrator and command are held exactly and LOCKED holds on every edge. The first clean window moves the integrator by 20/512 ppm, within the ±1 ppm bound.
  - A 100 ns in-window pulse, a shared boundary sample, a clean close before the slew, a level held for 7 or more windows, reset during a slew, tally saturation, and a replacing step.
  - Feature-off: `g_gptp_off` ties the level low, and `MCSERVO_P=0` leaves it unused.
  - My mutants `mid_window_memory_removed` and `boundary_seed_dropped` are KILLED (`receipts/mutants/`).
  - `open_seed_dropped` survives. That is not a defect: a level staged on a window's opening sample describes the advance into that sample, which lies outside the window's span. So the seed is conservative only, like the documented shared-boundary taint.
  - The residual coincidence gap is F2, which is a Tests finding.
  - No Robustness finding.
- [R300] UNCLEAN Tests: F1 and F2, plus suggestion S1. What was clean:
  - The author's four servo mutants each fail their named check at the head.
  - The connected gmstep slew phase passed its 8 slew-path checks, 56 checks in all, in the exact-tree hosted `milan_dp` run (`receipts/hosted_head_milan_dp_gmstep_slew_excerpt.txt`; shard 4/5 PASS in `receipts/hosted_head_verilator_shard4_job_107968459773.log`).
  - The tie-offs in the `crf_rx`, `gptp_shadow`, `gptp_txts`, `rails` and `autorepair` fixtures are appropriate.
- [R300] UNCLEAN Docs: F3. What was clean:
  - `docs/design/TIME_SYNC.md:97-132,173-174,192-234` (step-policy bullets, loop table rows, alignment and test prose), `docs/design/GM_LOSS_RECOVERY.md:152,154,189`, `docs/reference/REGISTER_MAP.md:1968` and `docs/reference/SUBMODULES.md:24,96-105` are accurate against the RTL and the engine contract.
  - `CHANGELOG.md` is accurate.
  - No stale "#545 open" wording remains.
  - Doc style, doc paths and `docs_check` pass (`receipts/doc_gates.log`).

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #545 acceptance 1-3, assignment items 1-6, #387 decisions, pin/ROM digest, hosted `rtl-full` 36102671321 | R300-1 | `fc8a719fecfaade8f5cdd7e7aef5292ffebcc1b4` |
| RTL | CLEAN | servo, shadow and datapath lines above; `ptp_csr_sync`/`timestamp_counter` latency; latency probe with controls; lint | R300-1 | `fc8a719fecfaade8f5cdd7e7aef5292ffebcc1b4` |
| Robustness | CLEAN | U14, S1-S4, P0-P4 at the head; 3 reviewer mutants with verdicts; feature-off ties | R300-1 | `fc8a719fecfaade8f5cdd7e7aef5292ffebcc1b4` |
| Tests | UNCLEAN (F1, F2) | `mmcm_servo` Makefile, `sim_main.cpp`, `sim_phc_step.cpp`, `slew_mutants.py`, `sim_gmstep.cpp`, `gmstep_mutants.py`, fixtures; hosted shards 2 and 4 | R300-1 | `fc8a719fecfaade8f5cdd7e7aef5292ffebcc1b4` |
| Docs | UNCLEAN (F3) | TIME_SYNC, GM_LOSS_RECOVERY, REGISTER_MAP, SUBMODULES, GPTP_PLANE, gptp guides, traceability, diagrams, CHANGELOG, TESTING, `tb/verilator/milan_dp/README.md` | R300-1 | `fc8a719fecfaade8f5cdd7e7aef5292ffebcc1b4` |

A fix for F1 or F2 touches `Tests` scope, and F3 touches `Docs`. RTL and Robustness stay banked only if the fix leaves `KL_mmcm_drp_servo.sv`, `KL_gptp_shadow.sv`, the datapath alignment and connection lines, and the servo harnesses' stimulus unchanged. Otherwise those lenses must be covered again at the new head.

## Real limits

- I did not build or run `milan_dp` (gmstep) or `gmstep_mutants.py --slew` locally. For the connected leg I rely on the exact-tree hosted `milan_dp` log and on the published author log for the two connection controls. My latency probe replaces the engine with a driven sequence that follows `gptp-processor/hdl/top/KL_gptp_engine.sv:917-944` at the pin. It is not the engine itself.
- I did not reproduce the area numbers (no Yosys run). They are consistent with the flop count by inspection only.
- I did not run the em-dash, TOC and anchor gates: the pinned Markdown renderer is absent from this host and installs were out of scope. The hosted `docs` workflow passed at the exact head.
- I did not run the xvlog, builder, behave, idiom, port-contract or naming gates, or the `crf_rx`, `gptp_shadow` and `gptp_txts` suites. The manager's banks and the author's receipts cover those.
- The author's `slew_mutants.py` builds use the Makefile's `-j 0`. My one unmodified `make` therefore compiled at host parallelism for five small servo builds. All my own builds were capped at 8 jobs in total.
- Physical calibration was not run, field skips are not hardware proof, and nothing here is bench evidence.

## Pending manager duties

- Hosted and act acceptance at the fixing head: shard 2/5 must show `PASS mmcm_servo` within its deadline (F1).
- The final current-dev candidate build at the merge turn, including the later dev merge for the #508 pin-text and diagram overlap. I judged content at this head only.
- Re-review of F1-F3 at the corrected head by a reviewer identity.
- The external review (R301) remains independent of this one.

R300-1 FINISHED
