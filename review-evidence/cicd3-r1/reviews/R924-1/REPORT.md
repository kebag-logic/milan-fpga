[R924] NEGATIVE - exact head 13e6d869d842fc06155ef5dae9b0347596d6d4df

Round R924-1, external independent review of issue #998 / PR #1003.
One MAJOR finding remains open. One wording-only RESIDUE is recorded separately.
All five lenses were applied. This is a source review, not merge authorization.

## Scope and authorities

Reviewed exactly `fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f..13e6d869d842fc06155ef5dae9b0347596d6d4df`, stacked on PR #1001. The head tree is `1e43c6e433e84cf7dad9bc1ce86220f0a7f8bb8c`. The three commits are `66b092e124`, `f6c11a2502`, and `13e6d869d8`; the delta has 53 files. Earlier stacked changes are not approved by this review.

Reconstruction followed AGENTS.md and CONTRIBUTING.md, docs/README.md, [issue #998](https://github.com/kebag-logic/milan-fpga/issues/998), REQUIREMENTS.md section 8 (REQ-VER-01 through REQ-VER-04), docs/testing/CI_WORKFLOWS.md, and docs/testing/TESTING.md, then the delta/history and published executable evidence. The issue had no public comments when inspected. Its frozen acceptance requires measured CPU/wall evidence and identical outputs, and every hosted job below 30 minutes with margin. RTL, firmware, expectations and graded figures are excluded from implementation scope.

The [PR](https://github.com/kebag-logic/milan-fpga/pull/1003) currently targets `dev-soft-core`; this review uses the explicitly assigned stacked source base, not GitHub's broader comparison. The public review-start comments identify the two independent roles. No additional manager scope amendment or source-bank evidence was present in the retrieved issue/PR comments. See `receipts/public-state.json`.

The [published author packet](https://github.com/kebag-logic/milan-fpga/tree/3743d3a8a69ad0e1828952edb7dd54694070a1dd/review-evidence/cicd3-r1/author) supplies source validation evidence. REPORT.md sections 1-3 and their receipts were examined. All 303 extracted author files match the publication manifest's published SHA-256 values. No private author material or another reviewer's report informed the independent pass.

## Findings

### R924-1-F1 - MAJOR - Conformance, Robustness, Tests, Docs

**Artifact:** `scripts/mutant_stage.py:54`, especially lines 54-71; callers `tb/verilator/milan_dp/split_mutants.py:206` and `tb/verilator/milan_dp/srptx_mutants.py:130`; controls at `scripts/mutant_stage.py:114`; claimed isolation at `docs/testing/TESTING.md:173` and `scripts/mutant_stage.py:17`.

**Title:** In-tree staging can erase an actively held slot when callers have different temporary directories.

**Authority/evidence:** Issue #998 requires verdict-preserving optimization. The staging contract promises exclusive slots and that a run never sees another run's files. `_take()` stores its locks under `stage_root()`, whose identity includes TMPDIR and UID, but a supplied `parent` places the actual stage directly under that parent without either discriminator. Thus two lock namespaces can govern one directory. Both production in-tree callers supply `parent=HERE`.

`receipts/focused-probes.jsonl` reproduces this with two independent processes and no source modifications. The first holds `split-mutants-0` and writes a marker. The second uses the same parent and UID but a different TMPDIR. It obtains its own lock, returns the identical path, removes the first marker, and leaves its own marker visible to the first caller. The same-TMPDIR positive control returns distinct paths. No different-user process was launched; the UID-dependent lock namespace combined with a UID-independent parent path has the analogous mismatch by inspection.

**Impact:** A direct campaign invocation can delete or replace another active campaign's planted sources, object files and executable path. Build failures or contaminated mutation evidence can result. Separate source checkouts remain isolated, but the helper's advertised concurrency guarantee is false for its supported in-tree mode. Existing tests cover nested holders in one namespace and a single in-tree allocation, so they pass despite this defect. The documentation's unconditional isolation statement is also not true at this head.

**Required outcome:** Every caller capable of naming one staging directory must participate in the same exclusion domain, or receive a distinct directory. Different TMPDIR settings and user namespaces must not permit deletion or reuse of a live stage. Preserve cleanup, stable reuse and safe fallback. Add independent-process regression coverage for the in-tree callers and accurately document any remaining restrictions. Do not resolve this by silently prohibiting an already supported invocation in prose.

**Verification:** Repeat the focused collision probe as a fixed-behavior regression: while the first lock is held, the second caller must not erase its marker or share its live path. Cover same/different TMPDIR, normal staging, in-tree staging, concurrent holders and slot exhaustion. Re-run staging/lifecycle controls and the affected mutation drivers' named-check comparisons. The supplied diagnostic currently asserts reproduction of the defect; it must be inverted when used to validate a fix.

### R924-1-R1 - RESIDUE - Docs

**Artifacts:** New behavior-comment blocks at `scripts/run_all_suites.sh:13`, `scripts/mutant_stage.py:4`, `scripts/ci_make_cases.py:71`, and `scripts/ci_suite_workflows.py:77`.

**Authority/evidence:** The supplied owner comment rule requires behavior/reason comments to carry issue and requirement IDs. These blocks explain behavior and reason but omit the task's issue/requirement attribution. The helper's reference to a separate processor issue does not identify this task's verification authority. No new bench lane label, review-round identifier, reviewer identifier or issue-comment identifier was found in added source comments.

**Impact:** Wording attribution only. No behavior, figure, test, verdict, privacy boundary or requirement interpretation changes.

**Exact fix:** Append `Issue #998; REQ-VER-01 and REQ-VER-04.` within each of those four explanatory comment/docstring blocks, using the file's existing comment syntax. Retain their behavioral explanation. This residue alone does not make any lens unclean.

**Verification:** Inspect the added comment text and rerun the applicable documentation/style gates. Manager may carry this exact wording fix on the residue checklist.

## Independent lens results

**Conformance:** Checked both frozen acceptance criteria against the three adopted changes and their public measurements. Preflight ownership, SHA binding, required context names, verdict preservation and scheduling population were examined. F1 prevents clean coverage. The 30-minute hosted acceptance remains unproved here; local contention-heavy timing and configured timeout values do not establish hosted margin.

**[R924] PASS RTL - `receipts/delta.patch`, the 38 changed mutation drivers, and `receipts/tree-integrity.jsonl` - no production RTL, firmware, interface declarations, clock/reset/CDC logic, mutation definitions, assertion predicates, Makefile recipes or submodule pins change in this delta.** Each driver change replaces temporary staging and imports the shared helper; the lifecycle fixture follows that helper. The scheduling change operates on the existing validated case inventory. This establishes the scope of the RTL result, not a new hardware or full-regression proof.

**Robustness:** Applied to failure/cancellation propagation, empty/missing/wrong evidence, fallback and lock cleanup, invalid CLI combinations, stale directories and reordered failed/unmeasured cases. Planted preflight failure exits 2. The actual generated aggregate step fails for failed, cancelled, skipped, wrong-SHA and absent-SHA preflights. Valid matching evidence passes. A case absent from the cost table still executes; an extraneous cost-table key cannot add or suppress a case. F1 leaves this lens unclean.

**Tests:** Ran the production controls and independent disposable probes. Existing controls correctly detect preflight failures and preserve failed-case outcomes. Warm-cache improvement and byte-identical mutation output were independently reproduced for tcam. The staging self-test's missing cross-namespace in-tree case allows F1 to escape, so this lens is unclean. Broad source-bank execution was neither authorized nor inferred.

**Docs:** Compared the changed CI and testing contracts with actual workflow generation, CLI paths, cache behavior, author receipts and PR scope. The preflight dependency/result/SHA description matches the implementation. Normal and physical sweeps retain preflight, and the selector rejects physical-plus-piece mode. Cost figures affect submission order only; results and receipts remain in driver order. The unconditional staging isolation claim is contradicted by F1. R1 is wording-only residue.

## Executed evidence

The portable scripts accept the review clone as an argument, except `compare_public.py`, which accepts an extracted published author directory. Commands ran as foreground invocations; the control and cache scripts joined their concurrent subprocesses before returning. The small campaign used two concurrent arms with at most four compiler jobs each. MAKEFLAGS was `-j16 --no-print-directory`; a disposable wrapper bounded the unchanged campaign's explicit `-j 0` to four. No full bank, hardware, container replay or host CI orchestration ran.

| Evidence | Result |
|---|---|
| `scripts/run_controls.py <clone>` / `receipts/controls.json` | All 11 command groups exit 0: workflow generation/checks, workflow controls, pieces, cases, staging, fail-fast, lifecycle, receipts, runtime evidence, and production preflight |
| Production `--preflight-only` | 252.386 s wall; all eight self-tests passed; eight raw logs retained in `receipts/preflight/`; no suite selected |
| `scripts/focused_probes.py <clone>` | Reproduces F1; matching-namespace isolation control passes; planted preflight failure and five invalid aggregate states fail closed; reordered failure and missing-cost cases retain identical results |
| `scripts/cache_probe.py <clone>` | Pinned executable reports Verilator 5.050; tcam base/head cold/warm all exit 0; all four transcripts byte-identical |
| tcam warm base versus head | 12/16 versus 16/16 direct hits; 4 versus 0 misses; 11.409 versus 2.868 s wall on this host; `receipts/cache-probe.log` |
| `scripts/compare_public.py <published-author>` | Four completed mutation-driver comparisons preserve every normalized line; warm hits reproduce 79/115 to 115/115, 37/48 to 48/48, 12/16 to 16/16 and 6/8 to 8/8 |
| Published piece/preflight receipts | All seven milan_dp piece results and all sixteen maap piece results identical after removing only head/tree metadata |
| `scripts/verify_tree.py <clone>` | All tracked bytes, modes and index entries match exact HEAD; required gitlinks and five initialized submodules match their pins and pinned bytes |

`ci-fail-fast` still has its same-repository event guard. The generated expected-job list now includes Verilator preflight. The new worker adds no explicit secret/token-bearing command or privilege escalation; it uses the existing checkout pattern. The seven required public contexts retain their names. The aggregate depends on preflight and runs its always-conditioned result/SHA check. Workflow-generation and event-contract controls pass; fail-fast controls exercise fork zero-write and first-failure behavior. These are local structural/executable checks, not a live cancellation request.

The published piece logs are explicitly first/last-200-line excerpts of larger transcripts. Their retained normalized excerpts match, and complete per-case receipt objects match apart from head/tree. This review does not claim to have recomputed the author's 4,234-line full-transcript comparison from those excerpts. The published mmcm_servo comparison is incomplete; its missing tail/runs are not counted as identical. The completed comparisons cover four of the 38 changed drivers, supplemented by the independent tcam campaign and inspection of every driver delta. They are not a claim that all 38 campaigns were independently rerun.

The author's measured scheduling arm used an earlier cost-table commit with the same ordering as the final table. The cache measurement preceded the parameter-name-only amendment. These provenance limits are retained; the exact-head control receipts do not convert those earlier measurements into fresh whole-bank execution.

## Prior public findings

The independent verdict and five-lens ledger were written before querying review submissions/threads. The retrieved PR discussion contained the two review-start comments only; there were no submitted reviews or inline review threads. No prior public FINDINGS on PR #1003 were available to resolve or retain at this head. The author's reference to an earlier rx_filter cache investigation was checked against its published measurements; it is not treated as another reviewer's verdict.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1; hosted acceptance pending) | Issue #998; REQUIREMENTS.md section 8; .github/workflows/rtl.yml:139,633; scripts/mutant_stage.py:54; receipts/public-comparison.jsonl | R924-1 | 13e6d869d842fc06155ef5dae9b0347596d6d4df |
| RTL | CLEAN | receipts/delta.patch; all 38 mutation-driver deltas; unchanged HDL/firmware/gitlinks; receipts/tree-integrity.jsonl | R924-1 | 13e6d869d842fc06155ef5dae9b0347596d6d4df |
| Robustness | UNCLEAN (F1) | scripts/mutant_stage.py:54; scripts/suite_preflight_controls.py; receipts/focused-probes.jsonl; receipts/lifecycle-controls.log | R924-1 | 13e6d869d842fc06155ef5dae9b0347596d6d4df |
| Tests | UNCLEAN (F1) | scripts/mutant_stage.py:114; scripts/ci_make_cases_selftest.py; receipts/controls.json; receipts/cache-probe.log; receipts/public-comparison.jsonl | R924-1 | 13e6d869d842fc06155ef5dae9b0347596d6d4df |
| Docs | UNCLEAN (F1; R1 nonblocking) | docs/testing/TESTING.md:173,254,674; docs/testing/CI_WORKFLOWS.md:486; PR and author evidence sections 1-3 | R924-1 | 13e6d869d842fc06155ef5dae9b0347596d6d4df |

## Limits and remaining manager duties

- Fix F1 and obtain a new independent verdict at the corrected head. No source fixes, commits, pushes, GitHub writes, merges or author contact were performed in this round.
- Establish exact-head hosted/act acceptance and actual job durations below 30 minutes with margin. The one retrieved snapshot showed four queued workflow runs, not successful executed jobs or successful skipped contexts. The inherited Verilator 45/60-minute, physical 145-minute and observer 120-minute timeout settings are not evidence of the issue's 30-minute execution bound. This review does not relabel those unchanged settings as a new defect in the three-commit delta or waive the acceptance criterion.
- The manager owns final candidate validation against the then-current remote dev tip. The supplied live-dev reference was `e275d7950ef3385753e6a15d2e191ba855b171ed`; the reviewed source base remains `fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f`. Record candidate identity and full builder/native/local/hosted receipts at the merge turn. No manager source bank at this exact head is claimed.
- Full parent, processor, timing and synthesis banks were not run. Physical calibration was NOT RUN. Field skips and desktop tests are not hardware proof. Release/physical requirements remain separate.
- Carry R1 to the residue checklist. Complete the remaining independent review, candidate gates, explicit merge authorization and post-merge containment before declaring the task complete.
- Final integrity verification covered 1,974 superproject entries and 1,362 entries across the five initialized submodules. The four mandatory dependency pins and lwSRP are registered and exact. The unused external submodule remains uninitialized. No tracked restoration was necessary because all probes changed only disposable trees.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable. The scratch directory contains disposable trees and is excluded. The manifest uses paths relative to this packet.

R924-1 FINISHED
