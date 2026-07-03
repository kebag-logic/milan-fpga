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

## ROOT CAUSE (resolved): the AX7101 is GMII, not RGMII
None of the RGMII delay/inversion/nibble variants worked, and the tell was that
`preamble_errors` incremented **exactly once per frame** — a *20000-frame blast → +20000
preamble errors, 0 CRC errors, 0 captured*. That is a **structural** data corruption, not
a timing margin. Checking the Alinx vendor top (`SRC/15_ethernet_test/.../ethernet_test.v`)
settled it: it declares **`input [7:0] e_rxd`** with **separate `e_rxdv` / `e_rxer`** and
`assign e_gtxc = e_rxc` — i.e. the RTL8211E on the AX7101 is strapped for **GMII (8-bit,
single-data-rate)**, *not* RGMII (4-bit DDR). Reading a 4-bit-DDR RGMII stream off an
8-bit-SDR GMII bus corrupts every byte (RX_DV, a level, still sampled fine → frames
detected → the per-frame preamble error). All the RGMII delay/clock-invert/nibble work was
debugging the wrong interface.

**Fix:** platform eth0 rewired to the **8-bit GMII** pinout (`rx_data[0:7]` = N22 H18 H17
M21 L21 N20 M20 N19, separate `rx_dv`=M22 / `rx_er`=N18, `tx_data[0:7]`, `gtx`=G21 / `rx`=
K18 / `tx`=K21), and `MilanMAC` switched to **`LiteEthPHYGMII`** (the RGMII s7rgmii/
`milan_rgmii.py` path is retired for this board). Rebuilding all-blocks @100 MHz; retest =
i210 broadcast → FPGA GMII RX → RX-DMA → memory (expect `preamble_errors` flat + a frame in
the buffer) = **M-A3 RX on silicon**.

## RESULT — GMII PHY works: M-A3 RX proven on silicon (2026-07-03)
With the GMII bitstream (`build_gmii`, all-blocks @100 MHz, `LiteEthPHYGMII`), i210 link
1000/Full, RX-DMA armed, and a **20000-frame broadcast blast** from the i210:
- **`rx_datapath_preamble_errors` (0xf0003808) stayed at 0**  (was **+20000** on RGMII)
- **`rx_datapath_crc_errors` (0xf000380c) = 0**
- **RX-DMA `done` (0xf000302c) 0 → 1**, `offset` (0xf0003034) = 4 — a received frame
  triggered the writer and it wrote to memory.

⇒ The **RGMII→GMII root-cause fix is confirmed on silicon**: the FPGA MAC now receives the
i210's frames **cleanly** (zero preamble/CRC errors), and the full RX path
**PHY → MAC → AXIS-CDC → datapath (rx_filter) → RX-DMA** fires on a real packet. The first
packets are crossing the Milan NIC on hardware = **M-A3 RX**.

Open detail (plumbing, not the NIC): reading the *exact* captured bytes back over the BIOS
console is confounded by (a) the `milan_dma_*_base` encoding and (b) L2 cache coherency —
the DMA writes DDR3 while the CPU `mem_read` hits stale L2 (the 2 MB boot memtest region is
cached, and untouched regions read uninit). The Linux `kl-eth` driver handles this correctly
(dma_map + descriptor addresses); the raw console is a crude tool for it. Does not affect the
proven result that frames are received and DMA'd.

## TX end-to-end bring-up — DMA proven good, bug isolated to the CDC/MAC handoff (2026-07-03)

Deep dive to get a **correct TX frame onto the wire** end-to-end (memory → TX-DMA →
AXIS-CDC → datapath → LiteEth MAC → GMII → i210). Driven from the BIOS console; egress
observed on the `amx-pw0` i210 (`enp6s0`) via `rx_packets` deltas + `tcpdump`. Findings,
in the order they eliminated hypotheses:

**1. The LiteX simple-mode DMA `length` is in BYTES, not words.**
`WishboneDMAReader.add_csr()` → `_length = CSRStorage(32, "…length in bytes")`, and
`length.eq(self.length[shift:])` (shift=3 for a 64-bit bus). Writing `length=8` transmits
**one** 64-bit word, not eight. All TX programming must use `len_bytes` (e.g. 64 for a
64-byte frame). This is an ABI fact the `kl-eth` driver must honor. (Base is likewise a
**byte** address, MSW at the lower CSR word: `0xf0003000`=bits[63:32], `0xf0003004`=[31:0].)

