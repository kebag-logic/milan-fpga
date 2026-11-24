# Input-mapped block-RAM loopback

Status: implemented behind a default-off option; route and regression evidence belongs to [PR #987](https://github.com/kebag-logic/milan-fpga/pull/987).

Issue: [#979](https://github.com/kebag-logic/milan-fpga/issues/979).

Date: 2026-11-23.

Examined base: `3cda030c174b325e36c26af6420487ff91346d15`.

The manager authorized implementation behind a default-off build option.

## Selected topology

The manager selected option B on Issue #979.

The physical destination remains independent of every Loopback destination.

The existing table accepts nine clusters on port 0.

The reproduced 8x8 input counts are `[9,8,8,8,8,8,8,7]`.

Port 0 contains its physical cluster plus eight Loopback clusters.

Ports 1 through 6 each contain eight Loopback clusters.

Port 7 contains seven Loopback clusters.

That exposes 63 independent destinations within 64 map keys.

The fixed page size remains eight keys.

Port 0 has two pages; other ports have one.

At 1x1, eight physical plus eight Loopback clusters require 16 keys.

Every cluster has `channel_count=1`.

No map interface or owner resource ceiling increases.

The constructor still refuses a 65-key negative control.

The builder test also generates complete descriptor images for both shapes.

Loopback destination indices follow the input pools' declaration order.

Output sources identify those destinations, independent of their current mappings.

The new output pool follows physical sources, matching factory-map priority.

## Implementation status

The mapped copy, synchronous capture reads, and descriptor pools are implemented.

The enabled 8x8 firmware exceeds its unchanged control-memory ledger.

Its product allocation remains refused; measurement exports record S14 debt.

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

Fresh leaf measurements are recorded on PR #987.

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

Disabled leaves retain their original ports and widths.

Enabled connections extend existing buses above their original fields.

Capture extends `lb_tdata_i` with the synchronous sample return.

Capture extends `tdm_walk_ns_o` with claim, read, and destination.

Queue extends `s_tdata_i` with map and capture controls.

Queue extends `m_tdata_o` with the synchronous mono return.

Disabled concatenations contain zero copies of these extensions.

Only the enabled generate branch owns the invalidation register.

The original map writer remains structurally unchanged.

Canonical release elaboration compares identifiers, widths, cells, and connections.

Only comments, attributes, and whitespace are excluded.

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

The buffer has eight pages of up to 64 words.

Each word contains a 24-bit sample, for 12288 sample-storage bits.

Four metadata slots hold validity, frame tags, and capture timestamps.

Those slots cover unclaimed frames at the supported leads.

A claim saves all three bits of its RAM page.

The active walk therefore survives reuse of its metadata slot.

Simple-dual-port operation targets one RAMB18.

It supports one write and one synchronous read.

The review receipts record physical inference and control cost.

Page validity makes old words unreachable without resetting the array.

Frame tags must be checked beyond the modulo page address.

Finite tags require invalidation before reuse, including after stopped clocks.

The capture crossbar reads two mono samples sequentially per pair.

Only the returned pair needs holding registers.

It must not reconstruct the old 32-pair flop bank.

The added request/return cycles enter the capture-walk timing calculation.

Absent or invalid samples become silence; every slot emits.

## Latency and rate contract

Additional audio delay: exactly one local media frame.

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

The wire scoreboard grades this one-frame relationship for both shapes.

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

Two missing domain-frame periods trigger the existing source-row flush.

The flush remains active while the domain is stopped.

This prevents queued future rows from acquiring shifted times on restart.

Only the enabled option adds this clock-loss flush.

A missed publication deadline drops the frame permanently.

Consumers can fan out eligible frames within their capture periods.

Period expiry invalidates frames regardless of retained RAM contents.

## Mapping changes

Use committed logical-map state, never speculative edit rows.

Read the committed map during the fill.

An edit invalidates the entire fill, so a mixed map cannot publish.

This avoids a second 64-entry register snapshot.

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

RTL option: `INPUT_LOOPBACK_P`, default zero.

Config fact: `audio_interface.cluster_mapping.fabric.input_loopback_lane`, default false.

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

## Validation and measurement contract

Exercise received audio through the real acceptance and talker paths.

Select a source stream different from the input port index.

Verify transmitted payload values, channel identity, and event sequence.

Cover ADD, REMOVE, replacement, fan-out, unmapped silence, and underrun.

Cover reset, bind loss, format clipping, and buffer-fill edits.

Observe the first nonzero sample after every invalidation.

Check page/tag wrap and prolonged absence for stale replay.

Plant ignored input mappings, wrong sources, and retained-page replay.

The new controls cover ignored invalidation, skipped copy, wrong bank,
wrong source, retained words, and wrong latency.

The existing render campaigns cover projection and bus-binding faults.

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

Detailed verdicts and exact source hashes are recorded in the review receipts.

## Completion disposition

Implementation must meet every validation and measurement obligation above.

The topology ruling does not relax resource or timing ceilings.

Overflow remains S14 debt; unmeasured behavior remains unclaimed.

## Retention and capture-clock bounds

The supported out-lead is at most two frames.
Eight pages keep a claimed page throughout its capture walk.
A concurrent domain event cannot overwrite that claimed page.
Larger leads fail elaboration before synthesis.
Expiry precedes page reuse; capture consumes each publication once.

The capture timestamp window includes four datapath clock cycles.
Two cover marker synchronization; two cover timestamp quantization.
It also covers 1000 ppm across the prediction horizon.
That horizon is the out-lead plus one media period.
One additional nanosecond covers integer rounding.
At 100 MHz, the maximum window is 104 ns.
At 50 MHz, it is 144 ns.
Both are below half the 48 kHz media period.
Offsets outside this bound may yield silence.
This bound does not claim sample-rate conversion.

The wire scoreboard does not isolate five defensive guards.
They are bind-only flush, one-shot claim, expiry, backlog, and age.
Combined invalidation and steady scheduling currently mask their removal.
They remain untested defence in depth, not mutation-proven guarantees.
