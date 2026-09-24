[A290]

Closes #55
Closes #56
Closes #77
Relates to kebag-logic/milan-fpga#510

Status: REVIEW READY. Assignment items 1–4 are complete; all required gates returned 0.

Processor branch: `510-mvu-waiver`.
Base: `265d6762a58d9d9e545624d6d3f1a34e7006d171`.
Head: `05fd9e1b2390e7cb0c704c07cd3d9ec47ecd0a19`.
Subject: `Record October MVU waiver and pin unsupported command responses`.
The working tree is clean. Changes are six architecture/compliance pages and
`tb/pp_top/{sim_main.cpp,README.md}`. There are no RTL or microcode source changes.

Parent base: `35f0695815c202392b6b4806bb9f59dd110687ed`.
Local parent commit: `65bc81ed7cd1ffc9c24226a5d81850e10f5cc241`.
Subject: `Validate processor October MVU waiver pin`.
Only the `protocol-processor` gitlink changes, from
`a8f8ce810ddba1816cd129d0afcd71e6e02ade1b` to the processor head above.
The supplied consumer checkout was detached at the expected base; it remains
detached. No branch elsewhere was moved. No push, PR operation, merge or hardware
operation was performed.

Assignment: [processor #77](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/77#issuecomment-5823862684).
Authority: [owner decision of 2026-09-23](https://github.com/kebag-logic/milan-fpga/issues/510#issuecomment-5789766089).
Processor #55, #56 and #77 were read in full, together with all parent #510 comments.

| Assignment item | Result |
|---|---|
| 1. Record the waiver | Section 6.9, F06.14, REQ-MVU-003/004 and GAP-03 record that both pairs are recommended and deliberately unsupported for October. Related interface, hazard and storage descriptions say deferred. P4 revisit only if the conformance lab requires it |
| 2. Reconcile phantom parameters | F01.5 retains P-EN-MVU-SUID and P-EN-MVU-MCR as reserved names, with n/a defaults and no RTL consumer; the single-source table remains authoritative |
| 3. Pin the current responses | M4 checks all four complete command forms plus reserved type 0x0005: message type, status, cdl, frame length and every echoed byte. M1/M2 pin features_flags = 0. Both mutations described below are rejected |
| 4. No RTL change and gates | Processor and all ten parent checks pass at the recorded local commits |

Specification independently checked: Milan v1.2, consolidated final 2023-11-30,
sections 5.4.4.2–5.4.4.5 (printed pp. 58–61) and 7.6 (printed p. 115).
Each marks support as a recommendation. See [SPEC-CHECK.md](SPEC-CHECK.md)
for the source fingerprint and clause/page findings. Table 5.19 defines status
1 as NOT_IMPLEMENTED. Table 5.20 has no SUID/MCR capability bits; the zero
features_flags value is not a command-support bitmap.

| Command type | Response status | AECPDU bytes | cdl | Untagged Ethernet bytes, excluding FCS |
|---|---|---|---|---|
| 0x0001 SET_SYSTEM_UNIQUE_ID | NOT_IMPLEMENTED (1) | 40 | 28 | 60 |
| 0x0002 GET_SYSTEM_UNIQUE_ID | NOT_IMPLEMENTED (1) | 32 | 20 | 60 |
| 0x0003 SET_MEDIA_CLOCK_REFERENCE_INFO | NOT_IMPLEMENTED (1) | 104 | 92 | 118 |
| 0x0004 GET_MEDIA_CLOCK_REFERENCE_INFO | NOT_IMPLEMENTED (1) | 32 | 20 | 60 |

These are command-reflection responses. They preserve protocol ID, command type,
sequence and body; message_type is 7. GET_MILAN_INFO remains SUCCESS with
protocol_version 1, features_flags 0, certification_version 0 and cdl 32.

All processor gates below returned **0**, with commands run in the foreground
and verdicts taken directly, without piping. CI workflow inventory:
`.github/workflows/hdl.yml`. The CI-pinned v5.050 executable was used.

| Command | Result / evidence |
|---|---|
| `python3 scripts/check-links.py` | pass; final `make check` verifies 871 links |
| `python3 scripts/check-matrix.py` | 115 requirement rows, 17 findings, pass |
| `python3 scripts/render-wavedrom.py --check` | 18 blocks, pass |
| `make stale` | pass |
| `./scripts/lint_hdl.sh` | pass, zero-tolerance lint |
| `./scripts/run_suites.sh` | 33 suites, 1,008,937 checks, zero failing; exact processor head above |
| `python3 scripts/gen_matrix.py --check` | 92 rows, zero untested, pass |
| `make -C tb/nvm_port figures` | all measured figures agree, including historical forms; pull #13 head fetched as CI requires |
| `./syn/yosys/run.sh` | all tops elaborate; engine memory-mapping assertions pass |
| `make check` | pass on final content: 41 diagram blocks, 18 waveform blocks, 871 links and both matrices |
| `make -C tb/pp_top run` | 1,966 PASS, 0 FAIL (1,946 default + 20 fixture) |

Logs and return codes are in [gate-results.jsonl](gate-results.jsonl).
Pre-commit entries record the then-current base HEAD; final `make check`
validated the content subsequently committed without edits. The full bank
records the final processor head. RTL, gate scripts, CI definitions and NVM
figure sources are identical between the base and final processor head.

Mutation evidence is reproducible with [MVU-MUTANTS.py](MVU-MUTANTS.py), run
from the processor repository root after building `tb/pp_top`. Only generated
`tb/pp_top/ucode.hex` changes temporarily; tracked sources remain untouched.

| Mutation | Observed rejection |
|---|---|
| Word 560: `c00000000001` to `c00000000000`, changing generic NOT_IMPLEMENTED to SUCCESS while retaining the body and length | exit 1; 197 failures out of 1,946. M4 has 10 failures: status and byte-exact response for each 0x0001–0x0005. All five length/cdl checks still pass |
| Word 741: `230000000000` to `230000000003`, advertising both defined feature flags | exit 1; exactly M1, M2 features_flags and M5b fail, 3 out of 1,946 |

The original ROM was restored byte-for-byte before the full bank.
SHA-256: `23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144`.
See [mutation-results.json](mutation-results.json),
[success-mutant.log](success-mutant.log) and [features-mutant.log](features-mutant.log).

All parent commands at the local parent commit returned **0**:

```text
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/xvlog_gate.py --check
python3 scripts/check_rtl_source_lists.py
python3 scripts/pp_srcs.py --check --selftest
python3 scripts/check_port_contracts.py
python3 scripts/measure_naming.py --check
python3 scripts/measure_test_evidence.py --check
python3 scripts/docs_check.py
make -C tb/verilator/pp_shadow -j8
```

The parent integration suite reports **371 checks, 0 failures**. Documentation
reports 0 findings. The passing source-analysis ratchet retains four recorded
processor findings; the source-list gate retains six recorded omissions from
the native portability top list. Port, naming and test-evidence ratchets stay
within their existing budgets; no budget or waiver was changed by this lane.
Parent logs are the `parent-*.log` files, with exact commands and return codes
in [gate-results.jsonl](gate-results.jsonl).

Deliberate remaining scope: no implementation, state storage, persistence or
notifications for either waived pair. REQ-MVU-005 timing remains in processor
#57. The P4 revisit is conditional on the conformance lab requiring support.

[PR-BODY.md](PR-BODY.md) is complete. The final publication is the
[REVIEW-READY.md](REVIEW-READY.md) comment on
[processor issue #77](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/77).
