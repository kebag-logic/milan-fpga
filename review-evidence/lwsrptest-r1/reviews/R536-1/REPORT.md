[R536] POSITIVE - exact head e4f9995b791489c53b8ccb8a8dc09ec508e32e6b

# R536-1 internal independent review: kebag-logic/lwSRP PR #3 (Closes #2)

- Reviewed head: `e4f9995b791489c53b8ccb8a8dc09ec508e32e6b`, tree `9457a9568dad668a04e2a4042f6d3f984aebe387`, parent `19f5796b63652eb1151906de73cb827d4980a53f` (base). It is one commit, and its tree is identical to the author's `ad6199083a1eb242f37dacf88de94bd00c4b3658`. That commit is publicly reachable with the same tree (`receipts/public-metadata.txt`).
- Review type: a cleared-context independent pass in a detached clone. Nothing was written to GitHub, and no source was edited. All probes ran on disposable `git archive` copies.
- Verdict: **POSITIVE**. There are no open BLOCKER, MAJOR or MINOR findings. One RESIDUE and three SUGGESTIONs are recorded below.

## Reconstruction (in order)

1. **Repository guidance.** There is no `AGENTS.md` or `CONTRIBUTING.md` at this head. The repository's coding-style file requires braces on all control flow and forbids typedef enums. The new C files contain no control flow and no enums. `README.md` gives the build commands (`cmake -B build -DCMAKE_BUILD_TYPE=Debug`, `cmake --build build`, `behave`, `ctest --test-dir build --output-on-failure`) and names cgreen and behave as dependencies. `doc/architecture.md` §1 shows the directory layout and §10 covers testing.
2. **Issue #2 frozen acceptance.**
   - (1) behave runs every scenario and returns 0, and the missing symbol is either exported or the harness is corrected, with the reason stated.
   - (2) ctest builds and runs the `mrp_pdu` codec tests with their real assertion count, and the placeholder is removed or kept only as an explicitly empty target.
   - (3) Each fix has a check that fails without it.
   - (4) No change to protocol behaviour.
   - The assignment comment limits the change to the export, the ctypes harness, the CMake test wiring and the tests. It also requires SPDX on new files, before/after counts with exit codes, a planted reversal for each fix, and one-line commit subjects.
   - No maintainer comment widens or narrows this scope.
3. **Interface authority.** `src/include/shish_lan/switch.h:26-29` defines `shlan_connect`, `shlan_disconnect`, `shlan_port_enable` and `shlan_port_disable` as `static inline` vtable dispatchers. That is why the base library had no `shlan_connect` symbol, and it is the reason the PR body states. The codec authority is the unchanged `tests/unit/mrp_pdu_test.c` (MRPDU helpers, §10.8.2.10).
4. **Diff `19f5796..e4f9995`.** Five files changed: `CMakeLists.txt` (M), `tests/features/environment.py` (M), `tests/features/switch_bindings.c` (A), `tests/unit/main.c` (A) and `tests/unit/placeholder.c` (D). Nothing under `src/`, `zephyr/`, `Kconfig.zephyr`, `doc/`, `README.md`, the codec test, the feature file or the step file changed (`receipts/static-checks.txt`).
5. **Public evidence.** The milan-fpga archive `d9259a0e` contains `review-evidence/lwsrptest-r1/{MANIFEST.json, author/CHECKS.txt, author/HANDOFF.md, author/PR-BODY.md}`. The downloaded files' sha256 values match `MANIFEST.json` `published_sha256` (`receipts/public-metadata.txt`). The issue and PR show no manager evidence comment beyond the review-start comments. lwSRP has no hosted checks at this head: 0 check runs and 0 commit statuses.
6. **Prior public review findings.** None exist. The PR has 0 reviews and 0 inline comments, and its 2 conversation comments are the R536-1 and R537-1 start notices. Nothing needs to be resolved or retained.

## Executed evidence (reviewer-run, own cgreen 1.7.0 built from source into scratch)

