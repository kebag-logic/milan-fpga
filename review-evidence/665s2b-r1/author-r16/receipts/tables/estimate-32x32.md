Measured with the CPU on sys at 100 MHz; the 32x32 columns are estimates, not measurements. ms; over the bound in bold, with the excess.

| Row | Bound | 1x1/1if | 8x8/1if | 8x8/2if | Estimate U, 4 x 8x8/2if | Estimate L, the measured line | Estimate S, the streams alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.82 | 1.18 | 1.35 | 5.4 | 3.1 | 2.6 |
| ADP record, first | 20 | 0.86 | 1.22 | 1.39 | 5.6 | 3.2 | 2.6 |
| MAAP record, first | 20 | 0.84 | 1.21 | 1.37 | 5.5 | 3.2 | 2.6 |
| AECP record, first | 20 | 0.86 | 1.22 | 1.38 | 5.5 | 3.2 | 2.6 |
| SRP record, first | 18 | 3.05 | 4.76 | 5.49 | **21.9** (+3.9) | 13.8 | 11.4 |
| ACMP record, last | 20 | 5.19 | 7.81 | 8.90 | **35.6** (+15.6) | **21.6** (+1.6) | 18.0 |
| ADP record, last | 20 | 3.70 | 5.66 | 6.77 | **27.1** (+7.1) | 17.3 | 13.6 |
| MAAP record, last | 20 | 3.74 | 4.89 | 5.49 | **21.9** (+1.9) | 11.5 | 9.8 |
| AECP record, last | 20 | 10.27 | 13.17 | 15.28 | **61.1** (+41.1) | **32.5** (+12.5) | **26.1** (+6.1) |
| SRP record, last | 18 | 10.81 | 14.93 | 16.45 | **65.8** (+47.8) | **35.8** (+17.8) | **30.6** (+12.6) |
| an ACMP command behind a full acmp ring | 20 | 3.78 | 5.88 | 7.11 | **28.4** (+8.4) | 18.5 | 14.3 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.94 | 3.82 | 5.49 | **22.0** (+2.0) | 14.2 | 8.5 |
| an event behind 15 others | 20 | 0.97 | 1.33 | 1.51 | 6.0 | 3.4 | 2.8 |
| The longest work pass | 2 | 1.14 | 1.59 | 1.85 | **7.4** (+5.4) | **4.3** (+2.3) | **3.4** (+1.4) |

