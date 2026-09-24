[R277] NEGATIVE - exact head e68c1b1ac08c8b1e12a28e281b266d06f881e402

External independent review, round R277-3, of PR #555 (Relates to #387, acceptance 3, datapath half).
Head `e68c1b1ac08c8b1e12a28e281b266d06f881e402`, tree `c8b28ac217337d5d5e12af41e9ece31e3e80e831`. The reviewed range is `57456af96b3127b9d309a995bbbd35a6113ce52d..e68c1b1a`: four one-line branch commits plus one merge of dev `57456af9`.

The verdict is NEGATIVE because of one BLOCKER. An existing required gate goes red at this head: `sw/builder/test_builder.py::test_baremetal_profile_contract` passes at the base and fails at the head. Three MINOR findings are also open. One of them, F4, was confirmed only after this verdict was written. The datapath behaviour itself matches the #387 decisions: the step is one `mr` toggle, MEDIA_RESET counts it, the render stage re-bases once, and a request can no longer cancel a pending restart. Mutation and property probes confirm this.

## Reconstruction

In order, I read the following:
- AGENTS.md and CONTRIBUTING.md (sections 1, 3 and 6.1);
- the issue #387 body;
- decision 5606198212 (part b);
- owner decision 5794731090;
- rulings 5802264260 (items 1 and 2);
- the aligner owner decision 5810378282;
- the #545 slew decision 5816509317;
- assignments 5814963103 and 5816975318;
- the author's REVIEW READY notes 5816940740 and 5817241898.

I then read the PR #555 body, the full diff and its history, the hosted check list, and the public evidence tree `964ac393:review-evidence/387b-r1`: the author and merge-round gate receipts, `sweep-state.txt` and `final-status.txt`. The PR carried no review findings when my pass began, only two review-start notices. See "Prior public findings" below.

## Findings

### F1 - BLOCKER - lenses: Tests, RTL - `sw/builder/test_builder.py:8861-8867` and `:10288-10295` against `hdl/milan/milan_datapath.sv:6026-6028`

- **Authority/evidence.** The builder gate pins the exact term set of `render_recentre_p_w`. Its comment says this is so "the extra reference can only ever be this read". It also plants an ADP-term mutant on the literal text `gm_recentre_p_r | eff_ptp_adjust_w | cfg_ptp_cmd_load`. The PR rewrites that initializer to `media_rebase_p_w | src_recentre_p_r` and does not update either anchor. Evidence:
  - At the base `57456af9`, `python3 -m pytest sw/builder/test_builder.py -k test_baremetal_profile_contract` passes: 1 passed in 369 s (`receipts/builder_baremetal_profile_contract_base.log`).
  - At the head it fails: `AssertionError: render recentre pulse must read only the GM-change, adjtime, settime and settled clock-source discontinuities: unexpected render_recentre_p_w initializer 'media_rebase_p_w | src_recentre_p_r'` (`receipts/builder_baremetal_profile_contract_head.log`).
  - `main()` runs this gate second (`test_builder.py:24443`).
  - Hosted `elaborate` (`.github/workflows/elaborate.yml:260`) and `docs` (`docs.yml:205`) run `test_builder.py`. Both were pending when checked.
  - The author's gate tables do not list `test_builder.py`. The PR's Definition of Done leaves "Required local verification bar passes" unchecked.
- **Impact.** Merging turns a required hosted gate red on `dev`. Separately, the PHC census that gate enforces never pins `media_rebase_p_w`. The PR introduces that wire, and it now carries the PHC step into both the render stage and `mcr_restart_p_w`.
- **Probe.** I re-pointed only the two literal anchors in a disposable copy (`probes/builder_pin_probe.py`). With that change the test passes: 1 passed in 373 s (`receipts/builder_pin_probe.log`). So the failure comes from the stale pin and nothing else. That probe is not a proposed fix.
- **Required outcome.** `test_builder.py` passes at the head, with its PHC-census pins covering the new read path. That means the exact right-hand side of `media_rebase_p_w` and the reason text, and a mutant anchor that exists exactly once.
- **Verification.** `python3 sw/builder/test_builder.py` exits 0 at the corrected head, or at minimum `pytest -k test_baremetal_profile_contract` passes. Hosted `elaborate` is green on that exact head.

