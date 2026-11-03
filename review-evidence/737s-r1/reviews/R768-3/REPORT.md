[R768] NEGATIVE - exact head 3b323864232fa430ec3a185f33ad7b30fbf1156b

# R768-3: external review of PR #836 (Relates to #737), round 3

- Head `3b323864232fa430ec3a185f33ad7b30fbf1156b`, tree `4376620f4802804538f53114af5544aafa7b34ee`. The tree was verified in the isolated clone (`receipts/clone-integrity.txt`).
- Source base and live dev: `e61a4afaa54a598ceec08b7b5879285256cc60b6`.
- Round 3 delta: `e180ba30..3b323864`, seven files, CI only: `ci_litex_legs.py`, `ci_litex_legs_selftest.py`, `ci_gate_workflows.py`, the elaborate template and generated workflow, `command-table.json` and `CI_WORKFLOWS.md`.
- Authority:
  - the round 3 ruling (#737 issuecomment-6611061323);
  - the STOP ruling, option (d) (issuecomment-6611968916);
  - the REVIEW READY comment (issuecomment-6613737865).
- Code outside the delta keeps its round 2 lens verdict. The delta does not change what that code depends on.

Verdict basis: two MINOR findings and one RESIDUE. Both MINORs come from the hosted runs at this head, and neither is a defect in the delta's logic.

- Every check the round 3 ruling and the STOP ruling asked for holds at this head: items (1) to (5) below.
- Elaborate is green at this head, with the union proof and a non-empty warm-key metadata restore.
- No stated bound is broken: no job came near its 45-minute limit.
- **F1:** the exact-head run measured components above the figures the code and docs state. The PR's own re-measurement rule says those figures must then be replaced, and that has not happened.
- **F2:** an rtl-full job (outside the diff) reached its 2-minute limit at this head.

## Focus checks

### (1) LEG_BUDGET, the partition and the limit refusal

**Holds.**

- `scripts/ci_litex_legs.py:64-78` computes `LEG_BUDGET = JOB_LIMIT - HEADROOM - SETUP - COLD_VERILATOR - SELFTEST`. That is 2700 - 600 - 485 - 431 - 3 = 1181 (`receipts/arith.log`).
- Each constant names its source:
  - setup 485: worker 3, run 41678609075 attempt 3;
  - cold Verilator 431: worker 3, attempt 1;
  - headroom 600: stated headroom, not a measurement.
- `LARGEST` (`:51-60`) covers run 41583428850 and run 41678609075 attempts 1 and 3. It includes the attempt 3 rows: soc_timing 510, gptp 462 and ctrl 284.
- The partition holds 462 / 448 / 794 at `LARGEST` (`receipts/litex-legs.log`), and `partition()` refuses a leg above budget (`:116-119`).
- The self-test requires each LiteX worker's generated limit × 60 to equal `JOB_LIMIT` (`scripts/ci_litex_legs_selftest.py:170`).
- Mutation probes, run on copies of the whole clone after regeneration (`scripts/mutation_probes.sh`, `receipts/probe-summary.txt`):
  - m1 sets the LiteX workers to 44 minutes. Refused: `AssertionError: ('elaborate', 2, 44)`.
  - m2 sets gptp `LARGEST` to 1182. Refused: "a LiteX leg holds 1182 measured seconds at its largest, above its 1181".
  - m0, the unmutated control, passes.

### (2) Worker projections against 2700 s

**Holds arithmetically.**

- Builders: 485 + 1130 = 1615 and 485 + 1119 = 1604, margins 1085 and 1096.
- LiteX cold: 919 + leg gives 1381, 1367 and 1713, margins 1319, 1333 and 987.
- LiteX with Verilator restored: 950, 936 and 1282.
- The table at `docs/testing/CI_WORKFLOWS.md:3212-3224` has the renamed `Own bound` column. Its exception sentence reads "except the elaborate workers', which is their 45-minute limit itself (#737)". The margins in the table match the code (`receipts/recompute.txt`, "stated" line).

### (3) The workflow figure

**Holds as stated, and is stated as a measurement, not a bound** (`CI_WORKFLOWS.md:3262-3270`).

- The allowance is 398 s: aggregate 104 (a 19 s depth-one checkout plus 85 s outside it), collector 149, watcher 120 and tail 25.
- The figure is 1615 + 398 = 2013 s, and cold 1713 + 398 = 2111 s, 213 and 311 s above 30 minutes.
- The 1953 s and 1723 s history figures reconcile: 338 s allowance, and 255 s setup at attempt 1's maxima.
- The aggregate's 3-minute margin is 180 - 104 = 76 s (`ci_gate_workflows.py:58-66`). #737 acceptance 1 is stated as open.

### (4) The metadata cache and the aggregate checkout

**Holds, in the generated workflow and in hosted runs.**

- Only `elaborate-gates-1` carries `Cache the generated CPU metadata` and "Keep the generated CPU netlist arguments for the next run".
- `metadata_worker()` (`ci_gate_workflows.py:486-494`) derives the worker from `ci_builder_legs` `ISOLATED`/`LEGS`/`REQUIRED`. That matches the leg construction at `ci_builder_legs.py:79`.
- The elaborate aggregate's checkout has no `with:` (`.github/workflows/elaborate.yml:1196`), and its limit is 3 minutes (`:1187`).
- More mutation probes:
  - m3 moves the metadata to builder 0. Refused by the literal constants assertion.
  - m4 restores the full-history aggregate. Refused, naming `fetch-depth: 0`.
  - m5 sets the aggregate limit to 4. Refused.

### (5) The arithmetic correction and figure agreement

**Holds.**

- e2426156 corrects worker 4 restored to 485 + 3 + 794 = 1282.
- Every round 3 figure agrees with the code: in `CI_WORKFLOWS.md` (`:1677`, `:3136-3190`, `:3212-3224`, `:3262-3280`), and in the live PR body's Round 3 section.
- The live PR body equals the packet's `author-r3/PR-BODY.md` apart from one trailing newline.
- The older figures in the PR body's Description (143 / 411 / 973 / 997 / 1077 / 270) carry a "round 2 figures; round 3 rebuilds them" label.

### Comment rule

The added comments in the delta (`ci_litex_legs.py`, `ci_gate_workflows.py`, the template at `:218-227`) contain no lane labels, lane names, review rounds, reviewer IDs or comment IDs. They name issue #737 and hosted run IDs only. No new RESIDUE.

## Hosted evidence at this head

The receipts are under `receipts/`.

### elaborate, run 41705989293

**Attempt 1: conclusion success.**

- All five workers passed.
- The aggregate passed in 21 s, with a 3 s checkout. Its log says "elaborate: 5 source gates exactly once; all worker jobs successful".
- `ci_gate_receipts.py verify` calls the LiteX union whenever leg receipts exist (`scripts/ci_gate_receipts.py:131-132`).
- Every simulation passed once: gptp 459, cpu 52, gmii 0, boot 18, mem 11, retained 236, ctrl 240, soc 409 (`receipts/attempt1-log-excerpts.txt`).
- `elaborate-gates-1` missed the metadata key, then saved it at 438 B ("Sent 438 of 438").
- No other worker log mentions the `elaborate-vexii` key.

**Attempt 2: manager re-run.**

- All five workers passed, and the aggregate passed with union `pass` (`receipts/attempt2-gate-union.json`, tree `4376620f…`).
- `elaborate-gates-1` reports "Cache hit … Cache Size: ~0 MB (438 B) … Cache restored".
  - The empty entries recorded earlier were 200 to 202 B, and a local zstd tar of one empty directory is 190 B (`receipts/empty-cache-calibration.txt`).
  - So the restore is non-empty, judged by size. That satisfies ruling item 4.
- The leg receipts (`receipts/attempt2-litex-leg-*.json`) show every simulation once and PASS: gptp 477, cpu 70, gmii 0, boot 25, mem 14, retained 331, ctrl 277, soc 472.
- The run ended `cancelled` because of the cascade under F2:
  1. rtl-full's watcher cancelled its siblings.
  2. That cancelled elaborate's watcher at 20:53:13.
  3. elaborate's tail then logged "Cancelled runs: [41705989346, 41705989293]".

**Attempt 3: re-ran the watcher and tail only. The run conclusion is now success** (`receipts/exact-head-runs.tsv`, `receipts/hosted-components-41705989293-a3.txt`).

**No job came near its limit.** The largest worker span was 1535 s against 2700 s, and the aggregate 29 s against 180 s.

### rtl-full, run 41705989346

- Attempt 1: `Union milan_dp_mclk` took 129 s against `timeout-minutes: 2` (`.github/workflows/rtl.yml:1095`). Every step succeeded, with "Fetch inventory dependencies" at 104 s, and the job was cancelled at its limit. `verilator-suites` then failed. See F2.
- Attempt 2, as read: all six unions, `verilator-suites` and `yosys-portability` are success. The watcher was still in progress when read (`receipts/rtl-full-41705989346-attempt2-jobs.json`).

### docs and rtl-fast, runs 41705989467 and 41705989299

Both success.

## Findings

### R768-3-F1: MINOR. The exact-head hosted run exceeds stated component maxima and a stated projection, and the stated re-measurement rule has not been applied

**Lenses:** Conformance, Docs.

**Where:**
- `scripts/ci_litex_legs.py:51-78` (`LARGEST`, `SETUP`, `LEG_BUDGET`);
- `docs/testing/CI_WORKFLOWS.md:3136-3190` and the table at `:3215-3224`;
- the `:3262-3270` workflow figure;
- the PR body's Round 3 item 1 and its STOP row.

**Evidence:** `receipts/hosted-components-41705989293.txt` and `receipts/recompute.txt`. In run 41705989293, against the stated figures:

| Component | Stated | Measured at this head |
|---|---:|---:|
| Setup (job span less gate and Verilator steps) | 485 | 739 (`elaborate-gates-1`, attempt 2: checkout 274, LiteX install 250); also 559, 525 and 513 (workers 2, 0 and 3, attempt 1) |
| `test_gptp_tx_timestamp` verdict row (`LARGEST`) | 462 | 477 (attempt 2) |
| `Collect CI manifest` | 149 | 183 and 182 |
| `Cancel late CI failures` | 25 | 29 |
| `elaborate-gates-2` span, cold | projection 1381 | 1414 (attempt 1) |

The sources of these figures:
- The docs build every figure from "the largest value it took over the cited hosted runs" (`:3136-3138`).
- The STOP ruling names 485 as the largest setup.
- `:3180-3187` states the rule: "a component it measures above its figure here replaces that figure … `LEG_BUDGET`, every projection in this section and the table below are then recomputed".

**What does hold:** recomputed with this head's maxima, every bound still holds.
- `LEG_BUDGET` becomes 927, and the legs at `LARGEST`, 477 / 448 / 794, still fit.
- The worst cold worker is 1967 s, a 733 s margin, which keeps the 600 s headroom.
- The workflow figure becomes 2305 s (2403 s cold), still a measurement only.

So this is not a broken bound. It is the same class as R768-2-F1 and R767-2-F2, in the form ruling (d) contains.

**Impact:** if merged as is, the authoritative doc and constants publish as "largest" figures that the merge head's own hosted run has exceeded:
- setup by 254 s;
- one projection by 33 s;
- the `LEG_BUDGET` derivation, overstated by 254 s.

A later reader cannot tell this from a figure that still holds.

**Required outcome:** one of the following.
- (a) Apply the stated rule with run 41705989293 attempts 1 and 2 added to the cited runs. That gives `SETUP` 739, gptp 477, collector 183, tail 29, `LEG_BUDGET` 927, the projections in `receipts/recompute.txt`, and allowance 436. The workflow figure becomes 2305 / 2403 s.
- (b) The manager publicly rules that the cited-run set closes at run 41678609075, so that a later run, including this head's, is judged only against the 2700 s limit less the 600 s headroom. The docs and PR body then say so in one sentence, and this head's maxima are recorded on #737.

Note: (a) produces a new head whose own run may exceed again. That is why (b), or (a) followed by judging only the bound at that head, is the bounded route.

**Verification:**
- For (a): `python3 scripts/ci_litex_legs.py legs` and the LiteX leg self-test show the new figures and still fit; the docs table and PR body match `receipts/recompute.txt`.
- For (b): the ruling link, and the docs sentence naming the closed set.

### R768-3-F2: MINOR. An rtl-full union job reached its 2-minute limit at this exact head, and its fail-fast cascade cancelled elaborate attempt 2

**Lenses:** Robustness (timeout path), Conformance (the section 7 exact-head `verilator-suites` bar).

**Where:** run 41705989346 attempt 1, job 126196630625 `Union milan_dp_mclk` (`receipts/rtl-full-union-milan_dp_mclk-job.json`). The limit is at `.github/workflows/rtl.yml:1095`.

**Evidence:**
- The job ran 129 s against 120 s; every step succeeded, and the job was cancelled.
- `verilator-suites` failed as a result.
- rtl-full's watcher then cancelled its siblings (`receipts/rtl-full-fail-fast-job.json`), and elaborate's tail cancelled both runs (`receipts/attempt2-log-excerpts.txt`).
- The same union jobs took up to 109 s at e180ba30 and 18 s at aa3e2d85.
- `rtl.yml` is not in this PR's diff, and the 104 s step is a dependency fetch the PR does not change. So the cause is outside this lane. It is the same shape as the docs-check aggregate candidate the author already named: a short limit over a variable fetch.

**Impact:** a protected exact-head context was red on the first run, and the run's cascade turned a green elaborate attempt into a `cancelled` run.

**Required outcome:** no change on this branch.
- A green exact-head or merge-candidate `verilator-suites`. Attempt 2 shows `verilator-suites` and `yosys-portability` success; the manager confirms it on completion.
- A public candidate Issue for the 2-minute rtl union limits, with the manager recording that it is outside #737's scope.

**Verification:** the run 41705989346 conclusion, and the Issue link.

### R768-3-RS1: RESIDUE (wording only)

**Lens:** Docs.

**Where:** `docs/testing/CI_WORKFLOWS.md:3197-3199`.

"it took 100 to 113 seconds on metadata builder leg 1 had generated earlier in the same job" is missing a relative pronoun.

**Exact fix:** "it took 100 to 113 seconds on metadata that builder leg 1 had generated earlier in the same job".

### R768-3-S1: SUGGESTION

**Lenses:** Tests, Robustness.

The non-empty metadata proof rests on archive size: 438 B against about 200 B empty. A one-line count of the files in `~/vexii-netlist-args` after the fill step, and after the restore, would make the warm-key check readable from the log rather than inferred. This is optional, and the template's event contract is pinned.

### R768-3-S2: SUGGESTION

**Lens:** Docs.

`CI_WORKFLOWS.md:1674` is one wrapped line longer than its neighbours: "…(attempts 1 and 3). Inside the old aggregate, after a builder". It is cosmetic; the hosted docs workflow passes at this head.

## Prior findings

Each is judged at its cause at this head.

| Finding | State at 3b323864 |
|---|---|
| R768-2-F1 (cold bounds broken by the exact-head run) | **Resolved at its cause by ruling (d).** The bound is now the job limit less 600 s, `LEG_BUDGET` is derived from named constants, and run 41678609075 attempts 1 and 3 are in the maxima. The class recurs as R768-3-F1 (figures only, no bound broken). |
| R768-2-F2 (metadata key saved empty) | **Resolved.** Only `elaborate-gates-1` carries the step. Attempt 1 saved 438 B, attempt 2 restored 438 B, and no other job references the key. |
| R768-2-F3 (aggregate timeout in checkout) | **Resolved.** The checkout is head-only: 3 s and 15 s, spans 21 s and 29 s, union passing in both attempts. |
| R767-2-F1, F2, F3 | As R768-2-F2, F1 and F3 above. |
| R767-2-R1 | **Resolved.** The sentence is gone; a grep for it at this head finds nothing. |
| R767-2-S1, R768-2-S1 to S4, R768-2-RS1 | **Dispositioned at ae7412eb**, per PR body item 4. Spot-checked: S1's literal names `SHARED_CACHES`, `METADATA` and `METADATA_WORKER` are at `ci_litex_legs_selftest.py:26-30`, and the m3 probe confirms they bite. S2's whole seconds are at `CI_WORKFLOWS.md:3283-3284`. |

## Lens lines

```text
[R768] MINOR Conformance — scripts/ci_litex_legs.py:51-78; CI_WORKFLOWS.md:3136-3190,3215-3224,3262-3270 vs run 41705989293 a1/a2 — stated maxima and one projection exceeded, re-measurement rule not applied (F1)
[R768] MINOR Conformance — run 41705989346 a1 job 126196630625 (rtl.yml:1095, 2 min) — exact-head verilator-suites red on first run; a2 green, pending completion (F2)
[R768] PASS RTL — generated .github/workflows/elaborate.yml worker blocks and aggregate (:1185-1196); ci_gate_workflows.py:57-66,265-270,461-494; template :218-227 — limits 45 min on all five workers and 3 min on the aggregate, metadata on gates-1 only, head-only aggregate; with exact-head maxima the worst cold worker keeps 733 s >= 600 s headroom, so the resource/timing effect is bounded
[R768] MINOR Robustness — rtl-full union timeout path and fail-fast cascade, runs 41705989346 a1 / 41705989293 a2 (F2); clean within the delta: refusals for missing/repeated cache and metadata steps, split elaboration gates, over-budget leg, non-2700 LiteX limit, full-history aggregate, each probed
[R768] PASS Tests — ci_litex_legs_selftest.py:54-77,158-231; ci_gate_workflows_selftest.py; receipts/probe-m0..m5 — each of five mutants (44-min LiteX limit, LARGEST over budget, metadata on builder 0, full-history aggregate, 4-min aggregate) refused after regeneration, control passes; author receipts g01/g04/g05/g09/g13/g14/g17/g19 and leg JSONs digest-verified at 3b323864
[R768] MINOR Docs — CI_WORKFLOWS.md:3136-3190,3215-3224,3262-3270 and PR body Round 3 — figures exceeded at this head (F1); RESIDUE RS1 at :3197-3199
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Both rulings; `ci_litex_legs.py:51-78`; `CI_WORKFLOWS.md` round 3 hunks; PR body; runs 41705989293 a1–a3 and 41705989346 a1–a2 | R768-3 | `3b323864232fa430ec3a185f33ad7b30fbf1156b` |
| RTL | CLEAN | Generated `elaborate.yml` worker and aggregate blocks; `ci_gate_workflows.py:57-66, 265-270, 461-494`; template `:218-227`; hosted spans and recomputed headroom | R768-3 | `3b323864232fa430ec3a185f33ad7b30fbf1156b` |
| Robustness | UNCLEAN (F2) | Generator and partition refusals (probes m1–m5); rtl-full union timeout and fail-fast cascade logs | R768-3 | `3b323864232fa430ec3a185f33ad7b30fbf1156b` |
| Tests | CLEAN | `ci_litex_legs_selftest.py`; `ci_gate_workflows_selftest.py`; probe receipts; author r3 receipts (digest-verified) | R768-3 | `3b323864232fa430ec3a185f33ad7b30fbf1156b` |
| Docs | UNCLEAN (F1); RESIDUE RS1 | `CI_WORKFLOWS.md:1666-1690, 3136-3290`; template comment; `METADATA_STEPS` and `HEAD_ONLY_AGGREGATES` comments; live PR body | R768-3 | `3b323864232fa430ec3a185f33ad7b30fbf1156b` |

## Real limits

**What I ran:**
- At the head, in the clone: `ci_gate_workflows.py --check`, the LiteX leg self-test, the gate workflow self-test and `ci_litex_legs.py legs`, all rc 0 (`receipts/gate-check.*`, `litex-selftest.*`, `gate-selftest.*`, `litex-legs.*`).
- Six disposable whole-clone probe copies, since removed.

**What I did not run:**
- act or the host act runner;
- any source bank;
- the local LiteX leg commands. For those I relied on the author's receipts and on two hosted attempts.

**What is inferred:**
- The non-empty metadata judgement is by archive size; the archive contents were not listed.
- The evidence commit 764886ec is not git-signed. Integrity rests on the `MANIFEST.json` digests, of which 14 author-r3 files were sampled, all OK (`receipts/author-r3-spotcheck-VERIFY.txt`).

**Not proof of anything:** physical calibration was NOT RUN, and field skips are not hardware proof.

**Timing of my reads:** rtl-full attempt 2 was still in progress (watcher) when read. The elaborate run conclusion was read after attempt 3.

**Clone state:** restored and verified at exact head bytes: worktree, index and `write-tree` equal tree `4376620f…`, and the six submodule gitlinks are unchanged (`receipts/clone-integrity.txt`).

## Pending manager duties

- Decide F1's route, (a) or (b).
- Confirm rtl-full run 41705989346 completes green, and file or rule on the rtl union 2-minute limit Issue (F2).
- Hosted and act acceptance at the final head.
- The current-dev merge candidate's builder and native banks.
- Carry RS1 to the residue checklist.
- The author's three open candidate Issues: the docs-check aggregate fetch, the package-downloads cache tar failure, and artifacts after a re-run.
- The two acceptance 1 candidates (shallower worker checkout, LiteX pip cache), recorded on #737.
- #737 acceptance 1 stays open. Attempt 1 here ran 2340 s from first job start to last job end.

R768-3 FINISHED
