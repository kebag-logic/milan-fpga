### 8x8-1if

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 5.639 (6.111) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 3.841 (4.936) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.194 (0.681) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.286 (2.214) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.413 (63.896) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.331 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.153 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 7.226 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.196 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 4.923 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.189 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 64.602 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.179 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-adp-refill.service.maap.last.if0` (backlog-adp-refill) | 4.993 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 4.573 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 14.421 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 9.787 | 19 | 150,100 (1.501) | yes | - |
| backlog-adp | 0 | 15.446 | 21 | 157,921 (1.579) | yes | - |
| backlog-adp-refill | 0 | 40.990 | 28 | 157,921 (1.579) | yes | - |
| backlog-owed | 0 | 360.382 | 64 | 154,078 (1.541) | yes | - |

Composed maximum over the 4 backlog windows: 157,921 CPU cycles (1.579 ms), backlog-adp.
Over the windows that released their whole load only: 157,921 (1.579 ms), backlog-adp.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 293 | 0 | 150,100 (1.501) | fits |
| backlog-adp | 312 | 0 | 157,921 (1.579) | fits |
| backlog-adp-refill | 319 | 0 | 157,921 (1.579) | fits |
| backlog-owed | 349 | 0 | 154,078 (1.541) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 128,598 | 1.286 | 20 | 200 | fits | 101,584 | 104 | 0.497 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 563,893 | 5.639 | 20 | 20 | fits | 75,269 | 44 | 0.487 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 119,573 | 1.196 | 20 | 200 | fits | 119,781 | 138 | 0.519 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 458,891 | 4.589 | 20 | 200 | fits | 88,243 | 55 | 0.550 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 115,314 | 1.153 | 20 | 20 | fits | 119,781 | 138 | 0.519 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 605,787 | 6.058 | 20 | 20 | fits | 75,269 | 44 | 0.487 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 118,899 | 1.189 | 20 | 24 | fits | 119,781 | 138 | 0.519 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 890,244 | 8.902 | 20 | 24 | fits | 27,296 | 29 | 0.472 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 117,859 | 1.179 | 20 | 50 | fits | 119,781 | 138 | 0.519 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 457,396 | 4.574 | 20 | 50 | fits | 88,243 | 55 | 0.550 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 457,331 | 4.573 | 18 | 18 | fits | 88,243 | 55 | 0.550 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 934,131 | 9.341 | 18 | 18 | fits | 15,261 | 17 | 0.292 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 384,108 | 3.841 | 20 | 20 | fits | 117,078 | 78 | 0.611 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 105,307 | 1.053 | 20 | 200 | fits | 109,989 | 135 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 488,343 | 4.883 | 20 | 200 | fits | 117,078 | 78 | 0.611 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 106,219 | 1.062 | 20 | 20 | fits | 109,989 | 135 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 714,391 | 7.144 | 20 | 20 | fits | 109,055 | 44 | 0.686 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 109,804 | 1.098 | 20 | 24 | fits | 109,989 | 135 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 1,272,378 | 12.724 | 20 | 24 | fits | 56,985 | 29 | 0.731 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 108,764 | 1.088 | 20 | 50 | fits | 109,989 | 135 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 492,019 | 4.920 | 20 | 50 | fits | 117,078 | 78 | 0.611 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 266,230 | 2.662 | 18 | 18 | fits | 157,921 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 1,442,145 | 14.421 | 18 | 18 | fits | 42,910 | 17 | 0.787 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 19,446 | 0.194 | 20 | 20 | fits | 42,788 | 20 | 0.780 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 105,307 | 1.053 | 20 | 200 | fits | 109,989 | 135 | 0.494 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 52,669 | 0.527 | 20 | 200 | fits | 42,788 | 20 | 0.780 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 106,219 | 1.062 | 20 | 20 | fits | 109,989 | 135 | 0.494 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 722,615 | 7.226 | 20 | 20 | fits | 109,062 | 44 | 0.685 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 109,804 | 1.098 | 20 | 24 | fits | 109,989 | 135 | 0.494 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 1,311,959 | 13.120 | 20 | 24 | fits | 57,160 | 29 | 0.732 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 108,764 | 1.088 | 20 | 50 | fits | 109,989 | 135 | 0.494 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 499,341 | 4.993 | 20 | 50 | fits | 124,400 | 77 | 0.664 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 266,230 | 2.662 | 18 | 18 | fits | 157,921 | 138 | 0.617 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 1,396,172 | 13.962 | 18 | 18 | fits | 42,950 | 17 | 0.788 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,341,349 | 63.413 | 20 | 20 | MISS ceiling | 45,671 | 25 | 0.601 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,033,107 | 360.331 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,033,032 | 360.330 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,032,957 | 360.330 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,032,882 | 360.329 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 112,560 | 1.126 | 20 | 200 | fits | 106,545 | 129 | 0.498 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 492,305 | 4.923 | 20 | 200 | fits | 121,346 | 67 | 0.680 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 108,301 | 1.083 | 20 | 20 | fits | 106,545 | 129 | 0.498 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 671,128 | 6.711 | 20 | 20 | fits | 89,759 | 33 | 0.775 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 111,886 | 1.119 | 20 | 24 | fits | 106,545 | 129 | 0.498 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 6,460,208 | 64.602 | 20 | 24 | MISS ceiling | 26,920 | 21 | 0.569 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 110,846 | 1.108 | 20 | 50 | fits | 106,545 | 129 | 0.498 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 490,810 | 4.908 | 20 | 50 | fits | 121,346 | 67 | 0.680 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 369,399 | 3.694 | 18 | 18 | fits | 154,078 | 95 | 0.677 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 1,188,547 | 11.885 | 18 | 18 | fits | 43,019 | 20 | 0.782 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
