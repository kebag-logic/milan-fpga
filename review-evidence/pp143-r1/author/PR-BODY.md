[A505]

Closes #143

Lane for #143 (assignment: #143 comment 5958637229): `--jobs N` for the eight mutation drivers that ran serially. Branch `pp143-campaign-jobs` from `main` `631eeb34`, two commits. The items are taken in the assignment's order; item 3's helper landed with item 1, which uses it:

| Commit | Item |
|---|---|
| `85da751` | 1 and 3: `--jobs N` in the eight drivers, through one shared helper, `tb/common/mutant_pool.py` |
| `ab8a50b` | 2 (and acceptance 6): the option stated in each campaign README, with both wall times |
| none | 4: `.github/workflows/hdl.yml` is unchanged; no CI step needs an explicit N (below) |

No RTL, microcode, mutation patch, mutant, control or recorded count changes. The diff from `631eeb34` touches 15 files: the eight drivers, the new helper and six READMEs. Every mutation table in the eight drivers (`MUTANTS`, `MUTATIONS`, `EQUIVALENT_MUTATIONS`, `PERFORMANCE_MUTATIONS`, `REMOVED_EQUIVALENTS`, gsi's `mutations()`), and every other module constant they had, has the same abstract syntax tree at `631eeb34` and at the head. One constant is new, `RTL` in `retry_mutants.py`, which holds the talker path the old code wrote inline.

## 1. `--jobs N` (`85da751`)

`--jobs N` has the meaning and default of `tb/pp_top/d3_mutants.py`: `type=int`, default 4, a pool of `max(1, N)` workers. Every unit (a positive control, a golden, a baseline or an arm) builds and runs in its own `tempfile.TemporaryDirectory` copy, so no two units share a tree or an `obj_dir`.

The gating each driver had is kept:

- A golden or baseline that the old code ran first, and stopped on, still runs first and alone (`retry_mutants.py`, `gsi_mutants.py`).
- Arms are submitted only after every positive control has passed, where the old code stopped on a failed control.
- A failure that used to stop a serial run is raised at its unit's turn, and every unit not yet started is cancelled.

| Driver | Worker and consumer | Notes |
|---|---|---|
| `tb/acmp_talker/retry_mutants.py` | `scratch_case` `:327`; `main` `:351` | The baseline still gates the pool. `restored` is now a fresh unmutated copy at the end, since there is no shared tree to restore (README updated). |
| `tb/adp_engine/mutants.py` | `trial` `:102`; `campaign` `:121` | `plant` applies the patch to a fresh copy instead of restoring `hdl/` first. |
| `tb/maap/mutants.py` | `trial` `:89`; `controls` `:103`; `arms` `:124` | Each copy carries the same suite set as before. |
| `tb/pp_top/aecp_dispatch_mutants.py` | `trial` `:165`; `campaign` `:188` | `run` still deletes the generated ROMs and model directories before each build, so the README sentence stays true. |
| `tb/pp_top/aecp_mutants.py` | `trial` `:189`; `campaign` `:217` | `forget_generated_roms` is removed: a copy never carries a `*.hex`, so every build generates its ROMs from the generators as planted. |
| `tb/pp_top/gsi_mutants.py` | `check_variant` `:117`; `report` `:153`; `main` `:162` | Gains `--only NAME ...` (d3's syntax), so `--only` and `--jobs` combine here too. Its 8-CPU affinity cap is kept. |
| `tb/srp_admission/mutants.py` | `trial` `:84`; `campaign` `:94` | One copy per (variant, suite) run, 12 units. Gains `--only NAME ...`; the controls always run. |
| `tb/srp_top/mutants.py` | `trial` `:130`; `campaign` `:149` | Five labels grade two suites under one receipt name, so receipts are written in declared order: the later row's receipt wins, as in a serial run. |

`--only` keeps each driver's existing syntax: a comma list for adp, maap, aecp, dispatch and srp_top, and a name list for retry. Every driver was smoke-run with `--only` and `--jobs` of 2 to 4 before the commit, and each selected arm was KILLED by its named check.

## 2. Equivalence: `--jobs 1` against `--jobs 8`

Both runs of each driver used a `git archive` of `85da751`, whose driver code equals the head's, and Verilator 5.050. Each run was pinned to its own 4 of the host's 16 CPUs; Verilator's `-j 0` honours the pin and builds on 4 threads. Two checks were applied to each pair:

- The two summaries (stdout) are identical line for line: the same verdict and count for every unit, in the same order.
- Every receipt is identical in its `FAIL` lines and its tally lines, and `results.json` is identical where a driver writes one.

| Driver | Units | `--jobs 1` | `--jobs 8` | Summary | Receipts | `FAIL` lines | Against the README |
|---|---|---:|---:|---|---|---:|---|
| retry | baseline, 70 cases, restored | 408 s | 248 s | 71 lines, identical | 73 of 73 (with `coverage.txt`) | 2,640 | 62 KILLED, each count equal; 7 equivalence controls, 1 performance control |
| adp | 2 controls, 30 arms | 502 s | 333 s | 211, identical | 32 of 32 | 178 | 30 of 30 equal |
| maap | 3 controls, 29 arm runs | 253 s | 194 s | 101, identical | 32 of 32 | 189 | 29 of 29 equal (N FAIL of M) |
| dispatch | 4 controls, 37 arms | 1,059 s | 814 s | 265, identical | 41 of 41, `results.json` identical | 237 | 37 of 37 equal |
| aecp | 5 controls, 55 arms | 1,366 s | 1,079 s | 641, identical | 60 of 60 | 580 | 55 of 55 equal |
| gsi | golden, 20 variants, restored | 1,108 s | 713 s | 23, identical | 44 of 44, `results.json` identical | 9,899 | 20 detected |
| srp_admission | 4 variants x 3 suites | 791 s | 240 s | 13, identical | 12 of 12 | 8,358 | all nine mutant counts equal |
| srp_top | 11 controls, 78 arm runs | 2,258 s | 1,099 s | 91, identical | 84 of 84 | 687 | 90 of 90, assertion coverage 65/65 |

The speed-ups are modest because both N ran on the same 4 CPUs, where the builds are CPU-bound. That is also the size of the hosted runner. Each README records both wall times beside the option.

Eight `pp_top` workers need about 8 GB, at about 0.5 GB for Verilator plus 0.25 GB per compiler thread. So the `pp_top`-heavy `--jobs 8` runs (dispatch, aecp, gsi, adp) had nothing heavy running beside them.

## 3. The shared helper, `tb/common/mutant_pool.py`

- `DEFAULT_JOBS = 4` and `add_jobs_argument(parser)` keep the one default in one place.
- `in_order(work, units, jobs)` is a context manager. It runs the units on a `ThreadPoolExecutor(max(1, jobs))` and yields their results in declared order, whatever order they finish in. A unit's exception is raised at its turn.
- Leaving the block, by its end, a return or an exception, cancels the units not yet started and waits for the running ones.
- It is a context manager rather than a bare generator because a generator held in a local stays alive in an exception's traceback. The pool would then run every queued unit before the interpreter exits.

`d3_mutants.py`, `acmp_mutants.py` and `notify_mutants.py` are not changed. They already take `--jobs`, and their output order is outside this issue's eight. `tb/pp_top/README.md` now states `notify_mutants.py`'s existing option, whose default stays 1.

## 4. CI

The `suites` job runs five campaigns through their make targets, which now run at the default `--jobs 4`, the four vCPUs of `ubuntu-latest`. At four workers a `pp_top` campaign needs about 6 GB of the runner's 16 GB. No step needs another N, so no step passes one and the workflow is unchanged.

The job's steps were replayed at the head on 4 pinned CPUs with the default N. All are rc 0:

| Step | Result |
|---|---|
| `verilator --version` | 5.050 |
| `./scripts/lint_hdl.sh` | 41 modules |
| `./scripts/run_suites.sh` | 33 suites, 1,019,127 checks, 0 failing; `tb/pp_top` 9,168; µPC map gate (61 constants, 89 entry points) and M9 gate (30 opcodes, self-test 9/9) PASS |
| `make -C tb/srp_top mutants` | 90 of 90, coverage 65/65 (891 s); summary identical to the `--jobs 1` run's |
| `make -C tb/maap mutants` | 32 of 32 (136 s); summary identical to the `--jobs 1` run's |
| `make -C tb/adp_engine mutants` | 32 of 32 (286 s); summary identical to the `--jobs 1` run's |
| `make -C tb/pp_top aecp-mutants` | 5 controls PASS, 55 of 55 KILLED (954 s); summary identical to the `--jobs 1` run's |
| `make -C tb/pp_top aecp-dispatch-mutants` | 4 controls PASS, 37 of 37 KILLED (734 s); summary identical to the `--jobs 1` run's |
| `python3 scripts/gen_matrix.py --check` | 94 rows, 0 untested |
| `make -C tb/nvm_port figures` (in a clone, after fetching `refs/pull/13/head` as CI does) | all measured figures agree with the tree (260 s) |

The `docs-gates` job, in a clone at the head: `check-links.py` (1,035 links), `check-matrix.py` (115 REQ rows, 17 GAP findings), `check-integrator-params.py` (27 parameters), `render-wavedrom.py --check` (18 blocks) and `make stale`, all rc 0. `make check` also passes (41 mermaid and 18 wavedrom blocks), and so does `git diff --check 631eeb34 HEAD`. The `portability` job's `./syn/yosys/run.sh` elaborates all 36 tops and the one Xilinx mapping, rc 0.

## Validation of the other campaigns at the head

Each ran from a `git archive` of `ab8a50b`. All are rc 0:

| Campaign | Result |
|---|---|
| `python3 tb/pp_top/d3_mutants.py --jobs 2` | 87 of 87 KILLED, 3 goldens PASS (3,492 s); the 75 `tb/pp_top` rows, the 11 `tb/acmp_nvm` rows and the `tb/rx_validator` row each equal their README's count |
| `python3 tb/pp_top/acmp_mutants.py --jobs 1` | 19 of 19 KILLED, 3 goldens PASS; every count equals its README row (14 in `tb/pp_top`; 93, 50, 40 and 30 in `tb/acmp_listener`; 27 in `tb/rx_validator`) |
| `python3 tb/pp_top/notify_mutants.py --jobs 1` | 40 of 40 KILLED, 5 goldens PASS; every count equals the README |
| `python3 tb/pp_top/name_wr_mutant.py` | decode killed; golden and restored PASS |
| `python3 tb/desc_mem_guard/mutate.py` | hold-deleted mutant detected by the completed byte assertion |
| retry, gsi and srp_admission | the equivalence runs above (driver code at `85da751` equals the head's) |

## Parent consumer gates (milan-fpga dev `cdf49d1a`)

The scratch parent is a `git archive` of a read-only checkout at `cdf49d1a`, committed in a fresh repository. Its tree (`904f3079`) and its index (984 entries, 4 gitlinks) equal that checkout's.

- `gptp-processor` (`5dce647a`) and `third_party/verilog-axis` (`48ff7a7e`) are at their recorded pins, fetched from their recorded URLs. `external` is recorded and uninitialised.
- `protocol-processor` is a clone of this branch at `ab8a50b`, with the gitlink staged at it.
- `parent-adoption-c4c6-ea3fb388.patch` is applied: the C6 binding in `KL_pp_shadow.sv` and the acmp/notify disposition lines in `measure_test_evidence.py`. Apart from the gitlink, it is the only change against `cdf49d1a`.

Each gate ran with Verilator 5.050. The `make -j16` builds were pinned to 4 CPUs, and `xvlog` never ran beside a Verilator build. All 16 are rc 0:

| # | Gate | Result |
|---:|---|---|
| 1 | `check_cpp_idiom.py` | every ratchet held (167 translation units) |
| 2 | `check_py_idiom.py` | every ratchet held: 0 unannotated and 0 undocumented public functions, 0 over-long lines, 7 <= 7 too many parameters |
| 3 | `xvlog_gate.py --check` | 4 findings == ratchet, none new, 0 under `hdl/`; pinned at `protocol-processor@ab8a50be` |
| 4 | `check_rtl_source_lists.py` | OK; protocol-processor 36/42 tops, 6 recorded |
| 5 | `pp_srcs.py --check --selftest` | OK |
| 6 | `sw/builder/test_builder.py` | all gates pass except 1 not run: the calibration gate needs a board build tree that is not on this host |
| 7 | `make -C tb/verilator/pp_shadow -j16` | 606, 606, 646 and 311 checks, 0 failures |
| 8 | `check_port_contracts.py` | OK; 49 literal-bound, 59 without a rationale, lowerable by 3 |
| 9 | `measure_naming.py --check` | 96 recorded |
| 10 | `measure_test_evidence.py --check` | 72 <= 77 suites without a mutation arm, 10 <= 10 unseeded draw sites, 0 <= 0 unexplained DUT-source readers, 3 <= 3 wall-clock-dependent files |
| 11 | `docs_check.py` | 0 findings |
| 12, 13 | `make -C tb/verilator/nvm_cosim lint`, `quick` | lint clean; 315 of 315 |
| 14 | `make -C tb/verilator/milan_dp -j16` | every RESULT PASS (9); the gmstep mutants 6 of 6 |
| 15 | `make -C tb/verilator/milan_dp_render -j16` | leg defects 5/5 |
| 16 | `lint_rtl.py --check` | 90 <= 90 |

## Parent-visible list

- No interface, RTL or behaviour change, and no port, parameter, register-map or microcode change.
- No parent registry entry and no budget change:
  - The parent's evidence gate classifies `retry_mutants.py`, `gsi_mutants.py` and `srp_admission/mutants.py` as DUT-source readers, and they still are, so their dispositions stay valid.
  - The other five drivers, and the new helper, read no `hdl/` path.
  - No driver reads host time or sets a process deadline; the wall times were measured outside the drivers. So the wall-clock ratchet stays at 3 <= 3.
  - The parent's own idiom and evidence predicates, run on each changed file at base and head, find nothing new.
- The processor's own check totals are unchanged by this lane (only campaign scripts changed): `tb/pp_top` 9,168, the sweep 1,019,127.
