[R332] NEGATIVE - exact head ae729bbfd90934f4d56d3b02f1ffc652496b414d

Round R332-5 is an internal, cleared-context delta review of PR #572 for issue #231.

- Head: `ae729bbfd90934f4d56d3b02f1ffc652496b414d`, tree `c2c692fb14fe731e46ff03873c11a45a77adc4e8`.
- Delta judged: `3a1477c5..ae729bbf`, assigned in issue 231 comment 5847557806. My previous round, R332-4, covered `3a1477c5` in full.
- Full base: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.

All five lenses were applied at this head.

**Verdict: NEGATIVE, on one MINOR Docs finding in the live PR body.**

- The committed correction is right. R332-4 F1 (the same finding as R333-3 F1) is **closed**:
  - the page and recipe no longer state the superseded counts;
  - the new category wording matches what the self-test actually exercises.
- **F1 (new, MINOR, Docs):** the live PR body's Round 4 section still says "This commit is local and unpushed ... the live PR has not been edited". That is false for the published PR.
  - No commit is needed to fix it. Editing the PR body and re-checking it can bank Docs at this same head.
- Conformance, RTL, Robustness and Tests are CLEAN.

## Reconstruction

Authorities read:
- AGENTS.md and CONTRIBUTING.md (by reference from AGENTS.md);
- the #231 body and its frozen acceptance criteria;
- scope decision 5844867171;
- the round-four assignment 5847557806, which says: "Describe the refusals and mutants by what they cover, not by a hard-coded count ... No other change";
- [A341] TAKEN 5847569885 and REVIEW READY 5847599517;
- the live PR #572 body (`receipts/pr572.json`);
- the public evidence tree `review-evidence/231-r1` at `c8a1a9a2`.

Order of reading:
- Prior public findings (R332-4 5847547395, R333-3 5847555580) were read only after my own pass over the delta and my executed checks.
- The concurrent same-head report of the other reviewer (R333-4) was not read.

## What was executed

Everything ran in the review clone at the exact head. The interpreter was Python 3.14.7. The documentation renderer was the repository's hash-locked set (`tools/markdown/requirements.txt`), installed with `--require-hashes --only-binary=:all:` into a disposable environment under `scratch/`.

The driver is `run_checks.sh <clone> <receipt-dir>`. It runs each check in the foreground and records its exit status.

| Check | Result | Receipt |
|---|---|---|
| `git diff --raw 3a1477c5 ae729bbf` | Two paths only, both mode 100644: `docs/findings/PP_SHADOW_BASELINE.md` (`bbc518ce`→`aa03dd7c`) and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` (`d66c667a`→`3894118a`). +4/-3 | `receipts/delta.raw`, `receipts/delta.diff` |
| `syn/`, `scripts/` and `.github/` trees compared between `3a1477c5` and `ae729bbf` | Byte-identical. `MUTANTS` has 28 entries at both commits, and had 10 at `0a506fa8` | `receipts/counts_and_identity.txt` |
| PR raw diff against the base | The same 13 paths as before. No `hdl/` path. All four gitlinks are identical to the base (sha256 of the gitlink list is identical) | `receipts/full.raw`, `receipts/integrity.txt` |
| `python3 syn/ooc/pp_baseline.py --selftest` | rc 0. Printed: 9 original refusals, 5 parameter/template refusals, 40 inventory refusals plus the restored control, a valid pathname plus 9 endpoint refusals, 3 default scripts, the attribution constraint, and CLI containment | `receipts/checks-pinned-renderer/selftest.log` |
| `python3 syn/ooc/pp_baseline_mutants.py` | control rc 0; all 28 maintained mutants rc 1 | `receipts/checks-pinned-renderer/mutants.log` |
| `python3 syn/ooc/pp_baseline_reports_selftest.py` | rc 0 | `.../reports_selftest.log` |
| `python3 scripts/docs_check.py` (Git mode) | rc 0: 0 findings, 168 md + 894 text files, scrub self-test 23/23 | `.../docs_check_git.log` |
| `env GIT_DIR=/dev/null python3 scripts/docs_check.py` | rc 0: 0 findings over the same 894 text files. It skips only inventory parity | `.../docs_check_nogit.log` |
| `python3 scripts/check_em_dash.py --base 7eb3b0d4...` | rc 0: 0 findings over 849 added lines, arms 339/339 | `.../em_dash.log` |
| `python3 scripts/check_doc_style.py` | rc 0 (22 current documents) | `.../doc_style.log` |
| `python3 scripts/gen_toc.py --check` | rc 0 | `.../toc_check.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | rc 0 (177 cross-page fragments) | `.../toc_anchors.log` |
| `python3 scripts/check_doc_paths.py` | rc 0 (848 cited paths resolve) | `.../doc_paths.log` |
| First run with the system interpreter, which lacks the renderer | The em-dash, TOC and anchor gates stop with rc 2 ("pinned Markdown renderer is not installed"). That is an environment refusal, not a verdict, and it was superseded by the run above. The other seven checks gave rc 0 | `receipts/checks-system-python-no-renderer/` |
| Clone integrity after every run | `git status` is empty. The index tree equals the HEAD tree. All 918 tracked regular files hash to their index blobs. The executable modes match. The gitlinks equal the base | `receipts/integrity.txt`, `.../status_after.txt` |

