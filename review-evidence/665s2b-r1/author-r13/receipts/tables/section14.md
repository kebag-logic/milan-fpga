Measured with the CPU on sys at 100 MHz; the 32x32 columns are estimates, not measurements. ms; over the bound in bold, with the excess.

| Row | Bound | 1x1/1if | 8x8/1if | 8x8/2if | Estimate U, 4 x 8x8/2if | Estimate L, the measured line | Estimate S, the streams alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.79 | 1.17 | 1.39 | 5.5 | 3.4 | 2.7 |
| ADP record, first | 20 | 0.83 | 1.21 | 1.43 | 5.7 | 3.5 | 2.8 |
| MAAP record, first | 20 | 0.81 | 1.20 | 1.41 | 5.6 | 3.5 | 2.8 |
| AECP record, first | 20 | 0.82 | 1.21 | 1.42 | 5.7 | 3.5 | 2.8 |
| SRP record, first | 18 | 2.92 | 4.68 | 5.61 | **22.5** (+4.5) | 14.9 | 11.8 |
| ACMP record, last | 20 | 5.18 | 7.25 | 8.31 | **33.3** (+13.3) | 19.1 | 15.8 |
| ADP record, last | 20 | 3.68 | 5.01 | 6.07 | **24.3** (+4.3) | 14.3 | 11.2 |
| MAAP record, last | 20 | 3.72 | 5.00 | 6.06 | **24.2** (+4.2) | 14.1 | 11.0 |
| AECP record, last | 20 | 10.17 | 13.21 | 15.96 | **63.9** (+43.9) | **35.8** (+15.8) | **28.1** (+8.1) |
| SRP record, last | 18 | 10.58 | 14.91 | 16.56 | **66.2** (+48.2) | **37.1** (+19.1) | **31.4** (+13.4) |
| an ACMP command behind a full acmp ring | 20 | 3.63 | 5.80 | 7.01 | **28.0** (+8.0) | 18.6 | 14.6 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.81 | 3.90 | 4.42 | 17.7 | 9.9 | 8.2 |
| an event behind 15 others | 20 | 0.93 | 1.32 | 1.54 | 6.1 | 3.6 | 2.9 |
| The longest work pass | 2 | 1.10 | 1.56 | 1.96 | **7.9** (+5.9) | **4.9** (+2.9) | **3.5** (+1.5) |

