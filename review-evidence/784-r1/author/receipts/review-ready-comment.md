[A673] REVIEW READY
Commit: `42dbe6bd42c950a7acedce56fcf29b82543123c6` on `784-act-runner-ubuntu-2404` (one commit on dev `d385b38e`; not pushed, the manager pushes and opens the PR)
Changed:
- `scripts/act_ci.py`: new `RUNS_ON_LABELS = ("ubuntu-latest", "ubuntu-24.04")`. `validate_workflow_sandbox` accepts exactly those literals and refuses every other `runs-on` by name (`runs on 'ubuntu-26.04'; only the literal labels ubuntu-latest, ubuntu-24.04 are replayed`). `build_act_command` passes one `--platform <label>=catthehacker/ubuntu:full-latest` per accepted label. The hosted 16 GB memory model is stated for both labels.
- Self-tests: 12 new arms (`selftest_runner_labels`, `selftest_runner_platforms`, `selftest_runner_label_replay`), 610 -> 622 arm lines.
- `docs/testing/CI_WORKFLOWS.md`: the runner contract paragraph names both labels, says others are refused by name, and why (hosted `ubuntu-latest` moved to 26.04; step 2 pins `ubuntu-24.04`), and why every accepted label needs a platform entry.
- Workflows, templates and generators unchanged.
Validation (all rc 0, at the head above, offline only; CPython 3.12.3 + PyYAML 6.0.2, the hosted pair, and CPython 3.14 + PyYAML 6.0.3 under the pinned Markdown renderer):
python3 scripts/act_ci.py --selftest   (selftest: PASS)
python3 -I <installed 0555 copy>/act_ci.py --selftest --worktree <checkout>   (the runner contract gate as docs-gates-2 runs it; selftest: PASS)
python3 scripts/ci_events.py --check   (2199 contract items OK)
python3 scripts/ci_events.py --selftest   (PASS, 5236 arms)
git diff --exit-code d385b38e5282b395ca55d49d135e46a93f56a340 -- .github   (empty)
docs: docs_check.py (also on a tree export with no .git), check_feature_status.py and --self-test, check_em_dash.py --base d385b38e and --selftest, check_doc_style.py and --selftest, gen_toc.py --selftest/--verify-anchors/--check, check_doc_paths.py, check_baremetal_only.py --check/--selftest, DOC_MAP.gen.py --check/--selftest
python: check_py_idiom.py (budget unchanged) and --selftest, check_hygiene.py, measure_fail_fast.py, measure_test_evidence.py, check_todo_ownership.py (each check and selftest), measure_control_flow.py/measure_cohesion.py --selftest
the CI scheduling and evidence controls step, all 14 commands (including ci_runtime_evidence_selftest.py and generate_ci_evidence_pins.py --check, which read act_ci.py)
Mutants, each in a scratch copy run as `python3 -I <copy> --selftest --worktree <checkout>`, all rc 1 with named failures:
- platform list drops ubuntu-24.04 (dev's form): fails `act's platform list maps ubuntu-latest and ubuntu-24.04 to the runner image, once each`, `every runs-on label the sandbox accepts has a platform entry, and nothing else does` and the ubuntu-24.04 dry-run replay check
- ubuntu-24.04 mapped to act's default node image: the same three
- RUNS_ON_LABELS back to ubuntu-latest only: 4 failures, including `a job on ubuntu-24.04 is accepted by the sandbox`
- sandbox accepts any `ubuntu-` label: 5 failures, including `a job on ubuntu-26.04 is refused before act, and the refusal names ubuntu-26.04`
- refusal text without the label (dev's wording): 3 failures, the refusal-names checks
Acceptance criteria (assignment, step 1):
1. met: ubuntu-24.04 accepted as ubuntu-latest is; both on the same image via two `--platform` entries; ubuntu-22.04 and ubuntu-26.04 refused by name (arms above).
2. met: the hosted memory model names both labels; an arm proves a ubuntu-24.04 replay carries the same 8g memory and swap bound.
3. met: a ubuntu-24.04 job passes the real sandbox and dry-run replays to an act command mapping its label; a ubuntu-26.04 job is refused naming the label before any Docker boundary; the platform-map mutant fails named checks.
4. met: act_ci.py --selftest, the runner contract gate, ci_events.py --check/--selftest rc 0; workflows byte-identical to dev.
5. met: CI_WORKFLOWS.md as above.
Issue #784 as a whole stays open: step 2 acceptance is not in this change, so the PR body says "Relates to #784".
STOP condition: not hit. The pinned act's `--platform` is a repeatable flag mapping each `label=image` entry; a no-daemon dry run of the pinned binary (no privilege, Docker pointed at a socket that does not exist) starts the ubuntu-24.04 job on the runner image with two entries, and with dev's single entry prints "Skipping unsupported platform" and exits 0, the false green the new cross-check guards against.
Open risks/questions:
- This PR's own hosted checks can still fail at pip resolution on ubuntu-26.04 (run 40187576861 job 121179871493: `Image: ubuntu-26.04`, `ResolutionImpossible`), because the workflows still say ubuntu-latest until step 2. That is #784's defect, not this change's; how this head gets its rtl-fast verdict is the manager's call.
- For step 2: act sets `ImageOS` per label (ubuntu20 vs ubuntu24). Nothing in `.github/` or `scripts/` and nothing in the audited setup-python v5 bundle reads it.
