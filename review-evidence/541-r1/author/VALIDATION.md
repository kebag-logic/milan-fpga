[A304] Validation evidence for #541

Head: `2734b771bcf0b383ea62ef05744452827bafe9e4`
Base: `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`

All commands ran in foreground processes with a 7,200-second timeout.
Gate stdout and stderr went directly to the named log, without pipelines.

Existing gate dependencies were selected with this PATH prefix:

```sh
export PATH=$VALIDATION_TOOLS/verilator-v5.050/bin:$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin:$PATH
```

No dependencies or tree exports were placed in the report directory.

| Command | Mode | Exit | Log |
|---|---|---|---|
| `python3 scripts/docs_check.py` | candidate worktree | 0 | `docs-git.log` |
| `python3 scripts/check_em_dash.py --base 5b73d3f47dfed519eb988c13d6beb1db664ef1e0` | candidate worktree | 0 | `em-dash.log` |
| `python3 scripts/check_doc_style.py` | candidate worktree | 0 | `doc-style.log` |
| `python3 scripts/gen_toc.py --check` | candidate worktree | 0 | `toc-check.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | candidate worktree | 0 | `toc-anchors.log` |
| `python3 scripts/check_doc_paths.py` | candidate worktree | 0 | `doc-paths.log` |
| `python3 docs/traceability/gen_module_matrix.py --check` | candidate worktree | 0 | `module-matrix.log` |
| `python3 scripts/xvlog_gate.py --check` | candidate worktree | 0 | `xvlog.log` |
| `python3 scripts/check_sv_idiom.py` | candidate worktree | 0 | `sv-idiom.log` |
| `python3 scripts/check_cpp_idiom.py` | candidate worktree | 0 | `cpp-idiom.log` |
| `python3 scripts/check_py_idiom.py` | candidate worktree | 0 | `py-idiom.log` |
| `python3 scripts/measure_test_evidence.py --check` | candidate worktree | 0 | `test-evidence.log` |
| `git diff --check` | candidate worktree | 0 | `diff-check.log` |
| `python3 scripts/docs_check.py` | HEAD archive without Git metadata | 0 | `docs-no-git.log` |

The no-Git mode used `git archive --format=tar -o <temporary-file> HEAD`,
extracted into a temporary directory without Git metadata, followed by
`python3 scripts/docs_check.py` from that directory. The temporary tree was
deleted when the check finished. No other checkout was created.

Both documentation modes read 165 Markdown and 865 text files with zero
findings. The no-Git mode skips only its Git-dependent inventory-parity
self-test. Live HDL analysis passed at its four existing pinned-processor
findings, with zero findings in the parent HDL population.

| Simulation command | Result | Log |
|---|---|---|
| `make -C tb/verilator/crf_rx` | rc 0; unit 13,836 checks, discontinuity 1,932 checks, connected talker-step 69 checks, mutation campaign 9 controls; zero failures | `crf_rx.log` |
| `make -C tb/verilator/mmcm_servo` | rc 0; unit 85 checks, playback rails 8 checks, PHC-step 113 checks; zero failures | `mmcm_servo.log` |

The mutation campaign rebuilt two positive controls and seven mutants.
Both clean controls exited zero. All seven mutants exited one and produced
their required named assertion failures. In particular:

```text
[PASS] validation_error_unlocks: rc=1
  named rejection: validation error preserves established lock
== crf_rx mutants: checks: 9   failures: 0 ==
```

The negative mutant exit is the expected detection result, not a failed gate.
The containing campaign and containing receiver make command both exited zero.
The new direct assertions also passed for the counter increment, retained lock,
valid resume, and silence before and after the 100 ms threshold.

Additional check: comment-stripped receiver RTL equals the base exactly.
The commit changes four files; only the receiver header changes in RTL.
No ratchet, gate, baseline or existing assertion was weakened.
