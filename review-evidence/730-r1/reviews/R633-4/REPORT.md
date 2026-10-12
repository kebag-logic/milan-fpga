[R633] NEGATIVE - exact head 31e53e82a4a1604569ccacba8473f21e70b9cbc0

R633-4, external independent review of issue #730 / PR #731. One MAJOR finding remains: a first termination signal at monitor cleanup entry can bypass containment and reader joining. All five lenses were applied and are UNCLEAN under this finding. This is a source-review verdict, not merge authorization.

The round-4 test change satisfies its assignment. Q24 is killed by the new workflow-order arm, and the unmodified self-test passes 498 arms. The finding below concerns the full PR and was previously described publicly as an optional suggestion. It is not a runtime regression introduced by the test-only commit.

Head tree: `9dc0b704562f67cab1d805b40d56a5c983ddcebb`. Source base and observed live dev: `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`. Reviewed all seven commits and the [complete two-file diff](full.diff), then the [round-4 delta](round4.diff). No workflow, HDL, firmware, interface or gitlink changed. [AST comparison](receipts/round4-runtime-identity.json) confirms that `selftest_job_concurrency` is the only changed function/class since `5c6f489a`; the other addition is its `itertools` import.

Reconstruction used AGENTS.md, CONTRIBUTING.md, docs/README.md, the [frozen issue](https://github.com/kebag-logic/milan-fpga/issues/730), [assignment](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131408752), [disk ruling](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815), and public round-2/3/4 decisions. REQUIREMENTS.md section 8, CI_WORKFLOWS.md and the architecture/submodule authorities supplied the verification and interface boundaries. An independent source-pass verdict and ledger were written before reading prior public findings. Those findings and published executable receipts were then checked against this head. No private author material was read.

**R633-4-F1 | MAJOR | Conformance, RTL, Robustness, Tests, Docs**

Artifact: `scripts/act_ci.py:5681` through the call at `:5683`; signal handler at `:283`; cleanup mask at `:5549`; standing signal controls at `:7843`; `docs/testing/CI_WORKFLOWS.md:1807`; PR #731 Description/Shutdown and Known limitations.

Authority/evidence: the assignment requires containment and joining on every exit, preserving cleanup guarantees. Round-2 decision [6132404197](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6132404197) requires reader completion and stream containment before boundary teardown. The authoritative CI document makes the same unconditional claim.

[probe_cleanup_entry.py](scripts/probe_cleanup_entry.py) extracts the exact monitor, cleanup and signal-handler definitions. It supplies inert process/command collaborators and a real worker held in an in-flight move. A trace hook delivers a real first SIGINT, SIGTERM or SIGHUP immediately before line 5682 executes, after the body returns. This selects an asynchronous interruption point without changing candidate code. The handler raises `TerminationRequest` from the generator's `finally`, before `stop_job_cpu_range_monitor` reaches its mask. The body-level `except` cannot catch this exit.

The [raw receipt](receipts/cleanup-entry.log), rc 1, records six cases:

| Signal delivery | Cases | Containment called | Reader alive at outer teardown | Pipe closed | Exit statuses |
|---|---|---|---|---|---|
| Inside the body, control | INT, TERM, HUP | yes | no | yes | 130, 143, 129 |
| At cleanup entry, line 5682 | INT, TERM, HUP | no | yes | no | 130, 143, 129 |

In each failing case the pending modeled move finishes only after the outer teardown observation, when the reviewer releases and joins the worker. The diagnostic nevertheless says the interruption occurred “after cleanup.” The stream collaborator is inert: this demonstrates skipped containment and ordering, not a measured live-daemon leak or its frequency. Every probe worker is joined before the probe exits.

Impact: the Docker boundary can unwind while the reader can still issue or finish an update. The event-stream process group receives no containment call on this path. This violates the ordering property behind the accepted round-1 reaping finding. The standing self-test remains green because its signals arrive inside the body, where the generator still has a cleanup-bearing unwind. The documented all-exits claim is false for this transition.

Required outcome: a first cleanup signal during the body-to-cleanup transition must still complete stream containment, reader completion/dead-thread proof and pipe finalization before outer teardown. Preserve conventional signal status and the required first-failure precedence. Add a standing control for this delivery point and align the authoritative guarantee with the implementation.

Verification: re-run `probe_cleanup_entry.py` in the disposable boundary. All six cases must observe containment, an ended reader and a closed pipe before teardown, with statuses 130/143/129 preserved. Keep the existing reaping, join-retry, hold, warning/verdict, lifecycle and mutation controls green.

Disposition of the earlier suggestion: this is R632-2-S2 / R632-3-S2, retained as F1 with demonstrated failure and all attributable lenses. The [round-3 decision](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6133149921) called suggestions optional, and the PR body defers this window. That public treatment is acknowledged. It does not satisfy this review's explicit all-exits criterion or change the unconditional authoritative cleanup contract. The narrow timing window and similar patterns elsewhere do not establish containment here. This is not wording-only RESIDUE. No source change was made.

**Full-PR assessment**

- Conformance: derivation at `act_ci.py:2044`, layout at `:4625`, capacity refusal at `:4673`, and the materialized-checkout call at `:5835` read selected workflows and refuse unsupported/excessive concurrency. Slot spacing is 20 CPUs with four-wide staging/job ranges. All 64 slots and capacity boundaries were exercised. The interpretation matches the pinned [scheduler](https://github.com/nektos/act/blob/v0.2.89/pkg/runner/runner.go#L171) and [default matrix width](https://github.com/nektos/act/blob/v0.2.89/pkg/model/workflow.go#L219). F1 prevents cleanup conformance.
- RTL/architecture: the full diff changes no HDL, CDC or product interface. The software lifecycle was reviewed: one reader owns allocation state; summaries follow joining; reservations precede updates; removal releases them. The monitor retains the existing slot command context, ownership filter, process-group boundary, lease gate and cleanup wiring. Memory/swap bounds and the slot cap are unchanged. F1 is an uncovered handoff in this architecture.
- Robustness: `JobCpuRanges:5300` retains reservations after death/restart and uncertain moves; inspect reconciles placement. Independent public models passed 76,800 and 120,000 transitions covering lost/applied updates, delayed events, removal without events and malformed/foreign input. Applied configuration versus CLI success agrees with the [daemon update implementation](https://github.com/moby/moby/blob/v28.0.0/daemon/update.go). Failures after cleanup enters its mask preserve the original failure. F1 covers the missing first-signal entry case.
- Tests: the new derivation arm covers both two-workflow orders and all six three-workflow permutations at job limits 1, 2 and 3, with expected maxima 4, 6 and 7. Q24 fails precisely that arm. Planted overlap, restart/timeout, busy reader, retry/hold, warning invariance and offline dry-run controls passed. The standing signal controls miss F1.
- Docs: the complete CI_WORKFLOWS.md diff, issue decisions, PR body and receipt provenance were checked. Layout, reservations, placement, slot-0 refusal, mixed-version restriction and deferred measurements match the code. The unconditional shutdown claim remains incorrect under F1; documentation gates do not discharge that semantic claim.

**Executed evidence**

Candidate imports and self-tests ran only in unprivileged disposable namespaces, with no network, daemon socket, credentials or host orchestration access. Mutation trees are under packet `scratch/`. Foreground drivers await every child. The campaigns ran concurrently with eight workers each, at most sixteen total. No heavy build ran.

| Check | Result and receipt |
|---|---|
| Unmodified candidate self-test | rc 0, 498 ok, 0 FAIL; [log](receipts/selftest.log) |
| R632-2 `mutants_r2.py`, unchanged | 36/36 killed; K10/K12/K13/K32/K36 fail relevant standing arms; [campaign](receipts/mutants-r2-unchanged.log) |
| R632-3 `mutants_r3.py`, unchanged | 24/30 killed, Q24 killed, no bad anchors; [campaign](receipts/mutants-r3-unchanged.log) |
| R633-1 original script, byte-for-byte | rc 1 before defect probes: constructor now requires inspect callback; [log](receipts/r633-r1-unchanged.log). Harness incompatibility, not a candidate finding |
| Published R633-1 compatibility adapter, unchanged | rc 0; original restart, applied-timeout, insufficient slot-0 capacity and reap-failure cases pass; [log](receipts/r633-r1-compatible.log) |
| R633-2 lifecycle and monitor probes, unchanged | rc 0; 76,800 transitions, 88 capacity combinations, failure precedence, no-join control and warning/verdict wiring; [lifecycle](receipts/r633-r2-lifecycle-unchanged.log), [monitor](receipts/r633-r2-monitor-unchanged.log) |
| R632-3 lifecycle/derivation and R632-2 shutdown probes, unchanged | rc 0; 120,000 transitions, P1-P5 and S1-S4; [lifecycle](receipts/r632-r3-probe-unchanged.log), [shutdown](receipts/r632-r2-shutdown-unchanged.log) |
| New cleanup-entry fault probe | rc 1; three controls pass, three entry cases violate containment; [log](receipts/cleanup-entry.log) |
| Offline dry-run path | rc 0; correct slot-0 and slot-3 plan/options; [log](receipts/offline-dryrun.log). Synthetic PR/head and inert boundaries, not live `--dry-run` |
| Slot-proof self-test | rc 0, 44 cases; [log](receipts/slot-proof-selftest.log) |
| Focused policy/documentation checks | CI contract 2016 items/2828 arms; Python idiom 54 controls; bare-metal 700 controls; privacy/routing, style, paths, TOC, anchors and em-dash: rc 0; [commands/results](receipts/gates.json) |
| Diff whitespace | rc 0 on read-only host Git; [rerun provenance](receipts/diff-check-rerun.json). Initial isolated attempt could not access the clone's alternate object store; its public diagnostic redacts only that private path |

Each mutation has separate stdout, stderr and status under `receipts/mutant-logs/`. [Hashes](receipts/unchanged-campaign-scripts.json) verify unchanged public drivers. Round-3 survivors are the previous optional controls Q06/Q11/Q13/Q28/Q29 and equivalent Q15; none is counted as killed. The actual code retains the behavior those optional mutations remove.

The [published author receipts](https://github.com/kebag-logic/milan-fpga/tree/24efc3346903a44ea112bfe1c6b3b6d86870cacb/review-evidence/730-r1/author-r4/receipts/r4) record 498 passing arms and focused gates at this head. [Publication hashes](receipts/public-manifest-verification.json) match all 33 downloaded files represented by the public manifest. Eight round-4 items also match the original SHA256SUMS. The ninth, `run_r4_evidence.sh`, matches the manifest's separately recorded published hash after path redaction. This is explained provenance, not a receipt defect. These are author source-head receipts. No manager source bank exists at this head, and none is claimed or inferred.

**Prior public findings at this head**

| Finding | Disposition | Evidence |
|---|---|---|
| R633-1-F1, restart reuse | Resolved | Reservation survives `die`; original event sequence through published adapter passes; lifecycle models have no overlap |
| R633-1-F2, uncertain update | Resolved | Reservation precedes update and survives uncertainty; applied-timeout and delayed completion pass |
| R633-1-F3, slot-0 fallback | Resolved | 19 CPUs refuse four-container slot 0; 20 supplies the full layout; capacity probes pass |
| R633-1-F4, reap failure skips join | Original fault resolved | Reap failure joins/closes before propagation; K09/K10/K11/K14 killed. Distinct cleanup-entry hole remains F1 |
| R632-1-F1, ineffective join test | Resolved | K10 removes joining and fails eleven arms; independent no-join control sees a live reader |
| R632-1-F2, warning/verdict gap | Resolved | K23/K24 killed; run-level controls retain success/failure verdicts and print warnings |
| R632-1-R1/R2, RESIDUE | Applied/superseded | CI_WORKFLOWS.md:2154 states one-version rule; PR Layout states refusal on every slot |
| R632-1-S1/S2/S3/S4 | Original cases addressed | Reservation lifetime, uncertain updates, reap finalization and removed-before-placement summaries corrected |
| R633-2-F1, original failure replaced | Resolved | Unchanged monitor probe passes; Q01-Q05 killed; signal status and secondary diagnostics preserved after cleanup starts |
| R632-2-F1(a)-(d) | Resolved | Unchanged campaign kills K12, K13, K36 and K32; unmodified self-test passes |
| R632-2-S1 | Addressed | K29/K31 killed: cleanup mask and reader-crash record pinned |
| R632-2-S2 / R632-3-S2 | Retained as MAJOR R633-4-F1 | Deterministic cleanup-entry probe demonstrates the unsatisfied guarantee |
| R632-2-S3 / R632-3-S3 | Optional SUGGESTION retained | Immediate join failure uses bounded-shutdown wording; the hold still prevents teardown. No new blocking classification for this diagnostic wording |
| R632-3-F1, maximum-order arm | Resolved | Q24 killed by `selftest_job_concurrency:7148`; permutations and single-workflow controls pass |
| R632-3-S1 | Optional SUGGESTION retained | Q06/Q11/Q13/Q28/Q29 remain future-regression controls; their implementation is present and was read |

The public inventory contained no submitted reviews or inline review comments beyond the conversation findings checked above. No new RESIDUE item is recorded.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1 | #730 acceptance/decisions; act_ci.py:2044, 4673, 5682, 5835; capacity/derivation and cleanup-entry receipts | R633-4, applied; no clean covering round | 31e53e82a4a1604569ccacba8473f21e70b9cbc0 |
| RTL | UNCLEAN: F1 | Full two-file diff; architecture section 7; act_ci.py:5300, 5549, 5682, 5780; single-writer/teardown ordering | R633-4, applied; no clean covering round | 31e53e82a4a1604569ccacba8473f21e70b9cbc0 |
| Robustness | UNCLEAN: F1 | act_ci.py:5356, 5410, 5446, 5500, 5682; lifecycle, uncertain-move, shutdown and signal-entry probes | R633-4, applied; no clean covering round | 31e53e82a4a1604569ccacba8473f21e70b9cbc0 |
| Tests | UNCLEAN: F1 | act_ci.py:6503, 7085, 7148, 7181, 7416, 7754, 7843, 8016; 498-arm log and both unchanged campaigns | R633-4, applied; no clean covering round | 31e53e82a4a1604569ccacba8473f21e70b9cbc0 |
| Docs | UNCLEAN: F1 | CI_WORKFLOWS.md full diff, especially :1807 and :2146; issue/PR, published receipts/manifests; documentation gates | R633-4, applied; no clean covering round | 31e53e82a4a1604569ccacba8473f21e70b9cbc0 |

**Limits, integrity and pending manager duties**

No live replay, Docker operation, host runner/self-test, privilege, hardware work, source fix, commit, push, GitHub write, author contact or delegated review occurred. No parent/processor/gPTP/synthesis/builder bank ran. Four-wide masks were checked; live container affinity and `nproc` were not measured. Event delivery and daemon timing remain unmeasured. Physical calibration was NOT RUN; field skips are not hardware proof.

The [hosted snapshot](receipts/hosted-checks.json) has three successful completed jobs and ten queued/in-progress jobs. It does not establish the required-context bar. Missing or skipped contexts supply no execution evidence. Hosted/replay acceptance remains the manager's responsibility.

[Integrity verification](receipts/integrity.json) passes all 1301 root entries against the requested tree: raw tracked blob bytes, executable modes and stage-0 index entries. All five gitlinks match. Protocol, gPTP and AXI-Stream checkouts match their required pins and tracked bytes. Unused external/lwSRP checkouts were not used. No nonignored untracked file remains. Candidate files were never edited, so no source restoration was necessary. Disposable files remain under packet `scratch/`, excluded from publication.

The manager must resolve F1 and obtain fresh independent review before treating the PR as clean. The round-4 derivation fix needs no further change on this evidence. Source-head evidence remains distinct from the final current-dev merge candidate: build and validate that candidate, including builder/native banks, and publish receipts at the merge turn. Complete hosted acceptance, obtain explicit merge authorization and run post-merge containment. Under the disk ruling, acceptance 3's same-head verdict comparison, acceptance 4's per-job timing/slot memory measurement and optional acceptance 5 remain post-merge duties. Keep #730 open until retained obligations are discharged.

R633-4 FINISHED
