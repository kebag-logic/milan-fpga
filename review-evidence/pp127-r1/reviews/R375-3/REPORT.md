[R375] POSITIVE - exact head 0404675dcd8788d29cb15a831a8c182438bf1c92

# R375-3: external independent review of processor PR #130 (issue #127), round 3

- **Scope:** delta review of `00b5c6c9..0404675d` (one commit, round-3 executor), for processor issue #127, against my round-2 finding R2-F1 and the round-3 assignment (issue #127 comment 5862744241).
- **Exact head:** `0404675dcd8788d29cb15a831a8c182438bf1c92`, tree `87b2925d9609f9e298ae9a0781dcdd127dcbb1ac`. The review clone is byte-exact at that head after all probes (`receipts/clone-integrity.txt`).
- **Round-3 delta:** four files, 18 insertions and 2 deletions. `.gitattributes` is new (2 lines); `.github/workflows/hdl.yml` +4; `tb/srp_top/Makefile` +5/−1; `tb/srp_top/README.md` +7/−1. There is no RTL change: `git diff 00b5c6c9 0404675d -- hdl` and `git diff cf4e5c63 0404675d -- hdl` are both empty. The 56 mutation patches are byte-identical to round 2.

## Verdict summary

**POSITIVE.** My round-2 MINOR (R2-F1) is resolved, and I found no new MINOR, MAJOR or BLOCKER. All five lenses are CLEAN. One SUGGESTION (R3-S1) is recorded; it does not affect the verdict.

The four assignment checks:

1. **`git diff --check` and the exemption.**
   - `git diff --check 16be6768 0404675d` exits 0.
   - The exemption matches only `tb/srp_top/mutations/*.patch`. It turns off only `blank-at-eol` and `blank-at-eof`; `space-before-tab` stays active in those files.
   - `git apply --check` accepts all 56 patches.
   - My re-run of the campaign is 56/56 KILLED, with 45/45 partition controls passing and 49/49 assertion families covered. The result for every arm is identical to round 2.
2. **The `mutants` target.**
   - `make -C tb/srp_top mutants` runs the complete, unpartitioned committed driver and propagates failure.
   - Plain `make` still runs only the positive suite (1987/1987).
   - The README matches both.
3. **The unrequested CI step.**
   - It is correct: PATH is set the same way as the existing Verilator steps, receipts go to `/tmp`, and a failure fails the job.
   - It ran green on both hosted runs at this head. Hosted, the unmodified target reported `64 checks: 64 PASS`, identical to mine for every arm.
   - It is also necessary. Under the parent's own rules, a `mutants:` target counts only if a processor entry runs it, and the entries are `scripts/run_suites.sh` (plain `make`) and `hdl.yml`. I confirmed this with the parent's unmodified functions: srp_top has no arm without the step, and the `mutants` driver arm with it. The manager's consumer receipt shows `20 of 95` armed, with `protocol-processor/tb/srp_top: mutants driver mutants.py`.
   - **Cost:** it makes the hosted `suites` job considerably longer (see Tests). That is the subject of SUGGESTION R3-S1.
4. **Nothing else changed.** The commit touches only the four files listed above, and there is no RTL change.

## Reconstruction (order followed)

1. **Repository conventions.** This repository has no `AGENTS.md` or `CONTRIBUTING.md`. I read `README.md` and `docs/README.md` (conventions, gates), and `docs/architecture/09_verification.md` §7–8 (CI and suite commands).
2. **Issue #127.** I read the body (frozen acceptance) and every comment: the assignment and decisions (5860872275), the round-2 assignment (5861796018), and the round-3 assignment (5862744241). Round 3 requires `git diff --check 16be6768 <head>` rc 0, the campaign still 56/56 KILLED, and `git apply` accepting every patch. It also takes suggestion R374-2 S1: a `mutants` target so that the parent inventory counts the campaign. There is no RTL change.
3. **PR #130.** I read the body (Round 3 section) and the manager comments 5861561819, 5862222946, 5862231642, 5863090585 and 5863226264 (banks at this head: donor 9/9, consumer 11/11).
4. **Diff and history.** I read the full diff `16be6768..0404675d` and the three-commit history. The round-3 commit is `0404675d`, whose parent is `00b5c6c9`. I read the full text of every changed file and of `tb/srp_top/mutants.py`.
5. **Public executable evidence.** `kebag-logic/milan-fpga@88ed7be3:review-evidence/pp127-r1` is round-1 input, which I verified in earlier rounds; it has no round-3 packet. I also read the manager's receipts for this head under `$VALIDATION_STORAGE/pp127-manager-0404675d/`: donor-full and parent-consumer.
6. **Prior review findings.** I read the prior public review findings (R374-1, R374-2, R375-1, R375-2) only after my own pass over the diff; see "Prior findings" below. I did not read any current-round report from another reviewer.

