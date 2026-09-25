[R301] POSITIVE - exact head b94f53cc4e5dbfd9527ba666922a55804515165c

# R301-2 external review: issue #545 / PR #563

- Role: [R301], external independent reviewer, cleared context, round R301-2 (delta round).
- Exact head: `b94f53cc4e5dbfd9527ba666922a55804515165c`, tree `2a7274e19b88474411829707fb0581e2861bb015`. That is one commit on `fc8a719fecfaade8f5cdd7e7aef5292ffebcc1b4`.
- Diff reviewed: I read `fc8a719f..b94f53cc` (12 files, +166/-37) in full. I checked it against the whole-lane diff `5b73d3f47dfed519eb988c13d6beb1db664ef1e0..b94f53cc`.
- Scope authority:
  - Issue #545 body.
  - Assignment 545#5827358783.
  - Round-2 assignment and decisions 545#5828714628:
    - F1: the slew campaign becomes an explicit target under the #367 rule. The deadline is not raised and no check is trimmed.
    - The streak rule: a slew discard resets the guard-discard streak. This is stated and pinned.
  - Executor post 545#5829377477 (REVIEW READY).
  - Public author packet `review-evidence/545-r1/author-r2` at archive `062a0a915e47380b408f5f3812b2723ae25d76c8`.
- My own round-1 verdict (PR comment 5828686574) covered `fc8a719f`. Section "Prior findings" disposes of each round-1 finding at this head.

## Verdict summary

The product RTL is unchanged in logic since round 1. The only hardware-source delta is four header comment lines in `KL_mmcm_drp_servo.sv:88-91`, and they describe lines 709-715 correctly. I re-applied all five lenses at this head. Every round-1 finding is closed by executable evidence I reproduced:

- **F1.** The default `mmcm_servo` target now runs unit 100, rails 8, step 113 and slew 90 checks, with no mutation campaign.
  - Hosted exact-head `Verilator shard 2/5` passed `mmcm_servo` in 1159.1 s of its 1800 s budget, and `verilator-suites` is `success`.
  - The explicit campaign `slew-mutants` passes 8/8. Every control fails its named check.
- **F2.** S5 stages a PHC step on the boundary sample of a slew-marked window with the level held, and requires a tally delta of exactly 1. The exclusion-removal control fails S5 at 2 counts. My round-1 probe reproduces its round-1 verdicts unchanged.
- **F3.** The connected tail check now grades against the counter's measured per-cycle advance.
  - It is not vacuous: exactly 4 tail samples at the head, equal to my independent round-1 tail probe.
  - The added addend-stage control fails it.
  - My own shortened-tail and two-stage-delay variants fail it too.
- **S1** is decided, documented and pinned by U15, and the U15 control fails.

The remaining observations are SUGGESTIONS only.

## Findings

No `BLOCKER`, `MAJOR` or `MINOR` finding is open at this head. Three SUGGESTIONS follow. They are optional and do not affect lens coverage.

### S-A SUGGESTION: the connected tail oracle is one-sided, so an over-long release is not graded

- **Lenses:** Tests.
- **Where:** `tb/verilator/milan_dp/sim_gmstep.cpp:439-450`. The oracle counts only `(raw || tail) && !sampled`. The only upper bound is the end-state check `:1091` ("servo clears after the PHC tail"), taken three Sync periods later.
- **Evidence:** In `receipts/connected_tail_probe.txt`, the head's release tail was lengthened from 4 to 12 stages (`tail12`). It passes 58/58 with 8 extra servo-high samples.
  - The round-1 harness compared equality with the RTL formula, so it would have flagged this. The new ground-truth oracle trades that away.
  - Over-coverage is conservative: it can only discard a window, never corrupt PI. So this is not a correctness gap.
- **Suggestion:** Also bound the over-coverage. For example, count `sampled && !(raw || tail)` samples per release and require at most a stated small number. That keeps the documented "delays release four cycles" (`TIME_SYNC.md:208`) visible to a regression.

### S-B SUGGESTION: record the hosted exact-head `mmcm_servo` window as the 1800 s row's current basis

- **Lenses:** Docs.
- **Where:** `docs/testing/CI_WORKFLOWS.md:158,162-170`; `tb/verilator/mmcm_servo/Makefile:19-21`.
- **Evidence:**
  - The 1800 s row now correctly labels 548 s as the "original hosted basis". It defers to the local two-CPU figure in the Makefile (952.797 s on 5.052) and to hosted acceptance.
  - Hosted acceptance at this head measured 1159.1 s. That is 64.4% of the budget with 640.9 s margin (35.6%), on a runner whose other suites matched the base run's speed (`receipts/hosted_exact_head.txt`).
  - This margin is inside the decision's "well inside" and above the `milan_dp` 10% split trigger. It is smaller than the 47.1% local margin in the Makefile header, and it is one sample.
