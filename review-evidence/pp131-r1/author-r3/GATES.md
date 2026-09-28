# Gate runs at `cbbb5ac`

Run by the scratch runner `gates.py` (this packet) in a clean processor clone at the head (with the processor's pull-request heads fetched read-only, so `nvm_port figures` can reconstruct its matrix injection from `dc354be~1` and `62d96d6~1`) and in a scratch parent (a clone of the read-only checkout at `7a7582f0`, `gptp-processor` and `third_party/verilog-axis` initialised from the pin lane as disposition 5868716919 shows, `protocol-processor` initialised from this lane with its gitlink staged at the head). PATH carries the pinned Verilator 5.050 wrapper and its VERILATOR_ROOT, as in the manager's bank. The two groups ran side by side, each command to completion; log size and SHA-256 per row (logs kept in scratch). The processor clone was clean afterwards (`git status` empty).

| Tree | Command | rc | Seconds | Log bytes | Log SHA-256 |
|---|---|---:|---:|---:|---|
| processor | `./scripts/run_suites.sh` | 0 | 563.0 | 1,647 | `840948f142699cfe…` |
| processor | `./scripts/lint_hdl.sh` | 0 | 11.5 | 1,056 | `9a3703ba1ec6767b…` |
| processor | `make check` | 0 | 34.7 | 225 | `a83ad716a3388f2b…` |
| processor | `python3 scripts/gen_matrix.py --check` | 0 | 0.0 | 33 | `7a2c98136a0892f1…` |
| processor | `./syn/yosys/run.sh` | 0 | 80.2 | 25,840 | `474219a64201b0cf…` |
| processor | `make -C tb/nvm_port figures` | 0 | 240.5 | 3,609 | `464afd258ae8af76…` |
| processor | `python3 tb/pp_top/d3_mutants.py --output <out>/d3-mutants --jobs 6 --verilator <pinned>/verilator` | 0 | 869.6 | 5,025 | `d073b8a0d94f39c2…` |
| processor | `make -C tb/srp_top mutants` | 0 | 1271.8 | 4,082 | `e739a3368c38502b…` |
| parent | `python3 scripts/check_cpp_idiom.py` | 0 | 1.2 | 315 | `1dc9c5c9796ba9bc…` |
| parent | `python3 scripts/check_py_idiom.py` | 0 | 3.4 | 461 | `2e384ade4c2ecd8c…` |
| parent | `python3 scripts/xvlog_gate.py --check` | 0 | 140.4 | 1,320 | `84cbfb8c5211a07a…` |
| parent | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.4 | 390 | `b8372555c3e35c33…` |
| parent | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.2 | 955 | `fad5e1b9dd5f465b…` |
| parent | `python3 sw/builder/test_builder.py` | 0 | 745.2 | 85,769 | `bc3d0bfbcdfb92a9…` |
| parent | `make -C tb/verilator/pp_shadow -j8` | 2 | 4.3 | 36,668 | `e23087c9206660fd…` |
| parent | `python3 scripts/check_port_contracts.py` | 0 | 2.4 | 421 | `c667fd3b6adc1bb1…` |
| parent | `python3 scripts/measure_naming.py --check` | 0 | 0.4 | 36,618 | `d633d2a58ff2834e…` |
| parent | `python3 scripts/measure_test_evidence.py --check` | 1 | 5.6 | 10,996 | `4d85b57aa3196f90…` |
| parent | `python3 scripts/docs_check.py` | 0 | 4.5 | 127 | `e7cc143cb86bb35a…` |

The two parent rows that are not rc 0 are the declared pin-adoption items, and nothing else:

- `make -C tb/verilator/pp_shadow -j8`, rc 2: exactly the 20 `PINMISSING` warnings of the manager's receipt at `2b38d68` (`parent-consumer/07.log`), four each for `d3_unflushed_o`, `restore_cause_o`, `restore_closed_o`, `restore_rb_o` and `rs_cause_o`, the five round-1 ports the pin-adoption lane connects. Round 3 adds no top port.
- `measure_test_evidence.py --check`, rc 1: two unexplained DUT-source readers, `protocol-processor/tb/acmp_talker/retry_mutants.py` (unexplained at this parent pin since before this lane; the parent's dev pin explains it) and `protocol-processor/tb/pp_top/d3_mutants.py`. With both disposition lines added to a scratch copy of the classifier (restored afterwards) it returns rc 0 and reports nothing else: `TEST-EVIDENCE RATCHET: PASS (75 <= 77 suite(s) without a mutation arm, 10 <= 10 unseeded draw site(s), 0 <= 0 unexplained DUT-source reader(s), 3 <= 3 wall-clock-dependent suite file(s))`.

Other parent observations (outside the consumer set):

- `make -C tb/verilator/nvm_cosim lint`: rc 0 at the head; 86 warnings against 85 with the processor at `2b38d68`, the one new being `PINMISSING` for `rs_agg_i` on `cosim_top.sv:257` (the parent's direct instance of `KL_acmp_nvm_shadow`).
- `make -C tb/verilator/nvm_cosim quick`: 308 of 315 at the head, the same 7 failures (B1 to B4 `later_record_persists@end:0x21`, and the power cycles after B1, B2 and B4) as with the processor at `2b38d68` and at `f72a2d2`; 315 of 315 at `c951a9ff` and at `505524e`. Introduced by round 1's DR2c backoff in the binding manager, not by round 3.
