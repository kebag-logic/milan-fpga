[A159] COMMAND RECEIPTS

Committed revision: `ad62493186576144f9fa1568babad012bc9ad8ca`. Commands run from the named candidate worktree unless an explicit scratch `--root` is present. Shell invocations used `rtk proxy`; JSON records the exact underlying argv. Compilation environment for focused gates: `MAKEFLAGS=-j8`, `CMAKE_BUILD_PARALLEL_LEVEL=8`. No builder, full RTL suite, Docker/act or candidate host orchestrator ran.

| Exact underlying command | Exit | Raw log directory |
|---|---|---|
| `python3 -B scripts/ci_events.py --check` | 0 | `gates/` |
| `python3 -B scripts/ci_events.py --selftest` | 0 | `gates/` |
| `python3 -B scripts/docs_check.py` | 0 | `gates/` |
| `python3 -B scripts/gen_toc.py --check` | 0 | `gates/` |
| `python3 -B scripts/check_doc_paths.py` | 0 | `gates/` |
| `python3 -B scripts/check_em_dash.py --base b17580b91deb11f3441dfc5d7f9fafe539d929b8` | 0 | `gates/` |
| `python3 -B scripts/check_doc_style.py` | 0 | `gates/` |
| `python3 -B scripts/check_py_idiom.py` | 0 | `gates/` |
| `python3 -B scripts/check_py_idiom.py --selftest` | 0 | `gates/` |
| `python3 -B scripts/check_hygiene.py --check` | 0 | `gates/` |
| `python3 -B scripts/check_todo_ownership.py` | 0 | `gates/` |
| `python3 -B scripts/measure_fail_fast.py --check` | 0 | `gates/` |
| `python3 -B scripts/check_feature_status.py` | 0 | `gates/` |
| `python3 -B scripts/lint_rtl.py --check` | 0 | `gates/` |
| `git diff --check` | 0 | `gates/` |
| `python3 -B scripts/ci_events.py --check` | 0 | `committed-gates/` |
| `python3 -B scripts/ci_events.py --selftest` | 0 | `committed-gates/` |
| `python3 -B scripts/check_em_dash.py --base b17580b91deb11f3441dfc5d7f9fafe539d929b8` | 0 | `committed-gates/` |
| `git diff --check 6af65a151663e1301f1983a6c9d22650a0b35da9 HEAD` | 0 | `committed-gates/` |

`gates/` contains focused checks during preparation. The em-dash gate judges committed HEAD; its authoritative revised-head receipt is `committed-gates/em-dash.log`, run after commit. Actual pristine check and full self-test were also rerun from committed HEAD. Every receipt under `after/` is regenerated from the committed source.

Reproduce the evidence instruments (EVIDENCE is this directory, REPO is the candidate worktree):

```sh
rtk proxy python3 -B "$EVIDENCE/probe_mutants.py" "$REPO" "$EVIDENCE/after" --phase after
rtk proxy python3 -B "$EVIDENCE/probe_controls.py" "$REPO" "$EVIDENCE/controls"
```

Reproduce the key historical and revised observations directly without reconstructing a checkout:

```sh
rtk proxy python3 -B "$EVIDENCE/before/M5b.py" --selftest --root "$EVIDENCE/before/inputs"
rtk proxy python3 -B "$EVIDENCE/after/M5b.py" --selftest --root "$EVIDENCE/after/inputs"
rtk proxy python3 -B "$EVIDENCE/after/real.py" --selftest --root "$EVIDENCE/after/inputs"
```

Expected exits respectively: 0, 1, 0. `before/results.json` and `after/results.json` contain every exact check/selftest argv, exit status, summary and AC5 analogue findings. `controls/results.json` records exact maintenance CLI commands and results; the separate inventories bind every new arm to its intended refusal.

The three initialized submodules remain at their original pins; `integrity.json` records them and the unchanged live base/remote PR head. `revision.patch` is the exact author commit diff. `public-state/` contains the input public contract, review reports and accepted decisions. No private reasoning or CLI transcript was used as an authority.
