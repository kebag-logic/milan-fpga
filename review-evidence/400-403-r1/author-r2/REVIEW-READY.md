[A313] REVIEW READY

Commit: 2d61e7edafa63cff7d5f8fdca9840a969ee070a6 (local branch 400-403-declaration-truth).
Base merged: 864b36f5e9450ef64f75ca3f0d68c44330e447d7.

Changed: revalidated the preserved #400/#403 bundle on the assigned dev base. Dev's processor pin 990f96526bb89356c963a260ebbdcf2a77e6623a and ROM digests are retained. Both sides' applicable register/submodule documentation is retained; the submodule diagrams were regenerated. Revalidation corrected the compiled census fixture's missing declaration boot constants, the CRF overlay's expected 2 ms field, and the documentation row for the already-refused listener offset, with two additional refusal cases. Product behavior was not changed by these follow-ups.

Validation: every final requested invocation returned 0.

- Complete sw/builder/test_builder.py in pinned RV32 and compiler-absent modes. The former also requires RV32; both require live elaboration. All five shipped recipes elaborate. Audited selector wrappers use the supplied read-only SDK and explicitly hide target compilers in absent mode.
- sw/builder/test_declarations.py: five configs, 26 refusals, 15 header mutants and nine binding/reset mutants.
- make -C tb/verilator/csr and make -C tb/verilator/pp_shadow; additionally 20 CSR shape/reset combinations (391 checks each), generated VID73 and CRF-on wrapper fixtures (402 checks each).
- Every default milan_dp run entry, split into four chunks with separate exit receipts: all integration legs, both clean render controls and four detected render mutations, plus the GM-step clean control and three detected mutations. NxN4/8, divergent, shipping four-channel, default, reduced-feature and true audio-clock legs all pass.
- check_baremetal_only --check; docs_check in both CI inventory modes; check_em_dash against the assigned base; check_doc_style; gen_toc --check and --verify-anchors; check_doc_paths; gen_module_matrix --check; xvlog_gate --check; check_rtl_source_lists; check_sv_idiom; lint_rtl --check; check_cpp_idiom; check_py_idiom; check_port_contracts; measure_naming --check; measure_test_evidence --check; check_entity_shape --self-test; diagram/submodule/source checks; git diff --check.
- cd tests && behave --no-capture -f plain: 14 features, 344 scenarios, 1739 steps, no skips.
- Repository OOC recipe before/after all three changed RTL modules: zero delta in LUT, LUTRAM, FF, BRAM, DSP and carry counts at default parameters/Arty-current shape. Total LUT counts are 4236 (milan_csr), 66991 (KL_pp_shadow) and 96819 (milan_datapath). Final-head frontend outputs match all six synthesis inputs byte for byte.

Acceptance: the publicly amended #400/#403 declaration, generated-VID, reset/boot, per-output runtime-offset, promiscuous-RX and exact-allocation criteria are met by the recorded checks. Actual saved-state PTOF restore remains #70 under the 2026-09-23 owner decision. The assignment's STOP condition was not found.

Limits: the historical mf48 placed-utilization calibration report is absent, so that optional builder arm did not run. Target-only instruments are intentionally absent in the compiler-absent mode and ran in SDK mode. No placement, hardware, review approval or merge-readiness claim is made.

Handoff artifacts: HANDOFF.md (conflicts with file:line, acceptance mapping, test/gate tables, area and exact command logs), PR-BODY.md, gate-results.jsonl and validated-inputs.json in the assigned 400-403-a313 output directory. Initial failed attempts and their corrections are disclosed there. The final source and pinned submodules are clean.

No push or PR creation/edit was performed. R249 and R250 remain the assigned independent reviewers. Publication and the manager-owned full repository/candidate, hosted and merge/containment gates remain pending.
