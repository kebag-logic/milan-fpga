# [A434] Round 4 handoff: PR #618 / issue #617

Status: REVIEW READY at `35f58b9cca1de9215f787872734e6a9040f82c19` (local branch, not pushed; this lane may not push). All 87 assigned gates rc 0 at that head; 13 suites, 52,288 checks, 0 failures; `capture_coherence` projected at 1,024 s hosted against its 1,800 s guard.

- Repository: kebag-logic/milan-fpga, origin `https://github.com/kebag-logic/milan-fpga.git` (confirmed).
- Lane: `$LANES/617-capture-frame-atomic`, branch `617-capture-frame-atomic`.
- Round-4 start: `ddb0774779d10a9b0bd90a4822f4e5df9fdedb1b` (confirmed HEAD). Branch base: dev `ce550952e47fbd92367f0d9b099345100f7f4215`.
- Head: `35f58b9cca1de9215f787872734e6a9040f82c19`, three round-4 commits on `ddb07747` (thirteen on dev):
  - `1e66db70b` Build the capture_coherence datapath legs under any inherited MAKEFLAGS, run the mutation arm in parallel and refuse a literal keep-off binding (`tb/verilator/capture_coherence/{Makefile,mutants.py,mga_keepoff.py}`, `tb/verilator/{media_nco,chmap_capture}/Makefile`).
  - `035dbedef` State the below-nominal on-crossing side as a gradual stretch and the settled lock as recorded converged (docs, RTL comments, harness comments).
  - `35f58b9cc` Make the capture_coherence datapath ROM images once before the mutation arm's parallel builds (`mutants.py`: `ROM_IMAGES`, `rom_images_result()`). Found in my own review of the parallel arm after a full gate pre-run at `35f58b9c` (86 of 86 rc 0, `evidence/gate-summary-035dbede.txt`): run alone from a clean suite directory, several dp builds would each generate `ltn_rom.hex` and `ucode.hex` in the suite directory at once. Benign (identical bytes, and no harness reads them until its build is done) but untidy; now made once before the pool starts, a no-op when the `dp` leg already made them.
