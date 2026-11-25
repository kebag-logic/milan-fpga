[R924] POSITIVE - exact head b0f2bc1a784d9f006204491c883ac2b1783e970a

R924-3, external independent review of issue #998 / PR #1003. Both round-2 functional findings are resolved. All five lenses are CLEAN for this narrow re-review. One new wording-only RESIDUE and four retained optional suggestions are recorded below. This is a source-review verdict, not merge authorization.

## Scope and provenance

Reviewed tree: `bb0c6d59a6e22c499de562a642978b73c998c653`. Source base: `fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f`, stacked on #1001. This round judges only the three commits `468c7e47`, `222362ff`, `b0f2bc1a` after `9c62539365fea8316dae2b9fd7c68defeff5cb31`, their dependencies, and the named prior findings. The delta has eleven paths; unchanged earlier code keeps its prior disposition.

Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, [issue #998](https://github.com/kebag-logic/milan-fpga/issues/998) and public scope records, REQUIREMENTS.md:326-335, the CI/testing authorities, then diff/history and executable evidence. The issue-comments API still returns zero comments. The [PR description](https://github.com/kebag-logic/milan-fpga/pull/1003) records the scope rulings; [#1008](https://github.com/kebag-logic/milan-fpga/issues/1008) separately records untouched long jobs and watcher/physical-job exceptions. This review uses the previously accepted touched-job timing scope, not a claim that every hosted job now meets 30 minutes.

Prior public findings were read after the independent delta pass. `independent-verdict.md` records my verdict and ledger before reading the other prior reviewer's report. No current parallel review, private author material, management source bank or lane scratchpad was read. The [review-start record](https://github.com/kebag-logic/milan-fpga/pull/1003#issuecomment-7155376325) binds this round to the requested head.

## Round-2 findings and residues

### R924-2-F1 - RESOLVED - Conformance, Robustness, Tests, Docs

Artifacts: `.github/ci-templates/rtl-fast.yml:583`, `.github/workflows/rtl-fast.yml:1154`, `scripts/ci_events.py:1366`, `:3889`, `:8408`; `cancellation-probe.log`, `generation-check.log`, `event-check.log`, `fork-controls.log`.

The template, generated matrix, contract constant and negative controls now agree on explicit `fail-fast: true`. The production contract passes 2,378 items. The focused probe executes all seven standing boundary-leg mutation arms and independently sets cancellation false or removes the key; each bad strategy is refused. Omitted-leg, missing-dependency, raised-deadline and extra-leg controls also fail for their intended reasons. Generation checking passes.

The failed-fork mechanism is native matrix cancellation. The service cancels queued/running siblings after a non-tolerated matrix failure; it requires no cancellation step or write-token grant. This follows the [GitHub matrix failure contract](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations#handling-failures). Neither capture leg has `continue-on-error` or a new permission grant. Both write-enabled observer jobs retain their same-repository event guards (`rtl-fast.yml:1691`, `:1760`); fork controls report zero writes.

The judge still depends on the capture matrix. Executing the actual aggregate shell body gives exit 0 for successful captures/judge and exit 1 for failed, cancelled or missing capture results with a skipped judge. No hosted fork failure was injected; live cancellation is supported by the native configuration and service contract, not claimed as an observed injected failure.

### R923-2-F1 - RESOLVED - Conformance, RTL, Robustness, Tests, Docs

Artifacts: `tb/verilator/follow_ring/Makefile:133`, `:158`; `follow_ring_make_probe.sh`, `make-head.log`, `make-old.log`, `build-pullin-small-{head,old}.log`, `exec-no-rebuild.log`, `output-spotcheck.log`.

Both fine-build recipe lines now start with `+`. The published original probe was adapted only to select the requested head; its previous-head control is also retained. Under make 4.4.1's pipe jobserver:

| Probe | Previous head 9c625393 | Reviewed head b0f2bc1a |
|---|---|---|
| `make -n run` versus base | DIFFERS | IDENTICAL |
| `small-pullin` jobserver warnings | 1 | 0 |
| `build-pullin-small` jobserver warnings | 1 | 0 |

The probe base `13e6d869` has exactly the source base's follow_ring Makefile. Host-dependent extraction paths alone were replaced with `ROOT` before byte comparison. `exec-pullin-small` with empty `LEG_BUILD` still emits only execution commands, with no build or glue-generation command. Its three-case inventory is unchanged.

The make probe deliberately uses a no-op compiler; the subsequent missing-model failure is expected and supplies no simulation verdict. Real execution support comes from published local piece receipts and two downloaded hosted union artifacts. All three complete case outputs match their recorded SHA-256 values in both local heads and both hosted logs: twelve log-to-digest matches, with identical output bytes. No simulation was rerun here.

### Wording residues from round 2 - RESOLVED - Docs

| Item | Exact-head disposition |
|---|---|
| R924-2-R1 | All named new explanation blocks cite Issue #998 and REQ-VER-01/04: follow_ring Makefile and output-order comments; capture template; ctrl_boundary/configs/runs; ci_events leg/setup/check/control comments. Added source comments contain no new bench-lane label, lane name, review round, reviewer identity or issue-comment ID. Existing neighboring labels are unchanged and outside this delta. |
| R924-2-R2 | `sw/firmware/ctrl/README.md:631` uses the requested sentence distinguishing transferred standalone builders from retained owned-image builders, stack gate and controls. It agrees with `ctrl_boundary.py:534-541` and the published judge receipt. |
| R923-2-R1 | `docs/testing/CI_WORKFLOWS.md:651` points the derivation table to PR #1003's description, where it exists. No figure changed. |

## New wording residue

### R924-3-R1 - RESIDUE - Docs

**Artifact:** PR #1003 description, section "How a failed capture leg cancels its sibling on a fork", second bullet; retained in `pr-wording-and-scope.json`. Compare `.github/workflows/rtl-fast.yml:1695`, `:1767` and `docs/testing/CI_WORKFLOWS.md:3552`.

**Authority/evidence:** The description calls the watcher "the only job with a write token". The existing terminal job `ci-cancel-tail` also requests `actions: write`, under the same fork exclusion. The policy correctly names both guarded jobs.

**Impact:** An overbroad noun phrase only. The actual guards, permissions, cancellation mechanism, measurements, tests and verdicts are unchanged; no privacy rule is implicated.

**Required outcome / exact fix:** Replace "the only job with a write token" with "one of the two guarded jobs requesting actions: write". Optionally name the terminal job in the same sentence.

**Verification:** Compare the corrected sentence with both permission blocks and event guards. This residue leaves no lens unclean and belongs on the manager's residue checklist.

## Earlier dispositions and retained suggestions

The prior [R924-2](https://github.com/kebag-logic/milan-fpga/pull/1003#issuecomment-7152865926) and [R923-2](https://github.com/kebag-logic/milan-fpga/pull/1003#issuecomment-7153013473) findings were reconciled, including retained earlier items.

| Prior item | Disposition at this head |
|---|---|
| R924-1-F1; R923-1-F1 | RESOLVED disposition retained. The repaired slot-lock/root-proof implementation and callers are unchanged by these commits; no staging dependency is altered. No new staging campaign is claimed. |
| R923-1-F2 | RESOLVED under the recorded touched-job ruling. Every touched job again finishes below 30 minutes; maximum worker 25.000 minutes. Untouched long jobs remain #1008. |
| R924-1-R1; R923-1-R1/R2/R3 | RESOLVED disposition retained. Their attribution, staging-path and qualified watcher wording remain intact; the PR's duplicate phrase remains removed. |

**R923-2-S1 / R923-1-S1 - SUGGESTION - Tests, Docs.** Artifact: `scripts/ci_make_cases.py:151`. Authority/evidence: shared frame output serializes execution in measured start order, unchanged here. Impact: optional clarity about the final writer; no demonstrated output defect. Required outcome if adopted: state that order or retain driver order for that mode. Verification: a deliberate multiwriter case and its final output.

**R923-2-S2 / R923-1-S2 - SUGGESTION - Robustness.** Artifacts: `scripts/ci_suite_workflows.py:76`, capture job at `rtl-fast.yml:1148`. Authority/evidence: both jobs inherit the existing permission pattern and introduce no new token. Impact: optional least-privilege clarity. Required outcome if adopted: explicit `permissions: {contents: read}`. Verification: regeneration and fork controls. This is distinct from R924-3-R1's wording correction.

**R923-2-S3 / R923-1-S3 - SUGGESTION - Docs.** Artifact: `docs/testing/CI_WORKFLOWS.md:500` and PR queue limitation. Authority/evidence: preflight can run beside workers only when runner capacity permits. Impact: scheduling qualification; no start-priority guarantee. Required outcome if adopted: qualify the policy wording. Verification: support any scheduling improvement with queue/start timestamps.

**R923-2-S4 - SUGGESTION - Docs.** Artifact: PR derivation table, `milan_dp__1`. Authority/evidence: rounded displayed walls reproduce 1152, while the unchanged conservative figure is 1153 from unrounded walls. Impact: exact reproduction from presentation precision only. Required outcome if adopted: publish sufficient wall-time precision. Verification: recompute the ceiling from those published values. No figure reduction is requested.

## Evidence and hosted minutes

The [author-r8 publication](https://github.com/kebag-logic/milan-fpga/tree/22b3d7ad1e8bca3a5b783af5c8bd2446edc2cc9a/review-evidence/cicd3-r1/author-r8) contains 107 files. Every file matches its `published_sha256`, with no missing or unlisted file in that directory. Three files are marked path-redacted. `verify_public.py` checks local receipt identities, inventories and complete result objects as well as publication hashes. The gate summary records 37 commands, all rc 0, including 5,968 event-control arms. These are author executions; this reviewer reran only generation, event checking, fork controls and focused probes.

Published follow_ring measurements, prior to current head: leg 0 wall 351.36 to 350.73 seconds, user CPU 463.95 to 463.51 seconds; leg 1 wall 472.07 to 464.87 seconds, user CPU 1386.15 to 1365.19 seconds. All case outputs remain identical. Cancellation is a policy restoration, not a new speed-up measurement or measured fork-cancellation latency claim.

`read_hosted.py` reads all jobs pages for the four fixed run IDs, verifies their source head, and computes elapsed minutes from API timestamps. All four runs succeeded on attempt 1. All seven required contexts executed successfully, not merely as skipped contexts.

| Hosted observation | Minutes / result |
|---|---|
| [45550366444](https://github.com/kebag-logic/milan-fpga/actions/runs/45550366444), capture 0 / capture 1 / judge | 15.267 / 10.983 / 5.050, success |
| [45550366428](https://github.com/kebag-logic/milan-fpga/actions/runs/45550366428), preflight | 1.950, success |
| Same run, all 26 workers | Maximum 25.000; five minutes below 30; all success |
| Same run, indivisible continuous-media-clock worker | 14.100, success |
| Same run, eight unions | 0.233 to 0.500, all success |
| Same run, exhaustive aggregates | 0.500 / 0.200, success |
| [45550366332](https://github.com/kebag-logic/milan-fpga/actions/runs/45550366332), elaboration context | Executed successfully |
| [45550366343](https://github.com/kebag-logic/milan-fpga/actions/runs/45550366343), three documentation contexts | Executed successfully |
| Nightly/manual physical job | SKIPPED, no execution duration claimed |

Untouched jobs exceeded 30 minutes: firmware-control-mutants 30.100, firmware-srp-mutants 30.467, publication-census 36.700. These are #1008 work. Watchers span their runs by design. No universal future runner-speed guarantee follows from these observations.

The downloaded union artifacts identify actual hosted merge `c5327b2517399ed2bff51ed8959ba713babc8b63`, tree `c79ebe1d2f98b4056b8bae45009f54e1cb26a400`, with parents `e608f8d82a88bca8b3996677ff4113aef353ce88` and the reviewed head. The comparison run used the same base and previous reviewed head. API parent checks and byte-level output comparisons are retained. The author's broader 8/8 receipt-table and 65/65 verdict-set comparison was inspected, not independently recomputed in full.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #998/#1008; REQUIREMENTS.md:326-335; rtl-fast.yml:1154; follow_ring Makefile:133,158; cancellation-probe.log; make-head.log; hosted-minutes.tsv | R924-3 | b0f2bc1a784d9f006204491c883ac2b1783e970a |
| RTL | CLEAN | Eleven-path delta with no production RTL/firmware/harness assertion/gitlink change; follow_ring recursive-build and empty LEG_BUILD interfaces; exec-no-rebuild.log; tree-integrity.json | R924-3 | b0f2bc1a784d9f006204491c883ac2b1783e970a |
| Robustness | CLEAN | ci_events.py:3889; matrix/judge/aggregate dependencies; both write-job guards; cancellation-probe.log; fork-controls.log; old/head pipe-jobserver probes | R924-3 | b0f2bc1a784d9f006204491c883ac2b1783e970a |
| Tests | CLEAN | ci_events.py:8408 seven fault arms; generation/event/fork controls; both recipe probes; prior-head failing control; output-spotcheck.log; public-verification.log | R924-3 | b0f2bc1a784d9f006204491c883ac2b1783e970a |
| Docs | CLEAN; R924-3-R1 nonblocking | CI_WORKFLOWS.md:119,124,651,2484,3552; ctrl/README.md:631; changed explanation blocks; PR wording; publication index/gate/hosted receipts | R924-3 | b0f2bc1a784d9f006204491c883ac2b1783e970a |

Each lens was applied to the delta and relevant dependencies. This ledger preserves earlier accepted work rather than claiming a fresh full-bank or hardware review. No open MINOR, MAJOR or BLOCKER remains from the assigned findings.

## Reproduction, limits and pending manager duties

Portable scripts accept the checkout or packet directory: `probe_cancellation.py CHECKOUT`, `verify_public.py CHECKOUT`, `verify_tree.py CHECKOUT`, `read_hosted.py PACKET`, `spotcheck_outputs.py PACKET`, and `sh follow_ring_make_probe.sh CHECKOUT PACKET/scratch/PROBE`. The output spot-check uses published local files and downloaded union logs held under scratch; its twelve matched hashes and three current hosted case outputs are publishable receipts. `PROBE_REVS='base:13e6d869d8 head:9c62539365'` reproduces the old make failure. `focused-commands.txt` records additional commands and outcomes.

- Carry R924-3-R1 to the residue checklist; retained suggestions are optional. Complete the other independent review before any merge.
- Publication checksum verification succeeded. The publication commit is unsigned (`publication-signature.json`, API `verified: false`, reason `unsigned`), and no detached signature was supplied. This establishes content/source binding, not authenticated author-signature verification.
- Source evidence consists of author receipts, inspected hosted executions and focused reviewer probes. No manager source bank at this exact head is claimed or inferred. No full parent, processor, synthesis or builder bank was run here. The full serial sweep was not rerun.
- The pinned simulator identified itself as version 5.050 before any possible use; only its version query ran. Make 4.4.1's pipe mode was exercised; published make 4.3 evidence was inspected but not re-executed. No model was built by these probes.
- Hosted/local-replica acceptance remains the manager's duty. No container replay or host CI orchestrator/self-test ran. No GitHub write, source fix, commit, push, merge, author contact, privilege change or hardware operation occurred.
- At the merge turn, validate the candidate against then-current remote dev, including builder/native banks, and link receipts. The supplied live-dev reference is `e275d7950ef3385753e6a15d2e191ba855b171ed`; source base remains `fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f`. The inspected hosted merge into `e608f8d8` is not that final candidate. Retain the prior image-audit provenance limitation; this delta supplies no refreshed image audit.
- Physical calibration was NOT RUN. The physical-job skip and field skips are not hardware proof. Release obligations remain separate.
- Final raw-byte verification covers all 1,974 superproject entries and 1,362 entries across five initialized submodules, including modes, index equality, registered roots and exact gitlinks, with replacement objects disabled. Required pins match; the unused external submodule is uninitialized. No tracked restoration was necessary. Disposable trees stayed under this packet's scratch directory.
- Merge requires explicit maintainer authorization, completed independent reviews, candidate validation and required evidence. Post-merge containment and issue/project completion remain pending.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable. Scratch is excluded.

R924-3 FINISHED
