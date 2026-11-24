# [A839] CICD improvement, round 3: three commits, one patch, one FPGA-gPTP branch, one proposal

**Summary.** Branch `cicd-3`, stacked on PR #1001's head `fcbc31f3`, carries three commits. Each is measured and
each kept every verdict identical. A fourth item is a patch for the manager, and item 5 is a branch in a scratch
FPGA-gPTP clone.

| # | Item | Result | Where |
|---:|---|---|---|
| 1 | Preflight once per head | A `verilator-preflight` job runs the eight self-tests once. The 19 workers run `--no-preflight`, and `verilator-suites` is red unless that job succeeded and recorded the run's SHA. Shard 9 replica: first suite at +2 s instead of +535 s, 134 CPU-s less, logs and receipts IDENTICAL. Hosted: −76..−97 s per worker, ~−23 runner-minutes per run. | `66b092e1` |
| 2 | Longest case first | A piece's cases start longest first by a measured cost table, and results print and record in driver order. milan_dp__0 replica: 3411.9 → 2711.8 s wall (−20.5 %), same instructions. Receipts IDENTICAL. | `13e6d869` |
| 3 | Stable mutant staging | Every mutation driver (38) stages through `scripts/mutant_stage.py`. Warm-cache hits: crf_rx 79/115 → 115/115, avtp_rxmon depkt 37/48 → 48/48, tcam 12/16 → 16/16, rx_filter binding 6/8 → 8/8. Every mutant is killed by the same named check. Finding 3 is this same defect, now fixed. | `f6c11a25` |
| 4 | SMT-aware booking | `round3/smt-booking.patch` (not applied). Measured: no gain on this host today. The counters show why: ten unpinned units float onto the idle siblings. | patch |
| 5 | FPGA-gPTP engine passes at once | Branch `engine-run-passes-at-once` at `bbda770` (not pushed): 2721.6 s → 974.6 s wall, CPU +2.3 %, transcript IDENTICAL. | scratch clone |
| 6 | Hosted ccache and cache retention | `round3/PROPOSAL-hosted-ccache.md`. 3.64 GB of the 5.68 GB Actions cache belongs to merged PRs. | proposal |

