[R636] POSITIVE - exact head fe2e2a543474dd9a932383052bb6fe14bfbbb1fe

Internal independent delta review R636-7, issue #737 / PR #739. Exact tree `08b7735bbb462b55bd3dfbdd179c1c4a9ab99151`. Delta `47fd0d3c510000e9412a1613a723b61d4ef2ae4a..fe2e2a543474dd9a932383052bb6fe14bfbbb1fe`, two commits (`2db6c0f9d`, `fe2e2a543`), assigned by [6190383901](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6190383901).

All five lenses are CLEAN at this head. R636-6-F1 (BLOCKER) is resolved at its cause, and the exact F1 check, the hosted `Local act runner contract gate`, passes on a four-CPU hosted runner at this head. No BLOCKER, MAJOR or MINOR is open. There are two RESIDUE items (PR-body tense, one source-line wrap) and two SUGGESTIONs.

**Runner SHA-256 for the manager's repin:** `scripts/act_ci.py` at this head is `7ff18c6a89aeb40c54d44411ffc6ff766fe6aa0f29baf595ba1e2aa833a446fd` (blob `58b9b054a228447fb469d0435442692132c6ee18`). It matches the author's value. The previous pin at `47fd0d3c` is `f968f67655ac386ea703248b724c3781b95ec379d3a5287b378e470df81f895c` (`receipts/identity.txt`).

## Contents

