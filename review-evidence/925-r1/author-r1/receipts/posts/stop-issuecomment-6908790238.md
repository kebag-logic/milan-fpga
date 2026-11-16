[A790] STOP: both split images miss the +0.030 ns floor on all three directives, by 6 to 22 ps; the base's 1x1/1if image misses it too

**What stopped.** I ran S9's recipe for the image built at `a9f0dbc0`: the builder's split placement, the export, the
integrated route and its signoff corners, then the other two directives from that route's synthesis checkpoint, one
Vivado at a time. On no directive are WNS and WHS >= +0.030 ns at every corner. Every route closed with 0 failing
endpoints and 0 routing errors; only the margin floor is missed.

| 1x1/1if | Slow WNS / WHS | Fast WNS / WHS | Short of the floor |
|---|---|---|---|
| ExtraPostPlacementOpt (recipe) | +0.024 / +0.092 | +1.660 / +0.036 | setup, 6 ps |
| ExtraTimingOpt | +0.008 / +0.050 | +1.641 / +0.023 | setup 22 ps, hold 7 ps |
| AltSpreadLogic_high | +0.177 / +0.050 | +1.641 / +0.023 | hold, 7 ps |

| 8x8/1if | Slow WNS / WHS | Fast WNS / WHS | Short of the floor |
|---|---|---|---|
| ExtraPostPlacementOpt (recipe) | +0.011 / +0.070 | +1.370 / +0.034 | setup, 19 ps |
| ExtraTimingOpt | +0.171 / +0.102 | +1.636 / +0.014 | hold, 16 ps |
| AltSpreadLogic_high | +0.215 / +0.102 | +1.636 / +0.014 | hold, 16 ps |

**The base misses too.** I routed the base's own 1x1/1if image (`16ba667d`, #901's review head, without this change)
through the same recipe. Its AltSpreadLogic_high run is queued for CPUs; its result goes to the lane's handoff.

| 1x1/1if at `16ba667d` | Slow WNS / WHS | Fast WNS / WHS | Short of the floor |
|---|---|---|---|
| ExtraPostPlacementOpt (recipe) | +0.208 / +0.051 | +1.636 / +0.014 | hold, 16 ps |
| ExtraTimingOpt | +0.260 / +0.053 | +1.636 / +0.014 | hold, 16 ps |

**Where the margin goes.** None of the worst paths is reached by this change:
- Setup: the mailbox register read path (`KL_mbx/rd_off_r` to `reg_rdata_r`, S9's known path) at 1x1, and the
  datapath's audio-map edit path (`KL_mbx_cdc/u_edit/rq_r` to `amap_edit_oclaim_expect_r`) at 8x8.
- Hold: the TDM render FIFO's clock-crossing BRAM write port (`chan_tdm_render/u_fcdc/mem_r`) at 1x1, the FIFO
  the base misses on too, and the AAF clock meter (`aaf_clock_meter/s2_ts_r` to `grp_ts0_r`) at 8x8.

The change is firmware only. The exported gateware equals the base's at both shapes, apart from LiteX's comment tree:
the same netlist, the same route script. Only the ROM's contents differ: 88 B more firmware at 1x1, so `rom_bank3`
holds 722 words where it held 700, in the same bank; 32 B more at 8x8, in its one bank. Vivado optimises through ROM
contents, so a different image places differently.

**Everything else is green.** Heads: `a9f0dbc0` (the image), and `1be0a6c4` (a test file's line wrap and
`srp_mbx.c`'s coverage counts, no image input).
- Firmware self-test: suites PASS; control 716 of 716, AECP 299, SRP 441 caught (the 10 new plants at both interface
  counts), 0 escaped. The SRP shard again at `1be0a6c4`: 441 caught, 0 escaped.
- `fw_coverage --check` PASS: `srp_mbx.c` at 741/741 lines and 671/671 branches after its standing exclusions.
- Workflow replays, step by step on fresh clones: every job of rtl-fast, elaborate and docs failed 0. The three
  mutant jobs ran as their campaign commands above. `docs` and `firmware-unit` ran again at `1be0a6c4`, which wraps
  the 121-column line the Python idiom gate found at `a9f0dbc0`.
- `plat_ledger.py` PASS at every point, with the 8x8/2if `ctrl_plat` record raised to 20,416 B (same 60.5 RAMB36).
  ROM is +88 B at 1x1 and +32 B at 8x8; 8x8/1if still plans 56.0.
- The release image is byte-identical: `bios.bin` and the stripped ELF at both configs.
- Split boots PASS at 1x1 and 8x8.
- Service budget at 1x1/1if, rc 0: 96 groups, 0 refusals, 0 of 129,813 passes over the share. The flip check at
  1x1/1if passes with every row within its bound; the load gate passes (0.517 / 0.514).
- Service budget at 8x8/1if: 95 groups, 0 refusals, 0 of 266,195 passes over the share. It exits 1 on STATED lines
  for the polls' base, ACMP's item and ACMP's declined offer over the one-interface statements, which that point
  holds to 1x1/1if's: the shape's known excess, the same classes as #894's 8x8/1if gate (#894 issuecomment-6867393730, item (b)). None of these is SRP's.
- Both points record the same 7 probe misses, all in `backlog-owed` (ACMP and AECP records behind seven owed frames).
  #919's branch records the same 7 on this harness at 1x1/1if.
- No stated cost changes: the SRP items measure within their statements at both points, and at 1x1/1if they measure
  2,733 cycles (walk) and 25,078 (an SRP record), rule figures 30 and 265 µs, statements 35 and 280.

**Decision needed.** The base's own image misses the floor too, by 16 ps on hold. Do you accept one of these routes for the
images (1x1/1if's AltSpreadLogic_high: WNS +0.177, WHS +0.023; 8x8/1if's: WNS +0.215, WHS +0.014)? Or should the
routes use directives or seeds outside S9's three, or something else? The fix itself is done: in `95426618`, the
latest registered of Talker Advertise and Talker Failed decides the Listener declaration (IEEE 802.1Q-2018 35.2.4,
35.2.6), with its tests. Nothing is pushed.
