[A535] REVIEW READY
Commit: `6f76d612a3191b77ac8a1fe2b9c66da42aeb405a` on `653-b11-bench`, one commit on dev `6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`. Local, not pushed, no PR.
Changed: new `docs/findings/653_DISCONNECT_ORDER_BENCH.md` with the dated section "#653 bench: disconnect order, 2026-10-04", and its row in `docs/findings/README.md`. No other file. Bench image: dev `bbf704ec` as booted, no flash.

**Result: the owner's report is not reproduced.** In all 23 disconnects the UNBIND_RX response left the DUT's port first, and the la_avdecc controller library flagged nothing.

- **Identity gate PASS** first: entity_id `020000fffe000001`, "Milan FPGA 1x1 TDM8", "2.96.0", "AX7101-0001"; VERSION and the AEM, BIOS and payload CRCs equal the build's; grader 10/10.
- **As found:** CLOCK_SOURCE 1 with the servo IDLE; STREAM_INPUT 0 and 1 at the peer's AAF and CRF talker formats; one input mapping; everything unbound. This equals lane B10's end state.
- **Probe:** C++ against the bench's la_avdecc 4.3.1.1 build.
  - The library's high-level controller enumerates both entities, registers for unsolicited notifications, binds, waits for MEDIA_LOCKED and unbinds.
  - A low-level second entity reads both formats live before each bind. All were equal, so none was set.
  - The same entity sends the control's own GET_COUNTERS.
- **Captures:** one tap capture at the DUT's port per cycle, under the bench lock. Each was decoded by the provided `tap_order_decode.py`, unchanged, and by a lane grader. Both read the same order in all 23.

**Per-run table** (intervals are tap timestamps; the pair is MEDIA_LOCKED/MEDIA_UNLOCKED/STREAM_INTERRUPTED):

| Run | Input | Order at the DUT's port | Command to response | Response to the unlock's GET_COUNTERS | Pushed pair | Library: input at that update | Library flags | Library pair after | Capture SHA-256 |
|---|---|---|---|---|---|---|---|---|---|
| C0, control | AAF 0 | RESPONSE_FIRST; COUNTERS_FIRST against the probe's own GET_COUNTERS | 7.5 µs | 115.4 µs | 1/1/0 | NotConnected | none | 1/1/0 | `4fa8c57c4b58` |
| A01 to A20 | AAF 0 | RESPONSE_FIRST, 20 of 20 | 7.5 µs each | 114.2 to 116.8 µs | 1/1/0 each | NotConnected each | none | 1/1/0 each | per cycle on the page |
| R01 | CRF 1 | RESPONSE_FIRST | 7.5 µs | 99,346.2 µs | 1/1/0 | NotConnected | none | 1/1/0 | `970a213ab53c` |
| R02 | CRF 1 | RESPONSE_FIRST | 7.5 µs | 99,731.4 µs | 1/1/0 | NotConnected | none | 1/1/0 | `c743c09453ab` |

The page has the full per-cycle table and every capture's SHA-256.

- **The AAF talker was still streaming** at every UNBIND_RX command: 303 to 1,562 frames arrived after it. So each unlock came from the bind fall.
- **Wire shape:** response, then an unsolicited GET_STREAM_INFO, then the unsolicited GET_COUNTERS. This matches the simulation trace at `fea346e7`.
- **Library:** no compatibility change, the Milan flag kept and no warning added. No diagnostics change, query error, AECP timeout or lost notification. The compatibility-event lists stayed empty.
- **Library order:** in every cycle it marked the input NotConnected before the update carrying the unlock. On AAF the gap was 51 to 113 µs.
- **CRF, before PR #655:** the library held 1/0 with the input NotConnected for 95.0 and 100.0 ms, then 1/1/0. It flagged nothing.

**Acceptance (#653):**
1. Held, 23 of 23, on inputs 0 and 1.
2. Bench captures done, with a control that reads counters first.
3. AAF held. CRF not at every instant on this pre-#655 image.
4. Held for the library: one session, 20 AAF and 2 CRF cycles, no counter error. Hive itself was not run.

**State as left:**
- Every format, map, binding and clock source read back as found.
- The census matches 45 of 46 entries; the 46th is the live propagation delay.
- The CRF cycles left the servo in HOLDOVER. A set to INTERNAL and back on the DUT's CLOCK_DOMAIN, the listener's, each read back, returned it to IDLE as found.
- Grader 10/10.
- The probe and staging are removed from the controller host, and the captures from the tap host after their hashes matched.
- The bench lock is free and nothing is left running.
- Residuals: 47 NVM commits, and three servo lock/unlock pairs on CLOCK_DOMAIN 0's counters.

**Validation:** at the head, every gate rc 0: `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors`, `check_em_dash.py --base 6c22d3ca` (0 findings over 357 added lines), `check_doc_paths.py`, `ci_scope.py --selftest`, `check_baremetal_only.py --check` and `--selftest`, `check_feature_status.py --self-test`, `git diff --check`. The bare `check_baremetal_only.py` is a usage error, rc 2, as in earlier lanes.

**Open risks/questions:**
- Only the library's own reports were recorded. Hive, on top of it, may apply counter checks of its own. The owner's Hive version, or a capture from that session, would settle the difference.
- The provided decoder's time column reads the tap timestamp's two words swapped, and its ACMP listener, unique ID and count columns read wrong offsets. Its line order is correct.

Refs #653.

