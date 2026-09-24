[R293] POSITIVE - exact head b0347a4fd668f8d40bdf40a142ac0ea70167acd1

# R293-2 external independent re-review: issue #514 / PR #552

- **Heads.**
  - Head `b0347a4fd668f8d40bdf40a142ac0ea70167acd1`, tree `6a162c641e5052b523bc8d88cbb13bf3eff1ad47`.
  - Source base `3d2f3e3131c9db5898e1db9dd3e2a35149843109`.
  - Round 1 reviewed `20b7bdaa307eba722ec6cc89d2683ba1636a0cb6`.
- **Sources.** The review used a cleared context and public state only:
  - AGENTS.md; CONTRIBUTING.md 2.1 step 7 (lines 178-271);
  - the #514 body, the manager's decision (issue comment 5789750055), the round-1 and round-2 assignments (5810682208, 5812011094), and the TAKEN and both REVIEW READY comments;
  - the PR #552 body;
  - `git diff 3d2f3e31..b0347a4f`, its three one-line commits, and the round-2 delta `20b7bdaa..b0347a4f`.
- **Lenses.** All five were applied again at this head.
- **Result.** Both round-1 MINOR findings are resolved by executable cases that fail for the defects they name. Behaviour, diagnostics and every existing expectation are unchanged, and no new MINOR or higher finding was found. The verdict is POSITIVE.

## Round-2 change

- **One file changed.** `git diff --raw 20b7bdaa..b0347a4f` touches a single file: `scripts/merge_containment_selftest_linear.py` (mode 100644, blob `357e99b5` becomes `6032fa55`). There are 83 insertions and no deletions (`receipts/diff-and-history.log`).
- **Commit shape.** The new commit `b0347a4f` has a one-line message, one parent (`20b7bdaa`) and no body or trailer.
- **Production code is untouched.** Nothing changed in the checker, replay module, docs, parsing or diagnostics.
- **Self-test result.** The full exact-head self-test passes 799 cases with 0 FAIL and no locale `NOT RUN`, exit 0 (`receipts/head-selftest.log`).
- **Case preservation** (`receipts/selftest-compare.txt`):
  - all 778 round-1 case lines appear verbatim and in their original order;
  - all 678 base case lines appear verbatim and in their original order;
  - the 21 added lines have 21 distinct names, all `linear-*`, and there are no duplicate names.
- **Determinism.** A second run from a `git archive` copy of the head, under `LC_ALL=C`, gives identical case lines (`receipts/head-selftest-archive-LC_C.log`).

## Round-1 findings at this head

### R293-1 F1 (MINOR, `Tests`): RESOLVED

The arm-level unmeasurable result is now reached twice through the CLI.

- **Empty net delta.** `_arm_measurement_cases` (`scripts/merge_containment_selftest_linear.py:148-168`) builds an exact replay of a change and its revert.
  - It checks the default `contained/0`, the optional `UNKNOWN/1`, and the diagnostic `linear retention unmeasurable: retention has no measurable changed-path set`.
- **Failed H read.** Lines 170-195 fail only `rev-list --no-merges`, and the default verdict comes from the path arm.
  - The default run makes 0 failed reads and stays `contained/0`.
  - The optional run makes exactly 1 failed read and gives `UNKNOWN/1`, with the diagnostic `rev-list could not enumerate refs/heads/pr`.
  - So the case provably reaches the arm's H error path rather than passing vacuously.
- **Mutants now killed** (`receipts/mutation-probe.log`):
  - `measurement-except-certifies` fails `linear-empty-delta` and `linear-H-measurement-failure`;
  - `H-error-ignored` fails `linear-H-measurement-failure` and `linear-H-failure-diagnostic`.
- **Additional round-2 mutants, all killed** (`receipts/round2-mutants.log`):
  - `empty-delta-certified`: `_retained_at_tip` returns `[]` instead of raising;
  - `H-error-silently-matched-empty-missing`;
  - `H-error-as-unsupported-noncolliding`: this downgrades an H measurement error to an `unsupported` UNKNOWN, and only the diagnostic pin catches it.
- **Behaviour.** The round-1 fixture probe is byte-identical to round 1. Head gives `UNKNOWN/1`, and the certifying mutant gives `retained/0` (`receipts/probe-unmeasurable.log`).

