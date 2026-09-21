<!-- Draft by A151, revised by A152. Filed as kebag-logic/milan-fpga #501. Under #70. A decision, then a small implementation. -->

# Saved state: an output channel-map set can outgrow its record at the 8x8 shape

## Observed

The decided allocation (`docs/design/SAVED_STATE_FASTCONNECT.md` section 4.2)
gives a channel-map record 8 bytes a cluster. An OUTPUT mapping is keyed by
stream channel (`hdl/milan/milan_datapath.sv`, `amap_edit_validate`: key =
stream_index * 8 + stream_channel, owned by one port), so one cluster may
feed several stream channels. At 8x8 a STREAM_PORT_OUTPUT has 9 entries
against 72 stream channels, so a legal fan-out set cannot be saved. At 1x1 it
cannot happen: 16 stream channels against 17 entries.

EXECUTED on the D3 evidence branch `500-design-evidence` (case K16 at 8x8,
the commit the page names): "10 mappings on a 9-entry record"; the D3 design
keeps such a set pending and unwritten, and the status never reads durable
over it.

## Decision needed

A conforming allocation, or an accepted-mapping limit with its protocol
consequence. Grow the output map record to the stream-channel key space (a
record-space change: `scripts/check_nvm_record_space.py`, the backend's map
length tables, the processor's writer), or bound the set at command time (a
behaviour a controller would see, and its refusal status). Milan v1.2
5.3.10.1 requires every mapping of each STREAM_PORT_OUTPUT to persist.
Permanent pending is failure containment, not persistence: it is not an
accepted resolution of this issue.

## Consequence for the D3 contract

Stage 3 of the D3 contract (its ticket T3) is BLOCKED until this issue
records its decision. Stages 1 and 2 do not depend on it.

## Acceptance

The decision recorded on the saved-state page; if the record grows, the
record-space gate and its controls updated. Validated with the actual
journal decode and a cleared-first restore, not a pending flag: the maximum
legal accepted set, the boundary and the one-over-capacity cases, and any
command refusal the decision requires. A note for whoever grows the record:
the D3 model's reset sets are not empty, and restoring port after port in
ascending order refuses a saved set that takes a stream channel a LATER
port's reset set still owns. The shipped reset sets are empty and cannot
conflict; a non-empty reset set would need every port's reset set removed
before any saved set is added.
