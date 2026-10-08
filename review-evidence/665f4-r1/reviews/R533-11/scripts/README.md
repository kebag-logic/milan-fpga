Run from an isolated checkout of b98eb2d5a21522bab3bc6bb943332cf8edf11893 with the four required submodules initialized. Set PACKET to this packet directory. Use a Python environment with the repository's documented test and documentation dependencies.

```sh
python3 -B "$PACKET/scripts/validate.py" --jobs 4
python3 -B "$PACKET/scripts/replay.py" --jobs 4
python3 -B "$PACKET/scripts/evidence_audit.py"
python3 -B "$PACKET/scripts/doc_checks.py"
python3 -B "$PACKET/scripts/integrity.py"
```

Run the first two commands separately: each waits for three concurrent children, each capped at four build jobs. All builds and copies are placed in packet scratch. The validation command runs IF=1/2 focused suites, sanitizer controls, 19 feedback mutations per interface count, and the coverage checker. The replay command runs the unchanged public probes and four core mutations under AddressSanitizer. Mutation controls intentionally fail their named test; the drivers return success only when those failures match their oracles.

The evidence audit and probe import read commit 2f7ab26dadbd359c55eb248ef56fcbcbe4e6bd40, which must be available in the checkout's object database. They do not write to the remote. The audit checks archived receipts, not fresh image links or full banks. The docs command uses the interpreter selected by its caller, including the pinned Markdown dependencies when required. The integrity command hashes actual tracked bytes rather than relying only on status.

The optional diagnostic R10WithdrawalFeedbackCostFitsAllowance is present in the imported source for byte identity, but excluded from acceptance execution because its nonzero-cost assertion does not apply to an undiscovered withdrawal. The discovered-talker version is included unchanged.

Publish only REPORT.md and the files in MANIFEST.sha256. Do not publish scratch.
