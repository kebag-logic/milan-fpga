[R784] NEGATIVE - exact head eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65

# R784-1: external review of #665 lane S5 (PR #844), the F2 to F5 timing hooks on the target core

- Head under review: `eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65`, tree `883f71864feecfd59543c9c94e5c4f6835019238`, `665-s5-hooks` -> `dev-soft-core`, source base `5b5f4336`.
- Delta: `git diff 5b5f4336..eef3d97a`, 8 one-line commits, 7 files, +2665: the new `tb/verilator/ctrl_service_hooks/` (README, `hooks.py`, `hooks_build.py`, `hooks_selftest.py`, `hooks_soc.py`, `run.py`) and one `OUTSIDE` entry in `sw/firmware/ctrl/test/ctrl_configs.py`.
- Reconstructed from: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #665 body and its manager and owner comments (the S5 assignment 6513150371, the T_svc ruling 6495692075, the clock correction 6508196970, the 100 MHz decision 6514866239, the 2026-11-04 rulings 6630265194 and 6634982529, the round 16 ruling 6674728988 and the REVIEW READY 6676840432), the PR body, FR_NFR.md 3.4.1 and 3.4.2, the mailbox RTL (`KL_mbx.sv`, `KL_mbx_rx.sv`) and contract (`mailbox.yaml`), `milan_soc.py`, the CPU budget harness it imports, and the author's published receipts at `c30339bc/review-evidence/665s5-r1`.
- Prior public review findings on PR #844: none exist. The PR has only the two review-start notices, and no reviews or review comments. There is nothing to resolve or retain.

**Verdict: NEGATIVE.** The measurement is sound and reported faithfully, misses included. Two MINOR findings remain open under the Tests lens:

- the `counters-late` plant's verdict is satisfied without the plant;
- the held push's bound and the table's worst-path selection have no self-test check.

Neither finding changes a published figure.

## Focus checks

