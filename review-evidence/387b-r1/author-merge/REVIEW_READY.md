[A268] REVIEW READY

Commit: `e68c1b1ac08c8b1e12a28e281b266d06f881e402` on `387-media-rebase` (local only).

One merge commit, parents `00d388d832189a93335935de7726b5e07dd6f0dc` and `57456af96b3127b9d309a995bbbd35a6113ce52d`, under the [merge-round assignment](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5816975318). One-line subject, no body or trailers.

Resolved `docs/design/GM_LOSS_RECOVERY.md`: kept #539's CRF-servo and grid-aligner rows, including the #387 aligner decision, and the branch's Yes rows for `tu`, render re-centre, `mr`, MEDIA_RESET and pending-restart merge, with their evidence. Each selected row is unchanged from its owning parent.

Clean-merged overlaps checked for coherence: `docs/design/TIME_SYNC.md`, `docs/reference/REGISTER_MAP.md`, `docs/testing/TESTING.md`, and `tb/verilator/milan_dp/README.md`. Both sides are retained. `CHANGELOG.md` was also checked: only the branch changed it since the common ancestor, and its entry remains intact. No additional edits were needed.

Validation at this exact merge head, all final exit codes 0:

| Gate | Result |
|---|---|
| `python3 scripts/docs_check.py`, Git and no-Git CI modes; no-Git `check_feature_status.py` | PASS |
| `check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d`, `check_doc_style.py`, `gen_toc.py --check`, `check_doc_paths.py`, `docs/traceability/gen_module_matrix.py --check` | PASS |
| `xvlog_gate.py --check`, `check_rtl_source_lists.py` | PASS; live parsing has 4 findings equal to the existing ratchet, 0 in repository RTL |
| `cd tests && behave --no-capture -f plain` | 344 scenarios, 1739 steps; 0 failures or skips |
| `git diff --check`, also the committed diff against the specified dev base | PASS |
| `make -C tb/verilator/milan_dp gmstep` | 48/48 |
| `make -C tb/verilator/tkdiag` | 90/90; mutation runner 3/3, including both named pending-restart mutants |
| `make -C tb/verilator/mmcm_servo` | Unit 78/78, rails 8/8, PHC-step 113/113 |

The em-dash and contents checks initially refused missing pinned Markdown dependencies. Installing the locked requirements in an isolated environment and rerunning those two checks resolved that setup issue; the commit stayed unchanged. Original and retry logs are retained.

All three required submodules were initialized after the merge and match their pins. The worktree is clean. The merge-round contract is met; this is author evidence for independent review. No push, PR operation, merge to dev or hardware operation was performed.

`HANDOFF.md` contains the resolution with file:line, overlap census and full gate table. It and all evidence are in the A268 author packet, `$HOME/milan-fpga-management/2026-09-23/387-a268/`.
