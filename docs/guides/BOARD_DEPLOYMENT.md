# Board deployment guide

Use this path to install an AX7101 board.

## Contents

- **[Check what you need](#check-what-you-need)** -- Hardware and a PC.
- **[Choose your path](#choose-your-path)** -- Flash or build first.
- **[Set the board identity](#set-the-board-identity)** -- Per-board fields.
- **[Install the build tools](#install-the-build-tools)** -- Pinned LiteX and Vivado.
- **[Build an image set](#build-an-image-set)** -- One build per board.
- **[Flash a new board](#flash-a-new-board)** -- The first install.
- **[Update a flashed board](#update-a-flashed-board)** -- Replace a known build.
- **[Check the board](#check-the-board)** -- Prove it works.

## Check what you need

- An ALINX AX7101 board with its power supply.
- The board's JTAG cable, a Digilent FT232H.
- A USB serial adapter on the board console.
- A PC that runs the tools below.
- An AVB switch and a Milan controller, such as Hive.

## Choose your path

One image set is three files from one build.

| File | Location in the build directory |
|---|---|
| Bitstream | `gateware/alinx_ax7101.bit` |
| Entity model | `aem_desc.bin` |
| Flash layout | `flashboot_layout.json` |

| You have | Do this |
|---|---|
| An image set made for this board | [Flash a new board](#flash-a-new-board) |
| Only this repository | [Install the build tools](#install-the-build-tools) |

Each board needs its own image set.

The board identity is built into the image.

## Set the board identity

The controller cannot change these fields.

Set them in a copy of `configs/endstation_ax7101_1x1_tdm8.yaml`.

| Field | Key | What to do |
|---|---|---|
| MAC address | `platform.mac_address` | Give every board its own value. |
| Serial number | `entity.serial_number` | Give every board its own value. |
| Vendor name | `entity.vendor_name` | Set once for all boards. |
| Entity ID | `entity.entity_id` | Keep `mac-derived`. |
| Entity model ID | `entity.entity_model_id` | Keep `hash-derived`. |
| gPTP priorities | `gptp.priority1`, `gptp.priority2` | Keep 248. |

The entity ID follows the MAC address.

The entity model ID follows the model shape only.

A new MAC or serial number keeps the model ID.

Write the MAC address in quotes, as six octets.

The `02` first octet marks a local address.

A shipped product needs addresses from your vendor block.

The controller changes these fields at run time:

- Entity name and group name.
- Sampling rate, stream formats and clock source.
- Channel maps, bindings and presentation time offset.

The configuration file holds only their first value.

Every key is mapped in the
[builder schema table](../ENDSTATION_BUILDER.md#3-config-schema--aem-descriptor-mapping).

## Install the build tools

Install the third tier of the
[README prerequisites](../../README.md#prerequisites--by-what-you-actually-want-to-do).

Install LiteX from the pins, never from upstream master.

Upstream LiteX cannot build this design.

Create the LiteX virtual environment, then install into it:

```sh
python3 -m venv ~/litex-milan/venv
. ~/litex-milan/venv/bin/activate
python3 -m pip install -r sw/litex/litex_pins.txt
python3 scripts/ci_litex_env.py
sw/litex/patches/apply.sh
```

The [patch series README](../../sw/litex/patches/README.md) explains each patch.

`build.sh` expects two install locations:

| Tool | Location |
|---|---|
| Vivado 2026.1 | `~/Xilinx2/2026.1/Vivado` |
| LiteX virtual environment | `~/litex-milan/venv` |

Link your install there if it lives elsewhere.

Initialise the submodules the builder reads:

```sh
git submodule update --init gptp-processor protocol-processor \
    third_party/tsn-c-stack third_party/verilog-axis
```

Name the JTAG cable before any flash write.

List the cables with `openFPGALoader --scan-usb`.

Copy `sw/litex/boards.local.sh.example` to `sw/litex/boards.local.sh`.

Set `AX_FTDI` there to the AX7101 cable serial.

Never commit that file.

## Build an image set

Build one image set per board.

1. Copy the shipping configuration:

   ```sh
   cp configs/endstation_ax7101_1x1_tdm8.yaml \
      configs/endstation_ax7101_1x1_tdm8_board2.yaml
   ```

2. Edit `mac_address` and `serial_number` in the copy.
3. Regenerate the tracked definition for the copy:

   ```sh
   python3 sw/builder/endstation_builder.py \
       configs/endstation_ax7101_1x1_tdm8_board2.yaml --write-rtl
   ```

   `build.sh` refuses the copy without this step.
4. Build, which takes about one hour:

   ```sh
   BUILD_CFG=configs/endstation_ax7101_1x1_tdm8_board2.yaml \
       sw/litex/build.sh ax7101
   ```

   The build prints its directory under `~/litex-milan/work/`.
5. Restore the shipping definition:

   ```sh
   python3 sw/builder/endstation_builder.py \
       configs/endstation_ax7101_1x1_tdm8.yaml --write-rtl
   ```

6. Keep the copy and the build directory.

   Never commit the copy.

The next update of that board needs its build directory.

## Flash a new board

A new board carries the vendor demonstration image.

`flash-pair` cannot prove that image, so it refuses.

Use the two recovery writes instead.

Write the entity model first and the bitstream last:

```sh
B=<build directory>
ALLOW_NONATOMIC_FLASH=1 LAYOUT=$B/flashboot_layout.json \
    BIT=$B/gateware/alinx_ax7101.bit sw/litex/deploy.sh flash-images
ALLOW_NONATOMIC_FLASH=1 LAYOUT=$B/flashboot_layout.json \
    BIT=$B/gateware/alinx_ax7101.bit sw/litex/deploy.sh flash
```

Both writes read back and verify their data.

## Update a flashed board

Name the build now in flash, then the new build:

```sh
INSTALLED_BUILD=<build directory now in flash> \
    sw/litex/build.sh flash ax7101:<new build directory>
```

The command proves the installed build before writing.

[QSPI flash boot](../integration/QSPI_FLASHBOOT.md#build-a-flash-boot-bitstream)
holds the full transaction.

## Check the board

Open the console at 115200 baud:

```sh
sw/litex/deploy.sh console
```

Power-cycle the board.

Within ten seconds the console shows three lines:

```console
Milan baremetal: CSR ID=4d494c4e VERSION=...
Milan baremetal: AEM ... B copied QSPI ... CRC ...
Milan baremetal: fabric entity enable requested; the fabric holds it until the restore releases it; UART diagnostics ready.
```

The third line prints only after the model check passes.
It reports that the firmware requested the enable.
The fabric holds the entity until the saved-state restore reaches its terminal.

Without it the controller cannot see the board.

Flash both images again in that case.

Within fifteen seconds the controller lists the entity.

Its serial number matches your configuration.

Set names, formats, clock source and bindings in the controller.

The [troubleshooting log](../limitations/TROUBLESHOOTING.md)
covers boot, flash, link and stream faults.
