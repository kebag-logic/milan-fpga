[A339] REVIEW READY
Commit: 3a1477c528bdf71b7cecadf86383b7579c9197d6
Branch: 231-pp-shadow-baseline (local, unpushed)
Changed: tests only in syn/ooc/pp_baseline.py and syn/ooc/pp_baseline_mutants.py. Production functions and constants are unchanged.
Acceptance criteria: round-three items 1-2 met. Synthetic exports cover ambiguous/missing bindings and packages, duplicated geometry declarations, and generated/parameter ROM geometry mismatches. Forty inventory refusals pass. All 28 maintained mutants are killed. The unchanged R332-3 scripts/extra_mutants.py kills 15/15; the unchanged R333-2 probe_selftest/mutate2.py kills 17/17. All three pristine controls pass.
Validation: all rc 0 at the stated head:
- python3 syn/ooc/pp_baseline.py --selftest
- python3 syn/ooc/pp_baseline_mutants.py
- Both unchanged reviewer scripts, with every verdict checked
- python3 -B scripts/docs_check.py, both Git and filesystem inventory modes (zero findings)
- python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a
- python3 scripts/check_doc_style.py
- python3 scripts/gen_toc.py --check
- python3 scripts/gen_toc.py --verify-anchors
- python3 scripts/check_doc_paths.py
- python3 scripts/check_py_idiom.py
- python3 scripts/measure_test_evidence.py --check
- git diff --check, plus the committed round-three delta
Evidence: HANDOFF.md contains file:line changes, every mutant verdict, script hashes and the complete gate table; PR-BODY.md preserves the full current body with a Round 3 section and Closes #231. Both are in the assigned output packet. Public probe source: 231-review-evidence at 1202ce2f09f92729d4cc1fda4d05284a3d8a5cc0; temporary evidence has been removed.
Open risks/questions: none in the assigned tests-only scope. Independent re-review and publication remain pending.
