<!--
SPDX-FileCopyrightText: 2026 Kebag Logic
SPDX-License-Identifier: CERN-OHL-W-2.0
-->

# Three wire-truth defect classes (2026-08-02)

Written 2026-08-02. One day on the bench produced three closed findings that
share a shape: **an instrument or a policy that reported what it was designed
to report, while the thing it described was something else.** Each section is
a symptom → measurement chain → root cause → fix → verification record; the
general lesson sits at the end of each. Repos: `milan-fpga` (fabric + desk
harness) and `milan-tests-avb` (board software + bench runner). The campaign
context is the [historical torture campaign](../testing/TORTURE_CAMPAIGN.md); the bench
itself is [BENCH_TOPOLOGY.md](BENCH_TOPOLOGY.md).

## Contents

- **[1. PROMISC voids the shield](#1-promisc-voids-the-shield)** — S50milan's own `promisc on` outranked the TCAM stream-drop the same script installs, so the RX shield never shielded anything on any build; the measured chain runs from an 8 kf/s AAF flood through single-hart starvation to the peer gating audio at ~30% duty, and the fix is a driver-side MC_HASH+TCAM shield plus a sysfs-gated promisc.
- **[2. control_data_length counted the id field](#2-control_data_length-counted-the-id-field)** — every raw AECP/ACMP builder over-declared `control_data_length` by the 8-octet id field for years; Ethernet's 60-byte minimum padding absorbed the lie until a declared-vs-delivered validator started silently dropping the big payloads, which looked exactly like a fabric wedge.
- **[3. Peer counters are measured parties](#3-peer-counters-are-measured-parties)** — the reference device's FRAMES counters tick per-frame where Milan Table 5.6 mandates per-interval, and the harness used to smear such pair disagreements over both sides; verdicts now attribute the deviation to the side that earned it, and the reset-on-bind check learned which transitions owe a reset at all.

## 1. PROMISC voids the shield

**Symptom.** USER reported "gPTP packets are not sent on time" during peer-device
loop testing — and was right, although every frame-*count* instrument on the
box read clean. Downstream, the peer rendered our stream in ~370 ms bursts at
roughly 30% duty, its `EARLY_TIMESTAMP` counter climbing at +5,635/s, and loop
THD+N stalled at −68 dB (gating-limited, not converter-limited). ssh to the
board intermittently took 30–150 s to complete a key exchange.

**Root cause, RTL half (by design, not a bug).**
[`hdl/ieee8021q/filtering/rx_mac_filter.sv`](../../hdl/ieee8021q/filtering/rx_mac_filter.sv) decides SOF pass/drop in strict
precedence **runt → PROMISC → TCAM hit → address filter**, and its own comment
says the ordering is deliberate: promiscuous means "hand me the wire", so it
outranks an explicit TCAM *drop* entry, which is filtering policy.

**Root cause, software half (the actual defect).** `S50milan` set
`ip link set eth0 promisc on` at boot (the 07-24 workaround for ptp4l seeing
zero PDUs) — and *the same script*, a few lines later, installed a TCAM
stream-DMAC drop. The first line voided the second **on every build that ever
shipped**. Nobody noticed because the failure mode is not an error; it is just
traffic arriving. The measured chain on the 08-02 peer loop: the ~8 kf/s
return-leg AAF flood reached the single-hart RV32 kernel → servo shells
starved → our talker presentation timestamps ran EARLY → the peer discarded
~70% of frames and gated its render.

**Refuted along the way:** "the filter is not in the bitstream". It is. The
LiteX top-level `.v` instantiates `milan_datapath` as a **black box**, so
grepping it for `rx_mac_filter`/`tcam` returns zero hits and proves nothing —
the build's `.tcl` source list carries the file, and nothing overrides
`RXFILT_P` (default 1) on the instantiation.

**The sharpest numbers** (tap A/B on the board link, 60 s windows, identical
method; `logSyncInterval` is −3, so 125 ms is the mandated cadence):

| condition | Sync inter-departure | Syncs/s | kernel RX |
|---|---|---|---|
| BEFORE, streams running | median 398 ms, **max 3001 ms** | 2.6 | ~8,000 pps |
| streams torn down (baseline) | median 100 ms, max 200 ms | 7.8 | — |
| AFTER (shield), both legs streaming | median 101 ms, max 200 ms | 7.8 | ~10 pps |

After the fix the loaded cadence is *identical to idle* — the defect is gone,
not reduced. Announce is back at 1000 ms. The fabric keeps receiving the
stream (PCM RX counters advance) while the kernel sees only control traffic:
the fabric taps sit PRE-filter, only the kernel DMA is post-filter, which is
exactly the shield design.

**The fix** (both halves needed, `milan-tests-avb`):

- `7b6f8b6` — kl-eth: MC_HASH programmed from the kernel multicast list (the
  RTL's 6-bit XOR fold), address filter armed at open, TCAM index-15 drop of
  the stream MAAP range `91:E0:F0:00:xx:xx`, `rx_shield=0` escape parameter,
  `MODULE_VERSION` `rxsh1-<xlen>`. The hash alone is NOT enough: ~3.1% of
  MAAP DMACs collide into an already-set control bucket, so the TCAM drop
  entry is load-bearing.
- `ae3df43` — S50milan: promisc is set ONLY when the driver lacks the shield.
- `c1ee98c` — the version gate first read `modinfo -F version`, and **busybox
  has no `modinfo`**, so the check silently took the else-branch and re-armed
  promisc over a shielded driver (cost one flash cycle). It now reads
  `/sys/module/kl_eth/version`.

Runtime promisc is still honoured (tcpdump on the board works); the posture
check is `cat /sys/class/net/eth0/flags` — **0x1203 correct**
(UP|BROADCAST|ALLMULTI|MULTICAST), **0x1303 = promisc leaked**.

**Lessons.** (a) A frame **count is not a cadence**: "229 gPTP frames in 10 s"
looked like full rate while one Sync in three was being sent — bunched sends
average out. Measure the **inter-departure distribution** (median/p95/max),
and measure it **at the tap**: the controller host sits on a pruned switch
port and cannot see the stream or link-local gPTP at all. (b) A protection
you installed is not a protection until you have observed it *dropping
something* — this one had never dropped a frame on any board, ever.

## 2. control_data_length counted the id field

**Symptom.** With the new `x32p_aslm` gateware on the board,
`ADD_AUDIO_MAPPINGS` (and other large-payload AECP commands) from the bench
tools went unanswered — no error, no counter, nothing. It looked exactly like
a fabric wedge in the new AECP directory logic.

**Root cause.** Every raw AECP/ACMP frame builder in the bench tooling
computed `control_data_length` as the length of everything after the common
header — *including* the 8-octet id field. 1722.1-2021 defines it as the
number of octets **following** that field: **9.2.2.6** (AECP — octets after
`target_entity_id`) and **8.2.1.6** (ACMP — octets after `stream_id`; 44 for
the Milan-shaped ACMPDU). Every command was over-declared by 8 octets, for
years.

**Why it was invisible.** Ethernet pads every frame to 60 bytes, so for small
GETs the wire always *delivered* at least what the over-declaration promised —
the padding covered the lie. The new gateware's declared-vs-delivered length
validator (first shipped in `x32p_aslm`) drops any frame whose declared
payload outgrows the delivered slack, **silently** — and the first commands
big enough to outgrow it were `ADD/REMOVE_AUDIO_MAPPINGS`. The ACMP
over-declaration was tolerated by both bench endpoints; it is fixed for
honesty, not symptom. (The fabric-side companion rule, from 1722-2016
4.4.5.4: `control_data_length` covers the control_data *payload* only.)

**The fix.** `milan-fpga` `b5c9f984` (hive tools) and `milan-tests-avb`
`bd37631` (`avdecc_l2.py`): both builders now subtract the id field. The ADP
discover path had always used the correct `cdl=56` — the defect lived only in
the hand-rolled AECP/ACMP builders.

**Lessons.** (a) **A tolerated over-declaration is a latent defect**: the wire
accepting a wrong length for years is not evidence the length was right. (b)
When a *new* validator lands, its first victims are usually **old lies** —
before suspecting the fresh RTL, re-derive the tool's octet arithmetic from
the standard's field definitions. (c) Validate frames by LENGTH against the
declaration, both directions — the same rule the repo already applies to AAF
(`42 + 24·C`).

## 3. Peer counters are measured parties

**Symptom.** Campaign `ax-rv32-e` filed dozens of cross-side counter FAILs
against the DUT that dissolve on inspection: the reference peer's
listener/talker `FRAMES_RX`/`FRAMES_TX` counters advance **per frame**
(~8,000/s for a class A stream) where Milan Table 5.4/5.6 defines them as
**per observation interval** (≤ 1/s shapes). A generic pair-FAIL then smeared
both sides — including the side that was conformant.

**The attribution fix.** `milan-fpga` `cc1057ec` (harness + plan) and
`milan-tests-avb` `3576806` (runner): when exactly one side of a pair ticks at
wire frame rate (beyond `max(600, 150/s × window)` — no ≤ 1 s interval can
tick that much), the pair verdict **PASSes for the conformant side by name**
and the deviation moves to its own finding class,
`xside.peer-counter-semantics`, attributed to the deviant side. `ax-rv32-e`
had smeared 37 pairs that way. A verdict must name the party it measured — a
reference device is a *measured party*, not an oracle.

**The reset-on-bind triage, same round.** Milan 5.3.8.10 resets the Stream
Input counters **only on the not-bound → bound transition**; 5.5.3.5.43
handles a BIND_RX at an already-bound input by updating binding parameters
**without transiting UNBOUND** — so an implicit rebind owes no reset, and the
trigger is the state transition, never the BIND_RX message itself. And a
counter observed at a small value just after a bind (`MEDIA_LOCKED [1,1]`,
i.e. reset → 0 → re-lock) is **proof OF the reset, not of its absence** —
event counters may legitimately re-tick to ≤ 8, interval/tally counters to
≤ 64, inside the observation window. Before these distinctions the campaign
had filed **31 conformant binds** (26 re-lock shapes + 5 rebinds/leftovers) as
SHALL violations. The full verdict/excuse tables live in
[historical torture campaign](../testing/TORTURE_CAMPAIGN.md).

**Lessons.** (a) **Attribute, never smear**: a two-party check that FAILs the
pair manufactures a defect record against the conformant side, and those
records poison every later triage. (b) **A reset check must know the FROM
state** — a check that cannot distinguish bound → bound from not-bound →
bound is testing its own bookkeeping, not the clause. (c) Read the clause for
the *trigger* (a transition) rather than the *message* (BIND_RX): the same
message is owed different behaviour in different states.
