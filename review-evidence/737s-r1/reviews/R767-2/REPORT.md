[R767] NEGATIVE - exact head e180ba30eccc4ee7c3c699d88973816bdc953caa

# Internal review R767-2: issue #737 / PR #836, round 2 (aa3e2d85..e180ba30, CI only)

Tree `81e4b3aa8ae39d28ced04d217f01bb4f512212d5`. Base and live dev: `e61a4afaa54a598ceec08b7b5879285256cc60b6`. All five lenses were applied.

## Verdict in one paragraph

The round-2 code does what the rulings describe:

- `SECONDS` equals the hosted leg receipts of run 41583428850, byte for byte. I downloaded those artifacts myself.
- The partition re-derives to 461 / 440 / 520.
- `LEG_BUDGET = 973` is the stated arithmetic.
- Worker 1's figure is the maximum over the six cited runs.
- The LiteX workers carry none of the four shared cache steps.
- The act trust files are untouched.
- Every new guard is planted and can fail. Four disposable mutants were all killed.

The verdict is NEGATIVE because the first hosted run at this exact head (run 41678609075, attempt 1) breaks three things the PR states:

1. **F1: the cache race is not closed.** Builder worker 0 saved the CPU-metadata key as an empty 201-byte entry, and worker 1's save was refused. Worker 0 did the same in every cited run, base run 41470524727 included (200 or 201 bytes). Option (B) removes only the LiteX side of the race. The ruling's required check, a non-empty restore on `elaborate-gates-0/1`, cannot pass at this head.
2. **F2: two stated cold projections are exceeded.** `elaborate-gates-3` took 1021 s against its 997 s projection, and `elaborate-gates-4` took 1178 s against 1077 s. The 143 s setup and 411 s cold Verilator components behind them, and behind `LEG_BUDGET`, were exceeded too: setup reached 255 s and the cold Verilator build 431 s.
3. **F3: the aggregate hit its timeout.** The `elaborate` aggregate exceeded its 3-minute limit during checkout. Fail-fast then cancelled the run, so no hosted union proof exists at this head.

There is no timeout risk on the worker jobs: the largest worker took 1178 s against 2700 s. Every simulation ran exactly once and passed, in its re-derived leg.

## What was read (in order)

- `AGENTS.md`, `CONTRIBUTING.md` (by reference), the issue #737 body (scope 1, acceptance 1).
- The [A10] round 2 ruling (issuecomment-6596926489) and the STOP ruling, option (B) (issuecomment-6608788472).
- `git diff aa3e2d85..e180ba30` (7 files) and its five commits.
- The signed packet: `review-evidence/737s-r1/author-r2a` and `author-r2` at tree `4ad35a66`. All 132 files match `MANIFEST.json` `published_sha256` (`receipts/evidence-manifest-verify.txt`).
- Hosted job logs and the jobs API for runs 41470524727, 41476923392 (attempts 1 to 3), 41526004847, 41554508699 and 41583428850, and for run 41678609075 (the exact head, attempts 1 and 2).
- The prior public findings of R767-1 and R768-1, read only after my own pass over the delta.

## Findings

### R767-2-F1 - MINOR - Conformance, RTL, Robustness, Docs - builder worker 0 saves the CPU-metadata key empty, so option (B) does not close the race

- **Where:**
  - `scripts/ci_gate_workflows.py:45-50` (`BUILDER_CACHES` and its comment) and `:440-455` (`builder_caches`).
  - `.github/ci-templates/elaborate.yml:213-223` (the "a miss must cost one ~90 s Scala run" contract and the new "ONLY THE BUILDER WORKERS CARRY THIS CACHE" text) and `:344-348`.
  - `.github/workflows/elaborate.yml:145` (worker 0) and `:380` (worker 1).
  - `docs/testing/CI_WORKFLOWS.md:1689-1706`.
  - The PR body, item 3 row and "The cost of keeping the shared caches off the LiteX workers".
- **Authority:**
  - Ruling item 3: "A job saves a cache entry only if it generates its content" and "it must show a non-empty `Cache the generated CPU metadata` restore on `elaborate-gates-0/1`".
  - STOP ruling (B): "so only the builder workers populate those keys".
