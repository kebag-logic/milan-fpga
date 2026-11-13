**1x1/1if, by measurement** (3 legs)

| Tier | Row | Longest, ms | Bound, ms | Margin | Group |
|---|---|---:|---:|---:|---|
| SRP | srp | 9.220 | 90 | 0.898 | notice-burst-5 |
| mrpdu | srp | 1.156 | 20 | 0.942 | notice-every-0 |
| tier 1 | acmp | 6.472 | 20 | 0.676 | notice-burst-5 |
| tier 1 | adp | 5.659 | 20 | 0.717 | notice-burst-3 |
| tier 1 | aecp | 4.605 | 20 | 0.770 | notice-every-6 |
| tier 1 | maap | 5.592 | 20 | 0.720 | notice-every-6 |
| queued notices | the first of a queue, the latest | 5.947 | 20 | | 16 queues |
| queued notices | every one, the latest of 192 | 19.288 | 125 | 0.846 | |
| egress held (tsn-c-stack #26) | backlog-owed.service.aecp.last | 61.548 | 20 | | backlog-owed |
| egress held (tsn-c-stack #26) | backlog.owed | 62.456 | 20 | | backlog-owed |
| egress held (tsn-c-stack #26) | backlog.owed_behind | 360.258 | 20 | | backlog-owed |

Heaviest work pass 156,754 CPU cycles (1.568 ms, THE SHARE 2.000 ms), notice-burst-2.
Longest tier-2 slices: build 90,543 cycles (srp), round 61,957 cycles (notice-every-0), srp 93,757 cycles (notice-every-4).
