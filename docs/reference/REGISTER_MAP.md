# Milan TSN CSR  -  register map (ABI)

Memory-mapped control/status registers for the Milan TSN NIC. This is the
**stable ABI** shared by the HDL (`hdl/common/csr/milan_csr.sv`), the Linux driver
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
| `0x648` | AECP/ACMP status + AAF talker (flat stream-0 registers) |
| `0x680` | lwSRP engine (802.1Q MSRP/MVRP, Milan v1.2 §5.6) |
| `0x6A4` | ACMP listener SM + AVTP RX / MAAP / audio diagnostics (Milan v1.2 §5.5) |
| `0x700` | RX destination-MAC TCAM filter |
| `0x71C` | Link guard / MAC recovery (`LINK_CTRL`, `RST_EPOCH`, `LINKG_STAT` 0x774) |
| `0x724` | Identity / playback / 802.1AS overlay words |
| `0x738` | CRF media-clock sink (Milan v1.2 7.3, `KL_crf_rx`) |
| `0x750` | CRF media-clock talker (`KL_crf_tx`) |
| `0x768` | AECP GET_DYNAMIC_INFO scan forensics (BDBG) |
| `0x7A0` | ACMP bind-restore (saved-state fast-connect, Milan 5.5.3.5.2) |
| `0x7B8` | Persistence-journal ingest (**specified, not in gateware yet**) |
| `0x800` | Indexed per-stream window (NxN streams, SEL/SNAP + 0x810-0x868) |
| `0x870` | AAF per-stage latency taps (item-11, `KL_aaf_latency_taps`) |
| `0x8B4` | RX stream-parser probe (the pre-match listener view) |
| `0x8C8` | Playback chain probe (item-7: host ring -> render crossbar -> DAC) |
| `0x8F8` | MMCM-DRP media-clock servo (Milan v1.2 7.3.4) |
| `0x900` | Channel-map fabric debug window (chmap64) |

The ring-DMA engines of the fully-FPGA build have their **own** CSR space
(LiteX-generated, e.g. the `0xf000_2800`/`0xf000_3000` regions) - see the
"DMA registers" section further down; those are not part of this 64 KB
window.

### 0x000  -  Identification / IRQ

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x000` | `ID` | RO | `0x4D494C4E` | Magic `"MILN"`; driver match/probe check |
| `0x004` | `VERSION` | RO | `0x0001_000F` | `[31:16]` major, `[15:0]` minor (0x0002 ADP, 0x0003 TCAM, 0x0005 CRF talker, 0x0006 link guard, 0x0007 robustness round, 0x0008 indexed per-stream window 0x800, 0x0009 P12: window engine-backed, 0x000A saved-state fast-connect: bind-restore 0x7A0 + window 0x860-0x868, 0x000B chmap64 AEM projector + ring source + wire_chans fan-out + tdm_dout, 0x000C N-context ACMP talker responder — probes answered per uid 0..N-1 with dmac = MAAP base+uid, t>0 admission mirrors t0 term-by-term, talker-window honesty + the 0xDEADDEAD not-backed rule, LTAP same-cycle cascade, 0x000D RX stream-parser probe group 0x8B4-0x8C4 — the first pre-match listener view, 0x000E item-7 playback chain closed in fabric — render crossbar gains a host-ring source (map `SRC` bit) and `KL_i2s_feed_mux` picks the DAC source **and** its pace, plus the PBK probe group 0x8C8-0x8D0, 0x000F fabric-listener blocker fix — window sid staging is qualified by the index it was staged for, and an eviction carrying the ZERO sid is RELEASE-TO-ALIAS (entry 0 returns to the ACMP bound record at runtime)) |
| `0x008` | `CAP` | RO | param | `[3:0]` num_queues, `[8]` CBS, `[9]` PTP, `[10]` STATS, `[11]` RX-filter, `[12]` ADP, `[13]` TCAM, `[14]` LWSRP, `[23:16]` ts_width |
| `0x00C` | `SCRATCH` | RW | `0` | R/W scratch (bus liveness test) |
| `0x010` | `IRQ_STATUS` | W1C | `0` | `[0]` tx_ts_ready, `[1]` link_change, `[2]` rmon_rollover |
| `0x014` | `IRQ_MASK` | RW | `0` | 1 = interrupt enabled; masked bits still visible in `IRQ_RAW` |
| `0x018` | `IRQ_RAW` | RO | `0` | Latched event bits before masking |

The PS IRQ line = `\|(IRQ_STATUS & IRQ_MASK)`.

### 0x100  -  MAC control / status  `(REQ-MAC-01..03)`

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x100` | `MAC_CTRL` | RW | `0x13` | `[0]` tx_en, `[1]` rx_en, `[2]` promisc, `[3]` allmulti, `[4]` is_1g (only consulted when `[5]` is set), `[5]` speed_manual (0 = derive the link rate from `MAC_STATUS` speed, 1 = use `[4]` verbatim  -  REQ-MAC-03, reset 0) |
| `0x104` | `MAC_IFG` | RW | `0x0C` | `[7:0]` inter-frame gap (bytes), default 12 |
| `0x108` | `MAC_ADDR_LO` | RW | `0` | station MAC `[31:0]`  -  **LSB-first**: wire byte 0 in `[7:0]`, byte 3 in `[31:24]` (a plain `memcpy` of the 6-byte address into two LE words) |
| `0x10C` | `MAC_ADDR_HI` | RW | `0` | station MAC `[47:32]` in `[15:0]`  -  wire byte 4 in `[7:0]`, byte 5 in `[15:8]` |
| `0x110` | `MAC_STATUS` | RO | – | `[0]` link_up, `[2:1]` speed (0=10,1=100,2=1000), `[3]` full_duplex |
| `0x114` | `MC_HASH_LO` | RW | `0` | multicast hash filter, buckets 0-31 (bit `n` = bucket `n`) |
| `0x118` | `MC_HASH_HI` | RW | `0` | multicast hash filter, buckets 32-63 |
| `0x11C` | `PHY_RESET` | RW | `0x1` | `[0]` phy_reset_n (0 = hold PHY in reset) |

