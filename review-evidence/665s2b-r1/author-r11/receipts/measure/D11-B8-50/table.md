### 8x8

Clock: CPU 50 MHz, the product's split CPU clock (the Milan clock), bus 100 MHz.

4 of 17 paths and 13 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 12.722 (13.855) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 7.226 (9.053) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.166 (1.117) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 3.475 (6.434) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 66.450 (67.176) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.668 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 3.251 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 13.802 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 3.293 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 9.000 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 10.606 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 3.286 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 68.754 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 3.276 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 10.591 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 8.792 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 25.454 | MISS ceiling | 31 srp | 4 | 4 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 24.108 | 18 | 164,764 (3.295) | yes | - |
| backlog-adp | 26.457 | 19 | 150,199 (3.004) | yes | - |
| backlog-adp-refill | 41.993 | 22 | 150,199 (3.004) | yes | - |
| backlog-owed | 360.719 | 64 | 150,389 (3.008) | yes | - |

Composed maximum over the 4 backlog windows: 164,764 CPU cycles (3.295 ms), backlog.
Over the windows that released their whole load only: 164,764 (3.295 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 100,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 301 | 6 | 164,764 (3.295) | OVER the share |
| backlog-adp | 311 | 6 | 150,199 (3.004) | OVER the share |
| backlog-adp-refill | 314 | 6 | 150,199 (3.004) | OVER the share |
| backlog-owed | 359 | 5 | 150,389 (3.008) | OVER the share |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 173,771 | 3.475 | 20 | 200 | fits | 156,950 | 129 | 0.622 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 636,095 | 12.722 | 20 | 20 | fits | 80,846 | 46 | 0.689 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 164,660 | 3.293 | 20 | 200 | fits | 164,764 | 146 | 0.621 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 530,298 | 10.606 | 20 | 200 | fits | 89,942 | 57 | 0.669 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 162,531 | 3.251 | 20 | 20 | fits | 164,764 | 146 | 0.621 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 690,114 | 13.802 | 20 | 20 | fits | 80,846 | 46 | 0.689 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 164,323 | 3.286 | 20 | 24 | fits | 164,764 | 146 | 0.621 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,102,306 | 22.046 | 20 | 24 | MISS T_svc | 40,172 | 31 | 0.723 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 163,803 | 3.276 | 20 | 50 | fits | 164,764 | 146 | 0.621 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 529,550 | 10.591 | 20 | 50 | fits | 89,942 | 57 | 0.669 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 439,576 | 8.792 | 18 | 18 | fits | 119,050 | 85 | 0.686 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,157,647 | 23.153 | 18 | 18 | MISS ceiling | 27,999 | 18 | 0.733 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 361,275 | 7.226 | 20 | 20 | fits | 96,045 | 74 | 0.624 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 92,227 | 1.845 | 20 | 200 | fits | 94,568 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 450,003 | 9.000 | 20 | 200 | fits | 96,045 | 74 | 0.624 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 92,683 | 1.854 | 20 | 20 | fits | 94,568 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 642,551 | 12.851 | 20 | 20 | fits | 84,798 | 34 | 0.725 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 94,476 | 1.890 | 20 | 24 | fits | 94,568 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,205,670 | 24.113 | 20 | 24 | MISS ceiling | 51,124 | 31 | 0.741 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 93,956 | 1.879 | 20 | 50 | fits | 94,568 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 451,841 | 9.037 | 20 | 50 | fits | 96,045 | 74 | 0.624 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 243,927 | 4.879 | 18 | 18 | fits | 150,199 | 140 | 0.638 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,272,688 | 25.454 | 18 | 18 | MISS ceiling | 28,728 | 15 | 0.813 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 8,308 | 0.166 | 20 | 20 | fits | 37,319 | 21 | 0.773 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 92,227 | 1.845 | 20 | 200 | fits | 94,568 | 140 | 0.517 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 39,785 | 0.796 | 20 | 200 | fits | 37,319 | 21 | 0.773 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 92,683 | 1.854 | 20 | 20 | fits | 94,568 | 140 | 0.517 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 641,761 | 12.835 | 20 | 20 | fits | 93,849 | 50 | 0.684 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 94,476 | 1.890 | 20 | 24 | fits | 94,568 | 140 | 0.517 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,165,330 | 23.307 | 20 | 24 | MISS T_svc | 51,124 | 31 | 0.741 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 93,956 | 1.879 | 20 | 50 | fits | 94,568 | 140 | 0.517 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 448,347 | 8.967 | 20 | 50 | fits | 92,551 | 69 | 0.670 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 243,927 | 4.879 | 18 | 18 | fits | 150,199 | 140 | 0.638 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,232,296 | 24.646 | 18 | 18 | MISS ceiling | 28,728 | 15 | 0.813 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 3,322,504 | 66.450 | 20 | 20 | MISS ceiling | 52,361 | 33 | 0.693 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,033,397 | 360.668 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,033,359 | 360.667 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,033,322 | 360.666 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,033,284 | 360.666 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 137,925 | 2.759 | 20 | 200 | fits | 94,590 | 136 | 0.536 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 495,313 | 9.906 | 20 | 200 | fits | 95,304 | 46 | 0.716 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 135,796 | 2.716 | 20 | 20 | fits | 94,590 | 136 | 0.536 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 647,623 | 12.952 | 20 | 20 | fits | 71,923 | 28 | 0.741 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 42,998 | 0.860 | 20 | 24 | fits | 43,753 | 65 | 0.577 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 3,437,678 | 68.754 | 20 | 24 | MISS ceiling | 26,409 | 23 | 0.591 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 42,478 | 0.850 | 20 | 50 | fits | 43,753 | 65 | 0.577 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 399,261 | 7.985 | 20 | 50 | fits | 111,999 | 75 | 0.711 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 287,230 | 5.745 | 18 | 18 | fits | 150,389 | 133 | 0.663 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,088,282 | 21.766 | 18 | 18 | MISS ceiling | 39,294 | 21 | 0.764 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
