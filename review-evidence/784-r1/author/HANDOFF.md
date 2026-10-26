# HANDOFF -- [A673], issue #784 step 1 (act runner accepts `ubuntu-24.04`)

Status: REVIEW READY. Not pushed (the manager pushes and opens the PR).

- Repository: kebag-logic/milan-fpga; `git remote get-url origin` = `https://github.com/kebag-logic/milan-fpga.git` (verified).
- Branch: `784-act-runner-ubuntu-2404`, branched from dev `d385b38e5282b395ca55d49d135e46a93f56a340` (verified: merge base with `origin/dev` is that commit).
- Head: `42dbe6bd42c950a7acedce56fcf29b82543123c6`, one commit, one-line subject, no body, no trailers:
  `Accept runs-on ubuntu-24.04 beside ubuntu-latest in the act runner and map both to the runner image (#784)`
- Diff: `scripts/act_ci.py` +159/-7, `docs/testing/CI_WORKFLOWS.md` +10/-1. `git diff --exit-code d385b38e -- .github` is empty: workflows, templates and the PR template are byte-identical to dev. No generator touched.
- Assignment: #784 comment 6400713781 ([A10], step 1). TAKEN posted as #784 comment 6400760785; REVIEW READY posted as #784 comment 6401144488 (copies in `receipts/taken-comment.md`, `receipts/review-ready-comment.md`).
- PR body: `PR-BODY.md` ("Relates to #784": step 2 acceptance is not met by this PR).
- Receipts: `receipts/` with `receipts/INDEX.md` generated from the files present.

## Changes (file:line at head, and reason)

