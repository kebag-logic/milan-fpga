# HANDOFF — [A727e] issue #737 round 3 (continued), PR #836

Lane: $LANES/737-elab-split, branch 737-elab-split, origin https://github.com/kebag-logic/milan-fpga.git (confirmed). Base dev e61a4afa.
Start head ae7412eb (round 3 items 1-3 by [A727d], STOP on item 1). **Final local head 3b323864232fa430ec3a185f33ad7b30fbf1156b**, five commits on top, no rebase, force or merge. PR #836 is still at e180ba30. Nothing was pushed.
Authority: the round 3 ruling (issuecomment-6611061323) and the ruling on the STOP, option (d) with the bound on the job limit (issuecomment-6611968916), which governs item 1. Reviews: R767-2 (issuecomment-6610985935) and R768-2 (issuecomment-6611052254).
Unit milan-737-a727e.service, CPUs 96-111 (taskset, nproc 16). Scratch $VALIDATION_STORAGE/737-a727e. Receipts are in receipts/ beside this file:
- each gate's .log and .rc, with the head in every .rc;
- logs over 200 KB as .log.ref, with size and sha256;
- receipts/superseded-d153844b/ holds the earlier full gate run at d153844b, superseded by the two corrections below;
- receipts/hosted/ holds the attempt 1 and 3 jobs API files, the timing over every cited run, attempt 3's member rows and log sha256, and figures.py/.txt, which recompute every stated figure.

## Status
- [x] TAKEN posted: issuecomment-6612014092 (receipts/taken.md)
- [x] item 1: LEG_BUDGET on the job limit (4f6cf352), correction e2426156
- [x] item 2: workflow figure as a measurement against acceptance 1 (4dc72137), wording 3b323864
- [x] item 3: items 2/3 of ae7412eb stand; the known docs placement defect is fixed (d153844b)
- [x] item 4: every round 2 residue and suggestion was already dispositioned at ae7412eb, so there is no commit (table below)
- [x] gates at 3b323864, all rc 0 (table below)
- [x] PR-BODY.md written
- [x] REVIEW READY posted: issuecomment-6613737865 (receipts/review-ready.md), head 3b323864232fa430ec3a185f33ad7b30fbf1156b

