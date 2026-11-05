[A729b] SRP Listener: apply a Talker attribute registered before the sink's ACMP settle (issue #212)

## The defect

A Stream Input's Listener declared nothing for a Talker attribute that the port registered
before the sink's ACMP settle (CONNECT_TX success). The sink's registrar started MT at the A15
settle and saw only events after it. So Listener Ready, or Asking Failed for a Talker Failed,
came only after the next LeaveAll made the talker re-declare, one T-MRP-LEAVEALL (10 to 15 s,
Milan v1.2 Table 4.3) late. This was seen on the wire after power-on and on a re-bind to an
already declared Talker Failed.

- Milan v1.2 §5.3.8.5: a settled, SRP-bound Stream Input with a matching registered Talker
  Advertise declares Listener Ready; Asking Failed is allowed for a Talker Failed.
- Milan v1.2 §5.5.3.5.18 step 4: on a successful PROBE_TX_RESPONSE the Listener starts the SRP
  reservation.
- IEEE 802.1Q-2022 §10.7 and §10.7.8: a full participant keeps a registrar per attribute value
  registered. Its state does not depend on when the application became interested.

## The design

Everything is inside `KL_srp_listener_fsm`, plus one connection in `KL_srp_top` (its existing
`link_up_i` now also reaches the listener). There is no top-level port, parameter or
register-map change: `hdl/top/protocol_processor_top.sv` is unchanged.

1. **Port Talker registrars.** There are N = `N_SINKS_P` (P-N-STREAM-IN) entries, the port's
   existing budget of Talker registrars (one per sink).
   - Each entry registers one Talker Advertise/Failed value, whether or not a sink is settled
     on it.
   - It runs the sink registrar's own Table 10-4 with Milan v1.2 §4.2.7.2.2 (rLv on IN is MT at
     once; rLv on LV is `-x-`), on the exact {stream_id, DA, VLAN} (Milan v1.2 §5.3.8.9). It
     uses the LeaveAll lane of the type it holds and the own LeaveAll. Its `T-MRP-LEAVE`
     leavetimer (Milan v1.2 Table 4.3) is kept in `$clog2(LEAVE_MS_P + 1)` bits, 13 at 5000 ms,
     compared wrap-safe on `now_ms_i`, with the sink registrar's priority.
   - The bound: 802.1Q-2022 §35.2.7 leaves the number of values held to the implementation. A
     value registered while all N entries are registered is not held. A sink that settles on
     it registers on the talker's next declaration, as before.
2. **The settle takes the registration.** An A15 settle on a held value starts the sink's
   registrar in the entry's state after the events of the settle's own clock.
   - It takes the type, latency and FailureInformation, raises EVT_TK_REGISTERED and requests
     the declaration at once.
   - So `tk_reg_state`, the failure code and bridge, GET_RX_STATE's REGISTERING_FAILED and the
     ACMP listener's SETTLED_RSV_OK all follow at the settle, and the next tx! sends the New.
   - An LV entry starts the sink LV, and the sink's leave slot is armed with the entry's
     deadline (rebuilt absolute from its remaining time), so no registrar timing changes.
3. **A re-bind to the same stream keeps its registration.** An A8 only disarms the matcher:
   the sink's registrar keeps registering its record's {stream_id, DA, VLAN} (Table 10-4, Δ13,
   its leave slot) until the sink's next A15, raising and publishing nothing meanwhile (F10.5's
   teardown edges carry no event; `tk_reg_state` NONE, `acc_latency` 0). An A15 on the same
   triple keeps that registration whatever the port table holds (802.1Q-2022 §10.7, §10.7.8),
   with the strobes and request of item 2.
4. **A link change ends the registrations a settle could take.** LINK_DOWN (Flush!) and
   LINK_UP (Begin!) take every port registrar, and the registrar of every sink not settled,
   to MT (802.1Q-2022 Table 10-4), so nothing registered before a link loss is seeded or kept
   after it.