## Tool identity

- **Simulator.** The requested `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used the manager's per-head wrapper `$VALIDATION_STORAGE/pp127-manager-0404675d/pinned-tool-bin/verilator`, which is also the one the manager's banks at this head use.
  - The wrapper's sha256 is `905795b9…`, byte-identical to the round-2 wrapper.
  - It reports `Verilator 5.050 2026-07-01 rev v5.050`.
  - The binary hashes (`verilator` `fb2cc573…`, `verilator_bin` `44898b22…`) are identical to round 2.
  - The system Verilator (5.052) was not used.
- **Other tools:** git 2.55.0, GNU Make 4.4.1 and Python 3.14.7 (`receipts/tool-identity.txt`).

## Executed evidence (all in this packet)

| What | Result | Receipt |
|---|---|---|
| `git diff --check 16be6768 0404675d` (and `00b5c6c9..0404675d`) | rc 0 (both) | `receipts/whitespace.log` |
| Mutation patches since `00b5c6c9`; `hdl/` since `00b5c6c9` and since `cf4e5c63` | no change in any of them | `receipts/whitespace.log` |
| `git check-attr whitespace` on 9 paths | only `tb/srp_top/mutations/<name>.patch` carries `-blank-at-eol,-blank-at-eof`. The nested `mutations/sub/x.patch`, `tb/srp_top/x.patch`, `mutations/x.diff`, `mutations/README.md`, `docs/x.patch`, RTL, C++ and Python paths are all `unspecified` | `receipts/whitespace.log` |
| Added or removed patch lines with trailing whitespace; space-before-tab in patches | none; none | `receipts/whitespace.log` |
| Probe P1: remove `.gitattributes` in a scratch clone | rc 2: 26 trailing-whitespace and 5 blank-at-EOF hits in 23 files, none outside `mutations/`. This is exactly R2-F1, so the attribute is what clears it | `receipts/whitespace-probes.log` |
| Probes P2–P4: space-before-tab in a patch; trailing whitespace in `tb/srp_top/README.md`; trailing whitespace in a nested `mutations/sub/x.patch` | rc 2 for each, so all three are still flagged | `receipts/whitespace-probes.log` |
| Probe P5: an added `+` line with trailing whitespace in a patch | rc 0. This is exempt by design (see the Robustness notes) | `receipts/whitespace-probes.log` |
| Probes P6/P7: `git apply --check` of all 56 patches, outside a repository against the head `hdl/`, and at a clone root | 56/56 accepted in each case | `receipts/whitespace-probes.log` |
| Committed driver `tb/srp_top/mutants.py`, unmodified, in 14 `--only` partitions (7 concurrent) | 56/56 arms KILLED by their required named assertion; 45/45 partition controls PASS; 49/49 families K1–O8 covered; no cycle-budget exits. Per-arm failure counts and tags are identical to my round-2 run | `receipts/campaign-summary.txt`, `receipts/campaign/`, `receipts/campaign-batch*.{log,time}` |
| Committed target `make -C tb/srp_top mutants`, unpartitioned, bounded at 570 s | all 7 controls PASS, then 15 arms KILLED in table order before the bound (rc 124 is my bound, not a verdict). All 15 match the partitioned results | `receipts/target-run-bounded.log` |
| `make -n` on the target and the default goal | `.DEFAULT_GOAL := run`. `mutants` runs `python3 mutants.py --output "$(MUTANT_OUTPUT)"`, with the default `/tmp/srp-leaveall-mutants`. The command line and the environment both override it, and a path with spaces is quoted. `run_suites.sh` calls plain `make`, and nothing else names `mutants` | `receipts/makefile-target-probes.log` |
| Failure propagation F1: `make mutants VERILATOR=/nonexistent/verilator` | the override reaches the Python-launched inner builds through MAKEFLAGS; the control fails; driver rc 1; make rc 2 | `receipts/makefile-failure-probes.log` |
| Failure propagation F2: PATH without any Verilator | the control fails; make rc 2 | `receipts/makefile-failure-probes.log` |
| Plain `make` in `tb/srp_top` (positive suite) | `1987 checks: 1987 PASS, 0 FAIL`, rc 0, in 99 s. No driver and no `git apply` are invoked | `receipts/head-plain-make-srp_top.log` |
| Parent arm rule counterfactual, using the parent's unmodified `measure_test_evidence.py` (`bfa1e442…`, parent dev `c0723222`) on this head | with the committed entries: goals `['', 'mutants']` and arm `('mutants','driver','mutants.py')`. With the hdl.yml step removed, or with `run_suites.sh` only: goals `['']` and no arm | `receipts/parent-arm-counterfactual.log` |
| `scripts/lint_hdl.sh` (pinned) | rc 0 | `receipts/head-lint_hdl.log` |
| `gen_matrix.py --check`, `check-links.py`, `check-matrix.py`, `check-integrator-params.py`; workflow YAML parses | all rc 0: 921 links; 115 REQ / 17 GAP; 24/24/24 parameters. The `suites` steps parse in the intended order | `receipts/head-gen_matrix-check.log`, `receipts/head-docs-gates.log` |
| Hosted runs at the exact head | Both runs at this head (push 36375812095, pull_request 36375813740) are complete, and 6/6 jobs executed and succeeded. The only skipped step is the Verilator build, skipped on a cache hit. The `SRP LeaveAll mutation campaign` step ran the unmodified target: 7/7 controls PASS, 56/56 KILLED, `assertion coverage: 49/49`, `64 checks: 64 PASS, 0 FAIL`. Every arm is identical to my local run (56/56). The step took 28 min 18 s (push) and 29 min 40 s (PR). The `suites` job took 44 min 7 s and 46 min 37 s, against about 12 min at `00b5c6c9` | `receipts/hosted-jobs.txt`, `receipts/hosted-push-campaign-step.log`, `receipts/hosted-vs-local-campaign.txt` |

Scripts: `scripts/prepare_tree.sh`, `scripts/r375_campaign.py` (adapted from my round-2 script: pinned path and scratch `TMPDIR`), `scripts/whitespace_probes.sh`, `scripts/parent_arm_counterfactual.py`, `scripts/clone_integrity.sh`.

## Manager receipts at this head (read, not re-run)

- **Donor full bank** (`$VALIDATION_STORAGE/pp127-manager-0404675d/donor-full/`): **9/9 rc 0**.
  - It includes step 9, `git diff --check 16be6768 HEAD`, which is rc 0 with an empty log.
  - `run_suites.sh` reports `1015312 checks total, 0 failing`, including srp_top 1987 and srp_stream_fsms 1215.
  - lint, `make -j1 check`, `gen_matrix --check`, `syn/yosys/run.sh` and the `nvm_port` figures are all rc 0.
- **Parent consumer gates** (`parent-consumer/`, parent candidate `1a655ea7` on dev `c0723222`): **11/11 rc 0**.
  - `measure_test_evidence.py --check` reports `20 of 95` armed. The srp_top line is `mutants` driver `mutants.py`. The ratchet is `75 <= 77`, and it notes "can be lowered to 75".
  - DUT-source readers are 0 ≤ 0, and the wall-clock files are 3 ≤ 3. `tb/srp_top/mutants.py` is in neither list.
  - The builder test reports "ALL GATES PASS EXCEPT 1 NOT RUN": the physical-calibration arm (gate 11) has no build report on disk. **Physical calibration was NOT RUN.**

## Prior findings: resolution at this head

| Prior finding | Status at `0404675d` | Evidence |
|---|---|---|
| **R375-2 R2-F1 (MINOR)**: `git diff --check` fails on the mutation patches | **RESOLVED** | rc 0 at head. Removing the attribute reproduces exactly the 31 hits in 23 files, so the scoped attribute is the cause of the pass. 56/56 apply, and the campaign is 56/56 KILLED with 45/45 controls and 49/49 families. The manager's donor bank is 9/9. |
| **R374-2 N1 (MINOR)**, the same defect | **RESOLVED** | Same evidence as R2-F1. |
| **R374-2 S1 (SUGGESTION)**: parent inventory does not count the campaign | **RESOLVED** | There is a `mutants` target, reached from `hdl.yml`. The parent's rules find the driver arm (counterfactual receipt), and the manager's consumer receipt reports 20 of 95 with srp_top armed. |
| R374-1 F1–F5 and R375-1 F1–F4 (resolved at round 2) | **REMAIN RESOLVED** | The round-3 delta touches no RTL, testbench source, driver or patch, so nothing that resolved them has changed. The campaign arms that pin R374-1 F2, R375-1 F2 and F3 are all still KILLED by the same assertions. The consumer gates (R374-1/R375-1 F1) are 11/11 at this head. |

## Lens: Conformance — CLEAN

- **Scope against the assignment.** The round-3 assignment allows exactly two things, the `git diff --check` fix and the `mutants` target, and forbids RTL change. The delta stays within that, plus the CI step, which is judged below. The issue's frozen requirements (keep expiry intent pending, apply the own LeaveAll at `sLA`, an early Leave sees IN, LV + rLv unchanged, #108 separate) were settled and proved in rounds 1–2. They are unaffected, because `hdl/` is byte-identical to `cf4e5c63`.
- **Behavioural proof still green at this head.** srp_top 1987/1987; donor suites 1,015,312 with 0 failing. All the conformance-pinning arms remain KILLED, including `my-expiry-pulse` and `r-expiry-pulse-restored` on K2 (restoring the timer-expiry pulse fails).
- **Examined:** issue #127 body and assignments; PR body; `git diff 00b5c6c9 0404675d`; empty `hdl` deltas; campaign and suite receipts.

## Lens: RTL — CLEAN

- **No RTL change.** `git diff 00b5c6c9 0404675d -- hdl` and `git diff cf4e5c63 0404675d -- hdl` are empty.
- **Scratch copies only.** The mutation patches still apply only to scratch copies: the driver copies `hdl/` into a `TemporaryDirectory` and runs `git apply` there. The attribute has no effect on any RTL file (`hdl/srp/KL_srp_top.sv` is `unspecified`).
- **Checks at head:** pinned lint rc 0. The manager's Yosys portability step is rc 0.
- **Examined:** the `hdl` deltas, the `check-attr` receipt, `mutants.py:89-95,143-148`, and the lint receipt.

## Lens: Robustness — CLEAN

- **Exemption scope is tight.** The pattern contains a slash, so it matches only direct children of `tb/srp_top/mutations/` (the nested `.patch` is flagged).
- **Default rule otherwise intact.** The value is parsed relative to git's default rule, so `space-before-tab` remains active. P2 shows it is still flagged.
- **Inherent exemption on added lines.** The exemption also hides trailing whitespace on `+` lines of future patches (P5). No current patch has one. Such a line would reach only the scratch RTL copy, and `git apply` warns by default, so I record this as an observation, not a defect.
- **Target robustness:**
  - `MUTANT_OUTPUT` is quoted.
  - `VERILATOR=` overrides reach the inner builds.
  - A missing simulator fails closed (make rc 2).
  - Build directories are excluded from the scratch copy (`ignore_patterns("obj_*")`), so the preceding `run_suites.sh` build in CI cannot leak into mutant builds.
  - The verdict comes from the driver's stdout and return code, not from receipt files, so stale logs in a reused `MUTANT_OUTPUT` cannot flip a result.
  - Two concurrent runs on one host with the default `/tmp` directory would overwrite each other's receipt logs but not each other's verdicts. The README documents `MUTANT_OUTPUT`.
- **CI step.**
  - A new `run:` step starts a fresh shell, so re-exporting `PATH="$HOME/verilator/bin:$PATH"` is required. It is identical to the lint/suites and `nvm_port` steps, and the cached Verilator is installed with a prefix, so no `VERILATOR_ROOT` is needed.
  - The step's default `bash -e` makes make's rc 2 fail the job.
  - If the step fails, the later steps in the same job (matrix check, `nvm_port` figures) are skipped. The job is still red, so this cannot produce a false pass; see R3-S1.
- **Examined:** `.gitattributes`, `tb/srp_top/Makefile`, `hdl.yml:49-58`, `mutants.py`, and probes P1–P7 and F1–F2.

## Lens: Tests — CLEAN

- **Campaign unchanged and still sound.**
  - 56/56 KILLED, 45/45 controls and 49/49 families, identical per arm to round 2. This includes all 19 reviewer arms (8 `my-*`, 11 `r-*`).
  - Build failures, timeouts and missing tallies still count as UNPROVEN (`mutants.py:115-117`).
  - The unpartitioned committed target reproduces the same per-arm results for every arm it reached within my bound.
- **Default suite unchanged.** Plain `make` runs only the positive suite, so the swept `run_suites.sh` suite is unchanged.
- **CI reach.** The campaign now runs in hosted CI at every push and pull request. That is what makes the parent inventory count it; with no entry reaching the target, the parent's rules ignore it, which I verified with the counterfactual.
- **Runtime.** On hosted runners the complete unpartitioned target took 28 min 18 s (push) and 29 min 40 s (PR). The `suites` job now takes 44–47 min, against about 12 min at round 2, roughly 3.7×. That is well inside the default 360-min job limit. Like every other step, it runs on both the push and the pull_request event. I judge the cost proportionate: this is the only entry that makes the parent count the campaign, and it is the only complete unpartitioned execution at each head. Its placement is the subject of R3-S1.
- **Examined:** `mutants.py`, the Makefile, the workflow, the campaign receipts, the bounded target run, the counterfactual, and the manager's consumer receipt 10.

## Lens: Docs — CLEAN

- **README campaign command (`tb/srp_top/README.md:207-218`).**
  - The command `make -C tb/srp_top mutants MUTANT_OUTPUT=/tmp/srp-leaveall-mutants` is correct, and its path equals the Makefile default ("the default is shown above").
  - "runs the complete campaign" is true: there is no `--only` in the recipe.
  - "invoked by the HDL workflow" is true (`hdl.yml:55-58`).
  - "Plain `make` still runs the positive suite" is true (`.DEFAULT_GOAL := run`).
  - "`.gitattributes` exempts only those files from blank-at-end-of-line and blank-at-end-of-file" is true (check-attr and probes).
- **Other files.**
  - The `.gitattributes` comment states the reason accurately.
  - The hdl.yml step name is accurate.
  - No other document enumerates the CI steps: `09_verification.md` §8 lists commands, not workflow steps, as it already does for the `nvm_port` figures step. No other document is stale.
- **PR body Round 3 section.** It matches my measurements: 56 byte-identical patches; `git apply --check` passes; 64/64 checks; 19 reviewer arms; 7 controls; 49/49 families; 20/95 armed with 75 unarmed.
- **Gates.** The docs gates pass at head.
- **Examined:** the README diff and its context, `.gitattributes`, `hdl.yml`, `docs/architecture/09_verification.md` §7–8, and the PR body.

## Findings

No open BLOCKER, MAJOR or MINOR.

### R3-S1 — SUGGESTION — lenses: Robustness, Tests

- **Where:** `.github/workflows/hdl.yml:55-58`. The campaign is a step inside the `suites` job.
- **Evidence:** the hosted campaign step took 28 min 18 s (push) and 29 min 40 s (PR) at this head. The `suites` job rose from about 12 min at `00b5c6c9` to 44 min 7 s and 46 min 37 s (`receipts/hosted-jobs.txt`). Locally, the unpartitioned committed target (build parallelism 2) finished only its 7 controls and 15 of 56 arms in 570 s. The campaign is a sequential chain of 63 simulator builds.
- **Impact:** every push and PR now waits for the campaign before the matrix and `nvm_port` figures steps. A campaign failure skips those two independent gates in that run. The job still fails, so there is no false pass, and no receipt directory is kept for diagnosis (only the stdout tails).
- **Suggested outcome (optional):** move the campaign into its own job that restores the same Verilator cache, so it runs in parallel with `suites` and does not mask later steps. Optionally, upload `MUTANT_OUTPUT` with `actions/upload-artifact` on failure. The parent inventory reads `make -C tb/srp_top mutants` from any step in `hdl.yml`, so a separate job keeps the arm counted.
- **Verification:** the hosted `suites` job returns to its previous duration, and a new job runs `make -C tb/srp_top mutants`. `measure_test_evidence.py` still lists srp_top as armed.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #127 body and assignments 5860872275, 5861796018 and 5862744241; PR body; `git diff 00b5c6c9 0404675d`; empty `hdl` deltas since `00b5c6c9` and `cf4e5c63`; srp_top 1987/1987; campaign K2 arms (`my-expiry-pulse`, `r-expiry-pulse-restored`); donor suites receipt | R375-3 | 0404675dcd8788d29cb15a831a8c182438bf1c92 |
| RTL | CLEAN | `hdl` deltas (empty); `check-attr` on RTL paths; `mutants.py` scratch isolation (`:89-95,143-148`); pinned lint rc 0; manager Yosys step rc 0 | R375-3 | 0404675dcd8788d29cb15a831a8c182438bf1c92 |
| Robustness | CLEAN (R3-S1 SUGGESTION) | `.gitattributes` and probes P1–P7; `tb/srp_top/Makefile` and probes (default goal, overrides, quoting); failure probes F1/F2; `hdl.yml:49-58` (PATH, `bash -e`, step order); `mutants.py` verdict path | R375-3 | 0404675dcd8788d29cb15a831a8c182438bf1c92 |
| Tests | CLEAN (R3-S1 SUGGESTION) | committed campaign re-run (56/56, 45/45, 49/49, identical per arm to round 2); bounded unpartitioned target run (7 controls + 15 arms, all matching); plain-make positive suite; parent-rule counterfactual; manager consumer receipt (20/95, srp_top armed); manager donor receipt (9/9); hosted target log (64/64, identical per arm) and job timings | R375-3 | 0404675dcd8788d29cb15a831a8c182438bf1c92 |
| Docs | CLEAN | `tb/srp_top/README.md:207-218`; `.gitattributes` comment; `hdl.yml` step name; `09_verification.md` §7–8; PR body Round 3; links, matrix, params and `gen_matrix` gates rc 0 | R375-3 | 0404675dcd8788d29cb15a831a8c182438bf1c92 |

## Real limits

- **Simulator path.** The requested path is absent. I used the manager's byte-identical per-head wrapper for Verilator 5.050, as recorded above.
- **Campaign partitioning.**
  - The full 56-arm campaign ran through the unmodified committed driver in 14 `--only` partitions, with the scratch copies capped at `--build -j 2`. That kept each foreground command under 10 minutes and within the 8-job limit.
  - The 49/49 family union is my own computation (`scripts/r375_campaign.py summary`).
  - The unpartitioned committed target ran only up to my 570 s bound: 7 controls and 15 arms. The complete unpartitioned execution of the target is the hosted run at this exact head: 64/64, identical to mine for every arm. I inspected its log; I did not execute it.
- **Parent gates and banks.** I did not run the parent consumer gates, the donor bank, or any full parent/PP/gPTP/Yosys/builder bank. I rely on the manager's receipts at this head (donor 9/9, consumer 11/11). The only parent code I executed was the pure arm-rule functions of the published `measure_test_evidence.py`, against this head's three files.
- **Documentation gates.** `make lint`, `wavedrom-check` and `stale` were not run by me, because they need diagram tooling. The manager's `make -j1 check` is rc 0, and this round changes no diagram.
- **Hardware.** Physical calibration was NOT RUN; the builder's calibration arm is NOT RUN. Field skips are not hardware proof. No bench disconnect or STREAM_STOP measurement was made in this round.
- **Round-3 author packet.** No round-3 author packet was published at the named evidence commit. All round-3 claims above rest on my own re-runs and the manager's receipts.
- **Scratch temporary directory.** My bounded target run was stopped by its time bound, which left one `srp-leaveall-*` temporary tree in `scratch/tmp`. It is scratch only and is not published.

## Pending manager duties

1. Publish this packet. Confirm the current-round donor bank (9/9) and consumer gates (11/11) receipts in public form.
2. Build and gate the final current-dev candidate at the merge turn. This is distinct from the source validation here: source base `16be6768`, live dev `c0723222`.
3. Own hosted and act acceptance at this head. All 6 hosted jobs executed and succeeded at this head. The only skipped step is the Verilator build, skipped on a cache hit.
4. Parent pin adoption, with the CRF frame/STREAM_STOP integration regression required by issue #127.
5. Parent-side follow-ups to record (not in this PR's scope):
   - `measure_test_evidence.py` reports "the mutation ratchet can be lowered to 75";
   - its `SUITE_TREES` comment says the processor CI "names one extra target by hand", but `hdl.yml` now names two (`figures`, `mutants`).
6. Schedule the bench re-measurement for parent #608 (100/100 disconnects stop). Physical calibration remains NOT RUN.
7. Decide on the optional R3-S1.

R375-3 FINISHED
