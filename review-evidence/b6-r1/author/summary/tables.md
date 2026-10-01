<!-- thdn -->
| Case | Tone | Blocks | Clean blocks | THD+N, clean, dB (median / worst) | SNR, clean, dB (median / worst) | Worst THD+N, a block with a listener discontinuity, dB | Worst THD+N, a block with a DUT beat only, dB |
|---|---|---|---|---|---|---|---|
| A0 | 997 Hz | 629 | 54 | -146.06 / -146.06 | 146.07 / 146.07 | -2.52 | -28.48 |
| A0 | 9,973 Hz | 629 | 54 | -145.99 / -145.99 | 145.99 / 145.99 | 4.70 | -8.10 |
| A1 | 997 Hz | 617 | 291 | -146.06 / -146.06 | 146.07 / 146.07 | none | -28.48 |
| A1 | 9,973 Hz | 617 | 291 | -145.99 / -145.99 | 145.99 / 145.99 | none | -8.10 |
| A2 | 997 Hz | 616 | 1 | -146.06 / -146.06 | 146.07 / 146.07 | 3.13 | -28.48 |
| A2 | 9,973 Hz | 616 | 1 | -145.99 / -145.99 | 145.99 / 145.99 | 17.28 | -8.10 |
| B INTERNAL | 997 Hz | 629 | 57 | -146.06 / -146.06 | 146.07 / 146.07 | 11.63 | -28.48 |
| B INTERNAL | 9,973 Hz | 629 | 57 | -145.99 / -145.99 | 145.99 / 145.99 | 11.07 | -8.10 |
| B CRF | 997 Hz | 629 | 611 | -146.06 / -146.06 | 146.07 / 146.07 | none | none |
| B CRF | 9,973 Hz | 629 | 611 | -145.99 / -145.99 | 145.99 / 145.99 | none | none |

<!-- offset -->
| Case | Fitted offset, clean blocks, 997 Hz, ppm (max magnitude) | Fitted offset, clean blocks, 9,973 Hz, ppm (max magnitude) | Tone offset over the window, listener only, ppm | DUT beat, ppm | Counted McASP0 to peer ratio, ppm |
|---|---|---|---|---|---|
| A0 | 3.1e-07 | 1.6e-08 | +17.142 | -10.622 | +6.519 (1 frame = 0.033) |
| A1 | 1.9e-07 | 1.4e-08 | +0.000 | -10.631 | -10.631 (1 frame = 0.034) |
| A2 | 2.2e-07 | 2.2e-09 | +10.617 | -10.685 | -0.068 (1 frame = 0.034) |
| B INTERNAL | 3.1e-07 | 1.5e-08 | +16.700 | -10.648 | +6.052 (1 frame = 0.033) |
| B CRF | 2.9e-07 | 7.8e-09 | +0.000 | +0.000 | +0.000 (1 frame = 0.033) |

<!-- discontinuities -->
| Case | Window, s | Listener drops (frames) | Listener repeats | Listener silent inserts | DUT beat repeats | Beat comb: period, frames; teeth expected | DUT SLIP_TDM, per s | Capture-path losses: events, clusters, frames lost | Torn frames |
|---|---|---|---|---|---|---|---|---|---|
| A0 | 629.56 | 519 (519) | 0 | 1 | 321 | 93,990.39; 321.8 | 0.5111 | 25, 10, 26,173 | 0 |
| A1 | 617.32 | 0 (0) | 0 | 0 | 315 | 93,990.38; 321.8 | 0.5111 | 51, 23, 615,026 | 0 |
| A2 | 616.14 | 494 (494) | 0 | 180 | 316 | 93,990.38; 322.0 | 0.5096 | 143, 61, 686,656 | 0 |
| B INTERNAL | 629.98 | 506 (506) | 0 | 1 | 322 | 93,990.38; 321.9 | 0.5097 | 36, 21, 15,552 | 0 |
| B CRF | 629.95 | 0 (0) | 0 | 0 | 0 | - | - | 40, 17, 12,216 | 0 |

<!-- ratio -->
| Case | Counted ratio, ppm | Timed ratio, McASP0 capture, ppm (95 % half-width) | Halves, ppm | McASP0 capture rate on the board's clock, Hz | External capture reads | Capture read stalls over 15 ms |
|---|---|---|---|---|---|---|
| A0 | +6.519 | +6.44 (+-0.72) | +5.35 / +6.68 | 47,997.928 | 62,844 | 105 |
| A1 | -10.631 | -12.19 (+-2.44) | -13.07 / -14.39 | 47,997.913 | 61,579 | 232 |
| A2 | -0.068 | -0.59 (+-1.24) | -0.53 / -1.76 | 47,997.959 | 61,337 | 316 |
| B INTERNAL | +6.052 | +6.85 (+-1.46) | +8.70 / +6.43 | 47,997.962 | 62,851 | 211 |
| B CRF | +0.000 | -0.01 (+-0.65) | +0.18 / +1.30 | 47,997.671 | 62,923 | 97 |