### F2 - MINOR - lens: Tests - `hdl/milan/milan_datapath.sv:3110` (`cfg_ptp_cmd_load` term) and `tb/verilator/milan_dp/sim_main.cpp:109-113`, `:975-979`, `:1033-1034`

- **Authority/evidence.** The PR's decision 4, `CHANGELOG.md:39`, `TIME_SYNC.md:197` and owner decision 5794731090 ("every step is one counted event") all make a software settime one `mr` toggle. No check can fail for that behaviour. I planted `settime_no_mr`: `mcr_restart_p_w` takes `eff_ptp_adjust_w` instead of `media_rebase_p_w`, so settime no longer restarts `mr` but adjtime still does. The mutant survives both legs that could see it:
  - the option-off `obj_dir` leg: 231/0, rc 0 (`receipts/optoff_settime_no_mr.log`);
  - the gmstep leg: 48/0, rc 0 (`receipts/gmstep_settime_no_mr.log`).

  The harness does issue a settime at `sim_main.cpp:1033` and increments `phc_steps_issued`. No `mr` check follows it, so the counter comment at `:109` ("settime or adjtime") suggests coverage that does not exist. The two other probes show the new check can fail:
  - `adjtime_no_mr` fails `CLKV: its mr toggled once per PHC step issued so far (#387)` (`receipts/optoff_adjtime_no_mr.log`);
  - `step_gated_by_source` fails the same check (`receipts/optoff_step_gated_by_source.log`).
- **Impact.** A regression that stops settime from restarting `mr` would merge green. Settime is a live product path: `sw/firmware/milan_baremetal/milan_baremetal.c:99-104` `settime_ns()`.
- **Required outcome.** A check that fails when a settime does not toggle `mr` once and count once, plus a control that plants that defect.
- **Verification.** The `settime_no_mr` probe (`probes/plant.py`, `probes/run_optoff.sh`) fails a named check.

### F3 - MINOR - lenses: Conformance, Robustness, Tests, Docs - `hdl/ieee1722/avtp/KL_media_clock_restart.sv:56-57`, `:68-72`, `:205`; `docs/design/GM_LOSS_RECOVERY.md:157`; PR body decision 1

- **Authority/evidence.** Ruling 5802264260 item 2 says "a step that lands while an `mr` restart is pending merges with it. The result is exactly one restart." The executor's reading, which this round was asked to judge, is that pending means requested but not yet on the wire. The RTL ends "pending" when the engine grants the new level. At that edge `mr_o` changes and `tgt_r` equals `mr_o`. The level reaches the wire only at the talker's next launch, which is up to one PDU period later: 125 us for AAF, 2 ms for CRF. A request in that gap sets `tgt_r <= ~mr_o` and becomes a second restart.
- **Probe.** The property probe (`probes/mcr_prop/tb.cpp`, directed cases D3 and D4) measures two wire toggles for two requests when the second lands after the grant and before any PDU at the granted level. The rationale the RTL banner gives for that case ("that stream's listeners have already seen the earlier toggle", `:70`) does not hold in this gap. The same rationale appears in the PR's decision 1, and `GM_LOSS_RECOVERY.md:157` says "after the stream stamped the first". When the stream's previous toggle has already held its eight PDUs, the usual case for the ruling's own example (a CRF disruption plus a step), the engine grants the first request on the next edge. So in practice the merge happens only when the second request arrives in that same cycle, or while an earlier toggle is still holding.
- **What is fine.** Nothing is lost or cancelled, and the hold is kept. The probe confirms this: P1 to P4 are clean over 6 seeds x 40 random runs (`receipts/mcr_prop_head.log`). The same probe catches the base engine losing requests (P1 = 21, `receipts/mcr_prop_base_engine.log`). So F3 is a mismatch between the decided reading, the code and the text, not a safety defect.
- **Impact.** A step that lands within one PDU period after a granted restart puts two counted restarts on the wire. Under the not-on-the-wire reading it should be one. The documentation says the listeners have already seen the toggle when they have not.
- **Required outcome.** One of the following:
  - (a) The manager rules publicly that "pending" ends at the engine's grant. The banner, the `GM_LOSS_RECOVERY.md` row and the PR text then state that boundary and drop the "listeners have seen it" rationale for the gap.
  - (b) The engine treats the stream as pending until a PDU at the granted level has launched.

  In either case, add a tkdiag arm that places a request in the grant-to-launch gap and grades the decided toggle count.
