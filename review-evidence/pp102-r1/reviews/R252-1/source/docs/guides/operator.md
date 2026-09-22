<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Operator guide — bringing a device up and telling working from broken

You have a board running this control plane and a controller — Hive, or something built on
la_avdecc — and you need to know whether it is healthy, and if not, where it stopped. This
page is about observable behaviour: what appears on the wire, what a controller sees, and
what every diagnostic counter means.

Two pictures do most of the work:

- **[`../diagrams/23-bringup-decision.svg`](../diagrams/23-bringup-decision.svg)** — the
  bring-up ladder. Seven questions in order, and the exact counter to read when one
  answers no.
- **[`../diagrams/24-adp-acmp-states.svg`](../diagrams/24-adp-acmp-states.svg)** — the two
  state machines you can watch live.

---

## 1. What this device does on the wire

It is the **control plane** of a Milan audio end-station. It never carries audio; it
announces the entity, answers controllers, negotiates bindings, and reserves bandwidth.

| Traffic | Address and type | What it is |
|---|---|---|
| ADP — discovery | destination 91:E0:F0:01:00:00, EtherType 0x22F0, subtype 0xFA | ENTITY_AVAILABLE every 5 seconds plus a randomised delay, 82 bytes on the wire |
| ACMP — binding | same multicast, subtype 0xFC | the Milan truncated form, 56 bytes |
| AECP — commands | **unicast** to and from the controller, subtype 0xFB | AEM and Milan Vendor Unique |
| MSRP — reservation | destination 01:80:C2:00:00:0E, EtherType 0x22EA | Talker and Listener declarations, Domain |
| MVRP — VLAN | destination 01:80:C2:00:00:21, EtherType 0x88F5 | VLAN membership for the stream VLAN |

Class A defaults to priority 3 on VLAN 2 until a bridge Domain declaration is adopted.

Two things it deliberately does **not** do, and which you should not go looking for:

- **It allocates no stream destination addresses.** MAAP lives in the surrounding
  fabric. If that allocator is absent, this processor's talker half is silent *by
  construction* — see question 7 of the ladder.
- **It carries no AVTP, no gPTP datapath and no media clock.** Those are neighbours, not
  parts of it.

## 2. What a controller sees

| Controller action | What this device answers |
|---|---|
| Discovery | the entity appears within one advertise cadence, with a monotonically rising `available_index` |
| Reading the model | descriptors served out of the integrator's main memory. If the image was never loaded, every `READ_DESCRIPTOR` answers `BAD_ARGUMENTS` because the store reports zero configurations, never a garbage descriptor |
| An unimplemented command | `NOT_IMPLEMENTED` with the command **echoed back**, correctly sized. Never silence, never a malformed frame |
| `IDENTIFY_NOTIFICATION` sent as a command | `BAD_ARGUMENTS` — the opcode-specific rule of IEEE 1722.1-2021 §7.4.39.2 beats the general fallback of §9.3.5.3.3 |
| `ACQUIRE_ENTITY` | `NOT_SUPPORTED`. Milan §5.4.2.1 says acquisition shall never succeed |
| `DISCONNECT_TX` | always `SUCCESS`, and it changes nothing. The Milan talker is stateless |
| `GET_TX_CONNECTION` | `NOT_SUPPORTED`, for the same reason |
| A command addressed to another entity | dropped and counted. A command that is an AECP *response* is dropped too — answering a response is how a control plane builds a storm |
| Anything, while the response memory is broken | a well-formed 60-byte `ENTITY_MISBEHAVING`. It is an honest failure, not a hang |

A controller that cannot see the device at all, when a capture shows the frames leaving,
is nearly always a controller that never joined the 91:E0:F0:01:00:00 group. Raw-socket
tools must join it explicitly.

## 3. Milan names, IEEE names

This repository uses Milan naming throughout. If your controller shows the IEEE names:

| Milan | IEEE 1722.1 |
|---|---|
| `BIND_RX` | `CONNECT_RX` |
| `UNBIND_RX` | `DISCONNECT_RX` |
| `PROBE_TX` | `CONNECT_TX` |

---

## 4. The diagnostic side port

Everything below is read through the management side port. `host_addr_i` is a 20-bit
**word** address, not a byte address — if your bridge hands it a byte address, everything
you read will be from the wrong place. The space has six windows:

| Window | Access | State in the landed top |
|---|---|---|
| 0x00000 | write before `entity_enable`, read | reserved seam. **Reads 0x00000000** — the descriptor image is loaded into main memory by software, not through here |
| 0x10000 | read only | reserved seam. **Reads 0x00000000** |
| 0x20000 | read only | **the snapshot window** — everything in section 5 |
| 0x30000 to 0x300FF | read/write | control and status, section 6 |
| 0x40000 | read only | the trace ring, section 7 |
| 0x50000 | read/write | firmware mailbox — **disabled**, so every access is refused |

