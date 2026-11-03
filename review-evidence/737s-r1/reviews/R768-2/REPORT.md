[R768] NEGATIVE - exact head e180ba30eccc4ee7c3c699d88973816bdc953caa

# External review R768-2: issue #737 / PR #836, round 2 delta `aa3e2d85..e180ba30`

Tree `81e4b3aa8ae39d28ced04d217f01bb4f512212d5`. Source base and live dev are both `e61a4afaa54a598ceec08b7b5879285256cc60b6`. Cleared-context external review. I read, in order: AGENTS.md, CONTRIBUTING.md, docs/README, the #737 body, the manager's round 2 ruling (issuecomment-6596926489), the STOP and its option (B) ruling (issuecomment-6608788472), the executor's TAKEN and REVIEW READY comments, the diff and history, the published author packets (`review-evidence/737s-r1/author-r2a` and `author-r2` at `4ad35a66`), and the hosted logs of both attempts at this head. I read the prior round's findings (R767-1, R768-1) only after my own pass.

## Verdict

The round 2 code does what the rulings asked for:

- The LiteX workers carry none of the four shared cache steps.
- The generator refuses a missing or repeated step, and a LiteX leg on a builder worker.
- The act trust set is untouched.
- Every figure the round derives from run 41583428850 recomputes exactly.

Three things fail the bar, all on hosted evidence at this exact head (elaborate run 41678609075):

1. **F1.** Two stated cold bounds are broken. `elaborate-gates-3` took 1021 s against 997, and `elaborate-gates-4` took 1178 s against 1077. The single 143 s setup figure was exceeded on four of five workers.
2. **F2 (R768-1-F3, retained).** The CPU-metadata key is still saved empty, now by builder worker 0, which never produces the metadata: "Sent 201 of 201". The manager's re-run then restored `~0 MB (201 B)` on `elaborate-gates-1`. The ruling's check (a non-empty restore on gates-0/1) fails. The same 200-byte builder save predates the split.
3. **F3.** The `elaborate` aggregate hit its 3-minute timeout in checkout, so the hosted union proof did not run at this head. Fail-fast then cancelled all four workflows of the head.

No worker came near its 45-minute limit, and every simulation ran once and passed. Each finding is MINOR.

## Findings

### F1 - MINOR - Conformance, RTL (resource/timing effects), Robustness, Docs - the restated LiteX cold bounds and the one setup figure are broken by the exact-head hosted run

- **Where:**
  - `docs/testing/CI_WORKFLOWS.md:3121-3149` (the one 143 s setup; "1018, 997 and 1077 seconds for legs 0 to 2"; "the cold one").
  - `docs/testing/CI_WORKFLOWS.md:3169-3171` (the `(cold)` rows).
  - `scripts/ci_litex_legs.py:29-54` (`SECONDS`; the `LEG_BUDGET = 973` derivation, "so that a cold LiteX worker keeps the workflow inside its 30 minutes").
  - The PR body's "Derived per job" table (`elaborate-gates-3` 997, `elaborate-gates-4` 1077 cold).
- **Evidence:** run 41678609075 attempt 1, the first run at this head, on new keys, so every LiteX worker built Verilator. Sources: `receipts/hosted/jobs-41678609075-a1.json`, `run-41678609075-a1-spans.txt`, `run-41678609075-a1-log-excerpts.txt`, and the three leg receipts. Setup is the job span less the gate/leg step and the Verilator build, as the docs define it.

  | Job | Stated bound (s) | Measured span (s) | Setup (stated 143) | Verilator build (stated 411) | Leg step (stated leg seconds) |
  |---|---:|---:|---:|---:|---:|
  | `elaborate-gates-0` | 1475 | 861 | **255** | - | 606 |
  | `elaborate-gates-1` | 1240 | 1143 | **205** | - | 938 |
  | `elaborate-gates-2` (cold) | 1018 | 706 | **184** | 274 | 248 (461) |
  | `elaborate-gates-3` (cold) | 997 | **1021** | 140 | **431** | 450 (440) |
  | `elaborate-gates-4` (cold) | 1077 | **1178** | **254** | 328 | 596 (520) |

  - Member seconds, this head against `SECONDS`:
    - `test_soc_timing_cuts` 369 against 240;
    - `test_retained_cdc_storage` 336 against 331;
    - `test_cpu_memory_port_cdc` 72 against 70;
    - `test_pp_mem_bridge` 15 against 14;
    - `test_gptp_tx_timestamp` 246 against 461;
    - `test_ctrl_memory` 224 against 280.
  - The checkout step took 24 to 157 s on the workers here, against 16 to 24 s in run 41583428850. That is most of the setup excess.
  - At this run's setup (255 s) and Verilator build (431 s), a leg at the 973 s `LEG_BUDGET` would project to 255 + 431 + 3 + 973 = 1662 s. That is above the 1530 s (1800 − 270) the comment says the budget protects.
