[R633] POSITIVE - exact head 5c6f489ac65f51763a6ccc41f338dde0e5fc90b5

R633-3, external independent review of issue #730 / PR #731. All five lenses are CLEAN at this head. The requested fixes are resolved. No new BLOCKER, MAJOR, MINOR, or RESIDUE is recorded. Two previously optional suggestions remain explicitly open below. This is a source review, not merge authorization or a claim that the Issue is complete.

Reviewed tree: `f2e72c84ee50dbd84ea0d37c98f18d2fc8bbdc24`. Source base: `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`. The full diff changes only `scripts/act_ci.py` and `docs/testing/CI_WORKFLOWS.md`; all six commits were examined. The round-3 delta from `5ba8313a` was also examined separately. No workflow, RTL, firmware, or gitlink changed.

Reconstruction used AGENTS.md, CONTRIBUTING.md, docs/README.md, the [frozen Issue](https://github.com/kebag-logic/milan-fpga/issues/730), [assignment](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131408752), [no-replay ruling](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815), [round-2 decision](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6132404197), and [round-3 decision](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6133149921). Relevant authorities were REQUIREMENTS.md section 8 and the CI workflow contract; the architecture's verification boundary confirms the product hardware is outside this delta. The independent full-diff pass, initial executable checks, verdict and ledger were written before reading prior review reports; [the intermediate record](receipts/independent-pass.txt) preserves that order. Prior public findings were then reconciled against the current source and fresh probes. No private author material or current-round peer report was read.

**Resolution of the public findings**

| ID, original severity and lenses | Disposition at this exact head | Artifact and verification |
|---|---|---|
| R633-1-F1, MAJOR, Conformance/RTL/Robustness/Tests/Docs | RESOLVED | `scripts/act_ci.py:5443` releases on destroy or inspect-proven absence, never die. The original restart sequence gives A `4-7`, B `8-11`, and A keeps its reservation on restart. `:7396` supplies a standing daemon-state assertion. [Compatible original probe](receipts/r633-r1-compatible.log), [lifecycle probe](receipts/r633-r2-lifecycle-unchanged.log), K01 killed. |
| R633-1-F2, MAJOR, all five lenses | RESOLVED | `scripts/act_ci.py:5405` reserves before assignment; `:5372` retains uncertain reservations. Applied-then-timeout, delayed application, rejected updates and unreadable inspect never release a possibly occupied target. Same probe receipts; K02, K03, K07, K08 killed. Keeping the range after an inspect still sees staging is conservative because the outstanding daemon request may complete later. |
| R633-1-F3, MAJOR, all five lenses | RESOLVED | `scripts/act_ci.py:4672,5831` refuses insufficient derived capacity before slot entry, including slot 0. Four containers refuse at 19 CPUs and fit at 20; one refuses at 7 and fits at 8. Standing boundary arms, independent capacity probes and K15/K16 verify this. The PR and `CI_WORKFLOWS.md:1783` now agree. |
| R633-1-F4, MAJOR, all five lenses | RESOLVED, including the remaining original-failure issue below | `scripts/act_ci.py:5528,5677` completes containment, join and close before propagation. Original reaping-failure probe and busy-reader controls pass; K09/K10/K11/K14 are killed. The original failure is now retained by R633-2-F1's correction. |
| R632-1-F1, MINOR, Tests/Docs | RESOLVED | `scripts/act_ci.py:7823` keeps a move outstanding through shutdown. Removing the join fails the standing suite: unchanged M13 is killed with 11 failing arms; K10 is killed. The independent no-join control observes a live reader at boundary exit. |
| R632-1-F2, MINOR, Tests | RESOLVED | `scripts/act_ci.py:6502` drives the workflow return path with staging and stream problems. Exit 0 stays PASS; exit 3 stays FAILED (3), with one summary and one warning per problem. Unchanged M16, M17 and M23 are killed, as are K23/K24. [Independent return-path output](receipts/r633-r2-monitor-unchanged.log) agrees. |
| R632-1-R1, RESIDUE, Docs | APPLIED | The requested mixed-runner-version sentence appears at `docs/testing/CI_WORKFLOWS.md:2154`. |
| R632-1-R2, RESIDUE, Docs | SUPERSEDED AND APPLIED | The PR body's Layout row now describes refusal for every insufficient slot, with the 20/8 CPU thresholds. The former fallback is gone. |
| R633-2-F1, MINOR, all five lenses | RESOLVED | `scripts/act_ci.py:5677` captures the original exception and passes it as `primary`; `:5576` reports secondary failures without replacing it. The unchanged [round-2 monitor probe](receipts/r633-r2-monitor-unchanged.log) now returns 143 with the SIGTERM diagnostic and secondary reap diagnostic. Original RuntimeError identity is preserved. Without an earlier failure, the reap Refusal still propagates. Containment, finished reader and closed pipe precede all outcomes. Standing real INT/TERM/HUP arms return 130/143/129. |
| R632-2-F1, MINOR, Tests | RESOLVED | `scripts/act_ci.py:7740,7996` pins event time, join retry, the hold after a short timeout, and multiple-cleanup-error precedence. The unchanged campaign kills K12, K13, K32 and K36 with 3, 4, 1 and 1 failing standing arms respectively. [Required-mutant receipts](receipts/required-mutants.json). |
| R632-1-S1/S2/S3/S4, SUGGESTION, Robustness | ADDRESSED | Restart, uncertain-update and failed-reap behavior is covered above. The summary separately counts containers removed before confirmed placement (`scripts/act_ci.py:5472`). |
| R632-2-S1, SUGGESTION, Tests | ADDRESSED | `scripts/act_ci.py:8070` checks the cleanup signal mask and failed-reader problem. K29 and K31 are now killed. |

**Retained optional findings**

The [round-3 decision](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6133149921) explicitly leaves these prior suggestions optional. They are not represented as resolved and do not bank a proof stronger than the tests establish.

- **R632-2-S2 | SUGGESTION | Conformance, RTL, Robustness, Tests, Docs.** Artifact: `scripts/act_ci.py:5680` through entry to `blocked_cleanup_signals` at `:5547`; PR body, Known limitations. Authority/evidence: the source still allows a first INT/TERM/HUP to arrive after normal resumption into `finally` but before the cleanup mask. That can bypass the monitor stop call. The accepted round-3 scope treats this window as optional; body interruption and an interruption already propagating are the corrected paths. Impact: a first signal in that narrow cleanup-entry window can leave the stream and reader uncontained by this monitor. Desired outcome: close the signal-entry window across the cleanup boundary without weakening child signal delivery. Verification: inject the first signal at cleanup entry and prove stream absence, completed reader and closed pipe before outer teardown. This round does not claim an unconditional all-signal-position containment proof.
- **R632-2-S3 | SUGGESTION | Robustness, Docs.** Artifact: `scripts/act_ci.py:5506`; [shutdown probe S2](receipts/r632-r2-shutdown-unchanged.log). Evidence: a join that raises immediately can print that the reader survived its bounded shutdown although the bounded wait did not elapse. Impact: imprecise diagnostic; the actual containment hold still waits for the reader. Desired outcome: distinguish failed-join and elapsed-timeout messages. Verification: assert separate diagnostics while retaining reader completion on both paths. This is retained as the prior optional diagnostic suggestion, not classified as prose-only RESIDUE.

**Executed evidence and its limits**

Every candidate self-test or imported candidate definition ran inside an unprivileged disposable boundary with no network, host credentials or Docker socket. The root checkout was mounted read-only. Mutation trees and dependencies live under packet `scratch/` only. Foreground drivers completed their concurrent subprocesses before returning, with at most 13 concurrent checks and no heavy builds.

| Check | Current-head result and receipt |
|---|---|
| Runner `--selftest` | rc 0, 497 ok, zero FAIL, [raw log](receipts/selftest.log). Interpreter 3.14.7. |
| R632-2 `mutants_r2.py`, unchanged, `--jobs 10` | 36/36 killed, no surviving mutation or bad anchor; [campaign](receipts/mutants-r2-unchanged.log). Each self-test's raw stdout/stderr and rc is retained under `receipts/mutant-logs/`. Script SHA-256 `c78da78362d7e19e2f068d76d368201f111b5faa80110c24a7c934748f85ec0b` matches the public script. |
| R633-2 `probe_monitor.py`, unchanged | rc 0; original signal and failure preserved; reap-only Refusal retained; join-removal negative control detects live reader; staging warnings preserve workflow verdict. |
| R633-2 `probe_lifecycle.py`, unchanged | rc 0; four fault modes, each 64 seeds x 300 transitions; 88 capacity combinations. [Receipt](receipts/r633-r2-lifecycle-unchanged.log). |
| R632-2 `probe_shutdown.py`, unchanged | rc 0, S1-S4 PASS: bounded hold, retry, first-error precedence and cleanup signal mask. [Receipt](receipts/r632-r2-shutdown-unchanged.log). |
| R632-1 `mutants.py`, unchanged, 8 jobs | 18 killed, one survivor, five obsolete anchors. M13/M16/M17/M23 are killed. M18, which removes the live interrupt gate's move requirement, survives the offline suite; that gate remains unrun. M08/M09/M12/M20/C24 are INVALID, not killed. [Campaign](receipts/mutants-r1-unchanged.log); raw logs under `receipts/mutants-r1-raw/`. |
| Offline dry-run path | Both slot 0 and slot 3 return 0. The shipping workflow is read by the actual `run_validation` dry-run path with external boundaries substituted. [Output](receipts/offline-dryrun.log), [portable driver](scripts/offline_dryrun.py). |
| Existing focused gates | CI contract 2016 items, its self-test 2828 arms; slot proof 44 cases; Python idiom and 54 self-checks; bare-metal check and 700 self-checks; documentation privacy/routing/style/paths; TOC and 480 anchors; em-dash 339 controls, zero findings over 133 added lines; diff whitespace. All final results rc 0. Individual logs/rc files and command lists are in `receipts/initial-runs.json` and `receipts/docs-runs.json`. |

Two old probe results require explicit interpretation:

1. [R633-1's byte-identical original](receipts/r633-r1-unchanged.log) returns 1 because `JobCpuRanges` now requires the new `read_cpus` collaborator. It is not credited as passing. The already-published [compatibility copy](public-inputs/reviews/R633-2/probe_cpu_ranges_compat.py), unchanged in this round, adds only the collaborator, selected join definition and process PID. Its original sequences/assertions pass, including F1-F4. No assertion was weakened.
2. The extra unchanged [R632-2 general probe](receipts/r632-r2-probe-unchanged.log) returns 1 only at P4, which requires the reap Refusal to replace the original body error. That expectation is explicitly reversed by the round-3 ruling. Its transcript shows containment, reader end and pipe close before exit and the original RuntimeError retained. All other checks pass, including 3,000 ordinary and 3,000 faulted interleavings. The unchanged mutation campaign's auxiliary calls inherit this stale P4; mutant kills are credited to the standing self-test failures, not those auxiliary return codes.

An initial sandbox whitespace query returned 128 because a required alternate object directory was not mounted. The subsequent read-only Git query succeeded; [environment receipt](receipts/diff-check-environment.txt). No candidate code was executed on the host. Hash-pinned Markdown dependencies were installed only in scratch. Raw mutation outputs were inspected to distinguish failing assertions from infrastructure errors.

The allocator's four-wide static ranges and refusal guards support the intended `nproc = 4` shape; no live affinity or nproc measurement is claimed. The workflow concurrency bound agrees with the pinned [default matrix width](https://github.com/nektos/act/blob/v0.2.89/pkg/model/workflow.go#L219) and [nested scheduler](https://github.com/nektos/act/blob/v0.2.89/pkg/runner/runner.go#L171). The ownership/type/action filters agree with the documented [event filter semantics](https://docs.docker.com/reference/cli/docker/system/events/#filtering---filter), and cpuset updates are an exposed [container update operation](https://docs.docker.com/reference/cli/docker/container/update/). These source checks and inert models do not measure daemon timing.

The dry-run output shows staging `0-3`, job ranges `4-7 8-11 12-15 16-19`, and staging `60-63`, job ranges `64-67 68-71 72-75 76-79`. It uses a synthetic PR/head. It is not a live, daemon-free invocation: the production dry run still enters its Docker boundary. Cross-slot disjointness applies to one consistent runner version; mixed versions are explicitly documented as overlapping.

Nine downloaded author round-3 receipt files match their published SHA-256 manifest, including the 497-arm runner log and gate/mutation summaries: [verification](receipts/author-manifest-verification.json). Their head attribution is the author's [published round-3 evidence comment](https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6133409048), with receipts in the [public evidence tree](https://github.com/kebag-logic/milan-fpga/tree/50e9635d4eea7d936e8309bbc42cd64bc93cf98f/review-evidence/730-r1/author-r3/receipts/r3). These are author source-head receipts. No manager source bank exists at this head, and none is inferred.

**Reviewer-owned ledger**

CLEAN means no open BLOCKER, MAJOR or MINOR under that lens. The retained SUGGESTION findings do not clear themselves and do not change that classification.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue acceptance/rulings; `scripts/act_ci.py:2043,2072,4672,5298,5677,5813`; full.diff; capacity/derivation/restart/timeout probes; offline dry-run | R633-3 | 5c6f489ac65f51763a6ccc41f338dde0e5fc90b5 |
| RTL | CLEAN | Full two-file diff establishes no hardware/CDC/reset/interface change; `docs/overview/ARCHITECTURE.md:111`; software architecture at `act_ci.py:2416,4834,5492,5528,5731`: single reader, existing bounded command path, containment ladder, lease gate and cleanup order; memory/swap and slot cap unchanged | R633-3 | 5c6f489ac65f51763a6ccc41f338dde0e5fc90b5 |
| Robustness | CLEAN | `act_ci.py:5353,5405,5443,5492,5528,5593`; lifecycle/fault/randomized probes, insufficient-capacity controls, busy-reader shutdown and primary/secondary failure receipts; S2/S3 retained optional | R633-3 | 5c6f489ac65f51763a6ccc41f338dde0e5fc90b5 |
| Tests | CLEAN | `act_ci.py:6502,7162,7396,7823,7996,14285`; selftest.log; unchanged 36-mutant campaign; M13/M16/M17/M23 rerun; independent no-join control; ci-events and slot-proof suites; old-fixture exceptions explicitly accounted for | R633-3 | 5c6f489ac65f51763a6ccc41f338dde0e5fc90b5 |
| Docs | CLEAN | Entire CI_WORKFLOWS.md delta, especially `:1750,1760,1773,1803,2144`; public Issue/PR body and author receipts; all focused documentation gates; no measured speedup or hardware claim credited | R633-3 | 5c6f489ac65f51763a6ccc41f338dde0e5fc90b5 |

**Integrity, real limits and pending manager duties**

[verify_integrity.py](scripts/verify_integrity.py) compares raw tracked bytes, file kinds/modes and complete stage-0 index entries against the exact head, with replacement objects disabled. The [receipt](receipts/integrity.json) passes all 1,301 root entries and the initialized required submodules: protocol processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`, gPTP processor `7dda9c3b4d65cbbb28f72a34e1ee0efe368695d9`, AXI-Stream `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The other two gitlinks also match; their checkouts remain uninitialized. No source restoration was necessary, and no nonignored untracked file remains in the clone.

The [exact-head hosted snapshot](receipts/hosted-snapshot.json) shows successful selectors, lint, BDD, wire accountability, docs-check-no-git, four synthesis shard jobs and one firmware mutation job. Other required work remains in progress, including all five simulation shards, docs and elaboration. The physical gPTP job is skipped. This is not a completed hosted acceptance bar; a skipped context is not executed coverage, and job status alone is not proof of fresh execution of every internal step.

No live replay, live interrupt test, Docker operation, host runner/self-test, broad parent/processor/synthesis/builder bank, heavy build, privileged action, shared install, source fix, commit, push, GitHub write, merge, author contact or delegated review occurred. Physical calibration was NOT RUN; field skips are not hardware proof. Models establish bookkeeping and fault-path behavior, not event delivery, daemon latency, real cpuset movement or performance. CPU availability still follows `os.cpu_count`, not an online/affinity census.

The manager retains these duties:

- Complete the independent review bar and own exact-head hosted/replay acceptance under the disk ruling. The live interrupt gate and M18's live-only claim remain unexercised here.
- Construct the final candidate from the then-current `dev`, validate its builder/native and other required banks, and link receipts at the merge turn. Source review and source-head evidence do not substitute for that candidate validation.
- Retain the two optional suggestions above in public scope; settle the known production dry-run/daemon-free wording conflict separately if needed.
- Obtain explicit maintainer merge authorization, then perform the repository's post-merge containment checks.
- Execute the deferred same-head verdict comparison and per-job wall-clock/slot-memory measurement; acceptance 4 is not measured here. Optional acceptance 5 follows the measurement ruling. Keep #730 open until its retained post-merge obligations are discharged.

Publish only REPORT.md and files listed in MANIFEST.sha256. Scratch is excluded.

R633-3 FINISHED