- **Evidence:** `receipts/hosted/vexii-cache-events.txt` lists each log's sha256 and the archive byte count the cache action logged.
  - **This head, run 41678609075 attempt 1:**
    - `elaborate-gates-0` missed the key, then at 17:06:46 logged `Sent 201 of 201` and `Cache saved with key: elaborate-vexii-e8d7156c…-a2886ad6…`.
    - `elaborate-gates-1` logged `Unable to reserve cache with key elaborate-vexii-…`.
    - The key at this head therefore holds an empty `~/vexii-netlist-args`, and the key has no `restore-keys`.
  - **Every cited run:**

    | Run | Worker 0 | Worker 1 |
    |---|---|---|
    | 41470524727 (base `e61a4afa`) | saved 200 B | save refused |
    | 41476923392 | saved 201 B | restored 201 B |
    | 41526004847 | restored 201 B | restored 201 B |
    | 41554508699 | restored 200 B | restored 200 B |
    | 41583428850 | save refused (worker 2 had saved 202 B) | save refused |

    No builder save of this key was ever non-empty. Worker 0's `Keep the generated CPU netlist arguments for the next run` copies nothing, which its `|| true` hides.
- **Impact:**
  - The second hosted run the rulings require will restore 201 B on both builders, by construction, so ruling item 3's acceptance cannot be met at this head.
  - The template contract text, `CI_WORKFLOWS.md:1694-1697` ("the builders' saves were refused", read as the only obstacle) and the PR's "only the builders populate those keys" each state an outcome the hosted run contradicts.
  - In every cited run, worker 1 regenerated its metadata on each run.
  - The "about 110 warm (100 to 113 inside the old aggregate)" contrast at `:1704-1705` and `:3146` is not a cache-warm figure. In 41526004847 and 41554508699 the restore was empty, so that metadata came from builder leg 1 earlier in the same job. Option (B) therefore did not create the cost it is said to cost.
  - Nothing fails or is skipped; the cost is undocumented time on the builder workers.
  - The empty save predates this PR (base run 41470524727). Ruling item 3 assigns it here, and the PR text claims it is closed.
- **Required outcome:** the conflict between the hosted evidence and the STOP ruling's premise is published and decided. Then one of these:
  - (a) The metadata key is saved only by a job that generated its content. Which job generates it is for the lane to establish; worker 1's saves were always refused, so no run shows it.
  - (b) The manager rules the cache inert. The template, `CI_WORKFLOWS.md` and the PR body then state that every builder run generates cold, with the measured cost.

  Either way, the stated "warm" contrast for `test_ctrl_memory` must name what it measured.
- **Verification:** on a second hosted run at the corrected head with an unchanged key, the `Cache the generated CPU metadata` restore on `elaborate-gates-0/1` is more than about 200 B. Alternatively, the manager's alternative ruling and the corrected text are on the PR. If `worker_controls` or `cache_controls` change, the Tests lens must be re-covered.

### R767-2-F2 - MINOR - Conformance, Robustness, Docs - the exact-head hosted run breaks two stated LiteX cold projections and the setup and Verilator components of `LEG_BUDGET`

- **Where:**
  - `docs/testing/CI_WORKFLOWS.md:3123-3149` and the table rows `:3169-3171` (1018 / 997 / 1077 cold).
  - `scripts/ci_litex_legs.py:26-54` (the `SECONDS` and `LEG_BUDGET` comments: "the 143-second setup", "the 411-second cold Verilator build").
  - The PR body, "Derived per job" table (cold 1018 / 997 / 1077).
- **Authority:**
  - Ruling item 1 (bounds from standalone measurements, the cold case over every invalidated cache).
  - The round bar: "a stated bound the hosted runs break is a finding".
