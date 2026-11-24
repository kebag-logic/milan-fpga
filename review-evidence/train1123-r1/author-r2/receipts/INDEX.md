# Receipts (generated from the files present)

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `budget/kept-grade-1x1-answering-ports-r2.txt` | 2,949 | `742dd06481a34a75` | # python3 -I tb/verilator/ctrl_service_budget/kept_grade.py <1x1 answering-ports build> --results <view of the formal leg's srp-kept and srp-bound logs>, at hea |
| `budget/kept-grade-1x1-arm-A-r2.txt` | 2,918 | `9a560c04009eb35e` | # python3 -I tb/verilator/ctrl_service_budget/kept_grade.py <1x1 arm-A build> --results <view of the formal leg's srp-kept and srp-bound logs>, at head 43076d0f |
| `budget/kept-grade-8x8-1if-answering-ports-r2.txt` | 3,416 | `c13f4127dccecea2` | # python3 -I tb/verilator/ctrl_service_budget/kept_grade.py <8x8-1if answering-ports build> --results <view of the formal leg's srp-kept and srp-bound logs>, at |
| `budget/kept-grade-8x8-1if-arm-A-r2.txt` | 3,138 | `ad8b5ea2a1d8254a` | # python3 -I tb/verilator/ctrl_service_budget/kept_grade.py <8x8-1if arm-A build> --results <view of the formal leg's srp-kept and srp-bound logs>, at head 4307 |
| `budget/kept-grade-planted-r2.txt` | 1,949 | `84512408c289417d` | # python3 -B <scratch>/bin/kept_mutants_r2.py at 43076d0f8c87b5118f6f4317d000a7eebdefc967: ten scratch monkeypatches of kept_grade (not committed), each run thr |
| `budget/kept-grade-selftest-r2.txt` | 2,421 | `e4acbcb046095e0b` | # python3 -I tb/verilator/ctrl_service_budget/kept_grade.py --selftest at 43076d0f8c87b5118f6f4317d000a7eebdefc967 |
| `budget/probe-output-map-largest-command-NOT-COMMITTED.txt` | 4,593 | `55f903f06a3acec4` | # A scratch probe, NOT committed: the answering-ports arm's aecp-largest-notice with the output map's 63-mapping edit (long_notice.groups trying port type 15 be |
| `budget/run-regrade-1x1-answering-ports-r2.txt` | 2,963 | `25684ef308e6c115` | # run.py --point <p> --build-dir <the formal leg's build> --regrade --out <a fresh directory holding copies of that leg's srp-kept and srp-bound .txt and .log>  |
| `budget/run-regrade-1x1-none-r2.txt` | 2,962 | `8bdb010290826d7f` | # run.py --point <p> --build-dir <the formal leg's build> --regrade --out <a fresh directory holding copies of that leg's srp-kept and srp-bound .txt and .log>  |
| `budget/run-regrade-8x8-1if-answering-ports-r2.txt` | 3,746 | `6a1f59fe55463a25` | # run.py --point <p> --build-dir <the formal leg's build> --regrade --out <a fresh directory holding copies of that leg's srp-kept and srp-bound .txt and .log>  |
| `budget/run-regrade-8x8-1if-none-r2.txt` | 3,487 | `f746f7b7346e8326` | # run.py --point <p> --build-dir <the formal leg's build> --regrade --out <a fresh directory holding copies of that leg's srp-kept and srp-bound .txt and .log>  |
| `docs/docs-workflow-steps-43076d0f.txt` | 9,319 | `95e6d4851fc509bb` | # bin/docs_steps_r2.py 43076d0f <root>: every run: step of docs.yml's five gate jobs on a fresh clean clone of the final head, read from the clone's own workflo |
| `docs/step-15-docs-gates-0-Link_health_wording_dead_reference_and_local_inf.log.txt` | 353 | `bef7f10ffb1f9065` | # docs step log 15-docs-gates-0-Link_health_wording_dead_reference_and_local_inf.log at 43076d0f |
| `docs/step-16-docs-gates-0-Added_line_em_dash_gate.log.txt` | 308 | `088755f05e62770a` | # docs step log 16-docs-gates-0-Added_line_em_dash_gate.log at 43076d0f |
| `docs/step-45-docs-gates-0-Python_idiom_gate.log.txt` | 3,147 | `4f8cb3b65ad737d5` | # docs step log 45-docs-gates-0-Python_idiom_gate.log at 43076d0f |
| `gates/ctrl-boundary-43076d0f.txt` | 72,837 | `8230b1ebffb8defa` | # bin/cb.sh: python3 -B sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest on a clean clone of the final head 43076d0f |
| `gates/firmware-gate-inputs-unchanged.txt` | 936 | `559938e7fb2e358e` | # The firmware gate (test_ctrl_firmware.py --require-rv32 --self-test, four shards) is not re-run at 43076d0f: no firmware or test input changed since f5a1585e, |
| `gates/tree-checks-43076d0f.txt` | 70,201 | `d09b7fad77f47d5f` | # bin/tree_checks.sh on a clean clone of the final head 43076d0f: load_grade --check, flip_grade --check at 1x1/1if and 8x8/1if, shape_costs --check, record_cla |
| `ledger/plat-ledger-43076d0f.txt` | 3,658 | `70bba8ac32c01533` | # bin/ledger.sh: python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <fresh build> on a clean clone of the final head, then each image's sha256 ( |
| `merge/merges-r2.txt` | 3,816 | `52bb0d39492f55eb` | # The round-2 merges on f5a1585e, fetched from the public repository |
