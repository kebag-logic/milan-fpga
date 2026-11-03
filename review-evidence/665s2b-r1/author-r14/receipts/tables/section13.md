CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz. Cells are arm A / arm B, ms, bold over the bound.

The four backlog windows:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.78 / 0.77 | 0.72 / 0.71 | 1.32 / 1.32 | 1.23 / 1.23 |
| ADP record, first | 20 | 0.82 / 0.81 | 0.76 / 0.75 | 1.36 / 1.37 | 1.28 / 1.27 |
| MAAP record, first | 20 | 0.80 / 0.80 | 0.75 / 0.73 | 1.34 / 1.35 | 1.26 / 1.26 |
| AECP record, first | 20 | 0.81 / 0.81 | 0.76 / 0.74 | 1.35 / 1.36 | 1.27 / 1.27 |
| SRP record, first | 18 | 2.87 / 2.85 | 2.69 / 2.65 | 5.45 / 5.43 | 5.05 / 5.06 |
| ACMP record, last | 20 | 5.11 / 5.16 | 4.53 / 4.61 | 7.87 / 8.51 | 7.34 / 7.72 |
| ADP record, last | 20 | 3.58 / 3.67 | 3.28 / 3.29 | 5.85 / 6.07 | 5.44 / 5.56 |
| MAAP record, last | 20 | 3.57 / 3.70 | 3.26 / 3.33 | 5.83 / 6.10 | 5.43 / 5.59 |
| AECP record, last | 20 | 10.04 / 10.37 | 9.07 / 9.67 | 14.83 / 15.93 | 13.49 / 14.33 |
| SRP record, last | 18 | 10.67 / 10.59 | 9.88 / 9.64 | 16.35 / 15.90 | 15.58 / 14.87 |
| an ACMP command behind a full acmp ring | 20 | 3.57 / 3.54 | 3.27 / 3.22 | 6.64 / 6.70 | 6.37 / 6.29 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.83 / 2.80 | 2.54 / 2.52 | 3.62 / 4.63 | 3.31 / 4.27 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.14 / 0.12 | 0.08 / 0.11 | 0.11 / 0.19 | 0.08 / 0.22 |
| an event behind 15 others | 20 | 0.92 / 0.92 | 0.87 / 0.85 | 1.47 / 1.48 | 1.39 / 1.38 |
| AECP record, last, in the owed window | 20 | **62.93** / **62.95** | **62.93** / **62.85** | **65.13** / **65.13** | **65.13** / **65.04** |
| a response with 7 frames owed ahead of it | 20 | **62.07** / **62.10** | **62.06** / **62.01** | **63.78** / **63.77** | **63.76** / **63.69** |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

A save's windows (save_window.py), 24 at each leg:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.43 / 1.44 | 1.42 / 1.32 | 1.96 / 1.91 | 1.84 / 1.69 |
| ADP record, first | 20 | 1.42 / 1.43 | 1.41 / 1.31 | 1.95 / 1.90 | 1.83 / 1.68 |
| MAAP record, first | 20 | 1.46 / 1.47 | 1.44 / 1.35 | 1.99 / 1.93 | 1.86 / 1.71 |
| AECP record, first | 20 | 1.47 / 1.48 | 1.45 / 1.36 | 2.00 / 1.94 | 1.87 / 1.72 |
| SRP record, first | 18 | 2.73 / 2.58 | 2.45 / 2.35 | 4.37 / 4.21 | 4.09 / 3.99 |
| ACMP record, last | 20 | 5.95 / 5.89 | 5.43 / 5.29 | 9.02 / 9.23 | 8.30 / 8.32 |
| ADP record, last | 20 | 4.43 / 4.40 | 4.08 / 3.97 | 6.57 / 6.79 | 6.08 / 6.15 |
| MAAP record, last | 20 | 4.46 / 4.43 | 4.11 / 4.01 | 6.61 / 6.82 | 6.12 / 6.18 |
| AECP record, last | 20 | 10.91 / 10.92 | 9.87 / 10.34 | 15.96 / 16.56 | 14.86 / 15.31 |
| SRP record, last | 18 | 11.46 / 11.22 | 10.51 / 10.32 | 17.23 / 16.91 | 16.48 / 15.56 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 3.55 / 3.53 | 3.31 / 3.21 | 5.42 / 5.35 | 5.03 / 4.87 |

save-held, every receive channel at its refill rate with its bursts:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | 20 | 2.76 / 2.73 | 2.28 / 2.26 | 4.78 / 4.80 | 4.43 / 4.44 |
| ACMP record, every channel at its refill rate, the longest | 20 | 4.39 / 4.32 | 3.66 / 3.63 | 8.11 / 8.17 | 7.17 / 7.09 |
| AECP record, every channel at its refill rate, the longest | 20 | 5.57 / 5.41 | 5.04 / 4.96 | 10.92 / 11.00 | 9.82 / 9.76 |
| MAAP record, every channel at its refill rate, the longest | 20 | 2.82 / 3.01 | 2.27 / 2.54 | 5.30 / 5.33 | 4.84 / 4.85 |
| SRP record, every channel at its refill rate, the longest | 18 | 8.09 / 8.01 | 7.07 / 7.09 | 14.12 / 14.20 | 13.42 / 13.38 |

