# Torture campaign `ax-rv32-f` — failure rundown and triage

Run concluded 2026-08-04. Device under test: ALINX AX7101, 8 talkers x 8 listeners
x 8 channels, single-hart RV32 VexiiRiscv, gateware VERSION `0x00010021`.

**The build under test predates every fix committed on 2026-08-03.** Six commits
landed after this bitstream was flashed (odd audio-mapping counts, the CRF bind
edge counter wipe, the ACMP SRP compare, the refused-LOCK state, the ACMP context
RAM, the AEM patch port). Nothing in this document should be read as the current
state of the tree — only as the measured state of the flashed silicon.

## Totals

| verdict | count | share |
|---|---:|---:|
| PASS | 3,267 | 52.0% |
| SKIP | 2,575 | 41.0% |
| INFO | 277 | 4.4% |
| **FAIL** | **157** | **2.5%** |
| NEEDS-HUMAN | 4 | 0.1% |
| CONFORMANT-REFUSAL | 2 | <0.1% |
| KNOWN-PENDING | 1 | <0.1% |
| **total** | **6,283** | |

`CONFORMANT-REFUSAL` is a verdict in its own right: the DUT refused something it
was *required* to refuse. It is a pass with a different name, not a near-miss.

## Attribution

Every grader names the side it holds responsible rather than recording a generic
pair disagreement. On that basis:

| attributed side | failures | share of FAIL |
|---|---:|---:|
| PEER (peer) | 102 | 65% |
| AX7101 (our DUT) | 55 | 35% |

## The failure classes

Five classes account for all 157. There is no long tail.

| # | class | n | side | area(s) | stream indices | governing clause | verdict |
|---|---|---:|---|---|---|---|---|
| 1 | `counters.stream_input.update-law-per-counter` | 37 | PEER | matrix 33, churn 2, physical 2 | 0, 2, 4, 6, 8 | Milan Table 5.6 + 1722.1 Table 7-157 | **UNSAFE TO ATTRIBUTE** — see below |
| 2 | `xside.peer-counter-semantics` | 37 | PEER | matrix 33, churn 2, physical 2 | 0, 2, 4, 6, 8 | Milan Table 5.4 / 5.6 interval law | **UNSAFE TO ATTRIBUTE** — same 37 observations as #1 |
| 3 | `counters.stream_input.frames-rx-advances` | 29 | **AX** | churn 14, audio 8, matrix 7 | 0-7 (all) | Milan Table 5.6 FRAMES_RX | **OURS — real, needs work** (8 audio suspect) |
| 4 | `stream.starts-on-bind-alone` | 27 | PEER 14, **AX 13** | churn 16, matrix 11 | AX: 0 only; PEER: 0, 1 | Milan 5.3.7.3 (no STREAMING_WAIT) | **SPLIT** — ours is index 0 only |
| 5 | `counters.stream_output.frames-tx-advances` | 27 | PEER 14, **AX 13** | churn 16, matrix 11 | AX: 0 only; PEER: 0, 1 | Milan Table 5.4 FRAMES_TX | **SPLIT** — co-reported with #4 |

Classes 4 and 5 are emitted as a pair from the same step (`*.start-if-needed`), so
27 + 27 describes 27 events, not 54.

---

## 1 & 2 — the peer counter finding (74 failures, 47% of the total)

Both graders describe the same 37 observations. The claim is that the PEER's
`FRAMES_RX` and `TIMESTAMP_VALID` advance at wire frame rate rather than at the
Milan observation-interval rate (interval bounded above by 1 s).

Measured: **18,048 ticks/s** over a 4.0 s window (72,192 ticks) on
`axt0 -> peerl0`.

**Do not act on this yet.** The number does not reconcile with our own silicon:
this project measured `TIMESTAMP_VALID` at **8,002/s** on a bound stream input,
which is the expected AAF packet rate for 48 kHz class A. A peer counting
18,048/s on a stream we transmit at ~8,000/s is internally inconsistent. Exactly
one of these is true:

- the PEER counts something other than received AVTPDUs (its finding, minor); or
- **our talker is transmitting at roughly 2.26x the correct packet rate** (our
  defect, and a far more serious one than any counter-semantics issue).

