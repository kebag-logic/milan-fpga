# Traceability — IEEE 802.1Q-2022 (VLAN / FQTSS-CBS / MRP / MSRP / MVRP)

Clause numbers are verified against the local standards PDF
`$STANDARDS_DIR/8021Q-2022.pdf` (Q-2018 numbering is
identical for these clauses). We are an **end station** (Talker/Listener PAAD),
not a bridge: bridge-only clauses are marked N/A. Milan MRP/MSRP deltas
(timer tolerances, endmarks, Domain values) are evaluated by the
[current Milan v1.2 audit](../testing/MILAN_V12_AUDIT_2026-08-16.md). Current
implementation coverage is in the [generated module matrix](MODULE_MATRIX.md).

Modules: [`hdl/ieee8021q/ts/`](../../hdl/ieee8021q/ts) (`traffic_classifier`,
`traffic_class_map`, `traffic_queues`, `traffic_shaping_core`,
`credit_based_shaper`, `traffic_controller_802_1q`) and
[`hdl/ieee8021q/filtering/tcam.sv`](../../hdl/ieee8021q/filtering/tcam.sv) +
`rx_mac_filter.sv`. **The lwSRP reservation stack that used to sit beside them —
11 modules behind CSR 0x680 — was DELETED on 2026-08-13**; MRP, MSRP and MVRP are
now the `protocol-processor` submodule's, reached through
[`hdl/milan/KL_pp_shadow.sv`](../../hdl/milan/KL_pp_shadow.sv).

## STATUS 2026-08-13: the reservation half moved out, the shaping half did not

This clause splits cleanly in two now, and the split is the most important thing
on the page:

- **Shaping is FABRIC and UNCHANGED.** Tag decode, priority regeneration, the
  per-class queues, the credit-based shaper and transmission selection all live in
  the same modules, with the same testbenches, and the 2026-08-13 control-plane
  deletion did not touch them. Rows Q-1..Q-8, Q-13, Q-14 are unaffected.
- **Reservation is the protocol processor's.** The lwSRP applicant, registrar,
  TA-registrar, walker, context table, timers and bandwidth gate are deleted — no
  parameter, no fallback: a build-time fallback would keep a second SRP
  implementation alive, and the substitution's parity argument holds only with
  exactly one owner of the wire law. MRP-1..MRP-8 and SRP-1..SRP-10 are now **🔵 PROCESSOR**: the
  submodule owns the wire law, this fabric consumes the result off the class-D face
  (`srp_sr_admitted_o` as the per-source stream gate, `srp_sum_slope_bps_o` as the
  class-A queue's idleSlope, the adopted {priority, VID} pair as every C-TAG this
  device emits), and [`hdl/milan/milan_datapath.sv`](../../hdl/milan/milan_datapath.sv)
  is where the two meet.

Two consequences worth stating rather than discovering:

- **The evidence went with the RTL.** The `lwsrp`, `lwsrp_ctx`, `lwsrp_rx`,
  `lwsrp_tx` and `lwsrp_switchpdu` Verilator suites are deleted, including the
  byte-exact MRPDU goldens, the real-switch PDU replay and the truncation/garbage
  torture that stood in for a remote-DoS defence. The surviving in-repo suite is
  [`tb/verilator/pp_shadow`](../../tb/verilator/pp_shadow), which grades
  integration and not wire law. The submodule's own benches
  (`protocol-processor/tb/srp_top`, `srp_decoder`, `srp_encoder`,
  `srp_stream_fsms`) carry the law and this repository's gates do not run them.
- **The slope-versus-gate ordering stopped being testable.** The deleted bandwidth
  gate held an explicit two-sided hold — slope joins the running Σ before the gate
  opens, gate closes before the slope leaves. The processor's admission round
  latches grant, granted slope and Σ together, so the invariant HOLDS (equal on the
  opening edge, conservative on the closing one, since Σ briefly budgets a stopped
  stream) but it is now a consequence of the round's structure rather than a
  sequencer any bench can point at.

