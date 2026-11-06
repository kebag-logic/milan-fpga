CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz. Cells are arm A / arm B, ms, bold over the bound.

The four backlog windows:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.82 / 0.79 | 0.73 / 0.73 | 1.34 / 1.35 | 1.25 / 1.32 |
| ADP record, first | 20 | 0.86 / 0.84 | 0.77 / 0.78 | 1.39 / 1.39 | 1.29 / 1.36 |
| MAAP record, first | 20 | 0.84 / 0.82 | 0.75 / 0.76 | 1.37 / 1.37 | 1.27 / 1.34 |
| AECP record, first | 20 | 0.86 / 0.83 | 0.77 / 0.77 | 1.38 / 1.38 | 1.28 / 1.36 |
| SRP record, first | 18 | 3.05 / 2.96 | 2.76 / 2.78 | 5.49 / 5.42 | 5.10 / 5.36 |
| ACMP record, last | 20 | 5.16 / 5.19 | 4.61 / 4.68 | 8.47 / 8.90 | 8.19 / 8.06 |
| ADP record, last | 20 | 3.66 / 3.70 | 3.32 / 3.35 | 6.58 / 6.77 | 6.16 / 6.33 |
| MAAP record, last | 20 | 3.65 / 3.74 | 3.31 / 3.39 | 5.49 / 5.43 | 5.11 / 5.36 |
| AECP record, last | 20 | 10.01 / 10.27 | 9.39 / 9.62 | 14.21 / 15.28 | 13.55 / 13.98 |
| SRP record, last | 18 | 10.81 / 10.55 | 10.18 / 9.89 | 16.45 / 15.72 | 14.68 / 15.15 |
| an ACMP command behind a full acmp ring | 20 | 3.78 / 3.66 | 3.38 / 3.40 | 7.11 / 6.81 | 6.33 / 6.89 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.94 / 2.85 | 2.61 / 2.58 | 4.69 / 5.49 | 5.01 / 4.95 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.08 / 0.14 | 0.09 / 0.05 | 0.09 / 0.18 | 0.08 / 0.09 |
| an event behind 15 others | 20 | 0.97 / 0.94 | 0.88 / 0.89 | 1.51 / 1.51 | 1.40 / 1.50 |
| AECP record, last, in the owed window | 20 | **63.03** / **62.97** | **62.91** / **63.00** | **64.81** / **64.87** | **64.78** / **64.96** |
| a response with 7 frames owed ahead of it | 20 | **62.16** / **62.13** | **62.07** / **62.13** | **63.55** / **63.62** | **63.56** / **63.66** |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

A save's windows opened from idle (save_window.py), 24 at each leg:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.52 / 1.45 | 1.44 / 1.42 | 1.86 / 1.83 | 1.77 / 1.87 |
| ADP record, first | 20 | 1.51 / 1.44 | 1.43 / 1.41 | 1.85 / 1.82 | 1.76 / 1.86 |
| MAAP record, first | 20 | 1.55 / 1.47 | 1.46 / 1.45 | 1.89 / 1.85 | 1.79 / 1.90 |
| AECP record, first | 20 | 1.56 / 1.48 | 1.47 / 1.46 | 1.90 / 1.86 | 1.80 / 1.91 |
| SRP record, first | 18 | 2.72 / 2.58 | 2.50 / 2.47 | 4.22 / 3.70 | 3.89 / 3.70 |
| ACMP record, last | 20 | 6.12 / 5.89 | 5.59 / 5.45 | 9.35 / 9.26 | 8.42 / 8.57 |
| ADP record, last | 20 | 4.68 / 4.41 | 4.17 / 4.12 | 7.02 / 7.13 | 6.45 / 6.62 |
| MAAP record, last | 20 | 4.61 / 4.44 | 4.21 / 4.16 | 6.41 / 6.63 | 6.08 / 6.41 |
| AECP record, last | 20 | 10.68 / 11.05 | 10.18 / 10.25 | 15.64 / 15.94 | 14.19 / 15.05 |
| SRP record, last | 18 | 11.59 / 11.26 | 11.05 / 10.74 | 17.52 / 16.44 | 15.08 / 15.53 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 3.88 / 3.55 | 3.38 / 3.34 | 5.76 / 5.86 | 5.30 / 5.45 |

