[R632] NEGATIVE - exact head 5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646

Round R632-2, internal cleared-context review of PR #731 (issue #730). Exact head `5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646`, tree `5cdc1268e31a15c1962a15212e5ace9f9101a207`. Source base `dc4d06cb`; live dev `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`. Full diff `dc4d06cb..5ba8313a`: `scripts/act_ci.py` and `docs/testing/CI_WORKFLOWS.md` only. Round-2 delta `eb566634..5ba8313a`: commits `93215f07` (code and self-tests) and `5ba8313a` (docs).

The verdict is NEGATIVE because of one open MINOR finding, F1, under `Tests`. The shipped runner logic is correct at this head:

- Every R633-1 and R632-1 finding is resolved, and each R633-1 probe sequence passes.
- Two independent randomized campaigns of 3000 interleavings each found no shared job range. Both campaigns model event lag and act running concurrently with the reader. The second also injects faults.
- 30 of my 36 mutants are killed.

F1 is about the evidence. Four arms covering the round's own shutdown and monitor guarantees cannot fail for the defect they claim to detect. Probes show that the code at this head behaves correctly on all four.

## Reconstruction (public sources only)

1. AGENTS.md, CONTRIBUTING.md (act-first replication, trust boundary, lenses), docs/README.md.
2. Issue #730: body (acceptance 1-5); assignment 6131408752; disk note 6131691911; ruling 6131815815 (no replays in the lane, measurement after merge, `--selftest`/`--dry-run` evidence); TAKEN; REVIEW READY (round 1); round-2 instruction 6132404197 (items 1-6); REVIEW READY (round 2).
3. `docs/testing/CI_WORKFLOWS.md` "Act-first local replication" and "Parallel replay slots", and act v0.2.89 upstream source, read-only:
   - `pkg/model/workflow.go` (`GetMaxParallel`);
   - `pkg/runner/runner.go` (stage and matrix executors);
   - `pkg/runner/job_executor.go` and `run_context.go` (removal order);
   - `pkg/common/executor.go` (`NewParallelExecutor`).
4. The full diff and the four commits; then the round-2 delta.
5. Public author evidence `01847718:review-evidence/730-r1/author-r2/` (selftest, gates, mutants, dry-run, host-stub receipts).
6. Only after my own pass over the diff, probes and mutants: the prior public findings R633-1 (6132335284) and R632-1 (6132397037), and their published probe and mutant scripts, to run them at this head.

## Executed evidence (this round; receipts in MANIFEST.sha256)

The candidate runner's offline self-test and every probe ran only on a `git archive` extraction of the exact head. The extraction's `act_ci.py` blob is `89afd58a`, the same as `HEAD:scripts/act_ci.py`. Each run was inside a disposable unprivileged namespace boundary, `scripts/sandbox.sh`:

- no network;
- no `/run` and no Docker socket;
- a read-only system;
- writable scratch only.

No `act_ci.py` ran host-side or against a PR. No Docker, act, daemon, sudo or replay was used.