Head measured: the commits above (the lane's `cicd-3` at `13e6d869`; `cicd-verilator-perf` untouched). Host: AMD
EPYC 9554P VM, 96 vCPU = 48 cores × 2 SMT threads (siblings 2k, 2k+1), load 170-230 from other lanes
throughout. Every CPU read 100 % busy in a 5 s `/proc/stat` sample, so wall times are inflated 2-3× and noisy, and
the decision figures are perf counters and CPU-seconds. Toolchain: pinned Verilator 5.050, g++ 16.2.1, ccache
4.14.1, GNU make 4.4.1. Raw data: /data-2/milan/tmp/cicd-a839/r3/.

Verdict identity rule (as in rounds 1-2): whole outputs are compared after removing only host text. That is
Verilator statistics and warnings, make chatter, compiler echoes, scratch paths, temp names and PIDs, plus, for
item 3, the staging directory's own name, which is what that change moves. Every check line, figure and verdict
must be byte-identical, with no number masked (`tools/logcmp.py`, `tools/mutcmp.py`). CI pieces are compared by
their receipts' per-case outcome, return code and `output_sha256`.

Placement: every A/B pair ran concurrently, each arm pinned to whole physical cores of its own (taskset;
`pool-spill.sh` was not running, and every pin held). Booked ranges came from `cpu_ranges.py pick`, held by
`milan-cicd-a839e-*` units so `busy()` saw them. Where no booking range was free, arms ran in the session pool.
Item 4 shows that a pin does not make a sibling idle on this host.

## 1. Preflight once per head (`66b092e1`)

### 1.1 What changed

- `scripts/run_all_suites.sh`:
  - `--preflight-only` runs `run_preflight_gates` under the same lock, log preparation and INT/TERM traps, and no
    suite: exit 0, or 2 when a self-test fails. It refuses `--shard`, `--list`, `--ci-pieces`, `--physical-gptp`
    and `--no-preflight`.
  - `--no-preflight` is accepted only with `--ci-pieces`. It prints `preflight: not run here; ...`. The serial
    sweep, `--physical-gptp`, local runs and act keep the preflight.
- `scripts/ci_suite_workflows.py` (the generator; the template and its contract are untouched):
  - It adds `verilator-preflight` ("Verilator preflight"), with the workers' `needs: full-ci-gate`, their `if`,
    checkout and SHA record. It runs `--preflight-only` and uploads `suite-preflight`.
  - It needs no submodules and none of the workers' tools: `--preflight-only` passes in a tree exported without
    submodules (receipts/preflight/preflight-only-without-submodules.log), and no self-test skipped anything.
  - It runs beside the workers, so its setup is not on their critical path.
  - Workers run `--ci-pieces --no-preflight --shard`.
  - `verilator-suites` needs the job, downloads `suite-preflight`, verifies it with `ci_events.py
    --require-target-sha --expect 1`, then fails unless `needs.verilator-preflight.result == success`.
- `.github/workflows/rtl.yml` is regenerated. The runtime layer adds the job to `ci-fail-fast`'s `EXPECTED_JOBS`,
  to `ci-manifest`'s needs and to the job-evidence steps automatically.
- `scripts/test_suite_cancellation.py` calls the new `scripts/suite_preflight_controls.py`. It was at its
  1000-line ratchet, so it stays at 1000 lines and the controls live in the new module.
- `scripts/ci_suite_pieces_selftest.py` adds the binding controls.
- Docs: CI_WORKFLOWS.md "Exhaustive validation" and "Failure and cancellation semantics"; TESTING.md (both modes).

Contract properties kept:

- **Required contexts:** `verilator-suites` and `yosys-portability` keep their names (PUBLIC_NAMES unchanged). The
  preflight job is not a required context; it feeds `verilator-suites`.
- **Cancellation contract:** both modes run under the same traps. A failed preflight is a failed job, so
  `ci-fail-fast` cancels the run's workers as it does for a failed worker today. Workflow concurrency is
  unchanged.
- **Fork safety:** the new job has no `permissions` key, no secret and no token use: the same as the workers. The
  fail-fast watcher stays same-repository only.
- **Overhead allowance:** `WORKER_OVERHEAD_SECONDS` (122 s, preflight included) is left as it is, to be
  conservative, until a hosted run re-measures it.

### 1.2 Proofs

| Check | Result |
|---|---|
| `ci_gate_workflows.py --check`, `ci_events.py --check` | OK (2287 contract items) |
| `ci_events.py --selftest` | PASS, 5755 arms |
| `ci_gate_workflows_selftest.py`, `ci_suite_pieces_selftest.py`, `ci_fail_fast_selftest.py`, `ci_runtime_evidence_selftest.py`, `ci_workflow_plan_selftest.py`, `ci_manifest_selftest.py`, `ci_suite_collect_selftest.py`, `ci_case_receipts_selftest.py`, `generate_ci_evidence_pins.py --check` | all exit 0 |
| `test_suite_cancellation.py` | PASS. New: preflight-only pass and fail, no-preflight, 7 refusals, INT/TERM at the preflight-only boundary, TERM at selection/command/transition under `--ci-pieces --no-preflight` |
| The new controls can fail | Two planted driver defects, each caught: `--no-preflight` still running the self-tests, and `--preflight-only` swallowing a failing self-test (receipts/gates/negative-controls.txt) |
| **A failing preflight fails the run** | `ci_suite_pieces_selftest.py` runs the generated `verilator-suites` step under bash with a preflight that passed for this SHA (green), and with one that failed, was cancelled, was skipped, passed for another SHA, or left no record. All five of the latter are red (receipts/preflight/binding-controls.txt). `--preflight-only` exits 2 on a failing self-test. The job is in fail-fast's EXPECTED_JOBS. |

Not done: no hosted run, since that needs a push, and no act replay. The act runner replays a pushed PR head;
this lane does not push.

### 1.3 Measured: shard 9/19 replica (maap__2 + aaf_clock_meter)

Two clones of `66b092e1` ran concurrently, each on 2 cores (4 logical CPUs, the hosted shape), with hosted job
budgets, no ccache and `SUITE_TIMEOUT=5400`. The first attempt hit 1800 s in aaf_clock_meter at this load. The
preflight-only arm ran alone on one core.

| arm | wall | CPU (user+sys) | first suite log born | result |
|---|---:|---:|---:|---|
| `--ci-pieces --shard 9/19` (preflight inside, today) | 4196.0 s | 1837.1 s | +535 s | 2/2 PASS, 487 checks |
| `--ci-pieces --no-preflight --shard 9/19` | 3956.4 s | 1702.8 s | +2 s | 2/2 PASS, 487 checks |
| `--preflight-only` (the new job's command) | 464.0 s | 140.1 s | — | exit 0 |

- maap__2 (33 lines) and aaf_clock_meter (120 lines) logs are IDENTICAL, and maap__2's 16 receipt results are
  identical.
- The preflight-only job's eight logs equal the shard's own preflight logs in seven cases. In the eighth,
  `test_suite_cancellation.log`, every line is identical once PIDs and temp names are masked, except one sampled
  process state (`"S"` against `"R"`) inside a handshake record. That is the state of a fixture process at the
  instant it was read, not a verdict.
- The CPU saved per worker, 134 CPU-s, equals the preflight's own 140 CPU-s. The 240 s wall difference is less
  than the 533 s preflight phase because the two arms' later suites were not equally contended.

Hosted estimate (run 45326076983's preflight spans): −76..−97 s per worker (median 78 s); shard 1, the longest
after #1001 at 26.4 min, becomes ~25.1. Runner time is −19 × 78 s ≈ −25 min, plus the new job's ~1.5-2 min, net
~−23 runner-minutes per run.

## 2. Longest case first (`13e6d869`)

### 2.1 What changed

- `scripts/ci_make_cases.py` gains `CASE_SECONDS`, the measured per-case cost of milan_dp's 26 cases (the only
  `ci_make_cases` suite with multi-case pieces), plus `start_order()` and `execute_all()`. A piece's cases are
  submitted to the two-worker pool longest first. Ties and unmeasured cases keep driver order. Results are
  collected by name and printed and recorded in driver order, so the transcript and receipt are unchanged by
  construction.
- `scripts/ci_make_cases_selftest.py` adds controls:
  - with one worker, cases start in exactly the expected order (longest, long, tie_a, tie_b, short, unmeasured);
  - with 1 and 3 workers, results return in driver order;
  - an unmeasured suite keeps driver order;
  - every table entry names a live case.
- TESTING.md documents the "Case start order in a piece" paragraph and how to retake the figures.

### 2.2 The cost table

Each case's `make -s -C tb/verilator/milan_dp exec-<case>` ran alone on one CPU of a booked core, at `fcbc31f3`,
in clone `base` on 56-63 (receipts/piece/cost/). CPU seconds are the figure; wall was 2.7-3.5× CPU from host load.
Piece 0: aclk 1558, gptp 862, dynmap 617, crflic 247, counters-1-frames 142, nxn4c 99, bootsa 96. Piece 1:
render-mutants 1375, gptp-lat 838, counters-8-frames 296, nxn 101, nolpf 22, maprec8 15, tspec8 14.

Start orders, list order → longest first:

| piece | list order (driver) | started |
|---|---|---|
| 0 | gptp, counters-1-frames, crflic, dynmap, nxn4c, **aclk**, bootsa | **aclk**, gptp, dynmap, crflic, counters-1-frames, nxn4c, bootsa |
| 1 | gptp-lat, counters-8-frames, tspec8, nxn, nolpf, maprec8, **render-mutants** | **render-mutants**, gptp-lat, counters-8-frames, nxn, nolpf, maprec8, tspec8 |
| 2 | counters-1, base, sidmove, nxndv, prune, maprec4 | counters-1, nxndv, base, sidmove, maprec4, prune |
| 3 | counters-8, notify, sidmove8, nxn8, ax1x1, split | notify, counters-8, nxn8, sidmove8, ax1x1, split |

Two-worker makespan from the table: piece 0 2519 → 1822 s (−28 %), piece 1 1823 → 1375 s (−25 %), pieces 2 and 3
within 2 %. aclk and render-mutants were still running when the table was first committed, so it held their
lower bounds (1049 and 1052 CPU-s, already above every finished case). The amend to the final figures changed no
start order. The measured arm below ran that first table, which starts cases in the same order.

### 2.3 Measured: the milan_dp__0 piece through its driver

Clones of `f6c11a25` (list order, as today) and `0572488b` (longest first, the first table, with the same
start order as the final one) ran concurrently on the booked range 0-7. Each arm had 2 cores (4 logical CPUs, the
hosted shape), the cases were prebuilt, and the arms used hosted job budgets and no ccache. Each ran `python3
scripts/ci_make_cases.py --suite milan_dp --shard 0/4 --jobs 2 --receipt ...`, as `ci_suite_pieces.py run
milan_dp__0` does.

| arm | wall | CPU (user+sys) | cycles | instructions | result |
|---|---:|---:|---:|---:|---|
| list order (driver order) | 3411.9 s | 4723.6 s | 17.04 T | 18.41 T | 7/7 pass |
| longest first | **2711.8 s (−20.5 %)** | 4840.2 s | 17.47 T | 18.41 T | 7/7 pass |

- **Identity:** the receipts' per-case outcome, return code and `output_sha256` are identical for all seven
  cases, and only `head` and `tree` differ, as the two commits do. The transcripts are IDENTICAL (4234 normalised
  lines) (receipts/piece/identity.txt).
- **Start times:** in the list-order arm aclk started about 1268 s in, behind gptp and nxn4c on its worker; in
  the longest-first arm it started at once.
- **Against the model:** the measured drop (−20.5 %) is below the table's −28 % for the execution phase. The
  wall includes the up-to-date build pass, and the two arms' cases were not equally contended at this load (the
  longest-first arm's cycles are +2.5 % for the same instructions).
- **Hosted estimate:** milan_dp__0's hosted figure is 1429 s (`PIECE_SECONDS`), so −20..−28 % is ~−290..−400 s,
  on worker 4, which runs that piece alone (24.8 min hosted at 300da99b) → ~19-20 min. Piece 1's render-mutants
  moves from last to first (model −25 %, not measured here); pieces 2 and 3 move by under 2 %.

## 3. Stable mutant staging (`f6c11a25`)

### 3.1 What changed

- `scripts/mutant_stage.py`:
  - `directory()` stands in for `tempfile.TemporaryDirectory` and `mkdtemp()` for `tempfile.mkdtemp`.
  - Both return `$TMPDIR/milan-mutant-stage-<uid>/<prefix><slot>`, the same path in every run and from every
    checkout.
  - Each of 8 slots is held under `flock` and emptied when taken, so a killed run's leftovers are cleared. A
    concurrent run takes the next slot. With all slots held it falls back to a random directory, correct but
    cold.
  - While a slot is held, the builds see `CCACHE_BASEDIR` at the stage root and `CCACHE_NOHASHDIR=1`
    (FPGA-gPTP #104's idiom); a caller's own setting wins.
  - With no cache (`OBJCACHE` empty), nothing changes.
  - `--selftest` has 7 controls and runs in docs.yml's "CI scheduling and evidence controls" step, which
    `ci_events.py` pins.
- All 38 drivers that staged through tempfile were changed by one codemod (receipts/tools/codemod_stage.py), and
  split/srptx's in-tree `mkdtemp` became `mutant_stage.mkdtemp(..., parent=HERE)`. Left alone:
  - gsi's `.gsi-uc-` run directory, which holds a ROM image and no build;
  - `nvm_backend`/`nvm_cosim`/`tdm_render`, which already use fixed paths;
  - `ctrl_service_budget`'s Python-level mutants.
- `gptp_shadow/test_mutant_lifecycle.py`:
  - Its fixtures install `scripts/mutant_stage.py`.
  - Its "refusal left scratch" check looks at the new location too. The old glob would have passed vacuously, a
    weakened test.
  - PASS.
- TESTING.md: the staging rule.

### 3.2 Why it was needed (reproduced)

Verilator writes each source's path into the generated C++. Planting the same RTL in two directories gives
`VL_FATAL_MT("/…/a/m.sv", …)` against `VL_FATAL_MT("/…/b/m.sv", …)` in `__024root__0.cpp` and `__Slow.cpp`
(receipts/mutants/embedded-path.txt). So every mutant model staged under tempfile's random directory misses ccache
in every run.

### 3.3 Measured (5 drivers, base `66b092e1` vs head `b01326c5`)

For each driver in turn: cold (empty cache), warm (same checkout), and for the head a warm run from a second
checkout. Each arm had its own cache and 2 cores. Hosted budgets throughout.

| driver | base cold | base warm | head cold | head warm | head, another checkout | warm wall base → head | warm CPU base → head |
|---|---:|---:|---:|---:|---:|---:|---:|
| crf_rx `mutants.py` (23 cases) | 74/115 | 79/115 | 74/115 | **115/115** | 100/115 | 282.9 → 232.0 s | 268.5 → 201.7 s (−25 %) |
| avtp_rxmon `depkt_mutants.py` | 33/48 | 37/48 | 33/48 | **48/48** | 46/48 | 54.2 → 19.7 s | 31.2 → 11.3 s (−64 %) |
| tcam `mutants.py` | 11/16 | 12/16 | 11/16 | **16/16** | 15/16 | 32.3 → 5.6 s | 8.9 → 1.6 s |
| rx_filter `binding_mutant.py` | 3/8 | 6/8 | 3/8 | **8/8** | 7/8 | 20.3 → 4.4 s | 5.0 → 1.1 s |
| mmcm_servo `slew_mutants.py` | 34/50 | (stopped) | (stopped) | — | — | — | — |

- **Verdict identity:** every log is IDENTICAL to the base cold run's in all five runs (crf_rx 44 lines, all 44
  verdict lines; depkt 25/12; tcam 6/4; rx_filter 6/5). So every mutant is still killed by the same named check.
- **mmcm_servo** is simulation-bound: its cold run took 3918 s wall for 1398 CPU-s. I stopped both arms there
  (my own units) and reran only crf_rx and depkt. Its head run had printed its first 16 of 19 lines identically.
- **The cross-checkout misses** come from harness sources compiled from the stage by their absolute checkout path.
  tcam's one miss is `/…/m3h/tb/verilator/tcam/sim_main.cpp` (ccache's own log, receipts/mutants/). crf_rx's 15 (ccache's log from a third checkout, receipts/mutants/crf_rx-third-checkout-misses.txt) are 2 harnesses compiled by absolute path (`sim_discontinuity.cpp`, mmcm_servo's `sim_main.cpp`) and the 13 staged harness copies, whose headers resolve through the Makefile's `-I$(CURDIR)`: that absolute checkout path lands in the preprocessed line markers. All 100 model and runtime compiles hit.
  Hosted runs check out at the same path every time, so they have none.
- **CPU:** the warm-run CPU that remains is simulation.
- **Change made after this measurement:** `b01326c5` was amended to `f6c11a25`, which renames the helper's `dir`
  parameter to `parent` (the idiom gate's shadowed-builtin rule) and changes no behaviour. The lifecycle test and
  the self-test were rerun on `f6c11a25`.

### 3.4 Finding 3 (rx_filter's non-reproducible `__ALL.cpp`): the same defect, fixed

- Three verilations of rx_filter into three directories give byte-identical C++; only the `.d`/`.dat` path
  records differ.
- The suite build through ccache hits 4/4 in the same checkout and 4/4 from another checkout, `__ALL.cpp`
  included.
- Round 2's persistent rx_filter misses were `binding_mutant.py`'s model, staged under a random temp directory:
  base warm 6/8, head warm 8/8. It was neither a build-ordering artefact nor a model artefact. It was the staging
  path, and item 3 removes it.

## 4. SMT-aware local booking (patch, not applied)

`round3/smt-booking.patch` holds the explanation and the diff. Summary:

- `cpu_ranges.py` gains `threads()` (one CPU per physical core, refusing a split core) and `unpinned()` (shown by
  `show`). `busy()` counts both siblings of every pinned CPU.
- `native-shards.py` pins each shard to one thread per booked core with `-j<cores>`.
- `start-act.py` refuses a split range.

`patch -p1 --dry-run` is clean against the live files, which are unchanged (md5 in the patch).

Measured on shard 8/19, concurrently, at `f6c11a25`:

- 2 cores with both siblings used: 3102.1 s, 10.97 T cycles;
- 4 booked cores, one thread each: 3256.7 s, 11.01 T cycles;
- 13.75 T instructions and IPC 1.25 in both; logs IDENTICAL.

No gain, because the nominally idle siblings were busy. Ten active units keep the full 0-95 mask (seven sessions
started outside lane-queue's `session_pool()`, this one included, and three gate units), and `busy()` cannot
count them. The patch is necessary and not sufficient: those units must be confined first, and the patch's
`show` names them.

## 5. FPGA-gPTP: the engine suite's four passes at once (branch, not pushed)

Scratch clone /data-2/milan/tmp/cicd-a839/r3/fpga-gptp, branch `engine-run-passes-at-once`, `bbda770` on main
`1213ac5`:

- `tb/verilator/engine/Makefile`: the images are written first, the four passes start together, and their
  outputs print in the serial order under the serial echo lines. The run stops at the first failing pass with
  its status. INT/TERM traps are set before the first pass starts. The stale "THREE times" comment now says FOUR.
- `docs/TEST_DEVELOPER.md`: four lines.
- `make docs` and `make lint` pass.

Measured:

- serial `1213ac5`, one core: 2721.6 s wall, 817.7 CPU-s;
- parallel, four cores, one thread each: 974.6 s, 836.8 CPU-s (2.79× faster wall, +2.3 % CPU);
- transcript IDENTICAL (170 normalised lines).

Hand checks:

- SIGTERM to make killed all four passes (make `Error 143`).
- A stub simulator failing in pass 1 printed pass 0, the echo line and pass 1's `[FAIL]`, and nothing later.
  make reported `Error 3`.

The body is `round3/PR-BODY-fpgagptp.md`.

## 6. Hosted ccache and Actions cache retention (proposal)

`round3/PROPOSAL-hosted-ccache.md`, in order:

1. **Free the quota.** Delete the merged PRs' entries now: 206 entries, 3.64 GB, one listed manager command.
   Then stop the duplication: key each tool cache by its own recipe instead of `hashFiles('.github/workflows/*.yml')`,
   so no PR entry has ever had a dev key, and save tool caches only from dev.
2. **ccache in the image (#737's recipe lane).** The request is derived from the sweep's `command -v ccache`
   probe, then the source lock, then smoke. `/usr/lib/ccache` stays off PATH, so firmware-boundary's judged
   compiles are never wrapped.
3. **Shards in the image.** The within-job hits come with no further change.
4. **A restored per-shard ccache.** At most 19 × 256 MB, saved nightly on dev, PRs restore-only, pruned to one
   generation.

## 7. Findings for their own Issues

1. **Unpinned units defeat every placement control** (item 4). Ten active units run with affinity 0-95, among
   them sessions launched outside lane-queue and the gate units lwsrppin-a834-r4-h-1x1/-8x8-1if and
   qual1124-a840-chain8. `busy()` treats a full mask as a daemon, so this load is invisible to bookings and lands
   on booked cores and their siblings.
2. **The cross-checkout residue of item 3.** A harness compiled from the stage by its absolute checkout path
   misses once per driver in a new checkout (crf_rx 15 of 115, all harness compiles; tcam 1, depkt 2, rx_filter 1). Copying the harness into the stage, or compiling it from
   a relative name, would close it. It costs nothing on hosted, where the checkout path is fixed.
3. **`check_py_idiom.py` reads tracked files only.** A new module passes the gate until it is committed. This round
   caught its own `dir` parameter only after the commit. A pre-commit run over `git ls-files --others
   --exclude-standard` as well would close that window.
4. **The CI tool inventory** (round 1 §5.3) is still red at the base. This round changes scripts it hashes
   (run_all_suites.sh, ci_make_cases.py) and adds two (mutant_stage.py, suite_preflight_controls.py), all
   unrecorded, as before.
