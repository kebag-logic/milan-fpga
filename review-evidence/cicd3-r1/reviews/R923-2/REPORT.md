[R923] NEGATIVE - exact head 9c62539365fea8316dae2b9fd7c68defeff5cb31

# R923-2: internal independent re-review of PR #1003 (Relates to #998)

- Round: R923-2, internal cleared-context review, the second round by this reviewer identity.
- Head: `9c62539365fea8316dae2b9fd7c68defeff5cb31`, tree `bbbe38c7db0b82682798e8afb1feb3a41a4ff491`.
- Source base: `fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f` (the head of #1001, since merged). Live `dev`: `e275d7950ef3385753e6a15d2e191ba855b171ed`.
- Delta judged: `13e6d869..9c625393`, six commits (`d95e95e8`, `59f4f478`, `45d5c35a`, `feb03206`, `96df313f`, `9c625393`), 21 files.
- Code outside the delta keeps its R923-1 lens verdict unless the delta changes what it depends on.

## Verdict

**NEGATIVE.** One MINOR finding is open (F1), and it is attributable to all five lenses.

- Every prior finding is resolved at this head: R924-1-F1, R923-1-F1, R923-1-F2, and the residues R924-1-R1 and R923-1-R1 to R3.
- The delta is otherwise sound:
  - The stage root is proved, and each slot is locked on its own inode.
  - No figure is lowered outside the split or re-keyed legs.
  - The five over-budget pieces are split.
  - The three `firmware-boundary` jobs carry the whole run's verdict.
  - Required contexts, cancellation and fork safety are unchanged.
  - At exact head, every job this PR touches ran within 30 minutes (Actions jobs API).
  - Acceptance 1's `milan_dp` gPTP difference comes from the base moving, as round 7 says.
- **F1:** follow_ring's two new fine-build recipe lines reach `$(MAKE)` only through a variable. So make no longer treats them as recursive.
  - `make -n run` is no longer the same as the base's, though the PR says it is.
  - Under a pipe-style jobserver, the serial `run` now prints a make warning that the base does not print. The serial suite output therefore changes.
  - The fix is one character per line.

## Findings

### R923-2-F1 - MINOR - Conformance, RTL (interface contract), Robustness, Tests, Docs - `tb/verilator/follow_ring/Makefile:129`, `:154` - the fine build is no longer a recursive make line, so `make -n run` changes and the serial run warns under a pipe jobserver

**Authority and evidence.**

- Issue #998 acceptance 1 requires byte-identical suite output against the base, host-dependent text excepted.
- The PR, Description item 7, says: "The serial `run` and every target's commands are unchanged (`make -n run` is the same)". How to validate lists `make -n -C tb/verilator/follow_ring run   # the serial run's commands, unchanged`.
- Base recipe (`13e6d869`): `small-pullin:` ran `$(MAKE) build CLK_HZ=25000000 FRAME_DIV=64 MDIR=…_fine`.
- Head recipes:
  - `:129`: `$(if $(LEG_BUILD),$(FINE_BUILD))`.
  - `:154` (`build-pullin-small`): `$(FINE_BUILD)`.
  - In both, `FINE_BUILD = $(MAKE) build …` (`:97`).
- GNU make marks a recipe line as recursive only when the line itself names `$(MAKE)` or `${MAKE}`, or starts with `+`. Neither head line does.
- `receipts/cases/follow_ring_make_probe.txt` (from `scripts/follow_ring_make_probe.sh`, GNU make 4.4.1, both trees extracted by `git archive`):
  - **`make -n run` DIFFERS.** The base recurses into the fine build and prints its `mkdir`, `dp_glue.py` and `verilator` lines. The head prints only `make build …` and does not recurse (`receipts/cases/make-n-run.{base,head}.txt`).
  - **Under `make -j4 --jobserver-style=pipe small-pullin`**, the head prints `make[1]: warning: jobserver unavailable: using -j1.  Add '+' to parent make rule.` The base prints nothing of the kind (`receipts/cases/small-pullin-pipe.{base,head}.txt`; warnings: base 0, head 1).
  - The serial `run` reaches this under a jobserver: `+$(MAKE) -j4 b8 pullin bind small-pullin settle-control` (`:92`).
- With make 4.4.1's default fifo jobserver, a real run's commands and output are the same as the base's. The only differences are traceback line numbers from the stub run.
- The CI pieces are not affected: they build under `MAKEFLAGS=-j1`, which has no jobserver.
- media_phase is not affected: its `make -n run` is byte-identical to the base's (`receipts/cases/media_phase-make-n-run.txt`).

**Impact.**

- On a host whose make uses a pipe jobserver, the serial follow_ring run prints an extra warning line in the suite log. GNU make 4.3 and earlier have only that kind; Ubuntu 24.04's make 4.3 is one example. The serial sweep there is no longer byte-identical to the base, and the fine build loses the jobserver.
- `make -n run` no longer shows the fine build's commands.
- The PR's stated validation for "the serial run is unchanged" is false as written.
- No verdict changes.

**Required outcome.**

- Make both lines recursive again, for example `+$(if $(LEG_BUILD),$(FINE_BUILD))` and `+$(FINE_BUILD)`, or name `$(MAKE)` in the line itself.
- Then the following must hold:
  - `make -n run` at the head equals the base's;
  - no jobserver warning under `--jobserver-style=pipe`;
  - `exec-pullin-small` (with `LEG_BUILD=` empty) still does not rebuild.
- Alternatively, keep the lines and state the make-version dependence. That would still leave acceptance 1's serial-output claim open on those hosts, so the code fix is preferred.

**Verification.** Run `sh scripts/follow_ring_make_probe.sh <repo> <out>` from this packet against the fixed tree, after adding the fixed commit to the script's head list. Expect `make -n run: IDENTICAL` and `head: jobserver warnings: 0`. Then run `make -s -C tb/verilator/follow_ring ci-list` and the `follow_ring__1` piece.

### RESIDUE (wording only; changes no figure, code, test or verdict)

- **R923-2-R1:** `docs/testing/CI_WORKFLOWS.md:649-650`.
  - Today: "Each new piece's figure, with the two local walls it scales by, is recorded on #998".
  - Problem: #998 has no comments (Issues API: 0). The derivation table is in PR #1003's description, item 8, "The new figures and their derivation". The figures themselves are in `scripts/suite_shards.py` `PIECE_SECONDS`.
  - Exact fix: replace "is recorded on #998" with "is in PR #1003's description (its derivation table)". Alternatively, post that table on #998 and keep the sentence.

### SUGGESTIONS (optional)

- **S1 (retained from R923-1-S1):** `scripts/ci_make_cases.py:151`. With `MILAN_COUNTER_FRAME_OUT` set, one worker runs a piece's cases in start order, not driver order. The final writer is unchanged today, as R923-1 showed. Either keep driver order in that case, or say in the comment that the serial order is the start order.
- **S2 (retained from R923-1-S2, now covering the new jobs too):** give `verilator-preflight` and `firmware-boundary-capture` a least-privilege `permissions: {contents: read}`.
  - They are fork-safe to the same degree as their siblings: no secret, no new token, `pull_request` only.
- **S3 (retained from R923-1-S3):** the preflight's "beside the workers" benefit holds only with free runners. At this head, 25 workers queued for 31 minutes (the PR's own note).
- **S4:** the PR's derivation table publishes walls to 0.1 s. For `milan_dp__1`, `1313 × 710.5 / 809.8` = 1152.00 rounds up to 1152, but the tree carries 1153 (`receipts/gates/figure-recompute.txt`).
  - The tree's figure is the ceiling of the unrounded walls, which is conservative, so this is not a defect.
  - Publishing the walls at full precision would make every row reproduce exactly.

