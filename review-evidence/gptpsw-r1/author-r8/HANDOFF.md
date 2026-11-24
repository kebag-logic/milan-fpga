STATUS: DONE, REVIEW READY. ETA: none (complete 17:55 CET 2026-11-24).

# PR #966 round 3b handoff (R883-5-F1)

Head: `e05f800a6ae3ae20ed616b58e4a36b1ceb6fd31d`. It is one local commit on `0acf24d9`. **Not pushed.** The lane
worktree is clean and one commit ahead of `origin/884-gptp-firmware`.

- **The fix.** It touches two lines, both in tests, and both change together:
  - The assertion at `test_aecp.cpp:4681` and the campaign needle at `aecp_face_mutants.py:31` now say
    "AS_CAPABLE is the firmware gPTP owner's".
  - That is the tree's existing wording (`docs/design/GPTP_SOFTWARE.md:153`). Neither string contains a #259 term.
  - The needle is still a substring of the assertion.
- **The gates at `e05f800a`:**
  - `check_baremetal_only.py --check` passes with rc 0 and 0 findings, and `--selftest` passes.
  - All 42 run-steps of docs-gates-0 pass with rc 0.
  - The full AECP campaign catches 388/388 with 0 escaped. The leak row is caught on the new words only, and the
    old words would no longer catch it.
  - The unplanted AVB test passes at 1 and 2 interfaces.
- **Not run:**
  - The four firmware shards, because no firmware product input changed.
  - fw_coverage.
  - docs-gates-1/2, act and the hosted runs.
- **Manager duties:**
  - Push the branch.
  - Run hosted and act at the new head. docs-gates-0's bare-metal step should now be green.
  - Arrange a delta re-review covering at least Conformance, Tests and Docs.
  - R883-5-S1/S2 and R883-4-R1 to R3 are untouched.

Details are in `REVIEW-READY.md` and the receipts in `receipts/INDEX.md`. Scratch files are in
`/data-2/milan/tmp/opt-a837-r3b`.
