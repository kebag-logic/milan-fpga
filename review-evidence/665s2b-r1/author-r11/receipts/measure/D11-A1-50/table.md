### 1x1

Clock: CPU 50 MHz, the product's split CPU clock (the Milan clock), bus 100 MHz.

3 of 16 paths and 6 of 49 probe instances miss their budget.

| Path | Interface | Worst instance | ms (bound) | Verdict | Records ahead | Instances | Misses |
|---|---:|---|---:|---|---:|---:|---:|
| an ACMP command behind a full acmp ring | 0 | `backlog.acmp_command.if0` (backlog) | 6.008 (6.502) | fits | 11 acmp | 1 | 0 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | `backlog.adp_available.if0` (backlog-adp) | 4.382 (5.367) | fits | 7 adp | 1 | 0 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | `backlog.adp_available_refill.if0` (backlog-adp-refill) | 0.093 (0.504) | fits | 0 adp | 1 | 0 |
| an event behind 15 others | 0 | `backlog.event.if0` (backlog) | 1.878 (3.388) | fits | 15 events | 1 | 0 |
| a response with 7 frames owed ahead of it | 0 | `backlog.owed.if0` (backlog-owed) | 63.346 (63.743) | MISS ceiling | 7 acmp | 1 | 1 |
| an ACMP command behind the owed input | 0 | `backlog.owed_behind0.if0` (backlog-owed) | at least 360.291 | NEVER ANSWERED | 8 acmp | 4 | 4 |
| ACMP record released under the composed load, first | 0 | `backlog.service.acmp.first.if0` (backlog) | 1.663 | fits | 0 acmp | 4 | 0 |
| ACMP record released under the composed load, last | 0 | `backlog-adp.service.acmp.last.if0` (backlog-adp) | 7.642 | fits | 11 acmp | 4 | 0 |
| ADP record released under the composed load, first | 0 | `backlog.service.adp.first.if0` (backlog) | 1.706 | fits | 0 adp | 4 | 0 |
| ADP record released under the composed load, last | 0 | `backlog-owed.service.adp.last.if0` (backlog-owed) | 5.512 | fits | 7 adp | 4 | 0 |
| AECP record released under the composed load, first | 0 | `backlog.service.aecp.first.if0` (backlog) | 1.699 | fits | 0 aecp | 4 | 0 |
| AECP record released under the composed load, last | 0 | `backlog-owed.service.aecp.last.if0` (backlog-owed) | 64.665 | MISS ceiling | 15 aecp | 4 | 1 |
| MAAP record released under the composed load, first | 0 | `backlog.service.maap.first.if0` (backlog) | 1.688 | fits | 0 maap | 4 | 0 |
| MAAP record released under the composed load, last | 0 | `backlog-owed.service.maap.last.if0` (backlog-owed) | 5.498 | fits | 6 maap | 4 | 0 |
| SRP record released under the composed load, first | 0 | `backlog.service.srp.first.if0` (backlog) | 3.364 | fits | 0 srp | 4 | 0 |
| SRP record released under the composed load, last | 0 | `backlog-adp.service.srp.last.if0` (backlog-adp) | 16.336 | fits | 31 srp | 4 | 0 |

Composed windows: a window that left its load unreleased ran its passes without that work, so its longest pass is a lower bound.

| Group | Window ms | Passes in it | Longest pass, CPU cycles (ms) | Load released | Unreleased |
|---|---:|---:|---:|---|---|
| backlog | 10.893 | 18 | 85,384 (1.708) | yes | - |
| backlog-adp | 16.825 | 19 | 83,962 (1.679) | yes | - |
| backlog-adp-refill | 40.806 | 26 | 83,962 (1.679) | yes | - |
| backlog-owed | 360.342 | 62 | 82,933 (1.659) | yes | - |

Composed maximum over the 4 backlog windows: 85,384 CPU cycles (1.708 ms), backlog.
Over the windows that released their whole load only: 85,384 (1.708 ms), backlog.

Per-pass share (share.py): 18 ms over 9 passes, 2.000 ms, 100,000 CPU cycles. A work pass over it is a finding whatever the rows say.

| Group | Work passes | Over the share | Longest pass, CPU cycles (ms) | Verdict |
|---|---:|---:|---:|---|
| backlog | 292 | 0 | 85,384 (1.708) | fits |
| backlog-adp | 309 | 0 | 83,962 (1.679) | fits |
| backlog-adp-refill | 316 | 0 | 83,962 (1.679) | fits |
| backlog-owed | 347 | 0 | 82,933 (1.659) | fits |

