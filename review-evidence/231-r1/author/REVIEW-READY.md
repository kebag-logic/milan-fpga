[A328] REVIEW READY

Commit: `af6d19c553ad8c445a80528344baf2273b41ad46`
Branch: `231-pp-shadow-baseline`
Changed: baseline page, complete parameter/image manifest, reproduction recipe, script preparation helper with nine negative controls, and the area-budget link. No RTL or donor changes.

Measurements: both product OOC syntheses, shipping 1x1 place-and-route, integrated 8x8 synthesis, three placement directives, and equivalent-geometry mapping completed at rc 0. The committed baseline identifies dominant hierarchy consumers, includes exact carry and scoped timing evidence, explains mapping differences, and retains the corrected historical provenance. Every image and source hash was rechecked; zero Synth 8-4445 diagnostics.

Validation: every entrypoint below returned rc 0, without pipes:

```text
python3 sw/builder/test_builder.py --require-rv32  (full entrypoint, audited pinned-SDK executable selection)
python3 sw/builder/test_builder.py                (full entrypoint, all target compiler candidates deliberately absent)
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
python3 scripts/check_nvm_capture.py
python3 scripts/check_baremetal_only.py --check
python3 -B scripts/docs_check.py                 (git and no-git CI modes)
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_doc_paths.py
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/xvlog_gate.py --check
python3 scripts/check_rtl_source_lists.py
python3 scripts/check_sv_idiom.py
python3 scripts/lint_rtl.py --check
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_port_contracts.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_test_evidence.py --check
cd tests && behave --no-capture -f plain
git diff --check
git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a
python3 syn/ooc/pp_baseline.py --selftest
```

The SDK run recorded 855 target compiler invocations (807 successful and 48 expected negative mutation refusals). Both builder modes explicitly report the historical mf48 calibration arm NOT RUN because the old report is unavailable; the no-compiler mode additionally omits the target compile/census arm by design. These omissions are preserved as coverage limits. The installed parser front end ran rather than taking its unavailable-tool skip.

Acceptance criteria: both product shapes measured with complete inputs; hierarchy attribution and distinct flow/stage labels published; exact reproduction commands committed; baseline reference posted on #229 at https://github.com/kebag-logic/milan-fpga/issues/229#issuecomment-5845524962. Publication of the local commit remains the maintainer's step under the no-push instruction.

Open limits: 8x8 exceeds device LUT capacity and has no placement claim. Existing integrated constraint warnings and I/O-delay omissions limit timing claims. No hardware test, push, PR creation/edit or merge was performed. Internal and external independent reviews remain pending.
