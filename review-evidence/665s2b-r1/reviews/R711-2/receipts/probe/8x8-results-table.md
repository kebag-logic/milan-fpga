### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

0 of 29 paths and 0 of 109 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| ACMP record released under the composed load, first | 0 | `x-links-2ms.service.acmp.first.if0` (x-links-2ms) | 1.725 | fits | 0 acmp | 9 | 0 |
| ACMP record released under the composed load, last | 0 | `x-save-2.service.acmp.last.if0` (x-save-2) | 8.100 | fits | 11 acmp | 9 | 0 |
| ADP record released under the composed load, first | 0 | `x-links-same.service.adp.first.if0` (x-links-same) | 1.419 | fits | 0 adp | 9 | 0 |
| ADP record released under the composed load, last | 1 | `x-save-2.service.adp.last.if1` (x-save-2) | 6.125 | fits | 7 adp | 9 | 0 |
| AECP record released under the composed load, first | 0 | `x-links-same.service.aecp.first.if0` (x-links-same) | 1.412 | fits | 0 aecp | 9 | 0 |
| AECP record released under the composed load, last | 1 | `x-save-2.service.aecp.last.if1` (x-save-2) | 13.902 | fits | 15 aecp | 9 | 0 |
| MAAP record released under the composed load, first | 0 | `x-links-same.service.maap.first.if0` (x-links-same) | 1.401 | fits | 0 maap | 9 | 0 |
| MAAP record released under the composed load, last | 0 | `x-save-2.service.maap.last.if0` (x-save-2) | 6.110 | fits | 6 maap | 9 | 0 |
| SRP record released under the composed load, first | 0 | `x-save-1.service.srp.first.if0` (x-save-1) | 6.911 | fits | 0 srp | 9 | 0 |
| SRP record released under the composed load, last | 1 | `x-save-2.service.srp.last.if1` (x-save-2) | 14.859 | fits | 31 srp | 9 | 0 |
| an ACMP command behind a full acmp ring | 0 | `x-links-1ms.acmp_command.if0` (x-links-1ms) | 6.185 (6.814) | fits | 11 acmp | 1 | 0 |
| an event behind 15 others | 0 | `x-links-1ms.event.if0` (x-links-1ms) | 0.917 (2.083) | fits | 14 events | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `x-links-2ms.acmp_command.if0` (x-links-2ms) | 5.840 (6.838) | fits | 11 acmp | 1 | 0 |
| an event behind 15 others | 0 | `x-links-2ms.event.if0` (x-links-2ms) | 0.917 (1.462) | fits | 14 events | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `x-links-same.acmp_command.if0` (x-links-same) | 6.602 (7.122) | fits | 11 acmp | 1 | 0 |
| an event behind 15 others | 0 | `x-links-same.event.if0` (x-links-same) | 1.506 (2.542) | fits | 14 events | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `x-save-0.acmp_command.if0` (x-save-0) | 7.234 (7.951) | fits | 11 acmp | 1 | 0 |
| an event behind 15 others | 0 | `x-save-0.event.if0` (x-save-0) | 1.435 (2.468) | fits | 15 events | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `x-save-1.acmp_command.if0` (x-save-1) | 7.239 (7.949) | fits | 11 acmp | 1 | 0 |
| an event behind 15 others | 0 | `x-save-1.event.if0` (x-save-1) | 1.435 (2.467) | fits | 15 events | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `x-save-2.acmp_command.if0` (x-save-2) | 7.454 (8.153) | fits | 11 acmp | 1 | 0 |
| an event behind 15 others | 0 | `x-save-2.event.if0` (x-save-2) | 1.435 (2.467) | fits | 15 events | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `x-save-3.acmp_command.if0` (x-save-3) | 7.439 (8.136) | fits | 11 acmp | 1 | 0 |
| an event behind 15 others | 0 | `x-save-3.event.if0` (x-save-3) | 1.435 (2.467) | fits | 15 events | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `x-save-4.acmp_command.if0` (x-save-4) | 6.611 (7.309) | fits | 11 acmp | 1 | 0 |
| an event behind 15 others | 0 | `x-save-4.event.if0` (x-save-4) | 1.434 (2.468) | fits | 15 events | 1 | 0 |
| an ACMP command behind a full acmp ring | 0 | `x-save-5.acmp_command.if0` (x-save-5) | 6.611 (7.308) | fits | 11 acmp | 1 | 0 |
| an event behind 15 others | 0 | `x-save-5.event.if0` (x-save-5) | 1.434 (2.468) | fits | 15 events | 1 | 0 |
| first joint link change | 0 | `x.links.if0` (x-links-quiet) | 0.042 (0.794) | fits | 0 events | 1 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| x-links-same | 0 | 11.252 | 20 | 200,378 (2.004) | yes | - |
| x-links-1ms | 0 | 11.513 | 20 | 157,325 (1.573) | yes | - |
| x-links-2ms | 0 | 11.864 | 22 | 131,388 (1.314) | yes | - |
| x-save-0 | 0 | 14.655 | 20 | 183,886 (1.839) | yes | - |
| x-save-1 | 0 | 15.805 | 21 | 201,045 (2.010) | yes | - |
| x-save-2 | 0 | 15.391 | 19 | 210,688 (2.107) | yes | - |
| x-save-3 | 0 | 15.379 | 19 | 238,763 (2.388) | yes | - |
| x-save-4 | 0 | 14.554 | 19 | 155,896 (1.559) | yes | - |
| x-save-5 | 0 | 14.556 | 19 | 155,896 (1.559) | yes | - |

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| x-links-same | 303 | 1 | 200,378 (2.004) | OVER the share |
| x-links-1ms | 303 | 0 | 157,325 (1.573) | fits |
| x-links-2ms | 305 | 0 | 131,388 (1.314) | fits |
| x-save-0 | 304 | 0 | 183,886 (1.839) | fits |
| x-save-1 | 305 | 1 | 201,045 (2.010) | OVER the share |
| x-save-2 | 303 | 1 | 210,688 (2.107) | OVER the share |
| x-save-3 | 303 | 1 | 238,763 (2.388) | OVER the share |
| x-save-4 | 304 | 0 | 155,896 (1.559) | fits |
| x-save-5 | 304 | 0 | 155,896 (1.559) | fits |
| x-links-quiet | 269 | 0 | 168,179 (1.682) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `x-links-same.event.if0` | 150,607 | 1.506 | 20 | 200 | fits | 112,101 | 115 | 0.492 |
| an ACMP command behind a full acmp ring | `x-links-same.acmp_command.if0` | 660,195 | 6.602 | 20 | 20 | fits | 88,782 | 52 | 0.561 |
| ADP record released under the composed load, first | `x-links-same.service.adp.first.if0` | 141,861 | 1.419 | 20 | 200 | fits | 142,061 | 146 | 0.509 |
| ADP record released under the composed load, last | `x-links-same.service.adp.last.if1` | 546,682 | 5.467 | 20 | 200 | fits | 92,951 | 57 | 0.536 |
| ACMP record released under the composed load, first | `x-links-same.service.acmp.first.if0` | 137,602 | 1.376 | 20 | 20 | fits | 142,061 | 146 | 0.509 |
| ACMP record released under the composed load, last | `x-links-same.service.acmp.last.if0` | 706,908 | 7.069 | 20 | 20 | fits | 88,782 | 52 | 0.561 |
| AECP record released under the composed load, first | `x-links-same.service.aecp.first.if0` | 141,187 | 1.412 | 20 | 24 | fits | 142,061 | 146 | 0.509 |
| AECP record released under the composed load, last | `x-links-same.service.aecp.last.if1` | 1,010,651 | 10.107 | 20 | 24 | fits | 29,874 | 31 | 0.414 |
| MAAP record released under the composed load, first | `x-links-same.service.maap.first.if0` | 140,147 | 1.401 | 20 | 50 | fits | 142,061 | 146 | 0.509 |
| MAAP record released under the composed load, last | `x-links-same.service.maap.last.if0` | 545,187 | 5.452 | 20 | 50 | fits | 92,951 | 57 | 0.536 |
| SRP record released under the composed load, first | `x-links-same.service.srp.first.if0` | 545,122 | 5.451 | 18 | 18 | fits | 92,951 | 57 | 0.536 |
| SRP record released under the composed load, last | `x-links-same.service.srp.last.if1` | 1,075,912 | 10.759 | 18 | 18 | fits | 16,746 | 18 | 0.140 |
| an event behind 15 others | `x-links-1ms.event.if0` | 91,696 | 0.917 | 20 | 200 | fits | 124,908 | 123 | 0.545 |
| an ACMP command behind a full acmp ring | `x-links-1ms.acmp_command.if0` | 618,513 | 6.185 | 20 | 20 | fits | 77,769 | 46 | 0.480 |
| ADP record released under the composed load, first | `x-links-1ms.service.adp.first.if0` | 83,168 | 0.832 | 20 | 200 | fits | 83,368 | 128 | 0.499 |
| ADP record released under the composed load, last | `x-links-1ms.service.adp.last.if1` | 514,346 | 5.143 | 20 | 200 | fits | 149,554 | 50 | 0.646 |
| ACMP record released under the composed load, first | `x-links-1ms.service.acmp.first.if0` | 108,088 | 1.081 | 20 | 20 | fits | 124,908 | 123 | 0.545 |
| ACMP record released under the composed load, last | `x-links-1ms.service.acmp.last.if0` | 663,787 | 6.638 | 20 | 20 | fits | 77,769 | 46 | 0.480 |
| AECP record released under the composed load, first | `x-links-1ms.service.aecp.first.if0` | 82,494 | 0.825 | 20 | 24 | fits | 83,368 | 128 | 0.499 |
| AECP record released under the composed load, last | `x-links-1ms.service.aecp.last.if1` | 1,036,682 | 10.367 | 20 | 24 | fits | 30,257 | 31 | 0.429 |
| MAAP record released under the composed load, first | `x-links-1ms.service.maap.first.if0` | 81,454 | 0.815 | 20 | 50 | fits | 83,368 | 128 | 0.499 |
| MAAP record released under the composed load, last | `x-links-1ms.service.maap.last.if0` | 512,851 | 5.129 | 20 | 50 | fits | 149,554 | 50 | 0.646 |
| SRP record released under the composed load, first | `x-links-1ms.service.srp.first.if0` | 595,469 | 5.955 | 18 | 18 | fits | 82,683 | 46 | 0.584 |
| SRP record released under the composed load, last | `x-links-1ms.service.srp.last.if1` | 1,102,029 | 11.020 | 18 | 18 | fits | 16,746 | 18 | 0.140 |
| an event behind 15 others | `x-links-2ms.event.if0` | 91,696 | 0.917 | 20 | 200 | fits | 62,870 | 105 | 0.503 |
| an ACMP command behind a full acmp ring | `x-links-2ms.acmp_command.if0` | 584,045 | 5.840 | 20 | 20 | fits | 77,420 | 46 | 0.476 |
| ADP record released under the composed load, first | `x-links-2ms.service.adp.first.if0` | 83,168 | 0.832 | 20 | 200 | fits | 83,368 | 128 | 0.499 |
| ADP record released under the composed load, last | `x-links-2ms.service.adp.last.if1` | 371,874 | 3.719 | 20 | 200 | fits | 101,231 | 62 | 0.626 |
| ACMP record released under the composed load, first | `x-links-2ms.service.acmp.first.if0` | 172,495 | 1.725 | 20 | 20 | fits | 101,231 | 62 | 0.626 |
| ACMP record released under the composed load, last | `x-links-2ms.service.acmp.last.if0` | 628,978 | 6.290 | 20 | 20 | fits | 77,420 | 46 | 0.476 |
| AECP record released under the composed load, first | `x-links-2ms.service.aecp.first.if0` | 82,494 | 0.825 | 20 | 24 | fits | 83,368 | 128 | 0.499 |
| AECP record released under the composed load, last | `x-links-2ms.service.aecp.last.if1` | 1,038,366 | 10.384 | 20 | 24 | fits | 29,874 | 31 | 0.414 |
| MAAP record released under the composed load, first | `x-links-2ms.service.maap.first.if0` | 81,454 | 0.815 | 20 | 50 | fits | 83,368 | 128 | 0.499 |
| MAAP record released under the composed load, last | `x-links-2ms.service.maap.last.if0` | 370,379 | 3.704 | 20 | 50 | fits | 101,231 | 62 | 0.626 |
| SRP record released under the composed load, first | `x-links-2ms.service.srp.first.if0` | 585,913 | 5.859 | 18 | 18 | fits | 84,211 | 46 | 0.581 |
| SRP record released under the composed load, last | `x-links-2ms.service.srp.last.if1` | 1,137,119 | 11.371 | 18 | 18 | fits | 16,746 | 18 | 0.140 |
| an event behind 15 others | `x-save-0.event.if0` | 143,477 | 1.435 | 20 | 200 | fits | 112,536 | 125 | 0.522 |
| an ACMP command behind a full acmp ring | `x-save-0.acmp_command.if0` | 723,363 | 7.234 | 20 | 20 | fits | 183,886 | 52 | 0.544 |
| ADP record released under the composed load, first | `x-save-0.service.adp.first.if0` | 134,070 | 1.341 | 20 | 200 | fits | 134,278 | 143 | 0.531 |
| ADP record released under the composed load, last | `x-save-0.service.adp.last.if1` | 528,174 | 5.282 | 20 | 200 | fits | 126,323 | 57 | 0.675 |
| ACMP record released under the composed load, first | `x-save-0.service.acmp.first.if0` | 129,811 | 1.298 | 20 | 20 | fits | 134,278 | 143 | 0.531 |
| ACMP record released under the composed load, last | `x-save-0.service.acmp.last.if0` | 789,852 | 7.899 | 20 | 20 | fits | 183,886 | 52 | 0.544 |
| AECP record released under the composed load, first | `x-save-0.service.aecp.first.if0` | 133,396 | 1.334 | 20 | 24 | fits | 134,278 | 143 | 0.531 |
| AECP record released under the composed load, last | `x-save-0.service.aecp.last.if1` | 1,284,223 | 12.842 | 20 | 24 | fits | 49,024 | 31 | 0.681 |
| MAAP record released under the composed load, first | `x-save-0.service.maap.first.if0` | 132,356 | 1.324 | 20 | 50 | fits | 134,278 | 143 | 0.531 |
| MAAP record released under the composed load, last | `x-save-0.service.maap.last.if0` | 526,679 | 5.267 | 20 | 50 | fits | 126,323 | 57 | 0.675 |
| SRP record released under the composed load, first | `x-save-0.service.srp.first.if0` | 526,614 | 5.266 | 18 | 18 | fits | 126,323 | 57 | 0.675 |
| SRP record released under the composed load, last | `x-save-0.service.srp.last.if1` | 1,412,201 | 14.122 | 18 | 18 | fits | 32,195 | 18 | 0.684 |
| an event behind 15 others | `x-save-1.event.if0` | 143,477 | 1.435 | 20 | 200 | fits | 112,467 | 125 | 0.521 |
| an ACMP command behind a full acmp ring | `x-save-1.acmp_command.if0` | 723,927 | 7.239 | 20 | 20 | fits | 101,444 | 46 | 0.676 |
| ADP record released under the composed load, first | `x-save-1.service.adp.first.if0` | 134,070 | 1.341 | 20 | 200 | fits | 134,278 | 143 | 0.531 |
| ADP record released under the composed load, last | `x-save-1.service.adp.last.if1` | 491,644 | 4.916 | 20 | 200 | fits | 89,862 | 48 | 0.592 |
| ACMP record released under the composed load, first | `x-save-1.service.acmp.first.if0` | 129,811 | 1.298 | 20 | 20 | fits | 134,278 | 143 | 0.531 |
| ACMP record released under the composed load, last | `x-save-1.service.acmp.last.if0` | 789,658 | 7.897 | 20 | 20 | fits | 101,444 | 46 | 0.676 |
| AECP record released under the composed load, first | `x-save-1.service.aecp.first.if0` | 133,396 | 1.334 | 20 | 24 | fits | 134,278 | 143 | 0.531 |
| AECP record released under the composed load, last | `x-save-1.service.aecp.last.if1` | 1,283,624 | 12.836 | 20 | 24 | fits | 48,962 | 31 | 0.678 |
| MAAP record released under the composed load, first | `x-save-1.service.maap.first.if0` | 132,356 | 1.324 | 20 | 50 | fits | 134,278 | 143 | 0.531 |
| MAAP record released under the composed load, last | `x-save-1.service.maap.last.if0` | 490,149 | 4.901 | 20 | 50 | fits | 89,862 | 48 | 0.592 |
| SRP record released under the composed load, first | `x-save-1.service.srp.first.if0` | 691,129 | 6.911 | 18 | 18 | fits | 201,045 | 52 | 0.592 |
| SRP record released under the composed load, last | `x-save-1.service.srp.last.if1` | 1,411,269 | 14.113 | 18 | 18 | fits | 32,195 | 18 | 0.684 |
| an event behind 15 others | `x-save-2.event.if0` | 143,477 | 1.435 | 20 | 200 | fits | 112,467 | 125 | 0.521 |
| an ACMP command behind a full acmp ring | `x-save-2.acmp_command.if0` | 745,431 | 7.454 | 20 | 20 | fits | 99,557 | 46 | 0.657 |
| ADP record released under the composed load, first | `x-save-2.service.adp.first.if0` | 134,070 | 1.341 | 20 | 200 | fits | 134,278 | 143 | 0.531 |
| ADP record released under the composed load, last | `x-save-2.service.adp.last.if1` | 612,470 | 6.125 | 20 | 200 | fits | 210,688 | 63 | 0.580 |
| ACMP record released under the composed load, first | `x-save-2.service.acmp.first.if0` | 129,811 | 1.298 | 20 | 20 | fits | 134,278 | 143 | 0.531 |
| ACMP record released under the composed load, last | `x-save-2.service.acmp.last.if0` | 810,035 | 8.100 | 20 | 20 | fits | 99,557 | 46 | 0.657 |
| AECP record released under the composed load, first | `x-save-2.service.aecp.first.if0` | 133,396 | 1.334 | 20 | 24 | fits | 134,278 | 143 | 0.531 |
| AECP record released under the composed load, last | `x-save-2.service.aecp.last.if1` | 1,390,163 | 13.902 | 20 | 24 | fits | 134,795 | 37 | 0.547 |
| MAAP record released under the composed load, first | `x-save-2.service.maap.first.if0` | 132,356 | 1.324 | 20 | 50 | fits | 134,278 | 143 | 0.531 |
| MAAP record released under the composed load, last | `x-save-2.service.maap.last.if0` | 610,975 | 6.110 | 20 | 50 | fits | 210,688 | 63 | 0.580 |
| SRP record released under the composed load, first | `x-save-2.service.srp.first.if0` | 610,910 | 6.109 | 18 | 18 | fits | 210,688 | 63 | 0.580 |
| SRP record released under the composed load, last | `x-save-2.service.srp.last.if1` | 1,485,872 | 14.859 | 18 | 18 | fits | 32,171 | 18 | 0.681 |
| an event behind 15 others | `x-save-3.event.if0` | 143,477 | 1.435 | 20 | 200 | fits | 112,467 | 125 | 0.521 |
| an ACMP command behind a full acmp ring | `x-save-3.acmp_command.if0` | 743,852 | 7.439 | 20 | 20 | fits | 99,415 | 46 | 0.655 |
| ADP record released under the composed load, first | `x-save-3.service.adp.first.if0` | 134,070 | 1.341 | 20 | 200 | fits | 134,278 | 143 | 0.531 |
| ADP record released under the composed load, last | `x-save-3.service.adp.last.if1` | 611,188 | 6.112 | 20 | 200 | fits | 126,497 | 57 | 0.677 |
| ACMP record released under the composed load, first | `x-save-3.service.acmp.first.if0` | 129,811 | 1.298 | 20 | 20 | fits | 134,278 | 143 | 0.531 |
| ACMP record released under the composed load, last | `x-save-3.service.acmp.last.if0` | 808,349 | 8.083 | 20 | 20 | fits | 99,415 | 46 | 0.655 |
| AECP record released under the composed load, first | `x-save-3.service.aecp.first.if0` | 133,396 | 1.334 | 20 | 24 | fits | 134,278 | 143 | 0.531 |
| AECP record released under the composed load, last | `x-save-3.service.aecp.last.if1` | 1,389,231 | 13.892 | 20 | 24 | fits | 49,127 | 31 | 0.683 |
| MAAP record released under the composed load, first | `x-save-3.service.maap.first.if0` | 132,356 | 1.324 | 20 | 50 | fits | 134,278 | 143 | 0.531 |
| MAAP record released under the composed load, last | `x-save-3.service.maap.last.if0` | 609,693 | 6.097 | 20 | 50 | fits | 126,497 | 57 | 0.677 |
| SRP record released under the composed load, first | `x-save-3.service.srp.first.if0` | 609,628 | 6.096 | 18 | 18 | fits | 126,497 | 57 | 0.677 |
| SRP record released under the composed load, last | `x-save-3.service.srp.last.if1` | 1,484,728 | 14.847 | 18 | 18 | fits | 32,194 | 18 | 0.684 |
| an event behind 15 others | `x-save-4.event.if0` | 143,402 | 1.434 | 20 | 200 | fits | 112,544 | 125 | 0.522 |
| an ACMP command behind a full acmp ring | `x-save-4.acmp_command.if0` | 661,122 | 6.611 | 20 | 20 | fits | 99,450 | 46 | 0.655 |
| ADP record released under the composed load, first | `x-save-4.service.adp.first.if0` | 134,070 | 1.341 | 20 | 200 | fits | 134,278 | 143 | 0.531 |
| ADP record released under the composed load, last | `x-save-4.service.adp.last.if1` | 528,224 | 5.282 | 20 | 200 | fits | 126,323 | 57 | 0.675 |
| ACMP record released under the composed load, first | `x-save-4.service.acmp.first.if0` | 129,811 | 1.298 | 20 | 20 | fits | 134,278 | 143 | 0.531 |
| ACMP record released under the composed load, last | `x-save-4.service.acmp.last.if0` | 725,619 | 7.256 | 20 | 20 | fits | 99,450 | 46 | 0.655 |
| AECP record released under the composed load, first | `x-save-4.service.aecp.first.if0` | 133,396 | 1.334 | 20 | 24 | fits | 134,278 | 143 | 0.531 |
| AECP record released under the composed load, last | `x-save-4.service.aecp.last.if1` | 1,306,758 | 13.068 | 20 | 24 | fits | 49,127 | 31 | 0.683 |
| MAAP record released under the composed load, first | `x-save-4.service.maap.first.if0` | 132,356 | 1.324 | 20 | 50 | fits | 134,278 | 143 | 0.531 |
| MAAP record released under the composed load, last | `x-save-4.service.maap.last.if0` | 526,729 | 5.267 | 20 | 50 | fits | 126,323 | 57 | 0.675 |
| SRP record released under the composed load, first | `x-save-4.service.srp.first.if0` | 526,664 | 5.267 | 18 | 18 | fits | 126,323 | 57 | 0.675 |
| SRP record released under the composed load, last | `x-save-4.service.srp.last.if1` | 1,402,209 | 14.022 | 18 | 18 | fits | 32,171 | 18 | 0.681 |
| an event behind 15 others | `x-save-5.event.if0` | 143,402 | 1.434 | 20 | 200 | fits | 112,475 | 125 | 0.521 |
| an ACMP command behind a full acmp ring | `x-save-5.acmp_command.if0` | 661,053 | 6.611 | 20 | 20 | fits | 99,450 | 46 | 0.655 |
| ADP record released under the composed load, first | `x-save-5.service.adp.first.if0` | 134,070 | 1.341 | 20 | 200 | fits | 134,278 | 143 | 0.531 |
| ADP record released under the composed load, last | `x-save-5.service.adp.last.if1` | 528,155 | 5.282 | 20 | 200 | fits | 126,323 | 57 | 0.675 |
| ACMP record released under the composed load, first | `x-save-5.service.acmp.first.if0` | 129,811 | 1.298 | 20 | 20 | fits | 134,278 | 143 | 0.531 |
| ACMP record released under the composed load, last | `x-save-5.service.acmp.last.if0` | 725,550 | 7.255 | 20 | 20 | fits | 99,450 | 46 | 0.655 |
| AECP record released under the composed load, first | `x-save-5.service.aecp.first.if0` | 133,396 | 1.334 | 20 | 24 | fits | 134,278 | 143 | 0.531 |
| AECP record released under the composed load, last | `x-save-5.service.aecp.last.if1` | 1,306,950 | 13.069 | 20 | 24 | fits | 49,127 | 31 | 0.683 |
| MAAP record released under the composed load, first | `x-save-5.service.maap.first.if0` | 132,356 | 1.324 | 20 | 50 | fits | 134,278 | 143 | 0.531 |
| MAAP record released under the composed load, last | `x-save-5.service.maap.last.if0` | 526,660 | 5.267 | 20 | 50 | fits | 126,323 | 57 | 0.675 |
| SRP record released under the composed load, first | `x-save-5.service.srp.first.if0` | 526,595 | 5.266 | 18 | 18 | fits | 126,323 | 57 | 0.675 |
| SRP record released under the composed load, last | `x-save-5.service.srp.last.if1` | 1,402,401 | 14.024 | 18 | 18 | fits | 32,171 | 18 | 0.681 |
| first joint link change | `x.links.if0` | 4,153 | 0.042 | 20 | 200 | fits | 59,496 | 38 | 0.654 |

Bounded waits that timed out (the probe is graded on what the log holds):

- none
