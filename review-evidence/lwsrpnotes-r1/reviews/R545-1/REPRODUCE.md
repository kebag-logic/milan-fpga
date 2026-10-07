Reproduce this focused review in an exact detached checkout of ced667d8ee35929ab5f9e77a1c5396e173a693d8.
Use a fresh packet directory containing these scripts. Put all generated dependencies, builds, mutations, and browser outputs beneath scratch/.
Required host programs are a C compiler, CMake, GNU Make, Python, behave, curl, tar, Git, the GitHub CLI, Mermaid CLI, and a compatible browser.
No global dependency installation is performed by these scripts.

```sh
mkdir -p receipts scratch
python3 scripts/record.py --name cgreen-bootstrap --cwd "$PWD" -- bash scripts/bootstrap-cgreen.sh
python3 scripts/run-tests.py /path/to/exact-checkout
python3 scripts/record.py --name reversal-audit-run --cwd /path/to/exact-checkout -- python3 "$PWD/scripts/audit-reversals.py" /path/to/exact-checkout
python3 scripts/record.py --name integrity --cwd /path/to/exact-checkout -- python3 "$PWD/scripts/verify-integrity.py" /path/to/exact-checkout
```

Before the documentation run, create scratch/puppeteer.json with executablePath pointing to your browser and the arguments required by your local environment.
The original run used a headless browser with sandboxing disabled inside the isolated review environment.

```sh
python3 scripts/run-docs.py /path/to/exact-checkout
```

The two normal builds share a 16-job make jobserver. Both original reversal drivers run concurrently and each uses two build workers.
No shell job is detached. Supervisors wait for all child commands and retain each command's log, return code, and duration.
Campaign directories must not exist before execution; use a new packet for a repeat run.
The driver is unmodified and does not accept --jobs.

The unit framework release, resolved commit, archive digest, and executable versions appear in receipts/environment.json.
Raw upstream campaign logs and command inventories appear under receipts/reversals/OFF and receipts/reversals/ON.
Expected mutation failures are recorded as nonzero command returns; a campaign returns zero only when all required detections and restoration succeed.
The 61 named-test mappings are independently checked against actual Failure records by audit-reversals.py.

Only REPORT.md and files listed by MANIFEST.sha256 are intended for publication.
The scratch directory includes builds, copied sources, the private-use standards extraction, and generated graph images. Never publish scratch.
The public evidence files are exact fetched bytes; their hashes were checked against the bundle's own manifest.
The other public API receipts retain the fields relevant to this review rather than account metadata.
The independent-verdict receipt is a historical checkpoint made before reading earlier findings; REPORT.md is the completed verdict.
