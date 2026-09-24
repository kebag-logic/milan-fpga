[A281] Round 4 handoff for FPGA-gPTP #75 / PR #76

Head: `6fd2ceb025e2a1bc7eaa6ccb09558584f0d499bf` on `75-slew-active`.
Baseline: `3face0914efd9d5e71f36da7e30108cfe09c837d`.
Commit: `Split slew lifecycle checks into phases and annotate the evidence checker`. One line, no body or trailers. The source, parent and parent submodule working trees are clean; [final state](final-state.json).

The [assignment](https://github.com/Mister-M-alt/FPGA-gPTP/issues/75#issuecomment-5821534416) is implemented in exactly two files. [The patch](round4.patch) splits the lifecycle scenario into named phases and adds the requested Python signatures and main docstring. All other 102 tracked files match the baseline, including RTL, the generator, ROM images, mutation definitions and documentation. [Scope verification](scope-verification.json) also proves that expanding the phases reproduces the original statements in order.

## Phase sizes

| Function | Lines, including declaration and closing brace |
|---|---:|
| `exercise_the_slew_level_contract` | 10 |
| `start_slew_contract_with_inactive_tracking` | 13 |
| `keep_slew_inactive_across_idle_lapses` | 24 |
| `keep_slew_inactive_across_capability_loss` | 28 |
| `exercise_slew_boundaries_and_replacement_steps` | 18 |
| `hold_slew_across_missing_pairs_and_gm_change` | 30 |
| `retire_slew_on_mastership_and_resume_tracking` | 22 |
| `hold_slew_across_capability_loss` | 15 |
| `clear_slew_on_warm_reset` | 17 |

## Before and after

| Evidence | Before | After | Comparison |
|---|---|---|---|
| Whole engine suite, each of three images | 1,613 PASS, 0 FAIL | 1,613 PASS, 0 FAIL | All 4,839 names and order identical |
| Engine mutation campaign | 33 caught; positive control passes | 33 caught; positive control passes | Same killing checks, return codes and full ordered failure lists |
| Required slew controls | 6 caught at their required named checks | 6 caught at their required named checks | Identical |
| Source-evidence ledger | 20 exact, 0 findings | 20 exact, 0 findings | stdout and stderr byte-identical |
| Ledger self-test | PASS, 7 arms | PASS, 7 arms | stdout and stderr byte-identical |

- Engine lists: [before](before-engine-checks.txt), [after](after-engine-checks.txt). Shared SHA-256: `bb5429fd3c8f27be8ca63f364259ade70e31683bda5be74c008d6c0347fb0266`.
- Mutant verdict tables: [before](before-mutant-verdicts.tsv), [after](after-mutant-verdicts.tsv). Shared SHA-256: `4600198a4b39daf90efd2f9af1ffbc07c41412a63447c10dbf7a731f9b4404a7`.
- The shipped campaign tables are [before](before-mutant-gate-table.txt) and [after](after-mutant-gate-table.txt); each has 34 PASS, 0 FAIL including the positive control.
- [All comparisons](comparisons.json) pass. The five comparison diffs for engine checks, mutant verdicts, shipped mutant output, ledger output and self-test output are empty; each direct comparison returns 0. The Python executable syntax trees match after excluding annotations and the new docstring.

The production harness prints only failures and its tally. [The trace script](trace_checks.py) therefore adds one check-name print in `expect()` in a temporary source export, then runs all three images. It changes no stimulus, expectation, counter or simulated clock operation. Both ordinary engine runs also pass. Source exports and builds stay outside this packet.

[The observer](observer/sitecustomize.py) copies the mutation campaign's already-captured output, preserving each subprocess result and the shipped verdict logic. Both observed campaigns invoke the unchanged `make -C tb/verilator/engine mutants`. The separate unobserved `make -j8` also runs the full campaign. The baseline's last 22 generator mutations reuse its already-built control executable; the live C++ edit occurred only after the final baseline C++ variant had finished, as recorded in [the reuse boundary receipt](baseline-reuse-boundary.json).

## Repository gates

`make -j8` returns 0 with no skipped suites. It runs the contract check; arithmetic, parser, engine, adapter, packet-generator and timestamp-tag suites; engine, adapter and packet-generator mutation controls; both lint targets; and documentation, diagram and source-evidence checks and self-tests. The candidate tracks no CI workflow files. The separate `make -C tb/verilator/engine mutants` also returns 0.

[Gate inventory](gate-inventory.json), [all commands and return codes](gate-results.tsv), [main gate receipt](after-make.receipt.json), [mutation gate receipt](after-mutants.receipt.json), and their adjacent stdout/stderr logs record the results. Each command runs as a foreground subprocess, without a shell pipeline, with a three-hour deadline. Existing dependencies are identified in [environment.json](environment.json).

## Parent consumer

The supplied parent was `584a8c17d67d9c86df3e18913e34e237f58cacc7`, on `dev` `573f0052a0e4412e81f0845438fcec2086ce5d55` plus one local gitlink commit. The new source head was fetched locally into `gptp-processor`, checked out there, and pinned by local parent commit `d2d89eb677d835c4b888b042833cf274290a3e30`. That commit changes only the gitlink and has a one-line message. [Commit details](commits.json).

| Command from the consumer | rc | Evidence |
|---|---:|---|
| `python3 scripts/check_cpp_idiom.py` | 0 | [receipt](parent-cpp.receipt.json) |
| `python3 scripts/check_py_idiom.py` | 0 | [receipt](parent-python.receipt.json) |
| `python3 scripts/xvlog_gate.py --check` | 0 | [receipt](parent-xvlog.receipt.json) |
| `python3 scripts/check_rtl_source_lists.py` | 0 | [receipt](parent-source-lists.receipt.json) |
| `python3 sw/builder/test_builder.py` | 0 | [receipt](parent-builder.receipt.json) |
| `make -C tb/verilator/gptp_shadow -j8` | 0 | [receipt](parent-shadow.receipt.json) |

The shadow suite passes 309 checks and all 9 mutation controls. Its existing missing-port warnings include `phc_slew_active_o`; connecting that port remains #545 work. The C++ gate reports zero long functions. The Python gate reports zero unannotated and zero undocumented public functions. The source parser matches its four existing findings in the other processor; it reports no new findings. The builder returns 0 but declares gate 11 not run: its calibration comparison needs the absent mf48 utilization report. This result does not cover that arm.

## Review handoff

The updated [PR body](PR-BODY.md) starts with `[A281]`, retains `Closes #75`, and includes Round 4. The assignment calls for R304's delta review at the new head; R305-3 remains the recorded positive review of the ancestor `3face091`. This handoff supplies author evidence, not a review verdict.

The parent #545 connection, timing-policy decisions and hardware validation remain separate work. No push, PR edit, merge or hardware operation was performed.
