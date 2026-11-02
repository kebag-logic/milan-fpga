CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz. Cells are arm A / arm B, ms, bold over the bound.

| Row | Bound, ms | 1x1/1if | 1x1/1if, both drafts | 8x8/2if | 8x8/2if, both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.75 / 0.75 | 0.65 / 0.67 | 1.30 / 1.31 | 1.21 / 1.22 |
| ADP record, first | 20 | 0.79 / 0.80 | 0.70 / 0.71 | 1.34 / 1.35 | 1.25 / 1.26 |
| MAAP record, first | 20 | 0.77 / 0.78 | 0.68 / 0.69 | 1.33 / 1.33 | 1.24 / 1.24 |
| AECP record, first | 20 | 0.78 / 0.79 | 0.69 / 0.70 | 1.34 / 1.34 | 1.25 / 1.25 |
| SRP record, first | 18 | 2.79 / 2.80 | 2.50 / 2.56 | 5.35 / 5.29 | 4.99 / 5.00 |
| ACMP record, last | 20 | 5.16 / 5.06 | 4.34 / 4.52 | 7.76 / 7.98 | 7.42 / 7.30 |
| ADP record, last | 20 | 3.65 / 3.59 | 3.18 / 3.22 | 5.81 / 5.85 | 5.26 / 5.08 |
| MAAP record, last | 20 | 3.68 / 3.63 | 3.22 / 3.26 | 5.80 / 5.84 | 5.30 / 5.12 |
| AECP record, last | 20 | 9.67 / 10.02 | 8.72 / 9.48 | 14.41 / 15.16 | 13.79 / 14.05 |
| SRP record, last | 18 | 9.95 / 10.00 | 9.49 / 9.68 | 15.88 / 15.96 | 14.84 / 14.81 |
| an ACMP command behind a full acmp ring | 20 | 3.45 / 3.47 | 3.03 / 3.11 | 6.51 / 6.73 | 6.19 / 6.21 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.73 / 2.74 | 2.42 / 2.45 | 3.53 / 4.19 | 3.95 / 4.11 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.12 / 0.12 | 0.11 / 0.10 | 0.25 / 0.23 | 0.23 / 0.09 |
| an event behind 15 others | 20 | 0.88 / 0.89 | 0.78 / 0.80 | 1.44 / 1.45 | 1.35 / 1.35 |
| AECP record, last, in the owed window | 20 | **62.66** / **62.73** | **62.75** / **62.77** | **64.99** / **64.95** | **64.94** / **65.01** |
| a response with 7 frames owed ahead of it | 20 | **62.07** / **61.93** | **61.94** / **61.95** | **63.68** / **63.93** | **63.91** / **63.68** |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

The share is 2.0 ms. Passes over it of the work passes run, longest in ms, arm A / arm B:

| 1x1/1if | 1x1/1if, both drafts | 8x8/2if | 8x8/2if, both drafts |
|---:|---:|---:|---:|
| 0 of 1277, 1.07 / 0 of 1250, 1.07 | 0 of 1279, 0.98 / 0 of 1250, 0.98 | 0 of 1319, 1.97 / 0 of 1286, 1.92 | 0 of 1310, 1.77 / 0 of 1302, 1.77 |

