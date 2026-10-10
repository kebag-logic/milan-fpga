# [A597] lwSRP issue #4 handoff: switch scenario steps assert their effect

Status: REVIEW READY at head `a8fe0849f37a0908bc899754c2644cf30a54b67f`.

- Repository: kebag-logic/lwSRP, branch `lwsrp4-steps` (local only; not pushed, no PR opened).
- Base: main `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`. Head: `a8fe0849f37a0908bc899754c2644cf30a54b67f`.
- Issue: #4, assignment comment 6100880112. TAKEN posted once as comment 6100886573. REVIEW READY posted once as comment 6101748797 ("[A597] REVIEW READY a8fe0849f37a0908bc899754c2644cf30a54b67f").
- Resume: the first session was stopped at 21:06 on 2026-10-10 by an external usage limit, not by a gate failure. At resume the working tree was clean and had no stray mutation plant. Its three commits were reviewed and kept. One commit was added. Every gate below was re-run at the final head; no earlier scratch log is cited.
- Scratch root for every receipt below: `$VALIDATION_STORAGE/lwsrp4-a597/final` (written `$F`). Receipts stay in scratch. Their sha256 prefixes and sizes are listed in "Receipts".

## Commits (one-line subjects, no body, no trailers, configured identity)

| Commit | Subject | Files |
| --- | --- | --- |
| `090252c` | Check every switch scenario step against the simulated port flags | `tests/features/environment.py`, `tests/features/steps/switch_steps.py` |
| `50e8189` | Plant miswired switch bindings that must fail named scenarios | `tests/check_reversals.py` |
| `95a1793` | Describe the state-checking switch steps, their planted faults and limits | `doc/manager.md`, `doc/tester.md` |
| `a8fe084` | Take the simulated port flag count from the adapter and stop on a layout change | `tests/features/environment.py`, `doc/tester.md` |

`git diff 08ee86e..a8fe084` is empty for `src/`, `zephyr/`, `Kconfig.zephyr`, `CMakeLists.txt`, `tests/unit/`, `tests/features/switch.feature` and `tests/features/switch_bindings.c`. No library code changed. No MRP semantics changed, and no scenario's intent changed (the feature file is byte-identical).

## How the effect is observed

The steps read the simulation adapter's own state, never a binding's result. `SimulatedPorts` (`tests/features/environment.py:35-71`) maps `struct shlan_switch.priv` (`src/include/shish_lan/switch.h:22-25`) onto the `int port_state[SIM_MAX_PORTS]` array of `struct sim_priv` (`src/modules/sim_adapter.c:6-10`; 1 = enabled, 0 = disabled). The flag meaning comes from the adapter: `sim_connect` clears every flag (`sim_adapter.c:12-17`), `sim_port_enable`/`sim_port_disable` set or clear one flag and return -1 at or beyond `SIM_MAX_PORTS` (`sim_adapter.c:24-36`), and `sim_disconnect` changes nothing (`sim_adapter.c:19-22`).

`_sim_port_count()` (`environment.py:15-24`, called at `environment.py:116`) reads `SIM_MAX_PORTS` from the adapter source. It stops with "struct sim_priv in sim_adapter.c no longer matches the port flag reader" if the struct no longer holds only that flag array. This replaced a hard-coded 48 (commit `a8fe084`). Scratch probes (`$F/layout-probes/`): an extra leading field and a `long` flag array each give behave rc 1 with that HOOK-ERROR (3 scenarios untested); a consistent `SIM_MAX_PORTS 64` still passes (rc 0, 3 scenarios).

No IEEE 802.1Q-2018 clause is cited. The steps drive only the lwSRP switch interface and its simulation, not MRP state, so no MRP behaviour is asserted.

## Steps and the effect each asserts

