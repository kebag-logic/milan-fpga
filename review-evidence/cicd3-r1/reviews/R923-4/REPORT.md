[R923] NEGATIVE - exact head 4f0d7a837512064d67f89938c32e4a064c39ed75

R923-4: composition acceptance review of issue #998 / PR #1003. The PR source head is `b0f2bc1a784d9f006204491c883ac2b1783e970a`, and its two independent POSITIVE source reviews are R923-3 and R924-3. That head is composed onto the validated merge-train candidate `4f0d7a837512064d67f89938c32e4a064c39ed75`, tree `9bc16d519883acd97ddfbfbb31a8b8f3dce73c55`. Its first parent is `b127f378a48adaa404d5a1f74ee352df2c8b532c` (#992's candidate, which carries PR #995 and the lwSRP `d1bb4f4e` pin). Its second parent is the PR head. The merge base is `fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f`.

**Verdict: NEGATIVE, for one MINOR composition finding (C1).** The textual composition is exact. The candidate tree is the clean automatic merge, and each of the three files changed on both sides carries both sides' hunks, with nothing lost or duplicated. The gptp_shadow mutant suite (13/13) and its lifecycle test pass at the candidate. The README's statements are true of the composed tree. But one shared registry interacts semantically. PR #995, on the dev side, doubled gptp_shadow's hosted cost: it went from 260-290 s with nine controls to 517-520 s with thirteen. This PR's 1276 s per-worker deal still prices that suite at 393 s. With the measured window entered, the PR's own dealer self-test fails on 26 workers. Neither source tree has this defect. The composition introduces it.

## 1. Composition: files changed on both sides

`git merge-tree --write-tree b127f378a 4f0d7a83^2` gives `9bc16d51`, which is the candidate tree (`receipts/composition_overlap_check.txt`). No manual resolution exists. The files the candidate changes against dev are exactly the PR's 65. The files it changes against the PR are exactly dev's 41. Three files are on both sides, as the manager stated:

