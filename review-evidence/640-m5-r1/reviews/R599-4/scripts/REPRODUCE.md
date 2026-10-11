These commands take an existing checkout at the reviewed head.
Run from the packet directory, setting `REVIEW_REPO` to that checkout.
All processes stay in the foreground. The documentation driver runs six
independent checks concurrently and waits for every child before returning.

```sh
python3 -m venv scratch/docs-venv
scratch/docs-venv/bin/python -m pip install --require-hashes -r "$REVIEW_REPO/tools/markdown/requirements.txt"
scratch/docs-venv/bin/python scripts/run_docs.py --repo "$REVIEW_REPO" --out receipts/docs-reproduced
python3 scripts/check_delta.py "$REVIEW_REPO" --pr-body receipts/pr-body.md
python3 scripts/check_identity.py "$REVIEW_REPO"
python3 scripts/check_public_evidence.py --scratch scratch/public-evidence-reproduced
python3 scripts/hosted_snapshot.py --out receipts/hosted-jobs-reproduced.json
```

The delta checker returns 1 for the captured PR-body discrepancy; its
preceding merge, plan arithmetic and source-identity assertions pass.
The documentation and identity checks return 0.
Hosted state is a time-specific observation and may change on reproduction.
The public-evidence check reads only the specified immutable author packet.

The focused reader-registry gate was also run from the reviewed checkout:
`PYTHONDONTWRITEBYTECODE=1 python3 scripts/measure_test_evidence.py --check`.
`git diff --check 6bfeeb132fa0b1ad8a5b957446c66a498e633af7 HEAD` was clean.
No simulation, implementation, broad bank, workflow replica or hardware
campaign is invoked by this packet.
