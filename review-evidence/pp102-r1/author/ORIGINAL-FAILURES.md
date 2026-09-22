# Original failures and expected negative results

1. The historical integrated parent command `python3 scripts/check_cpp_idiom.py`
   returned `build without warnings 1 > ratchet 0` for authorized PP pin
   `8452f564294300a82d56eed464276576f65f4d58`. This is public evidence from
   parent #400 comment 5781426819, preserved verbatim in
   `logs/original-finding.log`. A180 did not rerun the full parent gate and
   does not claim that gate now passes.
2. The actual immutable `cflags_missing` reports `['-Wall', '-Wextra']`
   for the author base Makefile. `logs/baseline-cflags.log` and
   `context/Makefile.before` retain this reproduction. The driver exits 0
   because the expected defect was observed; this is not a clean baseline.
3. `logs/focused-cflags.log` is an original exit-2 validation attempt.
   The corrected Makefile and both flag-removal controls passed first.
   An additional call to the parent's `_selftest_warning_flags` passed seven
   parser fixtures, then refused its live population arm because the
   read-only parent checkout's processor submodules are uninitialized.
   No parent setup was changed. `check_flags.initial.py` preserves that
   original driver. The final helper makes the optional wider controls
   explicit via `--parent-controls`; `logs/focused-cflags-only.log`
   records exit 0 for the required bounded test alone. This is not a pass
   of the whole parent self-test.
4. Removing newly repeated `-Wall` alone reports `['-Wall']`; removing
   newly repeated `-Wextra` alone reports `['-Wextra']`. These are expected
   negative controls using disposable copies, with copies/patches and
   hashes preserved under `context/` and `focused-results.json`.
5. Fixture guard `0002` and `1002` compiler refusals are expected behavior,
   graded by the unchanged four-case guard. The full pp_top raw log records
   the exact matched diagnostics and successful guard verdict, including
   the locale regression. The guard itself captures compiler output and
   prints only the graded result for expected outcomes.

No raw log was replaced or deleted to hide a failure. Remaining manager
gates were not attempted and have no author pass claim.
