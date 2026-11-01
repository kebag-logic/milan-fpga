# MAAP in fabric — design + reference contract (task #18)

This page describes the all-fabric shipping placement.
[Mark II placement](../ARCHITECTURE_HW_SW_SPLIT.md#1-ownership-rule) is build-selectable per control function.
Its default is bare-metal ADP, ACMP, AECP, MAAP and SRP.
All-fabric remains supported and the shipping default until F2 to F5 acceptance.
That acceptance covers all streams, counters and the audio soak.


Goal: Milan-mandatory dynamic multicast-DMAC allocation for the talker
(before this, `cfg_aaf_dmac` was statically provisioned).
[`hdl/ieee1722/maap/KL_maap.sv`](../../hdl/ieee1722/maap/KL_maap.sv)
on the established monitor-tap + low-rate-TX recipe (house style, `//!`
documentation comments).

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

- **[Annex B contract](#annex-b-contract)** -- The wire bytes, the Table B.7 walk, the timer draws and the conflict cells as IEEE 1722-2016 Annex B defines them and `KL_maap` implements them since #686, clause by clause. Also the remaining deviations, and the reference-implementation contract it replaced.
- **[Fabric integration](#fabric-integration)** -- Where `KL_maap` attaches (RX monitor tap on subtype 0xFE; TX as the second leg of the ONE control-lane merge), the `MAAP_CTRL.en=0` soft-migration that keeps `cfg_aaf_dmac` behaviour bit-exact, and the CSR block reconciled to `REGISTER_MAP`; note there are no ADDR_LO/HI registers, the DMAC is the pool base plus the claimed offset in `0x6D0`.
- **[The block ⇄ per-source bridge (KL_pp_maap_shim)](#the-block--per-source-bridge-kl_pp_maap_shim)** -- How one block claim answers N per-source ALLOC_DA requests, why `s` gets `base + s`, why a refusal is a state and not an error, and why RELEASE frees nothing.
- **[Open decisions](#open-decisions)** -- Both are now SETTLED, and the load-bearing one settled itself structurally: AAF admission ANDs the DA because the declaration cannot exist without it.
- **[Appendix: GET_DYNAMIC_INFO 0x4B contract](#appendix-get_dynamic_info-0x4b-contract)** -- Unrelated to MAAP. Records the current IEEE 1722.1-2021 batch contract and points to the processor implementation.

## Annex B contract

IEEE 1722-2016 Annex B is the authority for `KL_maap` (#686). The engine is
one Table B.7 machine for one contiguous block of `count_i` addresses. Its
`state_o` names map onto Table B.6 as IDLE = INITIAL, PROBE = PROBE and
ANNOUNCE = DEFEND.

**Wire (B.2, B.4).**

- The pool is `91:E0:F0:00:00:00` plus a 16-bit offset, `0xFE00` addresses
  (Table B.9). A randomly generated block is clipped to fit inside it. A
  supplied seed must fit entirely inside the dynamic pool.
  Invalid seeds fall back to a bounded random draw (#696 M7).
  A block ending exactly at offset `0xFE00` is valid.
- EtherType `0x22F0`, subtype MAAP (`0xFE`), `sv` 0, `version` 0,
  `maap_version` 1 (B.2.3.1), `stream_id` 0 (B.2.4).
- `control_data_length` is 16 in every MAAP frame (B.2.1).
- PROBE and ANNOUNCE go to `91:E0:F0:00:FF:00` (Table B.10). A DEFEND goes
  to the source MAC of the PROBE that caused it (B.2.1). That MAC is latched
  when the DEFEND is requested, so a later frame cannot redirect it.
- PROBE and ANNOUNCE carry this station's range in requested_* and zero
  conflict_* (B.3.6.5, B.3.6.7). A DEFEND carries the overlap of the PROBE's
  range with this station's in conflict_* (B.2.7, B.2.8).
  Its requested_* fields echo the triggering PROBE (B.3.6.6).
  The echo preserves all sixteen requested_count bits.
- Every per-frame field a protocol event can change (message type,
  destination, requested range, conflict range) is latched at the send
  request. A Restart! or a received PDU taken while a frame waits on the wire
  therefore cannot rewrite that frame.
  The source MAC follows `station_mac_i` during transmission.
  Reconfiguration during a frame is not protected.
- Frames are 60 bytes, zero-padded.
  RX requires every byte through conflict_count, including keep strobes.
  Truncation has no state, timer or transmission effect (#696 M8).
  RX parsing accepts every
  `maap_version` (B.2.3.2 to B.2.3.4) and ignores reserved message types
  (B.2.2).

**Walk (Table B.7, Table B.8, B.3.4).**

- Begin! is `enable_i` rising; generate_address uses the provisioning seed
  once (note a) and otherwise a random offset. A conflict's Restart! always
  draws a random offset.
- ReserveAddress! sends the first PROBE at once. The probe timer then sends
  three retransmissions (`MAAP_PROBE_RETRANSMITS` = 3), four PROBEs in total.
- The decrement to zero is probeCount!: the first ANNOUNCE goes at once,
  back to back with the fourth PROBE. The engine enters ANNOUNCE (Table B.7
  DEFEND) and `addr_valid_o` rises. The announce timer then repeats the
  ANNOUNCE.
- B.3.4.2 bounds the probe interval strictly between 500 and 600 ms. B.3.4.1
  bounds the announce interval strictly between 30 and 32 s. A timer load of
  N ms expires after more than N-1 ms and at most N ms plus one cycle, and a
  send can also wait for a frame already on the wire. So the engine draws N
  from a centred sub-range: 518 + 0..63 ms for the probe timer (17 ms of
  margin at each end) and 30488 + 0..1023 ms for the announce timer (487 ms).
  Both draws come from a free-running 32-bit LFSR with period 2^32 - 1.
  The probe draw is the 6-bit parity fold `PROBE_FOLD_C` of the generator's next state.
  The announce draw is the generator's low 10 bits.
  First enable samples the low 32 bits of the sum of the programmed MAC
  and the local real-time clock (#696 M4/M3, B.3.6.1) and loads that seed into the generator.
  Reset initializes a constant and clears the seed-sampled flag.
  Later Release!/Begin! events preserve the running sequence.
  A zero sum takes a nonzero constant to avoid the all-zero fixed point.
- The first Begin! after reset draws from the generator one step past the seed, as the firmware core does (#696 M4).
  Its offset word folds all 32 bits of that stepped seed: bit i is the parity of the stepped seed under row i of `OFFSET_FOLD_C`.
  The pool mapping then subtracts `0xFE00` from a word at or above it and clips the block to end inside the pool.
  The first PROBE goes on the next cycle, and its probe timer draws the probe fold of the same stepped seed.
  The 16 offset rows and the 6 probe rows are linearly independent, so the two first draws are independent too.
  Later Begin! events draw the running generator's next low 16 bits; Restart! draws its current low 16 bits.
- The fold rows serve equally timed stations, whose seeds differ only through the MAC or the clock (B.3.4 NOTE, B.3.6.1).
  The separation criterion is the one recorded on #696 in [comment 6102832618](https://github.com/kebag-logic/milan-fpga/issues/696#issuecomment-6102832618).
  Two seeds a power of two apart, with any carry, claim first blocks of up to 8 addresses that share no address (Table B.7 note b).
  This holds through the pool fold and the clip; a pair with a zero sum takes the fallback and is outside it.
  Adjacent MACs, MACs 2^i apart with i up to 31 and, at one MAC, clocks one power of two apart are such pairs.
  Such pairs also draw different first probe intervals.
  Seed bits 16..31 map one-to-one onto the offset word, so MACs differing only in bits 16..31 always draw different words; the pool fold can still map two such words onto one block, so their first blocks can coincide or overlap like any pair that is not a power of two apart.
  Two seeds not a power of two apart can still claim overlapping blocks, about 15 times in 65,024, as two independent draws would.
  No 16-bit draw can keep every pair of 2^32 seeds apart.
  The default MAAP target establishes these properties for every seed from the RTL itself, as the TB entry below describes.
- `enable_i` falling acts like Release!: back to IDLE at once.
- `port_operational_i` rising implements PortOperational! (B.3.5.9, Table B.7).
  An enabled active engine immediately revokes validity and re-probes.
  It draws a fresh range and sends four PROBEs.
  The event does not increment the conflict counter.
  A steady operational level causes no repeated restart.
  Table B.3 defines no event for leaving the operational state.
  A falling level therefore leaves the walk in progress running until the return.
  The datapath supplies its existing synchronous `eff_link_w` level.

**Conflict detection (B.3.2, Table B.7 note b).**

- Only a PDU whose range shares an address with this station's block is an
  event. The ranges are half-open, so an adjacent range is not a conflict,
  and a range of count 0 never conflicts.
- A PROBE or ANNOUNCE is judged on its requested_* range (B.2.5, B.2.6). Its
  conflict_* fields are zero (B.2.7, B.2.8), so they are never its range. A
  DEFEND is judged on its conflict_* range, the defender's addresses.
- The range's first four octets must be the pool's, `91:E0:F0:00`.

**Conflict cells (Table B.7).**

| Received, conflicting | in PROBE | in ANNOUNCE (Table B.7 DEFEND) |
|---|---|---|
| PROBE (rProbe!) | compare_MAC; Restart! when not lower | sDefend; retain one response while PROBE/ANNOUNCE drains |
| DEFEND (rDefend!) | Restart! | compare_MAC; Restart! when not lower |
| ANNOUNCE (rAnnounce!) | Restart! | compare_MAC (B.3.6.4); Restart! only when this station is not the lower |

compare_MAC compares the two MACs octet-reversed, with the last octet most
significant. When it is TRUE (this station is the lower), the PDU causes no
action (note d). One decision is taken per cycle, in priority order: disable,
Restart!, sDefend, then the timer's own send. A send deferred by any of them
happens on a later cycle.

**Remaining deviations.** These are recorded here; #696 rulings settled M6
capacity and M8 counting, and any further change needs its own decision.

- B.3.6.1 requires uniform address selection.
  Folding and clipping the 16-bit draw into the pool remains biased.
  M3 now supplies the 2^32 - 1 period and MAC-plus-clock seed.
  At the M3 step (lane head `39571196`, before the dev merge), the 1x1 recipe measures `g_maap.maap_engine` at 441 LUT / 340 FF.
  Against `6aa25dec` (439 LUT / 280 FF), growth is +2 LUT / +60 FF.
  At the merge result `0df48637`, before the first-draw folds, it measures 445 LUT / 340 FF.
  That is +6 LUT / +60 FF against `6aa25dec`.
  Dev `8b61b709` alone measures 443 LUT / 280 FF, so the lane's share is +2 LUT / +60 FF.
  The first-draw folds (#696 M4) add logic only: at lane head `bee1b0d7` it measures 490 LUT / 340 FF.
  That is +45 LUT / +0 FF against `0df48637` and +51 LUT / +60 FF against `6aa25dec`.
  This fits the +60 / +60 ceiling and uses its full FF allowance.
  In the [routed image](../findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-10-10-issue-696-first-draw) the engine uses 468 LUT / 339 FF.
  The pool mapping remains a separate deviation; full B.3.6.1 conformance is not claimed.
- One shared response buffer covers a PROBE during PROBE/ANNOUNCE transmission (#696 M6).
  Its destination, requested range and overlap remain until transmission completes.
  Pending and transmitting DEFENDs occupy that same buffer.
  The current frame remains byte-identical under backpressure.
  Disable, conflict restart and link return discard stale pending responses.
  Further PROBEs while that buffer is occupied remain unsupported.
  This includes PROBEs arriving during another DEFEND.
  The shared storage follows the area ruling on #696.
  At the M6 step, the 1x1 recipe measures `g_maap.maap_engine` at 457 LUT / 324 FF.
  The `6aa25dec` base is 439 LUT / 280 FF: cumulative growth is +18 LUT / +44 FF.
  This fits the ruling's +60 LUT / +60 FF ceiling; the shared buffer is retained.
  Table B.7 and B.3.6.6 define the response action.
  B.3.6.3 defines probe-count decrement, not response storage.
  Table B.7 requires responses; this capacity limit is not full conformance.
- RX parsing is untagged only; a tagged MAAP PDU is ignored.
- Truncated-PDU discard accounting remains absent (B.2, #696 M8).
  A later register-map change must provide an observable count.
  The manager ruling on #696 withdraws counting from this lane.

**History.** Before #686 the engine followed the byte layout of a
reference AVB implementation instead. It set `control_data_length` 28, sent
the DEFEND to the multicast address, sent three PROBEs with the first one a
probe interval late, drew probe intervals of 500 to 627 ms and announce
intervals of 3 to 5.047 s, judged an ANNOUNCE on its conflict_* fields, and
compared ranges with inclusive ends.

## Fabric integration

- RX: observe `rx_axis_fabric` (subtype 0xFE @ ether 0x22F0), aligned-lane
  parse (fields land in beats 0 to 5).
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
- Randomness: first enable samples `cfg_mac_addr` after firmware programming
  and adds `ptp_now_w[31:0]`, the existing local PHC's low nanosecond bits.
  The PHC and MAAP share the synchronous clock contract documented at the counter.
  Interval jitter uses the same free-running LFSR.
  The default MAAP target exercises the real CSR/datapath path.
  The two equally timed test stations use different programmed MACs and draw different intervals.
  Restoring reset-time sampling fails that check.
  Same-MAC stations enabled at different PHC times also draw different intervals.
  Ignoring the clock fails that integration check.
  The same stations' first PROBEs carry the first claims, graded as fixed pairs:
  the fixed adjacent MAC pair's blocks share no address, and the fixed pair of PHC times gives different first offsets.
  Restoring the pre-#696 first draw fails the first check; a first offset that ignores the clock fails the second.
  The unit suite observes the generator's linear transition map and checks its order.
  Short-period, nonlinear-trap, missing-clock, XOR-seed and repeated-seed defects
  fail the named M3 checks.
- Outputs: `maap_addr[47:0]`, `maap_valid` (ANNOUNCE state) → the datapath's
  `eff_aaf_dmac` mux into the AAF framer dmac when
  `MAAP_CTRL.en=1 && maap_valid`, **and** the block side of
  `KL_pp_maap_shim`, which is how the processor's talker learns a source's
  destination address. `cfg_aaf_dmac` stays the manual lever (en=0 keeps the
  pre-MAAP behavior bit-exact — soft-migration like CBS bypass).
- CSR ([`REGISTER_MAP.md`](../reference/REGISTER_MAP.md) is authoritative;
  the block below mirrors its `0x6CC`-`0x6D4` rows): `0x6CC MAAP_CTRL` (RW, reset `0`: `[0]` en,
  `[1]` seed_valid, `[15:8]` block count, `[31:16]` seed offset),
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
- TB: [`tb/verilator/maap`](../../tb/verilator/maap) grades the engine
  against Annex B, not against itself. It checks golden Figure B.1 frames,
  the four-PROBE walk at Begin! and Restart!, the DEFEND destination, every
  conflict cell above with its note b range edges, a conflicting PROBE
  parsed while an ANNOUNCE is part-way out on the wire, and strict B.3.4
  intervals over 150 walks and 24 announcements. A station MAC whose seed
  with clock 0 is zero (`02:00:00:00:00:00`) must also draw more than one
  distinct probe and announce interval. A link outage longer than a whole
  walk must leave that walk running, and only the return may restart it.
  A DEFEND answering a PROBE that starts below this station's offset must echo that PROBE's requested start, not the overlap start.
  Equally timed stations reset and enable on the same cycles and differ only in MAC or clock.
  For every carry run of the seed, one pair of seeds a power of two apart must claim first blocks that share no address.
  Adjacent MACs, MACs 2^i apart with 1 <= i <= 15 and MACs 2^i apart with 16 <= i <= 31 are separate checks.
  R558-6's four MAC pairs and two fixed clock pairs have their own checks, named as fixed pairs: they pin those pairs at the current fold rows and carry no guarantee of their own.
  Clocks one power of two apart must give different first offsets. The adjacent pairs, R558-6's pairs and the 16 single-bit pairs in bits 16..31 must give different first probe intervals.
  The harness's section [13] establishes the criterion for every seed, not a sample.
  It learns the first offset word and the first probe draw as linear maps of the seed from the RTL's own first Begin!, and confirms both maps on 256 further seeds.
  It then claims every word of the offset image through the RTL, for each block size from 1 to 8.
  Every one of the 528 carry runs, against every word and size, must claim disjoint blocks and draw a different first probe interval.
  Seed bits 16..31 must map one-to-one onto the offset word, and the two first draws must be independent.
  No fold row, generator tap or pool bound is restated in the suite, so a changed constant is graded as it stands.
  Its `mutants.py` plants at least one defect per #686 item and requires
  the named check to fail. The #696 plants include R558-6's p7 (the pre-#696 first draw), the raw low seed bits as the first offset,
  an offset fold without the seed's high half, a first offset that ignores the clock, and a raw-seed first probe draw.
  R559-6's q3 and q9 (one bit dropped from offset row 0 or row 6), its q1 (the probe fold of the unstepped state) and a nonlinear first fold pass every sampled pair, and each fails its section [13] check.
  A probe row that repeats an offset row fails the independence check.
  An echo of the overlap start fails the below-offset M2 check.
  The coverage gate is 95 %, like avtp_rxmon.

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
- **A conflict moves the source's Stream ID, not only its DA.** Since
  processor pin `f65c8ff7` (processor #202, #799) a conflict on a source
  whose Stream ID has been declared withdraws its Talker attribute,
  re-allocates at once and, at the grant, moves the source to a new Stream
  ID with the same upper 48 bits, declared without a wait: IEEE 802.1Q-2018
  35.2.2.8 asks for two LeaveAllTime periods only before the same StreamID
  returns with another FirstValue, and Milan v1.2 Table 5.3 lets the PAAD use
  another Stream ID. The processor publishes each source's current ID on
  `src_stream_id_o`; `milan_datapath` stamps it on the AAF and CRF frames and
  answers an output's GET_STREAM_INFO stream_id with it, so the wire and
  every answer name one ID. `milan_dp`'s `sidmove` and `sidmove8` legs drive
  a real conflict through this shim and grade that.

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
- **range/count:** firmware claims exactly the declared Stream Outputs.
  Count includes CRF only when its output is declared.
  The shim assigns indices 0..count-1 to those outputs.

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
