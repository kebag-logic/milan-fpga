[R395] POSITIVE - exact head 35f58b9cca1de9215f787872734e6a9040f82c19

# R395-4: external review of issue #617 / PR #618, round 4

Tree `9c090dda1d69b1572a763a9fa7bf29218bfd5fdb`. Delta reviewed: `ddb07747..35f58b9c` (three commits), under the round-4 ruling (issue 617 comment 5881942681), against the whole PR `ce550952..35f58b9c`. All five lenses were applied at this head. No BLOCKER, MAJOR or MINOR is open. Two SUGGESTIONs follow; neither affects coverage.

## Verdict in one paragraph

Round 3's blocker (R395-3 F1 = R394-3 F1) is resolved. The cause is GNU make 4.3 handing a `make -C` recipe `MAKEFLAGS=w`, which I reproduced with an upstream make 4.3 built from source. Both nested `$(shell $(MAKE))` calls now pass `--no-print-directory`, and the arm empties `MAKEFLAGS`. Either fix alone makes the `dp` build succeed; with both removed, the build fails the way it did on the hosted runner.

Hosted `Verilator shard 1/5` passes `capture_coherence`. Its arm reports `30 checks: 30 PASS, 0 FAIL`, including the `dp` and `dp-band` controls and both datapath mutants. The suite took about 993 s of the 1,800 s guard, a 44.8% margin, which beats the author's 1,024 s projection.

Locally at the exact head, under make 4.3, the arm is 30/30 on 4 and on 8 workers. Its verdict lines match the hosted run's line for line, in the same order. Both new checks fail under the faults they claim to catch, and RM9 is refused by name. The round-4 RTL changes are comment-only. The rewritten envelope and lock statements match independent measurements, including new 150,000-column converged-lock runs at ±100 and ±150 ppm.

## What the round asked me to verify

### (1) Hosted shard 1/5 at 35f58b9c

Evidence: run 36518018770, job 109244655191, and artifact `suite-logs-1` (`receipts/hosted-35f58b9c-shard1.txt`, `receipts/hosted-35f58b9c-shard1-capture_coherence.log`, `receipts/hosted-checks-35f58b9c.tsv`).

- The job checked out `76576f8`, which is `Merge 35f58b9c into eaa88a32`: the PR merge ref, not the source head alone. `TARGET_SHA` = `76576f833721a65453bc1e9296875b8587a6fbf1`.
- Suite tallies:
  - `capture_coherence`: 20,832 / 0.
  - `capture_coherence_dp`: 332 / 0.
  - Arm: `[i] 29 builds on 4 worker(s)`, then `30 checks: 30 PASS, 0 FAIL`.
- Arm contents:
  - Both new build checks pass. The planted-break line prints Verilator's `%Error: .../build_break_dp/milan_datapath.sv:7821:15: syntax error`.
  - All eight controls pass, `dp` and `dp-band` among them.
  - All twenty mutants are caught by their named checks: the `dp` one-pair-frame mutant, the `dp-band` round-1 binding, RM5, and RM9 by its refusal.
- Elapsed time: `scripts/run_all_suites.sh` runs suites serially. `capture_coherence`'s PASS line is 992.8 s after the previous suite's PASS line. That is an upper bound, since it includes the verdict tally.
  - Against the 1,800 s guard: 807 s spare, a 44.8% margin.
  - Against the ruling's 1,500 s target: inside it.
- Shard summary: 23/23 suites passed, 0 timed out.
- Every other hosted context at this head succeeded. `Physical gPTP (nightly and manual)` was **skipped**: a skipped context, not an executed one.

### (2) `--no-print-directory`, the emptied `MAKEFLAGS`, the failure tail, and the two new checks

- **Mechanism, reproduced independently** (`receipts/make43-w-demo.txt`, `scripts/make43_w_demo.sh`):
  - Under make 4.3, a recipe started by `make -C <dir>` gets `MAKEFLAGS=[w]`. A nested `make -s -C sub` then prints `Entering directory` into its stdout, and `--no-print-directory` suppresses it.
  - Under make 4.4.1 the recipe gets `MAKEFLAGS=[]`.
  - The make 4.3 used is built from upstream `make-4.3.tar.gz`, sha256 `e05fdde4…e78e19` (`receipts/tool-identity.txt`).
