# Entity: KL_aecp_packet_validator
- **File:** `hdl/aecp/KL_aecp_packet_validator.sv`
- **Spec:** IEEE 1722.1-2021 §9.1, Table 9.1

First stage of the AECP pipeline. Inspects beat 0 of every incoming frame and decides pass or drop. Valid frames are forwarded beat-by-beat to `m_axis`. Dropped frames are consumed without forwarding.

**Drop conditions**

| Condition | `status_o` |
|-----------|-----------|
| `message_type ∉ {0, 6}` | `STATUS_INVALID_COMMAND` (10) |
| `control_data_length < 20` | `STATUS_BAD_ARGUMENTS` (7) |

---

## Ports

| Port | Dir | Type | Description |
|------|-----|------|-------------|
| `clk_i` | in | `wire` | 125 MHz clock |
| `rst_n` | in | `wire` | Active-low reset |
| `s_axis` | — | `axi_stream_if.slave` | Incoming AECP frames (64-bit) |
| `m_axis` | — | `axi_stream_if.master` | Forwarded valid frames |
| `valid_o` | out | `logic` | 1-cycle strobe on `tlast` of accepted frame |
| `drop_o` | out | `logic` | 1-cycle strobe on `tlast` of dropped frame |
| `status_o` | out | `logic [4:0]` | Status code for current frame |
| `message_type_o` | out | `logic [3:0]` | Latched `message_type` from beat 0 |

---

## Signals

| Name | Type | Description |
|------|------|-------------|
| `state_r` | `state_t` | FSM state |
| `msg_type_r` | `logic [3:0]` | Registered message_type |
| `status_r` | `logic [4:0]` | Registered status |
| `frame_valid_r` | `logic` | Set when beat-0 validation passes |
| `w_msg_type` | `wire [3:0]` | Combinational extract: `tdata[35:32]` |
| `w_cdl` | `wire [10:0]` | Combinational extract: `tdata[26:16]` |
| `w_ok` | `wire` | `w_type_ok & w_cdl_ok` |

---

## State machine

| State | Description |
|-------|-------------|
| `FIRST_BEAT_S` | Wait for first beat handshake; validate message_type and CDL combinationally; go to `PASS_S` or `DROP_S` |
| `PASS_S` | Forward all beats to `m_axis`; assert `valid_o` on `tlast`; return to `FIRST_BEAT_S` |
| `DROP_S` | Consume beats from `s_axis` without forwarding; assert `drop_o` on `tlast`; return to `FIRST_BEAT_S` |

---

## Timing

- Decision is purely combinational on beat 0 — no latency added.
- `valid_o` / `drop_o` are registered and pulse for exactly **one clock cycle** coincident with the `tlast` handshake.
- Back-pressure from `m_axis.tready` is fully supported in `PASS_S`.
