[A257] REVIEW READY

Commit: `4eca4540d6a278aeb56687029d752bade6e714e3` (local branch `551-licence-real-grant`, based on `59b816708852472da6ed4576386c30ebd5f8f839`).

Changed: every parent CRF/AAF licence now requires ACTIVE AND the real per-source admission grant. The refused-branch comments and FR_NFR, REGISTER_MAP, EGRESS_QUEUE_MAP, ieee8021q and CHANGELOG are updated.

Acceptance evidence: the focused licence simulation passes 253 checks. Both sources and both admission phases exercise a ceiling-refused re-declaration: optimistic ACTIVE rises, the real grant stays low, and no licence, STREAM_START/STREAM_STOP pair, interval-counter reset or PDU occurs. Matching admitted cases stream. Added start latency is 2/1 cycles for AAF and 0/1 for CRF at the two round phases; ordinary Listener Ready adds 0. This is 0--20 ns at the leg's 100 MHz admission clock, or 0--40 ns for those cycles at 50 MHz.

The fixture stages a pending processor service tuple, then supplies Listener Ready through the real MAC decoder. It does not force the admission verdict, registrar, ACTIVE or licence. Nonzero interval-counter histories make unintended resets visible.

Validation (all commands run without pipelines):

- `make -C tb/verilator/milan_dp crflic VERILATOR_JOBS=8`: rc 0, 253 checks, 0 failures.
- `make -C tb/verilator/milan_dp crflic-mutants VERILATOR_JOBS=8`: rc 0, 7/7 checks; all six mutants caught by named assertions, including three dropping the real grant.
- `make -C tb/verilator/milan_dp VERILATOR_JOBS=8`: rc 0; all 13 simulation legs pass, plus the built-in render campaign (6/6 checks).
- `python3 scripts/docs_check.py`: rc 0 in both git and filesystem inventory modes. The latter uses an absent `GIT_DIR` and reports `filesystem walk (no git)`.
- `python3 scripts/check_em_dash.py --base 59b816708852472da6ed4576386c30ebd5f8f839`: rc 0.
- `python3 scripts/check_doc_style.py`, `python3 scripts/gen_toc.py --check`, `python3 scripts/check_doc_paths.py`: rc 0.
- `python3 scripts/xvlog_gate.py --check`: rc 0; 0 first-party findings, 4 unchanged pinned-processor findings at the ratchet.
- `python3 scripts/check_rtl_source_lists.py`, `python3 scripts/check_cpp_idiom.py`, `python3 scripts/check_py_idiom.py`: rc 0.
- Additional house-style/lint checks: `python3 scripts/check_sv_idiom.py`, `python3 scripts/lint_rtl.py --check`: rc 0.
- `git diff --check`: rc 0.

HANDOFF.md contains file:line changes, test/mutant/gate tables, fixture limits and local log names. PR-BODY.md is prepared in the assigned output directory. No push, PR change, merge or hardware action was performed.

Open risks/questions: independent review and subsequent publication/merge gates remain pending with the manager; no implementation blocker.
