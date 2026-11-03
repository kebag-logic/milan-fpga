# HANDOFF — [A727f] issue #737 round 4, PR #836

Lane: $LANES/737-elab-split, branch 737-elab-split, origin https://github.com/kebag-logic/milan-fpga.git (confirmed). Base dev e61a4afa.
Start head 3b323864 (round 3 by [A727d] and [A727e]; PR #836 at the same head). **Final local head 9104a8fc68979a7a8795859e8704aef27ea0634d**: three commits on top, with no rebase, force or merge. Nothing was pushed.
Authority: the round 4 ruling, #737 issuecomment-6615561789. Reviews: R767-3 (issuecomment-6615556366) and R768-3 (issuecomment-6615559663). Archived packets are on branch 737s-review-evidence (review-evidence/737s-r1/reviews/R767-3, R768-3).
Unit milan-737-a727f.service, CPUs 96-111 (taskset, nproc 16). The peak memory read was about 1.3 GB. Scratch: $VALIDATION_STORAGE/737-a727f.

Receipts are in receipts/ beside this file:
- each gate's .log and .rc, with the head in every .rc;
- logs over 200 KB as .log.ref, with size and sha256;
- receipts/hosted/:
  - the jobs API for run 41705989293 attempts 1 and 2, and 41678609075 attempt 2;
  - components.py and components.txt, which recompute every component and figure over the whole cited set from the jobs API (the other runs' jobs JSON are round 3's, in 737-a727e/receipts/hosted and the R767-3 packet);
  - member-rows-41705989293.txt, the verdict rows, self-test lines and aggregate verdicts from the job logs;
  - logs.sha256, with each job log's sha256 and size. The logs themselves are over 200 KB and stay in scratch.

## Status
- [x] TAKEN posted: issuecomment-6616747645 (receipts/taken.md)
- [x] item 1, ruling item 1: re-measurement (f3a49b93)
- [x] item 2, ruling items 2 and 3: frozen set and merge bar (56e6021a)
- [x] item 3: R767-3-R1, R767-3-R2, R768-3-RS1 and R768-3-S2 (9104a8fc), and R767-3-S2 in PR-BODY.md
- [x] gates at 9104a8fc, all rc 0 (table below)
- [x] PR-BODY.md written (round 3's published body plus Round 4 and Superseded (round 2))
- [x] REVIEW READY posted: issuecomment-6617179916 (receipts/review-ready.md), head 9104a8fc68979a7a8795859e8704aef27ea0634d

## Commits (one-line subject, no body, no trailers)
- f3a49b93 Re-measure every elaborate figure with run 41705989293 attempts 1 and 2 in the cited runs: setup 739, test_gptp_tx_timestamp 477, self-test 4 and LEG_BUDGET 926, the legs still fitting at 477, 448 and 794 seconds (#737)
- 56e6021a Freeze the elaborate figures' cited runs, so later hosted runs feed the next re-measurement under #737 acceptance 1, and judge a later run only by a timeout, a worker span above 2100 seconds, a LiteX simulation unrun, repeated or unreported, or a refusing union verifier (#737)
- 9104a8fc Scope the builder workers' largest job times to the LiteX legs apart, credit the 2700-second limit control to the gate workflow self-test, restore the dropped relative pronoun and rewrap the LiteX legs paragraph (#737)

## Deviations from the ruling's wording (decided here, with reasons)

1. **`SELFTEST` 4, so `LEG_BUDGET` is 926, not the ruling's 927.**
   - The ruling quotes 2700 - 600 - 739 - 431 - 3. Both reviews kept the self-test at round 3's 3 s, and neither recomputed it at run 41705989293.
   - Round 3 measured the self-test as the largest LiteX leg step less its verdict rows, in the jobs API's whole seconds (596 - 593). The same method on attempt 2's leg 0 gives 481 - 477 = 4.
   - The job log agrees: the leg step began at 20:37:11.49 and the next step at 20:45:12.12, 480.6 s against a 477 s row.
   - The ruling says to use "the maxima over the frozen set as you measure them". Keeping 3 would leave a stated maximum that the frozen set exceeds, which is exactly the F1 class.
   - The partition still fits: 794 against 926. Worker 4 cold is 1968, 132 s inside 2100.
   - The control uses 927, which is above both budgets.
2. **Allowance 443 (R767-3), not 436 (R768-3).**
   - R768-3 kept the aggregate at 104, with the 19 s depth-one checkout.
   - The rule lists "the aggregate's checkout" as a component. It is projected at the largest depth-one checkout over the cited runs, and that is 26 s: `Cancel late CI failures` in attempt 1, a depth-one job.
   - So the aggregate is 26 + 85 = 111 (margin 69), and the allowance is 111 + 183 + 120 + 29 = 443.
   - The workflow figure is 1869 + 443 = 2312 warm and 1968 + 443 = 2411 cold. R767-3's 2410 is one second lower because it kept the self-test at 3.
3. **The merge bar's span line names "an elaborate worker's measured span", where the ruling says "a job's".** The ruling's parenthetical, "its 2700 s limit less the 600 s headroom", only fits the 45-minute workers. The watcher, `Fail fast across this head`, has a 120-minute limit and ran 2299 s in attempt 1. Read as "a job", it would be a finding the ruling did not intend. Its timeout is still covered by "a job reaches its timeout".
4. **The cited list keeps "41678609075 (attempts 1 to 3)"**, as committed at 3b323864. R767-3 calls attempt 2 excluded, but the docs list it, and the ruling freezes "the list in `CI_WORKFLOWS.md` after step 1".
   - components.txt includes attempt 2. It raises no maximum: its aggregate's 163 s checkout was full-history, not depth-one, and its workers were cancelled during setup.
   - I briefly narrowed the list in my working tree and restored it before committing. The committed text is unchanged there.

## Findings and changes (file:line at 9104a8fc)

| Finding | Item | Change |
|---|---|---|
| R767-3-F1, R768-3-F1 (ruling item 1) | 1 | **`scripts/ci_litex_legs.py`:** `:47-49` (`LARGEST` covers 41705989293 a1/a2), `:56` (gptp 477), `:68-70` (`SETUP` 739, worker 1, a2), `:74-76` (`SELFTEST` 4, worker 2, a2). `LEG_BUDGET` is derived as 926. **`scripts/ci_gate_workflows.py`:** `:62-64` (aggregate 111 s, margin 69, depth-one checkout 26). **`ci/image/command-table.json:13614`:** `ci_litex_legs.py` re-pinned to its new sha256. **`docs/testing/CI_WORKFLOWS.md`:** `:1674-1679` (`LARGEST` runs, `LEG_BUDGET` 926), `:1691` (477 / 448 / 794), `:1720-1721` (ctrl cold 280, 224, 284, 240 and 277), `:3137-3163` (cited runs, setup, builder projections and largest job times, self-test 4, `LARGEST`, LiteX projections, spans), `:3169` (926), `:3176-3185` (aggregate 111, collector 183, tail 29, allowance 443), `:3212-3214` (cold metadata in 41705989293 too), `:3238-3242` (table 1869/831, 1858/842, 1651/1049, 1622/1078, 1968/732), `:3281-3295` (workflow 2312 / 2411, history 2013 / 2111 and 1953, setup rise 739: checkout 274, LiteX install 277, VexiiRiscv 108), `:3347` and `:3349` (aggregate 111 / 69, collector 183). |
| Ruling items 2 and 3 | 2 | `CI_WORKFLOWS.md:3187-3191`: the cited runs are frozen, and the rule's "later hosted measurement" now applies to the next re-measurement under acceptance 1. `:3201-3207`: the merge bar (a job at its timeout, an elaborate worker's span above 2100 s, a LiteX simulation unrun, run twice or unreported, the union verifier refusing), with a component above its figure being an observation. PR-BODY.md, Round 4: one sentence, linking the ruling. |
| R767-3-R1 | 3 | `CI_WORKFLOWS.md:3147-3149`: "Their largest measured job times with the LiteX legs apart are 1535 …". |
| R767-3-R2 | 3 | `CI_WORKFLOWS.md:3171-3172`: "and `ci_gate_workflows_selftest.py`, through the LiteX leg controls, requires each LiteX worker's generated limit to equal the 2700 seconds it starts from". PR-BODY.md: "The gate workflow self-test requires" (Round 3 item 1) and "fails `ci_gate_workflows_selftest.py` in its LiteX leg controls" (How to validate). |
| R768-3-RS1 | 3 | `CI_WORKFLOWS.md:3216`: "on metadata that builder leg 1 had generated". |
| R768-3-S2 | 3 | `CI_WORKFLOWS.md:1673-1680`: the LiteX legs paragraph is rewrapped, with no line over 78 characters. |
| R767-3-S2 | 3 | PR-BODY.md: round 2's "Derived per job" through its workflow paragraph moved under "## Superseded (round 2)", after Round 3 and Round 4, with a Contents entry. |
| R767-3-S1, R768-3-S1, observations | - | Declined by the ruling. Not taken (#837 holds S1). |
| R768-3-F2 | - | Settled by the ruling as outside this PR. No change. |

## Recomputed figures (receipts/hosted/components.txt)

Measured, the component maxima over the frozen cited set:

| Component | Round 3 | Round 4 | Source |
|---|---:|---:|---|
| setup | 485 | 739 | elaborate-gates-1, 41705989293 a2 (checkout 274, LiteX install 250, VexiiRiscv 108) |
| test_gptp_tx_timestamp | 462 | 477 | 41705989293 a2 |
| self-test (leg step less rows) | 3 | 4 | elaborate-gates-2, 41705989293 a2 (481 - 477) |
| cold Verilator | 431 | 431 | elaborate-gates-3, 41678609075 a1 |
| builder leg 0 / 1 | 1130 / 1119 | 1130 / 1119 | 41583428850 / 41476923392 a3 |
| collector | 149 | 183 | 41705989293 a1 |
| tail | 25 | 29 | 41705989293 a1 |
| depth-one checkout | 19 | 26 | Cancel late CI failures, 41705989293 a1 |
| aggregate less checkout | 85 | 85 | 41678609075 a3 |
| other LARGEST members | | unchanged | cpu 72, ctrl 284, gmii 0, boot 25, mem 15, retained 336, soc 510 |

Derived:

| Figure | Round 3 | Round 4 |
|---|---:|---:|
| LEG_BUDGET | 1181 | 926 = 2700 - 600 - 739 - 431 - 4 |
| legs at LARGEST | 462 / 448 / 794 | 477 / 448 / 794 (fit) |
| worker 0 / 1 (margin to 2700) | 1615 (1085) / 1604 (1096) | 1869 (831) / 1858 (842) |
| LiteX cold 2 / 3 / 4 (margin) | 1381 / 1367 / 1713 | 1651 (1049) / 1622 (1078) / 1968 (732); to 2100: 449 / 478 / 132 |
| LiteX Verilator restored | 950 / 936 / 1282 | 1220 / 1191 / 1537 |
| aggregate (margin to 180) | 104 (76) | 111 (69) |
| allowance | 398 | 443 = 111 + 183 + 120 + 29 |
| workflow warm / cold | 2013 / 2111 | 2312 (38.5 min) / 2411 (40.2 min) |

Measured spans in 41705989293, workers 0 to 4:
- attempt 1: 1535 / 1132 / 1414 / 1148 / 1233;
- attempt 2: 1304 / 1449 / 907 / 909 / 948.

Each span is below its projection, and all are inside 2100.

STOP check: the partition fits 926, and every projection is inside 2700 - 600 = 2100. The tightest is worker 4 cold at 1968. No STOP.

## Records touched

| Record | Touched | How / why |
|---|---|---|
| scripts/ci_litex_legs.py | yes | LARGEST gptp, SETUP, SELFTEST and their comments (item 1) |
| ci/image/command-table.json:13614 | yes | re-pin of ci_litex_legs.py (item 1) |
| scripts/ci_gate_workflows.py | yes | comment only: aggregate 111 / 69 / 26 (item 1). `--check` rc 0, generated workflow unchanged |
| docs/testing/CI_WORKFLOWS.md | yes | items 1, 2, 3 |
| .github/workflows/*, .github/ci-templates/* | no | g01 rc 0 |
| scripts/ci_litex_legs_selftest.py, scripts/ci_gate_workflows_selftest.py | no | |
| ci/image/tool-inventory.json, exec-audit-receipt.json | no | declined observation, as in round 3 |

## Gate table (at 9104a8fc; logs and rc in receipts/)

| Gate | rc | s |
|---|---:|---:|
| g01 python3 scripts/ci_gate_workflows.py --check (re-run last, after the mutant restore) | 0 | 0 |
| g02 python3 scripts/ci_events.py --check (2199 items) | 0 | 1 |
| g03 python3 scripts/ci_events.py --selftest (2199 items, 5489 arms; log 353 KB, .ref) | 0 | 223 |
| g04 scripts/run_litex_sims.sh --selftest (16 checks) | 0 | 2 |
| g05 python3 scripts/ci_litex_legs.py legs (461/440/520; at largest 477/448/794) | 0 | 0 |
| g06 LiteX leg 0 own command (test_gptp_tx_timestamp PASS 518 s) | 0 | 518 |
| g07 LiteX leg 1 own command (cpu 90, gmii 0, boot 29, mem 15, retained 276, each PASS) | 0 | 410 |
| g08 LiteX leg 2 own command (ctrl 73, soc 570, each PASS) | 0 | 643 |
| g09 `ci_litex_legs.py union` over g06-g08's receipts → "litex: 8 simulations exactly once, each a pass" | 0 | 0 |
| g10 control, `LARGEST` test_gptp_tx_timestamp 927 → "LiteX legs refused: a LiteX leg holds 927 measured seconds at its largest, above its 926; re-derive the legs or add a leg"; 926 accepted; restored byte-equal, accepted (receipts/g10-control-largest-over-budget.txt; on a `git archive HEAD` copy because the legs were running in the lane) | 1 at 927 (expected), 0 at 926 and restored | 0 |
| g10a control: test_pp_boot_bus_freeze dropped from leg 1's receipt → "LiteX legs refused: LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze" | 1 (expected) | 0 |
| g10b control restored | 0 | 0 |
| g11a aggregate verifier (`ci_gate_receipts.py verify --workflow elaborate`) over the real LiteX receipts | 0 | 1 |
| g11b verifier, dropped → "gate evidence refused: LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze" | 1 (expected) | 0 |
| g11c verifier restored | 0 | 1 |
| g12 git diff --check e61a4afa HEAD (re-run last) | 0 | 0 |
| g13 ci_gate_workflows_selftest.py | 0 | 17 |
| g14 ci_litex_legs_selftest.py (its over-budget plant now reads "927 ... above its 926") | 0 | 0 |
| g17 cd tests && behave --no-capture -f plain (508 scenarios; .ref) | 0 | 3 |
| g18 python3 scripts/ci_scope.py --selftest | 0 | 25 |
| g19 act_ci.validate_workflow_sandbox(elaborate) → None | 0 | 0 |
| d05 d06 d07 d33 d36 d37 d40 d42 d47 d50, the docs workflow's run steps that read the changed docs and scripts | all 0 | 8/4/0/1/12/1/0/12/32/9 |
| m01 mutant in the lane: LiteX worker limit 45 → 44 minutes, regenerated → `ci_gate_workflows_selftest.py` rc 1 with `AssertionError: ('elaborate', 2, 44)`, `ci_litex_legs_selftest.py` alone rc 0 (supports R767-3-R2's attribution). Restored with git checkout of the three files, the tree equal to HEAD^{tree}, `--check` rc 0 (receipts/m01-job-limit-mutation.txt) | 1 (expected) | - |

Notes:
- **g17 was run twice.** The first try called a bare `behave`, which is not on this host's PATH, and got rc 127. It was re-run as round 3 did, with the scratch docs venv's `python -m behave`, and got rc 0. The rc 127 receipt was overwritten under the same label.
- **The three legs ran concurrently** in my unit, on CPUs 96-111. Peak memory stayed about 1.3 GB.
- **A first m01 attempt on a `git archive` copy was not valid.** The gate self-test failed there for an unrelated reason: the export has no submodules, so `make -n` in `tb/verilator/capture_coherence` exits 2. The valid m01 ran in the lane after the legs had finished.
- **Not run:** `act_ci.py --selftest`, the candidate's copy in docs steps d38 and d39, because the agent contract forbids running the candidate's copy on the host. d38's other half is g02 and g03. The docs workflow file is unchanged, and its other steps read none of the changed files.
- **The gate script always exits 0 itself.** The rc in each .rc file is the gate's own exit status. Every .rc names head 9104a8fc68979a7a8795859e8704aef27ea0634d.
- **Leg receipts:** receipts/litex-leg-{0,1,2}.json, with sha256 in receipts/litex-leg-receipts.sha256.

## Real limits

- **The figures are hosted maxima** over the frozen cited set, which ends at run 41705989293 attempt 2. Under the ruling, later hosted runs feed the next re-measurement under #737 acceptance 1. They are not a re-measurement of this PR.
  - The manager's hosted run at the pushed head is judged only by the merge bar in `CI_WORKFLOWS.md:3201-3207`.
  - The tightest projection, a cold worker 4 at 1968 s, is 132 s inside the 2100 s line. A worker span above 2100 s at the merge head would be a finding under that bar, and the ruling names the depth-one worker checkout as its fix.
- **The local leg times are not hosted figures.** `test_soc_timing_cuts` took 570 s locally, above its hosted 510, on a shared host with three legs running at once. `test_ctrl_memory` took 73 s, because the scratch venv already held the CPU metadata.
- **#737 acceptance 1 is open.** The workflow figure is 2312 / 2411 s.
