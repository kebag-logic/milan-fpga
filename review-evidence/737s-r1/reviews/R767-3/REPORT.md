[R767] NEGATIVE - exact head 3b323864232fa430ec3a185f33ad7b30fbf1156b

# Internal review R767-3: issue #737 / PR #836, round 3 (e180ba30..3b323864, CI only)

Head `3b323864232fa430ec3a185f33ad7b30fbf1156b`, tree `4376620f4802804538f53114af5544aafa7b34ee`, base and live `dev` `e61a4afaa54a598ceec08b7b5879285256cc60b6`. Authorities: the round 3 ruling on #737 (issuecomment-6611061323) and the STOP ruling, option (d) (issuecomment-6611968916). This was a cleared-context pass over the delta, the published packets `author-r3` and `author-r3a` at `764886ec`, and the hosted runs. Prior findings were read only after the independent pass.

## Verdict

The code and docs do what the rulings ask, and they agree with each other. I checked every figure the brief names, items 1 to 5, against the hosted jobs API and the leg receipts and logs, and all of them hold over the cited runs. Every control I planted is refused.

The hosted `elaborate` run at this head (41705989293, attempt 1) is green:
- all five workers passed;
- the aggregate ran the union verifier, and it accepted;
- the aggregate's head-only checkout took 3 s, and the job took 21 s of its 3-minute limit;
- every LiteX simulation passed exactly once;
- only `elaborate-gates-1` saved the CPU-metadata key, at 438 B. Earlier runs saved it empty at 200 to 202 B, and the generated file is about 422 B.

The manager's warm-key re-run (attempt 2) is also green through its aggregate:
- `elaborate-gates-1` had a cache hit on the `elaborate-vexii-*` key and restored a 438 B entry. This is the non-empty restore the ruling asks for.
- The union verifier accepted again.
- The aggregate took 29 s, 15 s of it in its depth-1 checkout.

The same runs also break the PR's stated figures, and that is one MINOR finding (F1), so the verdict is NEGATIVE:
- Setup reached 559 s in attempt 1 and 739 s in attempt 2, against `SETUP = 485`.
- `test_gptp_tx_timestamp` took 477 s in attempt 2, against `LARGEST` 462.
- `elaborate-gates-2` took 1414 s in attempt 1, against its stated cold projection of 1381 s.
- By the PR's own re-measurement rule, `LEG_BUDGET` becomes 927 s, and every projection and margin changes.

No bound is broken yet:
- the legs (794 s at most) fit the recomputed budget;
- the slowest measured worker took 1535 s of its 2700 s limit;
- the aggregate is well inside 3 minutes.

At the new maxima, though, a cold LiteX worker 4 projects at 1967 s. That leaves only 133 s before the 600 s headroom line at 2100 s, and setup has risen 254 s across two attempts at this one head.

There are also two RESIDUE items, two SUGGESTIONs and some observations.

## Findings

### R767-3-F1 - MINOR - Conformance, Robustness, Docs - the exact-head hosted runs raise the setup, a `LARGEST` member, collector, tail and depth-one checkout components above their stated figures, and exceed worker 2's stated cold projection

- **Where:**
  - `scripts/ci_litex_legs.py:67-78` (`SETUP = 485`, which feeds `LEG_BUDGET = 1181`);
  - `docs/testing/CI_WORKFLOWS.md:3131-3178`, the "Own bound" table at 3215-3224 and the workflow figure at 3262-3271;
  - `scripts/ci_gate_workflows.py:59-64` (104 s projection, 76 s margin);
  - the PR body, Round 3 items 1 and 3 and the STOP row.
