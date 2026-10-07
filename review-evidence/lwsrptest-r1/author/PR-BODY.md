[A562]

[Closes #2](https://github.com/kebag-logic/lwSRP/issues/2).

The switch helpers are static inline functions. They have no exported symbols for ctypes. [Test bindings](https://github.com/kebag-logic/lwSRP/blob/ad6199083a1eb242f37dacf88de94bd00c4b3658/tests/features/switch_bindings.c#L1) call the same public helpers. The [harness](https://github.com/kebag-logic/lwSRP/blob/ad6199083a1eb242f37dacf88de94bd00c4b3658/tests/features/environment.py#L31) loads those bindings. Protocol behavior is unchanged.

The [unit target](https://github.com/kebag-logic/lwSRP/blob/ad6199083a1eb242f37dacf88de94bd00c4b3658/CMakeLists.txt#L43) now runs the existing codec suite through a [runner](https://github.com/kebag-logic/lwSRP/blob/ad6199083a1eb242f37dacf88de94bd00c4b3658/tests/unit/main.c#L1). The empty placeholder is removed. Configuration requires cgreen. CTest rejects an empty suite.

Before: CTest passed one target with zero assertions, exit 0. Behave stopped at setup, exit 1. All three scenarios and ten steps were untested.

After: CTest passes one target with nine codec tests and 1,690 assertions, exit 0. Behave passes one feature, three scenarios, and ten steps, exit 0.

Removing the bindings or restoring the old ctypes setup makes behave exit 1. Restoring the empty target or using an empty runner makes CTest exit 8. A wrong codec assertion also makes CTest exit 8. All planted reversals were restored. A configure without cgreen exits 1.