- **The fix in the code:**
  - Both nested calls carry `--no-print-directory` (`tb/verilator/capture_coherence/Makefile:101`, `:105`).
  - `mutants.py` runs every build with `MAKEFLAGS` set to `BUILD_MAKEFLAGS = ""` (`:123`, `:341`, `:522`).
  - A failed build prints `BUILD_TAIL_LINES = 40` lines of its own make and compiler output (`:126`, `:328-331`, and every `did not compile` branch).
- **R394-3's reproduction at this head, under make 4.3** (`receipts/r394_mf_repro-35f58b9c-make43.txt`; the script is copied unchanged, same sha256): with `MAKEFLAGS=''` and with `'w'`, `DP_SRCS` begins with the processor packages, and `mutants.build('dp')` builds `Vcoherence_dp` both times.
- **The make 4.3 chain** (`make -C tb/verilator/capture_coherence mutants`, without `-s`, as the sweep runs it):
  - rc 0 and `30 checks: 30 PASS, 0 FAIL`, with 4 workers (`receipts/make43-chain-mutants-35f58b9c-run1-4cpu.log`, 749 s).
  - The same with 8 workers (`receipts/make43-chain-mutants-35f58b9c.log`, 505 s).
  - Both ran on a shared host with load average 38-71, so neither time is a hosted projection.
- **Fault probes against the committed functions** (`scripts/check_fault_probe.py`, `receipts/build-check-fault-probes.txt`). Each probe injects a variant Makefile with `-f` or patches a constant in memory; no tree edit is involved.

| Probe | Fault | Result |
|---|---|---|
| A | `--no-print-directory` removed from the `DP_SRCS` call only | `makeflags_result` **FAILS**; the tail shows `%Error: Cannot find file containing module: 'Entering'` |
| B | `--no-print-directory` removed from the `DP_VFLAGS` call only | **FAILS**, same signature |
| C | committed Makefile | PASSES |
| E | `BUILD_MAKEFLAGS='w'`, committed Makefile | builds: the Makefile fix alone suffices |
| F | `BUILD_MAKEFLAGS=''`, both flags removed | builds: the environment fix alone suffices |
| G | `BUILD_MAKEFLAGS='w'`, both flags removed (the `ddb07747` state) | fails, and the tail prints the cause and make's `Error 1` |
| D1 | printed tail cut to 1 line | `build_break_result` **FAILS**: the `%Error` is no longer shown |
| D2 | the build's output discarded | **FAILS** |

Probe D (`BUILD_TAIL_LINES = 0`) was void and is marked so in the receipt: in Python, `lines[-0:]` is the whole log. D1 and D2 replace it (`receipts/build-break-fault-probe2.txt`).

### (3) The parallel arm: coverage, determinism and isolation

- **Coverage.** Every mutant stays in the PR gate. `all: run dp mutants` (`Makefile:70`) runs under the sweep's default guard. There is no quick/full split, and `scripts/run_all_suites.sh` is not in the diff.
  - 29 units: 2 build checks, 7 control builds serving 8 controls, and 20 mutants. The hosted and local logs both print `29 builds`.
  - The twenty mutants match the list in `docs/testing/TESTING.md:490`.
- **Sharing.** `control_groups()` groups legs by an identical `(suite, target, source variable, objdir variable, source file)`. Only the `dp` and `dp-band` controls share a build: the unmutated datapath, with only the harness arguments differing. No mutant shares anything.
- **Isolation, by reading the code:**
  - Each unit stages its source under `<tmp>/<tag>/` and builds into `<tmp>/obj_<tag>/`.
  - The 30 tags are unique. Truncating to 60 characters causes no collision, and a collision would raise, not merge.
  - The junction recipe writes `mga_keepoff.svh` into the unit's own `MDIR`.
  - `print-srcs` and `print-dp-vflags` only echo. The harnesses open no output files.
  - The only shared writes are the two generated ROM images, which are made once before the pool starts (`rom_images_result`) and then only read.
- **Isolation, observed.** Before and after each local chain, the four suite directories hold only the ignored ROM images and a `__pycache__`. No arm temp dir is left behind after a completed run.
- **Determinism:**
  - The verdict lines of hosted (4 workers), local 4 workers and local 8 workers are **identical and in the same order** (`scripts/compare_arm_lines.py`, `receipts/arm-lines-compare.txt`). The normalisation covers only the temp path and the planted line number, which differs on the merge ref.
  - The committed `run_units()` driven with 29 fake units of random duration on 1, 3, 4 and 8 workers prints identical output in list order. A unit that raises propagates the exception, so it is not counted as a pass (`scripts/order_probe.py`, `receipts/run_units-order-probe.txt`).