| file:line | change | reason |
|---|---|---|
| `scripts/act_ci.py:86-92` | New `RUNS_ON_LABELS = ("ubuntu-latest", "ubuntu-24.04")` with its reason comment. | One source for the accepted labels, read by the sandbox check and the platform list, so the two cannot drift. Comment states #784's reason (hosted `ubuntu-latest` moved to 26.04 where the pinned Python tools cannot install) and why other labels are refused (act would use its own default image, or skip the job and exit 0). |
| `scripts/act_ci.py:2061-2066` (`validate_workflow_sandbox`) | `runs-on` must be in `RUNS_ON_LABELS`; the refusal now reads `workflow <file> job <id> runs on '<label>'; only the literal labels ubuntu-latest, ubuntu-24.04 are replayed`. | Assignment item 1: accept `ubuntu-24.04` exactly as `ubuntu-latest`; refuse every other label by name. Same exactness as before: a list, a mapping, an expression, a missing key or any other spelling is refused. |
| `scripts/act_ci.py:4828` (`build_act_command`) | `--platform <label>=RUNNER_IMAGE` once per `RUNS_ON_LABELS` entry, replacing the single `ubuntu-latest=` entry. | Assignment item 1: both labels map to the same runner image, the `-P` list carries both. |
| `scripts/act_ci.py:7651-7653` (`selftest_container_memory_bound` comment) | "Hosted runners on either RUNS_ON_LABELS label have 16 GB". | Assignment item 2: the hosted memory model is stated for both labels. The per-container bound (`CONTAINER_MEMORY`) was already label-independent; the new arm at `:6822-6828` proves it on a `ubuntu-24.04` replay. |
| `scripts/act_ci.py:6697-6712` | `write_runs_on_workflow`, `runs_on_refusal` helpers. | Write a one-job docs workflow on a given `runs-on` and return the real sandbox's refusal text. |
| `scripts/act_ci.py:6714-6716` | `act_platforms` helper. | The `label=image` words after each `--platform`. |
| `scripts/act_ci.py:6719-6739` | `selftest_runner_labels` (7 arms). | Item 3: accepted / refused-by-name / exact-literal arms. |
| `scripts/act_ci.py:6742-6760` | `selftest_runner_platforms` (2 arms), called at `:15257` beside `selftest_act_command`. | Item 3: the named check the platform-map mutant fails, plus accepted set == mapped set. |
| `scripts/act_ci.py:6763-6807` | `dry_run_replay` helper. | Drives `run_validation` in dry-run with the REAL `validate_workflow_sandbox` and act command builder (Git, GitHub, Docker, act faked as `selftest_validation_transcript` fakes them). |
| `scripts/act_ci.py:6810-6835` | `selftest_runner_label_replay` (3 arms), called at `:15465`. | Item 3: a `ubuntu-24.04` job is accepted and replays; a `ubuntu-26.04` job is refused naming the label before any Docker boundary; item 2's same-memory-bound arm. |
| `scripts/act_ci.py:15464` | `selftest_runner_labels(tally)` call. | Wiring. |
| `docs/testing/CI_WORKFLOWS.md:2028-2038` | Runner contract paragraph: two literal labels, both mapped to the same image with one `--platform` each, every other label (e.g. `ubuntu-22.04`, `ubuntu-26.04`) refused by name; why (hosted `ubuntu-latest` moved to 26.04; step 2 of #784 pins `ubuntu-24.04`; until then the workflows still name `ubuntu-latest`); why every accepted label needs a platform entry. | Assignment item 5. |

Arm count: `act_ci.py --selftest` prints 610 arm lines at dev (`receipts/base-act-ci-selftest.log`) and 622 at head (12 new).

## New checks (planted mutant and failing words)

Each mutant is a single exact replacement in a scratch copy of `scripts/act_ci.py`, run as `python3 -I <copy> --selftest --worktree <checkout>` on CPython 3.12.3 + PyYAML 6.0.2 at head `42dbe6bd`. Driver: `receipts/scripts/mutants.py`; receipts: `receipts/mutants/*.json` (replacement text, rc, every FAIL line). All five rc 1.

| Mutant | Failing checks (exact words) |
|---|---|
| `drop-2404-from-platform-map` (the assignment's mutant: dev's single `--platform ubuntu-latest=` entry) | `act's platform list maps ubuntu-latest and ubuntu-24.04 to the runner image, once each`; `every runs-on label the sandbox accepts has a platform entry, and nothing else does`; `a job on ubuntu-24.04 passes the sandbox and dry-run replays to an act command that maps ubuntu-24.04 to the runner image` (3 failures) |
| `map-2404-to-act-default-image` (`ubuntu-24.04=node:16-bullseye-slim`) | the same three (3 failures) |
| `drop-2404-from-accepted-labels` (`RUNS_ON_LABELS = ("ubuntu-latest",)`) | `a job on ubuntu-24.04 is accepted by the sandbox`; `a job on ubuntu-24.04 passes the sandbox and dry-run replays to an act command that maps ubuntu-24.04 to the runner image`; `a ubuntu-24.04 replay holds its job containers to the same 8g memory and swap bound as ubuntu-latest`; `act's platform list maps ubuntu-latest and ubuntu-24.04 to the runner image, once each` (4 failures) |
| `accept-any-ubuntu-label` (`runs_on.startswith("ubuntu-")`) | `a job on ubuntu-26.04 is refused before act, and the refusal names ubuntu-26.04`; `a job on ubuntu-22.04 is refused before act, and the refusal names ubuntu-22.04`; `the arm image of an accepted label is refused: only the exact literal is replayed`; `a job on ubuntu-26.04 is refused naming ubuntu-26.04, before any Docker boundary or act command`; `every runs-on label the sandbox accepts has a platform entry, and nothing else does` (5 failures) |
| `refusal-omits-label` (dev's `must use literal ubuntu-latest` text) | `a job on ubuntu-26.04 is refused before act, and the refusal names ubuntu-26.04`; `a job on ubuntu-22.04 is refused before act, and the refusal names ubuntu-22.04`; `a job on ubuntu-26.04 is refused naming ubuntu-26.04, before any Docker boundary or act command` (3 failures) |

The 12 new arms (all `ok` at head): accepted on `ubuntu-latest`; accepted on `ubuntu-24.04`; `ubuntu-26.04` refused naming it; `ubuntu-22.04` refused naming it; `Ubuntu-24.04`, `ubuntu-24.04-arm` and `[ubuntu-24.04]` refused (exact literal only); `ubuntu-24.04` dry-run replay maps the label; same 8g bound on both labels; `ubuntu-26.04` replay refused before any boundary; platform list exact; accepted set == mapped set.

## Gate table (head `42dbe6bd`, every command run directly, never piped)

Interpreters: "renderer venv" = the pinned Markdown renderer venv (CPython 3.14.8, PyYAML 6.0.3, cmarkgfm 2025.10.22, html5lib 1.1); "hosted pair" = scratch CPython 3.12.3 + PyYAML 6.0.2 from `ci/constraints-ci.txt` (the hosted interpreter). Logs: `receipts/gates/` and `receipts/gates-py312/`; per-batch tables `table-*.md` there.

| Gate (workflow step) | Command(s) | Interpreter | rc |
|---|---|---|---|
| Local act runner contract gate (docs-gates-2, gate_42) | `python3 scripts/act_ci.py --selftest` then install `-m 0555` copy and `python3 -I <copy> --selftest --worktree <checkout>` | renderer venv, 100.4 s | 0 |
| Local act runner contract gate | same | hosted pair, 98.5 s | 0 |
| CI event and SHA contract gate (gate_41) | `python3 scripts/ci_events.py --check`; `python3 scripts/ci_events.py --selftest` (2199 items, 5236 arms) | renderer venv; hosted pair | 0, 0; 0, 0 |
| Workflows byte-identical to dev | `git diff --exit-code d385b38e5282b395ca55d49d135e46a93f56a340 -- .github` | git | 0 |
| Strip git metadata, then run the docs gate (docs-check-no-git) | `rm -rf .git; python3 scripts/docs_check.py; python3 scripts/check_feature_status.py` on a `git archive HEAD` export with empty gitlink dirs | renderer venv | 0 |
| Link health, wording, dead-reference and local-info (gate_7) | `python3 scripts/docs_check.py` | renderer venv | 0 |
| Added-line em-dash (gate_8) | `python3 scripts/check_em_dash.py --base d385b38e5282b395ca55d49d135e46a93f56a340`; `--selftest` | renderer venv | 0, 0 |
| Concise audience documentation (gate_9, style part) | `python3 scripts/check_doc_style.py`; `--selftest` | renderer venv | 0, 0 |
| Milan feature-status consistency (gate_15) | `python3 scripts/check_feature_status.py`; `--self-test` | renderer venv | 0, 0 |
| Doc cited-path | `python3 scripts/check_doc_paths.py` | renderer venv | 0 |
| Per-page contents | `python3 scripts/gen_toc.py --selftest`; `--verify-anchors`; `--check` | renderer venv | 0, 0, 0 |
| Audience diagram no-drift (DOC_MAP part; it names `CI_WORKFLOWS.md`) | `python3 docs/DOC_MAP.gen.py --check`; `--selftest` | renderer venv | 0, 0 |
| Bare-metal scope (masks `act_ci.py` and `CI_WORKFLOWS.md`) | `python3 scripts/check_baremetal_only.py --check`; `--selftest` | renderer venv | 0, 0 |
| Python idiom | `python3 scripts/check_py_idiom.py`; `--selftest` (every budget line unchanged, e.g. long function 9 <= 9) | renderer venv | 0, 0 |
| Mechanical hygiene ratchet | `python3 scripts/check_hygiene.py --check`; `--selftest` | renderer venv | 0, 0 |
| Fail-fast ratchet | `python3 scripts/measure_fail_fast.py --check`; `--selftest` | renderer venv | 0, 0 |
| Test-evidence ratchet | `python3 scripts/measure_test_evidence.py --check`; `--selftest` | renderer venv | 0, 0 |
| TODO ownership | `python3 scripts/check_todo_ownership.py`; `--selftest` | renderer venv | 0, 0 |
| Code-quality measurement self-tests | `python3 scripts/measure_control_flow.py --selftest`; `python3 scripts/measure_cohesion.py --selftest` | renderer venv | 0, 0 |
| CI scheduling and evidence controls (gate_50, all 14 commands; `ci_runtime_evidence_selftest.py` parses `act_ci.py`, `generate_ci_evidence_pins.py --check` reads its pins) | `ci_gate_workflows.py --check`, `ci_gate_workflows_selftest.py`, `ci_case_receipts_selftest.py`, `ci_make_cases_selftest.py`, `ci_maap_cases_selftest.py`, `ci_capture_cases_selftest.py`, `ci_suite_pieces_selftest.py`, `ci_suite_collect_selftest.py`, `ci_fail_fast_selftest.py`, `ci_runtime_evidence_selftest.py`, `ci_install_cache_selftest.py`, `generate_ci_evidence_pins.py --check`, `ci_workflow_plan_selftest.py`, `ci_manifest_selftest.py` | renderer venv | all 0 |

Not run, with reason:
- Verilator sweep, campaigns, Vivado: no RTL in the change (assignment: not required). No Vivado lock taken.
- rtl-fast bdd-conformance (`cd tests && behave`): nothing under `tests/` reads `act_ci.py`, `CI_WORKFLOWS.md` or any runs-on label (grep), so the change does not reach it.
- The act-first replica of this PR: per the bootstrap rule the trusted runner on dev replays it; the candidate runner was never run with `--sudo`, against a real PR, or through a host act slot, and no Docker daemon was contacted.
- Docs gates that read no changed file (diagram PNG/wavedrom, solution, submodule and gPTP docs, traceability matrix): the change does not reach them.

## STOP conditions

None hit.

- "act or the runner image cannot serve a second label without a change outside `scripts/act_ci.py`": not the case. Pinned act source (`cmd/root.go:82` `--platform` is a StringArray; `cmd/platforms.go` `newPlatforms` maps each `label=image` entry) and a no-daemon dry run of the pinned binary (sha256 `4d30fb23...bbd3f5`, equal to its build receipt) both show a second `-P ubuntu-24.04=catthehacker/ubuntu:full-latest` entry starts the `ubuntu-24.04` job on the runner image. `receipts/act-platform-probe.md`.
- Same probe shows the failure mode the new cross-check guards: with dev's single entry a lone `ubuntu-24.04` job is printed as `Skipping unsupported platform -- Try running with -P ubuntu-24.04=...` and act exits 0.

## Notes / open risks

1. **Hosted checks on this PR can be red for #784's own reason.** The workflows still say `ubuntu-latest`, which now lands on `ubuntu-26.04` where pip resolution fails (`receipts/hosted-image-evidence.md`: run 40187576861 job 121179871493 `Image: ubuntu-26.04` + `ResolutionImpossible`; dev push run 40187422760 job 121155262818 `Image: ubuntu-24.04`). Step 1 cannot fix that by its own scope (no workflow change). The manager decides how this PR's `rtl-fast` verdict is obtained.
2. act sets `ImageOS` per label (`ubuntu20` for `ubuntu-latest`, `ubuntu24` for `ubuntu-24.04`, `pkg/runner/run_context.go:1065-1074`). Nothing in `.github/` or `scripts/` reads `ImageOS`, and `actions/setup-python@v5` (`dist/setup/index.js` at `a26af69b`, sha256 `2ef3f65c...51ae`) has no reference, so step 2's label change reaches no step through it. Recorded for step 2.
3. act lower-cases labels for image lookup; the sandbox matches the exact literal, so `Ubuntu-24.04` is refused (an arm pins this).
4. Pre-existing, unrelated: `measure_test_evidence.py --check` prints "the mutation ratchet can be lowered to 67" (Verilator suites without a mutation arm); not this change's scope.
5. `third_party/tsn-c-stack` is uninitialised in this lane; no command needed it, and no git command was run inside it. protocol-processor and gptp-processor were verified (toplevel is the directory itself, origin is the processor repository) and sit at their pins.
6. Two `ci_events.py --selftest` logs exceeded 200 KB; the output directory keeps excerpts with each full log's sha256 and size (`*.excerpt.log`).
