[R613] POSITIVE - exact head a8fe0849f37a0908bc899754c2644cf30a54b67f

# R613-1 external independent review: kebag-logic/lwSRP PR #19 (issue #4)

- Exact head: `a8fe0849f37a0908bc899754c2644cf30a54b67f`, tree `a015aa87e297b006542fa6c62b03af18cc0c6e52` (verified in the detached review clone).
- Source base: main `08ee86e812a0eb5e1dc6cd61b494d8baf3491348`. Diff: 5 files, +202/-28 (`tests/features/environment.py`, `tests/features/steps/switch_steps.py`, `tests/check_reversals.py`, `doc/tester.md`, `doc/manager.md`).
- Review start: https://github.com/kebag-logic/lwSRP/pull/19#issuecomment-6101765027.
- Verdict: POSITIVE. No open BLOCKER, MAJOR or MINOR finding. One RESIDUE (prose wording only) and three SUGGESTIONs are recorded below.

## Reconstruction

1. lwSRP has no `AGENTS.md`. `CONTRIBUTING.md` sets the rules used here: one-line commit subjects without bodies or trailers, 25-word sentences, linked references, recorded exit codes, and no private infrastructure details.
2. `README.md` and `doc/tester.md` / `doc/manager.md` describe the scenario suite (3 scenarios, 10 steps) and the reversal runner.
3. Issue #4 is the frozen scope. Its body gives acceptance 1 (each scenario step asserts the observable effect of its call on the simulated switch state) and acceptance 2 (planted wrong-dispatch and no-op bindings each fail a named scenario). The maintainer assignment comment adds three things. Expected effects come from the scenario's words and the simulated switch state, never from the binding under test. Library code, MRP semantics and scenario intent do not change. A parent consumer check runs at milan-fpga dev `f88df731`. The author posted TAKEN and REVIEW READY at this head. No later scope change was posted.
4. Interface authorities: `src/include/shish_lan/switch.h:15-31` (`struct shlan_switch_ops`, `struct shlan_switch`, the out-of-line entry points), `src/modules/sim_adapter.c:6-60` (`SIM_MAX_PORTS`, `struct sim_priv`, the connect/enable/disable/disconnect semantics), `tests/features/switch_bindings.c` (the bindings under test), `tests/features/switch.feature` (scenario words). No IEEE 802.1Q clause is in scope: the steps drive only the switch interface and its simulation.
5. History: four one-line commits with no body or trailers (`090252c`, `50e8189`, `95a1793`, `a8fe084`).
6. Public evidence: the milan-fpga archive at `3b9dedba…/review-evidence/lwsrp4-r1` holds `MANIFEST.json`, `author/HANDOFF.md` and `author/PR-BODY.md`. The published PR-BODY.md hash `863ebe56…` matches its manifest entry. When this pass started, the manager had posted only the two review-start comments on the PR and no evidence comments. lwSRP has no hosted workflow: the head has 0 check runs and a combined status of `pending` with 0 contexts. No hosted job ran at this head.

## Independent execution at the exact head (reviewer-owned, all in scratch)

Toolchain: CMake 4.4.4, GCC 16.2.1, cgreen 1.7.0 (built from its upstream tag into scratch), behave 1.3.3 on Python 3.14.7, and behave 1.2.6 on CPython 3.12.3 in a scratch venv (`receipts/toolchain.txt`).

| Check | Base `08ee86e` (old steps) | Head `a8fe084` | Receipt |
| --- | --- | --- | --- |
| Configure / build / ctest / unit runner, `LWSRP_MILAN=OFF` | rc 0 each; 102 tests, 26658 passes | rc 0 each; 102 tests, 26658 passes | `receipts/gate-{base,head}-OFF.*` |
| Same, `LWSRP_MILAN=ON` | rc 0 each; 102 tests, 26646 passes | rc 0 each; 102 tests, 26646 passes | `receipts/gate-{base,head}-ON.*` |
| behave (behave 1.3.3), OFF and ON libraries | rc 0; 1 feature, 3 scenarios, 10 steps | rc 0; 1 feature, 3 scenarios, 10 steps | `receipts/gate-*.behave.log` |
| Reversal runner `tests/check_reversals.py`, OFF / ON, run concurrently | not applicable | rc 0 / rc 0; "Reversals: 106; failures: 0" each; baseline and restored scenarios rc 0 | `receipts/reversals-head-{OFF,ON}.*`, `receipts/reversal-scenario-logs/` |
| The 7 author plants applied to the base steps and hook | all 7 survive, behave rc 0, 3 scenarios pass | all 7 killed with the exact named set and words | `receipts/plants-base.json`, `receipts/plants-head.json` |
| Doc checks: sentences / references / reference self-test / links (authenticated) | — | rc 0 each: 1017 sentences, 0 over limit; 0 unlinked; 79 self-test cases; 374 local links, 21 external, 0 failures | `receipts/doc-*.log`, `receipts/doc-checks.rc` |