- **Authority:** round 3 ruling item 1 ("every stated projection and `LEG_BUDGET` is built from the largest measured value of each component over all cited hosted runs. That includes run 41678609075 at this head"). The STOP ruling item 1 keeps that rule and the re-measurement rule. The PR's own rule (`CI_WORKFLOWS.md:3180-3190`) says a component a later hosted measurement puts above its figure replaces that figure, and that `LEG_BUDGET`, every projection and the table are then recomputed. This brief's bar is "a stated bound the hosted runs break is a finding". My R767-2-F2 was this class of finding at the previous head.
- **Evidence:** from the jobs API and job logs of run 41705989293:
  - attempt 1: `receipts/figures-head-a1.txt`, `receipts/hosted-head-a1-setup-steps.txt`, `receipts/hosted-head-a1-member-rows.txt`;
  - attempt 2: `receipts/hosted/head-jobs-41705989293-a2.json`, `receipts/hosted-head-a2-setup-steps.txt`, `receipts/hosted-head-a2-member-rows.txt`.

  | Component | Stated | Head run, attempt 1 / attempt 2 | Cause in the head run |
  |---|---:|---:|---|
  | setup (span less gate and Verilator) | 485 | **559** (gates-2), 525, 513 / **739** (gates-1), 466 | full-history checkout up to 250 / 274 s; `Install LiteX at the pinned revisions` up to 277 / 250 s; VexiiRiscv placement up to 108 s |
  | `test_gptp_tx_timestamp` (`LARGEST`) | 462 | 459 / **477** | |
  | `elaborate-gates-2` span, cold | 1381 projected | **1414** measured (attempt 1) | Verilator 393 s; leg 462 s |
  | `Collect CI manifest` | 149 | **183** / not complete when read | |
  | `Cancel late CI failures` | 25 | **29** / not complete when read | |
  | largest depth-one checkout | 19 | **26** (`Cancel late CI failures`) / 15 (aggregate) | |
  | cold Verilator | 431 | 393 / restored | inside |
  | builder legs 0 / 1 | 1130 / 1119 | 1010, 737 / 1098, 710 | inside |
  | other members | `ci_litex_legs.py:51-60` | all inside (ctrl 240 / 277, soc 409 / 472, retained 236 / 331, cpu 52 / 70, boot 18 / 25, mem 11 / 14, gmii 0 / 0) | |

  Applying the PR's rule to both attempts gives:
  - `LEG_BUDGET` 2700 - 600 - 739 - 431 - 3 = **927** s. The legs at the updated `LARGEST` hold 477 / 448 / 794 s and still fit, so the partition does not change.
  - Builder workers project at 1869 / 1858 s, with margins 831 / 842 s.
  - LiteX workers project cold at 1650 / 1621 / 1967 s (margins 1050 / 1079 / 733 s), and at 1219 / 1190 / 1536 s with Verilator restored.
  - The aggregate projects at 26 + 85 = 111 s, a margin of 69 s.
  - The allowance is at least 111 + 183 + 120 + 29 = 443 s, pending attempt 2's collector and tail. The workflow figure becomes at least 2312 s with Verilator restored and 2410 s cold. Both are still measurements against acceptance 1, which stays open.
- **Impact:**
  - The stated setup, one `LARGEST` member, `LEG_BUDGET`, the five projections and their margins, and the aggregate margin all understate what the head's own hosted runs measured. One measured worker span is above its stated projection.
  - `LEG_BUDGET` as a gate is 254 s looser than current evidence allows: a leg between 928 and 1181 s would pass the refusal but break the 600 s headroom at the measured setup.
  - Nothing has reached a limit. The fullest leg holds 794 s and the slowest measured worker took 1535 s.
  - At the new maxima, a cold LiteX worker 4 sits only 133 s from the headroom line. Setup rose from 485 to 739 s across this one head's two attempts.
- **Required outcome:** one of the following.
  - (a) The figures, `SETUP`, `LARGEST` and the docs and PR text include run 41705989293 attempts 1 and 2 by the PR's stated rule, recomputed as above or from the author's own re-measurement, with no other change.
  - (b) A manager ruling that the exact head's own hosted runs feed the next re-measurement instead of gating this merge.

  This class recurs by construction. Setup has ranged from 92 to 739 s over the cited runs and this one, and every push makes a new exact-head run, so (a) may be needed again at the next head. Setup is dominated by the full-history worker checkout and the uncached LiteX install, which are the two candidates for acceptance 1 not taken here. Those candidates now protect the 600 s job-limit headroom too, not only acceptance 1. I recommend the manager decide between (a) and (b) explicitly, so review does not loop on this class, and weigh that growth when doing so.
- **Verification:** `python3 scripts/ci_litex_legs.py legs` still accepts, and every figure in `CI_WORKFLOWS.md`, the code comments and the PR body equals the component maxima over the cited runs plus 41705989293. Or, under (b), the ruling is linked from the PR.

### R767-3-R1 - RESIDUE - Docs - "their largest measured job times" omits the scope that makes 1244 true

- **Where:** `docs/testing/CI_WORKFLOWS.md:3145-3146`.
- **Evidence:** over the cited runs, worker one's largest job time is 2672 s (run 41554508699, when it carried the LiteX aggregate). 1244 s is its largest with the LiteX legs apart. The figure is right in that scope, and the preceding paragraph gives the 2672 s.
- **Exact fix:** replace "Their largest measured job times are 1254" with "Their largest measured job times with the LiteX legs apart are 1254".