- **Impact:**
  - The published cold per-job figures are not bounds: the first exact-head hosted run exceeds two of them, by 24 s and 101 s.
  - `LEG_BUDGET`'s stated guarantee rests on a setup and a Verilator figure this run exceeded.
  - No timeout risk: the largest worker was 1178 s against 2700 s.
  - Worker 0's 1475 s, which binds the 1745 s workflow projection, is not broken.
  - This is the second round in which a single-run source understated a stated bound (compare R768-1-F1).
- **Required outcome:**
  - Every stated LiteX-worker cold figure, the setup figure and the `LEG_BUDGET` derivation hold against every exact-head hosted run, 41583428850 and 41678609075 at least. For example, take setup, the Verilator build and each member's seconds as maxima over those runs, or state a measured variance margin.
  - The docs rows, the `LEG_BUDGET` comment and the PR body agree and name the runs.
  - Ruling item 1 fixed `SECONDS`'s source to run 41583428850's receipts. If widening that source needs a decision, the executor publishes the conflict and the manager rules.
- **Verification:**
  - Recompute from the jobs API of both runs.
  - Each restated cold figure is at or above both runs' spans.
  - `python3 scripts/ci_litex_legs.py legs` stays under the restated budget.
  - `ci_gate_workflows.py --check` and the self-tests pass.

### F2 - MINOR - RTL (resource/timing effects), Robustness (inter-job ordering), Conformance (ruling item 3), Docs - R768-1-F3 retained: the CPU-metadata key is saved empty by builder worker 0, so option (B) does not close the empty save

- **Where:**
  - `.github/ci-templates/elaborate.yml:213-223`. The key has no `restore-keys`. "a miss must cost one ~90 s Scala run". "ONLY THE BUILDER WORKERS CARRY THIS CACHE ... a LiteX worker, which never runs the elaboration, saved an empty metadata entry".
  - `scripts/ci_gate_workflows.py:45-50` (the `BUILDER_CACHES` comment).
  - `docs/testing/CI_WORKFLOWS.md:1689-1695` ("so only the builders populate those keys").
  - The PR body's item 3 row.
