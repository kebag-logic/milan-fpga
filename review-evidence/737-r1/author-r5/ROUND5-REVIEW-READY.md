[A614] REVIEW READY

Commit: `e3d25d964b5bbf0187290d0a357c6a6e4c5afd17`
Branch: `737-ci-30min`, from round-four head `08adb21a`. The worktree is clean. Not pushed: origin still holds `08adb21a`, and the coordinating role publishes it.

Round 5 ([6184143571](https://github.com/kebag-logic/milan-fpga/issues/737#issuecomment-6184143571)) is complete. Delta for review: `08adb21a..e3d25d96`, two commits.

**1. Merge dev `f6260253`** (`8db583050`, merge commit, parents `08adb21a` and `f6260253`). Git reported conflicts in exactly the three named files.
- `scripts/suite_shards.py`: the sixteen-worker tables are kept. `gptp_tables` enters the driver-derived inventory and balance whole, as every unsplit suite does: 63 default suites, 80 units. Its figure is 568 s, the larger of its hosted windows: worker 0/6 of dev run 38601263345 at `f6260253`, where that worker passed all its suites. PR #713's run 38538854504 measured 474 s. The provisional 1800 s is refused, because it would put worker 0 at 1922 s.
- `.github/workflows/*.yml` come from the generator only. Dev's six `rtl.yml` edits went into the source template `.github/ci-templates/rtl.yml` by a clean three-way merge: the six-worker matrix, the shard 5/6 `milan_dp` arm and `--expect 6`. The generator previously matched literal `4)` and `--expect 5`. It now derives both from the template's own count and refuses a template whose arm or expectation does not match. Regenerated workflows are byte-identical to `08adb21a`'s, and `--check` passes.
- `docs/testing/CI_WORKFLOWS.md` keeps the sixteen-worker text and dev's #713 facts (the provisional figure, the sixth worker at 115 s overhead, the refresh rule). It adds only the suite's placement; the counts move to 80 units and 63 suites.

**2. Re-projection** (`e3d25d964`). `gptp_tables` lands on worker 3 with `maap__2`, `milan_dp__0`, `chmap_capture` and `tdm_render`. Worker 3 projects 1544 s, 76 s inside its 1620 s bound and 256 s inside 30 minutes before downstream collection. Every regular worker is at 1538-1605 s, margins 15-82 s. Worker 0 (1605 s) and the media-clock exception (2032 s, bound 2160 s) are unchanged. The sixteen rows of the projection table are updated.

**3. Verification at this head**, fresh clones in the shipping image, one 8 GiB container at a time, 16 CPUs, no network:
- Docs-check: all 40 steps plus `wire-accountability` pass. That includes the builder (1482 s), the CI-event contract (2,187 items, 5,212 arms) and the scheduling and union controls (63 parents, 80 units). Peak 4.58 GB, no memory events. docs-check-no-git passes.
- rtl-fast: all 20 steps across twelve jobs pass, scope `rtl=true`. Peak 6.16 GB, no memory events.
- The runner contract gate passes both invocations (102 s), read-only, no socket. `scripts/act_ci.py` is unchanged, SHA-256 `f968f676…895c`, so no STOP was needed.
- Generated worker 3/16 passes all five units, `gptp_tables` among them, with 5,518 checks. Shard step 1121 s.
- Union proofs including `gptp_tables`: the collector and pieces self-tests on the real inventory pass. Planted controls refuse a missing duration, the provisional figure, and its log missing from worker 3, moved to worker 0 or duplicated. The unchanged tally refuses the set without it.
- Generator controls: the round-4 literal generator on the new template emits a stray shard-5 arm and `--expect 6`, and the contract check misses it. The derived generator refuses a missing arm, a stale arm index and a mismatched expectation.
- Dev changed the builder driver that elaboration divides, so the legs ran again. The unsharded reference, leg 0 and leg 1 pass. Their union equals the unsharded run, with a per-gate verdict digest identical to round 4's, and the production aggregate accepts the receipts.
- Host gates at the clean head pass (26 of 26), including generator freshness, the CI-event check, every scheduling, evidence and manifest self-test, and the em-dash checks against `f6260253` and `08adb21a`.

Acceptance criteria: round-5 items 1-3 are met, with the evidence above. The CI-event contract changed only through the merge (dev's six-worker literals); the author changed no CI assertion.

Open risks/questions:
- The merged #671 workload lengthens gates that the docs and elaboration workers carry. At dev `f6260253` the hosted docs builder took 1400 s (1065 s at `7032bca5`), the saved-state writer 410 s (119 s) and the elaboration builder 1763 s (1441 s).
- Docs: by `CI_WORKFLOWS.md`'s own method (the larger, local builder figure, 1482 s), `docs-gates-1` projects 1602 s, 18 s inside its bound. The docs workflow then projects about 31.2 minutes, above 30 (29.8 with the hosted figure).
- Elaboration, re-measured at this head (lone unsharded run 1434 s), projects workers of 1473 s and 1353 s, about 29.1 minutes.
- This round does not divide the docs builder, and `CI_WORKFLOWS.md` keeps its `7032bca5`-based docs and elaboration rows, as the round's documentation limit requires. Whether to divide the docs builder is for the coordinating role.
- These are projections, not hosted times. This is an author handoff, not a review verdict.
