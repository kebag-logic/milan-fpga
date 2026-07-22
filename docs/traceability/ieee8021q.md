# Traceability — IEEE 802.1Q-2022 (VLAN / FQTSS-CBS / MRP / MSRP / MVRP)

Part of [`docs/SPEC_TRACEABILITY.md`](../SPEC_TRACEABILITY.md). Clause numbers
verified against `/home/alex/standards/8021Q-2022.pdf` (Q-2018 numbering is
identical for these clauses). We are an **end station** (Talker/Listener PAAD),
not a bridge: bridge-only clauses are marked N/A. Milan MRP/MSRP deltas
(timer tolerances, endmarks, Domain values) live in
[`milan-v12.md`](milan-v12.md).

Modules: `hdl/802_1q_traffic_shaper/` (`traffic_classifier`,
`traffic_class_map`, `traffic_queues`, `traffic_shaping_core`,
`credit_based_shaper`, `traffic_controller_802_1q`), `hdl/lwsrp/` (9 modules,
CSR 0x680), supporting `hdl/common/tcam.sv` + `rx_mac_filter.sv`.

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
| Q-9 | 34.3 | Bandwidth availability: SR classes limited to 75 % (deltaBandwidth defaults) | KL_lwsrp_bw_gate | ✅ RTL lwsrp (75 % TSpec refusal scenario) | 34.3: exceeding 75 % legally starves best-effort — and the bridge will reject what we'd declare anyway. |
| Q-10 | 34.4 | Actual bandwidth derived from TSpec MSDU size incl. per-frame overheads → idleSlope | KL_lwsrp_bw_gate → CBS idleSlope activation | ✅ RTL lwsrp (slope-before-gate ordering on activate, gate-before-slope on teardown) | 34.4: forgetting the 42-byte per-frame overhead undersizes idleSlope and the shaper throttles in-contract media. |
| Q-11 | 34.5 | Default SR class config: class A = PCP 3, SR_PVID default = VID 2 | lwsrp_pkg constants; datapath VID discipline | ✅ RTL lwsrp_tx (Domain bytes); CERT es-1.2 (Domain {A, 3, 2}); SILICON (MSRP Domain = VID 2 corrected finding) | 34.5: the bench-measured truth — Domain misparse as 638 cost a debugging round; the defaults are load-bearing for interop. |
| Q-12 | 34.2 | SRP domain detection: talker uses the boundary-port rules (Domain attribute) to pick class priority | lwsrp registrar (domain boundary tracked) | ✅ RTL lwsrp_rx (domain boundary case) | 34.2: transmitting class-A-tagged frames on a non-SRP boundary port is undefined behavior for the bridge. |
| Q-13 | 8.6.1–8.6.5, 8.8, 8.13 | Bridge relay: forwarding, filtering DB, egress rules | — | ➖ N/A — end station (the bench bridge provides these; its pruning behavior is documented in findings) | Bridge-only obligations. |
| Q-14 | 8.6.9 / 8.6.10 | Scheduled traffic (Qbv TAS), PSFP gates | — | ➖ N/A — recorded out of scope (PROTOCOL_VALIDATION_MATRIX Q-5) | Not part of Milan; row tracks intent only. |

Supporting (no Q clause of their own): `tcam`/`rx_mac_filter` (dest-MAC
admission for MAAP-claimed + protocol multicasts; ✅ RTL tcam 19 / rx_filter
14 / tcam_csr) and `tx_ifg_gasket` (802.3 IPG discipline on the control lane
only — the MilanMAC back-to-back eater workaround; ✅ RTL ifg; NEVER on the
final output = 600 Mbit cap).

## 2. MRP core (Clause 10) — as profiled by lwSRP

lwSRP is a deliberate *simplified applicant* (deviations from the full MRP
applicant/registrar are documented in `docs/LWSRP_FPGA_ARCHITECTURE.md` and
the pipewire-contract notes). Rows assert the observable wire contract, not
the internal 10.7 state tables.

