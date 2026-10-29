[A699b] REVIEW READY
Head: ec1ff275a72d885f0908fd213d8009e9e4dda4d9 on branch 203-aecp-reboot. That is three commits on top of round 1's 1be824fccbda5d3341737f5fe033d60edd27af57 (base main f65c8ff7c673aaa8e2ea8da654f081ddb13588d8). No rebase, not pushed. The PR body is prepared with "Closes #203".
R732-F2: aede92e is comment-only. The heading reads `REBOOT request (REQ-FWX-001; IEEE 1722.1-2021 §7.4.43; issue #203)`; it is line 824, which the review cites as 823.
R732-F1, the terminal transmit-quiet state:
- One gate at the TX arbiter, through which every control-plane frame passes: arb_req_w = arb_want_w & rbt_tx_open_w. From the clock ADP has built and queued its last ENTITY_DEPARTING until rst_n, only ADP's lane is open. ADP's enable has fallen for good, so it builds nothing more, and nothing follows the final DEPARTING.
- The gate only decides which frame starts: no frame is cut, and the held request is unchanged.
- It covers AECP unsolicited (lock expiry, every notification, DEREGISTER), CONTROLLER_AVAILABLE, the listener's probes, MAAP and SRP. ADP is covered by its enable. The answering lanes are closed too.
- It closes only after the DEPARTING is built, not at the SHUTDOWN. A producer held at the gate keeps its shared TX slot (the originator's timer arms only at the serializer), so a gate closed at the SHUTDOWN can leave ADP no slot. Then no DEPARTING and no request come: RBT11 shows the deadlock.
- The SUCCESS response, the notifications and the DEPARTINGs are all still sent.
Tests: section RBT has 127 checks, 0 failures (RBT1 to RBT8 kept).
- RBT9 is the all-frame assertion from the final DEPARTING through a reset withheld 75 s. Lock expiry, AVB-info/path/grandmaster/counter changes, a queued command and later commands, a bound sink with a discovered talker, internal MAAP, SRP and a link bounce are all live. The MAC holds the DEPARTING's last byte 1.5 s first. No byte is offered on tx_* until the reset. The unsolicited AECP lane, the listener, MAAP and SRP each asked to send. After the reset the entity advertises again.
- RBT10 does the same for CONTROLLER_AVAILABLE in its own 65 s window.
- RBT11 takes every TX slot at the SHUTDOWN; the DEPARTING and the request still follow.
Arms: 13 new gate arms, all KILLED by name. They drop the gate, close it only with the request, let each producer through (notifications, originator, listener, MAAP, SRP), re-enable ADP, let each answering lane through with its command gates dropped, close the gate at the SHUTDOWN, and close it on the DEPARTING or the notifications. rbt-rx-gate-dropped and rbt-engine-hold-dropped keep their plants and are named by RBT7 and by the engine's command count, because RBT6's late answers now reach no wire. All 30 REBOOT counts equal their README cells.
Gates at the head, all rc 0:
- make check; run_suites (1,030,893 checks, 0 failing); check-req-tags (executed, 262 lines); lint_hdl (5.052, 5.050); syn/yosys/run.sh; elab guards 93.
- Mutant campaigns: aecp_dispatch (5 controls, 99 of 99), aecp 67, d3 110 of 110 (two parts, reconciled), notify 137 of 137, ctr 18, acmp 101 of 101, gsi 30, name-wr, elab-guard mutants 160 of 160, aecp_cmds 17 of 17, adp_engine 62.
Consumer gate: the scratch parent (local clone of milan-fpga dev 1e80128f, never pushed), pinned to this head with the port left unconnected.
- Full sweep: 64 suites, each once, 2,191,694 checks, 0 in-suite failures. The first run's shards shared CPUs with the campaigns and hit the wall clock, so each shard was re-run whole with SUITE_TIMEOUT=7200.
- 38 static, behave, elaboration and documentation gates pass.
- OOC area against dev: -257 LUT, +9 FF.
- No new adoption step beyond round 1's four.
- No top-level port, parameter or register-map change in this round, so no STOP.
