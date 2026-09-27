[A371] REVIEW READY
Commit: f8a52f919bd309960046330a5af127b56731cb27 (local commit; not pushed).

Changed: derive AEM_N_CONTROL_C from descriptor_counts; pass CONTROL through milan_datapath and KL_pp_shadow; bind N_AUDIO_UNIT_P, N_CLK_DOMAIN_P and N_CONTROL_P at u_pp while retaining the parent's N_CLK_DOM_P name. Update the parent inventory and add two-hop binding, header/census and descriptor-count checks.

Decision: follow the recorded binding option. _overlay_document and aem_assemble._entity_descriptors unconditionally construct one AUDIO_UNIT, CLOCK_DOMAIN and IDENTIFY CONTROL. No configuration can remove them, so no zero-count refusal is needed (Milan v1.2 Section 5.3.3, assignment citation).

Validation, all rc 0:
- Full sw/builder/test_builder.py --require-rv32 bank.
- Full sw/builder/test_builder.py bank with all three cross-compiler candidates hidden; native probes retained, absence audit asserted.
- sw/builder/test_declarations.py.
- scripts/check_entity_shape.py --self-test: 219 checks, zero failures; 24 new mutants killed, including unbound parameters, literal bindings and swapped pairs at both hops, plus a positive 2/3/4 census fixture.
- scripts/check_nvm_capture.py.
- scripts/docs_check.py, scripts/check_doc_paths.py, scripts/gen_toc.py --check, scripts/check_feature_status.py, scripts/check_doc_style.py, scripts/check_py_idiom.py, scripts/check_em_dash.py --base 2a2a7bb655e528edc3087c88033cd3a47546feb4.
- git diff --check, including the committed base-to-head diff.

Acceptance: all five tracked configurations build and retain counts 1/1/1. Their headers add only `localparam int AEM_N_CONTROL_C = 1;` (existing alignment preserved); all 65 other generated artifacts compare byte-identically with the base. Verilator 5.052 KL_pp_shadow elaborations at AX 1x1 and 8x8 have identical post-elaboration statistics in all four stages (127 and 128 node-kind rows respectively). Exact header diffs, SHA-256/size tables, commands, statistics, mutation and gate tables are in HANDOFF.md; PR-BODY.md is prepared.

Limits: both builder modes report the historical resource-calibration arm NOT RUN because its placement report is absent; compiler-absent mode also deliberately reports the compiler-backed census NOT RUN, which the present run exercises. The assigned docs/spec-refs.md is absent, so the decision record explicitly identifies the assignment's clause citation and the construction evidence used. No tracked configuration was refused or changed a count; STOP was not triggered. Processor pin 870ff88ad35bbd532244e4c7e6d7661b9f6e1366 and processor sources are unchanged. Worktree clean. Independent reviews by [R356] and [R357] remain pending.