### R293-1 F2 (MINOR, `Tests`): RESOLVED

Three new sets of cases pin the claim text and the failed-landing behaviour.

- **Ancestry claim.** `linear-ancestry-{optional,default}-claim` (lines 208-214) require exactly one `contained` line. That line must contain both "historical inclusion by ancestry" and "current retention not implied", with and without the option.
- **Retained claim.** `linear-*-retained-claim` (lines 107-113) requires exactly one `retained` line, naming both "raw no-op retention at refs/heads/main" and "historical linear replay proved". It runs for each of the 6 positive examples.
- **Failed landings.** `_failed_landing_cases` (lines 246-260) covers a STRANDED target and an unresolvable (UNKNOWN) target under `--current-retention`. For each it requires:
  - the failed verdict word first, with exit 1;
  - no `retained` line;
  - no `current retention:` line at all.
- **Mutants now killed:**
  - `ancestry-diagnostic-dropped` and `retained-diagnostic-blank` (`receipts/mutation-probe.log`);
  - the round-1 `retained`-beside-STRANDED mutant: its self-test now exits 1 with 2 FAIL (`receipts/probe-stranded-mutant.log`).
- **Additional round-2 mutants, all killed:**
  - `ancestry-disclaimer-dropped` and `ancestry-historical-dropped` (partial wording);
  - `retained-claim-replay-dropped` and `retained-claim-target-dropped`;
  - `retained-line-printed-twice`;
  - `unknown-ref-prints-retained`;
  - `retention-also-evaluated-when-stranded`;
  - `stranded-prints-unknown-retention`.

### Unchanged round-1 mutant set, re-run with the scripts unchanged

The seven round-1 scripts were copied into this packet and verified byte-identical against the round-1 manifest (`receipts/round1-scripts-identity.log`).

| mutant | round 1 (20b7bdaa) | round 2 (b0347a4f) |
|---|---|---|
| control-unmutated | PASS | PASS |
| T-bypass | KILLED | KILLED |
| shape-guard-off | KILLED | KILLED |
| merge-count-digit-guard-off | SURVIVED | SURVIVED (see limits) |
| H-unmatched-accepted | KILLED | KILLED |
| H-error-ignored | SURVIVED | **KILLED** |
| measurement-except-certifies | SURVIVED | **KILLED** |
| missing-list-ignored | KILLED | KILLED |
| retained-diagnostic-blank | SURVIVED | **KILLED** |
| report-unknown-not-counted | KILLED | KILLED |
| report-word-always-retained | KILLED | KILLED |
| option-never-enabled | KILLED | KILLED |
| option-dup-check-dropped | KILLED | KILLED |
| ancestry-diagnostic-dropped | SURVIVED | **KILLED** |
| linear-diagnostic-historical-dropped | KILLED | KILLED |
| retention-uses-default-arm-verdict | KILLED | KILLED |
| mode-rule-dropped | KILLED | KILLED |
| targeted: mode-rule-neutralised | KILLED | KILLED |
| targeted: kind-and-mode-bypassed | KILLED | KILLED |
| retained-beside-STRANDED | SURVIVED | **KILLED** |

- **Totals.** Round 1 killed 14 of 19 mutants; this round kills 18 of 19. Every round-1 kill still dies, and the control passes.
- **Round-2 set.** 13 of my 14 new mutants die for a genuine failing case (`receipts/round2-mutants.log`):
  - One of those 13 (`H-error-as-unsupported`) collides with a guard string used by the self-test's own mutant helper. It aborts the run, so it fails closed, and its non-colliding variant is killed by a genuine case.
  - The one survivor is `pre-error-prints-retained` (S4 below).

## Findings

There are no BLOCKER, MAJOR or MINOR findings at this head.

### Suggestions (non-blocking; they do not affect coverage)

- **R293-S1** (`Docs`, CONTRIBUTING.md:222-231). Retained from round 1; the text is unchanged.
  - Merge-commit landings and #423 redundant-merge landings are documented as outside the optional arm, so `--current-retention --merged-prs` prints `UNKNOWN` for them.
  - One sentence saying this is expected would spare a cold reader the apparent contradiction.
