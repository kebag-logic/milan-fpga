## Part A checkpoint

Local lwSRP branch `apache-2.0`, commit `fed1a0d0a08e1f9682ce1fca3bb4b9985d846e5b`, based on `19f5796b63652eb1151906de73cb827d4980a53f`.
`LICENSE:1` contains the complete official Apache-2.0 text. `NOTICE:1` names the assigned copyright holder. `README.md:65` adds the licence and company-contribution statement. Source, header, build and test files carry the SPDX identifier; the existing Kconfig identifier was preserved. No conflicting licence notice was found. The queue implementation identifies an external algorithm, without a third-party code copyright or licence notice; the owner's recorded ownership decision governs the original implementation.

| Check | Exit | Result |
|---|---|---|
| CMake configure and build | 0 | Host library and existing unit executable build |
| Existing CTest target | 0 | Empty placeholder suite; supplies no behavioral coverage |
| Existing MRPDU cgreen suite, loaded directly | 0 | Nine tests, 1,690 assertions |
| Existing behave suite, unchanged | 1 | Setup failure: `shlan_connect` has no exported symbol; three scenarios untested |
| Diff whitespace check | 0 | Clean |

The unsuccessful direct executable link lacked a main function; the existing suite was then loaded correctly through its test runner. The behavior-suite setup failure is pre-existing: the public switch operations are static inline and cannot be resolved through the shared-library interface. Part B needs a separate test-entrypoint fix before functional changes can be graded. No parent source has changed.

## Upstream implementation checkpoint
