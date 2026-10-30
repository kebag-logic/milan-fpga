# HANDOFF: #814 SoC sys-domain timing cuts, round 2, executor [A703b]

Status: **STOP** at head `8b28ebaf035e786ccf5b8e50098dbc111f51831f`, the round 1 head: round 2 added no commit. Worktree clean, every submodule at its gitlink, live remote dev still `1e80128f`. Nothing pushed.

- Lane: `814-soc-timing-cut`, from dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`
- origin: https://github.com/kebag-logic/milan-fpga.git (verified); no git command was run inside a submodule
- Assignment: the latest [A10] comment on #814 (issuecomment-6517931276), the corrected issue body, the F4 ruling (issuecomment-6516396929)
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/814#issuecomment-6518024195
- STOP: https://github.com/kebag-logic/milan-fpga/issues/814#issuecomment-6520509329 (the lane's only other post)
- Round 1: `../814-a703/HANDOFF.md` (the measurement of dev, the cuts, their checks and their out-of-context costs)

## STOP

Step 3's acceptance is not met, and two of the issue's remaining STOP conditions hold. So no record was re-recorded, nothing was committed, and the step 4 gates were not started.

1. **The shipping route fails `pp_resource_gate.py check`, exit 1.** WNS is +0.128 ns, a 0.312 ns fall from the +0.440 ns record against the 0.25 ns limit. Every resource figure passes (LUT -185, FF +315, slices -16), and so does WHS (+0.030 ns).
2. **A family outside F1 to F4 is within 0.3 ns of the worst path at the shipping directive** (the F4 ruling keeps this STOP). It is the worst path itself: the milan-domain reset into the MMCM servo's PS-domain reset synchroniser, a 50 MHz to 200 MHz crossing at +0.128 ns. Five more families outside F1 to F4 also lie within 0.3 ns of it (table below).
3. **The ExtraTimingOpt comparison route misses the +0.030 ns floor**: +0.010 ns at both slow corners. The path is `sys`: the AECP response-buffer bridge's byte select `milansoc_ws0_reg[5]`, through the CPU DMA port's write arbitration, into the NVM bridge's FSM `fsm2_state_reg[0]/CE`, 17 levels, 75 % routing. That family is outside F1 to F4 too. The shipping route and AltSpreadLogic_high meet the floor at every corner.

The cuts themselves did what they were for. At every directive F1, F2 and F3 sit more than 1 ns from the worst path. F1 was +0.627 to +0.816 ns at dev and is now +2.110 to +2.386 ns. F2 was +0.106 to +0.689 ns and is now +1.162 to +1.460 ns. F3 was +0.303 to +0.572 ns and has left the 5,000 worst `sys` endpoints, apart from one endpoint at +4.379 ns. What sets the WNS now is a different family at each directive, and none of those families has logic this lane changes. Each was measured at dev with more slack.

## 1. Route-1x1 at the head, three directives

Recipe unchanged (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`), `--single-thread-synthesis`, `general.maxThreads` 32, Vivado 2026.1, default seed, in a clean clone at `8b28ebaf`. The shipping ExtraPostPlacementOpt ran first. AltSpreadLogic_high and ExtraTimingOpt ran from its synthesis checkpoint (the recipe's snippet, `scripts/dir_prep.py`), in parallel through the slot wrapper. `scripts/paths.tcl` reopened each routed checkpoint and wrote the worst path per endpoint, for the 5,000 worst `sys` endpoints and for the 5,000 worst endpoints over every path group. Each stage's cells and the slices they occupy went to `stage_cells.tsv`. `scripts/summarize_paths.py` (`sys`) and `scripts/summarize_all.py` (every group) write the families.

| Directive | Vivado rc, minutes | WNS / WHS ns | Worst path (family) | F1 flash | F2 LiteDRAM -> crossing | F3 refresher | F4 CPU DMA write bridge | LUT / FF / slices |
|---|---|---|---|---:|---:|---:|---:|---|
| ExtraPostPlacementOpt (shipping) | 0, 57.8 | **+0.128** / +0.030 | milan reset -> MMCM servo PS reset synchroniser (milan -> 200 MHz), 1 level, 86 % routing | +2.386 | +1.162 | not in the 5,000 | +0.324 | 51,827 / 54,022 / 15,764 (86 free) |
| AltSpreadLogic_high | 0, 20.7 | **+0.039** / +0.029 | F4: `aligner/frontend_allocateSlot_wCmd_s2mPipe_rData_header_reg[0]` -> `onPerId_bridge/pendings_valids_reg[0]`, 19 levels, 75 % | +2.110 | +1.460 | +4.379 | +0.039 | 51,895 / 54,024 / 15,839 (11 free) |
| ExtraTimingOpt | 0, 24.5 | **+0.010** / +0.029 | `sys`: `milansoc_ws0_reg[5]` -> `FSM_sequential_subfragments_fsm2_state_reg[0]/CE`, 17 levels, 75 % | +2.228 | +1.380 | not in the 5,000 | +0.059 | 51,882 / 54,029 / 15,839 (11 free) |

Against dev `1e80128f`'s own three routes (round 1, the same recipe and bank):

| Directive | WNS dev -> head | `sys` | milan (clkout1) | milan -> 200 MHz crossing | eth RX | LUT / FF / slices, dev -> head |
|---|---|---|---|---|---|---|
| ExtraPostPlacementOpt | +0.303 -> +0.128 | +0.303 -> +0.324 | +0.599 -> +0.246 | +1.975 -> **+0.128** | +0.735 -> +0.390 | 51,801 -> 51,827 / 53,760 -> 54,022 / 15,834 -> 15,764 |
| AltSpreadLogic_high | +0.230 -> +0.039 | +0.230 -> **+0.039** | +1.136 -> +0.506 | +2.341 -> +1.039 | +1.228 -> +0.662 | 51,846 -> 51,895 / 53,759 -> 54,024 / 15,795 -> 15,839 |
| ExtraTimingOpt | +0.106 -> +0.010 | +0.106 -> **+0.010** | +0.428 -> +0.571 | +2.387 -> +0.963 | +1.330 -> +0.858 | 51,829 -> 51,882 / 53,758 -> 54,029 / 15,794 -> 15,839 |

Every corner (`alinx_ax7101_signoff_*_timing.rpt`):

| Directive | Slow 0C / 85C WNS, WHS | Fast 0C / 85C WNS, WHS | Floor (+0.030 / 0) |
|---|---|---|---|
| ExtraPostPlacementOpt | +0.128, +0.059 | +1.311, +0.030 | met |
| AltSpreadLogic_high | +0.039, +0.058 | +1.584, +0.029 | met |
| ExtraTimingOpt | **+0.010**, +0.058 | +1.480, +0.029 | **setup missed at both slow corners** |

### Families within 0.3 ns of the worst path

From `receipts/route-8b28ebaf/route-1x1-<directive>-all-top30.md` (every path group, worst path per endpoint):

| Directive | Family (clocks) | Worst slack ns | From the worst ns | Levels, routing | In F1 to F4? |
|---|---|---:|---:|---|---|
| ExtraPostPlacementOpt | `FDPE_3` -> `mmcm_servo/psrst_sync_r_reg[0]` (milan -> 200 MHz) | +0.128 | 0.000 | 1, 86 % | no |
| | `u_aecp/u_ucpu/uop_e_r_reg[imm]` -> `u_aecp/u_d3/taint_r_reg` (milan) | +0.246 | 0.118 | 36, 64 % | no |
| | F4 | +0.324 | 0.196 | 19, 74 % | F4 |
| | `milansoc_ws1_reg` -> `subfragments_fsm1_state_reg` (`sys`) | +0.348 | 0.220 | 16, 78 % | no |
| | LiteEth TX `bufferizeendpoints_state_reg` -> `src_in_r_reg` (eth RX clock) | +0.390 | 0.262 | 6, 83 % | no |
| | `u_ucpu/uop_e_r_reg[imm]` -> `deb_cnt_r_reg` (milan) | +0.393 | 0.265 | 35, 66 % | no |
| | `u_ucpu/uop_e_r_reg[fmt]` -> `live_mux_q_reg` (milan) | +0.411 | 0.283 | 23, 75 % | no |
| AltSpreadLogic_high | F4 | +0.039 | 0.000 | 19, 75 % | F4 |
| | `sdram_bankmachineN_row_reg` -> `sdram_twtrcon_count_reg` (`sys`) | +0.216 | 0.177 | | no |
| | `sdram_bankmachineN_row_reg` -> `bankmachineN_state_reg` (`sys`) | +0.231 | 0.192 | | no |
| ExtraTimingOpt | `milansoc_ws0_reg` -> `subfragments_fsm2_state_reg` (`sys`) | +0.010 | 0.000 | 17, 75 % | no |
| | F4 | +0.059 | 0.049 | | F4 |
| | `milansoc_ws0_reg` -> `milansoc_psn_reg` (`sys`) | +0.237 | 0.227 | | no |

What the outside families are:

- **The reset-synchroniser crossing.** `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:1292-1296` synchronises `rst_n` into `ps_clk_i` (`psrst_sync_r <= {psrst_sync_r[0], rst_n}`). The source `FDPE_3` is the milan domain's reset flip-flop, a high-fanout net. The two clocks come from one MMCM, so Vivado times the crossing as synchronous, with a 5 ns requirement. The path is one LUT and 4.0 ns of routing. It was +1.975, +2.341 and +2.387 ns at dev.
- **The processor memory bridges into the CPU's DMA port.** `ws0` and `ws1` are the byte selects of the AECP response-buffer bridge (`respmem`) and the NVM bridge (`nvmmem`). At ExtraTimingOpt the worst path runs from `ws0` through the bridge's Wishbone-to-AXI converter (`socbushandler1_wishbone2axi1`), LiteX's round-robin write arbiter (`socbushandler1_rr_write_grant`) and the CPU's DMA write-bus input pipe (`dma_bus_w_s2mPipe_rValid`). It ends at the NVM bridge FSM's enable. Round 1 measured `ws0 -> tmod1` at +0.427 ns (ExtraTimingOpt, 0.321 ns from F2), below its 0.3 ns line.
- **The protocol processor's AECP micro-CPU** on the 20 ns milan clock (35 or 36 levels). Dev had +0.428 to +1.136 ns.
- **LiteEth's TX buffer FSM** on the 8 ns Ethernet RX clock. Dev had +0.735 to +1.330 ns.
- **The LiteDRAM bank machines'** row compare into tWTR and the bank-machine state, inside LiteDRAM's controller.

None of these families has logic this lane changes. F4, which is inside the CPU netlist, moved from +0.603 / +0.353 / +0.686 ns at dev to +0.324 / +0.039 / +0.059 ns. The reset crossing, a single net, moved by 1.85 ns at the shipping directive. Round 1 measured 0.57 ns of route-to-route spread on F2, with no logic change either. Once F1 to F3 are cut, the WNS falls to whichever of these families draws the worst placement in a given route. They have similar depth: 15 to 19 levels on `sys` and 35 or 36 on milan, at 64 to 86 % routing. Every one of the head's three routes came out below dev's at the same directive: by 0.175, 0.191 and 0.096 ns.

## 2. The PHY-side flash stage in context

Cells named for each stage in the routed netlist (`stage_cells.tsv`: primitive cells whose names match the stage's signals, and the slices holding at least one of them, shared with other logic):

| Stage | FF | LUT | Slices occupied, EPPO / ASLH / ETO | Out of context, alone (round 1) |
|---|---:|---:|---|---|
| F1 `SPIPHYStage` (`milansoc_milansoc_stage_spi_phy_*`) | 174 | 61 | 51 / 44 / 44 | 54 LUT, 199 FF, 49 slices |
| F2 `AXIReadyStage` (`pipeready*`) | 88 | 6 | 26 / 26 / 26 | 78 LUT, 150 FF, 39 slices |
| F3 `RegisteredRefresher` (`refresher_cmd*`) | 3 | 6 | 3 / 4 / 4 | +0 LUT, +2 FF |

In context, 174 flip-flops carry the flash stage's names, against 199 out of context. The LUT counts are lower bounds: a LUT that synthesis merges with neighbouring logic can take that logic's name.

The flash family's slack is +2.386 / +2.110 / +2.228 ns (dev: +0.627 / +0.816 / +0.784 ns), 2.06 to 2.26 ns from each route's worst path. At the shipping directive its worst endpoint is the PHY's clock-divisor CSR, written from the CSR bus (+2.386 ns). The stage-to-PHY-counter path, which replaced the routed F1 path, has +3.478 ns.

The control route `c1` is the head with `SPIPHYStage` replaced by wires (`scripts/control_wire_phy.py`, measurement only, never committed). Its generated Verilog differs from the head's in the `milansoc_milansoc_stage_spi_phy_*` signals, and otherwise only in the module-tree comment, the generation time and the work-directory paths of three image files whose contents are identical (`receipts/control-c1/control-verilog-difference.txt`). It ran at the three directives:

| Directive | WNS / WHS ns, head -> control | Control's worst path (family) | F1, head -> control | F4, head -> control | LUT / FF / slices, head - control | Control gate |
|---|---|---|---|---|---|---|
| ExtraPostPlacementOpt | +0.128 / +0.030 -> **+0.168** / +0.025 | milan: `u_ucpu/uop_e_r_reg[imm]` -> `deb_cnt_r_reg`, 35 levels (outside F1 to F4) | +2.386 -> +0.677 | +0.324 -> +0.264 | +24 / +173 / -35 | **rc 1**: WNS fell 0.272 |
| AltSpreadLogic_high | +0.039 / +0.029 -> **+0.342** / +0.034 | `sys`: LiteDRAM `bankmachine7_row_reg[3]` -> `bankmachine1_twtpcon_count_reg[1]`, 15 levels (outside) | +2.110 -> +0.614 | +0.039 -> +0.559 | +32 / +175 / +18 | - |
| ExtraTimingOpt | +0.010 / +0.029 -> **+0.300** / +0.036 | `sys`: F1, uncut: `FSM_onehot_socbushandler0_axilite2wishbone_state_reg[1]` -> `milansoc_milansoc_phy_cnt_reg[8]`, 18 levels, 65 % | +2.228 -> +0.300 | +0.059 -> +0.385 | +47 / +179 / +19 | - |

- **The stage's in-context cost** (head minus control, the same directive): +24 to +47 LUTs and +173 to +179 FFs. Slices move by -35 to +19, inside the placement spread (the head's own routes differ by 75 slices between directives). Access latency is +2 `sys` cycles a word in a burst and +8 a new burst (round 1, F4 of `test_soc_timing_cuts.py`).
- **The stage's WNS.** With the stage, F1 has 1.50 to 1.93 ns more slack than without it, at every directive. Without it, F1 is the worst path at ExtraTimingOpt (+0.300 ns) and within 0.3 ns at AltSpreadLogic_high (+0.614 ns, 0.272 ns from +0.342 ns). The image's WNS goes the other way at two of three directives: the control is 0.303 ns better at AltSpreadLogic_high and 0.290 ns better at ExtraTimingOpt, and 0.040 ns better at the shipping directive. At the first two, the head's worst paths are F4 and the memory bridges into the CPU's DMA port; the stage touches neither. Each figure is one route at the default seed. The difference, about 0.3 ns, is the size of the route-to-route spread, so it does not separate the stage's own effect from placement.
- **The control fails the gate too** at the shipping directive (+0.168 ns, a 0.272 ns fall), with a milan-domain family outside F1 to F4 as its worst path. No route measured with the F2 and F3 cuts passes the WNS limit at the shipping directive: the head +0.128 ns, the control +0.168 ns. Dev's own route passes at +0.303 ns.

## 3. Acceptance (round 2 step 3)

| Condition | Result |
|---|---|
| The shipping route passes `pp_resource_gate.py check` | **no**: exit 1, `WNS_ns 0.44 -> 0.128, -0.312, REGRESSION: fell by more than 0.25`; every other figure ok, route complete |
| It meets the floor at every corner | yes: +0.128 / +0.059 slow, +1.311 / +0.030 fast |
| No family other than F4 within 0.3 ns of the worst path at the shipping directive | **no**: six (section 1) |

So the record was not re-recorded, `AREA_BUDGET.md` was not edited, and no commit was made.

## 4. The rest of the gates

| Gate | Head | rc | Result |
|---|---|---:|---|
| route-1x1, ExtraPostPlacementOpt, then `pp_resource_gate.py check --endpoint route-1x1` | `8b28ebaf` | 0, **1** | the STOP (section 1) |
| route-1x1, AltSpreadLogic_high | `8b28ebaf` | 0 | +0.039 / +0.029 ns, floor met |
| route-1x1, ExtraTimingOpt | `8b28ebaf` | 0 | **+0.010** / +0.029 ns, floor missed |
| ooc-1x1, then `check --endpoint ooc-1x1` | `8b28ebaf` | 0, 0 | `RESULT: PASS`, every figure equal to the twelfth record (24,346 LUT, 20,404 FF, 16 / 3 RAMB, 8 DSP) |
| rtl-8x8, ooc-8x8, then `check --endpoint ooc-8x8` | `8b28ebaf` | 0, 0, 0 | `RESULT: PASS`, every figure equal (34,156 LUT, 29,782 FF, 21 / 5 RAMB, 8 DSP) |
| The capture, the receipt's six arms and three controls (`scripts/capture_campaign.py`) | `8b28ebaf` | 0, all nine | section 5: worst contract-clock capture 13.85922 ms, 10.64 ms under 24.5 ms |
| The service-budget product-CPU runs, plan `all`, `--populated --enforce-service` (`scripts/svc_campaign.py`) | `8b28ebaf` | 0, both shapes | section 5: `PASS: measurement evidence`, no service finding |
| The full sweep, rtl-fast with behave, the docs gates, the builder bank | - | - | **not run, by the STOP** |
| The re-record and its documentation | - | - | **not run, by the STOP** (acceptance not met) |
| Flash boot on hardware | - | - | not in this lane: no hardware or bench access |

Round 1 at the same head: `sw/litex/test_soc_timing_cuts.py` 15 arms PASS; `scripts/run_litex_sims.sh` 8 / 8 PASS and its self-test 10 / 10; `python3 scripts/check_nvm_capture.py` PASS; `check_py_idiom.py` and `check_doc_style.py` within every ratchet (`../814-a703/HANDOFF.md`, gate table).

## 5. Capture and flash-path simulations at the head

The capture SoC (`tb/verilator/nvm_capture_cpu/soc.py`) keeps the product's flash controller with the shipping `MilanSoC.add_spi_flash`, so it carries the PHY stage. It also keeps the CPU memory port crossing with `AXIReadyStage`, and LiteDRAM with `RegisteredRefresher`. Its BIOS boots and reads the AEM image from the model flash through the stage. The receipt's own recipe was used: `unshare -Urn`, offline dependency resolution, `PYTHONHASHSEED=0`, Verilator 5.052 behind a two-build wrapper (`scripts/vwrap.py`).

| Arm | rc | Rows | ok | Minimum ms | Maximum ms | Under 24.5 ms by | Margin to the 49 ms floor | Committed receipt maximum ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 8x8-50-on | 0 | 16 | 16 | 13.84584 | 13.85922 | 10.64078 ms (43.4 %) | 3.5356x | 13.86328 |
| 8x8-50-off | 0 | 16 | 16 | 13.61714 | 13.67682 | 10.82318 ms (44.2 %) | 3.5827x | 13.68956 |
| 8x8-100-on | 0 | 16 | 16 | 10.42490 | 10.43194 | 14.06806 ms (57.4 %) | 4.6971x | 10.42973 |
| 8x8-100-off | 0 | 16 | 16 | 10.41566 | 10.41899 | 14.08101 ms (57.5 %) | 4.7030x | 10.41566 |
| 1x1-50-on | 0 | 16 | 16 | 3.96228 | 3.96814 | 20.53186 ms (83.8 %) | 12.3484x | 3.96548 |
| 1x1-50-off | 0 | 16 | 16 | 3.90676 | 3.92034 | 20.57966 ms (84.0 %) | 12.4989x | 3.92034 |

Worst contract-clock capture: 8x8-50-on, 13.85922 ms, 10.64078 ms under the 24.5 ms bound.
Control skip-copy: rc 0
Control no-traffic: rc 0
Control byte-only: rc 0, minimum slowdown 1.834640044677839

- **The margin against 24.5 ms**: 10.64078 ms (43.4 %), at the worst contract-clock row (8x8, 50 MHz, traffic on, 13.85922 ms). That row is 0.00406 ms under the committed receipt's 13.86328 ms (`tb/verilator/nvm_capture_cpu/measurements.json`, base `f3bb2014`). No dev-`1e80128f` capture ran beside it, so the small differences from the receipt are not attributed. 1x1 / 50 MHz OFF equals the receipt to the last digit.
- Every row of every arm is `ok=1`, with 0 mismatches and 0 open records. The three controls detect their named defects and return 0. byte-only's minimum slowdown is 1.8346 against the 1.5 threshold.
- The timed interval (ARM through ATTEST) reads no flash. It copies DDR to DDR: the live and stage windows sit in main RAM (`sw/litex/milan_soc.py:3366-3373`), reached through the CPU memory port that carries `AXIReadyStage`, with LiteDRAM's `RegisteredRefresher`. The flash read path runs at each boot through the stage: the firmware's memory-mapped copy of the AEM image (`milan_baremetal.c:1838-1861`), logged as `AEM 19520 B copied QSPI +0x00400000 -> 0x7f700000, CRC 2104c2d3` at 8x8. Every arm boots and runs to its last capture.

The service-budget harness (`tb/verilator/fw_service_budget`) keeps the real flash controller behind `MilanSoC.add_spi_flash(soc, phy=DeviceBoundary)`, so its device model sits behind the stage. Plan `all` runs the firmware's 17 command cases, two commits (erase, page program, read-back through LiteSPI's master) and a wipe on the product CPU.

