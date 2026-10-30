| Arm | rc | Rows | ok | Minimum ms | Maximum ms | Under 24.5 ms by | Margin to the 49 ms floor | Committed receipt maximum ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 8x8-50-on | 0 | 16 | 16 | 13.84584 | 13.85922 | 10.64078 ms (43.4 %) | 3.5356x | 13.86328 |
| 8x8-50-off | 0 | 16 | 16 | 13.61714 | 13.67682 | 10.82318 ms (44.2 %) | 3.5827x | 13.68956 |
| 8x8-100-on | 0 | 16 | 16 | 10.42490 | 10.43194 | 14.06806 ms (57.4 %) | 4.6971x | 10.42973 |
| 8x8-100-off | 0 | 16 | 16 | 10.41566 | 10.41899 | 14.08101 ms (57.5 %) | 4.7030x | 10.41566 |
| 1x1-50-on | 0 | 16 | 16 | 3.96228 | 3.96814 | 20.53186 ms (83.8 %) | 12.3484x | 3.96548 |
| 1x1-50-off | 0 | 16 | 16 | 3.90676 | 3.92034 | 20.57966 ms (84.0 %) | 12.4989x | 3.92034 |

Worst contract-clock capture: 8x8-50-on, 13.85922 ms, 10.64078 ms under the 24.5 ms bound.
Control skip-copy: rc 0
Control no-traffic: rc 0
Control byte-only: rc 0, minimum slowdown 1.834640044677839
