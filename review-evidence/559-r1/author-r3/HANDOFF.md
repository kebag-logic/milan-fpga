# [A314] Round 3 handoff

Status: implementation and local validation complete; ready for independent review.
Issue: https://github.com/kebag-logic/milan-fpga/issues/559
Pull request: https://github.com/kebag-logic/milan-fpga/pull/564
Assignment: https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5832136947
Branch: `559-capture-copy`.
Starting head: `31808e6525a83955bc4322ac8ac6871f9e6b10e6`.
Final local head: `b02af0480d3a3061df24683d522799d1759f7c33`.
Commit: `Pin the capture measurement gate in the workflow contract`.
The commit has one subject line, no body, and no trailers.
The worktree is clean. The commit is local and unpublished.

## Change list

Only these two repository files changed in round 3:

- `scripts/ci_events.py:1012`: record the capture step name and canonical
  command at position 28, after the record-space gate and before the
  saved-state writer gate. Shared validation permits exactly `name` and `run`.
- `scripts/ci_events.py:7083`: update existing count expectations to 50,
  including removal findings with 49 remaining steps.
- `scripts/ci_events.py:7118`: retain the cited-path/archive swap control
  at its shifted indices; update its diagnostic and the rename control.
- `scripts/ci_events.py:7129`: add four capture-specific sequence/skip controls.
- `scripts/ci_events.py:7693`: update the SDK-installation removal count.
- `docs/testing/CI_WORKFLOWS.md:1184`: document ordering, command, receipt
  checks, embedded controls, dependencies, and pin protection.

The precedents were `1576f089` and `5251942a`.
The existing script-control generator and missing-record self-test are unchanged.
The complete record removes the inventory mismatch and index error.
All 24 existing carrier-sequence control identities remain; four were added.
See `control-retention.log` and `ci-events-selftest.log`.
Round 2 measurements, gate logic, workflow, other documentation, product
inputs and submodule pins are unchanged.

## Capture-step mutation controls and failures

The new step has nine verified refusals. Four controls were explicitly added;
the existing carrier machinery supplies five. The in-memory control harness
returned 0 after verifying every expected diagnostic below.
Full diagnostics are in `mutation-controls.log` and `mutation-controls.json`.

| Control | Expected failure observed |
|---|---|
| removed | job `docs-check` must carry exactly 50 steps, in the recorded order (found 49) |
| reordered | job `docs-check` step 28 must be the step named `Capture measurement census and clock gate` |
| renamed | job `docs-check` step 28 must be the step named `Capture measurement census and clock gate` |
| if: false | (`Capture measurement census and clock gate`) must carry no `if` |
| no-op | job `docs-check` step 28 (`Capture measurement census and clock gate`) script is not the canonical form: line 1 must be 'python3 scripts/check_nvm_capture.py' |
| or-true | job `docs-check` step 28 (`Capture measurement census and clock gate`) script is not the canonical form: line 1 must be 'python3 scripts/check_nvm_capture.py' |
| append-command | job `docs-check` step 28 (`Capture measurement census and clock gate`) script is not the canonical form: line 2 must be None |
| continue-on-error | job `docs-check` step 28 (`Capture measurement census and clock gate`) must carry no `continue-on-error` |
| missing record | job `docs-check` step 28 (`Capture measurement census and clock gate`) must record a canonical normalized `run` script |

The complete self-test also passes whitespace normalization, matched record
maintenance, and its vacuity proof.
The capture gate runs its input and timing self-tests without a flag.
Its bytes, records, CPU clock, configured clock, system clock, omitted OFF
maximum and exact-limit/one-tick-over controls all pass.
Four additional CLI mutations returned the expected rc 1:

| Command | Expected failure | Result |
|---|---|---|
| `python3 scripts/check_nvm_capture.py --mutation bytes` | capture inputs changed; remeasure both arms | expected rc 1 |
| `python3 scripts/check_nvm_capture.py --mutation records` | capture inputs changed; remeasure both arms | expected rc 1 |
| `python3 scripts/check_nvm_capture.py --mutation clock` | capture inputs changed; remeasure both arms | expected rc 1 |
| `python3 scripts/check_nvm_capture.py --mutation ignore-off-timing` | OFF timing omitted from maximum | expected rc 1 |

