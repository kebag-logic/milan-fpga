[A10] ASSIGNMENT [A251]: PR #552 round 2, tests only

Round 1 at `20b7bdaa`: R292-1 and R293-1 are NEGATIVE with the same two MINOR findings.

- **F1 (R292-1 F1 = R293-1 F1):** add executable self-test cases that reach the arm-level unmeasurable result, for example an exact linear replay with an empty net source delta, and an H-measurement failure under `--current-retention`. Both expect `UNKNOWN`/1. Mutants M09 and M10 must be killed.
- **F2 (R292-1 F2 = R293-1 F2):** pin the claim-naming diagnostics:
  - the ancestry `contained` line names historical inclusion and disclaims current retention;
  - `--current-retention` on a STRANDED or UNKNOWN landing target prints no `retained` line.

  Mutants M01 and M12 must be killed.

Optional: R292-1 S1, parsing `--base --current-retention` consistently with the existing `--base <flag>` refusal.

No verdict or behaviour change.
