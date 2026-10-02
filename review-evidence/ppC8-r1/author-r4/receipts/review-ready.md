[A504] REVIEW READY at head `bd86f6466baa77113eea2266c00044c3a29678f2` (branch `c8-descriptor-lint`, two commits on `97f6eac`; local, not pushed).

Round 4 (merge only, 5958629222), in the assignment's order:
1. **Merge** (`3bfc7c6`): `main` `631eeb34` (#142, P141), merged with `--no-ff` and keeping both sides.
   - **07 §3.1 L6** takes P141's statement whole: the Milan v1.2 §5.3.3.6 set is a minimum; one INPUT_STREAM source per AAF input is allowed beside the CRF input's (IEEE 1722.1-2021 §7.2.9.2, Table 7-17); the order is INTERNAL 0, CRF 1, AAF k at 2 + k; the list may hold up to 216 entries; membership is §7.2.32's test; and BAD_ARGUMENTS is Table 7-141's. The row keeps the lint's list shape (at 76, `76 + 2 × count`) and its Checks column, and adds: "neither the processor nor the lint reads an order", and that 216 is the 508-octet L12 bound (a probe shows 216 sources pack and 217 are refused).
   - **REQ-MDL-005** takes P141's clause and requirement. Its Arch cell names the processor's range check and lint L6, "which accepts that set and reads no order". L6 and REQ-MDL-005 now read as one statement.
   - So that L6 and its check cite one clause, `domain-source-identity` now credits IEEE 1722.1-2021 §7.2.32, not §7.4.23.1. Only that refusal's parenthesis changes.
   - **L6 positive case** (`bd86f64`): no rule changes, because the lint already accepted the set. `ConformingModelTest.test_a_source_per_aaf_input_beside_crf` packs a CLOCK_DOMAIN of INTERNAL 0, CRF 1 and one INPUT_STREAM per AAF input at 2 + k: eight AAF inputs, ten sources, D3C's 8x8 shape. Five stricter L6 readings were planted. Without the test the gate kills 1 of 5; with it, 5 of 5.
2. **Re-measured** at `bd86f64`:
   - `git apply --check`: 207 of 207 campaign patches apply.
   - The packer gate passes 59 tests. The suppression driver kills 56 of 56, and its log equals round 3's.
   - `run_suites.sh` rc 0: 33 suites, 1,019,127 checks, 0 failing. Only `pp_top` moves, +17, main's D3C checks.
   - `lint_hdl.sh`, `make check`, `gen_matrix.py --check` and `git diff --check` are all rc 0.
   - The reviewers' round-3 plant scripts, run unchanged, give the same results as at `97f6eac`. R435-3's S1 plant still survives; S1 was not taken.
   - The five parent models pack byte-identically to round 3 at dev `cdf49d1a` and at #634 `0b066b6e`. At `0b066b6e` they carry #629's sources: 3, 6, 6, 3 and 10, in the order INTERNAL 0, CRF 1, AAF k at 2 + k. Four pack with no waiver, and `ax7101_8x8` packs only with its #584 waiver. The C8 and C4C6 patches are unchanged.
3. **Parent consumer set (16)** at dev `cdf49d1a`, with the C4C6 patch and then the C8 patch: all rc 0. The builder test reports one arm not run, gate 11, which needs a board report.
   - The first `milan_dp` run, beside the builder test, failed (rc 2). Builder gates 23j/23k briefly take away `gen/lwsrp_csr_defaults.svh`. Re-run alone, `milan_dp` passes with 9 RESULT PASS. The failed run is recorded in HANDOFF.

PR-BODY.md has a "Round 4" section, and the four Closes lines stand. HANDOFF.md, PR-BODY.md, both patches and the receipts are in the lane output directory.