| Probe | Check | Result | Receipt |
| --- | --- | --- | --- |
| Head baseline | configure / build / `ctest --output-on-failure` / `behave` | rc 0 / 0 / 0 / 0. CTest 1/1. The runner reports 9 tests and `Completed "mrp_pdu_suite": 1690 passes`. Behave: 1 feature, 3 scenarios and 10 steps passed, 0 failed or skipped | `receipts/probes/p0_head.*` |
| Base (before) | same | ctest rc 0 with `Completed "main": No assertions.`. Behave rc 1, `HOOK-ERROR in before_all ... undefined symbol: shlan_connect`, with 1 feature, 3 scenarios and 10 steps untested | `receipts/probes/p1_base.*` |
| Reversal 1: drop `switch_bindings.c` from the library sources | behave | rc 1, `undefined symbol: shlan_test_connect`, all untested | `receipts/probes/r1_drop_bindings.*` |
| Reversal 2: restore base `environment.py` | behave | rc 1, `undefined symbol: shlan_connect` | `receipts/probes/r2_old_env.*` |
| Reversal 3: restore `placeholder.c` and the original unit source list | ctest | rc 8, `No assertions`, 0/1 passed | `receipts/probes/r3_placeholder.*` |
| Reversal 4: runner uses `create_test_suite()` | ctest | rc 8, `No assertions`, 0/1 passed | `receipts/probes/r4_empty_runner.*` |
| Reversal 5: expected packed byte 215 changed to 214 | ctest | rc 8, `1689 passes, 1 failure` at `mrp_pdu_test.c:41` | `receipts/probes/r5_wrong_byte.*` |
| Own: configure with no cgreen on the search path | cmake | rc 1 at `CMakeLists.txt:45` | `receipts/probes/x1_no_cgreen.*` |
| Own: remove the `FAIL_REGULAR_EXPRESSION` guard and use the empty runner | ctest | rc 0. This shows the guard carries the empty-suite rejection | `receipts/probes/x2_*` |
| Own: `port_enable` binding always returns 0 | behave | rc 1, 1 scenario failed | `receipts/probes/x4_*` |
| Own: `port_disable` binding calls enable; `connect` binding is a no-op | behave | rc 0 for both. Not detected; see SUGGESTION R536-1-02 | `receipts/probes/x3_*`, `x5_*` |
| Own: exported dynamic symbols, base to head | `nm -D` | only `shlan_test_{connect,disconnect,port_enable,port_disable}` are added | `receipts/probe2/exported-symbols.diff` |
| Own: Zephyr module source list (stubbed Zephyr CMake functions, no cgreen) | cmake | configure rc 0 for both base and head. The source lists are identical: 7 `src/` files, no bindings, and no host targets | `receipts/probe2/z_*-zephyr-sources.txt`, `zephyr-sources.diff` |
| Own: strict warnings (`-Wmissing-prototypes -Wstrict-prototypes -Wshadow -Wconversion`), gcc and clang, head and base | build | all rc 0. The repository flags give no warnings. The extra flags add only missing-prototype warnings in the new or rewired test files; see SUGGESTION R536-1-04 | `receipts/probe2/s_*-warnings.txt` |
| Own: ASan+UBSan head build | unit runner with leak detection; behave with ASan preloaded | rc 0 / rc 0, 0 sanitizer reports, 9 tests / 1690 passes | `receipts/probe2/san-*.log` |
| Own: repeatability | 3 more ctest and behave runs | all rc 0 | `receipts/probe2/repeat-*.log` |
| Own: static checks | scope, commit shape, SPDX, privacy, clone integrity | see Robustness and Docs below | `receipts/static-checks.txt` |

The cgreen empty-suite text `No assertions` is printed by `src/text_reporter.c:194` at cgreen tags 1.4.0, 1.6.0, 1.6.3 and 1.7.0. The CTest guard therefore does not depend on one cgreen release (`receipts/toolchain.txt`).

All figures in the PR body match these runs:
- before: CTest exit 0 with zero assertions, and behave exit 1 at setup with 3 scenarios and 10 steps untested
- after: 9 tests and 1,690 assertions, and 1 feature, 3 scenarios and 10 steps
- reversal exit codes: 1 and 8
- configure without cgreen: exit 1

## Lenses

**Conformance: CLEAN.**
- Acceptance 1 is met. Behave runs all 3 scenarios in `tests/features/` with rc 0. The cause is stated in the PR body: the helpers are static inline. The fix exports test bindings (`tests/features/switch_bindings.c:6-24`) and maps them in the harness (`tests/features/environment.py:31-42`).
- Acceptance 2 is met. `CMakeLists.txt:48-51` builds `main.c` + `mrp_pdu_test.c` and registers `unit`, which reports 1690 real assertions. `placeholder.c` is deleted.
- Acceptance 3 is met. Each of the five reversals fails the named check, and the extra guards fail too (x1, x2).
- Acceptance 4 is met. `src/` is byte-identical to base and the Zephyr source list is identical. The bindings only forward to the existing inline dispatchers.

