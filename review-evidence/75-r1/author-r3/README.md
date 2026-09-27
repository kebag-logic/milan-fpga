# Round 3 addendum

[A391] Refs #75. PR #604.

The [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/75#issuecomment-5860554971)
limits this addendum to four corrections. It uses recorded data only.
Original round-1 and round-2 packets remain unchanged.
No raw captures or installed dependencies are included.

## Reproduce the analysis

Use the retained operator packet and its raw capture index.
Arguments below name input directories; outputs go to a separate directory.

```sh
python3 -B recompute.py OPERATOR_PACKET RAW_CAPTURE_ROOT OUTPUT_DIRECTORY
python3 -B declarations.py OPERATOR_PACKET RAW_CAPTURE_ROOT OUTPUT_DIRECTORY
python3 -B publish_records.py OPERATOR_PACKET OUTPUT_DIRECTORY
python3 -B check_controls.py OUTPUT_DIRECTORY ROUND_TWO_ADDENDUM
```

`recompute.py` retains the round-2 wire predicate and consistency checks.
Classification now uses ordinary conditions; all consistency failures raise errors.
It refuses both `-O` and `PYTHONOPTIMIZE` before reading inputs.
Outcome counts and rejected identities derive from the computed rows.
The 100 attempts per direction remain the assigned dataset contract.
The resulting stop ledger, quantiles and slopes equal round 2.

`declarations.py` counts only New, JoinIn and JoinMt as declarations.
It reads every retained talker MSRP TSV and verifies each against raw frames.
The setup TSV also matches, making 101 verified event records.
The hold window is [disconnect response, next connect command).
`hold-declarations.csv` counts each hold; `hold-events.csv` preserves its events.
The derived result is 99/100 declared holds, with cycle 1 the exception.
Cycle 1 withdraws, sends only Mt through the hold, and restarts in 0.117736084 s.
That exception constrains the initial-bind inference owned by #606.

`listener-events.csv` records every target bridge Listener event after disconnect
for non-stops 13, 24 and 75, including exact tap times and bracketing CRF times.
`declarations-summary.json` retains their full chronology and counter evidence.
Withdrawal crosses the DUT segment without an intervening Listener declaration
until after reconnect success, while CRF continues with at most 2.000053 ms gaps.
This supports DUT-side non-stop behavior at the tapped boundary under #608.
Internal acceptance of the withdrawal and the responsible state remain unproved.
The missing three restarts remain under #75; AAF remains unmeasured.

## Published cycle records

`talker-013`, `talker-024`, and `talker-075` contain all small cycle records.
They use the same neutral roles and accepted wire identifiers as cycles 1-5.
Only `raw-artifacts.json` changes: its historical absolute location becomes a
relative capture identifier. Raw bytes remain in retained storage.
The local `MANIFEST.sha256` files cover the publication copies.
`published-records.csv` gives both original and published hashes for all 48 records.
Historical acquisition `PASS` labels are preserved, not endorsed as restart verdicts.
The current verdict is `NOT_RESTART` in the round-3 stop ledger.

## Controls and validation

`check_controls.py` exercises silence, one settled PDU, continuous traffic,
early resumption, both optimization refusals, declaration-event membership,
and the old universal declaration claim on recorded cycle 1.
It also changes input counts and identities to check the printed outcome.
`controls.json` records all 14 checks and the unchanged numeric evidence.

`run_gates.py` runs the assigned commands synchronously at a clean committed head.
The only disposable clone is for the requested absent-submodule comparison.
It is created outside this packet, pinned to the head, checked without
submodules, checked again without Git metadata, then removed.
`render_tables.py` verifies every table row and cell with the pinned renderer.
`gates.json` and `table-render-check.json` identify their exact evidence.

`HANDOFF.md` records per-item file references, all 200 stop checks,
the recomputed distributions, local gates, and delivery status.
`PR-BODY.md` is the prepared replacement body; it retains [A386] and Refs #75.
Publishing the commit, addendum and body remains a separate authorized step.
