[A193] Annotate and document the two public pp_top fixture-guard functions

Closes #104

## Summary

The parent's Rule 12 gate (`scripts/check_py_idiom.py`) refused two public functions in this repository. Each now has a complete PEP 484 signature and a docstring that states its contract:

- `tb/pp_top/fixture_guards.py` `main() -> int`: reads its arguments from the command line, checks the four SRP VID fixture cases against the real bench under `LC_ALL=C`, and returns 0 when all four pass or 1 on a mismatch, after printing the compiler output. It raises `CalledProcessError` if the root query or model generation fails.
- `tb/pp_top/test_fixture_guards.py` `CompilerLocaleTest.test_compiler_environment_and_arguments(self) -> None`: states what the test requires.

No statement or branch changed. With the new return annotations and docstrings removed, both files' ASTs are identical to main `e1d0176`.

## Verification

This repository, at the fix head:
- `make -C tb/pp_top`: unit test OK, `fixture guards: 4 cases PASS`, `1411 checks: 1411 PASS, 0 FAIL`. The `make fixture-guards` output is byte-identical before and after the change. The only difference in unittest's `-v` report is that it now prints the docstring's first line under the test id.
- Deleting the `LC_ALL=C` override on a scratch copy still fails the unit test (`failures=2`).
- `make check`, `check-links.py`, `check-matrix.py`, `render-wavedrom.py --check`, `make stale`, `gen_matrix.py --check` and `lint_hdl.sh` all pass. `run_suites.sh` over every suite was not run, because only `tb/pp_top` Python is touched.

Parent consumer: a private clone of the parent at `574c29fa`, with protocol-processor staged:
- at main `e1d0176`, `check_py_idiom.py` exits 1 with `unannotated public function 2 > ratchet 0` and `undocumented public function 2 > ratchet 0`, which reproduces the issue;
- at this head `0ca1786`, `check_py_idiom.py` exits 0 (both ratchets `0 <= 0`), `check_cpp_idiom.py` exits 0, and `check_py_idiom.py --selftest` gives 54/54 PASS.
