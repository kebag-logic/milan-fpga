[A440] Bench lane B2 on the dev `13eda870` image: the first talker bind (#606), and listener withdrawal and reconnect restart (#608, #75)

Refs #606
Refs #608
Refs #75

Evidence only: two new findings pages, no other change. No issue closes here. Assignment: https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5885087413

- `docs/findings/606_FIRST_BIND_MEASUREMENT.md`: #606 item 3, the bench re-measure of the first bind and the long-hold connect.
- `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md`: #608 item 3 and #75's acceptance, 100 disconnect/reconnect cycles with the tap.

## Verdicts (operator measurements; the reviews decide)

| Issue item | Verdict | Evidence |
|---|---|---|
| #606 item 3: first bind, 1 s bound | PASS, 5 of 5 | 0.059-0.229 s from the `CONNECT_RX` response to the first valid CRF PDU; first probe SUCCESS every time; the bridge's first MRPDU is Listener Ready, no LeaveAll |
| #606 item 3: long-hold connect, 1 s bound | PASS, 4 of 4 | Binds 2-5 after 36.9-39.3 s unbound, each after the DUT withdrew its Talker Advertise |
| #608 item 3: stop within one PDU, 100 of 100 | Literal: NOT MET, 99 of 100. Recorded reading (withdrawal reaching an IN registrar): PASS, 99 of 99 | Cycle 22: the DUT's own MSRP LeaveAll crossed the tap 1.390 ms before the bridge's Listener `Lv`; the registrar was LV and the stream ran through the 2 s hold (1,005 PDUs) |
| #608 item 3: STREAM_STOP counts each stop | PASS, 99 of 99 | +1 START and +1 STOP per stop; cycle 22 +0 / +0 |
| #608: non-stop holds | 1 of 100 | 3 of 100 on image `9e9954e9` |
| #75: first valid AVTP PDU within 1 s of a reconnect | PASS, 99 of 99 demonstrated restarts | 0.011239-0.139247 s, median 0.013195 s, p95 0.081912 s |
| #75: restart latency does not grow | PASS | Slope -0.000083 s/cycle, 95% interval [-0.000235, +0.000069]; first-ten and last-ten medians 0.013168 and 0.013255 s |
| #75: at least 100 physical restarts, DUT talker | NOT MET, 99 of 100 | Cycle 22 never stopped |

The two readings of #608 item 3 need a decision; the page does not choose.

## Per-bind table (seconds after the tapped `CONNECT_RX` response)

| Bind | Unbound before, s | Pre-bind tap, s | DUT LeaveAll PDUs / target TA declarations in it | First probe status | First DUT TA, s | First bridge MRPDU, s | Bridge Listener Ready, s | First valid PDU, s | Result |
|---|---|---|---|---|---|---|---|---|---|
| 1 | more than 1,800 (lane B1's restore) | 17.315 | 2 / 0 | SUCCESS | 0.171413 (JoinMt) | 0.227724, Listener New | 0.227724 | 0.228304 | PASS |
| 2 | 39.3 | 17.323 | 1 / 0 | SUCCESS | 0.068868 (JoinMt) | 0.125289, Listener New | 0.125289 | 0.126451 | PASS |
| 3 | 36.9 | 17.341 | 1 / 0 | SUCCESS | 0.074340 (JoinMt) | 0.129176, Listener New | 0.129176 | 0.130400 | PASS |
| 4 | 37.0 | 17.373 | 1 / 0 | SUCCESS | 0.172822 (JoinMt) | 0.227576, Listener New | 0.227576 | 0.229360 | PASS |
| 5 | 36.9 | 17.334 | 2 / 0 | SUCCESS | 0.000337 (JoinMt) | 0.057989, Listener New | 0.057989 | 0.059352 | PASS |

## Per-cycle summary

- 99 of 100 withdrawals stopped the stream within one PDU of the bridge's `Lv` (last PDU 1.974 ms before to 0.001 ms after it).
- Registrar state at the `Lv`: 42 IN observed, 57 IN inferred, 1 LV (cycle 22). The inference rests on the bridge re-declaring within 0.088 s of all 110 Listener-type LeaveAlls seen while registered, and at least 2.743 s of capture before every `Lv`.
- Three cycles (20, 21, 88) sent their own LeaveAll within one join period after the `Lv`, the window processor PR 130 moved; all three stopped within one PDU.
- The 100-row table is in the #608/#75 page and in the REVIEW READY comment on #606.

## Method notes

- Identity gate as lane B1 ran it: VERSION `0x00020060`; ROM `acad92b9`, QSPI payload `d84bce7b` (seed `eto`), AEM `93742dd2`; ENTITY and CONFIGURATION byte-exact to the AEM image; grader 10/10.
- Fresh state without a reset: an unbind, the processor's 15 s probe freshness (`T-SRP-DAFRESH`), then at least 26 s after the DUT's Talker Advertise `Lv`. Each bind required a 16 s tap window with a DUT LeaveAll and no target Talker Advertise declaration.
- The #75 method of PR #604 on the DUT-talker pair only: `DISCONNECT_RX`, 2 s, `CONNECT_RX`, one bench-lock window per cycle, tap timing on one clock.
- The DUT was never flashed, reset, rebooted or power-cycled; no outlet was switched; the reset epoch read 1 throughout.

## Restore

All restored and proven: the pair unbound on the first attempt, 18 of 18 stream states at connection count 0, the start and end censuses equal on 53 of 53 non-counter reads, a final tap capture with no CRF, grader 10/10, temporary scripts and the temporary capture module removed, the capture host's interfaces as found, outlets as found, the bench lock free.

## Limits

- #606's post-reset allocation path is not exercised: reaching it needs a DUT reset. PR #613's first-probe regression remains its evidence.
- The 2 s hold cannot show when an LV registration expires; cycle 22's stop time without a reconnect is not measured.
- Only CRF was measured; AAF remains unmeasured.

## Validation (all rc 0 at the committed head, foreground, not piped)

`docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 13eda870`, `check_doc_paths.py` (pinned Markdown environment); `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test`, `git diff --check`.
