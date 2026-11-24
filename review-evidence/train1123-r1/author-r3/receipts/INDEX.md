# Receipts (generated from the files present)

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `budget/kept-grade-1x1-answering-ports-r3.txt` | 2,801 | `4ce11afff7532175` | # python3 -I tb/verilator/ctrl_service_budget/kept_grade.py <1x1-answering-ports build> --results <round 1's view of the leg's srp-kept and srp-bound logs>, at  |
| `budget/kept-grade-1x1-arm-A-r3.txt` | 2,781 | `bc074031c9e02065` | # python3 -I tb/verilator/ctrl_service_budget/kept_grade.py <1x1-none build> --results <round 1's view of the leg's srp-kept and srp-bound logs>, at head adc13d |
| `budget/kept-grade-8x8-1if-answering-ports-r3.txt` | 3,264 | `1173d97d528b8267` | # python3 -I tb/verilator/ctrl_service_budget/kept_grade.py <8x8-1if-answering-ports build> --results <round 1's view of the leg's srp-kept and srp-bound logs>, |
| `budget/kept-grade-8x8-1if-arm-A-r3.txt` | 2,997 | `30af6ba5f3d67c32` | # python3 -I tb/verilator/ctrl_service_budget/kept_grade.py <8x8-1if-none build> --results <round 1's view of the leg's srp-kept and srp-bound logs>, at head ad |
| `budget/kept-grade-planted-r3.txt` | 4,822 | `1c94b0521ba59aea` | # python3 -I -B <scratch>/r3/bin/kept_mutants_r3.py <lane> at head adc13dbdd1241b124c8877f1dda5318c1095e0df: scratch monkeypatches, nothing committed |
| `budget/kept-grade-selftest-r3.txt` | 3,077 | `10ee6e6782a156f9` | # python3 -I -B tb/verilator/ctrl_service_budget/kept_grade.py --selftest at head adc13dbdd1241b124c8877f1dda5318c1095e0df (porcelain 0) |
| `budget/regrade-summary-r3.txt` | 2,605 | `f0010c730a35ab49` | # regrade_r3.sh adc13dbdd1241b124c8877f1dda5318c1095e0df: log sha256s, exit codes and counts per leg |
| `budget/regrade_r3.sh.txt` | 2,203 | `346439e0eed839fe` | #!/bin/bash |
| `budget/run-regrade-1x1-answering-ports-r3.txt` | 2,842 | `72ae0783f11cdf8f` | # run.py --regrade of srp-kept,srp-bound with --record-budget-findings --record-share-findings, from round 1's measurement clone at c2b2ba1a with tb/verilator/c |
| `budget/run-regrade-1x1-none-r3.txt` | 2,830 | `257865a9a27e608e` | # run.py --regrade of srp-kept,srp-bound with --record-budget-findings --record-share-findings, from round 1's measurement clone at c2b2ba1a with tb/verilator/c |
| `budget/run-regrade-8x8-1if-answering-ports-r3.txt` | 3,629 | `a676c0a1fbe8b833` | # run.py --regrade of srp-kept,srp-bound with --record-budget-findings --record-share-findings, from round 1's measurement clone at c2b2ba1a with tb/verilator/c |
| `budget/run-regrade-8x8-1if-none-r3.txt` | 3,359 | `e9226d11b0ff28b7` | # run.py --regrade of srp-kept,srp-bound with --record-budget-findings --record-share-findings, from round 1's measurement clone at c2b2ba1a with tb/verilator/c |
| `docs/docs-workflow-steps-adc13dbd.txt` | 9,425 | `c9f49754519a1b6b` | # bin/docs_steps_r2.py adc13dbd <root> (unit milan-train1123-a828-docs-r3, rc 0): every run: step of docs.yml's five gate jobs on a fresh clean clone of adc13db |
| `gates/ctrl-boundary-adc13dbd.txt` | 72,861 | `21fe8286c3c41edf` | # bin/cb.sh: python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest on clean clone cb at adc13dbd (unit milan-train1123-a828-cb-r3, rc 0) |
| `gates/tree-checks-adc13dbd.txt` | 70,916 | `b57f3b68a76068d9` | # bin/tree_checks.sh on clean clone tc at adc13dbd (unit milan-train1123-a828-tree-r3, rc 0): load_grade --check, flip_grade --check at 1x1/1if and 8x8/1if, sha |
| `harness/probe-whole-build-slice-r3.txt` | 1,302 | `ab91a1364fd8ddbc` | # R911-1's tools/probe_whole_slice.py, unmodified (sha256 b7172b3e8ee2eafc), run on <lane> at head adc13dbdd1241b124c8877f1dda5318c1095e0df |
| `ledger/image-hashes-vs-43076d0f.txt` | 3,617 | `23344f8a28f44f8a` | # The 24 image hashes at adc13dbd against 43076d0f's (round 2's receipt plat-ledger-43076d0f.txt) |
| `ledger/plat-ledger-adc13dbd.txt` | 15,281 | `f8dfbc83fbf3c99b` | # bash ledger.sh <clean clone lg at adc13dbd> <fresh build dir ledger/adc13dbd> (systemd user unit milan-train1123-a828-ledger-r3, CPUs 8-15 booked through cpu_ |
