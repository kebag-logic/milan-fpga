# Sampling ledger: docs/integration/BOARD_PORTING_AX7101.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 3 | sentence | How the Milan fully-FPGA SoC was ported to the real **Alinx AX7101** board: where the pin data came from, how it was extracted, what changed, and what is ver... | path 2 | ok: sw/litex/platforms/alinx_ax7101.py exists; sw/litex/milan_soc.py:3980 --full |
| 3 | sentence | The result is [`sw/litex/platforms/alinx_ax7101.py`](../../sw/litex/platforms/alinx_ax7101.py) + `sw/litex/milan_soc.py --full` (now with DDR3). | path 2 | ok: sw/litex/platforms/alinx_ax7101.py exists; sw/litex/milan_soc.py:3980 --full |
| 19 | sentence | Source of truth: **github.com/alinxalinx/AX7101** (datasheets, schematics, and example Vivado projects with real constraints). | - | hist: vendor source of the pin data |
| 24 | row | \| FPGA \| **XC7A100T-2FGG484I** (Artix-7, FGG484, speed -2, industrial) \| part marking \| | - | ok: alinx_ax7101.py part xc7a100t (line 325 IDCODE note) FGG484 |
| 25 | row | \| System clock \| **200 MHz** differential (siT9102) on **R4/T4**, DIFF_SSTL15 \| `SRC/01_led_test/…/led.xdc` \| | - | ok: alinx_ax7101.py:27-28 R4/T4 DIFF_SSTL15 |
| 26 | row | \| Reset \| active-low key **T6** (LVCMOS15) \| led/uart XDC \| | - | ok: alinx_ax7101.py:30 cpu_reset_n T6 LVCMOS15 |
| 27 | row | \| UART console \| CP2102, **tx AB15 / rx AA15** (LVCMOS33) \| `SRC/04_uart_test/…/uart_test.xdc` \| | - | ok: alinx_ax7101.py:34-35 tx AB15 rx AA15 LVCMOS33 |
| 28 | row | \| LEDs \| E17, F16 \| led.xdc \| | - | ok: alinx_ax7101.py:39-40 E17, F16 |
| 29 | row | \| Ethernet \| **4× RTL8211E** GbE PHYs (`e1`..`e4`), RGMII/GMII \| `SRC/15_ethernet_test/…/top.xdc` \| | - | hist: vendor board fact (four RTL8211E); e1/e2 are the ports the platform carries |
| 30 | row | \| DDR3 \| **512 MB, 2× MT41J256M16** (32-bit) \| `SRC/07_ddr3_test/…/ddr3.ucf` \| | - | ok: alinx_ax7101.py:9 512 MB MT41J256M16; milan_soc.py:3036 MT41J256M16 on the AX7101 |
| 37 | sentence | Pins were **ported from the official constraints, not hand-guessed** - so they can be re-derived if the board revision changes: | - | hist: method record |
| 40 | item | **List the repo** via the GitHub API (`git/trees/master?recursive=1`) and locate the example XDC/UCF files (led, uart, ethernet, ddr3). | - | hist: method record |
| 44 | item | **Simple groups** (clock/reset/UART/LED, and the `e1`/`e2` Ethernet data+control pins - GMII, per the correction below) → transcribed directly into the LiteX... | - | hist: method record |
| 48 | item | **DDR3 (68 pins)** → parsed programmatically from `ddr3.ucf` into a LiteX `ddram` pad group (a short `re`-based script grouping `ddr3_addr/ba/dq/dqs/…` and m... | - | hist: method record |
| 54 | sentence | **CORRECTION (hardware bring-up):** the AX7101 RTL8211E is strapped for **GMII (8-bit SDR)**, *not* RGMII (4-bit DDR). | issue 2 | ok: GMII correction matches MilanMAC phy_model gmii default (milan_soc.py MilanMAC); #259 CLOSED holds the retired capture, #117 OPEN |
| 54 | sentence | This was initially ported as RGMII (matching LiteEth's default for a 1G Artix + RTL8211), and it produced **100 % MAC preamble errors** on silicon - reading ... | issue 2 | ok: GMII correction matches MilanMAC phy_model gmii default (milan_soc.py MilanMAC); #259 CLOSED holds the retired capture, #117 OPEN |
| 54 | sentence | The retired console capture remains available in Git history under #259; exact-candidate physical acceptance is tracked by #117. | issue 2 | ok: GMII correction matches MilanMAC phy_model gmii default (milan_soc.py MilanMAC); #259 CLOSED holds the retired capture, #117 OPEN |
| 63 | sentence | The **GMII (8-bit)** wiring per port is therefore: `rx_data[0:7]`, `tx_data[0:7]`, `rx_dv = e_rxdv`, `rx_er = e_rxer`, `tx_en = e_txen`, clocks `rx = e_rxc` ... | - | ok: MilanMAC uses LiteEthPHYGMII (milan_soc.py MilanMAC imports) |
| 63 | sentence | `MilanMAC` uses **`LiteEthPHYGMII`** (the earlier RGMII `s7rgmii`/`milan_rgmii.py` path is retired for this board). | - | ok: MilanMAC uses LiteEthPHYGMII (milan_soc.py MilanMAC imports) |
| 71 | item | **[`sw/litex/platforms/alinx_ax7101.py`](../../sw/litex/platforms/alinx_ax7101.py)** - replaced the placeholder pins (borrowed from the AX7203) with the real... | path 2 | ok: alinx_ax7101.py pins as lines 24-28 |
| 79 | item | **[`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py)** - added **512 MB DDR3 (LiteDRAM)**: `_CRG` now generates the DDR3 PHY clocks (`sys4x`, `sys4x_dqs`... | path 2 | F: D0-038 |
| 88 | sentence | `./sw/litex/milan_soc.py --full --xlen 64` elaborates and **exports a P&R-ready gateware** (exit 0): | - | F: D0-039 |
| 90 | item | `A7DDRPHY` + `sdram (LiteDRAMCore)` instantiated; `main_ram` = DDR3 @ `0x4000_0000`; the LiteDRAM software (`sdram.c`, DDR3 training) compiled into the BIOS. | - | ok: LiteX main_ram origin 0x4000_0000 (milan_soc.py:3214-3224 reads the region) |
| 92 | item | **284 `ddram` constraint lines** in the generated `.xdc` (the real DDR3 pinout). | - | hist: measured count of a past elaboration, not recomputed |
| 93 | item | `milan_datapath` (the NIC) + the LiteEth MAC/PHY present (e1 is **GMII** -- `LiteEthPHYGMII`, per the Section 3 correction). | - | ok: MilanMAC with LiteEthPHYGMII |
| 94 | item | The platform shape regenerates from this build's `csr.json` (see the retired binding toolkit, `fpga-ps-tools`). | - | hist: names a retired toolkit as such |
| 99 | item | **MDIO data pin** - ✅ **CLEARED (2026-07-22).** The Alinx GMII example doesn't route it, so `e_mdc` was known from the vendor XDC (J17/AB21) but `mdio` had t... | issue 2 | F: D0-010 (the #599 sentence at line 110); pins ok: alinx_ax7101.py:62-78 mdc J17, mdio L16 with PULLUP, e2 mdio AB22 |
| 112 | item | **Artix-7 bitstream** - `--full --build` needs Vivado with Artix-7 device support (the original dev host had only Spartan-7 installed). Earlier bitstreams we... | issue 2 | ok: #259 CLOSED holds the retired captures, #117 OPEN |
| 117 | item | **On-board bring-up** - the board is attached to the build box and **verified reachable**: **JTAG** = Digilent FT232H (`0403:6014`), `openFPGALoader -c ft232... | path 4; issue 2; command 1 | ok: sw/litex/deploy.sh:7 FT232H 0403:6014; deploy.sh:13 factory demo 9600 baud |
| 130 | sentence | A new board's PHY and MAC receive chain are not this board's, so it must measure its own `gptp.ingress_latency_ns` and `gptp.egress_latency_ns` before the fa... | - | ok: sw/builder/endstation_builder.py:4103-4111 refuses a missing gptp latency key (#358) |
| 130 | sentence | The builder refuses a board that omits either key, so this is a porting step and not an optional one. | - | ok: sw/builder/endstation_builder.py:4103-4111 refuses a missing gptp latency key (#358) |
| 139 | sentence | The quantity is the port's own timestamp error: how late its ingress stamp is plus how early its egress stamp is. | - | ok: measurement method; consistent with GPTP_LAT semantics (REGISTER_MAP 0x7F0) |
| 139 | sentence | It is measurable from OUTSIDE the device, with one capture tap and no access to the design. | - | ok: measurement method; consistent with GPTP_LAT semantics (REGISTER_MAP 0x7F0) |
| 143 | sentence | Put a capture tap inline on the link under test, so it timestamps every frame in both directions on ONE clock. | - | policy: method |
| 152 | sentence | Their difference is the tap's own transit for the request, twice the cable between tap and responder, and the responder's timestamp error. | - | ok: method arithmetic |
| 155 | sentence | Such a device compensates its own stamps, so its difference IS the tap transit plus cable, and it is the instrument's zero. | - | ok: method arithmetic |
| 155 | sentence | Subtract it from the port's difference and what remains is the port's own error, which is the sum to declare. | - | ok: method arithmetic |
| 160 | sentence | Forty exchanges per direction over about forty seconds is enough: the quantity is a fixed offset, and the spread across those exchanges is the uncertainty to... | - | policy: method |
| 166 | sentence | It cannot establish the SPLIT between ingress and egress, and no arrangement of one tap clock can: both errors enter the turnaround with the same sign. | - | ok: one tap clock sees only the sum (both corrections enter the turnaround with one sign) |
| 170 | sentence | So split the measured sum 3:1 receive to transmit unless the port's PHY datasheet states 1000BASE-T transmit and receive latencies, in which case use those a... | - | ok: configs/endstation_ax7101_1x1_tdm8.yaml:122-123 656/219 ns, a 3:1 split |
| 170 | sentence | The split error does not move the peer delay - both corrections enter the mean-delay expression with the same sign, so only their sum appears - but it moves ... | - | ok: configs/endstation_ax7101_1x1_tdm8.yaml:122-123 656/219 ns, a 3:1 split |
| 181 | sentence | The applied pair is published read-only at `GPTP_LAT` (`0x7F0`) and on the `milan_status` console line, so the value in the bitstream can be read back rather... | - | ok: milan_baremetal.c:1917-1926 prints GPTP_LAT on milan_status; Milan v1.2 4.2.6.1.1 neighborPropDelayThresh 800 ns |
| 181 | sentence | With the correction in place the port's published peer delay should fall to the true path delay, and a conformant bridge whose own measurement then sits insi... | - | ok: milan_baremetal.c:1917-1926 prints GPTP_LAT on milan_status; Milan v1.2 4.2.6.1.1 neighborPropDelayThresh 800 ns |
