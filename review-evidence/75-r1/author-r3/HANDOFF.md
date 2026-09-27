# Round 3 handoff

[A391] Refs #75. PR #604.

Status: all four assigned items complete; REVIEW READY posted and verified.
Branch: `75-reconnect-bench`.
Starting head: `5c7577e51702b00683a121f97a9806c167eb072b`.
Round-3 head: `9c18068512dec844d24fdff7fe0a3eb0d63c14f5`.

Assignment: [items 1-4](https://github.com/kebag-logic/milan-fpga/issues/75#issuecomment-5860554971).
TAKEN: [required start comment](https://github.com/kebag-logic/milan-fpga/issues/75#issuecomment-5860563147).
Reviewers: [R370] and [R371]; independent re-review remains required.
Only the findings page and findings index change in the repository.
All recomputations use retained data, opened read-only.
The original round-1, round-2, and review packets remain unchanged.
No hardware, push, PR edit, merge, or issue closure occurred.

## Per-item response

| Assignment / reviewer | Change, file:line | Response and evidence |
|---|---|---|
| 1 / R370-2 F1 | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:220`; `declarations.py:19`; `declarations.py:190` | Counts only New, JoinIn and JoinMt. The derived census is 99/100 holds with DUT Talker Advertise; cycle 1 has zero. Every retained talker TSV and the setup TSV match raw-frame MSRP replay. `hold-declarations.csv` retains all 100 counts; `hold-events.csv` retains the events. |
| 1 / R370-2 F1, #606 implication | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:229`; `declarations-summary.json` | Cycle 1 withdraws, sends only Mt during the hold, and remains undeclared until after reconnect success. It restarts in 0.117736084 s. The page removes the universal DUT-state contrast and points #606 to this counterexample. `check_controls.py:48` rejects the old universal claim on the actual census. |
| 2 / R371-2 F5 and R370-2 S1 | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:615`; `declarations.py:166`; `listener-events.csv` | Publishes each bridge Listener Lv and every subsequent target Listener declaration in cycles 13, 24 and 75. None re-declares until after reconnect success. CRF continues across all events, with zero DUT start/stop deltas. This supports DUT-side non-stop behavior at the tapped boundary; internal acceptance and cause remain unproved. |
| 2 / ownership and publication | `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:615`; `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:959`; `docs/findings/README.md:11`; `published-records.csv` | #608 is linked from stop checks, acceptance and the index. All 48 small source records for the three cycles are prepared in separate directories. Only raw-capture location fields become relative identifiers. Original and publication hashes, plus each directory manifest, verify. |
| 3 / R371-2 S5 | `recompute.py:15`; `recompute.py:67`; `recompute.py:72`; `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:1270` | Ordinary conditions classify the stop, and explicit consistency checks replace every assert. Both -O and PYTHONOPTIMIZE refuse before reading data. Controls cover silent holds, one settled PDU, continuous traffic and early resumption. |
| 4 / R370-2 S2 | `recompute.py:80`; `docs/findings/75_RECONNECT_RESTART_MEASUREMENT.md:1274` | Printed totals and excluded identifiers derive from computed rows. The fixed rejected-cycle equality is removed. Controls change both the input count and rejected identity, and also exercise no rejected rows. |

## Declaration census and cycle 1

The census window is [disconnect response, next connect command).
New, JoinIn and JoinMt declare; In, Mt, Lv and LeaveAll do not.
The count derives from all 100 retained talker `msrp.tsv` files.
The result is 99 declared holds, with cycle 1 the sole exception.

Cycle 1's events after disconnect success are Lv at +0.120687323 s,
then Mt at +0.520682079 and +1.720684762 s.
No declaration appears between disconnect and reconnect responses.
The first post-response declaration is +0.111313165 s.
Ready follows 0.006299407 s later; CRF follows another 0.000123512 s later.
The restart interval is 0.117736084 s.
The initial bind declares earlier after its response (+0.079237250 s),
yet takes 6.889398468 s to produce CRF.
The shared absence at the response cannot alone explain that delay.
The page and prepared REVIEW READY direct #606 to cycle 1.
No modification or comment on #606 was made.

## Three non-stop chronologies

All times below come from the same per-capture tap clock.
The first re-declaration in each cycle is Listener New, value 2.
No target bridge Listener declaration occurs after Lv and before reconnect success.

| Talker cycle | Listener Lv after disconnect, s | Reconnect response after disconnect, s | First re-declaration after disconnect, s | First re-declaration after response, s | CRF PDUs from Lv to re-declaration |
|---|---|---|---|---|---|
| 13 | 0.009770679 | 2.009383717 | 2.083160130 | 0.073776413 | 1036 |
| 24 | 0.010356881 | 2.008905104 | 2.027609644 | 0.018704540 | 1009 |
| 75 | 0.025307595 | 2.009020118 | 2.027707850 | 0.018687732 | 1001 |

The complete target bridge Listener sequence after disconnect follows.
Every event carries Listener value 2; Lv still means withdrawal.

| Talker cycle | Bridge Listener event | After disconnect response, s | After reconnect response, s |
|---|---|---|---|
| 13 | Lv | +0.009770679 | -1.999613038 |
| 13 | New | +2.083160130 | +0.073776413 |
| 13 | New | +2.182730731 | +0.173347014 |
| 13 | JoinMt | +2.280863937 | +0.271480220 |
| 24 | Lv | +0.010356881 | -1.998548223 |
| 24 | New | +2.027609644 | +0.018704540 |
| 24 | New | +2.121717417 | +0.112812313 |
| 24 | JoinMt | +2.221744020 | +0.212838916 |
| 75 | Lv | +0.025307595 | -1.983712523 |
| 75 | New | +2.027707850 | +0.018687732 |
| 75 | New | +2.122542224 | +0.113522106 |
| 75 | JoinMt | +2.222919836 | +0.213899718 |

CRF remains continuous at 2 ms intervals throughout the withdrawal interval.
The maximum gap through first re-declaration is 0.002000053 s in all three.
The same bound holds across each listed event's bracketing CRF pair.
Their STREAM_START and STREAM_STOP increments are zero.
No DISCONNECT_TX command crosses the tap in these captures.

Attribution: DUT-side non-stop behavior at the tapped boundary.
The bridge withdrawal crosses the DUT segment while transmission continues.
No upstream re-declaration explains the intervening traffic.
The capture does not prove internal receipt or identify the state/timer.
That mechanism and its correction remain owned by #608.
The 25.308 ms withdrawal in cycle 75 replaces the earlier inferred range.

The `talker-013`, `talker-024` and `talker-075` directories contain
all small per-cycle records, scrubbed like the earlier public cycles.
Historical acquisition PASS labels remain intact, not current restart verdicts.
`published-records.csv` documents all source and publication hashes.
The only content transformation replaces absolute raw-capture locations.
Wire identifiers remain within the accepted class from the round-2 decision.
No raw capture is copied into this packet.

## Stop checks per cycle

All 200 captures reproduce their retained size, hash and response anchors.
CRF validity, timing, source, destination and counter continuity checks pass.
The stop window is [disconnect response + 0.5 s, reconnect response).
The settling allowance defines analysis, not a protocol deadline.
Command-response counts close the original observation gap.
Start/stop pairs give counter increments, not cumulative values.
DUT counters refer to output 1; active-talker counters follow direction.

The derived outcome is 197 PASS and 3 FAIL.
Talker cycles 13, 24 and 75 are NOT_RESTART and excluded.
Each has 1,000 hold PDUs and 250 final-half-second PDUs.
All other attempts have zero settled-window PDUs and one active start/stop.
The complete ledger and summary are byte-identical to round 2.

| Direction | Cycle | Settled PDUs | Command-response PDUs | DUT start/stop | Active talker start/stop | Stop check |
|---|---|---|---|---|---|---|
| DUT listener | 1 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 2 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 3 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 4 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 5 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 6 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 7 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 8 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 9 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 10 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 11 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 12 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 13 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 14 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 15 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 16 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 17 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 18 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 19 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 20 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 21 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 22 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 23 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 24 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 25 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 26 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 27 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 28 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 29 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 30 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 31 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 32 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 33 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 34 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 35 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 36 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 37 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 38 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 39 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 40 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 41 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 42 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 43 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 44 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 45 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 46 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 47 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 48 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 49 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 50 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 51 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 52 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 53 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 54 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 55 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 56 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 57 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 58 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 59 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 60 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 61 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 62 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 63 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 64 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 65 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 66 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 67 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 68 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 69 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 70 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 71 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 72 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 73 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 74 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 75 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 76 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 77 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 78 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 79 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 80 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 81 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 82 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 83 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 84 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 85 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 86 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 87 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 88 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 89 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 90 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 91 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 92 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 93 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 94 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 95 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 96 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 97 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 98 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 99 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT listener | 100 | 0 | 0 | 0 / 0 | 1 / 1 | PASS |
| DUT talker | 1 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 2 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 3 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 4 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 5 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 6 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 7 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 8 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 9 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 10 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 11 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 12 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 13 | 754 | 4 | 0 / 0 | 0 / 0 | FAIL |
| DUT talker | 14 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 15 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 16 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 17 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 18 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 19 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 20 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 21 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 22 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 23 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 24 | 754 | 4 | 0 / 0 | 0 / 0 | FAIL |
| DUT talker | 25 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 26 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 27 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 28 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 29 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 30 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 31 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 32 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 33 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 34 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 35 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 36 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 37 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 38 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 39 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 40 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 41 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 42 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 43 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 44 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 45 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 46 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 47 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 48 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 49 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 50 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 51 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 52 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 53 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 54 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 55 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 56 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 57 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 58 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 59 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 60 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 61 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 62 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 63 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 64 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 65 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 66 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 67 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 68 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 69 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 70 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 71 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 72 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 73 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 74 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 75 | 755 | 5 | 0 / 0 | 0 / 0 | FAIL |
| DUT talker | 76 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 77 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 78 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 79 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 80 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 81 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 82 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 83 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 84 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 85 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 86 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 87 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 88 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 89 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 90 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 91 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 92 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 93 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 94 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 95 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 96 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 97 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 98 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 99 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |
| DUT talker | 100 | 0 | 0 | 1 / 1 | 1 / 1 | PASS |

## Recomputed distribution

Seconds; p95 uses nearest rank. Initial binds and non-restarts are excluded.

| Direction | Attempts | Demonstrated restarts | Min, s | Median, s | p95, s | Max, s |
|---|---|---|---|---|---|---|
| DUT listener | 100 | 100 | 0.006641168 | 0.110279505 | 0.188503018 | 0.204858977 |
| DUT talker | 100 | 97 | 0.017426921 | 0.019174613 | 0.042346644 | 0.117736084 |

The listener and talker distributions remain unchanged from round 2.
The talker count remains three short of the 100-restart requirement.
Both OLS slope intervals still include zero; no growth conclusion changes.
Original cycle numbers remain intact.
#75 stays open, AAF remains unmeasured, #606 owns initial bind,
and #608 owns non-stop behavior.

## Gates

Every row below ran at the round-3 committed head above, rc 0.
Commands ran in the foreground, without pipelines, with generous timeouts.
The candidate uses its physical workspace path and pinned validation submodules.
Pinned Markdown dependencies live outside the output directory.
The bare-metal gate uses the existing base interpreter with PyYAML.

| Command / context | Return code |
|---|---|
| `python3 scripts/docs_check.py`; physical candidate; pinned submodules present | 0 |
| `python3 scripts/check_doc_style.py`; physical candidate; pinned submodules present | 0 |
| `python3 scripts/gen_toc.py --check`; physical candidate; pinned submodules present | 0 |
| `python3 scripts/check_em_dash.py --base 8bc97021`; physical candidate; pinned submodules present | 0 |
| `python3 scripts/check_doc_paths.py`; physical candidate; pinned submodules present | 0 |
| `python3 scripts/ci_scope.py --selftest`; physical candidate; pinned submodules present | 0 |
| `python3 scripts/check_baremetal_only.py --check`; physical candidate; pinned submodules present; base interpreter with PyYAML | 0 |
| `python3 scripts/check_feature_status.py --self-test`; physical candidate; pinned submodules present | 0 |
| `git diff --check`; physical candidate; committed head | 0 |
| `git diff --check 8bc97021 HEAD`; physical candidate; full committed PR delta | 0 |
| `python3 scripts/docs_check.py`; exact-head validation clone; no submodules | 0 |
| `python3 scripts/docs_check.py`; same validation tree; no submodules or Git metadata | 0 |

The explicit absent-submodule gate used one disposable validation clone.
It was pinned to the committed head, with no submodules populated.
The no-Git check then removed only that clone's metadata.
The clone was deleted after validation; no other implementation checkout changed.
This is the narrow clone required by the assigned gate comparison.
No hosted-context pass is claimed.

`gates.json` and each `gate-*.txt` preserve command, context, head and rc.
`controls.json` records 14 passing replay controls.
`evidence-crosscheck.json` confirms the tables, numerical claims and record hashes.
`table-render-check.json` records 34 tables and 1,207 body rows.
Every source cell survives the pinned Markdown renderer unchanged.
Direct findings-page prose analysis reports zero findings in `page-style.json`.
`packet-check.json` records final privacy, size and manifest verification.
The known-name policy uses hashes; no forbidden names appear in this packet.

## Delivery

`PR-BODY.md` retains its [A386] first line and Refs #75.
Its Round 3 section answers each assigned review point.
The commit subject is one line, with no body or trailers.
The working tree is clean; no push or PR edit was made.
The round-3 addendum is prepared for later publication with that commit.
REVIEW READY: [posted comment](https://github.com/kebag-logic/milan-fpga/issues/75#issuecomment-5860674129).
The published body matches `REVIEW-READY.md`; `delivery.json` records verification.
Only the authorized TAKEN and REVIEW READY comments were posted.
No independent review verdict is supplied by this author.