## Assignment checks

### 1. Only the two documents change

**Met.**
- See the raw diff above.
- No script, measurement, TSV, JSON, workflow or gitlink changed.
- The commit subject is one line with no trailers: `docs: describe baseline refusal coverage without fixed counts`.

### 2. Neither document states a drifting count, and the categories match the self-test

**Met for the lines the assignment named.** `receipts/doc-claims-vs-selftest.txt` maps each category to code:

| Page category (`PP_SHADOW_BASELINE.md:282-283`) | What exercises it in `syn/ooc/pp_baseline.py` |
|---|---|
| inventory | missing generated ROM, nonempty SRAM, unlisted readmemh (`:319-323`) |
| geometry | generated ROM short/long/narrow/wide (`:325-329`); parameter ROM short/narrow/wide ×3 families (`:342-344`) |
| binding | duplicated/missing `.<PARAM>(...)` binding ×3 families (`:345-347`) |
| declaration | duplicated/missing geometry package and duplicated/missing depth/width declarations (`:353-362`) |
| endpoint | gateware directory, attribution endpoint, one synthesis command ×2, CLI endpoint ×2 (`:382-417`) |
| pathname | `{`, `}`, `"` in a string image parameter (`:404-408`) |
| CLI containment | in-repository `--output` refused with exit 2 (`:486-494`) |

Every category names refusals that exist and are executed. No executed export refusal falls outside the categories.

Wording of the mutant lines:
- `PP_SHADOW_BASELINE.md:286`: "Every maintained enforcement-removal mutant fails; the unchanged control passes."
- `PP_SHADOW_BASELINE_RECIPE.md:382`: "Run the maintained enforcement-removal mutants alongside the positive control."

Both are count-free and true: 28 of 28 were killed, and the control passed.

Remaining numerals:
- `:281` "Its self-test retains nine original refusal cases" still carries a number. It was not among the lines F1 or the assignment named. It is true at this head: the self-test computes and prints `9 refusals`. See S1.
- "Three default scripts" (`:284`) counts emitted endpoints, not refusals, and matches the code (`:460-472`).

### 3. Executable checks and gates

**Met.** All rc 0; see the table above.

### 4. No stale status or count lines in the PR body

**Not met.** See F1.
- The Round 2 section's "all ten enforcement-removal mutants" and "kills all five mutants" are round-scoped history. They were true at `0a506fa8` (10 entries, per `receipts/counts_and_identity.txt`), and Round 3 supersedes them explicitly ("kills all 28").
- The Round 3 counts (40 inventory, nine original, five parameter/template, nine endpoint, 28 mutants) all match this head.
- The Round 4 status paragraph does not match the live PR.

## Findings

### F1 - MINOR - Docs - PR #572 body, Round 4 section, final paragraph (`receipts/pr-body-status-lines.txt`, body line 59) - The live PR body says the reviewed head is unpushed and the PR unedited

**Authority:**
- AGENTS.md section 6, Docs lens: "The PR and Issue contain enough evidence for another cold reviewer."
- The round-five assignment, item 4: "the PR body has no stale status or count lines."

