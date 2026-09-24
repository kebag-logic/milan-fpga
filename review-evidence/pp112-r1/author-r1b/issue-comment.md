[A266] REVIEW READY

PR #114 / issue #112, round 1b. Local head: `90e1ce13bb1c49c0c985b64e583128b7b8c6a9c4` on `112-stale-grant` (baseline `73a5478784bd861f8c8d33c0d1619594390b9529`).

Changed only `tb/srp_top/sim_main.cpp` and `tb/srp_admission/mutants.py`: split declarations, extracted the recorded-cycle assertions into a helper without advancing the simulation, and annotated/documented the mutation entry point. Checks, stimuli, ordering, expected values, and printed results are preserved.

Validation before → after:

- `bash scripts/run_suites.sh`: rc 0 → 0; 33 suites, 739421 checks, 0 failures both times. SRP top remains 735/735; decoder 190/190; encoder 556/556; stream FSMs 1068/1068.
- `make -C tb/srp_admission shapes`: rc 0 → 0. N=1/2/3/5/8 remain 683/5252/20053/123286/723046 checks respectively, all PASS.
- `bash scripts/lint_hdl.sh`: rc 0 → 0; 40 modules pass. Suite bank and lint commands ran in the foreground with output written directly to logs, never piped.
- `python3 tb/srp_admission/mutants.py --output <logs>`: rc 0 → 0; 4/4 campaign checks PASS. Both controls pass; both stale-evaluation mutants are killed by the named assertion, with the same 184/5252 and 4032/723046 failing checks.
- Full SRP top/admission stdout, bank summaries, lint output, mutation campaign output, and all control/mutant runtime output are byte-for-byte identical before/after.
- Parent `python3 scripts/check_cpp_idiom.py`: **rc 0** at final head; multi-declarator and long-function counts both 0.
- Parent `python3 scripts/check_py_idiom.py`: **rc 0** at final head; unannotated and undocumented public-function counts both 0.

Both parent gates ran only in `$LANES/pp112-parent-consumer`, with the child checkout and temporarily staged gitlink at the final head. The parent index and child checkout were restored; parent HEAD is unchanged and both checkouts are clean.

Handoff, raw logs, return codes, output hashes, and patch: `$MANAGEMENT/2026-09-23/pp112-a266/HANDOFF.md`.

Acceptance criteria met. No open blocker. Commit has one subject line, no body or trailers. No push or PR edit performed.
