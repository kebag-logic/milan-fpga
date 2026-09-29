# Gate runs at `9dce84e`

Run by the scratch runner `gates.py` (this packet) with the pinned Verilator 5.050 wrapper
(`Verilator 5.050 2026-07-01 rev v5.050`, the manager's bank wrapper) and its VERILATOR_ROOT
first on PATH. Each command ran to completion; log size and SHA-256 per row (logs kept in
scratch). The host was shared with other runs (load average 20 to 50), so the seconds are not
comparable with earlier rounds.

- **Processor**: a clean clone of the lane at `9dce84e`, with PR #13's head fetched read-only
  so `nvm_port figures` can reconstruct its matrix injection. Afterwards `git status --short`
  is empty (build products are ignored).
- **Parent**: a clone of the read-only checkout at dev `eaa88a32`, `gptp-processor` and
  `third_party/verilog-axis` initialised from the pin lane (disposition 5868716919),
  `protocol-processor` at `9dce84e` staged, then this packet's `parent_edits.py` (12 files,
  `receipts/parent-edits.diff`). Scratch only; nothing committed. The manager's sixteen
  commands.
- **gptp**: a second scratch parent set up the same way, for the nightly physical harness
  outside the consumer set.

`processor`

| Tree | Command | rc | Seconds | Log bytes | Log SHA-256 |
|---|---|---:|---:|---:|---|
| processor | `verilator --version` | 0 | 0.1 | 38 | `46aedd5b30efdd94…` |
| processor | `./scripts/lint_hdl.sh` | 0 | 14.6 | 1,056 | `9a3703ba1ec6767b…` |
| processor | `./scripts/run_suites.sh` | 0 | 677.6 | 1,647 | `83cf499833738bde…` |
| processor | `make -j1 check` | 0 | 36.7 | 225 | `655893ef4a8041ff…` |
| processor | `python3 scripts/gen_matrix.py --check` | 0 | 0.1 | 33 | `7a2c98136a0892f1…` |
| processor | `./syn/yosys/run.sh` | 0 | 85.6 | 25,840 | `08efc9bf248d7c0e…` |
| processor | `make -C tb/nvm_port figures` | 0 | 255.2 | 3,611 | `d980f608333106e3…` |
| processor | `git diff --check c951a9ff0cb5851fb159d33e966e5a2a9a188fe3 HEAD` | 0 | 0.1 | 0 | `e3b0c44298fc1c14…` |
| processor | `python3 tb/pp_top/d3_mutants.py --output <scratch> --jobs 6 --verilator <scratch>` | 0 | 1099.1 | 5,896 | `ba571e44ff2b7bb1…` |
| processor | `make -C tb/srp_top mutants` | 0 | 1288.6 | 4,084 | `058c78d08cc5f336…` |

`parent`

| Tree | Command | rc | Seconds | Log bytes | Log SHA-256 |
|---|---|---:|---:|---:|---|
| parent | `python3 scripts/check_cpp_idiom.py` | 0 | 1.2 | 315 | `1dc9c5c9796ba9bc…` |
| parent | `python3 scripts/check_py_idiom.py` | 0 | 3.6 | 461 | `0ccdbd0ec7bedb7d…` |
| parent | `python3 scripts/xvlog_gate.py --check` | 0 | 207.7 | 1,320 | `7d79dcfa1dc4fd60…` |
| parent | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.5 | 390 | `b8372555c3e35c33…` |
| parent | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.3 | 955 | `fad5e1b9dd5f465b…` |
| parent | `python3 sw/builder/test_builder.py` | 0 | 800.7 | 95,684 | `ed125de0d8716097…` |
| parent | `make -C tb/verilator/pp_shadow -j8` | 0 | 253.8 | 322,972 | `46cf5a966a1aca02…` |
| parent | `python3 scripts/check_port_contracts.py` | 0 | 3.1 | 421 | `661be002a5a679e0…` |
| parent | `python3 scripts/measure_naming.py --check` | 0 | 0.5 | 36,618 | `d633d2a58ff2834e…` |
| parent | `python3 scripts/measure_test_evidence.py --check` | 0 | 5.7 | 11,495 | `fad6d4b4a38b7229…` |
| parent | `python3 scripts/docs_check.py` | 0 | 4.6 | 127 | `fcade68199603ee7…` |
| parent | `python3 scripts/lint_rtl.py --check` | 0 | 7.0 | 14,186 | `100ecae619de3a93…` |
| parent | `make -C tb/verilator/nvm_cosim lint` | 0 | 0.4 | 29,864 | `7d23d42100dfe8ff…` |
| parent | `make -C tb/verilator/nvm_cosim quick` | 0 | 33.4 | 394 | `9f175ab07059e9ca…` |
| parent | `make -C tb/verilator/milan_dp -j8` | 0 | 1627.0 | 2,082,739 | `28bad66d24883fa8…` |
| parent | `make -C tb/verilator/milan_dp_render -j8` | 0 | 319.0 | 169,226 | `3ad109161603d83c…` |

