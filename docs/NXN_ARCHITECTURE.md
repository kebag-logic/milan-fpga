# NxN AAF Milan Streams — Shared Engines + Per-Stream Context RAM

Normative architecture for roadmap item 5 (`docs/MILAN_COMPLIANCE_GAPS.md`,
"Suggested order of attack" item 5). Test shapes: **AX7101 = 8x8**,
**Arty = 4x4** (`configs/endstation_ax7101_8x8.yaml`,
`configs/endstation_arty_4x4.yaml`). Status: DESIGN — no RTL in this round.

**The replication verdict (why this doc exists).** The calibrated resource
estimator (`sw/builder/endstation_builder.py`, per-module costs measured from
the real mf48/mf38 hierarchical place reports) prices full per-stream
replication at **142.0% LUT for 8x8 and 107.5% LUT for 4x4** on the xc7a100t
(see `sw/builder/out/endstation_*/build_plan.md`, rows marked UPPER BOUND).
Replication is dead. The architecture is therefore:

> **ONE engine per function, N contexts per engine.** Every per-stream
> engine (depacketizer, monitor, packetizer, ACMP listener SM, MAAP claim,
> lwSRP registrar) becomes a single shared datapath whose per-stream mutable
> state lives in a BRAM-backed context record, indexed by a stream index
> `s` produced once, at classification time. BRAM-based context is cheap
> (a full 8-stream RX context is 8 Kb — 1/4 of one RAMB36); **muxing is the
> cost**, so the design rules below exist to bound mux growth.

**The no-regression axiom (normative).** Every increment in §5 keeps ALL
existing TBs green, and a build with `N = 1` SHALL produce today's behavior:
same wire bytes from the talker, same CSR map semantics at the legacy
addresses, byte-identical `aecp_aem_rom.svh` for `endstation_arty_current`
(the tracked-ROM identity gate). The legacy flat per-stream CSRs remain and
alias stream index 0.

Companion docs: `docs/ENDSTATION_BUILDER.md` (design decisions D1–D5; one
STREAM_PORT per stream; config-selectable clusters),
`docs/LWSRP_FPGA_ARCHITECTURE.md` (single-attribute engine being scaled
here), `docs/SPEC_TRACEABILITY.md` rows M-CNT-2 (Table 7-156 counters),
AAF-4 / M-FMT-2 (wire-truth channel policy), SRP-9 (per-stream attribute
instances).

## 0. Clause references (verified via pdftotext against /home/alex/standards)

| Ref | Source | Clause | Requirement grounded here |
|-----|--------|--------|---------------------------|
| [M-5.3.8] | Milan v1.2 | 5.3.8 (.2 bound, .3 binding params, .5 probing/settled, .6 probing/ACMP status) | Per-Stream-Input dynamic state — the fields of the ACMP listener context record, per sink |
| [M-5.3.8.10] | Milan v1.2 | 5.3.8.10, Table 5.6 | 10 diagnostic counters per Stream Input; 32-bit wrap; reset on not-bound→bound edge only |
| [M-5.4.2.25] | Milan v1.2 | 5.4.2.25 | GET_COUNTERS per descriptor — needs a coherent per-stream counter block read |
| [M-5.5.3] | Milan v1.2 | 5.5.3 | Listener sink state machine — one instance per sink (the SM the shared ACMP engine time-multiplexes) |
| [M-5.5.4] | Milan v1.2 | 5.5.4 | Talker behavior (PROBE_TX per talker_unique_id) |
| [M-6.3/6.4] | Milan v1.2 | 6.3, 6.4 | Base formats Class A; listener advertises all 48 kHz base formats per Stream Input |
| [M-7.2.2] | Milan v1.2 | 7.2.2 | "an AAF Media Listener with two or more AAF Media Inputs shall implement a CRF Media Clock Input" (have: KL_crf_rx) |
| [M-7.2.3] | Milan v1.2 | 7.2.3 | "an AAF Media Listener with two or more AAF Media Inputs shall implement a CRF Media Clock Output" — **mandatory the moment N≥2 listeners exist** (KL_crf_tx exists; §3.5 provisions it) |
| [M-7.3.2–7.3.4] | Milan v1.2 | 7.3.2–7.3.4, Table 7.1 | CRF stream: base 48000, interval 96, 1 ts/PDU, Class A reservation, format 0x041060010000BB80 |
| [A-7.4.42] | 1722.1-2021 | 7.4.42, Table 7-156/7-157 | STREAM_INPUT counters_valid bits and counters_block offsets — the context-RAM counter word order in §1.4 IS the Table 7-157 offset order |
| [A-7.2.13/7.2.19] | 1722.1-2021 | 7.2.13, 7.2.19 | STREAM_PORT owns clusters + one AUDIO_MAP (builder D1) |
| [P-7.3.3] | 1722-2016 | 7.3.3 | AAF PCM channels_per_frame = wire truth (AAF-4 row; per-stream `wire_chans` export) |
| [P-10] | 1722-2016 | 10 | CRF encapsulation (KL_crf_tx/rx) |
| [P-AnnexB] | 1722-2016 | Annex B | MAAP block claim (one contiguous block of `count` addresses) |
| [Q-35] | 802.1Q-2018 | 35, 35.1, 35.2.7 | MSRP per-stream attribute instances (SRP-9 row); attribute vectors carry ranges — exploited in §3.4 |

