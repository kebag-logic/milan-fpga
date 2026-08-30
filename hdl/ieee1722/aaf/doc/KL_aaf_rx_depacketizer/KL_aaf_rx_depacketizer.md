# Entity: KL_aaf_rx_depacketizer
- **File:** `hdl/ieee1722/aaf/KL_aaf_rx_depacketizer.sv`
- **Spec:** IEEE 1722-2016 AAF (Section 7 / Table 18 layouts); Milan v1.2 base audio formats

AAF RX payload extractor — the media half of the Milan listener. It taps the RX
AXI-Stream without ever backpressuring the MAC path, buffers every frame through
a drop-capable frame FIFO, and emits only the AAF sample payload (bytes O+24 ..
O+24+data_len−1, wire byte order = S32BE interleaved PCM) as one AXIS frame per
PDU toward the fabric route, render map and receive-to-talker loopback tap.

The accept/kill verdict is not re-derived: `KL_avtp_rx_monitor_ctx.pdu_accept_p`
(bound + stream_id + current-format match) arrives at parse-complete (frame byte
48) — always before `tlast` of any real AAF PDU (≥ 230 B) — and clears the
frame's bad-by-default marker before FIFO commit. The fabric payload output
therefore carries exactly the PDUs FRAMES_RX counts.

Payload realignment strips 38 (untagged) or 42 (C-VLAN) header bytes via a hold-register rotation (rotate-2 / rotate-6); the read side re-parses the buffered header (VLAN flag from bytes 12..13, `data_len` from O+20..21). Output beats are always full 8-byte words — Milan base-format payloads are 8-byte multiples (192 B @48 kHz, 384 B @96 kHz, 768 B @192 kHz); a non-multiple `data_len` is zero-padded in the final beat.

---

## Contents

- **[Generics](#generics)** — One parameter, the frame-FIFO depth, and what happens when it is too small: whole frames are dropped, and the count comes out on `drops_o`.
- **[Ports](#ports)** — Note the shape, not just the names: the `s_*` side is a tap the module only *observes* (`s_tready_i` is an input it watches, never drives), the output `tkeep` is always `0xFF` because Milan base payloads are emitted as whole words, and the two counters are the halves of CSR `0x6C4`.
- **[Integration](#integration)** — Where it sits beside the parser/monitor pair and how the accepted payload fans out to fabric render and loopback consumers.

## Generics

| Generic | Type | Default | Description |
|---------|------|---------|-------------|
| `FIFO_DEPTH_BYTES` | `int` | `2048` | Frame FIFO depth (BRAM); overflow drops whole frames, counted in `drops_o` |

## Ports

| Port | Dir | Type | Description |
|------|-----|------|-------------|
| `clk_i` | in | `wire` | Global clock |
| `rst_n` | in | `wire` | Active-low synchronous reset |
| `s_tdata_i` | in | `wire [63:0]` | RX tap data (little lane order, observed only) |
| `s_tkeep_i` | in | `wire [7:0]` | RX tap keep |
| `s_tvalid_i` | in | `wire` | RX tap valid |
| `s_tready_i` | in | `wire` | RX tap ready (observed) |
| `s_tlast_i` | in | `wire` | RX tap last |
| `pdu_accept_p_i` | in | `wire` | Commit verdict pulse from `KL_avtp_rx_monitor` |
| `m_axis_tdata` | out | `logic [63:0]` | PCM payload beat (full 8 bytes, wire order) |
| `m_axis_tkeep` | out | `logic [7:0]` | Always `0xFF` (whole-word base-format payload) |
| `m_axis_tvalid` | out | `logic` | Payload beat valid |
| `m_axis_tlast` | out | `logic` | One AXIS frame per AAF PDU |
| `m_axis_tready` | in | `wire` | Fabric-consumer readiness (absorbed by the FIFO, never the RX tap) |
| `pdus_o` | out | `logic [15:0]` | Payloads emitted to the fabric path (CSR 0x6C4 [15:0]) |
| `drops_o` | out | `logic [15:0]` | Whole frames lost to FIFO overflow (CSR 0x6C4 [31:16]) |

## Integration

Instantiated in `milan_datapath` next to the parser/monitor pair on the RX tap.
Its `m_axis_*` payload enters `KL_pcm_route`; accepted beats are also cloned,
without backpressure, into `KL_chan_map_render` and the capture map's LOOP
bucket. No listener sample interface leaves the datapath.
