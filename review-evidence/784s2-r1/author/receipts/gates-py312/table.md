| interpreter | `python3 -c 'import sys, yaml, cmarkgfm; print(sys.version.split()[0], yaml.__version__, cmarkgfm.__version__ if hasattr(cmarkgfm, "__version__") else "")'` | 0 | 0.0 s |
| gen-check | `python3 scripts/ci_gate_workflows.py --check` | 0 | 0.6 s |
| yosys-shards-selftest | `python3 scripts/yosys_shards.py --selftest` | 0 | 0.0 s |
| ci-events-check | `python3 scripts/ci_events.py --check` | 0 | 0.7 s |
| act-ci-selftest | `python3 scripts/act_ci.py --selftest` | 0 | 67.2 s |
| act-ci-contract-gate | `sh -c 'set -eu; install_dir="$(mktemp -d)"; trap "rm -rf \"$install_dir\"" EXIT; install -m 0555 scripts/act_ci.py "$install_dir/act_ci.py"; python3 -I "$install_dir/act_ci.py" --selftest --worktree "$PWD"'` | 0 | 33.5 s |
| ci-scope-selftest | `python3 scripts/ci_scope.py --selftest` | 0 | 22.5 s |
| ci-events-selftest | `python3 scripts/ci_events.py --selftest` | 0 | 209.2 s |
| sched-gate-workflows-selftest | `python3 scripts/ci_gate_workflows_selftest.py` | 0 | 9.2 s |
| sched-case-receipts | `python3 scripts/ci_case_receipts_selftest.py` | 0 | 0.5 s |
| sched-make-cases | `python3 scripts/ci_make_cases_selftest.py` | 0 | 0.1 s |
| sched-maap-cases | `python3 scripts/ci_maap_cases_selftest.py` | 0 | 0.1 s |
| sched-capture-cases | `python3 scripts/ci_capture_cases_selftest.py` | 0 | 0.1 s |
| sched-suite-pieces | `python3 scripts/ci_suite_pieces_selftest.py` | 0 | 6.2 s |
| sched-suite-collect | `python3 scripts/ci_suite_collect_selftest.py` | 0 | 2.4 s |
| sched-fail-fast | `python3 scripts/ci_fail_fast_selftest.py` | 0 | 1.0 s |
| sched-runtime-evidence | `python3 scripts/ci_runtime_evidence_selftest.py` | 0 | 5.9 s |
| sched-install-cache | `python3 scripts/ci_install_cache_selftest.py` | 0 | 0.1 s |
| sched-evidence-pins | `python3 scripts/generate_ci_evidence_pins.py --check` | 0 | 0.0 s |
| sched-workflow-plan | `python3 scripts/ci_workflow_plan_selftest.py` | 0 | 0.2 s |
| sched-manifest | `python3 scripts/ci_manifest_selftest.py` | 0 | 0.0 s |
| docs-check | `python3 scripts/docs_check.py` | 0 | 5.3 s |
| em-dash | `python3 scripts/check_em_dash.py --base a8594bb95631fa5c49d18fa0bbc9530e31ad59aa` | 0 | 2.7 s |
| toc-check | `python3 scripts/gen_toc.py --check` | 0 | 5.8 s |
| toc-anchors | `python3 scripts/gen_toc.py --verify-anchors` | 0 | 4.0 s |
| doc-style | `python3 scripts/check_doc_style.py` | 0 | 0.1 s |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0 | 0.1 s |
| py-idiom | `python3 scripts/check_py_idiom.py` | 0 | 5.8 s |