| # | Check | Result |
|---|---|---|
| 1 | Split CPU at its product clock of 100 MHz, Milan clock unchanged, both points, both arms | **Holds in substance, with one wiring nuance (S-1).** Every published run's `build.json` records `cpu_clock sys`, `cpu_hz 100000000`, `sys_hz 100000000`, `milan_hz 50000000`. At 8x8 it also records the ledgered `platform-8x8-two-interfaces`. The CPU is not clocked from `cd_sys` itself. `hooks_soc.py:220-238` keeps this base's `cpu_clk = ClockSignal("milan")` and its milan-to-sys memory crossing (`milan_soc.py:3079-3080`), and runs the test SoC's `milan_clk` clocker at the sys frequency. In this SoC (`with_milan=False`) nothing else is on `cd_milan`. `KL_mbx`, its ms tick, `timer0` and the CSR file are on `sys` (`split_soc.py:188,197`; `hooks_soc.py:231`). The firmware's time base is the mailbox TICK's `now_ms` (`mbx.c:469-471`), not a CPU-clock constant. So frequency, bus and time base are the product's. The only difference is the equal-frequency crossing's latency, which makes the figures pessimistic. README:82 and :401 and the PR's Limits disclose it. |
| 2 | Each hook against its own bound, none relaxed; results state exactly what was measured | **Holds.** `hooks.bound_ms` = min(20, `scenario.CEILING_MS`): ADP, DISC, ACMP, AECP, NOTIFY and MAAP get 20 ms, SRP 18. That matches ruling 6495692075. Every published row's `bound_ms - wait_ms` is in {20, 18}. The only W rows are `srp.domain` (W 200 ms, from the CPU budget harness) and `counters.held`, whose bound is 20 ms without W. Recomputed from the receipts: **alone**, every hook fits at both points and on both arms, except H-COUNTERS' ALL push: 27.58 ms at 1x1 and 218.71 ms at 8x8. **Under the composed load**, every hook has at least one miss at both points and on both arms, with two exceptions. H-DISC at 1x1 on the answering arm fits: its 2 loaded paths are within, the worst at 14.03 ms. H-COUNTERS runs on the answering arm only. The focus wording "every hook misses" therefore has one exception, and the author's text states that exception correctly (README:344, PR Status). |
| 3 | Composed windows a full refill after the registrations; aging group one interface at a time; each grader's mutant caught by name | **Partly.** The refill wait is max((burst+1) x refill_ms) = 180 ms. That covers `KL_mbx_rx.sv:603-605` (one token per period, starting at an arbitrary phase) for every channel in `mailbox.yaml`. `check_buckets_full` checks it and its mutant is caught. The aging group binds, waits, answers and settles per interface (`hooks.py:429-432`); `check_aging_group` and two mutants pin it. All four runs measure `hooks-disc-aging` on every interface. The self-test passes: 22/22 checks, 31/31 mutants. But three grading rules have no check, and their mutants escape (F-2). The `counters-late` plant's verdict cannot fail (F-1). |
| 4 | No firmware, RTL or shared harness file edited; plants never edit the checkout | **Holds.** The delta touches no RTL or firmware source and no S2 or S3 harness file. Those harnesses are imported and runtime-patched only (`unittest.mock`). The one file outside `tb/` is `ctrl_configs.py` (+6, an `OUTSIDE` classification the TSN stack boundary gate needs). It is disclosed in the PR and the REVIEW READY, and is left for the manager to accept as in scope (see Pending). Plants copy `sw/firmware/ctrl` into `<build>/ctrl-planted` (`hooks_build.py:116-123`), and `run.py:245-247` refuses a build directory inside the checkout (`receipts/refusal_probes.txt`). Every plant receipt ends `tree: 0 changed path(s)`. |
| 5 | Receipts back every figure | **Holds.** I recomputed, from the four published `results.json` files (`scripts/figures.py`, `receipts/figures_runs.txt`): every README Results table, the per-hook miss counts, the ordering applied/undecided counts, the H-COUNTERS rows and notice costs, the ACMP owed-command figures (77.84 and 90.26 ms; the commands behind it never served at 363.3 ms), the SRP starvation range (524.8 to 567.5 ms), and the AECP loaded range (48.47 to 205.20 ms). `receipts/figures_history.txt` does the same for the History tables. Each hook's worst path and its set of LATE findings, recomputed from the rows independently of the published summary, agree (`receipts/extra_mutants.txt`). The 16 plant receipts' first findings match README:324-339. `fa925043..eef3d97a` changes only the README, so the head regrade covers the runs. |

**For the manager's scope ruling.** The composed-load misses are measured results on `dev-soft-core` as it is, which is what assignment item 3 asks for. Closing them is firmware work: the SRP construction of S2b round 17 (6674728988 item 1), the ACMP owed-command drop, and the AECP backlog. The S5 STOP rule forbids this lane that work. The lane neither hides nor re-grades them. So the AC "each hook within its bound" stays not met on this base. The PR says so and uses "Relates to #665". Whether S5 can merge as a measurement, or re-measures on S2b's head once #810 merges, is a maintainer decision.

## Findings

### F-1 [R784] MINOR Tests - `tb/verilator/ctrl_service_hooks/run.py:300-305` (with `hooks.py:203-206`) - the `counters-late` plant is reported caught with no plant applied

- **Requirement/evidence.** The S5 assignment, item 5, says each plant "must fail". AGENTS section 6 (Tests) asks that each new test can fail for the defect it claims to detect.
  - The plant's verdict is "any finding of its group starting with `LATE H-COUNTERS:`".
  - Its group, `hooks-counters`, already yields such a finding unplanted: `LATE H-COUNTERS: counters.all.if0: 27.581 ms against its bound 20 ms (hooks-counters)` (published `runs/1x1-ans/results.json`).
  - `scripts/plant_vacuity_probe.py` drives `run.main()` with `--plant counters-late`, with the build and simulation replaced by those unplanted findings. It prints `PLANT counters-late caught: LATE H-COUNTERS: counters.all.if0: 27.581 ms ...` and returns 0 (`receipts/plant_vacuity_probe.txt`).
  - The 15 other plants are sound. Their groups have no unplanted LATE or ORDER finding under their words.
  - The published receipt's first finding names the planted path (`counters.first.if0`, 81.819 ms against 5.64 ms unplanted). So this run did show the defect, but the verdict did not depend on it.
