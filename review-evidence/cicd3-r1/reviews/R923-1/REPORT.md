[R923] NEGATIVE - exact head 13e6d869d842fc06155ef5dae9b0347596d6d4df

# R923-1: internal independent review of PR #1003 (Relates to #998)

- **Reviewed:** the three commits `fcbc31f3..13e6d869`, exact head `13e6d869d842fc06155ef5dae9b0347596d6d4df`, tree `1e43c6e433e84cf7dad9bc1ce86220f0a7f8bb8c`. The PR is stacked on PR #1001 (`fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f`), so this review covers only those three commits:
  - `66b092e1`: run the preflight once per head;
  - `f6c11a25`: stable mutant staging;
  - `13e6d869`: start each piece's longest case first.
- **Role:** internal independent reviewer, working from a cleared context in a detached clone.
- **Sources read:** public state only, in this order:
  1. AGENTS.md and CONTRIBUTING.md.
  2. docs/README.md.
  3. Issue #998's body. The issue has no comments.
  4. The PR body.
  5. The diff and its history.
  6. The author's public evidence packet, `review-evidence/cicd3-r1/author` at `3743d3a8`.
  7. The exact-head hosted run `45457006166`.

## Verdict

**NEGATIVE.** Two MINOR findings are open:

- **F1** affects RTL/architecture, Robustness and Tests.
- **F2** affects Conformance.

Three RESIDUE wording items and three SUGGESTIONs are recorded as well. None of the three commits changes a verdict where I could measure it:

- **Local runs:** 15 mutation drivers ran at base and at head on their own caches, and every comparison is identical. That includes the in-tree `parent=` path, exercised by `milan_dp/split_mutants.py`. 14 ran cold and warm on both arms. For `pp_shadow/pending_mutant.py`, the base warm arm was stopped by the reviewer for time; its cold pair and its head warm arm are identical.
- **Hosted runs:** 12 completed hosted worker artifacts at this head have receipts identical to the base PR head's. That includes `milan_dp__0`, `__1` and `__3`, so it covers the new start order.
- **Planted defects:** a planted preflight failure turns `verilator-suites` red, and 11 of 11 planted defects are caught by the new self-tests.
- **Warm-cache hits:** they rise as the PR states (`receipts/mutants/warm-hits.txt`):
  - The head's warm runs hit 100% on 13 of the 15 warm-measured drivers. The other two are capture_coherence (283/298) and mbx (3461/3464).
  - Five drivers were already at 100% at base. No driver's hit rate fell.
  - For example: maap 296/355 → 355/355, mbx dma_mutants 75/100 → 100/100, csr lock_mutants 16/150 → 150/150, mbx mutants 2732/3464 → 3461/3464.

The open findings are:

1. The new staging helper trusts a predictable shared-`/tmp` root.
2. Its slot lock lets two concurrent holders take the same physical directory.
3. At this exact head, one hosted job ran over the issue's 30-minute bound.

## Findings

### F1 - MINOR - RTL (interface contract), Robustness, Tests - `scripts/mutant_stage.py:47-75`, `:86-109` - the stable stage root is trusted without proof, and its slot lock is keyed by an unresolved path

**Authority and evidence.**

- The helper says it stands in for tempfile's two calls (docstring `:12-15`, `directory()` `:87`). It also says a slot is held "so a run never sees another run's files" (`:17-18`). The task's focus requires that the staging path cannot collide between concurrent runs or users.
- The base's `tempfile` calls created a random `0700` directory atomically.
- The head replaces those calls with the fixed name `<TMPDIR>/milan-mutant-stage-<uid>`:
  - `:49` builds that name.
  - `:55` creates it with `mkdir(parents=True, exist_ok=True)`.
  - `:56` and `:72` resolve slots inside it and create them there.
  - Nothing checks the root's type, owner or mode.
- `receipts/staging/stage_root_probe.txt` shows the consequences:
  - A pre-existing world-writable root is accepted (`root mode=0o777`).
  - A root that is a symbolic link to another directory is accepted, and the slot is created inside the link's target.
  - A `locks` entry that is a plain file makes every driver raise `FileExistsError`.
  - The fresh root is created `0755`.
