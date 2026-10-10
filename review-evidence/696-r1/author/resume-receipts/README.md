# Resume evidence

Source head: `bb1940966115e61733147b538182a6bccc3f4597`.
Status: scope STOP, not review ready.

The MAAP default target, coverage, lint and static gates pass.
`behave.log` reports 404 passing scenarios.
`differential-current.log` records the required clean-control failure.
`differential-resume.log` reproduces it with the incoming RTL.
`differential-base.log` passes with only the base MAAP RTL substituted.
All other differential inputs remain unchanged in those comparisons.
`reproduce_differential.py` repeats that attribution with two compiler workers.
`reproducer.log` and `reproducer-results.json` verify those expected outcomes.
The reproducer returns zero for successful attribution; the current differential
still returns one and remains a failing required gate.
The original discovery log is kept separately as `differential.log`.

The synthesis job was cancelled while waiting for the Vivado lock.
No new area report, route result or resource record is claimed.
The broader firmware bank was cancelled without a completed verdict.

`coverage.log` used the system reader. `coverage-pinned-final.log` repeats
annotation with the matching reader from the correct source directory.
The earlier `coverage-pinned.log` records its wrong-working-directory refusal.
Both successful annotations report 216/216 covered RTL lines.
`em-dash-head.log` checks the committed Markdown delta.

Host path prefixes in these receipts are replaced with neutral placeholders.
`PROVENANCE.json` records raw and delivered sizes and hashes separately.
The root `MANIFEST.sha256` always hashes delivered bytes after redaction.
Large artifacts and source exports remain outside this packet.
`SCRATCH-ARTIFACTS.json` records their sizes and hashes only.
Prior `fresh-receipts` belong to the previous head and are historical.