**RTL: CLEAN (not applicable).** lwSRP is a C11 software library with no HDL, synthesis or simulation sources, and this PR touches only CMake, C test glue and a Python harness. The pinned Verilator was neither needed nor used.

**Robustness: CLEAN.**
- `CMakeLists.txt:45-46` makes cgreen `REQUIRED`, so a missing dependency can no longer silently drop all unit tests (x1 rc 1). `REQUIRED` needs CMake 3.18 or later, and the project minimum is 3.20.
- The empty-suite guard `CMakeLists.txt:53` is shown to carry the empty-suite rejection (x2).
- The runner frees its suite and reporter and is clean under ASan/LSan and UBSan.
- The ctypes prototypes match the C signatures: `int(void*)`, `void(void*)` and `int(void*, uint8_t)`.
- The bindings do not reach the Zephyr module build (stub probe) and add only four `shlan_test_*` exports to the host-only, non-installed `libshlan.so`, which already embeds the simulation adapter.
- Clone integrity after the probes: HEAD/tree exact, the index matches the tree, the working-tree blob bytes and modes match HEAD, there are no untracked or ignored entries, and the tree has no gitlinks, so no submodule gitlinks are required.

**Tests: CLEAN.**
- Before and after counts and exit codes were reproduced independently.
- The five planted reversals each fail their named check: behave rc 1 for reversals 1 and 2, and ctest rc 8 for reversals 3 to 5.
- A real codec assertion failure propagates to the CTest exit code (reversal 5).
- The existing codec assertions and scenarios are unchanged.

**Docs: CLEAN.**
- The new files `tests/features/switch_bindings.c:1` and `tests/unit/main.c:1` start with `SPDX-License-Identifier: Apache-2.0`.
- The commit subject is one line with no body. Its author and committer identity matches the earlier repository commits.
- The diff, commit message and published author evidence contain no host paths, account names, or tool or model names.
- The PR body states the reason, the cgreen requirement and the reversal outcomes, and all of them were verified.
- Its links point at `ad61990`, which is public and has the identical tree.
- One stale layout listing is recorded as RESIDUE R536-1-01. Documentation edits were outside the assignment's change scope.

## Findings

