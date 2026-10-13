[R633] POSITIVE - exact head 73b8dcd667aa5bf1254e828dd1dd7217c8a103ce

R633-6, external independent review of issue #730 / PR #731. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains confirmed at this head. One wording-only RESIDUE is recorded below. This is a source-review verdict; merge, hosted acceptance and deferred measurements remain manager duties.

Tree: `73657b81c74af58dde382e4f9ce49d5a0e9e80bc`. Reviewed the full `dc4d06cb..73b8dcd6` diff and history, including the `ede700b0..73b8dcd6` correction. Only `scripts/act_ci.py` and `docs/testing/CI_WORKFLOWS.md` change. Workflow files, HDL, interfaces, firmware and gitlinks do not change.

The authorities are AGENTS.md sections 6-7, CONTRIBUTING.md sections 2-3, docs/README.md, REQUIREMENTS.md section 8, the CI policy and architecture/submodule boundaries, the [frozen issue](https://github.com/kebag-logic/milan-fpga/issues/730), [assignment](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131408752), [disk ruling](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815), and public round decisions. The [round-6 decision](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6137869227) settles the preceding reviewers' disagreement about closing-window precedence. It requires preserving the active failure and restoring the hold. No private author material or other checkout was inspected. The full independent diff pass preceded prior findings; [the initial independent verdict and ledger](independent-verdict.md) were written before reading another reviewer's report. The [final public inventory](receipts/public-findings-inventory.json) found no additional submitted or inline review findings.

[R633] PASS Conformance - `scripts/act_ci.py:2090`, `:2119`, `:4671`, `:4719`, `:5313`, `:5918`; shipping workflow files and #730 acceptance 1-3. Concurrency comes from the materialized workflows: the maximum, across selected workflows, of the widest `CONCURRENT_JOB_LIMIT` jobs. The shipping result is 4 for `rtl-full`, 1 for each other workflow. Unreadable matrix widths and widths beyond the slot capacity refuse. Slot N's 20-CPU block contains staging and four disjoint four-wide job ranges; insufficient capacity refuses on slot 0 too. The ownership label, memory/swap limits, concurrent-job limit and slot cap are retained. The default width and scheduling interpretation match the [pinned scheduler](https://github.com/nektos/act/blob/v0.2.89/pkg/runner/runner.go) and [matrix-width definition](https://github.com/nektos/act/blob/v0.2.89/pkg/model/workflow.go#L219). Four-wide configuration supports the intended `nproc` shape; live `nproc` and same-head verdict equivalence were not measured.

[R633] PASS RTL - [full.diff](full.diff); `scripts/act_ci.py:5380`, `:5487`, `:5525`, `:5574`, `:5610`, `:5675`, `:5818`; architecture section 7 and submodule map. The hardware-specific angles are inapplicable to the unchanged hardware artifacts. The architecture review examined the allocator's single-writer state, reservation-before-update, restart persistence, destroy/absence release, event ownership, command context, stream process group and reader-to-main handoff. Neither delayed updates nor `die` make a reserved range free. The real boundary retains pre/post integrity checks and the immediate pre-spawn lease gate. Stream containment and the reader's completion precede outer resource teardown. Worker starts inherit the cleanup mask; the normal execution window reopens signals and restores the hold.

[R633] PASS Robustness - `scripts/act_ci.py:5313`, `:5675`, `:7502`, `:7591`, `:7947`, `:8120`, `:8334`, `:12469`; [lifecycle](receipts/r633-r2-lifecycle.log), [monitor](receipts/r633-r2-monitor.log), [shutdown](receipts/r632-r2-shutdown.log), [cleanup-entry](receipts/cleanup-entry.log) and [first-restore](receipts/first-restore.log) receipts. Restart, uncertain/applied/lost updates, duplicate/delayed/foreign events, insufficient CPUs, reader startup failure, polling failure, failed reap/join and containment hold retain their required behavior. A body failure retains identity and diagnostic beside cleanup errors; signal-only cases retain conventional status. The new closing guard preserves the earlier Refusal for INT, TERM and HUP arriving with all three signals unblocked at line 5357, then completes containment, reader completion and pipe closure.

[R633] PASS Tests - `scripts/act_ci.py:6589`, `:7171`, `:7268`, `:7857`, `:8334`, `:12415`, `:12570`, `:14883`; the receipts below. The disjointness proof detects planted overlaps, the derivation arm tests reversed and permuted workflow order, and run-level controls pin warning/report behavior without changing the candidate verdict. Reader-join removal, join reordering, missed retries, abandonment after a bounded wait, first-failure reversal and wrong event time all fail. The new real-boundary controls reject the preceding implementation, lost primary capture, signal takeover, swallowed signal and missing beside-diagnostic.

[R633] PASS Docs - `docs/testing/CI_WORKFLOWS.md:1745`, `:1760`, `:1773`, `:1803`, `:1813`, `:2180`; [reviewed PR body](receipts/pr-body-reviewed.md), issue decisions and published source receipts. The text accurately describes retained reservations, inspect-based placement, all-slot refusal, fixed slot spacing, mixed-version incompatibility, warning-only placement uncertainty, masked cleanup and first-failure precedence. R632-5-R1/R2 are applied at lines 1833-1838. No speedup or hardware proof is claimed. The PR uses `Relates to #730`, retaining the deferred obligations.

All candidate imports, offline self-tests and mutations executed inside disposable unprivileged namespaces, with network, host credentials and daemon sockets absent. The host never invoked the candidate runner as an orchestrator or ran its self-test directly. Foreground drivers joined all work; campaigns used six workers each and focused work used at most four more. No background job is left running.

| Executed check | Result | Raw receipt |
|---|---|---|
| Exact-head offline runner self-test | 525 passing arms, zero FAIL; includes 18 closing cases and the per-step cleanup sweep | [self-test](receipts/independent-selftest.log), [rc](receipts/independent-selftest.rc) |
| Per-step standing signal sweep | 185 traced steps, main-thread and process-directed delivery: 370 injections; cleanup, conventional status and mask restoration pass | Same self-test receipt; step count depends on interpreter |
| Unchanged R633-5 probe | All nine cases preserve the Refusal/status 2 and finish cleanup | [boundary](receipts/independent-boundary.log) |
| Earliest closing restore, independent locator adaptation | All nine cases pass; three inject at unmasked line 5357 | [first restore](receipts/first-restore.log) |
| Unchanged R633-4 cleanup-entry probe | Six cases pass; INT/TERM/HUP exit 130/143/129 with cleanup finished | [cleanup entry](receipts/cleanup-entry.log) |
| Unchanged R633-1 probe | rc 1 at the changed `JobCpuRanges` constructor, missing `read_cpus`; not credited as a lifecycle pass | [unchanged probe](receipts/r633-r1-unchanged.log) |
| Published R633-1 compatibility probe | Same lifecycle/failure assertions pass with the new inspection collaborator | [compatible probe](receipts/r633-r1-compatible.log) |
| R633-2 lifecycle and monitor probes | No overlapping range; original error/signal preserved; reap error reported beside it | [lifecycle](receipts/r633-r2-lifecycle.log), [monitor](receipts/r633-r2-monitor.log) |
| R632 shutdown and derivation probes | S1-S4 pass; 300 seeds / 120,000 lifecycle steps, zero violations; all 64 slots and workflow order checked | [shutdown](receipts/r632-r2-shutdown.log), [derivation/lifecycle](receipts/r632-r3-probe.log) |
| Unchanged R632-2 mutation campaign | 36/36 killed, no bad anchors; K12/K13/K32/K36 killed; K10 join removal fails 35 arms | [round 2](receipts/mutants-r2.log) |
| Unchanged R632-3 mutation campaign | 24/30 killed, Q24 killed, no bad anchors; Q06/Q11/Q13/Q15/Q28/Q29 survive as previously disclosed | [round 3](receipts/mutants-r3.log) |
| Prior signal controls E01-E08 | All rejected; E06/E07 anchors adjusted for nesting while retaining their defects | [control results](receipts/signal-controls.json), `receipts/signal-E*.log` |
| Independent closing controls | Clean C00 passes. C01/C02/C03/C05/C06 fail 6/6/5/9/6 named arms. C05 substitutes the preceding boundary while retaining current tests | `receipts/signal-C*.log`, [additional result](receipts/signal-controls-extra.json) |
| Offline dry-run harness | Slots 0 and 3 print all four ranges, after `0-3` / `60-63` staging | [dry run](receipts/offline-dryrun.log) |
| CI contract and controls; slot proof; language ratchet and controls; documentation privacy/style/paths; diff whitespace | Pass: 2016 contract items, 2828 contract arms, 44 slot cases, 54 language controls, zero doc findings | [run inventory](receipts/independent-runs.json), corresponding logs/rc files; [native diff rc](receipts/diff-check-host.rc) |

The unchanged boundary probe now selects the outer restore at line 5376, where the mask is already held. Its pass alone would not prove the newly nested, unmasked restore. The independent locator adaptation explicitly selects line 5357, and the standing cases cover both sites. Restoring the prior boundary produces nine named failures in C05. C04, which changes only the diagnostic prefix while retaining signal type/name and the preserved-failure explanation, survives; it is not counted as a killed defect. Removing the diagnostic itself is C06 and fails six arms. An initially malformed C06 injection was discarded before grading and corrected; only its valid executable receipt is credited.

The first namespace Git check could not resolve the clone's external alternate object store. Its rc 128 is an execution-environment limitation, not a source finding. The identical read-only `git diff --check dc4d06cb HEAD` run directly in the clone passed. The offline dry-run uses synthetic PR metadata and inert boundaries; it is output-wiring evidence, not a live dry-run or daemon measurement. [Script hashes](receipts/unchanged-scripts.json) establish the required public probes and campaign drivers are unchanged.

The [published author evidence](https://github.com/kebag-logic/milan-fpga/tree/fa4034a877f3017c93ddf28e4e85ce24b42b3181/review-evidence/730-r1/author-r6/receipts/r6) was examined after the independent diff pass. [Verification](receipts/author-evidence-verification.json) matches both changed source files to this exact head and verifies 50 receipt hashes against the publication manifest. These include the source self-test, code/doc gates, mutation outcomes and dry-run record. They are author source execution evidence. No manager source bank ran at this exact head, and none is claimed or inferred.

Prior public findings are resolved or retained explicitly:

| Finding | Severity / original lenses | Disposition and exact-head evidence |
|---|---|---|
| R633-1-F1 | MAJOR / all five | RESOLVED: `observe` at :5525 retains reservations on `die`; restart probe and K01 detect premature reuse |
| R633-1-F2 | MAJOR / all five | RESOLVED: `place` at :5487 reserves before update; uncertain target remains held; applied/lost-update probes and K02/K03/K07/K08 fail regressions |
| R633-1-F3 | MAJOR / all five | RESOLVED: :4719 refuses insufficient CPUs on all slots; boundary probes and K15/K16 |
| R633-1-F4 | MAJOR / all five | RESOLVED: :5610 finishes containment/join/pipe handling before propagating; monitor/reap probes and K09-K14 |
| R632-1-F1 | MINOR / Tests, Docs | RESOLVED: busy-reader standing controls; K10 removal and K11 reorder are killed |
| R632-1-F2 | MINOR / Tests | RESOLVED: :6589 run-level warning/verdict controls; K23/K24 killed |
| R633-2-F1 | MINOR / all five | RESOLVED: primary passed into cleanup at :5770; unchanged monitor probe preserves original error and 143 beside reap failure |
| R632-2-F1 | MINOR / Tests | RESOLVED: unchanged K12/K13/K32/K36 all killed by the claimed arms |
| R632-3-F1 | MINOR / Tests | RESOLVED: :7171 permutation/reversed-order arm; unchanged Q24 killed |
| R633-4-F1 | MAJOR / all five | RESOLVED: :5754 hold precedes yield and survives into :5767 cleanup; six unchanged cleanup-entry cases and standing per-step sweep pass; E01/E02 fail |
| R633-5-F1 | MINOR / all five | RESOLVED under decision 6137869227: :5354 captures the primary; :5358 handles closing interruption; earliest-restore probe and 18 standing cases pass; C05 reinstates the failure |
| R632-1-R1 / R2 | RESIDUE / Docs | APPLIED / SUPERSEDED: mixed-version rule at CI policy :2187; PR now states refusal on every slot |
| R632-5-R1 / R2 | RESIDUE / Docs | APPLIED: exact beside-signal diagnostic and “Throughout” at CI policy :1833-1838 |
| R632-1-S1/S2/S3; R632-2-S1 | SUGGESTION / Robustness or Tests as originally filed | ADDRESSED by retained reservations, unconditional cleanup completion, and K29/K31-sensitive controls |
| R632-1-S4 | SUGGESTION / Robustness | ADDRESSED by the distinct removed-before-placement summary at :5553 and corresponding CI policy description |
| R632-2-S2 / R632-3-S2 / R632-4-S2 | SUGGESTION / Robustness; Docs also in R632-4 | ADDRESSED for this monitor by the mask; suggestions concerning unrelated cleanup entries remain outside this delta |
| R632-5-S1 | SUGGESTION / Tests | RETAINED: some fault controls can exit the whole gate instead of reporting a named arm; optional diagnostic improvement |
| R632-5-S2 | SUGGESTION / Tests, Docs | ADDRESSED: PR now states the sweep count depends on the interpreter |
| R632-3-S1 / R632-4-S1 / R632-5-S3 | SUGGESTION / Tests | RETAINED: Q06/Q11/Q13/Q28/Q29 remain standing-test gaps; Q15 is the previously recorded equivalent control. Current code is correct by inspection and focused probes |
| R632-2-S3 / R632-3-S3 / R632-4-S3 / R632-5-S4 | SUGGESTION / Robustness | RETAINED: :5591 failed-join path can use the bounded-shutdown wording without a completed bounded wait. Containment still holds; optional distinction between failed join and timeout |

The retained optional test suggestions concern `stop_job_cpu_range_monitor` pipe-close reporting, `JobCpuRanges` staging/off-target summaries, the stream's stderr sink, and `run_validation`'s materialized-checkout selection. A future arm should fail when each corresponding behavior is removed; the current Q-series and focused derivation probe are the verification references. No optional suggestion is being relabeled to clear a previously blocking finding.

R633-6-R1 | RESIDUE | Docs | PR #731 body, Status paragraph ([snapshot](receipts/pr-body-reviewed.md)).

Authority/evidence: the public PR head is the assigned `73b8dcd6`, but the status still says “These two new commits have not been pushed.” Impact: stale publication wording only; it changes no measurement, figure, verdict, executable behavior, conformance or clause claim. Exact fix: delete that sentence. Verification: reread the public Status paragraph after publication cleanup. The manager carries this item on the residue checklist; it does not unclean Docs.

Reviewer-owned completion ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #730 acceptance/decisions; act_ci.py:2090, 2119, 4671, 4719, 5313, 5918; workflow inputs; range and warning probes | R633-6 | 73b8dcd667aa5bf1254e828dd1dd7217c8a103ce |
| RTL | CLEAN | Full two-file diff; act_ci.py:5380, 5515, 5574, 5610, 5675, 5818; unchanged hardware/interface scope and gitlinks | R633-6 | 73b8dcd667aa5bf1254e828dd1dd7217c8a103ce |
| Robustness | CLEAN | Allocator/monitor/closing boundary; lifecycle, shutdown, cleanup-entry, first-restore and signal-control receipts | R633-6 | 73b8dcd667aa5bf1254e828dd1dd7217c8a103ce |
| Tests | CLEAN | act_ci.py:6589, 7171, 7268, 7857, 8334, 12415, 12570, 14883; 525-arm receipt; K/Q and E/C campaigns; disclosed optional survivors | R633-6 | 73b8dcd667aa5bf1254e828dd1dd7217c8a103ce |
| Docs | CLEAN | CI_WORKFLOWS.md:1745, 1760, 1803, 1813, 2180; public contract, PR and source receipts; docs gates; R1 wording residue | R633-6 | 73b8dcd667aa5bf1254e828dd1dd7217c8a103ce |

[Final integrity verification](receipts/integrity.json) passes raw bytes, modes and stage-zero index against the exact head for 1,301 root entries and all 880 tracked files in the three initialized submodules. All five root gitlinks match their required values. The unused external and lwSRP checkouts remain uninitialized; their gitlinks are verified, not their absent contents. Nothing tracked required restoration. There are no nonignored untracked files in the clone. Three public receipt files normalize only private absolute paths; original-byte hashes and replacements are recorded in `receipts/publication-normalization.json`. Portable drivers, scripts and receipts are enumerated in [MANIFEST.sha256](MANIFEST.sha256); disposable trees and installations are excluded under `scratch/`.

The [exact-head hosted snapshot](receipts/hosted-snapshot.json) records 12 successful jobs, 11 in progress and one skipped physical-gPTP job. The required aggregate bar was not complete at that snapshot. Executed jobs and skipped contexts are not interchangeable evidence. The manager owns hosted and replay acceptance; this review did not wait for or replace those checks.

Real limits: no live replay, daemon event timing, live affinity/nproc check, performance comparison, full parent/processor/builder/synthesis bank, hardware activity, shared installation, privileged operation, source fix, commit, push, GitHub write, author contact or delegated review. Physical calibration NOT RUN; field skips are not hardware proof. Signal delivery points were chosen by line tracing with inert process collaborators and real reader threads. This establishes the selected ordering and failure behavior, not the frequency of live races.

Pending manager duties: reconcile the independent reviews at this head, publish these receipts and carry R633-6-R1; accept exact-head hosted evidence; build and validate the then-current-dev merge candidate, including builder and native banks, and link its receipts. The supplied source base is `dc4d06cb`; the supplied live-dev tip is `49da9fd974e8805d56c90e29dcfcb67994c2c430`. Neither is a validated future merge result. Obtain explicit maintainer merge authorization and perform post-merge containment. Under the disk ruling, retain acceptance 3's same-head verdict comparison, acceptance 4's per-job wall-clock/slot-memory measurement, and optional acceptance 5 after merge. Keep #730 open until its remaining duties are discharged.

R633-6 FINISHED
