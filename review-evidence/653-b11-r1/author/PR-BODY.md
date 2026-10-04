[A535] #653 bench: disconnect order on the bbf704ec image (lane B11)

Refs #653

## What this adds

A findings page, `docs/findings/653_DISCONNECT_ORDER_BENCH.md`, with the dated section "#653 bench: disconnect order, 2026-10-04", and its row in `docs/findings/README.md`. No other file changes.

The page records the bench item of the [lane B11 assignment](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5983239639): the disconnect order a real controller sees, on dev `bbf704ec` as booted (no flash).

## Result

The owner's report is not reproduced on this bench. In all 23 disconnects the UNBIND_RX response left the DUT's port first, and the la_avdecc controller library flagged nothing.

| #653 acceptance | On this image |
|---|---|
| 1. UNBIND_RX response before the unlock's counters notification, AAF and CRF | Held, 23 of 23. Response 7.5 µs after the command; the unlock's GET_COUNTERS 114.2 to 116.8 µs later on AAF input 0, 99.3 and 99.7 ms later on CRF input 1 |
| 2. Bench capture with a control that fails the check | One tap capture per disconnect, read response first by the lane grader and by the provided decoder. In the control, the check reads counters first against the probe's own GET_COUNTERS |
| 3. LOCKED = UNLOCKED after the unbind, STREAM_INTERRUPTED not counted | AAF: 1/1, STREAM_INTERRUPTED 0, in the first push after the unbind. CRF: 1/0 until the 100 ms silence timeout, then 1/1, as expected before PR #655 |
| 4. 20 connects and disconnects with no counter error | Held for the library: one session, 20 AAF and 2 CRF cycles, no compatibility change, diagnostic, query error or lost notification. The Hive application was not run |

The AAF talker was still streaming at every UNBIND_RX command (303 to 1,562 frames after it), so each unlock came from the bind fall.

## Method in brief

- A C++ probe on the controller host, linked against the bench's la_avdecc 4.3.1.1 build. The library's high-level controller enumerates both entities, registers for unsolicited notifications, binds, waits for MEDIA_LOCKED, and unbinds. A second, low-level entity reads both formats live before each bind (the binding rule; all equal, none set) and sends the control's own GET_COUNTERS.
- One tap capture at the DUT's port per cycle, under the bench lock. Each capture is decoded by the provided `tap_order_decode.py`, unchanged, and by a lane grader that orders by capture position and checks the tap timestamps.
- Restore: every format, map, binding and clock source read back as found. The CRF cycles left the DUT's servo in HOLDOVER; a set to INTERNAL and back on the DUT's CLOCK_DOMAIN, the listener's, returned it to IDLE. The probe and staging were removed from the controller host.

## Validation

At the head, every gate rc 0 (physical `/data` path, Markdown gates in the pinned Markdown environment):

| Gate | Result |
|---|---|
| `scripts/docs_check.py` | rc 0, 0 findings |
| `scripts/check_doc_style.py` | rc 0 |
| `scripts/gen_toc.py --check`, `--verify-anchors` | rc 0 |
| `scripts/check_em_dash.py --base 6c22d3ca` | rc 0, 0 findings over 357 added lines |
| `scripts/check_doc_paths.py` | rc 0 |
| `scripts/ci_scope.py --selftest` | rc 0 |
| `scripts/check_baremetal_only.py --check`, `--selftest` | rc 0 (the bare call is a usage error, rc 2) |
| `scripts/check_feature_status.py --self-test` | rc 0 |
| `git diff --check`, `git diff --check 6c22d3ca HEAD` | rc 0 |

These are operator observations, not review verdicts. Not run: act and the hosted workflows (nothing pushed).

## Limits

- One controller layer: the library's own reports. Hive may apply its own counter checks.
- One registered controller; the order was captured at the DUT's port, not at the controller host.
- Every unbind came at least 2 s after the input's last counters push.
- The CRF 1/0 window is not re-measured on an image with PR #655.
