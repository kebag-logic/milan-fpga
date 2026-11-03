Measured with the CPU on sys at 100 MHz; the 32x32 columns are estimates, not measurements. ms; over the bound in bold, with the excess.

| Row | Bound | 1x1/1if | 8x8/1if | 8x8/2if | Estimate U, 4 x 8x8/2if | Estimate L, the measured line | Estimate S, the streams alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.78 | 1.22 | 1.32 | 5.3 | 3.2 | 2.8 |
| ADP record, first | 20 | 0.82 | 1.26 | 1.37 | 5.5 | 3.2 | 2.9 |
| MAAP record, first | 20 | 0.80 | 1.24 | 1.35 | 5.4 | 3.2 | 2.9 |
| AECP record, first | 20 | 0.81 | 1.26 | 1.36 | 5.4 | 3.2 | 2.9 |
| SRP record, first | 18 | 2.87 | 4.87 | 5.45 | **21.8** (+3.8) | 14.3 | 12.3 |
| ACMP record, last | 20 | 5.16 | 7.67 | 8.51 | **34.0** (+14.0) | 20.0 | 17.3 |
| ADP record, last | 20 | 3.67 | 5.43 | 6.07 | **24.3** (+4.3) | 14.3 | 12.4 |
| MAAP record, last | 20 | 3.70 | 5.47 | 6.10 | **24.4** (+4.4) | 14.3 | 12.6 |
| AECP record, last | 20 | 10.37 | 13.66 | 15.93 | **63.7** (+43.7) | **35.0** (+15.0) | **28.3** (+8.3) |
| SRP record, last | 18 | 10.67 | 14.94 | 16.35 | **65.4** (+47.4) | **35.8** (+17.8) | **31.0** (+13.0) |
| an ACMP command behind a full acmp ring | 20 | 3.57 | 5.98 | 6.70 | **26.8** (+6.8) | 17.4 | 14.9 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.83 | 4.05 | 4.63 | 18.5 | 10.8 | 8.8 |
| an event behind 15 others | 20 | 0.92 | 1.36 | 1.48 | 5.9 | 3.4 | 3.0 |
| The longest work pass | 2 | 1.11 | 1.60 | 1.97 | **7.9** (+5.9) | **4.9** (+2.9) | **3.6** (+1.6) |