| # | Clause | Required behavior | Module | Verification today / tsn_gen | Why it matters |
|---|--------|-------------------|--------|------------------------------|----------------|
| MRP-1 | 10.8.1 / 10.8.2 | MRPDU structure: ProtocolVersion, Messages (AttributeType/Length), VectorAttributes (VectorHeader = LeaveAllEvent + NumberOfValues, FirstValue, packed events), EndMarks | KL_lwsrp_tx (build), KL_lwsrp_walker (parse) | ✅ RTL lwsrp_tx (363: byte-exact, decoded like a bridge with endmark walk); lwsrp_rx (75); lwsrp_switchpdu (real certified-switch MSRPDU replay); ❌ tsn_gen NO MODEL | 10.8.2: the +k multi-value vector encoding ("value + k" per packed event) is the documented walker trap — one off-by-one registers the wrong stream. |
| MRP-2 | 10.8.3 | Packing/parsing: ThreePackedEvents (6^2), FourPackedEvents (Listener); truncated/garbage MRPDUs must not wedge the parser | KL_lwsrp_walker | ✅ RTL lwsrp_rx (four-packed gating, truncation/garbage recovery) — Milan 4.2.7.1.2 hardening | 10.8.3: MRP frames come from *every* neighbor; a parser wedge on garbage is a remote DoS on reservations. |
| MRP-3 | 10.7.7 | Applicant SM: declare via NEW/JOININ/JOINMT, withdraw via LV; state advances on peer JoinIn | KL_lwsrp_tx lifecycle | ✅ RTL lwsrp_tx (NEW/JOININ/LV lifecycle); lwsrp top (declare cadence ≥ 2 JoinTimes) | 10.7.7: an applicant that stops re-declaring ages out of the bridge in LeaveTime — the "reservation quietly disappears" failure. |
| MRP-4 | 10.7.8 | Registrar SM: IN on Join, leave-timer to MT on Lv/LeaveAll | KL_lwsrp_registrar / KL_lwsrp_ta_registrar | ✅ RTL lwsrp_rx (leave-timer expiry, LeaveAll storms) | 10.7.8: registrar state is what our talker reads as "listener present" — stale IN keeps media flowing to nobody (and vice versa). |
| MRP-5 | 10.7.9 | LeaveAll: on rx/tx LeaveAll, all registrations enter leave-pending and must be re-declared | timers + tx | ✅ RTL lwsrp (LeaveAll turn + prompt re-declare); lwsrp_rx (storm case) | 10.7.9: mishandling the periodic bridge LeaveAll (~every 10 s) tears every stream down once per period. |
| MRP-6 | 10.7.11 | Timer values: JoinTime ~200 ms, LeaveTime 600–1000 ms, LeaveAllTime ~10 s (+Milan tolerances 4.2.7.1.1) | KL_lwsrp_timers | ✅ RTL lwsrp (scaled-clock cadence ≥ 2 JoinTimes); CERT wire cadences | 10.7.11: too-slow Join loses the race against the registrar's LeaveTime on lossy links. |
| MRP-7 | 10.7.10 | PeriodicTransmission SM (periodic re-Join stimulus) | lwsrp timers (folded into declare cadence) | 🟡 covered implicitly by declare-cadence checks; no explicit periodic-enable/disable vector | 10.7.10: without periodic transmission, an MRPDU lost on a quiet link is never repaired until LeaveAll. |
| MRP-8 | 10.9–10.12 | MMRP application | — | ➖ N/A — MMRP not used (dest-MAC admission handled by MAAP + TCAM) | Not required for Milan PAADs. |

## 3. MSRP (Clause 35) + MVRP (Clause 11)

