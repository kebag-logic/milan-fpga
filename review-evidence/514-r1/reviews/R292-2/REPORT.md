[R292] POSITIVE - exact head b0347a4fd668f8d40bdf40a142ac0ea70167acd1

# R292-2 independent re-review: PR #552 for Issue #514

- Role: cleared-context internal independent reviewer, round R292-2.
- Exact head: `b0347a4fd668f8d40bdf40a142ac0ea70167acd1`, tree `6a162c641e5052b523bc8d88cbb13bf3eff1ad47`.
- Source base: `3d2f3e3131c9db5898e1db9dd3e2a35149843109`. History is three one-line commits with no bodies or trailers: `3f2fe73d1`, `20b7bdaa3` and `b0347a4fd`.
- Round-2 delta: `20b7bdaa..b0347a4f` changes one file, `scripts/merge_containment_selftest_linear.py`, with +83 lines and no deletions.
  - The production blobs are byte-identical to round 1: `check_merge_containment.py` `141baec9`, `merge_containment_replay.py` `5652be97` and `merge_containment_git.py` `b8f9fb83` (`receipts/clone-integrity.log`).
- Authorities read, in order:
  - AGENTS.md, CONTRIBUTING.md 2.1 step 7 and docs/README.md.
  - The Issue #514 body and acceptance items 1-5.
  - The manager's decision [5789750055](https://github.com/kebag-logic/milan-fpga/issues/514#issuecomment-5789750055), assignment 5810682208 and round-2 assignment 5812011094. The executor's notices 5810713843, 5810954305 and 5812212392.
  - The PR #552 body, review start 5812239927, REQ-VER-04, the base-to-head diff and history.
  - Public evidence tree `7a00fd14` `review-evidence/514-r1` (listing and author mutant summary). Exact-head hosted check runs.

## Verdict basis

Round 2 claims three things: the change is tests only, it makes no verdict or behaviour change, and it closes R292-1 F1 and F2. Each claim was verified at the exact head.

- **Tests only, no behaviour change.**
  - The production blobs are unchanged.
  - The 12 behaviour probes and the fixture 30, fixture 31 and `linear-patch-fallback` reproductions are byte-identical to round 1 (`receipts/probe-behaviour-head.log`, `receipts/repro-fixtures-head.log`).
- **Self-test.** It passes with exit 0: 799 `ok`, 0 FAIL, with no cleanup status 3 (`receipts/selftest_head.log`).
  - All 778 round-1 case lines are present verbatim and in order (`receipts/preservation.txt`, `scripts/preservation.py`), against a fresh run of `20b7bdaa` (`receipts/selftest_20b7bdaa.log`).
  - The 21 added lines are all `linear-*`.
- **Round-1 mutant set, re-run unchanged.** `scripts/mutants.py` is byte-identical to the R292-1 archive, sha256 `2909a2ff...0c2c5`. Results are in `receipts/mutants-head.log`.
  - M01, M09, M10 and M12 are now KILLED.
  - Every round-1 kill still dies: M02-M08, M14 and M15.
  - 13/15 are killed. Each target kill comes from a named, intended case. No kill comes from a helper abort: every target mutant ran 796-797 `ok` plus its FAIL lines, with no traceback (`receipts/mutants-head-fullcount.log`).
- **Reviewer equivalents M16-M24.** These were added this round in `scripts/mutants_r2.py`, and 8/9 are KILLED (`receipts/mutants-r2-head.log`). The one survivor, M16, is a SUGGESTION (S4).

No MINOR, MAJOR or BLOCKER is open at this head. All five lenses are covered clean.

## Findings

No open MINOR, MAJOR or BLOCKER findings.

### Round-1 findings (R292-1): disposition at this head

- **R292-1 F1 MINOR (Tests): RESOLVED.** Location: `scripts/merge_containment_selftest_linear.py:148-195`, wired at `:302`.
  - Empty-delta case: an exact replay of a change and its revert (`linear-empty-delta`) expects `UNKNOWN`/1. Its diagnostic is pinned to the arm-level handler text `linear retention unmeasurable: retention has no measurable changed-path set`. `linear-empty-delta-historical` keeps the default `contained`/0.
  - H-failure case: an injected `rev-list --no-merges` failure (`linear-H-measurement-failure`) expects `UNKNOWN`/1, with `linear-H-failure-reached` = 1 and a pinned `rev-list could not enumerate` diagnostic.
  - The default run of the same fixture proves that the landing does not read H (`linear-H-failure-historical`: 0 failed reads). So the injected failure reaches only the optional arm.
  - Kills: M09 (`linear-H-measurement-failure`, `linear-H-failure-diagnostic`) and M10 (`linear-empty-delta`, `linear-H-measurement-failure`).
  - Equivalents also killed: M19 (the empty changed-path guard returns `[]`), M21 (an H failure reported as "unsupported") and M23 (T skipped after H).
