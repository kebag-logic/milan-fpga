# Issue 397 author handoff

Author: [A358]. Independent reviewers: [R348] (internal), [R349] (external).
Branch: `397-service-budget`. Local head: `7f997b60d5a74d46beca5c263d27496ccce0ae4f`.
Parent: `ac18b50968b12efe4d15c0a06301264b35656b31`.
Worktree: `$LANES/397-service-budget`.
Origin was verified as `https://github.com/kebag-logic/milan-fpga.git`.

The measurement-only deliverable is ready for independent review. The 8x8
scenario exposes two NVM-status service-window overruns and a maximum
heartbeat gap of 1,449.77764 ms against 500 ms. Measurement validity passes;
these timing findings remain open. Refs #397; the architecture decision and
bench items remain open. The commit is local and has not been pushed.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/397#issuecomment-5854787465
Takeover: https://github.com/kebag-logic/milan-fpga/issues/397#issuecomment-5854812698
The final public payload is `REVIEW-READY.md`; `PR-BODY.md` is prepared only.
No review verdict, PR action, merge, hardware run, or hart-count decision is
claimed. No requested duty lacked an external or enclosing marker, so the
assignment's STOP condition was not reached.

## Change list

All paths below are relative to the physical worktree.

| File:line | Change |
| --- | --- |
| `tb/verilator/fw_service_budget/build.py:18` | Read-only capture-SoC reuse, unchanged firmware linkage, passive Wishbone/backend observation, independent device boundary |
| `tb/verilator/fw_service_budget/sim_main.cpp:17` | Device/UART driver and external event capture; explicit 50 MHz CPU clock at line 166 |
| `tb/verilator/fw_service_budget/flash.hpp:12` | Journal-only flash model with WEL, WIP, page and address enforcement |
| `tb/verilator/fw_service_budget/flash_test.cpp:35` | Fourteen independent device controls |
| `tb/verilator/fw_service_budget/run.py:145` | Marker/operation census, measured intervals, deadlines, all budget refusals; real-trace controls at line 216 |
| `tb/verilator/fw_service_budget/Makefile:1` | Portable default self-test entry point |
| `tb/verilator/fw_service_budget/README.md:9` | Build/run recipe and measurement contract |
| `docs/findings/397_SERVICE_BUDGET.md:49` | Two per-duty tables, device projections at line 126, limitations and reproduction |
| `docs/findings/397_SERVICE_BUDGET_1X1.json:1` | Complete 1x1 raw log, integer counters, analysis and hashes |
| `docs/findings/397_SERVICE_BUDGET_8X8.json:1` | Complete 8x8 raw log, integer counters, analysis and hashes |
| `docs/findings/README.md:11` | Current findings index entry |
| `docs/testing/TESTING.md:403` | Portable controls versus explicit full simulation |

Firmware, RTL, submodules, FR/NFR and `tb/verilator/nvm_capture_cpu` are unchanged.
The commit subject is one line, with no body or trailers.

## Results

CPU cycles are elapsed clock units rounded upward from the integer 100 MHz
system counter, not retired instructions. Milliseconds retain the unrounded
system interval. These are maxima over one populated-media cold boot and 17
command cases per shape, with fixed clock phase and no external packet traffic.
The 500 ms ordinary-command comparison is a service-window budget, not a UART
protocol response deadline. Boot/AEM have no supported numeric boot deadline;
ADP valid time does not define one. Wipe uses two individual erase limits, not
an invented whole-command timer.

**1x1: populated A/B slots, 0 ms WIP per erase/page.**

| Duty | Elapsed CPU cycles | Elapsed ms | Budget ms | Margin ms |
| --- | ---: | ---: | ---: | ---: |
| Boot to entity enabled | 15,548,512 | 310.97023 | N/A | N/A |
| AEM copy/CRC, enclosed by boot | 15,548,512 | 310.97023 | N/A | N/A |
| Binding restore walk | 1,138 | 0.02276 | 3,000 | 2999.97724 |
| Journal erase envelope | 1,006,829 | 20.13657 | 3,500 | 3479.86343 |
| Journal START-to-ACK | 7,826,455 | 156.52910 | 8,000 | 7843.47090 |
| Maximum heartbeat gap | 21,531,153 | 430.62305 | 500 | 69.37695 |
| `milan_status` | 388,880 | 7.77759 | 500 | 492.22241 |
| `milan_gettime` | 115,696 | 2.31391 | 500 | 497.68609 |
| `milan_settime`, maximum tested case | 258,615 | 5.17229 | 500 | 494.82771 |
| `milan_utc`, maximum tested case | 298,502 | 5.97003 | 500 | 494.02997 |
| `milan_nvm` status | 10,425,165 | 208.50329 | 500 | 291.49671 |
| `milan_nvm commit` | 13,738,559 | 274.77117 | 8,000 | 7725.22883 |
| `milan_nvm wipe`, whole command | 2,017,180 | 40.34359 | N/A | N/A |
| Wipe erase envelope, maximum of two | 1,005,511 | 20.11022 | 3,500 | 3479.88978 |
| `milan_nvm invalid` | 98,289 | 1.96577 | 500 | 498.03423 |

