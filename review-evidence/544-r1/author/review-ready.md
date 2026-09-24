[A286] REVIEW READY
Commit: `b068763c849a18096b0f46cf9b18e0f904e4d708`
Branch: `544-macro-sample`, based on `ffcbd33de70278ae34b533dcbadde0b36c8cba13`; clean, committed locally, not pushed.

Changed: `sw/builder/test_builder.py` protects the preprocessed identity sample between its read and mismatch guard, refusing assignment, compound assignment, increment/decrement, address-taking and mem*/str* destinations by the named single-store rule. Without the compiler, the named replacement rule refuses literal sample references and direct substitutions into used macro parameters. Both modes have cost-table rows in `docs/integration/BAREMETAL_FIRMWARE.md`.

Validation (all rc 0):
- `python3 sw/builder/test_builder.py --require-rv32`, with the verified pinned SDK mapped through the assigned absolute selector: 304/304 mutations refused, 38/38 firmware cases and 4/4 Makefile cases accepted, 46/46 RTL variants elaborated.
- `python3 sw/builder/test_builder.py`, with every cross candidate hidden: 249/249 mutations refused, 35/35 firmware cases and 4/4 Makefile cases accepted, 46/46 RTL variants elaborated; zero gate 1b firmware compiler invocations.
- `python3 -B scripts/docs_check.py` in both Git and filesystem-inventory modes. The latter uses an absent `GIT_DIR`, preserving worktree metadata.
- `python3 scripts/check_baremetal_only.py --check`
- `python3 scripts/check_em_dash.py --base ffcbd33de70278ae34b533dcbadde0b36c8cba13`
- `python3 scripts/check_doc_style.py`; `python3 scripts/gen_toc.py --check`; `python3 scripts/check_doc_paths.py`; `python3 scripts/check_py_idiom.py`
- `git diff --check` and `git diff --check ffcbd33de70278ae34b533dcbadde0b36c8cba13 HEAD`

Acceptance: both exact published hostile macro spellings are refused in both modes on their named rules; removing only the corresponding new check lets them pass through the whole remaining contract. All 15 original table/update/grader statements remain unchanged and ordered, and their verdicts remain green. The 280/280 and 222/222 floors are exceeded. The used-parameter interpretation and its conservative cost are recorded in comment 5822819158.

Open limits: R273-S3 (verifier `#else` deleted) remains ACCEPTED in both modes, at base and head; it was not fixed. The fallback checks local definitions and direct calls without general macro expansion. The existing gate 11 calibration-report arm declares NOT RUN in both full runs; compiler absence additionally declares the missing instruments NOT RUN. Neither is counted as coverage.

HANDOFF.md, PR-BODY.md, exact commands, full receipts and input hashes are prepared in the assigned output packet. No PR, push, merge, hardware or delegated work. Ready for the assigned independent reviewers.
