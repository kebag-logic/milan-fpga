# Round-2 reconnect analysis addendum

[A389], PR #604, refs #75.

This addendum answers the
[round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/75#issuecomment-5860261220).
It supersedes the round-1 talker restart count and quantiles.
The original packet and every capture remain unchanged.

Read `HANDOFF.md` for the change map and gate evidence.
`stop-checks.csv` contains every numbered attempt's wire and counter checks.
`recomputed-summary.json` contains distributions, regression, and capture-size data.
`stop-table.md` and `capture-size-table.md` are generated tables.
`input-hashes.csv` authenticates the small source records used per attempt.
Raw capture hashes and relative identifiers are in `stop-checks.csv`.

## Reproduction

Run this entirely offline with the retained inputs:

```sh
python3 -B recompute.py OPERATOR_PACKET RAW_CAPTURE_ROOT OUTPUT_DIRECTORY
```

The first argument is the original operator packet directory.
The second contains the indexed cycle directories and `tap.pcap` files.
The third is a separate output directory for the addendum.
Use the standard interpreter without optimization; assertions must remain enabled.
No acquisition code, hardware connection, or network action runs.

The public source packet is pinned at
[d7f333ac](https://github.com/kebag-logic/milan-fpga/tree/d7f333acdf4d630df33761c0093a8cb87b4f618a/review-evidence/75-r1/author).
It publishes cycles 1-5 per direction and all cycle directory hashes.
The other cycle records and raw captures remain retained inputs.
No private paths or equipment names are required in outputs.

## Interpretation

All 200 original response-to-next-PDU intervals reproduce exactly.
Stop assertions pass 197 attempts and fail three talker attempts.
Those failures are preserved as findings, not accepted restarts.
Successful completion of analysis does not turn them into passes.

The stop window begins 0.5 seconds after disconnect-response crossing.
It ends at reconnect-response crossing, excluding that endpoint.
This settling allowance is an analysis boundary, not protocol permission.
The original final-half-second window is also recomputed independently.
Command-to-response counts close the original window's missing tail.

The three non-restarts transmit continuously through the entire hold.
Each has 1,000 valid PDUs and zero start/stop increments.
Sequence and timestamp progression remain continuous through that window.
The replay rejects them before calculating restart distributions.
Both counter endpoints and between-cycle continuity are checked.

Latency regression retains original cycle numbers after excluding non-restarts.
It uses ordinary least squares with a two-sided Student-t interval.
Residual degrees of freedom are sample count minus two.
The script records its critical value and standard error.
The interval assumes independent errors with constant variance.
It describes this population rather than guaranteeing future performance.

The retained validity mask is `payload[1] & 0xf0 == 0x80`.
It does not test bit 3 (`mr`), `fs`, or `tu`.
Replay separately verifies all three were zero throughout numbered captures.
This corrects the review's description of the mask without changing it.

Issue #75 retains the three non-restarts and missing talker cycles.
Issue #606 owns the separate initial-bind path.
AAF remains unmeasured. No issue closure or merge is claimed.

## Validation boundary

Only the findings page and findings index change in the repository.
Gate evidence belongs to the local committed head in `HANDOFF.md`.
No push, PR edit, or hosted-context result is claimed.
Every retained addendum file stays below 200,000 bytes.
Packages and the disposable documentation clone stay outside this packet.
