[A292]

Round 4 is committed locally on `501-outmap-record`.
Head: `efcabc379b1e0be1366bfc05bdcc05a759b55616`.
Parent: `afdd28b701e7f5849317e27ce845c31d1c87f2a6`.
Source base: `573f0052a0e4412e81f0845438fcec2086ce5d55`.
Commit: `docs: remove donor capture-hold measurement condition`.

The [assignment](https://github.com/kebag-logic/milan-fpga/issues/501#issuecomment-5824399821)
authorizes deletion of the sentence identified by
[R312-3 F1](https://github.com/kebag-logic/milan-fpga/pull/557#issuecomment-5824394329) and
[R313-3 F1](https://github.com/kebag-logic/milan-fpga/pull/557#issuecomment-5824395155).
Only `docs/design/SAVED_STATE_MATERIALIZATION.md` changes: zero additions, two deletions.
The sentence formerly at lines 1648-1649 is deleted exactly.
Every other tracked byte remains unchanged, including all protected capacity-adoption lines.
Stage-3 release does not depend on capture-hold measurement.
Issue #559 continues to own that measurement and its resolution.
[Exact scope evidence](receipts/exact-scope.log) and [patch](receipts/round4.patch).

All assigned gates returned zero on this exact head:

| Command | rc | Receipt |
|---|---|---|
| `python3 scripts/check_nvm_record_space.py` | 0 | [record space](receipts/record-space.log) |
| `python3 scripts/check_nvm_record_space.py --self-test` | 0 | [self-test](receipts/record-space-self-test.log) |
| `python3 scripts/docs_check.py` with repository metadata | 0 | [docs](receipts/docs-check.log) |
| `python3 scripts/docs_check.py` in an exact-head export without metadata | 0 | [docs without metadata](receipts/docs-check-no-git.log) |
| `python3 scripts/check_em_dash.py --base 573f0052a0e4412e81f0845438fcec2086ce5d55` | 0 | [em dash](receipts/em-dash.log) |
| `python3 scripts/check_doc_style.py` | 0 | [style](receipts/doc-style.log) |
| `python3 scripts/gen_toc.py --check` | 0 | [contents](receipts/toc.log) |
| `python3 scripts/check_doc_paths.py` | 0 | [paths](receipts/doc-paths.log) |
| `git diff --check` | 0 | [worktree whitespace](receipts/diff-check.log) |
| `git diff --check afdd28b701e7f5849317e27ce845c31d1c87f2a6 HEAD` | 0 | [delta whitespace](receipts/diff-check-delta.log) |
| `git diff --check 573f0052a0e4412e81f0845438fcec2086ce5d55 HEAD` | 0 | [full whitespace](receipts/diff-check-full.log) |

The record-space gate reports zero findings across five configurations.
Its self-test passes all 18 named controls.
Both documentation modes inspect 165 pages and 859 text files.
The metadata-free mode omits inventory parity as designed.
The pinned Markdown dependencies were installed with required hashes in temporary scratch.
[Dependency versions](receipts/markdown-dependencies.txt).
All commands ran in the foreground, with no output pipelines.
[Exact commands and exit codes](receipts/gate-results.json).

Both reviewer scripts ran unchanged:

- `python3 <R312-3>/r3_text_check.py <repo-root> <R312-3>/capture_copy_probe.log <R312-3>/hold_margin.log`: rc 0; [receipt](receipts/r3-text-check.log).
- `bash <R313-3>/residual_search.sh <repo-root>`: rc 0; [receipt](receipts/residual-search.log).

`r3_text_check.py` passes 23 required and 14 forbidden-text checks.
It reports no capture-hold ownership residue.
Its one generic `RESIDUE` line is `SAVED_STATE_FASTCONNECT.md:457`:
“The later output-capacity adoption is a separate donor obligation.”
That capacity-only line is explicitly protected by the assignment.
The residual search confirms #559 ownership, no withdrawn copy premise,
and only the unchanged capacity obligations for processor #61/#83.
A search across all tracked Markdown confirms the same scope:
[search](receipts/all-tracked-pages-search.log), [result check](receipts/reviewer-result-check.log).

The scripts came from `501-review-evidence`, fetched into a temporary bare repository:

| Script | Archive | SHA-256 |
|---|---|---|
| `review-evidence/501-r1/reviews/R312-3/scripts/r3_text_check.py` | `68d31b03bb1b93d9b307821bf23605d5f7ae1399` | `94393f710e5a9432a82a4c795106a7ae3b4cc7ca35c550475acd687239c13101` |
| `review-evidence/501-r1/reviews/R313-3/scripts/residual_search.sh` | `6de818df4569360dc76ba3b37d3005a6e396bc9a` | `afd7fe00e5677c62971c285db40d9f7ccca0967d72a240216907d3d198c2de3f` |

The text check used the unchanged `capture_copy_probe.log` and `hold_margin.log`
from the first archive's `review-evidence/501-r1/reviews/R312-3/receipts/` directory.
These are archived numerical inputs; capture and hold probes were not rerun in Round 4.
[Script identities](receipts/reviewer-script-identity.tsv), [input identities](receipts/reviewer-input-identity.tsv).

[PR-BODY.md](PR-BODY.md) contains the complete current PR body updated for Round 4,
including `Closes #501`, current executor and head, and earlier validation limits.
It is prepared for publication by the manager.
The commit is local only. No push, PR edit, merge, additional checkout,
sub-agent or hardware activity occurred.
All temporary evidence, dependencies and the metadata-free export were deleted after validation.
No toolchain, dependency environment or tree export is stored in this output directory.

R312-3 F1 and R313-3 F1 are addressed; independent delta reviews remain pending.
Reviewers [R312] and [R313] own their verdicts and lens ledger.
The manager retains publication, hosted checks, candidate validation and merge duties.
The final public action is the `[A292] REVIEW READY` comment on issue #501.
