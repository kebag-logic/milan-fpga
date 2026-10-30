[A703] STOP

Head: `8b28ebaf035e786ccf5b8e50098dbc111f51831f` (branch `814-soc-timing-cut`, five commits on dev `1e80128f`; local, not pushed, no PR).

**STOP: route-8x8 does not fit** (the assignment's STOP "a route does not fit"). At `139949e2`, the 8x8 export at its own place directive (AltSpreadLogic_high), recipe unchanged, completes `opt_design`. Then DRC UTLZ-1 refuses placement: the design needs **70,686 LUT-as-logic cells for 63,400 sites** (7,286 over, 11.5 %), so the placer never ran. The three stages below cost about 132 LUTs out of context, so this is not their area. `docs/integration/BUILDING.md` already records that the `ax8x8` recipe has never produced a bitstream. The acceptance's route-8x8 half needs an owner decision.

**1. Measured first**: dev `1e80128f`, route-1x1 at the unchanged recipe, its three directives (default seed), top 5,000 `sys` endpoints. Dev's route reproduces #803's figures exactly (51,801 LUT, 53,760 FF, 15,834 slices) and passes the gate.

| Directive | WNS ns | Worst family | F1 flash | F2 LiteDRAM -> crossing FIFO | F3 ZQCS timer -> bank machines | F4 CPU DMA write bridge |
|---|---:|---|---:|---:|---:|---:|
| ExtraPostPlacementOpt | +0.303 | F3 (14 levels, 73 % routing) | +0.627 | +0.689 | +0.303 | +0.603 |
| AltSpreadLogic_high | +0.230 | F2 (14 levels, 79 %) | +0.816 | +0.230 | +0.432 | +0.353 |
| ExtraTimingOpt | +0.106 | F2 (14 levels, 79 %) | +0.784 | +0.106 | +0.572 | +0.686 |

- The two named families decide two of the three directives. The shipping directive's 20 worst paths are all F3: LiteDRAM's ZQCS timer into the bank machines, inside its controller.
- F2 is broader than the named path. Any LiteDRAM flip-flop (burst-to-beat counters, write buffer level, bank-machine FIFO levels) reaches the aw or ar crossing FIFO's registered read, never the w FIFO.
- **Added to the scope by the 0.3 ns rule:** F3 (0.202 ns from F2) and F4 (0.123 ns from F2). F4 is **not cut**: every cell is inside the generated CPU netlist (the DMA write bridge's aligner, arbiter, filter, mBus tracker and compactor), so no SoC-wiring stage reaches it. Cutting it needs a CPU-generator change.

**2-3. The cuts**, all in `sw/litex/milan_soc.py`, no LiteX patch, recipe and directives unchanged:

| Family | Boundary | LUT / FF / slices, alone | Added latency, sys cycles |
|---|---|---|---|
| F1 | `SPIPHYStage` between LiteSPI's core and its PHY: registered command and data streams and chip select | 54 / 199 / 49 | +2 a word in a burst, +8 a new burst |
| F2 | `AXIReadyStage`: `PipeReady` on the CPU memory port's aw and ar, after its crossing | 78 / 150 / 39 | 0 |
| F3 | `RegisteredRefresher`: LiteDRAM's own refresher with valid and last registered (`refresh_cls`) | +0 / +2 / - | 0; refresh one cycle later |

- The issue's first option, a registered Wishbone stage in front of the flash core (`cd83cd16`), was routed: gate PASS, WNS +0.253. The path then ran from the stage's own address register, **17 levels into the PHY counter at +0.254 ns, 0.001 ns from the worst path**: the burst compare, the mmap FSM and the PHY counter carry it. So `8b28ebaf` moves the boundary between the core and the PHY and drops the Wishbone stage.
- New check `sw/litex/test_soc_timing_cuts.py` (in the LiteX simulation inventory), 15 arms. It walks the elaborated migen netlist on the real LiteX, LiteSPI and LiteDRAM code through the shipping calls. With each stage replaced by wires, or by LiteDRAM's own refresher, it fails naming `fsm_state -> litespiclkgen_cnt`, `axiburst2beat_beat_count -> memory_adr` and `refreshtimer_count -> syncfifo_level`. Its behaviour arms grade flash data and exact added cycles, chip-select alignment, LiteDRAM's native port cycle for cycle and the DFI refresh one cycle later.

**At the head:** the new test 15 / 15 arms; the LiteX simulation aggregate 8 / 8 and its self-test 10 / 10; `check_nvm_capture.py` PASS; the Python idiom and doc style gates within every ratchet.
**Not run, by the STOP:** route-1x1 at the head and the standalone endpoints; the full sweep, rtl-fast, the docs gates and the builder bank; the capture re-measurement and the flash-boot simulations; the resource gate at the head and the re-record.

**Decisions needed:** (1) route-8x8 in the gate list and the acceptance, on a device it does not fit; (2) F4, which the SoC wiring cannot cut and which was the worst path at `cd83cd16`.