Any refused access — a write to a read-only window, an image write after
`entity_enable`, or an unmapped address — answers with the error flag one cycle later and
is never forwarded. Reading the snapshot window can never change behaviour.

---

## 5. The snapshot window, word by word

Word address = 0x20000 + N. Every counter here **saturates**: a maximum reading means "at
least this many", never "none". This map is transcribed from
[`protocol_processor_top.sv`](../../hdl/top/protocol_processor_top.sv); if you change the
top, change this table.

### Identity and health

| N | Bits | Field |
|---|---|---|
| 0 | 31:0 | magic 0x4B4C5050. A wrong value means the side port is mis-wired |
| 1 | 31:24 / 23:16 / 15:8 / 7:0 | built shape: Stream Inputs / Stream Outputs / RX slots / TX slots |
| 2 | 31:0 | free-running millisecond timebase. Frozen means no clock, or reset still asserted |
| 3 | 0 | `entity_enable_i` |
| 3 | 1 | `link_up_i` |
| 3 | 2 | PRNG has taken its one seed — it seeds once, on the first link-up |
| 3 | 3 | an SRP Domain was **adopted** from a bridge; 0 means still on defaults |
| 3 | 4 | at least one source was refused against the port bandwidth ceiling |
| 3 | 5 | NVM alarm — commit retries exhausted, sticky |

### What the RX front end threw away

| N | Bits | Field |
|---|---|---|
| 4 | 31:16 / 15:0 | frames dropped on destination address / on EtherType |
| 5 | 31:16 / 15:0 | dropped on subtype / on version |
| 6 | 31:16 / 15:0 | dropped on length · RX slot-pool overruns |
| 9 | 15:0 | header-latch drops in the top's RX glue |
| 29 | 31:16 | RX front-end drops |

A rising destination-address count while a controller is talking means it is addressing
someone else. A rising overrun count means frames arrived faster than the engines drained
them.

### Dispatch and back-pressure

| N | Bits | Field |
|---|---|---|
| 7 | 31:24 / 23:16 / 15:8 | queue occupancy: ADP / ACMP / AECP |
| 8 | 31:16 / 15:0 | stall cycles: ADP / ACMP |
| 9 | 31:16 | stall cycles: AECP |
| 15 | 31:24 / 17 / 16 | scoreboard holds outstanding / table full / barrier pending |
| 15 | 15:0 | trace-ring write count |
| 24 | 31:16 / 15:0 | timer-arm drops · MRP frames dropped at the strip queue |
| 25 | 18:3 / 2:0 | RX slots free (ADP replica) · TX slots free |
| 28 | 23:8 / 7:0 | talker-response lane drops · SRP service-face drops |

These are **stall** counters, not overflow counters: the dispatch queues never drop, so a
rising count means an engine was slow, not that work was lost.

### Transmit

| N | Bits | Field |
|---|---|---|
| 26 | 31:16 / 15:0 | arbiter grants on the ACMP lane / the ADP lane |
| 27 | 31:16 / 15:0 | arbiter grants on the SRP lane / the talker-response lane |

Grants rising while a capture shows nothing on the wire places the fault below this
processor, in the MAC path.

### Discovery and binding

| N | Bits | Field |
|---|---|---|
| 31 | 1:0 | advertise machine: 0 DOWN · 1 DRAW · 2 DELAY · 3 WAITING |
| 28 | 31:24 | per-sink binding installed, one bit per sink |

### Reservation

| N | Bits | Field |
|---|---|---|
| 10 | 18:16 / 11:0 | Class A priority / Class A VLAN id in force |
| 11 | 31:0 | summed granted idleSlope over admitted sources, in bit/s |
| 12 | 31:24 / 23:16 / 15:0 | per-source admitted / per-source active / registered Talker attribute, two bits per source |
| 13 | 31:16 / 15:0 | our Talker declaration / registered Listener attribute, two bits each |
| 14 | 31:16 / 3:0 | our Listener declaration / active VLAN memberships |
| 16 to 23 | 31:0 | registered accumulated latency for sink 0 to 7, in nanoseconds, raw |
| 29 | 7:0 | registered Failed code for sink 0 |
| 30 | 31:0 | granted idleSlope for source 0, in bit/s |

### AECP and the memory faces

