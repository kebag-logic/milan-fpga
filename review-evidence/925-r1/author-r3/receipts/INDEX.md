# Receipts index (generated from the files present by gen_index.py)

| File | Bytes | sha256 (16) | First line |
|---|---:|---|---|
| `budget/1x1-1if-artifacts.txt` | 31,080 | `c6d20299c02ee641` | Raw budget artifacts retained in scratch (files over 200 KB not copied): |
| `budget/1x1-1if-summary.md` | 3,804 | `fa09fd94953eaa56` | CPU budget 1x1-1if: measured 7a2def7c, both firmware ELFs relink byte-identical at 5f625090. |
| `budget/1x1-1if-table.md` | 188,630 | `3aaa9d91786786f9` | Round 3 CPU-budget 1x1/1if: complete row table, measured firmware byte-identical at 5f625090, rc 0 |
| `budget/1x1-1if.log` | 46,744 | `91b76942d9d5786a` | Round 3: CPU budget 1x1/1if, rc 0, 7a2def7c firmware byte-identical at 5f625090 |
| `budget/8x8-1if-artifacts.txt` | 30,770 | `323251fc5c8493d4` | Raw budget artifacts retained in scratch (files over 200 KB not copied): |
| `budget/8x8-1if-summary.md` | 12,061 | `c22651af7e25c737` | CPU budget 8x8-1if: measured 7a2def7c, both firmware ELFs relink byte-identical at 5f625090. |
| `budget/8x8-1if-table.md` | 187,195 | `f76858b97ce0ec40` | Round 3 CPU-budget 8x8/1if row table; measured firmware byte-identical at 5f625090 |
| `budget/8x8-1if.log` | 54,848 | `292d267e6a884404` | Round 3 CPU-budget 8x8/1if: rc 1, the three #914 statement categories; measured firmware byte-identi |
| `budget/comparison-audit.txt` | 1,595 | `b6778b60e0bfe32d` | Budget comparison at final firmware 5f625090; raw results sizes and hashes are in the artifact manif |
| `firmware/cov-check.log` | 5,429 | `e2eabaefc1c7e621` | head 5f625090 (clean clone, own unit); python3 -B sw/firmware/gtest/fw_coverage.py --check --jobs 4; |
| `firmware/cov-write-7a2def7c.log` | 5,504 | `bc21aa94465b27ec` | head 7a2def7c (clean clone, own unit); python3 -B sw/firmware/gtest/fw_coverage.py --write --jobs 8  |
| `firmware/fw0.log` | 77,239 | `5d4a88fe8e6aa637` | head 5f625090 (clean clone, own unit); python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --requ |
| `firmware/fw1.log` | 135,936 | `38ed7e3dc8ca58dc` | head 5f625090 (clean clone, own unit); python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --requ |
| `firmware/fw2.log` | 153,915 | `28874ae4636ff185` | head 5f625090 (clean clone, own unit); python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --requ |
| `firmware/fw3.log` | 5,326 | `bfc58e39617ada3b` | head 5f625090 (clean clone, own unit); python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --requ |
| `firmware/fw3.part1.log` | 159,895 | `3799a377a90458b7` | head 5f625090 (clean clone, own unit); python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --requ |
| `firmware/fw3.part2.log` | 43,308 | `9fb2879be065c504` | Continuation of fw3.part1.log, same completed run. |
| `graders/flip_grade-1x1-1if.txt` | 1,296 | `57c2064bc96d3525` | head 5f625090 (clean clone); python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --poi |
| `graders/load_grade.txt` | 1,513 | `add6228211076c89` | head 5f625090 (clean clone); python3 -I tb/verilator/ctrl_service_budget/load_grade.py --check; rc 0 |
| `images/final-budget-image-identity.txt` | 2,190 | `99e8c032807df391` | 5f625090 clean clone; both budget images relinked against their recorded flash maps; rc 0 |
| `images/release-identity.txt` | 1,253 | `22f50517b5b64622` | Release firmware comparison, 16ba667d vs 5f625090 (clean clone rebuild, both configurations rc 0). |
| `images/round2-vs-round3-route-exports.txt` | 1,156 | `930159f457e54f83` | round 2 (a9f0dbc0, whose images 09a948d4 relinks byte-identical) vs round 3 (7a2def7c) split exports |
| `ledger/plat_ledger-before-record.log` | 12,590 | `3fb0f4128cd6a87d` | plat_ledger.py on the worktree before the ledger record (6e4d9c1a's sources): rc 1, the findings the |
| `ledger/plat_ledger-final.log` | 12,424 | `176a6d900b6e3913` | 5f625090 clean clone; python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <output>; r |
| `ledger/plat_ledger-worktree.log` | 11,428 | `d579e77011fe5b15` | plat_ledger.py --build-dir <dir> on the worktree with the ledger record (= 44265574's sources); rc 0 |
| `ledger/test_ctrl_memory-final.log` | 45,042 | `5dd05b702b17e098` | 5f625090 clean clone; python3 -B sw/litex/test_ctrl_memory.py; rc 0 |
| `ledger/test_ctrl_memory.log` | 45,059 | `f51c0f44031993d9` | python3 -B sw/litex/test_ctrl_memory.py on the worktree (= 44265574's sources); rc 0 |
| `plants/feedback-and-held-latest-if1.log` | 5,255 | `0c29e91e26903284` | head 7a2def7c (clean clone); scripts run_plants.py feedback-latest-* held-latest-* at 1 interface(s) |
| `plants/feedback-and-held-latest-if2.log` | 12,933 | `98cf19b76e032fc1` | head 7a2def7c (clean clone); scripts run_plants.py feedback-latest-* held-latest-* at 2 interface(s) |
| `provenance/completed-runs.txt` | 3,294 | `1d2c52fb08fab20c` | Source and receipt provenance, resumed at 5f625090. |
| `provenance/final-audit.txt` | 868 | `23217dc496ca62b8` | Final packet audit, 2026-11-17 06:24 CET |
| `provenance/manager-rulings.txt` | 2,584 | `c88f391967c4060c` | https://github.com/kebag-logic/milan-fpga/issues/925#issuecomment-6908876793 |
| `provenance/publication.txt` | 434 | `019af42cf7291d33` | Round 3 publication, 2026-11-17 06:24 CET |
| `provenance/reviewer-inputs.txt` | 1,114 | `ae7fb677d1eeb187` | Reviewer input files, unchanged copies; full reports remain at their public review comments. |
| `provenance/scope-integrity.txt` | 1,938 | `f0ccee7648a08f80` | Scope integrity at 5f625090 against the reviewed round-2 head 09a948d4. |
| `reviewer-drivers/r849-1/r849_drive.py` | 5,174 | `bea199c1d73b8923` | """Reviewer drivers for #925 at the exact head, run from the clone's own harness modules. |
| `reviewer-drivers/r849-1/r849_probe_tests.cpp` | 9,127 | `c8bf7839dea64be6` | // Reviewer probe scenarios for #925 (appended to a disposable copy of srp_mbx.cpp; never committed) |
| `reviewer-drivers/r850-1/probes.cpp` | 2,490 | `7ae77e56a790d065` | namespace { |
| `reviewer-drivers/r850-1/rebind.cpp` | 1,049 | `e5b0f773db2cb92a` | namespace { |
| `reviewer-drivers/r850-1/reproduce.cpp` | 2,015 | `57b7a2d626c02208` | namespace { |
| `reviewer-drivers/r850-1/reproduce_feedback.cpp` | 1,202 | `da3ea04ea45628bd` | namespace { |
| `reviewer-drivers/r850-1/run_probes.py` | 1,179 | `7f3d6a6c37500f84` | #!/usr/bin/env python3 |
| `reviewer-drivers/r850-1/run_rebind.py` | 1,086 | `cde2b4bf5feab8a8` | #!/usr/bin/env python3 |
| `reviewer-drivers/r850-1/run_reproduce.py` | 1,331 | `47384a122ae8c5b6` | #!/usr/bin/env python3 |
| `reviewers/r849-1/mutants-if1.log` | 4,593 | `3611edba8b784db1` | head 7a2def7c (clean clone); R849-1's r849_drive.py mutants, 1 interface(s) |
| `reviewers/r849-1/mutants-if2.log` | 14,610 | `ab0d31b2fc7cf60e` | head 7a2def7c (clean clone); R849-1's r849_drive.py mutants, 2 interface(s) |
| `reviewers/r849-1/probes-if1.log` | 4,003 | `d06996882819a65e` | head 7a2def7c (clean clone); R849-1's r849_drive.py probes, 1 interface(s) |
| `reviewers/r849-1/probes-if2.log` | 4,493 | `8c546776c9872f38` | head 7a2def7c (clean clone); R849-1's r849_drive.py probes, 2 interface(s) |
| `reviewers/r849-1/probes-renew-if1.log` | 8,263 | `842cc6f1981c7f7f` | head 7a2def7c (clean clone); R849-1's r849_drive.py probes with its plant r849-renew-not-recorded, 1 |
| `reviewers/r849-1/probes-renew-if2.log` | 8,751 | `8167759ec8e4f40f` | head 7a2def7c (clean clone); R849-1's r849_drive.py probes with its plant r849-renew-not-recorded, 2 |
| `reviewers/r850-1/probes-if1.log` | 828 | `2ffd991424de2249` | head 7a2def7c (clean clone); R850-1's packet script (copied), --interfaces 1; rc 0 |
| `reviewers/r850-1/probes-if2.log` | 828 | `ff6c9b1b187000f5` | head 7a2def7c (clean clone); R850-1's packet script (copied), --interfaces 2; rc 0 |
| `reviewers/r850-1/rebind-if1.log` | 767 | `04d0d3eb66faab10` | head 7a2def7c (clean clone); R850-1's packet script (copied), --interfaces 1; rc 0 |
| `reviewers/r850-1/rebind-if2.log` | 767 | `9dfba265e070a29d` | head 7a2def7c (clean clone); R850-1's packet script (copied), --interfaces 2; rc 0 |
| `reviewers/r850-1/reproduce-if1-srp_mbx.cpp.log` | 1,131 | `ab087e1333811198` | head 7a2def7c (clean clone); R850-1's packet script (copied), --interfaces 1; rc 0 |
| `reviewers/r850-1/reproduce-if1-test_acmp_mbx.cpp.log` | 781 | `6549b4cbdc456cee` | head 7a2def7c (clean clone); R850-1's packet script (copied), --interfaces 1; rc 0 |
| `reviewers/r850-1/reproduce-if2-srp_mbx.cpp.log` | 1,131 | `44ea64492ed795cf` | head 7a2def7c (clean clone); R850-1's packet script (copied), --interfaces 2; rc 0 |
| `reviewers/r850-1/reproduce-if2-test_acmp_mbx.cpp.log` | 781 | `f2bbe049cc3bcc49` | head 7a2def7c (clean clone); R850-1's packet script (copied), --interfaces 2; rc 0 |
| `routes-prior/1x1-AltSpreadLogic_high.txt` | 581 | `803fa7de06dc24c9` | Historical round 1 route; misses at the base, owed to #927 under #925 issuecomment-6908876793. No ro |
| `routes-prior/1x1-ExtraPostPlacementOpt.txt` | 545 | `e063323daa37545d` | Historical round 1 route; misses at the base, owed to #927 under #925 issuecomment-6908876793. No ro |
| `routes-prior/1x1-ExtraTimingOpt.txt` | 538 | `fc5f6c9837e6ae10` | Historical round 1 route; misses at the base, owed to #927 under #925 issuecomment-6908876793. No ro |
| `routes-prior/8x8-AltSpreadLogic_high.txt` | 581 | `ea34ef7fff2dcb7b` | Historical round 1 route; misses at the base, owed to #927 under #925 issuecomment-6908876793. No ro |
| `routes-prior/8x8-ExtraPostPlacementOpt.txt` | 545 | `e3717013c38f7b8f` | Historical round 1 route; misses at the base, owed to #927 under #925 issuecomment-6908876793. No ro |
| `routes-prior/8x8-ExtraTimingOpt.txt` | 576 | `c4f981d8d9e7b510` | Historical round 1 route; misses at the base, owed to #927 under #925 issuecomment-6908876793. No ro |
| `routes-prior/base-1x1-ExtraPostPlacementOpt.txt` | 556 | `b027d2b0f47f49ff` | Historical round 1 route; misses at the base, owed to #927 under #925 issuecomment-6908876793. No ro |
| `routes-prior/base-1x1-ExtraTimingOpt.txt` | 549 | `f1fe3e6c7abea9c0` | Historical round 1 route; misses at the base, owed to #927 under #925 issuecomment-6908876793. No ro |
| `workflows/docs-verify.md` | 12,867 | `cf0386f113086e6a` | head 5f625090; docs.yml, every job replayed step by step on fresh clones (run_wf.py); verify_wf.py r |
| `workflows/docs.log` | 3,909 | `b9737e7de3496c03` | head 5f625090; wf_batch.sh, every docs.yml job (own unit); rc 0 |
| `workflows/elaborate-verify.md` | 8,549 | `17b05747ec26ba8c` | Final head 5f625090: every elaborate run step verified, rc 0 |
| `workflows/elaborate.log` | 1,333 | `39f55216dca0c3d9` | Final head 5f625090: elaborate workflow replay, recorded rc 0 |
| `workflows/rtl-fast-firmware-unit-and-changes.log` | 663 | `b2f58a432a9fdbb7` | head 5f625090; wf_batch.sh rtl-fast.yml:firmware-unit rtl-fast.yml:changes (own unit); rc 0 |
| `workflows/rtl-fast-firmware-unit-and-changes.md` | 2,445 | `50a8f8a8a2137561` | replay verification |
| `workflows/steps/docs__docs-check-no-git__ci_step_1.log` | 355 | `c3b75c70bdf9e5aa` | Workflow step, final head 5f625090; recorded rc 0. Raw log 277 B; sha256 9522d9ffc8c47a207d43a943ba0 |
| `workflows/steps/docs__docs-check-no-git__ci_step_1.sh` | 88 | `0b21a2fb342c14b5` | python3 scripts/ci_runtime_evidence.py identify --output "$RUNNER_TEMP/job-source.json" |
| `workflows/steps/docs__docs-check-no-git__ci_step_2.log` | 333 | `1faf583e84b77456` | Workflow step, final head 5f625090; recorded rc 0. Raw log 255 B; sha256 88add07f1aeae3cc95c43d4ec40 |
| `workflows/steps/docs__docs-check-no-git__ci_step_2.sh` | 446 | `ca8fbe7d4cd44bd9` | set -euo pipefail |
| `workflows/steps/docs__docs-check-no-git__ci_step_3.log` | 573 | `fb8edc630e4bd239` | Workflow step, final head 5f625090; recorded rc 0. Raw log 495 B; sha256 cb1098a3fd198888d80097a2c8f |
| `workflows/steps/docs__docs-check-no-git__ci_step_3.sh` | 82 | `3e686fc2073dff7a` | rm -rf .git |
| `workflows/steps/docs__docs-gates-0__ci_step_1.log` | 473 | `a9bea14b9afbdcf4` | Workflow step, final head 5f625090; recorded rc 0. Raw log 395 B; sha256 e5d979044acb239dbe42a5374c0 |
| `workflows/steps/docs__docs-gates-0__ci_step_1.sh` | 446 | `ca8fbe7d4cd44bd9` | set -euo pipefail |
| `workflows/steps/docs__docs-gates-0__ci_step_21.log` | 929 | `a93af3ee20c56d1f` | Workflow step, final head 5f625090; recorded rc 0. Raw log 998 B; sha256 f1d4a87a3343cd073c5b00f8d6a |
| `workflows/steps/docs__docs-gates-0__ci_step_21.sh` | 86 | `fb79bbfd41608dbb` | git submodule update --init third_party/verilog-axis protocol-processor gptp-processor |
| `workflows/steps/docs__docs-gates-0__ci_step_5.log` | 593 | `4e1c0ae41f4ba572` | Workflow step, final head 5f625090; recorded rc 0. Raw log 515 B; sha256 d85fedeca423d1820f08b720dd9 |
| `workflows/steps/docs__docs-gates-0__ci_step_5.sh` | 37 | `ba2ff42976ef05e2` | python3 -m pip install --quiet pyyaml |
| `workflows/steps/docs__docs-gates-0__ci_step_52.log` | 632 | `b346a325f1d1f390` | Workflow step, final head 5f625090; recorded rc 0. Raw log 603 B; sha256 8d1aaec9d34e2b469926733d7fb |
| `workflows/steps/docs__docs-gates-0__ci_step_52.sh` | 111 | `99b9cc04b998434a` | git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/t |
| `workflows/steps/docs__docs-gates-0__ci_step_7.log` | 593 | `e8be9be1198fbd51` | Workflow step, final head 5f625090; recorded rc 0. Raw log 515 B; sha256 cb5249f7daed8c9eff38edfefb5 |
| `workflows/steps/docs__docs-gates-0__ci_step_7.sh` | 127 | `411af5fe13cf00ce` | python3 -m pip install --quiet --cache-dir ~/.cache/milan-markdown-pip \ |
| `workflows/steps/docs__docs-gates-0__gate_1.log` | 1,385 | `7d63377ce49b8f37` | Workflow step, final head 5f625090; recorded rc 0. Raw log 1400 B; sha256 3c370647bf1036be1b10ae9475 |
| `workflows/steps/docs__docs-gates-0__gate_1.sh` | 243 | `ad6bbe1eb360e18f` | set -euo pipefail |
| `workflows/steps/docs__docs-gates-0__gate_10.log` | 716 | `7e1c5d7d428c3d35` | Workflow step, final head 5f625090; recorded rc 0. Raw log 638 B; sha256 df535b6e4101002d90463759f08 |
| `workflows/steps/docs__docs-gates-0__gate_10.sh` | 182 | `fc0a3ba5a2e09b4f` | python3 docs/DOC_MAP.gen.py --check |
| `workflows/steps/docs__docs-gates-0__gate_11.log` | 623 | `f1990f78aee34134` | Workflow step, final head 5f625090; recorded rc 0. Raw log 545 B; sha256 2fe3d0dc77414c9fc388a38c484 |
| `workflows/steps/docs__docs-gates-0__gate_11.sh` | 89 | `9a3b19048b6518a9` | python3 scripts/check_solution_docs.py |
| `workflows/steps/docs__docs-gates-0__gate_12.log` | 708 | `589db984029ad085` | Workflow step, final head 5f625090; recorded rc 0. Raw log 630 B; sha256 216652a7b431b5988e5a4578ae8 |
| `workflows/steps/docs__docs-gates-0__gate_12.sh` | 210 | `e65b618564ed692d` | python3 docs/diagrams/submodule_boundaries.gen.py --check |
| `workflows/steps/docs__docs-gates-0__gate_13.log` | 717 | `d93de9381339857f` | Workflow step, final head 5f625090; recorded rc 0. Raw log 639 B; sha256 2db37418bcf31612cc90cb84b5d |
| `workflows/steps/docs__docs-gates-0__gate_13.sh` | 330 | `86f93dcb06918aa1` | python3 scripts/gen_wavedrom.py --selftest |
| `workflows/steps/docs__docs-gates-0__gate_14.log` | 595 | `c62ae1c4222a4b19` | Workflow step, final head 5f625090; recorded rc 0. Raw log 517 B; sha256 5342fe99132a8527cc9247b8215 |
| `workflows/steps/docs__docs-gates-0__gate_14.sh` | 87 | `0ab5cb0e4aa2cda2` | python3 scripts/check_diagram_pngs.py |
| `workflows/steps/docs__docs-gates-0__gate_15.log` | 1,982 | `7e82e8545938833d` | Workflow step, final head 5f625090; recorded rc 0. Raw log 1903 B; sha256 132f6865cd1663eeecc3867f34 |
| `workflows/steps/docs__docs-gates-0__gate_15.sh` | 51 | `d147744787d803f1` | python3 scripts/check_feature_status.py --self-test |
| `workflows/steps/docs__docs-gates-0__gate_16.log` | 595 | `d49c288b8998f549` | Workflow step, final head 5f625090; recorded rc 0. Raw log 517 B; sha256 6a6114cbfb1687f6049ba39c2f6 |
| `workflows/steps/docs__docs-gates-0__gate_16.sh` | 54 | `c44e282213a03fa9` | python3 docs/traceability/gen_module_matrix.py --check |
| `workflows/steps/docs__docs-gates-0__gate_18.log` | 3,088 | `4ddb4a75873a37a8` | Workflow step, final head 5f625090; recorded rc 0. Raw log 3009 B; sha256 8af6162e8aca098ac8e869fedc |
| `workflows/steps/docs__docs-gates-0__gate_18.sh` | 80 | `1420bd61cc641c7e` | python3 scripts/check_gptp_docs.py --with-submodule |
| `workflows/steps/docs__docs-gates-0__gate_19.log` | 3,773 | `b30a5833357ec7cb` | Workflow step, final head 5f625090; recorded rc 0. Raw log 3694 B; sha256 86cf0ee3e7ecddde745caaaac3 |
| `workflows/steps/docs__docs-gates-0__gate_19.sh` | 98 | `dffa3e7cd0c9bf0a` | python3 scripts/measure_control_flow.py --selftest |
| `workflows/steps/docs__docs-gates-0__gate_21.log` | 580 | `4a6453f1c09d1237` | Workflow step, final head 5f625090; recorded rc 0. Raw log 502 B; sha256 76b9b9ebf2c009e2eb43ea0d29a |
| `workflows/steps/docs__docs-gates-0__gate_21.sh` | 99 | `43949fc003274d20` | python3 scripts/check_baremetal_only.py --check |
| `workflows/steps/docs__docs-gates-0__gate_24.log` | 51,955 | `57da1c9bafe72330` | Workflow step, final head 5f625090; recorded rc 0. Raw log 51892 B; sha256 fc4344a4b8b8e4592caa33ee1 |
| `workflows/steps/docs__docs-gates-0__gate_24.sh` | 169 | `c662dbf247464e23` | set -euo pipefail |
| `workflows/steps/docs__docs-gates-0__gate_26.log` | 12,773 | `b7cae2377dbbc2e4` | Workflow step, final head 5f625090; recorded rc 0. Raw log 12693 B; sha256 b47d1f546498ab7e4e8bf1fa0 |
| `workflows/steps/docs__docs-gates-0__gate_26.sh` | 272 | `acbe79a888534ce7` | python3 scripts/check_nvm_record_space.py |
| `workflows/steps/docs__docs-gates-0__gate_27.log` | 883 | `545f12311477ae5a` | Workflow step, final head 5f625090; recorded rc 0. Raw log 805 B; sha256 26ab97b254de951e24f6a321d0a |
| `workflows/steps/docs__docs-gates-0__gate_27.sh` | 36 | `cd8ab4f663ae0f13` | python3 scripts/check_nvm_capture.py |
| `workflows/steps/docs__docs-gates-0__gate_28.log` | 26,626 | `292473e450d3d142` | Workflow step, final head 5f625090; recorded rc 0. Raw log 26546 B; sha256 e91c9dffcba304b6057d72732 |
| `workflows/steps/docs__docs-gates-0__gate_28.sh` | 65 | `acdd5be67ef5c2f5` | python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test |
| `workflows/steps/docs__docs-gates-0__gate_29.log` | 5,302 | `242c052e55019388` | Workflow step, final head 5f625090; recorded rc 0. Raw log 5223 B; sha256 38d7db7bd747f459bde8047132 |
| `workflows/steps/docs__docs-gates-0__gate_29.sh` | 238 | `17ac8ee0681d5864` | python3 scripts/check_soc_sources.py |
| `workflows/steps/docs__docs-gates-0__gate_30.log` | 3,924 | `2f986a8af177b71e` | Workflow step, final head 5f625090; recorded rc 0. Raw log 3845 B; sha256 0ce8a9c4a465d6181c040051b7 |
| `workflows/steps/docs__docs-gates-0__gate_30.sh` | 95 | `bc702efe072ebe61` | python3 scripts/check_rtl_source_lists.py |
| `workflows/steps/docs__docs-gates-0__gate_31.log` | 41,073 | `2d738948f92b2d8a` | Workflow step, final head 5f625090; recorded rc 0. Raw log 40993 B; sha256 0fbceca4b453ee979c91df0c3 |
| `workflows/steps/docs__docs-gates-0__gate_31.sh` | 87 | `5cda07bbdccdeaec` | python3 scripts/measure_naming.py --check |
| `workflows/steps/docs__docs-gates-0__gate_32.log` | 5,503 | `4d0f0d4478c7d74b` | Workflow step, final head 5f625090; recorded rc 0. Raw log 5424 B; sha256 34199ec467bdb792e882252cdb |
| `workflows/steps/docs__docs-gates-0__gate_32.sh` | 91 | `0bcc27a61b65ba48` | python3 scripts/check_port_contracts.py |
| `workflows/steps/docs__docs-gates-0__gate_33.log` | 13,049 | `d0688d42071deee6` | Workflow step, final head 5f625090; recorded rc 0. Raw log 12969 B; sha256 479bfce5c633ce4e6183416d3 |
| `workflows/steps/docs__docs-gates-0__gate_33.sh` | 93 | `b4bf12519b4043cd` | python3 scripts/measure_fail_fast.py --check |
| `workflows/steps/docs__docs-gates-0__gate_34.log` | 3,209 | `115d1d1e5d3af5c6` | Workflow step, final head 5f625090; recorded rc 0. Raw log 3130 B; sha256 71c70123f6cc73dcc704ed325c |
| `workflows/steps/docs__docs-gates-0__gate_34.sh` | 91 | `13d51fd1cbcb2d0b` | python3 scripts/check_todo_ownership.py |
| `workflows/steps/docs__docs-gates-0__gate_35.log` | 29,251 | `afada2ef673327f1` | Workflow step, final head 5f625090; recorded rc 0. Raw log 29171 B; sha256 746ff7019ccffa74caeacc370 |
| `workflows/steps/docs__docs-gates-0__gate_35.sh` | 101 | `e40e92eb3fe34ff8` | python3 scripts/measure_test_evidence.py --check |
| `workflows/steps/docs__docs-gates-0__gate_36.log` | 4,443 | `5c24c614d0a73131` | Workflow step, final head 5f625090; recorded rc 0. Raw log 4364 B; sha256 a0976fabf77d856aa766380886 |
| `workflows/steps/docs__docs-gates-0__gate_36.sh` | 85 | `ddae99cc3c93153b` | python3 scripts/check_hygiene.py --check |
| `workflows/steps/docs__docs-gates-0__gate_37.log` | 3,642 | `37d7a569be7a6512` | Workflow step, final head 5f625090; recorded rc 0. Raw log 3563 B; sha256 209b619b1cb8532dd952fe2cf1 |
| `workflows/steps/docs__docs-gates-0__gate_37.sh` | 79 | `18adc03418636df9` | python3 scripts/check_sv_idiom.py |
| `workflows/steps/docs__docs-gates-0__gate_38.log` | 4,374 | `83ee605d516b9a7a` | Workflow step, final head 5f625090; recorded rc 0. Raw log 4295 B; sha256 376b55a8540f2edbb58a5c8995 |
| `workflows/steps/docs__docs-gates-0__gate_38.sh` | 81 | `18b86bebcf288133` | python3 scripts/check_cpp_idiom.py |
| `workflows/steps/docs__docs-gates-0__gate_39.log` | 3,454 | `dacd77ddec1a1488` | Workflow step, final head 5f625090; recorded rc 0. Raw log 3375 B; sha256 ffd7e1800650bb605db1af49e2 |
| `workflows/steps/docs__docs-gates-0__gate_39.sh` | 79 | `48ef3a9a724268d1` | python3 scripts/check_py_idiom.py |
| `workflows/steps/docs__docs-gates-0__gate_40.log` | 3,157 | `786f9add8f0f8576` | Workflow step, final head 5f625090; recorded rc 0. Raw log 3078 B; sha256 50da088a4ccbc0422c0a4c3cd3 |
| `workflows/steps/docs__docs-gates-0__gate_40.sh` | 79 | `a8e3b8f78ec34398` | python3 scripts/check_sh_idiom.py |
| `workflows/steps/docs__docs-gates-0__gate_43.log` | 564 | `e7787f01141ee17f` | Workflow step, final head 5f625090; recorded rc 0. Raw log 486 B; sha256 79cefdbc688bab9674385a40a9e |
| `workflows/steps/docs__docs-gates-0__gate_43.sh` | 34 | `75caa85822c37db5` | python3 scripts/check_doc_paths.py |
| `workflows/steps/docs__docs-gates-0__gate_44.log` | 594 | `c63184f0531ac835` | Workflow step, final head 5f625090; recorded rc 0. Raw log 516 B; sha256 67d89278b8805c43ca955f04fa9 |
| `workflows/steps/docs__docs-gates-0__gate_44.sh` | 77 | `6c9605a3490fd7d5` | python3 scripts/check_archive.py |
| `workflows/steps/docs__docs-gates-0__gate_45.log` | 662 | `fe968350ddc5f86e` | Workflow step, final head 5f625090; recorded rc 0. Raw log 584 B; sha256 0e851cf6a4e21dc3b33dd9946ac |
| `workflows/steps/docs__docs-gates-0__gate_45.sh` | 117 | `16edb17647fcca6d` | python3 scripts/gen_toc.py --selftest |
| `workflows/steps/docs__docs-gates-0__gate_46.log` | 4,070 | `f67a4284e4803509` | Workflow step, final head 5f625090; recorded rc 0. Raw log 3991 B; sha256 a23ff5eec7a79c3f8e9873ad94 |
| `workflows/steps/docs__docs-gates-0__gate_46.sh` | 43 | `b8e244f65d840bcc` | python3 avdecc/gen_aem_store.py --self-test |
| `workflows/steps/docs__docs-gates-0__gate_47.log` | 20,206 | `bd856259d0846451` | Workflow step, final head 5f625090; recorded rc 0. Raw log 20194 B; sha256 97bcc218bda75234d29636223 |
| `workflows/steps/docs__docs-gates-0__gate_47.sh` | 48 | `efac7c7666b78589` | python3 scripts/check_sweep_shape.py --self-test |
| `workflows/steps/docs__docs-gates-0__gate_48.log` | 9,760 | `c7659f34fad26458` | Workflow step, final head 5f625090; recorded rc 0. Raw log 9715 B; sha256 ee945efaa2976cc816ea6dc0e5 |
| `workflows/steps/docs__docs-gates-0__gate_48.sh` | 49 | `74c060bfb313f3f8` | python3 scripts/check_deploy_shape.py --self-test |
| `workflows/steps/docs__docs-gates-0__gate_49.log` | 28,199 | `3de0141c10d6e1a2` | Workflow step, final head 5f625090; recorded rc 0. Raw log 28136 B; sha256 f9e4faf7d691ea61dbc9977ca |
| `workflows/steps/docs__docs-gates-0__gate_49.sh` | 49 | `85ee6241773d6c40` | python3 scripts/check_entity_shape.py --self-test |
| `workflows/steps/docs__docs-gates-0__gate_50.log` | 136,077 | `2096eb805664ed48` | Workflow step, final head 5f625090; recorded rc 0. Raw log 136074 B; sha256 b82546c9d97b6978af873a29 |
| `workflows/steps/docs__docs-gates-0__gate_50.sh` | 626 | `371a9e414ab83635` | python3 scripts/ci_gate_workflows.py --check |
| `workflows/steps/docs__docs-gates-0__gate_7.log` | 627 | `a9f19201a8801fc0` | Workflow step, final head 5f625090; recorded rc 0. Raw log 549 B; sha256 2c110f9661ead1c05efb3bbddc1 |
| `workflows/steps/docs__docs-gates-0__gate_7.sh` | 29 | `95adb94b38a49ec4` | python3 scripts/docs_check.py |
| `workflows/steps/docs__docs-gates-0__gate_8.log` | 605 | `5ced2bc3183ccca1` | Workflow step, final head 5f625090; recorded rc 0. Raw log 527 B; sha256 9df95d32eb8964838858dd06194 |
| `workflows/steps/docs__docs-gates-0__gate_8.sh` | 632 | `5a170d73d69d41dc` | set -euo pipefail |
| `workflows/steps/docs__docs-gates-0__gate_9.log` | 645 | `0efc35d1f132779b` | Workflow step, final head 5f625090; recorded rc 0. Raw log 567 B; sha256 f88b5366b177f7e11f650d2425b |
| `workflows/steps/docs__docs-gates-0__gate_9.sh` | 162 | `a4a9e8e04e33cd7f` | python3 scripts/check_doc_style.py |
| `workflows/steps/docs__docs-gates-1__ci_step_1.log` | 473 | `825b2fc3f9908db5` | Workflow step, final head 5f625090; recorded rc 0. Raw log 395 B; sha256 99bcf87287b45b0dc36aa7cbb27 |
| `workflows/steps/docs__docs-gates-1__ci_step_1.sh` | 446 | `ca8fbe7d4cd44bd9` | set -euo pipefail |
| `workflows/steps/docs__docs-gates-1__ci_step_3.log` | 593 | `1a681a65eb2ef3da` | Workflow step, final head 5f625090; recorded rc 0. Raw log 515 B; sha256 e09e92b4cfc712525d399a38942 |
| `workflows/steps/docs__docs-gates-1__ci_step_3.sh` | 37 | `ba2ff42976ef05e2` | python3 -m pip install --quiet pyyaml |
| `workflows/steps/docs__docs-gates-1__ci_step_5.log` | 593 | `cac0c03d7e336212` | Workflow step, final head 5f625090; recorded rc 0. Raw log 515 B; sha256 c5116c06ca55926ea8eb2eef514 |
| `workflows/steps/docs__docs-gates-1__ci_step_5.sh` | 127 | `411af5fe13cf00ce` | python3 -m pip install --quiet --cache-dir ~/.cache/milan-markdown-pip \ |
| `workflows/steps/docs__docs-gates-1__ci_step_9.log` | 928 | `ce75a1f807669359` | Workflow step, final head 5f625090; recorded rc 0. Raw log 997 B; sha256 1d5912fc5998d10589f1ed69d2e |
| `workflows/steps/docs__docs-gates-1__ci_step_9.sh` | 86 | `fb79bbfd41608dbb` | git submodule update --init third_party/verilog-axis protocol-processor gptp-processor |
| `workflows/steps/docs__docs-gates-1__gate_25_0.log` | 51,009 | `d881589a3fab554a` | Workflow step, final head 5f625090; recorded rc 0. Raw log 50950 B; sha256 2808fd59062fdb7c4d37dbeac |
| `workflows/steps/docs__docs-gates-1__gate_25_0.sh` | 189 | `0d27cfd051375e97` | python3 -m pip install --quiet pyyaml |
| `workflows/steps/docs__docs-gates-2__ci_step_1.log` | 473 | `a22847fc36b92ebd` | Workflow step, final head 5f625090; recorded rc 0. Raw log 395 B; sha256 f637cb206e412da1adfa2355591 |
| `workflows/steps/docs__docs-gates-2__ci_step_1.sh` | 446 | `ca8fbe7d4cd44bd9` | set -euo pipefail |
| `workflows/steps/docs__docs-gates-2__ci_step_3.log` | 593 | `0416baa2d104ff8a` | Workflow step, final head 5f625090; recorded rc 0. Raw log 515 B; sha256 8def72403de177ab1a0e41ae299 |
| `workflows/steps/docs__docs-gates-2__ci_step_3.sh` | 37 | `ba2ff42976ef05e2` | python3 -m pip install --quiet pyyaml |
| `workflows/steps/docs__docs-gates-2__ci_step_5.log` | 593 | `bb0d1b6493dc9e92` | Workflow step, final head 5f625090; recorded rc 0. Raw log 515 B; sha256 17b76a18b4b730386ac1f165e40 |
| `workflows/steps/docs__docs-gates-2__ci_step_5.sh` | 127 | `411af5fe13cf00ce` | python3 -m pip install --quiet --cache-dir ~/.cache/milan-markdown-pip \ |
| `workflows/steps/docs__docs-gates-2__ci_step_9.log` | 928 | `1ca7699f80253d21` | Workflow step, final head 5f625090; recorded rc 0. Raw log 997 B; sha256 e6501db1d95c29a3d9caf66dbd6 |
| `workflows/steps/docs__docs-gates-2__ci_step_9.sh` | 86 | `fb79bbfd41608dbb` | git submodule update --init third_party/verilog-axis protocol-processor gptp-processor |
| `workflows/steps/docs__docs-gates-2__gate_25_1.log` | 76,734 | `d99bb325e38787ad` | Workflow step, final head 5f625090; recorded rc 0. Raw log 76722 B; sha256 3e78d352282b2e16fb14268f6 |
| `workflows/steps/docs__docs-gates-2__gate_25_1.sh` | 189 | `b17972a73531d972` | python3 -m pip install --quiet pyyaml |
| `workflows/steps/docs__docs-gates-2__gate_41.log` | 7,092 | `897ac63cd8b3fef5` | Workflow step, final head 5f625090; recorded rc 0. Raw log 350371 B; sha256 cb0d022dba0d16089f9c8c26 |
| `workflows/steps/docs__docs-gates-2__gate_41.sh` | 77 | `0704860d0056e4df` | python3 scripts/ci_events.py --check |
| `workflows/steps/docs__docs-gates-2__gate_42.log` | 123,892 | `e5cf8a3c8de3a323` | Workflow step, final head 5f625090; recorded rc 0. Raw log 124003 B; sha256 7e4ed0fc106984d2e865e36a |
| `workflows/steps/docs__docs-gates-2__gate_42.sh` | 235 | `0fb3835d1be8537d` | python3 scripts/act_ci.py --selftest |
| `workflows/steps/docs__wire-accountability__ci_step_1.log` | 487 | `bb53567fa40812ec` | Workflow step, final head 5f625090; recorded rc 0. Raw log 409 B; sha256 91ef0fced8be02ba92d11a66b22 |
| `workflows/steps/docs__wire-accountability__ci_step_1.sh` | 446 | `ca8fbe7d4cd44bd9` | set -euo pipefail |
| `workflows/steps/docs__wire-accountability__ci_step_3.log` | 657 | `eeaec471153b07eb` | Workflow step, final head 5f625090; recorded rc 0. Raw log 628 B; sha256 044a0f92f245002d796916b12f5 |
| `workflows/steps/docs__wire-accountability__ci_step_3.sh` | 42 | `e004752016f40a21` | git submodule update --init gptp-processor |
| `workflows/steps/docs__wire-accountability__ci_step_4.log` | 5,597 | `8ea1ecbee6b66c44` | Workflow step, final head 5f625090; recorded rc 0. Raw log 5518 B; sha256 c2bf48cd3f415acc32d15293f3 |
| `workflows/steps/docs__wire-accountability__ci_step_4.sh` | 95 | `d193fa3d83dd2fc2` | python3 -m pip install --quiet pyyaml |
| `workflows/steps/elaborate__elaborate-gates-0__ci_step_1.log` | 491 | `886cd04e5be72261` | Workflow step, final head 5f625090; recorded rc 0. Raw log 405 B; sha256 74aa7acc7db30d3ee0faba96c05 |
| `workflows/steps/elaborate__elaborate-gates-0__ci_step_1.sh` | 446 | `ca8fbe7d4cd44bd9` | set -euo pipefail |
| `workflows/steps/elaborate__elaborate-gates-0__ci_step_4.log` | 991 | `41937b23dbaf1e70` | Workflow step, final head 5f625090; recorded rc 0. Raw log 1051 B; sha256 4c95daea8f623f614a2ee9d691 |
| `workflows/steps/elaborate__elaborate-gates-0__ci_step_4.sh` | 86 | `fb79bbfd41608dbb` | git submodule update --init third_party/verilog-axis protocol-processor gptp-processor |
| `workflows/steps/elaborate__elaborate-gates-0__gate_15_0.log` | 51,135 | `cf9335046f7d21ec` | Workflow step, final head 5f625090; recorded rc 0. Raw log 51068 B; sha256 67ff9d1885639406c26aefae3 |
| `workflows/steps/elaborate__elaborate-gates-0__gate_15_0.sh` | 173 | `fd5cea06688cb68e` | python3 scripts/ci_builder_legs.py run 0 --receipt "$RUNNER_TEMP/gate-results/builder-leg-0.json" -- |
| `workflows/steps/elaborate__elaborate-gates-0__scope.log` | 18,390 | `65e1efccbfdafe47` | Workflow step, final head 5f625090; recorded rc 0. Raw log 18302 B; sha256 3fc8f81315dc9d4391d45f559 |
| `workflows/steps/elaborate__elaborate-gates-0__scope.sh` | 1,092 | `f227980e08b9cc03` | set -euo pipefail |
| `workflows/steps/elaborate__elaborate-gates-1__ci_step_1.log` | 491 | `65b920e94e1c93f3` | Workflow step, final head 5f625090; recorded rc 0. Raw log 405 B; sha256 384aac4e8747b44147a1e24fff9 |
| `workflows/steps/elaborate__elaborate-gates-1__ci_step_1.sh` | 446 | `ca8fbe7d4cd44bd9` | set -euo pipefail |
| `workflows/steps/elaborate__elaborate-gates-1__ci_step_23.log` | 655 | `46c5525a305c641a` | Workflow step, final head 5f625090; recorded rc 0. Raw log 579 B; sha256 f4f450f1c15c81300f86326386e |
| `workflows/steps/elaborate__elaborate-gates-1__ci_step_23.sh` | 211 | `84ac6f23bb66a729` | set -euo pipefail |
| `workflows/steps/elaborate__elaborate-gates-1__ci_step_4.log` | 991 | `f1c50d73eaa9ce0b` | Workflow step, final head 5f625090; recorded rc 0. Raw log 1051 B; sha256 eec7713793b3d4ac0cdd04f5f6 |
| `workflows/steps/elaborate__elaborate-gates-1__ci_step_4.sh` | 86 | `fb79bbfd41608dbb` | git submodule update --init third_party/verilog-axis protocol-processor gptp-processor |
| `workflows/steps/elaborate__elaborate-gates-1__gate_15_1.log` | 83,183 | `15c141e1b069d646` | Workflow step, final head 5f625090; recorded rc 0. Raw log 83761 B; sha256 8c8ad724a8987467fd85dabe3 |
| `workflows/steps/elaborate__elaborate-gates-1__gate_15_1.sh` | 173 | `757de7b0a7229b34` | python3 scripts/ci_builder_legs.py run 1 --receipt "$RUNNER_TEMP/gate-results/builder-leg-1.json" -- |
| `workflows/steps/elaborate__elaborate-gates-1__gate_19.log` | 1,707 | `d5dabb70ee3504b6` | Workflow step, final head 5f625090; recorded rc 0. Raw log 1637 B; sha256 f3623c93aa437423974511891b |
| `workflows/steps/elaborate__elaborate-gates-1__gate_19.sh` | 93 | `3735a1d6323d2df3` | scripts/run_litex_sims.sh --selftest |
| `workflows/steps/elaborate__elaborate-gates-1__scope.log` | 18,390 | `6ea5c1184ddbe476` | Workflow step, final head 5f625090; recorded rc 0. Raw log 18302 B; sha256 04c28f00bc6eaed2d991f47e7 |
| `workflows/steps/elaborate__elaborate-gates-1__scope.sh` | 1,092 | `f227980e08b9cc03` | set -euo pipefail |
| `workflows/steps/rtl-fast__changes__ci_step_1.log` | 321 | `ed31d5c3fc1ea894` | Workflow step, final head 5f625090; recorded rc 0. Raw log 243 B; sha256 be3535618fcc07d6617f23ce1e4 |
| `workflows/steps/rtl-fast__changes__ci_step_1.sh` | 446 | `ca8fbe7d4cd44bd9` | set -euo pipefail |
| `workflows/steps/rtl-fast__changes__scope.log` | 18,288 | `adf41c0f67d3b2b7` | Workflow step, final head 5f625090; recorded rc 0. Raw log 18208 B; sha256 6f54c09045626a5da86959b6a |
| `workflows/steps/rtl-fast__changes__scope.sh` | 1,243 | `fb8b830cdd4ebd7f` | set -euo pipefail |
| `workflows/steps/rtl-fast__firmware-unit__ci_step_1.log` | 483 | `98fa0bdb471f5b65` | Workflow step, final head 5f625090; recorded rc 0. Raw log 405 B; sha256 3bfa2aced870e27ec6a960e5a27 |
| `workflows/steps/rtl-fast__firmware-unit__ci_step_1.sh` | 446 | `ca8fbe7d4cd44bd9` | set -euo pipefail |
| `workflows/steps/rtl-fast__firmware-unit__ci_step_10.log` | 89,024 | `0409dafc9f41ef5e` | Workflow step, final head 5f625090; recorded rc 0. Raw log 92687 B; sha256 5e758cfb7f4cd309a2e33d6b0 |
| `workflows/steps/rtl-fast__firmware-unit__ci_step_10.sh` | 197 | `bac3f16c44b3a8cf` | set -euo pipefail |
| `workflows/steps/rtl-fast__firmware-unit__ci_step_11.log` | 5,331 | `ec8d86e8465e516f` | Workflow step, final head 5f625090; recorded rc 0. Raw log 5252 B; sha256 36cbf4b39e1cd934961a10eb6d |
| `workflows/steps/rtl-fast__firmware-unit__ci_step_11.sh` | 92 | `ec38f881704d1bb3` | python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs "$CI_CAMPAIGN_JOBS" |
| `workflows/steps/rtl-fast__firmware-unit__ci_step_12.log` | 9,619 | `8ae2ab290fb9c780` | Workflow step, final head 5f625090; recorded rc 0. Raw log 9540 B; sha256 189fa4d9007663e94de024c63d |
| `workflows/steps/rtl-fast__firmware-unit__ci_step_12.sh` | 146 | `33b0a14a6e60f5cf` | set -euo pipefail |
| `workflows/steps/rtl-fast__firmware-unit__ci_step_3.log` | 1,251 | `e8a4b0555f4e6b25` | Workflow step, final head 5f625090; recorded rc 0. Raw log 1417 B; sha256 138b76772fa34d660fd51f68ec |
| `workflows/steps/rtl-fast__firmware-unit__ci_step_3.sh` | 128 | `09f28ffac18c1a00` | git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/l |
| `workflows/steps/rtl-fast__firmware-unit__ci_step_7.log` | 2,492 | `71a88a43aab5c043` | Workflow step, final head 5f625090; recorded rc 0. Raw log 2413 B; sha256 27d52cef42077d04816cd03bb3 |
| `workflows/steps/rtl-fast__firmware-unit__ci_step_7.sh` | 43 | `f4106601f0439680` | python3 sw/firmware/gtest/tally_selftest.py |
