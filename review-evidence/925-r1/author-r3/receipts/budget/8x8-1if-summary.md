CPU budget 8x8-1if: measured 7a2def7c, both firmware ELFs relink byte-identical at 5f625090.
run.py --point 8x8-1if --build-dir <output> --record-budget-findings --record-share-findings --jobs 7
Recorded rc: 1
CPU clock: {'cpu_hz': 100000000, 'cpu_cd': 'sys', 'sys_hz': 100000000, 'label': "CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz"}
Groups 95; refusals 0; budget misses 7; share misses 0.
Counts: {'paths': 85, 'path_misses': 4, 'instances': 947, 'instance_misses': 7}

| Cost | Round 2 peak cycles | Round 3 peak cycles | Delta cycles | New measurement + 5%, rounded up to 5 us | Existing statement us | Worst group |
|---|---:|---:|---:|---:|---:|---|
| polls.acmp | 6656 | 6391 | -265 | 70 | 55 | backlog-owed |
| polls.acmp_declined | 2522 | 2196 | -326 | 25 | 20 | backlog-owed |
| polls.acmp_kept | 8630 | 8686 | +56 | 95 | 280 | backlog-owed |
| polls.aecp | 13812 | 13796 | -16 | 145 | 210 | aecp-fanout |
| polls.aecp_long | 0 | 0 | +0 | 0 | 365 | save-second |
| polls.base | 24499 | 27000 | +2501 | 285 | 225 | save-held |
| polls.mrpdu | 0 | 0 | +0 | 0 | 735 | save-second |
| polls.rebuild | 20026 | 19856 | -170 | 210 | 290 | adp-link |
| polls.reclaim | 864 | 959 | +95 | 15 | 25 | srp |
| polls.record | 21816 | 22220 | +404 | 235 | 280 | backlog-adp@blank-aged1-1 |
| polls.retained | 0 | 0 | +0 | 0 | 280 | save-second |
| polls.walk | 2145 | 1955 | -190 | 25 | 35 | srp |
| polls.withdraw | 5807 | 6121 | +314 | 65 | 90 | backlog |
| stated.build | 0 | 0 | +0 | 0 | 1010 | save-second |
| stated.build-one | 42765 | 42473 | -292 | 450 | 735 | srp |
| stated.step | 80906 | 81048 | +142 | 855 | 975 | backlog-adp@program-aged2-4 |

Peak cycles are the maxima in this run, not replacements for cross-arm cost statements. Zero means this cost is not directly staged by these groups. The rule column is the remeasurement plus 5%, rounded upward to 5 us; existing statements are retained where larger measurements from other approved arms support them.

| SRP / THE TRANSMIT path | Worst ms | Approved bound ms | Within bound | Worst group |
|---|---:|---:|---|---|
| held.srp | 9.04504 | 20.0 | True | save-starved |
| mrpdu | 2.62353 | 20.0 | True | save-starved |
| service.srp.first | 6.50317 | 20.0 | True | backlog-adp@program-aged2-6 |
| service.srp.last | 10.51546 | 20.0 | True | backlog-adp@verify-aged2-5 |
| srp.domain | 0.80499 | 220.0 | True | srp |
| srp.listener_ready | 0.46937 | 20.0 | True | srp |
| srp.malformed | 0.27059 | 20.0 | True | fixture |
| srp.startup | 0.84179 | 20.0 | True | srp |

THE TRANSMIT timer outcomes, all groups: {'released': 1168, 'empty': 866, 'late': 0, 'absent': 0, 'unresolved': 0}. Late means past the unchanged 49 ms bound.
Join intervals: 188.316 to 190.122 ms, approved 181 to 239 ms.