| Step (`switch.feature`) | Definition | Effect now asserted | Before (base) |
| --- | --- | --- | --- |
| `Given the switch is connected` (Background, all three scenarios) | `tests/features/steps/switch_steps.py:8-16` | Seeds every flag enabled (`:13`), calls connect, requires rc 0 (`:15`) and every one of the 48 flags disabled (`:16`). | No-op step; connect ran unchecked in the setup hook. |
| `Given port 0 is enabled` (Disable a port) | `switch_steps.py:46-51` via `_set_port` `:19-32` | The port exists (`:49`); enable returns 0 (`:26`); exactly that flag became enabled and no other flag changed (`:32`). | Called enable, result ignored. |
| `When port 0 is enabled` (Enable a port) | `switch_steps.py:54-56` via `_set_port` | rc 0 (`:26`); only port 0's flag changed, to enabled (`:32`). | Stored rc only. |
| `When port 255 is enabled` (Reject an out-of-range port) | same | rc nonzero for a port the simulation lacks (`:30`); no flag changed (`:32`). | Stored rc only. |
| `When port 0 is disabled` (Disable a port) | `switch_steps.py:59-62` via `_set_port` | rc 0 (`:26`); only port 0's flag changed, to disabled (`:32`). | Stored rc only. |
| `Then port 0 should be active` | `switch_steps.py:65-68` | Port 0's flag reads enabled (`:68`), read directly, not by a repeated call. | Re-called enable and checked rc 0. |
| `Then port 0 should be inactive` | `switch_steps.py:71-74` | Port 0's flag reads disabled (`:74`). | Re-called disable and checked rc 0. |
| `Then the operation should fail` | `switch_steps.py:77-80` | Last rc nonzero (`:79`); every flag equals its value before that operation (`:80`). | rc nonzero only. |
| Teardown: disconnect (every scenario) | `tests/features/environment.py:127-137` | Disconnect leaves every flag as it was (`:134`), then the adapter is destroyed. | Disconnect unchecked. |

Registration and declaration effects: no step in `tests/features/` drives an MRP registration or declaration, so there is none to assert. The behave suite has 1 feature, 3 scenarios and 10 steps, unchanged.

## Planted bindings

