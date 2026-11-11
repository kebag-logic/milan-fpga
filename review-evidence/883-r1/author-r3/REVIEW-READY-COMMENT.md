[A768] REVIEW READY
Commit: `3c58b143eac812d173b4326423c030b65ec63f9a` (round 3, under the ruling issuecomment-6809058443; branch `883-adopt-processor-801ef228`, from dev `46c971fa`; live dev `fa6c094b` merges cleanly; nothing pushed)

Changed since `e18c8225`, two new commits and no rewrite. No image, RTL, firmware or pin change.
- `8f3735d7`, F1 (R831-1 and R832-1): `scripts/check_cpp_idiom.py:269-271`.
  - The multi-declarator rule now reads a balanced one-line `{...}` initialiser up to three braces deep as one declarator's text, and the comment states that limit. A comma beside such an initialiser still separates declarators.
  - Eight arms at `:705-712`. One declarator with flat, once-nested or twice-nested braces gives 0. Two declarators beside flat, `{1}`-style, once-nested (either order) or twice-nested braces give 1.
  - The file stays at 1,000 lines: three wrapped arms in the same function are each joined onto one line.
- `3c58b143`, residue R2 (= R832-1 R1): `docs/testing/TESTING.md:357` now reads "the six gate mutants".
- PR body, residue R831-1 R1: the #495 row 6731336971 states its four items.
  - Items 3 (Makefile) and 2 (`TESTING.md`) are taken.
  - Item 1 (`SUBMODULES.md:813`) stays open on #495.
  - Item 4's note is rewritten here but keeps the form, now "+29 slices (80)", so it stays open on #495.

Validation at this head, on a clean clone:
- `python3 scripts/check_cpp_idiom.py --selftest`: 83 / 83, rc 0. The tree scan reads `multi-declarator declaration: 0 <= 0`.
- Planted back, each one line replaced and then restored:
  - dev `46c971fa`'s pattern fails the three "a brace initialiser's commas separate elements, not declarators (#495)" arms;
  - `e18c8225`'s flat-brace pattern fails the three nested two-declarator arms;
  - a one-nested-level pattern fails the three-deep arm.
- The reviewers' probes, unchanged, run with `-I`:
  - `probe_cpp_multidecl.py`: the head verdict equals `real>1` on all nine rows;
  - `probe_cpp_edges.py`: 1 for the nested two-declarator line, 0 for the nested single;
  - `probe_cpp_old_regex.py --selftest`: fails the brace-initialiser arms by name.
- docs.yml, all five jobs, on the pull_request merge commit with live dev: 64 steps rc 0, 33 not run with a reason, 0 failing. The `check_cpp_idiom.py`, `check_py_idiom.py` and `measure_*` steps are among them.
- `git diff --check 46c971fa HEAD`: rc 0.
- The two changed files are read only by docs.yml steps. The rest of the evidence stands from `e18c8225` (issuecomment-6806761644).

Acceptance criteria: items 1 to 5 are met, as at `e18c8225`. F1 is fixed with arms that fail when each earlier pattern is planted back.

Open risks/questions:
- One probe edge reads 0 at this head and at dev alike: `int a = f(1, 2), b;`. Both patterns exclude parentheses by design, so `f(a, b);` is never read as a declaration. It is not F1 and not changed here.
- Under the ruling, a delta reviewer per role re-covers Tests and Robustness at this head.
