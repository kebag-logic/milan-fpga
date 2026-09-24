[R292] NEGATIVE - exact head 20b7bdaa307eba722ec6cc89d2683ba1636a0cb6

# R292-1 independent review: PR #552 for Issue #514

- Role: cleared-context internal independent reviewer, round R292-1.
- Exact head: `20b7bdaa307eba722ec6cc89d2683ba1636a0cb6`, tree `9151db9e2286e15f1b9d46dcbeb95de87dae2e72`.
- Source base: `3d2f3e3131c9db5898e1db9dd3e2a35149843109`. Two one-line commits with no bodies or trailers: `3f2fe73d1`, `20b7bdaa3`.
- Authorities read: AGENTS.md, CONTRIBUTING.md 2.1 step 7, docs/README.md, and the Issue #514 body. Also the decision comment [5789750055](https://github.com/kebag-logic/milan-fpga/issues/514#issuecomment-5789750055), assignment 5810682208, TAKEN 5810713843 and REVIEW READY 5810954305. Then the PR #552 body, the full base-to-head diff and history, the R242 fixture builder at `badb350c`, public evidence at `bc03c9fe` `review-evidence/514-r1`, and the exact-head hosted check runs.
- Prior public review findings on PR #552: none. At the time of this review the only PR comments were the two review-start notices, 5811720017 and 5811746086. Nothing needed resolving or retaining.

## Verdict basis

The implementation does what the recorded decision asks:
- Linear replay keeps its historical `contained/0` verdict.
- `--current-retention` adds a separate `retained` or `UNKNOWN` line, built from #423's unchanged H and T.
- Every existing self-test line is preserved verbatim.
- Every probed behaviour matches CONTRIBUTING 2.1 step 7.

The verdict is NEGATIVE only because the Tests lens is unclean. Two MINOR findings (F1, F2) describe new-arm contracts that no self-test pins, and each is shown by a mutant that survives the full default self-test. The current code behaves correctly on all of them.

## Findings

### F1 MINOR (Tests): arm-level "unmeasurable" and H-failure paths have no executable example; certifying mutants survive

- Lenses: Tests.
- Location: `scripts/merge_containment_replay.py:174-180` (`linear_retention_verdict`: `matched is None` and the `except` handler) and `scripts/merge_containment_selftest_linear.py:122-219`. The latter has no case that reaches either path. The documented claim sits at `CONTRIBUTING.md:227`: "Empty net deltas also remain unmeasurable by this arm."
- Authority:
  - The Issue #514 acceptance says unsupported or unmeasurable cases are reported and never certified.
  - AGENTS section 5 asks for self-checking tests on changed behaviour.
  - The author's claim is that every negative example rejects a mutant of the new arm.
- Evidence (`receipts/mutants.log`, `scripts/mutants.py`):
  - **M10** changes the arm's `except` handler to `return True`. It SURVIVES the full self-test: exit 0, 0 FAIL.
  - **M09** treats an unmeasured H (`matched is None`) as a match. It also SURVIVES.
  - With M10, the behaviour probe `net-zero-source-delta` prints `retained ... linear retention unmeasurable: retention has no measurable changed-path set` and exits 0 (`receipts/probe-behaviour-M10-measurement-error-certifies.log`).
  - At the exact head the same scenario correctly reports `UNKNOWN`, exit 1 (`receipts/probe-behaviour-head.log`).
  - The only unmeasurable example in the self-test is an object read failure. It is attributed per path inside `_retained_at_tip` and never reaches the arm's own handler.
- Impact: a regression that certifies unmeasurable retention would pass the gate that guards this arm, including the documented empty-net-delta case. The acceptance says that must never happen.
- Required outcome: the default self-test contains at least one executable case that reaches the arm-level unmeasurable result (for example, an exact linear replay with an empty net source delta). It also contains one case where the H measurement itself fails under `--current-retention`. Both expect `UNKNOWN`/1 and fail against M10-class and M09-class mutants.
- Verification: rerun `python3 -B scripts/mutants.py run <clone> <scratch> M10-measurement-error-certifies` and `M09-H-measurement-failure-certifies` against the fixed head. Both must be KILLED, and the unchanged 678 base case lines must still pass.

