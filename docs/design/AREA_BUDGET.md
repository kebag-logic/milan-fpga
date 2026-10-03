# Area budget

The AX7101 release fit is decided by the placed Vivado utilization report and
post-route timing, never by an elaboration estimate. Yosys out-of-context
figures are useful for comparing isolated fabric blocks; the builder's model is
useful for refusing obviously oversized configurations. Neither is a placement
result.

The [protocol processor baseline](../findings/PP_SHADOW_BASELINE.md) records issue #231.
It also records issue #587's 50 MHz 8x8 rerun.
It separates standalone synthesis from integrated implementation.
Its [recipe](../testing/PP_SHADOW_BASELINE_RECIPE.md) binds both product geometries.
The [issue #234 baseline](../findings/234_PP_SHADOW_AREA_BASELINE.md) measures the current head.
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
- **[Protocol processor budget and resource gate](#protocol-processor-budget-and-resource-gate)** -- NFR-RES-01's 60 % LUT target against the measured shipping route, the open allocation decision, and the resource gate's tolerances, refusals and where it runs.

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

Measured with `syn/yosys/ooc.sh` at the 8-stream, 16-slot fabric shape. These
are comparison numbers, not guaranteed savings after placement.

> **Entity-shape provenance.** The stream and slot parameters above do not
> identify the generated entity shape bound through
> `` `include "gen/adp_shape_defaults.svh" ``. At the time of this measurement,
> `ooc.sh` named no `configs/generated/**` include directory, so the record
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

Issue #234 measured the shipping 1x1 image at dev `1269cdaf`, processor pin `631eeb34`.
The [issue #234 baseline](../findings/234_PP_SHADOW_AREA_BASELINE.md) holds the method, every figure and its receipt.

### Headroom target

NFR-RES-01 in the [requirements](../reference/FR_NFR.md) is the accepted headroom target.
The baseline product must fit `xc7a100t` with at most 60 percent of its LUTs used.
The routed shipping image does not meet it today:

| Resource | Device | Shipping route, dev `1269cdaf` | Used | Target | Status |
|---|---:|---:|---:|---|---|
| Slice LUT | 63,400 | 50,128 | 79.07 % | NFR-RES-01: at most 38,040 (60 %) | not met, 12,088 over |
| Slice register | 126,800 | 59,006 | 46.53 % | none stated | - |
| Slice | 15,850 | 15,815 | 99.78 % | must stay below the device to place | 35 free |
| Block RAM tile | 135 | 92.5 | 68.52 % | proposed reserve: 13.5 tiles (10 %) | 42.5 free |
| DSP | 240 | 14 | 5.83 % | none stated | - |
| WNS / WHS | - | +0.063 / +0.036 ns | - | [build gate](../integration/BUILDING.md#5-gates-before-a-build-is-good): at least +0.03 / 0 ns | met |

The slice row is the binding limit: placement has 35 slices left.
The routed critical path, 36 logic levels, lies inside the protocol processor.

### Allocation to the protocol processor

The standalone wrapper uses 24,343 LUTs, 38.4 % of the device, at the shipping clock.
Epic #229's milestone keeps the non-CPU stack under 30 %, 19,020 LUTs.
Read as `milan_datapath`, that stack names 41,527 LUTs in the routed image, 65.5 % of the device.
The wrapper names 23,937 of them in that rebuilt hierarchy.
On any reading, the wrapper alone exceeds the milestone.

Meeting NFR-RES-01 with the rest of the image unchanged needs the wrapper below 11,849 LUTs.
That is a 12,088-LUT cut, half of the wrapper.
The ranked levers in the baseline estimate about 3,600 LUTs.
The allocation that meets both targets therefore needs an owner decision.
Until then the gate holds every resource at its recorded value: no material growth.

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
The 0.25 ns fall limit matters only once the route has margin; at +0.063 ns the floor binds first.
One more RAMB36, RAMB18 or DSP is always material.
A primitive count moves only when storage or arithmetic changes its mapping.

The LUT and FF tolerances are about 1 % of each record.
The next adoption, measured as combination B, shows why that size.
It changes one processor block's logic, which grows by 83 LUTs.
In the 1x1 standalone synthesis, blocks it did not touch moved by a net 101 LUTs and 95 FFs.
At 8x8 the whole wrapper came out 172 LUTs smaller.
A standalone tolerance below that movement would judge noise, not the change.
Both standalone endpoints pass B.

The routed image is different: it is the fit itself.
B's route grows by 625 LUTs, 366 of them outside the wrapper, where no RTL changed.
That exceeds the route's 500-LUT tolerance, so the gate rejects B with exit 1.
Optimization moving in response to a change is still that change's cost to the image.
Accepting B means recording its route as the new baseline, a reviewed decision.
A change under the tolerance passes, and the gate still prints the sub-block movements.
A figure that improves by more than its tolerance passes and prints "re-baseline recommended".
The policy stays growth-only: recording the improved measurement is what lowers the bar.

The gate refuses, with exit 2, to compare across a tool or recipe change.
That covers the Vivado build, the device, the design and its state, every flow command and the standalone clock.
Identical inputs with different figures are refused the same way.
So a tool's mapping change is never reported as an architectural regression.
Such a change needs a new baseline, recorded with `record --write` and reviewed as a diff.
An unreadable measurement, a slack that is not finite, a timing summary with no timed endpoint and a missing route status report also exit 2.
So does a baseline file that is missing, not JSON or incomplete; exit 1 means a material regression only.

### Where the gate runs

Hosted CI has no Vivado.
The fast workflow runs the gate's self-test, its mutant campaign and `check-baseline` (manager ruling).
Those need only Python, so no runner or tool is added.
`check-baseline` refuses a baseline edit that breaks its own policy or departs from the policy table above.
The classifier files this page as read by a gate, so a change to it alone still runs that step.

The measurement and `check` need Vivado, so they run in the manager's local bank.
The proposal is one run per merge candidate that moves the processor pin, `KL_pp_shadow`, the shipping configuration or the build flow.
That is the route and the 1x1 standalone synthesis.
Here a route took 50 to 56 minutes and a 1x1 standalone synthesis 15 to 24, sharing the host.
Making it part of the merge bar is an owner decision; CONTRIBUTING is unchanged here.

A Yosys-based hosted ratchet is not proposed.
[The Yosys gate's documentation](../../syn/yosys/README.md#the-cells-record) records a deliberate decision against a checked-in cell baseline.
Yosys LUT counts do not predict Vivado's, and Yosys reports no timing.
The hosted Yosys gate also synthesizes the wrapper at its module defaults, eight streams each way.
That is not the shipping shape.
