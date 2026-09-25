[A297] Round 3 handoff

Issue #508; PR #560; branch 508-pp-pin-adopt.
Starting head: 6a9828c172aa4d5d8ee49725e357a10bae2caa52.
Final local head: 224ec0e9a9fa129924bf8f0433cf70b4140f7bd2.
Status: implementation and all assigned final-head validation complete; ready for delta review.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/508#issuecomment-5825850226
Review findings: https://github.com/kebag-logic/milan-fpga/pull/560#issuecomment-5825848456 and https://github.com/kebag-logic/milan-fpga/pull/560#issuecomment-5825730404
Acceptance-2 decision: https://github.com/kebag-logic/milan-fpga/issues/508#issuecomment-5825732419

The decision resolves R306-1 F4 / R307-1 F2 without a source change. G1 remains ACTIVE with ACMP status zero on bind; G3 remains PASSIVE after an unanswered retry with no discovered talker.

Changes, limited to the assignment:

1. CHANGELOG.md: restored the complete historical #530 section from c266432dcb0cdd464205823a3d82cad260eedde2. The four #116/#113 lines remain only in the 990f9652 section. Its byte-identity SHA-256 is 9128aa97df78a8221ad9d38da576756f85d7e5409d0c66b10d4ef693a07f9c47.
2. hdl/milan/milan_datapath.sv and tb/verilator/pp_shadow/sim_main.cpp: corrected processor citations and named the cited constructs. prove_citations.py checks all nine spans, including the multiline and unchanged adjacent references, against 990f96526bb89356c963a260ebbdcf2a77e6623a. It compares the named source text with the earlier a8f8ce81 references and inventories every added source-line citation in the complete lane diff.
3. tb/verilator/milan_dp/sim_nxn.cpp: G8 now requires exactly two sink-0 pushes to each registered controller, zero sink-1 pushes, and grades all four sink-0 bodies. Each is PASSIVE, ACMP status zero, failure-valid/REGISTERING_FAILED clear, failure code and bridge zero, and equal to the solicited body. The first is named registrar withdrawal (srp_evt_tk_unreg_w), the second settlement teardown (lstn_gsi_changed_r). Live owner reads mean the first response already sees the teardown. The README and banner now state two pushes and both causes.
4. tb/verilator/milan_dp/gsi_mutants.py: a copied processor replays the withdrawal after 4096 cycles, after the legitimate pushes drain. It must fail the named G8 sink-0 count to controller A. The measured mutant also fails controller B's count. A simultaneous OR duplicate would coalesce, so the replay is delayed. No processor checkout is edited. duplicate-mutant-raw.log records the two actual failures: each controller received 3 pushes where 2 were required. record_duplicate_mutant.py reproduces that receipt using the committed campaign functions.

Results, repeated at the final commit: notification leg 380/380; mutation campaign 9/9 (one clean control and eight caught mutants); duplicate replay produces 2 failures across 396 checks. The additional 16 checks grade its two extra responses. Existing field mutants fail 7, 7, 7, 7, 21, 42 and 14 checks respectively. Final-head receipts supersede preliminary receipts.

Validation: all required commands returned rc 0 at the exact local head:

```text
make -C tb/verilator/milan_dp notify gsi-mutants
make -C tb/verilator/milan_dp run
make -C tb/verilator/pp_shadow
python3 scripts/docs_check.py
env GIT_DIR=/nonexistent-508-a297-git python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_doc_paths.py
python3 scripts/xvlog_gate.py --check
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/check_port_contracts.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_test_evidence.py --check
git diff --check
git diff --check c266432dcb0cdd464205823a3d82cad260eedde2 HEAD
```

The notification leg passed 380/380; the campaign passed 9/9 controls (clean plus eight caught mutants). The complete default datapath run passed, including its built-in controls. The shadow suite passed 371/371. The citation/changelog proof and raw duplicate-mutant proof also returned zero. The HDL frontend ran with its four existing recorded findings; all budgets are unchanged. The em-dash and TOC checks used the locked Markdown dependencies. The no-git documentation mode skips only its Git inventory-parity arm.

All 19 final-head command/proof receipts have rc 0 and a clean worktree. completion-check.json binds their logs by SHA-256. gates.jsonl retains the earlier preliminary receipts separately. Every command ran in the foreground without a shell pipeline.

scope-proof.json verifies the change boundary, unchanged processor gitlink, one-line commit, and clean worktree/submodules. Only six tracked files changed. One commit, one-line subject, no body or trailers. The processor gitlink remains 990f96526bb89356c963a260ebbdcf2a77e6623a. The working tree is clean after the commit.

Public evidence was fetched read-only into temporary scratch and deleted after reading. See review-sources.md. No private transcripts or other management output directories were read. The temporary Markdown dependency environment was outside this output directory and has been removed. For reproduction, install tools/markdown/requirements.txt with its locked hashes into a fresh temporary environment; use that interpreter for the em-dash and TOC commands. markdown-env.txt records the original interpreter location.

PR-BODY.md contains the full current public PR body with the [A297] prefix, a Round 3 section, the acceptance decision, retained round-2 evidence, and Closes #508. It is a proposed body only.

Publication: [A297] REVIEW READY posted on #508: https://github.com/kebag-logic/milan-fpga/issues/508#issuecomment-5826185808. REVIEW-READY.md contains the exact posted body. No push, PR edit, merge, hardware action, processor edit, additional checkout, or parallel authoring was performed. The review handoff remains to independent reviewers R306 and R307. New-head publication and hosted checks remain pending; prior-head hosted evidence does not validate this unpushed head.