### (4) RM9

- `mga_keepoff.py:36`, `:48-51` and `:68-74` require `.LOCK_KEEPOFF_CYC_P (MGA_KEEPOFF_CYC_C)` exactly once.
- Run directly (`scripts/rm9_probe.sh`, `receipts/rm9-mga_keepoff-probe.txt`):
  - The head passes, rc 0.
  - These are refused with rc 1 and the named message: RM9's literal `128`, a literal `256`, `MGA_KEEPOFF_CYC_C + 0`, `((128))`, a removed binding, and a commented duplicate.
  - Only an appended `defparam` escapes. That construct is exotic and I do not raise it.
- In the arm, RM9 is caught hosted and locally as `its build refuses it: "does not bind LOCK_KEEPOFF_CYC_P to MGA_KEEPOFF_CYC_C"`.

### (5) Wording and figures

- **Below nominal: gradual; above nominal: sharp near 67 ppm.** The citations are `TIME_SYNC.md:548`, `:556-558`, `REGISTER_MAP.md:1958-1967`, `KL_chan_map_capture.sv:96-104`, `milan_datapath.sv:5678-5686` and `coherence_bench.hpp:73-87`. The figures match my round-3 receipts (`617-r395-3-packet/receipts`):
  - net zero by column 8 at +66 ppm, carried across at +67;
  - last slip at column 426 at -63 ppm (earlier through -62), 1,323 at -66, and 1,692 at -67 ("about 1700").
  - Engagements that dwell on the crossing stay within +1 or +2 cycles of it through -67 ppm. The +46x excursions in those logs are engagements pulled cleanly to the far side, with 0 slips.
  - The internal reviewer's round-3 table agrees: -67 at column 1,719, and at most 1-2 cycles past the crossing through -66.
  - The -70 ppm figures (column 2,918; 6 cycles) come from that reviewer's receipts. I did not re-probe -70.
  - "By column 6,300 at 80 ppm on either side" holds. Hosted `CRF-settle-80+0` has its last slip at 6,284 and `CRF-settle+80+8` at 6,056. My round-3 probes put the last slip at 6,284-6,290 at -80 ppm.
- **CRF-settle grades the approach, and the converged lock is cited from recorded runs.**
  - The committed runs' second-half spread is 109-159 cycles (hosted log), so "approach" is the accurate word, and the new text says so (`sim_main.cpp:70-83`, `TIME_SYNC.md:552`).
  - I ran the converged lock myself: the committed placements, 150,000 columns, ±100 and ±150 ppm, 8 engagements (`scripts/converged_probe.sh`, `receipts/converged/*.log`, built through my round-3 probe tooling from a head archive).
  - Results: 0 failures and 0 tail slips everywhere, with a second-half spread of 1 to 3 cycles. The tick settles 255-256 cycles after the close at negative rates, and 779-786 cycles after it at positive rates, which is 255.7-262.7 cycles before the next close.
  - That matches `TIME_SYNC.md:551`, "255 to 264 cycles off (a pulled engagement 255 to 257), spread at most 3".
- **`TRIMW_P = 18` beside the NCO area.** The PR body names it. `milan_datapath.sv:766` binds `.TRIMW_P (18)`. The quoted figures equal my round-3 OOC rows at `TRIMW_P=18`: LUT 101→106, FF 46, CARRY4 35→37 at 50 MHz; LUT 103→104, FF 47 at 100 MHz. The NCO RTL is unchanged since.
- **Absolute-`MDIR` run targets** (`receipts/absolute-mdir.txt`):
  - The run lines now use `$(abspath ...)`: `media_nco/Makefile:39`, `chmap_capture/Makefile:27`, and `capture_coherence/Makefile:85` and `:130`.
  - `make -C tb/verilator/media_nco run MDIR=<absolute>` runs 410/410.
  - Dry runs show absolute executable paths for the other three targets.
  - My first attempt failed only because Verilator 5.050's `--Mdir` does not create missing parent directories. That is independent of this PR, and the receipt records it.
- Also checked:
  - CHANGELOG lines 50-51 and 62-64.
  - TESTING.md's twenty-mutant list and its build-check sentence.
  - The `sim_main.cpp` and `coherence_bench.hpp` comments. Their round-4 edits are comment-only, confirmed by a comment-stripped comparison.

### (6) No RTL logic change