## Commits (one-line subject, no body, no trailers)
- 4f6cf352 Bound each LiteX leg by its worker's 45-minute limit less 600 seconds of headroom and the largest setup, cold Verilator and self-test, derived from named constants, with every elaboration projection and the aggregate's figure taken over run 41678609075 attempt 3 as well (#737)
- 4dc72137 State the elaborate workflow figure, 2013 seconds with Verilator restored and 2111 cold by the component-maxima rule, as a measurement against #737 acceptance 1, which stays open, and record the shallower worker checkout and a LiteX pip cache as its untaken candidates (#737)
- d153844b Keep the receipts paragraph whole and put the elaborate aggregate's head-only checkout after it, noting attempt 3's second cancellation of the old full-history fetch (#737)
- e2426156 Correct LiteX worker 4's projection with Verilator restored to 1282 seconds, its setup, self-test and 794-second leg at their largest (#737)
- 3b323864 Name attempt 1's maxima as the figure the elaborate workflow's setup rise is measured from (#737)

Why five rather than four:
- figures.py recomputed every stated number after the gate run at d153844b. It caught one slip in item 1's docs: worker 4 with Verilator restored is 485 + 3 + 794 = 1282, and I had written 1263.
- The fix needed a commit on top, because rebase and amend of item 1 are not allowed. e2426156 is item 1's correction.
- 3b323864 is item 2's wording fix: "the 1723 seconds stated before" referred to lane history a docs reader cannot see.
- Every gate was then re-run at 3b323864.

## Deviations from the ruling's wording (decided here, with reasons)

1. **Workflow figure 2013 / 2111 s, not "about 1953 s".**
   - The ruling quoted [A727d]'s 1953, which used the 338 s allowance.
   - Attempt 3's `elaborate` aggregate span less its checkout was 85 s (234 - 149). Of that, 82 s passed between the job's start (18:09:40) and its first step (18:11:02), from receipts/hosted/jobs-a3.json. A head-only checkout does not remove that time.
   - Excluding it would be option (c), "exclude a hosted-latency outlier", which the manager did not choose. So the component-maxima rule takes it: aggregate 19 + 85 = 104, and allowance 104 + 149 + 120 + 25 = 398.
   - With that allowance the workflow is 1615 + 398 = 2013 with Verilator restored (slowest: builder worker 0), and 1713 + 398 = 2111 at a cold Verilator key (slowest: LiteX worker 4).
   - Both are stated, with 1953 named as the figure before attempt 3 raised the aggregate's. The figure is a measurement, not a bound, so no decision depends on which number is used. Acceptance 1 is open either way.
2. **The aggregate's 3-minute limit now has 76 s of margin (104 s projection), not 136 s (44 s).** That is the same rule applied to the same component. It is recorded in `scripts/ci_gate_workflows.py:59-64` and `CI_WORKFLOWS.md:3322-3332`. The limit is unchanged.
3. **The elaborate rows of the projection table are now compared with 2700 s rather than the 60% bound (1620 s).**
   - The ruling says "compared with 2,700 s". Worker 4's 1713 s would exceed 1620.
   - The column is renamed "Own bound", and a sentence states the exception (`CI_WORKFLOWS.md:3212-3213`).
   - No script parses that table; this was checked by grep over scripts/ and tests/. The firmware and Verilator rows keep their 60% bound.

## Findings and changes (file:line at 3b323864)

| Finding | Item | Change |
|---|---|---|
| R767-2-F2, R768-2-F1 (bounds from component maxima), under the STOP ruling (d) | 1 | See the breakdown below this table. |
| STOP ruling item 3 (workflow figure as a measurement) | 2 | `CI_WORKFLOWS.md:3262-3280`: a measurement against #737 acceptance 1, not a bound; open. 2013 s warm (33.6 min) and 2111 s cold (35.2 min), 213 and 311 s above 30 minutes. 1953 is named as the figure before attempt 3's aggregate figure. The setup rise is attributed: checkout up to 208 s, LiteX install up to 143 s, VexiiRiscv placement up to 59 s. The two untaken candidates (the shallower worker checkout, which widens the act checkout contract, and a LiteX pip cache, which reverses option (B)) are recorded. Builder legs stay two and LiteX legs three. `:3291-3295`: run 41678609075 did not meet acceptance 1 (a1 1767 s with the aggregate cancelled; a3 2646 s with queueing up to 1043 s). PR-BODY.md, Round 3 table row "STOP ruling: the workflow figure". |
| R767-2-F1, R768-2-F2 (metadata cache) | 3 | Stands as a174e9e5 (no change). Gates re-run at 3b323864: g01, g13 (refusals of the metadata plants), g14. |
| R767-2-F3, R768-2-F3 (aggregate checkout) | 3 | Stands as e4d52a12. d153844b fixes [A727d]'s known placement defect: the receipts paragraph is whole again (`CI_WORKFLOWS.md:3302-3320`), and the head-only checkout paragraph follows it (`:3322-3332`) and notes attempt 3's second cancellation. g19 (act sandbox) accepts. |
| R767-2-R1 | 4 | Dispositioned at ae7412eb: the sentence is gone (item 1). Nothing left. |
| R767-2-S1 | 4 | Dispositioned at ae7412eb: worker 1 projects at its component sum, now 485 + 1119 = 1604. |
| R768-2-S1 | 4 | Applied at ae7412eb (literal names in the self-test). Nothing left. |
| R768-2-S2 | 4 | Applied at ae7412eb (1883 / 2307 / 2825). Nothing left. |
| R768-2-S3 | 4 | The fill step left the LiteX workers (ae7412eb). DECLINED, unchanged, for [A727d]'s reason: the placement copy sits in a step that also places the VexiiRiscv source every worker needs; its script is pinned by `scripts/ci_events.py` (act trust set), and copying from an absent directory is a no-op. |
| R768-2-S4 | 4 | Observation, no defect. No change. |
| R768-2-RS1 | 4 | Applied at ae7412eb in the PR body (kept in PR-BODY.md). |
| Observations (package-cache tar failure; artifacts 404) | - | Predate this PR and are outside its scope. Left for the manager as candidate Issues (I may not open Issues). |
| docs-check aggregate: same full fetch under 3 minutes | - | Not changed: round 3 item 3 names elaborate jobs only. Candidate Issue; stated in PR-BODY.md Known limitations. |

Item 1 breakdown (R767-2-F2, R768-2-F1, under STOP ruling (d)):
- **`scripts/ci_litex_legs.py:47-61`.** `LARGEST` now covers attempts 1 and 3: ctrl 284, gptp 462, soc 510.
- **`scripts/ci_litex_legs.py:62-78`.** Named constants `JOB_LIMIT` 2700, `HEADROOM` 600, `SETUP` 485 (worker 3, a3), `COLD_VERILATOR` 431 (worker 3, a1) and `SELFTEST` 3. `LEG_BUDGET = JOB_LIMIT - HEADROOM - SETUP - COLD_VERILATOR - SELFTEST` = 1181.
- **`scripts/ci_litex_legs_selftest.py:167-170`.** Each LiteX worker's generated `timeout-minutes` times 60 must equal `JOB_LIMIT`. Mutant m01 (limit 44) fails the self-test; see receipts/m01-job-limit-mutation.txt.
- **`ci/image/command-table.json:13611-13615`.** `ci_litex_legs.py` is re-pinned to f720579c… after review.
- **`scripts/ci_gate_workflows.py:59-64`.** The aggregate figure is 104 s with a 76 s margin (comment only).
- **`docs/testing/CI_WORKFLOWS.md`:**
  - `:1673-1681`: the legs bounded by `LEG_BUDGET` 1181, 600 s inside the 45-minute limit.
  - `:1690-1691`: 462 / 448 / 794 at `LARGEST`.
  - `:1719-1720`: cold `test_ctrl_memory` 280 / 224 / 284.
  - `:3136-3157`: components over every cited run, a1 to a3 included. Projections 1615 / 1604, LiteX cold 1381 / 1367 / 1713, warm 950 / 936 / 1282, measured spans.
  - `:3159-3166`: the comparison with 2700 s, and `LEG_BUDGET` derived from named constants.
  - `:3168-3178`: allowance 398, aggregate 104, with the 82 s pre-step reason.
  - `:3180-3189`: the single re-measurement rule. The job limit and headroom are not measurements.
  - `:3193-3197`: cold metadata in a1 and a3.
  - `:3212-3224`: table rows against 2700 with margins 1085 / 1096 / 1319 / 1333 / 987.
- **e2426156:** `:3154` 1263 -> 1282.
- **Three legs stay.** The partition is unchanged (`SECONDS`).

## Per-leg timing (measured and derived)

The partition (`legs`, g05) is unchanged: 0/3 {gptp} 461 s, 1/3 {cpu, gmii, boot, mem, retained} 440 s, 2/3 {ctrl, soc} 520 s, from `SECONDS` (run 41583428850). At `LARGEST` the legs hold 462 / 448 / 794 s, all within `LEG_BUDGET` 1181.

| Leg | Worker | Members | 41583428850 s | a1 s | a3 s | LARGEST s | Cold projection (vs 2700) | Warm projection | Hosted spans 41583428850 / a1 / a3 | Local leg at 3b323864 s (per member) |
|---|---|---|---|---|---|---:|---:|---:|---|---|
| 0/3 | gates-2 | gptp | 461 | 246 | 462 | 462 | 1381 (1319) | 950 | 585 / 706 / 906 | 571 (570) |
| 1/3 | gates-3 | cpu, gmii, boot, mem, retained | 70+0+25+14+331 | 72+0+25+15+336 | 71+0+25+14+333 | 448 | 1367 (1333) | 936 | 616 / 1021 / 930 | 410 (92, 0, 31, 15, 272) |
| 2/3 | gates-4 | ctrl, soc | 280+240 | 224+369 | 284+510 | 794 | 1713 (987) | 1282 | 1226 / 1178 / 1194 | 661 (84, 576) |

Here a1 and a3 are attempts 1 and 3 of run 41678609075.

Derived figures (receipts/hosted/figures.txt):
- Setup is 485 and cold Verilator 431.
- `LEG_BUDGET` = 2700 - 600 - 485 - 431 - 3 = 1181.
- Builder workers 0 and 1 project at 1615 and 1604 (margins 1085 and 1096). Their measured maxima are 1254 and 1244.
- The aggregate is 19 + 85 = 104, against 180 (margin 76), and the allowance is 398.
- The workflow is 2013 warm and 2111 cold, as a measurement. With the former 338 s allowance it was 1953.
- Every hosted span is below its projection. Attempt 3's warm spans 906 / 930 / 1194 are below the warm projections 950 / 936 / 1282.

Local versus hosted:
- The local times are not hosted figures and do not enter the rule.
- Locally, `test_soc_timing_cuts` took 576 s (633 s at d153844b), above its hosted 510. Even 633 would hold leg 2 at 917 s, inside 1181.
- `test_ctrl_memory` took 84 s locally because the scratch venv already held the CPU metadata (`fc22d570….py`, written 18:40 by [A727d]'s cold e01 run and copied with the venv).

## Records touched

| Record | Touched | How / why |
|---|---|---|
| scripts/ci_litex_legs.py | yes | `LARGEST`, named constants, derived `LEG_BUDGET` (item 1) |
| scripts/ci_litex_legs_selftest.py | yes | job-limit coupling assertion (item 1) |
| scripts/ci_gate_workflows.py | yes | comment only: aggregate figure 104 s / 76 s margin (item 1). `--check` rc 0, workflow unchanged |
| ci/image/command-table.json:13614 | yes | `ci_litex_legs.py` re-pinned to f720579c029907b4… (item 1). No other pinned file changed (`ci_gate_workflows.py` and the self-test are not pinned there) |
| docs/testing/CI_WORKFLOWS.md | yes | items 1, 2, 3 and the corrections |
| .github/workflows/elaborate.yml, .github/ci-templates/elaborate.yml | no | unchanged since ae7412eb (g01 rc 0) |
| scripts/act_ci.py, scripts/ci_events.py, scripts/ci_tool_inventory.py | no | act trust set unchanged (g19 accepts) |
| ci/image/tool-inventory.json, ci/image/exec-audit-receipt.json | no | as in round 2 and [A727d]: the inventory check already refuses on this host for an unrelated reason, and no workflow runs it; the exec audit is an image trace pinned to an older source |
| .github/workflows/docs.yml and its template | no | unchanged since e61a4afa |

## Gate table (at 3b323864; logs and rc in receipts/)

| Gate | rc | s |
|---|---:|---:|
| g01 python3 scripts/ci_gate_workflows.py --check | 0 | 0 |
| g02 python3 scripts/ci_events.py --check (2199 items) | 0 | 1 |
| g03 python3 scripts/ci_events.py --selftest (2199 items, 5489 arms; log 353 KB, .ref) | 0 | 223 |
| g04 scripts/run_litex_sims.sh --selftest (16 checks) | 0 | 2 |
| g05 python3 scripts/ci_litex_legs.py legs (461/440/520; at largest 462/448/794) | 0 | 0 |
| g06 LiteX leg 0 own command (test_gptp_tx_timestamp PASS 570 s) | 0 | 571 |
| g07 LiteX leg 1 own command (cpu 92, gmii 0, boot 31, mem 15, retained 272, each PASS) | 0 | 410 |
| g08 LiteX leg 2 own command (ctrl 84, soc 576, each PASS) | 0 | 661 |
| g09 `ci_litex_legs.py union` over g06-g08's receipts → "litex: 8 simulations exactly once, each a pass" | 0 | 1 |
| g10a control: test_pp_boot_bus_freeze dropped from leg 1's receipt → "LiteX legs refused: LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze" | 1 (expected) | 0 |
| g10b control restored (receipt equal to the real one) | 0 | 0 |
| g11a aggregate verifier (`ci_gate_receipts.py verify --workflow elaborate`) over the real LiteX receipts | 0 | 1 |
| g11b verifier, dropped → "gate evidence refused: LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze" | 1 (expected) | 1 |
| g11c verifier restored | 0 | 1 |
| g12 git diff --check e61a4afa HEAD | 0 | 0 |
| g13 ci_gate_workflows_selftest.py | 0 | 15 |
| g14 ci_litex_legs_selftest.py | 0 | 0 |
| g17 cd tests && behave --no-capture -f plain (508 scenarios; .ref) | 0 | 3 |
| g18 python3 scripts/ci_scope.py --selftest | 0 | 29 |
| g19 act_ci.validate_workflow_sandbox(elaborate) → None | 0 | 1 |
| d05 d06 d07 d33 d36 d37 d40 d42 d47 d50, the docs workflow's run steps that read the changed docs and scripts | all 0 | 8/3/1/1/10/1/0/11/35/9 |
| m01 mutant: LiteX worker limit 45 → 44 minutes fails the LiteX leg self-test with ('elaborate', 2, 44); file restored with git checkout | 1 (expected) | - |

Not run:
- `act_ci.py --selftest` (docs step d38/d39's candidate copy): the agent contract forbids running the candidate's copy on the host. d38's other half is g02/g03.
- The docs workflow is unchanged, so its other steps read none of the changed files.

The gate script always exits 0 itself. The rc in each .rc file is the gate's own exit status.

## Real limits

- Every bound is from hosted runs up to run 41678609075 attempt 3. A later hosted run above any component replaces it by the stated rule, and a leg over 1181 at `LARGEST` is refused.
- The non-empty metadata restore on `elaborate-gates-1` and a completed hosted `elaborate` aggregate with the head-only checkout can only be shown by the manager's hosted runs after the push.
- #737 acceptance 1 is open. The workflow figure (2013 / 2111 s) is above 30 minutes before any queueing.
- Candidate Issues for the manager:
  - the docs-check aggregate's full fetch under 3 minutes;
  - the `Cache exact package downloads 16` tar failure;
  - artifacts that list 0 and download as 404 after a re-run;
  - the shallower worker checkout and the LiteX pip cache, both for acceptance 1.

REVIEW READY posted: issuecomment-6613737865 (head 3b323864232fa430ec3a185f33ad7b30fbf1156b); text in receipts/review-ready.md
