[A251] Round 2 author handoff: PR #552 / Issue #514

## Head and scope

- Branch: `514-containment-retention`.
- Starting head: `20b7bdaa307eba722ec6cc89d2683ba1636a0cb6`.
- Review-ready head: `b0347a4fd668f8d40bdf40a142ac0ea70167acd1`; tree `6a162c641e5052b523bc8d88cbb13bf3eff1ad47`.
- Local commit: `test(containment): cover unmeasurable retention and scoped claims`.
- One-line subject, no body or trailers. One file changed, 83 insertions.
- Only `scripts/merge_containment_selftest_linear.py` changed. Production verdicts, parsing, diagnostic wording, documentation, and every existing test expectation remain unchanged.
- [Assignment](https://github.com/kebag-logic/milan-fpga/issues/514#issuecomment-5812011094), [R292-1](https://github.com/kebag-logic/milan-fpga/pull/552#issuecomment-5811949459), [R293-1](https://github.com/kebag-logic/milan-fpga/pull/552#issuecomment-5811996262).

## Assigned outcomes

| Finding | Added executable evidence | Outcome |
|---|---|---|
| F1: arm-level unmeasurable result | `linear-empty-delta`: distinct exact replays of source change and revert, with empty net source delta | Optional `UNKNOWN/1`; explicit arm-level diagnostic; default landing still `contained/0` |
| F1: H measurement failure | `linear-H-measurement-failure`: real exact-path landing, then injected failure of H's Git source enumeration | Optional `UNKNOWN/1`; failing Git read observed once; default path proof does not call it |
| F2: ancestry claim | `linear-ancestry-default-claim` and `linear-ancestry-optional-claim` | The `contained` line itself names historical inclusion and disclaims current retention |
| F2: no retention on failed landing | STRANDED source and nonexistent UNKNOWN target, both with the option | Failed landing and exit 1 preserved; no `retained` line or optional retention result |
| R293-F2: positive retained detail | Six positive retained examples | The `retained` line names raw current retention at the target and historical replay |

Optional parsing suggestion R292-S1 / R293-S2 was not taken. Other documentation suggestions remain outside the assigned tests-only change. These are author evidence claims, not review verdicts or a reviewer-owned coverage ledger.

## Existing self-test preservation

The committed head passes **799/799** full self-test cases. All **778** case lines at `20b7bdaa307eba722ec6cc89d2683ba1636a0cb6` are preserved verbatim and in order, verified independently against both archived reviewer logs. The original **678** base case lines are also preserved verbatim and in order. The change adds **21** checks.

The linear entry point passes **121** linear checks plus **12** shared preflight/cleanup checks (133 total). `run_linear.py` selects `linear_retention_cases` through the existing fixture harness. No locale arm reported `NOT RUN`.

Receipts: [full self-test](gates/selftest.log), [linear entry point](gates/linear.log), [case comparison](case-comparison.json), [patch](round2.patch).

## Mutation method and provenance

Before results are the reviewers' published runs at `20b7bdaa307eba722ec6cc89d2683ba1636a0cb6`, copied from these immutable archives:

- R292-1: `185549cf74b00568f5462f57961d1de8ad52dc38`, `review-evidence/514-r1/reviews/R292-1/`.
- R293-1: `c3d6a0e682bff1fe50121528e4d8ef991f10845b`, `review-evidence/514-r1/reviews/R293-1/`.

After results are new runs against script bytes exported from `b0347a4fd668f8d40bdf40a142ac0ea70167acd1`. All four copied reviewer scripts were verified byte-identical to their archive blobs; see [script integrity](script-integrity.json).

The R292 runner ordinarily creates a shared clone. To obey the no-other-checkouts instruction, `run_r292_no_checkout.py` imports its unchanged `MUTANTS` table and applies each exact replacement to a disposable scripts copy, then runs the full self-test from the assigned repository. Every mutation site must occur exactly once. No mutant definition or expected outcome was changed. R293's main, targeted, and STRANDED runners ran unchanged with their documented arguments. The unmutated R293 control passes.

All commands ran in foreground processes and were awaited. Recorded gates wrote raw output to files, without shell pipelines. Mutant scripts and disposable copies lived under the single scratch directory recorded in `scratch-path.txt`; its removal is recorded in `cleanup.json` before the review-ready comment.

### R292-1 before/after

| Mutant | Before | After | After rc | Failing cases |
|---|---|---|---:|---:|
| `M01-ancestry-note-dropped` | SURVIVED | KILLED | 1 | 2 |
| `M02-linear-note-unqualified` | KILLED | KILLED | 1 | 10 |
| `M03-retention-unknown-not-counted` | KILLED | KILLED | 1 | 16 |
| `M04-retention-word-always-retained` | KILLED | KILLED | 1 | 16 |
| `M05-option-ignored` | KILLED | KILLED | 1 | 58 |
| `M06-option-dup-check-removed` | KILLED | KILLED | 1 | 1 |
| `M07-missing-ignored` | KILLED | KILLED | 1 | 22 |
| `M08-one-merge-allowed` | KILLED | KILLED | 1 | 1 |
| `M09-H-measurement-failure-certifies` | SURVIVED | KILLED | 1 | 2 |
| `M10-measurement-error-certifies` | SURVIVED | KILLED | 1 | 2 |
| `M11-merge-count-parse-guard-removed` | SURVIVED | SURVIVED | 0 | 0 |
| `M12-retention-on-stranded` | SURVIVED | KILLED | 1 | 2 |
| `M13-summary-requested-proof-wording` | SURVIVED | SURVIVED | 0 | 0 |
| `M14-historical-linear-verdict-withdrawn` | KILLED | KILLED | 1 | 66 |
| `M15-H-refusal-falls-through-to-T` | KILLED | KILLED | 1 | 3 |

R292: **9 -> 13 killed, of 15**. M01, M09, M10, and M12 now fail genuine new cases. Every previous kill remains killed. The unchanged survivors are M11 (merge-count digit parsing, not an assigned finding) and M13 (summary wording, not a contract in the review).

Receipts: [before](before/R292-1/mutants.log), [after JSON](after/R292-1/mutants.json); full per-mutant logs are beside that JSON.

### R293-1 before/after

| Mutant | Before | After | After rc | Failing cases |
|---|---|---|---:|---:|
| `control-unmutated` | PASS | PASS | 0 | 0 |
| `T-bypass` | KILLED | KILLED | 1 | 2 |
| `shape-guard-off` | KILLED | KILLED | 1 | 1 |
| `merge-count-digit-guard-off` | SURVIVED | SURVIVED | 0 | 0 |
| `H-unmatched-accepted` | KILLED | KILLED | 1 | 3 |
| `H-error-ignored` | SURVIVED | KILLED | 1 | 2 |
| `measurement-except-certifies` | SURVIVED | KILLED | 1 | 2 |
| `missing-list-ignored` | KILLED | KILLED | 1 | 22 |
| `retained-diagnostic-blank` | SURVIVED | KILLED | 1 | 6 |
| `report-unknown-not-counted` | KILLED | KILLED | 1 | 16 |
| `report-word-always-retained` | KILLED | KILLED | 1 | 16 |
| `option-never-enabled` | KILLED | KILLED | 1 | 58 |
| `option-dup-check-dropped` | KILLED | KILLED | 1 | 1 |
| `ancestry-diagnostic-dropped` | SURVIVED | KILLED | 1 | 2 |
| `linear-diagnostic-historical-dropped` | KILLED | KILLED | 1 | 10 |
| `retention-uses-default-arm-verdict` | KILLED | KILLED | 1 | 38 |
| `mode-rule-dropped` | KILLED | KILLED | 1 | 2 |
| `mode-rule-neutralised` | KILLED | KILLED | 1 | 6 |
| `kind-and-mode-bypassed` | KILLED | KILLED | 1 | 16 |
| `retained-beside-stranded` | SURVIVED | KILLED | 1 | 2 |

R293: **13 -> 18 killed, of 19**, plus a passing unmutated control. This includes both targeted mutants and the separate STRANDED mutant. Every required equivalent is killed, including the blank retained diagnostic, and every previous kill remains killed. The merge-count digit-guard mutant remains the sole survivor.

Receipts: [before main set](before/R293-1/mutation-probe.json), [after main set](after/R293-1/mutation-probe.json), [targeted](after/R293-1/targeted-mutants.log), [STRANDED](after/R293-1/probe-stranded-mutant.log). Full main-set logs are beside its JSON.

Some existing broad mutants still collide with the self-test's own source-mutation guard strings and subsequently abort. Each killed mutant first records at least one genuine failing test case. The two targeted mutations preserve those guard strings and still fail the mode/kind examples. No kill is credited solely to an exception.

## Gate table

All gates ran at `b0347a4fd668f8d40bdf40a142ac0ea70167acd1` and returned 0. `PYTHONDONTWRITEBYTECODE=1` was set for the gates; disposable bytecode caches were removed after validation. The no-Git docs mode uses the same filesystem discovery path as its CI mode.

| Gate command | rc | Receipt |
|---|---:|---|
| `python3 scripts/check_merge_containment.py --selftest` | 0 | [selftest](gates/selftest.log) |
| `python3 -B $MANAGEMENT/2026-09-23/514-a251/run_linear.py $LANES/514-containment-retention/scripts` | 0 | [linear](gates/linear.log) |
| `python3 scripts/docs_check.py` | 0 | [docs-git](gates/docs-git.log) |
| `GIT_DIR=/dev/null python3 scripts/docs_check.py` | 0 | [docs-no-git](gates/docs-no-git.log) |
| `python3 scripts/check_em_dash.py --base 3d2f3e3131c9db5898e1db9dd3e2a35149843109` | 0 | [em-dash](gates/em-dash.log) |
| `python3 scripts/check_doc_style.py` | 0 | [doc-style](gates/doc-style.log) |
| `python3 scripts/gen_toc.py --check` | 0 | [toc](gates/toc.log) |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | [anchors](gates/anchors.log) |
| `python3 scripts/check_doc_paths.py` | 0 | [doc-paths](gates/doc-paths.log) |
| `python3 scripts/check_py_idiom.py` | 0 | [python-idiom](gates/python-idiom.log) |
| `git diff --check` | 0 | [diff-check](gates/diff-check.log) |
| `git diff --check 3d2f3e3131c9db5898e1db9dd3e2a35149843109 HEAD` | 0 | [diff-check-base](gates/diff-check-base.log) |

The receipt comparison helper initially matched `FAILS` inside a passing case description. Its result-line check was corrected and the comparison alone rerun successfully; no repository test or expectation changed. Individual gate exits were all 0 throughout.

## Reproduction

Run from the assigned lane. Export `HEAD:scripts` and the two immutable reviewer packets into a fresh scratch directory before the mutation commands. `$PACKET` below is this output directory, `$SCRATCH` is that temporary directory, and `$REPO` is the assigned lane.

```sh
python3 -B -u "$PACKET/run_gates.py"
python3 -B -u "$PACKET/run_r292_no_checkout.py" "$SCRATCH/review-evidence/514-r1/reviews/R292-1/scripts/mutants.py" "$SCRATCH/head/scripts" "$SCRATCH/r292-after" "$REPO" "$PACKET/after/R292-1"
python3 -B -u "$SCRATCH/review-evidence/514-r1/reviews/R293-1/mutation_probe.py" "$SCRATCH/head/scripts" "$SCRATCH/r293-after" "$REPO" "$PACKET/r293-after.json" 4
python3 -B -u "$SCRATCH/review-evidence/514-r1/reviews/R293-1/targeted_mutants.py" "$SCRATCH/head/scripts" "$SCRATCH/r293-targeted" "$REPO"
python3 -B -u "$SCRATCH/review-evidence/514-r1/reviews/R293-1/probe_stranded_mutant.py" "$SCRATCH/head/scripts" "$SCRATCH/r293-stranded" "$REPO"
```

## Remaining workflow and limits

The local worktree is clean at the named head. No push, PR edit, merge, other checkout, sub-agent, hardware run, or local workflow replay was performed. The existing checker self-tests create their own disposable Git fixtures as part of the required gate.

`PR-BODY.md` is the complete replacement body for manager publication. Independent re-review, reviewer-owned coverage decisions, publication, hosted evidence, required local workflow replication, current-dev candidate validation, merge authorization, and post-merge containment remain pending. This handoff supplies no review verdict or completion ledger.