- **R293-S2** (`Robustness`, `scripts/check_merge_containment.py:948-949`). Retained from round 1; not taken, and behaviour is byte-identical (`receipts/probe-options.log`).
  - `--base --current-retention main pr` is accepted as `--base main pr --current-retention`.
  - `--base --no-fetch main pr` is refused. No wrong base results, so only consistency is affected.
- **R293-S3** (`Docs`, docs/testing/RUNNING_TESTS.md:76). Retained from round 1. "It preserves historical linear replay verdicts ..." still follows a sentence about the runner, so "It" is ambiguous.
- **R293-S4 (new)** (`Tests`, `scripts/check_merge_containment.py:884-887`, the `pre_error` branch of `_report`).
  - That UNKNOWN branch is reachable only through a `--merged-prs` pre-error, and no case runs it with `--current-retention`.
  - A mutant that prints a `retained` line there survives (`receipts/round2-mutants.log`).
  - The branch contains no retention code and ends in `continue`. The realistic regressions, evaluating retention for STRANDED or for an unresolved target, are killed. So this is optional hardening: add one sweep case with a pre-error target under the option.

## Per-lens results at b0347a4f

- **[R293] PASS Conformance**
  - **Artifacts:** `scripts/merge_containment_replay.py:157-183`; `scripts/check_merge_containment.py:541,879-915`; CONTRIBUTING.md:208-245; `receipts/probe-matrix.log`; `receipts/probe-options.log`.
  - **Checked against:** the #514 decision, AC1-AC5 and the round-2 assignment.
  - The 42-fixture matrix (31 R242 scenarios plus 11 of my own) is byte-identical to round 1. Default verdicts and exits are identical at base and head.
  - Fixture 30 rebuilds to pr `9a9c1e7b` and main `219aa225`. It gives `contained/0`, and `UNKNOWN/1` naming `'mod.txt'` with the option. The `linear-patch-fallback` replica gives `contained/0`, and `UNKNOWN/1` naming `'linear'` with the option.
  - "No verdict or behaviour change": verified.
- **[R293] PASS RTL**
  - **Artifact:** `receipts/diff-and-history.log`.
  - The base..head raw diff has 8 paths: 4 docs and 4 scripts, one of them added. None is HDL, a constraint or tcl, and no mode changed.
  - The round-2 delta is one test file.
  - The CLI and module contracts are unchanged:
    - exit codes 0/1/2(/3);
    - the `contained()` triple;
    - `scripts/run_all_suites.sh:307` still invokes `--selftest`, and that file is unchanged.
- **[R293] PASS Robustness**
  - **Artifacts:** `receipts/probe-matrix.log`, `receipts/probe-unmeasurable.log`, `receipts/probe-options.log`, and `scripts/merge_containment_selftest_linear.py:148-260`.
  - All malformed, hostile, empty-delta, criss-cross and option-edge probes return the round-1 results byte for byte.
  - The new cases are hermetic:
    - each fixture resets its refs;
    - the `_git` patch is scoped by a context manager and filters exactly one argv prefix;
    - the counter proves the fault fired once.
  - Only S2 (non-blocking) found.
- **[R293] PASS Tests**
  - **Artifacts:** `scripts/merge_containment_selftest_linear.py`; `receipts/head-selftest.log`; `receipts/selftest-compare.txt`; `receipts/mutation-probe.log`; `receipts/targeted-mutants.log`; `receipts/probe-stranded-mutant.log`; `receipts/round2-mutants.log`.
  - F1 and F2 are resolved, with each new case shown to fail for its named defect.
  - The 799 case lines contain all 778 prior case lines verbatim and in order.
  - Only S4 (non-blocking) found.
- **[R293] PASS Docs**
  - **Artifacts:** CONTRIBUTING.md:178-271; AGENTS.md:416; docs/testing/CI_WORKFLOWS.md:1754-1760; docs/testing/RUNNING_TESTS.md:76-80; the PR #552 body; `receipts/doc-gates.log`.
  - These 13 gates all exit 0 at this head:
    - the docs check in both discovery modes;
    - em-dash against the base, and its self-test;
    - style, and its self-test;
    - TOC check, anchors, and its self-test;
    - doc paths;
    - Python idiom, and its self-test;
    - `git diff --check` base..head.
  - CONTRIBUTING.md:227 ("Empty net deltas also remain unmeasurable") and :245 ("The default self-test exercises these examples") are now backed by executable cases.
  - The PR body's round-2 statement that only the linear self-test file changes is accurate.
  - Only S1 and S3 (non-blocking) found.