A save's windows opened with the step's age at its limit, two (save_window.aged_window), 24 at each leg:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.17 / 0.79 | 1.02 / 1.09 | 1.28 / 1.65 | 1.52 / 1.62 |
| ADP record, first | 20 | 1.16 / 0.78 | 1.01 / 1.08 | 1.27 / 1.64 | 1.51 / 1.61 |
| MAAP record, first | 20 | 0.90 / 0.81 | 0.75 / 1.11 | 1.31 / 1.28 | 1.20 / 1.27 |
| AECP record, first | 20 | 0.91 / 0.82 | 0.76 / 1.12 | 1.32 / 1.29 | 1.21 / 1.28 |
| SRP record, first | 18 | 2.41 / 2.30 | 2.11 / 2.13 | 4.17 / 3.61 | 4.19 / 3.49 |
| ACMP record, last | 20 | 6.79 / 6.57 | 6.19 / 6.02 | 10.16 / 10.06 | 9.19 / 9.34 |
| ADP record, last | 20 | 5.37 / 5.20 | 4.87 / 4.78 | 7.97 / 7.92 | 7.40 / 7.39 |
| MAAP record, last | 20 | 4.53 / 4.37 | 4.11 / 4.03 | 6.51 / 6.41 | 6.04 / 6.16 |
| AECP record, last | 20 | 11.17 / 11.29 | 10.52 / 10.61 | 16.26 / 16.63 | 14.51 / 15.52 |
| SRP record, last | 18 | 11.92 / 11.62 | 11.22 / 11.20 | 17.66 / 17.29 | 15.68 / 16.31 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 4.57 / 4.41 | 4.14 / 4.06 | 6.67 / 6.65 | 6.25 / 6.22 |

The same one short of it, one, 24 at each leg that ran them (both arms, without the drafts):

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.17 / 1.12 | - / - | 1.28 / 1.64 | - / - |
| ADP record, first | 20 | 1.16 / 1.11 | - / - | 1.27 / 1.63 | - / - |
| MAAP record, first | 20 | 0.86 / 0.83 | - / - | 1.30 / 1.28 | - / - |
| AECP record, first | 20 | 0.87 / 0.84 | - / - | 1.31 / 1.29 | - / - |
| SRP record, first | 18 | 3.12 / 2.16 | - / - | 5.03 / 3.58 | - / - |
| ACMP record, last | 20 | 6.01 / 5.93 | - / - | 9.30 / 9.08 | - / - |
| ADP record, last | 20 | 4.58 / 4.56 | - / - | 7.05 / 6.95 | - / - |
| MAAP record, last | 20 | 4.00 / 3.80 | - / - | 6.25 / 6.05 | - / - |
| AECP record, last | 20 | 10.42 / 10.54 | - / - | 16.28 / 16.56 | - / - |
| SRP record, last | 18 | 12.23 / 10.78 | - / - | 17.77 / 17.33 | - / - |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 3.78 / 3.78 | - / - | 5.74 / 5.67 | - / - |

save-held, every receive channel at its refill rate with its bursts:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | 20 | 2.78 / 2.72 | 2.29 / 2.28 | 4.65 / 4.61 | 4.25 / 4.42 |
| ACMP record, every channel at its refill rate, the longest | 20 | 4.33 / 4.25 | 3.68 / 3.64 | 8.18 / 7.46 | 6.96 / 7.70 |
| AECP record, every channel at its refill rate, the longest | 20 | 5.52 / 5.48 | 5.01 / 5.03 | 10.56 / 10.34 | 9.04 / 9.63 |
| MAAP record, every channel at its refill rate, the longest | 20 | 2.97 / 2.75 | 2.50 / 2.55 | 5.14 / 5.09 | 4.62 / 4.82 |
| SRP record, every channel at its refill rate, the longest | 18 | 8.49 / 8.02 | 7.11 / 7.05 | 14.53 / 14.32 | 12.74 / 13.59 |