**Evidence:**
- The live body (`receipts/pr572.json`) ends: "This commit is local and unpushed. This body is a prepared replacement; the live PR has not been edited. Independent re-review, publication and final-head acceptance remain pending."
- The same API response reports `headRefOid` `ae729bbfd90934f4d56d3b02f1ffc652496b414d`, so the commit is pushed and is the PR head.
- The body is itself the edited live PR text.
- The sentence was true in the author's prepared file. It was published unchanged.
- The same pattern was raised as optional in earlier rounds (R333-2 S5, R333-3 S2). Here it is a false statement about the exact head under merge review, and the assignment makes it a check.

**Impact:**
- A cold reviewer, or the merge-turn reader, is told by the PR's own record that the head under review is not published and that "publication" is pending.
- Taken literally, this contradicts the head the reviews name. It invites doubt about whether the reviewed head is the merged one.
- No code or measurement is affected. That is why it is MINOR and not MAJOR.

**Required outcome:**
- The Round 4 section states the actual status: the commit is published as the PR head, and it is under (or has passed) independent re-review.
- It carries no "local", "unpushed" or "not edited" claim.
- The historical Round 1-3 sections may stay as round-scoped history.

**Verification:**
- Re-read the live PR body.
- No line claims the head is local or unpushed, or that the live PR is unedited.
- Every stated status matches the live `headRefOid` and review state.
- Because the PR body is not a tree artifact, Docs can be re-covered at this same head `ae729bbf` with no new commit.

### Suggestions (do not affect coverage)

**S1 - SUGGESTION - Docs - `docs/findings/PP_SHADOW_BASELINE.md:281`, against `syn/ooc/pp_baseline.py:252-310`.**
- "Its self-test retains nine original refusal cases" is the one remaining hard-coded refusal count in either document. It is true now: 9 are computed and printed.
- The qualifier "original" bounds it to the first unit arm, but adding a case to that arm would silently make it stale.
- The five parameter/template refusals (`:299-310`) are covered only generically by `:280` ("missing, short, malformed and ambiguous inputs").
- Optional: describe the unit arm by category too, for example "image, wrapper-block and template refusals", in the same style as `:282-283`.

**S2 - SUGGESTION - Docs - `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:382`.**
- Three maintained mutants alter an enforcement point rather than delete it: `microcode address depth`, `attribution boundary preservation` and `unfiltered hierarchy report`.
- "enforcement-removal" describes them loosely. It matches the harness's own docstring, so no reader is misled about the pass criterion. No action is needed.

## Prior public findings at this head

