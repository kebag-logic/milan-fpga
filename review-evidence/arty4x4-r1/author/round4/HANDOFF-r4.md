Status: REVIEW READY (14:17). The five decisions are applied and committed, #1004 round 11 is merged, and every gate passes at `12ab4b189`:
- firmware ×4, boots, region, memory, host arms, coverage ratchet;
- service self-test 323/323, ledger and Arty grades;
- builder suite (gate 11 NOT RUN, reason stated), docs and idiom.

The 1x1 and ALINX images are byte-identical, and so is the routed 4x4 ELF.
ETA: done. Next: independent review of the PR (stacked on #1004), and the bench (correction pair at 100 MHz).

[A863], round 4. Worktree `$LANES/arty-4x4`, branch `arty-4x4-1127`, head `12ab4b189f54439cd126f677b906a19835d7f32a`. Nothing pushed or posted; no bench, no flash.

## Round-4 commits

- `5e298db8e` merge of #1004 round 11 (`c0b625d1`): two wording conflicts (harness README, `arty_grade.py`) resolved keeping this lane's per-point code with round 11's words.
- `9e8ca43bd` the `arty-4x4` point's own held-egress ledger by #878's rule (#1020's ruling as precedent): figures 61.65 to 63.50 ms against measurements of 61.56471 to 63.32736 ms, side by side in section 15; self-test extended (24 mutants).
- `12ab4b189` FR-CLK-05: the 4x4 image's correction pair at 100 MHz recorded as owed to a measurement on the board.

## Decisions, as applied

1. Held-egress ledger: done, census 4 grades PASS against it (1655 instances).
2. Bind bounds 550 ms / 4 saves: confirmed, unchanged.
3. #1004 round 11 merged; every existing image's ELF and builder output byte-identical; the 4x4 ELF is the routed `1b8066e4…`.
4. Latency pair: owed, in FR_NFR and the PR body.
5. Thin margins: recorded as measured in REPORT.md section 2 and the PR body.

Gate 11 is NOT RUN. Its oracle is a v1-era place report (`build_arty_eto_milanfinal48`) that is not on this host, and no commit for it is recorded.

Scratch `$VALIDATION_STORAGE/arty4x4-a863` about 8.1 GB (three gate build trees removed, logged). One untracked gate artifact (`dispatch-build/`) was removed from the checkout, logged.

Files: REPORT.md, REVIEW-READY.md, PR-BODY.md (base `dev-soft-core`, stacked on #1004), receipts/INDEX.md.

REVIEW READY 12ab4b189f54439cd126f677b906a19835d7f32a
