# Milan TSN CSR  -  register map (ABI)

Memory-mapped control/status registers for the Milan TSN NIC. This is the
**stable ABI** shared by the HDL (`hdl/csr/milan_csr.sv`), the Linux driver
(`../kl-linux-drivers`), and the device tree (`reg` of the `kl,dma-ether` node).
Satisfies `REQ-CSR-05`; implements the control surface for `REQ-CSR/PTP/CBS/CLS/
MAC/*` in [`REQUIREMENTS.md`](../../REQUIREMENTS.md).

* **Bus:** AXI4-Lite, 32-bit data, little-endian. **Base is host-specific**  -  the
  register *offsets* below are fixed, only the window base differs per SoC:
  `0x43C0_0000` on the Zynq PS build, **`0x9000_0000`** on the fully-FPGA VexiiRiscv
  (formerly NaxRiscv) SoC (an MMIO peripheral must live in the CPU IO region ≥
  `0x8000_0000`; the mem-map is identical across the two cores, so the ABI is unchanged). The
  device-tree `reg` base must match the target. Window 64 KB.
* **Access:** `RO` read-only, `RW` read-write, `W1C` write-1-to-clear,
  `W1S` write-1-to-set (self-clearing command strobe), `ROc` read latches/clears.
* Unused bits read 0; writes to `RO` fields are ignored; unmapped offsets read 0
  and `SLVERR` is **not** raised (OKAY) to keep the driver simple.
* **Timing (2026-07-16 config-in-RAM read path):** plain-RW readback is served
  from a write-through shadow BRAM — reads complete one clock later than the
  original mux (AXI4-Lite handshake absorbs it; no driver change). After reset
  the block holds `*READY` low for ~513 clocks while the defaults ROM is swept
  into the shadow, so soft-reset readback values are identical to before.
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
| `0x600` | ADP advertiser (IEEE 1722.1 entity model) |
| `0x680` | lwSRP engine (802.1Q MSRP/MVRP, Milan v1.2 §5.6) |
| `0x6A4` | ACMP listener SM (Milan v1.2 §5.5, RO) |
| `0x700` | RX destination-MAC TCAM filter |

The ring-DMA engines of the fully-FPGA build have their **own** CSR space
(LiteX-generated, e.g. the `0xf000_2800`/`0xf000_3000` regions) - see the
"DMA registers" section further down; those are not part of this 64 KB
window.

### 0x000  -  Identification / IRQ

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x000` | `ID` | RO | `0x4D494C4E` | Magic `"MILN"`; driver match/probe check |
| `0x004` | `VERSION` | RO | `0x0001_0003` | `[31:16]` major, `[15:0]` minor (0x0002 ADP group, 0x0003 TCAM group) |
| `0x008` | `CAP` | RO | param | `[3:0]` num_queues, `[8]` CBS, `[9]` PTP, `[10]` STATS, `[11]` RX-filter, `[12]` ADP, `[13]` TCAM, `[14]` LWSRP, `[23:16]` ts_width |
| `0x00C` | `SCRATCH` | RW | `0` | R/W scratch (bus liveness test) |
| `0x010` | `IRQ_STATUS` | W1C | `0` | `[0]` tx_ts_ready, `[1]` link_change, `[2]` rmon_rollover |
| `0x014` | `IRQ_MASK` | RW | `0` | 1 = interrupt enabled; masked bits still visible in `IRQ_RAW` |
| `0x018` | `IRQ_RAW` | RO | `0` | Latched event bits before masking |

The PS IRQ line = `\|(IRQ_STATUS & IRQ_MASK)`.

### 0x100  -  MAC control / status  `(REQ-MAC-01..03)`

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

### 0x200  -  Statistics (RMON)  `(REQ-MAC-04)`

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

### 0x300  -  802.1Q classifier  `(REQ-CLS-01..04)`

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x300` | `CLS_CTRL` | RW | `0x1` | `[0]` use_pcp (1 = classify by PCP table, 0 = legacy EtherType), `[1]` dmac_check |
| `0x304` | `CLS_DEFAULT_PCP` | RW | `0` | `[2:0]` default port priority for untagged frames |
| `0x308` | `CLS_PCP_TC_MAP` | RW | `0xFAC688`* | PCP→traffic-class, 8×3 bits: TC of PCP `p` = `[3p+2:3p]` |
| `0x30C` | `CLS_PRIO_REGEN` | RW | `0xFAC688` (identity) | priority regeneration, 8×3 bits (ingress PCP→internal prio). Reset was `0x688FAC` until 2026-07-05  -  a half-swap (0..3↔4..7) that misrouted every tagged SR frame; fixed to identity. |
| `0x310` | `CLS_TC_QUEUE_MAP` | RW | `0xE4` | TC→queue, `N`×`ceil(log2 N)` bits (default identity `3,2,1,0`) |

