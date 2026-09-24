[A251] Separate historical linear inclusion from optional current retention

Closes #514

## Status

Round 2 is ready for independent re-review at `b0347a4fd668f8d40bdf40a142ac0ea70167acd1`. The round adds tests only. Publication of this local head and the remaining merge workflow are pending.

## Description

An exact linear replay followed by a revert still returns `contained/0`, preserving the decided historical-inclusion policy. Add `--current-retention` to request a separate `retained` or `UNKNOWN` result using #423's unchanged raw-entry and no-op three-way merge criterion. Diagnostics and the containment documentation identify the claim each result makes.

The optional arm requires a nonempty source-only linear range and distinct exact replays. Ancestry-only, squash-only and merge-shaped histories remain unsupported by this arm. Unmeasurable or unproved retention returns `UNKNOWN/1`; declared supersession intent does not supply proof.

## Round 2

Address the Tests findings in [R292-1](https://github.com/kebag-logic/milan-fpga/pull/552#issuecomment-5811949459) and [R293-1](https://github.com/kebag-logic/milan-fpga/pull/552#issuecomment-5811996262):

- Exercise an exact replay with an empty source delta and an H measurement failure. Both require optional `UNKNOWN/1` while preserving the default landing result.
- Assert that the ancestry `contained` line names historical inclusion and disclaims current retention, with and without the option.
- Assert that STRANDED and UNKNOWN landing targets emit no `retained` line or optional retention result.
- Assert that positive `retained` lines identify current raw retention and historical replay.

Only `scripts/merge_containment_selftest_linear.py` changes in this round. Existing expectations, production behavior, diagnostics and parsing remain unchanged. The optional parsing suggestion was not taken. Re-review of the corrected head is required.

## How to reproduce

Run unchanged fixture 30 and `linear-patch-fallback`: both remain `contained/0`. Adding `--current-retention` reports `UNKNOWN/1`, naming `mod.txt` and `linear` respectively. The baseline reproductions are recorded in the linked reviews and their immutable evidence packets.

The new empty-delta fixture replays a change and its revert exactly. Its source endpoint equals its starting tree, so optional current retention must be unmeasurable. The H-failure fixture has exact current paths, allowing default landing to pass before an injected Git enumeration failure reaches the optional arm.

## How to validate

Run `python3 scripts/check_merge_containment.py --selftest` and the `linear_retention_cases` entry point through the existing fixture harness. Run the docs gate in both discovery modes, `check_em_dash` against `3d2f3e3131c9db5898e1db9dd3e2a35149843109`, documentation style, TOC, paths, Python idiom and `git diff --check`.

Reapply both reviewers' unchanged mutant sets. M01, M09, M10, M12 and their R293 equivalents must fail, as must every previously killed mutant. The handoff contains the before/after tables, unchanged script hashes, raw gate logs and preservation comparison. Self-test results are evidence for re-review, not approval.

## DoD

- Historical verdicts and all existing test expectations preserved.
- Optional retention proof, claim-naming diagnostics and authoritative wording implemented.
- Assigned Round 2 measurement and diagnostic coverage added; required mutant sensitivity demonstrated.
- Assigned local gates pass. Independent re-review and the remaining hosted, candidate, merge and post-merge workflow are still required.
