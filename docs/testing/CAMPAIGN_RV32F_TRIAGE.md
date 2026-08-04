# Torture campaign `ax-rv32-f` — failure rundown and triage

Run concluded 2026-08-04. Device under test: ALINX AX7101, 8 talkers x 8 listeners
x 8 channels, single-hart RV32 VexiiRiscv, gateware VERSION `0x00010021`.

**The build under test predates every fix committed on 2026-08-03.** Six commits
landed after this bitstream was flashed. Nothing here describes the current tree —
only the measured state of the flashed silicon.

> **HEADLINE: 100 of the 157 failures are defects in our own test harness, not in
> either device.** Two grader bugs account for them, both proven from the run's
> own data. Read section "Harness defects" before acting on any row.

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

## The failure classes

Five classes account for all 157. There is no long tail.

| # | class | n | side | area(s) | indices | root cause | verdict |
|---|---|---:|---|---|---|---|---|
| 1 | `counters.stream_input.update-law-per-counter` | 37 | peer | matrix 33, churn 2, physical 2 | 0,2,4,6,8 | harness rate normalization | **FALSE — harness** |
| 2 | `xside.peer-counter-semantics` | 37 | peer | matrix 33, churn 2, physical 2 | 0,2,4,6,8 | same 37 observations as #1 | **FALSE — harness** |
| 3 | `counters.stream_input.frames-rx-advances` | 29 | **AX** | churn 14, audio 8, matrix 7 | 0-7 (all) | unexplained | **OPEN — ours** (8 contaminated) |
| 4a | `stream.starts-on-bind-alone` | 13 | **AX** | matrix 11, churn 2 | 0 only | harness band classifier | **FALSE — harness** |
| 4b | `stream.starts-on-bind-alone` | 14 | peer | churn | 0, 1 | peer did not stream | **OPEN — peer/bench** |
| 5a | `counters.stream_output.frames-tx-advances` | 13 | **AX** | matrix 11, churn 2 | 0 only | co-reported with 4a | **FALSE — harness** |
| 5b | `counters.stream_output.frames-tx-advances` | 14 | peer | churn | 0, 1 | co-reported with 4b | **OPEN — peer/bench** |

### Summary by disposition

| disposition | failures | share |
|---|---:|---:|
| **False — our harness** | **100** | **64%** |
| Open — ours (AX) | 29 (21 after removing contamination) | 18% |
| Open — peer / bench state | 28 | 18% |

Classes 4 and 5 are emitted as a pair from one step (`*.start-if-needed`), so
27 + 27 describes 27 events, not 54.

---

## Harness defects

### H1 — rate normalization inflates every peer rate by 2.26x (74 failures)

Both graders in classes 1 and 2 report the peer counting at **~18,050/s**. That
is not what the peer does.

The run contradicts itself inside a single step. In
`churn.bind-while-streaming.0.start-if-needed`, from the same counter over the
same window:

| recorded rate | verdict | grader |
|---:|---|---|
| **7,982.24 /s** | PASS | streaming-rate check |
| **18,048.00 /s** | FAIL | `xside.peer-counter-semantics` |

Ratio **2.261**. And 7,982/s is the physical truth: class A AAF at 125 us
intervals is 8,000 packets/s, and this project has separately measured
`TIMESTAMP_VALID` at 8,002/s on its own silicon.

So the peer ticks at the AAF packet rate, exactly as it should, and one grader's
window normalization is wrong by a constant factor. **The peer is exonerated on
all 74 rows.**

### H1b — and the clause was misapplied anyway

Independently of the arithmetic, class 1 cites the wrong law for
`TIMESTAMP_VALID`. IEEE 1722.1-2021 **Table 7-159** defines it as:

> "Increments on receipt of a Stream data AVTPDU with the tv bit set."

That is a **per-frame** counter, and Milan Table 5.6 does not redefine it. A
device ticking it once per received AVTPDU is therefore correct. Our grader
records the citation as Table 7-157 — **the table number in the grader is wrong
and must be corrected to 7-159.**

### H2 — band classifier rejects the mandated interval tick (26 failures)

Classes 4a/5a fail our own talker at index 0. The recorded detail:

