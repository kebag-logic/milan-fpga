# Gate runs at `2b38d68`

Run by the scratch runner `gates.py` (this packet) in a clean processor clone at the head and in a scratch parent (a clone of the read-only parent checkout at `7a7582f0`, `gptp-processor` and `third_party/verilog-axis` initialised from the pin lane as disposition 5868716919 shows, `protocol-processor` initialised from this lane with its gitlink staged at the head). PATH carries the pinned Verilator 5.050 wrapper and its VERILATOR_ROOT, as in the manager's bank. Each command ran to completion; log size and SHA-256 per row (logs kept in scratch).

| Tree | Command | rc | Seconds | Log bytes | Log SHA-256 |
|---|---|---:|---:|---:|---|
| processor | `./scripts/run_suites.sh` | 0 | 534.2 | 1,647 | `cb03d928a0763e16…` |
| processor | `./scripts/lint_hdl.sh` | 0 | 11.6 | 1,056 | `9a3703ba1ec6767b…` |
| processor | `make check` | 0 | 29.1 | 225 | `86dd0837a7576361…` |
| processor | `python3 scripts/gen_matrix.py --check` | 0 | 0.0 | 33 | `7a2c98136a0892f1…` |
| processor | `./syn/yosys/run.sh` | 0 | 80.5 | 25,840 | `2dd156fb83778109…` |
| processor | `make -C tb/nvm_port figures` | 2 | 236.2 | 6,836 | `af019c655bf9d1b3…` |
| processor | `python3 tb/pp_top/d3_mutants.py --output <out>/d3-mutants --jobs 6` | 0 | 451.6 | 4,488 | `a31209970f4b6970…` |
| processor | `make -C tb/srp_top mutants` | 0 | 1272.0 | 4,082 | `fb5e652956960e19…` |
| parent | `python3 scripts/check_cpp_idiom.py` | 0 | 1.2 | 315 | `1dc9c5c9796ba9bc…` |
| parent | `python3 scripts/check_py_idiom.py` | 0 | 3.4 | 461 | `992105aee1794ae6…` |
| parent | `python3 scripts/xvlog_gate.py --check` | 0 | 138.9 | 1,320 | `0730c17773bc62b0…` |
| parent | `python3 scripts/check_rtl_source_lists.py` | 0 | 1.4 | 390 | `b8372555c3e35c33…` |
| parent | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.2 | 955 | `fad5e1b9dd5f465b…` |
| parent | `python3 sw/builder/test_builder.py` | 0 | 757.3 | 85,768 | `6f67ea24823c41a6…` |
| parent | `make -C tb/verilator/pp_shadow -j8` | 2 | 4.2 | 36,668 | `5a78891c3a795c86…` |
| parent | `python3 scripts/check_port_contracts.py` | 0 | 2.3 | 421 | `76a9b78bb8836e97…` |
| parent | `python3 scripts/measure_naming.py --check` | 0 | 0.4 | 36,618 | `f5edd7bbf9d00bbb…` |
| parent | `python3 scripts/measure_test_evidence.py --check` | 1 | 5.5 | 10,996 | `4d85b57aa3196f90…` |
| parent | `python3 scripts/docs_check.py` | 0 | 4.4 | 127 | `e7cc143cb86bb35a…` |

Rerun of `make -C tb/nvm_port figures` in the same clone after fetching the processor's pull-request heads (read-only) so the revisions its matrix injection is reconstructed from (`dc354be~1`, `62d96d6~1`, on PR #13's head) exist: rc 0, 235 s, log 3,609 bytes, SHA-256 `0cdc5db5ba11e61f…`. The first run's rc 2 was that missing history ("cannot read dc354be~1"), not a figure.

The two parent rows that are not rc 0, and why neither is a regression this round adds:

- `make -C tb/verilator/pp_shadow -j8`, rc 2: exactly the 20 `PINMISSING` warnings of the
  manager's round-1 receipt (`parent-consumer/07.log`), for the five round-1 ports
  (`restore_closed_o`, `restore_rb_o`, `rs_cause_o`, `restore_cause_o`, `d3_unflushed_o`) that
  the parent pin-adoption lane connects. Round 2 adds no top port.
- `measure_test_evidence.py --check`, rc 1: two unexplained DUT-source readers.
  `protocol-processor/tb/acmp_talker/retry_mutants.py` is unexplained at this parent pin
  (`7a7582f0`) already, as in round 1; the manager's dev pin explains it.
  `protocol-processor/tb/pp_top/d3_mutants.py` is the in-tree driver item 5 requires; like
  `retry_mutants.py` after #129, it needs its disposition line in the parent's
  `DUT_READER_DISPOSITIONS` in the pin-adoption lane. With both lines added to a scratch copy
  of the classifier (restored afterwards) it returns rc 0 and reports nothing else:
  `TEST-EVIDENCE RATCHET: PASS (75 <= 77 suite(s) without a mutation arm, 10 <= 10 unseeded
  draw site(s), 0 <= 0 unexplained DUT-source reader(s), 3 <= 3 wall-clock-dependent suite
  file(s))`. The proposed text: "mutation campaign; it plants one D3 saved-state defect from
  its own table into an isolated copy and requires every named check to fail in a completed
  run; no expected value is read from the text".