- `receipts/staging/stage_alias_probe.txt` shows a collision between two concurrent holders:
  - The holders reach the same directory through two TMPDIR spellings: the directory itself and a symbolic link to it.
  - The lock file name hashes the unresolved path string (`:61`), so the two holders get different lock files.
  - Both are handed `alias-0`. The second empties the first holder's live slot: "same physical slot while both held: True; first holder's file survived: False".
- For comparison, the repository's own runner checks the owner and refuses symbolic links for its slot locks (`scripts/act_ci.py:4048-4054`).

**Impact.**

- *Shared hosts.* On a host where another local account can write `/tmp` first, that account can pre-create the predictable root. The root is world-writable or a symbolic link into its own directory. Renaming within a directory it owns needs no access to the victim's `0700` slot, so it can swap the victim's staged RTL or binaries while a mutation campaign runs. The campaign then builds or executes files that account controls.
- *Denial of service.* Any account can make every mutation driver of another user fail by planting `locks` as a file.
- *Same-user collision.* Two of the same user's runs whose TMPDIR spellings alias one directory empty each other's live slot. The mutant builds then fail. The outcome is red rather than falsely green, because "caught" requires the named check. Even so, the campaign result is wrong.
- *Hosted runners.* These are single-account machines, so none of this applies there.

**Required outcome.**

- The stage root is used only when it is a real directory, owned by the caller, with no group or other write permission. Check it with `lstat`, without following a link, both after creating it and when it already exists.
- Otherwise the helper falls back to the base's private random directory, or refuses with a named reason.
- Slot locks are keyed by the resolved physical path, so aliases of one directory share one lock.
- `--selftest` gains planted controls for:
  - a foreign-mode root;
  - a symbolic-link root;
  - a non-directory `locks`;
  - an aliased TMPDIR.

  Each control must fail against the current code.

**Verification.** `python3 scripts/mutant_stage.py --selftest` with the new controls, plus a rerun of this packet's `scripts/stage_root_probe.py` and `scripts/stage_alias_probe.py` against the fixed tree. Each world-writable or symbolic-link root must be refused or bypassed, and aliased holders must get distinct physical slots.

### F2 - MINOR - Conformance - exact-head hosted run `45457006166`, job "Verilator shard 1/19" - a hosted job exceeded the issue's 30-minute bound at this head

**Authority and evidence.**

- Issue #998 acceptance criterion 2: "Every hosted job stays within 30 minutes with margin." The task focus: "The 30-min hosted limit holds for every job."
- At this exact head, "Verilator shard 1/19" ran **38.6 min** in total, of which the suite step took 37.6 min (`receipts/hosted/shard_times.txt`). The same job at the base PR head (run `45383854694`) took 27.3 min, of which the suite step took 26.2.
- Per suite, base then head (`receipts/hosted/base-fcbc31f3-shard1.log`, `receipts/hosted/head-13e6d869-shard1.log`):
  - `capture_coherence__3`: 5.9 → 12.1 min;
  - `milan_dp__1`: 16.6 → 21.9 min;
  - the 8 small suites: 2.5 → 3.7 min.
- Suites the delta does not touch also slowed 1.3-1.6×: `aaf` 50 → 77 s, `tsn_fuzz` 38 → 62 s, `nvm_backend` 27 → 37 s, `cbs` 4.2 → 5.8 s. That points to runner speed. However, this round could not prove the cause: the hosted log names no CPU, and no compiler cache is in use on either run.
- The verdicts are unchanged: both pieces' receipts are identical.
- The other 14 workers that had completed at this head ran 8.1-22.1 min. Shards 7, 8, 12 and 18 were still running at the last read.
- The author's packet projects this job at about 25.1 min after the change. That projection is not borne out at this head.

**Impact.**

- The criterion is not evidenced at this head for that job.
- With a 27.3-minute base figure, the margin is thin enough that one slow runner breaks the bound. Whether the cause is the delta or the runner is still open.

**Required outcome.** Either of:

- hosted evidence at the merge candidate, or a rerun at this head, that shows every job within 30 minutes;
- a published attribution that separates runner speed from the delta for shard 1, for example a same-runner A/B, or `milan_dp__1`'s per-case timing set against untouched suites.