5. **A re-bind that settles before its old Leave went out.** Milan v1.2 §5.5.3.5.43 probes the
   new source at once. Issue #188 parks the owed Lv, and until now the new stream's New waited
   one more walk.
   - The two stream_ids are two attribute values, each with its own applicant and tx!
     (802.1Q-2022 §10.7.7, Table 10-3). So the walk that sends the parked Lv also applies the
     waiting New! and sends the New on its second pass, in the same MRPDU.
   - If another sink declares the new stream or holds its applicant, that group's applicant
     takes the request as before (issue #193).
6. **Not done: a LeaveAll at the settle.** Table 10-5 issues sLA only from Active, and only
   leavealltimer! enters Active: the timer's random T-MRP-LEAVEALL expiry (§10.7.4.3, Milan
   Table 4.3), or a Flush! (§10.7.5.2). A settle is neither, and the peer's re-declaration
   would take more than one T-MRP-JOIN.

## Acceptance

| Item | Met by |
|---|---|
| 1. A Talker Advertise or Failed registered before a sink settles is applied at the settle, with Ready / Asking Failed declared New within one join period | `tb/srp_stream_fsms` PS1 (Advertise) and PS2 (Failed): registered at the settle, New on the first tx! after it. PS17: the settle applies the held value's latest type, FailureInformation and latency. `tb/pp_top` AS9: after a reset the talker's Advertise registers before the bind; the settle registers it, and Ready New follows at most 240 ms later with no talker frame and no LeaveAll |
| 2. A re-bind with the Talker declared: the same within one join period, with the failure state and code at once | PS3 (the same stream, before and after the old Lv), PS20 (the same stream with every port registrar held by other values, before and after the old Lv, Advertise and Failed; the same stream_id on another DA or VLAN is another value), PS4 (another stream, its Talker Failed declared, the old Lv still owed: Lv and New Asking Failed in one tx!), PS5 (after the old Lv). AS8: FAILED, GET_RX_STATE REGISTERING_FAILED and GET_STREAM_INFO's failure code and bridge before any MRPDU; then the old Lv and New Asking Failed in the next MRPDU, at most 240 ms after the settle |
| 3. A Talker withdrawn before the settle (rLv, or a LeaveAll with no re-declaration) is not applied | PS6 (rLv, Advertise and Failed); PS7 (a received LeaveAll on its lane or the own LeaveAll, then T-MRP-LEAVE); PS9 (a settle on the leavetimer!'s own clock); PS16 (an rLv, rIn or rMt of a value no port registrar holds, also after a refusal while the table was full); PS19 (an rLv while LV leaves it LV, ending at its deadline); PS21 (a withdrawal or an unanswered LeaveAll while the sink is unbound is not applied at its re-bind); PS23 (a link down or up ends every registration a settle could take); LK1 on `KL_srp_top` |
| 4. The bound stays the existing per-port budget; no top-level or register-map change | N = `N_SINKS_P`; PS11 grades the bound; `KL_srp_listener_fsm` gains one internal input, fed from `KL_srp_top`'s existing `link_up_i`; no top-level file changed |
| 5. Rows with a mutant failing them by name; every suite green; the parent consumer gate passes | 46 issue #212 arms in the SRP campaign and two in the ACMP campaign, each failing its named check: `pt-seed-dropped` fails PS1 and PS5, and `presettle-removed` (the whole path: seed, kept registration and the one-walk declaration) fails PS3. For item 3 the arms break the path's withdrawal handling (rLv, leavetimer!, LeaveAll, allocation, the unbound registrar's events, the link change), since removing the path would leave those rows passing. Every suite and campaign passes (below), and so does the scratch-parent consumer gate with this head as its gitlink |

## Round 2

Two reviews of the round-1 head `04856e48` (R769-1 and R770-1) found no wrong behaviour in
what was tested. They raised one conformance finding each, three test gaps and two
residues. The round-2 assignment ruled on each. All are resolved on top of round 1, with no
rebase:

| Item | Ruling | Resolution | Row | Arm(s) failing it by name |
|---|---|---|---|---|
| R769-1 F1: a re-bind to the same stream lost its registration when the port table held N other values | option (a) | design item 3: the A8 leaves the sink's registrar registering its value, unpublished; an A15 on the same {stream_id, DA, VLAN} keeps it. No new state: one {DA, VLAN} comparator per sink beside the existing stream_id compare. While unbound the registrar follows Table 10-4 on its value, so a withdrawal meanwhile is not applied (PS21), and it raises and publishes nothing (PS22) | PS20 (table full, before and after the old Lv; Advertise and Failed; another DA or VLAN is another value), PS21, PS22 | `rebind-same-not-kept`, `keep-ignores-da`, `keep-ignores-vlan`, `keep-declares-seed-type`, `keep-latency-strobe-dropped`, `unarmed-registrar-deaf`, `keep-ignores-expiry`, `unarmed-indicates`, `unarmed-fail-chg`, `unarmed-unregistered`, `unarmed-latency-strobe`, `unarmed-publishes-latency`, `unarmed-dbg-registrar` |
| R770-1 F4: no Flush!/Begin! on the port registrars | fix | design item 4: `KL_srp_top`'s existing `link_up_i` feeds the listener, whose fall (LINK_DOWN, Flush!) and rise (LINK_UP, Begin!) take every port registrar, and the registrar of every sink not settled, to MT. The processor top and the register map are unchanged | PS23 (register, link down and up, settle: nothing applied; LINK_DOWN alone; LINK_UP alone; a sink's kept registration; a re-bind on the link's clock); `tb/srp_top` LK1 (the wiring) | `pt-link-flush-dropped`, `link-begin-dropped`, `unarmed-link-flush-dropped`, `keep-on-link-clock`, `top-listener-link-unwired` |
| R770-1 F1: an rLv, rIn or rMt of a value the table does not hold | test | none of them takes MT to IN (Table 10-4) | PS16, also a value refused while the table was full and sent after an entry freed | `pt-alloc-any-event` |
| R770-1 F2: FailureInformation and latency changed before the settle | test | the settle applies the latest | PS17 (Failed code, bridge and latency; Advertise latency; Advertise turned Failed) | `pt-fcode-first-only`, `pt-lat-on-alloc-only`, `pt-type-on-alloc-only` |
| R770-1 F3: an A8 on a held value; rLv on an LV entry | test | an A8 registers nothing; rLv in LV is `-x-` | PS18; PS19 (seeded LV with the LeaveAll's deadline, ending at it) | `seed-on-teardown`; `pt-rlv-on-lv-ends` |
| R769-1 S1: the path's practical reach | taken | the integrator guide (§8, after the GET_STREAM_INFO fields) and 10 §6.4 state it with the shipping N = 2 (one stream and the CRF stream), and the limits below | — | — |
| R769-1 S3: the stale-expiry guard ends at the arm's issue | the guard if a few LUT, else §6.4 corrected | §6.4 corrected. The arm path's latency is not visible to the listener: `KL_srp_top` notes that the processor top queues it behind other faces. An exact guard needs, per sink, the intended deadline (as `KL_srp_top` keeps for its LeaveAll slots) or an applied indication from the timer service. Either is more than a few LUT | — | — |
| R769-1 S2 / R770-1 S1: the 13-bit deadline | only if smaller at 2x2 and 8x8 | taken: `KL_srp_top` 2x2 13,260 → 13,193 LUT, 5,372 → 5,334 FF; 8x8 28,276 → 28,193 LUT, 11,376 → 11,224 FF (round-2 changes without, then with it) | PS7, PS8, PS9, PS19 | `pt-expiry-sign-bit`, `seed-deadline-rebuild-drops-now` |
| R769-1 R1: `10_srp_engine.md:222` | the reviewer's text | replaced with the reviewer's text | — | — |
| R770-1 F5: `10_srp_engine.md:759`, `:805` | the reviewer's text | replaced with the reviewer's text | — | — |

Also in round 2:
- Acceptance 5 names a mutant that removes the pre-settle path. With design item 3, a re-bind
  to the same stream (PS3) is served by the kept registration as well as by the seed. So
  `pt-seed-dropped` now names PS5 (a re-bind to another stream), and a new `presettle-removed`
  arm (no seed, no kept registration, no one-walk declaration: the behaviour before the
  issue) names PS3.
- Both reviewers' probes, re-run at this head: R769-1's re-bind probe passes (1,502 of
  1,502). R770-1's `pt-alloc-any-event`, `pt-fcode-first-only`, `pt-lat-on-alloc-only`,
  `pt-type-on-alloc-only`, `seed-on-teardown` and `pt-rlv-on-lv-ends` each fail by name
  (PS16, PS17, PS17, PS17, PS18, PS19).
- `dbg_reg_state_o`, which nothing in `KL_srp_top` reads, reports MT while a sink is not
  settled, as `tk_reg_state` does, so the existing check `L A8 disarms the matcher` holds
  unchanged.

## Changes

- `hdl/srp/KL_srp_listener_fsm.sv`:
  - the port registrars `pt_*` (`pt_match`, `pt_next`) and the seed (`pt_seed`), with the
    leave deadline in `$clog2(LEAVE_MS_P + 1)` bits;
  - the seeded sink registrar and its leave-slot arm (`sdl_*`);
  - the kept registration (`settle_keep`): the sink registrar runs on its record through an
    A8, unpublished, and an A15 on the same triple keeps it;
  - the link input (`link_up_i`, `link_q_r`): LINK_DOWN and LINK_UP take the port
    registrars and every unbound sink's registrar to MT;
  - the walk's one-pass declaration after a parked Leave (`park_hold`,
    `park_retire_declare`);
  - the banner and the comparator note.
- `hdl/srp/KL_srp_top.sv`: the listener's `link_up_i` from the engine's existing input.
- `docs/architecture/10_srp_engine.md`: contract, state, storage rows and measured cost, F10.5
  arcs, the owed-Leave rule, and the subsection "A Talker registered before the settle" (the
  bound and its reach, the settle, the same-stream re-bind, the link change, why no LeaveAll).
- `docs/guides/integrator.md`: the path's reach at the shipping N.
- `docs/architecture/02_interfaces.md`, `05_acmp_engine.md` and
  `docs/00_MILAN_COMPLIANCE_REVIEW.md` (REQ-ACMP-018).
- `tb/srp_stream_fsms`:
  - section PS (PS1 to PS23), a settable `now_ms_i`, a driven `link_up_i` and a counted
    latency strobe;
  - RB1, RB4, RB6 and RB7 expect the old Lv and the new New in one tick;
  - L9, SH14 and SH15 keep their premises (L9 fills the port registrars first; SH14 and SH15
    withdraw the talker before the joiner settles).
- `tb/srp_top`: LK1, group `link`.
- `tb/pp_top`: AS8, AS9, AS7 (one MRPDU), a Listener lookup that reads value k of a vector
  as its FirstValue plus k (802.1Q-2022 §35.2.2.8), and a GET_STREAM_INFO helper.
- Campaigns:
  - `tb/srp_top/mutants.py` and 46 issue #212 patches; coverage PS1-PS23 and LK1;
  - `tb/pp_top/acmp_mutants.py` (`presettle_seed_dropped`, `presettle_park_declares_next_walk`);
  - patches whose context moved, cut again with the same edits;
  - two named checks renamed where the behaviour moved them: `park_never_retires` (AS7) and the
    walk arm of `listener-park-never-retires` (`WK12: push`; the walk now declares the third
    stream, on the parked stream_id).
- READMEs: the PS, LK and AS rows and the new controls; the arm counts the new rows move.

## Validation

Every gate ran on a clean clone of this head (`a2fce43`), and every one is rc 0:

- `make check`;
- `scripts/lint_hdl.sh` under Verilator 5.052 and the pinned 5.050: 41 modules each;
- `./syn/yosys/run.sh`: 42 tops;
- `tb/elab_guards/guards.py --frontend yosys`: 93 checks;
- `bash scripts/run_suites.sh` with the pinned Verilator 5.050: **1,030,993 checks, 0 failing**,
  36 suites. pp_top has 11,064, srp_stream_fsms 1,500 (1,468 at round 1) and srp_top 8,671
  (8,669 at round 1);
- the executed REQ-tag check: 266 evidence lines, 14 suites.

Campaigns, pinned Verilator 5.050:

| Campaign | Result |
|---|---|
| SRP (`tb/srp_top/mutants.py`) | 275 of 275 (5 controls, 269 arm entries) with coverage 166 of 166; every count equal to the README cells |
| ACMP | 103 of 103 KILLED by their named checks |
| AECP | 67 PASS |
| GSI | 30 detected by named checks |
| CTR | 18 PASS |
| name write | PASS |
| AECP dispatch | 105 of 105 |
| notification | 137 of 137 |
| D3 | 110 of 110 |

Outside SRP, every per-arm result equals round 1's run, label for label.

Area, measured with sv2v then yosys 0.66 `synth_xilinx -family xc7 -flatten`:

| `KL_srp_top` shape | main `a9e84b66` | round 1 `04856e48` | this head | this head − main |
|---|---|---|---|---|
| 2 sources, 2 sinks: LUT | 11,475 | 12,690 | 13,193 | +1,718 |
| 2 sources, 2 sinks: FF | 4,812 | 5,372 | 5,334 | +522 |
| 8 and 8: LUT | 23,046 | 27,399 | 28,193 | +5,147 |
| 8 and 8: FF | 9,236 | 11,376 | 11,224 | +1,988 |

- No RAM changes.
- At the listener, the flip-flops are N × 244 + (1 + log2 N + 32) + 1. The link flip-flop
  merges with the Domain FSM's in `KL_srp_top`.
- This flow's LUT figure moves by up to about 300 for edits of a few LUT, so round 2's LUT
  change against round 1 is within its noise. The FF figure is exact.

## Scratch-parent consumer gate

The scratch parent is milan-fpga dev `604899c0` with this head as the protocol-processor
gitlink, committed locally and never pushed. The pin's ROM digests were recorded with
`./syn/yosys/ooc.sh --record-rom-digests`, and both equal main's.

At pin `a2fce43`, every rtl-fast job's run steps and milan_dp passed, all rc 0:
- changes: `true`;
- lint_rtl: 89 ≤ ratchet 89; pp_srcs;
- behave: 14 features, 508 scenarios;
- the yosys elaboration of `milan_datapath`, `KL_pp_shadow` and `KL_gptp_shadow`, with the
  OOC read-set, refusal, guard and cache self-tests;
- the publication census: 0 of 31 rules no arm proves;
- firmware-unit, firmware-boundary and firmware-verilator;
- the firmware mutation campaigns:
  - control, shard 1 of 4: 523 of 523 caught;
  - AECP, shard 2 of 4: 78 `[ok]`, PASS;
  - SRP, shard 3 of 4: 280 `[ok]`, PASS;
- `tb/verilator/milan_dp`: 12,075 `[ok]`, 1,301 `[PASS]`, 0 failures.

## Limits and open risks

- **The bound and its reach.** The port holds N Talker values, one per sink: 2 in the shipping
  image (one stream and the CRF stream). A listener port receives every Talker declaration
  of its VLAN. On a network with more Talker values than N, the stream a sink settles on
  after power-on is therefore generally not held, and that first settle still waits for the
  talker's next declaration. That is at the latest its re-join after a LeaveAll, one
  T-MRP-LEAVEALL later, as before this change (PS11). A re-bind of a sink to the stream it
  was bound to does not depend on the table (PS20).
- **A settled sink across a link change.** Its registrar has no link input, as before this
  change. A sink settled through a link change keeps its registration until the talker
  withdraws it or a LeaveAll ages it. Unbound sinks and the port registrars are flushed
  (PS23).
- **The seeded LV arm's stale-expiry window.** The listener's guard ends when it issues the
  arm, not when the timer service applies it. The arm crosses `KL_srp_top`'s and the
  processor top's queues, whose latency the listener does not see. An expiry of the old
  deadline in those few clocks would end the seeded registration early. The registrar before
  this change has the same window after LV, IN and LV again (10 §6.4).
- **Area.** Against round 1, `KL_srp_top` loses 38 FF at 2x2 and 152 at 8x8. Its yosys LUT
  figure rises by 503 and 794, but the flow's LUT figure moves by up to about 300 for edits of
  a few LUT. The shipping image needs a new Vivado route of this head; none was run here.
- **Behaviour change outside the issue.** A re-bind whose old Leave is still owed now sends the
  new stream's New in the same walk (design item 5). This replaces issue #188's one-walk delay;
  RB1, RB4, RB6, RB7 and AS7 grade it.
- **The pin bump.** It needs the parent's ROM-digest rows (recorded here, unchanged values)
  and its documented-pin update, which the parent's docs workflow checks.

Closes #212