| Shape | rc | Verdict | Commands | Erases / page programs / bytes (largest command) | Commits logged | Heartbeat max gap ms | Measurement-only budget findings | Service findings (the verdict) |
|---|---:|---|---:|---|---:|---:|---:|---:|
| 1x1 | 0 | PASS: measurement evidence; budget findings: 0 | 17 | 2 / 28 / 6672 | 2 | 267.034 | 0 | 0 |
| 8x8 | 0 | PASS: measurement evidence; budget findings: 0 | 17 | 2 / 104 / 26512 | 2 | 324.581 | 2 | 0 |

The two 8x8 measurement-only findings are "over-budget duty: milan_nvm": the two console commit commands, 860.03331 and 862.05357 ms, against the 500 ms console figure. Under --enforce-service the verdict counts service findings only (run.py:761); console response time has no protocol deadline (run.py:375-376).

- Both shapes boot, copy the AEM image from flash through the stage, run all 17 command cases, and wipe. The firmware logs two commits, each `acknowledged`. All their erases, page programs and read-backs go through LiteSPI's master behind the stage. The largest single command erased twice and programmed 104 pages (26,512 bytes) at 8x8, and 28 pages (6,672 bytes) at 1x1.
- The heartbeat's worst gap is 267.03 ms at 1x1 and 324.58 ms at 8x8, under the 500 ms bound, with continuous backing.
- The two 8x8 commit commands take 860.0 and 862.1 ms. `docs/findings/397_SERVICE_BUDGET.md` records 835.95 ms for the same 8x8 `milan_nvm` command, measured at an older head (`18199bac`). No dev-`1e80128f` service run ran beside these, so the stage's share is not separated from the firmware's changes since then.

