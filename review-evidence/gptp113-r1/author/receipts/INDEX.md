# Receipts

Host paths are replaced by `<scratch>`, `<consumer>`, `<gptp>`, `<tools>`, `<logs>` and similar placeholders.

| Receipt | Bytes | sha256 (16) | First line |
|---|---:|---|---|
| `logs/README.txt` | 2,155 | `c44bb240efed37dc` | # what each receipt is (gptp113: FPGA-gPTP issue 113, branch 113-runner-ratchets, head af11b3ef631eb44cdc1730c |
| `logs/ast-pass_run.log` | 139 | `d434acbb604b6bf4` | SAME program apart from docstrings: <scratch>/wt-base/tb/verilator/engine/pass_run.py vs <scratch>/wt-head/tb/ |
| `logs/branch/0001-Document-and-annotate-the-engine-runner-s-public-fun.patch` | 4,578 | `88c15ca1794bbb5a` | From f3b24f3cf5624d3ba88a910a9243ab0bb6de6811 Mon Sep 17 00:00:00 2001 |
| `logs/branch/0002-Move-the-engine-passes-test-to-tb-beside-the-mutatio.patch` | 6,964 | `a79e584763922a3b` | From af11b3ef631eb44cdc1730cfb31bedda95c33dc5 Mon Sep 17 00:00:00 2001 |
| `logs/clock-sites-3009.log` | 984 | `9a21149f1cb56d5b` | uses_wall_clock: True |
| `logs/consumer-ratchets-af11b3e.log` | 28,180 | `8553f219156a7421` | # consumer dev-soft-core c34e7d8b + local commit f791fdea1f: gptp-processor gitlink -> af11b3ef631eb44cdc1730c |
| `logs/donor-idiom-fix.patch.checked` | 6,075 | `2553a8962f768053` | diff --git a/tb/verilator/engine/pass_run.py b/tb/verilator/engine/pass_run.py |
| `logs/engine/base/dirty` | 0 | `e3b0c44298fc1c14` | (empty) |
| `logs/engine/base/head` | 41 | `1920d88eea4f48e5` | 3009f9a2a2d69375211d8355490675879033d940 |
| `logs/engine/base/log` | 18,743 | `cf051c7fce5772cf` | python3 ../../../hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex |
| `logs/engine/base/result` | 74 | `d2abe5fcd4aad201` | rc=0 wall=175.276255485 s verilator=Verilator 5.050 2026-07-01 rev v5.050 |
| `logs/engine/base-abort/dirty` | 36 | `e5c795f74a823990` |  M tb/verilator/engine/sim_main.cpp |
| `logs/engine/base-abort/head` | 41 | `1920d88eea4f48e5` | 3009f9a2a2d69375211d8355490675879033d940 |
| `logs/engine/base-abort/log` | 9,133 | `93e1fb188a910f54` | python3 ../../../hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex |
| `logs/engine/base-abort/result` | 74 | `a1125dfa7568bc5f` | rc=2 wall=181.509588062 s verilator=Verilator 5.050 2026-07-01 rev v5.050 |
| `logs/engine/base-abort.norm` | 5,554 | `2239a01f1d812f72` | python3 ../../../hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex |
| `logs/engine/base.norm` | 15,194 | `14e2c33c7a9046a5` | python3 ../../../hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex |
| `logs/engine/compare.txt` | 505 | `48433949b01d61b7` | base vs head: IDENTICAL (179 normalised lines of 187) |
| `logs/engine/head/dirty` | 0 | `e3b0c44298fc1c14` | (empty) |
| `logs/engine/head/head` | 41 | `29251c78a9b263ec` | af11b3ef631eb44cdc1730cfb31bedda95c33dc5 |
| `logs/engine/head/log` | 18,743 | `ddce179e68760dc5` | python3 ../../../hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex |
| `logs/engine/head/result` | 74 | `c63089c99bee30b0` | rc=0 wall=174.015961492 s verilator=Verilator 5.050 2026-07-01 rev v5.050 |
| `logs/engine/head-abort/dirty` | 36 | `e5c795f74a823990` |  M tb/verilator/engine/sim_main.cpp |
| `logs/engine/head-abort/head` | 41 | `29251c78a9b263ec` | af11b3ef631eb44cdc1730cfb31bedda95c33dc5 |
| `logs/engine/head-abort/log` | 9,133 | `f40b82bf7d398999` | python3 ../../../hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex |
| `logs/engine/head-abort/result` | 74 | `a2b59c2e36c1fc84` | rc=2 wall=170.006758734 s verilator=Verilator 5.050 2026-07-01 rev v5.050 |
| `logs/engine/head-abort.norm` | 5,554 | `2239a01f1d812f72` | python3 ../../../hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex |
| `logs/engine/head.norm` | 15,194 | `14e2c33c7a9046a5` | python3 ../../../hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex |
| `logs/engine/pass-records.txt` | 934 | `1206b0d355585659` | == base-abort |
| `logs/evidence-3009.log` | 27,225 | `970dd1e3cf2616cf` | RTL suites with an executable mutation or negative arm: 40 of 109 |
| `logs/evidence-af11b3e.log` | 27,295 | `e39e8f9acbb3d044` | RTL suites with an executable mutation or negative arm: 40 of 109 |
| `logs/evidence-base.log` | 27,295 | `e39e8f9acbb3d044` | RTL suites with an executable mutation or negative arm: 40 of 109 |
| `logs/evidence-selftest-af11b3e.log` | 5,900 | `4d5e76a1e949faec` | [PASS] a reachable target running a mutation driver is armed |
| `logs/head-gates/make-contract.log` | 67 | `af509294c405ee52` | python3 tb/check_phc_contract.py |
| `logs/head-gates/make-docs.log` | 2,548 | `20b05009be172e86` | python3 scripts/generate_diagrams.py --check |
| `logs/head-gates/make-lint.log` | 1,525 | `7e571df16c9dadb5` | Verilator 5.050 2026-07-01 rev v5.050 |
| `logs/head-gates/passes-test-2.log` | 6,230 | `1e57e8d76cd3faef` | make: Entering directory '<gptp>/tb/verilator/engine' |
| `logs/head-gates/passes-test-3-ulimit-c0.log` | 6,258 | `362ae56d7eb7ea9e` | make: Entering directory '<gptp>/tb/verilator/engine' |
| `logs/idiom-3009.log` | 1,581 | `db3dd4602f0c15b4` | FAIL: unannotated public function 1 > ratchet 0. New Python complies immediately; see Rule 12 in docs/developm |
| `logs/idiom-af11b3e.log` | 466 | `f69414b8002d65c8` | py idiom: 710 first-party modules, 337983 lines |
| `logs/idiom-base.log` | 466 | `b91e14f6a4e3540d` | py idiom: 707 first-party modules, 337110 lines |
| `logs/idiom-selftest-af11b3e.log` | 2,536 | `68a882038dd04b97` | [PASS] a bare except is a finding |
| `logs/make-contract-r1.log` | 62 | `cdc70d96a542ea1a` | python3 tb/check_phc_contract.py |
| `logs/make-docs-r1.log` | 2,543 | `8d7b1e1e768dc125` | python3 scripts/generate_diagrams.py --check |
| `logs/make-lint-r1.log` | 1,491 | `19a03b38d649559b` | verilator --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \ |
| `logs/passes-test-r1.log` | 6,270 | `5f2dedec57f78b88` | make: Entering directory '<gptp>/tb/verilator/engine' |
| `logs/plants-r1.log` | 6,938 | `f79c54114932177e` | PASS [old] control, no plant: rc=0, 73 PASS, 0 FAIL |
| `tools/ast_same.py` | 865 | `b7b213feb35f9b26` | """Are two Python sources the same program once docstrings are removed? usage: ast_same.py A B""" |
| `tools/clock_sites.py` | 663 | `33355d039f2ae8f0` | """List each line of a file that the consumer's wall-clock rule matches (its own regexes, imported).""" |
| `tools/engine_arm.sh` | 588 | `960422121766ff94` | #!/bin/bash |
| `tools/index_receipts.py` | 2,274 | `6649c7016757db78` | #!/usr/bin/env python3 |
| `tools/plants.py` | 7,688 | `5eb92b902fdd1f5d` | #!/usr/bin/env python3 |
