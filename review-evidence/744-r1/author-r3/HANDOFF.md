# HANDOFF: lane 744 (act slot OOM accounting, census jobs bounded by memory)

Role: author [A621]. Branch `744-slot-oom` from `dev` `84f9e300`. Not pushed.
Head: `7997eeb348c3af302079c7273d1b3092eee4dc6c` (round 3). Round 2 head: `43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e`. Round 1 head: `f643377f15c0d939d875ae5698672f1b0a99a644`.

TAKEN: https://github.com/kebag-logic/milan-fpga/issues/744#issuecomment-6197913607
REVIEW READY (round 1): https://github.com/kebag-logic/milan-fpga/issues/744#issuecomment-6198731137
REVIEW READY (round 2): https://github.com/kebag-logic/milan-fpga/issues/744#issuecomment-6200488334
REVIEW READY (round 3): https://github.com/kebag-logic/milan-fpga/issues/744#issuecomment-6202042166

## Round 3

Assignment: the newest [A10] "Round 3 for PR #745" comment on #744 (6200881924), with R636-2 (PR #745 comment 6200869845; its `scripts/sv2v_recount.py` read from the 744 review-evidence branch, `review-evidence/744-r1/reviews/R636-2/`). R637-2 was POSITIVE.

Head: `7997eeb348c3af302079c7273d1b3092eee4dc6c` (five commits on `43a25fa7e`). Not pushed.

| Item | Status |
|---|---|
| 1. R636-2-F1 (Docs MINOR): sv2v counts | done: only log-reproducible counts; "elaborated the full datapath" dropped |
| 2. R636-2-F2: review labels in comments | done: the reviewer's exact texts |
| 3. R636-2-F3: cross-declared-file arms | done: 39 arms, pooled mutant fails exactly those |
| 4. R636-2-F4: refusal reasons | done: every refusing control asserts its last stderr line; two silent refusals got reasons |
| Full docs-gates set on the committed head | done: all 47 steps rc 0 at `7997eeb34` |

### Commits (`43a25fa7e..7997eeb34`)

1. `1996179ab` Say what the host memory reads' gate comments mean without naming the review that decided them
2. `c55f2cf37` Refuse each declared host memory read in every other declared file, so the lines cannot be pooled across files
3. `d0091c29f` Give every census budget refusal its own stated reason and check each control refuses for it
4. `ab7965522` State only the sv2v counts the published per-run log reproduces
5. `7997eeb34` Write the planted cgroup root in the census controls' reasons as a placeholder, not as the host path

Commit 5 fixes commit 3: its reasons spelled the real cgroup root, and the bare-metal gate refused those 9 lines (found by the first full gate run at `ab7965522`, which was stopped; the gate run below is at `7997eeb34`). The fix writes the planted root as `<cgroups>`, so no new host path needs declaring.

### Changes (file:line at `7997eeb34`)

Item 1, R636-2-F1 (`docs/testing/CI_WORKFLOWS.md:2430-2436`):
- "Of those sv2v runs, 10 exited nonzero, 120 peaked at 1168056 to 1212036 KiB, and 20 were above 1205884 KiB. The largest of them, 1212036 KiB, was that run's largest process. `CENSUS_WORKER_BYTES` is the larger of the two runs' largest processes, 1213100 KiB or 1242214400 bytes."
- The round-2 "25 elaborated the full datapath, 23 above 1205884 KiB" was wrong: the log has 20 above 1205884 KiB and 120 at or above 1.0 GB. The log has no criterion for "full datapath", so the phrase is dropped rather than defined.
- Check: the reviewer's `sv2v_recount.py` (sha256 `5615f052...62c4`) on `evidence/r2/sv2v-rss-selftest.log` (sha256 `d91554a6...3f75`) gives 133 runs, 10 nonzero, largest 1212036, 20 above 1205884, 120 at or above 1000000 (`evidence/r3/sv2v-recount.txt`). Its last line is the script's fixed quote of the round-2 doc, not a recount. The "largest process" claims are `Maximum resident set size` 1212036 in `evidence/r2/census-capped-jobs4-selftest-time.txt` and 1213100 in `evidence/census-capped-jobs4-time.txt`.
- PR body: the round-2 R636-3 row is corrected to the same counts, marked "(corrected in round 3)".

Item 2, R636-2-F2 (`scripts/check_baremetal_only.py:359`, `:1283`, `:1293`): the reviewer's exact texts. `git diff 84f9e300 -- scripts .github` has no added line naming a review label, reviewer or comment ID.

Item 3, R636-2-F3 (`scripts/check_baremetal_only.py:1302-1313`):
- Each declared line is planted in every other declared file (variant `declared-file-<file>`) and must be refused there as `[R]` on that line. A `.yml` destination is used only for a line that starts with a space, because only an indented line sits unchanged in the workflow's `run: |` block scalar. An assertion checks that each line has at least one destination and is not itself declared there.
- 39 new arms (act_ci.py 14, ci_runtime_workflows.py 7, rtl-fast.yml 9, ci_gate_workflows_selftest.py 9): 829 in total.
- Mutant "every declared line pooled into each declared file's mask": `--selftest` rc 2, exactly the 39 `declared-file-` arms not caught, no other arm (`evidence/r3/baremetal-pooled-mutant.txt`).
- `docs/testing/CI_WORKFLOWS.md:2367-2369`: "the same line in another file, including another declared one, or in a product document are still refused".

