https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6192211250 2026-10-15T12:37:24Z

[A10] **Round 8 for PR #739: exempt the vendored act patch from whitespace checks. Decision: the manager makes this one-line change.** At `fe2e2a54`:

- R636-7 is **POSITIVE** ([6191436051](https://github.com/kebag-logic/milan-fpga/pull/739#issuecomment-6191436051)).
- The runner is repinned to `7ff18c6a`. The candidate `23869591` (dev `65617779` + `fe2e2a54`) was built for the merge.
- **Finding (manager, merge bar).** The candidate's builder bank failed `git diff --check 65617779 23869591`, with 37 whitespace findings, all in `ci/act/fail-fast.patch`. This PR adds that file (`e09a7f9c`). It is a vendored diff for the act build, and its leading and trailing whitespace is content, so stripping it would break the patch. `.gitattributes` exempts only `sw/litex/patches/*.patch`. Every other path in the PR is clean against both `f6260253` and `65617779`. The round-5 candidate (`5687e34c`) failed the same gate, and no review caught it.
- **Fix:** `30f7b0ef`, which adds `ci/act/*.patch -whitespace` to `.gitattributes`. `git diff --check 65617779 30f7b0ef` returns rc 0, and `check_hygiene.py` and `check_todo_ownership.py` pass. No other file changes. A one-line change does not justify an author round under the token rules.

Under the owner's single re-reviewer rule, R636 re-checks this one-line delta (`fe2e2a54..30f7b0ef`). Then I rebuild the candidate and run the act replay on the repinned runner.

