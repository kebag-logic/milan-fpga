[A10] Round 4 scope, amended after R306-2 and R307-2 (both NEGATIVE at `224ec0e9` on the same two findings). This replaces 5826321018. [A299] continues.

1. **R306-2 F1 (BLOCKER) = R307-2 F1 (MAJOR):** `tb/verilator/milan_dp/README.md:488` links into the processor submodule by relative path, which the hosted docs gates (no submodule checkout) cannot resolve. Use the repository's convention for submodule references: a commit-pinned GitHub blob URL at `990f9652`, as at the same README's :728. Keep the `#fig-06-lineage` and `#fig-05-settled` fragments and name F06.13 and F05.5 in the text. Verify with `docs_check.py` run in a `git archive` of the new head, where no submodule content is present: 0 findings.
2. **R306-2 F2 = R307-2 F2:** state the gsi-mutants campaign size as eight arms, eight elaborations and nine runs everywhere: `CHANGELOG.md:57`, the `tb/verilator/milan_dp/Makefile:451-452` comment, the `scripts/measure_test_evidence.py:619-620` disposition, and `docs/testing/TESTING.md:267` if it reads as campaign size.
3. Change nothing else. Gates: `gen_toc.py --verify-anchors`, `gen_toc.py --check`, `docs_check` in both modes plus the `git archive` run, `check_doc_paths`, `check_em_dash --base c266432d`, `measure_test_evidence.py --check` and `--selftest`, `check_py_idiom`, and `git diff --check`.

Review: delta reviews by [R306] and [R307].

