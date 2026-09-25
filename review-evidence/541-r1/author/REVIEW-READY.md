[A304] REVIEW READY

Commit: `2734b771bcf0b383ea62ef05744452827bafe9e4`
Branch: `541-crf-unlock`
Base: `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`

Changed: receiver header, CRF_CTRL register row, directed receiver test,
and receiver mutation campaign. No functional RTL change: comment-stripped
`KL_crf_rx.sv` matches the base exactly.

Acceptance criteria:

- Clause confirmation and excerpts are in the [takeover comment](https://github.com/kebag-logic/milan-fpga/issues/541#issuecomment-5827406716). Milan Table 5.6 leaves lock criteria to the manufacturer; the cited CRF rules impose no immediate unlock on a format error. The stop condition does not apply. The 100 ms duration remains an implementation policy.
- Header and CRF_CTRL now describe timeout-based unlock. A validation error breaks settling, retains established lock, and does not refresh the timeout. UNSUPPORTED_FORMAT increments once per affected observation interval through `fmt_err_o`; the documentation identifies the full-width GET_COUNTERS and low-eight-bit CRF_STATUS views.
- The new test starts LOCKED, injects a matching wrong-type PDU, checks lock on the rejection edge and through the counter commit, checks exactly one format count and no accepted-frame or lock/unlock event, resumes valid traffic, and grades silence before and after 100 ms. Existing #546 discontinuity and connected servo cases remain enabled.
- `validation_error_unlocks` compiles, exits 1, and produces the required `validation error preserves established lock` assertion failure. Both clean controls exit 0; all seven mutants are detected. The containing campaign exits 0 with nine controls and zero failures.

Validation: every command below returned 0, run in the foreground without pipelines:

```sh
make -C tb/verilator/crf_rx
make -C tb/verilator/mmcm_servo
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base 5b73d3f47dfed519eb988c13d6beb1db664ef1e0
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_doc_paths.py
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/xvlog_gate.py --check
python3 scripts/check_sv_idiom.py
python3 scripts/check_cpp_idiom.py
python3 scripts/check_py_idiom.py
python3 scripts/measure_test_evidence.py --check
git diff --check
```

The sixteenth invocation was `python3 scripts/docs_check.py` on an archive
of this exact head without Git metadata. Both documentation modes report
zero findings across 165 Markdown and 865 text files. The no-Git mode skips
only its Git-dependent inventory-parity self-test. Live HDL analysis passed
at the existing four pinned-processor findings, with zero parent-HDL findings.

Receiver results: 13,836 unit checks, 1,932 directed discontinuity checks,
69 connected talker-step checks, nine mutation controls; zero failures.
Servo results: 85 unit checks, eight playback checks, 113 PHC-step checks;
zero failures.

HANDOFF.md, PR-BODY.md and validation logs are complete in the assigned
output directory. Working tree clean; commit remains local as instructed.
Independent reviews remain with [R322] and [R323].

Open implementation risks/questions: none within this assignment.