- **R292-1 F2 MINOR (Tests): RESOLVED.**
  - Ancestry claim: `linear-ancestry-{optional,default}-claim` at `:208-214` require exactly one `contained` line carrying both `historical inclusion by ancestry` and `current retention not implied`, with and without the option.
  - No retention line beside a failed landing: `linear-{failed-landing,no-retained-on,no-retention-on}-{STRANDED,UNKNOWN}` at `:246-260` preserve the failed word and exit 1, forbid a `retained` line and forbid any `current retention:` line.
  - Retained-line wording: `linear-*-retained-claim` at `:107-113` pins that each positive `retained` line names raw current retention and historical replay.
  - Kills: M01 and M12.
  - Equivalents also killed:
    - M17 (a retention line printed in the `contained()`-UNKNOWN branch);
    - M18 (only the "current retention not implied" disclaimer dropped);
    - M20 (an unqualified retained detail);
    - M24 (a blank retained detail);
    - M22 (the real retention arm evaluated on STRANDED).
- **R292-1 S1 SUGGESTION (Robustness): RETAINED, optional, not taken.** Location: `scripts/check_merge_containment.py:948-949`.
  - `--base --current-retention main pr` still parses as `--base main pr`, exit 0 (`receipts/probe-behaviour-head.log`, `base-flag-then-option`).
- **R292-1 S2 SUGGESTION (Docs): RETAINED, optional, not taken.** Location: `CONTRIBUTING.md:219`.
  - The `--current-retention --merged-prs` sweep is `UNKNOWN`/1 by design for ancestry-landed PRs, and one sentence saying so would help a cold reader.
- **R292-1 S3 SUGGESTION (Docs): RETAINED, optional, not taken.** Location: `docs/testing/RUNNING_TESTS.md:76`.
  - The sentence's subject is ambiguous.

### New this round

- **S4 SUGGESTION (Tests): retention inserted after a pre-resolution UNKNOWN is unpinned.** Location: `scripts/check_merge_containment.py:884-887`.
  - Authority and evidence: M16 inserts a `retained` print into the `pre_error` branch. It SURVIVES with exit 0 and 0 FAIL (`receipts/mutants-r2-head.log`).
    - `pre_error` arises only for `--merged-prs` targets: a foreign-repository head, a ref-event error, or a discontinuous tip (`:848-853`).
    - The self-test's UNKNOWN case (`no-such-branch`) reaches the other UNKNOWN branch, through `contained()`. Mutant M17 on that branch is killed.
  - Why only a SUGGESTION:
    - The shipped branch ends in `continue` before any retention code, so a regression needs an inserted print, not an edit to existing logic.
    - The F2 required outcome ("STRANDED (or UNKNOWN)") is met by the STRANDED and `contained()`-UNKNOWN cases.
  - Impact: a future edit could print a retention line beside a pre-resolution UNKNOWN in a `--merged-prs` sweep. The exit would still be 1.
  - Optional outcome: add one `--merged-prs --current-retention` case with a patched `pre_error` target that expects UNKNOWN/1 and no `current retention:` line.
  - Verification: `python3 -B scripts/mutants_r2.py run <clone> <scratch> M16-retention-on-pre-error-unknown` is KILLED.
- **Retained non-contract survivors** (round-1 dispositions, unchanged):
  - M11, the merge-count digit guard, is unreachable without a Git shim.
  - M13 is summary-sentence wording, not a contract.

### Other round-1 review (R293-1): disposition at this head

I read this only after the verdict, findings and ledger above were written. Its findings are the manager-mapped equivalents of mine (assignment 5812011094). Each one was checked against this head with my own mutants, not the other reviewer's scripts.

- **R293-1 F1 MINOR (Tests): RESOLVED.**
  - Its `measurement-except-certifies` mutant corresponds to my M10, and its `H-error-ignored` to my M09. Both are KILLED at this head.
  - Its empty-net-delta fixture (A then revert(A), each replayed exactly) has the same shape as the new `linear-empty-delta` case, which expects `UNKNOWN`/1.
