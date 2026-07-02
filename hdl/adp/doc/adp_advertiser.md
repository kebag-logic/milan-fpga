# `adp_advertiser` — ADP transmit engine (design doc)

**Module:** [`hdl/adp/adp_advertiser.sv`](../adp_advertiser.sv)
**Verification:** [`tb/verilator/adp/`](../../../tb/verilator/adp) — 121 self-checks, PASS
**Standards:** IEEE 1722.1-2021 §6 (ADP), AVnu **Milan v1.2** Discovery
**Requirements:** FR-DISC-01..04 ([`FR_NFR.md`](../../../docs/FR_NFR.md),
[`MILAN_V12_DEPENDENCY_MATRIX.md`](../../../docs/MILAN_V12_DEPENDENCY_MATRIX.md) §A)

## 1. Purpose

The repo already decodes received ADPDUs (`KL_adp_parser.sv`) but had **no
transmit side** — nothing advertised the entity. `adp_advertiser` is that missing
half: it runs the ADP advertise / departing / discover-response behaviour and
serialises a **byte-exact ADPDU Ethernet frame** onto a 64-bit AXI4-Stream master,
ready to inject into the MAC TX path. It reuses the field set and constants in
[`adp_pkg.sv`](../adp_pkg.sv).

Why this block is in **hardware** (not the Linux AVDECC stack): advertising is
periodic, low-jitter, and must survive CPU load / be available the instant the
link comes up — exactly what a small FSM does better than software. The rest of
AVDECC (AECP/ACMP/MAAP) stays in software (see the migration plan §B.0).

## 2. Emitted frame — byte-exact layout

Total **82 bytes** = 14 B Ethernet + 68 B ADPDU. `control_data_length = 0x38`
(= 56, the ADP-specific bytes after `entity_id`). AXIS byte lane 0 (`tdata[7:0]`)
carries the **first** byte on the wire.

| Bytes | Field | Source |
|-------|-------|--------|
| 0–5 | dst MAC = **91:E0:F0:01:00:00** | AVDECC ADP multicast (const) |
| 6–11 | src MAC | `station_mac_i` |
| 12–13 | EtherType = **0x22F0** | `AVTP_ETHERNET_TYPE_C` |
| 14 | subtype = **0xFA** | `ADP_SUBTYPE_C` |
| 15 | sv(1)=0, ver(3)=0, **message_type**(4) | latched `tx_msg` (0/1/2) |
| 16 | valid_time(5) ‖ cdl[10:8]=0 | `valid_time_i` |
| 17 | cdl[7:0] = **0x38** | `CTRL_DATA_LENGTH_C` |
| 18–25 | entity_id | `entity_id_i` |
| 26–33 | entity_model_id | `entity_model_id_i` |
| 34–37 | entity_capabilities | `entity_capabilities_i` |
| 38–39 / 40–41 | talker_stream_sources / talker_capabilities | inputs |
| 42–43 / 44–45 | listener_stream_sinks / listener_capabilities | inputs |
| 46–49 | controller_capabilities | input |
| 50–53 | **available_index** | internal counter (latched) |
| 54–61 | gptp_grandmaster_id | `gptp_grandmaster_id_i` |
| 62 | gptp_domain_number | input |
| 63 | reserved = 0 | — |
| 64–65 / 66–67 / 68–69 | current_configuration_index / identify_control_index / interface_index | inputs |
| 70–77 | association_id | input |
| 78–81 | reserved = 0 | — |

All multi-byte fields are network (big-endian) order. These offsets match
`srcs/milan-tests-avb/controller/avdecc_l2.py::parse_adp` — i.e. what a real
controller decodes — which is exactly what the harness re-checks.

On the bus: **11 beats** of 8 bytes; the last beat carries 2 valid bytes
(`tkeep = 0x03`, `tlast = 1`).

## 3. Behaviour

### 3.1 Events → message
| Trigger | Message | `available_index` |
|---------|---------|-------------------|
| `link_up_i` (enabled) | ENTITY_AVAILABLE | **+1** (entity (re)available) |
| `gm_change_i` / `info_changed_i` | ENTITY_AVAILABLE | **+1** (advertised data changed) |
| `rcv_discover_i` | ENTITY_AVAILABLE | unchanged |
| periodic timer (`tick_i`) | ENTITY_AVAILABLE | unchanged |
| `link_down_i` / `shutdown_i` | ENTITY_DEPARTING | unchanged |

