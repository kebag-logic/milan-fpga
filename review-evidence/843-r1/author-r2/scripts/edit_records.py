"""edit_records.py <repo>: the #843 round 2 record text, after the combined route and the route-1x1 re-record.

Every replaced span must occur exactly once; the figures are the ones figures.py and the gate printed
(receipts/route-figures.json, receipts/rebaseline/). Touches documentation only."""
import sys
from pathlib import Path

root = Path(sys.argv[1])
D843 = "https://github.com/kebag-logic/milan-fpga/issues/843#issuecomment-6689115541"
D845 = "https://github.com/kebag-logic/milan-fpga/issues/845#issuecomment-6689114981"
I843 = "https://github.com/kebag-logic/milan-fpga/issues/843"
I845 = "https://github.com/kebag-logic/milan-fpga/issues/845"
I640 = "https://github.com/kebag-logic/milan-fpga/issues/640"
ANCHOR = "../findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-11-07-fpga-gptp-1616fc8f"


def edit(rel, pairs):
    path = root / rel
    text = path.read_text()
    for old, new in pairs:
        assert text.count(old) == 1, (rel, old[:80], text.count(old))
        text = text.replace(old, new)
    path.write_text(text)
    print("edited", rel)


DIRECTIVES = """| Directive | Dev WNS / WHS, worst corner | Dev LUT | Dev slice | This pin WNS / WHS, worst corner | LUT | FF | Slice | Free |
|---|---|---:|---:|---|---:|---:|---:|---:|
| AltSpreadLogic_high, selected | +0.121 / +0.025 ns | 52,968 | 15,817 | +0.242 / +0.012 ns | 53,221 | 54,754 | 15,834 | 16 |
| ExtraPostPlacementOpt | +0.122 / +0.036 ns | 52,845 | 15,841 | +0.062 / +0.024 ns | 53,166 | 54,757 | 15,846 | 4 |
| ExtraTimingOpt, dev's selection | +0.234 / +0.033 ns | 52,973 | 15,817 | +0.058 / +0.031 ns | 53,234 | 54,755 | 15,834 | 16 |
"""

BEST = """| Figure | Dev `1eb5289d`, ExtraTimingOpt | This pin, AltSpreadLogic_high | Change |
|---|---:|---:|---:|
| LUT | 52,973 | 53,221 | +248 |
| FF | 54,595 | 54,754 | +159 |
| Slice of 15,850 | 15,817 | 15,834 | +17 |
| RAMB36 / RAMB18 | 74 / 27 | 74 / 27 | 0 |
| DSP | 13 | 15 | +2 |
| WNS / WHS, slow corners | +0.234 / +0.061 ns | +0.242 / +0.071 ns | +0.008 / +0.010 ns |
| WNS / WHS, fast corners | +1.553 / +0.033 ns | +1.383 / +0.012 ns | -0.170 / -0.021 ns |
"""

# ---- docs/reference/SUBMODULES.md: the #843 adoption record's route ---------------------------------------
old_sub = """Route-1x1, shipping directive only, against dev `cc204c6f`:

| Figure | Dev `cc204c6f` | This pin | Change |
|---|---:|---:|---:|
| LUT | 51,994 | 52,695 | +701 |
| FF | 54,101 | 54,288 | +187 |
| Slice of 15,850 | 15,841 | 15,846 | +5 |
| RAMB36 / RAMB18 | 74 / 27 | 74 / 27 | 0 |
| DSP | 13 | 15 | +2 |
| WNS, slow corners | +0.236 ns | +0.018 ns | -0.218 ns |
| WHS, fast corners | +0.036 ns | +0.015 ns | -0.021 ns |

Both routes complete with no routing error.

This pin's slow corners miss the +0.03 ns floor.

Its worst path is the SoC's SDRAM controller.

The resource gate refuses the LUT, DSP and WNS rows.

The other two directives were not routed.

The decision on this route is open on #843.
"""
new_sub = f"""The shipping route is the first with both lab-fix pins.

It was measured at lane commit `a6d7cdf3`, the dev merge.

Later commits change no synthesis input.

It ran the recipe's three directives, as did dev `1eb5289d`:

{DIRECTIVES}
Each set's best directive, against dev's:

{BEST}
Every route completes with no routing error.

Every directive meets the build floor at every corner.

The worst setup path is the SoC's SDRAM controller.

On each directive the engine adds 469 to 475 LUTs.

It also adds 166 FFs and two DSPs.

Against the thirteenth record the gate refused this route.

LUTs grew by 692, over the 500 tolerance.

DSPs grew by two, over a tolerance of 0.

The [maintainer decision of 2026-11-06]({D843}) accepts that growth.

The gate's fourteenth record holds this route.

Against it, `check` and `check-baseline` exit 0.

The standalone records stay #845's.

Their top, `KL_pp_shadow`, holds no gPTP logic.
"""
edit("docs/reference/SUBMODULES.md", [(old_sub, new_sub)])

