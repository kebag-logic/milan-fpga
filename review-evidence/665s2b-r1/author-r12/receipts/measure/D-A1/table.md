### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 3.030 (3.343) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 2.415 (3.232) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.107 (0.335) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 0.784 (1.287) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 61.936 (62.163) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.201 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 0.655 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 4.342 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 0.697 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 3.179 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 0.691 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 62.748 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 0.680 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 3.215 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 2.499 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 9.490 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 5.990 | 19 | 74,136 (0.741) | yes | - |
| backlog-adp | 0 | 9.775 | 19 | 97,517 (0.975) | yes | - |
| backlog-adp-refill | 0 | 40.499 | 29 | 97,517 (0.975) | yes | - |
| backlog-owed | 0 | 360.251 | 65 | 96,670 (0.967) | yes | - |

Composed maximum over the 4 backlog windows: 97,517 CPU cycles (0.975 ms), backlog-adp.
Over the windows that released their whole load only: 97,517 (0.975 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 293 | 0 | 74,136 (0.741) | fits |
| backlog-adp | 313 | 0 | 97,517 (0.975) | fits |
| backlog-adp-refill | 323 | 0 | 97,517 (0.975) | fits |
| backlog-owed | 350 | 0 | 96,670 (0.967) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 78,409 | 0.784 | 20 | 200 | fits | 58,800 | 104 | 0.500 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 302,971 | 3.030 | 20 | 20 | fits | 40,742 | 44 | 0.493 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 69,741 | 0.697 | 20 | 200 | fits | 69,949 | 138 | 0.511 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 251,443 | 2.514 | 20 | 200 | fits | 49,375 | 55 | 0.553 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 65,482 | 0.655 | 20 | 20 | fits | 69,949 | 138 | 0.511 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 328,995 | 3.290 | 20 | 20 | fits | 40,742 | 44 | 0.493 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 69,067 | 0.691 | 20 | 24 | fits | 69,949 | 138 | 0.511 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 548,730 | 5.487 | 20 | 24 | fits | 21,544 | 29 | 0.500 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 68,027 | 0.680 | 20 | 50 | fits | 69,949 | 138 | 0.511 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 249,948 | 2.499 | 20 | 50 | fits | 49,375 | 55 | 0.553 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 249,883 | 2.499 | 18 | 18 | fits | 49,375 | 55 | 0.553 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 573,546 | 5.735 | 18 | 18 | fits | 8,716 | 17 | 0.397 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 241,503 | 2.415 | 20 | 20 | fits | 82,893 | 81 | 0.667 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 59,098 | 0.591 | 20 | 200 | fits | 63,780 | 135 | 0.482 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 317,864 | 3.179 | 20 | 200 | fits | 82,893 | 81 | 0.667 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 60,010 | 0.600 | 20 | 20 | fits | 63,780 | 135 | 0.482 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 434,177 | 4.342 | 20 | 20 | fits | 66,711 | 50 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 63,595 | 0.636 | 20 | 24 | fits | 63,780 | 135 | 0.482 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 871,675 | 8.717 | 20 | 24 | fits | 43,442 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 62,555 | 0.626 | 20 | 50 | fits | 63,780 | 135 | 0.482 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 321,540 | 3.215 | 20 | 50 | fits | 82,893 | 81 | 0.667 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 159,617 | 1.596 | 18 | 18 | fits | 97,517 | 138 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 948,996 | 9.490 | 18 | 18 | fits | 20,629 | 14 | 0.823 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 10,709 | 0.107 | 20 | 20 | fits | 20,334 | 20 | 0.776 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 59,098 | 0.591 | 20 | 200 | fits | 63,780 | 135 | 0.482 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 25,520 | 0.255 | 20 | 200 | fits | 20,334 | 20 | 0.776 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 60,010 | 0.600 | 20 | 20 | fits | 63,780 | 135 | 0.482 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 424,673 | 4.247 | 20 | 20 | fits | 66,652 | 50 | 0.682 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 63,595 | 0.636 | 20 | 24 | fits | 63,780 | 135 | 0.482 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 870,649 | 8.706 | 20 | 24 | fits | 43,449 | 29 | 0.733 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 62,555 | 0.626 | 20 | 50 | fits | 63,780 | 135 | 0.482 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 312,121 | 3.121 | 20 | 50 | fits | 73,474 | 71 | 0.659 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 159,617 | 1.596 | 18 | 18 | fits | 97,517 | 138 | 0.622 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 927,355 | 9.274 | 18 | 18 | fits | 28,891 | 17 | 0.789 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,193,562 | 61.936 | 20 | 20 | MISS ceiling | 26,384 | 25 | 0.600 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,020,062 | 360.201 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,019,987 | 360.200 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,019,912 | 360.199 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,019,837 | 360.198 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 67,668 | 0.677 | 20 | 200 | fits | 61,611 | 129 | 0.485 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 313,367 | 3.134 | 20 | 200 | fits | 72,558 | 67 | 0.676 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 63,409 | 0.634 | 20 | 20 | fits | 61,611 | 129 | 0.485 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 421,073 | 4.211 | 20 | 20 | fits | 54,551 | 33 | 0.773 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 66,994 | 0.670 | 20 | 24 | fits | 61,611 | 129 | 0.485 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,274,817 | 62.748 | 20 | 24 | MISS ceiling | 20,825 | 21 | 0.628 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 65,954 | 0.660 | 20 | 50 | fits | 61,611 | 129 | 0.485 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 311,872 | 3.119 | 20 | 50 | fits | 72,558 | 67 | 0.676 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 162,169 | 1.622 | 18 | 18 | fits | 96,670 | 131 | 0.648 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 765,491 | 7.655 | 18 | 18 | fits | 21,277 | 17 | 0.824 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
