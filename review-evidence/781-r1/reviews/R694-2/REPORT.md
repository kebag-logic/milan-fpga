[R694] POSITIVE - exact head 41f4a53cc0b12f143fa3e61a5339a11e79806ce9

Independent external review, R694-2, issue #781 / PR #782.
Tree: 51524679ffb3046c28887b4c112fd1bf5a6ddfe4.

Base: a032c6d6e3775f145349d5a495c1e1ad12294936.
Prior head: 8a4fa2f971427b1deb1f20a4b456a8a4d94bf008.

The independent verdict and ledger were written before reading any other review report. Prior public findings were subsequently reconciled against their causes. No private author narrative or current-round report from another reviewer was read.

The round-two delta meets the published calibration decision. The hosted job succeeds, its artifact digest matches, and the timestamped log measures media_phase at 582 seconds. The 1400-second execution deadline and estimate remain unchanged; the provisional set is empty. No blocking or minor defect was found in the delta.

This is a source-review verdict, not hosted acceptance or merge authorization. One optional test improvement and one PR-body wording residue are recorded below. All five lenses are CLEAN.

The review reconstructed AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue and public decisions, REQUIREMENTS.md's verification clauses, and scheduling/runner authorities before reading the complete seven-file base-to-head diff and the three-file round-two delta.

