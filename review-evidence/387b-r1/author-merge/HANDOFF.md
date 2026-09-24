# [A268] Merge-round handoff for issue #387

Author: [A268]. This is implementation and validation evidence for independent review.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5816975318

## Exact merge

- Branch: `387-media-rebase`.
- Head: `e68c1b1ac08c8b1e12a28e281b266d06f881e402`.
- Tree: `c8b28ac217337d5d5e12af41e9ece31e3e80e831`.
- First parent: `00d388d832189a93335935de7726b5e07dd6f0dc`.
- Second parent: `57456af96b3127b9d309a995bbbd35a6113ce52d`.
- Common ancestor used for the overlap census: `59b816708852472da6ed4576386c30ebd5f8f839`.
- Exactly one new first-parent commit, made with `git merge --no-ff --no-commit` and the one-line commit subject `Merge dev into #387 preserving the servo guard and one-event media re-base`.
- The commit has no body or trailers. No rebase.
- After fetching `origin dev`, the remote dev tip equalled the specified second parent.
- After the merge, `git submodule update --init third_party/verilog-axis protocol-processor gptp-processor` exited 0.

Submodule pins at validation:

| Path | Pin |
|---|---|
| `third_party/verilog-axis` | `48ff7a7e2ef782cf778d47910cf85835c64b1bce` |
| `protocol-processor` | `09f9bf3846511f8388d995126502ed92eaa65213` |
| `gptp-processor` | `e5dcea6e351abff18a27a00f8e345f3251bdbd8f` |

## Conflict resolution

There was one conflicted file: `docs/design/GM_LOSS_RECOVERY.md`.

| Location at the merge head | Resolution |
|---|---|
| `docs/design/GM_LOSS_RECOVERY.md:150` | Preserve the branch's `tu` row: Yes, driven by the plane's step pulse. |
| `docs/design/GM_LOSS_RECOVERY.md:151` | Preserve the branch's render row: Yes, one counted step event at PDU end; the GM identity adds no second re-centre. Preserve the existing 42-delay evidence. |
| `docs/design/GM_LOSS_RECOVERY.md:152` | Take #539's grid-aligner row verbatim, including the owner decision on #387: no independent re-centre; isolate the step at the servo; retain the #545/#546 paths and conditional option B. |
| `docs/design/GM_LOSS_RECOVERY.md:154` | Take #539's servo row verbatim: discard the local-step window, hold trim/integrator, count at `MCSRV_STAT[15:10]`, and retain the documented slew/talker-step gaps. |
| `docs/design/GM_LOSS_RECOVERY.md:155` | Preserve the branch's outgoing `mr` row: Yes, one step-triggered toggle regardless of selected media source. |
| `docs/design/GM_LOSS_RECOVERY.md:156` | Preserve the branch's MEDIA_RESET row: Yes, count the toggle transmitted, with the gmstep evidence. |
| `docs/design/GM_LOSS_RECOVERY.md:157` | Preserve the branch's pending-restart row: Yes, per-stream target merges an unstamped request; a request after stamping is a new restart. Preserve T17 evidence. |
| `docs/design/GM_LOSS_RECOVERY.md:185` | Preserve the clean merge's #539 servo-test reference to `Vphc_step`. |
| `docs/design/GM_LOSS_RECOVERY.md:187` | Preserve the branch's T17 pending-restart coverage reference. |

The two incoming rows and five branch rows are byte-identical to their respective parents. Every file changed by only one parent is byte-identical to that parent's version. The merge introduces no additional RTL or test edits. Evidence: `resolution-check.txt`, `merge-resolution.patch`, and the two parent deltas.

## Clean-merged overlap census and coherence

The census intersects the paths changed from the common ancestor to each parent. It contains five files: the one conflicted file above and these four clean merges. There are no additional clean-merged overlaps.

| Clean-merged file | What was checked |
|---|---|
| `docs/design/TIME_SYNC.md:148` and `docs/design/TIME_SYNC.md:197` | #539's step-window discard and implausible-window guard coexist with #387's step-driven render re-centre. The render row excludes an identity-only trigger and links to the merged recovery decision. |
| `docs/reference/REGISTER_MAP.md:127` and `docs/reference/REGISTER_MAP.md:1966` | CRF selection gates the CRF restart causes; a PHC step still restarts every running output and counts MEDIA_RESET. The servo word separately retains #539's saturating discarded-window field at bits 15:10, reserved bit 9 and unchanged register address. |
| `docs/testing/TESTING.md:267`, `docs/testing/TESTING.md:483` and `docs/testing/TESTING.md:501` | The nine-control gmstep inventory and three default controls coexist with the silicon-scale servo step harness and T17's two restart mutants. The entries describe distinct coverage and match their recipes. |
| `tb/verilator/milan_dp/README.md:470`, `tb/verilator/milan_dp/README.md:501` and `tb/verilator/milan_dp/README.md:504` | The default gmstep and mutant claims survive. Adjacent limitations preserve #539's decided aligner behavior and separate servo test, plus #387's T17 pending-restart test. No stale open aligner question or pending datapath edit is restored. |

`CHANGELOG.md` is not an overlap: only the branch changed it after the common ancestor. Its entry at `CHANGELOG.md:30` is byte-identical to the first parent and agrees with the merged one-event render/restart contract. The statement at `CHANGELOG.md:49` that no CSR moves remains correct; #539 documents a field at the existing servo address.

## Gate results

