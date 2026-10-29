### 8x8

Clock: CPU 100 MHz, a labelled option: not the product's split CPU clock, 50 MHz, bus 100 MHz.

4 of 17 paths and 8 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 10.422 (11.139) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 7.290 (8.315) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.157 (0.709) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.771 (3.291) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.619 (64.158) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.401 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.625 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 11.790 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.668 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-adp.service.adp.last.if0` (backlog-adp) | 8.262 | fits | 7 adp | 2 | 0 |
| ADP record released under the composed load, last | 1 | `backlog.service.adp.last.if1` (backlog) | 8.322 | fits | 7 adp | 2 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.661 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 1 | `backlog-owed.service.aecp.last.if1` (backlog-owed) | 64.958 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.651 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog.service.maap.last.if0` (backlog) | 7.502 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 3.267 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 1 | `backlog-adp.service.srp.last.if1` (backlog-adp) | 20.863 | MISS ceiling | 31 srp | 4 | 2 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 18.016 | 34 | 166,997 (1.670) | yes | - |
| backlog-adp | 21.449 | 34 | 134,930 (1.349) | yes | - |
| backlog-adp-refill | 41.073 | 41 | 134,930 (1.349) | yes | - |
| backlog-owed | 360.452 | 82 | 125,719 (1.257) | yes | - |

Composed maximum over the 4 backlog windows: 166,997 CPU cycles (1.670 ms), backlog.
Over the windows that released their whole load only: 166,997 (1.670 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 200,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 317 | 0 | 166,997 (1.670) | fits |
| backlog-adp | 337 | 0 | 134,930 (1.349) | fits |
| backlog-adp-refill | 344 | 0 | 134,930 (1.349) | fits |
| backlog-owed | 382 | 0 | 131,462 (1.315) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 177,071 | 1.771 | 20 | 200 | fits | 162,067 | 117 | 0.638 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 1,042,199 | 10.422 | 20 | 20 | fits | 77,729 | 33 | 0.714 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 166,789 | 1.668 | 20 | 200 | fits | 166,997 | 111 | 0.672 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if1` | 832,211 | 8.322 | 20 | 200 | fits | 80,469 | 36 | 0.705 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 162,530 | 1.625 | 20 | 20 | fits | 166,997 | 111 | 0.672 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 1,108,652 | 11.087 | 20 | 20 | fits | 77,729 | 33 | 0.714 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 166,115 | 1.661 | 20 | 24 | fits | 166,997 | 111 | 0.672 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if1` | 1,277,738 | 12.777 | 20 | 24 | fits | 48,775 | 26 | 0.704 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 165,075 | 1.651 | 20 | 50 | fits | 166,997 | 111 | 0.672 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 750,247 | 7.502 | 20 | 50 | fits | 79,583 | 45 | 0.639 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 326,687 | 3.267 | 18 | 18 | fits | 162,067 | 117 | 0.638 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if1` | 1,747,817 | 17.478 | 18 | 18 | fits | 33,429 | 13 | 0.805 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 728,980 | 7.290 | 20 | 20 | fits | 105,284 | 43 | 0.740 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 81,956 | 0.820 | 20 | 200 | fits | 86,638 | 105 | 0.585 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 826,242 | 8.262 | 20 | 200 | fits | 105,284 | 43 | 0.740 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 82,868 | 0.829 | 20 | 20 | fits | 86,638 | 105 | 0.585 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 1,179,013 | 11.790 | 20 | 20 | fits | 84,236 | 33 | 0.739 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 86,453 | 0.865 | 20 | 24 | fits | 86,638 | 105 | 0.585 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if1` | 1,410,740 | 14.107 | 20 | 24 | fits | 53,718 | 26 | 0.742 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 85,413 | 0.854 | 20 | 50 | fits | 86,638 | 105 | 0.585 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 724,634 | 7.246 | 20 | 50 | fits | 98,599 | 58 | 0.688 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 219,888 | 2.199 | 18 | 18 | fits | 134,930 | 110 | 0.702 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if1` | 2,086,331 | 20.863 | 18 | 18 | MISS ceiling | 35,822 | 13 | 0.798 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 15,723 | 0.157 | 20 | 20 | fits | 45,060 | 20 | 0.787 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 81,956 | 0.820 | 20 | 200 | fits | 86,638 | 105 | 0.585 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 52,813 | 0.528 | 20 | 200 | fits | 45,060 | 20 | 0.787 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 82,868 | 0.829 | 20 | 20 | fits | 86,638 | 105 | 0.585 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 1,161,754 | 11.618 | 20 | 20 | fits | 86,557 | 36 | 0.724 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 86,453 | 0.865 | 20 | 24 | fits | 86,638 | 105 | 0.585 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if1` | 1,393,408 | 13.934 | 20 | 24 | fits | 53,718 | 26 | 0.742 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 85,413 | 0.854 | 20 | 50 | fits | 86,638 | 105 | 0.585 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 724,634 | 7.246 | 20 | 50 | fits | 98,599 | 58 | 0.688 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 219,888 | 2.199 | 18 | 18 | fits | 134,930 | 110 | 0.702 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if1` | 2,069,707 | 20.697 | 18 | 18 | MISS ceiling | 37,812 | 16 | 0.735 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 6,361,927 | 63.619 | 20 | 20 | MISS ceiling | 49,870 | 27 | 0.548 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 36,040,096 | 360.401 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 36,040,021 | 360.400 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 36,039,946 | 360.399 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 36,039,871 | 360.399 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 99,173 | 0.992 | 20 | 200 | fits | 83,682 | 103 | 0.571 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if1` | 773,778 | 7.738 | 20 | 200 | fits | 67,597 | 22 | 0.772 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 94,914 | 0.949 | 20 | 20 | fits | 83,682 | 103 | 0.571 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 1,003,591 | 10.036 | 20 | 20 | fits | 68,423 | 25 | 0.802 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 98,499 | 0.985 | 20 | 24 | fits | 83,682 | 103 | 0.571 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if1` | 6,495,777 | 64.958 | 20 | 24 | MISS ceiling | 30,978 | 23 | 0.528 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 97,459 | 0.975 | 20 | 50 | fits | 83,682 | 103 | 0.571 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 704,686 | 7.047 | 20 | 50 | fits | 78,088 | 44 | 0.715 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 222,723 | 2.227 | 18 | 18 | fits | 125,719 | 97 | 0.697 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if1` | 1,773,104 | 17.731 | 18 | 18 | fits | 35,714 | 16 | 0.781 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