`gptp`

| Tree | Command | rc | Seconds | Log bytes | Log SHA-256 |
|---|---|---:|---:|---:|---|
| gptp | `make -C tb/verilator/milan_dp ax1x1gptp` | 0 | 3277.1 | 102,799 | `745fd27d71b2f3eb…` |

`runs` (focused scratch runs, `run_logged.py`)

| Tree | Command | rc | Seconds | Log bytes | Log SHA-256 |
|---|---|---:|---:|---:|---|
| parent (edits, gitlink `84572585`) | `make -C tb/verilator/milan_dp notify` | 0 | 28.0 | 111,401 | `2629b5ace7b86752…` |
| parent (edits, gitlink `84572585`) | `make -C tb/verilator/milan_dp ax1x1` | 0 | 17.1 | 101,994 | `a66b921cc26007a5…` |
| parent (edits, gitlink `84572585`) | `make -C tb/verilator/milan_dp aclk` | 0 | 485.0 | 97,864 | `1b4c1a50def956ad…` |
| parent (no edits, gitlink `c951a9ff`) | `make -C tb/verilator/nvm_cosim lint` | 0 | 0.4 | 29,633 | `b9e85920611ba39c…` |
| parent (edits, gitlink `84572585`) | `make -C tb/verilator/nvm_cosim lint` | 0 | 0.5 | 29,864 | `ee010db08ee95586…` |
| parent (edits, gitlink `84572585`) | `make -C tb/verilator/milan_dp ax1x1gptp` | 0 | 3246.9 | 102,775 | `5151767ec3b2f3f7…` |
| parent (edits except `sim_ax1x1gptp.cpp`, gitlink `84572585`) | `make -C tb/verilator/milan_dp ax1x1gptp` | 2 | 3253.6 | 102,823 | `c44f82471fe775e7…` |
| parent (edits, gitlink `9dce84e`), `tb/verilator/milan_dp_gptp` | `python3 verify_abort.py` | 0 | 556.4 | 3,538 | `482db6fd93bc4344…` |

Readings:
- `run_suites.sh`: 33 suites, 1,016,035 checks, 0 failing (`tb/pp_top` 7,888, `tb/acmp_nvm`
  359). `make check`: lint, WaveDrom, links 968, both matrices, params 26/26/26, stale.
  `d3_mutants.py`: 81 of 81 KILLED, goldens PASS (acmp_nvm, pp_top, rx_validator); every
  README count equals the run (MUTANTS.md). `srp_top` mutants: 64 checks, coverage 49/49.
- Parent: 16 of 16 rc 0. `nvm_cosim` quick 315/315; lint 85 warnings, 0 PINMISSING, 0
  PINCONNECTEMPTY. `pp_shadow` four builds 595, 595, 635, 295 checks, 0 failures. `milan_dp`:
  gmstep 103, gptp 181, gptp-lat 181, main 234, notify 378 (six `[AECP-WTMO]`), crflic 415,
  nxn 1,841, nxndv 1,843, nxn8 3,521, nxn4c 1,841, nolpf 234, prune 33, ax1x1 231, aclk 190,
  all 0 failures; `render_mutants.py` 6/6 and `gmstep_mutants.py` 6/6. `milan_dp_render`
  65/65, 152/152, 5/5. Evidence classifier 0 unexplained DUT readers.
- `ax1x1gptp` at `9dce84e`: rc 0, 139 checks, 0 failures, 16.992510280 s simulated
  (849,625,514 cycles), 3,251.88 s run wall (3,277.1 s with the build); both boots'
  `[BOOT] PP_STAT[2] the restore walk sequenced` pass. At `84572585` the same (139/0,
  3,246.9 s); without its edit 15 of 137 fail (every GET_AVB_INFO and GET_AS_PATH check),
  `make` rc 2 (`receipts/ax1x1gptp-84572585.txt`). `milan_dp_gptp`'s `verify_abort.py` on the
  `9dce84e` binary: rc 0, setup abort 6/6, no-TX 20/20, no-Pdelay 14/14.
