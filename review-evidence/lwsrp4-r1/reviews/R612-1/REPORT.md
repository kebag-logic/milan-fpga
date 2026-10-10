[R612] POSITIVE - exact head a8fe0849f37a0908bc899754c2644cf30a54b67f

# R612-1 internal independent review: kebag-logic/lwSRP issue #4 / PR #19

- Head `a8fe0849f37a0908bc899754c2644cf30a54b67f`, tree `a015aa87e297b006542fa6c62b03af18cc0c6e52`, base main `08ee86e8`.
- Scope: tests and docs only (`tests/features/steps/switch_steps.py`, `tests/features/environment.py`, `tests/check_reversals.py`, `doc/tester.md`, `doc/manager.md`).
- Verdict: POSITIVE. No BLOCKER, MAJOR, MINOR or RESIDUE finding is open. Three SUGGESTIONs are recorded.
- Order of work: I read CONTRIBUTING.md (the repository has no AGENTS.md), README and doc/, the issue body and the manager's scope comment, the switch interface (`src/include/shish_lan/switch.h`), the simulation adapter (`src/modules/sim_adapter.c`) and the integrator contract. Then I read the diff `08ee86e8..a8fe0849` and its four commits, then the published evidence (milan-fpga `3b9dedba`, `review-evidence/lwsrp4-r1`). My verdict and ledger draft (`receipts/verdict-draft-before-prior-findings.md`) were written before I read any prior public review finding.

## Authorities