| Path | Probe | CPU cycles | ms | Budget (+W) ms | Ceiling ms | Verdict | Taking pass cycles | Mailbox accesses (model) | Fetch share |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| an event behind 15 others | `backlog.event.if0` | 93,881 | 1.878 | 20 | 200 | fits | 84,000 | 117 | 0.617 |
| an ACMP command behind a full acmp ring | `backlog.acmp_command.if0` | 300,416 | 6.008 | 20 | 20 | fits | 35,746 | 44 | 0.538 |
| ADP record released under the composed load, first | `backlog.service.adp.first.if0` | 85,280 | 1.706 | 20 | 200 | fits | 85,384 | 141 | 0.626 |
| ADP record released under the composed load, last | `backlog.service.adp.last.if0` | 252,701 | 5.054 | 20 | 200 | fits | 40,582 | 55 | 0.522 |
| ACMP record released under the composed load, first | `backlog.service.acmp.first.if0` | 83,151 | 1.663 | 20 | 20 | fits | 85,384 | 141 | 0.626 |
| ACMP record released under the composed load, last | `backlog.service.acmp.last.if0` | 322,452 | 6.449 | 20 | 20 | fits | 35,746 | 44 | 0.538 |
| AECP record released under the composed load, first | `backlog.service.aecp.first.if0` | 84,943 | 1.699 | 20 | 24 | fits | 85,384 | 141 | 0.626 |
| AECP record released under the composed load, last | `backlog.service.aecp.last.if0` | 507,053 | 10.141 | 20 | 24 | fits | 17,864 | 29 | 0.532 |
| MAAP record released under the composed load, first | `backlog.service.maap.first.if0` | 84,423 | 1.688 | 20 | 50 | fits | 85,384 | 141 | 0.626 |
| MAAP record released under the composed load, last | `backlog.service.maap.last.if0` | 251,953 | 5.039 | 20 | 50 | fits | 40,582 | 55 | 0.522 |
| SRP record released under the composed load, first | `backlog.service.srp.first.if0` | 168,196 | 3.364 | 18 | 18 | fits | 84,000 | 117 | 0.617 |
| SRP record released under the composed load, last | `backlog.service.srp.last.if0` | 522,657 | 10.453 | 18 | 18 | fits | 8,086 | 17 | 0.459 |
| an ENTITY_AVAILABLE behind a full adp ring | `backlog.adp_available.if0` | 219,078 | 4.382 | 20 | 20 | fits | 51,957 | 72 | 0.628 |
| ADP record released under the composed load, first | `backlog-adp.service.adp.first.if0` | 54,616 | 1.092 | 20 | 200 | fits | 56,957 | 135 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp.service.adp.last.if0` | 265,730 | 5.315 | 20 | 200 | fits | 51,957 | 72 | 0.628 |
| ACMP record released under the composed load, first | `backlog-adp.service.acmp.first.if0` | 55,072 | 1.101 | 20 | 20 | fits | 56,957 | 135 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp.service.acmp.last.if0` | 382,076 | 7.642 | 20 | 20 | fits | 55,568 | 44 | 0.715 |
| AECP record released under the composed load, first | `backlog-adp.service.aecp.first.if0` | 56,865 | 1.137 | 20 | 24 | fits | 56,957 | 135 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp.service.aecp.last.if0` | 737,779 | 14.756 | 20 | 24 | fits | 36,622 | 29 | 0.767 |
| MAAP record released under the composed load, first | `backlog-adp.service.maap.first.if0` | 56,345 | 1.127 | 20 | 50 | fits | 56,957 | 135 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp.service.maap.last.if0` | 267,568 | 5.351 | 20 | 50 | fits | 51,957 | 72 | 0.628 |
| SRP record released under the composed load, first | `backlog-adp.service.srp.first.if0` | 140,079 | 2.802 | 18 | 18 | fits | 83,962 | 138 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp.service.srp.last.if0` | 816,801 | 16.336 | 18 | 18 | fits | 25,173 | 17 | 0.812 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | `backlog.adp_available_refill.if0` | 4,668 | 0.093 | 20 | 20 | fits | 17,197 | 20 | 0.789 |
| ADP record released under the composed load, first | `backlog-adp-refill.service.adp.first.if0` | 54,616 | 1.092 | 20 | 200 | fits | 56,957 | 135 | 0.503 |
| ADP record released under the composed load, last | `backlog-adp-refill.service.adp.last.if0` | 17,752 | 0.355 | 20 | 200 | fits | 17,197 | 20 | 0.789 |
| ACMP record released under the composed load, first | `backlog-adp-refill.service.acmp.first.if0` | 55,072 | 1.101 | 20 | 20 | fits | 56,957 | 135 | 0.503 |
| ACMP record released under the composed load, last | `backlog-adp-refill.service.acmp.last.if0` | 374,242 | 7.485 | 20 | 20 | fits | 55,499 | 44 | 0.714 |
| AECP record released under the composed load, first | `backlog-adp-refill.service.aecp.first.if0` | 56,865 | 1.137 | 20 | 24 | fits | 56,957 | 135 | 0.503 |
| AECP record released under the composed load, last | `backlog-adp-refill.service.aecp.last.if0` | 743,584 | 14.872 | 20 | 24 | fits | 36,694 | 29 | 0.767 |
| MAAP record released under the composed load, first | `backlog-adp-refill.service.maap.first.if0` | 56,345 | 1.127 | 20 | 50 | fits | 56,957 | 135 | 0.503 |
| MAAP record released under the composed load, last | `backlog-adp-refill.service.maap.last.if0` | 260,000 | 5.200 | 20 | 50 | fits | 44,389 | 62 | 0.615 |
| SRP record released under the composed load, first | `backlog-adp-refill.service.srp.first.if0` | 140,079 | 2.802 | 18 | 18 | fits | 83,962 | 138 | 0.641 |
| SRP record released under the composed load, last | `backlog-adp-refill.service.srp.last.if0` | 815,358 | 16.307 | 18 | 18 | fits | 17,892 | 14 | 0.841 |
| a response with 7 frames owed ahead of it | `backlog.owed.if0` | 3,167,296 | 63.346 | 20 | 20 | MISS ceiling | 22,268 | 25 | 0.644 |
| an ACMP command behind the owed input | `backlog.owed_behind0.if0` | 18,014,565 | 360.291 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind1.if0` | 18,014,527 | 360.291 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind2.if0` | 18,014,490 | 360.290 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| an ACMP command behind the owed input | `backlog.owed_behind3.if0` | 18,014,452 | 360.289 | 20 | 20 | NEVER ANSWERED | 0 | - | 0.000 |
| ADP record released under the composed load, first | `backlog-owed.service.adp.first.if0` | 59,110 | 1.182 | 20 | 200 | fits | 55,011 | 129 | 0.506 |
| ADP record released under the composed load, last | `backlog-owed.service.adp.last.if0` | 275,625 | 5.512 | 20 | 200 | fits | 62,289 | 67 | 0.701 |
| ACMP record released under the composed load, first | `backlog-owed.service.acmp.first.if0` | 56,981 | 1.140 | 20 | 20 | fits | 55,011 | 129 | 0.506 |
| ACMP record released under the composed load, last | `backlog-owed.service.acmp.last.if0` | 367,902 | 7.358 | 20 | 20 | fits | 46,048 | 33 | 0.790 |
| AECP record released under the composed load, first | `backlog-owed.service.aecp.first.if0` | 58,773 | 1.175 | 20 | 24 | fits | 55,011 | 129 | 0.506 |
| AECP record released under the composed load, last | `backlog-owed.service.aecp.last.if0` | 3,233,231 | 64.665 | 20 | 24 | MISS ceiling | 17,084 | 21 | 0.657 |
| MAAP record released under the composed load, first | `backlog-owed.service.maap.first.if0` | 58,253 | 1.165 | 20 | 50 | fits | 55,011 | 129 | 0.506 |
| MAAP record released under the composed load, last | `backlog-owed.service.maap.last.if0` | 274,877 | 5.498 | 20 | 50 | fits | 62,289 | 67 | 0.701 |
| SRP record released under the composed load, first | `backlog-owed.service.srp.first.if0` | 140,959 | 2.819 | 18 | 18 | fits | 82,933 | 131 | 0.668 |
| SRP record released under the composed load, last | `backlog-owed.service.srp.last.if0` | 654,264 | 13.085 | 18 | 18 | fits | 30,108 | 26 | 0.821 |

Bounded waits that timed out (the probe is graded on what the log holds):

- `backlog-owed`: wait tx TIMEOUT
