# Receipts (generated from the files present)

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `budget/cpu-1x1-1if-formal-c2b2ba1a.md` | 50,526 | `c41fb5d0b618b1c4` | # The formal CPU budget measurement at 1x1 on the composed head c2b2ba1a (clean clone): every arm and every group. |
| `budget/cpu-8x8-1if-formal-c2b2ba1a.md` | 103,283 | `0a776d5f4c4ec482` | # The formal CPU budget measurement at 8x8-1if on the composed head c2b2ba1a (clean clone): every arm and every group. |
| `budget/kept-grade-1x1-c2b2ba1a.txt` | 2,486 | `6973ddc2a8664a48` | # python3 -I tb/verilator/ctrl_service_budget/kept_grade.py <arm A build> --results <view of arm A's srp-kept and srp-bound logs> at 1x1, on the formal measurem |
| `budget/kept-grade-8x8-1if-c2b2ba1a.txt` | 2,800 | `fa4264741def6304` | # python3 -I tb/verilator/ctrl_service_budget/kept_grade.py <arm A build> --results <view of arm A's srp-kept and srp-bound logs> at 8x8-1if, on the formal meas |
| `budget/kept-grade-answering-ports-1x1-c2b2ba1a.txt` | 2,515 | `b8f73f62896b838c` | # python3 -I tb/verilator/ctrl_service_budget/kept_grade.py <answering-ports build> --results <view of the arm's srp-kept and srp-bound logs, which the legs' pa |
| `budget/kept-grade-answering-ports-8x8-1if-c2b2ba1a.txt` | 2,823 | `9aca373540aa6f0f` | # python3 -I tb/verilator/ctrl_service_budget/kept_grade.py <answering-ports build> --results <view of the arm's srp-kept and srp-bound logs, which the legs' pa |
| `budget/probe-output-map-largest-command-NOT-COMMITTED.txt` | 4,593 | `55f903f06a3acec4` | # A scratch probe, NOT committed: the answering-ports arm's aecp-largest-notice with the output map's 63-mapping edit (long_notice.groups trying port type 15 be |
| `budget/tree-checks-f5a1585e.txt` | 89,136 | `a1e9bffd53ad5362` | # On a clean clone of f5a1585e (the final head): load_grade --check, flip_grade --check at 1x1/1if and 8x8/1if, shape_costs --check, record_classes/flip_grade/k |
| `docs/docs-b6b2e603-the-two-findings.txt` | 964 | `994c7ed23d73ed6a` | # the early docs run's two real findings at b6b2e603 (docs_check's bare reference; the Python idiom gate's long module and over-long lines), each step's log tai |
| `docs/docs-workflow-steps-b6b2e603.txt` | 9,516 | `cb2cf676b8936f88` | # every run: step of docs.yml's gate jobs (wire-accountability, docs-check-no-git, docs-gates-0..2), read from the head's own workflow, on a fresh clean clone o |
| `docs/docs-workflow-steps-f5a1585e.txt` | 9,288 | `2757a79fed3fbe41` | # every run: step of docs.yml's gate jobs (wire-accountability, docs-check-no-git, docs-gates-0..2), read from the head's own workflow, on a fresh clean clone o |
| `firmware/builder-c2b2ba1a.txt` | 160,226 | `213f5d74da2ec2d6` | # scripts/ci_builder_legs.py run 0 and run 1 (test_builder.py --require-rv32), then union --workflow docs, on a clean clone of c2b2ba1a (submodule origins at th |
| `firmware/builder-union-c2b2ba1a.json.txt` | 8,770 | `a5622133907d602e` | {"head":"c2b2ba1a4742335e0678ec1f00f9033d1913b1da","inventory":["test_soc_option_refusals","test_commercial_timing_grade","test_baremetal_clock_contract","test_ |
| `firmware/ctrl-boundary-0ad0bf2d-makefile-pin-controls.txt` | 14,981 | `869a12c3cdcd8a41` | # The Makefile targets' pin controls of ctrl_boundary --selftest at 0ad0bf2d (from its log); #948's twin-fanout, twin-fanout-plants, build-twin8-sp, twin8-fw, f |
| `firmware/ctrl-boundary-0ad0bf2d.txt` | 31,421 | `719ec3ee2914a5fc` | # sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest on a clean clone of 0ad0bf2d: the run's lines but each builder's per-command line and the pin |
| `firmware/ctrl-boundary-b6b2e603.txt` | 31,326 | `9b1dd5414fe5c445` | # sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest on a clean clone of b6b2e603: the run's lines but each builder's per-command line and the pin |
| `firmware/ctrl-boundary-c2b2ba1a.txt` | 733 | `ef6675968c7eace3` | # sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest on a clean clone of c2b2ba1a: the run's lines but each builder's per-command line and the pin |
| `firmware/ctrl-boundary-f5a1585e.txt` | 31,343 | `45466722e1e1d56a` | # sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest on a clean clone of f5a1585e (the final head): the run's lines but each builder's per-command |
| `firmware/fw-coverage-c2b2ba1a.txt` | 13,910 | `c3b251ce3ae877ac` | # sw/firmware/gtest/fw_coverage.py --selftest, then --check --jobs 4, on a clean clone of c2b2ba1a |
| `firmware/fw-gate-c2b2ba1a-s0.txt` | 4,573 | `22f57812f8b571fa` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4 on a clean clone of c2b2ba1a (the composed code head): its |
| `firmware/fw-gate-c2b2ba1a-s1.txt` | 162,473 | `f906dfbe55a73a36` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4 --jobs 4 on a clean clone of c2b2ba1a (the composed code head): its |
| `firmware/fw-gate-c2b2ba1a-s2.txt` | 37,024 | `62b1ff57a091fee7` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4 --jobs 4 on a clean clone of c2b2ba1a (the composed code head): its |
| `firmware/fw-gate-c2b2ba1a-s3.txt` | 118,751 | `3e7eb17c9b6f76e6` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4 --jobs 4 on a clean clone of c2b2ba1a (the composed code head): its |
| `firmware/fw-gate-f5a1585e-s0.txt` | 4,565 | `f16cab4f6c24222f` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 4 on a clean clone of f5a1585e (the final head): its head, t |
| `firmware/fw-gate-f5a1585e-s1.txt` | 162,465 | `d3291bc9ec1f6ef7` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4 --jobs 4 on a clean clone of f5a1585e (the final head): its head, t |
| `firmware/fw-gate-f5a1585e-s2.txt` | 37,016 | `77eeb5fd4053a34d` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4 --jobs 4 on a clean clone of f5a1585e (the final head): its head, t |
| `firmware/fw-gate-f5a1585e-s3.txt` | 118,745 | `9b2f899c832a8ac7` | # python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4 --jobs 4 on a clean clone of f5a1585e (the final head): its head, t |
| `ledger/fixture-sizes-d6c398c8.txt` | 5,963 | `d2cc5afb1a400b98` | # #584's variant_sizes.py (tools/variant_sizes.py.txt) on a clean clone of d6c398c8, 8x8 with one interface then two (the second run alone; the first stopped af |
| `ledger/fixture-sizes-mutations-on-their-variants-c2b2ba1a.txt` | 1,977 | `124a321de8359ebe` | # tools/mut_variant_sizes.py.txt on a clean clone of c2b2ba1a: each CPU budget harness mutation that needs a labelled variant, built with it at both 8x8 points, |
| `ledger/plat-ledger-c2b2ba1a.txt` | 3,527 | `74668e0242750b00` | # python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <build> on a clean clone of c2b2ba1a (product LiteX venv, pinned RV32 SDK), then each image |
| `ledger/plat-ledger-d6c398c8.txt` | 5,509 | `92c6535607e62ab3` | # python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <build> on a clean clone of d6c398c8 (product LiteX venv, pinned RV32 SDK), then each image |
| `ledger/plat-ledger-f5a1585e.txt` | 3,585 | `c5f0f6d4ccf00cf4` | # python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <build> on a clean clone of f5a1585e (the final head), then each image's sha256, compared w |
| `ledger/test-ctrl-memory-c2b2ba1a.txt` | 60,315 | `d8148563833cf56e` | # sw/litex/test_ctrl_memory.py (product LiteX venv) on the lane's working tree, identical to c2b2ba1a in sw/litex and docs (committed right after) |
| `merge/merges-and-resolution.txt` | 116,444 | `931611ee7b3974a5` | # The composition train's merges: each merge commit, its parents, the PR head merged, the files each side changed, the conflicted files and the combined diff (g |
| `route/1x1-ExtraPostPlacementOpt/artifacts.sha256` | 252 | `9e6c1d2c4315f270` | 2be8074a0a6a1b22b595a88e62ec0bedca39c7e9c747d486695ef281944aa3b1  gateware/alinx_ax7101.bit |
| `route/1x1-ExtraPostPlacementOpt/build.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `route/1x1-ExtraPostPlacementOpt/identity.log` | 107 | `24e56f2b7ae5d7fc` | image identity: a split image whose manifest, ident, firmware, bitstream and placement agree, with no DDR3 |
| `route/1x1-ExtraPostPlacementOpt/per-clock.txt` | 1,362 | `a159e635124ccca3` | == Slow_85C |
| `route/1x1-ExtraPostPlacementOpt/recipe.txt` | 1,089 | `b1d3c81113900983` | vivado-slot: slot 0 ($VIVADO_LOCK), MemAvailable 68 GB, 2026-11-23T10:44:12+01:00 |
| `route/1x1-ExtraPostPlacementOpt/signoff.txt` | 298 | `1316a69adc482687` | Slow_85C: WNS +0.019 ns (0 failing), WHS +0.102 ns (0 failing) |
| `route/1x1-ExtraPostPlacementOpt/utilization-948-64117b77.txt` | 440 | `298f669c91719a76` | r41x1/build_ExtraPostPlacementOpt/gateware Slice LUTs=32768 LUT as Logic=31471 LUT as Memory=1297 Slice Registers=42805 Slice=13989 Block RAM Tile=79.5 RAMB36/F |
| `route/1x1-ExtraPostPlacementOpt/utilization.txt` | 438 | `3eb5e0535562798c` | 1x1/build_ExtraPostPlacementOpt/gateware Slice LUTs=32701 LUT as Logic=31404 LUT as Memory=1297 Slice Registers=42803 Slice=13731 Block RAM Tile=80.5 RAMB36/FIF |
| `route/1x1-ExtraTimingOpt/artifacts.sha256` | 252 | `f712974fdbe8757a` | 1d6357dce1b142930ee8f3f3c484d712e05fd039766653dd7652d61d9ff1ab30  gateware/alinx_ax7101.bit |
| `route/1x1-ExtraTimingOpt/build.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `route/1x1-ExtraTimingOpt/identity.log` | 107 | `24e56f2b7ae5d7fc` | image identity: a split image whose manifest, ident, firmware, bitstream and placement agree, with no DDR3 |
| `route/1x1-ExtraTimingOpt/per-clock.txt` | 1,362 | `963b0af07d00ddd7` | == Slow_85C |
| `route/1x1-ExtraTimingOpt/recipe.txt` | 1,075 | `b7a198811c8ca99e` | vivado-slot: slot 0 ($VIVADO_LOCK), MemAvailable 68 GB, 2026-11-23T11:02:54+01:00 |
| `route/1x1-ExtraTimingOpt/signoff.txt` | 372 | `6cc4a788ec556458` | Slow_85C: WNS +0.384 ns (0 failing), WHS +0.102 ns (0 failing) |
| `route/1x1-ExtraTimingOpt/utilization-948-64117b77.txt` | 433 | `7f428e3bb58c3d11` | r41x1/build_ExtraTimingOpt/gateware Slice LUTs=32765 LUT as Logic=31468 LUT as Memory=1297 Slice Registers=42804 Slice=14297 Block RAM Tile=79.5 RAMB36/FIFO=? R |
| `route/1x1-ExtraTimingOpt/utilization.txt` | 431 | `f0ed9351f57618d7` | 1x1/build_ExtraTimingOpt/gateware Slice LUTs=32680 LUT as Logic=31384 LUT as Memory=1296 Slice Registers=42805 Slice=14297 Block RAM Tile=80.5 RAMB36/FIFO=? RAM |
| `route/8x8-ExtraPostPlacementOpt/artifacts.sha256` | 252 | `cdef72a08be2104b` | b3ae74815d4bd3e98fd559db20d934b529a09aae025fe6e06616f427db59cd46  gateware/alinx_ax7101.bit |
| `route/8x8-ExtraPostPlacementOpt/build.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `route/8x8-ExtraPostPlacementOpt/identity.log` | 107 | `24e56f2b7ae5d7fc` | image identity: a split image whose manifest, ident, firmware, bitstream and placement agree, with no DDR3 |
| `route/8x8-ExtraPostPlacementOpt/per-clock.txt` | 1,550 | `6280b7fd2637c5ca` | == Slow_85C |
| `route/8x8-ExtraPostPlacementOpt/recipe.txt` | 1,103 | `529183f052329548` | vivado-slot: slot 0 ($VIVADO_LOCK), MemAvailable 70 GB, 2026-11-23T10:04:44+01:00 |
| `route/8x8-ExtraPostPlacementOpt/signoff.txt` | 372 | `e1806869254b2883` | Slow_85C: WNS +0.105 ns (0 failing), WHS +0.102 ns (0 failing) |
| `route/8x8-ExtraPostPlacementOpt/utilization-948-64117b77.txt` | 442 | `1bd8f911920f97a2` | r48x8/build_ExtraPostPlacementOpt/gateware Slice LUTs=44103 LUT as Logic=42901 LUT as Memory=1202 Slice Registers=51272 Slice=15691 Block RAM Tile=94 RAMB36/FIF |
| `route/8x8-ExtraPostPlacementOpt/utilization.txt` | 442 | `969fbe8adc99c02d` | 8x8/build_ExtraPostPlacementOpt/gateware Slice LUTs=46621 LUT as Logic=45401 LUT as Memory=1220 Slice Registers=53338 Slice=15570 Block RAM Tile=98.5 RAMB36/FIF |
| `route/chain-first-attempt-oom.log` | 430 | `817958b1ccdf0eca` | # the route chain's first attempt (session pool, 16 threads, MemoryMax 12G): the unit was OOM-killed at 08:34 in the 8x8 synthesis; restarted at 10:01 on a book |
| `route/chain.log` | 910 | `52bc64a87f1b0df3` | 2026-11-23T10:01:02+01:00 chain head c2b2ba1a4742335e0678ec1f00f9033d1913b1da cpus 56-63 |
| `rtl/nvm-split-target-c2b2ba1a.txt` | 6,106 | `46379a3031ecdbe3` | # tb/verilator/nvm_split_target/run.py --self-test, --point 1x1, --point 8x8, then scripts/check_nvm_capture.py, on a clean clone of c2b2ba1a: each command and  |
| `rtl/split-boot-c2b2ba1a.txt` | 5,041 | `20420de7cff68ed9` | # tb/verilator/ctrl_split_boot/run.py on a clean clone of c2b2ba1a: 1x1, 8x8, 8x8 --interfaces 2, --placement-controls, --native-controls, --self-test; each com |
| `rtl/suites-A-c2b2ba1a.txt` | 276 | `84006550d4c92778` | # scripts/run_all_suites.sh's per-suite recipe (timeout, make -C tb/verilator/<suite>, suite_tally's verdict) on a clean clone of c2b2ba1a, the CI image's Veril |
| `rtl/suites-B-c2b2ba1a.txt` | 398 | `f39ee3515d3f1062` | # scripts/run_all_suites.sh's per-suite recipe (timeout, make -C tb/verilator/<suite>, suite_tally's verdict) on a clean clone of c2b2ba1a, the CI image's Veril |
| `rtl/suites-C-c2b2ba1a.txt` | 987 | `8c45b103770473dc` | # scripts/run_all_suites.sh's per-suite recipe (timeout, make -C tb/verilator/<suite>, suite_tally's verdict) on a clean clone of c2b2ba1a, the CI image's Veril |
| `tools/analyse.sh.txt` | 1,107 | `34bfd3388e89287a` | #!/bin/bash |
| `tools/builder.sh.txt` | 976 | `d2c2d5093354373f` | #!/bin/bash |
| `tools/cb.sh.txt` | 541 | `d251eafe01e9c1a9` | #!/bin/bash |
| `tools/cov.sh.txt` | 462 | `614dace6b489779a` | #!/bin/bash |
| `tools/env.sh.txt` | 497 | `bcacc29947c8bf01` | # Environment for the 956 sync lane's harness and firmware runs (sourced). |
| `tools/fwgate.sh.txt` | 555 | `eac3b6fd59031130` | #!/bin/bash |
| `tools/launch.sh.txt` | 839 | `887d01461d895bb1` | #!/bin/bash |
| `tools/ledger.sh.txt` | 1,214 | `fae2746f2f70b5e7` | #!/usr/bin/env bash |
| `tools/legs.py.txt` | 3,453 | `6da16143cb8dd0c1` | #!/usr/bin/env python3 |
| `tools/make_index.py.txt` | 740 | `9c073abefb0290f9` | """make_index.py DIR: INDEX.md from the files present: path, size, sha256 (16 hex) and each file's first line.""" |
| `tools/mkclone.sh.txt` | 734 | `81eae6499b169d8c` | #!/bin/bash |
| `tools/mut_variant_sizes.py.txt` | 1,107 | `55da9c27b141a1b9` | #!/usr/bin/env python3 |
| `tools/nvmt.sh.txt` | 881 | `8fcbbf250f17b094` | #!/bin/bash |
| `tools/route-boot.sh.txt` | 457 | `4b0d6f9f9f197f04` | #!/usr/bin/env bash |
| `tools/route-chain.sh.txt` | 2,352 | `8e2185b7212df0da` | #!/usr/bin/env bash |
| `tools/route-env.sh.txt` | 678 | `0ae1506c4186fe7c` | # env.sh: the S12b gating lane's tool environment (its tools/env.sh), HOME and TMPDIR moved to train1117-a794's scratch; the pinned RV32 SDK in that lane's scra |
| `tools/route-gbuild.sh.txt` | 1,959 | `5fdc6852bc33a652` | #!/usr/bin/env bash |
| `tools/route-gprep.sh.txt` | 2,304 | `4659c251a82f44f6` | #!/usr/bin/env bash |
| `tools/route-signoff.py.txt` | 1,324 | `2900ae1a5485933c` | #!/usr/bin/env python3 |
| `tools/sanitize.py.txt` | 614 | `e75d62ac6c42b095` | """sanitize.py SRC DST [header]: copy a log with host paths replaced by placeholders; DST refused over 200 KB.""" |
| `tools/splitboot.sh.txt` | 1,138 | `f4b66314fc39ef8b` | #!/bin/bash |
| `tools/suites.sh.txt` | 1,456 | `3acde9aebc8ac0a0` | #!/usr/bin/env bash |
| `tools/survey_point4.py.txt` | 5,027 | `966d3ba4e49ceb42` | """(round 4 copy: the interface count from SURVEY_NIF, the tools from TOOLS) 8x8/1if's stated-table survey over the measurement's legs (round 5): two views of t |
| `tools/twin.sh.txt` | 347 | `e1de008ef45d6955` | #!/bin/bash |
| `tools/variant_sizes.py.txt` | 1,661 | `322f5901a15a5489` | #!/usr/bin/env python3 |
| `tools/variant_sizes_n.py.txt` | 1,700 | `100eacd03e7833fb` | #!/usr/bin/env python3 |
| `tools/worker.py.txt` | 2,217 | `3454a5ecd2318b87` | #!/usr/bin/env python3 |
| `twin/twin-c2b2ba1a.txt` | 32,877 | `72175131f0db2bfb` | # make -j8 twin, twin-plants, twin-maps, twin-maps-plants in tb/verilator/milan_dp on a clean clone of c2b2ba1a: each target's rc and its RESULT/PASS/FAIL/findi |
