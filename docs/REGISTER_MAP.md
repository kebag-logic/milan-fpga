# Milan TSN CSR — register map (ABI)

Memory-mapped control/status registers for the Milan TSN NIC. This is the
**stable ABI** shared by the HDL (`hdl/csr/milan_csr.sv`), the Linux driver
(`../kl-linux-drivers`), and the device tree (`reg` of the `kl,dma-ether` node).
Satisfies `REQ-CSR-05`; implements the control surface for `REQ-CSR/PTP/CBS/CLS/
MAC/*` in [`REQUIREMENTS.md`](../REQUIREMENTS.md).

* **Bus:** AXI4-Lite, 32-bit data, little-endian. Base (suggested)
  `0x43C0_0000`, window 64 KB.
* **Access:** `RO` read-only, `RW` read-write, `W1C` write-1-to-clear,
  `W1S` write-1-to-set (self-clearing command strobe), `ROc` read latches/clears.
* Unused bits read 0; writes to `RO` fields are ignored; unmapped offsets read 0
  and `SLVERR` is **not** raised (OKAY) to keep the driver simple.
* `N` = `NUMBER_OF_QUEUES` (from `CAP.num_queues`, default 4).

## Register groups

| Base | Group |
|------|-------|
| `0x000` | Identification / IRQ (global) |
| `0x100` | MAC control / status |
| `0x200` | Statistics (RMON) |
| `0x300` | 802.1Q classifier |
| `0x400` | 802.1Qav CBS (per-queue, stride `0x20`) |
| `0x500` | PTP hardware clock |

### 0x000 — Identification / IRQ

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x000` | `ID` | RO | `0x4D494C4E` | Magic `"MILN"`; driver match/probe check |
| `0x004` | `VERSION` | RO | `0x0001_0003` | `[31:16]` major, `[15:0]` minor (0x0002 ADP group, 0x0003 TCAM group) |
| `0x008` | `CAP` | RO | param | `[3:0]` num_queues, `[8]` CBS, `[9]` PTP, `[10]` STATS, `[11]` RX-filter, `[12]` ADP, `[13]` TCAM, `[23:16]` ts_width |
| `0x00C` | `SCRATCH` | RW | `0` | R/W scratch (bus liveness test) |
| `0x010` | `IRQ_STATUS` | W1C | `0` | `[0]` tx_ts_ready, `[1]` link_change, `[2]` rmon_rollover |
| `0x014` | `IRQ_MASK` | RW | `0` | 1 = interrupt enabled; masked bits still visible in `IRQ_RAW` |
| `0x018` | `IRQ_RAW` | RO | `0` | Latched event bits before masking |

The PS IRQ line = `\|(IRQ_STATUS & IRQ_MASK)`.

### 0x100 — MAC control / status  `(REQ-MAC-01..03)`

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x100` | `MAC_CTRL` | RW | `0x13` | `[0]` tx_en, `[1]` rx_en, `[2]` promisc, `[3]` allmulti, `[4]` is_1g |
| `0x104` | `MAC_IFG` | RW | `0x0C` | `[7:0]` inter-frame gap (bytes), default 12 |
| `0x108` | `MAC_ADDR_LO` | RW | `0` | station MAC `[31:0]` |
| `0x10C` | `MAC_ADDR_HI` | RW | `0` | station MAC `[47:32]` in `[15:0]` |
| `0x110` | `MAC_STATUS` | RO | – | `[0]` link_up, `[2:1]` speed (0=10,1=100,2=1000), `[3]` full_duplex |
| `0x114` | `MC_HASH_LO` | RW | `0` | multicast hash filter `[31:0]` |
| `0x118` | `MC_HASH_HI` | RW | `0` | multicast hash filter `[63:32]` |
| `0x11C` | `PHY_RESET` | RW | `0x1` | `[0]` phy_reset_n (0 = hold PHY in reset) |

