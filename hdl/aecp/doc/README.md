# AECP / AEM listener — Developer Reference

**Architecture diagram:** [`atdecc_architecture.drawio`](atdecc_architecture.drawio)
([PNG](atdecc_architecture.png)) — the ATDECC (ADP + AECP/AEM) block diagram:
RX monitor tap → validator → parser → l0_state + response_builder ↔
store/accessor/dyn_mux, the ADP advertiser, the TX merge arbiters, the entity
model/generation flow, the CSR groups, and the verification setup. Regenerate
with `python3 atdecc_architecture.gen.py atdecc_architecture.drawio` (then
`atdecc_architecture.render.py` for the SVG/PNG).

**Spec:** IEEE 1722.1-2021 §9 · Milan v1.2 §5.4
**Target:** Artix-7 (AX7101 `xc7a100tfgg484` @ 100 MHz datapath; Arty @ 50 MHz)
**Package:** `hdl/aecp/aecp_pkg.sv`
**Entity model:** `avdecc/milan-v12-entity.json` → `avdecc/gen_aem_store.py`

---

## Scope (Milan v1.2 hardware entity)

One entity, **one configuration**, exactly **five descriptors**:
ENTITY → CONFIGURATION → { AVB_INTERFACE×1, AUDIO_UNIT×1, STREAM_OUTPUT×1 }.

Answered on-wire, in hardware, with no CPU involvement:

| Command | Behaviour |
|---------|-----------|
| `READ_DESCRIPTOR` | all five descriptors, live fields overlaid (entity_id, MAC, caps, available_index, current_config, clock_identity) |
| `LOCK_ENTITY` | **implemented** — grant / owner-unlock / 60 s auto-expiry; other controllers get `ENTITY_LOCKED` (owner id in payload) |
| `ACQUIRE_ENTITY` | **NOT_SUPPORTED** (Milan) — never mutates state |
| `GET/SET_CONFIGURATION` | single config; out-of-range → `BAD_ARGUMENTS` |
| `GET/SET_NAME` | writes back to the AEM store (volatile mirror) |
| `GET/SET_SAMPLING_RATE` | validated against 48/96/192 kHz |
| `GET/SET_STREAM_FORMAT` | validated against the STREAM_OUTPUT format set |
| `GET_STREAM_INFO` | Milan fixed 56-byte payload (flags 0xF6000000) |
| `GET_AVB_INFO` | read-only status |
| `GET_COUNTERS` | Milan-mandatory; ALWAYS full 136-B payload (success AND error — the Hive field-report class). STREAM_OUTPUT valid=0x1F, AVB_INTERFACE valid=0x23, values 0 until HW counters are wired |
| `ENTITY_AVAILABLE`, `REGISTER/DEREGISTER_UNSOLICITED` | acknowledged |
| MVU `GET_MILAN_INFO` | protocol_id 00-1B-C5-0A-C1-00, version 1, cert 0 (not certified) |
| anything else | `NOT_IMPLEMENTED` with the command echoed |

ADP `ENTITY_DISCOVER` for this entity pulses the advertiser's `rcv_discover_i`
(discovery response). Deferred: NV persistence / factory-reset of SET_* writes,
unsolicited-notification push, HW-backed counter values, audio maps.

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
`hdl/aecp/gen/aecp_aem_rom.svh` (produced by `avdecc/gen_aem_store.py` from the
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