# ---- CHANGELOG.md: the #843 section's route lines ----------------------------------------------------------
old_cl = """- route-1x1 is 701 LUTs and 187 FFs over dev.
- It adds two DSPs; 4 of 15,850 slices remain.
- Its slow corners reach +0.018 ns WNS.
- That is under the +0.03 ns build floor.
- The resource gate refuses the LUT, DSP and WNS figures.
- Only the shipping directive was routed.
- The decision on the route is open on #843.
"""
new_cl = """- Its route is the first with both lab-fix pins.
- The best of three directives is AltSpreadLogic_high.
- It reaches +0.242 ns WNS, over the build floor.
- It uses 248 LUTs, 159 FFs and two DSPs more.
- That is against dev's best, ExtraTimingOpt at +0.234 ns.
- 16 of 15,850 slices remain.
- The gate refused the LUT and DSP growth.
- The 2026-11-06 maintainer decision accepts it.
- `route-1x1` is re-recorded; the standalone records stay.
"""
edit("CHANGELOG.md", [(old_cl, new_cl)])

# ---- docs/design/AREA_BUDGET.md ---------------------------------------------------------------------------
ab = [
    (f"""The [issue #234 baseline](../findings/234_PP_SHADOW_AREA_BASELINE.md) records the shipping image at [#845]({I845})'s lane commit `b16f0175` on dev `87e9d03a`, with processor `92100657` and FPGA-gPTP `135afd04`, under a [maintainer decision]({D845}).""",
     f"""The [issue #234 baseline](../findings/234_PP_SHADOW_AREA_BASELINE.md) records the shipping route at [#843]({I843})'s lane commit `a6d7cdf3`, its merge of dev `1eb5289d`, with processor `92100657` and FPGA-gPTP `1616fc8f`, and the standalone endpoints at [#845]({I845})'s lane commits `b16f0175` and `bf6c5a67`, both under a [maintainer decision]({D845})."""),
    (f"""That measurement is the gate's record; its [receipts and differences](../findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-11-06-processor-92100657) retain the preceding record.
All nine measurements use the same recipe identity and policy.
The route record's placement directive is now ExtraTimingOpt, the one flow difference the gate allows.""",
     f"""Its [receipts and differences](../findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-11-06-processor-92100657) retain the preceding record.
Issue [#843]({I843}) then re-recorded the route endpoint at lane commit `a6d7cdf3`, its merge of dev `1eb5289d`, adopting FPGA-gPTP `1616fc8f` with processor `92100657`.
Its route growth exceeded the LUT and DSP tolerances; it is recorded under the same [maintainer decision]({D843}), and Mark II ([#640]({I640})) recovers the area.
Its standalone endpoints keep #845's records: their top, `KL_pp_shadow`, holds no gPTP logic, and no source, generic or processor image of it differs from dev `1eb5289d`'s export.
That route and those standalone records are the gate's record; the route's [receipts and differences]({ANCHOR}) retain the preceding route record.
All ten measurements use the same recipe identity and policy.
The route record's placement directive is now AltSpreadLogic_high, the one flow difference the gate allows."""),
    ("""| Resource | Device | Shipping route, #845 on dev `87e9d03a`, processor `92100657`, FPGA-gPTP `135afd04`, ExtraTimingOpt | Used | Target | Status |""",
     """| Resource | Device | Shipping route, #843 on dev `1eb5289d`, processor `92100657`, FPGA-gPTP `1616fc8f`, AltSpreadLogic_high | Used | Target | Status |"""),
    ("""| Slice LUT | 63,400 | 52,529 | 82.85 % |""", """| Slice LUT | 63,400 | 53,221 | 83.94 % |"""),
    ("""| Slice register | 126,800 | 54,582 | 43.05 % |""", """| Slice register | 126,800 | 54,754 | 43.18 % |"""),
    ("""| Slice | 15,850 | 15,835 | 99.91 % | must stay below the device to place | 15 free |""",
     """| Slice | 15,850 | 15,834 | 99.90 % | must stay below the device to place | 16 free |"""),
    ("""| DSP | 240 | 13 | 5.42 % | none stated | - |""", """| DSP | 240 | 15 | 6.25 % | none stated | - |"""),
    ("""| WNS / WHS | - | +0.373 / +0.012 ns | - |""", """| WNS / WHS | - | +0.242 / +0.012 ns | - |"""),
    ("""The slice row is the binding limit: the selected route places 15,835 slices, so placement has 15 of 15,850 left.""",
     """The slice row is the binding limit: the selected route places 15,834 slices, so placement has 16 of 15,850 left."""),
    (f"""On dev `cc204c6f` (processor `a9e84b66`) the shipping route places 15,841 slices, 9 left, at +0.236 / +0.036 ns.
At FPGA-gPTP `1616fc8f` ([#843]({I843})) it places 15,846, 4 left, with 701 LUTs, 187 FFs and two DSPs more.
Its slow corners reach +0.018 ns, under the +0.03 ns build floor, on the shipping directive, the only one routed; its worst path is the SoC's SDRAM controller.
The gate refuses that route on its LUT (+683 over the record, tolerance 500), DSP (+2, tolerance 0) and WNS floor rows; the decision is open on #843.
""", ""),
    ("""The table above holds the re-recorded route, and `check` exits 0 on all three endpoints against the new record.""",
     """Its re-recorded route was the thirteenth record, and `check` exited 0 on all three endpoints against it."""),
    (f"""Mark II ([#640]({I640})) recovers the area.
The routed critical setup path has 15 logic levels on the SoC's 10 ns clock, outside the wrapper and the datapath.
It runs from the SDRAM bank machine's `milansoc_sdram_bankmachine0_pipe_valid_source_payload_addr_reg[7]` to the write-to-read timer `milansoc_sdram_twtrcon_ready_reg`; its data delay is 9.170 ns, of which 6.070 ns is routing.
The preceding [#799]""",
     f"""Mark II ([#640]({I640})) recovers the area.
The adoption of FPGA-gPTP `1616fc8f` ([#843]({I843})) is the other lab-fix pin that decision covers.
Its route, at lane commit `a6d7cdf3`, its merge of dev `1eb5289d`, is the first with both pins.
Against the thirteenth record the gate refused it: `pp_resource_gate.py check` exited 1 on `route-1x1`.
On `route-1x1` the gate selects AltSpreadLogic_high, the best of the three directives at WNS +0.242 ns.
It refused 53,221 LUTs (+692, tolerance +500) and 15 DSPs (+2, tolerance 0).
That route's 54,754 FFs (+172, tolerance +600), 15,834 slices (-1, tolerance +80), block RAM, WNS and WHS passed; 16 slices are left.
The table above holds that route, re-recorded with `record --write`, and `check` exits 0 against it.
The standalone endpoints keep #845's records, since `KL_pp_shadow` holds no gPTP logic.
Dev `1eb5289d` routed with the same recipe; its best directive, ExtraTimingOpt, passes the thirteenth record.
All six routes complete without error and meet the build floor at every corner:

{DIRECTIVES}
Best against best, the adoption adds 248 LUTs, 159 FFs, 17 slices and two DSPs, and WNS rises by 0.008 ns.
On each directive the gPTP engine `u_engine` grows by 469 to 475 LUTs, 166 FFs and two DSPs, FPGA-gPTP #100's Follow_Up information TLV logic; the rest of the image moves by packing.
The routed critical setup path has 16 logic levels on the SoC's 10 ns clock, outside the wrapper and the datapath.
It runs from the SDRAM bank machine's `milansoc_sdram_bankmachine6_row_reg[5]` to the write-to-read timer `milansoc_sdram_twtrcon_ready_reg`; its data delay is 9.301 ns, of which 6.248 ns is routing.
The preceding [#845]({I845}) image, at `b16f0175`, used 52,529 LUTs and 15,835 slices, 15 free, at +0.373 / +0.012 ns; its critical path had 15 logic levels from the SDRAM bank machine to its write-to-read timer.
The [#799]"""),
    ("""The [#799](https://github.com/kebag-logic/milan-fpga/issues/799) image, at `8b76de69`,""",
     """The [#799](https://github.com/kebag-logic/milan-fpga/issues/799) image before it, at `8b76de69`,"""),
    ("""The [#632](https://github.com/kebag-logic/milan-fpga/issues/632) image before it, at `5282b8b6`,""",
     """The [#632](https://github.com/kebag-logic/milan-fpga/issues/632) image before that, at `5282b8b6`,"""),
    ("""The [#771](https://github.com/kebag-logic/milan-fpga/issues/771) image before that, at `8de4b80b`,""",
     """The [#771](https://github.com/kebag-logic/milan-fpga/issues/771) image before that one, at `8de4b80b`,"""),
    ("""Read as `milan_datapath`, that stack names 43,906 LUTs in the routed image, 69.3 % of the device.
The wrapper names 24,895 of them in that rebuilt hierarchy.""",
     """Read as `milan_datapath`, that stack names 44,631 LUTs in the routed image, 70.4 % of the device.
The wrapper names 24,937 of them in that rebuilt hierarchy."""),
    (f"""[#799](https://github.com/kebag-logic/milan-fpga/issues/799)'s 52,012-LUT route replaced the #632 one, and [#845]({I845})'s 52,529-LUT route has since replaced the #799 one.""",
     f"""[#799](https://github.com/kebag-logic/milan-fpga/issues/799)'s 52,012-LUT route replaced the #632 one, [#845]({I845})'s 52,529-LUT route replaced the #799 one, and [#843]({I843})'s 53,221-LUT route has since replaced the #845 one."""),
    ("""The record now names ExtraTimingOpt, the directive the gate selected; every policy value stays unchanged.""",
     f"""The record now names ExtraTimingOpt, the directive the gate selected; every policy value stays unchanged.
The [fourteenth]({ANCHOR}) re-records the route alone for [#843]({I843})'s adoption of FPGA-gPTP `1616fc8f` on dev `1eb5289d`, with processor `92100657`; the standalone records stay the thirteenth's.
The route is measured at lane commit `a6d7cdf3`, the merge of dev `1eb5289d`.
Dev merged PRs #841 and #842 after the thirteenth without a new record, so its differences are theirs and this adoption's together.
Against the thirteenth, the route moved by +692 LUTs, +172 FFs, -1 slice and +2 DSPs, with RAM unchanged, WNS -0.131 ns and WHS 0.000 ns.
The gate refused the LUT and DSP growth; the same [maintainer decision]({D843}) accepts it, and Mark II ([#640]({I640})) recovers it.
The record now names AltSpreadLogic_high, the directive the gate selected; every policy value stays unchanged."""),
]
edit("docs/design/AREA_BUDGET.md", ab)

