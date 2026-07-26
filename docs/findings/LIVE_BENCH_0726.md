# Live bench campaign — 2026-07-26

Read-only health and function sweep of both boards plus the controller host,
run after the round that closed the fabric-listener blocker. **Nothing here was
reflashed**: both boards carry pre-round gateware, so this is a regression and
health baseline for what *is* deployed, not a test of this round's RTL.

Roles (see [`BENCH_TOPOLOGY.md`](BENCH_TOPOLOGY.md) for the map):

| role | board | flashed VERSION | uptime at test |
|---|---|---|---|
| listener + talker | AX7101 (8×8 shape) | `0x0001_000B` | 21.6 h |
| listener + talker | Arty (4×4 shape) | `0x0001_000A` | 79.7 h |
| controller host | x86 host, PipeWire | — | 13.3 h |

## Verdict

**Both boards healthy and streaming bidirectionally.** No kernel errors on
either, no MAC errors, no CRC errors, gPTP converged, and a live audio capture
off the listener is bit-plausible and correctly sized.

## What was confirmed

### gPTP domain is converged, and the AX is grandmaster

Both boards report the **same** grandmaster identity, and it is the AX's own
entity ID — so the AX is GM and the Arty is synced to it. That is a healthy
two-node domain and it matches the long-standing finding that the switch never
masters into the board ports.

### The two boards stream to each other

Read through the `0x800` window with SNAP discipline:

| board | listens to stream_id | route |
|---|---|---|
| AX | `0x0200_0000_0002_0000` (the Arty's MAC + uid 0) | DMA |
| Arty | `0x0200_0000_0001_0000` (the AX's MAC + uid 0) | RENDER \| DMA |

Both directions are live and both talkers are emitting (`AAF_FRAMES` ticking on
each).

### The listener-blocker workaround persists

The AX's entry-0 override — staged sid + `CTRL = 0x3`, applied earlier the same
day — was **still armed 21 h later** (`A_STRMW_CTRL` reads `0x3`, sid intact)
and the listener is still accepting: `AVTPRX_FRX` = 152.7 M and climbing
~14 k/s under the tick test. The workaround is stable across a long soak, not a
momentary poke. (The RTL fix that makes it unnecessary is `VERSION 0x000F`,
which is not on either board yet.)

### Stream quality is clean

`AVTPRX_ERR` decodes as `[31:16]` SEQ_NUM_MISMATCH, `[15:8]` UNSUPPORTED_FORMAT,
`[7:0]` TIMESTAMP_UNCERTAIN:

| board | frames accepted | seq gaps | format errors | ts-uncertain |
|---|---|---|---|---|
| AX | 152.7 M | 11 | **0** | **0** |
| Arty | 1.95 **G** | 51,523 | **0** | **0** |

Zero format errors and zero timestamp-uncertain on nearly **two billion** frames
is the meaningful result: the packetizer, the wire format and the presentation
timestamps are right. The only defects are sequence gaps, at 7 × 10⁻⁸ (AX) and
2.6 × 10⁻⁵ (Arty ≈ 0.18/s). Note SEQ_NUM_MISMATCH is a 16-bit field and the
Arty's count is approaching its ceiling — treat it as a floor, not an exact
count, on a long-lived board.

### Live audio capture works

On the AX, `hw:0,0` presents as *"Milan AVB streams … 1 capture"*. A 3-second
capture returned **exactly 1,152,000 bytes** = 48000 × 3 × 2 ch × 4 B — the
expected size to the byte, so no under-runs and no short reads. Content is not
silence: 49,069 of the first 65,536 bytes nonzero, and **256 distinct byte
values**, i.e. full range rather than a stuck pattern.

**Format trap worth recording:** the card accepts **`S32_BE` only** — AVTP wire
byte order. `S32_LE` is rejected outright, and `S32_BE` cannot go into a WAV
container (`arecord` refuses), so a capture must be `-t raw`. The working
command is:

```sh
arecord -D hw:0,0 -t raw -f S32_BE -c 2 -r 48000 -d 3 /tmp/cap.raw
```

## Confirmed-still-broken (already known, now observed live)

* **RMON counters are dead on both boards.** The `0x200` group reads zero and
  does not tick. This is the 2026-07-22 root cause — `i_mac_events` tied to `0`
  in SoC glue — and it is the same structurally-silent-port class as the
  tie-offs closed this round. Not yet fixed on any flashed build.
* **The Arty's netdev reports `speed = -1`** while its own `MAC_STATUS` reads
  100 Mb/s correctly (`[2:1] = 01`). That is exactly the `REQ-MAC-03` gap: the
  CSR now derives `is_1g` from the real speed, but `sw/litex` still ties the
  link/speed inputs to constants and nothing populates the driver's view. The
  fix for the CSR half landed this round; the SoC-glue half did not.

## Observed and explained, not a fault

`rx_dropped` differs by 100× between the boards — AX **18.4/s**, Arty
**0.18/s** — with `rx_errors = 0` and `rx_crc_errors = 0` on both. The AX rate
matches control-plane multicast the host receives but has no socket for
(gPTP ~8-16/s, plus ADP, MAAP and the MRP pair). Dropped is not errored, and the
AVB stream itself does not traverse that path — the AX accepted 152.7 M AVTP
frames while its netdev saw only 1.86 M packets, which is the prefilter working
as intended. The asymmetry between boards is unexplained and low-priority.

## Controller host

PipeWire (3 processes) and WirePlumber are up, `ptp4l` is running with
`/dev/ptp0` present, and both boards are reachable. **No Milan node is present
in the PipeWire graph** — `pw-milan-ring-source` is not loaded at the moment.
That is a state observation, not a fault; the ALSA path on the board is what was
exercised above.

## What this campaign could NOT test

Everything this round built, because **neither board has been reflashed**: the
listener fix (`0x000F`), the lwSRP row sizing and per-stream TSpec (`0x0010`),
the six-queue egress map (`0x0011`), DMAC-based control classification
(`0x0012`), the playback chain, the persistence journal and the CTF trace. All
of it is gated behind one Vivado build and a flash.
