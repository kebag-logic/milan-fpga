# Register-map production classes — needed / optional / debug

The classification overlay for [REGISTER_MAP.md](REGISTER_MAP.md): every
CSR group judged for a PRODUCTION image, with the rationale on the row.
Written 2026-08-06 against VERSION `0x0023` on the 1×1×8 TDM8 shape;
**reclassified 2026-08-13** against the protocol-processor substitution.

> **A FOURTH VERDICT NOW EXISTS: STRUCTURAL ZERO.** This repository's ADP,
> ACMP, AECP/AEM and lwSRP RTL was deleted in favour of the pinned
> `protocol-processor` submodule. Its **AECP uCPU has landed** and serves the
> inventory recorded in the current Milan audit, including descriptor reads,
> configuration, stream, clock, Identify, counter, audio-map, and Milan
> information operations. Unsupported commands receive a conformant fallback,
> which is not the same as implementing their required behavior.
> **No AECP command writes or reads any CSR in this map**, so the structural
> zeros below are unchanged in verdict; several of them changed in *reason*,
> and the reasons are now narrow and per-field rather than "there is no engine".
> The register map is an ABI, so **no register was removed**: a word whose
> source is gone reads a *structural* zero and is documented as one. A word that
> reads a plausible value instead would be a defect, and a word that merely
> reads back what software wrote while reaching nothing is called out separately
> as **write-only scratch**.
>
> A structural zero is not a class of usefulness, it is a statement about
> truth, so it composes with the three classes below: a group can be
> *needed* (its address is ABI, drivers touch it) and still be a structural
> zero (nothing behind it). Where that happens the table says both.
>
> **Per-word detail is [REGISTER_MAP.md](REGISTER_MAP.md)** — it carries the
> field-by-field verdicts and is the authority. This page stays at group
> granularity.

## Contents

