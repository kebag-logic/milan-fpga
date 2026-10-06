Source: https://github.com/kebag-logic/milan-fpga/blob/28f9666feab2b2ba287643c63ed3a16b1e0bb863/tb/verilator/milan_dp/README.md#L666

Verbatim lines 666 through 723.

## The #653 unbind order and Table 5.6 pair (the UNB section of `obj_notify`)

Issue #653 reports a counters push that left before its UNBIND_RX response.
`[UNB]` runs that unbind at the end of the timed leg, after `[GSI]`.
It uses the same ports, on the AAF input (0) and the CRF input (1).
For each input it does the following:

1. registers controllers A and B;
2. binds from A, answers the PROBE_TX and locks the input off clean PDUs;
3. keeps the talker streaming through the unbind;
4. waits until the row has pushed nothing for one second;
5. unbinds from A, then waits past both 100 ms silence timeouts.

Step 4 opens the GET_COUNTERS limiter, so only the order can hold a push back.
Milan v1.2 5.3.8.10 counts the unbind as one MEDIA_UNLOCKED, never a STREAM_INTERRUPTED.
Table 5.6 then reads MEDIA_LOCKED = MEDIA_UNLOCKED: not synchronized.

| Check | Graded |
|---|---|
| U1 | the UNBIND_RX response is SUCCESS |
| U2 | a push reporting the unlock reaches each controller, and every such push leaves after the response |
| U3 | the source pair reads 1/1 as the response's last byte leaves, and GET_COUNTERS reads 1/1/0 right after it |
| U3 | every later push reads MEDIA_LOCKED = MEDIA_UNLOCKED |
| U4 | 10.5 M cycles after the command, past both timeouts, the pair still reads 1/1/0 |

Each input prints an `[i]` trace, in cycles after the command's last byte.
Measured on 2026-10-04 UTC:

| Event | AAF input 0 | CRF input 1 |
|---|---|---|
| listener queues its response | +193 | +193 |
| debounced bind level falls | +199 | +199 |
| MEDIA_UNLOCKED written at its source | +204 | +200 |
| UNBIND_RX response leaves | +277 | +277 |
| push reporting the unlock, to A / B | +2,294 / +3,057 | +2,294 / +3,057 |

At dev `fea346e7` the response also led on both inputs.
There the CRF unlock waited for the silence timeout, at +9,818,177.
So for 100 ms an unbound CRF input read MEDIA_LOCKED 1, MEDIA_UNLOCKED 0.
`KL_crf_rx` now counts the unlock on the bind fall, as the AAF monitor does.
The unit-level cases are in `tb/verilator/crf_rx`, section `[UNB]`.

**Failing arms.** `make unb-mutants` runs `unb_mutants.py`.
It plants each defect in a copy of the processor tree or of `KL_crf_rx`.
`CRFRX_SRC` in the Makefile names the CRF engine for that purpose.
Each mutant must fail its named checks and still pass its named holds.
Measured on 2026-10-04 UTC: the clean leg passes 421/421 checks.

| Mutant | Named checks that fail | Failures |
|---|---|---|
| the ACMP lane is held 6,000 cycles, so the push overtakes the response | U2 order to A, AAF and CRF | 4 of 421 |
| the CRF unbind does not count its unlock, as at dev `fea346e7` | CRF U3 as the response left, and right after it | 2 of 421 |
| the CRF unbind keeps the lock, so the timeout counts again | CRF U4; CRF U3 every later push | 2 of 421 |
| the CRF unbind also counts a STREAM_INTERRUPTED | CRF U3 STREAM_INTERRUPTED; CRF U4 | 2 of 421 |
| the CRF unbind counts its unlock but arms no push | CRF U2 a push reached A | 2 of 421 |

The first mutant's holds are U1 and the push arriving, so the catch is the order.
Its 4 failures are exactly the four U2 order checks; nothing else in the leg moves.
