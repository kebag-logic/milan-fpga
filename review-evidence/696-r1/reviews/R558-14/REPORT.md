[R558] POSITIVE - exact head e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd

# R558-14 - issue #696 / PR #706 - delta review of the merge of PR #705's head `d40e4e98`

Internal independent review, cleared context. Exact head `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd`, tree `295aadcc963e941f2fcc97b27d497aa787da0d86`. Ordered parents: `313616d1a18549d41907db389d378f0beb9bc543` (696 lane, POSITIVE in R558-13 and R559-10) and `d40e4e9827be2516f8f34b9d65f0a483fff2194c` (PR #705 / 697c head). Merge base `e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c`.

Scope, per the round-14 assignment (issue #696 comment 6148294623): judge only the merge. 697c's own commits are reviewed on PR #705 and are not re-reviewed here.

**Summary.**

- The merge has one manual resolution, in `sw/firmware/ctrl/test/maap_differential.py`. It keeps both intents: 697c's shared stack pin and stack-built C core, and 696's Annex B RTL plant with its named rejection.
- Every other path equals a mechanical pick of the changed side, or git's own clean auto-merge (`sw/firmware/ctrl/maap/README.md`).
- No 696 or 697c file changed beyond the resolution. No RTL changed.
- On the merged tree, with the pinned simulator, these all pass:
  - the MAAP harness: 186 checks;
  - the MAAP campaign: 65 checks (63 rejected defects and 2 clean controls);
  - the integration: 5 checks;
  - the coverage: 225/225 lines;
  - the differential: 12 clean tests and 17/17 rejected defects;
  - 697c's boundary gate over the Verilator builders, the builders that run the differential: 0 findings, 0 misbehaved.
- Two run-time probes show the differential self-test fails if either side's intent is dropped from the resolution.
- The head stacks cleanly on the 697c merge-train candidate.
- No BLOCKER, MAJOR or MINOR. There are two new RESIDUE items (prose only) and one SUGGESTION.

## 1. Context reconstructed (in order)

- AGENTS.md and CONTRIBUTING.md: two positive reviews are needed, all five lenses must be covered at the exact head, and candidate-merge validation is the manager's.
- docs/README.md.
- Issue #696 body: acceptance 1-4 and M1-M8. Round rulings read: 6142198285 (dev merge), 6148294623 (round 14: merge `d40e4e98`, resolve `maap_differential.py` keeping both intents, list any other conflict, run the suites, update HANDOFF; no further dev merge; no 697c change beyond the resolution).
- Author REVIEW READY 6152831020.
- Authorities: `docs/design/MAAP_FABRIC.md` (unchanged), `sw/firmware/ctrl/maap/README.md`, `sw/firmware/ctrl/README.md`, and the PR #705 composition reference for candidate `7094848c` (tree `34b24fec`, PR #705 comments 6142825895 and 6149395907).
- Diff `c6bd08c6..e2cd089c` and the merge's three-way structure.
- Then the author's evidence at `217cf130:review-evidence/696-r1/author-r14`, and exact-head hosted runs.
- Prior public findings were read only after sections 2-7 were written (section 8).

## 2. Merge structure (independently reproduced)

| Check | Result | Receipt |
|---|---|---|
| `git merge-tree --write-tree 313616d1 d40e4e98` | Unresolved tree `63a94f32238ef4ec2319b3e545bcd418aa168d63`. Exactly one content conflict, in `maap_differential.py`. `sw/firmware/ctrl/maap/README.md` auto-merges cleanly | this table; equals the author's `merge-tree.log` |
| `git diff 63a94f32 295aadcc` | Only `sw/firmware/ctrl/test/maap_differential.py` differs (the manual resolution) | same |
| Per-path classification over all 1,328 paths, base/ours/theirs/result, mode and oid, gitlinks included | 1,236 equal on both sides, 15 ours-only, 75 theirs-only, all equal to the expected side. 2 changed on both sides: the README (git's clean auto-merge, blob `86ddf4a3`) and the differential (manual). **0 mismatches** | `receipts/merge_paths.txt`, `scripts/merge_paths.py` |
| RTL, synthesis, MAAP bench and design docs vs first parent | `git diff --stat 313616d1 e2cd089c -- hdl syn tb/verilator/maap docs/design/MAAP_FABRIC.md docs/design/AREA_BUDGET.md` is empty. The only `tb/` changes are 697c's `mbx` and `milan_dp` Makefiles, `mbx/README.md` and `stream_counter_f5.py` | `receipts/rtl_unchanged.txt` |
| Stacking on the 697c candidate | Candidate `7094848c` is not fetchable from the public remote ("not our ref"). I rebuilt its tree with `git merge-tree a0f39ad4 d40e4e98`, which gives `34b24fec86f5b1c43e6b4142f1c38facc5a72835`, equal to the tree R584 recorded for `7094848c`. I then made a local stand-in commit with the same tree and parents. `git merge-tree --write-tree <stand-in> e2cd089c` is **clean** (tree `8f36c903`). The stacked tree minus the candidate is exactly the 17 files of the 696 lane, and 16 of them are byte-equal to `e2cd089c`. The 17th, `docs/findings/README.md`, also carries dev `a0f39ad4`'s #730 row edit, which is a different table row | `receipts/stack_on_697c_candidate.txt` |

## 3. The resolution, hunk by hunk (`sw/firmware/ctrl/test/maap_differential.py` at the head)

| Line | 697c intent kept | 696 intent kept |
|---|---|---|
| :4-7, :17-19 | Module docstring on the shared pin check. Imports `STACK*`, `Refusal`, `stack_pin`, `MAAP_C` | none on this side |
| :23 | `stack: Path = STACK` | `rtl: Path \| None = None` |
| :26-27, :30 | `Tree(..., stack)`, `compile_c(... MAAP_C ...)`, `-I{stack / STACK_INCLUDE}` | none on this side |
| :32-38 | Objects before `-LDFLAGS` (static GoogleTest link order) | `str(rtl or ROOT / ".../KL_maap.sv")` |
| :50, :54-65 | `sensitivity(out, pinned=STACK)`, `m.path` and `MAAP_C` plant paths | none on this side |
| :71-73 | none on this side | `parent-ignores-mac` RTL plant (`station_mac_i[31:0] + realtime_ns_i` changed to `32'hAC61`) |
| :77-80, :82 | Per-case stack copy from the proven pin; plants under `STACK_PREFIX` go into the copy | none on this side |
| :81, :83-85 | none on this side | The RTL plant is written to `<case>/KL_maap.sv` from `ROOT / path` |
| :86-87 | The fixture uniqueness check is retained | same |
| :89 | Passes `stack` | Passes `source if is_rtl else None` |
| :90-92 | none on this side | Named needle `"MAC/phase sampling reaches the parent's "` for the RTL plant |
| :104-112, :116, :119 | `--stack`; `stack_pin` refusal (exit 2) before any build, in both modes | none on this side |

Only one line of either side was dropped: the `sensitivity` docstring. It now has 696's wording, "reject its named planted defect", without 697c's "planted in a copy of `pinned`" (SUGGESTION S1). No behaviour was lost.

## 4. Executed evidence at the exact head (this reviewer)

The simulator is the pinned Verilator 5.050: wrapper sha256 `905795b9...`, and the review wrappers exec the same `VERILATOR_ROOT` and binaries (`receipts/toolchain.txt`). The host's 5.052 was not used. Build trees and TMPDIR were in packet scratch, and jobs ran concurrently.

| Run | Command (from clone root) | Result | Receipt |
|---|---|---|---|
| MAAP harness and campaign | `make -j16 -C tb/verilator/maap MDIR=<scratch> all` | `KL_maap: 186 checks, 0 failures`; `== maap mutants: checks: 65 failures: 0 ==`, i.e. 63 rejected defects and 2 clean controls; rc 0. The total of 251 equals round 13 | `logs/maap-all.log`, `.rc` |
| Integration | `make ... integration-build DP_MDIR=<scratch>` then `./maap_integration` | `MAAP integration: 5 checks, 0 failures`; rc 0 | `logs/integration.log`, `.rc` |
| Coverage | `make ... coverage COV_MDIR=<scratch>` | `KL_maap.sv line 100.0% (225/225) PASS`; rc 0 | `logs/coverage.log`, `.rc` |
| Differential | `python3 sw/firmware/ctrl/test/maap_differential.py --self-test --keep <scratch>` | `tsn-c-stack at 405dc683...`. Clean run `PASS (12 tests, 0 failures)`. `differential mutants: 17/17 caught`, including `parent-ignores-mac`; rc 0 | `logs/differential.excerpt.log`, `.rc`; full-log hash in `logs/RAW-LOG-INDEX.txt` |
| Pin refusal, both modes | `scripts/pin_probe.sh` with `VERILATOR=false`, on a clone of the pinned stack | Pinned clone: accepted, reaching the (failing) build, default and `--self-test`. `src/maap.c` edited: `REFUSED: tsn-c-stack differs from the pinned 405dc683: src/maap.c`, exit 2, **no build directory created**, both modes. After restore: accepted | `receipts/pin_probe.txt` |
| Resolution probe: 696 intent dropped | `scripts/resolution_probe.py <repo> drop-rtl` (`differential()` ignores `rtl` at run time; no file edited) | `16/17 caught`; escaped exactly `parent-ignores-mac`; self-test rc 1, i.e. **detected** | `logs/probe-drop-rtl.log` |
| Resolution probe: 697c intent dropped | `... drop-stack` (builds the pinned submodule instead of the per-case stack copy) | `3/17 caught`; escaped exactly the 14 C-core plants (wire, release, 9 Table B.7 cells, 3 probe-interval); rc 1, i.e. **detected** | `logs/probe-drop-stack.log` |
| 697c boundary gate over the Verilator builders | `ctrl_boundary.py --require-rv32 --selftest --only verilator` (the hosted `firmware-verilator` command), with the RV32 SDK whose archive sha256 equals the repository pin | Captures `maap_differential.py --self-test: exit 0 (183 s)` and `make -C tb/verilator/mbx: exit 0`. Pin controls for the differential and its self-test refuse the edited core. The `maap_r584.h` plant is caught. `0 finding(s), 6 boundary, 120 pin and 4 figure controls, 0 misbehaved`; `ctrl_boundary: PASS`; rc 0 | `logs/boundary-verilator.log`, `.rc` |
| Pin prerequisites the merge brings into 696's benches | `make -C tb/verilator/{milan_dp,mbx} stack-pin` | `tsn-c-stack at 405dc683...`, rc 0 each | `receipts/stack_pin_targets.txt` |

Two earlier boundary attempts stopped on my environment, not on the source. The first used a shared clang-18 wrapper whose target is gone. The second ran before `third_party/lwSRP` was initialised (`REFUSED: lwSRP is not its own checkout`). Both are kept in `logs/boundary-attempts.txt`. The passing run used host clang 23.1.1; the stack's `check_boundary.py` has no compiler-version pin.

After the runs I removed my ignored build artifacts and checked the clone at the exact head (`receipts/restore_verification.txt`):

- index equal to the HEAD tree, as (mode, blob, path) for 1,317 entries;
- worktree equal to HEAD;
- zero status entries, including ignored files and submodules;
- every initialised gitlink checked out at its recorded commit and clean.

## 5. Hosted CI at `e2cd089c` (read by this reviewer, `receipts/hosted_checks_e2cd089c.tsv`, `receipts/hosted_job_steps.txt`)

- **Executed and succeeded at head `e2cd089c`:**
  - Workflow jobs: `changes`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`, `verilator-lint`, `publication-census`, `full-ci-gate`, `yosys-elaboration`.
  - Firmware jobs: `firmware-unit`, `firmware-boundary`, `firmware-verilator`, `firmware-aecp-mutants`, `firmware-control-mutants`, `firmware-srp-mutants`.
  - Shards: `Yosys shard 0-3/4`.
  - Aggregate: `rtl-fast`.
- **Gates verified as executed:** the steps of `firmware-verilator` (step 10, "Hold the TSN stack boundary over the Verilator builders' compiles"), `firmware-boundary` and `firmware-unit` ran with `success`; none of these gate steps was skipped.
- **Skipped context:** `Physical gPTP (nightly and manual)`. This is not hardware evidence.
- **Still in progress at 2026-10-13T21:21+02:00:** `Verilator shard 0-4/5`, `elaborate`, `docs-check`. I claim no result for these.

## 6. Findings of this round

### R558-14-R1 - RESIDUE - Docs - PR #706 body `:17-18`, `:102`, `:176` - stale publication wording

- **Evidence:** the PR's `headRefOid` is `e2cd089c...`, and hosted runs execute at it. The body still says:
  - `:17-18`: "Local head: `e2cd089c...`. The published PR #706 head remains `313616d1...` until the manager publishes this merge.";
  - `:102`: "After the manager publishes this head:";
  - `:176`: "Independent review of this head, publication, hosted acceptance and workflow replication remain manager duties."
- **Why RESIDUE:** this is PR-body wording only. No measurement, figure, verdict, test, code, generated artifact, conformance or clause claim, or privacy rule changes.
- **Exact fix:**
  - `:17-18`: "Head: `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd`, published as the PR #706 head."
  - `:102`: "To check out this head:"
  - `:176`: "Independent review of this head, hosted acceptance and workflow replication remain manager duties."
- **Verification:** reread the body against the PR head.
- This supersedes R558-13-R1 and R559-10-R1; their strings are gone and this is their successor.

### R558-14-R2 - RESIDUE - Docs - `review-evidence/696-r1/author-r14/HANDOFF.md:70-73` - three resolution line pointers miss their lines

- **Evidence:** at the head, `maap_differential.py:75` is the loop header; the stack copy is `:77-80`. `:80` is the stack `copytree`; the RTL plant's source selection is `:81-85`. `:107` is `args.stack.resolve()`; the pin proof is `:108-112`.
- **Why RESIDUE:** these are prose pointers in the author handoff only. Every claim they support holds at the corrected lines (section 3).
- **Exact fix:**
  - ":75 copies that stack" becomes ":77-80 copies that stack";
  - ":80 the RTL plant still selects its separate source" becomes ":81-85 ...";
  - ":107 both command modes run the shared pin proof" becomes ":108-112 ...".
- **Verification:** open the three ranges at `e2cd089c`.

### R558-14-S1 - SUGGESTION - Tests, Docs - `sw/firmware/ctrl/test/maap_differential.py:51` - docstring dropped 697c's location clause

The resolved docstring keeps 696's "reject its named planted defect" and drops 697c's "planted in a copy of `pinned`". It is still true. An optional combined form: "Require every differential case to reject its named planted defect: C plants in a copy of `pinned`, the RTL plant in a copy of the parent source." This is optional and has no lens effect.

No BLOCKER, MAJOR or MINOR.

## 7. Lens results (artifact-specific; evidence at `e2cd089c`)

```text
[R558] PASS Conformance - sw/firmware/ctrl/test/test_maap_differential.cpp (blob af9ae461, equal to first parent), hdl/ieee1722/maap/KL_maap.sv (blob 746be52d, equal to first parent), maap_differential.py:23-119 - the Annex B oracle (Table B.7 cells, B.2.1 CDL 16, B.3.4.2 strict 500/600 ms probe draws, MAC/phase draw coverage) runs unchanged against the stack-built C core and the unchanged parent RTL: 12/12 clean, 17/17 named rejections; MAAP harness 186/0, campaign 65/0, integration 5/0, coverage 225/225 on the merged tree; the assignment's deliverables 1-3 are met (resolution keeps both intents; only one conflict, the README auto-merge is listed by the author; suites re-run; HANDOFF:8 and :11 name the head and the #705 diff note); issue acceptance 1-3 artifacts are byte-identical to the R558-13 head; acceptance 4 (bench) remains separately assigned.
[R558] PASS RTL - receipts/rtl_unchanged.txt, receipts/merge_paths.txt - no file under hdl/ or syn/ and nothing in tb/verilator/maap changes in the merge; maap_differential.py:34-38 still elaborates KL_maap with -GCLK_FREQ_HZ_P=10000 from ROOT (or the per-case RTL plant), only the link order (objects before -LDFLAGS) moves; the merged tree stacks cleanly on the reconstructed 697c candidate tree 34b24fec with the 17 lane files carried; `make -C tb/verilator/{milan_dp,mbx} stack-pin` passes, so 697c's new prerequisites do not block 696's datapath benches.
[R558] PASS Robustness - maap_differential.py:77-89,104-112; receipts/pin_probe.txt; logs/boundary-verilator.log:196-197 - an edited stack is refused with exit 2 before any build in both modes; a restored clone is accepted; each plant goes into a per-case ctrl/stack/RTL copy (submodule and KL_maap.sv still clean and byte-equal after 17 + 34 planted builds: receipts/restore_verification.txt); the fixture-uniqueness refusal (:86-87) applies to C, test and RTL plants alike; a build failure never counts as a rejection (`caught` with needle, :90-92).
[R558] PASS Tests - logs/differential.excerpt.log, logs/probe-drop-rtl.log, logs/probe-drop-stack.log, logs/boundary-verilator.log, logs/maap-all.log - the differential self-test can fail for the resolution defects it guards: dropping 696's RTL forwarding escapes exactly parent-ignores-mac, and dropping 697c's stack forwarding escapes exactly the 14 C-core plants; the full self-test passes 17/17; 697c's boundary gate over the Verilator builders (which captures the differential self-test and the mbx bench) passes with 120 pin and 4 figure controls, 0 misbehaved; hosted firmware-verilator, firmware-boundary and firmware-unit executed and succeeded at e2cd089c.
[R558] PASS Docs - sw/firmware/ctrl/maap/README.md:183-184 and :204-207 (auto-merged: 697c's pin text and 696's 1,024-MAC sweep and draw-coverage account both present), sw/firmware/ctrl/README.md:279, docs/testing/CI_WORKFLOWS.md:97,107, author HANDOFF.md:8,11,68-76,285 (the round-14 record, the #705 diff note, and gate 11 NOT RUN), PR #706 body :47-55, :167 - the merge changes no doc beyond the auto-merged README; no doc states a differential mutant count that the 17th case would falsify (a search finds none); the PR body and HANDOFF state the historical-calibration limitation; the prose defects are R558-14-R1 and R558-14-R2 (RESIDUE, no lens effect).
```

## 8. Prior public findings at this head (read after sections 2-7)

| Finding | State at `e2cd089c` | Evidence |
|---|---|---|
| R558-13-R1 / R559-10-R1 (RESIDUE, PR body "unpublished" wording) | **Superseded** | Those strings are gone from the body; R558-14-R1 is their successor |
| R558-2-R1 / R559-2-R1 (RESIDUE, plan `:66`, `:317`, M0 row) and R558-5-R1 (RESIDUE, "records ... unchanged") | **Retained** | `MARK_II_AREA_PLAN.md` and `AREA_BUDGET.md` blobs are equal to `313616d1`, so the lines are unmoved |
| R558-11-F1, R558-9-F1, R558-5-F1 (MINOR) and their RESIDUEs | **Still resolved** | Their artifacts are byte-identical to `313616d1` (`receipts/merge_paths.txt`: ours-only paths equal the first parent) |
| R558-1-F1, R558-3-F1 = R559-3-F1 (BLOCKER), R558-6-F1, R558-7-F1, R559-1-F1/F2/F3, R559-6-F1/F2 | **Still resolved** | RTL, bench and differential test source are byte-identical to `313616d1`. Re-executed here: 186/0, 65/0, 5/0, 225/225, 12/0 and 17/17 |
| Earlier SUGGESTIONs (R558-3/4/6/7/8, R559-1/3/4/5/6/7) | **Retained, optional** | No lens effect |

None is treated as resolved by moving it to another issue.

## 9. Reviewer-owned coverage ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `test_maap_differential.cpp`, `KL_maap.sv` (blob identity), `maap_differential.py:23-119`; differential 12/0 and 17/17; MAAP 186/0, 65/0, 5/0, 225/225; round-14 assignment deliverables; issue acceptance 1-3 artifacts | R558-14 | `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd` |
| RTL | CLEAN | `merge_paths.txt` (0 mismatches), `rtl_unchanged.txt`, `maap_differential.py:34-38`, stacking on the candidate tree `34b24fec`, `stack-pin` targets | R558-14 | `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd` |
| Robustness | CLEAN | `maap_differential.py:77-112`; pin probe in both modes; per-case plant isolation; restore verification; boundary pin controls | R558-14 | `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd` |
| Tests | CLEAN (S1 optional) | differential self-test; drop-rtl and drop-stack resolution probes; boundary gate over the Verilator builders; MAAP campaign; executed hosted firmware jobs | R558-14 | `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd` |
| Docs | CLEAN (RESIDUE R558-14-R1 and R2, plus retained R558-2-R1 / R559-2-R1 and R558-5-R1, for the residue checklist) | MAAP README auto-merge, ctrl README, CI_WORKFLOWS, author HANDOFF round 14, PR #706 body | R558-14 | `e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd` |

## 10. Real limits

These are source-head checks by this reviewer. They are not a manager source bank and not the final current-dev candidate.

- **Suites relied on, not re-run.** I did not run the other six default suites (`milan_dp`, `mbx` with tallies, `pp_shadow`, `capture_coherence`, `milan_dp_mclk`, `milan_dp_render`). I also did not run the firmware parent campaign (506), store, coverage ratchet, builder, portability, static bank, behaviour or resource recipes. For these I rely on the author's round-14 receipts and on the hosted jobs that executed. The merge changes no input of those suites except 697c's `stack-pin` prerequisites, which I ran. I spot-checked the author's `suite-comparison.json`: `maap` is 186 + 65, matching my run.
- **Hosted jobs still running.** `Verilator shard 0-4/5`, `elaborate` and `docs-check` were in progress when read, so no result is claimed for them.
- **697c candidate commit.** `7094848c` is not public. Stacking was shown against a local stand-in with the identical tree (`34b24fec`) and parents (`a0f39ad4`, `d40e4e98`).
- **Boundary gate scope.** I ran only the `--only verilator` scope. The firmware-builder scope (`--without verilator`) is evidenced by the hosted `firmware-boundary` job and the author's full run. My run used host clang 23.1.1.
- **Recorded limitations, restated.** Builder historical calibration gate 11 is NOT RUN (author's recorded limitation, stated in HANDOFF `:285` and PR body `:167`). Physical calibration is NOT RUN. Field skips and the skipped physical gPTP context are not hardware proof. No hardware was used.

## 11. Pending manager duties

- Publish this report.
- Obtain the second (external) exact-head review.
- Accept the exact-head hosted results (Verilator shards, `elaborate`, `docs-check`) and the local workflow replica.
- Keep the merge order: #705 before #706. Until #705 merges, PR #706's diff shows 697c's commits.
- Build and validate the final current-dev candidate at the merge turn (source base `c6bd08c6`, live dev `a0f39ad4`), with builder and native banks. Its `docs/findings/README.md` takes dev's #730 row edit beside this lane's row edit.
- Carry R558-14-R1, R558-14-R2 and the retained residues to the residue checklist.
- Run post-merge containment.

R558-14 FINISHED
