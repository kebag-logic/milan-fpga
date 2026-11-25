Status: REVIEW READY. Both enabled shapes meet the #818 floor at the reviewed head 09201d35; no code change.
ETA: complete; no author jobs remain.

[A826] Round 8, issue #979 / PR #987. Head 09201d35d7ea720b3ba205da185ba35c159ec24a on pf-loopbram-1 (unchanged), target dev-soft-core.
No commit was made. Nothing was pushed or posted, and the bench was not used.

## Routes at 09201d35 (hdl tree 244c59e0, dev-soft-core 5de21ff3 merged in)

| Shape (enabled) | Selected of three | Setup / hold, worst of four corners | LUT | FF | BRAM tiles | Slices | DSP |
|---|---|---:|---:|---:|---:|---:|---:|
| 1x1 | AltSpreadLogic_high | +0.147 / +0.036 ns | 32669 | 42821 | 82.5 | 14225 | 13 |
| 8x8 | AltSpreadLogic_high | +0.309 / +0.036 ns | 48485 | 54965 | 110.5 | 15792 | 13 |

Others: 1x1 ExtraPostPlacementOpt +0.125 (PASS) and ExtraTimingOpt +0.020 (below +0.030); 8x8 ExtraPostPlacementOpt +0.117 / hold +0.015 (PASS) and
ExtraTimingOpt +0.049 (PASS). Zero failing endpoints, zero routing errors and every routable net routed on all six. The recipe equals rounds 4 and 5.
The ordinary enabled 8x8 export is refused (70.5 tiles against 56; +11.0 over the 59.5 ledger entry, S14 debt), the ordinary 1x1 export is accepted.
Each receipt is bound to the head, the configuration and the input hashes; the inputs were unchanged after the last route.

## R910-4-F1 and R909-6-N1

Closed by the author with the receipts; each is cleared only by its reviewer. R910-4-F2 is corrected here and in REVIEW-READY.md and PR-BODY.md:
R909-5 POSITIVE at 1516b2ffe321337858389ec8e42897f8a80644bb; R910-3 POSITIVE at 9acb9b828b29aba71bd51303a4836f86c2278267.
The round-7 wording, which attributed R910-3 to 1516b2ff, came from the round-7 brief. Round-7 files are unchanged.

## For the manager

- These are the reviewed head's routes. If your merges move dev-soft-core before this PR merges, the merge candidate re-routes both shapes (the PR body says so).
- The PR body's route section is replaced; the rest is round 7's. It still needs publishing over the PR's current body.
- Not added: hosted or local acceptance evidence. Round 7's "Not run" list stands, as does the 27th-worker confirmation.
- Residue R909-5-R1 and R909-6-R1 are unchanged and stay with you. No docs page states route figures, so no docs commit was made.
- Scratch: `/data-2/milan/tmp/loopbram-a826-r8` (0.7 GB) holds the projects, checkpoints and drivers, reusable for a candidate re-route. Nothing was removed this round, so `disk-cleanup.log` has no entry.
  `sw/builder/out/loopbram_measure_r8` (git-ignored) is the generated tree the routes read.
- Earlier scratch `loopbram-a826-r3*`, `-r4*`, `-r5`, `-r6` is about 30 GB on a filesystem at about 95%. It can be removed, if you decide, after this round's review.

[Round-8 delta](REVIEW-READY.md) · [Full PR body](PR-BODY.md) · [Receipts](receipts/INDEX.md)

REVIEW READY 09201d35d7ea720b3ba205da185ba35c159ec24a
