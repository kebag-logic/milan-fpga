Run from a detached checkout of af5be4710c3516cc247c353213d6939fa8d23f57.
Initialize protocol-processor, gptp-processor and third_party/verilog-axis at
their recorded gitlinks. Place this packet beside the candidate checkout.
Only the packet's scratch directory receives disposable dependencies and files.

```sh
python3 -m venv --system-site-packages <packet>/scratch/venv
<packet>/scratch/venv/bin/python -m pip install --no-cache-dir --require-hashes -r tools/markdown/requirements.txt
<packet>/scratch/venv/bin/python <packet>/run_receipt.py --repo <candidate> --name composition -- <packet>/scratch/venv/bin/python <packet>/composition_probe.py
<packet>/scratch/venv/bin/python <packet>/run_gates.py <candidate>
python3 <packet>/run_receipt.py --repo <candidate> --name audit -- python3 <packet>/collect_audit.py
python3 <packet>/run_receipt.py --repo <candidate> --name integrity -- python3 <packet>/integrity_probe.py
```

The candidate environment also needs PyYAML. The original environment already
provided it; only the locked Markdown packages were installed into scratch.
run_gates.py joins six concurrent foreground commands, each with its own log,
exit code and command receipt. It runs no compilation bank or container.
run_receipt.py places temporary files under scratch and disables bytecode writes.
Raw logs preserve command output. Publication-only path normalization, if any,
is recorded with before/after hashes in publication-normalization.json.

fetch_public.py retrieves scope and eight selected historical executable
receipts, verifying their published SHA-256 values. fetch_prior_reviews.py
requires an independently written verdict and ledger before retrieving the four
prior public reviews and checking submitted-review/inline-comment endpoints.
Those read-only commands require authenticated public repository access.

The first composition probe had a reviewer assertion error: it tested the known
shared document as though it were outside the overlap. composition_initial.log
retains that failure. The corrected probe explicitly excludes that document
from the equality-only assertion and separately proves its raw three-way merge.
No candidate source was changed to obtain a pass.

Only MANIFEST.sha256 entries and REPORT.md are publishable. Scratch is excluded.
