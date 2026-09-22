<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# 11 — MAAP Engine (dynamic multicast address acquisition)

## 1. Role and scope

The in-scope implementation of the MAC Address Acquisition Protocol, **IEEE Std
1722-2016 Annex B (normative)**, as one processor-class engine (`hdl/maap/
KL_pp_maap.sv`). It claims **one contiguous block** of `cfg_maap_count_i` multicast
destination addresses out of the Annex B dynamic allocation pool for the whole
entity — source `s` uses `base + s`, the convention the integrating fabric already
applies on both its planes — probes it, announces it, defends it, and yields with a
fresh random range when a peer wins, exactly per the Table B.7 state machine.

Selection is the quasi-static top input `cfg_maap_internal_i`
([02 §4.2](02_interfaces.md)):

- `0` (default): the landed behaviour, **byte-identical** — the processor implements
  no MAAP, the talker's `ALLOC_DA`/`RELEASE_DA` walk out of the top's `maap_*` port
  group, and the integrating fabric answers (its `KL_maap` behind `KL_pp_maap_shim`).
  The engine still drains its dispatch queue (a parked queue would head-block the
  shared normalizer) but transmits nothing and answers nothing.
- `1`: this engine answers the talker internally under the **same seam contract**
  the shim documents, the port group is quiesced, and the claim is published on the
  top's `maap_addr_o` group (KL_maap's `addr_o`/`addr_valid_o` naming, so the fabric
  substitution is mechanical: gate talker egress on `maap_addr_valid_o`, read source
  `s`'s DA as `maap_addr_o + s`, retire the fabric allocator).

The compliance review's owner decision 2026-08-11 ("MAAP stays external") remains
the shipping default; this engine is the opt-in internal alternative, mirroring the
`P-EN-SRP-ENGINE` pattern for SRP.

## 2. External contract