- **Impact.** A plant whose spin no longer delays the push it targets is still reported caught. The "16 of 16 caught" claim is not machine-checked for H-COUNTERS.
- **Required outcome.** A plant counts as caught only on a finding that its defect causes. For example: the plant names the path its words must be found on, or a finding already present in the unplanted baseline does not count. The self-test covers that rule with a mutant.
- **Verification.** The probe's shape: an identity plant, or the unplanted findings, gives `ESCAPED` and rc 1. The real `counters-late` is still caught on `counters.first`. A self-test mutant reverting to prefix matching is caught by name.

### F-2 [R784] MINOR Tests - `tb/verilator/ctrl_service_hooks/run.py:81-96,156-172` and `hooks_selftest.py:343-361` - grading rules without a self-test check

- **Requirement/evidence.** Manager focus item 3: each grader has a mutant caught by name. AGENTS section 6 (Tests).
  - `graded_with` patches `hooks.held_push` to `None`, so no check ever reaches `run.held_row`, and no check reads `run.summary`.
  - Three mutants escape the self-test (`scripts/extra_mutants.py`, `receipts/extra_mutants.txt`):
    1. the held push graded with its W (880 to 896 ms) added to its 20 ms bound;
    2. a held push never sent producing no finding;
    3. the table's "worst" cell picking the fastest path.
  - `check_held_push` pins the eligibility arithmetic only, not the bound applied to it.
- **Impact.** Each of these regressions could relax or misreport a hook's published verdict while the self-test reports 31 of 31. At this head the published figures are right: I recomputed them from the rows (focus check 5). The gap is in the gate, not the numbers.
- **Required outcome.** The held push's bound, without W, and its missing case are each pinned by a check with a mutant caught by name. So is the worst-path selection behind the README tables.
- **Verification.** The three mutants in `scripts/extra_mutants.py` each fail a named self-test check.

### RESIDUE-1 [R784] RESIDUE Docs - `tb/verilator/ctrl_service_hooks/hooks.py:446` - a lane name in a new source docstring

- **Evidence.** "...for the late plants: S2's groups wait as long as their paths take unplanted." The comment rule (owner 2026-10-15) forbids lane names in source comments. This is a new instance in the reviewed delta, the only one over every added `.py` line (`receipts/comment_rule_grep.txt`).
- **Exact fix.** Replace "S2's groups" with "the CPU budget harness's groups".

### RESIDUE-2 [R784] RESIDUE Docs - `tb/verilator/ctrl_service_hooks/README.md:343-344` and the PR body's Status bullets "Alone" and "Under the composed load" - "both arms" also covers H-COUNTERS, which runs on the answering arm only

- **Evidence.** The idle-arm rows of every table show "-" for H-COUNTERS, and README:56 and :97 say it runs only on the answering arm. The two summary sentences read "every hook ... at both points and on both arms".
- **Exact fix.** Append "(H-COUNTERS on the answering arm only, where it runs)" after "on both arms" in README:343 and :344 and in the two PR Status bullets.

### RESIDUE-3 [R784] RESIDUE Docs - `tb/verilator/ctrl_service_hooks/README.md:15` - the 20 ms authority versus FR_NFR at this base

