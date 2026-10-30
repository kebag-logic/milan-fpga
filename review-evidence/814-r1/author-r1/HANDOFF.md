# HANDOFF: #814 SoC sys-domain timing cuts, executor [A703]

Status: **STOP** at head `8b28ebaf035e786ccf5b8e50098dbc111f51831f` (worktree clean, every submodule at its gitlink, live remote dev `1e80128f` unchanged). Nothing pushed.

**STOP reason: route-8x8 does not fit** (the assignment's STOP "a route does not fit"). The 8x8 export at its own place directive (AltSpreadLogic_high), recipe unchanged, at `139949e2`: `opt_design` completes, then DRC UTLZ-1 refuses placement. The design needs **70,686 LUT-as-logic cells; the device has 63,400** (7,286 over, 11.5 %). The placer never ran (`receipts/route-8x8-139949e2/`). That is not this lane's area: its three stages cost about 132 LUTs out of context (section 4). `docs/integration/BUILDING.md` already says the `ax8x8` recipe "has never produced a bitstream", and `AREA_BUDGET.md` records 8x8 as "Synthesis only, no integrated-fit claim". So the issue's acceptance "route-1x1 and route-8x8 ... no longer have either path within 0.3 ns" cannot be met for route-8x8 on this device. That needs an owner decision.

State at the STOP: the measure-first bank is done; three cuts are implemented and graded (one placement measured insufficient and moved); the head's route-1x1 has **not** run.

- Lane: `814-soc-timing-cut`, from dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141` (verified: `git merge-base HEAD origin/dev`)
- origin: https://github.com/kebag-logic/milan-fpga.git (verified); no submodule git command was run
- Assignment: the latest [A10] comment on #814 (issuecomment-6514717735)
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/814#issuecomment-6514848377
- STOP: https://github.com/kebag-logic/milan-fpga/issues/814#issuecomment-6517869395 (the lane's only other post)

## Commits (one-line, no body, no trailer)

| # | Commit | Change |
|---|---|---|
| 1 | `cd83cd16` | a registered Wishbone stage between the decoder and the SPI-flash core, its test and the LiteX-sims inventory entry; routed, measured insufficient (section 2) |
| 2 | `a166465b` | the CPU memory port's registered READY on aw, w and ar (F2), its test arms, docs |
| 3 | `77f979ce` | LiteDRAM's own refresher behind registered valid and last (F3, added to the scope), its test arms |
| 4 | `139949e2` | READY registered on aw and ar alone (w had more than 4.1 ns slack at every directive) |
| 5 | `8b28ebaf` | the flash boundary moved between LiteSPI's core and its PHY; the Wishbone stage removed |

## 1. Measure first: dev `1e80128f` at the unchanged recipe

Bank: `scripts/route_bank.sh dev 1e80128f r1 dir paths` (the #787 and #806 lanes' bank, recipe `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` unchanged, `--single-thread-synthesis`, `general.maxThreads` 32, Vivado 2026.1), in a clean clone, one Vivado run at a time under the exclusive lock, each started above 20 GB MemAvailable. Route-1x1 04:16 -> 05:08 UTC (52 min), AltSpreadLogic_high 05:08 -> 05:22, ExtraTimingOpt 05:22 -> 05:37, from route-1x1's own synthesis checkpoint, default seed. `scripts/paths.tcl` reopened each routed checkpoint and wrote the worst setup path per `sys` endpoint (5,000 endpoints) with levels, data delay and its routing part. `scripts/summarize_paths.py` writes the top 20 and the families: `receipts/measure-dev/top20-<directive>.md`.

Dev's route-1x1 reproduces the #803 merge route exactly: 51,801 LUT, 53,760 FF, 15,834 slices, WNS +0.303 ns, WHS +0.028 ns; `pp_resource_gate.py check` PASS against the twelfth record (WNS fell 0.137 ns, tolerance 0.25).

| Directive | WNS ns | Worst family | F1 bridge -> SPI-flash | F2 LiteDRAM -> crossing FIFO read register | F3 ZQCS timer -> bank machines | F4 CPU DMA write bridge |
|---|---:|---|---:|---:|---:|---:|
| ExtraPostPlacementOpt (shipping) | +0.303 | F3 | +0.627 | +0.689 | **+0.303** | +0.603 |
| AltSpreadLogic_high | +0.230 | F2 | +0.816 | **+0.230** | +0.432 | +0.353 |
| ExtraTimingOpt | +0.106 | F2 | +0.784 | **+0.106** | +0.572 | +0.686 |

What the 20 worst paths are, per directive (full tables in the receipts):

- Shipping directive: all 20 are F3, `milansoc_sdram_zqcs_timer_count1_reg[13]` into bank machines 0 to 7 (`level`, `state`, `trascon`, `trccon`, `twtrcon`), 14 to 16 levels, 73 to 77 % routing. Cells: the ZQCS timer, the bank machines' refresh state, the multiplexer's `choose_req` grant, bank machine 7's command-FIFO read enable, its `level` CE. All inside LiteDRAM's controller.
- AltSpreadLogic_high: F2 holds the first 10 (`milansoc_read_beat_count_reg[4]` -> `storage_10_dat1_reg`, `storage_13_dat1_reg`, 14 levels, 79 % routing), then F4 (`downW_header_reg` -> `onW_buffer_N_strb`, +0.353, 16 levels, 76 %), then F3.
- ExtraTimingOpt: F2 holds the first 20 with a bank-machine start (`milansoc_sdram_bankmachine2_level_reg[1]` -> `storage_13_dat1_reg`, 14 levels, 79 %).

Confirmation, and what joins the scope:

- F1 never decides dev's WNS: +0.627 to +0.816 ns. It decided the #806 route (+0.032) and earlier records, and it is 0.324 ns from the worst path at the shipping directive.
- F2 is the issue's SDRAM family: any LiteDRAM flip-flop (the burst-to-beat counters, the AXI write buffer level, the bank machines' FIFO levels) into a crossing FIFO's registered read. It decides two of the three directives.
- **F3 joins the scope**: 0.202 ns from F2 at AltSpreadLogic_high, and the shipping directive's worst path. Cut in the SoC wiring through LiteDRAM's `ControllerSettings.refresh_cls` hook (section 3b), no patch.
- **F4 joins the scope by the same rule** (0.123 ns from F2 at AltSpreadLogic_high; 0.024 ns from F1 at the shipping directive). It is not cut. Every cell is inside the generated CPU netlist: the DMA write bridge's aligner, the down arbiter, the DMA filter, the unified mBus crossing's tracker and the bridge's compactor (`VexiiRiscvLitex_*/dma_bridge_write_bridge/...`), so no stage in `milan_soc.py` sits on it. A boundary there needs a CPU-generator change, outside this ruling. Recorded as an open decision.
- Below the 0.3 ns line and not in scope: `milansoc_ws0_reg -> milansoc_tmod1_reg` (the AECP response-buffer bridge's strobe into its watchdog counter, `pp_rw_bridge`, 12 levels), +0.427 at ExtraTimingOpt, 0.321 ns from F2; `bankmachineN_pipe_valid_source_payload_addr -> bankmachineN_level` (inside a bank machine), +0.465, 0.359 ns.

## 2. The bridge-to-SPI-flash cut (F1)

Where: the SoC wiring, `sw/litex/milan_soc.py`, no LiteX patch. Two placements were measured.

**First placement, measured insufficient: a registered Wishbone stage between the decoder and the flash core** (commit `cd83cd16`, the issue's first option). Route-1x1 at `cd83cd16` (05:41 -> 06:30 UTC, gate PASS: 51,791 LUT, 53,823 FF, 15,844 slices, WNS +0.253, WHS +0.033; `receipts/cut1-cd83cd16/`): the path now started at the stage's own address register and still ran **17 levels into the PHY counter at +0.254 ns, 0.001 ns from the worst path** (`milansoc_socbushandler_adapted_interface_adr_reg[22] -> milansoc_spiflash_phy_cnt_reg[8]`, 9.696 ns, 60 % routing). Along it: the origin offset adder (1.3 ns), LiteSPI's burst compare (2.0 ns), the mmap FSM and chip-select logic into the PHY (2.2 ns), and the PHY's clock-generator down-counter, a ripple of eight LUTs (4.0 ns). The bridge had contributed three levels. So the boundary has to sit between the mmap FSM and the PHY.

**Shipping placement: between LiteSPI's core and its PHY** (commit `8b28ebaf`, which also removes the Wishbone stage: with the PHY-side boundary it cut nothing still long, and it cost two bus cycles an access and flip-flops at 16 free slices).

- `SPIPHYStage` (`milan_soc.py:2465`): the core-to-PHY command stream and the PHY-to-core data stream each pass a LiteX `stream.Buffer(pipe_valid=True, pipe_ready=True)` (registered valid, payload and ready), and the chip select passes a flip-flop. The PHY sees the chip select and the command one cycle later, both together, so every transfer keeps its place inside the chip select (F5).
- `stage_spi_phy` (`:2496`): LiteSPI reads only `phy.sink`, `phy.source` and `phy.cs` (and `flash`, `dummy_bits`), so those three move to the stage, and the PHY keeps its own behind it. The stage is the PHY's submodule `stage`, so the PHY's CSR names (`spiflash_phy_clk_divisor`, `spiflash_phy_mode`) are unchanged.
- `MilanSoC.add_spi_flash` (`:3670`): LiteX's `add_spi_flash`, with the PHY staged. Without `phy` it builds the PHY LiteX would build (the same divisor, pads and `LiteSPIPHY`). A caller's own PHY is staged as well. So the capture SoC (`ProductSimulation.add_spi_flash` calls `super()` with `LiteSPIPHYModel`) and the service-budget build (`MilanSoC.add_spi_flash(soc, phy=DeviceBoundary)`) carry the stage too. Neither harness file changes. `MilanSoC.__init__` keeps its `self.add_spi_flash(...)` call (`:3183`).
- The Wishbone contract is untouched: nothing between the decoder and LiteSPI's mmap changed.
- Latency: **+2 bus cycles (sys, 100 MHz: 20 ns) per word in a burst, +8 per new burst** (command, address, dummy and data, one cycle each way). F4 measures every read of a burst, new bursts and a read after LiteSPI's 256-cycle burst timeout: `[8, 2, 2, 2, 8, 2, 8, 8, 2, 2, 8, 8]` against the wired control. At the shipping divisor (8) one 32-bit word takes 256 sys cycles of SCK, so a burst read is about 0.8 % slower.

## 3. The SDRAM-arbitration-to-FIFO cut (F2)

Where: the SoC wiring, inside `cross_cpu_memory_ports` (`milan_soc.py:2389-2391`), between the CPU memory port's `AXIClockDomainCrossing` and the port LiteDRAM connects. The LiteDRAM port contract is untouched: LiteDRAM's `add_sdram` still receives an AXI4 port of the same widths, id width and version, and its native port sees the same handshakes (D3, D4).

- `AXIReadyStage` (`:2397`): a LiteX `stream.PipeReady` on `aw` and `ar`. The crossing FIFO's read enable becomes the pipe's registered "empty"; the payload still passes in the same cycle and a held beat goes out on the next ready. The AXI handshake keeps its order and its valid-until-ready rule.
- `w`, `b` and `r` pass through. Commit `a166465b` staged `w` as well; `139949e2` drops it. The `w` FIFO's read register (`storage_11`, 293 bits) had no endpoint among the 5,000 worst `sys` endpoints at any dev directive (the 5,000th is +4.1 to +4.3 ns), so its pipe cost about 290 flip-flops and multiplexers for no measured path. Every F2 endpoint is in `storage_10` (aw) or `storage_13` (ar), 42 each.
- Latency: **0 cycles**. D4 requires LiteDRAM's native port to see the same command and write-data handshakes in the same cycles with the stage and without it, and each read to take the same milan cycles.

## 3b. Added to the scope: the ZQCS-timer-to-bank-machine cut (F3)

Where: the SoC wiring, through LiteDRAM's own hook (`ControllerSettings.refresh_cls`), no patch.

- `RegisteredRefresher` (`milan_soc.py:2430`): LiteDRAM's own `Refresher`, with its `cmd.valid` and `cmd.last` registered on the way to the controller. The command fields already leave LiteDRAM's executers from flip-flops, and `ready` passes back unchanged.
- `add_staged_sdram` (`:2454`): LiteX's `add_sdram` with `ControllerSettings(refresh_cls=RegisteredRefresher)`; every other controller setting keeps LiteDRAM's default, as before. `MilanSoC` calls it (`:3186`).
- Effect: each refresh and ZQCS starts and ends one cycle later, with its own tRP, tRFC and tZQCS spacing. Z3 records the DFI: precharge-all and refresh each exactly one cycle later at the same 782-cycle spacing. Access latency: 0 cycles, except an access waiting on a refresh waits one cycle more.
- An observation, not changed: LiteDRAM issues a ZQCS only when its one-cycle ZQCS timer pulse meets the refresh sequencer's end (`litedram/core/refresher.py`, `RefreshTimer` and `DO-REFRESH`). Neither simulation reached one, with the stage or without it. The timing path exists in the netlist all the same.

## 4. Costs

Each stage alone, out of context on the shipping part (`xc7a100tfgg484-2`) with the shipping synthesis and opt directives (AreaOptimized_high, ExploreArea), placed: `scripts/gen_stage_verilog.py` exports each from the head at the SoC's widths, `scripts/stage_ooc.tcl` implements it (`receipts/stage-costs-8b28ebaf/`, 0 errors). Context-free figures: in the image, packing shares slices and synthesis may trim unread bits.

| Cut | LUT | FF | Slices (alone) | Added access latency, sys cycles (10 ns) |
|---|---:|---:|---:|---|
| F1 `SPIPHYStage` (core2phy 60 bits, phy2core 32, cs) | 54 | 199 | 49 | +2 a word in a burst, +8 a new burst (F4) |
| F2 `AXIReadyStage` (aw, ar; 73-bit words, id 8) | 78 | 150 | 39 | 0 (D4) |
| F3 `RegisteredRefresher` minus LiteDRAM's `Refresher` | +0 (67 vs 67) | +2 (58 vs 56) | -2 (23 vs 25, placement) | 0; a refresh starts and ends one cycle later (Z3) |
| Total | about 132 | about 351 | - | - |

In context, routed, only the dropped placement was measured. The Wishbone stage at `cd83cd16` moved dev's route by -10 LUT, +63 FF and +10 slices (51,801 / 53,760 / 15,834 -> 51,791 / 53,823 / 15,844), and its access latency was +2 cycles. The head's route-1x1 did not run (STOP), so its in-context slice cost at 16 free slices is unmeasured.

## Changes (file:line at the head, and the reason)

| File:line | Change | Reason |
|---|---|---|
| `sw/litex/milan_soc.py:2381-2391` | `cross_cpu_memory_ports` builds a second sys-side AXI port and puts `AXIReadyStage` between the crossing and the port LiteDRAM gets | F2: LiteDRAM's ready was the crossing FIFOs' read enable |
| `sw/litex/milan_soc.py:2397` | `AXIReadyStage`: `PipeReady` on aw and ar; w, b, r pass through | F2 boundary, no added cycle; w measured outside the family |
| `sw/litex/milan_soc.py:2430` | `RegisteredRefresher`: LiteDRAM's `Refresher` with `cmd.valid` and `cmd.last` registered | F3: the ZQCS timer reached every bank machine through `refresh_req` |
| `sw/litex/milan_soc.py:2454`, `:3152` | `add_staged_sdram`: `add_sdram` with `ControllerSettings(refresh_cls=RegisteredRefresher)`; `MilanSoC` calls it | F3 through LiteDRAM's own hook; other controller settings stay at their defaults |
| `sw/litex/milan_soc.py:2465` | `SPIPHYStage`: `stream.Buffer` (valid, payload, ready registered) each way and a chip-select flip-flop | F1 boundary between the mmap FSM and the PHY |
| `sw/litex/milan_soc.py:2496` | `stage_spi_phy`: the stage takes over `phy.sink`, `phy.source`, `phy.cs`; it is the PHY's submodule | LiteSPI reads only those; the PHY's CSR names are unchanged |
| `sw/litex/milan_soc.py:3670` | `MilanSoC.add_spi_flash`: LiteX's, with the PHY staged; builds LiteX's PHY when none is given | every SoC from this class, the capture and service-budget harnesses included, carries the stage |
| `sw/litex/test_soc_timing_cuts.py` (new, 618 lines) | 15 arms (next section) | the assignment's simulation check with a planted unregistered path, by construction |
| `scripts/run_litex_sims.sh:107` | `test_soc_timing_cuts` in the pinned inventory | the aggregate refuses an unlisted `test_*.py` |
| `ci/image/exec-audit.json:1206-1212` | the generated stand-in the aggregate's self-test writes for the new member (digest `57b84e8b...`, computed from the runner's own template and checked against the existing `test_cpu_memory_port_cdc` entry) | the image audit's reviewed list names every such stand-in |
| `docs/testing/TESTING.md:722-741` | the new member's paragraph | TESTING.md section 2 names each member |
| `docs/litex/CLOCK_DOMAINS.md:276-281` | the crossing's new stage, in the #359 CPU DDR list | the CPU DDR crossing's description |

Not changed: the Vivado recipe, the directives, the floors, any constraint or pblock, `AREA_BUDGET.md`, the resource record, CHANGELOG (the record and its prose wait for an accepted route).

## New checks, planted mutants and failing words

`sw/litex/test_soc_timing_cuts.py` (in `scripts/run_litex_sims.sh`). Each path is built on the real LiteX, LiteSPI and LiteDRAM code through the shipping call: `MilanSoC.add_spi_flash` behind an AXI-Lite master on the Wishbone bus (so LiteX inserts its real AXI-Lite-to-Wishbone bridge, decoder and origin offset), and `cross_cpu_memory_ports` plus `add_staged_sdram` under LiteX's `add_sdram`. The structural arms read the elaborated migen netlist, never text. `Netlist` indexes every combinational and registered assignment by its target, its index and its enclosing conditions. `cone()` walks back from an endpoint to the flip-flops that reach it through logic alone. Each planted mutant is built by substituting one class in `milan_soc` for the build, and must fail the named arms.

| Arm | Checks | Planted mutant and the failing words |
|---|---|---|
| F0 | only stage flip-flops drive the PHY's command, ready and chip select and the core's data and ready | `WirePHYStage` (the stage's faces wired to the PHY): F0 fails |
| F1 | no AXI-Lite bridge or LiteSPI core flip-flop reaches a PHY flip-flop through the PHY's faces, and no PHY flip-flop a core flip-flop | `WirePHYStage`: 89 forward and 21 back paths, among them `fsm_state -> litespiclkgen_cnt` (the bridge state into the PHY counter, the routed path); F2 requires that name |
| F3 | twelve reads through the stage return the image: a burst, new bursts, after the 256-cycle burst timeout | - |
| F4 | added cycles per read against the wired control are exactly `[8, 2, 2, 2, 8, 2, 8, 8, 2, 2, 8, 8]` | - |
| F5 | the PHY takes every command inside its chip select, with the same chip-select edges and commands in the same order as without the stage (30 commands) | - |
| D0, D1 | the stage feeds the read address of the aw and ar crossing FIFOs, and no LiteDRAM converter or core flip-flop reaches either LUTRAM read address through logic alone | `WirePassThrough` (the AXI faces wired): 76 paths, among them `axiburst2beat_beat_count -> memory_adr`; D2 requires that name |
| D3 | LiteDRAM's native port sees each write's command, word and full mask, then each read's command, in order, at the addresses written | - |
| D4 | the native port sees the same handshakes in the same cycles with the stage and without it; each read takes the same milan cycles (`[12, 11, 15, 14]`) | - |
| Z0, Z1 | the refresh request is the stage's own flip-flops (143 controller flip-flops read it), and no refresher flip-flop reaches a bank-machine or multiplexer flip-flop through it | LiteDRAM's own `Refresher` in place of the stage: 715 paths, among them `refreshtimer_count -> syncfifo_level`; Z2 requires that name |
| Z3 | precharge-all and refresh on the DFI, each exactly one cycle later at the same spacing (8 commands over 3,200 cycles, first at 788 against 787) | - |

The Wishbone stage's arms (at `cd83cd16` to `139949e2`) went with it at `8b28ebaf`.

## Resources and route timing

Vivado 2026.1, recipe unchanged, one run at a time under the exclusive lock, each above 20 GB MemAvailable, each in a clean clone. Every route checked with `pp_resource_gate.py check` against the committed twelfth record (#799).

| Run | Head | Vivado rc | Gate | LUT | FF | Slices | WNS / WHS ns | Worst family |
|---|---|---:|---|---:|---:|---:|---|---|
| route-1x1 (shipping) | dev `1e80128f` | 0 | PASS | 51,801 | 53,760 | 15,834 | +0.303 / +0.028 | F3 |
| AltSpreadLogic_high | dev | 0 | - | 51,846 | 53,759 | 15,795 | +0.230 / +0.014 | F2 |
| ExtraTimingOpt | dev | 0 | - | 51,829 | 53,758 | 15,794 | +0.106 / +0.054 | F2 |
| route-1x1 | `cd83cd16` (Wishbone stage) | 0 | PASS | 51,791 | 53,823 | 15,844 | +0.253 / +0.033 | F4 +0.253, F1 +0.254 |
| route-8x8 | `139949e2` | **1** | - | - | - | - | - | **DRC UTLZ-1: 70,686 LUT-as-logic cells for 63,400 sites; placer not run** |

At `cd83cd16` the other families were F3 +0.497 (0.244 ns from the worst) and F2 +1.256. F2 had no logic change, so that is placement alone, the size of the route-to-route spread. Receipts: `receipts/measure-dev/`, `receipts/cut1-cd83cd16/`, `receipts/route-8x8-139949e2/`.

## Gate table

Head `8b28ebaf` unless noted; every command unpiped with its own log and rc.

| Gate | Head | rc | Result |
|---|---|---:|---|
| `sw/litex/test_soc_timing_cuts.py` (LiteX interpreter) | `8b28ebaf` worktree | 0 | 15 arms, 0 failures, `RESULT: PASS` |
| `scripts/run_litex_sims.sh <logs>` | `139949e2` clone | 0 | 8 / 8 members PASS (1,021 s) |
| `scripts/run_litex_sims.sh <logs>` | `8b28ebaf` clone | 0 | 8 / 8 members PASS (961 s), `test_soc_timing_cuts` among them |
| `scripts/run_litex_sims.sh --selftest` | `8b28ebaf` clone | 0 | 10 checks, 10 PASS |
| `python3 scripts/check_nvm_capture.py` | `8b28ebaf` clone | 0 | `PASS: capture census, clocks, both timing arms and receipt agree` |
| `python3 scripts/check_py_idiom.py` | `8b28ebaf` worktree | 0 | every ratchet held (too many parameters 7 <= 7, unannotated 0 <= 0) |
| `python3 scripts/check_doc_style.py` | `8b28ebaf` worktree | 0 | 23 current documents OK |
| `sw/litex/test_cpu_memory_port_cdc.py` | `139949e2` worktree | 0 | `RESULT: PASS` through the staged hook |
| route-1x1, three directives, top-path reopen | dev | 0 | section 1 |
| route-1x1 + gate | `cd83cd16` | 0, 0 | section 2 |
| route-8x8 | `139949e2` | **1** | the STOP |

Not run, by the STOP: the full sweep, rtl-fast, the docs workflow gates, the builder bank, the capture re-measurement and the flash-boot simulations, the SoC and DDR-backed suites at the head, route-1x1, ooc-1x1 and ooc-8x8 at the head, `pp_resource_gate.py` at the head and the re-record.

## STOP conditions

| Condition | Met? |
|---|---|
| A cut needs a recipe or directive change, or a pblock | no: all three are in `milan_soc.py`, F3 through LiteDRAM's own `refresh_cls` hook |
| A route does not fit, or misses the +0.030 ns floor | **yes: route-8x8 does not fit** (70,686 LUTs for 63,400); every route-1x1 met the floor |
| The capture misses 24.5 ms | not measured (STOP); the compiler-free gate passes on the committed receipt |
| A cut changes bus behaviour a suite sees, beyond latency | none seen: D3, D4, F3, F5 and Z3 grade exactly that; the suites did not run |
| The two paths stay within 0.3 ns of the worst path after both cuts | not measured at the head (STOP). At `cd83cd16` F1 was still within 0.001 ns, which is why the boundary moved |

## Open risks and questions

1. **Route-8x8 cannot fit this device** at the unchanged recipe: the gate list and the acceptance need an owner decision (for example, keep 8x8 synthesis-only as `AREA_BUDGET.md` records it, or a different 8x8 shape).
2. **F4, the CPU's DMA write bridge, joins the scope by the 0.3 ns rule and is not cut.** It runs from the aligner (`downW_header_reg`) through the down arbiter, the DMA filter and the mBus crossing's tracker into the bridge's compactor and the DMA bus input pipe, every cell inside the generated CPU netlist (`VexiiRiscvLitex_*`). It was 0.123 ns from F2 at AltSpreadLogic_high, 0.024 ns from F1 at the shipping directive, and the worst path at `cd83cd16` (+0.253 ns, 19 levels). A boundary there needs a CPU-generator change, outside the ruling's "SoC wiring". Without one, F4 is likely to set the head's WNS.
3. **The head's flash boundary is unrouted.** The Wishbone placement was measured insufficient; the PHY-side placement is graded in simulation only. Its in-context slice cost at 16 free slices is unknown.
4. Placement spread: F2 moved 0.567 ns between two routes with no change to its logic, so one route per head is weak evidence for a 0.3 ns margin.
5. LiteDRAM issues a ZQCS only when its one-cycle ZQCS timer pulse meets the refresh sequencer's end, so ZQCS is rare in hardware. Upstream behaviour, unchanged here; the path is in the netlist regardless.
6. The `ci/image/exec-audit.json` entry is computed from the runner's template; the image audit itself (#737) did not run here.

## Receipts

Everything cited is under `receipts/`, host paths replaced by placeholders (`<scratch>`, `<home>`, `<tools>`). A file over 200 KB is not copied: its SHA-256 and size are in that directory's `large.sha256`. `INDEX.md` lists every file present, generated by `scripts/gen_index.py` from the files themselves.

| Directory | Holds |
|---|---|
| `measure-dev/` | dev's bank log; route-1x1 at the three directives (EPPO, ASLH, ETO): route status, placed utilization (flat and hierarchical), IOB packing, DRC, every timing report's design table, the top 20 with families; the gate against the twelfth record |
| `cut1-cd83cd16/` | the Wishbone placement's route-1x1, the same reports, and its gate |
| `route-8x8-139949e2/` | the 8x8 run's DRC UTLZ-1 lines, its `opt_design` lines and the bank's lines; the full log by digest |
| `stage-costs-8b28ebaf/` | each stage's out-of-context placed utilization, the stage Verilog digests and the AXI id width |
| `litexsims-139949e2/`, `litexsims-8b28ebaf/` | the LiteX simulation aggregate and its self-test, the new member's log, every member log by digest |
| `head-8b28ebaf/` | the new test's full run and `check_nvm_capture.py` at the head |

`scripts/` holds the drivers: `route_bank.sh` (the #787 and #806 bank, steps r1, dir, o1, r8, o8, paths), `directive_sweep.sh` (the recipe's snippet), `paths.tcl`, `summarize_paths.py`, `collect_route.py`, `gen_stage_verilog.py`, `stage_ooc.tcl`, `queue.sh` (stopped after the 8x8 run), `make_clone.sh`, `env.sh`, `bg.sh`, the wait helpers, `copy_receipts.py`, `gen_index.py`, and the #806 lane's gate drivers adapted for a run that the STOP cancelled (`rtlfast_run.sh`, `rtl_fast_steps.py`, `docs_run.sh`, `docs_steps*.py`, `static_bank.sh`, `make_sweep_spec.py`).

## Not done (by the assignment's rules)

No push, no PR, no merge or rebase, no edit to any issue or PR comment, no sub-agents, no hardware or bench access, no flashing. On #814 the only posts are TAKEN and STOP.
