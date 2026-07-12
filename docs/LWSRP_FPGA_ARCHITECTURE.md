# lwSRP-fpga — lightweight SRP engine in fabric (proposal)

Status: PROPOSED 2026-07-12 (rev-2 delimitation: "everything goes FPGA, use
lwSRP"). Scope: talker endpoint first; listener half lands with STREAM_INPUT.
Pattern of record: the ADP/AECP/ACMP responder recipe (registered monitor tap,
template TX, low-rate merge, CSR status) — proven Milan=1-clean four times.

## 1. What lwSRP must do (and what it deliberately does not)

Milan v1.2 §5.6 pins SRP usage down enough that a small engine is conformant:

DOES (talker endpoint):
- **Declare** as MRP applicant, always-declare subset:
  - MSRP **Domain** (SR class A: classID 6, priority 3, VID from CSR, default 2)
  - MSRP **Talker Advertise** per enabled stream (N_STREAMS param; 1 today)
  - MVRP **VLAN** membership for the SR VID
- **Register** as MRP registrar, only what gates us:
  - **Listener** attribute for OUR StreamID(s): Ready / AskingFailed /
    ReadyFailed (four-packed declaration types)
  - Bridge **Domain** (class/priority/VID sanity -> SRP domain-boundary flag)
  - **LeaveAll** handling (re-declare on LeaveAll; registrar ages out)
- **Gate + provision bandwidth**: reservation ACTIVE :=
  (talker declared) AND (listener READY registered) AND (domain ok) AND
  (sum of granted BW <= 75 % of port rate). On ACTIVE: drive the class-A
  CBS idleSlope from the TSpec and OPEN the stream gate into the class-A
  queue (FR-SRP-03: no reservation -> no stream tx). On withdraw/leave/
  LeaveAll-timeout: close the gate first, then release the slope.

DOES NOT (lw choices, all safe against bridges):
- No full 12-state MRP applicant; we run the always-declare subset:
  periodic JoinIn on the Join timer, re-declare on LeaveAll, explicit Lv on
  disable. Bridges only need our attribute refreshed inside LeaveAll period.
- No MMRP. No SR class B (constants parameterized, class A only enabled).
- No domain negotiation — we assert Milan defaults and FLAG mismatch
  (AECP AVB_INFO already carries the flags field; readable at 0x66C too).
- No PDU generation with multi-value vectors (we declare exactly 1 value
  per attribute type; RX side handles arbitrary bridge vectors).

## 2. Wire formats (byte-exact, the part that must never be guessed)

MSRP: dst **01:80:C2:00:00:0E** (link-local, never forwarded), EtherType
**0x22EA**. MVRP: dst **01:80:C2:00:00:21**, EtherType **0x88F5**.

MRPDU = ProtocolVersion(1)=0, then Messages, then EndMark 0x0000.
MSRP Message = { AttributeType(1), AttributeLength(1),
                 **AttributeListLength(2) — MSRP only, MVRP has none**,
                 VectorAttributes..., EndMark }.
VectorAttribute = { VectorHeader(2) = LeaveAllEvent*8192 + NumberOfValues,
                    FirstValue(AttributeLength),
                    ThreePackedEvents ceil(N/3): v = e1*36 + e2*6 + e3
                      (0 New · 1 JoinIn · 2 In · 3 JoinMt · 4 Mt · 5 Lv),
                    [Listener only: FourPackedEvents ceil(N/4):
                      0 Ignore · 1 AskingFailed · 2 Ready · 3 ReadyFailed] }

FirstValue layouts:
- Domain (type 4, len 4):   { SRclassID(1)=6, SRclassPriority(1)=3, VID(2) }
- TalkerAdvertise (type 1, len 25):
    { StreamID(8) = station MAC(6) + UniqueID(2),
      DataFrameParameters { dest MAC(6), VID(2) },
      TSpec { MaxFrameSize(2), MaxIntervalFrames(2) },
      PriorityAndRank(1) = { prio[7:5]=3, rank[4]=1, rsvd[3:0] },
      AccumulatedLatency(4) }
- TalkerFailed (type 2, len 34): + { BridgeID(8), FailureCode(1) } — RX-only
  for us (we track the code for AECP/STREAM_INFO exposure).
- Listener (type 3, len 8): { StreamID(8) } + four-packed declarations.
- MVRP VID (type 1, len 2): { VID(2) }.

Vector semantics trap: value k of a vector is FirstValue **incremented k
times** (StreamID+k, VID+k). The RX walker must range-match our StreamID,
not equality-match the FirstValue.

Class-A idleSlope from TSpec (per reservation):
  idleSlope[bps] = MaxIntervalFrames x (MaxFrameSize + 42) x 8 x 8000
  (42 = preamble 8 + eth hdr 14 + VLAN 4 + FCS 4 + IPG 12; class A
  measurement interval 125 us -> 8000/s). 75 % gate vs port rate
  (1 Gb/s AX7101 · 100 Mb/s Arty via is_1g).

## 3. Block architecture (hdl/lwsrp/, KL_lwsrp_*)

```
rx_axis_to_dma (the tap point, little lane) ──┐ (copy, never stalls)
                                              v
                 ┌──────────────────────────────────────────┐
                 │ KL_lwsrp_ingress — registered tap;        │
                 │ dst ∈ {..:0E, ..:21} + ethertype match    │
                 └───────────────┬──────────────────────────┘
                                 v  beats (no frame buffer!)
                 ┌──────────────────────────────────────────┐
                 │ KL_lwsrp_walker — STREAMING vector parser │
                 │ (constant state: msg hdr, FirstValue      │
                 │ accumulator 25 B, vector countdown;       │
                 │ handles any PDU length — no truncation)   │
                 │ out: leaveall_p · domain_seen{cls,prio,   │
                 │ vid} · listener_evt{idx, 4packed}         │
                 └───────┬───────────────────┬──────────────┘
                         v                   v
        ┌───────────────────────┐  ┌───────────────────────────┐
        │ KL_lwsrp_registrar    │  │ KL_lwsrp_applicant        │
        │ per attribute:        │  │ always-declare: Join tick │
        │ MT/IN/LV + leave      │  │ (200 ms) refresh; LeaveAll│
        │ timer 600 ms;         │  │ -> re-declare; disable -> │
        │ LeaveAll -> LV        │  │ Lv then silence           │
        │ out: listener_state[i]│  └──────────┬────────────────┘
        │ domain_ok             │             v
        └──────────┬────────────┘  ┌───────────────────────────┐
                   │               │ KL_lwsrp_tx — template     │
                   │               │ MRPDU serialiser (the      │
                   │               │ adp_advertiser recipe):    │
                   │               │ MSRP {Domain + TalkerAdv}  │
                   │               │ + MVRP {VID}; fields       │
                   │               │ patched from CSR/stream    │
                   │               │ table; 64b AXIS LE        │
                   │               └──────────┬────────────────┘
                   v                          v
        ┌───────────────────────┐    lwsrp_tx ── into the low-rate
        │ KL_lwsrp_bw_gate      │    merge chain (4th input; chain
        │ ACTIVE := declared &  │    one more adp_tx_arbiter —
        │ READY & domain_ok &   │    established pattern)
        │ Σslope <= 75 % rate   │
        │ out: o_stream_gate[i] │──> AAF framer / class-A queue admission
        │ o_idle_slope (bps)    │──> traffic_shaping_core slope MUX
        │ o_res_state (CSR)     │    (lwsrp_en ? granted : CSR slope)
        └───────────────────────┘
        KL_lwsrp_timers: join 200 ms · leave 600 ms · leaveall 10 s
        (from the datapath 1 kHz tick — KL_aecp_timers pattern)
        KL_lwsrp_top: wiring + CSR + N_STREAMS=1 stream table
```

Key structural choices:
- **Streaming walker, no frame buffer.** Bridge MRPDUs can be ~1500 B with
  many vectors; buffering invites truncation bugs. The walker keeps only
  the current attribute header + a 25 B FirstValue accumulator + counters —
  constant area, any PDU length. (AECP buffered because it must ECHO;
  lwSRP never echoes.)
- **Gate-before-slope ordering** on teardown (close stream gate, then
  release bandwidth) so a withdrawn reservation can never leak frames.
- **Slope MUX, not CSR write-back**: the grant drives the shaper through a
  hardware mux (lwsrp_en selects granted slope over the 0x400 CSR value);
  software can still inspect both. No CDC writes into the CSR file.
- The **stream table** row i = { enabled, unique_id, dest_mac(6) [MAAP-range
  constant from CSR until fabric MAAP], vid, max_frame, interval_frames,
  latency } — AECP GET_STREAM_INFO and the future ACMP connection table read
  the same row: one source of stream truth, like the 0x600 identity group.

## 4. CSR group (proposed 0x660-0x69C, RO unless noted)

| Offset | Field |
|---|---|
| 0x660 | LWSRP_CTRL (RW): [0] enable · [1] talker0 enable · [7:4] class (RO=A) |
| 0x664 | LWSRP_VID (RW): [11:0] SR VID (reset 2) |
| 0x668/0x66C | LWSRP_DMAC lo/hi (RW): stream dest MAC (until fabric MAAP) |
| 0x670 | LWSRP_TSPEC (RW): {MaxIntervalFrames[31:16], MaxFrameSize[15:0]} |
| 0x674 | LWSRP_STATUS: [3:0] listener_state{none/askfail/ready/readyfail} · [4] declared · [5] domain_ok · [6] reservation_active · [8+] failure code (from TalkerFailed) |
| 0x678 | LWSRP_SLOPE: granted idleSlope, bps (RO) |
| 0x67C | LWSRP_CNT: {rx_pdus[31:16], tx_pdus[15:0]} (RO) |

TCAM note: two entries must admit the link-local dst MACs
(01:80:C2:00:00:0E, :21) to rx_axis_to_dma — add to the default entry set
next to the AVDECC multicast (default-pass covers it today; make explicit).

## 5. Integration contract

- **CBS**: `o_idle_slope` + `lwsrp_en` -> slope mux in traffic_shaping_core
  (class-A queue only). Reset behaviour unchanged when disabled.
- **AAF framer (next increment)**: `o_stream_gate[0]` is its transmit
  enable; no reservation, no media — by construction.
- **AECP**: GET_STREAM_INFO gains real {dest_mac, vid, msrp_failure_code,
  flags.CONNECTED}; GET_AVB_INFO flags gain SRP domain-boundary; overlay
  reads the stream table (same recipe as the 0x600 identity overlay).
- **ACMP connection table (follows lwSRP)**: acceptance check =
  `reservation_active`; PROBE_TX fast-connect arms `talker0 enable`.
- **gPTP**: none required for reservation itself; AccumulatedLatency is a
  constant until measured.

## 6. Verification plan (the campaign recipe)

1. **Verilator TB (tb/verilator/lwsrp)** — hand-built bridge-side MRPDUs:
   Listener Ready/AskingFailed/ReadyFailed (single + multi-value vectors
   spanning our StreamID at an offset — the +k trap), Domain match/mismatch,
   LeaveAll storm, leave-timer expiry, TalkerFailed code capture, gate/slope
   ordering on teardown, byte-exact TX templates (MSRP + MVRP), 75 % refusal.
2. **Yosys/lint gates** — same 20/20 discipline (streaming walker is plain
   FSM logic; no memories beyond the stream table FFs).
3. **Silicon** — the AVB switch is a real SRP bridge: talker attribute must
   appear in its registration database; **pw0's pipewire module-avb acts as
   the listener** (Listener Ready on connect — the same
   reference-as-validator move that closed the AECP campaign); OpenAvnu
   `mrpd` on pw0 as a second oracle. Gate: reservation_active=1 on the
   board, bandwidth visible on the switch, stream gate opens; unplug the
   listener -> Ready withdrawn -> gate closes within the leave time.

## 7. Implementation order (each step green before the next)

1. `lwsrp_pkg` + TX templates + applicant timers -> TB checks TX bytes.
2. Streaming walker + registrar -> TB bridge-PDU suite.
3. bw_gate + slope mux into CBS + stream gate -> milan_dp integration test.
4. CSR group + status; lint/yosys; build sweep; silicon vs the switch + pw0.
5. Then: fabric ACMP connection table consuming `reservation_active`.

Est. size: well under the AECP entity (~8-10K LUTs by analogy with the
ACMP responder 8.8K; the walker is the only nontrivial FSM).
