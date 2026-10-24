[R694] NEGATIVE - exact head 8a4fa2f971427b1deb1f20a4b456a8a4d94bf008

External independent review, round R694-1, issue #781 / PR #782.
Reviewed tree: `57cbe969ebfcd88b476edc9408446c13e299a01d`.
Base: `a032c6d6e3775f145349d5a495c1e1ad12294936`.

The authorized provisional implementation passes the focused source checks. No source-code defect was found in the seven-file delta. This verdict is negative because the required hosted calibration and its follow-up commit are not present at this head. It is not evidence that 1400 seconds has failed: that outcome remains unknown. The staged public ruling expressly anticipates this remaining work, but it does not waive the issue's final acceptance criteria.

All five lenses were independently applied. No other review report informed this verdict or the ledger below. No source fixes, commits, pushes, GitHub writes, full banks, host orchestration, or hardware operations were performed.

## Finding

**R694-1-F1 | MAJOR | Conformance, Robustness, Tests | `scripts/suite_shards.py:112`, `scripts/suite_shards.py:142`, `docs/testing/CI_WORKFLOWS.md:438`; hosted job 120983200812 | Required hosted calibration remains unproved.**

- Authority/evidence: [issue #781](https://github.com/kebag-logic/milan-fpga/issues/781) requires measuring this PR's hosted run, recording the figure and removing the provisional designation. The [public ruling](https://github.com/kebag-logic/milan-fpga/issues/781#issuecomment-6388150329) authorizes 1400 seconds provisionally and requires a follow-up only when the measured window is at most 1272 seconds under the supplied acceptance threshold. The current tree correctly retains `media_phase` as provisional. [Run 40131149135, shard 4/17, job 120983200812](https://github.com/kebag-logic/milan-fpga/actions/runs/40131149135/job/120983200812) was still building its compiler dependency at the initial inspection. Fetching its log returned `BlobNotFound` at 2026-10-24T20:49:45Z. At the final inspection its exhaustive-suite step had started, but the job remained in progress with no conclusion or completed window. The final run/job API records both bind `head_sha` to the reviewed head. See `public-state/media-log-attempt.json`, `public-state/final-hosted-run.json` and `public-state/final-media-job.json`.
- Impact: local completion and estimated scheduling loads cannot establish that the hosted timeout defect is fixed with the required margin. The current source still lacks the issue's required measured registration. Approval of issue completion would turn a projection into accepted timing evidence.
- Required outcome: complete this PR's own hosted shard, preserve the suite start/end timestamps, result, job/run identifiers and source binding, and evaluate the whole default target's wall clock against 1272 seconds. If it fits, publish the measured figure and remove the provisional designation in the planned follow-up commit. If it does not fit, retain the provisional status and seek the public ruling required by #781. Do not change predicates or omit cases to obtain a fit.
- Verification: independently read the completed hosted log/receipt; recompute the suite window and margin; review the follow-up diff; rerun shard bounds, ownership, generation and timeout-contract checks at that head. The final current-dev candidate remains a separate validation obligation.

No RESIDUE or SUGGESTION finding is raised. Existing piece-estimate underprediction for `milan_dp__3` and `pp_shadow__3` is explicitly assigned outside this change by the public ruling; this review does not claim to resolve it or treat its estimates as measured current-head timing.

## Independent results

**Conformance.** `scripts/suite_shards.py:112-149`, `scripts/run_all_suites.sh:249-261`, `scripts/measure_test_evidence.py:661-680`, and `.github/workflows/rtl.yml:141-168,620,1580` implement ruling (b): 1400 seconds on both scheduling and execution sides, the contract mirror updated, 17 overhead entries, and provisional status retained. The workflow is byte-for-byte reproducible by the unchanged generator: `ci_gate_workflows.py --check` passes. `ci_suite_workflows.py:95-128` derives the matrix size, final-worker timeout index and aggregate expectation from the overhead population. The generated matrix contains 0..16, total 17, the 60-minute exception at 16, `--expect 17`, and both fail-fast lists contain all 17 names. `ci_events.py --check` passes 2199 contract items. F1 prevents clean completion coverage.

**[R694] PASS RTL - `checks/workflow.diff`, `checks/integrity.log`, `docs/overview/ARCHITECTURE.md:76-99`, `tb/verilator/media_phase/Makefile:91-97` - Product architecture and test histories remain unchanged.** The complete base-to-head diff contains three Python/shell scheduling-contract files, one generated workflow and three documentation pages. Direct tree comparison proves no delta in `hdl/`, `tb/` or any dependency gitlink. Clock/reset/CDC, wire fields, FSMs, port contracts, and the carried media-clock history are not altered. The default media-phase target still runs pins, render, blend, offsets, detector and all thirteen loop cases. The dedicated continuous history remains alone on worker 16. Independent lint using verified version 5.050 passes at 89 violations against ratchet 89; the existing warnings are not claimed to be absent.

**Robustness.** `scripts/suite_shards.py:247-432,705-896` was checked for deterministic placement, distinct regular/exception bounds, the fixed specialized owners, invalid shard syntax, missing/extra durations and provisional-budget mismatch. `checks/suite-shards.log` passes its boundary and negative controls. `checks/mutants-summary.txt` reproduces all eight published mutations at this exact head: overhead left at 16, regenerated 16-worker schedule, either 900-second value retained, stale special timeout index, stale aggregate expectation, stale matrix total, and a 1499-second budget. All are caught with the expected diagnostic, and clean controls pass. The actual hosted timing tolerance remains F1.

**Tests.** `ownership.py` invokes every `--ci-pieces --shard k/17 --list` and compares the collected ownership multiset with the independently requested full listing: 64 serial suites, 81 CI units, exactly one owner per unit. The run is preserved in `checks/ownership.log` and `ownership/`. The union controls use production readers and fresh driver inventories: `ci_suite_pieces_selftest.py` rejects omitted/duplicate legs, a case removed from every claimed inventory, altered source identities, and absent/failing logs. `ci_suite_collect_selftest.py` rejects an extra worker, wrong source head, missing owned log and forged/altered union evidence. Both pass. The timeout-contract evidence ratchet and all 105 self-test checks pass. Behavior tests pass 14 features, 406 scenarios and 1977 steps. F1 is the remaining empirical acceptance gap.

**[R694] PASS Docs - `docs/testing/CI_WORKFLOWS.md:350-438,1365,2930-2951`, `docs/testing/RUNNING_TESTS.md:84-94`, `docs/testing/TESTING.md:541-554`, public ruling and receipts - Counts, examples, budget and provisional limits agree with source.** All three pages state seventeen workers; the central policy carries the #781 derivation, provisional status and load table. The projection is identified as such. Added source comments state behavior/reason with issue IDs and introduce no bench labels, reviewer identities, review rounds or issue-comment IDs. Independent documentation checks pass: zero wording/link/privacy findings, all 1062 cited paths, added-line em-dash controls 339/339, contents self-tests 1501/1501 and contents consistency on 149 pages, audience style and feature-status consistency. The initially absent Markdown dependency was installed only in a disposable environment, after which both initially refused gates passed. Published full docs receipts were also checked separately from these focused reruns.

### Planned loads independently reproduced

All loads include the 122-second allowance. These are scheduling predictions, not this PR's measured hosted job durations.

| Worker | Load seconds | Bound seconds |
|---|---:|---:|
| 0 | 1605 | 1620 |
| 1 | 1541 | 1620 |
| 2 | 1572 | 1620 |
| 3 | 1538 | 1620 |
| 4, media_phase owner | 1539 | 1620 |
| 5 | 1538 | 1620 |
| 6 | 1539 | 1620 |
| 7 | 1539 | 1620 |
| 8 | 1540 | 1620 |
| 9 | 1541 | 1620 |
| 10 | 1537 | 1620 |
| 11 | 1540 | 1620 |
| 12 | 1539 | 1620 |
| 13 | 1537 | 1620 |
| 14 | 1537 | 1620 |
| 15 | 1538 | 1620 |
| 16, continuous media-clock history only | 2032 | 2160 |

## Reviewer-owned coverage ledger

Every row below records an applied lens at this head. UNCLEAN rows cannot be banked as clean coverage.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN, F1 | #781 body/ruling; timeout triplet; generated workflow; hosted shard 4/17 | R694-1, applied, no clean covering round | 8a4fa2f971427b1deb1f20a4b456a8a4d94bf008 |
| RTL | CLEAN | Complete seven-file diff; direct RTL/test/gitlink tree comparison; architecture clock boundaries; lint receipt | R694-1 | 8a4fa2f971427b1deb1f20a4b456a8a4d94bf008 |
| Robustness | UNCLEAN, F1 | Bounds and provisional parser; eight mutations; union rejection controls; hosted job state | R694-1, applied, no clean covering round | 8a4fa2f971427b1deb1f20a4b456a8a4d94bf008 |
| Tests | UNCLEAN, F1 | All 17 ownership listings; selector/evidence/union self-tests; behavior tests; public sweep receipts; unavailable hosted measurement | R694-1, applied, no clean covering round | 8a4fa2f971427b1deb1f20a4b456a8a4d94bf008 |
| Docs | CLEAN | Three changed testing pages; added source comments; PR scope; public author receipts; focused docs gate receipts | R694-1 | 8a4fa2f971427b1deb1f20a4b456a8a4d94bf008 |

## Evidence provenance and limits

Prior public findings were checked only after the independent diff pass and this verdict/ledger were written. At that check, PR #782 had no submitted reviews, no inline review threads and only the two public review-start comments. There are therefore no prior public findings to resolve or retain. See `public-state/prior-findings.json`.

The public author evidence was read at fixed commit [ac1cc4ef42596b879ee48404ff19167f812dad5c](https://github.com/kebag-logic/milan-fpga/tree/ac1cc4ef42596b879ee48404ff19167f812dad5c/review-evidence/781-r1). Only its public receipt files and executable reproduction scripts were extracted; private author material and handoff narratives were not read. Published receipt hashes are checked against the publication manifest.

The full sweep is author evidence at `6f7b70edfeed8a624c625ca7797fd468992259d2`: 64/64 suite summaries pass, 2,189,253 checks, zero failed/timed-out suites. The next commit changes one documentation line only. The shard-3 receipt explicitly declares four skipped field-campaign/freshness items because the field generator is absent. Those ran nothing and contributed zero checks; neither the suite summary nor this review converts them into executed field tests. The issue's no-weakening requirement is supported by unchanged suite sources and complete ownership, not by denying those recorded environmental skips.

Author docs receipts at the reviewed head record 42 successful workflow gate steps, a separate builder leg, five pinned-renderer gates and two no-git checks. The published local runner contract receipt reports PASS; it was inspected, not executed by this reviewer, and is not a hosted/local equivalence verdict. The independent reruns here are focused checks only. The full parent, processor, synthesis and builder banks were not rerun. No manager source-head bank exists or is inferred.

Hosted observations distinguish pending execution from success. The run had a successful full-ci selector, pending/running native workers, and an explicitly skipped nightly physical job. No exhaustive protected-context pass, full hosted acceptance or local replay acceptance is claimed. Physical calibration: **NOT RUN**. Field skips and desk simulation are not hardware proof.

`integrity.py` directly hashes every tracked blob, checks modes and index entries, and verifies initialized required submodules against the superproject gitlinks. The main checkout remains detached at the reviewed head/tree. Mutation probes run only in a disposable clone and restore its tracked source. No author checkout was edited.

## Pending manager duties

1. Complete and publish hosted/local acceptance evidence, including F1's measured suite window and the planned follow-up commit. Do not close #781 from this provisional head.
2. Obtain independent re-review of changed artifacts and a reviewer-accepted clean ledger after that commit. Coverage does not automatically carry across affected artifacts.
3. Validate the final merge candidate against live current dev with the required native and builder banks and publish its exact tree/receipts. Source validation is distinct from that candidate; no manager source bank is claimed here.
4. Complete the remaining protected checks, review and explicit merge authorization, then the documented post-merge containment and issue/project closure steps. This report is not merge authorization.

R694-1 FINISHED
