# [A298] Issue #443 handoff

Status: local author assignment complete; ready for independent review.
Every requested gate command returned zero. Builder gate 11 was NOT RUN.
Base: `0755923d983218ca6ca9db6891a558cbe6425b8d`
Branch: `443-render-csr`
Head: `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e`
Scope: assignment items 1, 2, 3 and 5; no STREAM_INTERRUPTED wiring.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/443#issuecomment-5826079535

## Layout table

`RENDER_STAT` at `0x8DC`; existing `STRM_SEL` listener selection.

| Bits | Width | Meaning | Reset |
|---|---|---|---|
| 7:0 | 8 | Selected listener fill, events; bounded, no wrap | 0 |
| 8 | 1 | Prefill level | 1 when present |
| 9 | 1 | Converged level | 0 |
| 15:10 | 6 | Reserved zero | 0 |
| 31:16 | 16 | Global rails; saturates at 65535 | 0 |

Absent stage, talker selection or invalid listener: zero. The current
root always instantiates the stage; disabled output interfaces are not absence.
The control elaboration removes the stage and ties its outputs to zero.
No STREAM_INTERRUPTED wiring.

## Changes

- `hdl/common/csr/milan_csr.sv:437`: packed status input; `:922` address; `:2389` live selection; `:2561` aperture decode
- `hdl/milan/milan_datapath.sv:1202`: early net declaration; `:2588` CSR connection; `:6162` per-listener packing
- `hdl/ieee1722/aaf/KL_render_setpoint.sv:193`
- `docs/reference/REGISTER_MAP.md:1940`
- `docs/reference/REGISTER_MAP_CLASSES.md:107`
- `docs/design/TIME_SYNC.md:273`
- `docs/AAF_LATENCY_TAPS.md:96`
- `tb/verilator/milan_dp/sim_aclk.cpp:367`: live read and backpressure; `:413` rail; `:428` absence
- `tb/verilator/milan_dp/render_csr_controls.py:23`: absent source; `:37` control campaign
- `tb/verilator/milan_dp/Makefile:408`
- `tb/verilator/milan_dp/README.md:793`
- `tb/verilator/milan_dp_render/sim_tdm8_render.cpp:3277`

## Test evidence

| Test | Command/mode | Result |
|---|---|---|
| Focused CSR behavior | `make -C tb/verilator/milan_dp render-csr-controls`; clean `--render-csr-only` | 62 checks, 0 failures |
| Two-listener render | `make -C tb/verilator/milan_dp_render` | 64 checks, 0 failures; five added selector checks |
| Shipping render | Same default suite | 150 checks, 0 failures |
| TDM render controls | Same default suite | 5/5 controls passed |
| Setpoint render controls | Default datapath sweep | 6/6 controls passed |
| Grandmaster-step controls | Default datapath sweep | 4/4 controls passed; see SWEEP.md |
| Full true-clock-ratio leg | Default sweep, `obj_aclk/Vmilan_dp_aclk` | 188 checks, 0 failures |
| Full datapath sweep | `make -C tb/verilator/milan_dp` with recipe logging | rc 0; all 37 build/run chunks pass; see SWEEP.md |

The CSR reads compare against the independent taps at the live-mux capture
edge. They check successful AXI-Lite handshakes and response codes, stable
backpressure response, RO writes, selector direction/range and reset.
Observed words: filling `0x106`, converged `0x208`, rail `0x0001000e`,
reset after rail `0x100`.
The multi-stream check flushes listener 1 while listener 0 stays fed.
Its unequal states prevent a selector fixed at listener 0 from passing.

## Control evidence

| Control | Construction | Required result | Observed |
|---|---|---|---|
| Present-stage positive | Committed datapath, `--render-csr-only` | All CSR behavior checks pass | rc 0, 62/62 |
| Absent-stage negative | Remove the real stage instance in a temporary source; tie every output zero | `--render-csr-absent` reads structural zero at reset and during accepted ingress | rc 0, 31/31; more than three PDUs accepted |

The absent control is an explicit integration with no stage. Disabling TDM
output or I2S playback is not used as a false proxy for stage absence.
Temporary sources and builds are outside this output directory and removed
by the campaign. The tracked RTL is never mutated in place.

## Mutant evidence

| Mutation | Named check | Required exit | Observed |
|---|---|---:|---|
| Replace only the packed fill byte with zero | `RENDER-CSR: filling mirrors taps` | 1 | rc 1; got 256 (`0x100`), expected 262 (`0x106`) |

The same clean leg still passes. The complete campaign exits 0 and reports
3 checks, 0 failures. Build failures and failures without the named check
cannot count as caught mutations. Evidence: `render-csr-controls.log`.

## Cell counts

| Top | Base | Head | Delta |
|---|---:|---:|---:|
| `milan_csr` | 70,355 | 70,466 | +111 |
| `milan_datapath` | 1,633,435 | 1,631,783 | -1,652 |