**2. The DMA reader itself is correct — proven two ways.**
  - *Isolated Migen sim* (`scratchpad/sim_dma.py`): a 64-bit `WishboneDMAReader` →
    `wishbone.Converter` (64→32) → 32-bit `wishbone.SRAM` preloaded with a ramp, driven by
    the same simple-mode CSRs, produces **all 8 beats with correct data**. The 64→32 width
    conversion the SoC interconnect inserts is *not* the bug.
  - *On silicon, deterministic register readback* (no wire): program base+length, pulse
    `enable`, read `milan_dma_tx_done` (`0xf0003010`) and `…_offset` (`0xf0003018`):

    | source | length | `done` | `offset` |
    |--------|--------|--------|----------|
    | DRAM `0x40010000` | 64 B | **1** | **8 words** |
    | ROM  `0x00000000` | 64 B | **1** | **8 words** |
    | DRAM `0x40010000` |  8 B | **1** | **1 word** |

    The engine completes every transfer and reads the exact word count from **both** ROM and
    DRAM. So "the DMA can't read DDR3" is **false** — earlier all-zero egress was the
    length-in-bytes bug (1 word), not a dead read path.

**3. The datapath TX pipeline is byte-exact — Verilator `tb/verilator/datapath`.**
It injects 8-beat VLAN frames through `s_axis_tx` (with `tkeep=0xFF`, `tlast` on the last
beat) and checks **byte-exact egress** on `m_axis_mac_tx` through classify → CBS → PTP →
ADP-arbiter. `traffic_queues.sv` stores/forwards `tkeep` in every FIFO (`KEEP_ENABLE(1)`),
so the shaper preserves it. **Caveat found:** the harness captures egress `m_tdata` but
**never checks `m_tkeep`** — a datapath-egress keep bug would pass the TB (a real test gap).

**4. CBS is correctly bypassed.** `CBS_CTRL[0]=0` (`0x9000040c`/`…42c`/`…44c`/`…46c` = 0) is
**unshaped / strict-priority / credit forced eligible** — *not* a starved shaper. Ruled out.

**5. The symptom, pinned deterministically (i210 `rx_packets` delta, filter-independent):**
  - **single-beat** (8-byte) DMA-TX → **egresses**, but truncated — content `ff 00 00 …`,
    i.e. LiteEth `last_be` seen as `0x01` (**1 valid byte**) instead of `0xFF`/`0x80`.
  - **multi-beat** (64-byte) DMA-TX → **`rx_packets` delta = 0 over 300 frames**: the frame
    **never reaches the wire**, even though the DMA `done=1`/`offset=8`.
  - RX-DMA armed + 3000 i210 broadcast frames (raw `0x88b5`) → `done=0`, `offset=0`, target
    memory untouched, preamble/CRC = 0 (clean frames arrived, datapath forwarded none —
    consistent with the same integration break on the RX side, plus rx-filter selectivity).

**Localization (definitive).** DMA read = ✅, datapath (single-clock) = ✅, config = ✅.
The break is in the **only untested delta**: the milan-domain **AXIS clock-domain-crossing
layer** (`--milan-clk-freq 50e6` runs the datapath at 50 MHz behind five async-FIFO
`stream.ClockDomainCrossing`s + the AXI-Lite CDC — the 100 MHz timing fix) **and/or** the
`m_axis_mac_tx → core.sink.last_be` handoff in `MilanMAC` (`core.sink.last_be.eq(keep)`,
where LiteEth's `last_be` is a **one-hot pointer to the last valid byte**, not an AXIS keep
mask — `liteeth/mac/padding.py` Case). The generated CDC (`main_milan_mac_tx_dp_cdc_*`)
does carry `data/keep/first/last`, so the suspect narrows to CDC *timing/handshake under
multi-beat flow* and/or the `last_be` encoding.

