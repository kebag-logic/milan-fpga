| control | named checks (receipt) | 1/1 | 2/2 | 3/5 | 9/9 | caught at | = PR body |
|---|---|---:|---:|---:|---:|---|---|
| `tf-heads-swapped` | TF1, TF2 | 2 | 2 | 2 | 2 | 4 of 4 | yes |
| `tf-head-at-write-pointer` | TF1, TF4 | 2 | 2 | 2 | 2 | 4 of 4 | yes |
| `tf-listener-push-dropped` | TF2 | 1 | 1 | 1 | 1 | 4 of 4 | yes |
| `tf-ls-written-at-tk-pointer` | TF2, TF5 | 2 | 2 | 2 | 2 | 4 of 4 | yes |
| `tf-tk-head-read-ahead` | TF1, TF4 | 4 | 4 | 3 | 2 | 4 of 4 | yes |
| `tf-ls-head-reads-tk-ram` | TF1, TF2, TF3, TF4, TF5 | 4 | 4 | 4 | 5 | 4 of 4 | yes |
| `tf-tk-write-at-rptr` | TF1, TF4 | 2 | 2 | 2 | 2 | 4 of 4 | yes |
| `tf-full-guard-31` | TF4 | 1 | 1 | 1 | 1 | 4 of 4 | yes |
| `tf-tk-write-ignores-full` | TF4 | 1 | 1 | 1 | 1 | 4 of 4 | yes |
| `tf-ls-write-ignores-full` | TF5 | 1 | 1 | 1 | 1 | 4 of 4 | yes |
| `walk-record-written-on-close` | WK3 | 1 | 1 | 1 | 1 | 4 of 4 | yes |
| `wtsp-first-open-only` | WK2, WK3, WK4 | 3 | 5 | 7 | 19 | 4 of 4 | yes |
| `wtsp-read-at-gate-source` | WK1, WK2, WK4 | 1 | 4 | 9 | 33 | 4 of 4 | yes |
| `wtsp-read-at-source-0` | WK1, WK2, WK3, WK4, WK5 | 0 | 6 | 10 | 34 | 3 of 4 | yes |
| `wtsp-latency-field-shifted` | WK1, WK2, WK3, WK4, WK5 | 6 | 10 | 14 | 38 | 4 of 4 | yes |
| `wtsp-latency-shifted` | WK1, WK2, WK3, WK4, WK5 | 6 | 10 | 14 | 38 | 4 of 4 | yes |
| `wtsp-rank-dropped` | WK1, WK2, WK3, WK4, WK5 | 3 | 5 | 6 | 19 | 4 of 4 | yes |
| `wtsp-prio-rank-swapped` | WK1, WK2, WK3, WK4, WK5 | 5 | 9 | 13 | 34 | 4 of 4 | yes |
| `wid-ram-first-open-only` | WK2, WK3, WK4 | 0 | 0 | 7 | 19 | 2 of 4 | yes |
| `wid-ram-read-at-gate-source` | WK1, WK2, WK4 | 0 | 0 | 9 | 33 | 2 of 4 | yes |
| `wid-ram-read-neighbour` | WK1, WK2, WK3, WK4, WK5 | 0 | 0 | 14 | 38 | 2 of 4 | yes |
| `wid-flops-da-of-gate-source` | WK1, WK2, WK4 | 1 | 4 | 0 | 0 | 2 of 4 | yes |
| `wid-flops-sid-of-source-0` | WK1, WK2, WK3, WK4, WK5 | 0 | 6 | 0 | 0 | 1 of 4 | yes |
| `wid-flops-vid-of-source-0` | WK1, WK2, WK3, WK4, WK5 | 0 | 6 | 0 | 0 | 1 of 4 | yes |
| `talker-vid-unreset` | WK5 | 1 | 1 | 1 | 1 | 4 of 4 | yes |
| `wsid-ram-first-settle-only` | WK8 | 0 | 0 | 5 | 9 | 2 of 4 | yes |
| `wsid-ram-written-on-teardown` | WK7 | 0 | 0 | 1 | 1 | 2 of 4 | yes |
| `wsid-flops-of-control-sink` | WK6, WK8 | 0 | 3 | 0 | 0 | 1 of 4 | yes |
| `wsid-flops-read-sink-0` | WK6, WK7, WK8 | 0 | 4 | 0 | 0 | 1 of 4 | yes |

29 rows compared, 0 differ
