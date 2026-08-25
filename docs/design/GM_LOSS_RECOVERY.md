<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->

# Grandmaster loss and recovery — one fabric-owned mechanism

Status: product architecture at VERSION `0x0002_0055` (2026-08-23).
This page describes the default fabric-gPTP build. The older linuxptp
measurements remain useful only for the explicit option-off comparison and
are separated in the final section. Booted-board and two-board acceptance
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

- **[1. The active owner](#1-the-active-owner)** — The product-default `gptp-processor` owns the wire protocol, PHC actuator and one atomic public-state bank; host recovery runs without a gPTP daemon or CSR mirror
- **[2. Detecting loss and change](#2-detecting-loss-and-change)** — How Announce/Sync receipt expiry, BTCA and Pdelay qualification distinguish GM identity, synchronization and asCapable, including the valid “GM known but unsynchronized” state
- **[3. Publication and tu ordering](#3-publication-and-tu-ordering)** — The commit boundary that prevents torn GM/parent/pdelay reads and asserts `tu` on the discontinuity edge before any frame can leak the old-health verdict
- **[4. Public recovery surface](#4-public-recovery-surface)** — The selected-owner mapping into legacy CSRs, GET_AVB_INFO, GET_AS_PATH and AAF/CRF `tu`, with coherent multiword snapshots and ineffective software writes in fabric mode
- **[5. End-to-end timeline](#5-end-to-end-timeline)** — The ordered loss-to-recovery sequence from receipt timeout through atomic publication, Annex B holdover and restored servo lock
- **[6. Media and notification behavior](#6-media-and-notification-behavior)** — What continues during a time transition, what remains pinned to the internal media clock, and how selected-owner changes feed the complete Table 5.22 scheduler
- **[7. Explicit option-off comparison](#7-explicit-option-off-comparison)** — The marked software-owner profile, its staged publication and CLKV lease ABI, and the historical daemon-restart evidence that does not describe product-default recovery

## 1. The active owner

The product-default datapath elaborates `KL_gptp_shadow` and the pinned
`gptp-processor`. That one plane:

- receives and transmits Announce, Sync, Follow_Up and Pdelay messages;
- runs BTCA, receipt timers, peer-delay qualification and the PHC servo;
- applies adjfine and adjtime to the fabric timestamp counter; and
- commits GM, parent, flags, peer delay, offset, announce quality and the
  bounded selected PathTrace as one outward publication bank.

No default-rootfs process steers the PHC or mirrors GM/path/CLKV state. The
host still performs link recovery through `milan-statd --no-gptp --no-path`;
that mode neither opens a ptp4l management socket nor writes publication
CSRs. One owner therefore covers the wire protocol, clock actuator and public
state.

## 2. Detecting loss and change

There is no "GM lost" PDU. The engine infers it from the 802.1AS receipt
state machines:

1. Announce silence expires the announce receipt timer and BTCA chooses from
   the remaining qualified candidates. A device may correctly select itself
   when no better candidate remains.
2. Sync/Follow_Up loss clears the published synchronized flag even if the last
   GM identity is still known.
3. Pdelay qualification drives the published asCapable level and peer delay;
   stale daemon values cannot survive because there is no daemon mirror.
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

The legacy writes still receive AXI acknowledgements for ABI compatibility,
but while the fabric option is on they cannot change these live faces or grant
clock health.

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

## 7. Explicit option-off comparison

`fabric_gptp: false` is a supported diagnostic comparison, not an implicit
fallback. The builder emits `GPTP_PLANE_EN_P=0` and creates
the positive v1 software profile plus `/etc/milan-gptp-software-owner`; only
that profiled image starts `ptp4l-rt`,
`phc2sys`, and full `milan-statd` publication.

In this arm the compatibility ABI remains:

- software stages GM/parent LO and commits on HI;
- `CLKV_CTRL` carries sync, discontinuity and asCapable plus a renewable
  quarter-second lease; and
- lease expiry clears the software claims and returns `tu` to 1.

Historical 2026-08-06/07 measurements belong to this arm: a long self-GM era
could make a running linuxptp servo slew a large phase cliff, and restarting
ptp4l could invalidate statd's management connection until statd restarted.
Those observations explain why the compatibility lease fails safe. They are
not steps in the product-default recovery path, which contains neither daemon.
