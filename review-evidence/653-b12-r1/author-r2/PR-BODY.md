[A543] Refs #653

## Status

Bench findings on flashed dev `bbf704ec`, using controller library source `a71ffa99` and the application input-error rule at `a13db9d9`.

## Description

All 182 unbinds returned SUCCESS with response-first ordering. Both ten-minute sequence windows and all early PDU checks showed zero sequence mismatches and interruptions. The reference peer reported one EARLY and one LATE timestamp increment; their cause remains unresolved.

The findings include 140 fixed-hold cycles and 40 separate push-boundary controls, with actual durations and timing evidence.

## how-to-reproduce

The dated method and per-cycle tables are in `docs/findings/653_DISCONNECT_ORDER_BENCH.md`.

## how-to-validate

All seven required documentation gates returned 0 on `bef8dd7036f711bf286929fa4cba6bf724c7118d`. The [bounded public evidence packet](https://github.com/kebag-logic/milan-fpga/tree/9649a107657bdc77d1c47d7ce735e6a282394235/review-evidence/653-b12-r1) includes the operator handoff, per-cycle receipts and manifest; large captures are indexed separately.

## DoD

Both entities' bindings, formats, maps and clock sources match their as-found readbacks. The bench lock is released. Only `docs/findings/653_DISCONNECT_ORDER_BENCH.md` changes.

## Round 2

The retained startup headers show first-to-second timestamp steps of -23,612,829 ns and +521,369,096 ns in the two flagged cycles, with consecutive sequence values and `tv=1`. Earliest nonzero reads precede unbind. Absolute gPTP correlation is NOT RUN; fault ownership remains unresolved.

The packet now includes all 43 successful role-safe restoration projections, a strict comparator, and fourteen rejected adverse controls plus a passing equal-success control. Peer identifiers in encoded wire receipts are replaced with consistent neutral tokens.

Reproduce offline from the updated packet:

```sh
timeout 15s python3 -B startup_decode.py startup-headers.json
timeout 15s python3 -B check_startup.py .
timeout 15s python3 -B restore_compare.py restore-start.json restore-end.json
timeout 20s python3 -B check_restore.py . /tmp/653-b12-review-controls
```

All seven required round-2 gates returned 0 at `2263c6288956a5edd841df62252326780edd4870`; `validation-r2.json` records commands and results. No bench access occurred in this round. The updated packet awaits manager publication and independent re-review.
