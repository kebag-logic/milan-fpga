[R818] POSITIVE - exact head 88e1041c9b100c389f3629dfcf3185ad3be9c3f4

# R818-1: external review of PR #875 (issue #873) at exact head

- Head `88e1041c9b100c389f3629dfcf3185ad3be9c3f4`, tree `aadd493164d34bd1e5c65b165abff6f8e2b1d1a4`.
- Three commits on source base `45c0b56c1f4a8a52878815fdcb1359d18e2c5b1c`, which is also live `dev` at review time.
- Diff: `scripts/act_ci.py` +315/-49 (code and self-test arms), `docs/testing/CI_WORKFLOWS.md` +65/-10. No other file changes. No workflow, dispatcher (`ci/act/cpu_ranges.go`) or evidence-writer change.
- Reviewed from public state, in this order: AGENTS.md, CONTRIBUTING.md (via AGENTS), issue #873 body and comments, #737 (the owner CPU rule), the PR body, the diff and history, the published author evidence at `review-evidence/873-r1` (commit `5e97bbf7`), and hosted check runs at the exact head.
- This is source validation at the head. It is not a manager source bank and not the current-dev merge candidate. No physical calibration ran, and no Docker, act or live replay ran.

Verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR finding is open. Two RESIDUE wording items and seven SUGGESTIONs are recorded below. Every lens is covered clean at this head.

## What was run (all on fresh clones, offline sandbox)

Every command ran inside `scripts/sbx.sh`. That wrapper uses `bwrap` with `/run` replaced by an empty tmpfs, so no Docker socket is visible, and `--unshare-net`, so there is no network. `strace` traced every `execve` and `connect`. Result (`receipts/exec-trace-summary.txt`): 0 docker, sudo or act executions and 0 Docker-socket connects across 62 traced runs. The only `gh`, `pasta` and `git-remote-https` executions (115 of 115) are the self-test's own stubs under `/tmp/act-ci-*-selftest-*`.

| Run | Result | Receipt |
|---|---|---|
| head `python3 scripts/act_ci.py --selftest` | rc 0, `selftest: PASS`, 657 ok, 0 FAIL, 91 s | `receipts/head-selftest.{log,rc}` |
| base `45c0b56c` same | rc 0, 623 ok | `receipts/base-selftest.{log,rc}` |
| head flat 0555 install `-I ... --selftest --worktree` | rc 0, 655 ok | `receipts/head-flat-selftest.{log,rc}` |
| base flat install | rc 0, 621 ok | `receipts/base-flat-selftest.{log,rc}` |
| head `act_ci_small_host_selftest.py` | rc 0, `small-host runner control: PASS` | `receipts/head-small-host.{log,rc}` |
| arm label diff, base to head (4- and 5-digit line numbers normalised) | 0 base arms missing, in both installs; 34 new, identical set in both | `receipts/*.labels`, `receipts/new-arms-selftest.txt`, `receipts/new-arms-flat-selftest.txt` |
| default-behaviour differential, base vs head runner, same fixture | byte-identical JSON over 5 accepted and 15 refused `--cpu-ranges` cases | `receipts/probe-default-{base,head}.log`, `receipts/probe-default.diff` (empty) |
| 8 x 6 and 8 x 8 at 4 GiB, end to end through `parse_cpu_ranges`, `replay_container_concurrency`, `job_cpu_ranges`, `build_act_command` | accepted with the expected act words; kept refusals at each width | `receipts/probe-geom-8x6x4.log`, `receipts/probe-geom-8x8x4.log`, `receipts/probe-geom-8x{6,8}-ranges.log` |
| 24 reviewer-designed planted defects (M01-M24) + 2 base twins | 21 head mutants killed, 3 survived (M02, M09, M23; see S1-S3); M02 and M09 also survive at the base (B02, B09) | `receipts/mutants.txt`, `receipts/mutants-rerun.txt`, `receipts/mutants-base.txt`, `scripts/mutants.py` |
| author's 22 published planted defects, re-applied by me | 22/22 killed; 21/22 with the identical FAIL set; M5 had one extra, unrelated timing-arm FAIL that did not reproduce in 3 reruns | `receipts/author-mutants-replay.txt`, `receipts/load/M5-rerun-*`, `scripts/replay_author_mutants.py` |
| load: 6 head + 6 base flat self-tests at once | 12/12 rc 0 PASS | `receipts/load/{head,base}-*.{log,rc}` |
| 15 `docs.yml` gates touching the changed files, head and base, with submodules and the pinned renderer | head: all rc 0 (docs_check 0 findings; em-dash 0 findings over 65 added lines; doc_style, doc_paths, TOC anchors, docs_inventory, py_idiom, hygiene, fail_fast, test_evidence, naming, TODO, ci_gate_workflows, ci_events, `git diff --check`) | `receipts/gates/{head,base}/*`, `scripts/gates.sh` |
| `cd tests && behave` | 508 scenarios passed | `receipts/head-behave.{log,rc}` |
| `--help` | the three options and their bounds | `receipts/head-help.log` |
| hosted check runs at the exact head (read only) | snapshot at 10:34:45Z: 21 success, 1 skipped, 31 queued or in progress; `docs-gates-2` (holds the act runner contract gate) success | `receipts/hosted-checks-snapshot.txt` |

