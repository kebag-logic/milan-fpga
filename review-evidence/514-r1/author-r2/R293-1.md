[R293] NEGATIVE - exact head 20b7bdaa307eba722ec6cc89d2683ba1636a0cb6

# R293-1 external independent review: issue #514 / PR #552

- Head `20b7bdaa307eba722ec6cc89d2683ba1636a0cb6`, tree `9151db9e2286e15f1b9d46dcbeb95de87dae2e72`; source base `3d2f3e3131c9db5898e1db9dd3e2a35149843109`.
- Reviewed in a cleared context from public state only: AGENTS.md, CONTRIBUTING.md 2.1 step 7, REQUIREMENTS REQ-VER-04, the #514 body, the manager's decision (comment 5789750055) and assignment, the TAKEN and REVIEW READY comments, the PR #552 body, the base..head diff and its two one-line commits, and the immutable R242 evidence at `badb350c`.
- All five lenses were applied independently. Two MINOR findings are open under `Tests`, so the verdict is NEGATIVE. The implementation itself conforms to the decision, and I found no behavioural defect in it.

## What holds

- **Historical verdicts unchanged.** Across 42 deterministic fixtures, base and head give identical default exits and verdict words (`receipts/probe-matrix.log`, invariant I1). The fixtures are the full 31-scenario R242 matrix plus 11 of my own. All 678 base self-test case lines appear verbatim and in order at head. Head adds 100 cases, all named `linear-*` (`receipts/selftest-compare.txt`). No existing self-test file changed except two added lines in `scripts/merge_containment_selftest.py:109,138`.
- **Fixture 30 reproduced.** It rebuilds to pr `9a9c1e7b26ff2d3439ef5c5ec439cc3a13c9a34a` and main `219aa2256e055e8a577f9899ac6d36bd8bd986e0`, the same heads as the immutable R242 `fixture-matrix.json`. It returns `contained/0` at base and at head, and `UNKNOWN/1 ... unproved on: 'mod.txt'` with `--current-retention`. My replica of `linear-patch-fallback` gives `contained/0` by default and `UNKNOWN/1` naming `'linear'` with the option.
- **Optional arm is sound in every probe.** `retained/0` appears only where H and T both hold: two-commit linear replay, far extension, and revert-then-reapply. These are all `UNKNOWN/1`:
  - every reversion, rename, deletion, exec-bit loss, repeated-block relocation and hostile-attribute case;
  - ancestry, merge-shaped and squash-only histories (reported as `unsupported`);
  - an empty net delta (reported as unmeasurable).

  `--current-retention` never changed a non-zero default exit, and never printed `retained` without `contained` (invariant I2).
- **Mutation sensitivity.** The new examples kill mutants that:
  - bypass T;
  - drop the shape guard;
  - accept an unmatched H;
  - ignore the unproved-path list;
  - stop counting UNKNOWN;
  - always print `retained`;
  - never enable the option;
  - drop the duplicate-flag check;
  - drop the "historical inclusion only" wording;
  - substitute the default arm's verdict.

  They also kill two mode/kind mutants I wrote that leave every self-test guard string intact (`receipts/mutation-probe.log`, `receipts/targeted-mutants.log`).

## Findings

### R293-F1: MINOR. The arm-level "unmeasurable, so UNKNOWN" branch is not guarded by any test

- **Lenses:** `Tests`.
- **Location:** `scripts/merge_containment_replay.py:168-180`. These are the `raise _MeasurementError` paths and `except ...: return False, f"linear retention unmeasurable: {exc}"` inside `linear_retention_verdict`.
- **Authority:**
  - #514 AC3: unsupported or unmeasurable cases must not be silently certified.
  - CONTRIBUTING.md:227: "Empty net deltas also remain unmeasurable by this arm."
  - CONTRIBUTING.md:245: "The default self-test exercises these examples and killing mutations."
  - AGENTS section 6, `Tests`: each test can fail for the defect it claims to detect.
- **Evidence:**
  - These mutants each pass the full exact-head self-test (778 ok, `selftest: PASS`, exit 0; `receipts/mutation-probe.log`):
    - `measurement-except-certifies`: the except branch returns `True`;
    - `H-error-ignored`: an H measurement error becomes `matched = True`.
  - On a real fixture the first mutant certifies falsely. Source A then revert(A) are both replayed exactly into the target. At head the checker correctly prints `UNKNOWN ... linear retention unmeasurable: retention has no measurable changed-path set`, exit 1. The mutant prints `retained`, exit 0 (`receipts/probe-unmeasurable.log`).
  - The existing `missing-object-measurement` example fails inside `_retained_at_tip`'s per-path handler and never reaches this branch.