Seven plants live in `tests/check_reversals.py:196-210`. The required failing scenarios and assertion words are at `:213-224`, and the check is at `:385-392` (scenario names come from behave's "Failing scenarios" and "Errored scenarios" lists, `:306-316`). Each plant must give behave rc nonzero, fail exactly the named set, and print the words. Every plant compiled (build rc 0) before its scenario run.

| Plant | Family | Change (scratch copy) | Scenarios that fail | Assertion words |
| --- | --- | --- | --- | --- |
| `scenario-disable-dispatch` (issue item) | disable | `shlan_test_port_disable` calls `shlan_port_enable` | Disable a port | `after disabling port 0: port 0 enabled, expected disabled` |
| `scenario-disable-mapping` | disable | harness maps `shlan_port_disable` to `shlan_test_port_enable` | Disable a port | same |
| `scenario-disable-port` | disable | disable acts on `port_id + 1` | Disable a port | same |
| `scenario-enable-dispatch` | enable | `shlan_test_port_enable` calls `shlan_port_disable` | Enable a port; Disable a port | `after enabling port 0: port 0 disabled, expected enabled` |
| `scenario-connect-noop` (issue item) | connect | `shlan_test_connect` returns 0 without calling connect | Enable a port; Disable a port; Reject an out-of-range port | `after connecting: ports 0-47 enabled, expected disabled` |
| `scenario-connect-dispatch` | connect | `shlan_test_connect` calls disconnect | all three | same |
| `scenario-disconnect-dispatch` | disconnect | `shlan_test_disconnect` calls connect | Enable a port (teardown HOOK-ERROR, listed as errored) | `after disconnecting: port 0 disabled, expected enabled` |

Before the fix: the same seven plants were run against the base steps and setup hook (`environment.py` and `switch_steps.py` from `08ee86e`, everything else at head). All seven survived, each with behave rc 0 and 3 scenarios passing (`$F/logs/rev-scen-oldsteps.log`: "Reversals: 7; failures: 7").

## Base and head runs

Toolchain: CMake 4.4.4, gcc 16.2.1, cgreen 1.7.0 (built from its release archive into scratch), behave 1.3.3 under Python 3.14.7 and under CPython 3.12.3 (the hosted-CI interpreter).

| Run | Base `08ee86e` (old steps) | Head `a8fe084` |
| --- | --- | --- |
| Configure / build, `LWSRP_MILAN=OFF` | rc 0 / rc 0 | rc 0 / rc 0 |
| ctest / unit runner, OFF | rc 0 / rc 0, 102 tests, 26658 passes | rc 0 / rc 0, 102 tests, 26658 passes |
| Configure / build, `LWSRP_MILAN=ON` | rc 0 / rc 0 | rc 0 / rc 0 |
| ctest / unit runner, ON | rc 0 / rc 0, 102 tests, 26646 passes | rc 0 / rc 0, 102 tests, 26646 passes |
| behave, OFF library, Python 3.14.7 / 3.12.3 | rc 0 / rc 0; 1 feature, 3 scenarios, 10 steps passed | rc 0 / rc 0; 1 feature, 3 scenarios, 10 steps passed |
| behave, ON library, Python 3.14.7 / 3.12.3 | rc 0 / rc 0; same counts | rc 0 / rc 0; same counts |
| Reversal runner, OFF (`tests/check_reversals.py`) | not applicable (no scenario plants) | rc 0; 106 reversals, 106 KILLED, baseline and restored scenarios rc 0 |
| Reversal runner, ON | not applicable | rc 0; 106 reversals, 106 KILLED |
| Scenario plants only, CPython 3.12.3, OFF / ON | 7 survive (above) | rc 0 / rc 0; 7 KILLED each |
| `tests/check_embedded.py` | — | rc 0, both profile links and dispatch probes |
| `tests/check_freestanding.py`, default / `-DLWSRP_MILAN=1` | — | rc 0 / rc 0, 7 sources, 0 failures |
| `doc/tools/check_sentences.py` | — | rc 0; 1017 sentences, 0 over limit |
| `doc/tools/check_references.py` / `--self-test` | — | rc 0, 0 unlinked / rc 0, 79 cases |
| `doc/tools/check_links.py --github-auth` | — | rc 0; 374 local links, 21 external URLs, 0 failures |
| `doc/tools/render_mermaid.py` | — | rc 0; 28 graphs, 0 failures |

Disclosed rerun: a first attempt that ran both reversal profiles at the same time, on a host at load average about 127, gave rc 1 per profile. In each, one unrelated unit reversal hit ctest's fixed 10-second timeout (OFF: `received-withdrawal-value`; ON: `grouped-vector-order`; the log shows `***Timeout`, with `mrp_pdu_suite` taking 5883 ms instead of about 12 ms). All seven scenario plants were KILLED in both. Each profile was then re-run alone and gave rc 0 with 106/106 KILLED. These are the results in the table.

## Parent consumer

Scratch milan-fpga at dev `f88df731c77ec3d876b74e41b0091c513370afe9` with submodules initialised (`external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `2ad2f845`, `third_party/verilog-axis` `48ff7a7e`). `third_party/lwSRP` was fetched from the local branch and checked out at each revision; its toplevel was verified before every submodule git command. Final state: gitlink at `a8fe084`, working-tree modification only; nothing committed or pushed. Command: `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --build-dir <dir> --jobs 4` (local pinned RV32 SDK `riscv32-linux-gcc`, GoogleTest/GoogleMock 1.18.0, gcc 16.2.1).

The harness refuses any lwSRP other than its pin (`sw/firmware/ctrl/test/ctrl_arms.py:362`, `LWSRP_REV`). As in the previous lwSRP lane, the base and head runs used a scratch-only edit of that line, restored afterwards.

| Run | lwSRP | Harness | Arms ok | GoogleTest cases | SRP set (lwsrp + srp-*) | Result |
| --- | --- | --- | --- | --- | --- | --- |
| Gitlink at head, harness unmodified | `a8fe084` | pin `9197193e` | — | — | — | rc 2: `REFUSED: lwSRP at a8fe0849… is not the pinned 9197193e…` |
| Parent pin | `9197193e` | unmodified | 59/59 | 1191 | 35 arms, 291 cases | rc 0, PASS |
| Base | `08ee86e` | scratch `LWSRP_REV` = base | 59/59 | 1191 | 35 arms, 291 cases | rc 0, PASS |
| Head | `a8fe084` | scratch `LWSRP_REV` = head | 59/59 | 1191 | 35 arms, 291 cases | rc 0, PASS |

Per-arm verdicts (name, verdict, case count, failures, exit) are identical across pin, base and head. The RV32 `size` tables (230 rows) are identical between base and head, as expected, because `src/` is byte-identical. Pin to head differs only in `core_mrp_mad.o` text, 12709 → 13309 octets (+600) in each RV32 shape. That growth comes from the grouping work already on main between the pin and the base, not from this lane. The firmware SRP arms are unchanged by this lane.

## Limits

- Disconnection has no observable effect on the simulation (`sim_adapter.c:19-22`). A `shlan_test_disconnect` that skips the call is therefore equivalent on this adapter and passes (probe `disconnect-noop`, rc 0). The teardown check catches a disconnect that changes flags.
- The disable scenario enables only port 0. A disable binding that calls connect clears the same single flag and passes (probe `disable-reconnect`, rc 0). The scenario is not widened, because that would change its intent.
- Five more scratch probes were killed (`$F/logs/limit-probes.log`): enable no-op, disable no-op, enable of the next port, enable modulo 48 (fails "Reject an out-of-range port" with `enabling port 255 returned 0, but the simulated switch has no such port`), and a refusing enable or connect.
- The flag reader depends on the adapter's private layout; the source check above makes a layout change stop the run instead of reading the wrong memory. Scenarios run against the library that `SHLAN_LIBRARY` names; the layout is read from the checkout that holds `environment.py`.
- The reversal runner's interpreter now needs behave (`doc/tester.md`, Planted reversals). lwSRP has no hosted workflow. The parent's hosted jobs do not run lwSRP's behave or reversal runner.
- No hardware, bench, Zephyr SDK build or network interoperability was run. Nothing here is hardware proof.

## Receipts (scratch only; sha256 prefix, size in octets)

| File under `$F` | sha256 (first 16) | Size |
| --- | --- | --- |
| `logs/head-OFF-unit.log` | `9fc0edbf29d24ab2` | 428 |
| `logs/head-ON-unit.log` | `512fbff78127a5fd` | 427 |
| `logs/head-OFF-behave-py312.log` | `666474a7169d6f2b` | 1303 |
| `logs/base-OFF-unit.log` | `8db877bb19251137` | 426 |
| `logs/base-ON-unit.log` | `7ffcf72456bae7da` | 431 |
| `logs/base-OFF-behave-py314.log` | `5028e77862e79ead` | 1303 |
| `logs/rev-OFF.log` | `974fd8ea972b5963` | 9234 |
| `logs/rev-ON.log` | `974fd8ea972b5963` | 9234 |
| `logs/rev-scen-oldsteps.log` | `133557a9f83171bd` | 890 |
| `logs/rev-scen-py312-OFF.log` | `a51b58c4d41275b4` | 876 |
| `logs/limit-probes.log` | `60dfb580def4294d` | 2054 |
| `logs/fw-pin.log` | `34394e89ef724486` | 70081 |
| `logs/fw-base.log` | `0fb3e296b53238bd` | 70355 |
| `logs/fw-head.log` | `fe69be3616213be2` | 70355 |
| `logs/fw-head-unmodified.log` | `0f135ea2c91fb1a7` | 344 |
| `logs/doc-links.log` | `cc775acbc5b55e0c` | 1525 |
| `logs/doc-graphs.log` | `4a9151720b3a54a1` | 6219 |

## Acceptance

1. Each scenario step asserts the observable effect of its call on the simulated switch state: met (table "Steps and the effect each asserts").
2. Planted wrong-dispatch and no-op bindings each fail a named scenario: met for `port_disable` dispatching to enable ("Disable a port") and `connect` as a no-op (all three scenarios), plus one more wrong dispatch per step family. The disconnect no-op is equivalent on this simulation (Limits).

PR-BODY.md therefore says "Closes #4".
