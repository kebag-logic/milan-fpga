# Register-map production classes — needed / optional / debug

The classification overlay for [REGISTER_MAP.md](REGISTER_MAP.md): every
CSR group judged for a PRODUCTION image, with the rationale on the row.
Written 2026-08-06 against VERSION `0x0023` on the 1×1×8 TDM8 shape.

## The three classes

| class | meaning | production image |
|---|---|---|
| **needed** | The ABI: drivers, DT, boot software, persistence, or a Milan data feed references it. Removing it breaks the contract. | always present, frozen |
| **optional** | Field observability: diagnoses a failure over nothing but ssh/AECP — no bench, no captures. The system functions without it; support quality doesn't. | present by default; a size-pressed profile may drop |
| **debug** | Bench-only: meaningful only inside a lab workflow (frame captures alongside, scope-like probing, calibration runs). | absent; behind build features |

The test that assigns the class: *"who reads this register, standing
where?"* A driver → needed. A support engineer over ssh → optional. An
engineer with a ProfiShark beside the board → debug.

## Classification

| Region | Group | Class | Rationale |
|---|---|---|---|
| `0x000–0x00C` | ID / VERSION / CAP | **needed** | ABI root; VERSION gates every compatibility check made by drivers, scripts and gates |
| `0x204+` | STATS_CAP + RMON counters | **needed** | STATS_CAP's declared-unsupported honesty is contract; RMON feeds NIC-level field triage and future AVB_INTERFACE optional counters |
| `0x4xx` | CBS queue window, classifier map | **needed** | Production traffic-class configuration; boot software programs it |
| `0x600–0x65x` | Identity + enables (ADP_CTRL, AAF_CTRL, …) | **needed** | `S50milan` writes these every boot; the entity does not exist without them |
| `0x618/0x61C` | ADP shape words (RO) | **needed** | Read-only by design since `0x0015` — the advertised range *is* the descriptor set |
| `0x624/0x628` | GM identity | **needed** | `milan-statd` writes them; GET_AVB_INFO serves them — Milan-mandatory data path |
| `0x668` | ADP_DIAG | **debug** | Superseded: DIAG2 exists precisely because this word read the same `0` for healthy and stalled. Retire when the ABI is next unfrozen |
| `0x674` | ADP_DIAG2 | **optional** | Advertiser liveness distinguishable over ssh; created from a real field ambiguity (2026-07-30) |
| `0x680–0x694` | lwSRP CTRL / TSPEC / STATUS | **needed** | Reservation policy + the licence word `0x694` + the `[11]` row-shortfall flag — both configuration and the first field question ("is the stream licensed?") |
| `0x6A4` | ACMPL_STATE | **optional** | Bind/probe/settle state over ssh; used in every connection triage this month |
| `0x6B8` | RX-monitor CSR mirror | **optional** | The counters' CSR face for scripts/statd; AECP GET_COUNTERS carries the same truth for controllers |
| `0x6CC–0x6D4` | MAAP | **needed** | Address acquisition is production function |
| `0x6E8` | ACMPL_DBG (walker forensics) | **debug** | Classify-stage byte forensics. It root-caused the return-leg drop — *with a wire capture beside it*. Meaningless without one |
| `0x730/0x734` | AS_PATH | **needed** | Feeds GET_AS_PATH (Milan Table 5.22 push source); statd maintains it |
| `0x738–0x750` | CRF group (sink + talker enable) | **needed** | Media-clock configuration; Milan 7.3.3 class-A output |
| `0x778–0x780` | CLKV (tu sync lease) | **needed** | The tu policy is a conformance mechanism (IEEE 1722 AAF-10), not instrumentation; statd renews the lease |
| `0x7A0` | Bind-restore (fast-connect) | **needed** | Persistence: saved-state binds replay through it |
| `0x7B8–0x7C4` | Journal ingest | **needed** | Milan 5.3.8.2/.3 boot replay, CRC-gated |
| `0x7C8–0x7D4` | AEM saved-state write master | **needed** | The only path that puts persisted descriptor state back (5.3.8.1 family) |
| `0x800–0x868` | Stream window (SEL/SID/FMT/CTRL/DMAC + per-stream RO views incl `A_STRMW_SRP`/`_CNT`) | **needed** | Persistence replay provisions through the write half; the RO views are the per-stream field picture. `A_STRM_SEL[9]` (listener-0 row) included |
| `0x8B4–0x8C4` | APRB (RX stream-parser probe) | **debug** | The pre-match listener view — a scope instrument. Feature-gated (`datapath_probes`); ON at 1×1 only because the shape has headroom |
| `0x8C8–0x8D0` | PBK (playback-chain probe) | **debug** | Same class, same gate |
| `0x900–0x908` | Raw chmap WRITE window | **debug** | The USER's mapping law (2026-08-06) decides this: the ATDECC map store *is* the mux, and a raw poke path that bypasses the store is a divergence mechanism — exactly the loopback-vs-store split just eliminated. Bring-up images only; production gets no bypass |
| `0x910/0x914` | CHMAP_SNAP / CHMAP_LOOP (readback + LOOP_SUSPECT) | **optional** | The *auditor* that catches store-vs-hardware divergence, read-only and cheap — it stays even when the write window goes |
| latency-tap CSRs | AAF per-stage TX/RX taps | **debug** | Pure instrumentation (`latency_taps` feature). Lives until the 0.44% stress-late row is attributed, then off in production |

## The rules behind the table

1. **"Debug" is not "bench-only observability."** Registers that answer a
   field question over ssh — licence, ACMP state, counters, GM, the
   chmap auditor — are product quality, classed *optional*, and default
   ON. Only what needs lab context beside it (captures, probes,
   calibration) is *debug*.
2. **The raw map window is settled by the mapping law**: one truth (the
   AEM store == the crossbar), one edit path (AECP). The write window is
   a bring-up bypass; the read-only auditor (`0x910/0x914`) is the
   production-grade check that the law holds.
3. **Prune once, then freeze.** Removing any group shifts every window
   behind it — the DTB / driver / OpenSBI re-verification chain
   (`check_dtb_csr`, gate 19c). The production profile must be ONE
   deliberate build (`datapath_probes: false`, `latency_taps: false`,
   raw-window gated, `0x668` retired) whose ABI is then frozen — never
   an incremental trim per release.

Expected recovery from the full debug prune at 1×1: ~700–900 LUTs and a
simpler CSR decode — modest at 77 % utilization; the ABI hygiene is the
real value.
