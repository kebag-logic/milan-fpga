# `sw/` — build the bare-metal Milan SoC

The product is one cacheless RV32I VexiiRiscv hart in machine mode, with the
Milan TSN datapath memory-mapped at `0x9000_0000`. Fabric owns gPTP and the
bare-metal firmware owns startup, identity activation, diagnostics, and the
remaining software-visible policy.

The persistent image pair is:

```
end-station YAML ──▶ bitstream
        │
        └──────────▶ aem_desc.bin
```

`sw/litex/deploy.sh flash-pair` validates and writes the AEM image first and
commits the paired bitstream last.

## Contents

- **[Main entry points](#main-entry-points)** — The builder, SoC, build, sweep, and simulation commands that own the product flow.
- **[Build](#build)** — How to apply the pinned toolchain patches and invoke each supported board recipe.
- **[Validate](#validate)** — The builder, policy, simulation, and portability gates required before integration.

## Main entry points

| Path | Purpose |
|---|---|
| [`builder/endstation_builder.py`](builder/endstation_builder.py) | Validate an end-station YAML file and generate the SoC arguments, descriptor image, firmware-visible platform shape, and build plan. |
| [`litex/milan_soc.py`](litex/milan_soc.py) | Elaborate the board SoC and export the gateware and firmware artifacts. |
| [`litex/build.sh`](litex/build.sh) | Build a named product configuration or invoke the paired flash transaction. |
| [`litex/sweep.sh`](litex/sweep.sh) | Run the supported board/configuration synthesis sweep. |
| [`litex/milan_sim.py`](litex/milan_sim.py) | Exercise the SoC integration in simulation. |

## Build

Install the pinned toolchain described in
[`docs/litex/LITEX_SOC.md`](../docs/litex/LITEX_SOC.md), apply the local LiteX
patch series, then inspect or run a named build:

```sh
sw/litex/patches/apply.sh
sw/litex/build.sh ax7101 --dry-run
sw/litex/build.sh ax7101
sw/litex/build.sh ax8x8
sw/litex/build.sh arty
```

All named recipes emit the RV32I bare-metal profile. The fabric-off form is a
direct, verification-only elaboration and is never a build or flash recipe.

## Validate

```sh
python3 sw/builder/test_builder.py --require-elaboration
python3 scripts/check_baremetal_only.py --check
scripts/run_all_suites.sh "$(mktemp -d)"
syn/yosys/run.sh
```

See [`docs/integration/BAREMETAL_FIRMWARE.md`](../docs/integration/BAREMETAL_FIRMWARE.md)
for the UART and startup contract and
[`docs/testing/TESTING.md`](../docs/testing/TESTING.md) for the complete test
matrix.