| Face | Direction | Contract |
|---|---|---|
| dispatch-in | pop | `pp_txn_t` records with `protocol = PP_PROTO_MAAP` from the fourth `KL_pp_dispatch` queue (depth 2 + head — Annex B traffic is a handful of frames per walk) |
| RX slot pool | free only | records are **self-contained** (§3), so the engine never reads payload; it frees the record's slot at classify |
| PRNG | draw | kinds 5 (probe interval), 6 (announce interval), 7 (pool offset) — [08 §2](08_timing.md) |
| timer service | arm/expiry | two F08.4 slots: `base + 0` probe_timer, `base + 1` announce_timer; owner tags `PP_OWN_MAAP_C + {0, 1}`; expiries filtered by slot **and** protocol state (a stale expiry in the wrong state is Table B.7's `-x-`) |
| TX slots + arbiter | alloc/write/commit + lane 6 | whole 60-byte wire frames (42 real bytes zero-padded to the Ethernet minimum); `txreq` held until granted; background priority class with the T-TX-AGING guard — Annex B attaches no deadline to any PDU |
| allocator seam | serve | the exact 10-pin face of [02 §4.2](02_interfaces.md), muxed against the top ports by `cfg_maap_internal_i` |
| claim publication | level | `addr_o` (base), `addr_valid_o` (1 = DEFEND state), `state_o` (0 INITIAL / 1 PROBE / 2 DEFEND), `conflicts_o` (re-address events), `defends_o` (DEFENDs sent) — saturating 8-bit counters, KL_maap-compatible |

**The seam contract, inherited verbatim** from `KL_pp_maap_shim`'s five recorded
decisions: (1) accept whenever no response is in flight and answer from claim state
sampled at the accepting cycle — refuse fast, never ready-stuck-low, so a
still-probing walk (a legal ~1.7 s state) costs the talker's single walker two
cycles, not `P-MAAP-ACCEPT-CYC`; (2) `ok` only in DEFEND with `s < cfg_maap_count_i`,
and the grant adds on the 16-bit offset half only so a granted DA structurally
cannot leave the pool; (3) `RELEASE_DA` is a no-op acknowledgement (one block per
entity; Annex B has no partial release); (4) any block-identity change away from a
granting state — a yield, a link loss, a count change — raises one sticky conflict
per source, lowest pending first, a fresh move superseding an in-flight sweep;
(5) not-engaged and still-probing share the refuse path.

## 3. PDU handling

**Wire format** (Figure B.1; all octet offsets from the destination MAC):

| Bytes | Field | TX value | RX use |
|---|---|---|---|
| 0..5 | DA | PROBE/ANNOUNCE: `91:E0:F0:00:FF:00` (Table B.10); DEFEND: the probe's SA (B.2.1) | validator DA gate: MAAP DA or own unicast |
| 6..11 | SA | `own_mac_i` | compare_MAC operand; DEFEND destination |
| 12..13 | EtherType | `0x22F0` | gate |
| 14 | subtype | `0xFE` | demux to `PP_PROTO_MAAP` |
| 15 | sv/version/message_type | `0x0` + 1/2/3 (Table B.1) | V8 nibble check; reserved types ignored (B.2.2) |
| 16..17 | maap_version + cdl | `0x08 0x10` — version 1, **cdl 16** (B.2.1) | maap_version **not** checked (B.2.3.2/B.2.3.4); cdl by V1 |
| 18..25 | stream_id | 0 (B.2.4) | ignored |
| 26..33 | requested_start + count | our base + count; DEFEND: **echo** of the probe's | rides the record's `controller_eid` lane |
| 34..41 | conflict_start + count | 0; DEFEND: the B.3.6.6 overlap — first **allocated** address in conflict + count from it | rides the record's `operands` lane |
| 42..59 | padding | 0 | beyond cdl: ignored |

The validator ([03 §3](03_packet_engine.md)) captures both ranges into the record, so
MAAP RX needs **no payload reads** and no sixth RX-pool replica. The subtype gate is
DA-qualified: `0xFE` is accepted only to the MAAP multicast DA or our unicast (a
DEFEND answers the probe's SA), and the 1722.1 subtypes are no longer accepted on the
MAAP DA. The fabric peer's reference-contract frames (cdl 28) parse identically —
same offsets, longer stored tail.

**Which range a received PDU "contains"** (B.3.5.5-7, footnote b): a PROBE is judged
on `requested_*` (its conflict fields are 0 by B.2.7/B.2.8); a DEFEND or ANNOUNCE on
`requested_*` **or** `conflict_*` — the inclusive reading, matching the reference
peers which fill the conflict fields. A zero count is an empty range and never
conflicts. Overlap is computed on full 49-bit inclusive ends, so ranges crossing out
of the pool prefix compare correctly.

## 4. Internal blocks

One event-serialized walker (RX record > pending timer expiry > owed walk start),
the byte-exact frame builder into the shared TX pool, a single-draw PRNG serializer,
and the embedded seam logic (combinational grant + registered response + the
block-move conflict fan-out) which never contends with the walker.

## 5. State

`pstate` ∈ {INITIAL, PROBE, DEFEND} (Table B.6; encoded 0/1/2 = KL_maap's
`state_o`), the claimed `offset` (16-bit pool offset), `maap_probe_count` (Table
B.4), the footnote-a seed-used and conflict-noseed marks, and the two saturating
observability counters.

## 6. Behavior (Table B.7, executed literally)

- **Begin!/PortOperational!** = the rise of `cfg_maap_internal_i AND link_up_i AND
  cfg_maap_count_i != 0`: `generate_address` — the provisioned
  `cfg_maap_seed_offset_i` on the first attempt if `cfg_maap_seed_valid_i`
  (footnote a, clamped into the pool), else a kind-7 draw rejection-retried past
  `0xFE00 − count` so the fit clamp keeps the B.3.6.1 uniform distribution — then
  **ReserveAddress!**: `maap_probe_count := 3` (`MAAP_PROBE_RETRANSMITS`, Table
  B.8), start probe_timer with a fresh kind-5 draw, send a PROBE, enter PROBE.
- **probetimer!** (PROBE only): start probe_timer with a **fresh** draw, send a
  PROBE, decrement. The decrement reaching zero is **probeCount!** (B.3.5.8): stop
  probe_timer (implemented as skipping that final re-arm), start announce_timer
  (kind-6 draw), send the first ANNOUNCE **immediately**, enter DEFEND. Four PROBEs
  total leave the wire — the initial transmit plus three retransmits — and the claim
  is valid after exactly three probe intervals, the bound `KL_acmp_talker`'s
  `P-MAAP-RSP-MS` is derived from.
- **announcetimer!** (DEFEND only): fresh kind-6 draw, re-arm, send an ANNOUNCE.
- **Conflicts** (only PDUs whose contained range overlaps ours fire at all):

  | Event | PROBE state | DEFEND state |
  |---|---|---|
  | rProbe! | compare_MAC, else yield | **sDefend** (no tie-break) |
  | rDefend! | yield (no tie-break) | compare_MAC, else yield |
  | rAnnounce! | yield (no tie-break) | compare_MAC, else yield |

  compare_MAC (B.3.6.4): octet-wise **reversed** unsigned compare of our MAC
  against the PDU's SA; TRUE (we are lower) = no further processing. A yield stops
  the running timer, counts one re-address, and re-enters through
  INITIAL/**Restart!** with a fresh random range — the seed is deliberately not
  reused (the range is known-bad) — while the falling `addr_valid` fans out the
  per-source conflicts.
- **sDefend** (B.3.6.6): unicast to the probe's SA; `requested_*` echoed;
  `conflict_start` = max(requested_lo, ours_lo), `conflict_count` = overlapping
  addresses from there.
- **Release!** = engage fall (config drop or link down): stop both timers, INITIAL,
  **no PDU** (B.3.5.2 + footnote c — a local event), seed re-armed for the next
  engage. A later link rise is PortOperational! and restarts the walk.

## 7. µcode / dispatch

None — a hardwired FSM, ADP-class per [01 §3](01_overview.md) principle 1.

## 8. Timing

`T-MAAP-PROBE` (strictly 500 < T < 600 ms) and `T-MAAP-ANNOUNCE` (strictly
30 < T < 32 s) per [F08.1](08_timing.md#fig-08-constants), drawn fresh at every
timer start via PRNG kinds 5/6; the F08.4 MAAP pair of deadline slots. The B.3.6.1
PRNG requirements (sequence ≥ 2^32 − 1, MAC-and-clock seeding) are met by the shared
`KL_pp_prng` (2^64 − 1, entity_id XOR free-running counter at first link-up).

## 9. Deviations and notes

- Strict Annex B against the fabric `KL_maap`'s pipewire-reference contract:
  cdl **16** not 28; **4** probes not 3 with the first ANNOUNCE at probeCount!;
  announce cadence 30..32 s not 3 s; exclusive interval bounds; compare_MAC
  tie-breaks; PROBEs judged on `requested_*`. The reference peer's RX parser checks
  only EtherType + subtype, so the strict frames interoperate.
- MAAP PDUs are transmitted untagged (the fabric convention; the validator's RX
  path is untagged-only for every control subtype).
- One SM instance (one range) per entity by design — B.3.2 allows one per range;
  the per-source face is served by block arithmetic, not per-source claims.

## 10. Parameterization

`N_SRC_P` (= P-N-STREAM-OUT, conflict fan-out width), `RX_SLOTS_P`,
`TMR_SLOTS_P`/`TMR_SLOT_BASE_P`/`TMR_OWNER_BASE_P` (F08.4 MAAP pair),
`TX_STD_SLOTS_P`/`TX_OVERSIZE_BYTES_P`. Runtime quasi-static (02 §2 rule 4):
`cfg_maap_internal_i`, `cfg_maap_count_i`, `cfg_maap_seed_offset_i` +
`cfg_maap_seed_valid_i`.

## 11. Cross-references

Consumes [02 §4.2](02_interfaces.md)'s seam (as its internal server), the timer
service and PRNG of [08](08_timing.md), the TX pool and arbiter of
[03 §7-§8](03_packet_engine.md). Verified by `tb/maap` (the Annex B unit walk) and
the `tb/pp_top` MP section (end-to-end through the real validator, dispatch, talker
and MAC lanes); the F08.4 slots by `tb/timer_map`; the PRNG kinds by `tb/prng`; the
RX classification by `tb/rx_validator`; the fourth queue by `tb/dispatch`
([09](09_verification.md)).
