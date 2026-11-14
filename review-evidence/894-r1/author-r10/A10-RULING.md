[A10] **Round 10 of #894: the three MINOR findings at 5b264bf2.** This is a maintainer-delegated assignment, with no new decision. Both reviewers confirm everything else in round 9.

1. **R837-4-1, as its report requires.**
   - The `_Static_assert` bounds the declared slot array by the index range `place()` forms: `MAP_FIRSTS × MAP_CHANNELS`. Keep the floor and the domain as separate macros.
   - Add a compile-time control: a planted undersized table, at a configuration where it would overflow, must be refused.
   - The two document sentences say what the assertion holds, and say separately that the 256-slot floor is a layout choice (#909).
   - No image or behaviour change: sha256 receipts for every image against 5b264bf2.
2. **R838-4-F1.** `SPLIT_CONTROL_MEMORY.md`'s current row table and summary take the head's figures from `flip_grade.py --check --point 1x1/1if`. Any historical figures stay marked as a named head's.
3. **R838-4-F2.** The PR body's validation command becomes `'Core.*Map*:Core.Every*'`, which runs 13 tests.
4. **The RESIDUE items of both reports,** absorbed in the same pass.

**Gates:** the firmware suite, coverage, the AECP campaign, the docs gates, the image sha256 check and the 1x1/1if flip check. No full sweep is needed if every image is byte-identical. Otherwise, the full pass once.

**Reviews:** both reviewers, as delta reviews.
