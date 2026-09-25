[A318] Round 4 handoff

Issue: #551. PR: #553. Branch: `551-licence-real-grant`.
Assignment: [items 1 and 2](https://github.com/kebag-logic/milan-fpga/issues/551#issuecomment-5833406989).

Starting head: `f219a5edaa191b33acc8b77abd22469f8f0db1f9`.
Completed local head: `6e4a3b420e055ef7529ceb16bb2ab5be93c34487`.
Commit: `docs: refresh licence grant guarantee and control failure count`.
Origin confirmed: `https://github.com/kebag-logic/milan-fpga.git`.

## Changes

| File:line | Change | Assigned finding |
|---|---|---|
| `tests/features/milan_streaming_licence.feature:92` | Replaces the stale three-line comment with the current-TSpec guarantee, processor #112 adoption through #508, and the `[I]` changed-TSpec refusal check. | R296-2 N1 = R297-2 F1 |
| `tb/verilator/milan_dp/README.md:468` | Reports 34 control failures: 28 `[I]` assertions and 6 `[J]` admitted-case timing checks. | R296-2 S2 |

Only these two repository files changed. Non-comment feature lines are
byte-identical to the starting head. No executable code, steps, assertions,
submodule pins or acceptance criteria changed. The commit has one subject
line, no body and no trailers. See `receipts/scope-check.log`.

## Gate results

All commands ran sequentially in the foreground without shell pipelines.
Commands below ran from the candidate unless another directory is stated.
The pinned Markdown dependencies were installed under `/tmp` from the
repository lock. No environment or source export is in this output directory.

| Gate | Result | Receipt |
|---|---|---|
| `cd tests && behave --no-capture -f plain` | rc 0; 14 features, 344 scenarios and 1739 steps pass; none skipped | `receipts/behave.log` |
| `python3 scripts/bdd_mutants.py` (output directory; `MILAN_SOURCE` names the candidate) | rc 0; ACTIVE-only, raw-grant-only, OR and extra-term caught; clean controls 5/5 before and after | `receipts/bdd-mutants.log`, `receipts/bdd-*.log` |
| `grep -rnE "Residual\|pending fix\|previous slope" tests/` | No output; grep rc 1 is its expected no-match status; the absence assertion passes with rc 0 | `receipts/obsolete-wording.log`, `gate-results.json` |
| `python3 -B scripts/docs_check.py` (Git inventory) | rc 0; 0 findings; 165 Markdown files, 868 text files; 23/23 scrub and 4/4 routing arms | `receipts/docs-git.log` |
| `python3 -B scripts/docs_check.py` (metadata-free HEAD export) | rc 0; 0 findings; same file counts; 22/22 scrub and 4/4 routing arms; inventory parity skipped because metadata is absent | `receipts/docs-no-git.log` |
| `python3 scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7` | rc 0; 0 findings; 339/339 arms | `receipts/em-dash.log` |
| `python3 scripts/check_doc_style.py` | rc 0; 22 current documents | `receipts/doc-style.log` |
| `python3 scripts/gen_toc.py --check` | rc 0; 107 contents lists; 17 pages below threshold | `receipts/toc-check.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | rc 0; 174 fragment links reproduced | `receipts/toc-anchors.log` |
| `python3 scripts/check_doc_paths.py` | rc 0; 847 cited paths resolve; 1 allowlisted | `receipts/doc-paths.log` |
| `python3 scripts/measure_test_evidence.py --check` | rc 0; evidence contract and ratchets pass | `receipts/test-evidence.log` |
| `git diff --check` | rc 0 | `receipts/diff-check.log` |
| `git diff --check HEAD^ HEAD` | rc 0; committed Round 4 delta also checked | `receipts/commit-diff-check.log` |

The named `scripts/bdd_mutants.py` was absent from the candidate and the
initially empty output directory. The receipt script supplied here copies
only the existing feature, its steps and supporting files into `/tmp`.
Each mutant changes exactly one gate expression there. It must fail exactly
the composition scenario with the expected assertion; the other four
scenarios pass. Both clean controls pass, and original source bytes are
checked unchanged. The script is an external validation artifact, not part
of the commit. No prior private material was read.

`scripts/run_gates.py` reproduces this table from the output directory with
`MILAN_SOURCE=<candidate-worktree>` and
`MILAN_GATE_ENV=<temporary-environment>` set. It records every raw return
code in `gate-results.json`; expected mutant and no-match statuses are
explicitly checked. All exported source trees are temporary and removed.

## Handoff state

`PR-BODY.md` preserves the full current PR body obtained with
`gh pr view 553 --json body`, updates the leading role to `[A318]`, refreshes
Status, distinguishes the Round-3 head, records the complete control count,
and adds Round 4. It retains `Closes #551`.
`pr-original.json` and `PR-ORIGINAL.md` retain that public source body.

The two assigned outcomes are met. Independent re-review remains required;
this handoff is evidence, not a review verdict or completion ledger.
The other suggestions remain with #495. Publication and subsequent gates
remain with the coordinator. No push, PR edit, merge, other checkout,
sub-agent or hardware action was performed. The candidate worktree is clean.

The final authorized action is to post `REVIEW-READY.md` on #551 and stop.