### R767-3-R2 - RESIDUE - Docs - the 2700 s job-limit control is credited to the LiteX leg self-test, but it runs from the gate workflow self-test

- **Where:**
  - `docs/testing/CI_WORKFLOWS.md:3164-3166` ("`scripts/ci_litex_legs.py` derives it ..., and its self-test requires ...");
  - PR body, Round 3 item 1 ("Its self-test requires ...") and "How to validate" ("A mutant that sets a LiteX worker's limit to 44 minutes fails the LiteX leg self-test").
- **Evidence:** the assertion is in `scripts/ci_litex_legs_selftest.py:167-170`, inside `worker_controls`. That function is called only from `scripts/ci_gate_workflows_selftest.py:546`.
  - Probe p1 (`receipts/probes/p1-job-limit-2640.txt`) sets `JOB_LIMIT = 2640`. `python3 scripts/ci_litex_legs_selftest.py` exits 0, and `python3 scripts/ci_gate_workflows_selftest.py` exits 1 with `AssertionError: ('elaborate', 2, 45)`.
  - The author's own m01 control ran the gate self-test.
  - The guard is real and runs in CI (`.github/workflows/docs.yml:437`). Only its attribution is wrong.
- **Exact fix:**
  - Docs: replace "and its self-test requires each LiteX worker's generated limit to equal the 2700 seconds it starts from" with "and `ci_gate_workflows_selftest.py`, through the LiteX leg controls, requires each LiteX worker's generated limit to equal the 2700 seconds it starts from".
  - PR body: replace "fails the LiteX leg self-test" with "fails `ci_gate_workflows_selftest.py` in its LiteX leg controls", and "Its self-test requires" with "The gate workflow self-test requires".

### Suggestions (optional; they do not affect coverage)

- **S1 (Robustness):** the docs workflow's `docs-check` aggregate took 135 s at this head, 118 s of it in its full-history checkout, under the same 3-minute limit. The margin is 45 s and shrinks with the branch count. The author already lists this as a candidate Issue, and round 3 item 3 names elaborate jobs only. I recommend the manager open the Issue now. Evidence: `receipts/hosted/head-docs-jobs-41705989467-a1.json`.
- **S2 (Docs):** the PR body still carries the round 2 "Derived per job" table and workflow paragraph (973 / 1475 / 1745 s and so on). They are labelled "round 2 figures", but a cold reader meets them before Round 3. Collapsing them under a "superseded" heading would reduce misreading.

### Observations, not findings of this PR

- `docs-gates-2` took 1474 s at this head, against its unchanged projection of 1073 s, inside its 1620 s bound. That row was not touched by this delta.
- `ci/image/tool-inventory.json` still names `elaborate-gates-0`'s CPU-metadata cache and lists only workers 0 and 1. It was stale before this round and the PR body records it. `ci_tool_inventory.py --check` refuses here, for an environment reason (`CI_IMAGE_SHFMT`); the author reports it refuses at base on unrelated drift.
- Attempt 2 of 41678609075 (excluded from the cited set) was cancelled before any worker setup completed. Its largest component, a full-history aggregate checkout of 163 s, is now moot. Excluding it drops no larger figure.
- Run 41705989293 attempt 1 took 2340 s from first job start to last job end. The aggregate waited 448 s for a runner and the collector took 183 s. Acceptance 1 stays open, as the PR states.

## Focus items

1. **`LEG_BUDGET` from named constants.**
   - `scripts/ci_litex_legs.py:64-78` computes `JOB_LIMIT - HEADROOM - SETUP - COLD_VERILATOR - SELFTEST` = 2700 - 600 - 485 - 431 - 3 = 1181.
   - I traced each constant through my own jobs-API recomputation (`figures_r767.py`, `receipts/figures-cited.txt`):
     - setup 485: worker 3, 41678609075 attempt 3;
     - Verilator 431: worker 3, attempt 1;
     - self-test 3: the largest LiteX step less its rows, 596 - 593 in attempt 1.
   - `LARGEST` (`:51-60`) equals the per-member maximum over:
     - the 41583428850 leg receipts (`receipts/hosted-leg-rows.txt`);
     - the 41678609075 attempt 3 receipts;
     - the attempt 1 log rows (`receipts/hosted-a1-member-rows.txt`, which give cpu 72, mem 15 and retained 336).
   - `legs` prints 462 / 448 / 794 (`receipts/litex_legs.log`).
   - Boundary probes: soc 897 gives a leg of exactly 1181 and is accepted; 898 is refused at 1182 (p2, p3). A setup of 873 gives a `LEG_BUDGET` of 793 and is refused at 794 (p4).
   - The worker-timeout control exists and catches a changed limit, through the gate self-test (p1, R2).
   - **Holds over the cited runs. F1 at this head (setup 739, gptp 477, `LEG_BUDGET` 927).**
