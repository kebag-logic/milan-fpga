[R742] POSITIVE - exact head 430a077c0e9a5a42062103742a8f3f1b8bacc6b8

External independent review, round R742-6, of PR #815 (issue #797, D0 documentation audit lane).
Head `430a077c0e9a5a42062103742a8f3f1b8bacc6b8`, tree `7775f0a1d507e79a6106965c2353a782a046012b`.
Delta judged: `e8ec8d20..430a077c`. That is merge `626d367f` (dev `604899c0`, PR #836) and regeneration commit `430a077c`.

No BLOCKER, MAJOR or MINOR finding is open. All five lenses are clean at this head. Two wording RESIDUEs are retained for the manager's residue checklist. One of them, the PR body's hosted-status line, has recurred. Earlier SUGGESTIONs are retained, and this round adds one SUGGESTION outside the delta.

## Method and order

1. AGENTS.md, then issue #797's scope, rules and acceptance (`gh issue view 797`). I read the acceptance bullets and scope item 6, "every existing docs gate stays green".
2. Delta history, merge structure and a mechanical remerge.
3. Generator regeneration at the merge and at the head, and the gates that read the JSON and the command table.
4. Hosted check-runs at the exact head, read only.
5. Prior public findings on PR #815, read only after my independent pass. My preliminary verdict was written first: `receipts/preliminary_verdict_before_prior_findings.txt`. I did not read the other external reviewer's report at this head.

## Delta facts (each with its receipt)

- **One merge base.** `git merge-base HEAD 604899c0` = `604899c08ff1cd1830e1dd08b733109ef852400c`. The merge parents are `e8ec8d20` (lane) and `604899c0` (dev). Both commit subjects are one line with no trailers.
- **The merge is mechanical, so both sides are kept.** `git merge-tree --write-tree e8ec8d20 604899c0` gives tree `070213ea`, which equals the recorded tree of `626d367f`, and rc is 0, with no conflict. Of the 15 files dev changed since `e61a4afa`, 14 are byte-identical to dev in the merge. The one combined file is `ci/image/command-table.json` (`receipts/merge_remerge.txt`).
- **Command table, three-way at leaf level** (`table_threeway.py`, `receipts/command_table_threeway.txt`, rc 0):
  - **Lane side:** 6 leaves added, none removed: the `git -C <runtime> ls-files -z` row, the two `scripts/docs_inventory.py --check/--selftest` command rows, and the `scripts/docs_inventory.py` declaration with its class, reason and sha256.
  - **Dev side:** 6 leaves added or changed: re-pinned digests of `ci_gate_workflows_selftest.py`, `ci_scope_history.py` and `run_litex_sims.sh`, plus the new `ci_litex_legs.py` declaration.
  - **Result:** all 12 are in the merge, and the merge adds no leaf or value of its own. That matches the PR body's "the lane's inventory rows and dev's four PR #836 rows, and nothing was re-pinned by hand".
- **The lane's own diff against dev did not change.** For the 9 lane files other than the generated page, the +/- lines of `git diff 604899c0 430a077c` equal those of `git diff e61a4afa e8ec8d20` (`receipts/lane_diff_vs_dev_r5_vs_r6.txt`). The only lane-side content change in round 6 is `docs/DOCUMENTATION_AUDIT.md`. The six gitlinks equal dev's (`receipts/gitlinks_dev_vs_head.txt`). `git diff --check` gives rc 0 against both the merge base and `e8ec8d20`.
- **The page was regenerated only by the generator.**
  - At the merge `626d367f`, `--check` gives rc 1 (STALE, 6 lines, first difference at line 30). `--write` then `--check` give rc 0, and the written page is byte-identical to the `430a077c` blob (`receipts/docs_inventory_regen_from_merge.txt`).
  - At the head, `--check` gives rc 0. A fresh `--write` gives sha256 `d277b6b2…`, identical to the committed page, and then `--check` gives rc 0 (`receipts/docs_inventory_check_head.txt`, `receipts/docs_inventory_write_check.txt`).
  - `scripts/docs_inventory.json` and `scripts/docs_inventory.py` are unchanged in the delta. The JSON is the curated input, not generated output.
- **The figures follow the generator's rules.** `CI_WORKFLOWS.md` goes from 3414 to 3624 lines (+210) and `TESTING.md` from 1927 to 1935 (+8), measured with `wc -l` at `e8ec8d20` and `430a077c`.
  - Current: 73,277 + 210 = 73,487.
  - Stale (TESTING.md is stale through D0-057): 10,630 + 8 = 10,638.
  - Total: 91,909 + 218 = 92,127.
  - Page and status counts are unchanged: 213 pages, 176/16/0/21. There are 76 finding rows, 11 of them copies, counted at the head.
  - D0-057's copy row moved from 1810 to 1818. The quoted statement is at `docs/testing/TESTING.md:1818` at the head.
  - No row was added or dropped. The six changed lines are the only diff of the regeneration commit.
- **The gates that read the JSON and the table pass at the head.**

  | Gate | rc |
  |---|---|
  | `pp_srcs.py --check --selftest` (rtl-fast verilator-lint step 8) | 0 |
  | `docs_inventory.py --selftest` (50 controls) | 0 |
  | `docs_check.py` with Git | 0 |
  | No-Git docs job on a fresh `git archive` of the head (`docs_check.py`, `check_feature_status.py`, and the inventory `--check` through the filesystem walk) | 0 |
  | `ci_gate_workflows.py --check` and its selftest | 0 |
  | `ci_litex_legs_selftest.py` | 0 |
  | `check_doc_paths.py` | 0 |
  | `gen_toc.py --selftest/--verify-anchors/--check`, with the pinned cmarkgfm 2025.10.22 / html5lib 1.1 renderer | 0 |
  | `check_em_dash.py --base 604899c0`: 534 added lines, 0 findings | 0 |
  | `check_em_dash.py --base e8ec8d20`: 260 added lines, 0 findings | 0 |
  | `check_doc_style.py` and its selftest | 0 |
  | `check_solution_docs.py` and its selftest | 0 |
  | `check_baremetal_only.py --check` and its selftest | 0 |
  | `check_feature_status.py` | 0 |
- **The image command-table checker adds nothing of the PR's own.** `ci_tool_inventory.py --check` refuses here before any comparison because no checksum-pinned Bash parser is installed (`receipts/ci_tool_inventory_{head,dev}.txt`). I therefore recomputed its digest arm independently (`table_digests.py`).
  - Head with submodules: 116 ok, 34 stale, 1 missing (`tb/verilator/render_setpoint/mutants.py`). That is the PR body's "35 stale or missing" and the 34 + 1 in the maintainer's decision. `sw/builder/endstation_builder.py` is among the 34 stale.
  - Head and dev in submodule-less clones have identical stale and missing sets. The head has one more ok entry, the lane's `scripts/docs_inventory.py`, whose sha256 `2756e5b5…` matches the file.
  - This is dev's accepted failure tracked in #838, not a finding (`receipts/table_digests_*.txt`).
- **Comment rule.** The delta's code is entirely dev-side (byte-identical to `604899c0`). The lane authored only the generated page, which is a findings and inventory artifact that may name lanes. The delta has no new instance, so there is no RESIDUE under this rule.
- **Hosted, exact head, read only.** Snapshot taken at 2026-11-04 about 16:40Z (`receipts/hosted_checkruns_at_review.tsv`).
  - 56 check-runs: 27 completed success, 1 skipped (Physical gPTP, nightly and manual only), and 28 queued or in progress.
  - The successes include docs-check, docs-check-no-git, docs-gates-0..2, verilator-lint, elaborate and elaborate-gates-0..4, yosys-elaboration and full-ci-gate.
  - Most Verilator and Yosys shards were still running. The manager owns hosted and local-replica acceptance.

## Findings

No BLOCKER, MAJOR or MINOR.

### R1 - RESIDUE (retained from R742-5 R1 / R741-5 R1 / R741-6 R1, recurred) - Docs - PR #815 body, "Known limitations", last bullet - the hosted status is stale
- **Evidence:** the body says "Hosted result: this head has no hosted run until it is pushed, so its required contexts are still to be read." Head `430a077c` is pushed. At review time it had 27 successful runs and 28 running.
- **Impact:** wording only. It changes no measurement, gate or verdict.
- **Exact fix:** replace the bullet with wording that does not depend on push state, for example "Hosted result: the required contexts at the PR head are read from its check-runs; this body states no hosted verdict."
- **Verification:** read the PR body.

### R2 - RESIDUE (retained from R741-4 R2 via round 5 and R741-6) - Docs - `scripts/docs_inventory.py:32` - "the punctuation ending it" is wider than the code
- **Evidence:** the generator is unchanged in the delta, and the line is still present at the head (`sed -n 30,34p`).
- **Exact fix:** as recorded in R741-4 R2.
- **Verification:** read the docstring at the next head.

### S1 - SUGGESTION (retained from round 5 S1) - Conformance, Docs - `scripts/docs_inventory.json` D0-001, D0-033, D0-056 - three entries dev has fixed remain as "re-verify: quote not found" rows
- **Evidence:** `docs/DOCUMENTATION_AUDIT.md:465`, `:486` and `:507` at the head. The JSON is unchanged.
- **Status:** optional.

### S2 - SUGGESTION (retained from round 5 S2, re-measured on the #836 merge) - Docs - `docs/DOCUMENTATION_AUDIT.md:26` and the "Contradicted by" cells - line citations pinned at `1f29f189` trail the merged tree further
- **Evidence:** D0-026 cites `scripts/run_litex_sims.sh` lines 99-108 (`INVENTORY`) and 150 (`run_aggregate`) at `1f29f189`. Those lines were 100/151 at `e61a4afa`. PR #836 moves them to 115 and 192 at the head (`receipts/d0026_cited_lines.txt`).
- **Why it is not a defect:** the page states the pin, and the finding's substance still holds at the head. `run_aggregate` reconciles the inventory both ways (MISSING and UNLISTED). `SELECTED` defaults to the whole inventory (`scripts/run_litex_sims.sh:128`, `:192-218`), so `docs/guides/VERIFICATION_DEVELOPER.md:32` ("Migen scripts lack one aggregate runner") is still contradicted.
- **Status:** optional. Re-pin the citations when a round re-verifies statements.

### S3 - SUGGESTION (new, outside the delta) - Robustness - `scripts/docs_inventory.py`, filesystem-walk population - the no-Git walk counts a gitignored `scripts/__pycache__/`
- **Evidence:** on a fresh `git archive` of the head, the walk renders the committed page (rc 0). After a probe plants an ignored `scripts/__pycache__/x.pyc` (`.gitignore:28` ignores `__pycache__/`), `--check` gives rc 1. The page gains a `scripts/__pycache__/` module-README row and one line on the page's own count (`receipts/nogit_docs_inventory_walk.txt`). I first saw this when an earlier no-Git run in the same archive wrote bytecode (`receipts/nogit_docs_gate.txt`).
- **Impact:** a false STALE only when Python has already run in an archive tree before the walk. No workflow runs the inventory without Git: the no-Git job runs `docs_check.py` and `check_feature_status.py` only. The generator is unchanged since its lens was covered, so this does not reopen any lens.
- **Possible outcome (optional, a new Issue if wanted):** the walk skips ignored build artifacts the way `docs_check.py`'s `.gitignore`-aware walk does, or the docstring names the limit.

### Earlier SUGGESTIONs, all retained and optional

The delta does not touch the generator or the data file, so these stand as recorded:

- the two surviving self-test mutants;
- a quote that normalises to nothing is accepted;
- the broad `also` fragments (D0-059, D0-002);
- the generator is at 999 of 1,000 lines (still 999 by `wc -l`);
- the watcher job limit cancels healthy runs (outside this PR);
- the round 1 to round 3 suggestions listed by R742-5.

## Prior BLOCKER, MAJOR and MINOR findings

| Prior finding | State at `430a077c` | Evidence |
|---|---|---|
| R742-3 F1 / R741-3 F1 BLOCKER, the literal path fails `pp_srcs.py --check` | Stays RESOLVED | `pp_srcs.py --check --selftest` gives rc 0 at the head (`receipts/pp_srcs_check.txt`). The source-list files are byte-identical in the lane's diff against dev |
| R742-3 F2 MINOR, the search misses real copies | Stays RESOLVED | The generator is unchanged. `--selftest` passes 50/50. D0-057's copy row was re-found at its moved line |
| R742-2 F1-F3, R741-2 F1, R742-1 F1, R741-1 F-series | Stay RESOLVED | No data entry or generator line changed (`receipts/lane_diff_vs_dev_r5_vs_r6.txt`) |
| R742-3 R1, R741-3 R1-R3 RESIDUE | Stay APPLIED | JSON and docstring unchanged |

## Reviewer-owned lens ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (S1 optional) | Issue #797 acceptance and scope 1 and 6. `docs/DOCUMENTATION_AUDIT.md` regenerated byte-identical at the merge and at the head. Status counts 176/16/0/21 and the stale-page rule. The full docs gate set rc 0 at the head (receipts above) | R742-6 | `430a077c0e9a5a42062103742a8f3f1b8bacc6b8` |
| RTL | CLEAN | `git diff --name-only 604899c0 430a077c` lists 10 files, none under `hdl/`, `syn/` or the submodules, and the gitlinks equal dev's. `pp_srcs.py --check --selftest` rc 0. Hosted verilator-lint, elaborate and yosys-elaboration succeeded at the head | R742-6 | `430a077c0e9a5a42062103742a8f3f1b8bacc6b8` |
| Robustness | CLEAN (S3 optional) | Mechanical remerge tree `070213ea` equals `626d367f`. Command-table three-way leaf check. No-Git walk on a fresh archive rc 0, plus the planted ignored-directory probe. Digest arm head versus dev | R742-6 | `430a077c0e9a5a42062103742a8f3f1b8bacc6b8` |
| Tests | CLEAN | `docs_inventory.py --selftest` 50 controls. The gate fails on the stale merge page (rc 1) and heals with `--write`. `pp_srcs.py --selftest`, `ci_gate_workflows_selftest.py`, `ci_litex_legs_selftest.py`, and the doc-style, solution-docs and bare-metal selftests all rc 0 | R742-6 | `430a077c0e9a5a42062103742a8f3f1b8bacc6b8` |
| Docs | CLEAN (RESIDUE R1, R2; S2 optional) | Row diff of `docs/DOCUMENTATION_AUDIT.md` `626d367f..430a077c` with line arithmetic. D0-057 at `TESTING.md:1818`. D0-026 cited lines across `1f29f189`, `e61a4afa`, `604899c0` and `430a077c`. PR #815 body: Status, Round 6 and Known limitations. Em-dash on 534 and 260 added lines | R742-6 | `430a077c0e9a5a42062103742a8f3f1b8bacc6b8` |

## Real limits

- **Command-table checker.** I could not execute `scripts/ci_tool_inventory.py --check` because the checksum-pinned Bash parser is not installed. I did not install it. Its digest arm was recomputed independently. Its census and parser arms, and the PR body's statements that the refusal text is identical across five heads and that the inventory step "walked alone" passes, are not verified by me.
- **Statements on the pages.** No statement on any page was re-verified this round. That matches the PR's own limitation.
- **Execution evidence.** Source-head evidence is my own probes plus the author's published claims. No manager source bank runs at this head, and none is claimed or inferred.
- **Out of scope.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Hosted runs.** The hosted snapshot is partial: 28 runs were in flight.

## Pending manager duties

- Apply RESIDUE R1 to the PR body and carry R2 to the residue checklist.
- Build and validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts.
- Read the exact-head Verilator and Yosys shards to completion. Run the local replica.
- Own the #838 decision trail for the image command-table checker.

## Clone restoration

`HEAD` is `430a077c` with tree `7775f0a1`. `git status --porcelain --ignored` is empty. The index modes and blobs of all 1472 entries equal the HEAD tree, and `write-tree` gives `7775f0a1`. The six gitlinks are unchanged (`receipts/clone_restore_verify.txt`). All probe trees were under `scratch/`.

R742-6 FINISHED