- **Verification.** The D3/D4 probe, or an equivalent T17 arm, gives the ruled count. P1 to P4 stay clean.

### F4 - MINOR - lenses: Docs, RTL - `hdl/ieee1722/aaf/KL_render_setpoint.sv:81-83` and `:167-170`

My independent pass missed this finding. I added it after this verdict and ledger were written, when reading the parallel round's headings (see the cross-reference section), and confirmed it at this head by inspection.

- **Authority/evidence.** The render stage's banner (`:81-83`, "recentre_p_i (the integration's set: a GM identity change, a PHC step, a clock-source change ...)") and its port spec (`:167-170`) still list a grandmaster identity change as a re-centre trigger. After this PR `milan_datapath.sv:6026-6028` no longer feeds it one. CONTRIBUTING section 1 makes the port list the spec.
- **Impact.** The module's own contract states a trigger the integration no longer delivers.
- **Required outcome.** The banner and port comment name the #387 trigger set: the PHC step and the settled clock-source change.
- **Verification.** Inspection at the corrected head.

It adds nothing to the ledger: Docs and RTL are already UNCLEAN.

### Suggestions (do not affect coverage)

- **S1 (Docs).** `docs/testing/CI_WORKFLOWS.md:159` and `scripts/run_all_suites.sh:240-242` still give the `milan_dp` basis as "hosted worst case about 1815 s, plus 885 s (49%)". Adding about 182 s locally, about 288 s at the 1.58x hosted slowdown, projects about 2103 s against 2700 s, a margin of about 597 s. Record that projection, or the next hosted measurement, next to the budget.
- **S2 (Docs).** The PR body "Status" still names head `00d388d8` and base `59b81670`, and says the sweep ran there. Update it to the merge head and state which gates ran at `e68c1b1a`.
- **S3 (Docs).** The `GM_LOSS_RECOVERY.md:155` "whatever the media clock source" claim cites only gmstep, which runs under CRF selection. The INTERNAL-source evidence is the new `sim_main.cpp` `mr` check in the `obj_dir`, `obj_nolpf` and `obj_ax1x1` legs, which my `step_gated_by_source` probe shows can fail. Cite it.
- **S4 (Tests).** `gmstep_mutants.py:230` and `mcr_mutants.py:148` use whatever executable is already in `obj_gmstep` or `obj_dir` as the positive control, without checking it matches the sources. That is safe under `make`, which rebuilds first. A standalone run can grade a stale binary.

## Judgements requested by the assignment

- **1722-2016 4.4.4.3 and Milan Table 5.4.**
  - A step reaches `restart_p_i` ungated by the clock source (`milan_datapath.sv:3110-3113`), in the `axis_clk` domain like the other terms. `eff_ptp_adjust_w` and `cfg_ptp_cmd_load` already fed `ptp_csr_sync` on `aclk = axis_clk`, so no new crossing is added.
  - The eight-PDU hold stays per stream, and my probe (P2) found no violation.
  - MEDIA_RESET is derived from the `mr` bit each PDU actually carried (`KL_talker_diag_ctx`), so a merged request counts once and a separate restart counts separately. The gmstep leg shows one toggle at step+116 cycles and one MEDIA_RESET (`receipts/gmstep_leg_head.log`).
  - Conforms, except for the boundary in F3.
- **Readings.**
  - (i) Pending: acceptable only once the boundary in F3 is ruled and documented.
  - (ii) Streams ending on opposite `mr` levels: accepted. 4.4.4.3 holds are per stream, and 10.4.3 makes only the `mr` of the stream a Listener recovers from meaningful. T17 grades the divergent case (talker 0 gets two toggles, talker 1 one).
