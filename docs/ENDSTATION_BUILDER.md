# Software-defined End-Station builder — spec basis (roadmap item 4)

**Purpose.** One declarative config (`configs/endstation_*.yaml`, schema
`kebag-logic/milan-endstation-config`) drives gateware elaboration, the AEM
ROM, lwSRP tables and the DT/driver shape consistently
(`docs/MILAN_COMPLIANCE_GAPS.md` attack item 4). This document is the
specification-referenced design record for that builder: the settled design
decisions with their clause basis, and the config-schema → AEM-descriptor
mapping. Every clause reference below was verified against the PDFs in
`/home/alex/standards/` (pdftotext extraction, 2026-07-22) — the same rule as
[`SPEC_TRACEABILITY.md`](SPEC_TRACEABILITY.md). Cited documents: IEEE
1722.1-2021 ("1722.1"), IEEE 1722-2016 ("1722"), Milan Specification v1.2
Consolidated ("Milan"), IEEE 802.1Q-2022 ("Q").

The implementation lane (`sw/builder/endstation_builder.py`, the three
emitters, the `test_builder.py` identity gate against today's ROM) runs in
parallel; this document is the contract it converges on, and its rows are
meant to be promoted into the traceability matrix / CERT features per the
[`SPEC_TRACEABILITY.md`](SPEC_TRACEABILITY.md) review workflow.

## 1. Artifacts and flow

```
configs/endstation_<shape>.yaml          (single source of truth)
        │  endstation_builder.py
        ├── soc_params.json   → sw/litex/milan_soc.py design argv
        │                       (flow flags — --build, threads, directives —
        │                        stay in sw/litex/sweep.sh)
        ├── aem_overlay.json  → avdecc/gen_aem_store.py migration contract
        │                       (descriptor counts, formats, cluster/map
        │                        layout, entity identity)
        └── build_plan.md     → human review; shapes beyond current RTL
                                VALIDATE and are marked "planned"
```

Three example shapes exist: `endstation_arty_current.yaml` (today's real
Arty build — the identity gate), `endstation_arty_4x4.yaml` and
`endstation_ax7101_8x8.yaml` (the roadmap-item-5 NxN test shapes).

## 2. Settled design decisions

### D1 — one STREAM_PORT per AAF stream

**Decision.** The builder's NxN model gives every AAF stream its own
STREAM_PORT_INPUT (listeners) / STREAM_PORT_OUTPUT (talkers), each owning a
contiguous group of clusters and exactly one AUDIO_MAP. The CRF
STREAM_INPUT carries no audio channels and gets no port. Today's
1(+CRF)x1 shape degenerates to one port per direction — numerically
identical to the shipped ROM (`avdecc/gen_aem_store.py`), which is what the
v1.0 overlay gate asserts.

**Clause basis.**
- 1722.1 7.2.13 (Table 7-23): each STREAM_PORT_INPUT/OUTPUT descriptor
  carries its own `number_of_clusters`/`base_cluster` and
  `number_of_maps`/`base_map` — the cluster/map ownership boundary in AEM
  *is* the port.
- 1722.1 7.2.19: an AUDIO_MAP "contained in" a port maps channels of
  STREAM_INPUTs/OUTPUTs to channels of the AUDIO_CLUSTERs "contained in the
  same" port, and `mapping_cluster_offset` is "the offset from the
  base_cluster of the STREAM_PORT_INPUT or STREAM_PORT_OUTPUT" — map
  contents are port-relative by construction.
- Milan 5.4.2.27/5.4.2.28: the static-vs-dynamic mapping regime is decided
  **per port** ("For each Stream Port Input and for each Stream Port Output
  that has no Audio Map, the PAAD-AE shall implement the
  ADD_AUDIO_MAPPINGS command…"; ports *with* Audio Maps answer
  NOT_SUPPORTED). 1722.1 7.2.13 encodes the same split: dynamic-mapping
  entities set `number_of_maps = 0` and serve GET_AUDIO_MAP (7.4.44).

**Why.** Port-relative map offsets mean each stream's map is the identity
map over its own cluster group regardless of global cluster numbering —
adding or removing a stream never rewrites another stream's AUDIO_MAP
contents, only base indices. The 7.2.19 uniqueness rules (input: at most
one entry per cluster channel; output: at most one entry per stream channel
across the entire Configuration) hold trivially for per-port identity maps.
And because Milan's static/dynamic split is per-port, one-port-per-stream
is what later lets roadmap item 8 (dynamic maps, es-4.16) flip individual
streams to `number_of_maps = 0` without touching the rest of the model.

### D2 — cluster policy: mono cluster per stream channel (cap-at-interface rejected)

**Decision.** Schema 1.0 defines a single `cluster_mapping.rule`:
`mono-cluster-per-stream-channel` — every stream channel gets one mono
MBLA AUDIO_CLUSTER (1722.1 7.2.16/7.2.16.1), so a stream's cluster count
defaults to its channel count. The rejected alternative ("cap at
interface") would have sized the cluster space to the physical audio
interface width instead.

**Clause basis.**
- 1722.1 7.2.16: an audio cluster "describes groups of audio channels in a
  stream" with a per-cluster `channel_count` and a single `format` for all
  its channels (7.2.16.1: MBLA = Multi-bit Linear Audio) — mono clusters
  are legal and give per-channel granularity.
- Milan 6.4 (+ its note): a Stream Input that advertises one 48 kHz Base
  format shall advertise **all** 48 kHz Base formats — i.e. all channel
  counts up to 8 (Milan 6.2: N ∈ {1, 2, 4, 6, 8}). The model must be able
  to represent maps for the largest advertised format, not for the
  physical interface.
- Milan 5.3.10.1: a mapped cluster channel must reference a Stream Input
  channel "lower than the number of channels in the current format" — with
  one mono cluster per stream channel the representable map space exactly
  tiles the format family.
- Milan 5.4.2.27: a (dynamic) mapping referencing a stream channel that
  does not exist in the currently set format is invalid — cluster capacity
  and format family have to agree, and they only agree for every member of
  the ut family (1722 I.2.4) if clusters cover the maximum channel count.

**Why.** Cap-at-interface makes the AEM model a function of the hardware
SKU: an 8ch-capable Stream Input behind Arty's 2ch I2S could not represent
mappings for channels 2..7, violating the Milan 6.4 all-channel-counts
posture the moment a controller selects a wider family member. With
cluster-per-stream-channel the model is constant across interface families
and the *physical* truth lives in the binding rule instead (project
wire-truth 1-to-1 rule, `c705091`): physical interface channels bind in
order to the first clusters per direction; extra stream channels are
virtual; missing physical channels render 0. Mono clusters also match the
PipeWire reference layout the ROM was byte-derived from.

### D3 — talker cluster count as config

**Decision.** `streams.talkers[].clusters` is an explicit config field,
independent of `streams.talkers[].channels` (today's shape: 8 output
clusters, 2-channel talker framer — the shipped ROM's PipeWire reference
layout).

**Clause basis.**
- 1722.1 7.2.6 + 7.4.10.2: GET_STREAM_FORMAT returns "the current stream
  format… equivalent to the current_format field in the addressed…
  descriptor" — the *declared current format* is the contract a controller
  reads, and it must equal what the framer actually transmits
  (channels_per_frame, 1722 7.3.3: "the number of audio channels
  represented in the audio sample frame").
- Milan 5.3.7.1: a Stream Output shall always be using a format from its
  advertised formats list (one ut entry may describe the whole family).
- Milan 5.3.9.1: "each channel of each Stream Output **(in the current
  format)** is either not mapped or mapped to a channel of an Audio
  Cluster" — the map/cluster space may be larger than the current format's
  channel count; only currently-formatted channels participate.
- Milan 6.3: a talker "may advertise any Base Format that is reasonable
  for its functionality" — the advertisement is a functional choice, not a
  hardware echo.

**Why.** Wire truth and model capacity are different quantities. The
talker's `channels` is wire truth (what the framer emits — the value
GET_STREAM_FORMAT must report, and the pure-ACMP compatibility gate:
listeners with no SET_STREAM_FORMAT round-trip connect against the
*current* format). The talker's `clusters` is model shape (how much
routing capacity the entity exposes; today 8, per the reference layout).
Deriving one from the other silently is exactly the class of divergence
that produced the declared-8ch/wire-2ch silence incident — so both are
config, and the builder refuses to guess.

