[A703b] STOP

Head: `8b28ebaf035e786ccf5b8e50098dbc111f51831f`, unchanged from round 1, because round 2 added no commit (branch `814-soc-timing-cut`, five commits on dev `1e80128f`; local, not pushed, no PR).

**STOP.** Step 3's acceptance is not met, and two of the remaining STOP conditions hold:
1. **The shipping route fails `pp_resource_gate.py check` (exit 1).** WNS is +0.128 ns against the +0.440 ns record, a 0.312 ns fall against the 0.25 ns limit. Every resource figure passes: LUT -185, FF +315, slices 15,764 (86 free), RAM and DSP unchanged. WHS is +0.030 ns.
2. **A family outside F1 to F4 lies within 0.3 ns of the worst path at the shipping directive.** It is the worst path itself. `FDPE_3`, the milan-domain reset flip-flop (50 MHz), drives the MMCM servo's PS-domain reset synchroniser `mmcm_servo/psrst_sync_r_reg[0]` (200 MHz; `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:1292-1296`). The path is 1 LUT and 86 % routing, and the crossing is timed as synchronous with a 5 ns requirement. At dev's routes it had +1.975 ns or more. Five more families outside F1 to F4 lie within 0.3 ns: the AECP micro-CPU on the milan clock (+0.246, +0.393, +0.411 ns), the memory bridges' `ws1` into the CPU DMA port's write arbitration (+0.348), and LiteEth TX on the Ethernet clock (+0.390).
3. **The ExtraTimingOpt comparison route misses the +0.030 ns floor**, at +0.010 ns at both slow corners. The path is `sys`: the AECP response-buffer bridge's `milansoc_ws0_reg[5]`, through the CPU DMA port's write arbitration, into the NVM bridge FSM's enable. It has 17 levels, 75 % routing, and lies outside F1 to F4.

Route-1x1 at the head, recipe unchanged, the three directives in parallel through the slot wrapper. The comparison directives reuse the shipping run's synthesis checkpoint, default seed. Families come from the 5,000 worst endpoints over every path group.

| Directive | WNS / WHS ns (dev) | Worst family | F1 flash | F2 | F3 | F4 | LUT / FF / slices |
|---|---|---|---:|---:|---:|---:|---|
| ExtraPostPlacementOpt | **+0.128** / +0.030 (+0.303) | milan reset -> PS reset synchroniser | +2.386 | +1.162 | not in the 5,000 | +0.324 | 51,827 / 54,022 / 15,764 |
| AltSpreadLogic_high | **+0.039** / +0.029 (+0.230) | F4 (19 levels, 75 %) | +2.110 | +1.460 | +4.379 | +0.039 | 51,895 / 54,024 / 15,839 |
| ExtraTimingOpt | **+0.010** / +0.029 (+0.106) | `ws0` -> NVM bridge FSM (17 levels) | +2.228 | +1.380 | not in the 5,000 | +0.059 | 51,882 / 54,029 / 15,839 |

- **The cuts hold.** At dev F1 to F3 were +0.106 to +0.816 ns. Now each sits more than 1 ns from the worst path at every directive.
- **What sets the WNS now** is a different family at each directive, and this lane changes none of their logic. Each had more slack at dev. F4 (inside the CPU) moved from +0.603 / +0.353 / +0.686 ns to +0.324 / +0.039 / +0.059 ns. The reset crossing moved from +1.975 to +0.128 ns at the shipping directive. Every directive came out below dev's route: by 0.175, 0.191 and 0.096 ns.
- **The PHY-side flash stage in context.** It has 174 FFs and 61 LUTs, and occupies 44 to 51 slices. The control is the head with the stage replaced by wires (measurement only), routed at the same three directives. Against it the stage costs +24 to +47 LUTs and +173 to +179 FFs. Slices move by -35 to +19, which is placement. Access latency is +2 `sys` cycles a word in a burst and +8 a new burst. F1's slack is +2.386 / +2.110 / +2.228 ns with the stage and +0.677 / +0.614 / **+0.300** ns without it. Without the stage, F1 is the worst path at ExtraTimingOpt.
- **The control's WNS** is +0.168 / +0.342 / +0.300 ns: 0.040, 0.303 and 0.290 ns above the head's. Its shipping route also fails the gate: a 0.272 ns fall, with a milan-domain AECP path at +0.168 ns as the worst. The difference, about 0.3 ns, is the size of the route-to-route spread. With one seed per directive, it does not separate the stage's own effect from placement.

**Also run at the head:** ooc-1x1 and ooc-8x8, each with the gate `RESULT: PASS`. Every figure equals the twelfth record (24,346 / 20,404 and 34,156 / 29,782 LUT / FF).

**The capture**: the receipt's six arms and three controls, all rc 0. The worst contract-clock row is 13.85922 ms (8x8, 50 MHz, traffic on), so the **margin against 24.5 ms is 10.64 ms (43.4 %)**. That row is 0.004 ms under the committed receipt. Each boot reads the AEM image through the flash stage.

**The service-budget product-CPU runs** (plan `all`, `--populated --enforce-service`, 1x1 and 8x8): both `PASS`, with no service finding. Each covers 17 commands, two commits through LiteSPI's master behind the stage, and a wipe. The heartbeat's worst gap is 267.03 / 324.58 ms.

**Not run, by the STOP:** the re-record and its documentation; the full sweep; rtl-fast; the docs gates; the builder bank. Flash boot on hardware is outside this lane. The head's PHY stage has not been on a board; the pre-run image carried `77f979ce`.

**Decisions needed:**
1. Once F1 to F3 are cut, the WNS falls to whichever of at least six families draws the worst placement. Those are F4, the memory bridges into the CPU DMA port, the milan reset crossing, the AECP micro-CPU, LiteEth TX and the LiteDRAM bank machines. This lane changes none of them. The head's three routes give +0.128, +0.039 and +0.010 ns, and the gate binds at +0.190 ns. Under the #708 ruling, with no fall exception, the head cannot be re-recorded.
2. ExtraTimingOpt misses the +0.030 ns floor at the head.
3. If cutting continues, these are new scope. The worst path at the shipping directive is a reset synchroniser crossing, a CDC-constraint question in `KL_mmcm_drp_servo.sv` that no register boundary in the SoC wiring cuts. The memory bridges' path is SoC wiring as far as the CPU's DMA input pipe. F4 stays accepted.
