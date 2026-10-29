### 8x8

Clock: CPU 50 MHz, the product's split CPU clock (the Milan clock), bus 100 MHz.

4 of 17 paths and 13 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 17.692 (18.582) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 11.693 (13.404) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.355 (1.342) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 3.022 (5.588) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 66.374 (67.337) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.879 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 2.796 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 19.246 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 2.839 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 13.351 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 13.987 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 2.832 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 68.645 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 2.822 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 12.641 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 6.895 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 34.868 | MISS ceiling | 31 srp | 4 | 4 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 30.916 | 35 | 142,049 (2.841) | yes | - |
| backlog-adp | 35.902 | 35 | 104,227 (2.085) | yes | - |
| backlog-adp-refill | 42.003 | 38 | 104,227 (2.085) | yes | - |
| backlog-owed | 360.930 | 79 | 103,034 (2.061) | yes | - |

Composed maximum over the 4 backlog windows: 142,049 CPU cycles (2.841 ms), backlog.
Over the windows that released their whole load only: 142,049 (2.841 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 100,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 318 | 5 | 142,049 (2.841) | OVER the share |
| backlog-adp | 340 | 4 | 119,836 (2.397) | OVER the share |
| backlog-adp-refill | 343 | 4 | 119,836 (2.397) | OVER the share |
| backlog-owed | 379 | 5 | 119,836 (2.397) | OVER the share |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 151,107 | 3.022 | 20 | 200 | fits | 137,371 | 113 | 0.665 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 884,582 | 17.692 | 20 | 20 | fits | 52,607 | 33 | 0.676 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 141,945 | 2.839 | 20 | 200 | fits | 142,049 | 111 | 0.686 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 699,343 | 13.987 | 20 | 200 | fits | 66,545 | 36 | 0.734 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 139,816 | 2.796 | 20 | 20 | fits | 142,049 | 111 | 0.686 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 926,456 | 18.529 | 20 | 20 | fits | 52,607 | 33 | 0.676 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 141,608 | 2.832 | 20 | 24 | fits | 142,049 | 111 | 0.686 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,063,704 | 21.274 | 20 | 24 | MISS T_svc | 27,485 | 26 | 0.607 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 141,088 | 2.822 | 20 | 50 | fits | 142,049 | 111 | 0.686 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 632,050 | 12.641 | 20 | 50 | fits | 59,766 | 39 | 0.671 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 344,727 | 6.895 | 18 | 18 | fits | 66,495 | 45 | 0.678 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,498,112 | 29.962 | 18 | 18 | MISS ceiling | 28,108 | 13 | 0.811 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 584,649 | 11.693 | 20 | 20 | fits | 89,086 | 43 | 0.762 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 71,355 | 1.427 | 20 | 200 | fits | 73,696 | 105 | 0.598 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 667,568 | 13.351 | 20 | 200 | fits | 89,086 | 43 | 0.762 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 71,811 | 1.436 | 20 | 20 | fits | 73,696 | 105 | 0.598 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 962,277 | 19.246 | 20 | 20 | fits | 77,639 | 39 | 0.777 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 73,604 | 1.472 | 20 | 24 | fits | 73,696 | 105 | 0.598 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,142,187 | 22.844 | 20 | 24 | MISS T_svc | 48,782 | 36 | 0.772 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 73,084 | 1.462 | 20 | 50 | fits | 73,696 | 105 | 0.598 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 580,320 | 11.606 | 20 | 50 | fits | 80,509 | 58 | 0.722 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 177,083 | 3.542 | 18 | 18 | fits | 104,227 | 100 | 0.709 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,743,422 | 34.868 | 18 | 18 | MISS ceiling | 30,096 | 13 | 0.812 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 17,758 | 0.355 | 20 | 20 | fits | 39,017 | 20 | 0.804 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 71,355 | 1.427 | 20 | 200 | fits | 73,696 | 105 | 0.598 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 50,591 | 1.012 | 20 | 200 | fits | 39,017 | 20 | 0.804 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 71,811 | 1.436 | 20 | 20 | fits | 73,696 | 105 | 0.598 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 945,989 | 18.920 | 20 | 20 | fits | 77,694 | 39 | 0.778 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 73,604 | 1.472 | 20 | 24 | fits | 73,696 | 105 | 0.598 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,122,313 | 22.446 | 20 | 24 | MISS T_svc | 43,473 | 26 | 0.757 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 73,084 | 1.462 | 20 | 50 | fits | 73,696 | 105 | 0.598 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 580,320 | 11.606 | 20 | 50 | fits | 80,509 | 58 | 0.722 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 177,083 | 3.542 | 18 | 18 | fits | 104,227 | 100 | 0.709 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,730,895 | 34.618 | 18 | 18 | MISS ceiling | 30,096 | 13 | 0.812 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 3,318,698 | 66.374 | 20 | 20 | MISS ceiling | 42,919 | 27 | 0.584 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,043,947 | 360.879 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,043,909 | 360.878 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,043,872 | 360.877 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,043,834 | 360.877 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 75,156 | 1.503 | 20 | 200 | fits | 71,781 | 103 | 0.589 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 640,316 | 12.806 | 20 | 200 | fits | 56,839 | 22 | 0.793 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 73,027 | 1.461 | 20 | 20 | fits | 71,781 | 103 | 0.589 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 835,221 | 16.704 | 20 | 20 | fits | 47,602 | 19 | 0.784 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 74,819 | 1.496 | 20 | 24 | fits | 71,781 | 103 | 0.589 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 3,432,256 | 68.645 | 20 | 24 | MISS ceiling | 26,330 | 23 | 0.563 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 74,299 | 1.486 | 20 | 50 | fits | 71,781 | 103 | 0.589 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 582,729 | 11.655 | 20 | 50 | fits | 66,026 | 44 | 0.731 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 177,106 | 3.542 | 18 | 18 | fits | 103,034 | 97 | 0.720 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,484,048 | 29.681 | 18 | 18 | MISS ceiling | 30,008 | 16 | 0.795 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
