Original file: <scratch>/budget/final/held-egress-vs-base.md
Original size: 2246 bytes
Original sha256: 36aa35c755d7b01535f7a52da885f7d3b6ed49db515262955481166f1253a96f

# The seven held-egress rows (`backlog-owed`), the base 70f4056f against the final image

The final image is the one every head from 77c1aad7 to 7cfb8a04 builds (identical ctrl_app.elf). Each figure is the
harness's own grade of the `backlog-owed` group, in ms to 10 ns: the base by `--groups backlog-owed` on a clean clone
of 70f4056f, the final from the full regrade. The 60 ms egress hold is the scenario's; the service is the rest.

## 1x1/1if (no ledger: egress_ledger.py refuses the point)

| Row | Base, ms | Final, ms | Difference, ms | Service behind the hold, base -> final | Ledger, ms |
|---|---:|---:|---:|---|---:|
| `backlog.owed.if0` | 62.90483 | 63.04098 | +0.13615 | 2.90483 -> 3.04098 (+4.7 %) | - |
| `backlog.owed_behind0.if0` | 63.09229 | 63.22755 | +0.13526 | 3.09229 -> 3.22755 (+4.4 %) | - |
| `backlog.owed_behind1.if0` | 63.27978 | 63.41324 | +0.13346 | 3.27978 -> 3.41324 (+4.1 %) | - |
| `backlog.owed_behind2.if0` | 63.46639 | 63.59885 | +0.13246 | 3.46639 -> 3.59885 (+3.8 %) | - |
| `backlog.owed_behind3.if0` | 63.65221 | 63.78447 | +0.13226 | 3.65221 -> 3.78447 (+3.6 %) | - |
| `backlog-owed.service.acmp.last.if0` | 62.00208 | 62.14475 | +0.14267 | 2.00208 -> 2.14475 (+7.1 %) | - |
| `backlog-owed.service.aecp.last.if0` | 61.73581 | 61.88694 | +0.15113 | 1.73581 -> 1.88694 (+8.7 %) | - |

## 8x8/1if (graded by the egress ledger, PR #914 8883d499)

| Row | Base, ms | Final, ms | Difference, ms | Service behind the hold, base -> final | Ledger, ms |
|---|---:|---:|---:|---|---:|
| `backlog.owed.if0` | 63.51268 | 63.54603 | +0.03335 | 3.51268 -> 3.54603 (+0.9 %) | 63.86 |
| `backlog.owed_behind0.if0` | 63.79938 | 63.83736 | +0.03798 | 3.79938 -> 3.83736 (+1.0 %) | 64.1 |
| `backlog.owed_behind1.if0` | 64.02679 | 64.07120 | +0.04441 | 4.02679 -> 4.07120 (+1.1 %) | 64.36 |
| `backlog.owed_behind2.if0` | 64.27343 | 64.32965 | +0.05622 | 4.27343 -> 4.32965 (+1.3 %) | 64.61 |
| `backlog.owed_behind3.if0` | 64.51225 | 64.57842 | +0.06617 | 4.51225 -> 4.57842 (+1.5 %) | 64.86 |
| `backlog-owed.service.acmp.last.if0` | 62.38023 | 62.38865 | +0.00842 | 2.38023 -> 2.38865 (+0.4 %) | 62.62 |
| `backlog-owed.service.aecp.last.if0` | 62.03000 | 62.02430 | -0.00570 | 2.03000 -> 2.02430 (-0.3 %) | 62.16 |

