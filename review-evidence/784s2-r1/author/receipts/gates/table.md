| gen-check | `python3 scripts/ci_gate_workflows.py --check` | 0 | 0.5 s |
| yosys-shards-selftest | `python3 scripts/yosys_shards.py --selftest` | 0 | 0.0 s |
| ci-events-check | `python3 scripts/ci_events.py --check` | 0 | 0.6 s |
| act-ci-selftest | `python3 scripts/act_ci.py --selftest` | 0 | 65.3 s |
| act-ci-contract-gate | `sh -c 'set -eu; install_dir="$(mktemp -d)"; trap "rm -rf \"$install_dir\"" EXIT; install -m 0555 scripts/act_ci.py "$install_dir/act_ci.py"; python3 -I "$install_dir/act_ci.py" --selftest --worktree "$PWD"'` | 0 | 30.6 s |
| ci-events-selftest | `python3 scripts/ci_events.py --selftest` | 0 | 172.2 s |
| sched-gate-workflows-selftest | `python3 scripts/ci_gate_workflows_selftest.py` | 0 | 7.4 s |
| sched-case-receipts | `python3 scripts/ci_case_receipts_selftest.py` | 0 | 0.6 s |
| sched-make-cases | `python3 scripts/ci_make_cases_selftest.py` | 0 | 0.1 s |
| sched-maap-cases | `python3 scripts/ci_maap_cases_selftest.py` | 0 | 0.1 s |
| sched-capture-cases | `python3 scripts/ci_capture_cases_selftest.py` | 0 | 0.1 s |
| sched-suite-pieces | `python3 scripts/ci_suite_pieces_selftest.py` | 0 | 7.2 s |
| sched-suite-collect | `python3 scripts/ci_suite_collect_selftest.py` | 0 | 2.8 s |
| sched-fail-fast | `python3 scripts/ci_fail_fast_selftest.py` | 0 | 0.8 s |
| sched-runtime-evidence | `python3 scripts/ci_runtime_evidence_selftest.py` | 0 | 5.1 s |
| sched-install-cache | `python3 scripts/ci_install_cache_selftest.py` | 0 | 0.1 s |
| sched-evidence-pins | `python3 scripts/generate_ci_evidence_pins.py --check` | 0 | 0.0 s |
| sched-workflow-plan | `python3 scripts/ci_workflow_plan_selftest.py` | 0 | 0.2 s |
| sched-manifest | `python3 scripts/ci_manifest_selftest.py` | 0 | 0.0 s |
| docs-check | `python3 scripts/docs_check.py` | 0 | 6.9 s |
| em-dash | `python3 scripts/check_em_dash.py --base a8594bb95631fa5c49d18fa0bbc9530e31ad59aa` | 0 | 2.6 s |
| em-dash-selftest | `python3 scripts/check_em_dash.py --selftest` | 0 | 2.5 s |
| doc-style | `python3 scripts/check_doc_style.py` | 0 | 0.1 s |
| doc-style-selftest | `python3 scripts/check_doc_style.py --selftest` | 0 | 0.0 s |
| gptp-docs | `python3 scripts/check_gptp_docs.py` | 0 | 0.2 s |
| gptp-docs-selftest | `python3 scripts/check_gptp_docs.py --selftest` | 0 | 0.2 s |
| doc-map-check | `python3 docs/DOC_MAP.gen.py --check` | 0 | 0.4 s |
| doc-map-selftest | `python3 docs/DOC_MAP.gen.py --selftest` | 0 | 0.4 s |
| timesync-chain-check | `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 | 0.3 s |
| timesync-chain-selftest | `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 | 0.4 s |
| feature-status | `python3 scripts/check_feature_status.py` | 0 | 1.1 s |
| feature-status-selftest | `python3 scripts/check_feature_status.py --self-test` | 0 | 1.1 s |
| toc-selftest | `python3 scripts/gen_toc.py --selftest` | 0 | 0.8 s |
| toc-anchors | `python3 scripts/gen_toc.py --verify-anchors` | 0 | 3.7 s |
| toc-check | `python3 scripts/gen_toc.py --check` | 0 | 5.3 s |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0 | 0.1 s |
| archive | `python3 scripts/check_archive.py` | 0 | 0.4 s |
| archive-selftest | `python3 scripts/check_archive.py --selftest` | 0 | 0.0 s |
| baremetal-check | `python3 scripts/check_baremetal_only.py --check` | 0 | 25.0 s |
| baremetal-selftest | `python3 scripts/check_baremetal_only.py --selftest` | 0 | 5.5 s |
| py-idiom | `python3 scripts/check_py_idiom.py` | 0 | 5.0 s |
| py-idiom-selftest | `python3 scripts/check_py_idiom.py --selftest` | 0 | 4.9 s |
| hygiene-check | `python3 scripts/check_hygiene.py --check` | 0 | 0.4 s |
| hygiene-selftest | `python3 scripts/check_hygiene.py --selftest` | 0 | 0.4 s |
| fail-fast-check | `python3 scripts/measure_fail_fast.py --check` | 0 | 1.8 s |
| fail-fast-selftest | `python3 scripts/measure_fail_fast.py --selftest` | 0 | 1.8 s |
| test-evidence-check | `python3 scripts/measure_test_evidence.py --check` | 0 | 8.1 s |
| test-evidence-selftest | `python3 scripts/measure_test_evidence.py --selftest` | 0 | 8.1 s |
| todo-ownership | `python3 scripts/check_todo_ownership.py` | 0 | 2.0 s |
| todo-ownership-selftest | `python3 scripts/check_todo_ownership.py --selftest` | 0 | 2.0 s |
| control-flow-selftest | `python3 scripts/measure_control_flow.py --selftest` | 0 | 0.1 s |
| cohesion-selftest | `python3 scripts/measure_cohesion.py --selftest` | 0 | 0.0 s |
| ci-scope-selftest | `python3 scripts/ci_scope.py --selftest` | 0 | 17.8 s |
| ci-scope-this-change | `sh -c 'python3 scripts/ci_scope.py < /tmp/a679-changed-files.txt'` | 0 | 0.1 s |
| no-git-docs-check | `python3 scripts/docs_check.py` | 0 | 6.9 s |
| no-git-feature-status | `python3 scripts/check_feature_status.py` | 0 | 1.2 s |
| sh-idiom | `python3 scripts/check_sh_idiom.py` | 0 | 0.3 s |
| sh-idiom-selftest | `python3 scripts/check_sh_idiom.py --selftest` | 0 | 0.3 s |