**Verification.** The manager's hosted acceptance run. Read the per-job minutes from the Actions jobs API, as this packet's `scripts/shard_times.py` does.

### RESIDUE (wording only; no verdict, figure, code or test changes)

- **R1:** `docs/testing/TESTING.md:172-173`.
  - Today: "Every mutation driver therefore stages through ... Its directory is `$TMPDIR/milan-mutant-stage-<uid>/<prefix><slot>`, the same from any checkout and in every run."
  - Problem: `milan_dp/split_mutants.py` and `milan_dp/srptx_mutants.py` stage in their suite directory, through `mkdtemp(..., parent=HERE)`, so their path differs per checkout.
  - Exact fix: append "The two in-tree `milan_dp` drivers, `split_mutants.py` and `srptx_mutants.py`, use `tb/verilator/milan_dp/<prefix><slot>` instead, stable within one checkout."
- **R2:** `docs/testing/CI_WORKFLOWS.md:499-500`.
  - Today: "The job is one of the fail-fast watcher's expected jobs, so a failing preflight also cancels the run's workers."
  - Problem: the watcher runs only for pushes and same-repository pull requests (`ci-fail-fast`'s `if`, `rtl.yml:1645-1646`), and the preflight is not part of the worker matrix.
  - Exact fix: insert "on a push or a same-repository pull request; on a fork pull request the workers run to completion and `verilator-suites` is red" before the full stop.
- **R3:** PR #1003 body, Description item 3, last bullet.
  - Today: "Measured milan_dp__0 through its driver: milan_dp__0 through its driver 3411.9 s → 2711.8 s".
  - Exact fix: "Measured milan_dp__0 through its driver: 3411.9 s → 2711.8 s".

### SUGGESTIONS (optional)

- **S1:** `scripts/ci_make_cases.py:144-146`. When `MILAN_COUNTER_FRAME_OUT` is present, the run is serialised to one worker, which now runs the cases in start order, not driver order.
  - Today each piece has exactly one leg that reaches `[CTRS-OUT]`: `nxn4c`, `nxn`, `nxndv` and `nxn8` respectively. The `dynmap`, `maprec*` and `notify` legs return before that section (`tb/verilator/milan_dp/sim_nxn.cpp:3474-3510` against `:6620`), and the other legs build from `sim_main.cpp` or their own sources. So the final dump is unchanged.
  - The documented rule is that presence "preserves the final writer's outcome" (`tb/verilator/milan_dp/README.md:40-41`). Either keep driver order when the variable is present, or say in that comment that the serial order is the start order.
- **S2:** `.github/workflows/rtl.yml:139` (`verilator-preflight`, generated by `scripts/ci_suite_workflows.py` `preflight_job`). Give the job a least-privilege `permissions: {contents: read}`.
  - The job runs head code after a checkout that persists the token, exactly as the workers do today. It is fork-safe to the same degree as the workers and no worse.
- **S3:** Under this run's runner contention, the preflight job was the 18th of the 20 Verilator jobs to start: created 18:34:44, started 19:35:06 (`receipts/hosted/head-job-queue.txt`).
  - By then most workers had finished, so a failing preflight would have cancelled little.
  - If it starts last, it adds its own ~2 min to `verilator-suites`.
  - The "runs beside the workers" benefit holds only with free runners. That could be worth one measured sentence in CI_WORKFLOWS.

## Prior public review findings on this PR

- Before this round, PR #1003 carried no review findings. Its comments were two review-start notices, and it had no reviews and no inline review comments.
- A parallel round's verdict comment (R924-1, same head) appeared while this round was running. I did not read it before writing this verdict and ledger. It is not a prior round.
- The author's packet names its own earlier-round items, for example "Finding 3 (rx_filter)". Those come from other rounds of the lane, not from findings on this PR. They are not adjudicated here.

## Lens coverage (evidence per lens)

### Conformance

**Covered: UNCLEAN (F2).**

What I checked:

- Issue #998 scope. The diff touches no RTL, firmware, owner bound, test expectation or graded figure. Its 53 files are workflows, `scripts/`, two docs and 38 mutation drivers plus one lifecycle test, and the drivers change only where they stage. The lifecycle test's glob is widened, not weakened.
- **Acceptance criterion 1** (byte-identical output) is met wherever it was measured:
  - Local: 15 drivers ran at base and at head (`receipts/mutants/A`, `receipts/mutants/B2`, compared by `scripts/mutcompare.py`, results in `receipts/mutants/compare-*.txt`). Every complete pair is identical except `aaf/start_mutants.py`, which is identical as a multiset. Its arms print as they finish at the base too, and hosted base and head show the same reordering.
  - Hosted: 12 completed workers' receipts are identical outside `head`/`tree`, and their logs differ only in timing, PIDs and the order of parallel build or arm output (`receipts/hosted/artifact-compare-all.txt`).
- **Acceptance criterion 2** is not evidenced at this head (F2).

### RTL (architecture and interface contracts; no `hdl/` file is in the diff)

**Covered: UNCLEAN (F1).**

What I checked:

- **Job graph.**
  - Preflight `needs` and `if` are identical to the workers' (`rtl.yml:139-144` against `:211-216`).
  - The aggregate needs the preflight (`:637-646`), and the job's 15-minute timeout is under 30.
  - The aggregate's new steps (`:727-748`) run inside its existing 3-minute job. Its "every need succeeded" step (`:716-726`) also reads the preflight's result.
  - The fail-fast `EXPECTED_JOBS` (`:1681`) and `ci-manifest` needs (`:1566-1580`) include the job.
  - Required context names are unchanged.
  - `scripts/act_ci.py` names no job id.
- **Sweep CLI contract** (`scripts/run_all_suites.sh:161-197`, `:502-523`):
  - `--no-preflight` is refused without `--ci-pieces`.
  - `--preflight-only` refuses any suite selector.
  - `prepare_logs` (`:314-318`) removes only `*.log`, so the SHA record survives (planted run below).
- **Case-runner contract** (`scripts/ci_make_cases.py:71-106`): results are collected by name and zipped with the `selected` driver order. `ThreadPoolExecutor` starts work first in, first out, and `partition` and `validate_inventory` forbid duplicate cases.
- **Staging contract:** the stand-in for `tempfile` does not keep tempfile's uniqueness or privacy guarantee (F1).

### Robustness

**Covered: UNCLEAN (F1).**

What I checked:

- **Preflight failure paths.**
  - The real committed aggregate step (`scripts/run_aggregate_step.py`) was run over a real `--preflight-only` output, produced by a disposable clone with a planted failing `check_results_fresh.py --self-test`. In that clone, the cancellation self-test was stubbed so that the plant is what fails.
  - The sweep exits 2 at the planted gate and keeps `TARGET_SHA`.
  - The step exits 1 for result `failure` and 0 only for `success` (`receipts/preflight/planted2/`).
- **Preflight without submodules or tools.** The other seven preflight self-tests pass in a clone with uninitialised submodules, and the shims recorded zero simulator, synthesis or converter calls (`receipts/preflight/nosub-individual/summary`). The hosted job at this head ran all eight in 1.6 min and succeeded. Its artifact carries the eight logs and the run's SHA.
- **Cancellation and refusal paths of the new modes.** The new controls passed in full once (`receipts/cancellation/preflight-controls-1.log`). A second run hit the host-load timing boundary that also fails at base (limits below).
- **Staging under foreign, aliased or killed state:** F1.

### Tests

**Covered: UNCLEAN (F1).**

What I checked:

- **Planted defects.** Eleven planted defects, in memory, are each caught by the self-test that claims them (`receipts/negative/negative_controls.txt`). The seven workflow-binding defects:
  - the result test removed;
  - the SHA-record test removed;
  - the dependency on the preflight dropped;
  - `continue-on-error` on the aggregate step;
  - the job unwatched by fail-fast;
  - the job running something other than `--preflight-only`;
  - the job's condition diverging from the workers'.

  The four start-order defects:
  - an unmeasured case dropped;
  - the table ignored;
  - results returned in start order;
  - a table name that is not a live case.
- **Gates at head**, run in a clean clone (`receipts/gates/summary`). These pass:
  - `ci_gate_workflows --check`, `ci_events --check`, `ci_events --selftest` (2287 items, 5755 arms);
  - `ci_gate_workflows_selftest`, `ci_suite_pieces_selftest` (6 binding controls), `ci_make_cases_selftest`;
  - `mutant_stage --selftest`, `gptp_shadow/test_mutant_lifecycle.py`;
  - `check_py_idiom`, `check_sh_idiom`, `check_hygiene`, `docs_check`, `check_doc_paths`;
  - `ci_fail_fast`, `ci_runtime_evidence`, `ci_manifest`, `ci_workflow_plan` self-tests;
  - `generate_ci_evidence_pins --check`, `suite_shards --selftest`;
  - `check_em_dash --base fcbc31f3` and `gen_toc --check`. These two ran with the pinned Markdown lock, because the summary's first attempt lacked it.

  Expected refusal: `--no-preflight` without `--ci-pieces` exits 2.
- **Lifecycle test.** Its removal checks use the recorded workspace path (`tb/verilator/gptp_shadow/test_mutant_lifecycle.py:150`, `:238`, `:395`), so they still bite at the new location.
- **Gap:** no control covers a foreign or aliased stage root (F1).

### Docs

**Covered: CLEAN** (R1-R3 are RESIDUE).

What I checked:

- `docs/testing/CI_WORKFLOWS.md:486-503` and `:3672-3680`, against the generated job and the binding controls.
- The doc's "76 to 97 seconds" figure. It agrees with the hosted shard 9 log of run 45326076983: 76.7 s from step start to the first-suite line. It also agrees with this head's −83 s on shard 1 (118 s → 35 s).
- `docs/testing/TESTING.md:169-176` (staging), `:254-259` (both modes), `:655-656` (the ownership-step wording, verified at `rtl.yml` "Prove specialized suite ownership") and `:674-686` (start order), each against the code.
- Comment-rule scan of every added line in the delta: no lane label, lane name, review round, reviewer ID or comment ID. The one external reference is the issue ID "FPGA-gPTP #104".
- No added line carries U+2014, and none names a private path or identity.

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2) | Issue #998 AC1/AC2; diff file list; `receipts/mutants/*`; `receipts/hosted/artifact-compare-all.txt`, `shard_times.txt` | R923-1 | 13e6d869d842fc06155ef5dae9b0347596d6d4df |
| RTL | UNCLEAN (F1) | `.github/workflows/rtl.yml:139-210,633-760,1564-1700`; `scripts/ci_suite_workflows.py:68-217`; `scripts/run_all_suites.sh:161-197,314-318,502-523`; `scripts/ci_make_cases.py:71-146`; `scripts/mutant_stage.py` | R923-1 | 13e6d869d842fc06155ef5dae9b0347596d6d4df |
| Robustness | UNCLEAN (F1) | `receipts/preflight/planted2/`, `receipts/preflight/nosub-individual/`; `receipts/staging/*`; `receipts/cancellation/*` | R923-1 | 13e6d869d842fc06155ef5dae9b0347596d6d4df |
| Tests | UNCLEAN (F1) | `receipts/negative/negative_controls.txt`; `receipts/gates/*`; `tb/verilator/gptp_shadow/test_mutant_lifecycle.py`; `scripts/suite_preflight_controls.py`; `scripts/ci_suite_pieces_selftest.py:81-116`; `scripts/ci_make_cases_selftest.py:13-43,109-113` | R923-1 | 13e6d869d842fc06155ef5dae9b0347596d6d4df |
| Docs | CLEAN (RESIDUE R1-R3) | `docs/testing/CI_WORKFLOWS.md:486-503,3672-3680`; `docs/testing/TESTING.md:169-176,254-259,655-656,674-686`; delta comment and privacy scan; PR #1003 body | R923-1 | 13e6d869d842fc06155ef5dae9b0347596d6d4df |