Item 4, R636-2-F4:
- `scripts/ci_runtime_workflows.py:61,63` (generated `.github/workflows/rtl-fast.yml:436,438`): zero CPUs and a missing `MemTotal` used to refuse through a bare `test` with no reason of their own (zero CPUs printed nothing). They now print `no CPUs: nproc printed <n>` and `no MemTotal in kB`. Neither line names a host path. The workflow was regenerated with `python3 scripts/ci_gate_workflows.py`.
- `scripts/ci_gate_workflows_selftest.py:235` `census_budget` returns `(jobs or None, stderr lines)`, with the planted cgroup root written `<cgroups>` (`:272`).
- `:295` `census_controls`: each refusing case names its reason, and asserts rc nonzero, no export and that reason as the last stderr line (`:339`). Each passing case asserts its worker count and no stderr (`:335`).
- `docs/testing/CI_WORKFLOWS.md:2048-2049`: "each refusal must print its own reason as the step's last error line".
- Budget-shell mutants (`evidence/r3/budget-reason-mutants.txt`), all caught:

  | Mutant | Caught by |
  |---|---|
  | `cat` failure ignored (`&& false`) | `a mode-000 limit`: refused as non-numeric, not unreadable |
  | `cat` failure ignored (`\|\| true`) | same |
  | zero-CPU reason dropped | `zero CPUs`: no stderr |
  | MemTotal reason dropped | `no MemTotal`: only `test`'s own error |
  | unsearchable-cgroup refusal dropped | `a mode-000 ancestor cgroup`: 16 workers |

  The first two are R636-2-F4's outcome-equivalent mutant; they are now caught by reason.

### act_ci.py SHA-256 at `7997eeb34`

Unchanged in round 3: `b8a786cec30be9eff9f2e72c6b59e21c06d27e1f36e055a7929c3cc3b59e3ba8`, 698735 bytes, mode 755.

### Measured sv2v peak and jobs formula

Unchanged from round 2 (below): `CENSUS_WORKER_BYTES = 1242214400` (1213100 KiB), `CI_CENSUS_JOBS = max(1, min(nproc, floor(2 * M / (3 * 1242214400))))`. Round 3 adds two refusal reasons, not a new bound.

### Gates at `7997eeb34`

Every `run` step of the `docs` workflow's gate jobs ran on the committed head `7997eeb34` with a clean tree, in the same order, environment and substitutions as round 2 (below), one log and rc per step (`evidence/r3/docs-gates-7997eeb/`). All 47 exited 0. `git status` was empty before and after, and the submodules stayed at their gitlinks.

| # | Step (job/index name) | rc | time |
|---|---|---:|---:|
| 01 | docs-gates-0/3 Build the validated HDL reference | 0 | 2s |
| 02 | docs-gates-0/11 Link health, wording, dead-reference and local-info gate | 0 | 6s |
| 03 | docs-gates-0/12 Added-line em-dash gate | 0 | 3s |
| 04 | docs-gates-0/13 Concise audience documentation gate | 0 | 1s |
| 05 | docs-gates-0/14 Audience diagram no-drift gate | 0 | 2s |
| 06 | docs-gates-0/15 Product solution source-fact gate | 0 | 3s |
| 07 | docs-gates-0/16 Verified submodule documentation gate | 0 | 2s |
| 08 | docs-gates-0/17 HDL timing diagram no-drift gate | 0 | 1s |
| 09 | docs-gates-0/18 Published diagram PNG gate | 0 | 15s |
| 10 | docs-gates-0/19 Milan feature-status consistency gate | 0 | 1s |
| 11 | docs-gates-0/20 Traceability matrix no-drift gate | 0 | 1s |
| 12 | docs-gates-0/21 Fetch the builder source dependencies | 0 | 0s |
| 13 | docs-gates-0/22 Imported gPTP documentation gate | 0 | 1s |
| 14 | docs-gates-0/23 Code-quality measurement self-tests | 0 | 0s |
| 15 | docs-gates-0/25 Install the pinned sv2v release (local pin check) | 0 | 0s |
| 16 | docs-gates-0/26 Bare-metal scope gate | 0 | 31s |
| 17 | docs-gates-0/28 Install and verify the pinned RV32 SDK | 0 | 25s |
| 18 | docs-gates-0/29 Compiler-absent firmware controls | 0 | 517s |
| 19 | docs-gates-0/30 NVM record-space gate | 0 | 46s |
| 20 | docs-gates-0/31 Capture measurement census and clock gate | 0 | 1s |
| 21 | docs-gates-0/32 Saved-state writer gate | 0 | 249s |
| 22 | docs-gates-0/33 SoC source-list gate | 0 | 3s |
| 23 | docs-gates-0/34 RTL source-list drift gate | 0 | 4s |
| 24 | docs-gates-0/35 Boundary-unit naming ratchet | 0 | 2s |
| 25 | docs-gates-0/36 Port contract gate | 0 | 6s |
| 26 | docs-gates-0/37 Fail-fast ratchet | 0 | 3s |
| 27 | docs-gates-0/38 TODO ownership gate | 0 | 4s |
| 28 | docs-gates-0/39 Test-evidence ratchet | 0 | 21s |
| 29 | docs-gates-0/40 Mechanical hygiene ratchet | 0 | 0s |
| 30 | docs-gates-0/41 SystemVerilog idiom gate | 0 | 1s |
| 31 | docs-gates-0/42 C and C++ idiom gate | 0 | 3s |
| 32 | docs-gates-0/43 Python idiom gate | 0 | 11s |
| 33 | docs-gates-0/44 Shell idiom gate | 0 | 0s |
| 34 | docs-gates-0/45 Doc cited-path gate | 0 | 1s |
| 35 | docs-gates-0/46 Archive integrity gate | 0 | 0s |
| 36 | docs-gates-0/47 Per-page contents gate | 0 | 12s |
| 37 | docs-gates-0/48 AEM store generator self-test | 0 | 0s |
| 38 | docs-gates-0/49 Sweep/build shape gate | 0 | 14s |
| 39 | docs-gates-0/50 Deploy shape gate | 0 | 0s |
| 40 | docs-gates-0/51 Entity shape gate | 0 | 52s |
| 41 | docs-gates-0/52 Fetch inventory dependencies | 0 | 0s |
| 42 | docs-gates-0/53 CI scheduling and evidence controls | 0 | 27s |
| 43 | docs-gates-2/15 CI event and SHA contract gate | 0 | 219s |
| 44 | docs-gates-2/16 Local act runner contract gate | 0 | 122s |
| 45 | docs-check-no-git/3 Strip git metadata, then run the docs gate | 0 | 7s |
| 46 | docs-gates-1/14 End-station builder gates, leg 0 of 2 | 0 | 965s |
| 47 | docs-gates-2/14 End-station builder gates, leg 1 of 2 | 0 | 367s |

