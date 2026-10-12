[R632] POSITIVE - exact head 31e53e82a4a1604569ccacba8473f21e70b9cbc0

R632-4 is the internal, cleared-context review of issue #730 / PR #731 at exact head `31e53e82a4a1604569ccacba8473f21e70b9cbc0`, tree `9dc0b704562f67cab1d805b40d56a5c983ddcebb`. It covers the full diff `dc4d06cb..31e53e82` and the Round 4 delta `5c6f489a..31e53e82`, which only adds a test.

**Result.** All five lenses were applied and all five are CLEAN at this head. No BLOCKER, MAJOR, MINOR or RESIDUE finding is open. Three SUGGESTIONs remain open; they are optional and do not affect any lens. R632-3-F1 is resolved: Q24 is KILLED by the new arm, and the unmutated self-test passes with 498 ok and 0 FAIL. Every earlier public finding on this PR is resolved or retained below.

This is a review of the source at this head. It does not authorize a merge, and it is not a manager source bank. No replay ran, nor `act_ci.py` against any PR, nor Docker, act, `--dry-run` or a live self-test. The self-test and every probe ran only inside an unprivileged sandbox with no network and no Docker socket (`scripts/sandbox.sh`).

## Reconstruction (public sources only)

- **Authorities:** AGENTS.md sections 3 to 8; CONTRIBUTING.md workflow and act-first rules; docs/README.md.
- **Issue #730:**
  - acceptance 1 to 5;
  - assignment 6131408752;
  - ruling 6131815815: no replays in the lane; measurement and acceptance 5 after the merge; the lane delivers code, disjointness proof, offline dry-run lines and self-tests;
  - round rulings 6132404197, 6133149921 and 6133645896;
  - author REVIEW READY comments 6132134158, 6132825823, 6133409048 and 6133776179.
- **Interface authority:** `docs/testing/CI_WORKFLOWS.md`, the replica shape (`:1725-1847`) and the parallel replay slots' resource bounds (`:2146-2157`).
- **Diff and history:**
  - seven one-line commits with no trailers, from `7bb36e09` to `31e53e82`;
  - only `scripts/act_ci.py` and `docs/testing/CI_WORKFLOWS.md` change; no workflow, suite, RTL or firmware file;
  - the Round 4 delta (`receipts/round4-delta.diff`) adds `import itertools` and one arm in `selftest_job_concurrency`.
- **Ordering:** I recorded my own pass over the diff and my probes (`receipts/own-pass-before-prior-findings.txt`, 22:43:04Z) before reading any earlier review's finding text. I did not read the concurrent external round's report.

## Executed evidence (this round, exact head; receipts in MANIFEST.sha256)

