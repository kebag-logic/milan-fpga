# Reviewer probes, R300-3 (#545 / PR #563)

`TREE` is a `git archive` extraction of the superproject at exact head
`92ad1687d84ff077f872719b4f1df601f82064d2`. The servo harnesses read no
submodule. `TREE_T` is a copy of `TREE` that differs only in the servo
Makefile's `--build -j 0`, changed to `-j 2` to respect the job cap.
`TREE_P` is a copy of `TREE` with `u15_short_pulse_probe.patch` applied.
`VERILATOR` is Verilator 5.050 (`receipts/tool_identity.txt`).

1. My round-2 streak mutants, unchanged. `reviewer_mutants_r2.py` is
   byte-identical to the R300-2 script (sha256 in
   `receipts/tool_identity.txt`). For each of `clean_unit`,
   `slew_discard_extends_streak`, `slew_discard_counts_as_guard_trip`,
   `slew_streak_reset_removed` and `step_streak_reset_removed`, two at a
   time (-j 4 each):
   `python3 reviewer_mutants_r2.py TREE WORK <name> $VERILATOR`.
   Receipts: `receipts/mutants_r2/`, `receipts/runlogs/mutants_r2/`.
2. The author's explicit servo campaign, graded by its own `run_case()`.
   `slew_campaign_part_r3.py` imports the head's `slew_mutants.py` and
   differs from the R300-2 driver only in reading the round-3
   `STREAK_MUTANTS` tuple. Four parallel foreground parts on `TREE_T`
   together cover `clean`, `clean_unit`, the five slew defects and the three
   streak defects. Receipts: `receipts/campaign/part_[a-d].log`.
3. Default servo target, stage by stage, on `TREE_T`: `make unit-build`,
   the rails `verilator` line of `run`, `make phc_step_build`, then the four
   simulations in parallel, one CPU each: `Vservo_sim`, `Vrails_sim`,
   `Vphc_step`, `Vphc_step +slew_suite`. Receipts: `receipts/servo_default/`.
4. Round-3 reviewer mutants, same mechanism as step 1:
   `python3 reviewer_mutants_r3.py TREE WORK <name> $VERILATOR` for every
   name in its table. Receipts: `receipts/mutants_r3/`,
   `receipts/runlogs/mutants_r3/`.
5. Short-pulse probe. On `TREE_P` (U15's slew replaced by a 1 ms pulse
   inside one window, so the discarded window's boundary sample is clean;
   the tail check is removed because there is no tail):
   `reviewer_mutants_r3.py TREE_P WORK clean_unit` and
   `... slew_reset_only_while_level_high`.
   Receipts: `receipts/u15_short_pulse/`, `receipts/runlogs/u15_short_pulse/`.
6. Static gates in the exact-head clone: doc style, doc paths,
   `docs_check`, em-dash against the base, `git diff --check` over the PR
   range, `lint_rtl.py --check`, `measure_test_evidence.py --check`.
   Receipts: `receipts/static_gates.log`,
   `receipts/measure_test_evidence_check.log`.
7. Hosted exact-head state, read-only: `gh run list --commit <head>`,
   `gh run view <rtl-full> --json jobs`, and the Verilator shard 2/5 job log.
   Receipts: `receipts/hosted_exact_head_runs.txt`,
   `receipts/hosted_head_verilator_shard2_job_108037083220.log`.
8. Clone integrity after all probes: `receipts/clone_integrity.txt`.
