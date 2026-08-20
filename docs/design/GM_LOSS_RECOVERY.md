# Grandmaster loss and recovery — the complete mechanism

Status: fabric-default desk architecture at VERSION `0x0002_0055`
(2026-08-20); booted-board acceptance remains issue #117. The detailed
linuxptp timings below are the **measured option-off comparison baseline** from
the AX7101 08-06/08-07 root-causing session, not estimates. Companion to
[`TIME_SYNC.md`](TIME_SYNC.md) (the steady-state clock architecture);
this document covers the *transient*: what happens, layer by layer, when
the grandmaster disappears, changes, or comes back.

The current root keeps media-clock selection INTERNAL, and the general Table
5.22 notification producer is still missing. Mapping-change notifications are
the implemented exception.

## Current default at 0x0002_0055

The host publication loop is no longer in the product path:

```text
0x88F7 wire <-> KL_gptp_shadow -> PHC adjfine/adjtime
                              -> committed {GM,parent,pdelay,flags} bank
                              -> CSR + AVB_INFO/AS_PATH + tu/asCapable
```

Announce receipt timeout, BMCA, pdelay and servo decisions happen in the pinned
`gptp-processor` engine. A GM change or PHC step still arms
`KL_ptp_clock_validity`'s 0.25 s minimum Annex B holdover. Outside holdover,
`tu` is simply the inverse of the engine's published sync flag; `asCapable`
comes from the adjacent engine flag. CLKV software writes remain ABI-compatible
but have no authority and their lease fields read zero. Thus a daemon crash,
UDS reconnection or polling interval cannot make identity stale or expire a
healthy fabric claim.

`--no-fabric-gptp` retains the measured linuxptp/statd chain described below as
an A/B oracle. The sibling `milan-tests-avb` Buildroot services have not yet
been retired in this repository's WIP: remove ptp4l, phc2sys, milan-statd and
the gptp2csr fallback there, then use #117 to prove a booted default build reads
`tu=0` while synchronised. Until both happen, #116 remains open.

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `crf.media-clock-consumption` | `missing` | - |
| `notifications.change-events` | `partial` | - |
<!-- milan-feature-status:end -->

## Contents

