[A158] REVIEW READY - isolated author evidence for manager handoff

Commit: `0d43ff25d38917e77bb5c3d2ddb6473013cea3ba`.
Base: `b17580b91deb11f3441dfc5d7f9fafe539d929b8`.
Changed: six files covering two closer decisions, I440 controls, runner wiring, directly affected guard expectations and authoritative prose. No RTL/workflow/builder/version/budget/gitlink edit. Existing Unicode-fold controls and all runtime provenance/refusal logic remain unchanged.

Validation: `python3 -B scripts/gen_toc.py --selftest` 683/683; `--check` 105 TOCs; `--verify-anchors` 144 links; `--sites` 25 single-source sites. `python3 -B scripts/check_em_dash.py --selftest` 51/51; `--base b17580b91deb11f3441dfc5d7f9fafe539d929b8` zero findings on 32 added lines. `docs_check.py` and its selftest, `check_doc_paths.py`, `check_doc_style.py`, `check_py_idiom.py` and its selftest, `check_hygiene.py --check`, `check_rtl_source_lists.py`, `git diff --check`, scope/source guards and per-page comparison all pass. Exact commands and complete stdout/exit receipts are in `commands.jsonl` and `logs/`.

Acceptance criteria: exact fence and literal type-1 rules implemented; every changed property fails behavioral mutation controls; all historical characters, CR, inner blanks, Unicode folds, valid controls and cross-name rows are measured on both base/head against GitHub gfm. Head normalized helper agreement is 205/205; 100 rows remain globally refused. Raw head has zero escapes and five explicitly bounded CR withholdings that the actual readers normalize. Exact shipped-gate page comparisons reject hidden labels and preserve legitimate cross-name labels. All 163 tracked pages retain headings and generated Contents; 105 retain provenance. No directly affected tracked parser correction was needed.

Sensitivity: 11/11 disposable-copy mutants fail I440 behavior; fence widening is masked by existing shipped refusal and therefore held by raw arms. Unicode and other type-1 mutations also fail the shipped gate controls. Exact patches/results and source hashes are published with the renderer evidence in issue comments 5771717445 and 5771717582.

Open limitations: the historical instrument could not be obtained from its public references, so this is a documented population reconstruction. #437's container limitations remain out of scope. CR normalization and the independent LF-based Git diff boundary are stated explicitly. No open author-scope implementation question remains.

Manager-owned checks not run: complete native RTL/lint/elaboration/processor/builder/Yosys/behave gates, trusted act, hosted CI, independent reviews, candidate merge validation and containment. No full milan_dp sweep. This evidence is not an independent review verdict or the full completion bar. A10 owns publication and orchestration; R225 and R226 remain assigned for later cleared-context review.

Final state: one committed author head, clean tracked files and initialized submodules; unchanged uninitialized `external`; no push/PR/review/merge/subagent action.
