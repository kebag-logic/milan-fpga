Replay from the exact detached processor head `8947bafdd62b4bf991debf7bfd8cdb73994a3a81`.
Set `TREE` to that checkout and `PACKET` to this packet's root. No script changes
tracked processor sources. Disposable trees and temporary directories go under
`$PACKET/scratch`, which is excluded from publication.

```
mkdir -p "$PACKET/scratch" "$PACKET/receipts"
python3 "$PACKET/scripts/fetch_public.py"
python3 "$PACKET/scripts/audit_delta.py" "$TREE"
python3 "$PACKET/scripts/plant_audit.py" "$TREE"
python3 "$PACKET/scripts/run_focused.py" "$TREE"
python3 "$PACKET/scripts/run_units.py"
```

The public fetch is read-only and pinned to evidence archive `350e06ae86bd5372f9f79b5fa5c95e0f3863b5d2`.
It selects author evidence and the explicitly requested earlier probe script;
it never downloads review report files. It requires a configured `gh` client.
The compiler wrapper defaults to the assigned scoped 5.050 executable. Set
`PP_REVIEW_COMPILER` to an equivalent executable on another machine; verify its
version before running. It caps each build at four workers. `run_focused.py`
uses two concurrent reviewer-probe units, one shipped-campaign unit (`--jobs 1`),
and one fixture unit; outer make invocations use `-j16`. Each child is joined
and has a dedicated log and return code. No detached jobs are created.

`run_units.py` was run after the shipped-campaign unit completed, overlapping the
remaining long top simulations. Do not add it while all four build slots are busy.
The top default fixture runs the default binary, not all seven builds. The
default-timeout fixture runs `--withdraw-only` in the existing sixth build.

Documentation: run `make -j16 check` in the tracked checkout. Its inventory checks
require Git metadata. If the diagram dependency is unavailable, bootstrap its
environment only in a disposable source copy under `scratch`, then put that
environment's `bin` directory first in PATH when running the tracked checkout's
check target. Retain the log and exit code. The archive-only failed attempt and
corrected tracked run are both disclosed in the receipts.

`verify_checkout.py "$TREE"` validates every tracked blob, mode and index entry.
It also expects `scratch/parent-recorded-tree.json` and `scratch/parent-live-tree.json`;
recreate them using read-only API tree requests for parent revisions
`28f9666feab2b2ba287643c63ed3a16b1e0bb863` and
`d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`, with `recursive=1`.
These remote trees are metadata, not parent checkouts or bank executions.
