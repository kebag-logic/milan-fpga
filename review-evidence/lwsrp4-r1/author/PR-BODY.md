[A597] Switch scenario steps assert their effect on the simulated switch

Closes #4

## Why

The behave steps checked only that each call returned. A `port_disable` binding that called enable, or a `connect` binding that did nothing, still passed all three scenarios (PR #3 reviews, R536-1-02 and R537-1).

## What changed (tests and docs only)

- `tests/features/environment.py`: `SimulatedPorts` reads the simulation adapter's own port flags (`struct sim_priv` in `src/modules/sim_adapter.c`), never through a binding. The flag count comes from the adapter source; a layout change stops the run with a named error instead of reading the wrong memory. Connection moves from the setup hook to the Background step so the step can check it. Teardown requires disconnection to leave every flag unchanged.
- `tests/features/steps/switch_steps.py`: each step checks its effect.
  - `Given the switch is connected` seeds every flag enabled, then requires connect to return 0 and clear all 48.
  - Enable and disable steps require rc 0 and a change to their own port's flag only. An out-of-range port must be refused with no flag change.
  - `Then ... active` and `Then ... inactive` read the flag directly instead of repeating the operation.
  - `Then the operation should fail` also requires every flag to be unchanged.
- `tests/check_reversals.py`: seven scenario plants, each required to fail exactly its named scenarios with its assertion words. The runner also runs the scenarios before and after the plants.
- `doc/tester.md`, `doc/manager.md`: describe the checks, the plants and the limits.

No change to `src/`, CMake, the unit tests, `switch_bindings.c` or `switch.feature`. No MRP behaviour is involved: the steps drive only the switch interface and its simulation.

## Planted bindings

| Plant | Fails | Assertion words |
| --- | --- | --- |
| disable binding calls enable | Disable a port | `after disabling port 0: port 0 enabled, expected disabled` |
| harness maps disable to the enable binding | Disable a port | same |
| disable acts on the next port | Disable a port | same |
| enable binding calls disable | Enable a port; Disable a port | `after enabling port 0: port 0 disabled, expected enabled` |
| connect binding is a no-op | all three | `after connecting: ports 0-47 enabled, expected disabled` |
| connect binding calls disconnect | all three | same |
| disconnect binding calls connect | Enable a port (teardown error) | `after disconnecting: port 0 disabled, expected enabled` |

Against the base steps and setup hook, all seven survive with behave exit 0.

## Results

| Check | Base `08ee86e` | Head |
| --- | --- | --- |
| Configure, build, ctest, unit runner (default profile) | exit 0; 102 tests, 26658 assertions | exit 0; 102 tests, 26658 assertions |
| Same, `LWSRP_MILAN=ON` | exit 0; 102 tests, 26646 assertions | exit 0; 102 tests, 26646 assertions |
| behave, both libraries, CPython 3.12.3 and 3.14 | exit 0; 3 scenarios, 10 steps | exit 0; 3 scenarios, 10 steps |
| Reversal runner, default / Milan profile | — | exit 0 / exit 0; 106 of 106 killed each |
| Embedded and freestanding checks | — | exit 0 |
| Sentence, reference (+ self-test), link and graph checks | — | exit 0 |

The two profiles were run one after the other. A first attempt that ran them at the same time on a heavily loaded host hit ctest's fixed 10-second timeout in one unrelated unit reversal per profile (exit 1). Every scenario plant was still killed in that attempt.

Parent consumer: milan-fpga dev `f88df731` with `third_party/lwSRP` at this head. The firmware harness refuses any lwSRP other than its pin `9197193e`, giving exit 2. With a scratch-only edit of that pin, base and head each pass 59 of 59 arms and 1191 GoogleTest cases, including the 35 SRP arms (291 cases). Per-arm verdicts match the parent's own pin, and base and head RV32 object sizes are identical. Nothing in the parent was committed.

Commands, from the repository root:

```sh
cmake -S . -B "$LWSRP_BUILD" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=OFF
cmake --build "$LWSRP_BUILD" --parallel 2
ctest --test-dir "$LWSRP_BUILD" --output-on-failure
SHLAN_LIBRARY="$LWSRP_BUILD/libshlan.so" behave
python3 tests/check_reversals.py --work-dir "$REVERSAL_SCRATCH" --prefix "$CGREEN_PREFIX"
python3 tests/check_reversals.py --work-dir "$MILAN_REVERSAL_SCRATCH" --prefix "$CGREEN_PREFIX" --milan ON
```

## Limits

- The simulation's disconnect changes nothing, so a disconnect binding that skips the call is equivalent on this adapter and passes.
- The disable scenario enables only port 0, so a disable binding that reconnects also passes. The scenario was not widened, to keep its intent.
- The reversal runner's interpreter must now import behave.
- No hardware, target build or network interoperability was exercised.
