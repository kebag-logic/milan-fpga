# Receipts (generated from the files present)

| File | Bytes | sha256 | First line |
|---|---:|---|---|
| `builder/builder-leg-0.json` | 4,592 | `f0c4a52b1019924c` | {"driver":{"gates":[{"gate":"test_baremetal_profile_contract","not_run":[["gate 1b","the MAKEFLAGS += -e mutation: this make does not re-read MAKEFLAGS mid-pars |
| `builder/builder-leg-1.json` | 16,592 | `3a42a4692a7bfd20` | {"driver":{"gates":[{"gate":"test_soc_option_refusals","not_run":[],"verdict":"pass"},{"gate":"test_commercial_timing_grade","not_run":[],"verdict":"pass"},{"ga |
| `builder/builder-legs-union-39e9c9d2.txt` | 160,331 | `df7460932d29b392` | # builder.sh on the clean clone bld at 39e9c9d247ba0b22fe8611c9253c216700210ae4, submodule origins at their .gitmodules URLs: ci_builder_legs.py run 0 and 1 (te |
| `builder/union.json` | 8,770 | `4ffe9b6ce52896b4` | {"head":"39e9c9d247ba0b22fe8611c9253c216700210ae4","inventory":["test_soc_option_refusals","test_commercial_timing_grade","test_baremetal_clock_contract","test_ |
| `docs/docs-workflow-steps-8c5a51e1.txt` | 9,309 | `e2994ca8699d0db3` | # docs_steps.py 8c5a51e197b98ef79b3fbc7d8add8d6bf2126ee0: every run: step of docs.yml's gate jobs on a fresh clean clone; the style gate's 18 findings are fixed |
| `docs/docs-workflow-steps-bbfdb674.txt` | 9,300 | `e62b70cccdb49156` | # docs_steps.py bbfdb6746d585e490508783dc8a88c79fbab02c0 (the final head): every run: step of docs.yml's gate jobs on a fresh clean clone; em-dash base 300da99b |
| `docs/style-gate-8c5a51e1.log` | 2,844 | `d39266a229ca59c3` | # head 8c5a51e197b98ef79b3fbc7d8add8d6bf2126ee0 job docs-gates-0 step: Concise audience documentation gate |
| `ledger/image-hashes-vs-300da99b.txt` | 263 | `6d76d46ee7777376` | # the 24 image digests (elf, stripped, loadable at each of 8 points) at 39e9c9d2 against the base 300da99b's plat_ledger receipt (train lane round 4): diff outp |
| `ledger/plat-ledger-39e9c9d2.txt` | 15,269 | `b169f73ecbc78871` | # tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <scratch>/ledger-build on a clean clone at 39e9c9d247ba0b22fe8611c9253c216700210ae4 (unit milan-gptppi |
| `route/1x1-AltSpreadLogic_high/artifacts.sha256` | 252 | `79b9f395eea344c7` | d40ce1ac8ad9a32f50a301ad49ff5ef925c972e1b487e56638d6268ba9b87c6d  gateware/alinx_ax7101.bit |
| `route/1x1-AltSpreadLogic_high/build.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `route/1x1-AltSpreadLogic_high/identity.log` | 107 | `24e56f2b7ae5d7fc` | image identity: a split image whose manifest, ident, firmware, bitstream and placement agree, with no DDR3 |
| `route/1x1-AltSpreadLogic_high/per-clock.txt` | 1,362 | `e0e76e75090df851` | == Slow_85C |
| `route/1x1-AltSpreadLogic_high/recipe.txt` | 1,085 | `647d9acd3db57253` | vivado-slot: slot 0 ($VIVADO_LOCK), MemAvailable 67 GB, 2026-11-24T07:05:54+01:00 |
| `route/1x1-AltSpreadLogic_high/signoff.txt` | 336 | `c1e66d4c2a99cc05` | Slow_85C: WNS +0.072 ns (0 failing), WHS +0.102 ns (0 failing) |
| `route/1x1-AltSpreadLogic_high/utilization.txt` | 436 | `47b03279e7fa2b25` | 1x1/build_AltSpreadLogic_high/gateware Slice LUTs=32633 LUT as Logic=31337 LUT as Memory=1296 Slice Registers=42803 Slice=14142 Block RAM Tile=80.5 RAMB36/FIFO= |
| `route/1x1-ExtraPostPlacementOpt/artifacts.sha256` | 252 | `bfb0468609931bae` | 032af7d0369bc133d188440c90f18248da0fc38194b46509bde6cd25784f4a01  gateware/alinx_ax7101.bit |
| `route/1x1-ExtraPostPlacementOpt/build.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `route/1x1-ExtraPostPlacementOpt/identity.log` | 107 | `24e56f2b7ae5d7fc` | image identity: a split image whose manifest, ident, firmware, bitstream and placement agree, with no DDR3 |
| `route/1x1-ExtraPostPlacementOpt/per-clock.txt` | 1,362 | `be8ef13dd7d60943` | == Slow_85C |
| `route/1x1-ExtraPostPlacementOpt/recipe.txt` | 1,096 | `0ebca285c235fc7a` | vivado-slot: slot 1 (/tmp/milan-vivado-slot-1.lock), MemAvailable 62 GB, 2026-11-24T06:30:33+01:00 |
| `route/1x1-ExtraPostPlacementOpt/signoff.txt` | 298 | `1b9b882129cd922c` | Slow_85C: WNS +0.007 ns (0 failing), WHS +0.102 ns (0 failing) |
| `route/1x1-ExtraPostPlacementOpt/utilization-base-300da99b.txt` | 438 | `3eb5e0535562798c` | 1x1/build_ExtraPostPlacementOpt/gateware Slice LUTs=32701 LUT as Logic=31404 LUT as Memory=1297 Slice Registers=42803 Slice=13731 Block RAM Tile=80.5 RAMB36/FIF |
| `route/1x1-ExtraPostPlacementOpt/utilization.txt` | 438 | `a147343cef4eee0e` | 1x1/build_ExtraPostPlacementOpt/gateware Slice LUTs=32555 LUT as Logic=31258 LUT as Memory=1297 Slice Registers=42803 Slice=13598 Block RAM Tile=80.5 RAMB36/FIF |
| `route/1x1-ExtraPostPlacementOpt/worst-path.txt` | 274 | `e60264fcf3a55b6c` | 840-  Source:                 KL_mbx/rd_off_r_reg[8]/C |
| `route/1x1-ExtraTimingOpt/artifacts.sha256` | 252 | `046ad27b58775b5b` | 8095f07b2ef5e2f6daadc7fa888e7536918cc043a98b5b1918552c54fef3c46d  gateware/alinx_ax7101.bit |
| `route/1x1-ExtraTimingOpt/build.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `route/1x1-ExtraTimingOpt/hierdiff-vs-base.txt` | 3,252 | `2faee1f3c6b9ca7d` | # hierdiff.py <base 300da99b 1x1 ExtraTimingOpt gateware (the train lane's route of c2b2ba1a)> <this route's gateware at 973f2f20> 30 |
| `route/1x1-ExtraTimingOpt/identity.log` | 107 | `24e56f2b7ae5d7fc` | image identity: a split image whose manifest, ident, firmware, bitstream and placement agree, with no DDR3 |
| `route/1x1-ExtraTimingOpt/per-clock.txt` | 1,362 | `b28572e35762a700` | == Slow_85C |
| `route/1x1-ExtraTimingOpt/recipe.txt` | 1,075 | `92b7efcc800efbb0` | vivado-slot: slot 0 ($VIVADO_LOCK), MemAvailable 71 GB, 2026-11-24T06:47:54+01:00 |
| `route/1x1-ExtraTimingOpt/signoff.txt` | 336 | `c67b6ea0e6d90260` | Slow_85C: WNS +0.170 ns (0 failing), WHS +0.102 ns (0 failing) |
| `route/1x1-ExtraTimingOpt/utilization-base-300da99b.txt` | 431 | `f0ed9351f57618d7` | 1x1/build_ExtraTimingOpt/gateware Slice LUTs=32680 LUT as Logic=31384 LUT as Memory=1296 Slice Registers=42805 Slice=14297 Block RAM Tile=80.5 RAMB36/FIFO=? RAM |
| `route/1x1-ExtraTimingOpt/utilization.txt` | 431 | `593ca7d8aaf522ff` | 1x1/build_ExtraTimingOpt/gateware Slice LUTs=32639 LUT as Logic=31343 LUT as Memory=1296 Slice Registers=42805 Slice=14147 Block RAM Tile=80.5 RAMB36/FIFO=? RAM |
| `route/1x1-ExtraTimingOpt/worst-hold-path.txt` | 354 | `9f000ff0e4103585` | 3024-  Source:                 milan_datapath/chan_map_render/sel_r_reg[7][14]/C |
| `route/1x1-ExtraTimingOpt/worst-setup-path.txt` | 406 | `fa29c0a51e60367f` | 840-  Source:                 FSM_onehot_socbushandler_axilite2wishbone_state_reg[1]/C |
| `route/8x8-ExtraPostPlacementOpt/artifacts.sha256` | 252 | `de7669fb38e661e0` | 788cd754826629e97509b24f976fc5ed0b1beaa09c66fee06c12723e264474fd  gateware/alinx_ax7101.bit |
| `route/8x8-ExtraPostPlacementOpt/build.rc` | 2 | `9a271f2a916b0b6e` | 0 |
| `route/8x8-ExtraPostPlacementOpt/hierdiff-vs-base.txt` | 3,250 | `645f697b4f8ccda6` | # hierdiff.py <base 300da99b 8x8 ExtraPostPlacementOpt gateware (the train lane's route of c2b2ba1a)> <this route's gateware at 973f2f20> 30: the 30 placed-hier |
| `route/8x8-ExtraPostPlacementOpt/identity.log` | 107 | `24e56f2b7ae5d7fc` | image identity: a split image whose manifest, ident, firmware, bitstream and placement agree, with no DDR3 |
| `route/8x8-ExtraPostPlacementOpt/per-clock.txt` | 1,550 | `0ca87fc3f963893e` | == Slow_85C |
| `route/8x8-ExtraPostPlacementOpt/recipe.txt` | 1,102 | `4a13d5c0475199a2` | vivado-slot: slot 0 ($VIVADO_LOCK), MemAvailable 50 GB, 2026-11-24T05:55:50+01:00 |
| `route/8x8-ExtraPostPlacementOpt/signoff.txt` | 372 | `c44f77437045fa1c` | Slow_85C: WNS +0.066 ns (0 failing), WHS +0.102 ns (0 failing) |
| `route/8x8-ExtraPostPlacementOpt/utilization-base-300da99b.txt` | 442 | `969fbe8adc99c02d` | 8x8/build_ExtraPostPlacementOpt/gateware Slice LUTs=46621 LUT as Logic=45401 LUT as Memory=1220 Slice Registers=53338 Slice=15570 Block RAM Tile=98.5 RAMB36/FIF |
| `route/8x8-ExtraPostPlacementOpt/utilization.txt` | 442 | `e0aecec7dc774c51` | 8x8/build_ExtraPostPlacementOpt/gateware Slice LUTs=46246 LUT as Logic=45027 LUT as Memory=1219 Slice Registers=53381 Slice=15622 Block RAM Tile=98.5 RAMB36/FIF |
| `route/8x8-ExtraPostPlacementOpt/worst-setup-path.txt` | 359 | `5c840113c4995dd0` | 844-  Source:                 KL_mbx/rd_off_r_reg[5]_rep__1/C |
| `route/chain.log` | 1,431 | `73e99842503ba3af` | # the route chains' log: 8x8 and 1x1 side by side (VIVADO_SLOTS=2), each through the slot script, then the third 1x1 directive by one.sh (best of three after th |
| `route/prep-1x1.log` | 5,506 | `7a0605ac90df0c33` | # gprep.sh for 1x1 at 973f2f20 (builder split placement, stand-in export, flash map, platform image at one interface) |
| `route/prep-8x8.log` | 5,467 | `5aa1c99b289dd141` | # gprep.sh for 8x8 at 973f2f20 (builder split placement, stand-in export, flash map, platform image at one interface) |
| `rtl/mbx-rerun-ci-makeflags-8c5a51e1.log` | 91,989 | `50001e97af350698` | # make -C tb/verilator/mbx on a clean clone at 8c5a51e197b98ef79b3fbc7d8add8d6bf2126ee0 with MAKEFLAGS='-j8 --no-print-directory' (the CI's flag), rc 0 |
| `rtl/mbx-rerun-summary.txt` | 113 | `2abc040b46e97a2d` | head 8c5a51e197b98ef79b3fbc7d8add8d6bf2126ee0 porcelain 0 cpus 64-95 |
| `rtl/mbx-shard1-harness-fail-8c5a51e1.log` | 93,277 | `30892b3b548808c6` | # shard 1's mbx log: every check passes; dma-mutants refuses because make -s -C ... print-dma-vflags printed 'make[1]: Entering directory' (no --no-print-direct |
| `rtl/milan_dp-gptp-39e9c9d2.log` | 88,172 | `61b95eb629157e32` | # make -C tb/verilator/milan_dp gptp on a clean clone at 39e9c9d247ba0b22fe8611c9253c216700210ae4 (pinned Verilator 5.050), full log |
| `rtl/milan_dp-gptp-lat-39e9c9d2.log` | 89,497 | `5907e84eb70b1e1c` | # make -C tb/verilator/milan_dp gptp-lat on a clean clone at 39e9c9d247ba0b22fe8611c9253c216700210ae4 (pinned Verilator 5.050), full log |
| `rtl/milan_dp_gptp-physical-39e9c9d2.log` | 110,991 | `6981aa3e2cad8ce5` | # make -C tb/verilator/milan_dp_gptp (ax1x1gptp, verify_abort.py, verify_recentres.py --jobs 2) on a clean clone at 39e9c9d247ba0b22fe8611c9253c216700210ae4, se |
| `rtl/milan_dp_gptp-physical-summary.txt` | 124 | `a5bdf082b0ad1f80` | head 39e9c9d247ba0b22fe8611c9253c216700210ae4 porcelain 0 cpus 64-95 |
| `rtl/sweep-shard-0-8c5a51e1.txt` | 949 | `ce814dd70533efd8` | # sweep.sh 0: scripts/run_all_suites.sh --wait --shard 0/4 on a clean clone at 8c5a51e197b98ef79b3fbc7d8add8d6bf2126ee0, pinned Verilator 5.050, booked 8-CPU ra |
| `rtl/sweep-shard-1-8c5a51e1.txt` | 1,070 | `9da52a9d76205818` | # sweep.sh 1: scripts/run_all_suites.sh --wait --shard 1/4 on a clean clone at 8c5a51e197b98ef79b3fbc7d8add8d6bf2126ee0, pinned Verilator 5.050, booked 8-CPU ra |
| `rtl/sweep-shard-2-8c5a51e1.txt` | 1,071 | `f7e99654d2a93a67` | # sweep.sh 2: scripts/run_all_suites.sh --wait --shard 2/4 on a clean clone at 8c5a51e197b98ef79b3fbc7d8add8d6bf2126ee0, pinned Verilator 5.050, booked 8-CPU ra |
| `rtl/sweep-shard-2-oom-attempt-8c5a51e1.txt` | 707 | `6c9573b6b515bb34` | # shard 2's first attempt: the unit was OOM-killed at its 12 GB cap during capture_coherence (systemd: 'The kernel OOM killer killed some processes in this unit |
| `rtl/sweep-shard-3-8c5a51e1.txt` | 1,565 | `f25fdd5c44a42ec5` | # sweep.sh 3: scripts/run_all_suites.sh --wait --shard 3/4 on a clean clone at 8c5a51e197b98ef79b3fbc7d8add8d6bf2126ee0, pinned Verilator 5.050, booked 8-CPU ra |
| `rtl/tsn_fuzz-campaigns-8c5a51e1.log` | 36,738 | `64f5aedcc300a037` | # make -C tb/verilator/tsn_fuzz on a clean clone at 8c5a51e197b98ef79b3fbc7d8add8d6bf2126ee0 with TSN_GEN_ROOT set (the tsn-gen field campaigns, which the sweep |
| `rtl/tsn_fuzz-campaigns-tracked-diff.txt` | 1,581 | `3c510de70d607fc4` | # git diff the campaigns left in the clone: only each TEST_RESULTS.md's timestamp moves; gPTP/802.1AS 675 pass, 0 fail and AAF/AVTP 164 pass, 0 fail, equal to t |
| `synth/hosted-gate-equivalents-bbfdb674.txt` | 23,929 | `1a86a68a76c49f29` | # synth_gates.sh on a clean clone at bbfdb6746d585e490508783dc8a88c79fbab02c0 (session pool): lint_rtl.py --check --self-test; run.sh --mode elaborate of milan_ |
| `tools/builder.sh.txt` | 976 | `d2c2d5093354373f` | #!/bin/bash |
| `tools/docs_steps.py.txt` | 7,453 | `b81763d4d1bc9485` | #!/usr/bin/env python3 |
| `tools/env.sh.txt` | 497 | `bcacc29947c8bf01` | # Environment for the 956 sync lane's harness and firmware runs (sourced). |
| `tools/launch.sh.txt` | 876 | `cd604afbef963691` | #!/bin/bash |
| `tools/ledger.sh.txt` | 1,214 | `fae2746f2f70b5e7` | #!/usr/bin/env bash |
| `tools/legs.sh.txt` | 1,088 | `76371438e31c70e3` | #!/usr/bin/env bash |
| `tools/make_index.py.txt` | 740 | `9c073abefb0290f9` | """make_index.py DIR: INDEX.md from the files present: path, size, sha256 (16 hex) and each file's first line.""" |
| `tools/mkclone.sh.txt` | 734 | `81eae6499b169d8c` | #!/bin/bash |
| `tools/route-boot.sh.txt` | 457 | `4b0d6f9f9f197f04` | #!/usr/bin/env bash |
| `tools/route-chain.sh.txt` | 2,446 | `9aa92403d50a3291` | #!/usr/bin/env bash |
| `tools/route-collect_fit.sh.txt` | 1,564 | `a6b93a54bf2924e7` | #!/usr/bin/env bash |
| `tools/route-env.sh.txt` | 678 | `0ae1506c4186fe7c` | # env.sh: the S12b gating lane's tool environment (its tools/env.sh), HOME and TMPDIR moved to train1117-a794's scratch; the pinned RV32 SDK in that lane's scra |
| `tools/route-gbuild.sh.txt` | 1,959 | `5fdc6852bc33a652` | #!/usr/bin/env bash |
| `tools/route-gprep.sh.txt` | 2,304 | `4659c251a82f44f6` | #!/usr/bin/env bash |
| `tools/route-hierdiff.py.txt` | 1,700 | `a232f79fb4f54b32` | #!/usr/bin/env python3 |
| `tools/route-one.sh.txt` | 1,284 | `6ad9d4bcf4267e75` | #!/usr/bin/env bash |
| `tools/route-signoff.py.txt` | 1,324 | `2900ae1a5485933c` | #!/usr/bin/env python3 |
| `tools/route-util.py.txt` | 2,116 | `b6f47835df7c6fcc` | #!/usr/bin/env python3 |
| `tools/sanitize.py.txt` | 614 | `e75d62ac6c42b095` | """sanitize.py SRC DST [header]: copy a log with host paths replaced by placeholders; DST refused over 200 KB.""" |
| `tools/sweep.sh.txt` | 810 | `193a643e43577d6b` | #!/usr/bin/env bash |
| `tools/wait_launch.sh.txt` | 178 | `9106e3501fc4858d` | #!/bin/bash |