### D4 — entity_model_id derivation

**Decision.** `entity.entity_model_id` accepts either a pinned EUI-64 (the
form used for already-deployed silicon) or a derivation contract: a
deterministic hash of exactly the model-shaping config fields, folded into
a vendor-OUI-based EUI-64 base. Abstract contract only here — the concrete
field walk lives with the implementation lane.

**Clause basis (1722.1 6.2.2.8, all load-bearing).**
- "Different ATDECC Entity data models **shall** have different
  entity_model_id values", and "if a firmware revision changes the
  structure of an ATDECC Entity data model then it **shall** use a new
  unique entity_model_id" — any config change that alters a generated
  descriptor field must change the id.
- The clause then enumerates the fields **excluded** from "structure":
  `object_name` everywhere; ENTITY `entity_name`, `firmware_version`,
  `group_name`, `serial_number`, `available_index`, `association_id`,
  `current_configuration`; AUDIO_UNIT `current_sampling_rate`;
  STREAM_INPUT/OUTPUT `current_format`; CLOCK_SOURCE
  `clock_source_identifier`/`flags`; CLOCK_DOMAIN `clock_source_index`;
  control current values; AVB_INTERFACE `mac_address` + gPTP dynamics —
  these must **not** feed the hash, so renaming a unit, bumping
  `firmware_version`, changing a serial number or re-selecting a clock
  source never bumps the model id.