### F2 MINOR (Tests): two claim-scoping contracts are unpinned (the ancestry claim wording, and no retention line for a non-contained target)

- Lenses: Tests.
- Location: `scripts/check_merge_containment.py:541` (the ancestry note) and `scripts/check_merge_containment.py:893-898` (retention is evaluated only on the `contained` branch). The matching doc claims are at `CONTRIBUTING.md:210` ("Their `contained` diagnostics explicitly identify that historical claim.") and at `CONTRIBUTING.md` step 7 ("Each successful landing verdict keeps its own `contained` line. The option adds `retained` or `UNKNOWN`").
- Authority: Issue #514 acceptance item 5 (diagnostics tell a cold reader which claim each verdict makes) and AGENTS section 5.
- Evidence:
  - **M01** restores the base's note-less ancestry line. It SURVIVES the full self-test: exit 0, 0 FAIL.
  - With M01, the ancestry verdict prints a bare `contained  refs/heads/pr` with no historical qualifier (`receipts/probe-behaviour-M01-ancestry-note-dropped.log`). The linear-replay qualifier is pinned; M02 is killed by 10 `-claim` cases.
  - **M12** prints a `retained` line for a STRANDED target. It SURVIVES: no self-test runs `--current-retention` against a STRANDED or UNKNOWN landing target.
  - With M12, the probe `stranded-with-option` shows `STRANDED` followed by `retained` (`receipts/probe-behaviour-M12-retention-on-stranded.log`). At the exact head it correctly shows `STRANDED` only.
- Impact: the acceptance-item-5 wording for the ancestry claim, and the guarantee that a retention certificate never appears beside a failed landing, can both regress silently. Exit codes stay correct under M12, but the printed claim would be false.
- Required outcome: the self-test checks two things.
  - The ancestry `contained` diagnostic names historical inclusion and disclaims current retention.
  - `--current-retention` on a STRANDED (or UNKNOWN) landing target emits no `retained` line.
- Verification: M01 and M12 from `scripts/mutants.py` are KILLED at the fixed head.

### Suggestions (optional; they do not affect lens coverage)

- **S1 SUGGESTION (Robustness):** `scripts/check_merge_containment.py:948-949` against `:747-751`.
  - `--current-retention` is removed before `_take_base`, so `--base --current-retention main pr` is accepted as `--base main pr` (`receipts/probe-behaviour-head.log`, `base-flag-then-option`).
  - The existing contract refuses `--base <flag>` with exit 2. The outcome is benign, but parsing is now inconsistent across flags.
- **S2 SUGGESTION (Docs):** `CONTRIBUTING.md:219` recommends `--current-retention --merged-prs`.
  - On this repository's ordinary merge-commit landings every PR head is an ancestor, so the arm reports `UNKNOWN`/1 by design for every ancestry-landed PR (`ancestry-with-option` probe).
  - A #423 redundant-merge `contained` line, which already carries raw retention, is likewise followed by `UNKNOWN ... unsupported: source-only history contains merges`.
  - The exclusions are stated at `:226`. One sentence saying the sweep is expected to be `UNKNOWN` for such landings would stop a cold reader from taking exit 1 as a regression.
- **S3 SUGGESTION (Docs):** `docs/testing/RUNNING_TESTS.md:76` "It preserves historical linear replay verdicts..." follows a sentence whose subject is the runner. Naming "The containment self-test" would remove the ambiguity.

## Lens results (clean lenses, evidence format)

