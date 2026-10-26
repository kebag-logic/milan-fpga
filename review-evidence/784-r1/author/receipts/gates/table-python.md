| gate | command | rc | seconds |
|---|---|---|---|
| py-idiom | `python3 scripts/check_py_idiom.py` | 0 | 5.8 |
| py-idiom-selftest | `python3 scripts/check_py_idiom.py --selftest` | 0 | 6.1 |
| hygiene-check | `python3 scripts/check_hygiene.py --check` | 0 | 0.5 |
| hygiene-selftest | `python3 scripts/check_hygiene.py --selftest` | 0 | 0.5 |
| fail-fast-check | `python3 scripts/measure_fail_fast.py --check` | 0 | 2.1 |
| fail-fast-selftest | `python3 scripts/measure_fail_fast.py --selftest` | 0 | 2.1 |
| test-evidence-check | `python3 scripts/measure_test_evidence.py --check` | 0 | 9.2 |
| test-evidence-selftest | `python3 scripts/measure_test_evidence.py --selftest` | 0 | 9.4 |
| todo-ownership | `python3 scripts/check_todo_ownership.py` | 0 | 2.3 |
| todo-ownership-selftest | `python3 scripts/check_todo_ownership.py --selftest` | 0 | 2.4 |
| control-flow-selftest | `python3 scripts/measure_control_flow.py --selftest` | 0 | 0.1 |
| cohesion-selftest | `python3 scripts/measure_cohesion.py --selftest` | 0 | 0.1 |
