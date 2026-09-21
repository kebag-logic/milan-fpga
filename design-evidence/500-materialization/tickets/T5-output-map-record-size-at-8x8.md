<!-- Draft by A151 for the manager to file. Repository: kebag-logic/milan-fpga. Under #70. A decision, then a small implementation. -->

# Saved state: an output channel-map set can outgrow its record at the 8x8 shape

## Observed

The decided allocation (`docs/design/SAVED_STATE_FASTCONNECT.md` section 4.2)
gives a channel-map record 8 bytes a cluster. An OUTPUT mapping is keyed by
stream channel (`hdl/milan/milan_datapath.sv`, `amap_edit_validate`: key =
stream_index * 8 + stream_channel, owned by one port), so one cluster may
feed several stream channels. At 8x8 a STREAM_PORT_OUTPUT has 9 entries
against 72 stream channels, so a legal fan-out set cannot be saved. At 1x1 it
cannot happen: 16 stream channels against 17 entries.

EXECUTED (evidence branch `500-design-evidence`, commit
`a21b165ac1c671d10cba7255beaf75cea0f81d18`, case K16 at 8x8): "10 mappings
on a 9-entry record"; the D3 design keeps such a set pending and unwritten.

## Decision needed

Grow the output map record to the stream-channel key space (a record-space
change: `scripts/check_nvm_record_space.py`, the backend's map length tables,
the processor's writer), or bound the set at command time (a behaviour a
controller would see), or accept that an 8x8 fan-out set stays pending. Milan
v1.2 5.3.10.1 requires every mapping of each STREAM_PORT_OUTPUT to persist.

## Acceptance

The decision recorded on the saved-state page; if the record grows, the
record-space gate and its controls updated, and the 8x8 case of the D3
co-simulation saving a fan-out set.
