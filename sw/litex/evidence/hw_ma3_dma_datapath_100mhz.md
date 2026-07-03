# M-A3 (partial) — DMA + AXIS-CDC data path on silicon (100 MHz, all-blocks)

Driven from the LiteX BIOS console (`mem_write`/`mem_read`) on the AX7101, all-blocks
100 MHz bitstream (datapath in the 50 MHz `milan` CDC domain). No toolchain needed.

## Verified on hardware ✅
- **DDR3 R/W of a real Ethernet frame** — wrote a broadcast frame to `0x40010000`,
  read back `ff ff ff ff ff ff 02 00 00 00 00 01 08 00 aa aa …` (dst bcast / src
  02:00:…:01 / EtherType 0x0800 / payload).
- **DMA TX simple-mode CSRs program correctly** — `milan_dma_tx_base` @ `0xf0003000`
  is a 64-bit **word address, MSW-first** (`base = frame_byte_addr >> 3 = 0x08002000`;
  readback `00 00 00 00 | 00 20 00 08` ✓). Extends M-A2 to the DMA register block.
- **DMA TX engine runs** — after `length=8` (64-bit words) + `enable=1`,
  `milan_dma_tx_done` = **1**: the engine read the 8 words from DDR3 and pushed them
  into `s_axis_tx`.
- **AXIS clock-domain crossing works on silicon** — done=1 means the milan-domain
  async-FIFO accepted the whole frame across the sys(100)→milan(50) boundary. First
  on-hardware proof of the `--milan-clk-freq` datapath CDC on the *data* path.
- **MAC sees a link** — `MAC_STATUS` (`0x90000110`) = `0x0d` = link_up, 1000, full-duplex
  (the hardcoded LiteEth status until MDIO lands).

## NOT confirmable here ❌ (needs rig / a fix)
- **Whether the frame actually egressed the MAC onto the RGMII.** The milan RMON TX
  counters (`0x90000210…`) stayed 0 even after a `STATS_CTRL` snapshot — but that is
  **expected and not evidence of failure**: `MilanMAC` wires `i_mac_events = 0`
  (the LiteEth MAC core doesn't expose the Forencich event set), so those counters are
  tied low regardless of egress. Confirming egress needs one of:
  1. the ProfiTap capture rig (see the frame on the wire), or
  2. a MAC TX→RX loopback (plug or PHY-internal via MDIO) + read it back via the RX DMA, or
  3. wiring LiteEth's own MAC statistics to `i_mac_events` (a real follow-up).

## Net
The **memory → DMA → AXIS-CDC → datapath** half of M-A3 is proven on silicon; the
**datapath → MAC → wire** half is untestable from the console alone (rig-gated + the
`i_mac_events` stub). RX loopback (the other half of M-A3) needs a link partner / plug.

## Update — tested against the live rig (ProfiTap ProfiShark 1G+ taps)
Rig up: `amx-pw0`/`amx-pw1` i210s (`enp6s0`), `amx-ubuntu-server` with the `pt3usb`
driver loaded + two ProfiShark 1G+ capture ifaces (`enxe8eb1b37e2c0`/`…39111a`). Armed
continuous FPGA **loop-TX** (DMA `loop=1`, `enable=1`) of the broadcast frame and
captured on both taps:
- **No FPGA frame on either tap** (`ether src 02:00:00:00:00:01` = 0 hits; only
  amx-ubuntu's own IPv6 MLD on the capture iface).
- **i210 `carrier=0 / Link detected: no`** on both ports, even with the taps active.

**Localization (definitive):** the FPGA moves the frame all the way DDR3 → DMA →
AXIS-CDC → datapath (`done=1`), but **nothing egresses onto the wire**. Because the
RTL8211E does copper auto-negotiation independently of the MAC, the i210 seeing *no
carrier at all* means the FPGA-side PHY is **not operational** — most likely held in
reset / not clocked, not merely an RGMII-data problem. The break is the last, least-
validated stage: **LiteEth `LiteEthPHYRGMII` → RGMII → RTL8211E**.

## Root cause (once the tap ports were enabled and the link came up)
With the ProfiShark ports up, `amx-pw0` i210 shows **`carrier=1, 1000Mb/s, Full`** — the
copper link negotiates. But **no data flows either way**: 250 single-shot FPGA DMA-TX
frames → i210 `rx_packets/rx_errors/rx_dropped` all **+0**; i210 broadcast bursts (ARP,
tx_packets↑) → FPGA RX-DMA `done=0`, buffer all zeros. Link up + zero data in *both*
directions = the **RGMII MAC↔PHY delay is wrong**.

`liteeth/phy/s7rgmii.py` adds **2 ns MAC-side** on both RX (IDELAYE2) and TX (125 MHz
clock at 90° = `tx_phase = 125e6·tx_delay·360`). That is correct only for a PHY in plain
**"rgmii"** (no internal delay). The design/DT target **"rgmii-id"** (PHY internal delay);
if the RTL8211E straps enable it, MAC 2 ns + PHY 2 ns = **~4 ns double delay** → RGMII data
unsampleable both ways — exactly the symptom. MDIO is un-wired so the PHY can't be
reconfigured; the fix is MAC-side: **`LiteEthPHYRGMII(tx_delay=0, rx_delay=0)`** (let the
PHY's rgmii-id delay do the work). Made a build option — `milan_soc.py
--rgmii-tx-delay/--rgmii-rx-delay` (ns).

## Breakthrough — the RGMII RX is ALIVE, just mis-sampled (delay tuning)
The LiteEth MAC exposes RX error counters (`milan_mac` @ `0xf0003800`):
`rx_datapath_preamble_errors` @ `0xf0003808`, `rx_datapath_crc_errors` @ `0xf000380c`,
`phy_crg_reset` @ `0xf0003800` (the *real* PHY reset; the milan_csr 0x11C one is a stub).
With the **`--rgmii-*-delay 0`** bitstream, driving broadcast frames from the i210:
- `phy_crg_reset` = 0 (PHY not held in reset) ✓
- **`preamble_errors` 0x06 → 0x0C** (incremented) when the i210 transmitted, `crc_errors`
  stayed 0.

⇒ **The RGMII RX clock + data path are live — frames DO reach the FPGA MAC** — but they're
sampled at the wrong point (garbled preamble, so they never get to a CRC check or the
datapath). Both 0 ns and 2 ns are wrong, so the correct IODELAY tap is **in between**.
This is a pure **RX-delay-tuning** problem now, not "is the PHY/RGMII alive".

**Efficient finish:** `s7rgmii` uses a FIXED IDELAYE2, so sweeping means one ~25-min
rebuild *per tap*. The right move is to make the RX IDELAY **VARIABLE + runtime-loadable
via a CSR** (IDELAYCTRL is already present for DDR3/RGMII) — then sweep all 32 taps on
hardware in seconds, watching `preamble_errors` drop to 0. That converts the RGMII bring-up
from an N×25-min loop into one rebuild + a fast on-board sweep. TX delay (`tx_delay`,
90° clock phase) likely needs the matching treatment. This is the concrete last step to
**M-A3 on silicon** (first packet across the NIC).
