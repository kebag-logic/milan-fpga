Measured with the CPU on sys at 100 MHz; the 32x32 columns are estimates, not measurements. ms; over the bound in bold, with the excess.

| Row | Bound | 1x1/1if | 8x8/1if | 8x8/2if | Estimate U, 4 x 8x8/2if | Estimate L, the measured line | Estimate S, the streams alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.75 | 1.15 | 1.31 | 5.2 | 3.2 | 2.7 |
| ADP record, first | 20 | 0.80 | 1.20 | 1.35 | 5.4 | 3.3 | 2.7 |
| MAAP record, first | 20 | 0.78 | 1.18 | 1.33 | 5.3 | 3.2 | 2.7 |
| AECP record, first | 20 | 0.79 | 1.19 | 1.34 | 5.4 | 3.2 | 2.7 |
| SRP record, first | 18 | 2.80 | 4.57 | 5.35 | **21.4** (+3.4) | 14.1 | 11.4 |
| ACMP record, last | 20 | 5.16 | 7.23 | 7.98 | **31.9** (+11.9) | 17.7 | 15.1 |
| ADP record, last | 20 | 3.65 | 4.92 | 5.85 | **23.4** (+3.4) | 13.4 | 10.2 |
| MAAP record, last | 20 | 3.68 | 4.99 | 5.84 | **23.3** (+3.3) | 13.2 | 10.3 |
| AECP record, last | 20 | 10.02 | 13.12 | 15.16 | **60.6** (+40.6) | **32.8** (+12.8) | **25.8** (+5.8) |
| SRP record, last | 18 | 10.00 | 14.42 | 15.96 | **63.8** (+45.8) | **36.4** (+18.4) | **31.1** (+13.1) |
| an ACMP command behind a full acmp ring | 20 | 3.47 | 5.64 | 6.73 | **26.9** (+6.9) | 17.9 | 14.2 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.74 | 3.84 | 4.19 | 16.8 | 9.2 | 8.0 |
| an event behind 15 others | 20 | 0.89 | 1.29 | 1.45 | 5.8 | 3.4 | 2.8 |
| The longest work pass | 2 | 1.07 | 1.58 | 1.97 | **7.9** (+5.9) | **5.0** (+3.0) | **3.7** (+1.7) |

- 1x1/1if: an idle pass takes 6,410 to 15,161 CPU cycles.
- 8x8/1if: an idle pass takes 13,259 to 25,906 CPU cycles.
- 8x8/2if: an idle pass takes 14,832 to 33,234 CPU cycles.

Quiet work load, work-pass cycles over elapsed cycles from `settled` to `composed` (arm A): N-A1 1.14 %, P81-A8 2.06 %, N-A8 2.80 %.

The one-CPU arms, 8x8 and 1x1, the same rows (arm A, ms):

| Row | Bound | Split CPU 1x1 | cacheless RV32IM 1x1 | cacheless RV32I 1x1 | Split CPU 8x8 | cacheless RV32IM 8x8 | cacheless RV32I 8x8 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.75 | 1.56 | 1.58 | 1.30 | 2.90 | 2.93 |
| ADP record, first | 20 | 0.79 | 1.60 | 1.62 | 1.34 | 2.94 | 2.98 |
| MAAP record, first | 20 | 0.77 | 1.58 | 1.60 | 1.33 | 2.92 | 2.96 |
| AECP record, first | 20 | 0.78 | 1.59 | 1.61 | 1.34 | 2.93 | 2.97 |
| SRP record, first | 18 | 2.79 | 5.44 | 5.63 | 5.35 | 11.37 | 11.72 |
| ACMP record, last | 20 | 5.16 | 9.98 | 10.45 | 7.76 | 16.08 | 16.09 |
| ADP record, last | 20 | 3.65 | 7.14 | 7.78 | 5.81 | 11.70 | 11.77 |
| MAAP record, last | 20 | 3.68 | 7.18 | 7.81 | 5.80 | 11.71 | 11.75 |
| AECP record, last | 20 | 9.67 | 17.34 | 19.76 | 14.41 | **26.83** | **28.51** |
| SRP record, last | 18 | 9.95 | 17.98 | **21.63** | 15.88 | **30.26** | **34.52** |
| an ACMP command behind a full acmp ring | 20 | 3.45 | 6.87 | 7.06 | 6.51 | 14.29 | 14.42 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.73 | 5.50 | 5.94 | 3.53 | 8.75 | 7.78 |
| an event behind 15 others | 20 | 0.88 | 1.82 | 1.84 | 1.44 | 3.16 | 3.20 |
| The longest work pass | 2 | 1.07 | 2.14 | 2.35 | 1.97 | 3.61 | 3.85 |
| Passes over the share | - | 0 of 1277 | 3 of 1267 | 3 of 1270 | 0 of 1319 | 62 of 1314 | 64 of 1315 |
