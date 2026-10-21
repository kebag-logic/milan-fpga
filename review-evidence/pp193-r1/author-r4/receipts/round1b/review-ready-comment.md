[A661] REVIEW READY
Head: processor `193-shared-listener-leave` = 788425db609204234282ea655be2452649622cba (three commits on main 21601694; not pushed, no PR opened).

Ruling 6290012163, inside the existing per-sink plane (`KL_srp_listener_fsm` only; no port, parameter or register-map change):
- The owner (the lowest-index sink declaring the StreamID) holds the one applicant. Riders are VO: they take no event and send nothing.
- A sink's declaration request sets only its own type. The applicant declares the sum, Ready with AskingFailed = ReadyFailed (802.1Q-2018 35.1.2.2, Table 35-14), with New! for a first declarer or a changed sum.
- The handover carries the state (and its walk mark), with no Lv! and no New! unless the sum changed. That includes an A15 of the sink holding the applicant: handed over, not parked.
- The last declarer's withdrawal keeps the #188 rules.
- Per sink and unchanged: registrar, EVT_TK_*, GET_RX_STATE (`lstn_decl_state` is the sink's own type).

Tests:
- `tb/srp_stream_fsms` SH1-SH9: one applicant per tick; owner first and the reverse; three sinks; rider rebind; the type sum; a mid-walk handover; A8+A15 on consecutive clocks; a rider's A15 on the clock after the owner's A8.
- `tb/srp_top` group `share` SW1-SW3: one VectorAttribute per value, byte-exact; a Milan 4.2.7.2.2 peer Registrar never deregisters while a sink wants the stream, and one Lv at the last unbind; ReadyFailed byte-exact.
- 12 new controls in the srp_top campaign, each KILLED by its named check; the 9 #188 controls on moved lines are re-anchored and still KILLED.

Gates, base 21601694 vs head, all rc 0:
- run_suites 1,030,237 -> 1,030,284 (only srp_stream_fsms +42 and srp_top +5).
- lint, make check, matrix, portability elaboration and guards: identical.
- Every campaign that builds the listener FSM is identical, except srp_top (the new arms; coverage 113/113).
- gsi: the old edit of `failure-change-redeclares` became equivalent, because a request of an unchanged type no longer re-declares. Commit 3 plants it where the New! is decided, and gsi is then identical to base.

Parent consumer gates (dev e26f1816 + the three adoption patches, gitlink committed per pin): all rc 0 at base and head, with `check_submodule_docs` failing identically at both. KL_pp_shadow out-of-context: +1,037 LUT, +50 FF.

Main moved to 08023123 (#197) meanwhile. A scratch merge is conflict-free and passes tb/pp_top and the gsi campaign (23/23).

To confirm:
- the area cost above;
- a sole sink's request of the type it already declares no longer re-sends New (reachable only when a withdrawal and a re-registration meet before the grant).

Evidence: lane receipts (HANDOFF, PR body, records, index).