In my first mutant pass, M12, M15 and M22 were malformed (two syntax errors and one ambiguous match). They were corrected and re-run in `receipts/mutants-rerun.txt`, and all three are killed. The count of 21 includes them. M04 and M18 are killed by the module refusing its own default geometry at import, so they report no FAIL line, only rc 1.

## Focus items, judged against the issue and the code

1. **Default command line unchanged: shown, not asserted.** `receipts/probe-default.diff` is empty. Base and head runners built the same act command for 4 x 16 ranges, 4 x 12 fallback ranges, mixed 16+12, one range and eight 16-CPU ranges: `--concurrent-jobs 4`, `MILAN_CI_FALLBACK_CPUS=12`, `--memory=8g --memory-swap=8g`, the same replay concurrency and the same selected ranges. They also gave the same refusal text for 15 bad `--cpu-ranges` values, including `0-5`, `0-7`, `12-17`, `1-16` and `128-143` on a 128-CPU host. In the self-test, `the default geometry is the runner's before #873 ...` (`scripts/act_ci.py:7885`) pins `(4, 16, 8)`, `(16, 12)` and `8g`; `fallback has one named setting` pins 12. M01 (fallback reported as 16), M21 (`8G`), and the author's M12/M13 (default width 8, default memory 4) are each killed.
2. **`--cpu-ranges` refusals hold at every width.** One width-agnostic code path (`scripts/act_ci.py:4832-4854`) does the width check against `JOB_GEOMETRY.get().range_widths`, then alignment, host bound and overlap. Probes at `--job-cpus 6` and `--job-cpus 8` refuse unaligned (`3-8`, `4-11`), repeated (`0-5,6-11,0-5`), beyond-host (`126-131`, `128-135`) and other-width ranges, each for its own reason. Seven ranges for eight jobs are refused (`insufficient CPU ranges: 8 jobs need distinct ranges`). Mutants M06 (alignment only at 16/12), M08 (8 accepts 6), M14 (host bound skipped at 6/8), M20 (overlap dropped) and M24 (6 keeps a 12 fallback) are killed.
3. **Memory bounded by construction, refused before any collaborator.** `JobGeometry.__post_init__` (`scripts/act_ci.py:4760-4786`) refuses `jobs * memory_gib + SLOT_SERVICE_MEMORY_GIB > SLOT_MEMORY_GIB` and `jobs * cpus > REPLAY_CPU_LIMIT`. `main` builds the geometry inside the same `try` as `--cpu-ranges`, before `run_with_cleanup_signals` (`scripts/act_ci.py:17479-17484`). The command-line arms show `reached == []` for the memory, CPU and ninth-job refusals. M04 (inclusive bound), M10 (1 GiB share), M17, M18, M19 and the author's M1-M4 are killed. M10 and the `(5, 6, 7)` arm show the service share is counted. A share of 3 or 2 is an equivalent mutant: no in-range geometry has `jobs * cap` of 33 or 34. The geometry is read only in the main thread. The CPU monitor's reader thread gets its ranges as an argument (`scripts/act_ci.py:5784-5789`), so no thread falls back to the default context value.
4. **The measured basis and the 4 GiB question.** My judgment, from the documented measurements:
   - **Will 4 GiB OOM the jobs that peaked above it?** Not necessarily. But compile-heavy jobs at `--job-cpus 8` are likely to hit it. `memory.peak` counts page cache, which is reclaimed at `memory.max` before any OOM, so #835's 7.8 GiB maximum and 3.4 GiB median do not prove 7.8 GiB of anonymous memory. However, `docs/testing/CI_WORKFLOWS.md:2807-2826` records source builds at 8 compiler processes peaking at 5264482304 B = 4.90 GiB (Yosys) and 4811259904 B = 4.48 GiB (Verilator) under an 8 GiB cap, and Yosys at 16 compilers reaching 8 GiB with 174 limit events. `CI_TOOL_BUILD_JOBS=min(nproc, 8)` is still 8 at `--job-cpus 8`, so a cache-miss source build at 8 x 8 x 4 GiB is the likeliest OOM. At 8 x 6 it runs 6 compilers and is uncertain. Capture (5.632 GiB) cannot be settled offline.
   - **Is that unsafe for what the replay attests?** No. Inside an isolated slot, an OOM at a job's 4 GiB cap is counted by the slice's hierarchical `memory.events` and refuses the run (`valid build: False`, `scripts/act_ci.py:4618-4626`). Reclaim without an OOM can slow a job into a timeout, which is a FAILED the docs already say may be memory's. Neither path can turn a failing candidate into a PASS. Slot 0 still counts no OOM, as documented before this PR. So the 4 GiB opt-in geometry risks refused or failed calibration runs, not weaker positive evidence. The default stays 4 x 16 at 8 GiB.
   - **Should the slot limit rise instead?** Not in this PR. The host's `MemTotal` is 68.9 GiB (72246672 kB, measured on the review host). At 8 GiB per job, 8 jobs need 8 x 8 + 4 = 68 GiB, the whole host. At 6 GiB per job they need 52 GiB, three quarters of it for one slot, which leaves no room for a second slot. The cap is a host-allocation decision outside #873's text. This PR leaves it as one named constant (`SLOT_MEMORY_GIB`, `scripts/act_ci.py:178`) that the geometry bound reads, so a raise is a one-line change once it is decided.
   - **Recommendation for the manager's item 4:** run 8 x 6 at 4 GiB on an isolated slot as specified, and read `slot-memory.json` (`oom`, `oom_kill`, `max`, `peak`). If it is refused for memory, geometries inside 36G remain: 6 x 6 or 6 x 8 at 5 GiB (34 GiB), and 5 x 6 at 6 GiB (34 GiB). Only if those also fail should a slot-cap raise go to the owner, backed by the measured slot peak.