# ---- docs/design/MARK_II_AREA_PLAN.md ----------------------------------------------------------------------
edit("docs/design/MARK_II_AREA_PLAN.md", [
    ("""a fall of more than 0.25 ns from the +0.373 ns record is a warning""",
     """a fall of more than 0.25 ns from the +0.242 ns record is a warning"""),
    (f"""[#845]({I845}) has since re-recorded it at processor `92100657`, under a [maintainer decision]({D845}), now at 52,529 LUTs, 15,835 slices and 74/27; that record is the comparison anchor, and the ledger keeps the baseline figures.""",
     f"""[#845]({I845}) then re-recorded it at processor `92100657`, under a [maintainer decision]({D845}), to 52,529 LUTs, 15,835 slices and 74/27.
[#843]({I843}) has since re-recorded it at FPGA-gPTP `1616fc8f`, under the same decision, now at 53,221 LUTs, 15,834 slices and 74/27; that record is the comparison anchor, and the ledger keeps the baseline figures."""),
])

# ---- docs/findings/README.md -------------------------------------------------------------------------------
edit("docs/findings/README.md", [
    ("""The gate's current record is #845's re-baseline of 2026-11-06, in the [area budget](../design/AREA_BUDGET.md#headroom-target)""",
     """The gate's current route record is #843's re-baseline of 2026-11-07, and its standalone records are #845's of 2026-11-06, in the [area budget](../design/AREA_BUDGET.md#headroom-target)"""),
])

