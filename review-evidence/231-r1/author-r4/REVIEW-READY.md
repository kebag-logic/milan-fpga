[A341] REVIEW READY
Commit: `ae729bbfd90934f4d56d3b02f1ffc652496b414d`
Branch: `231-pp-shadow-baseline`

Changed: text-only correction in `docs/findings/PP_SHADOW_BASELINE.md` and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`. The page describes refusal coverage by category; both documents refer to the maintained enforcement-removal mutants without a fixed count. This addresses the shared MINOR Docs F1 from R332-4 and R333-3 under assignment 5847557806.

Validation at this head, all rc 0:
- `python3 syn/ooc/pp_baseline.py --selftest`: 40 inventory refusals and restored control pass; remaining self-test arms pass.
- `python3 syn/ooc/pp_baseline_mutants.py`: pristine control rc 0; all 28 maintained mutants rc 1.
- `python3 -B scripts/docs_check.py` and `env GIT_DIR=/dev/null python3 -B scripts/docs_check.py`: identical 894-text-file inventories, zero findings; filesystem mode skips only Git inventory parity.
- `python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`: zero findings, 339/339 control arms.
- `python3 scripts/check_doc_style.py`; `python3 scripts/gen_toc.py --check`; `python3 scripts/gen_toc.py --verify-anchors`; `python3 scripts/check_doc_paths.py`: all pass.
- `git diff --check` and `git diff --check 3a1477c528bdf71b7cecadf86383b7579c9197d6 HEAD`: clean.

Acceptance criteria: the round-four text-only assignment is met. No scripts or measurements changed; Python idiom is inapplicable. All commands ran in the foreground without pipelines. The pinned renderer was installed in the isolated output directory.

Open risks/questions: none for this correction. Independent re-review and final-head acceptance remain pending. The commit is local and unpushed, and the live PR was not edited. HANDOFF.md, the complete updated PR-BODY.md and gate receipts are prepared in the assigned output directory.