## Reviewer-owned completion ledger

| lens | result | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | replay.py:157-183; check_merge_containment.py:541,879-915; CONTRIBUTING.md:208-245; 42-fixture matrix; fixture 30 and fallback reproduction; option probes | R293-2 | b0347a4fd668f8d40bdf40a142ac0ea70167acd1 |
| RTL | CLEAN | base..head and round-2 raw diffs (no HDL); CLI/`contained()` contract; run_all_suites.sh:307 | R293-2 | b0347a4fd668f8d40bdf40a142ac0ea70167acd1 |
| Robustness | CLEAN | probe matrix, unmeasurable and option probes (byte-identical to round 1); new-case hermeticity | R293-2 | b0347a4fd668f8d40bdf40a142ac0ea70167acd1 |
| Tests | CLEAN | merge_containment_selftest_linear.py; 799-case self-test (two runs); case-line comparison; 19 round-1 + 14 round-2 reviewer mutants | R293-2 | b0347a4fd668f8d40bdf40a142ac0ea70167acd1 |
| Docs | CLEAN | CONTRIBUTING/AGENTS/CI_WORKFLOWS/RUNNING_TESTS; PR body; 13 doc/idiom gates | R293-2 | b0347a4fd668f8d40bdf40a142ac0ea70167acd1 |

## Prior public findings on PR #552

I read the other reviewer's reports only after the verdict and ledger above were written: R292-1 (PR comment 5811949459, at `20b7bdaa`) and R292-2 (5812395206, POSITIVE at this head, published while this round ran).

As a cross-check, I also ran R292-1's own mutant definitions unchanged. The script is `review-evidence/514-r1/reviews/R292-1/scripts/mutants.py` at `7a00fd14`, sha256 `2909a2ff…4e90b20d`. It runs in disposable shared clones of this review clone. Results are in `receipts/r292-mutants-crosscheck.log`:

- 13 of 15 mutants are KILLED, including M01, M09, M10 and M12.
- M11 and M13 survive, the same pair both reviewers recorded in round 1.

| Prior finding | Disposition at b0347a4f |
|---|---|
| R292-1 F1 MINOR `Tests` (M09, M10): arm-level unmeasurable and H-failure paths untested | **Resolved.** M09 and M10, and my equivalents `H-error-ignored` and `measurement-except-certifies`, are KILLED by `linear-empty-delta`, `linear-H-measurement-failure` and `linear-H-failure-diagnostic`. |
| R292-1 F2 MINOR `Tests` (M01, M12): ancestry wording unpinned; no test forbids `retained` beside STRANDED or UNKNOWN | **Resolved.** M01 and M12, and my equivalents `ancestry-diagnostic-dropped` and `retained-beside-STRANDED`, are KILLED. `unknown-ref-prints-retained` is also KILLED. |
| R293-1 F1 / F2 MINOR `Tests` | **Resolved**, as above. |
| R292-1 S1 / R293-1 S2 SUGGESTION `Robustness`: `--base --current-retention` parsing | Retained as a suggestion; not taken. |
| R292-1 S2 / R293-1 S1 SUGGESTION `Docs`: `UNKNOWN` expected for merge-commit and #423 landings | Retained as a suggestion; not taken. |
| R292-1 S3 / R293-1 S3 SUGGESTION `Docs`: "It" antecedent at RUNNING_TESTS.md:76 | Retained as a suggestion; not taken. |
| R292-2 S4 SUGGESTION `Tests`: pre-resolution UNKNOWN branch unpinned under the option | Same observation as R293-S4, found independently. Retained as a suggestion. |
| R292-1 M11 (merge-count digit guard) / my `merge-count-digit-guard-off` | Survives, not a finding. See the first item under Real limits. |
| R292-1 M13 (summary sentence wording) | Survives, not a finding. The summary line is not a verdict line; each verdict's claim is pinned on its own line. |

These dispositions change neither the verdict nor the ledger.

## Real limits

