# Receipts index (#943 round 1)

Generated from the files present by make_index.py. Host paths are replaced by `<lane>`, `<scratch>`, `<home>`, `<tools>` and `<tmp>`. Each row: path, size, sha256 prefix, first line.

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `budget/aecp-record-classes-by-image.txt` | 8808 | `6b4741e7d55d35b0` | # AECP record classes (record_classes.py of the final head 211c1ede: long 975 / 1720, paced 310 / 685, other 2 |
| `budget/answering-every-port-1x1-211c1ede.txt` | 23471 | `88592e4558e7f42b` | # CPU budget harness, --variant answering-every-port, 1x1/1if, head 211c1ede: every observation port answering |
| `budget/answering-every-port-8x8-1if-211c1ede.txt` | 76175 | `4f9a2d6ea8abfeee` | # CPU budget harness, --variant answering-every-port, 8x8/1if, head 211c1ede: every observation port answering |
| `budget/answering-ports-aecp-1x1-211c1ede.txt` | 6485 | `173e50fcd45f329f` | # CPU budget harness, --variant answering-ports --groups aecp,aecp-fanout,aecp-largest-notice,aecp-reboot, 1x1 |
| `budget/answering-ports-aecp-8x8-1if-211c1ede.txt` | 6510 | `71506953597361b2` | # CPU budget harness, --variant answering-ports --groups aecp,aecp-fanout,aecp-largest-notice,aecp-reboot, 8x8 |
| `budget/arm-a-1x1-211c1ede-console.txt` | 18893 | `307c59b404319478` | # CPU budget harness, arm A (the image as linked), 1x1/1if, head 211c1ede: the main run's first 33 groups and  |
| `budget/arm-a-1x1-211c1ede-table.md` | 191542 | `d445a548588ce518` | ### 1x1 |
| `budget/arm-a-8x8-1if-211c1ede-console.txt` | 18895 | `8f02416efb4a79cd` | # CPU budget harness, arm A (the image as linked), 8x8/1if, head 211c1ede: the main run's first 38 groups and  |
| `budget/arm-a-8x8-1if-211c1ede-table.md` | 190289 | `4751f10d6ede1ceb` | ### 8x8-1if |
| `budget/arm-a-aecp-rows-1x1-211c1ede.txt` | 5059 | `baea418f3f69f216` | # arm A at 1x1, head 211c1ede: every path row whose worst instance is an AECP group's (aecp, aecp-fanout, aecp |
| `budget/arm-a-aecp-rows-8x8-1if-211c1ede.txt` | 4223 | `2089a966a4832c3f` | # arm A at 8x8-1if, head 211c1ede: every path row whose worst instance is an AECP group's (aecp, aecp-fanout,  |
| `budget/declaring-face-measurement.txt` | 3645 | `99785c4c3bce2fe8` | # measurement only, never committed: the answering-ports arm with its face stub reporting every STREAM_OUTPUT  |
| `budget/declaring-face.patch.txt` | 900 | `6bbf159fc019d4bb` | diff --git a/tb/verilator/ctrl_service_budget/build.py b/tb/verilator/ctrl_service_budget/build.py |
| `budget/egress-ledger-8x8-1if-211c1ede.txt` | 857 | `9cfb0c9ee6ac8c9d` | # egress_ledger.py --point 8x8-1if over arm A's merged results at 211c1ede |
| `budget/flip-grade-1x1-1if-211c1ede.txt` | 1870 | `6705bacb6f3da736` | # python3 -I flip_grade.py --check --point 1x1/1if at the final head 211c1ede |
| `budget/flip-grade-1x1-1if-paced-325-trial.txt` | 1325 | `761e25948b6afbba` | # a trial only, never committed: 1x1/1if's paced one-row edit restated to 325 us (the rule's answer at c637eb0 |
| `budget/flip-grade-8x8-1if-211c1ede.txt` | 1447 | `efd34da8776d647f` | # python3 -I flip_grade.py --check --point 8x8/1if at the final head 211c1ede |
| `budget/harness-selftests-211c1ede.txt` | 1584 | `f3facd4ae6739ecc` | # the CPU budget harness's own self-tests at the final harness (211c1ede, tb/verilator/ctrl_service_budget): r |
| `budget/record-classes-1x1-211c1ede.txt` | 949 | `147bb5b509c483c5` | # record_classes.py at the final harness (211c1ede) over 1x1/1if's arm A (all 99 groups, merged), answering-po |
| `budget/record-classes-8x8-1if-211c1ede.txt` | 967 | `8102c28586923c45` | # record_classes.py at the final harness (211c1ede) over 8x8/1if's arm A (all 98 groups, merged), answering-po |
| `budget/talker-notices-1x1-211c1ede.txt` | 3567 | `b6ebb3e38250edc0` | # CPU budget harness, --variant talker-notices, 1x1/1if, head 211c1ede: a declared and a withdrawn Talker's ST |
| `budget/talker-notices-8x8-1if-211c1ede.txt` | 3573 | `66e6b9daea8182bf` | # CPU budget harness, --variant talker-notices, 8x8/1if, head 211c1ede: a declared and a withdrawn Talker's ST |
| `docs/docs-workflow-steps-502b041c.txt` | 11907 | `6749ada27f7e5925` | # every run: step of docs.yml's gate jobs (wire-accountability, docs-check-no-git, docs-gates-0, -1, -2), read |
| `docs/docs_steps.py.txt` | 7435 | `2705d1c5e7a6fe5f` | #!/usr/bin/env python3 |
| `firmware/failing-first-1x1-if1.txt` | 1691 | `9e1bad3eb6222284` | # the new App test on the unfixed bridge (the tree as 0839453f plus the test only), 1x1/1if: aecp_arms.py --ap |
| `firmware/failing-first-8x8-if1.txt` | 1420 | `ac2446cfe25d6447` | # the new App test on the unfixed bridge (the tree as 0839453f plus the test only), 8x8/1if: aecp_arms.py --ap |
| `firmware/plants-1x1-if1.txt` | 3918 | `35a865189d1e603a` | # the 14 output plants (aecp_output_mutants.py) at 1x1-if1, each planted alone and the AppOutputs test run (dr |
| `firmware/plants-1x1-if2.txt` | 4101 | `a546fd79c0506900` | # the 14 output plants (aecp_output_mutants.py) at 1x1-if2, each planted alone and the AppOutputs test run (dr |
| `firmware/plants-8x8-if1.txt` | 3913 | `787bc936d114083e` | # the 14 output plants (aecp_output_mutants.py) at 8x8-if1, each planted alone and the AppOutputs test run (dr |
| `gates/boundary-verilator-211c1ede.txt` | 61104 | `4f87d6c6bfce3d0e` | # firmware-verilator: ctrl_boundary.py --require-rv32 --selftest --only verilator on a clean clone of 211c1ede |
| `gates/boundary-without-verilator-head-and-base.txt` | 3072 | `db7699ebb637c277` | # firmware-boundary: ctrl_boundary.py --require-rv32 --selftest --without verilator, the LiteX venv's python3  |
| `gates/firmware-gate-211c1ede-shard0.txt` | 8149 | `49163c9eb8bad11e` | # test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4 on a clean clone of 211c1ede (the fina |
| `gates/firmware-gate-211c1ede-shard1.txt` | 56832 | `d2cbacb87edc92ae` | # test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4 --jobs 4 on a clean clone of 211c1ede (the fina |
| `gates/firmware-gate-211c1ede-shard2.txt` | 35170 | `783d9db01b3d7121` | # test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4 --jobs 4 on a clean clone of 211c1ede (the fina |
| `gates/firmware-gate-211c1ede-shard3.txt` | 66646 | `3e79552f53a87882` | # test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4 --jobs 4 on a clean clone of 211c1ede (the fina |
| `gates/firmware-unit-selftests-211c1ede.txt` | 1703 | `6358d97859668ca8` | # the rest of rtl-fast's firmware jobs on a clean clone of 211c1ede (the final code): firmware-unit's tally an |
| `gates/fw-coverage-211c1ede.txt` | 9915 | `e7c9a5c9a37e6a31` | HEAD 211c1ede start 14:23:52 |
| `gates/fw-coverage-22b4def4-finding.txt` | 10097 | `e7bb98a76ebe9a67` | # fw_coverage.py --check at 22b4def4 (before the output arm's unreachable branch was taken out): the one findi |
| `ledger/plat-ledger-base.txt` | 14904 | `447ab288b205fd7f` | # tb/verilator/ctrl_split_boot/plat_ledger.py on a clean clone (base: 0839453f); image sha256 after it |
| `ledger/plat-ledger-head.txt` | 14903 | `7a2ff5c80a9f64b5` | # tb/verilator/ctrl_split_boot/plat_ledger.py on a clean clone (head 211c1ede); image sha256 after it |
| `ledger/points-base-vs-head.txt` | 997 | `4f4526ce79a5739e` | # the platform image at each ledger point, base 0839453f against head 211c1ede (plat_ledger POINT lines) |
| `memory/test_ctrl_memory-head.txt` | 55849 | `2626cf65da430701` | # python3 sw/litex/test_ctrl_memory.py on a clean clone of the lane head 211c1ede |
| `release/release-image-base-vs-head.txt` | 3304 | `c67d978878a37ab5` | # the release (all-fabric) image, base 0839453f against head 211c1ede: endstation_builder.py, then milan_soc.p |
| `tools/budget.sh.txt` | 789 | `faf5d1842cf24b0a` | #!/usr/bin/env bash |
| `tools/env.sh.txt` | 585 | `463105af3b2e31f5` | # env.sh: the pinned tools for lane 943's harness and image runs (sourced) |
| `tools/launch_base.sh.txt` | 1114 | `2615f4782d39ad8f` | #!/usr/bin/env bash |
| `tools/launch_budget.sh.txt` | 1191 | `a5f6af69aeb33581` | #!/usr/bin/env bash |
| `tools/launch_wip.sh.txt` | 1222 | `ba1c6b60eed5c8ff` | #!/usr/bin/env bash |
| `tools/ledger.sh.txt` | 1214 | `fae2746f2f70b5e7` | #!/usr/bin/env bash |
| `tools/merge_arm.py.txt` | 1491 | `38fbaf3788f30a4b` | """merge_arm.py <main>: every group of the main run's list, its script and log copied into <main>/results-merg |
| `tools/plant_rows.py.txt` | 594 | `50618ee797b0f325` | """Plant only the named AECP rows (aecp_output_mutants) through aecp_mutants' own planting and grading.""" |
| `tools/plant_shapes.py.txt` | 1755 | `64898c4d2da39a8d` | """Plant each aecp_output_mutants row and run the AppOutputs test at one shape and interface count; report the |
| `tools/record_calls.py.txt` | 592 | `087ff6273764b223` | """record_calls.py <group.log> <cycles>: the functions called inside the AECP record span of that many CPU cyc |
| `tools/record_spans.py.txt` | 982 | `7ebd197c86dbde6b` | """record_spans.py <group.log> <cycles>: the AECP record span (aecp_mbx:frame) of that many CPU cycles, and ev |
| `tools/release_image.sh.txt` | 2200 | `8cb84b76d770b637` | #!/usr/bin/env bash |
| `tools/rows_vs.py.txt` | 1065 | `12306eb4e541c970` | """rows_vs.py <train table.md> <head table.md>: each path row of the head's table (worst instance, ms and its  |
| `twin/twin-22b4def4-row-gone.txt` | 2920 | `4bd9bd0ba8871417` | # make -C tb/verilator/milan_dp twin (pinned Verilator 5.050) at 22b4def4, the fix in and the owed row still i |
| `twin/twin-and-plants-211c1ede.txt` | 17207 | `5af5df1a0f65bc70` | # make -C tb/verilator/milan_dp twin, then twin-plants (pinned Verilator 5.050) on a clean clone of 211c1ede ( |