`available_index` is the controller's change-detector: it **must** advance on a
real change and **must not** advance on a plain re-advertisement or a discover
response, or controllers would think the model changed and needlessly re-enumerate.
The harness explicitly checks both directions.

### 3.2 Timing
`tick_i` is a **1-second** strobe (a 1PPS / prescaled-1 s pulse). The entity
re-advertises every `valid_time_i` seconds; because ADP validity is `2·valid_time`
seconds, re-advertising each `valid_time` s keeps the network entry fresh with
margin. `valid_time_i = 0` is treated as 1 to avoid a zero period.

### 3.3 FSM
Two states: `S_IDLE` (waiting) and `S_SEND` (serialising). A one-deep pending
request (`send_pending_r`, `pend_msg_r`, `pend_bump_r`) is captured by a
priority arbiter (depart > link-up > info/gm-change > discover > timer) and
consumed when a frame starts. The AXIS outputs are **combinational** functions of
the registered `state_r`/`beat_r` (the standard source pattern — data/valid track
the beat index with no handshake lag); `beat_r` advances only on an accepted beat
(`tready`), so the block is fully back-pressure safe.

## 4. Interface → CSR mapping

The quasi-static inputs come from the `milan_csr` ADP/identity registers (to be
added under the `0x000`/identity group); `available_index_o` is a RO readback and
must equal what ADP advertises (FR-DISC-04) and the ENTITY descriptor. `tick_i`
comes from a 1 s prescaler off the PHC/`axis_clk`. Events map to: link status
(from the MAC/PHY), `rcv_discover_i` from `KL_adp_parser.rcv_adp_discover_o`,
`gm_change_i` from the gPTP block, `info_changed_i` from any CSR write that
changes an advertised field, `shutdown_i` from a CSR bit.

## 5. Verification (what the harness proves)

[`tb/verilator/adp/sim_main.cpp`](../../../tb/verilator/adp/sim_main.cpp) drives the
events and **decodes the emitted frame like a controller**, asserting (121 checks):
- Ethernet header (dst/src/type), subtype, `control_data_length`, `valid_time`;
- every entity field byte-exact against the driven model;
- `message_type` per scenario (AVAILABLE vs DEPARTING);
- `available_index` semantics (bump on change; hold on re-advertise/discover;
  monotonic; never bumped by depart);
- the periodic timer fires after `valid_time` ticks;
- **byte-for-byte integrity under AXIS back-pressure** (toggled `tready`);
- no advertisement is emitted once departed.

Run: `cd tb/verilator/adp && make` → `RESULT: PASS`.

## 6. Integration status & next steps
- **Done:** RTL + Verilator harness (this block), byte-exact, lint-clean, PASS.
- **Done — CSR wiring:** the identity/control inputs come from the `milan_csr`
  **0x600 ADP group** (`docs/REGISTER_MAP.md`); `available_index_o` reads back at
  `ADP_STATUS`. `station_mac_i` = `MAC_ADDR`. Software strobes `ADP_CMD[0]`
  (advertise/field-change) → `info_changed_i`, `ADP_CMD[1]` (depart) → `shutdown_i`.
  CSR harness extended (62 checks, PASS).
- **Done — MAC TX integration:** [`adp_tx_arbiter.sv`](../adp_tx_arbiter.sv) merges
  the ADP stream with the datapath into the MAC TX between frames (never mid-frame);
  verified in [`tb/verilator/adp_tx/`](../../../tb/verilator/adp_tx) (26 checks, PASS).
  Wired in `milan_top.sv` (advertiser + arbiter + 1 s tick + link-edge pulses); all
  ports connectivity-checked; `milan_top` elaborates the ADP modules cleanly.
- **Next:** `rcv_discover_i` and `gm_change_i` are tied 0 pending the `KL_adp_parser`
  RX tap (§B.1) and gPTP GM tracking; `link_up` is still tied high (REQ-MAC-03) so the
  advertise pulse fires once on power-up. On real hardware/LiteX, a controller then
  sees the entity appear (M-B2 complete) once those events are live.
