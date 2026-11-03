# HANDOFF — [A727d] issue #737 round 3, PR #836 — STOPPED on item 1

Lane: $LANES/737-elab-split, branch 737-elab-split, origin https://github.com/kebag-logic/milan-fpga.git (confirmed). Base dev e61a4afa.
Start head e180ba30 (round 2, also PR #836's head). **Final local head ae7412eb293c6a52d64f86b57e69835c7d20121a** (4 commits over e180ba30, one per item). Nothing pushed.
Unit milan-737-a727d.service, CPUs 96-111. Scratch $VALIDATION_STORAGE/737-a727d. Receipts: receipts/ beside this file (each gate's .log and .rc; logs over 200 KB as .log.ref with size and sha256; hosted/ holds the jobs API files under 200 KB, the sha256 and sizes of all hosted files, and the timing scripts).
Authority: round 3 ruling issuecomment-6611061323. Reviews: R767-2 issuecomment-6610985935, R768-2 issuecomment-6611052254.

## Status
- [x] TAKEN posted: issuecomment-6611079006 (receipts/taken.md)
- [x] item 1 bounds from component maxima: f66312c4. **Broken by attempt 3 of run 41678609075, which finished after the commit. STOP.**
- [x] item 2 CPU-metadata cache: a174e9e5
- [x] item 3 aggregate checkout: e4d52a12 (one docs placement defect, see Known defects)
- [x] item 4 residues and suggestions: ae7412eb
- [x] gates at ae7412eb (table below), except the three local LiteX leg runs (not run: the STOP may change the legs)
- [x] STOP posted (see the last line)

Commits (one-line subject, no body, no trailers):
- f66312c4 Build every elaboration projection and LEG_BUDGET from each component's largest value over the cited hosted runs, run 41678609075 included, keep the legs while they fit at the members' largest seconds, and state the rule a later measurement follows (#737)
- a174e9e5 Carry the CPU metadata cache and the step that fills it only on the builder worker whose leg runs the elaboration gates that generate the metadata, so builder worker 0 no longer saves the key empty, and say what the warm ctrl_memory figure measured (#737)
- e4d52a12 Check out only the head in the elaborate aggregate, whose full-history fetch reached its 3-minute limit, and state that limit's margin over the measured maximum and why the other full-history elaborate jobs keep theirs (#737)
- ae7412eb Name the builders' shared caches, the CPU metadata steps and their worker literally in the LiteX legs self-test, and record run 41583428850's spans in the jobs API's whole seconds (#737)

## The STOP (item 1)

When I committed item 1, attempt 3 of run 41678609075 (the manager's re-run at e180ba30) still had two workers queued. Item 1 therefore used attempts 1 and 2. Attempt 3 completed at 18:10 UTC: all five workers succeeded, and every simulation ran once and passed. It raises the following components (receipts/hosted/timing-41678609075-a1-a3.txt, component-maxima.py/.txt).

| Component | Item 1 figure (a1) | Attempt 3 |
|---|---:|---:|
| setup (span less gate step and Verilator build) | 255 | 362 / 399 / 442 / 485 / 398 (workers 0 to 4) |
| `test_soc_timing_cuts` | 369 | 510 |
| `test_gptp_tx_timestamp` | 461 | 462 |
| `test_ctrl_memory` | 280 | 284 |
| cold Verilator | 431 | not built (restored) |
| builder leg 0 / 1 | 1130 / 1119 | 635 / 845 |

Where the setup excess comes from, in seconds:

| Worker (attempt 3) | Full-history checkout | `Install LiteX at the pinned revisions` | VexiiRiscv placement |
|---|---:|---:|---:|
| gates-3 | 208 | 143 | 59 |
| gates-4 | 184 | 109 | 36 |
| gates-0 | 156 | 89 | 56 |

The LiteX workers' pip install has had no pip cache since option (B).

Applying the ruling's rule (setup 485, cold Verilator 431, allowance 338, self-test 3):
- `LEG_BUDGET` = 1800 - 338 - 485 - 431 - 3 = **543**.
- The current legs at the members' largest seconds hold 462 / 448 / 794.
- The members' largest seconds total 1704, so three legs need at least 568 each. By exhaustive search, the best three-leg fullest leg is 620 and the best four-leg one is 510, which fits.
- So the legs cannot be re-derived within three LiteX workers. A fourth worker is one more concurrent runner per head, and round 2's queueing decision kept three.
- Builder worker 0 projects at 485 + 1130 = **1615**, 5 s inside its 1620 own bound. The workflow then projects at 1615 + 338 = **1953 s**, above #737 acceptance 1's 1800 s.
- That holds even at the former 270 s allowance (1885), and whatever the LiteX legs do.
- No ruling covers dividing builder leg 0, which is a single gate, or a projection above 30 minutes.
- Attempt 3's `elaborate` aggregate was cancelled again at its 3-minute limit, with "The job has exceeded the maximum execution time of 3m0s".
  - It spent 149 s in the full-history checkout that ae7412eb removes, and 85 s of span outside it, most of that the cancellation tail. Its collector took 117 s.
  - Read strictly, those 85 s raise the aggregate component from 44 to 19 + 85 = 104, and the allowance from 338 to 398. That only deepens the STOP.

Options for the manager (I choose none):
- (a) a fourth LiteX leg;
- (b) cut the setup:
  - the workers' full-history checkout. Their scope step needs only the head's parent on hosted runs, but `fetch-depth: 0` is the only depth the checkout contract in `scripts/ci_events.py` admits, and that file is in the act trust set.
  - the LiteX workers' cold pip install, from option (B);
- (c) bound setup by a stated figure, or exclude a hosted-latency outlier from the maxima;
- (d) accept a projection above 30 minutes and keep acceptance 1 open.

## Findings and changes (file:line at ae7412eb)

| Finding | Item | Change |
|---|---|---|
| R767-2-F2, R768-2-F1 | 1 | `scripts/ci_litex_legs.py:51` `LARGEST`: each member's largest verdict row over runs 41583428850 and 41678609075 (a1). `:62-69` `LEG_BUDGET = 773`, from 1800 - 338 - 255 - 431 - 3. `:37` `SECONDS` still derives the legs. `:84-110` `partition()` refuses a leg above `LEG_BUDGET` at `LARGEST` with "re-derive the legs or add a leg", and `legs` prints both sums. Self-test `scripts/ci_litex_legs_selftest.py:54-77`: LARGEST covers the inventory and is never below SECONDS; a missing LARGEST entry is refused; a later larger measurement that overfills a leg is refused ("at its largest"). Docs `docs/testing/CI_WORKFLOWS.md:1670-1690` (legs). `:3135-3175` (component maxima; projections 1385 / 1374 / 1150 / 1137 / 1338, warm 719 / 706 / 907; the 338 s allowance at `:3157-3165`). **The re-measurement rule is stated once, at `:3167-3175`.** Table rows `:3203-3207`, workflow 1723 s `:3245-3249`. Re-pinned `ci/image/command-table.json:13614`. **Broken by attempt 3: see the STOP.** |
| R767-2-F1, R768-2-F2 | 2 | `scripts/ci_gate_workflows.py:52-58` `METADATA_STEPS` (the cache plus "Keep the generated CPU netlist arguments for the next run"). `:485-492` `metadata_worker()` finds the builder worker whose leg holds every `--require-elaboration` gate of `ci_builder_legs.py` (worker 1), and refuses gates split across legs. `:460-482` `builder_caches()` requires each worker to carry both steps exactly once, then keeps them on that worker alone (`:480`). Generated `.github/workflows/elaborate.yml`: `elaborate-gates-0` loses the cache and the fill step, `-2` to `-4` the fill step. Template contract `.github/ci-templates/elaborate.yml:218-226`; `BUILDER_CACHES` comment `scripts/ci_gate_workflows.py:45-50`. Docs `CI_WORKFLOWS.md:1692-1723`, and the warm-figure correction at `:3177-3185`. Self-test `scripts/ci_litex_legs_selftest.py:170-178` (per-worker steps) and `:200-226`. The new plants are refused (g13 log lines 184-188): the generating builder without its fill step, a LiteX worker repeating it, and elaboration gates split across builder legs. Mutation m02 (removal a no-op) fails the self-test. |
| R767-2-F3, R768-2-F3 | 3 | `scripts/ci_gate_workflows.py:59-65`: `HEAD_ONLY_AGGREGATES = {"elaborate"}` and `AGGREGATE_TIMEOUT = 3`, with the derivation. `:264-268` drops `fetch-depth` from the elaborate aggregate's checkout. Generated `.github/workflows/elaborate.yml:1196` (`- uses: actions/checkout@v4`, no `with`). The docs aggregate is unchanged. Self-test `scripts/ci_litex_legs_selftest.py:189-197` `aggregate_controls`; mutation m03 fails it. Docs `CI_WORKFLOWS.md:3157-3160` and `:3273-3282`. Act sandbox: g19 accepts. |
| R767-2-R1 | 4 (via 1) | The sentence was replaced in item 1. Worker one's figure is now its component sum, and its measured 1240 is named separately (`CI_WORKFLOWS.md:3141-3146`). |
| R767-2-S1 | 4 (via 1) | APPLIED by item 1: worker 1 projects at setup + builder leg 1 (255 + 1119 = 1374). |
| R768-2-S1 | 4 | APPLIED. `scripts/ci_litex_legs_selftest.py:24-30` holds `SHARED_CACHES`, `METADATA` and `METADATA_WORKER` as literals. `:170-178` asserts the generator's constants equal them and checks each worker against them. Mutants m06 (R768's: the metadata cache dropped from `BUILDER_CACHES`, workflow regenerated) and m07 (the fill step dropped from `METADATA_STEPS`) each fail the self-test (receipts/m06-m07-literal-name-mutations.txt). |
| R768-2-S2 | 4 | APPLIED. `CI_WORKFLOWS.md:3252-3254` reads 1883 / 2307 / 2825, "in the jobs API's whole seconds". The PR body matches. |
| R768-2-S3 | 2 / 4 | The fill step is off the LiteX workers (item 2). DECLINED: removing the copy in "Place the VexiiRiscv source at the revision LiteX pins". That step also runs `ci_litex_env.py`, which places the source every worker needs. Its script is pinned verbatim by `scripts/ci_events.py` (act trust set), and the copy from an absent directory is a no-op. |
| R768-2-S4 | 4 | No change: an observation with no defect. |
| R768-2-RS1 | 4 | APPLIED in PR-BODY.md (round 2 item 5 row), exact text. |
| Observations (package-cache tar failure; artifacts 404) | - | Not this PR. Left for the manager as candidate Issues. |

## Known defects at ae7412eb (to fix with the item 1 rework)

- `docs/testing/CI_WORKFLOWS.md:3273-3282`: item 3's new paragraph absorbed the start of the receipts paragraph that followed it. Its last line continues with " The existing documentation-only elaboration skip remains valid...".
  - **Fix:** end the new paragraph after "under its 45 minutes.", start a new line with "The existing documentation-only", and move the new paragraph below the whole receipts paragraph (which ends "...The docs builder has no ...").
  - This was found after the item 3 and item 4 commits, and one commit per item was required, so it was not fixed here.

## Item 2 evidence: who generates and who reads the CPU metadata

- **Code.** LiteX `litex/soc/cores/cpu/vexiiriscv/core.py` `args_read` writes `<data_location>/<md5(metadata args)>.py` with sbt's PythonArgsGen only when that file is absent, then reads it. So every reader generates whatever it lacks, and no worker reads without generating.
- **Builder leg 1** (`elaborate-gates-1`) generates.
  - Local e01, at e180ba30 with the metadata moved aside, ran `test_builder.py --gates test_every_recipe_elaborates --require-elaboration`. Gate 23g took 93 s and wrote `fc22d570….py` (receipts/e01-*).
  - In run 41678609075 a1, at a cold key, gate 23g on gates-1 took 5 s, so the leg had already generated the metadata.
- **Builder leg 0** (`elaborate-gates-0`, `test_baremetal_profile_contract` alone) neither generates nor reads.
  - At a1's cold key its fill step found nothing, and it saved 201 B.
  - The same happened in runs 41470524727 (200 B) and 41476923392 (201 B).
- **LiteX legs.** Round 2's local leg runs moved the metadata aside before leg 0 and found none present before leg 2.
  - Legs 0 and 1 generated none.
  - Leg 2 (`test_ctrl_memory`, `test_soc_timing_cuts`) generated `fc22d570….py`.
  - Under option (B) and item 2, no LiteX worker carries the steps.
- **Result:** one saver. On a second attempt at an unchanged key, `elaborate-gates-1` should restore a non-empty entry. Only the hosted run after the push can show this.

## Per-leg timing (measured and derived)

Partition (`legs`, g05) is unchanged: 0/3 {gptp} 461 s, 1/3 {cpu, gmii, boot, mem, retained} 440 s, 2/3 {ctrl, soc} 520 s (SECONDS, run 41583428850).

| Leg | Worker | Members | 41583428850 s | 41678609075 a1 s | 41678609075 a3 s | LARGEST at ae7412eb (a1) | With a3 | Item 1 cold projection | Measured spans 41583428850 / a1 / a3 |
|---|---|---|---|---|---|---:|---:|---:|---|
| 0/3 | gates-2 | gptp | 461 | 246 | 462 | 461 | 462 | 1150 | 585 / 706 / 906 |
| 1/3 | gates-3 | cpu, gmii, boot, mem, retained | 70+0+25+14+331 | 72+0+25+15+336 | 71+0+25+14+333 | 448 | 448 | 1137 | 616 / 1021 / 930 |
| 2/3 | gates-4 | ctrl, soc | 280+240 | 224+369 | 284+510 | 649 | 794 | 1338 | 1226 / 1178 / 1194 |

- Derived at ae7412eb (a1 maxima): workers 0 / 1 project at 1385 / 1374, against measured maxima of 1254 and 1240 (worker 1 less its old LiteX step). The workflow is 1385 + 338 = 1723 s, and LEG_BUDGET is 773.
- With a3: setup 485, LEG_BUDGET 543, worker 0 1615, workflow 1953. The attempt 3 spans themselves stayed below the item 1 projections (906 / 930 / 1194 against 1150 / 1137 / 1338). What breaks is the derivation, not a span.
- Aggregate and checkout figures (receipts/hosted/aggregate-checkouts.txt):
  - The watcher's and tail's depth-one checkouts took at most 19 s.
  - The aggregate span less its checkout took at most 25 s.
  - The collector took at most 149 s and the tail at most 25 s.
  - The aggregate's full-history checkout took 260 s in a1 (cancelled at 3 min) and 163 s in a2.
- Not run locally this round: the three leg commands, because the STOP may change the legs. `SECONDS` is unchanged, so round 2's real receipts still match these legs (g09).

## Records touched

| Record | Touched | How / why |
|---|---|---|
| .github/workflows/elaborate.yml | yes | Regenerated (items 2, 3); `ci_gate_workflows.py --check` rc 0. |
| ci/image/command-table.json:13614 | yes | `scripts/ci_litex_legs.py` re-pinned to 90059176… after reviewing the change (item 1). No other pinned file changed. |
| scripts/act_ci.py, scripts/ci_events.py, scripts/ci_tool_inventory.py | no | Unchanged since e180ba30 (g19). The checkout contract admits a checkout with no `with`. |
| ci/image/tool-inventory.json | no | Still lists gates-0's `Cache the generated CPU metadata`. `ci_tool_inventory.py --check` refuses on this host (`CI_IMAGE_SHFMT must name the checksum-pinned Bash parser`), and no workflow runs it. Round 2 left it for the same reason. |
| ci/image/exec-audit-receipt.json | no | An image trace pinned to an older source. |
| .github/workflows/docs.yml and its template | no | The docs aggregate keeps its full fetch, because item 3 names elaborate jobs only. Its same 3-minute exposure is a candidate Issue. |

## Gate table (at ae7412eb; logs and rc in receipts/)

| Gate | rc | s |
|---|---:|---:|
| g01 python3 scripts/ci_gate_workflows.py --check | 0 | 0 |
| g02 python3 scripts/ci_events.py --check (2199 items) | 0 | 1 |
| g03 python3 scripts/ci_events.py --selftest (2199 items, 5489 arms: 18 fewer than e180ba30, from the removed metadata steps; log 353 KB, .ref) | 0 | 234 |
| g04 scripts/run_litex_sims.sh --selftest (16 checks) | 0 | 2 |
| g05 python3 scripts/ci_litex_legs.py legs (461/440/520; at largest 461/448/649) | 0 | 1 |
| g09 `ci_litex_legs.py union` over round 2's real leg receipts (legs unchanged; sha256 in g09-receipts.sha256) | 0 | 0 |
| g10a control: `test_pp_boot_bus_freeze` dropped from leg 1 → "LiteX legs refused: LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze" | 1 (expected) | 0 |
| g10b control restored | 0 | 0 |
| g12 git diff --check e61a4afa HEAD | 0 | 0 |
| g13 ci_gate_workflows_selftest.py | 0 | 15 |
| g14 ci_litex_legs_selftest.py | 0 | 0 |
| g17 cd tests && behave --no-capture -f plain (508 scenarios; .ref) | 0 | 4 |
| g18 python3 scripts/ci_scope.py --selftest | 0 | 29 |
| g19 act_ci.validate_workflow_sandbox(elaborate) → None | 0 | 1 |
| d05 d06 d07 d33 d36 d37 d40 d42 d47 d50 (docs workflow run steps that read the changed docs, template and scripts; docs workflow unchanged since e61a4afa) | all 0 | 8/3/1/1/12/1/0/12/35/10 |
| m02, m03, m06, m07 mutants (each fails the gate self-test; files restored) | non-zero (expected) | - |
| e01 builder gate 23g with cold metadata (item 2 evidence, at e180ba30) | 0 | 95 |
| NOT RUN: the three local LiteX leg commands (STOP); `act_ci.py --selftest` (candidate copy, not run on the host) | - | - |

## Real limits

- Item 1's committed figures are broken by attempt 3. The lane needs the manager's decision before item 1 can close.
- The non-empty metadata restore on `elaborate-gates-1` can only be shown by a hosted second attempt after the push.
- The elaborate aggregate's head-only checkout is proved by the generator, the self-test, the contract and the act sandbox. No hosted run shows it yet. When last checked, attempt 3's aggregate was still running with the old full-history checkout.
- The docs-check aggregate carries the same full fetch under 3 minutes (candidate Issue).

STOP posted: issuecomment-6611939319 (head ae7412eb293c6a52d64f86b57e69835c7d20121a); text in receipts/stop.md