## Prior public review findings on this PR

I read these only after my own pass over the delta.

| Finding | Status at `9c625393` | Evidence |
|---|---|---|
| R924-1-F1 MAJOR: in-tree staging erases a held slot across TMPDIRs | **RESOLVED** | The lock is an exclusive `flock` on the slot directory's inode, re-checked after locking (`scripts/mutant_stage.py:138-171`). The self-test control "two in-tree drivers under different TMPDIRs share one lock domain" uses independent processes (`:339-343`). My churn probe: 32 processes × 300 holds, in-tree and root, real and linked TMPDIR and parent spellings, 0 overlaps, and fallback exercised (`receipts/staging/stage_churn_probe32-9c625393.txt`). The foreign-uid control is at `:354-361`. The API is unchanged for the 38 callers. |
| R924-1-R1 RESIDUE: attribution in four comment blocks | **APPLIED** | `scripts/run_all_suites.sh:20`, `scripts/mutant_stage.py:5`, `scripts/ci_make_cases.py:79`, `scripts/ci_suite_workflows.py:82` |
| R923-1-F1 MINOR: stage root trusted without proof; lock keyed by an unresolved path | **RESOLVED** | `proved_root()` at `:88-125`: lstat type, owner, mode and the parent's sticky bit, then a re-check after open. My round-1 probes at head (`receipts/staging/stage_root_probe-9c625393.txt`): a world-writable root and a symlinked root are each refused with their reason and staged at a random private directory; a `locks` file no longer breaks staging; a fresh root is `0700`. `stage_alias_probe-9c625393.txt`: aliased TMPDIRs get distinct slots and the first holder's file survives. Self-test: all controls PASS (`selftest-9c625393.txt`). |
| R923-1-F2 MINOR: shard 1 took 38.6 min at `13e6d869` | **RESOLVED** under the manager's ruling | The bound applies to the jobs this PR touches. At exact head, Actions jobs API (`receipts/hosted/job-minutes-9c625393.txt`): slowest Verilator worker 27.7 min (1/26); preflight 1.9; `firmware-boundary-capture` 13.2 and 14.1; `firmware-boundary` 5.5; unions ≤ 0.6; `verilator-suites` 0.2. The untouched jobs over 30 minutes are tracked in #1008: `firmware-control-mutants` 38.8 and `publication-census` 37.2. The four "Fail fast across this head" watchers (64.7, 54.6, 38.3, 26.3) are #1008's documented exception. |
| R923-1-R1, R2 (wording) | **APPLIED** | `docs/testing/TESTING.md:174`, `docs/testing/CI_WORKFLOWS.md:510-512` |
| R923-1-R3 (PR body wording) | **APPLIED** | PR body item 3 |
| R923-1-S1 to S3 | Retained as S1 to S3 | — |