- Issue #4 frozen acceptance: (1) each scenario step asserts the observable effect of its call on the simulated switch state; (2) planted wrong-dispatch and no-op bindings each fail a named scenario.
- Manager scope comment on issue #4. Expected effects must come from the scenario's own words and the simulated switch state, never from the binding under test. Required plants: `port_disable` dispatching to enable, `connect` as a no-op, and one more wrong dispatch per step family. No change to library code, MRP semantics or scenario intent. Behave and unit tests must pass at head, and the base must pass under the old steps. The parent consumer's firmware SRP arms must be unchanged.
- Simulation contract: `doc/integrator.md:352-356` ("48 in-memory port flags", "Connection resets flags", "Range checks for port operations"). Implementation: `src/modules/sim_adapter.c:6-36` (connect clears all flags, enable/disable set or clear one flag and return -1 at or beyond 48, disconnect changes nothing).
- Origin findings: R536-1-02 (SUGGESTION, PR #3) and R537-1's retention of it.

## Lens results

### Conformance (acceptance 1 and 2, scope)

Each step was checked against the scenario words (`tests/features/switch.feature`, byte-identical to base) and the simulation contract:

| Step | Head assertion | Source of the expected effect |
| --- | --- | --- |
| `Given the switch is connected` (`switch_steps.py:8-16`) | Seeds all flags enabled, then requires connect rc 0 and all 48 flags disabled. | "Connection resets flags" (`integrator.md:354`, `sim_adapter.c:12-17`). The binding is not consulted. |
| `Given port 0 is enabled` (`:46-51`) | The port exists; enable rc 0; only port 0 changes, to enabled. | Scenario words plus the simulation's flag. |
| `When port N is enabled` / `disabled` (`:19-32`, `:54-62`) | In range: rc 0 and only port N changes. Out of range: rc nonzero and no flag changes. | Scenario words; the range comes from `SIM_MAX_PORTS` in the adapter source (`environment.py:15-24`), not from a binding. |
| `Then port N should be active` / `inactive` (`:65-74`) | Reads the flag directly. No operation is repeated. | The simulation's flag. |
| `Then the operation should fail` (`:77-80`) | Last rc nonzero and every flag unchanged. | Scenario words. |
| Teardown (`environment.py:127-137`) | Disconnect leaves every flag unchanged. | `sim_adapter.c:19-22`. |

- The flags are read through `struct shlan_switch.priv` into `struct sim_priv`, with ctypes (`environment.py:10-12`, `:42-44`). No binding is called to observe state.
- The flag count comes from the adapter source. If `struct sim_priv` changes shape, the run stops: probe `layout-extra-field` gives rc 1 with `HOOK-ERROR in before_all: AssertionError: struct sim_priv in sim_adapter.c no longer matches the port flag reader`, and all 3 scenarios are untested. A consistent `SIM_MAX_PORTS 64` still passes.
- No MRP registration or declaration step exists in `tests/features/`, so no MRP semantics are involved.
- `git diff 08ee86e8 a8fe0849` is empty for `src`, `zephyr`, `Kconfig.zephyr`, `CMakeLists.txt`, `tests/unit`, `switch.feature`, `switch_bindings.c`, `build.sh` and `behave.ini`. The `src` tree is `43e91d8e` at both base and head (`receipts/parent-consumer.log`).
- Acceptance 2 is met. The runner's seven plants cover:
  - disable: dispatch to enable, harness mapping and next port;
  - enable: dispatch to disable;
  - connect: no-op and dispatch to disconnect;
  - disconnect: dispatch to connect.

  Each plant must fail exactly its named scenarios with its assertion words (`check_reversals.py:196-226`, `:392`).
- Clean.

### RTL (C library and parent consumer)

- No HDL or C library source changed. The `src/` tree hash is identical at base and head.
- The parent harness consumes only lwSRP `src` (`ctrl_arms.py:354` `LWSRP_SOURCES`, `:364` `LWSRP_TREE = "src"` at milan-fpga dev `f88df731c77ec3d876b74e41b0091c513370afe9`).
- A scratch parent index with the `third_party/lwSRP` gitlink set to `a8fe0849` differs from dev only in that gitlink.
- Host objects of the four parent-consumed sources are byte-identical at base and head (sha256 in `receipts/parent-consumer.log`).
- The parent's `bdd-conformance` behave job runs the parent's own `tests/`, not lwSRP's.
- Clean. I did not run the RV32 firmware arms (see Limits).

### Robustness

- Independently spelled plants on head (`scripts/probe.py`, `receipts/probes-head/`). All 16 outcomes matched my prediction, and every plant built (build rc 0):

| Plant | Head behave | Failing / errored scenarios and words |
| --- | --- | --- |
| disable binding calls `sw->ops->port_enable` | rc 1 | Disable a port: `after disabling port 0: port 0 enabled, expected disabled` |
| disable binding no-op returning 0 | rc 1 | Disable a port: same words |
| connect binding returns 0 without connecting | rc 1 | all three: `after connecting: ports 0-47 enabled, expected disabled` |
| connect binding clears only port 0 | rc 1 | all three: `after connecting: ports 1-47 enabled, expected disabled` |
| connect connects but returns 1 | rc 1 | all three: `connecting returned 1, expected 0` |
| enable binding modulo 48 | rc 1 | Reject an out-of-range port: `enabling port 255 returned 0, but the simulated switch has no such port` |
| enable binding accepts out-of-range with rc 0 | rc 1 | Reject an out-of-range port: same words |
| enable also enables the next port | rc 1 | all three: `after enabling port 0: port 1 enabled, expected disabled` |
| harness maps enable to the disable binding | rc 1 | Enable a port, Disable a port: `after enabling port 0: port 0 disabled, expected enabled` |
| disconnect enables port 5 | rc 1 | all three hook errors: `after disconnecting: port 5 enabled, expected disabled` |
| struct sim_priv gains a leading field | rc 1 | before_all named stop, 3 untested |
| struct shlan_switch members swapped | rc -11 | crash, no false pass (R612-1-02) |
| disable ignores its port (always port 0) | rc 0 | survives (R612-1-01) |
| disable binding reconnects | rc 0 | survives; documented limit (`tester.md:195`) |
| disconnect binding no-op | rc 0 | survives; documented limit (`tester.md:193-194`) |
| `SIM_MAX_PORTS 64`, consistent | rc 0 | passes, as intended |

- The same 16 plants run against the base steps and setup hook (`receipts/probes-oldsteps/`). Every binding fault survives with rc 0, except the two out-of-range enable plants: the base reject step catches those (`expected failure but operation succeeded`). The two layout probes also survive at base, because base reads no adapter memory.
- Clean.

### Tests

- Default profile, head (`receipts/head-default.log`): configure, build and ctest rc 0. Unit runner `Completed "main": 26658 passes`. Behave rc 0: 1 feature, 3 scenarios, 10 steps passed.
- Milan profile, head (`receipts/head-milan.log`): the same, with 26646 passes and behave rc 0.
- Base `08ee86e8` with the old steps, both profiles (`receipts/base-*.log`): all rc 0 with the same counts.
- Behave under CPython 3.12.13 at head, both libraries: rc 0 (`receipts/behave-py312-head.log`). The three changed Python files also compile under 3.12 (`receipts/static-checks.log`).
- Reversal runner at head (`receipts/reversals-default.log`, `receipts/reversals-milan.log`):
  - rc 0 in both profiles, with 106 of 106 KILLED;
  - the baseline and restored scenario runs gave rc 0;
  - the two profiles ran concurrently with no timeout.

  Raw logs for the seven scenario plants are in `receipts/runner-scenario-logs/`.
- The runner's own seven scenario plants (`receipts/scenario-plants-*.log`):
  - against the base steps: all 7 SURVIVED ("Reversals: 7; failures: 7");
  - at head: all 7 KILLED.
- The runner's kill criterion is strict: rc nonzero, the exact failing or errored scenario set, and the assertion words.
- Clean.

### Docs

- `doc/tester.md:30`, `:160-165`, `:183`, `:193-195` and `:227-231`, and `doc/manager.md:58-62`, match the code and my measurements:
  - 3 scenarios and 10 steps;
  - 106 reversals in both profiles;
  - seven scenario plants;
  - the runner's interpreter needs behave;
  - the documented survivors.
- The stale "only repeat the operation" statements were removed everywhere.
- Checks at head:
  - sentences rc 0 (1017 fragments, 0 over limit);
  - references rc 0 (0 unlinked) and self-test rc 0 (79 cases);
  - links rc 0 (374 local links, 21 external URLs, 0 failures).
- The diff changes no Mermaid graph.
- The privacy scan of added lines, the PR body and the commit messages found no host, instrument, path or personal names (`receipts/static-checks.log`).
- All four commits have one-line subjects with no body or trailer.
- The PR body matches the published `PR-BODY.md` (sha256 `863ebe56…`), apart from a trailing newline.
- Clean.

## Findings

| ID | Severity | Lenses | Location | Evidence | Impact | Required outcome | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R612-1-01 | SUGGESTION | Tests, Docs | `doc/tester.md:193-195`; `tests/features/switch.feature:11-14` | Probe `disable-ignores-port`: `shlan_test_port_disable` acting on port 0 whatever its argument gives behave rc 0 (`receipts/probes-head/disable-ignores-port.behave.log`). | It is equivalent to the documented reconnect survivor, because only port 0 is ever disabled. The "Two enabled ports" next case already covers it. | Optional: name this survivor next to the reconnect sentence, or cover it when a two-port scenario is added. | Re-run the probe and expect it to be listed or killed. |
| R612-1-02 | SUGGESTION | Robustness | `tests/features/environment.py:10-12`, `:43-44` | Probe `layout-switch-swapped`: with `struct shlan_switch` members reordered in `switch.h`, behave dies with SIGSEGV (rc -11, no summary). The named layout stop covers only `struct sim_priv`. | No false pass. A public-struct change gives a crash rather than a named error. | Optional: check the `struct shlan_switch` member order the same way as `struct sim_priv`. | Re-run the probe and expect a named before_all stop. |
| R612-1-03 | SUGGESTION | Tests | `tests/check_reversals.py:196-226` | No runner plant fails only "Reject an out-of-range port". Probes `enable-accepts-out-of-range` and `enable-modulo-range` fail only that scenario, with `enabling port 255 returned 0, but the simulated switch has no such port`. | The out-of-range path is pinned only by my probes, not by the repository runner. | Optional: add one range plant to `CASES` and `SCENARIO_FAILURES`. | The runner reports it KILLED with that scenario set. |

## Prior public review findings at this head

- PR #19 has no prior review finding. Its only conversation comments are the two review-start notices. It has 0 reviews and 0 inline comments.
- R536-1-02 (PR #3, SUGGESTION, retained by R537-1) is RESOLVED at this head. Its x3 mutation (disable calls enable) and x5 mutation (connect no-op) now give behave rc 1, both in the runner and in my independently spelled probes. Disconnect is now observed for flag changes. Its no-op form is a documented equivalence on this simulation (`tester.md:193-194`).

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Issue #4 body and scope comment; `switch.feature`; `switch.h`; `sim_adapter.c`; `integrator.md:352-356`; step-by-step mapping; scope diff | R612-1 | a8fe0849f37a0908bc899754c2644cf30a54b67f |
| RTL | CLEAN | `src` tree identity; parent `ctrl_arms.py` consumed paths; scratch gitlink; host object identity of the 4 consumed sources | R612-1 | a8fe0849f37a0908bc899754c2644cf30a54b67f |
| Robustness | CLEAN | 16 independent plants at head and under the old steps; layout probes; hook and teardown error paths | R612-1 | a8fe0849f37a0908bc899754c2644cf30a54b67f |
| Tests | CLEAN | Head and base builds, ctest, unit runner and behave in both profiles; CPython 3.12 behave; reversal runner in both profiles (106/106); runner plants against the old steps (7/7 survive) | R612-1 | a8fe0849f37a0908bc899754c2644cf30a54b67f |
| Docs | CLEAN | `doc/tester.md` and `doc/manager.md` diffs against the measurements; sentence, reference and link checks; privacy scan; commit format; PR body | R612-1 | a8fe0849f37a0908bc899754c2644cf30a54b67f |

## Clone integrity

After the probes:
- HEAD is `a8fe0849`, and both the index write-tree and the HEAD tree are `a015aa87`.
- `git status --ignored` is empty.
- All 65 tracked files match their HEAD blob bytes and modes.
- fsck rc is 0.
- The repository has no submodule gitlinks (`receipts/clone-integrity.log`).

All plants ran in scratch copies, and the clone was never edited.

## Limits

- Toolchain: cgreen 1.6.4 built from source in scratch, CMake 4.4.4, GCC 16.2.1, and behave 1.3.3 under CPython 3.14.7 and 3.12.13.
- The unit counts are cgreen pass counts; I did not count tests separately. The suite script's "unit rc" line is the rc of a `tail` pipe. The ctest rc is the authoritative unit result.
- Parent consumer: the check is static, plus host-object identity. I did not run the RV32 firmware arms, because the full parent bank is out of scope. At head the parent harness refuses any lwSRP other than its pin `9197193e`; that is the author's published evidence, which I did not re-execute.
- lwSRP has no hosted workflow. No check run or status exists at this head, so there is no hosted evidence to separate into executed and skipped jobs.
- The published author receipts are summaries: their raw logs stay in the author's scratch. I independently re-executed every claim in scope except the firmware arms.
- No hardware was used. Physical calibration was NOT RUN. Nothing here is hardware proof.
- Publishable receipts had local absolute paths replaced with `$PACKET`, `$CLONE`, `$STORAGE` and `$HOME` after execution.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `08ee86e8`, live dev `f88df731c77ec3d876b74e41b0091c513370afe9`), including the builder and native banks, and link the receipts on the PR.
- Own hosted and act acceptance.
- Decide on moving the parent pin `LWSRP_REV`, which this lane does not change.
- Carry R612-1-01 to R612-1-03 as optional suggestions. There is no RESIDUE item.
- Merge requires a second independent positive review.

R612-1 FINISHED
