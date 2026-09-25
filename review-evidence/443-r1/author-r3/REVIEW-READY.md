[A310] REVIEW READY

Commit: `b3458db0db5a7c8b15582d80b492620f05f62e70` (local merge head; publication remains with the manager).
Parents: `5beebb7c7edd908d08be34e52286c9eee441f5b3`, `864b36f5e9450ef64f75ca3f0d68c44330e447d7`.

Changed: merged the assigned dev tip. Both `CHANGELOG.md` conflict hunks retain both Unreleased sections and Contents entries verbatim. No other manual repository edits. Submodules match the merged gitlinks; the worktree is clean.

Validation: all 17 requested gates have final exit 0:

- `make -C tb/verilator/csr`
- `make -C tb/verilator/milan_dp` (full default regression, including the merged harnesses and `aclk`)
- `make -C tb/verilator/milan_dp render-csr-controls`
- `make -C tb/verilator/milan_dp_render`
- `python3 scripts/docs_check.py`
- `env GIT_DIR=/dev/null python3 scripts/docs_check.py`
- `python3 scripts/check_em_dash.py --base 864b36f5e9450ef64f75ca3f0d68c44330e447d7`
- `python3 scripts/check_doc_style.py`
- `python3 scripts/gen_toc.py --check`
- `python3 scripts/gen_toc.py --verify-anchors`
- `python3 scripts/check_doc_paths.py`
- `python3 scripts/xvlog_gate.py --check`
- `python3 scripts/check_sv_idiom.py`
- `python3 scripts/check_cpp_idiom.py`
- `python3 scripts/check_py_idiom.py`
- `python3 scripts/measure_test_evidence.py --check`
- `git diff --check`

Three Markdown checks initially returned 2 for a missing locked dependency. After installing `tools/markdown/requirements.txt` in an isolated temporary environment outside the worktree and output directory, all three returned 0. Both attempts are recorded. No source or test fix was made. The parser gate ran and matched the unchanged baseline: zero first-party findings, four pinned-processor findings.

Evidence: CSR 380/380/115/38/380; full `aclk` 190; render CSR clean 64 and absent-stage 33, with both named mutants caught; render shipping 152, two-listener 65, and five existing controls. All campaigns returned 0.

Acceptance: merge-dev assignment met locally. `HANDOFF.md`, `PR-BODY.md` and complete logs are prepared for the manager. No push or PR edit was performed.

Open review: one independent delta review of this merge commit, as assigned; the other positive review stands on the ancestor. No new source or test failure remains.
