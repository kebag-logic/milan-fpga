**1x1/1if, by measurement** (3 legs)

| Tier | Row | Longest, ms | Bound, ms | Margin | Group |
|---|---|---:|---:|---:|---|
| SRP | srp | 9.044 | 90 | 0.900 | backlog-adp@program-aged2-5 |
| mrpdu | srp | 1.052 | 20 | 0.947 | notice-every-6 |
| tier 1 | acmp | 6.562 | 20 | 0.672 | notice-burst-3 |
| tier 1 | adp | 5.652 | 20 | 0.717 | notice-burst-5 |
| tier 1 | aecp | 4.605 | 20 | 0.770 | notice-every-6 |
| tier 1 | maap | 5.677 | 20 | 0.716 | notice-every-6 |
| queued notices | the first of a queue, the latest | 5.947 | 20 | | 16 queues |
| queued notices | every one, the latest of 192 | 17.228 | 125 | 0.862 | |
| egress held (tsn-c-stack #26) | backlog-owed.service.aecp.last | 61.505 | 20 | | backlog-owed |
| egress held (tsn-c-stack #26) | backlog.owed | 62.413 | 20 | | backlog-owed |
| egress held (tsn-c-stack #26) | backlog.owed_behind | 360.329 | 20 | | backlog-owed |

Heaviest work pass 156,127 CPU cycles (1.561 ms, THE SHARE 2.000 ms), notice-burst-2.
Longest tier-2 slices: build 90,543 cycles (srp), round 80,832 cycles (notice-every-5), srp 103,874 cycles (notice-every-1).