**Why it can't be a no-CDC HW A/B on this board:** the post-fix datapath critical path
(~15–19 ns) needs sys ≤ ~50–66 MHz to close, but DDR3 (A7DDRPHY DLL, sys4x ≥ ~303 MHz)
needs sys ≥ ~76 MHz — the conflict the CDC was introduced to resolve. A no-CDC build must
drop to integrated SRAM at ~50 MHz (changes two variables).

### ROOT CAUSE FOUND + FIX (2026-07-03) — `tkeep`↔`last_be` encoding mismatch in `MilanMAC`

The break is the AXIS↔LiteEth byte-enable handoff in `MilanMAC` (`milan_soc.py`), *not*
the CDC. LiteEth's `last_be` is a **one-hot pointer to the last valid byte** of the final
beat (proof: `liteeth/mac/padding.py` decodes `0x01→1 byte, 0x02→2 … 0x40→7`; `mac/
last_be.py` RX builds it by up-converting a single `last` bit). AXIS `tkeep` is a
**contiguous byte mask** (`0xFF` = 8 valid). The old code wired the mask straight across:

```python
self.core.sink.last_be.eq(tx_dp.sys.keep)                 # WRONG: 0xFF mask as one-hot
rx_dp.sys.keep.eq(Mux(..last, self.core.source.last_be..)) # WRONG: one-hot as mask
```

The 64→8 TX `StrideConverter` reads `0xFF`'s **lowest** set bit → **1 valid byte**, so a
full 64-bit word egresses as a single byte (measured `ff:00:00:00:00:00`), and for a
multi-beat frame the malformed last-byte marker breaks frame termination → **nothing on
the wire** (measured `rx_packets` delta = 0). The RX side had the mirror defect (one-hot
fed where the datapath/rx-filter expect a mask), consistent with RX-DMA capturing nothing.

**Fix** (`MilanMAC`, verified in generated verilog):
```python
self.core.sink.last_be.eq(tx_dp.sys.keep & ~(tx_dp.sys.keep >> 1))            # mask -> one-hot (highest set bit)
rx_dp.sys.keep.eq(Mux(self.core.source.last, (self.core.source.last_be << 1) - 1, 2**nb - 1))  # one-hot -> mask
```
`keep=0xFF → last_be=0x80` (8 bytes); `last_be=0x08 → keep=0x0F` (4 bytes). Why the
Verilator TB missed it: `tb/verilator/datapath` checks egress `m_tdata` but **not
`m_tkeep`**, and the `last_be` mapping lives in the LiteX integration (`milan_soc.py`),
which no RTL harness covers. Follow-up: add an egress-`tkeep` assertion to
`tb/verilator/datapath`.

### CONFIRMED ON SILICON — the `last_be` fix makes frames egress (2026-07-03)

`build_gmii_lastbe` built (timing met), loaded, NIC `ID=MILN`. Driving DMA-TX of a 64-byte
frame (`length=64` **bytes**), measured on the `amx-pw0` i210 hardware counters:
- **`rx_packets` Δ = exactly the frames fired** (150→150, 300→300, 500→443-with-serial-loss)
  — **was Δ=0 for multi-beat before the fix**.
- **`rx_crc_errors`=0, `rx_errors`=0, `rx_length_errors`=0**; `rx_bytes` ≈ 64 B/frame.

