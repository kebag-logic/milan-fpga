R629-5 focused review reproduction

Use a fresh packet directory for reruns so that the published receipts remain immutable. Copy the portable scripts there. Put the exact source checkout and every generated tree below that packet's `scratch/` directory. Check out `e7d604faa0472d505d6459883b382c2b237ad06d`, with the pinned processor, gPTP and AXI-stream submodules initialized. The expected tree and gitlinks are recorded in `receipts/checkout-verification.json`.

Set `REVIEW_SOURCE` to the disposable checkout, `REVIEW_PACKET` to the fresh packet, and `REVIEW_SIMULATOR` to the verified 5.050 executable. Create `scratch/tmp` and `receipts`. Set `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` to that scratch temporary directory, and `VERILATOR` to the executable. The source's documented build prerequisites apply. This review used Python 3.14.7; install documentation dependencies from the source's locked requirements only into a disposable environment. Dependency and command receipts record the actual checks.

The driver waits for every child and retains a log, status and command record for each check:

```sh
python3 run_checks.py "$REVIEW_SOURCE" "$REVIEW_PACKET" "$REVIEW_SIMULATOR" units
python3 run_checks.py "$REVIEW_SOURCE" "$REVIEW_PACKET" "$REVIEW_SIMULATOR" counters
python3 run_checks.py "$REVIEW_SOURCE" "$REVIEW_PACKET" "$REVIEW_SIMULATOR" direct
python3 run_checks.py "$REVIEW_SOURCE" "$REVIEW_PACKET" "$REVIEW_SIMULATOR" mutants
python3 run_checks.py "$REVIEW_SOURCE" "$REVIEW_PACKET" "$REVIEW_SIMULATOR" f5
python3 run_checks.py "$REVIEW_SOURCE" "$REVIEW_PACKET" "$REVIEW_SIMULATOR" light
python3 run_checks.py "$REVIEW_SOURCE" "$REVIEW_PACKET" "$REVIEW_SIMULATOR" docs
python3 run_checks.py "$REVIEW_SOURCE" "$REVIEW_PACKET" "$REVIEW_SIMULATOR" probes
python3 scripts/run_shifts.py "$REVIEW_PACKET"
python3 scripts/check_standing_controls.py "$REVIEW_SOURCE"
python3 scripts/probe_pending_wrap.py "$REVIEW_SOURCE" "$REVIEW_PACKET"
```

These lines show the available groups, not a requirement to serialize independent groups. Keep concurrent build work within 16 jobs and 12 GB; do not run a synthesis implementation alongside builds. Groups use bounded foreground-owned workers and complete before returning. `run_shifts.py` requires the two retained `direct` builds. The earlier three Python probes and shift launcher are copied unchanged from public evidence. Check their identities against `receipts/public-provenance.json`.

`audit_gaps.py` accepts raw runtime logs and independently recomputes the corrected cadence and packet totals. Supplemental generation/archive commands are recorded in their receipt logs. `fetch_public.py PACKET PATH ...` downloads explicitly named paths relative to the immutable public evidence directory and checks Git blob identities; it performs read-only API calls. Never run candidate host orchestration as part of these focused checks.

The original review clone remained untouched. `verify_checkout.py ORIGINAL_CLONE` checks actual tracked bytes, executable modes, index entries/flags, exact commit/tree and initialized submodule contents. It is expected to reject a disposable test checkout containing build products.

Publication normalizes workspace prefixes in transcript copies. `receipts/publication-normalization.json` records each affected receipt's original and published SHA-256 and replacement counts. Assertions, measurements and return codes remain unchanged. Build products, original unnormalized copies and downloaded source trees stay under unpublished `scratch/`.
