R254-1 focused reproduction. Python 3 and the repository's existing PyYAML are sufficient. No Verilator, Docker, act, installations, network calls or HDL banks are needed for the local probes. Supply the exact reviewed checkout and a fresh evidence directory. Preserve the archived receipts instead of overwriting them.

```sh
rtk proxy mkdir -p <new-evidence-dir>/receipts <new-evidence-dir>/disposable
rtk proxy python3 -B scripts/integrity.py <checkout> <new-evidence-dir>/receipts/initial-integrity.json
rtk proxy python3 -B scripts/review_probes.py <checkout> <new-evidence-dir>
rtk proxy python3 -B scripts/cli_controls.py <checkout> <new-evidence-dir>
rtk proxy python3 -B scripts/exact_base.py <checkout> <new-evidence-dir>
rtk proxy python3 -B scripts/disk_controls.py <checkout> <new-evidence-dir>
rtk proxy python3 -B scripts/malformed_controls.py <checkout> <new-evidence-dir>
rtk proxy python3 -B scripts/focused_gates.py <checkout> <new-evidence-dir>
rtk proxy python3 -B scripts/integrity.py <checkout> <new-evidence-dir>/receipts/final-integrity.json
rtk proxy python3 -B scripts/scope_preservation.py <checkout> <new-evidence-dir>/receipts/scope-preservation.json
rtk proxy git -C <checkout> diff --raw 483a133ed08867ea0d300d2b4a027b5b48a4282f f01f237d4b48c7b1ed59c80aca51430901791624
```

Run these commands from this evidence directory. Each script accepts explicit paths. Run them in the order shown; CLI and disk controls consume the independent inventory/base snapshot. `cli_controls.py` limits concurrency to four processes; other probes are serial. No workflow run body is executed. Expectations are in the portable scripts; exact subprocess argv, exit codes and raw streams are retained in receipts. The immutable public download helper uses read-only Git blob endpoints and verifies Git blob hashes; it never requests Actions, runs, checks or statuses. The public metadata snapshots use explicit fields only.

Archived *.original.py and *.second.py reproduce the review-tool failures described in FAILURES.md; use the unsuffixed scripts for corrected runs.