**8x8: populated A/B slots, 1 ms WIP per erase/page.**

| Duty | Elapsed CPU cycles | Elapsed ms | Budget ms | Margin ms |
| --- | ---: | ---: | ---: | ---: |
| Boot to entity enabled | 51,571,981 | 1031.43961 | N/A | N/A |
| AEM copy/CRC, enclosed by boot | 51,571,981 | 1031.43961 | N/A | N/A |
| Binding restore walk | 2,700 | 0.05400 | 3,000 | 2999.94600 |
| Journal erase envelope | 3,775,572 | 75.51143 | 3,500 | 3424.48857 |
| Journal START-to-ACK | 32,909,891 | 658.19782 | 8,000 | 7341.80218 |
| Maximum heartbeat gap | 72,488,882 | 1449.77764 | 500 | -949.77764 |
| `milan_status` | 388,880 | 7.77759 | 500 | 492.22241 |
| `milan_gettime` | 116,268 | 2.32535 | 500 | 497.67465 |
| `milan_settime`, maximum tested case | 258,615 | 5.17229 | 500 | 494.82771 |
| `milan_utc`, maximum tested case | 298,502 | 5.97003 | 500 | 494.02997 |
| `milan_nvm` status | 39,443,853 | 788.87705 | 500 | -288.87705 |
| `milan_nvm commit` | 55,457,868 | 1109.15735 | 8,000 | 6890.84265 |
| `milan_nvm wipe`, whole command | 7,554,712 | 151.09423 | N/A | N/A |
| Wipe erase envelope, maximum of two | 3,774,257 | 75.48514 | 3,500 | 3424.51486 |
| `milan_nvm invalid` | 98,289 | 1.96577 | 500 | 498.03423 |


Each scenario completed all 17 commands, two acknowledged commits and four
erases. The 1x1 run completed 26 page programs / 6,528 bytes at system cycle
137,348,992. The 8x8 run completed 100 page programs / 25,360 bytes at cycle
503,436,696. Restore envelopes contain 8 and 32 matching backend read/response
handshakes, with zero errors. All five product command registrations are
covered. The 1x1 final trace has no budget finding; the 8x8 trace has three.

## Device waits and limits

| Shape / operation | Measured service (ms) | Modeled WIP (ms) | Device maxima (ms) | Conditional total (ms) |
| --- | ---: | ---: | ---: | ---: |
| 1x1 journal START-to-ACK | 156.52910 | 0 | 3,065 | 3221.52910 |
| 1x1 whole console commit | 274.77117 | 0 | 3,065 | 3339.77117 |
| 1x1 journal erase envelope | 20.13657 | 0 | 3,000 | 3020.13657 |
| 1x1 whole wipe | 40.34359 | 0 | 6,000 | 6040.34359 |
| 8x8 journal START-to-ACK | 607.19782 | 51 | 3,250 | 3857.19782 |
| 8x8 whole console commit | 1058.15735 | 51 | 3,250 | 4308.15735 |
| 8x8 journal erase envelope | 74.51143 | 1 | 3,000 | 3074.51143 |
| 8x8 whole wipe | 149.09423 | 2 | 6,000 | 6149.09423 |


These projections add the saved-state section 9.4 device maxima to measured
non-WIP service. They are conditional, not measured worst-device runs or a
proof of the required twofold commit margin. Additional poll iterations and
arbitrary bus contention are not bounded here. The CPU still polls during
WIP; subtracting WIP does not measure idle CPU capacity. The 8x8 maximum
heartbeat interval includes 51.00020 ms of overlapping modeled WIP, retained
separately in its receipt without changing the elapsed deadline comparison.

The physical flash PHY is replaced at its stream boundary, DDR uses the
existing model, UART has immediate byte handshakes, and BIOS CRC/delay/memory
tests retain the capture recipe's exclusions. No physical boot-time claim is
made. The maximum UART 115,200-baud 8N1 serialization allowance is 33.07292 ms;
all per-command byte counts remain in the receipts. Restore covers the current
binding walk, not the seven remaining saved-state items. Page programming is
inside the measured journal bracket; its isolated 50 ms poll-loop margin is
not established. Clock-setting commands change the firmware PHC; measurement
cycles remain monotonic. Heartbeat observation ends at the final command.

The update writer, fault log, PHY management, temperature log, remaining
persistence features, architecture decision and AX7101 liveness torture remain
open. The normative one-hart rule is unchanged. The 8x8 misses need manager and
reviewer disposition; they were neither fixed nor hidden in this lane.

## Gate table

