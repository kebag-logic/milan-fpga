# Receipts (generated from the files present)

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `docs/docs-workflow-steps-f97e49fe.txt` | 25,563 | `b6424ac2ff4bee68` | # tools/docs_steps.py f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21: every run: step of docs.yml's gate jobs on fresh clean clones, in ten-minute windows (STEP_FILTE |
| `docs/step-logs/08-docs-gates-0-Added_line_em_dash_gate.log` | 236 | `6f101ef8f65e6aba` | # head f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 job docs-gates-0 step: Added-line em-dash gate |
| `docs/step-logs/09-docs-gates-0-Concise_audience_documentation_gate.log` | 274 | `8945e0aa4b96e640` | # head f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 job docs-gates-0 step: Concise audience documentation gate |
| `docs/step-logs/33-docs-gates-0-Test_evidence_ratchet.log` | 32,563 | `5c753b65a13e5b2e` | # head f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 job docs-gates-0 step: Test-evidence ratchet |
| `docs/step-logs/35-docs-gates-0-SystemVerilog_idiom_gate.log` | 3,269 | `404afaf0d971bf4e` | # head f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 job docs-gates-0 step: SystemVerilog idiom gate |
| `docs/step-logs/36-docs-gates-0-C_and_C_idiom_gate.log` | 4,827 | `f2fa65b212a7e55b` | # head f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 job docs-gates-0 step: C and C++ idiom gate |
| `docs/step-logs/37-docs-gates-0-Python_idiom_gate.log` | 3,081 | `a9e60d25645641ba` | # head f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 job docs-gates-0 step: Python idiom gate |
| `ledger/image-hashes-vs-round1.txt` | 5,937 | `e9e060baad15d2ac` | # the 24 image digests (elf, stripped, loadable at each of 8 points) at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 against round 1's at 39e9c9d2 |
| `ledger/image-inputs-f97e49fe.txt` | 1,691 | `23fdac93c6f411e9` | # paths changed from the routed commit 973f2f20 to the head f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| `ledger/plat-ledger-f97e49fe.txt` | 15,111 | `96c0c4edd36bb3ce` | # tools/ledger.sh: plat_ledger.py on the clean clone at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21, then each image's sha256 |
| `rtl/gptp_plane-all-window1-f97e49fe.log` | 12,752 | `9539fd9764cea1b8` | # make -C tb/verilator/gptp_plane (all) at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21: run passes, phc-step stopped by the 585 s window |
| `rtl/gptp_plane-phc-step-arms1-4-f97e49fe.log` | 1,473 | `64c814e858adf7d8` | # make -C tb/verilator/gptp_plane phc-step at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21: clean and the first three arms pass, then the 585 s window ends it |
| `rtl/gptp_plane-phc-step-arms5-8-f97e49fe.log` | 638 | `00c6d0032a2234fc` | # phc_step_slice.py --mutants (phc_step.py plus the PHC_STEP_ARMS filter) at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21: the four arms window 1 did not reach |
| `rtl/gptp_plane-run-f97e49fe.log` | 1,404 | `78901014f268c7ba` | # make -C tb/verilator/gptp_plane run at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| `rtl/gptp_shadow-legs-SUMMARY-f97e49fe.txt` | 146 | `d4737e09263816d5` | head f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 porcelain 0 |
| `rtl/gptp_shadow-lifecycle-f97e49fe.log` | 11,785 | `d120570118166aa2` | # make -C tb/verilator/gptp_shadow lifecycle (test_mutant_lifecycle.py) on the clean clone at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| `rtl/gptp_shadow-mutants-credit-control-at-bbfdb674.log` | 832 | `4f8a4c5b03b6420b` | # mutants.py main() on MUTATIONS[8:9], credit_never_withheld, on a clean clone at bbfdb674: already caught only by other checks |
| `rtl/gptp_shadow-mutants-slice-0-4-d616b1c6.log` | 998 | `e02529545d209952` | # mutants.py main() on MUTATIONS[0:4] (tools/mutants_slice.py), lane at d616b1c6, whose campaign inputs equal f97e49fe's |
| `rtl/gptp_shadow-mutants-slice-4-8-d616b1c6.log` | 1,193 | `edebca465923f052` | # mutants.py main() on MUTATIONS[4:8], lane at d616b1c6 (campaign inputs equal f97e49fe's) |
| `rtl/gptp_shadow-mutants-slice-8-11-d616b1c6.log` | 1,180 | `675ae13bb816aff1` | # mutants.py main() on MUTATIONS[8:11], lane at d616b1c6 (campaign inputs equal f97e49fe's): the two new controls |
| `rtl/gptp_shadow-run-base-bbfdb674.log` | 3,083 | `75594a5ef8dcc1ce` | # make -C tb/verilator/gptp_shadow run on a clean clone at bbfdb674 (the round-1 head), for the check count and run time |
| `rtl/gptp_shadow-run-f97e49fe.log` | 9,836 | `00f91b6cf8ed8078` | # make -C tb/verilator/gptp_shadow run on a clean clone at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 (pinned Verilator 5.050), full log |
| `rtl/gptp_tables-all-window1-f97e49fe.log` | 9,245 | `d6326d2c94f21cb0` | # make -C tb/verilator/gptp_tables (all) at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21: limits and run pass, mutants stopped by the 585 s window after 21 controls |
| `rtl/gptp_tables-limits-f97e49fe.log` | 186 | `6f3346effcd0f4f6` | # make -C tb/verilator/gptp_tables limits at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| `rtl/gptp_tables-mutants-0-13-f97e49fe.log` | 1,252 | `ab0b97560641b8ac` | # gptp_tables mutants.py main() on MUTATIONS[0:13] (tools/suite_mutants_slice.py) at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| `rtl/gptp_tables-mutants-13-26-f97e49fe.log` | 1,229 | `902ca8800502d586` | # gptp_tables mutants.py main() on MUTATIONS[13:26] at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| `rtl/gptp_txts-f97e49fe.log` | 26,281 | `985dafa4a1b92e6b` | # make -C tb/verilator/gptp_txts (all: mutants) at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| `rtl/legs1-SUMMARY-f97e49fe.txt` | 262 | `4d14680916dee74d` | head f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 porcelain 0 |
| `rtl/legs2-SUMMARY-f97e49fe.txt` | 219 | `eb9e2582690a0de5` | head f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 porcelain 0 |
| `rtl/legs3-SUMMARY-f97e49fe.txt` | 165 | `9cd06ddbb824fe0a` | head f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 porcelain 0 |
| `rtl/legs4-SUMMARY-f97e49fe.txt` | 161 | `46dd233185e1151b` | head f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 porcelain 0 |
| `rtl/lint_rtl-f97e49fe.log` | 14,903 | `c0e8f96addeb769a` | # python3 scripts/lint_rtl.py --check --self-test --jobs 16 on the clean clone at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| `rtl/milan_dp-gptp-f97e49fe.log` | 87,819 | `a4e47f9c057a9de7` | # make -C tb/verilator/milan_dp gptp at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| `rtl/milan_dp-gptp-lat-f97e49fe.log` | 8,573 | `e30eb943e2f99cbf` | # make -C tb/verilator/milan_dp gptp-lat at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| `rtl/milan_dp-gptp-lat-window1-f97e49fe.log` | 88,742 | `d37eb20055d70564` | # make -C tb/verilator/milan_dp gptp-lat at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21: stopped by the 585 s window under six parallel legs |
| `rtl/probe-control-f97e49fe.log` | 4,954 | `07ef9b4e570362e5` | # tools/probe_r916.py case control: gptp_shadow run at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21, no patch (rc in probe-*.rc) |
| `rtl/probe-control.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `rtl/probe-delayed-announce-f97e49fe.log` | 5,590 | `47dd168158688344` | # tools/probe_r916.py: R916-1's delayed-announce.patch on gptp-processor, gptp_shadow run at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| `rtl/probe-delayed-announce.rc` | 2 | `53c234e5e8472b6a` | 2 |
| `rtl/probe-retained-slave-rate-f97e49fe.log` | 5,668 | `94e7b5aca7ffadb3` | # tools/probe_r916.py: R916-1's retained-slave-rate.patch on gptp-processor, gptp_shadow run at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21 |
| `rtl/probe-retained-slave-rate.rc` | 2 | `53c234e5e8472b6a` | 2 |
| `rtl/tsn_fuzz-f97e49fe.log` | 36,465 | `d880d9b92507dcf4` | # make -C tb/verilator/tsn_fuzz at f97e49fec4fabd42ec6cb526c3c9baf61e0f1e21, TSN_GEN_ROOT at tsn-gen deca300c (the CI pin) |
| `rtl/tsn_fuzz-tracked-diff-f97e49fe.txt` | 1,500 | `cec74a030bc9fb71` | # the two TEST_RESULTS.md the campaigns rewrite: only the timestamps move (restored in the clone, not committed) |
| `tools/docs_steps.py.txt` | 7,637 | `104cf38e79b64f88` | #!/usr/bin/env python3 |
| `tools/ledger.sh.txt` | 1,258 | `a7652d7563d7bba3` | #!/usr/bin/env bash |
| `tools/legs.sh.txt` | 1,278 | `193c171008d64c8d` | #!/usr/bin/env bash |
| `tools/legs3.sh.txt` | 1,226 | `56797e27c099da11` | #!/usr/bin/env bash |
| `tools/mkclone.sh.txt` | 746 | `da30148cf8d51fbd` | #!/bin/bash |
| `tools/mutants_slice.py.txt` | 838 | `de4dc53f17271bea` | #!/usr/bin/env python3 |
| `tools/package.py.txt` | 9,348 | `a6b654f49830b6e3` | #!/usr/bin/env python3 |
| `tools/phc_step_slice.py.txt` | 6,949 | `749fa42afcbfdc5f` | #!/usr/bin/env python3 |
| `tools/probe_r916.py.txt` | 2,553 | `557c558cd957dbba` | #!/usr/bin/env python3 |
| `tools/suite_mutants_slice.py.txt` | 797 | `6ef546e48b3e8ad6` | #!/usr/bin/env python3 |
