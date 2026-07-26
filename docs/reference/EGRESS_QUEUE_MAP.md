# Egress queue map (802.1Q traffic classes)

The end-station's TX datapath owns **six egress queues**, `q0 … q5`, and the
**higher index is the higher priority** — `q5` wins arbitration over `q0`. That
is the 802.1Q convention and it is also the convention the credit-based shaper
needs (see [Why gPTP sits below the shaped classes](#why-gptp-sits-below-the-shaped-classes)).

Single source of truth in the RTL: `ethernet_packet_pkg::network_priority_t`
(the enum value **is** the queue index) and
`ethernet_packet_pkg::priority_encode` (scans from the top index down).
The CSR view is [REGISTER_MAP.md](REGISTER_MAP.md) — `CAP.num_queues`,
`CLS_TC_QUEUE_MAP` (`0x310`) and the per-queue CBS window at `0x400`.

## The map

| Queue | Enum | Purpose | Shaping |
|-------|------|---------|---------|
| **q5** | `SRA_CLASS` | **SR class A** — every AVB stream MSRP reserved, per the reservation domains | **CBS** (802.1Qav) |
| **q4** | `SRB_CLASS` | **SR class B** — not used today; provisioned so an MSRP class-B domain has somewhere to land | **CBS** (802.1Qav) |
| **q3** | `GPTP_CLASS` | 802.1AS / gPTP. Today these frames come from the CPU (the PTP daemon), so this is the CPU's sync lane | strict priority |
| **q2** | `CONTROL_CLASS` | MAAP, MSRP, MVRP, and IEEE 1722.1-2021 ADP / ACMP / AECP | strict priority |
| **q1** | `RESERVED_CLASS` | **spare** — deliberately unused, nothing maps here. It keeps the numbering stable if a class has to be inserted later without renumbering q2…q5 | strict priority |
| **q0** | `BEST_EFFORT` | everything else, to and from the CPU | strict priority — **never CBS**, see below |

## PCP → traffic class → queue

Classification is three programmable tables in series
(`traffic_class_map.sv`, `REQ-CLS-01..04`):

```
eff_pcp = vlan_valid ? frame PCP : CLS_DEFAULT_PCP      (0x304)
regen   = CLS_PRIO_REGEN[eff_pcp]                       (0x30C)
tc      = CLS_PCP_TC_MAP[regen]                         (0x308)
queue   = CLS_TC_QUEUE_MAP[tc]                          (0x310)
```

At reset `CLS_PRIO_REGEN` and `CLS_PCP_TC_MAP` are the identity
(`0x00FAC688`), so **traffic class == PCP**, and `CLS_TC_QUEUE_MAP` resets to
`0x006D2B00` — 3 bits per entry, giving:

| PCP (= TC at reset) | 802.1Q name | Queue |
|---------------------|-------------|-------|
| 0 | BE, best effort | q0 |
| 1 | BK, background | q0 |
| 2 | EE / **SR class B** (802.1Q-2018 Table 34-1 default) | **q4** |
| 3 | CA / **SR class A** (802.1Q-2018 Table 34-1 default; the PCP `KL_aaf_packetizer` and lwSRP actually put on the wire) | **q5** |
| 4 | VI, video | q2 |
| 5 | VO, voice | q2 |
| 6 | IC, internetwork control | q3 |
| 7 | NC, network control | q3 |

Nothing maps to q1 at reset. Software is free to reprogram all three tables;
an entry that names a queue `>= NUMBER_OF_QUEUES` is **clamped to q0** rather
than being handed to the demux, which would silently drop the frame
(`axis_demux.v`: `drop_ctl = drop || select >= M_COUNT`). That clamp only
exists because 6 is not a power of two — with a power-of-two queue count every
value of the field named a real queue.

**gPTP fast path.** EtherType `0x88F7` short-circuits the tables and always
lands on `GPTP_CLASS` (q3), in both PCP and legacy modes, because gPTP frames
are untagged and carry no PCP. With `CLS_CTRL[1]` set (`REQ-CLS-07`) the fast
path additionally demands the reserved destination `01-80-C2-00-00-0E`, so a
spoofed `0x88F7` cannot steal the sync lane.

## CBS reset slopes

`CBS_*_RST` in `milan_csr.sv`, mirroring `ethernet_packet_pkg::IDLE_SLOPE_1G`
and its `calc_hi_credit`/`calc_lo_credit` companions
(`MAX_FRAME_SIZE = 1522`):

| Queue | idleSlope @ 1 Gb/s | share | hiCredit | loCredit |
|-------|--------------------|-------|----------|----------|
| q5 SR class A | 450 Mb/s | 45 % | 684 | −837 |
| q4 SR class B | 150 Mb/s | 15 % | 228 | −1293 |
| q3 gPTP | 50 Mb/s | 5 % | 76 | −1445 |
| q2 control | 50 Mb/s | 5 % | 76 | −1445 |
| q1 spare | 25 Mb/s | 2.5 % | 38 | −1483 |
| q0 best effort | 25 Mb/s | 2.5 % | 38 | −1483 |

Σ = 750 Mb/s = **75 %** of the port rate (`REQ-CBS-03`), and the shaped pair
alone is 600 Mb/s = 60 %, comfortably inside the 802.1Q-2018 §34.3.1 ceiling
that actually constrains SR classes. `IDLE_SLOPE_100M` is the same shares of
100 Mb/s.

**Every queue powers up UNSHAPED** (`CBS_EN_RST = 0b000000`) and that is not an
oversight. Shaping q0 at reset once paced *all* best-effort TX to ~250 Mbit/s on
silicon — see [CBS_DEFAULT_SHAPING_BUG.md](../findings/CBS_DEFAULT_SHAPING_BUG.md).
Software opts a queue in through `CBS_CTRL[0]` once a reservation exists; the
lwSRP engine does it automatically for the queue named in `LWSRP_CTRL[4:2]`
(reset 5) when a reservation is granted.

## Why gPTP sits below the shaped classes

gPTP is at **q3, underneath the CBS-shaped q5 and q4**. Someone will eventually
read that as a bug and "fix" it. It is not a bug, and it is not a preference —
it is a correctness requirement:

* **802.1Q credit-based shaping assumes the shaped queues are the top of the
  strict-priority order.** The credit accounting in 802.1Q-2018 §8.6.8.2 bounds
  the class-A latency by reasoning about how long a shaped queue can be kept
  from transmitting: at most one maximum-length frame from a lower-priority
  queue, plus the queues above it that the standard *knows about*. A strict-
  priority queue placed **above** the shaped classes can preempt a class-A frame
  whose credit is already earned, for an amount of time the credit model does
  not account for. The shaper still runs, but the guarantee it computes is no
  longer the guarantee the network gets. In the USER's words: *"CBS is not
  working with something with higher priority."*
* **gPTP does not need to be on top, because it is not timed by when it
  leaves.** Every event message is hardware-timestamped at the **egress SFD**
  in `ptp_ts_top`, downstream of this arbiter. A queueing delay therefore
  changes *when* the message goes out, not the timestamp it carries — and the
  residence time is exactly what the protocol's correction field exists to
  absorb. What would genuinely hurt gPTP is timestamp *error*, and that is
  unaffected by queue order.
* **The load argument is not close, and it is measured, not asserted.** A Milan
  class-A domain at 48 kHz runs 8000 frames/s per stream; gPTP runs 8–16
  frames/s. `tb/verilator/shaper_core` (FQTSS-4) drives q5 shaped at its 450 Mb/s
  class-A reset slope and permanently backlogged, offers q3 continuously, and
  measures what q3 gets: **9.18 % of the port, worst service gap 368 slots =
  23.55 µs** of 1 Gb/s wire time. 8–16 frames of 64–90 B per second is ~0.2 % of
  a 1 Gb/s port, so q3 is offered **more than 40×** what 802.1AS can consume, and
  the gap is bounded because a credit-shaped q5 *must* yield periodically by
  construction.

Note also that the historical worry here was misdiagnosed: the TX
timestamp timeouts of 2026-07-13 were **not** queue starvation. Silicon was
running the legacy classifier at the time and gPTP already outranked bulk TCP;
the delay lived in the driver's single 256-slot TX descriptor ring, upstream of
the classifier entirely. The fix for that class of problem is a priority TX
ring/doorbell, not a queue promotion.

## FQTSS: what is actually measured

802.1Q-2018 clause 34 ("Forwarding and Queuing Enhancements for Time-Sensitive
Streams") is the layer *above* both the credit arithmetic and the arbiter, and
it is the property this whole ordering argument rests on. It is gated in
`tb/verilator/shaper_core` (and, for the register view software sees, in
`tb/verilator/csr`):

| Check | Clause | Result |
|-------|--------|--------|
| **Bandwidth availability.** Σ idleSlope over the SR classes, and over every queue, at both link rates | §34.3.1 / `REQ-CBS-03` | SR A+B = **600 Mb/s = 60 %** of 1 Gb/s; all six = **750 Mb/s = 75 %** at 1 G and 75 % at 100 M. Class A's slope must also exceed class B's. Read out of `ethernet_packet_pkg` **and** out of the `0x400` CSR window, so the package and the registers cannot drift apart. |
| **The shaped class and best effort share the port.** q5 shaped and permanently backlogged, q0 unshaped and permanently backlogged | §8.6.8.2 | q5 outranks q0 absolutely, so only the credit gate can stop it — and it does: **13.70 / 30.11 / 90.82 %** of the port at idleSlope 100 / 200 / 450 Mb/s, q0 taking the rest. Neither queue is ever starved, and the split is monotone in idleSlope. |
| **Non-vacuity.** Same stimulus with CBS switched off | — | q5 takes **100.00 %**. So the split above *is* the shaper, not the arbiter and not the harness. |
| **gPTP is not starved by a saturating class A** | §8.6.8.2 | 9.18 % of the port, worst gap 23.55 µs — see above. |
| **Admission.** A reservation whose slope would break the ceiling is refused | §34.3.1 | `KL_lwsrp_bw_gate` carries the 750e6 / 75e6 limits in RTL and tears down an over-budget TSpec on a live reservation (`tb/verilator/lwsrp`); the config side is builder gate 18d, which rejects an over-subscribed class-A request before a bitstream exists. |

**The reservation is honoured but over-delivered**, and that is `REQ-CBS-07`, not
a queue-map defect: at the 450 Mb/s class-A reset slope the shaped queue takes
90.8 % of the port where 802.1Qav would give it 45 %. The egress here is not
paced to line rate — the shaper hands 8 B per cycle into a MAC FIFO, so a beat
leaves in 10 ns while 8 B on a 1 Gb/s wire take 64 ns, and the queue accrues
idleSlope during the ~5.4 cycles the wire would still be busy. The debit per
byte is exact; the accrual is not. The suite asserts the accounting model and
**reports** the delta against the standard rather than hiding it. Anyone sizing
a reservation against this gateware must read the delivered share, not the
configured slope.

## Ingress (RX to the CPU): two queues

The RX side splits into **two** queues, and the split is gPTP vs everything
else (`RxSteer` in `sw/litex/milan_soc.py`, present when
`board.constraints.rx_queues >= 2`):

| RX queue | Contents |
|----------|----------|
| **q1** | frames whose DMAC is `01-80-C2-00-00-0E` **and** whose (inner) EtherType is `0x88F7` — the same test `traffic_class_map` applies on egress under `REQ-CLS-07`. One detector, one rule, both directions. |
| **q0** | everything else |

Each queue is its own DMA ring writer, its own interrupt and its own NAPI.
`steer_hash_sel[0] = 1` forces everything to q0 (bypass).

**What this replaced, honestly.** `RxSteer` used to be a TCP 4-tuple flow hash
built for throughput: it split one MTU-1500 RX stream into two flow-consistent
queues so two TCP flows' ACK/receive processing ran on two harts, which is how
the single-NAPI ACK-processing ceiling was broken (measured RX 223 Mbit — see
[RX_PERF_TUNING_MAP.md](../findings/RX_PERF_TUNING_MAP.md)). **That parallel
ACK split is gone.** Bulk RX is single-NAPI again and the RX throughput ceiling
reverts to the one-hart number.

What is bought instead is latency where it matters: PTP event messages no
longer sit behind bulk traffic in a shared ring. RX-side PTP latency is
precisely what once held `asCapable` false — late RX stamps, not a switch fault
([GPTP_RXPAD_ROOTCAUSE.md](../findings/GPTP_RXPAD_ROOTCAUSE.md)). A sync/pdelay
exchange is ~64–90 B at 8–16 frames/s, so the dedicated queue is essentially
never backlogged and its NAPI never competes with a 1500 B burst.

**Per-board `rx_queues`.** The correct value is now **2 on both boards**: with
`rx_queues = 1` there is no steer block at all and PTP shares q0 with bulk, so
the directive is simply not implemented on that build. The Arty config already
carries 2. The AX7101 8x8 config ships **1** because that is the layout its
*flashed* boot chain maps — flipping it moves every DMA window from `dma-ts`
onward by `0x74`, which the builder refuses against a pinned `boot_chain_pin`
(gate 19c). **Raising the AX to 2 is a reflash-gated change**: bump
`rx_queues`, move `boot_chain_pin.dma-ts`/`pcm-dma` to the 2-queue addresses,
rebuild, reflash, and re-pin against the new `csr.csv`.

## Where the fabric bypasses all of this

Only frames the **CPU** sends (`s_axis_tx_*` into `milan_datapath`) traverse the
classifier, the per-queue FIFOs and the CBS arbiter. The fabric engines inject
**after** the shaper, through the `adp_tx_arbiter` chain and the control-lane
IFG gasket:

* the AAF talker (`KL_aaf_packetizer` / `aaf_talker_i2s`) — paced by the lwSRP
  bandwidth gate rather than by CBS;
* ADP, ACMP, AECP, MAAP, the CRF talker, and the lwSRP MSRP/MVRP PDUs.

So the q5/q4/q2 assignments bite for **CPU-originated** traffic today: a
software AVDECC controller or a software MSRP stack lands on q2, gPTP from the
PTP daemon lands on q3, and everything else lands on q0. Moving the fabric
talker inside the shaper is a separate piece of work (the `is_1g` follow-up
noted in `milan_datapath.sv`).