## Lens coverage at `9c62539365fea8316dae2b9fd7c68defeff5cb31`

Each lens is UNCLEAN only through F1. The rest of what each lens examined is listed so that a second reviewer can open it and disagree.

### Conformance - UNCLEAN (F1)

- **Acceptance 2, as ruled.**
  - Every regular worker projects ≤ 1276 s (`receipts/gates/suite_shards.log`: 1199-1275 s), and leg A projects 1530 s ≤ 2160 s (#737).
  - `CI_BUDGET_SECONDS = int(1800 / 1.41)` = 1276 (`scripts/suite_shards.py:56-57`).
  - Hosted minutes at exact head are as in the table above. The four runs (rtl-full 45528738040, rtl-fast 45528738009, elaborate 45528738049, docs 45528737977) succeeded on attempt 1, with `head_sha` = the head (`receipts/hosted/runs-9c625393.tsv`). Worker minutes total 389.0, matching the PR.
- **"No figure lowered outside those legs."**
  - Per-commit diffs of `SUITE_SECONDS` and `PIECE_SECONDS` show every suite figure raised or unchanged.
  - Lowered values occur only in:
    - `milan_dp`'s four re-keyed legs (`59f4f478`: 1429/508/325/1307 → 1309/1313/275/399);
    - the split pieces of `milan_dp` and `capture_coherence` (`96df313f`);
    - the new `follow_ring` and `media_phase` pieces.
  - 20 of the 21 derivation rows reproduce exactly by ceiling; the 21st is S4 (`receipts/gates/figure-recompute.txt`).
- **Acceptance 1, the gPTP receipts.**
  - The two hosted merge trees (`dd5cf579` → tree `23af3e5f`, `241f036e` → tree `af158eaa`) differ in 43 paths. 18 are this PR's delta and 26 are the base's (`2509db68..e608f8d8`), with `TESTING.md` in both. None is unexplained (`receipts/hosted/merge-tree-classification.txt`).
  - Of the PR's 18 paths, none is a `milan_dp` input.
  - The base moved the `gptp-processor` gitlink `1616fc8f` → `1213ac5b`.
  - I downloaded both hosted `suite-union-milan_dp` artifacts. Each run's `gptp` and `gptp-lat` sections equal the published `*.old-pin.out` / `*.new-pin.out` byte for byte. The only change is the `[#207]` pointer line (`receipts/hosted/gptp-hosted-vs-published.txt`).
  - The 40-run determinism evidence is the author's (round 7). I did not re-run it.
- **Open:** F1, the serial follow_ring output under a pipe jobserver.

### RTL (architecture and interface contracts; no `hdl/` file in the diff) - UNCLEAN (F1)

- No `hdl/` path is in `13e6d869..9c625393` (`git diff --stat`).
- **Interface contracts examined:**
  - `mutant_stage.directory`/`mkdtemp` signatures are unchanged, with 36 and 2 call sites.
  - `ctrl_boundary.py --leg K/N --capture-out` refuses `--selftest`, `--capture` and `--only`, and refuses an existing output (`sw/firmware/ctrl/test/ctrl_boundary.py:472-494`, `:517-518`).
  - The judge's completeness is unchanged: `held()` refuses a builder with no compiles, and a capture whose `cwd` lies outside the checkout is refused (`sw/firmware/ctrl/test/ctrl_runs.py:188-207`).
  - `ctrl_runs.LEGS` and `leg_builders` refuse a stray or empty leg (`ctrl_runs.py:70-92`).
  - `ci_make_cases` builds sequentially and executes in parallel, so media_phase's per-case `build-<case>` never runs two Verilator builds into one directory at once (`scripts/ci_make_cases.py:115-118`, `:144-149`).
- **Open:** F1, the follow_ring Makefile's `run` contract ("every target's commands unchanged").

### Robustness - UNCLEAN (F1)

- **Staging under adversarial and concurrent states:**
  - foreign, world-writable, symlinked and regular-file roots;
  - a non-sticky shared TMPDIR;
  - aliases and different TMPDIRs;
  - another uid's slot;
  - slot exhaustion;
  - removal races under churn: 0 overlaps in 9 600 holds.
  - Receipts are under `receipts/staging/`.
- **Pipeline failure paths** (`.github/workflows/rtl-fast.yml:1148-1366`, `:1504-1580`):
  - With `fail-fast: false`, one failed leg does not cancel the other.
  - A failed leg skips the judge, whose implicit `success()` gate does that. The aggregate then fails on `FIRMWARE_BOUNDARY_CAPTURE_RESULT`.
  - The watcher's `EXPECTED_JOBS` and `SKIPPED_MATRICES` gain both legs.
  - No `pull_request_target`, `workflow_run`, secret, token or permission is added.
  - The required contexts at exact head (`rtl-fast`, `verilator-suites`, `yosys-portability`, `elaborate`, `docs-check`) keep their names and succeeded.
- **media_phase `exec-<case>`:** the recipe line's status comes from `test …rc`, so a `grep -v` with no output cannot fail a passing case. A failing case prints `CASE x FAILED` and exits 1, as the serial `cases` does.
- **Open:** F1, behaviour that depends on the make version.

### Tests - UNCLEAN (F1)

- Run at head, all exit 0 (`receipts/gates/*.log`):
  - `suite_shards.py --selftest`;
  - `ci_suite_pieces_selftest.py` (65 parents, 94 units);
  - `ci_gate_workflows.py --check`;
  - `ci_events.py --check` (2378 items) and `--selftest` (5967 arms, including the six boundary-leg arms and the capture job's RV32 arms);
  - `ci_make_cases_selftest.py`;
  - `test_suite_cancellation.py`;
  - `check_py_idiom.py`;
  - `mutant_stage.py --selftest`.
- **Planted in place, then restored byte-exact:** three of the author's budget defects. Each was refused by its intended control (`receipts/gates/plant-*.log`):
  - budget 1620: "computed without the constant" ESCAPED;
  - rule removed: "1277-second regular worker is refused" ESCAPED;
  - `follow_ring` whole: head worker 0 at 1615 s, FAIL.
- **One mutation driver at head** (`tb/verilator/tcam/mutants.py`, pinned Verilator 5.050 verified by `--version`): two runs are identical, 4 of 4 PASS, and the verdict lines equal the author's published log (`receipts/staging/tcam-mutants-run{1,2}.log`).
- **Open:** F1. The PR's validation command `make -n … run` does not show what it is said to show.

### Docs - UNCLEAN (F1)

- Read: the `docs/testing/CI_WORKFLOWS.md` delta (job list, aggregate list, worker counts, "The #998 budget", the firmware-boundary projection table, the refreshed-figures paragraphs, the projection table), the `TESTING.md` delta, the `RUNNING_TESTS.md` delta, and `sw/firmware/ctrl/README.md:132`, `:630-631`.
- These match the code and the receipts:
  - 94 units, 26 workers, 8 parents (26/36/43/66/4/4/3/18 units);
  - the 1275-second heaviest worker;
  - leg A at 1530 s.
- **Source-comment rule:** the delta adds no bench-lane label, lane name, review round, reviewer ID or issue-comment ID (scan of the delta's added lines). The "round-one" phrase in `CI_WORKFLOWS.md` already existed and is prose.
- **Open:** F1, the PR body's claim about `make -n run`. R923-2-R1 is wording only.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #998 acceptance 1-2 and the manager's rulings; `suite_shards.py` figures and budget; hosted jobs API for runs 45528738040/009/049/37977; both `suite-union-milan_dp` artifacts; merge-tree classification | R923-2 | `9c62539365fea8316dae2b9fd7c68defeff5cb31` |
| RTL | UNCLEAN (F1) | `mutant_stage.py` API; `ctrl_boundary.py`/`ctrl_runs.py` leg and judge contracts; `ci_make_cases.py` build/exec contract; follow_ring/media_phase Makefiles | R923-2 | `9c62539365fea8316dae2b9fd7c68defeff5cb31` |
| Robustness | UNCLEAN (F1) | staging probes; `rtl-fast.yml` capture/judge/aggregate/watcher; media_phase `exec-%` | R923-2 | `9c62539365fea8316dae2b9fd7c68defeff5cb31` |
| Tests | UNCLEAN (F1) | the eight self-tests and gates above; three planted budget defects; tcam mutants ×2 | R923-2 | `9c62539365fea8316dae2b9fd7c68defeff5cb31` |
| Docs | UNCLEAN (F1) | `CI_WORKFLOWS.md`, `TESTING.md`, `RUNNING_TESTS.md`, `sw/firmware/ctrl/README.md` deltas; PR body; added source comments | R923-2 | `9c62539365fea8316dae2b9fd7c68defeff5cb31` |

## Evidence used

- **The author's signed packet** (`review-evidence/cicd3-r1` at `726d9d25`): all 961 `MANIFEST.json` entries match their `published_sha256`, with none missing or unlisted (`receipts/evidence-manifest-726d9d25.txt`).
- **Packet sections read:**
  - author-r4: `mutants/summary.txt`;
  - author-r5: `figures.txt`, `tools/figures.py`;
  - author-r7: `INDEX.md`, `hosted/merge-commits-from-worker-logs.txt`, `hosted/milan_dp-runA-vs-runB.txt`, `local/gptp*.out`.
- **Hosted, read-only:** run and job metadata from the Actions API, and two artifacts (`suite-union-milan_dp` of runs 45481508309 and 45528738040).

## Real limits

- **No make 4.3 binary was run.** F1's pipe-jobserver behaviour was reproduced with GNU make 4.4.1's `--jobserver-style=pipe`. That 4.3 behaves the same is inferred from its pipe-only jobserver, not executed.
- **Not re-run here:**
  - `ctrl_boundary.py` legs and judge (they need the RV32 SDK): I relied on the exact-head hosted jobs' success and the author's round-6 local and negative receipts;
  - the 40-run gPTP determinism set;
  - the full serial sweep;
  - any Verilator piece;
  - act or Docker.
- No manager source bank runs at this head. I neither claim nor infer one.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The 1.41× budget is a projection rule. The hosted shard 1/26 ran 1.33× its projection, at 27.7 minutes.

## Pending manager duties

- After F1's fix, re-review the new head. The F1 fix touches the Tests and Docs scope, and a new commit un-covers any lens whose scope it changes.
- Carry R923-2-R1 to the residue checklist.
- Build and validate the current-dev merge candidate (builder and native banks) and link its receipts.
- Own hosted/act acceptance at the final head.
- Merge only with explicit maintainer authorization and two independent positive reviews.

## Probe hygiene

- The probes ran in place on `scripts/suite_shards.py` and were restored. Its sha256 equals `HEAD:scripts/suite_shards.py` (`7f5b8835…`).
- I removed the `scripts/__pycache__` the gates created.
- `git status --ignored` is clean. Index entries equal the `HEAD` tree listing (`b48e6255…`).
- Gitlinks are checked out at the head's pins: `gptp-processor` `1616fc8f`, `protocol-processor` `801ef228`, `third_party/*` as recorded.
- Disposable trees stayed under `scratch/`, which is not published.

R923-2 FINISHED
