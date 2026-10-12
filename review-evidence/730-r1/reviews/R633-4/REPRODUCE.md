Use a disposable exact-head checkout and this packet.
No daemon or live replay is required or permitted by these commands.
The namespace helper needs unprivileged user namespaces and `bwrap`.
The system Python needs PyYAML; the recorded environment had 6.0.3.

```sh
review_checkout=/path/to/exact-head-checkout
review_packet=/path/to/packet
mkdir -p "$review_packet/scratch/tmp" "$review_packet/scratch/pristine"
git -C "$review_checkout" archive 31e53e82a4a1604569ccacba8473f21e70b9cbc0 |
  tar -x -C "$review_packet/scratch/pristine"
chmod +x "$review_packet/scripts/sandbox.sh"
python3 "$review_packet/scripts/run_focused.py" "$review_checkout"
python3 "$review_packet/scripts/run_mutation_campaigns.py"
sh "$review_packet/scripts/reviewer_sandbox.sh" "$review_checkout" "$review_packet" \
  python3 -I /packet/scripts/probe_cleanup_entry.py /work
```

The new cleanup-entry probe exits 1 at the reviewed head.
Its three body-signal controls pass; three cleanup-entry cases fail.
The unchanged round-1 probe also exits 1, for harness incompatibility.
Its published compatibility adapter passes the original defect cases.
The full self-test must pass 498 arms.
The mutation results must match REPORT.md, including Q24 killed.
Every mutation has separate raw output and status receipts.
The two campaign drivers use eight workers each, sixteen total.
All drivers await foreground children and use bounded waits.

For documentation checks, install dependencies only inside packet scratch:

```sh
python3 -m venv "$review_packet/scratch/markdown"
"$review_packet/scratch/markdown/bin/python" -m pip install --require-hashes \
  -r "$review_checkout/tools/markdown/requirements.txt"
python3 "$review_packet/scripts/run_gates.py" "$review_checkout"
git -C "$review_checkout" diff --check dc4d06cb HEAD
python3 "$review_packet/scripts/verify_integrity.py" "$review_checkout"
```

The recorded checkout used an alternate object store outside the namespace.
Only the isolated whitespace check failed to resolve that store.
Its read-only host Git rerun passed; both receipts are retained.
Do not expose a host checkout to candidate orchestration to fix that access.

The sandboxed dry-run receipt uses synthetic PR/head values and inert collaborators.
It exercises output wiring without executing the printed command.
The original public scripts are retained under `public-inputs/`.
Their publication provenance is bound to commit
`24efc3346903a44ea112bfe1c6b3b6d86870cacb` in `public-input-hashes.json`.
The selected script copies have their own unchanged-byte verification receipt.
The integrity verifier changes only the original verifier's expected head/tree.

The manifest excludes all scratch data and itself.
REPORT.md is published separately and is also excluded from the manifest.
One initial diagnostic has its private alternate-object path redacted;
`receipts/diff-check-rerun.json` records that transformation.
