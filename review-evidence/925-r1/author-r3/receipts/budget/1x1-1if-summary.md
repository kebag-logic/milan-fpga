CPU budget 1x1-1if: measured 7a2def7c, both firmware ELFs relink byte-identical at 5f625090.
run.py --point 1x1 --build-dir <output> --record-budget-findings --record-share-findings --jobs 7
Recorded rc: 0
CPU clock: {'cpu_hz': 100000000, 'cpu_cd': 'sys', 'sys_hz': 100000000, 'label': "CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz"}
Groups 96; refusals 0; budget misses 7; share misses 0.
Counts: {'paths': 92, 'path_misses': 4, 'instances': 950, 'instance_misses': 7}

| Cost | Round 2 peak cycles | Round 3 peak cycles | Delta cycles | New measurement + 5%, rounded up to 5 us | Existing statement us | Worst group |
|---|---:|---:|---:|---:|---:|---|
| polls.acmp | 4355 | 4922 | +567 | 55 | 55 | backlog-owed |
| polls.acmp_declined | 1369 | 1711 | +342 | 20 | 20 | backlog-owed |
| polls.acmp_kept | 6362 | 6673 | +311 | 75 | 280 | backlog-owed |
| polls.aecp | 18069 | 18290 | +221 | 195 | 210 | aecp-fanout |
| polls.aecp_long | 34523 | 34220 | -303 | 360 | 365 | aecp-largest-notice |
| polls.base | 21322 | 19032 | -2290 | 200 | 225 | save-held |
| polls.mrpdu | 0 | 0 | +0 | 0 | 735 | acmp-notk |
| polls.rebuild | 20811 | 17121 | -3690 | 180 | 290 | fixture |
| polls.reclaim | 1186 | 1590 | +404 | 20 | 25 | srp |
| polls.record | 25078 | 23799 | -1279 | 250 | 280 | backlog-adp@blank-aged1-1 |
| polls.retained | 0 | 0 | +0 | 0 | 280 | acmp-notk |
| polls.walk | 2733 | 1998 | -735 | 25 | 35 | srp |
| polls.withdraw | 4951 | 4985 | +34 | 55 | 90 | backlog |
| stated.build | 0 | 0 | +0 | 0 | 1010 | acmp-notk |
| stated.build-one | 56000 | 51450 | -4550 | 545 | 735 | srp |
| stated.step | 81231 | 80620 | -611 | 850 | 975 | save-starved |

Peak cycles are the maxima in this run, not replacements for cross-arm cost statements. Zero means this cost is not directly staged by these groups. The rule column is the remeasurement plus 5%, rounded upward to 5 us; existing statements are retained where larger measurements from other approved arms support them.

| SRP / THE TRANSMIT path | Worst ms | Approved bound ms | Within bound | Worst group |
|---|---:|---:|---|---|
| held.srp | 8.07806 | 20.0 | True | save-starved |
| mrpdu | 1.87123 | 20.0 | True | save-starved |
| service.srp.first | 5.97565 | 20.0 | True | backlog-adp@program-aged2-5 |
| service.srp.last | 9.78783 | 20.0 | True | backlog-adp@program-aged2-6 |
| srp.domain | 0.80442 | 220.0 | True | srp |
| srp.listener_ready | 0.419 | 20.0 | True | srp |
| srp.malformed | 0.19427 | 20.0 | True | fixture |
| srp.startup | 0.74878 | 20.0 | True | srp |

THE TRANSMIT timer outcomes, all groups: {'released': 926, 'empty': 603, 'late': 0, 'absent': 0, 'unresolved': 0}. Late means past the unchanged 49 ms bound.
Join intervals: 189.053 to 190.07 ms, approved 181 to 239 ms.

Round 2 budget misses, for comparison:
backlog.owed.if0: 62.917 ms over its budget 20 ms
backlog.owed_behind0.if0: 63.105 ms over its budget 20 ms
backlog.owed_behind1.if0: 63.292 ms over its budget 20 ms
backlog.owed_behind2.if0: 63.479 ms over its budget 20 ms
backlog.owed_behind3.if0: 63.665 ms over its budget 20 ms
backlog-owed.service.acmp.last.if0: 62.013 ms over its budget 20 ms
backlog-owed.service.aecp.last.if0: 61.753 ms over its budget 20 ms

Round 3 budget misses (no suppression in this record):
backlog.owed.if0: 62.842 ms over its budget 20 ms
backlog.owed_behind0.if0: 63.014 ms over its budget 20 ms
backlog.owed_behind1.if0: 63.183 ms over its budget 20 ms
backlog.owed_behind2.if0: 63.352 ms over its budget 20 ms
backlog.owed_behind3.if0: 63.521 ms over its budget 20 ms
backlog-owed.service.acmp.last.if0: 62.006 ms over its budget 20 ms
backlog-owed.service.aecp.last.if0: 61.756 ms over its budget 20 ms

Refusals:

Share misses:

All over-statement/timer records:

Total over-statement/timer records: 0
