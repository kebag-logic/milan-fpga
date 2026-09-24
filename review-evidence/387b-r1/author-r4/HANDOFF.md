[A283]

Round 4 is committed locally at `00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b` on `387-media-rebase`.
Starting head: `0f003fab3303858ba4db955ad3c0512e67a8018b`.
Commit subject: `docs: align remaining milan_dp deadlines with decision 5820240308`.
The commit has one subject line, no body, and no trailers.

The [assignment](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5821889812) addresses F1 from the [internal review](https://github.com/kebag-logic/milan-fpga/pull/555#issuecomment-5821852091) and [external review](https://github.com/kebag-logic/milan-fpga/pull/555#issuecomment-5821883985).

Each assigned statement now gives the current `milan_dp` deadline as 3600 s and cites [decision 5820240308](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5820240308):

| Changed location | Correction |
|---|---|
| `docs/testing/TESTING.md:166` | 3600 seconds, the decision, and recorded hosted samples; the workflow-policy link remains. |
| `docs/testing/RUNNING_TESTS.md:79` | 3600 seconds under the decision. |
| `tb/verilator/milan_dp_gptp/README.md:31` | 3600-second budget under the decision. |
| `tb/verilator/milan_dp/render_mutants.py:37` | 3600 s under the decision in the module docstring. |

The [complete delta](round-4.patch) contains exactly those four files, with seven insertions and five deletions.
The [scope proof](receipts/scope-proof.txt) compares every changed file with the starting version and permits only the assigned replacement.
The executable syntax tree is unchanged after excluding the module docstring.
Both `docs/testing/CI_WORKFLOWS.md` and `scripts/measure_test_evidence_selftest.py` are byte-identical to the starting head.
The only remaining standalone `2700` references under `docs`, `scripts`, and `tb` are the history at `CI_WORKFLOWS.md:167,185` and the planted mutation at `measure_test_evidence_selftest.py:294`.
The worktree is clean.

All requested gates ran in the foreground without pipelines, at the committed head, with a 1800-second timeout per command.
The locked documentation dependencies and the temporary tree export were kept outside this packet.
The no-metadata run used an archive of the committed head; both documentation modes examined 165 Markdown files and 859 text files with zero findings.
The no-metadata mode reported its expected inventory-parity skip because that check requires repository metadata.

| Command | Exit | Receipt |
|---|---|---|
| `python3 scripts/docs_check.py` | 0 | [docs-check](receipts/docs-check.log) |
| `python3 scripts/docs_check.py (without Git metadata)` | 0 | [docs-check-no-git](receipts/docs-check-no-git.log) |
| `python3 scripts/check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d` | 0 | [em-dash](receipts/em-dash.log) |
| `python3 scripts/check_doc_style.py` | 0 | [doc-style](receipts/doc-style.log) |
| `python3 scripts/gen_toc.py --check` | 0 | [toc](receipts/toc.log) |
| `python3 scripts/check_doc_paths.py` | 0 | [doc-paths](receipts/doc-paths.log) |
| `python3 scripts/check_py_idiom.py` | 0 | [py-idiom](receipts/py-idiom.log) |
| `python3 -m py_compile tb/verilator/milan_dp/render_mutants.py` | 0 | [py-compile](receipts/py-compile.log) |
| `git diff --check` | 0 | [diff-check](receipts/diff-check.log) |
| `git diff --check 0f003fab3303858ba4db955ad3c0512e67a8018b 00db64eb1e6e0c9bdb9f35ec5e37ebe6e00d550b` | 0 | [delta-diff-check](receipts/delta-diff-check.log) |

The [structured gate results](gate-results.json) bind every receipt to the full head.
The [prepared PR body](PR-BODY.md) is the full current public body from `gh pr view 555 --json body`, updated for this author and round, with earlier evidence explicitly retained as Round 3 evidence.
It preserves `Relates to #387` and the acceptance-4 note.

The commit remains local. No push, PR edit, merge, other checkout, hardware access, or delegated work was performed.
Independent delta reviews by the assigned internal and external reviewers remain pending.
Publication, required hosted validation, and candidate validation remain manager-owned.
Acceptance 4, the two-board measurement under #117, remains open.
