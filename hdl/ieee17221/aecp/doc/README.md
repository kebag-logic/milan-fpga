# AECP / AEM listener — Developer Reference

**Architecture diagram:** [`atdecc_architecture.drawio`](atdecc_architecture.drawio)
— MULTI-PAGE: page 1 is the block overview ([PNG](atdecc_architecture.png));
pages 2–8 give every displayed block its own description, drilling from the
block's role down to bit level (frame byte maps, FSM states, segment programs
with CDLs, ROM/overlay/CSR address maps):
2-ingress · 3-validator-parser · 4-l0-timers · 5-response-builder ·
6-aem-store · 7-adp-advertiser · 8-tx-csr · 9-hw-sw-split (the softcore
delimitation; normative text in docs/ARCHITECTURE_HW_SW_SPLIT.md).
Per-page PNG/SVG alongside.
Regenerate with `python3 atdecc_architecture.gen.py atdecc_architecture.drawio`
(then `atdecc_architecture.render.py` renders every page to SVG/PNG).

**Spec:** IEEE 1722.1-2021 §9 · Milan v1.2 §5.4
**Target:** Artix-7 (AX7101 `xc7a100tfgg484` @ 100 MHz datapath; Arty @ 50 MHz)
**Package:** `hdl/ieee17221/aecp/aecp_pkg.sv`
**Entity model:** `avdecc/milan-v12-entity.json` → `avdecc/gen_aem_store.py`

---

## Scope (Milan v1.2 hardware entity)

One entity, **one configuration**, exactly **five descriptors**:
ENTITY → CONFIGURATION → the FULL Milan mandatory set (FR-ENUM-02, 34
descriptors): AUDIO_UNIT, STREAM_INPUT×2 (AAF + CRF), STREAM_OUTPUT,
AVB_INTERFACE, CLOCK_SOURCE×3, CLOCK_DOMAIN, CONTROL (IDENTIFY), LOCALE,
STRINGS, STREAM_PORT_IN/OUT, AUDIO_CLUSTER×16, AUDIO_MAP×2.

Answered on-wire, in hardware, with no CPU involvement:

| Command | Behaviour |
|---------|-----------|
| `READ_DESCRIPTOR` | all 34 descriptors, live fields overlaid (entity_id, MAC, caps, available_index, current_config, clock_identity) |
| `LOCK_ENTITY` | **implemented** — grant / owner-unlock / 60 s auto-expiry; other controllers get `ENTITY_LOCKED` (owner id in payload) |
| `ACQUIRE_ENTITY` | **NOT_SUPPORTED** (Milan) — never mutates state |
| `GET/SET_CONFIGURATION` | single config; out-of-range → `BAD_ARGUMENTS` |
| `GET/SET_NAME` | generated name directory (all named descriptors); writes back to the AEM store (volatile mirror) |
| `GET/SET_SAMPLING_RATE` | validated against 48/96/192 kHz |
| `GET/SET_STREAM_FORMAT` | validated against the STREAM_OUTPUT format set |
| `GET/SET_CLOCK_SOURCE` | CLOCK_DOMAIN[0], sources 0..2 (Internal / AAF / CRF), store write-back |
| `GET/SET_CONTROL` | CONTROL[0] IDENTIFY (LINEAR_UINT8 step 255 → 0/255 only); level exported on `identify_o` → board LED |
| `GET_AUDIO_MAP` | static default maps (AUDIO_MAP[0]/[1]) via STREAM_PORT_IN/OUT; `ADD/REMOVE_AUDIO_MAPPINGS` → `NOT_SUPPORTED` |
| `GET_STREAM_INFO` | Milan fixed 56-byte payload (flags 0xF6000000) |
| `GET_AVB_INFO` | read-only status |
| `GET_AS_PATH` | Milan-mandatory; count=1, path[0] = MAC-derived EUI64 clock_identity (matches the AVB_INTERFACE descriptor overlay) |
| `GET_COUNTERS` | Milan-mandatory; ALWAYS full 136-B payload (success AND error — the Hive field-report class). STREAM_OUTPUT valid=0x1F (**live** STREAM_START/STOP from the talker SM, FRAMES_TX from the AAF framer), AVB_INTERFACE valid=0x23 (**live** LINK_UP/DOWN, GPTP_GM_CHANGED), STREAM_INPUT valid=0xF3F (**live** KL_avtp_rx_monitor: MEDIA_LOCKED/UNLOCKED, STREAM_INTERRUPTED, SEQ_NUM_MISMATCH, TIMESTAMP_UNCERTAIN, UNSUPPORTED_FORMAT, FRAMES_RX; MEDIA_RESET/LATE/EARLY advertised-zero like the pipewire reference). Counter changes push unsolicited GET_COUNTERS(STREAM_INPUT 0), rate-limited 1/s per Milan §5.4.5 |
| `SET/GET_MAX_TRANSIT_TIME` | 0x4C/0x4D (la_avdecc-verified codes; 0x4B = GET_DYNAMIC_INFO); u64 ns onto the same presentation offset as SET_STREAM_INFO(ACC_LAT) |
| `ENTITY_AVAILABLE`, `REGISTER/DEREGISTER_UNSOLICITED` | acknowledged; 4-slot unsolicited push engine |
| MVU `GET_MILAN_INFO` | protocol_id 00-1B-C5-0A-C1-00, version 1, cert 0 (not certified) |
| MVU `SET/GET_SYSTEM_UNIQUE_ID` | Milan-1.2 wire form (reserved16 + 32-bit id), volatile |
| MVU `SET/GET_MEDIA_CLOCK_REFERENCE_INFO` | 74-B info block; flags bit0 = user priority (default 192, audio-interface class), bit1 = domain name (64 B store scratch) |
| anything else | `NOT_IMPLEMENTED` with the command echoed (incl. `GET_DYNAMIC_INFO` 0x4B — deferred SHOULD) |

