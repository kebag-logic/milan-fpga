| Class | Events | Frames | Per second |
|---|---|---|---|
| Whole-frame repeat | 334 | 334 | 0.508 |
| One-frame skip | 526 | 526 | 0.800 |
| Skip of 2 to 59 frames | 521 | 7,176 | 0.792 |
| Skip of 60 frames or more | 239 | 109,928 | 0.363 |
| Silent stretch | 6 | 6 | - |

| Cycle | Hold, s | Stopped in hold | Last valid after unbind, s | Restart, s | From command, s | Capture stall in restart | Result |
|---|---|---|---|---|---|---|---|
| 1 | 2.018 | yes | 0.0150 | 0.1358 | 0.1439 | no | PASS |
| 2 | 2.019 | yes | 0.0150 | 0.0282 | 0.0364 | no | PASS |
| 3 | 2.019 | yes | 0.0155 | 0.0269 | 0.0347 | no | PASS |
| 4 | 2.018 | yes | 0.0152 | 0.0273 | 0.0350 | no | PASS |
| 5 | 2.022 | yes | 0.0246 | 0.0276 | 0.0351 | no | PASS |
| 6 | 2.018 | yes | 0.0151 | 0.0287 | 0.0360 | no | PASS |
| 7 | 2.018 | yes | 0.0147 | 0.0262 | 0.0344 | no | PASS |
| 8 | 2.018 | yes | 0.0145 | 0.0271 | 0.0350 | no | PASS |
| 9 | 2.018 | yes | 0.0145 | 0.0268 | 0.0348 | no | PASS |
| 10 | 2.017 | yes | 0.0154 | 0.0279 | 0.0354 | no | PASS |
| 11 | 2.017 | yes | 0.0154 | 0.0288 | 0.0362 | no | PASS |
| 12 | 2.019 | yes | 0.0147 | 0.0270 | 0.0353 | no | PASS |
| 13 | 2.017 | yes | 0.0148 | 0.0281 | 0.0355 | no | PASS |
| 14 | 2.018 | yes | 0.0155 | 0.0285 | 0.0358 | no | PASS |
| 15 | 2.019 | yes | 0.0149 | 0.0274 | 0.0354 | no | PASS |
| 16 | 2.018 | yes | 0.0148 | 0.0283 | 0.0357 | no | PASS |
| 17 | 2.017 | yes | 0.0155 | 0.0282 | 0.0355 | no | PASS |
| 18 | 2.019 | yes | 0.0155 | 0.0270 | 0.0352 | no | PASS |
| 19 | 2.019 | yes | 0.0152 | 0.0273 | 0.0354 | no | PASS |
| 20 | 2.018 | yes | 0.0156 | 0.0389 | 0.0463 | yes, 19.8 ms | PASS |
| 21 | 2.018 | yes | 0.0144 | 0.0279 | 0.0354 | no | PASS |
| 22 | 2.017 | yes | 0.0154 | 0.0275 | 0.0349 | no | PASS |
| 23 | 2.018 | yes | 0.0150 | 0.0280 | 0.0355 | no | PASS |
| 24 | 2.018 | yes | 0.0146 | 0.0284 | 0.0356 | no | PASS |
| 25 | 2.018 | yes | 0.0151 | 0.0285 | 0.0359 | no | PASS |
| 26 | 2.017 | yes | 0.0145 | 0.0283 | 0.0355 | no | PASS |
| 27 | 2.019 | yes | 0.0153 | 0.0271 | 0.0352 | no | PASS |
| 28 | 2.018 | yes | 0.0148 | 0.0282 | 0.0355 | no | PASS |
| 29 | 2.019 | yes | 0.0152 | 0.0269 | 0.0351 | no | PASS |
| 30 | 2.018 | yes | 0.0145 | 0.0275 | 0.0349 | no | PASS |

| Population | Count | Below 1 s | Min, s | Median, s | p95, s | Max, s |
|---|---|---|---|---|---|---|
| Demonstrated restarts | 30 | 30 | 0.0262 | 0.0279 | 0.0389 | 0.1358 |

| First ten median, s | Last ten median, s | Slope, s per cycle | 95% slope interval, s per cycle | Residual df |
|---|---|---|---|---|
| 0.0274 | 0.0280 | -0.000664 | [-0.001495, +0.000166] | 28 |
