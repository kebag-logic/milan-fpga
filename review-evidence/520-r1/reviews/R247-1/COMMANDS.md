R247-1 portable reproduction commands

Run from this evidence directory. Substitute a clean checkout at
28e350b99ac240a750326b762c6d029f0653362c for `<checkout>`, and fresh output
directories for `<new-output>`. Initialize the three required submodules
before reproduction. Native tools used here are in `tools.json`; the scripts
do not install tools, change source, or write a shared cache. Use at most eight
jobs. The scripts run focused native jobs serially; separate scripts can overlap.

```sh
rtk proxy python3 verify_integrity.py <checkout> initial-integrity.json
rtk proxy python3 run_command.py <checkout> unit -- python3 syn/yosys/result_cache.py --selftest
rtk proxy python3 run_command.py <checkout> live-bank -- python3 syn/yosys/cache_selftest.py --logs <new-output>
rtk proxy python3 independent_controls.py <checkout> <new-output>
rtk proxy python3 independent_driver_controls.py <checkout> <new-output>
rtk proxy python3 independent_pp.py <checkout> <new-output>
rtk proxy python3 preserved_contracts.py <checkout>
rtk proxy python3 audit_public_evidence.py
rtk proxy python3 verify_integrity.py <checkout> final-integrity.json
```

`independent_pp.py` runs three live full-mode syntheses of just KL_pp_shadow:
baseline, changed generated ucode.hex, and the same changed input uncached.
It also checks baseline warm, seed, changed warm, and one deliberately
defective frozen-digest control. Only the labelled fault control freezes the
ROM digest. The unchanged source must miss on the changed input and match
uncached results. The original generators execute; injection changes only
their disposable output. No generator or driver source is edited.

`independent_controls.py` uses its own byte framing and canonical-key oracle,
CLI record/stat controls, and seven disposable result_cache.py mutants. Each
mutant's expected nonzero selftest is recorded separately. These are tests of
defect detection, not passing source variants.

`independent_driver_controls.py` exercises read-only seeds in both modes,
using two actual small tops and real sv2v/Yosys. Invalid generation and digest
failures must stop before lookup; bad records must synthesize live. It retains
the live stat JSON, exact arguments, result records and raw output.

Every `*.receipt.json` records actual argv, source head, working directory,
exit and elapsed time; matching stdout/stderr are raw. Per-run receipts and
artifacts are inside the three independent probe directories and `live-bank/`.
Elapsed times describe these executions and do not establish a performance claim.

Additional completed focused commands, with receipts `focused-1` through
`focused-7`, in order:

```sh
rtk proxy bash -n syn/yosys/run.sh
rtk proxy python3 scripts/check_py_idiom.py
rtk proxy python3 scripts/check_sh_idiom.py
rtk proxy python3 scripts/docs_check.py
rtk proxy python3 scripts/ci_events.py --check
rtk proxy python3 scripts/check_em_dash.py --base 483a133ed08867ea0d300d2b4a027b5b48a4282f
rtk proxy git diff --check 483a133ed08867ea0d300d2b4a027b5b48a4282f HEAD
```

Public retrieval uses GitHub issue/PR metadata with explicit fields and Git
tree/blob APIs. `fetch_evidence.py`, `public-tree.json`, `triage-tree.json`,
and `public-download-receipts.json` describe the immutable selected downloads.
`audit_public_evidence.py` checks the published manifest and independently
reads public PP stat/ROM data and manager source-bank receipts. Publication
redacted some source paths: published staged-Verilog hashes are distinct from
recorded original hashes, as declared in MANIFEST.json. The audit preserves
that distinction. No Actions, checks, runs, or statusCheckRollup API was read.