- **Changed legacy check.** `sim_main.cpp:975-979` masks only `mr` (`& 0xF7`, still expecting `0x81`) and adds a parity check of `mr` against the steps the harness issued. It is not a weakening: it catches a clock-source-gated step and a plane-off adjtime without `mr`. The obj_dir leg reports 231/0, matching the README count. Its gap is the settime arm (F2).
- **Sweep time.** On this host `make gmstep-mutants`, which builds and runs the leg plus all nine controls, took 393 s wall (`receipts/gmstep_and_mutants_all.log`), consistent with the author's 372 to 386 s. The author's +182 s for the default additions is plausible. The projected hosted margin of about 597 s, 22% of the budget, is adequate but unmeasured (S1). The deadline is not raised.
- **The #387 part b aligner decision.** Untouched:
  - the `GM_LOSS_RECOVERY.md` grid-aligner row is byte-identical to dev `57456af9`;
  - `KL_media_grid_align.sv` and `KL_mmcm_drp_servo.sv` are unchanged across the range;
  - the merge keeps #539's servo and aligner rows.

## Lens results (applied at `e68c1b1a`)

- `[R277] UNCLEAN Conformance - KL_media_clock_restart.sv:56-72,205; milan_datapath.sv:3097-3113 - checked against 1722-2016 4.4.4.3 and 10.4.3, Milan Table 5.4, decision 5606198212 part b, owner decision 5794731090, rulings 5802264260 items 1 and 2, aligner decision 5810378282; F3 open.`
- `[R277] UNCLEAN RTL - milan_datapath.sv:3110-3113,5934-5953,6026-6028; KL_media_clock_restart.sv:176-227; KL_crf_tx.sv:53-60,148-153 - clock domain of every media_rebase_p_w term, reset values, widths (tgt_r vector, sim_nxn.cpp mask), per-talker adoption; lint_rtl --check PASS 90<=90 (receipts/lint_rtl_check_head.log); F1 open (the PHC-census contract over these nets is broken).`
- `[R277] UNCLEAN Robustness - probes/mcr_prop/tb.cpp against KL_media_clock_restart.sv at head - random requests against two talkers with different PDU rates, reset between runs, lost, hold, stray and settle properties clean over 6x40 runs; the repeated-request boundary is F3.`
- `[R277] UNCLEAN Tests - tkdiag T17 90/90 plus mcr_mutants 3/3; gmstep 48/48 plus all 9 controls caught; obj_dir 231/0; probes settime_no_mr (survives), adjtime_no_mr and step_gated_by_source (caught); builder gate - F1, F2, F3 open.`
- `[R277] UNCLEAN Docs - GM_LOSS_RECOVERY.md:148-199, TIME_SYNC.md:197, REGISTER_MAP.md:124-133, TESTING.md:267,501, milan_dp/README.md, CHANGELOG.md:30-49; no U+2014 added (0 added lines); commits one-line with no trailers - F3 open; S1-S3.`

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F3) | `KL_media_clock_restart.sv`, `milan_datapath.sv:3097-3113,6026-6028`, #387 decisions and rulings, gmstep leg log | R277-3 | e68c1b1ac08c8b1e12a28e281b266d06f881e402 |
| RTL | UNCLEAN (F1, F4) | `milan_datapath.sv`, `KL_media_clock_restart.sv`, `KL_crf_tx.sv`, lint ratchet, builder PHC census | R277-3 | e68c1b1ac08c8b1e12a28e281b266d06f881e402 |
| Robustness | UNCLEAN (F3) | engine property probe (random, reset, per-talker holds, grant boundary), base-engine control | R277-3 | e68c1b1ac08c8b1e12a28e281b266d06f881e402 |
| Tests | UNCLEAN (F1, F2, F3) | tkdiag T17 plus mutants, gmstep plus 9 controls, obj_dir option-off leg plus 3 probes, `test_builder.py` gate 1b | R277-3 | e68c1b1ac08c8b1e12a28e281b266d06f881e402 |
| Docs | UNCLEAN (F3, F4) | `GM_LOSS_RECOVERY.md`, `TIME_SYNC.md`, `REGISTER_MAP.md`, `TESTING.md`, `CI_WORKFLOWS.md`, milan_dp README, CHANGELOG, PR body | R277-3 | e68c1b1ac08c8b1e12a28e281b266d06f881e402 |

