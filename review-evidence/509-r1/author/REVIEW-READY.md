[A327] REVIEW READY

Commit: `20423082f221a02f3de72952cec4e1ac0c839b1d`
Branch: `509-pp-descriptor-ownership`; base `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.

Changed: published the parent L1-L10/ADP allocation in
`docs/reference/PP_DESCRIPTOR_OWNERSHIP.md`, added reproducible packed-byte
measurements in `scripts/audit_pp_descriptors.py`, and reconciled the builder
reference's census and identity claims. Four files; no production validator,
shipping input, RTL, donor or pin change. Local commit only.

Acceptance evidence:
- Matrix rows name clauses, producers/consumers, check paths, configuration bounds and open owners; construction and discriminating refusals are separate.
- All five images decoded: 32/64/96/41/116 descriptors and 5792/10112/15360/7352/18288 bytes in reference-page order. All 15 generator CLI invocations passed and matched the audited image hashes. The receipt contains 30 packer, 13 YAML and two map probes.
- The generator-only reset_time mutation changes arty_4x4 image byte 6741 while model ID stays `0x001BC557FC6ABBC8`, retaining #495/processor #38 ownership. Parent contract updated; exact processor wording is in HANDOFF.md for its separate reviewed change. No implementation relies on that unpublished update.
- Follow-ups F1-F6 are bounded for maintainer filing: invalid model IDs, listener buffer floor, format validation, INTERNAL source availability, the F07.2 zero-cluster discrepancy, and parent L6/L10 image checks. The discrepancy needs a public clause-backed disposition under processor #60. #478/#464 stay closed and unexpanded; runtime processor #82 work stays excluded.

Validation: all requested commands returned 0; 29 recorded modes including the
audit and entity-shape self-test. Both complete builder runs passed using an
invocation wrapper: verified SDK mapping with `--require-rv32`, then deliberate
absence of all three cross-compiler candidates. SDK mode excludes only gate 11
calibration (missing placement report); absent mode additionally excludes the
compiler-backed gate 1b instruments. These exclusions are not counted as passes.

The #464-repaired generator self-test passes 20 checks and retains six declared
compatibility-map deviations. Entity-shape: 136 checks, zero failures. Behavior:
344 scenarios and 1739 steps pass. Both CI documentation modes pass; filesystem
mode has the expected inventory-parity skip. Existing xvlog/RTL lint ratchets
remain at 4/90 findings. Worktree clean after the final run.

<details>
<summary>Exact validation entry points (all exit 0)</summary>

Select the verified SDK and compiler-absent environments respectively for the
two complete builder commands. Compiler invocation receipts are in the handoff.

```sh
python3 scripts/audit_pp_descriptors.py --output /tmp/pp-descriptor-audit.json
python3 sw/builder/test_builder.py --require-rv32
python3 sw/builder/test_builder.py
python3 avdecc/gen_aem_store.py --self-test
python3 scripts/check_entity_shape.py --self-test
python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
python3 scripts/check_nvm_capture.py
python3 scripts/check_baremetal_only.py --check
python3 -B scripts/docs_check.py
GIT_DIR=/dev/null python3 -B scripts/docs_check.py
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
(cd tests && behave --no-capture -f plain)
git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a
```

</details>

No multi-configuration maximum proof or product-compliance verdict is claimed.
The output handoff contains file:line changes, image/evidence/gate tables,
compiler invocation receipts, exact separate processor wording and PR-BODY.md.
Independent reviews remain with [R330] and [R331]; publication remains with the maintainer.
