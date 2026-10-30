# Sampling ledger: docs/guides/BOARD_DEPLOYMENT.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 3 | sentence | Use this path to install an AX7101 board. | - | ok: AX7101 is the shipping board (configs/endstation_ax7101_1x1_tdm8.yaml) |
| 18 | item | An ALINX AX7101 board with its power supply. | - | ok: sw/litex/build.sh:69 ax7101 recipe |
| 19 | item | The board's JTAG cable, a Digilent FT232H. | - | ok: sw/litex/deploy.sh:7 'Digilent FT232H (0403:6014)', CABLE ft232 at line 54 |
| 37 | row | \| Only this repository \| [Install the build tools](#install-the-build-tools) \| | - | ok: anchor held by scripts/gen_toc.py --verify-anchors |
| 45 | sentence | The controller cannot change these fields. | - | ok: identity fields are build-time config (lines 49-56), AEM image generated per build |
| 51 | row | \| MAC address \| `platform.mac_address` \| Give every board its own value. \| | - | ok: configs/endstation_ax7101_1x1_tdm8.yaml:67 platform.mac_address |
| 52 | row | \| Serial number \| `entity.serial_number` \| Give every board its own value. \| | - | ok: same config line 28 entity.serial_number |
| 53 | row | \| Vendor name \| `entity.vendor_name` \| Set once for all boards. \| | - | ok: same config line 27 entity.vendor_name |
| 56 | row | \| gPTP priorities \| `gptp.priority1`, `gptp.priority2` \| Keep 248. \| | - | ok: same config lines 89-90 priority1/priority2 248 |
| 60 | sentence | The entity model ID follows the model shape only. | - | ok: same config line 22 entity_model_id hash-derived, comment 'shape change -> NEW id' |
| 76 | sentence | The configuration file holds only their first value. | - | ok: run-time fields (lines 71-74) have a config default only |
| 78 | sentence | Every key is mapped in the [builder schema table](../ENDSTATION_BUILDER.md#3-config-schema--aem-descriptor-mapping). | path 1 | ok: docs/ENDSTATION_BUILDER.md anchor (anchor gate) |
| 86 | sentence | Install LiteX from the pins, never from upstream master. | - | policy |
| 88 | sentence | Upstream LiteX cannot build this design. | - | ok: sw/litex/patches/apply.sh patch series is required (scripts/ci_litex_env.py) |
| 92 | code | ```sh python3 -m venv ~/litex-milan/venv . ~/litex-milan/venv/bin/activate python3 -m pip install -r sw/litex/litex_pins.txt python3 scripts/ci_litex_env.py ... | command 2 | ok: sw/litex/litex_pins.txt, scripts/ci_litex_env.py, sw/litex/patches/apply.sh exist |
| 106 | row | \| Vivado 2026.1 \| `~/Xilinx2/2026.1/Vivado` \| | - | ok: sw/litex/build.sh:492 sources $HOME/Xilinx2/2026.1/Vivado/settings64.sh |
| 113 | code | ```sh git submodule update --init gptp-processor protocol-processor \ third_party/tsn-c-stack third_party/verilog-axis ``` | - | ok: .gitmodules lines 5-17 carry all four paths |
| 124 | sentence | Set `AX_FTDI` there to the AX7101 cable serial. | - | ok: sw/litex/build.sh:57-64 AX_FTDI from sw/litex/boards.local.sh (example tracked) |
| 126 | sentence | Never commit that file. | - | ok: .gitignore:80 sw/litex/boards.local.sh |
| 132 | item | Copy the shipping configuration: | - | policy |
| 134 | code |  ```sh cp configs/endstation_ax7101_1x1_tdm8.yaml \ configs/endstation_ax7101_1x1_tdm8_board2.yaml ``` | - | ok: configs/endstation_ax7101_1x1_tdm8.yaml exists |
| 142 | code |  ```sh python3 sw/builder/endstation_builder.py \ configs/endstation_ax7101_1x1_tdm8_board2.yaml --write-rtl ``` | command 1 | ok: sw/builder/endstation_builder.py defines --write-rtl (auto) |
| 147 | sentence | `build.sh` refuses the copy without this step. | - | ok: sw/litex/build.sh:436-445 refuses through scripts/check_entity_shape.py --built-config when the tree is another shape's |
| 150 | code |  ```sh BUILD_CFG=configs/endstation_ax7101_1x1_tdm8_board2.yaml \ sw/litex/build.sh ax7101 ``` | command 1 | ok: sw/litex/build.sh:170-192 BUILD_CFG rebinding |
| 156 | item | Restore the shipping definition: | - | policy |
| 158 | code |  ```sh python3 sw/builder/endstation_builder.py \ configs/endstation_ax7101_1x1_tdm8.yaml --write-rtl ``` | command 1 | ok: as line 142 |
| 165 | sentence | Never commit the copy. | - | policy |
| 173 | sentence | `flash-pair` cannot prove that image, so it refuses. | - | ok: sw/litex/deploy.sh do_flash_pair proves the installed offset-zero payload (QSPI_FLASHBOOT.md:79 context) |
| 179 | code | ```sh B=<build directory> ALLOW_NONATOMIC_FLASH=1 LAYOUT=$B/flashboot_layout.json \ BIT=$B/gateware/alinx_ax7101.bit sw/litex/deploy.sh flash-images ALLOW_NO... | command 2 | ok: sw/litex/deploy.sh:33 and 398-400 ALLOW_NONATOMIC_FLASH, cases flash and flash-images at lines 518-520 |
| 193 | code | ```sh INSTALLED_BUILD=<build directory now in flash> \ sw/litex/build.sh flash ax7101:<new build directory> ``` | command 1 | ok: sw/litex/build.sh flash with INSTALLED_BUILD (QSPI_FLASHBOOT.md:75-76 same form) |
| 205 | sentence | Open the console at 115200 baud: | - | ok: sw/litex/deploy.sh:53 BAUD default 115200 |
| 207 | code | ```sh sw/litex/deploy.sh console ``` | command 1 | ok: sw/litex/deploy.sh:521 console case |
| 215 | code | ```console Milan baremetal: CSR ID=4d494c4e VERSION=... Milan baremetal: AEM ... B copied QSPI ... CRC ... Milan baremetal: fabric entity enabled; UART diagn... | - | ok: sw/firmware/milan_baremetal/milan_baremetal.c lines 1874, 1860 and 1833 print the three lines |
| 221 | sentence | The third line prints only after the model check passes. | - | ok: milan_baremetal.c entity_advertise() returns before printing unless the AEM verdict matched (line 1827-1833) |
| 223 | sentence | Without it the controller cannot see the board. | - | ok: ADP_CTRL[0] is set only in entity_advertise (line 1831) |
