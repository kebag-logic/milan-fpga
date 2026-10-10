# [A578] B14 bench handoff

Refs #608 #645 #647 #667 #682 #686 #691

- Base: `5603c353137e90c1fa95429f6d00ef7a2298d9ee` (dev, the flashed image, seed eppo).
- Branch: `608-b14-bench`, head `6ec1a3a9a827575a84fb60d42ad3b085ecb70f19` (three one-line commits on the base; local, not pushed). Findings page: `docs/findings/B14_BENCH_5603C353.md`; no other doc edit.
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-6085135051
- TAKEN (session 1, not posted again): https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-6087724820
- Session 1 STOP (controller host down): https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-6088157558 (files under `session1/`).
- Session 2 STOP (SoC board console at a login prompt): https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-6093984746 (files under `session2/`).
- Manager ruling (round 1c): https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-6094000332. Continue from item 2 without the SoC board; its console untouched; the identity gate not repeated unless a host or the board changes state; rebuild B13's controller fork and verify its source hash.
- Session 3 (round 1c): 2026-10-10 05:00 to 08:55 UTC. REVIEW READY: see Posts.

## Status

**All items run or ruled NOT RUN with a reason; bench restored and read back; lock free; nothing left running on any host.**

| Item | Planned | Completed | Result | Evidence |
|---|---:|---:|---|---|
| 1 Identity | 1 | 1 | PASS (session 2, 04:54 UTC); not repeated (no host or board state change) | identity/ |
| 2 INTERNAL to AAF | 10 | 10 | PASS against the declared transient: 1-3 frames before the settle boundary, 0 after; settle-recentre count NOT OBSERVABLE (no silicon counter) | item2/ |
| 2 AAF to CRF | 10 | 10 | PASS: no slip; MEDIA_UNLOCKED 0 while following; tap clean | item2/ |
| 3 DUT-talker withdrawals | 100 | 100 (+1 pilot) | PASS 100/100 stop within one PDU of Lv; START/STOP +1/+1 100/100; 0 DUT LeaveAll in 894 s | item3/ |
| 4 Talker starts | 100 | 100 | EARLY 0/100, LATE 0/100; first step 124,999-125,020 ns (B13: 14/100 EARLY) | item4/ |
| 5 Default map and soak | maps + 120 min | maps + 7,200.5 s | Maps 4 and 8; soak 121 polls, 0 error-class increments; three observations | soak/ |
| 6 Ethernet receive sanity | soak | soak | Link PASS; RX error counters NOT RUN (RMON needs a STATS_CTRL write) | soak/summary.json |
| 7 MAAP interoperation | 1 | soak | ANNOUNCE interop PASS, no overlap; acquisition and DEFEND NOT RUN | maap/ |
| 8 Restore | all | all | PASS: 44/44 inventory rows; residuals below | restore/ |

## Session 3 ledger (one row per check, build step, locked action, switch, cycle, start or poll; UTC, 2026-10-10)

