<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# srp_top — KL_srp_admission + KL_srp_top end-to-end engine suite

Proves the assembled SRP engine (`hdl/srp/KL_srp_top.sv` wiring
KL_srp_decoder → {Domain, VLAN, talker/listener FSMs} → KL_srp_encoder,
with `hdl/srp/KL_srp_admission.sv` feeding the talker plane) against
[10 §1/§2/§3/§6/§7/§9](../../docs/architecture/10_srp_engine.md) and the
[02 §4.1](../../docs/architecture/02_interfaces.md) `srp` contract —
**through the REAL shared blocks**: frames are pulled byte-by-byte off a
real `KL_pp_tx_slots` serialize face (the C++ side plays the 03 §8 TX
arbiter), cadence and registrar-leave timers run on a real
`KL_pp_timer_service` (time-compressed: 1 ms = 40 clk, 32 slots), and the
T-MRP-LEAVEALL draws come from a real `KL_pp_prng` (kind 3, 10–15 s).
`make` = build + run, exit 0 = PASS, **8656 checks**. `make` first runs the
timer-arm FIFO arms at four shapes
([below](#timer-arm-fifos-at-four-shapes-issue-230)), then this suite, whose
tally is the last line.

Expectations are independent: an MRPDU builder/parser written here from
802.1Q §10.8.1.2 / §35.2.2, a Σ-slope model transcribing the Milan v1.2
§4.3.3.2 recipe from the silicon-measured reference
(`milan-fpga/hdl/ieee8021q/srp/KL_lwsrp_bw_gate.sv`: F = MaxFrameSize+22,
min-68 clamp, W = F+20, slope = W·MaxIntervalFrames·8000·8) with the
greedy stream-index-order walk against the 75 % port-rate ceiling, and
the Table 10-3 fresh-declaration ladder (New, New, JoinMt) cited from the
standard — never DUT logic.

Covered end to end:

- **Bring-up**: link-up → Domain default declaration `{6, 3, 2}` New on
  the wire, byte-exact, at the first T-MRP-JOIN drain; class-D defaults.
- **Class-B service port** (02 §4.1 template): GET_DOMAIN {prio, VID}
  (class A only — class 5 FAILs), unknown op UNSUPPORTED, out-of-range
  indices FAIL; single-outstanding request/response contract throughout.
- **DECLARE_TALKER → admission → wire**: granted_slope_bps / sr_admitted /
  Σ / over_limit against the independent model; Talker Advertise New
  byte-exact (25 B FirstValue: stream_id, DA, VID, TSpec, prio/rank from
  the Domain + cfg, accumulated latency), the declaration ladder, and the
  MVRP VID New the membership join emits — all through the real slot pool.
- **Over-ceiling refusal (10 §6.3)**: a TSpec that pushes Σ past 75 % is
  refused → granted 0, over_limit, `tk_decl_state` FAILED, fail code 1 +
  own-MAC system id in class-D, and **Talker Failed code 1 byte-exact on
  the wire** (34 B FirstValue, §35.2.2.8.7 end-station MAC). Withdrawal of
  the blocking stream re-admits it: Advertise New replaces the Failed in
  place, over_limit clears.
- **Listener end-to-end**: DECLARE_LISTENER arms the exact matcher; a fed
  Talker Advertise MRPDU registers (TK_ATTR_REGISTERED, acc_latency
  latch) and the engine answers with a byte-exact Listener Ready New
  (FourPacked lane); the in-place Advertise↔Failed swap both ways
  (REGISTERED strobe, no unregister, failure info latched/gated,
  declaration follows Ready↔AskingFailed).
- **Certified two-class Domain arrival**: FirstValue `{5, 2, VID 5}`,
  NumberOfValues 2 — class A arrives as value 1 (802.1Q §35.2.2.9) —
  adopts (DOMAIN_CHANGE, class-D update, GET_DOMAIN agrees) and
  re-declares end-to-end: one Domain message, Lv `{6,3,2}` + New
  `{6,3,5}`, byte-exact.
- **LeaveAll per application (10 §6.5)**: the own MSRP leavealltimer
  (PRNG-drawn) emits a LeaveAllEvent PDU that flags every MSRP Attribute
  Type once, on its first vector (a NumberOfValues-0 vector for a type the
  cycle declares nothing of; 802.1Q §10.8.2.6), and whose cycle re-declares
  Domain JoinIn + Listener Ready; registrations stay published through LV and a
  peer re-join keeps them (no unregister). A received MSRP LeaveAll that
  flags every MSRP type, as a conformant peer's does (F2), ages the
  registrar over a real 5 s T-MRP-LEAVE to TK_ATTR_UNREGISTERED and the
  Listener Lv reaches the wire — while MVRP membership is untouched.
  The MVRP participant runs its own LeaveAll (flagged PDU, VID re-join,
  never an Lv flap). The F4 peer cadence flags every type the same way.
- **Received LeaveAll routed per Attribute Type, end to end (F5; 10 §6.5,
  802.1Q-2014 §10.7.5.20 NOTE)**: each step starts right after an own MSRP
  LeaveAll, so the next own cycle cannot land in its 5.4 s window, and the
  peer answers it with Listener Ready on source 1 and Talker Advertise
  toward sink 0.
  - **(a)** the bench switch's LeaveAll MRPDU from Run B (LeaveAll in every
    message, Listener JoinMt/Ready first, Talker Advertise/Failed as
    NumberOfValues-0 vectors; this bench's stream_id and Domain VID): the
    Listener registration stays IN past T-MRP-LEAVE and source 1 stays
    ACTIVE, while the Talker Advertise lane ages sink 0's un-re-declared
    Advertise to TK_ATTR_UNREGISTERED.
  - **(b)** a Domain-only LeaveAll: our Domain re-declares (JoinIn at the
    next T-MRP-JOIN, well before any periodic re-join); neither the
    Listener registration nor sink 0's Advertise ages.
  - **(c)** a Listener-only LeaveAll, never re-declared: Ready stays
    published for T-MRP-LEAVE (LV), then ages to MT and ACTIVE drops; sink
    0's Advertise is untouched. The Domain row's negative: no Domain JoinIn
    follows it before the next periodic re-join, nor, each in its own clean
    slot, a Talker Advertise LeaveAll (sink 0's Advertise re-declared in the
    flagged vector) or a Talker Failed-only LeaveAll.
- **Admission sweep**: 30 randomized declare/withdraw rounds across all 8
  sources vs the model — admitted vector, per-source granted slopes, Σ
  and over_limit, exercising the greedy order and capacity reuse.
- **Current-declaration grant (H, issue #112)**: sources 0, 1 and 7 at all
  eight slope-sampling phases. Cold refusal, 224 → 20000-byte growth,
  20000 → 224-byte shrink, and identical re-declaration are observed on
  every cycle from real service-gate acceptance. The refused source never
  grants; every admitted slope belongs to the current declaration; the
  grant is low on acceptance and only returns at round completion.
  Shrink/identical latency is 8/16/24 clocks from acceptance, printed per
  case. An actual Listener Ready PDU is paused before its packed events
  and completed just after acceptance, exercising optimistic ACTIVE before
  the real grant. The suite checks the three-published-round window, the
  ACTIVE equation, zero slope while unadmitted, and settled sum/refusal.
  The window length is printed per case: 25, 33 or 41 clocks, 17 past the
  round that publishes the verdict. No state or verdict is forced. The
  [unit suite](../srp_admission/README.md) covers smaller shapes, rapid
  changes, both TSpec fields and failing mutants.
- **A pending re-declaration frees no capacity (I, issue #112 round 2)**:
  source 0 (69.952 Mb/s) is admitted and ACTIVE. Source 1 or 7
  (15.488 Mb/s) is refused by the 75 Mb/s ceiling and declared Talker
  Failed, with a real Listener Ready. Source 0 then re-declares:
  - identically, or shrunk to 60.288 Mb/s. The other source stays refused.
    On every clock from acceptance it never grants, is never ACTIVE and
    never declares Advertise. Across two T-MRP-JOIN periods, no Talker
    Advertise vector for its stream reaches the wire.
  - shrunk to 17.024 Mb/s, the control that frees capacity. The other
    source's first grant is the same clock as source 0's re-grant, its
    Advertise follows, and its Advertise reaches the wire.

  Each case runs at all eight sampling phases, 48 runs in all. The
  identical re-declaration is also accepted 1 to 40 clocks before a
  T-MRP-JOIN tick (read-only `dbg_join_tick_o` probe). This is the placement
  where round 1's rule put a Talker Advertise on the wire for k = 1–5, 7
  and 8. Every recorded round must publish the independent greedy model,
  and between rounds a grant only retires with its own declaration.
- **The optimistic window outlives a held verdict (J)**: source 7, then
  source 0, both admissible, with 0 to 20 idle clocks between the two
  requests, at all eight phases.
  While source 0 is pending, source 7's verdict is held, and a window that
  aged on discarded rounds could close first. Neither source ever declares
  Failed. A verdict still pending at source 0's acceptance publishes in the
  same clock as source 0's.

Known limits (recorded honestly): the C++ side emulates the TX arbiter
and the processor-top header strip (both out of scope here — 03 §8 / 03
§5 own them); the PRNG face assumes this engine is the only draw client
(true in the wrap; the full processor routes draws); the byte-exact
checks align actions into clean 200 ms slots because T-MRP-PERIODIC
re-joins legitimately aggregate into the same MRPDU at boundary ticks —
aggregation itself is checked structurally by the parser, and the ladder
is covered by set-checks wherever bundling can occur.

Mutation-proven 2026-08-11 (backup/sed/run/restore):

| Mutation | Result |
|---|---|
| Admission ceiling widened to the full port rate (75 % term removed) | 33 of 230 FAIL (refusal phase C: admitted/over_limit/FAILED/wire Failed; the whole G sweep) |
| granted_slope_bps published ungated (raw slope instead of admitted-gated) | 31 of 230 FAIL (C "granted 0 while refused" + every G slope compare) |
| Admission verdict into the talker FSMs tied 1 (top wiring cut) | 5 of 230 FAIL (C: FAILED state, fail code/bridge, Talker Failed byte-exact; C2 swap-back) |

All three restored; suite back to 230/230 PASS.

Receive-side LeaveAll routing, mutation-proven 2026-09-23 (issue #106; each
arm planted, run, restored under a SHA-256 check). F2 and F4 flag every type
and pass under both the previous and the new routing; F5 separates them:

| Mutation | Result |
|---|---|
| The previous receive side (decoder, both FSMs, KL_srp_top, srp_pkg at the first #106 commit) | 5 of 252 FAIL (F5a, F5b, F5c) |
| Decoder strobes every lane at every flagged VectorHeader | 5 of 252 FAIL (F5a, F5b, F5c) |
| KL_srp_top broadcasts every lane to every plane | 5 of 252 FAIL (F5a, F5b, F5c) |
| Domain participant deaf to the Domain lane | 1 of 252 FAIL (F5b Domain re-declaration) |

The F5c Domain negative (PR #107 correction round 1), mutation-proven
2026-09-23 in a `git archive` export; the arm passed all 252 checks before it:

| Mutation | Result |
|---|---|
| Domain participant takes every MSRP lane (R270-1 X2, R271-1 R4) | 1 of 253 FAIL (F5c no Domain re-declaration) |

Its extension to the two talker lanes (PR #107 correction round 2),
mutation-proven 2026-09-24 in `git archive` exports with the reviewer's plants
verbatim; both arms passed all 253 checks before it:

| Mutation | Result |
|---|---|
| Domain participant also takes the Talker Advertise lane (R271-2 K13) | 1 of 255 FAIL (F5c Talker Advertise LeaveAll) |
| Domain participant also takes the Talker Failed lane (R271-2 K14) | 1 of 255 FAIL (F5c Talker Failed-only LeaveAll) |

FailureInformation change end to end (section D, issues #43/#49): after the
Advertise→Failed swap has drained, a Failed JoinIn with a changed code and
bridge raises `evt_tk_fail_chg_o` once and no EVT_TK_REGISTERED, latches the
new values, and puts NO Listener New on the wire for 800 ms; an unchanged
refresh strobes nothing. Mutation-proven 2026-09-24 in a scratch copy: folding
the change back into the registration indication → 3 of 259 FAIL (the strobe
count, the wire silence, and the unchanged-refresh count).

## Own LeaveAll at transmit acceptance (issue #127)

Timer expiry is only pending intent. The encoder reserves a transmit slot and
issues one `sLA` action, which ages both registrar arrays and starts both
applicant walks with `txLA!`. The tests observe real timer, decoder, allocation,
encoder and serialization handshakes; no DUT state or timer event is forced.
The wrapper can delay the slot pool's allocation request, and the BFM can delay
TX request acceptance. Read-only probes identify the action and decoded events.
The BFM waits until the clock after the serializer's final byte before requesting
another slot, matching the real serializer's return to idle.

| Group | Cases and oracle |
|---|---|
| K: expiry phase | Ready and Ready Failed on sources 0, 3 and 7, with three sources present. Leaves at -50, -1, +1, +40 and +80 ms from the real expiry clear IN and remain stopped for two seconds. At +120 and +199 ms, accepted sLA has legitimately entered LV, so rLv retains registration. Advertise and Failed sink Leaves follow the same phase sweep. |
| K: controls | Mismatched SID and malformed Listener Leave preserve IN; reset clears a blocked preparation; real LeaveTime expires both planes without renewal; timely rejoin preserves healthy registrations across the old deadline. |
| L: acceptance edge | Slot allocation is delayed while a real Listener Leave is decoded. Fourteen release positions for each Ready parameter cover decoded events from -8 through +5 clocks relative to sLA, including -1, 0 and +1. Receive priority clears IN before/on the edge; after it, LV retains registration. All unaffected registrars age once. |
| M: supersession | Each of the four MSRP types before preparation and while allocation is blocked cancels the pending own action. Rejoined registrars are never re-aged and no own flags appear. MVRP cannot cancel it. Since issue #108 an MSRP peer restarts the MSRP timer (a fresh 10-15 s deadline from the peer) and an MVRP peer leaves it unchanged (M4). Six peer/acceptance phases cover -2 through +3 clocks: the peer wins before/on acceptance, and cannot retract an accepted action. A peer from -12 to +1 clocks around real timer expiry leaves no own action: on or after the expiry it drops the new intent, and before it the restart makes that expiry stale (M10; before #108 the -1 case still acted). The sweep crosses rLA!'s draw request, the PRNG's rejection retries and the arm of the restarted deadline, and M9 grades each placement against the calibrated expiry clock, because once the restarted deadline is armed the superseded one never fires. A quiet canceled round waits for real content; a later own action can reuse its reserved slot. |
| N: congestion | Eight sources and eight sinks exceed the 12-entry table. A previous TX request stalls across several cadence ticks; Leaves still clear IN. After acceptance, a held TX request never repeats sLA. Interim and final drains preserve all live declarations and all four type flags, and queued ticks complete. Another case fills the table before acceptance and proves that this initial full condition also drains. Allocation held across two timer expiries produces just one accepted own action. An asymmetric eight-source/one-sink walk preserves the completed walker across blocked cadence ticks. |

The existing periodic-declaration and six-cycle/no-storm assertions retain their
limits. The measured six-cycle counts were 4, 3, 3, 3, 3, 2 (18 total, maximum 4).
Since issue #108 each peer LeaveAll restarts the timer, no own burst lands in
F4, and the counts are 4, 3, 3, 3, 2, 2 (pinned 17 total, maximum 4).
The accepted action precedes serialization; a Leave after that legitimate LV
entry may still retain registration for LeaveTime. This change does not impose
a stricter LV + rLv policy. The receive-timer restart is issue #108, below.

Run the mutation campaign with:

```sh
make -C tb/srp_top mutants MUTANT_OUTPUT=/tmp/srp-leaveall-mutants
```

The `mutants` target runs the complete campaign and is invoked by the HDL
workflow. `MUTANT_OUTPUT` selects the receipt directory; the default is shown
above. Plain `make` still runs the positive suite. The patch files retain their
unified-diff context verbatim; `.gitattributes` exempts only those files from
blank-at-end-of-line and blank-at-end-of-file whitespace checks.

`python3 tb/srp_top/mutants.py --output DIR [--only a,b] [--jobs N]` runs the
campaign directly: `--jobs N` (default 4, the meaning and default of
`tb/pp_top/d3_mutants.py`; the `mutants` target runs the default) builds and
runs up to N copies at once, and the results are printed in the declared order
whatever order they finish in. A label graded on two suites keeps one receipt,
the later row's, as a serial run leaves it. Measured 2026-10-02 at `85da751`
with Verilator 5.050, each run pinned to 4 of the host's 16 CPUs: `--jobs 1`
took 2,258 s and `--jobs 8` 1,099 s. All 89 runs (11 controls, 78 arm runs)
gave the same verdict and the same failing checks in both, and both ended
`90 checks: 90 PASS, 0 FAIL` with assertion coverage 65/65.

Each control and deliberate RTL defect builds in a temporary source copy of its
own. A mutation counts only when a simulation finishes with a nonzero result and
its named assertion fails; compilation failures and timeouts do not count.
The driver applies checked-in unified patches with `git apply --check` in a
fresh scratch RTL copy; it never reads DUT source to derive an oracle. Only
simulation logs are read. Original source integrity is recorded in the review
packet. `srp_top` stops at 300,000,000 DUT clocks (raised from 200,000,000
when the P8 arm-delay sweep brought the complete run to 185,012,669); the
encoder and stream-FSM
walks use finite cycle bounds. Budget exits and missing tallies are unproven,
not kills. `RUN_ARGS=phases`, `edge`, `peer`, `congestion`, `guards`,
`armdelay`, `restart`, `timers`, `join` or `lvleave` selects one group for a focused run,
`RUN_ARGS=storage` the timer-arm FIFO arms; plain `make` runs every existing and
new check. The stream-FSM suite independently walks every
applicant state with same-edge sLA/join acceptance.

Round 1 measurement: all five positive controls pass; all 36
mutation runs finish with the required named assertion failing. Restoring the
timer-expiry registrar pulse causes 81 failures. The union of killed assertions
covers all 41 new integration check families (K1–K12, L1–L4, M1–M12, N1–N13).
Both same-edge applicant tables are also mutation-proven. The complete campaign
returns 0 (42/42 checks), and the mutated RTL source hashes remain unchanged.
Build errors and timeouts are never counted as kills.

| Deliberate breakage | Group | Failing checks | Named failing assertions |
|---|---|---:|---|
| `bad-listener-length` | phases | 1 | K12 |
| `peer-restarts-timer` | peer | 8 | M4 |
| `repeated-action` | congestion | 5 | N10, N12, N13, N4, N8 |
| `expiry-event` | phases | 81 | K1, K11, K12, K2, K4, K5, K9 |
| `before-slot` | edge | 30 | L1, L4 |
| `talker-no-own` | phases | 25 | K2, K4, K8 |
| `listener-no-own` | phases | 13 | K11, K6 |
| `talker-lost-txla` | stream FSMs | 12 | same-edge Table 10-3 states/messages |
| `listener-lost-txla` | stream FSMs | 12 | same-edge Table 10-3 states/messages |
| `talker-strict-lv` | phases | 24 | K2, K4 |
| `listener-strict-lv` | phases | 13 | K11, K6 |
| `listener-sid-ignored` | phases | 33 | K12, K3, K5, K8 |
| `talker-no-renewal` | phases | 1 | K7 |
| `listener-no-renewal` | phases | 1 | K7 |
| `talker-no-expiry` | phases | 1 | K8 |
| `listener-no-expiry` | phases | 1 | K8 |
| `pending-peer-ignored` | peer | 14 | M1, M10, M2, M3 |
| `encoder-peer-ignored` | peer | 20 | M1, M11, M12, M2, M3, M6, M7 |
| `mvrp-supersedes-msrp` | peer | 6 | M1, M2, M3 |
| `reset-retains-intent` | phases | 1 | K10 |
| `full-drain-missing` | congestion | 7 | N10, N13, N3, N4, N5, N6, N8 |
| `already-full-missed` | congestion | 1 | N10 |
| `round-completion-lost` | congestion | 1 | N13 |
| `own-flags-missing` | congestion | 4 | N10, N12, N5, N6 |
| `expiry-congestion` | congestion | 5 | N1, N11, N12, N2, N9 |
| `missing-registrar-edge` | edge | 38 | L2, L3 |
| `empty-canceled-pdu` | peer | 1 | M11 |
| `reserved-slot-not-reused` | peer | 1 | M12 |
| `renewal-congestion` | congestion | 1 | N7 |
| `leaveall-expiry-lost` | peer | 18 | M1, M10, M12, M2, M3, M5, M8, M9 |
| `expiry-outranks-peer` | peer | 1 | M10 |
| `repeated-expiry-queued` | congestion | 1 | N12 |
| `receive-priority-lost` | edge | 2 | L2 |
| `action-omitted` | congestion | 6 | N10, N12, N13, N3, N4, N8 |
| `preparation-before-slot` | peer | 22 | M1, M10, M11, M12, M5, M6, M8 |
| `table-one-short` | congestion | 8 | N10, N13, N3, N4, N5, N6, N8, N9 |


## Round 2: pending-action guards

The default suite includes 73 additional checks; no DUT event is forced.
Reset edges are excluded from the event history because synchronous reset can
interrupt a combinational preparation acceptance without performing an action.

| Check | Stimulus and required behavior |
|---|---|
| O1 | A peer Domain LeaveAll while preparation waits behind a held encoder TX request cancels the eventual action and its wire flags. |
| O2 | After cancellation, a second real timer expiry while allocation remains blocked survives the canceled acceptance and produces exactly one own action/frame. |
| O3 | Peer Domain LeaveAll decoded at -1/0/+1 clocks around the join opportunity cancels before acceptance; both registrar planes remain IN. |
| O4 | With the link down, reuse a retained empty reservation; peer decode at -1/0/+1 around reuse acceptance permits wire flags only when the local action preceded the peer. The exact acceptance clock is checked separately. |
| O5 | Talker Advertise and Failed Leaves on sinks 0 and 7 decode at -1/0/+1 around acceptance. Before/on the edge they clear IN; afterward they retain LV. |
| O6 | Several cadence ticks during blocked preparation produce exactly one immediate follow-up walk after acceptance, before another cadence tick. |
| O7 | A canceled Domain-only round holds its empty reservation for periodic content; with the link up it drains within Periodic plus Join (measured 649 ms, test bound 1200 ms). |
| O8 (encoder suite) | An MVRP join tick and VID push coincide with MSRP preparation. MVRP intake remains open, and the deferred drain emits both VIDs without another tick. |

The reserved handle cannot be released through the current TX interface, which
has no abort operation. It holds one of the shared standard slots and blocks
this encoder's MVRP drains. The link-up bound assumes eventual TX acceptance.
With the link down it waits for link-up content or the next unsuperseded own
action; repeated peer cancellation or external backpressure can extend this
without a finite bound. See [10 section 6.5](../../docs/architecture/10_srp_engine.md#65-leaveall-and-the-δ13-registrar-deviation).

The round-2 campaign reproduces the 36 measurements above and adds all 19
reviewer arms (including aliases for the same edit) plus an empty-reservation
drain arm. All seven controls pass, all 56 arms are killed by their required
named assertions, and all 49 integration assertion families K1–O8 are covered:
`64 checks: 64 PASS, 0 FAIL`, driver rc 0. Stream-FSM control is 1215/1215;
encoder control is 562/562. The required new reviewer edits are measured below.

| Deliberate breakage | Group | Failing checks | Named failing assertions |
|---|---|---:|---|
| `my-expiry-pulse` | phases | 62 | K11,K12,K2,K4,K5 |
| `my-join-edge-peer` | guards | 2 | O3,O4 |
| `my-cancel-eats-new-intent` | guards | 1 | O2 |
| `my-edge-cancel-lost` | peer | 2 | M6,M7 |
| `my-la-outranks-leave` | edge | 2 | L2 |
| `my-drop-join-during-wait` | guards | 1 | O6 |
| `my-no-walk-at-sLA` | congestion | 5 | N10,N12,N13,N5,N6 |
| `my-reuse-flags-ignore-cancel` | guards | 1 | O4 |
| `r-expiry-pulse-restored` | phases | 62 | K11,K12,K2,K4,K5 |
| `r-cancel-latch-dropped` | guards | 1 | O1 |
| `r-cancel-consumes-new-intent` | guards | 1 | O2 |
| `r-join-start-guard-dropped` | guards | 2 | O3,O4 |
| `r-sink-receive-priority-lost` | guards | 2 | O5 |
| `r-join-coalesce-dropped` | guards | 1 | O6 |
| `r-la-only-emission-lost` | peer | 1 | M12 |
| `r-collect-blocks-pushes` | congestion | 4 | N12,N13,N5,N6 |
| `r-accept-edge-drain-lost` | congestion | 1 | N10 |
| `r-reuse-without-action` | peer | 1 | M12 |
| `r-mvrp-start-during-prepare` | srp_encoder | 5 | B1-vlan,O8 |
| `canceled-content-never-drains` | guards | 1 | O7 |

## Received LeaveAll restarts the leavealltimer (issue #108)

802.1Q-2014 Table 10-5 maps rLA! to "Start leavealltimer, Passive" in both
states, and 10.6 says why: a LeaveAll received from another participant
restarts the timer "without generating a message". The LeaveAll machine is per
application (10.7.5.20 NOTE), so a lane of any of its Attribute Types is its
rLA! (10.7.5.20 b)2)): any MSRP lane for MSRP, the VID lane for MVRP, never
across ([10 section 6.5](../../docs/architecture/10_srp_engine.md#fig-10-leaveall)).
`RUN_ARGS=restart` runs the group. Read-only probes add the MVRP deadline,
pending flag, expiry, flag hand-off, decoded MVRP lane and draw requests; no
DUT state is forced.

| Check | Stimulus and required behavior |
|---|---|
| P1 | F4's bridge shape (LeaveAll on every MSRP type, riding its re-declarations) every second for 20 cycles, past the 15 s ceiling of any draw: no own MSRP action and no flagged own MRPDU; every peer restarts the deadline to 10-15 s after it; MVRP keeps its own cycle; registrations stay IN. After the last peer the own LeaveAll follows 10-15 s later (measured +11092 ms). |
| P2 | The same for MVRP (peer VID 2 JoinIn flagged): no own MVRP flag in 20 cycles; MSRP keeps its own cycle; no VID Lv. |
| P3 | Each lane (MVRP, then MSRP types 1-4) 5 s before the earlier own deadline: only its application's deadline is redrawn from the peer. The superseded deadline passes silently; the restarted one fires once, 10 s or more after the peer (measured 13.2-14.0 s). |
| P4 | MVRP Active: right after the own MVRP expiry, a peer MVRP LeaveAll drops the pending flag, the VID re-join still goes out, and the timer restarts. Control without the peer: the flag rides the next drain. |
| P5 | MVRP Active with no VID held (no drain carries the flag): a peer MVRP LeaveAll makes it Passive, so the first VID New carries no own flag. Control: the flag rides that New. |
| P6 | The MVRP lane from -12 to +1 clocks around the real MVRP expiry: no own flag in any case, and a restarted timer (before the expiry the superseded deadline is stale, or never fires once the restarted one is armed). |
| P7 | The MVRP equal edge: after the own MVRP expiry the flag waits for the next MVRP join tick whose drain has content. A peer MVRP LeaveAll at -1 or 0 clocks of that tick drops it (Passive; the rider skips the flag on the peer's edge), at +1 the tick was tx! and the accepted own flag goes out. The timer restarts in all three. |
| P8 (`RUN_ARGS=armdelay`) | The committed form of the reviewer's delayed-arm probe. The wrapper delays the engine's timer arms by `arm_delay_i` clocks, as the processor top's queued arm port does. At delays 3, 4, 8 and 16, one reset scenario per offset puts a peer MVRP LeaveAll around the own MVRP expiry, then a peer MSRP (Domain) LeaveAll around the own MSRP expiry, each from -(delay + 12) to +2 clocks: no offset produces an own LeaveAll of either application, every peer lands at its offset and restarts its application's timer. |

The MSRP twin of P6 is M10. Mutation-proven 2026-09-29 through `mutants.py`
(checked-in patches, each built in a scratch RTL copy):

| Deliberate breakage | Group | Failing checks | Named failing assertions |
|---|---|---:|---|
| `expiry-only-redraw` (MSRP peer does not restart the timer) | restart | 15 | P1,P3 |
| `mvrp-expiry-only-redraw` (MVRP peer does not restart the timer) | restart | 6 | P2,P3,P6 |
| `stale-expiry-honoured` (MSRP superseded deadline acts) | peer | 1 | M10 |
| `mvrp-stale-expiry-honoured` (MVRP superseded deadline acts) | restart | 1 | P6 |
| `mvrp-passive-lost` (MVRP peer keeps the own flag) | restart | 4 | P4,P5,P6 |
| `mvrp-flag-at-expiry` (flag handed to the encoder at expiry, the old shape) | restart | 6 | P4,P5,P6 |

The round-1 arm `peer-restarts-timer` planted exactly the behavior #108
requires, so it is retired. Five arms whose context the change moved
(`expiry-outranks-peer`, `mvrp-supersedes-msrp`, `pending-peer-ignored`,
`reset-retains-intent`, `my-expiry-pulse`) are regenerated with the same edit and
re-measured: 1 (M10), 8 (M1-M4), 15 (M1, M2, M3, M10), 1 (K10) and 62 (K2, K4,
K5, K11, K12) failing checks.

### A stale expiry whatever the arm-path latency

The first guard treated a LeaveAll-slot expiry as stale until the restarted
deadline's arm was *issued*. Here that arm reaches the timer service on the
same clock, but the processor top queues it behind other faces, and with more
than two clocks of arm latency the superseded deadline could still fire after
the issue and act: one own LeaveAll right after the peer's. The guard now holds
while a draw is outstanding or `now_ms` is before the deadline the draw produced
([10 section 6.5](../../docs/architecture/10_srp_engine.md#fig-10-leaveall)).
M10 and P6 were widened from -1/0/+1 to -12..+1 clocks, P7 is the MVRP equal
edge and P8 the arm-delay sweep (table above). Mutation-proven 2026-09-29 through
`mutants.py`:

| Deliberate breakage | Group | Failing checks | Named failing assertions |
|---|---|---:|---|
| `rearm-at-issue` (the issue-time guard restored: stale only until the arm is issued) | armdelay | 8 | P8 |
| `r-rearm-no-inflight` (no stale window while the draw is in flight) | peer / restart | 3 / 6 | M10 / P6 |
| `r-rearm-no-deadline` (no stale window between the draw and the restarted deadline) | peer / armdelay | 3 / 8 | M10 / P8 |
| `r-flag-ignores-edge-peer` (the MVRP flag rides a join tick that meets a peer MVRP LeaveAll) | restart | 1 | P7 |

`rearm-at-issue` leaves M10 and P6 green: on the direct arm path the issue-time
guard holds. Under it P8 counts an own MSRP LeaveAll at 4, 4, 7 and 15 offsets
for delays 3, 4, 8 and 16 (peer -11..-8, -11..-8, -14..-8 and -22..-8 clocks
before the expiry), and an own MVRP LeaveAll at 2, 2, 6 and 14. At delay 0, M10
needs the guard from -7 to -1 clocks (the draw request at -1, the draw in flight
to -4, the restarted deadline to -7), and P6 from -7 to -1 (the MVRP draw in
flight to -7). `draw-kind-0` is
regenerated with the same edit (its context moved) and still fails 6 checks (Q1-Q4).
The widened sweeps and P7 re-measure these arms: `mvrp-expiry-only-redraw` 17
(P2, P3, P6), `stale-expiry-honoured` 7 (M10), `mvrp-stale-expiry-honoured` 7 (P6),
`mvrp-passive-lost` 6 (P4-P7), `mvrp-flag-at-expiry` 11 (P4-P7),
`pending-peer-ignored` 26 (M1, M2, M3, M10), `leaveall-expiry-lost` 16 (M1, M2,
M3, M5, M8, M9, M12) and `preparation-before-slot` 21 (M1, M5, M6, M8, M11, M12).

## MRP timers graded against Milan v1.2 Table 4.3 (issue #64, REQ-SRP-001)

Every captured MRPDU carries `now_ms_o` at its last byte (`archive_ms`), and the
BFM clock that accepted its request (`archive_accept`). `RUN_ARGS=timers` runs
one bring-up from reset: Begin! arms both leavealltimers at reset release, a
talker declaration on VID 2 in a clean slot, then 52 s with no peer LeaveAll,
then one peer LeaveAll per application. Only MRPDU spacing is graded, never a
DUT register.

| Check | Timer (Table 4.3 range) | Measured |
|---|---|---|
| Q1 | joinTime 180-240 ms: the Table 10-3 ladder New, New, JoinMt of one fresh declaration is one MRPDU per T-MRP-JOIN tick | 200, 200 ms |
| Q2 | periodictimer 900-1500 ms: a quiet declared Talker Advertise re-joins (JoinMt) on each periodic!, and so do the Domain and the MVRP VID (JoinIn); at least five of each before the first LeaveAll | 9 x 1000 ms each |
| Q3 | leavealltimer 10-15 s: the first own MSRP and MVRP LeaveAll no earlier than 10 s after arming, and consecutive own LeaveAlls 10-15 s apart, at least three per application | first +14206 / +10601 ms; MSRP 10000-12800 ms, MVRP 11000-13200 ms |
| Q4 | issue #108 on the wire: a peer LeaveAll 5 s after the latest own one restarts the timer, so the next own LeaveAll of that application comes 10-15 s after the peer's | MSRP +11000 ms, MVRP +14495 ms |

The own MSRP LeaveAll rides the first join opportunity after the expiry, so
its MRPDUs sit on the T-MRP-JOIN grid; with a 10-15 s draw their spacing stays
inside 10-15 s (the Q3 minimum is exactly one 10 s draw). Milan's own tolerance
is wider (9.5-15.5 s).

Mutation-proven 2026-09-29 through `mutants.py` (checked-in patches):

| Deliberate breakage | Group | Failing checks | Named failing assertions |
|---|---|---:|---|
| `join-ms-400` (`JOIN_MS_P = 400`) | timers | 2 | Q1,Q2 |
| `periodic-ms-3000` (`PERIODIC_MS_P = 3000`) | timers | 1 | Q2 |
| `draw-kind-0` (`draw_kind_o = 3'd0`, the 0-1 s range) | timers | 6 | Q1,Q2,Q3,Q4 |

## MVRP join before the stream (issue #65, REQ-SRP-006)

Milan v1.2 4.3.2: a Talker PAAD "shall join the relevant VLAN via MVRP prior to
sending any Stream frames"; 4.4.1: a Listener PAAD "shall declare an MVRP VID
attribute for each VLAN used by its settled sinks". ACTIVE, the streaming
licence, now also requires the source VID's MVRP declaration to have left: the
encoder strobes every MVRP MRPDU the TX arbiter accepts, and KL_srp_vlan marks
which live VIDs it carried ([10 section 6.2](../../docs/architecture/10_srp_engine.md#sec-10-join-before-stream)).
An MRPDU counts as transmitted at the clock the BFM accepted its request.
`RUN_ARGS=join` runs the group.

| Check | Stimulus and required behavior |
|---|---|
| R1 | DECLARE_TALKER on VID 2, then a Listener Ready at 1 ms, before the first join tick: registered, admitted, not ACTIVE. ACTIVE rises 1 clock after the BFM accepts the VID 2 New (measured at 200 ms), within one join-paced MRPDU. The VID New is accepted ahead of the first Talker Advertise, so a Ready that answers the Advertise never waits. |
| R2 | A second source on VID 2, already joined: ACTIVE as soon as its Ready registers. |
| R3 | Source 0 withdrawn and re-declared on VID 7 with a new Ready: no ACTIVE until VID 7's own New is accepted; VID 2 stays declared for source 1 (no Lv). |
| R4 | DECLARE_LISTENER sink 0 on VID 7, which no source holds: byte-exact MVRP VID 7 New, then JoinIn every 900-1500 ms (3 x 1000 ms measured), and WITHDRAW_LISTENER of its last user: byte-exact MVRP VID 7 Lv, no membership left. |

H and I (issue #112) registered a Listener Ready about 2 ms after reset,
before VID 2's MVRP join could leave: exactly the #65 case, so 184 of their
checks fail against the gated licence (96 H, 88 I). Each case now waits 250 ms
after its first declaration and asserts that VID 2's join was captured (24 + 88
new checks); every LATENCY, CROSS and WINDOW measurement line is byte-identical
to the one before the change.

Mutation-proven 2026-09-29 through `mutants.py` (checked-in patches):

| Deliberate breakage | Suite / group | Failing checks | Named failing assertions |
|---|---|---:|---|
| `licence-ignores-join` (talker ACTIVE without the VID term) | srp_top join | 3 | R1,R3 |
| `licence-ignores-join` | srp_stream_fsms | 3 | the three VID-term checks |
| `join-sent-at-handover` (VLAN marks a VID sent when the encoder takes its New) | srp_top join | 3 | R1,R3 |
| `join-sent-at-handover` | srp_encoder | 3 | W2,W3,W4 |
| `count-up-unsends` (a second user resets the VID's sent state) | srp_top join | 3 | R2,R3 |
| `count-up-unsends` | srp_encoder | 2 | W4 |
| `tx-strobe-any-app` (the transmission strobe also fires for MSRP) | srp_encoder | 1 | W1 |
| `listener-lane-cut` (`vu_sel_ls_w` forced 0, the #65 acceptance arm) | srp_top join | 3 | R4 |

## A withdrawal that meets an LV registrar (issue #134)

The bench case of milan-fpga #608 (cycle 22): the DUT's own LeaveAll crossed the wire
1.390 ms before the bridge's `Lv` for a stream whose listener had withdrawn. The Listener
registrar for that stream was already LV, so the talker streamed on through the 2 s hold.
802.1Q-2014 Table 10-4 puts rLv!, rLA! and txLA! in one row: in IN it starts the leavetimer
and enters LV, and in LV it is `-x-`. leavetimer! in LV is Lv and MT. Milan v1.2 4.2.7.2.2
(Δ13) replaces only the IN cell. So the `Lv` changes nothing, and the registration and
ACTIVE end when the leave timer expires, including a decoded `Lv` on that same clock.
The expiry is applied first; a same-clock New or Join instead finishes IN with the
new registration, as Table 10-4 at MT requires
([10 section 6.5](../../docs/architecture/10_srp_engine.md#sec-10-lv-withdrawal)).
`RUN_ARGS=lvleave` runs the group.

Each case starts from `leaveall_setup`: sources 0, 3 and 7 declared, each registering a
Listener Ready (or ReadyFailed) and ACTIVE, and sinks 0 and 7 registered. Eight cases: an
own and a peer LeaveAll, Ready and ReadyFailed, target source 0 and 7.

- **Own LeaveAll.** The real leavealltimer expires and the accepted `sLA` ages every
  registrar. 1.390 ms (56 clocks) after the LeaveAll MRPDU's last byte, the bridge answers
  with one MRPDU: JoinIn for every other registration, and `Lv` for the target.
- **Peer LeaveAll.** The bridge's LeaveAll on every MSRP type, Listener first, re-joining
  every registration but the target's. 1.390 ms later, its `Lv` for the target.

In both, the bridge repeats the target's `Lv` 2.5 s after the LeaveAll. The harness counts
every edge of ACTIVE, as the integrator's STREAM_START and STREAM_STOP counters do
([02 section 4.6](../../docs/architecture/02_interfaces.md)), and every `LISTENER_REG_CHANGE`
strobe, on every clock. No DUT state is forced; `dbg_t_reg_o` is read only.

| Check | Stimulus and required behavior |
|---|---|
| S1 | The LeaveAll (one `sLA`, or the peer's Listener lane with no own action) has put the target's registrar in LV, and both `Lv`s find it LV and leave it LV. Up to the last ms before the leave timer can expire, the registration is published (Ready or ReadyFailed), ACTIVE is high, and the case has seen no ACTIVE edge and no `LISTENER_REG_CHANGE` |
| S2 | The leave timer's expiry closes them: ACTIVE falls and `LISTENER_REG_CHANGE` strobes 5000 or 5001 ms after the LeaveAll, and the registrar is MT with `lstn_reg_state` 0. The 1 ms of slack is the arm's deadline, T-MRP-LEAVE from the clock the arm issues, which can fall in the next ms |
| S3 | 2 s after that: exactly one STREAM_STOP and no STREAM_START over the case, and one `LISTENER_REG_CHANGE` |

The leave timer is `KL_srp_top`'s `LEAVE_MS_P`, 5000 ms (F08.1 T-MRP-LEAVE, unchanged by the
processor top). Milan v1.2 Table 4.3 LeaveTime: default 5000 ms, tolerance +50 %/-10 %, so
4500 to 7500 ms. Each case prints one `LV_LEAVE` line. Measured at the head: the own
LeaveAll at 14200 ms, the first `Lv` decoded by 14216 ms, the second by 16700 ms, the close at
19200 ms; the peer LeaveAll at 705 ms, the `Lv`s by 711 and 3205 ms, the close at 5705 ms. The
leave time is 5000 ms in all eight cases, one STREAM_STOP and no STREAM_START in each.

Mutation-proven 2026-10-05 with the checked-in patches, each planted separately and
run through the complete default `make -C tb/srp_top` (8656 checks). `lv-second-lv-ends`
fails only the 16 S1/S2 checks. `lv-never-ends` fails the 16 S2/S3 checks plus 3016 SC2
checks in `lvcoll`, for 3032 failures:

| Deliberate breakage | Group | Failing checks | Named failing assertions |
|---|---|---:|---|
| `lv-second-lv-ends` (the registrar lets one `Lv` in LV pass and ends the registration on the second) | lvleave | 16 | S1,S2 |
| `lv-never-ends` (an `Lv` in LV stops the leave timer, so the registration never ends) | lvleave | 16 | S2,S3 |
| `lv-never-ends` (the same planted patch, in the same default run) | lvcoll | 3016 | SC2 |

The older one-line forms of the same two defects, `talker-strict-lv` (an `Lv` in LV ends the
registration at once) and `talker-no-expiry` (no leave-timer expiry reaches the talker
registrar), are campaign rows of the phases group. Run through this group they fail 16 checks
each, S1,S2 and S2,S3, closing after 14 or 5 ms and never.

### Same-clock leave expiry (round 2)

`RUN_ARGS=lvcoll` is also part of the default run. It contains 6,416 byte-stream
cases: k = 0..400, both planes, own/peer LeaveAll, Ready/ReadyFailed, index 0/7.
Sink 0 holds Advertise and sink 7 holds Failed. Both target registrars age;
only the selected plane receives the `Lv` near expiry. The listener plane has no
ACTIVE face: its matching TK_UNREGISTERED is graded alongside the source's
STREAM_STOP in every case.

A no-`Lv` calibration measures each plane's close clock. Each offset restores
identical DUT and BFM state saved 401 clocks before that clock, then starts a real
MRPDU k clocks before it. The shared prefix uses the real own/peer LeaveAll and
5000 ms timer. All clocks around decoding, expiry and publication execute, followed
by a 20 ms observation window. The run counter includes every executed replay
clock; the snapshot lives outside the tree and is removed after the sweep.

| Check | Required result | Planted fault that fails it |
|---|---|---|
| SC1 (`srp_stream_fsms`) | 128 simultaneous-event cases match Table 10-4, expiry first, including indications and timer operations | `lv-expiry-masked` 16 failures; `lv-expiry-last` 48; `lv-expiry-dropped` 80 SC1 failures |
| SC2 | Every k ends with both registrars MT, both registrations absent, ACTIVE low, one STREAM_STOP and one TK_UNREGISTERED | `lv-expiry-masked` restores both original planes: 16 failures, one collision in each combination |
| SC3 | Exactly one decoded `Lv` in each sweep shares the calibrated expiry clock | `lv-sweep-misses-collision` delays every frame 401 clocks: all 16 checks fail while SC2 stays green |

The restoration mutant is a checked-in reverse patch of the complete RTL change.
The two original mutants and S1-S3 remain. The two other matrix faults move expiry
after reception (so a registering event wrongly ends MT) and discard expiry
(so Lv/LA/In/Mt wrongly leave LV). Every new check fails under at least one fault.
The full campaign requires SC1-SC3 as well as the original assertion coverage.

Table 10-4 results after LV / leavetimer!: MT + Lv, then:

| Same-clock event | Final state | Published result |
|---|---|---|
| rLv | MT | Registration closes once |
| rLA / own txLA | MT | Registration closes once; no replacement leave ARM |
| rIn / rMt | MT | Registration closes once |
| rNew | IN | Received value registered; obsolete timer canceled |
| rJoinIn / rJoinMt | IN | Received value registered; obsolete timer canceled |

Both planes publish the final result of the composed transitions. A registering
event preserves the published registration; it emits no intermediate withdrawal
or ACTIVE edge. The listener retains its existing type-change, latency and
FailureInformation notifications for the received value. Separate REGISTERED and
UNREGISTERED pulses would enter independent event-router queues with no ordering
guarantee, so renewal must not publish a transient withdrawal.

## Timer-arm FIFOs at four shapes (issue #230)

Each stream FSM's timer ops reach the one merged arm port through a FIFO of its
own: 32 words of distributed RAM since issue #230
([10 §5.1](../../docs/architecture/10_srp_engine.md)), issued round-robin, one
word every two clocks. `store_main.cpp` checks them on the real engine and its
real services (`srp_store_wrap.sv`, time-compressed as above) at sources/sinks
1/1, 2/2, 3/5 and 9/9. A scoreboard reads both FSMs' arm faces (what each FIFO
is offered) and the merged face (what leaves) through read-only probes, and
holds the FIFO contract: every op an FSM offers leaves the merged face exactly
once, in that FSM's order and unmodified, except an op offered while its FIFO
holds 32 words, which the full guard refuses.

The first arm brings every source and sink up with a registration from the
peer and waits for an own LeaveAll. Its sLA ages both registrar arrays in one
clock, so both FSMs offer an op in the same clock (checked). On a LeaveAll clock
where the round-robin serves the listener FIFO first, a re-declaration of
source 0 is accepted, and its gate op cancels the leave timer that LeaveAll just
started. The talker FIFO therefore holds two words when the merged face selects
it (checked). On a LeaveAll where the round-robin points at the talker FIFO, the
peer re-joins all but source 0, whose leave timer runs out instead. That makes
an odd number of issues, so the next LeaveAll finds the listener FIFO first. At
every shape the second LeaveAll is the one.

The second arm reaches the full guard, which no port sequence reaches: the issue
drains a word every two clocks, and the registrar walks offer at most one op per
source or sink. `srp_store_wrap` holds the merged issue in TM_SEL while
`tm_stall_i` is high: **the one forced state in these arms**, and only in this
arm. Peer LeaveAll MRPDUs then offer each FIFO two ops per stream (the LeaveAll
ages, the re-join cancels) until each has been offered 36. Then the stall is
released.

| Check | What it proves |
|---|---|
| TF1 | the talker FIFO issues every op it accepted once, in its order and unmodified: no word lost, reordered, altered, duplicated or invented, and every queued word drains |
| TF2 | the same for the listener FIFO |
| TF3 | no op is refused while the issue runs unforced |
| TF4 | held, the talker FIFO accepts exactly 32 ops and refuses the rest; released, it issues those 32 in order, unmodified |
| TF5 | the same for the listener FIFO |

Preconditions are checks too: every registrar IN before each arm, an own
LeaveAll within 16 s, both FSMs offering in one clock, the re-declaration on a
LeaveAll clock, a two-word talker FIFO at a selection, more than 32 offers per
FIFO while held, and no FSM op issued while held. `make RUN_ARGS=storage` runs
these arms alone. Every part runs even after a failing one, and every failing
check names its shape (`[sources/sinks]`). Measured at the head, 15 checks at
each shape, all PASS:

| Shape | First arm: offered (= issued), talker / listener | Clocks with both offering | Two-word selections, talker / listener | Held arm: MRPDUs, offered, refused |
|---|---|---:|---|---|
| 1/1 | 3 / 4 | 2 | 1 / 0 | 18; 36 / 36; 4 / 4 |
| 2/2 | 7 / 8 | 4 | 2 / 1 | 9; 36 / 36; 4 / 4 |
| 3/5 | 11 / 20 | 7 | 4 / 7 | 6; 36 / 60; 4 / 28 |
| 9/9 | 35 / 36 | 18 | 19 / 15 | 2; 36 / 36; 4 / 4 |

The build waives three Verilator warnings for this wrap alone (the Makefile
says which and why). Verilator 5.050 faults on a hierarchical reference to
`KL_srp_top`'s enum item `TM_SEL`, so the wrap names its encoding (1'b0).

## Issue #230 storage controls

The probes of both #230 reviews (R458-1 `lockstep/probes.py` and R458-3's two
ready-handshake probes, R459-1 `make_controls.py` and its stall probe) and the
lane's own lockstep controls are killed controls of `mutants.py`, one
checked-in patch per distinct edit: 35 patches, where a probe and a control with
the same edit share one. The new arms carry no group of the suite above:
`storage` runs the FIFO arms, `walk` the
[walk-record arms](../srp_stream_fsms/README.md#walk-records-at-both-elaboration-arms-issue-230),
and the slope controls run the [admission suite](../srp_admission/README.md) at
its five shapes. The assertion-coverage check now also requires TF1-TF5 and
WK1-WK10.

Failing checks per shape, from the campaign's receipts. "n/e": the edited arm
is not elaborated at that shape. "equivalent": with one source or one sink the
edit changes nothing (it names source or sink 0, the only one). "equivalent in
simulation": at one sink the parked control index (WK6) is the face's only
out-of-range value, and Verilator reads a single 64-bit packed element at an
out-of-range index as element 0, so the edit reads sink 0 there too; the 48-bit
DA of `wid-flops-da-of-gate-source` does not alias, and that edit is caught at
1/1.

| Control | From | Edit | Named failing checks | 1/1 | 2/2 | 3/5 | 9/9 | Caught at |
|---|---|---|---|---:|---:|---:|---:|---|
| `tf-heads-swapped` | A523, R458-1 | each FIFO head reads the other FIFO's memory | TF1, TF2 | 2 | 2 | 2 | 2 | 4 of 4 |
| `tf-head-at-write-pointer` | A523 | talker head read at `wptr - 1`, the newest word | TF1, TF4 | 2 | 2 | 2 | 2 | 4 of 4 |
| `tf-listener-push-dropped` | A523 | listener push lost when both FSMs push | TF2 | 1 | 1 | 1 | 1 | 4 of 4 |
| `tf-ls-written-at-tk-pointer` | R458-1 | listener word written at the talker's write pointer | TF2, TF5 | 2 | 2 | 2 | 2 | 4 of 4 |
| `tf-tk-head-read-ahead` | R458-1, R459-1 (`tf-tk-head-reads-next`) | talker head read at `rptr + 1` | TF1, TF4 | 4 | 4 | 3 | 2 | 4 of 4 |
| `tf-ls-head-reads-tk-ram` | R459-1 | listener head reads the talker memory | TF1, TF2, TF3, TF4, TF5 | 4 | 4 | 4 | 5 | 4 of 4 |
| `tf-tk-write-at-rptr` | R459-1 | talker word written at the read pointer | TF1, TF4 | 2 | 2 | 2 | 2 | 4 of 4 |
| `tf-full-guard-31` | R458-1 | talker full guard at 31 words | TF4 | 1 | 1 | 1 | 1 | 4 of 4 |
| `tf-tk-write-ignores-full` | R459-1 (stall probe) | talker memory written while full | TF4 | 1 | 1 | 1 | 1 | 4 of 4 |
| `tf-ls-write-ignores-full` | R459-1 | listener memory written while full | TF5 | 1 | 1 | 1 | 1 | 4 of 4 |
| `walk-record-written-on-close` | A523, R459-1 (`wtsp-written-on-close`) | walk records also written by a gate close | WK3 | 1 | 1 | 1 | 1 | 4 of 4 |
| `wtsp-first-open-only` | A523, R458-1 | walk TSpec written only by a source's first open | WK2, WK3, WK4, WK9 | 4 | 6 | 8 | 20 | 4 of 4 |
| `wtsp-read-at-gate-source` | A523, R458-1 | walk TSpec read at the gate source | WK1, WK2, WK4, WK9 | 1 | 6 | 13 | 49 | 4 of 4 |
| `wtsp-read-at-source-0` | R459-1 | walk TSpec read at source 0 | WK1, WK2, WK3, WK4, WK5, WK9 | 0 (equivalent) | 8 | 14 | 50 | 3 of 4 |
| `wtsp-latency-field-shifted` | A523 | latency read one bit off (`wtsp_w[32:1]`) | WK1, WK2, WK3, WK4, WK5, WK9 | 8 | 14 | 20 | 56 | 4 of 4 |
| `wtsp-latency-shifted` | R458-1 | latency shifted left one bit | WK1, WK2, WK3, WK4, WK5, WK9 | 8 | 14 | 20 | 56 | 4 of 4 |
| `wtsp-rank-dropped` | R458-1 | rank bit published as 0 | WK1, WK2, WK3, WK4, WK5, WK9 | 4 | 8 | 9 | 28 | 4 of 4 |
| `wtsp-prio-rank-swapped` | R459-1 | priority and rank bits rotated | WK1, WK2, WK3, WK4, WK5, WK9 | 7 | 13 | 19 | 48 | 4 of 4 |
| `wid-ram-first-open-only` | A523, R458-1 | RAM {stream_id, DA, VLAN} written only by the first open | WK2, WK3, WK4, WK9 | 0 (n/e) | 0 (n/e) | 8 | 20 | 2 of 4 |
| `wid-ram-read-at-gate-source` | A523, R458-1 | RAM {stream_id, DA, VLAN} read at the gate source | WK1, WK2, WK4, WK9 | 0 (n/e) | 0 (n/e) | 13 | 49 | 2 of 4 |
| `wid-ram-read-neighbour` | R459-1 | RAM {stream_id, DA, VLAN} read at the previous source | WK1, WK2, WK3, WK4, WK5, WK9 | 0 (n/e) | 0 (n/e) | 20 | 56 | 2 of 4 |
| `wid-flops-da-of-gate-source` | A523, R458-1 | flop arm reads the gate source's DA | WK1, WK2, WK4, WK9 | 1 | 6 | 0 (n/e) | 0 (n/e) | 2 of 4 |
| `wid-flops-sid-of-source-0` | R458-1 | flop arm reads source 0's stream_id | WK1, WK2, WK3, WK4, WK5, WK9 | 0 (equivalent) | 8 | 0 (n/e) | 0 (n/e) | 1 of 4 |
| `wid-flops-vid-of-source-0` | R459-1 | flop arm reads source 0's VLAN | WK1, WK2, WK3, WK4, WK5, WK9 | 0 (equivalent) | 8 | 0 (n/e) | 0 (n/e) | 1 of 4 |
| `talker-vid-unreset` | A523 | the matcher VLAN loses its reset (a stored value read without its valid bit) | WK5 | 1 | 1 | 1 | 1 | 4 of 4 |
| `wsid-ram-first-settle-only` | A523, R458-1 | RAM stream_id written only by the first settle | WK8, WK10 | 0 (n/e) | 0 (n/e) | 6 | 10 | 2 of 4 |
| `wsid-ram-written-on-teardown` | A523, R458-1, R459-1 | RAM stream_id also written by a teardown | WK7 | 0 (n/e) | 0 (n/e) | 1 | 1 | 2 of 4 |
| `wsid-flops-of-control-sink` | A523, R458-1 | flop arm reads the control sink's stream_id | WK6, WK8, WK10 | 0 (equivalent in simulation) | 5 | 0 (n/e) | 0 (n/e) | 1 of 4 |
| `wsid-flops-read-sink-0` | R459-1 | flop arm reads sink 0's stream_id | WK6, WK7, WK8, WK10 | 0 (equivalent) | 6 | 0 (n/e) | 0 (n/e) | 1 of 4 |
| `wtsp-write-ignores-ready` | R458-3 (`r3-wtsp-write-ignores-ready`) | walk records written by a gate open not yet taken (`gate_valid_i` for `gate_acc_w`) | WK9 | 1 | 1 | 1 | 1 | 4 of 4 |
| `wsid-write-ignores-ready` | R458-3 (`r3-wsid-write-ignores-ready`) | RAM stream_id written by a settle not yet taken (`ctl_valid_i` for `ctl_acc_w`) | WK10 | 0 (n/e) | 0 (n/e) | 1 | 1 | 2 of 4 |

The slope controls, at the admission suite's five shapes. The suite stops at
its first failing shape, so the campaign sees N = 2; the counts at 3, 5 and 8
were measured one shape at a time in scratch copies:

| Control | From | Edit | N = 1 | N = 2 | N = 3 | N = 5 | N = 8 | Caught at |
|---|---|---|---:|---:|---:|---:|---:|---|
| `slope-stored-at-stage-2-index` | A523, R458-1, R459-1 (`slope-store-at-stage-1-index`) | slope written at `cidx_q1_r`, not `cidx_q2_r` | 0 (equivalent) | 1,333 of 12,615 | 4,109 of 41,012 | 12,760 of 201,073 | 38,919 of 991,231 | 4 of 5 |
| `slope-stored-at-source-0` | R458-1 | every slope written to source 0 | 0 (equivalent) | 1,521 of 12,615 | 3,915 of 41,012 | 12,415 of 201,073 | 39,056 of 991,231 | 4 of 5 |
| `slope-store-source-0-only` | A523 | only source 0's slope stored | 0 (equivalent) | 1,201 of 12,615 | 3,163 of 41,012 | 10,281 of 201,073 | 33,958 of 991,231 | 4 of 5 |
| `slope-read-source-0` | R459-1 | the admission walk reads source 0's slope | 0 (equivalent) | 578 of 12,615 | 1,683 of 41,009 | 6,125 of 201,068 | 22,202 of 991,223 | 4 of 5 |

"A523" is the lane's round-1 lockstep controls, and "R458-1", "R459-1" and "R458-3"
are the reviews' probes, by their names there. Every control is caught at every shape
where its arm is elaborated and the edit is not equivalent by construction, except
`wsid-flops-of-control-sink` at 1/1: there Verilator 5.050 reads the out-of-range 64-bit
element as element 0 (equivalent in simulation, above), as it would any 64-bit stream_id
read at an idle face at one context; 2/2 catches those edits. The
three edits R459-1 planted as equivalent leave every committed suite passing, as
an equivalent edit must: `tf-tk-same-entry-bypass` (the head bypasses the
memory when the write and read pointers meet), and `wid-threshold-ram-from-1`
and `wid-threshold-flops-always` (either walk arm at every shape).
