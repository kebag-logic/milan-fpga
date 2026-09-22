[A163] HANDOFF

Issue #407 / PR #505, kebag-logic/milan-fpga.
Sole author: A163. Lane: `407-carrier-script-pins` in `$CANDIDATE`.
Commit subject: `Clarify remaining RTL workflow script pin gaps` (one line, no trailers).

Old head: `ad62493186576144f9fa1568babad012bc9ad8ca`.
Old tree: `6b279253aa7d3edd6d9b5e9adc1ed9caf6f13d75`.
New head: `5d45ecc0cf2dc572d538cbc534b5d9f95c8688e7`.
New tree: `2ec2d2e9931d250dacb945643cf3a444ec0e9a91`.
Actual merge base: `b17580b91deb11f3441dfc5d7f9fafe539d929b8`.
The original dev base, origin/dev and live remote dev matched that merge base at the final check.

Changed artifact: `docs/testing/CI_WORKFLOWS.md:768`, only the remaining-content-gap paragraph in item 12. The commit replaces two lines with four. It names the seven RTL jobs' scripts without specialized pins and the sibling full-ci-gate "Print the event and pin the one SHA this run validates" script as future #439 work. The four-carrier statements and all remaining document bytes are preserved.

Original finding: R220-2 MINOR Docs F3. The inaccurate current-tree prose is corrected; the executable gaps remain future #439 work. The finding is not relabeled or disposed of merely by linking #439. Independent reviewers determine its resolution.

Validation: every command below exited 0. Logs contain complete stdout/stderr and JSON command, working-directory, timestamp, duration and exit-status receipts.

| Exact command | Result | Log prefix |
|---|---|---|
| `rtk proxy python3 -B scripts/ci_events.py --check` | 1505 contract items | `logs/04-ci-events-check` |
| `rtk proxy python3 -B scripts/ci_events.py --selftest` | 1144 arms; vacuity control fails all 1046 workflow mutation arms | `logs/05-ci-events-selftest` |
| `rtk proxy python3 -B scripts/docs_check.py` | 0 findings; 163 Markdown and 826 scrubbed files; 23/23 scrub and 4/4 routing arms | `logs/06-docs-check` |
| `rtk proxy python3 -B scripts/gen_toc.py --check` | 105 pages with contents; 17 below threshold | `logs/07-gen-toc` |
| `rtk proxy python3 -B scripts/check_doc_paths.py` | 824 cited paths resolve; 1 allowlisted | `logs/08-doc-paths` |
| `rtk proxy git diff --check` | No whitespace errors before commit | `logs/09-diff-check-worktree` |
| `rtk proxy python3 -B scripts/check_em_dash.py --base b17580b91deb11f3441dfc5d7f9fafe539d929b8` | 0 findings over 49 added lines; 34/34 controls | `logs/12-em-dash` |
| `rtk proxy git diff --check b17580b91deb11f3441dfc5d7f9fafe539d929b8 HEAD` | No whitespace errors through the committed head | `logs/13-diff-check-head` |
| `rtk proxy git diff --check` | Clean working-tree diff after commit | `logs/14-diff-check-clean` |

The first six commands ran on the corrected working-tree bytes before the commit. The final hash audit proves those exact bytes are the new committed tree. The em-dash gate ran after committing because its documented `--base REV` mode compares REV to HEAD. Its base was computed with `rtk proxy git merge-base origin/dev HEAD` and verified against live remote dev.

Tracked scope and integrity: all 850 non-gitlink files match their final HEAD blobs, including filesystem modes. All 849 files other than CI_WORKFLOWS.md are byte-identical to the starting head. All four gitlinks and the submodule status output are unchanged. The checker, workflow files, canonical records, normalization, mutation population and production RTL are unchanged. The index exactly matches HEAD; no assume-unchanged or skip-worktree flags are set. `git status --porcelain=v1 --untracked-files=all --ignore-submodules=none` is empty.

Per-file SHA-256 and Git blob receipts are in `logs/01-source-before.json` and `logs/15-source-after.json`; audit commands/results accompany them. The exact committed patch is `logs/15-committed.patch`. The old index SHA-256 is `6aebda216ed9a2606dfc14fdd3ba4a1bd529faac9c1cf04bea28b48338614501`; the new index SHA-256 is `2d77d68f7c0ab8cd6b04d865e63f658c588019ea9d19e8cacdc90f2045e1a474`.

Historical AC5 attribution: A10 measured act behavior at `6af65a151663e1301f1983a6c9d22650a0b35da9`; R220-2 independently read those receipts and retained them for the prior head `ad62493186576144f9fa1568babad012bc9ad8ca`. This author did not execute act or remeasure AC5. Those receipts are historical, not execution on the new head. Any retention decision for the corrected head belongs to the manager and independent reviewers.

Remaining manager work: publish the full review-ready evidence and corrected head; complete the required local/native gates, supported trusted act replicas and exact-head hosted gates; arrange targeted cold R219/R220 Docs and Conformance re-reviews. Only reviewers may accept any unchanged banked RTL/Robustness/Tests coverage. Candidate-merge validation and eventual post-merge containment remain required. No review verdict or completion ledger is supplied by this author.

The local commit is unpushed. PR505 remains draft at remote head `ad62493186576144f9fa1568babad012bc9ad8ca`. No PR metadata or project mutation, push, merge, other agent, Docker/act execution, privileged action, hardware access, dependency installation, unrelated gate or other worktree edit was performed. The optional malformed-pristine traceback suggestion was not adopted.

Public references:

- [Original R220-2 F3](https://github.com/kebag-logic/milan-fpga/pull/505#issuecomment-5772521129).
- [Accepted correction scope](https://github.com/kebag-logic/milan-fpga/pull/505#issuecomment-5772548304).
- [Settled #439 scope decision](https://github.com/kebag-logic/milan-fpga/issues/439#issuecomment-5772547851).
- [A163 TAKEN before edit](https://github.com/kebag-logic/milan-fpga/issues/407#issuecomment-5772948224).
- [A163 factual issue handoff](https://github.com/kebag-logic/milan-fpga/issues/407#issuecomment-5772987925).
