# Round 3 handoff

Status: REVIEW READY. Role: author.

- Repository: `Mister-M-alt/protocol-processor-control-plane-avb-milan`
- Origin verified: `https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan.git`
- Branch: `120-name-wr-export`
- Starting head: `a9b7874d415d935949becd7ccfd58799927efb08`
- Completed head: `83c84b19e09d397ed2eb6f5ace337686ce0ef86b`
- Tree: `7e6d16f3b5dfd3c4f1a0bc9ddb872f1156a1aea9`
- Commit subject: `Restore name-write harness contracts and warning-free builds`
- Commit body and trailers: none. Worktree: clean.

## Assignment and changes

[Assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/120#issuecomment-5846001897), items 1–2 only. The other review suggestions remain outside this round.

| Finding | File:line | Change |
|---|---|---|
| R334-F1 | `tb/pp_top/pp_top_wrap.sv:312` and `:321` | Move both new ports and their existing contracts before the effect-strobe bundle. Its four declarations are contiguous again. |
| R335-F1 | `tb/pp_top/sim_main.cpp:9744` | Add `[[maybe_unused]]` to `run_name_writes`; keep its body and default-build invocation unchanged. |

No behavior change: production RTL is byte-identical to the starting head; the harness body is unchanged; the only C++ difference is the attribute. The parent parser reports 211 harness ports and **162 undocumented**, matching the base debt. All six effect/name observation ports are documented. See [structural proof](focused/structure.json).

Both fresh harness builds emit **zero compiler warnings**. Default, fixture and focused simulation output matches the pre-change binaries byte for byte: 7,731/0, 20/0 and 85/0. The sequential canonical command reports 7,751/0. See [comparison receipt](focused/comparison.json). The pre-change comparison used the binaries already present in the lane; the source comparison independently proves the narrow change.

Read the assignment, both public review reports and relevant receipts, parent Rules 11–12, the port-contract and test-evidence scripts, and the repository workflow gates. Public evidence was read in a separate scratch clone at `5e689c1e5dd6468a5f21fc0edfaffa8699ace564`; all 179 published review manifest entries verified, including the path-redacted receipts. No private transcripts were used.

## Repository gates

Final executions, each captured directly to a log with no output pipe:

| Command | rc | Result | Receipt |
|---|---:|---|---|
| `make check` | 0 | All documentation prerequisites pass. | [log](gates/make-check.log) |
| `make -C tb/pp_top` | 0 | 7,751 checks: default 7,731; fixture 20; zero failures. | [log](gates/pp-top.log) |
| `make -C tb/pp_top name-writes` | 0 | 85 checks, zero failures. | [log](gates/name-writes.log) |
| `scripts/run_suites.sh` | 0 | 1,014,722 checks, zero failing suites. | [log](gates/run-suites.log) |
| `scripts/lint_hdl.sh` | 0 | 40 module tops clean. | [log](gates/lint-hdl.log) |
| `syn/yosys/run.sh` | 0 | 35 portability tops; engine memory mapping passes. | [log](gates/yosys.log) |
| `python3 scripts/check-integrator-params.py` | 0 | 24 top, 24 guide, 24 diagram parameters. | [log](gates/parameter-inventory.log) |
| `python3 scripts/check-links.py` | 0 | 915 links. | [log](gates/docs-links.log) |
| `python3 scripts/check-matrix.py` | 0 | 115 requirement rows and 17 gap findings. | [log](gates/docs-matrix.log) |
| `python3 scripts/render-wavedrom.py --check` | 0 | 18 diagram blocks. | [log](gates/docs-wavedrom.log) |
| `make stale` | 0 | Committed exports current. | [log](gates/docs-stale.log) |
| `python3 scripts/gen_matrix.py --check` | 0 | 92 rows; zero untested. | [log](gates/module-matrix.log) |
| `make -C tb/nvm_port figures` | 0 | 46 builds; historical figure checks pass. | [log](gates/nvm-figures.log) |
| `git diff --check` | 0 | Working-tree whitespace check passes. | [log](gates/diff-check.log) |

The committed range also passes `git diff --check a9b7874d415d935949becd7ccfd58799927efb08 HEAD`; see [receipt](gates/committed-diff-check.log). [Machine-readable gate results](gates/results.json) include elapsed times. Validation used the pinned 5.050 simulator with build parallelism capped at eight; [environment record](validation-environment.json) records versions and binary identity. Dependencies and scratch trees are outside this output directory.

## Parent consumer gates

Created the private copy with `git clone -q --no-hardlinks` from the named source parent, checked out `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`, and applied the supplied patch verbatim. Patch SHA-256: `1de2a73a99620b6aa6925cbf738a9d42bb2a263680f92aa4602fa35b6e32177c`.

Initialized `protocol-processor`, `gptp-processor` and `third_party/verilog-axis` from the source parent. Its `external` submodule is uninitialized and remained so. Set the processor checkout and staged gitlink to the completed head; created no parent commits. Ran the exact 12 argument vectors after the environment prefix from the supplied command inventory, in the private clone.

| # | Command | rc | Result | Receipt |
|---:|---|---:|---|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | C++ idiom ratchets pass. | [log](consumer/01.log) |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | Python idiom ratchets pass. | [log](consumer/02.log) |
| 3 | `python3 scripts/xvlog_gate.py --check` | 0 | Four existing processor findings equal the ratchet. | [log](consumer/03.log) |
| 4 | `python3 scripts/check_rtl_source_lists.py` | 0 | All four consumer source lists contain the required closure. | [log](consumer/04.log) |
| 5 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | Source inventory and self-tests pass. | [log](consumer/05.log) |
| 6 | `python3 sw/builder/test_builder.py` | 0 | All executed builder gates pass; calibration arm 11 not run (missing implementation report). | [log](consumer/06.log) |
| 7 | `make -C tb/verilator/pp_shadow -j8` | 0 | Three builds, 402 checks and zero failures each. | [log](consumer/07.log) |
| 8 | `python3 scripts/check_port_contracts.py` | 0 | Processor undocumented ports: 111 <= 111. | [log](consumer/08.log) |
| 9 | `python3 scripts/measure_naming.py --check` | 0 | Naming ratchet passes. | [log](consumer/09.log) |
| 10 | `python3 scripts/measure_test_evidence.py --check` | 0 | Zero unexplained source readers; three wall-clock-dependent files within budget. | [log](consumer/10.log) |
| 11 | `python3 scripts/docs_check.py` | 0 | Documentation checks pass. | [log](consumer/11.log) |
| 12 | `python3 scripts/lint_rtl.py --check` | 0 | 90 warnings <= 90 budget. | [log](consumer/12.log) |

All 12 command exits are zero. The builder's utilization-calibration arm is **NOT RUN** because the external implementation report is absent; it is not claimed as coverage. See [consumer results](consumer/results.json), [setup](consumer/setup.log), and [cleanup](consumer/cleanup.json).

The private `/tmp/pp120-consumer-check` copy was deleted after validation. The original parent remains clean at `f041ea4c95745a7adfa764a2a654ed056600ec8e`, with its processor still at `a9b7874d415d935949becd7ccfd58799927efb08`.

## Corrected execution attempts

- The first submodule initialization attempted the absent `external` checkout and stopped before two sibling checkouts were populated. The first C++ command correctly refused that incomplete population (rc 2). Forced checkout of the three locally available submodules repaired the private copy, then the entire consumer sequence passed. The refused attempt remains in `consumer/setup-incomplete-01.log` and `consumer/setup-incomplete-results.json`.
- The pre-change simulation comparison overlapped the first canonical harness command and added two entries to its shared generated tally. Both current simulations passed, but the aggregate correctly rejected four entries (rc 2). After the comparison finished, the sequential canonical rerun passed with exactly two entries. The fresh compiler output remains in `gates/pp-top-shared-tally-attempt.log`; the accepted canonical result is `gates/pp-top.log`. No source repair or assertion change was needed.

## Delivery

[PR-BODY.md](PR-BODY.md) preserves the full current PR body, updates the first line to `[A336]`, adds Round 3, and retains `Closes #120`. It contains no absolute home paths or attribution footer. [REVIEW-READY.md](REVIEW-READY.md) is the issue notification.

No push, pull-request edit, merge, hardware access, or parent-repository commit was performed. Independent review remains the next step.
