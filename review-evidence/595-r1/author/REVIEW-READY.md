[A417] REVIEW READY
Commit: 44d3ae3b15a0d058abb837c655ad24bd9b64c6e8 (local, unpushed)
Branch: 595-yaml-int-refusal

Changed: string-only station MAC and both `_declared_uint` callers (`entity.vendor_oui`, `entity.entity_capabilities`); explicit nulls receive the quote instruction. Non-list AAF `formats` receive a field-named list-type refusal. Quoted colon/dash MAC values and omitted/empty-list defaults retain their meaning. Tests and both builder guides are updated.

Validation at this committed head, all rc 0:
- `python3 sw/builder/test_builder.py --require-rv32 --require-elaboration`
- `python3 sw/builder/test_declarations.py`
- `python3 sw/builder/test_firmware_compiler.py --selftest` and `--absent --audit <scratch>/compiler-absent-audit.jsonl`
- Pinned `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`: `scripts/docs_check.py` with Git and `GIT_DIR=/dev/null`; `scripts/check_em_dash.py --base 1fa2357fcb9b83ad7d6cbeab0c7cc0eb957cdd3a`; `scripts/check_doc_style.py` and its `--selftest`; `scripts/gen_toc.py --selftest`, `--verify-anchors`, `--check`; `scripts/check_doc_paths.py`.
- Python idiom, naming, worktree/branch whitespace checks; focused mutation and artifact comparisons.

Acceptance 1-5 met: 233 loader cases pin messages and quoted values; 3/3 historical mutants are killed by named assertions with restored controls passing. All five configuration files and 70 generated artifacts match baseline sizes, SHA256 and raw bytes. The worktree is clean; the processor source and gitlink are unchanged.

Evidence: HANDOFF.md, PR-BODY.md, case/mutant tables, before/after hash tables, and 19 gate receipts are prepared in the assigned output directory. The full bank reports only the unavailable gate-11 utilization calibration report; absent-compiler controls explicitly record their intended stand-downs. No implementation blocker remains. Independent reviewers [R388] and [R389] remain assigned; #577 / PR #612 integration remains with the maintainer. No push or PR action performed. Stopping here.