- Rulings: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5881942681
- Reviews answered: R394-3 (PR #618 comment 5881895622: F1 MAJOR, S1-S4) and R395-3 (comment 5881941735: F1 BLOCKER, S1-S4).
- Roles: executor [A434]; internal reviewer [R394]; external reviewer [R395].
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5881952742
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5883145371
- Work directory (scratch, outside the tree and this output directory): `$VALIDATION_STORAGE/617-a434-work` (`logs/`, `gates/`, the `scratch/` tree exports, `tools/make43`).
- Tools: Verilator 5.050 (`$VALIDATION_TOOLS/verilator-v5.050/bin` first on PATH), Yosys 0.66, sv2v v0.0.13 (CI pins v0.0.12), host GNU make 4.4.1, and GNU make 4.3 built in the work directory from the GNU release tarball (`make-4.3.tar.gz` sha256 `e05fdde47c5f7ca45cb697e973894ff4f5d79e13b750ed57d7b66d8defc78e19`; binary sha256 `71267283f3424f6e607cf634cf12499041f54b92e14f1fdad314e2739377382b`): the make the hosted `ubuntu-24.04` image ships.
- CPUs: this session's affinity is CPUs 64-79 (16; the host has 128). Every timing run is pinned with `taskset` to four of them, otherwise idle during the measurement (sampled 0% busy before the first run).
- Tree exports: timing and reproduction runs used `git archive` exports of the exact commits plus `git archive` of the three pinned submodules (script `export.sh`; protocol-processor gets a scratch-local git repo so `pp_srcs.py` can list it). The lane was never built into for timing; gates ran in the lane itself (section 6).

## 1. MAKEFLAGS reproduction, before and after

### The cause, confirmed

The hosted image's GNU make 4.3 hands a recipe run under `make -C` `MAKEFLAGS=w`; 4.4.1 does not (`logs` probe: a recipe `echo "[$$MAKEFLAGS]"`):

| make | `make -C dir` | `cd dir; make` |
|---|---|---|
| GNU Make 4.3 | `recipe MAKEFLAGS=[w]` | `recipe MAKEFLAGS=[]` |
| GNU Make 4.4.1 | `recipe MAKEFLAGS=[]` | `recipe MAKEFLAGS=[]` |

`scripts/run_all_suites.sh:390` runs `make -C <suite>`; the `mutants` recipe runs `python3 mutants.py`, whose `make -s -C <suite> dp-build` inherited `w`. The Makefile's `DP_SRCS := $(shell $(MAKE) -s -C ../milan_dp print-srcs ...)` then began `make[1]: Entering directory ...`. R394-3 inferred make 4.3; this confirms it with make 4.3 itself.

### Before (`ddb07747`): `evidence/mf-repro-before.txt`

| Reproduction | Result |
|---|---|
| `mf_repro.py` (the committed `mutants.build('dp')`), host make 4.4.1, no MAKEFLAGS | builds; `DP_SRCS starts: ../../../protocol-processor/hdl/acmp/pp_acmp_pkg.sv ...` |
| same, `MAKEFLAGS=w` (R394-3's reproduction) | no harness ("did not compile"); `DP_SRCS starts: make[1]: Entering directory .../milan_dp` |
| the hosted chain: make 4.3 on PATH, `make -C <dir>` -> recipe -> `mutants.build('dp')` with what it inherited (`w`) | no harness; the same `Entering directory` list |
| the same chain under make 4.4.1 | builds |
| the whole suite, `make -C tb/verilator/capture_coherence` under make 4.3, 4 CPUs (run B1, section 3) | junction 20,832 / 0, dp 332 / 0, arm `27 checks: 23 PASS, 4 FAIL`: the dp and dp-band controls and both mutants "did not compile" - the hosted shard 1/5 signature exactly |

### After (`35f58b9c`)

| Reproduction | Result |
|---|---|
| R394-3's own `scripts/r394_mf_repro.py` (read from its packet, unchanged) at the lane head, `MAKEFLAGS=''` and `MAKEFLAGS=w` | both `built Vcoherence_dp`; under `w` the nested list starts with the processor packages (gate `makeflags_repro`, section 6) |
| the hosted chain under make 4.3 at the lane head | `built Vcoherence_dp` (same gate) |
| the whole suite under make 4.3, 4 CPUs (run A1) | rc 0: junction 20,832 / 0, dp 332 / 0, arm `30 checks: 30 PASS, 0 FAIL` |
| each fix alone, on `ddb07747` (`evidence/mf-repro-layers.txt`) | round-4 `mutants.py` with the old Makefile: builds (the nested list is still contaminated, but `build()` empties MAKEFLAGS); round-4 Makefile with the old `mutants.py`: builds, the nested list clean. Both under make 4.4.1 with `MAKEFLAGS=w` and under the make 4.3 chain |

### The fix (file:line at `35f58b9c`)

- `tb/verilator/capture_coherence/Makefile:101` and `:105`: both nested calls are `$(shell $(MAKE) -s --no-print-directory -C $(DP_DIR) ...)`; the comment above (`:93-96`) says why.
- `tb/verilator/capture_coherence/mutants.py`: `BUILD_MAKEFLAGS = ""` (`:118-123`); `build()` (`:334`) runs the recipe with `MAKEFLAGS` emptied, in its own session (`run_child()`, `:277`), and keeps its output (`build_log()`).
- New committed check `makeflags_result()` (`:485`): `make -s -C <suite> dp-build` under `MAKEFLAGS=w` must build (it bypasses `build()`, so it holds the Makefile fix alone). It fails with either `--no-print-directory` removed and with the `ddb07747` Makefile (`evidence/makeflags-check-can-fail.txt`).

## 2. Build-failure diagnostics

- `build()` keeps each build's combined make and compiler output (`build_log()`), and every failed-build verdict prints its last `BUILD_TAIL_LINES = 40` lines, indented `      | ` under the `[FAIL]` line (`build_tail()`): in `mutant_result()`, `control_results()`, `refusal_result()`, `makeflags_result()`.
- A planted build break, graded as a dp mutant through each tree's own `grade_mutant()` (`evidence/planted-break-demo.txt`):
  - `ddb07747`: `[FAIL] mutation 'planted build break ...' did not compile; ...` and nothing else.
  - `035dbede`: the same line, then `%Error: <tmp>/.../milan_datapath.sv:5722:9: syntax error, unexpected IDENTIFIER-for-type`, the source line with its caret, `%Error: Exiting due to 1 error(s)` and `make: *** [Makefile:125: dp-build] Error 1`.
- The original hosted failure, replayed with the Makefile fix removed (`evidence/makeflags-cause-tail.txt`): the tail now names it, `%Error: Cannot find file containing module: 'Entering'`, `'directory'`, the milan_dp path, `'Leaving'`.
- New committed check `build_break_result()` (`:502`): a syntax error appended to the dp leg's datapath must fail the build, and the printed tail must carry Verilator's `%Error:` on the planted file. Its `[PASS]` line quotes that error, so every run's log shows the diagnostics working.

## 3. Suite timing, before and after, and the hosted projection

Each run: `make -C tb/verilator/capture_coherence` from a clean suite directory, exactly as `run_all_suites.sh` runs it, under GNU make 4.3 (the hosted chain), `taskset` to the CPUs named; wall from `timed_suite.sh`; per-leg times from a monitor polling the log each second (the legs print their verdicts at exit), so each is within about 1 s.

| Run | Tree | CPUs | Wall | Junction leg | dp leg | Arm | Arm tally | rc |
|---|---|---|---:|---:|---:|---:|---|---:|
| B1 | `ddb07747` | 76-79 | 990.5 s | | | | 23 / 27 (4 dp items "did not compile") | 2 |
| B2 | `ddb07747` | 72-75, alongside A1 | 990.8 s | 247.7 s | 128.5 s | 614.6 s | 23 / 27 (the same 4) | 2 |
| A1 | `035dbede` | 76-79, alongside B2 | 703.4 s | 260.6 s | 123.5 s | 319.3 s | 30 / 30 | 0 |
| A2 | `035dbede` | 78-79 (two CPUs), alongside the gate pre-run | 1,014.3 s | 261.9 s | 132.6 s | 619.8 s | 30 / 30 | 0 |
| A3 (the timing gate) | `35f58b9c` | 76-79, alongside B3; foreign processes on these CPUs | 818.7 s | 305.0 s | 144.9 s | 368.8 s | 30 / 30 | 0 |
| B3 | `ddb07747` | 72-75, alongside A3; the same foreign load | 1,111.6 s | 298.0 s | 148.9 s | 664.7 s | 23 / 27 (the same 4) | 2 |

Hosted at `ddb07747` (both reviews' receipts): shard 1/5 ran `capture_coherence` 00:23:11 -> 00:47:13, 1,442 s, with the same four dp items failing fast.

- Hosted/local ratio at `ddb07747`: 1,442 / 990.65 = **1.456** (B1 and B2, quiet, agree within 0.3 s).
- **Projected hosted wall at the head: 703.4 x 1.456 = 1,024 s** (A1, quiet; `035dbede` differs from `35f58b9c` only by the ROM-image step, a no-op after the `dp` leg), against the default 1,800 s per-suite guard: 776 s (43%) of margin; 476 s under the ruling's 1,500 s target.
- The timing gate at `35f58b9c` itself (A3) ran while other lanes' processes (container builds and another suite's simulations) had spread onto CPUs 64-79, all 16 at 100%. Paired with B3 under the same load: 818.7 x 1,442 / 1,111.6 = **1,062 s** projected. The most pessimistic combination, A3 against the quiet ratio, is 818.7 x 1.456 = 1,192 s. Every estimate is under 1,500 s.
- No suite-specific guard: `scripts/run_all_suites.sh` is not edited.
- What a fix without the schedule would have cost: the arm's dp items cost 282.1 s on 4 CPUs one at a time (profile below), so the serial suite with the dp legs building is about 990.6 + 282.1 = 1,272.7 s locally, 1,853 s hosted: over the guard (R394-3 projected about 1,900).
- The ratio comes from a mostly serial run (118% CPU in B1/B2); A1 averages 233%. If the hosted runner's four vCPUs were two cores with SMT, the arm's parallel speed-up there would be smaller. A2 bounds that case: the head on two CPUs, and contended by the gate pre-run, took 1,014.3 s, 1,477 s projected: still inside 1,500 s and the guard.

Per-item profile of the `ddb07747` arm on 4 CPUs, one item at a time (`evidence/arm-profile-ddb0774-4cpu.tsv`): 27 items, builds 194.9 s, runs 734.6 s, 929.5 s in all; the largest build process 375 MB (a dp build), so four concurrent builds fit the hosted runner's memory.

| Leg | Items | Build + run, s | Longest item, s |
|---|---:|---:|---:|
| junction | 9 | 178.5 | 22.0 |
| band | 4 | 107.3 | 27.5 |
| band50 | 2 | 38.6 | 19.6 |
| fine | 2 | 86.9 | 43.6 |
| dp | 2 | 130.5 | 65.7 |
| dp-band | 2 | 151.6 | 76.1 |
| chmap | 4 | 209.1 | 53.1 |
| nco | 2 | 27.0 | 13.5 |

The schedule (ruling 2), `mutants.py` `run_units()` (`:552`) / `arm_units()` (`:541`) / `control_groups()` (`:476`) / `rom_images_result()` (`:517`):

- One unit = one build and the harness runs graded on it; a pool of `len(os.sched_getaffinity(0))` workers (4 on the hosted runner; 4 under `taskset` here).
- The dp and dp-band controls build the same clean datapath the same way (`control_groups()` groups legs by recipe and source), so one build serves both: 29 builds for 30 checks.
- The whole-datapath units start first (longest), then the rest in list order; results print in the fixed list order as soon as every earlier unit is done, so the log is deterministic.
- The dp harness's ROM images are made once before the pool starts (`ROM_IMAGES`, `:130`), so no two dp builds generate them at once.
- Every child (build or harness) leads its own session and is registered; the SIGTERM/SIGINT handler (`stop()`, `:306`) kills every group in flight, starts nothing more, and the temporary directory is removed. No host deadline is added (the wall-clock ratchet stays 3 <= 3).
- No mutant left the PR gate: no quick/full split, the default guard unchanged.

## 4. Mutant table

`tb/verilator/capture_coherence/mutants.py` at `35f58b9c`: 8 legs, 2 build checks, 8 clean controls (7 builds), 20 mutants: `30 checks: 30 PASS, 0 FAIL` (A1, and the gate run in section 6).

| # | Leg | Check or mutant | Named check that must fail | Round |
|---|---|---|---|---|
| B1 | dp | the dp recipe builds under an inherited `MAKEFLAGS=w` | (a build must succeed) | 4 |
| B2 | dp | a planted build break fails the build and its `%Error` is printed | (the tail must carry it) | 4 |
| C1-C8 | junction, band, band50, fine, dp, dp-band (one shared build), chmap, nco | clean controls | none | 1-3 |
| M1-M8 | junction | per-pair law of `ce550952`, no snapshot, first-pair close, late publish, unwritten stage, coincidence law ignored, round-1 snapshot instant, round-1 counter law | as in round 3 | 1-2 |
| M9-M11 | band | round-1 aligner binding; 1/128-sample keep-off; tick not delayed | `[C] slips while the CRF lock held` (M9, M10); `[C] CRF slips net zero` (M11) | 2 |
| M12 | dp | `milan_datapath` tells the crossbar a one-pair frame | `[A] AAF columns mixing two TDM frames` | 1 |
| M13 | dp-band | `milan_datapath`'s round-1 aligner binding | `[C] slips while the CRF lock held` | 2 |
| M14-M16 | chmap | RM1 (close on the bucket's last pair), RM7, RM8 | `F1: ...`, `Q: col 2 pair 0 L is frame 4`, `Q: col 1 pair 2 L is frame 2` + `Q: col 2 ...` | 2-3 |
| M17 | band50 | RM5: `MGA_KEEPOFF_CYC_C` 256 -> 128 | `[C] slips while the CRF lock held` | 3 |
| **M18** | **band50** | **RM9: `.LOCK_KEEPOFF_CYC_P (128)` in `milan_datapath`, the declaration left at 256** | **build refusal `does not bind LOCK_KEEPOFF_CYC_P to MGA_KEEPOFF_CYC_C`** | **4** |
| M19 | nco | the `==` terminal compare | `update landing at old end +0: ...` | 3 |
| M20 | fine | the `==` terminal compare | `[C] CRF slips net zero` | 3 |

M12 and M13 are the two mutants the hosted runner never built before this round; at `35f58b9c` they build and are caught under the make 4.3 chain (A1).

RM9 (R394-3's `rm9.diff`, the same line): `mga_keepoff.py` (`:48-50`, `:68-74`) now requires the datapath's one `.LOCK_KEEPOFF_CYC_P (...)` binding to be `MGA_KEEPOFF_CYC_C`; anything else (a literal, a second binding, none) fails the junction build with the message above. `mutants.py` grades such a mutant through `Refused` / `refusal_result()`: caught only when its build fails and prints the named refusal; if it builds, it SURVIVED. At `ddb07747` RM9 passed the datapath leg 332 / 0 and `--band` 198 / 0 (R394-3).

## 5. Suggestions taken (ruling 3)

| Suggestion | Where (file:line at `35f58b9c`) | What |
|---|---|---|
| R394-3 S1 (RM9) | `tb/verilator/capture_coherence/mga_keepoff.py:16-22,35-36,48-50,68-74`; `mutants.py:243-246` (RM9), `:136-139` (`Refused`), `:404` (`refusal_result()`); `Makefile:75-77`; `milan_datapath.sv:5693-5694` (comment) | a literal (or any other) keep-off binding in `milan_datapath` fails the junction build by name; RM9 killed by that refusal |
| R394-3 S3 = R395-3 S1 (the below-nominal limit) | `docs/design/TIME_SYNC.md:548,557-559`; `docs/reference/REGISTER_MAP.md:1958-1967`; `hdl/ieee1722/aaf/KL_chan_map_capture.sv:96-106` (banner); `hdl/milan/milan_datapath.sv:5678-5680` (comment); `tb/verilator/capture_coherence/coherence_bench.hpp:73-75,82-87,356`; PR body | above nominal a sharp limit, about 67 ppm (net zero by column 8 at +66, carried across from +67); below nominal no sharp limit: one net-zero pair, later with the rate (column 426 at -63, 1,323 at -66, about 1,700 at -67, 2,918 at -70; the close at most 2 cycles past the crossing through -66, 6 at -70), as R394-3 and R395-3 measured. Every "63/67" is gone (`git grep` for `63 ppm`, `63/67`, `63 below`: none). The grading law (`engage_columns()`) is unchanged |
| R394-3 S2 = R395-3 S4 (CRF-settle) | `docs/design/TIME_SYNC.md:470,551-552,570`; `REGISTER_MAP.md:1951-1956`; `sim_main.cpp:70-83,698-699`; `Makefile:14-15`; `CHANGELOG.md:49-51`; `docs/testing/TESTING.md:490`; crossbar banner and datapath comment | "settled" made literal by citation, not by lengthening the committed runs: CRF-settle is stated as grading the approach (no slip in the second half of 30,000 columns, while the close converges; time constant about 13,000 frames, R394-3); the converged lock is RECORDED. My own 150,000-column runs of the committed placements at -80, +80, -100, +100, -150 and +150 ppm (`evidence/settle-150k-*.log`, built from the head harness with only the settle list changed): 12 engagements, 42 / 0 checks each, second-half spread 1-3 cycles, the tick 255-256 cycles after the close on the negative side and 778-786 on the positive (close 256-264 cycles off; 255-257 for the pulled engagements), no tail slip; acquisition pairs net zero, last at columns 6,056-19,513 |
| R395-3 S2 (`TRIMW_P = 18`) | PR body, round-3 area line and Round 4 | the NCO area figures name the elaboration: `KL_media_nco` alone at `TRIMW_P = 18`, as `milan_datapath` binds it |
| R395-3 S3 (absolute `MDIR`) | `tb/verilator/media_nco/Makefile:39` | `run` executes `$(abspath $(MDIR))/Vmedia_nco_sim`. The same `./$(MDIR)/...` form, also introduced by this PR with an overridable objdir, is fixed alike in `tb/verilator/chmap_capture/Makefile:27` and in `capture_coherence`'s `run` and `dp` (`Makefile:85,130`) |

Not taken: none. R394-3 S4 (headroom) is ruling 2 (section 3).

## 6. Gate table

All at head `35f58b9cca1de9215f787872734e6a9040f82c19`. The tree was clean before and after (`git status --porcelain` empty), the 13 suites' build directories were cleaned first, and every gate ran from the physical path `$LANES/617-capture-frame-atomic`, unpiped, with its own log and rc, in four detached streams waited for in the foreground (`run_gates.sh`). Markdown gates ran in `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python`; `GIT_CONFIG_*` core.commitGraph=false (this worktree's git warns on stderr). **87 entries, all rc 0**: the round-3 set (85, the same names and commands), the `MAKEFLAGS=w` reproduction, and the 4-CPU timing. Full list with each command and seconds: `evidence/gate-summary-35f58b9c.txt`; logs under 200 KB in `evidence/gate-logs/`, the rest by sha256 in `evidence/large-logs-sha256.txt`. A full pre-run at `035dbede` (86 of 86 rc 0, `evidence/gate-summary-035dbede.txt`) preceded the ROM-image commit.

| Gate | Command | rc | Result |
|---|---|---:|---|
| `MAKEFLAGS=w` reproduction | `bash mf_gate.sh` (R394-3's `r394_mf_repro.py` read from its packet, and the make 4.3 chain, at the lane head) | 0 | R394-3 script: `built Vcoherence_dp` with `MAKEFLAGS=''` and with `'w'`, the nested list clean under `w`; make 4.3 chain: `built Vcoherence_dp` (`evidence/gate-logs/makeflags_repro.log`) |
| 4-CPU timing | `make -C tb/verilator/capture_coherence`, `git archive` of the head, make 4.3, `taskset -c 76-79` (A3) | 0 | 818.7 s under foreign load; junction 20,832 / 0, dp 332 / 0, arm 30 / 30; projections in section 3 |
| Builder bank | `python3 sw/builder/test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs a local Arty mf48 build report, absent here), 835 s |
| Lint ratchet | `python3 scripts/lint_rtl.py --check` | 0 | PASS: 90 violations <= ratchet 90; 17 waived, 0 justified lint_off |
| xvlog | `python3 scripts/xvlog_gate.py --check` | 0 | PASS: 4 findings == ratchet; 0 in `hdl/`, 4 in the pinned processors |
| Yosys | `syn/yosys/run.sh --top milan_datapath` / `KL_chan_map_capture` / `KL_media_nco` | 0 | TAP-PURITY RESULT: PASS each; 332 / 10 / 3 s |
| OOC | `OOC_CHPARAM="N_SLOTS_P=4 N_TDM_P=8 N_LB_STREAMS_P=1 N_LB_CH_P=8" syn/yosys/ooc.sh KL_chan_map_capture` | 0 | LUT 1265, LUTRAM 32, FF 1384, BRAM 0, CARRY4 34 (unchanged) |
| `capture_coherence` | `make -C tb/verilator/capture_coherence` (host make 4.4.1, 16 workers) | 0 | junction 20,832 / 0; datapath 332 / 0; arm `30 checks: 30 PASS, 0 FAIL`; 636 s beside the other streams |
| `chmap_capture` | `make -C tb/verilator/chmap_capture` | 0 | 371 / 0 + netlist 20 / 0 |
| `media_nco` | `make -C tb/verilator/media_nco` | 0 | 410 / 0 |
| `media_grid_align` | `make -C tb/verilator/media_grid_align` | 0 | 45 / 0; negative controls MGA_MUT_U_SIGN, MGA_MUT_NO_KEEPOFF, MGA_MUT_COIN red as required |
| `crf_rx`, `crf_tx`, `mmcm_servo`, `mmcm_servo_autorepair` | `make -C tb/verilator/<suite>` | 0 | 16,116 / 127 / 311 / 47 checks, 0 failures |
| `tdm`, `pair_fill`, `pp_shadow` | `make -C tb/verilator/<suite>` | 0 | 58 / 41 / 2,120 checks, 0 failures |
| `milan_dp_render` | `make -C tb/verilator/milan_dp_render` | 0 | 222 / 0 |
| `milan_dp` | `make -C tb/verilator/milan_dp` | 0 | 11,206 / 0 |
| Suite tally | `scripts/suite_tally.py` over the 13 suite logs, and `--verdict` per log | 0 | 52,288 checks, 0 in-suite failures (`evidence/suite-tally-35f58b9c.txt`); round 3 had 52,285: the arm's 27 became 30 |
| Markdown | `docs_check`, `check_em_dash --base ce550952...` (0 findings over 373 added lines in 20 pages) and `--selftest`, `gen_toc --check/--verify-anchors/--selftest`, `check_doc_style` and `--selftest`, `check_doc_paths`, `check_feature_status` and `--self-test`, `gen_module_matrix --check`, gptp/solution/submodule docs, `DOC_MAP.gen --check`, `check_archive` | 0 | PASS |
| Code quality | sv/cpp/py/sh idiom, hygiene, naming, port contracts, fail-fast, test evidence (wall-clock ratchet 3 <= 3, DUT readers 0 <= 0), TODO ownership, cohesion/control-flow self-tests, each with its `--selftest` | 0 | PASS |
| Source lists and scope | rtl source lists, SoC sources, `pp_srcs`, wire accountability, CI events, ci_scope self-test, bare-metal, NVM record space, diagrams | 0 | PASS |
| HDL reference | `gen_hdl_reference.py --output <work>/gates/hdlref-out` and `--selftest` (pyslang 11.0.0 venv) | 0 | built |

Recorded (not gates): the 150,000-column settle runs (section 5, `evidence/settle-150k-*.log`), the layer isolation (section 1), the planted-break and hosted-cause demonstrations (section 2), the 2-CPU run A2 (section 3).

Not run: the whole-tree sweep `scripts/run_all_suites.sh` (the affected suites were assigned), the act replica and hosted CI (nothing pushed; this lane may not push), bench acceptance 4.

## 7. Open risks

- **Hosted duration at the head is not observed.** The projection (1,024 s quiet, 1,062 s paired under load, 1,192 s at worst) uses the hosted/local ratio of a mostly serial run. A2 bounds a runner whose four vCPUs behave as two cores: 1,477 s projected. All are inside the default 1,800 s guard. The manager checks hosted `verilator-suites` at the pushed head.
- **Make 4.3 on the hosted image is inferred from `ubuntu-24.04`**, as R394-3 said, but the whole-suite run under make 4.3 reproduces the hosted shard's arm result exactly (the same four items, `27 checks: 23 PASS, 4 FAIL`), and the fixed head passes under make 4.3.
- **The same nested pattern elsewhere.** `tb/verilator/pp_shadow/Makefile:107` and `tb/verilator/milan_dp_render/Makefile:57,62` also evaluate `$(shell $(MAKE) -s -C ../milan_dp print-...)` without `--no-print-directory`. They are safe where they run today: at the top-level parse of `make -C <suite>`, which make 4.3 does not hand `w` (the hosted `capture_coherence` dp leg, parsed the same way, passed at every head). Only a recipe-run nested build, like this arm's, meets it. Not changed (out of this assignment's scope); a candidate follow-up for the manager.
- **The below-nominal restatement cites the reviewers' probes** (R394-3, R395-3), as ruling 3 asked; I did not re-probe -63 to -70 ppm myself. The committed grading does not depend on it.
- **The converged-lock claim is recorded, not committed**: my 150,000-column runs (±80, ±100, ±150 ppm) and R394-3's (±100, ±150). The committed `CRF-settle` grades the approach only, by design (ruling 3: no lengthened committed runs).
- **The Makefile `run`/`dp` absolute-`MDIR` fix** was applied to three suites (the one ruling named and the two this PR's other overridable objdirs use); `render_setpoint`'s `./$(MDIR)/$(EXE)` predates this PR and is unchanged.
- Local sv2v is v0.0.13; CI pins v0.0.12.

## 8. Log (2026-09-29, CEST)

- 03:34: confirmed origin and HEAD `ddb07747`, submodule toplevels. Read #617 in full, the round-4 rulings, R394-3 and R395-3, both review packets and the round-3 author packet.
- 03:36: posted TAKEN (https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5881952742).
- 03:38: built GNU make 4.3; `make -C` hands a recipe `MAKEFLAGS=w`, 4.4.1 does not. Reproduced the dp build failure at `ddb07747` with R394-3's shape and with the make 4.3 chain.
- 03:41-03:58: B1, the `ddb07747` suite under make 4.3 on 4 CPUs: 990.5 s, arm 23 / 27 (the hosted signature). Per-item arm profile on 4 CPUs.
- 03:45-04:00: Makefile `--no-print-directory`; `mutants.py` controlled MAKEFLAGS, build tails, parallel schedule, shared dp control build, the two build checks, RM9 via `mga_keepoff.py`'s binding check; the MAKEFLAGS check shown to fail without either fix; recorded 150,000-column settle runs; docs and comments; arm 30 / 30 on the working tree.
- 04:01: committed `1e66db70`, `035dbede`.
- 04:02-04:18: A1 (703.4 s, 30 / 30) beside B2 (990.8 s, 23 / 27). Layer isolation; planted-break and hosted-cause demonstrations.
- 04:20-04:48: gate pre-run at `035dbede`, 86 / 86 rc 0; A2 (2 CPUs) 1,014.3 s.
- 04:48: my review of the parallel arm: ROM images could be generated by several dp builds at once when the arm runs alone; committed `35f58b9c` (made once before the pool).
- 04:48-05:07: A3 (818.7 s, 30 / 30) beside B3 (1,111.6 s), both under foreign load on CPUs 64-79.
- 05:07-05:35: final gate run at `35f58b9c`: 86 / 86 rc 0 (87 with the timing gate); suite tally 52,288 / 0.
- 05:40: evidence assembled; PR-BODY.md Round 4 written; posted REVIEW READY (https://github.com/kebag-logic/milan-fpga/issues/617#issuecomment-5883145371). Stopped: no push, no PR edit, no other comment.
