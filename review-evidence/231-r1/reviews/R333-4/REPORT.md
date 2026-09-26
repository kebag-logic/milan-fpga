[R333] NEGATIVE - exact head ae729bbfd90934f4d56d3b02f1ffc652496b414d

# R333-4 external review: issue #231 / PR #572

Reviewer: [R333], external independent reviewer, round R333-4.

- Head: `ae729bbfd90934f4d56d3b02f1ffc652496b414d`.
- Tree: `c2c692fb14fe731e46ff03873c11a45a77adc4e8`, verified in the review clone (`receipts/01-head-identity.txt`, `receipts/40-clone-state-after.txt`).

This is a delta review. My round R333-3 covered `3a1477c5` in full and raised one MINOR finding (F1). This round judges `3a1477c5..ae729bbf`: one commit, `docs: describe baseline refusal coverage without fixed counts`. The commit message is one line with no trailers (`receipts/06-history.txt`). All five lenses are re-applied at this head.

Context was reconstructed from these public sources:

- AGENTS.md and CONTRIBUTING.md.
- docs/README.md.
- The #231 body and its frozen acceptance criteria (`receipts/33-issue.json`).
- The round-four assignment, issue comment 5847557806 (`receipts/32-assignment-comment.json`).
- The live PR #572 body at this head (`receipts/30-pr-view.json`, `receipts/31-pr-body.txt`).
- The diff and its history.

My verdict, findings and ledger were written before I read any other reviewer's report. The two round-three reviews (R332-4 and R333-3) were read only afterwards, to resolve their findings. Reading them changed nothing above the "Prior findings" section.

## Verdict

**NEGATIVE, on one MINOR Docs finding about the live PR body.** It is not about the committed tree.

The committed change is correct and complete for the round-three finding, which is **CLOSED**:

- The delta touches only the two named documents.
- The page and the recipe no longer state a superseded refusal or mutant count.
- Every refusal category the page names is exercised by the self-test.
- The self-test and the maintained mutant campaign pass as documented.
- Every documentation gate returns rc 0.

Item 4 of the assignment is not met. The Round 4 section of the live PR body ends with a status paragraph that is false on the published PR (F1 below).

## Assignment checks (issue 231 comment 5847557806)

