[A164] FACTUAL AUTHOR HANDOFF

PR507 / issue440, kebag-logic/milan-fpga. Sole implementation author A164.
Branch: `440-markdown-closers`.
Source: `$CANDIDATE`.

| Object | Exact identity |
|---|---|
| Base / actual post-commit merge base | `b17580b91deb11f3441dfc5d7f9fafe539d929b8` |
| Starting head | `0d43ff25d38917e77bb5c3d2ddb6473013cea3ba` |
| Starting tree | `c0e67508d3b753c21a28a243d365c4c37ed86d43` |
| Corrected head | `9d6109ccf924c03308cb8aa202ce68a435cd4f8d` |
| Corrected tree | `1d322d866da6b8d19ccd46cfd7ef5f405e9dadb4` |

One local commit: `Hold exact type-1 closer names with raw and shipped-label controls`.
Its sole parent is the starting head. One-line message, no trailers.
The branch is one commit ahead of its unchanged upstream. Nothing was pushed.

Only R226-F1 (MINOR Tests and Docs) was addressed. The correction adds 24 raw-walk controls and six shipped-label controls for `div`, `title`, and `xmp`, updates the existing TOC floor from 683 to 707, and specifies the coverage in DOC_GENERATION.md. Raw cases cover every allowed opener and both closer positions; label cases cover both positions with `pre`.

Changed paths (15 insertions, three deletions):

- `scripts/gen_toc_closer_cases.py`: independent other-name fixtures and expected hidden-label decisions.
- `scripts/gen_toc.py`: only `MIN_ARMS = 683` becomes `MIN_ARMS = 707`.
- `docs/DOC_GENERATION.md`: two coverage sentences replace the broad claim.

The production parser remains byte-identical after excluding the test-floor assignment. All other non-test/non-doc bytes, all tracked modes, all index flags, and all four gitlinks are unchanged. All 851 tracked non-gitlink files match their committed blobs and modes. Final status and staged/unstaged differences are clean. `original-integrity.json`, `precommit-integrity.json`, `final-integrity.json`, `IDENTITY.json`, and `author-change.patch` bind those facts. The precommit validated file bytes equal the committed bytes.

Validation: TOC 707/707; em-dash 57 controls; TOC check 105 lists; anchors 144; sites 25, all single source; docs_check zero findings; doc style and paths pass; staged and committed diff formatting pass. After commit, `git merge-base origin/dev HEAD` returned the exact base above; the em-dash gate reports zero findings across 34 added lines in one Markdown page. See COMMANDS.md and commands/ for exact commands, exit codes and logs.

All 683 original TOC fixture identities survive, including their fixture hashes. All 17 existing I440 label rows survive byte-for-byte with their expected counts; check_em_dash.py is wholly unchanged, retaining its other 34 controls. Totals are 707 TOC and 57 em-dash. fixture-retention.json and original/corrected population.json record the populations. Emptying the new raw population or removing one new raw case trips the 707 floor; an additional valid cross-name fixture passes 708/708. No em-dash floor was added.

The original R15/R16/X04 survivors and hidden-label escapes were independently reproduced using the public R226 instruments with explicit case/mutant selection. At the corrected bytes each exact widening fails eight named raw arms and two named label rows (four diagnostic lines). Real E14/E15 CLI runs now stop at the failing permanent controls, exit 2, before any page judgment. The unmutated CLI still rejects E14/E15 and xmp while accepting the E03 cross-name label. RESPONSE.md and OUTCOMES.json explain the receipts, including the difference between findings exit 1 and control refusal exit 2.

Public TAKEN: https://github.com/kebag-logic/milan-fpga/issues/440#issuecomment-5773071396 . Public input snapshots are retained verbatim as attributed source documents, not A164 review statements.

Manager next steps: publish the review-ready/archive evidence, then own push and full-native/act/hosted validation scheduling. PR507 remains draft at the remote old head. R225/R226 must independently reapply changed lenses and explicitly accept any coverage they bank from unchanged artifacts. This handoff contains no author review verdict or completion ledger and does not close R226-F1 on a reviewer's behalf.

No optional suggestions, production/parser/RTL changes, #437 container changes, unrelated cleanup, agents, other-lane edits, project/PR metadata mutations, push, merge, hardware, Docker/act, privilege changes or dependency installation were performed. The old ready replica remains interrupted evidence, not a pass. Full parent gates were intentionally left to the manager under this assignment.