- **Evidence:** run 41678609075 attempt 1 was cold, because the push changed every workflow-hashed key. Source: `receipts/hosted/timing-41678609075-a1.txt`, from the jobs API by `scripts/run_timing.py`. The same script reproduces the author's run 41583428850 table exactly (`receipts/hosted/timing-41583428850.txt`).

  | Job | Stated cold | Hosted | Setup (stated 143) | Cold Verilator (stated 411) | Leg step (stated leg + 3) |
  |---|---:|---:|---:|---:|---:|
  | `elaborate-gates-2` | 1018 | 706 | 184 | 274 | 248 (464) |
  | `elaborate-gates-3` | **997** | **1021** | 140 | **431** | **450** (443) |
  | `elaborate-gates-4` | **1077** | **1178** | **254** | 328 | **596** (523) |
  | `elaborate-gates-0` | 1475 | 861 | 255 | - | 606 |
  | `elaborate-gates-1` | 1240 | 1143 | 205 | - | 938 |

  - Member rows at this head (`receipts/hosted/exact-head-a1-extracts.txt`): `test_soc_timing_cuts` 369 s against `SECONDS` 240, `test_retained_cdc_storage` 336 against 331, `test_cpu_memory_port_cdc` 72 against 70, `test_pp_mem_bridge` 15 against 14, `test_ctrl_memory` 224 against 280, `test_gptp_tx_timestamp` 246 against 461.
  - Checkout alone took 24 to 157 s on the workers, against 16 to 23 s in run 41583428850.
  - At this head's setup and Verilator figures, a leg at `LEG_BUDGET` gives 255 + 431 + 3 + 973 + 270 = 1932 s, against the 1800 s the comment says it keeps.
- **Impact:**
  - Two published cold projections are below the measured span at the exact head, the same defect class as R767-1-F1.
  - `LEG_BUDGET`'s stated guarantee no longer follows from its own components.
  - No limit is at risk: 1178 s is inside the 1620 s per-job bound and the 2700 s timeout, and the largest leg (520 s measured, 596 s hosted) is far below 973.
  - `SECONDS` rests on one hosted run, as the author's open risk says. This run shows a member moving by +129 s and -215 s.
- **Required outcome:**
  - The stated cold projections and `LEG_BUDGET` hold against the exact-head hosted spans, with the runs they cite named. One way: each component is the maximum over the runs cited, run 41678609075 included, and the partition and `LEG_BUDGET` are re-derived from those maxima.
  - Alternatively, the text states a margin that it shows the hosted runs do not break.
  - Illustration, not a prescription: maxima over both standalone runs partition to 476 / 466 / 616. With setup 255 and Verilator 431 that projects at 1165 / 1155 / 1305 s cold, still under worker 0's 1475, with `LEG_BUDGET` = 1800 - 270 - 255 - 431 - 3 = 841.
- **Verification:**
  - Each documented LiteX cold figure is at or above the matching hosted span of every cited run: 706 / 1021 / 1178 at this head, and the own-leg reconciliation for run 41583428850.
  - `ci_litex_legs.py legs` and `ci_gate_workflows.py --check` agree with the text.

### R767-2-F3 - MINOR - Conformance, Robustness - the `elaborate` aggregate hit its 3-minute limit at the exact head, so no hosted union proof exists there

- **Where:** `.github/workflows/elaborate.yml:1218-1220` (job `elaborate`, `timeout-minutes: 3`) and its full-history `actions/checkout`. The PR body: "the aggregate keeps 3".
- **Authority:**
  - #737 acceptance 1 ("with the union proofs passing").
  - The fail-fast rule in the issue: a cancelled run is never a valid build.
  - The round bar: "a job at its timeout ... is a finding".
- **Evidence** (`receipts/hosted/exact-head-a1-extracts.txt`):
  - Run 41678609075 attempt 1: the aggregate started at 17:13:57, after 106 s queued.
  - Its checkout `git fetch --prune … +refs/heads/*:refs/remotes/origin/* +refs/tags/*` ran from 17:14:01 to 17:18:20.
  - Annotation: "The job has exceeded the maximum execution time of 3m0s".
  - `Require every gate exactly once` was skipped.
  - `Fail fast across this head` logged `{"first_failure": "elaborate", "conclusion": "cancelled"}` and cancelled the run and the sibling `docs` run.
  - Every checkout in this run was slow (24 to 260 s, against 2 to 24 s in run 41583428850), so the cause is hosted git latency against a limit and checkout that predate this PR. The delta does not touch either.
  - Attempt 2, the manager's re-run, was cancelled by the automation account at 17:25, before any job completed (`receipts/hosted/jobs-41678609075-a2-snapshot-1725Z.json`).
