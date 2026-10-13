[R633] NEGATIVE - exact head ede700b00ef4d79566a6f108b11ce9bd4ad6beaa

R633-5, external independent review of issue #730 / PR #731. All five lenses were applied. One MINOR finding remains: a first signal at the normal act boundary's closing mask restoration replaces an integrity Refusal that is already propagating. Stream containment, reader completion and pipe closure still succeed in this case. The earlier cleanup-entry containment defect is resolved.

This is a source-review verdict, not merge authorization. Tree: `1efdeba1e3477de15b8f04c5615c6d58e2756e46`. Source base: `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`. Observed live dev: `d5858bbee328cf8d2c39a99ec14203f5d0ddd123` ([scope receipt](receipts/scope.json)).

Reconstruction used AGENTS.md, CONTRIBUTING.md, docs/README.md, the [frozen issue and public decisions](https://github.com/kebag-logic/milan-fpga/issues/730), REQUIREMENTS.md section 8, CI_WORKFLOWS.md, the architecture verification boundary and submodule ownership rules. The [full diff](full.diff), [round-5 delta](round5.diff) and [ten-commit history](receipts/history.txt) were inspected before prior public findings. Only the runner and CI documentation change. No workflow, HDL, firmware, product interface or gitlink changes.

The [disk ruling](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815) defers live replay measurement and comparison. Public executable inputs came from evidence commit `783701eb94a967a23efafca2a86aa13a9c542051`; no private author material or other checkout was inspected.

## Finding

**R633-5-F1 | MINOR | Conformance, RTL, Robustness, Tests, Docs**

**Artifacts:** `scripts/act_ci.py:5350` and `:5351` (`execute_act_boundary` closing `finally`); `:5738` (monitor captures the exception only after the boundary has exited); `:8309` and `:12390` (standing signal controls); `docs/testing/CI_WORKFLOWS.md:1818`, `:1823` and `:1828`; PR #731 Round 5 failure-precedence claim.

**Authority:** [round-3 decision 6133149921](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6133149921) requires an already-propagating interruption or original failure to retain its status and diagnostic after cleanup. [Round-5 decision 6134111240](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6134111240) preserves that precedence while closing the signal window. The implementation's boundary docstring also promises restoration before returning or raising. The authoritative document states that an earlier body failure retains precedence.

**Evidence:** [probe_boundary_precedence.py](scripts/probe_boundary_precedence.py) runs the exact monitor and the exact production `execute_act_boundary`, with inert process/command collaborators and a real reader. The integrity callback raises `Refusal("original integrity failure")`. A trace hook delivers a real first INT, TERM or HUP immediately before line 5351 executes. At that point `sys.exception()` is the original Refusal and all three cleanup signals are unblocked. No candidate source is changed.

The first signal raises from the boundary's `finally`, skips its mask-restoration call, and supersedes the active Refusal before `job_cpu_range_monitor` can capture `primary`. The monitor consequently receives the signal as its primary exception. It completes containment and joining, but the application returns signal status and prints only the interruption diagnostic. The earlier Refusal is not the reported outcome.

[Raw receipt](receipts/boundary-precedence.log), [rc 1](receipts/boundary-precedence.rc):

| Delivery point after the Refusal | Cases | Result | Original diagnostic | Containment / reader ended / pipe closed |
|---|---|---|---|---|
| No signal, control | 3 | Refusal, status 2 | Preserved | All true |
| Boundary closing restoration, line 5351 | INT / TERM / HUP | 130 / 143 / 129 | Lost | All true |
| Monitor cleanup entry, line 5742, control | INT / TERM / HUP | Refusal, status 2 | Preserved; signal printed beside it | All true |

Thus the boundary's closing transition still violates first-failure precedence, although the monitor's protected cleanup works once reached. This is narrower than R633-4-F1: the probe does not demonstrate a leaked stream, a live reader at teardown, or a successful verdict after refusal.

**Impact:** an integrity/remote-state Refusal can be reported as an interruption instead, hiding the original reason and changing status 2 to 128 + signal. The new closing `finally` introduces this interruption point. This affects code behavior and its documented precedence claim, so it is not wording-only RESIDUE.

**Required outcome:** preserve the active failure and its diagnostic when the first signal arrives while the normal boundary closes its temporary signal window. Restore the monitor's hold and finish all containment obligations. Keep normal act interruptible, preserve pending-signal delivery before act starts, and retain conventional signal status when no earlier failure exists. Add a standing control using the real boundary with an earlier failure and delivery at its closing restoration.

**Verification:** rerun the new probe in the disposable boundary; all nine cases must retain the original Refusal, with later signals reported beside it. Retain the unchanged cleanup-entry probe, existing signal-window controls, full self-test and prior mutation outcomes. No source fix was made.

**Lens attribution:** Conformance covers the public precedence requirement; RTL covers the software boundary's exception/mask handoff; Robustness covers failure plus asynchronous interruption; Tests covers the missing failure-path control at that transition; Docs covers the unconditional restoration/precedence claim. No other open MINOR, MAJOR or BLOCKER was found. No new RESIDUE is recorded.

## Independent full-PR assessment

- **Conformance:** `act_ci.py:2090`, `:2119`, `:4671`, `:4719` and `:5896` derive from the materialized selected workflows, bound the widest concurrent jobs, and refuse unreadable or excessive concurrency. Slot N occupies `20N..20N+19`; staging and job ranges are four wide. The read interpretation agrees with the pinned [default-width implementation](https://github.com/nektos/act/blob/v0.2.89/pkg/model/workflow.go#L219) and [scheduler](https://github.com/nektos/act/blob/v0.2.89/pkg/runner/runner.go). Capacity and order probes pass. F1 leaves precedence unclean.
- **RTL / architecture:** the full diff leaves hardware interfaces and CDC untouched. `JobCpuRanges` at `:5355` has one reader writer; reservations precede updates and survive uncertainty. `:5836` nests the monitor inside the existing ownership/lease boundary. `:5585` contains the stream, waits for reader death and closes the pipe before outer teardown. Container memory/swap, the isolated-slot memory cap and ownership labels remain unchanged. The mask restoration handoff at `:5351` has F1.
- **Robustness:** `:5413`, `:5443` and `:5488` retain reservations through die/restart, applied-but-timed-out updates, delayed completion and unreadable inspect; only removal releases them. The two independent public lifecycle models pass 76,800 and 120,000 transitions, plus capacity boundaries. Malformed, foreign, duplicate and delayed events, missing removals, reap/join failures and held readers are exercised. F1 is the remaining failure/interruption combination.
- **Tests:** the unchanged full self-test passes 507 arms. The order arm tests both two-workflow orders and all six three-workflow orders at concurrent-job limits 1, 2 and 3. Planted overlaps and the no-join control fail as intended. The standing signal sweep passes 185 executed line steps with main-thread and process-wide delivery, 370 injections on this interpreter; the author's 198/396 count used a different interpreter. The sweep's ordinary-return path and its cleanup-entry body-error arm do not cover the real boundary's failure at closing restoration, as F1 demonstrates.
- **Docs:** the entire CI_WORKFLOWS.md diff and current PR body accurately describe allocation, reservation lifetime, inspect confirmation, slot-0 refusal, mixed-version restrictions and deferred measurement. The new mask/delivery text reflects the intended contract, but F1 leaves its restoration/precedence claim unsatisfied. Mechanical documentation gates pass.

## Executed evidence

Candidate runner imports and self-tests ran only in unprivileged disposable namespaces, without network, daemon socket or credentials. Mutation trees are confined to packet `scratch/`. Foreground drivers waited for every child: two campaigns used six workers each, with at most four other focused jobs, never more than sixteen. No heavy build ran.

| Check | Result / receipt |
|---|---|
| Unmodified candidate self-test | rc 0, 507 ok, 0 FAIL; [log](receipts/selftest.log) |
| R633-4 cleanup-entry probe, unchanged | rc 0, all six cases: contained stream, ended reader, closed pipe, 130/143/129; [log](receipts/cleanup-entry.log) |
| R632-2 campaign, unchanged | 36/36 killed; K12, K13, K32, K36 all killed; no bad anchors; [log](receipts/mutants-r2.log) |
| R632-3 campaign, unchanged | 24/30 killed; Q24 killed; unchanged survivors Q06/Q11/Q13/Q15/Q28/Q29; no bad anchors; [log](receipts/mutants-r3.log) |
| Eight published round-5 signal mutations | All rejected by targeted arms or the expected interrupt-probe Refusal, not timeouts; [commands/status](receipts/controls-gates.json), E01-E08 logs |
| R633-1 original script, unchanged bytes | rc 1 at its obsolete constructor: missing inspect callback; [log](receipts/r633-r1-unchanged.log). Harness incompatibility, not a candidate finding |
| Published R633-1 compatibility adapter, unchanged | rc 0; same restart, applied-timeout, slot-0 refusal and reap-failure probes pass; [log](receipts/r633-r1-compatible.log) |
| R633-2 lifecycle / monitor probes, unchanged | rc 0; 76,800 transitions, 88 capacity combinations; original failure/signal precedence after monitor entry, no-join mutant, warnings and verdicts; [lifecycle](receipts/r633-r2-lifecycle.log), [monitor](receipts/r633-r2-monitor.log) |
| R632-3 lifecycle/derivation and R632-2 shutdown probes, unchanged | rc 0; 120,000 transitions, P1-P5 and S1-S4; [lifecycle](receipts/r632-r3-probe.log), [shutdown](receipts/r632-r2-shutdown.log) |
| Offline dry-run path | rc 0; correct slot-0 and slot-3 staging/job options; [log](receipts/offline-dryrun.log). Synthetic PR/head and inert external boundaries |
| New boundary-closing precedence probe | rc 1; three failures, six controls pass; [log](receipts/boundary-precedence.log) |
| Focused policy gates | CI contract 2016 items / 2828 arms; slot proof 44 cases; Python idiom check / 54 controls; bare-metal check / 700 controls; all rc 0 |
| Documentation and whitespace | Privacy/routing, style, paths, TOC, anchors, em-dash and diff checks rc 0; em-dash 0 findings over 157 added lines |

[Review run commands](receipts/review-runs.json), [remaining gate commands](receipts/controls-gates.json), and [Markdown gate commands](receipts/markdown-gates.json) carry separate statuses. Per-mutant stdout, stderr and rc are retained under `receipts/mutant-logs/`. Q15 is the previously recorded equivalent control; the other five survivors are retained optional test suggestions, not claimed kills. Their corresponding implementation paths were read.

The published author's [source manifest](public-inputs/author-r5/receipts/r5/source-manifest.json) matches both exact-head changed files. All 69 fetched public input blobs match the evidence commit; all 68 downloaded files represented in the outer publication manifest match their published hashes ([verification](receipts/public-input-hashes.json), [publication hashes](receipts/public-publication-hashes.json)). The inner author manifest includes three items not published there: two redundant source exports and the long CI self-test log. The available result/rc receipts cover that command, and this review independently ran it. Those absent exports are not claimed as inspected evidence. No manager source bank exists at this head; none is claimed or inferred.

## Prior public findings at this head

| Finding | Disposition | Current evidence |
|---|---|---|
| R633-1-F1, restart reuse | Resolved | Reservation survives die; unchanged compatible sequence and both lifecycle models pass |
| R633-1-F2, uncertain update | Resolved | Applied timeout and delayed completion retain targets until removal |
| R633-1-F3, slot-0 fallback | Resolved | Insufficient derived capacity refuses; boundary probes pass |
| R633-1-F4, reap skips join | Resolved | Reap failure still contains/joins/closes; K09/K10/K11/K14 killed |
| R632-1-F1, ineffective join control | Resolved | K10 killed; independent no-join control observes reader alive |
| R632-1-F2, warning/verdict test gap | Resolved | Run-level success/failure controls pass; K23/K24 killed |
| R632-1-R1/R2 | Applied / superseded | CI_WORKFLOWS.md:2179 states one-version rule; PR states refusal on every slot |
| R632-1-S1 through S4 | Addressed | Lifetime, uncertainty, reap finalization and removed-before-placement summary corrected |
| R633-2-F1, cleanup replaces primary | Original fault resolved | Unchanged monitor probe passes; the newly added normal-boundary closing path has R633-5-F1 |
| R632-2-F1(a)-(d) | Resolved | Unchanged campaign kills K12/K13/K36/K32 |
| R632-2-S1 | Addressed | K29/K31 killed |
| R633-4-F1; R632-2-S2 / R632-3-S2 | Resolved | Unchanged cleanup-entry probe passes six cases; busy-reader per-step sweep and E01-E05 controls pass/reject as expected |
| R632-2-S3 / R632-3-S3 | Optional SUGGESTION retained | Immediate join failure still uses bounded-shutdown wording; containment still holds |
| R632-3-F1, maximum-order arm | Resolved | Q24 killed precisely by the order arm |
| R632-3-S1 | Optional SUGGESTION retained | Q06/Q11/Q13/Q28/Q29 survive; implementation remains present and was inspected |

The public review inventory contains no submitted review bodies or inline comments beyond the conversation findings checked. No previous positive verdict substitutes for this round's evidence.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1 | #730 decisions; act_ci.py:2090, 4719, 5351, 5896; capacity/order and boundary-precedence receipts | R633-5 applied; no clean covering round | ede700b00ef4d79566a6f108b11ce9bd4ad6beaa |
| RTL | UNCLEAN: F1 | Full two-file diff; architecture section 7; act_ci.py:5351, 5355, 5585, 5738, 5836; mask/exception handoff | R633-5 applied; no clean covering round | ede700b00ef4d79566a6f108b11ce9bd4ad6beaa |
| Robustness | UNCLEAN: F1 | act_ci.py:5413, 5443, 5488, 5550, 5351; lifecycle, shutdown and nine-case boundary probe | R633-5 applied; no clean covering round | ede700b00ef4d79566a6f108b11ce9bd4ad6beaa |
| Tests | UNCLEAN: F1 | act_ci.py:6564, 7146, 7243, 7922, 8309, 12390; 507-arm log, both unchanged campaigns, new probe | R633-5 applied; no clean covering round | ede700b00ef4d79566a6f108b11ce9bd4ad6beaa |
| Docs | UNCLEAN: F1 | CI_WORKFLOWS.md full diff, especially :1818 and :1823; issue/PR, public manifests and documentation gates | R633-5 applied; no clean covering round | ede700b00ef4d79566a6f108b11ce9bd4ad6beaa |

## Limits, integrity and manager duties

No live PR replay, live dry-run, Docker operation, host runner/self-test, privilege, hardware work, source fix, commit, push, GitHub write, author contact or delegated review occurred. No full parent, processor, gPTP, synthesis or builder bank ran. Four-wide masks were checked; live container affinity and `nproc` were not measured. Daemon timing, scheduling performance and memory effects remain unmeasured. Physical calibration was NOT RUN; field skips are not hardware proof.

The [exact-head hosted snapshot](receipts/hosted-checks.json) contains 11 successful completed jobs, 12 in-progress jobs and one skipped physical job. It does not establish the required-context bar. A skipped context is not executed evidence. Hosted and replay acceptance belong to the manager.

[Final integrity](receipts/integrity.json) proves all 1301 root tree/index entries, 1296 raw tracked blobs and executable/symlink modes. All five gitlinks match. The three populated dependency checkouts match their pins and raw tracked bytes; unused external and lwSRP checkouts remain uninitialized. The worktree is clean. Candidate tracked files were never edited, so restoration was unnecessary. Disposable copies, environments and mutation trees stay under `scratch/` and are excluded from publication. Receipt path normalization, where needed, is recorded separately; scripts remain portable and public input bytes remain unchanged.

The manager must carry F1 to the executor and obtain fresh review after its correction. At the merge turn, construct and validate the current-dev candidate, including the builder and native banks, and publish its receipts separately from these source-head results. Complete hosted acceptance, obtain explicit merge authorization and perform post-merge containment. Under the disk ruling, acceptance 3's same-head verdict comparison, acceptance 4's per-job wall-clock and slot-memory measurement, and optional acceptance 5 remain post-merge duties. Keep #730 open until those retained obligations are discharged.

R633-5 FINISHED