- **[The three classes](#the-three-classes)** — needed/optional/debug defined by who reads the register standing where: a driver, a support engineer over ssh, or an engineer with a ProfiShark beside the board.
- **[Classification](#classification)** — the row-by-row verdict for every CSR group from `0x000` to the latency taps, each with the rationale that assigned its class, and the 2026-08-13 truth column.
- **[The rules behind the table](#the-rules-behind-the-table)** — why ssh-reachable observability is optional not debug, why the mapping law that killed the raw write window has itself been overtaken, and why the prune must be one frozen build (~700–900 LUTs back).

## The three classes

| class | meaning | production image |
|---|---|---|
| **needed** | The ABI: drivers, DT, boot software, persistence, or a Milan data feed references it. Removing it breaks the contract. | always present, frozen |
| **optional** | Field observability: diagnoses a failure over nothing but ssh — no bench, no captures. The system functions without it; support quality doesn't. | present by default; a size-pressed profile may drop |
| **debug** | Bench-only: meaningful only inside a lab workflow (frame captures alongside, scope-like probing, calibration runs). | absent; behind build features |

The test that assigns the class: *"who reads this register, standing
where?"* A driver → needed. A support engineer over ssh → optional. An
engineer with a ProfiShark beside the board → debug.

**One input to that test changed.** The *optional* class used to lean on
"diagnoses a failure over ssh **or AECP**". AECP now answers exactly one
command — `READ_DESCRIPTOR`, and only from a descriptor image nothing in this
repository builds or loads, so on a stock build even that one command answers
`BAD_ARGUMENTS` (the microprogram's configuration range check precedes the
locate, and an invalid image reports `configurations_count` = 0) — so the only
thing a controller can ever learn over AECP is the static entity model, and
only once someone loads it. **No dynamic state, no counter and no CSR is
readable over AECP**: every getter draws a `NOT_IMPLEMENTED` echo. Every
observability question therefore still goes through the CSR plane over ssh,
which makes the observability groups *more* load bearing, not less. `0x6B8` is
the clearest case: it is the CSR face of counters that a controller can also
fetch with GET_COUNTERS.

## Classification

| Region | Group | Class | 2026-08-13 truth | Rationale |
|---|---|---|---|---|
| `0x000–0x00C` | ID / VERSION / CAP | **needed** | live | ABI root; VERSION gates every compatibility check made by drivers, scripts and gates. Major is now **2** (`0x0002_0043`) |
| `0x204+` | STATS_CAP + RMON counters | **needed** | live | STATS_CAP's declared-unsupported honesty is contract; RMON feeds NIC-level field triage |
| `0x4xx` | CBS queue window, classifier map | **needed** | live | Production traffic-class configuration; boot software programs it |
| `0x600–0x65x` | Identity + enables (ADP_CTRL, AAF_CTRL, …) | **needed** | **split** | `S50milan` writes these every boot. `ADP_CTRL.en` is still an entity enable — it is **ORed with `PP_CTRL[0]`**, deliberately, because it is the bit every existing board script writes and there is only one control plane now. But the ADPDU *content* words (entity_capabilities, valid_time, association_id, controller_capabilities, interface_index) and the advertise/depart strobes are **WRITE-ONLY SCRATCH**: the processor's ADP engine holds those as internal constants and exposes no port, so a write reads back and **changes nothing observable** |
| `0x618/0x61C` | ADP shape words (RO) | **needed** | live | Read-only by design since `0x0015` — and now doubly so: the same generated header sizes the processor's ACMP arrays |
| `0x624/0x628` | GM identity | **needed** | live | `milan-statd` writes them and they remain the fabric's GM truth. The processor now serves GET_AVB_INFO, but this legacy CSR pair is not its dynamic-state source |
| `0x668` | ADP_DIAG | **debug** | **STRUCTURAL ZERO** | Was already superseded by DIAG2. Its source (the deleted advertiser's depart/rearm/sent/discover census) no longer exists. **`A_ADP` available_index is the exception and is STILL LIVE** — published by the processor |
| `0x674` | ADP_DIAG2 | **optional** | **STRUCTURAL ZERO** | Created from a real field ambiguity (2026-07-30) about advertiser liveness; the advertiser it watched is deleted and the processor publishes no equivalent state word |
| `0x648–0x650` | AECP/ACMP status (locked, current config, cmd/resp counts, probe_armed) | **optional** | **STRUCTURAL ZERO** | The processor serves LOCK_ENTITY and configuration operations, but its dynamic-state outputs are not exported into this legacy CSR group. Command/response diagnostics instead live in the processor side-port snapshot window at `0x928`/`0x92C`. `probe_armed` has no fabric ACMP state machine to count. **`acmp talker_active` is the exception and remains live** through the processor's `acmp_declaring_o` |
| `0x680–0x694` | SRP CTRL / TSPEC / STATUS | **needed** | **split** | Reservation policy plus the licence word `0x694` and its `[11]` row-shortfall flag. Repointed to the processor's class-D SRP face: the **DOMAIN word (adopted/priority/VID), the granted slope and the over-limit bit are LIVE**. The **MRPDU tx/rx counts and rx drops are STRUCTURAL ZEROS** (the serializer/ingress pair that counted them is deleted), and the provisioning words the deleted applicant read — DMAC, MaxFrameSize, MaxIntervalFrames, the declare-bypass bit — are **WRITE-ONLY SCRATCH** |
| `0x6A4` | ACMPL_STATE | **optional** | **split** | Still the first stop in connection triage, but read it differently: **`bound`, `active` and bit 31 (CRF sink bound) are real**, published from the processor's bind record. The state-machine fields (state, probing, acmp_status, tk_avail, lstn_declare) and the per-sink SRP registrar bits are **STRUCTURAL ZEROS** — `ACMPL_STATE` no longer tracks PROBING/SETTLED and **a reader must take `bound` as the truth** |
| `0x6B8` | RX-monitor CSR mirror | **optional local face** | live | STREAM_INPUT counters remain readable locally and through GET_COUNTERS. STREAM_OUTPUT counters use their own `KL_talker_diag_ctx` banks and are served through the same AECP command |
| `0x6CC–0x6D4` | MAAP | **needed** | live | Address acquisition is production function, `KL_maap` survives, and the processor's talker cannot declare without an ALLOC_DA success through it — this group is now load-bearing for connectivity, not just for addressing |
| `0x6E8` | ACMPL_DBG (walker forensics) | **debug** | **STRUCTURAL ZERO** | Classify-stage byte forensics of a walker that is deleted |
| `0x730/0x734` | AS_PATH | **needed → dead end** | staging **STRUCTURAL ZERO** | The processor serves GET_AS_PATH, but this legacy CSR staging pair is not connected to that response. `0x7DC` staging accepts writes and discards them. The Table 5.22 unsolicited producer remains open |
| `0x738–0x750` | CRF group (sink + talker enable) | **needed** | live, with root integration losses | Media-clock configuration; Milan 7.3.3 class-A output. `KL_crf_rx` still parses and maintains counters. The processor accepts and stores `SET_CLOCK_SOURCE`, but the root does not export that dynamic selection, so the media plane remains pinned at 0 (INTERNAL). The CRF input counter outputs are also not connected to the solicited gather face |
| `0x778–0x780` | CLKV (tu sync lease) | **needed** | live | The tu policy is a conformance mechanism (IEEE 1722 AAF-10), not instrumentation; statd renews the lease |
| `0x784` | TXARB_DIAG | **debug** | **RENUMBERED** | The cascade collapsed from eight muxes to four. New lanes, LSB first: 0 `ctl_tx` (processor + MAAP), 1 `aaf_final`, 2 `crf_dp`, 3 `adp_tx` (MAC boundary). Bits `[7:4]` are a structural zero. **Anything decoding this word by the old numbering reads the wrong mux** |
| `0x7A0` | Bind-restore (fast-connect) | **needed → inert** | **STRUCTURAL ZERO** | Persistence: saved-state binds replayed through it. Writes are accepted, **ack never asserts, nothing is restored** |
| `0x7B8–0x7C4` | Journal ingest | **needed → inert** | **STRUCTURAL ZERO** | Milan 5.3.8.2/.3 boot replay, CRC-gated. Writes accepted and **discarded**; JNL_STAT and JNL_SEQ read structural zeros. **Nothing in this device persists a binding across a power cycle** |
| `0x7C8–0x7D4` | AEM saved-state write master | **needed → inert** | **STRUCTURAL ZERO** | It was the only path that put persisted descriptor state back. Writes accepted and discarded |
| `0x800–0x868` | Stream window (SEL/SID/FMT/CTRL/DMAC + per-stream RO views incl `A_STRMW_SRP`/`_CNT`) | **needed** | **mostly live** | The write half provisions the stream table and the RO views are the per-stream field picture — both unaffected. Two sub-ports inside the window are structural zeros: the **ACMP context-table read** (grant never asserts, record reads zero) and the **SRP attribute-row port** (no grant, no "stolen", readback zero) |
| `0x8B4–0x8C4` | APRB (RX stream-parser probe) | **debug** | live | The pre-match listener view — a scope instrument. Feature-gated (`datapath_probes`) |
| `0x8C8–0x8D0` | PBK (playback-chain probe) | **debug** | live | Same class, same gate |
| `0x8F8` | MCSRV_STAT (media-clock servo) | **optional** | **reads its IDLE** | Not a structural zero and not a live servo either: the servo is built, but its only selector input is pinned at 0, so it can never leave idle. `REGISTER_MAP` already records that this window has a dead-read carve-out — a reader cannot distinguish "no servo built" from "servo idle" here and must not try |
| `0x900–0x908` | Raw chmap WRITE window | **needed** (was *debug*) | live | **RECLASSIFIED.** The processor serves GET_AUDIO_MAP, but the audio-map writers remain unimplemented. This window is therefore the only programmer of both map RAMs, and `CHMAP_CTRL[0]` is also the crossbar arm. A production image without it cannot change a channel map |
| `0x90C` | CHMAP_STAT | **optional** | **split** | `csr_refused` is live and still means something (override disarmed). `aem_commits` and `aem_busy` are **STRUCTURAL ZEROS** — there is no projector |
| `0x910/0x914` | CHMAP_SNAP / CHMAP_LOOP (readback + LOOP_SUSPECT) | **optional** | live | Was "the auditor that catches store-vs-hardware divergence". There is no store to diverge from; it is now the **only** way to read the map back, and `LOOP_SUSPECT` (mapped & ~fed) is unchanged |
| `0x920–0x930` | PP_CTRL / PP_STAT / PP_SPADDR / PP_SPDATA / PP_DIAG | **needed** | live, **unconditional** | The protocol-processor window. `milan_csr`'s `PP_PLANE_P` parameter is **gone**, so the window is always decoded and `PP_STAT` always carries its `0x5B` tag. `PP_CTRL[0]` is ORed with `ADP_CTRL.en`. **`PP_SPADDR`/`PP_SPDATA` are how the AECP engine's own tallies are read** — command, response, drop, locate-miss, last status, last length, image-valid, image-fault all live in the processor's side-port snapshot window, not at `0x648`; the side port is the host bridge to them |
| latency-tap CSRs | AAF per-stage TX/RX taps | **debug** | live | Pure instrumentation (`latency_taps` feature) |

## The rules behind the table

1. **"Debug" is not "bench-only observability."** Registers that answer a
   field question over ssh — licence, bind state, counters, GM, the chmap
   readback — are product quality, classed *optional*, and default ON. Only
   what needs lab context beside it (captures, probes, calibration) is
   *debug*. This rule got sharper on 2026-08-13: AECP can be *asked* but
   answers only `READ_DESCRIPTOR`, so ssh is the **only** management interface
   that can read state, and dropping an *optional* group removes the last way
   to see that fact.
2. **The mapping law has been overtaken by events.** It said: one truth (the
   AEM store == the crossbar), one edit path (AECP), with the raw window as a
   bring-up bypass. There is no AEM store, and the AECP commands that would
   edit a map are unimplemented, so the raw window is the edit path and the
   read-only auditor (`0x910/0x914`) is the only readback. The law is not
   violated — there is still exactly one truth, and it is now the RAM itself.
3. **A structural zero must stay a zero.** The temptation when a source
   disappears is to leave the last value latched, or to publish a plausible
   idle. Both make a dead word indistinguishable from a working one; the
   0x668 row exists in this table *because* that word once read the same `0`
   for healthy and stalled, which is the whole reason DIAG2 was created.
   Where a group is a structural zero,
   [REGISTER_MAP.md](REGISTER_MAP.md) says so per word.
4. **Prune once, then freeze.** Removing any group shifts every window
   behind it — the DTB / driver / OpenSBI re-verification chain
   (`check_dtb_csr`, gate 19c). The production profile must be ONE
   deliberate build (`datapath_probes: false`, `latency_taps: false`,
   `0x668` retired) whose ABI is then frozen — never an incremental trim per
   release. **The structural-zero groups are the obvious prune candidates and
   are also the most dangerous ones**: they are exactly the addresses a
   deployed script already writes, so retiring them turns a harmless no-op
   into a decode fault.

Expected recovery from the full debug prune at 1×1: ~700–900 LUTs and a
simpler CSR decode — the ABI hygiene is the real value. That estimate
predates the substitution and is not re-measured here; the measured record of
what the plane change itself cost and returned is
[`../findings/PP_SHADOW_AREA_0812.md`](../findings/PP_SHADOW_AREA_0812.md).
