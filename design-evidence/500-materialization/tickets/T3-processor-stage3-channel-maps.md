<!-- Draft by A151, revised by A152, for the manager to file. Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan. BLOCKED: its implementation lane does not open until kebag-logic/milan-fpga #501 records a conforming output-map capacity decision. -->

# Saved state, stage 3: the record writer materializes the channel maps

## Status

BLOCKED on kebag-logic/milan-fpga #501. At 8x8 a legal accepted output set
can hold more mappings than the decided allocation gives its record (72
stream channels against 9 entries). Milan v1.2 5.3.10.1 requires every
accepted mapping to persist, and a set that stays pending for ever does not.
The design's pending-and-skip rule is FAILURE CONTAINMENT: it keeps the
status honest about a set no record can hold; it is not persistence and does
not satisfy this stage. This ticket does not choose the capacity.

## Objective

Extend `KL_aecp_nvm_writer` to the channel-map records `0x60` to `0x7F` (2 at
the parent's 1x1 shape, 16 at 8x8), Milan v1.2 5.3.9.1 and 5.3.10.1, inside
T1's restore transaction. The maps live in the integrator's fabric; the
processor reaches them only through the GET_AUDIO_MAP read face and the
ADD/REMOVE edit face.

## Authority

kebag-logic/milan-fpga `docs/design/SAVED_STATE_MATERIALIZATION.md` sections
3 (rules 3 and 8), 7.2 (K12, K16), 8.3, 8.4, 8.6, 8.8 and 10; the parent's
saved-state page section 4.2 (8 bytes a cluster), and whatever #501 decides
in its place.

## Prerequisites

- T2.
- #501's decision: a conforming allocation, or an accepted-mapping limit
  with its protocol consequence (a command a controller sees refused), and
  the record-space gate and backend tables that go with it.
- Before this stage is DECLARED SHIPPABLE: #502.

## Work that may proceed while this stage is blocked

Nothing here opens a stage-3 lane or claims map persistence. Separately:
#502's standalone correction (the live-write trigger feeding the parent's
pending bit for maps and names); and design-level evidence at 1x1, where
every legal output set fits its record (16 stream channels, 17 entries).

## In scope, once unblocked

- The trigger: the edit face's commit-one-record beat (`amap_edit_req_o` with
  `amap_edit_phase_o` 5), port from `amap_edit_desc_type_o` and
  `_desc_index_o`; never the class-6 mark.
- The latch of the port's live set over the GET_AUDIO_MAP face under the
  hold-off, packed at the head of the record and padded with unused entries,
  each EXACTLY eight 0xFF bytes.
- The restore framing rule: the saved set is the entries before the first
  unused one; any other entry is a mapping for the judge, whatever its
  stream index; an entry after an unused one refuses the record before the
  port's set is touched.
- The coupled restore: formats judged on "supported" first; each port's saved
  set replaces its reset set as one staged ADD; a refused set restores the
  reset set after reverting any format it would orphan; every restored format
  is judged again against the final maps.
- The roll-back owner: the parent's map plane returns every port to its
  reset set on T1's roll-back strobe (milan-fpga T4).
- Whatever #501 decides for a set its record cannot hold.

## Acceptance, once unblocked

- One map change converges; deleting the map trigger (each direction) alone
  reddens a save test, and deleting the map replay alone reddens a restore
  check.
- The framing cases, each against its refusal and application counts and
  the port's default set: stream index 0xFEFF, 0xFF00 and 0xFFFE, the exact
  unused entry, a malformed unused entry at the tail, a hole, an ordinary
  out-of-range index, and the valid empty set (applied, the port empty).
- The coupled restore cases of the design (a consistent narrower pair, an
  orphaning format reverted, refused maps revert their formats, the other
  records kept) with their mutants red; a pass-1 abort at the map records
  ends in DEFAULTS with formats and maps both at reset.
- #501's acceptance: the maximum legal accepted set and the boundary and
  one-over-capacity cases saved, decoded from the journal and restored
  cleared-first, with any refusal the decision requires.

## Dependencies

The prerequisites above. The parent deletes its sticky class-6/7 bit in the
same pin bump (milan-fpga T4).