- **R293-1 F2 MINOR (Tests): RESOLVED.**
  - Its `ancestry-diagnostic-dropped` mutant corresponds to my M01, and its `retained-diagnostic-blank` to M24 (M20 is the unqualified variant). All are KILLED.
  - It also retained the R292-1 STRANDED item, which is my M12, now KILLED, together with M22 and M17.
- **R293-1 S1 SUGGESTION (Docs), S2 SUGGESTION (Robustness) and S3 SUGGESTION (Docs): RETAINED, optional.** They are the same observations as R292-1 S2, S1 and S3 above, and remain present at this head because the Markdown and parsing are unchanged.

This reading does not change the verdict or the ledger.

## Lens results (evidence format)

- `[R292] PASS Conformance` — `receipts/repro-fixtures-head.log`, `receipts/probe-behaviour-head.log`, `receipts/preservation.txt` and `receipts/selftest_head.log` at `b0347a4f`, against Issue #514 acceptance 1-5 and decision 5789750055.
  - **Acceptance 1:** fixture 30 is rebuilt from the immutable R242 builder (sha256 `ec2c6489...d17ff`) at source `9a9c1e7b26ff2d3439ef5c5ec439cc3a13c9a34a` and target `219aa2256e055e8a577f9899ac6d36bd8bd986e0`. It returns `contained`/0 by default and `UNKNOWN`/1 naming `'mod.txt'` with the option. `linear-patch-fallback` returns `contained`/0, and `UNKNOWN`/1 naming `'linear'`.
  - **Acceptance 2:** the decision precedes the implementation, and all 778 prior expectations are preserved verbatim.
  - **Acceptance 3:** the unmeasurable result is now executable: empty delta, H failure and object-read failure. So are unsupported histories (ancestry, merge, squash). Each gives `UNKNOWN`/1 and none is certified. Every reversion, extension, supersession, mode, kind and binary row still holds.
  - **Acceptance 4:** the local self-test passes. The hosted, candidate and post-merge parts, and the second review, remain manager duties.
  - **Acceptance 5:** see Docs.
  - The round-2 assignment ("no verdict or behaviour change") is verified by unchanged production blobs and byte-identical probe outputs.
- `[R292] PASS RTL` — `receipts/clone-integrity.log` and the raw diffs `3d2f3e31..b0347a4f` and `20b7bdaa..b0347a4f`.
  - No HDL, constraint, testbench, build or gitlink artifact changes.
  - The four gitlinks are identical to the base: external `efeb541a`, gptp-processor `e5dcea6e`, protocol-processor `424c688f` and verilog-axis `48ff7a7e`.
  - The tooling interface contracts under this lens are unchanged from round 1, since the production blobs are identical: exit codes 0/1/2 plus cleanup status 3, the unchanged `--selftest` entry and the `replay_verdict` signature.
  - The scoped Verilator was not needed and not invoked, so its identity was not checked.
- `[R292] PASS Robustness` — `scripts/merge_containment_replay.py:157-183` and `scripts/check_merge_containment.py:879-914,945-949` at `b0347a4f`, exercised by 12 behaviour probes (PROBES PASS, identical to round 1) and by the new self-test failure paths.
  - Now executable: net-zero delta, H read failure, object-read failure, STRANDED and `contained()`-UNKNOWN landings with the option, unsupported histories, duplicate or conflicting options, and multi-target failure propagation.
  - The self-test's cleanup status is clean (exit 0, not 3), so the new fixtures leave no scratch tree.
  - The new injection is scoped by a context manager and restored (`:183`).
  - S1 is retained as an optional parsing inconsistency.
- `[R292] PASS Tests` — `scripts/merge_containment_selftest_linear.py:95-126,148-195,198-243,246-260,281-305` at `b0347a4f`.
  - Evidence: `receipts/selftest_head.log` (799/799), `receipts/preservation.txt` (778/778 in order), `receipts/mutants-head.log` (round-1 set, 13/15), `receipts/mutants-head-fullcount.log` and `receipts/mutants-r2-head.log` (8/9).
  - Each new case fails against the defect it claims to detect. Every target and equivalent mutant is killed by the named new case, not by a helper abort.
  - The failed-read counter guards the H-failure fixture against vacuity: 0 reads on the default path, 1 read on the optional path.
  - No existing expectation was weakened.
  - The survivors are S4 (optional) and M11/M13 (non-contract, retained dispositions).