| Cycle | UTC | Item | Observation | Result | Evidence |
|---|---|---|---|---|---|
| s3-host-001 | 05:04:33 | - | This host: board link address present; audio cards present; serial adapters present; bench lock free. Controller: up 19 min (booted 04:45, no change since session 2), AVB interface up, no gPTP daemon, sudo OK | OK | precheck/host-checks-s3.json |
| s3-build-001 | 05:06-05:11 | - | Library fork a71ffa99 exported with `git archive`: `source.tar` 8,519,680 B, sha256 `23ac438f...`, equal to B13's source hash; submodule archives at the gitlinks, each archive's commit id equal to its gitlink | OK | tools/build-inputs-s3.json |
| s3-build-002 | 05:11-05:20 | - | Controller: configure rc 0; build rc 0 (57 steps); B13's probe.cpp (sha256 `0074a28f...`) compiled rc 0; sizes equal B13's | OK | tools/build-receipt-s3.txt |
| s3-host-002 | 05:13:36 | - | Tap host: tap interface up, no tcpdump running, sudo OK, /tmp 3.7 G free | OK | precheck/host-checks-s3.json |
| item2-setup | 05:17:01.035-05:17:01.684 (locked) | 2 | As-found read, refused before any change: peer in 0 already bound (to the DUT's AAF), peer clock source 1 | REFUSED, nothing changed | item2/setup/ |
| asfound-001 | 05:17:53.221-05:17:53.595 (locked) | - | Read-only: peer CLOCK_SOURCE 0-5; source 1 = INPUT_STREAM on its in 8 | OK | restore/peer-clock-sources.jsonl |
| asfound-002 | 05:18:32.590-05:18:33.582 (locked) | - | Read-only GET_RX_STATE on 10 peer and 2 DUT listeners: peer in 0 <- DUT out 0, peer in 8 <- DUT out 1 (flags 0x0082), others unbound; peer follows its in 8; DUT at INTERNAL | OK | restore/asfound-rx.jsonl |
| item2-setup2 | 05:20:08.010-05:20:15.815 (locked) | 2 | Peer clock set 0 (read back 0); B8's first bind kept; binding rule (no format change); bound peer CRF -> DUT in 1 and peer AAF -> DUT in 0; output map already holds B8's 8 mappings | OK | item2/setup2/ |
| item2-cyc01 | 05:20:24.650-05:25:04.740 (locked) | 2 | Invocation cyc01: two cycles, console poll 0.5 s, agent, four tap captures | ACTION_RC=0 | item2/cyc01/ |
| item2-c01-aaf | within the invocation | 2 | set SUCCESS read back 2; LOCKED 6.705-7.205 s; SLIP_LB +6 before the boundary, 0/0 after; SLIP_TDM 0; rails 0-0; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c01-crf | within the invocation | 2 | set SUCCESS read back 1; LOCKED 2.832-3.333 s; SLIP_LB +0 before the boundary, 0/0 after; SLIP_TDM 0; rails 0-0; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c01-int | within the invocation | 2 | set SUCCESS read back 0; servo IDLE [0.0, 0.253]; SLIP_LB +0 (INTERNAL, not following) | OK (not graded) | item2/summary/switches.json |
| item2-c02-aaf | within the invocation | 2 | set SUCCESS read back 2; LOCKED 6.513-7.013 s; SLIP_LB +4 before the boundary, 0/0 after; SLIP_TDM 0; rails 0-0; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c02-crf | within the invocation | 2 | set SUCCESS read back 1; LOCKED 2.709-3.209 s; SLIP_LB +0 before the boundary, 0/0 after; SLIP_TDM 0; rails 0-0; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c02-int | within the invocation | 2 | set SUCCESS read back 0; servo IDLE [0.0, 0.121]; SLIP_LB +0 (INTERNAL, not following) | OK (not graded) | item2/summary/switches.json |
| item2-cyc03 | 05:26:02.000-05:30:42.327 (locked) | 2 | Invocation cyc03: two cycles, console poll 0.5 s, agent, four tap captures | ACTION_RC=0 | item2/cyc03/ |
| item2-c03-aaf | within the invocation | 2 | set SUCCESS read back 2; LOCKED 6.619-7.119 s; SLIP_LB +4 before the boundary, 0/0 after; SLIP_TDM 0; rails 4-4; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c03-crf | within the invocation | 2 | set SUCCESS read back 1; LOCKED 2.895-3.402 s; SLIP_LB +0 before the boundary, 0/0 after; SLIP_TDM 0; rails 4-4; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c03-int | within the invocation | 2 | set SUCCESS read back 0; servo IDLE [0.0, 0.298]; SLIP_LB +0 (INTERNAL, not following) | OK (not graded) | item2/summary/switches.json |
| item2-c04-aaf | within the invocation | 2 | set SUCCESS read back 2; LOCKED 6.593-7.098 s; SLIP_LB +6 before the boundary, 0/0 after; SLIP_TDM 0; rails 4-4; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c04-crf | within the invocation | 2 | set SUCCESS read back 1; LOCKED 2.846-3.346 s; SLIP_LB +0 before the boundary, 0/0 after; SLIP_TDM 0; rails 4-4; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c04-int | within the invocation | 2 | set SUCCESS read back 0; servo IDLE [0.0, 0.25]; SLIP_LB +0 (INTERNAL, not following) | OK (not graded) | item2/summary/switches.json |
| item2-cyc05 | 05:31:10.415-05:35:50.047 (locked) | 2 | Invocation cyc05: two cycles, console poll 0.5 s, agent, four tap captures | ACTION_RC=0 | item2/cyc05/ |
| item2-c05-aaf | within the invocation | 2 | set SUCCESS read back 2; LOCKED 6.223-6.726 s; SLIP_LB +4 before the boundary, 0/0 after; SLIP_TDM 0; rails 6-6; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c05-crf | within the invocation | 2 | set SUCCESS read back 1; LOCKED 2.838-3.352 s; SLIP_LB +0 before the boundary, 0/0 after; SLIP_TDM 0; rails 6-6; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c05-int | within the invocation | 2 | set SUCCESS read back 0; servo IDLE [0.0, 0.276]; SLIP_LB +2 (INTERNAL, not following) | OK (not graded) | item2/summary/switches.json |
| item2-c06-aaf | within the invocation | 2 | set SUCCESS read back 2; LOCKED 6.568-7.069 s; SLIP_LB +2 before the boundary, 0/0 after; SLIP_TDM 0; rails 7-7; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c06-crf | within the invocation | 2 | set SUCCESS read back 1; LOCKED 2.872-3.388 s; SLIP_LB +0 before the boundary, 0/0 after; SLIP_TDM 0; rails 7-7; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c06-int | within the invocation | 2 | set SUCCESS read back 0; servo IDLE [0.0, 0.287]; SLIP_LB +2 (INTERNAL, not following) | OK (not graded) | item2/summary/switches.json |
| item2-cyc07 | 05:35:56.175-05:40:35.770 (locked) | 2 | Invocation cyc07: two cycles, console poll 0.5 s, agent, four tap captures | ACTION_RC=0 | item2/cyc07/ |
| item2-c07-aaf | within the invocation | 2 | set SUCCESS read back 2; LOCKED 6.712-7.212 s; SLIP_LB +4 before the boundary, 0/0 after; SLIP_TDM 0; rails 8-8; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c07-crf | within the invocation | 2 | set SUCCESS read back 1; LOCKED 2.754-3.255 s; SLIP_LB +0 before the boundary, 0/0 after; SLIP_TDM 0; rails 8-8; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c07-int | within the invocation | 2 | set SUCCESS read back 0; servo IDLE [0.0, 0.104]; SLIP_LB +0 (INTERNAL, not following) | OK (not graded) | item2/summary/switches.json |
| item2-c08-aaf | within the invocation | 2 | set SUCCESS read back 2; LOCKED 6.625-7.126 s; SLIP_LB +4 before the boundary, 0/0 after; SLIP_TDM 0; rails 8-8; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c08-crf | within the invocation | 2 | set SUCCESS read back 1; LOCKED 2.868-3.369 s; SLIP_LB +0 before the boundary, 0/0 after; SLIP_TDM 0; rails 8-8; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c08-int | within the invocation | 2 | set SUCCESS read back 0; servo IDLE [0.0, 0.222]; SLIP_LB +0 (INTERNAL, not following) | OK (not graded) | item2/summary/switches.json |
| item2-cyc09 | 05:40:44.224-05:45:23.743 (locked) | 2 | Invocation cyc09: two cycles, console poll 0.5 s, agent, four tap captures | ACTION_RC=0 | item2/cyc09/ |
| item2-c09-aaf | within the invocation | 2 | set SUCCESS read back 2; LOCKED 6.21-6.715 s; SLIP_LB +4 before the boundary, 0/0 after; SLIP_TDM 0; rails 9-9; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c09-crf | within the invocation | 2 | set SUCCESS read back 1; LOCKED 2.792-3.292 s; SLIP_LB +0 before the boundary, 0/0 after; SLIP_TDM 0; rails 9-9; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c09-int | within the invocation | 2 | set SUCCESS read back 0; servo IDLE [0.0, 0.541]; SLIP_LB +2 (INTERNAL, not following) | OK (not graded) | item2/summary/switches.json |
| item2-c10-aaf | within the invocation | 2 | set SUCCESS read back 2; LOCKED 6.557-7.057 s; SLIP_LB +4 before the boundary, 0/0 after; SLIP_TDM 0; rails 9-9; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c10-crf | within the invocation | 2 | set SUCCESS read back 1; LOCKED 2.737-3.242 s; SLIP_LB +0 before the boundary, 0/0 after; SLIP_TDM 0; rails 9-9; tap gaps 0 | PASS | item2/summary/switches.json |
| item2-c10-int | within the invocation | 2 | set SUCCESS read back 0; servo IDLE [0.0, 0.13]; SLIP_LB +0 (INTERNAL, not following) | OK (not graded) | item2/summary/switches.json |
| item2-teardown | 05:45:34.141-05:45:36.963 (locked) | 2/8 | DUT clock source read 0; unbound peer AAF -> DUT in 0 and peer CRF -> DUT in 1; peer clock source set 1, read back 1; formats, maps and listener states equal as found (15 of 15) | ACTION_RC=0 | item2/teardown/ |
| item3-setup | 05:48:58.839-05:48:59.043 (locked) | 3 | As found: peer clock 1, DUT clock 0, DUT out 1 -> peer in 8 bound (kept), DUT in 1 free; peer clock set 0 (read back 0); binding rule (formats equal); bound peer CRF -> DUT in 1; DUT clock set 1 (read back 1) | ACTION_RC=0 | item3/setup in raw-index/other.jsonl |
| item3-cycle-001 | 05:49:08.228-05:49:17.551 (locked) | 3 | Lv 8.506 ms after the response; last PDU -0.090 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 44.4 ms pilot: capture rc 137, not graded | PASS | item3/cycles/cycle-001/ |
| item3-cycle-002 | 05:51:22.249-05:51:31.767 (locked) | 3 | Lv 8.884 ms after the response; last PDU -1.729 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 105.7 ms | PASS | item3/cycles/cycle-002/ |
| item3-cycle-003 | 05:51:31.865-05:51:41.871 (locked) | 3 | Lv 8.711 ms after the response; last PDU -1.435 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.0 ms | PASS | item3/cycles/cycle-003/ |
| item3-cycle-004 | 05:51:41.975-05:51:51.941 (locked) | 3 | Lv 9.258 ms after the response; last PDU -1.717 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.7 ms | PASS | item3/cycles/cycle-004/ |
| item3-cycle-005 | 05:51:52.046-05:52:02.089 (locked) | 3 | Lv 8.786 ms after the response; last PDU -1.121 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.4 ms | PASS | item3/cycles/cycle-005/ |
| item3-cycle-006 | 05:52:02.208-05:52:12.199 (locked) | 3 | Lv 9.269 ms after the response; last PDU -1.369 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.0 ms | PASS | item3/cycles/cycle-006/ |
| item3-cycle-007 | 05:52:12.302-05:52:22.310 (locked) | 3 | Lv 8.869 ms after the response; last PDU -0.717 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.7 ms | PASS | item3/cycles/cycle-007/ |
| item3-cycle-008 | 05:52:22.425-05:52:32.465 (locked) | 3 | Lv 9.331 ms after the response; last PDU -1.046 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 10.4 ms | PASS | item3/cycles/cycle-008/ |
| item3-cycle-009 | 05:52:32.572-05:52:42.557 (locked) | 3 | Lv 8.849 ms after the response; last PDU -0.307 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.1 ms | PASS | item3/cycles/cycle-009/ |
| item3-cycle-010 | 05:52:42.678-05:52:51.740 (locked) | 3 | Lv 8.771 ms after the response; last PDU -1.982 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 10.8 ms | PASS | item3/cycles/cycle-010/ |
| item3-cycle-011 | 05:52:51.850-05:53:00.947 (locked) | 3 | Lv 8.411 ms after the response; last PDU -0.512 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.9 ms | PASS | item3/cycles/cycle-011/ |
| item3-cycle-012 | 05:53:01.099-05:53:11.171 (locked) | 3 | Lv 10.516 ms after the response; last PDU -0.367 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 62.2 ms | PASS | item3/cycles/cycle-012/ |
| item3-cycle-013 | 05:53:11.274-05:53:21.309 (locked) | 3 | Lv 8.852 ms after the response; last PDU -1.563 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 10.9 ms | PASS | item3/cycles/cycle-013/ |
| item3-cycle-014 | 05:53:21.411-05:53:31.408 (locked) | 3 | Lv 8.398 ms after the response; last PDU -0.860 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.5 ms | PASS | item3/cycles/cycle-014/ |
| item3-cycle-015 | 05:53:31.513-05:53:41.549 (locked) | 3 | Lv 9.051 ms after the response; last PDU -1.290 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.3 ms | PASS | item3/cycles/cycle-015/ |
| item3-cycle-016 | 05:53:41.656-05:53:51.645 (locked) | 3 | Lv 8.491 ms after the response; last PDU -1.574 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 10.9 ms | PASS | item3/cycles/cycle-016/ |
| item3-cycle-017 | 05:53:51.750-05:54:01.763 (locked) | 3 | Lv 8.876 ms after the response; last PDU -1.837 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.6 ms | PASS | item3/cycles/cycle-017/ |
| item3-cycle-018 | 05:54:01.874-05:54:11.898 (locked) | 3 | Lv 9.319 ms after the response; last PDU -0.176 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.3 ms | PASS | item3/cycles/cycle-018/ |
| item3-cycle-019 | 05:54:12.011-05:54:22.007 (locked) | 3 | Lv 8.736 ms after the response; last PDU -1.462 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.0 ms | PASS | item3/cycles/cycle-019/ |
| item3-cycle-020 | 05:54:22.130-05:54:32.144 (locked) | 3 | Lv 9.926 ms after the response; last PDU -0.524 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.7 ms | PASS | item3/cycles/cycle-020/ |
| item3-cycle-021 | 05:54:32.270-05:54:42.294 (locked) | 3 | Lv 8.475 ms after the response; last PDU -1.072 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.4 ms | PASS | item3/cycles/cycle-021/ |
| item3-cycle-022 | 05:54:42.401-05:54:52.418 (locked) | 3 | Lv 9.044 ms after the response; last PDU -1.377 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.0 ms | PASS | item3/cycles/cycle-022/ |
| item3-cycle-023 | 05:54:52.522-05:55:02.575 (locked) | 3 | Lv 8.465 ms after the response; last PDU -0.713 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.8 ms | PASS | item3/cycles/cycle-023/ |
| item3-cycle-024 | 05:55:02.701-05:55:12.766 (locked) | 3 | Lv 8.905 ms after the response; last PDU -0.004 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 13.5 ms | PASS | item3/cycles/cycle-024/ |
| item3-cycle-025 | 05:55:12.899-05:55:22.938 (locked) | 3 | Lv 11.321 ms after the response; last PDU -1.302 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.2 ms | PASS | item3/cycles/cycle-025/ |
| item3-cycle-026 | 05:55:23.044-05:55:33.105 (locked) | 3 | Lv 84.466 ms after the response; last PDU -0.300 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.9 ms | PASS | item3/cycles/cycle-026/ |
| item3-cycle-027 | 05:55:33.232-05:55:43.261 (locked) | 3 | Lv 9.128 ms after the response; last PDU -1.842 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.6 ms | PASS | item3/cycles/cycle-027/ |
| item3-cycle-028 | 05:55:43.364-05:55:53.381 (locked) | 3 | Lv 8.616 ms after the response; last PDU -1.202 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.3 ms | PASS | item3/cycles/cycle-028/ |
| item3-cycle-029 | 05:55:53.486-05:56:03.546 (locked) | 3 | Lv 8.946 ms after the response; last PDU -1.422 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.0 ms | PASS | item3/cycles/cycle-029/ |
| item3-cycle-030 | 05:56:03.673-05:56:13.720 (locked) | 3 | Lv 8.489 ms after the response; last PDU -0.729 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.7 ms | PASS | item3/cycles/cycle-030/ |
| item3-cycle-031 | 05:56:13.836-05:56:23.919 (locked) | 3 | Lv 9.109 ms after the response; last PDU -0.207 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.4 ms | PASS | item3/cycles/cycle-031/ |
| item3-cycle-032 | 05:56:24.037-05:56:34.077 (locked) | 3 | Lv 9.349 ms after the response; last PDU -1.320 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.2 ms | PASS | item3/cycles/cycle-032/ |
| item3-cycle-033 | 05:56:34.199-05:56:44.263 (locked) | 3 | Lv 8.780 ms after the response; last PDU -0.614 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.9 ms | PASS | item3/cycles/cycle-033/ |
| item3-cycle-034 | 05:56:44.390-05:56:54.454 (locked) | 3 | Lv 8.485 ms after the response; last PDU -0.819 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.6 ms | PASS | item3/cycles/cycle-034/ |
| item3-cycle-035 | 05:56:54.560-05:57:04.605 (locked) | 3 | Lv 8.710 ms after the response; last PDU -0.171 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.3 ms | PASS | item3/cycles/cycle-035/ |
| item3-cycle-036 | 05:57:04.710-05:57:14.700 (locked) | 3 | Lv 9.396 ms after the response; last PDU -0.729 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 13.0 ms | PASS | item3/cycles/cycle-036/ |
| item3-cycle-037 | 05:57:14.808-05:57:24.859 (locked) | 3 | Lv 8.768 ms after the response; last PDU -1.993 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.7 ms | PASS | item3/cycles/cycle-037/ |
| item3-cycle-038 | 05:57:24.962-05:57:34.948 (locked) | 3 | Lv 8.914 ms after the response; last PDU -1.014 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.4 ms | PASS | item3/cycles/cycle-038/ |
| item3-cycle-039 | 05:57:35.052-05:57:45.035 (locked) | 3 | Lv 8.484 ms after the response; last PDU -1.458 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.0 ms | PASS | item3/cycles/cycle-039/ |
| item3-cycle-040 | 05:57:45.159-05:57:55.225 (locked) | 3 | Lv 8.829 ms after the response; last PDU -0.678 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.7 ms | PASS | item3/cycles/cycle-040/ |
| item3-cycle-041 | 05:57:55.332-05:58:05.347 (locked) | 3 | Lv 9.322 ms after the response; last PDU -0.033 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.4 ms | PASS | item3/cycles/cycle-041/ |
| item3-cycle-042 | 05:58:12.217-05:58:22.258 (locked) | 3 | Lv 9.239 ms after the response; last PDU -1.590 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 125.9 ms | PASS | item3/cycles/cycle-042/ |
| item3-cycle-043 | 05:58:22.362-05:58:32.421 (locked) | 3 | Lv 9.117 ms after the response; last PDU -1.346 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.6 ms | PASS | item3/cycles/cycle-043/ |
| item3-cycle-044 | 05:58:32.532-05:58:42.518 (locked) | 3 | Lv 9.027 ms after the response; last PDU -1.122 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.3 ms | PASS | item3/cycles/cycle-044/ |
| item3-cycle-045 | 05:58:42.623-05:58:52.661 (locked) | 3 | Lv 11.873 ms after the response; last PDU -0.834 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.0 ms | PASS | item3/cycles/cycle-045/ |
| item3-cycle-046 | 05:58:52.764-05:59:02.797 (locked) | 3 | Lv 9.034 ms after the response; last PDU -1.744 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.7 ms | PASS | item3/cycles/cycle-046/ |
| item3-cycle-047 | 05:59:02.899-05:59:12.908 (locked) | 3 | Lv 8.458 ms after the response; last PDU -1.056 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.4 ms | PASS | item3/cycles/cycle-047/ |
| item3-cycle-048 | 05:59:13.012-05:59:22.071 (locked) | 3 | Lv 8.884 ms after the response; last PDU -0.344 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 13.1 ms | PASS | item3/cycles/cycle-048/ |
| item3-cycle-049 | 05:59:22.191-05:59:32.188 (locked) | 3 | Lv 8.874 ms after the response; last PDU -0.208 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 13.2 ms | PASS | item3/cycles/cycle-049/ |
| item3-cycle-050 | 05:59:32.294-05:59:42.307 (locked) | 3 | Lv 8.457 ms after the response; last PDU -0.558 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.9 ms | PASS | item3/cycles/cycle-050/ |
| item3-cycle-051 | 05:59:42.620-05:59:52.600 (locked) | 3 | Lv 10.186 ms after the response; last PDU -1.144 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 10.7 ms | PASS | item3/cycles/cycle-051/ |
| item3-cycle-052 | 05:59:52.705-06:00:02.711 (locked) | 3 | Lv 9.259 ms after the response; last PDU -1.106 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.4 ms | PASS | item3/cycles/cycle-052/ |
| item3-cycle-053 | 06:00:02.835-06:00:12.815 (locked) | 3 | Lv 8.696 ms after the response; last PDU -0.409 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.0 ms | PASS | item3/cycles/cycle-053/ |
| item3-cycle-054 | 06:00:12.917-06:00:22.950 (locked) | 3 | Lv 9.254 ms after the response; last PDU -1.712 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.7 ms | PASS | item3/cycles/cycle-054/ |
| item3-cycle-055 | 06:00:23.053-06:00:33.046 (locked) | 3 | Lv 8.693 ms after the response; last PDU -1.040 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.4 ms | PASS | item3/cycles/cycle-055/ |
| item3-cycle-056 | 06:00:33.151-06:00:43.146 (locked) | 3 | Lv 95.701 ms after the response; last PDU -0.908 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.1 ms | PASS | item3/cycles/cycle-056/ |
| item3-cycle-057 | 06:00:43.248-06:00:53.256 (locked) | 3 | Lv 8.510 ms after the response; last PDU -0.750 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.8 ms | PASS | item3/cycles/cycle-057/ |
| item3-cycle-058 | 06:00:53.362-06:01:03.346 (locked) | 3 | Lv 9.174 ms after the response; last PDU -1.021 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.4 ms | PASS | item3/cycles/cycle-058/ |
| item3-cycle-059 | 06:01:03.452-06:01:12.469 (locked) | 3 | Lv 8.610 ms after the response; last PDU -0.323 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.1 ms | PASS | item3/cycles/cycle-059/ |
| item3-cycle-060 | 06:01:12.571-06:01:22.581 (locked) | 3 | Lv 8.628 ms after the response; last PDU -0.211 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.3 ms | PASS | item3/cycles/cycle-060/ |
| item3-cycle-061 | 06:01:22.685-06:01:32.718 (locked) | 3 | Lv 10.854 ms after the response; last PDU -1.204 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.9 ms | PASS | item3/cycles/cycle-061/ |
| item3-cycle-062 | 06:01:32.821-06:01:42.861 (locked) | 3 | Lv 8.647 ms after the response; last PDU -1.859 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.6 ms | PASS | item3/cycles/cycle-062/ |
| item3-cycle-063 | 06:01:42.965-06:01:53.038 (locked) | 3 | Lv 9.032 ms after the response; last PDU -0.130 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 13.3 ms | PASS | item3/cycles/cycle-063/ |
| item3-cycle-064 | 06:01:53.145-06:02:03.152 (locked) | 3 | Lv 9.370 ms after the response; last PDU -0.329 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.0 ms | PASS | item3/cycles/cycle-064/ |
| item3-cycle-065 | 06:02:03.258-06:02:13.336 (locked) | 3 | Lv 9.031 ms after the response; last PDU -0.744 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.7 ms | PASS | item3/cycles/cycle-065/ |
| item3-cycle-066 | 06:02:13.453-06:02:23.502 (locked) | 3 | Lv 8.400 ms after the response; last PDU -0.984 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.4 ms | PASS | item3/cycles/cycle-066/ |
| item3-cycle-067 | 06:02:23.619-06:02:33.688 (locked) | 3 | Lv 8.829 ms after the response; last PDU -0.290 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.2 ms | PASS | item3/cycles/cycle-067/ |
| item3-cycle-068 | 06:02:33.812-06:02:43.810 (locked) | 3 | Lv 9.229 ms after the response; last PDU -0.576 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 10.9 ms | PASS | item3/cycles/cycle-068/ |
| item3-cycle-069 | 06:02:43.941-06:02:53.955 (locked) | 3 | Lv 8.728 ms after the response; last PDU -1.812 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 10.6 ms | PASS | item3/cycles/cycle-069/ |
| item3-cycle-070 | 06:02:54.095-06:03:04.157 (locked) | 3 | Lv 10.316 ms after the response; last PDU -0.167 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.3 ms | PASS | item3/cycles/cycle-070/ |
| item3-cycle-071 | 06:03:04.274-06:03:14.273 (locked) | 3 | Lv 8.736 ms after the response; last PDU -0.459 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.0 ms | PASS | item3/cycles/cycle-071/ |
| item3-cycle-072 | 06:03:14.391-06:03:24.421 (locked) | 3 | Lv 8.839 ms after the response; last PDU -0.809 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.7 ms | PASS | item3/cycles/cycle-072/ |
| item3-cycle-073 | 06:03:24.548-06:03:34.597 (locked) | 3 | Lv 8.452 ms after the response; last PDU -0.053 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.4 ms | PASS | item3/cycles/cycle-073/ |
| item3-cycle-074 | 06:03:34.740-06:03:44.794 (locked) | 3 | Lv 9.157 ms after the response; last PDU -1.400 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.1 ms | PASS | item3/cycles/cycle-074/ |
| item3-cycle-075 | 06:03:44.913-06:03:54.987 (locked) | 3 | Lv 8.433 ms after the response; last PDU -1.529 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 10.8 ms | PASS | item3/cycles/cycle-075/ |
| item3-cycle-076 | 06:03:55.175-06:04:05.233 (locked) | 3 | Lv 8.970 ms after the response; last PDU -0.816 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.6 ms | PASS | item3/cycles/cycle-076/ |
| item3-cycle-077 | 06:04:05.339-06:04:15.384 (locked) | 3 | Lv 8.724 ms after the response; last PDU -1.446 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.3 ms | PASS | item3/cycles/cycle-077/ |
| item3-cycle-078 | 06:04:15.488-06:04:25.505 (locked) | 3 | Lv 8.959 ms after the response; last PDU -1.430 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 18.0 ms | PASS | item3/cycles/cycle-078/ |
| item3-cycle-079 | 06:04:25.610-06:04:35.594 (locked) | 3 | Lv 8.417 ms after the response; last PDU -1.754 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 10.7 ms | PASS | item3/cycles/cycle-079/ |
| item3-cycle-080 | 06:04:35.713-06:04:45.779 (locked) | 3 | Lv 8.866 ms after the response; last PDU -1.103 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.4 ms | PASS | item3/cycles/cycle-080/ |
| item3-cycle-081 | 06:04:45.881-06:04:55.897 (locked) | 3 | Lv 8.634 ms after the response; last PDU -1.594 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 13.0 ms | PASS | item3/cycles/cycle-081/ |
| item3-cycle-082 | 06:04:56.000-06:05:06.048 (locked) | 3 | Lv 8.988 ms after the response; last PDU -1.825 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 13.8 ms | PASS | item3/cycles/cycle-082/ |
| item3-cycle-083 | 06:05:06.174-06:05:16.240 (locked) | 3 | Lv 9.217 ms after the response; last PDU -1.941 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.5 ms | PASS | item3/cycles/cycle-083/ |
| item3-cycle-084 | 06:05:16.363-06:05:26.375 (locked) | 3 | Lv 8.763 ms after the response; last PDU -0.220 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.2 ms | PASS | item3/cycles/cycle-084/ |
| item3-cycle-085 | 06:05:26.483-06:05:36.488 (locked) | 3 | Lv 9.226 ms after the response; last PDU -1.561 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.9 ms | PASS | item3/cycles/cycle-085/ |
| item3-cycle-086 | 06:05:36.592-06:05:46.658 (locked) | 3 | Lv 8.758 ms after the response; last PDU -0.860 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.6 ms | PASS | item3/cycles/cycle-086/ |
| item3-cycle-087 | 06:05:46.763-06:05:56.770 (locked) | 3 | Lv 9.226 ms after the response; last PDU -1.203 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.3 ms | PASS | item3/cycles/cycle-087/ |
| item3-cycle-088 | 06:05:56.874-06:06:06.894 (locked) | 3 | Lv 8.838 ms after the response; last PDU -0.673 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.9 ms | PASS | item3/cycles/cycle-088/ |
| item3-cycle-089 | 06:06:07.013-06:06:17.068 (locked) | 3 | Lv 9.405 ms after the response; last PDU -0.127 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 13.7 ms | PASS | item3/cycles/cycle-089/ |
| item3-cycle-090 | 06:06:21.884-06:06:31.962 (locked) | 3 | Lv 9.100 ms after the response; last PDU -1.449 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.0 ms | PASS | item3/cycles/cycle-090/ |
| item3-cycle-091 | 06:06:32.084-06:06:42.155 (locked) | 3 | Lv 8.490 ms after the response; last PDU -0.714 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.8 ms | PASS | item3/cycles/cycle-091/ |
| item3-cycle-092 | 06:06:42.282-06:06:52.345 (locked) | 3 | Lv 9.032 ms after the response; last PDU -1.985 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 13.5 ms | PASS | item3/cycles/cycle-092/ |
| item3-cycle-093 | 06:06:52.469-06:07:02.522 (locked) | 3 | Lv 8.611 ms after the response; last PDU -0.444 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.2 ms | PASS | item3/cycles/cycle-093/ |
| item3-cycle-094 | 06:07:02.628-06:07:12.689 (locked) | 3 | Lv 8.988 ms after the response; last PDU -1.583 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.9 ms | PASS | item3/cycles/cycle-094/ |
| item3-cycle-095 | 06:07:12.792-06:07:22.796 (locked) | 3 | Lv 8.409 ms after the response; last PDU -1.869 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.6 ms | PASS | item3/cycles/cycle-095/ |
| item3-cycle-096 | 06:07:22.898-06:07:32.938 (locked) | 3 | Lv 8.780 ms after the response; last PDU -0.127 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.3 ms | PASS | item3/cycles/cycle-096/ |
| item3-cycle-097 | 06:07:33.058-06:07:43.144 (locked) | 3 | Lv 57.499 ms after the response; last PDU -0.832 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 13.0 ms | PASS | item3/cycles/cycle-097/ |
| item3-cycle-098 | 06:07:43.252-06:07:53.271 (locked) | 3 | Lv 8.778 ms after the response; last PDU -1.736 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 10.7 ms | PASS | item3/cycles/cycle-098/ |
| item3-cycle-099 | 06:07:53.373-06:08:03.359 (locked) | 3 | Lv 8.350 ms after the response; last PDU -0.062 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 12.4 ms | PASS | item3/cycles/cycle-099/ |
| item3-cycle-100 | 06:08:03.461-06:08:13.478 (locked) | 3 | Lv 8.961 ms after the response; last PDU -1.546 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 11.0 ms | PASS | item3/cycles/cycle-100/ |
| item3-cycle-101 | 06:08:13.595-06:08:23.665 (locked) | 3 | Lv 9.194 ms after the response; last PDU -0.670 ms from Lv; PDUs after Lv+T 0; START/STOP [1, 1]; restart 10.8 ms | PASS | item3/cycles/cycle-101/ |
| item3-restore | 06:08:53.346-06:08:53.717 (locked) | 3/8 | DUT clock 0 (read back); peer CRF -> DUT in 1 unbound; DUT out 1 -> peer in 8 bound, flags 0x0082; peer clock 1 (read back): equal to as found | ACTION_RC=0 | item3/summary.json |
| item4-release | 06:10:43.116-06:10:44.531 (locked) | 4 | Peer in 0 <- DUT out 0 (as found, flags 0x0082) unbound, read back 0 | ACTION_RC=0 | item4/asfound-release.jsonl |
| item4-starts-001 | 06:10:51.653-06:15:26.077 (locked) | 4 | Fifty starts, B13 probe, three captures each | ACTION_RC=0 | item4/ |
| item4-start-001 | 06:10:59.110 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 65; 3.241 s | PASS | item4/start-001.json |
| item4-start-002 | 06:11:04.571 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 132; 3.242 s | PASS | item4/start-002.json |
| item4-start-003 | 06:11:10.077 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 28; 3.239 s | PASS | item4/start-003.json |
| item4-start-004 | 06:11:15.578 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 192; 3.237 s | PASS | item4/start-004.json |
| item4-start-005 | 06:11:21.049 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 100; 3.241 s | PASS | item4/start-005.json |
| item4-start-006 | 06:11:26.492 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 8; 3.240 s | PASS | item4/start-006.json |
| item4-start-007 | 06:11:31.943 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 174; 3.239 s | PASS | item4/start-007.json |
| item4-start-008 | 06:11:37.346 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 81; 3.239 s | PASS | item4/start-008.json |
| item4-start-009 | 06:11:42.761 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 249; 3.241 s | PASS | item4/start-009.json |
| item4-start-010 | 06:11:48.119 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 157; 3.239 s | PASS | item4/start-010.json |
| item4-start-011 | 06:11:53.450 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 66; 3.237 s | PASS | item4/start-011.json |
| item4-start-012 | 06:11:58.766 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 235; 3.239 s | PASS | item4/start-012.json |
| item4-start-013 | 06:12:04.265 | 4 | EARLY 0; LATE 0; first step 125019 ns; first sequence 145; 3.239 s | PASS | item4/start-013.json |
| item4-start-014 | 06:12:09.722 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 54; 3.238 s | PASS | item4/start-014.json |
| item4-start-015 | 06:12:15.209 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 218; 3.239 s | PASS | item4/start-015.json |
| item4-start-016 | 06:12:20.693 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 126; 3.241 s | PASS | item4/start-016.json |
| item4-start-017 | 06:12:26.195 | 4 | EARLY 0; LATE 0; first step 125020 ns; first sequence 34; 3.241 s | PASS | item4/start-017.json |
| item4-start-018 | 06:12:31.585 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 198; 3.240 s | PASS | item4/start-018.json |
| item4-start-019 | 06:12:36.949 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 109; 3.237 s | PASS | item4/start-019.json |
| item4-start-020 | 06:12:42.301 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 17; 3.238 s | PASS | item4/start-020.json |
| item4-start-021 | 06:12:47.649 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 176; 3.239 s | PASS | item4/start-021.json |
| item4-start-022 | 06:12:53.073 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 84; 3.239 s | PASS | item4/start-022.json |
| item4-start-023 | 06:12:58.622 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 248; 3.239 s | PASS | item4/start-023.json |
| item4-start-024 | 06:13:04.170 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 156; 3.241 s | PASS | item4/start-024.json |
| item4-start-025 | 06:13:09.500 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 64; 3.241 s | PASS | item4/start-025.json |
| item4-start-026 | 06:13:14.882 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 62; 3.240 s | PASS | item4/start-026.json |
| item4-start-027 | 06:13:20.284 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 226; 3.238 s | PASS | item4/start-027.json |
| item4-start-028 | 06:13:25.645 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 134; 3.239 s | PASS | item4/start-028.json |
| item4-start-029 | 06:13:31.028 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 42; 3.239 s | PASS | item4/start-029.json |
| item4-start-030 | 06:13:36.390 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 206; 3.240 s | PASS | item4/start-030.json |
| item4-start-031 | 06:13:41.802 | 4 | EARLY 0; LATE 0; first step 125019 ns; first sequence 117; 3.241 s | PASS | item4/start-031.json |
| item4-start-032 | 06:13:47.254 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 27; 3.241 s | PASS | item4/start-032.json |
| item4-start-033 | 06:13:52.709 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 197; 3.241 s | PASS | item4/start-033.json |
| item4-start-034 | 06:13:58.198 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 113; 3.240 s | PASS | item4/start-034.json |
| item4-start-035 | 06:14:03.663 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 23; 3.238 s | PASS | item4/start-035.json |
| item4-start-036 | 06:14:09.182 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 187; 3.239 s | PASS | item4/start-036.json |
| item4-start-037 | 06:14:14.651 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 103; 3.240 s | PASS | item4/start-037.json |
| item4-start-038 | 06:14:19.973 | 4 | EARLY 0; LATE 0; first step 125019 ns; first sequence 3; 3.240 s | PASS | item4/start-038.json |
| item4-start-039 | 06:14:25.331 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 167; 3.241 s | PASS | item4/start-039.json |
| item4-start-040 | 06:14:30.679 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 78; 3.238 s | PASS | item4/start-040.json |
| item4-start-041 | 06:14:36.052 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 242; 3.237 s | PASS | item4/start-041.json |
| item4-start-042 | 06:14:41.450 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 150; 3.239 s | PASS | item4/start-042.json |
| item4-start-043 | 06:14:46.826 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 2; 3.237 s | PASS | item4/start-043.json |
| item4-start-044 | 06:14:52.205 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 169; 3.238 s | PASS | item4/start-044.json |
| item4-start-045 | 06:14:57.564 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 77; 3.240 s | PASS | item4/start-045.json |
| item4-start-046 | 06:15:03.025 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 241; 3.238 s | PASS | item4/start-046.json |
| item4-start-047 | 06:15:08.474 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 149; 3.241 s | PASS | item4/start-047.json |
| item4-start-048 | 06:15:13.880 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 65; 3.237 s | PASS | item4/start-048.json |
| item4-start-049 | 06:15:19.197 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 200; 3.237 s | PASS | item4/start-049.json |
| item4-start-050 | 06:15:24.546 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 100; 3.240 s | PASS | item4/start-050.json |
| item4-starts-051 | 06:15:31.950-06:20:07.178 (locked) | 4 | Fifty starts, B13 probe, three captures each | ACTION_RC=0 | item4/ |
| item4-start-051 | 06:15:41.166 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 8; 3.226 s | PASS | item4/start-051.json |
| item4-start-052 | 06:15:46.437 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 202; 3.227 s | PASS | item4/start-052.json |
| item4-start-053 | 06:15:51.830 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 65; 3.229 s | PASS | item4/start-053.json |
| item4-start-054 | 06:15:57.177 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 200; 3.229 s | PASS | item4/start-054.json |
| item4-start-055 | 06:16:02.611 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 68; 3.230 s | PASS | item4/start-055.json |
| item4-start-056 | 06:16:08.053 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 192; 3.230 s | PASS | item4/start-056.json |
| item4-start-057 | 06:16:13.502 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 68; 3.230 s | PASS | item4/start-057.json |
| item4-start-058 | 06:16:18.939 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 192; 3.229 s | PASS | item4/start-058.json |
| item4-start-059 | 06:16:24.278 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 60; 3.231 s | PASS | item4/start-059.json |
| item4-start-060 | 06:16:29.591 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 184; 3.227 s | PASS | item4/start-060.json |
| item4-start-061 | 06:16:34.955 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 52; 3.227 s | PASS | item4/start-061.json |
| item4-start-062 | 06:16:40.326 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 176; 3.230 s | PASS | item4/start-062.json |
| item4-start-063 | 06:16:45.630 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 47; 3.230 s | PASS | item4/start-063.json |
| item4-start-064 | 06:16:50.948 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 171; 3.228 s | PASS | item4/start-064.json |
| item4-start-065 | 06:16:56.230 | 4 | EARLY 0; LATE 0; first step 125019 ns; first sequence 47; 3.230 s | PASS | item4/start-065.json |
| item4-start-066 | 06:17:01.576 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 171; 3.227 s | PASS | item4/start-066.json |
| item4-start-067 | 06:17:06.883 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 42; 3.230 s | PASS | item4/start-067.json |
| item4-start-068 | 06:17:12.189 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 166; 3.231 s | PASS | item4/start-068.json |
| item4-start-069 | 06:17:17.499 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 34; 3.229 s | PASS | item4/start-069.json |
| item4-start-070 | 06:17:22.848 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 158; 3.231 s | PASS | item4/start-070.json |
| item4-start-071 | 06:17:28.285 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 28; 3.230 s | PASS | item4/start-071.json |
| item4-start-072 | 06:17:33.749 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 152; 3.228 s | PASS | item4/start-072.json |
| item4-start-073 | 06:17:39.184 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 12; 3.228 s | PASS | item4/start-073.json |
| item4-start-074 | 06:17:44.694 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 144; 3.227 s | PASS | item4/start-074.json |
| item4-start-075 | 06:17:50.023 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 12; 3.229 s | PASS | item4/start-075.json |
| item4-start-076 | 06:17:55.362 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 144; 3.228 s | PASS | item4/start-076.json |
| item4-start-077 | 06:18:00.671 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 23; 3.227 s | PASS | item4/start-077.json |
| item4-start-078 | 06:18:05.995 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 148; 3.229 s | PASS | item4/start-078.json |
| item4-start-079 | 06:18:11.299 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 17; 3.229 s | PASS | item4/start-079.json |
| item4-start-080 | 06:18:16.618 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 144; 3.228 s | PASS | item4/start-080.json |
| item4-start-081 | 06:18:21.944 | 4 | EARLY 0; LATE 0; first step 125019 ns; first sequence 13; 3.229 s | PASS | item4/start-081.json |
| item4-start-082 | 06:18:27.335 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 130; 3.227 s | PASS | item4/start-082.json |
| item4-start-083 | 06:18:32.706 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 254; 3.230 s | PASS | item4/start-083.json |
| item4-start-084 | 06:18:38.114 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 122; 3.229 s | PASS | item4/start-084.json |
| item4-start-085 | 06:18:43.514 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 246; 3.229 s | PASS | item4/start-085.json |
| item4-start-086 | 06:18:48.888 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 114; 3.230 s | PASS | item4/start-086.json |
| item4-start-087 | 06:18:54.250 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 246; 3.230 s | PASS | item4/start-087.json |
| item4-start-088 | 06:18:59.575 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 113; 3.230 s | PASS | item4/start-088.json |
| item4-start-089 | 06:19:04.885 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 237; 3.230 s | PASS | item4/start-089.json |
| item4-start-090 | 06:19:10.255 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 105; 3.231 s | PASS | item4/start-090.json |
| item4-start-091 | 06:19:15.675 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 229; 3.227 s | PASS | item4/start-091.json |
| item4-start-092 | 06:19:21.068 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 97; 3.229 s | PASS | item4/start-092.json |
| item4-start-093 | 06:19:26.423 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 221; 3.228 s | PASS | item4/start-093.json |
| item4-start-094 | 06:19:31.793 | 4 | EARLY 0; LATE 0; first step 125020 ns; first sequence 92; 3.226 s | PASS | item4/start-094.json |
| item4-start-095 | 06:19:37.186 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 219; 3.227 s | PASS | item4/start-095.json |
| item4-start-096 | 06:19:42.488 | 4 | EARLY 0; LATE 0; first step 125019 ns; first sequence 85; 3.230 s | PASS | item4/start-096.json |
| item4-start-097 | 06:19:47.811 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 217; 3.227 s | PASS | item4/start-097.json |
| item4-start-098 | 06:19:53.126 | 4 | EARLY 0; LATE 0; first step 125000 ns; first sequence 85; 3.230 s | PASS | item4/start-098.json |
| item4-start-099 | 06:19:58.385 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 209; 3.230 s | PASS | item4/start-099.json |
| item4-start-100 | 06:20:03.696 | 4 | EARLY 0; LATE 0; first step 124999 ns; first sequence 78; 3.229 s | PASS | item4/start-100.json |
| item4-rebind | 06:20:31.468-06:20:32.910 (locked) | 4/8 | Binding rule (formats equal); DUT out 0 -> peer in 0 bound, read back conn 1, flags 0x0082 (as found) | ACTION_RC=0 | item4/asfound-rebind.jsonl |
| soak-setup | 06:22:38.213-06:22:52.714 (locked) | 5 | Inventory, timing and counters read; console words; maps read (in 0: 4, out 0: 8); binding rule; bound peer AAF -> DUT in 0 and peer CRF -> DUT in 1; t0 06:23:22 | ACTION_RC=0 | soak/ |
| soak-chunk-00 | 06:23:03.301-06:30:27.255 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-000 | 06:23:23.249 | 5-7 | elapsed 0.541 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-001 | 06:24:22.922 | 5-7 | elapsed 60.213 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-002 | 06:25:22.914 | 5-7 | elapsed 120.205 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-003 | 06:26:22.913 | 5-7 | elapsed 180.205 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-004 | 06:27:22.919 | 5-7 | elapsed 240.210 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-005 | 06:28:23.247 | 5-7 | elapsed 300.538 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-006 | 06:29:22.949 | 5-7 | elapsed 360.240 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-007 | 06:30:22.922 | 5-7 | elapsed 420.213 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-01 | 06:31:04.300-06:38:27.221 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-008 | 06:31:22.907 | 5-7 | elapsed 480.198 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-009 | 06:32:22.934 | 5-7 | elapsed 540.226 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-010 | 06:33:23.248 | 5-7 | elapsed 600.539 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-011 | 06:34:22.933 | 5-7 | elapsed 660.224 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-012 | 06:35:22.896 | 5-7 | elapsed 720.187 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-013 | 06:36:22.917 | 5-7 | elapsed 780.208 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-014 | 06:37:22.930 | 5-7 | elapsed 840.222 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-015 | 06:38:23.244 | 5-7 | elapsed 900.534 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-02 | 06:38:34.615-06:45:29.057 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-016 | 06:39:22.929 | 5-7 | elapsed 960.221 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-017 | 06:40:22.918 | 5-7 | elapsed 1020.210 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-018 | 06:41:22.908 | 5-7 | elapsed 1080.200 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-019 | 06:42:22.928 | 5-7 | elapsed 1140.219 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-020 | 06:43:23.282 | 5-7 | elapsed 1200.573 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-021 | 06:44:22.938 | 5-7 | elapsed 1260.229 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-022 | 06:45:22.913 | 5-7 | elapsed 1320.204 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-03 | 06:45:59.190-06:53:27.942 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-023 | 06:46:22.934 | 5-7 | elapsed 1380.226 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-024 | 06:47:22.925 | 5-7 | elapsed 1440.217 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-025 | 06:48:23.250 | 5-7 | elapsed 1500.541 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-026 | 06:49:22.926 | 5-7 | elapsed 1560.218 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-027 | 06:50:22.897 | 5-7 | elapsed 1620.189 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-028 | 06:51:22.920 | 5-7 | elapsed 1680.211 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-029 | 06:52:22.916 | 5-7 | elapsed 1740.207 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-030 | 06:53:23.227 | 5-7 | elapsed 1800.518 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-04 | 06:53:35.842-07:00:26.873 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-031 | 06:54:22.910 | 5-7 | elapsed 1860.202 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-032 | 06:55:22.904 | 5-7 | elapsed 1920.195 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-033 | 06:56:22.945 | 5-7 | elapsed 1980.237 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-034 | 06:57:22.910 | 5-7 | elapsed 2040.201 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-035 | 06:58:23.240 | 5-7 | elapsed 2100.531 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-036 | 06:59:22.932 | 5-7 | elapsed 2160.223 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-037 | 07:00:22.922 | 5-7 | elapsed 2220.212 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-05 | 07:00:41.132-07:07:26.023 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-038 | 07:01:22.918 | 5-7 | elapsed 2280.210 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-039 | 07:02:22.934 | 5-7 | elapsed 2340.225 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-040 | 07:03:23.272 | 5-7 | elapsed 2400.563 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-041 | 07:04:22.919 | 5-7 | elapsed 2460.210 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-042 | 07:05:22.926 | 5-7 | elapsed 2520.217 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-043 | 07:06:22.898 | 5-7 | elapsed 2580.189 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-044 | 07:07:22.900 | 5-7 | elapsed 2640.191 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-06 | 07:07:45.778-07:14:25.745 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-045 | 07:08:23.265 | 5-7 | elapsed 2700.557 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-046 | 07:09:22.911 | 5-7 | elapsed 2760.202 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-047 | 07:10:22.905 | 5-7 | elapsed 2820.197 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-048 | 07:11:22.933 | 5-7 | elapsed 2880.224 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-049 | 07:12:22.920 | 5-7 | elapsed 2940.211 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-050 | 07:13:23.264 | 5-7 | elapsed 3000.555 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-051 | 07:14:22.906 | 5-7 | elapsed 3060.197 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-07 | 07:14:49.510-07:22:25.966 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-052 | 07:15:22.902 | 5-7 | elapsed 3120.194 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-053 | 07:16:22.889 | 5-7 | elapsed 3180.181 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-054 | 07:17:22.910 | 5-7 | elapsed 3240.201 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-055 | 07:18:23.246 | 5-7 | elapsed 3300.537 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-056 | 07:19:22.930 | 5-7 | elapsed 3360.221 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-057 | 07:20:22.916 | 5-7 | elapsed 3420.207 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-058 | 07:21:22.906 | 5-7 | elapsed 3480.198 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-059 | 07:22:22.902 | 5-7 | elapsed 3540.193 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-08 | 07:22:32.957-07:29:26.172 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-060 | 07:23:23.319 | 5-7 | elapsed 3600.611 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-061 | 07:24:22.898 | 5-7 | elapsed 3660.190 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-062 | 07:25:22.927 | 5-7 | elapsed 3720.218 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-063 | 07:26:22.915 | 5-7 | elapsed 3780.206 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-064 | 07:27:22.916 | 5-7 | elapsed 3840.207 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-065 | 07:28:23.290 | 5-7 | elapsed 3900.581 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-066 | 07:29:22.916 | 5-7 | elapsed 3960.206 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-09 | 07:29:48.340-07:37:30.064 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-067 | 07:30:22.915 | 5-7 | elapsed 4020.207 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-068 | 07:31:22.937 | 5-7 | elapsed 4080.228 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-069 | 07:32:22.937 | 5-7 | elapsed 4140.228 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-070 | 07:33:23.269 | 5-7 | elapsed 4200.561 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-071 | 07:34:22.921 | 5-7 | elapsed 4260.212 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-072 | 07:35:23.027 | 5-7 | elapsed 4320.317 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-073 | 07:36:22.959 | 5-7 | elapsed 4380.250 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-074 | 07:37:22.975 | 5-7 | elapsed 4440.266 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-10 | 07:37:46.062-07:44:26.189 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-075 | 07:38:23.445 | 5-7 | elapsed 4500.737 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-076 | 07:39:22.972 | 5-7 | elapsed 4560.263 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-077 | 07:40:22.961 | 5-7 | elapsed 4620.252 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-078 | 07:41:22.951 | 5-7 | elapsed 4680.242 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-079 | 07:42:24.136 | 5-7 | elapsed 4741.427 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-080 | 07:43:23.280 | 5-7 | elapsed 4800.571 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-081 | 07:44:22.916 | 5-7 | elapsed 4860.207 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-11 | 07:44:33.727-07:51:28.985 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-082 | 07:45:22.930 | 5-7 | elapsed 4920.222 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-083 | 07:46:22.917 | 5-7 | elapsed 4980.209 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-084 | 07:47:22.945 | 5-7 | elapsed 5040.237 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-085 | 07:48:23.246 | 5-7 | elapsed 5100.538 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-086 | 07:49:22.941 | 5-7 | elapsed 5160.233 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-087 | 07:50:22.914 | 5-7 | elapsed 5220.205 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-088 | 07:51:22.935 | 5-7 | elapsed 5280.226 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-12 | 07:51:44.665-07:58:28.295 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-089 | 07:52:22.923 | 5-7 | elapsed 5340.215 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-090 | 07:53:23.262 | 5-7 | elapsed 5400.553 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-091 | 07:54:22.926 | 5-7 | elapsed 5460.218 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-092 | 07:55:22.907 | 5-7 | elapsed 5520.198 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-093 | 07:56:22.929 | 5-7 | elapsed 5580.221 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-094 | 07:57:22.911 | 5-7 | elapsed 5640.202 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-095 | 07:58:23.260 | 5-7 | elapsed 5700.551 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-13 | 07:58:34.825-08:05:26.599 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-096 | 07:59:22.920 | 5-7 | elapsed 5760.211 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-097 | 08:00:22.918 | 5-7 | elapsed 5820.209 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-098 | 08:01:22.920 | 5-7 | elapsed 5880.211 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-099 | 08:02:22.930 | 5-7 | elapsed 5940.222 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-100 | 08:03:23.260 | 5-7 | elapsed 6000.551 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-101 | 08:04:22.916 | 5-7 | elapsed 6060.207 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-102 | 08:05:22.931 | 5-7 | elapsed 6120.222 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-14 | 08:05:51.772-08:13:28.559 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-103 | 08:06:22.905 | 5-7 | elapsed 6180.197 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-104 | 08:07:22.908 | 5-7 | elapsed 6240.199 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-105 | 08:08:23.288 | 5-7 | elapsed 6300.580 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-106 | 08:09:22.909 | 5-7 | elapsed 6360.200 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-107 | 08:10:22.897 | 5-7 | elapsed 6420.189 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-108 | 08:11:22.927 | 5-7 | elapsed 6480.218 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-109 | 08:12:22.918 | 5-7 | elapsed 6540.208 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-110 | 08:13:23.319 | 5-7 | elapsed 6600.609 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-15 | 08:13:42.914-08:20:27.167 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-111 | 08:14:22.922 | 5-7 | elapsed 6660.214 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-112 | 08:15:22.930 | 5-7 | elapsed 6720.221 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-113 | 08:16:22.935 | 5-7 | elapsed 6780.227 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-114 | 08:17:22.916 | 5-7 | elapsed 6840.207 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-115 | 08:18:23.234 | 5-7 | elapsed 6900.525 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| soak-116 | 08:19:22.904 | 5-7 | elapsed 6960.195 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-117 | 08:20:22.925 | 5-7 | elapsed 7020.216 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-chunk-16 | 08:20:33.972-08:23:26.911 (locked) | 5-7 | Probe online, rolling captures, polls below | ACTION_RC=0 | soak/run-events.jsonl |
| soak-118 | 08:21:22.912 | 5-7 | elapsed 7080.204 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-119 | 08:22:22.931 | 5-7 | elapsed 7140.222 s; counters; error-class increments 0 | CLEAN | soak/summary.json |
| soak-120 | 08:23:23.244 | 5-7 | elapsed 7200.535 s; counters, timing, console; error-class increments 0 | CLEAN | soak/summary.json |
| restore-end | 08:23:42.948-08:23:49.398 (locked) | 8 | Soak peer -> DUT bindings unbound; maps, listener states, inventory, timing, counters and console read back: 44 of 44 inventory rows equal | ACTION_RC=0 | restore/ |
| s3-cleanup | about 08:25 | 8 | Controller staging /tmp/608-b14 removed (375 MB, incl. the private peer file); tap host capture wrapper removed; no tcpdump, probe or agent left running; no pcap left on the tap host; bench lock free | OK | restore/controller-cleanup.txt, restore/tap-cleanup.txt |

## Restore ledger

As found (05:17-05:20): DUT at INTERNAL, both DUT listeners unbound; peer in 0 <- DUT out 0 (AAF) and peer in 8 <- DUT out 1 (CRF), flags 0x0082; peer clock source 1 (INPUT_STREAM on its in 8); DUT maps in 0: 4, out 0: 8; MAAP_CTRL 0x201, MAAP_STAT0 0xDD85, MAAP_STAT1 0x6; NVM image seq 234.

| Change | Made | Restored and read back |
|---|---|---|
| Peer clock source 1 -> 0 | 05:20:08 (item 2) | 1 at 05:45:36, read back 1 |
| Peer AAF -> DUT in 0, peer CRF -> DUT in 1 | 05:20:08 (item 2) | unbound 05:45:34, read back 0/0 |
| DUT clock source 0 -> 2/1/0 x10 | 05:20-05:45 | 0 at every cycle end and at teardown |
| Peer clock source 1 -> 0 | 05:48:58 (item 3) | 1 at 06:08:53, read back 1 |
| Peer CRF -> DUT in 1; DUT clock 0 -> 1 | 05:48:58 (item 3) | unbound, DUT clock 0 at 06:08:53, read back |
| DUT out 1 -> peer in 8 (as found) | cycled 101 times (item 3) | bound at the end, flags 0x0082 |
| DUT out 0 -> peer in 0 (as found) | released 06:10:43, cycled 100 times (item 4) | re-bound 06:20:31 under the binding rule, flags 0x0082 |
| Peer AAF -> DUT in 0, peer CRF -> DUT in 1 | 06:22:4x (soak) | unbound 08:23:43, read back 0/0 |
| Final | - | 08:23:49: 44 of 44 inventory rows equal the 06:22 inventory; formats, clocks, listener states and maps equal the 05:17-05:20 reads; MAAP words unchanged |

Residuals: NVM image seq 234 -> 272 (38 commits, 0 failed, dirty 0, content as found); `SLIP_LB` 0 -> 0x92 and `RENDER_STAT` rails 0 -> 10 (never cleared but by reset); GET_COUNTERS values advanced (MEDIA_RESET, STREAM_START/STOP, CLOCK_DOMAIN LOCKED/UNLOCKED); the peer's two as-found bindings re-established by controller commands.

## Deviations

- The SoC board console was not touched in session 3 (ruling); no item needed it.
- As found the peer followed the DUT's CRF with two bindings from the DUT; B2, B8 and B13 started all-unbound with the peer at INTERNAL. Items 2 and 3 set the peer's clock source to INTERNAL (avoiding a clock loop in methods that make the DUT follow the peer) and restored it; items 4 and 5 kept the peer as found.
- The first item 2 setup refused on the as-found binding (nothing changed); the runner was adapted to keep B8's first bind as found and to set and restore the peer clock (setup2).
- Item 2 holds: 60 s (AAF) and 45 s (CRF) after LOCKED, 15 s at INTERNAL (B8: 120-150 s); no tone, no SoC board, no external capture.
- Item 3 pilot cycle 1: the tap host's `timeout` did not forward SIGINT to tcpdump, which was SIGKILLed (rc 137, no statistics). Tested at 05:50 (three captures, rc 137 twice) and fixed (the wrapper signals tcpdump directly; test rc 0 with statistics at 05:51). Cycles 2-101 are the graded 100; cycle 1 is listed.
- Item 4: B13 had DUT clock source 1 and the peer at INTERNAL; here DUT INTERNAL and the peer following the DUT's CRF.
- Capture filters: item 2 = the brief's filter plus tagged AVTP; item 3 = everything but tagged AAF (B2's unfiltered method, reduced); items 4-5 = B13's three filters including the brief's.
- Soak: 17 locked chunks (bindings held in the devices between chunks); the tap has 16 gaps of 12-44 s (94.8 % coverage); counters cumulative.
- Soak raw captures (25.9 GB) are on $VALIDATION_STORAGE/608-b14-raw (this host's /tmp is RAM-backed), not under /tmp.
- Gates: the first worktree run called `check_baremetal_only.py` without a mode (usage error, rc 2) and then found the word "kernel" in the page; both fixed, every gate rc 0 at the worktree and at each head (gates/).

## Observations for triage (in the findings page)

- DUT FRAMES_TX (both talkers) and FRAMES_RX (CRF listener) advance one per second, not per PDU.
- The DUT sends no unsolicited GET_COUNTERS for its STREAM_INPUTs (one soak minute: 60 per STREAM_OUTPUT, 0 per STREAM_INPUT).
- One `SLIP_LB` frame at INTERNAL 5-10 min into the soak (peer following the DUT's CRF; no settle recentre at INTERNAL after a bind).
- Item 3: the DUT withdrew its Talker Advertise in 2 of 100 holds; those two cycles have the two slowest restarts (105.7 and 125.9 ms).

## Large artifacts

Outside the packet, indexed in RAW-ARTIFACTS.json and raw-index/ (1,294 files, 27.9 GB): /tmp/608-b14/raw (item 2: 20 captures 1.51 GB; item 3: 101 captures 89.8 MB; item 4: 300 captures 452 MB; polls, agent transcripts, probe logs) and $VALIDATION_STORAGE/608-b14-raw/soak (363 captures 25.9 GB, counter, timing and probe logs). Private originals of masked packet files: /tmp/608-b14/private (redaction.json).

## Tools (session 3)

| Tool | Taken from | Change |
|---|---|---|
| sw_b14.py | B8 run_b8.py case SW | No SoC board, tone or external capture; cycle structure; per-switch tap; as-found bind kept; peer clock set and restored |
| b8_ctl.py, console_poll_b8.py, b7_decode.py | B8 (unchanged, ORIGIN-B8.sha256) | - |
| cyc608_b14.py, b14_reconnect.py, an608_b14.py, wire_summary.py | B2 (ORIGIN-B2.sha256) | Paths; filter; analysis unchanged |
| b14_controller.py | B2 b2_controller.py | Peer ids from a private file; as-found-aware setup and restore; binding rule |
| capture_b14.py | B2 capture.py | Filter and snap length; stop signals tcpdump directly |
| start_b14.py, soak_b14.py | B13 run_short.py, run_b13.py (ORIGIN-B13.sha256) | Paths; ranges; chunked soak; cadence 60 s / 5 min; talker error counters; console reads |
| startup_report_b14.py, decode_capture.py | B13 | Paths only / unchanged |
| bindops_b14.py, soak_setup_b14.sh, restore_end_b14.sh, run_locked_b14.sh, series608_b14.sh | new | Binds, reads and lock windows |
| tapdec_b14.py, sw_summary_b14.py, maap_b14.py, summaries_b14.py | new | Offline analysis |
| probe (B13's probe.cpp) | B13, rebuilt | Source hash verified (tools/build-inputs-s3.json) |

## Posts

- Session 2 STOP, as above (session2/STOP.md, STOP.readback.md, stop-url.txt).
- Session 3 REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-6095837334, posted 2026-10-10 at about 08:58 UTC with the head and the per-cycle tables (REVIEW-READY.md; REVIEW-READY.readback.md equal but for one trailing newline; review-ready-url.txt). Nothing else was posted.

## Packet layout

| Path | What |
|---|---|
| HANDOFF.md, PR-BODY.md, REVIEW-READY.md (+ readback, url), TAKEN.md | This file, the proposed PR body, the posts |
| identity/, precheck/ | Item 1 (session 2) and the host checks |
| item2/ | Setup, five cycle invocations, teardown; summary/ (per switch, rails) |
| item3/ | Setup and restore transcripts; cycles/ (per cycle: action log, events, MSRP and ACMP tables, analysis, console and counter snapshots); summary.json, cycles.tsv |
| item4/ | Per start rows and wire summaries; startup summary and CSVs; capture receipts; release and re-bind |
| soak/ | Setup, chunk transcripts, polls ledger, console reads, capture receipts, summaries, wire aggregate, coverage, overlap recovery, AECP decode |
| maap/ | MAAP summary |
| restore/ | As-found reads, final read-back, comparison, cleanup |
| tools/ | Every tool used, with ORIGIN-B2/B8/B13.sha256 and the build receipts |
| gates/ | worktree (two attempts) and the three heads; head3 is the final head |
| session1/, session2/ | The earlier sessions' files |
| RAW-ARTIFACTS.json, raw-index/ | Every raw file outside the packet by path, size and SHA-256 |
| redaction.json, redaction-index/ | Every masked file: original and retained SHA-256, labels |
| MANIFEST.sha256 | SHA-256 of every packet file; item3/cycles, item4 and soak carry their own MANIFEST.sha256, hashed here |