Round 2 budget misses, for comparison:
backlog.owed.if0: 63.529 ms over its budget 20 ms
backlog.owed_behind0.if0: 63.771 ms over its budget 20 ms
backlog.owed_behind1.if0: 64.012 ms over its budget 20 ms
backlog.owed_behind2.if0: 64.253 ms over its budget 20 ms
backlog.owed_behind3.if0: 64.494 ms over its budget 20 ms
backlog-owed.service.acmp.last.if0: 62.379 ms over its budget 20 ms
backlog-owed.service.aecp.last.if0: 62.018 ms over its budget 20 ms

Round 3 budget misses (no suppression in this record):
backlog.owed.if0: 63.520 ms over its budget 20 ms
backlog.owed_behind0.if0: 63.775 ms over its budget 20 ms
backlog.owed_behind1.if0: 64.029 ms over its budget 20 ms
backlog.owed_behind2.if0: 64.282 ms over its budget 20 ms
backlog.owed_behind3.if0: 64.582 ms over its budget 20 ms
backlog-owed.service.acmp.last.if0: 62.336 ms over its budget 20 ms
backlog-owed.service.aecp.last.if0: 61.973 ms over its budget 20 ms

Refusals:

Share misses:

All over-statement/timer records:
('save-second', 'polls', {'kind': 'base', 'start_sys': 274272543, 'cycles': 25957})
('save-second', 'polls', {'kind': 'base', 'start_sys': 379304872, 'cycles': 25933})
('save-held', 'polls', {'kind': 'base', 'start_sys': 271580961, 'cycles': 27000})
('save-starved', 'polls', {'kind': 'base', 'start_sys': 271580961, 'cycles': 27000})
('backlog-adp@blank-0', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-1', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-2', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-3', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-4', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-5', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-6', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-7', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-0', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-1', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-2', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-3', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-4', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-5', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-6', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-7', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-0', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-1', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-2', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-3', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-4', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-5', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-6', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-7', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged2-0', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged2-1', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged2-2', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged2-3', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged2-4', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged2-5', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged2-6', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged2-7', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged1-0', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged1-1', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged1-2', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged1-3', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged1-4', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged1-5', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged1-6', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@blank-aged1-7', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged2-0', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged2-1', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged2-2', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged2-3', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged2-4', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged2-5', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged2-6', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged2-7', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged1-0', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged1-1', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged1-2', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged1-3', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged1-4', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged1-5', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged1-6', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@program-aged1-7', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged2-0', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged2-1', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged2-2', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged2-3', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged2-4', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged2-5', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged2-6', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged2-7', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged1-0', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged1-1', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged1-2', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged1-3', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged1-4', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged1-5', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged1-6', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('backlog-adp@verify-aged1-7', 'polls', {'kind': 'base', 'start_sys': 181431077, 'cycles': 25522})
('save', 'polls', {'kind': 'base', 'start_sys': 71412238, 'cycles': 25404})
('backlog-owed', 'polls', {'kind': 'acmp', 'start_sys': 282781266, 'cycles': 6391})
('backlog-owed', 'polls', {'kind': 'acmp', 'start_sys': 282934436, 'cycles': 5875})
('backlog-owed', 'polls', {'kind': 'acmp_declined', 'start_sys': 277057331, 'cycles': 2196})
('backlog-owed', 'polls', {'kind': 'acmp_declined', 'start_sys': 282796368, 'cycles': 2049})
('backlog-owed', 'polls', {'kind': 'acmp_declined', 'start_sys': 282948669, 'cycles': 2137})
('backlog-owed', 'polls', {'kind': 'acmp_declined', 'start_sys': 282987324, 'cycles': 2114})
('aecp-fanout', 'polls', {'kind': 'base', 'start_sys': 81860700, 'cycles': 24249})
('acmp-cmd', 'polls', {'kind': 'base', 'start_sys': 71929545, 'cycles': 24423})
('aecp', 'polls', {'kind': 'base', 'start_sys': 85357301, 'cycles': 22676})
('fixture', 'polls', {'kind': 'base', 'start_sys': 24878460, 'cycles': 22543})

Total over-statement/timer records: 87
