<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->

# AAF latency history ring (`KL_lat_history_ring`)

Roadmap item 11, DDR3 arm. Per-stage AAF pipeline latency, captured as a
**time-series** in a wrapping DRAM ring the CPU / userspace reads back.

## Why a ring (vs the CSR snapshot)

`KL_aaf_latency_taps` (PR #17, CSR base `0x870`) measures per-stage inter-stage
deltas and exposes only the **latest** `min / last / max` over CSR — an
instantaneous snapshot. That answers "what is the latency now" but not "how did
it move over the last N frames": you cannot build a jitter histogram, a tail
(p99) latency, or catch a transient burst from a single-value register.

`KL_lat_history_ring` turns **each** latency sample into a fixed 16-byte record
and streams it into a DRAM ring (the same ring pattern as the PCM audio ring).
Userspace mmaps the ring, chases the write pointer, and parses the records — a
full history, post-processed offline.

## Record format (16 bytes, little-endian in DRAM)

`RECORD_BYTES_P = 16`. Bytes are laid out for a packed little-endian struct
(the byte order a RISC-V LE reader gets straight from `mmap`):

| offset | size | field        | meaning                                             |
|--------|------|--------------|-----------------------------------------------------|
| `0`    | `u64`| `ptp_ns`     | gPTP nanosecond timestamp at the sample             |
| `8`    | `u32`| `latency_ns` | measured stage latency (ns, or datapath cycles)     |
| `12`   | `u8` | `stage_id`   | documented tap point (see below)                    |
| `13`   | `u8` | `stream_idx` | AAF stream index (NxN)                               |
| `14`   | `u16`| `flags`      | `{gap[15], rsvd[14:12], seq[11:0]}`                  |

- `seq` — rolling per-accepted-record counter (mod 4096). Userspace detects
  **lost or reordered** records by a gap in `seq`.
- `gap` (bit 15) — set on the **first** record written after one or more samples
  were dropped (writer stalled, or ring full in stop mode). A self-describing
  hole marker: a `1` here means "records are missing just before me".

```c
struct lat_rec {          /* 16 bytes, __attribute__((packed)) */
    uint64_t ptp_ns;
    uint32_t latency_ns;
    uint8_t  stage_id;
    uint8_t  stream_idx;
    uint16_t flags;       /* bit15 = gap, bits[11:0] = seq */
};
```

On the 64-bit downstream bus a record is **two beats**:

- beat 0 (lowest address) = `ptp_ns[63:0]`
- beat 1 = `{flags[15:0], stream_idx[7:0], stage_id[7:0], latency_ns[31:0]}`
  (latency in the low 32 bits)

## Ring CSR ABI (reused verbatim from the PCM ring)

The ring-writer control block mirrors the PCM ring (`_PCMRingNxN` /
`milan_dma_pcm`, LiteX bank `0xf0003120`) **field-for-field**, so the userspace
mmap+chase recipe is identical to `pw-milan-ring-source`:

| offset | name        | dir | module port  | meaning                                        |
|--------|-------------|-----|--------------|------------------------------------------------|
| `0x00` | `BASE_HI`   | RW  | `ring_base_i[63:32]` | ring base address, high word            |
| `0x04` | `BASE_LO`   | RW  | `ring_base_i[31:0]`  | ring base address, low word (bytes)     |
| `0x08` | `LENGTH`    | RW  | `ring_len_i`         | ring size in bytes (multiple of 16)     |
| `0x0C` | `ENABLE`    | RW  | `enable_i`           | 1 = run; 0 = clear write pointer + drop |
| `0x14` | `LOOP`      | RW  | `loop_i`             | 1 = wrap+overwrite; 0 = stop when full  |
| `0x18` | `OFFSET`    | RO  | `wptr_o`             | byte write pointer (userspace chase)    |

Plus one history-ring extension (own address, PCM-ABI untouched):

| offset | name        | dir | module port  | meaning                                        |
|--------|-------------|-----|--------------|------------------------------------------------|
| `0x1C` | `DROPPED`   | RO  | `dropped_o`  | records dropped (writer stalled / ring full)   |

`ENABLE=0` clears `OFFSET` to 0 and drops incoming samples (matches the PCM
ring's disable). `LOOP=1` is the normal history mode (newest overwrites oldest);
`LOOP=0` is a one-shot capture that stops when the ring fills and counts the
overflow in `DROPPED`.

The downstream write-request master (`wr_valid_o / wr_data_o / wr_addr_o /
wr_last_o / wr_ready_i`) is the same shape as the PCM ring's
`WishboneDMAWriter` sink, so the existing `milan_dma` DRAM writer carries it
unchanged (`writer.sink.data = wr_data_o`, `writer.sink.address =
wr_addr_o >> 3` for the 64-bit bus, `writer.sink.valid/ready` = the handshake).
`wr_addr_o` is a **byte** address = `ring_base_i + wptr + beat*8`.

## Documented tap points (`stage_id`)

The sample bus is fed by an adapter off `KL_aaf_latency_taps`: each completed
inter-stage delta becomes one record (`latency_ns` = delta × ns/cycle,
`stream_idx` = the AAF stream, `ptp_ns` = the chain epoch). The two chains and
their documented pipeline points:

| `stage_id` | chain | tap point                                             |
|------------|-------|-------------------------------------------------------|
| `0x00`     | TX    | `CAP`     — ring / I2S capture pair in                 |
| `0x01`     | TX    | `PKT_SOF` — packetizer first beat                      |
| `0x02`     | TX    | `PKT_EOF` — packetizer last beat                       |
| `0x03`     | TX    | `MAC_TX`  — frame egresses the MAC boundary            |
| `0x10`     | RX    | `MAC_RX`  — frame ingress                              |
| `0x11`     | RX    | `ACCEPT`  — AVTP monitor parse-complete / accept pulse |
| `0x12`     | RX    | `DEPKT`   — payload last beat                          |
| `0x13`     | RX    | `PCM_RING`— payload accepted at the ring writer        |

`stage_id` for a record is the **destination** stage of the delta (so a record
with `stage_id = 0x01` carries the `CAP -> PKT_SOF` latency, etc.).

### Input contract

`KL_lat_history_ring` takes a **fresh, clean** per-sample bus rather than PR
#17's CSR delta outputs (the taps module publishes aggregate min/last/max, not
a per-sample stream). The adapter that maps taps → samples is trivial and
independent, keeping this module reusable by any latency producer:

```
sample_valid_i   1-cycle pulse: one completed latency sample
sample_lat_ns_i  [31:0]  the measured latency
sample_stage_i   [7:0]   stage_id from the table above
sample_stream_i  [7:0]   AAF stream index
ptp_ns_i         [63:0]  gPTP ns at the sample
```

The producer is **never** back-pressured: a sample offered while the previous
record is still draining to DRAM (or while the ring is full in stop mode) is
dropped and counted in `DROPPED`. `wr_ready_i` gates the emitter only.

## Userspace read recipe (`pw-milan-ring-source` style)

```c
// 1. program the ring (record-aligned base + length), enable loop mode
poke(BASE_HI, ring_phys >> 32);  poke(BASE_LO, ring_phys & 0xffffffff);
poke(LENGTH,  RING_BYTES);       // multiple of 16
poke(LOOP,    1);
poke(ENABLE,  1);

// 2. mmap the ring region (uncached / coherent) and chase the write pointer
volatile uint8_t *ring = mmap(NULL, RING_BYTES, PROT_READ, MAP_SHARED,
                              devmem, ring_phys);
uint32_t rd = 0;                          // our read pointer (bytes)
for (;;) {
    uint32_t wr = peek(OFFSET);           // HW write pointer (bytes)
    while (rd != wr) {
        struct lat_rec *r = (struct lat_rec *)(ring + rd);
        // ... consume r->ptp_ns, r->latency_ns, r->stage_id, ...
        if (r->flags & 0x8000) note_gap();          // records missing before here
        rd = (rd + 16) % RING_BYTES;
    }
    poll_dropped(peek(DROPPED));           // ring-full / stall telemetry
}
```

Because `LOOP=1` overwrites oldest-first, a slow reader that falls more than
`RING_BYTES/16` records behind will read overwritten slots; `seq`
discontinuities and the `DROPPED` counter both flag that. Size the ring for the
worst-case reader latency (e.g. 64 KiB = 4096 records ≈ tens of ms of AAF
history at the class-A frame rate).

## Verification

`tb/verilator/lat_history_ring/` — the TB plays the DRAM writer, snoops every
write beat, reconstructs each record and checks: field byte-exactness, LE record
layout, beat addressing, record base = write pointer, rolling `seq`, `wptr`
advance (+16/record), loop wrap to base, stop-mode full, drop-on-full (stalled
writer + ring full) with the `DROPPED` counter, the `gap` marker, and timestamp
monotonicity. `make -C tb/verilator/lat_history_ring run` → **84 checks, 0
failures, RESULT: PASS**.