2. **Projections and the Own bound column.** By arithmetic:
   - 485 + 1130 = 1615 and 485 + 1119 = 1604;
   - 485 + 431 + 3 + {462, 448, 794} = 1381 / 1367 / 1713;
   - restored, 950 / 936 / 1282;
   - margins 1085 / 1096 / 1319 / 1333 / 987.

   The column is renamed "Own bound", and the exception sentence is at `CI_WORKFLOWS.md:3212-3213`. The cited spans 585 / 616 / 1226, 706 / 1021 / 1178 and 906 / 930 / 1194 are each below their projections. **Holds over the cited runs. F1 at this head (gates-2).**
3. **Workflow figure as a measurement.**
   - 1615 + 398 = 2013 and 1713 + 398 = 2111, which are 213 / 311 s above 1800. The allowance is 398 = 104 + 149 + 120 + 25.
   - The aggregate's rest of 85 s (234 - 149) and its 82 s lead come from attempt 3. The earlier 1953 = 1615 + 338, and 1723 = 255 + 1130 + 338.
   - The 208 / 143 / 59 s rise components are worker 3's in attempt 3.
   - "Ended 1767 s" (attempt 1) and "2646 s" (attempt 3) match. So does "workers waited up to 1043 s" (`elaborate-gates-1` in attempt 3; the 1209 s wait is the watcher's).
   - The text says "not a bound" and "acceptance 1 stays open" at `:3262-3264`, and the margin is 76 s.

   **Holds over the cited runs. F1 at this head (allowance at least 443, workflow at least 2312 / 2410).**
4. **Metadata cache and the head-only checkout.**
   - In the generated `elaborate.yml`, only `elaborate-gates-1` carries `Cache the generated CPU metadata` and its fill step. The other four carry neither, and the LiteX workers carry none of the four shared caches.
   - The aggregate checkout has no `with`, so it fetches at depth 1. Its limit is 3 minutes, `ci-manifest` keeps `fetch-depth: 0` under 15 minutes, and the workers keep theirs under 45.
   - The aggregate reads only `HEAD` and `HEAD^{tree}` (`ci_runtime_evidence.py:59-61`, `ci_gate_receipts.py`). `merge-base` is used only by `collect`, in `ci-manifest`.
   - Probes: p5 (head-only removed) and p6 (metadata on every worker) are each refused by `--check` and by the gate self-test. p7 drops the metadata cache from `BUILDER_CACHES` and regenerates: the workflow does not change and `--check` passes, but the gate self-test refuses on the literal names. That resolves R768-2-S1.
   - Hosted: the head's aggregate log shows `fetch-depth: 1`, a 3 s checkout and a 21 s job, and only worker 1 touches the `elaborate-vexii-*` key (cache miss, then saved at 438 B). The worker 0 and LiteX logs carry no `elaborate-vexii` restore or save.
   - **Holds.**
5. **Commit e2426156 and agreement.**
   - Worker 4 restored: 485 + 3 + 794 = 1282, which is now stated in the docs, the code comment and the PR body.
   - Every figure I checked in `CI_WORKFLOWS.md` and the PR body equals the code's constants and the jobs API over the cited runs. No round 2 figure survives in the docs (search for 973 / 1475 / 1745 / 1018 / 997 / 1077 / 607 / 586 / 666).
   - The command-table pin for `scripts/ci_litex_legs.py` equals its sha256, `f720579c...`.
   - The commits are one line each with no trailers. `git diff --check e61a4afa..HEAD` is clean.
   - Source-comment rule: the delta's added lines in `scripts/`, `.github/` and `ci/` carry no lane label, round, reviewer ID or comment ID. Run IDs only.
   - **Holds**, apart from R1 and R2.

## Hosted evidence at this head

| Run | Workflow | Attempt | Result when read |
|---|---|---|---|
| 41705989293 | elaborate | 1 | **success**. Workers 1535 / 1132 / 1414 / 1148 / 1233 s against 2700 s. Aggregate 21 s against 3 minutes; verify step "elaborate: 5 source gates exactly once; all worker jobs successful". Its exit 0 includes `ci_litex_legs.union` (`ci_gate_receipts.py:130-132`). 8 / 8 LiteX PASS rows, once each, in the worker logs (`receipts/hosted-head-a1-member-rows.txt`). |
| 41705989293 | elaborate | 2 | the manager's warm-key re-run. All five workers **success** (1304 / 1449 / 907 / 909 / 948 s). `elaborate-gates-1` log: "Cache hit for: elaborate-vexii-...", "Cache Size: ~0 MB (438 B)", "Cache restored successfully", and at post "Cache hit occurred on the primary key ..., not saving" (`receipts/hosted-head-a2-w1-metadata-restore.txt`). This is the **non-empty metadata restore**: 438 B against the 200 to 202 B empty entries of earlier runs. Aggregate **success** in 29 s (`fetch-depth: 1`, 15 s checkout), with "elaborate: 5 source gates exactly once; all worker jobs successful". 8 / 8 LiteX PASS rows once each. `Collect CI manifest` and the watcher were still running when read (20:52 UTC). Attempt 1's artifacts are hidden by this re-run (artifact list 0), so attempt 1's union and member figures come from its logs. |
| 41705989467 | docs | 1 | in progress; `docs-check` aggregate success in 135 s (S1). |
| 41705989299 / 41705989346 | rtl-fast / rtl-full | 1 | in progress / queued; not judged. |

## Prior public findings at this head

| Finding | Status at 3b323864 |
|---|---|
| R767-2-F1 / R768-2-F2 (worker 0 saves the metadata key empty) | **Resolved at its cause.** The metadata steps are on the generating builder only (`ci_gate_workflows.py:57-58, 461-494`). Hosted attempt 1 saved the key once, from `elaborate-gates-1`, at 438 B, and attempt 2 restored that 438 B entry on a cache hit. |
| R767-2-F2 / R768-2-F1 (bounds broken by the exact-head run) | **Resolved for the cited runs** by component maxima over every cited run, attempt 3 included. **The same class recurs at this head as R767-3-F1.** |
| R767-2-F3 / R768-2-F3 (aggregate at its 3-minute limit) | **Resolved.** Head-only checkout; hosted 3 s checkout, 21 s job, union proof run. |
| R767-2-R1 | Resolved: the sentence is gone. |
| R767-2-S1 | Applied: worker 1 = 485 + 1119 = 1604. |
| R768-2-S1 | Applied: literal names in the self-test; probe p7 confirms. |
| R768-2-S2 | Applied: 1883 / 2307 / 2825. |
| R768-2-S3 | Fill step off the LiteX workers. The placement-step split is declined with a reason (the copy is a no-op and the step is pinned), which I accept. |
| R768-2-S4 | Observation; no change needed. |
| R768-2-RS1 | Applied: exact text in the PR body's round 2 table, item 5. |

## Lens results

- `[R767] MINOR Conformance - scripts/ci_litex_legs.py:51-78; hosted 41705989293 a1 and a2 jobs API and logs - R767-3-F1`. Clean within the lens: ruling items 2 to 4 and STOP items 2 to 4 (metadata on the generator only, head-only aggregate, workflow figure stated as a measurement with acceptance 1 open, three legs kept, candidates recorded), the union proof green at the head, and every simulation run once and passing.
- `[R767] PASS RTL - scripts/ci_gate_workflows.py:45-66,262-270,461-494; .github/workflows/elaborate.yml (generated jobs, timeouts 45/45/45/45/45/3/15/120/3); scripts/ci_runtime_evidence.py:59-61` - the generator's step removal is exact per worker, `metadata_worker` derives the one builder from `ci_builder_legs.REQUIRED`/`ISOLATED`, and the aggregate needs no history. No timeout was raised. The job ordering and timing effects are understood and bounded by the job limit. F1's stale figures do not change any interface or ordering.
- `[R767] MINOR Robustness - hosted 41705989293 a1 and a2 (setup 559 / 739, gptp 477, collector 183, tail 29, depth-one checkout 26) - R767-3-F1`. Clean within the lens: limit and boundary refusals (p2 to p4), a changed worker limit (p1), split elaboration gates (the self-test plant), and the aggregate under a growing branch count (depth 1).
- `[R767] PASS Tests - scripts/ci_litex_legs_selftest.py:16-30,56-76,158-245; scripts/ci_gate_workflows_selftest.py:546; receipts/probes/p1..p7` - each new control fails for the defect it claims (p1, p5, p6, p7), the `LEG_BUDGET` boundary is exact (p2 / p3), and `--check`, the gate self-test, the LiteX self-test, `legs` and `ci_events.py --check` all exit 0 at the head.
- `[R767] MINOR Docs - docs/testing/CI_WORKFLOWS.md:3131-3271,3322-3333; PR body Round 3 - R767-3-F1`. Also RESIDUE R1 and R2. Clean within the lens: the arithmetic, the exception sentence, the re-measurement rule stated once, the metadata and checkout paragraphs, and no surviving round 2 figure.

## Gates and probes run at this head (16 CPUs or fewer; receipts in `receipts/`)

- `ci_gate_workflows.py --check` rc 0.
- `ci_gate_workflows_selftest.py` rc 0.
- `ci_litex_legs_selftest.py` rc 0.
- `ci_litex_legs.py legs` rc 0.
- `ci_events.py --check` rc 0.
- `git diff --check e61a4afa..HEAD` clean.
- Probes p1 to p7 (`probes_r767.sh`, plus the inline p7 receipt), each restored. Afterwards `git write-tree` = `4376620f...`, the worktree and index equal HEAD, and the three submodule gitlinks are unchanged (`receipts/restore-check.txt`).
- Not run: `ci_events.py --selftest`, `run_litex_sims.sh --selftest`, the three real LiteX legs, behave, `ci_scope.py --selftest`, act. For these I rely on the author's published receipts at `764886ec` (`author-r3/receipts`), whose listing I checked.

## Completion ledger (reviewer-owned)

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `ci_litex_legs.py:51-78`; the generated `elaborate.yml`; hosted 41705989293 a1 and a2; rulings 6611061323 / 6611968916 | R767-3 | 3b323864232fa430ec3a185f33ad7b30fbf1156b |
| RTL | CLEAN | `ci_gate_workflows.py:45-66,262-270,461-494`; the generated `elaborate.yml` jobs; `ci_runtime_evidence.py:59-61`; `ci_gate_receipts.py:110-191` | R767-3 | 3b323864232fa430ec3a185f33ad7b30fbf1156b |
| Robustness | UNCLEAN (F1) | hosted 41705989293 a1 and a2 jobs API and logs; probes p1 to p6 | R767-3 | 3b323864232fa430ec3a185f33ad7b30fbf1156b |
| Tests | CLEAN | `ci_litex_legs_selftest.py`; `ci_gate_workflows_selftest.py:546`; probes p1 to p7 | R767-3 | 3b323864232fa430ec3a185f33ad7b30fbf1156b |
| Docs | UNCLEAN (F1); R1 and R2 are RESIDUE | `CI_WORKFLOWS.md:1668-1724,3131-3333`; PR body at review (`receipts/pr-body-at-review.md`) | R767-3 | 3b323864232fa430ec3a185f33ad7b30fbf1156b |

## Real limits

- The jobs API's whole-second step timestamps limit every recomputed figure to ±1 s.
- Attempt 1's artifacts of both 41678609075 and 41705989293 are hidden by re-runs. Those member rows come from job logs.
- Cache contents cannot be read through the API. The restored entry is 438 B, against 200 to 202 B for the empty entries, which is consistent with the single generated file of about 422 B that the author's local cold run wrote.
- No manager source bank and no current-dev merge candidate were run or inferred. Physical calibration was NOT RUN, and field skips (for example the aggregate's "4 arm(s) did not run for recorded reasons") are not hardware proof.
- rtl-fast, rtl-full and docs at this head were not complete when read.

## Pending manager duties

- Rule on F1's two outcomes: (a) re-measure at this head, or (b) treat the exact head's run as input to the next re-measurement.
- Accept attempt 2 of 41705989293. It shows workers and aggregate green, the union proof, and a 438 B metadata restore on `elaborate-gates-1`. Its collector and watcher were still running when read, and their spans also feed F1's allowance.
- Judge rtl-fast, rtl-full and docs at this head, and the act replay.
- Open the docs-check aggregate checkout Issue (S1). Carry R1 and R2 to the residue checklist.
- Validate the current-dev merge candidate at the merge turn.

R767-3 FINISHED
