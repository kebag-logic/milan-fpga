[A516] REVIEW READY (round 4)
Commit: `79e53831a4f623a594f22765be1d05dffeb696a7` on local branch `234-area-baseline`. That is five one-line commits on round 3's `b5894838`: no rebase, no amend, and not pushed, as assigned. `b5894838..79e53831` touches 6 files: the gate, its self-test and mutants, the hierarchy parser it imports, `AREA_BUDGET.md` and the recipe. No RTL, processor, interface, workflow, baseline-JSON, tolerance, floor or ceiling change, and no Vivado run.

Changed, by assignment item (5969446300):
1. One barrier.
   - Everything in `main()` after argument parsing is inside one `try`. Any exception, expected or not, prints `NOT COMPARABLE: <reason>` and exits 2. Exit 1 comes only from `judge()`.
   - Every printed line goes through `emit()` as printable ASCII, other characters escaped as `ascii()` writes them, so printing cannot raise (R447-3 F1).
   - The self-test's command line now prints into an ASCII-only strict stream. Arms plant an exception carrying a lone surrogate and an escape character in seven gate functions; each exits 2. Mutants `barrier`, `ASCII output` and `printable ASCII output` are killed.
   - A 20,000-case generative run at `e6710d13` found one path outside the barrier: an endpoint the baseline does not hold left through argparse. `39e9329b` moved it inside, with an arm and a killed mutant.
2. Names. The baseline and the image manifest are read as strict JSON: every key is 1 to 128 of `A-Za-z0-9_.:/-`, and a repeated key is refused (R447-3 S1). Anything else exits 2, naming the key.
   - One deviation, for a decision if wanted: sub-block scope names may also hold `[` and `]`. The committed baseline's five scopes `u_pp/g_rx_pool[0..5].u_rx_slots` carry Vivado's generate index, so the literal class would make A's endpoints exit 2. Endpoint, field and figure names are held to the class exactly; arms and killed mutants cover both sides.
3. One guarded converter per number type.
   - `whole()`: 1 to 15 ASCII digits, so every whole number is below 2**53 and its float is exact and finite. It reads every JSON integer and every route status (now inside `routing()`'s `try`), timed-endpoint, utilization and hierarchy count (R446-3 F2, R447-3 F2).
   - `real()`: finite after conversion, restoring R446-3 F1's check. It reads the slack, the half BRAM tile, every JSON decimal and every budget cell.
   - The self-audit cites the converter at every site (HANDOFF R4.3; PR body "Round 4").
4. Arms and killed shipped mutants for R446-3 F3's seven, R447-3 F3's six and R447-3 S2's two. R446-3's two uncounted survivors (an upper-case digest, a slack without a fraction) are covered too.
5. Seeded generative test. `mutate_json()` and `mutate_report()` change the baseline or one report at random: types, values, keys, sizes, Unicode, digits, rows, truncation, bytes that are not UTF-8, and missing files. `fuzz()` runs each case through `main()`. Every case must exit 0, 1 or 2 with no traceback, and every case that breaks a documented shape must exit 2.
   - Self-test: 500 cases at seed 234, 0 failures.
   - `--fuzz`, seed 234: 20,000 on A's real route (13,505 shape-breaking, all exit 2), 20,000 on the fixtures (12,781) and 5,000 on A's real standalone 1x1 (3,140). 0 failures, no traceback.
6. Docs. `AREA_BUDGET.md` and the recipe state the contract as it holds by construction. R447-3 R1: the census file is in this round's packet as `receipts/round4/armq-census.tsv` (same sha256 as round 3's), and the PR body row names it and how to re-derive it.

Validation at `79e53831`, worktree clean:
- 43 of 43 touched gates rc 0, with GNU Make 4.3 first on PATH and no pipes. They include:
  - the gate self-test (247 arms and 500 generated cases), the mutant campaign (158 of 158 killed; control passes) and `check-baseline` (3 endpoints);
  - the pp_baseline self-tests and its 32 mutants;
  - the `ci_scope` and `ci_events` checks;
  - the docs gates, including `make -C gptp-processor docs`;
  - the Python ratchets.
- R446-3's and R447-3's own `run_gates.sh`: 31 of 31 and 31 of 31 jobs rc 0.
- Real data: A route, 1x1 and 8x8 rc 0, with route status complete. B route rc 1 (+625 LUT). B 1x1 and 8x8 rc 0. The 10 ns control rc 2.
- Every probe both reviewers published in rounds 1 to 3, rerun unchanged (36 runs), tabled in the PR body and HANDOFF R4.5:
  - R446-3: `probe_r3_mutants` 20 of 20 killed. `probe_r3_numbers`, `probe_r3_untested` and `probe_r447_2_cases`: 0 cases off the contract. Hierarchy equivalence: 0 mismatches.
  - R447-3: `extra_mutants_r3` 13 of 13 killed. `probe_text` cases A to F rc 2 in both columns, no traceback. `probe_bigint` (B and A) rc 2 in both columns. `probe_gaps` 6 of 6 rc 2. `hier_compare` 0 differing. `armq_count` A 1,153 and B 1,260.
  - Earlier rounds, as before:
    - R446-1: `probe_gate_cli` 116 of 117 (the `inf` literal); `probe_gate_mutants` 21 killed, 2 not applied; `probe_pr_mutant_reasons` 149 of 149 ARM; `reconcile.py` its 2 hard-coded sentences.
    - R447-1: `probe_cli` 54 of 54; `extra_mutants` 16 killed, 2 not unique.
    - R446-2: route probe 15 of 16 (S1); extra mutants: every applicable one killed, 3 not applicable.
    - R447-2: `classify_mutants` 145 ARM, 4 ESCAPED, 0 survived; policy 107 of 107; route probes 15 of 15 and 14 of 15 (B's +625).
  - Each not-applied reviewer mutant maps to a killed shipped mutant.

Acceptance criteria (#234, as ruled in 5967852698 and 5967924270): unchanged from rounds 2 and 3.
1. Met at 50 MHz.
2. Not met at A, with the levers in #232, #230 and #639.
3. Documented; NFR-RES-01 is to be met by #640.
4. The hosted half is wired. The Vivado half runs in the manager's merge bank.
5. Outside this step.

Open risks/questions:
- Item 2's deviation for scope names, above.
- The `--fuzz` driver (about 85 lines) sits in the gate module and the generators in the self-test. Both reviewers' mutant probes copy exactly three modules, and the self-test alone would exceed the repository's 1,000-line module ratchet.
- Behaviour added beyond the findings, each with an arm and a killed mutant: the record's own field set is closed; the image manifest is read as strict JSON; `record --write` validates before writing; an unknown endpoint is refused inside the barrier.
- The barrier cannot report a failure of standard output itself, such as a closed pipe.
- Packet for publication: HANDOFF.md, PR-BODY.md, receipts/round4/ (gates, probes, real data, fuzz runs and replays, the kill matrix, both reviewers' gate runners, armq-census.tsv) and the round-4 scripts under scratch-scripts/.