- **Evidence.** At this head, `docs/reference/FR_NFR.md:323,333` still reads "T_svc = 10 ms, proposed". The approved 20 ms and the min(T_svc, ceiling) rule are normative only once S2b round 9's FR_NFR edit (#810) merges. The README already cites the owner's decision and the ruling, not FR_NFR, for 20 ms.
- **Exact fix.** Add after the first sentence of line 15: "FR_NFR.md 3.4.1 at this base still reads the proposed 10 ms; its approved text arrives with #810."

### SUGGESTION (optional)

- **S-1 (Conformance, Docs) - `run.py:56-64` and the PR Status line "CPU 100 MHz on `sys`".** The label names the clock selection, not the wiring measured. The CPU runs on `cd_milan`, driven at the sys frequency behind this base's crossing. The text is disclosed and correct at README:82 and :401. A label such as "CPU 100 MHz (the sys frequency, behind this base's crossing)" would make each table self-describing when quoted alone.
- **S-2 (Robustness) - `hooks_selftest.py:24-34,540-541`.** Run directly, the module's own `__main__` fails with `AttributeError: module 'run' has no attribute 'hook_row'` (`receipts/selftest_standalone.txt`). `hooks` and `hooks_build` put the CPU budget harness's directory first, so `import run` resolves to that harness's `run.py`. The documented entry, `run.py --self-test`, works. Either fix the import or drop the `__main__` block.
- **S-3 (Robustness) - `hooks.py:604-620`.** `frames_received` pairs script frames with receive commits and refusals by cycle order. The parser already tags each commit with its frame's owner (`grade.owner`), so pairing by tag would not depend on commit latency against inter-frame gaps when refused and committed frames are back to back.

## Lens results (artifact-specific)

