[A260] REVIEW READY

Commit: `babb8925030612e47c687b1fda1a1ce614988721` (local `551-licence-real-grant`; not pushed).

Changed: the specification-facing licence scenario pins ACTIVE AND the per-source real grant, including both slices and no extra logic. ACTIVE-only and raw-grant-only mutants each fail that actual scenario (rc 1), with clean controls passing before and after. Q-9/Q-10 restore module mapping, processor status, caveat and clause rationale; regenerated matrices again list `KL_pp_shadow` against 34.3/34.4. The remaining ACTIVE-only interface/contract descriptions and unconditional refusal claims are corrected. This round changes no RTL logic or processor pin.

The default licence leg passes 253 checks. The additional `--unwarmed-refusal` arm is explicitly skipped by default as EXPECTED-FAIL processor #112. Running it gives 339 checks / 28 failures, rc 1: both sources and both phases expose a grant/licence pulse, STREAM_START/STREAM_STOP pair and interval-counter resets. No refused-case PDU appeared in that schedule. All no-pulse assertions remain intact. The latency text covers the reviewed 4-cycle changed-TSpec case as well as the 0--2 warm cycles.

Validation (foreground, no gate pipelines):

- `cd tests && behave --no-capture -f plain`: rc 0; 344 scenarios / 1739 steps.
- `make -C tb/verilator/milan_dp crflic VERILATOR_JOBS=8`: rc 0; 253 checks / 0 failures.
- `make -C tb/verilator/milan_dp crflic-mutants VERILATOR_JOBS=8`: rc 0; 7/7, all six mutants caught.
- `make -C tb/verilator/milan_dp VERILATOR_JOBS=8`: rc 0; all 13 simulation legs plus the render campaign (6/6).
- `python3 scripts/docs_check.py`: rc 0 in both Git and filesystem-inventory CI modes.
- `python3 scripts/check_em_dash.py --base 59b816708852472da6ed4576386c30ebd5f8f839`, `check_doc_style.py`, `gen_toc.py --check`, `check_doc_paths.py`, and `docs/traceability/gen_module_matrix.py --check`: all rc 0.
- `python3 scripts/xvlog_gate.py --check`, `check_rtl_source_lists.py`, `check_py_idiom.py`, `check_cpp_idiom.py`, `check_sv_idiom.py`, and `git diff --check`: all rc 0. Syntax analysis reports zero first-party and four unchanged processor findings at the ratchet.
- Local `rtl-fast` equivalents: full behaviour suite, `ci_scope.py --selftest` plus actual scope classification, `lint_rtl.py --check --self-test`, `pp_srcs.py --check --selftest`, and `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow`: all rc 0.

Acceptance: the assigned F2/F3/F4 corrections and F1 documentation/reproducer work are implemented for re-review. F1's functional acceptance remains **unmet**: a refused re-declaration with a TSpec different from the source's previous one can still get about one round of licence because the first-round grant uses the previous slope. [Processor #112](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/112) and its parent pin must land, then the unwarmed arm must become a required pass before #551 closes. This follows the [recorded decision](https://github.com/kebag-logic/milan-fpga/issues/551#issuecomment-5816014072).

HANDOFF.md, the full replacement PR-BODY.md and reproducible receipts are prepared in the assigned output directory. Hosted checks, publication and independent re-review remain with the manager. No PR edit, push, merge or hardware action was performed.
