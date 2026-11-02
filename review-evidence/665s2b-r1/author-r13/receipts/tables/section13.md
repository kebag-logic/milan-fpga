## A save's windows

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.48 / 1.46 | 1.41 / 1.37 | 1.85 / 1.87 | 1.71 / 1.81 |
| ADP record, first | 20 | 1.47 / 1.45 | 1.40 / 1.36 | 1.84 / 1.86 | 1.70 / 1.80 |
| MAAP record, first | 20 | 1.51 / 1.49 | 1.43 / 1.39 | 1.88 / 1.89 | 1.73 / 1.84 |
| AECP record, first | 20 | 1.52 / 1.50 | 1.44 / 1.40 | 1.89 / 1.90 | 1.74 / 1.85 |
| SRP record, first | 18 | 2.68 / 2.59 | 2.44 / 2.41 | 4.39 / 4.38 | 4.08 / 4.01 |
| ACMP record, last | 20 | 5.95 / 5.92 | 5.47 / 5.33 | 8.89 / 9.30 | 8.20 / 8.39 |
| ADP record, last | 20 | 4.44 / 4.42 | 4.10 / 4.02 | 6.44 / 6.85 | 5.94 / 6.24 |
| MAAP record, last | 20 | 4.47 / 4.46 | 4.14 / 4.06 | 6.48 / 6.89 | 5.96 / 6.28 |
| AECP record, last | 20 | 10.86 / 11.15 | 10.22 / 10.34 | 15.86 / 16.79 | 14.51 / 15.38 |
| SRP record, last | 18 | 11.17 / 11.14 | 10.60 / 10.31 | 16.99 / 17.29 | 15.79 / 15.46 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 3.57 / 3.55 | 3.32 / 3.26 | 5.29 / 5.40 | 4.87 / 4.96 |

## The four backlog windows

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.78 / 0.79 | 0.71 / 0.72 | 1.32 / 1.39 | 1.23 / 1.24 |
| ADP record, first | 20 | 0.82 / 0.83 | 0.75 / 0.76 | 1.37 / 1.43 | 1.28 / 1.28 |
| MAAP record, first | 20 | 0.81 / 0.81 | 0.73 / 0.74 | 1.35 / 1.41 | 1.26 / 1.26 |
| AECP record, first | 20 | 0.82 / 0.82 | 0.74 / 0.75 | 1.36 / 1.42 | 1.27 / 1.28 |
| SRP record, first | 18 | 2.88 / 2.92 | 2.68 / 2.70 | 5.42 / 5.61 | 5.06 / 5.06 |
| ACMP record, last | 20 | 5.06 / 5.18 | 4.79 / 4.60 | 7.85 / 8.31 | 7.28 / 7.37 |
| ADP record, last | 20 | 3.52 / 3.68 | 3.38 / 3.30 | 5.85 / 6.07 | 5.38 / 5.35 |
| MAAP record, last | 20 | 3.54 / 3.72 | 3.42 / 3.33 | 5.84 / 6.06 | 5.36 / 5.33 |
| AECP record, last | 20 | 9.68 / 10.17 | 9.44 / 9.60 | 14.69 / 15.96 | 13.58 / 14.35 |
| SRP record, last | 18 | 10.58 / 10.47 | 9.74 / 9.58 | 16.56 / 16.46 | 15.33 / 14.81 |
| an ACMP command behind a full acmp ring | 20 | 3.59 / 3.63 | 3.27 / 3.28 | 6.59 / 7.01 | 6.36 / 6.37 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.81 / 2.81 | 2.54 / 2.53 | 3.60 / 4.42 | 3.29 / 3.95 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.08 / 0.10 | 0.13 / 0.06 | 0.12 / 0.12 | 0.19 / 0.25 |
| an event behind 15 others | 20 | 0.92 / 0.93 | 0.85 / 0.88 | 1.47 / 1.54 | 1.38 / 1.39 |
| AECP record, last, in the owed window | 20 | **62.90** / **63.01** | **62.90** / **62.87** | **65.10** / **65.31** | **65.12** / **65.14** |
| a response with 7 frames owed ahead of it | 20 | **62.05** / **62.14** | **62.03** / **62.02** | **63.75** / **64.19** | **63.75** / **63.76** |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

## The share

| Groups | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| The four backlog windows | 0 of 1280, 1.10 / 0 of 1251, 1.10 | 0 of 1276, 1.01 / 0 of 1250, 1.01 | 0 of 1314, 1.96 / 0 of 1286, 1.95 | 0 of 1317, 1.86 / 0 of 1286, 1.82 |
| A save's 24 windows | 0 of 11195, 1.22 / 0 of 8643, 1.21 | 0 of 11134, 1.18 / 0 of 8631, 1.16 | 0 of 18088, 1.95 / 0 of 11745, 1.98 | 0 of 18111, 1.86 / 0 of 11742, 1.83 |
| Every group the leg ran | 0 of 19927, 1.22 / 0 of 10496, 1.21 | 0 of 13012, 1.18 / 0 of 10483, 1.16 | 0 of 27214, 1.96 / 0 of 13648, 1.98 | 0 of 20045, 1.86 / 0 of 13645, 1.83 |