`MAC_CTRL` reset `0x13` = tx_en+rx_en+is_1g (preserves today's tied constants).

### 0x200 — Statistics (RMON)  `(REQ-MAC-04)`

Counters mirror `ethernet_events`. Software writes `STATS_CTRL[0]=1` to latch a
**coherent snapshot** of all counters into the read window, then reads them.

Order follows the `ethernet_events_t` enum in
`hdl/eth_event_counter/ethernet_events.svh`; `STAT`*n* is counter lane *n*
(`counts_o[n*32 +: 32]`), so the HW packing and the ABI stay 1:1.

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x200` | `STATS_CTRL` | W1S/RW | `0` | `[0]` snapshot (W1S, self-clear), `[1]` reset-counters |
| `0x210` | `STAT_TX_ERROR_UNDERFLOW` | RO | `0` | TX underflow |
| `0x214` | `STAT_TX_FIFO_OVERFLOW` | RO | `0` | TX FIFO overflow |
| `0x218` | `STAT_TX_FIFO_BAD_FRAME` | RO | `0` | TX FIFO bad frame |
| `0x21C` | `STAT_TX_FIFO_GOOD_FRAME` | RO | `0` | frames transmitted OK |
| `0x220` | `STAT_RX_ERROR_BAD_FRAME` | RO | `0` | RX bad frames |
| `0x224` | `STAT_RX_ERROR_BAD_FCS` | RO | `0` | RX FCS errors |
| `0x228` | `STAT_RX_FIFO_OVERFLOW` | RO | `0` | RX FIFO overflow |
| `0x22C` | `STAT_RX_FIFO_BAD_FRAME` | RO | `0` | RX FIFO bad frame |
| `0x230` | `STAT_RX_FIFO_GOOD_FRAME` | RO | `0` | frames received OK |

### 0x300 — 802.1Q classifier  `(REQ-CLS-01..04)`

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x300` | `CLS_CTRL` | RW | `0x1` | `[0]` use_pcp (1 = classify by PCP table, 0 = legacy EtherType), `[1]` dmac_check |
| `0x304` | `CLS_DEFAULT_PCP` | RW | `0` | `[2:0]` default port priority for untagged frames |
| `0x308` | `CLS_PCP_TC_MAP` | RW | `0xFAC688`* | PCP→traffic-class, 8×3 bits: TC of PCP `p` = `[3p+2:3p]` |
| `0x30C` | `CLS_PRIO_REGEN` | RW | `0x688FAC`* | priority regeneration, 8×3 bits (ingress PCP→internal prio) |
| `0x310` | `CLS_TC_QUEUE_MAP` | RW | `0xE4` | TC→queue, `N`×`ceil(log2 N)` bits (default identity `3,2,1,0`) |

\* Reset packs the Table 8-5 default PCP→TC for 4 classes; driver overwrites via
`tc mqprio`. The identity map keeps parity with the current enum ordering until
the driver programs Table 8-5 (see `REQ-CLS-04`).

### 0x400 — 802.1Qav CBS (per queue)  `(REQ-CBS-01..03)`

Per queue `q ∈ [0,N)` at `0x400 + q*0x20`:

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `+0x00` | `CBS_IDLE_SLOPE` | RW | see below | idleSlope, bits/s (sendSlope = idleSlope − portRate, derived in HW) |
| `+0x04` | `CBS_HI_CREDIT` | RW | see below | hiCredit, signed bytes |
| `+0x08` | `CBS_LO_CREDIT` | RW | see below | loCredit, signed bytes |
| `+0x0C` | `CBS_CTRL` | RW | q<2?1:0 | `[0]` shaped-enable (0 = strict priority, credit forced eligible) |

Reset defaults (`milan_csr` `CBS_*_RST`, mirroring `ethernet_packet_pkg.sv`):

| q | idleSlope | hiCredit | loCredit | shaped |
|---|-----------|----------|----------|--------|
| 0 | 300 Mb/s | 456 | −1065 | 1 |
| 1 | 200 Mb/s | 304 | −1217 | 1 |
| 2 | 150 Mb/s | 228 | −1293 | 0 |
| 3 | 100 Mb/s | 152 | −1369 | 0 |

Σ idleSlope = 750 Mb/s = 75 % of the 1 Gb/s port rate (`REQ-CBS-03`); hi/lo are
`calc_hi/lo_credit(idleSlope, 1e9)` for MAX_FRAME_SIZE = 1522. BE/control power
up **unshaped** (`REQ-CBS-02`). The HW clamps credit down immediately if a write
lowers hiCredit below the current credit, so shrinking a slope takes effect at
once. The driver must keep Σ idleSlope of the *shaped* queues ≤ 75 % of the port
rate.

**Shaping applies per queue, not globally.** A frame is credit-based-shaped **only
when both** hold: (1) its PCP maps — through `CLS_PRIO_REGEN` → `CLS_PCP_TC_MAP` →
`CLS_TC_QUEUE_MAP` — to a queue, **and** (2) that queue's `CBS_CTRL[0]` shaped-enable
is **1**. A queue with `CBS_CTRL[0]=0` (or a PCP that maps to it) is **strict
priority / unshaped** (`allow_transmit` forced 1 in `credit_based_shaper.sv`). At
reset **only q0 and q1 are shaped** (`CBS_EN_RST = 0b0011`); q2/q3 (best-effort,
control) run unshaped. Software chooses which queues are SR/shaped (subject to the
75 % Σ idleSlope budget) by programming the PCP→queue map and the per-queue enables
together — e.g. `tc mqprio` + `tc cbs offload`.

### 0x500 — PTP hardware clock  `(REQ-PTP-01..04, 06)`

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x500` | `PTP_CTRL` | RW | `0x1` | `[0]` counter enable |
| `0x504` | `PTP_INCR` | RW | `0x0800_0000` | nominal increment per tick, **Q8.24** ns: `[31:24]` integer ns, `[23:0]` fractional ns. `0x08000000` = 8.0 ns/tick @125 MHz |
| `0x508` | `PTP_ADJ` | RW | `0` | signed Q8.24-ns adjfine addend added to `PTP_INCR` each tick (rate discipline) |
| `0x510` | `PTP_TOD_WR_LO` | RW | `0` | settime target `[31:0]` (ns) |
| `0x514` | `PTP_TOD_WR_HI` | RW | `0` | settime target `[63:32]` |
| `0x518` | `PTP_OFFSET_LO` | RW | `0` | adjtime signed delta `[31:0]` |
| `0x51C` | `PTP_OFFSET_HI` | RW | `0` | adjtime signed delta `[63:32]` |
| `0x520` | `PTP_CMD` | W1S | `0` | `[0]` load (apply settime), `[1]` adjust (apply adjtime), `[2]` snapshot (latch TOD for gettime) — self-clearing pulses |
| `0x530` | `PTP_TOD_RD_LO` | RO | `0` | latched TOD `[31:0]` (updated when the PHC snapshot returns) |
| `0x534` | `PTP_TOD_RD_HI` | RO | `0` | latched TOD `[63:32]` |
| `0x540` | `PTP_INGRESS_LAT` | RW | `0` | ingress latency correction (ns) |
| `0x544` | `PTP_EGRESS_LAT` | RW | `0` | egress latency correction (ns) |

### 0x700 — RX destination-MAC TCAM filter  `(REQ-MAC-02)`

A ternary CAM (`tcam.sv`) in the RX path (`rx_mac_filter`) that accepts/drops
frames by destination MAC — exact **or** wildcard/range (per-bit `mask`). Precise
alternative to the approximate `MC_HASH` hash filter. Software programs one indexed
entry per commit: write the KEY/MASK/ACTION shadows, then `TCAM_CMD`. Reset:
`default_pass=1` (accept-all until entries are installed — safe bring-up).

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x700` | `TCAM_CTRL` | RW | `0x1` | `[0]` default_pass (1 = accept frames that miss the table) |
| `0x704` | `TCAM_KEY_LO` | RW | `0` | match key `[31:0]` (dest MAC, MSB-first: byte0 in `[31:24]`? no — see note) |
| `0x708` | `TCAM_KEY_HI` | RW | `0` | match key `[47:32]` in `[15:0]` |
| `0x70C` | `TCAM_MASK_LO` | RW | `0` | care mask `[31:0]` (1 = compare, 0 = wildcard) |
| `0x710` | `TCAM_MASK_HI` | RW | `0` | care mask `[47:32]` in `[15:0]` |
| `0x714` | `TCAM_ACTION` | RW | `0` | `[0]` drop-on-match (else accept), `[7:1]` steer tag |
| `0x718` | `TCAM_CMD` | W1S | `0` | `[4:0]` entry index, `[8]` valid (1 = add/update, 0 = remove), `[16]` commit (self-clearing) — latches KEY/MASK/ACTION shadows into the entry |

The 48-bit `key`/`mask` = `{HI[15:0], LO}` and are compared MSB-first against the
destination MAC in standard notation (`01-80-C2-00-00-0E` → `0x0180C200000E`).
Whitelist: `default_pass=0` + accept entries (`ACTION[0]=0`). Blacklist:
`default_pass=1` + drop entries (`ACTION[0]=1`). Example ternary entry: reserved
multicast block `01-80-C2-00-00-0x` = key `0x0180C2000000`, mask `0xFFFFFFFFFFF0`.
See [`../hdl/common/doc/tcam.md`](../hdl/common/doc/tcam.md).

`PTP_CMD` strobes cross into the `gtx_clk` PTP domain via `ptp_csr_sync`
(value + toggle-synchronised apply strobe, `REQ-CSR-03`). `gettime` is
asynchronous: writing `PTP_CMD[2]` pulses the snapshot command into the PHC; the
sampled TOD returns across the CDC and lands in `PTP_TOD_RD_{LO,HI}` a few cycles
later (the driver reads it after the round trip). `PTP_INCR`/`PTP_ADJ` are the
Q8.24-ns rate controls consumed by `timestamp_counter`.

### 0x600 — ADP advertiser  `(IEEE 1722.1-2021 / Milan v1.2, FR-DISC-01..04)`

Identity and control for the hardware ADP transmit engine (`adp_advertiser`). The
software AVDECC stack programs the entity identity here (typically mirroring the
`avdecc/milan-v12-entity.json` ENTITY descriptor); the hardware owns the advertise
timing and `available_index`. `station MAC` (source MAC / entity_id seed) comes from
`MAC_ADDR_{LO,HI}`, not this group.

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x600` | `ADP_CTRL` | RW | `0x0000_1F00` | `[0]` advertise-enable, `[12:8]` valid_time (units of 2 s; reset 31 ⇒ 62 s validity) |
| `0x604` | `ADP_ENTITY_ID_LO` | RW | `0` | entity_id `[31:0]` (EUI-64) |
| `0x608` | `ADP_ENTITY_ID_HI` | RW | `0` | entity_id `[63:32]` |
| `0x60C` | `ADP_MODEL_ID_LO` | RW | `0` | entity_model_id `[31:0]` |
| `0x610` | `ADP_MODEL_ID_HI` | RW | `0` | entity_model_id `[63:32]` |
| `0x614` | `ADP_ENTITY_CAPS` | RW | `0` | entity_capabilities (e.g. `0xC588` for a Milan PAAD) |
| `0x618` | `ADP_TALKER` | RW | `0` | `[15:0]` talker_stream_sources, `[31:16]` talker_capabilities |
| `0x61C` | `ADP_LISTENER` | RW | `0` | `[15:0]` listener_stream_sinks, `[31:16]` listener_capabilities |
| `0x620` | `ADP_CONTROLLER_CAPS` | RW | `0` | controller_capabilities |
| `0x624` | `ADP_GPTP_GM_LO` | RW | `0` | gptp_grandmaster_id `[31:0]` |
| `0x628` | `ADP_GPTP_GM_HI` | RW | `0` | gptp_grandmaster_id `[63:32]` |
| `0x62C` | `ADP_GPTP_DOMAIN` | RW | `0` | `[7:0]` gptp_domain_number |
| `0x630` | `ADP_IDX0` | RW | `0` | `[15:0]` current_configuration_index, `[31:16]` identify_control_index |
| `0x634` | `ADP_IDX1` | RW | `0` | `[15:0]` interface_index |
| `0x638` | `ADP_ASSOC_ID_LO` | RW | `0` | association_id `[31:0]` |
| `0x63C` | `ADP_ASSOC_ID_HI` | RW | `0` | association_id `[63:32]` |
| `0x640` | `ADP_CMD` | W1S | `0` | `[0]` advertise-now (+ bump available_index), `[1]` depart — self-clearing |
| `0x644` | `ADP_STATUS` | RO | `0` | `[31:0]` available_index (owned by the advertiser; equals the value on the wire) |

The advertiser emits an 82-byte ADPDU (dst `91:E0:F0:01:00:00`, EtherType `0x22F0`,
subtype `0xFA`) merged into the MAC TX stream by `adp_tx_arbiter` between frames.
`available_index` is bumped on link-up and on `ADP_CMD[0]` (a field change), and held
on periodic re-advertise. See [`../hdl/adp/doc/adp_advertiser.md`](../hdl/adp/doc/adp_advertiser.md).

## Notes

* All command strobes (`STATS_CTRL[0]`, `PTP_CMD[*]`) read back 0 (self-clearing).
* Multi-word 64-bit reads (TOD, MAC addr) are **not** atomic on the bus; for TOD
  use the snapshot latch, for others read hi/lo with the field stable.
* The map is versioned by `VERSION`; additive changes bump minor, breaking
  changes bump major and the driver's `of` compatible string.
