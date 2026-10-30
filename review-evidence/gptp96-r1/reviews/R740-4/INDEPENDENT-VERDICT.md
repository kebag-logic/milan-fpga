[R740] NEGATIVE - exact head db9ab2215ba18aec4c1828090b3611b001dbf2b8

Independent verdict recorded before accessing PR comments or any other reviewer's report. Tree: df0a399476813ccfda8d3bb03fa9d7a272b5fd0c. Delta base: 411b35fcc56d11c2361d861e7205307587a04a1d; source base: 135afd04.

All five lenses have been applied independently. The delta contains three documentation pages and scripts/check_docs.py. No RTL, generator, test harness, build input, or nested gitlink changes. Prior public findings and manager PR evidence remain to be reconciled into the final report after this independent verdict.

## Finding R740-4-F1

- Severity: MINOR.
- Lenses: Conformance, Robustness, Tests, Docs.
- Location: scripts/check_docs.py:479-483, introduced by c6bca77.
- Authority: issue #96 single-source values and current-document accuracy; manager's round-4 ruling retains defects that let a real stale copy pass. Markdown fence semantics: https://spec.commonmark.org/0.31.2/#fenced-code-blocks.
- Evidence: receipts/fence-regression.json and the eight corresponding gate logs. A four-tilde fenced example containing a three-tilde line followed by visible prose falsely closes and then reopens the checker's fence state. The full production docs gate at this head accepts a planted current-page statement, "The Sync receipt timeout is 125 ms." The generator and constants table specify 375 ms. The preceding head rejects the identical modified page. Plain-prose and ordinary four-tilde controls reject at both heads. A matching-value restatement of 375 ms also escapes at this head.
- Impact: the changed checker silently excludes visible prose after a valid fenced example, allowing an actual wrong numeric statement and a restated protocol value to pass. No such false timeout statement is present in the submitted documentation; this is a demonstrated checker regression.
- Required outcome: preserve opening fence marker and length; close only on a valid matching closing fence. Add production-page regression coverage for a shorter same-character marker inside a longer fence, with a copy after the closing fence.
- Verification: fence_regression.py records old-head rejection and exact-head acceptance; review_checks.py records the ordinary stale-table, stale-duplicate-row and restated-value failures, the bypass, and restored controls. receipts/fence-case.html shows the statement as a paragraph outside the code block.

## Finding R740-4-R1

- Severity: RESIDUE.
- Lenses: Docs, Conformance.
- Location: saved PR body, receipts/pr-body.txt:55-62.
- Authority: manager ruling removes every prose statement of the gate's accepted or rejected forms, including the PR body.
- Evidence: the five-item list names rejected table forms and concludes that the production gate reports all five.
- Impact: remaining prose duplicates the executable rule specification; no measured value, clause, code or verdict changes.
- Exact fix: remove the five-item list and its explanatory paragraph; retain the single checker/self-test specification pointer. Make the PR body's self-test pointer an actual link to scripts/check_docs.py.
- Verification: inspect the refreshed body for absence of this enumeration and presence of the linked pointer.

## Reviewer-owned independent ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | Issue #96, parent #797, manager ruling, constants table, delta scope; F1 | R740-4 delta | db9ab2215ba18aec4c1828090b3611b001dbf2b8 |
| RTL | CLEAN | Unchanged hdl/, bench/, simulation/build inputs; publication assigns, source-anchor gate, contract and lint | R740-4 dependency check; prior behavior retained | db9ab2215ba18aec4c1828090b3611b001dbf2b8 |
| Robustness | UNCLEAN | Unit/minute patterns, fence state, actual-page positive/negative controls; F1 | R740-4 | db9ab2215ba18aec4c1828090b3611b001dbf2b8 |
| Tests | UNCLEAN | 53 checker arms, diagram/source self-tests, published 9 checker mutants and 25 probes, independent full-gate probes; F1 | R740-4 | db9ab2215ba18aec4c1828090b3611b001dbf2b8 |
| Docs | UNCLEAN | Three changed pages, all current-page gate references, PR body, table and prose probes; F1; R1 nonblocking | R740-4 | db9ab2215ba18aec4c1828090b3611b001dbf2b8 |

## Evidence and limits

Independent exact-head docs (including diagrams and source evidence), contract, pinned lint and both diff checks pass. The new self-tests pass; required ordinary stale table and copied-value probes fail as expected. All 60 published author-r4 receipts match the pinned publication manifest. Publication commit b71327c650cd5a941ebbb73e64695650a21861cb is reported unsigned by the public commit API; only content integrity is verified, not a cryptographic signature.

No manager source bank is claimed. Current-dev candidate integration, builder/native banks, hosted acceptance and physical calibration remain manager duties. No hardware or full simulation bank was run. The isolated source's 113 tracked blobs and modes match its index and HEAD; no nested submodule gitlinks exist. Disposable mutations were confined to packet/scratch and restored there.

R740-4 FINISHED