| Run | Result | Receipt |
| --- | --- | --- |
| `act_ci.py --selftest` on a `git archive` of the head (blob `ab097a5c`, the same as the clone's index), in the sandbox, CPython 3.14.7, PyYAML 6.0.3 | rc 0, `selftest: PASS`, 498 ok, 0 FAIL, 6 s | `receipts/selftest-head.*` |
| The same with `os.cpu_count` stubbed to 1, 4 (hosted `docs` runner), 8, 19 and 20 | rc 0 each, `selftest: PASS` | `receipts/selftest-cpu{1,4,8,19,20}.*`, `scripts/cpu_stub_selftest.py` |
| R632-3's `mutants_r3.py`, unchanged (sha256 `2ef94964...`, matches the public copy) | 30 mutants, 24 killed; **Q24 KILLED**, failing exactly the new arm "the most of any selected workflow in every order"; survivors Q06, Q11, Q13, Q15, Q28, Q29, the set recorded at R632-3; bad anchors none | `receipts/mutants_r3-at-head.*` |
| R632-2's `mutants_r2.py`, unchanged (sha256 `c78da783...`) | 36 of 36 killed, including K12 (3 arms), K13 (4), K32 (1) and K36 (1) | `receipts/mutants_r2-at-head.*` |
| R632-3's `probe_r3.py` (300 seeds) and R632-2's `probe_shutdown.py`, both unchanged | P1-P5 PASS, including P3b (the run derives from the materialized checkout); S1-S4 PASS | `receipts/probe_r3-at-head.*`, `receipts/probe_shutdown-at-head.*` |
| R633-2's `probe_lifecycle.py`, `probe_monitor.py` and `probe_cpu_ranges_compat.py`, and R632-2's adapted R633-1 probe, all unchanged | All PASS. Adapted R633-1 F1 (restart sequence), F2 (update applied, then CLI timeout), F3 (slot 0 at 19 CPUs refuses) and F4 (reap failure still joins the reader) PASS. The monitor probe's signal arm observed 143 | `receipts/r633-2-*`, `receipts/r632-2-r633-1-probe-adapted-at-head.*` |
| R633-1's `probe_cpu_ranges.py`, unchanged | rc 1 at setup: `JobCpuRanges.__init__() missing ... 'read_cpus'`. The record gained its inspect seam in Round 2 (R633-1-F1/F2), so the unchanged probe cannot build the record. Its four contract probes are re-run through the adapted copy above and through `probe_r2.py` P1-P3 | `receipts/r633-1-probe_cpu_ranges-at-head.*` |
| R632-2's `probe_r2.py`, unchanged | P1, P2, P2b, P3a, P3b, P7-P10 PASS. P4 FAILS by design: it expects the reap Refusal to replace a body failure, the behaviour that the Round 3 ruling (6133149921 item 1) reversed. At this head the body failure propagates, the reap failure is printed beside it, and containment, the move, the end of the stream and the pipe close all come before the monitor exits (trail in the log) | `receipts/probe_r2-at-head.*` |
| My independent probe `probe_r632_4.py` (400 seeds) | A1-A5 PASS (detail below) | `receipts/probe_r632_4-at-head.*` |
| The same probe on a tree with Q29 applied (derivation reads the runner's own `ROOT`) | A4 FAILS: planted `max-parallel` 2, 3 and 9 all give 4 ranges, and 9 is no longer refused. So A4 can fail for the defect it targets | `receipts/probe_r632_4-on-Q29-mutant.*` |
| Offline dry run of the shipping `rtl-full` through the runner's own harness (`dry_run_transcript`: real `run_validation`, with GitHub, git, the slot daemon and the boundary stood in) | slot 0: `each created on --cpuset-cpus=0-3, then moved to a free one of --cpuset-cpus=4-7 --cpuset-cpus=8-11 --cpuset-cpus=12-15 --cpuset-cpus=16-19`; slot 3: `60-63` then `64-67 68-71 72-75 76-79`; act word `--cpuset-cpus=<staging> --memory=16g`; rc 0 for both | `receipts/dryrun-offline-at-head.*`, `scripts/dryrun_r632_4.py` |
| Repository gates in the sandbox: `ci_events.py --check` (2016 items) and `--selftest` (2828 arms); `act_slot_proof.sh --selftest` (44); `check_py_idiom.py` and `--selftest` (54); `check_baremetal_only.py --check` and `--selftest` (700); `docs_check.py`; `check_doc_style.py`; `gen_toc.py --check` and `--verify-anchors`; `check_em_dash.py --base dc4d06cb` (0 findings over 133 added lines); `check_doc_paths.py`; `git diff --check dc4d06cb HEAD` | all rc 0. The first pass had environment-only failures; see the note in the receipt | `receipts/gates/`, `receipts/tree-gates-summary.txt`, `receipts/gates-summary-gitcopy.txt` |
| Hosted contexts on PR #731, snapshot at 22:44Z | Many still pending, including `docs-check`, where the self-test runs on a 4-vCPU runner. Completed contexts pass. No conclusion is drawn; hosted acceptance belongs to the manager | `receipts/hosted-checks-snapshot.txt` |

**What `probe_r632_4.py` checks.** It is my own code and imports nothing from earlier reviews.

- **A1:** a fuzz with its own daemon model. The model has:
  - event lag: the daemon acts before the record reads the event, and any number of events can be pending;
  - restarts, and containers that vanish without a `destroy`;
  - moves that are applied and then time out, lost and landing later, or refused;
  - transient inspect timeouts.

  After every daemon step and every observed event, no job range is used by two existing containers, counting moves that may still land. Every container on a job range holds that range in the record. Result: 0 violations, 1316 confirmed moves, 108 containers left on staging and reported.
- **A2:** the previous workflow's tail events, replayed into a fresh record by `--since`, move nothing that exists and raise nothing.
- **A3:** a move whose CLI raises `OSError` stops the reader as a recorded problem and raises nothing.
- **A4:** at run level, a materialized checkout whose `rtl-full` names `max-parallel` 2 or 3 derives 2 or 3 ranges, while the runner's own workflows stay at the default. An expression, or 9, refuses the run.
- **A5:** `max-parallel` spellings. `04` is accepted, as act's Atoi accepts it. `+4`, `0x4`, blank, `4 ` and `1_0` are refused. A strategy with no matrix runs one container.

## Judgement on the focus questions

- **Ranges never overlap, within or across slots.**
  - `slot_cpu_base` (`scripts/act_ci.py:4625`) gives slot N the block `20N..20N+19`.
  - `job_cpu_ranges` (`:4673-4708`) refuses a derived concurrency outside 1..`SLOT_JOB_RANGES`, refuses a host without the last range on every slot, slot 0 included (`:4688-4695`), and re-checks its own ranges against the staging range.
  - The standing proof (`selftest_cpu_layout_disjoint`, `:7182`) covers slots 0-63 at full concurrency. It fails on the planted cross-slot and within-slot overlaps.
  - Under create/die races and restarts, `JobCpuRanges` (`:5299-5480`):
    - reserves before it moves (`place`, `:5406-5437`);
    - frees only on `destroy`, on an inspect answering `No such container`, or on a move answering `No such container` (`observe` `:5444-5460`, `release` `:5367-5371`, `effective_cpus` `:5354-5365`);
    - keeps a failed or uncertain move reserved (`check`, `:5373-5404`);
    - reads placement from `docker container inspect`.

    A1, `probe_r3` P1 (120,000 steps), R633-2's lifecycle probe and the standing model-daemon arms (`:7416`, `:7505`) all find no shared range.
  - Disjointness never depends on the derivation being right. A container that finds no free range stays on the staging range, which no job range overlaps.
- **A container left on the staging range cannot change a verdict.**
  - `report_job_cpu_ranges` (`:5688`) only prints, and `execute_workflows` (`:5775-5813`) decides the verdict from act's exit alone.
  - This is pinned at run level by `selftest_cpu_range_warnings` (`:6503`): exit 0 gives `PASS`, exit 3 gives `FAILED (3)`.
  - Only `--interrupt-selftest` (`:15318-15331`) turns a missed move into a Refusal, which is its stated purpose.
- **The events stream is contained and joined on every exit path.**
  - `job_cpu_range_monitor` (`:5594`) starts the stream in its own session under deferred signal delivery. `stop_job_cpu_range_monitor` (`:5529`) then runs poll, the containment ladder, the join retried until the reader has provably ended, and the pipe close, with signals masked and whatever an earlier step raised.
  - Only after that is a failure surfaced. An interrupt or body failure already propagating keeps its exit status and diagnostic (`:5678-5685`, `:5577-5590`).
  - The reader thread is started with the cleanup signals blocked (`start_cleanup_thread_or_refuse`).
  - The monitor exits before `cleanup_owned_containers` and the boundary's teardown, so the ownership, lease, cleanup and leftover Refusals are unchanged.
  - The one known gap is retained as S2.
- **Derivation.**
  - `replay_container_concurrency` (`:2073`) is called on `layout.checkout` (`:5835`), which holds the replayed workflows, through the duplicate-key-refusing all-strings loader. This is before `replay_slot` (`:5848`).
  - An unreadable or too-wide `max-parallel` is a Refusal (`:2044-2070`, `:4681-4687`; A4, A5).
  - The width rule matches act 0.2.89. The binary's own strings include `Failed to parse 'max-parallel' option` and the `--rm` help text "automatically remove container(s)/volume(s) after a workflow(s) failure".
  - Reusable workflows, service and job containers, and `docker://` steps are already refused by `validate_workflow_sandbox` (`:1998-2040`), so no container that the derivation cannot see is created.
- **`nproc` stays 4.** Every staging and job range is `CONTAINER_CPU_LIMIT` wide on any host the run accepts: `probe_r3` P5, the widths check in the disjointness proof, and A1. `--memory`, `--memory-swap`, `--concurrent-jobs` and `SLOT_MEMORY_MAX` are untouched in the diff.

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE finding is open at this head.

### SUGGESTIONS (optional; no lens impact)

- **R632-4-S1 | SUGGESTION | Tests | `scripts/act_ci.py:5835`, `selftest_dry_run_cpu_ranges` (`:14362`).** This retains R632-3-S1.
  - Evidence: no standing arm pins that the run derives from the materialized checkout and not from the runner's own tree. In the self-test the checkout carries the shipping workflows, so Q29 survives.
  - Other survivors, each about a diagnostic or a summary count: Q06 (a pipe-close failure is recorded), Q11 (outcome label `staging`), Q13 (warning for a moved container read off its range, `:5400`), Q28 (stream stderr to `DEVNULL`).
  - The head is correct (A4, `probe_r3` P3b), and a regression would only under- or over-provision ranges. Containers would land on staging with a warning; nothing would overlap and no verdict would change.
  - Desired outcome: one dry-run arm that plants a checkout whose `rtl-full` names a different `max-parallel` than the runner's tree. A4 is a ready template, and it kills Q29.
- **R632-4-S2 | SUGGESTION | Robustness, Docs | `scripts/act_ci.py:5681-5685` up to the mask in `stop_job_cpu_range_monitor` (`:5549`); `docs/testing/CI_WORKFLOWS.md:1807`.** This retains R632-2-S2 / R632-3-S2.
  - Evidence: a first INT/TERM/HUP that lands after the generator resumes into `finally` and before the mask skips the monitor's containment.
  - The window is a few bytecodes. The Round 3 ruling makes it optional, and `replay_slot` and `run_act_process` share the pattern. The doc's existing teardown guarantee (`:2206`) is worded with the same absoluteness.
  - Desired outcome: a separate Issue closing the window across the runner's cleanup entries, or the doc carrying the PR body's caveat until then.
- **R632-4-S3 | SUGGESTION | Robustness | `join_job_cpu_reader` (`:5493-5526`).** This retains R632-2-S3.
  - A join that raises at once is still reported as "survived its bounded shutdown".
  - The hold is accurate, since teardown waits, but the diagnostic conflates the two causes.

### Prior public findings, resolved or retained at this head

| Finding | State | Evidence at this head |
| --- | --- | --- |
| R633-1-F1 (`die` freed a restartable container's range) | RESOLVED | `observe` frees only on `destroy` or inspect-proven absence (`:5444-5460`, `:5354-5371`); adapted R633-1 F1 PASS; K01 killed; A1 0 violations |
| R633-1-F2 (an uncertain update freed its target) | RESOLVED | `place` reserves before `assign`, and only `No such container` frees (`:5406-5437`); adapted F2 PASS; K02, K03, K07 and K08 killed; A1 covers the applied, lost and refused cases |
| R633-1-F3 (slot 0 fell back silently) | RESOLVED | `job_cpu_ranges` refuses on every slot (`:4688-4695`) before `replay_slot`; adapted F3 PASS; `probe_r2` P3a/P3b; standing arm `:7233` |
| R633-1-F4 (a reap failure skipped the join) | RESOLVED | `stop_job_cpu_range_monitor` (`:5529-5591`); adapted F4 PASS; K09, K10, K11 and K14 killed |
| R632-1-F1 (no arm failed without the reader join) | RESOLVED | `selftest_job_cpu_monitor_busy` (`:7843`); K10 killed |
| R632-1-F2 (verdict invariance not pinned at run level) | RESOLVED | `selftest_cpu_range_warnings` (`:6503`); K23 and K24 killed |
| R632-1-R1, R632-1-R2 (RESIDUE) | APPLIED | `CI_WORKFLOWS.md:2154-2157` mixed runner versions; the PR body's Layout row states the refusal on every slot |
| R632-1-S1..S4 | ADDRESSED | By the R633-1 fixes, and the `<g> removed before that` summary field |
| R633-2-F1 (a cleanup failure replaced an interrupt already unwinding) | RESOLVED | `primary` recorded (`:5678-5679`) and handed to stop, which prints and returns (`:5577-5590`); the monitor probe's signal arm observed 143; standing arms for SIGINT/SIGTERM/SIGHUP plus reap failure (`:7843`) |
| R632-2-F1 (K12, K13, K32, K36 survived) | RESOLVED | `mutants_r2.py`, unchanged: 36 of 36 killed; `probe_shutdown.py` S1-S4 PASS |
| R632-2-S1 | TAKEN | K29 and K31 killed |
| R632-2-S2, R632-2-S3 | RETAINED as R632-4-S2 and S3 | See above |
| R633-3 (POSITIVE; retained R632-2-S2/S3 as SUGGESTION) | CONSISTENT | Same classification here |
| R632-3-F1 (the derivation arm could not fail for "the most of any selected workflow"; Q24) | RESOLVED | New arm at `:7122-7153`: three planted workflows (4, 3 and 1 wide) at `CONCURRENT_JOB_LIMIT` 1, 2 and 3; each narrower one alone gives 3 and 1; all six orders plus both two-workflow orders give 4, 6 and 7. `mutants_r3.py`, unchanged: Q24 KILLED, failing exactly this arm. The unmutated self-test passes, 498/0 |
| R632-3-S1, S2, S3 | RETAINED as R632-4-S1, S2 and S3 | See above |

## Lens coverage at this head

```text
[R632] PASS Conformance — scripts/act_ci.py:2044-2093, 4625-4718, 5299-5700, 5775-5813, 5835-5848, 15318-15331; .github/workflows/*.yml (unchanged in the diff); receipts/dryrun-offline-at-head.txt — acceptance 1 (own CONTAINER_CPU_LIMIT-wide range per concurrent container, disjoint in and across slots, memory bounds unchanged, Refusal on a host without the CPUs on every slot), acceptance 2 (derived from the replayed checkout's max-parallel and CONCURRENT_JOB_LIMIT; disjointness proved at maximum concurrency with planted overlaps), acceptance 3 (no workflow, step or job change; nproc 4) and ruling 6131815815 (offline dry-run lines for slot 0 and slot 3; verdict clause, 4 and 5 post-merge; PR says Relates to) — checked against code, act 0.2.89's strings, the self-test, A1-A5 and the prior probes.
[R632] PASS RTL — git diff --name-only dc4d06cb..31e53e82 (scripts/act_ci.py, docs/testing/CI_WORKFLOWS.md; no HDL, CDC or interface file), so the hardware angles do not apply; runner architecture at scripts/act_ci.py:5299-5700 — the outcome machine (moving, moved, gone, staging) has complete transitions for every event, including unknown, duplicate and late ones; single-writer record read only after the reader is proven ended; the integer layout arithmetic (slot_cpu_base, the last-CPU bound) is exact at every slot 0-63 (probe_r3 P4); the monitor sits inside the act spawn and before container cleanup and boundary teardown (:5775-5790).
[R632] PASS Robustness — JobCpuRanges.parse/check/place/observe (:5299-5480), read_job_cpu_events/join_job_cpu_reader/stop_job_cpu_range_monitor/job_cpu_range_monitor (:5483-5686), job_container_width (:2044) — malformed, foreign, duplicate, replayed and lagging events, restarts, vanishing containers, applied/lost/refused moves, inspect timeouts, a non-Refusal exception in the reader (A1-A3, probe_r3 P1, R633-2 lifecycle); return, raise, real SIGINT/SIGTERM/SIGHUP, reap/join/poll/close failures and start failures in shutdown (standing arms, probe_shutdown S1-S4, R633-2 monitor probe); unreadable, signed, hex, blank and too-wide max-parallel (A5, standing arms); hosts at 1, 4, 8, 19 and 20 CPUs (cpu-stub self-tests). S2 and S3 are SUGGESTIONs.
[R632] PASS Tests — scripts/act_ci.py:6503, 7085-7153 (Round 4 arm at 7122-7153), 7182-7300, 7416-8170, 14296-14385; receipts/selftest-head.log (498/0), mutants_r3-at-head.txt (Q24 KILLED; survivors are diagnostics or the equivalent Q15, with Q29 as S1), mutants_r2-at-head.txt (36/36) — every claimed arm checked for its ability to fail; the disjointness proof fails on both planted overlaps; the Round 4 arm fails for last-wins, first-wins, sum and min orders. S1 is a SUGGESTION.
[R632] PASS Docs — docs/testing/CI_WORKFLOWS.md:1551-1558, 1725-1847, 2146-2157, 2364-2366; PR #731 body at head 31e53e82 — the staging/move mechanism, reservation until destroy or inspect, inspect-read placement, derivation and Refusals, the 20N..20N+19 blocks (slots 1-5 fit any shipping workflow and slot 6 a one-container workflow on 128 CPUs, both checked by arithmetic), mixed runner versions, shutdown precedence, the self-test pin list and the post-merge reading (12 containers for a full pull_request run: physical-gptp is skipped off schedule/dispatch); no stale 4N layout remains (repository search); the docs gates are rc 0. S2's doc caveat is a SUGGESTION.
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Acceptance 1-3 and ruling 6131815815 against `scripts/act_ci.py:2044-2093, 4625-4718, 5299-5700, 5775-5848, 15318-15331`; offline dry run, slots 0 and 3; A4, A5 | R632-4 | 31e53e82a4a1604569ccacba8473f21e70b9cbc0 |
| RTL | CLEAN | Diff file list (no HDL/CDC/interface); runner state machine, threading and ordering at `:5299-5700, 5775-5790`; layout arithmetic (probe_r3 P4) | R632-4 | 31e53e82a4a1604569ccacba8473f21e70b9cbc0 |
| Robustness | CLEAN (S2, S3 are SUGGESTIONs) | A1-A3, A5; probe_r3 P1; probe_shutdown S1-S4; R633-2 lifecycle and monitor probes; adapted R633-1 F1-F4; cpu-stub self-tests at 1, 4, 8, 19 and 20 CPUs | R632-4 | 31e53e82a4a1604569ccacba8473f21e70b9cbc0 |
| Tests | CLEAN (S1 is a SUGGESTION) | Self-test 498/0; `mutants_r3.py` 24/30 with Q24 KILLED; `mutants_r2.py` 36/36; Round 4 arm `:7122-7153`; A4 against a Q29 mutant | R632-4 | 31e53e82a4a1604569ccacba8473f21e70b9cbc0 |
| Docs | CLEAN (S2's caveat is a SUGGESTION) | `docs/testing/CI_WORKFLOWS.md:1551-1558, 1725-1847, 2146-2157, 2364-2366`; PR body at head; docs gates rc 0 | R632-4 | 31e53e82a4a1604569ccacba8473f21e70b9cbc0 |

CLEAN means no BLOCKER, MAJOR or MINOR is open under that lens. A SUGGESTION does not affect coverage.

## Real limits of this round

- Nothing ran against a live Docker daemon: no `docker events`, `docker container update` or `docker container inspect`, no act, no replay and no live interrupt gate (ruling and brief). The claims about the event JSON shape, the label filters, the `update` action and updating the cpuset of a running or created container rest on reading the code and the PR's moby/act citations. The live interrupt gate is the only pin for R632-1's M18.
- R633-1's probe, unchanged, cannot construct the Round 2 record (setup error, rc 1). Its four contracts were re-run through R632-2's published adaptation and through `probe_r2.py`.
- The CPU-count stubs replace `os.cpu_count` only. No real 4-vCPU host ran the self-test, and hosted `docs-check` was still pending at the snapshot.
- The self-test and probes ran on CPython 3.14.7. The author's receipts cover 3.12.3.
- No manager source bank exists at this head, and none is inferred. Physical calibration was NOT RUN.
- The wall-clock and memory effects (acceptance 4 and 5) are unmeasured by design. Faster legs may change when the slot's memory peak arrives under the 24G cap. The post-merge measurement should read the cap line.

## Pending manager duties

- Merge-turn validation of the current-dev candidate, with the builder and native banks, on the live dev tip (source base `dc4d06cb`), with receipts linked on the PR.
- Hosted and act acceptance at the exact head. The hosted contexts were in progress at 22:44Z, including `docs-check`, where the self-test runs on a 4-vCPU runner.
- The post-merge measurement under ruling 6131815815: per-job wall clock before (#721 at `42678ae2`, #715 at `c7d0ad63`) and after; the slot memory peak and cap line; the CPU-ranges summary (`m == n == 12`, `g == s == 0`, `k == 4`, no WARNING line); the same-head verdict. Acceptance 5 is optional after that.
- Decide whether to file the follow-up Issue for the cleanup-entry signal window (S2), which `replay_slot` and `run_act_process` share. Carry S1 and S3 as optional.
- Keep `Relates to #730` (not `Closes`) until acceptance 3's verdict clause and acceptance 4 are measured.

## Clone integrity after probes

`receipts/clone-integrity.txt`:

- HEAD `31e53e82a4a1604569ccacba8473f21e70b9cbc0`, tree `9dc0b704562f67cab1d805b40d56a5c983ddcebb`; the index tree is identical.
- The worktree and index equal HEAD, with zero porcelain lines.
- `scripts/act_ci.py` is blob `ab097a5c`, mode 100755. `docs/testing/CI_WORKFLOWS.md` is blob `7d45d589`, mode 100644.
- Submodule gitlinks: gptp-processor `7dda9c3b`, protocol-processor `2ad2f845` and third_party/verilog-axis `48ff7a7e` are initialized at their pins; external `efeb541a` and third_party/lwSRP `08ee86e8` are not initialized and are unchanged.
- No edit was made to the clone. Every mutant and probe ran on copies under the packet's scratch directory.

R632-4 FINISHED