| Prior finding | Status at `ae729bbf` | Evidence |
|---|---|---|
| R332-4 F1 = R333-3 F1, MINOR Docs: the page and recipe state superseded counts ("six additional inventory refusals", "Ten ... mutants", "the ten removal mutants") | **Closed** | `receipts/delta.diff` replaces all three lines. `grep -rniE 'mutant\|refusal'` over both documents and `AREA_BUDGET.md` shows only count-free wording, plus the true "nine original" (S1) (`receipts/counts_and_identity.txt`). Categories map to executed refusals (table above). The self-test and mutants pass 28/28 |
| R332-4 S1, S2 (Tests: fixture `UPC_W_C = 1`; readmemh subset weakening) | Retained as optional suggestions | Script bytes are unchanged since `3a1477c5` |
| R333-3 S1 (unpinned unsupported-log-value refusal) | Retained as optional; unchanged code | Same |
| R333-3 S2 (stale "local round-three commit" PR-body text) | That sentence is gone. The equivalent Round 4 sentence is F1 above | `receipts/pr-body-status-lines.txt` |
| R332-3 F2 / R333-2 F1 (#229 reference) | Closed in R332-4. The merge-commit link update remains a manager duty (below). The delta touches only `PP_SHADOW_BASELINE.md:282-286` (Input integrity), not the figures the #229 comment quotes | `receipts/delta.diff` |
| Earlier findings R332-1, R333-1, R332-3 F1, R333-2 F4 | Closed in earlier rounds. The delta touches none of their artifacts | `receipts/delta.raw` |

## Lens results

| Lens | Artifact examined at `ae729bbf` | Result |
|---|---|---|
| Conformance | issue 231 comment 5847557806 against `receipts/delta.diff`; #231 acceptance and decision 5844867171 against `receipts/full.raw` | CLEAN. The text-only scope is honoured. Only the named claims changed, to count-free wording. No measurement, figure or recipe command changed, so the acceptance evidence covered at earlier heads is untouched |
| RTL | `receipts/full.raw` (no `hdl/` path); gitlinks in `receipts/integrity.txt` (identical to base `7eb3b0d4`) | CLEAN. No RTL artifact is in scope. The delta is two Markdown files |
| Robustness | `syn/ooc/pp_baseline.py:314-418` (restoration in `finally`, `expect_refusal` rejects unrelated exceptions); empty `receipts/checks-pinned-renderer/status_after.txt` | CLEAN. Code is byte-identical to `3a1477c5`. The self-test and mutant runs leave no residue in the clone |
| Tests | `receipts/checks-pinned-renderer/selftest.log`, `mutants.log`, `reports_selftest.log`; `syn/ooc/pp_baseline_mutants.py:12-77` (28 entries) | CLEAN. The pristine control passes, every maintained mutant is killed, and the report self-test passes. The documented recipe command block (`RECIPE.md:384-387`) runs as written |
| Docs | `docs/findings/PP_SHADOW_BASELINE.md:278-288`; `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:379-391`; all seven documentation gates; live PR body | UNCLEAN (F1, PR body). The committed documents and gates are clean |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | assignment 5847557806; decision 5844867171; `receipts/delta.diff`, `receipts/full.raw`, `receipts/counts_and_identity.txt` | R332-5 | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| RTL | CLEAN | `receipts/full.raw` (no `hdl/`); gitlinks in `receipts/integrity.txt` equal to base | R332-5 | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| Robustness | CLEAN | `syn/ooc/pp_baseline.py:314-418`; `receipts/checks-pinned-renderer/status_after.txt`; `receipts/integrity.txt` | R332-5 | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| Tests | CLEAN | `receipts/checks-pinned-renderer/{selftest,mutants,reports_selftest}.log`; `syn/ooc/pp_baseline_mutants.py:12-77` | R332-5 | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| Docs | UNCLEAN (F1 open) | `docs/findings/PP_SHADOW_BASELINE.md:278-288`; `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:379-391`; `receipts/checks-pinned-renderer/*` doc gates; `receipts/pr572.json`, `receipts/pr-body-status-lines.txt` | R332-5 (not covered clean) | ae729bbfd90934f4d56d3b02f1ffc652496b414d |

## Limits

- This is a delta review. Measurements, builder banks, synthesis and place-and-route were not rerun. Their coverage rests on earlier rounds and on byte-identity of everything outside the two documents.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- Public evidence tree `c8a1a9a2` (committed 15:29Z) predates this head (15:43Z). It has no round-four or exact-head manager bank receipts (`receipts/evidence_tree_*.txt`). I did not independently see the manager's exact-head static, builder and native results; they are the manager's claim.
- The em-dash, TOC and anchor gates required the pinned renderer. The system interpreter lacks it, so the passing run used a disposable hash-locked environment. Both runs are receipted.
- Hosted checks at this head were observed read-only while in flight (`receipts/hosted_check_runs.txt`):
  - Yosys shards 0-3, verilator-lint, bdd-conformance, wire-accountability, docs-check-no-git, changes and full-ci-gate reported success.
  - Verilator shards 0-4, elaborate, yosys-elaboration and docs-check were still in progress.
  - Physical gPTP was skipped, which is not execution.
  - I did not wait for them and make no hosted acceptance claim.
- I did not read the concurrent R333-4 report.

## Pending manager duties

- Fix F1 by editing the PR body, then have Docs re-covered by a reviewer. This can be at this same head.
- Hosted and local-replica acceptance of the exact head, including the in-flight Verilator, elaborate, yosys-elaboration and docs-check contexts.
- The final current-dev candidate build and validation. Source base is `7eb3b0d4`; live dev is `831f94f4146cc45ec476f8c8dcf5afac7cd8eacf`.
- Update the #229 reference to the merge commit at the merge turn (carried from R332-4).
- A second independent positive review, and maintainer merge authorization.

R332-5 FINISHED
