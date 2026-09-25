[A293]

Status: REVIEW READY. Round 2 for processor PR #118, issues #55, #56 and #77.
Processor branch: `510-mvu-waiver`.
Head: `490e4309749c83f92d794a8ff10d3043e0f5f080`.
Merged baseline: `b51bc3893b06f4d39be49726c1b8f4ed6c65573d`.
Subject: `Refresh merged MVU waiver evidence and pin refusal under lock`.

Assignment: [issue #77](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/77#issuecomment-5824629677).
Reviews: [R318-1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/118#issuecomment-5824628105)
and [R319-1](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/118#issuecomment-5824520215).
The published evidence archives at `010c8a321ff2dce1b449e2481df80afc50bddb44`
and `282093f98aa0857cf46a33032d36aec7fb610ce7` were fetched read-only into
scratch, inspected, checked against their manifests, and deleted.
See [archive verification](review-archive-verification.json).

| Assignment item / finding | Change |
|---|---|
| Item 1; R318-1-F1 / R319-1-F1 | Re-measured the merged baseline and both ROM mutations. The README names that exact commit and explicitly says the counts predate M4L and are historical measurements. Later heads require remeasurement |
| Item 2; R318-1-S1 / R319-1-S1 | Both waiver descriptions quote the complete recommendation note, with spelling normalization disclosed. They and REQ-MVU-003/004 add a targeted Milan revision making support mandatory as a revisit trigger |
| Item 2; R319-1-S2 | Section 11 replaces the phantom P-ID with the F01.5 microcode constant name |
| Item 2; R318-1-S2 / R319-1-S3 | M4L checks a byte-exact lock grant, both complete nonzero SETs from a second controller, each NOT_IMPLEMENTED echo, no extra AECP response during each 20 ms observation, and a byte-exact unlock |
| Item 3 | No RTL change. All required local processor and parent validation is recorded below |

Only four tracked files change: the compliance review, AECP architecture,
and `tb/pp_top/{README.md,sim_main.cpp}`. Implementation tree
`d8879608b8fae8c06a505d7d5d485a97903a5766` is identical to the merged baseline.
The gate definitions, scripts, synthesis sources and NVM figure inputs are also
unchanged. See [source scope](source-scope.json) and [round-2 patch](round2.patch).

These counts are measurements of the named source snapshots, not live totals.

| Measurement | Merged baseline `b51bc389` | Round-2 content in `490e4309` |
|---|---|---|
| Top-level suite | 7,660 PASS: 7,640 default + 20 fixture; rc 0 | 7,666 PASS: 7,646 default + 20 fixture; rc 0 |
| Word 560, NOT_IMPLEMENTED to SUCCESS | 197 failures / 7,640; rc 1 | 199 failures / 7,646; rc 1 |
| Word 741, features_flags 0 to 3 | 3 failures / 7,640; rc 1 | 3 failures / 7,646; rc 1 |

The SUCCESS mutation fails the status and byte-exact M4 assertions for every
0x0001–0x0005 command, while their lengths and cdl remain correct. Round 2 adds
two failing M4L refusal checks under the same mutation. The feature mutation
fails M1, M2 features_flags and M5b. Both mutations use disposable ROM copies;
the original remains unchanged, SHA-256
`23605682298004274d80437a4ad83640c2d70e4fc161b23defb7c6eab6fa7144`.
Reproduce with [MVU-MUTANTS.py](MVU-MUTANTS.py) after building the chosen snapshot.
See [merged measurements](merged-mutation-results.json) and
[round-2 measurements](round2-mutation-results.json).

All gates run in the foreground, with direct return codes and no gate-output
pipeline. [gate-results.jsonl](gate-results.jsonl) records each command, starting
HEAD, runtime, return code and log. Pre-commit entries name the merged baseline;
the round-2 top-level run and `make check` tested the subsequently committed
content. The lint, portability and NVM figure inputs did not change.
The CI-pinned compiler release 5.050 was used, with compilation capped at eight
jobs. [validation-context.json](validation-context.json) records the workflow
and executable versions.

| Processor command | Result |
|---|---|
| `python3 scripts/check-links.py` | rc 0; 872 links |
| `python3 scripts/check-matrix.py` | rc 0; 115 requirement rows, 17 GAP findings |
| `python3 scripts/render-wavedrom.py --check` | rc 0; 18 blocks |
| `make stale` | rc 0 |
| `./scripts/lint_hdl.sh` | rc 0 |
| `python3 scripts/gen_matrix.py --check` | rc 0; 92 rows, zero untested |
| `make -C tb/nvm_port figures` | rc 0; every measured figure agrees; pull #13 head fetched first as CI requires |
| `./syn/yosys/run.sh` | rc 0; all tops elaborate and memory-mapping assertions pass |
| `make check` | rc 0; 41 diagram blocks, 18 waveform blocks, 872 links and both matrices |
| `make -C tb/pp_top run` | rc 0; counts above |
| `./scripts/run_suites.sh` | rc 0 at processor head; 33 suites, 1,014,637 checks, zero failing |

Parent consumer base for the `508-pp-pin-adopt` lane:
`35f0695815c202392b6b4806bb9f59dd110687ed`.
The supplied checkout was detached at local commit
`e5951e4c4d61d592eb20825f16ca18d4adb717b1`, whose only change from that base
was the processor gitlink at `b51bc389`. The new local parent commit is
`d1d1fbba98563524a46cc825e4cf9936603ef1bb`; only its processor gitlink changes to the processor head above.
The checkout remains detached, and no parent branch is pushed.

All ten parent commands returned **0** at the local parent commit above.

| Command | Result / receipt |
|---|---|
| `python3 scripts/check_cpp_idiom.py` | rc 0; [parent-cpp-idiom.log](parent-cpp-idiom.log) |
| `python3 scripts/check_py_idiom.py` | rc 0; [parent-py-idiom.log](parent-py-idiom.log) |
| `python3 scripts/xvlog_gate.py --check` | rc 0; [parent-xvlog.log](parent-xvlog.log) |
| `python3 scripts/check_rtl_source_lists.py` | rc 0; [parent-source-lists.log](parent-source-lists.log) |
| `python3 scripts/pp_srcs.py --check --selftest` | rc 0; [parent-pp-srcs.log](parent-pp-srcs.log) |
| `python3 scripts/check_port_contracts.py` | rc 0; [parent-port-contracts.log](parent-port-contracts.log) |
| `python3 scripts/measure_naming.py --check` | rc 0; [parent-naming.log](parent-naming.log) |
| `python3 scripts/measure_test_evidence.py --check` | rc 0; [parent-test-evidence.log](parent-test-evidence.log) |
| `python3 scripts/docs_check.py` | rc 0; [parent-docs.log](parent-docs.log) |
| `make -C tb/verilator/pp_shadow -j8` | rc 0; 371 checks, zero failures; [parent-pp-shadow.log](parent-pp-shadow.log) |


Existing parent ratchet budgets are unchanged. The source-analysis gate retains
four recorded processor findings; the native top-list check retains six recorded
omissions. Both gates pass their existing budgets. No push, PR edit, merge,
sub-agent or hardware operation was performed. The processor and parent
tracked working trees are clean at handoff. REQ-MVU-005 timing remains in #57.
The parent integration owner still needs to retire the SUBMODULES known-conflict
row when adopting this pin; this assignment permits only the gitlink change.
Hosted validation and the current-dev integration candidate remain subsequent
integration work.

[PR-BODY.md](PR-BODY.md) contains the full updated proposed PR body.
[REVIEW-READY.md](REVIEW-READY.md) contains the issue #77 handoff comment.