\* Reset packs the Table 8-5 default PCP→TC for 4 classes; driver overwrites via
`tc mqprio`. The identity map keeps parity with the current enum ordering until
the driver programs Table 8-5 (see `REQ-CLS-04`).

### 0x400  -  802.1Qav CBS (per queue)  `(REQ-CBS-01..03)`

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
| 0 | 300 Mb/s | 456 | −1065 | 0 |
| 1 | 200 Mb/s | 304 | −1217 | 0 |
| 2 | 150 Mb/s | 228 | −1293 | 0 |
| 3 | 100 Mb/s | 152 | −1369 | 0 |

Σ idleSlope = 750 Mb/s = 75 % of the 1 Gb/s port rate (`REQ-CBS-03`); hi/lo are
`calc_hi/lo_credit(idleSlope, 1e9)` for MAX_FRAME_SIZE = 1522. **ALL queues
power up unshaped** (`CBS_EN_RST = 0b0000`): the default class map routes
untagged/BE traffic to q0, and shaping q0 at reset silently paced all
best-effort TX to ~250 Mbit/s (measured on silicon 2026-07-07, see
CBS_DEFAULT_SHAPING_BUG.md). Software opts a queue in via `CBS_CTRL[0]`
(REQ-CBS-02: SR classes only, never BE). The HW clamps credit down immediately
if a write lowers hiCredit below the current credit, so shrinking a burst
allowance takes effect at once. An `CBS_IDLE_SLOPE` write takes effect within
two slope-engine passes, at most 200 datapath cycles = 2 us at 100 MHz
(`credit_based_shaper.sv slope_engine`, sequential divider since 2026-07-11);
hiCredit/loCredit/shaped-enable act on the next cycle. The driver must keep
Σ idleSlope of the *shaped* queues ≤ 75 % of the port rate.

**Shaping applies per queue, not globally.** A frame is credit-based-shaped **only
when both** hold: (1) its PCP maps  -  through `CLS_PRIO_REGEN` → `CLS_PCP_TC_MAP` →
`CLS_TC_QUEUE_MAP`  -  to a queue, **and** (2) that queue's `CBS_CTRL[0]` shaped-enable
is **1**. A queue with `CBS_CTRL[0]=0` (or a PCP that maps to it) is **strict
priority / unshaped** (`allow_transmit` forced 1 in `credit_based_shaper.sv`). At
reset **no queue is shaped** (`CBS_EN_RST = 0b0000`, see the reset-defaults note
above). Software chooses which queues are SR/shaped (subject to the
75 % Σ idleSlope budget) by programming the PCP→queue map and the per-queue enables
together  -  e.g. `tc mqprio` + `tc cbs offload`.

