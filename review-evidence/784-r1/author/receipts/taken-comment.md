[A673] TAKEN
Branch: `784-act-runner-ubuntu-2404`, from dev `d385b38e5282b395ca55d49d135e46a93f56a340`
Authoritative references: #784 (Decision, step 1; Acceptance, step 1); assignment https://github.com/kebag-logic/milan-fpga/issues/784#issuecomment-6400713781; `scripts/act_ci.py` (`validate_workflow_sandbox` runs-on check, `build_act_command` platform map, the hosted memory model beside `CONTAINER_MEMORY`); `docs/testing/CI_WORKFLOWS.md` (runner contract paragraph); AGENTS.md section 5 bootstrap rule.
Interpreted scope: `act_ci.py` accepts `runs-on: ubuntu-24.04` exactly as it accepts `ubuntu-latest` and passes act one `--platform <label>=<runner image>` entry per accepted label, both naming the same image; every other label (for example `ubuntu-22.04`, `ubuntu-26.04`) is refused before act, with the label in the refusal. The hosted 16 GB memory model is stated for both labels. Self-tests add: a `ubuntu-24.04` job accepted by the sandbox and carried through an offline dry-run replay to the act command; a `ubuntu-26.04` job refused naming the label; a check that fails when the new label is dropped from the platform map (mutant planted and recorded). `CI_WORKFLOWS.md` states both labels and why. No workflow, generator or template change; workflows stay byte-identical to dev. No STOP so far: the pinned act's `--platform` is a repeatable flag mapping each label to an image, so a second label needs no change outside `act_ci.py`.
Validation plan (offline only, no privilege, no Docker, no real PR):
python3 scripts/act_ci.py --selftest
python3 -I <installed copy>/act_ci.py --selftest --worktree <checkout>   (the runner contract gate, as docs-gates-2 runs it)
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
git diff --exit-code d385b38e -- .github
plus the docs gates the page edit reaches (docs_check, check_em_dash, gen_toc, check_doc_paths, check_feature_status, check_baremetal_only) under the pinned Markdown renderer, and the Python gates act_ci.py reaches (check_py_idiom, check_hygiene, measure_fail_fast, measure_test_evidence, check_todo_ownership).
Blockers: none