Every command ran in the foreground from the physical worktree above, without
pipelines. The table gives the executed program and arguments; execution
wrappers supplied a 1,200-second limit for short gates and a 7,200-second limit
for builds/simulation, with logs redirected under `/tmp`. All final results
below are rc 0. The final source and saved-log identities were rechecked after
analysis changes; no simulated product or native driver changed between the
completed run and the final analysis.

| Program and arguments | Final result | rc |
| --- | --- | ---: |
| `python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/397-a358-1x1 --reuse-build --populated` | 17 commands, two acknowledged commits, valid measurement | 0 |
| `python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/397-a358-8x8 --reuse-build --populated --device-wait-us 1000 --record-budget-findings` | 17 commands, two acknowledged commits; budget refusals retained | 0 |
| `python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/397-a358-1x1 --populated --regrade` | Bound-log final analysis, zero budget findings | 0 |
| `python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/397-a358-8x8 --populated --device-wait-us 1000 --regrade --record-budget-findings` | Bound-log final analysis, three named budget findings | 0 |
| `python3 -B tb/verilator/fw_service_budget/run.py --self-test` | 14 device + 8 oracle controls, zero failures; planted interval and delayed real UART trace caught | 0 |
| `python3 -B scripts/check_nvm_capture.py` | Existing receipt and seven controls pass; pinned harness unchanged | 0 |
| `python3 -B scripts/check_feature_status.py --self-test` | 46/46 controls, zero findings | 0 |
| `python3 -B scripts/docs_check.py` | Zero findings; scrub 23/23, routing 4/4 | 0 |
| `python3 -B scripts/check_doc_paths.py` | 848 cited paths resolve | 0 |
| `python3 -B scripts/check_doc_style.py` | 22 current documents pass | 0 |
| `python3 -B scripts/check_archive.py` | 21 indexed historical pages pass | 0 |
| `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python -B scripts/gen_toc.py --check` | 112 annotated contents lists; 18 below threshold | 0 |
| `$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31` | Exact committed head: zero findings, 339/339 controls | 0 |
| `python3 -B scripts/check_py_idiom.py` | 264 modules; all ratchets pass | 0 |
| `python3 -B scripts/check_cpp_idiom.py` | 159 translation units; all checks zero | 0 |
| `python3 -B scripts/check_hygiene.py --check` | 794 files, three populations pass | 0 |
| `python3 -B scripts/measure_test_evidence.py --check` | Existing ratchets pass; no threshold changed | 0 |
| `git diff HEAD --check` (before commit), `git diff --check` (after commit) | No whitespace errors; final worktree clean | 0 |

The default invocation rejects timing overruns after preserving their receipt.
The explicit measurement-only reporting option prints and retains every
refusal, while still failing malformed markers, failed commands, stale builds
or bad device sequences. Its rc 0 certifies measurement integrity, not timing
approval. The control suite proves that a named over-budget command survives
the reporting path. The portable default target does not claim a fresh full
simulation; the test-evidence inventory's limited static detector lists this
suite among those without a recognized mutation entry. No unrelated ratchet
was lowered to change that classification.

## Reproduction and artifact identities

The sibling README gives the portable recipe. The completed builds are under
`/tmp/397-a358-1x1` and `/tmp/397-a358-8x8`, outside the output directory. Build
commands used the existing integration environment and offline cached CPU:

```sh
env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=riscv32-linux PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin timeout 7200 unshare -Urn $WORKSPACE_HOME/litex-milan/venv/bin/python -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/397-a358-1x1 --build-only
env PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=riscv32-linux PATH=$WORKSPACE_HOME/litex-milan/venv/bin:/usr/bin:/bin:$WORKSPACE_HOME/br-milan-rv32/host/bin timeout 7200 unshare -Urn $WORKSPACE_HOME/litex-milan/venv/bin/python -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/397-a358-8x8 --build-only
```

The firmware source digest is
`0bf43cd4fe02b110fb1ae4f051b3bc7baa6bb62c3769962520ed1f4bd12247a6`.
The generated CPU digest is
`c208df0b7fafcaab190dba3f1734f2a38acd54645b33a834b0e59282e6a7813d`,
matching the pinned capture receipt. Existing dependency patches were retained,
not edited. Receipts include dependency revisions, generated SoC/BIOS/native
binary hashes, product/measurement inputs, raw UART/event text and its digest.
Both committed receipts were independently recomputed through `grade()` and
checked against current `inputs()` and the raw-log SHA-256.

Initial build attempts exposed an incorrect observer-interface assumption and
executable search-order problems; corrected builds passed. An exploratory
8x8 run was stopped before completion when final UART-byte instrumentation was
added; it is not evidence. A preliminary blank 1x1 run is likewise excluded
from the final tables. One C++-gate invocation used an unsupported option;
the documented default invocation passed. Final gates above all returned zero.
A shared repository commit-graph warning did not affect commands or results.

No build tree, dependency copy, installation, tree export or large log was
written into the output directory. The handoff artifacts are each below 200 KB.