- **The merge-count guard is untestable without a Git shim.** `merge-count-digit-guard-off` (M11) survives because `git rev-list --count` always prints an integer on success, so the guard cannot be reached. Without the guard, `int()` would raise an uncaught `ValueError`: a traceback with a non-zero exit, never a retention certificate.
- **Hosted checks were inspected, not accepted.** Snapshot at 2026-09-24T10:40:34Z, `receipts/hosted-check-runs.tsv`:
  - 17 completed runs succeeded, among them `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `elaborate`, Yosys shards 0-3/4 and Verilator shards 0, 2 and 3/5.
  - Verilator shards 1/5 and 4/5 were still in progress, so the combined status was `pending`.
  - "Physical gPTP (nightly and manual)" was skipped. A skip is not hardware evidence.
- **Manager bank evidence was not found.** I did not locate receipts for the manager's source static/builder and native banks in `review-evidence/514-r1` at `7a00fd14`, whose contents are author, handoff and reviewer packets. This round does not rely on them.
- **Not run:** any full parent, protocol-processor, gPTP, Yosys or builder bank; Docker/act, host act_ci or its self-test; hardware. Physical calibration is NOT RUN.
- **Scoped Verilator not used.** The scoped Verilator binary was not needed and was neither used nor identity-checked.
- **Tool versions:** Git 2.55.0 and Python 3.14.7 only. The self-test's locale arms ran as shipped, with no `NOT RUN` notice.
- **Source validation only.** This round validates the source at the exact head. It does not validate the final current-dev candidate (source base `3d2f3e31`, live dev `eaf0e6c4`).
- **Clone restored and verified** (`receipts/clone-integrity.log`):
  - HEAD, HEAD tree and index tree equal `6a162c641e5052b523bc8d88cbb13bf3eff1ad47`;
  - index modes and OIDs equal the HEAD tree, and tracked worktree bytes equal HEAD;
  - porcelain status, including ignored files, is empty, and no `__pycache__` exists;
  - the four gitlinks equal the head tree: `external` efeb541a, `gptp-processor` e5dcea6e, `protocol-processor` 424c688f, `third_party/verilog-axis` 48ff7a7e.

  All probes ran on `git archive` copies or disposable shared clones under the packet's scratch directory.

## Pending manager duties

- Publish this report. Merge still needs two independent POSITIVE reviews at the merge head.
- Hosted and act acceptance at the exact head, including the two in-progress Verilator shards.
- Build and gate the current-dev candidate from base `3d2f3e31` and live dev `eaf0e6c4`.
- Maintainer merge authorization, post-merge containment, and closing #514 and moving it to Done.
- Optional: dispose of S1-S4.

## Reproduction (scripts in this packet, paths relative to it)

- `python3 -B mutation_probe.py HEAD_SCRIPTS_DIR SCRATCH GIT_REPO receipts/mutation-probe.json 8` (round-1 set, unchanged)
- `python3 -B targeted_mutants.py HEAD_SCRIPTS_DIR SCRATCH GIT_REPO`
- `python3 -B probe_stranded_mutant.py HEAD_SCRIPTS_DIR SCRATCH GIT_REPO`
- `python3 -B probe_unmeasurable.py HEAD_CHECKER MUTANT_CHECKER ROOT`. MUTANT_CHECKER is the `measurement-except-certifies` copy that `mutation_probe.py` leaves in SCRATCH.
- `python3 -B probe_matrix.py BASE_CHECKER HEAD_CHECKER R242_fixtures.py ROOT receipts/probe-matrix.json`. The R242 `fixtures.py` is `badb350c:readiness-evidence/423/design/R242/scripts/fixtures.py`, sha256 `ec2c6489…d17ff`.
- `sh probe_options.sh HEAD_CHECKER BASE_CHECKER ROOT/rv-two-commit-no-later`
- `python3 -B round2_mutants.py HEAD_SCRIPTS_DIR SCRATCH GIT_REPO receipts/round2-mutants.json 8` (new this round)
- `python3 compare_selftest_cases.py OLD.log receipts/head-selftest.log`
- R292-1 cross-check: `python3 -B mutants.py run GIT_REPO SCRATCH <id>` for each id from `mutants.py list`.

HEAD_SCRIPTS_DIR and BASE_CHECKER come from `git archive <sha> scripts`. GIT_REPO is a clean clone at the head.

R293-2 FINISHED