- `[R292] PASS Conformance` — evidence: Issue #514 decision 5789750055 and acceptance 1-5, against the diff and `receipts/repro-fixtures-{head,base}.log`, `receipts/probe-behaviour-head.log` and `receipts/selftest-case-compare.log`.
  - **Acceptance 1:** fixture 30 (`linear-control-exact-revert`) was rebuilt from the immutable R242 builder (sha256 `ec2c6489...d17ff`). It reproduces source `9a9c1e7b26ff2d3439ef5c5ec439cc3a13c9a34a` and target `219aa2256e055e8a577f9899ac6d36bd8bd986e0`, matching R242's `fixture-matrix.json` byte for byte.
    - Base and head both return `contained`, exit 0. Head's text names "historical inclusion only".
    - With `--current-retention`, head returns `UNKNOWN`, exit 1, "unproved on: 'mod.txt'".
    - A `linear-patch-fallback` replica gives `contained/0` on both base and head, and `UNKNOWN`/1 naming `'linear'` with the option. So does fixture 31.
    - The base checker refuses the option with exit 2, so the arm is new.
  - **Acceptance 2:** the decision was published before implementation, and no existing expectation changed. All 678 base self-test lines, name and description, are present verbatim at head and pass. The 100 added lines are all `linear-*`. The only edit to existing self-test modules is a +2 import-and-call hook.
  - **Acceptance 3:** the examples cover exact and partial reversion, extension, supersession (with "intent" in the commit message), mode loss and later mode change, file kind, symlink and gitlink identity and reversion, binary, deletion, object-read failure, and ancestry, merge and squash histories. The unsupported cases report `UNKNOWN`/1.
  - **Acceptance 5:** see Docs.
  - The arm reuses #423's `_retained_at_tip` and `_linear_patches_contained` unchanged, which is the "#423 shape" the decision named.
- `[R292] PASS RTL` — evidence: `receipts/clone-integrity.log`, the base-to-head raw diff.
  - The diff touches no HDL, constraint, testbench, build or gitlink artifact. The eight changed paths are Markdown and Python tooling, and the four submodule gitlinks (external `efeb541a`, gptp-processor `e5dcea6e`, protocol-processor `424c688f`, verilog-axis `48ff7a7e`) are unchanged against the base.
  - The tooling interface contracts this lens protects still hold:
    - Exit codes are still 0/1/2, plus self-test cleanup status 3.
    - `run_all_suites.sh:307` still calls the unchanged `--selftest` entry.
    - The `replay_verdict` signature and behaviour are unchanged.
    - No other script parses `contained` output (repository search).
  - Verilator was not needed and was not used.
- `[R292] PASS Robustness` — evidence: `scripts/merge_containment_replay.py:157-183` and `scripts/check_merge_containment.py:879-914` at head, exercised by `receipts/probe-behaviour-head.log` (12 scenarios, PROBES PASS). Each case below reports as stated:
  - A net-zero source delta: `UNKNOWN` "unmeasurable".
  - Criss-cross or merge-bearing sources: `UNKNOWN` "unsupported".
  - A STRANDED target with the option: no retention line, exit 1.
  - A squash or path-arm landing, and an ancestry landing: `UNKNOWN` "unsupported".
  - A rename that is reverted: both paths named. A rename that is retained: `retained`/0.
  - An exact revert under an `ours` merge driver with a quiet textconv: `UNKNOWN`. Attributes provide no proof.
  - A duplicated `--current-retention`, or combining it with `--selftest`: exit 2 (the self-test covers both).
  - Any unresolved target makes the command exit 1.
  - The one parsing inconsistency found is benign and is filed as S1.
  - Proving that a linear source-only range cannot have two merge bases shows the "exactly one merge base" refusal is unreachable for this arm. It is not a gap.
- `[R292] UNCLEAN Tests`: F1 and F2 above.
  - Also applied: 15 reviewer mutants run against the full default self-test at head (`receipts/mutants.log`).
    - **KILLED:** M02 (linear claim wording), M03 (UNKNOWN not counted), M04 (word always `retained`), M05 (option ignored), M06 (duplicate-flag check), M07 (`missing` ignored), M08 (one merge allowed), M14 (historical linear verdict withdrawn: 64 FAIL, including existing `linear-patch-fallback` and `replay-30`) and M15 (H refusal falls through to T; killed by `linear-squash-unsupported`).
    - **SURVIVED:** M01, M09, M10 and M12 are covered by F1 and F2. M11 (the merge-count digit guard) is not reachable without a Git shim. M13 (summary sentence wording) is not a contract.
  - The self-test passes at head: 778 case lines, 0 non-ok, exit 0, in 35 s (`receipts/selftest-head.log`). The base passes 678 (`receipts/selftest-base.log`).