### 0x500  -  PTP hardware clock  `(REQ-PTP-01..04, 06)`

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x500` | `PTP_CTRL` | RW | `0x1` | `[0]` counter enable |
| `0x504` | `PTP_INCR` | RW | `0x0800_0000` | nominal increment per tick, **Q8.24** ns: `[31:24]` integer ns, `[23:0]` fractional ns. `0x08000000` = 8.0 ns/tick @125 MHz |
| `0x508` | `PTP_ADJ` | RW | `0` | signed Q8.24-ns adjfine addend added to `PTP_INCR` each tick (rate discipline) |
| `0x510` | `PTP_TOD_WR_LO` | RW | `0` | settime target `[31:0]` (ns) |
| `0x514` | `PTP_TOD_WR_HI` | RW | `0` | settime target `[63:32]` |
| `0x518` | `PTP_OFFSET_LO` | RW | `0` | adjtime signed delta `[31:0]` |
| `0x51C` | `PTP_OFFSET_HI` | RW | `0` | adjtime signed delta `[63:32]` |
| `0x520` | `PTP_CMD` | W1S | `0` | `[0]` load (apply settime), `[1]` adjust (apply adjtime), `[2]` snapshot (latch TOD for gettime)  -  self-clearing pulses |
| `0x530` | `PTP_TOD_RD_LO` | RO | `0` | latched TOD `[31:0]` (updated when the PHC snapshot returns) |
| `0x534` | `PTP_TOD_RD_HI` | RO | `0` | latched TOD `[63:32]` |
| `0x540` | `PTP_INGRESS_LAT` | RW | `0` | ingress latency correction (ns) |
| `0x544` | `PTP_EGRESS_LAT` | RW | `0` | egress latency correction (ns) |

### 0x700  -  RX destination-MAC TCAM filter  `(REQ-MAC-02)`

A ternary CAM (`tcam.sv`) in the RX path (`rx_mac_filter`) that accepts/drops
frames by destination MAC  -  exact **or** wildcard/range (per-bit `mask`). Precise
alternative to the approximate `MC_HASH` hash filter. Software programs one indexed
entry per commit: write the KEY/MASK/ACTION shadows, then `TCAM_CMD`. Reset:
`default_pass=1` (accept-all until entries are installed  -  safe bring-up).

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x700` | `TCAM_CTRL` | RW | `0x1` | `[0]` default_pass (1 = accept frames that miss the table) |
| `0x704` | `TCAM_KEY_LO` | RW | `0` | match key `[31:0]` (dest MAC, MSB-first: byte0 in `[31:24]`? no  -  see note) |
| `0x708` | `TCAM_KEY_HI` | RW | `0` | match key `[47:32]` in `[15:0]` |
| `0x70C` | `TCAM_MASK_LO` | RW | `0` | care mask `[31:0]` (1 = compare, 0 = wildcard) |
| `0x710` | `TCAM_MASK_HI` | RW | `0` | care mask `[47:32]` in `[15:0]` |
| `0x714` | `TCAM_ACTION` | RW | `0` | `[0]` drop-on-match (else accept), `[7:1]` steer tag |
| `0x718` | `TCAM_CMD` | W1S | `0` | `[4:0]` entry index, `[8]` valid (1 = add/update, 0 = remove), `[16]` commit (self-clearing)  -  latches KEY/MASK/ACTION shadows into the entry |

The 48-bit `key`/`mask` = `{HI[15:0], LO}` and are compared MSB-first against the
destination MAC in standard notation (`01-80-C2-00-00-0E` → `0x0180C200000E`).
Whitelist: `default_pass=0` + accept entries (`ACTION[0]=0`). Blacklist:
`default_pass=1` + drop entries (`ACTION[0]=1`). Example ternary entry: reserved
multicast block `01-80-C2-00-00-0x` = key `0x0180C2000000`, mask `0xFFFFFFFFFFF0`.
See [`../hdl/common/doc/tcam.md`](../../hdl/common/doc/tcam.md).

`PTP_CMD` strobes cross into the `gtx_clk` PTP domain via `ptp_csr_sync`
(value + toggle-synchronised apply strobe, `REQ-CSR-03`). `gettime` is
asynchronous: writing `PTP_CMD[2]` pulses the snapshot command into the PHC; the
sampled TOD returns across the CDC and lands in `PTP_TOD_RD_{LO,HI}` a few cycles
later (the driver reads it after the round trip). `PTP_INCR`/`PTP_ADJ` are the
Q8.24-ns rate controls consumed by `timestamp_counter`.