`MAC_CTRL` reset `0x13` = tx_en+rx_en+is_1g (preserves today's tied constants).

**Link rate (REQ-MAC-03).** The effective `is_1g` follows the MAC's reported
speed (`MAC_STATUS[2:1] == 2`) unless `MAC_CTRL[5]` is set. `MAC_CTRL[4]`'s
reset value is 1, so before 2026-07-26 a 100 Mb/s port reported gigabit to every
`is_1g` consumer until software wrote the register  -  and `is_1g` sets the lwSRP
bandwidth-gate admission limit (750 vs 75 Mb/s) and the CBS sendSlope
denominator, so a 100 Mb/s port admitted reservations against a 10x-too-large
budget. `MAC_CTRL[5]` exists to pin the rate by hand when the MAC's speed report
cannot be trusted.

**RX address filter (REQ-MAC-02).** `promisc`/`allmulti`/`MAC_ADDR_*`/`MC_HASH_*`
are consumed by `rx_mac_filter` in the RX AXIS path, but only once
`TCAM_CTRL[1]` (`addr_filter_en`, reset 0) is set  -  a build that never sets it
keeps the legacy blanket `TCAM_CTRL[0]` miss policy. Decision order per frame:

1. a 1-beat runt is always swallowed;
2. `promisc` → accept (it outranks even an explicit TCAM drop entry  -  a
   capture must see the wire, and filtering is exactly what promiscuous mode
   switches off);
3. a TCAM hit → `ACTION[0]` decides;
4. `addr_filter_en` → broadcast accepted; **group** address accepted if
   `allmulti` **or** its hash bucket is set; **unicast** accepted only on an
   exact match with `MAC_ADDR_HI/LO`;
5. otherwise `TCAM_CTRL[0]`.

**Multicast hash function.** Bucket = a 6-bit XOR fold of the 48-bit
destination MAC in standard notation, MSB-aligned groups of six bits:
`bucket = a[47:42] ^ a[41:36] ^ a[35:30] ^ a[29:24] ^ a[23:18] ^ a[17:12] ^
a[11:6] ^ a[5:0]`. `ndo_set_rx_mode` must compute the same fold (`01-80-C2-00-00-0E`
→ `0x0180C200000E` → bucket 23, i.e. `MC_HASH_LO` bit 23). The hash is approximate by design (many
addresses share a bucket); the `0x700` TCAM is the exact alternative.

### 0x200  -  Statistics (RMON)  `(REQ-MAC-04)`

Counters mirror `ethernet_events`. Software writes `STATS_CTRL[0]=1` to latch a
**coherent snapshot** of all counters into the read window, then reads them.

**Invalidate-on-MAC-reset (2026-07-22):** a MAC reinit (link-guard episode or
`LINK_CTRL[1]`) restarts the MAC path *without* a CSR-domain reset, so a
pre-reset snapshot would keep serving stale counts (the 2026-07-19
"CSR plane lies until live counters tick" forensics).

The reinit **release** edge now zeroes `STAT0..8` in hardware; all-zero means
"no valid snapshot" - software re-arms with a fresh `STATS_CTRL[0]` write.
Plain-RW config registers are unaffected (they are not MAC-domain state; the
aresetn-swept defaults ROM already covers full fabric resets).

Order follows the `ethernet_events_t` enum in
`hdl/common/eth_event_counter/ethernet_events.svh`; `STAT`*n* is counter lane *n*
(`counts_o[n*32 +: 32]`) at offset `0x210 + 4*n`, so the HW packing and the ABI
stay 1:1.

**Lane sources (2026-07-22 "RMON never worked on silicon" fix):** the good-frame
lanes (`0x21C`/`0x230`) are derived *inside* `milan_datapath` from its MAC AXIS
boundary handshake (one accepted `tlast` beat = one frame) — the matching bits
of the `i_mac_events` port are ignored, so an external MAC can never
double-count them.

The remaining lanes pass through `i_mac_events` from the external MAC; the
LiteX/LiteEth SoCs tie that port to 0 (LiteEth exposes no event pulses), so on
both boards those error/overflow lanes legitimately read 0 while the
good-frame lanes count real traffic.

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
| `0x300` | `CLS_CTRL` | RW | `0x1` | `[0]` use_pcp (1 = classify by PCP table, 0 = legacy EtherType), `[1]` dmac_check (1 = the 0x88F7 gPTP fast path also demands DMAC `01-80-C2-00-00-0E`; a spoofed 0x88F7 then falls to the PCP tables / BEST_EFFORT instead of taking the priority queue  -  REQ-CLS-07, reset 0 = today's wire behaviour) |
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
`calc_hi/lo_credit(idleSlope, 1e9)` for MAX_FRAME_SIZE = 1522.

**ALL queues power up unshaped** (`CBS_EN_RST = 0b0000`): the default class map
routes untagged/BE traffic to q0, and shaping q0 at reset silently paced all
best-effort TX to ~250 Mbit/s (measured on silicon 2026-07-07, see
[CBS_DEFAULT_SHAPING_BUG.md](../findings/CBS_DEFAULT_SHAPING_BUG.md)). Software opts a queue in via `CBS_CTRL[0]`
(REQ-CBS-02: SR classes only, never BE).

Write semantics:

* The HW clamps credit down immediately if a write lowers hiCredit below the
  current credit, so shrinking a burst allowance takes effect at once.
* An `CBS_IDLE_SLOPE` write takes effect within two slope-engine passes, at
  most 200 datapath cycles = 2 us at 100 MHz
  (`credit_based_shaper.sv slope_engine`, sequential divider since 2026-07-11);
  hiCredit/loCredit/shaped-enable act on the next cycle.
* The driver must keep Σ idleSlope of the *shaped* queues ≤ 75 % of the port
  rate.

**Shaping applies per queue, not globally.** A frame is credit-based-shaped
**only when both** hold:

1. its PCP maps  -  through `CLS_PRIO_REGEN` → `CLS_PCP_TC_MAP` →
   `CLS_TC_QUEUE_MAP`  -  to a queue, **and**
2. that queue's `CBS_CTRL[0]` shaped-enable is **1**.

A queue with `CBS_CTRL[0]=0` (or a PCP that maps to it) is **strict
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
| `0x540` | `PTP_INGRESS_LAT` | RW | `0` | ingress latency correction, ns  -  **SUBTRACTED** from every RX capture (the wire SFD preceded the AXIS SOP the tap stamps). Unsigned; the sign is fixed in HW, software never negates. |
| `0x544` | `PTP_EGRESS_LAT` | RW | `0` | egress latency correction, ns  -  **ADDED** to every TX capture (the SFD follows the AXIS SOP) |

Both reset to 0 = uncorrected. The bench currently applies its measured
constants in `ptp4l` (`ingressLatency`); move the correction to one side or the
other, **never both**, or it double-counts. These registers are the
register half of REQ-PTP-06  -  true SFD capture needs a tap at the GMII/PHY
boundary, which nothing at the AXIS boundary can synthesise, so the constants
stay characterisation-derived.

### 0x700  -  RX destination-MAC TCAM filter  `(REQ-MAC-02)`

A ternary CAM (`tcam.sv`) in the RX path (`rx_mac_filter`) that accepts/drops
frames by destination MAC  -  exact **or** wildcard/range (per-bit `mask`). Precise
alternative to the approximate `MC_HASH` hash filter. Software programs one indexed
entry per commit: write the KEY/MASK/ACTION shadows, then `TCAM_CMD`. Reset:
`default_pass=1` (accept-all until entries are installed  -  safe bring-up).

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x700` | `TCAM_CTRL` | RW | `0x1` | `[0]` default_pass (1 = accept frames that miss the table), `[1]` addr_filter_en (1 = a TCAM miss falls to the 802.3 station address filter of the `0x100` group instead of `[0]`  -  REQ-MAC-02, reset 0) |
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
See [`../hdl/ieee8021q/filtering/doc/tcam.md`](../../hdl/ieee8021q/filtering/doc/tcam.md).

### Link guard / MAC recovery (VERSION minor ≥ 0x0006)

The L1/L2 link-bounce supervisor (`hdl/common/KL_link_guard.sv`) and the daemon
recovery strobes. (Added 2026-07-23 — these were live in RTL but undocumented here,
which caused a false "0x774 = TCAM" reading; TCAM is 0x700–0x718 only.)

| Offset | Name | Acc | Reset | Fields |
|--------|------|-----|-------|--------|
| `0x71C` | `LINK_CTRL` | RW | `0` | `[0]` sw_link (daemon-tracked PHY link), `[1]` mac_reinit (hold MAC sys-side in reset), `[2]` linkg_dis (1 = guard disabled), `[3]` linkg_freeze (test hook: fake eth clock death → drills the full FSM with no cable) |
| `0x720` | `RST_EPOCH` | RO | `0` | datapath reset-release count — the shadow-lie canary (a live tick proves a real reset happened, e.g. so a CSR-wipe is not mistaken for an unbind) |
| `0x774` | `LINKG_STAT` | RO | — | `KL_link_guard` `stat_o`: `[31:16]` bounce_cnt (saturating), `[9]` freeze, `[8]` dis, `[7]` act_recent (RX seen ~1.3 s), `[6]` guard_rst (reinit held), `[5:4]` state (0 RUN, 1 HOLD, 2 SETTLE), `[2]` eth_rst (sequenced eth-CDC reset, minor ≥ 0x0007), `[1]` tx_alive, `[0]` rx_alive |

`PTP_CMD` strobes cross into the `gtx_clk` PTP domain via `ptp_csr_sync`
(value + toggle-synchronised apply strobe, `REQ-CSR-03`). `gettime` is
asynchronous: writing `PTP_CMD[2]` pulses the snapshot command into the PHC; the
sampled TOD returns across the CDC and lands in `PTP_TOD_RD_{LO,HI}` a few cycles
later (the driver reads it after the round trip). `PTP_INCR`/`PTP_ADJ` are the
Q8.24-ns rate controls consumed by `timestamp_counter`.

### 0x724  -  identity / playback / 802.1AS overlay

Software-published overlay words: the softcore daemons write board identity
and live gPTP topology here so the fabric ADP/AEM engines answer with wire
truth ([`../design/TIME_SYNC.md`](../design/TIME_SYNC.md) §2.5).

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x724` | `ENT_NAME_LO` | RW | `0` | entity_name chars 0-3, `[7:0]` = char 0 (board-name overlay; all-zero = keep the ROM name) |
| `0x728` | `ENT_NAME_HI` | RW | `0` | entity_name chars 4-7 |
| `0x72C` | `LPF_CTRL` | RW | `0x1` | `[0]` playback biquad LPF enable (`KL_pcm_lpf`), on by default |
| `0x730` | `AS2_LO` | RW | `0` | 802.1AS parent bridge clockIdentity `[31:0]` |
| `0x734` | `AS2_HI` | RW | `0` | parent bridge clockIdentity `[63:32]`; 0 = none/unknown. Daemon-written from the gPTP PARENT_DATA_SET; the AEM AVB_INTERFACE overlay answers AS_PATH = [GM, parent bridge] from it |

### 0x738  -  CRF media-clock sink  `(Milan v1.2 7.3, KL_crf_rx)`

The measurement half of the CRF clock-recovery loop: `KL_crf_rx` validates
every PDU of the followed CRF stream against the Milan 7.3.2 profile
constants and produces the servo's phase/frequency inputs; the MMCM-DRP
actuator status lives at `0x8F8`. Loop semantics + RTL citations:
[`../design/TIME_SYNC.md`](../design/TIME_SYNC.md) §3.3-3.4.

The followed stream normally comes from the CRF sink bind (ACMP listener
sink 1 — the bind wins); the SID pair here is the manual lever, and the
bind-restore group notes that this sink re-arms via `0x738`.

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x738` | `CRF_CTRL` | RW/RO | `0` | `[0]` CRF sink enable (RW); `[31]` locked (RO live: 8 clean consecutive PDUs to lock, 100 ms silence or a validation error to unlock) |
| `0x73C` | `CRF_SIDLO` | RW | `0` | followed CRF stream_id `[31:0]` |
| `0x740` | `CRF_SIDHI` | RW | `0` | stream_id `[63:32]` |
| `0x744` | `CRF_DELTA` | RO | `0` | signed `crf_ts - ptp_now` (ns) at each accepted PDU — phase, same signed-delta contract as `AVTPRX_TSD` (0x6EC); carries the talker+transit constant, deliberately NOT a servo input |
| `0x748` | `CRF_RATE` | RO | `0` | signed ns error per 512 ms window (256-PDU ring): the talker's media clock measured against gPTP — the servo frequency input (1 ppm = 512 units) |
| `0x74C` | `CRF_STATUS` | RO | `0` | `[31:16]` PDUs accepted, `[15:8]` format errors (7.3.2 pull/base/dlen/interval/type check), `[7:0]` sequence errors |

### 0x750  -  CRF media-clock talker  `(Milan v1.2 7.3.1, KL_crf_tx)`

Emits the CRF AUDIO_SAMPLE stream (subtype 4, pull 0, base_frequency 48000,
timestamp_interval 96 ⇒ 500 PDU/s), timestamped from the real audio-MMCM
sample grid: every 96th `/512` sample event latches the live PHC value, so
the wire carries the actual audio-clock rate as the PHC sees it. A PDU that
would collide with a busy serializer is skipped whole — timestamps stay
truthful, only the cadence stretches
([`../design/TIME_SYNC.md`](../design/TIME_SYNC.md) §3.2).

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x750` | `CRFT_CTRL` | RW | `0` | `[0]` CRF talker enable |
| `0x754` | `CRFT_SIDLO` | RW | `0` | CRF talker stream_id `[31:0]`. **Reset 0 = AUTO (since VERSION `0x0010`, `N_STREAMS > 1` builds only):** the fabric uses `{station MAC, N_STREAMS}` — exactly the stream_id the ACMP talker responder answers with for `talker_unique_id = N_STREAMS`, the CRF Media Clock Output context ([NXN_ARCHITECTURE.md](../NXN_ARCHITECTURE.md) §3.5). A non-zero pair wins outright (static provisioning, unchanged) |
| `0x758` | `CRFT_SIDHI` | RW | `0` | stream_id `[63:32]`, same AUTO rule (the pair is tested together) |
| `0x75C` | `CRFT_DMLO` | RW | `0` | CRF stream dest MAC `[31:0]` (same packing as `AAF_DM*`). **Reset 0 = AUTO:** the MAAP block slot `base + N_STREAMS`, one past the audio talkers — so `MAAP_CTRL`'s claimed count must be `N_STREAMS+1`. A non-zero pair wins outright |
| `0x760` | `CRFT_DMHI` | RW | `0` | dest MAC `[47:32]` in `[15:0]`, same AUTO rule |
| `0x764` | `CRFT_COUNT` | RO | `0` | CRF PDUs emitted |

### 0x768  -  AECP GET_DYNAMIC_INFO scan forensics (BDBG)

Three RO words latched at each record verdict of the `0x4B`
GET_DYNAMIC_INFO batch scanner in `KL_aecp_response_builder`
(descriptor-read debugging).

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x768` | `BDBG0` | RO | `0` | the four record-header bytes as scanned `{dlen_hi, dlen_lo, cmd_hi, cmd_lo}` |
| `0x76C` | `BDBG1` | RO | `0` | `[30:16]` record command_type, `[15:0]` record data length, at the verdict |
| `0x770` | `BDBG2` | RO | `0` | `[24:16]` scan pointer, `[8:0]` payload end (bytes) |

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

`available_index` increments on EVERY transmitted ADPDU — periodic re-advertise,
discover response and departing alike (`adp_advertiser.sv` serialiser: controllers
treat a repeated index as an incoherent entity; bump-on-change-only was
silicon-diagnosed 2026-07-12).

A frozen `ADP_STATUS` therefore means no ADPDUs are leaving at all — the
[`ADP_DORMANCY.md`](../findings/ADP_DORMANCY.md) incident signature. See
[`../hdl/ieee17221/adp/doc/adp_advertiser.md`](../../hdl/ieee17221/adp/doc/adp_advertiser.md).

### 0x648  -  AECP/ACMP status + AAF talker  `(IEEE 1722.1 / Milan v1.2)`

Read-only counters from the AECP/AEM listener (`KL_aecp_top`) and the ACMP
responder, the legacy flat AAF talker configuration for stream 0 (talker
index 0 of the 0x800 window is a hard alias of these — see the alias rule
there), the ADP dormancy diagnostics and the Milan talker SM view. Stream
semantics: [`../design/AUDIO_STREAMING.md`](../design/AUDIO_STREAMING.md).

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x648` | `AECP_STAT0` | RO | `0` | `[16]` entity locked (a controller holds LOCK_ENTITY), `[15:0]` AECP commands accepted |
| `0x64C` | `AECP_STAT1` | RO | `0` | `[31:16]` AECP responses sent, `[15:0]` live current_configuration_index |
| `0x650` | `ACMP_STAT` | RO | `0` | ACMP responder: `[31:16]` responses sent, `[15:0]` commands accepted |
| `0x654` | `AAF_CTRL` | RW | `0x0002_0002` | `[0]` talker enable, `[1]` gate bypass (1 = stream whenever enabled — legacy default until the probe path is silicon-proven; 0 = Milan probe-gated), `[27:16]` SR VID (reset 2). Write bit-preserving — `0x0002_0003` to enable; a bare `0x3` zeroes the VID, and VID-0 frames leave the reserved SR tree (bridges strip the tag on egress) and flood unshaped |
| `0x658` | `AAF_DMLO` | RW | `0xF000_FE01` | AAF stream dest MAC `[31:0]` (reset = MAAP-range `91:E0:F0:00:FE:01`). Fallback value: while `MAAP_CTRL[0]` is set and `MAAP_STAT1[2]` addr_valid, the datapath streams to the MAAP-claimed DMAC instead (`eff_aaf_dmac` mux) |
| `0x65C` | `AAF_DMHI` | RW | `0x91E0` | dest MAC `[47:32]` in `[15:0]` |
| `0x660` | `AAF_FRAMES` | RO | `0` | AAF frames sent (the window `PDUS` word latches this at talker idx 0) |
| `0x664` | `AAF_PAIRS` | RO | `0` | I2S sample pairs captured by the talker front-end |
| `0x668` | `ADP_DIAG` | RO | `0` | ADP dormancy forensics: `[7:0]` depart events taken, `[15:8]` dormancy self-re-arms, `[17:16]` last depart cause `{shutdown, link_down}`. rearm_cnt ticking while depart_cnt holds = a state upset, not a commanded depart ([`ADP_DORMANCY.md`](../findings/ADP_DORMANCY.md)) |
| `0x66C` | `ACMP_TALKER` | RO | `0` | Milan talker SM: `[0]` probe_armed (PROBE_TX activation), `[1]` talker_active, `[2]` mirror of the `ACMP_LOBS[0]` manual override (the SM's effective listener_observed additionally ORs the lwSRP term in the datapath), `[3]` resolved AAF admission gate |
| `0x670` | `ACMP_LOBS` | RW | `0` | `[0]` manual listener_observed override — OR-ed with the lwSRP-sourced listener_observed (the lwSRP socket, see the 0x680 group) |

### 0x680  -  lwSRP engine  `(802.1Q MSRP/MVRP, Milan v1.2 §5.6, FR-SRP-*)`

The fabric SRP talker endpoint (`hdl/ieee8021q/srp/KL_lwsrp_top.sv`,
[`LWSRP_FPGA_ARCHITECTURE.md`](../LWSRP_FPGA_ARCHITECTURE.md)). Re-homed here
from that doc's original 0x660 sketch (0x654-0x670 are AAF/DIAG/ACMP now).

While enabled it declares MSRP Domain (+ TalkerAdvertise when `[1]` is set)
and the MVRP VID every JoinTime, registers the bridge's Listener attribute
for our StreamID `{station MAC, 0}`, and resolves the reservation into the
AAF admission gate + the class-A CBS idleSlope (hardware mux over the 0x400
value of the queue selected in `LWSRP_CTRL[3:2]` — no CSR write-back).

While enabled it also:

* sources ACMP `listener_observed` (OR-ed with the manual `A_ACMP_LOBS`
  override at 0x670), and
* makes a reservation a PRECONDITION for AAF transmit (`FR-SRP-03`;
  `AAF_CTRL[1]` bypass remains the escape hatch).

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x680` | `LWSRP_CTRL` | RW | `0xC` | `[0]` engine enable, `[1]` talker declare, `[3:2]` class-A queue for the slope mux (reset 3 = the reset PCP3→TC3→q3 map) |
| `0x684` | `LWSRP_VID` | RW | `2` | `[11:0]` SR VID (Domain + DataFrameParameters + MVRP) |
| `0x688` | `LWSRP_DMAC_LO` | RW | `0xF000_FE01` | stream dest MAC `[31:0]` (same packing as `AAF_DM*`) |
| `0x68C` | `LWSRP_DMAC_HI` | RW | `0x91E0` | stream dest MAC `[47:32]` |
| `0x690` | `LWSRP_TSPEC` | RW | `0x0001_00E0` | `[15:0]` MaxFrameSize, `[31:16]` MaxIntervalFrames (per class-A 125 µs interval). **Scope (since VERSION `0x0010`): this word serves the LEGACY row 0 and every listener context row only.** A talker context row at `0x800` window idx>0 derives its own MaxFrameSize from that stream's TCTX w0 `chans` — `24 + 24*C`, the AAF-PCM32 MSDU the packetizer actually frames — so a 2ch and an 8ch talker no longer reserve identically ([NXN_ARCHITECTURE.md](../NXN_ARCHITECTURE.md) §3.4.2). `MaxIntervalFrames` stays shared: it is an SR-class property |
| `0x694` | `LWSRP_STATUS` | RO | `0` | `[1:0]` listener declaration (0 none/ignore, 1 asking-failed, 2 ready, 3 ready-failed), `[2]` listener registered, `[3]` listener ready, `[4]` talker declared, `[5]` domain ok, `[6]` reservation ACTIVE, `[7]` TSpec over the 75 % gate, `[8]` stream gate open, `[9]` slope mux engaged, `[10]` TalkerFailed seen (sticky), `[11]` **attribute-row shortfall (sticky, since VERSION `0x0010`)**: a `0x800` provisioning request named a context row this build does not have (`ctx_idx >= KL_lwsrp_top.N_CTX_P`). Reads 0 on a correctly-sized engine; a 1 means the shape needs more than the elaborated `L+T-1` rows and the surplus reservations are being dropped — the ONLY software-visible symptom, since a refused row moves no counter anywhere else. `[15:12]` reserved 0, `[23:16]` MSRP failure code, `[31:24]` ingress FIFO frame drops |
| `0x698` | `LWSRP_SLOPE` | RO | `0` | granted idleSlope, bits/s = `MaxIntervalFrames × (MaxFrameSize+42) × 8 × 8000` |
| `0x69C` | `LWSRP_CNT` | RO | `0` | `[31:16]` MRPDUs received (post dst/EtherType filter), `[15:0]` MRPDUs sent |
| `0x6A0` | `LWSRP_LATENCY` | RW | `0` | TalkerAdvertise AccumulatedLatency, ns (constant until measured) |

MSRP frames go to `01:80:C2:00:00:0E`/`0x22EA`, MVRP to
`01:80:C2:00:00:21`/`0x88F5` (link-local, never forwarded by bridges) through
the low-rate control TX merge. `CAP[14]` advertises the group. Timers: Join
200 ms, Leave 600 ms, LeaveAll 10 s from `MILAN_CLK_FREQ_HZ`.

### 0x6A4  -  ACMP listener SM  `(Milan v1.2 §5.5 listener, FR-CONN-01)`

The `KL_acmp_listener` state machine for the STREAM_INPUT[0] sink
(BIND_RX/UNBIND_RX/GET_RX_STATE + the talker-probe ladder; pipewire
acmp-milan-v12.c contract). The SM/monitor registers are read-only — the
binding is controller-driven over ACMP; the group tail carries the RW
MAAP/tone/pdelay knobs.

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
| `0x6D8` | `I2SPB_STAT` | RO/W1C | I2S playback drift rails: `[31:16]` underruns (silence frames), `[15:0]` overruns (pairs dropped) — measures free-running-48k drift until CRF media-clock discipline. Both rails saturate at `0xFFFF`; **W1C per half (2026-07-22, gaps 5b)**: a write with any bit of a half set restarts that half's counter (the other half is untouched; a zero write is inert; readback stays the live count). W1C was chosen over clear-on-bind: the rails are engine diagnostics, not Milan Table 5.6 stream counters — a bind-triggered clear would erase evidence mid-diagnosis and add a bind-path dependency, while W1C leaves the observation window entirely under software control |
| `0x6DC` | `TONE_CTRL` | RW | `[0]` pilot tone: 1 kHz 0 dBFS exact-period 48×24-bit sine replaces the I2S ADC on both talker channels (digital THD+N −148.1 dB; E2E acceptance ≤ −120 dBFS via `tone_thdn.py` on the listener ring dump) |
| `0x6E0` | `I2SPB_TRIM` | RO | media-clock recovery servo: `[31:16]` signed NCO trim (LSB ≈ 15.3 ppm; fill-level servo steers playback rate to the talker), `[15:0]` FIFO fill (pairs). Rail events count MEDIA_RESET |
| `0x6E4` | `GPTP_PDELAY` | RW | reset `0`: measured gPTP neighbor propagation delay, ns — written by the softcore gPTP daemon, served back through the AEM AVB_INTERFACE overlay ([`../design/TIME_SYNC.md`](../design/TIME_SYNC.md) §2.5) |
| `0x6E8` | `ACMPL_DBG` | RO | listener walker forensics: `[31:24]` CLASSIFY entries (any frame), `[23:16]` ACMP-subtype (0xFC) classifies, `[15:8]` flags at the last ACMP classify `{dst_ok, etype_ok, sv0, len_ok, ovfl, lstnr_hi_ok, lstnr_lo_ok, is_lstn_cmd}`, `[7:0]` ACMP-base + listener-command hits |
| `0x6EC` | `AVTPRX_TSD` | RO | signed ts_delta = `avtp_timestamp - ptp_now` (ns) at the last accepted STREAM_INPUT[0] PDU — the stream-sync error signal (LATE counts when delta < 0, EARLY beyond offset + margin; [`../design/TIME_SYNC.md`](../design/TIME_SYNC.md) §3.6) |
| `0x6F0` | `I2SPB_DBG` | RO | DAC-serial forensics: the exact 32 serial bits of the last LEFT half-frame as sent at the DAC pin (CDC-latched) |

Timers per the reference: probe response 200 ms ×2, retry 4 s, no-talker
10 s, random pre-probe delay 0..1023 ms (LFSR).

### 0x7A0  -  ACMP bind-restore  `(saved-state fast-connect E1, Milan 5.5.3.5.2)`

Boot-time re-injection of a listener bind saved in non-volatile memory - the
journal record format, the QSPI slot map, the torn-write contract and the boot
replay sequence are in
[`../design/SAVED_STATE_FASTCONNECT.md`](../design/SAVED_STATE_FASTCONNECT.md).

Software stages the persisted binding parameters (5.5.2.4 + 5.5.3.5.3:
talker_entity_id, talker_unique_id, controller_entity_id, flags) and
commits; the fabric writes the Milan 5.5.3.5.2 ENTRY record into the ACMP
listener context table — state `PRB_W_AVAIL`, probing_status `PASSIVE`,
ACMP status 0, and the SRP stream parameters (stream_id / dest MAC / VLAN)
**cleared** per 5.5.2.6 step 1.

No new connection logic: the existing fabric ladder (ADP talker watch ->
TMR_DELAY -> PROBE_TX ladder) takes over, so the sink waits for the talker's
ENTITY_AVAILABLE (5.5.1.4) and re-probes exactly like a power-on
fast-connect. Software gate: VERSION >= `0x000A` **and** a write/readback
probe of `0x7A0` (pattern `0xA5C35A3C`).

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x7A0` | `REST_TK_LO` | RW | `0` | saved talker_entity_id `[31:0]` (doubles as the feature probe word) |
| `0x7A4` | `REST_TK_HI` | RW | `0` | saved talker_entity_id `[63:32]` |
| `0x7A8` | `REST_META` | RW | `0` | `[15:0]` talker_unique_id; `[27:16]` saved VLAN — informational only, **ignored on load** (5.5.2.6 step 1 re-probes it) |
| `0x7AC` | `REST_CTLR_LO` | RW | `0` | saved controller_entity_id `[31:0]` |
| `0x7B0` | `REST_CTLR_HI` | RW | `0` | saved controller_entity_id `[63:32]` |
| `0x7B4` | `REST_CMD` | W1S / RO | `0` | Write: `[31]` commit (accepted only while idle), `[23:8]` binding flags (bit 3 = STREAMING_WAIT), `[3:0]` target sink index (listener_unique_id). Read (live): `[31]` busy (commit in flight), `[30]` done (a commit completed since reset), `[9:8]` status of the last commit — `0` injected, `1` refused: target context OCCUPIED (not `LSM_UNBOUND_S`; record untouched), `2` refused: bad index (>= N sinks, or a record-only context without the probe SM — the CRF sink re-arms via `0x738`), `[3:0]` last committed index |

The commit is refused rather than merged when the context is already bound
(5.5.1.2: only a controller changes a bound state) — `acmp-persist` treats
status 1/2 as "leave the fabric alone". With no engine attached (TB ties)
a commit stays busy forever; the VERSION + probe gate prevents software
from ever committing on such gateware.

### 0x7B8  -  Persistence-journal ingest  `(saved-state fast-connect E3)`

> **NOT IN GATEWARE YET.** The RTL
> ([`../../hdl/ieee17221/aecp/KL_persist_journal.sv`](../../hdl/ieee17221/aecp/KL_persist_journal.sv))
> and this ABI are Verilator-gated by `tb/verilator/persist` (96 checks), whose
> `persist_wrap.sv` carries the decode below as an executable spec; `milan_csr`
> has not been wired to it. Until it is, `0x7BC` writes go nowhere and `0x7C0`
> reads `0` - which is indistinguishable from "idle, no verdict", so software
> **must** gate on `VERSION` and not on a read of this group. Design record:
> [`../design/SAVED_STATE_FASTCONNECT.md`](../design/SAVED_STATE_FASTCONNECT.md) §8.

Software pushes ONE journal slot image (32-bit little-endian words, verbatim
from flash) through this port. The fabric verifies magic / format major / shape
/ length / CRC-32 / owning `entity_id` / `SEQ` monotonicity and only THEN issues
the E1 bind-restore transactions above - one per journal record. **A torn,
truncated, foreign or stale image produces ZERO restores**: the CRC-32 trailer
is the last word of the image, so a half-applied context table is not
representable, not merely avoided.

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x7B8` | `JNL_CTRL` | W1S / RO | `0` | Write: `[0]` start a slot image, `[1]` image complete -> verify (+ replay), `[2]` abort back to idle. Read (live): `[31]` busy, `[30]` done (a verdict produced since reset) |
| `0x7BC` | `JNL_DATA` | WO | - | next 32-bit journal word, little-endian exactly as read from flash. Reads `0` |
| `0x7C0` | `JNL_STAT` | RO | `0` | `[2:0]` state (0 idle, 1 load, 2 verify, 3/4/5 replay, 6 done), `[7:4]` verdict, `[11:8]` records in the accepted image, `[15:12]` records the ACMP engine injected, `[23:16]` per-record refusal bitmap (bit r = record r came back with a nonzero E1 status), `[30]` done, `[31]` busy |
| `0x7C4` | `JNL_SEQ` | RO | `0` | `SEQ` of the last **accepted** image; 0 = none accepted this boot. A rejected image never advances it, which is what makes the A/B fall-back to an older intact slot admissible |

Verdicts in `0x7C0[7:4]`: `0` none · `1` ACCEPT · `2` MAGIC (not a journal slot,
or an erased one) · `3` VERSION (format major this build cannot read) · `4`
SHAPE (`rec_words` != 6, or `n_rec` 0 / above capacity) · `5` LENGTH (truncated
or overlong transfer) · `6` CRC (**torn write / bit rot**) · `7` ENTITY (journal
belongs to another `entity_id` - a cloned rootfs) · `8` STALE (`SEQ` does not
beat the accepted watermark).

Structural verdicts are ordered before the CRC so an operator gets a naming
diagnosis (an erased slot reads as MAGIC, not CRC), but nothing that is
**trusted for action** - the entity id, the `SEQ` watermark, any record word -
is consulted until the CRC has closed.

### 0x800  -  Indexed per-stream window  `(NxN streams, [NXN_ARCHITECTURE.md](../NXN_ARCHITECTURE.md) §1.5)`

One SELECT register plus ONE decoded word block views any of the N listener /
N talker stream contexts — decode area is O(1) in N instead of the O(N) flat
replication (~500 words at 8x8). The reader is the single softcore daemon:
SEL-then-read sequencing costs nothing. `N_LISTENERS_P` / `N_TALKERS_P` are
elaboration parameters of `milan_csr` (both 1 in today's shipping shape).

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x800` | `A_STRM_SEL` | RW | `0` | `[3:0]` stream index, `[8]` dir (0 = listener, 1 = talker). Only these bits are stored/read back. Writing SEL invalidates the ACMP/SRP read snapshots (they re-poll for the new selection). **Until a re-poll lands, the snapshot-served words read literal `0`** — a listener `SID`/`DMAC` of 0 right after a SEL write means "not fresh yet", NOT "no bind" (and on a running board a persistence daemon may be moving SEL in its own loop: read until a value repeats — [TROUBLESHOOTING §21](../limitations/TROUBLESHOOTING.md)) |
| `0x804` | `A_STRM_SNAP` | W1S / RO | `0` | Write `[0]`=1: latch the selected stream's `STATE` + `CNT0..9` + `PDUS` into the window shadow as ONE coherent block. Read: `[0]` busy. Poll busy=0 before reading the latched words |
| `0x810` | `A_STRMW_CTRL` | RW | — | listener: `[0]` en, `[2:1]` route FLAGS `{[2] RENDER, [1] DMA}` — independently combinable, see the route paragraph below (LCTX w4, engine-backed); talker idx 0: `[0]` en = **hard alias of `AAF_CTRL[0]`** (merge write — VID/bypass bits untouched); talker idx>0: TCTX w0 (`[0]` en arms the stream — the per-stream admission composition, see the talker t>0 paragraph). A CTRL write at idx>0 also COMMITS the lwSRP provisioning record (see below). **Staging rule (VERSION ≥ `0x000F`): a CTRL commit overrides the stream table only when a stream_id was staged FOR THIS INDEX** via `A_STRMW_SID_LO/HI` — staging for one index then committing another no longer arms the second with the first's sid. **`[0]`=0 with no sid staged for this index is RELEASE-TO-ALIAS**: it commits the zero sid, which disarms the override so entry 0 returns to the live ACMP bound record. An eviction that *does* carry a staged sid is a deliberate disable and keeps the override armed |
| `0x814` | `A_STRMW_SID_LO` | RW/RO | — | stream_id `[31:0]`. listener: RO from the ACMP bind context (tbl port); talker idx 0: RO derived `{station MAC, uid=0}`; talker idx>0: RO from the lwSRP row snapshot. Writes stage the provisioning sid (and forward to LCTX w0 for listeners) |
| `0x818` | `A_STRMW_SID_HI` | RW/RO | — | stream_id `[63:32]`, same rules (LCTX w1) |
| `0x81C` | `A_STRMW_DMAC_LO` | RW/RO | — | stream DMAC `[31:0]`. listener: RO ACMP bind context; talker idx 0: **hard alias of `AAF_DMLO`** (RW, exact); talker idx>0: TCTX w1 (engine-backed). Writes stage the provisioning DMAC |
| `0x820` | `A_STRMW_DMAC_HI` | RW/RO | — | DMAC `[47:32]` in `[15:0]`; talker idx 0 = **hard alias of `AAF_DMHI`**; talker idx>0: TCTX w2 |
| `0x824` | `A_STRMW_FMT_LO` | RW | — | current stream format `[31:0]` (LCTX w2, engine-backed; talker side is AECP-owned — reads `0xDEADDEAD`, writes ignored) |
| `0x828` | `A_STRMW_FMT_HI` | RW | — | format `[63:32]` (LCTX w3; talker side reads `0xDEADDEAD`) |
| `0x82C` | `A_STRMW_STATE` | RO snap | `0` | Snap-latched pack. listener: `[2:0]` ACMP lsm state, `[4:3]` probing, `[9:5]` acmp_status, `[10]` media_locked, `[18:11]` wire_chans, `[27:19]` SRP bits (= low 9 bits of `A_STRMW_SRP`). talker (LIVE per-stream since 0x000C — bits `[3:0]` at idx>0 were hardwired 0 before, the 2026-07-26 window-honesty fix): `[0]` probe_armed, `[1]` talker_active, `[2]` lobs, `[3]` composed admission (`aaf_stream_en[idx]`; idx 0 = `aaf_gate`), `[27:19]` SRP bits |
| `0x830`-`0x854` | `A_STRMW_CNT0..9` | RO snap | `0` | The 10 Milan Table 5.6 / 1722.1-2021 Table 7-157 STREAM_INPUT counters at the Table 7-157 word offsets 0..36: MEDIA_LOCKED, MEDIA_UNLOCKED, STREAM_INTERRUPTED, SEQ_NUM_MISMATCH, MEDIA_RESET, TIMESTAMP_UNCERTAIN, UNSUPPORTED_FORMAT, LATE_TIMESTAMP, EARLY_TIMESTAMP, FRAMES_RX. Talker contexts read `0xDEADDEAD` (the not-backed rule below) |
| `0x858` | `A_STRMW_PDUS` | RO snap | `0` | listener: `{drops[31:16], pdus[15:0]}` (= `PCMRX_CNT` at idx 0); talker: per-stream frames_sent (idx 0 = `AAF_FRAMES`; idx>0 = the packetizer ctx FRAMES word, snap-fetched through the TCTX port) |
| `0x85C` | `A_STRMW_SRP` | RO | — | per-stream lwSRP attribute status. idx 0: **live hard alias of `LWSRP_STATUS` (0x694)**. idx>0: `{16'0, ctx_rd_stat}` = `{valid, dir, declared, registered, ready, failed, decl[1:0], fail_code[7:0]}` from the live lwSRP context row — listener idx `k` = ctx row `k`, talker idx `t` = ctx row `(L-1)+t`, so the table is `L+T-1` rows deep ([NXN_ARCHITECTURE.md](../NXN_ARCHITECTURE.md) §3.4.1). **`0xDEAD` = NOT BACKED** (since VERSION `0x0010`): the selected row is `>= N_CTX_P` in this build. It used to alias row 0 instead, i.e. report the legacy pair's live reservation for a row that was never provisioned; `LWSRP_STATUS[11]` latches whenever this happens. The ctx port only grants while `LWSRP_CTRL[0]` is set, so with the engine disabled the SRP-served words (`SRP`, and `SID_*` at talker idx>0) stay at their "not fresh" 0 |
| `0x860` | `A_STRMW_CTLR_LO` | RO | — | **E2 (saved-state fast-connect):** binding controller_entity_id `[31:0]` from the ACMP bind context (5.5.3.5.3 step 2). Listener contexts only — talker dir reads `0xDEADDEAD` |
| `0x864` | `A_STRMW_CTLR_HI` | RO | — | controller_entity_id `[63:32]` (talker dir `0xDEADDEAD`) |
| `0x868` | `A_STRMW_BIND` | RO | — | `{flags[31:16], tuid[15:0]}` from the ACMP bind context — `flags` are the stored binding flags (bit 3 = STREAMING_WAIT, 5.5.2.4), `tuid` the bound talker_unique_id. Talker dir reads `0xDEADDEAD`; `0x86C` (window hole) reads `0xDEADDEAD` |

**The `0xDEADDEAD` not-backed rule (0x000C).** A window word that does not
exist for the selected direction/index reads the POISON value `0xDEADDEAD`,
never 0 — software (and a bench devmem) can tell "this word is not backed
here" from a true zero at first glance. Out-of-range index reads stay 0
(a different condition: the selection itself is invalid).

**The alias rule (N=1 bit-compat axiom).** The legacy flat registers remain
the authority and index 0 of the window is a HARD ALIAS of them — never a
copy:

* talker idx 0 `CTRL[0]`/`DMAC_LO`/`DMAC_HI` are the same storage as
  `AAF_CTRL[0]`/`AAF_DMLO`/`AAF_DMHI` (a window write is visible at the flat
  address and vice versa; the `CTRL` alias merges bit 0 only),
* `SRP` idx 0 is the live `0x694` word, and
* the listener idx-0 SNAP latches the flat
  `AVTPRX_*`/`PCMRX_CNT`/`ACMPL_STATE` sources (`CNT0..3/5/6` mirror today's
  truncated 8/16-bit flat counters — the idx-0 SNAP deliberately keeps the
  flat sources in P12 too, which IS the alias axiom; extra contexts read the
  full 32-bit LCTX words).

Every pre-window CSR TB passes unchanged. `PCMRX_CNT` (0x6C4) stays the
SHARED depacketizer's global `{drops,pdus}` across all streams; per-stream
pdus live in the window `PDUS` word.

**SNAP atomicity ([M-5.4.2.25] GET_COUNTERS).** A SNAP latches `STATE` +
`CNT0..9` + `PDUS` as one coherent set. Index 0 latches all flat sources in
a single cycle. Extra contexts run an engine-arbitrated burst on the context
RAM's port B; `busy` covers the whole burst; the latched words serve reads
until the next SNAP (they do NOT track live counters). Firmware
GET_COUNTERS = `SEL`, `SNAP`, poll `busy`, read the block.

**P12 coherence level (engine-backed, VERSION 0x0009).** The live engines
serve each burst word only when fully event-drained, so every latched WORD
is event-atomic and reflects a completely-applied event state; the engines
do not freeze across the whole burst, so a block whose fetch straddles an
in-flight event is bounded by the burst's start/end states (counters are
monotonic, reset only on that stream's bind edge).

Engine-backed CFG words (`CTRL`/`FMT` listener side, `CTRL`/`DMAC` extra
talker contexts) are "slow" reads served live from the context RAM (>= 4
AXI-stalled cycles, longer while the engine walks an event). A listener
`CTRL` commit at any idx also writes the classification stream-table entry
`{sid staged via SID_LO/HI, en}` and the route field.

**Route flags (`CTRL[2:1]`, KL_pcm_route).** The 2-bit field is a pair of
INDEPENDENT flags, not an exclusive enum:

* `CTRL[1]` = DMA (payload lands in the stream's DRAM ring at
  `pcm base + s*stride`, see the `_PCMRingNxN` CSRs at N > 1),
* `CTRL[2]` = RENDER (feeds the LPF + I2S render path; if several streams
  carry the flag the lowest-indexed one wins).

`0b11` = RENDER|DMA = capture-while-rendering; `0b00` = NULL (neither — the
monitor still counts).

Mapping from the retired P3 enum (ALSA-design feedback, open question 4):

* P3 `0 NULL` -> `0b00`;
* P3 `1 RENDER` -> `0b11` (P3's RENDER also forwarded the ring copy — the
  flags now say so directly);
* P3 `2 DMA` -> `0b01` (the raw value 2 now means RENDER-only).

Reset default: stream 0 = `0b11`, others `0b00` — bit-identical N=1
behavior to P3.

**Talker t>0 arming (`aaf_stream_en_w`, mirrored since 0x000C).** Talker
stream 0's admission is the flat `aaf_gate` unchanged (`AAF_CTRL`
en/bypass, MAAP claim, ACMP talker-active, lwSRP row-0 gate). A talker
idx>0 arms with the SAME composition, term by term:

* TCTX `CTRL[0]` (this window) AND
* the engine-wide MAAP term (`~MAAP_CTRL[0] | addr_valid` — ONE claim
  engine claims a BLOCK of N addresses; stream j transmits and answers
  probes with base+j) AND
* `AAF_CTRL[1]` bypass OR (per-stream ACMP talker_active AND the
  per-stream lwSRP bw-gate with the `~LWSRP_CTRL[0]` escape).

The per-stream ACMP term comes from `KL_acmp_tlkr_ctx` at
`N_SRC_P = N_STREAMS` (0x000C): CONNECT_TX/PROBE_TX answers SUCCESS for
every `talker_unique_id` 0..N-1 (stream_id `{station MAC, uid}`, dest_mac
`MAAP base + uid`), each uid keeping its own Milan §4.3.3.1 15 s probe
window; `talker_active[j>0]` = probe window open OR that stream's
reservation row live (a granted per-stream reservation implies a ready
listener); `A_ACMP_LOBS[0]` overrides every stream. Note the sample-source
reality: the PHYSICAL I2S capture front-end emits slot 0 only — an armed
t>0 emits frames when the chmap capture crossbar
([`../CHANNEL_MAP_64.md`](../CHANNEL_MAP_64.md) §4/§5) feeds its pair
slots (any source, TONE included).

**Bench warning (2026-07-26 silicon).** With `LWSRP_CTRL[0]` cleared the
CBS slope mux disengages, so an admitted talker stream transmits UNPACED
(measured ≈56 k frames/s against the paced 10.4 k/s on the AX 8×8) — a
100M listener port drowns in minutes. Open t>0 admission through real
per-stream reservations (or keep windows short) — never leave the engine
off with armed extra talkers.

**Engine-backed words + read timing.** Window reads of LCTX/TCTX-backed
words (`CTRL`/`FMT` listener side, `CTRL`/`DMAC` extra talker contexts) are
served from the context RAM's second port — the AXI read simply stretches a
few clocks (handshake absorbs it, like the config-shadow reads).

While the lane-K engines are not connected, those inputs are tied inert at
the SoC (`i_lctx_rd_data=0`, `i_lctx_snap_ok=1`, same for TCTX,
`i_acmp_tbl_*=0` — allowlisted in `scripts/check_tied_inputs.sh`), so
engine-backed words read 0 and SNAP completes immediately; the index-0
aliases are fully live today. During a SNAP burst, engine-backed word reads
return 0 (poll busy first).

**lwSRP provisioning through the window.** For idx>0, writing `SID_LO/HI`
(+ `DMAC_LO/HI` for talkers) stages the record and a `CTRL` write commits it
to the live lwSRP attribute-context port (`KL_lwsrp_top ctx_*`): `en`=1
provisions (TalkerAdvertise or Listener declaration per dir), `en`=0
withdraws.

Row map: listener idx k → ctx row k, talker idx t → ctx row
`N_LISTENERS_P-1+t`; row 0 is the legacy pair (read-only, served by the
flat aliases). PriorityAndRank is the class-A constant; TSpec/latency come
from the shared `LWSRP_TSPEC`/`LWSRP_LATENCY` registers until per-stream
TSpec words exist.

**Out-of-range rule.** idx ≥ `N_LISTENERS_P` (dir 0) / `N_TALKERS_P`
(dir 1): every window word reads 0, writes are ignored (no alias, no engine
strobes, no provisioning), SNAP latches zeros and completes. `A_STRM_SEL` /
`A_STRM_SNAP` themselves always decode.

### 0x870  -  AAF per-stage latency taps  `(roadmap item-11, KL_aaf_latency_taps)`

> **Pipeline diagram of where every tap sits:** [`../AAF_LATENCY_TAPS.md`](../AAF_LATENCY_TAPS.md)
> (TX CAP→SOF→EOF→MAC_TX, RX MAC_RX→ACCEPT→DEPKT→PCM_RING, each mapped to its
> trigger and CSR). Per-sample DDR3 history: [`../LATENCY_HISTORY_RING.md`](../LATENCY_HISTORY_RING.md).

Per-stage TX/RX AAF pipeline latency, measured in **axis_clk cycles** (divide
by the datapath clock - 50 MHz Arty / 100 MHz AX7101 - for seconds). Two
independent chains each latch a free-running cycle count at the documented
pipeline points and expose the inter-stage deltas (last / min / max,
saturating 16-bit) plus the gPTP epoch of the measured reference frame:

  * **TX**: `CAP` (ring/I2S pair in) `->` `PKT_SOF` (packetizer first beat)
    `->` `PKT_EOF` (packetizer last beat) `->` `MAC_TX` (frame egresses the
    MAC boundary). Deltas d0 = CAP→SOF, d1 = SOF→EOF, d2 = EOF→MAC.
  * **RX**: `MAC_RX` (frame ingress) `->` `ACCEPT` (AVTP monitor
    parse-complete / accept pulse) `->` `DEPKT` (payload last beat) `->`
    `PCM_RING` (payload accepted at the ring writer). Deltas d0 = MAC_RX→ACCEPT,
    d1 = ACCEPT→DEPKT, d2 = DEPKT→RING.

**Measurement model.** Each chain follows ONE tagged reference frame at a
time: it arms on a stage-0 edge (latching the epoch cycle + gPTP time), takes
the next edge at each later stage as that frame's progress, and on the final
stage records the deltas + publishes the epoch + increments `samples`.

A per-stage timeout (`TIMEOUT_C` ≈ 0.5 ms) aborts and re-arms a stuck token
(`timeouts++`), so a dropped frame never wedges the chain. The token is
followed by ORDER, not a threaded frame id, so under mixed traffic a shared
boundary (`MAC_TX`/`MAC_RX`) may catch a nearer non-AAF edge - min/last/max
therefore characterise the latency ENVELOPE rather than one exact frame.

The I2S-out playout stage is FIFO-fill dominated (the CDC pair FIFO decouples
PDUs from DAC frames) and stays observed via `I2SPB_STAT` fill/converged; a
**DDR3 per-sample history ring is the documented follow-up**.

Both the `LTAP_CTRL` status word and the 16 RO readback words live at
`>= 0x800`, so - exactly like the servo - they need the `rd_in_window`
carve-out or they read 0. Per-delta packing: word `2d` = `{max16, last16}`,
word `2d+1` = `{16'd0, min16}`.

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x870` | `LTAP_CTRL` | RW | `0x2` | W: `[1]` enable (measure; reset 1), `[0]` W1S clear all stats. R: `[1]` enable, `[8]` tx_active, `[11:9]` tx stage awaited, `[12]` rx_active, `[15:13]` rx stage awaited. Since 0x000C the chain walk consumes SAME-CYCLE stage pulses as 0-cycle hops (combinational stages — e.g. the `KL_pcm_route` DEPKT→RING pass-through — no longer strand the token; RX D2 legitimately reads min=0) |
| `0x874` | `LTAP_TX_EPOCH` | RO | `0` | gPTP ns (`ptp_now[31:0]`) latched at the last completed TX frame's CAP stage |
| `0x878` | `LTAP_TX_INFO` | RO | `0` | `[15:0]` samples (completed TX frames, saturating), `[31:16]` timeouts (aborted tokens) |
| `0x87C` | `LTAP_TX_D0` | RO | `0` | CAP→SOF: `[15:0]` last, `[31:16]` max (cycles) |
| `0x880` | `LTAP_TX_D0_MIN` | RO | `0xFFFF` | CAP→SOF: `[15:0]` min (cycles) |
| `0x884` | `LTAP_TX_D1` | RO | `0` | SOF→EOF: `[15:0]` last, `[31:16]` max |
| `0x888` | `LTAP_TX_D1_MIN` | RO | `0xFFFF` | SOF→EOF: `[15:0]` min |
| `0x88C` | `LTAP_TX_D2` | RO | `0` | EOF→MAC_TX: `[15:0]` last, `[31:16]` max |
| `0x890` | `LTAP_TX_D2_MIN` | RO | `0xFFFF` | EOF→MAC_TX: `[15:0]` min |
| `0x894` | `LTAP_RX_EPOCH` | RO | `0` | gPTP ns latched at the last completed RX frame's MAC_RX stage |
| `0x898` | `LTAP_RX_INFO` | RO | `0` | `[15:0]` samples, `[31:16]` timeouts |
| `0x89C` | `LTAP_RX_D0` | RO | `0` | MAC_RX→ACCEPT: `[15:0]` last, `[31:16]` max |
| `0x8A0` | `LTAP_RX_D0_MIN` | RO | `0xFFFF` | MAC_RX→ACCEPT: `[15:0]` min |
| `0x8A4` | `LTAP_RX_D1` | RO | `0` | ACCEPT→DEPKT: `[15:0]` last, `[31:16]` max |
| `0x8A8` | `LTAP_RX_D1_MIN` | RO | `0xFFFF` | ACCEPT→DEPKT: `[15:0]` min |
| `0x8AC` | `LTAP_RX_D2` | RO | `0` | DEPKT→PCM_RING: `[15:0]` last, `[31:16]` max |
| `0x8B0` | `LTAP_RX_D2_MIN` | RO | `0xFFFF` | DEPKT→PCM_RING: `[15:0]` min |

### 0x8B4  -  RX stream-parser probe  `(APRB, avtp_stream_parser + milan_datapath)`

**Why this group exists (2026-07-26).** Every other listener-side counter in
this design — `AVTPRX_*`, `PCMRX_*`, the `0x800` window `CNT0..9`, the RX
latency taps — lives **downstream of the stream-table match**. When a bound
listener accepts nothing they all read 0 in unison and none of them can say
*why*: frames never arrived, or arrived and matched nothing, or matched and
were rejected. These five words are the view **upstream** of the match, and
they were the missing instrument in the fabric-listener accept blocker
([`../limitations/TROUBLESHOOTING.md`](../limitations/TROUBLESHOOTING.md)
§21). The counters already existed inside `avtp_stream_parser`; this group
is what finally wires them out.

The `SID`/`INFO` latch only follows **stream** subtypes (`subtype[7] = 0`:
AAF, CRF, CVF, 61883). Control traffic — ADP/ACMP/AECP/MAAP, which is
continuous on a live fabric — is deliberately excluded so it cannot
overwrite the media evidence between two `devmem` reads. All words are live
RO (no arm, no snapshot) and free-running from reset; read them twice to
get a rate.

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x8B4` | `APRB_PARSED` | RO | `0` | AVTP frames the RX parser fully parsed (32-bit free-running, all subtypes) |
| `0x8B8` | `APRB_MATCHED` | RO | `0` | of those, frames whose `stream_id` matched an ARMED stream-table entry |
| `0x8BC` | `APRB_SID_LO` | RO | `0` | `stream_id[31:0]` **as lifted off the wire** for the last stream-subtype frame |
| `0x8C0` | `APRB_SID_HI` | RO | `0` | `stream_id[63:32]` of that frame |
| `0x8C4` | `APRB_INFO` | RO | `0` | `[7:0]` that frame's AVTP subtype, `[8]` it matched, `[15:12]` matched entry index, `[23:16]` stream-table entries currently armed |

**Reading the three failure modes** (listener bound, nothing accepted):

| `PARSED` | `MATCHED` | verdict |
|---|---|---|
| static | static | frames are not reaching the parser at all — look upstream (MAC, filter, classify), not at the listener |
| climbing | static | the parser sees them and the compare misses — diff `APRB_SID_*` against the bind record (`0x814`/`0x818`) and check `INFO[23:16]` is non-zero (a table with **no armed entry** matches nothing) |
| climbing | climbing | the match is fine; the loss is downstream — `AVTPRX_ERR` (format) then the depacketizer/ring |

### 0x8C8  -  Playback chain probe  `(PBK, roadmap item-7: KL_pcm_tx -> KL_chan_map_render -> KL_i2s_feed_mux -> KL_i2s_playback)`

**Why this group exists (2026-07-26).** The playback engine's own control and
status (`pb_enable`, ring base/len/stride, per-stream `wr_ptr`/`rd_ptr`,
underrun/overrun) are **migen** CSRs generated inside the LiteX SoC
(`sw/litex/milan_soc.py`), so they exist only on that build and never appear
in this map. Nothing on the AXI-Lite control plane could answer the first
question you ask of a silent line-out: *did any audio frame reach the DAC at
all, and if not, where did it stop?* These three words answer it end to end —
`PBK_FEEDS` moving proves the chain is delivering, `PBK_STAT[15:0]` separates
"armed and genuinely silent" from "you never programmed the map", and
`PBK_RAILS` says whether the host is keeping the ring fed.

All words are live RO (no arm, no snapshot) and free-running from reset; read
them twice to get a rate. Same `>= 0x800` `rd_in_window` carve-out class as
the `0x8B4` and `0x870` groups (without it the whole block reads 0 while the
fabric counts fine — the `0x8F8` dead-read trap).

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x8C8` | `PBK_STAT` | RO | `0` | `[15:0]` disarmed-render frames: media frames delivered to the DAC while the crossbar was selected and **no** map entry backed phys{0,1} (saturates at `0xFFFF`) — nonzero means the audio is silent because the map is empty, not because the source is; `[16]` feed source (1 = render crossbar, 0 = legacy listener tap) = `CHMAP_CTRL[0]`; `[17]` `KL_pcm_tx` is walking a sample tick; `[18]` playback master enable; `[19]` phys{0,1} armed in the render map; `[21:20]` reserved 0; `[31:22]` per-phys playback-source mask (map entry `EN` **and** `SRC` = playback), phys 0..9 |
| `0x8CC` | `PBK_FEEDS` | RO | `0` | media frames handed to the `KL_i2s_playback` producer on the **live** source (32-bit, wraps). Render mode counts 48 kHz media ticks; legacy mode counts accepted listener-tap beats. A **static** count with the chain armed is the "nothing is being delivered" verdict |
| `0x8D0` | `PBK_RAILS` | RO | `0` | `KL_pcm_tx` host-ring rails, summed across streams and saturating at `0xFFFF` per half: `[31:16]` underruns (ring empty at a media tick — the host is not refilling; the pair is still emitted so the cadence never skews), `[15:0]` overruns (host lapped the reader by more than one sub-ring; `rd_ptr` fast-forwards one lap) |
| `0x8D4` | - | - | `0` | unmapped (reads 0, never shadow-aliased) |

**Reading a silent line-out** (playback armed, nothing audible):

| `PBK_FEEDS` | `PBK_STAT[15:0]` | `PBK_RAILS[31:16]` | verdict |
|---|---|---|---|
| static | - | - | nothing is reaching the DAC feed. If `PBK_STAT[16]` = 0 the crossbar is not even selected (`CHMAP_CTRL[0]`); if it is 1 the media grid is dead |
| climbing | climbing | - | the crossbar is running but the render map is empty — program phys 0/1 (`CHMAP_SEL`/`CHMAP_WORD` with `SRC` = playback) and re-check `PBK_STAT[31:22]` |
| climbing | static 0 | climbing | the map is armed and the DAC is being fed, but the **host** is starving the ring — the samples are repeat-last (or silence) substitutes, not audio. Look at the ALSA writer, not the fabric |
| climbing | static 0 | static | the chain is delivering real ring words; a silent output is downstream (DAC mute/level, `I2SPB_STAT` rails at `0x6D8`) |

### 0x8F8  -  MMCM-DRP media-clock servo  `(Milan v1.2 7.3.4, KL_mmcm_drp_servo)`

The CRF clock-recovery ACTUATOR (status word + control knobs; loop
semantics in [`../design/TIME_SYNC.md`](../design/TIME_SYNC.md) §3.4).
Parked at the map TAIL (after the 0x800-0x85C window) on purpose: parallel
feature lanes are extending the 0x700 group, so a tail slot cannot collide
on merge; `0x8FC` next to it holds the servo control knobs.

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x8F8` | `MCSRV_STAT` | RO | `0` | `[2:0]` state (0 IDLE, 1 VERIFY, 2 REPAIR, 3 ACQUIRE, 4 LOCKED, 5 HOLDOVER, 6 FAULT), `[3]` DRP config verified, `[4]` DRP config mismatch (read-verify failed; repaired only when `MCSRV_CTRL[1]` is set), `[5]` MMCM LOCKED (synced), `[6]` fine-PS actuator busy, `[7]` PSDONE-watchdog fault (sticky), `[8]` DRP relock-timeout fault, `[15:9]` reserved 0, `[31:16]` **signed** applied frequency trim in 1/16 ppm units (e.g. `+0x06E9` = +110.6 ppm). The servo engages only at `clock_source == 2` (CRF descriptor); in every other mode this word reads state IDLE with trim 0 and the servo generates **zero** DRP/PS activity |
| `0x8FC` | `MCSRV_CTRL` | RW | `0` | `[0]` ps_invert: flips the servo fine-PS direction mapping (bench sign knob - 2026-07-23 mf51 silicon stepped opposite the UG472 reading and rails went 25x worse under the servo; settle the polarity on silicon via this bit, then bake the winner as the RTL default); `[1]` auto_repair: 1 = allow the DRP divider repair path (a `[4]` mismatch triggers the full reset-sequenced read-modify-write reprogram), default 0 = verify-only (bench-gated). NOTE both 0x8F8/0x8FC needed the rd_in_window >=0x800 carve-out - 0x8F8 read 0 on every build before 2026-07-23 |

### 0x900  -  channel-map fabric  `([docs/CHANNEL_MAP_64.md](../CHANNEL_MAP_64.md) §6, KL_chan_map_render / KL_chan_map_capture)`

Debug write port + bypass arm for the 64x64 render/capture map RAMs. Same
dedicated-arm carve-out as MCSRV (NOT in `is_plain_rw` - a 0x900 shadow write
would alias word 0x100 - plus its own `rd_in_window` 0x900-0x93F term, or every
read here would be the 0x8F8 dead-read trap).

`CHMAP_CTRL[0]` = 0 (reset) leaves the deployed audio path bit-identical: the
render/capture crossbars are muxed OUT of both the packetizer feed and the
i2s_playback feed. Setting it to 1 also moves the DAC's **pace** onto the
48 kHz media grid and masks the render LPF (`KL_i2s_feed_mux`; see the
`0x8C8` group) - without that a host-ring playback can never advance the
DAC, because the legacy feed only ticks when an inbound AVB stream does. The AEM audio-map projector (1722.1 7.2.19 / Milan es-4.16)
is the canonical programmer; this window is the bench override (a documented
follow-up wires the projector to the same port).

| Offset | Name | Acc | Reset | Description |
|--------|------|-----|-------|-------------|
| `0x900` | `CHMAP_CTRL` | RW | `0` | `[0]` csr_write_en - fabric bypass arm. While 0, the default capture/render paths drive bit-identically and `CHMAP_WORD` writes are refused (counted in `CHMAP_STAT[23:16]`). Set 1 after programming the map to select the crossbar outputs |
| `0x904` | `CHMAP_SEL` | RW | `0` | `[5:0]` map entry index, `[8]` side (0 = RMAP/render phys channel 0..9, 1 = CMAP/capture pair slot 0..31). Selects the target of the next `CHMAP_WORD` write |
| `0x908` | `CHMAP_WORD` | RW | - | `[15:0]` the §5 map word `{EN[15], SRC[14:12], rsvd[11:8], IDX_HI[7:4], IDX_LO[3:0]}`. Write commits through the shared map write port when `CHMAP_CTRL[0]` = 1; readback = last committed word. **Render side (RMAP)**: `SRC[12]` selects the source bank — 0 = AVB listener, `IDX` = `{stream[6:4], ch[2:0]}` (the pre-item-7 meaning, and what the AEM projector always writes); 1 = **host playback ring**, `IDX` = `{[6:4],[2:0]}` read as one linear playback channel `2*pair_slot + (0 L / 1 R)` from `KL_pcm_tx`. This is the only route from an ALSA playback ring to the line-out |
| `0x90C` | `CHMAP_STAT` | RO | `0` | `[15:0]` aem/csr commits (wraps), `[23:16]` csr_refused (override disarmed; saturates) |
| `0x910`-`0x93C` | - | - | `0` | reserved to this feature (read 0, never shadow-aliased) |

## DMA registers (fully-FPGA build only  -  separate CSR space)

On the fully-FPGA VexiiRiscv (formerly NaxRiscv) SoC the AXIS↔memory DMA (§A.6,
`MilanDMA`) is **not** part of the `milan_csr` window above  -  its engines' registers are auto-mapped in the
**LiteX CSR space** (absolute addresses in the generated `build/csr.csv`; the device
tree exposes them via the `dma-tx`, `dma-rx`, `dma-ts` `reg` entries).

**`dma-tx` and `dma-rx` are ring engines** (2026-07-04: `RingDMAReader`/`RingDMAWriter`,
native AXI-burst masters on the coherent dma_bus  -  see
[`RX_RING_DMA.md`](../../historical_now_obsolete/findings/RX_RING_DMA.md) for why the simple-mode/wishbone predecessors were
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
> later Option 6b upgrade  -  see [`FULLY_FPGA_RISCV_MIGRATION.md`](../../historical_now_obsolete/integration/FULLY_FPGA_RISCV_MIGRATION.md) §A.6.)

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
> block. See also [`sw/dts/README.md`](../../sw/dts/README.md) and [`sw/driver/README.md`](../../sw/driver/README.md).

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