1. **The delta touches only the two documents.** Met.
   - `git diff --name-status 3a1477c5 ae729bbf` lists only `docs/findings/PP_SHADOW_BASELINE.md` (+3/-2) and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` (+1/-1) (`receipts/02-delta.diff`, `receipts/03-delta-names.txt`).
   - The full `ls-tree -r` comparison differs in exactly those two blobs (`receipts/05-lstree-delta.txt`). No script, measurement, TSV/JSON artifact, workflow or gitlink changed.
   - The four gitlinks are identical to base `7eb3b0d4` (`receipts/40-clone-state-after.txt`).
   - The whole PR still has the same 13 paths against `7eb3b0d4` (`receipts/04-full-stat.txt`).
2. **No drift-prone count remains, and the category description matches the code.** Met.
   - The superseded lines are gone: "six additional inventory refusals" (page, old `:282`), "Ten enforcement-removal mutants" (old `:285`) and "the ten removal mutants" (recipe, old `:382`).
   - They now read as follows:
     - `PP_SHADOW_BASELINE.md:282-283`: "inventory, geometry, binding and declaration refusals … endpoint, pathname and CLI containment refusals".
     - `:286`: "Every maintained enforcement-removal mutant fails; the unchanged control passes".
     - `PP_SHADOW_BASELINE_RECIPE.md:382`: "Run the maintained enforcement-removal mutants alongside the positive control".
   - I searched the PR's documents for any count next to "refusal", "mutant" or "removal" (`receipts/16-count-search.txt`). The only hit is `PP_SHADOW_BASELINE.md:281`, "Its self-test retains nine original refusal cases", which is unchanged since `3a1477c5`. It is not a drifting count:
     - it names the fixed original set, which the self-test still counts and prints as "9 refusals PASS" (`receipts/11-selftest.txt`);
     - adding arms does not falsify it;
     - the assignment did not name it.

     See S2.
   - `scripts/category_map.py` (`receipts/14-category-map.txt`) classifies every refusal arm the self-test runs:
     - The 40 synthetic-export inventory arms split into:
       - inventory: 2 (missing generated ROM, unlisted readmemh);
       - geometry: 14 (generated-ROM and parameter-ROM short, long, narrow and wide, plus the nonempty SRAM);
       - binding: 6 (duplicated and missing `*_HEX_P` bindings for three families);
       - declaration: 18 (duplicated and missing package reads, and depth/width declarations).
     - endpoint: 2 (`syn/ooc/pp_baseline.py:382-385`).
     - pathname: 3 (`:404-408`).
     - CLI containment: 3 (`:412-417` and the in-repository refusal at `:486-493`).

     Every category named on the page has at least one arm. The only exercised category the page does not name is the two single-synthesis-command template refusals (`:386-394`). The page's list is not presented as exhaustive, so this is S1, not a finding.
3. **Executable checks rerun at this head.** Met. Python 3.14.7 (`receipts/10-python-version.txt`).
   - `python3 -B syn/ooc/pp_baseline.py --selftest`: rc 0. The output reads: 9 original refusals, 5 parameter/template refusals, 40 inventory refusals plus the restored control, 9 endpoint refusals plus a valid pathname, then 3 default scripts, the attribution constraint and CLI containment (`receipts/11-selftest.txt`).
   - `python3 -B syn/ooc/pp_baseline_mutants.py`: rc 0. The control has rc 0, and all 28 maintained mutants have rc 1 and are killed (`receipts/12-mutants.txt`).
   - `python3 -B syn/ooc/pp_baseline_reports_selftest.py`: rc 0 (`receipts/13-reports-selftest.txt`).
   - Documentation gates, all rc 0:
     - `docs_check.py` in Git mode: 0 findings, 168 md + 894 text files (`receipts/20-docs_check-git.txt`, `receipts/28-docs_check-venv-git.txt`).
     - `docs_check.py` with `GIT_DIR=/dev/null`: 0 findings, the same 894 files; it skips only the Git inventory parity check (`receipts/21-docs_check-nogit.txt`, `receipts/29-docs_check-venv-nogit.txt`).
     - `check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`: 0 findings over 849 added lines in 3 pages (`receipts/22-em_dash.txt`).
     - `check_doc_style.py`: OK (`receipts/23-doc_style.txt`).
     - `gen_toc.py --check`: OK (`receipts/24-gen_toc-check.txt`).
     - `gen_toc.py --verify-anchors`: 177 links reproduced (`receipts/25-gen_toc-anchors.txt`).
     - `check_doc_paths.py`: 848 cited paths resolve (`receipts/26-doc_paths.txt`).

     The em-dash and TOC gates need the pinned Markdown renderer. It was installed with `--require-hashes` from `tools/markdown/requirements.txt` into a private disposable environment under the unpublished scratch directory; no shared install was made (`receipts/27-renderer-venv-freeze.txt`). The first attempts, which ran without that renderer and returned rc 2 ("renderer not installed"), were overwritten by these runs.
   - CI wiring is unchanged. `.github/workflows/rtl-fast.yml:209-211` and `scripts/ci_events.py:2325-2327` run all three self-tests (`receipts/15-ci-wiring.txt`).
4. **The PR body has no stale status or count lines.** Not met; see F1.
   - The Round 3 section's counts (40, nine, five, nine, 28, 15/15, 17/17) are still accurate at this head.
   - The Round 2 section's "all ten enforcement-removal mutants" is labelled history for its own round, and Round 3 supersedes it explicitly. I judge it acceptable.
   - The Round 4 section's closing paragraph is not history. It is false now.

## Findings

### F1 - MINOR - Docs - PR #572 body, section "Round 4", final paragraph - The live PR body says the reviewed commit is unpushed and the body unpublished

- **Authority/evidence.**
  - The live body (`receipts/31-pr-body.txt`, fetched after its 2026-09-26T15:51:03Z update, with `headRefOid` = `ae729bbfd90934f4d56d3b02f1ffc652496b414d`) ends: "This commit is local and unpushed. This body is a prepared replacement; the live PR has not been edited. Independent re-review, publication and final-head acceptance remain pending."
  - The commit is the published PR head, and the text is the live body. Both of the first two sentences are false on the page that carries them.
  - AGENTS.md sections 1-2 and the Docs lens require that the PR carry public state a cold reviewer can rely on. The round-four assignment's item 4 asks for exactly this check.
  - This class of text was rated SUGGESTION twice before: R333-2 S5, the "unpushed" text, and R333-3 S2, "ready for re-review". I raise it to MINOR for three reasons:
    - this round's assignment makes it an explicit verification item;
    - it has recurred in every round;
    - this is the merge-deciding round, so no later round is left to refresh it before the body becomes the permanent PR record.
- **Impact.** No technical claim is wrong; the committed tree is unaffected. A later reader of the merged PR is told that the merged commit was never pushed and that the description was never published. That contradicts the PR's own metadata and weakens the record as evidence.
- **Required outcome.** The PR body carries no status sentence that is false for the live PR. Deleting that paragraph or replacing it with an accurate status is sufficient. The head does not change: this is a metadata edit.
- **Verification.** Run `gh pr view 572 --json body,headRefOid` and confirm that no such sentence remains and that `headRefOid` is still `ae729bbfd90934f4d56d3b02f1ffc652496b414d`. Because the head does not change, a reviewer can close this at the same exact head without re-running the tree lenses.

### S1 - SUGGESTION - Docs - `docs/findings/PP_SHADOW_BASELINE.md:282-283` - Template refusals are exercised but not named

The self-test's two single-synthesis-command refusals (`syn/ooc/pp_baseline.py:386-394`) belong to none of the seven named categories. The list does not claim to be exhaustive, so nothing is misstated. Adding "template" to the second sentence would make the list complete. This is optional.

### S2 - SUGGESTION - Docs - `docs/findings/PP_SHADOW_BASELINE.md:281` - One fixed count remains

"Its self-test retains nine original refusal cases" is accurate at this head. The self-test prints "9 refusals PASS", and the sentence is phrased so that added arms do not falsify it. If the maintainers want the page to have no hard-coded counts at all, this sentence could name those cases by kind (image, wrapper-block and default-expression refusals). This is optional.

## Lens results (per-lens evidence)

```text
[R333] PASS Conformance — issue #231 acceptance; assignment 5847557806 items 1-3; receipts/02-delta.diff; receipts/05-lstree-delta.txt — The delta is text-only in the two named pages. The refusal and mutant claims match the executed self-test and mutant campaign. Measured figures, scripts and acceptance-relevant artifacts are byte-unchanged from 3a1477c5, which R333-3 found clean under this lens.
[R333] PASS RTL — receipts/05-lstree-delta.txt; receipts/40-clone-state-after.txt — No hdl/ file, gitlink, constraint, script or synthesis input changed between 3a1477c5 and ae729bbf. Gitlinks equal base 7eb3b0d4. RTL scope is unchanged from R333-3's clean coverage.
[R333] PASS Robustness — syn/ooc/pp_baseline.py (blob 2d2634b9, unchanged); receipts/11-selftest.txt; receipts/14-category-map.txt — Every refusal the page names is still exercised and passes at this head. No refusal was weakened, because the script bytes are unchanged.
[R333] PASS Tests — syn/ooc/pp_baseline_mutants.py (blob db3f4a87, unchanged); receipts/12-mutants.txt; receipts/13-reports-selftest.txt; receipts/15-ci-wiring.txt — The control passes, all 28 maintained mutants are killed, the reports self-test passes, and fast-CI wiring runs all three.
[R333] MINOR Docs — PR #572 body, Round 4 final paragraph — F1 above. The committed pages themselves (PP_SHADOW_BASELINE.md:276-290, PP_SHADOW_BASELINE_RECIPE.md:376-392) match the executed self-test (receipts/14-category-map.txt), and all seven documentation gates return rc 0 (receipts/20-29).
```

## Completion ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #231 acceptance; assignment 5847557806; delta diff and tree comparison; self-test and mutant receipts | R333-4 | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| RTL | CLEAN | tree comparison 3a1477c5→ae729bbf (2 doc blobs only); gitlinks against base | R333-4 | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| Robustness | CLEAN | `syn/ooc/pp_baseline.py` (unchanged); self-test output; category map | R333-4 | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| Tests | CLEAN | `syn/ooc/pp_baseline_mutants.py` (unchanged); mutant, self-test and reports-self-test runs; CI wiring | R333-4 | ae729bbfd90934f4d56d3b02f1ffc652496b414d |
| Docs | UNCLEAN (F1, MINOR) | `PP_SHADOW_BASELINE.md:276-290`; `PP_SHADOW_BASELINE_RECIPE.md:376-392`; live PR #572 body; seven documentation gates | R333-4 | ae729bbfd90934f4d56d3b02f1ffc652496b414d |

For Conformance, RTL, Robustness and Tests, the full depth of coverage rests on R333-3 at `3a1477c5`, which is an ancestor of this head. Nothing within those lenses' scope changed between the two commits, as the tree comparison shows, and this round re-applied each lens to the delta.

## Prior findings disposition (written after the verdict, findings and ledger above)

| Prior finding | Status at ae729bbf | Evidence |
|---|---|---|
| R333-3 F1 MINOR (Docs) = R332-4 F1: page `:282`, `:285` and recipe `:382` state superseded refusal/mutant counts | **CLOSED** | The lines were replaced by category and "every maintained" wording (`receipts/02-delta.diff`). The categories match the executed arms (`receipts/14-category-map.txt`), and no drifting count remains (`receipts/16-count-search.txt`). |
| R333-3 S1 (Tests, Robustness): the unsupported-log-value refusal is unpinned | Unchanged; optional | Script untouched by the delta. |
| R333-3 S2 (Docs): stale PR-body round status | **Superseded by F1** | The Round 3 wording was replaced. The new Round 4 status paragraph is false, not just dated. |
| R332-4 S1, S2 (Tests); R332-3 S1, S2; R333-2 S1, S3, S4, S6; R332-1 S1, S2; R333-1 S2 | Unchanged; optional | Untouched by the delta. |
| R332-3 F1, F2; R333-2 F1, F4; R333-1 F1-F4; R332-1 F1-F3 | Remain **CLOSED** | Closed at earlier heads (R333-3, R332-4). The delta changes no artifact they cover apart from the two claim lines verified above. |

## Real limits

- This round is a delta review. The full-depth Conformance, RTL, Robustness and Tests coverage of the unchanged scripts, measurements and pages comes from R333-3 at `3a1477c5`. It was not repeated here.
- No synthesis, place-and-route, Yosys, builder, Verilator bank or hardware run was performed. The measured figures are not re-derived by this round. Physical calibration was NOT RUN, and field skips are not hardware proof.
- The pinned renderer for the em-dash and TOC gates was installed from the repository's hash-locked requirements into a private, unpublished environment. Its versions are recorded in `receipts/27-renderer-venv-freeze.txt`.
- Hosted checks at this head were still running when sampled: Verilator shards, `yosys-elaboration`, `elaborate` and `docs-check` were in progress, and `Physical gPTP` was skipped (`receipts/34-hosted-check-runs.tsv`). Those are not evidence here.
- The clone is restored at the exact head. HEAD, tree, index tree and index entries equal HEAD, status including ignored files is empty, and gitlinks equal base (`receipts/40-clone-state-after.txt`).

## Pending manager duties

- Correct the Round 4 closing paragraph of the PR body (F1), and have the correction confirmed at the same head.
- Accept the exact-head hosted `rtl-fast`, `verilator-suites` and `yosys-portability` results once complete. Distinguish executed jobs from skipped contexts.
- Build and validate the current-dev candidate merge (source base `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`, live dev `831f94f4146cc45ec476f8c8dcf5afac7cd8eacf`) at the merge turn.
- Update the #229 reference if the merge head changes. Obtain explicit maintainer merge authorization, and run post-merge containment.

R333-4 FINISHED
