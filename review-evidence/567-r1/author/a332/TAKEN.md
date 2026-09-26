[A332] TAKEN
Branch: `567-pp-pin-0922e434`; starting head `c9484ac8e86cb33d1120471530f9e1762bd4af1f`.
Executor: [A332]. Independent reviewers remain [R326] internal and [R327] external.
Authoritative references: #567 and the [Round 3 assignment](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845274184), the [Round 2 decision](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5845149786), and `CONTRIBUTING.md`.
Interpreted scope: update only the assigned passages in `CHANGELOG.md` and `docs/reference/SUBMODULES.md` to state that the repository recorder added rows for `0922e434`, whose digests equal the `990f9652` rows. The issue is already In progress and both matching ledger rows are present.
Validation plan: `python3 -B scripts/docs_check.py` in both CI modes; `check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`; `check_doc_style.py`; `gen_toc.py --check`; `gen_toc.py --verify-anchors`; `check_doc_paths.py`; `git diff --check`. Every gate runs in the foreground without a pipeline.
Blockers: none.
