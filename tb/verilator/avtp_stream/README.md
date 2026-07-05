# avtp_stream — AVTP stream parser verification

Self-checking Verilator harness for `hdl/1722/avtp_stream_parser.sv`, the first RTL
increment of the **AVTP stream engine** (S1 / hook A in
`docs/AVB_SWITCH_DIRECTION.md`).

The parser is a **non-intrusive monitor** on the RX AXI-Stream: it parses each
frame's Ethernet + AVTP common-stream header and, for AVTP *stream* subtypes
(AAF/CVF/… with `sv=1`) whose `stream_id` matches a programmable table, emits one
metadata pulse per frame carrying the matched index, the 64-bit `stream_id`, the
32-bit presentation timestamp and the subtype. A later increment routes the sample
payload into that stream's sample ring so PipeWire wakes per audio period, not per
packet.

`make` builds and runs. Checks (21): stream-id / presentation-time / subtype / `tv`
extraction for untagged **and** C-VLAN-tagged frames, the programmable stream match
(index + `avtp_frames`/`matched_frames` counters), and the reject cases — unknown
stream-id, control subtypes (ADP/AECP/…), `sv=0`, and non-AVTP (IPv4) frames.