5. **Arms and planted defects.** The 34 new arms are listed in `receipts/new-arms-selftest.txt`. All 623 base arms (621 flat) are present at the head with identical labels once source line numbers are normalised. Their expected values for the default now come from the geometry, which a separate new arm pins to the literal default. That is why the differential probe in item 1 is the stronger evidence. Every one of the 22 published planted defects fails the flat self-test, and 21 of 22 fail with exactly the published FAIL set. M5's extra FAIL was a pre-existing signal-timing arm under 12-way load; it did not reproduce (3 reruns, plus 12/12 loaded runs). My own 24 defects found three gaps, all SUGGESTION (S1-S3). Two of them already exist at the base. None of the three can make a new arm pass for a defect it claims to detect.
6. **Docs.** `docs/testing/CI_WORKFLOWS.md:2272-2283` covers the range width per geometry, the default-only 16/12, the refusals at every width and the #737 reconciliation. Line 2339 covers the admission bound. Lines 2355-2385 cover the two bounds, the 1-8 / 16-8-6 / 1-8 GiB ranges, a five-row table of accepted and refused shapes (each row matches the code and an arm) and the 6-CPU straddle. Lines 2386-2406 give #835's figures, which match the issue body exactly, the unchanged default, the 4 GiB caveat, and the item-4 calibration (8 x 6 against a 4 x 16 receipt, durations, timeouts, wall time, peak memory) with "Until that replay is recorded here, the default does not change". Line 2832 generalises the admission formula. The docs do not say who runs the calibration. That is acceptable for durable docs; the PR body assigns it.