The two reversal profiles ran concurrently on 16 cores with no ctest timeout. That is consistent with the author's disclosed rerun.

### Reviewer plants (independently spelled; `scripts/make_specs.py`, `scripts/plants.py`)

Each plant edits one line in a scratch copy, rebuilds `libshlan`, and runs behave.

| Plant | Family | behave rc | Failing scenarios | Assertion words seen |
| --- | --- | --- | --- | --- |
| `r-disable-calls-enable` (`int rc = shlan_port_enable(...); return rc;`) | disable | 1 | Disable a port | `after disabling port 0: port 0 enabled, expected disabled` |
| `r-connect-noop` (`return sw ? 0 : -1;`) | connect | 1 | all three | `after connecting: ports 0-47 enabled, expected disabled` |
| `r-enable-noop` | enable | 1 | all three | `after enabling port 0: port 0 disabled, expected enabled`; `enabling port 255 returned 0, but the simulated switch has no such port` |
| `r-disable-noop` | disable | 1 | Disable a port | `after disabling port 0: …` |
| `r-enable-xor-port` (port ^ 1) | enable | 1 | Enable, Disable | port flag words |
| `r-enable-wraps-range` (port % 48) | enable | 1 | Reject an out-of-range port | `enabling port 255 returned 0, but the simulated switch has no such port` |
| `r-enable-accepts-oor` | enable | 1 | Reject an out-of-range port | same |
| `r-enable-rc-lie` (sets flag, returns -1) | enable | 1 | Enable, Disable | `enabling port 0 returned -1, expected 0` |
| `r-connect-rc-lie` (returns 1) | connect | 1 | all three | rc words |
| `r-connect-enables-last` (connect then enable 47) | connect | 1 | all three | `after connecting: port 47 enabled, expected disabled` |
| `r-disconnect-disables-all` | disconnect | 1 | Enable a port (teardown hook error) | `after disconnecting: port 0 disabled, expected enabled` |
| `r-env-connect-to-disconnect` (harness mapping) | connect | 1 | all three | `connecting returned None, expected 0` |
| `r-env-enable-to-disable` (harness mapping) | enable | 1 | Enable, Disable | port flag words |
| `lim-disconnect-noop` | disconnect | 0 (survives, declared limit) | — | — |
| `lim-disable-reconnects` | disable | 0 (survives, declared limit) | — | — |
| `lim-disable-all` (clears all 48 flags) | disable | 0 (survives; same cause as the declared limit) | — | — |

Two independently spelled plants (`r-disable-calls-enable` and `r-connect-noop`) survive on the base steps, with rc 0 and 3 scenarios passing. A subset re-run under behave 1.2.6 / CPython 3.12.3 gave the same named sets and words, including the teardown hook error (`receipts/plants-head-behave126.json`).

### Layout probes

| Probe | Result |
| --- | --- |
| Field after `port_state` / field before it / `unsigned char` flags / `SIM_MAX_PORTS (48)` | behave rc 1, 3 scenarios untested; `HOOK-ERROR in before_all: AssertionError: struct sim_priv in sim_adapter.c no longer matches the port flag reader` (behave 1.3.3 and 1.2.6) |
| Consistent `SIM_MAX_PORTS 64` | rc 0, 3 scenarios pass; the count follows the adapter |
| Public `struct shlan_switch`: extra field before `priv`, or `ops`/`priv` swapped | behave terminated by SIGSEGV (rc -11). The run stops, but without a named error (see R613-1-02) |

