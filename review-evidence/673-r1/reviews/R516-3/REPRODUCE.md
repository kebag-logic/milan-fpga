R516-3 portable reproduction

Run from this packet directory. Set REVIEW_CLONE to a detached checkout at
72d3780d23a0b96362f8ae64059311b866ff5776 with its required submodules initialized.
The scripts derive the packet path from their own location. All child processes
are waited for in the foreground; the gate supervisor uses four workers.
Only focused checks run. No build bank, hardware, or workflow replica is invoked.

Verify delivered receipts before rerunning: reruns replace logs.

```sh
rtk proxy sha256sum -c MANIFEST.sha256
rtk proxy python3 scripts/composition.py "$REVIEW_CLONE"
rtk proxy python3 scripts/semantic_checks.py "$REVIEW_CLONE"
rtk proxy python3 scripts/run_gates.py "$REVIEW_CLONE"
rtk proxy python3 scripts/reconcile.py "$REVIEW_CLONE"
rtk proxy python3 scripts/verify_tree.py "$REVIEW_CLONE"
```

The public reconciliation command needs read-only repository API access.
The source reviews must be read after an independent verdict and ledger exist.
This packet records that checkpoint in receipts/independent-pass.md.

If the Markdown prerequisites are absent, install the repository lock into
scratch and rerun only the affected checks:

```sh
rtk proxy python3 -m venv --system-site-packages scratch/markdown-env
rtk proxy scratch/markdown-env/bin/python3 -m pip install --require-hashes -r "$REVIEW_CLONE/tools/markdown/requirements.txt"
rtk proxy env PATH="$PWD/scratch/markdown-env/bin:$PATH" python3 scripts/run_gates.py "$REVIEW_CLONE" toc_check toc_anchors em_dash
```

Initial prerequisite refusals remain in their original logs and rc files;
successful reruns have the _retry suffix. Scratch is never published.
