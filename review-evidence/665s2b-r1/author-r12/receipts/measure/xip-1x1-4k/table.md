### 1x1

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

16 of 16 paths and 49 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 144.199 (162.055) | MISS ceiling | 11 acmp | 1 | 1 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 117.482 (153.917) | MISS ceiling | 7 adp | 1 | 1 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 145.130 (174.237) | MISS ceiling | 6 adp | 1 | 1 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 32.337 (59.653) | MISS T_svc | 15 events | 1 | 1 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 230.709 (239.274) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind3.if0` (backlog-owed) | at least 860.000 | NEVER ANSWERED | 11 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog-adp.service.acmp.first.if0` (backlog-adp) | 34.445 | MISS ceiling | 0 acmp | 4 | 4 |
| ACMP record released under the composed load, last | 0 | `backlog-adp-refill.service.acmp.last.if0` (backlog-adp-refill) | 208.674 | MISS ceiling | 11 acmp | 4 | 4 |
| ADP record released under the composed load, first | 0 | `backlog-adp.service.adp.first.if0` (backlog-adp) | 34.436 | MISS T_svc | 0 adp | 4 | 4 |
| ADP record released under the composed load, last | 0 | `backlog-adp-refill.service.adp.last.if0` (backlog-adp-refill) | 168.718 | MISS T_svc | 6 adp | 4 | 4 |
| AECP record released under the composed load, first | 0 | `backlog-adp.service.aecp.first.if0` (backlog-adp) | 34.481 | MISS ceiling | 0 aecp | 4 | 4 |
| AECP record released under the composed load, last | 0 | `backlog-adp.service.aecp.last.if0` (backlog-adp) | 462.474 | MISS ceiling | 15 aecp | 4 | 4 |
| MAAP record released under the composed load, first | 0 | `backlog-adp.service.maap.first.if0` (backlog-adp) | 34.470 | MISS T_svc | 0 maap | 4 | 4 |
| MAAP record released under the composed load, last | 0 | `backlog-adp.service.maap.last.if0` (backlog-adp) | 143.816 | MISS ceiling | 6 maap | 4 | 4 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 490.362 | MISS ceiling | 0 srp | 4 | 4 |
| SRP record released under the composed load, last | 0 | `backlog-adp-refill.service.srp.last.if0` (backlog-adp-refill) | at least 685.095 | STARVED: never released | 31 srp | 4 | 4 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Event records held at its opening | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---:|---|---|
| backlog | 0 | 644.252 | 56 | 3,480,780 (34.808) | yes | - |
| backlog-adp | 0 | 617.535 | 22 | 4,025,468 (40.255) | no | {'srp': 26} |
| backlog-adp-refill | 0 | 685.132 | 25 | 3,854,869 (38.549) | no | {'srp': 23} |
| backlog-owed | 0 | 860.053 | 52 | 3,166,066 (31.661) | yes | - |