Key results:
- 16: `baremetal-only: OK (0 findings across 1344 tracked first-party file(s))`, `selftest: PASS (829 arm(s))`.
- 42: `ci_gate_workflows.py --check` rc 0; 16 `Census budget:` cases, each refusal with its reason, none skipped (not root).
- 43: `ci_events.py --selftest`: `PASS (2187 contract items, 5218 arms)` (log 335095 bytes; sha256 in `large-logs.sha256`).
- 44: runner self-test `selftest: PASS` direct and isolated (`act_ci.py` unchanged this round).
- 45: `docs_check: 0 finding(s)` and `feature_status: 0 finding(s)` without `.git`.
- 46, 47: builder legs `ALL GATES PASS` and `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11's real-report calibration arm, as in round 2), rc 0.
- 03: `check_em_dash`: 0 findings over 122 added lines.

An earlier full run at `ab7965522` was stopped at step 18 after step 16 failed with 9 findings in commit 3's reasons; commit 5 fixed them and the run above is the complete one.

## Round 2

Assignment: the newest [A10] "Round 2 for PR #745" comment on #744 (6199231775), with M1 (PR #745 comment 6199082046), R636-1 (6199187632) and R637-1 (6199224923).

Head: `43a25fa7eba4d7ed7d2bb757aa42b973bd24c76e` (four commits on `f643377f1`). Not pushed.

| Item | Status |
|---|---|
| 1. Bare-metal gate (M1 = R636-1 BLOCKER = R637-1-F2) | done: declared by whole line and file, prose reworded, negative controls; `--check` 0 findings, `--selftest` 790 arms |
| 2. R637-1-F1, an unreadable limit | done: present but unreadable `memory.max` (leaf or ancestor) or an unsearchable cgroup refuses before `CI_CENSUS_JOBS`; mode-000 controls |
| 3. R636-2 RESIDUE | done, the reviewer's exact texts |
| 4. R636-3 | done: measured over the self-test arms; constant 1213100 KiB = 1242214400 bytes |
| 5. R636-4 | done: `valid_build` is `oom_free` |
| Full docs-gates set on the committed head | done: all 47 steps rc 0 at `43a25fa7e` |

### Commits (`f643377f1..43a25fa7e`)

1. `1cb7f19bd` Refuse a census memory limit that is present but unreadable, at the job's cgroup or any ancestor, with mode-000 controls
2. `597c43f92` Declare the host memory reads in the bare-metal gate as whole lines in their files, and reword the prose that only needed the word
3. `dcd4d98ae` Name the slot evidence field oom_free for what it decides, and say the manifest's completeness does not read the slot's memory events
4. `43a25fa7e` Set the census worker peak to 1213100 KiB, the largest sv2v measured over the self-test's arms as well as the shapes

### Changes (file:line at `43a25fa7e`)

Item 1, bare-metal gate (M1's ruling):
- `scripts/check_baremetal_only.py:367` `HOST_MEMORY_READS`: the 14 declared lines, by file. `scripts/act_ci.py` has 5: `PROC_MOUNTS`, the two `SLOT_MOUNTS` fixture lines, and the two lines of the no-cgroup2-mount case. `scripts/ci_runtime_workflows.py` has 3: `MemTotal`, the cgroup path, and the walk's stop. `.github/workflows/rtl-fast.yml` has the same 3 at their generated indentation. `scripts/ci_gate_workflows_selftest.py` has 3: the planted-path substitutions.
- `:393` `declared_line_mask`: each `/proc` or `/sys` token in a declared line becomes `(?<=^<text before>)<token>(?=<text after>$)`. That is the whole line, the same form as #532's `ACT_SLOT_TERM_CONTEXTS`.
- `:400` `with_declared_lines`, `:409`: these are merged into `HOST_RUNTIME_MASKS`, after the existing `scripts/act_ci.py` expression.
- `:56-59` the class-R docstring names the table.
- `:1274` `_arms_host_memory_reads`, registered at `:1712`:
  - every declared file's lines together are clean at home;
  - M1's negative control: `cat /proc/cpuinfo`, `ls /sys/class/net` and `the target kernel`, each appended to each declared file (and to `docs/testing/CI_WORKFLOWS.md`'s existing masked line), is refused as `[R]` on exactly that line;
  - every declared line is refused in another file, in the product document, with `# ` before it, with text after it, and with a different path in its own context.
  - 90 new arms, 790 in total.
