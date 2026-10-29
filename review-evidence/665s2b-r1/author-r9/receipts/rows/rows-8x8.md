# 8x8/2if: every composed row, graded against its own bound (rows9.py)

Bound: min(T_svc = 20 ms, the family's ceiling) plus W. Cells arm A / arm B, ms, bold over the bound. Round 8's legs are its receipts (graded then at 10 ms), regraded here.

| 8x8/2if: row | Bound, ms | round 8 after | final head | round 8 with both drafts | final head, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 2.02 / 2.06 | 2.02 / 2.06 | 2.01 / 1.98 | 2.01 / 1.98 |
| ACMP record, last | 20 | 8.51 / 8.94 | 8.51 / 8.94 | 8.62 / 8.28 | 8.62 / 8.28 |
| ADP record, first | 20 | 2.06 / 2.10 | 2.06 / 2.10 | 2.05 / 2.02 | 2.05 / 2.02 |
| ADP record, last | 20 | 6.68 / 6.86 | 6.68 / 6.86 | 6.64 / 6.52 | 6.64 / 6.52 |
| AECP record, first | 20 | 2.05 / 2.10 | 2.05 / 2.10 | 2.05 / 2.01 | 2.05 / 2.01 |
| AECP record, first, in the owed window | 20 | 1.14 / 1.22 | 1.14 / 1.22 | 1.08 / 1.04 | 1.08 / 1.04 |
| AECP record, last | 20 | 14.92 / 15.89 | 14.92 / 15.89 | 14.47 / 15.22 | 14.47 / 15.22 |
| AECP record, last, in the owed window | 20 | **64.66** / **64.79** | **64.66** / **64.79** | **64.79** / **64.68** | **64.79** / **64.68** |
| MAAP record, first | 20 | 2.04 / 2.09 | 2.04 / 2.09 | 2.04 / 2.00 | 2.04 / 2.00 |
| MAAP record, last | 20 | 6.66 / 6.84 | 6.66 / 6.84 | 6.63 / 6.50 | 6.63 / 6.50 |
| SRP record, first | 18 | 4.35 / 4.45 | 4.35 / 4.45 | 4.37 / 4.28 | 4.37 / 4.28 |
| SRP record, last | 18 | 16.30 / 16.39 | 16.30 / 16.39 | 15.81 / 15.19 | 15.81 / 15.19 |
| a response with 7 frames owed ahead of it | 20 | **63.44** / **63.51** | **63.44** / **63.51** | **63.78** / **63.42** | **63.78** / **63.42** |
| an ACMP command behind a full acmp ring | 20 | 7.87 / 8.29 | 7.87 / 8.29 | 7.98 / 7.63 | 7.98 / 7.63 |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 4.23 / 4.32 | 4.23 / 4.32 | 4.24 / 4.38 | 4.24 / 4.38 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.13 / 0.14 | 0.13 / 0.14 | 0.24 / 0.23 | 0.24 / 0.23 |
| an event behind 15 others | 20 | 2.15 / 2.20 | 2.15 / 2.20 | 2.15 / 2.12 | 2.15 / 2.12 |