- `[R292] PASS Docs` — `CONTRIBUTING.md:207-245`, `docs/testing/CI_WORKFLOWS.md:1754-1760`, `docs/testing/RUNNING_TESTS.md:76-80`, `AGENTS.md:416`, the module docstrings, and the new case descriptions and docstrings in `merge_containment_selftest_linear.py` at `b0347a4f`.
  - The Markdown is unchanged since round 1, and each claim still matches observed behaviour.
  - The CONTRIBUTING claims "Empty net deltas also remain unmeasurable by this arm" and "The default self-test exercises these examples and killing mutations" are now backed by executable cases.
  - The PR body's round-2 section matches the delta.
  - Nine doc and idiom gates exit 0 (`receipts/doc-gates-head.log`): docs_check in both discovery modes, em-dash against `3d2f3e31`, doc style, the TOC check and anchors, doc paths, Python idiom, and `git diff --check`.
  - S2 and S3 are retained as optional.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #514 decision and acceptance 1-5; fixture 30/31 and linear-patch-fallback reproductions; 778/778 preserved lines; unchanged production blobs | R292-2 | b0347a4fd668f8d40bdf40a142ac0ea70167acd1 |
| RTL | CLEAN | Raw diffs base..head and round1..head (no HDL or gitlink change); four gitlinks equal base; exit-code and entry-point contracts | R292-2 | b0347a4fd668f8d40bdf40a142ac0ea70167acd1 |
| Robustness | CLEAN | `merge_containment_replay.py:157-183`, `check_merge_containment.py:879-949`; 12 probes; new failure-path self-test cases | R292-2 | b0347a4fd668f8d40bdf40a142ac0ea70167acd1 |
| Tests | CLEAN | `merge_containment_selftest_linear.py` (full file); self-test 799/799; round-1 mutant set 13/15; equivalents 8/9; full-count reruns | R292-2 | b0347a4fd668f8d40bdf40a142ac0ea70167acd1 |
| Docs | CLEAN | CONTRIBUTING 2.1 step 7, CI_WORKFLOWS, RUNNING_TESTS, AGENTS, docstrings and case descriptions; 9 doc/idiom gates | R292-2 | b0347a4fd668f8d40bdf40a142ac0ea70167acd1 |

Open at this head: SUGGESTION only (S1-S4), and none affects coverage.

## Real limits

- **Hosted checks were inspected, not accepted** (`receipts/hosted-checks-head.tsv`, fetched 2026-09-24T10:25:39Z).
  - Completed successfully: `verilator-lint`, `bdd-conformance`, `wire-accountability`, `changes`, `full-ci-gate`, `docs-check-no-git`, Verilator shards 2/5 and 3/5, and Yosys shards 0-3.
  - Still in progress: `docs-check`, `elaborate`, `yosys-elaboration`, and Verilator shards 0/5, 1/5 and 4/5.
  - Skipped by schedule: "Physical gPTP (nightly and manual)". A skip is not hardware evidence.
- **The manager's bank receipt was not located.** The public tree `7a00fd14` `review-evidence/514-r1` holds the executor's and the round-1 reviewers' material. I did not locate the manager's source static/builder/native bank receipt for `b0347a4f` there, so I did not verify that claim.
- **Not run:** a full parent, protocol-processor, gPTP, Yosys or builder bank, Docker/act, host act_ci, hardware, or the scoped Verilator. Physical calibration is NOT RUN.
- Git 2.55.0 and Python 3.14.7 only. The self-test's locale arms ran as shipped, with no NOT RUN notice.
- **Scratch clones.** Mutants ran in disposable shared clones under the packet `scratch/` directory, which is not published. The prior-head self-test ran in a scratch clone of `20b7bdaa`.
- **Review clone restored.** I removed the `scripts/__pycache__` bytecode that my own runs created (all timestamped this session). Then I re-verified the clone:
  - HEAD, tree and index tree are `6a162c64`.
  - The status is empty, including ignored files.
  - The 879 index entries (mode, blob, path) equal the HEAD tree.
  - The worktree equals the index.
  - The gitlinks are unchanged (`receipts/clone-integrity.log`).

## Pending manager duties

- Publish this report and the manifest-listed receipts.
- Accept the hosted and act results at the final head, including the checks still in progress.
- Build and validate the current-dev candidate (source base `3d2f3e31`, live dev `9d328810`), then run post-merge containment.
- Obtain the second independent review at the final head (Issue #514 acceptance 4) and the maintainer's explicit merge authorization.
- Optionally route S1-S4. None blocks this verdict.

R292-2 FINISHED
