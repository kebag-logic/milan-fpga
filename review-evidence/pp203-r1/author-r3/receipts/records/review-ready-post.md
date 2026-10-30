[A699c] REVIEW READY
Head: 013ee63fd42455987ddbbbeb3b66f5af106b5793 on branch 203-aecp-reboot. That is two commits on top of round 2's ec1ff275a72d885f0908fd213d8009e9e4dda4d9 (base main f65c8ff7c673aaa8e2ea8da654f081ddb13588d8). No rebase, not pushed. The PR body is prepared at this head's figures, with "Closes #203".
R731-F1 = R732-F3, the request after the last frame started:
- KL_pp_tx_arbiter gets an internal output, busy_o = arb_st_r != A_IDLE. It is high from a frame's selection to the clock the MAC takes its last byte, with no grant outstanding outside it.
- RB_DEP now leaves on !adp_tx_busy_w && (laneq_adp_cnt_r == 0) && !arb_busy_w. This replaces ADP's own frame in flight, a strict subset of it.
- With or without a DEPARTING, reboot_req_o rises only after the last frame the processor started has had its EOF taken at the MAC face. The exit is taken with the transmit gate closed and ADP's queue empty, so no frame is being selected, and none starts after it.
- The SUCCESS response and the notifications stay first: RB_RESP and RB_NTF are unchanged.
- No top-level port, parameter or register-map change (no STOP).
Tests: section RBT has 155 checks, 0 failures (RBT1 to RBT11 kept).
- RBT12 is R731's probe, made permanent: not advertising, the lock expiring while the MAC holds the REBOOT notification 1 s. RBT13 is R732's: not advertising, eight sinks probing, every standard TX slot taken.
- In both, another lane's frame (the unlock notification; the listener's CONNECT_TX_COMMAND) is in flight as the round ends, and the MAC holds its last byte 20 ms. The request stays 0 meanwhile and rises after that byte. From the rise through a reset withheld 5 s no byte is offered on tx_*.
- RBT7 now also checks that every TX lane is open while the response's last byte is held.
- tb/tx_arbiter (67 checks) compares busy_o with its model's owner every clock.
Arms: 31 REBOOT arms, all KILLED by name, each count equal to its README cell.
- rbt-last-frame-unwatched drops the wait for busy_o and is named by RBT12. rbt-last-byte-offered takes the last byte offered for taken and is named by RBT13. Each also fails the other row.
- rbt-departing-flight-unwatched became rbt-last-frame-unwatched.
- rbt-response-unwatched and rbt-notification-flight-unwatched keep their plants. With the drain they no longer move the request; they close the gate while the MAC holds that frame. They are named by the open-gate checks of RBT7 and RBT12.
The reviewers' probes, unchanged, pass at the head: R731's window probe (PRB-NA: the request at 105515, after the last byte at 105513; PRB-ADV), R732's post-DEPARTING probe (156 checks, 0 failures) and R732's non-advertising probe (162, 0).
Gates at the head, all rc 0:
- make check; run_suites (1,030,922 checks, 0 failing); check-req-tags (executed, 264 lines); lint_hdl (5.052, 5.050); syn/yosys/run.sh; elab guards 93.
- Mutant campaigns, each in one run: aecp_dispatch (5 controls, 100 of 100), acmp 101 of 101, notify 137 of 137, d3 110 of 110, aecp 67, gsi 30, elab-guard mutants 160 of 160, ctr 18, aecp_cmds 17 of 17, adp_engine 62, name-wr.
Consumer gate: the scratch parent (local clone of milan-fpga dev 1e80128f, never pushed), pinned to this head with the port left unconnected.
- Full sweep in four shards: 64 suites, 0 failed, 0 timed out, 2,191,694 checks, 0 in-suite failures.
- 38 static, behave, elaboration and documentation gates pass.
- OOC area against dev: -385 LUT, +7 FF. ROM digests unchanged from round 2.
- No new adoption step beyond round 1's four.
R732-F4: PR-BODY.md restates every figure at this head and labels rounds 1 and 2's as superseded. The author's source and scratch-consumer evidence is kept apart from the manager's candidate.
