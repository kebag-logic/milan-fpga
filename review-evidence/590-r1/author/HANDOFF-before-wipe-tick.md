# [A385] Combined firmware lane handoff

Status: resumed under the public scope correction. The existing five-file draft is preserved. Commit the three issue changes, merge origin/dev with resolution only, apply the single authorized fixture-count correction, then complete measurements and gates. No REVIEW READY claim yet.

Scope correction: https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859930453

The sections below retain historical draft evidence until replaced by final-head results. The former builder blocker is authorized for the selection-count fixture only; all other builder edits remain excluded. The 870ff88a capture is historical only.

Branch: `590-592-599-firmware`.
Initial base: `8bc97021f28fb7f729418d3a00851c84ea0b50fd`.
Current committed head: `0d6f697ac` (service checks and integrated PHY host test).
Draft commits: #590 `4befe3f0d`, #592 `a133358f9`, #599 `f420e1a73`.
Merged remote dev `20aa4eabf` without conflicts. Initialized processor: `16be6768f710e79450aace277abacd6c2c3336e5`.
Fixture commit: `999a03255`, one assertion count changed from 2 to 4.
Compiler-present full builder bank: rc 0, one existing physical utilization-report calibration arm NOT RUN; every elaboration arm ran. Compiler-absent focused census: rc 0, one registered compiler-dependent instrument group NOT RUN. The full absent bank is underway. Firmware host self-test: rc 0 for five shapes, existing four NVM mutants and new PHY publisher mutant. Expanded service self-test: 36 oracle checks and 14 flash checks, rc 0. Staged C/C++ and Python idiom gates pass after splitting the PHY test's array initializers across lines.

New capture arms at the merged pin are underway; no completed arm yet. Partial 8x8 traffic-on observations are 13.22-13.23 ms; partial 1x1 traffic-on observations are about 3.88 ms. These are progress observations only. The service harness now runs MDIO through simulated pin CSRs, reads actual MAC_STATUS through the system bus, observes fabric link counters, and counts every unbacked system cycle after arming. Both queued plans contain at least 133 bytes. New controls include dispatch removal and publication removal. Target executions remain in progress; no timing conclusion is claimed.

An initial service build completed, but its exploratory run was terminated before duty measurement to finish the continuous-backing and fabric-readback observers. It supplies no final evidence. Current measurement builds use the completed observer. Authoritative documentation edits remain uncommitted pending the measurements.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859537529
Takeover: https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859548869
Reviewers: internal [R368], external [R369].
STOP report: https://github.com/kebag-logic/milan-fpga/issues/590#issuecomment-5859923842

## Historical STOP, resolved by the public correction

The original census stopped at the planted-conditional selection count. The manager authorized exactly that fixture correction. It is now committed as 2 to 4, without altering any substantive refusal or acceptance assertion. Both the compiler-present full builder bank and compiler-absent focused census have passed that point and completed successfully. The full compiler-absent bank is running.

The three preserved draft commits precede the resolution-only merge. No push, PR operation, hardware action, processor source edit, RTL edit, configuration edit or additional checkout has been performed. The sole builder change remains the authorized count. The following historical tables will be replaced with the completed measurements at the merged pin; they do not supersede the resume results above.

## Per-issue changes

All line numbers refer to the uncommitted working draft, not the base HEAD.

| Issue | Changes and file:line | State |
|---|---|---|
| #590 | `sw/firmware/milan_baremetal/milan_baremetal.c:473` ticks every 256 CRC bytes once NVM is ready; `:636` ticks every 16 validated records; `:1631`, `:1733`, `:1762`, `:1773`, `:1794` tick on entry to the five registered Milan command handlers | Implemented draft; queued schedule, dispatch-removal control and final duty measurements not run |
| #592 | `sw/firmware/milan_baremetal/milan_baremetal.c:447` defines the NVM word type; `:1166` retains closed-record bounds and uses aligned word interiors with byte edges; `tb/verilator/nvm_capture_cpu/firmware.py:92` and `run.py:111` add the byte-only control and maintain the missing-copy control | Five-shape host checks pass; 8x8 / 50 MHz / traffic-on capture arm passed 16 captures; timing control not run |
| #599 | `sw/firmware/milan_baremetal/milan_baremetal.c:773` sets a provisional 125 ms interval; `:790` drives Clause-22 reads; `:826` resolves mode; `:873` discovers the PHY and publishes status; `:917` services PHY work at heartbeat opportunities | Host test passes; target timing and simulation integration missing; bench acceptance 4 remains deferred |
| #599 tests | `sw/firmware/nvm_hosttest/phy_host.c:30` models MDIO pins, `:75` counts publication edges, `:100` exercises discovery/link/mode/error cases; `test_phy_firmware.py:11` compiles the firmware and kills the missing-publication mutant | New untracked tests; standalone run passes; not yet integrated into the existing host self-test |

## Tick placement and measured stretches

The existing 250 ms heartbeat rate limit is unchanged. The historical measurements below are the merged #397 findings at the starting HEAD, not measurements of this draft. They justify investigating the placements, but do not validate their spacing. Final target measurements remain required.

