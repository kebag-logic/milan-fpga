# [A505] HANDOFF — #143 `--jobs` for the eight serial mutation drivers

Lane: branch `pp143-campaign-jobs` from `main` `631eeb34`. Assignment: issue #143 comment 5958637229.

Status: REVIEW READY at head `ab8a50be3a6ffeaf9155f3807acd812ff7679d8a` (local branch; not pushed — push
is not this lane's to do). TAKEN posted as #143 comment 5958642683; REVIEW READY posted as #143 comment
5962222796 with the head. No STOP condition met: no RTL, test-arm, count or parent-visible change. PR body:
`PR-BODY.md` beside this file ("Closes #143"). Scratch evidence kept under `$VALIDATION_STORAGE/pp143-a505`
(logs, receipts, sources; build products deleted afterwards to free disk).

| Commit | Item |
|---|---|
| `85da751` | 1 (and 3): `--jobs N` in the eight drivers through the shared `tb/common/mutant_pool.py` |
| `ab8a50b` | 2 (and acceptance 6): the option stated in the campaign READMEs, both wall times recorded |
| (none) | 4: `.github/workflows/hdl.yml` unchanged; no step needs an explicit N (see "CI") |

Diff from `631eeb34`: 15 files (8 drivers, the helper, 6 READMEs). Every mutation table and module constant
of the eight drivers has the same AST at base and head (`MUTANTS`, `MUTATIONS`, `EQUIVALENT_MUTATIONS`,
`PERFORMANCE_MUTATIONS`, `REMOVED_EQUIVALENTS`, gsi `mutations()`, `SUITES`, `PATCHES`, `TREES`, ...); the one
new constant is `RTL` in `retry_mutants.py`, the path it used inline. `85da751..ab8a50b` changes READMEs only,
so the equivalence runs at `85da751` ran the head's driver code.

## Constraints found (why the code looks as it does)

- Reference semantics (`tb/pp_top/d3_mutants.py:547,564`): `--jobs N`, `type=int`, default 4, a thread pool
  of `max(1, N)`; every mutant in its own `tempfile.TemporaryDirectory` copy. (acmp/notify default 1; the
  assignment names d3's default, so 4.)
- Parent gates (milan-fpga dev cdf49d1a):
  - `measure_test_evidence.py --check`: a `tb/` file that reads files and holds a quoted `hdl/` path is a
    DUT-source reader needing a disposition; a vanished reader makes its disposition stale. The helper reads
    nothing and names no `hdl/` path; `retry_mutants.py`, `gsi_mutants.py`, `srp_admission/mutants.py` stay
    readers; the other five stay non-readers. Host time / `timeout=` in a suite file counts against the
    3 <= 3 wall-clock ratchet, so no driver times itself; wall times were taken outside (`date` in a wrapper).
  - `check_py_idiom.py`: 0 unannotated / 0 undocumented public functions, 0 lines > 120 columns, functions
    <= 100 lines, <= 6 parameters, no unmanaged `open()`, no built-in shadowing. The parent's own `scan`,
    `reads_dut_source`, `uses_wall_clock`, `is_driver` were run on every changed file at base and head: no
    idiom finding; classification unchanged for all eight; the helper is none of the three.
- Host: 16 CPUs, 12 GiB cgroup cap, `/tmp` is tmpfs (charged to the cap). Every run used
  `TMPDIR=$VALIDATION_STORAGE/pp143-a505/tmp`, Verilator 5.050 (`$VALIDATION_TOOLS/pinned-verilator-5.050`) first
  on `PATH`, `PYTHONDONTWRITEBYTECODE=1`.
- Memory (cgroup peak): 8 `pp_top` workers x 8 build threads reached the cap (11.5 GB anon; no OOM kill; the
  9 units were still correct); 8 workers x 4 threads beside three `--jobs 1` runs reached 11.9 GB — that
  `--jobs 8` run was stopped and discarded, then re-run alone. A `pp_top` worker costs about 0.5 GB
  (Verilator) + 0.25 GB per compiler thread. Rule adopted: every equivalence run, at either N, pinned to its
  own 4 CPUs (`taskset`; Verilator's `-j 0` honours it: 4 threads); the `pp_top`-heavy `--jobs 8` runs
  (dispatch, aecp, gsi, adp) with nothing heavy beside them, under a guard that would kill only that run
  above 10.5 GiB anon (it never fired; highest anon seen afterwards 10.1 GiB). The parent's `make -j16`
  builds were pinned to 4 CPUs for the same reason.
- Session lessons: only runs started in background mode survive a call; `pkill -f PATTERN` must not use a
  pattern present in its own command line (it killed its own shell twice, exit 144); a foreground `sleep` is
  refused, so waits polled rc files.

## Shared helper: `tb/common/mutant_pool.py` (46 lines)

- `DEFAULT_JOBS = 4` (`:22`) and `add_jobs_argument(parser)` (`:25`): `--jobs N`, `type=int`, one default.
- `in_order(work, units, jobs)` (`:32-46`), a context manager: `ThreadPoolExecutor(max(1, jobs))`, units
  submitted in declared order, results yielded in that order whatever order they finish in; a unit's
  exception raised at its turn; leaving the block (end, return, exception) cancels units not yet started and
  waits for the running ones (`shutdown(cancel_futures=True)`). Not a bare generator: a generator held in a
  local survives in an exception's traceback and the pool would run every queued unit before exit (found in
  self-review of the first draft, fixed before the commit).
- Scratch test (`$VALIDATION_STORAGE/pp143-a505/test_pool.py`, not committed): declared order with reversed
  finish times; a unit exception at its turn (10 of 20 started); a consumer exception and an early return
  cancel the rest; `--jobs 0` = one worker; default 4.
- Drivers import it via `sys.path.insert(0, <repo>/tb/common)`. d3/acmp/notify are untouched (they already
  have `--jobs`; their summaries print in completion order — outside this issue's eight; a possible
  follow-up if the order rule should cover them too).

## Per-driver changes (head `ab8a50b`)

Every driver: `add_jobs_argument(parser)`; a worker that makes a private `tempfile` copy (own `obj_dir`),
plants its unit there and runs it; results read through `in_order` in declared order. Gating kept: a golden
or baseline the old code ran first and stopped on still runs first and alone; arms are submitted only after
every control passed where the old code stopped on a failed control. `--only` keeps each driver's syntax.

| Driver | Worker / consumer | Notes |
|---|---|---|
| `tb/acmp_talker/retry_mutants.py` | `mutated_source` `:315`, `scratch_case` `:327`, `main` `:351` (`with in_order` `:365`) | baseline serial and gating; mutants + `restored` in the pool; `restored` is a fresh unmutated copy (README updated) |
| `tb/adp_engine/mutants.py` | `trial` `:102`, `campaign` `:121` (`:128`, `:139`) | `plant` patches a fresh copy instead of restoring `hdl/` |
| `tb/maap/mutants.py` | `trial` `:89`, `controls` `:103`, `arms` `:124` | each copy carries `common` + every selected suite, as before |
| `tb/pp_top/aecp_dispatch_mutants.py` | `trial` `:165`, `campaign` `:188` (`:193`, `:204`) | `run` still deletes `GENERATED` before each build |
| `tb/pp_top/aecp_mutants.py` | `trial` `:189`, `campaign` `:217` (`:224`, `:235`) | `forget_generated_roms` removed: a copy never carries `*.hex` |
| `tb/pp_top/gsi_mutants.py` | `check_variant` `:117`, `report` `:153`, `main` `:162` (`:185`) | golden serial and gating; `--only NAME ...` added; 8-CPU affinity cap kept |
| `tb/srp_admission/mutants.py` | `trial` `:84`, `campaign` `:94` (`:111`) | one copy per (variant, suite) run, 12 units; `--only NAME ...` added; controls always run |
| `tb/srp_top/mutants.py` | `trial` `:130`, `campaign` `:149` (`:155`, `:166`) | receipts kept in the copy and written in declared order (5 labels share a receipt name across two suites; the later row's wins, as serially) |

`--only` with `--jobs` 2 to 4 was smoke-run on every driver at the final code before the commit (each arm
at its README count).

## Equivalence (`--jobs 1` vs `--jobs 8`, at `85da751`, each run pinned to 4 CPUs)

`compare.py` (scratch): stdout identical line for line (every verdict, count and the order) — in fact every
`eq-<driver>-j1.log` is byte-identical to its `-j8.log` (same sha256, below) — and every receipt identical in
FAIL lines and tally lines; `results.json` identical where written.

| Driver | Units | `--jobs 1` | `--jobs 8` | stdout | receipts | FAIL lines | README counts |
|---|---|---:|---:|---|---|---:|---|
| retry | baseline + 70 + restored | 408 s | 248 s | 71 lines identical | 73/73 (+ `coverage.txt`) | 2,640 | 62 KILLED equal; 7 equivalent, 1 performance |
| adp | 2 controls + 30 arms | 502 s | 333 s | 211 identical | 32/32 | 178 | 30/30 equal |
| maap | 3 controls + 29 arm runs | 253 s | 194 s | 101 identical | 32/32 | 189 | 29/29 equal (FAIL of checks) |
| dispatch | 4 controls + 37 arms | 1,059 s | 814 s | 265 identical | 41/41, results.json identical | 237 | 37/37 equal |
| aecp | 5 controls + 55 arms | 1,366 s | 1,079 s | 641 identical | 60/60 | 580 | 55/55 equal |
| gsi | golden + 20 + restored | 1,108 s | 713 s | 23 identical | 44/44, results.json identical | 9,899 | 20 detected |
| srp_admission | 4 variants x 3 suites | 791 s | 240 s | 13 identical | 12/12 | 8,358 | 9 mutant counts equal |
| srp_top | 11 controls + 78 arm runs | 2,258 s | 1,099 s | 91 identical | 84/84 | 687 | 90/90, coverage 65/65 |

Speed-ups are modest because both N ran on the same 4 CPUs (CPU-bound builds); that is the hosted runner's
size too. Observation, not changed: srp_admission's README gives the srp_top control 1527 checks (dated
2026-09-24); it is now 2200 (the suite grew on main before this lane); the mutant counts are unchanged.

## CI (item 4)

`hdl.yml`'s `suites` job runs five campaigns through their make targets, now at the default `--jobs 4` =
the 4 vCPUs of `ubuntu-latest`; at 4 workers a `pp_top` campaign needs about 6 GB of the runner's 16 GB. No
step needs another N, so no step passes one. All three jobs replayed at the head (the `suites` job pinned to
4 CPUs, default N), all rc 0 — table below.

## Suites and entry points (head `ab8a50b`, `git archive` export unless noted), all rc 0

| Command | Result |
|---|---|
| `verilator --version` | Verilator 5.050 2026-07-01 |
| `./scripts/lint_hdl.sh` | 41 modules (12 s) |
| `./scripts/run_suites.sh` | 33 suites, 1,019,127 checks, 0 failing; `tb/pp_top` 9,168; µPC map gate 61 constants / 89 entry points; M9 gate 30 opcodes, self-test 9/9 (852 s on 4 CPUs) |
| `make -C tb/srp_top mutants` | 90/90, coverage 65/65 (891 s); summary == `--jobs 1` run |
| `make -C tb/maap mutants` | 32/32 (136 s); summary == `--jobs 1` run |
| `make -C tb/adp_engine mutants` | 32/32 (286 s); summary == `--jobs 1` run |
| `make -C tb/pp_top aecp-mutants` | 60/60: 5 controls, 55 KILLED (954 s); summary == `--jobs 1` run |
| `make -C tb/pp_top aecp-dispatch-mutants` | 41/41: 4 controls, 37 KILLED (734 s); summary == `--jobs 1` run |
| `python3 scripts/gen_matrix.py --check` | 94 rows, 0 untested |
| `make -C tb/nvm_port figures` (scratch clone, after `git fetch ... refs/pull/13/head`) | all measured figures agree with the tree (260 s) |
| `make check` (scratch clone; wavedrom from the tools venv) | 41 mermaid + 18 wavedrom blocks, 1,035 links, 115 REQ rows, 17 GAP, 94 rows 0 untested, 27 parameters, stale OK |
| docs-gates job: `check-links.py`, `check-matrix.py`, `check-integrator-params.py`, `render-wavedrom.py --check`, `make stale` | each rc 0, figures as above |
| `git diff --check 631eeb34 HEAD` | clean |
| portability job: `./syn/yosys/run.sh` | 36 tops + 1 Xilinx mapping OK (104 s) |

## Campaigns at README counts (head `ab8a50b`), all rc 0

| Campaign | Result |
|---|---|
| `tb/pp_top/d3_mutants.py --jobs 2` | 87/87 KILLED, 3 goldens PASS (3,492 s); 75 `tb/pp_top` rows, 11 `tb/acmp_nvm` rows and the `tb/rx_validator` row (4) equal their READMEs |
| `tb/pp_top/acmp_mutants.py --jobs 1` | 19/19 KILLED, 3 goldens PASS (417 s); 14 pp_top rows equal; acmp_listener 93/50/40/30 and rx_validator 27 equal |
| `tb/pp_top/notify_mutants.py --jobs 1` | 40/40 KILLED at the README counts, 5 goldens PASS (1,105 s) |
| `tb/pp_top/name_wr_mutant.py` | decode killed; golden and restored PASS |
| `tb/desc_mem_guard/mutate.py` | hold-deleted mutant detected by the completed byte assertion |
| the eight drivers | equivalence table above (+ the five CI targets at the head) |

## Parent consumer gates (milan-fpga dev cdf49d1a + parent-adoption-c4c6-ea3fb388.patch), all rc 0

Scratch parent `$VALIDATION_STORAGE/pp143-a505/parent`: `git archive` of the trusted checkout at `cdf49d1a`,
committed in a fresh repo; tree `904f3079` and index (984 entries, 4 gitlinks) equal the checkout's.
`gptp-processor` `5dce647a` and `third_party/verilog-axis` `48ff7a7e` cloned from their recorded URLs;
`external` recorded, uninitialised; `protocol-processor` a clone of this branch at `ab8a50b`, gitlink staged
at it (`git submodule status`: ' ' for all three); the patch applied with `git apply` (2 files). The trusted
checkout was only read (its `scripts/__pycache__` predates this session, 07:35).

| # | Gate | Result |
|---:|---|---|
| 1 | `check_cpp_idiom.py` | every ratchet held (167 translation units) |
| 2 | `check_py_idiom.py` | every ratchet held: long function 9 <= 9, long module 10 <= 10, unannotated 0 <= 0, undocumented 0 <= 0, os.path 1 <= 1, unmanaged open 0 <= 0, too many parameters 7 <= 7, global 0 <= 0, over-long line 0 <= 0 |
| 3 | `xvlog_gate.py --check` (Vivado 2026.1, alone) | 4 findings == ratchet, 0 under `hdl/`; pinned at `protocol-processor@ab8a50be` |
| 4 | `check_rtl_source_lists.py` | OK; 107 files in the closure; protocol-processor 36/42 tops, 6 recorded |
| 5 | `pp_srcs.py --check --selftest` | OK |
| 6 | `sw/builder/test_builder.py` | all gates pass except 1 not run (gate 11: the calibration gate needs a board build tree not on this host) |
| 7 | `make -C tb/verilator/pp_shadow -j16` (4 CPUs) | 606, 606, 646 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | OK; 49 literal-bound, 59 without a rationale, lowerable by 3 |
| 9 | `measure_naming.py --check` | 96 recorded |
| 10 | `measure_test_evidence.py --check` | 72 <= 77 unarmed suites, 10 <= 10 unseeded, 0 <= 0 unexplained DUT-source readers, 3 <= 3 wall-clock |
| 11 | `docs_check.py` | 0 findings |
| 12, 13 | `make -C tb/verilator/nvm_cosim lint`, `quick` | lint clean; 315/315 |
| 14 | `make -C tb/verilator/milan_dp -j16` (4 CPUs) | every RESULT PASS (9); gmstep mutants 6/6 (1,809 s) |
| 15 | `make -C tb/verilator/milan_dp_render -j16` (4 CPUs) | leg defects 5/5 |
| 16 | `lint_rtl.py --check` | 90 <= 90 |

## Evidence (scratch, not in the tree; sizes in bytes, sha256 prefix)

Logs in `$VALIDATION_STORAGE/pp143-a505/logs`, receipts in `.../eq/out/<driver>-j{1,8}` and `.../head/out`.

| Log | Bytes | sha256 |
|---|---:|---|
| eq-retry-j1 / -j8 | 3,865 | 7bda8adf83703e45 (both) |
| eq-adp-j1 / -j8 | 15,806 | c71fe84cc09e8241 (both) |
| eq-maap-j1 / -j8 | 7,591 | 823ef7e638f720b0 (both) |
| eq-dispatch-j1 / -j8 | 27,808 | bb2e878ab890ae1e (both) |
| eq-aecp-j1 / -j8 | 70,393 | 35daf851262ab866 (both) |
| eq-gsi-j1 / -j8 | 4,150 | 5f6d67707db7bfed (both) |
| eq-srpadm-j1 / -j8 | 479 | 6977d367d954c85c (both) |
| eq-srptop-j1 / -j8 | 5,547 | e85d77e97510c5a0 (both) |
| ci-suites | 1,746 | 7c51e16dc35eee2d |
| camp-d3 | 6,345 | 9ae76c02bfebe5df |
| pg07-pp-shadow | 332,681 | dda5ccf9325b4bb6 |
| pg14-milan-dp | 2,087,792 | d86038a55ef65018 |
| pg03-xvlog | 1,320 | d7caf1b86a091121 |