`scripts/rtl_comment_only.py` (`receipts/rtl-comment-only-ddb07747-35f58b9c.txt`): `KL_chan_map_capture.sv` and `milan_datapath.sv` are the only `hdl/` files changed in round 4. With comments and whitespace stripped, both are identical to `ddb07747`.

### The nested-make pattern in `pp_shadow` and `milan_dp_render`

Classification: **safe in the PR gate; latent, and failing closed, in two explicit mutation targets under make 4.3.** Evidence: `scripts/nested_make_classify.sh` and `receipts/nested-make-classify.txt`, plus code reading.

- **At a top-level parse** (`make -C <suite>`, as the sweep runs it), both suites get clean lists under make 4.3: `pp_shadow` `DP_SRCS`, and `milan_dp_render` `SRCS` and `DP_VFLAGS`.
- **In a child make that inherits `MAKEFLAGS=w`**, every one of those lists begins `make: Entering directory …`. `capture_coherence`'s fixed lists stay clean.
- **The default gates never start such a child:**
  - `pp_shadow`: `all → run` has no recursive make. `pending_mutant.py` sits behind the explicit `pending-mutant` target.
  - `milan_dp_render`: `run` calls `tdm8_render_mutants.py --leg-defects`, which runs the on-disk binaries the top-level recipe built (`clean_legs`, `run_leg_defects`) and builds nothing.
- **Under make 4.3, two explicit targets are exposed:**
  - `make -C tb/verilator/pp_shadow pending-mutant`: both the listing call and `make run-pending` inherit `w`.
  - `make -C tb/verilator/milan_dp_render tdm8render-mutants`: `build()` launches `make -s -C` from a recipe.
  - Both would fail with "did not compile" or "clean control did not pass". That is a spurious red, never a false green.
- This PR does not touch either suite. See S2.

## Findings

No BLOCKER, MAJOR or MINOR.

### S1 - SUGGESTION - Robustness, Docs - `tb/verilator/capture_coherence/mutants.py:306-314`, `:572-573`, `:582`, and the docstring at `:83-86`: under the sweep's kill, the parallel arm often fails to remove its temporary directory

- **Evidence:**
  - Under `timeout … make -C <suite>`, the recipe's process receives **two** SIGTERMs, with both make 4.3 and 4.4.1: timeout signals the process group, and make forwards the signal to its child (`scripts/sigterm_count_demo.sh`, `receipts/sigterm-count-demo.txt`).
  - `stop()` is not idempotent. The first `sys.exit(143)` interrupts `as_completed`. The second interrupts `pool.shutdown(wait=True)` in the `finally`.
  - `TemporaryDirectory` then removes the directory while worker threads are still writing their `obj_<tag>.log` files, which raises `OSError: [Errno 39] Directory not empty`.
  - Across five kill probes (`scripts/kill_probe.sh`, `receipts/arm-kill-probe*.txt`, `receipts/arm-kill-probe-log-1.txt` with the full traceback), three left the directory behind, printed a chained traceback and exited 1; two exited cleanly with 143.
  - This behaviour is new with round 4's threaded driver. The round-3 handler was a one-line `sys.exit(143)` on a serial loop.
- **Impact: small.**
  - No arm process survives: the first `stop()` SIGKILLs every live process group, and `STOPPING` kills anything started later.
  - The sweep still records TIMEOUT, because `timeout` returns 124 whatever the child's exit status.
  - What is left is a directory of late-written build logs (124-216 KB here), the killed compilers' `cc*.s` files in `$TMPDIR`, and a traceback in the log.
  - The docstring's "removes the temporary directory" is inaccurate in about half of real kills.
- **Suggested outcome:** make `stop()` act once, for example by returning early when `STOPPING` is already set. Optionally, let cleanup tolerate late writers once the workers are joined.
- **Verification:** `scripts/kill_probe.sh <repo> 70`, repeated. Expect `make … Error 143`, no traceback, and no leftover `capture-coherence-mutants-*` directory.

### S2 - SUGGESTION - Tests, Robustness - `tb/verilator/pp_shadow/Makefile:107` with `pending_mutant.py:54`; `tb/verilator/milan_dp_render/Makefile:57-62` with `tdm8_render_mutants.py:411`: the same latent pattern, outside this PR

- **Evidence:** the classification above.
- **Impact:** `pending-mutant` and `tdm8render-mutants` fail spuriously under GNU make 4.3, for example on the hosted image or an Ubuntu 24.04 desk. Neither is in the default gate.
- **Suggested outcome:** a follow-up issue, filed by the manager, that applies this PR's two fixes (`--no-print-directory`, and a controlled `MAKEFLAGS` in the drivers). No change is needed in this PR.
- **Verification:** `scripts/nested_make_classify.sh` shows clean lists under an inherited `w`, and both explicit targets pass under make 4.3.

