# Gate runs at `9b4da6b`

Run by the scratch runner `gates.py` (round 5's, unchanged) with the pinned Verilator 5.050
wrapper (`Verilator 5.050 2026-07-01 rev v5.050`, the manager's bank wrapper) and its
VERILATOR_ROOT first on PATH. Each command ran to completion; log size and SHA-256 per row (logs
kept in scratch). The two groups ran at the same time on a shared host (load average 14 to 29),
so the seconds are not comparable with earlier rounds.

- **Processor**: a clean clone of the lane at `9b4da6b`, with PR #13's head fetched read-only so
  `nvm_port figures` can reconstruct its matrix injection. Afterwards `git status --short` is
  empty (build products are ignored).
- **Parent**: `mk_parent.sh` (a clone of the read-only checkout at dev `eaa88a32`,
  `gptp-processor` and `third_party/verilog-axis` from the pin lane, `protocol-processor` at
  `9b4da6b` staged), then `parent_edits.py` (byte-identical to round 5's; its diff equals round
  5's `parent-edits.diff` apart from index lines). Scratch only; nothing committed. The manager's
  sixteen commands. `ax1x1gptp` was not rerun: no processor file it builds changed since
  `9dce84e` (round 5: 139 of 139).

`gates-processor`

| Tree | Command | rc | Seconds | Log bytes | Log SHA-256 |
|---|---|---:|---:|---:|---|
| processor | `verilator --version` | 0 | 0.1 | 38 | `46aedd5b30efdd94…` |
| processor | `./scripts/lint_hdl.sh` | 0 | 11.5 | 1,056 | `9a3703ba1ec6767b…` |
| processor | `./scripts/run_suites.sh` | 0 | 580.6 | 1,647 | `b27bb8d8d8b4baff…` |
| processor | `make -j1 check` | 0 | 32.3 | 225 | `655893ef4a8041ff…` |
| processor | `python3 scripts/gen_matrix.py --check` | 0 | 0.0 | 33 | `7a2c98136a0892f1…` |
| processor | `./syn/yosys/run.sh` | 0 | 84.6 | 25,840 | `08efc9bf248d7c0e…` |
| processor | `make -C tb/nvm_port figures` | 0 | 245.5 | 3,621 | `6c8109757a4374c0…` |
| processor | `git diff --check c951a9ff0cb5851fb159d33e966e5a2a9a188fe3 HEAD` | 0 | 0.0 | 0 | `e3b0c44298fc1c14…` |
| processor | `python3 tb/pp_top/d3_mutants.py --output <scratch> --jobs 6 --verilator <scratch>` | 0 | 1009.5 | 6,042 | `e0c5606eec279bcd…` |
| processor | `make -C tb/srp_top mutants` | 0 | 1273.2 | 4,094 | `ee32bc692a3cb815…` |

`gates-parent`

| Tree | Command | rc | Seconds | Log bytes | Log SHA-256 |
|---|---|---:|---:|---:|---|
| parent | `python3 scripts/check_cpp_idiom.py` | 0 | 1.2 | 315 | `1dc9c5c9796ba9bc…` |
| parent | `python3 scripts/check_py_idiom.py` | 0 | 3.4 | 461 | `3f9092b5b5dd82e8…` |
| parent | `python3 scripts/xvlog_gate.py --check` | 0 | 141.2 | 1,320 | `6253dc3e3c4c7b26…` |
| parent | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.4 | 390 | `b8372555c3e35c33…` |
| parent | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.2 | 955 | `fad5e1b9dd5f465b…` |
| parent | `python3 sw/builder/test_builder.py` | 0 | 758.2 | 95,936 | `2e84b01d1a5b7fde…` |
| parent | `make -C tb/verilator/pp_shadow -j8` | 0 | 232.3 | 323,023 | `eb5d506ac42aba22…` |
| parent | `python3 scripts/check_port_contracts.py` | 0 | 2.4 | 421 | `661be002a5a679e0…` |
| parent | `python3 scripts/measure_naming.py --check` | 0 | 0.5 | 36,618 | `d633d2a58ff2834e…` |
| parent | `python3 scripts/measure_test_evidence.py --check` | 0 | 5.7 | 11,495 | `fad6d4b4a38b7229…` |
| parent | `python3 scripts/docs_check.py` | 0 | 4.5 | 127 | `fcade68199603ee7…` |
| parent | `python3 scripts/lint_rtl.py --check` | 0 | 6.2 | 14,186 | `100ecae619de3a93…` |
| parent | `make -C tb/verilator/nvm_cosim lint` | 0 | 0.3 | 29,874 | `581782788e230e51…` |
| parent | `make -C tb/verilator/nvm_cosim quick` | 0 | 27.8 | 404 | `579dcaa9155a45ff…` |
| parent | `make -C tb/verilator/milan_dp -j8` | 0 | 1564.0 | 2,083,031 | `1435c5444312ec4a…` |
| parent | `make -C tb/verilator/milan_dp_render -j8` | 0 | 315.5 | 169,256 | `2c576a6af7c6d6fa…` |

Readings:
- `run_suites.sh`: 33 suites, 1,016,036 checks, 0 failing (`tb/pp_top` 7,888, `tb/acmp_nvm`
  360; round 5 1,016,035). `make check`: lint, WaveDrom, links 968, both matrices, params
  26/26/26, stale. `d3_mutants.py`: 83 of 83 KILLED, goldens PASS (acmp_nvm, pp_top,
  rx_validator); every README count equals the run (MUTANTS.md; R391-5's
  `check_readme_counts.py` 86 entries, 0 problems). `srp_top` mutants: 64 checks, coverage 49/49.
  `nvm_port figures` rc 0.
- Parent: 16 of 16 rc 0. C++ idiom (long function 0 <= 0) and Python idiom rc 0; xvlog 4 ==
  ratchet; `nvm_cosim` quick 315/315, lint 85 warnings, 0 PINMISSING; `pp_shadow` four builds
  595, 595, 635, 295 checks, 0 failures; `milan_dp`: gmstep 103, gptp 181, gptp-lat 181, main
  234, notify 378, crflic 415, nxn 1,841, nxndv 1,843, nxn8 3,521, nxn4c 1,841, nolpf 234,
  prune 33, ax1x1 231, aclk 190, all 0 failures, 30 `[AECP-WTMO]` passes (five legs x six), the
  four image-less legs naming CLOSED; `render_mutants.py` 6/6 and `gmstep_mutants.py` 6/6.
  `milan_dp_render` 65/65, 152/152, 5/5. Evidence classifier 0 unexplained DUT readers (with the
  declared `d3_mutants.py` disposition). Every reading equals round 5's.
- Before the commit, the working diff was also run through the parent's C++ and Python idiom
  gates in a scratch parent; the first attempt found one function over the 100-line ratchet
  (`sample_producers()`, 109 lines), fixed by moving the owned-cycle monitor into
  `sample_m0_owned_read()` before committing.