```
rate_after_start:     0.996
reading_after_start:  "neither"
start_streaming_status: 11
```

Two things are wrong with that verdict.

**The rate is conformant.** Milan's interval law is "at the end of every
observation interval", the interval bounded above by 1 s — so ~1 tick/s is
exactly the mandated behaviour. This project already established that
(`1.0/s FRAMES_TX is the mandated interval tick`) after an earlier round recorded
the *inverted* verdict on the same counter. The classifier bands 0.996/s as
"neither", i.e. neither per-frame nor interval, almost certainly because it tests
`>= 1.0` against a measurement that lands 0.4% under. **This is the same verdict
inversion, recurring at the boundary.**

**Status 11 is NOT_SUPPORTED.** When the harness sent `START_STREAMING`, our
entity refused it. That refusal is *required*: Milan 5.3.7.3 says STREAMING_WAIT
shall not be implemented, so there is no such command to honour. The harness
records the correct refusal as "the workaround did not work".

Both halves mean the fabric behaved correctly and was failed for it.

---

## Genuinely open

### O1 — our listener FRAMES_RX does not advance (29, of which 21 credible)

Ours, and the index set is the story: **all eight listener inputs, 0 through 7**,
not a subset. A defect confined to one index would point at per-index plumbing;
all eight points at something common — steering, the RX shield, or the counter's
interval tick.

**8 of the 29 are contaminated.** Their steps are `audio.identity.loop-ch12.t0`
through `t4`; a looping music player held the playback device during part of the
run. Re-run that area with no player before counting them.

Note this coexists with a PASS from earlier silicon work where a bound stream
input served mask `0xFFF` live with `FRAMES_RX` interval-conformant at 1/s. The
counter is not universally dead, so the failing condition is narrower than
"FRAMES_RX never moves" — and given H2, check first whether this grader shares
the same boundary bug.

### O2 — the peer did not stream after rebind (28)

Peer indices 0 and 1, concentrated in `churn.implicit-rebind.*`, reporting
`rate 0.0/s` and `"nothing moved: no frame was transmitted or received in the
window under either reading"`. Zero is unambiguous — it is not a normalization
artefact.

Two prior rounds traced an identically-shaped cluster to **bench state**, not
fabric: reservations not reaching READY, or gPTP not leased after a reboot. That
history earns this suspicion before it earns a defect report against the peer.

---

## Items requiring a human

Four checks cannot self-serve. All four need the same action:

> Unplug the DUT's Ethernet cable for 5 s, then plug it back into **the same**
> switch port. Then repeat into a **different** port.

| check | what it proves |
|---|---|
| `adp.alive` | the entity re-advertises after a link bounce |
| `counters.avb_interface.mask` | interface counters survive and resume |
| `stream.recovers-without-intervention` | streams restart with no controller action |
| `srp.reservation-reestablished` | the reservation is rebuilt, not orphaned |

Whether the inline taps can drop a link under software control — which would make
the "same port" half self-serving — is under investigation.

## Recommended order

1. **Fix the two harness defects first.** They are 64% of the failures and they
   actively mislead: H1 accuses a conformant peer, H2 accuses our own conformant
   fabric. Concretely: find and fix the window normalization behind the 2.261x
   inflation; widen the interval band to accept ~1/s with tolerance; correct the
   Table 7-157 citation to 7-159; and teach the harness that a NOT_SUPPORTED
   answer to `START_STREAMING` is *conformance*, not a failed workaround.
2. **Re-run the audio area with no player** to clear the 8 contaminated rows.
3. **Flash** the build carrying the 2026-08-03 fixes plus the rebuilt root
   filesystem, then cold-cycle.
4. **Re-run this identical suite** for a clean before/after.
5. **Then** work the residue: listener `FRAMES_RX` across all eight indices, and
   the peer's post-rebind streaming.

## Lesson

Every one of the 100 false failures came from a grader that was *newly added* to
catch counter-law violations. New checks are as capable of being wrong as the
thing they check, and a grader that disagrees with another grader in the same
step — as H1 did, 7,982 against 18,048 — is self-refuting evidence that was
sitting in the run's own output the whole time. Cross-check new graders against
existing ones on shared observations before trusting a first campaign's verdicts.
