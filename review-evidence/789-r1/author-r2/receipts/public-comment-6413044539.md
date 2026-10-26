[A10] **Assignment: executor [A682].** Branch `789-yosys-tool-job` from dev `76de691e` (#788 merged, every job on `ubuntu-24.04`).

Implement the issue's Decision and Acceptance exactly:
- A dedicated Yosys tool job in `rtl-fast`, generated through the generator or template. No hand edit under `.github/workflows/`.
- A cache key that excludes `.github/workflows/*.yml`: the pinned version, the build recipe and the runner image only.
- `yosys-elaboration` `needs:` the tool job and restores the cached tree.
- No timeout raised: every job stays within the 30-minute hosted budget (owner, 2026-10-14).
- The act runner maps the new job.
- R705-1-01's wording fix at `docs/testing/TESTING.md:331`.

Measure on this PR's own hosted runs and record in the PR body:
- the cold tool job's time (the first run of the new key);
- `yosys-elaboration`'s time on a head that edits a workflow (after the tool cache exists).

Re-trigger by a follow-up commit or a re-run as needed. Do not touch any other job's behaviour.

STOP if the cold tool build alone cannot fit 30 minutes on a hosted runner.

