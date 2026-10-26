| gate | command | rc | seconds |
|---|---|---|---|
| ci-events-check | `python3 scripts/ci_events.py --check` | 0 | 0.8 |
| ci-events-selftest | `python3 scripts/ci_events.py --selftest` | 0 | 199.6 |
| runner-contract-gate | `python3 scripts/act_ci.py --selftest; install_dir="$(mktemp -d)"; trap 'rm -rf "$install_dir"' EXIT; install -m 0555 scripts/act_ci.py "$install_dir/act_ci.py"; python3 -I "$install_dir/act_ci.py" --selftest --worktree "$PWD"` | 0 | 100.4 |
