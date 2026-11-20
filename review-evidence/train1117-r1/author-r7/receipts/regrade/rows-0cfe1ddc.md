### 1x1/1if

| Row | Figure, ms | Bound, ms | Margin, ms |
|---|---:|---:|---:|
| R4 | 13.43 | 20 | -6.57 |
| R5 | 76.55 | 90 | -13.45 |
| R6 | 74.05 | 90 | -15.95 |
| first | 14.75 | 20 | -5.25 |
| last | 137.97 | 140 | -2.03 |
| R4L | 203.58 | 238 | -34.42 |
| ACMP | 29.93 | 30 | -0.07 |
| ADP | 28.14 | 30 | -1.86 |
| MAAP | 28.23 | 30 | -1.77 |
| tx | 34.30 | 49 | -14.70 |
| txL | 48.89 | 49 | -0.11 |

- findings: 0 OVER line(s)

### 8x8/1if

Load 0.739 against its ceiling 0.75 (1.00x).

| Row | Figure, ms | Bound, ms | Margin, ms |
|---|---:|---:|---:|

- HELD 8x8/1if: THE TRANSMIT's figure CTRL_LOOP_TX_MS 75 ms against its tx row by every source 76.81 ms (tx_held; the hold-off adds the figure)
- findings: 1 OVER line(s):
  - OVER 8x8/1if: CTRL_LOOP_TX_MS states 75 ms, under the built design's tx row 76.81 ms

### 8x8/2if

Load 0.799 against its ceiling 0.70 (1.14x).

| Row | Figure, ms | Bound, ms | Margin, ms |
|---|---:|---:|---:|
| R4 | 45.24 | 20 | +25.24 |
| R5 | 209.68 | 90 | +119.68 |
| R6 | 199.36 | 90 | +109.36 |
| first | 21.13 | 20 | +1.13 |
| last | 867.89 | 125 | +742.89 |
| R4L | 211.12 | 238 | -26.88 |
| ACMP | 69.22 | 30 | +39.22 |
| ADP | 69.16 | 30 | +39.16 |
| MAAP | 73.41 | 30 | +43.41 |
| tx | 104.69 | 49 | +55.69 |
| txL | 474.19 | 49 | +425.19 |

- findings: 11 OVER line(s):
  - OVER 8x8/2if: the load 0.799 at the pin is over the flip ceiling 0.70
  - OVER 8x8/2if R4: under the tiers (slice 1300 us, tier 1 aecp-first, tier 2 srp-first, AECP queue) 45.24 ms, over its bound 20 ms; the largest term timers 11.45 ms
  - OVER 8x8/2if R5: under the tiers (slice 1300 us, tier 1 aecp-first, tier 2 srp-first, AECP queue) 209.68 ms, over its bound 90 ms; the largest term others 34.68 ms
  - OVER 8x8/2if R6: under the tiers (slice 1300 us, tier 1 aecp-first, tier 2 srp-first, AECP queue) 199.36 ms, over its bound 90 ms; the largest term others 33.40 ms
  - OVER 8x8/2if first: under the tiers (slice 1300 us, tier 1 aecp-first, tier 2 srp-first, AECP queue) 21.13 ms, over its bound 20 ms; the largest term spacing 8.00 ms
  - OVER 8x8/2if last: under the tiers (slice 1300 us, tier 1 aecp-first, tier 2 srp-first, AECP queue) 867.89 ms, over its bound 125 ms; the largest term srp 168.26 ms
  - OVER 8x8/2if ACMP: under the tiers (slice 1300 us, tier 1 aecp-first, tier 2 srp-first, AECP queue) 69.22 ms, over its bound 30 ms; the largest term timers 12.65 ms
  - OVER 8x8/2if ADP: under the tiers (slice 1300 us, tier 1 aecp-first, tier 2 srp-first, AECP queue) 69.16 ms, over its bound 30 ms; the largest term others 14.52 ms
  - OVER 8x8/2if MAAP: under the tiers (slice 1300 us, tier 1 aecp-first, tier 2 srp-first, AECP queue) 73.41 ms, over its bound 30 ms; the largest term others 16.80 ms
  - OVER 8x8/2if tx: under the tiers (slice 1300 us, tier 1 aecp-first, tier 2 srp-first, AECP queue) 104.69 ms, over its bound 49 ms; the largest term others 22.24 ms
  - OVER 8x8/2if txL: under the tiers (slice 1300 us, tier 1 aecp-first, tier 2 srp-first, AECP queue) 474.19 ms, over its bound 49 ms; the largest term aecp 102.56 ms