### Parent consumer (scratch milan-fpga at dev `f88df731c77ec3d876b74e41b0091c513370afe9`)

- The parent harness compiles only lwSRP `src/` (`sw/firmware/ctrl/test/ctrl_arms.py`, `LWSRP_TREE = "src"`). `git diff 08ee86e8..a8fe0849 -- src CMakeLists.txt tests/unit tests/features/switch.feature tests/features/switch_bindings.c` is empty.
- With `third_party/lwSRP` at this head and the harness unmodified, the harness refuses the revision with rc 2: `REFUSED: lwSRP at a8fe0849… is not the pinned 9197193e…` (`receipts/fw-head-unmodified.*`).
- I used a scratch-only `LWSRP_REV` edit in separate worktrees, with protocol-processor `2ad2f845` and gptp-processor `5dce647a` checked out. `test_ctrl_firmware.py --require-rv32 --jobs 4` gave rc 0 at the pin `9197193e`, at the base and at the head. Each run had 59/59 arms ok and 1191 GoogleTest cases, including 35 lwsrp/srp arms with 291 cases. Per-arm verdict lines are identical (`receipts/fw-rv32-*.log`, `receipts/fw-rv32-compare.txt`).
- The SRP RV32 object-size blocks are byte-identical between base and head after path normalisation. Pin to head differs only in `core_mrp_mad.o` (12709 → 13309 text) and the totals, which comes from work already on main (`receipts/fw-rv32-srp-blocks-*.norm`). An earlier run without `--require-rv32` gave 49/49 arms with the same 1191 cases, because the 10 SRP RV32 arms are gated on that flag (`receipts/fw-{pin,base,head}.log`). Nothing in the parent was committed, and no shared checkout was touched.

## Lens analysis

### Conformance
- The feature file is byte-identical. The step texts are unchanged, so behave binds the same 10 steps (`receipts/gate-*-OFF.behave.log`). No MRP code, registration or declaration path is driven, and no clause claim is made or changed. Acceptance 1 does not apply to MRP effects because no step drives them.
- Each step checked against its words:
  - `Given the switch is connected` (`switch_steps.py:8-16`): rc 0, then every flag disabled after seeding them enabled. This is the simulated connect's effect (`sim_adapter.c:12-17`).
  - `Given/When port N is enabled` and `When port N is disabled` (`:19-62`): rc 0, and only that port's flag moves to the named state. For a port the adapter lacks, a nonzero rc and no change.
  - `Then … active/inactive` (`:65-74`): the flag is read directly.
  - `Then the operation should fail` (`:77-80`): a nonzero rc and the flags unchanged.
- Every expected value comes from the scenario text (port id, enabled/disabled) or from the adapter (`SIM_MAX_PORTS` parsed from `sim_adapter.c`, flags read from `struct sim_priv` memory). None comes from a binding's return. CLEAN.

### RTL
- No HDL, firmware source or generated artifact changes. The RTL lens is applied through the consumer: lwSRP `src/` is unchanged, and the parent's firmware SRP arms (host and RV32) give identical verdicts and identical SRP RV32 object sizes at base and head. CLEAN.

### Robustness
- Teardown always destroys the adapter (`environment.py:132-137`, `try/finally`) and skips a failed creation (`:128-129`). Creation failure is a named assertion (`:122`).
- A changed `struct sim_priv` stops the run with a named error under both behave releases, and a consistent count change is followed. Hook errors produce a nonzero exit under behave 1.2.6 and 1.3.3.
- Two residual hazards remain outside the documented workflow (R613-1-02, SUGGESTION). The layout is read from the checkout's source, not from the library that `SHLAN_LIBRARY` names. A public handle layout change ends in SIGSEGV rather than a named error. Neither can turn a wrong binding into a pass in the documented workflow (the library is built from the same checkout). CLEAN.

### Tests
- Acceptance 1 is met: every step asserts its effect (see Conformance).
- Acceptance 2 is met. The issue's two plants (`port_disable` dispatching to enable, `connect` as a no-op) and one more wrong dispatch per family (disable ×3, enable ×1, connect ×2, disconnect ×1) are killed by the runner at head. Each is required to fail exactly its named scenarios and print its words (`check_reversals.py:196-224`, `:385-392`), and all seven survive on the base steps. Thirteen independently spelled reviewer plants are killed, and the three survivors are the declared simulation limits.
- Base and head unit, ctest and behave pass in both profiles. The runner's scenario parser (`failed_scenarios`, `check_reversals.py:306-316`) reads both the failing and the errored lists, so the teardown plant counts.
- Observations are recorded as SUGGESTIONs R613-1-03 and R613-1-04. CLEAN.

