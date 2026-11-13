**8x8/2if, by measurement** (3 legs)

| Tier | Row | Longest, ms | Bound, ms | Margin | Group |
|---|---|---:|---:|---:|---|
| SRP | srp | 13.937 | 90 | 0.845 | notice-every-7 |
| mrpdu | srp | 5.572 | 20 | 0.721 | save-starved |
| tier 1 | acmp | 9.605 | 20 | 0.520 | notice-burst-1 |
| tier 1 | adp | 8.344 | 20 | 0.583 | notice-burst-1 |
| tier 1 | aecp | 5.648 | 20 | 0.718 | notice-every-0 |
| tier 1 | maap | 7.746 | 20 | 0.613 | notice-burst-1 |
| queued notices | the first of a queue, the latest | 3.572 | 22 | | 16 queues |
| queued notices | every one, the latest of 640 | 53.336 | 62 | 0.140 | |
| egress held (tsn-c-stack #26) | backlog-owed.service.aecp.last | 61.997 | 20 | | backlog-owed |
| egress held (tsn-c-stack #26) | backlog.owed | 64.014 | 20 | | backlog-owed |
| egress held (tsn-c-stack #26) | backlog.owed_behind | 360.585 | 20 | | backlog-owed |

Heaviest work pass 228,022 CPU cycles (2.280 ms, THE SHARE 2.000 ms), notice-every-0.
Longest tier-2 slices: build 157,971 cycles (srp), round 73,427 cycles (notice-burst-6), srp 121,720 cycles (notice-every-5).
