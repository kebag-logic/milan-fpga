# [A193] HANDOFF: issue #104, the fixture-guard idiom fix

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Issue: #104
- Branch: `104-fixture-guard-idiom`, from main `e1d0176d3a486bce4a80765cfbcefcb61964f8e9`
- Fix head: `0ca178678490024707b3a2393a86dc9e7b2a0ca4`, one commit: "Annotate and document the two public pp_top fixture-guard functions"
- Lane: `$LANES/pp104-fixture-guard-idiom`. Nothing was pushed, and no PR was opened.

## What changed

| File | Function | Change |
|---|---|---|
| `tb/pp_top/fixture_guards.py` | `main` | `-> int`, plus a docstring stating the contract: what it reads from the command line, the four fixture cases, `LC_ALL=C`, the exit status (0 = all four PASS, 1 = mismatch after the compiler output is printed), and the `CalledProcessError` raised when the root query or model generation fails |
| `tb/pp_top/test_fixture_guards.py` | `CompilerLocaleTest.test_compiler_environment_and_arguments` | `-> None`, plus a docstring stating what the test requires |

These are the only two public functions that the parent's Rule 12 gate (`scripts/check_py_idiom.py`) flagged in this repository. The change touches 2 files: 19 insertions and 2 deletions. No statement or branch changed.

## Behaviour-preservation evidence

- **AST identity.** I stripped the new return annotation and docstring from each function and compared the result with `git show e1d0176:<file>`. The two ASTs are identical for both files. `argparse`'s `description=__doc__` reads the module docstring, which is unchanged.
- **Guard output.** I ran `make fixture-guards` before and after the change. Its stdout (the four `fixture guard …` lines and `fixture guards: 4 cases PASS`) is byte-identical.
- **Unit test report.** `make fixture-guards-test` gives `Ran 1 test … OK` before and after. The only difference is that unittest's `-v` report now prints the first line of the new docstring under the test id. That is a change to the report format, not to the test.
- **The test still catches the regression.** On a scratch copy, I deleted `compiler_env["LC_ALL"] = "C"` and the test failed with `FAILED (failures=2)`, as `tb/pp_top/README.md` requires.

## Gates in this repository (at the fix head)

| Command | Result |
|---|---|
| `make -C tb/pp_top` (unit test, fixture guards, both builds) | exit 0. `fixture guards: 4 cases PASS`; `1411 checks: 1411 PASS, 0 FAIL` |
| `python3 scripts/check-links.py` | `links: 807 checked, OK` |
| `python3 scripts/check-matrix.py` | `matrix: 115 REQ rows, 17 GAP findings, OK` |
| `python3 scripts/render-wavedrom.py --check` | `wavedrom: 18 blocks checked, OK` |
| `make stale` / `make check` | exit 0 |
| `python3 scripts/gen_matrix.py --check` | `matrix: OK (86 rows, 0 untested)` |
| `./scripts/lint_hdl.sh` | exit 0 (no HDL was touched) |

Not run here: `./scripts/run_suites.sh` over every suite, and the `nvm_port` figures step. The change touches only `tb/pp_top/*.py`, and those files are reached only by the `tb/pp_top` Makefile, whose full run is recorded above. Local Verilator is 5.052; CI pins v5.050.

## Parent consumer gates

I took a private clone of the read-only parent checkout `$LANES/pp102-parent-consumer` into scratch and detached it at parent `574c29fa111c74e5e5ed63e4670aff1f492e28e2`. The submodules were initialised from local copies at their recorded pins: gptp-processor `c1b61743`, third_party/verilog-axis `48ff7a7e`, and external left uninitialised, as in the source checkout. The protocol-processor gitlink was then staged in two states:

| Staged protocol-processor | `check_py_idiom.py` | `check_cpp_idiom.py` |
|---|---|---|
| `e1d0176` (main, before the fix) | **exit 1**: `unannotated public function 2 > ratchet 0`, `undocumented public function 2 > ratchet 0`. `--list` attributes one of each to `tb/pp_top/fixture_guards.py` and one of each to `tb/pp_top/test_fixture_guards.py` | not needed |
| `0ca1786` (fix head) | **exit 0**: 213 modules, every refusal 0, `unannotated public function: 0 <= 0`, `undocumented public function: 0 <= 0`, every other ratchet at its budget | **exit 0**: 146 translation units, every count 0 |

`git submodule status` showed protocol-processor with a clean ` ` prefix at the staged commit, so the scope helper's pin check was satisfied. `python3 scripts/check_py_idiom.py --selftest` gave `54 checks: 54 PASS, 0 FAIL`. The read-only parent checkout was not modified: it still stages `e0c43b0`. The scratch clone and its logs have been deleted.

## For reviewers

- The docstrings are the substance to review. Check that each one states the contract the code implements and nothing it does not.
- To reproduce the parent gate result, stage protocol-processor at `0ca1786` in a parent clone and run `python3 scripts/check_py_idiom.py` and `python3 scripts/check_cpp_idiom.py`.
- The class `CompilerLocaleTest` has no docstring. Rule 12 counts only functions, so I left the class alone to keep the diff to what the gate refuses.