## Lens results (each covered at this head)

```text
[R395] PASS Conformance - tb/verilator/capture_coherence (junction 20,832/0 and dp 332/0 at the exact head under make 4.3: receipts/head-35f58b9c-junction-leg.log, receipts/head-35f58b9c-dp-leg.log; hosted merge-ref run receipts/hosted-35f58b9c-shard1-capture_coherence.log; arm 30/30) - #617 acceptance 1-3 (one TDM frame per column; drift in INTERNAL and CRF, failing at ce550952 through the committed ce550952-law mutant; render path unchanged) and ruling 1 (dp legs build anywhere), ruling 2 (every mutant in the PR gate, 993 s of 1,800 s hosted) and ruling 3 (RM9, wording, TRIMW_P, absolute MDIR) checked item by item
[R395] PASS RTL - hdl/ieee1722/aaf/KL_chan_map_capture.sv:92-110, hdl/milan/milan_datapath.sv:5675-5700 and :766 (receipts/rtl-comment-only-ddb07747-35f58b9c.txt) - the round-4 RTL delta is comment-only; the rewritten banners were checked against the probe receipts and the committed binding (MGA_KEEPOFF_CYC_C, TRIMW_P 18); no port, parameter or interface change
[R395] PASS Robustness - mutants.py build/kill paths, mga_keepoff.py, Makefile :101/:105 (receipts/build-check-fault-probes.txt, build-break-fault-probe2.txt, rm9-mga_keepoff-probe.txt, absolute-mdir.txt, arm-kill-probe*.txt, converged/*.log) - inherited MAKEFLAGS=w, planted break, literal/expression/removed bindings, absolute MDIR, kill mid-arm (S1, suggestion only: no surviving process, TIMEOUT verdict intact), and the settled lock converged to +/-150 ppm over 150,000 columns
[R395] PASS Tests - tb/verilator/capture_coherence/mutants.py and Makefile at 35f58b9c (receipts/make43-chain-mutants-35f58b9c*.log, arm-lines-compare.txt, run_units-order-probe.txt, r394_mf_repro-35f58b9c-make43.txt, hosted shard 1/5) - arm 30/30 hosted and locally on 4 and 8 workers with identical ordered verdicts; both new checks fail under their faults (A, B, D1, D2, G); dp/dp-band controls share only the unmutated build; no mutant moved out of the gate
[R395] PASS Docs - docs/design/TIME_SYNC.md:467-470, :545-570; docs/reference/REGISTER_MAP.md:1948-1970; CHANGELOG.md:47-66; docs/testing/TESTING.md:490; sim_main.cpp:67-83; coherence_bench.hpp:70-87; mutants.py and Makefile headers - every "63/67" is corrected; the figures reproduce against my round-3 receipts and this round's converged runs; CRF-settle is described as the approach; the twenty-mutant list matches MUTATIONS (the S1 docstring point is a suggestion)
```

## Reviewer-owned completion ledger

| Lens | Result | Artifacts examined | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #617 acceptance 1-3; round-4 ruling; junction and dp legs at the head; hosted shard 1/5 (merge ref 76576f8); arm 30/30 | R395-4 | 35f58b9cca1de9215f787872734e6a9040f82c19 |
| RTL | CLEAN | `KL_chan_map_capture.sv`, `milan_datapath.sv` (comment-only delta; binding and TRIMW_P) | R395-4 | 35f58b9cca1de9215f787872734e6a9040f82c19 |
| Robustness | CLEAN (S1 and S2 are suggestions) | `mutants.py` kill and build paths, `mga_keepoff.py`, Makefiles, RM9 variants, absolute MDIR, converged ±100/±150 ppm lock | R395-4 | 35f58b9cca1de9215f787872734e6a9040f82c19 |
| Tests | CLEAN (S2 is a suggestion) | Mutation arm (hosted, local 4 and 8 workers), fault probes A-G, D1, D2, order probe, R394-3 reproduction | R395-4 | 35f58b9cca1de9215f787872734e6a9040f82c19 |
| Docs | CLEAN (S1 is a suggestion) | TIME_SYNC.md, REGISTER_MAP.md, CHANGELOG.md, TESTING.md, suite headers and comments, PR body | R395-4 | 35f58b9cca1de9215f787872734e6a9040f82c19 |

