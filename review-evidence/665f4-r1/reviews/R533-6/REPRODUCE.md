Use a clean checkout at `cce554f64f6bdab1f6d26e5c4d7b46d54d228c52`.
Initialize the four required submodules at their gitlinks.
Set `REPO` to that checkout and `PACKET` to this packet.
All generated products belong below `$PACKET/scratch`.

```sh
python3 "$PACKET/scripts/run_parallel.py" "$REPO"
python3 "$PACKET/scripts/fetch_runtime.py"
python3 "$REPO/scripts/ci_rv32_sdk.py" --destination "$PACKET/scratch/sdk"
python3 "$PACKET/scripts/run_command.py" sizes python3 "$PACKET/scripts/measure.py" "$REPO"
python3 "$PACKET/scripts/run_command.py" mailbox python3 "$PACKET/scripts/mailbox.py" "$REPO" --hdl "$PINNED_VERILATOR"
python3 "$PACKET/scripts/run_command.py" static python3 "$PACKET/scripts/static.py" "$REPO"
python3 "$PACKET/scripts/run_command.py" upstream python3 "$PACKET/scripts/upstream.py" "$REPO"
python3 "$PACKET/scripts/run_command.py" integrity python3 "$PACKET/scripts/integrity.py" "$REPO"
python3 "$PACKET/scripts/reproduce_public_recipe.py" "$REPO"
```

Run independent groups concurrently while respecting sixteen compilation jobs.
The parallel driver uses four foreground children with four compilation jobs each.
The linked-image driver uses four workers.
The mailbox driver runs two bus builds with two compilation jobs each.
The dependency setup uses sixteen jobs; run it after other builds finish.
The two dependency profiles then use eight jobs each.
Every driver joins its children before returning. No shell background jobs are used.

The first command runs source suites, the full SRP mutation campaign, coverage,
and the unchanged Round 5 probe with its retry-removal control.
The retry-removal binaries must exit 1 and name the withdrawal test's active-state assertion.
The collector exits 0 only when those negative controls are detected.

The public-recipe reproduction is intentionally different from a successful gate:
its export must exit 128 on the absent tracked path. The collector records that
status and exits 0 when the finding is reproduced.

The linked-size driver uses the exact image fixture and runtime recipe. For FC
base exports it selects the actual pre-MAAP portable source population, avoiding
references to files that did not exist at that base. Both head and base use the
same pinned compiler and verified runtime inputs. All compiler artifacts remain
in scratch; `receipts/sizes.json` retains their hashes and section measurements.

The original upstream collector exited 1 after both profile suites passed because
the review driver initially misspelled a reversal selector. The corrected three
reversal runs are recorded separately in `note-reversals-OFF/ON` receipts.
The final scripts contain the corrected selector. No production source was changed.

Receipt text uses `${REPO}`, `${PACKET}`, `${STANDARDS_DIR}` and `${TOOLS}` for
local installation roots. `receipt-provenance.json` binds original and normalized
bytes. Standard text and disposable source/build trees are excluded from publication.
