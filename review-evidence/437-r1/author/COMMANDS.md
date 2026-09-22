# Exact-head author command record

Head `65df1df50a80cd5f540a93d8f0cfabc97da3da75`, tree `da06c8609b7a574e3df121fbcb8a1fc8f207dcb7`. All 25 listed commands exit 0. Individual JSON/log files record UTC, status and full output.

- `rtk proxy python3 -B scripts/gen_toc.py --selftest`: exit 0 (`head-toc.log`).
- `rtk proxy python3 -B scripts/gen_toc.py --check`: exit 0 (`head-toc-check.log`).
- `rtk proxy python3 -B scripts/gen_toc.py --verify-anchors`: exit 0 (`head-toc-anchors.log`).
- `rtk proxy python3 -B scripts/gen_toc.py --sites`: exit 0 (`head-toc-sites.log`).
- `rtk proxy python3 -B scripts/check_em_dash.py --selftest`: exit 0 (`head-em-dash.log`).
- `rtk proxy python3 -B scripts/check_em_dash.py --base 88e9276b2a220c716f64a843f7e1eb8f9265e896`: exit 0 (`head-em-dash-base.log`).
- `rtk proxy python3 -B scripts/docs_check.py`: exit 0 (`head-docs.log`).
- `rtk proxy python3 -B scripts/docs_check.py --selftest`: exit 0 (`head-docs-selftest.log`).
- `rtk proxy python3 -B scripts/check_doc_style.py`: exit 0 (`head-doc-style.log`).
- `rtk proxy python3 -B scripts/check_doc_style.py --selftest`: exit 0 (`head-doc-style-selftest.log`).
- `rtk proxy python3 -B scripts/check_doc_paths.py`: exit 0 (`head-doc-paths.log`).
- `rtk proxy python3 -B scripts/check_py_idiom.py`: exit 0 (`head-py-idiom.log`).
- `rtk proxy python3 -B scripts/check_py_idiom.py --selftest`: exit 0 (`head-py-idiom-selftest.log`).
- `rtk proxy python3 -B scripts/check_hygiene.py --check`: exit 0 (`head-hygiene.log`).
- `rtk proxy python3 -B scripts/check_hygiene.py --selftest`: exit 0 (`head-hygiene-selftest.log`).
- `rtk proxy python3 -B scripts/measure_test_evidence.py --check`: exit 0 (`head-test-evidence.log`).
- `rtk proxy python3 -B scripts/measure_test_evidence.py --selftest`: exit 0 (`head-test-evidence-selftest.log`).
- `rtk proxy python3 -B scripts/measure_fail_fast.py --check`: exit 0 (`head-fail-fast.log`).
- `rtk proxy python3 -B scripts/measure_fail_fast.py --selftest`: exit 0 (`head-fail-fast-selftest.log`).
- `rtk proxy python3 -B scripts/check_todo_ownership.py`: exit 0 (`head-todo.log`).
- `rtk proxy python3 -B scripts/check_todo_ownership.py --selftest`: exit 0 (`head-todo-selftest.log`).
- `rtk proxy python3 -B scripts/measure_cohesion.py --selftest`: exit 0 (`head-cohesion-selftest.log`).
- `rtk proxy python3 -B scripts/measure_control_flow.py --selftest`: exit 0 (`head-control-flow-selftest.log`).
- `rtk proxy python3 -B scripts/ci_events.py --check`: exit 0 (`head-ci-events.log`).
- `rtk proxy python3 -B scripts/ci_events.py --selftest`: exit 0 (`head-ci-events-selftest.log`).

Additional reproducible scripts: receipt.py (base/head corpus and cached-GFM comparison), mutations.py (17 expected failures in each shipped selftest), refusal_controls.py (50 character cases and invalid base), preservation.py (707 prior inputs, #507 bytes, gate policy functions, tracked scope, submodule pins). See HANDOFF.md for exact invocations and actual child exits.
