[A679] REVIEW READY
Commit: `847eb4dd031eb3891b61773f4a8324cb2ed6cdc0` on `784-pin-ubuntu-2404` (tree `05ae0179dbffa852651aa7ec8367758b380672d0`; one commit on dev `a8594bb9`; not pushed, the manager pushes and opens the PR)
Changed:
- Templates: all 22 source jobs in `.github/ci-templates/` say `runs-on: ubuntu-24.04`. One historical comment no longer names the label.
- Generators: `ci_gate_workflows.py` (aggregates), `ci_runtime_workflows.py` (watcher, tail guard, collector) and `ci_suite_workflows.py` (unions, Yosys tool job) emit `ubuntu-24.04`. Census: no other `runs-on` writer; `yosys_shards.py`'s only label mention was a comment, now `ubuntu-24.04`, the image of its weight run.
- Workflows: regenerated only through `python3 scripts/ci_gate_workflows.py`. The diff is exactly 46 `runs-on: ubuntu-latest` -> `runs-on: ubuntu-24.04` lines.
- `ci_events.py`: the `physical-gptp` whole-job contract and the self-test fixtures pin `ubuntu-24.04`.
- `act_ci.py`:
  - `RUNS_ON_LABELS = ("ubuntu-24.04",)`.
  - A job on `ubuntu-latest` is refused before act, naming it: `runs on 'ubuntu-latest'; only the literal label ubuntu-24.04 is replayed`.
  - act gets one `--platform` entry.
  - Label, platform and replay arms follow.
  - Every fixture and probe workflow moves to `ubuntu-24.04`.
  - The sandbox-policy arms now each require their own refusal reason, because a fixture on a refused label is refused by its label first and the old Refusal-only arms passed with the container or action refusal deleted.
- `docs/testing/CI_WORKFLOWS.md`: the page opening states the pinned image and why (hosted `ubuntu-latest` moved to 26.04, where the pinned CPython 3.12 wheels do not install). The runner contract names the single label and carries R697-1-01's exact `--platform` sentence. The physical job line is updated.
- `docs/testing/TESTING.md`: the physical job targets `ubuntu-24.04`. Run 37892515345 keeps its `ubuntu-latest` label and gains its image, `ubuntu-24.04`, from its job log.
- Three suite and harness READMEs that describe the current job now say `ubuntu-24.04`.
Validation (all rc 0 at the head, offline only; CPython 3.14.8 + PyYAML 6.0.3 under the pinned Markdown renderer, and CPython 3.12.3 + PyYAML 6.0.2, the hosted pair):
python3 scripts/ci_gate_workflows.py --check
python3 scripts/yosys_shards.py --selftest
python3 scripts/ci_events.py --check   (2199 contract items OK)
python3 scripts/ci_events.py --selftest   (PASS, 5236 arms)
python3 scripts/act_ci.py --selftest   (623 ok, 0 FAIL)
python3 -I <installed 0555 copy>/act_ci.py --selftest --worktree <checkout>   (the runner contract gate; 621 ok, 0 FAIL)
the other 13 commands of the CI scheduling and evidence controls step
python3 scripts/ci_scope.py --selftest   (this change classifies as RTL/tooling relevant)
- Docs gates: docs_check (also on a tree export with no .git), check_em_dash --base a8594bb9 (26 added lines, 0 findings) and --selftest, check_doc_style and check_gptp_docs (each with --selftest), DOC_MAP.gen.py and timesync_chain.gen.py (--check, --selftest), check_feature_status and --self-test, gen_toc (--selftest, --verify-anchors, --check), check_doc_paths, check_archive and --selftest, check_baremetal_only (--check, --selftest).
- Python gates: check_py_idiom (budget unchanged) and --selftest, check_hygiene, measure_fail_fast, measure_test_evidence, check_todo_ownership, check_sh_idiom (each check and selftest), measure_control_flow/measure_cohesion --selftest.
- Bootstrap, offline: dev's trusted act_ci.py (blob 904d4fda), installed 0555, runs `--selftest --worktree <head>` with rc 0, including `ok shipping workflows satisfy the sandbox policy`. Its validate_workflow_sandbox accepts all 46 head jobs.
Mutants (scratch copies run as the contract gate runs; tree mutants in scratch worktrees). The control is rc 0; each mutant fails with rc 1 and named checks:
- `RUNS_ON_LABELS` back to dev's two labels (3): `a job on ubuntu-latest is refused before act, and the refusal names ubuntu-latest`; `a job on ubuntu-latest is refused naming ubuntu-latest, before any Docker boundary or act command`; `act's platform list maps ubuntu-24.04 to the runner image, once, and no other label`
- `("ubuntu-latest",)` (8); label check reduced to `is None` (11); platform words dropped (3); `ubuntu-latest` also mapped (2); refusal text without the label (8)
- container/services refusal deleted (2), unapproved-action refusal deleted (4), reusable-workflow refusal deleted (1)
- Demonstrations: with the old sandbox-policy arms put back, deleting the container refusal or the action refusal leaves the self-test rc 0, so those arms were vacuous. dev's runner with only its label narrowed aborts at the boundary-probe fixture.
- Tree: a template or generator job back on `ubuntu-latest` and regenerated passes the generator check and ci_events, and fails the runner contract gate with `shipping workflows satisfy the sandbox policy (workflow .github/workflows/docs.yml job wire-accountability runs on 'ubuntu-latest'; ...)`. Not regenerated, it fails the generator check (`regenerate the gate jobs`). A hand-edited workflow fails the generator check and ci_events. The physical job fails ci_events (`physical-gptp must match ...`) and the contract gate.
Acceptance criteria (assignment, step 2):
1. Met: every `runs-on` writer emits `ubuntu-24.04`; all four workflows are regenerated through the generator, with no hand edits.
2. Met: no `ubuntu-latest` in `.github/` or the generators (`git grep` exit 1); `ubuntu-24.04` is the only accepted label; `ubuntu-latest` is refused by name; self-tests and mutants follow.
3. Met: ci_events --check/--selftest, the generator check mode, act_ci.py --selftest and the runner contract gate are rc 0 on both interpreters.
4. Met: CI_WORKFLOWS.md states the pinned image and why, plus R697-1-01's exact sentence; TESTING.md names `ubuntu-24.04`.
5. Met offline: the trusted dev runner accepts every head job; the changed runner was tested offline only.
Issue #784 stays open: its hosted proof (`Image: ubuntu-24.04` on every job, every required check green), the dev push run after merge and the ruleset restore are not in this change, so the PR body says "Relates to #784".
STOP condition: not hit.
Open risks/questions:
- act's `ImageOS` in the replay moves from `ubuntu20` to `ubuntu24` (pinned act `pkg/runner/run_context.go:1066-1073`). No file in `.github/`, `scripts/` or `ci/` reads it, and `actions/setup-python@v5` (today `a26af69be951a213d495a4c3e4e4022e16d87065`) contains no `ImageOS` in `dist/setup` or `dist/cache-save`. The runner resolves `@v5` at replay time.
- Every cache key that hashes `.github/workflows/*.yml` misses once on the first hosted run.
- Not run: the Verilator sweep, campaigns and Vivado (no RTL), and `bdd-conformance` (nothing under `tests/` reads a changed file).