- Prose that only needed the word was reworded:
  - `scripts/act_ci.py:7012,13305,14758,14760`: "a real kernel's" became "a real host cgroup's";
  - `docs/testing/CI_WORKFLOWS.md:2515`: "kernel OOM kills" became "OOM kills";
  - `:2532`: "a real host cgroup's events";
  - `:2039-2044`: "planted meminfo and cgroup files".
- `docs/testing/CI_WORKFLOWS.md:2357-2367`: the bare-metal policy paragraph now names `HOST_MEMORY_READS`, its four files and what is still refused. The paragraph before it said host literals were masked only in `scripts/act_ci.py`.
- Mask mutants (`evidence/r2/baremetal-mask-mutants.txt`), all caught:

  | Mutant | Caught by |
  |---|---|
  | table not merged | `--check` (14 findings) and `--selftest` |
  | token masked anywhere in the file | `--selftest` |
  | prefix not anchored to the line start | `--selftest` (`-prefixed`) |
  | suffix not anchored to the line end | `--selftest` (`-trailing`) |
  | path component masked to the end of the line | `--selftest` |
  | one declared runner line dropped | `--check` (`scripts/act_ci.py:4618`) |

Item 2, R637-1-F1 (`scripts/ci_runtime_workflows.py:54-88`, generated at `.github/workflows/rtl-fast.yml:432-463`):
- `:68-70`: a cgroup directory on the walk that exists but cannot be searched refuses: "unsearchable cgroup ...: its memory limit cannot be proved absent".
- `:71-75`: `[ -e memory.max ]` replaces `[ -r memory.max ]`. A present file that `cat` cannot read refuses ("unreadable memory limit in ..."). Only an absent file means no limit there.
- `:77`: a non-numeric or empty limit still refuses, now worded "non-numeric memory limit".
- `scripts/ci_gate_workflows_selftest.py:235` `census_budget(..., denied)`: makes a planted limit mode 000, a planted cgroup directory mode 000, or a planted `memory.max` a directory. Modes are restored after the run.
- `:279` `mode_zero_denies`: probes whether mode 000 denies this process. Root's CAP_DAC_OVERRIDE reads through it, so as root the three mode-000 cases print `LOUD SKIP`, the precedent in `check_baremetal_only.py`'s `[unreadable-file]` arm. Hosted runners run as an unprivileged user.
- `:293` `census_controls`: 16 cases. The readable 8 GiB limit gives 4, and the readable 4 GiB ancestor gives 2, both unchanged. New: a mode-000 limit, a mode-000 ancestor limit, a mode-000 ancestor cgroup, a limit that is a directory, and an ancestor limit that is a directory all refuse. The readable-garbage case keeps its control of the non-numeric branch, renamed "a non-numeric limit" so it no longer claims to test unreadability.
- `docs/testing/CI_WORKFLOWS.md:2037-2049`: the contract says the same.
- Budget-shell mutants (`evidence/r2/budget-shell-mutants.txt`):
  - the round-1 `-r` test: caught (`a mode-000 limit` gives 16);
  - no unsearchable-directory refusal: caught (`a mode-000 ancestor cgroup` gives 16);
  - `cat` failure swallowed: still refuses, because the empty result meets the non-numeric branch. This mutant is equivalent in outcome.
- Real caps, using the head's emitted step (`evidence/r2/budget-step-real-caps-head.txt`): 8G scope 4, 4G scope 2, 2G scope 1, this 16 GiB unit 9.

Item 3, R636-2 (`docs/testing/CI_WORKFLOWS.md`):
- `:2016-2017`: "`slot-memory.json` retains an isolated slot's memory accounting and whether an OOM invalidated it."
- `:2522-2523`: "The manifest's completeness does not read the slot's memory events, so `slot-memory.json` and the exit status 2 carry an OOM's invalidity."
- The PR body bullet now uses the reviewer's text, "its completeness does not read the slot's memory events".

Item 4, R636-3 (`scripts/ci_runtime_workflows.py:47-51`; `.github/workflows/rtl-fast.yml:459`; `docs/testing/CI_WORKFLOWS.md:2033,2416-2433`):
- `CENSUS_WORKER_BYTES = 1242214400` (1213100 KiB), up from 1234825216 (1205884 KiB).
- The census was measured under the job container's bound:

  ```sh
  systemd-run --user --scope -q -p MemoryMax=8G -p MemorySwapMax=0 -p OOMPolicy=continue \
    capped.sh run.sh
  ```

  `run.sh` runs the emitted budget step, then the emitted census command, `python3 sw/mailbox/publication_census.py --check --selftest --jobs "$CI_CENSUS_JOBS"`, with `SV2V` and `YOSYS` set to shims that run `/usr/bin/time -a -o <log> -f "%M KiB %e s ..."` around the pinned binaries (`evidence/r2/census-run.sh`, `evidence/r2/shim-sv2v`).
- Result (`evidence/r2/census-capped-jobs4-selftest.txt`, `-time.txt`):
  - 4 workers of 16 CPUs;
  - 234 checks, 0 failures; 0 of 120 arms failed; 0 of 31 rules unproved;
  - scope peak 5569384448 bytes, every `memory.events` counter 0; 12:40 wall.
