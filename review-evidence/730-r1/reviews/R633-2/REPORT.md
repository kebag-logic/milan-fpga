[R633] NEGATIVE - exact head 5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646

R633-2, external independent review of issue #730 / PR #731. All five lenses were applied. One MINOR finding remains: a monitor cleanup error replaces an earlier interruption, changing its required exit status and suppressing its diagnostic. Containment and joining succeed in the reproduced case. This is a source-review verdict, not merge authorization.

Head tree: `5cdc1268e31a15c1962a15212e5ace9f9101a207`. Source base and observed live dev: `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`. Reviewed the full `dc4d06cb..5ba8313a` diff and all four commits, plus the `eb566634..5ba8313a` correction delta. Only `scripts/act_ci.py` and `docs/testing/CI_WORKFLOWS.md` change. No workflow, RTL, firmware, testbench, or gitlink changes.

**Public scope and authorities**

The review used AGENTS.md, CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md section 8, the architecture's verification boundary, the submodule integration map, and CI_WORKFLOWS.md's replication, ownership, cleanup, and slot contracts. The public task contract is the [issue body](https://github.com/kebag-logic/milan-fpga/issues/730), [assignment](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131408752), [no-replay ruling](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815), and [round-2 decision](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6132404197). The latter retains the original cleanup guarantees. Acceptance 4 and optional acceptance 5 move after merge; the same-head replay-verdict comparison remains unmeasured.

The independent full-diff pass preceded reading prior public review findings. Those findings and the manager's accepted dispositions were then checked explicitly. No other round-2 report, private author material, management checkout, or lane scratchpad was used. Public scope/evidence snapshots are in [public-scope.json](receipts/public-scope.json) and [public-inventory.json](receipts/public-inventory.json).

**R633-2-F1 | MINOR | Conformance, RTL, Robustness, Tests, Docs**

Artifact: `scripts/act_ci.py:5656` (body unwind followed by unguarded monitor cleanup), `scripts/act_ci.py:5571` (cleanup failure raised), `scripts/act_ci.py:425` and `scripts/act_ci.py:16042` (signal-status versus Refusal handling), `scripts/act_ci.py:7803` (combined-error assertion), and `docs/testing/CI_WORKFLOWS.md:1807` / `:1979`.

Authority/evidence: The assignment retains cleanup guarantees. Round-2 item 4 requires keeping the original failure; the authoritative CI contract explicitly retains `128 + signal` after cleanup. [probe_monitor.py](probe_monitor.py) extracts the exact monitor and return-handling definitions with inert command collaborators. Its body raises the same `TerminationRequest(SIGTERM)` used by the production handler. The stream collaborator proves containment and then raises the documented leader-reaping Refusal. The reader finishes its pending move, the stream ends, the join completes, and the pipe closes. Nevertheless, the context manager propagates the cleanup Refusal instead of the incoming signal. The signal wrapper cannot catch it; the outer Refusal branch returns 2. With successful cleanup, the identical signal produces 143. [Raw receipt](receipts/monitor.log), exit 1, records both controls and the combined failure.

The earlier exception survives only as Python exception context. The normal outer Refusal handler prints only the cleanup message, so this does not retain the interrupted-run status or its diagnostic. A body RuntimeError is similarly replaced. The new standing combined-error test at `:7803` explicitly expects the replacement; its separate signal case at `:7810` never combines a signal with cleanup failure.

Impact: Cancellation is misreported as a setup/resource refusal, and the original failure is hidden from the normal diagnostic. This is a bounded status/diagnostic defect; the probe does not show unsafe teardown or an overlapping range. It changes code behavior and a documented guarantee, so it is not RESIDUE.

Required outcome: After all containment and reader-completion obligations finish, retain an already-propagating interruption/original failure and report secondary cleanup errors without replacing it. With no earlier failure, preserve the cleanup Refusal. Keep the documented signal exit statuses and cleanup-before-teardown behavior.

Verification: Extend the combined-fault controls to an original body failure and each of INT, TERM, and HUP, paired with reaping/join failure. Assert the original disposition, visible secondary cleanup evidence, the completed reader, closed pipe, and contained stream before boundary exit. The existing no-primary reaping-error control must still propagate its Refusal.

**Disposition of prior public findings**

| Finding | Disposition at this head | Evidence |
|---|---|---|
| R633-1-F1, MAJOR, all five lenses | Resolved | `JobCpuRanges.observe` at `:5443` releases on destroy, not die. The unchanged restart sequence now gives A `4-7` and B `8-11`. Standing model checks effective configuration, including stopped containers. |
| R633-1-F2, MAJOR, all five lenses | Resolved | `place` at `:5405` reserves before assignment; `check` reconciles inspect without releasing uncertainty. Applied-then-timeout, delayed completion, and unreadable-inspect probes preserve exclusive reservations. |
| R633-1-F3, MAJOR, all five lenses | Resolved | `job_cpu_ranges` at `:4672` refuses insufficient capacity on every slot. Slot 0 at 19 CPUs refuses four containers; 20 provides the full layout. PR and authoritative docs now state this. |
| R633-1-F4, MAJOR, all five lenses | Join/pipe defect resolved; original-failure preservation remains open as R633-2-F1 | The original reaping-failure probe now joins and closes before propagating that failure. Independent busy-reader controls also pass. Combining an incoming interruption with that failure exposes F1. The remaining severity is MINOR because containment succeeds. |
| R632-1-F1, MINOR, Tests and Docs | Resolved | The busy-reader test and its `joined_before_exit` predicate at `:7681` can fail. The published M13 result is KILLED; independently removing the join leaves a live reader at boundary exit and makes that exact predicate false. |
| R632-1-F2, MINOR, Tests | Resolved | `selftest_cpu_range_warnings` at `:6477` drives a staged container through the run path with success and nonzero workflow exits. Published M16/M17/M23 are KILLED. Independent `execute_workflows` probes preserve PASS/FAILED and print each warning once. |
| R632-1-R1, RESIDUE, Docs | Applied | `CI_WORKFLOWS.md:2141` now states the mixed-version overlap and one-version rule. |
| R632-1-R2, RESIDUE, Docs | Superseded and applied | The current PR Layout row states refusal on every slot and the derived 20/8-CPU thresholds. It no longer describes fallback. |
| R632-1-S1/S2/S3, optional Robustness suggestions | Addressed by the accepted lifecycle/reaping fixes, with F1's remaining qualification | Reservation and shutdown receipts below. |
| R632-1-S4, optional Robustness suggestion | Addressed | `JobCpuRanges.summary` at `:5471` separates containers removed before confirmed placement from containers never seen on their range; the updated measurement instructions read both counters. |

No new RESIDUE or SUGGESTION finding is recorded.

**Executed checks and evidence limits**

The original public [round-1 probe](probe_cpu_ranges_r1.py) was retained byte-for-byte, SHA-256 `87225dfc471e9219cc55b4b750aff38c10577c33fadea98365b78a7b49305df6`, and run unchanged. It stops at the newly required inspect argument before reaching the four defect probes; this is a harness-interface failure, not a product finding. Its [receipt](receipts/original-r1-probe.log) has only local path strings redacted.

The [compatibility copy](probe_cpu_ranges_compat.py) adds that inspect callback, selects the new join helper, and supplies the process PID. All original event sequences, assignment behavior, assertions, limits, and injected failures are unchanged. Its [receipt](receipts/compatible-r1-probe.log) passes all probes, including F1-F4. [probe_compatibility.txt](probe_compatibility.txt) records the adapter boundary.

Additional focused probes:

- [probe_lifecycle.py](probe_lifecycle.py), [receipt](receipts/lifecycle.log): 76,800 seeded daemon/event transitions across ordinary updates, applied-then-timeout, late completion, and unreadable inspect. Delayed, missing, duplicated, and reordered events preserve reservations for configured and pending job ranges. Staging is explicitly excluded from exclusive-job-range claims. Eighty-eight capacity combinations check refusal boundaries.
- [probe_monitor.py](probe_monitor.py), [receipt](receipts/monitor.log): busy reader, normal return, body failure, reaping failure, combined body/reaping failure, signal unwind, combined signal/reaping failure, no-join mutation, and warning-to-verdict wiring. All completion/order controls pass; the combined-error disposition fails as F1 describes. Every created probe thread is joined before the probe exits.
- Static and repeated round-1 controls: 320 disjoint four-wide ranges over slots 0-63, a planted overlap detected, workflow-derived widths `4/1/1/1`, unreadable/too-wide max-parallel refused, and slot-0/slot-3 plan strings checked.

These are inert extractions of selected definitions, not an import or execution of the host runner, its entrypoint, or its self-test. No Docker, act, live signal delivery, daemon timing, or real process-group fault is claimed. The no-join mutation changes only the extracted AST in memory. Source bytes remain unchanged.

[run_gates.py](run_gates.py) ran independent gates concurrently with six workers, each foreground child bounded to eight minutes and all children awaited. [gates.json](receipts/gates.json) records commands, return codes, and times. All eleven repository gates pass: CI contract (2016 items), CI contract self-test (2828 arms), Python idiom, bare-metal scope, docs privacy/routing, doc style, doc paths, TOC, anchors, em-dash (339 controls), and diff whitespace. Markdown dependencies were hash-pinned and installed only in disposable scratch. No heavy build or broad source bank ran.

**Public execution receipts and implementation assessment**

Thirteen round-2 author receipt files from [the published evidence commit](https://github.com/kebag-logic/milan-fpga/tree/01847718a891043d6a5790310a397498c8dc5f17/review-evidence/730-r1/author-r2/receipts/r2) match their published manifest hashes; see [verification](receipts/public-evidence-hashes.json). The runner receipt records 490 passing arms and zero failures. The slot-proof receipt records 44 passing cases. The public mutation tables record all 21 new mutations killed and the earlier join/warning mutations killed. M18 remains limited to the unrun live interrupt gate; four old anchors are inapplicable, not killed. These are author execution receipts, not reviewer reruns or a manager source bank.

The published dry-run receipt uses synthetic head `222222...` and substituted Git/daemon boundaries. It shows the real dry-run output wiring, including slot 0 staging `0-3` with `4-7`, `8-11`, `12-15`, `16-19`, and slot 3 staging `60-63` with `64-67` through `76-79`. It is not evidence of a daemon-free live invocation. The real dry-run still enters its Docker boundary, as the public limitations state.

The derived concurrency matches the pinned [matrix default](https://github.com/nektos/act/blob/v0.2.89/pkg/model/workflow.go#L219) and [stage/job scheduler](https://github.com/nektos/act/blob/v0.2.89/pkg/runner/runner.go#L171). The event filter combines the ownership label and container type with the permitted lifecycle actions, consistent with [documented filter semantics](https://docs.docker.com/reference/cli/docker/system/events/#filtering---filter). Reservation of an uncertain update is conservative even if inspect still shows staging: the request may complete later. No normative acceptance change is needed for that decision.

The full diff leaves memory/swap limits, job concurrency, slot memory cap, endpoint selection, credential isolation, ownership label, and lease gate intact. `execute_workflows` places the monitor around the existing spawn boundary and before container/volume cleanup. The reader uses the existing bounded command helper with its inherited blocked-signal worker path. The production stream termination helper proves group absence before its documented reap failure. These observations support the allocator and containment fixes; they do not cure F1's exception priority.

Four-wide staging and job masks support the intended `nproc = 4` shape. Live affinity and nproc were not measured. No product HDL or clock/reset/CDC/interface change is present; the RTL lens therefore assessed the changed software architecture and lifecycle, using the full two-file diff and `docs/overview/ARCHITECTURE.md:111` to establish that product datapaths are outside this delta.

**Reviewer-owned completion ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #730 acceptance/decisions; act_ci.py:2043, :4672, :5405, :5656; CI_WORKFLOWS.md:1979; F1 | R633-2 applied; no clean covering round | 5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646 |
| RTL | UNCLEAN | Full two-file diff/history; architecture:111; allocator lifecycle, worker command path :5090, monitor unwind :5656, workflow wiring :5749; F1. Product HDL/interfaces unchanged | R633-2 applied; no clean covering round | 5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646 |
| Robustness | UNCLEAN | act_ci.py:5353, :5405, :5443, :5492, :5528; lifecycle, insufficient-capacity, uncertain-update, busy-reader and combined-fault receipts; F1 | R633-2 applied; no clean covering round | 5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646 |
| Tests | UNCLEAN | act_ci.py:6477, :7059, :7371, :7460, :7681, :7779, :7803; public 490-arm and mutation receipts; independent probes and no-join control; F1 | R633-2 applied; no clean covering round | 5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646 |
| Docs | UNCLEAN | Full CI_WORKFLOWS.md delta, especially :1760, :1783, :1807, :1979, :2133; current PR body and public scope/evidence; wording gates; F1 | R633-2 applied; no clean covering round | 5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646 |

**Integrity, limits, and pending manager duties**

[verify_integrity.py](verify_integrity.py) and its [receipt](receipts/integrity.json) prove all 1301 root entries against the exact head: raw tracked blob bytes, file modes, complete stage-0 index, and all five gitlinks, with replacement objects disabled. The initialized protocol, gPTP, and AXI-Stream submodules also match their pinned bytes/modes/index. The external and lwSRP checkouts remain uninitialized; only their gitlink/index identities were verified. No tracked restoration was necessary and no nonignored untracked file remains in the clone.

The [hosted snapshot](receipts/hosted-snapshot.json) shows completed successful selectors, lint, BDD, wire-accountability, docs-check-no-git, four synthesis shard jobs, and one firmware mutation job. Other jobs, including docs, elaboration and all five simulation shards, remain in progress in that snapshot. The physical gPTP context is skipped. This is not a completed required-context bar; a successful cache-backed shard or skipped context is not fresh full execution proof. The manager owns hosted/replay acceptance.

No manager source bank exists at this head and none is inferred. Source validation here is distinct from the final current-dev merge candidate. The manager must validate that candidate, including builder/native banks, and publish its receipts at the merge turn. The manager also owns the outstanding live interrupt/replay acceptance under the disk ruling, the post-merge per-job timing/memory and same-head verdict comparisons, and optional acceptance 5. The partial stopped before replay is not a completed measurement.

No source fix, commit, push, GitHub write, merge, author contact, delegated review, privilege, shared install, hardware work, live replay, host runner/self-test, or broad build bank occurred. Physical calibration was NOT RUN; field skips are not hardware proof. Disposable trees and dependencies reside only under packet `scratch/`, which is excluded from publication.

Resolve F1 and obtain a fresh review of the corrected head before counting these lenses clean. Remaining merge duties include the other independent review, the exact-current-dev candidate bar, explicit maintainer merge authorization, post-merge containment, and retaining #730 open until its deferred acceptance duties are discharged. This report does not authorize merge or claim task completion.

R633-2 FINISHED