## 1. Dataplane RX — shared depacketizer + monitor engine

### 1.1 Stream table (classification, the single authority)

`avtp_stream_parser.sv` **already** carries an `N_STREAMS = 8` match table
(`cfg_stream_id_i[64*N-1:0]` + `cfg_stream_en_i[N-1:0]`, combinational
64-bit compare loop emitting `match_index_o`) — classification needs no new
matcher, only new table writers. Normative:

- The stream table is indexed `s = 0..N_LISTENERS-1` for AAF sinks; the CRF
  sink keeps its dedicated compare inside `KL_crf_rx` (single media clock
  domain, one sink — no table entry burned).
- Match key is the 64-bit **stream_id** (wire truth), never the DMAC. Table
  entries are written by the ACMP listener context on bind/settle
  ([M-5.3.8.3]: sid/dmac/vlan come from the last PROBE_TX_RESPONSE) and may
  be overridden per stream via the CSR window (§1.5) for bench use.
- `match_index_o` rides the frame as sideband (`tuser[3:0]`) into the
  depacketizer frame FIFO and the monitor pulse bundle. The index is
  computed ONCE; every downstream engine consumes it — no re-matching.

### 1.2 Shared depacketizer

Finding from the single-stream RTL: the AAF frames arrive serialized on one
MAC pipe, and `KL_aaf_rx_depacketizer`'s in-flight scratch (`rstate_r`,
`rbeat_r`, `hold_r`, `remain_r`, `vlan_r`, `good_r`, `in_frame_r`) only ever
describes ONE frame at a time. Therefore the depacketizer engine stays a
**single instance with zero context duplication of its FSM**; only its
counters (`pdus`, `drops`) become per-stream context words. The frame FIFO
stays single (2 KB) and stores `{tuser=s}` alongside each frame; the read
side emits `{s, pcm beats}`.

### 1.3 PCM routing policy

Each listener context carries a 2-bit `route` field of INDEPENDENT flags
(reworked from the P3 exclusive enum per the ALSA driver design feedback,
the-private-test-repo `fpga/docs/ALSA_DRIVER_DESIGN.md` open question 4):

