# Entity: KL_avtp_rx_monitor
- **File:** `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv`
- **Spec:** IEEE 1722.1-2021 Table 7-156, Milan v1.2 §5.4.5.3 / Table 5.16

Milan STREAM_INPUT diagnostic-counter engine for the bound listener sink. Consumes the per-frame pulse bundle from `avtp_stream_parser` (which already matched the bound stream_id) and maintains the counters AECP `GET_COUNTERS` serves and its unsolicited push advertises. The counting contract is byte-extracted from the pipewire module-avb reference (`stream.c handle_aaf_packet` + `cmd-get-counters.c`): first-valid-PDU lock, 8-PDU seq-settle window, mismatch/interrupt at `lost >= 2`, 100 ms silence unlock, per-PDU format compare (a mismatched PDU counts only UNSUPPORTED_FORMAT), reset on the not-bound → bound edge. MEDIA_RESET / LATE / EARLY are advertised valid but never tick (reference behavior; they land with the media-clock work). `pdu_accept_p_o` pulses for every FRAMES_RX-counted PDU — the commit verdict consumed by `KL_aaf_rx_depacketizer`.

---

## Generics

| Generic | Type | Default | Description |
|---------|------|---------|-------------|
| `CLK_FREQ_HZ_P` | `int unsigned` | `50_000_000` | Clock frequency; sizes the 100 ms unlock timeout |

## Ports

| Port | Dir | Type | Description |
|------|-----|------|-------------|
| `clk_i` | in | `wire` | Global clock |
| `rst_n` | in | `wire` | Active-low synchronous reset |
| `match_valid_i` | in | `wire` | One-cycle pulse per bound-sid-matched frame (from the parser) |
| `subtype_i` | in | `wire [7:0]` | AVTP subtype of the matched PDU |
| `seq_num_i` | in | `wire [7:0]` | sequence_num of the matched PDU |
| `ts_uncertain_i` | in | `wire` | tu bit |
| `avtp_ts_i` | in | `wire [31:0]` | Presentation time of the PDU |
| `fsh_i` | in | `wire [63:0]` | Format-specific header bytes O+16..O+23 |
| `bound_i` | in | `wire` | Listener sink 0 is bound (ACMP listener SM) |
| `fmt_i` | in | `wire [63:0]` | Current STREAM_INPUT[0] format u64 (AECP live copy) |
| `cnt_media_locked_o` | out | `logic [31:0]` | MEDIA_LOCKED (valid-mask bit 0) |
| `cnt_media_unlocked_o` | out | `logic [31:0]` | MEDIA_UNLOCKED (bit 1) |
| `cnt_stream_interrupted_o` | out | `logic [31:0]` | STREAM_INTERRUPTED (bit 2) |
| `cnt_seq_mismatch_o` | out | `logic [31:0]` | SEQ_NUM_MISMATCH (bit 3) |
| `cnt_ts_uncertain_o` | out | `logic [31:0]` | TIMESTAMP_UNCERTAIN (bit 5) |
| `cnt_unsupported_fmt_o` | out | `logic [31:0]` | UNSUPPORTED_FORMAT (bit 8) |
| `cnt_frames_rx_o` | out | `logic [31:0]` | FRAMES_RX (bit 11) |
| `media_locked_o` | out | `logic` | Current lock state (level) |
| `dirty_p_o` | out | `logic` | One-cycle pulse on any counter change (builder rate-limits pushes to 1/s) |
| `pdu_accept_p_o` | out | `logic` | One-cycle pulse per FRAMES_RX-counted PDU (depacketizer commit verdict) |
| `last_ts_o` | out | `logic [31:0]` | avtp_timestamp of the last accepted PDU (media-clock hook, CSR 0x6C8) |

## Integration

Paired with `avtp_stream_parser` (1-entry match table = the ACMP-listener bound stream_id) on the datapath RX tap; counters feed `KL_aecp_top` → `GET_COUNTERS`/unsolicited push and the CSR RO group `0x6B8-0x6C0`.
