# Virtual switch research & decision — the AVB-aware wire for the boardless tier

Status: **DESIGN / RESEARCH DECISION (2026-08-01).** Not a validated
implementation. This selects the switch architecture for the T2/T3 virtual wire.
A primary-source citation pass (Opus research task) is deferred; the claims here
are derived from the referenced kernel/P4 docs and the project's own constraints
and are marked where they must still be independently sourced. Companion docs:
[`VIRTUAL_E2E_QEMU.md`](VIRTUAL_E2E_QEMU.md), [`TRUE_E2E_REQUIREMENTS.md`](TRUE_E2E_REQUIREMENTS.md), [`VIRTUAL_E2E_HOWTO.md`](VIRTUAL_E2E_HOWTO.md).

**User directive:** the Ethernet wire attaches directly to a RAW socket; find a
good real-time virtual switch (P4, kernel, or pure userspace) that could satisfy
AVB compliance, to refine for testing later.

## Contents

- **[1. The decision (up front)](#1-the-decision-up-front)** — build deterministic userspace `virtwire` as the primary CI backend, Linux bridge + `tc` as the secondary wall-clock lane, P4 deferred; virtwire stays a behavioral model until independently tested.
- **[2. Why the user's "real-time virtual switch" needs two modes](#2-why-the-users-real-time-virtual-switch-needs-two-modes)** — the 1 MHz sim clock (~1000× under line rate) forces a split: virtual-time mode for CI verdicts, wall-clock mode for realism only.
- **[3. Decision matrix](#3-decision-matrix)** — six candidates (virtwire, bridge+tc, P4/BMv2, OVS, DPDK, ns-3/OMNeT++) scored on AVB semantics, determinism, real-time honesty, integration, and maturity.
- **[4. Raw-socket (AF_PACKET) fidelity boundary — state this always](#4-raw-socket-af_packet-fidelity-boundary--state-this-always)** — what an L2 frame without preamble or trustworthy FCS can and cannot validate, plus the adapter requirements (offloads off, netns, bounded queues).
- **[5. Why not P4 first (and when it earns a place)](#5-why-not-p4-first-and-when-it-earns-a-place)** — BMv2 cannot express CBS credit state or residence time and is not a real-time target; P4 stays an optional later backend.
- **[6. virtwire required behavior (the AVB feature list)](#6-virtwire-required-behavior-the-avb-feature-list)** — the ten-point spec: byte-exact forwarding, explicit reserved-group policy, deterministic events, fault injection, a reference-checked CBS model, counters and evidence output.
- **[7. VirtualWirePort contract (implementation interface)](#7-virtualwireport-contract-implementation-interface)** — the six-call port API and the `SOCK_SEQPACKET` one-atomic-message-per-frame envelope.
- **[8. Phased plan (maps to T2/T3)](#8-phased-plan-maps-to-t2t3)** — T2.0 frame contract/loopback through T2.3 single-node E2E, then the T3 two-node plan with its negative controls.
- **[9. What we must NOT claim](#9-what-we-must-not-claim)** — the honesty rails: no line-rate compliance at sim speed, no transparent-clock claim for `tc`, bridge reserved-group defaults untested, green virtual is never a hardware claim.
- **[10. Primary sources to cite (deferred Opus pass)](#10-primary-sources-to-cite-deferred-opus-pass)** — the citation backlog: no kernel/P4/DPDK claim in §3–§5 is final until its primary doc is linked here.

## 1. The decision (up front)

**Build a deterministic userspace L2 switch ("`virtwire`") as the primary CI
backend. Do not start with P4. Use Linux bridge + `tc` only as a secondary
wall-clock integration lane. Defer P4 to an optional later programmable-forwarding
experiment.**

One interface, two backends:

| backend | role | why |
|---|---|---|
| **`virtwire` (deterministic userspace)** | primary CI / correctness oracle | exact frame preservation, virtual-time scheduler, fault injection, seeded replay, no hidden kernel filtering of reserved groups |
| **Linux bridge + `tc` (mqprio/cbs/taprio)** | secondary wall-clock integration lane | near-real-time realism, kernel queueing, TAP/QEMU integration |
| **P4 / BMv2** | deferred, optional | parsing/match/forwarding only; not real-time; weak temporal model |

The `virtwire` core is an **AVB *behavioral* model, not an AVB-compliant
switch** until its CBS/VLAN/reservation/timing behavior is independently tested.

## 2. Why the user's "real-time virtual switch" needs two modes

"Real-time" is ambiguous against a 1 MHz simulated sys clock (~1000× slower than
Gigabit line rate). The switch needs two explicit modes:

- **Deterministic (virtual-time) mode — the CI verdict lane.** Time advances
  from RTL/guest events, not the host wall clock. Same seed + inputs → identical
  normalized JSONL event sequence and PCAP. This is what "prove the protocol"
  means without a board.
- **Wall-clock mode — the integration lane.** `CLOCK_TAI`/monotonic, CPU
  affinity, optional RT scheduling; reports jitter and missed deadlines. At the
  1 MHz sim clock the RTL cannot sustain wall-clock line rate, so this lane is
  for realism experiments, not correctness verdicts.

## 3. Decision matrix

| candidate | AVB semantics (CBS/TAS/VLAN/reserved-grp/gPTP) | determinism/replay | real-time vs 1 MHz sim | integration w/ Verilator+raw-socket | maturity | verdict |
|---|---|---|---|---|---|---|
| deterministic userspace `virtwire` | implement CBS/Qav queues, PCP, group allowlist, gPTP policy — full control | **strong** (seeded JSONL/PCAP) | exact virtual time; no wall-clock false claims | direct (UNIX seqpacket + AF_PACKET) | to build | **PRIMARY** |
| Linux bridge + `tc` (mqprio/cbs/taprio/etf, flower) | cbs/taprio model Qav/Qbv; **not** a full 802.1AS transparent clock; reserved-group forwarding needs explicit `group_fwd_mask` | weak (host scheduling) | near-real-time, but no hard guarantees | veth/netns/AF_PACKET | mature kernel | **SECONDARY lane** |
| P4 / BMv2 (simple_switch) | match/forward only; no native CBS/gPTP temporal model | n/a for timing | **not a real-time target** | heavy (P4 program + target) | mature | **DEFER** |
| Open vSwitch | mature forwarding/control | weak | no AVB temporal compliance | netdev | mature | not primary |
| DPDK | high throughput, timing control | needs custom TSN behavior | custom effort | hugepages/root, complex | mature | too heavy for now |
| ns-3 / OMNeT++ INET TSN | rich offline TSN models (CBS, 802.1AS) | offline sim | **hard lockstep with RTL/QEMU**; not real-time | poor fit | mature sim | reference only |

## 4. Raw-socket (`AF_PACKET`) fidelity boundary — state this always

A raw socket is the right **attachment point** but is **not** an AVB-compliant
switch by itself. `AF_PACKET`/`SOCK_RAW`/`ETH_P_ALL` with `TPACKET_V3`/
`PACKET_RX_RING` delivers Ethernet **L2 frames** — typically **without** preamble
or a trustworthy FCS, and the host NIC may strip/regenerate FCS. So the wire can
validate VLAN/PCP, ADP/AECP/ACMP, AVTP/AAF/CRF, MSRP/MVRP, forwarding, queue
selection, and above-MAC fault injection. It **cannot** validate preamble/SFD,
bad-FCS reception, RGMII/PHY timing, analog behavior, or hardware timestamp
quality. Those stay `BLOCKED` in the virtual tier.

Adapter requirements: `PACKET_IGNORE_OUTGOING`; preserve VLAN tags (disable
VLAN offload); disable GRO/GSO/TSO/LRO; deterministic MACs; netns isolation;
`CAP_NET_RAW`/`CAP_NET_ADMIN` only (never whole-suite root); bounded queues with
explicit overflow counters; never block the Verilator scheduler on a socket read.

## 5. Why not P4 first (and when it earns a place)

P4 is excellent for parse/match/forward, but BMv2/simple_switch is not a
real-time target and its pipeline does not express CBS credit state or 802.1AS
residence time — you would still need an external scheduler/time model, exactly
what `virtwire` provides. A hardware P4 target would violate the boardless
requirement. **Keep P4 as an optional later backend** once the `virtwire` frame
contract is stable, if a programmable-switch test is ever wanted.

## 6. `virtwire` required behavior (the AVB feature list)

1. **No frame mutation by default** — bytes in = bytes out; preserve VLAN
   TPID/TCI/PCP; PCAP ingress/egress hashes match in transparent mode.
2. **Explicit reserved-group policy** — allowlist/test matrix for
   `01:80:C2:00:00:0E` (gPTP), AVDECC `91:E0:F0:01:FF:00`, MAAP, MSRP/MRP/MVRP
   groups. Never rely on an unspecified bridge default.
3. **Deterministic event model** — every frame gets
   `{sequence, virtual_time_ns, ingress, egress, sha256}`; seeded replay.
4. **Fault injection** — drop/duplicate/reorder/delay/corrupt/PCP-tag-corrupt/
   link-down-restart; each fault has an expected DUT/oracle result.
5. **Backpressure** — bounded queues, declared overflow policy, overflow is a
   recorded event, never silent loss.
6. **Independent observation** — the switch captures evidence but must not be the
   only oracle; T3 requires a foreign AVDECC controller (candidate: `la_avdecc`).
7. **VLAN-aware forwarding + PCP classification**; separate best-effort and
   Class A queues.
8. **CBS (802.1Qav) model** — `idleSlope`, `sendSlope`, `hiCredit`, `loCredit`,
   matched against a separate reference implementation.
9. **MSRP/MVRP transport + observable registration state.**
10. **Per-port/per-queue counters**; deterministic queue-order evidence; PCAP +
    JSONL output; link up/down events; explicit gPTP fidelity declaration.

## 7. `VirtualWirePort` contract (implementation interface)

```
send(frame, ingress_vtime, metadata)
recv() -> frame, egress_vtime, metadata
set_link(up/down)
set_rate(bits_per_second)
set_fault_profile(seed, profile)
snapshot_counters()
```

Transport: each virtual DUT gets a dedicated UNIX `SOCK_SEQPACKET` endpoint; a
frame is one atomic message with envelope
`{node_id, direction, simulated_time_ns, frame_len, raw_ethernet_frame}`.
Optional `AF_PACKET` adapter bridges `virtwire` to the host/controller.

## 8. Phased plan (maps to T2/T3)

- **T2.0 — frame contract + loopback.** `virtwire` core, envelope tests
  (framing, max size, malformed length, disconnect/reconnect), PCAP+JSONL,
  transparent forwarding of tagged/untagged frames. Acceptance: input==egress;
  same seed → identical JSONL/PCAP; malformed envelope → classified reject.
- **T2.1 — attach the real Verilator datapath MAC** to `virtwire` (raw frames
  cross the real MAC boundary, not a high-level model). Negative frame/FCS/
  length cases reach the intended rejection path.
- **T2.2 — Linux-sized RAM + real RV32 boot.** Replace the 64 KiB integrated RAM
  with a Linux-sized SDRAM sim model; boot the RV32 tuple (OpenSBI+DTB+kernel+
  rootfs) with real `S50milan`. Exact-hardware lane = VexiiRiscv+LiteX+Verilator
  (authoritative); QEMU lane = fast orchestration (the LiteX OpenSBI likely does
  not boot stock `-machine virt`; prove or build a custom machine model).
- **T2.3 — true single-node E2E.** provisioned CSR state matches; ≥1 ADPDU on the
  wire; independent decoder validates; 1×1 `entity_model_id` negative control
  goes red; shaped-traffic CBS sequence matches the reference model.
- **T3 — machine-to-machine** (distinct MAC/entity/model/stream/image/seed per
  node; `la_avdecc` as controller; stale-AEM / duplicate-entity-id / dropped-ADP
  / journal-corruption negative controls).

## 9. What we must NOT claim

- No line-rate AVB compliance at the 1 MHz sim clock.
- `tc cbs`/`taprio` are **not** a complete 802.1AS transparent clock.
- A Linux bridge does **not** forward `01:80:C2:xx` reserved groups by default —
  this must be tested, not assumed.
- `virtwire` is a **behavioral model**, not a conformant switch, until
  independently tested.
- A green virtual run is a simulation result, never a hardware claim.

## 10. Primary sources to cite (deferred Opus pass)

The citation pass must fetch and date-stamp primary docs for: `tc-cbs`,
`tc-mqprio`, `tc-taprio`, `tc-etf`, bridge VLAN filtering + `group_fwd_mask`,
`packet(7)`/`TPACKET_V3`, linuxptp `ptp4l` (SW vs HW timestamping, transparent-
clock limits), BMv2 `simple_switch` queue behavior, PSA/PNA scheduling limits,
DPDK `rte_eth_tx_burst` / time-aware scheduling, ns-3/INET TSN CBS + 802.1AS
models, and QEMU RISC-V machine-model options. No claim in §3–§5 about kernel /
P4 / DPDK behavior is final until its source is linked here.