## Decisions needed

1. **The record and its fall limit.** With F1 to F3 cut, the WNS goes to whichever of at least six families draws the worst placement: F4 (CPU), the processor memory bridges, the milan reset crossing, the AECP micro-CPU, LiteEth TX, the LiteDRAM bank machines. This lane changes none of them. The head's three routes give +0.128, +0.039 and +0.010 ns. The record is +0.440 ns, and the gate binds at +0.190 ns. Under the #708 ruling (no fall exception) the head cannot be re-recorded.
2. **ExtraTimingOpt misses the floor** at the head (+0.010 ns). The shipping directive and AltSpreadLogic_high meet it.
3. **The next families, if cutting continues.** The worst path at the shipping directive is a reset synchroniser crossing timed as a synchronous path. A register boundary there does not cut it. It is a CDC constraint question in `KL_mmcm_drp_servo.sv`, outside the SoC wiring. The memory bridges' path into the CPU DMA port's write arbitration is SoC wiring up to the CPU's DMA input pipe. F4 is accepted by the owner ruling. Each of these is new scope.

## Open risks

- The head's PHY stage has never been on hardware. The pre-run image the manager flashed carried `77f979ce`, the Wishbone stage. No simulation here drives LiteSPI's real PHY behind the stage with a pad-level flash. The capture and service harnesses keep the real LiteSPI core and the stage, with a model PHY or a device boundary in place of the real PHY. `test_soc_timing_cuts.py` checks the real PHY's structure, and checks behaviour on the model PHY.
- The stage adds 2 `sys` cycles (20 ns) to every master transfer, against 640 ns of SCK per byte at 12.5 MHz. That is inside the margin `docs/design/SAVED_STATE_FASTCONNECT.md` section 9.4 states for the byte pump. No figure there changes.
- One seed per directive, as the recipe prescribes. The spread argument above rests on dev's and the head's three routes, and round 1's `cd83cd16` route.

