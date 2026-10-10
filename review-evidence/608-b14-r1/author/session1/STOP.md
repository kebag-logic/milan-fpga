[A578] STOP

Head: `5603c353137e90c1fa95429f6d00ef7a2298d9ee` (branch `608-b14-bench`, unchanged, no commit).

**Item 1, the identity gate, cannot run.** The bench's host machines were restarted at about 19:17 UTC. The controller host has not come back since: it has no network presence, so the DUT cannot be read over ATDECC. Every later item needs the controller, so items 2 to 7 did not run, and item 8 has nothing to restore.

| Cycle | UTC | Item | Observation | Result |
|---|---|---|---|---|
| precheck-001 | 19:24:57-19:25:39 | 1 | Local prerequisites present (board link address, both audio cards, both consoles); controller connect timeout; tap host reachable with both tap interfaces | BLOCKED |
| precheck-002 | 19:28:42 | 1 | Controller: no route to host; neighbour resolution failed | BLOCKED |
| precheck-003 | 19:29:01 | - | Tap host up, both tap interfaces up; serial adapters and audio cards present | OK |
| precheck-004 | 19:31:07 | 1 | Sweep of the host network: the controller address is absent | BLOCKED |
| precheck-005 | 19:31:18-19:40:18 | 1 | Controller polled every 20 s: no answer | BLOCKED |
| precheck-006 | 19:40:39-19:49:59 | 1 | Controller polled every 20 s: no answer | BLOCKED |
| precheck-007 | 19:50:20 | - | Bench lock: free (one non-blocking probe that ran nothing) | OK |
| precheck-008 | 19:50:59 | 1 | Controller: no route to host | BLOCKED |

| Item | Planned | Completed | Result |
|---|---:|---:|---|
| 1 Identity | 1 | 0 | BLOCKED |
| 2 INTERNAL→AAF / AAF→CRF | 10 / 10 | 0 / 0 | NOT RUN |
| 3 DUT-talker disconnects | 100 | 0 | NOT RUN |
| 4 Talker starts | 100 | 0 | NOT RUN |
| 5 Default maps, two-hour soak | 120 min | 0 | NOT RUN |
| 6 Ethernet RX sanity | soak | 0 | NOT RUN |
| 7 MAAP interop | 1 | 0 | NOT RUN |
| 8 Restore | - | - | Nothing changed |

**Bench state:** unchanged. No console, JTAG, power-strip, tap-capture or controller action was taken. The lock is free.

**Needed to resume:** the controller host back on the network. The whole lane then reruns from item 1 on the same image.

Stopping here.
