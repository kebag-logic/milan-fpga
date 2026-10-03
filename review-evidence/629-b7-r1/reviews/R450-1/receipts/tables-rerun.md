<!-- b7-thdn -->
| Case | Tone | Blocks | Blocks at the floor | THD+N there, dB (median / worst) | SNR there, dB (median / worst) | Worst THD+N, a block with a listener discontinuity, dB | Worst THD+N, all blocks, dB |
|---|---|---|---|---|---|---|---|
| A0 | 997 Hz | 630 | 444 | -146.06 / -146.06 | 146.07 / 146.07 | -7.19 | -2.22 |
| A0 | 9,973 Hz | 630 | 444 | -145.99 / -145.99 | 145.99 / 145.99 | +1.01 | +23.84 |
| A1 | 997 Hz | 629 | 597 | -146.06 / -146.06 | 146.07 / 146.07 | None | +12.71 |
| A1 | 9,973 Hz | 629 | 597 | -145.99 / -145.99 | 145.99 / 145.99 | None | +21.58 |
| A2 | 997 Hz | 628 | 578 | -146.06 / -146.06 | 146.07 / 146.07 | None | +13.23 |
| A2 | 9,973 Hz | 628 | 578 | -145.99 / -145.99 | 145.99 / 145.99 | None | +19.67 |
| B0 | 997 Hz | 629 | 434 | -146.06 / -146.06 | 146.07 / 146.07 | -6.31 | -2.13 |
| B0 | 9,973 Hz | 629 | 434 | -145.99 / -145.99 | 145.99 / 145.99 | +4.14 | +19.01 |
| BCRF | 997 Hz | 628 | 559 | -146.06 / -146.06 | 146.07 / 146.07 | None | +15.74 |
| BCRF | 9,973 Hz | 628 | 559 | -145.99 / -145.99 | 145.99 / 145.99 | None | +18.73 |
| BAAF | 997 Hz | 627 | 564 | -146.06 / -146.06 | 146.07 / 146.07 | None | +0.60 |
| BAAF | 9,973 Hz | 627 | 564 | -145.99 / -145.99 | 145.99 / 145.99 | None | +21.26 |

<!-- b7-offset -->
| Case | Fitted offset, blocks at the floor, ppm (largest magnitude, either tone) | Listener drops (frames) | Listener repeats | Listener silent inserts | DUT beat repeats | Tone offset, listener only, ppm | Counted McASP0 to peer ratio, ppm |
|---|---|---|---|---|---|---|---|
| A0 | 2.7e-07 | 470 (470) | 0 | 291 | 0 | +5.916 | +5.916 (1 frame = 0.033) |
| A1 | 2.3e-07 | 0 (0) | 0 | 0 | 0 | +0.000 | +0.000 (1 frame = 0.033) |
| A2 | 2.1e-07 | 0 (0) | 0 | 0 | 0 | +0.000 | +0.000 (1 frame = 0.033) |
| B0 | 2.4e-07 | 457 (457) | 0 | 278 | 0 | +5.924 | +5.924 (1 frame = 0.033) |
| BCRF | 2.9e-07 | 0 (0) | 0 | 0 | 0 | +0.000 | +0.000 (1 frame = 0.033) |
| BAAF | 3.2e-07 | 0 (0) | 0 | 0 | 0 | +0.000 | +0.000 (1 frame = 0.033) |

<!-- b7-discontinuities -->
| Case | Window of captured audio, s | DUT `SLIP_TDM` dups in the window (reads, s) | Capture-path losses: events, clusters, frames | Torn frames | Result |
|---|---|---|---|---|---|
| A0 | 630.31 | 0 (600 s) | 15, 7, 5,058 | 0 | PASS as a control |
| A1 | 629.88 | 0 (600 s) | 37, 32, 5,580 | 0 | PASS |
| A2 | 628.04 | 0 (600 s) | 62, 53, 112,533 | 0 | PASS |
| B0 | 629.55 | 0 (600 s) | 39, 19, 22,404 | 0 | PASS as a control |
| BCRF | 628.53 | 0 (600 s) | 86, 69, 74,568 | 0 | PASS |
| BAAF | 627.74 | 0 (600 s) | 78, 65, 115,701 | 0 | PASS |

<!-- b7-ratio -->
| Case | Counted ratio, ppm | Timed ratio, McASP0 capture, ppm (95 % half-width) | Window halves, timed, ppm | McASP0 capture rate on the board's clock, Hz | External capture reads | Capture read stalls over 15 ms |
|---|---|---|---|---|---|---|
| A0 | +5.916 | +5.71 (+-0.55) | +5.96 / +4.98 | 47,997.956 | 63,027 | 10 |
| A1 | +0.000 | -0.28 (+-1.40) | -2.33 / +0.33 | 47,997.953 | 62,970 | 42 |
| A2 | +0.000 | +2.15 (+-4.42) | +3.73 / +0.14 | 47,997.954 | 62,745 | 79 |
| B0 | +5.924 | +5.62 (+-0.44) | +5.67 / +5.81 | 47,997.948 | 62,860 | 66 |
| BCRF | +0.000 | +1.98 (+-6.52) | -0.60 / +9.14 | 47,997.667 | 62,699 | 130 |
| BAAF | +0.000 | -1.49 (+-11.64) | +0.16 / -22.60 | 47,997.667 | 62,642 | 112 |

<!-- b7-servo -->
| Case | DUT reads in the window | Servo state at every read | Trim, ppm (min / max) | AAF meter: locked, rate valid at every read | Meter rate, ppm (min / max) | Meter restarts (first / last) | Meter largest deviation, ns | CRF sink rate, ppm (min / max) | Set to LOCKED, s | CLOCK_DOMAIN LOCKED/UNLOCKED, window start -> end |
|---|---|---|---|---|---|---|---|---|---|---|
| A0 | 21 | IDLE | +0.00 / +0.00 | not selected | - | - | - | - | - | 3/2 -> 3/2 |
| A1 | 21 | IDLE | +0.00 / +0.00 | not selected | - | - | - | - | - | 3/2 -> 3/2 |
| A2 | 21 | IDLE | +0.00 / +0.00 | not selected | - | - | - | - | - | 3/2 -> 3/2 |
| B0 | 21 | IDLE | +0.00 / +0.00 | not selected | - | - | - | +11.025 / +11.057 | - | 3/2 -> 3/2 |
| BCRF | 21 | LOCKED | -6.00 / -5.94 | not selected | - | - | - | +11.008 / +11.057 | 3.1 to 3.6 | 4/3 -> 4/3 |
| BAAF | 21 | LOCKED | -6.00 / -5.94 | yes, yes | +11.018 / +11.043 | 0 / 0 | 29 | - | 6.6 to 7.1 | 5/4 -> 5/4 |