ADP `ENTITY_DISCOVER` for this entity pulses the advertiser's `rcv_discover_i`
(discovery response). Deferred: NV persistence / factory-reset of SET_* writes,
GET_DYNAMIC_INFO, dynamic audio-map edits.

---

## Pipeline

```
MAC RX (post-filter, monitor tap — reads only, never backpressures the NIC)
        │
        ▼
KL_aecp_ingress        — filter AECP-for-us / ADP-discover; store-and-forward;
        │                strip Eth header; replay big-lane; capture src MAC
        ▼
KL_aecp_packet_validator — drop bad message_type / CDL < 12
        ▼
KL_aecp_common_parser    — aecp_hdr_t, entity_id match (beat 0 IS the first
        │                  accepted beat — no dead IDLE cycle)
        ├───────────────► KL_aecp_l0_state  (LOCK / ACQUIRE-unsupported / config)
        ▼
KL_aecp_response_builder — capture payload, classify, SET_* write-back,
        │  ▲               serialise the response frame (little lane / MAC order)
        ▼  │ st_byte (overlaid)
KL_aecp_aem_store ──► KL_aecp_aem_dyn_mux   (ROM image + live-field overlay)
        (KL_aecp_accessor resolves descriptor -> {base,len})
        │
        ▼
response AXIS ──► low-rate arbiter (ADP + AECP) ──► datapath TX arbiter ──► MAC
```

`KL_aecp_top` wires it all; the store read address is delayed one cycle into the
overlay mux to align with the store's 1-cycle data latency.

The generated descriptor ROM + directory + overlay map is
`hdl/ieee17221/aecp/gen/aecp_aem_rom.svh` (produced by `avdecc/gen_aem_store.py` from the
entity JSON — never hand-edit it). The command decode and response-frame
assembly (the planned `cmd_specific_extract` / `accessor` / `egress_mux` /
`vu_milan` stages) are folded into `KL_aecp_response_builder` +
`KL_aecp_top` for a tight, single-FSM implementation.

---

## AXI-Stream beat layout (64-bit, big-endian inside the AECP pipeline)

The ingress replays the frame from the EtherType onward, in big lane order
(`tdata[63:56]` = first byte) — the order the parser chain expects. The response
builder emits little lane order (`tdata[7:0]` = first wire byte) — the MAC/
Forencich convention. VU frames have **no** u/command_type after `sequence_id`:
`protocol_id(6)` follows immediately (AEM frames put u+command_type there).

---

## CSR (milan_csr, read-only status)

| Offset | Field |
|--------|-------|
| `0x648` | `[16]` locked · `[15:0]` command count |
| `0x64C` | `[31:16]` response count · `[15:0]` current_configuration |

Enable/identity come from the ADP `0x600` group (`cfg_adp_enable`, entity_id,
caps, MAC, gPTP GM/domain, available_index) — ADP and AEM can never disagree.

---

## Implementation status

| Module | Status |
|--------|--------|
| `KL_aecp_ingress` | ✅ RX filter + big-lane replay + src-MAC capture + ADP-discover |
| `KL_aecp_packet_validator` | ✅ |
| `KL_aecp_common_parser` | ✅ (beat-0 fix + beat-3 field extraction) |
| `KL_aecp_l0_state` | ✅ Milan LOCK / ACQUIRE-not-supported |
| `KL_aecp_timers` | ✅ (parameterised clock) |
| `KL_aecp_accessor` | ✅ directory lookup |
| `KL_aecp_aem_store` | ✅ generated ROM + SET_* write-back (volatile) |
| `KL_aecp_aem_dyn_mux` | ✅ live-field overlay |
| `KL_aecp_response_builder` | ✅ full command set + segmented frame builder |
| `KL_aecp_top` | ✅ subsystem wiring |

---

## Verification

- **Unit / subsystem:** `tb/verilator/aecp` — 61 self-checks across READ_DESCRIPTOR
  (all 5), ACQUIRE→NOT_SUPPORTED, LOCK grant/deny/unlock, GET/SET_CONFIGURATION,
  SET_NAME+readback, SET_SAMPLING_RATE valid/invalid, GET_COUNTERS (full-size
  on every status), MVU GET_MILAN_INFO, entity-id filtering, ADP-discover pulse. Run: `cd tb/verilator/aecp && make run`.
- **Datapath integration:** `tb/verilator/milan_dp` (17 checks) exercises the
  full `milan_datapath` with the listener in place — no NIC regression.
- **Lint:** `scripts/run-verilator-lint.sh` (per-module + full `KL_aecp_top`).
- **Co-sim:** `tb/verilator/aecp/cosim_driver.py` — tsn-gen builds/parses the
  frames, the real `KL_aecp_top` RTL answers over an AxiStreamBeat socket (36/36).
- **la_avdecc (Hive's library):** `enum_probe.cpp` on the AVB peer — full
  controller enumeration with strict payload-size validation. Verdict on silicon:
  entity ONLINE, IEEE17221=1. NOTE: compile the probe with la_avdecc's OWN feature
  defines (`-DENABLE_AVDECC_FEATURE_CBR/JSON/REDUNDANCY
  -DENABLE_AVDECC_STRICT_2018_REDUNDANCY` + nlohmann include) — a bare g++ build
  ABI-mismatches the lib and crashes on the first virtual call.
- **Silicon:** `avdecc/milan_controller.py <iface>` on the AVB-segment peer drives
  the real AECP exchange (24 checks). Reads status back over CSR `0x648/0x64C`.