| Placement or duty | Prior 1x1 longest no-tick span (ms) | Prior 8x8 longest no-tick span (ms) | Draft measured span |
|---|---:|---:|---|
| Each command entry; queued schedule | 2569.49201 heartbeat gap | 2513.33593 heartbeat gap | Not measured; these two baseline values are schedule gaps, not individual duty spans |
| NVM status CRC and record validation | 220.48254 | 800.91654 | Not measured |
| NVM commit CRC and record validation | 137.09021 | 523.18408 | Not measured |
| Existing flash-wait tick, erase envelope | 20.14069 | 74.51875 | Not remeasured |
| Existing restore tick | 0.01111 | 0.01111 | Not remeasured |
| New MDIO work at tick entry | N/A | N/A | Not measured on target CPU |

The required continuously queued input of at least 133 bytes on both shapes is not yet demonstrated. The merged harness defaults to only three NVM status commands at 8x8; that plan needs an authorized test update and rerun. There is no committed dispatch-tick-removal control.

## MDIO poll-period derivation

The draft uses `(500 ms maximum heartbeat period - 250 ms rate-limit phase) / 2 = 125 ms`. That reserves half the available interval for scheduling delay and half for the duty plus PHY work. This is a provisional allocation, not a completed service-budget derivation: the final no-tick stretches, UART allowance and target MDIO execution time have not been measured. Do not treat the interval as accepted.

The host peer observed 59 completed 64-bit transfers and 241,664 requested delay cycles in its entire test. Each transfer requests `64 * 2 * 32 = 4096` delay cycles, which is 81.92 microseconds at 50 MHz or 40.96 microseconds at 100 MHz before instruction, CSR and bookkeeping overhead. These are arithmetic delay contributions, not target transaction durations. Discovery scans one address per opportunity. A resolved poll can perform several register reads; both one transaction and the complete poll need target measurements. The assignment's MDIO timing STOP condition has not been evaluated.

The host edge counter is a software observer of the publish accessor. It is not evidence of fabric LINK_DOWN/LINK_UP counters or MAC_STATUS wiring. Those simulation checks remain required.

## Capture measurements

The completed preliminary arm uses the unchanged processor pin `870ff88ad35bbd532244e4c7e6d7661b9f6e1366`, CPU 50 MHz and system 100 MHz. Firmware SHA-256: `c4ae162d591beb89c44cb1092a6b93134df99fc1d6997271cbe877ee181b574c`, 64,438 bytes. The required final receipt has not been replaced. The completed arm has a minimum of 13.21794 ms, a maximum of 13.23262 ms, zero destination mismatches, zero open-record copies and nonzero concurrent requests, responses and reads in every capture. See `capture-8x8-50-on.json`, `capture-8x8-50-on.log` and `capture-8x8-50-on-build.log`. This is one arm of an incomplete re-measure on an uncommitted draft.

| Shape | CPU MHz | Traffic | Captures | Maximum ms | 24.5 ms bar |
|---|---:|---|---|---|---|
| AX7101 1x1 | 50 | Off | Not run | N/A | Not evaluated |
| AX7101 1x1 | 50 | On | Not run | N/A | Not evaluated |
| AX7101 8x8 | 50 | Off | Not run | N/A | Not evaluated |
| AX7101 8x8 | 50 | On | 16/16, rc 0 | 13.23262 | Pass, 11.26738 ms below bar; preliminary draft |
| AX7101 8x8, labelled comparison | 100 | Off / On | Not run | N/A | Not evaluated |

Capture command, executed from `$LANES/590-592-599-firmware` in the foreground without network access:

```sh
rtk proxy timeout 14400 unshare -Urn env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=$WORKSPACE_HOME/br-milan-rv32/host/bin/riscv32-linux PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin $WORKSPACE_HOME/litex-milan/venv/bin/python -B tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic on --build-dir /tmp/a385-capture-8x8-50-on > /tmp/a385-capture-8x8-50-on.log 2>&1
```

## #397 harness table

| Plan or check | 1x1 | 8x8 | Meaning |
|---|---|---|---|
| Harness self-test | Shared: rc 0 | Shared: rc 0 | 30 grading checks and 14 flash checks; no target duty timing |
| `all` | Not run | Not run | All command/duty coverage remains required |
| `uart-paced` | Not run | Not run | UART allowance and no-tick spans remain required |
| `queued-input`, at least 133 bytes | Not run | Not run | Backing retention and dispatch control remain required |
| `device-wait`, 3 s erase / 5 ms page | Not run | Not run | Worst device-wait and commit timings remain required |
| MDIO integration | Not run | Not run | MAC_STATUS and fabric link counters remain required |

The findings refresh must distinguish the historical `ac18b509` 8x8 generated gPTP/lwSRP 100 MHz declaration from the current 50 MHz declaration. That documentation change is still pending.

## Mutants and controls

