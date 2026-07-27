# Entity: KL_aecp_common_parser
- **File:** `hdl/ieee17221/aecp/KL_aecp_common_parser.sv`
- **Spec:** IEEE 1722.1-2021 §9.1, §9.2

Second pipeline stage. Extracts the fixed AECP common header from beats 0–3, forwards all beats transparently to `m_axis`, and checks `target_entity_id` against the local entity ID.

`hdr_o.hdr_valid` pulses for **one cycle** when beat 3 is accepted. Downstream modules latch `hdr_o` on that strobe.

---

## Contents

- **[Ports](#ports)** — Confirms the shape: `m_axis` is a transparent passthrough, `hdr_o` is the extracted header, and `mismatch_o` is the one verdict this stage forms — target entity ID against the local one.
- **[aecp_hdr_t fields populated](#aecp_hdr_t-fields-populated)** — The beat-and-bit map to decode against, including the two fields that straddle a beat boundary (both entity IDs). Also names what this stage deliberately leaves zeroed for the next one.
- **[State machine](#state-machine)** — One state per header beat plus a payload drain. The note under the table is the load-bearing part: the AXI-Stream signals are combinational, so beats flow through regardless of which state the FSM is in.
- **[Signals](#signals)** — Three internals, and the one worth knowing: `hdr_r` accumulates combinationally and is only registered on beat 3, which is the same edge `hdr_valid` pulses on.

## Ports

| Port | Dir | Type | Description |
|------|-----|------|-------------|
| `clk_i` | in | `wire` | 125 MHz clock |
| `rst_n` | in | `wire` | Active-low reset |
| `l0_state_i` | in | `aecp_l0_state_t` | Provides `entity_id` for mismatch check |
| `s_axis` | — | `axi_stream_if.slave` | From `KL_aecp_packet_validator` |
| `m_axis` | — | `axi_stream_if.master` | Transparent passthrough to `KL_aecp_cmd_specific_extract` |
| `hdr_o` | out | `aecp_hdr_t` | Parsed header; valid when `hdr_o.hdr_valid = 1` |
| `mismatch_o` | out | `logic` | Asserted when `target_entity_id ≠ l0_state_i.entity_id` |

---

## aecp_hdr_t fields populated

| Field | Beat | Bits |
|-------|------|------|
| `message_type` | 0 | `[35:32]` |
| `status` | 0 | `[31:27]` |
| `control_data_length` | 0 | `[26:16]` |
| `target_entity_id` | 0–1 | `[15:0]` + `[63:16]` |
| `controller_entity_id` | 1–2 | `[15:0]` + `[63:16]` |
| `sequence_id` | 2 | `[15:0]` |
| `u_flag` | 3 | `[63]` |
| `command_type` | 3 | `[62:48]` |

`configuration_index`, `descriptor_type`, `descriptor_index` — zeroed (extracted in `KL_aecp_cmd_specific_extract`, TODO).

---

## State machine

| State | Description |
|-------|-------------|
| `IDLE_S` | Wait for `tvalid`; clear `mismatch_o` |
| `BEAT0_S` | Extract message_type, status, CDL, target_eid[63:48] |
| `BEAT1_S` | Extract target_eid[47:0], ctlr_eid[63:48] |
| `BEAT2_S` | Extract ctlr_eid[47:0], sequence_id |
| `BEAT3_S` | Extract u_flag, command_type; check entity_id; assert `hdr_o.hdr_valid`; go to `PAYLOAD_S` or `IDLE_S` |
| `PAYLOAD_S` | Drain remaining payload beats transparently until `tlast`; return to `IDLE_S` |

> **Note:** AXI-Stream signals are wired combinationally (`assign`), so all beats pass through regardless of FSM state.

---

## Signals

| Name | Type | Description |
|------|------|-------------|
| `state_r` | `state_t` | FSM state register |
| `hdr_r` | `aecp_hdr_t` | Header accumulator (combinational write, registered on beat 3) |
| `w_hs` | `wire` | `s_axis.tvalid & s_axis.tready` — beat handshake |
