[A651] Listener path: keep the owed MSRP Listener Leave across a re-settle (#188); REGISTERING_FAILED follows the in-place swap (#189)

Closes #188
Closes #189

Two commits on main 5addf297, one per issue.

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
| LA or LO (a Leave or an Empty owed) | the one it holds (the re-probe) | keeps the applicant: the next tx! sends the Lv, or New if the talker registers again first (LA + New! = VN) |
| LA or LO | another (the rebind) | arms the matcher at once, parks the old stream_id in a per-sink leave copy until its tx! sends what it owes; the new stream's Listener values are not applied and its declaration request waits meanwhile |
| VO, AO or QO | either | the new stream starts in VO at once (Table 10-3 note 11) |

Nothing back-pressures ACMP. The cost is one T-MRP-JOIN of latency on a new declaration
only where a Leave was owed, and 64 bits per sink for the leave copy (distributed RAM from
three sinks, flip-flops at one and two, the same arms as the walk's stream_id copy) plus
one 64-bit comparator. The Δ13 registrar rule (Milan v1.2 4.2.7.2.2) is untouched. The
design banner that recorded the old trade-off is rewritten. Documented in
`docs/architecture/10_srp_engine.md` §5.1 and §6.4 ("A settle while a Leave is still owed").

## #189: GET_RX_STATE REGISTERING_FAILED follows the in-place swap

In SETTLED_RSV_OK an EVT_TK_REGISTERED is the in-place Talker Advertise <-> Failed swap
(802.1Q 35.2.6). Its F05.3 cell stays '—' (Milan Table 5.30 'x'): no arc, no action, no
frame, no notification. `KL_pp_acmp_listener` now lets `srp_decl[1]` take the
registered type from that event, so REGISTERING_FAILED (Milan Table 5.39, "1 if
registering a Talker Failed attribute") follows the swap in both directions. The
transition ROM is unchanged. Documented in `docs/architecture/05_acmp_engine.md` §6.3.

## Checks and planted controls

| Check | Suite | Planted controls that fail it |
|---|---|---|
| RB1: rebind before tx!: new stream registered, Listener not yet declared; the next tx! sends only the old stream's Lv (Ready); the tx! after it the new stream's New Ready | `tb/srp_stream_fsms` | `listener-rebind-abandons-leave`, `listener-declaration-not-held`, `listener-park-never-retires` |
| RB2: re-probe onto the same stream: the next tx! sends its Lv | `tb/srp_stream_fsms` | `listener-reprobe-abandons-leave` |
| RB3: re-probe whose talker registers again before tx!: New Ready, no Lv | `tb/srp_stream_fsms` | `listener-reprobe-parks-own-stream` |
| WK11: the leave copy at 1/1, 2/2, 3/5 and 9/9 sinks: one Leave per re-settled declaring sink, naming the stream_id it held | `tb/srp_stream_fsms` walk arms | `walk-ignores-leave-copy`, `lsid-ram-read-sink-0`, `lsid-flops-read-sink-0`, `lsid-ram-written-with-new-stream`, `wsid-write-ignores-ready` |
| AS7: end to end, a rebind settled before the next T-MRP-JOIN: that MRPDU carries the old stream's Lv and nothing for the new one; the next declares the new one | `tb/pp_top` | `rebind_abandons_leave`, `park_never_retires` |
| B4, B4b: in SETTLED_RSV_OK the swap to Talker Failed sets REGISTERING_FAILED (GET_RX_STATE 0x0042), the swap back clears it (0x0002), no arc | `tb/acmp_listener` | `rf_swap_unlatched`, `rf_swap_sticky` |
| AS5b, AS5c: the same end to end from MSRP frames: FAILED registered, Asking Failed declared, GET_RX_STATE byte-exact both ways | `tb/pp_top` | `rf_swap_unlatched`, `rf_swap_sticky` |
| AS6 (added): the unbind releases the sink's VLAN membership (MVRP Lv of its VID) | `tb/pp_top` | `st_ls_teardown_as_declare`, `st_ls_teardown_lost` |

The srp_top campaign carries the RB and WK11 arms (and requires WK1-WK11 and RB1-RB3 in its
assertion coverage); `tb/pp_top/acmp_mutants.py` carries the rest. Since a settle now
withdraws the old Listener declaration, a teardown issued as a settle still puts the Lv on
the wire, so the existing control `st_ls_teardown_as_declare` is now graded by the VLAN
release (AS6), which it breaks; nothing else in the default pp_top run caught it. The five
walk-copy patches under `tb/srp_top/mutations/` were re-anchored on the new context with
the same edits; `wsid-write-ignores-ready` now also fails WK11.

A residual, not changed here: the event router keeps the first payload of a source that strobes
again before the listener takes it, so two type changes of one sink's registration within a few
clocks (one MRPDU declaring both types of one stream) would leave GET_RX_STATE on the first. The
SRP side, GET_STREAM_INFO and the declaration follow the last.

## Records

Base 5addf297, head dc01aec4, the same pinned Verilator 5.050 and sv2v 0.0.12; every command's own
exit status, never piped.

| Gate | Base | Head |
|---|---|---|
| `scripts/run_suites.sh` | rc 0, 1,030,013 checks | rc 0, 1,030,026 (acmp_listener +3, pp_top +5, srp_stream_fsms +5) |
| `check-req-tags.py --suites --evidence` | rc 0, 227 | rc 0, 229 |
| `scripts/lint_hdl.sh`, `make check`, `scripts/gen_matrix.py --check`, `syn/yosys/run.sh`, `tb/elab_guards/guards.py --frontend yosys` | rc 0 | rc 0, identical apart from link, ID-file and tag counts |

Every campaign that builds a changed file is rc 0 at both, with identical per-arm results apart
from the new arms and the new checks the old arms now also fail: srp_top (137 -> 146 arms),
srp_admission, maap, adp_engine, aecp, aecp-dispatch, ctr, acmp (51 -> 57), gsi, name_wr, notify,
name_state, elab_guards, d3.

Reference platform (milan-fpga dev e9cbb676, gitlink staged at each revision, with the
parent-evidence-classification patch and the milan_dp #67 adoption patch in the working tree):
BDD, lint_rtl, the idiom, naming, evidence, hygiene, port-contract and source-list gates, the xvlog
gate, the Yosys elaboration of milan_datapath / KL_pp_shadow / KL_gptp_shadow, the OOC self-test
and KL_pp_shadow pricing, test_builder, pp_shadow, nvm_cosim, milan_dp_render and milan_dp all pass
at both, with identical check lines. `check_submodule_docs` fails identically at both ("documented
pin differs from Git"), as it does for any gitlink the parent has not adopted yet. KL_pp_shadow
(Yosys OOC): LUT_TOT 59,992 -> 60,056, FF 26,282 -> 26,296, block RAM and DSP unchanged.
