R236-1 independent review receipts for issue #464 / PR #513.

`REPORT.md` is the review deliverable. Its exact head is `a769d9dbc937fb324c4726e60dee5b2f7ad349e3`, tree `31ddc6b5615ff91ceed7a6b52afca61c5fb9653d`. The report contains the reviewer-owned ledger and ends `R236-1 FINISHED`.

Run the following from this receipt directory, substituting the isolated review checkout path. Commands write only here and in `scratch/`; integrity checks read the checkout. Required tools were already installed. No install is part of reproduction.

```sh
rtk proxy python3 integrity.py /path/to/review-checkout before
rtk proxy python3 prepare.py /path/to/review-checkout
rtk proxy python3 focused.py
rtk proxy python3 -B geometry_controls.py scratch/head
rtk proxy python3 supplemental_mutations.py
rtk proxy python3 -B ci_controls.py scratch/head
rtk proxy python3 store_cli_compare.py
rtk proxy python3 integrity.py /path/to/review-checkout after
```

`focused.py` requires existing `python3.14` and `python3.12` executables. It runs eight head/base/historical cases, two CI contract commands, two pristine mutation-fixture controls, and 40 interpreter/mutation combinations: 52 expected outcomes. One intended green is removal of Callable on Python 3.14; the same mutation fails on 3.12. Read the individual logs, not only exit status. The all-nine-guard checks have the named failure/exception evidence in those logs. `geometry_controls.py` adds 14 controls, `supplemental_mutations.py` adds eight causal controls, and `ci_controls.py` adds 13 carrier controls. These counts overlap in behavior and are not summed into product check coverage.

`prepare.py` restores exact archive snapshots and checks the complete original/current issue-delta equality and unchanged production AST/input trees. The store CLI script deliberately regenerates its default JSON only in scratch; this does not edit the review checkout or attempt to repair the tracked snapshot.

`fetch_evidence.py` downloads only the frozen public factual packet named by `evidence-tree.json`; it checks each Git blob identity. `public-download-integrity.json` covers all 204 downloaded files. `public-manifest-verification.json` records 203 matching published manifest entries; the outer manifest itself is the remaining Git-verified file. Original author receipts stay tagged to `1576f089`. `author-byte-manifest-verification.json` records the 83-file published comparison's measured scope. The full builder/native/processor bars were inspected as public evidence and were not rerun.

`capture_public_state.py` performs read-only GitHub reads and filters PR comments to manager `[A10]` statements before storing or displaying them. It does not fetch review bodies. Final captured hosted results and identities are in `hosted-*-final.json`, `pr-final.json`, `remote-dev-final.json`, and `public-state-time.json`. `hosted-docs-check.log` and `hosted-checkout-commit.json` prove the actual AEM self-test execution and equivalent hosted merge tree. This script may observe a later state when reproduced; the report explicitly dates its observation.

`integrity.py` hashes every tracked file directly, checks kinds/modes, compares index entries to committed trees, and verifies each required submodule pin/population. It disables Git replace-object substitution. `integrity-comparison.json` records full initial/final equality, including index file hashes and clean status. Optional historical external content is excluded by name, not counted as a populated dependency.

`standards-identities.json` identifies the primary PDFs and clauses read; copyrighted specification text is not republished. The public web search did not supply the normative conclusion; the local primary PDFs did.

The initial scratch mutation harness lacked `hdl/common/csr/milan_csr.sv`. Its FileNotFoundError outcomes are invalid, contribute no successful mutation evidence, and are retained only in `invalid-harness-missing-csr.json` and `invalid-harness-missing-csr-logs/`. The corrected script copies the dependency, requires pristine 20-arm passes on both interpreters before mutations, and explicitly rejects FileNotFoundError outcomes. The final counted receipts are `focused-results.json` and `focused-logs/`.

Publication: publish REPORT.md and these scripts/receipts with the permitted workstation-path neutralization. `scratch/` contains disposable source extracts and generated files; exclude it from publication. Invalid-harness records are explicitly non-evidence. Do not turn a manager start marker, an optional skip, the unavailable builder calibration arm, or this source-review verdict into a merge/gate pass. No private reasoning is included.
