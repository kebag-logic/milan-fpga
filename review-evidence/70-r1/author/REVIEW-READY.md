[A401] REVIEW READY
Commit: `6029890c8ba6fd35fac3d3210b8f3a7b30bb1769` (local, not pushed)
Previous lane-0 commit: `0309a9eec3c1fa06c6338def6638e307e99bdfc1`
Branch: `70-d3-contract`
Reviewers: [R380] internal; [R381] external.

Changed: recorded the [manager ruling](https://github.com/kebag-logic/milan-fpga/issues/70#issuecomment-5862405632) in a separate one-line documentation commit. All ten D3 section 15.1 rows now read RULED and reproduce the selected option exactly, retaining options, consequences and the adopted defaults.

DR3a is explicit in the acceptance text and lanes 1-5: lane 1 measures both deadline candidates; the manager ratifies or revises both before lane 2 implements. DR4 narrows shipping area acceptance to 1x1 TDM8 with the stage budgets, matched-head method and corrected #607 constraints. The 8x8 retains synthesis diagnostics; its post-place obligation remains open and blocked, not waived. It remains non-shipping until it fits (#584/#229). FASTCONNECT and snapshot cross-references agree with the ruled register.

Validation: every command below returned 0 at the committed head above, in the foreground without pipelines. Python checks used the repository hash-locked Markdown dependencies and PyYAML 6.0.3.

| Command | Exit |
|---|---|
| `python3 scripts/docs_check.py` | 0 |
| `python3 scripts/check_doc_paths.py` | 0 |
| `python3 scripts/check_doc_style.py` | 0 |
| `python3 scripts/gen_toc.py --check` | 0 |
| `python3 scripts/check_em_dash.py --base c07232228c12b72805dd20e6852bf93f25794da0` | 0 |
| `python3 scripts/check_baremetal_only.py --check` | 0 |
| `python3 scripts/ci_scope.py --selftest` | 0 |
| `git diff --check` | 0 |
| `git diff --check c07232228c12b72805dd20e6852bf93f25794da0 HEAD` | 0 |

Acceptance criteria: continuation complete. The ten selected options match the ruling exactly. All 26 FASTCONNECT checklist states are unchanged and retain reconciliation rows. Every child contract explicitly carries DR3a and DR4. HANDOFF.md and PR-BODY.md are updated in the assigned output directory, with committed-head gate logs. Worktree clean.

Open obligations: independent review; lane 1 measurements and the manager's pre-lane-2 DR3a ratification; implementation, dependency closure and physical acceptance. This contract update claims no new product behavior or physical result. No processor, RTL, firmware or builder source changes; no push, PR operation or merge.