- **Suggestion:** At merge, record the hosted window, with its job link, beside the `milan_dp` samples. `mmcm_servo` is now the longest default suite besides `milan_dp`, so its row should state its own margin trigger.

### S-C SUGGESTION: name the shadow addend latch among the `gmstep-mutants` triggers

- **Lenses:** Docs, Tests.
- **Where:** `docs/testing/TESTING.md:267`.
- **Evidence:** The trigger list names the datapath slew wiring, the PHC addend path, `ptp_csr_sync.sv` and `timestamp_counter.sv`. It does not name `KL_gptp_shadow.sv` or a `gptp-processor` pin change. Yet `TIME_SYNC.md:208-210` counts the shadow latch in the four-cycle tail, and the engine's level/addend-pulse alignment sets its start.
  - The default leg still runs the tail check on every sweep, so this only affects when the controls must be re-proved.
- **Suggestion:** Add `KL_gptp_shadow.sv` (`phc_adj_o`, the slew pass-through) and processor pin bumps to the "who runs it" list.

## Prior findings on this PR (my round 1, `fc8a719f`), resolved or retained at this head

| ID | Round-1 severity | Status at `b94f53cc` | Evidence |
|---|---|---|---|
| F1 | MAJOR | **Resolved** | Details below |
| F2 | MINOR | **Resolved** | Details below |
| F3 | MINOR | **Resolved** | Details below |
| S1 | SUGGESTION | **Resolved** as decided | Details below |

**F1 evidence:**
- `Makefile:48` `all: run`. The `run` target (`:72-80`) keeps unit, rails, step and `+slew_suite`. `slew-mutants` (`:86-87`) is explicit, and `mutants` is an alias.
- Hosted suite log `suite-logs-2/mmcm_servo.log` shows 100/8/113/90 checks and no campaign invocation.
- Hosted `mmcm_servo` took 1159.1 s of 1800 s. Run 36113401588 is `success` and `verilator-suites` is `success`.
- My local default on two pinned CPUs with the pinned 5.050 took 746 s (66.5 + 338.5 + 340.6 s).
- Explicit campaign 8/8, with each control failing by name.
- `TESTING.md:268` row and triggers present.
- Author timings (base 516.943 s, r1 1652.793 s, r2 952.797 s on CPUs 8-11) are in `author-r2/timing-*.log`, and they are consistent with mine.

**F2 evidence:**
- S5 is `sim_phc_step.cpp:518-534`, run by both `slew_control` (`:110`) and `slew_suite` (`:122`).
- Head: `[S5] ... counted once = 1 in [1, 1]`.
- Control `step_dedupe_removed` fails S5 by name.
- My unchanged round-1 probe: head 1, mutant 2 (`receipts/coincide_probe_r1_rerun.txt`).
- My unchanged unit-only mutant still survives U14 (`receipts/reviewer_mutants_r1_a.txt`). That is expected, because U14 steps mid-window, and its label now says so (`sim_main.cpp:667`).

**F3 evidence:**
- The oracle reads `ts_counter.acc` including its 24 fraction bits (`sim_gmstep.cpp:422-427`). It uses no pipeline depth.
- The head has 4 tail samples and 0 errors.
- The addend-stage control fails. My `tail3` gives 1 error and my `addend2` gives 2 errors.
- My unchanged round-1 tail probe still reports 4 stages exact and 3 stages violating (`receipts/tail_probe_r1_rerun.txt`).
- The datapath, shadow, CSR sync and counter are byte-identical to round 1 (`git diff fc8a719f..b94f53cc -- hdl` touches only the servo header).

**S1 evidence:**
- Decision 545#5828714628.
- Header `KL_mmcm_drp_servo.sv:88-91` and `TIME_SYNC.md:180-186` agree with the RTL: `:715` resets on a slew hit, and `:711` does the same on a #539 step, pinned by U12.
- U15 (`sim_main.cpp:555-579`) passes.
- Control `slew_streak_reset_removed` fails `[U15] four fresh guard trips precede re-base`. My unchanged round-1 unit streak mutant now fails U15 too (`reviewer_mutants_r1_a.txt`).
- The silicon slew suite alone still does not catch it (`reviewer_mutants_r1_b.txt`). That is expected, and it is why U15 exists.

## Prior findings on this PR (internal round R300-1, `fc8a719f`), resolved or retained at this head

I read these only after my verdict and ledger above were written.