## Findings

### R818-1-F1 RESIDUE (Docs): stale "four-job scheduler" docstring

- Where: `scripts/act_ci.py:5988`, `execute_workflows` docstring: "Run all selected workflows through one four-job scheduler and one cleanup boundary."
- Evidence: the line itself is unchanged, but this delta made its count a parameter. Admission is now `JOB_GEOMETRY.get().jobs` (`scripts/act_ci.py:2145`, `:4947`), 1 to 8.
- Impact: wording only. No behaviour, test or figure changes.
- Exact fix: `"""Run all selected workflows through one scheduler bounded by the job geometry's job count, and one cleanup boundary."""`
- Verification: read the line at the fixed head; the self-test is unaffected.

### R818-1-F2 RESIDUE (Docs): PR body overstates what a real run prints

- Where: PR #875 body, Description, the paragraph after the table: "The printed act command line already shows the geometry."
- Evidence: the act command is printed only under `--dry-run` (`scripts/act_ci.py:6008-6010`). A real run prints `act-ci: slot N: up to <concurrency> concurrent jobs; created directly on reserved CPU ranges: ...` (`:4870`, `:6114`). `cpu-placements.json` records the ranges and `peak_jobs` (`:6033-6035`). No real-run output or evidence file records the per-job memory cap, except the OOM refusal reason (`:4622`).
- Impact: wording in the PR body. No code change is required, because recording the cap in the evidence would change what the replay records, which #873 puts out of scope (see S7).
- Exact fix: replace the sentence with "A `--dry-run` prints the act command with the geometry's words. A real run prints the job count and the booked ranges, and `cpu-placements.json` records the ranges and `peak_jobs`; the per-job memory cap is printed only in an OOM refusal, so a calibration receipt must keep its own command line."
- Verification: read the edited PR body.

### Suggestions (optional; none affects coverage)