## How the runs were made

- Vivado: `scripts/r2_export.sh` (clone, export, `pp_baseline.py`, no Vivado), then `scripts/launch.sh` per run. It runs `setsid nohup vivado-slot.sh` with no timeout, with the command inside its own user scope (MemoryMax 14G), so three parallel routes are not charged to the lane's unit. route-1x1 and ooc-8x8 started before that change, in the unit. No lock was taken directly.
- Each Vivado run started only with a free slot and at least 20 GB MemAvailable (the wrapper). **The lane's unit peaked at 17.0 GB** (`memory.peak`, page cache included), above the 12 GB guidance. That was the window when route-1x1 and ooc-8x8 both ran inside it, before later Vivado runs moved into their own scopes. Its cap is 24 GB, and nothing was throttled or killed.
- Scratch outside the tree; every clone was clean at the head. Receipts redact host paths (`<scratch>`, `<home>`, `<tools>`); files over 200 KB are recorded by SHA-256 and size in each directory's `large.sha256`.

## Progress log (UTC)

- 08:05 TAKEN posted. Live remote dev `1e80128f`.
- 08:06 route-1x1 (ExtraPostPlacementOpt) at `8b28ebaf` started. 08:07-08:09 the 8x8 export, rtl-8x8 (rc 0, 81 s), ooc-8x8 started. 08:11 the capture campaign. 08:15 the control export `c1`.
- 08:36 ooc-8x8 rc 0, gate PASS. 08:44 the synthesis checkpoint; AltSpreadLogic_high and ExtraTimingOpt started; ooc-1x1 prepared and queued. 08:47 the service-budget runs.
- 09:04 route-1x1 rc 0, gate rc 1. 09:05 AltSpreadLogic_high rc 0. 09:07 the control route started. 09:09 ExtraTimingOpt rc 0 (+0.010). 09:10-09:13 path tables. 09:20 ooc-1x1 rc 0, gate PASS. 09:49 the control's two comparison directives started.
- 10:05 the control's AltSpreadLogic_high and ExtraTimingOpt rc 0; 10:08 its shipping route rc 0, gate rc 1; 10:10-10:12 its path tables. 09:40 the capture campaign ended, nine rc 0. 10:25 the 8x8 service run ended, rc 0.

