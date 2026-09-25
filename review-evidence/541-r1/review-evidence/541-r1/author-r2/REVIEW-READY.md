[A306] REVIEW READY

Commit: `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c`
Branch: `541-crf-unlock`
Base unchanged: `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`

Round 2 addresses R322-1 F1, R323-1 F1, and assigned R323-1 F2.

- Added a public-output receiver check: matched wrong-type PDUs arrive every 2 ms after the last accepted PDU. Lock is retained through 99.96 ms, clears by 100.06 ms with exactly one MEDIA_UNLOCKED, and stays cleared without recount or relock through 200.06 ms.
- Added `validation_error_refreshes_timeout`, which must fail `reject stream cannot refresh the 100 ms timeout`. The default campaign passes all ten controls; both validation-error mutants compile, return 1, and fail their required named checks.
- Ran the published reviewer scripts unchanged against this head. R322 `P2_error_refreshes_timeout` and R323 `uf_refreshes_timeout` are both DETECTED by the discontinuity check, each with four named failures. Both clean controls pass. Unit legs remain green; R323's connected talker leg also remains green.
- Updated the `crf_rx` testing-index row and evidence description to name both validation-error mutants. No ratchet budget change.

All RTL, the receiver header and the CRF_CTRL text remain byte-identical to the starting head. The decision and clause evidence remain unchanged. No dev merge occurred.

Validation: all 16 assigned invocations returned 0, in the foreground without pipelines:

```sh
make -C tb/verilator/crf_rx
make -C tb/verilator/mmcm_servo
python3 scripts/docs_check.py
python3 scripts/docs_check.py  # exact-head archive without Git metadata
python3 scripts/check_em_dash.py --base 5b73d3f47dfed519eb988c13d6beb1db664ef1e0
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_doc_paths.py
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/xvlog_gate.py --check
python3 scripts/check_sv_idiom.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/measure_test_evidence.py --check
git diff --check
```

Receiver: 13,836 unit, 2,201 discontinuity, 69 connected talker-step checks and ten mutation controls, all passing. Servo: 85 unit, eight playback and 113 PHC-step checks, all passing. Both documentation modes report zero findings. Live HDL analysis passes at the existing four processor findings, with zero parent-HDL findings.

Acceptance: round-2 items 1 and 2 are met. HANDOFF.md contains file:line changes, named check/mutant verdicts, gate receipts and unchanged-script hashes. PR-BODY.md updates the complete current body with Round 2 and retains `Closes #541`. Both are in the assigned output directory. Scratch evidence and exports were removed. The commit remains local; no push or PR edit was performed.

Open implementation risks/questions: none within this assignment. Independent re-review remains pending; this is author evidence, not a review verdict.