- NOTE in 6.2.2.8: "The entity_model_id is not a device's product or model
  number" — hence hash-of-model, not SKU constant.
- 6.2.2.8 also defines dynamically-assigned ids via the EUI-64 I/G bit; the
  builder does not use them (controllers may not cache descriptors for
  dynamic ids — the caching benefit is the point of a stable id).

**Why + the pin override.** Controllers cache descriptor trees keyed by
entity_model_id (the ADP-6 traceability row's field catch: reusing an id
across ROM changes serves stale models — and the inverse, gratuitous id
churn, defeats caching and can strand saved bindings, cf. 1722.1's own
note on stale connections after entity_model_id changes). Hashing the
model-shaping fields makes "model changed ⇔ id changed" structural instead
of a release-checklist item. The pin override exists because both flashed
boards already advertise fixed ids; a pinned config must reproduce them
byte-exactly, and the builder's job there is to *verify* the pin still
matches the generated model rather than to invent a new id.

### D5 — config as single source of truth (sweep flags generated)

**Decision.** The YAML config is the only place a design fact lives; the
`milan_soc.py` design argv (`soc_params.json`), the AEM overlay, and the
DT/driver shape are all emitted from it. Flow flags (`--build`,
`--vivado-max-threads`, `--place-directive`, output dirs) are explicitly
*not* end-station definition and stay in `sw/litex/sweep.sh`.

**Why (engineering, no clause needed).** Today the same fact lives in up to
four places — `sweep.sh` OPTS, `gen_aem_store.py` constants,
`milan_soc.py` defaults, the DT — and every desynchronization so far became
a field incident: declared-8ch vs wire-2ch silence, the honest-counts
provisioning round, the AEM-default-8ch trap that rejected 2ch pure-ACMP
connects. A generated artifact can be stale but never *divergent*; the
`test_builder.py` gate pins the emitted argv to `sweep.sh`'s BASE and the
overlay counts to the shipped ROM for today's shape.

**Audio-interface family subtask** (gaps item 4 subtask). The config's
`audio_interface.kind` — `tdm8|tdm16|tdm32|i2s_philips|aes3|spdif` — selects
the ser/des RTL family and its parameters (slots, word length, frame
format). In RTL today: `i2s_philips` (`KL_i2s_playback` /
`aaf_talker_i2s`/`KL_aaf_capture_i2s`, the default) and the `tdmN` kinds —
the builder emits `--audio-interface tdmN`, which `milan_soc.py` maps to
the `milan_datapath` `AUDIO_IF_SLOTS_P` generate select instantiating the
`KL_tdm_capture` TDM slave (N slots × 32-bclk words, pulse or 50%-duty
frame sync, data delay 0/1); its per-slot pair stream feeds the
`KL_aaf_packetizer` multi-channel payload builder (TCTX `chans` =
`channels_per_frame`, even 2..8 per stream, partitioning the pair-slot
space). `aes3`/`spdif` are contract-only for now (the pair-stream contract
and the biphase-mark plan live in
`hdl/ieee1722/aaf/doc/audio_frontend_family.md`) and validate with a
planned mark. On the AEM side the physical interface is modeled by,
per 1722.1:
- **JACK_INPUT/JACK_OUTPUT** (7.2.7): the physical connector, with
  `jack_type` from Table 7-12 — `SPDIF` and `AES_EBU` are dedicated types;
  TDM and I2S headers use the generic `DIGITAL` type.