| bit | Flag | Meaning |
|-----|------|---------|
| 0 | `DMA` | Depacketized PCM written to the per-stream PCM DMA ring in DRAM (ring base + `s`·ring_stride, the existing LiteX PCM-ring DMA generalized with an index) — the capture-PCM feed for roadmap item 7 (ALSA). |
| 1 | `RENDER` | Feeds the physical render path: LPF (x1, engages per today's `chans==2` rule) → `KL_i2s_playback`/TDM serializer. **Exactly one stream renders; if several carry the flag, the lowest-indexed one wins (deterministic rule, RTL-enforced).** |

`0b00` = NULL (discarded — monitor still counts, [M-5.3.8.10] counters run
regardless of rendering); `0b11` = RENDER|DMA = capture-while-rendering.
Mapping from the P3 enum: `0 NULL`→`0b00`, `1 RENDER`→`0b11` (P3's RENDER
de-facto also forwarded the ring copy), `2 DMA`→`0b01`.

Default at reset: stream 0 = RENDER|DMA, others NULL — the N=1 shape is
bit-identical to today. The render path (LPF, playback walker, wire-truth
1-to-1 channel rule per AAF-4/M-FMT-2) is instantiated ONCE; `wire_chans`
delivered to the walker is the RENDER stream's context field.

### 1.4 Listener context record (LCTX) — bit-accurate layout

One RAMB18 (SDP, 32-bit ports), address `{s[2:0], word[4:0]}` — 32 words
(1024 bits) per stream, 8 streams = 8 Kb.

**CFG region (CSR/ACMP-written, engine-read):**

| Word | Field | Bits | Source |
|------|-------|------|--------|
| w0 | `SID_LO` | [31:0] | ACMP bind (or CSR override) |
| w1 | `SID_HI` | [31:0] | " |
| w2 | `FMT_LO` | [31:0] | AECP SET_STREAM_FORMAT (current format u64, [M-5.3.8.1]) |
| w3 | `FMT_HI` | [31:0] | " |
| w4 | `CTRL` | [0] en, [2:1] route, [31:3] rsvd | CSR |

**DYN region (engine-owned; today's `KL_avtp_rx_monitor` scalar registers):**

| Word | Field | Bits |
|------|-------|------|
| w8 | `MON_STATE` | [7:0] prev_seq, [11:8] settle, [12] media_locked, [13] bound_q, [21:14] wire_chans, [31:22] rsvd |
| w9 | `LAST_TS` | [31:0] avtp_timestamp of last accepted PDU |
| w10 | `LAST_TSD` | [31:0] signed ts_delta |
| w11 | `DEPKT_CNT` | [15:0] pdus, [31:16] drops |

**CNT region — w16..w25, in 1722.1-2021 Table 7-157 offset order** so a
GET_COUNTERS block is a linear burst read: `MEDIA_LOCKED, MEDIA_UNLOCKED,
STREAM_INTERRUPTED, SEQ_NUM_MISMATCH, MEDIA_RESET, TIMESTAMP_UNCERTAIN,
UNSUPPORTED_FORMAT, LATE_TIMESTAMP, EARLY_TIMESTAMP, FRAMES_RX` (10 × 32 b,
wrap-to-zero, reset ONLY on that stream's not-bound→bound edge —
[M-5.3.8.10]).

**Timer rule (normative, applies to every context engine in this doc):**
free-running per-stream timers do NOT go to RAM. They are re-based to the
shared 1 ms tick and held as narrow per-stream flop arrays. The monitor's
100 ms silence watchdog becomes a 7-bit ms-counter × N (56 FF for N=8)
instead of a 32-bit cycle counter × N in RAM needing a RMW every cycle.
Context RAM holds event-driven state only; the engine performs a serial
read-modify-write walk per accepted frame (≥ ~780 cycles available between
frames of one stream at 8 kHz class-A cadence; total RX PDU rate 64 k/s at
N=8 leaves > 700 datapath cycles per PDU at 50 MHz — a ~15-cycle RMW walk
has > 40x margin).

### 1.5 Per-stream counter access — indexed CSR window (the register interface)

Today's per-stream CSRs are flat fixed addresses (0x6A4–0x6F0 listener
group, 0x6B8 `AVTPRX_STAT` = "STREAM_INPUT[0], Milan Table 7-156"). Flat
replication for 8+8 streams would add ~500 decoded words to `milan_csr`
(~1.6 k LUT today for ~120 registers — decode scales with word count).
**Decision: indexed window, placed in the free CSR tail (map is used up to
0x774; 0x778+ is free — see `docs/reference/REGISTER_MAP.md`).**

| Addr | Name | R/W | Fields |
|------|------|-----|--------|
| 0x800 | `A_STRM_SEL` | RW | [3:0] stream index, [8] dir (0 = listener, 1 = talker) |
| 0x804 | `A_STRM_SNAP` | W strobe / R [0] busy | Latches the selected stream's full CNT region + STATE into the window shadow in one engine-arbitrated burst — the coherent block [M-5.4.2.25] GET_COUNTERS needs |
| 0x810 | `A_STRMW_CTRL` | RW | [0] en, [2:1] route (listener) / [0] en (talker) |
| 0x814/0x818 | `A_STRMW_SID_LO/HI` | RW(talker)/RO(listener-bound) | stream_id |
| 0x81C/0x820 | `A_STRMW_DMAC_LO/HI` | RW/RO | stream DMAC |
| 0x824/0x828 | `A_STRMW_FMT_LO/HI` | RW | current stream format |
| 0x82C | `A_STRMW_STATE` | RO | packed: ACMP lsm state[2:0], probing[4:3], acmp_status[9:5], media_locked[10], wire_chans[18:11], SRP bits[27:19] |
| 0x830–0x857 | `A_STRMW_CNT0..9` | RO | the 10 Table 7-157 counters (offsets 0..36 preserved) |
| 0x858 | `A_STRMW_PDUS` | RO | {drops[31:16], pdus[15:0]} (listener) / frames_sent (talker) |
| 0x85C | `A_STRMW_SRP` | RO | per-stream lwSRP attribute status (mirrors 0x694 bit layout) |

Window reads are served from the context RAM's second port (SDP port B) —
no shadow copies except the SNAP latch block. Justification of indexed over
flat: (a) decode area O(1) instead of O(N); (b) the reader is the single
softcore daemon — sequential SEL-then-read costs nothing; (c) SNAP gives
GET_COUNTERS atomicity that flat regs never had; (d) legacy flat registers
(0x648–0x764) stay wired to index 0 / the dedicated CRF engines, which IS
the no-regression axiom for N=1. AECP GET_COUNTERS handling in firmware
switches from fixed 0x6B8-group reads to SEL/SNAP/window reads keyed by
descriptor index.

## 2. Dataplane TX — shared packetizer

### 2.1 Engine

`aaf_talker_i2s` splits cleanly: the audio-domain capture front-end (I2S
today, TDM8/16 with item 4's ser/des subtask) is physical-interface-scoped
(x1), and the framer/serializer (seq, ts latch, header build, 12-beat AXIS
emit) becomes the shared packetizer. Per-stream mutable state (today's
scalars `seq_r`, `ts_r`, `nsamp_r`, `frame_pend_r`, `buf_l/r[0:5]`,
`frames_sent_o`) moves to the talker context.

### 2.2 Talker context record (TCTX) — bit-accurate layout

RAMB18 region, `{t[2:0], word[3:0]}`:

| Word | Field | Bits |
|------|-------|------|
| w0 | `CTRL` | [0] en, [4:1] chans (wire truth, [P-7.3.3]), [16:5] vlan_vid, [31:17] rsvd |
| w1 | `DMAC_LO` | [31:0] (default = MAAP base + t, §3.3; CSR-overridable) |
| w2 | `DMAC_HI` | [15:0]; [31:16] `UID` (stream_id = {station_mac, uid}, uid default = t) |
| w3 | `SEQ_TS` | [7:0] sequence_num, [31:8] rsvd |
| w4 | `TS` | [31:0] latched presentation time (ptp_ns + transit_ns at first-sample capture) |
| w5 | `FRAMES` | [31:0] frames_sent counter |

Sample staging: a double-buffered BRAM region, `6 samples × chans × 24 b`
per stream (8 × 8 ch = 9.2 Kb per bank; both banks fit one RAMB36 beside
the TCTX). The audio-domain TDM deserializer writes bank A while the
packetizer drains bank B; the bank swap IS the epoch boundary.

### 2.3 Scheduling across N talker streams

All N talker streams share the media clock, so all frame on the same
6-sample cadence (48 kHz / 6 = 8 kHz per stream, the class-A observation
interval, [M-6.3]). Normative scheduler: an **epoch round-robin** — on each
8 kHz epoch strobe (media_adv-derived / audio-MMCM grid), the packetizer
walks `t = 0..T-1`, emits one AAF PDU per enabled stream back-to-back into
the AAF class-A queue. Worst case 8 streams × ~25 beats ≈ 200 datapath
cycles per 6250-cycle epoch (50 MHz) — 3% occupancy; no per-stream pacing
needed. Per-stream ts is latched per epoch from the shared PHC read (one
read, N stamps).

### 2.4 CBS interaction

The shaper is untouched: all AAF streams map to the same class-A queue
(qidx from `LWSRP_CTRL[3:2]`). The epoch burst (≤ 8 × ~190 B ≈ 1.5 KB) is
spread across the 125 µs interval by CBS credits exactly as designed. What
generalizes is the **reservation math**: `KL_lwsrp_bw_gate` becomes a
Σ-slope accumulator — idleSlope(queue) = Σ granted per-stream slopes, and
`over_limit` compares the Σ against the 75% ceiling (§3.4). Per-stream
`stream_gate[t]` gates each stream's epoch slot individually (a torn-down
stream stops instantly; others keep their slots). Bandwidth sanity at
N=8×8ch: 8 × 8000 × ~190 B ≈ 97 Mbit/s < 750 Mbit/s ceiling.

### 2.5 CRF output — dedicated engine, not a stream slot

`KL_crf_tx` (exists, wire-proven, CSRs 0x750–0x764, 6th low-rate
control-merge source) stays a dedicated engine rather than talker context
N: its cadence (500 PDU/s, [M-7.3.2] interval 96), its 60-byte fixed frame,
and its audio-MMCM event-grid timestamp capture share nothing with the AAF
packetizer walk. What it lacks is provisioning, not datapath — §3.5.

## 3. Control plane

### 3.1 ACMP listener SM × N

`KL_acmp_listener` already contains the exact split this architecture
needs: a shared frame engine (COLLECT/CLASSIFY/RESPOND scratch: 9×64
frame buffer, `cap_*` captures, TX watchdog, LFSR/ms timebase — stays x1)
and a per-sink binding record — which the RTL **already duplicates by hand
once** (the sink-1 CRF record `s1_*`). That duplication generalizes into
the ACMP context RAM (ACTX), `N_LISTENERS + 1` entries (AAF sinks + CRF
sink), selected by `listener_unique_id` from the classified ACMPDU:

| Field | Bits | [M-5.3.8] anchor |
|-------|------|------------------|
| `lsm_state` | 3 (acmp_lsm_t, [M-5.5.3] states) | 5.3.8.5/.6 |
| `bnd_ctlr` | 64 | 5.3.8.3 |
| `bnd_talker` | 64 | 5.3.8.3 |
| `bnd_tuid` | 16 | 5.3.8.3 |
| `bnd_flags` | 16 | STREAMING_WAIT etc. |
| `sid` | 64 | 5.3.8.5 (authoritative post-probe) |
| `dmac` | 48 | " |
| `vlan` | 12 | " |
| `active` | 1 | started/stopped |
| `probe_seq` | 16 | outgoing PROBE_TX sequence_id |
| `acmp_status` | 5, `probing` 2 | 5.3.8.6 |
| `tk_avail` | 1 | 5.3.8.4 (per-sink ADP discovery watch) |
| `clock_sink` | 1 | flavor bit — CRF sink record semantics (today's sink-1 SM) |
| `cmd_count`/`probe_count` | 16+16 | forensics |

= 366 bits → 12 words × 32 b; 9 entries ≈ 4.3 Kb (RAMB18). Timers
(`tmr` 200 ms/4 s/10 s, `adp_age` 63 s) follow the §1.4 timer rule: ms/s
tick scan, one context per tick slot. On bind edge the engine pulses
`ctx_bind_rise[s]`, which resets that stream's LCTX CNT region ([M-5.3.8.10]
reset rule) and writes the stream table entry (§1.1).

### 3.2 Talker activation × N

`KL_acmp_responder`: shared frame engine stays; the per-talker activation
state (`probe_armed`, 5-bit `probe_tmr`, 15 s window, [M-5.5.4]) becomes a
flop array indexed by `talker_unique_id` (N × 6 b = 48 FF — below the RAM
threshold, stays in flops). `talker_active[t] = probe_armed[t] |
listener_observed[t]`, where `listener_observed[t]` comes from the
per-stream lwSRP listener-ready bit (§3.4).

### 3.3 MAAP — one block claim covers all N (block count 8 already)

`KL_maap` claims ONE contiguous block of `count_i` addresses ([P-AnnexB]);
`MAAP_CTRL[15:8]` already resets to 8. Normative: **no per-stream claim
contexts.** Per-stream DMACs are derived: `dmac(t) = claimed_base + t` for
AAF talkers, `dmac(CRF) = claimed_base + T`; the block count becomes
`T + 1` (CSR default lifted 8→9 when the CRF output is enabled). Conflict
detection and DEFEND are already range-based over the whole block, so the
single SM defends all stream DMACs at today's cost. The `eff_aaf_dmac` mux
generalizes to a per-context adder. This is the cheapest subsystem of the
whole item — by design the protocol did the N-scaling for us.

### 3.4 lwSRP — N + N attribute contexts (subsumes the CRF-reservation gap)

The walker (`KL_lwsrp_walker`) already carries TWO hard-coded match
contexts (`{val_match_r, k_r, cap_evt_r, cap_par_r}` for our talker sid,
`{lval_match_r, lk_r, lcap_evt_r}` for the ACMP-bound sid) — the seed of
the context engine. Generalization (SRP-9, [Q-35.2.7]):

- **Match stage:** `T+1` talker keys + `L+1` listener keys (AAF + CRF each
  side), 64-bit range compares against the streaming FirstValue — for N=8
  this is 18 compares, structurally today's 2 × 9. Keys come from the SRP
  attribute context RAM (SCTX), maintained by ACMP bind (listener side) and
  the talker config (talker side).
- **Talker attribute context** (per t): `{uid[15:0], vid[11:0],
  max_frame[15:0], interval[15:0], acclat[31:0], declared, fresh, evt[2:0],
  listener_reg, listener_decl[1:0], lstn_leave_ms[9:0], tfail_valid,
  tfail_code[7:0], tfail_bridge[63:0], slope[31:0], gate, over}` ≈ 210 b.
- **Listener attribute context** (per l): `{sid[63:0], declare, ready,
  ta_registered, ta_failed, ta_fail_code[7:0], ta_vlan[11:0],
  ta_acclat[31:0], ta_bridge[63:0], ta_leave_ms[9:0], tf_leave_ms[9:0]}`
  ≈ 200 b. (Today's `KL_lwsrp_registrar` + `KL_lwsrp_ta_registrar` state,
  one row each.)
- Leave/age timers per the §1.4 ms-tick scan rule.
- **TX declaration walk:** `KL_lwsrp_tx` emits per JoinTime one MSRP PDU
  whose TalkerAdvertise / Listener vector attributes cover all declared
  contexts. Because uid = t, our stream_ids are consecutive — the MRP
  vector encoding carries them as ONE FirstValue + NumberOfValues = T
  attribute (a wire-size and LUT win; per-context event values ride the
  packed vector). Non-consecutive overrides fall back to one attribute per
  context.
- **Σ-slope:** bw_gate accumulates granted slopes over contexts (walked on
  the ms tick), drives the single class-A `idle_slope`, per-context
  `stream_gate`, and `over_limit` vs the 75% ceiling.
- **This closes the CRF reservation gap:** the CRF sink gets listener
  attribute context `L`, the CRF output gets talker attribute context `T`
  with the Class A reservation [M-7.3.3] — the CRF stream stops riding
  untagged best-effort (gaps §2 REMAINING item).

### 3.5 CRF Media Clock Output provisioning ([M-7.2.3])

With N ≥ 2 AAF listener sinks, the CRF Media Clock Output is mandatory.
KL_crf_tx exists; the item-5 round provisions it: (a) AEM overlay emits the
CRF `STREAM_OUTPUT` descriptor (builder change — the 8x8/4x4 overlays gain
one STREAM_OUTPUT with format 0x041060010000BB80, no STREAM_PORT per D1);
(b) MAAP DMAC slot `base + T` (§3.3); (c) lwSRP talker attribute context
`T` (§3.4); (d) provisioning daemon arms `A_CRFT_*` from the claimed DMAC
and station identity. The CRF sink side ([M-7.2.2]) is already compliant.

### 3.6 AEM / AECP changes

The overlay path already builds structurally valid multi-port ROMs (one
STREAM_PORT per stream, per-port cluster blocks, §7.2.19-relative maps —
builder D1/D2/D3); nothing in fabric consumes them yet. AECP RTL changes:
the svh validation tables (`AEM_FMTS_C` — first STREAM_INPUT only;
`WB_STREAM_FORMAT_C` — STREAM_OUTPUT[0] only) become descriptor-indexed
2-D tables emitted by `gen_aem_store.py` codegen; SET/GET_STREAM_FORMAT,
GET_STREAM_INFO and GET_COUNTERS handlers key the §1.5 window by descriptor
index. ADP source/sink counts already come honest from the overlay.

## 4. Clock domains, CDC, and the timing-risk register

Domains (unchanged set): `axis/milan clk` (AX 100 MHz / Arty 50 MHz),
`gtx_clk` 125 MHz (MAC-RX timestamping only), audio MMCM 24.576 MHz,
CPU/system. **All context engines and context RAMs live entirely in the
milan clk domain** — parser, monitor, depacketizer, ACMP, MAAP, lwSRP,
CRF-rx are single-domain today (verified per module) and stay so; the
context-RAM refactor adds ZERO new CDC. The audio boundary crossings do
not multiply with N:

- TX capture: ONE widened `cdc_pair_fifo` carries `{slot, sample}` from the
  TDM deserializer (all streams' samples ride one crossing).
- RX render: ONE `cdc_pair_fifo` to the DAC serializer (only the RENDER
  stream crosses).
- CRF-tx keeps its `cdc_pulse` event-grid crossing.

**Timing-risk register** (the cones that grow, against the AX 100 MHz
history — AX31 guard-netlist round: 6–8 seed misses from a single
`storage_32`/`tx_sf ADDR[9]` cone; defect 4: LUTRAM read-port replica
divergence caught by BDBG):

| # | Cone | Risk | Mitigation (normative) |
|---|------|------|------------------------|
| T1 | Context-RAM RMW (read→modify→write counter/state walk) | New RMW loop per engine; same-address back-to-back hazard | 2-stage pipelined RMW with a single bypass register; serial walk (one word/cycle) — never a parallel 10-counter update |
| T2 | CSR window readback mux | Widening the `milan_csr` read mux was the historic decode-cone trap | Window served from context-RAM port B (registered BRAM output, 2-cycle read latency); ONE explicit read port per RAM (defect-4 rule: no inferred read-port replicas) |
| T3 | Parser 8-way 64-bit sid compare | — | Already exists at N_STREAMS=8 and closes at AX 100 MHz today; adding table-write muxing only. lwSRP walker grows 2→18 compares: register the FirstValue once, tree the compares, allow one extra pipeline stage (MRP has ms-scale timing slack) |
| T4 | TX epoch scheduler arbitration | New round-robin grant + context fetch feeding the header builder | Context prefetch one slot ahead; header build already serial (12 beats) |
| T5 | Σ-slope accumulator | 49-bit multiply-accumulate over contexts | Walked on the ms tick, one context per cycle — sequential by construction (the CBS sequential-slope-engine pattern that saved 8 K LUTs in the area-70 campaign) |
| T6 | AX 100 MHz closure at ~88% LUT | Historic: seed lottery above ~80% utilization | 3×32-thread seed sweeps (standing rule); levers of §6 before any timing heroics; QSPI-corruption floor: never ship below the WNS ≥ +0.03 rule if a clock bump is ever attempted |

## 5. Phasing — TB-gated increments (no-regression axiom throughout)

Every increment: full `tb/verilator/*` sweep green (`for d in */; do (cd $d
&& make) done`), yosys portability check, builder gates
(`python3 sw/builder/test_builder.py` incl. the ROM byte-identity gate),
and the N=1 shape bit-compatible. Lanes A–D are parallelizable after P0;
integration steps are serial at the end.

| # | Increment | Lane | TB gate | Parallel? |
|---|-----------|------|---------|-----------|
| P0 | `N_STREAMS` parameter plumbing: milan_datapath/milan_top/milan_soc `--num-streams` (builder emits it in soc_params); N=1 default, zero functional delta | — | full sweep unchanged; `datapath`, `milan_dp` | serial (root) |
| P1 | Stream-table CSR authority + `tuser` stream-index tag parser→FIFO→monitor bundle; index constant 0 at N=1 | A | `avtp_stream` extended (multi-entry match already covered), `avtp_rxmon` 75 + coverage gate | lane root |
| P2 | Monitor context RAM: LCTX DYN+CNT regions, bind-edge reset per stream, silence→ms-tick flop array; 0x6B8 group aliases stream 0 | A | `avtp_rxmon` (≥95% line cov held) + new N-stream interleave TB | ∥ with B,C,D |
| P3 | PCM routing policy: `route` field, RENDER-lowest-wins, per-stream DMA rings, NULL default for s>0 | A | `i2spb` untouched-green, `datapath` | after P2 |
| P4 | Shared TX packetizer + TCTX + epoch scheduler; golden-frame check: N=1 emits today's exact wire bytes | B | `aaf` + new golden-frame byte-compare TB | ∥ with A,C,D |
| P5 | Σ-slope bw_gate + per-stream gates | B | `lwsrp` 36 (bw math rows) + `cbs` | after P4 |
| P6 | ACMP listener ACTX (sink-1 record folds into context N flavor); timer scan | C | `acmp_lstn` 89 checks + xN bind/probe interleave checks | ∥ with A,B,D |
| P7 | Responder per-tuid activation array | C | `acmp` | after P6 |
| P8 | MAAP count=T+1 + per-stream DMAC derivation adder | C | `maap` | ∥ within C |
| P9 | lwSRP walker N-key match + SCTX registrar/declaration contexts + vector-range TX (closes SRP-9 + CRF reservation) | D | `lwsrp` 36, `lwsrp_rx` 75, `lwsrp_tx` 363, `lwsrp_switchpdu` | ∥ with A,B,C |
| P10 | CRF output provisioning: overlay STREAM_OUTPUT + MAAP slot + SRP context + daemon arming ([M-7.2.3]) | D | `crf_tx` + builder gates (overlay counts) | after P8, P9 |
| P11 | Indexed CSR window (0x800 block) + AECP per-stream validation tables (codegen) | E | `csr`, `aecp` 474, ROM byte-identity gate | after P2, P6 |
| P12 | Integration: 4x4/8x8 config builds end-to-end, 2-stream smoke in `milan_dp`, estimator re-run with shared-engine rows replacing UPPER BOUNDs | — | `datapath`, `milan_dp`, full sweep, `test_builder` | serial (last) |

Lanes: **A (RX contexts), B (TX), C (ACMP/MAAP), D (lwSRP)** run
concurrently after P0 (lane A additionally needs P1 first); P11 joins A+C;
P12 closes. Silicon sweeps (3-seed Vivado rule) happen after P12, outside
this doc's scope.

## 6. Resource budget per subsystem

Baseline = the estimator's calibrated per-module numbers (mf48 measured
x1); "replicated" = the estimator's UPPER BOUND (dead); "shared" = this
architecture. **Stated assumptions:** context RAM in BRAM is charged at its
BRAM cost only; the shared-engine LUT/FF overhead for context indexing,
RMW pipelining and muxing is modeled at **+35% LUT / +20% FF** of the
measured single-instance engine (+50%/+40% for the TX packetizer whose
scheduler is new; +40% for ACMP; +60% for the lwSRP walker whose compare
tree really grows) — deliberately conservative, and to first order
N-independent (mux widths grow with log2 N only). All rows LUT/FF/BRAM36/DSP.

| Subsystem | Measured x1 | 8x8 replicated (estimator UB) | 8x8 shared (this doc) | 4x4 shared |
|---|---|---|---|---|
| RX stream engine (depkt+parser+monitor+LPF) | 1223/2094/1.5/1 | 9784/16752/12/8 | 1650/2500/2.5/1 | 1590/2400/2.5/1 |
| TX packetizer (talker framer) | 338/645/0/0 | 2704/5160/0/0 | 510/800/1.0/0 | 490/750/1.0/0 |
| ACMP listener SM | 1569/1527/0/0 | 12552/12216/0/0 | 2200/1900/0.5/0 | 2120/1850/0.5/0 |
| MAAP | 480/267/0/0 | 3840/2136/0/0 | 540/280/0/0 | 540/280/0/0 |
| lwSRP attribute contexts (beyond base) | 926/750/0/0 | 12964/10500/0/0 | 1500/1200/0.5/0 | 1435/1150/0.5/0 |
| CSR indexed window (delta) | — | — | 300/400/0.5/0 | 300/400/0.5/0 |
| AECP per-stream tables (delta) | — | — | 400/200/0/0 | 400/200/0/0 |
| TDM interface delta (item-4 ser/des) | — | — | 200/300/0/0 | 200/300/0/0 |
| CRF-out provisioning delta | — | — | 100/100/0/0 | 100/100/0/0 |
| Fixed base (soc_infra, cpu, tc, aecp, crf_rx, csr, ptp, rx_filter, i2s, misc, lwsrp_base) | 48181/47419/…/… | 48181/47419 | 48181/47419 | 48181/47419 |
| AEM ROM cluster growth (model) | — | 0/0/2.0/0 | 0/0/2.0/0 | 0/0/0.25/0 |
| L2 delta (8x8 config: 32 KB) | — | −8 BRAM | −8 BRAM | 0 (64 KB) |

**Totals vs xc7a100t (63400 LUT / 126800 FF / 135 BRAM36 / 240 DSP):**

| Shape | LUT | FF | BRAM36 | DSP | vs estimator replicated |
|---|---|---|---|---|---|
| 8x8-ax shared | ~55.6 k (**87.7%**) | ~55.1 k (43.5%) | ~94.5 (70.0%) | 43 (17.9%) | 142.0% → 87.7% LUT |
| 4x4-arty shared | ~55.4 k (**87.3%**) | ~54.5 k (43.0%) | ~100.7 (74.6%) | 43 (17.9%) | 107.5% → 87.3% LUT |
| Today's shipping 1x1 (reference) | 51.8 k (81.7%) | 52.0 k (41.0%) | 97.0 (71.9%) | 42 | — |

The shared-engine architecture makes 4x4 and 8x8 nearly the same size —
that is the point: cost is per-ENGINE, and N only widens indexes and
deepens BRAMs. **Both shapes fit the part arithmetically with ~12% LUT
headroom**, but both land in the estimator's OVER band (> 80%, area-70
directive: expect placement/timing pain), only +6 points over the shipping
81.7% build that closes timing on both boards today. Honest split: **4x4 on
Arty (50 MHz milan domain) is expected to close** on the shipping
precedent; **8x8 on AX at 100 MHz is the timing-risk shape** (§4 T6).
Levers, in order, if a shape refuses to close:

