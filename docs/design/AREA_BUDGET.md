# Area budget

The AX7101 release fit is decided by the placed Vivado utilization report and
post-route timing, never by an elaboration estimate. Yosys out-of-context
figures are useful for comparing isolated fabric blocks; the builder's model is
useful for refusing obviously oversized configurations. Neither is a placement
result.

The current command and media-clock claims are checked against the
[Milan feature status ledger](../reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `aem.served-command-set` | `implemented` | - |
| `crf.media-clock-consumption` | `missing` | - |
<!-- milan-feature-status:end -->

## Contents

- **[Rules for optional blocks](#rules-for-optional-blocks)** — The default-present, elaboration-time, safe-tie, and evidence rules every prune must follow.
- **[Tier 1 - implemented optional fabric blocks](#tier-1---implemented-optional-fabric-blocks)** — The RTL parameter, SoC flag, configuration key, and permitted absence condition for each implemented prune.
- **[Isolated synthesis estimates](#isolated-synthesis-estimates)** — Comparable Yosys resource estimates for the optional fabric blocks at the measured shape.
- **[Release accounting](#release-accounting)** — The placed utilization, timing, identity, and repeated evidence required for a release candidate.

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
| MAAP engine | `MAAP_P` | `--no-maap` | `maap` | stream destination addresses are statically provisioned |
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
