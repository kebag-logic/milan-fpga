# Fault tracing: bare-metal DRAM ring and workstation bundles

Milan fault traces are Common Trace Format (CTF) packets produced by the
bare-metal image into caller-provided DRAM. A bench acquisition link copies
complete raw packet segments to a workstation. The workstation then compresses,
rotates, verifies, and decodes those segments.

The current wire contract is **Milan trace ABI 2**. The contract is
[`milan_trace.yaml`](../../sw/trace/milan_trace.yaml); the generated metadata
that accompanies a bundle is the authority used to decode that bundle.

## Contents

- **[1. Current architecture](#1-current-architecture)** — The device/workstation boundary and the files that implement it.
- **[2. ABI 2](#2-abi-2)** — Common context, clock, packet shape, and compatibility rules.
- **[3. Event IDs and categories](#3-event-ids-and-categories)** — The exact numeric map and the subsystem each event describes.
- **[4. Ring and extraction contract](#4-ring-and-extraction-contract)** — Packet ownership, overwrite behavior, and segment handoff.
- **[5. Workstation bundle format](#5-workstation-bundle-format)** — Independent segment files, metadata colocation, and atomic packing.
- **[6. Rotation and eviction](#6-rotation-and-eviction)** — Oldest-first retention with a pinned first-fault segment.
- **[7. Compression](#7-compression)** — The measured, pinned workstation filter chain.
- **[8. Torn-input recovery](#8-torn-input-recovery)** — Exact-prefix recovery and its integrity boundary.
- **[9. Validation and ABI changes](#9-validation-and-abi-changes)** — The executable evidence and safe update sequence.
- **[10. Reading a trace](#10-reading-a-trace)** — Verify, unpack, and inspect commands.
- **[11. Scope and limits](#11-scope-and-limits)** — What this repository supplies and what integration must provide.

## 1. Current architecture

```text
bare-metal event producer
        |
        v
barectf C producer + milan_trace.c
        |
        v
caller-provided DRAM ring (fixed 4 KiB CTF packet slots)
        |
        | milan_trace_segment_begin/packet/end
        v
bench acquisition link (copies complete raw packets)
        |
        v
workstation trace_segment.py
        |
        +-- independent .ctf.xz segments + matching metadata
        +-- ctf_read.py or babeltrace2
```

The firmware side ends at the raw-segment API. Path handling, compression,
retention, and decoding run on the workstation after acquisition.

| Source | Responsibility |
|---|---|
| [`milan_trace.yaml`](../../sw/trace/milan_trace.yaml) | ABI environment, packet layout, enums, and 23 event types |
| [`generated/metadata`](../../sw/trace/generated/metadata) | Checked-in CTF 1.8 decode contract |
| [`generated/barectf.c`](../../sw/trace/generated/barectf.c) and [`barectf.h`](../../sw/trace/generated/barectf.h) | Checked-in dependency-free C producer |
| [`milan_trace.c`](../../sw/trace/milan_trace.c) and [`milan_trace.h`](../../sw/trace/milan_trace.h) | Freestanding DRAM ring, arming, accounting, and extraction API |
| [`trace_segment.py`](../../sw/trace/trace_segment.py) | Workstation pack, unpack, verify, rotate, and ratio commands |
| [`ctf_read.py`](../../sw/trace/ctf_read.py) | Metadata-driven CTF reader using the Python standard library |
| [`test_trace_roundtrip.py`](../../sw/trace/test_trace_roundtrip.py) | Host-runnable end-to-end contract gate |

## 2. ABI 2

`environment.milan_trace_abi` in the YAML and `MILAN_TRACE_ABI` in
`milan_trace.h` are both 2. The `boot.abi` payload repeats the value in-band.
Every bundle carries the generated metadata from the same ABI because barectf
assigns event IDs by sorted event name. Current metadata must never be
substituted for the metadata shipped with an older bundle.

Every event has two one-byte common-context fields.

| `sev` value | Meaning |
|---:|---|
| 0 | `DEBUG` |
| 1 | `INFO` |
| 2 | `NOTICE` |
| 3 | `WARN` |
| 4 | `ERROR` |
| 5 | `FATAL` |

`WARN` and above arm extraction; severity is therefore both diagnostic data and
an input to the extraction policy.

| `src` value | Category |
|---:|---|
| 0 | `FABRIC` |
| 1 | `JOURNAL` |
| 2 | `LINKMON` |
| 3 | `PROVISION` |
| 4 | `AUDIO` |
| 5 | `FIRMWARE` |
| 6 | `TRACE` |
| 7 | `TEST` |

The CTF clock is a free-running 1 MHz monotonic counter. It is not the gPTP
clock: gPTP time and corrections are ordinary `ptp` payload fields, so a time
correction cannot reorder the trace container. Packet begin/end timestamps are
64-bit. Event timestamps carry the low 32 bits and wrap after 2^32 microseconds
(about 71.6 minutes); the producer must emit `heartbeat` at least every 60
seconds so readers can extend them unambiguously.

Packets are little-endian and include the CTF magic, stream ID, total and
content sizes, 64-bit begin/end timestamps, discarded-record snapshot, packet
sequence, and `boot_id`. The magic and fixed-size slots let the reader stop at
the last structurally valid complete packet when input ends early.

## 3. Event IDs and categories

The numeric IDs below are ABI data. The category column is a navigation aid;
it is not another encoded field. Payload fields and enum values are generated
in the complete [`TRACE_EVENTS.md`](../reference/TRACE_EVENTS.md) catalogue.

| ID | Event | Design area |
|---:|---|---|
| 0 | `acmp_listener` | Connection control |
| 1 | `avtp_rx` | AVTP/audio receive |
| 2 | `boot` | Firmware lifecycle |
| 3 | `csr_access` | Diagnostic CSR audit |
| 4 | `firmware_lifecycle` | Firmware lifecycle |
| 5 | `heartbeat` | Trace continuity |
| 6 | `journal` | Saved-state journal |
| 7 | `link` | Link supervision |
| 8 | `ltap` | Datapath latency |
| 9 | `maap` | Address allocation |
| 10 | `mac_reset` | Link/reset supervision |
| 11 | `mediaclk` | Audio timing |
| 12 | `note` | Typed-event escape hatch |
| 13 | `parser_probe` | AVTP parser/match path |
| 14 | `ptp` | gPTP state and time payload |
| 15 | `ring` | Datapath ring accounting |
| 16 | `srp` | Stream reservation |
| 17 | `srp_refusal` | Stream-reservation refusal |
| 18 | `stream_ctx` | Stream provisioning state |
| 19 | `stream_ctx_write` | Stream provisioning writes |
| 20 | `trace_drop` | Trace loss accounting |
| 21 | `trace_evict` | Workstation retention accounting |
| 22 | `trace_flush` | Segment extraction accounting |

Adding or renaming an event can renumber every name that sorts after it. The
round-trip gate pins this entire map so such a change is explicit.

## 4. Ring and extraction contract

`milan_trace_init()` receives aligned DRAM, packet size/count, a monotonic clock
callback, and a boot identifier. The default packet size is 4 KiB. At least two
slots are required so the open writer packet and the segment reader cannot
share one slot.

The producer never blocks event emission. When it laps the ring it overwrites
the oldest complete packet and increments both its statistics and CTF discarded
record accounting. A missing interval is therefore observable.

Extraction is a three-call ownership protocol:

1. `milan_trace_segment_begin()` closes the open packet and selects complete
   packets oldest first. The default maximum is 64 packets, or 256 KiB.
2. `milan_trace_segment_packet(i)` returns each fixed-size slot. Acquisition
   must copy all selected packets before allowing enough new events to lap them.
3. `milan_trace_segment_end(ok)` releases the view, resets arming only after a
   successful copy, and reports any slots overwritten while the view was open.

A `WARN`-or-higher event arms extraction. The library also applies the
configured minimum interval and byte budget so trace export cannot monopolize
the acquisition link. A heartbeat is emitted by the firmware caller because
only that caller knows uptime and its active subsystem bitmap.

## 5. Workstation bundle format

[`trace_segment.py`](../../sw/trace/trace_segment.py) turns each raw segment
into an independent xz stream. Independent files contain damage to one segment
and let retention remove complete segments.

Packing writes a temporary workstation file, synchronizes it, and atomically
replaces the final name. The matching CTF metadata is copied into the bundle,
so decode never depends on the metadata in a later checkout.

## 6. Rotation and eviction

The firmware ring is drained oldest first. Workstation retention also removes
the oldest eligible segment first, leaving packet order as the single ordering
rule across the handoff. Segment 0 is pinned because it represents the first
captured fault after boot. A `trace_evict` event makes an intentional retention
decision distinguishable from a segment that was never acquired.

## 7. Compression

The pinned chain is LZMA2 preset 0, a 256 KiB dictionary, CRC-32, and one block.
On the checked-in 1.75 MiB benchmark, preset 0 produced a 0.2104 ratio in 8.9 ms
per 256 KiB segment; preset 6e produced 0.1997 in 49.6 ms. The small byte saving
does not justify the higher workstation cost. The round-trip gate remeasures
the current producer and enforces a ratio below 0.40.

## 8. Torn-input recovery

The unpacker tolerates an incomplete xz stream and returns the bytes that were
decoded before the break. `ctf_read.py` then admits only structurally valid
whole packets, so recovery is an exact event prefix. Such a prefix is not
CRC-verified and is reported as truncated; it is never presented as an intact
segment. Raw input ending within a CTF packet follows the same whole-packet
rule.

## 9. Validation and ABI changes

Run the complete gate from the repository root:

```sh
python3 sw/trace/test_trace_roundtrip.py
```

Its 15 checks cover generated-source freshness when barectf is available, the
pinned event map, warning-clean C compilation, all 23 event types, compression,
raw and compressed truncation, damaged-packet refusal, timestamp-wrap margin,
export accounting, workstation rotation, bundle bounds, optional babeltrace2
agreement, and catalogue freshness. Missing optional tools are reported as
explicit skips; all other checks still run.

For any ABI edit:

1. Edit `milan_trace.yaml`; append payload members rather than changing the
   size, signedness, order, or meaning of existing members.
2. Increment `environment.milan_trace_abi` and keep `MILAN_TRACE_ABI` and the
   `boot.abi` emission in step.
3. Regenerate the checked-in barectf outputs using the pinned procedure in
   [`sw/trace/README.md`](../../sw/trace/README.md).
4. Update the `EVENT_IDS` map if sorted names changed.
5. Regenerate the catalogue with
   `python3 sw/trace/gen_trace_events.py`.
6. Run the round-trip gate and review the ABI diff as one change.

## 10. Reading a trace

All paths in this example are workstation paths:

```sh
python3 sw/trace/trace_segment.py verify /path/to/milan-trace-bundle
python3 sw/trace/trace_segment.py unpack /path/to/milan-trace-bundle -o /tmp/milan-trace
python3 sw/trace/ctf_read.py /tmp/milan-trace --format summary
python3 sw/trace/ctf_read.py /tmp/milan-trace --min-sev WARN
babeltrace2 /tmp/milan-trace   # optional
```

Always point the reader at the unpacked directory containing the bundle's own
`metadata` file.

## 11. Scope and limits

This repository supplies the ABI, generated producer, freestanding ring,
segment-copy contract, workstation bundle tools, reader, and executable tests.
The physical acquisition link and its scheduling are board-integration choices;
they must preserve packet boundaries and satisfy the three-call ownership
protocol.

The ring is volatile until acquisition copies a segment. A producer can lap an
open segment if acquisition stalls, but the API reports that condition. The
workstation recovery path can return a structurally valid packet prefix from
incomplete input; it cannot reconstruct bytes that were never copied.
