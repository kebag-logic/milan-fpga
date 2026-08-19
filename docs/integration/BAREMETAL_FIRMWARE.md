# Bare-metal AX7101 firmware profile

The shipping AX7101 profile uses one RV32I VexiiRiscv hart in machine mode,
with no supervisor mode, MMU, Linux, FPU, L1 cache, L2 cache or LiteX SDRAM
cache. It explicitly enables the fabric gPTP plane bought by #114; the RTL
parameter still defaults off so other configurations do not change shape by
accident. Linux remains a supported bring-up profile for the Arty and AX7101
8x8 configurations.

The capability rows on this page are checked against the
[Milan feature status ledger](../reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `soc.baremetal-profile` | `implemented` | - |
| `host.sound-card-option` | `implemented` | - |
<!-- milan-feature-status:end -->

## Contents

- **[Build contract](#build-contract)** — The checked shipping shape, its cacheless one-hart RV32I invariants, the 50 MHz Milan/CPU clock boundary and the configuration-owned gPTP ROM.
- **[Boot and AEM image](#boot-and-aem-image)** — The raw QSPI descriptor-image slot and the identity, copy and CRC checks that must pass before the protocol processor and ADP are enabled.
- **[Fabric gPTP option](#fabric-gptp-option)** — How the shipping YAML opts into the fabric plane without changing the RTL default or taking #116's software-retirement work.
- **[UART commands](#uart-commands)** — The status, TAI set/get and explicit UTC conversion commands, followed by the non-disruptive host smoke invocation.
- **[Optional Linux sound-card surface](#optional-linux-sound-card-surface)** — What the shipping build removes with `sound_card: false`, what audio fabric remains, and how retained Linux bring-up builds opt back in.
- **[Verification gates](#verification-gates)** — The mandatory local bar, complete three-directive Vivado cell, timing-clean winner and measured resource buy-back that fund the fabric gPTP plane.

## Build contract

The authoritative product shape is
[`configs/endstation_ax7101_1x1_tdm8.yaml`](../../configs/endstation_ax7101_1x1_tdm8.yaml).
The builder and `milan_soc.py` both reject a bare-metal profile unless all of
these statements hold:

- CPU is VexiiRiscv, XLEN is 32, and `cpu_count` is one.
- `l2_bytes` is zero, no FPU is selected, and no cache or prefetch Scala
  arguments are present.
- `flashboot` is `baremetal` or `none`; the `baremetal` manifest cannot be
  selected under the Linux profile.
- The Vexii netlist ISA is RV32I plus `zicsr` and `zifencei`. Machine mode is
  the only privilege level and the CPU has no MMU.
- The cacheless CPU side and the 64-bit Milan plane run at 50 MHz. Vexii's
  supported decoupled-clock boundary crosses CPU traffic back into the 100 MHz
  LiteX system fabric; the system/audio clock recipe therefore stays unchanged.
- `board.features.fabric_gptp` is true and a `gptp:` section is present. The
  builder emits `--fabric-gptp` and generates `gptp_ucode.hex` from that same
  configuration's station MAC, priority1 and 50 MHz Milan clock.

Build through the checked configuration entry point:

```console
sw/litex/build.sh ax7101
```

For an elaboration-only check, first generate the configuration artifacts,
then pass the emitted `soc_params.json` arguments to `milan_soc.py` without
`--build`. `sw/builder/test_builder.py` checks the generated command against
the named build and sweep recipes.

## Boot and AEM image

Firmware is linked into the LiteX ROM. The only mutable boot artifact is the
builder-generated protocol-processor entity image:

| QSPI slot | Offset | Budget | Format | Consumer |
|---|---:|---:|---|---|
| bitstream | `0x000000` | 4 MiB | raw FPGA configuration | FPGA configuration logic |
| AEM image | `0x400000` | 64 KiB | raw `aem_desc.bin` beginning with `AEMI` | bare-metal firmware |

`deploy.sh flash-images` writes the AEM image raw. It must not receive a
LiteX FBI header. At build time the firmware receives the image length, CRC32
and DRAM destination as generated constants. The PHC is enabled by the CSR
reset and the option-on fabric gPTP plane starts independently of the AVDECC
AEM image. Firmware therefore does not gate either one on AEM verification.
It performs this order:

1. Keep ADP and the protocol processor disabled while the PHC and fabric gPTP
   plane remain active.
2. Program the generated entity ID, model ID, station MAC, SR VID, stream
   counts, lwSRP policy, MAAP count and CRF/AAF controls.
3. Copy the raw AEM image from QSPI to the protocol processor's paired DRAM
   window and verify its CRC32.
4. Enable the protocol processor and then the ADP entity only after the
   identity check and AEM verification succeed.

A missing or corrupt image leaves the AVDECC entity disabled while the PHC and
fabric gPTP plane continue independently. The UART status line then reports
`AEM=disabled`; it is not treated as a quiet healthy boot.

## Fabric gPTP option

`board.features.fabric_gptp` defaults to `false`; the shipping AX7101 YAML
sets it to `true`. An option-on build elaborates `KL_gptp_shadow` with
`GPTP_PLANE_EN_P=1` and passes an absolute path to the builder-generated
microcode image. A missing `gptp:` section is rejected instead of silently
using the generator's example identity or clock defaults.

This #120 integration does not change the RTL default or the CSR compatibility
surface. The #116 flip still owns the default-on transition and retirement of
the remaining software-era CSR/readback behavior. The bare-metal firmware
exposes explicit UART commands for setting the PHC epoch; the fabric plane
owns adjfine and adjtime in an option-on build. When an external grandmaster
is selected, that plane steps and disciplines the PHC; a free-running or
grandmaster board uses `milan_settime` or `milan_utc` to establish its TAI
epoch.

## UART commands

The LiteX BIOS console stays at 115200 baud and provides:

| Command | Effect |
|---|---|
| `milan_status` | Read the Milan CSR identity, PTP/ADP/processor controls, processor status, AEM state and current TAI nanoseconds. |
| `milan_gettime` | Snapshot and print the fabric PHC as `TAI_NS=0x...`. |
| `milan_settime <tai-seconds> [nanoseconds]` | Set the PHC from explicit TAI seconds. Overflow and nanoseconds outside `0..999999999` are refused. |
| `milan_utc <utc-seconds> <nanoseconds> <tai-minus-utc>` | Convert an explicit UTC value and TAI-UTC offset to TAI before setting the PHC. |

The firmware does not embed a leap-second table. The operator or controller
must provide the current TAI-UTC offset to `milan_utc`.

Run the post-flash test from the host connected to the console:

```console
MILAN_PROFILE=baremetal MILAN_UART=/dev/serial/by-id/<adapter> \
  scripts/hostplane_smoke.sh
```

It checks the CSR magic, paired AEM image, enable bits and PHC progression.
It does not set the clock, so a smoke run cannot disturb an established time.

## Optional Linux sound-card surface

`board.features.sound_card` defaults to `false`. When false, generation omits
the PCM DMA master, its LiteX CSR window, the device-tree PCM node, the
reserved capture ring, playback rings and host-role AEM clusters. The receive
AVTP parser/depacketizer, physical audio capture, AAF packetizer, channel maps,
loopback sources and render path remain fabric functions.

Linux bring-up configurations that need ALSA set `sound_card: true` and emit
`--sound-card`. `--aaf-playback` is valid only with that option. For a Linux
build that intentionally omits ALSA, run the existing smoke with
`SOUND_CARD=0`; the ALSA check is explicitly skipped while NIC, timestamp and
protocol-processor checks still run.

## Verification gates

Before a bitstream is accepted, run the builder tests, Verilator suites,
behavior tests, Yosys portability sweep, clean-tree documentation gates and
the three place-directive AX7101 sweep required by
[`CONTRIBUTING.md`](../../CONTRIBUTING.md). The placed-resource and timing
record below is the shipping option-on measurement; an elaboration estimate
is not accepted as a substitute.

### Placed-and-routed shipping record

The measured cell is commit `1e80a106`, configuration
`configs/endstation_ax7101_1x1_tdm8.yaml`, part `xc7a100t-fgg484-2`, Vivado
2026.1 and sweep tag `i120gptp50`. It uses 32 threads, no explicit placer seed
(the Vivado default), `AreaOptimized_high` synthesis, `ExploreArea`
optimization, `AggressiveExplore` physical optimization and routing, and the
three place directives below. The 100 MHz system/audio clocks and the 50 MHz
Milan/cacheless-CPU clock are asynchronous by construction.

| Place directive | Slice LUTs | Slice registers | BRAM tiles | DSP | Slices | WNS (ns) | TNS (ns) | WHS (ns) | Result |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `ExtraPostPlacementOpt` | 54,305 | 57,938 | 100 | 15 | 15,849 | +0.033 | 0.000 | +0.049 | timing met; bitstream |
| `AltSpreadLogic_high` | 54,299 | 57,939 | 100 | 15 | 15,850 | -0.029 | -0.289 | +0.013 | setup failed; bitstream |
| `ExtraTimingOpt` | 54,284 | 57,939 | 100 | 15 | 15,850 | -0.051 | -0.220 | +0.047 | setup failed; bitstream |

`ExtraPostPlacementOpt` is the shipping winner. Its bitstream is
`build_ax7101_eppo_i120gptp50/gateware/alinx_ax7101.bit`; the signed-off report
has zero setup and hold failing endpoints. The placed design occupies 15,849
of 15,850 slices, so the directive is part of the reproducible cell and is not
interchangeable with the two failing alternatives.

The first option-on experiment kept both the system and Milan planes at
100 MHz. It emitted bitstreams but did not meet setup timing:

| Place directive | WNS (ns) | TNS (ns) | WHS (ns) |
|---|---:|---:|---:|
| `AltSpreadLogic_high` | -3.933 | -11,973.169 | +0.036 |
| `ExtraTimingOpt` | -3.897 | -9,278.585 | +0.057 |
| `ExtraPostPlacementOpt` | -3.762 | -12,239.650 | +0.020 |

That result is why the cacheless CPU and 64-bit Milan plane run at 50 MHz;
3.2 Gb/s still exceeds the 1 Gb/s wire rate while the LiteX system and audio
recipe remain at 100 MHz.

Post-synthesis resource accounting also proves the intended buy-back. The
#114 Linux, plane-off baseline used 59,497 LUT, 63,092 registers, 126 BRAM
tiles and 15 DSP. The fabric gPTP plane in this build accounts for 3,364 LUT,
2,939 registers, 4.5 BRAM tiles and 4 DSP. Adding that plane to the old
baseline would require 62,861 LUT, 66,031 registers, 130.5 BRAM tiles and 19
DSP; the new option-on bare-metal build instead uses 57,111 LUT, 58,043
registers, 100 BRAM tiles and 15 DSP. The downgrade therefore funds the plane
and still frees 5,750 LUT, 7,988 registers, 30.5 BRAM tiles and 4 DSP relative
to that old-plus-plane comparison.
