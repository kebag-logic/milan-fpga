# Input-mapped block-RAM loopback proposal

Status: STOP before implementation; routing capacity needs owner selection.

Issue: [#979](https://github.com/kebag-logic/milan-fpga/issues/979).

Author: [A826]. Date: 2026-11-23.

Examined base: `3cda030c174b325e36c26af6420487ff91346d15`.

This document proposes behavior; it grants no implementation approval.

## Decision required

The request specifies a Loopback input cluster, not its cardinality.

The old 8x8 lane exposes 64 received channels.

Those facts allow materially different advertised routing capabilities.

Milan requires every cluster to be mono.

One 64-channel cluster cannot avoid the input-key limit.

The approved physical destination remains independently useful.

At 8x8, it consumes one input-map key.

Eight independent Loopback destinations per listener consume another 64.

The resulting 65 keys exceed the current 64-key limit.

`avdecc/aem_assemble.py:441` explicitly refuses that geometry.

This is an implementation limit, not a Milan limit.

It is also distinct from the owner's immutable resource ceilings.

Choose the enabled configuration's capacity and physical-map independence:

| Option | 8x8 input geometry | Forwarding capacity | Consequence |
|---|---|---|---|
| A: minimal pool | Port 0: physical plus one Loopback; ports 1-7: one Loopback each | Eight independently mapped mono channels | Nine keys; no physical coupling. Its area cannot establish savings for a 64-channel replacement. |
| B: bounded separate pool | Port 0: physical plus seven Loopback; ports 1-7: eight Loopback each | 63 independently mapped mono channels | 64 keys; preserves physical independence, with asymmetric forwarding capacity. |
| C: shared first destination | Same geometry as B; also copy the physical destination into buffer channel 0 | 64 forwarded mono channels | 64 keys; physical slot 0 and forwarding channel 0 share one input mapping. |
| D: full separate pool | Port 0: physical plus eight Loopback; ports 1-7: eight Loopback each | 64 independently mapped mono channels | 65 keys; requires a separately authorized map-capacity extension and interface audit. |

Recommendation: C if sharing the first mapping is acceptable.

It preserves forwarding width without raising the input-key limit.

Otherwise choose B, or authorize D's capacity work explicitly.

Option A is suitable only for a deliberately smaller feature.

None changes a resource, timing, memory, or service bound.

No option has been selected or implemented.

At 1x1, eight physical plus eight Loopback clusters fit.

That geometry requires 16 keys.

Option C would share consistently at 1x1 too.

Retain eight physical clusters and add seven Loopback clusters.

Only the first physical cluster also feeds the buffer.

That gives eight forwarding channels and 15 input keys.

Every cluster still has `channel_count=1`.

The geometry probe exercised the existing table constructor directly.

Nine, 16, and 64 keys were accepted; 65 was refused.

It proved this boundary only, not full descriptor generation.

## Authority and existing behavior

Milan `v1.2 5.3.3.8` requires mono Audio Clusters.

Sections `5.4.2.26-28` govern enumeration and atomic mapping commands.

IEEE 1722.1-2021 7.2.19 defines port-relative mapping offsets.

An input mapping can select any permitted Stream Input channel.

Its source is not implicitly the input port's stream number.

Multiple destinations may select the same received channel.

Output mappings may similarly fan out a source cluster.

The #584 owner disposition remains the disabled configuration's contract.

Port 0 retains its physical destination on TDM32 slot 0.

Ports 1-7 retain their documented Unrouted clusters.

The 1x1 legacy loop option remains enabled as currently configured.

The 8x8 legacy loop option remains disabled.

`amap_in_store_r` is the protocol-visible input map.

The physical render map is only its projection.

The new buffer must consume the protocol mapping directly.

Reading only physical-map write pulses would miss nonphysical clusters.

Every mapping writer must feed that logical view.

Include accepted edits, boot defaults, restore, rollback, and format clipping.

The existing loop lane remains behind `LOOPBACK_P` unchanged.

It uses bucket 5 and receives the depacketizer clone.

Its current source contains elastic queues plus flop holds.

Its empty-queue behavior repeats samples; this proposal must not.

The supplied +2303 LUT / +1542 FF comparison is historical.

The current queued lane has not been remeasured.

## Memory-port finding

`KL_render_queue.sv:382-405` declares two sample/valid banks.

Each bank has a write port and synchronous read port.

`write_ports`, lines 612-637, shares writes with row invalidation.

The read scheduler, lines 639-665, serves presentation frames.

Neither bank has an unused physical port.

Use a separate inferred input buffer, targeting one RAMB18.

Copy mapped samples through an optional scheduled read interval.

Reuse their read ports after the existing interface read.

Complete the additional reads before invalidating the consumed frame.

The occupied ports would serve an additional scheduled reader.

The disabled branch retains the existing scheduler unchanged.

This route avoids another raw 64-channel sample-hold bank.

Dense two-sample beats need no additional serialization.

The optional reader requests one mapped channel at a time.

It selects the bank and writes one mono buffer word.

Physical rendering keeps its existing read order and deadlines.

## Proposed datapath

The capacity choice determines destination indices, not the pipeline:

```text
accepted timestamped received samples
  -> existing render queue and its presentation-frame classification
  -> optional mapped-channel read schedule
  -> separate frame-indexed input buffer
  -> synchronous source bucket 6
  -> output mapping and existing talker packetization
```

Bucket 5 keeps its current meaning.

Bucket 6 identifies a buffered input destination.

Each output port advertises its selected backed source set.

Its descriptor offsets resolve to those destination indices.

Names identify destinations; a remap must not invalidate their names.

Distinct names must identify the new source pool.

The buffer has four pages of up to 64 words.

A word contains a 24-bit sample and validity/tag information.

A 32-bit, 256-word organization uses 8192 storage bits.

Simple-dual-port operation targets one RAMB18.

It supports one write and one synchronous read.

Physical inference and control cost remain unmeasured.

Page validity makes old words unreachable without resetting the array.

Frame tags must be checked beyond the modulo page address.

Finite tags require invalidation before reuse, including after stopped clocks.

The capture crossbar reads two mono samples sequentially per pair.

Only the returned pair needs holding registers.

It must not reconstruct the old 32-pair flop bank.

The added request/return cycles enter the capture-walk timing calculation.

Absent or invalid samples become silence; every slot emits.

## Latency and rate contract

Proposed additional audio delay: exactly one local media frame.

At 48 kHz this is 20.833333 microseconds.

Define received presentation frame F using the existing render queue.

Copy F into the buffer before its eligibility deadline.

Capture frame F+1 may consume only that tagged frame.

Never consume an earlier frame to conceal a missing one.

The existing queue's half-period snapping remains upstream behavior.

The talker uses its normal capture timestamp and presentation offset.

It must not reuse the received packet's timestamp unchanged.

Its existing packetization and transport lead remain additional terms.

Recalculate those terms with the new synchronous source-read schedule.

The one-frame proposal is a target contract, not measured latency.

Both shapes must pass deadline assertions before claiming completion.

A missed deadline produces silence.

No sample-rate converter is proposed or advertised.

Different nominal rates follow current mapping/format rejection rules.

Milan `v1.2 5.4.2.27` recommends mismatch rejection.

Small clock-rate differences can occur within one nominal rate.

Existing timestamp placement produces missing or overlapping frames.

A missing frame yields zero without repeating preceding samples.

The existing placement policy settles overlaps and counts slips.

Reset, unbind, and stopped/restarted media clocks invalidate availability.

A missed publication deadline drops the frame permanently.

Consumers can fan out eligible frames within their capture periods.

Period expiry invalidates frames regardless of retained RAM contents.

## Mapping changes

Use committed logical-map state, never speculative edit rows.

Freeze a map snapshot for a buffer-frame fill.

Any input-map change during the fill invalidates that publication.

Accepted changes invalidate the affected destination's retained samples.

A conservative first implementation may invalidate the entire loop buffer.

Successful commands prevent later capture snapshots from selecting old-map data.

Already captured samples inside an outgoing packet remain in flight.

The packet already being assembled is not retroactively rewritten.

Publish a complete frame under the new map.

It becomes eligible at its specified F+1 capture boundary.

Until then the affected output channels contain silence.

REMOVE, format clipping, rollback, and unbind share this invalidation rule.

No-op and rejected commands never publish speculative maps.

Command atomicity, locks, and notifications retain their existing owner.

Map-generation wrap must not resurrect a retained buffer page.

## Build and descriptor contract

Proposed option: `INPUT_LOOPBACK_P`, default zero.

Proposed config fact: `fabric.input_loopback_lane`, default false.

The builder derives the instance flag and descriptor pools together.

The old `fabric.loopback_lane` remains independent and unchanged.

Both may exist; their source buckets and destination identities differ.

The measurement configuration disables the old lane explicitly.

With the option off, generated artifacts remain byte-identical.

Declarations, descriptors, source entries, and identities remain unchanged.

Compare both existing artifact sets: `1x1/1if` and `8x8/1if`.

Enabling it generates mono Loopback destinations and backed output sources.

Their input mappings remain dynamic with fixed GET page partitions.

Derive every affected artifact from the selected topology.

Include descriptor identities, names, saved maps, and firmware geometry.

Record capacity overflow as debt; never widen owner ledgers.

## Validation and measurement after the decision

Exercise received audio through the real acceptance and talker paths.

Select a source stream different from the input port index.

Verify transmitted payload values, channel identity, and event sequence.

Cover ADD, REMOVE, replacement, fan-out, unmapped silence, and underrun.

Cover reset, bind loss, format clipping, and buffer-fill edits.

Observe the first nonzero sample after every invalidation.

Check page/tag wrap and prolonged absence for stale replay.

Plant ignored input mappings, wrong sources, and retained-page replay.

Also plant REMOVE-as-no-op, wrong projection, and bucket wiring faults.

Each plant must fail its named assertion.

The clean build must pass.

Run the affected render suite and the complete builder union.

Run documentation gates and the relevant mapping/restore regressions.

Measure the leaf and integrated 8x8/1if enabled build.

Report LUT, FF, RAMB18/RAMB36, occupied slices, and worst-corner slack.

Select the best of the three prescribed placement directives.

Require setup slack of at least `+0.030 ns`.

Hold slack must be nonnegative.

Preserve every existing resource and firmware-memory ceiling.

Report historical comparison separately from fresh same-head measurements.

The Issue additionally requests routing evidence for both shapes.

No routing, area, binary-equivalence, or simulation pass is claimed here.

## Stop disposition

The decision changes advertised channel capacity or physical routing coupling.

It cannot be settled by choosing an RTL implementation detail.

The request explicitly requires stopping for an owner-only decision.

Implementation and measurements therefore remain unstarted.

The Issue remains Backlog pending the recorded topology decision.

Independent implementation review remains unassigned and unclaimed.

STOP: owner must select loopback channel count and physical-map independence
