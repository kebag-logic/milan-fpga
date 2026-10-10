[A578] B14 bench handoff

Refs #608 #645 #647 #667 #682 #686 #691

Base: 5603c353137e90c1fa95429f6d00ef7a2298d9ee.
Branch: 608-b14-bench, clean, no commit (head = base).
Assignment: https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-6085135051
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-6087724820 (posted 2026-10-09T19:23:11Z by the first session; not posted again).
Status: STOP at item 1. The identity gate cannot run: the controller host has not returned since the bench VMs restarted at about 19:17 UTC. Every item needs the controller, so nothing after item 1 ran.
Started: 2026-10-09T19:23:10Z (first session); resumed 2026-10-09T19:28Z after an external usage limit.

| Item | Planned cycles | Completed | Result |
|---|---:|---:|---|
| 1 Identity | 1 | 0 | BLOCKED: controller host unreachable; STOP |
| 2 INTERNAL to AAF | 10 | 0 | NOT RUN |
| 2 AAF to CRF | 10 | 0 | NOT RUN |
| 3 Talker disconnect | 100 | 0 | NOT RUN |
| 4 Talker start | 100 | 0 | NOT RUN |
| 5 Default maps and soak | 120 minutes | 0 | NOT RUN |
| 6 Ethernet receive sanity | Soak interval | 0 | NOT RUN |
| 7 MAAP interoperation | 1 | 0 | NOT RUN |
| 8 Restore | All changed items | 0 | Nothing changed, nothing to restore |

| Cycle | UTC | Item | Observation | Result | Evidence |
|---|---|---|---|---|---|
| precheck-001 | 19:24:57-19:25:39 | 1 | Local prerequisites present (board link address, both audio cards, both consoles); controller SSH connect timeout; tap host reachable with both tap interfaces | BLOCKED | preconditions.json, host-checks.json |
| precheck-002 | 19:28:42 | 1 | Controller SSH "No route to host"; its neighbour entry FAILED | BLOCKED | host-checks-2.json |
| precheck-003 | 19:29:01 | - | Tap host up 12 min, both tap interfaces UP, non-interactive privilege OK; three serial adapters and both audio cards present | OK | host-checks-2.json |
| precheck-004 | 19:31:07 | 1 | Ping sweep of the VM network: only this host, the gateway and the tap host (two addresses, one MAC) answer; the controller VM is absent | BLOCKED | host-checks-2.json |
| precheck-005 | 19:31:18-19:40:18 | 1 | Controller SSH polled every 20 s: never answered | BLOCKED | host-checks-2.json |
| precheck-006 | 19:40:39-19:49:59 | 1 | Controller SSH polled every 20 s: never answered | BLOCKED | host-checks-2.json |
| precheck-007 | 19:50:20 | - | Bench lock probed with a non-blocking `flock -n` running only `true`: free | OK | host-checks-2.json |
| precheck-008 | 19:50:59 | 1 | Controller SSH "No route to host"; ping fails | BLOCKED | this file |
| end-check | 19:51:40 | - | Final state: branch clean at base; bench lock probed again the same way (non-blocking, `true` only): free | OK | this file |

STOP: https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-6088157558 (posted 2026-10-09 at about 19:51 UTC; STOP.md, STOP.readback.md equal except for one trailing newline, stop-url.txt). Nothing else was posted.

Restore ledger: no bench state changed. The bench lock was taken only by two non-blocking probes (precheck-007 and end-check), each running `true` and touching nothing. No console, JTAG, power strip, tap capture, probe or controller session was used. Nothing to restore.

Deviation: neither lock probe was needed for the STOP decision.

Large artifacts: none.
Validation: no commit, so no documentation gate applies. The findings page `docs/findings/B14_BENCH_5603C353.md` was not written: no item produced a measurement.

To resume: once the controller host answers, rerun the whole lane from item 1 on the same image. B13's build at /tmp/667-b13 on the controller host must be re-verified first, because the VM restart may have cleared /tmp.