- **S1 (Tests):** `job_cpu_ranges`' geometry bound below the 8-job maximum is never exercised. Mutant M09 (`concurrency <= MAX_CONCURRENT_JOBS`) survives, and so does its base twin B09. The cause is that the existing `unsupported job admission width` arm (`scripts/act_ci.py:7866`) accepts any refusal, and count 5 is refused for too few ranges first. Production cannot reach the bound, because concurrency is `min(geometry.jobs, count)`. A useful arm: the default geometry with eight booked 16-CPU ranges on a 128-CPU host, where `job_cpu_ranges(0, 5)` must give exactly `unsupported concurrent job count: 5`.
- **S2 (Tests):** `--concurrent-jobs` being capped by the number of booked ranges (`scripts/act_ci.py:4947`) is never exercised (M02 survives, as does its base twin B02). If the cap were dropped, the pinned dispatcher would refuse the run rather than oversubscribe, so the effect is safe. An arm could still pin it.
- **S3 (Tests):** the slot OOM refusal reason naming the run's per-job cap (`scripts/act_ci.py:4622`) is never exercised at a non-default geometry (M23 survives). It is diagnostic text only.
- **S4 (Docs, pre-existing):** "The host now has 61 GB" (`docs/testing/CI_WORKFLOWS.md:2382`, and "61 GB shared" at `:2719`) is already in the base. The host measures 68.9 GiB `MemTotal`. This bears on any slot-cap decision, so it belongs in a follow-up issue, not this delta.
- **S5 (Docs/Robustness):** the 4 GiB caveat names capture (5.632 GiB) and #835's maximum (7.8 GiB). It could also name the source-build peaks at 8 compilers (4.90 GiB Yosys and 4.48 GiB Verilator; 5264482304 B and 4811259904 B), which apply unchanged at `--job-cpus 8` because `CI_TOOL_BUILD_JOBS` stays `min(nproc, 8)`. The calibration could include a cache-miss source build.
- **S6 (Tests/Robustness):** the generated CPU-budget shell controls run at 1, 4, 12 and 16 CPUs (`docs/testing/CI_WORKFLOWS.md:2335`), not at the newly admitted 6 and 8. The arithmetic is simple and the widths are bracketed, but a 6- and 8-CPU control would cover the new widths. This is outside the runner and would be a follow-up issue.
- **S7 (follow-up issue, outside #873's scope):** record the geometry (jobs, width, per-job cap) in the evidence directory, for example beside `slot_memory`. Then two evidence sets from the same runner digest can be told apart without the operator's own log.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts (at this head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #873 items 1-3 and 5 against `scripts/act_ci.py:107-126,178-180,4743-4867,4903-4952,17357-17370,17465-17484` and `receipts/probe-default.diff`, `receipts/probe-geom-*.log`; item 4 deferred to the manager (pending duty); out-of-scope: `git diff --stat` shows no workflow, dispatcher or evidence-writer change | R818-1 | 88e1041c9b100c389f3629dfcf3185ad3be9c3f4 |
| RTL (here: runner architecture, interfaces, bounds and widths; no HDL in the diff) | CLEAN | `JobGeometry` bounds and integer typing (`scripts/act_ci.py:4760-4786`); contextvar set in the main thread before any collaborator and read only there (`:17480`, `:5784-5789`, `run_with_cleanup_signals`); dispatcher contract `ci/act/cpu_ranges.go:16-65` (width 16 or fallback, alignment, limit vs ranges) against the runner's widths and `MILAN_CI_FALLBACK_CPUS`; slot slice cap unchanged (`:178-180`, `:4403`) | R818-1 | 88e1041c9b100c389f3629dfcf3185ad3be9c3f4 |
| Robustness | CLEAN | refusals at widths 6, 8 and default for missing, malformed, unaligned, repeated, beyond-host, other-width and too-few ranges (`receipts/probe-geom-8x{6,8}-ranges.log`, `receipts/probe-default-head.log`); out-of-range and non-integer geometry; memory/CPU over-subscription before collaborators; `--selftest` with geometry options is a usage error; OOM/reclaim behaviour at a 4 GiB cap (focus item 4); load run `receipts/load/*` | R818-1 | 88e1041c9b100c389f3629dfcf3185ad3be9c3f4 |
| Tests | CLEAN | 657/655 head and 623/621 base self-tests, label diff (0 removed, 34 added), 22 author mutants re-run, 24 own mutants + 2 base twins (`receipts/mutants*.txt`, `receipts/author-mutants-replay.txt`), small-host control, behave 508, 15 docs.yml gates | R818-1 | 88e1041c9b100c389f3629dfcf3185ad3be9c3f4 |
| Docs | CLEAN (two RESIDUE items carried to the manager's checklist) | `docs/testing/CI_WORKFLOWS.md:2272-2283,2335-2340,2355-2406,2807-2833` against the code and issue figures; `--help` text; new source comments checked against the comment rule (no lane labels, review rounds, reviewer IDs or comment IDs on any added line); PR body and issue evidence | R818-1 | 88e1041c9b100c389f3629dfcf3185ad3be9c3f4 |

## Real limits of this round

- No Docker, act, live replay, `--dry-run` against a daemon, slot or sudo. The geometry's effect on act was proved offline on the generated command, as the existing arms prove the default.
- No physical calibration. #873 item 4 is NOT RUN, and nothing here is evidence about wall time, per-job durations, timeouts or slot peak memory at 8 x 6.
- Not every `docs.yml` step was run: 15 gates touching the changed files, plus the act runner contract gate's two self-tests and behave. `scripts/ci_tool_inventory.py --check` is refused at both base and head on this host (`CI_IMAGE_SHFMT must name the checksum-pinned Bash parser`; `receipts/gates/*/tool_inventory.*`). The `scripts/act_ci.py` digest in `ci/image/tool-inventory.json` (`b8a786ce...`) already differs at the base (`3f91c996...`) and still differs at the head (`cb5bb5d5...`). That is pre-existing and checked only by the image build.
- Hosted acceptance belongs to the manager. At the snapshot, 31 contexts were still queued or running.
- Python on this host is 3.14.9. The hosted documentation runner uses 3.12.3.
- One pre-existing signal-timing arm ("a first signal at each of the 185 steps ...") failed once under about 12 concurrent self-tests inside a mutant run. It did not reproduce. Base and head carry the arm unchanged.

## Pending manager duties

- #873 item 4: the 8 x 6 calibration and a 4 x 16 receipt at the same head, through the audited-install bootstrap, because the trusted `dev` runner has no geometry options. Keep the exact invocation in the receipt (F2). Read the slot's OOM counters as in focus item 4.
- The PR says `Closes #873`, but item 4 is not met by the diff. Record the calibration, or otherwise settle item 4 publicly, before the merge closes the issue.
- Decide whether #737's 16-CPU ruling also binds the explicit `--job-cpus 8` and `--job-cpus 6`. The PR reads #873 as the newer decision by the same account and published the question.
- Booking: a 6-aligned range can straddle a 16-CPU boundary (`12-17`). Concurrent replays must get disjoint ranges.
- Hosted exact-head contexts, the current-dev candidate merge validation (builder and native banks), and post-merge containment.
- Residue checklist: F1, F2. Follow-up issues if wanted: S4, S6, S7.
- The docs promise the calibration result will be "recorded here". A later commit to `docs/testing/CI_WORKFLOWS.md` therefore changes the Docs lens's scope, and Docs must be covered again at that head (AGENTS section 7: coverage is banked against a commit).
- The author packet's `author/CALIBRATION.md` (not in the head tree) quotes source-build and census peaks in GB as GiB, for example "Yosys source builds at 5.26 GiB" where 5264482304 B is 4.90 GiB. Correct it before using that plan.

## Prior and concurrent public findings on PR #875

- Before this round, PR #875 carried no review findings, only the two review-start comments. There was nothing to resolve or retain.
- The internal round R817-1 (`[R817] POSITIVE`, issue comment 6765132159) was published during this round. I read it only after the verdict, findings and ledger above were written. Its findings, against mine at this head:

| R817-1 item | Severity there | Status in R818-1 |
|---|---|---|
| S1: no arm books more ranges than `--jobs`, so `--concurrent-jobs`'s range clamp is unpinned (their M07; survives at base) | SUGGESTION | Same as my S2 (M02, base twin B02). Retained as SUGGESTION. |
| S2: the OOM refusal's named cap is pinned only against itself (their M17) | SUGGESTION | Same as my S3 (M23). Retained as SUGGESTION. |
| S3: docs should say an OOM is counted only in an isolated slot, and give the calibration's cap and slot | SUGGESTION | Agreed as SUGGESTION. This round already lists an isolated slot as the calibration's condition (pending duties). |
| S4: link the measured basis to its replay receipt | SUGGESTION | Agreed as SUGGESTION. The figures match the frozen #873 body, which is the authority this PR cites. |
| O1: "The host now has 61 GB" is stale (pre-existing) | observation | Same as my S4. |
| O2: the author's calibration plan quotes GB as GiB | observation | Confirmed. It also caught the same slip in this report's draft (focus item 4 and S5), corrected before publication. Carried as a pending duty above. |

- R817-1 recorded no RESIDUE. This round adds F1 and F2 (RESIDUE) and S1, S5, S6 and S7. No R817-1 item is a BLOCKER, MAJOR or MINOR, and neither round's verdict or lens state conflicts with the other's.

R818-1 FINISHED
