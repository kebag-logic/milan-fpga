# HANDOFF: #784 step 2 (pin runs-on ubuntu-24.04), executor [A679]

Status: REVIEW READY (not pushed; the manager pushes and opens the PR)

- Lane: branch `784-pin-ubuntu-2404`, one commit on dev `a8594bb95631fa5c49d18fa0bbc9530e31ad59aa` (confirmed at start: HEAD == origin/dev == a8594bb9; origin `https://github.com/kebag-logic/milan-fpga.git`).
- Head: `847eb4dd031eb3891b61773f4a8324cb2ed6cdc0`, tree `05ae0179dbffa852651aa7ec8367758b380672d0`.
- Commit subject (one line, no body, no trailers): `Pin every workflow job to runs-on ubuntu-24.04 through the generators and refuse ubuntu-latest in the act runner (#784)`
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/784#issuecomment-6409728491
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/784#issuecomment-6409772221
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/784#issuecomment-6410631568 (text in `receipts/review-ready-comment.md`)
- Live dev at hand-off: `a8594bb95631fa5c49d18fa0bbc9530e31ad59aa` (`git ls-remote origin refs/heads/dev`), unchanged since the branch point. Lane clean (0 untracked or ignored entries; session-created `__pycache__` removed; scratch worktrees removed).
- Delta: 20 files, +179/-164. No HDL, no submodule pointer, no Makefile, no CHANGELOG (product changelog; CI-tooling PRs #785, #745, #739, #731, #735 added none).
- Receipts: `receipts/` (index `receipts/INDEX.md`, generated from the files present).

## Changes (file:line at the head, reason)

Generators and templates (assignment item 1). The four workflows were regenerated only through `python3 scripts/ci_gate_workflows.py`; the workflow diff is exactly 46 `runs-on: ubuntu-latest` lines replaced by 46 `runs-on: ubuntu-24.04` lines and nothing else (`receipts/census.md`).

| File:line | Change | Reason |
|---|---|---|
| `.github/ci-templates/docs.yml:10,496,510` | `runs-on: ubuntu-24.04` (3 jobs) | the templates are the hand-edited source the generator reads |
| `.github/ci-templates/elaborate.yml:71` | same (1 job) | same |
| `.github/ci-templates/rtl-fast.yml:26,80,122,137,259,334,383,417,451,500,539,605` | same (12 jobs) | same |
| `.github/ci-templates/rtl.yml:37,156,320,403,461,586` | same (6 jobs) | same |
| `.github/ci-templates/rtl.yml:494` | comment "whatever ubuntu-latest carried" -> "whatever the hosted image carried" | item 2: no `ubuntu-latest` in the templates; the history it states is unchanged |
| `scripts/ci_gate_workflows.py:165` | aggregate job `"runs-on": "ubuntu-24.04"` | generator-written job (docs-check, elaborate aggregates) |
| `scripts/ci_runtime_workflows.py:127,145,159` | watcher, tail guard, collector `"runs-on": "ubuntu-24.04"` | generator-written jobs in every workflow |
| `scripts/ci_suite_workflows.py:44,76` | suite union and Yosys tool jobs `"runs-on": "ubuntu-24.04"` | generator-written jobs in rtl.yml |
| `scripts/yosys_shards.py:21` | comment "0.33-5build2 on ubuntu-latest" -> "on ubuntu-24.04" | item 2 names this generator; the weight run 32406467657 ran on `Image: ubuntu-24.04` with the noble `yosys 0.33-5build2` package (`receipts/hosted-image-evidence.md`), so the comment is now exact rather than label-relative |
| `.github/workflows/{docs,elaborate,rtl-fast,rtl}.yml` | regenerated: 9 + 6 + 15 + 16 = 46 jobs, all `ubuntu-24.04` | no hand edits; `ci_gate_workflows.py --check` rc 0 |

`scripts/ci_install_workflows.py` writes no `runs-on` (census). No other script writes a job label.

Contract and fixtures:

| File:line | Change | Reason |
|---|---|---|
| `scripts/ci_events.py:177` | `PHYSICAL_GPTP_CONTRACT` `'runs-on': 'ubuntu-24.04'` | the whole-job pin of `physical-gptp` must equal the regenerated job (mutant `physical-job-on-latest` shows it now refuses `ubuntu-latest`) |
| `scripts/ci_events.py` (16 self-test fixture jobs: 4651, 4663, 4676, 4689, 4702, 4734, 4791, 5030, 5102, 5274, 5341, 5757, 5772, 7861, 8435, 8473) | decoy/fixture jobs on `ubuntu-24.04` | fixtures model valid jobs; arm count unchanged (5236) |
| `scripts/ci_workflow_plan_selftest.py:20,30,39` | fixture jobs on `ubuntu-24.04` | same; planner self-test unchanged |

Act runner (assignment item 2):

| File:line | Change | Reason |
|---|---|---|
| `scripts/act_ci.py:86-92` | `RUNS_ON_LABELS = ("ubuntu-24.04",)`; comment states the pin, why (hosted `ubuntu-latest` moved to 26.04, where the pinned CPython 3.12 wheels do not install) and what act would do with any other label | `ubuntu-24.04` is the only accepted label; `ubuntu-latest` is refused like any other |
| `scripts/act_ci.py:2064-2065` | refusal text `only the literal label ubuntu-24.04 is replayed` (still names the refused value: `runs on 'ubuntu-latest'`) | grammar for one label; refusal by name kept |
| `scripts/act_ci.py:4828` | unchanged code; act now gets one `--platform ubuntu-24.04=catthehacker/ubuntu:full-latest` | the platform list is derived from `RUNS_ON_LABELS` |
| `scripts/act_ci.py:6719-6738` | `selftest_runner_labels`: `ubuntu-24.04` accepted; `ubuntu-latest`, `ubuntu-26.04`, `ubuntu-22.04` refused naming the label | self-tests follow the label |
| `scripts/act_ci.py:6741-6759` | `selftest_runner_platforms`: platform list is exactly `[ubuntu-24.04=<runner image>]` | same |
| `scripts/act_ci.py:6809-6832` | `selftest_runner_label_replay`: the `ubuntu-24.04` replay maps its label and holds the 8g bound; `ubuntu-latest` and `ubuntu-26.04` replays are refused naming the label before any Docker boundary or act command | the "same bound as ubuntu-latest" arm could no longer compare against a refused label; its bound check stays (R697-1-02 noted its low discrimination) |
| `scripts/act_ci.py:7648` | memory-model comment: "the RUNS_ON_LABELS label" | one label now |
| `scripts/act_ci.py:13275-13366` | `selftest_sandbox_policy`: every arm requires its own refusal reason (`runs on 'self-hosted'`, `runs on None`, `runs on '${{ matrix.os }}'`, `requests job/service containers`, `uses a reusable workflow`, `uses unapproved action '<action>'`), and its fixtures run on `ubuntu-24.04` | narrowing the label made every `ubuntu-latest` fixture refused by the runs-on check first, so the old Refusal-only arms passed with the container or action refusal deleted (receipts `mutants/old-sandbox-arms-*.json`, rc 0) |
| `scripts/act_ci.py:6605, 7707, 8685, 8711, 8714, 13035, 13375, 13389, 13419, 15542, 15551, 15564, 16659` | remaining fixture and probe workflows on `ubuntu-24.04` | the boundary probe fixture passes the real sandbox (dev's runner with only the label narrowed crashes there: `mutants/dev-narrowed-only.json`), and the live interrupt and boundary probes would otherwise run on act's default `node:16` image |

Documents (assignment item 4):

| File:line | Change | Reason |
|---|---|---|
| `docs/testing/CI_WORKFLOWS.md:7-13` | new paragraph: every job runs on the pinned hosted image `ubuntu-24.04`, never the floating `ubuntu-latest` (#784); the generators write it and the act runner replays no other; hosted `ubuntu-latest` moved to `ubuntu-26.04`, where the pinned CPython 3.12 wheels in `ci/constraints-ci.txt` do not install | item 4: the pinned image and why |
| `docs/testing/CI_WORKFLOWS.md:2036-2048` | runner contract: the one literal label, one `--platform` entry, `ubuntu-latest`/`ubuntu-22.04`/`ubuntu-26.04` refused by name and why; R697-1-01's exact sentence ("A label that has neither a `--platform` entry nor an entry in act's built-in table, such as `ubuntu-24.04`, ... so the self-test requires an entry for every accepted label.") | item 4, R697-1-01 verbatim; checked against the pinned act source (`receipts/imageos-readers.md`: built-in table maps `ubuntu-latest` to `node:16-buster-slim`) |
| `docs/testing/CI_WORKFLOWS.md:565` | physical job "four-core `ubuntu-24.04` job" | current job label |
| `docs/testing/TESTING.md:174` | "Both target a four-core `ubuntu-24.04` hosted worker." | current job label |
| `docs/testing/TESTING.md:331` | run 37892515345 "used a hosted `ubuntu-latest` runner, then the `ubuntu-24.04` image, ..." | historical label kept; its image added from the job log (`receipts/hosted-image-evidence.md`), so the measurement visibly applies to the pinned image |
| `tb/verilator/milan_dp/README.md:355`, `tb/verilator/milan_dp_gptp/README.md:27` | physical job "four-core `ubuntu-24.04`" | statement about the current job (named in TAKEN) |
| `sw/firmware/gtest/README.md:442` | "`ubuntu-24.04`, as the job installs them" (drops "(`ubuntu-latest`)") | `ubuntu-latest` is no longer 24.04 |

Left as is, with reason: `tb/verilator/follow_ring/Makefile:26` and `tb/verilator/milan_dp_render/Makefile:42` record the label of past run 37892515345 (true; build files kept out of the diff). Every other remaining `ubuntu-latest` explains or probes the refusal (`receipts/census.md`).

## New checks, planted mutants, failing words

All mutants: one exact replacement in a scratch copy, run as the runner contract gate runs (`python3 -I <0555 copy> --selftest --worktree <checkout>`), or a scratch detached worktree of the head for tree mutants. Driver `receipts/scripts/mutants.py`; per-mutant JSON and full log in `receipts/mutants/`. Control (unchanged head copy): rc 0, 621 ok, 0 FAIL.

| Mutant | rc | Failing checks (exact words) |
|---|---|---|
| `readd-ubuntu-latest` (`RUNS_ON_LABELS = ("ubuntu-latest", "ubuntu-24.04")`, dev's form) | 1 | `a job on ubuntu-latest is refused before act, and the refusal names ubuntu-latest`; `a job on ubuntu-latest is refused naming ubuntu-latest, before any Docker boundary or act command`; `act's platform list maps ubuntu-24.04 to the runner image, once, and no other label` |
| `latest-only` (`("ubuntu-latest",)`) | 1 | 8, including `a job on ubuntu-24.04 is accepted by the sandbox`, `a job on ubuntu-24.04 passes the sandbox and dry-run replays to an act command that maps ubuntu-24.04 to the runner image`, `a ubuntu-24.04 replay holds its job containers to the 8g memory and swap bound`, `slot 0 uses external ranges without staging` |
| `label-unchecked` (`if runs_on is None:`) | 1 | 11, including the three `refused before act, and the refusal names` arms, the three exact-literal arms, `self-hosted runner authority is refused`, `a nonliteral runner label is refused` |
| `platform-entry-dropped` (`*(),` for the platform words) | 1 | the `ubuntu-24.04` dry-run replay arm; `act's platform list maps ubuntu-24.04 ...`; `every runs-on label the sandbox accepts has a platform entry, and nothing else does` |
| `platform-maps-latest-too` (map `ubuntu-latest` as well) | 1 | `act's platform list maps ubuntu-24.04 ...`; `every runs-on label the sandbox accepts has a platform entry, and nothing else does` |
| `refusal-omits-label` (`runs on an unaccepted label`) | 1 | 8: the five refusal-names arms and the new reason arms `self-hosted runner authority is refused`, `a missing runner label is refused`, `a nonliteral runner label is refused` |
| `container-refusal-removed` | 1 | `job container authority is refused`; `service container authority is refused` |
| `action-refusal-removed` | 1 | `step-level action docker://alpine:3.20 is refused before act` and the other three step-level action arms |
| `reusable-refusal-removed` | 1 | `reusable workflow authority is refused` |

Why the fixtures and the sandbox-policy arms had to follow (demonstrations, not mutants of the head):

| Demonstration | rc | Result |
|---|---|---|
| `dev-narrowed-only`: dev's `act_ci.py` with only `RUNS_ON_LABELS` narrowed | 1 | self-test aborts: `Refusal: workflow .github/workflows/boundary-probe-selftest.yml job probe runs on 'ubuntu-latest'; only the literal labels ubuntu-24.04 are replayed` |
| `old-sandbox-arms`: head with dev's `selftest_sandbox_policy` put back | 0 | all arms ok |
| `old-sandbox-arms-container-refusal-removed` | **0** | `ok job container authority is refused`, `ok service container authority is refused`: the deleted refusal is not seen |
| `old-sandbox-arms-action-refusal-removed` | **0** | the four `ok step-level action ...` arms: the deleted refusal is not seen |

Tree mutants (where a reintroduced `ubuntu-latest` is caught):

| Mutant | gen `--check` | `ci_events --check` | runner contract gate |
|---|---|---|---|
| `template-job-on-latest` (docs template `wire-accountability`, regenerated) | 0 | 0 | 1: `shipping workflows satisfy the sandbox policy (workflow .github/workflows/docs.yml job wire-accountability runs on 'ubuntu-latest'; only the literal label ubuntu-24.04 is replayed)` |
| `generator-emits-latest` (watcher in `ci_runtime_workflows.py`, not regenerated) | 1: `.github/workflows/<each>.yml: regenerate the gate jobs` (all four) | not run | not run |
| `generator-emits-latest-regenerated` | 0 | 0 | 1: `... job ci-fail-fast runs on 'ubuntu-latest' ...`, plus `slot 0`/`slot 3 uses external ranges without staging` |
| `hand-edited-workflow` (rtl.yml `verilator-suites`, no regeneration) | 1: `.github/workflows/rtl.yml: regenerate the gate jobs` | 1: `generated gate jobs must match their complete inventory and aggregate ...` | not run |
| `physical-job-on-latest` (rtl template, regenerated) | 0 | 1: `physical-gptp must match its pinned schedule, budget, steps and evidence` | 1: `... job physical-gptp runs on 'ubuntu-latest' ...` |

So a job put back on `ubuntu-latest` through a template or generator passes the generator check and `ci_events.py` (except `physical-gptp`), and is caught by the runner contract gate's `shipping workflows satisfy the sandbox policy` arm, which the hosted docs workflow runs (docs-gates-2, inside the required `docs-check`), and by the trusted act replay itself.

## Gate table

Head `847eb4dd`, every command run directly in the checkout, one log and rc file per gate (`receipts/scripts/gates.py`, never piped), all rc 0.

- Renderer venv: the pinned Markdown renderer environment, CPython 3.14.8, PyYAML 6.0.3, cmarkgfm 2025.10.22, html5lib 1.1 (`receipts/gates/`, 58 gates).
- Hosted pair: scratch CPython 3.12.3 venv with PyYAML 6.0.2 from `ci/constraints-ci.txt` and the renderer from `tools/markdown/requirements.txt` (`receipts/gates-py312/`, 28 gates).

| Gate (workflow step) | Commands | Renderer venv | Hosted pair |
|---|---|---|---|
| Generator check mode (CI scheduling step) | `python3 scripts/ci_gate_workflows.py --check` | 0 | 0 |
| Yosys shard selector | `python3 scripts/yosys_shards.py --selftest` | 0 | 0 |
| CI event and SHA contract gate | `python3 scripts/ci_events.py --check` (2199 items); `python3 scripts/ci_events.py --selftest` (5236 arms) | 0, 0 | 0, 0 |
| Local act runner contract gate | `python3 scripts/act_ci.py --selftest` (623 ok); then `install -m 0555` copy and `python3 -I <copy> --selftest --worktree <checkout>` (621 ok) | 0, 0 | 0, 0 |
| CI scheduling and evidence controls, the other 13 commands | `ci_gate_workflows_selftest.py`, `ci_case_receipts_selftest.py`, `ci_make_cases_selftest.py`, `ci_maap_cases_selftest.py`, `ci_capture_cases_selftest.py`, `ci_suite_pieces_selftest.py`, `ci_suite_collect_selftest.py`, `ci_fail_fast_selftest.py`, `ci_runtime_evidence_selftest.py`, `ci_install_cache_selftest.py`, `generate_ci_evidence_pins.py --check`, `ci_workflow_plan_selftest.py`, `ci_manifest_selftest.py` | all 0 | all 0 |
| Scope classifier | `python3 scripts/ci_scope.py --selftest`; this change's file list classifies `true` (RTL/tooling relevant) | 0, 0 | 0 |
| Link health (gate_7) | `python3 scripts/docs_check.py` | 0 | 0 |
| Added-line em-dash | `python3 scripts/check_em_dash.py --base a8594bb95631fa5c49d18fa0bbc9530e31ad59aa` (26 added lines, 5 pages, 0 findings); `--selftest` | 0, 0 | 0 |
| Concise audience documentation | `check_doc_style.py` and `--selftest`; `check_gptp_docs.py` and `--selftest` | 0, 0, 0, 0 | 0 (style) |
| Audience diagram no-drift | `docs/DOC_MAP.gen.py --check`/`--selftest`; `docs/diagrams/timesync_chain.gen.py --check`/`--selftest` | 0 x4 | - |
| Feature status | `check_feature_status.py`; `--self-test` | 0, 0 | - |
| Per-page contents | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0, 0, 0 | -, 0, 0 |
| Doc cited-path, archive | `check_doc_paths.py`; `check_archive.py` and `--selftest` | 0, 0, 0 | 0 (paths) |
| Bare-metal scope (reads `tb/verilator/milan_dp/README.md`) | `check_baremetal_only.py --check`; `--selftest` | 0, 0 | - |
| docs-check-no-git | `git archive HEAD` export, empty gitlink dirs, no `.git`: `docs_check.py`; `check_feature_status.py` | 0, 0 | - |
| Python idiom | `check_py_idiom.py` (every budget line unchanged, e.g. long function 9 <= 9; over-long line 0); `--selftest` | 0, 0 | 0 |
| Hygiene, fail-fast, test-evidence, TODO ownership | each `--check`/plain and `--selftest` | all 0 | - |
| Shell idiom | `check_sh_idiom.py`; `--selftest` | 0, 0 | - |
| Code-quality measurement self-tests | `measure_control_flow.py --selftest`; `measure_cohesion.py --selftest` | 0, 0 | - |

Bootstrap (assignment item 5), offline: dev's trusted `act_ci.py` (blob `904d4fda`), installed 0555 and run `-I --selftest --worktree <head checkout>`: rc 0, `ok shipping workflows satisfy the sandbox policy` (`receipts/bootstrap/dev-runner-on-head.log`); dev's `validate_workflow_sandbox` loaded by path accepts all 46 head jobs, all `ubuntu-24.04` (`receipts/bootstrap/dev-sandbox-on-head-workflows.txt`). The trusted runner on dev therefore replays this PR.

## Not run, with reason

- Verilator sweep, campaigns, Vivado: no RTL in the change (brief: not required). No Vivado lock taken, no shard units started.
- rtl-fast `bdd-conformance` (`cd tests && behave`): nothing under `tests/` reads a workflow, `act_ci.py`, `CI_WORKFLOWS.md`, `TESTING.md` or any changed README, and `ci_scope.py`'s `GATE_READ_DOCS` names none of the changed pages, so the change does not reach it.
- The act-first replica of this PR and any live act or Docker run: bootstrap rule; the candidate runner was run only offline (`--selftest`), never with `--sudo`, against a real PR, or through a host act slot; no Docker daemon contacted.
- Hosted runs: not pushed. The acceptance item "a hosted run of the PR shows `Image: ubuntu-24.04` on every job, and every required check is green", and the post-merge dev push run that restores the ruleset, are the manager's.
- Docs gates that read no changed file (diagram PNG/wavedrom, solution, submodule docs, traceability matrix) and the HDL, C/C++ and SystemVerilog ratchets: not reached.

## STOP conditions

None hit.

## Acceptance (assignment items)

1. Met: every generator that writes `runs-on` emits `ubuntu-24.04` (census: `ci_gate_workflows.py`, `ci_runtime_workflows.py`, `ci_suite_workflows.py`; `yosys_shards.py` and `ci_install_workflows.py` write none); all four workflows regenerated through the generator, no hand edits (workflow diff is exactly the 46 label lines).
2. Met: no `ubuntu-latest` in `.github/` or the generators (`git grep` exit 1); `RUNS_ON_LABELS = ("ubuntu-24.04",)`; a job on `ubuntu-latest` is refused by name before act (arms and mutants above).
3. Met: `ci_events.py --check`/`--selftest`, `ci_gate_workflows.py --check`, `yosys_shards.py --selftest`, `act_ci.py --selftest` and the runner contract gate rc 0 on both interpreters.
4. Met: `CI_WORKFLOWS.md` states the pinned image and why, carries R697-1-01's exact sentence; `TESTING.md` names `ubuntu-24.04` where it names the current label.
5. Met offline: dev's trusted runner accepts every head job; the changed runner was tested offline only.
- Issue #784 closing items not in this PR's power: a hosted run of this PR with `Image: ubuntu-24.04` on every job and every required check green, then a hosted dev push run after merge and the ruleset restore. PR body therefore says "Relates to #784".

## Open risks

- act sets `ImageOS` from the label (`ubuntu-latest` -> `ubuntu20`, `ubuntu-24.04` -> `ubuntu24`, pinned act source `pkg/runner/run_context.go:1066-1073`), so the replay's `ImageOS` changes with this PR. Nothing in `.github/`, `scripts/` or `ci/` reads it, and `actions/setup-python@v5` (resolved today to `a26af69be951a213d495a4c3e4e4022e16d87065`) has no `ImageOS` reference in `dist/setup/index.js` or `dist/cache-save/index.js` (`receipts/imageos-readers.md`). The runner resolves `@v5` at replay time, so a later v5 could differ.
- Every cache key that hashes `.github/workflows/*.yml` misses once on the first hosted run after this change (the keys bind the workflow text by design).
- The workflows' first hosted run on this head is the real proof of the image; offline evidence cannot show `Image: ubuntu-24.04`.
