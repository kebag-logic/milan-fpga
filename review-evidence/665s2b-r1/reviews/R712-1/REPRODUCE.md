Run from this packet directory, with an isolated exact-head checkout and the repository's existing host-test prerequisites. The scripts keep all disposable output in `scratch/`. No script edits the supplied checkout. The prescribed simulator is `$VALIDATION_TOOLS/pinned-verilator-5.050/verilator`, version 5.050, revision v5.050.

```sh
REVIEW_CHECKOUT=/path/to/isolated/exact-head-checkout
python3 -B run_focused.py "$REVIEW_CHECKOUT"
python3 -B run_memory.py "$REVIEW_CHECKOUT"
python3 -B run_memory_mutants.py "$REVIEW_CHECKOUT"
python3 -B probe_dma_length.py "$REVIEW_CHECKOUT"
python3 -B verify_checkout.py "$REVIEW_CHECKOUT"
```

The boundary probe must return **1** on the reviewed head, with the 12 failures in `dma-length.log`; the others return zero. Individual planted-memory logs fail deliberately; their campaign succeeds only if the named assertion catches each plant. The focused driver runs independent tasks concurrently with bounded workers; no background shell job is needed. Each invocation must finish before the session ends.

To reproduce the receipt audit, the checkout must have the public evidence commit object `b447e26340def7706919eff18d41f198c29ae5b9` available. `verify_public_evidence.py` reads only the public receipt/script/donor paths enumerated in `public-evidence-integrity.log`, checks their published SHA256 values, and extracts them into `scratch/public-evidence`. It does not read author handoffs or other reviewers' reports.

```sh
python3 -B verify_public_evidence.py "$REVIEW_CHECKOUT"
python3 -B audit_rows.py
sha256sum -c MANIFEST.sha256
```

The audit returns zero for correct receipt arithmetic, while printing the over-share passes supporting F2. It does not claim to execute the CPU simulations. Re-running scripts can rewrite receipts; validate this published packet's manifest before reproducing into a separate copy.