save-starved, the same and a grandmaster change as every pass starts:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | 20 | 2.86 / 2.81 | 2.37 / 2.60 | 4.74 / 4.70 | 4.34 / 4.63 |
| ACMP record, every channel at its refill rate, the longest | 20 | 4.48 / 4.42 | 3.82 / 4.04 | 8.39 / 7.65 | 6.98 / 7.91 |
| AECP record, every channel at its refill rate, the longest | 20 | 6.13 / 6.06 | 5.64 / 5.65 | 11.23 / 10.99 | 9.67 / 10.38 |
| MAAP record, every channel at its refill rate, the longest | 20 | 2.92 / 2.87 | 2.68 / 2.59 | 5.27 / 5.22 | 4.73 / 4.94 |
| SRP record, every channel at its refill rate, the longest | 18 | 8.65 / 8.61 | 8.00 / 7.94 | 15.08 / 14.90 | 13.59 / 14.26 |

The share is 2.0 ms. Passes over it, of the work passes run, and the longest in ms, arm A / arm B:

| Groups | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| The four backlog windows | 0 of 1315, 1.14 / 0 of 1272, 1.11 | 0 of 1318, 1.04 / 0 of 1273, 1.03 | 0 of 1355, 1.63 / 0 of 1311, 1.85 | 0 of 1362, 1.53 / 0 of 1312, 1.81 |
| A save's windows from idle | 0 of 12644, 1.16 / 0 of 8798, 1.12 | 0 of 12640, 1.13 / 0 of 8796, 1.12 | 0 of 22645, 1.90 / 0 of 11936, 1.86 | 0 of 22731, 1.77 / 0 of 11937, 1.81 |
| Aged windows at the limit | 0 of 25748, 1.15 / 0 of 22572, 1.12 | 0 of 25715, 1.13 / 0 of 22195, 1.12 | 0 of 29414, 1.90 / 0 of 19133, 1.87 | 0 of 30654, 1.78 / 0 of 18234, 1.82 |
| Aged windows one short of it | 0 of 23328, 1.28 / 0 of 20074, 1.20 | 0 of 0, 0.00 / 0 of 0, 0.00 | 0 of 28096, 1.90 / 0 of 17786, 1.87 | 0 of 0, 0.00 / 0 of 0, 0.00 |
| save-held | 0 of 3426, 1.13 / 0 of 3429, 1.13 | 0 of 3439, 1.11 / 0 of 3433, 1.12 | 0 of 8623, 1.66 / 0 of 8638, 1.65 | 0 of 8678, 1.57 / 0 of 8665, 1.61 |
| save-starved | 0 of 42843, 0.97 / 0 of 42843, 0.97 | 0 of 43204, 0.97 / 0 of 41993, 0.97 | 0 of 57407, 1.69 / 0 of 58001, 1.67 | 0 of 58295, 1.60 / 0 of 52030, 1.64 |
| save-second | 0 of 81422, 0.96 / 0 of 81198, 0.97 | 0 of 81075, 0.97 / 0 of 78972, 0.96 | 0 of 129900, 1.31 / 0 of 0, 0.00 | 0 of 0, 0.00 / 0 of 0, 0.00 |
| Every group run | 0 of 199801, 1.28 / 0 of 180796, 1.20 | 0 of 168001, 1.13 / 0 of 157272, 1.12 | 0 of 286852, 1.90 / 0 of 117430, 1.87 | 0 of 122348, 1.78 / 0 of 92803, 1.82 |

