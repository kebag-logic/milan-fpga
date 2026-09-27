[A353] REVIEW READY

Commit: `92c6154a17d1f1192f20a3a642e6a01b616afb67` (one local commit after `867a2e38`; not pushed).

Changed: all three [Round 4 assignment items](https://github.com/kebag-logic/milan-fpga/issues/502#issuecomment-5854288100). The materialization page marks #502's reporting window resolved and labels the old mark-trigger evidence as historical. The whole-tree sweep also corrects the release history, ownership introduction, backend/CSR comments, co-simulation description and VERSION diagnostic. Accepted name writes and actual parent phase-5 map writes raise pending; unchanged maps raise nothing; marks remain completion triggers. Refusal status and map-count diagnostics now carry their case names.

Validation, final commands all rc 0:

- `make -C tb/verilator/pp_shadow`: 591 + 591 + 591 + 295 checks, zero failures.
- `make -C tb/verilator/pp_shadow pending-mutant`: clean 295/0; the historical trigger produces the required K10/K12 failures, including REMOVE.
- `python3 scripts/docs_check.py` and `GIT_DIR=/dev/null python3 scripts/docs_check.py`: zero findings.
- `python3 scripts/check_em_dash.py --base 831f94f4`, `python3 scripts/check_doc_style.py`, `python3 scripts/gen_toc.py --check`, `python3 scripts/gen_toc.py --verify-anchors`, and `python3 scripts/check_doc_paths.py` pass.
- `git diff --check`, staged whitespace validation, and committed diff checks against `867a2e38` and `831f94f4` pass.

Acceptance: R329-3 F1/S1 and R328-3 S1 addressed. All seven search patterns and all 335 matches (264 distinct file:line hits) are individually disposed in HANDOFF.md, including accurate statements and unrelated lexical matches. No executable RTL changed; the two trigger modules are byte-identical. SystemVerilog changes are comments only. No firmware, configuration or gitlink changes. The worktree is clean.

The first default attempt stopped after the passing base leg because the temporary Python environment hid PyYAML. After correcting that environment, the complete target passed; both attempts are recorded. No failed attempt is counted as passing evidence.

HANDOFF.md, gate receipts and the full replacement PR-BODY.md are complete in the assigned output directory. The live PR body was not edited. Independent re-review and subsequent publication/hosted acceptance remain outstanding. No materialization or hardware claim is added.
