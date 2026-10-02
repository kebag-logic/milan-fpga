[R441] POSITIVE - exact head 7d9fabf13ea3ef08d7d204c0297820561054b04a

# R441-1 external independent review: issue #143 / PR #146

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `7d9fabf13ea3ef08d7d204c0297820561054b04a`, tree `739f75ea8d7bbebed4c78478c9f624803f3816a2` (verified in the review clone)
- Reviewed range: `88969246cbb82bf9d4975496f93a5420bbe3aa21..7d9fabf1`. These are the author's two commits, `85da751` (the drivers and the helper) and `ab8a50b` (the READMEs), made on `main` `631eeb34`, followed by the manager's `--no-ff` merge of `main` `88969246` (PR #144, C8).
- Round: R441-1, from a cleared context. The reviewer's own runs, scripts and receipts are in this packet. Every listed receipt is hashed in `MANIFEST.sha256`.

## Verdict

**POSITIVE.** All six acceptance items of #143, and its out-of-scope rule, hold at the exact head:

1. Each of the eight drivers takes `--jobs N` with d3's meaning and default, through `tb/common/mutant_pool.py`.
2. Every unit builds in a private copy, and no shared path was found.
3. `--only` and `--jobs` combine.
4. Results did not depend on N in any driver run at both N here: four full drivers (retry, srp_admission, maap, adp) and three subsets (dispatch, gsi, aecp). The summaries come out in declared order.
5. No mutant, control, patch or recorded count changed.
6. `hdl.yml` is unchanged, and its default of 4 fits the hosted runner.
7. Each README states the option and both wall times.
8. The merge keeps both sides of `tb/pp_top/README.md`.

No BLOCKER, MAJOR, MINOR or RESIDUE finding is open. Two SUGGESTIONs are recorded. Neither blocks the merge.

## Reconstruction (in the required order)

1. **Governance.** The tree has no `AGENTS.md` or `CONTRIBUTING.md`. I read `docs/README.md`, the root `README.md` and `.gitignore`.
2. **Scope.** I read the issue #143 body (acceptance 1-6; out of scope: changing any mutant, control or recorded count) and the lane assignment, comment 5958637229. The assignment gives d3's default, shared code allowed, no count change, CI N passed only where needed, and a STOP on any RTL, test-arm, count or parent-visible change. I also read TAKEN (5958642683), REVIEW READY at `ab8a50be` (5962222796), the PR #146 body with the manager's merge note, and the two review-start comments.
3. **Authorities.**
   - `tb/pp_top/d3_mutants.py` defines the meaning of `--jobs`: `type=int`, default 4, a `ThreadPoolExecutor(max(1, N))`, each mutant in its own `tempfile.TemporaryDirectory` copy (`:497-502`, `:517`, `:547`, `:564`).
   - `.github/workflows/hdl.yml` runs five of the campaigns through their make targets with no `--jobs`.
   - Each driver's README holds its recorded counts.
4. **Diff and history.** I read `git diff 88969246..7d9fabf1` in full: 15 files, the eight drivers, the helper and six READMEs. I read the merge parents (`ab8a50be`, `88969246`) and the merge base `631eeb34`.
5. **Public evidence.**
   - `kebag-logic/milan-fpga@e87e0642:review-evidence/pp143-r1`, as published: `MANIFEST.json`, `author/HANDOFF.md`, `author/PR-BODY.md` and `author/parent-adoption-c4c6-ea3fb388.patch`. That tree holds only the author packet. The manager's bank results are taken as stated in the review assignment and were not re-run.
   - The exact-head hosted check runs, queried read-only.

## Acceptance, item by item

| # | #143 acceptance | Result at `7d9fabf1` | Evidence |
|---|---|---|---|
| 1 | `--jobs N`, d3's meaning and default; each worker in its own copy and `obj_dir` | Holds | All eight `--help` texts print `--jobs JOBS units built and run at once, each in its own copy (default 4)` (`receipts/cli-checks.txt`). `mutant_pool.py:22,27,41` gives `DEFAULT_JOBS = 4`, `type=int` and `ThreadPoolExecutor(max(1, jobs))`. The helper's contract was probed with 5 unit tests, all OK (`receipts/test-mutant-pool.txt`): peak concurrency equals N, `--jobs 0` and `--jobs -2` give 1 worker, results come back in declared order whatever order they finish in, a unit's exception is raised at its turn and the rest are cancelled, and an early return cancels the remaining units and waits for the running ones. Isolation was checked against the trees, the trace and a poisoned ROM image; see "Shared-path hunt" below. |
| 2 | `--only` and `--jobs` combine | Holds | **gsi** `--only` with 4 names given out of declared order, at `--jobs 1` and `--jobs 8`: exactly golden, the 4 named variants in declared order, and restored (`receipts/gsi-sub-j8/stdout.txt`). The 13 receipts are identical, and `results.json` is byte-identical across N. **srp_admission** `--only pending-absent --jobs 8`: exactly the 3 controls and that mutant's 3 runs (6 checks). Every receipt equals the full run's in its FAIL lines and tally. **dispatch** and **aecp** comma lists of 8 and 7 arms ran at both N and were selected exactly. Unknown names are refused with rc 2 by gsi, srp_admission, maap and retry. |
| 3 | Results independent of N; README records both wall times | Holds | See the table below. Every pair matched on the summary (line for line), the receipt names, and every receipt's FAIL lines and tally lines. `results.json` and `coverage.txt` were byte-identical where the driver writes them. All eight READMEs record both wall times. |
| 4 | Summary in declared order | Holds | Every summary pair is identical line for line, including runs where units finish out of order (for example, srp_admission's 991k-check `admission-8` runs beside its 12k-check `admission-2`). A disposable probe changed only `in_order` to yield in completion order (`receipts/probe-order.diff`). It produced `6 checks: 4 PASS, 2 FAIL` and attached the `admission-8` verdicts to the wrong rows (`receipts/probe-order/stdout.txt`). Declared order is what makes each verdict correct, not just a matter of presentation, and the head has it right. |
| 5 | CI passes at the hosted runner's core count; N passed only where needed | Holds (the hosted run is still finishing; the manager owns it) | `hdl.yml` is unchanged in `88969246..7d9fabf1` and in `631eeb34..ab8a50b` (`receipts/scope.txt`). The repository is public, so `ubuntu-latest` is 4 vCPU / 16 GB, and the default `--jobs 4` matches it. At the time of writing, the two exact-head `hdl` runs (push 37070750896, pull_request 37070771201) show `docs-gates` and `portability` as success. Their `suites` jobs show these steps as success: lint plus every suite, the SRP LeaveAll campaign (31.8 min, against 40-42 min serial on `main` runs 37046526362 and 37056436937), MAAP (3.6 min, against 5.1-5.3 min) and ADP (7.9 min, against 8.6-9.2 min). The AECP, AECP-dispatch, matrix and nvm_port steps were still running. |
| 6 | `tb/pp_top/README.md` and the other campaign READMEs state the option | Holds | The option is stated for retry, adp, maap, gsi, aecp, dispatch, srp_admission and srp_top, and for notify (whose default is 1, matching `notify_mutants.py:334`). Merge check: `git merge-tree --write-tree ab8a50b 88969246` recomputes `739f75ea`, exactly the head tree. All 7 lines `main` added to `tb/pp_top/README.md` and all 42 lines the lane added are present at the head (`receipts/merge-readme.txt`). |
| - | Out of scope: no mutant, control or recorded count change | Holds | I wrote my own syntax-tree comparison of the eight drivers (`scripts/ast_tables.py`). Against both `631eeb34` and `88969246`, every module constant compares the same: `MUTANTS`, `MUTATIONS`, `EQUIVALENT_MUTATIONS`, `PERFORMANCE_MUTATIONS`, `REMOVED_EQUIVALENTS`, `SUITES`, `TREES`, `GENERATED`, `COMPLETE`, `PATCHES`, `ADMISSION` and the rest. gsi's `mutations()` and every judging function (`judge`, `run`, `run_case`, `run_suite`, `tally`, `completed`, `failures_of`, `build_tree`) are also the same, docstrings excluded. Only two constants are new: `RTL` in retry and the `Variant` type alias in gsi. Only `plant` changed in five drivers, by dropping the restore copy that a fresh copy makes redundant. `hdl/`, every `mutations/` and `aecp_dispatch_mutations/` patch, `scripts/` and `.github/` are untouched. Recorded counts reproduced (`receipts/*-readme-counts.txt`): retry 62 of 62 kill counts plus 7 equivalence and 1 performance controls; maap 29 of 29 "N FAIL of M"; adp 30 of 30; srp_admission 9 of 9 mutant counts; dispatch 8 of 8 sampled arms; aecp 7 of 7 sampled arms. |

### N-independence runs (reviewer-run, Verilator 5.050)

Each run was pinned with `taskset` to its own CPUs. `TMPDIR` was private to each run (`scratch/tmp-<run>`), and the pinned Verilator was first on `PATH`. Wall times are reviewer-host figures under concurrent load, not README figures.

| Driver | Units | `--jobs 1` (CPUs, s) | `--jobs 8` (CPUs, s) | Summary | Receipts | FAIL lines compared | Result |
|---|---|---|---|---|---|---:|---|
| retry (full) | baseline, 70, restored | 2, 692 | 3, 420 | 71 lines, identical | 73 = 73, `coverage.txt` byte-identical | 2,640 | MATCH |
| srp_admission (full) | 4 variants x 3 suites | 2, 981 | 3, 401 | 13, identical | 12 = 12 | 8,358 | MATCH |
| maap (full) | 3 controls, 29 arm runs | 2, 406 | 4, 226 | 101, identical | 32 = 32 | 189 | MATCH |
| adp (full) | 2 controls, 30 arms | 2, 649 | 2, 660 | 211, identical | 32 = 32 | 178 | MATCH |
| dispatch (`--only`, 8 arms incl. 4 microcode) | 4 controls, 8 arms | 2, 552 | 2, 594 | 81, identical | 13 = 13, `results.json` byte-identical | 70 | MATCH |
| gsi (`--only`, 4 variants) | golden, 4, restored | 2, 425 | 4, 224 | 7, identical | 13 = 13, `results.json` byte-identical | 1,792 | MATCH |
| aecp (`--only`, 7 arms incl. 2 microcode) | 5 controls, 7 arms | 2, 439 | 2, 464 | 136, identical | 12 = 12 | 123 | MATCH |
| srp_top (full, `--jobs 8` only) | 11 controls, 78 arm runs | - | 8, 620 | `90 checks: 90 PASS, 0 FAIL`, coverage 65/65, 11 controls and 78 KILLED in declared order | 84 | - | at README totals |
| maap (full, `--jobs 8`, traced) | as above | - | 4, 198 | identical to the untraced `--jobs 8` run | 32 = 32 | 189 | MATCH |

The FAIL-line totals for retry (2,640), srp_admission (8,358), maap (189) and adp (178) equal the figures in the PR body. Run `strace-maap` was an earlier traced run whose trace was superseded by `strace2-maap`; its summary also matches.

### Shared-path hunt (acceptance 1)

- **Code reading.** Every worker creates its own `tempfile.TemporaryDirectory` and copies `hdl/` plus the suites it needs into it. It plants the change there, builds there with relative `../../hdl` paths, and writes a single log whose name is unique per unit (`control-<pair>`, `<arm>`, `<label>-<suite>`, `<name>-build/-run`). Every table key is unique, except srp_top's five labels that run on two suites. For those, the worker returns its receipt text and the main thread writes it in declared order (`tb/srp_top/mutants.py:130-147,155-168`). All printing happens in the main thread. Generated ROMs: the copies skip `*.hex` and `obj*` or `obj_*`, and dispatch also deletes `GENERATED` before each build (`aecp_dispatch_mutants.py:137,146-149`). The pp_top `fixture_guards.py` already uses its own `TemporaryDirectory`. No Makefile names a fixed temporary path that a worker uses: the `MUTANT_OUTPUT ?= /tmp/...` defaults apply only to whole campaigns started through make.
- **Trees watched at `--jobs 8`.** A 5 s monitor listed every live copy, its `obj*` directories and its `*.hex` files for every run (`receipts/monitor-phase*.log`, `.dirs`). Each unit had its own randomly named copy: 12 for each dispatch run, 6 for srp_admission `--only`, and so on.
- **Syscall trace.** maap `--jobs 8` (3 controls and 29 arm runs on maap, rx_validator and pp_top) ran under per-process `strace -ff -y`, with each process's working directory followed through clone and chdir (`scripts/strace_writes.py`, `receipts/strace-maap-writes.txt`). Across 1,527 traced processes, every write landed in one of these places:
  - the 32 unit copies;
  - 272 compiler `mkstemp` temporaries and 32 per-make jobserver FIFOs, all randomly or PID named;
  - one Python `tempfile` probe, opened `O_EXCL` and unlinked at once;
  - the output directory, where each of the 32 logs was opened for writing exactly once;
  - `/dev/null`.

  Nothing was written in the review clone, and no other path was written.
- **Poisoned ROM probe.** In a disposable `git archive` copy, a garbage `ucode.hex` and `ltn_rom.hex`, newer than their generators, were planted in `tb/ucpu` and `tb/pp_top`. A direct `make run` in the poisoned `tb/ucpu` failed (`429 checks: 148 PASS, 281 FAIL`, rc 2), which proves the poison is live. `aecp_mutants.py --only ucpu-preempt-repeats,dl-preempt-after-effect --jobs 2` in that same copy still passed its control and killed both arms at their README counts, 18 and 4 (`receipts/probe-hex/`). This confirms that removing `forget_generated_roms` is safe: a copy never carries a ROM image.
- **Source checkout.** Before the runs, `git status --porcelain --ignored` was empty. During the runs the only change was the ignored `tb/common/__pycache__/`. The driver process writes it once, when it imports the helper; the workers are threads of that process, and every copy skips `__pycache__`. It was removed afterwards (`receipts/clone-restore.txt`).

### Memory (the author's 12 GB note)

- The run unit's cgroup cap is 12 GiB. Peak anonymous memory per phase: 5.65 GB with dispatch `--jobs 8` on 2 CPUs; 8.49 GB with adp `--jobs 8` on 2 CPUs beside adp `--jobs 1`; 11.64 GB with gsi `--jobs 8` on 4 CPUs beside gsi `--jobs 1` and srp_top `--jobs 8` on 8 CPUs.
- The cgroup reached its cap, including page cache, 3,146 times and swapped up to 128 MB. There were no OOM kills, and every verdict matched.
- Memory grows with N times each build's compiler threads, because every copy's Verilator `-j 0` uses all the CPUs it may run on. This confirms the author's note, and it is SUGGESTION S1.

## Five lenses

- **Conformance: CLEAN.** The issue's acceptance list was checked item by item (table above). The assignment's STOP conditions are not met: no RTL, test-arm, count or parent-visible change. `85da751..ab8a50b` touches READMEs only, so the author's equivalence runs at `85da751` exercised the head's driver code. The 18 driver line references in the PR body match the head (`receipts/pr-body-line-refs.txt`).
- **RTL: CLEAN.** `hdl/`, every mutation patch and every planting rule (anchor counts, `git apply --check`) are unchanged. Each copy receives the same planted RTL or microcode as the old shared tree after its restore step. The microcode arms in dispatch (lk-*, pg-*) and aecp (`mvu-silent`, `dlkill-always-misbehaving`) were killed at their README counts while running concurrently with RTL arms.
- **Robustness: CLEAN.**
  - The helper's contract was probed: order, bounded concurrency, error at its turn, and cancellation on return or exception. Gating is kept: retry's baseline and gsi's golden run alone and first. adp, aecp, dispatch and srp_top return on a failed control, and the exit from the `with` block cancels the queued arms.
  - Isolation was confirmed by tree monitoring, the syscall trace and the poisoned-ROM probe. The declared-order read was shown to be essential to correctness by the order-mutation probe.
  - SUGGESTION S1 covers the memory scaling.
- **Tests: CLEAN.** I ran seven drivers at `--jobs 1` and `--jobs 8`: four in full and three as `--only` subsets. srp_top ran in full at `--jobs 8`. Every pair matched. Recorded counts were reproduced for six drivers. Hosted CI at the head was green on every step that had completed by the time of writing. Limits are listed below.
- **Docs: CLEAN.**
  - The eight README passages state `--jobs N` (default 4, d3's meaning) and the declared order, and record both wall times. The pp_top README also states notify's default of 1.
  - The merge keeps both sides of `tb/pp_top/README.md`.
  - The new sentences about private copies, the `restored` copy, and the later srp_top receipt winning match the code.
  - The one stale figure I found predates the lane (S2).

## Findings

No BLOCKER, MAJOR, MINOR or RESIDUE finding.

**S1 - SUGGESTION (Robustness, Docs): memory scales as N times per-build compiler threads**

- **Where:** `tb/common/mutant_pool.py:41`, together with every suite Makefile's `--build -j 0`. srp_admission's Makefile uses `-j 8`.
- **Evidence:** Each of the N copies runs a Verilator build that uses every CPU it may run on. gsi's `--jobs 8` on 4 CPUs, beside two lighter campaigns, reached 11.64 GB of anonymous memory under a 12 GiB cap (`receipts/monitor-phase5.log`). The author independently reports reaching the cap with eight pp_top builds at full width.
- **Impact:** None in CI. There, 4 workers on 4 vCPU use about 6 GB of 16 GB, and N is the default. A developer who runs `--jobs 8` unpinned on a large host can exhaust memory. This is the same behaviour as d3's pool, and #143 asks for d3's meaning, so it is not a defect of this lane.
- **Suggested outcome:** a follow-up could add one sentence per campaign README on the memory per pp_top worker. Alternatively, it could pass a per-copy Verilator thread count such as `cpus // N`.
- **Verification:** none needed for this PR.

**S2 - SUGGESTION (Docs; predates the lane, not attributable to #146): stale control figure in srp_admission's README**

- **Where:** `tb/srp_admission/README.md:94-95`, "the controls pass (12615 checks at two sources, 991231 at eight, 1527 in srp_top)", dated 2026-09-24.
- **Evidence:** The srp_top control now prints `2200 checks: 2200 PASS, 0 FAIL` at both N. The other two control figures and all nine mutant counts match. The lane changed no suite, so the figure was already stale at `631eeb34`. The author's handoff records the same observation.
- **Impact:** A stale measured figure in prose. #143 forbids changing recorded counts, so fixing it here would be out of scope.
- **Suggested outcome:** a follow-up issue re-measures and restates the srp_top control figure.
- **Verification:** run `python3 tb/srp_admission/mutants.py --output DIR` and read `control-srp-top.log`.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #143 body and acceptance; assignment 5958637229; the PR #146 body (claims, line references, figures); d3's `--jobs` reference; `receipts/scope.txt`, `ast-tables-*.txt`, `pr-body-line-refs.txt` | R441-1 | `7d9fabf13ea3ef08d7d204c0297820561054b04a` |
| RTL | CLEAN | `hdl/`, `tb/*/mutations/`, `tb/pp_top/aecp_dispatch_mutations/` (unchanged); `plant` and anchor logic in all eight drivers; microcode arms run concurrently with RTL arms (dispatch and aecp subsets); poisoned-ROM probe | R441-1 | `7d9fabf13ea3ef08d7d204c0297820561054b04a` |
| Robustness | CLEAN | `tb/common/mutant_pool.py`; the worker and consumer of each of the eight drivers; `scripts/test_mutant_pool.py` (5/5); `strace-maap-writes.txt`; `monitor-phase1..9`; `probe-order`; `probe-hex`; `cli-checks.txt` | R441-1 | `7d9fabf13ea3ef08d7d204c0297820561054b04a` |
| Tests | CLEAN | 20 reviewer runs (table above; `receipts/<run>/`); `compare-*.txt`; `*-readme-counts.txt`; exact-head hosted check runs, step states as of writing | R441-1 | `7d9fabf13ea3ef08d7d204c0297820561054b04a` |
| Docs | CLEAN | READMEs of acmp_talker, adp_engine, maap, pp_top (gsi, aecp, dispatch, notify), srp_admission and srp_top; `merge-readme.txt`; other references to the drivers in `docs/` and the tb READMEs (no stale serial wording) | R441-1 | `7d9fabf13ea3ef08d7d204c0297820561054b04a` |

## Prior public review findings

This is review round 1. No earlier review round on PR #146 or issue #143 published findings. The only earlier public comments are lane administration (TAKEN, REVIEW READY, the merge note) and the two review-start notices. Nothing to resolve or retain. A same-round internal review report (R440-1, posted 2026-10-02T23:14Z) is not a prior-round review. This review was formed without it and did not read it.

## Real limits

- **Not run at both N here.** aecp (55 arms), dispatch (37) and gsi (20) were not run in full at `--jobs 1` and `--jobs 8`: only `--only` subsets of 7, 8 and 4 were. srp_top was run at `--jobs 8` only, and checked against its README totals, not against a `--jobs 1` run. For these, full-campaign N-independence rests on the author's published runs, which this review did not re-execute. The PR body's figures for the four full drivers I did run match mine exactly.
- **Syscall tracing.** Only maap (which covers maap, rx_validator and pp_top builds) was traced. The other drivers' isolation was checked by code reading and tree monitoring.
- **Wall times.** The wall times in this report were measured under concurrent load on a host shared with other work. They neither confirm nor refute the README wall times, which were taken on 4 pinned CPUs.
- **Not run by this reviewer.** The full suite sweep, `lint_hdl.sh`, the docs gates, Yosys portability, d3, acmp and notify campaigns, the parent consumer set and the donor bank were not run (not allowed or not assigned).
- **Hosted CI.** Observed read-only. The AECP, AECP-dispatch, matrix and nvm_port steps of both exact-head `suites` jobs were still in progress when this report was written.
- **Calibration.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Gitlinks.** The processor repository has no gitlinks (0 entries of mode 160000), so no submodule pin applied to the restore check.

## Restore

The clone is at the exact head (`receipts/clone-restore.txt`):

- `git status --porcelain --ignored` is empty;
- `diff-index HEAD` is clean;
- the index equals the head tree in mode, blob and path for all 479 entries (465 of mode 100644, 14 of mode 100755);
- rehashing all 479 worktree files gives 0 mismatches;
- there are 0 gitlinks.

All probes ran in disposable `git archive` copies under `scratch/`.

## Pending manager duties

- Hosted and act acceptance at the exact head: confirm that the `suites` jobs of runs 37070750896 and 37070771201 conclude success, including the AECP and AECP-dispatch campaigns at the default `--jobs 4`.
- The donor bank (9) and the parent consumer set (16) at this head, with `parent-adoption-c4c6-ea3fb388.patch` at milan-fpga dev `cdf49d1a`.
- The final current-dev candidate at the merge turn (source base `88969246`, live dev `cdf49d1a28527562888f0a903de51b6b15b1244f`). Source validation here does not cover it.
- The second independent review (R440-1) and the full completion bar before merge.
- Optionally, follow-up issues for S1 and S2.

R441-1 FINISHED
