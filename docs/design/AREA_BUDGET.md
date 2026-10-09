# Area budget

The AX7101 release fit is decided by the placed Vivado utilization report and
post-route timing, never by an elaboration estimate. Yosys out-of-context
figures are useful for comparing isolated fabric blocks; the builder's model is
useful for refusing obviously oversized configurations. Neither is a placement
result.

The [protocol processor baseline](../findings/PP_SHADOW_BASELINE.md) records issue [#231](https://github.com/kebag-logic/milan-fpga/issues/231).
It also records issue [#587](https://github.com/kebag-logic/milan-fpga/issues/587)'s 50 MHz 8x8 rerun.
It separates standalone synthesis from integrated implementation.
Its [recipe](../testing/PP_SHADOW_BASELINE_RECIPE.md) binds both product geometries.
The [issue #234 baseline](../findings/234_PP_SHADOW_AREA_BASELINE.md) records the shipping image after merging dev `6aa25dec` for [#645](https://github.com/kebag-logic/milan-fpga/issues/645) and [#647](https://github.com/kebag-logic/milan-fpga/issues/647), retaining processor `2ad2f845`.
Its figures back the protocol processor budget and resource gate below.

The current command and media-clock claims are checked against the
[Milan feature status ledger](../reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `aem.served-command-set` | `implemented` | - |
| `crf.media-clock-consumption` | `implemented` | - |
<!-- milan-feature-status:end -->

## Contents

- **[Rules for optional blocks](#rules-for-optional-blocks)** -- The default-present, elaboration-time, safe-tie, and evidence rules every prune must follow.
- **[Tier 1 - implemented optional fabric blocks](#tier-1---implemented-optional-fabric-blocks)** -- The RTL parameter, SoC flag, configuration key, and permitted absence condition for each implemented prune.
- **[Isolated synthesis estimates](#isolated-synthesis-estimates)** -- Comparable Yosys resource estimates for the optional fabric blocks at the measured shape.
- **[Release accounting](#release-accounting)** -- The placed utilization, timing, identity, and repeated evidence required for a release candidate.
- **[Protocol processor budget and resource gate](#protocol-processor-budget-and-resource-gate)** -- The recorded baseline, Mark II estimates, unchanged policy and D7 re-record rule.

## Rules for optional blocks

1. Every optional block defaults to present.
2. Pruning is an elaboration-time decision, not a runtime disable bit.
3. The absent arm ties every exposed result to an inert value.
4. A prune names the physical/compliance evidence that must be repeated.
5. The builder refuses a configuration whose declared function needs a pruned
   block.

## Tier 1 - implemented optional fabric blocks

| block | `milan_datapath` | SoC flag | `board.features` | absent only when |
|---|---|---|---|---|
| media-clock servo | `MCSERVO_P` | `--no-media-clock-servo` | `media_clock_servo` | every media clock is internal |
| latency taps | `LTAP_P` | `--no-latency-taps` | `latency_taps` | stage instrumentation is not required |
| MAAP engine | `MAAP_P` | `--no-maap` | `maap` | never in supported configurations; every declared talker requires MAAP |
| I2S playback | `I2SPB_P` | `--no-i2s-playback` | `i2s_playback` | the board has no I2S DAC |
| RX address filter | `RXFILT_P` | `--no-rx-mac-filter` | `rx_mac_filter` | the fabric integration intentionally accepts the unfiltered control/media observation |
| PCM low-pass | `LPF_P` | `--no-render-lpf` | `render_lpf` | the physical render chain does not require the filter |
| datapath probe groups | `DPROBES_P` | `--no-datapath-probes` | `datapath_probes` | release diagnostics may be omitted and the reserved CSR range may read zero |

The builder tests require this table to agree with its option map and with the
real RTL generate arms.

## Isolated synthesis estimates

Measured with [`syn/yosys/ooc.sh`](../../syn/yosys/ooc.sh) at the 8-stream, 16-slot fabric shape. These
are comparison numbers, not guaranteed savings after placement.

> **Entity-shape provenance.** The stream and slot parameters above do not
> identify the generated entity shape bound through
> `` `include "gen/adp_shape_defaults.svh" ``. At the time of this measurement,
> [`ooc.sh`](../../syn/yosys/ooc.sh) named no `configs/generated/**` include directory, so the record
> does not establish which generated shape supplied the ACMP context counts.
> Treat these figures as **parameter-pinned and entity-shape-unknown** until
> they are repeated with a named configuration.

| block | LUT | FF | DSP | BRAM36 |
|---|---:|---:|---:|---:|
| media-clock servo | 814 | 789 | 1 | 0 |
| latency taps | 948 | 614 | 0 | 0 |
| MAAP engine | 634 | 269 | 0 | 0 |
| I2S playback | 454 | 631 | 0 | 1 |
| RX address filter | 801 | 1,691 | 0 | 0 |
| PCM low-pass | 864 | 756 | 1 | 0 |
| **total** | **4,515** | **4,750** | **2** | **1** |

The datapath-probe row was added after this measurement and is intentionally
not folded into the total.

## Release accounting

For every candidate, retain:

- the exact configuration and generated source manifest;
- placed Slice LUT, Slice, flip-flop, BRAM, and DSP rows;
- post-route WNS/TNS and the selected placement directive;
- a hierarchical comparison against the immediately preceding candidate;
- the optional-block presence table emitted by the builder.

A block removed for area changes the candidate's capabilities and may
invalidate media, timing, observability, or compliance evidence. Repeat the
named campaign before quoting the resulting image as release-ready.

## Protocol processor budget and resource gate

Issue [#234](https://github.com/kebag-logic/milan-fpga/issues/234) first measured the shipping 1x1 image at dev `1269cdaf`, processor pin `631eeb34`.
Later records cover PR [#634](https://github.com/kebag-logic/milan-fpga/issues/634) and [#661](https://github.com/kebag-logic/milan-fpga/issues/661)'s adoption of processor `ead80360`.
[Combination F](../findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-10-07-processor-2ad2f845) was measured for [#682](https://github.com/kebag-logic/milan-fpga/issues/682) at parent `4d253880` after merging dev `79b086d4`, processor `2ad2f845`.
It explicitly limits synthesis to one worker; the flow identity records this memory setting.
The [issue #234 baseline](../findings/234_PP_SHADOW_AREA_BASELINE.md) holds those measurements, differences and receipts.
Issue [#686](https://github.com/kebag-logic/milan-fpga/issues/686) re-recorded all three endpoints on 2026-10-08 at `e519e31f`, its merge of dev `291710b1`, after `KL_maap`'s Annex B change.
Issue [#645](https://github.com/kebag-logic/milan-fpga/issues/645) then re-recorded all three endpoints on merge result `a5ca6e51`, including dev `6aa25dec`, the GMII capture change and the listener settle recentre.
That merge-result measurement is the gate's record; its [receipts and differences](../findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-10-08-issues-645-and-647) retain the preceding [#686](https://github.com/kebag-logic/milan-fpga/issues/686) record.
Both measurements use the same recipe identity and policy.
The [#686](https://github.com/kebag-logic/milan-fpga/issues/686) flow identity matches F, the one synthesis worker included.
The [#686](https://github.com/kebag-logic/milan-fpga/issues/686) repository inputs differ from F's only in [`KL_maap.sv`](../../hdl/ieee1722/maap/KL_maap.sv) and comment lines of [`milan_datapath.sv`](../../hdl/milan/milan_datapath.sv); the processor pins are F's.

### Headroom target

[NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest) in the [requirements](../reference/FR_NFR.md) is the accepted headroom target.
The baseline product must fit `xc7a100t` with at most 60 percent of its LUTs used.
The adopted image does not meet it:

| Resource | Device | Shipping route, processor `2ad2f845` | Used | Target | Status |
|---|---:|---:|---:|---|---|
| Slice LUT | 63,400 | 50,267 | 79.29 % | [NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest): at most 38,040 (60 %) | not met, 12,227 over |
| Slice register | 126,800 | 54,413 | 42.91 % | none stated | - |
| Slice | 15,850 | 15,779 | 99.55 % | must stay below the device to place | 71 free |
| Block RAM tile | 135 | 87.5 | 64.81 % | reserve: 13.5 tiles (10 %), the 121.5-tile ceiling, accepted (manager ruling) | 47.5 free |
| DSP | 240 | 14 | 5.83 % | none stated | - |
| WNS / WHS | - | +0.299 / +0.031 ns | - | [build gate](../integration/BUILDING.md#5-gates-before-a-build-is-good): at least +0.03 / 0 ns | met |

The table is the gate's record.
The slice row is the binding limit: placement has 71 slices left.
The routed critical setup path has 14 logic levels, from `milansoc_write_w_buffer_level0_reg[1]` to `storage_13_dat1_reg[14]`.
Its data delay is 9.294 ns, of which 7.331 ns is routing.
The preceding [#686](https://github.com/kebag-logic/milan-fpga/issues/686) image used 50,391 LUTs and 15,788 slices, 62 free, at +0.241 / +0.029 ns.
The earlier F image used 49,957 LUTs and 15,734 slices, 116 free, at +0.124 / +0.031 ns; its critical path had 18 logic levels from the AXI-Lite-to-Wishbone bridge state to the SPI-flash PHY counter.
The E image before F used 49,888 LUTs and 15,805 slices, 45 free, at +0.101 / +0.031 ns.
The baseline records F's endpoint and sub-block differences from E.

### Allocation to the protocol processor

The standalone wrapper uses 23,179 LUTs, 36.6 % of the device, at the shipping clock.
The superseded [#229](https://github.com/kebag-logic/milan-fpga/issues/229) milestone targeted a non-CPU stack below 30 %, 19,020 LUTs.
Read as `milan_datapath`, that stack names 41,689 LUTs in the routed image, 65.8 % of the device.
The wrapper names 23,345 of them in that rebuilt hierarchy.
The wrapper alone exceeds that historical allocation.
The active [#640](https://github.com/kebag-logic/milan-fpga/issues/640) acceptance bar is the whole-image [NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest) target.

Meeting [NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest) with the rest of the image unchanged needs the wrapper at most 11,118 LUTs.
That requires removing 12,227 LUTs, 52 % of the wrapper.
The [owner decided on 2026-10-03](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5967924270) that [NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest) stays at 60 %.
It is met by the [Mark II redesign plan](MARK_II_AREA_PLAN.md) ([#640](https://github.com/kebag-logic/milan-fpga/issues/640)).
The [2026-10-05 schedule correction](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5988555968)
places milestone 12 before P3, with delivery planned by 2026-12-15.
The former Instrument-verification prerequisite no longer applies.
The [#396](https://github.com/kebag-logic/milan-fpga/issues/396) release campaigns run on the qualified redesigned image.
Until M9, comparisons retain the last recorded baseline and unchanged policy.
The [#232](https://github.com/kebag-logic/milan-fpga/issues/232), [#230](https://github.com/kebag-logic/milan-fpga/issues/230) and [#639](https://github.com/kebag-logic/milan-fpga/issues/639) storage changes are now adopted and measured; the remaining redesign stays under [#640](https://github.com/kebag-logic/milan-fpga/issues/640).

### Mark II planning ledger

Round 1d uses the three records committed on dev `5603c353`.
Their measurement inputs are `a5ca6e51`, as the endpoint notes state.
No new implementation run is claimed by this documentation update.

| Recorded endpoint | LUT | FF | RAMB36 / RAMB18 | DSP | Timing interpretation |
|---|---:|---:|---:|---:|---|
| `route-1x1` | 50,267 | 54,413 | 74 / 27 | 14 | +0.299 / +0.031 ns, routed setup/hold |
| `ooc-1x1` | 23,179 | 19,779 | 16 / 3 | 8 | Synthesis only, no integrated-fit claim |
| `ooc-8x8` | 30,135 | 27,380 | 21 / 5 | 8 | Synthesis only, no integrated-fit claim |

The [owner's decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5993114362) assigns the bare-metal split to milestone 12.
Integration precedes P3.
ADP, ACMP, MAAP, SRP, AECP and saved-state handling move.
All-fabric remains supported and remains the current shipping default.
The flip requires F2-F5 suites and bench acceptance.
[#664](https://github.com/kebag-logic/milan-fpga/issues/664) governs that qualification.
Unqualified functions retain fabric placement.
The hard-core port remains milestone 13.
Diagnostics stay in the shipping image under D2.
The optional-block table above grants no Mark II diagnostic-pruning credit.
MAAP remains required in either placement.
Relocation does not disable it.

The [plan ledger](MARK_II_AREA_PLAN.md#ledger) gives each saving's basis.
These figures are estimates of the complete qualified default image:

| Lane | Estimated saving, central | Image after, central | Dependency |
|---|---:|---:|---|
| F0-F5 split | 14,000 | 36,267 | Approved [#664](https://github.com/kebag-logic/milan-fpga/issues/664); both M0s measurements and memory-ledger reconciliation before flip; function, service and bench qualification |
| M2 retained SoC tables | 200 | 36,067 | Adopted pin; [L3](MARK_II_AREA_PLAN.md#l3-ram-friendly-retained-tables) names surviving MAC/CSR FIFOs; excludes DDR3 and M6/M7 tables |
| M5 CSR read path | 600 | 35,467 | Stable existing ABI and both placement faces |
| M6 media contexts | 600 | 34,867 | Fabric-owned counters, channel map and render state |
| M7 gPTP tables | 500 | 34,367 | Fabric gPTP deadlines preserved |
| M8a on-chip main memory | 1,000 | 33,367 | D4 approved; shape-sized [#70](https://github.com/kebag-logic/milan-fpga/issues/70)/F1 staging; packing/replacement estimate below |
| M8b smaller cacheless RV32I | 1,700 | 31,667 | D5 conditional: capture <= 24.5 ms at 8x8, boot and split load |
| M3 residual fabric AECP | 0 | 31,667 | 2,600 estimated only where fabric AECP remains |
| M10 shared gPTP/AECP engine | 0 | 31,667 | 1,200 estimated only with a separate retained AECP engine |
| M9 closure and re-record | No assumed saving | Measured at closure | <= 38,040 LUT and timing met |

The split estimate includes the measured 3,102-LUT mailbox skeleton.
It also reserves 1,000 LUTs for remaining fabric integration.
Its 11,500-16,000 range includes mapping and integration uncertainty.
M3/M10 cannot save an engine already removed by F5.
M1 is dropped; F4 replaces M4.
The retained-fabric opportunities are not added to the default ledger.

M8a is repriced to 1,000 LUTs, range 400-1,500.
The [census](../findings/649_RESOURCE_MAP_AND_SENSITIVITY.md#the-soc-tops-own-logic) counts 823 controller and 873 PHY LUT cells.
These are pre-packing cells, not packed LUT sites.
Its 3,231 anonymous LUT cells have no assigned owner.
No saving is credited to that unowned remainder.
[L11](MARK_II_AREA_PLAN.md#l11-the-soc-side) applies 50/75/100 percent packing assumptions.
It debits 400/250/100 LUTs respectively for replacement logic.
Round down to each [L11 case](MARK_II_AREA_PLAN.md#l11-the-soc-side).
They remain estimates requiring M8a's routed and memory-capacity checks.

The combined estimate spans 27,567-35,867 LUTs.
Its central estimate is 31,667.
Without the smaller core, the conservative estimate is 37,167.
These estimates prove neither routing nor timing nor memory capacity.
M8 must include F5's image, stack, contexts and saved-state staging.
All-fabric must retain its response/staging capacity too.
The 121.5-tile ceiling and 13.5-tile reserve remain unchanged.

The [owner's memory decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081706413) replaces the approximately 128 KB firmware budget.
The [F5 ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081705916) allows 224 KB, AECP included.
Budget about 50 RAMB36 tiles for the complete firmware allocation.
The [F5 preflight](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081556432) measured 94,688 bytes for shipping 1x1 with one interface.
The largest supported shape with two interfaces measured 147,360 bytes.
Both fixtures retain F1 but exclude AECP and its descriptor image.
These are linked spans, not mapped RAMB36 measurements or irreducible minima.

The [memory ledger](MARK_II_AREA_PLAN.md#firmware-and-block-ram-ledger) gives each source and condition:

| Item | RAMB36 delta | RAMB18 delta | Tile delta | Image tiles after |
|---|---:|---:|---:|---:|
| Recorded route at `a5ca6e51` | 74 | 27 | 87.5 | 87.5 |
| L2 credited removals: AECP and SRP storage | -6 | -1 | -6.5 | 81 |
| Measured mailbox replacement | +1 | +10 | +6 | 87 |
| M8a reuse of existing BIOS ROM and SRAM, estimate | -18 | -1 | -18.5 | 68.5 |
| Total firmware allocation, including reused CPU memory | +50 | 0 | +50 | 118.5 |
| M2 maximum additional allocation | +2 | 0 | +2 | 120.5 |
| Conditional release of remaining wrapper storage | -10 | -2 | -11 | 109.5 |

The CPU-memory reuse uses the [historical SoC census](../findings/649_RESOURCE_MAP_AND_SENSITIVITY.md#the-soc-tops-own-logic).
M8a must confirm it at the actual checkpoint.
Retained boot storage outside the firmware allocation adds a debit.
Descriptor images, alignment and saved-state staging outside it add debits.
Without that reuse, the totals become 139 and 128 tiles.
Neither fits the ceiling.

The nominal 50 tiles use approximately 4.5 KB raw capacity each.
A 4 KiB usable mapping would require 56 tiles for 224 KiB.
Actual primitive counts decide fit; the byte-to-tile estimate cannot prove it.
At 50 tiles, the ledger leaves one tile before conditional reclamation.
After it, twelve tiles remain below 121.5.
At 56 firmware tiles, the conditional total is 115.5, leaving six.
The separate 13.5-tile reserve remains untouched in these estimates.
Unpriced integration buffers and M6/M7 conversions consume the remaining allowance.

Above 50 firmware tiles, the remaining wrapper stores give way first.
They are five RX pools, MRP strip, TX slots, timer, trace, RX validator and `ctl_fifo`.
The plan names their exact [scopes and counts](MARK_II_AREA_PLAN.md#firmware-and-block-ram-ledger): eleven tiles altogether.
These credits require full removal and debiting every replacement store.
D2 still requires equivalent diagnostics.
If more capacity is needed, defer M2's two-tile MAC/CSR FIFO conversion.
Defer new M6/M7 RAM conversions next; reprice every lost LUT saving.
Keep existing functionality, capacities and the 10 percent reserve.
Further unmet demand needs a manager ruling commissioning redesign.
Partial placement cannot claim retained AECP or wrapper storage as released.
Its same 50-tile hold gives 126.5 before additional fabric-AECP staging.
M0s must replace that over-ceiling estimate with the actual allocation.

Both M0s routes, the default flip and M9 publish memory-ledger reconciliation.
Report linked text, rodata, data, BSS, stack and static pools.
Count pools once; identify alignment, descriptor images and staging separately.
Report usable bytes, RAMB36/RAMB18 allocation and unused firmware capacity.
Cover shipping and largest supported shapes at one and two interfaces.
List the five largest BSS consumers and a reduction option each.
F5 changes no footprint outside AECP's own implementation.
The flip needs routed LUT, FF, RAMB36/RAMB18 and timing evidence.
Firmware must reside in block RAM, with total use at most 121.5 tiles.
Missing evidence or exceeding that ceiling prevents the default flip.

The [fallback scenarios](MARK_II_AREA_PLAN.md#no-split-and-partial-flip-estimates) price retained fabric AECP separately.
No-split central is 45,667 before M3/M10.
Including them gives 41,867.
The partial case qualifies F0-F4 while F5 stays unqualified.
AECP, notification, originator and their NVM path remain fabric-owned.
F1/F3 owns moved binding persistence.
Integration must preserve single ownership.
The partial removal basis is 8,012 LUTs.
Mailbox, integration and mapping allowances leave 3,910 centrally.
The range is 1,410-5,910.
Remaining M-lane savings are 4,600 centrally.
Their range is 2,900-6,700.
For fabric AECP, M3/M10 add 3,800 centrally.
Their range is 2,400-5,100.
M3 must preserve a separate removable engine for M10.

| Placement | Case | Estimated image LUT | Headroom to 38,040 | Headroom to 37,659 |
|---|---|---:|---:|---:|
| Full split | Conservative | 35,867 | +2,173 | +1,792 |
| Full split | Central | 31,667 | +6,373 | +5,992 |
| Full split | Optimistic | 27,567 | +10,473 | +10,092 |
| No split, including M3/M10 | Conservative | 44,967 | -6,927 | -7,308 |
| No split, including M3/M10 | Central | 41,867 | -3,827 | -4,208 |
| No split, including M3/M10 | Optimistic | 38,467 | -427 | -808 |
| Partial, F5 unqualified | Conservative | 43,557 | -5,517 | -5,898 |
| Partial, F5 unqualified | Central | 37,957 | +83 | -298 |
| Partial, F5 unqualified | Optimistic | 32,557 | +5,483 | +5,102 |

Positive headroom meets that LUT bar; negative headroom misses.
Full split clears both bars in every estimated case.
No-split misses both throughout; partial central misses only D8.
Partial conservative misses both; partial optimistic clears both.
All cases conditionally include M8b; timing acceptance remains separate.
Without M8b, partial central is 39,657 and misses both.

No-split centrally needs another 4,208 LUTs to clear both.
Partial centrally needs 298; its conservative case needs 5,898.
F5 qualification enables the priced full-split outcome.
That removes M3/M10 credit.
Otherwise, week 4 needs a manager ruling commissioning further redesign.
That ruling must name its measured target and revised schedule.
No unpriced saving or margin exception is assumed.
A D8 exception alone cannot cure an [NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest) miss.

[D8](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5990755268)
requires at least 1 percent planning margin.
The integer ceiling is 37,659 LUTs.
The binding bar remains 38,040 with timing met.
[M0s](MARK_II_AREA_PLAN.md#lane-sequence) is owned by the manager's resource bench.
Its tooling and both measurements precede week 4.
They also precede the default flip.
First, now: route integrated F0-F4 with AECP in fabric.
Second, after F5 merges: route the complete selected split.
Both select build switches; all-fabric remains the shipping default.
F5 integration must land by week 3 for this schedule.
Later qualification does not delay the pre-flip measurement requirement.
A missing route is a missed checkpoint, never a pass.

M0s supplies reviewed split-aware recipe and gate coverage before routing.
The current recipe requires one wrapper.
The complete split removes it.
Keep named placement endpoints with comparable whole-image metrics.
Retain all-fabric shipping and standalone 1x1/8x8 references independently.
D7 compares M0s figures against the last accepted gate record.
Later lane deltas also name their matching M0s placement.
Intermediate measurements enter the ledger; M9 alone re-records acceptance.
The week-4 checkpoint and M9 consume this measurement coverage.
The default flip additionally requires the selected functions' qualification.
This page changes no record, gate implementation or policy value.

### The resource gate

[`syn/ooc/pp_resource_gate.py`](../../syn/ooc/pp_resource_gate.py) judges one recipe measurement.
[`syn/ooc/pp_resource_baseline.json`](../../syn/ooc/pp_resource_baseline.json) records three endpoints: the shipping route and the 1x1 and 8x8 standalone syntheses.
Each endpoint holds its measured record and its policy.
The [recipe](../testing/PP_SHADOW_BASELINE_RECIPE.md#resource-gate) gives the commands.

| Endpoint | LUT | FF | Slice | RAMB36 | RAMB18 | DSP | WNS floor | WHS floor | Timing fall | BRAM tile ceiling |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `route-1x1` | +500 | +600 | +80 | +0 | +0 | +0 | +0.030 ns | 0 ns | 0.25 ns | 121.5 |
| `ooc-1x1` | +250 | +250 | - | +0 | +0 | +0 | - | - | - | - |
| `ooc-8x8` | +316 | +339 | - | +0 | +0 | +0 | - | - | - | - |

A resource column is the growth a figure may take; a dash is not gated.
WNS and WHS must stay at or above their floors and may each fall by at most the timing fall.
Standalone timing is not gated: those syntheses have no I/O constraints.
The tolerances, floors and ceiling are accepted as working policy (manager ruling).
`check-baseline` reads this table and refuses a baseline whose policy differs from it in any cell.
It also requires the route's BRAM tile ceiling.

Growth beyond a tolerance, a ceiling crossed or a timing floor crossed exits 1.
A route whose status report names an unrouted net or a routing error exits 1 too: the image does not fit.
At the current +0.299 ns WNS record, the 0.25 ns fall limit binds first: a comparable candidate needs at least +0.049 ns WNS.
The absolute +0.030 ns WNS floor and zero WHS floor remain unchanged.
One more RAMB36, RAMB18 or DSP is always material.
A primitive count moves only when storage or arithmetic changes its mapping.

The LUT and FF tolerances are about 1 % of each record.
They were sized on the first record, at dev `1269cdaf`.
The next adoption, measured beside it as combination B, shows why that size.
It changes one processor block's logic, `u_nvm_port`, which grows by 83 LUTs and 33 FFs.
In the 1x1 standalone synthesis, the rest of the wrapper moved by a net +79 LUTs and +93 FFs.
That partition is the own logic of every instance the record lists outside `u_nvm_port`, 51 terms.
Its absolute movements sum to 391 LUTs and 121 FFs.
The processor top's own logic is one of those terms: -23 LUTs and +107 FFs; the 107 FFs are its timer-arm queues.
At 8x8 the whole wrapper came out 172 LUTs smaller.
A standalone tolerance below that movement would judge noise, not the change.
Both standalone endpoints passed B against the first record.

The routed image is different: it is the fit itself.
B's route grew by 625 LUTs, 366 of them outside the wrapper, where no RTL changed.
That exceeds the route's 500-LUT tolerance, so the gate rejected B with exit 1.
Optimization moving in response to a change is still that change's cost to the image.
Accepting B means recording its route as the new baseline, a reviewed decision.
A change under the tolerance passes, and the gate still prints the sub-block movements.
A figure that improves by more than its tolerance passes and prints "re-baseline recommended".
The policy stays growth-only: recording the improved measurement is what lowers the bar.

Outside the Mark II exception below, a merge moving the shipping image records its own re-baseline ([manager ruling](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5972491855)).
Its PR measures the three endpoints again on its merge result and writes them with `record --write`, the policy unchanged.
So growth under a tolerance cannot pile up unrecorded across merges.
Growth over one is accepted or refused as the change that made it, never as a later PR's.
Each endpoint's `measured` note names the dev revision its record describes.

**Mark II exception, D7.** The [manager ruling](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5990755268)
keeps intermediate lane measurements in the [plan ledger](MARK_II_AREA_PLAN.md#ledger).
M0s supplies measured placement figures against the last gate record.
Each later lane publishes its comparison and matching M0s delta.
Growth remains visible across the default flip.
M9 re-records only after meeting [NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest) with timing met.
An improvement recommendation does not authorize an intermediate re-record.
No tolerance, floor or ceiling is weakened.
A primitive increase remains a gate failure requiring explicit disposition.
The RAM-conversion estimate never waives that zero-growth policy.

The first re-baseline recorded PR [#634](https://github.com/kebag-logic/milan-fpga/issues/634)'s growth on 2026-10-03, in PR [#638](https://github.com/kebag-logic/milan-fpga/issues/638), which added the gate.
The [issue #234 baseline](../findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-10-03-after-pr-634) gives its delta per endpoint and sub-block.
The [second re-baseline](../findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-10-05-processor-ead80360) records the adopted `ead80360` image on dev `506d91db` for [#661](https://github.com/kebag-logic/milan-fpga/issues/661).
The [third re-baseline](../findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-10-06-processor-2ad2f845) records processor `2ad2f845` on dev `bd884631` for [#682](https://github.com/kebag-logic/milan-fpga/issues/682), including its changed measurement flow.
The [fourth re-baseline](../findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-10-07-processor-2ad2f845) records the same processor after [#682](https://github.com/kebag-logic/milan-fpga/issues/682) merges dev `79b086d4`, under the same measurement flow.
The fifth records [#686](https://github.com/kebag-logic/milan-fpga/issues/686)'s `KL_maap` change on its merge of dev `291710b1`, under the same flow.
Against F, its route moved by +434 LUTs, -11 FFs and +54 slices, and its WNS rose from +0.124 to +0.241 ns while WHS fell from +0.031 to +0.029 ns; both standalone records kept every figure.
In [#686](https://github.com/kebag-logic/milan-fpga/issues/686)'s routed hierarchy `KL_maap` uses 429 LUTs and 279 FFs, against 479 and 267 for the previous `KL_maap` in the [resource map](../findings/649_RESOURCE_MAP_AND_SENSITIVITY.md), and the wrapper 47 LUTs fewer than F; the rest of the LUT growth lies in blocks the change does not touch.
The [sixth re-baseline](../findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-10-08-issues-645-and-647) records [#645](https://github.com/kebag-logic/milan-fpga/issues/645) and [#647](https://github.com/kebag-logic/milan-fpga/issues/647) on their merge of dev `6aa25dec`.
Against [#686](https://github.com/kebag-logic/milan-fpga/issues/686), its route moved by -124 LUTs, +150 FFs and -9 slices, with WNS +0.058 ns and WHS +0.002 ns.
All three endpoints passed against the preceding records before being written; every policy value stays unchanged.

The gate refuses, with exit 2, to compare across a tool or recipe change.
That covers the Vivado build, the device, the design and its state, every flow command and the standalone clock.
Identical inputs with different figures are refused the same way.
So a tool's mapping change is never reported as an architectural regression.
Such a change needs a new baseline, recorded with `record --write` and reviewed as a diff.
`check` exits 0 within tolerance, 1 for a material regression only, and 2 for every input it cannot judge.
That contract holds by construction rather than input by input.
Exit 1 comes from one place, the comparison with the baseline.
Everything after the arguments are read runs inside one barrier.
Any exception there, expected or not, prints `NOT COMPARABLE:` with its reason and exits 2, so no input reaches a traceback or exit 1.
Every printed line is printable ASCII: any other character of a name or value is written escaped, as `\ud800`.
Every number the gate reads goes through one of two converters.
A whole number must be 1 to 15 ASCII digits, so its float is exact and finite; a decimal's float must be finite.
That covers every report count, the slack, the half BRAM tile, the budget cells and every number in the baseline file.
An unreadable measurement exits 2.
That covers a count or slack in any other form, and a timing summary with no timed endpoint or without its endpoint columns.
It also covers a route status report that is missing or lacks exactly one routable-nets, fully-routed-nets and routing-errors row.
`check` and `check-baseline` read the baseline file through one validator before using any field.
A baseline file that is missing or not strict JSON exits 2.
Strict JSON here has no NaN, no Infinity and no repeated key, and every key is 1 to 128 of `A-Z a-z 0-9 _ . : / -`.
That holds for every key of the baseline, the keys inside its notes included, and of the measurement's image manifest, the keys of its entries included.
The one exception is a sub-block scope name, which may also hold a generate index's brackets, as Vivado names `u_pp/g_rx_pool[5].u_rx_slots`.
A field not of the recorded shape exits 2 too: the kind, the record's and identity's fields and types, the input digest, the figures, the sub-block scopes, or a policy value that is not a number.
`record --write` never writes a baseline that this validator would refuse.
A seeded generative test changes baselines and reports at random: every case must exit 0, 1 or 2 without a traceback, give its reason with 2, and exit 2 when it breaks a documented shape.
The self-test runs 500 cases on its fixtures; `--fuzz` runs any number on a real measurement directory.

### Where the gate runs

Hosted CI has no Vivado.
The fast workflow runs the gate's self-test, its mutant campaign and `check-baseline` (manager ruling).
Those need only Python, so no runner or tool is added.
`check-baseline` refuses a baseline edit that breaks its own policy or departs from the policy table above.
The classifier files this page as read by a gate, so a change to it alone still runs that step.

The measurement and `check` need Vivado, so they run in the manager's local bank.
The manager's merge bank runs it for every PR that changes RTL, the processor pin or the build recipe (manager ruling).
That is the route and the 1x1 standalone synthesis.

The bank also catches a predecessor that moved the image without recording its re-baseline ([manager ruling](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5972491855)).
The trigger is the merge result's delta from the recorded baseline, not the PR's own diff.
That baseline is the dev revision each endpoint's `measured` note names.
So the bank runs the comparison for any merge whose dev delta since that revision touches RTL, the processor pin or the build recipe.
That holds even when the PR itself changes none of them.
Growth the PR did not make is not charged to it.
Outside Mark II, the predecessor's growth is first recorded with attribution,
as issue [#234](https://github.com/kebag-logic/milan-fpga/issues/234) recorded PR [#634](https://github.com/kebag-logic/milan-fpga/issues/634)'s; the PR uses that record.
For Mark II, D7 instead retains the last gate record until M9.
Its ledger distinguishes predecessor movement from the current lane's delta.
Both the comparison and any regression remain visible.
This is the bank's rule, stated here; it adds no tooling.
Here a route took 39 to 56 minutes and a 1x1 standalone synthesis 15 to 24, sharing the host.
That bank run is the local half of [#234](https://github.com/kebag-logic/milan-fpga/issues/234)'s fourth criterion (manager ruling); CONTRIBUTING is unchanged here.

A Yosys-based hosted ratchet is not proposed.
[The Yosys gate's documentation](../../syn/yosys/README.md#the-cells-record) records a deliberate decision against a checked-in cell baseline.
Yosys LUT counts do not predict Vivado's, and Yosys reports no timing.
The hosted Yosys gate also synthesizes the wrapper at its module defaults, eight streams each way.
That is not the shipping shape.
