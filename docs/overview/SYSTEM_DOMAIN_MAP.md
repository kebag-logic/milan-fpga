# System domain map

Which module lives in which domain and language: the bare-metal Milan TSN NIC
from its target firmware down to Artix-7 silicon, plus the host tooling that
generates and deploys it. Software is at the top, hardware at the bottom.

![Milan system domain map](../SYSTEM_DOMAIN_MAP.svg)

*(Editable source: [`SYSTEM_DOMAIN_MAP.drawio`](../SYSTEM_DOMAIN_MAP.drawio)  -  open in
[diagrams.net](https://app.diagrams.net). Regenerate the `.drawio`/`.svg`/`.png` from one
layout model with [`SYSTEM_DOMAIN_MAP.gen.py`](../SYSTEM_DOMAIN_MAP.gen.py)
(`python3 docs/SYSTEM_DOMAIN_MAP.gen.py docs/SYSTEM_DOMAIN_MAP` → `.svg`+`.drawio`, then
`rsvg-convert -o …png …svg`). If you add modules, edit the generator, not the outputs.)*

## The domains

| Domain | Language / form | Where | Contains |
|--------|-----------------|-------|----------|
| **Bare-metal firmware** | C | target (machine mode) | Milan UART/CSR diagnostics and boot policy plus the LiteX BIOS, which CRC-checks and copies the raw AEM image from QSPI. This is the one target software surface. |
| **Retired software stack (#259)** | historical only | Git history | Linux kernel, `kl-eth`, OpenSBI, device tree, Buildroot rootfs, PipeWire/ALSA and the linuxptp software owner are not product domains or supported configurations. |
| **SoC integration** | Python (Migen/LiteX) → Verilog | dev host | `MilanSoC`, `_CRG`, `MilanNIC`/`add_milan_datapath`, `MilanMAC`, `MilanDMA`, `MilanDebug`  -  the glue that wires our RTL to the CPU (VexiiRiscv or NaxRiscv)/LiteEth/LiteDRAM/LiteSPI. All in **milan-fpga** [`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py). |
| **Milan datapath  -  RTL** | SystemVerilog / Verilog | FPGA fabric | The actual TSN logic in **milan-fpga** `hdl/`: `milan_datapath`/`milan_top`, `milan_csr` (the register ABI), the 802.1Q CBS shaper, PTP timestamp unit, 1722 AVTP + AVDECC ADP parsers, event counters, `rx_mac_filter`/`tcam`, CDC. |
| **Vendored IP** | 3rd-party cores | FPGA fabric | VexiiRiscv supplies the cacheless product RV32I core. Former Linux/MMU VexiiRiscv and NaxRiscv profiles are retired historical configurations (#259). LiteEth, LiteDRAM, LiteSPI and verilog-axis remain pinned upstream IP. |
| **Board / silicon** | physical |  -  | XC7A100T-2FGG484, DDR3 512 MB, 16 MB QSPI (N25Q128), RTL8211E GbE PHY, 200 MHz clock. |
| **Host tooling** | Python / bash | dev host | `milan_soc.py`, the end-station builder, `deploy.sh`, `boot.sh`, `patches/apply.sh` and `crcfbigen` generate, validate, flash and boot the bare-metal artifact set. Host tools are not a target runtime. |

The register map (`milan_csr`) is the contract between RTL, bare-metal
firmware, generated build artifacts and host diagnostics; see
[REGISTER_MAP.md](../reference/REGISTER_MAP.md). For runtime data/control flow
see [ARCHITECTURE.md](ARCHITECTURE.md), and for deployment see
[QSPI_FLASHBOOT.md](../integration/QSPI_FLASHBOOT.md).