| # | Clause | Required behavior | Module | Verification today / tsn_gen | Why it matters |
|---|--------|-------------------|--------|------------------------------|----------------|
| SRP-1 | 35.2.2 / 35.2.6 | Attribute encodings: Domain (ClassID/Priority/VID), TalkerAdvertise FirstValue = {StreamID, DataFrameParameters (DMAC+VID), TSpec (MaxFrameSize, MaxIntervalFrames), PriorityAndRank, AccumulatedLatency}, Listener + FourPackedEvent | KL_lwsrp_tx / walker / lwsrp_pkg | ✅ RTL lwsrp_tx (byte-exact Domain + TalkerAdvertise); lwsrp_switchpdu; ❌ tsn_gen NO MODEL | 35.2.6: every field here is consumed by the *bridge's* admission math — a wrong TSpec byte turns into a TalkerFailed three hops away. |
| SRP-2 | 35.1.2 (talker) | End-station talker declares TalkerAdvertise for each stream it can source; withdraws when stopping | KL_lwsrp_tx (single talker attribute) | ✅ RTL lwsrp_tx + lwsrp top; SILICON (bridge registers, stream flows) — 🟡 single-stream only (gaps §3; NxN work planned) | 35.1.2: no declaration = bridge prunes the stream to zero ports (proven on the bench: unregistered SR-tagged stream forwarded nowhere). |
| SRP-3 | 35.1.2 (listener) | Listener declares Listener Ready for bound streams; withdraws on unbind; attaches only after Ready | KL_lwsrp_ta_registrar + listener attr TX; driven by KL_acmp_listener bind | ✅ RTL lwsrp (activation ordering); acmp_lstn (SRP registered/failed transitions); SILICON bind→register→media | 35.1.2: Ready is what makes the bridge open the gate toward us; media before Ready is dropped upstream. |
| SRP-4 | 35.2.4 | Talker registration consumed: TalkerAdvertise ⇒ stream connectable; TalkerFailed ⇒ failure code surfaced (Table 35-6) | walker + registrar (TalkerFailed capture incl. code) | ✅ RTL lwsrp_rx (TalkerFailed capture); SILICON (code 5 = DMAC collision → MAAP fix; code 8 = no 802.1AS on port) | 35.2.4/Table 35-6: the failure code is the only diagnostic the network gives a listener — both bench root-causes came from reading it. |
| SRP-5 | 35.2.1.4 etc. | Domain declaration participation: emit/receive Domain {class, priority, VID}; mark boundary if peer disagrees | tx + registrar | ✅ RTL lwsrp_tx (Domain PDU); lwsrp_rx (domain boundary); CERT es-1.2 | 35.1.4: agreeing on {A, 3, 2} per port is the precondition for every reservation on the link. |
| SRP-6 | 35.2.4.3(b)-ish rank/latency | AccumulatedLatency propagation + MSRP_ACC_LAT exposure via AECP SET/GET_STREAM_INFO | walker capture → AECP (direct dp net) | ✅ RTL aecp (MSRP_ACC_LAT sub-command) + aecp [25]: a CHANGING acc-latency follows into GET_STREAM_INFO (137042 → 250000 → dereg 0). Evidence chain: lwsrp_rx proves the wire→walker capture, aecp [25] the input→readback, and the join is the single named `milan_datapath` net `lwsrp_ta_acclat` (ta_acclat_o → lstn_ta_acclat_i, no CSR hop) — no one TB yet drives wire-MRPDU→GET_STREAM_INFO in one run | 35.2.2: AccumulatedLatency is the number controllers use to align presentation offsets across listeners. |
| SRP-7 | Clause 11 (11.2.1–11.2.3) | MVRP: declare the SR VID (2) so the bridge adds port membership | KL_lwsrp_tx MVRP VID MRPDU | ✅ RTL lwsrp_tx (byte-exact MVRP PDU); SILICON (bridge VLAN-2 ingress-filter lesson: no MVRP join = tagged frames dropped at ingress) | 11.2.1: VLAN membership is dynamic on AVB bridges; skipping MVRP is why early talker frames vanished at the first hop. |
| SRP-8 | 35.x class B | SR class B (PCP 2, 250 µs interval) declarations and domain | KL_lwsrp_walker/registrar (RX handling only) | 🟡 INCOMING half TB-proven (lwsrp_rx 8b): packed B-first NoV=2 Domain vectors (the certified switch's real shape) surface the derived class-A value, a wrong derived-A prio flags the boundary, an A=Mt packed value is ignored (neither boundary nor heal), B+Listener in one MRPDU parses with no walker desync. Declaring/using class B stays MISSING (engine + bench class A only, gaps §3). The RTL DEFECT this vector found (2026-07-22: `vector_done` read `dom_a_evt_r` same-cycle-stale, so the class-A event lagged one Domain PDU) is FIXED — the just-decoded class-A event now passes through the emit helper (`daevt`, same staleness rule as every other capture; the EXT_LANES/lsid captures already passed through and were never exposed) and the 8b case asserts the correct behavior | 35.1.4: a second SR class is mandatory-to-*handle* (Domain PDUs for B arrive from the bridge today and must at least not confuse the walker). |
| SRP-9 | 802.1Qat historical / 35 general | Multiple simultaneous reservations (per-stream attribute instances) | — | ❌ MISSING — single talker + single listener attribute today; NxN AAF (AX 8x8 / Arty 4x4) is roadmap item 4, needs per-stream registrar/declaration instances + 2nd listener attr for CRF | 35.2.7: attribute value support requirements assume per-stream instances; the CRF stream currently rides untagged best-effort because the 2nd listener attribute is missing (gaps §2). |

**tsn_gen status: ❌ NO 802.1Q MODELS AT ALL** — to author:
`data_link/ethernet/vlan_tag.yaml` (extend mac_frame; rows Q-1..Q-4),
`data_link/802_1q/mrpdu_msrp.yaml` + `mrpdu_mvrp.yaml` (rows MRP-1..2,
SRP-1..7 — generate legal + mutated vectors: +k ranges, four-pack edge
values, endmark truncation, class-B Domain for SRP-8). These would replace
the hand-hexed frames in `lwsrp_rx`/`lwsrp_switchpdu` and make the Milan
4.2.7.1.2 malformed-MRPDU sweep systematic.
