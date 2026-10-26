[R697] POSITIVE - exact head 42dbe6bd42c950a7acedce56fcf29b82543123c6

# R697-1: internal cleared-context review of PR #785 (issue #784, step 1)

- Head: `42dbe6bd42c950a7acedce56fcf29b82543123c6`, tree `5fdfce709af95cf8bfe7efc1083cca5162b62d1f`, one commit on dev `d385b38e5282b395ca55d49d135e46a93f56a340`.
- Delta: `scripts/act_ci.py` +159/-7, `docs/testing/CI_WORKFLOWS.md` +10/-1. `.github/` and the four generators (`ci_gate_workflows.py`, `ci_runtime_workflows.py`, `ci_suite_workflows.py`, `yosys_shards.py`) are byte-identical to dev: `git diff d385b38e HEAD -- .github <generators>` is 0 lines.
- Role: internal reviewer. I reconstructed the task from AGENTS.md, CONTRIBUTING.md, the #784 body (Decision, Acceptance step 1), the step 1 assignment (issuecomment-6400713781), the takeover and REVIEW READY comments, and the runner contract in `docs/testing/CI_WORKFLOWS.md` (act-first replication and the bootstrap rule, lines 1762-1800 and 2028-2047). After that I read the diff and the published author evidence at `1a5e9b86/review-evidence/784-r1`.
- Prior public review findings on PR #785: none. At my start the PR had only the two review-start notices, so nothing needed resolving or retaining.
- Verdict basis: no BLOCKER, MAJOR or MINOR finding. There is one RESIDUE (prose only) and one SUGGESTION. All five lenses are covered clean at this head.

## Findings

### R697-1-01: RESIDUE (Docs)

- **Where:** `docs/testing/CI_WORKFLOWS.md:2035-2037`, "A label without a `--platform` entry is no error to `act`: it skips that job as an unsupported platform and can still exit 0".
- **Evidence:** the pinned act source (`receipts/act-source-reading.txt`, `cmd/platforms.go`) gives act a built-in table for `ubuntu-latest`, `ubuntu-22.04`, `ubuntu-20.04` and `ubuntu-18.04`, all mapped to `node:16` images. act skips a job (`pkg/runner/run_context.go:820-826`) only when the label is in neither the `-P` list nor that table. Without its `--platform` entry, `ubuntu-latest` would therefore run on `node:16-buster-slim`; it would not be skipped. The sentence is only true of a label that is not in act's table, such as `ubuntu-24.04`. The code comment at `scripts/act_ci.py:86-91` already states both outcomes correctly, and so does the self-test comment ("a label it cannot map").
- **Impact:** wording only. The conclusion is still correct: every accepted label needs an entry, and the self-test enforces that. No code, test, figure or verdict depends on the sentence.
- **Exact fix:** replace it with: "A label that has neither a `--platform` entry nor an entry in act's built-in table, such as `ubuntu-24.04`, is no error to `act`: it skips that job as an unsupported platform and can still exit 0, and a built-in label such as `ubuntu-latest` would run on act's default `node:16` image instead, so the self-test requires an entry for every accepted label."
- **Verification:** reread the sentence against `cmd/platforms.go`, then run `docs_check.py`, `check_em_dash.py --base d385b38e`, `gen_toc.py --check` and `ci_events.py --check`.

### R697-1-02: SUGGESTION (Tests)

- **Where:** `scripts/act_ci.py:6822-6828`, the arm "a ubuntu-24.04 replay holds its job containers to the same 8g memory and swap bound as ubuntu-latest".
- **Evidence:** `build_act_command` builds `--container-options` without reference to the label. This arm can therefore only fail when the `ubuntu-24.04` replay fails to start at all, and the replay arm above it already detects that. My mutant `sandbox-accepts-only-2404-drops-latest` killed it only through the `ubuntu-latest` refusal.
- **Impact:** none on correctness. The arm adds little discrimination, but it does record assignment item 2.
- **Optional change:** none required.

## Lens results (clean-lens format)

- **[R697] PASS Conformance:** `scripts/act_ci.py:92`, `:2061-2066` and `:4828`, checked against the #784 Decision/Acceptance step 1 and assignment items 1 to 5.
  - `RUNS_ON_LABELS = ("ubuntu-latest", "ubuntu-24.04")` is the only source for both the sandbox check and the `--platform` words. `grep` finds no other consumer of `runs-on` in `act_ci.py`.
  - Each label gets exactly one `--platform <label>=catthehacker/ubuntu:full-latest`.
  - `ubuntu-22.04` and `ubuntu-26.04` are refused, and the refusal names them (`receipts/runs-on-probe.log`).
  - A `ubuntu-24.04` job replays offline (`receipts/gates/act-ci-selftest.log:70`).
  - The memory model comment covers both labels (`:7651-7653`).
  - `.github/` is byte-identical to dev (`receipts/gates/github-diff.rc` = 0).
  - The STOP condition does not apply. In the pinned act source, `-P` is a repeatable string array (`cmd/root.go:82`), and `build_ci_act.py`'s patch does not touch platforms.
