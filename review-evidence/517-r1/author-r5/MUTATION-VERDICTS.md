# Targeted mutation verdicts

Source: public reviewer scripts from evidence commit `f0ff6b8f51b6f1da6b1f9d37f3bf2feb9f369576`, run unchanged.

| Probe | Case | Unit result | Backpressure result | Reported verdict |
|---|---|---|---|---|
| Internal | no-exclusion | 1 | 0 | KILLED |
| Internal | group-reverse-order | 1 | 1 | KILLED |
| Internal | no-independent-overlap | TIMEOUT | 0 | KILLED |
| Internal | mk-drop-crflic | 1 | 1 | KILLED |
| Internal | mk-swap-order | 1 | 1 | KILLED |
| Internal | mk-default-one | 1 | TIMEOUT | KILLED |
| Internal | mk-ignore-errors | 1 | 0 | KILLED |
| Internal | drain-blocking-write | 0 | 1 | KILLED |
| Internal | drain-ignores-signals | 0 | 1 | KILLED |
| Internal | final-drain-waits | 0 | 1 | KILLED |
| Internal | fd-flags-not-restored | 0 | 1 | KILLED |
| External | M03-no-exclusion | FAIL | PASS | KILLED |
| External | M04-group-order-reversed | FAIL | PASS | KILLED |
| External | M15-blocking-stdout | PASS | FAIL | KILLED |
| External | M16-final-drain-waits | PASS | FAIL | KILLED |
| External | M17-flags-not-restored | PASS | FAIL | KILLED |
| External | M28-make-drop-prune | FAIL | FAIL | KILLED |
| External | M32-make-crflic-exclusive | FAIL | PASS | KILLED |

The reviewer scripts call any nonzero exit or guard timeout KILLED. The no-independent-overlap result is a guard TIMEOUT with no assertion catch. The default-one mutant has a unit assertion failure and a backpressure guard TIMEOUT. All other selected mutants produce assertion failures.

The original runner blob `761ec858` gives 28 FAIL, exit 1: 24 blocked-cancellation assertions and four missing replay-file failures. After restoration, unit controls pass 17/17 and backpressure controls pass 28/28.