### Docs
- The `doc/tester.md` and `doc/manager.md` changes replace the stale "repeats the operation" text with the new checks, the seven plants, the 106-reversal count (verified: 95 unit, 7 scenario, 2 freestanding, 1 strict, 1 embedded) and the limits. No stale issue #4 defect text remains (grep over `README.md`, `CONTRIBUTING.md`, `doc/`). All doc checks return rc 0.
- The PR body figures match my measurements: unit counts, 106/106 per profile, and parent 59/59, 1191, 35 and 291.
- The public diff, commit metadata and PR body contain no instrument, host or private path names (scan of the added lines).
- One wording defect is recorded as RESIDUE R613-1-01. CLEAN.

## Findings

### R613-1-01 — RESIDUE — Docs
- Location: `doc/tester.md:163`.
- Evidence: the line reads "The [connection step](../tests/features/steps/switch_steps.py) first enables every port, so the reset is visible." The step writes every flag directly through `SimulatedPorts.set_all` (`switch_steps.py:13`, `environment.py:58-60`). It makes no enable call through a binding. The PR body says "seeds every flag enabled".
- Impact: purely prose. A reader may think the step drives the enable binding 48 times. No test, figure or claim changes.
- Exact fix: "The [connection step](../tests/features/steps/switch_steps.py) first sets every simulated port flag to enabled without a binding call, so the reset is visible."
- Verification: re-run `doc/tools/check_sentences.py` and `check_references.py` (rc 0).

### R613-1-02 — SUGGESTION — Robustness, Tests
- Location: `tests/features/environment.py:7`, `:10-12`, `:15-24`, `:42-44`, `:58-60`.
- Evidence: `_sim_port_count()` parses the checkout's `sim_adapter.c`, but the reader maps memory of whatever library `SHLAN_LIBRARY` or `build/` provides. A stale library with a smaller `struct sim_priv` would let `set_all` write past its allocation. The ctypes mirror of `struct shlan_switch` is not guarded. Probes `hdr-field-before-priv` and `hdr-swap-ops-priv` end in SIGSEGV (rc -11), not a named error (`receipts/plants-header.json`).
- Impact: none in the documented workflow (the library is built from the same checkout, and the run still stops). The hazard is a confusing crash on misuse.
- Suggested outcome (optional): name the dependency in `doc/tester.md`, or add a guard that does not use the binding under test. For example, check the `struct shlan_switch` field order in `switch.h` the same way, and require `SHLAN_LIBRARY` to sit in a build of this checkout.

### R613-1-03 — SUGGESTION — Tests
- Location: `tests/features/steps/switch_steps.py:29-32` versus `:77-80`.
- Evidence: for an out-of-range port, the `When port N is enabled` step itself asserts refusal and no flag change. The `Then the operation should fail` step's checks therefore can never be the failing assertion. The plants `r-enable-wraps-range` and `r-enable-accepts-oor` fail "Reject an out-of-range port" with the When step's words.
- Impact: none on acceptance. The scenario fails by name with clear words. The Then step is a redundant second check.
- Suggested outcome (optional): leave the refusal verdict to the Then step (the When step records rc and checks only that no other flag moved), or note the redundancy in the step comment.

### R613-1-04 — SUGGESTION — Tests, Docs
- Location: `doc/tester.md:193-195`; `tests/features/switch.feature:11-14`.
- Evidence: probe `lim-disable-all` (a disable binding that clears all 48 flags) survives with rc 0. It has the same cause as the documented "disable binding that reconnects" limit: only port 0 is ever enabled.
- Impact: covered by the documented cause and by the "Two enabled ports" next case. No acceptance gap.
- Suggested outcome (optional): word the limit as "a disable binding that also clears other ports, for example by reconnecting, also passes".

## Reviewer-owned ledger

