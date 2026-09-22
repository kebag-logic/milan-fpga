Factual receipts for R219-2, PR505 / issue407.

Use an isolated checkout at ad62493186576144f9fa1568babad012bc9ad8ca with existing Python/PyYAML dependencies. The receipt scripts write only beside themselves, in temporary directories, or in memory. They do not run workflow shell bodies, act, builds, installs or privileged commands.

From the checkout, set R219_EVIDENCE to this receipt directory and run:

```sh
rtk proxy python3 -B "$R219_EVIDENCE/independent_probes.py"
rtk proxy python3 -B "$R219_EVIDENCE/cli_probes.py"
rtk proxy python3 -B "$R219_EVIDENCE/verify_integrity.py"
```

The checked review environment has all submodules uninitialized. The CLI script therefore expects the optional Python-idiom scan to refuse with exit 2. Run it in that same state to reproduce this receipt exactly. The first recorded attempt initially expected 0 and stopped at that setup refusal; the remaining focused probes were continued with `--mutants-only`. One subsequent harness assertion was narrowed from the whole file to the named function because `c.item(recorded, path,` occurs elsewhere too. These were review harness corrections, not candidate edits or product defects. The completed cli-results.json preserves the actual command results; the original Python-idiom row retains its initial expected value and actual exit 2. A fresh script invocation records the now-explicit expected refusal.

Main receipts:

- source-preservation.json: production/normalization/global-constant and workflow preservation against base and first-round head.
- inventory.json, line-swallowing.json, check-calls.json: independently enumerated live bodies and named per-line controls.
- mutation-population.json: all old mutation edits/reasons retained; specialized reasons tested with the new helper disabled.
- cli-results.json and corresponding logs: actual pristine, source-mutant, before/after, native AC5 and maintenance CLI runs. Temporary argv paths document original invocations; rerunning cli_probes.py recreates those fixtures.
- mutant-patches/: exact comparison/record-enforcement substitutions, each scoped to check_carrier_script.
- positive-controls.log: retained whitespace and record-update positives plus missing-record controls.
- final-integrity.json and tracked-blob-verification.json: raw parent blob/mode, index, HEAD, status and uninitialized submodule checks.
- public/: read-only GitHub API responses and selected immutable author/manager evidence. Reviewer archive files were excluded. Public first-round reports are the explicitly requested PR comment bodies.
- public-manifest-verification.json: published hashes verified; original hashes are not substituted for redacted published bytes.
- ac5-verifier.log: the inspected public AC5 verifier's successful run. This is receipt verification, not an act execution.

Public downloads can be reproduced with `rtk proxy python3 -B "$R219_EVIDENCE/fetch_public.py"`; it uses the captured immutable GitHub tree and verifies Git blob identities. To repeat only the supplied AC5 receipt verifier:

```sh
rtk proxy python3 -B "$R219_EVIDENCE/public/archive/ac5/verify_receipts.py" "$R219_EVIDENCE/public/archive"
```

All manager/author execution results remain attributed unless the report names an independent reproduction. Pending execution gates, draft-skipped exhaustive contexts, and missing physical calibration are not passes.