- **EXTERNAL_PORT_INPUT/OUTPUT** (7.2.14): the Unit-side port "matching"
  the Jack, carrying the `signal_type`/`signal_index` chain into the unit.
- **AUDIO_UNIT** (7.2.3): "represents a single audio clock domain"; its
  external-port base/count fields and `sample_rates` list are where the
  interface's port count and the rate set surface.
- **AUDIO_CLUSTER** (7.2.16): the `signal_type`/`signal_index` fields tie
  clusters into that signal chain (INVALID for clusters on a
  STREAM_PORT_INPUT).

Today's ROM deviates knowingly: it defines **no** JACK/EXTERNAL_PORT
descriptors (deviation recorded in the `gen_aem_store.py` header — the
entity JSON's 8 external ports are not emitted). The schema reserves the
physical-side model for this subtask; the builder's capability marks call
every non-I2S `kind` "planned".

## 3. Config schema → AEM descriptor mapping

Consumers: **AEM** = `avdecc/gen_aem_store.py` (via `aem_overlay.json` —
the migration contract), **SoC** = `sw/litex/milan_soc.py` (via
`soc_params.json` argv), **DT** = device tree / `kl-eth` driver shape,
**prov** = boot-time provisioning (CSR writes: ADP identity/counts block).
"—" in the clause column = engineering fact, no normative clause governs
the field itself.

| # | Config field | Generates (descriptor / field) | Clause ref | Consumer |
|---|--------------|--------------------------------|-----------|----------|
| 1 | `entity.name` | ENTITY `entity_name` (identity only — excluded from model hash) | 1722.1 7.2.1, 6.2.2.8 | AEM |
| 2 | `entity.entity_model_id` (pin or hash, D4) | ENTITY + ADPDU `entity_model_id` | 1722.1 6.2.2.8 | AEM, prov |
| 3 | `entity.entity_id: mac-derived` | ENTITY/ADPDU `entity_id` EUI-64 from port MAC | 1722.1 6.2.2.7 | prov |
| 4 | `entity.vendor_name` / `firmware_version` / `serial_number` / `group_name` | ENTITY strings + LOCALE/STRINGS refs (all 6.2.2.8-excluded) | 1722.1 7.2.1, 7.2.11–12 | AEM |
| 5 | `board.target` + `board.constraints.*` (clk, l2, phy, flashboot, uart, probes, GMII knobs) | `milan_soc.py` design argv | — | SoC |
| 6 | `board.constraints.rx_queues` / `hs_page_bytes` | DT/driver shape (STRICT `hsplit` pairing) | — | DT |
| 7 | `clocking.sampling_rate_hz` | AUDIO_UNIT `current_sampling_rate` (6.2.2.8-excluded) | 1722.1 7.2.3 | AEM |
| 8 | `clocking.audio_unit_rates_hz` | AUDIO_UNIT `sample_rates` list | 1722.1 7.2.3 | AEM |
| 9 | `clocking.media_clock_sources` | CLOCK_SOURCE set: INTERNAL + one INPUT_STREAM per AAF listener (+ CRF, row 11) | 1722.1 7.2.9, 7.2.9.2 | AEM |
| 10 | `clocking.default_source` | CLOCK_DOMAIN `clock_source_index` reset value (6.2.2.8-excluded; persisted per Milan) | 1722.1 7.2.32; Milan 5.3.11.1 | AEM, SoC |
| 11 | `clocking.crf_sink` | CRF STREAM_INPUT (appended after AAF listeners) + its INPUT_STREAM CLOCK_SOURCE + `KL_crf_rx` instance | Milan 7.2.2; 1722.1 7.2.9.2 | AEM, SoC |
| 12 | `clocking.crf_format` | CRF STREAM_INPUT `formats` entry (48 kHz base, 1 ts/PDU, interval 96) | Milan 7.3.2 | AEM |
| 13 | `clocking.audio_pll_hz` | audio MMCM constraint (MCLK derivation) | — | SoC |
| 14 | `audio_interface.kind` | ser/des RTL family + params (`i2s_philips` = default front-end; `tdmN` → `--audio-interface` → `AUDIO_IF_SLOTS_P` / `KL_tdm_capture`; `aes3`/`spdif` contract-only); planned: JACK_IN/OUT `jack_type`, EXTERNAL_PORT_IN/OUT, AUDIO_UNIT ext-port counts (D5) | 1722.1 7.2.7 (Table 7-12), 7.2.14, 7.2.3 | SoC, AEM (planned) |
| 15 | `audio_interface.word_length_bits` | ser/des word length; bounds usable AAF `bit_depth` | 1722 7.3.4 | SoC |
| 16 | `audio_interface.cluster_mapping.rule` | AUDIO_CLUSTER + AUDIO_MAP generation policy (D2) | 1722.1 7.2.16, 7.2.19; Milan 5.3.9.1/5.3.10.1 | AEM |
| 17 | `streams.listeners[].channels` | STREAM_INPUT default `current_format` channel count (= wire `channels_per_frame`) | 1722.1 7.2.6; 1722 7.3.3; Milan 6.4 | AEM, SoC |
| 18 | `streams.listeners[].formats` | STREAM_INPUT `formats` list (ut families per Milan) | 1722.1 7.2.6; Milan 5.3.8.1, 6.5; 1722 I.2.4 | AEM |
| 19 | `streams.listeners[].buffer_length_ns` | STREAM_INPUT `buffer_length` (ns, MAC ingress buffer) | 1722.1 7.2.6 (Table 7-8) | AEM |
| 20 | `streams.listeners[].clusters` | input AUDIO_CLUSTERs (mono MBLA) + STREAM_PORT_INPUT `number_of_clusters`/`base_cluster` + identity AUDIO_MAP (D1/D2) | 1722.1 7.2.13, 7.2.16, 7.2.19 | AEM |
| 21 | `streams.talkers[].channels` | STREAM_OUTPUT `current_format` = framer wire truth (D3) | 1722.1 7.2.6, 7.4.10.2; Milan 5.3.7.1; 1722 7.3.3 | AEM, SoC |
| 22 | `streams.talkers[].formats` | STREAM_OUTPUT `formats` list | 1722.1 7.2.6; Milan 6.3 | AEM |
| 23 | `streams.talkers[].clusters` | output AUDIO_CLUSTERs + STREAM_PORT_OUTPUT bases + AUDIO_MAP (D1/D3) | 1722.1 7.2.13, 7.2.16, 7.2.19; Milan 5.3.9.1 | AEM |
| 24 | `len(listeners)` / `len(talkers)` | CONFIGURATION `descriptor_counts`; ADPDU `talker_stream_sources` / `listener_stream_sinks` (honest counts) | 1722.1 7.2.2, 6.2.2.10, 6.2.2.12 | AEM, prov |
| 25 | stream count (NxN shapes) | per-stream ACMP/MAAP/monitor contexts + per-stream lwSRP attribute instances (capacity is an implementation decision, stated in PICS) | Q 35.2.7 | SoC (planned, item 5) |
| 26 | whole config (stream/cluster/L2 counts) | build-plan `## Resource estimate`: LUT/FF/BRAM36/DSP vs xc7a100t + OK/TIGHT/OVER verdict (cost table calibrated from the real mf48 place report; NxN rows UPPER BOUND; recipe in sw/builder/README-parameters.md) | - (engineering budget; area-70 directive) | build_plan.md |
| 27 | `clocking.crf_output` (enabled + format) | CRF STREAM_OUTPUT appended after the AAF talkers (mirrors the CRF sink: no STREAM_PORT/cluster/map — it carries no audio); `stream_flags` = CLOCK_SYNC_SOURCE\|CLASS_A (0x0003); domain wiring = the STREAM descriptor's own `clock_domain_index` 0 — 7.2.9.2 defines no OUTPUT_STREAM CLOCK_SOURCE type, so the CLOCK_SOURCE/CLOCK_DOMAIN sets are unchanged; ADPDU `talker_stream_sources` +1. **RULE ENFORCED**: >=2 AAF listener streams reject without it, citing Milan 7.2.3 | Milan 7.2.3, 7.3.2 (format 0x041060010000BB80), 7.3.3 (Class A); 1722.1 7.2.6, 7.2.6.1, 7.2.9.2, 7.2.32 | AEM; SoC (provisioning planned, item 5) |

27 rows. Rows 14 (AEM half), 25, and the SoC half of 27 generate *planned*
artifacts: the config validates and the overlay is complete, but the RTL
lands with the referenced roadmap items — the build plan marks them, never
errors.

## 4. What the 8x8 shape adds (`endstation_ax7101_8x8.yaml`)

Descriptor growth under D1–D3, relative to today's 1(+CRF)x1 model
(counts per 1722.1 7.2.2 CONFIGURATION `descriptor_counts`):

| Descriptor | today | 8x8 | clause driving the count |
|------------|-------|-----|--------------------------|
| STREAM_INPUT | 2 (1 AAF + CRF) | 9 (8 AAF + CRF) | 1722.1 7.2.6; Milan 7.2.2 (CRF input stays mandatory) |
| STREAM_OUTPUT | 1 | 9 (8 AAF + CRF output) | 1722.1 7.2.6; Milan 7.2.3 (>=2 AAF inputs => CRF Media Clock Output) |
| STREAM_PORT_INPUT / _OUTPUT | 1 / 1 | 8 / 8 (D1: one per AAF stream; CRF gets none) | 1722.1 7.2.13 |
| AUDIO_CLUSTER | 16 (8 in + 8 out) | 128 (64 + 64, mono MBLA) | 1722.1 7.2.16; Milan 6.4 |
| AUDIO_MAP | 2 | 16 (one identity map per port) | 1722.1 7.2.19 |
| CLOCK_SOURCE | 3 | 10 (internal + 8× INPUT_STREAM + CRF) | 1722.1 7.2.9.2 |
| ADP `talker_stream_sources` / `listener_stream_sinks` | 1 / 2 | 9 / 9 (CRF output counted) | 1722.1 6.2.2.10 / 6.2.2.12 |

Unchanged: ENTITY, CONFIGURATION, AUDIO_UNIT (still one clock domain,
1722.1 7.2.3), AVB_INTERFACE, CLOCK_DOMAIN, CONTROL, LOCALE, STRINGS.

**New Milan obligation the shape triggers — model half DONE.** With two
or more AAF Media Inputs, Milan 7.2.3 makes a **CRF Media Clock Output**
mandatory (7.2.2 already mandates the CRF input, which we have). The
builder now ENFORCES the rule (`clocking.crf_output`, mapping row 27: a
>=2-AAF-listener config without it is a validation error citing 7.2.3)
and the overlay/`gen_aem_store.py` advertise the CRF STREAM_OUTPUT
(Milan 7.3.2 format `0x041060010000BB80`, `clock_domain_index` 0,
CLOCK_SYNC_SOURCE|CLASS_A, no audio port — mirrors the CRF sink; counts
above include it). The fabric talker exists (`KL_crf_tx`, CSRs
0x750–0x764, silicon-proven at 500 PDU/s); what still rides with the
item-5 round is the *provisioning* half: S50 boot wiring + the ACMP
talker context for the CRF stream (plus its Class-A reservation, Milan
7.3.3 — traceability M-CLK-2).

**Stays planned-item-5** (config validates, build plan marks it):
per-stream ACMP listener/talker contexts, per-stream MAAP allocations and
RX-monitor counter blocks, per-stream lwSRP registrar/declaration
instances (Q 35.2.7 — today's engine is single-stream, traceability row
SRP-9), the CRF stream's own reservation (Milan 7.3.3, Class A —
traceability M-CLK-2), and the TDM16 ser/des (item-4 audio subtask, D5).
What 8 depacketizer/framer contexts cost the AX7101 in area/timing at
100 MHz is an item-5 measurement, not a claim this document makes.

## 5. Relation to CERT and the traceability matrix

The builder does not add new normative behavior — it *generates* the
artifacts whose behavior the existing rows already verify (AEM-1..8,
M-FMT-1/2, ADP-7 honest counts, M-AECP-4 static-maps posture). Its own
gates are: (a) the `test_builder.py` identity gate — today's config must
reproduce the shipped ROM's descriptor counts and `sweep.sh`'s design argv
byte-for-byte; (b) on migration, `gen_aem_store.py` consuming the overlay
must keep the CERT suite green on both boards (63/63 posture) with an
unchanged entity_model_id for an unchanged model (D4). Any new descriptor
content the NxN shapes introduce (per-stream ports/maps, CRF output) gets
new traceability rows before it gets RTL, per the matrix's review
workflow.
