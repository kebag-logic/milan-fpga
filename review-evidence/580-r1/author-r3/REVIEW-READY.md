[A372] REVIEW READY

Merge head: `01e18f6c4d01a545e8d927ac119187c9514dc40c`.
Tree: `17de168ce12a5af81ba8a0f9d795290e071e7948`.
Parents, in order: `d02db63c367daf9adc7d709840bd81077e781d80`, `2a2a7bb655e528edc3087c88033cd3a47546feb4`.
Subject: `Merge dev into 580-pp-pin-16be6768` (one line, no body or trailers).

Changed: resolved only the two assigned `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md` hunks. The header keeps dev's original-measurements and F1-F4 enforcement facts plus the lane's historical audit-pin distinction. F1-F4 are verbatim dev; F5-F8 retain the lane text, including processor #122 and parent #584's F5 disposition. Every other tree entry equals the appropriate parent. Processor gitlink and checkout remain `16be6768f710e79450aace277abacd6c2c3336e5`.

Validation: all 40 gate invocations returned rc 0 at this merge head, in the foreground, without pipelines, from the physical worktree. `check_nvm_capture.py` passed without remeasurement; neither stop condition occurred. The normal OOC path checked the ROM ledger without rewriting it. Builder declarations passed the F1-F4 controls and binding mutants. All 33 documentation checks and four whitespace checks passed.

<details>
<summary>Exact gate commands; every rc is 0</summary>

`DOC_PYTHON` names the existing interpreter with the repository-locked Markdown and HDL parser dependencies. Each command ran with a 3600-second timeout.

| Command | rc |
|---|---:|
| `python3 scripts/check_nvm_capture.py` | 0 |
| `syn/yosys/ooc.sh KL_chan_map_render` | 0 |
| `python3 sw/builder/test_declarations.py` | 0 |
| `python3 scripts/docs_check.py` | 0 |
| `python3 scripts/docs_check.py --selftest` | 0 |
| `python3 scripts/check_doc_style.py` | 0 |
| `python3 scripts/check_doc_style.py --selftest` | 0 |
| `python3 scripts/check_gptp_docs.py` | 0 |
| `python3 scripts/check_gptp_docs.py --selftest` | 0 |
| `python3 scripts/check_solution_docs.py` | 0 |
| `python3 scripts/check_solution_docs.py --selftest` | 0 |
| `python3 scripts/check_submodule_docs.py` | 0 |
| `python3 scripts/check_submodule_docs.py --selftest` | 0 |
| `python3 scripts/check_diagram_pngs.py` | 0 |
| `python3 scripts/check_diagram_pngs.py --selftest` | 0 |
| `python3 scripts/check_archive.py` | 0 |
| `python3 scripts/check_archive.py --selftest` | 0 |
| `$DOC_PYTHON scripts/check_em_dash.py --base 2a2a7bb655e528edc3087c88033cd3a47546feb4` | 0 |
| `$DOC_PYTHON scripts/check_em_dash.py --selftest` | 0 |
| `python3 scripts/check_doc_paths.py` | 0 |
| `python3 scripts/check_feature_status.py` | 0 |
| `python3 scripts/check_feature_status.py --self-test` | 0 |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 |
| `$DOC_PYTHON scripts/gen_hdl_reference.py --selftest` | 0 |
| `python3 scripts/check_baremetal_only.py --check` | 0 |
| `python3 scripts/check_rtl_source_lists.py` | 0 |
| `python3 docs/diagrams/timesync_chain.gen.py --check` | 0 |
| `python3 docs/diagrams/timesync_chain.gen.py --selftest` | 0 |
| `python3 docs/DOC_MAP.gen.py --check` | 0 |
| `python3 docs/DOC_MAP.gen.py --selftest` | 0 |
| `python3 docs/diagrams/submodule_boundaries.gen.py --check` | 0 |
| `python3 docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 |
| `$DOC_PYTHON scripts/gen_toc.py --selftest` | 0 |
| `$DOC_PYTHON scripts/gen_toc.py --verify-anchors` | 0 |
| `$DOC_PYTHON scripts/gen_toc.py --check` | 0 |
| `python3 scripts/check_py_idiom.py` | 0 |
| `git diff --check 2a2a7bb655e528edc3087c88033cd3a47546feb4 HEAD` | 0 |
| `git diff --check d02db63c367daf9adc7d709840bd81077e781d80 HEAD` | 0 |
| `git diff --check` | 0 |
| `git diff --cached --check` | 0 |

</details>

Reported unchanged per the assignment: `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:186` names a 47-entry YAML probe, while `scripts/audit_pp_descriptors.py:263-264` constructs 48 entries. Both texts already exist on dev `2a2a7bb6`; the merge did not create the mismatch.

Acceptance: the assigned local merge, conflict resolution, gates and handoff artifacts are complete. `HANDOFF.md` contains verbatim before/after hunks, head/tree, gate table and evidence receipts; `PR-BODY.md` preserves its original labels and appends the short Merge with dev section. Both are in the assigned `580-a372` output directory. The worktree is clean. No push or PR edit was performed; this head awaits independent review and authorized publication.
