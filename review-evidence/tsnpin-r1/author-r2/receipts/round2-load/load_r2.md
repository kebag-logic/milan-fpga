| Point | Load, committed pin column (70936b77) | Load, committed donor column (tsn-c-stack#32) | Load, 715589c with the redelivery (this measurement) | Ceiling | Verdict | Largest terms |
|---|---:|---:|---:|---:|---|---|
| 1x1/1if | 0.463 | 0.450 | **0.483** | 0.70 | within | srp 0.156, rec.acmp 0.053, ticks 0.047, item.aecp 0.046, rec.aecp 0.041, item.acmp 0.037 |
|  | costs moved against the committed donor column: item.acmp 35 -> 120, item.retained 250 -> 260, record.srp 250 -> 260 | | | | | |
| 8x8/2if | 0.815 | 0.719 | **0.767** | 0.75 | OVER | srp 0.219, item.acmp 0.063, item.aecp 0.062, rec.acmp 0.061, ticks 0.059, timers 0.057 |
|  | costs moved against the committed donor column: base 245 -> 250, item.acmp 40 -> 165 | | | | | |
FINDING 1x1/1if: measured item.acmp 10974 cycles over poll_grade.py's 65 us
