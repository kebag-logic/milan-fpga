[A279] REVIEW READY
Commit: e41703b2948ef53e5cb0dd01a1e13c5632637615
Branch: 548-ctlr-diag-zero (local, not pushed)

Changed: REGISTER_MAP row, paragraph and group gloss now identify CTLR_DIAG (0x6F4) as STRUCTURAL ZERO and name the processor monitor. Corrected the CSR/datapath comments and #117 evidence interpretation. Added one AXI-Lite zero check after the existing timed controller probes, retry and eviction. No functional RTL change; frozen history and sw/builder/test_builder.py untouched.

Test evidence: obj_notify passes 147 checks with 0 failures. A temporary mutant driving aecp_ctlr_diag with 32'h01001001 exits 1 with exactly the new zero assertion failing (147 checks, 1 failure). The mutation campaign returns 0. No notification-leg mutant runner exists; the same existing build recipe was used for both runs and preserved in the handoff packet.

Validation: all assigned positive gates return 0:

- `make -C tb/verilator/milan_dp` (1307.54 s, including existing render mutations; VERILATOR_JOBS=8).
- `python3 scripts/docs_check.py` and `env GIT_DIR=/dev/null python3 scripts/docs_check.py` (Git and filesystem inventory modes).
- `python3 scripts/check_em_dash.py --base 573f0052a0e4412e81f0845438fcec2086ce5d55`.
- `python3 scripts/check_doc_style.py`; `python3 scripts/gen_toc.py --check`; `python3 scripts/check_doc_paths.py`.
- `python3 docs/traceability/gen_module_matrix.py --check`; `python3 scripts/xvlog_gate.py --check` (existing four processor findings match ratchet; zero first-party findings).
- `python3 scripts/check_rtl_source_lists.py`; `python3 scripts/check_cpp_idiom.py`; `python3 scripts/check_py_idiom.py`.
- `git diff --check` and `git diff --check 573f0052a0e4412e81f0845438fcec2086ce5d55 HEAD`.

Acceptance criteria: the recorded decision and assignment items 1-6 are met. HANDOFF.md, PR-BODY.md, the mutation reproducer and full logs are in the assigned output directory. Worktree clean. Independent reviews [R308] and [R309] pending; this is author evidence, not a review verdict.
Open technical risks/questions from this change: none.