**Calibration and source binding.** The [ruling](https://github.com/kebag-logic/milan-fpga/issues/781#issuecomment-6388150329) and [round-two assignment](https://github.com/kebag-logic/milan-fpga/pull/782#issuecomment-6390031279) require a measurement within the supplied 1272-second threshold, removal of provisional status, and retention of 1400 seconds.

- [Hosted job 120983200812](https://github.com/kebag-logic/milan-fpga/actions/runs/40131149135/job/120983200812), Verilator shard 4/17, concluded success. Its suite step ran 2026-10-24T20:50:36Z to 21:01:31Z: 655 seconds including preflight and all four suites.
- The raw log places the preceding fw_service_budget PASS at 20:51:49.9660890Z and media_phase PASS at 21:01:31.7124752Z. Their interval is 581.7463862 seconds, rounded upward to 582 by the unchanged measurement parser. hosted-measurement.log reproduces it. Raw API logs lack the two tab-separated presentation fields expected from the command-line log view; the preserved prefixed copy adds those fields without changing timestamps or messages.
- The suite-logs-4 ZIP has SHA-256 2d5ad7de5d50bd681322f677a8d18004019061061ca2ddb9f5ace68630efa3e2, matching GitHub's artifact digest. Its media_phase.log contains 28 PASS result blocks and 386 checks. The job reports four passed suites, zero failed and zero timed out.
- Artifact TARGET_SHA is e9df8b0a1f7cd46625531dcd0e2ab5eb5d831fad. Its parents are the recorded base and prior source head; its tree is 57cbe969ebfcd88b476edc9408446c13e299a01d, identical to 8a4fa2f9. This measures that tree, not an execution at 41f4a53c.
- Both 582 and the conservative 655-second whole-step upper bound are below 1272. The rounded suite figure leaves 818 seconds, 58.4% of the 1400-second budget. This commit changes no suite inputs, cases, deadline or assignment, so that measurement remains applicable.

The cancellation was external to suite execution, rather than an initiating test failure. The precise timeline starts earlier than the assignment's shorthand: rtl-fast job 120983101989 reports “The operation was canceled” at 21:15:35.8779939Z. Its watcher, job 120982936824, detects yosys-elaboration as cancelled at 21:16:50Z and reports cancelling runs 40131149135 and 40131149068 at 21:16:51Z. The exhaustive run's watcher, job 120982936960, is itself cancelled at 21:17:22Z; its cancellation step is skipped. The interrupted workers and subsequent union/aggregate failures do not establish test failures, nor do they constitute a successful full run. The logs establish the cancellation chain, not the initial cancelling actor's identity or reason.

**Independent lens results.**

[R694] PASS Conformance - scripts/suite_shards.py:71-76,116,143-147; scripts/run_all_suites.sh:249-258; CI_WORKFLOWS.md:438 - The measured registration, empty provisional set and retained 1400-second values meet the decision. REQUIREMENTS.md:307-315 remains the verification authority; no protocol or product-interface requirement changes. The PR body contains Closes #781.

[R694] PASS RTL - complete a032c6d6..41f4a53c diff; rtl.yml:139-168; measure_test_evidence.py:661-680; tree-verification.json - No hdl/, tb/ or dependency gitlink changes exist. The prior product architecture verdict carries forward. The round-two change leaves ownership, continuous-history isolation, specialized installs and deadlines unchanged. Clock, reset, CDC, FSM and wire contracts acquire no new dependency from this delta.

[R694] PASS Robustness - suite_shards.py:383-400,810-904; suite-shards-selftest.log; focused_probes.py - Empty provisional status changes the message without bypassing synthetic controls. Disabling the provisional comparison is independently caught. Syntax, missing/extra duration, deterministic selection, specialized ownership and bound controls pass. Regular loads remain 1537-1605 seconds against 1620; worker 4 is 1539/1620 and dedicated worker 16 is 2032/2160.

[R694] PASS Tests - ownership-verification.json; ci-events.log; ci-gate-workflows.log; published round-two gates and mutants - All 19 listings (serial, expanded and seventeen workers) are byte-identical between the prior and current heads. There are 64 serial suites, 81 expanded units and exactly one owner per unit. media_phase remains on worker 4 and continuous media-clock history alone on worker 16. The generator check passes; the event contract passes 2199 items. The selector self-test and timeout contract pass independently.

[R694] PASS Docs - CI_WORKFLOWS.md:438,2930-2952; suite_shards.py:63-76,143-147; run_all_suites.sh:249-251; docs-command-binding.json - Measurement, retained budget and non-provisional load description agree with evidence. All seventeen documented loads, bounds and margins match independent selector output. New source comments contain behavior/reason and issue references, with no lane labels, reviewer IDs, review rounds or comment IDs.

**Gate evidence and provenance.** The fixed [public evidence commit](https://github.com/kebag-logic/milan-fpga/tree/f9c239222d78ce52a9e8b067b76fb8d2e74ec3a3/review-evidence/781-r1) supplies author receipts. Eighty round-two receipt/script files were checked against its publication manifest; four earlier sweep summaries were checked separately. SHA-256 verification establishes equality with that pinned publication. GitHub reports the evidence commit as unsigned, so no cryptographic signature verification is claimed.

The inspected author receipts at 41f4a53c record lint PASS at 89/89 and behave 14 features, 406 scenarios and 1977 steps passed, with no failed or skipped behavior scenarios. The docs receipt identifies the same head before and after execution: 42 successful workflow commands under GNU Make 4.3. Every recorded command digest matches the current workflow command. Two excluded entries are explicitly accounted for: the local runner contract has a separate PASS receipt, and both no-git gates have separate successful receipts. The separate builder leg and five markdown-gate receipts also pass. These are inspected author source-head receipts, not reviewer reruns or a manager source bank. The local orchestration self-test was not executed here.

All eight published mutation controls report the expected refusal: disabled provisional comparison, 582 while provisional, misspelt provisional name, driver restored to 900, stale sixteen-entry overhead, regenerated sixteen-worker schedule, stale long-timeout index and a 1499-second figure. Their reproduction script was examined. Independent disposable probes spot-checked the disabled comparison and documented measured-582 escape; both reproduced with head-dependent self-test arms active.

The four-shard author sweep at 6f7b70ed totals 64/64 suites and 2,189,253 checks, with no failed/timed-out suites. Its field-generator and freshness skips remain skips, contributing no executed field evidence. No full parent, processor, synthesis or builder bank was rerun here.

**Reviewer-owned coverage ledger.** Each row covers this exact head. Prior results were retained only where the delta leaves their artifacts and dependencies unchanged.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #781 decisions 6388150329 and PR assignment 6390031279; REQUIREMENTS.md:307-315; scripts/suite_shards.py:71,116,147; hosted job 120983200812 and artifact 12576025045 | R694-2 | 41f4a53cc0b12f143fa3e61a5339a11e79806ce9 |
| RTL | CLEAN | Complete a032c6d6..41f4a53c seven-file diff; unchanged hdl/, tb/, gitlinks; scripts/run_all_suites.sh:252; .github/workflows/rtl.yml:139; tree-verification.json | R694-2 | 41f4a53cc0b12f143fa3e61a5339a11e79806ce9 |
| Robustness | CLEAN | scripts/suite_shards.py:383,810,839; suite-shards-selftest.log; disabled-provisional-guard.log; measured-582.log; ownership-verification.json | R694-2 | 41f4a53cc0b12f143fa3e61a5339a11e79806ce9 |
| Tests | CLEAN | Published author-r2/receipts/round2/head-41f4a53c gates and mutants/mutants.txt; focused_probes.py; ci-events.log; ci-gate-workflows.log | R694-2 | 41f4a53cc0b12f143fa3e61a5339a11e79806ce9 |
| Docs | CLEAN | docs/testing/CI_WORKFLOWS.md:438,2949; scripts/suite_shards.py:63-76,143-147; scripts/run_all_suites.sh:249-251; public scope and published docs receipts | R694-2 | 41f4a53cc0b12f143fa3e61a5339a11e79806ce9 |

**R694-2-S1 | SUGGESTION | Conformance, Robustness, Tests | scripts/suite_shards.py:116,383-400; scripts/measure_test_evidence.py:661-680.**

- Authority/evidence: the assignment deliberately retains 1400 despite the 582-second measurement; focused_probes.py reproduces a substituted measured estimate passing the selector self-test. The timeout contract independently retains 1400.
- Impact: no defect at this head. Measured scheduling estimates ordinarily differ from deadlines, and all current loads use the required 1400. A future edit could discard this deliberate allowance without a policy-specific diagnostic.
- Required outcome: optional; consider separately checking the retained #781 estimate or representing conservative overrides. Requiring all measured estimates to equal execution timeouts would contradict their existing purpose.
- Verification: if adopted, a 582-second replacement must fail the override control while ordinary measured estimates remain valid.

**R694-2-R1 | RESIDUE | Docs | PR #782 body, Linked Issue / roles, lines 28-29 in pr-body.txt.**

- Authority/evidence: public review-start comments name both reviewers; the body still says both are to be assigned.
- Impact: stale prose only. Public assignments and evidence are unambiguous; no measurement, gate, source behavior or conformance claim changes.
- Required outcome: replace “Internal cleared-context reviewer: [R<n>] (to be assigned)” with “Internal cleared-context reviewer: [R693]”, and the external counterpart with “[R694]”.
- Verification: compare the revised body with the public review-start comments. This residue does not affect CLEAN coverage.

**Prior finding reconciliation.** The [R694-1 review](https://github.com/kebag-logic/milan-fpga/pull/782#issuecomment-6389406209) and [R693-1 review](https://github.com/kebag-logic/milan-fpga/pull/782#issuecomment-6389637033) were read only after the independent verdict/ledger was written. The API returned no submitted review objects or inline threads requiring additional reconciliation.

- R694-1-F1 | MAJOR | Conformance, Robustness, Tests | suite_shards.py:116,147; CI_WORKFLOWS.md:438; job 120983200812. **RESOLVED.** Its cause was missing completed hosted calibration and the follow-up registration. The bound log, artifact, recomputed margin and delta provide the required outcome. Bounds, ownership, generator and timeout-contract checks pass. These three lenses are now clean.
- R693-1-S1 | SUGGESTION | Tests, Docs | CI_WORKFLOWS.md:1365,2930-2946. **RETAINED OPTIONAL.** Earlier planted prose/table errors escaped gates; current values independently match. Impact is future documentation drift. Optional outcome remains generating or checking those values; verification remains rejection of the two prose mutants.
- R693-1-S2 | SUGGESTION | Robustness, Tests | suite_shards.py:155; rtl.yml:147-168. **RETAINED OPTIONAL.** The prior eighteen-worker mutation was accepted; the current schedule has the authorized seventeen. Impact is possible future excess allocation, not current correctness. Optional outcome remains a count-policy check or explicit flexibility; verify the eighteen-worker control against that policy.
- R693-1-S3 | SUGGESTION | Conformance, Docs | suite_shards.py:71-76,116; CI_WORKFLOWS.md:438. **CONSERVATIVE-BUDGET OUTCOME MET; OPTIONAL WORDING/REMEASUREMENT RETAINED.** Both 1400-second values remain. Public comparisons in earlier-hosted-inputs.json confirm queued heads changed suite inputs; 582 seconds measures this prior source-head tree. tb/verilator/media_phase/Makefile:50-55 includes the affected RTL. Impact is overgeneralizing one timing sample across changed inputs. Optional outcome remains explicitly distinguishing samples and remeasuring after queued changes merge; verify source-bound receipts and wording.
- R693-1-S4 | SUGGESTION | Docs | CI_WORKFLOWS.md:369,438. **RETAINED OPTIONAL.** The PR links the #781 ruling; the central policy still cites the issue without its decision link. Impact is navigation effort only. Optional outcome remains adding that link; verify link health.

No prior suggestion becomes a blocking requirement, and no unresolved defect is moved to another issue to obtain coverage.

**Real limits and pending manager duties.** At the final hosted snapshot (2026-10-24 22:52:21 UTC), exact-head run 40139678015 had successful full-ci selection and compiler preparation, with shard 4/17 job 121008732969 still in progress and other workers running/queued. No failed test was reported in that snapshot. The nightly physical job was skipped. The docs, elaborate and rtl-fast workflows were also incomplete. No new-head media_phase PASS, successful exhaustive aggregate or complete protected-context acceptance is claimed.

The manager must finish exact-head hosted/local acceptance, including media_phase, all worker/union evidence and required contexts; obtain the remaining independent review and ensure no review is in flight; validate and publish the current-dev merge candidate's native and builder banks; then follow explicit merge authorization, containment and issue/project closure. Source validation is distinct from that candidate. **No manager source-head bank exists or is inferred.**

Physical calibration: **NOT RUN**. Desk gates and field skips provide no hardware proof. The deferred pre-existing piece-estimate observation remains outside this change under the public ruling.

No source fixes, commits, pushes, GitHub writes, author contact, sub-agent calls, host orchestration or hardware operations were performed. Probes used only a disposable clone under this packet's scratch directory. Direct verification checked 1441 superproject blobs, modes and index entries, plus 703 protocol-processor, 107 gptp-processor, 214 verilog-axis and 98 tsn-c-stack blobs against required gitlinks. The isolated source clone remains clean at the exact head/tree. Only MANIFEST.sha256-listed files and this report are publication inputs; scratch is excluded.

R694-2 FINISHED
