[A341] TAKEN
Branch: `231-pp-shadow-baseline`
Starting head: `3a1477c528bdf71b7cecadf86383b7579c9197d6`
Executor: [A341]. Independent reviewers: [R332] and [R333].
Authoritative references: [round-four assignment](https://github.com/kebag-logic/milan-fpga/issues/231#issuecomment-5847557806), [R332-4 F1](https://github.com/kebag-logic/milan-fpga/pull/572#issuecomment-5847547395), [R333-3 F1](https://github.com/kebag-logic/milan-fpga/pull/572#issuecomment-5847555580), REQUIREMENTS.md REQ-VER-04 and CONTRIBUTING.md.
Interpreted scope: replace the stale refusal and mutant counts in the baseline page and recipe with coverage descriptions. Text only; the existing implementation lane continues.
Validation plan: `python3 syn/ooc/pp_baseline.py --selftest`; `python3 syn/ooc/pp_baseline_mutants.py`; `python3 -B scripts/docs_check.py` in Git and filesystem modes; `python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`; `python3 scripts/check_doc_style.py`; `python3 scripts/gen_toc.py --check`; `python3 scripts/gen_toc.py --verify-anchors`; `python3 scripts/check_doc_paths.py`; `git diff --check`.
Blockers: none.