Composed maximum over the 4 backlog windows: at least 4,025,468 CPU cycles (40.255 ms), backlog-adp, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).
Over the windows that released their whole load only: 3,480,780 (34.808 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 323 | 323 | 3,480,780 (34.808) | OVER the share |
| backlog-adp | 296 | 296 | 4,025,468 (40.255) | OVER the share |
| backlog-adp-refill | 299 | 299 | 3,854,869 (38.549) | OVER the share |
| backlog-owed | 330 | 330 | 3,166,066 (31.661) | OVER the share |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 3,233,750 | 32.337 | 20 | 200 | MISS T_svc | 2,504,606 | 104 | 0.720 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 14,419,889 | 144.199 | 20 | 20 | MISS ceiling | 2,155,066 | 47 | 0.794 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 2,880,549 | 28.805 | 20 | 200 | MISS T_svc | 2,705,373 | 138 | 0.706 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 11,237,129 | 112.371 | 20 | 200 | MISS T_svc | 2,371,803 | 64 | 0.756 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 2,876,290 | 28.763 | 20 | 20 | MISS ceiling | 2,705,373 | 138 | 0.706 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 15,620,284 | 156.203 | 20 | 20 | MISS ceiling | 2,155,066 | 47 | 0.794 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 2,879,875 | 28.799 | 20 | 24 | MISS ceiling | 2,705,373 | 138 | 0.706 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 28,893,301 | 288.933 | 20 | 24 | MISS ceiling | 1,269,555 | 26 | 0.822 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 2,878,835 | 28.788 | 20 | 50 | MISS T_svc | 2,705,373 | 138 | 0.706 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 11,235,634 | 112.356 | 20 | 50 | MISS ceiling | 2,371,803 | 64 | 0.756 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 19,691,524 | 196.915 | 18 | 18 | MISS ceiling | 1,414,196 | 41 | 0.769 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 38,496,098 | 384.961 | 18 | 18 | MISS ceiling | 734,728 | 23 | 0.796 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 11,748,177 | 117.482 | 20 | 20 | MISS ceiling | 4,025,468 | 137 | 0.785 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 3,443,554 | 34.436 | 20 | 200 | MISS T_svc | 3,026,700 | 146 | 0.723 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 14,377,960 | 143.780 | 20 | 200 | MISS T_svc | 4,025,468 | 137 | 0.785 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 3,444,466 | 34.445 | 20 | 20 | MISS ceiling | 3,026,700 | 146 | 0.723 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 20,773,748 | 207.737 | 20 | 20 | MISS ceiling | 3,117,542 | 88 | 0.807 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 3,448,051 | 34.481 | 20 | 24 | MISS ceiling | 3,026,700 | 146 | 0.723 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 46,247,385 | 462.474 | 20 | 24 | MISS ceiling | 2,372,834 | 73 | 0.828 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 3,447,011 | 34.470 | 20 | 50 | MISS T_svc | 3,026,700 | 146 | 0.723 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 14,381,636 | 143.816 | 20 | 50 | MISS ceiling | 4,025,468 | 137 | 0.785 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 49,036,234 | 490.362 | 18 | 18 | MISS ceiling | 2,789,369 | 62 | 0.894 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 61,749,773 | 617.498 | 18 | 18 | STARVED: never released | 0 | - | 0.000 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 14,513,024 | 145.130 | 20 | 20 | MISS ceiling | 3,546,311 | 99 | 0.809 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 3,443,554 | 34.436 | 20 | 200 | MISS T_svc | 3,026,700 | 146 | 0.723 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 16,871,762 | 168.718 | 20 | 200 | MISS T_svc | 3,546,311 | 99 | 0.809 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 3,444,466 | 34.445 | 20 | 20 | MISS ceiling | 3,026,700 | 146 | 0.723 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 20,867,374 | 208.674 | 20 | 20 | MISS ceiling | 3,546,311 | 99 | 0.809 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 3,448,051 | 34.481 | 20 | 24 | MISS ceiling | 3,026,700 | 146 | 0.723 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 45,874,483 | 458.745 | 20 | 24 | MISS ceiling | 2,295,201 | 67 | 0.832 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 3,447,011 | 34.470 | 20 | 50 | MISS T_svc | 3,026,700 | 146 | 0.723 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 14,019,219 | 140.192 | 20 | 50 | MISS ceiling | 3,663,051 | 130 | 0.774 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 48,740,965 | 487.410 | 18 | 18 | MISS ceiling | 2,867,002 | 68 | 0.887 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 68,509,536 | 685.095 | 18 | 18 | STARVED: never released | 0 | - | 0.000 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 23,070,939 | 230.709 | 20 | 20 | MISS ceiling | 2,248,171 | 41 | 0.840 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 24,940,397 | 249.404 | 20 | 20 | MISS ceiling | 2,450,333 | 40 | 0.850 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 27,890,266 | 278.903 | 20 | 20 | MISS ceiling | 2,985,589 | 51 | 0.847 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 30,880,219 | 308.802 | 20 | 20 | MISS ceiling | 2,374,450 | 47 | 0.839 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 85,999,996 | 860.000 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 2,663,513 | 26.635 | 20 | 200 | MISS T_svc | 2,731,950 | 129 | 0.734 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 11,136,599 | 111.366 | 20 | 200 | MISS T_svc | 2,707,411 | 79 | 0.778 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 2,659,254 | 26.593 | 20 | 20 | MISS ceiling | 2,731,950 | 129 | 0.734 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 15,781,773 | 157.818 | 20 | 20 | MISS ceiling | 2,244,799 | 43 | 0.822 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 2,662,839 | 26.628 | 20 | 24 | MISS ceiling | 2,731,950 | 129 | 0.734 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 36,409,796 | 364.098 | 20 | 24 | MISS ceiling | 2,033,004 | 37 | 0.846 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 2,661,799 | 26.618 | 20 | 50 | MISS T_svc | 2,731,950 | 129 | 0.734 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 11,135,104 | 111.351 | 20 | 50 | MISS ceiling | 2,707,411 | 79 | 0.778 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 19,992,334 | 199.923 | 18 | 18 | MISS ceiling | 2,582,820 | 41 | 0.858 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 64,300,564 | 643.006 | 18 | 18 | MISS ceiling | 1,975,965 | 29 | 0.898 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-adp-refill`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
- `backlog-owed`: wait tx TIMEOUT
- `backlog-owed`: wait quiet TIMEOUT
