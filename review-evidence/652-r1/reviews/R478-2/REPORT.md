[R478] POSITIVE - exact head d5e743440a56c77c43241879226b851abb3c62ac

# R478-2: internal cleared-context review of #652 / PR #660, round 2

- Head `d5e743440a56c77c43241879226b851abb3c62ac`, tree `9a481b19651cc534966c94be0a68e3487299e6e2`, in a detached clone. After the probes, the clone's bytes, modes, index and gitlinks were verified (`receipts/clone_integrity.txt`).
- Source base `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`. The lane merged dev `c0280fc008ef9c5c1650402a58bab3e47a92127b`, which is still the live remote dev tip (`receipts/merge_both_sides.txt`).
- All five lenses were applied at this head: Conformance, RTL, Robustness, Tests and Docs. Every lens is CLEAN.
- Open items: two new SUGGESTIONs (A and B). The round-1 SUGGESTIONs S1 (residual drift path, ruled no change) and S3 stay open. No BLOCKER, MAJOR, MINOR or RESIDUE is open.

## Reconstruction

I read these in order:

1. AGENTS.md and CONTRIBUTING.md (commit and merge rules, section 2).
2. The #652 issue body (acceptance 1 to 3).
3. The lane comment, the executor's STOP, and the ruling (option 1, items 1 to 4).
4. The round-1b REVIEW READY.
5. The round-2 assignment (#652 comment 5984666082) and the round-2 REVIEW READY (5985156837).
6. The PR #660 body.
7. `git diff 6c22d3ca..d5e74344` and the history. I read the lane's round-2 delta `ef236411..d5e74344` (4 commits) in full, and the merge `ef236411` separately.
8. The public evidence tree `7ac6966b` `review-evidence/652-r1` (the round-1b author packet).
9. #649's published inputs (`649-review-evidence` at `113a1fb9`, `review-evidence/649-r2/author/inputs`).

I read no private author material and no lane scratchpad. I wrote my verdict and ledger to `receipts/independent_verdict_before_prior_findings.txt` (22:52Z) before reading any prior finding text. Only then did I read R478-1 and R479-1 and resolve them below.

The other reviewer's round-2 comment (R479-2) was already posted on the PR by then, so I saw it when I listed the comments, after my own verdict was on file. One of its suggestions (S4, the summary rows) overlaps part of my SUGGESTION B, which I had found and recorded independently before.

## Delta under review (`2f0f5929..d5e74344`)

| Commit | Change | What I checked |
|---|---|---|
| `ef236411` | `--no-ff` merge of dev `c0280fc0` | The recorded tree `7d14122b` equals `git merge-tree --write-tree 2f0f5929 c0280fc0`. Each of dev's 12 files is identical to `c0280fc0` at the merge and at the head. Each of the lane's 12 files is identical to `2f0f5929` at the merge. The two sets do not overlap, and no later lane commit touches a dev file. Both sides are kept. |
| `b71979dc` | Check 14 moves to `scripts/nvm_allocation_table.py`. A row whose cell count differs from the header's is a finding (`:99-101`, with `strict=True` at `:104`). New controls `short_allocation_row` and `long_allocation_row` (`check_nvm_record_space.py:311-328`). | Twelve page edits through the gate's own seam, and ten mutants of the new module |
| `694e2b18` | `generate_shapes()` (`yosys_sweep.py:353`) is split out of `command_shapes`. Stand-in-builder arm `_shapes` (`yosys_sweep_selftest.py:81`). End-to-end `build()` arm `_selftest_build` (`resmap_models.py:477`). | r3, r11 and 14 further mutants |
| `94a12eb8` | `"cause"` pinned on both expected refusals (`sweep_plan.json:58,62`). `load_plan` refuses a refusal with no cause, and a cause on a variant expected to build (`yosys_sweep.py:127-134`). The step counts a refusal for a foreign cause (`:373,380`). | Eight planted plans at the head, plus two under the `2f0f5929` code |
| `d5e74344` | Each plan-validation arm requires its own refusal message (`yosys_sweep.py:852-870`). | Mutant m8 (the expectation check removed) is now red |

The lane's builder, RTL, gate 38, gate 24a, `ENDSTATION_BUILDER.md` and `SAVED_STATE_FASTCONNECT.md` are unchanged since `2f0f5929`. I re-ran them at this head anyway; see the Conformance and Tests rows.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE.

### A - SUGGESTION - Tests, Robustness - `syn/resmap/yosys_sweep.py:131`: no self-test arm holds the empty-cause refusal

- **Evidence.**
  - `load_plan` refuses a cause that is not a non-empty string. The real CLI does refuse `"cause": ""` (plan p7, rc 1, "an expected refusal must pin its cause"; `receipts/shapes/head-p7-empty-cause.log`).
  - No arm plants an empty cause. Mutant m9 (`not (isinstance(cause, str) and cause)` -> `not isinstance(cause, str)`) leaves `yosys_sweep.py --selftest` green (`receipts/resmap_mutants.txt`, `receipts/mut/m9-empty-cause-accepted.log`).
- **Impact.** If that conjunct regressed, an empty cause would be accepted. An empty cause is a substring of every line, so the cause pin would silently stop pinning. The code is correct at this head, and the tracked plan carries a non-empty cause.
- **Suggested outcome.** Add a fourth case to the `_selftest_plan` table: an expected refusal with `"cause": ""`, refused for "must pin its cause".
- **Verification.** Re-plant m9; the self-test turns red.

### B - SUGGESTION - Tests, Docs - `scripts/nvm_allocation_table.py:109,112`: two of check 14's arms have no negative control, and the summary rows are not required

- **Evidence.**
  - I planted ten defects in disposable git-backed copies of the head (`receipts/nvmmut/`). Each mutant was run under the unmutated check and the three allocation controls:
    - The round-2 width rule is held. n1 (the pre-fix shorter comparison), n2 to n4 (the width check removed or one-sided) and n5 (the messages swapped) are each caught by a control. So are the figure compare (n8) and the page seam (n9).
    - n6 (`if set(ALLOC) - seen:` -> `if False:`) passes all three controls, and so does n7 (the block comparison removed).
  - At this head the gate itself does catch both kinds of defect: a deleted group row gives "no row for ['NAME']" (`receipts/page_user-row-deleted.log`). Those two arms are round-1b code, and no `--mutate` control holds them.
  - Deleting the `records` row or the `highest id` row passes the gate, CHECK rc 0 (`receipts/page_records-row-deleted.log`, `receipts/page_highest-row-deleted.log`). This leaves no wrong figure on the page; the page just loses two figures. But `allocation_findings`'s docstring motivates the width rule with "a figure dropped from the table is not a figure checked", and that does not hold for a dropped summary row.
- **Impact.**
  - Regression only. A later edit that removes the block comparison or the row-presence check lands green.
  - A deleted summary row goes unnoticed.
  - No figure on the page at this head is unchecked or wrong.
- **Suggested outcome.**
  - Controls for a deleted group row and a wrong block figure.
  - Optionally, require the `records` and `highest id` rows as `ALLOC` groups are required.
- **Verification.** Re-plant n6 and n7; a control turns red. A deleted `records` row gives rc 1.

## Per-lens results (clean lenses in findings format)

```text
[R478] PASS Conformance - receipts shapes_real.log, shapes_real_outcomes.json, bank.log (gate 38, gate 24a), byte_identity.log, byte_identity_rtl.log, reproduce_649_tables.log, page_tables_*.log, nvm_space.log, merge_both_sides.txt; sw/builder/endstation_builder.py:2689-2713; hdl/milan/KL_nvm_backend.sv:247,293-295 - checked against #652 acceptance 1-3, ruling items 1-3 and round-2 items 1-5:
  - Acceptance 1. The real shapes step refuses both 235-name variants with one line naming 235, 128 and "N_NAME_MAX_C, hdl/milan/KL_nvm_backend.sv:247". Gate 38 reports the capacity read from that line, 128 built, and 129 and 235 refused before any write.
  - Acceptance 2. Gate 38 turns 9/9 planted defects red. Its RTL arm ran under the pinned Verilator: it elaborates at 128 and refuses at 129.
  - Acceptance 3. All five tracked configurations give 50 artifacts each, byte-identical at base and head (diff -r, sha256 lists). With --write-rtl --write-fragment in a fresh copy per configuration, each rewritten tracked file is byte-identical at base and head, and the sets of touched files are equal. The shipping 1x1 TDM8 rewrites none.
  - Ruling 2. The shapes step gives 7 built and 2 refused as expected, rc 0. From #649's published inputs, the head page equals a fresh generation (so does the base page). The page's 26 tables are byte-identical to round 1b's. Against the base, only guard-refusals and datapath-marginals differ.
  - Ruling 3. Check 14 is clean: section 4.2 reads 39/107, 54/164 and 0xA6/0xEA, the derived figures.
  - Round-2 items. Item 1: short and long rows refused, and both controls are present and red. Item 2: r3 and r11 are red (Tests row), and the PR body's description of the arms matches the code. Item 3: a foreign cause fails the step (plans p1 and p2 rc 1; rc 0 under the 2f0f5929 code). Item 4: S1 is stated in the body and S3 is listed open. Item 5: --no-ff merge, both sides kept.
[R478] PASS RTL - hdl/milan/KL_nvm_backend.sv:240-247,293-295 (head vs base); receipts guard_parity.log, suite_nvm_backend.log, merge_both_sides.txt - the pinned Verilator 5.050 (wrapper sha256 905795b9..., reports "Verilator 5.050 2026-07-01 rev v5.050"):
  - Lint-only -Wall at N_NAME_P 0, 1, 99, 128, 129 and 235 gives the same rc and the same g_refuse_names message at base and head.
  - The nvm_backend suite gives 751 checks (541 + 210), 0 failures, with its 4 negative controls red.
  - The lane changes no RTL after d33bdc3d.
  - The merged dev RTL (KL_crf_rx.sv, milan_datapath.sv) is byte-identical to c0280fc0. It is not part of this PR's diff against dev.
[R478] PASS Robustness - syn/resmap/yosys_sweep.py:127-134,353-382; scripts/nvm_allocation_table.py:52-113; receipts shapes/*.log, page_*.log, plans/*.json - checked:
  - Every surprise fails the step: a refusal for a foreign cause (p1 both variants, p2 one), no expectation marks (p3), an expected refusal that builds (p4). load_plan refuses a refusal without a cause (p5), a cause on a built variant (p6) and an empty cause (p7). The tracked plan stays rc 0 (p0).
  - Check 14 catches a dropped last cell and a dropped middle cell in the user-name row, an extra cell, a blank 8x8 cell, a short records row, a short highest-id row, a short configuration-index row and a deleted group row. The unedited page stays clean.
  - The deleted summary rows are SUGGESTION B.
[R478] PASS Tests - receipts resmap_mutants.txt, mut/*.log, nvmmut/*.log, nvm_space_self.log, self_*.log, bank.log, suite_nvm_backend.log - checked:
  - The round-1 bar. r3 (failures += outcome == "failed") turns yosys_sweep.py --selftest red: "an unexpected refusal exited 0, not 1" and "an expected refusal that builds exited 0, not 1". r11 (by_builder -> pass) turns resmap_models.py --selftest red: "guards.by_builder is None". Both were planted with the round-1 mutate_module.py, unchanged (sha256 e0a4c996...).
  - Unmutated self-tests stay green.
  - 14 further resmap mutants: 13 red and 1 survivor (m9, SUGGESTION A). The foreign cause not counted (m1), the cause test inverted (m2), the cause never checked (m3), the step always passing (m4), the refusal line not recorded (m5), each load_plan check removed (m6, m7, m8), a crash read as a refusal (m10), the stand-in builder bypassed (m11), by_builder always written (m12) and by_builder naming the wrong points (m13) are each red. m14 was recorded for information only and also raised.
  - Allocation mutants: 8 of 10 caught, n6 and n7 not (SUGGESTION B).
  - The record-space --self-test turns 21/21 controls red.
  - The five resmap self-tests give rc 0.
  - The builder bank ends "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11, no mf48 tree on this host). Gate 24a (d) and (e) each turn 2/2 controls red, and gate 38 turns 9/9.
[R478] PASS Docs - docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md:91; syn/resmap/sweep_plan.json description; syn/resmap/yosys_sweep.py:34-64 docstring; syn/resmap/yosys_sweep_selftest.py:1-19; scripts/check_nvm_record_space.py:88-92; scripts/nvm_allocation_table.py:1-13; docs/design/SAVED_STATE_FASTCONNECT.md:269-311; docs/ENDSTATION_BUILDER.md:101-104,754-775,1108-1119; the PR #660 body; receipts docs/*.log - checked:
  - Each round-2 statement matches the code it describes: the cause pin and its failure, the stand-in arm's five cases, the end-to-end build() arm, the width rule and its three controls, and the moved modules with r3 and r11 left unmoved.
  - The PR body's disclosure that the refusals table's arm reads a hand-made by_builder is accurate.
  - The section 4.2 figures are bound by check 14. The D8 arithmetic is 8 x (16 + 1 + 72) = 712.
  - Docs gates, all rc 0: docs_check, gen_toc --check, check_doc_paths, check_doc_style, check_archive, and check_em_dash against both 6c22d3ca (0 findings over 179 added lines) and c0280fc0 (0 over 66), run with the Markdown renderer at the pinned requirement versions. Ratchets, all rc 0: check_py_idiom ("long module: 10 <= 10"), check_hygiene and measure_test_evidence.
```

## Prior public review findings (read after my verdict was on file)

| Finding | Status at this head | Evidence |
|---|---|---|
| R478-1 F1 (MINOR; Tests, Docs): the shapes fail-closed comparison and the by_builder producer were held by no self-test | **Resolved** | r3 and r11 each turn their self-test red. The arms are `yosys_sweep_selftest.py:81` `_shapes` (5 cases) and `resmap_models.py:477` `_selftest_build`. The PR body now says what each arm holds and discloses the hand-made `by_builder` in the table arm. |
| R479-1 F1 (MINOR; Robustness, Tests): check 14 passed a 4.2 row that lost a column figure | **Resolved** | A short row and a long row are each refused with a named finding (`page_user-row-short`, `page_user-row-long`, `page_user-row-middle-cell-lost`). The `short_allocation_row` and `long_allocation_row` controls are red in `--self-test`. The unmutated gate is rc 0. Pre-fix mutant n1 is caught. |
| R478-1 S2 / R479-1 S2 (SUGGESTION): `expect: refused` accepted any refusal | **Resolved (taken)** | The cause is pinned. Plans p1 and p2 give rc 1 at the head and rc 0 under the `2f0f5929` code. The stand-in's foreign-cause case is red under m1 and m3. |
| R478-1 S1 / R479-1 S1 (SUGGESTION): `ALLOC["NAME"] = (0x80, 128)` | **Retained, open as a suggestion** | Ruled no change (#652 comment 5984666082). The PR body states the judgment. The residual drift path (the RTL capacity and gate 38's pin moving without `ALLOC`) is still open, as the body says. |
| R478-1 S3 / R479-1 S3 (SUGGESTION): `ID_NAME_C + N_NAME_MAX_C` unchecked | **Retained, open as a suggestion** | Listed open in the PR body's Known limitations. |

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Real shapes step and outcomes; gate 38 and 24a in the bank; 5-config byte identity, with and without `--write-rtl`/`--write-fragment`; #649 page re-derived from published inputs; check 14 against section 4.2; round-2 items 1-5; merge parents and tree | R478-2 | `d5e743440a56c77c43241879226b851abb3c62ac` |
| RTL | CLEAN | `KL_nvm_backend.sv` guard parity at 6 values under the pinned Verilator 5.050; nvm_backend suite (751 checks); merged dev RTL identical to `c0280fc0` | R478-2 | `d5e743440a56c77c43241879226b851abb3c62ac` |
| Robustness | CLEAN | 8 planted plans through the real shapes step, and 2 under the `2f0f5929` code; 12 page edits through check 14's seam | R478-2 | `d5e743440a56c77c43241879226b851abb3c62ac` |
| Tests | CLEAN | r3 and r11 re-planted; 14 further resmap mutants; 10 allocation mutants; record-space `--self-test` (21 controls); 5 resmap self-tests; full builder bank; nvm_backend suite | R478-2 | `d5e743440a56c77c43241879226b851abb3c62ac` |
| Docs | CLEAN | Round-2 docstrings, plan description, #649 page line 91; section 4.2; ENDSTATION_BUILDER D8 and section 4; PR body; docs and ratchet gates | R478-2 | `d5e743440a56c77c43241879226b851abb3c62ac` |

## Commands and results (scripts under `scripts/`, receipts under `receipts/`)

Each job ran with its own log and rc file (`scripts/launch.sh`, `scripts/wait_rc.sh`). Commands marked "clone" ran in the review clone, which they leave unmodified. The others ran in scratch exports of base, round-1b and head made by `scripts/export_tree.sh` at the pinned submodule gitlinks. The record-space mutants and the nvm_backend suite ran in a git-backed copy of the head export (`scripts/make_git_copy.sh`).

| Check | Result |
|---|---|
| `test_builder.py --require-rv32` (clone, pinned Verilator on PATH) | rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11) |
| `check_nvm_record_space.py` and `--self-test` (clone) | rc 0; rc 0 with 21/21 controls red |
| `scripts/nvm_page_probe.py`, 12 cases (clone, in memory) | 9 caught, unedited control clean; records-row, highest-row and reserved-row deletions pass (B) |
| `scripts/nvm_alloc_mutant.py`, n0-n9 | Control clean with 3/3 caught; n1-n5, n8, n9 caught; n6, n7 not (B) |
| `yosys_sweep.py shapes` (clone, work in scratch) | rc 0: 7 built, 2 refused as expected, with the pinned cause |
| Planted plans p0-p7 (clone CLI); p1, p2 under `2f0f5929` code (`scripts/shapes_probe_rev.py`) | p0 rc 0; p1-p7 rc 1; under 2f0f5929, p1 and p2 rc 0 |
| `scripts/run_resmap_mutants.sh` (via `mutate_module.py`, in memory) | 2 controls green; r3, r11 red; 13 of 14 more red; m9 survives (A) |
| Resmap self-tests (5) | rc 0 each |
| `scripts/byte_identity.sh` | 5/5 rc 0 at base and head; 50 = 50 files; diff -r rc 0; sha256 lists identical |
| `scripts/byte_identity_rtl.sh` | rc 0; every tracked rewrite identical at base and head |
| `scripts/reproduce_649_tables.sh` | Head and base: "every table equals a fresh generation" |
| `scripts/page_tables_diff.py` | 2f0f5929 vs head: 26/26 unchanged; base vs head: 24/26 |
| `scripts/guard_parity.sh` | Identical verdicts and messages at base and head |
| `make -j16 -C tb/verilator/nvm_backend` | rc 0; 751 checks; 4 negative controls red |
| Docs and ratchet gates (clone) | All rc 0 |
| Clone integrity | HEAD, HEAD tree and index tree are `9a481b19...`. 0 status lines (ignored included). `ls-files -s` equals `ls-tree -r HEAD` (1015 entries). Gitlinks: external efeb541a, gptp-processor 5dce647a, protocol-processor 631eeb34, third_party/verilog-axis 48ff7a7e; each initialised submodule is at its pin and clean. Caches and ignored outputs created by this review's runs were removed. |

Each `page_*.rc` file is the probe wrapper's exit status. The gate's verdict is the `CHECK rc=` line inside each `page_*.log`.

## Real limits

- **Not run by me:** the full Verilator sweep, the Yosys portability bank, the parent/PP/gPTP banks, nvm_cosim, Vivado, hardware, Docker/act and host act_ci (out of scope for this round).
- **Gate 11 NOT RUN:** the builder bank's Arty mf48 calibration gate did not run on this host. Its verdict does not cover that arm.
- **#649 page re-derivation:** I applied the head `summary` rule for builder-refused points to #649's published `summary.json`, using this round's own shapes outcomes. I re-priced no point and re-ran none of #649's Yosys or Vivado steps.
- **Byte identity, 50 files per side:** I compared the 50 files the builder writes and the tracked-tree rewrites. The author's 120 also include in-memory dumps that I did not regenerate.
- **Hardware:** physical calibration NOT RUN. Field skips are not hardware proof.
- **Hosted CI:** snapshot at 2026-10-04T22:43Z, exact head (`receipts/hosted_checks_snapshot.txt`).
  - Success: bdd-conformance, changes, docs-check-no-git, full-ci-gate, verilator-lint, wire-accountability, Verilator shard 3/5, and Yosys shards 0-3/4.
  - In progress: docs-check, elaborate, yosys-elaboration, and Verilator shards 0, 1, 2 and 4/5.
  - Skipped: Physical gPTP (nightly and manual), which is not an executed job.
  - I made no hosted acceptance judgment.

## Pending manager duties

- Hosted acceptance on the exact head, including the contexts still in progress, and the act-first local replica.
- The final current-dev candidate merge build and validation (source base `6c22d3ca`, live dev `c0280fc0`), and post-merge containment.
- The external review's verdict and the maintainer's merge authorization.
- Optionally route SUGGESTIONs A and B, and the still-open S1 drift path and S3.

R478-2 FINISHED