Also gone with the applicant: the MRPDU tx/rx counters and rx-drop count at CSR
0x680 read **structural zeros**, and the provisioning words software used to write
(DMAC, MaxFrameSize, MaxIntervalFrames, the declare-bypass bit) are **write-only
scratch** — they read back what was written and change nothing observable. The
Domain word, the granted slope and the over-limit bit are STILL LIVE, repointed at
the processor's face.


## Contents

- **[STATUS 2026-08-13: the reservation half moved out, the shaping half did not](#status-2026-08-13-the-reservation-half-moved-out-the-shaping-half-did-not)** -- Where the clause boundary now falls. CBS, the classifier, the queues and the TCAM are still this repository's RTL and still tested here; MRP and SRP are the protocol processor's, asserted against an implementation whose internals this repo cannot see and whose benches it does not run. Also states the evidence lost with the deleted suites.
- **[1. VLAN tagging + priority (Clauses 6, 9)](#1-vlan-tagging--priority-clauses-6-9)** -- Rows Q-1..Q-14: tag decode, PCP regeneration, per-class queueing and the CBS credit math, each with the module and the TB that proves it. **Unaffected by the 2026-08-13 substitution** except Q-9..Q-12, where the admission and Domain inputs now come from the processor. Also the two deliberate N/A rows (bridge relay, Qbv/PSFP) and the standing tsn_gen gap: `mac_frame.yaml` has no VLAN fields at all.
- **[2. MRP core (Clause 10), as profiled by lwSRP](#2-mrp-core-clause-10-as-profiled-by-lwsrp)** -- Rows MRP-1..MRP-8, now 🔵 the protocol processor's. The +k packed-vector trap and the garbage-MRPDU DoS defence are still the two that matter, and both lost their testbench with the applicant. Read MRP-2 before assuming this device is still hardened against a malformed neighbour.
- **[3. MSRP (Clause 35) + MVRP (Clause 11)](#3-msrp-clause-35--mvrp-clause-11)** -- Rows SRP-1..SRP-10, the reservation wire contract, now 🔵 PROCESSOR. The bench root causes read straight off TalkerFailed codes (5 = DMAC collision, 8 = no 802.1AS on port) still hold and the codes still reach software; the MVRP lesson still holds. SRP-6 records that GET_STREAM_INFO publishes AccumulatedLatency to controllers, and that SET_STREAM_INFO's MSRP_ACC_LAT sub-command writes it since 0x0053.

## 1. VLAN tagging + priority (Clauses 6, 9)

| # | Clause | Required behavior | Module | Verification today / tsn_gen | Why it matters |
|---|--------|-------------------|--------|------------------------------|----------------|
| Q-1 | 9.3 / 9.4 / 9.5 | Recognize the C-VLAN tag: TPID 0x8100 immediately after SA; untagged frames still classified | traffic_classifier | ✅ RTL cls (200 k configs incl. untagged default + legacy EtherType fallback); classifier (6); ❌ tsn_gen mac_frame.yaml has NO VLAN-tag fields | 9.5: missing the TPID reads the TCI as EtherType and mis-routes every tagged frame. |
| Q-2 | 9.6 | TCI decode: PCP[15:13], DEI[12], VID[11:0] | traffic_classifier / traffic_class_map | ✅ RTL cls + datapath (tdest exact); RTL aaf (TX TCI golden 0x6002 = PCP 3, VID 2) | 9.6: PCP is the sole input to traffic-class selection on ingress; VID selects the SR tree. |
| Q-3 | 6.9.3 | Priority Code Point encoding on transmit (PCP ← priority, per PCP encoding table) | aaf_talker_i2s / KL_crf_tx (SR class A → PCP 3) | ✅ RTL aaf/crf_tx TCI bytes; SILICON (VID-2 clobber lesson: AAF_CTRL always 0x00020003) | 6.9.3: an SR frame sent with PCP 0 transits the network as best-effort — reservation bypassed, shaping meaningless. |
| Q-4 | 6.9.4 | Priority regeneration on receive (regen table before TC mapping) | traffic_class_map (CSR 0x300) | ✅ RTL cls (PCP→regen→TC→queue over random configs); SIM (CSR-programmed) | 6.9.4 lets a port re-map untrusted upstream PCPs; wrong order (regen after TC) yields different queues than the spec's pipeline. |
| Q-5 | 8.6.6 | Frames queued strictly by traffic class; per-class queues independent | traffic_queues | ✅ RTL queues (11: tdest routing, per-queue byte-exact); controller_rate (cross-queue back-to-back regression) | 8.6.6: cross-queue interleave corruption was a real TX-wedge bug (CBS_DATAPATH_BUG) — this row has a dedicated gating TB. |
| Q-6 | 8.6.7 | Queue management: no reordering within a class, loss only by admission | traffic_queues + shaping core | ✅ RTL datapath (in-order byte-exact per class, burst) | 8.6.7: reordering inside an SR class breaks the AVTP sequence_num contract downstream (AVTP-7). |
| Q-7 | 8.6.8.1 / 34.6.2 | Strict priority transmission selection among non-shaped queues | traffic_shaping_core | ✅ RTL shaper_core (61 k vs independent model: SP order, unshaped bypass) | 8.6.8.1 is the default algorithm; inversion starves the control plane under media load. |
| Q-8 | 8.6.8.2 / 34.6.1 | Credit-based shaper: idleSlope accrual, sendSlope drain, hiCredit/loCredit clamp, credit-reset rules, no transmit while credit < 0 | credit_based_shaper (CSR 0x400) | ✅ RTL cbs (87 k: bit-exact vs fixed-point replica + bounded vs ideal continuous model; accrual under back-pressure; live reconfig hiCredit clamp) | 34.6.1's math is the AVB latency guarantee itself; the TB's dual-model approach is the reference for any shaper change. |
| Q-9 | 34.3 | Bandwidth availability: SR classes limited to 75 % (deltaBandwidth defaults) | protocol processor `KL_srp_admission` (behind `KL_pp_shadow`) → the fabric's CBS idleSlope mux | 🔵 PROCESSOR — the 75 % TSpec-refusal scenario went with the deleted `lwsrp` suite. The fabric still consumes the verdict: `srp_sr_admitted_o` is the per-source stream gate and `srp_sum_slope_bps_o` the class-A queue's idleSlope | 34.3: exceeding 75 % legally starves best-effort — and the bridge will reject what we'd declare anyway. |
| Q-10 | 34.4 | Actual bandwidth derived from TSpec MSDU size incl. per-frame overheads → idleSlope | protocol processor `KL_srp_admission` (behind `KL_pp_shadow`) → the fabric's CBS idleSlope mux | 🔵 PROCESSOR — and the slope-versus-gate ORDERING is no longer a testable behaviour: the admission round latches grant, slope and Σ together, so the invariant holds structurally (equal on the opening edge, conservative on the closing one) with no sequencer left to point a bench at. The MaxFrameSize the recipe consumes is still derived in [`milan_datapath`](../../hdl/milan/milan_datapath.sv) from the real AAF geometry and handed over as `cfg_tspec_max_frame_i` | 34.4: forgetting the 42-byte per-frame overhead undersizes idleSlope and the shaper throttles in-contract media. |
| Q-11 | 34.5 | Default SR class config: class A = PCP 3, SR_PVID default = VID 2 | processor SRP encoder for the declaration; `cfg_lwsrp_vid` (reset word 0x684 = 2) for this fabric's default, and the ADOPTED pair from the class-D face once a Domain has been seen | 🔵 PROCESSOR for the Domain bytes; ✅ RTL crf_tx TCI golden 0x6002 for the tag. The property that survives intact is the ONE-SOURCE rule: the AAF and CRF C-TAGs mux off exactly the pair the processor publishes (`srp_class_a_prio_o` / `srp_class_a_vid_o`), so frame and declaration cannot name different values. Historic: BENCH item 1.2; SILICON MSRP Domain = VID 2 | 34.5: the bench-measured truth — Domain misparse as 638 cost a debugging round; the defaults are load-bearing for interop. |
| Q-12 | 34.2 | SRP domain detection: talker uses the boundary-port rules (Domain attribute) to pick class priority | processor SRP registrar (`srp_domain_adopted_o`) | 🔵 PROCESSOR — the boundary case was pinned by the deleted `lwsrp_rx` suite. The fabric reads only the adopted verdict | 34.2: transmitting class-A-tagged frames on a non-SRP boundary port is undefined behavior for the bridge. |
| Q-13 | 8.6.1–8.6.5, 8.8, 8.13 | Bridge relay: forwarding, filtering DB, egress rules | — | ➖ N/A — end station (the bench bridge provides these; its pruning behavior is documented in findings) | Bridge-only obligations. |
| Q-14 | 8.6.9 / 8.6.10 | Scheduled traffic (Qbv TAS), PSFP gates | — | ➖ N/A — recorded out of scope by the [testing guide](../testing/TESTING.md) | Not part of Milan; row tracks intent only. |

Supporting (no Q clause of their own): `tcam`/`rx_mac_filter` (dest-MAC
admission for MAAP-claimed + protocol multicasts; ✅ RTL tcam 19 / rx_filter
14 / tcam_csr) and `tx_ifg_gasket` (802.3 IPG discipline on the control lane
only — the MilanMAC back-to-back eater workaround; ✅ RTL ifg; NEVER on the
final output = 600 Mbit cap).

## 2. MRP core (Clause 10), as profiled by lwSRP

These rows described a deliberate *simplified applicant*, and that applicant is DELETED
(2026-08-13). MRP is now the protocol processor's, and the rows below assert the same
observable wire contract against a different implementation — one whose internals this
repository cannot see and whose benches it does not run. The design doc that recorded the
old deviations from the full 10.7 state tables went with it.

| # | Clause | Required behavior | Module | Verification today / tsn_gen | Why it matters |
|---|--------|-------------------|--------|------------------------------|----------------|
| MRP-1 | 10.8.1 / 10.8.2 | MRPDU structure: ProtocolVersion, Messages (AttributeType/Length), VectorAttributes (VectorHeader = LeaveAllEvent + NumberOfValues, FirstValue, packed events), EndMarks | processor `KL_srp_encoder` (build) / `KL_srp_decoder` (parse) | 🔵 PROCESSOR — the 363-check byte-exact golden, the bridge-style endmark walk and the real reference-switch MSRPDU replay are all deleted with `lwsrp_tx`, `lwsrp_rx` and `lwsrp_switchpdu`. ❌ tsn_gen still has NO MRPDU model, which now leaves the +k trap with no mechanised guard at all | 10.8.2: the +k multi-value vector encoding ("value + k" per packed event) is the documented walker trap — one off-by-one registers the wrong stream. |
| MRP-2 | 10.8.3 | Packing/parsing: ThreePackedEvents (6^2), FourPackedEvents (Listener); truncated/garbage MRPDUs must not wedge the parser | processor `KL_srp_decoder` | 🔵 PROCESSOR — **and this is the row where the evidence loss bites hardest**: MRP frames come from every neighbour, a parser wedge on garbage is a remote DoS on reservations, and the truncation/garbage torture that stood guard is gone. UNVERIFIED here | 10.8.3: MRP frames come from *every* neighbor; a parser wedge on garbage is a remote DoS on reservations. |
| MRP-3 | 10.7.7 | Applicant SM: declare via NEW/JOININ/JOINMT, withdraw via LV; state advances on peer JoinIn | processor SRP stream FSMs | 🔵 PROCESSOR — the NEW/JOININ/LV lifecycle and the ≥ 2-JoinTime declare cadence were pinned by deleted suites. An applicant that stops re-declaring ages out in LeaveTime, and nothing in this repo would notice | 10.7.7: an applicant that stops re-declaring ages out of the bridge in LeaveTime — the "reservation quietly disappears" failure. |
| MRP-4 | 10.7.8 | Registrar SM: IN on Join, leave-timer to MT on Lv/LeaveAll | processor SRP stream FSMs (talker and listener directions) | 🔵 PROCESSOR — the registrar state this fabric reads is now `srp_tk_reg_state_o` / `srp_lstn_decl_state_o` off the class-D face, and the composed streaming licence uses it exactly as before | 10.7.8: registrar state is what our talker reads as "listener present" — stale IN keeps media flowing to nobody (and vice versa). |
| MRP-5 | 10.7.9 | LeaveAll: on rx/tx LeaveAll, all registrations enter leave-pending and must be re-declared | processor timer service + SRP FSMs | 🔵 PROCESSOR — the LeaveAll turn and prompt re-declare were pinned by the deleted `lwsrp` suite | 10.7.9: mishandling the periodic bridge LeaveAll (~every 10 s) tears every stream down once per period. |
| MRP-6 | 10.7.11 | Timer values: JoinTime ~200 ms, LeaveTime 600–1000 ms, LeaveAllTime ~10 s (+Milan tolerances 4.2.7.1.1) | processor timer service | 🔵 PROCESSOR — Milan Table 4.3 tightens these values and the submodule owns them now. [`tb/verilator/pp_shadow`](../../tb/verilator/pp_shadow) compresses the prescaler for liveness only, never for cadence | 10.7.11: too-slow Join loses the race against the registrar's LeaveTime on lossy links. |
| MRP-7 | 10.7.10 | PeriodicTransmission SM (periodic re-Join stimulus) | processor timer service | 🟡 → 🔵 PROCESSOR — the periodic-transmission stimulus was implicit in the deleted applicant's declare cadence and is implicit in the processor's now; still no explicit vector, and now no in-repo bench that could carry one | 10.7.10: without periodic transmission, an MRPDU lost on a quiet link is never repaired until LeaveAll. |
| MRP-8 | 10.9–10.12 | MMRP application | — | ➖ N/A — MMRP not used (dest-MAC admission handled by MAAP + TCAM) | Not required for Milan PAADs. |

## 3. MSRP (Clause 35) + MVRP (Clause 11)

| # | Clause | Required behavior | Module | Verification today / tsn_gen | Why it matters |
|---|--------|-------------------|--------|------------------------------|----------------|
| SRP-1 | 35.2.2 / 35.2.6 | Attribute encodings: Domain (ClassID/Priority/VID), TalkerAdvertise FirstValue = {StreamID, DataFrameParameters (DMAC+VID), TSpec (MaxFrameSize, MaxIntervalFrames), PriorityAndRank, AccumulatedLatency}, Listener + FourPackedEvent | processor `KL_srp_encoder` (build) / `KL_srp_decoder` (parse) | 🔵 PROCESSOR — every FirstValue field is consumed by the BRIDGE's admission math, so a wrong byte still becomes a TalkerFailed three hops away; the byte-exact goldens that caught that class are deleted. ❌ tsn_gen NO MODEL | 35.2.6: every field here is consumed by the *bridge's* admission math — a wrong TSpec byte turns into a TalkerFailed three hops away. |
| SRP-2 | 35.1.2 (talker) | End-station talker declares TalkerAdvertise for each stream it can source; withdraws when stopping | processor SRP encoder, declaring per source; the fabric supplies `cfg_stream_id_i` / `cfg_src_en_i` / `cfg_tspec_max_frame_i` and nothing else | 🔵 PROCESSOR. The 2026-07-28 correction stands and is worth keeping: an *unregistered* VLAN-2 stream DMAC is **flooded** (ordinary multicast) while a **registered but listener-less** stream is pruned, so tagging without declaring does not hide a stream — it puts an unreserved one inside the reserved SR VLAN. The per-row provisioner that made every talker declare is deleted; whether every source declares is the submodule's property now | 35.1.2: a declaration is what BUYS pruning toward registered Listeners. **Corrected 2026-07-28:** this row used to read "no declaration = bridge prunes the stream to zero ports"; the bench measured the opposite and [`../limitations/TROUBLESHOOTING.md`](../limitations/TROUBLESHOOTING.md) records it - an *unregistered* VLAN-2 stream DMAC is **flooded** (it is ordinary multicast), while a **registered but listener-less** stream is pruned. The consequence for a talker: tagging without declaring does not hide a stream, it puts an unreserved one inside the reserved SR VLAN. Measured 2026-07-28: 4001 untagged CRF frames in 8 s on a listener-less port. |
| SRP-3 | 35.1.2 (listener) | Listener declares Listener Ready for bound streams; withdraws on unbind; attaches only after Ready | processor's listener declaration, driven by its own ACMP bind | 🔵 PROCESSOR — the bind and the declaration are now both inside the submodule, so the ordering this row asserts (Ready before media) is no longer observable from this repository except at the wire | 35.1.2: Ready is what makes the bridge open the gate toward us; media before Ready is dropped upstream. |
| SRP-4 | 35.2.4 | Talker registration consumed: TalkerAdvertise ⇒ stream connectable; TalkerFailed ⇒ failure code surfaced (Table 35-6) | processor SRP decoder; `srp_snk_fail_code_o` / `srp_src_fail_code_o` on the class-D face | 🔵 PROCESSOR for the capture; ✅ the failure CODE still reaches software through the CSR. Note the face publishes a per-SOURCE bridge id only, so the per-SINK failure BridgeID reads a structural zero rather than wearing a source's value. Both bench root-causes came from reading these codes (5 = DMAC collision, 8 = no 802.1AS on port), and that diagnostic path survives | 35.2.4/Table 35-6: the failure code is the only diagnostic the network gives a listener — both bench root-causes came from reading it. |
| SRP-5 | 35.2.1.4 etc. | Domain declaration participation: emit/receive Domain {class, priority, VID}; mark boundary if peer disagrees | processor SRP encoder + registrar | 🔵 PROCESSOR — agreeing on {A, 3, 2} per port is still the precondition for every reservation, and the adopted pair is published back to this fabric so the C-TAGs follow it | 35.1.4: agreeing on {A, 3, 2} per port is the precondition for every reservation on the link. |
| SRP-6 | 35.2.4.3(b)-ish rank/latency | AccumulatedLatency propagation and MSRP_ACC_LAT exposure through AECP GET_STREAM_INFO | processor SRP decoder → `srp_acc_latency_o` on the class-D face → root GET_STREAM_INFO gather and CSR | 🟡 SPLIT: GET_STREAM_INFO is implemented and publishes the current per-stream AccumulatedLatency to controllers. Processor `pp_top` group G grades the byte-exact Milan response, and root `milan_dp` B2 grades the integrated 80-byte response. SET_STREAM_INFO's MSRP_ACC_LAT sub-command is served since 0x0053, so a controller can both read the value and set the presentation offset the framers stamp; the folded transit entry is the shared source. Historic: ✅ RTL aecp [25] (a changing acc-latency followed into GET_STREAM_INFO, 137042 → 250000 → dereg 0) | 35.2.2: AccumulatedLatency is the number controllers use to align presentation offsets across listeners. |
| SRP-7 | Clause 11 (11.2.1–11.2.3) | MVRP: declare the SR VID (2) so the bridge adds port membership | processor SRP encoder (MVRP) | 🔵 PROCESSOR — the byte-exact MVRP PDU golden is deleted. The SILICON lesson stands and is expensive to relearn: no MVRP join means the bridge drops our tagged frames at ingress | 11.2.1: VLAN membership is dynamic on AVB bridges; skipping MVRP is why early talker frames vanished at the first hop. |
| SRP-8 | 35.x class B | SR class B (PCP 2, 250 µs interval) declarations and domain | processor `KL_srp_decoder` (RX handling only) | 🔵 PROCESSOR — the packed B-first NoV=2 vectors, the derived class-A extraction and the stale-event defect this repo found and fixed were all pinned by the deleted `lwsrp_rx` suite. Milan's verdict is unchanged and still bounds the obligation: 4.2.7.2.1's Domain *shall* is Class A only, so class-B DECLARING is not a compliance blocker and HANDLING is the whole duty | 35.1.4: a second SR class is mandatory-to-*handle* (Domain PDUs for B arrive from the bridge today and must at least not confuse the walker). **Milan verdict (4.2.7.2.1, read 2026-07-28):** the Domain *shall* is **for Class A only** — *"a PAAD shall use SR Class Priority 3 and Default VLAN ID 2 for Class A, and send MSRPDUs declaring an MSRP Domain for Class A"* — and the GET_STREAM_INFO CLASS_B flag is "Not defined by this specification", so class-B DECLARING is not a Milan-compliance blocker; the handling half above is the whole obligation. |
| SRP-10 | 35.2.2.8.4 a) | TSpec MaxFrameSize, verbatim: *"It represents the maximum frame size that the Talker **will produce**, excluding any overhead for media-specific framing (e.g., preamble, IEEE 802.3 header, Priority/VID tag, CRC, interframe gap)"* — the WIRE, never the declaration | the MaxFrameSize derivation SURVIVES in [`milan_datapath`](../../hdl/milan/milan_datapath.sv) — header + the Milan step-1 extra octet + samples×channels, from the same constant that resets `KL_aaf_packetizer`'s chans field — and is handed to the processor as `cfg_tspec_max_frame_i` | ✅ builder gates still green on every shape, and the tie is now SHORTER: the value goes straight from the framer geometry into the declaring engine with no attribute-row table in between. The 2026-07-28 lesson keeps its teeth — a TSpec of a frame nobody sent is a silent over-reservation the bridge dutifully honours | The 2026-07-28 bench measured a TSpec of a frame nobody sent: declared-8ch MaxFrameSize announced while the wire carried the 2ch 72-byte MSDU — a ~3× over-reservation the bridge dutifully honoured. |
| SRP-9 | 802.1Qat historical / 35 general | Multiple simultaneous reservations (per-stream attribute instances) | processor per-source and per-sink SRP state (`N_STREAM_OUT_P` / `N_STREAM_IN_P` arrays) | 🔵 PROCESSOR — the single-attribute limitation this row recorded was the deleted applicant's. The processor carries per-source and per-sink state by construction and publishes it as per-index vectors on the class-D face; the 16-row `ctx_idx` ceiling and its elaboration assert went with the context table. Whether every index really declares is UNVERIFIED here | 35.2.7: attribute value support requirements assume per-stream instances. **2026-07-28:** the CRF stream no longer rides untagged best-effort - it owns a TALKER attribute row of its own (`N_TALKERS_P` = N+1, ctx row `2N-1`), fabric-provisioned so its StreamID/DMAC are derived rather than restated. At 8x8 that is EXACTLY 16 rows = the whole 4-bit `ctx_idx`, guarded by a `milan_datapath` elaboration assert and a builder ConfigError. |

**tsn_gen status: ❌ NO 802.1Q MODELS AT ALL** — and the case for authoring them is now
much stronger than it was, because the hand-hexed frames they were going to replace have
been deleted along with the suites that carried them. To author:
`data_link/ethernet/vlan_tag.yaml` (extend mac_frame; rows Q-1..Q-4),
`data_link/802_1q/mrpdu_msrp.yaml` + `mrpdu_mvrp.yaml` (rows MRP-1..2, SRP-1..7 —
generate legal + mutated vectors: +k ranges, four-pack edge values, endmark truncation,
class-B Domain for SRP-8). Fired at the processor over the wire, that corpus would be the
ONLY systematic Milan 4.2.7.1.2 malformed-MRPDU coverage this project has.
