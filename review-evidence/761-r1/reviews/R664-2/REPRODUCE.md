Run from the reviewed repository at eef90b4238b6c19b679b44adc6f09362809be153. Supply an absolute packet directory containing these scripts. All commands stay in the foreground. Builds and temporary source copies go under packet scratch/; no source edit is required.

```sh
export PYTHONDONTWRITEBYTECODE=1
export REVIEW_SIMULATOR=/absolute/path/to/the/prescribed/simulator
python3 "$PACKET/scripts/spot_checks.py" "$REPO" "$PACKET"
python3 "$PACKET/scripts/crf_both.py" "$REPO" "$PACKET"
python3 "$PACKET/scripts/verify_checkout.py" "$REPO"
```

The recorded run used the prescribed 5.050 installation. The wrapper limits each compilation to four jobs. The focused script concurrently runs the AAF campaign, CRF positive control and receipt controls. The paired CRF script runs at most two builds concurrently. Peak build concurrency is eight compilation jobs. Do not run both scripts concurrently without accounting for their combined budget.

The clean harnesses return 0. Every negative control returns 1 with its named check failing; the campaign scripts return 0 only after confirming those expected failures. Compile diagnostics remain in scratch, while raw harness verdicts and return codes are in receipts.

Fetch evidence commit 32af21b0d0ae35008fa65c3199b282419f171274 into the repository, then run:

```sh
python3 "$PACKET/scripts/audit_public.py" "$REPO" "$PACKET"
```

That command reads only the selected public author receipts and their manifest. It verifies published_sha256 and extracts receipts beneath scratch/public. It does not inspect private material or other reviewer reports and does not authenticate a signature.

REPORT.md states the separate source, hosted, candidate and hardware limits. Scratch is never publication material.