- sv2v ran 133 times (`evidence/r2/sv2v-rss-selftest.log`). 25 of those runs elaborated the full datapath, at 1.0 to 1.21 GB. 23 were above the round-1 constant, and the largest was 1212036 KiB. Ten exited 1, the arms that plant broken sources.
- Yosys ran 141 times, peaking at 380492 KiB.
- Round 1's capped `--check --selftest --jobs 4` reported "Maximum resident set size 1213100 KiB" for its largest descendant (`evidence/census-capped-jobs4-time.txt`). Yosys and the driver are far smaller, so that was an sv2v run. The constant is the larger of the two arm figures, 1213100 KiB.
- That run's budget step was emitted before the constant changed. At the new constant the step gives the same 4 at 8 GiB (`evidence/r2/budget-step-real-caps-head.txt`).
- Bound check: `4 * 3 * 1242214400 = 14906572800 <= 2 * 8 GiB < 5 * 3 * 1242214400`. The hosted runner's 16765378560 bytes give 8, capped at 4 CPUs.

Item 5, R636-4 (`scripts/act_ci.py:4609-4612`, the self-test at `:7021,7028`; `docs/testing/CI_WORKFLOWS.md:2518-2521`):
- `slot-memory.json`'s `valid_build` is now `oom_free`, and its docstring says it records only that no OOM invalidated the slot.
- The printed `valid build: False` line stays: #744 item 1 names that text.

### Formula at the head

`CI_CENSUS_JOBS = max(1, min(nproc, floor(2 * M / (3 * 1242214400))))`. M is the smaller of `MemTotal` and every numeric `memory.max` from the job's cgroup up to the root it can see. A present but unreadable `memory.max`, an unsearchable cgroup on the walk, a non-numeric limit, a missing `MemTotal` or zero CPUs refuse before the export.

### act_ci.py SHA-256 at `43a25fa7e`

`b8a786cec30be9eff9f2e72c6b59e21c06d27e1f36e055a7929c3cc3b59e3ba8`, 698735 bytes, mode 755. At round 1 (`f643377f1`) it was `9ce3a660...ffee8`; dev's is `7ff18c6a...46fd`.

### Gates at `43a25fa7e`

Every `run` step of the `docs` workflow's gate jobs ran on the committed head with a clean tree, in order, one log and rc per step (`evidence/r2/docs-gates-43a25fa/`). The jobs are `docs-gates-0` steps 3 to 53, `docs-gates-1` and `docs-gates-2` steps 14 to 16, and `docs-check-no-git` in a `git archive` tree without `.git`.

- Environment: CPython 3.12.3 venv with PyYAML 6.0.2, the pinned Markdown renderer, `tools/hdl_reference/requirements.txt` (hash-locked) and wavedrom 2.0.3.post3 (`pip-freeze.txt`); the pinned sv2v binary (sha256 checked by step 15); Yosys 0.66.
- Not run locally:
  - The steps that install onto the runner (pip, apt, sv2v unzip) are replaced by the environment above.
  - The SDK installer ran against a new scratch destination, as its docstring requires for local runs ("SDK fresh installation: verified").
  - The builder legs used the SDK already at the path the builder hard-codes.
  - `docs-check` verifies the hosted jobs' uploaded receipts, so it runs only hosted.
- `git status` was empty before and after the run, and the submodules stayed at their gitlinks (`status-before`, `status-after`, `submodules-after`).
- Leg 1 is `ALL GATES PASS EXCEPT 1 NOT RUN`, rc 0. The arm not run is gate 11's real-report calibration arm, which needs a local FPGA build tree that this host and the hosted runners lack. Its `disabled-writer ... FAIL` lines are the planted-mutant controls, which it reports "caught in both states".