- **Impact:** a regression that turns an arm-level measurement failure into a retention certificate would pass the gate. That covers an empty net delta and a failed H, merge-base or rev-list measurement. This is exactly the unmeasurable-certified outcome AC3 forbids.
- **Required outcome:** executable CLI examples that fail against such mutants. At minimum:
  - an empty-net-delta exact linear replay giving `UNKNOWN/1`;
  - an H measurement failure inside the optional arm giving `UNKNOWN/1`, for example where the default verdict comes from the path arm, which does not call H.
- **Verification:** re-apply both mutants; each must fail the updated self-test.

### R293-F2: MINOR. The new claim-naming diagnostics are not pinned by any test

- **Lenses:** `Tests`.
- **Location:**
  - `scripts/check_merge_containment.py:541`: the ancestry note "historical inclusion by ancestry; current retention not implied".
  - `scripts/merge_containment_replay.py:183`: the `retained` detail "raw no-op retention at ...; historical linear replay proved".
- **Authority:**
  - #514 AC5: diagnostics tell a cold reader which claim each verdict makes.
  - CONTRIBUTING.md:210: "Their `contained` diagnostics explicitly identify that historical claim."
  - AGENTS section 5: add or update self-checking tests for changed behaviour.
- **Evidence:** both mutants survive the full self-test (`receipts/mutation-probe.log`):
  - `ancestry-diagnostic-dropped` restores the old bare `contained` line;
  - `retained-diagnostic-blank` empties the retained detail.

  The linear replay claim is pinned (`linear-*-claim`); these two new claims are not.
- **Impact:** the AC5 wording for the most common landing (ancestry) and for the positive retention result can regress silently.
- **Required outcome:** self-test cases that assert each new claim text, or a stable token of it, through the CLI.
- **Verification:** both mutants fail the updated self-test.

### Suggestions (non-blocking; they do not affect coverage)

- **R293-S1** (`Docs`, CONTRIBUTING.md:222-231).
  - A target landed by the #423 redundant-merge arm already prints "raw no-op retention at ..." on its `contained` line. With the option it also prints `UNKNOWN ... unsupported: source-only history contains merges`, exit 1 (R242 positive fixtures in `receipts/probe-matrix.log`).
  - Ordinary merge-commit landings, which is how this repository's PRs land, are ancestry-only and always give `UNKNOWN/1` under the option.
  - Both are documented exclusions. One sentence saying that `--current-retention --merged-prs` is expected to print `UNKNOWN` for merge-commit landings would spare a cold reader the apparent contradiction.
- **R293-S2** (`Robustness`, `scripts/check_merge_containment.py:948-949`).
  - `--current-retention` is removed before `_take_base`. So `--base --current-retention main pr` is accepted as `--base main pr --current-retention`, exit 0, where the base refused it as an unknown option.
  - `--base --no-fetch main pr` is still refused with "--base needs a ref" (`receipts/probe-options.log`).
  - The flag is not swallowed as the base value, so no wrong base results; the difference is only inconsistency.
- **R293-S3** (`Docs`, docs/testing/RUNNING_TESTS.md:76). "It preserves historical linear replay verdicts ..." follows a sentence about the runner, so "It" is ambiguous. "The containment self-test" would remove the ambiguity.

## Per-lens results

- **[R293] PASS Conformance.**
  - Artifacts: `scripts/merge_containment_replay.py:157-183`, `scripts/check_merge_containment.py:507,541,878-915`, CONTRIBUTING.md:208-245. Checked against the #514 decision/assignment and AC1-3/5.
  - The default historical-inclusion verdict is kept. Retention is a separate, optional H + T result that reuses #423's unchanged `_linear_patches_contained` and `_retained_at_tip`.
  - Behaviour matches the CONTRIBUTING table for exact and partial reversion, extension, supersession, mode, file kind, symlink, gitlink, deletion, binary and missing object.
  - Unsupported histories give `UNKNOWN`, exit 1.
  - AC1 is reproduced at the R242 heads, and the AC4 self-test passes.