## Prior public findings, resolved or retained at this head

I read these only after my own pass over the diff and the probes above.

| Prior finding | Status | Evidence |
|---|---|---|
| R395-3 F1 (BLOCKER) = R394-3 F1 (MAJOR): `dp`/`dp-band` legs never built on the hosted runner, and the suite's time against its guard | **RESOLVED** | Items (1)-(3): hosted 30/30 with both dp controls and mutants, 993 s of 1,800 s; make 4.3 chain 30/30 locally; the cause reproduced and both fixes proved independently |
| R395-3 S1 = R394-3 S3: below-nominal limit | **TAKEN** | Item (5) |
| R395-3 S2: `TRIMW_P` beside the NCO area | **TAKEN** | Item (5) |
| R395-3 S3: absolute `MDIR` | **TAKEN** | Item (5), also in `chmap_capture` and `capture_coherence` |
| R395-3 S4 = R394-3 S2: CRF-settle grades a converging lock | **TAKEN** | Item (5); converged lock re-measured over 150,000 columns |
| R394-3 S1: RM9 | **TAKEN** | Item (4) |
| R394-3 S4: time-guard headroom | **TAKEN** | Shared control build and parallel arm; 44.8% hosted margin |
| Rounds 1-2 (R394-1/2, R395-1/2) | **RESOLVED** at `ddb07747` (R395-3) | Round 4 reopens none: its RTL delta is comment-only and the harness C++ edits are comment-only |

## Real limits

- **Simulator.** Verilator 5.050 (`rev v5.050`) from `$VALIDATION_TOOLS/verilator-v5.050-src`, because the assigned pinned path does not exist on this host (`receipts/tool-identity.txt`). Build parallelism was capped by a wrapper (`scripts/verilator-jcap.sh`) so that at most 8 jobs ran at once. This changes build speed only.
- **GNU make 4.3** was built from the upstream tarball in scratch. I did not observe the hosted image's make version directly; the hosted signature it explains was reproduced.
- **Hosted evidence** is on the PR merge ref `76576f8` (the head plus dev `eaa88a32`). It is neither the source head alone nor live dev `13eda870`. The 993 s is an upper bound taken from serial log timestamps.
- **Local wall times** (505-749 s for the arm) were measured on a host shared with other lanes, at load average 38-71. They are not a hosted projection.
- **My first arm run.** During its last seconds, after every build had finished, I mistook it for dead. I renamed its open log and removed its temp dir while the final harness processes were still running. It completed at rc 0 with 30/30. The receipt carries this note, and the second run (8 workers) is the clean receipt. One kill probe also briefly ran beside another lane's arm. It shared CPUs only; I did not touch that lane's processes.
- **Envelope figures** from the internal reviewer's round-3 receipts (-70 ppm; the 13,000-frame time constant) were not re-probed. The OOC area was not re-run, because the NCO RTL is unchanged since round 3.
- **Not run by this reviewer:** the builder bank, native banks, lint, xvlog, Yosys, the Markdown gates, and the other Verilator suites (`milan_dp`, `milan_dp_render`, `pp_shadow`, and so on). These are the manager's banks, which passed at this head per the assignment.
- **Hardware.** Physical calibration: NOT RUN. Bench acceptance 4 is out of scope ("Relates to #617"). Field skips are not hardware proof.

## Pending manager duties

- Accept hosted `verilator-suites` and `yosys-portability` for this head. They ran on merge ref `76576f8`. The physical gPTP context was skipped, not executed.
- Build and validate the candidate merge on live dev `13eda870d1a6cf3f946fc228a98862366b08d102`, which differs from the hosted merge base `eaa88a32`. Run the native banks there.
- Update the PR body. It still says hosted checks "have not run" and that the duration is "not yet observed". The observed figure is about 993 s of 1,800 s.
- Decide S1. File the follow-up issue for S2.
- The completion bar also needs the internal reviewer's positive at this head.

## Restoration

`receipts/restore-verification.txt`:

- The clone is at `35f58b9c`, tree `9c090dda`, with no untracked or ignored files.
- The index equals the HEAD tree, 957 entries.
- 953 tracked files match their blobs byte for byte, with no exec-bit mismatch.
- The `gptp-processor`, `protocol-processor` and `third_party/verilog-axis` gitlinks match their checkouts, which are clean. `external` is uninitialised, as it was at the start.

Disposable trees are under `scratch/` only.

R395-4 FINISHED
