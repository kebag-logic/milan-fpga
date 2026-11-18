[A794] Area debt: the release image's LUT growth at the flip train's final head (#665 issuecomment-6979461559, item 4; issuecomment-6979996755, item 5)

The resource gate's release route endpoint (`pp_resource_gate.py check --endpoint route-1x1`, the recipe's three
placement directives, ExtraTimingOpt selected) measures the flip train's final head `05dc1791` against its record:

| Figure | Record | Final head | Delta |
|---|---:|---:|---:|
| LUT | 53,461 | 54,002 | **+541** (tolerance 500) |
| FF | 54,971 | 55,203 | +232 |
| SLICE | 15,849 | 15,849 | 0 |
| RAMB36 | 74 | 71 | -3 |
| RAMB18 | 27 | 27 | 0 |
| DSP | 15 | 15 | 0 |
| WNS / WHS (ns) | 0.334 / 0.017 | 0.194 / 0.017 | #818's floor holds |

#665 accepts the growth by re-baseline: the record moves to the final head's figures by the record-only commit
`73272666`, with no RTL or firmware. This note records the growth and its attribution as area debt; it is not a floor exception.

**Attribution**, placed on the same directive (ExtraPostPlacementOpt). The train's step-10 candidate `c8ff391a`, before
#927, places 53,571 LUTs, 54,944 flops and 74 RAMB36. The final head places 53,971, 55,206 and 71, which is +510 over
the record on that directive; the gate's +541 is the selected ExtraTimingOpt route's. So:

- **the train before #927 is +110 LUTs** over the record, inside the tolerance;
- **#927 (#939, frozen `0297a19a`) brings about +400 LUTs**, +262 flops and -3 RAMB36. By hierarchy, from the two
  routed checkpoints:
  - the render crossing, `KL_tdm_render_master`'s frame FIFO `u_fcdc` (`cdc_pair_fifo`, `DIST_RAM_P = 1`): its storage
    moves from 3 RAMB36 to 128 LUTRAMs, and its read register adds +192 FF;
  - the AAF clock meter (`KL_aaf_clock_meter`): +41 LUT, -18 FF;
  - the EDIT-window claim registers: +96 FF;
  - about +230 LUT of synthesis and placement variation in modules whose RTL is unchanged.

The render crossing is shared, so the release image takes the distributed storage as the 1x1/1if split image does.

**CDC residue (#495):** the render crossing's distributed storage adds 192 CDC-15 rows (clock-enable controlled, all counted Safe), beside the 50 the TDM capture's crossing already carries. Neither is waived or repaired. The timing findings document is to list the render crossing's beside the capture crossing's,
in the same class, and whether both get a waiver that carries the argument is decided after the flip (#665 issuecomment-6981065172).