- **[R293] PASS RTL.**
  - Artifact: `git diff --raw 3d2f3e31..20b7bdaa` covers 8 files, with no HDL, constraint or tcl path. Existing modes are unchanged, and the new file is `100644`.
  - No RTL changed. The applicable interface contract is the checker CLI and module API. Exit codes stay 0/1/2(/3), and existing refusals are unchanged.
  - `contained()` keeps its triple, and only the ancestry note text changed. Its only callers are `_report` and the self-tests.
  - `scripts/run_all_suites.sh:307` still invokes the unchanged `--selftest` entry.
- **[R293] PASS Robustness.**
  - Artifacts: `receipts/probe-matrix.log`, `receipts/probe-unmeasurable.log`, `receipts/probe-options.log`.
  - These are refused: hostile merge/diff attributes, repeated-block relocation, renames, deletions, exec-bit loss, and a criss-cross source (merge-shaped, before T).
  - An empty net delta gives `UNKNOWN/1`.
  - A duplicate `--current-retention`, and `--current-retention` combined with `--selftest`, both exit 2.
  - Only S2 (non-blocking) found.
- **[R293] UNCLEAN Tests.** Artifacts: `scripts/merge_containment_selftest_linear.py`, `receipts/head-selftest.log`, `receipts/mutation-probe.log`, `receipts/probe-stranded-mutant.log`. F1 and F2 are open, and so is the retained R292-F2 item (no test forbids `retained` beside `STRANDED`); see below.
- **[R293] PASS Docs.**
  - Artifacts: CONTRIBUTING.md:208-245 and 269-271; AGENTS.md:416; docs/testing/CI_WORKFLOWS.md:1754-1760; docs/testing/RUNNING_TESTS.md:76-80; the module docstrings.
  - Each verdict's claim is stated, and the decision link resolves to the manager's 2026-09-23 decision.
  - These all exit 0 (`receipts/doc-gates.log`): the docs check in both discovery modes, em-dash against the base, style, TOC, anchors, paths, Python idiom and `diff --check`.
  - Only S1 and S3 (non-blocking) found.

## Reviewer-owned completion ledger

| lens | result | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | replay.py:157-183; check_merge_containment.py:507,541,878-915; CONTRIBUTING.md:208-245; fixture 30 and fallback reproduction | R293-1 | 20b7bdaa307eba722ec6cc89d2683ba1636a0cb6 |
| RTL | CLEAN | base..head raw diff (no HDL); CLI and `contained()` contract; run_all_suites.sh:307 | R293-1 | 20b7bdaa307eba722ec6cc89d2683ba1636a0cb6 |
| Robustness | CLEAN | 42-fixture probe matrix; unmeasurable probe; option-parsing probes | R293-1 | 20b7bdaa307eba722ec6cc89d2683ba1636a0cb6 |
| Tests | UNCLEAN (F1, F2) | merge_containment_selftest_linear.py; base/head self-test logs; 17 + 2 + 1 reviewer mutants | R293-1 | 20b7bdaa307eba722ec6cc89d2683ba1636a0cb6 |
| Docs | CLEAN | CONTRIBUTING/AGENTS/CI_WORKFLOWS/RUNNING_TESTS diffs; docstrings; doc gates | R293-1 | 20b7bdaa307eba722ec6cc89d2683ba1636a0cb6 |

## Prior public findings on PR #552

I read these only after the verdict and ledger above were written. At that point the only prior review round was R292-1 (PR comment 5811949459, NEGATIVE at the same head). The head has not changed, so none of its findings can be resolved; each is disposed of below.

| Prior finding | Disposition at 20b7bdaa |
|---|---|
| R292 F1 MINOR `Tests`: arm-level unmeasurable and H-failure paths lack examples | **Retained.** Same defect as R293-F1, reproduced independently (`measurement-except-certifies`, `H-error-ignored`, and the empty-net-delta fixture). |
| R292 F2 MINOR `Tests`: ancestry wording unpinned | **Retained.** Same defect as R293-F2 (`ancestry-diagnostic-dropped`). |
| R292 F2 MINOR `Tests`: no test forbids a retention line beside a STRANDED/UNKNOWN target | **Retained. I had not found this one myself.** I reproduced it independently: a mutant that prints `retained` beside `STRANDED` passes the full self-test (exit 0, 0 FAIL). On a stranded fixture the head prints only `STRANDED`, exit 1, while the mutant prints `STRANDED` then `retained` (`receipts/probe-stranded-mutant.log`). R293-F2's required outcome now also covers this: under `--current-retention`, a STRANDED or UNKNOWN target emits no `retained` line. |
| R292 S1 SUGGESTION `Robustness`: `--base --current-retention` parsing | Retained as a suggestion; same as R293-S2. |
| R292 S2 SUGGESTION `Docs`: the sweep is UNKNOWN for merge-commit and #423 landings | Retained as a suggestion; same as R293-S1. |
| R292 S3 SUGGESTION `Docs`: "It" antecedent in RUNNING_TESTS.md:76 | Retained as a suggestion; same as R293-S3. |