| N | Bits | Field |
|---|---|---|
| 32 | 31:16 / 15:0 | commands accepted / responses emitted |
| 33 | 31:16 / 15:0 | commands dropped / descriptor locate misses |
| 34 | 0 | **descriptor image valid** — the magic, layout version and checksum at `DESC_BASE_P` all agreed |
| 34 | 4:1 | descriptor-store fault code |
| 34 | 9:5 | status of the last response |
| 34 | 20:10 | length of the last response |
| 35 | 31:16 / 15:0 | responses voided by the response memory / lanes written to it |
| 36 | 2:0 | last fault code on the response-memory master |

Word 34 bit 0 reading 0 is the single most common cause of an entity that discovers
cleanly and then shows nothing in a controller: the model lives in the integrator's
memory and software has not put it there. A late load heals it without a reset.

---

## 6. The control window

Word address = 0x30000 + N.

| N | Access | Field |
|---|---|---|
| 0 | read/write | a scratch register. Writing then reading it back is the cheapest proof the side port works in both directions |
| 1 | read only | bit 0 `entity_enable_i` · bit 1 restore busy · bit 2 restore done · bit 3 restore failed |

`restore_fail_o` means a torn read-back aborted the whole boot restore — deliberately, so
a partial set of bindings is never preloaded. A blank device is not a failure: a record
that fails its framing check is skipped, and that sink simply starts unbound.

**Do not read restore done as restore succeeded.** It says the walk reached its end,
which every skipped record also does, so a device whose NVM is blank — or whose
integrator never wired a backend at all — publishes the same two bits as one that
restored every sink. `restore_blank_o` is the third pin: set when the completed walk
validated zero records. Whether there is any media behind the device face is a fact
only the integrating fabric holds, and it has to publish that too.

## 7. The trace ring

Word address = 0x40000 + N, where bits 1 and 0 of N select the 32-bit lane and bits 9
through 2 select the record. Each record is four lanes, most significant word first.

The ring overwrites oldest-first and **never back-pressures a producer** — tracing may
lose history, it must never stall the plane. Snapshot word 15 bits 15 through 0 carry the
monotonic write count: its low bits are the write pointer, and it is how you find the head
and detect a wrap.

---

## 8. Reading the two state machines

Both are in
[`../diagrams/24-adp-acmp-states.svg`](../diagrams/24-adp-acmp-states.svg).

**The advertise machine** is live at snapshot word 31. `WAITING` is the healthy resting
state — it has already sent an ENTITY_AVAILABLE and is counting to the next. `DOWN` means
a gate is down, not a fault: Milan §5.6.1 holds the entity silent until `entity_enable_i`.

Note that the two ways out of advertising are different, and a controller can tell:

- **link down** goes quietly to `DOWN` and sends nothing (Milan §5.6.3.5.6);
- **deasserting `entity_enable_i`** is the shutdown — it emits ENTITY_DEPARTING and
  resets `available_index` to 0.

**The listener binding machine** is what a controller reads back as `probing_status` in
`GET_STREAM_INFO`: 0 DISABLED, 1 PASSIVE, 2 ACTIVE, 3 COMPLETED. `PASSIVE` means bound but
still waiting for the talker to be discovered — which is a talker problem, not a binding
problem. The full transition matrix is
[F05.3](../architecture/05_acmp_engine.md#fig-05-listener-matrix); the summary in the
diagram is a vocabulary, not a path.

Bindings **survive a power cycle**. On boot a restored binding starts in `PRB_W_AVAIL` and
re-probes; it does not resume as though nothing happened.

---

## 9. Four honest failures, and what each one means

This processor is built so that a broken neighbour produces a truthful answer rather than
silence. Recognising these four saves a lot of time.

| On the wire | Means |
|---|---|
| `BAD_ARGUMENTS` for every `READ_DESCRIPTOR` | the descriptor image is missing, truncated or corrupt; its zero configuration count fails before locate. Check snapshot word 34 bit 0 |
| `NO_SUCH_DESCRIPTOR` from a direct-locate command | the image is invalid, or the loaded model does not contain that descriptor. Check snapshot word 34 bit 0 |
| `ENTITY_MISBEHAVING`, 60 bytes | the response-memory bridge failed — snapshot words 35 and 36 |
| `TALKER_DEST_MAC_FAILED` from PROBE_TX | this source has no allocated stream address, because the MAAP allocator in the fabric is absent or did not answer |
| `NOT_IMPLEMENTED` with the command echoed | that opcode is genuinely not implemented yet. It is a correct answer, not a fault |

---

## 10. See also

- [Integrator guide](integrator.md) — the memory regions, the tie-off rules and the
  status wires behind these counters.
- [HDL engineer guide](hdl-engineer.md) — if a counter you need does not exist yet.
- [04 ADP](../architecture/04_adp_engine.md), [05 ACMP](../architecture/05_acmp_engine.md),
  [10 SRP](../architecture/10_srp_engine.md) — normative behaviour for each protocol.
