# 1x1/1if: every composed row, graded against its own bound (rows9.py)

Bound: min(T_svc = 20 ms, the family's ceiling) plus W. Cells arm A / arm B, ms, bold over the bound. Round 8's legs are its receipts (graded then at 10 ms), regraded here.

| 1x1/1if: row | Bound, ms | round 8 after | final head | round 8 with both drafts | final head, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.09 / 1.04 | 1.09 / 1.04 | 0.97 / 0.97 | 0.97 / 0.97 |
| ACMP record, last | 20 | 5.09 / 5.02 | 5.09 / 5.02 | 4.41 / 4.55 | 4.41 / 4.55 |
| ADP record, first | 20 | 1.13 / 1.09 | 1.13 / 1.09 | 1.01 / 1.01 | 1.01 / 1.01 |
| ADP record, last | 20 | 3.77 / 3.56 | 3.77 / 3.56 | 3.22 / 3.24 | 3.22 / 3.24 |
| AECP record, first | 20 | 1.13 / 1.08 | 1.13 / 1.08 | 1.01 / 1.01 | 1.01 / 1.01 |
| AECP record, first, in the owed window | 20 | 0.73 / 0.72 | 0.73 / 0.72 | 0.63 / 0.65 | 0.63 / 0.65 |
| AECP record, last | 20 | 9.56 / 9.93 | 9.56 / 9.93 | 8.64 / 9.00 | 8.64 / 9.00 |
| AECP record, last, in the owed window | 20 | **62.40** / **62.32** | **62.40** / **62.32** | **62.25** / **62.36** | **62.25** / **62.36** |
| MAAP record, first | 20 | 1.12 / 1.07 | 1.12 / 1.07 | 1.00 / 0.99 | 1.00 / 0.99 |
| MAAP record, last | 20 | 3.81 / 3.60 | 3.81 / 3.60 | 3.25 / 3.27 | 3.25 / 3.27 |
| SRP record, first | 18 | 2.17 / 2.08 | 2.17 / 2.08 | 1.97 / 1.97 | 1.97 / 1.97 |
| SRP record, last | 18 | 10.41 / 9.91 | 10.41 / 9.91 | 9.11 / 9.26 | 9.11 / 9.26 |
| a response with 7 frames owed ahead of it | 20 | **61.70** / **61.64** | **61.70** / **61.64** | **61.60** / **61.68** | **61.60** / **61.68** |
| an ACMP command behind a full acmp ring | 20 | 3.91 / 3.69 | 3.91 / 3.69 | 3.44 / 3.44 | 3.44 / 3.44 |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.88 / 2.72 | 2.88 / 2.72 | 2.46 / 2.48 | 2.46 / 2.48 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.11 / 0.07 | 0.11 / 0.07 | 0.07 / 0.09 | 0.07 / 0.09 |
| an event behind 15 others | 20 | 1.22 / 1.17 | 1.22 / 1.17 | 1.10 / 1.10 | 1.10 / 1.10 |