Retaining these changes neither the verdict nor the ledger: the `Tests` lens was already UNCLEAN.

## Real limits

- **Hosted checks were inspected, not accepted.** Snapshot at 2026-09-24T10:00:02Z, `receipts/hosted-check-runs.tsv`:
  - 18 runs completed with success, including `rtl-fast`, docs checks, lint, elaboration, BDD, Verilator shards 0-3/5 and Yosys shards 0-3/4.
  - "Verilator shard 4/5" was still in progress.
  - "Physical gPTP (nightly and manual)" was skipped by schedule. A skip is not hardware evidence.
- **Not run:** any full parent, protocol-processor, gPTP, Yosys or builder bank; Docker/act, host act_ci or its self-test; hardware. Physical calibration is NOT RUN. The scoped Verilator binary was not needed and was not used.
- **Tool versions:** probes ran with Git 2.55.0 and Python 3.14.7 only.
- **Locale arms:** the self-test's locale arms ran on this host as shipped, with no locale NOT RUN notice in `receipts/head-selftest.log`.
- **Harness abort on colliding mutants.** Some mutants (T-bypass, mode-rule-dropped) remove text that the self-test's own mutation helpers look up. Those helpers then raise and abort the rest of the run, which fails closed. Each such mutant was killed by a genuine failing case before the abort. The mode and kind rules were re-checked with non-colliding mutants (`receipts/targeted-mutants.log`): `linear-mode-loss` and `linear-file-kind-change` kill them.
- **Unreachable path:** the "exactly one merge base" refusal cannot be reached by this arm. A merge-free source-only range has a unique fork parent, and the criss-cross probe is refused earlier as merge-shaped.
- **Source validation only.** This round validates the source at the exact head. It does not validate the final current-dev candidate.
- **Clone restored.** HEAD, HEAD tree and index tree all equal `9151db9e2286e15f1b9d46dcbeb95de87dae2e72`. Porcelain status, including ignored files, is empty. There are no index or worktree differences, and the four gitlinks equal the base (`receipts/clone-integrity.log`). The one reviewer-created artifact, `scripts/__pycache__` from the gate runs, was removed.

## Pending manager duties

- Publish this report. After F1/F2 (and the retained R292 items) are fixed at a new head, `Tests` needs re-review there.
- Decide at that head whether `Robustness` or `Conformance` scope was touched.
- Hosted and act acceptance at the merge head, including the in-progress Verilator shard 4/5.
- Build and gate the current-dev candidate (source base `3d2f3e31`, live dev `9d328810`).
- Obtain a second independent POSITIVE, run post-merge containment, and close the Issue.

## Reproduction (scripts in this packet, paths relative to it)

- `python3 -B probe_matrix.py BASE_CHECKER HEAD_CHECKER R242_fixtures.py ROOT receipts/probe-matrix.json`. The R242 `fixtures.py` is blob `ed1af35d` at `badb350c:readiness-evidence/423/design/R242/scripts/fixtures.py`, sha256 `ec2c6489…d17ff`.
- `python3 -B mutation_probe.py HEAD_SCRIPTS_DIR SCRATCH GIT_REPO receipts/mutation-probe.json 8`
- `python3 -B targeted_mutants.py HEAD_SCRIPTS_DIR SCRATCH GIT_REPO`
- `python3 -B probe_unmeasurable.py HEAD_CHECKER MUTANT_CHECKER ROOT`
- `python3 -B probe_stranded_mutant.py HEAD_SCRIPTS_DIR SCRATCH GIT_REPO`
- `sh probe_options.sh HEAD_CHECKER BASE_CHECKER FIXTURE_REPO`
- `python3 compare_selftest_cases.py receipts/base-selftest.log receipts/head-selftest.log`

HEAD_SCRIPTS_DIR and BASE_CHECKER come from `git archive <sha> scripts`. GIT_REPO is any clean clone, which the checker needs for its graft check.

R293-1 FINISHED
