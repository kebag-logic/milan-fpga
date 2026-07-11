# Board porting  -  Alinx AX7101 (XC7A100T-2FGG484I)

How the Milan fully-FPGA SoC was ported to the real **Alinx AX7101** board: where the
pin data came from, how it was extracted, what changed, and what is verified vs.
board-gated. The result is `sw/litex/platforms/alinx_ax7101.py` +
`sw/litex/milan_soc.py --full` (now with DDR3).

## 1. Board facts (from the official Alinx repo)

Source of truth: **github.com/alinxalinx/AX7101** (datasheets, schematics, and example
Vivado projects with real constraints).

| Item | Value | Source |
|------|-------|--------|
| FPGA | **XC7A100T-2FGG484I** (Artix-7, FGG484, speed -2, industrial) | part marking |
| System clock | **200 MHz** differential (siT9102) on **R4/T4**, DIFF_SSTL15 | `SRC/01_led_test/…/led.xdc` |
| Reset | active-low key **T6** (LVCMOS15) | led/uart XDC |
| UART console | CP2102, **tx AB15 / rx AA15** (LVCMOS33) | `SRC/04_uart_test/…/uart_test.xdc` |
| LEDs | E17, F16 | led.xdc |
| Ethernet | **4× RTL8211E** GbE PHYs (`e1`..`e4`), RGMII/GMII | `SRC/15_ethernet_test/…/top.xdc` |
| DDR3 | **512 MB, 2× MT41J256M16** (32-bit) | `SRC/07_ddr3_test/…/ddr3.ucf` |

The Milan NIC's two ports map to **`e1` and `e2`**  -  i.e. the "two first interfaces"
the `amx-pw0` / `amx-pw1` test endpoints exercise. `e3`/`e4` are spare.

## 2. Porting method (reproducible)

Pins were **ported from the official constraints, not hand-guessed**  -  so they can be
re-derived if the board revision changes:

1. **List the repo** via the GitHub API (`git/trees/master?recursive=1`) and locate the
   example XDC/UCF files (led, uart, ethernet, ddr3).
2. **Fetch** them with `raw.githubusercontent.com` and read the `PACKAGE_PIN` /
   `NET … LOC` lines.
3. **Simple groups** (clock/reset/UART/LED, and the `e1`/`e2` RGMII data+control pins)
   → transcribed directly into the LiteX `_io` list, with each pin annotated by its
   Alinx signal name (`e1_rxd[0]` = N22, …).
4. **DDR3 (68 pins)** → parsed programmatically from `ddr3.ucf` into a LiteX `ddram`
   pad group (a short `re`-based script grouping `ddr3_addr/ba/dq/dqs/…` and mapping to
   the A7DDRPHY subsignal names `a/ba/ras_n/cas_n/we_n/cs_n/dm/dq/dqs_p/dqs_n/clk_p/
   clk_n/cke/odt/reset_n`). This avoids transcription errors on the largest group.

### PHY mapping (per port)  -  GMII, not RGMII
> **CORRECTION (hardware bring-up):** the AX7101 RTL8211E is strapped for **GMII
> (8-bit SDR)**, *not* RGMII (4-bit DDR). This was initially ported as RGMII (matching
> LiteEth's default for a 1G Artix + RTL8211), and it produced **100 % MAC preamble
> errors** on silicon  -  reading a 4-bit-DDR stream off an 8-bit-SDR bus corrupts every
> byte. The Alinx vendor top (`SRC/15_ethernet_test/.../ethernet_test.v`) is explicit:
> `input [7:0] e_rxd`, separate `e_rxdv`/`e_rxer`, `assign e_gtxc=e_rxc`. Full story in
> `docs/TROUBLESHOOTING.md` §17 + `sw/litex/evidence/hw_ma3_dma_datapath_100mhz.md`.

The **GMII (8-bit)** wiring per port is therefore: `rx_data[0:7]`, `tx_data[0:7]`,
`rx_dv = e_rxdv`, `rx_er = e_rxer`, `tx_en = e_txen`, clocks `rx = e_rxc` /
`gtx = e_gtxc` (1G) / `tx = e_txc` (MII), plus `rst_n = e_reset`. `MilanMAC` uses
**`LiteEthPHYGMII`** (the earlier RGMII `s7rgmii`/`milan_rgmii.py` path is retired for
this board).

## 3. What changed

- **`sw/litex/platforms/alinx_ax7101.py`**  -  replaced the placeholder pins (borrowed
  from the AX7203) with the real AX7101 pinout: exact part `xc7a100t-fgg484-2`, clock
  R4/T4, reset T6, UART AB15/AA15, LEDs, `eth`/`eth_clocks` 0+1 (e1/e2 RGMII), the
  full `ddram` group, and the SPIx4/CONFIGRATE bitstream settings from the Alinx XDC.
- **`sw/litex/milan_soc.py`**  -  added **512 MB DDR3 (LiteDRAM)**: `_CRG` now generates
  the DDR3 PHY clocks (`sys4x`, `sys4x_dqs`, `idelay` + IDELAYCTRL); `MilanSoC` adds
  `s7ddrphy.A7DDRPHY` + `add_sdram(module=MT41J256M16, l2_cache_size=8192)` behind a new
  `--with-dram` flag (included in `--full`). With DRAM, main RAM is the DDR3 at
  `0x4000_0000` (not integrated SRAM)  -  this is what makes the SoC **Linux-capable**
  (migration §A.3). This closes the last big platform gap.

## 4. Verification (open toolchain, no Vivado)

`./sw/litex/milan_soc.py --full --xlen 64` elaborates and **exports a P&R-ready
gateware** (exit 0):
- `A7DDRPHY` + `sdram (LiteDRAMCore)` instantiated; `main_ram` = DDR3 @ `0x4000_0000`;
  the LiteDRAM software (`sdram.c`, DDR3 training) compiled into the BIOS.
- **284 `ddram` constraint lines** in the generated `.xdc` (the real DDR3 pinout).
- `milan_datapath` (the NIC) + `LiteEthPHYRGMII` (e1/e2 MAC/PHY) present.
- The device tree regenerates from this build's `csr.json` (see `sw/dts`,
  `fpga-ps-tools`).

## 5. Board-gated (needs the schematic / Vivado / the board)

- **MDIO data pin**  -  the Alinx GMII example doesn't route it; `e_mdc` is known
  (J17/AB21) but the `mdio` pin must come from `SCH/AX7101_EX_SCH.pdf`. MDIO is left
  unwired for now (the RGMII data path works on the PHY power-on straps); PHY
  management is migration §A.7.
- **Artix-7 bitstream**  -  `--full --build` still needs Vivado with Artix-7 device
  support (this host has only Spartan-7 installed). The gateware/pins are ready; only
  the vendor P&R is blocked.
- **On-board bring-up**  -  the board is attached and **verified reachable**:
  **JTAG** = Digilent FT232H (`0403:6014`), `openFPGALoader -c ft232` reads IDCODE
  `0x3631093` = xc7a100t ✅; **console** = CP2102N (`10c4:ea60`), currently showing the
  Alinx factory demo (`Hello ALINX AX7101` @ 9600). Identify by `/dev/serial/by-id/`
  (the `ttyUSBn` numbers flip on re-plug). Program with `sw/litex/deploy.sh`, then
  M-A1…M-A5 (see `FULL_FPGA_SOLUTION.md` §9). Still gated on the Artix-7 bitstream.