| Control | Required result | Observed |
|---|---|---|
| Dispatch tick removed | Queued-input check fails | Not implemented/run |
| Byte-only capture copy | Old timing restored | Injection added; not run |
| Missing capture copy | Poison/byte oracle rejects | Injection adapted for both stores; not run |
| Link publication removed | Link-cycle check fails | Host assertion `publishes == before + 1u` killed mutant, rc 0 driver |
| Four existing NVM host mutants | Each defect detected across the existing self-test | All four caught |
| Existing capture-receipt controls | Seven planted receipt/grading errors detected | All seven detected, but overall gate rc 1 for stale firmware digest |

## Gate table

These results are preliminary checks on the uncommitted working tree. None is final committed-head evidence. Commands ran from the physical workspace path with explicit timeouts and no gate output pipelines.

| Gate | Command | Result / evidence |
|---|---|---|
| Full builder bank, compiler present | Not run | Blocked by focused gate 1b failure |
| Full builder bank, compiler absent | Not run | Blocked by focused gate 1b failure |
| Focused firmware census, compiler present | `rtk proxy timeout 1800 $WORKSPACE_HOME/litex-milan/venv/bin/python -B -c 'import sys; sys.path.insert(0,"sw/builder"); import test_builder; test_builder.test_baremetal_profile_contract()'` | rc 1, fixed-count fixture at line 13304; `census-bounded.log` |
| Focused firmware gate, compiler absent | `rtk proxy timeout 1800 $WORKSPACE_HOME/litex-milan/venv/bin/python -B sw/builder/test_firmware_compiler.py --absent --audit /tmp/a385-census-absent.jsonl` | rc 1, same fixture; `census-absent.log` |
| Firmware host self-test, all five shapes including Arty | `python3 -B sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | rc 0; `host-pre2.log` |
| PHY host test and no-publish mutant | `python3 -B sw/firmware/nvm_hosttest/test_phy_firmware.py` | rc 0; `phy-host.log` |
| Preliminary capture, 8x8 / 50 MHz / traffic on | Foreground command above | rc 0; 16/16 captures; `capture-8x8-50-on.json` |
| Capture receipt | `python3 -B scripts/check_nvm_capture.py` | rc 1, expected stale firmware digest; `capture-receipt-pre.log` |
| Service-budget harness self-test | `python3 -B tb/verilator/fw_service_budget/run.py --self-test` | rc 0; `service-selftest.log` |
| Service-budget target runs | Not run | No final-head evidence |
| CI scope self-test | `python3 -B scripts/ci_scope.py --selftest` | rc 0; `ci-scope.log` |
| Documentation check | `python3 -B scripts/docs_check.py` | rc 0; `docs.log`; tracked files only, no authoritative updates made |
| C/C++ idiom | `python3 -B scripts/check_cpp_idiom.py` | rc 0; `cpp.log`; tracked-file census |
| Python idiom | `python3 -B scripts/check_py_idiom.py` | rc 0; `python.log`; tracked-file census |
| Diff whitespace | `git diff --check` | rc 0 at handoff finalization; new untracked files also checked for trailing whitespace |

Final worktree verification confirmed origin, branch, unchanged HEAD, an empty index, unchanged prohibited paths, the firmware digest, the exact saved draft patch and no root hex files. The short commands above identify each gate. Consult the retained logs and the capture command for the recorded environment. Additional documentation gates have not run. The new untracked test files are not covered by checks that enumerate `git ls-files`.

## Remaining work

1. Complete the full absent builder bank and the final committed-head repetitions. The scope correction and single fixture edit are complete.
2. Finish and measure #590 dispatch/walk placement, at least 133 queued bytes on both shapes, and a dispatch-removal control.
3. Measure complete MDIO transactions and polls on the target CPU; prove the service budget, fabricate no timing bound from host delays, and run the real MAC_STATUS/link-counter simulation.
4. Complete all capture arms after the final firmware change, run the byte-only timing control and updated poison control, and replace the digest-bound receipt. Stop if 8x8 exceeds 24.5 ms.
5. Rerun every #397 duty on both shapes; refresh the findings and authoritative firmware/register/compliance documents.
6. Complete every required gate at the eventual committed head. Clean generated root hex artifacts before any commit. Commit subjects must be one line without bodies or trailers.
7. Publish review-ready evidence only when those requirements are met. #599 bench acceptance 4 remains a later lane.

## Completed resumed capture arms

| Shape | CPU MHz | Traffic | Captures | Maximum ms | 24.5 ms margin | Result |
|---|---:|---|---:|---:|---:|---|
| AX7101 1x1 | 50 | On | 16 | 3.88702 | 20.61298 | rc 0, zero mismatches and open-record copies |
| AX7101 1x1 | 50 | Off | 16 | 3.84214 | 20.65786 | rc 0, zero mismatches and open-record copies |

Processor pin: `16be6768f710e79450aace277abacd6c2c3336e5`. Firmware digest remains `c4ae162d591beb89c44cb1092a6b93134df99fc1d6997271cbe877ee181b574c`. The four 8x8 arms and target controls are in progress. The receipt is not replaced until all six arms complete.
