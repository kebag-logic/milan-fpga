[A583] REVIEW READY (round 4)
Commit: e07b305458ed3520e4adfc55e9746144ce5cdc79 (tree ec8f8fb21ee972f83bf14a535e07f3633bc9a35e), four new commits on d1b22e80: 6d43e1978, d25ae924a, 9453fcc10, e07b30545. No rebase or amend, not pushed (PR #705 still shows d1b22e80).

Changed (only the boundary gate, its new controls module `ctrl_plants.py` and their docs; no firmware source, header, test, builder, mutation table, coverage row, build flag, Makefile or workflow):
- R585-3-F1, the boundary step within 5 minutes, the same configurations, modes and shapes judged and every control kept:
  - Each preprocessing runs once per run. It is reused only for the same unit and the same arguments, with every file it read byte-identical (sha256) and no file the trees gained or lost that it could look up by name. A preprocessing that failed other than on an `#error` is never reused.
  - The controls share one prepared base: the unplanted copies, judged first, which must pass (a control of its own).
  - A control that must be refused stops at the finding it names. A judgement returns only when everything it started has finished.
  - A unit's configurations go to four compilers at once and every side runs at once. The stack's own gate runs beside the controls.
  - `ctrl_boundary.py` stays under the 1000-line module limit: the controls' data moved to `ctrl_plants.py`, one of the gate's own modules.
  - `judge(trees, rv32, work, universe, computed, control=None)` keeps the positional form the reviewers' probe harnesses call.
- R584-3-F1: a builder's C++ name now resolves in the firmware tree too (`test/test_maap_differential.cpp`) and in every directory of the checkout the builder names (`aecp_wire.py`'s `sim_main.cpp`). It resolves in the trees judged.
  - A name the builder writes itself is followed through the builder's literals (`reference.cpp`).
  - A name that resolves to no file, or that a builder computes, fails the gate by name.
  - `NOT_SOURCES` lists the two report paths `fw_coverage_selftest.py` names, which are no files. Each is checked (held by its builder, unresolved, unwritten) and printed.
- R585-3-S1: a `-D` or `-U` that is neither a literal nor an f-string is refused by name. That covers `"-D" + NAME`, `"-DNAME=" + value`, `"-D%s" % NAME`, a bare `-D` alone, a computed macro name in an f-string, and in Makefiles `-D$(NAME)`, `-DNAME=$(VALUE)` and `$(addprefix -D,...)`. No builder uses them, so the 18 derived modes are unchanged.
- Docs: `sw/firmware/ctrl/README.md:94-102,114-118`; `docs/testing/CI_WORKFLOWS.md:67-74`, the budget (5 of the job's 45 minutes), the measured worst case and the margin; the module docstrings.

Validation (each commit's tree checked before it was committed; host for the boundary, the probes, the images and the docs; the CI-parity container with CPython 3.12.3, gcc 13.3 and GoogleTest 1.14.0 for the firmware gates; clean clones):
- Step timings, `ctrl_boundary.py --require-rv32 --selftest` pinned to four CPUs (the hosted runner's count) on a shared host:
  - before, at d1b22e80: 807 s;
  - at 9453fcc10: 82.0, 73.6 and 81.2 s (load average 23);
  - at e07b30545: 86.0 s, beside this lane's own container gates.
  - The 807 s run matches the hosted step at d1b22e80, whose self-test phase took 12 min 16 s. The worst run leaves 214 s of the 300 s budget.
- At e07b30545 the self-test passes: `(942 configurations, 943 preprocessed) ... 0 finding(s), 60 boundary and 20 pin controls, 0 misbehaved`. The 60 boundary controls are the base, 56 refused by name and 3 passing.
- Twelve controls are new, each refused by name:
  - R584-3's plant: `firmware c++: maap/maap_r584.h includes tsn-c-stack/tests/acmp_fake.hpp, not one of the stack's public headers`, reached only through `test_maap_differential.cpp`;
  - a C++ name that is no file, and a computed one;
  - a generated C++ source reaching a C++-only stack-example include;
  - a `NOT_SOURCES` name that becomes a file, and a stale `NOT_SOURCES` entry;
  - six Python and Makefile flag forms of R585-3-S1.
- Memo check (scratch): every control judged in full with and without reuse. 0 of 60 differ.
- The reviews' own probe scripts, rerun unchanged against a clean clone:
  - R584-3 `boundary_probes.py`: `cplusplus-new-header-maap-differential` is now CAUGHT; the other 19 give R584-3's verdicts.
  - R585-3 `boundary_probes3.py all`: f1 to f4 now REFUSED by name, f5 and f6 REFUSED, the other 12 CAUGHT.
  - R585-3 `cxx_unfollowed_probe.py`: CAUGHT through both `test_maap_differential.cpp` and `test_maap_mbx.cpp`.
  - R585-2 `boundary_probes.py all`: 11 of 11 CAUGHT.
- RV32 images: 35 of 35 ELF files byte-identical to round 3's and to dev aef7ac66's (manifest sha256 de8ae063…).
- `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4`: PASS. Its 843 verdict lines are identical to round 3's (471/471 control, 74/74 AECP, 169 and 68 SRP, 2/2 lwSRP pin).
- Coverage: `--selftest` 29 of 29; `--check` PASS (30 files), every row identical to round 3's.
- Harness self-tests: 17, 18/18 and 33 checks.
- All 54 docs-job commands exit 0, with every submodule and with only the hosted docs job's three. `ci_events.py --check` OK (1757 items). em-dash: 0 findings over 18 added lines. `check_py_idiom.py`: no ratchet raised.

Acceptance criteria: met at the head. Images are byte-identical to dev aef7ac66 at every shape; coverage and kills are unchanged. Round 4 items 1 to 3 are met as above, except item 1's hosted confirmation, which is the manager's.
Open risks/questions:
- The step is not yet measured on a hosted runner (no push).
- The memo's reuse assumes a preprocessing depends only on its arguments, the unit's path, the bytes it read and which files exist where it looks. The gate adds no file outside its temporary directory during a run, and the scratch check found no difference.
- The first round-4 commit (6d43e1978) has no memo, so its self-test takes about 25 minutes; only the head runs in CI.
- R584-3-S1 and R585-2-S2 (both optional) are not addressed.
- Hosted CI and act have not run at any round-4 commit.

Details are in the Round 4 sections of the lane packet's HANDOFF.md and PR-BODY.md.
