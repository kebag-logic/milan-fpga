[R633] POSITIVE - exact head b341e875d87c6aa2be355bad17f373782517f723

R633-7, external independent review of issue #730 / PR #731. All five lenses were applied to the complete change and are CLEAN. No BLOCKER, MAJOR or MINOR remains. One publication-wording RESIDUE and the explicitly retained optional suggestions below remain. This is a source review, not merge authorization or completion of the deferred measurement.

Reviewed tree: `82915e6c72b793bdf50a3b615afa5b03a6883c07`. Source base: `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`. The full diff changes only `scripts/act_ci.py` and `docs/testing/CI_WORKFLOWS.md`. The round-seven delta from `73b8dcd667aa5bf1254e828dd1dd7217c8a103ce` adds 79 test lines. AST comparison confirms that only `selftest_act_signal_window` changes and `act_interrupt_signal_case` is added; existing runtime definitions are identical ([static receipt](receipts/static-checks.json), [full diff](full.diff)).

The review began with AGENTS.md, CONTRIBUTING.md and docs/README.md, then the [frozen issue](https://github.com/kebag-logic/milan-fpga/issues/730), [assignment](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131408752), [disk ruling](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815), and the public round decisions through [round seven](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6138356353). Relevant authorities are REQUIREMENTS.md:307 (REQ-VER-01 through REQ-VER-06), CI_WORKFLOWS.md's replication/slot contracts, architecture section 7, and the submodule integration map. The complete diff and history received an independent pass before prior public finding comments were read. Public executable scripts and receipts were used; no private author material or separately hosted reviewer REPORT file was used as authority.

The ruling defers acceptance 4 and optional 5 until after merge. Acceptance 3's live `nproc` and same-head verdict comparison remain unmeasured. Offline four-wide range checks and warning/status checks discharge their narrower code claims, not that live comparison.

[R633] PASS Conformance - `scripts/act_ci.py:2090`, `:2119`, `:4671`, `:4719`, `:5918`; issue #730 acceptance 1-3 - the materialized workflow mappings determine concurrency, using the maximum over the selected workflows and the sum of the widest allowed concurrent jobs. Unsupported `max-parallel` values and insufficient CPUs refuse before slot entry, including slot 0. Slot N's fixed block is `20N..20N+19`; staging and assigned job ranges are four wide. The [pinned scheduler](https://github.com/nektos/act/blob/v0.2.89/pkg/runner/runner.go#L171), [default matrix width](https://github.com/nektos/act/blob/v0.2.89/pkg/model/workflow.go#L219), and [executor minimum](https://github.com/nektos/act/blob/v0.2.89/pkg/common/executor.go#L95) support the concurrency bound. Workflow bytes and resource limits are unchanged. No protocol clause or product behavior changes.

[R633] PASS RTL - `scripts/act_ci.py:5380`, `:5574`, `:5610`, `:5675`, `:5818`, `:15927`; `docs/overview/ARCHITECTURE.md:111`; full diff - hardware/CDC/firmware/interface artifacts are unchanged. The software architecture retains one allocator writer, reads its result after joining, uses the existing per-slot command context, and reuses the established process-group containment ladder. The ownership-label filter agrees with the documented [event filter semantics](https://docs.docker.com/reference/cli/docker/system/events/#filtering---filter). Remote-head checks, integrity checks, the pre-spawn lease gate, owned-resource cleanup and absence refusals remain wired around the new monitor. The live interrupt gate's added monitor integration was inspected, not executed.

[R633] PASS Robustness - `scripts/act_ci.py:5435`, `:5462`, `:5492`, `:5527`, `:5586`, `:5626`, `:5733`, `:5333`; lifecycle, shutdown and signal receipts - reservations precede the update and survive `die`, rejection, timeout and unreadable placement. Only removal releases them. Restarts and late updates cannot reuse a reserved job range. The monitor holds cleanup signals across its yield-to-finalization transition; its reader inherits the mask. The real act boundary reopens signals, preserves an active failure at closing, and restores the hold. Stream containment, reader completion/dead-thread checks and pipe finalization precede outer teardown. The probes exercise the ordinary, failed-reap, failed-join, held-reader, startup, malformed-event and interrupt paths. Model evidence does not establish live daemon latency.

[R633] PASS Tests - `scripts/act_ci.py:7171`, `:7268`, `:7502`, `:7591`, `:7947`, `:8120`, `:8334`, `:12466`, `:12476`, `:12649`, `:14962`; executable receipts below - all 531 standing arms pass. The six new cases use the real monitor and normal boundary, a real reader, and inert external collaborators. They require exact conventional stderr, `128 + signal`, delivery during act or before it starts, restored masks, and completed cleanup. S8 fails all six new named arms. Earlier required mutation outcomes remain intact; optional survivors are disclosed rather than counted as kills.

[R633] PASS Docs - `docs/testing/CI_WORKFLOWS.md:1746`, `:1760`, `:1773`, `:1803`, `:1813`, `:1838`, `:2180`; public issue and PR body - the documentation describes staging, persistent reservations, inspect-confirmed placement, insufficient-capacity refusal, masked cleanup, exact precedence diagnostics and mixed-version slot overlap. It separates deferred live measurement from offline proof. R632-5-R1/R2 are applied. The remaining PR Status wording is R633-7-R1 below and changes no technical claim.

Executed evidence is recorded in [execution.json](receipts/execution.json), with separate raw logs and return-code files. Candidate code ran only inside disposable, unprivileged namespaces with an isolated process tree/network, empty environment, no host home and no daemon socket. The three unchanged campaign drivers ran concurrently with `--jobs 5`, `--jobs 5`, and `--jobs 3`; baseline and focused lanes kept the maximum at 15 candidate jobs. The foreground driver joined every worker. No full parent, processor, gPTP, synthesis or builder bank ran.

| Check / receipt | Observed result |
|---|---|
| [Complete runner self-test](receipts/runner-selftest.log) | rc 0; 531 ok, 0 FAIL, PASS |
| [R632-6 unchanged campaign](receipts/mutants_r632_6.log) | rc 0; 8/10 killed; S8 rc 1 with six named FAIL arms; S5/S6 survive; no bad anchors |
| [R632-2 unchanged campaign](receipts/mutants_r2.log) | rc 0; 36/36 killed, including K12/K13/K32/K36; K10 missing join fails 41 arms, K11 join-before-containment fails 40 |
| [R632-3 unchanged campaign](receipts/mutants_r3.log) | rc 0; 24/30 killed; Q24 killed by the workflow-order arm; Q06/Q11/Q13/Q15/Q28/Q29 survive; no bad anchors |
| [Unchanged interrupt diagnostic probe](receipts/probe_r6_interrupt_diag.log) | rc 0; six cases, exact conventional diagnostic only |
| [Unchanged cleanup-entry probe](receipts/probe_cleanup_entry.log) | rc 0; six cases, stream contained, reader ended and pipe closed before outer teardown |
| [Unchanged boundary-precedence probe](receipts/probe_boundary_precedence.log) | rc 0; nine cases preserve the original Refusal/status 2 and complete cleanup |
| [Earliest closing restore variant](receipts/first-restore.log) | rc 0; nine cases. Explicitly targets the first nested restore; the unchanged probe now selects the outer restore |
| [Round-one byte-unchanged probe](receipts/probe_cpu_ranges_r1.log) | rc 1: constructor setup incompatibility (`read_cpus` is now required), not an invariant verdict |
| [Published round-one compatibility adapter](receipts/probe_cpu_ranges_compat.log) | rc 0; unchanged event sequences and fault cases, zero contract violations |
| [Lifecycle probe](receipts/probe_lifecycle.log) | rc 0; four fault modes, each 64 seeds x 300 transitions; 88 capacity combinations |
| [Lifecycle/derivation/layout probe](receipts/probe_r3.log) | rc 0; 200 seeds x 400 transitions; selected-order and differing-checkout derivation; 320 disjoint ranges over 64 slots |
| [Monitor probe](receipts/probe_monitor.log) and [shutdown probe](receipts/probe_shutdown.log) | rc 0; first-failure precedence, warning/verdict independence, retry and hold; planted missing join fails the independent observation |
| [Offline dry-run transcript](receipts/offline_dryrun.log) | rc 0; slot 0 staging `0-3`, jobs `4-7 8-11 12-15 16-19`; slot 3 staging `60-63`, jobs `64-67 68-71 72-75 76-79` |
| [CI contract](receipts/ci-events-check.log), [its controls](receipts/ci-events-selftest.log), [slot controls](receipts/slot-proof.log) | all rc 0; 2016 items, 2828 arms, 44 cases |
| [Diff / source checks](receipts/static-checks.json) | whitespace clean; both author source digests match the reviewed blobs |

The local interpreter is CPython 3.14.7 with PyYAML 6.0.3 ([environment](receipts/environment.json)). The per-step signal arm records 185 steps, each targeted both thread-locally and process-wide. The author's CPython 3.12.3 receipt records 198 steps; the PR correctly says this count depends on the interpreter. The 18 real-boundary closing cases cover both restores, all three signals, and no failure/Refusal/RuntimeError. Four-wide masks support the intended `nproc = 4` shape; no live `nproc` measurement was made.

[Public-input digests](receipts/public-inputs.json) establish that the required historical scripts were rerun byte-unchanged, except for the separately identified adapter and earliest-restore variant. The wrapper, source-export script and foreground driver are included for reproduction: run `python3 scripts/prepare_tree.py <exact-head-checkout>` in a fresh packet, then `python3 scripts/run_review.py`. Scratch trees are never publication artifacts. Per-mutant stdout, stderr and return codes are included under `receipts/mutant-logs/`.

The [published author receipts](https://github.com/kebag-logic/milan-fpga/tree/16c2f70eb7da6161d1aceddb57b09ddd540b801f/review-evidence/730-r1/author-r7/receipts/r7) were examined separately. Thirty-four selected blobs were verified against their published Git object IDs ([retrieval](receipts/author/retrieval.json)). Their [source manifest](receipts/author/source-manifest.json) matches this exact head's two changed files. The [code-gate results](receipts/author/code-gates/results.json) and [documentation-gate results](receipts/author/docs-gates/results.json), together with their raw logs, report successful runner, contract, slot, idiom, scope, privacy/routing, style, TOC, anchors, em-dash, path and whitespace checks. These are author source-head receipts; they are not a manager source bank or a validated merge candidate.

Prior public findings were reconciled against this head, preserving their original lens ownership:

| Finding(s) | Disposition and evidence at this head |
|---|---|
| R633-1-F1; R632-1-S1 | RESOLVED: reservation lasts through `die` and restart; `observe` at :5527; exact restart sequence, randomized lifecycle probes, K01 |
| R633-1-F2; R632-1-S2 | RESOLVED: reserve before update and retain uncertain targets; `place` at :5492; applied-timeout/late/unreadable controls, K02/K03/K07/K08 |
| R633-1-F3 | RESOLVED: `job_cpu_ranges` at :4719 refuses insufficient capacity on every slot; 19/20-CPU and smaller-host controls, K15 |
| R633-1-F4; R632-1-S3 | RESOLVED: `stop_job_cpu_range_monitor` at :5610 completes independent cleanup obligations after reaping failure; compatibility and monitor probes, K09-K11/K14 |
| R632-1-F1 (Tests, Docs) | RESOLVED: busy-reader standing controls fail without joining; K10/K11 and independent missing-join control |
| R632-1-F2 (Tests) | RESOLVED: `selftest_cpu_range_warnings` at :6589 pins printed warnings and both successful/failed workflow outcomes; K23/K24 |
| R633-2-F1 | RESOLVED: primary failure preserved, secondary failures printed; :5664 and :5767, monitor/shutdown controls and Q-series |
| R632-2-F1 (Tests) | RESOLVED: K12/K13/K32/K36 all killed by named arms; retry, bounded hold, event timestamp and first-failure claims are distinguishable |
| R632-3-F1 (Tests) | RESOLVED: all selected-workflow orders graded; Q24 killed |
| R633-4-F1; R632-2-S2 / R632-3-S2 / R632-4-S2 | RESOLVED: mask held before yield through finalization; :5754 and :5767; unchanged cleanup-entry probe and complete standing per-step sweep |
| R633-5-F1 | RESOLVED: real-boundary closing precedence at :5333; unchanged nine-case probe, earliest-restore variant and standing 18-case controls |
| R632-6-F1 (Tests) | RESOLVED: new :12466/:12476 cases kill S8 with six named failures; unchanged diagnostic probe passes |
| R632-1-R1/R2 | APPLIED / SUPERSEDED: mixed-version warning at CI_WORKFLOWS.md:2187; slot-0 fallback removed and public layout now states refusal |
| R632-1-S4 | ADDRESSED: summary distinguishes containers removed before confirmed placement at :5559 |
| R632-2-S1 | ADDRESSED: cleanup-mask and reader-failure controls; K29/K31 killed |
| R632-5-R1/R2 | APPLIED: exact secondary-signal wording at CI_WORKFLOWS.md:1833 and “Throughout” at :1838 |
| R632-5-S2 | ADDRESSED: PR states the per-step count depends on the interpreter |
| R632-6-R1 / R633-6-R1 | Round-six wording corrected, but the same publication staleness recurs for round seven; retained as R633-7-R1 below |

R633-7-R1 | RESIDUE | Docs | PR #731 Status, [reviewed snapshot](receipts/pr-body.md).

Authority/evidence: the published head is `b341e875d87c6aa2be355bad17f373782517f723`, while Status still names `73b8dcd6` as the PR head and says round seven is local and unpushed. Impact: publication wording only; no measurement, figure, verdict, test, code, generated artifact, conformance, clause or privacy claim changes. Exact fix: replace the three status lines beginning with the branch/head line through “The manager owns its publication and re-review” with: “`730-act-cpusets` -> `dev`, published PR head `b341e875d87c6aa2be355bad17f373782517f723`. The manager owns publication of the review results.” Verification: reread Status against the published PR head. Carry this on the residue checklist; Docs stays CLEAN.

Retained optional findings:

- R632-6-S1 (also R632-5-S1) | SUGGESTION | Tests | closing-signal self-tests at `scripts/act_ci.py:12415` and `:12649`, S9 receipt. Evidence: removing both restores is rejected with rc 129 but no named FAIL arm. Impact: weaker failure attribution; the gate still rejects the mutation. Optional outcome: contain this negative control within its arm. Verification: S9 remains rejected and identifies its failing arm. The earlier live-probe-window attribution suggestion is likewise optional.
- R632-6-S2 (R632-3-S1 / R632-4-S1 / R632-5-S3) | SUGGESTION | Tests | `scripts/act_ci.py:5649`, `:5499`, `:5486`, `:5748`, `:5921`; Q06/Q11/Q13/Q28/Q29 receipts. Evidence: standing controls do not individually pin pipe-close error reporting, staging/off-target summaries, stderr disposal, or derivation specifically from a differing materialized checkout. Current code was inspected and the differing-checkout probe passes. Impact: future regressions in those optional checks may escape the standing suite. Optional outcome: add distinct negative controls. Verification: corresponding Q mutants fail named arms; Q15 remains an equivalent mutation, not a defect.
- R632-6-S3 (R632-2-S3 / R632-3-S3 / R632-4-S3 / R632-5-S4) | SUGGESTION | Robustness | `scripts/act_ci.py:5591`, shutdown receipt. Evidence: a join that raises immediately can print “survived its bounded shutdown” before a full bounded wait. Impact: imprecise diagnostic cause; containment still waits correctly. Optional outcome: distinguish join failure from elapsed timeout. Verification: retry and hold probes retain containment while naming the correct cause.

S5/S6 are disclosed equivalent campaign survivors: other restores and the latched repeat-signal behavior retain the tested outcomes. No previously blocking finding has been downgraded or moved to another issue to clear a lens. Submitted-review and inline-comment inventories were empty; historical findings are in the public conversation comments linked by the assignments.

Reviewer-owned completion ledger:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #730 acceptance/decisions; act_ci.py:2090, :2119, :4671, :4719, :5918; shipping workflows; capacity, derivation and warning/status receipts | R633-7 | b341e875d87c6aa2be355bad17f373782517f723 |
| RTL | CLEAN | Full two-file diff; architecture:111; act_ci.py:5380, :5574, :5610, :5675, :5818, :15927; unchanged interfaces/gitlinks | R633-7 | b341e875d87c6aa2be355bad17f373782517f723 |
| Robustness | CLEAN | act_ci.py:5333, :5435, :5462, :5492, :5527, :5586, :5626, :5733; lifecycle, shutdown, cleanup-entry and precedence probes | R633-7 | b341e875d87c6aa2be355bad17f373782517f723 |
| Tests | CLEAN | act_ci.py:7171, :7268, :7502, :7947, :8120, :8334, :12466, :12476, :12649, :14962; 531-arm receipt; three campaigns and their raw mutant receipts | R633-7 | b341e875d87c6aa2be355bad17f373782517f723 |
| Docs | CLEAN | Full CI_WORKFLOWS.md diff, especially :1760, :1773, :1813, :1833, :1838, :2180; issue, PR, author gate receipts; R633-7-R1 wording residue | R633-7 | b341e875d87c6aa2be355bad17f373782517f723 |

Limits and remaining manager duties:

- Live placement, daemon event timing, `nproc`, CPU/memory performance and same-head replay verdict comparison were NOT RUN. The live interruption/credential gates and real dry-run were not invoked. Offline dry-run uses synthetic PR metadata and inert external boundaries; it is not proof that a live dry-run is daemon-free.
- No manager source bank exists at this exact head and none is inferred. The source base is `dc4d06cb`; supplied live dev is `49da9fd974e8805d56c90e29dcfcb67994c2c430`. The manager must construct and validate the then-current-dev merge candidate, including builder and native banks, and publish those separate receipts.
- The [exact-head hosted snapshot](receipts/hosted-snapshot.json) contains 10 successful executed contexts, 10 in progress, three queued and one skipped physical job. This is not a completed hosted acceptance bar. A skipped context is not executed coverage. The manager owns hosted/replica acceptance under the disk ruling.
- Physical calibration was NOT RUN; field skips are not hardware proof. Nothing here satisfies the physical release obligations of REQUIREMENTS.md.
- Reconcile both independent reviews and the residue, publish this packet, complete the hosted/current-dev candidate bar, obtain explicit maintainer merge authorization, and perform post-merge containment. After merge, retain acceptance 3's live comparison, acceptance 4's per-job wall-clock and memory measurement, and optional acceptance 5. Keep #730 open until those retained duties are discharged.

[Final integrity verification](receipts/integrity.json) checks every raw tracked blob, executable/symlink mode and stage-zero index entry, with replacement objects disabled: 1301 root entries, including 1296 blobs and five unchanged gitlinks. The initialized required submodules match their pins and bytes: protocol processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`, gPTP processor `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`, and AXI-Stream `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The unused external and lwSRP checkouts remain uninitialized. All checked indexes/statuses are clean. No tracked restoration was needed: mutations affected only disposable exports. No source fix, commit, push, GitHub write, author contact, delegation, privileged action, shared installation or hardware operation occurred.

R633-7 FINISHED
