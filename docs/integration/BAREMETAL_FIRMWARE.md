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
- `board.features.fabric_gptp` is true and a `gptp:` section is present. The
  builder emits `--fabric-gptp` and generates `gptp_ucode.hex` from that same
  configuration's station MAC, priority1 and 100 MHz Milan clock.

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
and DRAM destination as generated constants. At boot it performs this order:

1. Keep ADP and the protocol processor disabled.
2. Program the generated entity ID, model ID, station MAC, SR VID, stream
   counts, lwSRP policy, MAAP count and CRF/AAF controls.
3. Copy the raw AEM image from QSPI to the protocol processor's paired DRAM
   window and verify its CRC32.
4. Enable the PTP clock, protocol processor and ADP entity only after the
   identity check and AEM verification succeed.

A missing or corrupt image leaves the entity disabled. The UART status line
then reports `AEM=disabled`; it is not treated as a quiet healthy boot.

## Fabric gPTP option

`board.features.fabric_gptp` defaults to `false`; the shipping AX7101 YAML
sets it to `true`. An option-on build elaborates `KL_gptp_shadow` with
`GPTP_PLANE_EN_P=1` and passes an absolute path to the builder-generated
microcode image. A missing `gptp:` section is rejected instead of silently
using the generator's example identity or clock defaults.

This #120 integration does not change the RTL default or the CSR compatibility
surface. The #116 flip still owns the default-on transition and retirement of
the remaining software-era CSR/readback behavior. The bare-metal firmware
sets the PHC epoch explicitly; after that, the fabric plane owns adjfine and
adjtime in an option-on build.

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

The final table is populated from the winning AX7101
`ExtraPostPlacementOpt` / `AltSpreadLogic_high` / `ExtraTimingOpt` sweep before
the change is merged. It records Slice LUTs, Slice registers, BRAM, DSP, slices,
WNS and TNS together with the winning directive and build tag.