- **[1. What "GM lost" actually is on the wire](#1-what-gm-lost-actually-is-on-the-wire)** — Loss is inferred from announce silence; a deferring device still self-claims when alone, and the real GM's return is a measured 18-60 s phase cliff, not a smooth re-slave
- **[2. The historical ptp4l comparison](#2-the-ptp4l-layer--step-vs-slew-and-the-one-step-budget)** — option-off step/slew measurements
- **[3. The historical publication chain](#3-the-publication-layer--how-the-fabric-learns-about-it)** — the retired UDS/statd/CSR lease baseline
- **[4. The honesty layer — tu](#4-the-honesty-layer--tu-the-timestamp-uncertain-bit)** — common fabric holdover, with owner selected at elaboration
- **[5. The announcement layer — ADP, counters, pushes](#5-the-announcement-layer--adp-counters-pushes)** — The out-of-cycle ADPDU, GPTP_GM_CHANGED, and the single event-law push burst a GM change produces
- **[6. The media layer — where the minutes used to go](#6-the-media-layer--where-the-minutes-used-to-go)** — The root-caused 2-minute walk, and the as-built cure: the 0x002A recenter snap plus the 0x002B free-wheeling lock, with SRP untouched by design
- **[7. The recovery timeline, end to end (as built)](#7-the-recovery-timeline-end-to-end-as-built)** — The full T+0 to T+50s sequence; everything after the GM returns is seconds
- **[8. Traps on record (all hit live, all in memory)](#8-traps-on-record-all-hit-live-all-in-memory)** — The five ways this mechanism burned us on the bench and the cure for each

## 1. What "GM lost" actually is on the wire

gPTP has no "GM lost" message. Loss is inferred: the elected master's
**Announce messages stop arriving**, and after
`announceReceiptTimeout × announceInterval` (3 × 1 s by default) BMCA
re-runs with the remaining candidates. Two consequences that are easy to
misread as defects:

1. **A deferring device still becomes GM when it is alone.** priority1
   250 loses to *anybody*, but an election with no other candidates
   elects yourself — that is BMCA working, not a config failure.
   Measured 08-07: the board (priority1 250) self-claimed within ~3 s of
   the switch's announces vanishing, exactly per
   `LISTENING → MASTER on ANNOUNCE_RECEIPT_TIMEOUT_EXPIRES`.
2. **The return of the real GM is itself a step event.** The board's
   self-mastered epoch and the switch's epoch differ by however long the
   two clocks have diverged — measured **18–36 s** on one occurrence and
   **59.6 s** on another. The hand-off is therefore not a smooth
   re-slave: it is a phase cliff the whole media stack must survive.

## 2. The ptp4l layer — step vs slew, and the one-step budget

**Historical option-off comparison.** None of this restart policy is part of
the default fabric plane; it remains useful as the measured A/B oracle.

When the real GM reappears: `new foreign master` → BMCA `selected best
master clock` → `MASTER → UNCALIBRATED → SLAVE`, typically ~2 s.
What happens to the offset then depends on linuxptp's servo state:

- A **fresh ptp4l instance** spends its `first_step_threshold` budget on
  the first correction: the PHC **steps** the whole cliff at once and the
  servo lands at ns-level in ~10–30 s. Measured: rms 18.0 s → 9 ns in
  12 s; and 59.6 s → **36 ns in under 30 s** after a restart.
- An **already-running instance** has spent that budget. It **slews** at
  the servo's max frequency adjustment — measured closing ~1 s of phase
  per 40 s (~26 000 ppm), i.e. **~40 minutes for a 60 s cliff**. This is
  the "still not locked, still waiting" trap: the daemon is healthy,
  SLAVE, converging — geologically.

**Operational rule (bench-proven the hard way): after a self-GM era
longer than a few seconds, restart ptp4l once** rather than letting it
slew. The restart is cheap (the step + reconverge is seconds); the slew
is not. The roadmap replacement (task #22 software half) is a
PipeWire-style DLL that re-bases on steps instead of the
phc2sys-lineage slew — no restart needed once it lands.

Note the PHC here **is** the fabric timestamp counter (`/dev/ptp0` =
the Q8.24 counter in `timestamp_counter.sv`), so a ptp4l step slams the
fabric's presentation timebase atomically — every downstream layer sees
the cliff in the same cycle.

## 3. The publication layer — how the fabric learns about it

**Historical option-off comparison.** At 0x0055 the engine bank replaces this
entire chain in the default build.

The fabric does not parse Announce. It learns the GM identity from the
**software lease chain**:

```
ptp4l ──UDS/pmc──> milan-statd ──devmem──> ADP_GMLO/HI 0x624/0x628
                    (reference text: gptp2csr.sh)   (atomic LO-then-HI pair)
```

- `TIME_STATUS_NP.gmIdentity` + `gmPresent` → the committed GM pair.
  `gmPresent = false` (we are GM / nobody elected) is a distinct state
  the lease writer handles explicitly.
- `PORT_DATA_SET.peerMeanPathDelay` → `GPTP_PDELAY 0x6E4`.
- The commit is **LO-then-HI with an atomic latch** in `milan_csr` so no
  consumer ever samples a half-old/half-new identity — an identity no
  grandmaster ever had (the pre-0x001D class of bug).

**Failure mode measured 08-07: the lease chain breaks silently if ptp4l
is restarted by hand** — statd's UDS conversation dies with the old
instance and the CSR pair goes stale (it kept reporting the switch while
ptp4l had self-claimed). The lease design makes this fail SAFE for
timestamps (Section 4: tu returns to 1 when the lease lapses) but fail STALE
for identity readouts. Restarting statd re-acquires. The rootfs rebuild
(task #7) owns making the boot chain resilient to this.

## 4. The honesty layer — tu, the timestamp-uncertain bit

Milan 4.3.5.2 makes `tu` the *only* conformant lever while streaming
(5.3.7.3 forbids stopping the stream; 1722-2016 7.5 forbids `tv = 0` on
AAF). Two independent mechanisms drive it:

1. **Fabric holdover** (`KL_ptp_clock_validity`): a GM-identity change
   or PHC step arms `tu = 1` for 0.25–0.5 s **with no software
   involvement** (Milan Annex B.1.1). This covers the cliff itself.
2. **The selected owner**: the default fabric arm uses the engine's live sync
   flag and has no lease; the explicit software arm uses `CLKV_CTRL 0x778`.
   In that legacy arm statd (reference:
   `gptp2csr.sh`) grants the `tu = 0` claim only while ptp4l reports
   SLAVE with |offset| < 1 µs for **3 consecutive polls**, and the claim
   auto-expires (lease ≥ 8 s, sized to 2 measured loop iterations + 4 s)
   if the writer dies. Reset state is `tu = 1`: *unknown clock state
   means NOT valid.*

Measured chain on 08-07: lease lapsed (hand-restarted ptp4l) →
`CLKV_TUCNT` climbing ~1/s (every interval carried tu=1 frames) → the
peer device **correctly refused to lock** on our stream. After the
statd/ptp4l repair and 3 clean polls: claim bit set (`CLKV_CTRL[0]`),
TUCNT frozen, peer locked. A listener that ignores tu would "work"
through this window and present garbage time — the refusal is the spec
working on both ends.

## 5. The announcement layer — ADP, counters, pushes

- **ADP**: the advertiser self-detects the committed GM pair changing
  and emits an out-of-cycle ADPDU carrying the new
  `gptp_grandmaster_id` (Milan 5.6.3.5.7 / IEEE Figure 6-5 UPDATE GM).
- **Counters**: `GPTP_GM_CHANGED` increments on the AVB_INTERFACE
  (measured: 6 changes across the churn night). LINK_UP/DOWN share the
  edge machinery.
- **Unsolicited pushes** (Table 5.22, the 0x0024/0x0028 event law): the
  VERSION `0x002B` implementation armed AVB_INTERFACE `GET_COUNTERS` and
  `GET_AS_PATH` pushes. That producer was deleted during the control-plane
  replacement and has not been restored in the current root.

## 6. The media layer — where the minutes used to go

The pre-0x002A/0x002B behavior, fully root-caused:

- Nothing in the media path consumed the GM change. The playback FIFO's
  convergence observer (`KL_i2s_playback`, fill within MID±64 for
  100 ms) walked back into its band at the residual rate error —
  **133 s at 10 ppm**, the measured "~2 minutes to lock".
- The media-lock gate coupled the render stream's MEDIA_LOCKED to that
  observer, so the whole walk was spent "unlocked", flapping every
  controller's view.

The as-built mechanism (`0x002A` + `0x002B`):

1. **Recenter** (`0x002A`): `milan_datapath` edge-detects the committed
   GM pair (first lease out of reset exempt) and pulses
   `KL_i2s_playback.recenter_p_i`: the read pointer snaps to
   `wptr − MID` **that cycle** (fill = MID exactly; proven 212→256 in
   the unit sim), `media_reset_p_o` pulses honestly (one audible
   discontinuity instead of two silent minutes), and convergence
   re-confirms in its normal 100 ms.
2. **Free-wheel** (`0x002B`, Milan 4.4.2.3 + 1722-2016 E.2.1 + Milan
   5.3.8.10): MEDIA_LOCKED is the stream-vs-timebase capability
   predicate — an accepted in-format PDU locks, for every clock source,
   and convergence loss / GM change / clock-source churn **never
   unlocks a flowing stream**. Unlock remains for genuine loss only:
   100 ms of silence or a bind wipe. The servo's state lives on
   CLOCK_DOMAIN.LOCKED; the FIFO's excursions live in its own counters.
3. **SRP is untouched by design**: Listener Ready is a pure function of
   settled-state + a matching Talker Advertise (Milan 5.3.8.5 — no lock
   term; the 5.5.3.3 event list has no lock event), so reservations and
   licences ride through the hand-off. The talker keeps streaming
   (5.3.7.3), stamping tu per Section 4.

## 7. The recovery timeline, end to end (fabric default)

```
T+0      selected master's Announce stops
T+timeout engine announce-receipt timeout -> BMCA runs; sync flag clears
          tu=1 immediately; published GM/parent change atomically
T+X       real GM returns -> engine selects it and servo reacquires
T+X+step  engine applies PHC step; Annex B holdover keeps tu=1 >=0.25 s
T+lock    engine publishes sync_ok; after holdover tu=0 with no daemon lease
```

Desk tests prove the ownership and holdover sequence. Exact timeout/lock bounds
and the final `tu=0` board observation are #117 evidence, not a desk claim.

## 8. Traps on record (all hit live, all in memory)

| Trap | Consequence | Cure |
|---|---|---|
| Hand-restarting ptp4l mid-session | statd lease chain stale → tu stuck 1 → peers refuse lock | restart statd too; long-term: boot-chain resilience (#7) |
| Long self-GM era + existing ptp4l | slew, not step: ~40 min for 60 s | one ptp4l restart; long-term: the DLL (#22) |
| rootfs ships priority1 238 | board WINS elections after any reboot | live fix each boot until the #7 rootfs carries 250 |
| Reading GM from the CSR alone | stale identity when the lease chain broke | `pmc GET TIME_STATUS_NP` is the ground truth |
| Judging lock from the old law | GM change looked like stream failure | 0x002B: lock free-wheels; check TUCNT and the counters instead |
