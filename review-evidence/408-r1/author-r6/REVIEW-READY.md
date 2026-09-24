[A276] REVIEW READY

Commit: `062e89ad098806ae5def8341fcb8c2815583ca00` (local; manager publication pending).
Parent: `991d59653ff82ccf73ef4df9477de1df8c8c5964`.

Changed: R273-7 F1's gate-call comment now states position-independent allowlist refusal, agreement measured at the closure table's 23 positions, and the two lexer corpora as the bound elsewhere. Also addressed R273-7 S1 and R272-6 S1-S3: null-directive cost, one `/*/` corpus spelling, directive-line boundary wording, and finding references scoped to their reviewed heads. Only `sw/builder/test_builder.py` and `docs/integration/BAREMETAL_FIRMWARE.md` changed.

Validation: every required command returned 0 at this head, in the foreground without pipes.

- Full `python3 sw/builder/test_builder.py` with `--require-rv32`, using the assignment's verified-SDK selector mapping: 280/280 mutations, 29/29 firmware edits and 4/4 Makefile edits accepted. Final verdict: `ALL GATES PASS EXCEPT 1 NOT RUN` (existing gate-11 report absence).
- Full builder with all cross candidates hidden: 222/222 mutations, 29/29 + 4/4 accepted edits, zero firmware compilations. Final verdict: `ALL GATES PASS EXCEPT 2 NOT RUN` (missing compiler instruments and gate 11).
- Both modes: 1846/1846 lexer spellings (79 fixed, 1767 generated) and 6440/6440 closure cells. Re-measured with the SDK; recorded expectations checked without it.
- `python3 -B scripts/docs_check.py` in both CI modes: repository metadata present, and exact-head tracked-source export without it; zero findings in each.
- `python3 scripts/check_baremetal_only.py --check`; `python3 scripts/check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9`; `python3 scripts/check_doc_style.py`; `python3 scripts/gen_toc.py --check`; `python3 scripts/check_doc_paths.py`; `python3 scripts/check_py_idiom.py`; `git diff --check`; and the committed correction's `git diff --check`: all 0.

Regression control: the added `/*/` spelling agrees with the pinned compiler, keeping `a` and `z`. Moving the block-comment closer search from `i + 2` to `i + 1` in memory makes gate 1b fail on that row in both modes, keeping `a`, `b`, `z`. Removing the added row makes the syntax tree identical to the parent; there is no other executable change.

Acceptance criteria: the scoped round-six assignment is met; acceptance 4 remains 280/280 SDK and 222/222 absent with full-suite exit 0 in both modes. Existing mutation and accepted-edit entries are unchanged.

Evidence: `HANDOFF.md`, full updated `PR-BODY.md`, command receipts, logs, scope proof, correction patch and manifest are prepared in the assigned output directory. The commit subject is one line with no body or trailers; the worktree is clean.

Open risks/questions: no new ones. Independent re-review, publication, final-head CI acceptance and candidate-merge validation remain with the manager. No push, PR edit, merge or hardware operation was performed.
