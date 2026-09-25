# Reviewer probes, R300-2 (#545 / PR #563)

`TREE` is an exact-head extraction of `b94f53cc4e5dbfd9527ba666922a55804515165c`,
made with `git archive` of the superproject and of each pinned submodule
(`gptp-processor` 5dce647a, `protocol-processor` 09f9bf38,
`third_party/verilog-axis` 48ff7a7e). For the `milan_dp` recipe, the two
processor directories were given throwaway local Git repositories holding
exactly the archived files. The file counts match the pinned commits:
224 files in `protocol-processor` and 104 in `gptp-processor`.
`VERILATOR` is Verilator 5.050 (`receipts/tool_identity.txt`).

1. Default servo target, stage by stage. `TREE_T` is a copy of `TREE`. It
   differs only in the servo Makefile's `--build -j 0`, changed to `-j 2` to
   respect the job cap. Build all three harnesses with
   `make unit-build`, the rails `verilator` line of `run`, and
   `make phc_step_build`. Then run the four stages, each pinned to one CPU:
   - `obj_dir/Vservo_sim`
   - `obj_rails/Vrails_sim`
   - `obj_phc/Vphc_step`
   - `obj_phc/Vphc_step +slew_suite`

   Receipts: `receipts/servo_default/`.
2. The author's explicit servo campaign, graded by its own `run_case()`.
   Run `python3 scripts/slew_campaign_part.py TREE_T WORK <case>...` in four
   parts that together cover `clean`, `clean_unit` and all six defects.
   Receipts: `receipts/campaign/part_[a-d].log`.
3. My round-1 mutants, unchanged. `scripts/reviewer_mutants_r1.py` is
   byte-identical to the R300-1 script
   (`receipts/r1_scripts_identity.txt`). Run
   `python3 scripts/reviewer_mutants_r1.py TREE WORK <name> $VERILATOR`.
   Receipts: `receipts/mutants_r1/`.
4. New streak mutants. Run
   `python3 scripts/reviewer_mutants_r2.py <tree> WORK <name> $VERILATOR`,
   using the same mechanism as step 3.
   - On `TREE`: receipts in `receipts/mutants_r2/`.
   - On `TREE` with `scripts/u15_one_trip_arming.patch` applied, which arms
     U15 with one guard trip instead of two: receipts in
     `receipts/u15_one_trip/`.
   - On `TREE` with `scripts/u15_tail_gap_print.patch` applied, which only
     prints the gap from the tail discard to the first fresh trip: receipts
     in `receipts/u15_tail_gap/`.
5. Connected gmstep leg and the author's connection controls, unchanged.
   Run `VERILATOR_JOBS=6 make -C TREE/tb/verilator/milan_dp gmstep`, then
   `python3 gmstep_mutants.py --slew`. Receipts: `receipts/gmstep/`.
6. The gmstep oracle probe. Apply `scripts/gmstep_oracle_print.patch`, which
   prints counters and the samples around release and changes no check. Then
   run `python3 scripts/gmstep_oracle_probe.py TREE_G WORK <case>...` with
   the cases `clean`, `addend_delay_1`, `addend_delay_2`, `tail_3`, `tail_5`
   and `level_stuck_high`. Receipts: `receipts/gmstep/oracle_probe_[ab].log`
   and `receipts/runlogs/gmstep_oracle/`.
7. My round-1 PHC latency probe, unchanged
   (`scripts/latency_probe_r1/`, byte-identical). Tail lengths 4, 3 and 2.
   Receipt: `receipts/latency_probe.log`.
8. Static gates, run in the exact-head clone:
   - `measure_test_evidence.py --check`
   - `lint_rtl.py --check`
   - doc style, doc paths and `docs_check`
   - em-dash against the base
   - `git diff --check`

   Receipts: `receipts/*.log`. Clone integrity after the probes:
   `receipts/clone_integrity.txt`.