⇒ **The `last_be` fix is confirmed on silicon**: multi-beat frames now leave the FPGA as
**clean, full-size, good-FCS Ethernet** — the datapath → milan-CDC → LiteEth MAC → GMII →
wire path produces valid frames. **This is the M-A3 TX breakthrough** (the "no correct
frame on the wire" blocker is resolved).

### Remaining: CPU↔DMA cache coherency (driver-scope, not the NIC)

The *content* the DMA transmits is stale — a CPU↔DMA coherency gap, proven cleanly with
the i210 counters (no capture needed):

| DMA base | DRAM there | i210 Δ`rx_packets` | meaning |
|----------|-----------|--------------------|---------|
| `0x40010000` (old test region) | stale broadcast bytes | = frame count, as **broadcast** | DMA reads committed-but-stale DRAM |
| `0x40810000` (fresh, 3× `flush_cpu_dcache`+`flush_l2_cache`) | zeros | **0** | all-zero unicast frame → i210 drops it |

The CPU reads its frame back correctly at `0x40010000` (`02 00 00 00 00 aa 02 00 …` ramp),
but the DMA transmits only what is **committed to DRAM** — and neither `flush_cpu_dcache`
(NaxRiscv `.word 0x500F`) nor `flush_l2_cache` gets the CPU's write there. NaxRiscv accesses
DRAM via a cached path that the BIOS flushes don't push through to the DMA's DRAM view.
A byte-swap of my unicast dst would still be **unicast**, but the i210 counts these as
**broadcast/multicast**, so this is **coherency, not endianness** — no further gateware fix
is needed. The `kl-eth` driver (M-A5) handles this exactly like the Zynq path
(`dma_alloc_coherent` / `dma_map_single` + `flush_dcache_range` around descriptors); the raw
BIOS console cannot. TX-DMA reads, the datapath, the `last_be` handoff, GMII RX, and now
GMII TX-egress are all proven on silicon.

**Rig note:** amx-pw0 `tcpdump` captured nothing (even self-sent outgoing frames) and the
ProfiShark taps (`amx-ubuntu-server` `enxe8eb1b3*`) were flaky, so byte-level content was
read via the i210 stats + counters instead of pcap. Capture-tooling issue, not the NIC.

## Coherent DMA + internal loopback + endianness (2026-07-03, `build_gmii_coh`/`_final`)

After the `last_be` fix landed frames on the wire, two more issues remained: the DMA read
**stale** DRAM (content wrong), and the on-wire bytes were **reversed**. Both fixed:

### (a) Cache-coherent DMA — the DMA read stale DRAM
Root cause in `naxriscv/core.py`: NaxRiscv reaches DRAM via a **direct `memory_buses` →
LiteDRAM** port, while the Milan DMA masters went through `pbus → wishbone → LiteX-L2 →
LiteDRAM` — two different paths, so CPU writes and DMA reads never shared a view (BIOS
`flush_cpu_dcache`/`flush_l2_cache` don't bridge them). **Fix:** enable NaxRiscv
`--with-coherent-dma` (exposes a cache-snooping `soc.dma_bus`) and attach the DMA masters
there (`getattr(soc, "dma_bus", soc.bus).add_master(...)`). New `milan_soc.py --coherent-dma`.

### (b) Internal MAC loopback CSR — self-contained verification
`milan_mac_loopback` (`0xf0003810`, 1 bit): feeds the datapath's MAC-TX AXIS straight back
into MAC-RX (bypassing LiteEth core + PHY), so a full frame is verifiable
`memory → TX-DMA → datapath → RX-DMA → memory` with **no wire/rig**.

**Loopback result (CONFIRMED on silicon, `build_gmii_coh`, no cache flush):** CPU wrote a
64-byte frame at `0x40010000`; RX-DMA `done=1`, `offset=8`; `0x40020000` read back
**byte-identical** (`ff ff ff ff ff ff 02 00 00 00 00 01 88 b5 00 01 02 03 …`). Proves
**coherent DMA + the entire datapath + all four AXIS CDCs, end-to-end, byte-exact, with zero
cache management.**

### (c) DMA endianness — on-wire bytes were reversed
With coherent DMA, RX frames landed in memory **byte-reversed within each 64-bit word**
(wire `ff ff ff ff ff ff 02 aa` → memory `aa 02 ff ff ff ff ff ff`). That also mangled TX:
a broadcast `ff:..:ff` egressed as `00:02:ff:..` (unicast!) so the i210 dropped every frame
(`rx_packets` Δ=0 — *not* a dead wire path; the frames egress, the dst is just scrambled).
Cause: `WishboneDMAReader/Writer` default `endianness="little"` **byte-swaps** each word
(`dma.py`: `little → with_byteswap=True`), which reverses vs LiteEth's little-endian GMII
path. The loopback stayed byte-exact only because the read-swap and write-swap cancel.
**Fix:** `endianness="big"` (no swap) on all three DMA engines — Wishbone word order == AXIS
== wire order, both directions; loopback still symmetric. Verifying in `build_gmii_final`:
loopback still byte-exact + TX broadcast counts as broadcast on the i210 + RX memory matches
wire order.
