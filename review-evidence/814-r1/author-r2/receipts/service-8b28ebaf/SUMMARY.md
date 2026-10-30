| Shape | rc | Verdict | Commands | Erases / page programs / bytes (largest command) | Commits logged | Heartbeat max gap ms | Measurement-only budget findings | Service findings (the verdict) |
|---|---:|---|---:|---|---:|---:|---:|---:|
| 1x1 | 0 | PASS: measurement evidence; budget findings: 0 | 17 | 2 / 28 / 6672 | 2 | 267.034 | 0 | 0 |
| 8x8 | 0 | PASS: measurement evidence; budget findings: 0 | 17 | 2 / 104 / 26512 | 2 | 324.581 | 2 | 0 |

The two 8x8 measurement-only findings are "over-budget duty: milan_nvm": the two console commit commands, 860.03331 and 862.05357 ms, against the 500 ms console figure. Under --enforce-service the verdict counts service findings only (run.py:761); console response time has no protocol deadline (run.py:375-376).