### 0x600  -  ADP advertiser  `(IEEE 1722.1-2021 / Milan v1.2, FR-DISC-01..04)`

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
| `0x640` | `ADP_CMD` | W1S | `0` | `[0]` advertise-now (+ bump available_index), `[1]` depart  -  self-clearing |
| `0x644` | `ADP_STATUS` | RO | `0` | `[31:0]` available_index (owned by the advertiser; equals the value on the wire) |

The advertiser emits an 82-byte ADPDU (dst `91:E0:F0:01:00:00`, EtherType `0x22F0`,
subtype `0xFA`) merged into the MAC TX stream by `adp_tx_arbiter` between frames.
`available_index` is bumped on link-up and on `ADP_CMD[0]` (a field change), and held
on periodic re-advertise. See [`../hdl/adp/doc/adp_advertiser.md`](../../hdl/adp/doc/adp_advertiser.md).

### 0x680  -  lwSRP engine  `(802.1Q MSRP/MVRP, Milan v1.2 §5.6, FR-SRP-*)`

The fabric SRP talker endpoint (`hdl/lwsrp/KL_lwsrp_top.sv`,
[`LWSRP_FPGA_ARCHITECTURE.md`](../LWSRP_FPGA_ARCHITECTURE.md)). Re-homed here
from that doc's original 0x660 sketch (0x654-0x670 are AAF/DIAG/ACMP now).
While enabled it declares MSRP Domain (+ TalkerAdvertise when `[1]` is set)
and the MVRP VID every JoinTime, registers the bridge's Listener attribute
for our StreamID `{station MAC, 0}`, and resolves the reservation into the
AAF admission gate + the class-A CBS idleSlope (hardware mux over the 0x400
value of the queue selected in `LWSRP_CTRL[3:2]` — no CSR write-back). While
enabled it also (a) sources ACMP `listener_observed` (OR-ed with the manual
`A_ACMP_LOBS` override at 0x670) and (b) makes a reservation a PRECONDITION
for AAF transmit (`FR-SRP-03`; `AAF_CTRL[1]` bypass remains the escape hatch).

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x680` | `LWSRP_CTRL` | RW | `0xC` | `[0]` engine enable, `[1]` talker declare, `[3:2]` class-A queue for the slope mux (reset 3 = the reset PCP3→TC3→q3 map) |
| `0x684` | `LWSRP_VID` | RW | `2` | `[11:0]` SR VID (Domain + DataFrameParameters + MVRP) |
| `0x688` | `LWSRP_DMAC_LO` | RW | `0xF000_FE01` | stream dest MAC `[31:0]` (same packing as `AAF_DM*`) |
| `0x68C` | `LWSRP_DMAC_HI` | RW | `0x91E0` | stream dest MAC `[47:32]` |
| `0x690` | `LWSRP_TSPEC` | RW | `0x0001_00E0` | `[15:0]` MaxFrameSize, `[31:16]` MaxIntervalFrames (per class-A 125 µs interval) |
| `0x694` | `LWSRP_STATUS` | RO | `0` | `[1:0]` listener declaration (0 none/ignore, 1 asking-failed, 2 ready, 3 ready-failed), `[2]` listener registered, `[3]` listener ready, `[4]` talker declared, `[5]` domain ok, `[6]` reservation ACTIVE, `[7]` TSpec over the 75 % gate, `[8]` stream gate open, `[9]` slope mux engaged, `[10]` TalkerFailed seen (sticky), `[23:16]` MSRP failure code, `[31:24]` ingress FIFO frame drops |
| `0x698` | `LWSRP_SLOPE` | RO | `0` | granted idleSlope, bits/s = `MaxIntervalFrames × (MaxFrameSize+42) × 8 × 8000` |
| `0x69C` | `LWSRP_CNT` | RO | `0` | `[31:16]` MRPDUs received (post dst/EtherType filter), `[15:0]` MRPDUs sent |
| `0x6A0` | `LWSRP_LATENCY` | RW | `0` | TalkerAdvertise AccumulatedLatency, ns (constant until measured) |

MSRP frames go to `01:80:C2:00:00:0E`/`0x22EA`, MVRP to
`01:80:C2:00:00:21`/`0x88F5` (link-local, never forwarded by bridges) through
the low-rate control TX merge. `CAP[14]` advertises the group. Timers: Join
200 ms, Leave 600 ms, LeaveAll 10 s from `MILAN_CLK_FREQ_HZ`.

### 0x6A4  -  ACMP listener SM  `(Milan v1.2 §5.5 listener, FR-CONN-01)` — RO

The `KL_acmp_listener` state machine for the STREAM_INPUT[0] sink
(BIND_RX/UNBIND_RX/GET_RX_STATE + the talker-probe ladder; pipewire
acmp-milan-v12.c contract). All registers read-only; the binding is
controller-driven over ACMP.

| Offset | Register | Access | Fields |
|--------|----------|--------|--------|
| `0x6A4` | `ACMPL_STATE` | RO | `[2:0]` SM state (0 UNBOUND, 1 PRB_W_AVAIL, 2 PRB_W_DELAY, 3 PRB_W_RESP, 4 PRB_W_RESP2, 5 PRB_W_RETRY, 6 SETTLED_NO_RSV, 7 SETTLED_RSV_OK), `[3]` bound, `[4]` stream active, `[5]` Listener attr declared, `[6]` TalkerAdvertise registered, `[7]` TalkerFailed registered, `[12:8]` last ACMP status (7 = listener-talker timeout), `[14:13]` probing status (0 disabled / 1 passive / 2 active / 3 completed), `[15]` bound talker ADP-visible, `[27:16]` stream VLAN from the probe response |
| `0x6A8` | `ACMPL_TALKER_LO` | RO | bound talker entity id `[31:0]` |
| `0x6AC` | `ACMPL_TALKER_HI` | RO | bound talker entity id `[63:32]` |
| `0x6B0` | `ACMPL_CNT` | RO | `[31:16]` PROBE_TX commands sent, `[15:0]` listener commands accepted |
| `0x6B4` | `ACMPL_TUID` | RO | `[23:16]` MSRP TalkerFailed code (bound stream), `[15:0]` bound talker unique id |
| `0x6B8` | `AVTPRX_STAT` | RO | AVTP RX monitor (STREAM_INPUT[0], Milan Table 7-156): `[31:24]` STREAM_INTERRUPTED, `[23:16]` MEDIA_UNLOCKED, `[15:8]` MEDIA_LOCKED (low bytes), `[0]` media-locked level |
| `0x6BC` | `AVTPRX_FRX` | RO | STREAM_INPUT[0] FRAMES_RX (full 32-bit counter) |
| `0x6C0` | `AVTPRX_ERR` | RO | `[31:16]` SEQ_NUM_MISMATCH, `[15:8]` UNSUPPORTED_FORMAT, `[7:0]` TIMESTAMP_UNCERTAIN (low bytes/half-words) |
| `0x6C4` | `PCMRX_CNT` | RO | AAF RX depacketizer: `[31:16]` whole frames dropped (FIFO overflow), `[15:0]` PDU payloads emitted to the PCM ring |
| `0x6C8` | `PCMRX_TS` | RO | avtp_timestamp of the last ring-accepted PDU (media-clock recovery hook) |
| `0x6CC` | `MAAP_CTRL` | RW | reset `0x0800`: `[0]` en, `[1]` seed_valid, `[15:8]` block count (default 8), `[31:16]` seed offset (provisioning re-claim) |
| `0x6D0` | `MAAP_STAT0` | RO | `[31:24]` conflicts (re-address events), `[23:16]` DEFENDs sent, `[15:0]` claimed offset |
| `0x6D4` | `MAAP_STAT1` | RO | `[2]` addr_valid (= ANNOUNCE state; DMAC = 91:E0:F0:00 + offset), `[1:0]` state (0 idle / 1 probe / 2 announce) |
| `0x6D8` | `I2SPB_STAT` | RO | I2S playback drift rails: `[31:16]` underruns (silence frames), `[15:0]` overruns (pairs dropped) — measures free-running-48k drift until CRF media-clock discipline |

Timers per the reference: probe response 200 ms ×2, retry 4 s, no-talker
10 s, random pre-probe delay 0..1023 ms (LFSR).

## DMA registers (fully-FPGA build only  -  separate CSR space)

On the fully-FPGA VexiiRiscv (formerly NaxRiscv) SoC the AXIS↔memory DMA (§A.6,
`MilanDMA`) is **not** part of the `milan_csr` window above  -  its engines' registers are auto-mapped in the
**LiteX CSR space** (absolute addresses in the generated `build/csr.csv`; the device
tree exposes them via the `dma-tx`, `dma-rx`, `dma-ts` `reg` entries).

**`dma-tx` and `dma-rx` are ring engines** (2026-07-04: `RingDMAReader`/`RingDMAWriter`,
native AXI-burst masters on the coherent dma_bus  -  see
[`RX_RING_DMA.md`](../findings/RX_RING_DMA.md) for why the simple-mode/wishbone predecessors were
throughput-broken). Both share one 7-word layout over a circular coherent buffer of
frame slots `[8 B header][payload padded to 8 B]`, wrapping via `mask`:

| Offset | Register | dma-rx (writer) | dma-tx (reader) |
|--------|----------|-----------------|-----------------|
| `+0x00/+0x04` | `base` hi/lo | ring base **byte** address (64-bit, MS word first) | same |
| `+0x08` | `mask`   | ring size−1 (power of two) | same |
| `+0x0c` | `wr_ptr` | **RO**  -  HW commits a whole frame at a time | **RW**  -  SW advances after queueing a frame |
| `+0x10` | `rd_ptr` | **RW**  -  SW releases consumed bytes | **RO**  -  HW consumption pointer |
| `+0x14` | `enable` | ring enable | same |
| `+0x18` | `dropped` / `sent` | RO: whole frames dropped (ingress/ring full) | RO: frames streamed to the datapath |

Header word: RX = `{rsvd[31:0], seq[15:0], len[15:0]}` (len = padded payload bytes);
TX = `{rsvd[47:0], len[15:0]}` (len = **exact** bytes  -  HW derives the last-beat byte
mask, so TX wire frames are not 8-padded). RX `wr_ptr` only moves after the frame's
last AXI B response (software never sees a partial frame); TX HW resyncs `rd := wr`
on a nonsense header (len 0 or > 4096) instead of streaming garbage. Frame slots may
wrap the ring end  -  software splits its memcpy, hardware splits its bursts (also at
4 KB AXI boundaries). Max frame 4096 B incl. header.

**`dma-ts` remains a LiteX simple-mode engine** (mirrors Zynq `axi_dma` simple mode):

| Register | Access | Meaning |
|----------|--------|---------|
| `<eng>_base`   | RW (64-bit) | DMA buffer base **byte** address in system memory |
| `<eng>_length` | RW (32-bit) | transfer length in **bytes** |
| `<eng>_enable` | RW | 1 = arm/start the transfer |
| `<eng>_done`   | RO | 1 = transfer complete (raises the `<eng>` IRQ) |
| `<eng>_loop`   | RW | 1 = continuous (ring) mode |
| `<eng>_offset` | RO | current transfer offset (progress, in **bus words**) |

> **⚠ `base`/`length` are BYTE quantities, not words** (simple-mode: hardware-confirmed
> `length=8` transmits ONE 8-byte word; `offset` counts words). The ring pointers/masks
> are byte quantities too, always 8-aligned. (Descriptor rings / multi-queue remain the
> later Option 6b upgrade  -  see [`FULLY_FPGA_RISCV_MIGRATION.md`](../integration/FULLY_FPGA_RISCV_MIGRATION.md) §A.6.)

> **Cache-coherent DMA (no manual flushes).** Built with `milan_soc.py --coherent-dma`,
> the DMA masters attach to VexiiRiscv's (formerly NaxRiscv's) cache-snooping `dma_bus`, so
> a CPU-written TX frame is DMA-read correctly and a DMA-written RX frame is CPU-read correctly
> **without any cache maintenance**. Without it, the CPU reaches DRAM by a direct memory bus while the DMA uses
> the wishbone/L2  -  a different path, so the DMA sees stale DRAM (hardware-confirmed). The
> DMA engines use `endianness="big"` (no byte-swap) so the Wishbone/AXIS/on-wire byte order
> all match; the LiteX default `"little"` byte-swaps each word and reverses every frame.
>
> **MAC loopback**  -  `milan_mac_loopback` (`0xf0003810`, bit 0): `1` feeds the datapath's
> MAC-TX stream straight back into MAC-RX (bypassing LiteEth core + PHY), for a
> memory→TX-DMA→datapath→RX-DMA→memory self-test with no wire. `0` = normal (to the PHY).

> **⚠ Caveat  -  this DMA window uses a *different* register layout than `milan_csr`.**
> The `milan_csr` control plane (`0x9000_0000`) is a plain 32-bit AXI-Lite slave
> (offset = register; my 64-bit regs are explicit hi/lo pairs). The DMA registers live
> in the **LiteX CSR bus** (a *separate* window, `0xf000_0000` family), with
> `config_csr_data_width = 32`: each CSR is a **native-endian** 32-bit word at a 4-byte
> stride  -  plain `readl`/`writel` (verified: LiteX's `CSR_MMPTR` is
> `*(volatile uint32_t *)`, no byte-swap). So `length`/`enable`/`done`/`offset` are just
> `readl`/`writel`.
>
> The one twist is **`config_csr_ordering_big`, which is WORD order, not byte order**: a
> register wider than 32 bits is split into 32-bit words with the **most-significant word
> at the lower address**. The 64-bit `base` is therefore `base[63:32]` at `+0x0` and
> `base[31:0]` at `+0x4` (`milan_dma_tx_base` = `0xf0002800..0x2807`, `_length` at
> `0xf0002808`; matches the generated `base_read` = `read(0x2800)<<32 | read(0x2804)`).
> A native 64-bit `iowrite64`/`readq` to `base` swaps the two halves → wrong DMA address
> → silent corruption. Write it as two 32-bit words (hi @ `+0x0`, lo @ `+0x4`) or use the
> LiteX `csr.h` accessors.
>
> **On "endian":** (a) the DTB encodes all `reg`/`interrupts` cells big-endian by spec,
> but that is the blob format  -  `of_*`/`be32_to_cpu` convert it transparently and it does
> **not** change register access. (b) These CSRs are **native-endian**, so do **NOT** put
> a `big-endian` property on the node or use `ioread32be`/a BE regmap  -  that would
> byte-swap and corrupt every read. The only "big" here is the multi-word *word* order
> above. This whole caveat is LiteX-specific  -  on Zynq the DMA was a plain-MMIO `axi_dma`
> block. See also `sw/dts/README.md` and `sw/driver/README.md`.

## Notes

* All command strobes (`STATS_CTRL[0]`, `PTP_CMD[*]`) read back 0 (self-clearing).
* Multi-word 64-bit reads (TOD, MAC addr) are **not** atomic on the bus; for TOD
  use the snapshot latch, for others read hi/lo with the field stable.
* The map is versioned by `VERSION`; additive changes bump minor, breaking
  changes bump major and the driver's `of` compatible string.

### PCM ring (LiteX CSR bank, `0xf0003120`)

The AAF RX payload lands in a wrapping DRAM ring driven by a
`WishboneDMAWriter` in loop mode (same recipe as the TS record ring):
`milan_dma_pcm_base/length/enable/loop` configure it, `milan_dma_pcm_offset`
is the ring write pointer (in 64-bit words) the consumer chases. Payload is
full 64-bit words in wire byte order = S32BE interleaved PCM. Registered
after `hs_pgsz_cap` — additions-only, no existing CSR address moved
(csv-diff-verified).
