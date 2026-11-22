# Receipts index (#950 and #954 round 1)

Generated from the files present by make_index.py. Host paths are replaced by `<lane>`, `<scratch>`, `<home>`, `<tools>` and `<tmp>`. Each row: path, size, sha256 prefix, first line.

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `budget/cpu-table-c7cfba76.md` | 19392 | `a63cc8f6bc29bdbf` | # The full CPU re-measure at #950's images (c7cfba76): every arm the harness holds (arm A and each of build.py |
| `budget/egress-ledger-8x8-1if.txt` | 1813 | `e4bf5935641dbda1` | # egress_ledger.py --point 8x8-1if (287ca1ee's harness) over the full re-measure's two parts that run backlog- |
| `budget/flip-grade-1x1-1if-287ca1ee.txt` | 1916 | `376fe4e28b47c22c` | # python3 -I flip_grade.py --check --point 1x1/1if at 287ca1ee (the statements as committed: 1x1/1if's record. |
| `budget/flip-grade-1x1-asis-trial.txt` | 1898 | `d3bc1a08b8bf038a` | # python3 -I flip_grade.py --check --point 1x1/1if at c7cfba76's harness, the statements as the train states t |
| `budget/flip-grade-1x1-other-trial.txt` | 1915 | `a68eab4c4a78280d` | # a trial, not committed: the same with 1x1/1if's record.aecp (load_grade STATED_US and GRADED) restated 250 - |
| `budget/flip-grade-1x1-paced-trial.txt` | 1900 | `9715d71b2d346419` | # a trial, not committed: the same with 1x1/1if's one-row edit (edit_rows.PACED) restated 315 -> 320 us by the |
| `budget/flip-grade-1x1-restated-trial.txt` | 1878 | `bdd6dc5737e862ab` | # a trial, not committed: the same with both restated (record.aecp 255, the one-row edit 320) |
| `budget/flip-grade-8x8-1if-287ca1ee.txt` | 1496 | `4e6f39a177e528d5` | # python3 -I flip_grade.py --check --point 8x8/1if at 287ca1ee (the statements as committed: 1x1/1if's record. |
| `budget/groups-and-findings.txt` | 3030 | `d074e4f61c530a42` | # the full re-measure's parts (c7cfba76): each part's run.py summary line summed per point, then every BUDGET  |
| `budget/harness-selftests-287ca1ee.txt` | 404 | `5ddf489540238a99` | # the CPU budget harness's own self-tests at 287ca1ee's harness (the restated load_grade.py): record_classes.p |
| `budget/image-hashes.txt` | 1861 | `4408d93e64bbce91` | # each arm's CPU-budget image (ctrl_app.elf sha256, 16 hex) at the head's full re-measure (c7cfba76) and the t |
| `budget/layout-search-1x1.txt` | 1526 | `14c6ed04ea800818` | # the core change's code shapes, each the same behaviour, measured at 1x1/1if on the two groups of its tightes |
| `budget/load_grade-check-287ca1ee.txt` | 1840 | `9f816ce59f63a462` | # python3 -I load_grade.py --check at 287ca1ee |
| `budget/record-classes-1x1-287ca1ee.txt` | 4696 | `d21f8b7d05051670` | # record_classes.py at 287ca1ee's harness (record.aecp 255 us, by the rule) over the same 64 parts |
| `budget/record-classes-1x1-c7cfba76-statements.txt` | 4893 | `1bd636bc2cb49490` | # record_classes.py at c7cfba76's harness (record.aecp 250 us) over the 64 parts at 1x1/1if: the class lines;  |
| `budget/record-classes-8x8-1if-c7cfba76.txt` | 4887 | `130ce77f3a6b55ff` | # record_classes.py over the 64 parts at 8x8/1if (no 8x8/1if statement restated; the same at 287ca1ee) |
| `budget/shape_costs-check-287ca1ee.txt` | 668 | `320677d0f942d51d` | # python3 -I shape_costs.py --check at 287ca1ee |
| `budget/survey-1x1-compare-long.txt` | 526 | `3f00f6023d4394b4` | # the same: the largest legal notice against poll_grade's aecp_long |
| `budget/survey-1x1-compare-ordinary.txt` | 11782 | `3bcce47891f3ab32` | # survey_point4.py at 1x1 over the 64 parts at c7cfba76: compare_point.py's table (the head's statements) |
| `budget/survey-8x8-1if-compare-long.txt` | 526 | `906ac249fa67b648` | # the same: the largest legal notice against poll_grade's aecp_long |
| `budget/survey-8x8-1if-compare-ordinary.txt` | 11865 | `8eb04e257cbdbb12` | # survey_point4.py at 8x8-1if over the 64 parts at c7cfba76: compare_point.py's table (the head's statements) |
| `budget/tight-probes-1x1-8x8.txt` | 2421 | `e13db55b2a5b0a67` | # the CPU budget harness's tight statements, probed: each arm built as run.py builds it by default (legs.py bu |
| `docs/docs-workflow-steps-287ca1ee.txt` | 9290 | `b03a3b3febda70af` | # every run: step of docs.yml's gate jobs (wire-accountability, docs-check-no-git, docs-gates-0, -1, -2), read |
| `docs/docs-workflow-steps-a00a3c96.txt` | 9274 | `f02a867048ab8dcc` | # every run: step of docs.yml's gate jobs (wire-accountability, docs-check-no-git, docs-gates-0, -1, -2), read |
| `docs/rv32-sdk-verify-base-15168e14.txt` | 399 | `8874b03a0e30ce51` | # the docs workflow's 'Install and verify the pinned RV32 SDK' step's two commands on a clean clone of the bas |
| `firmware/failing-first-core-1x1-if2.txt` | 1130 | `b461ca81f3d48268` | # the new core test on the unfixed core: base 15168e14 plus the test commit 9ed4fc95 alone; aecp_arms.py --app |
| `firmware/failing-first-platsinks-1x1.txt` | 2311 | `4d8230c11bd531ea` | # the new platform tests (Streams.*, test_plat_sinks.cpp) on the unfixed tree: the base 15168e14 plus the test |
| `firmware/failing-first-platsinks-8x8.txt` | 5522 | `415acbfb94d6993c` | # the new platform tests (Streams.*, test_plat_sinks.cpp) on the unfixed tree: the base 15168e14 plus the test |
| `firmware/plants-aecp-rows.txt` | 1624 | `0cfc0f4e2dca3e01` | # the AECP campaign's rows this lane adds (#950) and the five it re-anchors on the core's new status, each pla |
| `firmware/plants-ctrl-rows.txt` | 2417 | `399d2c2063a8d9eb` | # the control campaign's rows this lane adds (#950, #954) and plat-source-past-count (its anchor's function ch |
| `firmware/plants-reanchored-c7cfba76.txt` | 1118 | `2be9115dab46d142` | # the four rows re-anchored on aecp_again's final body (c7cfba76: the check named by the change the waiting co |
| `gates/boundary-verilator-f90884e6.txt` | 17874 | `5385d41d4e911685` | # firmware-verilator: ctrl_boundary.py --require-rv32 --selftest --only verilator, the LiteX venv's python3, p |
| `gates/boundary-without-verilator-f90884e6.txt` | 27045 | `fc4ebe94f1a41a8b` | # firmware-boundary: ctrl_boundary.py --require-rv32 --selftest --without verilator, the LiteX venv's python3, |
| `gates/firmware-gate-287ca1ee-s0.txt` | 929 | `b4f0626c59446b63` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4 on a cle |
| `gates/firmware-gate-287ca1ee-s1.txt` | 8535 | `4da96c1fe757eb5b` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4 --jobs 4 on a cle |
| `gates/firmware-gate-287ca1ee-s2.txt` | 2826 | `587841a24354513b` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4 --jobs 4 on a cle |
| `gates/firmware-gate-287ca1ee-s3.txt` | 4000 | `6f6d953ed11f9c61` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4 --jobs 4 on a cle |
| `gates/firmware-gate-c7cfba76-s0.txt` | 933 | `40aaa891c0845356` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4 on a cle |
| `gates/firmware-gate-c7cfba76-s1.txt` | 8539 | `85993302b1c4699d` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4 --jobs 4 on a cle |
| `gates/firmware-gate-c7cfba76-s2.txt` | 2830 | `5207bdeb68927e7a` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4 --jobs 4 on a cle |
| `gates/firmware-gate-c7cfba76-s3.txt` | 4004 | `5a24fbcd9eaaa2e8` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4 --jobs 4 on a cle |
| `gates/fw-coverage-c7cfba76.txt` | 13872 | `20fa7f053325d1dc` | # python3 sw/firmware/gtest/fw_coverage.py --selftest, then --check --jobs 4, on a clean clone of c7cfba76 (th |
| `ledger/plat-ledger-4a08c90d.txt` | 15625 | `728bd452e5a96ecf` | # the same on 4a08c90d (the one-interface entry at 58.5 by the owner's rule of 2026-11-15) |
| `ledger/plat-ledger-base-15168e14.txt` | 15801 | `704b96de38f274be` | # tb/verilator/ctrl_split_boot/plat_ledger.py on a clean clone of the base 15168e14 (ledger.sh: the product Li |
| `ledger/plat-ledger-f90884e6-finding.txt` | 16172 | `93063b10a00c0783` | # the same on f90884e6 (the firmware final, the ledger unchanged): the 8x8 one-interface image 40 B past what  |
| `ledger/test-ctrl-memory-a00a3c96.txt` | 17225 | `7919f71264402f73` | # python3 sw/litex/test_ctrl_memory.py (the product LiteX venv) on the tree of a00a3c96: its ledger lines, fai |
| `release/release-image-base-vs-c7cfba76.txt` | 2965 | `5a65303d2f3aace9` | # the release (all-fabric) image, base 15168e14 against head c7cfba76: endstation_builder.py <config>, then mi |
| `tools/analyse.sh.txt` | 1502 | `965bb30fc22df4c0` | #!/bin/bash |
| `tools/cpu_table.py.txt` | 1433 | `1a46c25b8f389a4d` | """cpu_table.py <head compare-ordinary> <base compare-ordinary> <point> <head> <base>: the statement survey's  |
| `tools/docs_steps.py.txt` | 7423 | `0bc35d8170b2f871` | #!/usr/bin/env python3 |
| `tools/ledger.sh.txt` | 1214 | `fae2746f2f70b5e7` | #!/usr/bin/env bash |
| `tools/legs.py.txt` | 3453 | `6da16143cb8dd0c1` | #!/usr/bin/env python3 |
| `tools/make_index.py.txt` | 1555 | `bcade69c9cfc3eb7` | # (receipt copy: the host-path literals this tool scrubs are masked as <data-2>, <data>, <tmp>, <home>) |
| `tools/mchunk.sh.txt` | 1168 | `e7ab9faaa2379ec4` | #!/bin/bash |
| `tools/mqueue.py.txt` | 2490 | `1a3044376e55cafa` | """mqueue.py REV [POINT...]: launch the full re-measure's unit chunks at REV that are not yet launched, one pe |
| `tools/place_again.py.txt` | 1266 | `d8c40a950b5698b3` | """place_again.py <clone> <before>: move aecp_again (its comment and body) in aecp_commands.c of a clean clone |
| `tools/plant_aecp_rows.py.txt` | 794 | `58efa35ed9ac9980` | """plant_aecp_rows.py <test-dir> <out> <name>...: plant only the named rows of aecp_mutants.DEFECTS through th |
| `tools/plant_ctrl_rows.py.txt` | 757 | `e519c13f77f07ac2` | """plant_ctrl_rows.py <test-dir> <out> <name>...: plant only the named rows of ctrl_mutants.MUTANTS through th |
| `tools/release_image.sh.txt` | 2200 | `8cb84b76d770b637` | #!/usr/bin/env bash |
| `tools/run_sinks.py.txt` | 1466 | `5684c058931bb8d0` | """run_sinks.py <tree-root> <out> <shape: 8x8/1x1> [gtest filter]: build the platsinks arm (plat_arms.arm_plat |
| `tools/sanitize.py.txt` | 1206 | `cb5cdc0050c122ca` | # (receipt copy: the host-path literals this tool scrubs are masked as <data-2>, <data>, <tmp>, <home>) |
| `tools/twin.sh.txt` | 459 | `1793af593d2730c4` | #!/bin/bash |
| `twin/twin-and-plants-c7cfba76.txt` | 7971 | `d6517617459b7cae` | # make -C tb/verilator/milan_dp twin, twin-plants, twin-maps, twin-maps-plants -j8 (pinned Verilator 5.050) on |