- `[R292] PASS Docs` — evidence: `CONTRIBUTING.md:207-245`, `docs/testing/CI_WORKFLOWS.md:1754-1760`, `docs/testing/RUNNING_TESTS.md:76-80`, `AGENTS.md:416`, and the checker and replay module docstrings at head. Each claim was checked against observed behaviour:
  - historical inclusion for ancestry and linear replay;
  - current identity for path equality;
  - an empty source delta for net-zero;
  - `retained` or `UNKNOWN` as an optional separate line;
  - the exclusions and exit 1;
  - each row of the reversion, extension, supersession, mode, kind and binary table;
  - supersession intent is never evidence.
  - The #514 link resolves to the manager's decision comment.
  - The doc gates exit 0 at head (`receipts/doc-gates-head.log`): docs_check in both discovery modes, em-dash against the base, doc style, the TOC check and anchors, doc paths, Python idiom, and `git diff --check`.
  - Suggestions S2 and S3 are optional.

## Reviewer-owned completion ledger (this round)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #514 decision/acceptance; fixture 30/31 and linear-patch-fallback reproductions base vs head; 678/678 preserved case lines | R292-1 | 20b7bdaa307eba722ec6cc89d2683ba1636a0cb6 |
| RTL | CLEAN | Base-to-head raw diff (no HDL/gitlink change); gitlinks; exit-code and entry-point contracts; `run_all_suites.sh:307` | R292-1 | 20b7bdaa307eba722ec6cc89d2683ba1636a0cb6 |
| Robustness | CLEAN | `merge_containment_replay.py:157-183`, `check_merge_containment.py:879-949`; 12 behaviour probes | R292-1 | 20b7bdaa307eba722ec6cc89d2683ba1636a0cb6 |
| Tests | UNCLEAN (F1, F2 MINOR) | `merge_containment_selftest_linear.py`; full self-test base/head; 15 mutants | R292-1 | 20b7bdaa307eba722ec6cc89d2683ba1636a0cb6 |
| Docs | CLEAN | CONTRIBUTING 2.1 step 7, CI_WORKFLOWS, RUNNING_TESTS, AGENTS, module docstrings; 9 doc/idiom gates | R292-1 | 20b7bdaa307eba722ec6cc89d2683ba1636a0cb6 |

A fix commit for F1 or F2 that touches only self-test modules changes the Tests scope. Whether it also un-covers Robustness or Conformance depends on the artifacts that commit touches, and a later round decides that at the new head.

## Real limits

- Hosted exact-head checks were inspected, not accepted (`receipts/hosted-checks-head.tsv`, 2026-09-24T09:54:38Z).
  - Executed successfully: `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `elaborate`, `verilator-lint`, `yosys-elaboration`, `bdd-conformance`, `changes`, `full-ci-gate`, Verilator shards 0, 2 and 3, and Yosys shards 0-3.
  - Still in progress: Verilator shards 1/5 and 4/5.
  - Skipped by schedule: "Physical gPTP (nightly and manual)". A skip is not hardware evidence.
- No full parent, protocol-processor, gPTP, Yosys or builder bank was run, and no Docker/act, host act_ci, hardware or physical calibration was run. Physical calibration is NOT RUN.
- Probes used Git 2.55.0 and Python 3.14.7 only; other Git versions were not exercised.
- Selftest locale arms ran on this host as shipped. No locale NOT RUN notice appeared in `receipts/selftest-head.log`.
- Mutants M08 and M15 (first form) collide with guard strings that the self-test's own mutant helper searches for. That helper raises and aborts the remaining self-test (nonzero exit, fail-closed). M15 was re-run with a non-colliding edit and is killed by a genuine example. M08 is killed by the genuine `linear-merge-unsupported` case before the abort.
- The review clone was restored and verified: HEAD, tree and index tree all equal `9151db9e`, the worktree status is empty including ignored files, index entries equal the tree entries, and the gitlinks are unchanged (`receipts/clone-integrity.log`).

## Pending manager duties

- Publish this report. Route F1 and F2 to the executor, then re-review the corrected head.
- Accept the hosted and act results at the final head, including the two Verilator shards still in progress.
- Build and validate the current-dev candidate (source base `3d2f3e31`, live dev `9d328810`), then perform the post-merge containment.
- Obtain the second independent review on the final head (Issue #514 acceptance 4) and the maintainer's merge authorization.

R292-1 FINISHED