```text
[R784] PASS Conformance - hooks.py:41,70-78 + scenario.py:91-100 + receipts/figures_runs.txt + hooks_soc.py:213-238 - bounds = min(20, ceiling) per ruling 6495692075 (SRP 18), no row relaxed (bound - W in {20, 18}; held push without W); FR_NFR 3.4.2 hook rows' start and end points match the probes; the CPU at the 100 MHz sys frequency per 6514866239 with the time base on sys; acceptance stated as met and not met exactly as the receipts show
[R784] PASS RTL - hooks_soc.py:84-164 against KL_mbx.sv:503-531,680 and KL_mbx_rx.sv:597-631; milan_soc.py:3079-3080 - no RTL in the delta; test gateware checked: CSR file one-cycle ack with registered read and single write per access; CTR/GSI answer at wait_cycles-1 matches KL_mbx's accept-before-timeout priority and resets per request (busy clears, a new request needs a CPU write); the equal-frequency CPU crossing is the base's and disclosed
[R784] PASS Robustness - run.py:241-264,276-281 + hooks_build.py:104-123,154-164,240-252 + receipts/refusal_probes.txt - refusals by name for a missing build directory, a build inside the checkout, a stale or missing reused build, unknown groups, stale scripts and unanchored edits; plants on a scratch copy; probes rc 2 as documented; S-2 and S-3 optional
[R784] MINOR Tests - run.py:300-305 - counters-late plant verdict satisfied without the plant (F-1)
[R784] MINOR Tests - run.py:81-96,156-172 / hooks_selftest.py:343-361 - held-push bound, missing case and worst-path selection unchecked (F-2)
[R784] PASS Docs - tb/verilator/ctrl_service_hooks/README.md (all sections) + PR body + receipts/figures_runs.txt, figures_history.txt, comment_rule_grep.txt - every figure, table, plant line and cited ruling checked against the receipts and #665; the composed misses, the H-DISC exception, the crossing and the unmeasured rows are disclosed; three RESIDUE wording items only
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `hooks.py` bounds and families, `scenario.py` ceilings, FR_NFR 3.4.1 and 3.4.2, rulings 6495692075, 6514866239, 6634982529 and 6630265194, `hooks_soc.py` clocking, `milan_soc.py:3060-3080`, four `build.json` and `results.json` files | R784-1 | `eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65` |
| RTL | CLEAN | `hooks_soc.py` test gateware against `KL_mbx.sv`, `KL_mbx_rx.sv`, `mailbox.yaml`; no RTL in the delta | R784-1 | `eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65` |
| Robustness | CLEAN | `run.py` refusals, `hooks_build.py` anchors, plants, reuse and digests, refusal probes | R784-1 | `eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65` |
| Tests | UNCLEAN (F-1, F-2) | `hooks_selftest.py` (ran: 22/22, 31/31), 16 plant receipts, plant-verdict probe, 3 extra mutants | R784-1 | `eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65` |
| Docs | CLEAN (3 RESIDUE) | harness README, PR body, REVIEW READY comment, `ctrl_configs.py` entry, comment-rule grep of every added `.py` line | R784-1 | `eef3d97a2b8d74f6c21529eb77cf4e58a3e05c65` |

## What I ran (all in the foreground, at the exact head)

- `python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test`: rc 0, "22 of 22 checks pass; 31 of 31 mutants caught" (`receipts/hooks_selftest.log`).
- `scripts/figures.py` over the published runs, plus a history recomputation (`receipts/figures_runs.txt`, `receipts/figures_history.txt`).
- `scripts/plant_vacuity_probe.py`: F-1 (`receipts/plant_vacuity_probe.txt`).
- `scripts/extra_mutants.py`: F-2, and an independent worst-path and LATE consistency check (`receipts/extra_mutants.txt`).
- Refusal probes (`receipts/refusal_probes.txt`), the standalone self-test entry (`receipts/selftest_standalone.txt`), and the comment-rule grep (`receipts/comment_rule_grep.txt`).
- `git merge-tree --write-tree HEAD a68536fa` (the live `dev-soft-core` tip, unchanged since the author's candidate): clean.
- A hosted-check snapshot (`receipts/hosted_checks_snapshot.txt`).
- After the probes: HEAD, tree, index tree, worktree and index identical to the head, 0 untracked or ignored files, the six gitlinks unchanged and the delta files' blob modes 100644 (`receipts/head_integrity.txt`).

## Real limits

- **No simulation re-run.** I rebuilt no native model and re-ran no point or plant. The per-figure checks are recomputations from the author's published `results.json`, `table.md` and plant logs, plus code reading. They are not an independent simulation.
- **F-1 probe scope.** The probe replaces build, simulation and grade with the published unplanted findings. It exercises `run.main()`'s real verdict code, not a planted image.
- **Gates not re-run.** I did not re-run the firmware self-test, the CPU budget harness, the builder test, the boundary gate, the docs gates or behave. For those I rely on the author's receipts: `fa925043` for the build gates, `eef3d97a` for docs and behave.
- **No source bank.** I make no claim of a manager source bank at this head. The merge-candidate validation is the author's receipt at `88a7e705` (onto `a68536fa`).
- **Hosted CI.** Hosted contexts at snapshot time: 6 pass (bdd-conformance, docs-check-no-git, Prepare pinned Yosys, changes, full-ci-gate, wire-accountability), 1 skipped (Physical gPTP, nightly or manual), 41 pending. A skipped context is not evidence.
- **Hardware.** Physical calibration NOT RUN. No hardware or field evidence is claimed.

## Pending manager duties

- Rule whether the composed-load misses belong to S5's scope or to S2b's round 17 construction, and whether S5 re-measures on S2b's head after #810 merges (the author's open question).
- Rule the H-COUNTERS ALL push: one path from the event to the last push, as FR_NFR 3.4.2 reads, or per descriptor (the author's open question).
- Accept or reject the one shared file outside `tb/` (`sw/firmware/ctrl/test/ctrl_configs.py`, the `OUTSIDE` entry) against assignment item 4's file scope.
- Hosted and act acceptance at the exact head, the current-dev merge candidate's builder and native banks, and linking their receipts.
- Carry the three RESIDUE items to the residue checklist.

R784-1 FINISHED
