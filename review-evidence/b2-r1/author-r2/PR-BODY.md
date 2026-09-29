[A440] Bench lane B2 on the dev `13eda870` image: the first talker bind (#606), and listener withdrawal and reconnect restart (#608, #75)

Relates to #606
Relates to #608
Relates to #75

Evidence only: two new findings pages and their rows in the findings index, no other change. No issue closes here. Assignment: https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5885087413

- `docs/findings/606_FIRST_BIND_MEASUREMENT.md`: #606 item 3, the bench re-measure of the first bind and the long-hold connect.
- `docs/findings/608_75_WITHDRAWAL_AND_RESTART.md`: #608 item 3 and #75's acceptance, 100 disconnect/reconnect cycles with the tap.
- `docs/findings/README.md`: index rows for both pages; the #75 row points at them.

## Verdicts (operator measurements; the reviews decide)

| Issue item | Verdict | Evidence |
|---|---|---|
| #606 item 3: first bind, 1 s bound | PASS, 5 of 5 | 0.059-0.229 s from the `CONNECT_RX` response to the first valid CRF PDU; first probe SUCCESS every time; the bridge's first MRPDU is Listener Ready, no LeaveAll |
| #606 item 3: long-hold connect, 1 s bound | PASS, 4 of 4 | Binds 2-5 after 36.9-39.3 s unbound, each after the DUT withdrew its Talker Advertise |
| #608 item 3: stop within one PDU of the withdrawal | 99 of 99 withdrawals that reached an IN registrar stopped; qualified | Graded under the [corrected ruling](https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-5886425487): cycle 22's LV registrar is attributed to the processor #108 deviation; met without qualification only after the pin adoption of processor PR #133 and a bench re-run |
| #608 item 3: STREAM_STOP counts each stop | PASS, 99 of 99 | +1 START and +1 STOP per stop; cycle 22 +0 / +0 |
| #608: non-stop holds | 1 of 100 | 3 of 100 on image `9e9954e9` |
| #75: first valid AVTP PDU within 1 s of a reconnect | PASS, 99 of 99 demonstrated restarts | 0.011239-0.139247 s, median 0.013195 s, p95 0.081912 s |
| #75: restart latency does not grow | PASS | Slope -0.000083 s/cycle, 95% interval [-0.000235, +0.000069]; first-ten and last-ten medians 0.013168 and 0.013255 s |
| #75: at least 100 physical cycles resume within 1 s, DUT talker | Met under the ruling: 100 cycles, 99 of 99 demonstrated restarts | Cycle 22 never stopped, so it is not a restart; the [#608 ruling](https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-5885808887) requires no additional cycle |

The reading of #608 item 3 is decided:
- The [ruling](https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-5885808887) sets the bar at a withdrawal that reaches an IN registrar.
- Its [correction](https://github.com/kebag-logic/milan-fpga/issues/608#issuecomment-5886425487) grades this image: 99 of 99 withdrawals that reached an IN registrar stopped within one PDU.
- The cycle-22 non-stop is attributed to the processor #108 deviation, not accepted as standard behavior.
- #608 item 3 is met without qualification only after the pin-adoption lane carries processor PR #133 and the bench re-runs the 100-cycle withdrawal.
- Processor #134 still grades the LV-registrar stop in simulation, because a peer can also open an LV window.
- Read literally, the item's text asks for 100 of 100; this run is 99 of 100. That reading is kept as history only.

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
- Registrar state at the `Lv`: 42 IN observed, 57 IN inferred, 1 LV (cycle 22). The inference rests on the bridge re-declaring within 0.088 s of all 110 Listener-type LeaveAlls seen while registered, and at least 2.742 s of capture before every `Lv`.
- Cycle 22's LV window: the DUT's own LeaveAll came 0.401121 s after the bridge's, which a conformant participant suppresses (802.1Q-2014 Table 10-5, clause 10.6); the processor's open deviation, #108.
- Three cycles (20, 21, 88) sent their own LeaveAll within one join period after the `Lv`, the window processor PR 130 moved; all three stopped within one PDU.
- The 100-row table is in the #608/#75 page and in the REVIEW READY comment on #606.

## Method notes

- Identity gate as lane B1 ran it: VERSION `0x00020060`; ROM `acad92b9`, QSPI payload `d84bce7b` (seed `eto`), AEM `93742dd2`; ENTITY and CONFIGURATION byte-exact to the AEM image; grader 10/10.
- Fresh state without a reset: an unbind, the processor's 15 s probe freshness (`T-SRP-DAFRESH`), then at least 26 s after the DUT's Talker Advertise `Lv`. Each bind required a 16 s tap window with a DUT LeaveAll and no target Talker Advertise declaration.
- The #75 method of PR #604 on the DUT-talker pair only: `DISCONNECT_RX`, 2 s, `CONNECT_RX`, one bench-lock window per cycle, tap timing on one clock.
- The DUT was never flashed, reset, rebooted or power-cycled; no outlet was switched; the reset epoch read 1 throughout.

## Restore

All restored and proven: the pair unbound on the first attempt, 18 of 18 stream states at connection count 0, the start and end censuses equal on 53 of 53 non-counter reads, a final tap capture with no CRF, grader 10/10, temporary scripts and the temporary capture module removed, the capture host's interfaces as found, outlets as found, the bench lock free.

The DUT's saved-state status read the same at the identity gate and the final restore: slots 229 / 230, image 230, commits 2 / 0, `PP_STAT` `0x5b000c44` (`nvm_pend` 1), `PP_NVM_STAT` `0xc34000e4`. No bind, unbind or cycle wrote a record, and `nvm_pend` 1 was inherited from lane B1. The persisted records were not compared with the found state.

## Limits

- #606's post-reset allocation path is not exercised: reaching it needs a DUT reset. PR #613's first-probe regression remains its evidence.
- The 2 s hold cannot show when an LV registration expires; cycle 22's stop time without a reconnect is not measured.
- Only CRF was measured; AAF remains unmeasured.

## Round 2

Docs only, no bench access, under the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/606#issuecomment-5886531640), answering [R404-1](https://github.com/kebag-logic/milan-fpga/pull/622#issuecomment-5886414299) and [R405-1](https://github.com/kebag-logic/milan-fpga/pull/622#issuecomment-5886527108). One commit on `c37f1d04`.

- **F1, the #608 reading.** The #608 page's verdict table, its decision paragraph and this body grade #608 item 3 and the #75 cycle count under the ruling and its correction, as above. The earlier two-readings text is replaced; the literal count stays as history.
- **F3, cycle 22.** The #608 page's Cycle 22 section records the 0.401121 s gap from the bridge's LeaveAll to the DUT's own, the processor's documented deviation (`10_srp_engine.md` section 6.5 at `c951a9ff`, processor #108), and the session count. "Genuine LeaveAll cycle" is qualified: cycle 22 is not one in that sense.
- **F3, the session count.** 67 DUT LeaveAlls, in 64 of the 112 captures, came less than 10 s after a received bridge LeaveAll (gaps 0.199564-4.807277 s). R404-1's 67 counts LeaveAll PDUs and R405-1's 64 counts captures; the page states both.
- **F2, the saved-state layer.** Both restore sections carry the start and end table (slots, image, records, commits, `PP_STAT` with `nvm_pend`, `PP_NVM_STAT`). The #606 page gives the derivation: 226 console samples, 210 ACMP commands all to the peer's input, no AECP write, and the DUT's stream inputs unbound in all 340 polls. It also gives the cause: binding records are indexed by the DUT's stream inputs, and only its Stream Output 1 was bound, so no record was written and no commit ran. `nvm_pend` 1 is lane B1's residue. Between the two reads the samples carry `PP_STAT` alone. The persisted content was not compared with the found state.
- **F4** was resolved by the maintainer's redacted archive (`666d8897`, disposition 5886425159).
- **Suggestions taken.** Findings index rows for both pages and a corrected #75 row (R404-1 S1, R405-1 S3). The MSRP spacing now reads "1.000 s periodic spacing, 0.2 s after a LeaveAll" (R404-1 S2, R405-1 S2). The inference bound is 2.742 s (R405-1 S1).
- **Measurement tables unchanged.** Every measurement table on both pages and this body's per-bind table is byte-identical to round 1. Only the two verdict tables changed, and the saved-state tables were added. The round-2 packet's `tables_identity.py` receipt holds the diff.

## Validation (all rc 0 at the committed head, foreground, not piped)

`docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `check_em_dash.py --base 13eda870`, `check_doc_paths.py` (pinned Markdown environment); `ci_scope.py --selftest`, `check_baremetal_only.py --check`, `check_feature_status.py --self-test`, `git diff --check`.