| ID | Round-1 severity and lenses | Status at `b94f53cc` | Evidence |
|---|---|---|---|
| R300 F1 | MAJOR, Conformance and Tests | **Resolved** | Same evidence as my F1 above |
| R300 F2 | MINOR, Tests | **Resolved** | Details below |
| R300 F3 | MINOR, Docs | **Resolved** | Details below |
| R300 S1 | SUGGESTION, Tests | **Resolved** | Details below |

**R300 F1 evidence:**
- Default `mmcm_servo` hosted `PASS` in 1159.1 s of 1800 s, with no check trimmed and the deadline unchanged.
- The explicit campaign is recorded in `TESTING.md:268`, and it runs 8/8 with named rejections. That includes the original five controls' four defects plus the two new ones.

**R300 F2 evidence:**
- S5 (`sim_phc_step.cpp:518-534`) arms the `[P2a]`-style boundary step with the level held and requires exactly 1.
- The `&& !step_hit_w` removal control fails S5 by name (`receipts/slew_case_step_dedupe_removed.txt`).

**R300 F3 evidence:**
- `TESTING.md:267` states twelve gmstep and two option-off controls. The code has exactly that (`receipts/campaign_inventory.txt`): 13 at `fc8a719f` plus the new addend-stage control.
- The trigger list names `.phc_slew_active_i` and `slew_rate_alignment`.
- `TESTING.md:484` describes the default/explicit split.
- `measure_test_evidence --check` passes (`receipts/measure_test_evidence_check.txt`).
- Hosted `docs` is `success`.

**R300 S1 evidence:**
- The tail is graded against the measured PHC advance (`sim_gmstep.cpp:419-450`). It is non-vacuous, and the added-stage control fails it.
- See F3 above. The residual one-sidedness is my S-A.

## Lens results (all applied at `b94f53cc`)

```text
[R301] PASS Conformance - issue #545 acceptance 1-3; assignment 545#5828714628 items 1-5; Makefile:12-21,48,72-88; TESTING.md:267-268,484; hosted run 36113401588 (rtl-full success, verilator-suites success, mmcm_servo 1159.1 s/1800 s), runs 36113401650/36113401578/36113401580 success - each round-2 item checked against the decision text: campaign explicit, deadline unchanged at scripts/run_all_suites.sh:247, no default check removed (hosted counts 100/8/113/90 = round-1 94/8/113/87 + U15 6 + S5 3)
[R301] PASS RTL - KL_mmcm_drp_servo.sv:88-91 (only delta, comment), unchanged logic re-read at :470-500,:589-723 (step/slew/guard streak, tally); datapath slew_rate_alignment milan_datapath.sv:2762-2767 unchanged since round 1 - header text checked against :709-715; tail exactness re-proved at this head by receipts/tail_probe_r1_rerun.txt and connected_tail_probe.txt (4 PHC-measured tail samples)
[R301] PASS Robustness - sim_phc_step.cpp:518-534 (step on the boundary sample of a held slew window), sim_main.cpp:555-579 (streak across slew + partial tail), :645-670 (reset during slew, saturation, mid-window step), receipts/connected_tail_probe.txt (shortened/lengthened release, extra addend delay) - checked against the documented once-per-window tally and the four-trip re-base rule
[R301] PASS Tests - slew_mutants.py:18-31,68-92 run per case (8/8, receipts/slew_case_*.txt); gmstep_mutants.py:112-142 --slew 3/3 + clean (receipts/gmstep_leg_and_slew_controls.txt); gmstep leg 58/58; unit 100, rails 8, step 113, slew 90; reviewer probes (coincide, tail, connected variants, round-1 mutants) - each new check shown able to fail for the defect it names; S-A recorded as SUGGESTION
[R301] PASS Docs - TIME_SYNC.md:180-186,238-244; CI_WORKFLOWS.md:158,162-170; TESTING.md:267-268,484; milan_dp/README.md:895-899; servo header :88-91; measure_test_evidence.py:596-600,622 with receipts/measure_test_evidence_check.txt (ratchet PASS); hosted docs run success - every statement checked against RTL, harness and receipts; S-B, S-C recorded as SUGGESTIONS
```

Additional detail per lens:

- **Conformance.**
  - Acceptance 1 (decision recorded on #387) and acceptance 2 (100 us / 200 ppm slew, LOCKED held, integrator within the stated bound, failing arms) stand as in round 1. The slew suite passes 90/90 locally and hosted.
  - Acceptance 3 (gates green): the exact-head hosted `rtl-fast`, `elaborate`, `docs` and `rtl-full` all concluded `success`. `rtl-full` includes `verilator-suites` and `yosys-portability`. `Physical gPTP` was skipped by design, and a skip is not hardware proof.
  - These hosted jobs tested merge ref `4bb43170`, which is `b94f53cc` merged onto live dev `a3d795ae`. That is hosted evidence, not the manager's candidate.
- **RTL.** There is no logic delta, so area is unchanged from round 1 (+7 LUT/+2 FF for the servo, reproduced in round 1). No port count or redundancy assumption was added.
- **Tests.**
  - U14's label now matches its mid-window stimulus.
  - U15 measures the post-slew 32/32/32/33-tick pattern.
  - S5 arms the coincidence with explicit arming checks.
  - The campaign rejects compilation failures and requires the named `[FAIL]` line.
  - The unit-mode markers (`slew_mutants.py`) accept a control only with rc=1 plus the named failure.
- **Docs.**
  - The inventory counts match the code (`receipts/campaign_inventory.txt`): gmstep 12 + option-off 2 = 14 controls with 3 by default; servo 6 defects + 2 positive.
  - The triggers name `.phc_slew_active_i` and `slew_rate_alignment`.
  - The suite-index row describes the split.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #545 acceptance; 545#5828714628 items 1-5; Makefile; TESTING rows; hosted runs 36113401588/650/578/580 (shard 2 suite log) | R301-2 | b94f53cc4e5dbfd9527ba666922a55804515165c |
| RTL | CLEAN | KL_mmcm_drp_servo.sv header and :470-723; milan_datapath.sv:2762-2767; round-1 tail probe rerun; connected tail probe | R301-2 | b94f53cc4e5dbfd9527ba666922a55804515165c |
| Robustness | CLEAN | S5, U15, U14, connected release/latency variants, round-1 mutants | R301-2 | b94f53cc4e5dbfd9527ba666922a55804515165c |
| Tests | CLEAN (S-A suggestion only) | slew_mutants.py 8/8; gmstep --slew 3/3 + leg 58/58; default servo 100/8/113/90; reviewer probes and mutants | R301-2 | b94f53cc4e5dbfd9527ba666922a55804515165c |
| Docs | CLEAN (S-B, S-C suggestions only) | TIME_SYNC, CI_WORKFLOWS, TESTING, milan_dp README, servo header, measure_test_evidence dispositions and --check | R301-2 | b94f53cc4e5dbfd9527ba666922a55804515165c |

## Real limits

- **Campaign split.** I ran the explicit campaign as eight separate invocations of its own `run_case()` (`scripts/slew_campaign_case.py`), one case per command, rather than as one `make slew-mutants` invocation. My per-command foreground limit is shorter than the whole campaign. The grading code, anchors and named failures are the campaign's own. The author's single-invocation log (`author-r2/timing-round2.log`, 1142.751 s, 8/8) covers the unsplit form.
- **Default target split.** I also split the local default target into its three sequential parts (`scripts/servo_default_part.sh`), and summed their wall clocks.
- **Timing conditions.** The local timings are from a shared host (load average about 13 on 16 CPUs) with the pinned 5.050, pinned to CPUs 8-9. The hosted figure is one sample.
- **Scratch trees.** All builds used a scratch copy of the head whose 890 tracked parent blobs were verified against the head (`receipts/make_tree.txt`). Its submodules were local clones checked out at the head's gitlinks, needed because the recipe runs `git ls-files` (`receipts/tree_submodule_git.txt`). `measure_test_evidence --check` ran in a scratch clone at the head.
- **Not run by me:**
  - the full parent, protocol-processor, gPTP, Yosys and builder banks;
  - the other `milan_dp` legs;
  - local docs/lint gates, for which I relied on the exact-head hosted `docs`, `rtl-fast` and `elaborate` successes;
  - area, because there is no RTL logic delta;
  - hardware and physical calibration. Simulation and skipped physical contexts are not hardware proof.
- **Receipts.** The receipts are raw output, except that host home-directory paths were replaced with `<home>` or `<pinned-simulator-root>`.
- **Clone restored.** The reviewed clone was never modified. HEAD, tree, index, worktree blob ids, modes, the four gitlinks, clean submodules and the empty ignored/untracked state all match the pre-run baseline (`receipts/restore_verification.txt`).

## Pending manager duties

- Build and validate the final current-dev candidate at the merge turn (source base `5b73d3f4`, live dev `a3d795ae`), including the deferred #508 text overlap.
- Accept the hosted and act evidence for this head. The hosted `rtl-full` shard evidence cited here is read-only.
- Obtain the internal reviewer's round on this head. Coverage is banked per head.
- Optionally act on S-B at merge (record the 1159.1 s hosted window and its margin).

R301-2 FINISHED