These negative runs are successful controls, not failed acceptance gates.
See `capture-mutation-results.json` and `nvm-capture-mutation-*.log`.

## Gate table

Every required gate's final run returned 0 on the final local head.
Commands ran serially in the foreground, without pipelines, with 3600-second
per-gate timeouts. The command proxy preserved exit statuses.
`gate-results.json` records commands, durations and the exact head.

| Command | Result | Log |
|---|---|---|
| `python3 scripts/ci_events.py --check` | rc 0 | `ci-events-check.log` |
| `python3 scripts/ci_events.py --selftest` | rc 0 | `ci-events-selftest.log` |
| `python3 scripts/act_ci.py --selftest` | rc 0 | `act-contract-selftest.log` |
| `python3 scripts/check_nvm_capture.py` | rc 0 | `nvm-capture.log` |
| `python3 -B scripts/docs_check.py` | rc 0 | `docs-git.log` |
| `GIT_DIR=/dev/null python3 -B scripts/docs_check.py` | rc 0 | `docs-no-git.log` |
| `python3 scripts/check_em_dash.py --base a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4` | rc 0 | `em-dash.log` |
| `python3 scripts/check_doc_style.py` | rc 0 | `doc-style.log` |
| `python3 scripts/check_doc_style.py --selftest` | rc 0 | `doc-style-selftest.log` |
| `python3 scripts/gen_toc.py --check` | rc 0 | `toc-check.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | rc 0 | `toc-anchors.log` |
| `python3 scripts/check_doc_paths.py` | rc 0 | `doc-paths.log` |
| `python3 scripts/check_py_idiom.py` | rc 0 | `python-idiom.log` |
| `python3 scripts/check_py_idiom.py --selftest` | rc 0 | `python-idiom-selftest.log` |
| `python3 scripts/check_sh_idiom.py` | rc 0 | `shell-idiom.log` |
| `python3 scripts/check_sh_idiom.py --selftest` | rc 0 | `shell-idiom-selftest.log` |
| `git diff --check` | rc 0 | `diff-check.log` |
| `git diff --check 31808e6525a83955bc4322ac8ac6871f9e6b10e6 HEAD` | rc 0 | `commit-diff-check.log` |

The shell gate's actual name is `check_sh_idiom.py`; both commands match
its workflow step. The runner command is exactly the workflow's offline
self-test. No live workflow orchestration was invoked.

The contract check passed 1,655 items; its self-test passed 2,197 arms.
Both documentation modes checked 166 Markdown and 874 text files.
Git mode passed 23 scrub controls and four routing controls.
The no-Git mode passed 22 scrub controls and four routing controls.
Its one expected skip is inventory parity, which requires Git.
`GIT_DIR=/dev/null` selected the filesystem inventory without removing
metadata or creating another checkout.

The first em-dash invocation returned rc 2 because html5lib was absent.
Its diagnostic remains in `em-dash-missing-dependency.log`.
Installing `tools/markdown/requirements.txt` with `--require-hashes` into a
new temporary environment outside the output directory resolved it.
The unchanged gate then returned 0. See `markdown-dependencies.log`.
`validation-environment.txt` identifies that external environment.
No packages, environments, SDKs, tool prefixes or repository exports are
stored in the output directory.

## Delivery and remaining review

`PR-BODY.md` contains the full current public body, updated for round 3.
Its first line is `[A314]`; it retains `Closes #559` and Round 2.
It contains no absolute home paths or attribution footer.
`PR-BODY-CURRENT.json` retains the body fetched from the public PR.
The PR itself was not edited.

`REVIEW-READY.md` is the prepared Issue comment.
Review readiness publication: [posted on #559](https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5832296849).
Independent re-review and exact-head hosted acceptance remain outstanding.
There is no claimed review verdict or hosted success for this local commit.
No push, PR creation or edit, merge, other checkout, hardware access,
sub-agent work, or donor edit was performed.
