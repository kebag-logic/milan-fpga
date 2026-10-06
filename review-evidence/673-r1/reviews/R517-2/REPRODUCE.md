The packet contains read-only checks for the exact reviewed head. Verify the manifest before rerunning: reruns regenerate receipts. Set REVIEW_CLONE to the isolated clone and PACKET to this packet directory. Every temporary environment and fixture belongs under PACKET/scratch.

```sh
cd "$PACKET"
sha256sum -c MANIFEST.sha256
python3 scripts/integrity.py "$REVIEW_CLONE"
python3 scripts/run_checks.py "$REVIEW_CLONE" "$PACKET"
python3 -m venv "$PACKET/scratch/markdown-env"
"$PACKET/scratch/markdown-env/bin/python" -m pip --disable-pip-version-check install --no-cache-dir --require-hashes -r "$REVIEW_CLONE/tools/markdown/requirements.txt"
python3 scripts/docs_retry.py "$REVIEW_CLONE" "$PACKET"
python3 scripts/cancellation_receipt.py "$REVIEW_CLONE" "$PACKET"
python3 scripts/reconcile.py "$REVIEW_CLONE" "$PACKET"
python3 scripts/integrity.py "$REVIEW_CLONE"
```

The first group preserves prerequisite refusals if the default interpreter lacks the pinned renderer; docs_retry.py uses the isolated locked environment. The group uses four workers, joined before returning. Each command has a 300-second guard. The reconciliation script needs read-only access to the public repository and current PR; it refuses a moved head. Historical public endpoint snapshots can change after this review. None of these scripts runs a native suite bank, compiler, container or host-side workflow orchestrator.

Raw cancellation output remains in scratch; its publishable copy replaces only the absolute scratch root with $SCRATCH. All other validation logs retain their command output bytes. Source integrity compares actual disk blobs and executable modes against commit objects with replacement objects disabled, then compares every index entry and verifies the required registered submodules. The unused external dependency remains uninitialized.
