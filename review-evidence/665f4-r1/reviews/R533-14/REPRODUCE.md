R533-14 reproduction

Use a detached checkout at `fe1cd0679f5028c749af7242c903a82ca2b3d692`.
Its tree must be `1452e3d48865f09739432b92608401371257dfb1`.
Run commands in the foreground. No command below invokes the replay runner.
No privilege, container, compiler bank or hardware operation is needed.

Set `review_root` to that checkout and `review_packet` to this packet directory.
Create disposable data only beneath `review_packet/scratch`.
Python, Git and the repository's existing YAML dependency are sufficient.

```sh
rtk proxy python3 "$review_packet/scripts/fetch_public_receipts.py"
rtk proxy python3 "$review_packet/scripts/audit_manifest.py" "$review_root" "$review_packet/scratch/probes"
rtk proxy python3 "$review_packet/scripts/audit_public_receipts.py"
rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 "$review_root/scripts/ci_events.py" --check --root "$review_root"
rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 "$review_root/scripts/ci_events.py" --selftest --root "$review_root"
rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 "$review_root/scripts/docs_check.py"
rtk proxy env PYTHONDONTWRITEBYTECODE=1 python3 "$review_root/scripts/check_doc_style.py"
rtk proxy python3 "$review_packet/scripts/verify_checkout.py" "$review_root"
```

Run the repository documentation commands from the checkout.
Capture each command's stdout/stderr and exit status separately.
All final executions above returned zero in this review.
The independent contract check and controls were started concurrently,
each as a foreground command, and both were awaited to completion.
The public-receipt fetch uses eight concurrent read-only requests.
No reviewed source, author helper, or candidate runner is imported by the audits.

The public source is fixed at evidence commit
`2276e34a9a7a615cdf65b4e6c026129680ede1f9`.
The fetch reads only public `author-r14` evidence and the publisher's manifest.
It verifies downloaded file content against the public Git blob identifiers.
The receipt audit checks original and redacted public hashes separately.
It also grades the eight published mutation assertions by name.
This is verification of published execution evidence, not a fresh runner execution.

The manifest audit constructs one inert text file from the trusted source
at `17f62ef64a66562384e8a93b1d6be6f86e51f95c` plus the approved tuple.
It never installs, imports or executes that file.
The manager owns the real installation and replay.

The checkout verifier hashes tracked bytes directly and checks file modes
and complete index records against commit trees.
It reports an empty uninitialized lwSRP checkout explicitly.
It verifies that gitlink in both the parent tree and index.
Initialized dependencies are verified recursively at their assigned pins.
The initial probe's stricter initialization assumption and two receipt-counter
assumptions are retained as failed-attempt receipts and explained in REPORT.md.

From this packet directory, verify publication integrity with:

```sh
rtk proxy sha256sum --check MANIFEST.sha256
```

Only the listed files and REPORT.md are publishable.
The scratch directory contains disposable downloaded data and inert probes.
