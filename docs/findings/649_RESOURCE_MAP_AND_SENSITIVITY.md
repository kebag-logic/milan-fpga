# Whole-image resource map and design-parameter sensitivity for issue #649

Measured 2026-10-04 for issue #649, a side project of the #229 area epic and an input to the #640 redesign.
It measures and analyses only: no RTL, configuration, shipping shape or gate baseline changes here.
The image is the shipping `endstation_ax7101_1x1_tdm8` route at dev `241f9184`.
The opportunities at the end are recommendations, each with its cost in function; none is applied.

## Contents

- **[Summary](#summary)** -- What the map and the sweep found, in a few lines, and what they mean for #640.
- **[Method](#method)** -- The reused route, the map script and its seven ties, the Yosys sweep, the Vivado anchors, the SoC exports and the models.
- **[Whole-image map](#whole-image-map)** -- Every block of the routed image with LUT, FF, BRAM, DSP, CARRY4 and slices, tied to the recorded totals, and the SoC top split by cell name.
- **[Parameter inventory](#parameter-inventory)** -- Every parameter that moves resources, with its source of truth, shipping value and swept values, and the `sweep.sh` stream-count trap.
- **[Sensitivity](#sensitivity)** -- Per-stream, per-channel and per-slot models with residuals, the marginal cost of each optional block and option, the processor parameters, the SoC options and the second port.
- **[Yosys and Vivado calibration](#yosys-and-vivado-calibration)** -- Vivado over Yosys at the four anchors, per block and in total, and the route over Vivado out of context.
- **[Ranked opportunities](#ranked-opportunities)** -- Where the area is, ranked, each with its measured cost, its estimated saving and its cost in function; nothing applied.
- **[Run receipts](#run-receipts)** -- Every Vivado and Yosys run's exit status, duration and log digest.

## Summary

- **Where the area is.** The shipping route's 50,767 LUTs split into the protocol processor (23,904, 47.1 percent), the rest of the datapath (18,296, 36.0 percent) and the SoC side (8,567, 16.9 percent). Outside the processor, the gPTP plane (5,004) and the CSR block (3,073) are the two large blocks; the other 34 blocks and the datapath's own logic hold under 1,100 LUTs each. Every block, 175 in all, is tied to the recorded route.
- **Streams are the expensive parameter.** Out of context, each stream per direction adds 3,828 LUTs, 2,911 FFs and 1.5 BRAM tiles, two thirds of the LUTs in the processor. With 18 slices free, no shape above 1x1 fits this device.
- **Channels and the TDM bus width are free.** Eight channels per stream cost the same as two, and 32 capture slots the same as 8; the render lane is what costs, 499 routed LUTs.
- **The optional blocks are small against the gap.** Pruning the RX address filter, the latency taps, the loopback lane and the probes saves about 1,200 routed LUTs, a tenth of NFR-RES-01's 12,727-LUT gap. The other optional blocks carry functions the product ships.
- **Yosys is a direction, not a figure.** Its LUT counts are 2.2 to 2.8 times Vivado's after optimization, block ratios spread over two orders of magnitude, and it does not enforce the RTL's elaboration guards. The out-of-context Vivado anchor predicts the route within 3.3 percent.
- **Refused shapes.** The builder accepts an eight-stream TDM8 configuration that the RTL refuses (235 writable names against the saved-state backend's 128).
- **SoC options.** Every CPU and cache option is refused by the recipe's one software profile; the DDR3 controller and PHY hold 2,599 of the SoC top's 6,072 flip-flops.
- **The second port** would replicate at least 7,100 routed LUTs and 9,918 FFs of measured per-port blocks, plus its MAC; nothing is recommended about it.

## Method

### The image and its route

Dev `241f9184` is the merge of PR #638.
That PR's round-7 measurement routed its merge commit `4d81e10d` with the [baseline recipe](../testing/PP_SHADOW_BASELINE_RECIPE.md).
Between `4d81e10d` and `241f9184` only documentation and `syn/ooc/pp_resource_baseline.json` change.
So that route is dev `241f9184`'s image, and this page reuses it rather than routing again.
Its checkpoint `alinx_ax7101_route.dcp` hashes to `769a04bb733f2281`, the digest PR #638's receipts record.
Its totals are the gate's `route-1x1` record: 50,767 LUT, 59,634 FF and 15,832 slices.

### The map

[`route_map.tcl`](../../syn/resmap/route_map.tcl) reopens the routed checkpoint and changes nothing.
It writes three inputs:

- the hierarchical utilization at depth 64 with the small-instance filter off;
- the flat utilization;
- a census of every primitive cell with its placed site and BEL.

[`resmap_map.py`](../../syn/resmap/resmap_map.py) reads them.
A block is a leaf of the reported hierarchy: an instance with no reported child, or the own logic of one that has children, written `@own`.
The leaves partition the image.
The hierarchy is the one Vivado rebuilds after cross-boundary optimization, so its names describe placement, not source ownership.

The report gives LUT (logic, LUT RAM and SRL), FF, RAMB36, RAMB18 and DSP per block.
The census adds CARRY4, flip-flops placed in I/O tiles and slices.
A slice is shared among the leaves whose cells sit in it, in proportion to the BELs each occupies.

Seven ties must hold before the script prints a figure; each compares two independent readings:

| Tie | What is compared |
|---|---|
| Ancestry | Each instance's FF, RAMB36, RAMB18 and DSP, against its own row plus its children. Its LUT columns may be smaller than their parts: the report counts a LUT shared by two children in both, and the difference is kept as that instance's sharing adjustment, never positive |
| Partition | The top row, against the leaves plus every sharing adjustment, in every column |
| Flat report | The top row, against the flat utilization report |
| Record | The top row, the slices and the census's CARRY4, against the `route-1x1` record; every processor scope the record lists, against the map's row for it |
| Census | Each leaf's slice FFs, RAMB36, RAMB18 and DSP counted cell by cell, against its report row |
| Slices | The sum of the slice shares, against the record's 15,832 |
| Depth | The deepest reported row, which must lie above the requested depth |

`resmap_map.py --selftest` builds a small consistent image, ties it, and plants one wrong figure per tie: 11 arms, each caught by name.
The first tie of the real image failed on 21 flip-flops: the census counted the ones packed into I/O tiles, which the report's FF column leaves out.
They are now counted apart, and one self-test arm plants that mistake.

### The sweep

[`sweep_plan.json`](../../syn/resmap/sweep_plan.json) names every sweep point.
Each point is the shipping shape with the changes it names.
[`yosys_sweep.py`](../../syn/resmap/yosys_sweep.py) prices them:

- Sources are the record `syn/ooc/dp_srcs.py` derives from `syn/yosys/run.sh`; none is listed by hand.
- A `milan_datapath` point rewrites the parameter defaults of a scratch copy of the top, because `chparam` cannot re-derive that top. A processor point uses `chparam`. A package or module constant is rewritten in a scratch copy of its one source.
- An entity shape that no tracked configuration provides is generated: the shipping configuration with only its stream section, or the named lines, changed, run through the builder in a scratch export of `HEAD`.
- The three ROM images come from `syn/yosys/ooc.sh` and are re-hashed against `syn/yosys/rom_digests.tsv` at every copy.
- The instrument is the recipe's hierarchy-preserving mapping, `synth_xilinx -family xc7` without `-flatten`. Every block's cells stay in its module, so a point's blocks are read off `stat -json` and tied to Yosys's own design totals.
- The stream-count points are also mapped flattened, the `ooc.sh` instrument.

Columns follow `ooc.sh`: LUT counts LUT1 to LUT6 plus the LUT6 equivalents of distributed RAM, and FF counts FD* cells.
Yosys 0.66 and sv2v v0.0.13 ran every point.

**Elaboration guards.**
sv2v turns an elaboration-time `$error` in a generate block into an `initial $display`, which Yosys does not enforce.
So a point the RTL refuses still maps, with no error: neither `ooc.sh` nor `run.sh` looks for the converted message.
`yosys_sweep.py guards` lints every point with Verilator 5.050, which evaluates those guards and reports each as `USERERROR`.
A point whose guard fires is listed in [the refusals](#guard-refusals) and left out of every fit.

### Vivado calibration anchors

[`datapath_ooc.tcl`](../../syn/resmap/datapath_ooc.tcl) synthesizes `milan_datapath` out of context at four anchors: the shipping 1x1 shape, its 2x2 and 4x4 variants, and the tracked 8x8 configuration.
The 8x8 variant of the shipping shape is refused, so it is not an anchor ([guard refusals](#guard-refusals)).
It reads the point file `yosys_sweep.py vivado-point` writes, so both tools read the same derived sources and shape.
It binds every shipping parameter as a generic, uses the shipping directives (`AreaOptimized_high`, then `opt_design -directive ExploreArea`) and constrains the 50 MHz clock.
It reports after synthesis and after optimization at full depth.
It runs two threads where the route used 32, because the host is shared.

### SoC options

[`soc_sweep.py`](../../syn/resmap/soc_sweep.py) runs `sw/litex/milan_soc.py` without `--build` for each SoC variant in the plan.
Each variant is the shipping configuration's SoC arguments with the named flags changed.
A refused variant is recorded with its refusal.
An accepted one is priced twice, flattened: the CPU netlist alone, and the LiteX top with every non-LiteX module replaced by a black box.

### Models

[`resmap_models.py`](../../syn/resmap/resmap_models.py) fits everything below from the sweep's outputs.
[`resmap_tables.py`](../../syn/resmap/resmap_tables.py) renders every table between a pair of `table:` markers on this page; with `--page` and no `--write` it checks that each one equals a fresh generation.

### Reproducing

With the [baseline recipe's](../testing/PP_SHADOW_BASELINE_RECIPE.md#prerequisites) tools, Verilator 5.050, an empty `$WORK` and the routed checkpoint in `$ROUTE`:

```sh
mkdir "$WORK/route-map" && (cd "$WORK/route-map" && vivado -mode batch \
  -source "$REPO/syn/resmap/route_map.tcl" -nojournal -log route_map.log -tclargs "$ROUTE")
python3 syn/resmap/resmap_map.py map "$WORK/route-map"
python3 syn/resmap/yosys_sweep.py --work "$WORK/sweep" shapes
python3 syn/resmap/yosys_sweep.py --work "$WORK/sweep" roms
python3 syn/resmap/yosys_sweep.py --work "$WORK/sweep" --jobs 2 run
python3 syn/resmap/yosys_sweep.py --work "$WORK/sweep" --jobs 2 --verilator "$VERILATOR" guards
for point in ship streams-2 streams-4 ship-8x8; do
  python3 syn/resmap/yosys_sweep.py --work "$WORK/sweep" vivado-point "$point"
  (cd "$WORK/sweep/vivado/$point" && vivado -mode batch \
    -source "$REPO/syn/resmap/datapath_ooc.tcl" -nojournal -log ooc.log -tclargs point.txt)
done
python3 syn/resmap/soc_sweep.py --work "$WORK/sweep" --litex-python "$LITEX_PYTHON" --sdk "$SDK" export
python3 syn/resmap/soc_sweep.py --work "$WORK/sweep" price
python3 syn/resmap/yosys_sweep.py --work "$WORK/sweep" summary
python3 syn/resmap/resmap_models.py --work "$WORK/sweep" --map "$WORK/route-map" --out "$WORK/models"
python3 syn/resmap/resmap_tables.py --work "$WORK/sweep" --models "$WORK/models" --map "$WORK/route-map" \
  --out "$WORK/tables.md" --page docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md
```

Each Vivado run here held the host's shared Vivado lock, one at a time.
The `soc_sweep.py` exports need the scratch export `shapes` writes, and the SDK triple comes from the SDK installer, as in the recipe.

## Whole-image map

`resmap_map.py map` ties every check on the reopened route: 175 blocks at depth 5.

| Quantity | Map | Flat report | `route-1x1` record |
|---|---:|---:|---:|
| LUT | 50,767 | 50,767 | 50,767 |
| FF (slice registers) | 59,634 | 59,634 | 59,634 |
| Slices | 15,832.0 | 15,832 | 15,832 |
| RAMB36 / RAMB18 | 79 / 27 | 79 / 27 | 79 / 27 |
| DSP | 14 | 14 | 14 |
| CARRY4 | 3,506 | - | 3,506 |
| Flip-flops in I/O tiles | 21 | - | - |

The 21 I/O-tile flip-flops are the GMII transmit and receive registers, 18 of them, and the TDM `bclk`, `fsync` and `dout` registers.
They are not slice registers, so no FF figure here or in the record includes them.

### The image

`@own` at this level is the LiteX top's own logic.

<!-- table: map-image -->
| Scope | LUT | Logic | LUTRAM | SRL | FF | IOB FF | RAMB36 | RAMB18 | DSP | CARRY4 | Slices | LUT % of image |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `milan_datapath` | 42,200 | 40,388 | 1,812 | 0 | 48,433 | 3 | 30 | 12 | 14 | 3,107 | 13,083.0 | 83.12 |
| `@own` | 4,847 | 4,551 | 294 | 2 | 6,072 | 18 | 47 | 10 | 0 | 274 | 1,535.7 | 9.55 |
| `VexiiRiscvLitex_f5f08b170311db53220574624f819159` | 3,524 | 3,400 | 122 | 2 | 4,734 | 0 | 2 | 5 | 0 | 114 | 1,128.8 | 6.94 |
| `KL_gptp_gmii_launch` | 186 | 186 | 0 | 0 | 317 | 0 | 0 | 0 | 0 | 3 | 68.1 | 0.37 |
| `KL_mac_rmon_events` | 49 | 49 | 0 | 0 | 78 | 0 | 0 | 0 | 0 | 8 | 16.5 | 0.10 |
| sharing adjustment | -39 | -39 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | - |
| **alinx_ax7101** | 50,767 | 48,535 | 2,228 | 4 | 59,634 | 21 | 79 | 27 | 14 | 3,506 | 15,832.0 | 100.00 |
<!-- end table: map-image -->

The datapath, `milan_datapath`, places 83.1 percent of the LUTs and 82.6 percent of the slices.
The protocol processor, `pp_shadow`, is 47.1 percent of the LUTs and 45.0 percent of the slices on its own.
The SoC side, everything outside `milan_datapath`, is 8,567 LUTs: the LiteX top's own logic (`@own`, 4,847), the CPU (3,524) and two parent blocks.
It holds 49 of the 79 RAMB36 and 15 of the 27 RAMB18, and no DSP.

### Inside the datapath

<!-- table: map-datapath -->
| Scope | LUT | Logic | LUTRAM | SRL | FF | IOB FF | RAMB36 | RAMB18 | DSP | CARRY4 | Slices | LUT % of image |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `milan_datapath/pp_shadow` | 23,904 | 22,796 | 1,108 | 0 | 24,265 | 0 | 21 | 3 | 8 | 1,576 | 7,121.8 | 47.09 |
| `milan_datapath/g_gptp_plane.u_gptp_shadow` | 5,004 | 4,496 | 508 | 0 | 5,899 | 0 | 3 | 3 | 4 | 339 | 1,571.4 | 9.86 |
| `milan_datapath/csr` | 3,073 | 3,073 | 0 | 0 | 2,141 | 0 | 0 | 2 | 0 | 37 | 703.5 | 6.05 |
| `milan_datapath/chan_map_capture` | 1,079 | 1,079 | 0 | 0 | 1,321 | 0 | 1 | 0 | 0 | 20 | 326.1 | 2.13 |
| `milan_datapath/g_mmcm_servo.mmcm_servo` | 899 | 899 | 0 | 0 | 814 | 0 | 0 | 0 | 0 | 156 | 236.9 | 1.77 |
| `milan_datapath/avtp_rx_monitor` | 889 | 889 | 0 | 0 | 1,353 | 0 | 0 | 1 | 0 | 71 | 304.9 | 1.75 |
| `milan_datapath/aaf_latency_tap_bank` | 674 | 674 | 0 | 0 | 621 | 0 | 0 | 0 | 0 | 72 | 190.9 | 1.33 |
| `milan_datapath/aaf_packetizer` | 622 | 622 | 0 | 0 | 1,331 | 0 | 1 | 1 | 0 | 9 | 251.3 | 1.23 |
| `milan_datapath/@own` | 563 | 563 | 0 | 0 | 2,805 | 0 | 0 | 0 | 0 | 65 | 456.6 | 1.11 |
| `milan_datapath/g_rx_filter.rx_filter` | 512 | 512 | 0 | 0 | 1,570 | 0 | 0 | 0 | 0 | 0 | 247.4 | 1.01 |
| `milan_datapath/avtp_rx_parser` | 501 | 501 | 0 | 0 | 706 | 0 | 0 | 0 | 0 | 83 | 161.0 | 0.99 |
| `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render` | 499 | 499 | 0 | 0 | 623 | 1 | 3 | 0 | 0 | 0 | 141.7 | 0.98 |
| `milan_datapath/g_aaf_meter.aaf_clock_meter` | 483 | 451 | 32 | 0 | 630 | 0 | 0 | 0 | 0 | 91 | 153.3 | 0.95 |
| `milan_datapath/g_maap.maap_engine` | 479 | 479 | 0 | 0 | 267 | 0 | 0 | 0 | 0 | 65 | 110.3 | 0.94 |
| `milan_datapath/render_setpoint` | 381 | 253 | 128 | 0 | 137 | 0 | 0 | 0 | 0 | 14 | 88.9 | 0.75 |
| `milan_datapath/media_grid_align` | 373 | 373 | 0 | 0 | 107 | 0 | 0 | 0 | 0 | 77 | 81.8 | 0.73 |
| `milan_datapath/crf_tx` | 317 | 317 | 0 | 0 | 311 | 0 | 0 | 0 | 1 | 19 | 90.1 | 0.62 |
| `milan_datapath/ptp_sync` | 297 | 297 | 0 | 0 | 405 | 0 | 0 | 0 | 0 | 36 | 97.5 | 0.59 |
| `milan_datapath/aaf_rx_depkt` | 273 | 271 | 2 | 0 | 144 | 0 | 1 | 1 | 0 | 17 | 62.9 | 0.54 |
| `milan_datapath/crf_rx` | 267 | 267 | 0 | 0 | 542 | 0 | 0 | 1 | 0 | 101 | 147.8 | 0.53 |
| `milan_datapath/talker_diag` | 225 | 225 | 0 | 0 | 359 | 0 | 0 | 0 | 0 | 87 | 113.2 | 0.44 |
| `milan_datapath/media_nco` | 130 | 130 | 0 | 0 | 46 | 0 | 0 | 0 | 1 | 30 | 27.3 | 0.26 |
| `milan_datapath/chan_map_render` | 112 | 112 | 0 | 0 | 676 | 0 | 0 | 0 | 0 | 0 | 89.0 | 0.22 |
| `milan_datapath/adp_tx_mux` | 109 | 109 | 0 | 0 | 24 | 0 | 0 | 0 | 0 | 5 | 17.1 | 0.21 |
| `milan_datapath/ts_counter` | 97 | 97 | 0 | 0 | 153 | 0 | 0 | 0 | 0 | 16 | 29.3 | 0.19 |
| `milan_datapath/ctl_tx_mux` | 85 | 85 | 0 | 0 | 22 | 0 | 0 | 0 | 0 | 4 | 13.9 | 0.17 |
| `milan_datapath/g_aif_tdm_master.g_solo.aaf_capture` | 75 | 41 | 34 | 0 | 243 | 2 | 0 | 0 | 0 | 8 | 47.1 | 0.15 |
| `milan_datapath/link_guard` | 72 | 72 | 0 | 0 | 114 | 0 | 0 | 0 | 0 | 25 | 31.0 | 0.14 |
| `milan_datapath/stream_table` | 58 | 58 | 0 | 0 | 69 | 0 | 0 | 0 | 0 | 6 | 17.0 | 0.11 |
| `milan_datapath/g_gptp_plane.gptp_ctl_mux` | 55 | 55 | 0 | 0 | 23 | 0 | 0 | 0 | 0 | 5 | 10.3 | 0.11 |
| `milan_datapath/ptp_clock_validity` | 51 | 51 | 0 | 0 | 125 | 0 | 0 | 0 | 0 | 20 | 31.2 | 0.10 |
| `milan_datapath/ethernet_counters` | 40 | 40 | 0 | 0 | 449 | 0 | 0 | 0 | 0 | 40 | 78.1 | 0.08 |
| `milan_datapath/tone_gen_media` | 38 | 38 | 0 | 0 | 30 | 0 | 0 | 0 | 0 | 0 | 7.3 | 0.07 |
| `milan_datapath/crf_dp_mux` | 34 | 34 | 0 | 0 | 23 | 0 | 0 | 0 | 0 | 5 | 7.8 | 0.07 |
| `milan_datapath/media_clock_restart` | 20 | 20 | 0 | 0 | 28 | 0 | 0 | 0 | 0 | 4 | 7.4 | 0.04 |
| `milan_datapath/pp_maap_shim` | 9 | 9 | 0 | 0 | 46 | 0 | 0 | 0 | 0 | 4 | 7.1 | 0.02 |
| `milan_datapath/ctl_ifg` | 8 | 8 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 2.2 | 0.02 |
| `milan_datapath/pcm_route` | 2 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.3 | 0.00 |
| sharing adjustment | -109 | -109 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.0 | - |
| **milan_datapath** | 42,200 | 40,388 | 1,812 | 0 | 48,433 | 3 | 30 | 12 | 14 | 3,107 | 13,083.0 | 83.12 |
<!-- end table: map-datapath -->

Outside the processor the datapath holds 18,296 LUTs, 24,168 FFs and 5,961 slices.
The fabric gPTP plane is the largest block there, 5,004 LUTs, and its microcontroller `u_engine/u_ucpu` alone is 2,088.
The CSR block `csr` is next, 3,073 LUTs and 2,141 FFs.
Every DSP is in the datapath: 8 in the processor, 4 in the gPTP plane, one each in `crf_tx` and `media_nco`.

The processor's sub-blocks are #638's.
Its recorded route lists 51 scopes inside `pp_shadow`, and the map's row equals the record for every one, in LUT, FF, RAMB36, RAMB18, DSP and CARRY4.
The [#234 findings](234_PP_SHADOW_AREA_BASELINE.md#processor-sub-blocks) attribute them in source terms and rank their levers.

### The SoC top's own logic

LiteX generates the SoC top as one flat module, so the report cannot split its 4,847 LUTs.
The census can split its cells by name.
A register keeps its signal's name, so the flip-flop column attributes exactly; the classes sum to the top's own 6,072 FFs, and the script checks that.
A LUT that synthesis renamed carries no owner: 3,231 of the top's LUT cells are such anonymous cells.
LUT cells are counted before Vivado combines two into one LUT site, so they are not comparable to the LUT column.

<!-- table: map-soc-names -->
| Name class | FF | IOB FF | LUT cells | LUT-RAM cells | RAMB36 | RAMB18 | DSP |
|---|---:|---:|---:|---:|---:|---:|---:|
| DDR3 controller | 1,334 | 0 | 823 | 0 | 0 | 0 | 0 |
| DDR3 PHY | 1,265 | 0 | 873 | 1 | 0 | 0 | 0 |
| Other named cells | 1,185 | 9 | 271 | 1 | 0 | 0 | 0 |
| CSR banks and bus | 714 | 0 | 123 | 0 | 0 | 0 | 0 |
| Clock-domain crossings | 420 | 0 | 0 | 0 | 0 | 0 | 0 |
| Ethernet MAC and PHY | 368 | 9 | 123 | 0 | 0 | 0 | 0 |
| Milan NIC bridge | 272 | 0 | 77 | 0 | 0 | 0 | 0 |
| Generated FIFO storage | 199 | 0 | 34 | 582 | 29 | 9 | 0 |
| SPI flash | 194 | 0 | 57 | 0 | 0 | 0 | 0 |
| SPI master | 121 | 0 | 1 | 0 | 0 | 0 | 0 |
| Anonymous LUT | 0 | 0 | 3,231 | 0 | 0 | 0 | 0 |
| BIOS ROM and SRAM | 0 | 0 | 0 | 0 | 18 | 1 | 0 |
<!-- end table: map-soc-names -->

The DDR3 controller and its PHY hold 2,599 of the top's FFs, the largest share.
The 47 RAMB36 are the BIOS ROM and SRAM (18) and generated FIFO storage (29).

### Every block, ranked

All 175 blocks, by LUT and then FF.
`@own` alone is the SoC top's own logic; under a path it is that instance's own logic.
Processor rows are #638's recorded route, as above.

<!-- table: map-ranking -->
| Rank | Block | LUT | Logic | LUTRAM | SRL | FF | IOB FF | RAMB36 | RAMB18 | DSP | CARRY4 | Slices | LUT % of image |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `@own` | 4,847 | 4,551 | 294 | 2 | 6,072 | 18 | 47 | 10 | 0 | 274 | 1,535.7 | 9.55 |
| 2 | `milan_datapath/pp_shadow/u_pp/u_notify` | 3,149 | 3,053 | 96 | 0 | 3,301 | 0 | 0 | 0 | 0 | 188 | 955.9 | 6.20 |
| 3 | `milan_datapath/csr` | 3,073 | 3,073 | 0 | 0 | 2,141 | 0 | 0 | 2 | 0 | 37 | 703.5 | 6.05 |
| 4 | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/u_ucpu` | 2,088 | 1,956 | 132 | 0 | 728 | 0 | 1 | 1 | 4 | 105 | 393.9 | 4.11 |
| 5 | `milan_datapath/pp_shadow/u_pp/u_aecp/@own` | 1,791 | 1,791 | 0 | 0 | 1,099 | 0 | 1 | 0 | 0 | 106 | 452.1 | 3.53 |
| 6 | `milan_datapath/pp_shadow/u_pp/u_aecp/u_ucpu` | 1,716 | 1,584 | 132 | 0 | 496 | 0 | 3 | 0 | 0 | 72 | 342.7 | 3.38 |
| 7 | `milan_datapath/pp_shadow/u_pp/u_listener` | 1,407 | 1,407 | 0 | 0 | 1,110 | 0 | 5 | 0 | 0 | 28 | 345.7 | 2.77 |
| 8 | `milan_datapath/pp_shadow/u_pp/u_srp/u_encoder` | 1,317 | 1,149 | 168 | 0 | 1,062 | 0 | 0 | 0 | 0 | 99 | 365.7 | 2.59 |
| 9 | `milan_datapath/pp_shadow/u_pp/u_aecp/u_d3` | 1,317 | 1,317 | 0 | 0 | 485 | 0 | 0 | 0 | 0 | 112 | 285.9 | 2.59 |
| 10 | `milan_datapath/pp_shadow/u_pp/u_aecp/u_dyn` | 1,142 | 1,142 | 0 | 0 | 467 | 0 | 0 | 0 | 0 | 44 | 240.4 | 2.25 |
| 11 | `milan_datapath/chan_map_capture` | 1,079 | 1,079 | 0 | 0 | 1,321 | 0 | 1 | 0 | 0 | 20 | 326.1 | 2.12 |
| 12 | `milan_datapath/pp_shadow/u_pp/u_aecp/u_store` | 979 | 893 | 86 | 0 | 694 | 0 | 2 | 0 | 1 | 107 | 270.4 | 1.93 |
| 13 | `milan_datapath/avtp_rx_monitor` | 889 | 889 | 0 | 0 | 1,353 | 0 | 0 | 1 | 0 | 71 | 304.9 | 1.75 |
| 14 | `milan_datapath/pp_shadow/u_pp/u_timer` | 884 | 884 | 0 | 0 | 179 | 0 | 1 | 0 | 0 | 229 | 187.3 | 1.74 |
| 15 | `milan_datapath/pp_shadow/u_pp/u_srp/@own` | 862 | 862 | 0 | 0 | 2,792 | 0 | 0 | 0 | 0 | 0 | 626.7 | 1.70 |
| 16 | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/@own` | 852 | 544 | 308 | 0 | 2,158 | 0 | 0 | 0 | 0 | 54 | 432.3 | 1.68 |
| 17 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/vexiis_0_logic_core/@own` | 798 | 774 | 22 | 2 | 1,041 | 0 | 0 | 0 | 0 | 35 | 233.5 | 1.57 |
| 18 | `milan_datapath/pp_shadow/u_pp/u_nvm_shadow` | 793 | 695 | 98 | 0 | 1,118 | 0 | 0 | 0 | 0 | 51 | 231.9 | 1.56 |
| 19 | `milan_datapath/g_mmcm_servo.mmcm_servo/@own` | 791 | 791 | 0 | 0 | 770 | 0 | 0 | 0 | 0 | 148 | 213.1 | 1.56 |
| 20 | `milan_datapath/pp_shadow/u_pp/u_originator` | 726 | 706 | 20 | 0 | 885 | 0 | 0 | 0 | 0 | 53 | 250.8 | 1.43 |
| 21 | `milan_datapath/pp_shadow/u_pp/u_talker` | 710 | 654 | 56 | 0 | 517 | 0 | 0 | 0 | 0 | 17 | 170.5 | 1.40 |
| 22 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/@own` | 700 | 700 | 0 | 0 | 1,807 | 0 | 0 | 0 | 0 | 17 | 285.9 | 1.38 |
| 23 | `milan_datapath/aaf_packetizer` | 622 | 622 | 0 | 0 | 1,331 | 0 | 1 | 1 | 0 | 9 | 251.3 | 1.23 |
| 24 | `milan_datapath/g_gptp_plane.u_gptp_shadow/@own` | 615 | 571 | 44 | 0 | 985 | 0 | 0 | 0 | 0 | 64 | 243.6 | 1.21 |
| 25 | `milan_datapath/pp_shadow/u_pp/u_srp/u_talker` | 608 | 608 | 0 | 0 | 671 | 0 | 0 | 0 | 0 | 20 | 184.3 | 1.20 |
| 26 | `milan_datapath/pp_shadow/u_pp/u_srp/u_decoder` | 584 | 584 | 0 | 0 | 630 | 0 | 0 | 1 | 0 | 61 | 171.5 | 1.15 |
| 27 | `milan_datapath/@own` | 563 | 563 | 0 | 0 | 2,805 | 0 | 0 | 0 | 0 | 65 | 456.6 | 1.11 |
| 28 | `milan_datapath/pp_shadow/u_pp/u_rx_validator` | 548 | 548 | 0 | 0 | 751 | 0 | 0 | 1 | 0 | 45 | 191.1 | 1.08 |
| 29 | `milan_datapath/g_rx_filter.rx_filter/mac_cam` | 511 | 511 | 0 | 0 | 1,568 | 0 | 0 | 0 | 0 | 0 | 247.0 | 1.01 |
| 30 | `milan_datapath/pp_shadow/u_nvm` | 505 | 505 | 0 | 0 | 476 | 0 | 0 | 0 | 4 | 45 | 147.7 | 0.99 |
| 31 | `milan_datapath/avtp_rx_parser` | 501 | 501 | 0 | 0 | 706 | 0 | 0 | 0 | 0 | 83 | 161.0 | 0.99 |
| 32 | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/u_parser` | 485 | 485 | 0 | 0 | 370 | 0 | 0 | 0 | 0 | 52 | 127.8 | 0.95 |
| 33 | `milan_datapath/g_aaf_meter.aaf_clock_meter` | 483 | 451 | 32 | 0 | 630 | 0 | 0 | 0 | 0 | 91 | 153.3 | 0.95 |
| 34 | `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render/u_fcdc` | 482 | 482 | 0 | 0 | 24 | 0 | 3 | 0 | 0 | 0 | 77.1 | 0.95 |
| 35 | `milan_datapath/g_maap.maap_engine` | 479 | 479 | 0 | 0 | 267 | 0 | 0 | 0 | 0 | 65 | 110.3 | 0.94 |
| 36 | `milan_datapath/pp_shadow/u_pp/u_srp/u_listener` | 474 | 474 | 0 | 0 | 667 | 0 | 0 | 0 | 0 | 29 | 154.7 | 0.93 |
| 37 | `milan_datapath/pp_shadow/u_pp/u_adp` | 443 | 395 | 48 | 0 | 471 | 0 | 0 | 0 | 1 | 32 | 130.6 | 0.87 |
| 38 | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_txret` | 442 | 442 | 0 | 0 | 1,159 | 0 | 0 | 0 | 0 | 26 | 226.0 | 0.87 |
| 39 | `milan_datapath/pp_shadow/u_pp/u_nvm_port` | 439 | 439 | 0 | 0 | 127 | 0 | 0 | 0 | 0 | 58 | 96.7 | 0.86 |
| 40 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_toAxiLite4_logic_bridge/@own` | 406 | 406 | 0 | 0 | 103 | 0 | 0 | 0 | 0 | 14 | 78.7 | 0.80 |
| 41 | `milan_datapath/pp_shadow/u_pp/@own` | 382 | 382 | 0 | 0 | 3,084 | 0 | 0 | 0 | 0 | 20 | 418.3 | 0.75 |
| 42 | `milan_datapath/pp_shadow/u_pp/u_dispatch/u_aecp_q` | 382 | 190 | 192 | 0 | 287 | 0 | 0 | 0 | 0 | 6 | 80.7 | 0.75 |
| 43 | `milan_datapath/render_setpoint` | 381 | 253 | 128 | 0 | 137 | 0 | 0 | 0 | 0 | 14 | 88.9 | 0.75 |
| 44 | `milan_datapath/media_grid_align` | 373 | 373 | 0 | 0 | 107 | 0 | 0 | 0 | 0 | 77 | 81.8 | 0.73 |
| 45 | `milan_datapath/aaf_latency_tap_bank/g_ltap.aaf_latency_taps/rx_chain` | 343 | 343 | 0 | 0 | 290 | 0 | 0 | 0 | 0 | 32 | 93.8 | 0.68 |
| 46 | `milan_datapath/pp_shadow/u_pp/u_tx_slots` | 341 | 341 | 0 | 0 | 135 | 0 | 1 | 0 | 0 | 5 | 75.6 | 0.67 |
| 47 | `milan_datapath/pp_shadow/u_pp/u_aecp/u_resp` | 332 | 332 | 0 | 0 | 260 | 0 | 0 | 0 | 0 | 16 | 86.0 | 0.65 |
| 48 | `milan_datapath/aaf_latency_tap_bank/g_ltap.aaf_latency_taps/tx_chain` | 326 | 326 | 0 | 0 | 290 | 0 | 0 | 0 | 0 | 32 | 90.6 | 0.64 |
| 49 | `milan_datapath/crf_tx/@own` | 314 | 314 | 0 | 0 | 307 | 0 | 0 | 0 | 1 | 19 | 89.2 | 0.62 |
| 50 | `milan_datapath/ptp_sync` | 297 | 297 | 0 | 0 | 405 | 0 | 0 | 0 | 0 | 36 | 97.5 | 0.58 |
| 51 | `milan_datapath/pp_shadow/u_pp/u_dispatch/u_acmp_q` | 285 | 149 | 136 | 0 | 204 | 0 | 0 | 0 | 0 | 0 | 56.0 | 0.56 |
| 52 | `milan_datapath/crf_rx` | 267 | 267 | 0 | 0 | 542 | 0 | 0 | 1 | 0 | 101 | 147.8 | 0.53 |
| 53 | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/u_timer` | 245 | 245 | 0 | 0 | 320 | 0 | 0 | 0 | 0 | 28 | 77.9 | 0.48 |
| 54 | `milan_datapath/talker_diag` | 225 | 225 | 0 | 0 | 359 | 0 | 0 | 0 | 0 | 87 | 113.2 | 0.44 |
| 55 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/vexiis_0_logic_core/integer_RegFilePlugin_logic_regfile_fpga` | 225 | 225 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 8 | 29.9 | 0.44 |
| 56 | `milan_datapath/pp_shadow/u_pp/u_srp/u_admission` | 224 | 224 | 0 | 0 | 207 | 0 | 0 | 0 | 2 | 16 | 53.6 | 0.44 |
| 57 | `milan_datapath/aaf_rx_depkt/frame_fifo` | 223 | 223 | 0 | 0 | 32 | 0 | 1 | 1 | 0 | 5 | 38.4 | 0.44 |
| 58 | `milan_datapath/pp_shadow/u_pp/u_event_router` | 221 | 221 | 0 | 0 | 51 | 0 | 0 | 0 | 0 | 0 | 45.8 | 0.43 |
| 59 | `milan_datapath/pp_shadow/u_pp/u_tx_arbiter` | 204 | 204 | 0 | 0 | 182 | 0 | 0 | 0 | 0 | 4 | 51.1 | 0.40 |
| 60 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/mem_toAxi4_logic_bridge/@own` | 192 | 192 | 0 | 0 | 338 | 0 | 0 | 0 | 0 | 0 | 78.1 | 0.38 |
| 61 | `KL_gptp_gmii_launch/@own` | 178 | 178 | 0 | 0 | 201 | 0 | 0 | 0 | 0 | 3 | 49.2 | 0.35 |
| 62 | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/u_txslot` | 150 | 126 | 24 | 0 | 62 | 0 | 0 | 0 | 0 | 0 | 31.3 | 0.29 |
| 63 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/aligner` | 146 | 144 | 2 | 0 | 143 | 0 | 0 | 0 | 0 | 8 | 38.4 | 0.29 |
| 64 | `milan_datapath/pp_shadow/u_pp/u_srp/u_vlan` | 140 | 128 | 12 | 0 | 126 | 0 | 0 | 0 | 0 | 9 | 38.4 | 0.28 |
| 65 | `milan_datapath/pp_shadow/u_pp/u_scoreboard` | 138 | 138 | 0 | 0 | 169 | 0 | 0 | 0 | 0 | 16 | 44.1 | 0.27 |
| 66 | `milan_datapath/pp_shadow/u_pp/u_prng` | 133 | 133 | 0 | 0 | 150 | 0 | 0 | 0 | 0 | 22 | 46.1 | 0.26 |
| 67 | `milan_datapath/media_nco` | 130 | 130 | 0 | 0 | 46 | 0 | 0 | 0 | 1 | 30 | 27.3 | 0.26 |
| 68 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/vexiis_0_logic_core/FetchCachelessPlugin_logic_buffer_words` | 128 | 104 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 19.9 | 0.25 |
| 69 | `milan_datapath/pp_shadow/u_pp/u_ca_builder` | 127 | 127 | 0 | 0 | 152 | 0 | 0 | 0 | 0 | 0 | 39.8 | 0.25 |
| 70 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/ioBus_to_peripheral_bus_cc/a_1/@own` | 120 | 120 | 0 | 0 | 16 | 0 | 1 | 1 | 0 | 0 | 21.5 | 0.24 |
| 71 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/unified_mBus_to_mem_toAxi4_up_widthAdapter/upsize_d_ctx/contexts` | 119 | 115 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 18.5 | 0.23 |
| 72 | `milan_datapath/chan_map_render` | 112 | 112 | 0 | 0 | 676 | 0 | 0 | 0 | 0 | 0 | 89.0 | 0.22 |
| 73 | `milan_datapath/adp_tx_mux` | 109 | 109 | 0 | 0 | 24 | 0 | 0 | 0 | 0 | 5 | 17.1 | 0.21 |
| 74 | `milan_datapath/g_mmcm_servo.mmcm_servo/u_tick_cdc` | 103 | 103 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 8 | 18.5 | 0.20 |
| 75 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_read_bridge/aligner` | 99 | 91 | 8 | 0 | 122 | 0 | 0 | 1 | 0 | 8 | 32.4 | 0.20 |
| 76 | `milan_datapath/ts_counter` | 97 | 97 | 0 | 0 | 153 | 0 | 0 | 0 | 0 | 16 | 29.3 | 0.19 |
| 77 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/unified_mBus_arbiter_core/a_arbiter` | 96 | 96 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 19.7 | 0.19 |
| 78 | `milan_datapath/pp_shadow/u_pp/g_rx_pool[5].u_rx_slots` | 89 | 89 | 0 | 0 | 62 | 0 | 1 | 0 | 0 | 3 | 21.6 | 0.17 |
| 79 | `milan_datapath/ctl_tx_mux` | 85 | 85 | 0 | 0 | 22 | 0 | 0 | 0 | 0 | 4 | 13.9 | 0.17 |
| 80 | `milan_datapath/pp_shadow/u_pp/u_srp/u_domain` | 77 | 77 | 0 | 0 | 108 | 0 | 0 | 0 | 0 | 0 | 26.9 | 0.15 |
| 81 | `milan_datapath/pp_shadow/u_pp/u_normalizer` | 72 | 72 | 0 | 0 | 307 | 0 | 0 | 0 | 0 | 6 | 48.7 | 0.14 |
| 82 | `milan_datapath/link_guard` | 72 | 72 | 0 | 0 | 114 | 0 | 0 | 0 | 0 | 25 | 31.0 | 0.14 |
| 83 | `milan_datapath/pp_shadow/ctl_fifo` | 72 | 72 | 0 | 0 | 33 | 0 | 1 | 1 | 0 | 3 | 14.2 | 0.14 |
| 84 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_toAxiLite4_logic_bridge/a_buffered_fork2` | 71 | 71 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 12.3 | 0.14 |
| 85 | `milan_datapath/pp_shadow/u_pp/u_mrp_strip` | 70 | 70 | 0 | 0 | 107 | 0 | 1 | 0 | 0 | 17 | 30.6 | 0.14 |
| 86 | `milan_datapath/pp_shadow/u_pp/u_dispatch/u_adp_q` | 70 | 10 | 60 | 0 | 88 | 0 | 0 | 0 | 0 | 0 | 18.0 | 0.14 |
| 87 | `milan_datapath/g_gptp_plane.u_gptp_shadow/rx_fifo` | 69 | 69 | 0 | 0 | 33 | 0 | 1 | 1 | 0 | 7 | 15.6 | 0.14 |
| 88 | `milan_datapath/stream_table` | 58 | 58 | 0 | 0 | 69 | 0 | 0 | 0 | 0 | 6 | 17.0 | 0.11 |
| 89 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_bus_decoder_core/d_arbiter` | 58 | 58 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 9.2 | 0.11 |
| 90 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_filter_down_to_unified_mBus_cc/a_1/@own` | 57 | 57 | 0 | 0 | 16 | 0 | 1 | 1 | 0 | 0 | 10.6 | 0.11 |
| 91 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_clint_thread_core` | 55 | 55 | 0 | 0 | 208 | 0 | 0 | 0 | 0 | 24 | 41.3 | 0.11 |
| 92 | `milan_datapath/g_gptp_plane.u_gptp_shadow/tx_fifo` | 55 | 55 | 0 | 0 | 30 | 0 | 1 | 1 | 0 | 3 | 13.6 | 0.11 |
| 93 | `milan_datapath/g_gptp_plane.gptp_ctl_mux` | 55 | 55 | 0 | 0 | 23 | 0 | 0 | 0 | 0 | 5 | 10.3 | 0.11 |
| 94 | `milan_datapath/g_aif_tdm_master.g_solo.aaf_capture/u_tcdc` | 54 | 20 | 34 | 0 | 82 | 0 | 0 | 0 | 0 | 0 | 21.2 | 0.11 |
| 95 | `milan_datapath/pp_shadow/u_pp/u_side_port` | 53 | 53 | 0 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 8.0 | 0.10 |
| 96 | `milan_datapath/ptp_clock_validity` | 51 | 51 | 0 | 0 | 125 | 0 | 0 | 0 | 0 | 20 | 31.2 | 0.10 |
| 97 | `milan_datapath/aaf_rx_depkt/@own` | 51 | 49 | 2 | 0 | 112 | 0 | 0 | 0 | 0 | 12 | 24.4 | 0.10 |
| 98 | `milan_datapath/pp_shadow/u_pp/g_rx_pool[2].u_rx_slots` | 50 | 50 | 0 | 0 | 62 | 0 | 1 | 0 | 0 | 2 | 14.9 | 0.10 |
| 99 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_filter_down_to_unified_mBus_cc/d_1/@own` | 46 | 18 | 28 | 0 | 57 | 0 | 0 | 0 | 0 | 0 | 15.9 | 0.09 |
| 100 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/ioBus_to_peripheral_bus_cc/d_1/@own` | 45 | 15 | 30 | 0 | 60 | 0 | 0 | 0 | 0 | 0 | 19.7 | 0.09 |
| 101 | `milan_datapath/pp_shadow/u_pp/g_rx_pool[0].u_rx_slots` | 38 | 38 | 0 | 0 | 38 | 0 | 1 | 0 | 0 | 7 | 12.8 | 0.07 |
| 102 | `milan_datapath/tone_gen_media` | 38 | 38 | 0 | 0 | 30 | 0 | 0 | 0 | 0 | 0 | 7.3 | 0.07 |
| 103 | `milan_datapath/pp_shadow/u_pp/u_trace` | 37 | 37 | 0 | 0 | 18 | 0 | 1 | 0 | 0 | 4 | 9.2 | 0.07 |
| 104 | `milan_datapath/pp_shadow/u_pp/g_rx_pool[4].u_rx_slots` | 36 | 36 | 0 | 0 | 22 | 0 | 1 | 0 | 0 | 3 | 8.2 | 0.07 |
| 105 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_filter_logic_core` | 36 | 36 | 0 | 0 | 21 | 0 | 0 | 0 | 0 | 0 | 9.2 | 0.07 |
| 106 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_plic_intc_thread_logic` | 34 | 34 | 0 | 0 | 145 | 0 | 0 | 0 | 0 | 0 | 32.4 | 0.07 |
| 107 | `milan_datapath/crf_dp_mux` | 34 | 34 | 0 | 0 | 23 | 0 | 0 | 0 | 0 | 5 | 7.8 | 0.07 |
| 108 | `KL_mac_rmon_events/@own` | 32 | 32 | 0 | 0 | 66 | 0 | 0 | 0 | 0 | 8 | 12.9 | 0.06 |
| 109 | `milan_datapath/pp_shadow/u_pp/g_rx_pool[1].u_rx_slots` | 30 | 30 | 0 | 0 | 22 | 0 | 1 | 0 | 0 | 3 | 7.6 | 0.06 |
| 110 | `milan_datapath/pp_shadow/u_pp/u_dispatch/@own` | 28 | 28 | 0 | 0 | 48 | 0 | 0 | 0 | 0 | 12 | 14.9 | 0.06 |
| 111 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/compactor/@own` | 27 | 27 | 0 | 0 | 40 | 0 | 0 | 0 | 0 | 0 | 9.7 | 0.05 |
| 112 | `milan_datapath/g_aif_tdm_master.g_solo.aaf_capture/@own` | 21 | 21 | 0 | 0 | 161 | 2 | 0 | 0 | 0 | 8 | 25.9 | 0.04 |
| 113 | `milan_datapath/media_clock_restart` | 20 | 20 | 0 | 0 | 28 | 0 | 0 | 0 | 0 | 4 | 7.4 | 0.04 |
| 114 | `milan_datapath/g_gptp_plane.u_gptp_shadow/u_txticket` | 19 | 19 | 0 | 0 | 54 | 0 | 0 | 0 | 0 | 0 | 9.4 | 0.04 |
| 115 | `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render/@own` | 18 | 18 | 0 | 0 | 599 | 1 | 0 | 0 | 0 | 0 | 64.6 | 0.04 |
| 116 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/unified_mBus_to_mem_toAxi4_up_widthAdapter/@own` | 17 | 17 | 0 | 0 | 346 | 0 | 0 | 0 | 0 | 0 | 60.5 | 0.03 |
| 117 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/unified_mBus_decoder_core/d_arbiter` | 13 | 13 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 3.5 | 0.03 |
| 118 | `milan_datapath/pp_shadow/u_pp/u_nvm_arb` | 13 | 13 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 2.5 | 0.03 |
| 119 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/mem_toAxi4_logic_bridge/d_arbiter` | 13 | 13 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 2.4 | 0.03 |
| 120 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/mem_toAxi4_logic_bridge/a_ctx/contexts` | 13 | 9 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2.4 | 0.03 |
| 121 | `milan_datapath/pp_shadow/u_pp/u_dispatch/u_maap_q` | 11 | 7 | 4 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 2.9 | 0.02 |
| 122 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_down_arbiter_core/a_arbiter` | 11 | 11 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 2.6 | 0.02 |
| 123 | `milan_datapath/pp_shadow/@own` | 9 | 9 | 0 | 0 | 321 | 0 | 0 | 0 | 0 | 6 | 42.1 | 0.02 |
| 124 | `milan_datapath/pp_maap_shim` | 9 | 9 | 0 | 0 | 46 | 0 | 0 | 0 | 0 | 4 | 7.1 | 0.02 |
| 125 | `milan_datapath/ethernet_counters/event_counter_gen[3].counter_inst` | 8 | 8 | 0 | 0 | 32 | 0 | 0 | 0 | 0 | 8 | 8.8 | 0.02 |
| 126 | `milan_datapath/ethernet_counters/event_counter_gen[4].counter_inst` | 8 | 8 | 0 | 0 | 32 | 0 | 0 | 0 | 0 | 8 | 8.8 | 0.02 |
| 127 | `milan_datapath/ethernet_counters/event_counter_gen[5].counter_inst` | 8 | 8 | 0 | 0 | 32 | 0 | 0 | 0 | 0 | 8 | 8.8 | 0.02 |
| 128 | `milan_datapath/ethernet_counters/event_counter_gen[7].counter_inst` | 8 | 8 | 0 | 0 | 32 | 0 | 0 | 0 | 0 | 8 | 8.8 | 0.02 |
| 129 | `milan_datapath/ethernet_counters/event_counter_gen[8].counter_inst` | 8 | 8 | 0 | 0 | 32 | 0 | 0 | 0 | 0 | 8 | 9.0 | 0.02 |
| 130 | `milan_datapath/ctl_ifg` | 8 | 8 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 2.2 | 0.02 |
| 131 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/onPerId_bridge/onAw_halted_fork2` | 8 | 8 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1.2 | 0.02 |
| 132 | `KL_mac_rmon_events/gen_evt_cdc[8].gen_live_lane.evt_cdc` | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1.1 | 0.02 |
| 133 | `milan_datapath/g_mmcm_servo.mmcm_servo/u_batch_hs` | 7 | 7 | 0 | 0 | 40 | 0 | 0 | 0 | 0 | 0 | 5.3 | 0.01 |
| 134 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/mem_toAxi4_logic_bridge/a_halted_fork2` | 6 | 6 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1.4 | 0.01 |
| 135 | `KL_gptp_gmii_launch/u_rec_cdc` | 5 | 5 | 0 | 0 | 102 | 0 | 0 | 0 | 0 | 0 | 16.0 | 0.01 |
| 136 | `milan_datapath/aaf_latency_tap_bank/@own` | 5 | 5 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 1.5 | 0.01 |
| 137 | `KL_gptp_gmii_launch/u_seal_cdc` | 4 | 4 | 0 | 0 | 14 | 0 | 0 | 0 | 0 | 0 | 2.9 | 0.01 |
| 138 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_read_bridge/compactor` | 4 | 4 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 1.5 | 0.01 |
| 139 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_clint_time_cc_driver/@own` | 3 | 3 | 0 | 0 | 130 | 0 | 0 | 0 | 0 | 0 | 17.4 | 0.01 |
| 140 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_read_bridge/toTileink` | 3 | 3 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 1.0 | 0.01 |
| 141 | `milan_datapath/crf_tx/u_evt_cdc` | 3 | 3 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0.9 | 0.01 |
| 142 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/vexiis_0_priv_stoptime_regNext_cc_driver/@own` | 3 | 3 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 1.2 | 0.01 |
| 143 | `KL_mac_rmon_events/gen_evt_cdc[3].gen_live_lane.evt_cdc` | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.3 | 0.01 |
| 144 | `KL_mac_rmon_events/gen_evt_cdc[4].gen_live_lane.evt_cdc` | 2 | 2 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0.8 | 0.00 |
| 145 | `KL_mac_rmon_events/gen_evt_cdc[5].gen_live_lane.evt_cdc` | 2 | 2 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0.8 | 0.00 |
| 146 | `KL_mac_rmon_events/gen_evt_cdc[7].gen_live_lane.evt_cdc` | 2 | 2 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0.6 | 0.00 |
| 147 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/compactor/io_up_aw_fork2` | 2 | 2 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.6 | 0.00 |
| 148 | `milan_datapath/pcm_route` | 2 | 2 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.3 | 0.00 |
| 149 | `milan_datapath/aaf_latency_tap_bank/g_ltap.aaf_latency_taps/@own` | 1 | 1 | 0 | 0 | 32 | 0 | 0 | 0 | 0 | 8 | 5.0 | 0.00 |
| 150 | `milan_datapath/g_rx_filter.rx_filter/@own` | 1 | 1 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.4 | 0.00 |
| 151 | `milan_datapath/pp_shadow/u_pp/u_desc_mem_guard` | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.2 | 0.00 |
| 152 | `milan_datapath/pp_shadow/u_pp/u_lsn_admit` | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.2 | 0.00 |
| 153 | `milan_datapath/ethernet_counters/@own` | 0 | 0 | 0 | 0 | 289 | 0 | 0 | 0 | 0 | 0 | 34.0 | 0.00 |
| 154 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_filter_down_to_unified_mBus_cc/a_1/popToPushGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 1.5 | 0.00 |
| 155 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_filter_down_to_unified_mBus_cc/a_1/pushToPopGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 1.5 | 0.00 |
| 156 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_filter_down_to_unified_mBus_cc/d_1/popToPushGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 0.8 | 0.00 |
| 157 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_filter_down_to_unified_mBus_cc/d_1/pushToPopGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 1.1 | 0.00 |
| 158 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/ioBus_to_peripheral_bus_cc/a_1/popToPushGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 1.1 | 0.00 |
| 159 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/ioBus_to_peripheral_bus_cc/a_1/pushToPopGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 1.0 | 0.00 |
| 160 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/ioBus_to_peripheral_bus_cc/d_1/popToPushGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 1.8 | 0.00 |
| 161 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/ioBus_to_peripheral_bus_cc/d_1/pushToPopGray_buffercc` | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 1.8 | 0.00 |
| 162 | `milan_datapath/pp_shadow/u_pp/u_release_merge` | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0.4 | 0.00 |
| 163 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_write_bridge/onPerId_bridge/@own` | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0.4 | 0.00 |
| 164 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/bufferCC_19` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.2 | 0.00 |
| 165 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/bufferCC_20` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.2 | 0.00 |
| 166 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/cpuResetCtrl_fiber_aggregator_asyncBuffers_0` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.5 | 0.00 |
| 167 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/cpuResetCtrl_fiber_buffer` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1.0 | 0.00 |
| 168 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_clint_time_cc_driver/litex_reset_asyncAssertSyncDeassert_buffercc` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.4 | 0.00 |
| 169 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_clint_time_cc_driver/outHitSignal_buffercc` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.2 | 0.00 |
| 170 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_clint_time_cc_driver/pushArea_target_buffercc` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1.0 | 0.00 |
| 171 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/peripheral_plic_intc_to_vexiis_0_priv_mei_flag_buffercc` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.2 | 0.00 |
| 172 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/vexiis_0_priv_stoptime_regNext_cc_driver/outHitSignal_buffercc` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.2 | 0.00 |
| 173 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/vexiis_0_priv_stoptime_regNext_cc_driver/pushArea_target_buffercc` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 1.0 | 0.00 |
| 174 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/vexiis_0_priv_stoptime_regNext_cc_driver/toplevel_cpuResetCtrl_reset_asyncAssertSyncDeassert_buffercc` | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0.4 | 0.00 |
| 175 | `VexiiRiscvLitex_f5f08b170311db53220574624f819159/dma_bridge_read_bridge/onPerId_bridge` | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0.1 | 0.00 |
<!-- end table: map-ranking -->

## Parameter inventory

Every design parameter below can change the image's resources.
Its source of truth is the first place a build can set it.
The swept column names the plan points in [`sweep_plan.json`](../../syn/resmap/sweep_plan.json) that move it.

**Datapath and entity shape**

| Parameter | Source of truth | Reaches | Shipping | Swept |
|---|---|---|---:|---|
| Streams per direction | configuration `streams.listeners` and `streams.talkers` | builder `--num-streams`, `milan_datapath` `N_STREAMS`; the generated shape header's `ADP_LISTENER_SINK_C`, `ADP_TALKER_SRC_C`, `AEM_NAME_ENTRIES_C` and dynamic-map geometry, bound on `KL_pp_shadow` as `N_STREAM_IN_P`, `N_STREAM_OUT_P`, `N_SPORT_IN_P`, `N_SPORT_OUT_P`, `DESC_NAME_ENTRIES_P` | 1 | 1, 2, 4; 8 is refused at this shape, so the tracked 8x8 configuration stands in |
| Channels per stream | configuration `streams.*.channels` | builder `--talker-wire-chans`, `TALKER_WIRE_CHANS_P` | 8 | 2, 4, 8 at one stream; 2 and 8 at four streams |
| TDM capture slots | configuration `audio_interface.kind` | `--audio-interface`, `AUDIO_IF_SLOTS_P`; `AUDIO_IF_CLK_HZ_P` must divide to the bit clock | 8 | 0 (stereo I2S), 8, 16, 32 |
| TDM bus role | configuration `audio_interface` kind and master role | `--audio-interface-master`, `AUDIO_IF_MASTER_P` | master | slave only with I2S |
| TDM render slots | configuration `audio_interface.physical_channels.render` | `--audio-interface-render`, `AUDIO_IF_RENDER_SLOTS_P` | 8 | 0, 8 |
| Loopback lane | configuration `audio_interface.cluster_mapping.fabric.loopback_lane` | `--loopback-lane`, `LOOPBACK_P` | on | off |
| Media-clock servo | configuration `board.features.media_clock_servo` | `--no-media-clock-servo`, `MCSERVO_P` | on | off |
| Latency taps | `board.features.latency_taps` | `--no-latency-taps`, `LTAP_P` | on | off |
| MAAP engine | `board.features.maap` | `--no-maap`, `MAAP_P` | on | off |
| I2S playback | `board.features.i2s_playback` | `--no-i2s-playback`, `I2SPB_P` | off | on |
| RX address filter | `board.features.rx_mac_filter` | `--no-rx-mac-filter`, `RXFILT_P` | on | off |
| PCM low-pass | `board.features.render_lpf` | `--no-render-lpf`, `LPF_P` | off | on |
| Datapath probe groups | `board.features.datapath_probes` | `--no-datapath-probes`, `DPROBES_P` | on | off |
| PPS output | none; the launcher flag only | `--pps`, `PPS_P` | off | on |
| Fabric gPTP plane | `board.features.fabric_gptp`, one product value | `--fabric-gptp`, `GPTP_PLANE_EN_P` | on | off, a verification-only elaboration |
| AAF media-clock following | configuration `clocking.media_clock_sources` holding `input_stream` | shape header `AEM_N_AAF_CLKSRC_C`, the AAF clock meter | 1 | 0 |
| CRF sink and CRF output | `clocking.crf_sink`, `clocking.crf_output.enabled` | shape header counts (one processor context each); `KL_crf_rx` and `KL_crf_tx` are unconditional | both | neither |
| Datapath clock | `board.constraints.milan_clk_hz`, one product value | `MILAN_CLK_FREQ_HZ`, timer and divider widths | 50 MHz | not swept |
| Datapath width | none | `TDATA_WIDTH` | 64 | not swept: every stream interface carries it |

**Protocol processor**

| Parameter | Source of truth | Reaches | Shipping | Swept |
|---|---|---|---:|---|
| Stream contexts in and out | shape header, as above | `N_STREAM_IN_P`, `N_STREAM_OUT_P` (streams plus CRF) | 2, 2 | 2, 3, 5, 9, with stream ports 1, 2, 4, 8 |
| Writable name entries | the AEM model the builder generates | `AEM_NAME_ENTRIES_C`, `DESC_NAME_ENTRIES_P` | 39 | 39, 64, 128; 235 refused |
| Audio units and clock domains | the AEM model | `AEM_N_AUDIO_UNIT_C`, `AEM_N_CLKDOM_C`; `N_AUDIO_UNIT_P`, `N_CLK_DOM_P` | 1, 1 | 1, 2, 4 |
| Controls | the AEM model | `AEM_N_CONTROL_C`, `N_CONTROL_P` | 1 | 1, 2, 4 |
| Descriptor index entries | RTL default of `milan_datapath` `PP_DESC_IDX_ENTRIES_P` | `DESC_IDX_ENTRIES_P` | 32 | 16, 32, 64 |
| Descriptor line bytes | RTL default `PP_DESC_LINE_BYTES_P` | `DESC_LINE_BYTES_P` | 576 | 576, 768, 1008; 288, 512 and 1152 refused |
| Control receive FIFO | RTL default of `KL_pp_shadow` | `RX_FIFO_BYTES_P` | 4096 | 2048, 4096, 8192 |
| Registered controllers | package constant `PP_N_CTRL_C` | the notification registry, its timers and the CA pool | 16 | 4, 8, 12, 16; 32 refused |
| Receive slots per pool | RTL default of the processor top `RX_SLOTS_P` | the receive pools | 4 | 2, 4, 8 |
| Receive slot bytes | RTL default `RX_SLOT_BYTES_P` | the receive pools | 576 | 288, 576, 1152 |
| Standard transmit slots | RTL default `TX_STD_SLOTS_P` | the transmit slots | 4 | 2, 4, 8 |
| AVB interfaces of the ADP engine | the processor top binds `N_IF_P` to 1 | `KL_adp_engine` | 1 | 1, 2, 4, standalone |

**SoC**

| Option | Source of truth | Shipping | Measured |
|---|---|---|---|
| CPU, XLEN, core count, FPU | configuration `soc.*`; `milan_soc.py` `--cpu`, `--xlen`, `--cpu-count`, `--with-fpu` | VexiiRiscv, 32, 1, none | refused by the recipe under its one software profile |
| CPU caches | configuration `soc.scala_args`, `--scala-args` | none | refused |
| L2 cache | configuration `board.constraints.l2_bytes`, `--l2-bytes` | 0 | refused |
| Main bus standard | `--bus-standard` only | Wishbone | AXI-Lite |
| Integrated main RAM | `--main-ram-size` | DDR3 instead | no effect: DDR3 provides main RAM |
| Flash, UART, Ethernet port, I/O delays, floorplan, timing options | launcher flags | as shipped | not swept: pins, constraints and flow only |

**The `sweep.sh` stream-count trap.**
`sw/litex/sweep.sh ax7101` takes its stream count from the generated fragment `configs/generated/sweep_opts_ax7101.sh`.
That fragment is the shipping configuration's, so it builds 1x1 whatever the tag says; only `SWEEP_CFG` naming another configuration changes the shape.
Until 2026-07-26 it passed no `--num-streams` at all, and builds called 8x8 were 1x1 ([build guide](../integration/BUILDING.md#31-the-shape-gate-scriptscheck_sweep_shapepy)).
This sweep does not use `sweep.sh`.
Each point's stream count is the builder's shape for a configuration with that many streams, together with the matching `N_STREAMS`.
`milan_datapath` also carries an elaboration guard (`milan_datapath.sv:1636`) against a header whose talker-source count is neither `N_STREAMS` nor one more.
Every point's receipt records the digest of the header it elaborated.


## Sensitivity

Yosys figures below are hierarchical-mapping estimates, not placement results.
The [calibration](#yosys-and-vivado-calibration) gives their Vivado ratios; the routed block, where one ships, is the better guide to a saving.
LUT here is Yosys's `LUT_TOT`, logic LUTs plus LUT-RAM equivalents.
BRAM is in tiles: a RAMB36 is one, a RAMB18 half.

### Guard refusals

<!-- table: guard-refusals -->
| Point | Guard that fires |
|---|---|
| pp-ctrl-32 | `F08.4: owner tags OVERLAP at SI=2 SO=2 (8-bit expiry bus)` |
| pp-line-1152 | `DESC_LINE_BYTES_P=1152 is above 1008: 16 + line passes the 1024-byte cursor`; `RESP_D8_CAP_BYTES_P=1168 outside 524..1024 (the 10-bit cursor)` |
| pp-line-288 | `response buffer (304 B) is smaller than GET_DYNAMIC_INFO limit (524 B)`; `DESC_LINE_BYTES_P=288 is below 576: no room for a 71-record GET_AUDIO_MAP page`; `RESP_D8_CAP_BYTES_P=304 outside 524..1024 (the 10-bit cursor)` |
| pp-line-512 | `DESC_LINE_BYTES_P=512 is below 576: no room for a 71-record GET_AUDIO_MAP page` |
| pp-names-235 | `KL_nvm_backend: N_NAME_P=235 outside 1..128: the NAME block is 0x80..0xFF.` |
| streams-8 | `KL_nvm_backend: N_NAME_P=235 outside 1..128: the NAME block is 0x80..0xFF.` |
| streams-8-chans-2 | `KL_nvm_backend: N_NAME_P=235 outside 1..128: the NAME block is 0x80..0xFF.` |
<!-- end table: guard-refusals -->

Each refused point mapped in Yosys without an error; Verilator's lint and, for `streams-8`, Vivado refuse it.
None of these points is in a fit, and none is a product shape.
What the refusals measure:

- **An eight-stream TDM8 product is refused.** The shipping configuration with eight 8-channel streams each way has 235 writable names, and the saved-state backend holds 128 NAME records. The builder accepts that configuration; the RTL refuses it at elaboration, and Vivado stops in synthesis with `Synth 8-6058`. The buildable eight-stream shape is the tracked `endstation_ax7101_8x8` configuration, with TDM32, no render lane and 107 names, so it is the eight-stream anchor here.
- **The descriptor line holds 576 to 1,008 bytes.** Below 576 a GET_AUDIO_MAP page of 71 records does not fit, and above 1,008 the response cursor's 10 bits overflow.
- **32 registered controllers overlap the processor's timer owner tags.** The controller fit therefore uses 4, 8 and 16 controllers, plus 12.

### Streams and channels

N is streams per direction, C channels per stream.
Each stream point's shape is the builder's for the shipping configuration with N listeners and N talkers of C channels, so it also carries the matching CRF contexts, name entries and dynamic-map geometry.

**Vivado anchors.** `milan_datapath` out of context after `opt_design`, at the shipping directives:

<!-- table: vivado-opt-data -->
| Anchor | N | LUT | FF | BRAM | DSP | LUT residual |
|---|---:|---:|---:|---:|---:|---:|
| ship | 1 | 43,622 | 48,697 | 36.0 | 14 | -364 |
| streams-2 | 2 | 48,361 | 51,521 | 39.5 | 14 | 547 |
| streams-4 | 4 | 55,288 | 57,413 | 41.0 | 14 | -182 |
<!-- end table: vivado-opt-data -->

<!-- table: vivado-opt-fit -->
| Measure after optimization | Fixed | Per stream | Points | Residual RMS | Largest residual |
|---|---:|---:|---:|---:|---:|
| LUT | 40,158.5 | 3,827.9 | 3 | 393.6 | 546.6 |
| FF | 45,751.0 | 2,911.1 | 3 | 37.6 | 52.3 |
| BRAM | 35.2 | 1.5 | 3 | 0.8 | 1.2 |
| DSP | 14.0 | 0.0 | 3 | 0.0 | 0.0 |
<!-- end table: vivado-opt-fit -->

Over the three anchors on the stream line, each stream per direction adds 3,828 LUTs, 2,911 FFs and 1.5 BRAM tiles after optimization, with a residual RMS of 394 LUTs.
The growth is a little less than linear: the second stream costs 4,739 LUTs and the third and fourth 3,464 each.
The processor takes 2,478 LUTs and 1,155 FFs of each stream: about two thirds of the LUTs and two fifths of the flip-flops.
The datapath's own logic takes 879 FFs, the per-stream registers it keeps outside its blocks.
The channel-map capture, the CSR block, the listener monitor and the render setpoint take 205 to 317 LUTs each, and no DSP moves.
The tracked 8x8 configuration is a different audio shape, so it calibrates the tools but is not fitted here.
At 60,454 LUTs it lies 10,328 below the line's value at eight streams; the blocks it prunes (the render lane, the latency taps, the loopback lane and the probes) are about 1,200 routed LUTs of that, so the growth per stream falls further above four streams.

The blocks that grow with N, after optimization:

<!-- table: vivado-opt-blocks -->
| Block | LUT at N=1 | LUT per stream | LUT RMS | FF per stream | BRAM per stream |
|---|---:|---:|---:|---:|---:|
| `KL_pp_shadow` | 25,094 | 2,478.1 | 61.7 | 1,155.3 | 1.54 |
| `KL_chan_map_capture` | 1,080 | 316.9 | 14.7 | 350.9 | 0.00 |
| `milan_csr` | 2,893 | 210.6 | 119.4 | 27.9 | 0.00 |
| `KL_avtp_rx_monitor_ctx` | 1,011 | 208.5 | 81.0 | 24.8 | 0.00 |
| `KL_render_setpoint` | 380 | 205.1 | 0.9 | 28.0 | 0.00 |
| `@own` | 230 | 137.1 | 0.5 | 878.6 | 0.00 |
| `KL_aaf_packetizer` | 655 | 95.4 | 98.8 | 33.5 | -0.00 |
| `KL_chan_map_render` | 119 | 87.1 | 8.2 | 192.0 | 0.00 |
| `KL_talker_diag_ctx` | 281 | 65.6 | 17.9 | 166.0 | 0.00 |
| `KL_stream_table` | 58 | 55.1 | 3.9 | 69.0 | 0.00 |
| `KL_crf_rx` | 300 | -23.6 | 14.5 | 0.0 | 0.00 |
| `timestamp_counter` | 97 | 15.4 | 21.4 | 0.0 | 0.00 |
| `KL_maap` | 507 | -9.4 | 2.8 | 0.0 | 0.00 |
| `KL_aaf_latency_tap_bank` | 675 | -9.1 | 9.9 | 0.1 | 0.00 |
<!-- end table: vivado-opt-blocks -->

**Yosys model**, y = a + b*N + c*C + d*N*C over the six stream and channel points the guards pass:

<!-- table: yosys-stream-total -->
| Measure | Fixed | Per stream | Per channel | Per stream-channel | Points | Residual RMS | Largest residual |
|---|---:|---:|---:|---:|---:|---:|---:|
| LUT | 82,767.4 | 13,881.0 | 401.2 | -99.0 | 6 | 1,227.5 | 2,431.8 |
| FF | 50,785.2 | 3,202.0 | 22.6 | -3.4 | 6 | 81.4 | 161.4 |
| BRAM | 26.1 | 0.8 | 0.0 | -0.0 | 6 | 0.1 | 0.1 |
| DSP | 21.5 | 0.4 | 0.1 | -0.0 | 6 | 0.2 | 0.4 |
<!-- end table: yosys-stream-total -->

<!-- table: yosys-stream-data -->
| Point | N | C | LUT | FF | BRAM | DSP | LUT residual |
|---|---:|---:|---:|---:|---:|---:|---:|
| ship | 1 | 8 | 97,607 | 54,041 | 27.0 | 22 | -1,459 |
| streams-2 | 2 | 8 | 114,587 | 57,477 | 28.0 | 23 | 2,432 |
| streams-4 | 4 | 8 | 137,523 | 63,611 | 29.5 | 23 | -811 |
| chans-2 | 1 | 2 | 97,577 | 54,041 | 27.0 | 22 | 324 |
| chans-4 | 1 | 4 | 97,371 | 54,041 | 27.0 | 22 | -486 |
| streams-4-chans-2 | 4 | 2 | 138,302 | 63,611 | 29.5 | 23 | 0 |
<!-- end table: yosys-stream-data -->

Yosys's per-stream LUT figure is about 3.6 times Vivado's, and its residual shows the growth is not linear: the ACMP talker and the datapath's own logic grow faster than N.
Flip-flops fit the linear model to a residual RMS of 81, and the per-channel and stream-channel terms are within their residuals: channels cost nothing.
The blocks that move most with N in the Yosys model:

<!-- table: yosys-stream-blocks -->
| Block | LUT fixed | LUT per stream | LUT per channel | LUT per N*C | LUT RMS | FF per stream | FF RMS |
|---|---:|---:|---:|---:|---:|---:|---:|
| `KL_pp_shadow` | 48,964 | 7,693.2 | 355.9 | -52.0 | 1,275.5 | 1,428.2 | 53.8 |
| `@own` | 4,311 | 4,849.7 | 123.7 | -58.9 | 240.2 | 824.7 | 0.4 |
| `KL_chan_map_capture` | 828 | 471.2 | -0.2 | 0.0 | 0.8 | 335.6 | 6.4 |
| `KL_avtp_rx_monitor_ctx` | 1,069 | 228.9 | 19.9 | -3.0 | 71.7 | 105.1 | 3.1 |
| `KL_talker_diag_ctx` | 25 | 217.9 | -19.8 | 3.0 | 71.2 | 166.0 | 0.0 |
| `KL_render_setpoint` | 213 | 193.1 | 0.2 | -0.0 | 0.7 | 28.0 | 0.0 |
| `KL_stream_table` | -4 | 93.4 | -1.8 | 0.3 | 6.4 | 69.0 | 0.0 |
| `avtp_stream_parser` | 1,905 | 80.4 | 2.6 | -0.4 | 9.3 | 0.7 | 0.1 |
| `KL_chan_map_render` | 2,454 | -15.0 | -84.6 | 12.8 | 304.1 | 192.0 | 0.0 |
| `milan_csr` | 4,585 | 26.5 | 0.2 | -0.0 | 0.9 | 0.4 | 0.2 |
| `KL_media_clock_restart` | 19 | 17.9 | -0.2 | 0.0 | 0.7 | 10.0 | 0.0 |
| `KL_aaf_packetizer` | 1,379 | 14.2 | 5.7 | -0.8 | 27.7 | 39.9 | 17.4 |
| `KL_pp_maap_shim` | 108 | 4.9 | 0.4 | -0.1 | 1.4 | 1.0 | 0.0 |
| `KL_aaf_clock_meter` | 568 | 3.4 | -0.5 | 0.1 | 1.9 | 0.3 | 0.1 |
<!-- end table: yosys-stream-blocks -->

Only 1x1 can be routed on this device, so the route is the only one this page uses.
The 1x1 route leaves 18 slices free, and one more stream each way adds the Vivado figures above; a slice holds four LUTs and eight flip-flops, so even perfectly packed they need over 1,100 more slices.

### TDM and render slots

<!-- table: tdm-model -->
| Point | Capture slots | LUT | FF | BRAM | DSP |
|---|---:|---:|---:|---:|---:|
| render-0 | 8 | 96,547 | 52,928 | 27.0 | 22 |
| tdm16 | 16 | 96,553 | 52,931 | 27.0 | 22 |
| tdm32 | 32 | 96,554 | 52,934 | 27.0 | 22 |
<!-- end table: tdm-model -->

With the render lane pruned, the capture front end costs the same at 8, 16 and 32 slots, within 7 LUTs and 6 FFs.
The bus width changes counters and the frame position, not the number of stored samples.
The cost is the render lane: `render-0` below removes `KL_tdm_render_master`, 1,060 LUTs and 1,113 FFs in Yosys.
The routed image places that block at 499 LUTs, 623 FFs, 3 RAMB36 and 141.7 slices.
`tdm16` and `tdm32` must prune the render lane: a master render lane is the full bus width, and the crossbar's TDM key lane holds eight slots (`milan_datapath.sv:969-976`).
The stereo I2S front end (`i2s`) is 759 LUTs smaller than TDM8 in Yosys, almost all of it the same render lane.

### Optional blocks and options

Each point below is the shipping point with the changes it names; the figures are the point minus the shipping point.
"LUT x calibration" scales the Yosys LUT change by the whole datapath's Vivado-over-Yosys ratio at the shipping anchor.
"Routed block" is the block itself in the shipping route, where it ships: the most a prune can save before re-placement.

<!-- table: datapath-marginals -->
| Point | Change | LUT | FF | BRAM | DSP | LUT x calibration | Routed block LUT / FF | Blocks that moved most (LUT) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| all-tier1-off | `DPROBES_P`=0, `LTAP_P`=0, `MAAP_P`=0, `MCSERVO_P`=0, `RXFILT_P`=0 | -3,456 | -3,453 | 0 | -1 | -1,545 | - | `KL_aaf_latency_tap_bank/KL_aaf_latency_taps/KL_aaf_latency_chain` -930; `KL_mmcm_drp_servo/@own` -858; `rx_mac_filter/tcam` -678 |
| chans-2 | `TALKER_WIRE_CHANS_P`=2 | -30 | 0 | 0 | 0 | -13 | - | `KL_pp_shadow/protocol_processor_top/KL_aecp_engine` -28; `@own` -15; `KL_aaf_packetizer` +8 |
| chans-4 | `TALKER_WIRE_CHANS_P`=4 | -236 | 0 | 0 | 0 | -105 | - | `@own` -268; `KL_pp_shadow/protocol_processor_top/KL_adp_engine` +18; `KL_aaf_packetizer` +14 |
| i2s | `AUDIO_IF_MASTER_P`=0, `AUDIO_IF_RENDER_SLOTS_P`=0, `AUDIO_IF_SLOTS_P`=0, `TALKER_WIRE_CHANS_P`=2 | -759 | -1,044 | 0 | +1 | -339 | - | `KL_tdm_render_master/@own` -858; `KL_tone_gen` +169; `KL_tdm_render_master/cdc_pair_fifo` -139 |
| no-aaf-meter | rm_ax7101_1x1_tdm8_noaafclk | -685 | -640 | 0 | 0 | -306 | 483 / 630 | `KL_aaf_clock_meter` -570; `@own` -238; `KL_pp_shadow/protocol_processor_top/KL_pp_acmp_listener` +80 |
| no-crf | rm_ax7101_1x1_tdm8_nocrf | -6,552 | -739 | 0 | 0 | -2,928 | - | `KL_pp_shadow/protocol_processor_top/KL_srp_top` -3,232; `KL_pp_shadow/protocol_processor_top/@own` -969; `@own` -928 |
| no-dprobes | `DPROBES_P`=0 | -26 | -74 | 0 | 0 | -12 | - | `@own` -26 |
| no-gptp-plane | `GPTP_PLANE_EN_P`=0 | -11,354 | -7,893 | -4.5 | -4 | -5,074 | 5,004 / 5,899 | `KL_gptp_shadow/KL_gptp_engine/@own` -3,838; `KL_gptp_shadow/KL_gptp_engine/KL_gptp_ucpu` -1,732; `@own` -1,566 |
| no-loopback | `LOOPBACK_P`=0 | -50 | -190 | 0 | 0 | -22 | - | `KL_chan_map_capture` -87; `@own` +38; `KL_mmcm_drp_servo/@own` -1 |
| no-ltap | `LTAP_P`=0 | -943 | -622 | 0 | 0 | -421 | 674 / 621 | `KL_aaf_latency_tap_bank/KL_aaf_latency_taps/KL_aaf_latency_chain` -930; `@own` -53; `KL_pp_shadow/protocol_processor_top/@own` +49 |
| no-maap | `MAAP_P`=0 | -782 | -268 | 0 | 0 | -349 | 479 / 267 | `KL_maap` -595; `@own` -235; `KL_pp_shadow/protocol_processor_top/@own` +49 |
| no-mcservo | `MCSERVO_P`=0 | -858 | -798 | 0 | -1 | -383 | 899 / 814 | `KL_mmcm_drp_servo/@own` -858; `KL_pp_shadow/protocol_processor_top/KL_adp_engine` -72; `KL_crf_rx` +67 |
| no-rxfilt | `RXFILT_P`=0 | -786 | -1,691 | 0 | 0 | -351 | 512 / 1,570 | `rx_mac_filter/tcam` -678; `rx_mac_filter/@own` -123; `KL_pp_shadow/protocol_processor_top/@own` +49 |
| render-0 | `AUDIO_IF_RENDER_SLOTS_P`=0 | -1,060 | -1,113 | 0 | 0 | -474 | 499 / 623 | `KL_tdm_render_master/@own` -858; `KL_tdm_render_master/cdc_pair_fifo` -139; `@own` -110 |
| ship-8x8 | `AUDIO_IF_CLK_HZ_P`=98304000, `AUDIO_IF_RENDER_SLOTS_P`=0, `AUDIO_IF_SLOTS_P`=32, `DPROBES_P`=0, `LOOPBACK_P`=0, `LTAP_P`=0, `N_STREAMS`=8 | +72,659 | +16,774 | +2.5 | 0 | 32,472 | - | `@own` +22,847; `KL_pp_shadow/protocol_processor_top/KL_acmp_talker` +20,212; `KL_pp_shadow/protocol_processor_top/KL_srp_top` +14,271 |
| streams-2 | `N_STREAMS`=2 | +16,980 | +3,436 | +1.0 | +1 | 7,589 | - | `KL_pp_shadow/protocol_processor_top/KL_acmp_talker` +6,390; `@own` +5,046; `KL_pp_shadow/protocol_processor_top/KL_srp_top` +2,210 |
| streams-4 | `N_STREAMS`=4 | +39,916 | +9,570 | +2.5 | +1 | 17,839 | - | `@own` +13,209; `KL_pp_shadow/protocol_processor_top/KL_acmp_talker` +10,722; `KL_pp_shadow/protocol_processor_top/KL_srp_top` +7,773 |
| streams-4-chans-2 | `N_STREAMS`=4, `TALKER_WIRE_CHANS_P`=2 | +40,695 | +9,570 | +2.5 | +1 | 18,187 | - | `@own` +14,028; `KL_pp_shadow/protocol_processor_top/KL_acmp_talker` +10,722; `KL_pp_shadow/protocol_processor_top/KL_srp_top` +7,772 |
| streams-8 (refused by a guard) | `N_STREAMS`=8 | +86,176 | +22,063 | +5.5 | +1 | 38,513 | - | `@own` +30,406; `KL_pp_shadow/protocol_processor_top/KL_acmp_talker` +20,139; `KL_pp_shadow/protocol_processor_top/KL_srp_top` +14,271 |
| streams-8-chans-2 (refused by a guard) | `N_STREAMS`=8, `TALKER_WIRE_CHANS_P`=2 | +87,432 | +22,063 | +5.5 | +1 | 39,075 | - | `@own` +31,950; `KL_pp_shadow/protocol_processor_top/KL_acmp_talker` +19,865; `KL_pp_shadow/protocol_processor_top/KL_srp_top` +14,271 |
| tdm16 | `AUDIO_IF_CLK_HZ_P`=49152000, `AUDIO_IF_RENDER_SLOTS_P`=0, `AUDIO_IF_SLOTS_P`=16 | -1,054 | -1,110 | 0 | 0 | -471 | - | `KL_tdm_render_master/@own` -858; `KL_tdm_render_master/cdc_pair_fifo` -139; `@own` -110 |
| tdm32 | `AUDIO_IF_CLK_HZ_P`=98304000, `AUDIO_IF_RENDER_SLOTS_P`=0, `AUDIO_IF_SLOTS_P`=32 | -1,053 | -1,107 | 0 | 0 | -471 | - | `KL_tdm_render_master/@own` -858; `KL_tdm_render_master/cdc_pair_fifo` -139; `@own` -110 |
| with-i2spb | `I2SPB_P`=1 | +673 | +678 | +1.0 | 0 | 301 | - | `KL_i2s_playback/@own` +440; `@own` +106; `KL_i2s_feed_mux` +83 |
| with-lpf | `LPF_P`=1 | -69 | 0 | 0 | 0 | -31 | - | `@own` -96; `KL_pp_shadow/protocol_processor_top/KL_aecp_engine` +32; `KL_mmcm_drp_servo/@own` -5 |
| with-pps | `PPS_P`=1 | +156 | +294 | 0 | 0 | 70 | - | `timestamp_counter` +117; `@own` +50; `KL_pp_shadow/protocol_processor_top/KL_aecp_engine` -28 |
<!-- end table: datapath-marginals -->

What the table measures, block by block:

- **Channels per stream cost nothing.** From 8 to 2 channels the datapath moves by 30 LUTs at one stream and by 779 at four, inside the stream model's residual, and by no FF at either. The 64-bit datapath carries the channels; only the framer's channel count changes.
- **Latency taps** (`LTAP_P`): 943 LUTs and 622 FFs in Yosys; 674 LUTs, 621 FFs and 190.9 slices routed.
- **RX address filter** (`RXFILT_P`): 786 LUTs and 1,691 FFs in Yosys; 512 LUTs, 1,570 FFs and 247.4 slices routed. Its TCAM is 1,568 of the flip-flops.
- **Media-clock servo** (`MCSERVO_P`): 858 LUTs in Yosys; 899 LUTs, 814 FFs and 236.9 slices routed.
- **MAAP** (`MAAP_P`): 782 LUTs in Yosys; 479 LUTs and 267 FFs routed.
- **AAF clock meter** (no `input_stream` clock source): 685 LUTs and 640 FFs in Yosys; 483 LUTs and 630 FFs routed, the figure PR #634 published.
- **Datapath probes** (`DPROBES_P`) and the **loopback lane** (`LOOPBACK_P`) are small: 26 and 50 LUTs, 74 and 190 FFs.
- **PPS** (`PPS_P`, off in the shipping image) would add 156 LUTs and 294 FFs; **I2S playback** (`I2SPB_P`, off) 673 LUTs, 678 FFs and one BRAM tile.
- **PCM low-pass** (`LPF_P`) adds nothing while I2S playback is pruned: it feeds only that block, and synthesis removes it with its consumer.
- **The fabric gPTP plane** (`GPTP_PLANE_EN_P`) is 11,354 LUTs and 7,893 FFs in Yosys and 5,004 LUTs and 5,899 FFs routed. Its off state is a verification-only elaboration that no product configuration selects.
- **CRF sink and output** (`no-crf`): removing both CRF stream ports removes two processor stream contexts, 6,552 LUTs in Yosys, about 2,900 calibrated. `KL_crf_rx` and `KL_crf_tx` stay: they are instantiated unconditionally.

### Protocol processor parameters

Each processor point is `KL_pp_shadow` at the shipping binding with one parameter changed, mapped hierarchically.
A package or processor-top constant is rewritten in a scratch copy of its one source.
The fit is y = a + b*x over the shipping point and the points that change only that parameter.

<!-- table: processor-parameters -->
| Parameter | Values | LUT per unit | FF per unit | BRAM per unit | LUT residual RMS | Largest LUT residual |
|---|---|---:|---:|---:|---:|---:|
| `DESC_IDX_ENTRIES_P` | 16, 32, 64 | 3.45 | 0.04 | 0.000 | 0.9 | 1.3 |
| `DESC_LINE_BYTES_P` | 576, 768, 1,008 | -0.08 | 0.00 | 0.000 | 73.5 | 103.7 |
| `DESC_NAME_ENTRIES_P` | 39, 64, 128 | 1.72 | 1.00 | 0.010 | 62.0 | 85.0 |
| `N_AUDIO_UNIT_P+N_CLK_DOM_P` | 1, 2, 4 | 107.43 | 57.00 | 0.000 | 154.0 | 213.9 |
| `N_CONTROL_P` | 1, 2, 4 | -44.21 | 9.00 | 0.000 | 121.8 | 169.1 |
| `N_SPORT_IN_P+N_SPORT_OUT_P+N_STREAM_IN_P+N_STREAM_OUT_P` | 1, 2, 4, 8 | 5,885.97 | 1,367.45 | -0.000 | 1,988.8 | 2,759.3 |
| `PP_N_CTRL_C` | 4, 8, 12, 16 | 635.25 | 9.33 | 0.000 | 1,224.0 | 2,037.0 |
| `RX_FIFO_BYTES_P` | 2,048, 4,096, 8,192 | -0.01 | 0.00 | 0.000 | 7.4 | 10.3 |
| `RX_SLOTS_P` | 2, 4, 8 | 215.18 | 79.43 | 0.960 | 181.3 | 251.8 |
| `RX_SLOT_BYTES_P` | 288, 576, 1,152 | 1.16 | 0.08 | 0.010 | 88.9 | 123.4 |
| `TX_STD_SLOTS_P` | 2, 4, 8 | 58.61 | 42.25 | 0.180 | 303.8 | 421.9 |
<!-- end table: processor-parameters -->

- **Stream contexts** dominate. One more stream each way, with its stream ports, adds 5,886 Yosys LUTs and 1,367 FFs, and the residual (RMS 1,989) shows the growth is faster than linear. Most of it is the ACMP talker, which Yosys maps at many times Vivado's size: the portability finding of the [#234 reconciliation](234_PP_SHADOW_AREA_BASELINE.md#yosys-reconciliation). The [Vivado anchors](#streams-and-channels) measure the real per-stream cost.
- **Registered controllers** (`PP_N_CTRL_C`, 16) cost 635 Yosys LUTs each, nearly all in `KL_aecp_notify`: the registry that the [#234 ranking's](234_PP_SHADOW_AREA_BASELINE.md#reduction-ranking) first lever moves to distributed RAM. The residual is large because 12, not a power of two, maps differently. FR-CTRL-03 requires at least 16 controllers, so the count is not a lever; the registry's storage is.
- **Receive slots** cost 215 LUTs, 79 FFs and about one BRAM tile per slot in each pool.
- **Descriptor index entries** cost 3.5 LUTs each. **Name entries** cost about 1.7 LUTs and one FF each, up to the 128 the saved-state backend holds: the name table itself is in block RAM.
- **Payload bounds.** The descriptor line costs nothing measurable across its legal 576 to 1,008 bytes. The receive slot costs about 1.2 LUTs per byte, and 1,152 bytes take three more BRAM tiles. The receive FIFO's byte count costs no logic; 8,192 bytes take one more BRAM tile.
- **Audio units and clock domains** cost about 107 LUTs each; **controls** show no cost above the noise.

The noise floor is the notification block.
`KL_aecp_notify` holds its registry in about 2,000 flip-flops, and its Yosys mapping moves by several hundred LUTs on parameters that do not reach it: `TX_STD_SLOTS_P`=2 moves it by +856.
A per-unit figure under about 100 LUTs is inside that noise.
The marginal of every processor point:

<!-- table: processor-marginals -->
| Point | Change | LUT | FF | BRAM | DSP | LUT x calibration | Routed block LUT / FF | Blocks that moved most (LUT) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| pp-controls-2 | `N_CONTROL_P`=2 | -326 | +9 | 0 | 0 | - | - | `protocol_processor_top/KL_srp_top/KL_srp_talker_fsm` -125; `protocol_processor_top/KL_pp_rx_validator` -113; `protocol_processor_top/KL_adp_engine` -43 |
| pp-controls-4 | `N_CONTROL_P`=4 | -189 | +27 | 0 | 0 | - | - | `protocol_processor_top/KL_srp_top/KL_srp_talker_fsm` -125; `protocol_processor_top/KL_pp_rx_validator` -113; `protocol_processor_top/KL_aecp_engine/KL_aecp_dyn_state` -55 |
| pp-ctrl-12 | `PP_N_CTRL_C`=12 | +728 | -32 | 0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` +1,170; `protocol_processor_top/KL_srp_top/KL_srp_listener_fsm` -204; `protocol_processor_top/@own` -91 |
| pp-ctrl-32 (refused by a guard) | `PP_N_CTRL_C`=32 | +11,922 | +241 | 0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` +11,607; `protocol_processor_top/KL_pp_timer_service` +363; `protocol_processor_top/KL_srp_top/KL_srp_talker_fsm` -271 |
| pp-ctrl-4 | `PP_N_CTRL_C`=4 | -6,818 | -111 | 0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` -7,092; `protocol_processor_top/KL_pp_originator` +219; `protocol_processor_top/KL_acmp_nvm_shadow` +167 |
| pp-ctrl-8 | `PP_N_CTRL_C`=8 | -4,228 | -72 | 0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` -3,826; `protocol_processor_top/KL_srp_top/KL_srp_listener_fsm` -204; `protocol_processor_top/KL_acmp_talker` -105 |
| pp-idx-16 | `DESC_IDX_ENTRIES_P`=16 | -53 | -1 | 0 | 0 | - | - | `protocol_processor_top/KL_pp_rx_validator` -76; `protocol_processor_top/KL_aecp_engine/@own` -55; `protocol_processor_top/KL_acmp_nvm_shadow` +51 |
| pp-idx-64 | `DESC_IDX_ENTRIES_P`=64 | +112 | +1 | 0 | 0 | - | - | `protocol_processor_top/KL_aecp_engine/KL_aecp_desc_store` +80; `protocol_processor_top/KL_acmp_nvm_shadow` +51; `protocol_processor_top/KL_pp_rx_validator` -48 |
| pp-line-1008 | `DESC_LINE_BYTES_P`=1008 | -23 | 0 | 0 | 0 | - | - | `protocol_processor_top/KL_pp_rx_validator` -58; `protocol_processor_top/KL_aecp_engine/@own` -41; `protocol_processor_top/KL_adp_engine` +24 |
| pp-line-1152 (refused by a guard) | `DESC_LINE_BYTES_P`=1152 | +837 | +1 | 0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` +915; `protocol_processor_top/KL_pp_rx_validator` -76; `protocol_processor_top/KL_adp_engine` -33 |
| pp-line-288 (refused by a guard) | `DESC_LINE_BYTES_P`=288 | -20 | +63 | -1.0 | 0 | - | - | `protocol_processor_top/@own` -143; `protocol_processor_top/KL_aecp_engine/KL_aecp_desc_store` +88; `protocol_processor_top/KL_adp_engine` +88 |
| pp-line-512 (refused by a guard) | `DESC_LINE_BYTES_P`=512 | -433 | +64 | -1.0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` -276; `protocol_processor_top/@own` -143; `protocol_processor_top/KL_pp_rx_validator` -76 |
| pp-line-768 | `DESC_LINE_BYTES_P`=768 | +146 | 0 | 0 | 0 | - | - | `protocol_processor_top/KL_adp_engine` +88; `protocol_processor_top/@own` +49; `protocol_processor_top/KL_aecp_engine/KL_aecp_ucpu` +24 |
| pp-names-128 | `DESC_NAME_ENTRIES_P`=128 | +116 | +89 | +1.0 | 0 | - | - | `KL_nvm_backend` +248; `protocol_processor_top/@own` -143; `protocol_processor_top/KL_srp_top/KL_srp_admission` +70 |
| pp-names-235 (refused by a guard) | `DESC_NAME_ENTRIES_P`=235 | +78 | +89 | +3.0 | 0 | - | - | `KL_nvm_backend` +234; `protocol_processor_top/@own` -143; `protocol_processor_top/KL_srp_top/KL_srp_admission` +70 |
| pp-names-64 | `DESC_NAME_ENTRIES_P`=64 | -103 | +25 | 0 | 0 | - | - | `protocol_processor_top/@own` -143; `KL_nvm_backend` +89; `protocol_processor_top/KL_pp_rx_validator` -64 |
| pp-rxbytes-1152 | `RX_SLOT_BYTES_P`=1152 | +834 | +43 | +3.0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` +745; `protocol_processor_top/KL_pp_rx_slots` +84; `protocol_processor_top/KL_adp_engine` +67 |
| pp-rxbytes-288 | `RX_SLOT_BYTES_P`=288 | -129 | -31 | -3.0 | 0 | - | - | `protocol_processor_top/KL_adp_engine` -93; `protocol_processor_top/KL_acmp_talker` +80; `protocol_processor_top/KL_aecp_engine/@own` -31 |
| pp-rxfifo-2048 | `RX_FIFO_BYTES_P`=2048 | -4 | -5 | 0 | 0 | - | - | `axis_fifo` -4 |
| pp-rxfifo-8192 | `RX_FIFO_BYTES_P`=8192 | -40 | +5 | +1.0 | 0 | - | - | `protocol_processor_top/KL_pp_rx_validator` -46; `axis_fifo` +6 |
| pp-rxslots-2 | `RX_SLOTS_P`=2 | -850 | -161 | -3.0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` -602; `protocol_processor_top/KL_pp_rx_slots` -216; `protocol_processor_top/KL_pp_rx_validator` -69 |
| pp-rxslots-8 | `RX_SLOTS_P`=8 | +525 | +316 | +3.0 | 0 | - | - | `protocol_processor_top/KL_pp_rx_slots` +528; `protocol_processor_top/KL_acmp_talker` -51; `protocol_processor_top/KL_pp_rx_validator` -50 |
| pp-si3 | `N_SPORT_IN_P`=2, `N_SPORT_OUT_P`=2, `N_STREAM_IN_P`=3, `N_STREAM_OUT_P`=3 | +10,780 | +1,555 | 0 | 0 | - | - | `protocol_processor_top/KL_acmp_talker` +6,443; `protocol_processor_top/KL_srp_top/KL_srp_talker_fsm` +948; `protocol_processor_top/KL_srp_top/KL_srp_listener_fsm` +881 |
| pp-si5 | `N_SPORT_IN_P`=4, `N_SPORT_OUT_P`=4, `N_STREAM_IN_P`=5, `N_STREAM_OUT_P`=5 | +22,044 | +4,177 | 0 | 0 | - | - | `protocol_processor_top/KL_acmp_talker` +10,572; `protocol_processor_top/KL_srp_top/KL_srp_talker_fsm` +3,258; `protocol_processor_top/KL_srp_top/KL_srp_listener_fsm` +2,604 |
| pp-si9 | `N_SPORT_IN_P`=8, `N_SPORT_OUT_P`=8, `N_STREAM_IN_P`=9, `N_STREAM_OUT_P`=9 | +42,959 | +9,645 | 0 | 0 | - | - | `protocol_processor_top/KL_acmp_talker` +20,248; `protocol_processor_top/KL_srp_top/KL_srp_talker_fsm` +6,957; `protocol_processor_top/KL_srp_top/KL_srp_listener_fsm` +5,642 |
| pp-txslots-2 | `TX_STD_SLOTS_P`=2 | +586 | -97 | 0 | 0 | - | - | `protocol_processor_top/KL_aecp_notify` +856; `protocol_processor_top/KL_pp_tx_slots` -163; `protocol_processor_top/KL_pp_rx_validator` -113 |
| pp-txslots-8 | `TX_STD_SLOTS_P`=8 | +797 | +159 | +1.0 | 0 | - | - | `protocol_processor_top/@own` +499; `protocol_processor_top/KL_pp_tx_slots` +317; `protocol_processor_top/KL_pp_rx_validator` -121 |
| pp-units-2 | `N_AUDIO_UNIT_P`=2, `N_CLK_DOM_P`=2 | -249 | +57 | 0 | 0 | - | - | `protocol_processor_top/KL_srp_top/KL_srp_talker_fsm` -125; `protocol_processor_top/KL_pp_rx_validator` -113; `protocol_processor_top/KL_adp_engine` -43 |
| pp-units-4 | `N_AUDIO_UNIT_P`=4, `N_CLK_DOM_P`=4 | +251 | +171 | 0 | 0 | - | - | `protocol_processor_top/KL_adp_engine` +152; `protocol_processor_top/KL_pp_rx_validator` -113; `protocol_processor_top/@own` -96 |
<!-- end table: processor-marginals -->

### SoC options

`milan_soc.py` accepts one software profile, and it refuses every CPU and cache variant under it.
Each refusal is the measurement: pricing those options needs a change to the build recipe, which this issue does not make.

<!-- table: soc-outcomes -->
| Variant | Changed flags | Outcome | Refusal |
|---|---|---|---|
| axilite | `--bus-standard axi-lite` | accepted | - |
| cpu2 | `--cpu-count 2` | refused | `--software-profile baremetal requires --cpu vexiiriscv --xlen 32 --cpu-count 1` |
| l1-caches | `--scala-args=--with-fetch-l1 --with-lsu-l1` | refused | `--software-profile baremetal requires no FPU, --l2-bytes 0, and no --scala-args overrides` |
| l2-8k | `--l2-bytes 8192` | refused | `--software-profile baremetal requires no FPU, --l2-bytes 0, and no --scala-args overrides` |
| naxriscv | `--cpu naxriscv` | refused | `--software-profile baremetal requires --cpu vexiiriscv --xlen 32 --cpu-count 1` |
| rv64 | `--xlen 64` | refused | `--software-profile baremetal requires --cpu vexiiriscv --xlen 32 --cpu-count 1` |
| rv64-fpu | `--xlen 64`, `--with-fpu` | refused | `--software-profile baremetal requires --cpu vexiiriscv --xlen 32 --cpu-count 1` |
| ship | as shipped | accepted | - |
<!-- end table: soc-outcomes -->

The accepted variants, priced flattened in Yosys:

<!-- table: soc-prices -->
| Variant | Part | LUT | FF | RAMB36 | RAMB18 | DSP |
|---|---|---:|---:|---:|---:|---:|
| axilite | cpu | 4,574 | 5,337 | 0 | 0 | 0 |
| axilite | top | 10,100 | 8,805 | 14 | 3 | 0 |
| ship | cpu | 4,574 | 5,337 | 0 | 0 | 0 |
| ship | top | 9,778 | 8,690 | 14 | 3 | 0 |
<!-- end table: soc-prices -->

The CPU prices the same in both: the bus standard does not reach the core.
AXI-Lite instead of Wishbone adds 322 LUTs and 115 FFs to the SoC top in Yosys, so it is no saving.
Against the route, Yosys reads the CPU at 1.30 times its routed 3,524 LUTs and the SoC top at 2.02 times its routed 4,847.
The CPU's two RAMB36 and five RAMB18 in the route are LUT RAM and flip-flops in Yosys.

### The redundancy second port

The shipping image has one AVB interface on one cabled port; the owner keeps the Milan Section 8 path open (#394).
No RTL parameter builds a second port today, so its cost is measured from what exists, and nothing is recommended.

Under the reading that each AVB interface carries its own MAC, gPTP port engine, time base, receive filter and transmit arbitration, these routed blocks would be replicated:

<!-- table: redundancy-blocks -->
| Routed block | LUT | FF | RAMB36 | RAMB18 | DSP |
|---|---:|---:|---:|---:|---:|
| `KL_gptp_gmii_launch` | 186 | 317 | 0 | 0 | 0 |
| `KL_mac_rmon_events` | 49 | 78 | 0 | 0 | 0 |
| `milan_datapath/g_gptp_plane.u_gptp_shadow` | 5,004 | 5,899 | 3 | 3 | 4 |
| `milan_datapath/g_gptp_plane.gptp_ctl_mux` | 55 | 23 | 0 | 0 | 0 |
| `milan_datapath/g_rx_filter.rx_filter` | 512 | 1,570 | 0 | 0 | 0 |
| `milan_datapath/ts_counter` | 97 | 153 | 0 | 0 | 0 |
| `milan_datapath/ptp_sync` | 297 | 405 | 0 | 0 | 0 |
| `milan_datapath/ptp_clock_validity` | 51 | 125 | 0 | 0 | 0 |
| `milan_datapath/link_guard` | 72 | 114 | 0 | 0 | 0 |
| `milan_datapath/ethernet_counters` | 40 | 449 | 0 | 0 | 0 |
| `milan_datapath/ctl_tx_mux` | 85 | 22 | 0 | 0 | 0 |
| `milan_datapath/ctl_ifg` | 8 | 10 | 0 | 0 | 0 |
| `milan_datapath/adp_tx_mux` | 109 | 24 | 0 | 0 | 0 |
| `milan_datapath/crf_dp_mux` | 34 | 23 | 0 | 0 | 0 |
| `milan_datapath/avtp_rx_parser` | 501 | 706 | 0 | 0 | 0 |
| **sum** | **7,100** | **9,918** | **3** | **3** | **4** |
<!-- end table: redundancy-blocks -->

The sum is 7,100 LUTs and 9,918 FFs, 14.0 percent of the image's LUTs, before the second port's MAC.
That MAC is LiteEth in the SoC top's own logic: 368 flip-flops and 9 I/O-tile flip-flops by name, and LUTs the census cannot attribute.
Inside the processor only the ADP engine has an interface-count parameter, `N_IF_P`:

<!-- table: adp-marginals -->
| Point | Change | LUT | FF | BRAM | DSP | LUT x calibration | Routed block LUT / FF | Blocks that moved most (LUT) |
|---|---|---:|---:|---:|---:|---:|---:|---|
| adp-if-2 | `N_IF_P`=2 | +239 | +76 | 0 | 0 | - | - | `KL_adp_engine` +239 |
| adp-if-4 | `N_IF_P`=4 | +493 | +226 | 0 | 0 | - | - | `KL_adp_engine` +493 |
<!-- end table: adp-marginals -->

The processor's SRP, ACMP and AECP state are not parameterized by interface, so a second interface's cost there is not measured.

## Yosys and Vivado calibration

At each anchor both tools read the same derived sources, the same shape header and the same ROM images.

<!-- table: calibration-totals -->
| Anchor | Measure | Yosys hierarchical | Yosys flattened | Vivado synth | Vivado opt | Opt / hierarchical | Opt / flattened |
|---|---|---:|---:|---:|---:|---:|---:|
| ship | LUT | 97,607 | 108,067 | 44,305 | 43,622 | 0.447 | 0.404 |
| ship | FF | 54,041 | 47,718 | 48,821 | 48,697 | 0.901 | 1.021 |
| ship-8x8 | LUT | 170,266 | 173,181 | 61,439 | 60,454 | 0.355 | 0.349 |
| ship-8x8 | FF | 70,815 | 61,823 | 61,436 | 61,383 | 0.867 | 0.993 |
| streams-2 | LUT | 114,587 | 123,111 | 49,185 | 48,361 | 0.422 | 0.393 |
| streams-2 | FF | 57,477 | 51,127 | 51,622 | 51,521 | 0.896 | 1.008 |
| streams-4 | LUT | 137,523 | 146,016 | 56,238 | 55,288 | 0.402 | 0.379 |
| streams-4 | FF | 63,611 | 57,321 | 57,533 | 57,413 | 0.903 | 1.002 |
<!-- end table: calibration-totals -->

Across the four anchors, Vivado after optimization is 0.36 to 0.45 of the hierarchical Yosys LUT count and 0.35 to 0.40 of the flattened one, falling as the design grows.
Flip-flops are 0.87 to 0.90 of the hierarchical count and 0.99 to 1.02 of the flattened one.
So a flattened Yosys flip-flop count predicts Vivado's within 2 percent, as the Yosys README says, while the LUT ratio itself moves by a quarter between 1x1 and 8x8.
Optimization removes about 1.5 percent of the synthesized LUTs at every anchor.

Per block at the shipping anchor, with the route beside the out-of-context figure:

<!-- table: calibration-blocks -->
| Block | Yosys LUT | Vivado opt LUT | Opt / Yosys LUT | Opt / Yosys FF | Routed LUT | Routed / opt |
|---|---:|---:|---:|---:|---:|---:|
| `KL_pp_shadow` | 57,515 | 25,094 | 0.436 | 0.904 | 23,904 | 0.953 |
| `KL_gptp_shadow` | 9,414 | 5,204 | 0.553 | 0.920 | 5,004 | 0.962 |
| `milan_csr` | 4,612 | 2,893 | 0.627 | 0.616 | 3,073 | 1.062 |
| `KL_chan_map_capture` | 1,299 | 1,080 | 0.831 | 0.954 | 1,079 | 0.999 |
| `KL_avtp_rx_monitor_ctx` | 1,345 | 1,011 | 0.752 | 1.240 | 889 | 0.879 |
| `KL_mmcm_drp_servo` | 865 | 912 | 1.054 | 1.028 | 899 | 0.986 |
| `KL_aaf_latency_tap_bank` | 938 | 675 | 0.720 | 1.000 | 674 | 0.999 |
| `KL_aaf_packetizer` | 1,396 | 655 | 0.469 | 0.974 | 622 | 0.950 |
| `KL_aaf_clock_meter` | 570 | 534 | 0.937 | 0.992 | 483 | 0.904 |
| `avtp_stream_parser` | 1,991 | 519 | 0.261 | 0.844 | 501 | 0.965 |
| `rx_mac_filter` | 801 | 513 | 0.640 | 0.928 | 512 | 0.998 |
| `KL_maap` | 595 | 507 | 0.852 | 0.996 | 479 | 0.945 |
| `KL_tdm_render_master` | 997 | 507 | 0.509 | 0.576 | 499 | 0.984 |
| `KL_media_grid_align` | 310 | 383 | 1.235 | 1.000 | 373 | 0.974 |
| `KL_render_setpoint` | 407 | 380 | 0.934 | 0.851 | 381 | 1.003 |
| `KL_crf_tx` | 443 | 322 | 0.727 | 1.000 | 317 | 0.984 |
| `ptp_csr_sync` | 8 | 307 | 38.375 | 1.000 | 297 | 0.967 |
| `KL_crf_rx` | 370 | 300 | 0.811 | 0.996 | 267 | 0.890 |
| `KL_aaf_rx_depacketizer` | 268 | 297 | 1.108 | 0.548 | 273 | 0.919 |
| `adp_tx_arbiter` | 356 | 283 | 0.795 | 1.000 | 283 | 1.000 |
| `KL_talker_diag_ctx` | 196 | 281 | 1.434 | 1.000 | 225 | 0.801 |
| `@own` | 9,458 | 230 | 0.024 | 0.906 | 563 | 2.448 |
| `KL_media_nco` | 107 | 131 | 1.224 | 1.000 | 130 | 0.992 |
| `KL_chan_map_render` | 2,238 | 119 | 0.053 | 0.893 | 112 | 0.941 |
| `timestamp_counter` | 368 | 97 | 0.264 | 1.000 | 97 | 1.000 |
| `KL_tdm_capture_master` | 91 | 78 | 0.857 | 0.988 | 75 | 0.962 |
| `ethernet_events` | 94 | 73 | 0.777 | 1.997 | 40 | 0.548 |
| `KL_link_guard` | 101 | 68 | 0.673 | 1.018 | 72 | 1.059 |
| `KL_tone_gen` | 150 | 62 | 0.413 | 1.000 | 38 | 0.613 |
| `KL_stream_table` | 85 | 58 | 0.682 | 1.000 | 58 | 1.000 |
| `KL_ptp_clock_validity` | 52 | 32 | 0.615 | 1.000 | 51 | 1.594 |
| `KL_media_clock_restart` | 36 | 23 | 0.639 | 1.000 | 20 | 0.870 |
| `KL_pp_maap_shim` | 114 | 9 | 0.079 | 0.422 | 9 | 1.000 |
| `tx_ifg_gasket` | 15 | 8 | 0.533 | 1.000 | 8 | 1.000 |
| `KL_pcm_route` | 2 | 2 | 1.000 | 1.000 | 2 | 1.000 |
<!-- end table: calibration-blocks -->

Per block, Vivado-after-optimization over Yosys spans more than two orders of magnitude.
Several blocks differ by a factor of four or more; two kinds are explained, and the others (`KL_chan_map_render`, `avtp_stream_parser`, `KL_pp_maap_shim`) are not explained here:

- `@own`, the datapath's own logic: Yosys keeps the logic sv2v flattens out of interfaces and generate blocks in the top's own module, where Vivado's rebuilt hierarchy moves it into children or removes it.
- `ptp_csr_sync` and the like: Yosys leaves inverters as `INV` cells, which the `ooc.sh` columns do not count, so a block of inverters and flops reads as almost no LUT.

The route over the out-of-context optimized figure lies between 0.88 and 1.06 for every block above 1,000 LUTs, and is 0.967 for the whole datapath (42,200 against 43,622).
So the out-of-context anchor predicts the routed image's blocks well, and a Yosys figure does not.
A Yosys LUT change is a direction and an order of magnitude; a decision needs the Vivado anchor or the route.

## Ranked opportunities

The ranking orders where the area is against what removing it would cost in function.
Costs are measured: the routed block, or a sweep point.
A saving is an estimate until a matched before-and-after route measures it, and no slice saving is claimed: only a route measures slices.
Nothing here is applied; each opportunity belongs to its own issue.

The gap is NFR-RES-01's: the image is 12,727 LUTs over 60 percent of the device ([area budget](../design/AREA_BUDGET.md#headroom-target)).
Placement binds before LUTs do: 18 slices are free.

| Rank | Opportunity | Where | Measured cost | Estimated saving | Cost in function |
|---:|---|---|---|---|---|
| 1 | The protocol processor's redesign and its ranked levers | `pp_shadow`, #640; levers #232, #230, #639 | 23,904 LUT, 24,265 FF, 7,121.8 slices: 47.1 percent of the image | about 3,600 LUT and 5,600 FF for levers 1 to 5 ([#234 ranking](234_PP_SHADOW_AREA_BASELINE.md#reduction-ranking)); the registry those levers start with scales by 635 Yosys LUT per controller | none intended: the levers change storage, not protocol behaviour |
| 2 | The CSR block's structure | `csr` (`milan_csr`) | 3,073 LUT, 2,141 FF, 703.5 slices; 211 LUT more per stream out of context | not estimated: it needs a design | none intended if the register map stays; a restructured read path may add read latency |
| 3 | One microcontroller instead of two | the gPTP plane's `u_engine/u_ucpu` (2,088 LUT) and the AECP's `u_aecp/u_ucpu` (1,716 LUT) | 3,804 LUT for the two | at most the smaller one's 1,716 LUT, not estimated | the gPTP sequences are time-critical and the AECP ones are not; sharing one engine would schedule both, which needs its own timing proof |
| 4 | Prune the RX address filter | `RXFILT_P`, `board.features.rx_mac_filter` | 512 LUT, 1,570 FF, 247.4 slices routed; 786 LUT and 1,691 FF in Yosys | up to the routed block | no hardware station-address filter; the supported receive policy is promiscuous with or without it, and the `TCAM_*` words lose their consumer ([Tier 1](../design/AREA_BUDGET.md#tier-1---implemented-optional-fabric-blocks)) |
| 5 | Prune the latency taps | `LTAP_P`, `board.features.latency_taps` | 674 LUT, 621 FF, 190.9 slices routed | up to the routed block | the LTAP window reads zero, and the AAF latency-tap silicon figures cannot be repeated on that image; the shipping configuration keeps the taps on purpose |
| 6 | Prune the loopback lane and the datapath probes | `LOOPBACK_P`, `DPROBES_P` | 76 LUT and 264 FF in Yosys | about 35 LUT | the eight loopback clusters become model-only; the APRB and PBK diagnostics read zero |

Not recommended: each would remove a function the product ships.

| Block | Measured cost | Function it carries |
|---|---|---|
| The TDM render lane (`AUDIO_IF_RENDER_SLOTS_P`) | 499 LUT, 623 FF, 3 RAMB36, 141.7 slices routed | the TDM8 output on J11.5 |
| The CRF sink and output | about 2,900 LUT (6,552 in Yosys): two processor stream contexts | the CRF Media Clock Input and Output stream ports |
| The AAF clock meter | 483 LUT, 630 FF, 153.3 slices routed | following an AAF stream's media clock (#629) |
| The media-clock servo (`MCSERVO_P`) | 899 LUT, 814 FF, 236.9 slices routed | the actuator of CRF and AAF media-clock following |
| MAAP (`MAAP_P`) | 479 LUT, 267 FF routed | dynamic stream addresses; the builder requires it for every declared talker |
| The fabric gPTP plane | 5,004 LUT, 5,899 FF, 1,571.4 slices routed | the product's time-sync owner |
| Fewer registered controllers | 635 Yosys LUT each | FR-CTRL-03 requires at least 16 |

Not levers, measured:

- Channels per stream, the TDM capture slot count, the receive FIFO's bytes and the descriptor name entries cost nothing, or a few LUTs per unit.
- Every CPU and cache option is refused by the recipe; the one accepted SoC bus option costs more, not less.

Ranks 4 to 6 together are about 1,200 routed LUTs, a tenth of the gap.
The gap is where the map puts the area: the processor (47 percent), the gPTP plane and the CSR block (16 percent together).
One more stream each way costs 4,739 LUTs out of context, far more than the device has left, so every shape above 1x1 waits on that redesign.

## Run receipts

Every run was started in the foreground of its own runner, without a pipeline, on 2026-10-04.
Each Vivado run held the host's shared Vivado lock and was this lane's only Vivado; other lanes' runs shared the host.
Minutes count only the time under the lock.
The route itself is PR #638's: its receipts are in the [#234 findings](234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-10-03-after-pr-634).

| Run | rc | Minutes under the lock | Log | Log SHA-256, first 16 | Log bytes |
|---|---:|---:|---|---|---:|
| Route reopen, first attempt, stopped by this lane | 143 | 4.0 | `route_map.log` | `70e1dc88fd63eeb8` | 6,740 |
| Route reopen | 0 | 0.6 | `route_map.log` | `4ea7f6275a4587bc` | 6,847 |
| Anchor 1x1, shipping shape | 0 | 18.9 | `ooc.log` | `b42c9ec112cfa29f` | 344,150 |
| Anchor 8x8, tracked configuration | 0 | 29.1 | `ooc.log` | `b85aa07b33221025` | 341,175 |
| Anchor 2x2 | 0 | 20.3 | `ooc.log` | `522655f46cfc6954` | 345,731 |
| Anchor 4x4 | 0 | 22.2 | `ooc.log` | `3a40bae068e72c76` | 347,730 |
| Anchor 8x8 TDM8, refused in synthesis | 1 | 0.2 | `ooc.log` | `9c2ac5ce68776d0d` | 75,199 |

The first reopen wrote its census one line at a time through indexed list access, about 67 lines a second; it was stopped after 4 minutes to free the lock, and `route_map.tcl` now iterates the lists in parallel.
The refused anchor stopped in synthesis on the guard named in [the refusals](#guard-refusals).

The 59 Yosys points, every one with sv2v and Yosys rc 0, 247.9 minutes of mapping in all, two at a time.
Each point's guard lint ran Verilator 5.050 with rc 0; "refused" marks a guard that fired.

| Point | Top | rc | Seconds | `stat.json` SHA-256, first 16 | Guard |
|---|---|---:|---:|---|---|
| adp-if-1 | `KL_adp_engine` | 0 | 12.7 | `384297c10a588f3f` | clean |
| adp-if-2 | `KL_adp_engine` | 0 | 13.8 | `6fd3b4d6a764229c` | clean |
| adp-if-4 | `KL_adp_engine` | 0 | 13.6 | `4b157fd0917200dd` | clean |
| all-tier1-off | `milan_datapath` | 0 | 207.3 | `ae40712051539b02` | clean |
| chans-2 | `milan_datapath` | 0 | 228.2 | `bfafec9c0f7c4bdb` | clean |
| chans-4 | `milan_datapath` | 0 | 225.7 | `0db9e76693d2a14c` | clean |
| i2s | `milan_datapath` | 0 | 249.6 | `9861e1aab979d480` | clean |
| no-aaf-meter | `milan_datapath` | 0 | 246.8 | `bbf0b769c1d71ff9` | clean |
| no-crf | `milan_datapath` | 0 | 224.3 | `d13834bf72cf1099` | clean |
| no-dprobes | `milan_datapath` | 0 | 222.8 | `fffc8808bbf7dc53` | clean |
| no-gptp-plane | `milan_datapath` | 0 | 251.6 | `4d38aec36782321b` | clean |
| no-loopback | `milan_datapath` | 0 | 218.2 | `13dae08cada65e54` | clean |
| no-ltap | `milan_datapath` | 0 | 243.1 | `0e3989c8e409c951` | clean |
| no-maap | `milan_datapath` | 0 | 218.1 | `84e42a6122061c32` | clean |
| no-mcservo | `milan_datapath` | 0 | 244.7 | `62aee914a79ad10e` | clean |
| no-rxfilt | `milan_datapath` | 0 | 222.3 | `6ed5643049e9a34d` | clean |
| pp-controls-2 | `KL_pp_shadow` | 0 | 107.5 | `9660174318f92620` | clean |
| pp-controls-4 | `KL_pp_shadow` | 0 | 114.6 | `35237c6f87a1e5b1` | clean |
| pp-ctrl-12 | `KL_pp_shadow` | 0 | 102.4 | `181f71e2da27ff68` | clean |
| pp-ctrl-32 | `KL_pp_shadow` | 0 | 127.4 | `c67deed95c109ce7` | refused |
| pp-ctrl-4 | `KL_pp_shadow` | 0 | 112.8 | `ada6dcd5bba4e597` | clean |
| pp-ctrl-8 | `KL_pp_shadow` | 0 | 116.6 | `14028a790c6a4d68` | clean |
| pp-idx-16 | `KL_pp_shadow` | 0 | 114.6 | `74a744d6e78d71eb` | clean |
| pp-idx-64 | `KL_pp_shadow` | 0 | 108.5 | `90a3b7dc5ec74f4d` | clean |
| pp-line-1008 | `KL_pp_shadow` | 0 | 103.0 | `17d6f89cfbe71fb2` | clean |
| pp-line-1152 | `KL_pp_shadow` | 0 | 106.0 | `93a6f830d627bee9` | refused |
| pp-line-288 | `KL_pp_shadow` | 0 | 107.2 | `7db336888d7c02f1` | refused |
| pp-line-512 | `KL_pp_shadow` | 0 | 106.6 | `52a0efd550f19bb2` | refused |
| pp-line-768 | `KL_pp_shadow` | 0 | 105.5 | `3c12c00467628a28` | clean |
| pp-names-128 | `KL_pp_shadow` | 0 | 123.3 | `b70e8dccdc18e6bb` | clean |
| pp-names-235 | `KL_pp_shadow` | 0 | 122.4 | `cb81a2474516e2b9` | refused |
| pp-names-64 | `KL_pp_shadow` | 0 | 124.7 | `e86b1a1240781d32` | clean |
| pp-rxbytes-1152 | `KL_pp_shadow` | 0 | 104.1 | `d7d996b9c0bb62f5` | clean |
| pp-rxbytes-288 | `KL_pp_shadow` | 0 | 103.3 | `5c8c37ea46fdf246` | clean |
| pp-rxfifo-2048 | `KL_pp_shadow` | 0 | 107.3 | `e3c63696d45d9b8c` | clean |
| pp-rxfifo-8192 | `KL_pp_shadow` | 0 | 105.7 | `86a558514be948ab` | clean |
| pp-rxslots-2 | `KL_pp_shadow` | 0 | 113.2 | `6cd6aa28cc1da695` | clean |
| pp-rxslots-8 | `KL_pp_shadow` | 0 | 106.1 | `a6ab00f3e72e9e24` | clean |
| pp-ship | `KL_pp_shadow` | 0 | 112.4 | `d5922f2c67227c84` | clean |
| pp-si3 | `KL_pp_shadow` | 0 | 125.0 | `ed32c2dce4bd977c` | clean |
| pp-si5 | `KL_pp_shadow` | 0 | 152.9 | `07b97e994edafbd9` | clean |
| pp-si9 | `KL_pp_shadow` | 0 | 203.6 | `ac62da5a56bc3789` | clean |
| pp-txslots-2 | `KL_pp_shadow` | 0 | 102.5 | `fee7436057d4f054` | clean |
| pp-txslots-8 | `KL_pp_shadow` | 0 | 103.6 | `1ac922981334d267` | clean |
| pp-units-2 | `KL_pp_shadow` | 0 | 105.4 | `f2501adb4c7e90d0` | clean |
| pp-units-4 | `KL_pp_shadow` | 0 | 106.2 | `d59eb137c16238de` | clean |
| render-0 | `milan_datapath` | 0 | 216.9 | `27a299d26fb4748a` | clean |
| ship | `milan_datapath` | 0 | 632.2 | `57e1f262f71f54bd` | clean |
| ship-8x8 | `milan_datapath` | 0 | 1234.7 | `571cf20b5067d11c` | clean |
| streams-2 | `milan_datapath` | 0 | 736.4 | `664bffff10071534` | clean |
| streams-4 | `milan_datapath` | 0 | 1020.5 | `421179373b882e6a` | clean |
| streams-4-chans-2 | `milan_datapath` | 0 | 371.4 | `f3b9b36047519dc0` | clean |
| streams-8 | `milan_datapath` | 0 | 2127.7 | `2bf1431e04838840` | refused |
| streams-8-chans-2 | `milan_datapath` | 0 | 788.1 | `9727a53a55f2e904` | refused |
| tdm16 | `milan_datapath` | 0 | 243.7 | `5cc44c2e45aec766` | clean |
| tdm32 | `milan_datapath` | 0 | 253.8 | `2d81a8a255013ec6` | clean |
| with-i2spb | `milan_datapath` | 0 | 285.6 | `5ec66216f503d59a` | clean |
| with-lpf | `milan_datapath` | 0 | 225.7 | `c2782a33e1caf470` | clean |
| with-pps | `milan_datapath` | 0 | 238.9 | `d0dfbb64dbeeb1b6` | clean |

The executor's packet holds every digest in full: each report, census, point receipt, ROM image, shape header and SoC export log.
