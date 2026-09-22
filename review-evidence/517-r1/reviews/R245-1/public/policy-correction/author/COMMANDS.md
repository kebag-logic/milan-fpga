# Factual command ledger

Each row links the raw combined output and its argv/exit receipt.
Precommit tests name the then-current parent HEAD; they are not clean-head runs.
The final gate check/selftest and byte proof name the correction commit.

| Label | Exit | Exact argv |
|---|---:|---|
| [baseline-check](raw/baseline-check.log) ([receipt](raw/baseline-check.json)) | 1 | `rtk proxy python3 scripts/check_baremetal_only.py --check` |
| [baseline-selftest](raw/baseline-selftest.log) ([receipt](raw/baseline-selftest.json)) | 0 | `rtk proxy python3 scripts/check_baremetal_only.py --selftest` |
| [preliminary-selftest](raw/preliminary-selftest.log) ([receipt](raw/preliminary-selftest.json)) | 0 | `rtk proxy python3 scripts/check_baremetal_only.py --selftest` |
| [preliminary-python-idiom](raw/preliminary-python-idiom.log) ([receipt](raw/preliminary-python-idiom.json)) | 0 | `rtk proxy python3 scripts/check_py_idiom.py` |
| [preliminary-check](raw/preliminary-check.log) ([receipt](raw/preliminary-check.json)) | 0 | `rtk proxy python3 scripts/check_baremetal_only.py --check` |
| [preliminary-boundary-probe](raw/preliminary-boundary-probe.log) ([receipt](raw/preliminary-boundary-probe.json)) | 2 | `rtk proxy python3 scripts/check_baremetal_only.py --selftest` |
| [preliminary-integrity](raw/preliminary-integrity.log) ([receipt](raw/preliminary-integrity.json)) | 0 | `rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/517-policy-author/scripts/integrity.py preliminary-integrity --working` |
| [corrected-selftest](raw/corrected-selftest.log) ([receipt](raw/corrected-selftest.json)) | 0 | `rtk proxy python3 scripts/check_baremetal_only.py --selftest` |
| [runner-controls](raw/runner-controls.log) ([receipt](raw/runner-controls.json)) | 0 | `rtk proxy python3 tb/verilator/milan_dp/test_sim_pool.py` |
| [mutation-probes](raw/mutation-probes.log) ([receipt](raw/mutation-probes.json)) | 0 | `rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/517-policy-author/scripts/mutation_probes.py` |
| [phase-controls](raw/phase-controls.log) ([receipt](raw/phase-controls.json)) | 0 | `rtk proxy python3 tb/verilator/milan_dp/test_render_phase_observation.py` |
| [public-authority](raw/public-authority.log) ([receipt](raw/public-authority.json)) | 0 | `rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/517-policy-author/scripts/capture_public.py` |
| [docs-check](raw/docs-check.log) ([receipt](raw/docs-check.json)) | 0 | `rtk proxy python3 scripts/docs_check.py` |
| [ownership-controls](raw/ownership-controls.log) ([receipt](raw/ownership-controls.json)) | 0 | `rtk proxy python3 scripts/suite_shards.py --selftest` |
| [tally-controls](raw/tally-controls.log) ([receipt](raw/tally-controls.json)) | 0 | `rtk proxy python3 scripts/suite_tally.py --selftest` |
| [python-idiom](raw/python-idiom.log) ([receipt](raw/python-idiom.json)) | 0 | `rtk proxy python3 scripts/check_py_idiom.py` |
| [hygiene](raw/hygiene.log) ([receipt](raw/hygiene.json)) | 0 | `rtk proxy python3 scripts/check_hygiene.py --check` |
| [fail-fast](raw/fail-fast.log) ([receipt](raw/fail-fast.json)) | 0 | `rtk proxy python3 scripts/measure_fail_fast.py --check` |
| [test-evidence](raw/test-evidence.log) ([receipt](raw/test-evidence.json)) | 0 | `rtk proxy python3 scripts/measure_test_evidence.py --check` |
| [todo-ownership](raw/todo-ownership.log) ([receipt](raw/todo-ownership.json)) | 0 | `rtk proxy python3 scripts/check_todo_ownership.py` |
| [stage-correction](raw/stage-correction.log) ([receipt](raw/stage-correction.json)) | 0 | `rtk proxy git add -- scripts/check_baremetal_only.py` |
| [commit-correction](raw/commit-correction.log) ([receipt](raw/commit-correction.json)) | 0 | `rtk proxy git commit -m 'Bound simulation host-tool policy masks to their source contexts'` |
| [committed-check](raw/committed-check.log) ([receipt](raw/committed-check.json)) | 0 | `rtk proxy python3 scripts/check_baremetal_only.py --check` |
| [committed-integrity](raw/committed-integrity.log) ([receipt](raw/committed-integrity.json)) | 0 | `rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/517-policy-author/scripts/integrity.py committed-integrity` |
| [committed-em-dash](raw/committed-em-dash.log) ([receipt](raw/committed-em-dash.json)) | 0 | `rtk proxy python3 scripts/check_em_dash.py --base 7ab1c8d0ad073fbc1977c455dea89b7b318d4e52` |
| [committed-selftest](raw/committed-selftest.log) ([receipt](raw/committed-selftest.json)) | 0 | `rtk proxy python3 scripts/check_baremetal_only.py --selftest` |
| [committed-whitespace](raw/committed-whitespace.log) ([receipt](raw/committed-whitespace.json)) | 0 | `rtk proxy git diff --check 7ab1c8d0ad073fbc1977c455dea89b7b318d4e52 HEAD` |
| [policy-scope-proof](raw/policy-scope-proof.log) ([receipt](raw/policy-scope-proof.json)) | 0 | `rtk proxy python3 $WORKSPACE_HOME/milan-fpga-management/2026-09-22/517-policy-author/scripts/policy_scope_proof.py` |
| [final-status](raw/final-status.log) ([receipt](raw/final-status.json)) | 0 | `rtk proxy git status --porcelain=v1 --branch --untracked-files=all` |
| [remote-source-branch](raw/remote-source-branch.log) ([receipt](raw/remote-source-branch.json)) | 0 | `rtk proxy git ls-remote origin refs/heads/517-bounded-simulation-pool` |
| [final-commit](raw/final-commit.log) ([receipt](raw/final-commit.json)) | 0 | `rtk proxy git show -s --format=fuller HEAD` |
| [post-review-ready](raw/post-review-ready.log) ([receipt](raw/post-review-ready.json)) | 0 | `rtk proxy gh issue comment 517 --repo kebag-logic/milan-fpga --body-file $WORKSPACE_HOME/milan-fpga-management/2026-09-22/517-policy-author/REVIEW-READY.md` |

The baseline exit 1 and preliminary boundary exit 2 are preserved failures.
Mutation exits are separately recorded in mutations/receipts.json and are expected refusals.
