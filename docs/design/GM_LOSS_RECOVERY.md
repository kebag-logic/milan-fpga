<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->

# Grandmaster loss and recovery — one fabric-owned mechanism

Status: product architecture at VERSION `0x0002_0056` (2026-08-30).
This page describes the fabric-gPTP product build and its ownerless
verification-only option-OFF elaboration. Booted-board and two-board acceptance
remain owned by #117; this document does not turn simulation into that
physical evidence.

Companion to [TIME_SYNC.md](TIME_SYNC.md) for steady state and
[GPTP_PLANE.md](GPTP_PLANE.md) for the integration seams.

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `crf.media-clock-consumption` | `missing` | - |
| `gptp.fabric-product-owner` | `implemented` | - |
| `notifications.change-events` | `implemented` | - |
<!-- milan-feature-status:end -->

## Contents

- **[1. The active owner](#1-the-active-owner)** — The product-default `gptp-processor` owns the wire protocol, PHC actuator and one atomic public-state bank; recovery needs no parallel CSR mirror
- **[2. Detecting loss and change](#2-detecting-loss-and-change)** — How Announce/Sync receipt expiry, BTCA and Pdelay qualification distinguish GM identity, synchronization and asCapable, including the valid “GM known but unsynchronized” state
- **[3. Publication and tu ordering](#3-publication-and-tu-ordering)** — The commit boundary that prevents torn GM/parent/pdelay reads and asserts `tu` on the discontinuity edge before any frame can leak the old-health verdict
- **[4. Public recovery surface](#4-public-recovery-surface)** — The selected-owner mapping into legacy CSRs, GET_AVB_INFO, GET_AS_PATH and AAF/CRF `tu`, with coherent multiword snapshots and ineffective software writes in fabric mode
- **[5. End-to-end timeline](#5-end-to-end-timeline)** — The ordered loss-to-recovery sequence from receipt timeout through atomic publication, Annex B holdover and restored servo lock
- **[6. Media and notification behavior](#6-media-and-notification-behavior)** — What continues during a time transition, what remains pinned to the internal media clock, and how selected-owner changes feed the complete Table 5.22 scheduler
- **[7. Verification-only option-off elaboration](#7-verification-only-option-off-elaboration)** — The option-OFF proof target is deliberately ownerless: its publication outputs are zero, `tu` is asserted, and legacy writes are inert.

## 1. The active owner

The product-default datapath elaborates `KL_gptp_shadow` and the pinned
`gptp-processor`. That one plane:

- receives and transmits Announce, Sync, Follow_Up and Pdelay messages;
- runs BTCA, receipt timers, peer-delay qualification and the PHC servo;
- applies adjfine and adjtime to the fabric timestamp counter; and
- commits GM, parent, flags, peer delay, offset, announce quality and the
  bounded selected PathTrace as one outward publication bank.

The fabric plane directly steers the PHC and atomically publishes GM/path/CLKV
state. Link recovery only resets and requalifies the physical boundary; it does
not participate in time selection or publication. One owner therefore covers
the wire protocol, clock actuator and public state.

## 2. Detecting loss and change

There is no "GM lost" PDU. The engine infers it from the 802.1AS receipt
state machines:

1. Announce silence expires the announce receipt timer and BTCA chooses from
   the remaining qualified candidates. A device may correctly select itself
   when no better candidate remains.
2. Sync/Follow_Up loss clears the published synchronized flag even if the last
   GM identity is still known.
3. Pdelay qualification directly drives the published asCapable level and
   peer delay in the engine's atomic publication bank.
4. A different selected vector changes the published GM, parent and complete
   PathTrace at one engine commit boundary.

The engine can transition through "GM known but not synchronized". That is a
first-class public state: identity/path may be useful for topology while AVTP
timestamps remain uncertain.

## 3. Publication and `tu` ordering

The donor engine updates individual raw words while handling an event and
pulses `pub_commit` only when the transaction is complete.
`KL_gptp_shadow` copies the scalar fields plus canonical PathTrace count/tail
into its outward bank on that pulse, so a consumer cannot observe a new GM
paired with an old parent, pdelay, flag word or path epoch.

One edge needs stronger ordering. A GM change or a synchronized-to-unsynchronized
transition is detected combinationally from the raw commit and emitted as
`pub_disc`. `KL_ptp_clock_validity` includes that live pulse in `tu`, before
its registered hold timer or the new outward bank is visible. Therefore an
AVTP frame launched on the commit edge is already stamped `tu=1`; there is no
one-frame old-health leak.

The same validity block arms holdover for:

- a fabric publication discontinuity;
- a PHC `settime` step; or
- a PHC `adjtime` step.

Holdover lasts at least Milan Annex B.1.1's 0.25 s, independent of the event's
phase against the quarter-second tick. Outside holdover:

```text
tu = !fabric_sync_ok
```

`asCapable` is published separately; GET_AVB_INFO consumes the engine level,
not a peer-delay-is-nonzero proxy.

## 4. Public recovery surface

Every public consumer selects the same compile-time owner:

| Consumer | Fabric-default value |
|---|---|
| `ADP_GM_LO/HI` `0x624/0x628` | committed GM identity |
| `GPTP_PDELAY` `0x6E4` | committed peer mean path delay in ns |
| `AS2_LO/HI` `0x730/0x734` | committed parent identity |
| `CLKV_STAT` `0x77C` | live `tu`, sync, holdover and asCapable; lease fields are structural zero |
| AAF and CRF talkers | the same live `tu` verdict |
| GET_AVB_INFO | snapshotted GM, pdelay and asCapable with the other response fields |
| GET_AS_PATH | zero entries without a GM or when the selected Announce has no PathTrace TLV; otherwise that TLV's sequence, bounded to the GM plus seven tail identities |

GM and parent each occupy two 32-bit CSR addresses. On the first half read,
the CSR block snapshots the full live 64-bit value and holds it through the
complementary half. LO→HI and HI→LO are both coherent, including when a
publication commit lands between transactions. GET_AVB_INFO and GET_AS_PATH
likewise snapshot all gPTP fields at selector zero and hold them through the
multi-word response.

Legacy writes still receive AXI acknowledgements for address-map compatibility,
but they cannot change these live faces or grant clock health in either
elaboration.

## 5. End-to-end timeline

```text
T+0        Announce or Sync delivery stops
T+timeout  engine receipt state expires; BTCA/sync state changes
same edge  pub_disc=1, AVTP tu=1, complete raw bank commits atomically
next edge  CSR/protocol consumers see the new committed bank
holdover   tu remains 1 for at least 0.25 s
recovery   qualified master + Sync/Follow_Up restore servo lock
commit     fabric_sync_ok=1; tu clears only after holdover has elapsed
```

If the recovered epoch requires an engine PHC step, that step independently
re-arms holdover. No service restart or lease reacquisition is part of the
default path.

## 6. Media and notification behavior

The talker keeps streaming through a time transition as Milan requires, using
`tu` to mark uncertain presentation timestamps. Listener reservations are not
torn down merely because the time source changes.

The current root still pins media-clock selection to INTERNAL. The historical
playback recenter/free-wheel mechanism remains separate from gPTP ownership:
a committed GM change may recenter the elasticity FIFO, while genuine stream
silence or bind loss remains the unlock cause. CRF media-clock consumption is
still missing, as the feature row above states.

The protocol processor consumes the same selected-owner values for solicited
GET_AVB_INFO/GET_AS_PATH responses and Table 5.22 pushes. The root compares the
complete served snapshots: GM/pdelay/domain/asCapable changes drive AVB_INFO,
while AS_PATH compares `(count ? GM : 0, count, active tails)`. Fabric count
zero is the selected no-TLV empty sequence, not a synthetic GM-only path:
0 <-> 1 drives AS_PATH, but GM A->B while both counts are zero does not. The
scalar identity edge still drives AVB_INFO and GPTP_GM_CHANGED. The shared
scheduler sends the resulting unsolicited response to every other registered
controller; the timed integration leg also grades controller probing and
removal.

## 7. Verification-only option-off elaboration

`fabric_gptp: false` is refused for every product configuration. The form
survives only as a direct, verification-only elaboration and has no image or
runtime owner behind it.

The retained addresses are inert compatibility surfaces. GM, parent, path and
peer-delay publications read as zero; sync and asCapable read as zero; `tu`
reads as one. Writes are acknowledged but cannot create a publication, renew a
lease, clear `tu`, or assert clock health. The option-OFF tests explicitly try
those writes and prove that the ownerless verdict does not change.
