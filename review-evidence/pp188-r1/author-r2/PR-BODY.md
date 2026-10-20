[A651] Listener path: keep the owed MSRP Listener Leave across a re-settle (#188); REGISTERING_FAILED follows the registered type on every change (#189)

Closes #188, closes #189

Round 1: two commits on main 5addf297, one per issue, and the merge of main b48312e1.
Round 2 (six commits on that merge) answers both reviews: REGISTERING_FAILED now follows
the last of two type changes that coalesce in the event router, every documented settle arm
of #188 has its own check and planted control, a sink with no record no longer owes a
Leave, and the wording items are applied.

## #188: an A15 settle no longer abandons the owed Listener Leave

`KL_srp_listener_fsm` used to force the sink's applicant to VO on every A15 settle, so a
Listener Leave still pending from the A8 before it (applicant in LA) was never sent when
the sink settled again before the next transmit opportunity: on a rebind (Milan v1.2
5.5.3.5.43 probes the new source at once) and on the re-probe after the talker's
registration ends (5.5.3.5.48). The old declaration then stayed registered at the bridge
until a LeaveAll plus LeaveTime aged it out.

IEEE 802.1Q-2018 10.7.7 keeps one Applicant per attribute value, and Table 10-3 takes
AA/QA to LA on Lv! and sends the Leave from LA at tx!. The settle now applies Lv! (as the
A8 before it already did) and then:

| Applicant after Lv! | New stream_id | Settle |
|---|---|---|
| LA or LO (a Leave or an Empty owed) | the one it holds (the re-probe) | keeps the applicant: the next tx! sends what it owes (the Lv from LA, the Empty from LO), unless the talker registers again first, when New! takes LA or LO to VN and the tx! sends New |
| LA or LO | another (the rebind) | arms the matcher at once, parks the old stream_id in a per-sink leave copy until its tx! sends what it owes; the Listener values of either stream are not applied and the new stream's declaration request waits meanwhile |
| VO, AO or QO | either | the new stream starts in VO at once (Table 10-3 note 11) |

While a stream_id is parked it is the one the applicant holds: a further settle onto a third
stream keeps it parked, a settle back onto it is the first row, and a txLA! walk (LA to LO,
no message) keeps the park until the tx! that sends the Empty. A sink with no record since
reset holds no value and owes nothing, whatever state a received LeaveAll left its applicant
in (round 2: the first #188 change let such a sink send an Empty for a stream_id it never
held on its first settle, and its New one T-MRP-JOIN late).

Nothing back-pressures ACMP. The cost is one T-MRP-JOIN of latency on a new declaration
only where a Leave was owed, and 64 bits per sink for the leave copy (distributed RAM from
three sinks, flip-flops at one and two, the same arms as the walk's stream_id copy) plus
one 64-bit comparator. The Δ13 registrar rule (Milan v1.2 4.2.7.2.2) is untouched.
Documented in the design banner and in `docs/architecture/10_srp_engine.md` §5.1 and §6.4
("A settle while a Leave is still owed").

## #189: GET_RX_STATE REGISTERING_FAILED follows the registered type on every change

In SETTLED_RSV_OK an EVT_TK_REGISTERED is the in-place Talker Advertise <-> Failed swap
(802.1Q 35.2.6). Its F05.3 cell stays '—' (Milan Table 5.30 'x'): no arc, no action, no
frame, no notification. `KL_pp_acmp_listener` lets `srp_decl[1]` take the registered type
from that event, so REGISTERING_FAILED (Milan Table 5.39, "1 if registering a Talker
Failed attribute") follows the swap in both directions.

The event router keeps the first payload of a source that strobes again before the listener
takes its event, and the listener takes router events only when idle. So two type changes of
one sink while the listener is busy (for example behind held MAC TX) were one event whose
payload named the type in between. The top now drives the listener's Failed input from the
SRP listener's registered-type level of the presented sink when the listener takes the event,
not from the payload; the payload still carries the type at strobe time to the trace ring.
No port, parameter, register-map or transition-ROM change. Documented in
`docs/architecture/05_acmp_engine.md` §6.3.

## Checks and planted controls

| Check | Suite | Planted controls that fail it |
|---|---|---|
| RB1: rebind before tx!: new stream registered, Listener not yet declared; the next tx! sends only the old stream's Lv (Ready); the tx! after it the new stream's New Ready | `tb/srp_stream_fsms` | `listener-rebind-abandons-leave`, `listener-declaration-not-held`, `listener-park-never-retires` |
| RB2: re-probe onto the same stream: the next tx! sends its Lv | `tb/srp_stream_fsms` | `listener-reprobe-abandons-leave` |
| RB3: re-probe whose talker registers again before tx!: New Ready, no Lv | `tb/srp_stream_fsms` | `listener-reprobe-parks-own-stream` |
| RB4: a second rebind while parked, onto a third stream: the tx! sends the first stream's Lv, the next declares the third | `tb/srp_stream_fsms` | `listener-csid-ram-ignores-park` |
| RB5: a rebind back to the parked stream, its talker registering again: applicant kept, New Ready, no Lv | `tb/srp_stream_fsms` | `listener-rebind-back-keeps-park` |
| RB6: an LO applicant settled onto another stream: the tx! sends the held stream's Empty, then New | `tb/srp_stream_fsms` | `listener-lo-not-owed` |
| RB7: a txLA! walk while parked: nothing sent, park kept, then the held Empty, then New | `tb/srp_stream_fsms` | `listener-park-retires-on-txla` |
| RB8: a Listener value received while parked (LO) is not applied: the held Empty still goes out | `tb/srp_stream_fsms` | `listener-parked-applies-rx` |
| RB9: a first settle after a received LeaveAll, no record before it: New Ready, no Empty | `tb/srp_stream_fsms` | `listener-unrecorded-applicant-owes` |
| WK11: the leave copy at 1/1, 2/2, 3/5 and 9/9 sinks: one Leave per re-settled declaring sink, naming the stream_id it held | `tb/srp_stream_fsms` walk arms | `walk-ignores-leave-copy`, `lsid-ram-read-sink-0`, `lsid-flops-read-sink-0`, `lsid-ram-written-with-new-stream`, `wsid-write-ignores-ready` |
| WK12: every declaring sink settled on a second and a third stream before tx!: each Leave names the stream_id declared, at both elaboration arms | `tb/srp_stream_fsms` walk arms | `listener-csid-ram-ignores-park`, `listener-csid-flops-ignores-park` |
| AS7: end to end, a rebind settled before the next T-MRP-JOIN: that MRPDU carries the old stream's Lv and nothing for the new one; the next declares the new one | `tb/pp_top` | `rebind_abandons_leave`, `park_never_retires` |
| B4, B4b: in SETTLED_RSV_OK the swap to Talker Failed sets REGISTERING_FAILED (GET_RX_STATE 0x0042), the swap back clears it (0x0002), no arc | `tb/acmp_listener` | `rf_swap_unlatched`, `rf_swap_sticky` |
| AS5b, AS5c: the same end to end from MSRP frames: FAILED registered, Asking Failed declared, GET_RX_STATE byte-exact both ways | `tb/pp_top` | `rf_swap_unlatched`, `rf_swap_sticky` |
| AS5d, AS5e: two swaps while the listener is held busy (MAC TX held, TX slots full), Advertise to Failed to Advertise and Failed to Advertise to Failed, taken as one coalesced event: after the queue drains (the answers and nothing else, no arc) GET_RX_STATE follows the last type byte-exact, and still after an unchanged refresh | `tb/pp_top` | `tk_failed_first_payload` (the previous behaviour, both), `tk_failed_or_payload` (AS5d), `tk_failed_and_payload` (AS5e); preconditions: `router_coalesce_unflagged`, `tk_type_unlatched` |
| AS6: the unbind releases the sink's VLAN membership (MVRP Lv of its VID) | `tb/pp_top` | `st_ls_teardown_as_declare`, `st_ls_teardown_lost` |

The srp_top campaign carries the RB and WK arms and requires WK1-WK12 and RB1-RB9 in its
assertion coverage; `tb/pp_top/acmp_mutants.py` carries the rest. Two probes of the settle
logic stay without a control, accepted as likely equivalent and recorded in the srp_top
README: the park's retire keeping the old FourPacked parameter (it shows only in an Empty,
which registers nothing) and the same-value test without the record term (with RB9's fix it
matters only when something is owed, which needs a record).

## Records

Base cb8bab04 (the round-1 head) and head cca12e3c, pinned Verilator 5.050, sv2v 0.0.12,
Yosys 0.33, every rc 0:

- `scripts/run_suites.sh`: 1,030,051 -> 1,030,070 checks, 0 failing (pp_top 10,533 -> 10,543,
  srp_stream_fsms 1,352 -> 1,361; every other suite identical). `scripts/lint_hdl.sh`,
  `scripts/gen_matrix.py --check`, `syn/yosys/run.sh` and the Yosys elaboration guards
  identical; `make check` identical but for the link and file counts of the eight new patches.
- `tb/srp_top` mutants: 168 -> 179 arms, all KILLED, assertion coverage 94/94 -> 101/101 (WK12,
  RB4-RB9). `tb/pp_top/acmp_mutants.py`: 60 -> 65 of 65 KILLED. Every other campaign that
  builds a changed file (srp_admission, maap, adp_engine, aecp, aecp-dispatch, ctr, gsi,
  name_wr, notify, name_state, elab_guards, d3) identical.
- Consumer gates in the integrating repository with this head pinned: every gate's result is
  identical at base and head (two gates fail at both for the moved pin and an RTL lint ratchet
  against main's merged TSpec ports, nothing this change touches); Yosys out-of-context
  KL_pp_shadow LUT 56,701 -> 56,105, every other resource unchanged.
