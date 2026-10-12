[R633] NEGATIVE - exact head eb5666349fc20ed3b5437a4357ef097c1231e557

R633-1, external independent review of issue #730 / PR #731. Four MAJOR findings remain. All five lenses were applied; none is clean. This is a source review, not merge authorization.

Head tree: `301ea3a9a3ff9a1e4a4eee40edfd70925982d0cb`. Reviewed both commits and the complete two-file diff from `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`. No workflow, RTL, firmware, or submodule gitlink changed.

**Scope and authorities**

Reconstruction followed AGENTS.md, CONTRIBUTING.md, docs/README.md, the [frozen issue](https://github.com/kebag-logic/milan-fpga/issues/730), [assignment](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131408752), and [no-replay ruling](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815), followed by REQUIREMENTS.md section 8, architecture and submodule authorities, CI_WORKFLOWS.md, the full diff/history, and public executable evidence. Acceptance 4 and optional acceptance 5 are deferred by that ruling. The same-head verdict comparison is unmeasured. The ruling does not waive disjoint ranges, insufficient-CPU refusal, or containment.

**R633-1-F1 | MAJOR | Conformance, RTL, Robustness, Tests, Docs**

Artifact: `scripts/act_ci.py:5391` (`observe`, especially 5401-5406); `scripts/act_ci.py:7035`; `docs/testing/CI_WORKFLOWS.md:1750`.

Authority/evidence: Acceptance 1 requires nonoverlapping concurrent ranges, including restarts under this review's assignment. `die` discards A's reservation without clearing its configured cpuset. A later `start` only increments a statistic. The inert probe sends `create A, update A, start A, die A, create B, update B, start B, start A`. Both live containers then retain `4-7`; the record holds only B and reports no problem. Configuration persists for a stopped container's next start; see the [daemon update implementation](https://github.com/moby/moby/blob/v28.0.0/daemon/update.go#L74). This is a modeled restart, not a claim that a shipping job was observed restarting.

Impact: A range can be reassigned while its former container can resume on it. The summary also misidentifies the resumed container as staging and undercounts concurrent users. The existing event test destroys the dead container before replacement and cannot detect this case. The documentation's exclusive-range claim is false for this lifecycle.

Required outcome: A restartable container must retain exclusive ownership or be proved unable to resume on a released range. Handle delayed lifecycle events consistently; counting `start` alone is insufficient. Correct the summaries and documented guarantee accordingly.

Verification: Add a restart/interleaving control that tracks effective container configuration independently of `held`, and fails this head. Require exclusive ranges throughout death, replacement creation, and restart, not only after the last event.

**R633-1-F2 | MAJOR | Conformance, RTL, Robustness, Tests, Docs**

Artifact: `scripts/act_ci.py:5371` (assignment failure and reservation); `scripts/act_ci.py:2414`; `scripts/act_ci.py:7035`; `docs/testing/CI_WORKFLOWS.md:1780`.

Authority/evidence: Acceptance 1 and the assignment's retained failure guarantees. `place` reserves a range only after CLI success. A timeout is converted to Refusal by `run_docker`, caught as a warning, and leaves the range available. The probe applies A's `4-7` update in the inert daemon, then raises a timeout. It subsequently delivers A's `update` event and creates B. Both live configurations are `4-7`; the event does not reconcile A's missing reservation. CLI containment cannot undo a daemon request already accepted. This distinction already governs the documented post-accept rollback contract at CI_WORKFLOWS.md:1824. The upstream update path applies configuration before returning its response, as shown in the same daemon source linked above.

Impact: A lost/delayed response creates overlapping live assignments. The printed staging explanation and measurement counters can be wrong. The existing failed-update test models rejection without a daemon-side effect, so its passing result does not cover this failure.

Required outcome: Keep an uncertain target reserved until effective state is reconciled or the container cannot use it. A failed command must not establish that the container stayed on staging. Preserve the existing distinction between resource uncertainty and a candidate verdict.

Verification: Exercise update-applied-then-timeout, response loss, and delayed completion while another container is created. Check actual modeled cpusets, reservations, warning accuracy, and unchanged candidate verdict handling.

**R633-1-F3 | MAJOR | Conformance, RTL, Robustness, Tests, Docs**

Artifact: `scripts/act_ci.py:4689`; `scripts/act_ci.py:7009`; `docs/testing/CI_WORKFLOWS.md:1767`; PR body, Layout row.

Authority/evidence: Acceptance 1 explicitly requires a Refusal when the host lacks sufficient CPUs. Neither manager scope decision authorizes a slot-0 exception. With 19 host CPUs and concurrency 4, the exact function returns `()` rather than refusing. The caller consequently runs all containers on staging with no monitor. The new self-test positively requires that fallback; the docs and PR describe it as accepted behavior.

Impact: A supported invocation silently retains the original shared-CPU defect instead of meeting the frozen acceptance criterion. This is an unresolved public contract conflict, not prose residue.

Required outcome: Refuse insufficient capacity in slot 0 as well, or obtain an explicit public acceptance change before treating this behavior as compliant. Align tests and documentation with the settled rule.

Verification: Test slot 0 below, at, and above the derived capacity boundary, including hosts below four CPUs. At the present four-container setting, 19 CPUs must refuse and 20 must yield four disjoint job ranges plus staging.

**R633-1-F4 | MAJOR | Conformance, RTL, Robustness, Tests, Docs**

Artifact: `scripts/act_ci.py:5436`; `scripts/act_ci.py:4934`; `scripts/act_ci.py:7165`; `docs/testing/CI_WORKFLOWS.md:1786`.

Authority/evidence: The assignment retains cleanup/Refusal guarantees, and the new documentation promises containment and reader joining on every exit before Docker teardown. `stop_job_cpu_range_monitor` calls `terminate_group` before any protected reader-finalization block. The production termination helper explicitly raises Refusal when leader reaping fails. The inert probe injects precisely that documented failure: the refusal escapes with no reader join and the pipe open. Existing monitor tests always make the termination collaborator succeed, including their body-exception case.

Impact: The outer Docker boundary may unwind while the reader is still running its separately tracked update command or consuming buffered events. Returning a refusal does not make concurrent teardown safe. This is a fault-path reproduction; no real process group or daemon was started to trigger a reaping failure.

Required outcome: Cleanup errors must not bypass the reader completion/dead-thread proof or stream containment obligation. Preserve the original failure while preventing boundary teardown until those obligations are satisfied.

Verification: Inject poll, termination/reap, and join failures with a reader whose completion is independently observable. Assert that neither normal return nor exceptional propagation reaches Docker teardown while it can still issue updates. Retain ordinary exit, body-exception, startup failure, and signal-path coverage.

**Independent checks and evidence**

[probe_cpu_ranges.py](probe_cpu_ranges.py) AST-extracts selected exact-head definitions and supplies inert collaborators. It never imports or launches the runner, executes its self-test, starts a subprocess through candidate code, or uses Docker. Run `python3 probe_cpu_ranges.py <checkout>`. [Raw probe output](receipts/probe.log) returns 1 for the four reproduced invariant violations. Other controls pass: 320 disjoint four-wide ranges over slots 0-63, a planted overlap detected, nominal four-container assignment, death/destruction reuse, foreign/malformed events, shipping workflow derivation (4/1/1/1), and unreadable/too-wide max-parallel refusals. The slot-0 and slot-3 plan strings are checked separately from a full dry run.

The concurrency model was compared with [the pinned scheduler](https://github.com/nektos/act/blob/v0.2.89/pkg/runner/runner.go#L171) and [its default matrix width](https://github.com/nektos/act/blob/v0.2.89/pkg/model/workflow.go#L219). Event filtering matches the documented [AND/OR filter semantics](https://docs.docker.com/reference/cli/docker/system/events/#filtering---filter). Static four-wide masks support the intended `nproc` shape; live affinity and `nproc` were not measured. Static inspection of `execute_workflows` at 5619-5662 confirms that placement warnings do not replace the workflow return code. The unchanged command builder retains memory/swap limits and the ownership label, and the existing lease gate still precedes each spawn. The monitor uses the slot's existing command context, so no new credential or endpoint input is introduced. These observations do not cure F1-F4.

Locally executed gates passed: CI contract (2016 items), CI contract self-test (2828 arms), Python idiom ratchet, bare-metal scope, documentation privacy/routing, documentation style, document paths, TOC, fragment anchors, em-dash controls (339 arms), and diff whitespace. Each has a separate raw log and return-code receipt. The initial TOC attempt refused because the pinned renderer was absent; the successful rerun used hash-pinned dependencies installed only in disposable scratch. No broad RTL, synthesis, firmware, or builder bank ran.

The [published author evidence](https://github.com/kebag-logic/milan-fpga/tree/b5cf83a079c91288af7296dc37ec5d46da58b7be/review-evidence/730-r1) was read only after the independent diff pass. Six receipt files match their published SHA-256 manifest; see [hash verification](evidence-hash-verification.json). The runner log records 477 passing arms and zero failing arms; the slot-proof log records 44 passing cases. These are author execution receipts, not reviewer reruns or a manager source bank. The published dry-run fixture uses synthetic head `222222...` and substituted boundaries; it demonstrates output wiring, not a live daemon-free invocation. The interrupted before replay is not the required performance measurement. Ten claimed mutants have no individual raw receipts in the provided published receipt set, so they are not independently credited here.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #730 acceptance and decisions; act_ci.py:2038, 4669, 5306, 5427; F1-F4 | R633-1, applied; no clean covering round | eb5666349fc20ed3b5437a4357ef097c1231e557 |
| RTL | UNCLEAN | Full two-file diff; architecture section 7; software allocation lifecycle, worker containment, call wiring at act_ci.py:5619 and 5679; F1-F4. HDL/CDC/interfaces unchanged | R633-1, applied; no clean covering round | eb5666349fc20ed3b5437a4357ef097c1231e557 |
| Robustness | UNCLEAN | act_ci.py:5329, 5371, 5391, 5427, 4689; restart, post-accept timeout, insufficient capacity, shutdown-failure probes; F1-F4 | R633-1, applied; no clean covering round | eb5666349fc20ed3b5437a4357ef097c1231e557 |
| Tests | UNCLEAN | act_ci.py:6847-7230 and 13374-13452; published runner/slot receipts; independent controls and missing lifecycle/failure cases; F1-F4 | R633-1, applied; no clean covering round | eb5666349fc20ed3b5437a4357ef097c1231e557 |
| Docs | UNCLEAN | Full CI_WORKFLOWS.md diff; public issue, PR and evidence; correctness claims at 1750, 1767, 1780, 1786; documentation gates; F1-F4 | R633-1, applied; no clean covering round | eb5666349fc20ed3b5437a4357ef097c1231e557 |

No RESIDUE or SUGGESTION finding is recorded. The documentation issues above change behavioral, measurement, or guarantee claims and therefore do not qualify as wording-only residue.

**Prior public findings**

The independent verdict and ledger above were written before the final public-finding check. [The read-only inventory](receipts/prior-public-inventory.json) found two PR conversation comments, both review-start notices; zero submitted reviews; zero inline review comments; and the five issue comments already used for scope/evidence. There are no prior public review findings to resolve or retain at this head. No other reviewer's report was read.

**Limits, integrity, and pending manager duties**

The [hosted snapshot](receipts/hosted-snapshot.json) contains successful `full-ci-gate` and `docs-check-no-git`, an in-progress docs job, queued elaboration/fast/full workers, and a skipped physical gPTP job. It is not a completed required-context bar. A skipped context is not executed coverage. No manager source bank exists at this head and none is inferred. Source validation and the manager's future current-dev merge-candidate validation are distinct.

No live replay, host runner/self-test, privileged operation, shared installation, source edit, commit, push, GitHub write, hardware work, or delegated review occurred. Physical calibration was NOT RUN; field skips are not hardware proof. Restart and transport-failure probes use explicit inert models; they establish the bookkeeping response to those cases, not live daemon timing.

[verify_integrity.py](verify_integrity.py) verifies raw tracked blob bytes, modes, and stage-0 index entries against the exact head, with replacement objects disabled. Its [receipt](receipts/integrity.json) passes 1301 root entries plus the initialized protocol, gPTP, and AXI-Stream submodules at their required gitlinks. All five root gitlinks match; the unused external and lwSRP checkouts remain uninitialized. No tracked restoration was necessary and no nonignored untracked file remains in the clone. Disposable files are confined to packet scratch.

The manager must obtain fixes and fresh independent review, publish candidate receipts when available, validate the then-current dev merge result including builder/native banks, own hosted/replay acceptance under the disk ruling, obtain explicit merge authorization, and perform post-merge containment. Acceptance 4's job timing/memory comparison and optional acceptance 5 remain pending after merge. Keep #730 open until its retained duties are discharged.

R633-1 FINISHED
