https://github.com/kebag-logic/milan-fpga/issues/734
## Problem

The scope steps of `rtl.yml`, `rtl-fast.yml` and `elaborate.yml` classify a PR with a two-argument `git diff <recorded base> <head>`, which compares trees. When dev has moved since the PR's merge base, that diff also contains *other* PRs' changes in reverse. A docs-only PR is then classified as RTL-relevant and runs the full RTL suite, hosted and in the act replay (which mirrors the scope steps on purpose; see `build_event` in `scripts/act_ci.py`).

Measured on PR #725 (B16, two documentation files) at head `f1b2489f` against recorded base `49da9fd9`:

| Diff | Files | `ci_scope.py` |
|---|---|---|
| two-argument `49da9fd9 f1b2489f` | 64 (including `.github/workflows/rtl-fast.yml`, `scripts/…`, `gptp-processor`) | relevant: full suite |
| merge-base `49da9fd9...f1b2489f` | 2 (`docs/findings/…`) | documentation only |

The act replay for that docs-only PR ran 23 jobs for 3 h 48 min.

## Change

Classify the PR's own changes: the scope steps diff from the merge base (`<base>...<head>`), hosted and in the act replay alike. The equality between them, which `act_ci.py` keeps on purpose, is preserved.

This is safe because the composition is validated elsewhere. The merge train builds the current-dev candidate and runs its builder and full native banks before every merge, so RTL interactions with dev changes are still caught before the merge lands.

## Acceptance

1. All three scope steps use the merge-base diff, and `docs/testing/CI_WORKFLOWS.md` states the rule and why it is safe (the candidate banks).
2. `act_ci.py`'s replay classifies the same file set as hosted. Its `build_event` docstring and selftest cover a stale-base, docs-only PR, which must come out docs-only in both.
3. Controls:
   - a docs-only PR on an older base is classified documentation-only;
   - an RTL change on an older base is classified relevant;
   - a submodule pointer is still always relevant;
   - an empty diff still fails safe.
4. The `ci_scope.py` selftest and the runner contract gates pass.
5. Two reviews; the act replay; hosted CI green.

Not in scope: parallel act slots, which need only the existing `--slot-root` and a disk.
