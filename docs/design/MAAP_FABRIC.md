# MAAP in fabric — design + reference contract (task #18)

Goal: Milan-mandatory dynamic multicast-DMAC allocation for the talker
(before this, `cfg_aaf_dmac` was statically provisioned).
[`hdl/ieee1722/maap/KL_maap.sv`](../../hdl/ieee1722/maap/KL_maap.sv)
on the established monitor-tap + low-rate-TX recipe (house style, TerosHDL).

> **AS-BUILT:** `KL_maap` ([`hdl/ieee1722/maap/KL_maap.sv`](../../hdl/ieee1722/maap/KL_maap.sv)) is implemented in
> fabric and silicon-proven — no longer a plan/future item. The design +
> reference contract below is the as-built spec; the CSR block has been
> reconciled to REGISTER_MAP.
>
> **AND IT SURVIVED THE SUBSTITUTION (2026-08-13).** When this repository's
> own ADP / ACMP / AECP / lwSRP planes were deleted in favour of the pinned
> `protocol-processor` submodule, `KL_maap` stayed as the selected shipping
> allocator. The processor now also contains an internal `KL_pp_maap` engine,
> but this integration holds it disabled with `cfg_maap_internal_i = 0` and
> uses the processor's **per-source ALLOC_DA / RELEASE_DA face** instead.
> [`hdl/milan/KL_pp_maap_shim.sv`](../../hdl/milan/KL_pp_maap_shim.sv)
> bridges the two models and [`hdl/milan/milan_datapath.sv`](../../hdl/milan/milan_datapath.sv)
> wires it between them. So this engine is the active MAAP engine in this
> repository's own RTL, and the talker half of
> the processor's ACMP is dead by construction without it -- see [Fabric
> integration](#fabric-integration).

## Contents

- **[Reference contract (byte-extracted from an independent AVB implementation)](#reference-contract-byte-extracted-from-an-independent-avb-implementation)** -- The wire bytes and the IDLE/PROBE/ANNOUNCE machine as the reference implementation actually behaves, including the deliberate quirk: the reference sets LENGTH = 28 where 1722 says `control_data_length` = 16, and we match the reference bytes. Also the rule that the address is only valid in ANNOUNCE.
- **[Fabric integration](#fabric-integration)** -- Where `KL_maap` attaches (RX monitor tap on subtype 0xFE; TX as the second leg of the ONE control-lane merge), the `MAAP_CTRL.en=0` soft-migration that keeps `cfg_aaf_dmac` behaviour bit-exact, and the CSR block reconciled to `REGISTER_MAP`; note there are no ADDR_LO/HI registers, the DMAC is the pool base plus the claimed offset in `0x6D0`.
- **[The block ⇄ per-source bridge (KL_pp_maap_shim)](#the-block--per-source-bridge-kl_pp_maap_shim)** -- How one block claim answers N per-source ALLOC_DA requests, why `s` gets `base + s`, why a refusal is a state and not an error, and why RELEASE frees nothing.
- **[Open decisions](#open-decisions)** -- Both are now SETTLED, and the load-bearing one settled itself structurally: AAF admission ANDs the DA because the declaration cannot exist without it.
- **[Appendix: GET_DYNAMIC_INFO 0x4B contract](#appendix-get_dynamic_info-0x4b-contract)** -- Unrelated to MAAP. Records the current IEEE 1722.1-2021 batch contract and points to the processor implementation.

## Reference contract (byte-extracted from an independent AVB implementation)

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
- **TX: the second leg of the ONE control-lane merge.** The TX arbiter
  cascade collapsed from eight muxes to four when the planes that fed the
  other merges were deleted; what is left on the control lane is
  `ctl_tx_mux`, whose two sources are the protocol processor's packed TX
  (ADP + ACMP + SRP, internally arbitrated) and **MAAP's
  probe/defend/announce**. The selected processor pin also contains
  `KL_pp_maap`, but this integration ties `cfg_maap_internal_i` low and
  selects the fabric `KL_maap` leg through `KL_pp_maap_shim`. Lane 0 of
  `A_TXARB_DIAG 0x784` supervises that merge — **anything decoding `0x784` by
  the old eight-lane numbering now reads the wrong mux.**
- Randomness: LFSR seeded from station MAC; interval jitter from the same.
- Outputs: `maap_addr[47:0]`, `maap_valid` (ANNOUNCE state) → the datapath's
  `eff_aaf_dmac` mux into the AAF framer dmac when
  `MAAP_CTRL.en=1 && maap_valid`, **and** the block side of
  `KL_pp_maap_shim`, which is how the processor's talker learns a source's
  destination address. `cfg_aaf_dmac` stays the manual lever (en=0 keeps the
  pre-MAAP behavior bit-exact — soft-migration like CBS bypass).
- CSR ([`REGISTER_MAP.md`](../reference/REGISTER_MAP.md) is authoritative;
  the block below mirrors its `0x6CC`-`0x6D4` rows): `0x6CC MAAP_CTRL` (RW, reset `0x0800`: `[0]` en,
  `[1]` seed_valid, `[15:8]` block count (default 8), `[31:16]` seed offset),
  `0x6D0 MAAP_STAT0` (RO: `[31:24]` conflicts, `[23:16]` DEFENDs sent,
  `[15:0]` claimed offset), `0x6D4 MAAP_STAT1` (RO: `[2]` addr_valid
  (= ANNOUNCE state), `[1:0]` state). There are NO separate ADDR_LO/ADDR_HI
  registers — the allocated DMAC is 91:E0:F0:00 + claimed offset.
- NV persistence (reference load/save_state) = softcore provisioning
  (S50milan writes the last-known offset into MAAP_CTRL before enable) —
  document, not fabric. Note that **nothing else in this device persists
  across a power cycle any more**: the saved-state journal died with the AECP
  plane and the processor's AECP µCPU did not bring persistence back — there
  is no saved state and no fast-connect — so a boot-time MAAP_CTRL seed is the
  only continuity there is.
- TB: golden frames vs the layout above; scenarios: 3-probe→announce
  walk, probe-vs-probe restart, announce-defend, defend-loss restart,
  conflict-window edges (start/end overlap), non-conflicting ranges
  ignored, LFSR re-address distribution sanity; coverage gate ≥95 %
  like avtp_rxmon.

## The block ⇄ per-source bridge (`KL_pp_maap_shim`)

`KL_maap` claims **one contiguous block** — a base plus `count` addresses —
and publishes `addr_valid_o` only while it is in ANNOUNCE (probed, and being
defended). It has no notion of a source. The processor asks **per source**: a
held valid/ready `ALLOC_DA` / `RELEASE_DA` naming one source index, answered
by exactly one response carrying a 48-bit DA, plus a per-source conflict
event. The shim is the whole of the translation, and its own header is
authoritative; the four decisions worth knowing here:

- **Source `s` gets `base + s`** — already this fabric's convention
  (`eff_aaf_dmac + j` for stream *j*, and the CRF talker on the same rule), so
  the processor's talker declares exactly the address the AAF framer puts on
  the wire. Any other mapping would have two planes disagree about one
  stream's DA.
- **`ready` means "no response is already in flight", not "the block is
  valid".** A request is accepted immediately and answered `ok = 0` when the
  block cannot back it, because the processor's MAAP event sits on the same
  single walker that serves PROBE_TX / DISCONNECT_TX / GET_TX_STATE for every
  source: parking that walker for the ~1.5 s a legal PROBE takes would make
  the talker half of ACMP deaf while the fabric is doing exactly what it is
  supposed to. The refusal costs two cycles and reaches the identical end
  state — the source stays without a DA and PROBE_TX answers
  `TALKER_DEST_MAC_FAILED`, which is the honest answer.
- **A refusal is a state, not an error.** `ok = 1` requires the block VALID
  *and* the source index inside the claimed count; outside it, the address
  belongs to nobody and granting it is a wire defect that shows up as someone
  else's audio dropping out.
- **RELEASE frees nothing, and says so.** One block serves the whole engine
  for as long as it is enabled and Annex B has no partial-release message, so
  the release is a no-op acknowledgement the processor's tracker needs to
  clear its busy flag.

**What depends on it:** `acmp_declaring_o` — the talker gate — is reachable
ONLY through an ALLOC_DA success. With the face unconnected, or with the
allocator pruned (`MAAP_P = 0`) or disabled (`MAAP_CTRL.en = 0`), every ALLOC
is answered `ok = 0` in one cycle, no source ever declares, and the talker
half is dead by construction. That is the same code path in all three cases,
deliberately: a build without an allocator must not take an untested branch.

## Open decisions

Both settled.

- **ADP/talker gating: should PROBE_TX/streaming wait for `maap_valid`?**
  **SETTLED — yes, and structurally.** It is no longer an AND term composed in
  `milan_datapath`: the processor's talker cannot declare without an ALLOC_DA
  success, so "a valid Destination MAC Address exists" is a precondition of
  the declaration itself. One decision, one place.
- **range/count:** count = 8 like the reference, indices 0..count−1 handed to
  sources 0..N−1 by the shim.

---

## Appendix: GET_DYNAMIC_INFO 0x4B contract

The processor implements `GET_DYNAMIC_INFO` in
[`KL_aecp_engine.sv`](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/a25b5cc9794b8e7f70f738548f4d674e9669b469/hdl/aecp/KL_aecp_engine.sv).
Each record is `{data_length[2], reserved[2], status[1], reserved[1],
command_type[2], command_data[L]}`. The response `control_data_length` is 12
plus the sum of retained record sizes.

IEEE 1722.1-2021 section 7.4.76 permits exactly thirteen fixed-size getters.
The engine pre-scans the complete request before processing any record. A
forbidden command type, truncated header, record overrun, or oversized command
returns outer `BAD_ARGUMENTS` and no getter runs. A legal unimplemented getter
returns record-level
`NOT_SUPPORTED` and copies its command data. Implemented getters run
independently, so one record can report `NO_SUCH_DESCRIPTOR` while adjacent
records succeed.

The command-side `info_status` is the complete one-byte field and must be
`SUCCESS`. Any nonzero bit returns `BAD_ARGUMENTS` for that record without
suppressing parseable neighbours. The field is not a record delimiter, and
IEEE 1722.1-2021 section 7.4.76.1 requires independent record handling.

The command-side `control_data_length` limit remains 524. A command above that
limit returns `BAD_ARGUMENTS` before record processing. The aggregate response
length starts empty and advances only when a response record is retained, so a
skipped record cannot expose unwritten response-buffer bytes.

A record whose response would push `control_data_length` past 524 is omitted
without error, and processing continues with later records. The processor has
no `IN_PROGRESS` response path. Milan `GET_STREAM_INFO` contributes its
56-byte Milan message-specific body, not the 84-byte base IEEE body. The
engine also checks each getter's actual response cursor against the selected
fixed response length before appending the record. A mismatch voids the
aggregate with `ENTITY_MISBEHAVING` instead of shifting later records or
exposing stale response memory. Four-byte descriptor copies write no second
word beyond their declared response.

The packet-level W8 tests in
[`sim_main.cpp`](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/a25b5cc9794b8e7f70f738548f4d674e9669b469/tb/pp_top/sim_main.cpp) grade these
rules byte for byte.