- **Evidence:**
  - **This head, attempt 1** (`receipts/hosted/run-41678609075-a1-log-excerpts.txt`):
    - `elaborate-gates-0` finished first, at 861 s. Builder leg 0 runs one gate (gate 1b: "SUBSET: 1 of 107 gates ran").
    - It saved `elaborate-vexii-e8d7156c…-a2886ad6…` as "Sent 201 of 201 (100.0%)" at 17:06:46.
    - `elaborate-gates-1` was then refused: "Unable to reserve cache with key elaborate-vexii-…" at 17:11:30.
  - **This head, attempt 2** (the manager's re-run; `receipts/hosted/run-41678609075-a2-gates-1-log-excerpt.txt`): `elaborate-gates-1` "Cache Size: ~0 MB (201 B)" and "Cache restored from key: elaborate-vexii-e8d7156c…-a2886ad6…". `elaborate-gates-0` was cancelled in checkout before its restore (see F3).
  - **Before the split** (`receipts/hosted/earlier-runs-vexii-cache-lines.txt`):
    - Run 41470524727: builder `elaborate-gates-0` saved the key as "Sent 200 of 200", and `elaborate-gates-1` was refused.
    - Runs 41526004847 and 41554508699 restored "~0 MB (201 B)" and "(200 B)" on both builders.
  - So a builder whose gates do not produce the metadata saves the empty first entry as well. R768-1-F3's line "the first finisher holding that key was builder worker 0, which saved its generated arguments" was wrong, and I correct it here.
  - The other three builder caches now work at this head. The re-run restored sv2v (2,157,523 B), pip pins (6,024,638 B) and sbt (57,017,278 B), all saved by builder worker 0.
- **Impact:**
  - Ruling item 3's verification, a non-empty `Cache the generated CPU metadata` restore on `elaborate-gates-0/1`, cannot be met at this head on this key.
  - The cache is non-functional. The template's "one ~90 s Scala run per miss" is in fact every run.
  - The template and docs text attribute the empty entry to the LiteX workers alone.
  - No stated builder bound moves. Every cited builder run already ran with empty metadata, so the regeneration cost is inside the measured builder figures.
- **Required outcome:**
  - The metadata key is never saved without generated content: saved only by a job whose run produced the metadata, or not saved when the directory is empty. Or the manager rules on an alternative, for example declaring the cache ineffective and dropping it.
  - The template contract, the `BUILDER_CACHES` comment, CI_WORKFLOWS.md and the PR body state the actual behaviour.
  - The design choice belongs to the executor and, where it crosses the ruling, to the manager.
- **Verification:** a hosted run on the same key shows a non-empty metadata restore on `elaborate-gates-0/1`, or the manager's alternative is recorded and the text matches it.

### F3 - MINOR - Conformance (#737 acceptance 1, "with the union proofs passing"), Robustness (timeout path), RTL (timing) - the exact-head hosted union proof did not run: the `elaborate` aggregate hit its 3-minute timeout in checkout

- **Where:** `.github/workflows/elaborate.yml:1220` (`timeout-minutes: 3`) and the same job's `actions/checkout@v4` with `fetch-depth: 0`. Both are unchanged from dev `e61a4afa`, so the delta did not introduce this.
- **Evidence:**
  - Job 126077456636, annotation: "The job has exceeded the maximum execution time of 3m0s" (`receipts/hosted/run-41678609075-a1-elaborate-annotations.json`).
  - The checkout ran from 17:14:00 to 17:18:20 in "Fetching the repository", then "The operation was canceled".
  - "Require every gate exactly once" was skipped.
  - The fail-fast watcher logged `{"first_failure": "elaborate", "conclusion": "cancelled"}` and "Cancelled runs: [41678608971, 41678608972, 41678609009, 41678609075]".
  - Attempt 2 (started 17:22) was cancelled across all jobs at about 17:25, during checkout (`receipts/hosted/jobs-41678609075-a2.json`).
  - Attempt 2's cancelled receipts replaced attempt 1's `gate-elaborate-*` artifacts. My copies of the three attempt-1 LiteX leg receipts were taken before that, and they hash in `MANIFEST.sha256`.
- **Impact:**
  - At this head there is no hosted proof that every gate and every LiteX simulation ran exactly once.
  - One slow fetch in a 3-minute job cancels every workflow of the head.
  - Offline, my own union over the three exact-head hosted leg receipts passes ("litex: 8 simulations exactly once, each a pass", `receipts/g09-union-over-41678609075-a1-receipts.log`). That is local evidence, not the hosted proof.
- **Required outcome:**
  - An exact-head hosted elaborate run whose aggregate passes "Require every gate exactly once" within its budget.
  - The manager decides whether a checkout that can exceed the 3-minute aggregate budget is #737's to fix, or belongs to a new Issue. #737 forbids raising a timeout, and a finding moved to another Issue is not resolved for this lens ledger.
- **Verification:** the manager's hosted readback names a completed exact-head aggregate with the union step green.

### Suggestions (optional; they do not affect coverage)

- **S1 (Tests):** `worker_controls` and `cache_controls` read `BUILDER_CACHES` from the implementation (`scripts/ci_litex_legs_selftest.py:150-175`).
  - Mutant m6 drops `"Cache the generated CPU metadata"` from the constant and regenerates the workflow. That puts the metadata cache back on `elaborate-gates-2`, yet `ci_gate_workflows.py --check`, `ci_gate_workflows_selftest.py` and `ci_events.py --check` all pass (`receipts/mutants/m6-regenerated.txt`).
  - Only the regenerated workflow diff would show it. Pinning the four names literally in the self-test, or against the CI_WORKFLOWS.md sentence, would make the control independent of the constant it checks.
- **S2 (Docs):** the recorded spans 1882, 2306 and 2824 s (`docs/testing/CI_WORKFLOWS.md:3218-3219`, PR body) are 1 s under the jobs API's whole-second figures: 1883, 2307 and 2825 from the 05:21:24 first start (`receipts/hosted/run-41583428850-spans.txt`). The author's own `cited-runs-timing.txt` also says 1883, 2307 and 2825. This is within timestamp truncation, so it is not a defect. Matching the receipt, or writing "about", would remove the mismatch.
- **S3 (RTL/Robustness):** two steps on the LiteX workers are now dead:
  - "Place the VexiiRiscv source at the revision LiteX pins" still copies from an always-empty `~/vexii-netlist-args`.
  - "Keep the generated CPU netlist arguments for the next run" copies into a directory that no cache on those workers saves, so its "for the next run" cannot happen.
  - Both are harmless (`|| true`). The second could leave the LiteX workers with the four caches, or its name could be qualified.
- **S4 (Robustness), observation:** `Cache exact Python downloads` (`~/.cache/pip`, key `python-cpython3.12.3-…`) is still shared by builders and LiteX workers. Both install the same pins (`.github/workflows/elaborate.yml:130` and `:365` on the builders, `:584`, `:830` and `:1076` on the LiteX workers), so a LiteX-first save is not empty. It is outside the ruling's four, and I found no defect.
- **Observation carried from R767-1 (not this delta):** the `Cache exact package downloads 16` post-save tar failure ("tar exit code 2") recurs on the LiteX Verilator-miss workers at this head (`elaborate-gates-2` log). It predates this PR.

### RESIDUE (wording only; does not affect the verdict or coverage)

- **RS1 - PR body, Round 2 table, item 5 row:** "because each needs a new content pin for that script and the runtime union already refuses each by name". The trailing-comma case (R768-1-S3) is refused by nothing. `--only a,` runs exactly `a`, and the generated step never emits a trailing comma, so the clause overstates. **Exact fix:** "because each needs a new content pin for that script; the runtime union refuses a truncated selection and a FAIL row by name, and the generated step never emits a trailing comma."
- **Source-comment rule:** I scanned the delta's added lines in `scripts/` and `.github/ci-templates/` for lane labels, round or reviewer IDs and comment IDs. None found.

## Focus items (round 2 brief)

1. **`SECONDS`, partition, setup, cold case, `LEG_BUDGET`.**
   - All eight `SECONDS` values equal the verdict rows of run 41583428850's three leg receipts. I downloaded `gate-elaborate-2/3/4` myself and they are byte-identical to the published receipts. They bind merge commit `6570ad60`, whose parents are `e61a4afa` and `aa3e2d85`.
   - `ci_litex_legs.py legs` gives 461 / 440 / 520.
   - One setup figure, 143, is used everywhere, and it is the maximum over the cited runs.
   - Cold projections recompute: 143 + 411 + 3 + leg = 1018 / 997 / 1077, and warm 607 / 586 / 666. The reconciliation 797 / 1057 / 1238 s is at or above 585 / 616 / 1226 s.
   - `LEG_BUDGET` = 1800 − 270 − 143 − 411 − 3 = 973.
   - All of this is correct against run 41583428850, and broken at this head: **F1**.
2. **Maxima.**
   - Worker 1, job less LiteX step: 992, 1072, 1187, 1240, 1223 and 1234 s, so the maximum is 1240 (run 41476923392 attempt 1).
   - Builder leg 1: 869 to 1119 s.
   - Worker 0's measured maximum: 1254 s.
   - Setup maximum: 143 s.
   - Verified against `cited-runs-timing.txt` and the jobs API. **R768-1-F2 resolved.**
3. **Option (B).**
   - The generated LiteX workers carry none of the four steps. The live hosted logs of `elaborate-gates-2..4` show only the Python-downloads, RV32 SDK, Verilator and apt cache lines.
   - The generator refuses a missing or repeated step (mutants m1 and m5 caught) and a LiteX leg on a builder worker (m2 caught).
   - `scripts/act_ci.py`, `scripts/ci_events.py` and `scripts/ci_tool_inventory.py` are untouched in the delta. Their only change against dev is round 1's scope-fixture owner count.
   - The workflow's `uses:` set is within `TRUSTED_ACTION_USES`, checked statically (`receipts/g08-act-trust-static.txt`). The author's sandbox receipt `g19` is rc 0.
   - The per-run cost is stated, and the projections hold on run 41583428850's evidence.
   - The empty-save race persists through a builder: **F2**.
4. **Queueing.**
   - The "excludes runner queueing" statement is present in the docs, the `LEG_BUDGET` comment and the PR body.
   - Spans are recorded against acceptance 1 with queueing named as the cause. The waits, 1268 s and 388 s, match the API exactly. For the spans' 1-s offset see S2.
   - Three legs are kept by the manager's decision, and acceptance 1 under concurrency stays open on #737. **R767-1-F2 resolved.**
5. **R767-1-R1 and the suggestions.**
   - R1's exact text is at `docs/testing/CI_WORKFLOWS.md:1683`. **Resolved.**
   - R768-1-S2: applied, as a comment at `scripts/ci_litex_legs.py:171-172`. The reachability claim holds: a second-leg or repeated row already fails the per-leg `executed != legs[leg]` check (mutant m4 removes it, and the self-test still fails, through the absent-name branch).
   - R768-1-S3, boolean half: applied. Mutant m3, the old check, is caught: "accepted a boolean runner exit".
   - R767-1-S1, disjoint assertion: applied (m2 caught).
   - Declined with reasons: the `run_litex_sims.sh` arms, the trailing comma (see RS1) and a `run()` sandbox arm. I accept the reasons.

**Hosted cache-race judgement, as the brief asks.** Both attempts at this head are only partly complete:

- Attempt 1 completed every worker.
- The manager's attempt 2 restored the metadata key on `elaborate-gates-1` before the fail-fast cancellation.

It restored an empty entry: "Cache Size: ~0 MB (201 B)", which builder worker 0 saved in attempt 1. The non-empty restore the ruling requires is not shown, and on this key it cannot be.

## Prior public review findings at this head

| Finding | Status at `e180ba30` |
|---|---|
| R768-1-F1 (cold bound) | Resolved as stated: the cold case covers every invalidated cache, is reconciled with 1226 s, uses one setup figure, and `LEG_BUDGET` agrees. Superseded by **F1**: the restated bounds are broken by this head's run. |
| R768-1-F2 (maxima) | Resolved (focus 2). |
| R768-1-F3 (metadata race) | **Retained as F2**: the LiteX path is closed, and the builder path saves empty. |
| R768-1-S1 / S2 / S3 | S1 declined with reason; S2 applied; S3 half applied, half declined with reason (RS1). |
| R767-1-F1 | Resolved as for R768-1-F1; see **F1**. |
| R767-1-F2 | Resolved. |
| R767-1-R1 | Resolved, exact text. |
| R767-1-S1 | Disjoint assertion applied; the rest declined with reason. |

## Lens results

```text
[R768] MINOR Conformance — docs/testing/CI_WORKFLOWS.md:3121-3171, scripts/ci_litex_legs.py:29-54 vs run 41678609075 — stated cold bounds broken (F1)
[R768] MINOR Conformance — .github/ci-templates/elaborate.yml:213-223 vs run 41678609075 a1/a2 vexii lines — ruling item 3 check fails (F2)
[R768] MINOR Conformance — elaborate job 126077456636 (timeout 3m0s) — exact-head hosted union proof did not run (F3)
[R768] MINOR RTL — run 41678609075 setup/Verilator/leg decomposition; vexii save 201 B; aggregate checkout 260 s — timing effects (F1, F2, F3)
[R768] MINOR Robustness — LEG_BUDGET derivation; inter-job save ordering; 3-minute aggregate timeout path (F1, F2, F3)
[R768] MINOR Docs — CI_WORKFLOWS.md:1689-1707, :3121-3171; template :213-223; PR body tables (F1, F2); RESIDUE RS1
[R768] PASS Tests — scripts/ci_litex_legs_selftest.py:90,150-175 and scripts/ci_gate_workflows.py:129-131,440-456 at e180ba30 — gate self-test rc 0; mutants m1 (no-op removal), m2 (disjoint check off), m3 (boolean exit), m4 (per-leg check off), m5 (exactly-once weakened) each fail a self-test; m0 control passes; m6 (constant shrunk) survives, recorded as S1, not a defect
```

## Gates and probes run at this head (16 CPUs; receipts in `receipts/`)

- `ci_gate_workflows.py --check`, `ci_gate_workflows_selftest.py`, `ci_litex_legs_selftest.py`, `ci_litex_legs.py legs`, `ci_events.py --check`, `run_litex_sims.sh --selftest`, `git diff --check e61a4afa HEAD`: all rc 0 (`g01` to `g07`).
- Mutants m0 to m6 in disposable copies, planted by `scripts/plant_mutants.py`. The results are in `receipts/mutants/`.
  - The first `git archive` copies lacked submodule content and git metadata. That made the gate self-test fail in the unmutated control too. I discarded those results and re-ran on working-tree copies with a throwaway index, where the control m0 passes.
  - m3 needs no git, so it was run in the archive copy.
- The LiteX union over the three exact-head hosted leg receipts: rc 0.
- Static act trust-set check (I did not run the act runner).
- After the probes: the clone has no changes, its index blobs and modes equal HEAD's tree, and the submodule gitlinks are unchanged (`receipts/restore-verify.txt`).

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | ruling items 1-5; `CI_WORKFLOWS.md:1662-1707, 3105-3230`; `ci_litex_legs.py:29-54`; PR body; runs 41583428850, 41678609075 a1/a2 | R768-2 | `e180ba30eccc4ee7c3c699d88973816bdc953caa` |
| RTL | UNCLEAN (F1, F2, F3) | generated `.github/workflows/elaborate.yml` worker blocks; template `:213-223, :344-348`; hosted step timings and cache lines | R768-2 | `e180ba30eccc4ee7c3c699d88973816bdc953caa` |
| Robustness | UNCLEAN (F1, F2, F3) | `ci_gate_workflows.py:126-131, 440-466`; `ci_litex_legs.py:127-180`; save ordering in hosted logs; aggregate timeout path | R768-2 | `e180ba30eccc4ee7c3c699d88973816bdc953caa` |
| Tests | CLEAN (S1 optional) | `ci_litex_legs_selftest.py`, `ci_gate_workflows_selftest.py` run; mutants m0-m6 | R768-2 | `e180ba30eccc4ee7c3c699d88973816bdc953caa` |
| Docs | UNCLEAN (F1, F2; RS1 residue) | `CI_WORKFLOWS.md` delta; template comments; `BUILDER_CACHES` comment; PR body | R768-2 | `e180ba30eccc4ee7c3c699d88973816bdc953caa` |

## Real limits

- The evidence archive at `4ad35a66` is a sha256 manifest (`MANIFEST.json`). Every file I fetched from it (21 files) matches its published hash. The archive commit itself is unsigned, so it is verified by hash only, not by signature.
- Both hosted elaborate attempts at this head are incomplete: attempt 1's aggregate timed out, and attempt 2 was cancelled in checkout. `elaborate-gates-0`'s attempt-2 restore was never reached.
- Hosted per-member seconds vary from run to run, by up to 1.9 times for one member (`test_gptp_tx_timestamp` 461 against 246; `test_soc_timing_cuts` 240 against 369). Two runs do not bound that variance.
- I did not run the LiteX legs locally. For local leg seconds I relied on the author's receipts (`g06` to `g11`), which I spot-checked, not on my own runs.
- I did not execute the act sandbox validation. I checked the trust set statically and relied on the author's `g19`.
- No builder, native, Yosys, PP, gPTP or parent bank was run. No physical calibration or hardware was involved, and field skips are not hardware proof.
- I did not infer or claim any manager source bank.

## Pending manager duties

- The hosted exact-head elaborate run with the union step green (F3), and the decision on the 3-minute aggregate checkout fragility.
- A ruling on F2's alternative: a content-only save, or declaring the metadata cache ineffective.
- A ruling on F1's source, if widening `SECONDS` beyond run 41583428850 conflicts with ruling item 1.
- The current-dev merge candidate (builder and native banks) at the merge turn, and hosted/act acceptance.
- Carry RS1 to the residue checklist.

R768-2 FINISHED