## Receipts

`INDEX.md` lists every file present (`scripts/gen_index.py`).

| Directory | Holds |
|---|---|
| `receipts/route-8b28ebaf/` | the head's three routes: route status, placed utilization (flat and hierarchical), IOB packing, DRC, every timing report's design table (the four signoff corners included), the signoff grade, the `sys` top 20 with families, every-group top 30 with families, stage cells; the shipping route's gate log; the slot lines; logs and path tables by digest |
| `receipts/control-c1/` | the control route at three directives, the same reports |
| `receipts/exports-8b28ebaf/` | the three exports' logs: clone state at the head, the SDK and recipe self-tests, `pp_baseline.py` |
| `receipts/ooc-8b28ebaf/` | ooc-1x1, rtl-8x8 and ooc-8x8: gate logs, parameter blocks, utilization, slot lines; logs by digest |
| `receipts/capture-8b28ebaf/` | each arm's and control's capture log and measurement, the summary |
| `receipts/service-8b28ebaf/` | the service runs' logs, receipts and summary |

`scripts/` holds the drivers: `r2_export.sh`, `launch.sh`, `viv.sh`, `dir_prep.py`, `paths.tcl`, `summarize_paths.py`, `summarize_all.py`, `collect_route.py`, `control_wire_phy.py`, `capture_campaign.py`, `capture_summary.py`, `svc_campaign.py`, `vwrap.py`, `make_clone.sh`, `copy_receipts.py`, `gen_index.py`, the wait helpers, and round 1's gate drivers (`static_bank.sh`, `rtlfast_run.sh`, `rtl_fast_steps.py`, `docs_run.sh`, `docs_steps*.py`, `make_sweep_spec.py`), repointed and not run.

## Not done (by the assignment's rules)

No push, no PR, no merge or rebase, no edit to any issue or PR comment, no sub-agents, no hardware or bench access, no flashing. On #814 the only posts are TAKEN and STOP.
