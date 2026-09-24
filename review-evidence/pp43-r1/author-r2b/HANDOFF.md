# [A262] Round 2b handoff

Author: [A262]. PR #111, issues #43/#49.
[Assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/43#issuecomment-5816452238).

Branch: `43-49-gsi-internal` in `$LANES/pp43-49-gsi-internal`.
Base: `a14ef8b4787b5309dd9ab472e82ae2b4a3fdbb72`.
Head: `a024ab51b926690be5ade8ec35ec1fa7dd23981b`.
Commit subject: `Split SRP failure-change test scenarios` (one line, no body or trailers).

Only `tb/srp_stream_fsms/sim_main.cpp` changed: eight added lines.
The existing L1–L7 scenario remains together. L8 (different streams with
independent sink latches) and L9 (registered sinks sharing one stream) now
have named methods, called in the original order immediately after L1–L7.
Both extracted scenarios retain their existing resets. Every original check,
input, expected value, message and simulation operation is unchanged.
Removing only the added declarations, method boundaries and calls reproduces
the complete baseline source byte for byte; see [source-equivalence.log](source-equivalence.log).

| Function | Before lines | After lines |
|---|---:|---:|
| `listener_failure_change_notifies_without_redeclaring` | 121 | 79 |
| `listener_failure_change_compares_each_sink_with_its_own_latch` | part of above | 20 |
| `listener_failure_change_notifies_registered_sinks_on_a_shared_stream` | part of above | 24 |
| Longest function anywhere in the file | 121 | 90 |

The SRP stream suite's complete runtime output before and after is identical:

```text
Before: 1087 checks: 1087 PASS, 0 FAIL
After:  1087 checks: 1087 PASS, 0 FAIL
```

The `Before:` and `After:` prefixes above label the two captures. Raw outputs:
[before](srp-stream-output-before.log), [after](srp-stream-output-after.log).
`diff -u` produced no output and returned 0 ([comparison](stream-output-diff.log),
[status](stream-output-diff.rc)). Build/run logs are
[before](srp-stream-before.log) and [after](srp-stream-after.log), both rc 0.

| Validation | Before checks | After checks | After result |
|---|---:|---:|---|
| SRP decoder | 190 | 190 | 190 PASS, 0 FAIL; rc 0 |
| SRP encoder | 556 | 556 | 556 PASS, 0 FAIL; rc 0 |
| SRP stream FSMs | 1087 | 1087 | 1087 PASS, 0 FAIL; rc 0 |
| SRP top | 259 | 259 | 259 PASS, 0 FAIL; rc 0 |
| Full bank, 32 suites | 16416 | 16416 | 0 failing; rc 0 |
| HDL lint, 40 modules | — | — | 40 OK; rc 0 |

Before counts are also recorded in [full-suites-before.log](full-suites-before.log).
Each SRP suite was explicitly run with `make -C tb/<suite>` after the split;
see `srp-decoder-after.log`, `srp-encoder-after.log`, `srp-stream-after.log`
and `srp-top-after.log` and their matching `.rc` files.
`./scripts/run_suites.sh` returned 0 before and after; its complete outputs
are byte-identical, including all 32 suite tallies and the final line:

```text
suites: 16416 checks total, 0 failing
```

Evidence: [after bank](full-suites-after.log),
[bank output comparison](full-suite-output-diff.log),
[comparison rc 0](full-suite-output-diff.rc), [lint](lint-after.log).
All validation commands ran in foreground subprocesses with 7200-second
timeouts, using the workflow-pinned simulator at
`$VALIDATION_TOOLS/verilator-v5.050/bin`. Output went directly to files,
never through a pipe. Each `.json` records the exact command, working
directory, timeout, elapsed time and actual return code.

Rule 11 and `long_functions()` were read from the read-only parent checkout
`$LANES/pp43-parent-consumer`. The limit is 100 physical lines,
including the opening signature and closing brace; a length greater than
100 is a finding, and the unchanged budget permits zero findings.

[measure_cpp_length.py](measure_cpp_length.py) copies the parent's unchanged
`scripts/check_cpp_idiom.py`, `scripts/cpp_idiom.budget`, and required
`scripts/code_quality_scope.py` into a fresh `/tmp/pp43-a262-cpp-*` directory.
It imports that copy, calls `blank_non_code()`, `long_functions()`, `scan()`,
`read_budget()` and `ratchet()` over the target file, then deletes the scratch
directory. Copy equality and SHA-256 hashes are recorded in each gate log.

```text
Before: long_functions(): [(922, 121)]
        FAIL: long function 1 > ratchet 0
        measurement rc 1 (expected reproduction)
After:  long_functions(): []
        long function: 0 <= 0: PASS
        Source scan and unchanged budget: PASS
        measurement rc 0
```

Evidence: [gate-before.log](gate-before.log), [gate-after.log](gate-after.log).
Both logs confirm their scratch directories were deleted. This proves the
requested measurement over the changed file; the parent checkout was not
modified or used for a full-tree gate run.

The final worktree is clean. No push, PR edit, merge, delegation or hardware
operation was performed. Review-ready comment text is in
[REVIEW_READY.md](REVIEW_READY.md); the publication response is saved in
`issue-ready.log`.
