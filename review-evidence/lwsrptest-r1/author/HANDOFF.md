<!-- SPDX-License-Identifier: Apache-2.0 -->

# Handoff

Status: REVIEW READY. Local commit complete, verified, and unpushed.

Author: [A562]. Internal reviewer: [R536]. External reviewer: [R537].

Branch: tests-harness. Base: 19f5796b63652eb1151906de73cb827d4980a53f. Head: ad6199083a1eb242f37dacf88de94bd00c4b3658.
Origin verified as https://github.com/kebag-logic/lwSRP.git before work.
Initial worktree was clean. No push, PR creation, merge, rebase, amend, or sub-agent work occurred.

Read the complete [issue body](https://github.com/kebag-logic/lwSRP/issues/2) and [assignment](https://github.com/kebag-logic/lwSRP/issues/2#issuecomment-6030566128).
Posted [TAKEN](https://github.com/kebag-logic/lwSRP/issues/2#issuecomment-6030580466).
Posted [REVIEW READY](https://github.com/kebag-logic/lwSRP/issues/2#issuecomment-6030686979) with the full head; posting rc 0.

## Changes

| File:line | Change and reason |
| --- | --- |
| CMakeLists.txt:38 | Build test bindings into the host shared library. The Zephyr source list is unchanged. |
| CMakeLists.txt:45 | Require cgreen library and headers so a missing dependency cannot silently disable all unit tests. |
| CMakeLists.txt:48 | Compile the codec suite with its runner and register it as the unit CTest target. |
| CMakeLists.txt:53 | Fail CTest when cgreen reports No assertions, even when the process exits zero. |
| tests/features/switch_bindings.c:1 | New licensed test bindings export four wrapper symbols. Each calls its existing static inline public helper without changing behavior. |
| tests/features/environment.py:31 | Set ctypes signatures on the exported test bindings. Retain the names used by existing scenario hooks and steps. |
| tests/unit/main.c:1 | New licensed runner executes mrp_pdu_suite and releases the suite and reporter. It returns the suite result. |
| tests/unit/placeholder.c:1 at the base | Remove the zero-assertion placeholder. |

No files under src/ changed. The existing codec assertions and feature scenarios are unchanged.
The wrappers are only in the host shared-library target. They do not change protocol operations or the public inline API.
The regression guard uses the empty-suite message observed from cgreen 1.7.0.

## Before and after

| Check | Before count | Before rc | After count | After rc |
| --- | --- | --- | --- | --- |
| Configure and build | Successful after locating installed cgreen | 0 each | Successful | 0 each |
| CTest | 1/1 targets passed, empty unit suite | 0 | 1/1 targets passed, real codec suite | 0 |
| Native unit runner | 0 tests; 0 assertions | 0 | 9 tests; 1690 passing assertions | 0 |
| Behave | 0 features/scenarios/steps run; 1 feature, 3 scenarios, 10 steps untested | 1 | 1 feature, 3 scenarios, 10 steps passed; none failed or skipped | 0 |

The initial default dependency search did not locate the existing scratch cgreen installation. That preliminary CTest run found zero targets and still exited 0. The existing installation was copied into task scratch and the same unmodified base was configured and tested again. The main before row uses this dependency-complete baseline.

[CHECKS.txt](CHECKS.txt) contains the commands, individual return codes, and complete check output, including verbose CTest's 1690-assertion summary. Checks ran in foreground without pipelines. Each invocation had a 540-second subprocess deadline inside a 600-second foreground deadline.

The build and test commands shown in the unchanged README were run: cmake -B build -DCMAKE_BUILD_TYPE=Debug; cmake --build build; behave; ctest --test-dir build --output-on-failure. All four returned 0 after the fixes. Dependency installation commands were not needed: the existing cgreen installation and behave were used. No package was installed system-wide.

## Planted reversals

Each reversal was applied separately. Relevant native targets were rebuilt. Every edit was restored, and the final suites passed again.

| Reversal | Failing check | Observed rc | Observed failure |
| --- | --- | --- | --- |
| Remove tests/features/switch_bindings.c from host library sources | behave | 1 | Missing shlan_test_connect; 1 feature, 3 scenarios, 10 steps untested |
| Restore base tests/features/environment.py | behave | 1 | Missing shlan_connect; 1 feature, 3 scenarios, 10 steps untested |
| Restore placeholder.c and the original unit source list | ctest --test-dir build --output-on-failure | 8 | 0/1 targets passed; 0 tests; No assertions rejected |
| Replace mrp_pdu_suite() with create_test_suite() in the runner | ctest --test-dir build --output-on-failure | 8 | 0/1 targets passed; 0 tests; No assertions rejected |
| Change the expected packed byte from 215 to 214 in the existing codec test | ctest --test-dir build --output-on-failure | 8 | 0/1 targets passed; 9 tests; 1689 passes and 1 failure |

The fifth check confirms that a real failed codec assertion propagates to CTest's return code.
A separate fresh configure with library/include searches restricted to an empty scratch root returned 1 at the required cgreen lookup.
After restoration: configure/build rc 0, CTest 1/1 rc 0, behave 1 feature / 3 scenarios / 10 steps rc 0. Verbose CTest confirmed 9 tests and 1690 assertions.

## Artifacts and review

Public PR draft: [PR-BODY.md](PR-BODY.md).
Complete check evidence: [CHECKS.txt](CHECKS.txt).

Task scratch: $VALIDATION_STORAGE/lwsrptest-a562/.
The full command ledger, raw logs, copied cgreen installation, build directories, and reversal script remain there. They are not in the repository or output directory.
The repository's temporary build symlink was removed after testing. To repeat the README commands under the same storage restriction, first recreate build as a symlink to the retained scratch build directory. Its CMake cache already records the scratch dependency prefix. A fresh build needs that prefix supplied through CMAKE_PREFIX_PATH.

The commit subject is one line with no body or trailers. It uses neutral author and committer labels.
Only the five assigned harness files are changed. New source files have the required SPDX first line.
Final diff, metadata, cleanliness, public-text and artifact-size checks returned 0 and are recorded in the evidence.
The output directory contains only small text artifacts. No files over 200 KB, packages, toolchains, virtual environments, or rendered SVGs are included.
The manager is responsible for pushing the local branch and opening the PR.
