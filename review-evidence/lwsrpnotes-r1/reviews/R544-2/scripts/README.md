# R544-2 reproduction scripts

All scripts take paths as arguments and write only under the output directory given.
CHECKOUT is a clean clone at f680e3c8c2b02ee4ab4f935ca3a2b893d92e7152.
PREFIX is a unit-framework install prefix (cgreen 1.6.3 was built from its public tag; CMake 4 needs `-DCMAKE_POLICY_VERSION_MINIMUM=3.5`).

| Script | Purpose |
| --- | --- |
| `run_suites.sh CHECKOUT PREFIX OUT` | Both profiles (configure, build, ctest, unit runner, behave, dry run), embedded check, freestanding OFF/ON, both reversal drivers, run concurrently. |
| `count_tests.sh CHECKOUT PREFIX OUT [REV]` | Exports REV (default HEAD) and counts executed tests per profile by wrapping the reporter's start_test. |
| `run_doc_checks.sh CHECKOUT OUT` | Sentence, reference, reference self-test, link (authenticated and anonymous) and graph-render checks. |
| `probe_mutations.py CHECKOUT PREFIX OUT` | Reviewer probes on the note 4/5 guard in exported copies, both profiles. |
| `run_sanitizers.sh CHECKOUT PREFIX OUT` | Address and undefined-behaviour sanitizer unit runs, both profiles. |
| `verify_clone.sh CHECKOUT HEAD TREE` | Byte, mode, index, gitlink and status integrity of the clone. |