All gates below ran at the exact merge head above. Commands ran synchronously in the foreground, without pipelines, with a four-hour per-gate timeout. The outer runner had a twelve-hour timeout. Raw output goes directly to each log, preserving the command's exit code.

The no-git CI mode ran on a `git archive` export of the exact commit, inside this output directory. It is a source export with no Git metadata, not another checkout. Both documentation modes scanned 165 Markdown files and 859 text files. The no-git inventory-parity self-test is explicitly inapplicable there, as expected.

The first em-dash and contents checks refused to run because the pinned Markdown dependencies were missing (rc 2). Installing `tools/markdown/requirements.txt` with `--require-hashes` in `gate-venv` resolved that setup issue. Only those two checks were rerun, using `PATH` with `gate-venv/bin` first. Their original and retry logs are retained; the table reports the completed checks. The repository did not change during this setup repair.

| Command / mode | rc | Result | Log |
|---|---|---|---|
| `python3 scripts/docs_check.py` | 0 | 0 findings; 165 Markdown / 859 text files; scrub 23/23, routing 4/4 | [docs-check.log](docs-check.log) |
| `python3 scripts/docs_check.py` (no Git metadata) | 0 | 0 findings; same 165 / 859 inventory; scrub 22/22, routing 4/4; Git-only parity arm inapplicable | [docs-check-no-git.log](docs-check-no-git.log) |
| `python3 scripts/check_feature_status.py` (no Git metadata) | 0 | 0 findings; second command of the no-git CI job | [feature-status-no-git.log](feature-status-no-git.log) |
| `python3 scripts/check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d` | 0 | 0 findings; 89 added lines across 6 pages; planted controls 339/339 | [em-dash-retry.log](em-dash-retry.log) |
| `python3 scripts/check_doc_style.py` | 0 | 22 current documents OK | [doc-style.log](doc-style.log) |
| `python3 scripts/gen_toc.py --check` | 0 | 107 annotated contents lists OK; 17 pages below threshold | [toc-retry.log](toc-retry.log) |
| `python3 scripts/check_doc_paths.py` | 0 | 841 cited paths resolve; 1 allowlisted | [doc-paths.log](doc-paths.log) |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | 69 modules; 0 untested; generator controls 5/5 | [module-matrix.log](module-matrix.log) |
| `python3 scripts/xvlog_gate.py --check` | 0 | PASS: 4 findings equal ratchet; 0 repository RTL, 4 pinned processors; live analysis ran | [xvlog.log](xvlog.log) |
| `python3 scripts/check_rtl_source_lists.py` | 0 | 103-file datapath closure in all 4 consumers; processor 32/38 tops, 6 recorded omissions | [rtl-source-lists.log](rtl-source-lists.log) |
| `cd tests && behave --no-capture -f plain` | 0 | 14 features, 344 scenarios, 1739 steps passed; 0 failures or skips | [behave.log](behave.log) |
| `git diff --check` | 0 | No whitespace errors in the working tree | [diff-check.log](diff-check.log) |
| `make -C tb/verilator/milan_dp gmstep` | 0 | 48 checks, 0 failures; default feed delay 0 | [gmstep.log](gmstep.log) |
| `make -C tb/verilator/tkdiag` | 0 | 90 checks, 0 failures; mutation runner 3/3 (clean plus both named mutants) | [tkdiag.log](tkdiag.log) |
| `make -C tb/verilator/mmcm_servo` | 0 | Unit 78/78; rails 8/8; PHC-step 113/113; all three default suites passed | [mmcm-servo.log](mmcm-servo.log) |
| `git diff --check 57456af96b3127b9d309a995bbbd35a6113ce52d HEAD` | 0 | Committed merge diff against the specified dev base is clean | [diff-against-dev-check.log](diff-against-dev-check.log) |

The original sequential runner retained rc 1 because its first em-dash and contents attempts returned rc 2. The successful retries are recorded separately. `final-gate-results.json` combines the completed gate results without altering the original logs or results.

## Review scope and artifacts

The assigned merge-round contract is met. The worktree is clean at the head above, and all three submodules match their pins. This report covers the requested local gates; it does not claim a new full datapath sweep, full gmstep mutation campaign, synthesis run, independent review verdict or physical acceptance. The existing #117, #545 and #546 scope remains unchanged.

No push, PR creation or edit, merge to dev, other checkout, delegation or hardware operation occurred. The sole public update for this round is the accompanying `[A268] REVIEW READY` issue comment.

- `merge-inputs.json`: exact parents, common ancestor and changed-path census.
- `merge-result.json`: merge head/tree, ordered parents, one-line subject and submodule pins.
- `branch-delta.patch`, `dev-delta.patch`: each side against the common ancestor.
- `branch-overlap.patch`, `dev-overlap.patch`: the overlapping paths on each side.
- `merge-resolution.patch`: the conflict and its resolution as a remerge diff.
- `merge-relative-to-dev.patch`: the resulting branch change against the specified dev base.
- `resolution-check.txt`: exact row and exclusive-file preservation check.
- `gate-results.json`, `markdown-retries.json`, `final-gate-results.json`: original attempts, successful retries and final gate table.
- `run_gates.py`, `retry_markdown.py`: synchronous command runners.
- `markdown-environment.json`: locked dependency versions and lock-file hash.
- `merge-head.tar`, `no-git-export/`: exact committed source used for no-git CI validation.
- `final-status.txt`: final clean branch, head and pin check.
- `REVIEW_READY.md`: issue-comment body.
- `MANIFEST.sha256`: hashes of the handoff and top-level evidence files.
