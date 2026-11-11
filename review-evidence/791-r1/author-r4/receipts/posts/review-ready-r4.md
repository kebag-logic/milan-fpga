[A765c] REVIEW READY
Commit: `6a5acf06c80c8a04cef0c5d2b3aeb47252393b8c` (branch `791-split-region-decode`, PR #888 -> `dev-soft-core`): two commits on the manager's sync merge `77e1efa0`, per the round-4 ruling on R826-4. No merge, rebase, force or amend.
Changed:
- F1: `test_ctrl_memory.py`'s mutant planting (`mutated`, `patched`) moved verbatim to the new `sw/litex/ctrl_memory_mutant.py`. The test imports both back, so nothing is dropped and every caller runs unchanged. `test_ctrl_memory.py` is now 972 lines (was 1,003); `scripts/py_idiom.budget` is unchanged.
- F1, found by the gate on the clean clone of the first commit: the idiom gate's `exec` inventory is keyed by file, so the moved `exec` was refused there. `scripts/check_py_idiom.py`'s entry now names `sw/litex/ctrl_memory_mutant.py` in place of `test_ctrl_memory.py`, with the same guard. It is still five entries; no site was added.
- F2: `docs/testing/TESTING.md:792-798` states fifty-nine mutants (`len(test_ctrl_memory.MUTANTS)`). One sentence names the CPU decode arm and `ctrl_memory_decode.py`, which carries twelve of them. S9's mapper sentence is unchanged, and 59 + 3 = the run's 62.
- S1: docstring items 8 and 9 are wrapped at the items' width. Item 7 adds that `ctrl_memory_mutant.py` rebuilds each mutant and puts it in place. The header still says nine things.
Validation (clean clones of this head, all rc 0):
- `check_py_idiom.py`: `long module: 10 <= 10`. `--selftest`: `54 checks: 54 PASS, 0 FAIL`.
- `test_ctrl_memory.py`: 192 ok, 0 FAIL, `RESULT: PASS`. 62 caught mutants; the CPU decode and mapper arms both run.
- Region-decode self-test: `none 0/0, single-mask 4/4, cover 6/6, PASS`.
- Every docs.yml job: 9 of 9 success; `102 steps ran, 0 failed; 6 not run, each with its reason`.
- `git diff --check` against `1d6bf555`: no output.
STOP condition: not met.
- The region test's netlists `88c5cdf9`, `18be4f88` and `57948043` are unchanged, and no netlist was generated.
- The all-fabric compare of `77e1efa0` against this head is identical for every shipped config, apart from comment-only timestamp lines at AX7101.
Acceptance criteria: #791 Required 1 to 3 met; the round-4 items are done.
Open risks/questions: none new.