The second possibility is not excluded by anything in this run, and it would
invalidate the "peer is at fault" reading entirely.

**Discriminating measurement:** a wire capture of that stream's actual packet
rate. The ProfiShark settles it in one pass. Until then these 74 rows are
*unattributed*, not "the peer's problem".

The index set `{0, 2, 4, 6, 8}` matches the campaign's PEER listener binding
exactly (listeners 0/2/4/6 plus CRF media clock input 8), which confirms the rows
describe the peer's stream inputs and not ours.

## 3 — our listener FRAMES_RX does not advance (29 failures)

Ours, and the index set is the story: **all eight listener inputs, 0 through 7**,
not a subset. A defect confined to one index would point at per-index plumbing;
all eight points at something common — steering, the shield, or the counter's
interval tick itself.

Of the 29:

- **8 are in the `audio` area and are probably contaminated.** Their steps are
  `audio.identity.loop-ch12.t0` through `t4` — the channel-identity loop. A
  looping music player held the playback device during part of the run before it
  was stopped, which manufactures spurious device-busy failures in exactly this
  area. Re-run required before these count.
- **21 are in `churn` and `matrix`** and are not explained by that.

Note this coexists with a **PASS** result from earlier silicon work, where a bound
stream input served mask `0xFFF` live with `FRAMES_RX` interval-conformant at
1/s. So the counter is not universally dead — the failing condition is narrower
than "FRAMES_RX never moves", and identifying it is the work.

## 4 & 5 — streaming did not start on bind alone (27 events)

Milan 5.3.7.3 makes a bind plus a Listener Ready the *whole* licence to stream:

> "As long as a PAAD is declaring a Talker Advertise attribute and receiving a
> Listener Ready or Listener Ready Failed attribute for a Stream Output, it shall
> be streaming AVTP packets. This specification excludes the possibility for a
> Stream Output to be stopped (STREAMING_WAIT state shall not be implemented)."

The harness is built to see this honestly: it **measures first**, sends
`START_STREAMING` only if nothing moved, and records which of the two happened. A
harness that always sends the command cannot tell the difference, which is how a
workaround becomes an invisible permanent behaviour.

- **Ours: 13 events, all on talker index 0.** Index 0 only is a strong hint — the
  same shape as an already-tracked idx>0 egress defect stack, but inverted, and
  worth checking against it directly.
- **PEER: 14 events, indices 0 and 1**, reported with
  `licence_state: OPEN` and `why: "nothing moved: no frame was transmitted or
  received in the window under either reading"`.

The PEER half concentrates in `churn.implicit-rebind.*`, i.e. after a rebind
rather than on a first bind. Two prior rounds on this project traced an
identically-shaped "streams do not flow" cluster to **bench state**, not fabric —
reservations not reaching READY, or gPTP not leased after a reboot. That history
earns this cluster suspicion before it earns a defect report.

---

## Items requiring a human

Four checks cannot self-serve; all four need the same physical action:

> Unplug the DUT's Ethernet cable for 5 s, then plug it back into **the same**
> switch port. Then repeat into a **different** port.

| check | what it proves |
|---|---|
| `adp.alive` | the entity re-advertises after a link bounce |
| `counters.avb_interface.mask` | interface counters survive and resume |
| `stream.recovers-without-intervention` | streams restart with no controller action |
| `srp.reservation-reestablished` | the reservation is rebuilt, not orphaned |

Best done **after** the next flash, so it exercises the build carrying the
2026-08-03 fixes rather than the one this run measured.

## Recommended order

1. **Wire-capture the talker packet rate.** One capture decides whether 74 rows
   are a peer finding or our own transmit defect. Nothing else should be
   attributed until this is settled.
2. **Flash** the build carrying the 2026-08-03 fixes, together with the rebuilt
   root filesystem, then cold-cycle.
3. **Re-run this identical suite** for a clean before/after. Several classes here
   are expected to clear on the new gateware; which ones actually do is the
   measurement that matters.
4. **Re-run the audio area with no player running** to remove the 8 contaminated
   rows.
5. **Then** work the residue: our listener `FRAMES_RX` across all eight indices,
   and the talker index 0 streaming licence.
