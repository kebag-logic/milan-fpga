# Board deployment guide

Use this path to install an AX7101 board.

It also covers the same board fitted with an XC7A200T.

## Contents

- **[Check what you need](#check-what-you-need)** -- Hardware and a PC.
- **[Choose your path](#choose-your-path)** -- Flash or build first.
- **[Flash an image set over JTAG](#flash-an-image-set-over-jtag)** -- The plain commands.
- **[Set the board identity](#set-the-board-identity)** -- Per-board fields.
- **[Install the build tools](#install-the-build-tools)** -- Pinned LiteX and Vivado.
- **[Build an image set](#build-an-image-set)** -- One build per board.
- **[Flash a new board](#flash-a-new-board)** -- The first install.
- **[Update a flashed board](#update-a-flashed-board)** -- Replace a known build.
- **[Check the board](#check-the-board)** -- Prove it works.
- **[What is untested on the XC7A200T](#what-is-untested-on-the-xc7a200t)** -- No board ran it.

## Check what you need

- An ALINX AX7101 board with its power supply.

  The XC7A200T variant is the same board with that die.
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

Both boards use these names.

Each variant reads its values from its own layout:

<!-- board-flash-variants:start -->
| Board | `build.sh` recipe | Part | Entity model offset | Flash device |
|---|---|---|---|---|
| AX7101 | `ax7101` | `xc7a100tfgg484` | `0x400000` | `N25Q128A13` |
| XC7A200T variant | `ax7a200t` | `xc7a200tfbg484` | `0xa00000` | `N25Q128A13` |
<!-- board-flash-variants:end -->

The table is checked against the sources by `scripts/board_variants.py`.

A delivered image set keeps this directory layout.

| You have | Do this |
|---|---|
| An image set made for this board | [Flash a new board](#flash-a-new-board) |
| Only this repository | [Install the build tools](#install-the-build-tools) |

Each board needs its own image set.

The board identity is built into the image.

## Flash an image set over JTAG

Read the part, offset and flash ID from the layout:

```sh
B=<image set directory>
set -- $(python3 -c 'import json, sys; d = json.load(open(sys.argv[1]))
print("xc" + d["bitstream_fpga_part"],
      hex([i for i in d["images"] if i["name"] == "aem"][0]["offset"]),
      hex(d["flash_jedec_id"]))' "$B/flashboot_layout.json")
P=$1 O=$2
echo "part $P, entity model at $O, flash ID $3"
```

A test load writes only the FPGA, not the flash:

```sh
openFPGALoader -c ft232 --fpga-part $P $B/gateware/alinx_ax7101.bit
```

It is lost at the next power-cycle.

A persistent write takes two commands, entity model first:

```sh
openFPGALoader -c ft232 --fpga-part $P -o $O --write-flash \
    --file-type raw --verify $B/aem_desc.bin
openFPGALoader -c ft232 --fpga-part $P -f --verify \
    $B/gateware/alinx_ax7101.bit
```

Then power-cycle the board.

Add `--ftdi-serial <serial>` when two FTDI cables are plugged in.

`openFPGALoader --scan-usb` lists their serials.

Without it, a write can reach the wrong board.

Vivado Hardware Manager is the fallback.

Join both images into one file, in the Vivado console:

```tcl
set B <image set directory>
set O <offset printed above>
write_cfgmem -force -format bin -interface spix4 -size 16 \
    -loadbit "up 0x0 $B/gateware/alinx_ax7101.bit" \
    -loaddata "up $O $B/aem_desc.bin" -file image_set.bin
```

Then program it:

1. Open the target, then add a configuration memory device.
2. Pick `mt25ql128-spi-x1_x2_x4` for flash ID `0x20ba18`.
3. Program `image_set.bin` with erase and verify on.
4. Power-cycle the board.

Vivado lists the N25Q128A13 under that successor name.

The erase covers that file's range only.

`deploy.sh` stays the checked route, and adds three proofs:

- The bitstream payload and part are bound to the layout.
- The FPGA die and flash ID match the image set.
- `flash-pair` proves the build now in flash first.

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

   Build the XC7A200T variant with `sw/litex/build.sh ax7a200t`.
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

For the XC7A200T variant, also set `FPGA_PART=xc7a200tfbg484`.

Each write first reads the FPGA die and flash ID.

It refuses an image set made for another die.

It also refuses a flash other than the layout's.

## Update a flashed board

`INSTALLED_BUILD` is the image set directory now in flash.

A delivered image set can be that directory.

Name it, then the new build:

```sh
INSTALLED_BUILD=<build directory now in flash> \
    sw/litex/build.sh flash ax7101:<new build directory>
```

The XC7A200T variant uses `ax7a200t:` in place of `ax7101:`.

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

Without it the controller cannot see the board.

Flash both images again in that case.

The third line reports that the firmware requested the enable.

The saved-state restore releases the enable at its terminal.

Within fifteen seconds the controller lists the entity.

Its serial number matches your configuration.

Set names, formats, clock source and bindings in the controller.

The [troubleshooting log](../limitations/TROUBLESHOOTING.md)
covers boot, flash, link and stream faults.

## What is untested on the XC7A200T

No XC7A200T board has run this image yet.

Its build closes timing, and its flash commands ran dry.

Confirm three things on the board first:

- The die is speed grade -2.
- The flash ID matches the layout's `flash_jedec_id`.
- The JTAG cable is the onboard FT232H.

`deploy.sh` checks the die and the flash ID itself.

The speed grade is printed on the package only.