- [Context reconstructed](#context-reconstructed)
- [Check 1: the runner diff and its trust boundary](#check-1-the-runner-diff-and-its-trust-boundary)
- [Check 2: the four-CPU control and the planted non-containment](#check-2-the-four-cpu-control-and-the-planted-non-containment)
- [Check 3: the hosted docs run at this head](#check-3-the-hosted-docs-run-at-this-head)
- [Check 4: R1, R2, S1 and S2](#check-4-r1-r2-s1-and-s2)
- [Check 5: workflows unchanged](#check-5-workflows-unchanged)
- [Findings](#findings)
- [Lens results](#lens-results)
- [Prior findings at this head](#prior-findings-at-this-head)
- [Reviewer-owned ledger](#reviewer-owned-ledger)
- [Real limits and pending manager duties](#real-limits-and-pending-manager-duties)

## Context reconstructed

I read these in order:

1. AGENTS.md.
2. The issue body.
3. The round-7 assignment 6190383901 and the author's REVIEW READY 6191144807.
4. The full delta diff (`receipts/delta-47fd0d3c-fe2e2a54.diff`) and its two commits.
5. The published round-7 evidence at `c3d4b118`: `review-evidence/737-r1/author-r7/round7-evidence.json` and `round7/`.
6. The live PR body (`receipts/pr739-body.md`, sha256 `0c1c7937...3991`).
7. The exact-head hosted runs.

I read the prior reviews R636-6 (6190373804) and R637-6 (6190205831) only after my own pass over the diff, to resolve or retain their findings.

The delta touches four files:

- `scripts/act_ci.py` (+4/-2);
- new `scripts/act_ci_small_host_selftest.py` (+101);
- `scripts/ci_gate_workflows_selftest.py` (+35/-1);
- `docs/testing/CI_WORKFLOWS.md` (+26/-1).

No HDL, gitlink, workflow template or generated workflow changes.

## Check 1: the runner diff and its trust boundary

**Result: holds.**

- **The whole `scripts/act_ci.py` diff** is two hunks inside one function, `selftest_main_entry_probe`, nested in `run_main_entry_probe` (`scripts/act_ci.py:12168-12182`):
  - one comment line is replaced by three;
  - on the existing `with` that patches `SAFE_PATH`, `):` becomes `), mock.patch.object(os, "cpu_count", return_value=512):`.

  No other line changes. No production function, constant, refusal, argument parser or pin block changes. The author's published `round7/act_ci.diff` is byte-identical to my diff.
- **The patch scope is right.**
  - The `with` encloses the `main([... "--cpu-ranges", ...])` call, so `parse_cpu_ranges` (`:4675-4696`) sees 512.
  - The probe still runs production `main` against the stub `gh`, and still sends SIGTERM through `process_directed_signal_probe` (`:12046`).
  - The patch matches the other main-path probes (`:6574`, `:8635`, `:13495`, `:13677`, `:14675`, `:14783`, `:14846`), all `return_value=512`.
- **Only the flat-install launcher escapes the forced count.**
  - The only self-test arm that re-executes the runner as a fresh interpreter is the flat-install launcher (`:6499`), and the isolated child skips it via `sys.flags.isolated` (`:6485`).
  - The only other `sys.executable -I` spawn (`:12145`) runs a tree helper, not the runner.

  So the control's claim that "every other arm runs under" the forced count holds.
- **No in-tree pin needs updating.** No file in the tree carries either runner hash, so the repin is the coordinating role's host-side duty.

## Check 2: the four-CPU control and the planted non-containment

**Result: holds, on published evidence.** I did not execute the control. It runs the runner self-test, which this round does not allow on the host.

**Control source** (`scripts/act_ci_small_host_selftest.py:44-97`):

- The bootstrap forces `os.cpu_count` in an `-I` child and runs the read-only installed runner as `__main__`.
- The clean run must exit 0 and print `selftest: PASS`.
- The planted copy replaces the single `return run_with_cleanup_signals(execute_pr_run)` with `return execute_pr_run()`. If that anchor does not appear exactly once, the control fails closed (`:79-81`).
- The planted run must exit non-zero, print the main-entry probe's FAIL line, and leave stderr free of `exceeds this host's`. That stderr test is not vacuous: the forked probe child inherits stderr, and `main` prints its refusal there (`:16855`).
- `--cpus` is bounded to 1..63 (`:76-77`).

**Published logs.** All four digests match `round7-evidence.json` (`receipts/published/`).

| Log | sha256 | Key lines |
|---|---|---|
| `control4.log` | `dff4027b...f9c9` | Forced count 4. Clean run: `selftest: PASS`, with `ok production main contains an interrupted early repository lookup` (l.487). Planted run: `FAIL` on that probe only (`selftest: 1 FAILURE(S)`, l.1210), detail `recorded=(2559, 2560, 2559) runner_status=-15 group_absent=False` (l.1218). The stub was reached and its group survived. Ends `small-host runner control: PASS` |
| `control1.log` | `619c97b5...435e` | Same outcomes at a forced count of 1 |
| `control-unfixed.log` | `e191be3e...b598` | The `47fd0d3c` runner. Its clean run fails with `act-ci: REFUSED: CPU range 0-15 exceeds this host's 4 CPUs` and `recorded=None` (l.607-608), which reproduces the hosted refusal. Its planted run fails only by that refusal, and the control rejects it (l.1219-1225, `2 FAILURE(S)`) |
| `gate.log` | `8e8e5f26...d00d` | Both docs-step invocations print `selftest: PASS` (l.611, l.1220) |

`docs/testing/CI_WORKFLOWS.md:1748-1767` documents the control, and the text matches the source.

## Check 3: the hosted docs run at this head

**Result: green for the F1 check.**

- **Run and job.** Docs run **38728843356** (`pull_request`, head `fe2e2a54`). Job `docs-gates-2` **116401304536** completed with **success**.
- **Step 18, `Local act runner contract gate`:** 11:47:40Z to 11:49:15Z, success.
  - The first invocation prints `ok flat isolated full selftest uses the explicit shipping worktree`.
  - Both invocations print `ok production main contains an interrupted early repository lookup` and `selftest: PASS`.
  - The step window has 0 `FAIL` lines and 0 `REFUSED: CPU range` lines (`receipts/hosted/step18-summary.txt`).
  - The job ran on 4 CPUs: `CI_BUILD_JOBS: 4`, `VERILATOR_JOBS: 4` (log l.387-390).
  - Raw log: `receipts/hosted/job-116401304536-docs-gates-2.log`, sha256 `b9baf2f0...db35`.
- **The passing bytes are the reviewed bytes.** The hosted checkout is the PR merge ref `c8aea9fc58215d1ddd0ce2190e6ac4847808bb70`, whose parents are dev `65617779018f41d7e55d1b1ac189ef882bff6367` and this head. Its `scripts/act_ci.py` and `scripts/act_ci_small_host_selftest.py` blobs equal this head's (`receipts/hosted/merge-ref-identity.txt`).
- **Other steps in the same job.** Step 16 (docs builder leg 1) and step 17 (`CI event and SHA contract gate`, `selftest: PASS (2187 contract items, 5215 arms)`) succeeded.
- **Rest of the hosted state at the 11:51:18Z snapshot** (`receipts/hosted/snapshot-final.txt`):
  - succeeded: `docs-gates-0`, `docs-check-no-git`, `wire-accountability`;
  - still running: `docs-gates-1` and the fail-fast watcher;
  - `elaborate` in progress; `rtl-fast` and `rtl-full` queued.

  I infer no completed workflow, duration or aggregate verdict from that snapshot.

## Check 4: R1, R2, S1 and S2

**Result: all four hold.**

**R1 (resolved).** The live PR body's round-6 status (l.44-50) ends with the exact text "The coordinating role published this head." No historical paragraph still says the author does not push. The sentence appears again in the round-7 status: see R636-7-R1.

**R2 (resolved).** The last "Known limitations" bullet (l.200-203) carries the exact R636-6 text, wrapped.

**S1 (resolved).** `scripts/ci_gate_workflows_selftest.py:444-451` requires that the workers owning a builder case equal `BUILDER_WORKERS[name]`. It also requires that each leg's upload path holds `builder-leg-*.json` exactly when that leg is an owner.

**S2 (resolved).** `scripts/ci_gate_workflows_selftest.py:93-114` plants two templates each for docs and elaborate:

- one with the driver repeated in a preparation line, whose last line is still the driver;
- one whose last line is `true`.

An assertion pins that each plant breaks one condition alone (driver count 2 or 0), and the generator must raise "one driver command".

**My mutation battery** (`scripts/mutation_probe.sh`, receipts in `receipts/mutations/`) ran in disposable full copies. Each mutation was regenerated, so `ci_gate_workflows.py --check` returns 0 under it.

| Mutation | Gate self-test |
|---|---|
| m0 pristine | rc 0. Four "Builder split refused" lines; `gate workflow and union controls: PASS` |
| m1 receipts kept for elaborate only (R636-6's S1 probe) | rc 1, `AssertionError: ('docs', 1, ...receipt.json)` |
| m2 receipts kept on every worker | rc 1, `('docs', 0, ...builder-leg-*.json...)` |
| m3 preparation-line refusal removed (R636-6's S2 probe) | rc 1, "builder split accepted the docs template with its driver in a preparation line" |
| m4 last-line refusal removed | rc 1, "...with its last line not the driver" |
| m5 receipts dropped on the last builder worker | rc 1, `('docs', 2, ...)` |

Every mutation is killed.

## Check 5: workflows unchanged

**Result: holds.**

- `git diff --name-status 47fd0d3c..HEAD` lists only the four files above, and nothing under `.github/` (`receipts/identity.txt`).
- `python3 scripts/ci_gate_workflows.py --check` returns 0 at this head (`receipts/head-gates.txt`).

The round-6 template and generated-graph verdicts carry forward unchanged.

## Findings

### R636-7-R1 - RESIDUE - Docs - PR #739 body, Status, round-7 paragraph (body l.29): "The author does not push."

**Evidence.** The live PR head is `fe2e2a543474dd9a932383052bb6fe14bfbbb1fe`, so the head is published. This is the same pattern R636-6-R1 fixed for round 6, recurring for the new round.

**Exact fix.**

- Replace "The author does not push." with "The coordinating role published this head."
- Optionally, update the round-7 section's closing sentence (body l.693-695). Replace "After review, the coordinating role repins the runner and reads back the hosted docs run at this head; that readback is the exact check for F1." with "After review, the coordinating role repins the runner. The hosted docs run at this head, run 38728843356, passed the runner contract gate on four CPUs; that is the exact check for F1."

**Verification.** Read the live PR body against the PR head and the run.

### R636-7-R2 - RESIDUE - Docs - `docs/testing/CI_WORKFLOWS.md:1766`

**Evidence.** The line "`sudo`, as on the hosted runner. The hosted gate itself runs on four CPUs, so this control is a local" is 101 characters, while the surrounding paragraph wraps near 78. This is layout only: the rendered text is unchanged, and `check_doc_style.py` passes.

**Exact fix.** Re-wrap lines 1765-1767 at the paragraph's width, with no wording change.

**Verification.** Check the line lengths and run `python3 scripts/check_doc_style.py`.

### R636-7-S1 - SUGGESTION - Tests, Robustness - `scripts/act_ci_small_host_selftest.py:91`

**Evidence.** The planted arm establishes "reached the lookup" only in combination. It checks that the CPU-refusal text is absent, and it relies on the clean run passing in the same environment. The probe already prints direct evidence: `recorded=(...)` when the stub ran, and `recorded=None` when it did not (`control4.log` l.1218, `control-unfixed.log` l.1220). The conjunction is sound today, because the control requires both runs.

**Suggested outcome.** The planted arm also requires a recorded tuple, that is, no `recorded=None` in the probe detail. Then the arm alone proves that the lookup was reached, even if some other early refusal is added later.

**Verification.** The `47fd0d3c` runner still fails the control, and this head still passes.

### R636-7-S2 - SUGGESTION - Tests - `docs/testing/CI_WORKFLOWS.md:1764-1767`; no workflow step runs `scripts/act_ci_small_host_selftest.py`

**Evidence.** The control is a documented local command. If the control itself regresses, for example through a moved anchor, nothing shows it until someone runs it, although it then fails closed. The hosted four-CPU gate covers the product behaviour. The decision not to add a step is public and reasoned: a step would change the generated graph and the contract inventory.

**Suggested outcome.** Optionally, in a follow-up, run the control in an existing contract step the next time the graph is regenerated.

**Verification.** Not applicable at this head.

## Lens results

```text
[R636] PASS Conformance - scripts/act_ci.py:12168-12182 (full diff, receipts/delta-47fd0d3c-fe2e2a54.diff); hosted docs run 38728843356 job 116401304536 step 18 on 4 CPUs at merge ref c8aea9fc (dev 65617779 + head); round-7 decision 6190383901 - only the probe changed, no production path; the F1 required outcome (hosted gate passes, probe exercises the lookup, planted non-containment fails) is met; runner SHA-256 7ff18c6a...46fd recorded for the repin
[R636] PASS RTL - git diff --name-status 47fd0d3c..fe2e2a54 (receipts/identity.txt); gitlinks unchanged (receipts/integrity.txt) - no HDL, constraint, gitlink, template or generated workflow in the delta; CI scheduling graph unchanged (ci_gate_workflows.py --check rc 0); the lens is inapplicable by those artifacts
[R636] PASS Robustness - scripts/act_ci.py:4675-4696, 6485, 6499, 12046, 12145, 12168-12182, 16855; scripts/act_ci_small_host_selftest.py:76-97 - the dependence on the host CPU count is removed; control checked at 4 and 1 CPUs and against the unfixed runner (published logs, digests verified); fail-closed anchor and bounded --cpus; only the flat launcher escapes the forced count; S1 SUGGESTION only
[R636] PASS Tests - scripts/ci_gate_workflows_selftest.py:93-114, 444-451; receipts/mutations/m0-m5; receipts/published/control{4,1,-unfixed}.log - each new check is killed by its mutation (5/5) and pristine passes; the control fails the 47fd0d3c runner and passes the head; S1/S2 SUGGESTION only
[R636] PASS Docs - docs/testing/CI_WORKFLOWS.md:1446-1453, 1748-1767; PR #739 body (receipts/pr739-body.md) l.20-64, 186-203, 643-695 - text matches the control source, the self-test and the hosted evidence; R1 and R2 exact texts present; R636-7-R1/R2 are RESIDUE only
```

**Supporting gates I ran at this head**, in a disposable copy (`receipts/head-gates.txt`):

- `ci_gate_workflows.py --check`: rc 0.
- `check_hygiene.py --check`: rc 0.
- `check_doc_style.py`: rc 0.
- `py_compile` of the new control: rc 0.
- `git diff --check 47fd0d3c..fe2e2a54`: rc 0.
- `check_em_dash.py` could not judge, rc 2, because the pinned renderer html5lib is not installed here. A fallback scan of the delta's added lines found 0 U+2014, and the hosted `Added-line em-dash gate` passed on `docs-gates-0`.

## Prior findings at this head

| Finding | Status at `fe2e2a54` | Evidence |
|---|---|---|
| R636-6-F1 (BLOCKER: runner self-test fails on hosts with fewer than 64 CPUs) | **Resolved** at its cause | Checks 1-3; hosted step 18 succeeded on 4 CPUs |
| R636-6-R1 (RESIDUE: round-6 publication tense) | **Resolved**, exact text. **Recurs** for round 7 as R636-7-R1 | PR body l.50 and l.29 |
| R636-6-R2 (RESIDUE: last limitation bullet) | **Resolved**, exact text | PR body l.200-203 |
| R636-6-S1 (receipt retention unchecked) | **Resolved** | `ci_gate_workflows_selftest.py:444-451`; m1, m2 and m5 killed |
| R636-6-S2 (preparation-line refusal unplanted) | **Resolved**, and the last-line refusal is now planted too | `ci_gate_workflows_selftest.py:93-114`; m3 and m4 killed |
| R636-5-S2 (stray `milan_dp` arm not refused by the generator) | **Retained** | `scripts/ci_suite_workflows.py` is not in the delta |
| R636-4-S1 ("listed above" union log line) | **Retained** | `scripts/ci_builder_legs.py` is not in the delta |
| R636-4-S2 (builder-inventory reader not in the preparation contract) | **Retained** | `scripts/ci_suite_workflows.py` and `ci_gate_receipts.py` are not in the delta |
| R636-4-S3 (driver selection refusals lack subprocess controls) | **Retained** | `sw/builder/test_builder.py` is not in the delta |
| R636-1-S4 (piece versus parent deadline wording) | **Retained** | `scripts/run_all_suites.sh` is not in the delta |
| R637-6 (POSITIVE, no new finding) and every finding it lists as resolved | **Remain resolved**; the delta touches none of their artifacts | R637-6 table; delta file list |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-7 decision 6190383901; full `scripts/act_ci.py` delta; hosted docs run 38728843356, job 116401304536, step 18; merge-ref identity; runner SHA-256 | R636-7 | `fe2e2a543474dd9a932383052bb6fe14bfbbb1fe` |
| RTL | CLEAN (inapplicable: no HDL, gitlink or workflow change) | Delta file list; gitlinks; `ci_gate_workflows.py --check` | R636-7 | `fe2e2a543474dd9a932383052bb6fe14bfbbb1fe` |
| Robustness | CLEAN (S1 optional) | `scripts/act_ci.py:4675-4696, 6485, 6499, 12046, 12145, 12168-12182, 16855`; `scripts/act_ci_small_host_selftest.py`; published control logs | R636-7 | `fe2e2a543474dd9a932383052bb6fe14bfbbb1fe` |
| Tests | CLEAN (S1, S2 optional) | `scripts/ci_gate_workflows_selftest.py:93-114, 444-451`; `receipts/mutations/`; published control logs; hosted step 18 | R636-7 | `fe2e2a543474dd9a932383052bb6fe14bfbbb1fe` |
| Docs | CLEAN (R1, R2 RESIDUE) | `docs/testing/CI_WORKFLOWS.md:1446-1453, 1748-1767`; live PR #739 body | R636-7 | `fe2e2a543474dd9a932383052bb6fe14bfbbb1fe` |

Code outside the delta keeps its round-6 lens verdicts:

- R637-6 found all five lenses CLEAN at `47fd0d3c`.
- R636-6 found Docs CLEAN there.
- F1 was the only cause R636-6 recorded under its UNCLEAN lenses, and it is resolved here.

Nothing those verdicts depend on changed in the delta: no template, no generated workflow, no union rule, no builder driver and no product source.

## Real limits and pending manager duties

**What I ran and did not run.**

- I did not run, on the host, `act_ci.py`, the runner self-test or the small-host control.
- I did not run Docker, act, or any parent, PP, gPTP, Yosys, builder or Verilator bank.
- The four-CPU and one-CPU control results rest on the author's published logs. Their digests match the signed evidence index, and the exact-head hosted gate on four CPUs confirms them independently.

**Hosted state.** At my snapshot (11:51:18Z), docs run 38728843356 was still in progress (`docs-gates-1` builder leg 0 and the watcher). `elaborate` 38728843378 was in progress, and `rtl-fast` 38728843346 and `rtl-full` 38728843379 were queued. Only the jobs named as completed in Check 3 are evidence. I claim no workflow duration, 30-minute readback or aggregate verdict.

**Not claimed.** Physical calibration is NOT RUN, and field skips are not hardware proof. No manager source bank exists at this head, and none is inferred. The source-head execution evidence is the author's published receipts.

**Pending manager duties.**

1. Repin the runner to `7ff18c6a89aeb40c54d44411ffc6ff766fe6aa0f29baf595ba1e2aa833a446fd`, then run the local replay with the repinned runner.
2. Read back the completed exact-head hosted runs (docs, elaborate, rtl-fast, rtl-full), with their durations and required contexts.
3. Build and validate the current-dev merge candidate with its builder and native banks, and link the receipts. The source base is `fa7347fc59173f90e4feec2df207692e6e6e72ec`; live dev is `65617779018f41d7e55d1b1ac189ef882bff6367`.
4. Carry R636-7-R1 and R636-7-R2 to the residue checklist.

**Clone integrity.**

- All probes ran in disposable copies under `scratch/`.
- The review clone is at the exact head and tree, with 0 status entries including ignored files. I removed the bytecode caches created by one in-clone self-test run.
- The index has 1,376 entries, and all six gitlinks are unchanged (`receipts/integrity.txt`).

**Portable script.** `scripts/mutation_probe.sh <clone> <scratch> <receipts>`.

R636-7 FINISHED