## Real limits

- **Cancellation self-test.** `scripts/test_suite_cancellation.py` could not be run green on this host at this time. It fails identically at base `fcbc31f3` and at head, on host-load timing boundaries: `normal-orphan`, `cancel-transition-SIGTERM` and `hard-HUP` "missing boundary" or 60 s finish timeouts (`receipts/cancellation/`, `receipts/gates/test_suite_cancellation.log`, `receipts/preflight/nosub.out`).
  - The new preflight-mode controls in it passed in full once and hit the same boundary class once.
  - The author's packet and the exact-head hosted preflight job record it green. This round does not independently reproduce that.
- **Mutation drivers.** 15 of 38 ran locally at base and head. I chose drivers that the author's packet had not measured; crf_rx, depkt, tcam and rx_filter are the author's.
  - `pp_shadow/pending_mutant.py`'s base warm arm was stopped (addendum).
  - The rest rely on the hosted suite-log comparison (`receipts/hosted/driver-coverage.txt`). That compares the owning suite's log, not each driver's run individually.
- **Local milan_dp piece run.** It was refused by the receipt's source-origin proof, because my clones' submodule URLs are local paths (`receipts/piece/`). The start-order identity rests on the hosted receipts (`milan_dp__0`, `__1`, `__3`), the in-memory controls and the code.
- **`ci_tool_inventory.py --check`** refuses at its parser precondition (`CI_IMAGE_SHFMT`) at both base and head on this host, and no workflow runs it (`receipts/inventory/`). The PR discloses that the inventory does not record the changed scripts.
- **F1 attacker model.** F1's foreign-account cases are modelled by mode and link shape under one account. No second account was used.
- **Hosted run.** The run at this head was still in progress when I last read it: shards 7, 8, 12 and 18 were running, and `verilator-suites` and `yosys-portability` were not yet run. Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Not run:** no act or Docker, no manager source bank, no full sweep, no Yosys or builder bank.