| Command / probe | Result |
| --- | --- |
| `act_ci.py --selftest` | rc 0, 490 `ok`, 0 FAIL, `selftest: PASS` (CPython 3.14.7, PyYAML 6.0.3, real CPU count 16). Also rc 0 with `os.cpu_count` stubbed to 1 and to 4, the hosted docs runner's size (`receipts/selftest-*.log`) |
| `ci_events.py --check` / `--selftest` | rc 0 (2016 items) / rc 0 (2828 arms) |
| `act_slot_proof.sh --selftest` | rc 0 (44 cases) |
| `check_py_idiom.py` / `--selftest` | rc 0 (long function 9 <= 9, too many parameters 7 <= 7, over-long 0) / rc 0 (54) |
| `check_baremetal_only.py --check` / `--selftest` | rc 0 / rc 0 (700 arms) |
| `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `--verify-anchors`, `check_doc_paths.py` | all rc 0 |
| `check_em_dash.py --base dc4d06cb` | rc 0, 0 findings over 120 added lines, arms 339/339 |
| `git diff --check dc4d06cb HEAD` | rc 0 |
| `scripts/probe_r2.py` (my independent model and probes) | rc 0, all PASS (`receipts/probes-head.log`); see below |
| `scripts/probe_shutdown.py` (shutdown guarantees) | rc 0, S1-S4 PASS at head (`receipts/probe-shutdown-head.log`) |
| `scripts/mutants_r2.py`, 36 mutants, 12 jobs | 30 killed; survivors K12, K13, K29, K31, K32, K36 (`receipts/mutants-r2.log`) |
| R633-1 `probe_cpu_ranges.py` (sha256 `87225dfc...`), byte-unchanged | Stops at a constructor-signature change: `JobCpuRanges` now takes an inspect reader (`receipts/r633-1-probe-unchanged-at-head.log`) |
| Same probe with a small adapter; every sequence byte-identical (`receipts/r633-1-probe-adapter.diff`) | The adapter adds an inspect reader on its inert daemon, the split-out join helper and a pid. rc 0, `CONTRACT VIOLATIONS=0`: F1, F2, F3 and F4 all PASS (`receipts/r633-1-probe-adapted-at-head.log`) |
| R632-1 `mutants.py` (sha256 `d2ced226...`), unchanged | 19 killed, including M13, M16, M17 and M23. M18 survives (live interrupt gate only). M08, M09, M20 and C24 have no anchor at this head (`receipts/r632-1-mutants-unchanged-at-head.log`) |

The first attempts of four gates refused for environment reasons and were re-run (`receipts/gates-summary.txt`):

- em-dash and TOC: the pinned renderer was missing from one venv;
- py-idiom: run in a copy without submodules;
- diff-check: run in a copy without object alternates.

### Independent probes at this head (`scripts/probe_r2.py`)

- **P1 restart, R633-1's sequence.** The sequence is `create A, update A, start A, die A, create B, update B, start B, start A`. A keeps `4-7`, B gets `8-11`, and the two never share a range.
- **P2 update applied, then the CLI times out.** A's `4-7` stays reserved and inspect shows A there. B gets `8-11`, and the warning says both.
- **P2b move and inspect both time out.** `4-7` stays reserved through A's `die`, and the later creates get `8-11` and `12-15`.
- **P3a slot 0 with too few CPUs.** Slot 0 refuses 4, 7, 8 and 19 CPUs for 4 containers, and 4 and 7 CPUs for 1 container.
- **P3b slot 0 at run level.** This runs the runner's own dry-run harness with the shipping `rtl-full` and its host pin replaced. On 19 CPUs it gives `REFUSED: replay slot 0 needs CPUs 0-19 ...` with the slot never entered. On 20 CPUs the slot is entered and gets `4-7..16-19`.
- **P4 injected reap failure with a failing body.** The order is contained, then the in-flight move finishes, then the stream ends, then the pipe closes, then the monitor exits. The reader thread has ended. The reap Refusal is raised, and the body's original failure is kept in its chain.
- **P7 derivation from a workflow file.**
  - Default gives 4.
  - Literal `2` and quoted `'3'` are honoured.
  - `5` is refused at the range step.
  - An expression and `0x4` are refused.
  - The shipping workflows derive `rtl-full` 4 and `docs`, `elaborate` and `rtl-fast` 1.
- **P8 independent layout check.** Slots 0-63 give 320 ranges. All are disjoint, every one is 4 wide (`nproc` 4), and slot N spans exactly `20N..20N+19`.
- **P9 and P10 randomized campaigns.** Each runs 3000 interleavings against an independent daemon model:
  - stopped containers keep their cpuset;
  - the record reads events with lag;
  - act creates, starts, kills and removes containers while the reader is inside an update or inspect call;
  - in P10, moves may be applied-then-timeout, lost-then-landing-late, or refused, and inspects may time out.

  The invariant is that no two existing containers ever stand on one job range, counting a pending move as standing on its target. It held in all 6000 runs. The campaigns can fail: K01 (`die` frees), K02 (a timed-out move frees), K05, K07 and K08 each fail P9 or P10 (`receipts/mutants-r2.log`).

## Findings

### F1: MINOR (Tests): four arms cannot fail for the defect they claim to detect, and the containment hold is not exercised

Authority: AGENTS.md section 6 `Tests`, "Each new test can fail for the defect it claims to detect". Round-2 instruction item 4 (6132404197) also applies: "block the Docker boundary's teardown until those obligations are met". The PR body and docs make the matching claims: "the join is retried until the reader is proven ended", "raises the first failure only afterwards", "A reader still running after its bounded wait is printed as a containment hold, and teardown waits for it", and "streams container events from a second before act".

Evidence (each mutant passes all 490 arms; `receipts/mutants-r2.log`):

- **(a) Join retry, mutant K12.** The mutant makes `join_job_cpu_reader` return at once after a failed join (`scripts/act_ci.py:5510`, `if failure is not None or not reader.is_alive()`). It survives.
  - The arm at `scripts/act_ci.py:7888-7910` is labelled "a reader join that fails is retried until the reader has ended".
  - Its stand-in reader lives 0.2 s, but the code pauses 0.25 s after a failed join (`:5509`). So the reader is always dead before the retry decision, and the arm cannot see a missing retry.
  - The author's N09 is killed only because it also drops the pause.
- **(b) Containment hold, mutant K13.** The mutant makes the join return the failure when the bounded wait expires with the reader alive, instead of holding (`:5512-5513`). It survives.
  - No arm has a reader that outlives `DOCKER_COMMAND_TIMEOUT + 10`.
  - The "survived its bounded shutdown" and hold branch (`:5512-5525`) is never reached by a timeout.
- **(c) First-failure precedence, mutant K36.** The mutant replaces `raise failures[0]` with `failures[-1]` (`:5571-5572`). It survives, because no arm combines two cleanup failures.
- **(d) Event window, mutant K32.** The arm at `:7703-7715` claims "from a second before act", but it checks only that `--since` is present, never its value (`:5623-5624`).
  - The mutant replays from an hour in the future and survives.
  - In that state the monitor reads no event, so every container stays on the staging range. No warning is printed: the record is empty and the summary reads "0 job container(s) created".

Impact: regressions that let Docker teardown overlap a live reader (a, b), or that report a later cleanup failure in place of the first (c), would pass every offline gate. So would one that silently disables every move (d). The code is correct today: `scripts/probe_shutdown.py` S1-S3 pass at head and fail on K12, K13 and K36 (`receipts/probe-shutdown-mutants.log`), and (d) is correct by reading. Only the live interrupt gate would catch (b) and (d), and it has not run in this lane.

Required outcome: make each arm able to fail for its claim. For example:

- a reader that is still running after the post-failure pause, for (a);
- a patched short bounded wait with a reader that outlives it, asserting the hold line, the recorded problem and a return only after the reader ended, for (b);
- a reap failure plus a join failure, asserting which one is raised, for (c);
- the `--since` value pinned against a stubbed clock, for (d).

Verification: re-run `scripts/mutants_r2.py`. K12, K13, K32 and K36 must be KILLED, and the unmutated self-test must still pass.

### Prior public findings, resolved or retained at this head

| Finding | Status at 5ba8313a | Evidence |
| --- | --- | --- |
| R633-1-F1 (`die` freed a restartable container's range) | RESOLVED | `observe` frees only on `destroy` or inspect-proven absence (`scripts/act_ci.py:5443-5459`, `5366-5370`). P1; R633-1 probe F1 PASS (adapted). K01 is killed by the self-test and by P1, P9 and P10 |
| R633-1-F2 (an uncertain update freed its target) | RESOLVED | The target is reserved before the update, and only `No such container` frees it (`:5420-5436`, `5372-5403`). P2, P2b, P10; R633-1 probe F2 PASS; K02, K03, K07 and K08 killed. The PR body publishes, as a material decision, that the range stays reserved until destroy even when inspect shows staging. That matches item 2's intent, since a late completion could otherwise land on a re-assigned range |
| R633-1-F3 (slot-0 silent fallback) | RESOLVED | `job_cpu_ranges` refuses on every slot (`:4687-4694`) and is called before `replay_slot` (`:5809-5822`). P3a and P3b; R633-1 probe F3 PASS; K15 killed |
| R633-1-F4 (a reap failure skipped the join) | RESOLVED | `stop_job_cpu_range_monitor` (`:5528-5572`) runs poll, containment, join and close whatever an earlier step raised. P4; R633-1 probe F4 PASS; K09, K10, K11 and K14 killed. The pinning of retry, hold and precedence is F1 above |
| R632-1-F1 (no arm failed without the reader join) | RESOLVED | `selftest_job_cpu_monitor_busy` (`:7779-7817`); R632-1 M13 and my K10 killed |
| R632-1-F2 (verdict invariance not pinned at run level) | RESOLVED | `selftest_cpu_range_warnings` (`:6477-6519`); R632-1 M16, M17 and M23, and my K23 and K24, killed |
| R632-1-R1 (mixed runner versions not in the authoritative doc) | APPLIED | `docs/testing/CI_WORKFLOWS.md:2141-2143` carries the exact sentence |
| R632-1-R2 (PR-body slot-0 fallback sentence) | APPLIED (superseded) | The PR body's Layout row now states the refusal on every slot, slot 0 included |
| R632-1-S1..S4 (suggestions) | Addressed | S1-S3 by R633-1-F1, F2 and F4 above. S4 by the new summary field `<g> removed before that` (`:5471-5479`) |

### SUGGESTIONS (optional; no lens impact)

- **S1 (Tests).** Two further properties are correct by reading and by probe S4, but no arm pins them:
  - the cleanup-signal mask held during `stop_job_cpu_range_monitor` (`:5543`; mutant K29 survives);
  - the problem line recorded when the reader crashes (`:5488-5489`; mutant K31 survives).
- **S2 (Robustness).** A first INT/TERM/HUP can land after the generator resumes in `job_cpu_range_monitor`'s `finally` (`:5657-5659`) and before `stop_job_cpu_range_monitor` masks signals (`:5543`). If it does, it raises there and skips containment and the join, and the `docker events` group never ends by itself. The window is a few bytecodes, and `replay_slot` and `run_act_process` share the same pattern. Masking signals across the whole `finally` would close it.
- **S3 (Robustness, diagnostics).** A join that raises at once is reported as "the CPU-range monitor survived its bounded shutdown" with a containment-hold line, although no bounded wait elapsed (`:5506-5525`; seen in probe S2's output). Distinguishing a failed join from a timed-out one would keep the warning accurate.

## Lens coverage at this head

```text
[R632] PASS Conformance — issue #730 acceptance 1-3 and ruling 6131815815 against scripts/act_ci.py:2043-2093 (derivation from the materialized checkout's workflows), 4624-4717 (layout, refusal on every slot), 5297-5479 (reservation until destroy/inspect), 5749-5759 and 5809-5822 (wiring, refusal before slot entry); git diff --name-status (two files; no workflow, step, job or gitlink change); act v0.2.89 GetMaxParallel/NewParallelExecutor/removal order; probes P1-P3, P7, P8; R633-1 probe F1-F3 (adapted). Acceptance 3's verdict clause, 4 and 5 deferred by the ruling (PR says Relates to #730)
[R632] PASS RTL — no HDL, CDC or interface file in the diff (git diff --name-status dc4d06cb..5ba8313a), so the hardware angles are inapplicable; architecture angles applied to the runner: single-writer record read only after the join (5482-5525, 5759, 15071-15081), reader started with cleanup signals blocked and its CLI calls on the worker branch of run_tracked_process_group_command (324-334, 5090-5160), containment through the existing ProcessSeams ladder (4932-4945, 5549-5556), CONTAINER_MEMORY/SLOT_MEMORY_MAX/CONCURRENT_JOB_LIMIT/CONTAINER_CPU_LIMIT and the act options word unchanged (diff search)
[R632] PASS Robustness — JobCpuRanges under restart, out-of-order and lagging events, applied/lost/refused moves, inspect timeouts, foreign/malformed events, gone-before-move (P1, P2, P2b, P9, P10 over 6000 interleavings; R633-1 probe adapted); shutdown under body return/raise/termination, reap failure, poll failure, failed join, reader outliving the bounded wait (P4, probe_shutdown S1-S4); host sizes 1-1280 and the slot-0 boundary (P3a, P3b, P8); max-parallel literal/quoted/expression/hex/too-wide (P7). S2 and S3 are SUGGESTIONS
[R632] MINOR Tests — scripts/act_ci.py:7703-7715, 7888-7910, 5506-5525, 5571-5572 — F1, UNCLEAN (K12, K13, K32, K36 survive). Examined: selftest_job_concurrency, selftest_cpu_layout_disjoint, selftest_job_cpu_ranges, selftest_job_cpu_record, selftest_job_cpu_move_failures, selftest_job_cpu_monitor(_busy/_failures), selftest_cpu_range_warnings, selftest_dry_run_cpu_ranges (6201-6519, 7052-7910, 14056-14135); 36-mutant campaign; R632-1 campaign unchanged; full gate set
[R632] PASS Docs — docs/testing/CI_WORKFLOWS.md:1554-1558, 1725-1847, 2133-2143, 2353 against the code (reservation lifetime, inspect placement, slot-0 refusal, shutdown order, mixed runner versions, pin list); repository-wide search for the stale 4N layout (none left); PR body and both REVIEW READY comments; docs_check, doc_style, gen_toc --check/--verify-anchors, check_doc_paths, check_em_dash all rc 0
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Issue #730 acceptance 1-3, the assignment, the ruling and round-2 items 1-6, against `scripts/act_ci.py:2043-2093, 4624-4717, 5297-5479, 5749-5759, 5809-5822`; diff name-status; act v0.2.89 source; P1-P3, P7, P8; R633-1 probe F1-F3 | R632-2 | 5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646 |
| RTL | CLEAN | No HDL, CDC or interface file in the diff. Runner architecture: single-writer record read only after the join (`5482-5525, 5759, 15071-15081`); worker signal branch (`324-334, 5090-5160`); reuse of the containment ladder (`4932-4945, 5549-5556`); resource constants unchanged | R632-2 | 5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646 |
| Robustness | CLEAN (S2, S3 SUGGESTION) | P1, P2, P2b, P4, P9 and P10 (6000 randomized interleavings); probe_shutdown S1-S4; P3a, P3b, P7, P8; R633-1 probe adapted | R632-2 | 5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646 |
| Tests | UNCLEAN (F1) | Self-test arms at `6201-6519, 7052-7910, 14056-14135`; `scripts/mutants_r2.py` (36 mutants, 30 killed); R632-1 `mutants.py` unchanged (19 killed, M18 live-only); gates | R632-2 | 5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646 |
| Docs | CLEAN | `docs/testing/CI_WORKFLOWS.md:1554-1558, 1725-1847, 2133-2143, 2353`; PR body; search for the stale layout; docs gates rc 0 | R632-2 | 5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646 |

