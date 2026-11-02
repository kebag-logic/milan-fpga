### 8x8

Clock: CPU 100 MHz on sys, the product's split CPU clock, bus 100 MHz.

3 of 17 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 7.561 (8.265) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 3.432 (4.550) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.129 (0.671) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 4.095 (6.151) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.604 (64.129) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.461 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.855 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog.service.acmp.last.if0` (backlog) | 8.212 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.898 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 4.497 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 6.143 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.891 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.917 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.881 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 6.128 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog-adp.service.srp.first.if0` (backlog-adp) | 6.175 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 16.007 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 14.627 | 19 | 210,754 (2.108) | yes | - |
| backlog-adp | 16.583 | 20 | 164,184 (1.642) | yes | - |
| backlog-adp-refill | 41.029 | 29 | 163,971 (1.640) | yes | - |
| backlog-owed | 360.512 | 66 | 178,503 (1.785) | yes | - |

Composed maximum over the 4 backlog windows: 210,754 CPU cycles (2.108 ms), backlog.
Over the windows that released their whole load only: 210,754 (2.108 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 302 | 1 | 210,754 (2.108) | OVER the share |
| backlog-adp | 322 | 0 | 164,184 (1.642) | fits |
| backlog-adp-refill | 331 | 0 | 163,971 (1.640) | fits |
| backlog-owed | 360 | 0 | 178,503 (1.785) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 409,454 | 4.095 | 20 | 200 | fits | 210,754 | 92 | 0.708 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 756,085 | 7.561 | 20 | 20 | fits | 108,954 | 52 | 0.690 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 189,772 | 1.898 | 20 | 200 | fits | 189,980 | 122 | 0.612 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 614,258 | 6.143 | 20 | 200 | fits | 210,754 | 92 | 0.708 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 185,513 | 1.855 | 20 | 20 | fits | 189,980 | 122 | 0.612 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 821,246 | 8.212 | 20 | 20 | fits | 108,954 | 52 | 0.690 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 189,098 | 1.891 | 20 | 24 | fits | 189,980 | 122 | 0.612 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,313,271 | 13.133 | 20 | 24 | fits | 48,782 | 31 | 0.685 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 188,058 | 1.881 | 20 | 50 | fits | 189,980 | 122 | 0.612 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 612,763 | 6.128 | 20 | 50 | fits | 210,754 | 92 | 0.708 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 612,698 | 6.127 | 18 | 18 | fits | 210,754 | 92 | 0.708 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,409,562 | 14.096 | 18 | 18 | fits | 32,524 | 18 | 0.706 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 343,207 | 3.432 | 20 | 20 | fits | 119,277 | 97 | 0.571 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 105,671 | 1.057 | 20 | 200 | fits | 110,353 | 116 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 449,737 | 4.497 | 20 | 200 | fits | 119,277 | 97 | 0.571 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 106,583 | 1.066 | 20 | 20 | fits | 110,353 | 116 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 734,167 | 7.342 | 20 | 20 | fits | 119,550 | 46 | 0.688 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 110,168 | 1.102 | 20 | 24 | fits | 110,353 | 116 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,400,997 | 14.010 | 20 | 24 | fits | 65,095 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 109,128 | 1.091 | 20 | 50 | fits | 110,353 | 116 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 453,413 | 4.534 | 20 | 50 | fits | 119,277 | 97 | 0.571 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 617,532 | 6.175 | 18 | 18 | fits | 164,184 | 52 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 1,600,677 | 16.007 | 18 | 18 | fits | 48,108 | 18 | 0.726 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 12,916 | 0.129 | 20 | 20 | fits | 44,001 | 21 | 0.780 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 105,671 | 1.057 | 20 | 200 | fits | 110,353 | 116 | 0.516 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 49,381 | 0.494 | 20 | 200 | fits | 44,001 | 21 | 0.780 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 106,583 | 1.066 | 20 | 20 | fits | 110,353 | 116 | 0.516 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 714,256 | 7.143 | 20 | 20 | fits | 119,449 | 46 | 0.687 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 110,168 | 1.102 | 20 | 24 | fits | 110,353 | 116 | 0.516 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,384,442 | 13.844 | 20 | 24 | fits | 65,095 | 31 | 0.705 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 109,128 | 1.091 | 20 | 50 | fits | 110,353 | 116 | 0.516 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 433,816 | 4.338 | 20 | 50 | fits | 99,680 | 87 | 0.552 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 597,722 | 5.977 | 18 | 18 | fits | 163,971 | 52 | 0.744 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 1,584,098 | 15.841 | 18 | 18 | fits | 48,108 | 18 | 0.726 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,360,356 | 63.604 | 20 | 20 | MISS ceiling | 48,866 | 27 | 0.564 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,046,139 | 360.461 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,046,064 | 360.461 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,045,989 | 360.460 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,045,914 | 360.459 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 113,032 | 1.130 | 20 | 200 | fits | 107,184 | 110 | 0.521 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 501,641 | 5.016 | 20 | 200 | fits | 178,503 | 92 | 0.698 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 108,773 | 1.088 | 20 | 20 | fits | 107,184 | 110 | 0.521 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 700,469 | 7.005 | 20 | 20 | fits | 99,024 | 35 | 0.749 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 112,358 | 1.124 | 20 | 24 | fits | 107,184 | 110 | 0.521 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,491,739 | 64.917 | 20 | 24 | MISS ceiling | 30,591 | 23 | 0.548 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 111,318 | 1.113 | 20 | 50 | fits | 107,184 | 110 | 0.521 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 500,146 | 5.001 | 20 | 50 | fits | 178,503 | 92 | 0.698 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 500,081 | 5.001 | 18 | 18 | fits | 178,503 | 92 | 0.698 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,335,715 | 13.357 | 18 | 18 | fits | 48,054 | 21 | 0.726 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
