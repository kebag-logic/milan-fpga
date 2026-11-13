[A773] STEP 0

Head: `ccb47e39a534f4c8d02af826fa50fcd6578a38de` (`894-tiers`, dev-soft-core `cec88385` merged; tree unchanged from `eebc37a3`).

**What-if (ruling issuecomment-6857835707, item 3).** Model only, no firmware change. The rows at 1x1/1if are the built design's (`rows_tiers.solve`, `rows_tiers.BUILT`, the 800 us slice). Every input is the tree's, at the pin column the flip check reads, except three:
- the pace P;
- the polls' base;
- ACMP's item.

At the tree, those are P = 8, a base of 205 us and an ACMP item of 120 us in that column (125 in the donor column), giving txL 47.25 ms and the last queued notice 137.79 ms. The other merged costs stay as they are: SRP record 280, retained retry 280, centisecond 150, walk 35, and builds 1,010 / 430 us.

txL in ms (bound 40) at each P. The last queued notice in ms (bound 125) does not depend on P. **Bold** marks a pair that holds both rows.

| Base, us | ACMP item, us | P = 8 | P = 9 | P = 10 | P = 11 | Last queued notice |
|---:|---:|---:|---:|---:|---:|---:|
| 155 | 35 | **39.36** | **39.36** | **38.65** | **38.65** | **116.45** |
| 155 | 80 | 43.88 | 43.17 | **39.55** | **39.55** | **122.74** |
| 155 | 125 | 44.87 | 44.16 | 44.16 | 42.62 | 127.13 |
| 180 | 35 | **39.86** | **39.86** | **39.15** | **39.15** | **121.85** |
| 180 | 80 | 44.43 | 43.72 | 43.72 | 42.20 | 126.51 |
| 180 | 125 | 46.79 | 44.71 | 44.71 | 43.15 | 135.65 |
| 205 | 35 | 43.99 | 43.28 | 39.65 | 39.65 | 125.60 |
| 205 | 80 | 44.98 | 44.27 | 44.27 | 42.73 | 134.99 |
| 205 | 125 | 47.37 | 47.37 | 45.78 | 43.67 | 141.79 |

**10 of the 36 combinations hold both rows:**
- a base of 155 or 180 us with ACMP's item at 35 us, at every P from 8 to 11;
- a base of 155 us with ACMP's item at 80 us, at P = 10 and 11.

R4L stays within its 240 ms at every one of the 36 (187.85 to 233.27 ms). No combination with the base at 205 us holds the last queued notice: with ACMP's item at 35 us it is 125.60 ms.

So round 7 continues with the levers of item 4 (#908). The target is a base of at most 180 us and ACMP's item near 35 us, both of which #810's merge raised. Not waiting for an answer.
