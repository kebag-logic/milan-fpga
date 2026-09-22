R219-3 factual receipt index

REPORT.md is the publication payload. The root GitHub JSON snapshots and their
`.receipt.json` files preserve read-only API commands, capture times and exit
statuses. `comment-*.md` files contain extracted public PR comment bodies.
No private author/reviewer event stream or lane prompt was read.

Reproduction from the isolated exact-head clone:

```sh
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/505-r3-r219/run_gates.py
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/505-r3-r219/probe_review.py
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/505-r3-r219/audit_integrity.py
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/505-r3-r219/fetch_evidence.py
```

- `gates/`: exact focused command receipts, complete stdout and stderr.
- `round3-diff.txt`, `whole-pr-diff.txt`, `head-history.txt`: Git evidence.
- `scope-identity.json`: parent/base/tree identity, complete change scope and
  critical blob/mode comparisons at base, first head, prior head and this head.
- `arm-population.json`: unchanged labels, reasons and mutated workflow payloads
  for all 1046 arms; 56 bodies and 173 line-swallowing controls.
- `f1-f2-focused.json`: exact refusal diagnostics for the three shape-gate
  proof-flag edits and the non-last AC5 call edit.
- `f3-disclosed-gap.json`: ten accepted SHA-pin-script mutations in memory,
  confirming the gap remains and the corrected paragraph discloses it.
- `historical-executable-identity.json`: checker AST comparison excluding
  docstrings, plus workflow and trusted-runner blob equality.
- `ac5-native-diagnostic-comparison.json`: actual checker CLI invocations on
  minimal temporary copies at three revisions, with the historical AC5 edit;
  exit 1 and byte-identical complete stdout. Temporary copies were removed.
- `public-evidence/`: downloaded public manager and historical AC5 artifacts.
  `public-evidence-downloads.json` records immutable archive and verified Git
  blob IDs. These are attributed executions, not reviewer executions.
- `historical-ac5-verifier.json`: inspected published receipt checker command,
  successful exit and stdout. Its input includes the normal historical docs log.
- `check-runs.json`, `workflow-runs.json`: hosted state at this exact head.
- `final-public-*.json`, `final-live-dev.json`: final public identity/status.
- `initial-*`, `final-integrity.json`: initial index/tree/status and final direct
  file hashing, modes, flags, complete cleanliness and submodule state.

Reviewer tooling note: an initial probe helper invocation stopped while JSON
sorting PyYAML's mixed boolean/string mapping keys. Only the external helper's
serialization was corrected. The complete subsequent probe passed. This was
not a candidate failure, and no initial failed helper result is called a pass.

No act/Docker command, builder/RTL sweep, compilation or submodule initialization
is part of these reproduction scripts. The probe imports only the CI checker
and executes its checking paths; it never runs workflow scripts. All scripts
use `-B` for candidate Python invocations and `rtk` for subprocess commands.