save-starved, the same and a grandmaster change as every pass starts:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | 20 | 2.85 / 2.82 | 2.37 / 2.35 | 4.86 / 4.88 | 4.51 / 4.53 |
| ACMP record, every channel at its refill rate, the longest | 20 | 4.55 / 4.47 | 3.82 / 3.85 | 8.27 / 8.50 | 7.32 / 7.28 |
| AECP record, every channel at its refill rate, the longest | 20 | 6.10 / 6.09 | 5.60 / 5.54 | 11.49 / 11.35 | 10.36 / 10.35 |
| MAAP record, every channel at its refill rate, the longest | 20 | 2.94 / 2.89 | 2.37 / 2.40 | 5.41 / 5.61 | 4.95 / 4.97 |
| SRP record, every channel at its refill rate, the longest | 18 | 8.67 / 8.69 | 7.65 / 7.68 | 14.60 / 14.81 | 13.88 / 13.89 |

The share is 2.0 ms. Passes over it, of the work passes run, and the longest in ms, arm A / arm B:

| Groups | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| The four backlog windows | 0 of 1264, 1.11 / 0 of 1251, 1.10 | 0 of 1285, 1.01 / 0 of 1250, 1.01 | 0 of 1311, 1.97 / 0 of 1285, 1.92 | 0 of 1313, 1.89 / 0 of 1287, 1.77 |
| A save's windows | 0 of 10748, 1.22 / 0 of 8643, 1.23 | 0 of 11112, 1.18 / 0 of 8633, 1.17 | 0 of 18324, 1.96 / 0 of 11744, 1.95 | 0 of 17871, 1.86 / 0 of 11737, 1.85 |
| save-held | 0 of 3411, 1.03 / 0 of 3395, 1.03 | 0 of 3405, 1.04 / 0 of 3421, 1.03 | 0 of 8474, 1.69 / 0 of 8489, 1.69 | 0 of 8504, 1.63 / 0 of 8499, 1.63 |
| save-starved | 0 of 44390, 0.97 / 0 of 43629, 0.97 | 0 of 39664, 0.97 / 0 of 43670, 0.97 | 0 of 52488, 1.71 / 0 of 52090, 1.72 | 0 of 52624, 1.66 / 0 of 53926, 1.66 |
| Every group run | 0 of 66819, 1.22 / 0 of 57520, 1.23 | 0 of 56068, 1.18 / 0 of 57576, 1.18 | 0 of 88204, 1.97 / 0 of 74225, 1.95 | 0 of 80929, 1.89 / 0 of 76066, 1.85 |

Saves, ms from the change to durable against the stated worst case, arm A / arm B (steps; longest gap between flash steps, ms):

| Group | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| save | 2019.2 of 4,070 (102; 10.918) / 2018.4 of 4,070 (102; 10.942) | 2018.3 of 4,070 (102; 10.862) / 2018.3 of 4,070 (102; 10.91) | 4697.4 of 12,110 (370; 12.611) / 4697.4 of 12,110 (370; 12.561) | 4697.4 of 12,110 (370; 12.717) / 4698.3 of 12,110 (370; 12.536) |
| save-held | 2019.0 of 4,070 (102; 15.058) / 2018.1 of 4,070 (102; 14.63) | 2018.1 of 4,070 (102; 13.895) / 2018.1 of 4,070 (102; 14.141) | 4696.9 of 12,110 (370; 19.447) / 4696.7 of 12,110 (370; 19.545) | 4697.0 of 12,110 (370; 18.424) / 4731.1 of 12,110 (370; 17.659) |
| save-starved | 4049.0 of 4,070 (102; 30.982) / 4048.1 of 4,070 (102; 30.97) | 4047.9 of 4,070 (102; 31.08) / 4048.0 of 4,070 (102; 31.047) | 12087.0 of 12,110 (370; 31.325) / 12087.0 of 12,110 (370; 31.254) | 12087.1 of 12,110 (370; 31.476) / 12088.0 of 12,110 (370; 31.417) |

Passes that carry the store's step, every group: count, the longest pass and the longest step, CPU cycles (ms), arm A / arm B:

| 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---:|---:|---:|---:|
| 14299: 121,795 (1.218); 96,151 (0.962) / 10704: 123,127 (1.231); 96,123 (0.961) | 10701: 118,240 (1.182); 96,579 (0.966) / 10701: 117,691 (1.177); 96,244 (0.962) | 18290: 129,153 (1.292); 96,213 (0.962) / 14529: 126,560 (1.266); 96,208 (0.962) | 14528: 124,581 (1.246); 96,375 (0.964) / 14514: 124,882 (1.249); 95,857 (0.959) |

