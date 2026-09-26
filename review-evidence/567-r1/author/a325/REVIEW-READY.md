[A325] REVIEW READY
Commit: `1912c0472635ea174f1a2e2de2f3c96d09f55e9b`
Branch: `567-pp-pin-0922e434`; base `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.

Changed: adopt processor `0922e43408f891fc0b84a84691df86b4fd0f1c0d`; update current pin text, adoption notes and changelog; regenerate the submodule master, renders and PNG manifest. Parent RTL is unchanged; no donor source was edited. No push or PR action was performed.

Evidence: the processor's complete `hdl` tree is `d8879608b8fae8c06a505d7d5d485a97903a5766` at both pins. Both generated ROM images match the previous pin's digest values. The inventory checker reports 24 parameters in each of the top, guide and diagram; all 14 explicit parent bindings agree. The shadow suite passes 402 checks in each of its three configurations. Behavior tests pass 344 scenarios and 1,739 steps.

Validation: all assigned commands returned 0. The SDK builder reports one NOT RUN arm (absent historical calibration report); absent-compiler mode reports that arm plus the expected compiler-dependent firmware instruments. These skipped arms are not counted as passes. All gates ran in the foreground without pipelines.

<details>
<summary>Reproducible command evidence</summary>

| Command | Result |
|---|---|
| `make -C tb/verilator/pp_shadow` | rc 0 |
| `python3 protocol-processor/scripts/check-integrator-params.py` | rc 0 |
| `python3 sw/builder/test_builder.py --require-rv32` with the verified SDK compiler selector mapped to the supplied read-only SDK | rc 0; 855 audited compiler invocations |
| `python3 sw/builder/test_builder.py` with the three RV32 compiler candidates absent | rc 0; all three candidates hidden |
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | rc 0 |
| `python3 scripts/check_nvm_capture.py` | rc 0 |
| `python3 scripts/check_baremetal_only.py --check` | rc 0 |
| `python3 -B scripts/docs_check.py`, Git and no-Git filesystem modes | rc 0 in both |
| `python3 scripts/ci_events.py --check`; `python3 scripts/ci_events.py --selftest` | rc 0 each |
| `python3 scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a` | rc 0 |
| `python3 scripts/check_doc_style.py` | rc 0 |
| `python3 scripts/gen_toc.py --check`; `python3 scripts/gen_toc.py --verify-anchors` | rc 0 each |
| `python3 scripts/check_doc_paths.py` | rc 0 |
| `python3 docs/traceability/gen_module_matrix.py --check` | rc 0 |
| `python3 scripts/xvlog_gate.py --check` | rc 0; existing ratchet unchanged |
| `python3 scripts/check_rtl_source_lists.py` | rc 0 |
| `python3 scripts/check_sv_idiom.py`; `python3 scripts/lint_rtl.py --check` | rc 0 each |
| `python3 scripts/check_cpp_idiom.py`; `python3 scripts/check_py_idiom.py` | rc 0 each |
| `python3 scripts/check_port_contracts.py` | rc 0 |
| `python3 scripts/measure_naming.py --check`; `python3 scripts/measure_test_evidence.py --check` | rc 0 each |
| `cd tests && behave --no-capture -f plain` | rc 0 |
| `git diff --check`; `git diff --cached --check` | rc 0 each |
| `python3 scripts/check_submodule_docs.py`; `python3 docs/diagrams/submodule_boundaries.gen.py --check`; `python3 scripts/check_diagram_pngs.py` | rc 0 each |

</details>

Acceptance: 1 and 4 are met. Acceptance 2 is followed literally: ROM inputs did not change, so the ledger was not re-recorded. The assigned command set for acceptance 3 passes; the broader OOC path remains unresolved for the reason below. This is an author handoff for independent review, not a merge verdict.

Open risk/decision: the [previously recorded conflict](https://github.com/kebag-logic/milan-fpga/issues/567#issuecomment-5844889430) remains unresolved. `syn/yosys/ooc.sh:464` requires rows for the exact new processor pin; acceptance 2 currently prevents adding them because the ROM inputs are unchanged. The existing rows therefore do not authorize OOC synthesis at this pin. A public acceptance decision is required; no OOC pass is claimed. HANDOFF.md and PR-BODY.md are prepared in the assigned output directory.
