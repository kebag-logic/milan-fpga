# Connected probe results

The archived runner leaves these mutant rows informational. This packet also
checks the stricter Round 2 assignment expectations explicitly.

| Variant | Required | Observed | Failures | Evidence |
|---|---|---|---:|---|
| `clean` | PASS | PASS | 0 | [clean__talker.log](receipts/R302/clean__talker.log) |
| `rx_no_detection` | FAIL | FAIL | 23 | [rx_no_detection__talker.log](receipts/R302/rx_no_detection__talker.log) |
| `jump_removed` | FAIL | FAIL | 15 | [jump_removed__talker.log](receipts/R302/jump_removed__talker.log) |
| `lower_bound_removed` | FAIL | FAIL | 15 | [lower_bound_removed__talker.log](receipts/R302/lower_bound_removed__talker.log) |
| `servo_ignores_valid` | FAIL | FAIL | 5 | [servo_ignores_valid__talker.log](receipts/R302/servo_ignores_valid__talker.log) |

Clean quiet traffic observes 550 post-edge artifacts and zero sampled invalidity.
The same pre-edge observer supplies the step-case withholding assertion.

The clean unchanged `lag_sweep` passes 36 checks. Its no-detection counterpart
fails 13 checks. Both unchanged talker-only signs pass clean and fail without
receiver detection.

The runner source is unchanged; its HEAD binding alone selects the candidate.
`probe-input-identity.txt` proves the same targeted inputs at the final head.
`unchanged-probe-hashes.sha256` proves all archived probe sources unchanged.


The unchanged R303 campaign completed all 23 cases, rc 0: four clean
controls pass, all seventeen expected mutant kills occur, and both
informational ignored-tu cases pass as expected. See
[the R303 summary](receipts/R303/SUMMARY.txt).
The revised connected harness rejects jump removal (15 failures), combined
detector removal (22), ignored validity (5), and forced validity (11).
The unchanged listener-first probe passes clean (19/0), and rejects jump
removal (3), combined detector removal (6), and ignored validity (1).
