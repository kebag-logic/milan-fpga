[A347] REVIEW READY

Commit: `4f746408a15f494c4b30bdc9add6d7295309dff9`
Branch: `573-builder-model-refusals`, from `e0920d77162284d8da52ffaf13a973e451e44f90`.
Four local commits, ordered #573, #574, #575, #576. Nothing pushed; no PR created or edited.

Changed: parent configuration refusals for reserved literal/pinned model IDs, every listener buffer floor, final stream-format count/family and both Milan CRF words, and INTERNAL availability for every output. The existing declaration entry runs the new controls. The ownership matrix and parameter guide state the enforced boundaries.

Validation, all exit status 0:
- Full `sw/builder/test_builder.py --require-rv32`: 763.10 s.
- Full `sw/builder/test_builder.py` main entry with the three RV32 candidates hidden through the existing compiler audit: 558.09 s. All other subprocesses ran normally.
- `sw/builder/test_declarations.py`; `scripts/audit_pp_descriptors.py --output <receipt>`; `avdecc/gen_aem_store.py --self-test`.
- `scripts/lint_rtl.py --check`; `scripts/check_py_idiom.py`; `scripts/measure_naming.py --check`.
- `scripts/docs_check.py` in Git and `GIT_DIR=/dev/null` modes; `scripts/check_em_dash.py --base e0920d77`; `scripts/check_doc_style.py`; `scripts/gen_toc.py --check` and `--verify-anchors`; `scripts/check_doc_paths.py`; `git diff --check e0920d77 HEAD`.

Acceptance criteria: met for F1-F4. All five tracked configurations remain accepted; 85/85 builder/store/image artifacts retain their before/after SHA-256 and size. All 14 removed-check mutants were killed at this exact head, followed by a passing unmutated declaration run. No STOP condition occurred. Input-only clock loading remains supported; full product YAML still requires both AAF directions.

Evidence limits: the full builder records the unavailable physical calibration report in both modes, and its expected compiler-instrument stand-down in absent mode. The compiler-present instruments ran. The no-Git docs gate records its expected inventory-parity skip.

`HANDOFF.md`, `PR-BODY.md`, exact commands, logs, mutations and both hash inventories are in the assigned delivery directory. The worktree and initialized submodules are clean. Independent review remains with [R340] and [R341]. Model evolution remains with #495; no other ownership-matrix follow-up was expanded.

Open risks/questions within the assigned scope: none.