- **Impact:**
  - The exact head has no successful hosted `elaborate` run and no hosted LiteX union.
  - The 270 s aggregate/collector allowance was also exceeded: the aggregate ran 267 s plus its queue, and `Collect CI manifest` ran 149 s.
  - The wall clock from first job start to last job end was still 1767 s.
- **Required outcome:**
  - An exact-head hosted `elaborate` run whose aggregate completes and passes the union.
  - Either the aggregate is shown to fit its 3-minute limit under hosted checkout latency (the means are the executor's), or the manager rules that exposure out of this PR's scope by name, publicly.
- **Verification:** the manager's hosted readback shows `elaborate` success at this head (or its successor), with `Require every gate exactly once` executed and the gate-union artifact present.

### R767-2-R1 - RESIDUE - Docs - "its largest measured job time less that step over the six" reads as max(job) minus its step

- **Where:** `docs/testing/CI_WORKFLOWS.md:3117-3118`.
- **Evidence:** the figure is the largest of (job - step) over the six runs: 992, 1072, 1187, 1240, 1223, 1234. The largest job, 2740 in attempt 3, less its own step gives 1234. The figure 1240 is right; the sentence parses both ways.
- **Exact fix:** replace "so worker one projects at its largest measured job time less that step over the six, `2735 - 1495` in attempt 1," with "so worker one projects at the largest, over the six, of its measured job time less that step: `2735 - 1495`, in attempt 1,".

### R767-2-S1 - SUGGESTION - Conformance, Docs - worker 1's measured-span projection sits below its own component maxima

The largest setup plus the largest builder leg 1 over the cited runs is 143 + 1119 = 1262 s, against the projected 1240 s. Ruling item 2 is met: 1240 is the maximum of the measured figure, and worker 1 took 1143 s at this head. Stating 1262, or saying why the measured span suffices, would align it with "one setup figure everywhere". Neither bound moves.

### Observations, not findings of this PR

- **Package-cache save failure:** the `Cache exact package downloads 16` post-save still fails on all three LiteX workers at this head with `tar: ../../_temp/ci_packages_16/lock: Cannot open: Permission denied`. R767-1 recorded this as a candidate new Issue; it predates this PR.
- **Artifacts unavailable:** the artifacts of run 41678609075 list as 0 and download as 404 after the re-run, although the job logs show them uploaded. The exact-head member seconds above therefore come from the job logs' verdict rows, not from leg receipts.

## Focus items

1. **Item 1: SECONDS, partition, setup, cold case, `LEG_BUDGET`.**
   - `SECONDS` (`scripts/ci_litex_legs.py:37-46`) equals the `results` rows of the three hosted leg artifacts of run 41583428850. I downloaded them independently, and their canonical digests match the author's copies (`receipts/hosted/run-41583428850-leg-receipts/`).
   - `legs` prints 461 / 440 / 520 (`receipts/p03-litex-legs.log`). Longest-first onto the least-loaded leg, by hand, gives the same.
   - 1800 - 270 - 143 - 411 - 3 = 973.
   - Own-leg reconciliation for 41583428850: 797 / 1057 / 1238 against 585 / 616 / 1226 measured. This holds.
   - At this head it is broken: F2.
2. **Item 2: maxima.**
   - The job-less-step values over the six runs are 992, 1072, 1187, 1240, 1223 and 1234, so 1240 is the maximum.
   - Builder leg 1 ranged from 869 to 1119 s, with 1119 in attempt 3.
   - The 143 s setup is the maximum over the cited runs.
   - Recomputed from the jobs API in the author's `cited-runs-timing.txt`, which my script reproduces for run 41583428850.
   - Wording residue: R1; S1.
3. **Item 3: option (B).**
   - The generated workers 2 to 4 carry only `Cache exact Python downloads`, `Cache the pinned RV32 SDK`, `Cache the pinned Verilator build` and `Cache exact package downloads 16`. Workers 0 and 1 carry all four shared cache steps.
   - No generated step references a removed step's outputs.
   - The exactly-once precheck and the removal are guarded (mutants m1 and m4 killed).
   - The diff of `scripts/act_ci.py`, `scripts/ci_events.py` and `scripts/ci_tool_inventory.py` over the round is empty, and `ci_events.py --check` and `--selftest` pass (2199 items, 5507 arms).
   - The act sandbox acceptance rests on the author's `g19` receipt; I may not run it.
   - The cold-metadata cost is folded into the projections. The race itself is not closed: F1.
4. **Item 4: queueing.**
   - `CI_WORKFLOWS.md:3214-3226` and PR body lines 78 to 82 state that the projection excludes runner queueing.
   - They record 1882 / 2306 / 2824 s and the 1268 s and 388 s waits, name queueing as the cause, and leave acceptance 1 open on #737. This is met.
   - Spans from the jobs API: 1883 / 2307 / 2825 from first job start. The 1 s difference is rounding of sub-second start times; the ruling's figures are quoted.
5. **Item 5: R1 and the suggestions.**
   - R767-1-R1's exact text is at `CI_WORKFLOWS.md:1683`.
   - R768-1-S2 is applied as a comment. It is accurate: the per-leg `executed != legs[leg]` check (`ci_litex_legs.py:160-164`) refuses a repeat first, because the legs are disjoint.
   - R768-1-S3's boolean exit is applied with a plant (m3 killed).
   - R767-1-S1's disjoint-worker check is applied with a plant (m2 killed).
   - The declined items each carry a reason in the PR body.

## Prior public findings at this head

| Finding | Status at e180ba30 | Evidence |
|---|---|---|
| R767-1-F1 | Resolved as specified for run 41583428850. The same class recurs at this head as R767-2-F2. | Focus 1; F2 |
| R767-1-F2 | Resolved: the queueing exclusion is stated, spans recorded, manager decision recorded. No LiteX worker queued at this head (2 s each). | Focus 4 |
| R767-1-R1 | Resolved (exact text) | `CI_WORKFLOWS.md:1683` |
| R767-1-S1 | Partly taken (disjoint-worker assertion); the rest declined with reasons | m2; PR body item 5 |
| R768-1-F1 | Resolved as R767-1-F1; superseded by R767-2-F2 | Focus 1 |
| R768-1-F2 | Resolved: each figure is the maximum over the cited runs. S1 is optional. | Focus 2 |
| R768-1-F3 | **Not resolved at its cause; retained as R767-2-F1.** Its premise that worker 0 saved generated arguments at base does not hold: it saved 200 B. | F1 |
| R768-1-S1 | Declined with reason | PR body item 5 |
| R768-1-S2 | Taken (comment); the comment is accurate | Focus 5 |
| R768-1-S3 | Boolean exit taken (m3); trailing comma declined with reason | Focus 5 |

## Lens results

- `[R767] MINOR Conformance - .github/workflows/elaborate.yml:145 and hosted run 41678609075 a1 worker 0 log - R767-2-F1`. Also F2 and F3. Clean within the lens: `SECONDS`, partition, `LEG_BUDGET` arithmetic, item 2 maxima, item 4 text, item 5. No timeout raised (workers 45, aggregate 3). No step made conditional. All 8 simulations ran once and passed in the re-derived legs at this head (1 + 5 + 2, `selection: … the reconciliation covered all of it` in each leg).
- `[R767] MINOR RTL - scripts/ci_gate_workflows.py:45-50,440-455; .github/workflows/elaborate.yml worker cache steps - R767-2-F1`. Clean within the lens: the generated delta removes exactly 12 steps (4 cache steps on each of 3 workers). It leaves no dangling `steps.<id>` reference on any job, and every other job, the builders included, is identical to `aa3e2d85` (`receipts/generated-structure.txt`).
- `[R767] MINOR Robustness - hosted run 41678609075 a1 (worker 0 save, aggregate timeout, jobs API spans) - R767-2-F1, F2, F3`. Clean within the lens: a boolean exit, a LiteX leg on a builder worker, a builder lacking a shared cache and a LiteX worker repeating one are each refused, naming the job (`receipts/p05-gate-selftest.log:184-186,266`).
- `[R767] PASS Tests - scripts/ci_litex_legs_selftest.py:87,147-175; scripts/ci_gate_workflows_selftest.py (run); receipts/mutation-probes.txt - each new plant fails for its defect`.
  - Mutants m1 to m4, which drop the removal, the disjoint check, the integer-exit check and the exactly-once precheck, are each killed.
  - At this head, `ci_gate_workflows.py --check`, the gate self-test, `ci_litex_legs_selftest.py`, `run_litex_sims.sh --selftest` (16/16), `ci_events.py --check` and `--selftest`, `ci_scope.py --selftest` and `git diff --check e61a4afa HEAD` all exit 0.
- `[R767] MINOR Docs - .github/ci-templates/elaborate.yml:213-223; docs/testing/CI_WORKFLOWS.md:1689-1706,3123-3149,3169-3171; PR body - R767-2-F1, F2`. Also RESIDUE R1. Clean within the lens: the item 4 text, the R1 text, and the item 2 figures as stated.
- **Comment rule:** the added source and template lines carry no lane labels, lane names, review rounds, reviewer IDs or issue-comment IDs. Run IDs and `#737` only.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | #737 scope 1 / acceptance 1; both rulings; `scripts/ci_litex_legs.py`; generated `elaborate.yml`; leg artifacts of run 41583428850; jobs API and logs of runs 41470524727, 41476923392 a1-a3, 41526004847, 41554508699, 41583428850, 41678609075 a1/a2 | R767-2 | e180ba30eccc4ee7c3c699d88973816bdc953caa |
| RTL | UNCLEAN (F1) | `scripts/ci_gate_workflows.py`; `.github/ci-templates/elaborate.yml`; per-worker cache steps and step references of `.github/workflows/elaborate.yml`; builder metadata cache events in nine cited-run logs plus two exact-head logs | R767-2 | e180ba30eccc4ee7c3c699d88973816bdc953caa |
| Robustness | UNCLEAN (F1, F2, F3) | union and generator refusals; hosted ordering of cache saves; exact-head spans and aggregate timeout | R767-2 | e180ba30eccc4ee7c3c699d88973816bdc953caa |
| Tests | CLEAN | `scripts/ci_litex_legs_selftest.py`, `scripts/ci_gate_workflows_selftest.py`, `scripts/run_litex_sims.sh --selftest`, `ci_events.py --selftest`, `ci_scope.py --selftest`; mutants m1 to m4 | R767-2 | e180ba30eccc4ee7c3c699d88973816bdc953caa |
| Docs | UNCLEAN (F1, F2); RESIDUE R1 | `docs/testing/CI_WORKFLOWS.md` round-2 hunks; template comments; live PR body (equal to the packet's `author-r2/PR-BODY.md` apart from one trailing newline) | R767-2 | e180ba30eccc4ee7c3c699d88973816bdc953caa |

## Gates and probes run at this head (16 CPUs, foreground)

- `receipts/p01` to `p09` (`.log` and `.rc`): generator check, events check and self-test, `legs`, the LiteX legs self-test, the gate self-test, the runner self-test, the scope self-test, and `git diff --check`. All rc 0.
- `receipts/probe-m*`: the mutants. The in-clone edits were restored with `git checkout`. The clone is clean at `e180ba30`, with `git status` empty.
- No submodule gitlink was touched.

## Real limits

- I did not run the act sandbox validation, act or `act_ci` (not allowed). Option (B)'s act acceptance rests on the author's `g19` receipt.
- I did not run the LiteX leg simulations locally. Execution evidence is the author's local leg receipts and the hosted logs.
- The exact-head hosted leg receipts were unavailable (404), so member seconds there come from job-log verdict rows.
- Only one exact-head hosted run completed, attempt 1, and it ran during unusually slow hosted checkouts. Attempt 2 was cancelled before any job finished, so there is no warm-key observation. F1 rests on attempt 1 and the cited runs.
- I did not establish which builder leg, if any, generates the metadata content, because worker 1's saves were always refused.
- No manager source bank exists at this head, and none is claimed. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Decide the F1 conflict: option (B)'s premise against the builder-0 empty save. Then trigger a hosted run with the key unchanged, and read the `elaborate-gates-0/1` metadata restore size.
- Obtain a successful exact-head hosted `elaborate` run with the union executed (F3). Re-run only after the head's sibling runs settle, since attempt 2 was cancelled by the automation account. Rule on the aggregate-limit scope.
- Hosted and act acceptance; the current-dev merge candidate (builder and native banks); carrying RESIDUE R1 to the residue checklist; the package-downloads cache observation as a candidate Issue.

R767-2 FINISHED