Both measurements passed, rc 0. The base source was converted before any RTL
edit, as verified while its synthesis process consumed the converted input.
No other checkout or tree export was used.
Both recipes use `syn/yosys/run.sh --top milan_csr --top milan_datapath
--no-structural --results <result-directory>`.
The result directories are `yosys-base/` and `yosys-head/` beside this file.
Generic `synth`, default parameters, same installed binaries and allocator;
Yosys 0.66 (`86f2ddebc-dirty`), sv2v v0.0.13, jemalloc.
Simulation: Verilator 5.052, eight build jobs.
No device area or timing claim. The datapath reduction is the generic mapping
result, not a claimed physical saving.

## Gates

Commands run from the candidate worktree, unpiped and foreground.
`run_gate.py` captures each exit and log without masking it.
The default make uses `chunk_shell.py` to record build/run exits.
Both helpers and their JSON exit ledgers are beside this file.
`SWEEP.md` indexes the individual default-sweep chunks and their exits.
`PYDOC` below means `/tmp/443-a298-docs-env/bin/python3`.
`OUT` means this handoff's containing directory.

| Gate command | Exit | Evidence |
|---|---|---|
| `make -C tb/verilator/milan_dp VERILATOR_JOBS=8 SHELL=$OUT/chunk_shell.py` | 0 | `milan-dp-default.log` |
| `make -C tb/verilator/milan_dp_render VERILATOR_JOBS=8` | 0 | `milan-dp-render.log` |
| `make -C tb/verilator/milan_dp render-csr-controls VERILATOR_JOBS=8` | 0 | `render-csr-controls.log` |
| `syn/yosys/run.sh --top milan_csr --top milan_datapath --results $OUT/yosys-base --no-structural` | 0 | `yosys-base.log` |
| `syn/yosys/run.sh --top milan_csr --top milan_datapath --results $OUT/yosys-head --no-structural` | 0 | `yosys-head.log` |
| `python3 sw/builder/test_builder.py` | 0; gate 11 NOT RUN | `builder.log` |
| `python3 scripts/docs_check.py` | 0 | `docs-check.log` |
| `env GIT_DIR=/tmp/443-a298-no-git-metadata python3 scripts/docs_check.py` | 0 | `docs-check-no-git.log` |
| `PYDOC scripts/check_em_dash.py --base 0755923d983218ca6ca9db6891a558cbe6425b8d` | 0 | `em-dash.log` |
| `python3 scripts/check_doc_style.py` | 0 | `doc-style-final.log` |
| `PYDOC scripts/gen_toc.py --check` | 0 | `toc.log` |
| `python3 scripts/check_doc_paths.py` | 0 | `doc-paths.log` |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `module-matrix.log` |
| `python3 scripts/xvlog_gate.py --check` | 0 | `xvlog.log` |
| `python3 scripts/check_rtl_source_lists.py` | 0 | `rtl-source-lists.log` |
| `python3 scripts/check_sv_idiom.py` | 0 | `sv-idiom.log` |
| `python3 scripts/lint_rtl.py --check` | 0 | `lint-rtl.log` |
| `python3 scripts/check_cpp_idiom.py` | 0 | `cpp-idiom.log` |
| `python3 scripts/check_py_idiom.py` | 0 | `py-idiom.log` |
| `python3 scripts/check_port_contracts.py` | 0 | `port-contracts.log` |
| `python3 scripts/measure_naming.py --check` | 0 | `naming.log` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `test-evidence.log` |
| `git diff --check 0755923d983218ca6ca9db6891a558cbe6425b8d HEAD` | 0 | `diff-check.log` |
| `git diff --check` | 0 | `diff-check-final.log` |

Builder: rc 0; all gates pass except one NOT RUN arm.
Gate 11 requires the placement utilization report from the calibration build.
That report is absent; no calibration evidence is claimed.

The default sweep ran for 1487.75 seconds and returned zero.
Its 37 chunk exits are all zero; `SWEEP.md` lists each one.
The requested CSR control campaign separately returned zero in 96.09 seconds.

Initial documentation-style failure was fixed by paragraph breaks.
The final check passes; `doc-style.log` retains the initial result.
No-git mode points `GIT_DIR` at a nonexistent path.
The gate confirms filesystem-walk mode and skips only inventory parity.
The Markdown environment and its locked dependencies are outside this directory.
RTL lint: 90 existing findings, budget 90; no new finding.
The front-end analysis ran: zero own-tree findings, four pinned-processor
findings matching the recorded budget. It does not perform elaboration.

## Review handoff

Acceptance items 1, 2, 3 and 5 are implemented. The explicit controls and
cell measurements pass. The full default sweep also passes.
The worktree is clean at the recorded head.
Item 4 follows the public decision: no STREAM_INTERRUPTED connection.

The four original deferral sites now name the implemented #443 word:
`KL_render_setpoint.sv:193`, `milan_datapath.sv:6151`,
`TIME_SYNC.md:273` and `AAF_LATENCY_TAPS.md:96`.
References to #390 elsewhere still describe its junction counters.

The reviewers remain [R320] internal and [R321] external. These self-test
results are evidence, not a review verdict. Hosted PR gates, independent
reviews and merge validation are outside this local author assignment.

No push, PR creation/edit, merge, other checkout, sub-agent or hardware
operation was performed. `PR-BODY.md` is a local draft only.
The final authorized action is the review-ready comment on issue #443.