| # | Step (job/index name) | rc | time |
|---|---|---:|---:|
| 01 | docs-gates-0/3 Build the validated HDL reference | 0 | 2s |
| 02 | docs-gates-0/11 Link health, wording, dead-reference and local-info gate | 0 | 5s |
| 03 | docs-gates-0/12 Added-line em-dash gate | 0 | 3s |
| 04 | docs-gates-0/13 Concise audience documentation gate | 0 | 1s |
| 05 | docs-gates-0/14 Audience diagram no-drift gate | 0 | 2s |
| 06 | docs-gates-0/15 Product solution source-fact gate | 0 | 3s |
| 07 | docs-gates-0/16 Verified submodule documentation gate | 0 | 2s |
| 08 | docs-gates-0/17 HDL timing diagram no-drift gate | 0 | 1s |
| 09 | docs-gates-0/18 Published diagram PNG gate | 0 | 14s |
| 10 | docs-gates-0/19 Milan feature-status consistency gate | 0 | 1s |
| 11 | docs-gates-0/20 Traceability matrix no-drift gate | 0 | 1s |
| 12 | docs-gates-0/21 Fetch the builder source dependencies | 0 | 0s |
| 13 | docs-gates-0/22 Imported gPTP documentation gate | 0 | 1s |
| 14 | docs-gates-0/23 Code-quality measurement self-tests | 0 | 0s |
| 15 | docs-gates-0/25 Install the pinned sv2v release (local pin check) | 0 | 0s |
| 16 | docs-gates-0/26 Bare-metal scope gate | 0 | 28s |
| 17 | docs-gates-0/28 Install and verify the pinned RV32 SDK | 0 | 25s |
| 18 | docs-gates-0/29 Compiler-absent firmware controls | 0 | 491s |
| 19 | docs-gates-0/30 NVM record-space gate | 0 | 42s |
| 20 | docs-gates-0/31 Capture measurement census and clock gate | 0 | 1s |
| 21 | docs-gates-0/32 Saved-state writer gate | 0 | 181s |
| 22 | docs-gates-0/33 SoC source-list gate | 0 | 3s |
| 23 | docs-gates-0/34 RTL source-list drift gate | 0 | 5s |
| 24 | docs-gates-0/35 Boundary-unit naming ratchet | 0 | 1s |
| 25 | docs-gates-0/36 Port contract gate | 0 | 6s |
| 26 | docs-gates-0/37 Fail-fast ratchet | 0 | 4s |
| 27 | docs-gates-0/38 TODO ownership gate | 0 | 4s |
| 28 | docs-gates-0/39 Test-evidence ratchet | 0 | 22s |
| 29 | docs-gates-0/40 Mechanical hygiene ratchet | 0 | 1s |
| 30 | docs-gates-0/41 SystemVerilog idiom gate | 0 | 1s |
| 31 | docs-gates-0/42 C and C++ idiom gate | 0 | 3s |
| 32 | docs-gates-0/43 Python idiom gate | 0 | 11s |
| 33 | docs-gates-0/44 Shell idiom gate | 0 | 0s |
| 34 | docs-gates-0/45 Doc cited-path gate | 0 | 0s |
| 35 | docs-gates-0/46 Archive integrity gate | 0 | 1s |
| 36 | docs-gates-0/47 Per-page contents gate | 0 | 11s |
| 37 | docs-gates-0/48 AEM store generator self-test | 0 | 0s |
| 38 | docs-gates-0/49 Sweep/build shape gate | 0 | 11s |
| 39 | docs-gates-0/50 Deploy shape gate | 0 | 0s |
| 40 | docs-gates-0/51 Entity shape gate | 0 | 48s |
| 41 | docs-gates-0/52 Fetch inventory dependencies | 0 | 0s |
| 42 | docs-gates-0/53 CI scheduling and evidence controls | 0 | 28s |
| 43 | docs-gates-2/15 CI event and SHA contract gate | 0 | 218s |
| 44 | docs-gates-2/16 Local act runner contract gate | 0 | 101s |
| 45 | docs-check-no-git/3 Strip git metadata, then run the docs gate | 0 | 6s |
| 46 | docs-gates-1/14 End-station builder gates, leg 0 of 2 | 0 | 877s |
| 47 | docs-gates-2/14 End-station builder gates, leg 1 of 2 | 0 | 379s |

Key results:
- 16: `baremetal-only: OK (0 findings across 1344 tracked first-party file(s))`, `selftest: PASS (790 arm(s))`.
- 42: `ci_gate_workflows.py --check` rc 0; 16 `Census budget:` cases, none skipped (not root).
- 43: `ci_events.py --selftest`: `PASS (2187 contract items, 5218 arms)`. The full log is 335095 bytes, so only its sha256 is in `large-logs.sha256`, and its last line is in `43.tail.log`.
- 44: runner self-test `selftest: PASS` direct (610 ok) and isolated (608 ok).
- 45: `docs_check: 0 finding(s)` and `feature_status: 0 finding(s)` without `.git`.

### Notes for the re-review

- The bare-metal declarations are content-bound: editing any declared line (including regenerating `rtl-fast.yml` with different indentation) fails `--check` until the table is updated with it.
- The mode-000 cases cannot deny root. In an act job container (root) they print `LOUD SKIP`; the directory-as-limit cases still refuse there. Hosted runners run them for real.
- The four-job act replay at this head is the manager's item-2 receipt.

## Round 1 status

- [x] Item 1: truthful slot accounting (`scripts/act_ci.py`), with planted and native controls
- [x] Item 2, author part: census `--jobs` bounded by memory in the generator, template and contract; regenerated; per-sv2v peak measured natively; the bounded census passes under an 8 GiB cap
- [ ] Item 2, receipt: the full four-job act replay at this head is the manager's (not run here: Docker and act are out of this lane's authority)
- [x] Item 3: new `act_ci.py` SHA-256 below; `docs/testing/CI_WORKFLOWS.md` updated for both behaviours
- [x] Every touched gate rc 0 at the head (table below)
- PR body uses "Relates to #744" because the item 2 replay receipt is still outstanding.

## Commits (84f9e300..f643377f1)

1. `f049d579e` Refuse a replay on any OOM in its slot, read from the slice's hierarchical memory events before teardown
2. `9a706ef27` Bound the publication census workers by the job's memory and a measured sv2v peak, never above nproc
3. `f643377f1` Document the slot's hierarchical OOM accounting and the census memory bound with their measurements

## Changes (file:line at the head)