No RESIDUE finding is recorded this round.

## Real limits

- **Nothing ran live.** This round and, per the PR, the lane both ran without:
  - a `docker events`, `docker container update` or `docker container inspect` command against a daemon;
  - the live `--interrupt-selftest`;
  - any replay.

  These rest on code reading and the act/moby sources:
  - the real event order under `--rm` (`destroy` before the next leg's `create`);
  - the owner label on `update`/`destroy` events;
  - a cpuset move under the slot slice;
  - inspect latency.

  M18 and K32 are pinned only by the live gate.
- **The safety invariant was shown against models.** It held against my daemon model, the self-test's model and R633-1's inert daemon, not a real daemon.
- **Host CPU count.** `os.cpu_count()` counts all CPUs, not online or affinity-allowed ones. This is the same as before #730. On a host whose CPUs are offline or restricted, a move fails, which is a warning and not a verdict.
- **Sandbox Python.** The sandboxed self-test ran on CPython 3.14.7 only. The hosted docs job uses 3.12, which the author recorded.
- **Hosted checks were incomplete at read time** (`receipts/hosted_check_runs.tsv`).
  - Succeeded: 15, including all four Yosys shards.
  - Skipped: 1, Physical gPTP (nightly and manual).
  - In progress: 8, including all five Verilator shards, `elaborate`, `docs-check` and `publication-census`.

  A skipped context is not executed coverage, and this round makes no hosted verdict.
- **No source bank and no hardware run.** No manager source bank ran at this head, and none is claimed or inferred. Physical calibration NOT RUN; field skips are not hardware proof.

## Pending manager duties

- F1 fix, then a re-review of the corrected head. Re-bank `Tests`. Any change to `scripts/act_ci.py` outside the self-test also un-covers `Conformance`, `RTL` and `Robustness` for the changed artifacts.
- The external review R633 is independent and still required.
- Hosted and act acceptance at the final head: `rtl-fast`, and exact-head `verilator-suites` and `yosys-portability` once ready. This is under the disk ruling.
- The current-dev candidate merge validation (builder and native banks) at the merge turn.
- An open public question from the round-1 REVIEW READY. A live `--dry-run` is not daemon-free on an isolated slot, which conflicts with ruling item 2's premise. It needs a decision or its own Issue.
- The post-merge measurement under the ruling.
  - Acceptance 3's same-head verdict clause and acceptance 4: before is the slot-0 replays of #721 at `42678ae2` and #715 at `c7d0ad63`; after is the first replay on the merged runner.
  - Read the plan line and the `CPU ranges:` summary. Expect `m == n`, `g == s == 0`, `k == 4`, and no `WARNING ... CPU ranges:` line.
  - Also read the verdict and the slot memory peak.
  - Optional acceptance 5 comes after that.
- Explicit maintainer merge authorization, then post-merge containment. Keep #730 open until its post-merge duties are discharged.

## Clone integrity

The review clone was never written to. Gates that needed it mounted it read-only, and every probe and mutant ran on scratch copies. After the round (`receipts/clone_integrity.txt`, `scripts/verify_clone.sh`):

- HEAD is `5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646` and the tree is `5cdc1268e31a15c1962a15212e5ace9f9101a207`.
- The index equals the tree in mode, id and path.
- All 1296 tracked non-gitlink entries were re-hashed: bytes and exec bits match.
- `git status --porcelain --untracked-files=all` is empty.
- The submodules match their gitlinks: gptp-processor `7dda9c3b`, protocol-processor `2ad2f845` and verilog-axis `48ff7a7e`. `external` and `lwSRP` are uninitialized, with gitlinks unchanged from `dc4d06cb` (`receipts/gitlinks_head.txt`).

R632-2 FINISHED
