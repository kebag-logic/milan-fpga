<!-- Draft by A151 for the manager to file. Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan. After T2. -->

# Saved state, stage 3: the record writer materializes the channel maps

## Objective

Extend `KL_aecp_nvm_writer` to the channel-map records `0x60` to `0x7F` (2 at
the parent's 1x1 shape, 16 at 8x8), Milan v1.2 5.3.9.1 and 5.3.10.1. The maps
live in the integrator's fabric; the processor reaches them only through the
GET_AUDIO_MAP read face and the ADD/REMOVE edit face.

## Authority

kebag-logic/milan-fpga `docs/design/SAVED_STATE_MATERIALIZATION.md` sections
3 (rules 3 and 8), 7.2 (K12, K16), 8.3, 8.4; the parent's saved-state page
section 4.2 (8 bytes a cluster).

## In scope

- The trigger: the edit face's commit-one-record beat (`amap_edit_req_o` with
  `amap_edit_phase_o` 5), port from `amap_edit_desc_type_o` and
  `_desc_index_o`; never the class-6 mark.
- The latch of the port's live set over the GET_AUDIO_MAP face under the
  hold-off, packed at the head of the record and padded with unused entries.
- A set with more mappings than the record has entries is never written in
  part and never forgotten: it stays dirty and is skipped until its port
  changes again.
- The coupled restore: formats judged on "supported" first; each port's saved
  set replaces its reset set as one staged ADD; a refused set restores the
  reset set after reverting any format it would orphan; every restored format
  is judged again against the final maps.

## Acceptance

- One map change converges; deleting the map trigger alone reddens a case.
- An oversized set (reachable at 8x8) reads pending, is not written, raises
  no alarm, and converges once shrunk; a mutant that forgets it reddens.
- The coupled restore cases of the design (a consistent narrower pair, an
  orphaning format reverted, refused maps revert their formats) with their
  mutants red.

## Dependencies

T2. The parent deletes its sticky class-6/7 bit in the same pin bump
(milan-fpga T4). The 8x8 record size is milan-fpga T5.