Item 1, runner:
- `scripts/act_ci.py:151-162` `SLOT_MEMORY_MAX` comment: what is refused now.
- `scripts/act_ci.py:4567` `SlotMemory`: `oom`, `oom_kill`, `max`, `peak`; `exhausted` = `oom or oom_kill`; `report()`, `refusal()` (contains "valid build: False"), `evidence()`.
- `scripts/act_ci.py:4617` `LOCAL_EVENTS_OPTION`, `PROC_MOUNTS`.
- `scripts/act_ci.py:4621` `read_slot_memory`: reads `/proc/self/mounts` (exactly one cgroup2 mount at `/sys/fs/cgroup`, refused if it carries `memory_localevents`), then the slice's hierarchical `memory.events` (`oom`, `oom_kill`, `max` required), then `memory.peak` (unreadable gives "unrecorded"). Replaces `require_slot_memory_cap_unexhausted`, which read `memory.events.local`.
- `scripts/act_ci.py:4654` `report_slot_memory_beside`: prints the accounting next to a body's exception without replacing it.
- `scripts/act_ci.py:4664` `replay_slot` now yields the slot's meter (`lambda: None` for slot 0); `:4697` the yield; on a body exception it prints the accounting and re-raises; on return it prints the accounting and refuses when exhausted, all before `release_replay_slot` removes the slice.
- `scripts/act_ci.py:5735` `WorkflowPlan.slot_memory`.
- `scripts/act_ci.py:5943-5954` `execute_workflows`: after container and volume cleanup, reads the meter, writes `slot-memory.json` into the evidence directory, emits the manifest, then on any OOM prints `...; valid build: False` and raises the Refusal (rc 2), whatever act returned.
- `scripts/act_ci.py:6001`, `:6026` `run_validation` passes the meter into the plan.
- Self-test: `:13300` `SLOT_MOUNTS`, `:13307` `OOM_KILLED_EVENTS` (real kernel text, verbatim, from a capped scope here); `FakeSlotHost` serves `memory.events`, a clean `memory.events.local`, `memory.peak`, the mount table; `:13593` `SLOT_TEARDOWN_KINDS`; `:6991` `selftest_slot_memory_evidence` (planted kill through `run_validation`/`execute_workflows` to the refusal and `slot-memory.json`); `:14734` `selftest_slot_memory_cap` (refusals); `:14813` `selftest_slot_memory_report` (reports, body exceptions). `PlantedRun` gained `slot_memory` and `evidence_directory`; `run_workflow_control` patches `replay_slot` and `emit_local_manifest` for it.

Item 2, census bound:
- `scripts/ci_runtime_workflows.py:50` `CENSUS_WORKER_BYTES = 1234825216`; `:53` `census_budget_step()`; `:90` `instrument()` inserts it after the CPU budget step in any job whose steps name `$CI_CENSUS_JOBS` (today only `publication-census`).
- `.github/ci-templates/rtl-fast.yml:255` comment, `:316` census command `--jobs "$CI_CENSUS_JOBS"`.
- `scripts/ci_events.py:2476` the source contract's census command, same change.
- `.github/workflows/rtl-fast.yml:432` generated step, `:546` census command (regenerated by `python3 scripts/ci_gate_workflows.py`; step ids after it shift by one).
- `scripts/ci_gate_workflows_selftest.py:235` `census_budget`, `:266` `census_controls`, `:489` called from `main`.

Docs:
- `docs/testing/CI_WORKFLOWS.md:310`, `:318-321` census job paragraph; `:2016` `slot-memory.json`; `:2026-2042` the bound and its controls; `:2390-2412` the measurements; `:2480-2525` the OOM accounting; `:2785-2788` the CI-event arm count (5,215 at `84f9e300`, 5,218 here).
- `docs/design/MAILBOX_SPLIT.md:1033` census parallelism.

## Measured sv2v peak

At the `84f9e300` datapath, CPython 3.12.3, sv2v v0.0.12 (binary sha256 `b29952bc8f400ca90207507db0ff6763263e03d3eec711da80338430ed636b9b`), Yosys 0.66:

```sh
SV2V=<shim: /usr/bin/time -a -o sv2v-rss.log -f "%M KiB %e s sv2v" <pinned sv2v> "$@"> \
YOSYS=<same shim around yosys> \
/usr/bin/time -v python3 sw/mailbox/publication_census.py --check --jobs 1
```

- sv2v per shape (six shapes): 1203800, 1202864, 1185428, 1203776, 1205884, 1167000 KiB (plus 15828 KiB for `--version`). Largest 1205884 KiB = 1234825216 bytes, which is `CENSUS_WORKER_BYTES`.
- Yosys: largest 386824 KiB. Whole run: Maximum resident set size 1205884 KiB, 3:54 wall, exit 0, 234 checks, 0 failures.
- Files: `evidence/sv2v-rss.log`, `evidence/yosys-rss.log`, `evidence/census-jobs1-time.txt`.

## Jobs bound formula

`CI_CENSUS_JOBS = max(1, min(nproc, floor(2 * M / (3 * 1234825216))))`, where M is the smaller of `MemTotal` and every numeric `memory.max` from the job's own cgroup (`/proc/self/cgroup`) up to the root it can see. One third of M is headroom for the driver, the Yosys after each sv2v and the page cache. A non-numeric limit, a missing `MemTotal` or zero CPUs fail the step.