1. **L2 32 KB** (standing USER authorization when space-bound; already in
   the 8x8 config, applicable to 4x4 too: −8 BRAM + placement relief; note
   the perf delta per the authorization's terms).
2. `crf_rx` ts-history ring 256×64 b → BRAM (today ~8.4 k FF in that
   module; −FF and placement relief, ≈ +1 BRAM).
3. Compile-time `N_RENDER=1` pruning already assumed (LPF + playback walker
   x1); further: compile out DMA-ring writers for shapes that don't enable
   ALSA capture yet.
4. Area-70 playbook trims (sequentialize any remaining parallel cones —
   T5's pattern; `tx_sf` 512 lever from the AX seed-miss round).
5. If 8x8-ax still refuses: ship 8x8 with the 4x4 gateware config on AX
   (config-selectable N is exactly what the builder emits) and keep 8x8 as
   the sweep target — the architecture does not change.

The estimator's `RESOURCE_COSTS` UPPER BOUND rows are to be replaced by
shared-engine rows (engine x1 + per-context marginal ≈ 0 LUT + BRAM model)
in P12, keeping the calibration gate honest.

**P12 DONE (2026-07-22):** the shared-engine rows landed — engines charged
once at the measured x1 + yosys-OOC-derived per-context marginals (N=1→8
deltas of the merged engines, LUT4:LUT6 charged 1:1 = safe-side). Recomputed
verdicts: **4x4 = 84.9% LUT, 8x8 = 89.2% LUT** — both FIT the part with
headroom, both in the OVER band as this table predicted (87.3/87.7 modeled);
`test_builder` gate 13 pins the envelope (< 88% / < 92%).