## Pending manager duties

- Hosted and act acceptance at the exact head, including `verilator-suites` red/green and the disposition of F2.
- Rebase onto `dev` once PR #1001 merges.
- Validate the current-dev merge candidate. Live dev at hand-off was `e275d7950ef3385753e6a15d2e191ba855b171ed`; the source base is `fcbc31f3`.
- Carry R1-R3 to the residue checklist.

## Reproduction

The scripts are in this packet's `scripts/`, and each takes its tree as an argument:

- `run_driver.sh` and `wave.sh`: drivers, cold then warm, base and head.
- `mutcompare.py`: transcript identity.
- `negative_controls.py`: planted defects.
- `run_aggregate_step.py`: the committed aggregate step over a real artifact.
- `run_preflight_controls.py`: only the new mode controls.
- `stage_root_probe.py` and `stage_alias_probe.py`: F1.
- `shard_times.py`, `job_queue.py`, `artifact_compare.py` and `checkruns.py`: hosted evidence.
- `gates.sh`: local gates.
- `piece_run.sh`: the refused local piece run.

Tool identities are in `receipts/tool-identity.txt`. Probes ran in disposable clones under `scratch/`, which is not published. The review clone was verified at the exact head afterwards: clean, with the index and tree matching and the six gitlinks at their recorded commits.

## Addendum: end-of-round driver status

- **Wave A** (`receipts/mutants/A`, `compare-A.txt`) ran in exported trees with no git metadata. Seven drivers are valid there and identical: aaf start, avtp_rxmon ctxfmt and fanout, csr lock, reboot_ctrl, render_queue and tkdiag mcr.
  - Its `maap` pair is environment-invalid. Both arms exited 1 identically, because the processor source derivation needs git metadata, and the arms were then stopped.
  - That pair is superseded by wave B2's valid `maap` run. This is the one "differing or missing" count in `compare-A.txt`.
- **Wave B2** (`receipts/mutants/B2`, `compare-B2.txt`) ran in git-backed clones. Eight drivers, every comparison IDENTICAL: maap, mbx, mbx dma, chmap_capture lockstep, capture_coherence, gptp_tables, pp_shadow pending and milan_dp split.
  - The single "differing" count is `pp_shadow-pending_mutant-base-warm`. The reviewer stopped that arm for time (rc 143), so it is not a comparison.
  - `milan_dp/split_mutants.py` (the in-tree `parent=` path) hit 330/330 warm at base and at head. Its in-tree slot was removed after the run.
- **Warm-cache figures** are in `receipts/mutants/warm-hits.txt`.

R923-1 FINISHED
