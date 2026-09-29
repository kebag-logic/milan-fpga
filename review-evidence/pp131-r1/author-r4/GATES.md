# Gate runs at `8457258`

Run by the scratch runner `gates.py` (this packet) with the pinned Verilator 5.050 wrapper
(sha256 `905795b99e0a8803…`, `Verilator 5.050 2026-07-01 rev v5.050`) and its VERILATOR_ROOT
first on PATH, as in the manager's bank. Each command ran to completion; log size and SHA-256
per row (logs kept in scratch). Machine load was high (several groups ran side by side), so
the seconds are not comparable with earlier rounds.

- **Processor**: a clean clone of the lane at `8457258`, with PR #13's head fetched read-only so
  `nvm_port figures` can reconstruct its matrix injection. Afterwards `git status --short` is
  empty (build products are ignored).
- **Parent, gitlink only**: a clone of the read-only checkout at dev `b5c0f69d`,
  `gptp-processor` and `third_party/verilog-axis` initialised from the pin lane (disposition
  5868716919), `protocol-processor` at `8457258` staged. No other edit.
- **Parent, declared edits**: a fresh clone set up the same way, then `parent_edits.py`
  (this packet; `receipts/parent-edits.diff`, 12 files) applied. Scratch only; nothing committed.

**Processor at `8457258`**

| Tree | Command | rc | Seconds | Log bytes | Log SHA-256 |
|---|---|---:|---:|---:|---|
| processor | `./scripts/run_suites.sh` | 0 | 580.9 | 1,647 | `6cb244e831849bf4…` |
| processor | `./scripts/lint_hdl.sh` | 0 | 11.7 | 1,056 | `9a3703ba1ec6767b…` |
| processor | `make check` | 0 | 33.3 | 225 | `655893ef4a8041ff…` |
| processor | `python3 scripts/gen_matrix.py --check` | 0 | 0.1 | 33 | `7a2c98136a0892f1…` |
| processor | `./syn/yosys/run.sh` | 0 | 86.7 | 25,840 | `08efc9bf248d7c0e…` |
| processor | `make -C tb/nvm_port figures` | 0 | 244.3 | 3,599 | `49355f200d26d92a…` |
| processor | `python3 tb/pp_top/d3_mutants.py --output <scratch> --jobs 6 --verilator <scratch>` | 0 | 980.7 | 5,543 | `c1c375b58e20e4e2…` |
| processor | `make -C tb/srp_top mutants` | 0 | 1286.8 | 4,072 | `6079a105e0f1b07e…` |

**Parent consumer set, gitlink only**

| Tree | Command | rc | Seconds | Log bytes | Log SHA-256 |
|---|---|---:|---:|---:|---|
| parent | `python3 scripts/check_cpp_idiom.py` | 0 | 1.2 | 315 | `1dc9c5c9796ba9bc…` |
| parent | `python3 scripts/check_py_idiom.py` | 0 | 3.4 | 461 | `01ebfc4c1e132626…` |
| parent | `python3 scripts/xvlog_gate.py --check` | 0 | 140.2 | 1,320 | `6b296dbcda6c9be3…` |
| parent | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.4 | 390 | `b8372555c3e35c33…` |
| parent | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.2 | 955 | `fad5e1b9dd5f465b…` |
| parent | `python3 sw/builder/test_builder.py` | 0 | 769.1 | 89,748 | `2fd49f34f32d4627…` |
| parent | `make -C tb/verilator/pp_shadow -j8` | 2 | 4.5 | 36,748 | `4a940dfabb53c808…` |
| parent | `python3 scripts/check_port_contracts.py` | 0 | 2.4 | 421 | `661be002a5a679e0…` |
| parent | `python3 scripts/measure_naming.py --check` | 0 | 0.5 | 36,618 | `d633d2a58ff2834e…` |
| parent | `python3 scripts/measure_test_evidence.py --check` | 1 | 5.6 | 11,158 | `e1bcef3caad0b374…` |
| parent | `python3 scripts/docs_check.py` | 0 | 4.6 | 127 | `2fadcbb728aedaa9…` |
| parent | `make -C tb/verilator/nvm_cosim lint` | 0 | 0.3 | 30,525 | `d4e33aae55884292…` |
| parent | `make -C tb/verilator/nvm_cosim quick` | 2 | 31.0 | 1,796 | `04b981185839edc2…` |
| parent | `make -C tb/verilator/milan_dp -j8` | 2 | 153.9 | 280,121 | `8cb292603581f9b6…` |
| parent | `make -C tb/verilator/milan_dp_render -j8` | 2 | 145.9 | 168,449 | `a3a717057d094161…` |

**Parent consumer set, declared edits applied**