Saves, ms from the change to durable against the stated worst case, arm A / arm B (steps; longest gap between flash steps, ms):

| Group | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| save | 2018.4 of 4,070 (102; 10.95) / 2018.5 of 4,070 (102; 10.988) | 2018.4 of 4,070 (102; 10.946) / 2018.5 of 4,070 (102; 10.843) | 4697.3 of 12,110 (370; 11.3) / 4698.2 of 12,110 (370; 11.367) | 4698.2 of 12,110 (370; 11.322) / 4697.3 of 12,110 (370; 11.28) |
| save-held | 2018.2 of 4,070 (102; 14.206) / 2018.3 of 4,070 (102; 14.275) | 2018.2 of 4,070 (102; 13.966) / 2018.3 of 4,070 (102; 13.935) | 4696.9 of 12,110 (370; 18.923) / 4730.9 of 12,110 (370; 18.217) | 4707.9 of 12,110 (370; 17.255) / 4696.9 of 12,110 (370; 18.348) |
| save-starved | 4048.1 of 4,070 (102; 31.043) / 4048.2 of 4,070 (102; 31.119) | 4048.1 of 4,070 (102; 30.893) / 4048.2 of 4,070 (102; 30.959) | 12087.0 of 12,110 (370; 31.092) / 12087.9 of 12,110 (370; 31.1) | 12087.9 of 12,110 (370; 31.115) / 12086.7 of 12,110 (370; 31.106) |
| save-second | 6029.8 of 6,070 (102; 30.948) / 6029.9 of 6,070 (102; 30.937) | 6029.9 of 6,070 (102; 30.895) / 6029.8 of 6,070 (102; 30.927) | 22110.1 of 22,150 (370; 31.041) / - | - / - |

Aged windows: the least margin and its row, the aged steps among their records (count, the longest aged pass, CPU cycles (ms), and the kinds), per age, arm A / arm B:

| Age | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| 2 | 6.077 (11.923, program-aged2-7); 24 aged in 24, longest 90,231 (0.902), issue/read-back / 6.380 (11.620, program-aged2-7); 24 aged in 24, longest 83,253 (0.833), issue/read-back | 6.776 (11.224, blank-aged2-7); 24 aged in 24, longest 89,359 (0.894), issue/read-back / 6.798 (11.202, blank-aged2-0); 24 aged in 24, longest 83,413 (0.834), issue/read-back | 0.335 (17.665, verify-aged2-4); 24 aged in 24, longest 85,164 (0.852), issue/read-back / 0.713 (17.287, verify-aged2-4); 24 aged in 24, longest 83,661 (0.837), issue/read-back | 2.318 (15.682, verify-aged2-7); 24 aged in 24, longest 85,683 (0.857), issue/read-back / 1.693 (16.307, verify-aged2-7); 24 aged in 24, longest 84,117 (0.841), issue/read-back |
| 1 | 5.771 (12.229, blank-aged1-7); 0 aged in 24 / 7.218 (10.782, blank-aged1-5); 0 aged in 24 | - / - | 0.235 (17.765, verify-aged1-7); 14 aged in 24, longest 84,053 (0.841), issue/read-back / 0.674 (17.326, verify-aged1-7); 13 aged in 24, longest 83,311 (0.833), issue/read-back | - / - |

Passes that carry the store's step, every group: count, the longest pass and the longest step, CPU cycles (ms), arm A / arm B:

| 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---:|---:|---:|---:|
| 30478: 128,083 (1.281); 96,212 (0.962) / 26876: 120,051 (1.201); 95,990 (0.960) | 19050: 113,084 (1.131); 96,078 (0.961) / 19050: 112,416 (1.124); 96,030 (0.960) | 40519: 130,212 (1.302); 95,999 (0.960) / 35688: 126,891 (1.269); 95,746 (0.957) | 25123: 125,743 (1.257); 95,873 (0.959) / 25120: 127,428 (1.274); 96,034 (0.960) |