- **[R697] PASS RTL:** artifact `git diff --stat d385b38e..42dbe6bd` (2 files, both non-HDL). No HDL, CDC, FSM, width or interface artifact is in the delta, so the lens is inapplicable. On the architecture side, the validation order in `run_validation` (`scripts/act_ci.py:5975-5994`) still runs the sandbox before job-volume scope, CPU ranges, submodules, Docker boundary or act. The mutant `run-validation-skips-sandbox` proves the new replay arm depends on that order.
- **[R697] PASS Robustness:** checked `receipts/runs-on-probe.log` (20 probes through the head's real `validate_workflow_sandbox`, loaded by path, not copied) and `scripts/act_ci.py:2007` (`UniqueKeyLoader(yaml.BaseLoader)`, so every scalar is a string).
  - Accepted: the literals and their quoted forms.
  - Refused, each named in the refusal: empty, `""`, `null`, `24.04`, a matrix expression, one- and two-label lists, a `{group, labels}` mapping, a trailing space, upper case, `windows-latest`, `macos-latest`, `self-hosted`, `ubuntu-20.04/22.04/26.04`.
  - A missing key is refused by the existing arm "a missing runner label is refused".
  - `repr` escapes control characters in the refusal text.
  - The refusal comes before any boundary (`act-ci-selftest.log:72`, `entered == 0`).
- **[R697] PASS Tests:** checked `receipts/gates/act-ci-selftest.log` (622 ok, 0 FAIL; the 12 new arms at lines 63-72 and 126-127), `receipts/gates/act-ci-contract-gate.log` (620 ok; the two flat-launcher arms are skipped inside the isolated child by design) and `receipts/mutants/summary.json`.
  - The arms call the real `validate_workflow_sandbox`, `build_act_command` and `run_validation`, with only Git, GitHub, Docker and act faked (`:6763-6807`).
  - Control copy: rc 0, 0 FAIL. All 9 mutants were KILLED with named new failures:
    - the two the brief names: `drop-2404-from-platform-map` and `map-2404-to-act-default-image`, 3 failures each;
    - my own seven: `sandbox-accepts-any-ubuntu-prefix` (5), `sandbox-accepts-one-label-list` (1), `sandbox-case-insensitive` (1), `third-label-2204-added` (2), `platform-map-duplicated` (1), `run-validation-skips-sandbox` (1) and `sandbox-accepts-only-2404-drops-latest` (5).
  - The same suites pass on CPython 3.12.3 + PyYAML 6.0.2, the hosted pair (`receipts/gates-py312/`).
- **[R697] PASS Docs:** checked `docs/testing/CI_WORKFLOWS.md:2028-2039` against `scripts/act_ci.py:86-92` and the pinned act source.
  - The page states both labels, refusal by name, the one-image mapping, and the reason (hosted `ubuntu-latest` moved to 26.04, pip resolution fails, step 2 pins `ubuntu-24.04`). The reason is confirmed by `receipts/hosted-sample-failure.txt`: `Image: ubuntu-26.04` and `ResolutionImpossible` on PyYAML==6.0.2 at this head.
  - The only defect is the prose in R697-1-01 (RESIDUE).
  - Gates under the pinned renderer, all rc 0: `docs_check`, `check_em_dash --base d385b38e` (10 added lines, 0 findings), `gen_toc --check` and `--verify-anchors`, `check_doc_paths`, `check_doc_style`, `check_feature_status`, `check_baremetal_only --check`, `DOC_MAP.gen.py --check`.
  - The added comments carry only `#784`, with no lane, round, reviewer or comment IDs (scan of `receipts/full.diff`).
  - No CHANGELOG entry is expected: CONTRIBUTING has no such rule, and the prior runner PRs (#745, #739, #731, #735) added none.

## Brief checks (1) to (5)

1. **Single source, exact acceptance, mapping:** confirmed. See Conformance and Robustness above. Refusal by name happens before Docker or act: `run_validation` order, the arm at log line 72, and the `run-validation-skips-sandbox` mutant. Both labels map to the same `RUNNER_IMAGE`, one `--platform` each (log line 126).
2. **Other places that assume the label:** in `act_ci.py`, the only `runs-on` reader is the sandbox, and the memory comment is updated.
   - `ci_events.py:177`, the generators and `ci_workflow_plan_selftest.py` still name `ubuntu-latest`. That is step 2 scope and out of scope for this PR by the assignment. None of them accepts a second label.
   - Within the runner, nothing else accepts any label: `workflow_job_volume_scope`, `replay_container_concurrency` and the boundary probe do not read `runs-on`.
3. **Arms drive the real code:** confirmed, and I reran the self-test myself. See Tests above.
4. **Bootstrap:**
   - The workflows are unchanged, so the trusted dev runner sees the same `ubuntu-latest` jobs as before. Inside the docs job, the candidate copy runs only its offline `--selftest`; the flat-install contract gate passes at this head.
   - Nothing in the delta changes materialization, trust checks or the trusted invocation. The only changes in the `run_validation` call graph are the refusal text and the `--platform` words.
   - Once merged, dev's trusted copy accepts and maps `ubuntu-24.04`. A step 2 head whose jobs all say `ubuntu-24.04` therefore passes the sandbox and runs on `RUNNER_IMAGE`, as `selftest_runner_label_replay` exercises offline, even if step 2 also drops `ubuntu-latest` from its own candidate copy.
5. **Gates:** `ci_events.py --check` (2199 items) and `--selftest` (5236 arms), the runner contract gate, `generate_ci_evidence_pins.py --check`, `ci_runtime_evidence_selftest.py`, `ci_gate_workflows.py --check`, `check_py_idiom`, `check_hygiene`, `check_todo_ownership` and the docs gates above all exit 0 (`receipts/gates/*.rc`). The two system-Python runs of `check_em_dash` and `gen_toc` that returned rc 2 only lacked the renderer; their reruns under the hash-pinned renderer (`receipts/gates/renderer-env.txt`) replaced those logs.

## Reviewer-owned ledger

| lens | state | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `act_ci.py:86-92, 2061-2066, 4828, 7651-7653`; #784 step 1 and the assignment; act `cmd/root.go:82`, `cmd/platforms.go` | R697-1 | 42dbe6bd42c950a7acedce56fcf29b82543123c6 |
| RTL | CLEAN | delta file list (no HDL); `act_ci.py:5975-5994` validation order | R697-1 | 42dbe6bd42c950a7acedce56fcf29b82543123c6 |
| Robustness | CLEAN | `receipts/runs-on-probe.log` (20 probes); `act_ci.py:2007` BaseLoader | R697-1 | 42dbe6bd42c950a7acedce56fcf29b82543123c6 |
| Tests | CLEAN | `act_ci.py:6697-6835, 15257, 15464-15465`; self-test and contract-gate logs (3.14 and 3.12.3); `receipts/mutants/` (control plus 9 killed) | R697-1 | 42dbe6bd42c950a7acedce56fcf29b82543123c6 |
| Docs | CLEAN (R697-1-01 RESIDUE carried) | `CI_WORKFLOWS.md:2028-2039`; docs gates under the pinned renderer; `receipts/full.diff` comment scan | R697-1 | 42dbe6bd42c950a7acedce56fcf29b82543123c6 |

## Real limits

- Offline only. Per the brief, no Docker, act, host `act_ci` replay, privilege, or real PR run. I read the act source; I did not execute act. The live act behaviour is the author's no-daemon probe receipt (`author/receipts/act-platform-probe.md`, whose hash matches the published manifest), and it agrees with my source reading.
- No manager source bank ran at this head, and I claim none. Hosted runs at this head: 12 success, 16 failure, 8 cancelled, 10 skipped (`receipts/hosted-check-runs.tsv`). The sampled failure is the #784 ubuntu-26.04 pip failure, not this change. Skipped and cancelled contexts are not evidence.
- The `ImageOS` claim (act sets `ubuntu20` for `ubuntu-latest` and `ubuntu24` for `ubuntu-24.04`) is confirmed in the act source (`run_context.go:1066-1073`). No `.github/`, `scripts/` or `ci/` file reads `ImageOS`; cache keys use `runner.os`. The audited `actions/setup-python@v5` bundle was not available to me, so the author's statement that it does not read `ImageOS` is unverified here. It matters only for step 2's replay, not for this head.
- Physical calibration was NOT RUN. Nothing here is hardware evidence.

## Pending manager duties

- The act replay and the signed local CI of the current-dev merge candidate (source base d385b38e, live dev e76a755a), with the builder and native banks, at the merge turn.
- Hosted/act acceptance, under the temporary ruleset in issuecomment-6400810252.
- Carry R697-1-01 to the residue checklist.
- Collect the external review verdict.
- Keep #784 open for step 2 (the PR says "Relates to #784").

## Clone restoration

`receipts/restore-check.txt` records the restored clone state:

- HEAD and index tree equal the exact head and tree.
- 0 untracked or ignored entries, after removing the session-created `scripts/__pycache__` (36 files, all newer than this review's start).
- `scripts/act_ci.py` blob `904d4fda`, mode 100755, matches HEAD.
- All six gitlinks match HEAD.

R697-1 FINISHED