| Tree | Command | rc | Seconds | Log bytes | Log SHA-256 |
|---|---|---:|---:|---:|---|
| parent | `python3 scripts/check_cpp_idiom.py` | 0 | 1.2 | 315 | `1dc9c5c9796ba9bc…` |
| parent | `python3 scripts/check_py_idiom.py` | 0 | 3.5 | 461 | `3574d9d38f79ef8f…` |
| parent | `python3 scripts/xvlog_gate.py --check` | 0 | 139.7 | 1,320 | `6b296dbcda6c9be3…` |
| parent | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.4 | 390 | `b8372555c3e35c33…` |
| parent | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.2 | 955 | `fad5e1b9dd5f465b…` |
| parent | `python3 sw/builder/test_builder.py` | 0 | 740.8 | 89,747 | `925ffeafe1892608…` |
| parent | `make -C tb/verilator/pp_shadow -j8` | 0 | 199.5 | 322,973 | `c4b344fd4113cfea…` |
| parent | `python3 scripts/check_port_contracts.py` | 0 | 2.4 | 421 | `661be002a5a679e0…` |
| parent | `python3 scripts/measure_naming.py --check` | 0 | 0.5 | 36,618 | `d633d2a58ff2834e…` |
| parent | `python3 scripts/measure_test_evidence.py --check` | 0 | 5.5 | 11,495 | `fad6d4b4a38b7229…` |
| parent | `python3 scripts/docs_check.py` | 0 | 4.4 | 127 | `2fadcbb728aedaa9…` |
| parent | `make -C tb/verilator/nvm_cosim lint` | 0 | 0.4 | 30,043 | `b82b1f9226ca8e97…` |
| parent | `make -C tb/verilator/nvm_cosim quick` | 0 | 27.8 | 394 | `9bd7ec6709ee4dfe…` |
| parent | `make -C tb/verilator/milan_dp -j8` | 0 | 1474.1 | 2,082,131 | `6e3f01661f4fb6b9…` |
| parent | `make -C tb/verilator/milan_dp_render -j8` | 0 | 314.4 | 169,226 | `20139c0f8af4f879…` |

Processor readings: `run_suites.sh` 33 suites, 1,016,031 checks, 0 failing (`tb/pp_top` 7,888,
`tb/acmp_nvm` 355); `make check` (lint, WaveDrom, links 968, both matrices, params 26/26/26,
stale); `d3_mutants.py` 76 of 76 KILLED, goldens PASS; `srp_top` mutants 64 checks, coverage
49/49; `nvm_port figures` rc 0.

Parent, gitlink only (the pin-adoption lane's starting point): 10 of 15 rc 0.
- `pp_shadow` rc 2: 20 PINMISSING, four each for the five round-1 ports; its sim never runs.
- `measure_test_evidence.py` rc 1: `protocol-processor/tb/pp_top/d3_mutants.py` unexplained.
- `nvm_cosim lint` rc 0 with 86 warnings, two PINMISSING (`wr_chg_o`, `rs_agg_i`).
- `nvm_cosim quick` rc 2: 308 of 315 (B1-B4 `later_record_persists@end:0x21`, and the power
  cycles after B1, B2 and B4 `restores_last_verified`).
- `milan_dp` rc 2: `gmstep` 11 of 103, `gptp` and `gptp-lat` fail; `make` stops there, so the pool legs never run.
- `milan_dp_render` rc 2: `tdm8_render` 2 of 151 (T8 REMOVE).

Parent, declared edits applied: **15 of 15 rc 0**.
- `nvm_cosim quick` 315 of 315; `nvm_cosim lint` 85 warnings, 0 PINMISSING.
- `pp_shadow` four builds, 0 failures (595, 595, 635, 295 checks).
- `measure_test_evidence.py`: PASS (0 <= 0 unexplained DUT-source readers).
- `milan_dp`: `gmstep` 103/103, `gptp` 181/181, `gptp-lat` 181/181; pool legs notify 372,
  crflic 415, nxn 1,841, nxndv 1,843, nxn8 3,521, nxn4c 1,841, prune 33, and the main, nolpf,
  ax1x1 and aclk legs, all 0 failures; `render_mutants.py` 6/6 and `gmstep_mutants.py` 6/6.
- `milan_dp_render`: `tdm8_render` 65/65 and 152/152; its mutants 5/5.
- `xvlog_gate.py`: 4 findings == ratchet; `check_port_contracts.py`: processor 111 <= 111.

The `nvm_cosim` attribution variants (same scratch setup, `make quick`):
pins only 308/315 (`receipts/nvm_cosim-quick-pins-only.log`); pins plus the derived
backoff, window 1,500 ms, 311/315 (`receipts/nvm_cosim-quick-pins-backoff-1500ms.log`);
all declared edits, window 2,000 ms, 315/315 (above).
