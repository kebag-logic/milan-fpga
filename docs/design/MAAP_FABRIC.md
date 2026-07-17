# MAAP in fabric — design + reference contract (task #18)

Goal: Milan-mandatory dynamic multicast-DMAC allocation for the talker
(today `cfg_aaf_dmac` is statically provisioned). New `hdl/maap/KL_maap.sv`
on the established monitor-tap + low-rate-TX recipe (house style, TerosHDL).

## Reference contract (byte-extracted from pipewire module-avb maap.c/h)

- Pool base `91:E0:F0:00:00:00`, size `0xFE00`; conflict compare = first
  4 bytes equal pool base, then 16-bit `{addr[4],addr[5]}` range overlap.
- Destination MAC `91:E0:F0:00:FF:00`, ethertype `0x22F0`, subtype MAAP
  (0xFE), `maap_version = 1` (hdr SUB2/status field), message_type in the
  control-AVTPDU sub1 field: PROBE=1 DEFEND=2 ANNOUNCE=3.
- PDU after the 4-byte control header: stream_id(8, sent 0) +
  request_start(6) + request_count(2) + conflict_start(6) +
  conflict_count(2). The reference sets LENGTH = sizeof(packet) = 28
  (note: 1722 says control_data_length = 16; match the REFERENCE bytes,
  golden-frame the TB against it).
- State machine: IDLE / PROBE / ANNOUNCE.
  - `make_new_address(range=8)`: offset = rand % (0xFE00 − range),
    count = range, state = PROBE, probe_count = 3,
    timeout = 500 ms + rand(0..100 ms).
  - Periodic: PROBE → send PROBE ×3 at the probe interval, then →
    ANNOUNCE; ANNOUNCE → send ANNOUNCE every 3000 ms + rand(0..2000 ms).
  - RX PROBE conflicting: if we are PROBING → new random address;
    if ANNOUNCE → send DEFEND carrying the conflict range.
  - RX DEFEND or ANNOUNCE conflicting (checks the CONFLICT fields of
    DEFEND, REQUEST fields of ANNOUNCE — reference passes p->conflict_*
    for both) → new random address unconditionally.
  - Address is valid ONLY in ANNOUNCE state (`avb_maap_get_address`
    returns EAGAIN otherwise).

## Fabric integration

- RX: tap `rx_axis_to_dma` (subtype 0xFE @ ether 0x22F0), aligned-lane
  parse (fields land in beats 1..4).
- TX: extend the low-rate TX arbiter chain (after acmpl's `ctlg` stage).
- Randomness: LFSR seeded from station MAC; interval jitter from the same.
- Outputs: `maap_addr[47:0]`, `maap_valid` (ANNOUNCE state) → datapath
  mux into the AAF framer dmac + GET_STREAM_INFO/ACMP dmac reporting when
  `MAAP_CTRL.en=1 && maap_valid`; `cfg_aaf_dmac` stays the manual lever
  (en=0 keeps today's behavior bit-exact — soft-migration like CBS bypass).
- CSR (next free after 0x6C8): `0x6CC MAAP_CTRL` (en, count[7:0]),
  `0x6D0 MAAP_STATUS` (state[1:0], valid, probe_count, offset[15:0]),
  `0x6D4 MAAP_ADDR_LO/0x6D8 _HI` (RO allocated address), conflict counter.
- NV persistence (reference load/save_state) = softcore provisioning
  (S50milan writes the last-known offset into MAAP_CTRL before enable) —
  document, not fabric.
- TB: golden frames vs the layout above; scenarios: 3-probe→announce
  walk, probe-vs-probe restart, announce-defend, defend-loss restart,
  conflict-window edges (start/end overlap), non-conflicting ranges
  ignored, LFSR re-address distribution sanity; coverage gate ≥95 %
  like avtp_rxmon.

## Open decisions

- ADP/talker gating: should PROBE_TX/streaming wait for maap_valid when
  enabled? (Milan: stream DMAC must be valid before SRP/streaming.)
  Proposal: AAF admission gate ANDs maap_valid when MAAP_CTRL.en.
- range/count: 1 stream today → count=8 like the reference (keeps the
  contract; uses index 0).

---

# Appendix: GET_DYNAMIC_INFO 0x4B contract (task #19 tail, pinned 07-17)

Reference `cmd-get-dynamic-info.c`: response = echo hdr + payload
`config_index(2)+reserved(2)` then ONE record per descriptor that carries
mutable state, in descriptor-list order. Records (BE):

| Descriptor | Record after `type(2)+index(2)` | Size |
|---|---|---|
| ENTITY | current_configuration(2)+rsvd(2) | 8 |
| AUDIO_UNIT | current_sampling_rate(4) | 8 |
| STREAM_INPUT ×2 | stream_id(8)+stream_format(8)+stream_info_flags(4)+acmp_connection_count(2)+flags_ex(1)+pbsta(1) | 28 |
| STREAM_OUTPUT | same 28-B stream record | 28 |
| CLOCK_DOMAIN | clock_source_index(2)+rsvd(2) | 8 |

Our fixed entity ⇒ FIXED response: 4 + 8 + 8 + 28×3 + 8 = 112 B payload
(+12 AECP hdr = CDL 124). All source fields already exist in the builder
(store scratch + the load_stream_info_consts / load_input_stream_info_consts
field logic + clock_src_idx/sampling-rate registers). Implement as one
DECIDE branch: SEG_ECHO(4: config_index+rsvd from cmd) + CONST/STORE
segments per record; NO_SUCH_DESCRIPTOR for config_index != 0.
IMPLEMENTATION NOTE: records interleave const-sourced (hdrs, stream_id,
flags) and store-sourced (formats, sampling rate) fields => needs ~9
segments; the builder's segment arrays (seg_kind/addr/len/cum_q[0:3]) and
the WRITE_S cum computation must grow to [0:11] first — mechanical but
touches the emit core; do it as an isolated commit with the full aecp TB
before adding the 0x4B branch.
Status: NOT yet implemented (next increment).
