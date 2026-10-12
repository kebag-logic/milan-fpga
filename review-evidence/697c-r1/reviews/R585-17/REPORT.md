[R585] POSITIVE - exact head 27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c

# R585-17: external review of issue #697 / PR #705, round 18 (merge of dev `dc4d06cb`)

- Head `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c`, tree `f84ea680aafd3b578b03cee405aeb818bee8bf4a`, verified in a detached clone.
- Delta under review: `5b4ea551..27ee16b5`. That is merge `ddbd7fd7` (parents `5b4ea551` and dev `dc4d06cb`) plus one commit, `27ee16b5`.
- Prior POSITIVE reviews at `5b4ea551`: R584-15 and R585-16.

**Verdict: POSITIVE.**
- All five lenses were applied independently against the round-18 assignment ([6130298041](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6130298041)).
- There is no open BLOCKER, MAJOR or MINOR.
- One new RESIDUE (PR-body wording) and one new SUGGESTION are recorded. One earlier RESIDUE (R585-16-RES-1) is retained as carried.

## Scope reconstructed

Round 18 asks for four things:

1. Merge dev `dc4d06cb` (#716 / PR #724: `firmware-unit` split into four required firmware jobs) so that both sides stand.
   - Every firmware job keeps its own steps once.
   - No check is dropped or doubled.
   - Each job stays within 60 % of its `timeout-minutes`.
   - `ci_events.py --check` and `--selftest` pass.
2. No other change.
   - The images equal dev `dc4d06cb`'s, entry for entry.
   - All pin controls hold.
   - STOP if firmware behaviour, an image input or the pin would change.
3. Re-run round 17's bar at the merge head.
4. Record the resolution in the PR body.

Two things were read only after my own pass over the diff: prior findings R584-15-RES-1 and R585-16-RES-1 (resolved or retained below), and the PR body.

## What was examined and run (receipts under `receipts/`)

| Check | Result | Receipt |
|---|---|---|
| Remerge of `ddbd7fd7` | Four conflicts, exactly the four files the assignment names. Each is resolved as a union of both sides (read hunk by hunk below). | `remerge-diff-ddbd7fd7.txt` |
| `rtl-fast.yml` parsed and compared with both parents per job | Each job is accounted for: dev's four firmware jobs equal dev's except for the added `third_party/tsn-c-stack` fetch. `firmware-boundary` and `firmware-verilator` equal the branch's. Every other job and the top-level keys equal both parents. The aggregate's `needs` is exactly the union of both parents' jobs, and each job appears once in its env and once in its loop. The 9 firmware check steps each occur once. | `compare-workflow.txt` (script `scripts/compare_workflow.py`) |
| The lane's own change to `firmware-unit` over the old dev base `c6bd08c6` | Only the tsn-c-stack fetch, which the head carries into all four jobs, so nothing of the lane's job is lost in the split | `branch-lane-firmware-unit-delta.txt` |
| Other workflow files | `docs.yml` and `elaborate.yml` equal both parents. `rtl.yml` equals the branch's (the lane's own earlier change). | (command output, summarized here) |
| `ci_events.py --check` / `--selftest` at the head | OK, 2169 items; PASS, 3064 arms | `ci-events-check.log`, `ci-events-selftest.log`, `ci-events-counts.txt` |
| Additivity of the CI contract | Contract items: base `c6bd08c6` 1821, branch +153, dev +195, so 1821 + 153 + 195 = 2169 at the head. Self-test arms: 2530 + 236 + 298 = 3064. Exactly additive, so no item or arm is lost or counted twice in the merge. | `ci-events-counts.txt` (script `scripts/ci_events_counts.sh`) |
| Self-test arms per job | A missing-compiler arm for each of `firmware-unit` (2), the three mutation jobs and `firmware-boundary`. A timeout arm and a budget-row arm for each of the four #716 jobs. | `ci-events-selftest.log:243-294` |
| `--firmware-census` | `"preserved": true` | `firmware-census.log` |
| 15 planted workflow defects against `ci_events.py --check`, on a copy of the head tree | 14 REFUSED. These cover each of the six jobs' fetch without tsn-c-stack, three aggregate `needs` drops, the loop and env drops, the control shard doubled into the AECP job, and `--require-rv32` / `--selftest` dropped from the boundary steps. One escaped: a raised `firmware-boundary` timeout. It also escapes at `5b4ea551`, so it predates the merge; see S1. | `probe-ci-events.txt`, `probe-boundary-timeout-at-5b4ea551.txt` (script `scripts/probe_ci_events.sh`) |
| Shard dispatch proof standalone, traced for process starts | 916 invocations, shards [60, 507, 77, 272], five PASS lines. Exactly one `execve`, the interpreter itself, so it starts no compiler. This supports the `OUTSIDE` reason in `27ee16b5`. | `shards-standalone.log`, `shards-standalone.strace` |
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 2/4` at the head (local) | `test_ctrl_firmware: PASS` in 222 s. It printed the shard proof and `tsn-c-stack at 405dc683…` before any build. | `shard2-aecp.log/.rc` |
| `--shard 3/4` (local) | Did not finish within my 590 s per-command cap while sharing the host (rc 124). The hosted exact-head run below executed it. | `shard3-srp.log/.rc` |
| Captures of the four firmware builders' `--build-only` / builds, made under `ctrl_capture.py` | All rc 0. The merged `test_ctrl_firmware.py --build-only` ends `BUILT`. | `cap-{rv32,ctrl,nvm,cov}.log/.rc` |
| `ctrl_boundary.py --require-rv32 --selftest --without verilator --capture ×4` | PASS. 2822 compiled sources of 3049 invocations; 0 findings; 105 boundary, 106 pin and 4 figure controls; 0 misbehaved. The gate's own standalone build was cut by my 590 s cap (`boundary-without-verilator.*`), so the same judgement ran over the captures. | `boundary-captured-without-verilator.log/.rc` |
| `27ee16b5` necessity probe: the `OUTSIDE` entry removed in place, then restored | REFUSED (rc 2): "sw/firmware/ctrl/test/test_ctrl_firmware_shards.py names the firmware's tree and is a program, and is neither a known builder …". The control run at the head bytes gave PASS. | `probe-outside-removed.log`, `probe-outside-control.log` |
| Pin: stack `include/wire.h` poisoned, then restored | Every form tried was REFUSED (rc 2), naming the file, with 0 build lines first: `--shard 0/4` to `3/4`, `--build-only` and the unsharded `--self-test`. | `probe-poisoned-stack-shard-forms.txt` |
| Flag combinations | `--build-only --shard`, `--build-only --self-test` and all three together each exit 2 with a usage error | `probe-flag-combinations.txt` |
| Images: `ctrl_image.py --base dc4d06cb` | `+0` in every section at both shapes. `ctrl_app.elf` and `.img.bin` sha256 are byte-identical between head and dev at both shapes. | `ctrl-image-base-dev.log`, `ctrl-image-elf-hashes.txt` |
| Image inputs | `git diff 5b4ea551 27ee16b5` touches only `rtl-fast.yml`, `CI_WORKFLOWS.md`, `ci_events.py`, `ctrl_configs.py`, `test_ctrl_firmware.py` and `test_ctrl_firmware_shards.py`. Neither it nor dev's `c6bd08c6..dc4d06cb` touches a firmware source, the image builders, `configs/` or a gitlink. The head differs from dev `dc4d06cb` in exactly the lane's 72 files, the same set as `5b4ea551` against `c6bd08c6`. | (command output, summarized here) |
| Hosted runs at the exact head (run `38297906261`) | All six firmware jobs, `rtl-fast` and every other fast job succeeded. Full CI (run `38297906280`) at the time of writing: `full-ci-gate`, Yosys shards 0-3/4 and Verilator shard 0/5 succeeded; Verilator shards 1-4/5 were still in progress; Physical gPTP was skipped (nightly/manual only; not hardware proof). `docs-check`, `elaborate` and `wire-accountability` succeeded. | `hosted/check-runs-head-final.tsv`, `hosted/*.log` |
| Hosted job logs | Each mutation job: five shard-proof PASS lines, `tsn-c-stack at 405dc683…`, `test_ctrl_firmware: PASS`, and `mutants: 506 of 506 caught` (control). `firmware-unit`: shard 0/4 PASS, store 435 tests, coverage PASS (30 files, 100 %). Each boundary job: 0 findings, 0 misbehaved (105/106/4 and 6/106/4). | `hosted/firmware-*.log`, `hosted/rtl-fast.log` |
| Hosted timings against 60 % of the timeout | `firmware-unit` 694 s of 2700 (25.7 %), control 757 s (28.0 %), AECP 251 s (9.3 %), SRP 730 s (27.0 %), `firmware-boundary` 678 s of 1800 (37.7 %), `firmware-verilator` 436 s of 2400 (18.2 %). All are under 60 %. | `hosted-budgets.txt` (script `scripts/budgets.py`) |

## Resolution read hunk by hunk

- **`.github/workflows/rtl-fast.yml`**
  - The `firmware-unit` comment (`:312-317`) states both sides.
  - The four firmware jobs (`:318-467`) are dev's, and each fetches `third_party/tsn-c-stack`. That is required, because each builds the cores from the submodule and runs the pin check.
  - `gcov --version` stays in dev's four install steps and stays out of the lane's two boundary jobs, as on each side.
  - `firmware-boundary` (`:484-515`) and `firmware-verilator` (`:523-583`) are unchanged from the branch.
  - The aggregate (`:587-630`) needs, binds and loops over all eleven jobs, once each.
- **`scripts/ci_events.py`**
  - Both constant blocks are kept (`:1263-1274`). The inherited env is the union (`:595`).
  - Dev's split derives every job's step list from `firmware-unit`'s merged list (`:2499-2508`), so all four contract fetches require tsn-c-stack. The probes confirm it.
  - `RV32_REQUIRED_STEPS` (`:7909-7919`) keeps the lane's `firmware-boundary` entry and gains dev's three phase steps.
  - `_rv32_sdk_arms` (`:7921-7929`) iterates dev's four jobs plus `firmware-boundary`.
  - Dev's census and budget checks (`:3660-3701`) are unchanged.
- **`sw/firmware/ctrl/test/test_ctrl_firmware.py`**
  - Dev's phase dispatch is kept.
  - The lane adds its `--build-only` refusal of `--self-test` and `EXECUTION.run`, before dispatch (`:282-287`).
  - The lane's pin print is in both `coverage()` (`:227`) and `main()` (`:304`), before any build, and every phase passes through it.
  - The `verdict()` BUILT wording is kept (`:249-251`).
  - The docstring states both flags (`:96-104`).
  - The suite list in dev's `run_suites` equals the branch's former inline list, arm for arm. The branch's separate `Refusal` handling around `lwsrp_pin_arms` is subsumed by the outer handler, still exit 2.
- **`docs/testing/CI_WORKFLOWS.md`**
  - The firmware bullet (`:44-65`) states the four jobs, the tsn-c-stack fetch in each, and that none runs a capture.
  - `:128` says the aggregate also requires the two boundary jobs.
  - The docs-only skip (`:156-157`) names all six jobs.
  - The local commands (`:2448-2460`) list the four shard forms.
  - The lane's former single-job budget lines are replaced by #716's table (`:132-137`). The two boundary jobs keep their own budget paragraphs.
- **`27ee16b5` (`sw/firmware/ctrl/test/ctrl_configs.py:162-163`)**
  - This is one registry entry for a semantic conflict Git could not see.
  - It is necessary: the probe refuses without it.
  - Its reason is accurate: the traced run starts no process.
  - It changes no firmware, image input or pin, so it does not trigger the assignment's STOP condition.
  - The README (`sw/firmware/ctrl/README.md:145`) describes the registry generically, so no prose needs it listed.

## Findings

### R585-17-RES-1 - RESIDUE - Docs - the PR body's Round 18 still says the head is not pushed

- **Artifact:** PR #705 body, `## Round 18`, "Open, for the manager", item (c): "#716's hosted acceptance at the new head, ten consecutive runs, is the manager's; the head is not pushed;" (`receipts/pr-body-at-review.md:466`).
- **Evidence:** the PR head is `27ee16b5`, and hosted runs exist at it (`receipts/hosted/check-runs-head-final.tsv`). This is the same wording defect R584-15-RES-1 found in the Round 17 section.
- **Impact:** wording only. No measurement, figure, verdict, test, code or claim depends on it.
- **Exact fix:** replace "the head is not pushed;" with "the head was pushed after this section was prepared, and its hosted runs are the manager's to accept;".
- **Verification:** re-read the item.

### R585-17-S1 - SUGGESTION - Tests, Robustness - the two boundary jobs' timeouts are not pinned by the CI contract

- **Artifact:** `scripts/ci_events.py:3693-3698` pins `timeout-minutes: 45` for #716's four jobs only. `firmware-boundary` (`rtl-fast.yml:488`, 30 min) and `firmware-verilator` (`:527`, 40 min) are not pinned.
- **Evidence:** raising `firmware-boundary` to 31 passes `--check` at the head and also at `5b4ea551` (`receipts/probe-ci-events.txt`, `receipts/probe-boundary-timeout-at-5b4ea551.txt`). So the merge did not introduce it.
- **Impact:** a raised timeout could quietly widen the budget that `CI_WORKFLOWS.md` states for those jobs. The 60 % rule still holds today by the hosted timings.
- **Suggested outcome:** pin both timeouts, and a stated budget figure if wanted, as #716 does for its four jobs.

## Prior public findings at this head

| Finding | Status at `27ee16b5` | Evidence |
|---|---|---|
| R584-15-RES-1 (PR body Round 17 (d) "the head is not pushed") | APPLIED with its exact text | `pr-body-at-review.md:431` |
| R585-16-RES-1 (allowlist "names a program" wording) | RETAINED as RESIDUE, carried. The source is unchanged (`sw/firmware/ctrl/README.md:181`, `ctrl_build.py:199`, `:551-552`), as round 18 forbids other changes. Its exact fix is recorded in the PR body (`pr-body-at-review.md:461`). | source; PR body |
| R584-15-S1, R585-16-S1 and the earlier retained suggestions (R585-14-S1/S2/S3, R584-13-S1, R585-13-S1/S3, R584-11-S1, R584-9-S1, R585-2-S2) | RETAINED as SUGGESTIONS. They are outside this delta: no file they name changed in `5b4ea551..27ee16b5`. | `git diff --stat 5b4ea551 27ee16b5` |
| R584-8-RES-1 and the #495 residue | RETAINED; not re-verified one by one | - |
| Author-noted carried items: the unused `import os` (`test_ctrl_firmware.py:123`, present at both parents), and `check_rtl_source_lists.py --selftest` under `MAKEFLAGS=w` (same at dev) | Not introduced by the merge; not findings of this round | source |

## Lens results

```text
[R585] PASS Conformance - rtl-fast.yml:318-630; ci_events.py:595,1263-1274,2499-2508,3660-3701,7909-7929; receipts/compare-workflow.txt, ci-events-counts.txt, hosted-budgets.txt, ctrl-image-elf-hashes.txt - round-18 items 1-4 against the assignment: both sides stand, the aggregate is complete, every job is under 60 % by its exact-head hosted time, --check/--selftest pass, images equal dev's, nothing beyond the four files except the necessary registry entry
[R585] PASS RTL - git diff --stat 5b4ea551 27ee16b5 (no HDL file); rtl-fast.yml job/needs topology; test_ctrl_firmware.py:262-310 argument and dispatch contract - no RTL in the delta; the CI job graph, the driver's flag contract (--build-only vs --shard, exit codes) and the pin-before-build ordering hold
[R585] PASS Robustness - receipts/probe-poisoned-stack-shard-forms.txt, probe-flag-combinations.txt, probe-ci-events.txt, probe-outside-removed.log - poisoned stack refused by every form before any build; invalid flag mixes exit 2; 14 of 15 planted workflow defects refused, the escape predating the merge (S1)
[R585] PASS Tests - receipts/shard2-aecp.log, shards-standalone.*, boundary-captured-without-verilator.log, ci-events-selftest.log, hosted/firmware-*.log - merged dispatch executed locally (AECP) and at the hosted exact head (all four phases, 506/506 control mutants, both boundary jobs 0 misbehaved); the shard proof's planted missing/duplicate/future-suite cases pass; per-job self-test arms are present for both sides
[R585] PASS Docs - docs/testing/CI_WORKFLOWS.md:44-65,128,132-137,156-157,2448-2460; test_ctrl_firmware.py:96-116; ctrl_configs.py:162-163; PR #705 body Status and Round 18 - both sides stated and true at the head; residue only (R585-17-RES-1 new, R585-16-RES-1 carried)
```

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment 6130298041; `rtl-fast.yml:318-630`; `ci_events.py` merged regions; image hashes; hosted budgets | R585-17 | `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c` |
| RTL | CLEAN | Delta file list (no HDL); job graph; `test_ctrl_firmware.py:262-310` | R585-17 | `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c` |
| Robustness | CLEAN (SUGGESTION S1 only) | Pin-poison, flag-combination, workflow-plant and registry-removal probes | R585-17 | `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c` |
| Tests | CLEAN (SUGGESTION S1 only) | Local AECP shard, boundary self-test over captures, shard proof, `ci_events` self-test; hosted exact-head firmware logs | R585-17 | `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c` |
| Docs | CLEAN (RESIDUE R585-17-RES-1 new, R585-16-RES-1 carried) | `CI_WORKFLOWS.md` merged sections; `test_ctrl_firmware.py` docstring; `ctrl_configs.py:162-163`; PR body | R585-17 | `27ee16b52ac49b6b2523dafbf45f3af7ff4bba8c` |

## Real limits

- **Local runs:**
  - The SRP shard (`--shard 3/4`) hit my 590 s per-command cap while sharing the host. I did not run the control shard (`1/4`), `--shard 0/4` or `firmware-verilator`'s `--only verilator` gate locally.
  - All of these ran and passed in the hosted jobs at the exact head, which I inspected as executed evidence.
  - The merged `run_selected` and `run_srp_mutants` are byte-identical to dev's.
- **Boundary gate:** the local `--without verilator` self-test judged pre-made captures of the four builders' own commands. The gate's standalone capture run was cut by the same cap. The hosted `firmware-boundary` ran it standalone and passed.
- **Toolchain:** the local toolchain is GCC 16.2.1 with GoogleTest 1.18.0, not the runner's GCC 13.3 with GoogleTest 1.14.0. CPython is 3.14.7.
- **Images:** only `ctrl_image.py`'s two shapes were compared byte-for-byte. The other images rest on input equality: no image input differs between `5b4ea551` and the head, and none changed in dev's delta. Byte identity at `5b4ea551` was established by earlier rounds.
- **Hosted full CI:** when the report was written, Verilator shards 1-4/5 of the exact-head full CI run were still in progress. I neither waited for nor accepted them.
- Physical calibration was NOT RUN; skipped physical contexts are not hardware proof.
- No manager source bank ran at this head, and none is claimed.

## Pending manager duties

- Accept the hosted exact-head runs, including the in-progress Verilator shards 1-4/5, and act replication.
- #716's ten-run hosted acceptance at the new head.
- Validate the current-dev merge candidate (builder and native banks) at the merge turn.
- Carry R585-17-RES-1 and R585-16-RES-1, with the #495 residue, to the residue checklist.
- A merge needs the full completion bar and explicit maintainer authorization.

R585-17 FINISHED
