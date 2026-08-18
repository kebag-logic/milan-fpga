<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->

# D7 reproduced: the grandmaster is lost under RX load, because bulk RX and gPTP share one ring

**Date:** 2026-07-28 **Gateware:** `0x0001_0016` on **both** boards (R7 —
read from `0x90000004` on each before any comparative run)
**Level / oracle:** L5 (the wire, on hardware). The oracle is not our own CSR
mirror: it is `ptp4l`'s own BMCA state and per-message-type counters
(`pmc GET PORT_STATS_NP` / `TIME_STATUS_NP` / `PARENT_DATA_SET`) read on three
independent stacks — the ALINX, the Arty and the peer host — plus the peer's
independent re-election of a *third-party* device as grandmaster.

---

## Contents

- **[1. The report, and what it turned out to be](#1-the-report-and-what-it-turned-out-to-be)** -- Filed as "the GM loses the election under egress load"; measured as nothing of the kind. The symptom decomposes into our own transmitter going silent, and the peers' takeover is the CONFORMANT half of the story.
- **[2. Root cause](#2-root-cause)** -- `rx_queues: 1` means no steer block exists, so gPTP shares the bulk RX ring with the flood; ptp4l starves, our Announce stops, and a conformant BMCA (802.1AS 10.3) deposes a silent claimant. Not egress, not CBS -- do not chase those.
- **[3. The evidence, five runs, with a negative control and a same-board A/B](#3-the-evidence-five-runs-with-a-negative-control-and-a-same-board-ab)** -- Reproduced 2/2 under a 950M UDP flood, absent 2/2 without it, and the same board with 2 queues rides the identical flood out -- the A/B that pins the queue count as the variable.
- **[4. Hardware acceptance procedure](#4-hardware-acceptance-procedure)** -- The exact iperf3/ptp4l/pmc commands, the registers to read before and after, and what a PASS looks like on the reflashed 2-queue build.
- **[5. What the fix is, and what it is not](#5-what-the-fix-is-and-what-it-is-not)** -- `rx_queues: 2` with the boot chain re-pinned (+0x74 on every window from dma-ts). It is reflash-gated by design; no runtime poke exists, and priority tweaks that "help" are the forced-win anti-pattern the GM-recovery directive forbids.
- **[6. Tests added](#6-tests-added)** -- The builder gates that refuse a queue flip under a pinned boot chain, and the bench step that runs the flood against the new build (8.3 ladder item 8).
- **[7. Defects found outside this lane's scope — NOT fixed here](#7-defects-found-outside-this-lanes-scope--not-fixed-here)** -- Recorded per methodology Section 5 for their own lanes, with the evidence that made each real.

## 1. The report, and what it turned out to be

USER: *"when the device receive packet, the gPTP GM changed for no reason."*
Recorded as open defect **D7** (*"as soon as the DS20 receives packets the gPTP
is discarded"*), **not reproduced** on a 25 s sample.

It reproduces on demand. **Trigger: a saturating unicast RX flood aimed at the
grandmaster board.** 58 Mb/s of TCP does nothing; ~935 Mb/s of UDP takes the
grandmaster out of the domain within seconds.

**The grandmaster change is not the defect.** Deposing a master that has
stopped announcing is exactly what IEEE 802.1AS-2020 requires — the
`PortAnnounceInformation` state machine expires the master after
`announceReceiptTimeout` × `announceInterval` (3 × 1 s = 3 s) and re-runs the
BMCA (Clause 10.3; intervals Clause 10.6). `ptp4l` names the transition in its
own log: `ANNOUNCE_RECEIPT_TIMEOUT_EXPIRES`. **The defect is upstream of the
BMCA: our grandmaster stops transmitting.** So "for no reason" is precise —
from the network's point of view the grandmaster simply vanished.

## 2. Root cause

[`configs/endstation_ax7101_8x8.yaml`](../../configs/endstation_ax7101_8x8.yaml) ships **`rx_queues: 1`**, and its own
comment already says what that means:

> *"with 1 there is no steer block at all, so gPTP shares the bulk ring and the
> USER's 2-ingress-queue directive is simply not implemented on this build."*

With one ring there is one NAPI context and one softcore. A line-rate RX flood
consumes it entirely; userspace never runs; `ptp4l` transmits nothing. Observed
directly on the flooded board:

```
kl-eth 90000000.ethernet eth0: poll hb: n=954368 q0_on=1 q1_on=0 rd0=880 rd1=0
kl-eth 90000000.ethernet eth0: bd-stage ns/frame: build 38780 meta 5733 gro 181849
```

`q1_on=0` — no second queue exists on the flashed build. `gro 181849` ns/frame
is the poll loop eating the core. `ssh` to the board died at the same time
(`Connection timed out during banner exchange`), which is the same starvation
seen from another angle: this is CPU starvation of userspace, not fabric queue
starvation.

**Chain:** `rx_queues: 1` → no `RxSteer` → bulk RX and gPTP share one ring and
one NAPI → saturating RX monopolises the softcore → `ptp4l` is not scheduled →
Announce/Sync transmission stops → peers hit `announceReceiptTimeout` → BMCA
re-elects (conformant) → **the grandmaster changed.**

## 3. The evidence, five runs, with a negative control and a same-board A/B

Segment: ALINX `020000fffe000001` (priority1 **238**, grandmaster), Arty
`020000fffe000002` (`clientOnly`, priority1 248), peer host
`6805cafffe95b2d1`, reference device `3cc0c6fffefe0210` (priority1 **246**).
All counts are `pmc PORT_STATS_NP` deltas across the stated wall-clock window;
the load occupies 60 s inside each window.

| run | target | load | window | result |
|---|---|---|---|---|
| **E1** | ALINX (`rx_queues 1`) | 58 Mb/s TCP | 93.27 s | **no effect.** Announce 105 (1.13/s), Sync 823 (8.8/s), Pdelay 105. GM held, 0 BMCA events. |
| **E2** | ALINX (`rx_queues 1`) | **935 Mb/s UDP** | 183.51 s | **GM LOST.** Announce 116 where 183 were due; Sync 917 where 1468 were due. The 60 s flood contributed ~zero. Peer re-elected `3cc0c6fffefe0210` (prio1 246); the Arty's GM CSR followed (`0x624/0x628` → `3CC0C6FF_FEFE0210`); Arty `master_offset` blew out to **724,785,319 ns**. Recovered automatically when the flood stopped. |
| **E3** | Arty (`rx_queues 2`) | **935 Mb/s UDP** | 97.58 s | **NEGATIVE CONTROL — holds.** Announce 97 (0.994/s), Sync 775 (7.94/s), Pdelay 98 (1.00/s). GM never moved, `ssh` stayed responsive, board still passed 4 Mb/s to userspace. |
| **E4** | Arty, **steer bypassed** | **931 Mb/s UDP** | 98.06 s | **SAME-BOARD CAUSALITY.** `RxSteer.hash_sel := 1` (`0xF0003094`) forces every frame to q0 — the 1-queue topology, one bit, same silicon, same flood. Announce **0.41/s** (59 % lost), Sync **3.06/s** (62 % lost), Pdelay_Resp **0.45/s**. Restored to 0 afterwards. |
| **E5** | ALINX (`rx_queues 1`) | **936 Mb/s UDP** | 98.00 s | **REPEAT OF E2 — identical.** Peer `gmIdentity` → `3cc0c6.fffe.fe0210` (prio1 246); Arty GM CSR → `0xFEFE0210 / 0x3CC0C6FF`; Arty `master_offset` → **677,654,114 ns**; ALINX `ssh` timed out. **2/2 on the trigger.** |

**Determinism: 2 for 2** on the stated trigger (E2, E5), with two independent
negatives — E1 (same board, ordinary traffic) and E3 (same flood, 2-queue
board). The effect is bounded exactly by the 60 s load window in both runs and
every sample carries a wall clock, so it is not a coincidence of an
unrelated event.

**Recovery is automatic** (USER rule D9 — never force the GM to stabilise a
measurement). 41 s after the flood ended the whole segment was back on
`020000.fffe.000001` with no operator action, on both E2 and E5. Note however
that the Arty then takes a further ~60 s to close its offset (measured
677 ms → 160 ms → 0), because its `ptp4l` is `clientOnly` with no
`step_threshold` and can only slew at the ±1 % rail — **that is D8, a bench
config defect, and it lengthens the audible consequence of every flap.**

E3 vs E4 is the load-bearing comparison: **one register bit on one board turns
a perfectly held gPTP cadence into a 60 %-loss cadence under an identical
flood.** E1 vs E2 shows the effect is a threshold, not a gradient — ordinary
traffic is harmless.

**Honest limit of E4:** at 59 % Announce loss the Arty did *not* lose the
grandmaster in 60 s. Losing 59 % of announces scattered is not the same as one
contiguous 3 s gap; the ALINX lost ~100 % (total silence) and did flip. E4
proves the *mechanism* (steering is what protects gPTP); E2 proves the
*symptom*.

Steer address validated before use — `q1_frames` (`0xF0003090`) ticks at
exactly **20 frames/s** on an idle segment, which is the gPTP message rate
(8 Sync + 8 Follow_Up + 1 Announce + 3 Pdelay). A register that counts the
right thing at the right rate is the address; a plausible offset is not.

## 4. Hardware acceptance procedure

Run from the peer host. **Both boards must read `0x00010016` at `0x90000004`
first** — a comparative result across different gateware is not a result.

Copy [`scripts/gptp_probe.sh`](../../scripts/gptp_probe.sh) to the peer first
(no rsync there — `tar cf - scripts/gptp_probe.sh | ssh <peer> 'cd /tmp && tar xf -'`).

```bash
# 1. sampler (peer): pmc on all three stacks + the GM CSRs on both boards
sh /tmp/scripts/gptp_probe.sh PRE

# 2. flood the grandmaster board for 60 s
iperf3 -c <alinx-ip> -u -b 950M -l 1400 -t 70 -f m

# 3. sample again
sh /tmp/scripts/gptp_probe.sh POST
```

**Expected values.**

* **Today (`rx_queues: 1`, the defect):** across a ~180 s window containing the
  flood, ALINX `tx_Announce` delta ≈ **116** against ~183 due, `tx_Sync` ≈
  **917** against ~1468 due; the peer's `gmIdentity` moves to
  `3cc0c6.fffe.fe0210` with `grandmasterPriority1 246`; the Arty's
  `0x90000624/0x90000628` shows `0xFEFE0210 / 0x3CC0C6FF`.
* **Fixed (`rx_queues: 2`):** `tx_Announce` delta within **2** of
  `floor(window / 1 s)`, `tx_Sync` within **2** of `floor(window / 0.125 s)`,
  `gmIdentity` never leaves `020000.fffe.000001` on any of the three stacks,
  and `bmca_events` stays 0 in `/var/log/messages` on both boards.

The tolerance of 2 is not arbitrary: a receipt timeout needs
`announceReceiptTimeout` (3) *consecutive* missing messages, so a shortfall of
≤ 2 in the whole window cannot produce one. That is the sufficient direction
and it is the one the gate uses.

**Same-board rehearsal without a reflash** (proves the fix mechanism on the
Arty, which already has the steer block):

```bash
ssh root@<arty-ip> 'devmem 0xF0003094 32 1'   # bypass  -> expect ~60 % gPTP loss
ssh root@<arty-ip> 'devmem 0xF0003094 32 0'   # restore -> expect nominal cadence
```

Always arm a dead-man restore (`(sleep 200; devmem 0xF0003094 32 0) &`) before
setting the bypass.

## 5. What the fix is, and what it is not

The fix is `rx_queues: 2` on `endstation_ax7101_8x8.yaml` — **reflash-gated**.
The config comment already documents the cost: raising it moves
`boot_chain_pin.dma-ts` and `pcm-dma` by `0x74`, and builder gate 19c refuses
the change until the pin is re-derived against the new `csr.csv`. That is a
build-and-flash round, which this lane did not take (no Vivado build, no
flash).

**It is not a CBS/egress problem.** The arithmetic never supported egress
starvation (2-channel AAF at 8000 fps is ~5.8 Mb/s; eight streams is a small
slice of a gigabit) and the measurement agrees: the failure is on the *ingress*
side and shows up as CPU starvation, with `ssh` dying alongside `ptp4l`. Do not
enable CBS to chase this — shaping q0 at reset once paced all best-effort TX to
~250 Mb/s ([`CBS_DEFAULT_SHAPING_BUG.md`](CBS_DEFAULT_SHAPING_BUG.md)).

**A caveat worth carrying into the fix round:** the steer block gives gPTP its
own ring and its own NAPI, which is what E3/E4 measure. It does not by itself
guarantee `ptp4l` — a *userspace* process — gets the CPU under a worse flood.
E3 shows the Arty's userspace kept transmitting Pdelay_Req at exactly 1.00/s
through a 935 Mb/s flood, so the separation is sufficient at line rate on this
hardware; it is not proof that no load can ever starve userspace. Re-run the
acceptance procedure after the reflash rather than assuming.

## 6. Tests added

* [`tests/features/gptp_announce_receipt_timeout.feature`](../../tests/features/gptp_announce_receipt_timeout.feature) (10 scenarios) —
  the BMCA receipt-timeout boundary from **both** sides (a 2 s gap must NOT
  move the master; a 3 s gap must), the measured D7 flap including its
  automatic recovery, and a cadence budget fed the real `PORT_STATS_NP`
  deltas above: one window that holds (E1) and one that breaks (E2), so the
  check has a negative control.
* [`tests/steps/gptp_bmca_steps.py`](../../tests/steps/gptp_bmca_steps.py) — the model and the budget rule.
* [`docs/traceability/ieee8021as.md`](../traceability/ieee8021as.md) row **AS-12**.

## 7. Defects found outside this lane's scope — NOT fixed here

1. **`CLKV_CTRL` lease is never renewed, so every AVTP frame we emit carries
   `tu = 1`.** `CLKV_STAT` (`0x9000077C`) reads `0x00000005` on **both**
   boards = `tu` asserted now, no live lease, sync claim never made.
   `CLKV_TUCNT` (`0x780`) increments at exactly **1.00/s** — tu was set in
   **100 % of one-second observation intervals** since boot (ALINX 5,502
   intervals over 5,502 s of uptime). `CLKV_CTRL` (`0x778`) reads `0x00000080`
   = a wdog of 8 quarter-ticks (2 s) written once, `sync_ok = 0`, and nothing
   renews it. Per `KL_ptp_clock_validity.sv` this is the *honest* reset
   behaviour ("unknown == not valid"), but the consequence is that a
   conformant listener is told our timestamps are untrustworthy on every
   single frame. This is a strong candidate for the *other* reading of D7
   ("as soon as it receives packets the gPTP is discarded" = the far end
   flagging our clock the instant frames arrive) and deserves its own lane:
   **nothing in the boot chain leases `CLKV_CTRL`.** Grep found no writer in
   `/usr/bin`, `/usr/sbin` or `/etc` on either board.
2. **ALINX `rx_dropped` = 117,223 of 145,126 (81 %)** at rest, static across
   idle periods — pre-existing, not load-correlated, and not explained here.
3. **Bench config, already recorded:** ALINX `priority1 238` forces the BMCA
   (D9 — USER: use 248); Arty `ptp4l` is `clientOnly` with no
   `step_threshold` (D8). Neither was changed by this lane, and neither
   affects the result above: the GM change in E2 was a genuine automatic
   re-election *away from* the forced winner and back again.
