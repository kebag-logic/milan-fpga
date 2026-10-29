CPU at the product's split CPU clock, 50 MHz, bus 100 MHz:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 20 | 8.65 / 8.90 | 7.64 / 7.46 | 14.37 / 14.72 | 13.79 / 13.80 |
| ADP record, last | 20 | 6.08 / 6.38 | 5.51 / 5.36 | 11.20 / 11.23 | 10.59 / 10.61 |
| MAAP record, last | 20 | 6.11 / 6.42 | 5.50 / 5.34 | 11.19 / 11.21 | 10.57 / 10.59 |
| AECP record, last | 20 | 15.95 / 17.05 | 14.87 / 15.76 | **25.02** / **25.61** | **24.02** / **24.11** |
| SRP record, last | 18 | 17.81 / 17.02 | 16.34 / 16.26 | **28.25** / **27.25** | **25.66** / **25.45** |
| An ACMP command behind a full ACMP ring | 20 | 6.83 / 6.78 | 6.01 / 6.09 | 13.57 / 13.60 | 12.71 / 12.72 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 4.55 / 4.88 | 4.38 / 4.26 | 7.63 / 7.87 | 7.32 / 7.23 |
| An event behind 15 others | 20 | 2.06 / 2.06 | 1.88 / 1.89 | 3.63 / 3.64 | 3.46 / 3.48 |
| AECP record, last, in the owed window | 20 | **64.73** / **64.67** | **64.66** / **64.65** | **68.53** / **68.46** | **68.71** / **68.75** |
| A response with 7 frames owed ahead of it | 20 | **63.41** / **63.33** | **63.35** / **63.33** | **66.26** / **66.20** | **66.41** / **66.45** |
| An ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

CPU at the labelled 100 MHz option, bus 100 MHz:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 20 | 5.51 / 5.30 | 4.60 / 4.76 | 8.79 / 8.82 | 8.30 / 8.12 |
| ADP record, last | 20 | 3.93 / 3.77 | 3.28 / 3.41 | 6.67 / 6.69 | 6.31 / 6.33 |
| MAAP record, last | 20 | 3.97 / 3.81 | 3.26 / 3.44 | 6.65 / 6.68 | 6.29 / 6.32 |
| AECP record, last | 20 | 10.25 / 10.43 | 9.36 / 9.98 | 15.10 / 15.84 | 13.74 / 14.61 |
| SRP record, last | 18 | 10.53 / 10.40 | 9.97 / 10.19 | 16.95 / 16.32 | 15.60 / 15.40 |
| An ACMP command behind a full ACMP ring | 20 | 4.07 / 4.04 | 3.64 / 3.70 | 8.13 / 8.15 | 7.64 / 7.45 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 3.02 / 2.87 | 2.58 / 2.60 | 4.13 / 4.32 | 3.33 / 4.03 |
| An event behind 15 others | 20 | 1.24 / 1.23 | 1.14 / 1.15 | 2.09 / 2.10 | 2.01 / 2.02 |
| AECP record, last, in the owed window | 20 | **62.81** / **62.90** | **62.84** / **62.83** | **65.03** / **64.94** | **65.02** / **65.09** |
| A response with 7 frames owed ahead of it | 20 | **61.99** / **62.06** | **62.01** / **62.00** | **63.70** / **63.64** | **63.69** / **63.74** |
| An ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

Per-pass share, 2.0 ms of CPU time; each cell is arm A / arm B: the work passes over it of the four groups' runs, and the longest pass in ms:

| CPU clock | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| 50 MHz (product) | 0 of 1273, 1.89 / 0 of 1245, 1.89 | 0 of 1264, 1.71 / 0 of 1246, 1.72 | **32 of 1310, 3.46** / **30 of 1286, 3.47** | **24 of 1307, 3.28** / **23 of 1285, 3.30** |
| 100 MHz (option) | 0 of 1272, 1.14 / 0 of 1248, 1.14 | 0 of 1273, 1.04 / 0 of 1249, 1.06 | **1 of 1311, 2.29** / **2 of 1284, 2.30** | **1 of 1332, 2.20** / **1 of 1298, 2.20** |