- act job container, 8 GiB, 16 CPUs: 4. Hosted runner, 16 GiB RAM, 4 CPUs, no cgroup limit: 4 (unchanged from today's `CI_CAMPAIGN_JOBS`).
- Executed natively under a real cap, the generated step (`evidence/budget-step-as-executed.sh`, byte-identical to the committed step) printed `census workers: 4 of 16 CPU(s) within 8589934592 bytes of memory`.
- Bounded census under `systemd-run --user --scope -p MemoryMax=8G -p MemorySwapMax=0 -p OOMPolicy=continue` (the job container's bound): the generated census command passed 234 checks with 0 failures, 0 of 120 arms failed, 0 of 31 rules unproved, in 591 s. Scope peak 5806784512 bytes (67.6% of 8 GiB). `memory.events` all zero (`max 0 oom 0 oom_kill 0`). Files: `evidence/census-capped-jobs4.txt`, `evidence/census-capped-jobs4-time.txt`.
- Negative control, same cap, `--jobs 16`: 113 of 120 arms failed with `sv2v ... exit -9`, scope `oom 2298 oom_kill 209 max 111756`, peak 8589934592 (at the cap). This is #742 reproduced natively. File: `evidence/census-capped-jobs16.txt`.
- The scope ran beside this unit, not inside it: the unit's cgroup is not delegated. Its own 8 GiB cap bounded it. This unit stayed far below 13 GB.

## Slot accounting: fields read and the planted control

- Read, in order, before teardown: `/proc/self/mounts` (cgroup2 at `/sys/fs/cgroup`, no `memory_localevents`), `<slice>/memory.events` fields `oom`, `oom_kill`, `max`, then `<slice>/memory.peak`. `memory.events.local` is no longer read.
- Invalid when `oom > 0` or `oom_kill > 0`, whatever act returned. The evidence directory gets `slot-memory.json` (`{"slot", "memory_max", "peak", "max", "oom", "oom_kill", "valid_build"}`), the runner prints `act-ci: slot N: memory peak ...; K OOM kill(s) and E OOM event(s) in the slot; valid build: False`, and exits 2 with the refusal naming both counts.
- Planted controls, runner self-test:
  - #742 shape: hierarchical `oom 210 oom_kill 210` beside clean local events, every job passing. Refused by count.
  - Real kernel fixture `OOM_KILLED_EVENTS`, with RC_OK and with RC_FAILED. Refused.
  - OOM without a kill, kill without an OOM event. Refused.
  - Five malformed or missing event inputs, an unreadable mount table, no cgroup2 mount, a `memory_localevents` mount. Refused as unprovable.
  - Unreadable peak reported as unrecorded. A FAILED run at a limit without an OOM keeps FAILED.
  - Body exceptions keep their own exception, with the accounting printed beside them.
  - `selftest_slot_memory_evidence` drives the real-kernel kill through `run_validation` to the refusal, the `valid build: False` line and `slot-memory.json` with `valid_build: false`, with act rc 0 and rc 3. A clean slot keeps PASS.
- Mutants (each run through the full isolated self-test at the head's `act_ci.py`; all caught; `evidence/mutants.txt`):

  | Mutant | Failing arms |
  |---|---:|
  | m1: read `memory.events.local` | 18 |
  | m2: no evidence-path refusal | 2 |
  | m3: no slot-exit refusal | 5 |
  | m4: `exhausted` ignores `oom` | 1 |
  | m5: no `memory_localevents` guard | 1 |
  | m6: no report beside an exception | 3 |
  | m7: refusal before the manifest | 2 |
- Native kernel control (`evidence/real-control.txt`):
  - Setup: a 400 MiB allocation in a 200 MiB, no-swap scope below a 36G user slice. Killed, rc 137.
  - Slice `memory.events`: `max 35 oom 1 oom_kill 1`. Slice `memory.events.local`: all zero.
  - dev's reader on that slice: `memory peak 0.2 GiB of its 36G cap; the cap was hit 0 time(s), with no OOM at it`. That is the false line from #742.
  - This head's reader: `1 OOM kill(s) and 1 OOM event(s) in the slot; exhausted=True`, with the refusal text and `valid_build: False`.

## act_ci.py SHA-256

`9ce3a6604486c99209333430b09f8892bc2a5c0f5ed87b052a2ddc85577ffee8`, 698675 bytes, at `f643377f1`. The dev and #739 pin was `7ff18c6a89aeb40c54d44411ffc6ff766fe6aa0f29baf595ba1e2aa833a446fd`. No file in the repository pins the runner digest.

## Gates (all rc 0 at `f643377f1`, CPython 3.12.3, PyYAML 6.0.2, pinned Markdown renderer)

`evidence/final-gates.tsv` holds the per-command rc and time. Notable results:
- `python3 scripts/act_ci.py --selftest`: PASS, 610 ok, 68.8 s.
- Isolated install (`install -m 0555` into a fresh directory, then `python3 -I <dir>/act_ci.py --selftest --worktree "$PWD"`): PASS, 608 ok. The two meta-arms about the flat install itself run only in the direct form.
- `python3 scripts/ci_events.py --check`: rc 0. `python3 scripts/ci_events.py --selftest`: PASS, 2187 contract items, 5218 arms (dev: 5215), 222.9 s.
- The whole "CI scheduling and evidence controls" list: `ci_gate_workflows.py --check`, `ci_gate_workflows_selftest.py` (11 census budget cases plus the owner and order checks), and twelve more. All rc 0.
- Idiom and ratchet gates, all rc 0:
  - `check_py_idiom.py` and `--selftest`, `check_sh_idiom.py` and `--selftest`, `check_hygiene.py --check` and `--selftest`
  - `measure_fail_fast.py --check`, `measure_test_evidence.py --check`, `measure_naming.py --check`
  - `check_todo_ownership.py` and `--selftest`
- Doc gates over `84f9e300..HEAD`, all rc 0:
  - `check_em_dash.py --base 84f9e300...`: 0 findings over 92 added lines. `--selftest` also passes.
  - `check_doc_style.py` and `--selftest`, `check_doc_paths.py`, `check_solution_docs.py`
  - `gen_toc.py --selftest`, `--verify-anchors` and `--check`
  - `docs_check.py`, `check_archive.py` and `--selftest`
- Gates not run: none that these files touch. No RTL, product tests or census checks changed.

## Open risks / notes for review

- The four-job act replay at this head (the item 2 receipt) is outstanding. It is the manager's.
- Slot 0 has no slice, so it still counts no OOM. This is documented.
- The bound assumes cgroup v2. On v1 only `MemTotal` would be read.
- `CENSUS_WORKER_BYTES` is a measurement at today's datapath. A larger datapath needs a new measurement.
- On an OOM, the collector still writes `ci-manifest.json`, whose completeness reads only job receipts. `slot-memory.json` and the rc 2 refusal carry the invalidity.
