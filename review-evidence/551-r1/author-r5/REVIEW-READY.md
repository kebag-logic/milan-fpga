[A318] REVIEW READY

Commit: `6e4a3b420e055ef7529ceb16bb2ab5be93c34487` (local, not pushed).
Branch: `551-licence-real-grant`; PR #553, round 4.

Changed:
- `tests/features/milan_streaming_licence.feature:92`: current-TSpec grant guarantee from processor #112, adopted through #508; steps and assertions unchanged (R296-2 N1 = R297-2 F1).
- `tb/verilator/milan_dp/README.md:468`: complete pre-#112 control count, 28 `[I]` plus 6 `[J]`, 34 total (R296-2 S2).

Validation at this head:
- `cd tests && behave --no-capture -f plain`: rc 0; 344 scenarios, 1739 steps, no failures or skips.
- `python3 scripts/bdd_mutants.py`: rc 0; all four mutants caught; clean feature 5/5 before and after. The named runner was absent, so a reproducible receipt script was supplied in the handoff; mutations ran only in temporary source copies.
- `grep -rnE "Residual|pending fix|previous slope" tests/`: no output, expected no-match rc 1; absence assertion passes.
- `python3 -B scripts/docs_check.py`: rc 0 in both CI inventory modes; zero findings. The metadata-free mode skips only inventory parity, as expected.
- `python3 scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7`: rc 0.
- `python3 scripts/check_doc_style.py`, `python3 scripts/gen_toc.py --check`, `python3 scripts/gen_toc.py --verify-anchors`, `python3 scripts/check_doc_paths.py`, `python3 scripts/measure_test_evidence.py --check`, `git diff --check`, and `git diff --check HEAD^ HEAD`: all rc 0.

Acceptance: assigned items 1 and 2 met; only the two text files changed. Worktree clean. `HANDOFF.md`, the full updated `PR-BODY.md`, scripts and receipts are prepared in the assigned output directory.

Open risks/questions: none for the assigned text corrections. Independent re-review and publication remain pending. No push, PR edit, merge or hardware action performed. Other suggestions remain with #495.