| File | PR side (since `fcbc31f3`) | Dev side (#995, lwSRP pin) | Candidate |
|---|---|---|---|
| `sw/firmware/ctrl/README.md` | `:129` names only `firmware-verilator` as the no-`--capture` job. `:629-632` describes the capture legs and the judge. | `:649` pin `d1bb4f4e`. `:651` adds lwSRP PR #21. | Both. Change lines are identical to each side's (`receipts/composition_overlap_check.txt`). |
| `tb/verilator/gptp_shadow/mutants.py` | Removes `import tempfile`. Adds `import mutant_stage` (`:50`). Stages via `mutant_stage.directory` (`:345`). | Adds ENGINE/GENERATOR/HARNESS anchors, four controls (#106, #107, the credit gate, the harness order) and tuple-capable `planted()`/`apply_control()`. | Both. One `import mutant_stage`, one `planted`, one `apply_control`. No stray `tempfile` import. `py_compile` OK. |
| `tb/verilator/gptp_shadow/test_mutant_lifecycle.py` | Installs `scripts/mutant_stage.py` in fixtures (`:116`, `:376`). Adds `scratch_left()` covering stage slots (`:318-321`). | Imports `planted`. Installs real pinned-dependency targets. Counts are 13. | Both. The fixture installs both `mutant_stage.py` and the real gptp-processor targets. |

Semantic interplay between the two sides of `mutants.py`: the dev side's new targets lie in the `gptp-processor` gitlink (`KL_gptp_engine.sv`, `gen_gptp_ucode.py`) and the suite's `sim_main.cpp`. The PR side's staging root copies them through `copy_inputs(... targets)` at `:347`. The campaign shows this works.

- **Mutant suite:** `make -C tb/verilator/gptp_shadow mutants` with pinned Verilator 5.050 gave rc=0. All 13 were caught, ending `controls: 13   failures: 0` / `RESULT: PASS` (`receipts/gptp_shadow_mutants.log:52-53`, `.rc`). The four dev-side controls are caught by their named checks (`:42-45`).
- **Lifecycle test:** `make -C tb/verilator/gptp_shadow lifecycle` gave rc=0. It ended `mutant lifecycle: PASS (normal/repeat, thirteen named defects, ...)` (`receipts/gptp_shadow_lifecycle.log:52`). Its cancellation records run inside `milan-mutant-stage-*` slots (5 records). These agree with the manager's candidate receipt `full-suite-logs/gptp_shadow.log` (`controls: 13   failures: 0`).

Every README statement checked true at the candidate:

| README line | Checked against |
|---|---|
| `:129` | `rtl-fast.yml:1482`: `firmware-verilator` runs `--selftest --only verilator`, with no `--capture`. |
| `:629` | `rtl-fast.yml:1344-1345`: `firmware-boundary` runs `--without verilator` with two `--capture`. |
| `:631-632` | `rtl-fast.yml:1226-1227`: legs run `--leg K/2 --capture-out`. `ctrl_runs.py:71`: `LEGS`. |
| `:649` | `ctrl_arms.py:438` `LWSRP_REV = d1bb4f4e...` equals the `third_party/lwSRP` gitlink. |
| `:651` | The lwSRP gitlink commit `d1bb4f4` is "Merge pull request #21". |

**Firmware boundary at the candidate.** Here the PR's leg split (`ctrl_runs.LEGS`) meets the dev side's new `srp_own_leaveall.cpp` arm.

- `ctrl_boundary.py --require-rv32 --without verilator --leg 0/2` gave rc=0. It recorded 1888 compiler invocations from `test_ctrl_firmware.py`, and the capture holds the new `srp_own_leaveall` compiles (`receipts/fw_boundary_leg0.log`).
- Leg 1 was REFUSED locally because the `migen` module is missing on this host (`receipts/fw_boundary_leg1.log`). The dev side changes none of leg 1's builders. So the joined judge was not run locally (see limits).

## 2. Gates run at the candidate (all rc=0 unless stated)

- **Repository gates:**
  - `docs_check.py`, also run under the pinned Markdown environment
  - `gen_toc.py --check`
  - `gen_toc.py --verify-anchors`
  - `check_em_dash.py --base b127f378a`, and `--base b0f2bc1a`
  - `ci_events.py --check`
  - `ci_events.py --selftest`
  - `suite_shards.py --selftest`
  - `check_doc_style.py`
  - `check_doc_paths.py`
  - `check_py_idiom.py`
  - `check_submodule_docs.py`
  - `docs_inventory.py --check`
  - `mutant_stage.py --selftest`
  - `git diff --check b127f378a 4f0d7a83`
- **Receipts:** `receipts/gate_*.log`.
- **First attempt at the Markdown gates:** under the host interpreter they refused with "pinned Markdown renderer is not installed". That is an environment issue. They were re-run under the pinned renderer environment and pass.
- **Manager receipts:** the candidate receipts at `$VALIDATION_STORAGE/cicd3-candidate-0923` were spot-checked. Their `head` is `4f0d7a83` and their base is `b127f378a`. All 49 builder-bank commands and the native bank exit 0.

## 3. Findings

### C1 - MINOR - Conformance, Robustness, Tests - `scripts/suite_shards.py:108` (`"gptp_shadow": 393`) with `:57` and `:157`, the deal it feeds, and `docs/testing/CI_WORKFLOWS.md:532-536`

**Authority:** #998 acceptance criterion 2: "Every hosted job stays within 30 minutes with margin." The PR implements it as "every regular worker must project at most 1276 s, allowance included" (`CI_WORKFLOWS.md:532-536`, `suite_shards.py:11-12,57`). Its figure rule is to raise each figure that a measured window exceeded (`suite_shards.py:76-77`, `CI_WORKFLOWS.md:640-646`).

**Evidence.** Each hosted window below was measured with the repository's own `suite_shards.py --measure` (`receipts/hosted_measure.txt`). The tested commits come from each log's checkout line (`receipts/hosted_tested_commits.txt`):

| Hosted run / job | Tree tested | gptp_shadow controls | Window |
|---|---|---|---|
| 45589649197 / 139120946828 | dev `e275d795` | 9 | 260 s |
| 45481508309 / 138756679308 (the PR's third measurement run) | `45d5c35a` merged into `2509db68` | 9 | 290 s |
| 45532703784 / 139035886772 | #992 merged into `e608f8d8` (#995) | 13 | 517 s |
| 45550366428 / 138990302815 (the PR's final run) | `b0f2bc1a` merged into `e608f8d8` | 13 | 520 s |

The 393 s figure dates from `111611fa9` and neither side changed it. It covers the source tree's suite. It does not cover the composed tree's suite, which costs about 520 s.

**Probe.** `probe_gptp_shadow_figure.sh` sets the figure to the measured 520 s and runs the PR's own `suite_shards.py --selftest`, then restores the bytes (`receipts/probe_gptp_shadow_figure.txt`).

- The result is rc=1. The dealer re-deals: gptp_shadow moves from worker 1 to worker 21. Four workers then project above the bound: 10/26 at 1280 s, 20/26 at 1278 s, 22/26 at 1279 s and 23/26 at 1280 s, against 1276 s.
- With the shipped 393 s, the result is rc=0, and worker 1 projects 453+220+393+62+122 = 1250 s.
- The gate passes at the candidate only because its registry holds the source tree's figure.

**Impact:**
- The composed tree's per-worker budget, the PR's means of meeting AC2, is satisfied on paper only.
- On a runner 1.41 times as slow, the worker carrying gptp_shadow is projected over 30 minutes.
- No suite verdict, test or RTL changes. The jobs' hosted `timeout-minutes` (45, and 60 on worker 25) are not threatened by this alone.
- It is a figure and deal defect, not wording, so it is not RESIDUE.

**Required outcome.** Before this composition merges, one of:

- (a) Raise gptp_shadow's figure to at least its composed hosted window (520 s). Re-deal so every regular worker projects at most 1276 s, and record the figure's derivation where the other #998 figures are recorded. The probe shows that a re-deal at 26 workers alone overshoots by 2-4 s, so another lever is needed, such as a worker or a split.
- (b) Publish a maintainer decision that accepts the stale figure until the composed tree's first hosted windows replace it, naming the expected overshoot.

**Verification:**
- `python3 scripts/suite_shards.py --selftest` passes with a gptp_shadow figure of at least 520.
- `--measure` on the composed tree's first hosted worker log shows no regular worker over 1276 s in projection.
- `probe_gptp_shadow_figure.sh <checkout> 520` passes at the new head.

### Out-of-composition observations (do not affect this verdict)

- **O1 - SUGGESTION - Docs - `docs/reference/SUBMODULES.md:1130`.** It reads "It includes PR #12, PR #15 and PR #18." The composed `sw/firmware/ctrl/README.md:651` reads "PR #12, PR #15, PR #18 and PR #21" for the same lwSRP `d1bb4f4e` pin. Both are dev-side (lwSRP pin lane) text, and neither statement is false. Suggested fix, for that lane: "It includes PR #12, PR #15, PR #18 and PR #21."
- **O2 - SUGGESTION - Robustness - hosted run 45550366428.** Three Verilator workers ran past 1276 s of actual wall time: 2/26 at 1500 s, 9/26 at 1459 s and 1/26 at 1373 s (`receipts/hosted_run45550366428_worker_walls.txt`). Most of it was setup: worker 1's suites took 999 s, but its setup took 362 s against the 122 s allowance. This is #1008's area, beside R923-3's S7. It is not composition-introduced.

## 4. Prior public findings on this PR, at this head

These were read after my own pass and probes.

- **RESOLVED at the source, and the composition does not reopen them:** R923-1-F1 and R924-1-F1 (staging lock and root proof), R923-2-F1 (follow_ring recursive make), and R924-2-F1 (capture-matrix fail-fast).
  - The candidate's `scripts/mutant_stage.py`, `tb/verilator/follow_ring/Makefile` and `.github/workflows/rtl-fast.yml` are byte-identical to `b0f2bc1a`. Dev changes none of them.
  - Dev's only interaction is with gptp_shadow's `mutants.py` staging call, which I ran (13/13).
- **R924-2-R1/R2, R923-2-R1 and R923-1-R1/R2/R3 (applied residues):** still applied. The candidate keeps the PR's text in those files, and the dev hunk in the README lies below `:631`.
- **R923-3-R1 - RESIDUE (retained):** `sw/firmware/ctrl/README.md:631` "Those standalone builders ..." is unchanged at the candidate. The exact fix is R923-3's: "The standalone builders (`ctrl_runs.py`: every builder but the owned image builders) run in `firmware-boundary-capture`; `firmware-boundary` still runs its owned image builders, the stack gate and the controls, then judges the joined captures."
- **R924-3-R1 - RESIDUE (retained, PR body):** "the only job with a write token" should read "one of the two guarded jobs requesting actions: write".
- **S1-S7 (retained, optional):** not affected by the composition.
- **Comment rule:** the composition adds no line that neither side had, so it adds no new comment residue.

## 5. Per-lens results at `4f0d7a837512064d67f89938c32e4a064c39ed75`

```text
[R923] MINOR Conformance - scripts/suite_shards.py:108 vs receipts/hosted_measure.txt, receipts/probe_gptp_shadow_figure.txt - composed gptp_shadow figure 393 s vs 517-520 s window; #998 AC2's 1276 s deal fails its own selftest with the measured figure (C1)
[R923] MINOR Robustness - same artifacts - budget/timeout headroom of the worker carrying gptp_shadow is overstated in the composed tree (C1)
[R923] MINOR Tests - scripts/suite_shards.py --selftest (receipts/gate_suite_shards_selftest.log rc=0 vs probe rc=1) - the budget gate passes only on the source tree's figure (C1). Otherwise clean: gptp_shadow mutants 13/13 (receipts/gptp_shadow_mutants.log:52-53), lifecycle PASS (receipts/gptp_shadow_lifecycle.log:52), ci_events --selftest, mutant_stage --selftest, fw boundary leg 0 rc=0
[R923] PASS RTL - merge-tree recomputation (receipts/composition_overlap_check.txt) and gitlinks (receipts/restore_verify.txt) - the composition changes no hdl/ file beyond dev's side. The PR changes no RTL or gitlink. Gitlinks gptp-processor 1213ac5b, protocol-processor 801ef228, lwSRP d1bb4f4e, tsn-c-stack 715589c1, verilog-axis 48ff7a7e equal dev's. gptp_shadow's engine and generator controls build and are caught at the candidate
[R923] PASS Docs - sw/firmware/ctrl/README.md:129,629-632,649,651 against rtl-fast.yml:1226-1227,1344-1345,1482, ctrl_runs.py:71, ctrl_arms.py:438 and the lwSRP gitlink; docs_check, gen_toc --check/--verify-anchors, check_em_dash --base b127f378a and b0f2bc1a, check_doc_style, check_doc_paths, docs_inventory all rc=0 (receipts/gate_*.log). The README statements are true of the composed tree. R923-3-R1 RESIDUE is carried
```

## 6. Reviewer-owned completion ledger (composition)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (C1) | #998 AC2; `suite_shards.py:57,108,157`; `CI_WORKFLOWS.md:532-536,640-651`; 4 hosted worker logs; figure probe | R923-4 (source: R923-3, R924-3 at `b0f2bc1a`) | `4f0d7a837512064d67f89938c32e4a064c39ed75` |
| RTL | CLEAN | Merge-tree equality; gitlink set; dev-side gptp-processor targets staged and caught; PR has no RTL | R923-4 (source: R923-3, R924-3 at `b0f2bc1a`) | `4f0d7a837512064d67f89938c32e4a064c39ed75` |
| Robustness | UNCLEAN (C1) | Worker budget/timeout headroom; hosted worker walls; staging and cancellation paths in the lifecycle (PASS) | R923-4 (source: R923-3, R924-3 at `b0f2bc1a`) | `4f0d7a837512064d67f89938c32e4a064c39ed75` |
| Tests | UNCLEAN (C1) | gptp_shadow mutants 13/13; lifecycle PASS; `suite_shards --selftest` vs probe; `ci_events --selftest`; `mutant_stage --selftest`; fw boundary leg 0 | R923-4 (source: R923-3, R924-3 at `b0f2bc1a`) | `4f0d7a837512064d67f89938c32e4a064c39ed75` |
| Docs | CLEAN (R923-3-R1 RESIDUE carried) | Composed `ctrl/README.md` statements vs workflow, `ctrl_runs`, `ctrl_arms`, gitlink; doc gates | R923-4 (source: R923-3, R924-3 at `b0f2bc1a`) | `4f0d7a837512064d67f89938c32e4a064c39ed75` |

Lenses the composition does not touch, beyond the items above, keep their source coverage from R923-3 (`[R923] POSITIVE`) and R924-3 (`[R924] POSITIVE`), both at `b0f2bc1a784d9f006204491c883ac2b1783e970a`.

## 7. Real limits

- **Firmware boundary:** leg 1 (`test_ctrl_memory.py` needs `migen`) and the joined `firmware-boundary` judge over both captures were not run locally. Leg 0, which holds every dev-side firmware change, passed. Hosted `firmware-boundary` on the composed tree is owned by the manager.
- **Local timing:** wall times here were taken at host load near 95 on 32 CPUs and are not hosted figures. C1 rests on hosted windows only.
- **Mutant reruns:** an early attempt ran the mutant campaign twice concurrently, which garbled one log, and one foreground rerun hit my 595 s timeout after 6 of 13 controls. The published receipt comes from a single complete run (rc=0, 921 s).
- **Not run:** full parent, PP, gPTP, Yosys and builder banks; Docker/act; hardware. Physical calibration was NOT RUN, and field skips are not hardware proof. No manager source bank is claimed.

## 8. Pending manager duties

- **C1:** decide or route it, either with a figure, re-deal and derivation, or with a recorded acceptance, before the merge turn.
- **Residues:** carry R923-3-R1 and R924-3-R1 to the residue checklist. Optionally route O1 to the lwSRP pin lane, and O2 to #1008.
- **Current-dev candidate:** build and validate it at the merge turn (source base `b127f378a48adaa404d5a1f74ee352df2c8b532c`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`), including hosted and act acceptance and the joined firmware-boundary judge.

## 9. Reproduction

- `hosted_gptp_shadow_window.sh RUN_ID OUTDIR` is read-only. It finds the Verilator worker that ran gptp_shadow and prints its result lines. Measure the saved log with `python3 scripts/suite_shards.py --measure LOG`.
- `probe_gptp_shadow_figure.sh CHECKOUT SECONDS` is a disposable figure probe that restores the tracked bytes.
- After the probes, the clone was restored and verified:
  - HEAD `4f0d7a83`, and the worktree and index equal HEAD.
  - `write-tree` gives `9bc16d51`.
  - All five gitlinks match, and the submodules and superproject are clean, with no untracked or ignored entries (`receipts/restore_verify.txt`).

R923-4 FINISHED