## Prior public findings

When my pass began, PR #555 carried no review findings: 0 formal reviews, 0 inline comments, and two review-start notices. The R277-1 findings belong to PR #540, not this PR. A parallel round, R276-4, published a verdict on this PR at 16:21 UTC, after my pass began. I did not read it before writing this verdict and ledger.

**Cross-reference, read after the verdict and ledger were written** (https://github.com/kebag-logic/milan-fpga/pull/555#issuecomment-5817943136):

| R276-4 | This round |
|---|---|
| F1 (builder pin) | Same defect as this round's F1, found independently. |
| F2 (the pending boundary is adoption, not the wire) | Same substance as this round's F3, found independently. |
| F3 (render-stage banner and port spec) | Confirmed at this head and added as F4, marked as not found independently. |
| F4 (the stated `milan_dp` margin rests on a stale figure) | This round raised only the stale figure, as S1 (SUGGESTION). The claim that the real margin is about half the stated one was not independently established. I neither adopt nor dismiss it; the manager's hosted measurement settles it. |
| S1 and S2 | Match this round's S2 and S4. |

R276-4 records Robustness as clean. This round records it UNCLEAN because it files the pending-boundary finding under Robustness as well (repeated-request idempotence).

## Limits

- **Not run:**
  - the full `milan_dp` default sweep at this head (I ran the gmstep leg, all nine gmstep controls and the obj_dir option-off leg);
  - the complete `test_builder.py`, `run_all_suites.sh`, Yosys, xvlog and docs gates;
  - hosted and replicated CI.
- **Evidence gap.** The author's full sweep receipt is from `1dc93828`, before the merge. The merge brings #539's `KL_mmcm_drp_servo.sv`, which the gmstep leg elaborates and passed with here. The manager's statement that the full static/builder bank passed at this head conflicts with F1. I found no manager-owned builder receipt in the evidence tree.
- **Build jobs.** One recipe run (`make gmstep-mutants`) used the Makefile's default `VERILATOR_JOBS=0`, which lets the compiler use more than eight jobs. Every later build set `VERILATOR_JOBS` to 2 or 4 with at most four builds at once.
- **Probe scope.** The property probe models the packetizer as latch-at-launch with a fixed 3-cycle completion latency. It runs the engine alone, not the datapath.
- **Not claimed.** Physical calibration and the #117 two-board handover (acceptance 4) were NOT RUN and are not claimed. Field skips are not hardware proof.
- **Hosted checks.** At the time of checking, the exact-head hosted checks `elaborate`, `full-ci-gate`, `verilator-lint`, `yosys-elaboration` and `docs-check` were pending. `bdd-conformance`, `docs-check-no-git`, `changes` and `wire-accountability` passed.

## Pending manager duties

- Obtain the F1 fix and a green `test_builder.py`/`elaborate` on the corrected head.
- Rule the F3 pending boundary.
- Accept the F2 settime arm.
- Re-review the corrected head.
- Run the current-dev candidate merge validation and the hosted/act acceptance.
- Run the #117 bench (acceptance 4) after merge.

## Clone integrity

The review clone was never modified; every build and probe ran in copies under `scratch/`. After the probes, the clone showed:
- HEAD `e68c1b1a`;
- `git write-tree` = `c8b28ac2`;
- an empty `status --ignored`;
- all 883 tracked files byte- and mode-identical to their blobs, with no assume-unchanged or skip-worktree flags;
- gitlinks `gptp-processor` e5dcea6e, `protocol-processor` 09f9bf38 and `third_party/verilog-axis` 48ff7a7e checked out at their pins, with `external` uninitialised as at the start (`receipts/clone_integrity.txt`).

## Receipts

Listed in `MANIFEST.sha256`:
- `receipts/` contains the logs above plus `tool_identity.txt` (the simulator is 5.050 rev v5.050, with its wrapper hash).
- `probes/` contains the portable scripts: `plant.py`, `run_optoff.sh`, `run_gmstep_probe.sh`, `builder_pin_probe.py`, and `mcr_prop/{tb.cpp,run.sh}`.

R277-3 FINISHED
