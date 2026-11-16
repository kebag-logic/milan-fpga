[A789] STOP (#923 and #924, round 2): the 1x1/1if split image misses the hold floor on all three of S9's directives, on one datapath path

**The gate.** Timing met: WNS and WHS at least +0.030 ns at every corner on the best of S9's three directives. 8x8/1if meets on all three. 1x1/1if meets setup on all three and the issue floor (WHS >= 0) everywhere, but its fast corners hold at +0.014 to +0.015 ns on every directive:

| Image | Directive | WNS / WHS, ns (worst corners) | Against +0.030 |
|---|---|---|---|
| 1x1/1if | ExtraPostPlacementOpt | +0.256 / +0.015 | hold under |
| 1x1/1if | ExtraTimingOpt | +0.126 / +0.014 | hold under |
| 1x1/1if | AltSpreadLogic_high | +0.195 / +0.014 | hold under |
| 8x8/1if | ExtraPostPlacementOpt | +0.295 / +0.036 | met |
| 8x8/1if | ExtraTimingOpt | +0.034 / +0.035 | met |
| 8x8/1if | AltSpreadLogic_high | +0.047 / +0.035 | met |
| 1x1/1if at the base `16ba667d` | ExtraPostPlacementOpt | +0.208 / +0.014 | hold under, the same path family |

**The path is not this lane's.** On every directive the one path under the floor is the same one inside `milan_datapath`: `g_tdm_render_live.g_master.chan_tdm_render/bank_r_reg[3][22]` to `u_fcdc/mem_r_reg_1/DIADI[22]`, a register into a RAMB36 data input, 0 logic levels, at both fast corners. That is the TDM render FIFO crossing that #919's ruling recorded as #927's (issuecomment-6907583837, item 1). The 1x1/1if export is the base's but for the control memory: one 2 KiB rom bank more (43.0 to 43.5 RAMB36) and the rom's contents. No RTL, constraint or generator input changed between `16ba667d` and the head. Routed at the base `16ba667d` on the recipe's directive, the 1x1/1if image misses the same way: +0.014 ns at both fast corners, on `chan_tdm_render/bank_r_reg[6][22]` to `u_fcdc/mem_r_reg_2/DIADI[22]`. So the miss is the base's.

**The question.** May this lane record its 1x1/1if routes as misses owed to #927, as #919's were, with no seeds and no further directives? Or must the 1x1/1if image meet the floor here? That needs a seed, a fourth directive or a logic cut in the datapath, and none of those is this lane's to choose. #927's acceptance names the 8x8/1if image and has 1x1/1if keep meeting, so no issue settles this one.

**Recommendation (A).** Record it as #927's: add the 1x1/1if TDM render FIFO crossing to #927's paths, and route again here only if the gateware changes.

**State of the lane at `70c100da` (local; nothing pushed):**
- #923 and #924 as round 1 left them, and the ruling's ledger: the 8x8/1if platform image at its own entry, 56.5 RAMB36, S14 debt; the 8x8/2if entries at 59.5 and 61.0. The product build plans a ledgered image at its own entry by its symbols. The 8x8/1if image routed at 56.5: 92.5 of the device's 135 Block RAM tiles, the fabric's 36. The 1x1/1if image: 82, the fabric's 38.5 (81 at the base). At the recipe's directive the 1x1/1if area moves by -74 LUT and -8 FF, and by one RAMB36: the 2 KiB rom bank the plan counts as a RAMB18 is placed as a RAMB36. The 8x8/1if base route, for its area delta, is running.
- Found and fixed this round:
  - The coverage ratchet: `aecp_maps.c` 418 of 419 branches. A test of a refused restore removal with a clipped reset set, and its plant, caught by name; the six changed files recorded at 100 %.
  - The harness at 8x8 with two interfaces: a TypeError from the product build's new `ledgered=`, and EDIT verdicts that read 0. Every edit there had answered NOT_SUPPORTED with no notice.
  - The firmware page's pin-control figure, 183 to 185, for the two twin-maps targets.
  - `rows_tiers.py` held at its module length.
- Costs, base to head, the same legs, by the rule: the one-row edit at 1x1/1if 255 to 295 us and the largest legal command 915 to 975 us, within the stated 300 and 975. At 8x8/2if 305 to 355 us and 1,325 to 1,395 us, within 595 and 1,650. The 8x8/2if one-row member is stated at 355 (325 before). No input of the tier model moves, so every row, the load, the pace and the slice stand.
- The full arm A at 1x1/1if, 93 groups, and the record classes over every held leg: RESULT PASS. Its only budget findings are the seven `backlog-owed` held-egress rows of the base, already ruled. The 8x8/1if parts report the same rows and the costs that shape takes past 1x1/1if's statements, as that point does.
- The release image is byte-identical (`bios.bin` at both configs).
- `twin-maps` at `70c100da`: its 20 checks pass, and its plant fails its three checks by name. Round 1's comment counted 21; the run has 20.
- The clean-clone workflow pass ran at `e628d35a`, before the figure fix. Every job passed but three:
  - The pin-control figure, now fixed.
  - The soc timing-cuts simulation and the publication census, killed by their 900 s wall clocks with the host at load 300 to 1,000. The timing-cuts rerun passed. The census's third run passed its 6 shapes (246 checks), but one of its 163 self-test arms was killed by the same clock, so it is unknown, not failed.
- At `70c100da` the pass is running again, on booked CPUs since the host restart, and its results go to the lane's handoff. No 4-shard sweep runs in this round: none runs beside a route or after a stop.