| Lens | Verdict | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | issue #4 scope, `switch.feature`, `switch_steps.py`, `environment.py`, `switch.h`, `sim_adapter.c`; behave step binding at base and head | R613-1 | a8fe0849f37a0908bc899754c2644cf30a54b67f |
| RTL | CLEAN | empty `src/`/CMake diff; parent `test_ctrl_firmware.py --require-rv32` at pin, base and head (59 arms, 35 SRP arms, identical verdicts and SRP RV32 sizes) | R613-1 | a8fe0849f37a0908bc899754c2644cf30a54b67f |
| Robustness | CLEAN (SUGGESTION R613-1-02) | `environment.py` hooks; 4 layout probes, 1 consistent-count probe, 2 header probes; behave 1.2.6 and 1.3.3 hook-error exit codes | R613-1 | a8fe0849f37a0908bc899754c2644cf30a54b67f |
| Tests | CLEAN (SUGGESTIONs R613-1-03, -04) | `switch_steps.py`, `check_reversals.py`; base/head gates in both profiles; reversal runner 106/106 in both profiles; 7 author plants at base and head; 16 reviewer plants | R613-1 | a8fe0849f37a0908bc899754c2644cf30a54b67f |
| Docs | CLEAN (RESIDUE R613-1-01) | `doc/tester.md`, `doc/manager.md`, `README.md`, `CONTRIBUTING.md`, PR body, commit metadata; four doc checks rc 0; privacy scan | R613-1 | a8fe0849f37a0908bc899754c2644cf30a54b67f |

## Prior public findings on this PR

When this pass started, PR #19 had no review or finding: only the two review-start comments, 0 reviews, 0 inline comments. The originating findings from the PR #3 reviews (R536-1-02 and R537-1's suggestion: a `port_disable`→enable binding and a `connect` no-op both pass) are RESOLVED at this head. Both now fail named scenarios, and they still survive on the base steps (`receipts/plants-*.json`).

## Concurrent public review cross-check (read only after the verdict and ledger above were written)

The internal review R612-1 was posted on PR #19 during this round, with a POSITIVE verdict at the same head and three SUGGESTIONs. I read it only after this report's verdict and ledger were on disk. My verdict is unchanged.

- R612-1-01 (SUGGESTION: a disable binding that ignores its port survives). Agreed and retained as a SUGGESTION. It has the same cause as my R613-1-04 (`lim-disable-all` survives): only port 0 is ever enabled.
- R612-1-02 (SUGGESTION: the `struct shlan_switch` mirror is unguarded and fails by SIGSEGV). Independently reproduced (`hdr-swap-ops-priv`, `hdr-field-before-priv`, rc -11). Retained as a SUGGESTION and merged into R613-1-02.
- R612-1-03 (SUGGESTION: no runner plant fails only "Reject an out-of-range port"). Confirmed by my `r-enable-wraps-range` and `r-enable-accepts-oor`. Each fails only that scenario at head and is not in `CASES`. Retained as a SUGGESTION: the acceptance asks for one wrong dispatch per step family, and the enable family has one.
- R612-1 records no RESIDUE. I retain R613-1-01, a wording fix only.

## Real limits

- Physical calibration was NOT RUN. No hardware, bench, target or network interoperability was exercised. Field skips are not hardware proof.
- No manager source bank ran at this exact head, and none is claimed or inferred. The current-dev merge candidate (builder and native banks, live dev `f88df731…`) is the manager's merge-turn duty.
- lwSRP has no hosted workflow, so no hosted job executed at this head (0 check runs, 0 status contexts). Hosted and act acceptance belong to the manager.
- The parent check used a scratch-only edit of the harness pin. The `external` submodule was not checked out, because the harness did not need it. Mermaid rendering was not re-run, because the diff changes no graph.
- The behave 1.2.6 / CPython 3.12.3 run covered a subset of 8 plants plus the unmodified tree. The full set ran on behave 1.3.3 / Python 3.14.7.

## Pending manager duties

- Build and validate the current-dev merge candidate (source base `08ee86e8` onto live dev `f88df731…`) with the builder and native banks, and link those receipts on the PR.
- Carry RESIDUE R613-1-01 to the residue checklist.
- Publish this report and the files listed in `MANIFEST.sha256`.

R613-1 FINISHED