| ID | Severity | Lenses | Location | Authority / evidence | Impact | Required outcome | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R536-1-01 | RESIDUE | Docs | `doc/architecture.md:69-76` (§1 Directory Layout) | Line 71 still lists `tests/unit/placeholder.c`, which this PR deletes. It also omits the new `tests/unit/main.c` and `tests/features/switch_bindings.c` (`receipts/static-checks.txt` changed-file list) | Prose layout listing only. It changes no test, code, figure or claim. The issue's assigned scope excluded doc edits | In §1, replace line 71 `    │   └── placeholder.c` with `    │   └── main.c                 cgreen runner for mrp_pdu_suite`, and after line 74 (`environment.py`) add `        ├── switch_bindings.c       ctypes test bindings for switch.h inline helpers`. Carry this to the residue checklist or a follow-up docs change | Read §1 at the later head and check that it lists `main.c` and `switch_bindings.c` and not `placeholder.c` |
| R536-1-02 | SUGGESTION | Tests, Robustness | `tests/features/steps/switch_steps.py:26-36` (unchanged); `tests/features/switch_bindings.c:11-24` | x3: a `port_disable` binding that calls enable still passes behave. x5: a no-op `connect` binding still passes behave. The "active/inactive" steps use the enable/disable return code as a proxy for state, and nothing observes connect or disconnect | A miswired binding for disable, connect or disconnect would go undetected. This scenario design predates the PR, and the issue did not ask for stronger scenarios | Optional follow-up issue: add an observable port and connection state accessor (for example, on the simulation adapter) and assert it in the Then steps | Re-run x3/x5 and expect behave rc 1 |
| R536-1-03 | SUGGESTION | Robustness | `CMakeLists.txt:38`, `CMakeLists.txt:45-46` | A host (non-Zephyr) configure now needs cgreen even to build only `libshlan.so`, and that library exports four `shlan_test_*` symbols. The Zephyr module path is unaffected (stub probe), and the host target has no install rules | No integrator impact today, because the host library is the test and simulation artefact. If a host integration path is ever documented, the test glue and the hard cgreen requirement would come with it | Optional: gate the bindings, cgreen and the unit target behind a test option (for example, CTest's `BUILD_TESTING`, default ON) | Configure with the option OFF and no cgreen, then `nm -D` shows no `shlan_test_*` |
| R536-1-04 | SUGGESTION | Tests | `tests/features/switch_bindings.c:6-24`, `tests/unit/main.c:5`, `tests/unit/mrp_pdu_test.c:139` | With `-Wmissing-prototypes` (not a repository flag), gcc and clang warn that the four bindings and `mrp_pdu_suite` have no previous prototype, because the suite is declared only in the runner (`receipts/probe2/s_head_*-warnings.txt`) | None under the repository's `-Wall -Wextra -Wpedantic`. A signature drift between the runner and the suite would only be caught at link time, not at compile time | Optional: a small test-only header that declares `mrp_pdu_suite` and the bindings, included by both sides | Strict-flag build reports no warnings in these files |

There is no open BLOCKER, MAJOR or MINOR finding.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Issue #2 acceptance and assignment; `switch.h:26-29`; full diff; base/head behave and ctest; Zephyr source-list probe; `src/` diff (empty) | R536-1 | e4f9995b791489c53b8ccb8a8dc09ec508e32e6b |
| RTL | CLEAN (not applicable) | Repository content (C11 library, CMake, Python harness); no HDL in tree or diff | R536-1 | e4f9995b791489c53b8ccb8a8dc09ec508e32e6b |
| Robustness | CLEAN | `CMakeLists.txt:38-53`; `switch_bindings.c`; `environment.py:31-42`; `main.c`; x1/x2; exported-symbol diff; Zephyr stub; ASan/UBSan; strict-warning builds; clone integrity | R536-1 | e4f9995b791489c53b8ccb8a8dc09ec508e32e6b |
| Tests | CLEAN | p0/p1 baselines; reversals r1-r5; own mutants x2-x5; repeat runs; author `CHECKS.txt`/`HANDOFF.md` claims cross-checked | R536-1 | e4f9995b791489c53b8ccb8a8dc09ec508e32e6b |
| Docs | CLEAN | SPDX on new files; commit message and identity; PR body claims and links; `README.md`; `doc/architecture.md` §1/§10; privacy scan of diff, message and published author evidence | R536-1 | e4f9995b791489c53b8ccb8a8dc09ec508e32e6b |

## Real limits

- Only one host toolchain was used (`receipts/toolchain.txt`): CMake/CTest 4.4.3, gcc 16.2.1, clang 22.1.8, Python 3.14.7, behave 1.3.3, and cgreen 1.7.0 built from its tag. CMake 3.20 (the declared minimum), distribution cgreen packages and macOS (`libshlan.dylib`) were not exercised. Only the cgreen message string was checked across 1.4.0 to 1.7.0.
- The Zephyr check stubs Zephyr's CMake functions. No real Zephyr/west build was run.
- lwSRP has no hosted CI. There are no exact-head hosted jobs to inspect, so no hosted context is claimed as executed.
- The milan-fpga parent banks, builder and native banks, Verilator, Docker/act and hardware were out of scope and not run. Physical calibration was NOT RUN, and nothing here is hardware proof.
- This review covers source validation at the exact head only. It does not cover the current-dev merge candidate.

## Pending manager duties

- Build and validate the final current-dev candidate (source base `19f5796`, live dev `910f338dbd050f4efd2d96991ddcf928a583d55f`) at the merge turn.
- Own hosted/act acceptance. lwSRP currently reports no checks at this head.
- Carry RESIDUE R536-1-01 to the residue checklist, and decide whether SUGGESTIONs R536-1-02 to R536-1-04 become follow-up issues.
- Obtain the second independent positive review (R537) before merge.
- Publish this report and the files listed in `MANIFEST.sha256`. The scripts `probe.sh`, `probe2.sh` and `checks.sh` reproduce the receipts, given a clone and a cgreen prefix. Host paths in the receipts are redacted to `$PACKET`, `$WORK`, `$CLONE`, `$CGREEN_PREFIX` and `$USERBASE`.

R536-1 FINISHED