# ---- docs/findings/234_PP_SHADOW_AREA_BASELINE.md ----------------------------------------------------------
SECTION = f"""## Re-baseline of 2026-11-07, FPGA-gPTP 1616fc8f

This re-baseline records [#843]({I843})'s adoption of FPGA-gPTP `1616fc8f062fbf58c35ad31674b5b233207bbdb8` (FPGA-gPTP PRs #99 and #101, for its #98 and #100), with clockAccuracy per board.
`route-1x1` measures lane commit `a6d7cdf3e29fd07f98e3fcd0b4d1402302f65a3e`, the lane's merge of dev `1eb5289db8fc9d139ce90cad2e380b4515793806`, with processor `92100657`.
It is the first route with both lab-fix pins; the lane's later commits change no synthesis input.
Dev merged PRs #841 and #842 after the [preceding record](#re-baseline-of-2026-11-06-processor-92100657) without a new one, so the differences below are theirs and this adoption's together.
Only the route is re-recorded: the standalone endpoints synthesise `KL_pp_shadow`, which holds no gPTP logic, and no source, generic or processor image of it differs from dev `1eb5289d`'s export, so `ooc-1x1` and `ooc-8x8` keep the preceding record's figures.

**Maintainer decision.** Against the preceding record the gate refused the route with exit 1.
It grew by 692 LUTs against 500 and by two DSPs against 0.
The [maintainer decision of 2026-11-06]({D843}) accepts the area growth of the mandatory lab fixes on the shipping image, with a re-baselined budget; it is the decision #845's record cites ({D845}), and it names this gPTP pin.
This record is written under that decision; Mark II ([#640]({I640})) recovers the area.
Every tolerance, floor and ceiling stays unchanged, and every other gated figure passed.

The route was measured through the [recipe](../testing/PP_SHADOW_BASELINE_RECIPE.md) with `--single-thread-synthesis`, with `general.maxThreads` 32 and `synth.maxThreads` 1.
It is judged on its [route set](../testing/PP_SHADOW_BASELINE_RECIPE.md#resource-gate): the shipping route and its two comparison directives, placed from one synthesis checkpoint at the default seed.
The gate selected AltSpreadLogic_high, so the record's flow names that directive where the preceding record's named ExtraTimingOpt.
The resource gate reports matching measurement identities against the preceding record.
Dev `1eb5289d` was routed the same way, one run at a time, for the comparison; against the preceding record its best directive, ExtraTimingOpt, passes the gate with exit 0.

| Endpoint | LUT | FF | Slice | RAMB36 / RAMB18 | DSP | CARRY4 | WNS ns | WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `route-1x1` | 53,221 | 54,754 | 15,834 | 74 / 27 | 15 | 3,726 | +0.242 | +0.012 |

{DIRECTIVES}
| Difference from the preceding record | LUT | FF | Slice | RAMB36 / RAMB18 | DSP | WNS ns | WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| `route-1x1` | **+692** | +172 | -1 | 0 / 0 | **+2** | -0.131 | 0.000 |
| Tolerance | 500 | 600 | 80 | 0 / 0 | 0 | 0.25 | 0.25 |

Best against best, against dev `1eb5289d`:

{BEST}
On the same directive the routed hierarchy names the gPTP engine as the growth:

| Directive | `u_engine` LUT, dev to this pin | FF | DSP | `alinx_ax7101` LUT | FF |
|---|---:|---:|---:|---:|---:|
| ExtraPostPlacementOpt | 4,235 to 4,710, +475 | +166 | +2 | +321 | +161 |
| AltSpreadLogic_high | 4,236 to 4,705, +469 | +166 | +2 | +253 | +158 |
| ExtraTimingOpt | 4,236 to 4,705, +469 | +166 | +2 | +261 | +160 |

On AltSpreadLogic_high its `u_ucpu` holds +256 of those LUTs, `u_timer` +110 and `u_parser` +57; the two DSPs are the information TLV's frequency multiply.
FPGA-gPTP #100's out-of-context figures predicted +475 LUTs and two DSPs.
In the routed hierarchy of the selected route `milan_datapath` holds 44,631 LUTs and the wrapper 24,937.
Against the preceding record the gate's sub-block rows, which it does not judge, move the wrapper by +42 LUTs and -4 FFs; no wrapper source changed.

The selected route uses 87.5 RAM tiles and leaves 16 slices free.
Each route's status report has no unrouted net or routing error, and the IOB packing check passes.
WNS fell by 0.131 ns and is 0.212 ns above its +0.030 ns floor; WHS is 0.012 ns above zero.

| Route corner | WNS ns | WHS ns |
|---|---:|---:|
| `Slow_0C` | +0.242 | +0.071 |
| `Slow_85C` | +0.242 | +0.071 |
| `Fast_0C` | +1.383 | +0.012 |
| `Fast_85C` | +1.383 | +0.012 |

The worst setup path has 16 logic levels on the SoC's 10 ns clock, outside the wrapper and the datapath.
It runs from the SDRAM bank machine's `milansoc_sdram_bankmachine6_row_reg[5]` to the write-to-read timer `milansoc_sdram_twtrcon_ready_reg`.
Its data delay is 9.301 ns: 3.053 ns of logic and 6.248 ns of routing.
The worst hold path runs from the SoC's `milansoc_rdat1_reg[2]` to the block RAM `storage_43_reg`, at +0.012 ns at the fast corners.

The endpoint was written with `record --write` after its `check`, which returned 1.
`check-baseline` passes, and `check` returns 0 against the new record.
The endpoint note identifies the measured lane commit and cites the maintainer decision.

| Endpoint | Input SHA-256 |
|---|---|
| `route-1x1` | `3eb58b65ce9c76d6a47a412dfb5d626298cdf847e9caa57e9ceaffb0efd99df4` |

All 6 recorded memory-image entries were rehashed after measurement and match.
No completed measurement log contains a `Synth 8-4445` diagnostic; the one match is the script's own `set_msg_config` line.
The synthesis log's one `Synth 8-6901` is the parent's `crft_emit_en_w`.
Runs went one at a time.

| Run | rc | Minutes | Log SHA-256 | Log bytes |
|---|---|---:|---|---:|
| `route-1x1`, ExtraPostPlacementOpt, with synthesis | 0 | 49.1 | `06f2cfbf372cbf12896b455c74285fff9377390b4963204b3161b76c681bac81` | 1,043,761 |
| `route-1x1`, AltSpreadLogic_high | 0 | 18.2 | `3279e647fd85d2987991f7b3eb0bea1bb5f8f715da21fefc09860651f6175d00` | 350,937 |
| `route-1x1`, ExtraTimingOpt | 0 | 15.1 | `0026d6e546ea12a1c0cb674ac756f0313b3c03e8e4b1358bcd3f443c6b31523d` | 339,214 |

"""
f = "docs/findings/234_PP_SHADOW_AREA_BASELINE.md"
edit(f, [
    ("""The [current record](#re-baseline-of-2026-11-06-processor-92100657) adopts processor `92100657` for #845 on dev `87e9d03a`, under a maintainer decision.""",
     """Its [next record](#re-baseline-of-2026-11-06-processor-92100657) adopted processor `92100657` for #845 on dev `87e9d03a`, under a maintainer decision.
The [current route record](#re-baseline-of-2026-11-07-fpga-gptp-1616fc8f) adopts FPGA-gPTP `1616fc8f` for #843 on its merge of dev `1eb5289d`, under the same decision; the standalone records stay #845's."""),
    ("""Dev then moved the gPTP pin to `135afd04` and the processor pin to `a9e84b66`, and the current record moves the processor pin to `92100657`.""",
     """Dev then moved the gPTP pin to `135afd04` and the processor pin to `a9e84b66`, #845's record moved the processor pin to `92100657`, and the current route record moves the gPTP pin to `1616fc8f`."""),
    ("""- **[Re-baseline of 2026-11-06, processor 92100657](#re-baseline-of-2026-11-06-processor-92100657)** -- The current record, under a maintainer decision:""",
     """- **[Re-baseline of 2026-11-07, FPGA-gPTP 1616fc8f](#re-baseline-of-2026-11-07-fpga-gptp-1616fc8f)** -- The current route record, under the same maintainer decision: FPGA-gPTP `1616fc8f` with processor `92100657` on the merge of dev `1eb5289d`, the route alone on the recipe's three directives with AltSpreadLogic_high selected, against dev's own route, the engine's share, route-corner timing and input receipts.
- **[Re-baseline of 2026-11-06, processor 92100657](#re-baseline-of-2026-11-06-processor-92100657)** -- The preceding route record and the current standalone records, under a maintainer decision:"""),
    ("""## Re-baseline of 2026-11-06, processor 92100657
""", SECTION + """## Re-baseline of 2026-11-06, processor 92100657
"""),
])
