# Grandmaster loss and recovery — the complete mechanism

Status: as built at VERSION `0x002B` (2026-08-07), with every number below
**measured on the AX7101 bench during the 08-06/08-07 root-causing
session**, not estimated. Companion to
[`TIME_SYNC.md`](TIME_SYNC.md) (the steady-state clock architecture);
this document covers the *transient*: what happens, layer by layer, when
the grandmaster disappears, changes, or comes back.

Current integration note: the measurements below predate the control-plane
replacement. The current root keeps media-clock selection INTERNAL, and the
Table 5.22 notification scheduler and departing-controller monitor are live
since 0x0002_0055. The measured transient numbers below remain historical.

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `crf.media-clock-consumption` | `missing` | - |
| `notifications.change-events` | `implemented` | - |
<!-- milan-feature-status:end -->

## Contents

- **[1. What "GM lost" actually is on the wire](#1-what-gm-lost-actually-is-on-the-wire)** — Loss is inferred from announce silence; a deferring device still self-claims when alone, and the real GM's return is a measured 18-60 s phase cliff, not a smooth re-slave
- **[2. The ptp4l layer — step vs slew, and the one-step budget](#2-the-ptp4l-layer--step-vs-slew-and-the-one-step-budget)** — A fresh instance steps the cliff in seconds; a running one slews at ~26k ppm (40 min for 60 s) — the restart-once operational rule and the DLL that retires it
- **[3. The publication layer — how the fabric learns about it](#3-the-publication-layer--how-the-fabric-learns-about-it)** — The ptp4l -> statd -> CSR lease chain with its atomic GM-pair commit, and the measured fail-stale mode when ptp4l is restarted by hand
- **[4. The honesty layer — tu, the timestamp-uncertain bit](#4-the-honesty-layer--tu-the-timestamp-uncertain-bit)** — Fabric holdover plus the software lease: tu=1 marks the labels untrustworthy through the transient, and peers refusing them is both ends conforming
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
2. **The software lease** (`CLKV_CTRL 0x778`): statd (reference:
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
- **Counters**: the current `GPTP_GM_CHANGED` law increments only when the
  grandmaster identity changes. A domain-only update still re-advertises the
  changed ADPDU, but it is neither a GM counter event nor an AS_PATH change.
  The historical bench measured 6 increments across the churn night;
  LINK_UP/DOWN use their own physical edges.
- **Unsolicited pushes** (Table 5.22, the 0x0024/0x0028 event law): since
  0x0002_0055 the processor sends `GET_AVB_INFO`, `GET_AS_PATH`, and the
  rate-limited AVB_INTERFACE `GET_COUNTERS` notifications driven by those
  separated event facts. The replacement control plane also monitors silent
  registered controllers and deregisters them after the required probe and
  retry sequence.

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

## 7. The recovery timeline, end to end (as built)

```
T+0      switch announces stop
T+~3s    announce timeout -> board self-claims GM (BMCA, correct)
         fabric: tu holdover arms; lease will lapse within <= ~24s -> tu=1
         ADPDU with own GM id; GPTP_GM_CHANGED++; one push burst
T+X      real GM returns -> foreign master seen
T+X+2s   BMCA selects it -> UNCALIBRATED -> SLAVE
T+X+2s   PHC STEPS the cliff (fresh servo; restart ptp4l if it slews)
         media: recenter pulse -> fill=MID, MEDIA_RESET, lock HELD
T+X+~30s ptp4l at ns offset
T+X+~50s statd: 3 clean polls -> tu=0 lease -> peers lock on our frames
```

Everything after `T+X` is seconds. The only minutes-scale path left is
the slew trap in Section 2, and that dies with the DLL.

## 8. Traps on record (all hit live, all in memory)

| Trap | Consequence | Cure |
|---|---|---|
| Hand-restarting ptp4l mid-session | statd lease chain stale → tu stuck 1 → peers refuse lock | restart statd too; long-term: boot-chain resilience (#7) |
| Long self-GM era + existing ptp4l | slew, not step: ~40 min for 60 s | one ptp4l restart; long-term: the DLL (#22) |
| rootfs ships priority1 238 | board WINS elections after any reboot | live fix each boot until the #7 rootfs carries 250 |
| Reading GM from the CSR alone | stale identity when the lease chain broke | `pmc GET TIME_STATUS_NP` is the ground truth |
| Judging lock from the old law | GM change looked like stream failure | 0x002B: lock free-wheels; check TUCNT and the counters instead |
